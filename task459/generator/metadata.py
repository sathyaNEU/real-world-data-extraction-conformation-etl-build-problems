"""Write task459/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as P    # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    P.FILES["camd"]: "EPA Clean Air Markets hourly emissions of the offered plants' monitored units, 2024 and 2025, in the layout of the CAMPD hourly export",
    P.FILES["plans"]: "the monitored units' monitoring plan records",
    P.FILES["xwalk"]: "EPA-EIA power sector data crosswalk rows for the offered plants",
    P.FILES["eia860"]: "Form EIA-860 2025 generator data for the offered plants' EIA plant codes",
    P.FILES["eia923"]: "Form EIA-923 Page 1 generation and fuel, 2024 and 2025, for the offered plants' EIA plant codes",
    P.FILES["offers"]: "the district's log of the offers received under its 2026 baseload request for offers",
    P.FILES["meter"]: "the respondents' hourly revenue-meter net generation, 2024 and 2025, compiled by the district",
    P.FILES["gads"]: "the respondents' 2025 GADS event records, compiled by the district",
    P.FILES["outages27"]: "the respondents' planned and maintenance outages for 2027",
    P.FILES["procedure"]: "the district's Resource Procurement Procedure RP-7, revised 9 June 2026",
    P.FILES["terms"]: "the district's 2026 Baseload Request for Offers, issued 1 June 2026",
    P.FILES["dictionary"]: "the district's field descriptions for the evaluation data",
}
DISTRACTORS = ["eia923", "outages27"]


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8", errors="replace") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2026-11-04",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task459",
        "architecture": 1,
        "title": "How much of a public utility district's 1,000 MW baseload need its offers can fill under the state's "
                 "925-pound emissions performance standard, and from which plants: each offered gas plant's carbon "
                 "dioxide per net megawatt-hour under its commitment, conformed from EPA's hourly emissions and the "
                 "plants' revenue meters",
        "domain": "Physical & Environmental Sciences",
        "subdomain": "emissions-inventory (a power-sector carbon dioxide inventory for ten offered gas plants: EPA hourly "
                     "emissions per monitored stack, revenue-meter net generation, the EIA generator and generation "
                     "surveys and the EPA-EIA crosswalk conformed into each plant's emission rate)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "01: a ranked list under a cap, the 1,000 MW need filled in order of capacity price from the "
                        "offers whose plants meet the 925-pound standard; every offered plant's emission rate, its 2025 "
                        "forced outage hours and outages and its 2025 hours of substitute data",
        "as_of": "2026-11-04",
        "deliverables": ["eps_determination_rfo_2027.pdf", "offered_plants_eps_2027.xlsx"],
        "distractor_files": [P.FILES[k] for k in DISTRACTORS],
        "stated_inputs": ["925", "1,000"],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task459/generator/build.py (seeded, deterministic) in the "
                               "layouts of EPA's Clean Air Markets hourly emissions and monitoring plan exports, the "
                               "EPA-EIA crosswalk, Forms EIA-860 and EIA-923, revenue-meter interval data and NERC GADS "
                               "event records; the district, the plants and their owners are fictional.",
                     "date": "2026-11-04", "license": "CC0-1.0 (original work)"}],
        "created": "2026-11-04",
        "generator": "task459/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
