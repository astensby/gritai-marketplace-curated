---
name: gws-sheets
description: "Google Sheets via gws CLI — read, write, append, create spreadsheets, manage tabs and formatting. Use when the user wants to work with spreadsheets, read/write cell data, create trackers, or analyze tabular data in Google Sheets."
allowed-tools: Bash, Read
---

# Google Sheets (gws CLI)

> **PREREQUISITE:** The `gws` CLI must be installed and authenticated. If not, load the `gws-setup` skill.

## Quick Reference

| Action | Command |
|---|---|
| Read cells | `gws sheets +read --spreadsheet ID --range "Sheet1!A1:D10"` |
| Append row | `gws sheets +append --spreadsheet ID --range "Sheet1!A1" --values '["Alice", 95]'` |
| Create sheet | `gws sheets spreadsheets create --json '{"properties": {"title": "Q1 Budget"}}'` |

## Common Operations

### Read values

```bash
gws sheets +read --spreadsheet SPREADSHEET_ID --range "Sheet1!A1:D10"
```

### Append a row

```bash
gws sheets +append --spreadsheet SPREADSHEET_ID --range "Sheet1!A1" --values '["Name", "Score", "Date"]'
```

### Write values (overwrite)

```bash
gws sheets spreadsheets values update \
  --params '{"spreadsheetId": "ID", "range": "Sheet1!A1:C1", "valueInputOption": "USER_ENTERED"}' \
  --json '{"values": [["Name", "Score", "Grade"]]}'
```

### Batch update (multiple ranges)

```bash
gws sheets spreadsheets values batchUpdate \
  --params '{"spreadsheetId": "ID"}' \
  --json '{
    "valueInputOption": "USER_ENTERED",
    "data": [
      {"range": "Sheet1!A1", "values": [["Header1"]]},
      {"range": "Sheet1!B1", "values": [["Header2"]]}
    ]
  }'
```

### Create a new spreadsheet

```bash
gws sheets spreadsheets create --json '{"properties": {"title": "Expense Tracker"}}'
```

### Get spreadsheet metadata

```bash
gws sheets spreadsheets get --params '{"spreadsheetId": "ID"}'
```

## Shell Escaping

Sheets ranges use `!` which zsh interprets as history expansion. **Always use double quotes** for ranges:

```bash
# CORRECT (double quotes)
gws sheets +read --spreadsheet ID --range "Sheet1!A1:D10"

# WRONG (single quotes in zsh — ! may expand)
gws sheets +read --spreadsheet ID --range 'Sheet1!A1:D10'
```

## Safety

- **Always confirm** before writing or modifying spreadsheet data
- Use `--dry-run` to preview write operations
