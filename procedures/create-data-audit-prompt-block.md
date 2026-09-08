---
id: create-data-audit-prompt-block
title: Create a reusable data-audit prompt block
type: procedure
status: active
owner: songws1
created: 2026-09-07
last_reviewed: null
review_cycle_days: 90
level: basic
tool: copilot-free
implements: portable-prompt-template
audience: [ops-analyst]
requires_concepts: [system-prompt]
prerequisites: []
est_time_minutes: 20
superseded_by:
verification:
  method: agent-executed
  reviewed: llm-reviewed
  verified_on: 2026-09-07
  verified_by: claude
  test_artifact: tests/create-data-audit-prompt-block.md
  confidence: medium
tags: []
---

## Why this exists

The free tier documents no way to save a reusable skill inside the product ([[copilot-free]] limitation 2), so a recurring data-quality review is otherwise re-derived from memory each time and its output drifts. This procedure realizes [[portable-prompt-template]] for one concrete recurring task.

## Prerequisites

- A recurring dataset whose quality needs checking (CSV export, spreadsheet range, or pasted table).
- A folder where the block file can be kept (personal documents, or the team folder if [[share-prompt-blocks-with-team]] will follow).

## Steps

1. Create a new text file named data-audit-prompt.md.
2. Paste the block below into it.
3. Save the file.

```text
ROLE: You are a data quality auditor. You report only what is present in the data you are given. You never invent values, rows, or columns.

TASK: Audit the data below for quality problems.

RULES:
1. Report only problems you can point to in the supplied data.
2. For every problem, quote the exact value and name the column and row where it appears.
3. If a column is clean, say so in one line. Do not pad the report.
4. Suggest only manual fixes a person could apply in a spreadsheet.

OUTPUT FORMAT — use exactly these five headings, in this order, and nothing else:
## Column inventory
## Problems found
## Clean columns
## Suggested manual fixes
## Questions for the data owner

DATA (comes after this block):
```

4. Start a new chat in free Copilot.
5. Paste the entire block into the chat.
6. Paste the sample data underneath the block, after the "DATA" marker line — instructions first, data last.
7. Send.
8. Read the reply against the declared format: the five headings, in order, with no extra sections.

## How to verify it worked

Run the block against a deliberately messy sample and confirm three things: the output uses exactly the five declared headings; every problem it quotes exists verbatim in the sample; no row or column appears in the output that is absent from the data. The recorded run is in tests/create-data-audit-prompt-block.md, against tests/sample-messy-data.csv, executed 2026-09-07 by an LLM agent (nondeterministic — see the notes in that test file). Scope: that run covers format conformance and non-invention only — it does not cover whether the findings are exhaustive, or stable across reruns.

## Known failure modes

- **The reply adds sections or skips one** → reply "Output only the five headings from the instructions" and resend the original block unchanged.
- **Findings appear that are not in the data** → the RULES section was not followed; resend the block as-is rather than re-asking in your own words.
- **Very long tables get truncated** → paste only the rows that matter, or chunk the data and audit one chunk per conversation.
- **Different runs flag different problems** → expected; the model is nondeterministic. Treat the block as a checklist accelerator, not a validator — confirm flagged rows yourself before acting on them.

## Sources

- raw/copilot-prompt-four-parts.md — prompt structure; nondeterminism
- raw/copilot-prompt-order.md — order matters; data last
- raw/copilot-free-vs-m365.md — free tier scope
