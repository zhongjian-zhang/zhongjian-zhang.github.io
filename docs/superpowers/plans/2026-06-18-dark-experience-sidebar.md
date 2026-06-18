# Dark Experience Cards and Sidebar Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve dark-theme experience logo readability, align desktop profile contacts, and keep large visit counts compact.

**Architecture:** Keep visual rules in the repository's existing mirrored style blocks in `_includes/head/custom.html` and `assets/css/main.scss`. Add one small dependency-free browser script for formatting the external counter value, with a Node unit test covering the numeric contract.

**Tech Stack:** Jekyll, Liquid/HTML, Sass/CSS, browser JavaScript, Node.js built-in test runner

---

### Task 1: Compact Visit Count Formatter

**Files:**
- Create: `assets/js/visit-count.js`
- Create: `test/visit-count.test.js`
- Modify: `_includes/scripts.html:7`

- [x] **Step 1: Write the failing formatter test**

```javascript
const test = require('node:test');
const assert = require('node:assert/strict');
const { formatVisitCount } = require('../assets/js/visit-count.js');

test('formats visit counts using compact suffixes', () => {
  assert.equal(formatVisitCount('32680'), '32.7K');
  assert.equal(formatVisitCount('10300483'), '10.3M');
  assert.equal(formatVisitCount('999'), '999');
});

test('preserves non-numeric placeholders', () => {
  assert.equal(formatVisitCount(''), '');
  assert.equal(formatVisitCount('--'), '--');
});
```

- [x] **Step 2: Run the formatter test and verify RED**

Run: `node --test test/visit-count.test.js`

Expected: FAIL because `assets/js/visit-count.js` does not exist.

- [x] **Step 3: Implement the formatter and counter observer**

```javascript
(function(root) {
  function formatVisitCount(value) {
    var text = String(value == null ? '' : value).trim();
    var count = Number(text.replace(/,/g, ''));
    if (!text || !Number.isFinite(count)) return text;
    if (count >= 1000000) return (count / 1000000).toFixed(1).replace(/\.0$/, '') + 'M';
    if (count >= 1000) return (count / 1000).toFixed(1).replace(/\.0$/, '') + 'K';
    return String(count);
  }

  function compactVisitCount() {
    var value = root.document && root.document.getElementById('busuanzi_value_site_pv');
    if (!value) return;
    var formatted = formatVisitCount(value.textContent);
    if (formatted !== value.textContent) value.textContent = formatted;
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { formatVisitCount: formatVisitCount };
  }

  if (root.document) {
    new MutationObserver(compactVisitCount).observe(root.document.documentElement, {
      childList: true,
      subtree: true
    });
    root.document.addEventListener('DOMContentLoaded', compactVisitCount);
  }
})(typeof window !== 'undefined' ? window : globalThis);
```

Include `/assets/js/visit-count.js` after the Busuanzi script in `_includes/scripts.html`.

- [x] **Step 4: Run the formatter test and verify GREEN**

Run: `node --test test/visit-count.test.js`

Expected: 2 tests pass with 0 failures.

### Task 2: Experience Cards and Desktop Sidebar

**Files:**
- Modify: `_includes/head/custom.html:451-580,1158-1175`
- Modify: `assets/css/main.scss:767-896,1474-1491`

- [x] **Step 1: Record the current visual contract**

In the browser, confirm the dark experience background is `rgb(23, 32, 51)`, logo wrappers are transparent, and desktop contact rows use `padding-left: 2.25rem`.

- [x] **Step 2: Add the minimal mirrored CSS changes**

Apply the same rules in both style files:

```css
@media (min-width: 1024px) {
  .sidebar .author__contact-item {
    padding-left: 2.75rem !important;
  }
}

[data-theme="dark"] .experience-item {
  border-color: #34445b !important;
  border-left-color: #60a5fa !important;
  background: #223047 !important;
}

[data-theme="dark"] .experience-logo-wrap {
  box-sizing: border-box;
  padding: 0.28rem 0.4rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.9) !important;
}
```

Keep the visitor map rules unchanged so it remains centered.

- [x] **Step 3: Verify source consistency**

Run: `git diff --check && rg -n "padding-left: 2.75rem|background: #223047|rgba\\(255, 255, 255, 0.9\\)" _includes/head/custom.html assets/css/main.scss`

Expected: no whitespace errors and each rule appears in both style files.

### Task 3: Build and Responsive Visual Verification

**Files:**
- Verify: generated site at `_site/`

- [x] **Step 1: Run automated verification**

Run: `node --test test/visit-count.test.js && bundle exec jekyll build`

Expected: formatter tests pass and Jekyll exits with status 0.

- [x] **Step 2: Verify desktop dark theme**

Reload `http://127.0.0.1:4000/` at approximately `1117x863`. Confirm all three logos are legible on consistent light backings, the cards are visibly lighter than the page, contact rows shift right, the map remains centered, and the visit value uses compact notation.

- [x] **Step 3: Verify desktop light theme**

Toggle to light theme and confirm the experience cards retain their existing white treatment and logo sizing.

- [x] **Step 4: Verify mobile layout**

Set a `390x844` viewport. Confirm experience cards stack without overflow, compact logo backings fit the card width, and the compact mobile profile links remain centered.

- [x] **Step 5: Review final diff**

Run: `git diff --check && git status --short && git diff --stat`

Expected: only the planned style, script, test, and plan files are changed.
