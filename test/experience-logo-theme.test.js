const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const root = path.resolve(__dirname, '..');
const styleSources = [
  '_includes/head/custom.html',
  'assets/css/main.scss',
];

test('dark experience logos use a layout-neutral outline', () => {
  for (const relativePath of styleSources) {
    const source = fs.readFileSync(path.join(root, relativePath), 'utf8');
    const rule = source.match(/\[data-theme="dark"\] \.experience-logo-wrap\s*\{([^}]+)\}/);

    assert.ok(rule, `missing dark logo rule in ${relativePath}`);
    assert.doesNotMatch(rule[1], /border:\s*1px/, `${relativePath} adds a layout-changing border`);
    assert.match(rule[1], /box-shadow:\s*inset\s+0\s+0\s+0\s+1px/, `${relativePath} lacks a layout-neutral outline`);
  }
});
