---
name: gws-workflow-weekly-digest
description: "Weekly summary — this week's meetings, unread email count, and open tasks. Use when the user asks for a weekly overview, end-of-week summary, or weekly planning context."
---

# Weekly Digest (gws CLI)

> **PREREQUISITE:** The `gws` CLI must be installed and authenticated. If not, load the `gws-setup` skill.

## Quick Command

```bash
gws workflow +weekly-digest
```

## Manual Workflow

```bash
# 1. This week's events
gws calendar +agenda --week

# 2. Unread email count
gws gmail users messages list --params '{"userId": "me", "q": "is:unread", "maxResults": 1}'
# Check resultSizeEstimate in the response for approximate unread count

# 3. Open tasks
gws tasks tasks list --params '{"tasklist": "@default", "showCompleted": false}'
```

## Safety

- This is **read-only** — no confirmation needed
