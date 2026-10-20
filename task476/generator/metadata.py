"""metadata.json: files with source, date and license, the distractors, the deliverables."""
import json

import world as W

DATES = {"guidelines": "2027-01-11", "finds": "2027-03-15", "odor": "2027-03-15", "repairs": "2027-03-15",
         "schedule": "2027-03-15", "mains": "2026-12-31", "notes": "2027-03-15", "costs": "2027-03-15",
         "closeouts": "2027-03-15", "tickets": "2027-03-15", "meters": "2027-03-15", "customers": "2027-01-12",
         "lauf": "2027-02-16"}


def write(path, x, n):
    files = [dict(file=fn, source="%s (fictional), synthetic records" % W.UTILITY, date=DATES[k],
                  license="CC0-1.0 (synthetic, generated for this task)", rows=n.get(k))
             for k, fn in sorted(W.FILES.items(), key=lambda t: t[1])]
    meta = dict(task="task476", title="Hollister Gas accelerated main replacement designations 2027",
                setting="A fictional city-owned gas utility in an unnamed U.S. state; every record is synthetic.",
                as_of=W.EXTRACT.isoformat(), files=files,
                distractors=[dict(file=W.FILES["customers"], why="customers by district: a per-customer normalisation "
                                  "the guidelines do not use"),
                             dict(file=W.FILES["lauf"], why="lost and unaccounted-for gas: a system-wide leakage "
                                  "proxy not allocated to districts")],
                deliverables=[W.GOLDEN["workbook"], W.GOLDEN["memo"]])
    json.dump(meta, open(path, "w", encoding="utf-8"), indent=1)
