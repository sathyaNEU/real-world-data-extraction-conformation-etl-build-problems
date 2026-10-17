"""Write task155/metadata.json from the built pack."""
import json
import os

import common as K

SOURCES = {
    K.F_OFFERS: "Kellaway's Workforce Systems, KWS offer history report, shifts 29/08/2025 to 12/11/2026",
    K.F_REGISTER: "Kellaway's Workforce Systems, KWS call-in register, shifts 29/08/2025 to 12/11/2026",
    K.F_LEGACY: "Kellaway's stores, legacy rostering tool weekly export, roster weeks 29/08/2025 to 20/02/2026",
    K.F_KWS: "Kellaway's Workforce Systems, KWS roster lines, roster weeks 27/02/2026 to 06/11/2026",
    K.F_XMAS: "Kellaway's Workforce Systems, KWS roster report, Christmas 2026 rosters as published 12/11/2026",
    K.F_PEOPLE: "Kellaway's Workforce Systems, KWS people, 12/11/2026",
    K.F_AVAIL: "Kellaway's Workforce Systems, KWS availability profiles, 12/11/2026",
    K.F_PAYROLL: "Kellaway's People and Payroll, payroll casual register, 12/11/2026",
    K.F_STORES: "Kellaway's, store list",
    K.F_STANDARD: "Kellaway's Workforce Planning, relief crew placement standard WP-04 version 4, 09/10/2026",
    K.F_NOTES: "Kellaway's Workforce Systems, KWS Call-in module notes version 2.3, 04/08/2026",
    K.F_EA: "Kellaway's People and Payroll, enterprise agreement 2024 casual employment summary, 01/07/2026",
    K.F_PLAN: "Kellaway's Store Operations, Christmas trading plan 2026 version 2, 30/10/2026",
    K.F_CAL: "Kellaway's Store Operations, Victorian school terms and public holidays 2025 and 2026",
    K.F_TRANSMIT: "Kellaway's Workforce Systems, transmittal for data extract WR-26-1187, 12/11/2026",
}
AS_OF = "2026-11-13"


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
        return sum(max(ws.max_row - 6, 0) for ws in wb.worksheets) if "roster" in path else \
            sum(max(ws.max_row - 5, 0) for ws in wb.worksheets)
    if path.endswith(".json"):
        with open(path, encoding="utf-8") as fh:
            return len(json.load(fh)["people"])
    return None


def write(task, target):
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": AS_OF,
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task155",
        "title": "Which of a Victorian grocery chain's eight stores gets its one 25-person relief crew for the four "
                 "trading weeks to Christmas Eve 2026, placed where it will work the most hours the stores' casual "
                 "call-ins would otherwise leave unworked, and the crew hours it will work there",
        "domain": "Economics & Econometrics",
        "client_domain": "Economics & Econometrics",
        "subdomain": "discrete-choice-limited-dependent-variable-modeling (each casual's accept-or-decline choice on a "
                     "call-in offer, fitted on the offer log with the offer's position against the casual's own "
                     "rostered shift as a term, and run through the call-in module over the published Christmas "
                     "rosters)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a committed store and its crew hours in a one-page placement brief with a chart of every "
                        "store's expected unworked hours, and two tables: last Christmas's call-ins by store (hours "
                        "put out, covered and left uncovered, 24 cells) and cover across stores in those weeks "
                        "(each store's call-in hours covered by other stores' casuals and its casuals' hours "
                        "covered elsewhere, 16 cells)",
        "as_of": AS_OF,
        "deliverables": K.DELIVERABLES,
        "distractor_files": K.DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task155/generator/build.py (seeded, deterministic) "
                               "around a fictional family-owned Victorian grocery chain of eight stores, in the "
                               "layouts of a workforce management system's call-in register, offer history, roster "
                               "lines, people and availability exports, a legacy rostering spreadsheet tool's weekly "
                               "export, a payroll casual register, a published roster workbook, a planning standard, "
                               "system notes, an enterprise agreement summary, a trading plan, a calendar and an "
                               "extract transmittal; no real organisation's records or person is depicted.",
                     "date": AS_OF, "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-17",
        "generator": "task155/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task, "metadata.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
