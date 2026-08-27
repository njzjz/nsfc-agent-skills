#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Search academic literature using the OpenAlex API (free, no API key required).

Usage:
    uv run search_literature.py "deep potential molecular dynamics" [--limit 10] [--year-from 2020] [--sort cited_by_count|relevance_score|publication_date]

Output: JSON list of papers with title, DOI, authors, year, citation count, abstract.
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

OPENALEX_API = "https://api.openalex.org/works"
USER_AGENT = "nsfc-agent-skills/0.1 (OpenAlex literature helper)"


def _parse_work(work: dict) -> dict:
    """Normalize one OpenAlex work while tolerating nullable API fields."""
    authors = []
    for authorship in work.get("authorships") or []:
        author = authorship.get("author") or {}
        name = author.get("display_name") or ""
        if name:
            authors.append(name)

    doi = work.get("doi") or ""
    doi = doi.removeprefix("https://doi.org/")

    abstract_index = work.get("abstract_inverted_index") or {}
    word_positions = [
        (position, word)
        for word, positions in abstract_index.items()
        for position in positions
    ]
    word_positions.sort()
    abstract = " ".join(word for _, word in word_positions)

    primary_location = work.get("primary_location") or {}
    source = primary_location.get("source") or {}
    return {
        "title": work.get("title") or "",
        "doi": doi,
        "authors": authors[:5],
        "year": work.get("publication_year"),
        "cited_by_count": work.get("cited_by_count") or 0,
        "journal": source.get("display_name") or "",
        "abstract": abstract[:500],
        "openalex_id": work.get("id") or "",
    }


def search(
    query: str,
    limit: int = 10,
    year_from: int | None = None,
    sort: str = "relevance_score",
    mailto: str | None = None,
) -> list[dict]:
    """Search OpenAlex and return normalized records.

    ``mailto`` is optional. Supply a real contact address to use OpenAlex's
    polite pool; the script deliberately does not ship a fake default address.
    """
    query = query.strip()
    if not query:
        raise ValueError("query must not be empty")
    if not 1 <= limit <= 50:
        raise ValueError("limit must be between 1 and 50")

    # Future-dated repository deposits can dominate publication-date sorting.
    # Limit results to current journal and conference records by default.
    filters = [
        f"to_publication_date:{datetime.now(timezone.utc).date().isoformat()}",
        "primary_location.source.type:journal|conference",
    ]
    if year_from:
        filters.append(f"from_publication_date:{year_from}-01-01")

    params = {
        "search": query,
        "per_page": limit,
        "filter": ",".join(filters),
    }
    if mailto:
        params["mailto"] = mailto
    # OpenAlex sorts by relevance by default when using search; only add sort for other fields
    if sort != "relevance_score":
        params["sort"] = sort + ":desc"
    url = f"{OPENALEX_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())

    return [_parse_work(work) for work in data.get("results") or []]


def main():
    parser = argparse.ArgumentParser(
        description="Search academic literature via OpenAlex"
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument(
        "--limit", type=int, default=10, help="Number of results (max 50)"
    )
    parser.add_argument(
        "--year-from", type=int, default=None, help="Filter papers from this year"
    )
    parser.add_argument(
        "--sort",
        default="relevance_score",
        choices=["relevance_score", "cited_by_count", "publication_date"],
        help="Sort order",
    )
    parser.add_argument(
        "--compact", action="store_true", help="Compact output (one line per paper)"
    )
    parser.add_argument(
        "--mailto", default=None, help="Real contact email for the OpenAlex polite pool"
    )
    args = parser.parse_args()

    try:
        results = search(args.query, args.limit, args.year_from, args.sort, args.mailto)
    except (
        ValueError,
        urllib.error.URLError,
        TimeoutError,
        json.JSONDecodeError,
    ) as exc:
        print(f"Error: OpenAlex search failed: {exc}", file=sys.stderr)
        return 1

    if args.compact:
        for r in results:
            authors_str = ", ".join(r["authors"][:3])
            if len(r["authors"]) > 3:
                authors_str += " et al."
            print(
                f"[{r['year']}] {r['title']} | {authors_str} | {r['journal']} | DOI:{r['doi']} | Cited:{r['cited_by_count']}"
            )
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
