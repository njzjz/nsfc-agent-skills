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
import urllib.request
import urllib.parse


OPENALEX_API = "https://api.openalex.org/works"
MAILTO = "openclaw-agent@example.com"  # polite pool


def search(query: str, limit: int = 10, year_from: int | None = None,
           sort: str = "relevance_score") -> list[dict]:
    params = {
        "search": query,
        "per_page": min(limit, 50),
        "mailto": MAILTO,
    }
    # OpenAlex sorts by relevance by default when using search; only add sort for other fields
    if sort != "relevance_score":
        params["sort"] = sort + ":desc"
    if year_from:
        params["filter"] = f"from_publication_date:{year_from}-01-01"

    url = f"{OPENALEX_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())

    results = []
    for work in data.get("results", []):
        authors = [
            a.get("author", {}).get("display_name", "")
            for a in work.get("authorships", [])
        ]
        doi = work.get("doi", "")
        if doi and doi.startswith("https://doi.org/"):
            doi = doi[len("https://doi.org/"):]

        abstract_index = work.get("abstract_inverted_index")
        abstract = ""
        if abstract_index:
            # Reconstruct abstract from inverted index
            word_positions = []
            for word, positions in abstract_index.items():
                for pos in positions:
                    word_positions.append((pos, word))
            word_positions.sort()
            abstract = " ".join(w for _, w in word_positions)

        results.append({
            "title": work.get("title", ""),
            "doi": doi,
            "authors": authors[:5],  # first 5 authors
            "year": work.get("publication_year"),
            "cited_by_count": work.get("cited_by_count", 0),
            "journal": (work.get("primary_location") or {}).get("source", {}).get("display_name", ""),
            "abstract": abstract[:500] if abstract else "",
            "openalex_id": work.get("id", ""),
        })

    return results


def main():
    parser = argparse.ArgumentParser(description="Search academic literature via OpenAlex")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=10, help="Number of results (max 50)")
    parser.add_argument("--year-from", type=int, default=None, help="Filter papers from this year")
    parser.add_argument("--sort", default="relevance_score",
                        choices=["relevance_score", "cited_by_count", "publication_date"],
                        help="Sort order")
    parser.add_argument("--compact", action="store_true", help="Compact output (one line per paper)")
    args = parser.parse_args()

    results = search(args.query, args.limit, args.year_from, args.sort)

    if args.compact:
        for r in results:
            authors_str = ", ".join(r["authors"][:3])
            if len(r["authors"]) > 3:
                authors_str += " et al."
            print(f"[{r['year']}] {r['title']} | {authors_str} | {r['journal']} | DOI:{r['doi']} | Cited:{r['cited_by_count']}")
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
