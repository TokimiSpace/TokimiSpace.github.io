<div align="center">

# Tokimi Open Source

**A bilingual entry point to five Tokimi open-source directions, with public scope, evidence, and honest boundaries in one place.**

[繁體中文](README.md) · [English](README.en.md)

[Open-source hub・English](https://tokimispace.github.io/?lang=en) ·
[開源首頁・中文](https://tokimispace.github.io/?lang=zh-TW) ·
[Official Tokimi open-source guide](https://tokimi.space/en/open-source/) ·
[GitHub organization](https://github.com/TokimiSpace)

</div>

> [!WARNING]
> **Fraud alert / 防詐提醒**
>
> Any `@gmail.com` address claiming to represent Tokimi is not an official Tokimi contact channel; do not pay or share verification codes.
>
> 任何以 `@gmail.com` 結尾、並自稱代表 Tokimi／時見數位科技的帳號，都不是 Tokimi 官方聯絡管道；請勿付款或提供驗證碼。
>
> **Verify only through / 請只透過：** [tokimi.space](https://tokimi.space/) · [ben@tokimi.space](mailto:ben@tokimi.space)

![Tokimi Open Source social card: a signal bus connects Rover, AstroGroot, Darkforest Web, BridgeTime Kimi Privacy, and IFF x402 Transparency](social-card-open-source-v3.png)

This repository contains the dependency-free static source for
[TokimiSpace GitHub Pages](https://tokimispace.github.io/?lang=en) and serves as the common entry
point to five projects. It states both what is open and what is not included or proven, so a local
demo, research index, or privacy reference is not mistaken for a complete production service.

## Public scope of the five projects

| Project | What is open | Not included / not evidence of |
| --- | --- | --- |
| 🚗 [Tokimi Rover](https://github.com/TokimiSpace/tokimi-rover) | Dual ESP32-S3 firmware, wiring documentation, audit evidence, and Supercar V3 Blender body CAD | This audit did not repeat physical vehicle safety tests; the CAD size discrepancy still needs an A4 physical fit-check and is not a verified fit |
| 🔭 [AstroGroot](https://github.com/topben/astrogroot) | MIT-licensed Deno/Hono application, collectors, trilingual search, knowledge map, APIs, and MCP | Indexed third-party material is not relicensed; AI summaries are not authoritative and must be checked against original sources |
| 🌲 [Darkforest Web](https://github.com/TokimiSpace/darkforest-web) | Browser frontend, 12 local fixtures, 6 interface locales, and QA tooling | A pre-alpha, loopback-only demo; no production matchmaking, private game core, official service contract, or LiveOps |
| 🛡️ [BridgeTime Kimi Privacy](https://github.com/TokimiSpace/bridgetime-kimi-privacy) | v0.2.0 Private Intent five-field allowlist, pinned Kimi egress, offline wire-capture tests, and a retained alias mode for comparison | Not the complete BridgeTime service or deployment evidence; Kimi still sees abstract operation and account/network metadata, while the alias mode retains re-identification risk |
| 🔎 [IFF x402 Transparency](https://github.com/ifandonlyif-io/iff-x402-transparency) | Public x402 v2 specification, test vectors, standard-library verifier, Go and TypeScript SDKs, and OIDC/SLSA release provenance | Named observations and software provenance are not proof of endpoint honesty, payment safety, TEE/remote attestation, or a composite trust score; manual probes do not affect public cards |

Related production services: [AstroGroot](https://astrogroot.org/?lang=en) ·
[Darkforest](https://darkforest.tw/) · [BridgeTime](https://bridgetime.org/) · [IFF](https://ifandonlyif.io/). Their production scope is not the same as the open repositories above.

## Local preview in 60 seconds

The site is plain HTML, CSS, and JavaScript with no build step:

```bash
git clone https://github.com/TokimiSpace/TokimiSpace.github.io.git
cd TokimiSpace.github.io
python3 -m http.server 8000
```

- English: <http://localhost:8000/?lang=en>
- Chinese: <http://localhost:8000/?lang=zh-TW>

Run the publication checks with:

```bash
python3 scripts/check_site.py
node --check main.js
```

## Language URLs

- Production English: <https://tokimispace.github.io/?lang=en>
- 正式中文：<https://tokimispace.github.io/?lang=zh-TW>

Both languages are authored into the same static page without automatic translation. A valid
`lang` URL parameter takes precedence over a locally remembered choice, so each link is shareable
and bookmarkable.

## Licences, marks, and sharing

This repository uses path-specific **Apache-2.0** and **CC BY 4.0** terms; see
[LICENSES.md](LICENSES.md). Each linked project keeps its own licence map, and this portal does not
relicense third-party material indexed by AstroGroot.

Tokimi, 時見數位科技, and official project identities are not licensed with the source; see
[TRADEMARKS.md](TRADEMARKS.md). A fork may describe its origin truthfully but must not imply
official certification, sponsorship, or affiliation.

The site loads no analytics or trackers. LINE, Facebook, and Twitter/X previews use the committed
[1200 × 630 PNG](social-card-open-source-v3.png).
