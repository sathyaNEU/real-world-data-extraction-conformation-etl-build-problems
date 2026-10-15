"""Write task458/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as P    # noqa: E402

F = P.FILES
SOURCES = {
    F["claims"]: "the plan's claims system extract of behavioral-health claims and encounters with a service date in the contract year, every version, paid or accepted through 31 October 2026",
    F["spans"]: "the plan's enrollment system spans for every member number with coverage in the contract year",
    F["nppes"]: "the NPPES monthly file of October 2026, the records with a Washington practice or mailing address and the plan's provider file NPIs, in the NPPES downloadable file layout (selected columns)",
    F["week1"]: "the NPPES weekly incremental file of 12 to 18 October 2026, same selection and layout",
    F["week2"]: "the NPPES weekly incremental file of 19 to 25 October 2026, same selection and layout",
    F["week3"]: "the NPPES weekly incremental file of 26 October to 1 November 2026, same selection and layout",
    F["week4"]: "the NPPES weekly incremental file of 2 to 8 November 2026, same selection and layout",
    F["deact"]: "the NPPES deactivated NPI report of 10 November 2026, in the CMS report layout",
    F["zipcty"]: "a ZIP code to county crosswalk for the second quarter of 2026 in the HUD-USPS crosswalk layout, for the ZIP codes of the plan's members and providers",
    F["nucc"]: "the provider taxonomy codes the NPPES records carry, in the NUCC code set layout (code, grouping, classification, specialization, display name, section)",
    F["fees"]: "the plan's fee schedule for behavioral-health professional services in the contract year",
    F["policy"]: "the plan's Network Policy NP-31, Prescriber Service Area Designation (approved 21 May 2026)",
    F["dict"]: "Network Analytics' descriptions of the files and their fields",
    F["adequacy"]: "the plan's network adequacy time and distance report for behavioral-health prescribers, second quarter of 2026",
    F["ofm"]: "county population estimates of 1 April 2026 for the ten counties, in the layout of the state Office of Financial Management's estimates",
    F["manifest"]: "the list of the files Network Analytics pulled on 12 November 2026",
}
DISTRACTORS = [F["adequacy"], F["ofm"], F["week4"]]
DELIVERABLES = ["prescriber_pilot_county_scorecard_2027.xlsx", "county_adult_members_2026_conformed.csv"]


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
                      "source": "Constructed: " + SOURCES[f], "date": "2026-11-12",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task458",
        "architecture": 1,
        "title": "Which of a Medicaid managed care plan's ten eastern Washington counties are designated for its 2027 "
                 "behavioral-health prescriber loan-repayment pilot, each county's members with a serious mental illness "
                 "and with an opioid use disorder estimated from claims against enrollment",
        "domain": "Healthcare Delivery & Health Economics",
        "subdomain": "payment-claims-health-plan-analytics (claims-based case identification against enrollment: a "
                     "lasting condition's prevalence measured on the members enrolled all year, by eligibility group, and "
                     "carried to every member, for need-based workforce ratios over a contract year)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "10: a scorecard against thresholds (three standards for each of ten counties, two of three to "
                        "designate), with quarterly payments and the conformed county and eligibility-group file",
        "as_of": "2026-11-12",
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["2027", "2026", "2025", "31", "10", "1,000", "16.5", "23.0", "68"],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task458/generator/build.py (seeded, deterministic) in the "
                               "public layouts of the NPPES downloadable files and deactivation report, the HUD-USPS "
                               "ZIP-county crosswalk and the NUCC taxonomy code set, and in the idiom of a Medicaid managed "
                               "care plan's claims and enrollment extracts; the plan, its agencies, practices, clinicians, "
                               "members and people are fictional, as are every NPI and address.",
                     "date": "2026-11-12", "license": "CC0-1.0 (original work)"}],
        "created": "2026-11-12",
        "generator": "task458/generator/build.py",
        "files": files,
    }
    json.dump(meta, open(out_path, "w"), indent=1)
    open(out_path, "a").write("\n")
    return meta
