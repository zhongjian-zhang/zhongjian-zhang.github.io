const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const root = path.resolve(__dirname, '..');
const styleSources = [
  '_includes/head/custom.html',
  'assets/css/main.scss',
];

test('desktop contact rows use a centered fixed-width column', () => {
  for (const relativePath of styleSources) {
    const source = fs.readFileSync(path.join(root, relativePath), 'utf8');

    assert.match(
      source,
      /\.sidebar \.author__urls li\.author__contact-item:not\(\.visitor-map-widget\)\s*\{[^}]*justify-self:\s*center !important;[^}]*width:\s*5rem !important;[^}]*padding-left:\s*0 !important;/,
      `${relativePath} does not center a fixed-width contact column`,
    );
    assert.match(
      source,
      /\.sidebar \.author__contact-item > (?:a|button)[^}]*width:\s*auto !important;/,
      `${relativePath} allows interactive rows to stretch the contact column`,
    );
    assert.match(
      source,
      /\.sidebar \.author__contact-item > i\s*\{[^}]*flex:\s*0 0 1\.25rem !important;/,
      `${relativePath} allows the Visits icon column to shrink`,
    );
  }
});
