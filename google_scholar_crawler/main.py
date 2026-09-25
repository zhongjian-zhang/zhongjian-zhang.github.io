import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

import requests
from bs4 import BeautifulSoup


class ScholarParseError(ValueError):
    """Raised when a Google Scholar profile response is incomplete."""


class ScholarFetchError(RuntimeError):
    """Raised when a Google Scholar profile cannot be fetched in time."""


def _integer(text: str) -> int:
    digits = re.sub(r"[^0-9]", "", text or "")
    return int(digits) if digits else 0


def parse_author_profile(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    name_node = soup.select_one("#gsc_prf_in")
    citation_node = soup.select_one("#gsc_rsb_st .gsc_rsb_std")
    if name_node is None:
        raise ScholarParseError("Scholar response is missing the author name")
    if citation_node is None:
        raise ScholarParseError("Scholar response is missing the citation total")

    publications = {}
    for row in soup.select(".gsc_a_tr"):
        title_node = row.select_one(".gsc_a_at")
        if title_node is None:
            continue
        publication_id = parse_qs(
            urlparse(title_node.get("href", "")).query
        ).get("citation_for_view", [""])[0]
        if not publication_id:
            continue

        details = row.select(".gsc_a_t .gs_gray")
        authors = details[0].get_text(" ", strip=True) if details else ""
        citation = details[1].get_text(" ", strip=True) if len(details) > 1 else ""
        year_node = row.select_one(".gsc_a_y span")
        count_node = row.select_one(".gsc_a_c")
        publications[publication_id] = {
            "author_pub_id": publication_id,
            "bib": {
                "title": title_node.get_text(" ", strip=True),
                "author": authors,
                "citation": citation,
                "pub_year": year_node.get_text(strip=True) if year_node else "",
            },
            "num_citations": _integer(
                count_node.get_text(" ", strip=True) if count_node else ""
            ),
        }

    return {
        "name": name_node.get_text(" ", strip=True),
        "citedby": _integer(citation_node.get_text(" ", strip=True)),
        "updated": str(datetime.now()),
        "publications": publications,
    }


def build_shields_data(author: dict) -> dict:
    return {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(author["citedby"]),
    }


def fetch_profile(
    url: str,
    *,
    attempts: int = 3,
    timeout: float = 20,
    backoff: float = 2,
) -> str:
    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    headers = {
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        ),
    }
    last_error = None
    with requests.Session() as session:
        for attempt in range(1, attempts + 1):
            try:
                response = session.get(url, headers=headers, timeout=timeout)
                response.raise_for_status()
                return response.text
            except requests.RequestException as error:
                last_error = error
                if attempt < attempts and backoff > 0:
                    time.sleep(backoff * (2 ** (attempt - 1)))

    raise ScholarFetchError(
        f"Unable to fetch Google Scholar profile after {attempts} attempts: "
        f"{last_error}"
    ) from last_error


def write_results(author: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "gs_data.json").open("w", encoding="utf-8") as outfile:
        json.dump(author, outfile, ensure_ascii=False)
    with (output_dir / "gs_data_shieldsio.json").open(
        "w", encoding="utf-8"
    ) as outfile:
        json.dump(build_shields_data(author), outfile, ensure_ascii=False)


def main() -> None:
    scholar_id = os.environ.get("GOOGLE_SCHOLAR_ID", "").strip()
    if not scholar_id:
        raise RuntimeError("GOOGLE_SCHOLAR_ID is required")

    query = urlencode({"user": scholar_id, "hl": "en", "pagesize": 100})
    profile_url = f"https://scholar.google.com/citations?{query}"
    author = parse_author_profile(fetch_profile(profile_url))
    print(json.dumps(author, indent=2, ensure_ascii=False))
    write_results(author, Path(__file__).resolve().parent / "results")


if __name__ == "__main__":
    main()
