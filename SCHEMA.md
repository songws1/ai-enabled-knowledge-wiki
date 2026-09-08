# AI Enablement Wiki — Schema Specification

**Purpose of this file.** This is the contract that every page in this wiki follows. It exists for two readers: the human maintainer, and any AI agent (Cline, Claude Code, a remote Claude session) that ingests source material into the wiki or answers questions from it. If you are an agent creating or updating a page, this file is authoritative. Do not invent fields, entity types, or relationship names that are not listed here.

**What this wiki is.** A public, working knowledge base about getting real work done with AI tools, at the access tier people actually have. Content is drawn only from publicly available sources. No internal, proprietary, or personally identifying information belongs in this repository.

**Why the structure looks like this.** This wiki is deliberately shaped as a miniature SOP system. The content is public AI knowledge, but the structure rehearses a larger internal system that links SOPs, process maps, a service catalog, and role data. The mapping is documented in the final section. Structure decisions should be made in favor of that eventual transfer, not in favor of short-term convenience.

---

## 1. Folder structure

```
/
  SCHEMA.md          <- this file
  CLAUDE.md          <- router: tells an agent where things live and how to navigate
  AGENTS.md          <- copy of CLAUDE.md, for non-Claude agents
  llms.txt           <- generated manifest for cheap remote lookup (do not hand-edit)
  raw/               <- immutable captured sources, never edited after capture
    <slug>.md
  tools/             <- one page per tool AND tier
  patterns/          <- tool-agnostic reusable approaches
  procedures/        <- concrete, step-by-step, tool-specific instructions
  concepts/          <- explanatory reference knowledge
  roles/             <- audience definitions
  paths/             <- ordered learning sequences
  tests/             <- one test case per verifiable procedure
```

Do **not** create folders by difficulty level (`basic/`, `advanced/`). Level is metadata, not location. The primary axis is entity type, because that is the axis that survives the move to the real system.

---

## 2. Universal frontmatter

Every page in every folder except `raw/` carries these fields.

```yaml
---
id:                 # stable unique slug, never changes once assigned. kebab-case.
title:              # human-readable
type:               # tool | pattern | procedure | concept | role | path
status:             # draft | active | needs-review | deprecated
owner:              # who is responsible for this page being correct
created:            # YYYY-MM-DD
last_reviewed:      # YYYY-MM-DD, or null. see 5.3 — null until a HUMAN confirms the page.
review_cycle_days:  # integer, how long until this page is considered stale
tags: []            # freeform, lowercase
---
```

`id` is the anchor for all cross-references. Rename the file if you must, but never change `id`.

`status: deprecated` pages are kept, not deleted, and must carry `superseded_by`. Deletion destroys the history that makes governance auditable.

---

## 3. Entity types

### 3.1 `tools/` — one page per tool *and tier*

A tool at a different access tier is a different page, because its capabilities and constraints differ materially. `copilot-free` and `copilot-m365` are two pages, not one page with a section.

Additional fields:

```yaml
vendor:             # Microsoft | Anthropic | OpenAI | ...
tier:               # free | licensed | enterprise
access_notes:       # one line: who typically has this
capabilities: []    # what it can do, as short phrases
limitations: []     # what it cannot do. this is what drives procedures.
verified_on:        # YYYY-MM-DD, last date capabilities/limitations were checked
```

`limitations` is the most load-bearing field in this wiki. Nearly every procedure exists because some tier lacks a capability that another tier has. Write limitations precisely enough that a procedure can cite one as its reason for existing.

### 3.2 `patterns/` — tool-agnostic reusable approaches

A pattern describes *a way of solving a class of problem*, independent of which tool you hold. "Simulate saved skills using portable markdown prompt templates" is a pattern. It can be implemented on Copilot free, on Claude chat, or anywhere else.

Additional fields:

