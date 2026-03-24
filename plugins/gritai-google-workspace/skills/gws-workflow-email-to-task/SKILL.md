---
name: gws-workflow-email-to-task
description: "Convert a Gmail message into a Google Tasks entry — extracts subject and key details. Use when the user wants to turn an email into a task, add an email to their to-do list, or track email follow-ups."
---

# Email to Task (gws CLI)

> **PREREQUISITE:** The `gws` CLI must be installed and authenticated. If not, load the `gws-setup` skill.

## Quick Command

```bash
gws workflow +email-to-task --message-id MESSAGE_ID
```

## Manual Workflow

```bash
# 1. Read the email
gws gmail users messages get --params '{"userId": "me", "id": "MESSAGE_ID"}'

# 2. Extract subject and sender from the response

# 3. Create a task with the email context
gws tasks tasks insert --params '{"tasklist": "@default"}' --json '{
  "title": "Follow up: [EMAIL_SUBJECT]",
  "notes": "From: [SENDER]\nDate: [DATE]\n\n[KEY_DETAILS]",
  "due": "2026-03-14T00:00:00Z"
}'
```

## Safety

- **Confirm** before creating the task (write operation)
- The email read step is read-only
