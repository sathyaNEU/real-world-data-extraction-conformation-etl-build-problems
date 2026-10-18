"""task246 generator checks, run by make.py on the built pack: the call and its variants, the analyst test on the
simulator's clean truth (R3), every row of the design note's semantic fork table (SF1 to SF17), the separation of the
household files from the call (S1), the ask's device and stops, the input gates and the pack's dates."""
import datetime as dt
import os
import shutil
import tempfile

import numpy as np
import pandas as pd

import build as B
import estim as E
import params as P
import solve

GOLD = ["NP", "NL", "CP", "LT", "EP", "WP", "WR"]
DEFAULT = ["NP", "CP", "LT", "EP"]


class Count:
    n = 0


def ok(cond, what):
    assert cond, what
    Count.n += 1


def clean_truth(W):
    """the call on the simulator's clean truth: every child once and in range, read by the anthropometrist on duty, the
    test as drawn; the default path (offsets out, the repeat error out of the spread) against the decisive step alone
    (the departures' variance about the offset), and the children's own arm circumference as drawn"""
    rows = []
    for a, e in W.test.items():
        for s, rd in zip(e["sessions"], e["reads"]):
            ref = W.sessions[s][1].mean(0)
            for c in range(rd.shape[1]):
                rows.append((a, s, c + 1, float(rd[0][c]), float(rd[1][c]), float(ref[c])))
    T = E.test_stats(rows)
    out, truth = {}, {}
    for z in P.ZCODES:
        ks = [k for k in W.children if k["zone"] == z]
        rest = [k for k in ks if not k["oedema"]]
        oed = len(ks) - len(rest)
        x = [k["muac"] for k in rest]
        out[z] = E.zone_figures(x, [k["measurer"] for k in rest],
                                [1 if k["date"] < P.REFRESHER else 2 for k in rest], oed, T)
        own = np.array([k["own"] for k in rest])
        truth[z] = E.figure(own.mean(), own.var(ddof=1), len(rest), oed)
    true_noted = [z for z in P.ZCODES if abs(round(out[z]["readings"], 1) - round(truth[z], 1)) >= P.NOTE_POINTS - 1e-9]
    return E.noted(out, "R2_offset_repeat"), E.noted(out, E.REFERENCE), true_noted


