#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Tokimi Rover contributors
# SPDX-License-Identifier: Apache-2.0

"""Validate the dependency-free Tokimi Open Source static page."""

from __future__ import annotations

import struct
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent
WEBSITE = ROOT
INDEX = ROOT / "index.html"
SOCIAL_PREVIEW = ROOT / "social-card-rover-v1.png"


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
        "OWNER-SELECTED V3 CAD PUBLISHED",
        "HARDWARE NOT AUDIT-RETESTED",
        "LIVE SITE VERIFIED",
        "PUBLIC SOURCE REPOSITORY",
        "APPLICATION CODE · MIT",
        "AI SUMMARIES · CHECK SOURCES",
        "BUILD + DATA NOT AUDIT-VERIFIED",
        "FEATURED 2 · PLANNED 1",
        "PROJECT REGISTER / 01—03",
        "PUBLISHING PROTOCOL / 04",
        "PLANNED · NOT RELEASED",
        "LICENSE TBD",
    }
    lowered = source.lower()
    for marker in sorted(required_markers):
        if marker.lower() not in lowered:
            failures.append(f"missing public status marker: {marker}")

    for language in ("zh-TW", "en"):
        if f'data-language="{language}"' not in source:
            failures.append(f"missing language option: {language}")

    social_image_url = "https://tokimispace.github.io/social-card-rover-v1.png"
    for marker, failure in {
        '<meta name="robots" content="index, follow, max-image-preview:large">': "missing large-image robots directive",
        '<meta property="og:title"': "missing Open Graph title",
        '<meta property="og:description"': "missing Open Graph description",
        '<meta property="og:site_name" content="Tokimi Open Source">': "missing Open Graph site name",
        '<meta property="og:locale" content="zh_TW">': "missing primary Open Graph locale",
        '<meta property="og:locale:alternate" content="en_US">': "missing alternate Open Graph locale",
        f'<meta property="og:image" content="{social_image_url}">': "missing absolute Open Graph image",
        f'<meta property="og:image:secure_url" content="{social_image_url}">': "missing secure Open Graph image",
        '<meta property="og:image:type" content="image/png">': "missing Open Graph image type",
        '<meta property="og:image:width" content="1200">': "missing Open Graph image width",
        '<meta property="og:image:height" content="630">': "missing Open Graph image height",
        '<meta property="og:image:alt"': "missing Open Graph image alternative text",
        '<meta name="twitter:card" content="summary_large_image">': "missing large Twitter Card",
        '<meta name="twitter:title"': "missing Twitter Card title",
        '<meta name="twitter:description"': "missing Twitter Card description",
        f'<meta name="twitter:image" content="{social_image_url}">': "missing absolute Twitter Card image",
        '<meta name="twitter:image:alt"': "missing Twitter Card image alternative text",
    }.items():
        if marker not in source:
            failures.append(failure)

    forbidden_claims = {
        "production-ready",
        "safety-certified rover",
        "Darkforest source available",
        "Tokimi Rover is available now",
        "AstroGroot source audited",
        "AstroGroot build confirmed",
        "AstroGroot summaries are peer reviewed",
    }
    for claim in sorted(forbidden_claims):
        if claim.lower() in lowered:
            failures.append(f"forbidden or unsupported claim: {claim}")

    official_site = 'href="https://tokimi.space/"'
    if source.count(official_site) < 2:
        failures.append("official Tokimi website must be linked in header and footer")

    cad_package = (
        'href="https://github.com/TokimiSpace/tokimi-rover/tree/main/'
        'hardware/cad/top-cover-v3"'
    )
    if cad_package not in source:
        failures.append("missing public Supercar V3 top-cover CAD link")

    for label, link in {
        "AstroGroot live site": 'href="https://astrogroot.org/"',
        "AstroGroot source": 'href="https://github.com/topben/astrogroot"',
        "AstroGroot MIT license": (
            'href="https://github.com/topben/astrogroot/blob/main/LICENSE"'
        ),
    }.items():
        if link not in source:
            failures.append(f"missing {label} link")

    for boundary in ("195 × 100 mm", "203 × 105 mm"):
        if boundary not in source:
            failures.append(f"missing CAD physical-boundary marker: {boundary}")

    for filename, license_id in {
        "index.html": "Apache-2.0",
        "styles.css": "Apache-2.0",
        "main.js": "Apache-2.0",
        "favicon.svg": "CC-BY-4.0",
        "robots.txt": "Apache-2.0",
        "sitemap.xml": "Apache-2.0",
        "social-card-rover-v1.svg": "Apache-2.0",
        "social-card-rover-v1.png.license": "Apache-2.0",
    }.items():
        contents = (WEBSITE / filename).read_text(encoding="utf-8")
        if f"SPDX-License-Identifier: {license_id}" not in contents:
            failures.append(f"missing {license_id} SPDX marker: {filename}")

    main_script = (WEBSITE / "main.js").read_text(encoding="utf-8")
    if 'localStorage.setItem("tokimi-language"' not in main_script:
        failures.append("language preference is not persisted locally")
    for marker, failure in {
        'searchParams.get("lang")': "language is not read from the URL",
        'searchParams.set("lang", language)': "language is not written to the URL",
        '"pushState"': "language changes do not create navigable history",
        '"popstate"': "browser history does not restore the page language",
        '"zh-TW"': "Traditional Chinese does not use the canonical URL tag",
    }.items():
        if marker not in main_script:
            failures.append(failure)

    readme = (WEBSITE / "README.md").read_text(encoding="utf-8")
    for language_url in ("?lang=en", "?lang=zh-TW"):
        if language_url not in readme:
            failures.append(f"missing documented language URL: {language_url}")

    for required in (
        ROOT / "LICENSE",
        ROOT / "LICENSES" / "CC-BY-4.0.txt",
        ROOT / "LICENSES.md",
        ROOT / "TRADEMARKS.md",
        ROOT / "robots.txt",
        ROOT / "sitemap.xml",
        ROOT / "social-card-rover-v1.svg",
        ROOT / "social-card-rover-v1.png.license",
    ):
        if not required.is_file():
            failures.append(f"missing publication file: {required.relative_to(ROOT)}")

    if not SOCIAL_PREVIEW.is_file():
        failures.append("missing rendered social preview PNG")
    else:
        data = SOCIAL_PREVIEW.read_bytes()
        if len(data) > 5_000_000:
            failures.append("social preview PNG exceeds 5 MB")
        if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
            failures.append("social preview is not a valid PNG")
        elif data[12:16] != b"IHDR":
            failures.append("social preview PNG is missing IHDR")
        else:
            width, height = struct.unpack(">II", data[16:24])
            if (width, height) != (1200, 630):
                failures.append(
                    f"social preview must be 1200x630, got {width}x{height}"
                )

    robots = ROOT / "robots.txt"
    if robots.is_file() and "https://tokimispace.github.io/sitemap.xml" not in (
        robots.read_text(encoding="utf-8")
    ):
        failures.append("robots.txt does not advertise the sitemap")
    sitemap = ROOT / "sitemap.xml"
    if sitemap.is_file() and "https://tokimispace.github.io/" not in (
        sitemap.read_text(encoding="utf-8")
    ):
        failures.append("sitemap does not contain the canonical site URL")

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
