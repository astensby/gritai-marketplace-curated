---
name: gws-meet
description: "Google Meet via gws CLI — create meeting spaces, check participant info. Use when the user wants to create a Meet link, set up a video call, generate a conference link, create a meeting room, or check meeting attendance and participants."
allowed-tools: Bash, Read
---

# Google Meet (gws CLI)

> **PREREQUISITE:** The `gws` CLI must be installed and authenticated. If not, load the `gws-setup` skill.

## Common Operations

### Create a meeting space

```bash
gws meet spaces create --json '{}'
```

### Get meeting space details

```bash
gws meet spaces get --params '{"name": "spaces/SPACE_ID"}'
```

### List conference records

```bash
gws meet conferenceRecords list
```

### List participants of a meeting

```bash
gws meet conferenceRecords participants list --params '{"parent": "conferenceRecords/RECORD_ID"}'
```

## Schema Introspection

```bash
gws meet --help
gws schema meet.spaces.create
```
