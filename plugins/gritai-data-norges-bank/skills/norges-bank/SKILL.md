---
name: norges-bank
description: >
  ESSENTIAL for any task involving Norges Bank data, Norwegian exchange rates, policy rates,
  NOWA, government bonds, or financial market data from Norway's central bank. Provides a
  bundled CLI tool (nb_fetch.py) and complete API reference for Norges Bank's SDMX REST API
  -- without this you will waste time on SDMX key syntax, semicolon-delimited CSV parsing,
  and UNIT_MULT scaling. MUST use when: user mentions Norges Bank, styringsrenten, valutakurs,
  NOK exchange rate, NOWA, Norwegian government bonds, or data.norges-bank.no; wants USD/NOK,
  EUR/NOK, or any currency-to-NOK rate; asks about Norwegian interest rates, policy rate
  history, yield curves, or financial conditions; or references datasets like EXR, IR, or
  SHORT_RATES. Contains a Python script for listing datasets, fetching data, and parsing
  SDMX responses into clean CSV -- do NOT query the Norges Bank API without it.
---

# Norges Bank Data Explorer

This skill enables you to discover, fetch, and analyze data from Norges Bank's (Norwegian central bank) open data API. It covers exchange rates, interest rates, government debt, banking liquidity, and financial indicators.

## Quick Start

1. **List** available datasets or explore a specific one
2. **Fetch** data with targeted series keys
3. **Analyze** the results

Use the bundled helper script at `scripts/nb_fetch.py` (relative to this skill) for all API interactions. It handles SDMX key construction, CSV parsing (semicolon-delimited), and UNIT_MULT scaling.

## API Basics

- **Base URL**: `https://data.norges-bank.no/api/`
- **Auth**: None required -- fully open data
- **Protocol**: SDMX REST API v2.1
- **Languages**: `en` (default), `no` (Norwegian -- changes decimal separator to comma, avoid for parsing)
- **CSV delimiter**: Semicolon (`;`), not comma

For the full endpoint reference, read `references/api-reference.md`.

---

## Key Datasets

| Dataset | Description | Key Use Cases |
|---------|-------------|---------------|
| **EXR** | Exchange rates (41 currencies vs NOK) | USD/NOK, EUR/NOK, trade-weighted index |
| **IR** | Policy rate (styringsrenten) | Current/historical key policy rate |
| **SHORT_RATES** | NOWA overnight rate | Interbank rates, compounded averages |
| **ANN_KPRA** | Policy rate announcements | Rate decisions, changes, effective dates |
| **FINANCIAL_INDICATORS** | Financial Conditions Index | FCI total and subcomponents |
| **GOVT_GENERIC_RATES** | Government bond yields | Yield curve (3M to 10Y) |
| **GOVT_ZEROCOUPON** | Zero coupon yields | Term structure |
| **SEC** | Securities prices and yields | Individual bond data |
| **REGNET** | Regional Network survey | Business sentiment by region |

## Step 1: Explore Available Data

List all datasets:

```bash
python scripts/nb_fetch.py datasets
```

Explore a specific dataset's structure (dimensions, available values):

```bash
python scripts/nb_fetch.py structure EXR
```

List all available series keys in a dataset:

```bash
python scripts/nb_fetch.py series EXR
```

## Step 2: Fetch Data

### Exchange rates

```bash
# Latest USD/NOK rate
python scripts/nb_fetch.py data EXR B.USD.NOK.SP --last 1

# Multiple currencies, date range
python scripts/nb_fetch.py data EXR B.USD+EUR+GBP+SEK.NOK.SP --start 2024-01-01 --end 2024-12-31

# All currencies for today
python scripts/nb_fetch.py data EXR "B..NOK.SP" --last 1

# Monthly averages
python scripts/nb_fetch.py data EXR M.USD+EUR.NOK.SP --start 2024-01

# Trade-weighted index
python scripts/nb_fetch.py data EXR B.TWI.NOK.SP --last 30
```

### Interest rates

```bash
# Current policy rate
python scripts/nb_fetch.py data IR B.KPRA..R --last 1

# Policy rate history
python scripts/nb_fetch.py data IR B.KPRA.SD.R --start 2020-01-01

# Policy rate announcements (last 10 decisions)
python scripts/nb_fetch.py data ANN_KPRA KPRA --last 10

# NOWA overnight rate
python scripts/nb_fetch.py data SHORT_RATES B.NOWA.ON.R --last 10
```

### Government bonds

```bash
# 10-year government bond yield
python scripts/nb_fetch.py data GOVT_GENERIC_RATES B.10Y.GBON --last 30

# Full yield curve (latest)
python scripts/nb_fetch.py data GOVT_GENERIC_RATES "B..GBON" --last 1

# Zero coupon yields
python scripts/nb_fetch.py data GOVT_ZEROCOUPON "B." --last 1
```

### Financial indicators

```bash
# Financial Conditions Index
python scripts/nb_fetch.py data FINANCIAL_INDICATORS D.FCI_TOTAL --last 30

# All FCI subcomponents
python scripts/nb_fetch.py data FINANCIAL_INDICATORS "D." --last 10
```

## SDMX Key Syntax

The key is a dot-separated string where each position is a dimension:

| Pattern | Meaning | Example |
|---------|---------|---------|
| `B.USD.NOK.SP` | Specific values | Daily USD/NOK spot |
| `B.USD+EUR.NOK.SP` | Multiple values with `+` | USD and EUR |
| `B..NOK.SP` | Empty = wildcard (all) | All currencies |
| `B.USD` | Trailing dims omitted | Partial key |

### Common frequency codes
- `B` -- Business daily (excludes weekends/holidays)
- `D` -- Daily (calendar days)
- `M` -- Monthly (averages)
- `A` -- Annual (averages)

## Output Options

```bash
# Save to CSV file
python scripts/nb_fetch.py data EXR B.USD.NOK.SP --start 2024-01-01 --output usdnok.csv

# Get raw SDMX-JSON
python scripts/nb_fetch.py data EXR B.USD.NOK.SP --last 5 --format sdmx-json

# Quick summary statistics
python scripts/nb_fetch.py data EXR B.USD.NOK.SP --start 2024-01-01 --analyze
```

## Important Gotchas

1. **UNIT_MULT scaling**: Some currencies are quoted per 100 units (SEK, DKK, JPY, etc.). The script handles this automatically -- values are always shown as "1 foreign currency = X NOK".

2. **Semicolon CSV**: The raw API returns semicolon-delimited CSV. The script converts to comma-delimited.

3. **Locale**: Never use `locale=no` for data parsing -- it changes decimal separator from `.` to `,`. The script always uses `locale=en`.

4. **Business days**: Daily exchange rates (`B` frequency) skip weekends and Norwegian public holidays. Use `M` or `A` for continuous time series.

5. **Discontinued currencies**: RUB (discontinued 2022-03-01), HRK (discontinued 2022-12-30).

6. **Collection time**: Exchange rates are fixed at ECB concertation time, 14:15 CET.

## Tips

- For exchange rate analysis, use monthly (`M`) frequency to avoid gaps from holidays.
- The trade-weighted index (`TWI`) and import-weighted index (`I44`) are calculated indices, not direct rates.
- Policy rate announcements (`ANN_KPRA`) include `VALID_FROM` and `DELTA_VALUE` attributes showing when the rate took effect and by how much it changed.
- Government generic rates have tenors: `3M`, `6M`, `12M`, `3Y`, `5Y`, `7Y`, `10Y`.
