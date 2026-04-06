#!/usr/bin/env python3
"""
SSB Data Fetcher -- CLI tool for Statistics Norway's PxWeb API v2.

Supports searching tables, fetching metadata, exploring codelists,
and querying data with automatic JSON-stat 2.0 parsing.
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import urllib.error
from itertools import product
from pathlib import Path

BASE_URL = "https://data.ssb.no/api/pxwebapi/v2"


def api_get(path: str, params: dict | None = None) -> dict | str:
    """Make a GET request to the SSB API."""
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read().decode("utf-8")
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return data
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def api_post(path: str, body: dict, params: dict | None = None) -> dict | bytes:
    """Make a POST request to the SSB API."""
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            content_type = resp.headers.get("Content-Type", "")
            if "json" in content_type:
                return json.loads(raw.decode("utf-8"))
            return raw
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def api_get_raw(path: str, params: dict | None = None) -> bytes:
    """Make a GET request and return raw bytes (for CSV, XLSX, etc.)."""
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


# --- JSON-stat 2.0 parsing ---

def jsonstat_to_records(js: dict) -> list[dict]:
    """Convert a JSON-stat 2.0 dataset to a list of flat records."""
    dim_ids = js["id"]
    sizes = js["size"]
    values = js["value"]
    dimensions = js["dimension"]

    # Build ordered labels for each dimension
    dim_labels = {}
    dim_codes = {}
    for dim_id in dim_ids:
        dim = dimensions[dim_id]
        cat = dim["category"]
        index = cat["index"]
        label_map = cat.get("label", {})
        # index can be {code: position} or [code, code, ...]
        if isinstance(index, dict):
            sorted_codes = sorted(index.keys(), key=lambda c: index[c])
        else:
            sorted_codes = index
        dim_codes[dim_id] = sorted_codes
        dim_labels[dim_id] = [label_map.get(c, c) for c in sorted_codes]

    # Compute strides for row-major indexing
    strides = []
    stride = 1
    for s in reversed(sizes):
        strides.append(stride)
        stride *= s
    strides.reverse()

    records = []
    total = 1
    for s in sizes:
        total *= s

    # Generate all combinations using product for efficiency
    code_lists = [dim_codes[d] for d in dim_ids]
    label_lists = [dim_labels[d] for d in dim_ids]

    for flat_idx, combo in enumerate(product(*[range(s) for s in sizes])):
        record = {}
        for i, dim_id in enumerate(dim_ids):
            record[f"{dim_id}_code"] = code_lists[i][combo[i]]
            record[dim_id] = label_lists[i][combo[i]]
        val = values[flat_idx] if flat_idx < len(values) else None
        record["value"] = val
        records.append(record)

    return records


def records_to_csv(records: list[dict], output_path: str | None = None) -> str:
    """Convert records to CSV string, optionally writing to file."""
    if not records:
        return ""
    headers = list(records[0].keys())
    lines = [",".join(headers)]
    for r in records:
        row = []
        for h in headers:
            v = r.get(h)
            if v is None:
                row.append("")
            elif isinstance(v, str):
                row.append(f'"{v}"')
            else:
                row.append(str(v))
        lines.append(",".join(row))
    csv_str = "\n".join(lines) + "\n"
    if output_path:
        Path(output_path).write_text(csv_str, encoding="utf-8")
        print(f"Wrote {len(records)} rows to {output_path}")
    return csv_str


# --- Commands ---

def cmd_search(args):
    """Search for tables."""
    params = {"lang": args.lang, "pageSize": args.limit, "pageNumber": 1}
    if args.query:
        params["query"] = args.query
    if args.past_days:
        params["pastDays"] = args.past_days
    if args.include_discontinued:
        params["includeDiscontinued"] = "true"

    result = api_get("/tables", params)
    tables = result.get("tables", [])
    page = result.get("page", {})

    print(f"Found {page.get('totalElements', '?')} tables (showing {len(tables)}):\n")
    for t in tables:
        updated = t.get("updated", "")[:10]
        period = f"{t.get('firstPeriod', '?')}-{t.get('lastPeriod', '?')}"
        variables = ", ".join(t.get("variableNames", []))
        print(f"  {t['id']:>8}  {t['label']}")
        print(f"           Period: {period}  |  Updated: {updated}  |  Unit: {t.get('timeUnit', '?')}")
        print(f"           Variables: {variables}")
        if t.get("paths"):
            path_labels = " > ".join(p["label"] for p in t["paths"][0])
            print(f"           Path: {path_labels}")
        print()

    if page.get("totalPages", 1) > 1:
        print(f"Page {page['pageNumber']} of {page['totalPages']}. Use --page N to see more.")


def cmd_metadata(args):
    """Show table metadata."""
    params = {"lang": args.lang}

    # First get table info
    info = api_get(f"/tables/{args.table_id}", params)
    print(f"Table {args.table_id}: {info.get('label', 'Unknown')}")
    print(f"  Source: {info.get('source', '?')}")
    print(f"  Period: {info.get('firstPeriod', '?')} - {info.get('lastPeriod', '?')}")
    print(f"  Updated: {info.get('updated', '?')[:10]}")
    print(f"  Time unit: {info.get('timeUnit', '?')}")
    if info.get("description"):
        print(f"  Description: {info['description']}")
    print()

    # Then get full metadata
    meta = api_get(f"/tables/{args.table_id}/metadata", params)
    dim_ids = meta.get("id", [])
    sizes = meta.get("size", [])
    dims = meta.get("dimension", {})
    roles = meta.get("role", {})

    # Compute total cells
    total_cells = 1
    for s in sizes:
        total_cells *= s
    print(f"  Total cells (full table): {total_cells:,}")
    print()

    # Show variables
    print("Variables:")
    for i, dim_id in enumerate(dim_ids):
        dim = dims.get(dim_id, {})
        cat = dim.get("category", {})
        ext = dim.get("extension", {})
        n_values = sizes[i]
        label = dim.get("label", dim_id)
        eliminatable = ext.get("elimination", False)
        codelists = ext.get("codelists", [])

        role_tags = []
        for role_name, role_vars in roles.items():
            if dim_id in role_vars:
                role_tags.append(role_name)

        role_str = f" [{', '.join(role_tags)}]" if role_tags else ""
        elim_str = " (eliminatable)" if eliminatable else ""

        print(f"\n  {dim_id}{role_str}{elim_str}")
        print(f"    Label: {label}")
        print(f"    Values: {n_values}")

        # Show first/last few values
        index = cat.get("index", {})
        label_map = cat.get("label", {})
        if isinstance(index, dict):
            codes = sorted(index.keys(), key=lambda c: index[c])
        else:
            codes = index

        if len(codes) <= 15:
            for code in codes:
                print(f"      {code}: {label_map.get(code, code)}")
        else:
            for code in codes[:5]:
                print(f"      {code}: {label_map.get(code, code)}")
            print(f"      ... ({len(codes) - 10} more) ...")
            for code in codes[-5:]:
                print(f"      {code}: {label_map.get(code, code)}")

        # Show units for ContentsCode
        units = cat.get("unit", {})
        if units:
            for code, unit in units.items():
                print(f"    Unit [{code}]: {unit.get('base', '?')} (decimals: {unit.get('decimals', '?')})")

        # Show codelists
        if codelists:
            print(f"    Codelists ({len(codelists)}):")
            for cl in codelists:
                print(f"      {cl['id']}: {cl['label']} ({cl['type']})")


def cmd_codelist(args):
    """Show codelist details."""
    params = {"lang": args.lang}
    cl = api_get(f"/codelists/{args.codelist_id}", params)
    print(f"Codelist: {cl.get('label', cl.get('id', '?'))}")
    print(f"  Type: {cl.get('type', '?')}")
    print(f"  Values:")
    for v in cl.get("values", []):
        value_map = v.get("valueMap", [])
        map_str = f" -> [{', '.join(value_map[:5])}{'...' if len(value_map) > 5 else ''}]" if value_map else ""
        print(f"    {v['code']}: {v['label']}{map_str}")


def cmd_data(args):
    """Fetch data from a table."""
    params = {"lang": args.lang}
    fmt = args.format or "json-stat2"

    format_params_list = []
    if args.codes_and_texts:
        format_params_list.append("UseCodesAndTexts")
    if args.format_params:
        format_params_list.extend(args.format_params.split(","))

    # Build query from --select args or --query file
    if args.query_file:
        query_body = json.loads(Path(args.query_file).read_text())
    elif args.select:
        selection = []
        for sel in args.select:
            parts = sel.split("=", 1)
            if len(parts) != 2:
                print(f"Invalid --select format: {sel}. Use VarCode=value1,value2", file=sys.stderr)
                sys.exit(1)
            var_code, values_str = parts
            # Check if a codelist is specified with @
            codelist = None
            if "@" in var_code:
                var_code, codelist = var_code.split("@", 1)
            value_codes = [v.strip() for v in values_str.split(",")]
            item = {"variableCode": var_code, "valueCodes": value_codes}
            if codelist:
                item["codelist"] = codelist
            selection.append(item)
        query_body = {"selection": selection}
    else:
        # No selection: use default
        query_body = None

    if query_body:
        # POST request
        params["outputFormat"] = fmt
        if format_params_list:
            params["outputFormatParams"] = ",".join(format_params_list)

        if fmt in ("json-stat2", "json-px"):
            result = api_post(f"/tables/{args.table_id}/data", query_body, params)
        else:
            # For CSV, XLSX etc., get raw bytes
            url = f"{BASE_URL}/tables/{args.table_id}/data"
            if params:
                url += "?" + urllib.parse.urlencode(params)
            data = json.dumps(query_body).encode("utf-8")
            req = urllib.request.Request(
                url, data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(req) as resp:
                    raw = resp.read()
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", errors="replace")
                print(f"HTTP {e.code}: {body}", file=sys.stderr)
                sys.exit(1)

            if args.output:
                Path(args.output).write_bytes(raw)
                print(f"Wrote output to {args.output}")
            else:
                try:
                    print(raw.decode("utf-8"))
                except UnicodeDecodeError:
                    print(f"Binary output ({len(raw)} bytes). Use --output to save to file.", file=sys.stderr)
            return
    else:
        # GET with defaults
        params["outputFormat"] = fmt
        if format_params_list:
            params["outputFormatParams"] = ",".join(format_params_list)
        if fmt in ("json-stat2", "json-px"):
            result = api_get(f"/tables/{args.table_id}/data", params)
        else:
            raw = api_get_raw(f"/tables/{args.table_id}/data", params)
            if args.output:
                Path(args.output).write_bytes(raw)
                print(f"Wrote output to {args.output}")
            else:
                try:
                    print(raw.decode("utf-8"))
                except UnicodeDecodeError:
                    print(f"Binary output ({len(raw)} bytes). Use --output to save to file.", file=sys.stderr)
            return

    # Handle json-stat2 result
    if fmt == "json-stat2" and isinstance(result, dict):
        if args.output and args.output.endswith(".json"):
            Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"Wrote JSON-stat 2.0 to {args.output}")
            return

        records = jsonstat_to_records(result)

        if args.output:
            records_to_csv(records, args.output)
        elif args.analyze:
            print_analysis(records, result)
        else:
            csv_str = records_to_csv(records)
            # Print first 50 lines as preview
            lines = csv_str.strip().split("\n")
            for line in lines[:50]:
                print(line)
            if len(lines) > 50:
                print(f"\n... ({len(lines) - 50} more rows, {len(records)} total)")
                print("Use --output file.csv to save all data.")
    elif isinstance(result, dict):
        output_str = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).write_text(output_str, encoding="utf-8")
            print(f"Wrote output to {args.output}")
        else:
            print(output_str)

    if args.analyze and fmt == "json-stat2" and isinstance(result, dict):
        pass  # Already handled above


def print_analysis(records: list[dict], js: dict):
    """Print summary statistics for the data."""
    if not records:
        print("No data.")
        return

    print(f"Dataset: {js.get('label', 'Unknown')}")
    print(f"Source: {js.get('source', '?')}")
    print(f"Updated: {js.get('updated', '?')}")
    print(f"Records: {len(records)}")
    print()

    # Extract numeric values
    values = [r["value"] for r in records if r["value"] is not None]
    if values:
        print(f"Value statistics:")
        print(f"  Count:   {len(values)}")
        print(f"  Min:     {min(values):,.2f}")
        print(f"  Max:     {max(values):,.2f}")
        print(f"  Mean:    {sum(values) / len(values):,.2f}")
        sorted_vals = sorted(values)
        mid = len(sorted_vals) // 2
        median = sorted_vals[mid] if len(sorted_vals) % 2 else (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
        print(f"  Median:  {median:,.2f}")
        nulls = sum(1 for r in records if r["value"] is None)
        if nulls:
            print(f"  Missing: {nulls}")
    print()

    # Show dimension summaries
    dim_ids = js.get("id", [])
    for dim_id in dim_ids:
        codes = sorted(set(r.get(dim_id, "") for r in records))
        if len(codes) <= 10:
            print(f"  {dim_id}: {', '.join(str(c) for c in codes)}")
        else:
            print(f"  {dim_id}: {len(codes)} unique values")


def cmd_default_selection(args):
    """Show default selection for a table."""
    params = {"lang": args.lang}
    result = api_get(f"/tables/{args.table_id}/defaultselection", params)
    print(f"Default selection for table {args.table_id}:\n")
    for sel in result.get("selection", []):
        codelist = sel.get("codelist")
        cl_str = f" (codelist: {codelist})" if codelist else ""
        values = sel.get("valueCodes", [])
        if len(values) <= 10:
            val_str = ", ".join(values)
        else:
            val_str = f"{', '.join(values[:5])}, ... ({len(values)} total)"
        print(f"  {sel['variableCode']}{cl_str}: {val_str}")


def cmd_config(args):
    """Show API configuration."""
    result = api_get("/config")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="SSB Data Fetcher -- query Statistics Norway's PxWeb API v2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s search "population" --lang en
  %(prog)s metadata 07459 --lang en
  %(prog)s codelist agg_FemAarigGruppering --lang en
  %(prog)s data 07459 --select "Region=0301" --select "Tid=top(5)" --lang en
  %(prog)s data 07459 --query query.json --format csv --output result.csv
        """,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # search
    p_search = sub.add_parser("search", help="Search for tables")
    p_search.add_argument("query", nargs="?", help="Search query")
    p_search.add_argument("--lang", default="en", help="Language (en/no)")
    p_search.add_argument("--limit", type=int, default=10, help="Max results")
    p_search.add_argument("--page", type=int, default=1, help="Page number")
    p_search.add_argument("--past-days", type=int, help="Updated within N days")
    p_search.add_argument("--include-discontinued", action="store_true")

    # metadata
    p_meta = sub.add_parser("metadata", help="Show table metadata")
    p_meta.add_argument("table_id", help="Table ID (e.g., 07459)")
    p_meta.add_argument("--lang", default="en", help="Language (en/no)")

    # codelist
    p_cl = sub.add_parser("codelist", help="Show codelist details")
    p_cl.add_argument("codelist_id", help="Codelist ID")
    p_cl.add_argument("--lang", default="en", help="Language (en/no)")

    # data
    p_data = sub.add_parser("data", help="Fetch data from a table")
    p_data.add_argument("table_id", help="Table ID (e.g., 07459)")
    p_data.add_argument("--select", action="append", help="Variable selection: VarCode=val1,val2 or VarCode@codelist=val1,val2")
    p_data.add_argument("--query", dest="query_file", help="Path to JSON query file")
    p_data.add_argument("--format", choices=["json-stat2", "csv", "xlsx", "html", "px", "json-px"], help="Output format")
    p_data.add_argument("--output", "-o", help="Output file path")
    p_data.add_argument("--lang", default="en", help="Language (en/no)")
    p_data.add_argument("--analyze", action="store_true", help="Print summary statistics")
    p_data.add_argument("--codes-and-texts", action="store_true", help="Include both codes and text labels")
    p_data.add_argument("--format-params", help="Comma-separated output format params")

    # defaultselection
    p_def = sub.add_parser("defaultselection", help="Show default selection for a table")
    p_def.add_argument("table_id", help="Table ID")
    p_def.add_argument("--lang", default="en", help="Language (en/no)")

    # config
    sub.add_parser("config", help="Show API configuration")

    args = parser.parse_args()

    commands = {
        "search": cmd_search,
        "metadata": cmd_metadata,
        "codelist": cmd_codelist,
        "data": cmd_data,
        "defaultselection": cmd_default_selection,
        "config": cmd_config,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
