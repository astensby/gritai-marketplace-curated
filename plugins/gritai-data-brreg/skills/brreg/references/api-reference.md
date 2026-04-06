# BRREG API -- Complete Reference

**Entity Registry**: `https://data.brreg.no/enhetsregisteret/api/`  
**Financial Statements**: `https://data.brreg.no/regnskapsregisteret/regnskap/`  
**Auth**: None required (open data)  
**Format**: JSON  
**Pagination**: Spring Data style, 0-based, max 10,000 results

## Table of Contents

1. [Entity Search](#entity-search)
2. [Entity Lookup](#entity-lookup)
3. [Sub-entities](#sub-entities)
4. [Roles](#roles)
5. [Financial Statements](#financial-statements)
6. [Organization Forms](#organization-forms)
7. [Municipalities](#municipalities)
8. [Update Feed](#update-feed)
9. [Pagination](#pagination)
10. [Entity JSON Structure](#entity-json-structure)
11. [Financial Statement Structure](#financial-statement-structure)
12. [Error Handling](#error-handling)
13. [Gotchas](#gotchas)

---

## Entity Search

**GET /enhetsregisteret/api/enheter**

| Parameter | Type | Description |
|-----------|------|-------------|
| `navn` | string | Name search (case-sensitive, substring match) |
| `organisasjonsnummer` | string | Org number (comma-separated for multiple) |
| `organisasjonsform` | string | Org form code: AS, ASA, ENK, NUF, etc. |
| `kommunenummer` | string | Municipality code (0301=Oslo) |
| `naeringskode` | string | NACE code: 2-digit (`62`) or 5-char (`06.100`) |
| `konkurs` | boolean | In bankruptcy |
| `underAvvikling` | boolean | Under liquidation |
| `underTvangsavviklingEllerTvangsopplosning` | boolean | Under forced dissolution |
| `registrertIForetaksregisteret` | boolean | In Register of Business Enterprises |
| `registrertIMvaregisteret` | boolean | Registered for VAT |
| `registrertIStiftelsesregisteret` | boolean | In Foundation Registry |
| `registrertIFrivillighetsregisteret` | boolean | In Volunteer Registry |
| `fraRegistreringsdatoEnhetsregisteret` | date | Registered after (yyyy-MM-dd) |
| `tilRegistreringsdatoEnhetsregisteret` | date | Registered before |
| `fraStiftelsesdato` | date | Founded after |
| `forretningsadresse.kommunenummer` | string | Business address municipality |
| `hjemmeside` | string | Website |
| `institusjonellSektorkode` | string | Institutional sector code |
| `page` | int | Page number (0-based) |
| `size` | int | Page size (default 20) |
| `sort` | string | Sort: `field,direction` (e.g., `navn,asc`) |

All parameters combine with AND logic.

---

## Entity Lookup

**GET /enhetsregisteret/api/enheter/{orgNummer}**

Returns full entity JSON or 404. Deleted entities return with `slettedato` field.

---

## Sub-entities

**Search**: `GET /enhetsregisteret/api/underenheter?{params}`
- Same filters as enheter, plus `overordnetEnhet` (parent org number)
- Org forms: `BEDR` (business sub-unit), `AAFY` (non-business sub-unit)

**Lookup**: `GET /enhetsregisteret/api/underenheter/{orgNummer}`

---

## Roles

**GET /enhetsregisteret/api/enheter/{orgNummer}/roller**

Returns `rollegrupper[]`, each with `type` and `roller[]`:

```json
{
  "rollegrupper": [
    {
      "type": {"kode": "STYR", "beskrivelse": "Styre"},
      "roller": [
        {
          "type": {"kode": "LEDE", "beskrivelse": "Styrets leder"},
          "person": {
            "fodselsdato": "1965-01-15",
            "navn": {"fornavn": "OLA", "etternavn": "NORDMANN"}
          },
          "fratraadt": false
        }
      ]
    }
  ]
}
```

**Key role codes:**
| Code | Description (NO) | Description (EN) |
|------|-------------------|-------------------|
| DAGL | Daglig leder | CEO |
| LEDE | Styrets leder | Chair of the Board |
| MEDL | Styremedlem | Board member |
| NEST | Nestleder | Deputy chair |
| VARA | Varamedlem | Alternate member |
| REVI | Revisor | Auditor |
| REGN | Regnskapsfører | Accountant |
| INNH | Innehaver | Owner (sole prop.) |

Auditors (`REVI`) reference an `enhet` (company) not a person.

**Reference endpoints:**
- `GET /enhetsregisteret/api/roller/rollegruppetyper`
- `GET /enhetsregisteret/api/roller/rolletyper`

---

## Financial Statements

**GET /regnskapsregisteret/regnskap/{orgNummer}**

Returns JSON array of financial statement objects (currently only latest year).

**GET /regnskapsregisteret/regnskap/{orgNummer}/{id}** -- single statement by ID.

**Limitations:**
- Only latest filed year available
- Bank accounts not supported (returns 500)
- Small companies use simplified format (`oppstillingsplan: smaa`)

---

## Organization Forms

**GET /enhetsregisteret/api/organisasjonsformer** -- all 44 forms  
**GET /enhetsregisteret/api/organisasjonsformer/enheter** -- forms for main entities  
**GET /enhetsregisteret/api/organisasjonsformer/underenheter** -- AAFY, BEDR

Key codes: `AS` (private limited), `ASA` (public limited), `ENK` (sole proprietorship), `NUF` (foreign entity), `SA` (cooperative), `STI` (foundation), `DA` (general partnership), `ANS`, `KS`.

---

## Municipalities

**GET /enhetsregisteret/api/kommuner** -- 365 municipalities, paginated.

---

## Update Feed

**GET /enhetsregisteret/api/oppdateringer/enheter?dato={ISO-datetime}&size={n}**

Date format: `2026-04-01T00:00:00.000Z` (full ISO required).

Returns: `oppdateringsid`, `dato`, `organisasjonsnummer`, `endringstype` (Endring/Sletting/Ny).

---

## Pagination

All list endpoints:
- `page` -- 0-based page number
- `size` -- items per page (default 20)
- **Hard cap: `size * (page + 1) <= 10,000`**
- `sort` -- `field,direction` (e.g., `stiftelsesdato,desc`)

Response includes:
```json
"page": {"size": 20, "totalElements": 205031, "totalPages": 10252, "number": 0}
```

---

## Entity JSON Structure

```
organisasjonsnummer, navn
organisasjonsform{kode, beskrivelse}
hjemmeside, telefon, epostadresse
forretningsadresse{land, landkode, postnummer, poststed, adresse[], kommune, kommunenummer}
postadresse{...}
stiftelsesdato, registreringsdatoEnhetsregisteret
naeringskode1{kode, beskrivelse}
naeringskode2{kode, beskrivelse}
naeringskode3{kode, beskrivelse}
antallAnsatte, harRegistrertAntallAnsatte
institusjonellSektorkode{kode, beskrivelse}
registrertIForetaksregisteret (boolean)
registrertIMvaregisteret (boolean)
sisteInnsendteAarsregnskap (year string)
konkurs, underAvvikling, underTvangsavviklingEllerTvangsopplosning (booleans)
vedtektsfestetFormaal[] (purpose clauses)
aktivitet[]
erIKonsern (boolean)
kapital{belop, antallAksjer, type, valuta, innfortDato}
```

---

## Financial Statement Structure

```
regnskapstype: "SELSKAP" or "KONSERN"
regnskapsperiode{fraDato, tilDato}
valuta, oppstillingsplan ("store" or "smaa")

resultatregnskapResultat:
  aarsresultat (net income)
  ordinaertResultatFoerSkattekostnad
  driftsresultat:
    driftsresultat (operating profit)
    driftsinntekter{sumDriftsinntekter} (revenue)
    driftskostnad{sumDriftskostnad}
  finansresultat:
    nettoFinans
    finansinntekt{sumFinansinntekter}
    finanskostnad{sumFinanskostnad}

eiendeler:
  sumEiendeler (total assets)
  omloepsmidler{sumOmloepsmidler} (current assets)
  anleggsmidler{sumAnleggsmidler} (fixed assets)

egenkapitalGjeld:
  sumEgenkapitalGjeld
  egenkapital{sumEgenkapital} (total equity)
  gjeldOversikt{sumGjeld, kortsiktigGjeld{sumKortsiktigGjeld}, langsiktigGjeld{sumLangsiktigGjeld}}
```

---

## Error Handling

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 400 | Validation error (structured JSON with `valideringsfeil`) |
| 404 | Not found |
| 500 | Server error (e.g., bank accounts in regnskapsregisteret) |

---

## Gotchas

1. **Name search is case-sensitive** -- "EQUINOR" ≠ "equinor". Use uppercase.
2. **NACE codes**: Use `62` (2-digit) or `06.100` (5-char with dot). `62.010` or `62.01` return 0.
3. **Pagination cap at 10,000** -- narrow filters if needed.
4. **Financial statements**: Only latest year. Banks return 500. ENK don't file.
5. **Update feed**: Requires full ISO datetime, not just date.
6. **`antallAnsatte`**: Self-reported, often 0 even for large companies.
7. **Deleted entities**: Still accessible but have `slettedato` field.
