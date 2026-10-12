"""Build task134's evidence pack into <out>/ (default: task134/target), then target.zip and metadata.json.

    python3 task134/generator/build.py [--out DIR] [--zip PATH]
"""
import argparse
import datetime as dt
import json
import os
import shutil
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import askcalc as AC
import asktune as AT
import distract as Q
import docs as DOC
import estimators as E
import frames as F
import observe as OB
import readpack as RP
import sim
import tune
import world as W

TASK = os.path.dirname(HERE)
FILES = {
    "placements": "care_home_placements_2021-2026.csv",
    "lines": "fpnc_payment_lines_2021-2026.csv",
    "crosswalk": "client_id_crosswalk_2023.csv",
    "assess": "charging_assessments_2021-2026.csv",
    "deaths": "nrs_death_linkage_2027-01-15.tsv",
    "register": "care_home_register_2026-12.xlsx",
    "lookup": "postcode_locality_lookup.csv",
    "definitions": "care_home_budget_definitions_2027-28.docx",
    "policy": "charging_policy_2026-27.pdf",
    "notes": "extract_notes_2027-01-18.txt",
    "rates": "nchc_rates_2021-22_to_2026-27.xlsx",
    "offer": "nchc_draft_offer_2027-28.pdf",
    "homecare": "care_at_home_hours_2024-2026.csv",
    "grades": "care_inspectorate_grades_2026.csv",
}
DISTRACTORS = ["offer", "homecare", "grades"]
# UK wall-clock times each file was last saved
MTIMES = {
    "placements": (2027, 1, 18, 9, 12), "lines": (2027, 1, 18, 9, 40), "crosswalk": (2027, 1, 18, 9, 15),
    "assess": (2027, 1, 18, 9, 44), "deaths": (2027, 1, 15, 14, 3), "register": (2026, 12, 21, 15, 47),
    "lookup": (2026, 11, 3, 10, 20), "definitions": (2027, 1, 12, 16, 8), "policy": (2026, 4, 2, 15, 5),
    "notes": (2027, 1, 18, 11, 26), "rates": (2026, 5, 11, 14, 26), "offer": (2026, 12, 8, 11, 40),
    "homecare": (2027, 1, 11, 8, 52), "grades": (2026, 12, 14, 16, 31),
}
PL_COLS = F.PL_COLS
LI_COLS = F.LI_COLS
CW_COLS = ["legacy_client_no", "client_id", "debtor_ref", "merged_into"]
DL_COLS = ["client_id", "date_of_death", "date_registered", "match_status"]
FA_COLS = ["assessment_no", "debtor_ref", "completed", "effective_from", "weekly_contribution", "outcome"]
REG_COLS = ["service_no", "service_name", "provider", "postcode", "service_type", "registered_places", "registered",
            "cancelled", "previous_service_no"]
ASK_SEED = 71
ASK_ITERS = 100000


def tables(S, O):
    T = {}
    T["pl"] = F.as_str(F.placements_df(O), PL_COLS)
    T["li"] = F.as_str(F.lines_df(O), LI_COLS)
    T["cw"] = F.as_str(F.crosswalk_df(O), CW_COLS)
    T["dl"] = F.as_str(F.deaths_df(O), DL_COLS)
    a = F.assess_df(O)
    a["debtor_ref"], a["completed"], a["effective_from"], a["weekly_contribution"] = a["_ref"], a["completed_s"], a["effective_s"], a["amount"]
    T["ass"] = F.as_str(a, FA_COLS)
    T["reg"] = F.as_str(F.register_df(S, O), REG_COLS)
    T["lookup"] = F.lookup_df(O)
    return T


def evaluate(S):
    O = OB.observe(S)
    T = tables(S, O)
    I, _, _ = RP.inputs(T["pl"], T["li"], T["cw"], T["dl"])
    res = E.golden(I)
    return res["total"], res


def world():
    """the timeline after the centring moves, the observation, and the ask-side tuning"""
    S = sim.simulate(W.SEED)
    moves = tune.centre(S, evaluate)
    O = OB.observe(S)
    T = tables(S, O)
    rest, detail = AT.run(S, O, AC.table(T), ASK_SEED, iters=ASK_ITERS)
    return S, O, moves, rest, detail


