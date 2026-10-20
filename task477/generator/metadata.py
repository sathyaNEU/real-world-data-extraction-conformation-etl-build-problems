"""metadata.json: files with source, date and license, the distractors, the deliverables."""
import json

import world as W

DATES = {"qcew_a": "2026-06-11", "qcew_b": "2026-03-11", "qcew_c": "2026-06-11", "layout": "2026-06-11",
         "areas": "2026-06-11", "industries": "2026-06-11", "guidelines": "2026-08-03", "exits": "2026-09-30",
         "wages": "2026-09-22", "employers": "2026-08-31", "peo": "2026-07-01", "ita": "2026-09-30",
         "register": "2026-09-30", "etpl": "2026-06-30", "manual": "2025-02-19", "projections": "2026-05-19",
         "oews": "2026-04-02"}
SOURCE = {"qcew_a": W.AGENCY, "qcew_b": W.AGENCY, "qcew_c": W.AGENCY, "layout": W.AGENCY, "areas": W.AGENCY,
          "industries": W.AGENCY, "guidelines": "State Workforce Development Council", "exits": W.BOARD,
          "wages": W.AGENCY, "employers": W.AGENCY, "peo": W.AGENCY, "ita": W.BOARD, "register": W.BOARD,
          "etpl": W.AGENCY, "manual": W.BOARD, "projections": W.AGENCY, "oews": W.AGENCY}


def write(path, x, n):
    files = [dict(file=fn, source="%s (fictional), synthetic records" % SOURCE[k], date=DATES[k],
                  license="CC0-1.0 (synthetic, generated for this task)", rows=n.get(k))
             for k, fn in sorted(W.FILES.items(), key=lambda t: t[1])]
    meta = dict(task="task477", title="Tallis Valley 2027-2029 sector-partnership slate",
                setting="A fictional one-county workforce board in an unnamed U.S. state (state code 52); every record "
                        "is synthetic.",
                as_of="2026-10-14", files=files,
                distractors=[dict(file=W.FILES["projections"], why="projected employment growth by industry: a "
                                  "measure the Fund's ranking does not use"),
                             dict(file=W.FILES["oews"], why="occupational hourly wages from an establishment survey: "
                                  "not pay per job by industry, and not comparable across years")],
                deliverables=[W.GOLDEN["table"], W.GOLDEN["memo"]])
    json.dump(meta, open(path, "w", encoding="utf-8"), indent=1)
