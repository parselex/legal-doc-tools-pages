---
hide:
  - navigation
  - toc
---

# Parselex Legal Doc Tools — Public Docs

Welcome to the **static public documentation site** for the Parselex Legal
Document Intelligence Platform.

> [!INFO]
> This site is hosted on **GitHub Pages** and contains only static,
> non-sensitive material: architecture diagrams, reporting research, and
> work-in-progress notes.
>
> The **live application** (chat, document analysis, drafting, RAG search,
> pipeline execution, user accounts) runs on the Parselex orchestrator at
> **[parselex.app](https://parselex.app/auth-gate)** and requires
> authentication.

## Quick links

| Resource | Location |
|----------|----------|
| Live application (auth-gated) | [https://parselex.app](https://parselex.app/auth-gate) |
| Security architecture page | [../security/](../security/index.html) |
| Interactive architecture presentation | [../interactive-technical-layout.html](../interactive-technical-layout.html) |
| Landing page | [../](../) |
| Corpus architecture diagram | [../assets/corpus-flowchart.png](../assets/corpus-flowchart.png) |
| Modules ecosystem diagram | [../assets/modules-ecosystem.png](../assets/modules-ecosystem.png) |
| Pipeline flow diagram | [../assets/pipeline-flow.png](../assets/pipeline-flow.png) |
| High-level architecture | [../assets/architecture.png](../assets/architecture.png) |

## What lives where?

```
parselex.github.io/legal-doc-tools-pages/   <- this static site (public, free)
        |
        |  (separate from)
        |
parselex.app                                <- live FastAPI app (auth-gated)
        |
        +-- /              landing (mirrors this site, but served by FastAPI)
        +-- /auth-gate     login wall (Basic Auth + GitHub OAuth)
        +-- /api/v1/*      18 dynamic API modules (chat, docs, drafting, RAG…)
        +-- /documents, /chat, /analysis, /drafting, /judge,
           /jurisdiction, /library, /modules, /options, /pipeline,
           /rag, /results, /users, /app, /debug   (17 dynamic HTML pages)
```

## Documentation sections

- [**Security Architecture**](security.md) — LexConnect Zero-Trust networking,
  the edge-side PII redaction pipeline ("Ethics Firewall"), and the published
  threat model.

## Why the split?

Static content (this site) changes rarely and benefits from:

- **Free, zero-ops hosting** on GitHub Pages.
- **Edge CDN** via GitHub's global network (plus Cloudflare in front of
  `docs.parselex.app`).
- **Decoupled releases** — docs and architecture diagrams can ship without
  redeploying the application.
- **Public visibility** — no auth wall for prospective users reading the
  architecture and reporting research.

Dynamic content (the application) stays on the orchestrator because it
requires:

- Authenticated sessions (Basic Auth + GitHub OAuth).
- Live access to ChromaDB, the GCP L4/A100 GPU pool, and DeepSeek/Gemini/
  Groq API keys.
- User-uploaded document storage and per-user RAG state.
