"""Write task451/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as P    # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    P.FILES["claims"]: "the claims administrator's monthly client extract of the Fund's medical claims, every version, run 1 February 2027",
    P.FILES["notice"]: "the claims administrator's client notice of September 2026 on moving the Fund's claims to its Tallis platform",
    P.FILES["elig"]: "the Fund Office's export of its eligibility spans (hour-bank coverage), every version",
    P.FILES["roster"]: "the Fund Office's monthly attribution roster of members to accountable care partner groups for 2026",
    P.FILES["codes"]: "the Fund Office's reference list of the codes in its claims, pharmacy and eligibility feeds",
    P.FILES["agreement"]: "Schedule B (annual reconciliation) of the Fund's accountable care partner agreements, with Exhibit 1",
    P.FILES["rx"]: "the pharmacy benefit manager's client claims file for prescriptions filled in 2026",
    P.FILES["clinicians"]: "the Fund's network file of clinicians in each partner group on 1 January 2027",
    P.FILES["stoploss"]: "the Fund's specific stop-loss policy summary for 2026",
    P.FILES["quality"]: "the partners' preliminary 2026 quality measures",
}


def rows_of(path):
    if path.endswith((".csv", ".txt")):
        with open(path, encoding="utf-8", errors="replace") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2027-02-03",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task451",
        "architecture": 2,
        "title": "The accountable care partners that owe a multiemployer health fund a shared-loss payment for 2026, "
                 "with each partner's pharmacy spending and the share of its professional spending outside the group",
        "domain": "Healthcare Delivery & Health Economics",
        "subdomain": "payment-claims-health-plan-analytics (a multiemployer health fund's annual reconciliation with its "
                     "accountable care partners)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "other: a register of the partner groups, each with whether it owes, its members' 2026 "
                        "pharmacy spending and the share of its members' 2026 professional spending that went to "
                        "clinicians outside the group, with a chart of each partner's cost against its target",
        "as_of": "2027-02-03",
        "deliverables": ["partner_settlement_2026.xlsx", "partners_against_target_2026.svg"],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task451/generator/build.py (seeded, deterministic) in the "
                               "layouts of a third-party administrator's medical claims extract (837-derived, with claim "
                               "frequency codes and type-of-bill codes), a multiemployer fund's eligibility and attribution "
                               "files, and an NCPDP-style pharmacy benefit manager claims file; the fund, its "
                               "administrator, its partners and every member are fictional, and every NPI is synthetic.",
                     "date": "2027-02-03", "license": "CC0-1.0 (original work)"}],
        "created": "2027-02-03",
        "generator": "task451/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
