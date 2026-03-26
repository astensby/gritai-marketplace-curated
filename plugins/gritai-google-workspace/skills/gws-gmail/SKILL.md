---
name: gws-gmail
description: "Gmail via gws CLI — send, read, triage, reply, forward, watch, search, draft, label, and manage email. Use when the user wants to work with email, send messages, check inbox, reply to threads, or manage labels."
allowed-tools: Bash, Read
---

# Gmail (gws CLI)

> **PREREQUISITE:** The `gws` CLI must be installed and authenticated. If not, load the `gws-setup` skill.

## Quick Reference

| Action | Command |
|---|---|
| Send email | `gws gmail +send --to alice@example.com --subject 'Hi' --body 'Hello!'` |
| Triage inbox | `gws gmail +triage --max 10` |
| Reply | `gws gmail +reply --message-id MSG_ID --body 'Thanks!'` |
| Reply all | `gws gmail +reply-all --message-id MSG_ID --body 'Noted.'` |
| Forward | `gws gmail +forward --message-id MSG_ID --to bob@example.com` |
| Watch for new mail | `gws gmail +watch` |

## Common Operations

### List messages

```bash
gws gmail users messages list --params '{"userId": "me", "maxResults": 10}'
```

### Search with Gmail query syntax

```bash
gws gmail users messages list --params '{"userId": "me", "q": "from:boss@company.com is:unread"}'
```

### Read a message

```bash
gws gmail users messages get --params '{"userId": "me", "id": "MESSAGE_ID"}'
```

### Send email (with HTML)

```bash
gws gmail +send --to alice@example.com --subject 'Report' --body '<h1>Q1 Report</h1><p>See attached.</p>' --html
```

### Send with CC/BCC

```bash
gws gmail +send --to alice@example.com --cc bob@example.com --bcc admin@example.com --subject 'Update' --body 'FYI'
```

### Create a draft

```bash
gws gmail users drafts create --params '{"userId": "me"}' --json '{
  "message": {
    "raw": "BASE64_ENCODED_RFC2822"
  }
}'
```

### Manage labels

```bash
# List labels
gws gmail users labels list --params '{"userId": "me"}'

# Create label
gws gmail users labels create --params '{"userId": "me"}' --json '{"name": "Important/Projects"}'

# Apply label to message
gws gmail users messages modify --params '{"userId": "me", "id": "MSG_ID"}' --json '{"addLabelIds": ["LABEL_ID"]}'
```

### Search operators

| Operator | Example |
|---|---|
| `from:` | `from:alice@example.com` |
| `to:` | `to:me` |
| `subject:` | `subject:meeting` |
| `has:attachment` | Messages with attachments |
| `is:unread` | Unread messages |
| `after:` / `before:` | `after:2026/03/01 before:2026/03/13` |
| `label:` | `label:important` |
| `in:sent` | Sent messages |

## Safety

- **Always confirm** before sending, replying, or modifying messages
- Use `--dry-run` to preview send commands
- Never expose email content without user consent

## Schema Introspection

```bash
gws schema gmail.users.messages.send
gws schema gmail.users.messages.list
```
