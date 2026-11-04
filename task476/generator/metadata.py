"""metadata.json: every pack file with its source, date, licence and row count, the distractors and why each is
unused, and the deliverables."""
import json
import os
import sqlite3

import world as W

LIC = "CC0-1.0 (synthetic, generated for this task)"
SRC = {
    "db": "%s inventory database (FieldCruise backend), fictional; synthetic records" % W.COMPANY,
    "t2026": "%s 2026 contract remeasurement export, fictional; synthetic records" % W.CONTRACTOR,
    "revisit": "%s September 2026 return-visit export, fictional; synthetic records" % W.CONTRACTOR,
    "register": "%s plot register, fictional; synthetic records" % W.COMPANY,
    "species": "%s species list with FIA codes (codes as published by the USDA Forest Service FIA program)" % W.COMPANY,
    "manual": "%s field manual, fictional; synthetic document" % W.COMPANY,
    "stands": "%s GIS stand table, fictional; synthetic records" % W.COMPANY,
    "policy": "%s board policy, fictional; synthetic document" % W.COMPANY,
    "burns": "%s burn unit reports, fictional; synthetic document" % W.COMPANY,
    "fire": "%s fire report, fictional; synthetic document" % W.COMPANY,
    "ads": "aerial detection survey polygons in the style of the USDA Forest Service Region 5 survey, fictional; synthetic",
    "logs": "delivered log price sheet in the style of a regional mill posting, fictional; synthetic",
}
DATES = {"db": "2026-05-28", "t2026": "2026-09-02", "revisit": "2026-09-21", "register": "2026-09-29",
         "species": "2026-04-12", "manual": "2026-04-12", "stands": "2026-09-30", "policy": "2026-08-14",
         "burns": "2024-12-03", "fire": "2025-10-17", "ads": "2026-02-10", "logs": "2026-10-01"}
DISTRACTORS = [
    {"file": W.FILES["ads"], "why": "insect activity mapped from aircraft by polygon in July 2025: a survey of "
                                    "discoloured crowns, not a plot measurement, and it predates the 2026 remeasurement"},
    {"file": W.FILES["logs"], "why": "delivered log prices for the third quarter of 2026: a market sheet the board "
                                     "uses for sale planning; Policy 7.4 marks stands on measured basal area, not value"},
]


def write(path, n):
    target = os.path.join(os.path.dirname(path), "target")
    key = {v: k for k, v in W.FILES.items()}
    files = []
    for root, _, fs in os.walk(target):
        for f in sorted(fs):
            rel = os.path.relpath(os.path.join(root, f), target)
            k = key[rel]
            rows = None
            if rel.endswith(".csv"):
                rows = sum(1 for _ in open(os.path.join(root, f), encoding="utf-8")) - 1
            elif rel.endswith(".sqlite"):
                con = sqlite3.connect(os.path.join(root, f))
                rows = {t: con.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]
                        for (t,) in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")}
                con.close()
            files.append({"path": rel, "source": SRC[k], "date": DATES[k], "license": LIC, "rows": rows,
                          "role": "distractor" if k in ("ads", "logs") else "input"})
    files.sort(key=lambda r: r["path"])
    meta = {"task": "task476",
            "title": "2027 salvage marking under the board's salvage policy",
            "setting": "A fictional family-owned timber company's tree farm in California's northern Sierra Nevada; "
                       "every record is synthetic.",
            "as_of": "2026-10-01", "files": files, "distractor_files": [d["file"] for d in DISTRACTORS],
            "distractors": DISTRACTORS,
            "deliverables": ["tree_fates_2021_2026.csv", "salvage_marking_2027.pdf"]}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
