import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
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
    citation_text = citation_node.get_text(" ", strip=True)
    if not re.fullmatch(r"[0-9][0-9,\s]*", citation_text):
        raise ScholarParseError("Scholar citation total is not a number")

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

    if not publications and _integer(citation_text) > 0:
        raise ScholarParseError("Scholar response is missing publications")

    return {
        "name": name_node.get_text(" ", strip=True),
        "citedby": _integer(citation_text),
        "updated": datetime.now(timezone.utc).isoformat(),
        "publications": publications,
    }


def build_shields_data(author: dict) -> dict:
    return {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(author["citedby"]),
    }


def _api_count(value) -> int:
    if type(value) is not int or value < 0:
        raise ScholarParseError("SerpApi returned an invalid citation count")
    return value


def parse_serpapi_profile(data: dict, scholar_id: str) -> dict:
    """Convert a complete author response without publishing vendor metadata."""
    try:
        if data.get("error") or data["search_metadata"]["status"] != "Success":
            raise ScholarParseError("SerpApi did not return a successful author response")
        if data["search_parameters"]["author_id"] != scholar_id:
            raise ScholarParseError("SerpApi returned a different author")
        if data.get("serpapi_pagination", {}).get("next"):
            raise ScholarParseError("SerpApi profile exceeds 100 articles; pagination is required")
        name = data["author"]["name"]
        if not isinstance(name, str) or not name.strip():
            raise ScholarParseError("SerpApi response is missing the author name")
        total = _api_count(next(
            row["citations"]["all"] for row in data["cited_by"]["table"]
            if "citations" in row
        ))
        articles = data["articles"]
        if not isinstance(articles, list) or (total > 0 and not articles):
            raise ScholarParseError("SerpApi response is missing publications")
        publications = {}
        for article in articles:
            publication_id = article["citation_id"]
            if (not isinstance(publication_id, str)
                    or not publication_id.startswith(scholar_id + ":")
                    or publication_id in publications):
                raise ScholarParseError("SerpApi returned an invalid or duplicate publication ID")
            title = article["title"]
            if not isinstance(title, str) or not title.strip():
                raise ScholarParseError("SerpApi returned an article without a title")
            # Scholar leaves the cited-by cell empty for uncited publications.
            count = article.get("cited_by", {}).get("value")
            publications[publication_id] = {
                "author_pub_id": publication_id,
                "bib": {
                    "title": title,
                    "author": article.get("authors", ""),
                    "citation": article.get("publication", ""),
                    "pub_year": str(article.get("year") or ""),
                },
                "num_citations": 0 if count is None else _api_count(count),
            }
    except (KeyError, TypeError, AttributeError, StopIteration):
        raise ScholarParseError("SerpApi returned an incomplete author profile") from None
    return {
        "name": name.strip(),
        "citedby": total,
        "updated": datetime.now(timezone.utc).isoformat(),
        "publications": publications,
        "scholar_id": scholar_id,
        "source": "serpapi",
    }


def fetch_serpapi_profile(
    scholar_id: str, api_key: str, *, attempts: int = 2,
    timeout: float = 45, backoff: float = 2,
) -> dict:
    if not api_key.strip():
        raise ScholarFetchError("SERPAPI_API_KEY is required; configure the repository Actions secret")
    if attempts < 1:
        raise ValueError("attempts must be at least 1")
    params = {
        "engine": "google_scholar_author", "author_id": scholar_id,
        "hl": "en", "num": 100, "api_key": api_key,
    }
    reason = "no response"
    with requests.Session() as session:
        for attempt in range(1, attempts + 1):
            try:
                response = session.get("https://serpapi.com/search.json", params=params,
                                       timeout=timeout, allow_redirects=False)
                if response.status_code != 200:
                    reason = f"HTTP {response.status_code}"
                    # Authentication, quota and other client errors need action,
                    # not repeated requests. Never print the credential-bearing URL.
                    if response.status_code < 500:
                        break
                else:
                    return parse_serpapi_profile(response.json(), scholar_id)
            except requests.RequestException:
                reason = "network error or invalid JSON response"
            except ScholarParseError:
                reason = "invalid or incomplete author response"
                break
            if attempt < attempts and backoff > 0:
                time.sleep(backoff * attempt)
    # Do not chain requests exceptions: their URLs can contain api_key.
    raise ScholarFetchError(
        f"SerpApi fetch failed: {reason}. Check API key, quota and service status. "
        "Previously published citation data has not been changed."
    ) from None


def fetch_profile(
    url: str,
    *,
    fallback_url: Optional[str] = None,
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
    request_count = 0
    source_urls = [url] + ([fallback_url] if fallback_url else [])
    with requests.Session() as session:
        for source_index, source_url in enumerate(source_urls):
            for attempt in range(1, attempts + 1):
                try:
                    request_count += 1
                    response = session.get(source_url, headers=headers, timeout=timeout)
                    response.raise_for_status()
                    # A challenge page can return HTTP 200. Validate before choosing
                    # this source so a valid fallback is still attempted.
                    parse_author_profile(response.text)
                    return response.text
                except ScholarParseError as error:
                    last_error = error
                    print("Scholar returned an incomplete profile; trying next source", flush=True)
                    break
                except requests.HTTPError as error:
                    last_error = error
                    if error.response is not None and error.response.status_code in (403, 429):
                        if source_index == 0 and fallback_url:
                            print(f"Direct Scholar access returned HTTP {error.response.status_code}; trying translated profile", flush=True)
                        break
                except requests.RequestException as error:
                    last_error = error

                if attempt < attempts and backoff > 0:
                    time.sleep(backoff * (2 ** (attempt - 1)))

    raise ScholarFetchError(
        f"Unable to fetch Google Scholar profile after {request_count} attempts: "
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

    if os.environ.get("SCHOLAR_SOURCE") == "serpapi" or os.environ.get("SERPAPI_API_KEY"):
        author = fetch_serpapi_profile(scholar_id, os.environ.get("SERPAPI_API_KEY", ""))
        print(f"Fetched {author['citedby']} citations across {len(author['publications'])} papers via SerpApi")
        write_results(author, Path(__file__).resolve().parent / "results")
        return

    query = urlencode({"user": scholar_id, "hl": "en", "pagesize": 100})
    profile_url = f"https://scholar.google.com/citations?{query}"
    translated_query = urlencode({
        "user": scholar_id,
        "hl": "en",
        "pagesize": 100,
        "_x_tr_sl": "auto",
        "_x_tr_tl": "en",
        "_x_tr_hl": "en",
    })
    fallback_url = f"https://scholar-google-com.translate.goog/citations?{translated_query}"
    author = parse_author_profile(fetch_profile(profile_url, fallback_url=fallback_url))
    print(json.dumps(author, indent=2, ensure_ascii=False))
    write_results(author, Path(__file__).resolve().parent / "results")


if __name__ == "__main__":
    main()
