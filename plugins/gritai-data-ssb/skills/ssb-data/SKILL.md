---
name: ssb-data
description: >
  ESSENTIAL for any task involving Norwegian statistics, SSB, or data.ssb.no. Provides a
  bundled CLI tool (ssb_fetch.py) and API reference for Statistics Norway's PxWeb API v2 —
  without this you will waste time reverse-engineering JSON-stat 2.0, codelists, and query
  syntax. MUST use when: user mentions SSB, Statistisk sentralbyrå, Statistics Norway,
  Statistikkbanken, data.ssb.no; wants Norwegian demographic, economic, labor, health,
  education, population, housing, price, immigration, trade, or environmental data;
  references SSB table IDs like "07459"; asks about kommuner/fylker statistics; or even
  casually asks "population of Oslo", "unemployment in Norway", "KPI data", "boligpriser".
  Contains a Python script for searching 3,900+ tables, fetching metadata, querying data,
  and parsing to CSV — do NOT query the SSB API without it.
---

# SSB Data Explorer

This skill enables you to discover, fetch, and analyze data from Statistics Norway's (SSB) open data API. SSB publishes ~3,900 statistical tables covering demographics, economy, health, education, labor, housing, prices, trade, environment, and more.

## Quick Start

The typical workflow has four steps:

1. **Search** for relevant tables
2. **Explore** table metadata (variables, values, codelists)
3. **Fetch** data with a targeted query
4. **Analyze** the results

Use the bundled helper script at `scripts/ssb_fetch.py` (relative to this skill) for all API interactions. It handles JSON-stat 2.0 parsing, pagination, and outputs clean pandas DataFrames or CSV files. Run it with `python` or `python3`.

## API Basics

- **Base URL**: `https://data.ssb.no/api/pxwebapi/v2`
- **Auth**: None required -- fully open data
- **Languages**: `en` (English) or `no` (Norwegian, default)
- **Max cells per request**: 800,000
- **Default output**: JSON-stat 2.0

For the full endpoint reference, read `references/api-reference.md`.

---

## Step 1: Search for Tables

Find tables by keyword search:

```bash
python scripts/ssb_fetch.py search "population" --lang en --limit 10
```

This searches table titles, descriptions, and variable names. Common search strategies:

- **Broad topic**: `"population"`, `"employment"`, `"income"`, `"prices"`, `"housing"`
- **Specific measure**: `"consumer price index"`, `"unemployment rate"`, `"births"`
- **Geographic**: `"municipalities"`, `"counties"`, `"kommuner"`, `"fylker"`
- **Recently updated**: add `--past-days 30` to find tables updated in the last month

The search returns table IDs, titles, time ranges, and last update dates. Note the table ID (e.g., `07459`) for the next step.

If you know the subject area, you can also browse by subject code. Common subject codes:
- `be` -- Population
- `al` -- Labour market and earnings
- `pp` -- Prices and price indices
- `he` -- Health
- `ud` -- Education
- `if` -- Income and consumption
- `bb` -- Construction, housing and property
- `ei` -- Energy, manufacturing and mining
- `ut` -- External economy
- `nm` -- Nature and environment

## Step 2: Explore Table Metadata

Once you have a table ID, inspect its structure:

```bash
python scripts/ssb_fetch.py metadata 07459 --lang en
```

This shows:
- **Table title** and description
- **Variables** (dimensions) with their codes and available values
- **Codelists** available for aggregation (e.g., 5-year age groups, county-level regions)
- **Time range** covered
- **Which variables can be eliminated** (omitted to sum across that dimension)

Understanding the metadata is critical before querying. Pay attention to:
- **Variable codes**: These are what you use in queries (e.g., `Region`, `Kjonn`, `Alder`, `Tid`)
- **Value codes**: The actual selectable values (e.g., `0301` for Oslo, `1` for Males)
- **Codelists**: Aggregation options that group values (e.g., `agg_FemAarigGruppering` groups single ages into 5-year bands)

To inspect a specific codelist:

```bash
python scripts/ssb_fetch.py codelist agg_FemAarigGruppering --lang en
```

## Step 3: Fetch Data

### Simple queries (few selections)

```bash
python scripts/ssb_fetch.py data 07459 \
  --select "Region=0301" \
  --select "Kjonn=1,2" \
  --select "Alder=000" \
  --select "ContentsCode=Personer1" \
  --select "Tid=top(5)" \
  --lang en \
  --format csv \
  --output population_oslo.csv
```

### Complex queries (codelists, many values)

For queries with codelists or many selections, use a JSON query file:

