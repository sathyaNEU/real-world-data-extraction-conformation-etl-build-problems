"""metadata.json for the task folder (outside target/)."""
import json
import os

import pandas as pd

from build import FILES, DISTRACTORS, TASK

DESC = {
    "facts": ("Data platform mart mp_card_week: card x ISO week sales, margin and reward cost, 2026-W15 to W34", "2026-09-14"),
    "alloc": ("Offer engine allocation register for the summer 2026 test ST26", "2026-09-14"),
    "cards": ("CRM member card master", "2026-09-14"),
    "memb": ("CRM membership master", "2026-09-14"),
    "branches": ("Branch register, January 2026 edition", "2026-01-12"),
    "notice": ("Network planning notice: branch closures and regional changes from 1 July 2026", "2026-06-12"),
    "standard": ("Programme analytics standard MP-3, revision 3: how offers are measured and budgeted", "2026-03-18"),
    "catalogue": ("CRM test catalogue for ST26: cells, allocation, offer mechanics", "2026-05-26"),
    "plan": ("Programme finance plan 2027: active cards by region and the budget lines", "2026-09-09"),
    "notes": ("Data platform field notes for the handover extracts", "2026-09-11"),
    "log": ("Data platform extract log for the 14 September 2026 handover", "2026-09-14"),
    "footfall": ("Store door-counter visits by branch and ISO week", "2026-09-14"),
    "panel": ("External market research panel, June 2026 wave, summary tables", "2026-07-06"),
    "competitors": ("Monthly competitor basket price checks near each branch", "2026-09-01"),
}


def write(target=None):
    target = target or os.path.join(TASK, "target")
    files = []
    for k, name in FILES.items():
        path = os.path.join(target, name)
        ext = os.path.splitext(name)[1][1:]
        rows = None
        if ext == "csv":
            rows = int(sum(1 for _ in open(path, encoding="utf-8")) - 1)
        elif ext == "parquet":
            rows = int(len(pd.read_parquet(path, columns=["card_no"])))
        e = {"path": name, "format": ext, "bytes": os.path.getsize(path)}
        if rows is not None:
            e["rows"] = rows
        e.update({"source": "Constructed: " + DESC[k][0], "date": DESC[k][1],
                  "license": "CC0-1.0 (original work, constructed for this task)"})
        files.append(e)
    meta = {
        "task": "task131",
        "title": "Choosing the 2027 member card offer for a Swiss consumer co-operative from a card-randomised summer test",
        "domain": "Marketing & Consumer Research",
        "subdomain": "crm-loyalty-retention",
        "objective": "Experiment & Causal Analysis",
        "prompt_shape": "07 (grid of cells): six regions by four offers on net margin per active card-week, plus the four offers' 2027 programme values",
        "as_of": "2026-10-12",
        "deliverables": ["programme_offer_2027.docx", "offer_grid_2027.png"],
        "distractor_files": [FILES[k] for k in DISTRACTORS],
        "input_gates": {
            "files": len(FILES),
            "formats": sorted({f["format"] for f in files}),
            "largest_file": FILES["facts"],
            "largest_file_rows": next(f["rows"] for f in files if f["path"] == FILES["facts"]),
        },
        "sources": [{
            "files": "all files under target/",
            "origin": "constructed for this task by task131/generator/build.py (seeded, deterministic) around a fictional consumer co-operative (Talwerk Genossenschaft) with real eastern Swiss towns and postcodes; no real member, card or transaction is depicted.",
            "date": "2026-10-10",
            "license": "CC0-1.0 (original work)",
        }],
        "created": "2026-10-10",
        "generator": "task131/generator/build.py",
        "files": files,
    }
    with open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


if __name__ == "__main__":
    write()
