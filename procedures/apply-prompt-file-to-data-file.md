---
id: apply-prompt-file-to-data-file
title: Apply a prompt file to a data file in one conversation
type: procedure
status: active
owner: songws1
created: 2026-09-07
last_reviewed: null
review_cycle_days: 90
level: intermediate
tool: copilot-free
implements: portable-prompt-template
audience: [ops-analyst]
requires_concepts: [system-prompt]
prerequisites: [create-data-audit-prompt-block]
est_time_minutes: 25
superseded_by:
verification:
  method: vendor-documented
  reviewed: llm-reviewed
  verified_on: 2026-09-07
  verified_by: claude
  test_artifact: null
  confidence: low
tags: []
---

## Why this exists

Applying a standard check to a new dataset without a saved skill ([[copilot-free]] limitation 2) means getting both the instructions and the data into one conversation. Free Copilot documents file upload for free users, but with unpublished capacity limits ([[copilot-free]] limitation 4), and upload behavior varies by build and region — so this procedure keeps a paste fallback that works everywhere.

## Prerequisites

- A saved prompt block file (see [[create-data-audit-prompt-block]]).
- The data as a file (CSV, TXT, or a similar text format) or as text you can paste.

## Steps

1. Open a new chat in free Copilot.
2. Attach the prompt block file. If your build offers no attach control, paste the block text instead.
3. Attach the data file, or paste the data text underneath — instructions first, data last.
4. Send the message with one added line: "Apply the instructions in the first file to the data in the second file and answer in the output format the instructions declare."
5. Read the reply against the block's declared output format.

## How to verify it worked

The reply follows the block's declared format exactly, and every finding quotes values that exist verbatim in the supplied data. If either fails, fall back to pasting the block text and data directly (the [[portable-prompt-template]] route), which does not depend on attachment support.

## Known failure modes

- **No attach control, or the file type is rejected** → availability varies by region, account, and app build; use the paste fallback. This is the single biggest uncertainty on this page — whether attachment of arbitrary files works on a given free account was not verifiable without a live account, hence low confidence.
- **Large files are rejected or only partly read** → subset the data; audit the subset that matters.
- **The model applies the block only partially** (skips a heading, merges two sections) → resend the whole block unchanged rather than negotiating section by section.
- **Results differ between sessions** → capacity limits change and the model is nondeterministic; retry later or fall back to paste.

## Sources

- raw/copilot-app-changes.md — free users can upload files, subject to capacity and limits
- raw/copilot-free-vs-m365.md — free tier scope; regional variation
- raw/copilot-prompt-order.md — instructions first, data last
