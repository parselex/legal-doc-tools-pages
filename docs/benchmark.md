---
hide:
  - toc
---

# RAG Evaluation Benchmark

> The benchmark pipeline runs weekly (Mondays 09:00 UTC) in the **private**
> `parselex/legal-doc-tools` repository and publishes its rendered Plotly
> dashboard here. The evaluation itself requires ChromaDB, GCP LLMs, and
> API keys — it cannot run on this public static site. Only the **rendered
> output** (a self-contained HTML file) is mirrored here.

## Live dashboard

<iframe src="../benchmark/" width="100%" height="780" style="border:1px solid #e2e5eb;border-radius:10px;background:#f8f9fb" title="Parselex RAG Benchmark Dashboard"></iframe>

> If the iframe is empty, the benchmark has not been published yet. Run the
> `RAG Benchmark & Dashboard` workflow in the private repo to regenerate.

**Direct link**: [../benchmark/](../benchmark/) · [metrics.json](../benchmark/metrics.json)

## What the benchmark measures

The pipeline (`eval/run_benchmark.py`) evaluates the Parselex RAG system
across three axes:

| Stage | What | Tooling |
|-------|------|---------|
| 1. Retrieval | ChromaDB vector search recall@k for the legal corpus | `--skip-retrieval` in CI (no ChromaDB on the GitHub-hosted runner) |
| 2. Generation | Multi-provider LLM answers (Gemini 2.5-flash primary, Groq llama-3.3-70b fallback, Ollama qwen3.5:35b-a3b local) | `GEMINI_API_KEY` + `GROQ_API_KEY` secrets |
| 3. RAGAS judging | LLM-as-judge scoring (faithfulness, answer relevancy, context precision/recall) | `JUDGE_API_KEY` (Groq) |

## Inputs

- `inputs.skipped` — retrieval is skipped in CI (ChromaDB not available
  on the GitHub-hosted runner); the dashboard reflects generation +
  judging only.
- `inputs.skip_ragas` — skip the LLM-as-judge stage (saves API costs).
- `inputs.providers` — space-separated LLM providers to test
  (e.g. `gemini groq ollama`).
- `inputs.judge_model` — model for the RAGAS judge (default: Groq llama-3.3-70b).

## Outputs

The private repo's `eval/results/` directory contains:

| File | What |
|------|------|
| `dashboard.html` | Self-contained Plotly dashboard (HTML + inline JS) — **mirrored to `/benchmark/` here** |
| `metrics_summary.json` | Machine-readable metrics — **mirrored to `/benchmark/metrics.json`** |
| `allure-results/` | Allure test report artifacts (consumed by the `allure-report` job) |
| `junit-report.xml` | JUnit XML test report |

## Schedule & triggers

- **Weekly**: every Monday 09:00 UTC (`cron: '0 9 * * 1'`).
- **Manual**: `workflow_dispatch` with optional `skip_ragas`, `providers`,
  `judge_model` inputs.

## Cross-repo publish mechanism

The private repo's `.github/workflows/benchmark.yml` was modified to push
its rendered `dashboard.html` + `metrics.json` to this public repo's
`benchmark/` directory (via a PAT with `contents:write` on
`parselex/legal-doc-tools-pages`). This avoids the HTTP 422 blocker on the
private repo's own Pages (Free plan + private repo = no Pages).

See the private repo's `handoff/benchmark-cross-repo` branch for the
modified workflow, and `deliverables/06_benchmark_cross_repo_patch.md`
in the workspace for the patch + setup notes.
