#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Tokimi Rover contributors
# SPDX-License-Identifier: Apache-2.0

"""Validate the dependency-free Tokimi Open Source static page."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent
WEBSITE = ROOT
INDEX = ROOT / "index.html"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.references: list[tuple[str, str]] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = dict(attrs)
        if element_id := values.get("id"):
            self.ids.append(element_id)
        for attribute in ("href", "src"):
            if value := values.get(attribute):
                self.references.append((attribute, value))


def main() -> int:
    failures: list[str] = []
    parser = PageParser()
    source = INDEX.read_text(encoding="utf-8")
    parser.feed(source)

    duplicate_ids = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicate_ids:
        failures.append(f"duplicate HTML id(s): {', '.join(duplicate_ids)}")

    known_ids = set(parser.ids)
    for attribute, raw_reference in parser.references:
        parsed = urlsplit(raw_reference)
        if parsed.scheme in {"http", "https", "mailto", "tel"}:
            continue
        if raw_reference.startswith("//"):
            failures.append(f"protocol-relative {attribute}: {raw_reference}")
            continue
        if parsed.path.startswith("/"):
            failures.append(f"root-absolute {attribute} breaks project Pages: {raw_reference}")
            continue
        if not parsed.path:
            if parsed.fragment and parsed.fragment not in known_ids:
                failures.append(f"missing fragment target: {raw_reference}")
            continue

        target = (WEBSITE / unquote(parsed.path)).resolve()
        if not target.exists():
            failures.append(f"missing local {attribute}: {raw_reference}")

    required_markers = {
        "SOURCE AUDITED",
        "HARDWARE NOT AUDIT-RETESTED",
        "PLANNED · NOT RELEASED",
        "LICENSE TBD",
    }
    lowered = source.lower()
    for marker in sorted(required_markers):
        if marker.lower() not in lowered:
            failures.append(f"missing public status marker: {marker}")

    for language in ("zh-Hant", "en"):
        if f'data-language="{language}"' not in source:
            failures.append(f"missing language option: {language}")

    forbidden_claims = {
        "production-ready",
        "safety-certified rover",
        "Darkforest source available",
        "Tokimi Rover is available now",
    }
    for claim in sorted(forbidden_claims):
        if claim.lower() in lowered:
            failures.append(f"forbidden or unsupported claim: {claim}")

    for filename, license_id in {
        "index.html": "Apache-2.0",
        "styles.css": "Apache-2.0",
        "main.js": "Apache-2.0",
        "favicon.svg": "CC-BY-4.0",
    }.items():
        contents = (WEBSITE / filename).read_text(encoding="utf-8")
        if f"SPDX-License-Identifier: {license_id}" not in contents:
            failures.append(f"missing {license_id} SPDX marker: {filename}")

    main_script = (WEBSITE / "main.js").read_text(encoding="utf-8")
    if 'localStorage.setItem("tokimi-language"' not in main_script:
        failures.append("language preference is not persisted locally")

    for required in (
        ROOT / "LICENSE",
        ROOT / "LICENSES" / "CC-BY-4.0.txt",
        ROOT / "LICENSES.md",
        ROOT / "TRADEMARKS.md",
    ):
        if not required.is_file():
            failures.append(f"missing publication file: {required.relative_to(ROOT)}")

    if "data-repo-link" in source or "../README.md" in source:
        failures.append("repository links still depend on the former Rover-repo layout")

    if failures:
        print("website check failed:", file=sys.stderr)
        print("\n".join(f"- {failure}" for failure in failures), file=sys.stderr)
        return 1

    print("website structure and claim check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
