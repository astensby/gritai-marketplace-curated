---
name: gws-setup
description: "Install and authenticate the gws CLI for Google Workspace access. Use when the user needs to set up Google Workspace, encounters auth errors, or when gws is not installed."
allowed-tools: Bash, Read
---

# Google Workspace Setup (gws CLI)

This skill configures the `gws` CLI — a single command-line tool for all Google Workspace APIs.

## Prerequisites

- **Node.js 18+** (for npm install)
- **A Google account** with Workspace access

## Installation

Check if gws is available:

```bash
gws --version
```

If not installed:

```bash
npm install -g @googleworkspace/cli
```

## Authentication

### Step 1: Create a Google Cloud project (one-time)

If you have `gcloud` installed and authenticated:

```bash
gcloud projects create my-workspace-cli --name="Workspace CLI"
gcloud config set project my-workspace-cli
```

Otherwise, create one at https://console.cloud.google.com/projectcreate

### Step 2: Enable Workspace APIs

With gcloud:

```bash
gcloud services enable \
  gmail.googleapis.com \
  drive.googleapis.com \
  sheets.googleapis.com \
  calendar-json.googleapis.com \
  docs.googleapis.com \
  slides.googleapis.com \
  chat.googleapis.com \
  tasks.googleapis.com \
  people.googleapis.com \
  forms.googleapis.com \
  meet.googleapis.com \
  --project=my-workspace-cli
```

Or enable them in the Cloud Console under APIs & Services → Library.

### Step 3: Set up OAuth consent screen

Open: `https://console.cloud.google.com/apis/credentials/consent?project=my-workspace-cli`

1. User Type: **External** → Create
2. App name: `gws CLI`, support email: your email
3. Click **Save and Continue** through all screens
4. Under **Test users** → **Add users** → add your Google account email

> **Multi-account tip:** If the Cloud Console opens with the wrong Google account, replace `/u/0/` with `/u/1/` in the URL to switch accounts.

### Step 4: Create OAuth client credentials

Open: `https://console.cloud.google.com/apis/credentials?project=my-workspace-cli`

1. Click **Create Credentials** → **OAuth client ID**
2. Application type: **Desktop app**
3. Name: `gws CLI`
4. Click **Create**
5. **Download the JSON file** and save it to: `~/.config/gws/client_secret.json`

```bash
mkdir -p ~/.config/gws
mv ~/Downloads/client_secret_*.json ~/.config/gws/client_secret.json
```

### Step 5: Login

```bash
gws auth login -s drive,gmail,sheets,calendar,docs,tasks
```

This opens your browser for OAuth consent. Select your Google account and approve the scopes.

> **Important:** For unverified apps (testing mode), Google limits consent to ~25 scopes. Use `-s service1,service2` to select only the services you need instead of requesting all scopes.

### Step 6: Verify

```bash
gws gmail users getProfile --params '{"userId": "me"}'
```

You should see your email address and message count in the JSON response.

### Security model

All credentials stay on your machine:
- **Client secret**: `~/.config/gws/client_secret.json` (your own GCP OAuth client)
- **Encrypted tokens**: `~/.config/gws/credentials.enc` (AES-256-GCM, key in OS keyring)
- **No secrets in this plugin** — skills are pure markdown documentation

## Shared Conventions

### Global flags

| Flag | Description |
|---|---|
| `--format <FORMAT>` | Output format: `json` (default), `table`, `yaml`, `csv` |
| `--dry-run` | Validate locally without calling the API |
| `--sanitize <TEMPLATE>` | Screen responses through Model Armor |
| `-o, --output <PATH>` | Save binary responses to file (e.g., Drive downloads) |

### Output format
All `gws` commands return structured JSON by default. Use `--format table` for human-readable output.

### Safety rules
- **Always confirm** with the user before executing write/delete commands
- Use `--dry-run` to preview destructive operations
- Never output secrets, API keys, or tokens

### Schema introspection
Before calling any unfamiliar API method:

```bash
gws schema <service>.<resource>.<method>
```

### Pagination
For large result sets:

```bash
gws <command> --page-all                    # Auto-paginate (NDJSON output)
gws <command> --page-all --page-limit 5     # Limit pages
gws <command> --page-all --page-delay 200   # Delay between pages (ms)
```

### Shell escaping
Sheets ranges use `!` which zsh interprets as history expansion. Use double quotes for ranges containing `!`:

```bash
gws sheets +read --spreadsheet ID --range "Sheet1!A1:D10"
```

### Discovering uncovered services
This plugin ships curated skills for the most common services. For services without a dedicated skill (Keep, Classroom, Events, ModelArmor), use raw `gws` commands:

```bash
gws keep --help
gws schema keep.notes.list
gws generate-skills    # Generate upstream SKILL.md files for all services
```

## Troubleshooting

| Issue | Fix |
|---|---|
| `gws: command not found` | Run `npm install -g @googleworkspace/cli` |
| `No OAuth client configured` | Download client_secret JSON from Cloud Console and save to `~/.config/gws/client_secret.json` |
| `Access blocked: Authorization Error` | Add yourself as a **test user** in the OAuth consent screen, and make sure you're signing in with the correct Google account |
| Wrong Google account selected | Use the `prompt=select_account` URL or open an incognito window with only the correct account logged in |
| Cloud Console opens wrong account | Replace `/u/0/` with `/u/1/` (or `/u/2/`) in the console URL |
| Scope limit errors (>25 scopes) | Use `-s service1,service2` instead of the `recommended` preset |
| Token expired | Run `gws auth login` to re-authenticate |
| `gcloud auth` expired | Run `gcloud auth login` before retrying `gws auth setup` |

## Reference

- Repository: https://github.com/googleworkspace/cli
- Full skills index: https://github.com/googleworkspace/cli/blob/main/docs/skills.md
