"""metadata.json: files with source, date and license, the distractors, the deliverables."""
import json

import world as W

DATES = {"census": "2023-05-25", "acs": "2025-12-15", "metro": "2026-10-05", "county": "2026-10-02",
         "civic": "2026-10-06", "demo": "2026-10-06", "gq": "2026-06-30", "utility": "2026-04-20", "codes": "2025-01-08",
         "rules": "2026-02-17", "notes": "2026-10-14", "schools": "2025-11-03", "voters": "2026-09-01"}
SOURCE = {"utility": W.UTILITY, "metro": "Metro permit system (fictional cities)", "civic": "Civic permit system",
          "county": "County Building Department", "schools": "State Department of Education",
          "voters": "Secretary of State, Elections Division"}


def write(path, e, n):
    files = [dict(file=fn, source="%s (fictional), synthetic records" % SOURCE.get(k, W.OFFICE), date=DATES[k],
                  license="CC0-1.0 (synthetic, generated for this task)", rows=n.get(k))
             for k, fn in sorted(W.FILES.items(), key=lambda t: t[1])]
    meta = dict(task="task484", title="2027 municipal revenue-sharing tiers",
                setting="A fictional state's population estimates unit and twelve fictional cities; every record is "
                        "synthetic.",
                as_of="2026-10-14", files=files,
                distractors=[dict(file=W.FILES["schools"], why="school enrollment by city: children enrolled, not "
                                  "residents, and a different date"),
                             dict(file=W.FILES["voters"], why="voter registration by city: registered adults, "
                                  "including inactive registrations, not residents")],
                deliverables=[W.GOLDEN["workbook"], W.GOLDEN["memo"]],
                stated_inputs=["50,000"])
    json.dump(meta, open(path, "w", encoding="utf-8"), indent=1)