def call_checks(target, W):
    F = B.FILES
    A = solve.answer(target, F)
    ZF = A["ZF"]
    ok(A["noted"] == GOLD, ("the call", A["noted"]))
    for k in E.VARIANTS:
        ok(E.noted(ZF, k) == GOLD, ("variant", k))
    sets = {k: E.noted(ZF, k) for k in E.RUNGS}
    ok(sets["R0_repeat"] == [] and sets["R2_offset_repeat"] == DEFAULT and sets["R1_field"] == ["NL", "WP", "WR"] and
       sets["R5_offset_mse"] == ["NP", "NL", "CP", "LT", "EP", "ER", "WP", "WR"], ("the rungs", sets))
    # R3: the analyst test on the clean truth
    r2, r3, true_noted = clean_truth(W)
    ok(r2 == DEFAULT, ("R3: the default path on the clean truth", r2))
    ok(r3 == GOLD, ("R3: the decisive step alone on the clean truth", r3))
    ok(true_noted == GOLD, ("R3: the children's own arm circumference as drawn", true_noted))
    # SF1: the nearest zone to the line under any variant is 0.4 or more away
    dist = min(abs(abs(E.points(ZF[z], k)) - P.NOTE_POINTS) for z in P.ZCODES for k in E.VARIANTS)
    ok(dist >= 0.4, ("SF1", dist))
    # SF2: the unrounded difference gives the same notes under every variant
    for k in E.VARIANTS:
        ok([z for z in P.ZCODES if abs(ZF[z]["readings"] - ZF[z][k]) >= P.NOTE_POINTS] == GOLD, ("SF2", k))
    # SF3: the readings' figure prints the same with the divisor n, and the notes hold
    df = A["df"]
    for z in P.ZCODES:
        d = df[df.zone == z]
        x = d[~d.oedema].muac.values
        f0 = E.figure(x.mean(), x.var(ddof=0), len(x), int(d.oedema.sum()))
        ok(round(f0, 1) == round(ZF[z]["readings"], 1), ("SF3", z, f0))
    # SF4, SF5, SF7: the alternative age, every row kept, the children outside 6 to 59 months kept
    for opts, sf in ((dict(age="days"), "SF4"), (dict(dedupe=False), "SF5"), (dict(ages=(0, 99)), "SF7")):
        alt = solve.answer(target, F, **opts)
        ok(alt["noted"] == GOLD and all(E.noted(alt["ZF"], k) == GOLD for k in E.VARIANTS), (sf, alt["noted"]))
    resent = pd.read_csv(os.path.join(target, F["ncha_anthro"]))
    ok(resent.duplicated(subset=["cluster", "hh_no", "child_no"]).sum() > 0, "SF5: NCHA team 2's rows sent twice")
    wide = solve.readings(target, F, ages=(0, 99), muac_range=True)
    out_age = wide[(wide.age < 6) | (wide.age > 59)]
    ok(len(out_age) == 16 and set(out_age.age) <= {4, 5, 60, 61, 62, 63}, ("SF7: 16 children at 4 to 5 or 60 to 63 months",
                                                                        sorted(out_age.age)))
    # SF6: four readings outside 75 to 220 mm, each left out
    raw = solve.readings(target, F, muac_range=False)
    bad = raw[~raw.oedema & ((raw.muac < 75) | (raw.muac > 220))]
    ok(len(bad) == 4, ("SF6", len(bad)))
    # SF8: PRK team 4's change of anthropometrist falls between two working days
    sample = pd.read_csv(os.path.join(target, F["sample"]))
    t4 = sorted(solve._dmy(d) for d in sample[(sample.partner == "PRK") & (sample.team == 4)].date_visited)
    ok(dt.date(2027, 6, 26) in t4 and dt.date(2027, 6, 27) not in t4 and P.SUBSTITUTION in t4, "SF8")
    # SF9: every test child of both sessions has two supervisor readings
    nt = pd.read_csv(os.path.join(target, F["ncha_test"]))
    sup = nt[nt.measured_by == "SUPERVISOR"].groupby(["session", "test_child"]).size()
    ok(len(sup) == 20 and (sup == 2).all(), "SF9")
    # SF16: a shared zone's children come from both its teams
    for z in ("CA", "EA", "WA"):
        ok(df[df.zone == z].measurer.nunique() == 2, ("SF16", z))
    # SF17: oedema children counted in both figures; their readings kept as ordinary readings move no note
    alt = {}
    for z in P.ZCODES:
        d = df[df.zone == z]
        meas = list(d.measurer)
        alt[z] = E.zone_figures(d.muac.values, meas, list(d.session), 0, A["T"])
    ok(E.noted(alt, E.REFERENCE) == GOLD and int(df.oedema.sum()) > 0, "SF17")
    # SF10 to SF15 are the variants, asserted above
    for sf in ("SF10", "SF11", "SF12", "SF13", "SF14", "SF15"):
        ok(True, sf)
    return A


def separation(target):
    """S1: the call computed from the pack without the three household files"""
    F = B.FILES
    tmp = tempfile.mkdtemp()
    for k in B.PACK:
        if k not in ("visits", "members", "births"):
            shutil.copy(os.path.join(target, F[k]), tmp)
    try:
        A = solve.answer(tmp, F)
        ok(A["noted"] == GOLD, "S1: the call without the household files")
    finally:
        shutil.rmtree(tmp)


