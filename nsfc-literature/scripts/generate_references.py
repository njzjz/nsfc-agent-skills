#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Generate references from a list of identifiers using wenxian.

Usage:
    uv run generate_references.py dois.txt [--format bibtex|text|markdown] [--output refs.bib]

Input file: one DOI, PMID, arXiv ID, or title per line. Comments start with #.
Requires: wenxian (installed via uvx).
"""

import argparse
import subprocess
import sys


def generate_citation(identifier: str, fmt: str = "bibtex") -> str | None:
    """Generate a citation for one identifier using wenxian."""
    cmd = ["uvx", "wenxian", "from", identifier]
    if fmt != "bibtex":
        cmd.extend(["-t", fmt])

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30, check=False
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            print(f"Failed for {identifier}: {result.stderr.strip()}", file=sys.stderr)
            return None
    except subprocess.TimeoutExpired:
        print(f"Timeout for {identifier}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print(
            "Error: uvx was not found; install uv before running this script",
            file=sys.stderr,
        )
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Batch generate references from identifier list"
    )
    parser.add_argument(
        "input", help="File with one DOI, PMID, arXiv ID, or title per line"
    )
    parser.add_argument(
        "--format",
        "-f",
        default="bibtex",
        choices=["bibtex", "text", "markdown"],
        help="Output format",
    )
    parser.add_argument(
        "--output", "-o", default=None, help="Output file (default: stdout)"
    )
    parser.add_argument(
        "--ignore-errors",
        action="store_true",
        help="Allow partial output and exit successfully",
    )
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        identifiers = [
            stripped
            for line in f
            if (stripped := line.strip()) and not stripped.startswith("#")
        ]

    if not identifiers:
        print("Error: the input file contains no identifiers", file=sys.stderr)
        return 1

    citations = []
    failures = 0
    for i, identifier in enumerate(identifiers, 1):
        print(f"[{i}/{len(identifiers)}] Processing {identifier}...", file=sys.stderr)
        citation = generate_citation(identifier, args.format)
        if citation:
            citations.append(citation)
        else:
            failures += 1

    output = "\n\n".join(citations)

    if not citations:
        print("Error: no citations were generated; no output was written", file=sys.stderr)
        return 1

    if failures and not args.ignore_errors:
        print(
            f"Error: {failures} identifier(s) failed; no output was written",
            file=sys.stderr,
        )
        return 1

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output + "\n")
        print(
            f"Wrote {len(citations)}/{len(identifiers)} citations to {args.output}",
            file=sys.stderr,
        )
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
