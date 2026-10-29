(function (root) {
  function citationStatus(data, now) {
    if (!data || !Number.isInteger(data.citedby) || data.citedby < 0 ||
        typeof data.updated !== 'string') return null;
    // Older snapshots used naive UTC timestamps from the Ubuntu runner.
    var timestamp = data.updated.replace(' ', 'T');
    if (!/(Z|[+-]\d{2}:\d{2})$/.test(timestamp)) timestamp += 'Z';
    var updated = new Date(timestamp);
    var age = (now === undefined ? Date.now() : now) - updated.getTime();
    if (!Number.isFinite(age) || age < -5 * 60 * 1000) return null;
    var date = updated.toISOString().slice(0, 10);
    var stale = age > 7 * 24 * 60 * 60 * 1000;
    return {
      count: data.citedby,
      stale: stale,
      text: stale ? 'Last updated ' + date + ' · Update delayed' : 'Updated ' + date
    };
  }

  if (typeof module === 'object' && module.exports) {
    module.exports = { citationStatus: citationStatus };
  } else {
    root.ScholarStats = { citationStatus: citationStatus };
  }
})(typeof window === 'undefined' ? this : window);
