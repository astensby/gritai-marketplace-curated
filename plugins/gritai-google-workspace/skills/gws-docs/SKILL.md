---
name: gws-docs
description: "Google Docs via gws CLI — read, write, append text, create documents, apply formatting. Use when the user wants to create or edit Google Docs, write reports, or extract text from documents."
---

# Google Docs (gws CLI)

> **PREREQUISITE:** The `gws` CLI must be installed and authenticated. If not, load the `gws-setup` skill.

## Quick Reference

| Action | Command |
|---|---|
| Write to doc | `gws docs +write --title 'Meeting Notes' --body 'Content here'` |
| Read doc | `gws docs documents get --params '{"documentId": "DOC_ID"}'` |

## Common Operations

### Create a new document (with content)

```bash
gws docs +write --title 'Project Brief' --body '## Overview\n\nThis project aims to...'
```

### Read a document

```bash
gws docs documents get --params '{"documentId": "DOC_ID"}'
```

### Append text to existing document

```bash
gws docs documents batchUpdate --params '{"documentId": "DOC_ID"}' --json '{
  "requests": [
    {
      "insertText": {
        "location": {"index": 1},
        "text": "New paragraph added.\n"
      }
    }
  ]
}'
```

### Create from template (copy + edit)

```bash
# 1. Copy template
gws drive files copy --params '{"fileId": "TEMPLATE_ID"}' --json '{"name": "Invoice - March 2026"}'
# 2. Replace placeholders
gws docs documents batchUpdate --params '{"documentId": "NEW_DOC_ID"}' --json '{
  "requests": [
    {"replaceAllText": {"containsText": {"text": "{{CLIENT_NAME}}"}, "replaceText": "Acme Corp"}}
  ]
}'
```

## Safety

- **Always confirm** before creating or modifying documents
