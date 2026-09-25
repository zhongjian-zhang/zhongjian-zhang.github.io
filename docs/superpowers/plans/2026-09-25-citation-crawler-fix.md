# Citation Crawler Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the hanging `scholarly` dependency chain with a bounded direct Scholar fetch while preserving both JSON output contracts.

**Architecture:** `google_scholar_crawler/main.py` will expose pure HTML parsing and output-building functions plus a small bounded network wrapper. GitHub Actions will install only lightweight pinned dependencies, run the crawler under a job timeout, validate both JSON files, and publish them in a separate step.

**Tech Stack:** Python 3.12, requests, Beautiful Soup, unittest, GitHub Actions YAML, Node test runner for workflow assertions

---

### Task 1: Lock the crawler contract with failing tests

**Files:**
- Create: `google_scholar_crawler/test_main.py`
- Modify: `google_scholar_crawler/main.py`

- [ ] **Step 1: Write the failing parser tests**

Create a representative Scholar HTML fixture containing `#gsc_prf_in`, citation table cells, and two `.gsc_a_tr` rows. Assert that `parse_author_profile(html)` returns the name, integer `citedby`, and a publication dictionary keyed by each `citation_for_view` identifier. Add a second test asserting that HTML without `#gsc_rsb_st` raises `ScholarParseError`.

- [ ] **Step 2: Run the tests and verify RED**

Run: `python3 -m unittest google_scholar_crawler/test_main.py -v`

Expected: FAIL because importing the current script performs an environment-dependent network call and no `parse_author_profile` API exists.

- [ ] **Step 3: Implement the pure parser and output helpers**

Refactor `main.py` behind `if __name__ == "__main__":`. Add `ScholarParseError`, `parse_author_profile(html)`, `build_shields_data(author)`, and `write_results(author, output_dir)`. Parse citation counts from the first statistics row, normalize publication identifiers from `citation_for_view`, and retain `name`, `citedby`, `updated`, and `publications` in `gs_data.json`.

- [ ] **Step 4: Run the tests and verify GREEN**

Run: `python3 -m unittest google_scholar_crawler/test_main.py -v`

Expected: both parser tests PASS.

- [ ] **Step 5: Commit the parser contract**

```bash
git add google_scholar_crawler/main.py google_scholar_crawler/test_main.py
git commit -m "Fix Scholar profile parsing"
```

### Task 2: Add bounded fetching and lightweight dependencies

**Files:**
- Modify: `google_scholar_crawler/main.py`
- Modify: `google_scholar_crawler/test_main.py`
- Modify: `google_scholar_crawler/requirements.txt`

- [ ] **Step 1: Write a failing bounded-fetch test**

Use a local `http.server.ThreadingHTTPServer` fixture that returns HTTP 503 twice and valid Scholar HTML on the third request. Assert that `fetch_profile(url, attempts=3, timeout=1, backoff=0)` succeeds after exactly three requests. Add a server fixture that always returns 503 and assert a clear `ScholarFetchError` after the configured attempts.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python3 -m unittest google_scholar_crawler.test_main.CrawlerTests.test_fetch_retries_are_bounded -v`

Expected: FAIL because `fetch_profile` and `ScholarFetchError` do not exist.

- [ ] **Step 3: Implement the bounded network wrapper**

Use `requests.Session.get` with a browser user agent, explicit per-request timeout, `raise_for_status()`, three attempts, and short exponential backoff. Build the URL from `GOOGLE_SCHOLAR_ID`, request up to 100 publications, parse the response, and write results only after successful validation. Pin `requests` and `beautifulsoup4` in `requirements.txt`; remove `scholarly`, `jsonpickle`, and `bibtexparser`.

- [ ] **Step 4: Run the crawler unit suite and verify GREEN**

Run: `python3 -m unittest google_scholar_crawler/test_main.py -v`

Expected: all parser, retry, and error tests PASS without contacting Google.

- [ ] **Step 5: Commit bounded fetching**

```bash
git add google_scholar_crawler/main.py google_scholar_crawler/test_main.py google_scholar_crawler/requirements.txt
git commit -m "Bound Scholar crawler network retries"
```

### Task 3: Make the Action observable and time-bounded

**Files:**
- Create: `test/citation-workflow.test.js`
- Modify: `.github/workflows/google_scholar_crawler.yaml`

- [ ] **Step 1: Write the failing workflow test**

Assert that the workflow contains `workflow_dispatch`, `permissions: contents: write`, `timeout-minutes`, `actions/checkout@v4`, `actions/setup-python@v5`, Python `3.12`, and separate named steps for installing dependencies, fetching citations, validating JSON, and publishing results. Assert that the old combined `cd ./google_scholar_crawler` block is absent.

- [ ] **Step 2: Run the test and verify RED**

Run: `node --test test/citation-workflow.test.js`

Expected: FAIL on the missing timeout and setup-python assertions.

- [ ] **Step 3: Rewrite the workflow**

Keep the daily cron and `page_build`, add manual dispatch, set a 10-minute job timeout, set up Python 3.12 with pip caching, install pinned requirements, run `python -u main.py`, validate both JSON documents with `python -m json.tool`, and publish the isolated `results` directory using the checkout-provided authenticated remote.

- [ ] **Step 4: Run the workflow test and full Node suite**

Run: `node --test test/citation-workflow.test.js test/*.test.js`

Expected: all tests PASS.

- [ ] **Step 5: Commit the workflow fix**

```bash
git add .github/workflows/google_scholar_crawler.yaml test/citation-workflow.test.js
git commit -m "Fix citation update workflow"
```

### Task 4: Verify the crawler end to end

**Files:**
- Generated locally and not committed: `google_scholar_crawler/results/*.json`

- [ ] **Step 1: Install the pinned crawler environment**

Run: `python3 -m venv /tmp/evomembench-scholar-venv && /tmp/evomembench-scholar-venv/bin/pip install -r google_scholar_crawler/requirements.txt`

Expected: dependency installation completes in under two minutes.

- [ ] **Step 2: Run a live profile fetch**

Run from `google_scholar_crawler/`: `GOOGLE_SCHOLAR_ID=XkeONm0AAAAJ /tmp/evomembench-scholar-venv/bin/python -u main.py`

Expected: both JSON files are created, `name` is `Zhongjian Zhang`, and `citedby` is a positive integer.

- [ ] **Step 3: Validate generated JSON and working-tree scope**

Run: `python3 -m json.tool google_scholar_crawler/results/gs_data.json >/dev/null && python3 -m json.tool google_scholar_crawler/results/gs_data_shieldsio.json >/dev/null && git status --short`

Expected: JSON validation succeeds; generated result files are ignored or removed from the final change set.

