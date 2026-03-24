---
name: gws-workflow-standup
description: "Daily standup report — combines today's calendar events with open tasks into a concise summary. Use when the user asks for a standup update, daily briefing, or morning summary."
---

# Daily Standup Report (gws CLI)

> **PREREQUISITE:** The `gws` CLI must be installed and authenticated. If not, load the `gws-setup` skill.

## Quick Command

```bash
gws workflow +standup-report
gws workflow +standup-report --format table
```

This combines:
1. Today's calendar events (from all calendars)
2. Open Google Tasks

## Manual Alternative

If the workflow helper is unavailable, assemble manually:

```bash
# 1. Get today's events
gws calendar +agenda

# 2. Get open tasks
gws tasks tasklists list
# Then for each task list:
gws tasks tasks list --params '{"tasklist": "TASKLIST_ID", "showCompleted": false}'
```

## Output

The standup report includes:
- Meeting times, titles, and attendees for today
- Open tasks with due dates
- Summary suitable for sharing in Slack or Chat

## Safety

- This is **read-only** — no confirmation needed
