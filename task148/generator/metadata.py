"""Write task148/metadata.json from the built pack."""
import json
import os
import sys

import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AS       # noqa: E402
import deliver as DL    # noqa: E402
import docs as DOC      # noqa: E402
import records as R     # noqa: E402

SOURCES = {
    R.F_CURRENT: "Fenmore Savings Bank current servicing system, month-end loan history of the SBA 7(a) book, October "
                 "2017 to September 2026",
    R.F_LEGACY: "Fenmore Savings Bank legacy core, month-end loan history of the SBA 7(a) book, October 2009 to October 2017",
    R.F_CODES: "Fenmore Savings Bank servicing status codes, current system and legacy core",
    R.F_MASTER: "Fenmore Savings Bank SBA Lending portfolio register of 7(a) loans approved from October 2009",
    R.F_REGISTER: "Fenmore Savings Bank loan documentation system, guarantee register",
    DOC.F_POLICY: "Fenmore Savings Bank credit policy CP-SBA-07 version 4, allowance for credit losses on SBA 7(a) "
                  "unguaranteed portions",
    DOC.F_TERMS: "Fenmore Savings Bank SBA Loan Authorization Part B standard terms, form SBL-AUTH-B (March 2018)",
    AS.F_CARES: "SBA fiscal transfer agent remittance detail for Section 1112 payments, CARES Act layout, as received "
                "by Fenmore Savings Bank",
    AS.F_EAA: "SBA fiscal transfer agent remittance detail for Section 1112 payments, Economic Aid Act layout, as "
              "received by Fenmore Savings Bank",
    AS.F_CREDITS: "Fenmore Savings Bank treasury management, credits to the SBA settlement account",
    AS.F_LEDGER: "Fenmore Savings Bank Special Assets, charge-off and recovery entries on SBA 7(a) loans",
    AS.F_PAYSBA: "Fenmore Savings Bank accounts payable and treasury management, payments to SBA",
    R.F_1502: "Fenmore Savings Bank Form 1502 report for September 2026",
    R.F_SECMKT: "Fenmore Savings Bank secondary market settlements of SBA guaranteed portions",
    R.F_MANIFEST: "SBA Servicing export manifest for the allowance data",
    DOC.F_README: "SBA Servicing and Loan Operations README and field notes for the allowance data",
}
DISTRACTORS = [R.F_1502, R.F_SECMKT]


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        return pq.ParquetFile(path).metadata.num_rows
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        return sum(ws.max_row - 1 for ws in wb.worksheets)
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2026-10-05",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task148",
        "title": "How much a savings bank books at its fiscal year-end as the CECL allowance on the unguaranteed "
                 "portions of its relief-era SBA 7(a) loans, when an operator's units are cross-defaulted under the "
                 "same personal guarantees",
        "domain": "Banking, Credit & Financial Risk",
        "client_domain": "Banking, Credit & Financial Risk",
        "subdomain": "expected-credit-loss-provisioning (lifetime expected charge-offs from default and payoff hazards "
                     "by months on book, conditioned on survival, with the guarantor group as the unit that defaults)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "one figure (the allowance to the nearest $1 million) with its split by approval fiscal year, a "
                        "board note with a chart of the allowance and the unguaranteed principal, and two tables "
                        "(Section 1112 payments by fiscal quarter; net charge-offs by fiscal year and approval year)",
        "as_of": "2026-09-30",
        "deliverables": [DL.GOLD_BOOK, DL.GOLD_NOTE],
        "distractor_files": DISTRACTORS,
        "stated_inputs": [],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task148/generator/build.py (seeded, deterministic) around "
                               "a fictional savings bank, its SBA lending division, its borrowers and guarantors and "
                               "their records, in the layouts of a lender's servicing extracts and of the reports SBA's "
                               "fiscal transfer agent sends lenders; no real organisation's records, person or borrower "
                               "is depicted. The prime rate path the servicing records follow is the published prime "
                               "rate to December 2025, held at 6.75 per cent after.",
                     "date": "2026-10-05", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-16",
        "generator": "task148/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    t = os.path.join(os.path.dirname(HERE), "target")
    write(t, os.path.join(os.path.dirname(HERE), "metadata.json"))
