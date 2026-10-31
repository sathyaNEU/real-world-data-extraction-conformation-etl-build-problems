"""Write task448/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as DC   # noqa: E402
import pack as P    # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    P.FILES["lar"]: "HMDA loan-level records for Kansas, 2024 and 2025, in the FFIEC public layout (the fields kept)",
    P.FILES["panel"]: "HMDA reporter panel rows for the institutions with records in the eight counties",
    P.FILES["feed24"]: "county recorder vendor's purchase-money mortgage file, eight counties, recordings of 2024",
    P.FILES["feed25"]: "county recorder vendor's purchase-money mortgage file, eight counties, recordings of 2025",
    P.FILES["feed26"]: "county recorder vendor's purchase-money mortgage file, recordings of January to August 2026",
    P.FILES["deliveries"]: "the research desk's register of the vendor's deliveries",
    P.FILES["alias"]: "mortgagee names as indexed, matched to lenders",
    P.FILES["register"]: "lenders known to the fund, with identifiers",
    P.FILES["shortlist"]: "the board's twelve-lender shortlist",
    P.FILES["agg2023"]: "HMDA 2023 originations by Kansas county, purpose and loan type",
    P.FILES["education"]: "homebuyer education completions by month, county and class format",
    P.FILES["codes"]: "the FFIEC's published values for the coded HMDA fields",
    DC.GUIDELINES: "Rural Down-Payment Assistance Program guidelines, 2027",
    DC.LAYOUT: "the vendor's file layout guide, versions 3 and 4",
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
                      "source": "Constructed: " + SOURCES[f], "date": "2026-10-09",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task448",
        "title": "The lenders a Kansas homeownership nonprofit recruits first for its 2027 rural down-payment "
                 "program, ranked on the home-purchase mortgages each made in the service area in 2024 and 2025",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "census-register-administrative-data-quality",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "01 (ranked list under a cap): the first lenders to recruit, in order, with counts and the next",
        "as_of": "2026-10-09",
        "deliverables": ["rural_lender_recruitment_2027.xlsx", "rural_lender_recruitment_2027.pptx"],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task448/generator/build.py (seeded, deterministic) around "
                               "a fictional Kansas nonprofit, its lenders and a fictional recorder data vendor, in the "
                               "layouts of the public HMDA files; no real lender, person or loan is depicted.",
                     "date": "2026-10-09", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-09",
        "generator": "task448/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
