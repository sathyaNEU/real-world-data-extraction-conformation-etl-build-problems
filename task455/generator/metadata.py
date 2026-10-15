"""Write task455/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W   # noqa: E402

F = W.FILES
SOURCES = {
    F["register"]: "the state UI tax system's employer register, every private employer account with a worksite in the "
                   "seven Lornock Valley counties open at any time from 1 October 2024 to 14 May 2027",
    F["qcew"]: "the quarterly contribution reports (QCEW microdata layout) of those accounts, 2024Q4 to 2026Q4",
    F["wages"]: "the quarterly wage reports of those accounts, one row per worker, account and quarter, with the "
                "bureau's protected worker key",
    F["counties"]: "the region's county codes",
    F["guideline"]: "the Department of Commerce's Formation Counties Program designation guideline FC-G-2027-01 "
                    "(issued 2 February 2027)",
    F["dict"]: "the Labor Market Information Bureau's data dictionary for the research extract",
    F["manifest"]: "the list of the files in the bureau's extract of 14 May 2027",
    F["pop"]: "the state demographer's July 1 county population estimates, vintage 2026",
    F["sos"]: "the Secretary of State's new business entity filings with a principal office in the seven counties, "
              "2025 and 2026",
    F["grants"]: "the Formation Counties Program's grant disbursements in fiscal year 2026 (the 2025 to 2027 grant "
                 "period)",
}
DISTRACTORS = [F[k] for k in W.DISTRACTORS]
DELIVERABLES = ["formation_county_designation_2027.pdf", "lornock_establishment_births_2026.xlsx"]


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
                      "source": "Constructed: " + SOURCES[f], "date": W.EXTRACT.isoformat(),
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task455",
        "architecture": 2,
        "title": "Which three of the Lornock Valley's seven counties the state Commerce Department designates as "
                 "Formation Counties for 2027 to 2029 on their 2026 establishment birth rates, conformed from the UI "
                 "employer register, quarterly contribution reports and wage records",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "census-register-administrative-data-quality (business demography from an administrative "
                     "employer register: establishment births separated from businesses continuing under a new "
                     "employer account by the continuity of their workforce)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "01: a ranked list under a cap (seven counties, three designated), with each county's births, "
                        "set-aside accounts and rate, the runner-up and gap, and each county's 2025 births and deaths "
                        "with their rates",
        "as_of": W.EXTRACT.isoformat(),
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["2027", "2029", "2026", "2025", "2024", "100"],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task455/generator/build.py (seeded, deterministic) in the "
                               "layouts of a state UI employer register, the BLS QCEW microdata record and a state UI "
                               "wage record file; the region, its counties, employers, workers and people are "
                               "fictional, as are every account number, FEIN, address and worker key.",
                     "date": W.EXTRACT.isoformat(), "license": "CC0-1.0 (original work)"}],
        "created": W.EXTRACT.isoformat(),
        "generator": "task455/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")
    return meta
