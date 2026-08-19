# Tokimi Open Source

Source for the bilingual organization page at
[tokimispace.github.io](https://tokimispace.github.io/).

The page introduces Tokimi projects without hiding their current boundaries:

- [Tokimi Rover](https://github.com/TokimiSpace/tokimi-rover) is a supervised,
  open-source hardware prototype whose source and firmware builds have been
  audited. The current audit did not physically retest the assembled rover.
- Darkforest is planned for a future open-source release. Its source, scope,
  license, and release date have not been announced.

## Local preview

The site is dependency-free HTML, CSS, and JavaScript. From this repository's
root, start any static HTTP server—for example:

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000/`. Run the publication checks with:

```sh
python3 scripts/check_site.py
node --check main.js
```

## Publishing

Every push to `main` validates the page, uploads the repository root as a
GitHub Pages artifact, and deploys it through GitHub Actions. Pull requests run
the same local validation without deploying.

The page loads no analytics, trackers, third-party fonts, remote images, or
package dependencies. Rover links deliberately point to the separate
`TokimiSpace/tokimi-rover` repository rather than being inferred from this
organization-site repository.

## Content boundaries

The abstract Darkforest visual is CSS artwork for this page, not game footage
or production game art. No Darkforest source, download, waitlist, feature set,
license, platform, or date is promised here.

See [LICENSES.md](LICENSES.md) for path-specific licensing and
[TRADEMARKS.md](TRADEMARKS.md) for brand boundaries.
