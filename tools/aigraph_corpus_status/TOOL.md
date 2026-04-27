---
name: aigraph_corpus_status
description: Report status of an offline arXiv reasoning corpus — total entries, sync_status breakdown, artifact count, citation coverage. No LLM calls.
---

# aigraph_corpus_status

Pure local file read. Use before any downstream skill to confirm the corpus is ready, or to give the user a snapshot of what they have.

## When to use

- User asks "what papers do we have" / "how big is the corpus" / "how is the sync going"
- Before kicking off `aigraph_extract_claims` or `aigraph_pipeline_run`, to verify there is a manifest with completed artifacts

## Parameters

| Name | Type | Default | Notes |
|---|---|---|---|
| `root` | string | required | Corpus root directory. |

## Output (one-line string)

```
manifest_entries=4895 sync_status={'complete':4926,'queued':24} artifact_dirs=4926 papers_with_citations=4885 avg_cit=87
```

If the manifest does not exist, returns `no manifest found at <path>`.

## Cost / time

- $0
- < 1 second for any realistic corpus size
