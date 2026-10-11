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
    "members": "household_members_2026-09-30.csv",
    "lets": "moveon_lets_2018-04_2026-09.csv",
    "plan": "moveon_plan_2026-27.xlsx",
    "notice": "corvane_notice_tenter_house.pdf",
    "scheme": "housing_allocations_scheme_2024_parts_3_and_6.pdf",
    "procedure": "tenter_house_closure_procedure.docx",
    "prices": "dps_lot2_lot3_price_schedule.xlsx",
    "position": "ta_weekly_position_2026-09-28.xlsx",
    "register": "accommodation_register_2026-09.csv",
    "dictionary": "housing_needs_extracts_dictionary.txt",
    "reglets": "housing_register_lets_2025-26.csv",
    "spend": "ta_spend_monitoring_2026-27_q1.xlsx",
}
DISTRACTORS = ["reglets", "spend", "position"]
MTIMES = {
    "placements": (2026, 10, 1, 7, 42), "cases": (2026, 10, 1, 7, 40), "reviews": (2026, 10, 1, 7, 41),
    "members": (2026, 10, 1, 7, 43),
    "lets": (2026, 10, 1, 7, 44), "plan": (2026, 10, 1, 9, 25), "notice": (2026, 9, 15, 11, 31), "scheme": (2024, 3, 28, 10, 5),
    "procedure": (2026, 9, 18, 15, 12), "prices": (2026, 9, 22, 12, 10), "position": (2026, 9, 28, 9, 5),
    "register": (2026, 10, 1, 7, 46), "dictionary": (2026, 10, 1, 9, 10), "reglets": (2026, 4, 8, 10, 2),
    "spend": (2026, 7, 21, 15, 45),
}


OCT = pd.Timestamp("2026-10-01")
FWD = pd.date_range("2026-11-01", "2027-03-01", freq="MS")


def _truth_lists(df, lt, pl):
    """the November to March lists on the truth side: every open main-duty case on the cut except the
    households with October lets, in duty-date order, with the Part 3 need on each round day from the
    people on the application on the cut"""
    A = W.ASOF
    o = df[df["main"] & (df["duty"] <= A) & (df["exit"].isna() | (df["exit"] > A))]
    o = o.sort_values(["duty", "case_ref"], kind="mergesort")
    octl = set(lt.loc[lt["tenancy_start"] >= OCT, "row"])
    o = o[~o.index.isin(octl)]
    th_rows = set(pl[(pl["type"] == "Tenter House") & (pl["start"] <= A) & (pl["end"] > A)]["row"])
    mem = [[m for m in df.at[i, "members"] if m[2] <= A] for i in o.index]
    needs = [np.array([S.rooms(m, S.round_date(mo)) for m in mem]) for mo in FWD]
    return o["duty"].values, np.array([i in th_rows for i in o.index]), needs


def _clean(plan, duty, isth, needs):
    """no round's cut falls inside a same-day tie that mixes Tenter House and other households"""
    gone = np.zeros(len(duty), bool)
    for k in range(5):
        for s in W.SIZES:
            idx = np.flatnonzero((needs[k] == s) & ~gone)
            n = plan[s][k + 1]
            if 0 < n < len(idx) and duty[idx[n - 1]] == duty[idx[n]]:
                tie = idx[duty[idx] == duty[idx[n]]]
                if isth[tie].any() and not isth[tie].all():
                    return False
            gone[idx[:n]] = True
    return True


