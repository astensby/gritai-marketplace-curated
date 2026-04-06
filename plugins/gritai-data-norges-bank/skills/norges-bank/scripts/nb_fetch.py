#!/usr/bin/env python3
"""
Norges Bank Data Fetcher -- CLI tool for Norges Bank's SDMX REST API.

Supports listing datasets, exploring structure, fetching data series,
and parsing SDMX responses into clean CSV.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

BASE_URL = "https://data.norges-bank.no/api"


def api_get(path: str, params: dict | None = None, accept: str = "application/json") -> dict | str | bytes:
    """Make a GET request to the Norges Bank API."""
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept": accept})
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            content_type = resp.headers.get("Content-Type", "")
            if "json" in content_type:
                return json.loads(raw.decode("utf-8"))
            return raw
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def fetch_csv(path: str, params: dict | None = None) -> str:
    """Fetch CSV data from the API."""
    url = f"{BASE_URL}{path}"
    p = dict(params or {})
    p["format"] = "csv"
    p["locale"] = "en"
    url += "?" + urllib.parse.urlencode(p)
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def parse_semicolon_csv(raw_csv: str) -> list[dict]:
    """Parse Norges Bank semicolon-delimited CSV into records."""
    lines = raw_csv.strip().split("\n")
    if not lines:
        return []
    headers = [h.strip().strip('"') for h in lines[0].split(";")]
    records = []
    for line in lines[1:]:
        if not line.strip():
            continue
        values = [v.strip().strip('"') for v in line.split(";")]
        record = {}
        for i, h in enumerate(headers):
            record[h] = values[i] if i < len(values) else ""
        records.append(record)
    return records


def records_to_csv(records: list[dict], output_path: str | None = None) -> str:
    """Convert records to standard comma-delimited CSV."""
    if not records:
        return ""
    headers = list(records[0].keys())
    lines = [",".join(headers)]
    for r in records:
        row = []
        for h in headers:
            v = r.get(h, "")
            if "," in str(v) or '"' in str(v):
                row.append(f'"{v}"')
            else:
                row.append(str(v))
        lines.append(",".join(row))
    csv_str = "\n".join(lines) + "\n"
    if output_path:
        Path(output_path).write_text(csv_str, encoding="utf-8")
        print(f"Wrote {len(records)} rows to {output_path}")
    return csv_str


def apply_unit_mult(records: list[dict]) -> list[dict]:
    """Adjust OBS_VALUE by UNIT_MULT for exchange rates (per-unit normalization)."""
    for r in records:
        if "UNIT_MULT" in r and "OBS_VALUE" in r:
            try:
                mult = int(r["UNIT_MULT"])
                val = float(r["OBS_VALUE"])
                if mult > 0:
                    r["OBS_VALUE_RAW"] = r["OBS_VALUE"]
                    r["OBS_VALUE"] = str(round(val * (10 ** (-mult)), 6))
                    r["UNIT_NOTE"] = f"Adjusted from per-{10**mult} to per-unit"
            except (ValueError, TypeError):
                pass
    return records


# --- Commands ---

def cmd_datasets(args):
    """List all available datasets."""
    result = api_get("/dataflow/all/all/latest", {"format": "sdmx-json"})

    dataflows = []
    try:
        structures = result.get("data", result).get("dataflows", [])
        for df in structures:
            df_id = df.get("id", "?")
            names = df.get("name", df.get("names", "?"))
            if isinstance(names, dict):
                name = names.get("en", names.get("no", str(names)))
            elif isinstance(names, str):
                name = names
            else:
                name = str(names)
            dataflows.append((df_id, name))
    except (AttributeError, KeyError):
        # Fallback: try alternate structure
        try:
            for struct in result.get("data", {}).get("structures", []):
                df_id = struct.get("id", "?")
                name = struct.get("name", "?")
                dataflows.append((df_id, name))
        except (AttributeError, KeyError):
            print("Could not parse dataflow response.", file=sys.stderr)
            print(json.dumps(result, indent=2)[:2000])
            return

    dataflows.sort(key=lambda x: x[0])
    print(f"Available datasets ({len(dataflows)}):\n")
    for df_id, name in dataflows:
        print(f"  {df_id:30s} {name}")


def cmd_structure(args):
    """Show dataset structure (dimensions and values)."""
    result = api_get(f"/data/{args.dataset}", {"format": "sdmx-json", "detail": "serieskeysonly"})

    try:
        structure = result["data"]["structure"]
        dims = structure["dimensions"]["series"]
    except (KeyError, TypeError):
        print("Could not parse structure response.", file=sys.stderr)
        print(json.dumps(result, indent=2)[:3000])
        return

    print(f"Dataset: {args.dataset}")
    print(f"Key structure: {'.'.join(d['id'] for d in dims)}\n")
    print("Dimensions:\n")

    for dim in dims:
        dim_id = dim.get("id", "?")
        name = dim.get("name", dim_id)
        values = dim.get("values", [])
        print(f"  {dim_id} ({name}) -- {len(values)} values")
        if len(values) <= 20:
            for v in values:
                vid = v.get("id", "?")
                vname = v.get("name", vid)
                extra = ""
                if v.get("start"):
                    extra += f" [from {v['start']}]"
                if v.get("end"):
                    extra += f" [to {v['end']}]"
                print(f"    {vid}: {vname}{extra}")
        else:
            for v in values[:10]:
                vid = v.get("id", "?")
                vname = v.get("name", vid)
                print(f"    {vid}: {vname}")
            print(f"    ... ({len(values) - 10} more)")
        print()


def cmd_series(args):
    """List all series keys in a dataset."""
    result = api_get(f"/data/{args.dataset}", {"format": "sdmx-json", "detail": "serieskeysonly"})

    try:
        structure = result["data"]["structure"]
        dims = structure["dimensions"]["series"]
        datasets = result["data"]["dataSets"]
    except (KeyError, TypeError):
        print("Could not parse response.", file=sys.stderr)
        return

    dim_values = []
    for dim in dims:
        dim_values.append({str(i): v.get("id", "?") for i, v in enumerate(dim.get("values", []))})

    print(f"Series in {args.dataset}:\n")
    count = 0
    for ds in datasets:
        for series_key in sorted(ds.get("series", {}).keys()):
            indices = series_key.split(":")
            key_parts = []
            for i, idx in enumerate(indices):
                if i < len(dim_values):
                    key_parts.append(dim_values[i].get(idx, idx))
                else:
                    key_parts.append(idx)
            sdmx_key = ".".join(key_parts)
            print(f"  {sdmx_key}")
            count += 1
            if count >= 100:
                print(f"\n  ... (showing first 100, may have more)")
                return
    print(f"\nTotal: {count} series")


def cmd_data(args):
    """Fetch data from a dataset."""
    # Build URL path
    key = args.key if args.key else ""
    path = f"/data/{args.dataset}"
    if key:
        path += f"/{key}"

    params = {}
    if args.start:
        params["startPeriod"] = args.start
    if args.end:
        params["endPeriod"] = args.end
    if args.last:
        params["lastNObservations"] = str(args.last)
    if args.first:
        params["firstNObservations"] = str(args.first)

    fmt = args.format or "csv"

    if fmt == "sdmx-json":
        params["format"] = "sdmx-json"
        params["locale"] = "en"
        result = api_get(path, params)
        output_str = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).write_text(output_str, encoding="utf-8")
            print(f"Wrote SDMX-JSON to {args.output}")
        else:
            print(output_str[:5000])
            if len(output_str) > 5000:
                print(f"\n... ({len(output_str)} chars total, use --output to save)")
        return

    # CSV format
    raw_csv = fetch_csv(path, params)
    records = parse_semicolon_csv(raw_csv)

    if not records:
        print("No data returned.")
        return

    # Apply UNIT_MULT scaling for exchange rates
    if args.dataset == "EXR" and not args.raw:
        records = apply_unit_mult(records)

    if args.analyze:
        print_analysis(records, args.dataset, key)
        return

    if args.output:
        records_to_csv(records, args.output)
    else:
        # Print as clean CSV to stdout
        csv_str = records_to_csv(records)
        lines = csv_str.strip().split("\n")
        for line in lines[:50]:
            print(line)
        if len(lines) > 50:
            print(f"\n... ({len(lines) - 50} more rows, {len(records)} total)")
            print("Use --output file.csv to save all data.")


def print_analysis(records: list[dict], dataset: str, key: str):
    """Print summary statistics."""
    if not records:
        print("No data.")
        return

    print(f"Dataset: {dataset}")
    if key:
        print(f"Key: {key}")
    print(f"Records: {len(records)}")
    print()

    # Extract numeric values
    obs_values = []
    for r in records:
        try:
            v = float(r.get("OBS_VALUE", ""))
            obs_values.append(v)
        except (ValueError, TypeError):
            pass

    if obs_values:
        print(f"OBS_VALUE statistics:")
        print(f"  Count:   {len(obs_values)}")
        print(f"  Min:     {min(obs_values):,.4f}")
        print(f"  Max:     {max(obs_values):,.4f}")
        print(f"  Mean:    {sum(obs_values) / len(obs_values):,.4f}")
        sorted_vals = sorted(obs_values)
        mid = len(sorted_vals) // 2
        median = sorted_vals[mid] if len(sorted_vals) % 2 else (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
        print(f"  Median:  {median:,.4f}")
        if len(obs_values) >= 2:
            print(f"  First:   {obs_values[0]:,.4f}")
            print(f"  Last:    {obs_values[-1]:,.4f}")
            change = obs_values[-1] - obs_values[0]
            pct = (change / obs_values[0]) * 100 if obs_values[0] != 0 else 0
            print(f"  Change:  {change:+,.4f} ({pct:+.2f}%)")
    print()

    # Show time range
    periods = [r.get("TIME_PERIOD", "") for r in records if r.get("TIME_PERIOD")]
    if periods:
        print(f"  Period: {min(periods)} to {max(periods)}")

    # Show unique dimension values
    skip_cols = {"TIME_PERIOD", "OBS_VALUE", "OBS_VALUE_RAW", "UNIT_NOTE", "OBS_STATUS", "OBS_CONF", "OBS_PRE_BREAK"}
    for col in records[0]:
        if col in skip_cols:
            continue
        unique = sorted(set(r.get(col, "") for r in records))
        if 1 < len(unique) <= 10:
            print(f"  {col}: {', '.join(unique)}")
        elif len(unique) > 10:
            print(f"  {col}: {len(unique)} unique values")


def main():
    parser = argparse.ArgumentParser(
        description="Norges Bank Data Fetcher -- query the SDMX REST API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s datasets
  %(prog)s structure EXR
  %(prog)s series EXR
  %(prog)s data EXR B.USD.NOK.SP --last 10
  %(prog)s data EXR B.USD+EUR+GBP.NOK.SP --start 2024-01-01 --end 2024-12-31 --output rates.csv
  %(prog)s data IR B.KPRA..R --start 2020-01-01 --analyze
  %(prog)s data ANN_KPRA KPRA --last 10
        """,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # datasets
    sub.add_parser("datasets", help="List all available datasets")

    # structure
    p_struct = sub.add_parser("structure", help="Show dataset structure")
    p_struct.add_argument("dataset", help="Dataset ID (e.g., EXR, IR)")

    # series
    p_series = sub.add_parser("series", help="List series keys in a dataset")
    p_series.add_argument("dataset", help="Dataset ID")

    # data
    p_data = sub.add_parser("data", help="Fetch data from a dataset")
    p_data.add_argument("dataset", help="Dataset ID (e.g., EXR, IR)")
    p_data.add_argument("key", nargs="?", default="", help="SDMX key (e.g., B.USD.NOK.SP)")
    p_data.add_argument("--start", help="Start period (e.g., 2024-01-01)")
    p_data.add_argument("--end", help="End period (e.g., 2024-12-31)")
    p_data.add_argument("--last", type=int, help="Last N observations per series")
    p_data.add_argument("--first", type=int, help="First N observations per series")
    p_data.add_argument("--format", choices=["csv", "sdmx-json"], default="csv", help="Output format")
    p_data.add_argument("--output", "-o", help="Output file path")
    p_data.add_argument("--analyze", action="store_true", help="Print summary statistics")
    p_data.add_argument("--raw", action="store_true", help="Skip UNIT_MULT adjustment for EXR")

    args = parser.parse_args()

    commands = {
        "datasets": cmd_datasets,
        "structure": cmd_structure,
        "series": cmd_series,
        "data": cmd_data,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
