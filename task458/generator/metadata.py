"""metadata.json: every shipped file's source, as-of date, licence, format, rows and role, and the named distractors."""
import json
import os

from docs import PROVENANCE
from pack import DISTRACTORS, FILES

LICENCE = ("Synthetic data generated for this task by the author's generator (task458/generator); no third-party "
           "content. Released for evaluation use under CC BY 4.0.")


def write(target, path, rows):
    prov = {k: (src, d, desc) for k, src, d, desc in PROVENANCE}
    files = []
    for k, fn in FILES.items():
        src, d, desc = prov[k]
        files.append({"file": fn, "format": fn.rsplit(".", 1)[1], "source": src, "as_of": d, "licence": LICENCE,
                      "description": desc, "rows": rows.get(k), "bytes": os.path.getsize(os.path.join(target, fn)),
                      "role": "distractor" if k in DISTRACTORS else "evidence"})
    meta = {
        "task": "task458",
        "title": "Ashlund Home Group FY2026 stock provision and borrowing base",
        "objective": "Data Extraction & Conformation (ETL)",
        "domain": "General Statistics & Data Science (house domain: Accounting, Audit & Forensic Analytics)",
        "task_type": "data-integration-record-linkage-entity-resolution",
        "setting_date": "2027-01-22",
        "files": files,
        "distractors": [{"file": FILES[k], "why_relevant": w, "why_unused": u} for k, w, u in (
            ("open_po", "Purchases still to arrive add to stock in 2027.",
             "The provision measures stock held at 31 December 2026 (FIN-07 2.5); orders not yet received are not in it."),
            ("pallets", "Warehouse occupancy shows how full the distribution centres were with the stock being provided for.",
             "Occupancy measures space, not the cost, the demand or the disposal proceeds of any line."))],
        "generator": "task458/generator/build.py",
    }
    with open(path, "w") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")
    return meta
