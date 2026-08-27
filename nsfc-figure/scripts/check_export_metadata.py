#!/usr/bin/env python3
"""Detect embedded Draw.io source in exported SVG or PNG files.

Draw.io can intentionally place a complete ``mxfile`` document in an export so
that the image remains editable. That is useful inside a controlled workspace,
but it may disclose hidden or off-canvas proposal content when the image is
submitted or shared. This checker reports metadata keys only and never prints
their values.
"""

from __future__ import annotations

import argparse
import json
import struct
import urllib.parse
import xml.etree.ElementTree as ET
import zlib
from dataclasses import asdict, dataclass, field
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


@dataclass
class Inspection:
    """Summarize export metadata without echoing potentially sensitive text."""

    path: str
    format: str
    embedded_drawio: bool = False
    metadata_keys: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def _contains_mxfile(payload: bytes) -> bool:
    """Recognize raw, XML-escaped, or URL-encoded mxfile content."""

    lowered = payload.lower()
    if b"mxfile" in lowered:
        return True
    try:
        return b"mxfile" in urllib.parse.unquote_to_bytes(payload).lower()
    except UnicodeDecodeError:
        return False


def _decode_itxt(payload: bytes) -> tuple[str, bytes]:
    """Decode a PNG iTXt chunk into its keyword and text payload."""

    keyword_raw, remainder = payload.split(b"\0", 1)
    if len(remainder) < 2:
        raise ValueError("truncated iTXt compression fields")
    compressed, method = remainder[0], remainder[1]
    remainder = remainder[2:]
    _language, remainder = remainder.split(b"\0", 1)
    _translated, text = remainder.split(b"\0", 1)
    if compressed:
        if method != 0:
            raise ValueError(f"unsupported iTXt compression method {method}")
        text = zlib.decompress(text)
    return keyword_raw.decode("latin-1", "replace"), text


def inspect_png(path: Path) -> Inspection:
    """Inspect textual PNG chunks and validate chunk boundaries."""

    inspection = Inspection(str(path), "png")
    try:
        data = path.read_bytes()
    except OSError as exc:
        inspection.errors.append(str(exc))
        return inspection
    if not data.startswith(PNG_SIGNATURE):
        inspection.errors.append("invalid PNG signature")
        return inspection

    offset = len(PNG_SIGNATURE)
    saw_iend = False
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk_end = offset + 12 + length
        if chunk_end > len(data):
            inspection.errors.append("truncated PNG chunk")
            break
        payload = data[offset + 8 : offset + 8 + length]
        stored_crc = struct.unpack(">I", data[offset + 8 + length : chunk_end])[0]
        actual_crc = zlib.crc32(chunk_type + payload) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            inspection.errors.append(
                f"CRC mismatch in {chunk_type.decode('latin-1')} chunk"
            )
        offset = chunk_end

        try:
            if chunk_type == b"tEXt":
                key_raw, text = payload.split(b"\0", 1)
                key = key_raw.decode("latin-1", "replace")
            elif chunk_type == b"zTXt":
                key_raw, remainder = payload.split(b"\0", 1)
                if not remainder or remainder[0] != 0:
                    raise ValueError("unsupported zTXt compression method")
                key = key_raw.decode("latin-1", "replace")
                text = zlib.decompress(remainder[1:])
            elif chunk_type == b"iTXt":
                key, text = _decode_itxt(payload)
            else:
                if chunk_type == b"IEND":
                    saw_iend = True
                    break
                continue
        except (ValueError, zlib.error) as exc:
            inspection.errors.append(f"invalid {chunk_type.decode('latin-1')} chunk: {exc}")
            continue

        inspection.metadata_keys.append(key)
        if key.lower() == "mxfile" or _contains_mxfile(text):
            inspection.embedded_drawio = True

    if not saw_iend:
        inspection.errors.append("PNG is missing IEND")
    inspection.metadata_keys = sorted(set(inspection.metadata_keys))
    return inspection


def inspect_svg(path: Path) -> Inspection:
    """Inspect SVG markup for an embedded mxfile document."""

    inspection = Inspection(str(path), "svg")
    try:
        data = path.read_bytes()
    except OSError as exc:
        inspection.errors.append(str(exc))
        return inspection
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        inspection.errors.append(f"invalid SVG XML: {exc}")
        return inspection
    if root.tag.rsplit("}", 1)[-1].lower() != "svg":
        inspection.errors.append("XML root element is not svg")
        return inspection
    # Check both the original bytes and normalized XML. ElementTree resolves
    # encodings and character references, which prevents equivalent markup
    # such as UTF-16 SVG or ``m&#120;file`` from bypassing the detector.
    normalized = ET.tostring(root, encoding="utf-8")
    inspection.embedded_drawio = _contains_mxfile(data) or _contains_mxfile(normalized)
    return inspection


def inspect(path: Path) -> Inspection:
    """Route a supported export to its format-specific inspector."""

    suffix = path.suffix.lower()
    if suffix == ".png":
        return inspect_png(path)
    if suffix == ".svg":
        return inspect_svg(path)
    return Inspection(str(path), suffix.lstrip(".") or "unknown", errors=["unsupported format"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Check exports for embedded Draw.io source")
    parser.add_argument("paths", nargs="+", type=Path, help="SVG or PNG exports")
    parser.add_argument("--json", action="store_true", help="Emit a JSON report")
    args = parser.parse_args()

    inspections = [inspect(path) for path in args.paths]
    if args.json:
        print(json.dumps([asdict(item) for item in inspections], ensure_ascii=False, indent=2))
    else:
        for item in inspections:
            if item.errors:
                status = "ERROR"
            elif item.embedded_drawio:
                status = "EMBEDDED-SOURCE"
            else:
                status = "CLEAN"
            keys = f"; metadata keys: {', '.join(item.metadata_keys)}" if item.metadata_keys else ""
            print(f"{status}: {item.path}{keys}")
            for error in item.errors:
                print(f"  error: {error}")

    return 1 if any(item.errors or item.embedded_drawio for item in inspections) else 0


if __name__ == "__main__":
    raise SystemExit(main())
