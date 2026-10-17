"""Write task154/metadata.json from the built pack."""
import json
import os

import records as R

SOURCES = {
    R.F_GUIDE: "Statistics Office, quarterly national accounts user guide, 2026 edition",
    R.F_NOTICE: "Statistics Office, notice on the June quarter 2026 advance estimate, 24 July 2026",
    R.F_DB: "Statistics Office, real-time database of quarterly GDP estimates (Tarbert Economics' download of 26 June 2026)",
    R.F_ANNUAL: "Statistics Office, annual national accounts 2025 with revised quarterly series, 21 July 2026",
    R.F_PRICES: "Statistics Office, price indexes, June 2026",
    R.F_BULLETIN: "Trade and Business Statistics, merchandise trade and business stocks, June 2026",
    R.F_PORTAL: "Trade and Business Statistics, portal monthly series (Tarbert Economics' pull of 24 June 2026)",
    R.F_BULK: "Trade and Business Statistics, bulk download of trade by country and SITC division (pull of 24 June 2026)",
    R.F_COUNTRIES: "Trade and Business Statistics, country codes",
    R.F_SITC: "Trade and Business Statistics, SITC Revision 4 divisions",
    R.F_PORTS: "Harbours Board, monthly bulk loadings by port",
    R.F_TRACKER: "Tarbert Economics, GDP tracker for the June quarter 2026",
    R.F_POLL: "Harbourline, economists' poll on June quarter 2026 GDP",
    R.F_SURVEY: "Industry Federation, business conditions survey",
    R.F_INDEX: "Tarbert Economics, index of the desk's data folder",
}
DISTRACTORS = R.DISTRACTORS
AS_OF = "2026-07-29"


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for ln in fh) - 1
    if path.endswith(".txt"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for ln in fh if ln.strip())
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        return sum(max(ws.max_row - 1, 0) for ws in wb.worksheets)
    if path.endswith(".json"):
        return None
    return None


def write(target, out_path):
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": AS_OF,
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task154",
        "title": "What a bank's economics desk calls for the advance estimate of June-quarter GDP growth the evening "
                 "before, when the late trade and stocks bulletin feeds three of its lines",
        "domain": "Economics & Econometrics",
        "client_domain": "Economics & Econometrics",
        "subdomain": "forecasting-forecast-evaluation (a bottom-up forecast of a statistical office's first release, "
                     "the change in business inventories built from book-value stocks revalued over each industry's "
                     "stockholding period at both quarter ends, validated against the office's estimates of past "
                     "quarters)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a single committed growth rate in a one-page client preview, with two tables: the advance "
                        "estimate's revision record (three quarters and two means over twelve) and the change in coal "
                        "and LNG shipped to five markets (ten cells and two totals)",
        "as_of": AS_OF,
        "deliverables": ["gdp_preview_2026q2.pdf", "gdp_preview_2026q2_tables.xlsx"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task154/generator/build.py (seeded, deterministic) "
                               "around a fictional country's statistics office, its trade and business statistics "
                               "unit, its ports board, a wire service, an industry body and a fictional commercial "
                               "bank's economics desk, in the layouts of a national accounts user guide and notice, a "
                               "real-time database and annual accounts workbook, price index tables, a monthly trade "
                               "and stocks bulletin, a statistics portal pull and bulk download, port statistics, a "
                               "desk tracker workbook, a poll and a survey release; no real organisation's records or "
                               "person is depicted.",
                     "date": AS_OF, "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-17",
        "generator": "task154/generator/build.py",
        "files": out,
    }
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