```yaml
level:              # basic | intermediate | advanced
solves: []          # the capability gaps this pattern addresses
implemented_by: []  # ids of procedures that realize this pattern
requires_concepts: []
```

Patterns are the abstract layer. They are the analog of a process map. Keep them free of vendor-specific UI steps; those belong in procedures.

### 3.3 `procedures/` — concrete step-by-step instructions

The SOP analog, and the core of this wiki. A procedure is always specific to at least one tool page and is always executable by a named audience.

Additional fields:

```yaml
level:              # basic | intermediate | advanced
tool:               # id of the tools/ page this runs on
implements:         # id of the patterns/ page this realizes, if any
audience: []        # ids of roles/ pages
requires_concepts: []   # ids of concepts/ pages a reader must understand first
prerequisites: []       # ids of other procedures that must be done first
est_time_minutes:   # integer
superseded_by:      # id, only when status is deprecated
verification:       # see section 5.1. required on every procedure.
  method:           # vendor-documented | agent-executed | script-verified | human-executed
  reviewed:         # none | llm-reviewed | human-reviewed
  verified_on:      # YYYY-MM-DD
  verified_by:      # script | claude | <person>
  test_artifact:    # path under tests/, or null if none exists
  confidence:       # high | medium | low
```

Body structure for a procedure, in this order:

1. **Why this exists** — one or two sentences naming the constraint being worked around.
2. **Prerequisites** — what must be true before starting.
3. **Steps** — numbered, imperative, each independently verifiable.
4. **How to verify it worked** — the observable success condition.
5. **Known failure modes** — what commonly goes wrong and what it means.
6. **Sources** — links to the `raw/` captures this was derived from.

Section 4 (verification) is mandatory. A procedure whose success cannot be observed cannot be governed, because nobody can tell whether it still works.

### 3.4 `concepts/` — explanatory reference knowledge

Explains how something works. Does not tell anyone to do anything. "How retrieval-augmented generation works", "what a context window is", "why chunking loses relationships".

Additional fields:

```yaml
level:              # basic | intermediate | advanced
related_tools: []   # ids, optional
see_also: []        # ids of other concepts
```

Concepts should be written so a procedure can link to one instead of re-explaining the idea inline. If the same explanation is appearing inside two procedures, it belongs in a concept page.

### 3.5 `roles/` — audience definitions

Who the material is for. These are generic, publicly describable roles, never named individuals.

Additional fields:

```yaml
typical_tools: []   # ids of tools/ pages this role usually has access to
goals: []           # what this role is trying to accomplish with AI
starting_level:     # basic | intermediate | advanced
```

This folder is the structural rehearsal for employee/org data in the eventual internal system. Keep it purely role-based so nothing personal ever enters the repository.

### 3.6 `paths/` — ordered learning sequences

A curriculum. This is what makes the wiki reusable as training material rather than only as a reference.

Additional fields:

```yaml
target_role:        # id of a roles/ page
sequence: []        # ordered list of ids (procedures, concepts, patterns)
outcome:            # one sentence: what someone can do after completing this
est_total_minutes:  # integer
```

A path must only reference pages that exist and whose `status` is `active`. A path referencing a deprecated page is a build error.

---

## 4. Relationship vocabulary

These are the only relationship names in use. Every relationship is expressed twice: once as a frontmatter field (machine-readable) and once as a `[[wikilink]]` in prose where it aids a human reader.

