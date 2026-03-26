---
name: gws-forms
description: "Google Forms via gws CLI — create forms, read responses, manage questions. Use when the user wants to create surveys, feedback forms, or collect responses."
allowed-tools: Bash, Read
---

# Google Forms (gws CLI)

> **PREREQUISITE:** The `gws` CLI must be installed and authenticated. If not, load the `gws-setup` skill.

## Common Operations

### Create a form

```bash
gws forms forms create --json '{"info": {"title": "Team Feedback Q1"}}'
```

### Add questions

```bash
gws forms forms batchUpdate --params '{"formId": "FORM_ID"}' --json '{
  "requests": [
    {
      "createItem": {
        "item": {
          "title": "How would you rate this quarter?",
          "questionItem": {
            "question": {
              "choiceQuestion": {
                "type": "RADIO",
                "options": [
                  {"value": "Excellent"},
                  {"value": "Good"},
                  {"value": "Needs improvement"}
                ]
              }
            }
          }
        },
        "location": {"index": 0}
      }
    }
  ]
}'
```

### Get form details

```bash
gws forms forms get --params '{"formId": "FORM_ID"}'
```

### List responses

```bash
gws forms forms responses list --params '{"formId": "FORM_ID"}'
```

## Safety

- **Always confirm** before creating or modifying forms
