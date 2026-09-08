---
id: 
title: 
type: procedure
status: draft
owner: 
created: 
last_reviewed: null
review_cycle_days: 90
level: 
tool: 
implements: 
audience: []
requires_concepts: []
prerequisites: []
est_time_minutes: 
superseded_by: 
verification:
  # method = how strongly the CLAIMS are backed. See SCHEMA 5.1.
  #   vendor-documented (max confidence: low)
  #   agent-executed    (max confidence: medium) - LLM ran the test, nondeterministic
  #   script-verified   (max confidence: high)   - deterministic test passed
  #   human-executed    (max confidence: high)   - PERSON ONLY, agents must never set
  method: vendor-documented
  # reviewed = whether the WRITING was checked. A different axis from method.
  #   none | llm-reviewed | human-reviewed (PERSON ONLY)
  reviewed: none
  verified_on: 
  verified_by: 
  test_artifact: null
  confidence: low
tags: []
---

## Why this exists

<!-- One or two sentences naming the constraint being worked around. Cite the
     specific limitation from the tool page. If you cannot name a constraint,
     this may not need to be a procedure. -->

## Prerequisites

<!-- What must be true before starting. -->

## Steps

<!-- Numbered, imperative, each independently verifiable. One action per step. -->

1. 

## How to verify it worked

<!-- REQUIRED. The observable success condition. A procedure whose success
     cannot be observed cannot be governed.

     ALSO REQUIRED when method is agent-executed or script-verified (SCHEMA 5.1):
     one sentence stating what the test does NOT cover. A test always proves
     something narrower than the procedure. Say where its edge is. -->

## Known failure modes

<!-- What commonly goes wrong, and what it means. -->

## Sources

<!-- Links to the raw/ captures this was derived from. -->