```bash
python scripts/ssb_fetch.py data 07459 --query query.json --lang en --output result.csv
```

Where `query.json` looks like:

```json
{
  "selection": [
    {"variableCode": "Region", "valueCodes": ["0301", "4601"]},
    {"variableCode": "Kjonn", "valueCodes": ["*"]},
    {"variableCode": "Alder", "codelist": "agg_FemAarigGruppering", "valueCodes": ["*"]},
    {"variableCode": "ContentsCode", "valueCodes": ["Personer1"]},
    {"variableCode": "Tid", "valueCodes": ["top(10)"]}
  ]
}
```

### Selection expressions

These work in both `--select` values and JSON query files:

| Expression | Meaning | Example |
|-----------|---------|---------|
| Literal codes | Specific values | `0301,4601` |
| `*` | All values | `*` |
| `top(n)` | Last n values (most recent for time) | `top(5)` |
| `bottom(n)` | First n values | `bottom(3)` |
| `from(code)` | All values from code onward | `from(2020)` |
| `range(a,b)` | Values from a through b | `range(2015,2025)` |

### Elimination

Variables marked as "eliminatable" can be omitted entirely from your query. When omitted, values are summed across that dimension. For example, omitting `Kjonn` (sex) returns totals for both sexes combined.

### Output formats

Use `--format` with: `csv` (recommended for analysis), `json-stat2` (raw API format), `xlsx`, `html`.

## Step 4: Analyze the Data

The script outputs clean CSV or pandas-ready data. For analysis in the conversation:

```bash
# Fetch as CSV and inspect
python scripts/ssb_fetch.py data 07459 \
  --select "Region=0301" \
  --select "Kjonn=1,2" \
  --select "ContentsCode=Personer1" \
  --select "Tid=top(10)" \
  --lang en \
  --format csv \
  --output data.csv
```

Then read the CSV and perform analysis -- pivot tables, time series, comparisons, etc.

For quick inline analysis, you can also use the `--analyze` flag which prints summary statistics:

```bash
python scripts/ssb_fetch.py data 07459 \
  --select "Region=0301" \
  --select "ContentsCode=Personer1" \
  --select "Tid=top(10)" \
  --lang en \
  --analyze
```

---

## Common Patterns

### Population by municipality for the latest year

```bash
python scripts/ssb_fetch.py data 07459 \
  --select "Region=*" \
  --select "ContentsCode=Personer1" \
  --select "Tid=top(1)" \
  --lang en --format csv --output pop_municipalities.csv
```

Note: omitting `Kjonn` and `Alder` (both eliminatable) gives totals.

### Time series for a specific region

```bash
python scripts/ssb_fetch.py data 07459 \
  --select "Region=0301" \
  --select "ContentsCode=Personer1" \
  --select "Tid=from(2000)" \
  --lang en --format csv --output oslo_pop_timeseries.csv
```

### Comparing regions with age group aggregation

Use a JSON query to apply codelists:

```json
{
  "selection": [
    {"variableCode": "Region", "valueCodes": ["0301", "4601", "5001"]},
    {"variableCode": "Kjonn", "valueCodes": ["*"]},
    {"variableCode": "Alder", "codelist": "agg_TredeltGrupperingB2", "valueCodes": ["*"]},
    {"variableCode": "ContentsCode", "valueCodes": ["Personer1"]},
    {"variableCode": "Tid", "valueCodes": ["top(1)"]}
  ]
}
```

This compares Oslo (0301), Bergen (4601), and Trondheim (5001) using the tripartite age grouping (0-19, 20-64, 65+).

---

## Handling Large Tables

If a query exceeds 800,000 cells, the API will reject it. Strategies:

1. **Reduce selections**: Pick specific regions/years instead of `*`
2. **Use codelists**: Aggregate ages, regions, etc. into groups
3. **Eliminate variables**: Omit eliminatable dimensions to collapse them
4. **Split queries**: Fetch data in batches (e.g., by year range) and combine

The script estimates cell count before querying and warns if you're approaching the limit.

## Tips

- Always start with `search` and `metadata` before trying to fetch data. Understanding the table structure prevents wasted queries.
- Norwegian and English table content can differ slightly. If you can't find something in English, try Norwegian (`--lang no`).
- The `ContentsCode` variable contains the actual measures (e.g., "Persons", "Per cent", "NOK"). A single table can have multiple measures.
- Time variable codes follow patterns: `2024` (annual), `2024M01` (monthly), `2024K1` (quarterly).
- Region codes: `0301` = Oslo, `4601` = Bergen, `5001` = Trondheim, `03` = Oslo county, `30` = Viken, etc.
