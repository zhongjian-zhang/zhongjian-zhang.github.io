# Scholar API recovery

Goal: restore current citations and move the daily update from blocked GitHub-runner scraping to the SerpApi Google Scholar Author API, using its free monthly allowance.

The public Scholar page was verified on 2026-10-29: 187 citations, 12 articles. The statistics branch has been restored from that observation. The latest failing Actions job reached HTTP fetching after successful dependency installation; both the direct and translated sources were blocked. Re-running is not a durable remedy.

- [x] Restore the statistics branch from the verified public profile, with an explicit UTC observation timestamp and browser source.
- [x] Reproduce malformed-total, missing-publications and HTTP-200 challenge handling bugs with failing tests; fix them without writing invalid results.
- [ ] Add a tested SerpApi adapter preserving the existing total and per-paper JSON contract. Reject error responses, mismatched author IDs and truncated results. Bound network retries and redact credential-bearing exceptions.
- [ ] Configure the daily workflow to require `SERPAPI_API_KEY`, run regression tests before fetching, and retain existing published files when fetching fails. Remove page-build triggers to limit requests to the daily schedule and intentional manual runs.
- [ ] Display the last successful update date and a visible stale-data notice after seven days. Verify fresh, old, invalid and unavailable responses using behavioral tests.
- [ ] Run Python/Node tests, Jekyll build and desktop/mobile checks. Push the fix, verify Pages, and run the API workflow once the user has configured the free account's repository secret. Do not claim that an API call succeeded before that live verification.

References: https://serpapi.com/pricing and https://serpapi.com/google-scholar-author-api (checked 2026-10-29). One author request includes up to 100 articles; this profile currently needs one request per daily run. No subscription or billing changes are part of this repair.
