---
name: gws-workflow-file-announce
description: "Announce a Drive file in a Google Chat space — shares the link with a message. Use when the user wants to share a document in Chat, announce a new file to a team, or notify a Chat space about a Drive file."
allowed-tools: Bash, Read
---

# File Announce (gws CLI)

> **PREREQUISITE:** The `gws` CLI must be installed and authenticated. If not, load the `gws-setup` skill.

## Quick Command

```bash
gws workflow +file-announce --file-id FILE_ID --space spaces/SPACE_ID --message 'New design doc ready for review'
```

## Manual Workflow

```bash
# 1. Get file metadata (name, webViewLink)
gws drive files get --params '{"fileId": "FILE_ID", "fields": "name,webViewLink"}'

# 2. Post in Chat
gws chat +send --space spaces/SPACE_ID --text 'New document shared: [FILE_NAME] - [LINK]'
```

## Safety

- **Confirm** before sending the Chat message (write operation)
