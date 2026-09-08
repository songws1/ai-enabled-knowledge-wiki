# How this repo gets built

This file records the working method, not the content rules. `SCHEMA.md` governs what a page must contain. `CLAUDE.md` tells an agent how to navigate the wiki. This file says who does what, and why the split exists.

Read it at the start of any session that will add content or change the schema.

---

## The two roles

| | **Spec side** (Claude, in a chat session) | **Build side** (Cline, in this folder) |
|---|---|---|
| Owns | `SCHEMA.md`, `CLAUDE.md`, this file, `BATCH-*.md`, migration instructions | Every page under `tools/` `patterns/` `procedures/` `concepts/` `roles/` `paths/`, everything in `raw/` and `tests/` |
| Does | Designs structure, writes batch briefs, reviews output, diagnoses schema defects, writes migrations | Captures sources, writes pages, runs tests, runs `validate.py`, runs git |
| Cannot | Execute anything on this machine, open a browser, run git, see a file it was not shown | Judge whether the schema itself is wrong; it is inside the spec, not above it |

The maintainer decides. Neither side commits without review.

## Why it is split this way

Cline can actually run things on the machine — a headless browser, a script, a git command — and its tokens are billed separately from the maintainer's chat budget. Claude cannot execute, but it holds the whole schema in view at once and can tell when an output quietly violates it.

The deeper reason is that **the author of a spec is the worst person to execute it.** Following your own spec, you unconsciously patch its gaps as you go and never notice they were there. Batch 01 proved this in both directions:

- Cline found that four limitations the batch brief asserted about free Copilot could not be sourced from vendor documentation, and refused to state them as fact. The brief was wrong; the builder caught it.
- Claude found three schema defects in what Cline produced: `method` conflated evidence with review, `automated` hid the difference between an LLM run and a deterministic script, and `last_reviewed` was being set by agents on pages no human had read.

Neither side would have found the other's error alone. Keep the split.

---

## The loop

1. **Spec.** Claude writes a `BATCH-NN-*.md` naming exactly which pages to produce, the verification plan, and — in its last section — the schema questions this batch is meant to stress-test. Content is the means; testing the schema is the end.
2. **Build.** Cline executes the batch against `SCHEMA.md`, runs `validate.py` to zero errors, regenerates `llms.txt`, and answers the batch's schema questions honestly in `BACKLOG.md`. It does **not** commit.
3. **Review.** Claude reads the output and the BACKLOG answers, and decides whether the schema needs to change before this batch is frozen into history.
4. **Migrate, if needed.** Claude writes a `MIGRATION-NN.md`. Cline applies it and re-validates.
5. **Commit.** Only after validation passes and the maintainer has looked.

Schema changes are cheap now and expensive after a hundred pages. That is why review sits between build and commit, not after it.

---

## How changes get delivered

**Default: Claude writes instructions, Cline edits the file in place.**

Claude does not hand over a rewritten copy of a file that already exists in the repo. A delivered copy means the same file exists in two places, the builder has to guess which is authoritative, and `git diff` shows a wholesale replacement instead of what actually changed and why.

So for an existing file, Claude specifies: which file, which section, what it should say, and the reason. Cline makes the edit. One copy of the truth, and the reasoning survives in the diff.

**Two exceptions, both narrow:**

- **New files.** A scaffold or a first-time file has nothing to conflict with. Claude writes it.
- **Code Claude must test.** `validate.py` is the case. A validator is only worth having if it actually rejects what it claims to reject, so Claude writes it, runs failure cases against it, and hands over a version proven to catch them. Specifying a validator in prose and hoping the builder implements it correctly defeats the purpose.

**Staging folder hygiene.** When Claude does deliver a file, the desktop app drops it in `Claude outputs/`, which is git-ignored. That folder is a handover tray, not repo content: copy the file to its real path, then delete it from the tray. Two versions of `SCHEMA.md` on disk is exactly the confusion the default rule above exists to prevent.

---

## Standing rules for the build side

These hold across every batch. Batch briefs add to them, never relax them.

- `SCHEMA.md` outranks preference and convenience. Do not invent fields, folders, entity types, or relationship names.
- Capture into `raw/` first, unedited, with URL and capture date. Derive afterward. Never edit a `raw/` file.
- Copy from `_templates/` rather than composing frontmatter from memory.
- Never set `verification.method: human-executed` or `verification.reviewed: human-reviewed`, and never set `last_reviewed` to a date. Those three are a person's to claim. The validator enforces it; do not rely on the validator to stop you.
- When sources disagree or documentation is silent, say so on the page and lower confidence. Do not resolve uncertainty by picking the confident-sounding option.
- Out-of-scope ideas go in `BACKLOG.md`. Do not widen a batch while executing it.
- Public information only. Nothing internal, proprietary, or personally identifying.
- Stop and report rather than working around a blocker. A batch that halts halfway with a clear reason is more useful than one that completes by guessing.

## What the review looks for

In rough order of how often it matters:

1. A page claiming more certainty than its evidence supports. This is the failure the whole verification system exists to prevent.
2. A tested procedure whose scope statement is missing or too generous — the test proves something narrower than the page implies.
3. Pattern and procedure content bleeding into each other; vendor-specific steps drifting up into a pattern page.
4. Relationships expressed only in prose when a frontmatter field exists for them.
5. Honest BACKLOG answers. A batch that reports friction is worth more than one that reports everything was fine, because the friction is the schema telling you where it is wrong.
