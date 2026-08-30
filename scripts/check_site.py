#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Tokimi Rover contributors
# SPDX-License-Identifier: Apache-2.0

"""Validate the dependency-free Tokimi Open Source static page."""

from __future__ import annotations

import json
import struct
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent
WEBSITE = ROOT
INDEX = ROOT / "index.html"
SOCIAL_CARD_BASENAME = "social-card-open-source-v3"
SOCIAL_SOURCE = ROOT / f"{SOCIAL_CARD_BASENAME}.svg"
SOCIAL_PREVIEW = ROOT / f"{SOCIAL_CARD_BASENAME}.png"
SOCIAL_LICENSE = ROOT / f"{SOCIAL_CARD_BASENAME}.png.license"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.references: list[tuple[str, str]] = []
        self.json_ld_blocks: list[str] = []
        self._json_ld_chunks: list[str] | None = None

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = dict(attrs)
        if tag == "script" and values.get("type") == "application/ld+json":
            self._json_ld_chunks = []
        if element_id := values.get("id"):
            self.ids.append(element_id)
        for attribute in ("href", "src"):
            if value := values.get(attribute):
                self.references.append((attribute, value))

    def handle_data(self, data: str) -> None:
        if self._json_ld_chunks is not None:
            self._json_ld_chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._json_ld_chunks is not None:
            self.json_ld_blocks.append("".join(self._json_ld_chunks))
            self._json_ld_chunks = None


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
        "FEATURED 5 · CLEARLY SCOPED",
        "PROJECT REGISTER / 01—05",
        "PUBLISHING PROTOCOL / 04",
        "FRONTEND SOURCE AVAILABLE",
        "FRONTEND · PRE-ALPHA",
        "APACHE-2.0 CODE",
        "SERVER NOT INCLUDED",
        "PRIVATE INTENT V0.2.0",
        "NOT PRODUCTION DEPLOYMENT EVIDENCE",
        "FIVE-FIELD RUNTIME ALLOWLIST",
        "EXACT WIRE-CAPTURE TESTS",
        "LOCAL DATA → FIVE ENUM FIELDS → KIMI",
        "ABSTRACT INTENT METADATA",
        "PUBLIC SPEC + TEST VECTORS",
        "STANDARD-LIBRARY VERIFIER",
        "GO + TYPESCRIPT SDK V0.2.0",
        "OIDC + SLSA PROVENANCE",
        "NO TEE · NO TRUST SCORE",
    }
    lowered = source.lower()
    for marker in sorted(required_markers):
        if marker.lower() not in lowered:
            failures.append(f"missing public status marker: {marker}")

    for language in ("zh-TW", "en"):
        if f'data-language="{language}"' not in source:
            failures.append(f"missing language option: {language}")

    social_image_url = (
        f"https://tokimispace.github.io/{SOCIAL_CARD_BASENAME}.png?v=5"
    )
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
        '<script type="application/ld+json">': "missing JSON-LD project list",
    }.items():
        if marker not in source:
            failures.append(failure)

    forbidden_claims = {
        "production-ready",
        "safety-certified rover",
        "Darkforest source available",
        "Darkforest game is open source",
        "Darkforest server source available",
        "Full game source available",
        "Tokimi Rover is available now",
        "AstroGroot source audited",
        "AstroGroot build confirmed",
        "AstroGroot summaries are peer reviewed",
        "all user data is anonymized",
        "no user data reaches the provider",
        "guarantees zero leakage",
        "production assistant enabled",
    }
    for claim in sorted(forbidden_claims):
        if claim.lower() in lowered:
            failures.append(f"forbidden or unsupported claim: {claim}")

    official_site = 'href="https://tokimi.space/"'
    if source.count(official_site) < 2:
        failures.append("official Tokimi website must be linked in header and footer")

    identity_notice = 'data-official-identity-notice role="note"'
    if source.count(identity_notice) != 1:
        failures.append("page must contain exactly one in-flow identity notice with role=note")
    for marker, failure in {
        'href="mailto:ben@tokimi.space"': "identity notice lacks official email link",
        "Any @gmail.com address claiming to represent Tokimi is not an official Tokimi contact channel": "identity notice lacks exact English Gmail warning",
        "Do not pay or share verification codes": "identity notice lacks English payment/code warning",
        "以 @gmail.com 結尾、並自稱代表 Tokimi": "identity notice lacks exact Chinese Gmail warning",
        "不是 Tokimi 官方聯絡管道": "identity notice lacks Chinese official-channel warning",
        "請勿付款或提供驗證碼": "identity notice lacks Chinese payment/code warning",
    }.items():
        if marker.lower() not in lowered:
            failures.append(failure)

    for locale, link in {
        "Traditional Chinese": 'href="https://tokimi.space/open-source/"',
        "English": 'href="https://tokimi.space/en/open-source/"',
    }.items():
        if source.count(link) < 2:
            failures.append(f"official {locale} open-source page must be linked in header and footer")

    if "standalone public-demo schema v1" not in source:
        failures.append("missing canonical standalone public-demo schema v1 wording")

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
        "Darkforest frontend source": (
            'href="https://github.com/TokimiSpace/darkforest-web"'
        ),
        "Darkforest official site": 'href="https://darkforest.tw/"',
        "BridgeTime Kimi privacy source": (
            'href="https://github.com/TokimiSpace/bridgetime-kimi-privacy"'
        ),
        "BridgeTime live site": 'href="https://bridgetime.org/"',
        "IFF transparency source": (
            'href="https://github.com/ifandonlyif-io/iff-x402-transparency"'
        ),
        "IFF public evidence service": 'href="https://ifandonlyif.io/"',
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
        f"{SOCIAL_CARD_BASENAME}.svg": "Apache-2.0",
        f"{SOCIAL_CARD_BASENAME}.png.license": "Apache-2.0",
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

    for readme_name in ("README.md", "README.en.md"):
        readme_source = (WEBSITE / readme_name).read_text(encoding="utf-8")
        for marker in (
            "> [!WARNING]",
            "Any `@gmail.com` address claiming to represent Tokimi is not an official Tokimi contact channel",
            "請勿付款或提供驗證碼",
            "https://tokimi.space/",
            "mailto:ben@tokimi.space",
        ):
            if marker not in readme_source:
                failures.append(f"{readme_name} lacks anti-fraud marker: {marker}")

    if not parser.json_ld_blocks:
        failures.append("missing parseable JSON-LD block")
    else:
        try:
            json_ld = json.loads(parser.json_ld_blocks[0])
        except json.JSONDecodeError as error:
            failures.append(f"invalid JSON-LD: {error}")
        else:
            if json_ld.get("@type") != "ItemList":
                failures.append("JSON-LD root must be an ItemList")
            if json_ld.get("numberOfItems") != 5:
                failures.append("JSON-LD project count must be 5")
            elements = json_ld.get("itemListElement")
            if not isinstance(elements, list) or len(elements) != 5:
                failures.append("JSON-LD must describe exactly five projects")
            else:
                repositories = {
                    element.get("item", {}).get("codeRepository")
                    for element in elements
                    if isinstance(element, dict)
                }
                expected_repositories = {
                    "https://github.com/TokimiSpace/tokimi-rover",
                    "https://github.com/topben/astrogroot",
                    "https://github.com/TokimiSpace/darkforest-web",
                    "https://github.com/TokimiSpace/bridgetime-kimi-privacy",
                    "https://github.com/ifandonlyif-io/iff-x402-transparency",
                }
                missing_repositories = expected_repositories - repositories
                if missing_repositories:
                    failures.append(
                        "JSON-LD missing code repositories: "
                        + ", ".join(sorted(missing_repositories))
                    )

    for required in (
        ROOT / "LICENSE",
        ROOT / "LICENSES" / "CC-BY-4.0.txt",
        ROOT / "LICENSES.md",
        ROOT / "TRADEMARKS.md",
        ROOT / "robots.txt",
        ROOT / "sitemap.xml",
        SOCIAL_SOURCE,
        SOCIAL_LICENSE,
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

    if SOCIAL_SOURCE.is_file():
        social_source = SOCIAL_SOURCE.read_text(encoding="utf-8")
        for marker in (
            "TOKIMI / OPEN SOURCE / SIGNAL BUS",
            "TOKIMI ROVER",
            "ASTROGROOT",
            "DARKFOREST WEB",
            "BRIDGETIME KIMI PRIVACY",
            "IFF X402 TRANSPARENCY",
            "LOCAL DATA → FIVE ENUM FIELDS → KIMI",
            "OPEN / 05",
            "#007370",
            "#6655c7",
            "#dc5939",
            "#a33c73",
            "#1d5fa7",
        ):
            if marker not in social_source:
                failures.append(f"social-card source missing project signal: {marker}")

    for stale_source, label in (
        (source, "index.html"),
        (readme, "README.md"),
    ):
        for stale_card in (
            "social-card-rover-v1.png",
            "social-card-open-source-v2.png",
        ):
            if stale_card in stale_source:
                failures.append(f"{label} still references stale social card: {stale_card}")

    for stale_count in (
        "FEATURED 4 · CLEARLY SCOPED",
        "PROJECT REGISTER / 01—04",
        "OPEN / 04",
        "Four open projects",
        "Four projects",
        "四個實驗，四種",
        "FEATURED 3 · CLEARLY SCOPED",
        "PROJECT REGISTER / 01—03",
        "OPEN / 03",
        "Three open projects",
        "三個實驗，三種",
    ):
        if stale_count.lower() in lowered:
            failures.append(f"index.html still contains stale project-count marker: {stale_count}")

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
