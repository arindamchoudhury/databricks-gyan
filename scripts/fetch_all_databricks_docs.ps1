$PYTHON = "C:\Users\arind\miniforge3\envs\notes-fetch\python.exe"
$SCRIPT = "c:\opt\learn\databricks\notes\scripts\fetch_page.py"
$CACHE  = "c:\opt\learn\databricks\notes\cache\web"
$LOG    = "c:\opt\learn\databricks\notes\cache\web\_fetch-log.txt"

$pages = @(
    @{ slug = "notebook-debugger";            url = "https://docs.databricks.com/aws/en/notebooks/debugger" },
    @{ slug = "serverless-notebooks";         url = "https://docs.databricks.com/aws/en/compute/serverless/notebooks" },
    @{ slug = "serverless-jobs";              url = "https://docs.databricks.com/aws/en/jobs/run-serverless-jobs" },
    @{ slug = "serverless-pipelines";         url = "https://docs.databricks.com/aws/en/ldp/serverless" },
    @{ slug = "serverless-limitations";       url = "https://docs.databricks.com/aws/en/compute/serverless/limitations" },
    @{ slug = "classic-compute-overview";     url = "https://docs.databricks.com/aws/en/compute/use-compute" },
    @{ slug = "classic-compute-configure";    url = "https://docs.databricks.com/aws/en/compute/configure" },
    @{ slug = "standard-compute-overview";    url = "https://docs.databricks.com/aws/en/compute/standard-overview" },
    @{ slug = "dedicated-compute-overview";   url = "https://docs.databricks.com/aws/en/compute/dedicated-overview" },
    @{ slug = "compute-pools";                url = "https://docs.databricks.com/aws/en/compute/pool-index" },
    @{ slug = "sql-warehouse-overview";       url = "https://docs.databricks.com/aws/en/compute/sql-warehouse/" },
    @{ slug = "sql-warehouse-types";          url = "https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-types" },
    @{ slug = "photon";                       url = "https://docs.databricks.com/aws/en/compute/photon" },
    @{ slug = "lakeguard";                    url = "https://docs.databricks.com/aws/en/compute/lakeguard" },
    @{ slug = "notebooks-overview";           url = "https://docs.databricks.com/aws/en/notebooks/" },
    @{ slug = "notebook-dashboards";          url = "https://docs.databricks.com/aws/en/notebooks/dashboards" },
    @{ slug = "notebook-testing";             url = "https://docs.databricks.com/aws/en/notebooks/testing" },
    @{ slug = "notebook-widgets";             url = "https://docs.databricks.com/aws/en/notebooks/widgets" },
    @{ slug = "notebook-workflows";           url = "https://docs.databricks.com/aws/en/notebooks/notebook-workflows" },
    @{ slug = "notebook-ipywidgets";          url = "https://docs.databricks.com/aws/en/notebooks/ipywidgets" },
    @{ slug = "notebook-share-code";          url = "https://docs.databricks.com/aws/en/notebooks/share-code" },
    @{ slug = "notebook-best-practices";      url = "https://docs.databricks.com/aws/en/notebooks/best-practices" },
    @{ slug = "spark-ui-guide";               url = "https://docs.databricks.com/aws/en/optimizations/spark-ui-guide" },
    @{ slug = "optimize-data-workloads-guide"; url = "https://www.databricks.com/discover/pages/optimize-data-workloads-guide" },
    @{ slug = "failing-spark-jobs";           url = "https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/failing-spark-jobs" },
    @{ slug = "long-spark-stage";             url = "https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/long-spark-stage" },
    @{ slug = "long-spark-stage-page";        url = "https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/long-spark-stage-page" },
    @{ slug = "spark-memory-issues";          url = "https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/spark-memory-issues" },
    @{ slug = "long-spark-stage-io";          url = "https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/long-spark-stage-io" },
    @{ slug = "slow-spark-stage-low-io";      url = "https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/slow-spark-stage-low-io" },
    @{ slug = "spark-rewriting-data";         url = "https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/spark-rewriting-data" },
    @{ slug = "one-spark-task";               url = "https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/one-spark-task" },
    @{ slug = "losing-spot-instances";        url = "https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/losing-spot-instances" },
    @{ slug = "sql-join-hints";               url = "https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-hints" },
    @{ slug = "aqe";                          url = "https://docs.databricks.com/aws/en/optimizations/aqe" }
)

$total = $pages.Count
$done  = 0
$failed = @()
$batchStart = Get-Date

"=== Batch fetch started $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" | Tee-Object -FilePath $LOG -Append

foreach ($p in $pages) {
    $done++
    $pageStart = Get-Date
    Write-Host "[$done/$total] Fetching: $($p.slug)" -ForegroundColor Cyan
    "[$done/$total] $($p.slug)  $($p.url)" | Add-Content $LOG

    $output = & $PYTHON $SCRIPT $p.url --slug $p.slug --out $CACHE 2>&1
    $exitCode = $LASTEXITCODE
    $elapsed = [int]((Get-Date) - $pageStart).TotalSeconds

    $imgLine = $output | Where-Object { $_ -match "Images: captured" } | Select-Object -Last 1
    $imgs = if ($imgLine) { $imgLine } else { "no images" }

    if ($exitCode -eq 0) {
        Write-Host "  OK  ${elapsed}s  $imgs" -ForegroundColor Green
        "  OK  ${elapsed}s  $imgs" | Add-Content $LOG
    } else {
        Write-Host "  FAIL  ${elapsed}s" -ForegroundColor Red
        $output | ForEach-Object { "    $_" | Add-Content $LOG }
        $failed += $p.slug
    }
}

$totalElapsed = [int]((Get-Date) - $batchStart).TotalSeconds
"" | Add-Content $LOG
"=== Done in ${totalElapsed}s. Failed: $($failed.Count) ===" | Tee-Object -FilePath $LOG -Append
if ($failed) { "Failed: $($failed -join ', ')" | Tee-Object -FilePath $LOG -Append }
