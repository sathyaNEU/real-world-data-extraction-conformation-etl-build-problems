"""Write task183/metadata.json from the built pack: what the task is about, the deliverables, the distractors and
each file's provenance. It names no method and no mechanism."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as P   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    "acct": "Core banking export of every posting on the reviewed customers' current accounts, January 2025 to "
            "September 2026",
    "ms": "Merchant services daily trade by terminal for the reviewed customers and the till service's other "
          "customers, January 2025 to September 2026",
    "mreg": "Merchant register of the Bank's acquiring business, October 2026",
    "seg": "Financial Crime Operations' cash-intensive segment review list for the review year 2025-26",
    "till": "Till service daily totals for the reviewed customers on the Bank's till service, January 2025 to "
            "September 2026",
    "bcr": "The Bank's Business Cash Review Standard BCR-3, issue 3",
    "ap": "An Post's export of the business lodgements its counters took for the Bank, October 2025 to September 2026",
    "apfee": "Schedule 2 (fees) of the agency services agreement between An Post and the Bank",
    "tlog": "The till service's central log of Z-reports received from every till-service customer, October 2025 to "
            "the October 2026 extract",
    "rsi": "A monthly retail sales value and volume index by retail sector, January 2024 to September 2026",
    "orders": "The branches' weekly note and coin orders from the cash centre, 2025-26",
    "offices": "An Post's list of the post offices in the Bank's branch areas, with office type and opening hours",
}
DATES = {"acct": "2026-10-14", "ms": "2026-10-14", "mreg": "2026-10-14", "seg": "2025-10-01", "till": "2026-10-14",
         "bcr": "2025-06-18", "ap": "2026-10-09", "apfee": "2025-06-24", "tlog": "2026-10-14", "rsi": "2026-10-28",
         "orders": "2026-10-02", "offices": "2026-10-05"}
DISTRACTORS = {
    "rsi": "a sector index of retail trade: relevant to whether the year's trading was ordinary, used by no figure",
    "orders": "the branches' cash orders from the cash centre: relevant to the cash cycle, used by no figure",
    "offices": "An Post's office list with types and hours: relevant to the post office channel, used by no figure",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path, counts=None):
    files = []
    for k, f in P.FILES.items():
        p = os.path.join(target, f)
        rows = rows_of(p)
        if rows is None and counts and k in counts:
            rows = counts[k]
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows,
                      "source": "Constructed: " + SOURCES[k], "date": DATES[k],
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    files.sort(key=lambda x: x["path"])
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task183",
        "title": "Which cash-intensive business customers of a regional Irish bank go to Financial Crime "
                 "Investigations for cash lodged in 2025-26 beyond what their own trading took, with the year's post "
                 "office agency and till service months",
        "domain": "Banking, Credit & Financial Risk",
        "subdomain": "fraud and anti-money-laundering detection (a fictional regional bank's annual review of its "
                     "cash-intensive business customers)",
        "objective": "Anomaly Detection & Diagnostics",
        "prompt_shape": "01: the referral list under a line, each reviewed customer's figure charted, with two monthly "
                        "tables",
        "as_of": "2026-11-06",
        "deliverables": ["fci_referrals_jan2027.docx", "cash_review_2026.xlsx"],
        "largest_file": {"path": big["path"], "rows": big["rows"]},
        "distractors": [{"path": P.FILES[k], "why": v} for k, v in DISTRACTORS.items()],
        "files": files,
        "fictional": "Lough Ree Bank DAC, its customers, staff, accounts and records are invented; the towns, An Post "
                     "and the Irish public holidays are real.",
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta
