"""metadata.json: the pack's files with source, date and license, the distractors, the deliverables."""
import json

import pack as P
import world as W

SOURCES = {
    "guidelines": ("City of Carrow, Community Development Department (fictional)", "2027-01-04"),
    "neighbourhoods": ("City of Carrow, Community Development Department (fictional)", "2027-03-15"),
    "tract18": ("Synthetic, in the layout of a U.S. Census Bureau ACS 5-year detailed table download (2014-2018)",
                "2019-12-19"),
    "tract23": ("Synthetic, in the layout of a U.S. Census Bureau ACS 5-year detailed table download (2019-2023)",
                "2024-12-12"),
    "bg18": ("Synthetic, ACS 5-year block-group layout (2014-2018)", "2019-12-19"),
    "bg23": ("Synthetic, ACS 5-year block-group layout (2019-2023)", "2024-12-12"),
    "tractrel": ("Synthetic, in the layout of the Census Bureau's 2020 to 2010 tract relationship file", "2021-12-01"),
    "blockrel": ("Synthetic, in the layout of the Census Bureau's 2010 to 2020 block relationship file", "2021-04-26"),
    "pl2010": ("Synthetic, in the layout of a 2010 Census P.L. 94-171 block table download", "2011-03-15"),
    "parcels": ("City of Carrow open data extract (fictional)", "2027-03-15"),
    "cases": ("City of Carrow code enforcement export (fictional)", "2027-03-15"),
    "events": ("City of Carrow code enforcement export (fictional)", "2027-03-15"),
    "payments": ("City of Carrow Neighborhood Stabilization Fund payment journal (fictional)", "2027-03-15"),
    "notes": ("City of Carrow open data extract notes (fictional)", "2027-03-15"),
}


def write(path, x, n):
    files = []
    for k, fn in sorted(W.FILES.items(), key=lambda t: t[1]):
        src, date = SOURCES[k]
        files.append(dict(file=fn, source=src, date=date, license="CC0-1.0 (synthetic, generated for this task)",
                          rows=n.get(k)))
    meta = dict(task="task476", title="Carrow Neighborhood Stabilization Fund 2027 designations",
                setting="A fictional city in an unnamed U.S. state; every record is synthetic.",
                as_of=W.AS_OF, files=files,
                distractors=[dict(file=W.FILES["pl2010"], why="2010 block populations: relevant to weighting a crosswalk, "
                                  "unused by the solution"),
                             dict(file=W.FILES["bg23"], why="2019-2023 block groups: the 2020 tracts publish their own "
                                  "estimates, unused by the solution")],
                deliverables=[W.GOLDEN["workbook"], W.GOLDEN["memo"]],
                stated_inputs=sorted({P.tract_name(code) for t in x["ts"] if t.nbhd for code, _ in t.children}))
    json.dump(meta, open(path, "w", encoding="utf-8"), indent=1)