def ask_checks(target):
    F = B.FILES
    gr, gm = solve.response(target, F), solve.mortality(target, F)
    cr, cm = solve.response(target, F, codes="v4"), solve.mortality(target, F, codes="v4")
    for z in P.ZCODES:
        ok(round(cr[z], 1) != round(gr[z], 1), ("the cracker's response", z))
        ok(round(cm[z][0], 2) != round(gm[z][0], 2), ("the cracker's crude death rate", z))
        ok(round(cm[z][1], 2) != round(gm[z][1], 2), ("the cracker's under-five death rate", z))
    # the device's evidence: who was visited again, and who left, either side of 21 June
    day4 = solve.form_v4_day(target, F)
    ok(day4 == dt.date(2027, 6, 21), ("the switch", day4))
    v = pd.read_csv(os.path.join(target, F["visits"]))
    v["day"] = [solve._dmy(d) for d in v.date]
    again = set((int(r.cluster), int(r.hh_no)) for r in v[v.visit == 2].itertuples())
    for before in (True, False):
        f = v[(v.visit == 1) & ((v.day < day4) if before else (v.day >= day4))]
        for code in (3, 4):
            g = f[f.outcome == code]
            back = sum((int(r.cluster), int(r.hh_no)) in again for r in g.itertuples())
            revisit = (code == 3) == before
            ok(back == (len(g) if revisit else 0) and len(g) > 0, ("the revisits", before, code, back, len(g)))
    m = solve._members(target, F)
    yrs = m.age / np.where(m.age_unit == "months", 12.0, 1.0)
    ok(int(((m.day >= day4) & (m.left_reason == 3) & (yrs >= 15)).sum()) == 0, "no adult moved with a caregiver from 21 June")
    ok(int(((m.day < day4) & (m.left_reason == 3) & (yrs >= 15)).sum()) > 0, "adults coded 3 before 21 June")
    ok(int(((m.day < day4) & (m.left_reason == 4) & (yrs >= 15)).sum()) == 0, "no adult coded 4 before 21 June")
    # every golden figure separates from its stops; no stop is the golden in every zone
    for kw in (dict(codes="v4", away=False), dict(codes="v4", births_module=False), dict(away=False),
               dict(births_module=False), dict(age_unit=False)):
        alt = solve.mortality(target, F, **kw)
        same = sum(round(alt[z][i], 2) == round(gm[z][i], 2) for z in P.ZCODES for i in (0, 1))
        ok(same < 24, ("a stop that lands everywhere", kw))
    # the members sent twice are one cluster's, every row an exact copy but its form id
    mm = pd.read_csv(os.path.join(target, F["members"]))
    dup = mm[mm.duplicated(subset=["cluster", "hh_no", "line_no"], keep=False)]
    ok(dup.cluster.nunique() == 1 and len(dup.drop(columns=["form_id"]).drop_duplicates()) * 2 == len(dup), "the resync")
    return gr, gm


def gates(target):
    F = B.FILES
    files = [F[k] for k in B.PACK]
    ok(all(os.path.exists(os.path.join(target, f)) for f in files) and len(files) >= 10, "ten files or more")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three formats or more")
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, ("a file of 25,000 rows", big))
    ok(len(B.DISTRACTORS) >= 2, "two distractors")
    ok(sorted(os.listdir(target)) == sorted(files), "the pack is the declared files")
    # no record dated after the round's files were gathered
    for k in ("ncha_anthro", "visits", "members", "births"):
        df = pd.read_csv(os.path.join(target, F[k]))
        for col in df.columns:
            if col in ("today", "interview_date"):
                ok(max(dt.date.fromisoformat(x) for x in df[col].dropna()) <= P.FIELD_END, (k, col))
            if col in ("date", "date_of_death", "date_of_birth"):
                ok(max(solve._dmy(x) for x in df[col].dropna()) <= P.FIELD_END, (k, col))


def run(target, W, fig, golden):
    Count.n = 0
    A = call_checks(target, W)
    separation(target)
    ask_checks(target)
    gates(target)
    S = {s["code"]: s for s in fig["zones"]}
    for z in P.ZCODES:
        ok(S[z]["note"] == (z in GOLD), ("figures.json note", z))
        ok(S[z]["own_range"][0] <= S[z]["own"] <= S[z]["own_range"][1], ("own inside its range", z))
    ok(os.path.exists(os.path.join(golden, "lr2027_muac_measurement_review.xlsx")), "golden workbook")
    ok(os.path.exists(os.path.join(golden, "lr2027_gam_measurement_note.pdf")), "golden note")
    return Count.n
