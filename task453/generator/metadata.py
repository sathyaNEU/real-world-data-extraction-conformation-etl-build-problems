"""Write task453/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W    # noqa: E402

TASK = os.path.dirname(HERE)
F = W.FILES
SOURCES = {
    F["wide"]: "the Provincial Revenue Agency's yearly tables of payroll jobs by municipality and industry group, 2021 to 2023",
    F["long"]: "the Agency's monthly payroll jobs by municipality and NAICS sector, January 2024 to March 2027, as of 23 April 2027",
    F["rev"]: "the Agency's revision file of 7 May 2027 for January to March 2027",
    F["work"]: "the Agency's workplace schedule lines for March 2026 and March 2027, as of 7 May 2027",
    F["dict"]: "the Agency's field descriptions for its statistics files",
    F["note"]: "the Agency's release note of 16 February 2026 on placing payroll jobs at the workplace",
    F["conc"]: "the bureau's municipal concordance to economic regions",
    F["reg"]: "the Regional Rapid Response Program Regulation, consolidated to 1 July 2026",
    F["trans"]: "the Agency's transmittal of 7 May 2027",
    F["lfs"]: "the labour force survey's three-month moving averages by economic region, January 2025 to March 2027",
    F["pop"]: "the bureau's municipal population estimates, 1 July 2024 to 2026",
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
                      "source": "Constructed: " + SOURCES[f], "date": "2027-05-07",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task453",
        "architecture": 1,
        "title": "Which economic regions a provincial statistics bureau certifies for the first quarter of 2027 under a "
                 "rapid response regulation read off seasonally adjusted payroll jobs, built from employer returns "
                 "whose placement of jobs moved from account addresses to workplaces in January 2026",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "seasonal-adjustment-official-time-series-production (each economic region's monthly payroll "
                     "jobs conformed from the revenue agency's employer return statistics in two layouts, a revision "
                     "file and a municipal concordance, and seasonally adjusted across a documented change of placement)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "10: a scorecard of every economic region against the designation line, with each region's "
                        "employers with payroll jobs in March 2027 and the jobs its workplaces lost from March 2026",
        "as_of": "2027-05-07",
        "deliverables": list(W.DELIVERABLES),
        "distractor_files": [F[k] for k in W.DISTRACTORS],
        "stated_inputs": ["1.0"],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task453/generator/build.py (seeded, deterministic) in the "
                               "layouts of a provincial revenue agency's employer return statistics, a statistics "
                               "bureau's municipal concordance and population estimates, and a labour force survey's "
                               "regional estimates; the province, its regions, municipalities, employers and people are "
                               "fictional.",
                     "date": "2027-05-07", "license": "CC0-1.0 (original work)"}],
        "created": "2027-05-07",
        "generator": "task453/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
