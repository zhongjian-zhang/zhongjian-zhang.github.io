const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const workflow = fs.readFileSync(
  path.resolve(__dirname, '../.github/workflows/google_scholar_crawler.yaml'),
  'utf8',
);

test('citation workflow has a bounded and reproducible runtime', () => {
  assert.match(workflow, /workflow_dispatch:/);
  assert.match(workflow, /permissions:\s*\n\s+contents:\s*write/);
  assert.match(workflow, /timeout-minutes:\s*10/);
  assert.match(workflow, /uses:\s*actions\/checkout@v4/);
  assert.match(workflow, /uses:\s*actions\/setup-python@v5/);
  assert.match(workflow, /python-version:\s*["']3\.12["']/);
});

test('citation workflow exposes install, fetch, validation, and publish steps', () => {
  for (const stepName of [
    'Install crawler dependencies',
    'Fetch Scholar citations',
    'Validate citation JSON',
    'Publish citation data',
  ]) {
    assert.match(workflow, new RegExp(`- name: ${stepName}`));
  }

  assert.doesNotMatch(
    workflow,
    /cd \.\/google_scholar_crawler\s+pip3 install[\s\S]+python3 main\.py/,
  );
});

test('daily workflow uses the API without extra page-build queries or ignored failures', () => {
  assert.match(workflow, /SERPAPI_API_KEY: \$\{\{ secrets\.SERPAPI_API_KEY \}\}/);
  assert.match(workflow, /SCHOLAR_SOURCE: serpapi/);
  assert.doesNotMatch(workflow, /page_build:|continue-on-error:|--force/);
  assert.match(workflow, /python -m unittest/);
});
