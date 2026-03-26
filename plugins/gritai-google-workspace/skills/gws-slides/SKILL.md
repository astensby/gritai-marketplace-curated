---
name: gws-slides
description: "Google Slides via gws CLI — create presentations, add slides, read content. Use when the user wants to create or read Google Slides presentations, build a pitch deck, make a slide deck, prepare presentation slides, or extract content from an existing presentation."
allowed-tools: Bash, Read
---

# Google Slides (gws CLI)

> **PREREQUISITE:** The `gws` CLI must be installed and authenticated. If not, load the `gws-setup` skill.

## Common Operations

### Create a presentation

```bash
gws slides presentations create --json '{"title": "Q1 Review"}'
```

### Get presentation content

```bash
gws slides presentations get --params '{"presentationId": "PRES_ID"}'
```

### Add a slide

```bash
gws slides presentations batchUpdate --params '{"presentationId": "PRES_ID"}' --json '{
  "requests": [
    {"createSlide": {"slideLayoutReference": {"predefinedLayout": "TITLE_AND_BODY"}}}
  ]
}'
```

### Insert text into a slide

```bash
gws slides presentations batchUpdate --params '{"presentationId": "PRES_ID"}' --json '{
  "requests": [
    {"insertText": {"objectId": "SHAPE_ID", "text": "Slide content here"}}
  ]
}'
```

## Safety

- **Always confirm** before creating or modifying presentations
