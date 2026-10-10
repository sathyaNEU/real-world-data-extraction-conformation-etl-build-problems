"""Build task130's evidence pack into <out>/ (default: task130/target)."""
import argparse
import datetime as dt
import json
import os
import shutil
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W
import sim as S
import extracts as X
import docs as D
import distract as Q
import estimators as E
import postprocess as P

TASK = os.path.dirname(HERE)
FILES = {
    "placements": "ta_placements_2018-04_2026-09.csv",
    "cases": "homelessness_cases_2026-09-30.csv",
    "reviews": "bedroom_need_reviews.csv",
    "lets": "moveon_lets_2018-04_2026-09.csv",
    "plan": "moveon_plan_2026-27.xlsx",
    "notice": "corvane_notice_tenter_house.pdf",
    "procedure": "tenter_house_closure_procedure.docx",
    "prices": "dps_lot2_lot3_price_schedule.xlsx",
    "position": "ta_weekly_position_2026-09-28.xlsx",
    "register": "accommodation_register_2026-09.csv",
    "dictionary": "housing_needs_extracts_dictionary.txt",
    "reglets": "housing_register_lets_2025-26.csv",
    "spend": "ta_spend_monitoring_2026-27_q1.xlsx",
}
DISTRACTORS = ["reglets", "spend", "position"]
PENDING = {1: 6, 2: 8, 3: 3, 4: 1}
MTIMES = {
    "placements": (2026, 10, 1, 7, 42), "cases": (2026, 10, 1, 7, 40), "reviews": (2026, 10, 1, 7, 41),
    "lets": (2026, 10, 1, 7, 44), "plan": (2026, 9, 14, 16, 40), "notice": (2026, 9, 15, 11, 31),
    "procedure": (2026, 9, 18, 15, 12), "prices": (2026, 9, 22, 12, 10), "position": (2026, 9, 28, 9, 5),
    "register": (2026, 10, 1, 7, 46), "dictionary": (2026, 10, 1, 9, 10), "reglets": (2026, 4, 8, 10, 2),
    "spend": (2026, 7, 21, 15, 45),
}


def _lists(df, pl):
    """each size's list on the cut (truth side) and whether each member is in Tenter House"""
    A = W.ASOF
    o = df[df["main"] & (df["duty"] <= A) & (df["exit"].isna() | (df["exit"] > A))].copy()
    o["cur"] = S.need_at(o, A)
    th_rows = set(pl[(pl["type"] == "Tenter House") & (pl["start"] <= A) & (pl["end"] > A)]["row"])
    out = {}
    for s in W.SIZES:
        q = o[o["cur"] == s].sort_values(["duty", "case_ref"], kind="mergesort")
        out[s] = (q["duty"].values, np.array([i in th_rows for i in q.index]))
    return out


def _clean(vec, duty, isth):
    """no cumulative cut falls inside a same-day tie that mixes Tenter House and other households"""
    for k in np.cumsum(vec):
        if 0 < k < len(duty) and duty[k - 1] == duty[k]:
            grp = isth[duty == duty[k]]
            if grp.any() and not grp.all():
                return False
    return True


def tune_plans(df, pl):
    """Settle the revised plan's monthly phasing (half-year totals fixed) so no monthly cut splits a
    mixed tie, and give the superseded March plan its own phasing."""
    lists = _lists(df, pl)
    rev, orig = {}, {}
    for s in W.SIZES:
        duty, isth = lists[s]
        base = list(W.PLAN_REVISED[s])
        cands = [base]
        for a in range(6):
            for b in range(6):
                if a != b and base[a] > 0:
                    v = list(base); v[a] -= 1; v[b] += 1
                    cands.append(v)
        for a in range(6):
            for b in range(6):
                for c2 in range(6):
                    for d2 in range(6):
                        if a != b and c2 != d2 and base[a] > 0 and base[c2] > 0:
                            v = list(base); v[a] -= 1; v[b] += 1; v[c2] -= 1; v[d2] += 1
                            if min(v) >= 0:
                                cands.append(v)
        pick = next((v for v in cands if _clean(v, duty, isth)), None)
        if pick is None:
            raise SystemExit("no phasing clears the ties for %d-bed" % s)
        rev[s] = pick
        o = list(W.PLAN_ORIGINAL[s])
        if s in (1, 2):
            tot = sum(pick)
            o = [int(round(tot * w)) for w in (0.22, 0.19, 0.15, 0.15, 0.14, 0.15)]
            o[-1] += tot - sum(o)
        orig[s] = o
    return rev, orig


