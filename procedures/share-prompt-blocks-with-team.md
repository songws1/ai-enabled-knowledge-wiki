---
id: share-prompt-blocks-with-team
title: Distribute prompt blocks to a team without a paid tier
type: procedure
status: active
owner: songws1
created: 2026-09-07
last_reviewed: null
review_cycle_days: 90
level: basic
tool: copilot-free
implements: portable-prompt-template
audience: [team-lead]
requires_concepts: []
prerequisites: [create-data-audit-prompt-block]
est_time_minutes: 15
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

The free tier has no shared skill library, so a block one person refined stays on that person's machine ([[copilot-free]] limitation 2). Distribution has to be built from ordinary file sharing, because the product offers nothing to build it on.

## Prerequisites

- At least one finished block file, produced by [[create-data-audit-prompt-block]] or by the same method.
- A shared folder the whole team can already open — the team's existing drive or document library. Nothing new needs to be purchased.

## Steps

1. Create a folder named ai-prompt-blocks in the team's shared location.
2. Copy one canonical file per block into it, named after the task (for example data-audit-prompt.md).
3. Add a README.txt in the folder that states, in one line each, when to use each block.
4. In the browser profile the team shares, create a bookmarks folder named AI prompt blocks.
5. Bookmark the shared folder's location into that bookmarks folder.
6. Send the team the usage rule in two lines: start a new chat, paste the block, put the data underneath it.

## How to verify it worked

A teammate who did not write the block finds it starting from the bookmark and runs it against their own data successfully. This step is human-observed and has not been executed for this page, which is why this procedure stays at vendor-documented with low confidence until a team-lead runs it for real.

## Known failure modes

- **Some teammates cannot open the folder** → permissions exclude them; test with a non-owner account before announcing.
- **Divergent copies appear** ("final_v2 (3).md") → keep one canonical file per block; changes go into that same file, with a dated note at the bottom of the block.
- **The bookmark is not there for teammates** → the bookmarks folder lives on a profile they do not use; paste the folder path into the team chat instead of relying on bookmarks.
- **Pasting loses the line breaks** → some surfaces mangle pasted text; the file remains the canonical copy, so re-copy from the file.

## Sources

- raw/copilot-free-vs-m365.md — no shared skill storage on the free tier
- raw/copilot-prompt-order.md — the usage rule: block first, data last
