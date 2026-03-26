---
name: gws-chat
description: "Google Chat via gws CLI — send messages, manage spaces, list conversations. Use when the user wants to send messages in Google Chat spaces or manage Chat conversations."
allowed-tools: Bash, Read
---

# Google Chat (gws CLI)

> **PREREQUISITE:** The `gws` CLI must be installed and authenticated. If not, load the `gws-setup` skill.

## Quick Reference

| Action | Command |
|---|---|
| Send message | `gws chat +send --space spaces/SPACE_ID --text 'Hello team!'` |
| List spaces | `gws chat spaces list` |

## Common Operations

### Send a message

```bash
gws chat +send --space spaces/SPACE_ID --text 'Deploy complete. All systems green.'
```

### Send with raw API (for cards/formatting)

```bash
gws chat spaces messages create \
  --params '{"parent": "spaces/SPACE_ID"}' \
  --json '{"text": "Status update: *Build passed*"}'
```

### List spaces

```bash
gws chat spaces list
```

### List messages in a space

```bash
gws chat spaces messages list --params '{"parent": "spaces/SPACE_ID"}'
```

### Get a specific message

```bash
gws chat spaces messages get --params '{"name": "spaces/SPACE_ID/messages/MSG_ID"}'
```

## Safety

- **Always confirm** before sending messages
- Use `--dry-run` to preview messages
