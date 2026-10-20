"""metadata.json: the task's identity, its files, the distractors, the input gates and the sources."""
import json
import os

import world as W

F = W.FILES
DISTRACTORS = [F[k] for k in W.DISTRACTORS]


def rows_of(path):
    if path.endswith(".csv") or path.endswith(".txt"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path, counts=None):
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    rows = {f: rows_of(os.path.join(target, f)) for f in files}
    big = max((f for f in files if rows[f] is not None), key=lambda f: rows[f])
    meta = {
        "task": "task474",
        "architecture": 1,
        "title": "How the Regional Opportunity Fund's $12,000,000 for FY2027 is split among the nine planning "
                 "regions' councils of governments when the State Data Center's 2020 to 2022 poverty estimates exist "
                 "only for the former counties; with each region's 2020, 2021 and 2022 residents in poverty and "
                 "2020-2024 average, a chart of the nine amounts, and each council's share of the former county "
                 "agencies' unexpended FY2026 balances, the people it is counted on and the FY2026 energy assistance "
                 "paid in its towns",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "seasonal-adjustment-official-time-series-production (an annual model-based poverty series "
                     "rebuilt on new county-equivalents, the years the new geography lacks produced by temporal "
                     "disaggregation with a benchmarked administrative indicator)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "05: an allocation to a fixed total: each of the nine councils' FY2027 amounts from "
                        "$12,000,000, on the conformed region series (27 region-years and nine averages), beside 27 "
                        "transition figures",
        "as_of": "2026-10-16",
        "deliverables": list(W.DELIVERABLES),
        "distractor_files": DISTRACTORS,
        "wrong_basis_distractor": {
            "file": F["factors"],
            "basis": "each former county's 2020 census population and housing units split among the planning regions, "
                     "not its residents in poverty in each year",
            "ruled_out_by": "the allocation rule (1.1 and 2.2), which divides each former county's estimate by its "
                            "towns' residents in poverty in that year"},
        "stated_inputs": ["2020", "2022", "2024", "FY2026", "FY2027"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task474/generator/build.py (seeded, deterministic) in the layouts "
                       "of a state data center's annual model-based poverty estimate releases and methods note, an "
                       "American Community Survey B17001 five-year extract with the Census Bureau's standard table "
                       "notes, a state social services department's monthly SNAP participation file by town, a town "
                       "to county to planning region code file, county-to-region allocation factors, a budget "
                       "office's fund allocation rule, allocation table and grant closeout, and a grants data "
                       "system's client services extract, profile audit trail, client number conversion and export "
                       "layout; the state is unnamed and its counties, regions, towns, agencies and people are "
                       "fictional",
             "date": "2026-10-16",
             "license": "original work for this task; no third-party data"}],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta
