"""Write task451/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as DC   # noqa: E402
import pack as P    # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    P.FILES["datastore"]: "the IATI Datastore's flattened transaction export for the secretariat's country and sector query of 5 October 2026",
    P.FILES["gxml"]: "the Pelorus Maternal Health Fund's IATI activity file, as downloaded on 5 October 2026",
    P.FILES["sxml"]: "the Sahel Maternal Survival Fund's IATI activity file, as downloaded on 5 October 2026",
    P.FILES["register"]: "the secretariat's register of members at 1 September 2026",
    P.FILES["registry"]: "the IATI Registry's publisher list for the publishers in the extract, October 2026",
    P.FILES["fx"]: "the secretariat's exchange table, units of currency per US dollar for every day from 2023 to September 2026",
    P.FILES["codelists"]: "the IATI codelists the extract uses",
    P.FILES["query"]: "the secretariat's note of the Datastore query",
    P.FILES["indicators"]: "the secretariat's compilation of maternal and newborn health indicators by country",
    P.FILES["offices"]: "the secretariat's estimates of office running costs in each capital for 2027",
    DC.METHOD: "the secretariat's methodology note for its member funds statistics, version 2, March 2026",
    DC.PAPER: "the Members' Council paper C/26/14 on country coordination offices",
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
        "task": "task451",
        "title": "Where a donor collaborative's members' council opens its three 2027 country coordination offices, "
                 "by the members' money spent in each country in 2025, once the money given through two pooled funds "
                 "is credited at the members' share of what each fund held when it paid",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "census-register-administrative-data-quality (aid statistics compiled from the publishers' IATI "
                     "records: the members' money followed through two pooled funds to the countries where it is spent)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "other: a register of 13 candidate countries, each with the members' money spent in 2025, the "
                        "commitments not yet paid at 30 June 2026 and the organisations paid directly in 2025; the "
                        "call is the three countries with the most members' money spent",
        "as_of": "2026-10-09",
        "deliverables": ["coordination_offices_2027.pptx", "member_funds_by_country.csv"],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task451/generator/build.py (seeded, deterministic) in the "
                               "layouts of IATI activity XML (version 2.03), the IATI Datastore's flattened transaction "
                               "export and the IATI Registry's publisher list, around a fictional donor collaborative, "
                               "its members, two pooled funds and the organisations they fund; no real organisation, "
                               "person or activity is depicted.",
                     "date": "2026-10-09", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-09",
        "generator": "task451/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
