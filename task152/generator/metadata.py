"""Write task152/metadata.json from the built pack."""
import json
import os

import docs as DOC
import records as R

SOURCES = {
    R.F_OLD: "Hadley Ranch Solar, original SCADA daily report export",
    R.F_NEW: "Hadley Ranch Solar, replacement SCADA daily export",
    R.F_TAGS: "Hadley Ranch Solar, SCADA tag crosswalk",
    R.F_HOURLY: "Hadley Ranch Solar, block data loggers' hourly inverter AC export, 2025",
    R.F_MET: "Hadley Ranch Solar, meteorological station hourly export, 2025",
    R.F_EVENTS: "Hadley Ranch Solar, inverter alarm and event log, 2025",
    R.F_WO: "Tresco Field Services, CMMS work order export for Hadley Ranch Solar",
    R.F_LEGACY: "Vado Seco Irrigation and Power District, legacy billing system daily export for account 7731-0459",
    R.F_MDM: "Vado Seco Irrigation and Power District, meter data system daily export for account 7731-0459",
    R.F_SP: "Vado Seco Irrigation and Power District, service points on account 7731-0459",
    R.F_BLOTTER: "Marden-Vail Building Products, energy and commodities desk forward blotter",
    R.F_LT: "Clearfield Solar Resource, site-adapted hourly irradiance series for Hadley Ranch Solar",
    R.F_CURVE: "Marden-Vail Building Products, desk forward marks for Palo Verde, calendar 2027",
    DOC.F_POLICY: "Marden-Vail Building Products, treasury energy risk policy, revision 4",
    DOC.F_SCOPE: "Marden-Vail Building Products, module replacement scope and schedule",
    DOC.F_OM: "Tresco Field Services and Marden-Vail Building Products, O&M agreement schedules 2 and 4",
    DOC.F_EXHIBIT: "Vado Seco Irrigation and Power District, interconnection agreement exhibit C (metering)",
    DOC.F_RIG: "Corvane Solar, field applications report FA-2026-114",
    DOC.F_SHEETS: "Kellerman Solar and Corvane Solar module datasheets",
    DOC.F_CONF: "Westmark Power Trading, confirmations file",
    DOC.F_INTERRUPT: "Vado Seco Irrigation and Power District, interruption report for the Hadley Ranch 69 kV tap, 2025",
    DOC.F_TRESCO: "Tresco Field Services, repowering program summary",
    DOC.F_README: "Marden-Vail Building Products, README for the data pull",
}
DISTRACTORS = [DOC.F_TRESCO, R.F_CURVE]


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for ln in fh if not ln.startswith("#")) - 1
    if path.endswith(".txt"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for ln in fh if ln.strip())
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        return sum(max(ws.max_row - 1, 0) for ws in wb.worksheets)
    return None


def write(target, out_path, B=None):
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": "2026-10-06",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task152",
        "title": "How much of a solar plant's 2027 output to sell forward at its one-year P90 once its worn modules "
                 "are replaced, when only the modules' own wear leaves with them",
        "domain": "Energy Systems & Utilities",
        "client_domain": "Energy Systems & Utilities",
        "subdomain": "asset-condition-maintenance (a repowered plant's forward energy: the original modules' wear read "
                     "apart from the dust carried between washes and the inverters' losses, on the days after each "
                     "wash at the inverters' DC input, then the long-term record's one-year P90)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a single committed volume with the P50 and standard deviation it rests on, a one-page note "
                        "with a chart of the 25 weather-year outputs marking the P50 and the volume, and two tables "
                        "(each inverter's 2025 availability under the O&M agreement; each year's over or under of net "
                        "energy at the delivery point against the volume sold forward, 2016 to 2025)",
        "as_of": "2026-10-06",
        "deliverables": ["hedge_volume_2027.xlsx", "hedge_note_2027.pdf"],
        "distractor_files": DISTRACTORS,
        "field_terms": ["generator"],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task152/generator/build.py (seeded, deterministic) around "
                               "a fictional manufacturer's solar plant in Arizona, its O&M contractor, module suppliers, "
                               "irrigation district, irradiance provider and trading counterparty, in the layouts of "
                               "plant SCADA exports, data logger and event exports, a CMMS work order export, utility "
                               "billing and meter data exports, a trade blotter and confirmations; the weather is "
                               "simulated for the site; no real organisation's records or person is depicted.",
                     "date": "2026-10-06", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-16",
        "generator": "task152/generator/build.py",
        "files": out,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
