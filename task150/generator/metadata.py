"""Write task150/metadata.json from the built pack."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AS           # noqa: E402
import deliver as DL        # noqa: E402
import docs as DOC          # noqa: E402
import records as R         # noqa: E402

TASK = os.path.dirname(HERE)
ASOF = "2026-10-09"
SOURCES = {
    R.F_LEGACY: "Sorrel Creek RE-6 legacy student information system, October membership snapshots 2013-14 to 2018-19 "
                "(pipe-delimited archive export)",
    R.F_MEMBERS: "Sorrel Creek RE-6 student information system, October membership snapshots 2019-20 to 2026-27",
    R.F_XWALK: "Sorrel Creek RE-6 student information system, 2019 conversion crosswalk of legacy student numbers to "
               "state IDs",
    R.F_CODES: "Sorrel Creek RE-6 student information system, elementary school codes (legacy and state)",
    R.F_BIRTHS: "Brandt County Public Health, Vital Records: resident live births by RE-6 attendance area, 2008 to 2025",
    AS.F_SECTIONS: "Sorrel Creek RE-6 student information system, elementary sections scheduled for 2026-27",
    AS.F_SECT_ENR: "Sorrel Creek RE-6 student information system, pupil lines in the fall 2026 elementary sections",
    AS.F_PRESCHOOL: "Sorrel Creek RE-6 preschool registration platform, enrollments at the elementary sites, 2026-27",
    AS.F_ECSE: "Sorrel Creek RE-6 Special Education Department, early childhood special education roster on "
               "10/01/2026",
    DOC.F_POLICY: "Sorrel Creek RE-6 Board of Education, Policy FEA-R2 Elementary Classroom Placement (2025 Bond "
                  "Program), adopted 03/12/2026",
    DOC.F_CAPACITY: "Sorrel Creek RE-6 Facilities and Operations, elementary school capacity report 2026-27",
    DOC.F_SIS_NOTES: "Sorrel Creek RE-6 Student Information Systems, notes on the student-system files",
    DOC.F_BIRTH_NOTES: "Brandt County Public Health, Vital Records: notes on the births file",
    DOC.F_MANIFEST: "Sorrel Creek RE-6 Planning and Enrollment Office, manifest of the October 2026 pull",
    DOC.F_FCA: "Sorrel Creek RE-6 Facilities and Operations, facility condition assessment of the elementary schools, "
               "spring 2025",
    DOC.F_MEALS: "Sorrel Creek RE-6 Nutrition Services, meal benefit eligibility of K-5 pupils on the October 1, 2026 "
                 "count",
}
DISTRACTORS = [DOC.F_FCA, DOC.F_MEALS]


def rows_of(path):
    if path.endswith(".csv") or path.endswith(".txt") and "membership" in path:
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": ASOF,
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task150",
        "title": "Where a suburban Colorado school district's 2025 bond places its 24 new elementary classrooms under "
                 "the board's placement standard, from each school's projected enrollment over 2028-29 to 2032-33",
        "domain": "Sociology & Demography",
        "client_domain": "Sociology & Demography",
        "subdomain": "population-estimation-demographic-projection (a small-area cohort-component projection of each "
                     "attendance area's K-5 pupils: cohorts aged through grades, kindergartens from births five years "
                     "earlier, exits and moves between areas as rates on the area a pupil leaves, arrivals from outside "
                     "the district as counts)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a placement schedule for seven schools (each school's classroom need and classrooms placed), "
                        "two October 1, 2026 tables (homeroom classes by grade band at seven schools; preschool children "
                        "and classrooms at four sites), and a seven-panel enrollment chart",
        "as_of": ASOF,
        "deliverables": [DL.F_BOOK, DL.F_CHART],
        "distractor_files": DISTRACTORS,
        "stated_inputs": [],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{
            "files": "all files under target/",
            "origin": "constructed for this task by task150/generator/build.py (seeded, deterministic) around a "
                      "fictional Colorado school district (Sorrel Creek School District RE-6, Brandt County), its "
                      "schools, board, county vital records office and their systems; no real organisation, person or "
                      "system is depicted. Grade, entry and school code conventions follow common Colorado student "
                      "information practice; the board policy code follows the NEPN/NSBA classification.",
            "date": ASOF,
            "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-16",
        "generator": "task150/generator/build.py",
        "files": files,
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
