# Parselex — Documentation Site

> **Public static site** for the Parselex Legal Document Intelligence Platform,
> served at **[docs.parselex.app](https://docs.parselex.app/)** via GitHub Pages.
> The live application (auth-gated, dynamic) lives at
> **[parselex.app](https://parselex.app/auth-gate)**.

## What is here

| Path | What |
|------|------|
| `index.html` | Landing page, English canonical |
| `ru/` `es/` `fr/` `hi/` | Localized landing pages (Russian, Spanish, French, Hindi) |
| `legal/{privacy,personal-data,cookies,payments,terms,disclaimer}/` | 6 legal pages, English (canonical) |
| `{ru,es,fr,hi}/legal/<slug>/` | The same 6 legal pages, localized (24 pages) |
| `security/` + `{ru,es,fr,hi}/security/` | Security architecture page (LexConnect / Zero-Trust), 5 languages |
| `docs/` + `mkdocs.yml` | MkDocs Material documentation (`/docs/`) |
| `benchmark/` | RAG benchmark dashboard |
| `assets/` | Architecture diagrams, favicon |
| `interactive-technical-layout.html` | Interactive SVG architecture presentation |
| `auth-gate/`, `signup/` | Redirect stubs to the live application |
| `.github/workflows/deploy.yml` | Build (MkDocs + static) → deploy to Pages |

## Key URLs

| Resource | URL |
|----------|-----|
| Site root | <https://docs.parselex.app/> |
| Documentation | <https://docs.parselex.app/docs/> |
| Security architecture | <https://docs.parselex.app/security/> |
| RAG benchmark | <https://docs.parselex.app/benchmark/> |
| Legal pages (EN) | <https://docs.parselex.app/legal/terms/> and siblings |
| Live application | <https://parselex.app/auth-gate> |

## Languages

The site ships in 5 languages (`en` / `ru` / `es` / `fr` / `hi`), using
path-prefixed pages (`/`, `/ru/`, `/es/`, `/fr/`, `/hi/`). Every page carries
`rel="canonical"` + `hreflang` alternates, localized meta/OG tags, and a
language switcher. Legal and security pages follow the same locale model with
locale-prefixed cross-links.

## Deploy

Pushes to `main` trigger `.github/workflows/deploy.yml`, which:

1. Builds MkDocs Material into `site/docs/`.
2. Assembles the static root (landings, legal, security, benchmark, assets)
   alongside it.
3. Uploads and deploys the artifact to GitHub Pages.

Manual deploy: **Actions → Deploy Pages → Run workflow**.

## Split boundary (security)

This repository holds static, non-secret content only. Never commit secrets
(API keys, SSH/VPN keys, service-account JSON) or dynamic application pages.
Dynamic routes are served by the FastAPI application at `parselex.app`.

## License

Proprietary — Parselex. Public repository for static presentation only.
