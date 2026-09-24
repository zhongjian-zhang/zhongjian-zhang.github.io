(function () {
  function visibleNewsHeight(timelineTop, fifthItemBottom, paddingBottom) {
    return Math.ceil(fifthItemBottom - timelineTop + paddingBottom);
  }

  function updateNewsTimelineHeight() {
    const timeline = document.querySelector('.news-timeline');
    if (!timeline) return;

    const items = timeline.querySelectorAll('.news-item');
    if (items.length <= 5) {
      timeline.style.maxHeight = 'none';
      return;
    }

    const scrollTop = timeline.scrollTop;
    timeline.style.maxHeight = 'none';

    const paddingBottom = parseFloat(window.getComputedStyle(timeline).paddingBottom) || 0;
    const height = visibleNewsHeight(
      timeline.getBoundingClientRect().top,
      items[4].getBoundingClientRect().bottom,
      paddingBottom
    );

    timeline.style.maxHeight = `${height}px`;
    timeline.scrollTop = scrollTop;
  }

  if (typeof document !== 'undefined') {
    const initialize = () => {
      updateNewsTimelineHeight();
      window.addEventListener('resize', updateNewsTimelineHeight);
      if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(updateNewsTimelineHeight);
      }
    };

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initialize);
    } else {
      initialize();
    }
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { visibleNewsHeight };
  }
})();
