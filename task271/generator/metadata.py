"""Write task271/metadata.json from the built pack: the distractors, the input gates and every shipped file's source,
date and licence."""
import json
import os

import docs as DOC
import pack as P

SOURCES = {
    P.F_REGISTER: "Pelloran Plateau Fisheries Society, lake register (revised 14 April 2026)",
    P.F_COUNTS: "Pelloran Plateau creel survey, aerial count file as keyed by the observers after each loop, 2026 season "
                "(exported 23 October 2026)",
    P.F_INTERVIEWS: "Pelloran Plateau creel survey, access interviews from the clerks' tablets, 2026 season (exported "
                    "23 October 2026)",
    P.F_FLIGHTLOG: "Vellacott Air, flight log for the society's survey charter, 2026",
    P.F_TRIPS: "Quillet Creek Hatchery, release trip sheets, 2026",
    P.F_DROPS: "Quillet Creek Hatchery, drop crew tally app export (2 September 2026)",
    P.F_SAMPLES: "Quillet Creek Hatchery, Monday raceway sample counts and inventory, 2026",
    P.F_RACEWAYS: "Quillet Creek Hatchery, raceway numbering from the new headbox (22 June 2026)",
    P.F_LOGGERS: "Pelloran Plateau Fisheries Society, compiled temperature logger downloads, 2026",
    P.F_DEPLOY: "Pelloran Plateau Fisheries Society, temperature logger deployment sheet, 2026",
    P.F_CAMP: "Recreation Sites and Trails, nightly occupancy at the plateau's lakeside recreation sites, 2026 season",
    DOC.F_POLICY: "Pelloran Plateau Fisheries Society, Catchable Trout Allocation Policy, 2026 revision (12 March 2026)",
    DOC.F_PROTOCOL: "Pelloran Plateau Creel Survey 2026, field protocol (28 April 2026)",
}
DISTRACTORS = [P.F_CAMP, P.F_FLIGHTLOG]
TITLE = ("Which of a lake-stocking society's lakes go into its 2027 high-use catchable tier on 2026 open-water "
         "angler-hours per hectare, the creel survey's route-timed flight counts read against each lake's own "
         "hour-by-hour presence from the access interviews")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        return sum(max(sum(1 for _ in ws.iter_rows(values_only=True)) - 1, 0) for ws in wb.worksheets)
    if path.endswith(".json"):
        return len(json.load(open(path))["records"])
    return None


def write(task_dir):
    target = os.path.join(task_dir, "target")
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": "2026-10-26",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task271",
        "title": TITLE,
        "domain": "Survey Research & Official Statistics",
        "client_domain": "Survey Research & Official Statistics",
        "subdomain": "sample-design-allocation-weighting (a lake-stocking society's creel survey: each lake's "
                     "open-water angler-hours per hectare from aerial counts flown at route-fixed hours and the "
                     "access interviews' start and finish times)",
        "objective": "Descriptive & Distribution Analysis",
        "prompt_shape": "a tier for every lake that takes catchables against the allocation policy's high-use line with "
                        "a bar chart, and two per-lake tables (the catchables each lake received alive in 2026; the "
                        "July and August warm days at each lake's 1 m logger)",
        "as_of": "2026-10-26",
        "deliverables": ["stocking_tiers_2027.xlsx", "stocking_board_note_2027.docx"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task271/generator/build.py (seeded, deterministic) around "
                               "a fictional British Columbia lake-stocking society, its hatchery, its creel survey "
                               "and a floatplane operator, in the layouts of an aerial count file, access-interview "
                               "tablet exports, hatchery trip sheets and a drop tally app, temperature logger downloads "
                               "and a recreation sites occupancy export; no real organisation's records or person is "
                               "depicted.",
                     "date": "2026-10-26", "license": "CC0-1.0 (original work)"}],
        "created": "2026-11-01",
        "generator": "task271/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
