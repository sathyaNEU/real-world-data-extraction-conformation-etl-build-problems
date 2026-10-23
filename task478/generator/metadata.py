"""metadata.json: the files with source, date and licence, the distractors, the deliverables."""
import json

import pack as P

DATES = {"plan": "2027-02-19", "guidance": "2027-02-17", "cems": "2027-02-08", "tests_old": "2027-02-09",
         "tests_new": "2027-02-09", "statements": "2027-02-16", "permits": "2027-02-10", "events": "2027-02-11",
         "billing": "2027-02-03", "engine_logs": "2027-02-12", "inspections": "2027-02-12", "no2": "2027-01-20",
         "onroad": "2026-12-08"}
SOURCE = {"plan": "Planning and Rules Division", "guidance": "Engineering Division",
          "cems": "continuous emissions monitoring data system", "tests_old": "source test results database (to 2021)",
          "tests_new": "source test results database (from 2022)", "statements": "emission statements database",
          "permits": "permit system, device list", "events": "compliance tracking system",
          "billing": "Tamsett Valley Gas (fictional) under the District's data sharing agreement",
          "engine_logs": "facilities' Rule 4702 operating logs as submitted", "inspections": "engine inspection records",
          "no2": "community air monitoring network", "onroad": "Mobile Sources Section, county-scale MOVES run"}


def write(path, n):
    files = [dict(file=fn, source="Tamsett Basin Air Pollution Control District (fictional), %s; synthetic records"
                  % SOURCE[k], date=DATES[k], license="CC0-1.0 (synthetic, generated for this task)", rows=n.get(k))
             for k, fn in sorted(P.FILES.items(), key=lambda t: t[1])]
    meta = dict(task="task478", title="Tamsett Basin APCD, Lowry Creek NOx reduction agreements 2027",
                setting="A fictional regional air pollution control district in an unnamed U.S. state; every record is "
                        "synthetic.",
                as_of="2027-02-19", files=files,
                distractor_files=[P.FILES["no2"], P.FILES["onroad"]],
                distractors=[dict(file=P.FILES["no2"], why="the corridor's community NO2 monitors: what residents "
                                  "breathe from every source, not what each facility's units emitted"),
                             dict(file=P.FILES["onroad"], why="on-road NOx on the corridor's road links: traffic "
                                  "emissions the plan's facility agreements do not cover")],
                deliverables=["tbapcd_cerp_facilities_2027.xlsx", "tbapcd_nox_inventory_2026.csv",
                              "tbapcd_facility_nox_2026.svg"],
                stated_inputs=["Rule 4306 units", "five of fourteen facilities", "calendar 2026"])
    json.dump(meta, open(path, "w", encoding="utf-8"), indent=1)
