# AI Enablement Wiki — agent router

You are working in a public knowledge wiki about getting real work done with AI tools, at whatever access tier a person actually has. This file tells you where things live and how to behave. Read it before doing anything else.

**Authoritative files.** `SCHEMA.md` defines every entity type, field, and relationship. It wins over your instincts. `BATCH-*.md` files define scoped work. Do not invent fields, folders, entity types, or relationship names.

**Public repository.** Everything here is world-readable. Nothing internal, proprietary, or personally identifying enters this repo. If a source contains such material, do not capture it.

---

## Where things live

| Path | What it holds | Read it when |
|---|---|---|
| `SCHEMA.md` | The contract every page follows | Before creating or editing any page |
| `llms.txt` | Generated manifest of every page with a one-line description | **First**, when answering a question. It is small and tells you what exists. |
| `raw/` | Immutable captured sources, never edited after capture | Tracing a claim back to its origin |
| `tools/` | One page per tool AND tier | A question names a specific tool |
| `patterns/` | Tool-agnostic reusable approaches | A question is about method, not a specific product |
| `procedures/` | Concrete step-by-step instructions, tool-specific | Someone wants to accomplish a task |
| `concepts/` | Explanatory reference knowledge, no instructions | Someone asks how or why something works |
| `roles/` | Audience definitions, generic roles only | Tailoring an answer to who is asking |
| `paths/` | Ordered learning sequences | Someone asks where to start or what to learn next |
| `tests/` | One test case per verifiable procedure | Checking whether a procedure still works |
| `scripts/validate.py` | Structural validator (Layer 1) | Before committing anything |

---

## Routing rules

**Answering a question.**

1. Read `llms.txt` first. It is deliberately small so this step is cheap. Do not read the whole repo.
2. From the manifest, pick the 1 to 3 pages that actually bear on the question. Fetch only those.
3. If the question is "how do I do X", start in `procedures/`. If it is "how does X work", start in `concepts/`. If it is "what can this tool do", start in `tools/`. If it is "where do I start", start in `paths/`.
4. When you cite a procedure, **always report its `verification.method`**. See the honesty rules below.
5. If nothing fits, say so. Do not synthesize a procedure that is not in the wiki and present it as if it were.

**Creating or updating pages.**

1. Read `SCHEMA.md`.
2. Capture the source into `raw/` first, unedited, with retrieval URL and capture date. Then derive.
3. Search existing ids before creating a page. Reuse rather than near-duplicate.
4. One page covers one thing. Four workarounds in a source means four procedure pages.
5. Every derived page cites the `raw/` file it came from.
6. If a new source contradicts an existing page, set that page to `status: needs-review` and record both claims in the body. Never silently overwrite.
7. Run `python scripts/validate.py .` and fix every error before committing.
8. Regenerate `llms.txt` with `python scripts/generate_llms_txt.py .`.

---

## Honesty rules about verification

This wiki tracks how strongly each procedure is backed by evidence. This is the single most important convention here, because a confidently written page that nobody tested looks exactly like a page that works.

**Two separate fields, two separate questions.** `method` says how strongly the claims are backed. `reviewed` says whether the writing was checked. A page can be carefully reviewed and completely unverified, and that is the normal state for anything needing a live account.

`method`, weakest to strongest:

- `vendor-documented` — from official docs, nobody executed anything. Max confidence `low`.
- `agent-executed` — an LLM ran the test. Nondeterministic; a rerun can differ. Max confidence `medium`.
- `script-verified` — a deterministic test passed. Max confidence `high`.
- `human-executed` — a person did it against the live tool. Max confidence `high`.

`reviewed`: `none`, `llm-reviewed` (an agent checked the writing), or `human-reviewed` (a person read it and believed it).

**You may set `method` to `vendor-documented`, `agent-executed`, or `script-verified`, and `reviewed` to `none` or `llm-reviewed`. You may never set `human-executed` or `human-reviewed`, and you may never write a date into `last_reviewed`.** Those three are a person's to claim. The validator enforces it; do not rely on the validator to stop you.

**When you cite a procedure, report its `method`** — and when the method is `agent-executed` or `script-verified`, report the scope limit the page states. A test proves something narrower than the procedure it belongs to, and the page says where that edge is. Repeating "verified" without its scope is how a narrow test turns into a broad claim.

When something cannot be verified because it needs a live account, a paid tier, or a vendor UI, say so plainly and leave it at `vendor-documented`. Do not let good writing be mistaken for verification.

**`last_reviewed: null` means no human has read the page.** Such a page is not stale, because it was never fresh — it is unreviewed, which is a stronger caveat, not a weaker one. Treat its content accordingly when answering from it.

---

## Governance conventions

- Staleness is computed from `last_reviewed` and `review_cycle_days`, never asserted by hand.
- Every page has an `owner`. If nobody will own it, do not create it.
- Deprecate, never delete: set `status: deprecated`, fill `superseded_by`, keep the file.
- `id` is permanent. Rename files freely; never change an `id` once assigned.

---

## Why this repo is shaped this way

The content here is public AI knowledge and is disposable. The structure is not. This wiki is deliberately built as a miniature SOP system: `tools/` stands in for a service catalog, `patterns/` for process maps, `procedures/` for SOPs, `roles/` for org data, `tests/` for process control testing. Section 7 of `SCHEMA.md` has the full mapping.

Prefer structural decisions that survive that transfer over decisions that are convenient right now.
