"""Write task157/metadata.json from the built pack: the distractors, the portal's keys, the input gates and every
shipped file's source, date and licence."""
import json
import os

import docs as DOC
import records as R

SOURCES = {
    R.F_LEGACY: "Larch Rides, old dispatch platform's monthly driver export by legacy driver number, May 2021 to 14 "
                "July 2024",
    R.F_ACTIVITY: "Larch Rides dispatch warehouse, monthly driver activity, 15 July 2024 to the extract run of 3 "
                  "January 2027",
    R.F_CROSSWALK: "Larch Rides dispatch migration crosswalk, legacy driver numbers to driver ids (15 July 2024)",
    R.F_ACCOUNTS: "Larch Rides dispatch warehouse, driver accounts as at 3 January 2027",
    R.F_RUN25: "Larch Rides payments, old payout report for the 2025 winter guarantee main run (14 February 2025)",
    R.F_RUN26: "Larch Rides payments system, 2026 winter guarantee main run export (13 February 2026)",
    R.F_ADJ: "Larch Rides payments system, winter guarantee adjustment run lines, 2025 and 2026",
    R.F_RETURNS: "Larch Rides payout account, the bank's ACH return report, 2025 and 2026",
    R.F_EVENTS: "Larch Rides payments system, winter guarantee payout events, 2025 and 2026",
    R.F_APPS: "Larch Rides onboarding app, applications export, 2 June 2025 to 3 January 2027",
    R.F_ORDERS: "Larch Rides screening vendor portal, background check order export, June 2025 to January 2027",
    R.F_REFERRAL: "Larch Rides referral programme, 2026 referral bonus ledger",
    R.F_DEMAND: "Larch Rides marketplace planning, rider demand plan for Q1 2027 (4 December 2026)",
    DOC.F_TERMS: "Larch Rides Driver Supply, Winter Guarantee 2027 driver terms (14 December 2026)",
    DOC.F_EMAIL: "Larch Rides Finance, email on the guarantee account (30 December 2026)",
    DOC.F_PAYNOTES: "Larch Rides Payments Operations, winter guarantee payout notes (20 March 2026)",
    DOC.F_ONBNOTES: "Larch Rides Driver Onboarding, pipeline counting notes (5 August 2026)",
    DOC.F_KPI: "Larch Rides Supply Analytics, driver supply KPIs to November 2026 (11 December 2026)",
    DOC.F_NOTES: "Larch Rides Supply Analytics, data notes for the 3 January 2027 pull",
    DOC.F_LOG: "Larch Rides Supply Analytics, log of the 3 January 2027 pull",
}
DISTRACTORS = [R.F_DEMAND, R.F_REFERRAL]
TITLE = ("How much a Twin Cities ride-hail operator's January 2027 winter guarantee will pay ($350 to every driver "
         "completing 40 trips in four weeks), when last winter's recruits come back in a wave that straddles the "
         "funding date")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        n = sum(max(ws.max_row - 1, 0) for ws in wb.worksheets)
        wb.close()
        return n
    return None


def write(task_dir, n=None):
    target = os.path.join(task_dir, "target")
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": "2027-01-03",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task157",
        "title": TITLE,
        "domain": "Product Analytics",
        "client_domain": "Product Analytics",
        "house_domain": "product-analytics",
        "subdomain": "retention-cohort-lifetime-value-modeling (a ride-hail platform's supply-side driver cohorts: last "
                     "winter's recruits read as a returning cohort whose resurrection is under way at the forecast "
                     "date, sized from the part already back at the timing earlier cohorts kept)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a committed fund to the nearest $50,000 with the drivers expected to qualify, a table taking "
                        "the 2025 and 2026 guarantees to net cost (what never reached a driver, the net cost, the "
                        "drivers paid), a table of the onboarding pipeline by month of first application from June to "
                        "October 2026 (people who applied, approved, first trip by the as-of), and a two-slide deck "
                        "with each guarantee's steps from main run to net cost charted",
        "as_of": "2027-01-03",
        "deliverables": ["guarantee_fund_jan2027.xlsx", "guarantee_fund_jan2027.pptx"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task157/generator/build.py (seeded, deterministic) around "
                               "a fictional regional ride-hail operator in the Twin Cities, in the layouts of a "
                               "dispatch platform's monthly driver export and its successor's warehouse extract, a "
                               "payments system's payout runs, events and adjustment lines, a bank's ACH return "
                               "report, an onboarding app's applications export and a screening vendor's order "
                               "export; no real organisation's records or person is depicted.",
                     "date": "2027-01-03", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-17",
        "generator": "task157/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
