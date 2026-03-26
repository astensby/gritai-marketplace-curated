---
name: gws-people
description: "Google People/Contacts via gws CLI — look up contacts, search directory, sync contacts. Use when the user wants to look up contact information, search the company directory, or manage contacts."
allowed-tools: Bash, Read
---

# Google People / Contacts (gws CLI)

> **PREREQUISITE:** The `gws` CLI must be installed and authenticated. If not, load the `gws-setup` skill.

## Common Operations

### Search contacts

```bash
gws people people searchContacts --params '{"query": "Alice", "readMask": "names,emailAddresses,phoneNumbers"}'
```

### List connections (all contacts)

```bash
gws people people connections list --params '{"resourceName": "people/me", "personFields": "names,emailAddresses"}'
```

### Get a specific contact

```bash
gws people people get --params '{"resourceName": "people/PERSON_ID", "personFields": "names,emailAddresses,phoneNumbers,organizations"}'
```

### Search directory (Workspace)

```bash
gws people people searchDirectoryPeople --params '{"query": "engineering", "readMask": "names,emailAddresses", "sources": ["DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE"]}'
```

## Schema Introspection

```bash
gws people --help
gws schema people.people.searchContacts
```
