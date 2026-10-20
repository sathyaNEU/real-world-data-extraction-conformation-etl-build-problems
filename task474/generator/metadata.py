"""metadata.json: files with source, date and license, the distractors, the deliverables."""
import json

import world as W

DATES = {"stations": "2026-10-19", "register": "2026-07-01", "dot": "2026-10-05", "county": "2026-09-29",
         "consultant": "2026-10-02", "links": "2026-10-22", "rates": "2026-02-11", "rules": "2026-01-14",
         "notes": "2026-10-26", "gates": "2026-10-23", "fleet": "2026-10-20", "no2": "2026-10-15", "certs": "2026-05-12",
         "complaints": "2026-10-21"}
SOURCE = {"stations": W.DOT, "register": W.DOT, "dot": W.DOT, "county": W.COUNTY, "consultant": W.CONSULTANT,
          "no2": "State Department of Environmental Protection, Air Monitoring",
          "complaints": "City of Bayline 311 service requests"}


def write(path, e, n):
    files = [dict(file=fn, source="%s (fictional), synthetic records" % SOURCE.get(k, W.PORT), date=DATES[k],
                  license="CC0-1.0 (synthetic, generated for this task)", rows=n.get(k))
             for k, fn in sorted(W.FILES.items(), key=lambda t: t[1]) if k in DATES]
    meta = dict(task="task474", title="Bayline Port Authority Air Corridor Program 2027 designations",
                setting="A fictional port authority in an unnamed U.S. coastal state; every record is synthetic.",
                as_of="2026-10-26", files=files,
                distractors=[dict(file=W.FILES["no2"], why="ambient NO2 at two monitors: air quality, not the "
                                  "NOx any link's traffic emits"),
                             dict(file=W.FILES["complaints"], why="311 truck complaints by street: where residents "
                                  "notice trucks, not the NOx a link's traffic emits")],
                deliverables=[W.GOLDEN["workbook"], W.GOLDEN["memo"]],
                stated_inputs=["%.2f" % W.LINE])
    json.dump(meta, open(path, "w", encoding="utf-8"), indent=1)
