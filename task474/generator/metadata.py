"""metadata.json: files with source, date and license, the distractors, the deliverables."""
import json

import world as W

DATES = {"dahs": "2026-10-19", "notes": "2026-10-19", "units": "2026-06-30", "tickets": "2026-10-19",
         "guidelines": "2026-01-12", "invoices": "2026-10-15", "terms": "2024-10-28", "events": "2026-10-16",
         "ozone": "2026-10-05", "allowances": "2026-10-01"}
SOURCE = {"dahs": W.COOP, "notes": W.COOP, "units": W.COOP, "tickets": W.COOP, "guidelines": W.COOP,
          "invoices": "Prairie Basin Gas Marketing LLC", "terms": "Prairie Basin Gas Marketing LLC", "events": W.COOP,
          "ozone": "State Department of Environmental Quality", "allowances": W.COOP}


def write(path, x, n):
    files = [dict(file=fn, source="%s (fictional), synthetic records" % SOURCE[k], date=DATES[k],
                  license="CC0-1.0 (synthetic, generated for this task)", rows=n.get(k))
             for k, fn in sorted(W.FILES.items(), key=lambda t: t[1])]
    meta = dict(task="task474", title="Ridgeline Power Cooperative SCR Upgrade Program 2027 designations",
                setting="A fictional generation and transmission cooperative in an unnamed U.S. state; every record is "
                        "synthetic.",
                as_of="2026-11-09", files=files,
                distractors=[dict(file=W.FILES["ozone"], why="ambient ozone at the region's monitors: air quality, "
                                  "not any unit's emissions"),
                             dict(file=W.FILES["allowances"], why="allowance holdings by facility: a compliance "
                                  "position, not a unit's emission rate"),
                             dict(file=W.FILES["invoices"], why="the gas supplier's invoices: what the plants paid "
                                  "for gas, neither emissions nor outages"),
                             dict(file=W.FILES["terms"], why="the gas supply agreement: the gas day and the price "
                                  "basis, which no answer uses")],
                deliverables=[W.GOLDEN["workbook"], W.GOLDEN["memo"]],
                stated_inputs=["%.3f" % W.TARGET])
    json.dump(meta, open(path, "w", encoding="utf-8"), indent=1)
