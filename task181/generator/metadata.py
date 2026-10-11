"""Write ../metadata.json from the built target/."""
import json
import os

import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, "..", "target")
DESC = {
    "card_authorisations": "Authorisation host messages for the credit union's cards, 1 June to 4 October 2026 (UTC)",
    "merchant_directory": "Acquirer merchant directory: merchant ID, name, MCC, address, town, province or state, country",
    "card_history": "Card services card history at 5 October 2026: cards, replacements, members",
    "fraud_cases": "Fraud desk workbook, one row per disputed transaction, cases opened 1 August to 4 October 2026",
    "chargebacks": "Chargeback events, 1 August to 4 October 2026",
    "pos_entry_mode_codebook": "Code lists for the authorisation extract (entry mode, message type, processing, response, currency)",
    "CP-14": "Card policy CP-14 v3: card compromise and reissue",
    "MS-3": "Member service standard MS-3: unauthorised card transactions, with the 2026 holiday list",
    "fraud_desk_notes": "Fraud desk field notes for the extracts",
    "close_out_2025": "Close-out of the 2025 Brockville branch ATM skimming incident",
    "online_banking_logins": "Online banking session log, 1 August to 4 October 2026",
    "atm_cash_replenishment": "Branch ATM cash replenishment visits, July to September 2026",
    "cudw_job_fraud_weekly": "Data warehouse job report for the 5 October 2026 fraud_weekly run",
}
DISTRACTORS = ("online_banking_logins", "atm_cash_replenishment")


def main():
    files, fmts = [], set()
    for f in sorted(os.listdir(T)):
        p = os.path.join(T, f)
        ext = os.path.splitext(f)[1][1:]
        fmts.add(ext)
        e = {"path": f, "format": ext, "bytes": os.path.getsize(p)}
        if ext == "csv":
            with open(p) as fh:
                e["rows"] = sum(1 for _ in fh) - 1
        if ext == "parquet":
            e["rows"] = pq.ParquetFile(p).metadata.num_rows
        key = next(k for k in DESC if f.startswith(k))
        e.update(source="Constructed: " + DESC[key], date="2026-10-05",
                 license="CC0-1.0 (original work, constructed for this task)")
        files.append(e)
    big = max((x for x in files if "rows" in x), key=lambda x: x["rows"])
    meta = {
        "task": "task181",
        "title": "Sizing a credit union's card reissue after a counterfeit wave traced to two skimmed terminals",
        "domain": "Banking, Credit & Financial Risk",
        "subdomain": "fraud and AML detection (card compromise, common point of purchase)",
        "objective": "Anomaly Detection & Diagnostics",
        "prompt_shape": "18 hypotheses versus evidence: every terminal a hypothesis; the committed figure is the exposed card population",
        "as_of": "2026-10-05",
        "deliverables": ["card_reissue_request.pdf", "common_point_trace.xlsx"],
        "distractor_files": [x["path"] for x in files if x["path"].startswith(DISTRACTORS)],
        "input_gates": {"files": len(files), "formats": sorted(fmts), "largest_file": big["path"],
                        "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task181/generator/build.py (seeded, deterministic) around a "
                               "fictional credit union (Larchmere Credit Union) in real eastern Ontario towns; every "
                               "member, card, merchant, terminal and case is invented.",
                     "date": "2026-10-11", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-11",
        "generator": "task181/generator/build.py",
        "files": files,
    }
    with open(os.path.join(HERE, "..", "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    print(meta["input_gates"], meta["distractor_files"])


if __name__ == "__main__":
    main()
