// One persistent navbar on every page; no scroll-to-hide behavior.
document.addEventListener('DOMContentLoaded', function () {
  var nav = document.getElementById('mainNav');
  var button = nav.querySelector('.navbar-toggler');
  var menu = document.getElementById('navbarResponsive');

  function closeMenu() {
    menu.classList.remove('show');
    button.setAttribute('aria-expanded', 'false');
    scheduleColors();
  }

  button.addEventListener('click', function () {
    var open = menu.classList.toggle('show');
    button.setAttribute('aria-expanded', String(open));
    scheduleColors();
  });

  nav.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && menu.classList.contains('show')) {
      closeMenu();
      button.focus();
    }
  });

  menu.addEventListener('click', function (event) {
    if (event.target.closest('a')) closeMenu();
  });

  // Use each link's actual position so a photo/white boundary can cross the bar.
  var photoPanels = Array.from(document.querySelectorAll('[data-nav-theme="light"]'));
  var navItems = Array.from(nav.querySelectorAll('a, button'));
  var colorUpdatePending = false;

  function updateColors() {
    colorUpdatePending = false;
    var panels = photoPanels.map(function (panel) { return panel.getBoundingClientRect(); });
    navItems.forEach(function (item) {
      var bounds = item.getBoundingClientRect();
      var x = bounds.left + bounds.width / 2;
      var y = bounds.top + bounds.height / 2;
      var overPhoto = panels.some(function (panel) {
        return x >= panel.left && x < panel.right && y >= panel.top && y < panel.bottom;
      });
      if (menu.contains(item) && menu.classList.contains('show')) overPhoto = false;
      item.classList.toggle('nav-over-photo', overPhoto);
    });
  }

  function scheduleColors() {
    if (!colorUpdatePending) {
      colorUpdatePending = true;
      window.requestAnimationFrame(updateColors);
    }
  }

  window.addEventListener('scroll', scheduleColors, { passive: true });
  window.addEventListener('resize', scheduleColors);
  window.addEventListener('load', scheduleColors);
  new ResizeObserver(scheduleColors).observe(document.body);
  updateColors();

  window.matchMedia('(min-width: 992px)').addEventListener('change', closeMenu);
});
