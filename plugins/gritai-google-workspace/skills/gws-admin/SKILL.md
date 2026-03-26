---
name: gws-admin
description: "Google Workspace Admin via gws CLI — audit logs, usage reports, security monitoring. Use when the user wants admin reports, audit trails, or usage statistics for their Workspace domain."
allowed-tools: Bash, Read
---

# Google Workspace Admin Reports (gws CLI)

> **PREREQUISITE:** The `gws` CLI must be installed and authenticated. If not, load the `gws-setup` skill. Requires admin privileges.

## Common Operations

### Get login activity

```bash
gws admin-reports activities list --params '{"userKey": "all", "applicationName": "login"}'
```

### Get admin activity

```bash
gws admin-reports activities list --params '{"userKey": "all", "applicationName": "admin"}'
```

### Get Drive activity

```bash
gws admin-reports activities list --params '{"userKey": "all", "applicationName": "drive"}'
```

### Usage reports

```bash
gws admin-reports userUsageReport get --params '{"userKey": "all", "date": "2026-03-12"}'
```

## Safety

- These commands are read-only audit/reporting tools
- Admin privileges are required — commands will fail for non-admin accounts
