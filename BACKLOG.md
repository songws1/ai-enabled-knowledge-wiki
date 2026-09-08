# Backlog

Things deferred, and questions the schema has not answered yet. Batch documents
tell you to record findings here rather than expanding scope mid-batch.

## Schema questions raised during work

<!-- After each batch, answer these honestly. Schema changes are cheap now and
     expensive after a hundred pages. -->

### Batch 01 (copilot-free), 2026-09-07

**1. Did the `patterns` vs `procedures` split hold, or did it feel arbitrary?**

It held. One moment of pressure was informative: while writing
portable-prompt-template, the mechanics of paste-versus-attach kept trying to
creep into the pattern page. The split forced the pattern to stay at "store the
block as a file; instructions first, data last" and pushed every UI detail down
into the three procedures implementing it — which is where those details belong.
The 1-to-3 pattern-to-procedure ratio is where the abstraction actually paid
for itself. Not arbitrary.

**2. Was `limitations` on the tool page specific enough for procedures to cite?**

Mostly, with two frictions.

- Citing by number ("limitation 2") is fragile: reorder the tool page's list
  and every citation silently points somewhere else. The procedures ended up
  paraphrasing the limitation inline next to the number, which survives
  reordering but duplicates text. A convention needs choosing: cite by number,
  by quoted phrase, or by stable slug.
- The batch expected limitations (no persistent memory, no custom GPTs, no
  saved projects, no file storage) could not be sourced affirmatively from
  vendor documentation. The captures support only absence-of-documentation
  claims, so the tool page carries a "Not verifiable from vendor
  documentation" subsection and its limitations list is shorter and more
  careful than the batch brief assumed. Consequence: the `limitations` field
  quietly mixes two kinds of claims — vendor-documented absences, and
  observations that documentation is silent. Worth deciding whether those
  belong in one field.

**3. Did the four-value `verification.method` scale capture the real situations?**

Something was forced. Batch 01 gives three instructions that conflict for the
two procedures that were content-reviewed but never executed
(share-prompt-blocks-with-team, apply-prompt-file-to-data-file):

- Layer 2 says: "Set method: llm-reviewed, confidence: medium at most" for all
  procedures.
- Layer 3 says: "Everything else stays vendor-documented and does not advance
  until a person runs it."
- The batch table says, for share: "UI-dependent, so `vendor-documented`."

Resolution taken: the table and Layer 3's sentence won — both pages are
`vendor-documented`, confidence low. The Layer 2 review did happen, but
recording it as `llm-reviewed` would overstate the evidence, because the field
reads as "this procedure works", and nothing here has been shown to work.
The scale has no way to express "writing reviewed, claims vendor-documented,
nobody executed anything" as one grade.

Second gap: create-data-audit-prompt-block was executed by an LLM agent, which
SCHEMA's `automated` row permits ("Script or agent"). But an LLM-executed
prompt test is materially weaker than a deterministic script test — it is
nondeterministic and only checks format conformance and non-invention. Its
confidence was deliberately capped at medium, but nothing in the vocabulary
distinguishes it from a script run. A sub-flag on `automated` (deterministic
vs agent-executed), or a fifth method, would remove the ambiguity.

**4. Did any page need a relationship not in the section 4 vocabulary?**

Twice, both minor, neither worth a new relationship name:

- Procedures want to cite specific tool limitations as their reason for
  existing. There is no relationship for limitation-citation; the batch
  anticipated this by making limitation text citable, and prose citation
  worked. The citation-format question from answer 2 applies here too.
- Test files want to state scope ("this test verifies the artifact spec, not
  the live-model behavior"). `tests/` files have no frontmatter and no
  relationships, so the scope statement lives in prose notes. Acceptable, but
  it means the strongest verification signal in the wiki (automated) carries
  its own caveat only as unstructured text.

**5. Did `roles/` do any real work, or was it decoration?**

Real work, but narrow. `audience` on procedures and `target_role` on the path
are required fields pointing at roles, so the pages must exist — that part is
structural. Content-wise, roles shaped two decisions: the share procedure's
verification stays low until a team-lead (not the page author) observes a
teammate running a block, and the path's outcome is written as a capability
check for the ops-analyst role. Where it was decoration: the `goals` lists
paraphrase what the procedures already say, and no page in this batch needed a
second role. Verdict: keep roles/ — the internal-system mapping depends on it
— but its value flows through the `audience`/`target_role` wiring, not the
prose.

**One more tension, not in the batch's five:** SCHEMA 5.3 defines
`last_reviewed` as "a human read the page and believed it", but the field is
mandatory and every batch-01 page was created by an agent. All pages carry
`last_reviewed: 2026-09-07` (creation day). A human review pass should update
it; until then the field means "agent-set on creation day" on every page in
the wiki. Either the field definition needs an agent-created-page rule, or
agents should stop setting it (but then the validator fails).

### Resolution — schema revision 2 (2026-09-07, applied by MIGRATION-01)

Question 3 and the `last_reviewed` tension above were both resolved in schema
revision 2, before batch 01 was committed:

- **Question 3 (the `method` conflict).** The evidence axis and the review
  axis are now separate fields: `method` (vendor-documented |
  agent-executed | script-verified | human-executed) says how strongly the
  claims are backed; `reviewed` (none | llm-reviewed | human-reviewed) says
  whether the writing was checked. The old single `automated` grade was split
  into `agent-executed` (nondeterministic, capped at medium) and
  `script-verified` (deterministic, capped at high) — the sub-flag this
  answer asked for. Confidence caps are now enforced by the validator
  (vendor-documented can never claim more than low). All four batch-01
  procedures were remapped accordingly, and the two vendor-documented ones
  now carry `reviewed: llm-reviewed`, which the old vocabulary could not
  express.
- **The `last_reviewed` tension.** Agents now write `last_reviewed: null`;
  only a person writes a date. Null pages are reported by the validator under
  a separate UNREVIEWED heading — that count is the deliverable, not a
  failure. All twelve batch-01 pages were reset to null.

Deliberately left open: question 2 (limitation-citation convention) and
question 5 (roles verdict). Deferred-tooling item "validate.py should fail
when llms.txt is out of date" was already recorded below and remains open.

## Deferred content

- **A person running build-roi-calculator-copilot-free end to end on live free
  Copilot.** This is the single highest-value pending verification in the
  batch: the artifact spec is tested (script-verified, high), but "free Copilot
  emits an artifact meeting the spec" is still unproven. Owner: songws1.
- **A live check of file-attachment availability on a real free account** for
  apply-prompt-file-to-data-file, ideally in more than one region. The
  procedure's low confidence hangs entirely on this.
- **A live check of the "Not verifiable from vendor documentation" items on
  the tool page** (persistent memory, custom GPTs, saved projects, file
  retention) against the actual product; the page body should then be updated
  with observed facts.
- **Edge sidebar Copilot variant of the paste-block workflow** — noted, not
  written. Out of batch scope.

## Deferred tooling

- `validate.py` does not check that `llms.txt` is current. CI should run
  `generate_llms_txt.py` and fail on a diff, so a forgotten regeneration is
  caught mechanically.
- The data-audit test's LLM execution could later be scripted against a model
  API to make it deterministic and repeatable without an agent session.
- Decide and document the limitation-citation convention (see schema question
  2), then normalize the four procedures to it.