def write_csv(df, path, sep=","):
    df.to_csv(path, index=False, sep=sep, lineterminator="\r\n")


def build(out):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    S, O, moves, rest, detail = world()
    T = tables(S, O)
    p = lambda k: os.path.join(out, FILES[k])
    write_csv(T["pl"], p("placements"))
    write_csv(T["li"], p("lines"))
    write_csv(T["cw"], p("crosswalk"))
    write_csv(T["ass"], p("assess"))
    write_csv(T["dl"], p("deaths"), sep="\t")
    write_csv(T["lookup"], p("lookup"))
    DOC.register_xlsx(T["reg"], p("register"))
    DOC.definitions_docx(p("definitions"))
    DOC.charging_policy_pdf(p("policy"))
    DOC.draft_offer_pdf(p("offer"))
    DOC.rates_xlsx(p("rates"))
    DOC.extract_notes(p("notes"))
    write_csv(Q.homecare(np.random.default_rng(W.SEED + 1313)), p("homecare"))
    write_csv(Q.grades(T["reg"], np.random.default_rng(W.SEED + 1414)), p("grades"))
    for k in FILES:
        ts = W.posix(dt.datetime(*MTIMES[k]))
        os.utime(p(k), (ts, ts))
    with open(os.path.join(HERE, "build_record.json"), "w") as f:
        json.dump(dict(seed=W.SEED, centring_moves=[[m[0], int(m[1])] for m in moves], ask_tune_residual=round(float(rest), 4),
                       ask_tune_detail={k: round(float(v), 4) for k, v in detail.items()}), f, indent=1)
        f.write("\n")
    return S, O


def write_metadata():
    meta = {
        "task": "task134",
        "title": "Strathallan: council-funded care home residents for the 2027-28 budget",
        "domain": "Healthcare Delivery & Health Economics",
        "subdomain": "utilization-access-demand-forecasting",
        "objective": "Forecasting & Predictive Modeling",
        "as_of": "2026-12-31",
        "deliverables": ["care_home_funding_forecast_2027-28.xlsx", "care_home_costs_by_locality.png"],
        "input_files": [{"path": FILES[k], "format": FILES[k].rsplit(".", 1)[1]} for k in sorted(FILES, key=lambda k: FILES[k])],
        "distractors": [FILES[k] for k in DISTRACTORS],
        "distractor_notes": {
            FILES["offer"]: "declared wrong-basis distractor: the draft 2027-28 contract rates, not agreed; a 31 December "
                            "2026 cost is priced at the placement's contracted 2026-27 fee (definitions 3.2), and the note "
                            "itself says the offer is not agreed",
            FILES["homecare"]: "care at home hours by locality: a neighbouring service, not care home residents",
            FILES["grades"]: "inspection grades by home: no figure the forecast or the cost averages use",
        },
        "provenance": "Fully constructed pack: every extract is generated by task134/generator from a simulated "
                      "timeline of care home residents for a fictional Scottish health and social care partnership; "
                      "documents written for the fiction. No real council's, provider's or resident's data.",
        "license": "Constructed data, released with the task (CC BY 4.0).",
        "created": "2026-10-11",
    }
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")


ZIP_TIME = (2027, 1, 18, 12, 0, 0)


def zip_target(src, path):
    """the bundle as shipped: every file flat, in name order, one fixed timestamp, so a rebuild is byte-identical"""
    with zipfile.ZipFile(path, "w") as z:
        for name in sorted(os.listdir(src)):
            zi = zipfile.ZipInfo(name, date_time=ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.create_system = 3
            zi.external_attr = 0o644 << 16
            with open(os.path.join(src, name), "rb") as f:
                z.writestr(zi, f.read())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(TASK, "target"))
    ap.add_argument("--zip", default=None)
    a = ap.parse_args()
    build(a.out)
    if os.path.abspath(a.out) == os.path.join(TASK, "target"):
        write_metadata()
        zip_target(a.out, os.path.join(TASK, "target.zip"))
    elif a.zip:
        zip_target(a.out, a.zip)
    print("built", a.out)
