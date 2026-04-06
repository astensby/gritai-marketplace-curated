# SSB PxWeb API v2 -- Complete Reference

**Base URL**: `https://data.ssb.no/api/pxwebapi/v2`  
**Auth**: None (open data)  
**Languages**: `en`, `no` (default)  
**OpenAPI Spec**: https://raw.githubusercontent.com/statisticssweden/PxApiSpecs/master/PxAPI-2.yml  
**Swagger UI**: https://data.ssb.no/api/pxwebapi/v2/index.html

## Table of Contents

1. [Endpoints](#endpoints)
2. [Table Search](#table-search)
3. [Table Info](#table-info)
4. [Metadata](#metadata)
5. [Codelists](#codelists)
6. [Default Selection](#default-selection)
7. [Data Queries -- GET](#data-queries-get)
8. [Data Queries -- POST](#data-queries-post)
9. [Selection Expressions](#selection-expressions)
10. [Output Formats](#output-formats)
11. [JSON-stat 2.0 Response Format](#json-stat-20-response-format)
12. [CSV Response Format](#csv-response-format)
13. [Config Endpoint](#config-endpoint)
14. [Error Handling](#error-handling)
15. [Subject Codes](#subject-codes)
16. [Saved Queries](#saved-queries)

---

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/tables` | Search/list tables |
| GET | `/tables/{id}` | Single table info |
| GET | `/tables/{id}/metadata` | Full metadata (JSON-stat 2.0) |
| GET | `/tables/{id}/defaultselection` | Default variable selection |
| GET | `/tables/{id}/data` | Fetch data (GET) |
| POST | `/tables/{id}/data` | Fetch data (POST) |
| GET | `/codelists/{id}` | Codelist definition |
| GET | `/config` | API configuration |
| POST | `/savedqueries` | Create saved query |
| GET | `/savedqueries/{id}` | Get saved query |
| GET | `/savedqueries/{id}/data` | Execute saved query |
| GET | `/savedqueries/{id}/selection` | Get resolved selection |

All endpoints accept `?lang=en` or `?lang=no` query parameter.

---

## Table Search

**GET /tables**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Full-text search |
| `lang` | string | `en` or `no` |
| `pastDays` | integer | Tables updated within N days |
| `includeDiscontinued` | boolean | Include discontinued tables |
| `pageNumber` | integer | Page (default 1) |
| `pageSize` | integer | Results per page |

**Response**:
```json
{
  "tables": [
    {
      "id": "07459",
      "label": "Population, by region, sex, age, contents and year",
      "description": "...",
      "sortCode": "...",
      "updated": "2026-02-25T07:00:00Z",
      "firstPeriod": "1986",
      "lastPeriod": "2026",
      "category": "public",
      "variableNames": ["region", "sex", "age", "contents", "year"],
      "source": "Statistics Norway",
      "subjectCode": "be",
      "timeUnit": "Annual",
      "paths": [[{"id": "be", "label": "Population"}, ...]],
      "links": [...]
    }
  ],
  "page": {
    "pageNumber": 1,
    "pageSize": 10,
    "totalElements": 451,
    "totalPages": 46,
    "links": [...]
  }
}
```

---

## Table Info

**GET /tables/{id}**

Returns a single table object (same structure as in search results) with full details.

---

## Metadata

**GET /tables/{id}/metadata**

Returns JSON-stat 2.0 Dataset object describing the table structure.

| Parameter | Type | Description |
|-----------|------|-------------|
| `lang` | string | `en` or `no` |
| `codelist[VarCode]` | string | Apply codelist to variable |
| `defaultSelection` | boolean | Apply default selection |

**Response structure**:
```json
{
  "version": "2.0",
  "class": "dataset",
  "label": "Table title",
  "id": ["Region", "Kjonn", "Alder", "ContentsCode", "Tid"],
  "size": [994, 2, 106, 1, 41],
  "dimension": {
    "Region": {
      "label": "region",
      "category": {
        "index": {"0301": 0, "4601": 1, ...},
        "label": {"0301": "Oslo", "4601": "Bergen", ...}
      },
      "extension": {
        "elimination": true,
        "show": "value",
        "codelists": [
          {"id": "vs_RegionKommune", "label": "Municipality", "type": "Valueset"},
          {"id": "agg_RegionFylke", "label": "County", "type": "Aggregation"}
        ]
      }
    },
    "Tid": {
      "label": "year",
      "category": {
        "index": {"1986": 0, "1987": 1, ..., "2026": 40},
        "label": {"1986": "1986", ..., "2026": "2026"}
      }
    },
    "ContentsCode": {
      "category": {
        "unit": {"Personer1": {"base": "number", "decimals": 0}}
      }
    }
  },
  "role": {"time": ["Tid"], "geo": ["Region"], "metric": ["ContentsCode"]},
  "extension": {
    "px": {"tableid": "07459", "decimals": 0},
    "contact": [{"name": "...", "email": "...", "phone": "..."}]
  }
}
```

Key fields per dimension:
- `category.index` -- value code to position mapping
- `category.label` -- value code to label mapping
- `category.unit` -- (ContentsCode only) measurement units
- `extension.elimination` -- can this variable be omitted?
- `extension.codelists` -- available aggregation/valueset codelists

---

## Codelists

**GET /codelists/{id}**

```json
{
  "id": "agg_FemAarigGruppering",
  "label": "Five-year groups",
  "type": "Aggregation",
  "values": [
    {"code": "F00-04", "label": "0-4 years", "valueMap": ["000","001","002","003","004"]},
    {"code": "F05-09", "label": "5-9 years", "valueMap": ["005","006","007","008","009"]},
    ...
  ]
}
```

- **Aggregation** codelists map original values to groups
- **Valueset** codelists filter to a subset of values

---

## Default Selection

**GET /tables/{id}/defaultselection**

Returns the default variable selections the API uses when no explicit selection is provided:

```json
{
  "selection": [
    {"variableCode": "Region", "valueCodes": ["0"], "codelist": null},
    {"variableCode": "Kjonn", "valueCodes": ["*"], "codelist": null},
    {"variableCode": "Alder", "valueCodes": ["*"], "codelist": "agg_FemAarigGruppering"},
    {"variableCode": "ContentsCode", "valueCodes": ["*"], "codelist": null},
    {"variableCode": "Tid", "valueCodes": ["top(5)"], "codelist": null}
  ]
}
```

---

## Data Queries -- GET

**GET /tables/{id}/data**

Query parameters use deepObject style:

| Parameter | Style | Description |
|-----------|-------|-------------|
| `valuecodes[VarCode]` | deepObject | Comma-separated value codes or expression |
| `codelist[VarCode]` | deepObject | Codelist ID to apply |
| `outputFormat` | string | Output format |
| `outputFormatParams` | string | Comma-separated format options |
| `heading` | string | Comma-separated variables for heading |
| `stub` | string | Comma-separated variables for stub |
| `lang` | string | `en` or `no` |

**Example**:
```
GET /tables/07459/data?lang=en
  &valuecodes[Region]=0301
  &valuecodes[Kjonn]=1,2
  &valuecodes[Alder]=000
  &valuecodes[ContentsCode]=Personer1
  &valuecodes[Tid]=top(3)
  &outputFormat=csv
```

URL encoding: `[` = `%5B`, `]` = `%5D`

---

## Data Queries -- POST

**POST /tables/{id}/data**

```json
{
  "selection": [
    {
      "variableCode": "Region",
      "valueCodes": ["0301", "4601"]
    },
    {
      "variableCode": "Kjonn",
      "valueCodes": ["1", "2"]
    },
    {
      "variableCode": "Alder",
      "codelist": "agg_FemAarigGruppering",
      "valueCodes": ["F00-04", "F05-09"]
    },
    {
      "variableCode": "ContentsCode",
      "valueCodes": ["Personer1"]
    },
    {
      "variableCode": "Tid",
      "valueCodes": ["top(3)"]
    }
  ],
  "placement": {
    "heading": ["ContentsCode", "Tid"],
    "stub": ["Region", "Kjonn", "Alder"]
  }
}
```

- `selection` is required; each variable in the table should be included (unless eliminatable)
- `codelist` is optional per variable
- `placement` is optional (controls output layout)
- Expressions (`top()`, `from()`, `*`, etc.) work inside `valueCodes` array

Query string params `?outputFormat=csv&lang=en` still apply to POST requests.

---

## Selection Expressions

| Expression | Description | Example |
|-----------|-------------|---------|
| Literal | Specific code(s) | `"0301"` or `["0301", "4601"]` |
| `*` | All values | `["*"]` |
| `top(n)` | Last n values | `["top(5)"]` |
| `bottom(n)` | First n values | `["bottom(3)"]` |
| `from(code)` | From code onward | `["from(2020)"]` |
| `range(a,b)` | Range inclusive | `["range(2015,2025)"]` |

In GET requests, `range()` needs brackets: `[range(000,005)]`

---

## Output Formats

| Format | `outputFormat` value | Content-Type |
|--------|---------------------|--------------|
| JSON-stat 2.0 | `json-stat2` | application/json |
| CSV | `csv` | text/plain |
| Excel | `xlsx` | application/octet-stream |
| HTML table | `html` | text/plain |
| PX file | `px` | text/plain |
| JSON-PX | `json-px` | application/json |

**Output format params** (comma-separated in `outputFormatParams`):
- `UseCodes` -- Code values only
- `UseTexts` -- Text labels only
- `UseCodesAndTexts` -- Both
- `IncludeTitle` -- Add title row
- `SeparatorTab` / `SeparatorSemicolon` / `SeparatorSpace` -- CSV separator
- `ExcludeZerosAndMissingValues` -- Skip zero/null rows

---

## JSON-stat 2.0 Response Format

```json
{
  "version": "2.0",
  "class": "dataset",
  "label": "Table title",
  "source": "Statistics Norway",
  "updated": "2026-02-25T07:00:00Z",
  "id": ["Region", "Kjonn", "ContentsCode", "Tid"],
  "size": [1, 2, 1, 3],
  "dimension": { ... },
  "role": {"time": ["Tid"], "geo": ["Region"], "metric": ["ContentsCode"]},
  "value": [4214, 4452, 4631, 4002, 3960, 4132]
}
```

The `value` array is **flat, row-major order**. To decode position `[i0, i1, ..., iN]`:

```
flat_index = i0 * (size[1] * size[2] * ... * size[N])
           + i1 * (size[2] * ... * size[N])
           + ...
           + iN
```

Missing values appear as `null`.

---

## CSV Response Format

```csv
"region","sex","contents","year","value"
"0301 Oslo","Males","Persons",2024,4214
"0301 Oslo","Males","Persons",2025,4452
```

With `IncludeTitle`:
```csv
"07459: Population, by region, sex, age and year"
"region","sex","contents","year","value"
...
```

---

## Config Endpoint

**GET /config**

```json
{
  "apiVersion": "2.2.0",
  "appVersion": "2.3.0+build.22",
  "languages": [{"id": "no", "label": "Norsk"}, {"id": "en", "label": "English"}],
  "defaultLanguage": "no",
  "maxDataCells": 800000,
  "maxCallsPerTimeWindow": 0,
  "timeWindow": 0,
  "license": "https://www.ssb.no/en/diverse/lisens",
  "sourceReferences": [
    {"language": "en", "text": "Source: Statistics Norway"},
    {"language": "no", "text": "Kilde: Statistisk sentralbyra"}
  ],
  "defaultDataFormat": "json-stat2",
  "dataFormats": ["json-stat2", "csv", "px", "xlsx", "html", "json-px"],
  "features": [{"id": "CORS", "params": [{"key": "enabled", "value": "True"}]}]
}
```

---

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Invalid parameters, non-existent values, too many cells, illegal expression |
| 403 | Forbidden (cell threshold exceeded) |
| 404 | Table/resource not found |
| 429 | Rate limit (not currently enforced) |

Error response body:
```json
{
  "type": "Parameter error",
  "title": "Too many cells selected",
  "status": 400,
  "detail": "Too many cells selected"
}
```

---

## Subject Codes

| Code | Subject |
|------|---------|
| `al` | Labour market and earnings |
| `bb` | Construction, housing and property |
| `be` | Population |
| `bf` | Banking and financial markets |
| `ei` | Energy, manufacturing and mining |
| `he` | Health |
| `if` | Income and consumption |
| `js` | Construction (alternative) |
| `kf` | Culture and recreation |
| `nk` | National accounts |
| `nm` | Nature and environment |
| `os` | Public sector |
| `pp` | Prices and price indices |
| `sk` | Social conditions |
| `ti` | Establishments and enterprises |
| `tr` | Transport and tourism |
| `ud` | Education |
| `ut` | External economy |
| `va` | Elections |
| `vf` | Enterprises |

---

## Saved Queries

**POST /savedqueries** -- Create a saved query for re-use:
```json
{
  "tableId": "07459",
  "selection": [...],
  "placement": {...}
}
```

**GET /savedqueries/{id}** -- Retrieve definition  
**GET /savedqueries/{id}/data?outputFormat=csv** -- Execute and get data  
**GET /savedqueries/{id}/selection** -- Get resolved selection
