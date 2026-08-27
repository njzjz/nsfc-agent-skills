#!/usr/bin/env python3
"""Validate structural invariants of compressed or uncompressed Draw.io XML.

This validator checks properties that can be established without a graphical
renderer: XML integrity, graph roots, unique IDs, valid references, explicit
geometry, and page bounds. A successful result does not replace visual export
and print-size inspection.
"""

from __future__ import annotations

import argparse
import base64
import json
import urllib.parse
import xml.etree.ElementTree as ET
import zlib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ValidationReport:
    """Collect machine-checkable errors, warnings, and document statistics."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    diagrams: int = 0
    cells: int = 0
    vertices: int = 0
    edges: int = 0


def _decode_model(diagram: ET.Element) -> ET.Element:
    """Return an mxGraphModel from either Draw.io storage representation."""

    model = diagram.find("mxGraphModel")
    if model is not None:
        return model

    payload = (diagram.text or "").strip()
    if not payload:
        raise ValueError("diagram has neither mxGraphModel nor compressed content")
    try:
        compressed = base64.b64decode(payload, validate=True)
        encoded_xml = zlib.decompress(compressed, -15).decode("utf-8")
        return ET.fromstring(urllib.parse.unquote(encoded_xml))
    except (ValueError, zlib.error, UnicodeDecodeError, ET.ParseError) as exc:
        raise ValueError(f"cannot decode compressed diagram: {exc}") from exc


def _float_attr(element: ET.Element, name: str) -> float | None:
    """Parse an optional numeric attribute without hiding malformed values."""

    value = element.get(name)
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def validate_file(path: Path) -> ValidationReport:
    """Validate one Draw.io file and return a reusable structured report."""

    report = ValidationReport()
    try:
        document = ET.parse(path)
    except (OSError, ET.ParseError) as exc:
        report.errors.append(f"cannot parse XML: {exc}")
        return report

    mxfile = document.getroot()
    if mxfile.tag != "mxfile":
        report.errors.append(f"root element must be mxfile, found {mxfile.tag!r}")
        return report

    diagrams = mxfile.findall("diagram")
    report.diagrams = len(diagrams)
    if not diagrams:
        report.errors.append("mxfile must contain at least one diagram")
        return report

    for diagram_index, diagram in enumerate(diagrams, start=1):
        context = f"diagram {diagram_index}"
        try:
            model = _decode_model(diagram)
        except ValueError as exc:
            report.errors.append(f"{context}: {exc}")
            continue

        graph_root = model.find("root")
        if graph_root is None:
            report.errors.append(f"{context}: mxGraphModel is missing root")
            continue

        cells = graph_root.findall("mxCell")
        report.cells += len(cells)
        ids = [cell.get("id") for cell in cells]
        missing_ids = sum(cell_id is None or not cell_id for cell_id in ids)
        if missing_ids:
            report.errors.append(f"{context}: {missing_ids} mxCell element(s) lack an ID")
        concrete_ids = [cell_id for cell_id in ids if cell_id]
        duplicate_ids = sorted(
            cell_id for cell_id in set(concrete_ids) if concrete_ids.count(cell_id) > 1
        )
        if duplicate_ids:
            report.errors.append(f"{context}: duplicate mxCell IDs: {duplicate_ids}")
        id_set = set(concrete_ids)
        if "0" not in id_set or "1" not in id_set:
            report.errors.append(f"{context}: graph must contain root cells '0' and '1'")
        cells_by_id = {cell.get("id"): cell for cell in cells if cell.get("id")}
        root_cell = cells_by_id.get("0")
        layer_cell = cells_by_id.get("1")
        if root_cell is not None and root_cell.get("parent"):
            report.errors.append(f"{context}: root cell '0' must not have a parent")
        if layer_cell is not None and layer_cell.get("parent") != "0":
            report.errors.append(f"{context}: default layer cell '1' must have parent '0'")

        page_width = _float_attr(model, "pageWidth")
        page_height = _float_attr(model, "pageHeight")
        if page_width is None or page_width <= 0 or page_height is None or page_height <= 0:
            report.warnings.append(f"{context}: pageWidth/pageHeight are missing or invalid")

        for cell in cells:
            cell_id = cell.get("id", "<missing>")
            parent = cell.get("parent")
            if cell_id not in {"0", "1"} and not parent:
                report.errors.append(
                    f"{context}: cell {cell_id!r} lacks a parent and is disconnected from root '0'"
                )
            if parent and parent not in id_set:
                report.errors.append(
                    f"{context}: cell {cell_id!r} references missing parent {parent!r}"
                )

            is_vertex = cell.get("vertex") == "1"
            is_edge = cell.get("edge") == "1"
            report.vertices += int(is_vertex)
            report.edges += int(is_edge)
            geometry = cell.find("mxGeometry")

            if is_vertex:
                if geometry is None:
                    report.errors.append(f"{context}: vertex {cell_id!r} lacks mxGeometry")
                    continue
                width = _float_attr(geometry, "width")
                height = _float_attr(geometry, "height")
                if width is None or width <= 0 or height is None or height <= 0:
                    report.errors.append(
                        f"{context}: vertex {cell_id!r} needs positive width and height"
                    )
                x = _float_attr(geometry, "x")
                y = _float_attr(geometry, "y")
                if (
                    geometry.get("relative") != "1"
                    and None not in (x, y, width, height, page_width, page_height)
                    and (x < 0 or y < 0 or x + width > page_width or y + height > page_height)
                ):
                    report.warnings.append(
                        f"{context}: vertex {cell_id!r} extends beyond the configured page"
                    )

            if is_edge:
                source = cell.get("source")
                target = cell.get("target")
                if not source or source not in id_set:
                    report.errors.append(
                        f"{context}: edge {cell_id!r} source {source!r} does not exist"
                    )
                if not target or target not in id_set:
                    report.errors.append(
                        f"{context}: edge {cell_id!r} target {target!r} does not exist"
                    )
                if geometry is None or geometry.get("relative") != "1":
                    report.errors.append(
                        f"{context}: edge {cell_id!r} needs relative mxGeometry"
                    )

            style = cell.get("style", "")
            if "image=file:" in style.lower():
                report.warnings.append(
                    f"{context}: cell {cell_id!r} uses a machine-local image path"
                )
            style_values = {
                key.lower(): value
                for token in style.split(";")
                if "=" in token
                for key, value in [token.split("=", 1)]
            }
            if cell.get("visible") == "0" or style_values.get("opacity") == "0":
                report.warnings.append(
                    f"{context}: cell {cell_id!r} is hidden and may retain sensitive text"
                )

        # With every non-root cell required to have an existing parent, the
        # only remaining way to be unreachable from cell '0' is a parent cycle.
        reported_cycles: set[frozenset[str]] = set()
        for start_id in concrete_ids:
            current = start_id
            path: list[str] = []
            positions: dict[str, int] = {}
            while current != "0":
                if current in positions:
                    cycle = path[positions[current] :]
                    cycle_key = frozenset(cycle)
                    if cycle_key not in reported_cycles:
                        report.errors.append(
                            f"{context}: parent cycle prevents root reachability: {cycle}"
                        )
                        reported_cycles.add(cycle_key)
                    break
                positions[current] = len(path)
                path.append(current)
                current_cell = cells_by_id.get(current)
                if current_cell is None:
                    break
                parent = current_cell.get("parent")
                if not parent or parent not in id_set:
                    break
                current = parent

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Draw.io XML structure")
    parser.add_argument("paths", nargs="+", type=Path, help="One or more .drawio files")
    parser.add_argument("--json", action="store_true", help="Emit a JSON report")
    args = parser.parse_args()

    failed = False
    results: dict[str, object] = {}
    for path in args.paths:
        report = validate_file(path)
        failed = failed or bool(report.errors)
        result = {
            "errors": report.errors,
            "warnings": report.warnings,
            "diagrams": report.diagrams,
            "cells": report.cells,
            "vertices": report.vertices,
            "edges": report.edges,
        }
        results[str(path)] = result
        if not args.json:
            status = "FAIL" if report.errors else "OK"
            print(
                f"{status}: {path} "
                f"({report.diagrams} diagram(s), {report.vertices} vertices, {report.edges} edges)"
            )
            for warning in report.warnings:
                print(f"  warning: {warning}")
            for error in report.errors:
                print(f"  error: {error}")

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
