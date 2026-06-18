(function(root, factory) {
  var api = factory(root);

  if (typeof module === 'object' && module.exports) {
    module.exports = api;
  } else {
    root.VisitCount = api;
  }
})(typeof window !== 'undefined' ? window : globalThis, function(root) {
  function isLocalHostname(hostname) {
    return hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '::1';
  }

  function observeVisitCount(targetRoot) {
    var document = targetRoot && targetRoot.document;
    var hostname = targetRoot && targetRoot.location && targetRoot.location.hostname;
    if (!document || !isLocalHostname(hostname)) return;

    function renderLocalPlaceholder() {
      var value = document.getElementById('busuanzi_value_site_pv');
      if (value && value.textContent !== '-----') value.textContent = '-----';
    }

    if (typeof targetRoot.MutationObserver === 'function' && document.documentElement) {
      new targetRoot.MutationObserver(renderLocalPlaceholder).observe(document.documentElement, {
        childList: true,
        subtree: true
      });
    }

    document.addEventListener('DOMContentLoaded', renderLocalPlaceholder);
    renderLocalPlaceholder();
  }

  observeVisitCount(root);

  return {
    isLocalHostname: isLocalHostname,
    observeVisitCount: observeVisitCount
  };
});