| Relationship | From | To | Frontmatter field |
|---|---|---|---|
| runs on | procedure | tool | `tool` |
| implements | procedure | pattern | `implements` |
| is implemented by | pattern | procedure | `implemented_by` |
| requires understanding of | procedure, pattern | concept | `requires_concepts` |
| must be done after | procedure | procedure | `prerequisites` |
| is intended for | procedure | role | `audience` |
| typically has access to | role | tool | `typical_tools` |
| is part of | procedure, concept, pattern | path | (via path's `sequence`) |
| replaces | procedure | procedure | `superseded_by` |

Do not introduce new relationship names without updating this table. An uncontrolled relationship vocabulary is the single fastest way to make a knowledge graph unbuildable later.

---

## 5. Governance rules

### 5.1 Verification: what was checked, and how

`verified_on` alone is not enough. A date with no method behind it cannot be audited, because "I read the vendor's documentation" and "I ran these steps and they worked" produce the same date and mean completely different things. Every procedure therefore carries a `verification` block.

**Evidence and review are two different axes.** An earlier version of this schema folded them into one `method` field, which forced a page that had been carefully reviewed but never executed to be graded either as more verified than it was, or as unreviewed. Both were wrong. They are now separate fields:

- `method` answers **how strongly the claims are backed**.
- `reviewed` answers **whether the writing has been checked**.

A page can be well reviewed and completely unverified. That is the normal state for anything requiring a live account, and the schema must be able to say so.

**`method` — the evidence grade, weakest to strongest:**

| `method` | What it means | Who can set it | Trust it for |
|---|---|---|---|
| `vendor-documented` | Derived from official docs. Nobody executed anything. | Agent | A starting draft only |
| `agent-executed` | An LLM agent ran the procedure's test and it passed. Nondeterministic: a rerun can differ. | Agent | Format and structure conformance, not reliability |
| `script-verified` | A deterministic test in `tests/` ran and passed. Same input, same result, every time. | Script or agent | Exactly what the test covers, and nothing beyond it |
| `human-executed` | A person performed the steps against the live tool and observed the success condition | **Person only** | The procedure as a whole |

`agent-executed` and `script-verified` replace the old single `automated` value, because an LLM run and a deterministic script run are not the same strength of evidence and should never share a grade.

**An agent must never set `method: human-executed`.** Only a person may claim that. Claiming it falsely is the failure this entire field exists to prevent, and the validator rejects it.

**`reviewed` — the quality gate:**

| `reviewed` | What it means |
|---|---|
| `none` | Nobody has checked the writing |
| `llm-reviewed` | An agent checked internal consistency, completeness, executable phrasing, and agreement with the `raw/` source |
| `human-reviewed` | A person read the page and believed it |

An agent may set `reviewed` to `none` or `llm-reviewed`, never `human-reviewed`.

So the common case from batch 01 — writing carefully checked, claims only vendor-documented, nobody executed anything — is now expressible exactly: `method: vendor-documented`, `reviewed: llm-reviewed`, `confidence: low`.

**Confidence caps.** `confidence` is set relative to `method`, not independently, and `reviewed` never raises it. A reviewed page whose claims nobody tested is still low confidence.

| `method` | Max `confidence` |
|---|---|
| `vendor-documented` | `low` |
| `agent-executed` | `medium` |
| `script-verified` | `high` |
| `human-executed` | `high` |

**Scope statements are mandatory on any tested procedure.** A test proves something narrower than the procedure. When `method` is `agent-executed` or `script-verified`, the "How to verify it worked" section must state in one sentence what the test does **not** cover. A page that says `script-verified: high` without naming its scope overstates itself, which is the exact failure this system exists to prevent.

**Where an agent's verification genuinely stops.** Anything requiring a live account, a vendor UI, or a paid tier cannot be verified by an agent. Those stay at `vendor-documented` until a person runs them. Do not let a well-written page be mistaken for a verified one.

### 5.2 The `tests/` folder

A procedure whose output is an inspectable artifact (generated code, a prompt template, a file, a config) should have a matching test file at `tests/<procedure-id>.md`:

```markdown
# Test: <procedure-id>
input:        what to feed the procedure
run:          how to execute the test
expect:       the observable pass condition, stated so a machine or a person can judge it
last_run:     YYYY-MM-DD
last_result:  pass | fail | not-run
notes:        anything that makes this test fragile
```

Tests make re-verification repeatable instead of a fresh manual effort each cycle. In the internal system this folder becomes process control testing: the evidence that a documented process still matches reality.

Not every procedure can have a test. A procedure that consists of clicking through a vendor UI has no inspectable artifact, and should say so with `test_artifact: null` rather than pretending otherwise.

### 5.3 Review dates

**Two different dates, and they are not interchangeable.**

- `last_reviewed` means a human read the page and believed it.
- `verification.verified_on` means the procedure was checked by the method named in `verification.method`.

**`last_reviewed` is null until a human reviews the page. Agents must never set it.**

Batch 01 exposed the problem: every page was agent-created and every page carried `last_reviewed` set to its creation date, which made twelve unreviewed pages look reviewed and would have made the staleness calculation lie three months later. A date nobody stands behind is worse than no date, because it silently converts into false assurance.

So an agent creating a page writes `last_reviewed: null`. A person writes the date when they have actually read the page.

Consequences, all intended:

- A page with `last_reviewed: null` is **never stale** — it was never fresh. It is *unreviewed*, which the build reports separately and which is a louder signal, not a quieter one.
- The unreviewed count is the real backlog of human attention this wiki owes. It should be visible, not hidden behind a creation date.
- `created` still records when the page appeared, so nothing is lost.

For AI tooling content, `verified_on` decays much faster than `last_reviewed`, because the tool changes underneath a page that nobody touched. Tracking both is the point. In the eventual internal SOP system these correspond to "someone read this SOP" versus "someone walked this process end to end and confirmed the SOP matches reality", which are also routinely confused.

**Staleness is computed, not asserted.** A page is stale when `today - last_reviewed > review_cycle_days`. The build should list stale pages. Do not mark staleness by hand.

**Suggested review cycles.** Tools and procedures: 90 days. Patterns: 180 days. Concepts: 365 days. Roles and paths: 180 days.

**Ownership is mandatory.** A page without an `owner` is unmaintainable. If nobody will own it, do not create it.

**Deprecate, do not delete.** Set `status: deprecated`, fill `superseded_by`, keep the file.

---

## 6. Rules for agents ingesting sources

1. Capture the source into `raw/` first, unedited, with the retrieval URL and capture date at the top. Never edit a `raw/` file afterward.
2. Only then derive wiki pages from it.
3. One page covers one thing. If a source describes four workarounds, that is four procedure pages, plus possibly one pattern page, not one long page.
4. Reuse an existing `id` rather than creating a near-duplicate page. Search before creating.
5. Every derived page must cite the `raw/` file it came from.
6. If a new source contradicts an existing page, do not silently overwrite. Set the existing page to `status: needs-review` and note the contradiction in the body.
7. Never write anything internal, proprietary, or personally identifying into this repository. If a source contains it, do not capture that source.
8. Regenerate `llms.txt` after any page is added, changed, or deprecated.

---

## 7. Mapping to the eventual internal system

This is why the structure is what it is. Keep this table accurate as the schema evolves.

| This wiki | Internal SOP system |
|---|---|
| `tools/` page | Service catalog entry |
| `patterns/` page | Process map, the abstract flow |
| `procedures/` page | SOP, the concrete executable instance |
| `concepts/` page | Domain reference knowledge |
| `roles/` page | Employee and org data, role level |
| `paths/` page | Onboarding curriculum, competency track |
| `tier` on a tool | System entitlement or access level for a role |
| `owner` | Process owner accountable for the SOP |
| `last_reviewed` + `review_cycle_days` | SOP review governance cycle |
| `verification.method` | Evidence grade behind an SOP: documented policy vs observed practice |
| `tests/` | Process control testing, the evidence an SOP still matches reality |
| `prerequisites` | Upstream process dependency |
| `superseded_by` | SOP version control |
| `requires_concepts` | Required background knowledge for a process |

The content in this repository is disposable. The schema is not. Changes to this file should be made deliberately, because everything downstream, including the eventual internal build, inherits these decisions.
