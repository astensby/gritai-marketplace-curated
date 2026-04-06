#!/usr/bin/env python3
"""
BRREG Company Fetcher -- CLI tool for Brønnøysundregistrene APIs.

Supports searching companies, looking up by org number, fetching roles
(board/CEO), financial statements, and sub-entities.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

BASE_ENH = "https://data.brreg.no/enhetsregisteret/api"
BASE_REG = "https://data.brreg.no/regnskapsregisteret/regnskap"


def api_get(url: str) -> dict | list | None:
    """Make a GET request, return parsed JSON."""
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        body = e.read().decode("utf-8", errors="replace")[:500]
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def records_to_csv(records: list[dict], output_path: str | None = None) -> str:
    """Convert records to CSV string, optionally writing to file."""
    if not records:
        return ""
    headers = list(records[0].keys())
    lines = [",".join(headers)]
    for r in records:
        row = []
        for h in headers:
            v = r.get(h, "")
            if v is None:
                v = ""
            v = str(v)
            if "," in v or '"' in v or "\n" in v:
                v = '"' + v.replace('"', '""') + '"'
            row.append(v)
        lines.append(",".join(row))
    csv_str = "\n".join(lines) + "\n"
    if output_path:
        Path(output_path).write_text(csv_str, encoding="utf-8")
        print(f"Wrote {len(records)} rows to {output_path}")
    return csv_str


def flatten_entity(e: dict) -> dict:
    """Flatten an entity JSON into a flat record for CSV output."""
    addr = e.get("forretningsadresse", {}) or {}
    post = e.get("postadresse", {}) or {}
    nace1 = e.get("naeringskode1", {}) or {}
    nace2 = e.get("naeringskode2", {}) or {}
    orgform = e.get("organisasjonsform", {}) or {}
    sektor = e.get("institusjonellSektorkode", {}) or {}
    kap = e.get("kapital", {}) or {}

    return {
        "organisasjonsnummer": e.get("organisasjonsnummer", ""),
        "navn": e.get("navn", ""),
        "organisasjonsform": orgform.get("kode", ""),
        "organisasjonsform_beskrivelse": orgform.get("beskrivelse", ""),
        "stiftelsesdato": e.get("stiftelsesdato", ""),
        "registreringsdato": e.get("registreringsdatoEnhetsregisteret", ""),
        "antall_ansatte": e.get("antallAnsatte", ""),
        "hjemmeside": e.get("hjemmeside", ""),
        "naeringskode1": nace1.get("kode", ""),
        "naeringskode1_beskrivelse": nace1.get("beskrivelse", ""),
        "naeringskode2": nace2.get("kode", ""),
        "kommune": addr.get("kommune", ""),
        "kommunenummer": addr.get("kommunenummer", ""),
        "poststed": addr.get("poststed", ""),
        "postnummer": addr.get("postnummer", ""),
        "adresse": ", ".join(addr.get("adresse", [])),
        "sektorkode": sektor.get("kode", ""),
        "sektorbeskrivelse": sektor.get("beskrivelse", ""),
        "konkurs": e.get("konkurs", False),
        "under_avvikling": e.get("underAvvikling", False),
        "registrert_mva": e.get("registrertIMvaregisteret", False),
        "registrert_foretaksregisteret": e.get("registrertIForetaksregisteret", False),
        "siste_aarsregnskap": e.get("sisteInnsendteAarsregnskap", ""),
        "aksjekapital": kap.get("belop", ""),
        "antall_aksjer": kap.get("antallAksjer", ""),
        "er_i_konsern": e.get("erIKonsern", False),
    }


def flatten_financial(f: dict) -> dict:
    """Flatten a financial statement JSON into a flat record."""
    virk = f.get("virksomhet", {}) or {}
    periode = f.get("regnskapsperiode", {}) or {}
    resultat = f.get("resultatregnskapResultat", {}) or {}
    drift = resultat.get("driftsresultat", {}) or {}
    driftsinnt = drift.get("driftsinntekter", {}) or {}
    driftskost = drift.get("driftskostnad", {}) or {}
    finans = resultat.get("finansresultat", {}) or {}
    eiendeler = f.get("eiendeler", {}) or {}
    ekgjeld = f.get("egenkapitalGjeld", {}) or {}
    ek = ekgjeld.get("egenkapital", {}) or {}
    gjeld = ekgjeld.get("gjeldOversikt", {}) or {}

    return {
        "organisasjonsnummer": virk.get("organisasjonsnummer", ""),
        "regnskapstype": f.get("regnskapstype", ""),
        "fra_dato": periode.get("fraDato", ""),
        "til_dato": periode.get("tilDato", ""),
        "valuta": f.get("valuta", ""),
        "oppstillingsplan": f.get("oppstillingsplan", ""),
        "sum_driftsinntekter": driftsinnt.get("sumDriftsinntekter", ""),
        "sum_driftskostnad": driftskost.get("sumDriftskostnad", ""),
        "driftsresultat": drift.get("driftsresultat", ""),
        "netto_finans": finans.get("nettoFinans", ""),
        "resultat_for_skatt": resultat.get("ordinaertResultatFoerSkattekostnad", ""),
        "aarsresultat": resultat.get("aarsresultat", ""),
        "sum_eiendeler": eiendeler.get("sumEiendeler", ""),
        "sum_egenkapital": ek.get("sumEgenkapital", ""),
        "sum_gjeld": gjeld.get("sumGjeld", ""),
        "kortsiktig_gjeld": gjeld.get("kortsiktigGjeld", {}).get("sumKortsiktigGjeld", "") if isinstance(gjeld.get("kortsiktigGjeld"), dict) else "",
        "langsiktig_gjeld": gjeld.get("langsiktigGjeld", {}).get("sumLangsiktigGjeld", "") if isinstance(gjeld.get("langsiktigGjeld"), dict) else "",
    }


# --- Commands ---

def cmd_search(args):
    """Search for companies."""
    params = {}
    if args.name:
        name = args.name.upper() if args.ignore_case else args.name
        params["navn"] = name
    if args.orgform:
        params["organisasjonsform"] = args.orgform
    if args.kommune:
        params["kommunenummer"] = args.kommune
    if args.nace:
        params["naeringskode"] = args.nace
    if args.konkurs:
        params["konkurs"] = "true"
    if args.under_avvikling:
        params["underAvvikling"] = "true"
    if args.registered_after:
        params["fraRegistreringsdatoEnhetsregisteret"] = args.registered_after
    if args.registered_before:
        params["tilRegistreringsdatoEnhetsregisteret"] = args.registered_before
    if args.mva:
        params["registrertIMvaregisteret"] = "true"
    if args.sort:
        params["sort"] = args.sort
    params["size"] = str(args.size)
    params["page"] = str(args.page)

    url = f"{BASE_ENH}/enheter?" + urllib.parse.urlencode(params)
    result = api_get(url)

    if not result:
        print("No results.")
        return

    embedded = result.get("_embedded", {})
    entities = embedded.get("enheter", [])
    page_info = result.get("page", {})

    total = page_info.get("totalElements", 0)
    print(f"Found {total} companies (showing {len(entities)}):\n")

    records = []
    for e in entities:
        flat = flatten_entity(e)
        records.append(flat)
        nace = flat["naeringskode1_beskrivelse"] or flat["naeringskode1"]
        emp = flat["antall_ansatte"]
        emp_str = f"  |  Employees: {emp}" if emp else ""
        print(f"  {flat['organisasjonsnummer']:>10}  {flat['navn']}")
        print(f"             {flat['organisasjonsform']}  |  {flat['kommune'] or flat['poststed']}{emp_str}")
        if nace:
            print(f"             Industry: {nace}")
        print()

    if total > len(entities):
        total_pages = page_info.get("totalPages", "?")
        current = page_info.get("number", 0)
        print(f"Page {current} of {total_pages}. Use --page N to see more.")

    if args.output and records:
        records_to_csv(records, args.output)


def cmd_lookup(args):
    """Look up companies by org number."""
    records = []
    for org_nr in args.org_numbers:
        url = f"{BASE_ENH}/enheter/{org_nr}"
        result = api_get(url)
        if result is None:
            print(f"  {org_nr}: Not found", file=sys.stderr)
            continue

        flat = flatten_entity(result)
        records.append(flat)

        print(f"\n{'='*60}")
        print(f"  {flat['navn']} ({flat['organisasjonsnummer']})")
        print(f"{'='*60}")
        print(f"  Org form:      {flat['organisasjonsform']} ({flat['organisasjonsform_beskrivelse']})")
        print(f"  Founded:       {flat['stiftelsesdato']}")
        print(f"  Registered:    {flat['registreringsdato']}")
        print(f"  Employees:     {flat['antall_ansatte'] or 'Not reported'}")
        print(f"  Municipality:  {flat['kommune']} ({flat['kommunenummer']})")
        print(f"  Address:       {flat['adresse']}, {flat['postnummer']} {flat['poststed']}")
        if flat['hjemmeside']:
            print(f"  Website:       {flat['hjemmeside']}")
        print(f"  NACE 1:        {flat['naeringskode1']} ({flat['naeringskode1_beskrivelse']})")
        if flat['naeringskode2']:
            print(f"  NACE 2:        {flat['naeringskode2']}")
        print(f"  Sector:        {flat['sektorkode']} ({flat['sektorbeskrivelse']})")
        if flat['aksjekapital']:
            print(f"  Share capital: {flat['aksjekapital']:,} NOK ({flat['antall_aksjer']:,} shares)" if flat['antall_aksjer'] else f"  Share capital: {flat['aksjekapital']:,} NOK")
        print(f"  In group:      {flat['er_i_konsern']}")
        print(f"  VAT reg:       {flat['registrert_mva']}")
        print(f"  Bankruptcy:    {flat['konkurs']}")
        print(f"  Latest accts:  {flat['siste_aarsregnskap']}")

        # Show purposes if available
        purposes = result.get("vedtektsfestetFormaal", [])
        if purposes:
            print(f"  Purpose:       {purposes[0][:100]}{'...' if len(purposes[0]) > 100 else ''}")

    if args.output and records:
        records_to_csv(records, args.output)


def cmd_roles(args):
    """Get roles (board, CEO, auditor) for a company."""
    url = f"{BASE_ENH}/enheter/{args.org_number}/roller"
    result = api_get(url)

    if not result:
        print(f"No roles found for {args.org_number}.")
        return

    groups = result.get("rollegrupper", [])
    records = []

    for group in groups:
        group_type = group.get("type", {})
        group_code = group_type.get("kode", "")
        group_desc = group_type.get("beskrivelse", "")

        for role in group.get("roller", []):
            role_type = role.get("type", {})
            role_code = role_type.get("kode", "")
            role_desc = role_type.get("beskrivelse", "")

            person = role.get("person", {})
            enhet = role.get("enhet", {})

            if person:
                navn = person.get("navn", {})
                name = f"{navn.get('fornavn', '')} {navn.get('mellomnavn', '') or ''} {navn.get('etternavn', '')}".strip()
                name = " ".join(name.split())  # clean double spaces
                birth = person.get("fodselsdato", "")
            elif enhet:
                name = enhet.get("organisasjonsnummer", "") + " " + " ".join(enhet.get("navn", []))
                birth = ""
            else:
                name = "Unknown"
                birth = ""

            fratraadt = role.get("fratraadt", False)

            record = {
                "organisasjonsnummer": args.org_number,
                "role_group": group_code,
                "role_group_desc": group_desc,
                "role_code": role_code,
                "role_desc": role_desc,
                "name": name,
                "birth_date": birth,
                "is_entity": bool(enhet),
                "resigned": fratraadt,
            }
            records.append(record)

    # Print
    current_group = None
    for r in records:
        if r["role_group"] != current_group:
            current_group = r["role_group"]
            print(f"\n  {r['role_group_desc']} ({r['role_group']}):")
        status = " (resigned)" if r["resigned"] else ""
        print(f"    {r['role_code']:5s} {r['role_desc']:25s} {r['name']}{status}")

    print(f"\n  Total: {len(records)} roles")

    if args.output and records:
        records_to_csv(records, args.output)


def cmd_financials(args):
    """Get financial statements."""
    records = []
    for org_nr in args.org_numbers:
        url = f"{BASE_REG}/{org_nr}"
        result = api_get(url)

        if not result:
            print(f"  {org_nr}: No financial statements found.", file=sys.stderr)
            continue

        statements = result if isinstance(result, list) else [result]
        for stmt in statements:
            flat = flatten_financial(stmt)
            flat["organisasjonsnummer"] = org_nr
            records.append(flat)

            print(f"\n  {org_nr} -- {flat['regnskapstype']} ({flat['fra_dato']} to {flat['til_dato']})")
            print(f"  Plan: {flat['oppstillingsplan']}  |  Currency: {flat['valuta']}")
            print(f"  Revenue:           {_fmt(flat['sum_driftsinntekter'])}")
            print(f"  Operating costs:   {_fmt(flat['sum_driftskostnad'])}")
            print(f"  Operating profit:  {_fmt(flat['driftsresultat'])}")
            print(f"  Net financials:    {_fmt(flat['netto_finans'])}")
            print(f"  Pre-tax result:    {_fmt(flat['resultat_for_skatt'])}")
            print(f"  Net income:        {_fmt(flat['aarsresultat'])}")
            print(f"  Total assets:      {_fmt(flat['sum_eiendeler'])}")
            print(f"  Equity:            {_fmt(flat['sum_egenkapital'])}")
            print(f"  Total debt:        {_fmt(flat['sum_gjeld'])}")

    if args.output and records:
        records_to_csv(records, args.output)


def _fmt(val):
    """Format a number for display."""
    if val == "" or val is None:
        return "N/A"
    try:
        return f"{int(val):>15,}"
    except (ValueError, TypeError):
        return str(val)


def cmd_subunits(args):
    """Get sub-entities for a company."""
    params = {"overordnetEnhet": args.org_number, "size": str(args.size)}
    url = f"{BASE_ENH}/underenheter?" + urllib.parse.urlencode(params)
    result = api_get(url)

    if not result:
        print(f"No sub-entities found for {args.org_number}.")
        return

    embedded = result.get("_embedded", {})
    subs = embedded.get("underenheter", [])
    page_info = result.get("page", {})
    total = page_info.get("totalElements", 0)

    print(f"Found {total} sub-entities (showing {len(subs)}):\n")

    records = []
    for s in subs:
        addr = s.get("beliggenhetsadresse", {}) or {}
        nace = s.get("naeringskode1", {}) or {}
        record = {
            "organisasjonsnummer": s.get("organisasjonsnummer", ""),
            "navn": s.get("navn", ""),
            "overordnet_enhet": s.get("overordnetEnhet", ""),
            "kommune": addr.get("kommune", ""),
            "kommunenummer": addr.get("kommunenummer", ""),
            "poststed": addr.get("poststed", ""),
            "naeringskode": nace.get("kode", ""),
            "naeringsbeskrivelse": nace.get("beskrivelse", ""),
            "antall_ansatte": s.get("antallAnsatte", ""),
        }
        records.append(record)
        print(f"  {record['organisasjonsnummer']:>10}  {record['navn']}")
        print(f"             {record['kommune']}  |  {record['naeringsbeskrivelse']}")
        if record['antall_ansatte']:
            print(f"             Employees: {record['antall_ansatte']}")
        print()

    if args.output and records:
        records_to_csv(records, args.output)


def main():
    parser = argparse.ArgumentParser(
        description="BRREG Company Fetcher -- query Brønnøysundregistrene",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s search --name "EQUINOR"
  %(prog)s search --nace "62" --kommune 0301 --orgform AS --size 20
  %(prog)s lookup 923609016
  %(prog)s roles 923609016
  %(prog)s financials 923609016 914778271
  %(prog)s subunits 923609016 --size 50
        """,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # search
    p_search = sub.add_parser("search", help="Search for companies")
    p_search.add_argument("--name", help="Company name (case-sensitive, use uppercase)")
    p_search.add_argument("--orgform", help="Organization form (AS, ASA, ENK, etc.)")
    p_search.add_argument("--kommune", help="Municipality code (e.g., 0301 for Oslo)")
    p_search.add_argument("--nace", help="NACE industry code (e.g., 62 or 06.100)")
    p_search.add_argument("--konkurs", action="store_true", help="In bankruptcy")
    p_search.add_argument("--under-avvikling", action="store_true", help="Under liquidation")
    p_search.add_argument("--registered-after", help="Registered after date (yyyy-MM-dd)")
    p_search.add_argument("--registered-before", help="Registered before date (yyyy-MM-dd)")
    p_search.add_argument("--mva", action="store_true", help="VAT registered")
    p_search.add_argument("--ignore-case", action="store_true", help="Auto-uppercase name search")
    p_search.add_argument("--size", type=int, default=20, help="Results per page (default 20)")
    p_search.add_argument("--page", type=int, default=0, help="Page number (0-based)")
    p_search.add_argument("--sort", help="Sort: field,direction (e.g., stiftelsesdato,desc)")
    p_search.add_argument("--output", "-o", help="Save results to CSV")

    # lookup
    p_lookup = sub.add_parser("lookup", help="Look up companies by org number")
    p_lookup.add_argument("org_numbers", nargs="+", help="Organization number(s)")
    p_lookup.add_argument("--output", "-o", help="Save to CSV")

    # roles
    p_roles = sub.add_parser("roles", help="Get roles (board, CEO, auditor)")
    p_roles.add_argument("org_number", help="Organization number")
    p_roles.add_argument("--output", "-o", help="Save to CSV")

    # financials
    p_fin = sub.add_parser("financials", help="Get financial statements")
    p_fin.add_argument("org_numbers", nargs="+", help="Organization number(s)")
    p_fin.add_argument("--output", "-o", help="Save to CSV")

    # subunits
    p_sub = sub.add_parser("subunits", help="Get sub-entities (branches)")
    p_sub.add_argument("org_number", help="Parent organization number")
    p_sub.add_argument("--size", type=int, default=20, help="Results per page")
    p_sub.add_argument("--output", "-o", help="Save to CSV")

    args = parser.parse_args()

    commands = {
        "search": cmd_search,
        "lookup": cmd_lookup,
        "roles": cmd_roles,
        "financials": cmd_financials,
        "subunits": cmd_subunits,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
