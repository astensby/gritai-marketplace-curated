# Norges Bank SDMX REST API -- Complete Reference

**Base URL**: `https://data.norges-bank.no/api/`  
**Auth**: None (open data)  
**Protocol**: SDMX REST API v2.1  
**Agency ID**: `NB`  
**Contact**: data@norges-bank.no

## Table of Contents

1. [Endpoints](#endpoints)
2. [Data Queries](#data-queries)
3. [SDMX Key Structure](#sdmx-key-structure)
4. [Query Parameters](#query-parameters)
5. [Response Formats](#response-formats)
6. [Dataset Catalog](#dataset-catalog)
7. [EXR -- Exchange Rates](#exr----exchange-rates)
8. [IR -- Policy Rate](#ir----policy-rate)
9. [SHORT_RATES -- NOWA](#short_rates----nowa)
10. [ANN_KPRA -- Rate Announcements](#ann_kpra----rate-announcements)
11. [FINANCIAL_INDICATORS](#financial_indicators)
12. [GOVT_GENERIC_RATES -- Bond Yields](#govt_generic_rates----bond-yields)
13. [Other Datasets](#other-datasets)
14. [Error Handling](#error-handling)
15. [Practical Notes](#practical-notes)

---

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/data/{dataflow}/{key}` | Fetch data series |
| GET | `/data/{dataflow}` | Fetch all data in a dataflow |
| GET | `/dataflow/all/all/latest` | List all available dataflows |
| GET | `/datastructure` | List data structure definitions |

---

## Data Queries

```
GET /data/{dataflow}/{key}?{parameters}
```

- `{dataflow}` -- Dataset ID: `EXR`, `IR`, `SHORT_RATES`, etc.
- `{key}` -- Dot-separated dimension values (optional, omit for all)

---

## SDMX Key Structure

Each position in the key corresponds to a dimension defined in the dataset's structure.

| Pattern | Meaning |
|---------|---------|
| `B.USD.NOK.SP` | Specific value per dimension |
| `B.USD+EUR+GBP.NOK.SP` | Multiple values with `+` (OR) |
| `B..NOK.SP` | Empty position = all values (wildcard) |
| `B.USD` | Trailing dimensions omitted |

---

## Query Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `format` | string | Response format | `csv`, `sdmx-json`, `sdmx-compact-2.1` |
| `startPeriod` | string | Start date | `2024-01-01`, `2024-01`, `2024` |
| `endPeriod` | string | End date | `2024-12-31` |
| `lastNObservations` | integer | Last N observations per series | `5` |
| `firstNObservations` | integer | First N observations per series | `3` |
| `updatedAfter` | string | Data updated after timestamp | `2024-03-01T00:00:00` |
| `detail` | string | Detail level | `full`, `dataonly`, `serieskeysonly`, `nodata` |
| `locale` | string | Language | `en` (default), `no` |

**Warning**: `locale=no` changes decimal separator from `.` to `,`. Always use `locale=en` for programmatic access.

---

## Response Formats

### CSV (`format=csv`)
- **Delimiter**: Semicolon (`;`)
- Includes dimension codes, names, TIME_PERIOD, OBS_VALUE, and attributes
- Default locale is English

### SDMX-JSON (`format=sdmx-json`)
```json
{
  "meta": {"id": "...", "prepared": "..."},
  "data": {
    "dataSets": [{
      "series": {
        "0:0:0:0": {
          "attributes": [0, 0, 0, 0],
          "observations": {
            "0": ["10.2971"],
            "1": ["10.3672"]
          }
        }
      }
    }],
    "structure": {
      "dimensions": {
        "series": [...],
        "observation": [{"id": "TIME_PERIOD", "values": [...]}]
      },
      "attributes": {"series": [...], "observation": [...]}
    }
  }
}
```

Series keys `"0:0:0:0"` are colon-separated indices into `dimensions.series[n].values`.
Observation keys `"0"`, `"1"` are indices into `dimensions.observation[0].values` (TIME_PERIOD).

### XML (default)
Standard SDMX 2.1 compact XML format when no `format` parameter specified.

---

## Dataset Catalog

### Core Datasets

| ID | Name | Key Structure | Data From |
|---|---|---|---|
| `EXR` | Exchange rates | `FREQ.BASE_CUR.QUOTE_CUR.TENOR` | 1960 |
| `IR` | Policy rate | `FREQ.INSTRUMENT_TYPE.TENOR.UNIT_MEASURE` | 1991 |
| `SHORT_RATES` | NOWA overnight rate | `FREQ.INSTRUMENT_TYPE.TENOR.UNIT_MEASURE` | 2011 |
| `ANN_KPRA` | Policy rate announcements | `INSTRUMENT_TYPE` | Historic |
| `FINANCIAL_INDICATORS` | Financial Conditions Index | `FREQ.INDICATOR` | 2002 |

### Government Debt

| ID | Name | Key Structure |
|---|---|---|
| `GOVT_GENERIC_RATES` | Generic bond/bill yields | `FREQ.TENOR.INSTRUMENT_TYPE` |
| `GOVT_ZEROCOUPON` | Zero coupon yields | `FREQ.TENOR` |
| `GOVT_IRS` | Interest rate swaps | Complex (9 dims) |
| `GOVT_KEYFIGURES` | Key debt indicators | `UNIT_MEASURE.QUARTER.FREQ.INSTRUMENT_TYPE` |
| `GOVT_PRIMARY_MARKET` | Auctions | Complex |
| `GOVT_SECONDARY_MARKET` | Secondary market turnover | Complex |
| `SEC` | Securities | `FREQ.SECURITY.UNIT_MEASURE` |

### Banking / Liquidity

| ID | Name |
|---|---|
| `LIQUIDITY_FORECAST` | Structural/total liquidity forecast |
| `LIQUIDITY_STATISTICS` | Bank liquidity statistics |
| `FAUCTION` | F-auction announcements and results |
| `MONEY_MARKET` | Money market data |
| `SETTLEMENT_STATISTICS` | Settlement system statistics |

### Other

| ID | Name |
|---|---|
| `REGNET` | Regional Network survey |
| `ANN_FX_SPU` | FX transactions for Government Pension Fund |

---

## EXR -- Exchange Rates

**Key**: `FREQ.BASE_CUR.QUOTE_CUR.TENOR`

### Frequency (FREQ)
- `B` -- Business daily
- `M` -- Monthly average
- `A` -- Annual average

### Currencies (BASE_CUR) -- 41 total
`USD`, `EUR`, `GBP`, `SEK`, `DKK`, `CHF`, `JPY`, `CAD`, `AUD`, `NZD`, `CNY`, `HKD`, `SGD`, `KRW`, `INR`, `THB`, `MYR`, `IDR`, `PHP`, `TWD`, `ZAR`, `TRY`, `PLN`, `CZK`, `HUF`, `RON`, `BGN`, `HRK` (discontinued 2022-12-30), `ISK`, `ILS`, `MXN`, `BRL`, `PKR`, `BDT`, `MMK`, `VND`, `BYN`, `RUB` (discontinued 2022-03-01), `XDR` (IMF SDR), `TWI` (trade-weighted index), `I44` (import-weighted index)

### Quote Currency (QUOTE_CUR)
Always `NOK`.

### Tenor
Always `SP` (Spot).

### UNIT_MULT (important!)
- `0` (Units): Most major currencies (USD, EUR, GBP, etc.) -- rate is per 1 unit
- `2` (Hundreds): SEK, DKK, JPY, CHF, CZK, HUF, ISK, INR, THB, KRW, etc. -- rate is per 100 units

To get "1 foreign currency = X NOK": `adjusted_rate = OBS_VALUE * 10^(-UNIT_MULT)`

### Collection
Exchange rates fixed at ECB concertation time, **14:15 CET**.

---

## IR -- Policy Rate

**Key**: `FREQ.INSTRUMENT_TYPE.TENOR.UNIT_MEASURE`

- **INSTRUMENT_TYPE**: `KPRA`
- **TENOR**: `SD` (Sight deposit / key policy rate), `OL` (Overnight lending), `RR` (Reserve rate)
- **UNIT_MEASURE**: `R` (Rate in percent)

Current rates (April 2026): SD=4.00%, OL=5.00%, RR=3.00%

---

## SHORT_RATES -- NOWA

**Key**: `FREQ.INSTRUMENT_TYPE.TENOR.UNIT_MEASURE`

- **INSTRUMENT_TYPE**: `NOWA` (daily), `NOWA_AVERAGE` (compounded)
- **TENOR**: `ON` (overnight), `1D`, `1M`, `3M`, `6M`
- **UNIT_MEASURE**: `R` (Rate), `V` (Volume), `T` (Transactions), `I` (Index), `BL` (Banks lending), `BB` (Banks borrowing)

---

## ANN_KPRA -- Rate Announcements

**Key**: `INSTRUMENT_TYPE` (always `KPRA`)

Each observation includes attributes:
- `VALID_FROM` -- Date the rate takes effect
- `DELTA_VALUE` -- Change from previous rate
- `OVERNIGHT_LENDING_RATE`, `RESERVE_RATE`, `SIGHT_DEPOSIT_RATE`

---

## FINANCIAL_INDICATORS

**Key**: `FREQ.INDICATOR`

- **FREQ**: `D` (Daily)
- **INDICATOR**: `FCI_TOTAL`, `FCI_FEX`, `FCI_HOUSING`, `FCI_LENDINGRATES`, `FCI_STOCK`

---

## GOVT_GENERIC_RATES -- Bond Yields

**Key**: `FREQ.TENOR.INSTRUMENT_TYPE`

- **FREQ**: `B`, `M`, `A`
- **TENOR**: `3M`, `6M`, `12M`, `3Y`, `5Y`, `7Y`, `10Y`
- **INSTRUMENT_TYPE**: `GBON` (Government bonds), `TBIL` (Treasury bills)

---

## Error Handling

| Status | Meaning |
|--------|---------|
| 200 | Success (may still be empty result set) |
| 400 | Invalid query syntax |
| 404 | No data found (invalid code, future date, wrong dataset) |
| 406 | Unsupported format |

---

## Practical Notes

1. CSV uses semicolon (`;`) as delimiter, not comma
2. `locale=no` changes decimal separator from `.` to `,` -- avoid for programmatic use
3. UNIT_MULT must be accounted for in exchange rates (some are per 100 units)
4. Business day frequency (`B`) excludes weekends and Norwegian public holidays
5. Monthly/Annual values are averages (`COLLECTION=A`)
6. TWI and I44 are calculated indices, not direct exchange rates
7. RUB discontinued 2022-03-01; HRK discontinued 2022-12-30
8. Historical data: USD from 1960, EUR from 1999, policy rates from 1991
