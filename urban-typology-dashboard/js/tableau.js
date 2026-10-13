// Keep Tableau in normal document flow and resize it with its container.
document.querySelectorAll('.tableauPlaceholder').forEach(function (container) {
  var object = container.querySelector('object');

  function resize() {
    var height = container.clientWidth < 600
      ? container.dataset.mobileHeight : container.dataset.height;
    container.style.height = height + 'px';
    var viz = container.querySelector('iframe') || object;
    viz.style.width = '100%';
    viz.style.height = height + 'px';
    viz.style.minWidth = '0';
  }

  resize();
  new ResizeObserver(resize).observe(container);
  new MutationObserver(resize).observe(container, { childList: true });
});

var tableauScript = document.createElement('script');
tableauScript.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
document.body.appendChild(tableauScript);
