"""metadata.json: every pack file with its source, date, licence and row count, the distractors and why each is
unused, and the deliverables."""
import json
import os

import world as W

LIC = "CC0-1.0 (synthetic, generated for this task)"
SRC = {
    "stage": "gauge BP-1 stage logger export (%s for %s), fictional; synthetic records" % (W.CONSULTANT, W.COMPANY),
    "register": "%s station register for gauge BP-1, fictional; synthetic records" % W.CONSULTANT,
    "rating_report": "%s Rating 7 memorandum, fictional; synthetic document" % W.CONSULTANT,
    "visits": "%s 2026 field visit log, fictional; synthetic records" % W.CONSULTANT,
    "temp": "gauge BP-1 water temperature logger export, fictional; synthetic records",
    "release": "%s plant bypass release log, fictional; synthetic records" % W.COMPANY,
    "generation": "%s plant daily generation, fictional; synthetic records" % W.COMPANY,
    "license": "%s license articles (excerpt), fictional; synthetic document" % W.PROJECT,
    "plan": "%s flow monitoring plan, fictional; synthetic document" % W.PROJECT,
    "precip": "%s powerhouse rain gauge, fictional; synthetic records" % W.COMPANY,
    "prior": "%s 2025 annual flow compliance report, fictional; synthetic document" % W.COMPANY,
}
DATES = {"stage": "2026-11-04", "register": "2026-05-02", "rating_report": "2023-10-12", "visits": "2026-10-06",
         "temp": "2026-11-04", "release": "2026-11-02", "generation": "2026-11-02", "license": "2019-06-11",
         "plan": "2024-03-18", "precip": "2026-11-02", "prior": "2026-01-22"}
DISTRACT = {"temp", "generation", "precip"}
DISTRACTORS = [
    {"file": W.FILES["temp"], "why": "water temperature at BP-1 for the license's temperature monitoring; it carries no "
                                     "flow"},
    {"file": W.FILES["generation"], "why": "the unit's daily energy and run hours: the plant's own production record, "
                                           "not a measure of the bypassed reach"},
    {"file": W.FILES["precip"], "why": "daily rain at the powerhouse: weather, not flow"},
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
            files.append({"path": rel, "source": SRC[k], "date": DATES[k], "license": LIC, "rows": rows,
                          "role": "distractor" if k in DISTRACT else "input"})
    files.sort(key=lambda r: r["path"])
    meta = {"task": "task476", "title": "2026 bypassed-reach minimum flow report",
            "setting": "A fictional run-of-river hydroelectric project in Oregon's western Cascade foothills; every record "
                       "is synthetic.",
            "as_of": "2026-11-04", "files": files, "distractor_files": [d["file"] for d in DISTRACTORS],
            "distractors": DISTRACTORS,
            "deliverables": ["bypass_flow_record_2026.xlsx", "minimum_flow_deviation_report_2026.docx"]}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
