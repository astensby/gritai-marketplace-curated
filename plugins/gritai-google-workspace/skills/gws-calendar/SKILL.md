---
name: gws-calendar
description: "Google Calendar via gws CLI — view agenda, create/update/delete events, check availability, manage attendees. Use when the user wants to work with calendar events, schedule meetings, check free/busy, or manage their schedule."
allowed-tools: Bash, Read
---

# Google Calendar (gws CLI)

> **PREREQUISITE:** The `gws` CLI must be installed and authenticated. If not, load the `gws-setup` skill.

## Quick Reference

| Action | Command |
|---|---|
| View agenda | `gws calendar +agenda` |
| View week | `gws calendar +agenda --week` |
| Create event | `gws calendar +insert --summary 'Meeting' --start '2026-03-14T10:00:00' --end '2026-03-14T11:00:00'` |

## Common Operations

### View today's agenda

```bash
gws calendar +agenda
gws calendar +agenda --format table
```

### View this week

```bash
gws calendar +agenda --week
```

### Create an event

```bash
gws calendar +insert \
  --summary 'Team Standup' \
  --start '2026-03-14T09:00:00+01:00' \
  --end '2026-03-14T09:30:00+01:00' \
  --attendee alice@example.com \
  --attendee bob@example.com \
  --location 'Conference Room A' \
  --description 'Daily sync'
```

### List events in a time range

```bash
gws calendar events list --params '{
  "calendarId": "primary",
  "timeMin": "2026-03-13T00:00:00Z",
  "timeMax": "2026-03-20T00:00:00Z",
  "singleEvents": true,
  "orderBy": "startTime"
}'
```

### Update an event

```bash
gws calendar events patch --params '{"calendarId": "primary", "eventId": "EVENT_ID"}' \
  --json '{"summary": "Updated Title", "location": "Room B"}'
```

### Delete an event

```bash
gws calendar events delete --params '{"calendarId": "primary", "eventId": "EVENT_ID"}'
```

### Check free/busy

```bash
gws calendar freebusy query --json '{
  "timeMin": "2026-03-14T08:00:00Z",
  "timeMax": "2026-03-14T18:00:00Z",
  "items": [{"id": "primary"}, {"id": "colleague@example.com"}]
}'
```

### List calendars

```bash
gws calendar calendarList list
```

## Tips

- Use RFC 3339 timestamps with timezone offset (e.g., `2026-03-14T09:00:00+01:00`)
- The `+agenda` helper is read-only and safe to run without confirmation
- For recurring events, use the raw API: `gws calendar events insert --json '{"recurrence": ["RRULE:FREQ=WEEKLY"]}'`

## Safety

- **Always confirm** before creating, updating, or deleting events
- Use `--dry-run` to preview changes
