<#
.SYNOPSIS
    Check whether research notes are stale against their live source pages.
.DESCRIPTION
    Scans docs/sources/ for Markdown notes that contain both a **Source:** URL
    and a **Source updated:** date. For each note, fetches the live page and
    attempts to extract its current "Last updated" date. Reports STALE /
    OK / NEEDS-CLAUDE.

    JavaScript-rendered pages (e.g. Databricks docs) require Claude to verify:
    static HTTP fetches cannot execute JS, so the date is not in the raw HTML.
    Those pages are listed with ready-to-paste URLs at the end of the report.
.EXAMPLE
    pwsh scripts\check-docs-freshness.ps1
    pwsh scripts\check-docs-freshness.ps1 -Course databricks-docs
    pwsh scripts\check-docs-freshness.ps1 -SkipFetch
#>
param (
    [string]$Course    = "*",   # course folder to scan; default = all courses
    [switch]$SkipFetch          # skip HTTP fetches; report metadata only
)

$root       = Split-Path $PSScriptRoot -Parent
$sourcesDir = Join-Path $root "docs\sources"
$searchDir  = if ($Course -eq "*") { $sourcesDir } else { Join-Path $sourcesDir $Course }

$files = Get-ChildItem $searchDir -Filter "*.md" -Recurse -ErrorAction SilentlyContinue |
         Where-Object { $_.Name -ne "index.md" -and $_.Name -ne "page-map.md" }

if (-not $files) { Write-Warning "No .md files found under: $searchDir"; exit 1 }

# Patterns to try against raw (static) HTML.
# Databricks docs are Next.js-rendered: the "Last updated" text is injected by
# JavaScript and will NOT be found by these patterns. Those pages get NEEDS-CLAUDE.
$datePatterns = @(
    '(?i)last[_\-\s]?updated[\s"=>:]+(\w+\s+\d{1,2},?\s+\d{4})',    # "Last updated Apr 13, 2026"
    '(?i)"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})',                  # JSON-LD dateModified
    '(?i)article:modified_time[^>]+content="(\d{4}-\d{2}-\d{2})"',    # OpenGraph meta
    '(?i)data-last-updated="(\d{4}-\d{2}-\d{2})"'                     # data-* attribute
)

function Get-LiveDate([string]$url) {
    try {
        $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 20 -ErrorAction Stop
        foreach ($p in $datePatterns) {
            $m = [regex]::Match($r.Content, $p)
            if ($m.Success) {
                $raw = $m.Groups[1].Value.Trim()
                try { return [datetime]::Parse($raw).ToString("yyyy-MM-dd") }
                catch { return $raw }
            }
        }
        return $null   # date not in static HTML (JS-rendered)
    } catch {
        $msg = $_.Exception.Message -replace "`n.*", ""
        return "ERROR: $($msg.Substring(0, [Math]::Min(60, $msg.Length)))"
    }
}

$results = foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw

    $urlMatch  = [regex]::Match($content, '\*\*Source:\*\*\s*\[[^\]]*\]\((https?://[^)]+)\)')
    $dateMatch = [regex]::Match($content, '\*\*Source updated:\*\*\s*(\d{4}-\d{2}-\d{2})')

    $url      = if ($urlMatch.Success)  { $urlMatch.Groups[1].Value }  else { $null }
    $captured = if ($dateMatch.Success) { $dateMatch.Groups[1].Value } else { $null }

    # Skip non-source files (no URL in metadata block)
    if (-not $url) { continue }

    $liveDate = if (-not $SkipFetch -and $url) { Get-LiveDate $url } else { $null }

    $status = switch ($true) {
        { -not $captured }             { "MISSING-DATE" }
        { $SkipFetch }                 { "SKIPPED" }
        { $liveDate -like "ERROR:*" }  { "FETCH-ERROR" }
        { -not $liveDate }             { "NEEDS-CLAUDE" }
        { $captured -eq $liveDate }    { "OK" }
        default                        { "STALE" }
    }

    [PSCustomObject]@{
        Note     = $file.Name
        Captured = if ($captured) { $captured } else { "(none)" }
        Live     = if ($liveDate) { $liveDate } else { "-" }
        Status   = $status
        URL      = $url
    }
}

if (-not $results) { Write-Host "No notes with Source URL metadata found."; exit 0 }

$results | Format-Table Note, Captured, Live, Status -AutoSize

# --- Grouped summaries ---

$stale   = @($results | Where-Object Status -eq "STALE")
$needs   = @($results | Where-Object Status -eq "NEEDS-CLAUDE")
$missing = @($results | Where-Object Status -eq "MISSING-DATE")
$errors  = @($results | Where-Object Status -eq "FETCH-ERROR")
$ok      = @($results | Where-Object Status -eq "OK")

if ($stale.Count -gt 0) {
    Write-Host "`n=== STALE ($($stale.Count)) ===" -ForegroundColor Red
    foreach ($r in $stale) {
        Write-Host "  $($r.Note)"
        Write-Host "    Captured: $($r.Captured)  |  Live: $($r.Live)"
        Write-Host "    $($r.URL)"
    }
}

if ($missing.Count -gt 0) {
    Write-Host "`n=== Missing 'Source updated' field ($($missing.Count)) ===" -ForegroundColor Yellow
    foreach ($r in $missing) {
        Write-Host "  $($r.Note)"
        if ($r.Live -ne "-") { Write-Host "    Live date: $($r.Live) — add to note metadata" }
        Write-Host "    $($r.URL)"
    }
}

if ($errors.Count -gt 0) {
    Write-Host "`n=== Fetch errors ($($errors.Count)) ===" -ForegroundColor DarkYellow
    foreach ($r in $errors) { Write-Host "  $($r.Note): $($r.Live)" }
}

if ($needs.Count -gt 0) {
    Write-Host "`n=== Needs Claude verification ($($needs.Count)) ===" -ForegroundColor Cyan
    Write-Host "  Page date is JavaScript-rendered — not in static HTML."
    Write-Host ""
    Write-Host "  Paste this prompt into Claude Code:"
    Write-Host "  -------------------------------------------------------"
    Write-Host "  For each URL below, fetch the live page and extract the"
    Write-Host "  'Last updated' date. Compare it to the captured date and"
    Write-Host "  report which notes are stale."
    Write-Host ""
    foreach ($r in $needs) {
        Write-Host "  $($r.Note) | captured $($r.Captured)"
        Write-Host "  $($r.URL)"
        Write-Host ""
    }
    Write-Host "  -------------------------------------------------------"
}

if ($ok.Count -gt 0 -and $stale.Count -eq 0 -and $needs.Count -eq 0 -and $missing.Count -eq 0) {
    Write-Host "`nAll $($ok.Count) pages confirmed up to date." -ForegroundColor Green
}

Write-Host ""
