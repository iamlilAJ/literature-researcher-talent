# Literature Conflict Researcher

A [OneManCompany](https://github.com/1mancompany/OneManCompany) talent that turns a research topic into a queryable knowledge graph of paper-level claims, then surfaces methodological conflicts and proposes new testable methods grounded in authors' own acknowledged limitations.

Powered by [aigraph](https://github.com/iamlilAJ/literature-conflict-graph) — an offline arXiv corpus + claim extraction + conflict graph + creator-mode hypothesis pipeline.

## What it does

- Builds offline corpora from arXiv (4000–5000+ papers per topic) with full-text + section parsing + Semantic Scholar citation enrichment
- Extracts structured claims (16 fields per claim) per paper, every claim grounded with a verbatim `evidence_span`
- Reads each paper's limitations and conclusion sections for explicit acknowledged limitations / future-work suggestions / untested extensions
- Detects 7 categories of cross-paper anomaly: `impact_conflict`, `benchmark_inconsistency`, `setting_mismatch`, `metric_mismatch`, `evidence_gap`, `community_disconnect`, `bridge_opportunity`
- Produces two complementary hypothesis streams per anomaly:
  - **Critic mode** — methodological critique grounded in claims (e.g. "Pass@1 vs F1 reverses the ranking on this benchmark cluster")
  - **Creator mode** — concrete NEW method proposals grounded in conflicts + authors' own open questions, each with a falsifiable `minimal_test`

## Install

This talent is published as a standalone repo. Drop it into your OMC instance:

```bash
git clone https://github.com/iamlilAJ/literature-researcher-talent.git \
  src/onemancompany/talent_market/talents/literature-researcher
```

Then install the `aigraph` engine alongside OMC. Add to your OMC `pyproject.toml`:

```toml
[project.optional-dependencies]
literature-researcher = [
    "aigraph[real] @ git+https://github.com/iamlilAJ/literature-conflict-graph.git@v0.2.0",
]
```

And run:

```bash
uv sync --all-extras
```

> **Note:** `pyproject.toml` for hatch-built OMC also needs:
> ```toml
> [tool.hatch.metadata]
> allow-direct-references = true
> ```
> so hatchling will accept the git URL.

## Hire and use

```text
You: "I want to research methodological conflicts in LLM reasoning"
CEO: "Hiring literature-researcher"
literature-researcher's agent autonomously:
  1. Builds an arxiv reasoning corpus
  2. Extracts claims + open questions
  3. Detects 7 categories of conflict
  4. Generates both critic and creator hypotheses
  5. Hands you `selected.md` + an interactive graph HTML
```

## Skills

| skill | what it does |
|---|---|
| `corpus-build` | Seeds candidate papers from arXiv, syncs full text via TeX/HTML/PDF fallback, enriches with Semantic Scholar citations |
| `claim-extract` | Extracts structured claims and OpenQuestion records (limitations / future-work / untested-extensions) per paper |
| `conflict-detect` | Builds typed claim graph, detects 7 categories of anomaly |
| `idea-synthesize` | Generates 1-3 NEW method proposals per anomaly, each grounded in ≥2 claim_id or open_question_id citations and shipping a falsifiable minimal_test |

## Custom tools

| tool | purpose |
|---|---|
| `aigraph_corpus_build` | Build / refresh corpus (seed + sync + optional Semantic Scholar enrich) |
| `aigraph_corpus_status` | Report corpus manifest health (sync status, citation coverage) |
| `aigraph_extract_claims` | Run LLM claim extractor with thread-pooled workers |
| `aigraph_extract_open_questions` | Surface acknowledged limitations and future-work signals |
| `aigraph_pipeline_run` | Full e2e: graph + anomaly + critic + creator hypotheses + select + visualize |

## Cost guard

| stage | cost | wall time |
|---|---|---|
| Corpus build (5000 papers) | $0 | 2-3 hours (network bound) |
| Citation enrich (5000 papers) | $0 | 15s (Semantic Scholar batch API) |
| Claim extract (5000 papers, 8 workers) | ~$50 | ~3 hours |
| Open-question extract (5000 papers) | ~$50 | ~14 hours serial |
| Pipeline run (graph + anomaly + critic + creator) | ~$2-5 | ~30 minutes |

The talent should ask before scaling beyond a 200-paper preview.

## Validated end-to-end on 100 reasoning papers

- 408 claims (LLM, 100% with grounded evidence_span)
- 212 OpenQuestions surfaced from limitations + conclusions
- 1431 anomalies detected (77 high-signal)
- 231 critic hypotheses (100% unique) + 179 creator hypotheses (100% unique, 100% grounded)
- `selected.md` (top 12) + interactive `index.html` generated

## Engine repo

[iamlilAJ/literature-conflict-graph](https://github.com/iamlilAJ/literature-conflict-graph) — the `aigraph` Python package this talent wraps. Pinned to `v0.2.0` in this talent.

## License

MIT — see `LICENSE`.

---

## Citation

> **DO NOT REMOVE THIS SECTION** — Required by the [Talent Market Attribution License](https://github.com/1mancompany/talent-template/blob/main/LICENSE) of the upstream template.

This talent was built using the [Talent Market](https://one-man-company.com) template by [Zhengxu Yu](mailto:yuzxfred@gmail.com) / [1mancompany](https://github.com/1mancompany).

```
@software{talentmarket,
  title  = {Talent Market - AI Agent Marketplace},
  author = {Zhengxu Yu},
  email  = {yuzxfred@gmail.com},
  url    = {https://one-man-company.com},
  year   = {2026}
}
```
