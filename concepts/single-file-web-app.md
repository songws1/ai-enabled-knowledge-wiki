---
id: single-file-web-app
title: Single-file web app (self-contained HTML)
type: concept
status: active
owner: songws1
created: 2026-09-07
last_reviewed: null
review_cycle_days: 365
level: basic
related_tools: [copilot-free]
see_also: []
tags: []
---

## In short

A self-contained HTML file carries its markup, its styling, and its behavior inside one plain-text file, so the page runs when the file is opened in a browser — no server, no install, and no internet connection required.

## How it works

An `.html` file is plain text containing HTML code, which the browser renders as a page. Styling (CSS) and behavior (JavaScript) can be written inline in that same file. If the file references nothing external — no CDN scripts, no linked assets, no network calls — then everything the page does is decided by its own contents, and opening it from a local disk behaves the same as loading a web page. MDN describes opening a saved HTML file by loading it in the browser from the file system (via Open With, or by dragging the file onto a browser window).

Two consequences follow:

- **Distribution is file distribution.** The tool travels as an attachment or a file-share copy, exactly like a spreadsheet. Whoever receives it can open it with the browser they already have.
- **Nothing persists.** State lives only in the page while it is open. A page that needs to remember anything across sessions must save files explicitly; otherwise it starts fresh every time.

Whether a web server is needed to *view* a local HTML file: the captured MDN page does not state this outright (see the recorded absence in raw/mdn-local-html-files.md). It is nonetheless directly observable — a saved file opens and runs with no server process — and the procedure build-roi-calculator-copilot-free tests exactly that.

## Why it matters here

For someone who cannot deploy anything — no server, no admin rights, no budget — a single file is the one software artifact they can still receive, run, and pass on. This is the concept behind the pattern [[generated-single-file-tool]]: an AI chat tool can emit such a file, and the user's only remaining job is to save it and open it.

## Sources

- raw/mdn-local-html-files.md — what an .html file is; opening a saved file in a browser; recorded absence about servers
