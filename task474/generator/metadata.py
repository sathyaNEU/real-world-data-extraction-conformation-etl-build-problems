"""metadata.json: files with source, date and license, the distractors, the deliverables."""
import json

import world as W

DATES = {"claims": "2026-11-02", "roster": "2026-11-02", "remit": "2026-11-02", "notes": "2026-11-02",
         "groups": "2026-07-01", "rules": "2026-03-02", "rx": "2026-11-02", "classes": "2026-09-14",
         "quality": "2026-06-19", "survey": "2026-01-22"}
SOURCE = {"remit": W.STATE_AGENCY, "rx": "%s, pharmacy benefit manager feed" % W.PLAN}


def write(path, x, n):
    files = [dict(file=fn, source="%s (fictional), synthetic records" % SOURCE.get(k, W.PLAN), date=DATES[k],
                  license="CC0-1.0 (synthetic, generated for this task)", rows=n.get(k))
             for k, fn in sorted(W.FILES.items(), key=lambda t: t[1])]
    meta = dict(task="task474", title="Prairie Hills Health Plan Cost Performance Program 2027 designations",
                setting="A fictional Medicaid managed care plan in an unnamed U.S. state; every record is synthetic.",
                as_of="2026-11-09", files=files,
                distractors=[dict(file=W.FILES["quality"], why="2025 HEDIS quality rates by group: quality, not "
                                  "cost, and a different year"),
                             dict(file=W.FILES["survey"], why="2025 member experience survey by group: satisfaction, "
                                  "not cost or enrollment")],
                deliverables=[W.GOLDEN["workbook"], W.GOLDEN["memo"]],
                stated_inputs=["%.2f" % W.BENCHMARK])
    json.dump(meta, open(path, "w", encoding="utf-8"), indent=1)
