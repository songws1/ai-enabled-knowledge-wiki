---
id: generated-single-file-tool
title: Generated single-file tool (the model emits the software)
type: pattern
status: active
owner: songws1
created: 2026-09-07
last_reviewed: null
review_cycle_days: 180
level: intermediate
solves:
  - No app-building or hosting available on this tier
  - No deployment rights or budget for small calculators, checklists, and converters
implemented_by: [build-roi-calculator-copilot-free]
requires_concepts: [single-file-web-app]
tags: []
---

## The problem

A small but real piece of software — a payback calculator, a checklist, a unit converter — would traditionally need a developer, a hosting decision, or admin rights to deploy. A free-tier chat user has none of those.

## The approach

Ask the model to emit one complete, standalone HTML file: markup, inline CSS, inline JavaScript, and no external references of any kind (see [[single-file-web-app]] for why such a file runs anywhere). Save the emitted text as a `.html` file, open it in the browser, and distribute it like any other file.

Two disciplines make the result governable rather than a one-off trick:

- **Specify the interface, not just the feature.** Naming the inputs, the outputs, the formulas, and the element ids in the request makes different generations comparable and makes the artifact testable.
- **Verify with a known case before trusting any number.** The model writes the formulas; the requester must check them against one hand-computed case. An untested generated calculator is a plausible-looking spreadsheet with unchecked formulas.

## When it applies

- Single-user, offline-capable, logic-only tools: calculators, checklists, converters, formatters.
- Situations where the artifact can be verified by inspecting the file.

## When it does not

- Anything needing a database, concurrent multi-user editing, server-side secrets, or scheduled runs.
- Anything whose correctness cannot be checked without a running backend.

## Sources

- raw/copilot-free-vs-m365.md — no hosting or app platform on the free tier
- raw/mdn-local-html-files.md — what makes a single file runnable
- raw/copilot-prompt-order.md — how to structure the generation request
