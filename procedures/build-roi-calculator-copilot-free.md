---
id: build-roi-calculator-copilot-free
title: Build a single-file ROI calculator with free Copilot
type: procedure
status: active
owner: songws1
created: 2026-09-07
last_reviewed: null
review_cycle_days: 90
level: intermediate
tool: copilot-free
implements: generated-single-file-tool
audience: [ops-analyst]
requires_concepts: [single-file-web-app, system-prompt]
prerequisites: []
est_time_minutes: 45
superseded_by:
verification:
  method: script-verified
  reviewed: llm-reviewed
  verified_on: 2026-09-07
  verified_by: claude
  test_artifact: tests/build-roi-calculator-copilot-free.md
  confidence: high
tags: []
---

## Why this exists

The free tier includes no way to build or host an application — [[copilot-free]] limitation 1, a web-based general assistant with no development or deployment surface — so [[generated-single-file-tool]] is the only route by which a non-developer can end up with a working tool. This procedure is the batch's execution-verification pilot: its output is an inspectable file, so its artifact can be genuinely tested without a live account.

## Prerequisites

- A browser with access to free Copilot, signed in or not (capabilities vary by account and region — see [[copilot-free]]).
- A local folder where you are allowed to save files.
- A plain-text editor (Notepad is sufficient).

## Steps

1. Open copilot.microsoft.com and start a new chat.
2. Paste the prompt block below into the chat.
3. Send it.

```text
Create a single self-contained HTML file that works when saved locally and opened by double-click, with no internet connection.

Requirements:
- One file only. All CSS and JavaScript inline. No external links, no CDN scripts, no network requests.
- Inputs: one-time implementation cost; hours saved per year; hourly labor rate; recurring annual software cost.
- A button labelled Calculate. When clicked, compute and display: annual net benefit, payback period in months, year-one return on investment as a percentage.
- Formulas: annual net benefit = (hours saved per year × hourly rate) − recurring annual cost. Payback months = one-time cost ÷ (annual net benefit ÷ 12). Year-one ROI = (annual net benefit − one-time cost) ÷ one-time cost × 100.
- If annual net benefit is zero or negative, display a plain-language message instead of a number.
- Give these exact element ids: one-time-cost, hours-saved, hourly-rate, recurring-cost, annual-benefit, payback, roi. Put the calculation in a global function named calculate.
- Currency as dollars with thousands separators; payback to one decimal place.
```

4. Wait until the model returns the whole file in one code block. If it stops mid-file, reply "continue from where you stopped" until the closing html tag appears.
5. Copy the entire code block contents.
6. Paste into the text editor and save as roi-calculator.html (UTF-8).
7. Open the saved file in the browser (double-click it, or use Open With).
8. Enter this known case and click Calculate: one-time cost 6000; hours saved 300; hourly rate 50; recurring cost 3000.
9. Read the three outputs and compare them to the expected values in the next section.

## How to verify it worked

For the known case in step 7 the calculator must show exactly: annual net benefit 12,000.00 dollars; payback 6.0 months; year-one ROI 100 percent. Any other value means the model altered a formula — regenerate.

A repeatable automated version of this check exists: tests/build-roi-calculator-copilot-free.md drives the reference artifact tests/build-roi-calculator-copilot-free.html (authored to the same spec the prompt above gives the model) through the known case in a headless browser, and it passed on 2026-09-07. Scope of that result: the artifact specification is correct and testable; whether a live free-Copilot session emits an artifact meeting the spec is verified the first time a person runs this procedure end to end.

## Known failure modes

- **External links or CDN scripts appear** → the file will not work offline. Reply: "Regenerate with no external references at all." Re-check by searching the file text for http.
- **File arrives truncated** → ask the model to continue from the exact cut point; assemble only when the closing html tag is present.
- **Numbers differ from the known case** → the model reworded the formulas. Regenerate quoting the formulas line verbatim.
- **Element ids differ from the requested ones** → the automated harness (and any scripted check) cannot attach to the page. Ask for the exact ids again.
- **The browser refuses to open the saved file** → use right-click, Open With, and pick the browser explicitly; this is a local-file association issue, not a defect in the artifact.

## Sources

- raw/copilot-free-vs-m365.md — free tier scope; no hosting or app platform
- raw/copilot-app-changes.md — free usage subject to capacity and limits
- raw/mdn-local-html-files.md — what an .html file is; opening a saved file in a browser
- raw/copilot-prompt-order.md — request structure; verification-relevant ordering
