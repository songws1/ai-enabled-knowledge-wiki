#!/usr/bin/env python3
"""
Structural validator for the AI Enablement Wiki (Layer 1).

Checks only what can be checked mechanically: schema conformance, referential
integrity, and staleness. It does NOT check whether content is correct or
whether a procedure actually works. That is Layer 2 and Layer 3.

Usage:
    python validate.py [repo_root]

Exit code 0 = pass, 1 = errors found. Wire into CI so a broken repo fails loudly.
"""

import sys
import re
import datetime
from pathlib import Path

# ---------------------------------------------------------------- config

ENTITY_FOLDERS = {
    "tools": "tool",
    "patterns": "pattern",
    "procedures": "procedure",
    "concepts": "concept",
    "roles": "role",
    "paths": "path",
}

UNIVERSAL_FIELDS = [
    "id", "title", "type", "status", "owner",
    "created", "last_reviewed", "review_cycle_days",
]

TYPE_FIELDS = {
    "tool": ["vendor", "tier", "capabilities", "limitations", "verified_on"],
    "pattern": ["level", "solves"],
    "procedure": ["level", "tool", "audience", "est_time_minutes", "verification"],
    "concept": ["level"],
    "role": ["typical_tools", "goals", "starting_level"],
    "path": ["target_role", "sequence", "outcome"],
}

VALID_STATUS = {"draft", "active", "needs-review", "deprecated"}
VALID_LEVEL = {"basic", "intermediate", "advanced"}
VALID_METHOD = {"automated", "llm-reviewed", "human-executed", "vendor-documented"}
VALID_CONFIDENCE = {"high", "medium", "low"}

# method -> the highest confidence it may claim
MAX_CONFIDENCE = {
    "vendor-documented": "medium",
    "llm-reviewed": "medium",
    "automated": "high",
    "human-executed": "high",
}
CONFIDENCE_RANK = {"low": 0, "medium": 1, "high": 2}

# fields whose values are ids pointing at other pages
REF_FIELDS_SINGLE = ["tool", "implements", "superseded_by", "target_role"]
REF_FIELDS_LIST = [
    "audience", "requires_concepts", "prerequisites",
    "implemented_by", "typical_tools", "see_also",
    "related_tools", "sequence",
]

DEFAULT_REVIEW_CYCLE = {
    "tool": 90, "procedure": 90, "pattern": 180,
    "concept": 365, "role": 180, "path": 180,
}

errors = []
warnings = []


def err(page, msg):
    errors.append(f"ERROR  {page}: {msg}")


def warn(page, msg):
    warnings.append(f"WARN   {page}: {msg}")


# ---------------------------------------------------------------- parsing

def parse_frontmatter(text):
    """
    Minimal YAML-ish frontmatter parser. Deliberately dependency-free so this
    runs anywhere. Handles scalars, inline lists, block lists, and one level
    of nesting (which is all the schema uses).
    """
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end].strip("\n")

    data = {}
    current_list_key = None
    current_map_key = None

    for raw_line in block.split("\n"):
        if not raw_line.strip() or raw_line.strip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip())
        line = raw_line.strip()

        # block list item
        if line.startswith("- "):
            value = line[2:].strip().strip("\"'")
            if current_map_key and indent >= 4:
                pass  # nested lists under a map are not used by the schema
            elif current_list_key:
                data.setdefault(current_list_key, []).append(value)
            continue

        if ":" not in line:
            continue

        key, _, value = line.partition(":")
        key = key.strip()
        value = value.split("#")[0].strip()

        # nested block (e.g. verification:)
        if indent >= 2 and current_map_key:
            data[current_map_key][key] = _coerce(value)
            continue

        current_map_key = None
        current_list_key = None

        if value == "":
            # could be a block list or a nested map; decide on the next line
            data[key] = None
            current_list_key = key
            current_map_key = key
            data[key] = {} if key == "verification" else None
            if key != "verification":
                data[key] = []
            continue

        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [
                v.strip().strip("\"'") for v in inner.split(",") if v.strip()
            ] if inner else []
            continue

        data[key] = _coerce(value)

    # a key we optimistically made a list but that stayed empty is fine
    return data


def _coerce(value):
    value = value.strip().strip("\"'")
    if value in ("null", "~", ""):
        return None
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def parse_date(value):
    if not isinstance(value, str):
        return None
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        return None


