---
name: brreg
description: >
  ESSENTIAL for any task involving Norwegian companies, business registries, or
  Brønnøysundregistrene. Provides a bundled CLI tool (brreg_fetch.py) and API reference
  for the Enhetsregisteret and Regnskapsregisteret APIs -- without this you will struggle
  with case-sensitive name search, NACE code format quirks, pagination caps, and the
  nested roles endpoint. MUST use when: user mentions Brønnøysundregistrene, BRREG,
  Enhetsregisteret, Norwegian company lookup, organisasjonsnummer, org number, company
  registry, foretaksregisteret, or data.brreg.no; wants to find, look up, or analyze
  Norwegian companies; asks about board members, CEO, roles, financial statements,
  annual accounts, or company structure; or needs industry analysis by NACE code,
  municipality, or organization form (AS, ASA, ENK). Do NOT query BRREG without it.
---

# BRREG Company Explorer

This skill enables you to search, look up, and analyze Norwegian companies using Brønnøysundregistrene's open APIs. It covers the Entity Registry (Enhetsregisteret), roles/board members, and financial statements (Regnskapsregisteret).

## Quick Start

1. **Search** for companies by name, industry, location, or status
2. **Look up** a specific company by org number
3. **Get roles** (board members, CEO, auditor)
4. **Get financials** (latest annual accounts)

Use the bundled helper script at `scripts/brreg_fetch.py` (relative to this skill) for all API interactions.

## API Basics

- **Entity Registry**: `https://data.brreg.no/enhetsregisteret/api/`
- **Financial Statements**: `https://data.brreg.no/regnskapsregisteret/regnskap/`
- **Auth**: None required -- fully open data
- **Format**: JSON
- **Pagination**: 0-based pages, default size 20, hard cap at 10,000 results per query

For the full endpoint reference, read `references/api-reference.md`.

---

## Step 1: Search for Companies

```bash
# Search by name (case-sensitive -- use uppercase for best results)
python scripts/brreg_fetch.py search --name "EQUINOR"

# Search by municipality (Oslo = 0301)
python scripts/brreg_fetch.py search --kommune 0301 --orgform AS --size 10

# Search by industry (NACE code)
python scripts/brreg_fetch.py search --nace "62" --kommune 0301 --size 10

# Recently registered companies
python scripts/brreg_fetch.py search --registered-after 2026-01-01 --orgform AS --size 20

# Companies in bankruptcy
python scripts/brreg_fetch.py search --konkurs --size 10

# Combine filters
python scripts/brreg_fetch.py search --name "TECH" --orgform AS --kommune 0301 --size 20
```

### Important: Name search is case-sensitive

Company names in the registry are stored in UPPERCASE. Searching for "equinor" returns different results than "EQUINOR". For best results, uppercase your search terms. The script provides a `--ignore-case` flag that searches both original and uppercased forms.

### NACE code format

Use either 2-digit prefix (`62` for IT) or full 5-char format with dot (`62.010`). The formats `62.01` or `62.010` without proper structure may return 0 results. Common codes:
- `62` -- IT/computer programming
- `64` -- Financial services
- `68` -- Real estate
- `41` -- Construction
- `46` -- Wholesale trade
- `47` -- Retail trade
- `70` -- Management consultancy
- `06` -- Oil and gas extraction

## Step 2: Look Up a Company

```bash
# By org number
python scripts/brreg_fetch.py lookup 923609016

# Multiple org numbers
python scripts/brreg_fetch.py lookup 923609016 914778271 985258237
```

This returns full details: name, address, industry codes, number of employees, registration dates, capital structure, and more.

## Step 3: Get Roles (Board, CEO, Auditor)

```bash
# All roles for a company
python scripts/brreg_fetch.py roles 923609016

# Save to CSV
python scripts/brreg_fetch.py roles 923609016 --output equinor_board.csv
```

Key role types:
- `DAGL` -- CEO (Daglig leder)
- `LEDE` -- Chair of the Board (Styrets leder)
- `MEDL` -- Board member (Styremedlem)
- `NEST` -- Deputy chair (Nestleder)
- `VARA` -- Alternate member (Varamedlem)
- `REVI` -- Auditor (Revisor)
- `REGN` -- Accountant (Regnskapsfører)

## Step 4: Get Financial Statements

```bash
# Latest annual accounts
python scripts/brreg_fetch.py financials 923609016

# Save to CSV
python scripts/brreg_fetch.py financials 923609016 --output equinor_financials.csv

# Multiple companies
python scripts/brreg_fetch.py financials 923609016 914778271 --output comparison.csv
```

Returns key figures: revenue, operating profit, net income, total assets, equity, debt.

**Limitations:**
- Only the latest filed year is available via the API
- Bank accounts are not supported (returns error for banks)
- Small companies may use simplified reporting (`oppstillingsplan: smaa`)

## Step 5: Get Sub-entities (Branches)

```bash
# All branches of a company
python scripts/brreg_fetch.py subunits 923609016 --size 20
```

## Common Patterns

### Company profile (full picture)

```bash
python scripts/brreg_fetch.py lookup 923609016
python scripts/brreg_fetch.py roles 923609016
python scripts/brreg_fetch.py financials 923609016
python scripts/brreg_fetch.py subunits 923609016
```

### Industry analysis

```bash
# All AS companies in IT sector in Oslo
python scripts/brreg_fetch.py search --nace "62" --orgform AS --kommune 0301 --size 100 --output oslo_it_companies.csv
```

### Recently registered companies

```bash
python scripts/brreg_fetch.py search --registered-after 2026-01-01 --orgform AS --sort "stiftelsesdato,desc" --size 50
```

### Companies under financial distress

```bash
python scripts/brreg_fetch.py search --konkurs --size 50 --output bankruptcies.csv
python scripts/brreg_fetch.py search --under-avvikling --size 50 --output liquidations.csv
```

## Tips

- The **pagination cap is 10,000 results** per query. If your search returns more, add filters (municipality, org form, date range) to narrow it down.
- **`antallAnsatte`** (number of employees) is self-reported and may be 0 even for large companies.
- **`sisteInnsendteAarsregnskap`** tells you the most recent year of filed accounts, without needing to call the financials endpoint.
- **ENK** (sole proprietorships) don't file public accounts -- use `--orgform AS` to focus on companies with financial statements.
- Organization forms: `AS` (private limited), `ASA` (public limited), `ENK` (sole proprietorship), `NUF` (foreign entity), `SA` (cooperative), `STI` (foundation).
