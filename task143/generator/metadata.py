"""Write task143/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402

TASK = os.path.dirname(HERE)
# per file: what it is, the system or office that produced it, and the day it was issued or pulled (the provenance;
# nothing under target/ describes the pack)
LAB_PULL, SERVICE_PULL, MONEY_PULL = "2026-10-12", "2026-10-05", "2026-10-09"
SOURCES = {
    K.F_POLICY: ("Product Finance policy FIN-RS-04, battery warranty reserve at lot release, revision 3",
                 "Product Finance, Notebook Division", "2025-03-18"),
    K.F_MEMO: ("Battery Reliability Lab memo QM-07, release model RL-3 for Zelvora ZP-4820 cells, revision 4",
               "Battery Reliability Lab", "2026-09-30"),
    K.F_SPEC: ("Model K battery pack specification, revision D", "Product Engineering, Battery Plant", "2025-03-14"),
    K.F_CYC_A: ("Cycler export of the first QP-3 cycles of the release-test cells run on fleet A, lots ZC2437 to ZC2638",
                "Battery Reliability Lab, fleet A cycler software", LAB_PULL),
    K.F_CYC_B: ("Cycler export of the first QP-3 cycles of the release-test cells run on fleet B, lots ZC2506 to ZC2638",
                "Battery Reliability Lab, fleet B cycler software (weekly pulls)", LAB_PULL),
    K.F_REG: ("Release test register, lots ZC2437 to ZC2638", "Battery Reliability Lab", LAB_PULL),
    K.F_LIFE: ("Life monitoring results of the release-test cells, lots ZC2437 to ZC2614",
               "Battery Reliability Lab, life monitoring", LAB_PULL),
    K.F_CELLS: ("Zelvora cell data package for lot ZC2638", "Zelvora Cell s.r.o.", LAB_PULL),
    K.F_GEN: ("Genealogy of the Model K packs built from lot ZC2638", "Battery Plant, line MES", LAB_PULL),
    K.F_MODEL_J: ("Genealogy of the Model J packs built from lot ZC2638", "Battery Plant, line MES", LAB_PULL),
    K.F_COA: ("Zelvora certificate of analysis for lot ZC2638", "Zelvora Cell s.r.o., Quality", "2026-09-22"),
    K.F_CASES: ("Service case system extract, K14 and K15 battery cases, September 2024 to September 2026",
                "Service case system", SERVICE_PULL),
    K.F_SAP: ("DACH depot service orders on K14 and K15 batteries, September 2024 to 1 March 2026",
              "DACH service depot, SAP", SERVICE_PULL),
    K.F_RETURNS: ("Goods-receipt log of the batteries received at the Bielefeld returns depot",
                  "Returns depot, Bielefeld", MONEY_PULL),
    K.F_CARRIER: ("Carrier statement of inbound consignments of returned batteries, September 2025 to October 2026",
                  "Carrier statement to Service Operations", MONEY_PULL),
    K.F_INV["FRB"]: ("Dauvergne Réparation invoices to Service Operations, September 2025 to September 2026",
                     "Dauvergne Réparation SAS", MONEY_PULL),
    K.F_INV["UKI"]: ("Tolley Marsh Repair invoices to Service Operations, September 2025 to September 2026",
                     "Tolley Marsh Repair Ltd", MONEY_PULL),
    K.F_INV["NOR"]: ("Ljungqvist Service invoices to Service Operations, September 2025 to September 2026",
                     "Ljungqvist Service AB", MONEY_PULL),
    K.F_INV["SOU"]: ("Ferrucci Assistenza invoices to Service Operations, September 2025 to September 2026",
                     "Ferrucci Assistenza S.r.l.", MONEY_PULL),
    K.F_FX: ("Treasury month-end exchange rates, January 2025 to September 2026", "Treasury", MONEY_PULL),
    K.F_COST: ("Service cost sheet FY2026", "Service Operations controlling", MONEY_PULL),
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
        what, who, when = SOURCES[f]
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: %s (%s)" % (what, who), "date": when,
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task143",
        "title": "How many of Zelvora cell lot ZC2638's 7,200 Model K packs Kalvenhorst Systeme reserves for at "
                 "release: the packs expected to fall below 80 per cent of rated capacity within the 600-cycle "
                 "warranty",
        "domain": "General Statistics & Data Science",
        "client_domain": "General Statistics & Data Science",
        "subdomain": "bayesian-modeling-posterior-inference (the expected number of a supplier cell lot's battery packs "
                     "that fall below the warranty's capacity line)",
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
