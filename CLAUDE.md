# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Public marketing site for NOON Tech (independent language-app studio), served by GitHub Pages from `main` at the repo root: https://noonelche-cyber.github.io/noon-tech-site/. Anything merged to `main` goes live automatically.

It is a dependency-free static site: hand-written HTML, one CSS file, a few vanilla JS files. No package.json, no bundler, no tests, no linter, no trackers, no cookies or localStorage — keep it that way.

## Commands

- Preview locally: `python3 -m http.server 8000` from the repo root, then open `http://127.0.0.1:8000/`. The i18n link rewriting treats `127.0.0.1` like the production `/noon-tech-site/` path, so use that host (not `localhost`) when checking `?lang=` propagation.
- Regenerate the KARDASH template previews after editing any `apps/kardash/templates/files/*.json` or the template page: `node scripts/build-template-previews.cjs`. It rewrites `apps/kardash/templates/index.html` in place, and throws if the example values in the script don't match a template's field count or if the page doesn't contain exactly 13 template cards. Adding/removing a template means updating the `examples` map and the count in the script.
- KARDASH bundle ZIPs in `apps/kardash/templates/bundles/` are committed binaries matching `bundles.json`; rebuild them if their template lists or JSON files change.

## Architecture

**Pages.** Each URL is a directory with an `index.html` (`about/`, `contact/`, `apps/<id>/`, `privacy/`, `privacy/<id>/`). These paths are permanent links used by the Android apps and Store listings — don't rename or remove them. All links are relative (`./`, `../../`) because the site lives under `/noon-tech-site/`. Pages share markup by copy, not by include: header, language picker, footer and script tags are duplicated across every HTML file, so site-wide changes must be applied to all of them (including `404.html`).

**i18n (`assets/i18n.js` + `assets/i18n-extra.js`).** HTML is authored in English; translation happens client-side by exact-string lookup. `i18n.js` walks every text node, `aria-label` and `document.title`, trims each, and replaces it if the English string is a key in the dictionary. Consequences:
- A new or edited English string in HTML must be added with the *identical* text as a key, or it silently stays English.
- Dictionary sources: `rows` in `i18n.js` (en/fr/es), `window.NOON_EXTRA` (it/nl/de for those same keys), and `window.NOON_JODER` in `i18n-extra.js` (6-column rows `[en, fr, es, it, nl, de]`) — new strings normally go in a `NOON_JODER.push(...)` block. `i18n-extra.js` must load before `i18n.js`.
- Elements with `translate="no"` (and their descendants) are skipped.
- Default language is French; `?lang=fr|es|en|it|nl|de` selects another, and same-origin links get `?lang=` appended so the choice persists without storage.

**Cache busting.** CSS and the i18n scripts are referenced with a `?v=` query (currently `espresiones-1`; images use `20260912`). When `assets/style.css`, `i18n.js` or `i18n-extra.js` change, bump the version string in every HTML file that references it.

**Store buttons (`apps.json` + `assets/store.js`).** `apps.json` is the app registry. App pages contain a `[data-store="<id>"]` element; `store.js` fetches `../../apps.json` and, only if that app's `store` is an HTTPS `play.google.com` or `apps.apple.com` URL, injects a download button and fires `store-ready` so i18n re-translates it. `store` is `null` for every app today. When adding a real Store link, also change the "Coming soon" status on the home-page card in `index.html`. Never invent Store links or prices.

**Home page cards** in `index.html` are static and duplicate data from `apps.json` (name, tag, description, language count); keep both in sync along with the collection counter (`THE NOON COLLECTION / 01—05`, which is itself a translation key).

## Content rules from the README

- App privacy pages are not finalized: they must describe each app's real data practices before Store submission — don't fill them with invented policies.
- Language counts distinguish interface languages from bilingual content (e.g. ¡JODER! has 6 interface languages; VOSOTROS and TRAMPA are French/Spanish content). Keep `apps.json` `includedLanguages`/`languageScope`, the cards and the app pages consistent.
- KARDASH template JSON files use French field labels by design.

Note: the README still lists DREK! URLs; DREK was replaced by ESpresiones and `apps/drek/` no longer exists.
