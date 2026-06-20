(function () {
  // outerWidth >= availWidth when Windows maximizes (invisible resize border extends off-screen)
  // Observed values: maximized outerWidth=1936 vs availWidth=1920; not-maximized outerWidth=974
  function isMaximized() {
    return window.outerWidth >= screen.availWidth;
  }

  function applyState() {
    var max = isMaximized();
    document.body.classList.toggle('is-maximized', max);
    document.querySelectorAll('.md-sidebar').forEach(function (el) {
      el.style.setProperty('display', max ? '' : 'none', 'important');
    });
  }

  function setup(sidebar, storageKey, collapseChar, expandChar) {
    var btn = document.createElement('button');
    btn.className = 'sidebar-toggle';
    btn.title = 'Toggle sidebar';

    var collapsed = localStorage.getItem(storageKey) === '1';
    if (collapsed) sidebar.classList.add('is-collapsed');
    btn.textContent = collapsed ? expandChar : collapseChar;

    btn.addEventListener('click', function () {
      var nowCollapsed = sidebar.classList.toggle('is-collapsed');
      localStorage.setItem(storageKey, nowCollapsed ? '1' : '0');
      btn.textContent = nowCollapsed ? expandChar : collapseChar;
    });

    sidebar.prepend(btn);
  }

  document.addEventListener('DOMContentLoaded', function () {
    applyState();
    var nav = document.querySelector('.md-sidebar--primary');
    var toc = document.querySelector('.md-sidebar--secondary');
    if (nav) setup(nav, 'sidebar-nav-collapsed', '◀', '▶');
    if (toc) setup(toc, 'sidebar-toc-collapsed', '▶', '◀');
  });

  window.addEventListener('load', function () { setTimeout(applyState, 100); });
  window.addEventListener('resize', applyState);
})();
