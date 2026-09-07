# Batch 01 — Microsoft Copilot (free tier)

**Purpose.** First content batch for the AI Enablement Wiki. One tool, covered properly, so the schema's gaps surface before the wiki grows. Read `SCHEMA.md` first; it is authoritative and this file does not repeat it.

**Scope discipline.** Do not add tools, procedures, or entity types beyond what is listed here. The point of this batch is to test the pipeline and the schema, not to maximize coverage. If a source suggests something outside this list, note it in `BACKLOG.md` and move on.

---

## 1. Pages to produce

### tools/ (1)

| id | notes |
|---|---|
| `copilot-free` | Microsoft Copilot, free consumer tier. The `limitations` field is the most important part of this page: no saved projects, no custom GPTs, no saved skills, no persistent memory across sessions, no file storage. Nearly every procedure below exists because of one of these. State each limitation precisely enough that a procedure can cite it. |

### concepts/ (2)

| id | level | notes |
|---|---|---|
| `system-prompt` | basic | What a system prompt is and why putting role, rules, and output format up front changes results. This is the concept behind the portable-prompt pattern. |
| `single-file-web-app` | basic | Why a self-contained HTML file with inline CSS and JS runs from a double-click with no server, and what that enables for someone who cannot deploy anything. |

### patterns/ (2)

| id | level | solves | notes |
|---|---|---|---|
| `portable-prompt-template` | basic | No saved skills or reusable projects on this tier | Store a role + rules + output-format block as a shared file; paste it above raw input to standardize an operation. Keep this tool-agnostic. It applies equally to any chat tool without saved instructions. |
| `generated-single-file-tool` | intermediate | No app-building or hosting available | Have the model emit a complete standalone HTML/JS file; save and open it locally. Again, tool-agnostic. |

### procedures/ (4)

| id | level | tool | implements | test | notes |
|---|---|---|---|---|---|
| `build-roi-calculator-copilot-free` | intermediate | `copilot-free` | `generated-single-file-tool` | **yes** | Generate a single-file ROI/payback calculator. This is the execution-verification pilot for the batch. |
| `create-data-audit-prompt-block` | basic | `copilot-free` | `portable-prompt-template` | yes | Build a reusable data-audit skill block; verify by running it against a deliberately messy sample. |
| `share-prompt-blocks-with-team` | basic | `copilot-free` | `portable-prompt-template` | no | Distribute prompt blocks via a shared folder and a browser favorites folder. UI-dependent, so `vendor-documented`. |
| `apply-prompt-file-to-data-file` | intermediate | `copilot-free` | `portable-prompt-template` | no | Attach a prompt file and a data file together and instruct the model to apply one to the other. Availability varies by build, so treat capability claims cautiously. |

### roles/ (2)

| id | notes |
|---|---|
| `ops-analyst` | Has free-tier tooling only. Goal: standardize recurring analysis without buying anything. |
| `team-lead` | Cares about distributing a repeatable method to a team, not about doing the task once. |

### paths/ (1)

| id | target_role | notes |
|---|---|---|
| `free-tier-starter` | `ops-analyst` | Sequence: `system-prompt` → `create-data-audit-prompt-block` → `share-prompt-blocks-with-team` → `single-file-web-app` → `build-roi-calculator-copilot-free`. Concepts before the procedures that need them. |

### tests/ (2)

`tests/build-roi-calculator-copilot-free.md` and `tests/create-data-audit-prompt-block.md`. Format is in `SCHEMA.md` section 5.2.

---

## 2. Verification plan for this batch

Per `SCHEMA.md` section 5.1. Applies in order; do not skip ahead.

**Layer 1 — structural, automated, all pages.** Run `validate.py`. Every page must pass before any content review happens. Checks: required frontmatter present; `type` matches folder; every referenced id exists; no circular `prerequisites`; no path references a deprecated or missing page; every procedure has a `verification` block; `confidence` is consistent with `method`; every `test_artifact` path exists or is explicitly null.

**Layer 2 — content, LLM-reviewed, all procedures.** For each procedure, check: every step is imperative and independently observable; no step hides two actions; prerequisites are complete; the success condition in section 4 is actually observable; nothing contradicts the `raw/` source it cites; nothing contradicts another page. Set `method: llm-reviewed`, `confidence: medium` at most. **This layer verifies the writing, not the truth of the claim.**

**Layer 3 — execution, one pilot only.** `build-roi-calculator-copilot-free` is the pilot. Its output is a real HTML file, so it can be genuinely executed and inspected. Run the test in `tests/`, confirm the calculator loads, accepts inputs, and computes correct payback for a known case. If it passes, that procedure alone gets `method: automated`, `confidence: high`.

`create-data-audit-prompt-block` may also reach `automated` if its prompt block is run against a sample messy CSV and the output matches the declared format.

Everything else stays `vendor-documented` and does not advance until a person runs it. **No agent may set `method: human-executed`.**

---

## 3. Ingestion rules specific to this batch

1. Capture sources into `raw/` before deriving anything. Prefer Microsoft's own documentation for capability and limitation claims over third-party blog posts, and note the capture date, because free-tier capabilities change without announcement.
2. Free Copilot's feature set differs by region, account type, and Edge version. Where a capability is uncertain, say so in the page rather than asserting it, and set `confidence: low`.
3. Do not copy prose from sources. Derive and rewrite. Cite the `raw/` file.
4. If two sources disagree about what the free tier can do, create the page with `status: needs-review` and record both claims. Do not silently pick one.
5. Public information only. Nothing internal, proprietary, or personally identifying enters this repository.
6. Regenerate `llms.txt` at the end.

---

## 4. Definition of done

- [ ] 12 pages exist: 1 tool, 2 concepts, 2 patterns, 4 procedures, 2 roles, 1 path
- [ ] 2 test files exist
- [ ] `validate.py` passes with zero errors
- [ ] Every procedure has been through Layer 2 review
- [ ] The ROI calculator pilot has actually been executed, and its result recorded in its test file
- [ ] `llms.txt` regenerated
- [ ] Anything deferred is written to `BACKLOG.md`

---

## 5. What this batch is really testing

The content is a means, not the end. When the batch is done, these are the questions to answer honestly, because they determine whether the schema survives contact with reality.

1. Did the `patterns` vs `procedures` split hold, or did it feel arbitrary while writing?
2. Was `limitations` on the tool page specific enough for procedures to cite, or too vague to be useful?
3. Did the four-value `verification.method` scale capture the real situations, or was something forced into the wrong bucket?
4. Did any page need a relationship not in the section 4 vocabulary?
5. Did `roles/` do any real work, or was it decoration?

Record the answers in `BACKLOG.md`. Schema changes are cheap now and expensive after a hundred pages.
