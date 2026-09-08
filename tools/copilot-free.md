---
id: copilot-free
title: Microsoft Copilot (free consumer tier)
type: tool
status: active
owner: songws1
created: 2026-09-07
last_reviewed: null
review_cycle_days: 90
vendor: Microsoft
tier: free
access_notes: Anyone with a browser at copilot.microsoft.com; a free personal Microsoft account sign-in unlocks chat history and more image creation; feature set varies by region and account type
capabilities:
  - Chat with AI for help with writing, brainstorming, and summarizing
  - Real-time answers grounded in web search
  - Image creation, subject to capacity and limits
  - File upload in chat for free users, subject to capacity and limits
  - Copilot in Edge for webpage summarization and insights
limitations:
  - No integration into Word, Excel, PowerPoint, Outlook, or Teams; the free tier is a web-based general assistant
  - No reusable skill or project storage is documented for the free tier; anything meant to be reused must be stored outside the product as ordinary files
  - Without sign-in there is no chat history, shorter conversations, and limited image creation and voice
  - Free usage limits are capacity-based and not published as fixed numbers, and they change without notice
  - Feature availability varies by region and account type, and features are retired without local control (Podcasts, Deep Research, and Group chat were announced as retiring in the 2026-09-07 capture)
verified_on: 2026-09-07
tags: []
---

## What it is

Microsoft Copilot's free consumer tier is a web-based AI chat assistant, available at no cost in a browser, in desktop and mobile apps, and inside Edge. Microsoft frames it as "ideal for general questions and answers, people trying AI for the first time, and web-based tasks".

## Capabilities

Grounded in the captures listed under Sources, as of 2026-09-07:

- **Chat** for writing, brainstorming, summarizing, and general questions.
- **Web-grounded answers** — real-time answers based on web search.
- **Image creation** — free users can create images, subject to capacity and limits.
- **File upload in chat** — Microsoft states free users can "upload files and more for free, subject to available capacity and limits". Which file types are accepted in which build is not documented and varies; see apply-prompt-file-to-data-file for how this procedure handles the uncertainty.
- **Copilot in Edge** for webpage summarization and insights.

Signing in with a personal Microsoft account (free) "unlocks more, including your chat history, more image creation, longer conversations, extended voice sessions, and other features".

## Limitations

The most load-bearing part of this page. Each limitation below is written so a procedure can cite it as its reason for existing.

1. **No integration into desktop Office apps.** Deep integration with documents, email, spreadsheets, and calendars is listed only for Microsoft 365 subscribers. The free tier works in chat, on the web. *Affects:* everything on this tier happens through the chat surface.
2. **No documented reusable skill or project storage.** Vendor documentation for the free tier names no way to save a prompt, a skill, a project, or a reusable configuration inside the product. Anything that must be reused has to be stored outside the product, as an ordinary file in a folder the team controls. *Affects:* portable-prompt-template and every procedure implementing it.
3. **Sign-in gates persistence.** Without signing in there is no chat history, shorter conversations, and limited image creation and voice. Even signed in, the free tier documents no long-term storage of uploaded files as a retrievable library. *Affects:* nothing done in a free-tier chat should be treated as durable; save artifacts outside the product.
4. **Unpublished, capacity-based limits.** Free usage is "subject to available capacity and limits"; Microsoft does not publish free-tier quota numbers, and paid pages state that limits "may also change over time as new AI models become available". *Affects:* any procedure must degrade gracefully — capacity limits are handled by coming back later or falling back to paste, not by relying on a documented allowance.
5. **Regional and account-type variation, and silent feature changes.** "Copilot features, functionality, and availability may vary by region", and features are retired (Podcasts, Deep Research, Group chat announced as retiring in the capture). *Affects:* capability claims on this wiki are dated and re-verified each review cycle.

### Not verifiable from vendor documentation

The batch brief expected these limitations, but the captured vendor pages neither document nor explicitly deny them for the current free tier, so this page does not assert them as fact. Treat each as unknown, re-check against the live product, and lower confidence on any procedure that assumes it:

- Whether any form of persistent memory across sessions exists on the free tier.
- Whether free users can use or create custom GPTs / agents.
- Whether anything like saved projects or a file library exists.
- Whether uploaded files are retained at all beyond the conversation.

## Access notes

- Reachable signed-out, but signed-out sessions lose history and hit limits sooner.
- A personal Microsoft account is free; a work or school account routes to a different (organization-controlled) experience. The account type changes what you get.
- Feature set varies by region and by app build; what this page records is what Microsoft's own documentation stated on 2026-09-07.

## Sources

- raw/copilot-free-vs-m365.md — what free includes; what paid adds; regional variation
- raw/copilot-app-changes.md — free users' chat/images/file upload subject to capacity and limits; retiring features
- raw/copilot-app-what-is.md — sign-in effects; account types shape the experience
- raw/copilot-ai-credits-limits.md — paid-tier credit model; recorded absence of free-tier quotas
