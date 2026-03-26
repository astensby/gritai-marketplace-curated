---
name: gws-tasks
description: "Google Tasks via gws CLI — create, list, complete, and manage task lists and tasks. Use when the user wants to manage their to-do lists, create tasks, mark tasks complete, or review overdue items."
allowed-tools: Bash, Read
---

# Google Tasks (gws CLI)

> **PREREQUISITE:** The `gws` CLI must be installed and authenticated. If not, load the `gws-setup` skill.

## Common Operations

### List task lists

```bash
gws tasks tasklists list
```

### List tasks in a list

```bash
gws tasks tasks list --params '{"tasklist": "TASKLIST_ID"}'
```

### Create a task

```bash
gws tasks tasks insert --params '{"tasklist": "TASKLIST_ID"}' --json '{
  "title": "Review pull request",
  "notes": "PR #42 — needs security review",
  "due": "2026-03-14T00:00:00Z"
}'
```

### Complete a task

```bash
gws tasks tasks patch --params '{"tasklist": "TASKLIST_ID", "task": "TASK_ID"}' \
  --json '{"status": "completed"}'
```

### Create a new task list

```bash
gws tasks tasklists insert --json '{"title": "Sprint 12"}'
```

### Review overdue tasks

```bash
gws tasks tasks list --params '{"tasklist": "TASKLIST_ID", "dueMax": "2026-03-13T23:59:59Z", "showCompleted": false}'
```

## Safety

- **Always confirm** before creating, completing, or deleting tasks