def tune_plans(df, lt, pl, october):
    """Settle the revised plan's November to March phasing (half-year totals fixed) so no round's cut
    splits a mixed tie, and give the superseded March plan its own phasing. October is the September
    round, already made."""
    duty, isth, needs = _truth_lists(df, lt, pl)
    base = {s: [october[s]] + list(W.PLAN_REVISED[s][1:]) for s in W.SIZES}
    if _clean(base, duty, isth, needs):
        rev = base
    else:
        rev = None
        moves = [(s, a_, b_) for s in W.SIZES for a_ in range(1, 6) for b_ in range(1, 6) if a_ != b_]
        for s, a_, b_ in moves:
            if base[s][a_] == 0:
                continue
            v = {k: list(x) for k, x in base.items()}
            v[s][a_] -= 1
            v[s][b_] += 1
            if _clean(v, duty, isth, needs):
                rev = v
                break
        if rev is None:
            for (s1, a1, b1) in moves:
                for (s2, a2, b2) in moves:
                    v = {k: list(x) for k, x in base.items()}
                    if v[s1][a1] == 0:
                        continue
                    v[s1][a1] -= 1
                    v[s1][b1] += 1
                    if v[s2][a2] == 0:
                        continue
                    v[s2][a2] -= 1
                    v[s2][b2] += 1
                    if _clean(v, duty, isth, needs):
                        rev = v
                        break
                if rev is not None:
                    break
        if rev is None:
            raise SystemExit("no phasing clears the ties")
    orig = {}
    for s in W.SIZES:
        o = list(W.PLAN_ORIGINAL[s])
        if s in (1, 2):
            tot = sum(rev[s])
            o = [int(round(tot * w)) for w in (0.22, 0.19, 0.15, 0.15, 0.14, 0.15)]
            o[-1] += tot - sum(o)
        orig[s] = o
    rev[5] = [october.get(5, 0), 0, 0, 0, 0, 0]
    orig[5] = [0] * 6
    return rev, orig


def simulate():
    rng = np.random.default_rng(W.SEED)
    df = S.cases(rng)
    df, lt = S.allocate(df, rng, OCT)
    pl = S.placements(df, rng)
    df = S.record_assessments(df, pl, lt)
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
    X.members_frame(df).to_csv(p("members"), index=False)
    lets = X.lets_frame(df, lt, rng)
    lets.to_csv(p("lets"), index=False)
    place, units = X.placements_frame(df, pl)
    place.to_csv(p("placements"), index=False)
    reg = X.register_frame(units)
    reg.to_csv(p("register"), index=False)

    # plan actuals April to September 2026 and the September round's October lets, from the lets log
    started = lets[lets["let_status"] == "Tenancy started"]
    ts = pd.to_datetime(started["tenancy_start"])
    b5 = started["bedrooms"].clip(upper=5)
    actuals = {s: [int(((b5 == s) & (ts.dt.to_period("M") == pd.Period("2026-%02d" % m))).sum())
                   for m in range(4, 10)] for s in D.ROWS}
    acc = lets[lets["let_status"] != "Tenancy started"]
    october = {s: int((acc["bedrooms"].clip(upper=5) == s).sum()) for s in D.ROWS}
    rev, orig = tune_plans(df, lt, pl, october)
    W.PLAN_REVISED.clear()
    W.PLAN_REVISED.update(rev)
    W.PLAN_ORIGINAL.clear()
    W.PLAN_ORIGINAL.update(orig)
    D.plan_xlsx(p("plan"), actuals)
    D.notice_pdf(p("notice"))
    D.scheme_pdf(p("scheme"))
    D.procedure_docx(p("procedure"))
    D.prices_xlsx(p("prices"))
    # weekly position from the placements extract on Sunday 27 September, by the unit each household occupies
    t = pd.Timestamp("2026-09-27")
    ps = pd.to_datetime(place["placement_start"])
    pe = pd.to_datetime(place["placement_end"].replace("", None))
    live = place[(ps <= t) & (pe.isna() | (pe > t))]
    beds = dict(zip(reg["unit_ref"], reg["bedrooms"]))
    size = [0 if typ in ("Bed and breakfast", "Hostel") else int(beds[u])
            for typ, u in zip(live["accommodation_type"], live["unit_ref"])]
    counts = live.assign(n=size).groupby(["accommodation_type", "n"]).size().to_dict()
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
            P.normalize_pdf(path, stamp=b"D:20240328100500Z'" if k == "scheme" else b"D:20260915113100Z'")
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
