"""Write task145/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import records as R   # noqa: E402
import deliver as DL  # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    R.F_HV["2024Q4"]: "Clearance system high-value check extract, October to December 2024 (earlier layout)",
    R.F_HV["2025Q1"]: "Clearance system high-value check extract, January to March 2025 (earlier layout)",
    R.F_HV["2025Q2"]: "Clearance system high-value check extract, April to June 2025 (earlier layout)",
    R.F_HV["2025Q3"]: "Clearance system high-value check extract, July to September 2025 (earlier layout)",
    R.F_HV["2025Q4"]: "Clearance system high-value check extract, October to December 2025 (earlier layout)",
    R.F_HV["2026Q1"]: "Clearance system high-value check extract, January to March 2026",
    R.F_HV["2026Q2"]: "Clearance system high-value check extract, April to June 2026",
    R.F_HV["2026Q3"]: "Clearance system high-value check extract, July to September 2026",
    R.F_GW_LEGACY: "Legacy brokerage system monthly gateway report GA-02, January 2021 to September 2024",
    R.F_GW_NEW: "Clearance system monthly gateway report, October 2024 to September 2026",
    R.F_PLAN27: "Network plan 2027 (Network Planning), volumes and planning assumptions",
    R.F_PLAN26: "Network plan 2026 as issued in September 2025 (Network Planning)",
    R.F_STD: "Customs Brokerage standard BRK-STD-03, brokerage staffing, revision 4",
    R.F_CLR: "Clearance operations manual CLR-OPS-11, valuation, routing and the high-value check, revision 7",
    R.F_NOTE_CLR: "Clearance Operations' note on the clearance and brokerage extracts",
    R.F_TA_OLD: "Legacy time and attendance export, April to October 2025",
    R.F_TA_NEW: "Time and attendance export, 27 October 2025 to September 2026",
    R.F_HR_STAFF: "HR extract of the brokerage desks' staff",
    R.F_HR_CHG: "HR extract of assignment changes on the brokerage desks",
    R.F_CC: "Finance cost-centre map, legacy and ERP 2025 schemes",
    R.F_NOTE_PAY: "HR Systems' note on the payroll, HR and contract broker extracts",
    R.F_BCS_PDF: "Brandmoor Customs Services statements of account, April 2025 to March 2026",
    R.F_BCS_PORTAL: "Brandmoor Customs Services client portal detail export",
    R.F_AP: "Accounts Payable register for Brandmoor Customs Services",
    R.F_BCS_RATES: "Brandmoor Customs Services contract schedule B",
    R.F_EXPORTS: "Export desk monthly declarations report",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".json"):
        with open(path, encoding="utf-8") as fh:
            return len(json.load(fh)["lines"])
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2026-10-07",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task145",
        "title": "Where Larchwood Express Canada's six new 2027 broker posts go across its five import gateways, "
                 "or are held, on each gateway's forecast formal entries per broker post",
        "domain": "Economics & Econometrics",
        "client_domain": "Economics & Econometrics",
        "subdomain": "forecasting-forecast-evaluation (a conditional forecast of each gateway's 2027 formal import "
                     "entries on the network plan's exchange rates: the shipments whose value for duty, set in "
                     "their invoice currency, will exceed CAD 3,300 at the plan year's rates)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "05 allocation to a fixed total: the six posts across five gateways and the held bucket, each "
                        "gateway's forecast monthly formal entries and its load after the review, with two fiscal "
                        "2025-26 tables (overtime hours by desk and quarter, the contract broker's charges by desk "
                        "and quarter) and a two-slide deck",
        "as_of": "2026-10-13",
        "deliverables": [DL.GOLD_BOOK, DL.GOLD_DECK],
        "distractor_files": list(R.DISTRACTORS),
        "stated_inputs": ["3,300", "3300", "1.3400", "1.6800", "1.8750", "0.18800", "0.0092500", "560"],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task145/generator/build.py (seeded, deterministic) around "
                               "a fictional Canadian express carrier (Larchwood Express Canada Ltd.), its customs "
                               "brokerage desks at five import gateways, its people and systems, and a fictional "
                               "contract customs broker (Brandmoor Customs Services Inc.); no real organisation, "
                               "person or system is depicted, and the exchange rates are constructed.",
                     "date": "2026-10-07", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-15",
        "generator": "task145/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