def simulate():
    rng = np.random.default_rng(W.SEED)
    df = S.cases(rng)
    df, lt = S.allocate(df, rng, W.ASOF)
    pl = S.placements(df, rng)
    return df, lt, pl


def build(out):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    df, lt, pl = simulate()
    rng = np.random.default_rng(W.SEED + 1)
    p = lambda k: os.path.join(out, FILES[k])

    cases = X.cases_frame(df, rng)
    cases.to_csv(p("cases"), index=False)
    rvf = X.reviews_frame(df)
    rvf = rvf[rvf["case_ref"].isin(set(cases["case_ref"]))]
    rvf.to_csv(p("reviews"), index=False)
    pend = X.pending_lets(df, PENDING)
    lets = X.lets_frame(df, lt, pend, rng)
    lets.to_csv(p("lets"), index=False)
    place, units = X.placements_frame(df, pl)
    place.to_csv(p("placements"), index=False)
    X.register_frame(units).to_csv(p("register"), index=False)

    # plan actuals April to September 2026 from the lets log
    started = lets[lets["let_status"] == "Tenancy started"]
    ts = pd.to_datetime(started["tenancy_start"])
    actuals = {s: [int(((started["bedrooms"] == s) & (ts.dt.to_period("M") == pd.Period("2026-%02d" % m))).sum())
                   for m in range(4, 10)] for s in W.SIZES}
    rev, orig = tune_plans(df, pl)
    W.PLAN_REVISED.update(rev)
    W.PLAN_ORIGINAL.update(orig)
    D.plan_xlsx(p("plan"), actuals)
    D.notice_pdf(p("notice"))
    D.procedure_docx(p("procedure"))
    D.prices_xlsx(p("prices"))
    # weekly position from the placements extract on Sunday 27 September
    t = pd.Timestamp("2026-09-27")
    ps = pd.to_datetime(place["placement_start"])
    pe = pd.to_datetime(place["placement_end"].replace("", None))
    live = place[(ps <= t) & (pe.isna() | (pe > t))]
    cs = cases.copy()
    cs["need0"] = pd.to_numeric(cs["bedrooms_needed_at_decision"].replace("", None))
    rvw = pd.read_csv(p("reviews"))
    rvw["review_date"] = pd.to_datetime(rvw["review_date"])
    nd = E.need_at(cs, rvw, t)
    counts = live.assign(n=live["case_ref"].map(nd)).groupby(["accommodation_type", "n"]).size().to_dict()
    th_live = live[live["accommodation_type"] == "Tenter House"]
    th_flats = th_live["unit_ref"].str[3].astype(int).value_counts().to_dict()
    D.weekly_position_xlsx(p("position"), counts, th_flats)
    D.dictionary_txt(p("dictionary"))
    Q.register_lets_csv(p("reglets"), np.random.default_rng(W.SEED + 2))
    Q.spend_xlsx(p("spend"))

    for k, f in FILES.items():
        path = p(k)
        if f.endswith((".xlsx", ".docx")):
            P.normalize_zip(path, MTIMES[k] + (0,))
        if f.endswith(".pdf"):
            P.normalize_pdf(path, stamp=b"D:20260915113100Z'")
        ts_ = dt.datetime(*MTIMES[k]).timestamp()
        os.utime(path, (ts_, ts_))
    return df, lt, pl


def write_metadata():
    meta = {
        "task": "task130",
        "title": "Tenter House: replacement units for 1 April 2027",
        "domain": "Demographic & Social Science",
        "subdomain": "housing",
        "objective": "Forecasting & Predictive Modeling",
        "as_of": "2026-09-30",
        "deliverables": ["tenter_house_replacement_units.xlsx", "tenter_house_runoff.png"],
        "input_files": [{"path": FILES[k], "format": FILES[k].rsplit(".", 1)[1]} for k in sorted(FILES, key=lambda k: FILES[k])],
        "distractors": [FILES[k] for k in DISTRACTORS],
        "provenance": "Fully constructed pack (dataset-generation section 2): every extract is generated by "
                      "task130/generator from a simulated homelessness caseload, move-on lettings and placements "
                      "for a fictional borough; documents written for the fiction. No real person's data.",
        "license": "Constructed data, released with the task (CC BY 4.0).",
        "created": "2026-10-10",
    }
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(TASK, "target"))
    a = ap.parse_args()
    build(a.out)
    if a.out == os.path.join(TASK, "target"):
        write_metadata()
    print("built", a.out)
