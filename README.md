# GritAI Marketplace (Curated)

A curated collection of [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and Cowork plugins by GritAI — audio generation, design systems, Google Workspace integration, image generation, and Norwegian public data access.

## Plugins

| Plugin | What it does | Type | Requires |
|--------|-------------|------|----------|
| [gritai-audio](#gritai-audio) | Text-to-speech and audio with ElevenLabs | MCP Server | `ELEVENLABS_API_KEY` |
| [gritai-design](#gritai-design) | Design systems and themes for web UIs | Skills | Nothing |
| [gritai-google-workspace](#gritai-google-workspace) | Gmail, Calendar, Drive, Sheets, Docs, and more | Skills | `gws` CLI |
| [gritai-image-gen](#gritai-image-gen) | Image generation with Google Imagen 3 | MCP Server | `GEMINI_API_KEY` |
| [gritai-data-ssb](#gritai-data-ssb) | Statistics Norway open data (demographics, economy, labor, etc.) | Skills | Python 3 |
| [gritai-data-norges-bank](#gritai-data-norges-bank) | Norges Bank financial data (exchange rates, policy rates, bonds) | Skills | Python 3 |
| [gritai-data-brreg](#gritai-data-brreg) | Norwegian company data (search, lookup, board, financials) | Skills | Python 3 |

## Quick Start

### Install from GitHub (recommended)

No cloning required — add this repo as a marketplace directly in Claude Code:

```bash
# 1. Add the marketplace
/plugin marketplace add astensby/gritai-marketplace-curated

# 2. Install a plugin (example: image generation)
/plugin install gritai-image-gen@gritai-marketplace-curated --scope user

# 3. Enable it in your project
cd your-project
/plugin enable gritai-image-gen@gritai-marketplace-curated --scope project
```

You can also use the interactive UI by running `/plugin` and browsing the **Marketplaces** tab.

### Install from a local clone

```bash
# 1. Clone this repo
git clone https://github.com/astensby/gritai-marketplace-curated.git

# 2. Install a plugin (example: image generation)
claude plugin install gritai-image-gen@gritai-marketplace-curated --scope user

# 3. Enable it in your project
cd your-project
claude plugin enable gritai-image-gen@gritai-marketplace-curated --scope project
```

## Setup by Plugin

### gritai-audio

Generate speech, clone voices, and create audio content using [ElevenLabs](https://elevenlabs.io).

**Setup:**

1. Get an API key at [elevenlabs.io](https://elevenlabs.io)
2. Set the environment variable:
   ```bash
   export ELEVENLABS_API_KEY="your-key-here"
   ```
3. The plugin runs the ElevenLabs MCP server via `uvx elevenlabs-mcp` — make sure you have [uv](https://docs.astral.sh/uv/) installed.

---

### gritai-design

Curated design systems and visual themes for building polished web interfaces with Tailwind CSS.

**Available themes:**

- **Warm Terracotta Light** — premium editorial aesthetic with terracotta accents, paper backgrounds, and serif typography. Includes a complete Tailwind config and component patterns.

**Setup:** Nothing required — works out of the box. Just install and start building.

---

### gritai-google-workspace

Full Google Workspace integration powered by the [`gws` CLI](https://github.com/googleworkspace/cli). 18 skills covering 12 Google services plus 5 cross-service workflows.

| Service | Highlights |
|---------|-----------|
| Gmail | Send, triage, reply, forward, search, labels, watch |
| Calendar | Agenda, create/update events, free/busy |
| Drive | List, upload, download, share, organize |
| Sheets | Read, write, append, create |
| Docs | Read, write, create from template |
| Slides | Create, read presentations |
| Chat | Send messages, manage spaces |
| Tasks | Create, list, complete tasks |
| Forms | Create forms, read responses |
| Meet | Create meeting spaces |
| People | Contact lookup, directory search |
| Admin | Audit logs, usage reports |

**Workflows:** standup report, meeting prep, email-to-task, weekly digest, file announce.

**Setup:**

1. Install the CLI:
   ```bash
   npm install -g @googleworkspace/cli
   ```
2. Authenticate with your Google account:
   ```bash
   gws auth login -s drive,gmail,sheets,calendar,docs,tasks
   ```
3. That's it. No API keys needed in this plugin — the `gws` CLI handles OAuth on your machine. All credentials stay local, encrypted with your OS keyring.

For full setup details including GCP project creation and OAuth configuration, see the `gws-setup` skill included in the plugin.

---

### gritai-image-gen

Generate photorealistic images using Google's Imagen 3 model through the bundled Nano Banana MCP server.

**Features:** text-to-image, multiple aspect ratios (1:1, 16:9, 9:16, 4:3, 3:4), negative prompts, batch generation (up to 4 images).

**Setup:**

1. Get a Gemini API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Set the environment variable:
   ```bash
   export GEMINI_API_KEY="your-key-here"
   ```
3. The MCP server is pre-built and bundled — no build step needed.

**Rebuilding the server** (only if you modify the source):

```bash
npm install        # Install esbuild
npm run build      # Rebuild the server bundle
```

---

### gritai-data-ssb

Access Statistics Norway's open data API — ~3,900 statistical tables covering demographics, economy, health, education, labor, housing, prices, trade, and environment.

**Setup:** Requires Python 3 (uses only standard library). No API keys needed — all data is open.

**Usage:** The plugin provides a `ssb_fetch.py` CLI tool for searching tables, exploring metadata, and fetching data as CSV. Typical workflow: search -> metadata -> fetch -> analyze.

---

### gritai-data-norges-bank

Access Norges Bank's financial data API — exchange rates for 41 currencies, policy rates, NOWA overnight rates, government bond yields, and financial indicators.

**Setup:** Requires Python 3 (uses only standard library). No API keys needed — all data is open.

**Usage:** The plugin provides a `nb_fetch.py` CLI tool for listing datasets, exploring structure, and fetching time series as CSV.

---

### gritai-data-brreg

Search and analyze Norwegian companies via Brønnøysundregistrene — the Entity Registry (Enhetsregisteret) and Financial Statements Registry (Regnskapsregisteret).

**Setup:** Requires Python 3 (uses only standard library). No API keys needed — all data is open.

**Usage:** The plugin provides a `brreg_fetch.py` CLI tool for searching companies, looking up details, fetching board members/roles, and retrieving financial statements.

## Project Structure

```
gritai-marketplace-curated/
├── plugins/
│   ├── gritai-audio/            # ElevenLabs MCP server config
│   ├── gritai-design/           # Design system skills + Tailwind configs
│   ├── gritai-google-workspace/ # 18 Google Workspace skill files
│   ├── gritai-image-gen/        # Imagen 3 MCP server (source + bundle)
│   ├── gritai-data-ssb/             # Statistics Norway data skill
│   ├── gritai-data-norges-bank/     # Norges Bank financial data skill
│   └── gritai-data-brreg/           # Norwegian company data skill
├── scripts/
│   └── build-servers.mjs        # esbuild bundler for MCP servers
├── .claude-plugin/
│   └── marketplace.json         # Plugin registry
├── package.json
├── LICENSE                      # MIT
└── README.md
```

## Environment Variables

No secrets are stored in this repository. Plugins that need API keys read them from environment variables at runtime.

| Variable | Used by | Where to get it |
|----------|---------|----------------|
| `ELEVENLABS_API_KEY` | gritai-audio | [elevenlabs.io](https://elevenlabs.io) |
| `GEMINI_API_KEY` | gritai-image-gen | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |

**Alternative to shell exports:** You can set these in Claude Code settings instead of your shell profile:

```json
// ~/.claude/settings.json (user-level, all projects)
// or .claude/settings.local.json (project-level, gitignored)
{
  "env": {
    "GEMINI_API_KEY": "your-key-here",
    "ELEVENLABS_API_KEY": "your-key-here"
  }
}
```

## Contributing

1. Fork this repo
2. Create a branch for your changes
3. Follow the plugin structure in any existing plugin as a reference
4. Submit a PR

## License

MIT
