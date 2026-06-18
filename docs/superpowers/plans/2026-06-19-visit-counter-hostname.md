# Host-Aware Visit Counter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Show `-----` for shared local-development counters and preserve the raw Busuanzi page-view value on the production hostname.

**Architecture:** Replace numeric compaction with a hostname-aware renderer in `assets/js/visit-count.js`. The renderer observes delayed Busuanzi writes only to enforce the local placeholder; production values pass through unchanged.

**Tech Stack:** Browser JavaScript, Node.js built-in test runner, Jekyll

---

### Task 1: Replace Compact Formatting With Host-Aware Rendering

**Files:**
- Modify: `assets/js/visit-count.js`
- Modify: `test/visit-count.test.js`

- [x] **Step 1: Replace formatter tests with hostname behavior tests**

```javascript
test('replaces a delayed local Busuanzi value with five dashes', async () => {
  const fixture = createCounterFixture('127.0.0.1');
  observeVisitCount(fixture.root);
  fixture.value.textContent = '10301511';
  await new Promise((resolve) => setImmediate(resolve));
  assert.equal(fixture.value.textContent, '-----');
});

test('preserves the raw production Busuanzi value', async () => {
  const fixture = createCounterFixture('zhongjian-zhang.github.io');
  observeVisitCount(fixture.root);
  fixture.value.textContent = '849';
  await new Promise((resolve) => setImmediate(resolve));
  assert.equal(fixture.value.textContent, '849');
});
```

- [x] **Step 2: Run tests and verify RED**

Run: `node --test test/visit-count.test.js`

Expected: FAIL because the current implementation converts local values to `10.3M` and still exports obsolete formatter behavior.

- [x] **Step 3: Implement hostname-aware rendering**

```javascript
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
```

Export `isLocalHostname` and `observeVisitCount`; remove `formatVisitCount` and all `K/M` formatting.

- [x] **Step 4: Verify tests and build**

Run: `node --test test/visit-count.test.js && bundle exec jekyll build && git diff --check`

Expected: hostname tests pass, Jekyll exits 0, and no whitespace errors appear.

- [x] **Step 5: Verify browser behavior**

Reload `http://127.0.0.1:4000/` and confirm the counter reads exactly `-----`. Verify the production-path unit test preserves `849` without suffixes.
