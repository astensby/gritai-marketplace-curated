---
name: gws-workflow-meeting-prep
description: "Meeting preparation — shows next meeting's agenda, attendees, description, and linked documents. Use when the user asks to prepare for a meeting, wants meeting context, or asks 'what's my next meeting about?'"
allowed-tools: Bash, Read
---

# Meeting Preparation (gws CLI)

> **PREREQUISITE:** The `gws` CLI must be installed and authenticated. If not, load the `gws-setup` skill.

## Quick Command

```bash
gws workflow +meeting-prep
```

This gathers:
1. Next upcoming meeting details (title, time, attendees)
2. Meeting description/agenda
3. Any linked Google Docs, Sheets, or Slides

## Manual Alternative

```bash
# 1. Get next event
gws calendar +agenda

# 2. Get full event details (with attendees, description, attachments)
gws calendar events get --params '{"calendarId": "primary", "eventId": "EVENT_ID"}'

# 3. If there are linked documents, fetch their metadata
gws drive files get --params '{"fileId": "DOC_ID"}'
```

## Safety

- This is **read-only** — no confirmation needed
