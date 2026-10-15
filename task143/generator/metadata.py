"""Write task143/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    K.F_POLICY: "Product Finance policy FIN-RS-04, battery warranty reserve at lot release, revision 3",
    K.F_MEMO: "Battery Reliability Lab memo QM-07, release model RL-3, revision 4",
    K.F_SPEC: "Model K battery pack specification, revision D (Product Engineering)",
    K.F_README: "The battery reliability lab's and battery plant's note on the release extracts",
    K.F_README_SVC: "Service Operations' note on the service and costing extracts",
    K.F_CYC_A: "Cycler fleet A export of the first 100 QP-3 cycles of release-test cells",
    K.F_CYC_B: "Cycler fleet B export of the first 100 QP-3 cycles of release-test cells",
    K.F_REG: "Release test register of the battery reliability lab",
    K.F_LIFE: "Life test results of the finished lots' release-test cells",
    K.F_CELLS: "Zelvora cell data package for lot ZC2638",
    K.F_GEN: "Line MES genealogy of the Model K packs built from lot ZC2638",
    K.F_MODEL_J: "Line MES genealogy of the Model J packs built from lot ZC2638",
    K.F_COA: "Zelvora certificate of analysis for lot ZC2638",
    K.F_CASES: "Service case system extract, Model K battery cases, September 2024 to September 2026",
    K.F_SAP: "DACH depot SAP service orders, September 2024 to 1 March 2026",
    K.F_RETURNS: "Bielefeld returns depot goods-receipt log of returned batteries",
    K.F_CARRIER: "Carrier statement of inbound consignments of returned batteries",
    K.F_INV["FRB"]: "Dauvergne Réparation invoices to Service Operations",
    K.F_INV["UKI"]: "Tolley Marsh Repair invoices to Service Operations",
    K.F_INV["NOR"]: "Ljungqvist Service invoices to Service Operations",
    K.F_INV["SOU"]: "Ferrucci Assistenza invoices to Service Operations",
    K.F_FX: "Treasury month-end exchange rates",
    K.F_COST: "Service Operations controlling cost sheet FY2026",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2026-10-12",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task143",
        "title": "How many of Zelvora cell lot ZC2638's 7,200 Model K packs Kalvenhorst Systeme reserves for at "
                 "release: the packs expected to fall below 80 per cent of rated capacity within the 600-cycle "
                 "warranty",
        "domain": "General Statistics & Data Science",
        "client_domain": "General Statistics & Data Science",
        "subdomain": "bayesian-modeling-posterior-inference (the posterior predictive for the members of new groups: "
                     "the chance that the weakest of a pack's three cells from one new formation tray falls below the "
                     "warranty line, under the between-tray variance of the release model's error)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "single-figure: the reserve in packs, with two 2025-26 tables (the four repair partners' "
                        "capacity replacements under the warranty and their average cost, the capacity replacements "
                        "carried out each month) and one chart",
        "as_of": "2026-10-15",
        "deliverables": [K.GOLD_BOOK, K.GOLD_NOTE],
        "distractor_files": list(K.DISTRACTORS),
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task143/generator/build.py (seeded, deterministic) around "
                               "a fictional German notebook maker (Kalvenhorst Systeme GmbH, Bielefeld), its battery "
                               "plant, reliability lab, service depot and people, a fictional Czech cell supplier "
                               "(Zelvora Cell s.r.o., Ostrava) and four fictional repair partners; no real "
                               "organisation, person, product or system is depicted.",
                     "date": "2026-10-12", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-15",
        "generator": "task143/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
