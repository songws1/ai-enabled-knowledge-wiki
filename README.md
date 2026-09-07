# AI Enabled Knowledge Wiki

A public, structured knowledge base about getting real work done with AI tools, at whatever access tier you actually have.

Most AI guidance assumes you have the paid tier. This wiki starts from the opposite premise: you have what your organization gave you, that tier is missing features, and there is usually a way to work around the gap. Each procedure names the constraint it exists to solve.

## What is in here

| Folder | Contents |
|---|---|
| `tools/` | One page per tool **and tier**. Free Copilot and licensed Copilot are separate pages, because their limits differ. |
| `patterns/` | Reusable approaches that are not tied to any product. |
| `procedures/` | Step-by-step instructions for a specific tool. |
| `concepts/` | How and why things work. No instructions. |
| `roles/` | Who the material is for. Generic roles only. |
| `paths/` | Ordered learning sequences. |
| `tests/` | Test cases for procedures whose output can be inspected. |
| `raw/` | Captured sources, unedited. |

## How claims are backed

Every procedure carries a `verification.method` saying how strongly it is backed:

| Method | Meaning |
|---|---|
| `vendor-documented` | Taken from official docs. Nobody executed it. |
| `llm-reviewed` | An AI checked the writing for consistency and completeness. Not a check that the claim is true. |
| `automated` | A test in `tests/` ran and passed. |
| `human-executed` | A person performed the steps against the live tool and observed the result. |

Read the method before trusting a page. A well-written procedure that nobody has run is still a well-written procedure that nobody has run.

## Contributing

1. Read `SCHEMA.md`. It is the contract, and it wins over preference.
2. Capture your source into `raw/` before writing anything derived from it.
3. Run `python scripts/validate.py .` and fix all errors.
4. Regenerate the manifest: `python scripts/generate_llms_txt.py .`

Public information only. Nothing internal, proprietary, or personally identifying belongs in this repository.

## For AI agents

Start with `CLAUDE.md` (or `AGENTS.md`, which is identical). When answering a question, read `llms.txt` first: it is a small manifest of every page, so you can find the two or three pages that matter without reading the repository.

## License

MIT. See `LICENSE`.
