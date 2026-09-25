# Citation Crawler and EvoMemBench Homepage Update

## Scope

This change has two bounded parts:

1. Make the Google Scholar citation workflow deterministic and prevent multi-hour GitHub Actions runs.
2. Add the accepted EvoMemBench paper and its acceptance announcement to the homepage.

No unrelated homepage content, generated `_site/` files, or existing publication records will be changed.

## Citation crawler

Replace `scholarly==1.5.1` with a small direct HTTP crawler that requests the public Google Scholar author profile, parses the author summary and visible publication rows, and writes the same two artifacts:

- `results/gs_data.json`, retaining the existing top-level `name`, `citedby`, `updated`, and `publications` fields.
- `results/gs_data_shieldsio.json`, retaining `schemaVersion`, `label`, and `message`.

The network call will use a browser-like user agent, a finite request timeout, and a small bounded retry count. Missing or blocked Scholar content will produce an explicit error instead of silently writing incomplete data.

The GitHub Actions workflow will:

- use current checkout and Python setup actions;
- pin a supported Python version;
- grant only the repository-content write permission needed for the statistics branch;
- separate dependency installation, crawling, output validation, and publishing into visible steps;
- set a short job timeout so external failures cannot consume the six-hour runner limit;
- retain the existing `google-scholar-stats` branch and force-publish behavior;
- support both the daily schedule and manual dispatch.

## EvoMemBench publication

Insert EvoMemBench at the top of Publications with:

- Title: `EvoMemBench: Benchmarking Agent Memory from a Self-Evolving Perspective`
- Authors in the supplied order: Yuyao Wang, Zhongjian Zhang, Mo Chi, Kaichi Yu, Yuhan Li, Miao Peng, Bing Tong, Chen Zhang, Yan Zhou, Jia Li
- Only the profile owner's name rendered as `Zhongjian Zhang*` and bolded
- Venue: `NeurIPS'26 · Evaluations & Datasets Track`
- Badge: `CCF-A`
- Paper, Code, and BibTeX controls using the arXiv paper and DSAIL-Memory repository

The Publications heading will contain a compact `* Equal contribution` note aligned on the same row. It will be visually subordinate to the heading, remain legible in dark mode, and wrap safely on narrow screens. No other author will receive an asterisk on this personal homepage.

## News

Add a featured `2026.09` item at the top of News announcing the NeurIPS 2026 Evaluations & Datasets Track acceptance and linking the paper title to arXiv. Keep exactly the latest three News items featured; the previous third featured item becomes a standard item.

## Validation

Before implementation, add tests that fail against the current state and cover:

- parsing a representative Scholar profile into the existing JSON contract;
- rejecting Scholar responses that do not contain a citation total;
- the workflow's bounded timeout, explicit Python setup, separated steps, and output validation;
- the EvoMemBench title, author order, single owner asterisk, heading-level equal-contribution note, venue, links, BibTeX, and newest News entry;
- exactly three featured News items.

After implementation, run the crawler unit tests, existing Node tests, a live local Scholar fetch, `bundle exec jekyll build`, and visual checks at desktop and mobile widths in both light and dark themes.

