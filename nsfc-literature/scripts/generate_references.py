#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Generate references from a list of DOIs using wenxian.

Usage:
    uv run generate_references.py dois.txt [--format bibtex|text|markdown] [--output refs.bib]

Input file: one DOI per line (lines starting with # are ignored).
Requires: wenxian (installed via uvx).
"""

import argparse
import subprocess
import sys


def generate_citation(doi: str, fmt: str = "bibtex") -> str | None:
    """Generate a citation for a single DOI using wenxian."""
    cmd = ["uvx", "wenxian", "from", doi]
    if fmt != "bibtex":
        cmd.extend(["-t", fmt])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            print(f"⚠️  Failed for {doi}: {result.stderr.strip()}", file=sys.stderr)
            return None
    except subprocess.TimeoutExpired:
        print(f"⚠️  Timeout for {doi}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="Batch generate references from DOI list")
    parser.add_argument("input", help="File with one DOI per line")
    parser.add_argument("--format", "-f", default="bibtex",
                        choices=["bibtex", "text", "markdown"],
                        help="Output format")
    parser.add_argument("--output", "-o", default=None,
                        help="Output file (default: stdout)")
    args = parser.parse_args()

    with open(args.input) as f:
        dois = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    citations = []
    for i, doi in enumerate(dois, 1):
        print(f"[{i}/{len(dois)}] Processing {doi}...", file=sys.stderr)
        citation = generate_citation(doi, args.format)
        if citation:
            citations.append(citation)

    output = "\n\n".join(citations)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output + "\n")
        print(f"✅ Wrote {len(citations)}/{len(dois)} citations to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
