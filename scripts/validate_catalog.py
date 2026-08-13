#!/usr/bin/env python3
"""Validate the catalogue, watchlist, and local Markdown links using stdlib only."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "protocols.json"
WATCHLIST = ROOT / "catalog" / "watchlist.json"

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LOCAL_LINK_RE = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")

ALLOWED_MATURITY = {
    "standard",
    "candidate",
    "draft",
    "experimental",
    "implementation",
    "framework",
    "working-hypothesis",
    "deprecated",
}

ALLOWED_DOMAINS = {
    "task-context",
    "inference",
    "metrics",
    "device-telemetry",
    "flow-routing",
    "path-measurement",
    "compute-network",
    "project-concept",
}

PRIMARY_HOSTS = {
    "www.w3.org",
    "opentelemetry.io",
    "github.com",
    "prometheus.io",
    "docs.vllm.ai",
    "docs.nvidia.com",
    "datatracker.ietf.org",
}


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)}: {exc}")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_iso_date(value: object, label: str) -> None:
    if not isinstance(value, str):
        fail(f"{label} must be an ISO date string")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        fail(f"{label} is not a valid ISO date: {exc}")


def validate_id(value: object, label: str) -> str:
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        fail(f"{label} must match {ID_RE.pattern}")
    return value


def validate_https_or_local(value: object, label: str) -> None:
    if not isinstance(value, str) or not value:
        fail(f"{label} must be a non-empty URL or local reference")
    if value.startswith("../docs/"):
        target = (CATALOG.parent / value).resolve()
        if ROOT not in target.parents or not target.is_file():
            fail(f"{label} points to a missing local file: {value}")
        return
    parsed = urlparse(value)
    if parsed.scheme != "https" or parsed.hostname not in PRIMARY_HOSTS:
        fail(f"{label} must use an approved authoritative HTTPS host: {value}")


def require_non_empty_string(item: dict, key: str, label: str) -> None:
    if not isinstance(item.get(key), str) or not item[key].strip():
        fail(f"{label}.{key} must be a non-empty string")


def require_string_list(item: dict, key: str, label: str) -> None:
    value = item.get(key)
    if not isinstance(value, list) or not value or not all(isinstance(v, str) and v.strip() for v in value):
        fail(f"{label}.{key} must be a non-empty list of strings")


def validate_catalog() -> tuple[dict, set[str]]:
    data = load_json(CATALOG)
    require_non_empty_string(data, "schema_version", "catalog")
    validate_iso_date(data.get("baseline_date"), "catalog.baseline_date")
    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        fail("catalog.entries must be a non-empty list")

    ids: set[str] = set()
    for index, entry in enumerate(entries):
        label = f"catalog.entries[{index}]"
        if not isinstance(entry, dict):
            fail(f"{label} must be an object")
        entry_id = validate_id(entry.get("id"), f"{label}.id")
        if entry_id in ids:
            fail(f"duplicate catalogue id: {entry_id}")
        ids.add(entry_id)

        for key in ("name", "type", "version", "status_notes", "relevance", "limitations"):
            require_non_empty_string(entry, key, label)
        if entry.get("domain") not in ALLOWED_DOMAINS:
            fail(f"{label}.domain has unsupported value: {entry.get('domain')}")
        if entry.get("maturity") not in ALLOWED_MATURITY:
            fail(f"{label}.maturity has unsupported value: {entry.get('maturity')}")
        require_string_list(entry, "evidence", label)
        validate_iso_date(entry.get("last_checked"), f"{label}.last_checked")

        sources = entry.get("primary_sources")
        if not isinstance(sources, list) or not sources:
            fail(f"{label}.primary_sources must be a non-empty list")
        for source_index, source in enumerate(sources):
            source_label = f"{label}.primary_sources[{source_index}]"
            if not isinstance(source, dict):
                fail(f"{source_label} must be an object")
            require_non_empty_string(source, "title", source_label)
            validate_https_or_local(source.get("url"), f"{source_label}.url")

    return data, ids


def validate_watchlist(catalog_ids: set[str]) -> dict:
    data = load_json(WATCHLIST)
    require_non_empty_string(data, "schema_version", "watchlist")
    validate_iso_date(data.get("baseline_date"), "watchlist.baseline_date")
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        fail("watchlist.sources must be a non-empty list")

    source_ids: set[str] = set()
    tracked: set[str] = set()
    for index, source in enumerate(sources):
        label = f"watchlist.sources[{index}]"
        if not isinstance(source, dict):
            fail(f"{label} must be an object")
        source_id = validate_id(source.get("id"), f"{label}.id")
        if source_id in source_ids:
            fail(f"duplicate watchlist source id: {source_id}")
        source_ids.add(source_id)
        require_non_empty_string(source, "organisation", label)
        validate_https_or_local(source.get("url"), f"{label}.url")
        require_string_list(source, "tracks", label)
        require_string_list(source, "check_for", label)
        unknown = set(source["tracks"]) - catalog_ids
        if unknown:
            fail(f"{label}.tracks references unknown catalogue ids: {sorted(unknown)}")
        tracked.update(source["tracks"])

    expected = catalog_ids - {"fox"}
    missing = expected - tracked
    if missing:
        fail(f"catalogue entries missing from watchlist coverage: {sorted(missing)}")
    return data


def validate_local_markdown_links() -> int:
    checked = 0
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for raw_target in LOCAL_LINK_RE.findall(text):
            target_text = raw_target.split("#", 1)[0].strip()
            if not target_text:
                continue
            target = (path.parent / target_text).resolve()
            if ROOT != target and ROOT not in target.parents:
                fail(f"{path.relative_to(ROOT)} link escapes repository: {raw_target}")
            if not target.exists():
                fail(f"{path.relative_to(ROOT)} has missing local link: {raw_target}")
            checked += 1
    return checked


def main() -> None:
    catalog, catalog_ids = validate_catalog()
    watchlist = validate_watchlist(catalog_ids)
    link_count = validate_local_markdown_links()
    print(
        "Validation passed: "
        f"{len(catalog['entries'])} catalogue entries, "
        f"{len(watchlist['sources'])} watch sources, "
        f"{link_count} local Markdown links."
    )


if __name__ == "__main__":
    main()
