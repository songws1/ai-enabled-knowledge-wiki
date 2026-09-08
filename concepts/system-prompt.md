---
id: system-prompt
title: The system prompt (a fixed instruction block)
type: concept
status: active
owner: songws1
created: 2026-09-07
last_reviewed: null
review_cycle_days: 365
level: basic
related_tools: [copilot-free]
see_also: []
tags: []
---

## In short

A system prompt is a block of standing instructions — the role to play, the rules to follow, and the output format to return — placed at the start of a conversation so that every later response in that conversation is shaped by it, before any data is supplied.

## How it works

An instruction block fixes three things that would otherwise drift: who the assistant is acting as, what rules it must obey, and what shape its answer takes. Microsoft's own prompt guidance describes a prompt as having up to four parts — goal, context, expectations, and source — of which only a clear goal is required, and adding the rest makes results more specific.

Three documented properties matter when designing such a block:

- **Order matters.** "Later parts of a prompt are likely to be emphasized more than earlier parts", and material the model should work from (files, sources, data) should be put last. A reusable block therefore goes first and the data goes underneath it.
- **Positive phrasing works better.** Telling the model what to do outperforms telling it what not to do; "if-then" phrasing is recommended for conditional behavior.
- **Nondeterminism is real.** Microsoft states that "using the same prompt multiple times can result in different responses" because of neural-network randomness. A fixed block reduces variance; it does not eliminate it. Outputs still need checking against a declared format.

A system prompt in the strict sense is set by the product, not the user. What a free-tier user can build is the same thing expressed as an ordinary message at the top of the conversation — which behaves like a system prompt for the rest of that conversation.

## Why it matters here

On a tier with no saved skills and no reusable projects, the only place a "skill" can live is a file the user keeps and pastes or attaches at the start of each conversation. That file is a system prompt by another route, and it is the entire mechanism behind [[portable-prompt-template]] and the procedures that implement it.

## Sources

- raw/copilot-prompt-four-parts.md — the four-part prompt structure; only the goal is required; nondeterminism
- raw/copilot-prompt-order.md — order matters; data last; positive instructions
