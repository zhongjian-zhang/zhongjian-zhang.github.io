const test = require('node:test');
const assert = require('node:assert/strict');
const { citationStatus } = require('../assets/js/scholar-stats.js');

const now = Date.parse('2026-10-29T06:00:00Z');

test('fresh citations expose the successful update date', () => {
  const status = citationStatus({ citedby: 187, updated: '2026-10-29T05:00:00+00:00' }, now);
  assert.equal(status.count, 187);
  assert.equal(status.text, 'Updated 2026-10-29');
  assert.equal(status.stale, false);
});

test('old data stays visible and is explicitly marked stale', () => {
  const status = citationStatus({ citedby: 181, updated: '2026-10-13 15:26:21.356379' }, now);
  assert.equal(status.count, 181);
  assert.equal(status.text, 'Last updated 2026-10-13 · Update delayed');
  assert.equal(status.stale, true);
});

test('invalid or unavailable data never becomes a zero citation count', () => {
  for (const data of [null, {}, { citedby: '187' }, { citedby: -1 },
    { citedby: 187, updated: 'invalid' }, { citedby: 187, updated: '2099-01-01' }]) {
    assert.equal(citationStatus(data, now), null);
  }
});

test('a genuine zero is accepted with a valid timestamp', () => {
  assert.equal(citationStatus({ citedby: 0, updated: '2026-10-29T00:00:00Z' }, now).count, 0);
});
