const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const root = path.resolve(__dirname, '..');

test('the visible News height ends after the fifth complete item', () => {
  const { visibleNewsHeight } = require('../assets/js/news-timeline');

  assert.equal(visibleNewsHeight(100, 462.2, 2.4), 365);
});

test('only the first three News items have the featured weight', () => {
  const page = fs.readFileSync(path.join(root, '_pages/about.md'), 'utf8');
  const news = page.split('<div class="news-timeline">')[1].split('</div>\n\n<h1 id="-publications"')[0];
  const items = [...news.matchAll(/class="news-item(?: news-item--featured)?"/g)];

  assert.equal(items.length, 11);
  assert.deepEqual(items.map((item) => item[0].includes('news-item--featured')).slice(0, 5), [true, true, true, false, false]);

  for (const relativePath of ['assets/css/main.scss', '_includes/head/custom.html']) {
    const css = fs.readFileSync(path.join(root, relativePath), 'utf8');
    assert.match(css, /\.news-date\s*\{[^}]*font-weight:\s*400;/, `${relativePath} should use regular dates by default`);
    assert.match(css, /\.news-item--featured \.news-date\s*\{[^}]*font-weight:\s*700;/, `${relativePath} should bold featured dates`);
  }
});
