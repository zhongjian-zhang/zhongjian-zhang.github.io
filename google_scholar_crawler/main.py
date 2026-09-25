import json
import os
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup


class ScholarParseError(ValueError):
    """Raised when a Google Scholar profile response is incomplete."""


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


def write_results(author: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "gs_data.json").open("w", encoding="utf-8") as outfile:
        json.dump(author, outfile, ensure_ascii=False)
    with (output_dir / "gs_data_shieldsio.json").open(
        "w", encoding="utf-8"
    ) as outfile:
        json.dump(build_shields_data(author), outfile, ensure_ascii=False)


def main() -> None:
    from scholarly import scholarly

    author = scholarly.search_author_id(os.environ["GOOGLE_SCHOLAR_ID"])
    scholarly.fill(
        author, sections=["basics", "indices", "counts", "publications"]
    )
    author["updated"] = str(datetime.now())
    author["publications"] = {
        publication["author_pub_id"]: publication
        for publication in author["publications"]
    }
    print(json.dumps(author, indent=2, default=str))
    write_results(author, Path("results"))


if __name__ == "__main__":
    main()