# ---------------------------------------------------------------- checks

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    today = datetime.date.today()

    pages = {}          # id -> (relpath, data)
    ids_by_type = {}    # type -> set of ids

    # ---- load
    for folder, expected_type in ENTITY_FOLDERS.items():
        d = root / folder
        if not d.is_dir():
            warn(folder, "folder does not exist")
            continue
        for path in sorted(d.glob("*.md")):
            rel = f"{folder}/{path.name}"
            data = parse_frontmatter(path.read_text(encoding="utf-8"))
            if data is None:
                err(rel, "missing or malformed frontmatter")
                continue

            pid = data.get("id")
            if not pid:
                err(rel, "missing required field 'id'")
                continue
            if pid in pages:
                err(rel, f"duplicate id '{pid}' (also in {pages[pid][0]})")
                continue

            if data.get("type") != expected_type:
                err(rel, f"type '{data.get('type')}' does not match folder "
                         f"(expected '{expected_type}')")

            pages[pid] = (rel, data)
            ids_by_type.setdefault(data.get("type"), set()).add(pid)

    if not pages:
        # A freshly scaffolded repo has no pages yet. That is a valid state,
        # not an error, so CI passes on the first push.
        print("No pages found. Empty scaffold is valid; nothing to validate.")
        report()
        return

    # ---- per page
    for pid, (rel, data) in pages.items():
        ptype = data.get("type")

        for field in UNIVERSAL_FIELDS:
            if data.get(field) in (None, "", []):
                err(rel, f"missing required field '{field}'")

        for field in TYPE_FIELDS.get(ptype, []):
            if data.get(field) in (None, "", []):
                err(rel, f"missing required field '{field}' for type '{ptype}'")

        status = data.get("status")
        if status and status not in VALID_STATUS:
            err(rel, f"invalid status '{status}'")

        level = data.get("level")
        if level and level not in VALID_LEVEL:
            err(rel, f"invalid level '{level}'")

        # dates
        for date_field in ("created", "last_reviewed"):
            if data.get(date_field) and not parse_date(data[date_field]):
                err(rel, f"'{date_field}' is not a valid YYYY-MM-DD date")

        # staleness is computed, never asserted
        reviewed = parse_date(data.get("last_reviewed"))
        cycle = data.get("review_cycle_days")
        if reviewed and isinstance(cycle, int):
            age = (today - reviewed).days
            if age > cycle:
                warn(rel, f"STALE: reviewed {age}d ago, cycle is {cycle}d")
        if isinstance(cycle, int) and ptype in DEFAULT_REVIEW_CYCLE:
            if cycle > DEFAULT_REVIEW_CYCLE[ptype]:
                warn(rel, f"review_cycle_days {cycle} exceeds suggested "
                          f"{DEFAULT_REVIEW_CYCLE[ptype]} for {ptype}")

        # deprecation hygiene
        if status == "deprecated" and not data.get("superseded_by"):
            err(rel, "status is deprecated but 'superseded_by' is empty")

        # verification block (procedures)
        if ptype == "procedure":
            v = data.get("verification")
            if not isinstance(v, dict) or not v:
                err(rel, "missing or malformed 'verification' block")
            else:
                method = v.get("method")
                conf = v.get("confidence")
                if method not in VALID_METHOD:
                    err(rel, f"verification.method '{method}' is invalid")
                if conf not in VALID_CONFIDENCE:
                    err(rel, f"verification.confidence '{conf}' is invalid")
                if not parse_date(v.get("verified_on")):
                    err(rel, "verification.verified_on is not a valid date")
                if method in MAX_CONFIDENCE and conf in CONFIDENCE_RANK:
                    cap = MAX_CONFIDENCE[method]
                    if CONFIDENCE_RANK[conf] > CONFIDENCE_RANK[cap]:
                        err(rel, f"confidence '{conf}' too high for method "
                                 f"'{method}' (max '{cap}')")
                # an agent must never claim human execution
                if method == "human-executed" and v.get("verified_by") in (
                    "claude", "script", "agent", "cline"
                ):
                    err(rel, "verification.method 'human-executed' claimed by a "
                             "non-human verified_by. only a person may set this.")
                if method == "automated":
                    ta = v.get("test_artifact")
                    if not ta:
                        err(rel, "method 'automated' requires a test_artifact")
                    elif not (root / ta).exists():
                        err(rel, f"test_artifact '{ta}' does not exist")

        # referential integrity
        for field in REF_FIELDS_SINGLE:
            ref = data.get(field)
            if ref and ref not in pages:
                err(rel, f"'{field}' points at unknown id '{ref}'")

        for field in REF_FIELDS_LIST:
            refs = data.get(field)
            if not isinstance(refs, list):
                continue
            for ref in refs:
                if ref not in pages:
                    err(rel, f"'{field}' contains unknown id '{ref}'")

        # paths must not reference non-active pages
        if ptype == "path":
            for ref in data.get("sequence") or []:
                if ref in pages and pages[ref][1].get("status") != "active":
                    err(rel, f"sequence references '{ref}' with status "
                             f"'{pages[ref][1].get('status')}' (must be active)")

    # ---- cycles in prerequisites
    for pid in list(pages):
        seen = set()
        stack = [(pid, [pid])]
        while stack:
            node, trail = stack.pop()
            for nxt in pages.get(node, (None, {}))[1].get("prerequisites") or []:
                if nxt == pid:
                    err(pages[pid][0], "circular prerequisite chain: "
                                       + " -> ".join(trail + [nxt]))
                    stack = []
                    break
                if nxt in pages and nxt not in seen:
                    seen.add(nxt)
                    stack.append((nxt, trail + [nxt]))

    # ---- orphans worth knowing about
    for pid, (rel, data) in pages.items():
        if data.get("type") != "concept":
            continue
        referenced = any(
            pid in (other[1].get("requires_concepts") or [])
            or pid in (other[1].get("sequence") or [])
            for other in pages.values()
        )
        if not referenced:
            warn(rel, "concept is not referenced by any page")

    report()


def report():
    for w in warnings:
        print(w)
    for e in errors:
        print(e)
    print()
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
