#!/usr/bin/env python3
"""
Generate llms.txt: a small manifest of every page in the wiki.

Why this exists. A remote agent answering a question should not read the whole
repository. It reads this one file, sees what exists, and then fetches only the
two or three pages that matter. That is the entire token-saving mechanism.

Keep the output small. If this file ever grows past a few thousand tokens, split
it by section or shorten descriptions. Do not hand-edit llms.txt; regenerate it.

Usage:
    python scripts/generate_llms_txt.py [repo_root]
"""

import sys
import re
from pathlib import Path

SECTIONS = [
    ("tools", "Tools", "One page per tool and access tier."),
    ("paths", "Learning paths", "Ordered sequences. Start here if unsure where to begin."),
    ("patterns", "Patterns", "Tool-agnostic approaches."),
    ("procedures", "Procedures", "Step-by-step, tool-specific. Check verification.method before trusting."),
    ("concepts", "Concepts", "How and why things work."),
    ("roles", "Roles", "Who material is written for."),
]

HEADER = """# AI Enabled Knowledge Wiki

Getting real work done with AI tools at the access tier you actually have.

HOW TO USE THIS FILE. This is a manifest, not the content. Find the one to three
pages that bear on your question, then fetch only those files. Do not fetch the
whole repository.

VERIFICATION. Every procedure states how strongly it is backed:
  vendor-documented = from docs, nobody executed it
  llm-reviewed      = an AI checked the writing, not the truth of the claim
  automated         = a test ran and passed
  human-executed    = a person did it against the live tool
Report the method when you cite a procedure.

Schema: SCHEMA.md   Routing rules: CLAUDE.md
"""


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    data = {}
    nested = None
    for raw in text[3:end].split("\n"):
        if not raw.strip() or raw.strip().startswith("#") or raw.strip().startswith("- "):
            continue
        if ":" not in raw:
            continue
        indent = len(raw) - len(raw.lstrip())
        key, _, val = raw.strip().partition(":")
        key, val = key.strip(), val.split("#")[0].strip().strip("\"'")
        if indent >= 2 and nested:
            data.setdefault(nested, {})[key] = val
            continue
        nested = key if val == "" else None
        if val:
            data[key] = val
    return data


def first_sentence(text):
    """First real sentence of the body, used when a page has no summary field."""
    body = re.sub(r"^---.*?\n---\n", "", text, flags=re.S)
    body = re.sub(r"^#.*$", "", body, flags=re.M)          # headings
    body = re.sub(r"```.*?```", "", body, flags=re.S)      # code blocks
    body = re.sub(r"[*_`\[\]]", "", body)                  # light md cleanup
    for line in body.split("\n"):
        line = line.strip()
        if len(line) > 20:
            m = re.match(r"(.{0,180}?[.!?])(\s|$)", line)
            return (m.group(1) if m else line[:180]).strip()
    return ""


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    out = [HEADER]
    total = 0

    for folder, heading, blurb in SECTIONS:
        d = root / folder
        if not d.is_dir():
            continue
        rows = []
        for path in sorted(d.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            if fm.get("status") == "deprecated":
                continue  # deprecated pages stay in the repo but off the manifest

            pid = fm.get("id", path.stem)
            title = fm.get("title", pid)
            desc = fm.get("summary") or first_sentence(text)

            bits = []
            if fm.get("level"):
                bits.append(fm["level"])
            if folder == "procedures":
                v = fm.get("verification") or {}
                if v.get("method"):
                    bits.append(v["method"])
                if fm.get("tool"):
                    bits.append(f"on {fm['tool']}")
            if fm.get("status") == "needs-review":
                bits.append("NEEDS REVIEW")
            meta = f" [{', '.join(bits)}]" if bits else ""

            rows.append(f"- `{folder}/{path.name}` — **{title}**{meta}"
                        + (f": {desc}" if desc else ""))
            total += 1

        if rows:
            out.append(f"\n## {heading}\n\n{blurb}\n")
            out.extend(rows)

    out.append(f"\n---\n\n{total} active pages.\n")
    text = "\n".join(out)
    (root / "llms.txt").write_text(text, encoding="utf-8")

    approx_tokens = len(text) // 4
    print(f"Wrote llms.txt: {total} pages, {len(text)} chars (~{approx_tokens} tokens)")
    if approx_tokens > 4000:
        print("WARNING: manifest is getting large. Consider shortening descriptions "
              "or splitting into per-section manifests.")


if __name__ == "__main__":
    main()
