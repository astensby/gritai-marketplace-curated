---
name: gws-drive
description: "Google Drive via gws CLI — list, search, upload, download, share, organize files and folders, manage permissions. Use when the user wants to work with Google Drive files, upload/download documents, share files, or organize folders."
---

# Google Drive (gws CLI)

> **PREREQUISITE:** The `gws` CLI must be installed and authenticated. If not, load the `gws-setup` skill.

## Quick Reference

| Action | Command |
|---|---|
| List recent files | `gws drive files list --params '{"pageSize": 10}'` |
| Upload file | `gws drive +upload ./report.pdf` |
| Search files | `gws drive files list --params '{"q": "name contains '\''report'\''"}'` |

## Common Operations

### List files

```bash
gws drive files list --params '{"pageSize": 10}'
gws drive files list --params '{"pageSize": 10}' --format table
```

### Search files

```bash
# By name
gws drive files list --params '{"q": "name contains '\''budget'\''"}'

# By type
gws drive files list --params '{"q": "mimeType = '\''application/vnd.google-apps.spreadsheet'\''"}'

# In a specific folder
gws drive files list --params '{"q": "'\''FOLDER_ID'\'' in parents"}'

# Modified recently
gws drive files list --params '{"q": "modifiedTime > '\''2026-03-01T00:00:00'\''"}'
```

### Upload a file

```bash
gws drive +upload ./report.pdf
gws drive files create --json '{"name": "report.pdf"}' --upload ./report.pdf
```

### Download a file

```bash
gws drive files get --params '{"fileId": "FILE_ID", "alt": "media"}' -o ./downloaded-file.pdf
```

### Export Google Doc as PDF

```bash
gws drive files export --params '{"fileId": "FILE_ID", "mimeType": "application/pdf"}' -o ./document.pdf
```

### Create a folder

```bash
gws drive files create --json '{"name": "Project Docs", "mimeType": "application/vnd.google-apps.folder"}'
```

### Move file to folder

```bash
gws drive files update --params '{"fileId": "FILE_ID", "addParents": "FOLDER_ID", "removeParents": "OLD_PARENT_ID"}'
```

### Share a file

```bash
# Share with specific user
gws drive permissions create --params '{"fileId": "FILE_ID"}' \
  --json '{"type": "user", "role": "writer", "emailAddress": "alice@example.com"}'

# Share with anyone (link sharing)
gws drive permissions create --params '{"fileId": "FILE_ID"}' \
  --json '{"type": "anyone", "role": "reader"}'
```

### List permissions

```bash
gws drive permissions list --params '{"fileId": "FILE_ID"}'
```

### Find large files (storage audit)

```bash
gws drive files list --params '{"q": "mimeType != '\''application/vnd.google-apps.folder'\''", "orderBy": "quotaBytesUsed desc", "pageSize": 20, "fields": "files(name,size,quotaBytesUsed)"}'
```

### Paginate through all files

```bash
gws drive files list --params '{"pageSize": 100}' --page-all | jq -r '.files[].name'
```

## Drive MIME Types

| Type | MIME |
|---|---|
| Google Doc | `application/vnd.google-apps.document` |
| Google Sheet | `application/vnd.google-apps.spreadsheet` |
| Google Slides | `application/vnd.google-apps.presentation` |
| Folder | `application/vnd.google-apps.folder` |

## Safety

- **Always confirm** before deleting files, changing permissions, or moving files
- Use `--dry-run` to preview write operations
