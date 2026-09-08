---
id: portable-prompt-template
title: Portable prompt template (carry the skill as a file)
type: pattern
status: active
owner: songws1
created: 2026-09-07
last_reviewed: null
review_cycle_days: 180
level: basic
solves:
  - No saved skills or reusable projects on this tier
  - Inconsistent results when the same recurring task is run from memory by different people or in different weeks
implemented_by: [create-data-audit-prompt-block, share-prompt-blocks-with-team, apply-prompt-file-to-data-file]
requires_concepts: [system-prompt]
tags: []
---

## The problem

On a tier with no saved skills, no reusable projects, and no persistent memory worth building on, every run of a recurring task starts from scratch. Whoever runs it reconstructs the instructions from memory, and the output drifts — across people, across weeks, across wording.

## The approach

Store the standing instruction block — role, rules, and declared output format, in the shape described in [[system-prompt]] — as an ordinary file kept with the team's other standards. To run the operation, start a fresh conversation, put the block at the top (pasted, or attached as a file where attachment exists), and supply the raw input underneath it, so the standing instructions come first and the data last.

Keep the block governed like any other standard: one canonical file per block, a stated output format so quality is checkable, and changes made in the file rather than improvised in a chat.

This is deliberately tool-agnostic. It works identically on any chat product that lacks persistent instruction storage, and it keeps working if the team moves to another product — the file is the skill, not the product.

## When it applies

- Recurring, well-specified operations: audits, summaries, format conversions, first-draft generation.
- Any chat tool without saved instructions — which is nearly all of them at free tiers.

## When it does not

- Tasks that need live work-data grounding (email, meetings, files behind a sign-in the tier cannot reach).
- Operations whose instructions must change every run — then the block is overhead, not leverage.
- Conversations long enough that the opening block no longer dominates the context; start a fresh conversation per run instead.

## Sources

- raw/copilot-free-vs-m365.md — no skill or project storage documented for the free tier
- raw/copilot-prompt-four-parts.md — what a reusable block should contain
- raw/copilot-prompt-order.md — block first, data last
