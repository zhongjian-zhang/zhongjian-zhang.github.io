# EvoMemBench Homepage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the EvoMemBench NeurIPS 2026 publication and acceptance news with a single owner asterisk explained in the Publications heading.

**Architecture:** The new content follows the existing static HTML structures in `_pages/about.md`. A small heading-note style is mirrored in both stylesheet sources because this repository currently keeps critical homepage rules in `assets/css/main.scss` and `_includes/head/custom.html`.

**Tech Stack:** Jekyll, Markdown with embedded HTML, Sass/CSS, Node test runner

---

### Task 1: Specify the publication and news markup

**Files:**
- Create: `test/evomembench-content.test.js`
- Modify: `_pages/about.md`

- [ ] **Step 1: Write the failing content tests**

Assert that the first News item is dated `2026.09`, links EvoMemBench to `https://arxiv.org/abs/2605.18421`, and names the NeurIPS 2026 Evaluations & Datasets Track. Assert exactly three featured News items. Assert that the first paper has the verified title and author order, contains exactly one `Zhongjian Zhang*`, does not append an asterisk to Yuyao Wang, uses `NeurIPS'26 · Evaluations & Datasets Track`, links the paper and repository, exposes a BibTeX button, and contains the arXiv BibTeX record.

- [ ] **Step 2: Run the test and verify RED**

Run: `node --test test/evomembench-content.test.js`

Expected: FAIL because the publication and News item are absent.

- [ ] **Step 3: Add the minimal homepage content**

Insert the acceptance News item first and remove `news-item--featured` from the now-fourth item. Add the publication first with CCF-A badge, bold `Zhongjian Zhang*` only, the requested venue label, Paper and Code links, and a `wang2026evomembench` BibTeX block matching the verified arXiv author order.

- [ ] **Step 4: Run the content test and verify GREEN**

Run: `node --test test/evomembench-content.test.js`

Expected: all content assertions PASS.

- [ ] **Step 5: Commit the content**

```bash
git add _pages/about.md test/evomembench-content.test.js
git commit -m "Add EvoMemBench publication and news"
```

### Task 2: Style the equal-contribution heading note

**Files:**
- Modify: `test/evomembench-content.test.js`
- Modify: `_pages/about.md`
- Modify: `assets/css/main.scss`
- Modify: `_includes/head/custom.html`

- [ ] **Step 1: Extend the test for heading-note behavior**

Assert that the Publications heading contains `<span class="section-heading__note">* Equal contribution</span>`. For each stylesheet source, assert a `.section-heading__note` rule with smaller font size, normal weight, muted color, and `margin-left: auto`, plus a dark-theme color rule and a narrow-screen rule that allows safe wrapping.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `node --test test/evomembench-content.test.js`

Expected: FAIL on the missing note markup and styles.

- [ ] **Step 3: Add the heading note and mirrored styles**

Add the note as the final child of the Publications `<h1>`. Style it as a compact right-aligned annotation on desktop, use a muted dark-theme color, and reduce its size on mobile without changing other section headings.

- [ ] **Step 4: Run the full Node suite and Jekyll build**

Run: `node --test test/*.test.js && bundle exec jekyll build`

Expected: all Node tests PASS and Jekyll reports `done`.

- [ ] **Step 5: Commit the heading note**

```bash
git add _pages/about.md assets/css/main.scss _includes/head/custom.html test/evomembench-content.test.js
git commit -m "Label equal contribution on publications"
```

### Task 3: Visual verification

**Files:**
- No additional source files expected

- [ ] **Step 1: Inspect desktop light and dark themes**

Open `http://127.0.0.1:4000/` at a desktop width. Confirm the note shares the Publications heading row, the paper remains first, links are usable, the badge aligns, and the dark-theme note remains readable.

- [ ] **Step 2: Inspect a mobile width**

Set the browser viewport near 390 px. Confirm the Publications heading and note wrap without overlap, the first publication card fits, and the first News item remains readable.

- [ ] **Step 3: Run final repository checks**

Run: `git diff --check && node --test test/*.test.js && python3 -m unittest google_scholar_crawler/test_main.py -v && bundle exec jekyll build`

Expected: no whitespace errors, all tests PASS, and Jekyll builds successfully.

