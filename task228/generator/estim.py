"""The analysis, run on the shipped files: labels, every check's record under each route, the pick, the hold line,
the weekly review by type and the app-wide incidents."""
import json
import os
import re
from math import floor, sqrt

import numpy as np
import pandas as pd

import params as P

CHECKS = ["gap", "dup", "late", "epu", "share"]
NAMES = {"gap": "Gap sessions", "dup": "Duplicate sessions", "late": "Late sessions", "epu": "Events per install",
         "share": "Treatment share"}
COL = {"gap": "gaps", "dup": "dups", "late": "lates"}
TYPES = ["telemetry loss", "duplicate delivery", "late delivery", "consent loss"]


def norm(s):
    return re.sub(r"\s+", " ", str(s)).strip().lower()


def load(target):
    p = lambda f: os.path.join(target, f)
    reg = json.load(open(p("experiment_registry_2026.json")))["experiments"]
    q1 = pd.read_csv(p("install_summary_2026q1.csv"), dtype={"install": str})
    q1 = q1.rename(columns={"exp_id": "key", "install": "id", "variant": "arm", "os": "platform", "n_sessions": "sess",
                            "sessions_seq_gap": "gaps", "sessions_dup_ids": "dups", "sessions_late": "lates", "events": "ev"})
    q1["arm"] = q1["arm"].map({"A": "control", "B": "treatment"})
    q1["platform"] = q1["platform"].str.lower()
    qs = [q1]
    for f in ("install_summary_2026q2.parquet", "install_summary_2026q3.parquet"):
        t = pd.read_parquet(p(f)).rename(columns={"experiment_key": "key", "install_id": "id", "sessions": "sess",
                                                  "gap_sessions": "gaps", "duplicate_sessions": "dups",
                                                  "late_sessions": "lates", "events_received": "ev"})
        qs.append(t)
    ins = pd.concat(qs, ignore_index=True)
    rgx = pd.read_excel(p("data_incident_register_2026.xlsx"), dtype={"incident_id": str})
    rev = pd.read_csv(p("weekly_review_log_2026.csv"))
    return dict(reg=reg, ins=ins, rgx=rgx, rev=rev)


def labels(D):
    by_title = {norm(e["title"]): e["key"] for e in D["reg"]}
    r = D["rgx"]
    ex = r[(r["scope"] == "experiment") & (r["status"] == "confirmed")]
    return sorted({by_title[norm(t)] for t in ex["experiment"]})


# ------------------------------------------------------------------ per-arm sufficient statistics
def arm_stats(ins):
    g = ins.copy()
    for m, c in COL.items():
        g[c + "_q"] = g[c] / g["sess"]
    agg = {"sess": ["count", "sum"], "ev": ["sum"]}
    g["sess2"] = g["sess"].astype(float) ** 2
    g["ev2"] = g["ev"].astype(float) ** 2
    cols = {"n": ("sess", "count"), "sy": ("sess", "sum"), "syy": ("sess2", "sum"), "se": ("ev", "sum"), "see": ("ev2", "sum")}
    for m, c in COL.items():
        g[c + "2"] = g[c].astype(float) ** 2
        g[c + "y"] = g[c].astype(float) * g["sess"]
        g[c + "_q2"] = g[c + "_q"] ** 2
        cols.update({m + "_sx": (c, "sum"), m + "_sxx": (c + "2", "sum"), m + "_sxy": (c + "y", "sum"),
                     m + "_sq": (c + "_q", "sum"), m + "_sqq": (c + "_q2", "sum")})
    s = g.groupby(["key", "arm"]).agg(**cols)
    return s


def _ratio(row, m):
    n = row["n"]
    mx, my = row[m + "_sx"] / n, row["sy"] / n
    vx = (row[m + "_sxx"] - n * mx * mx) / (n - 1)
    vy = (row["syy"] - n * my * my) / (n - 1)
    cxy = (row[m + "_sxy"] - n * mx * my) / (n - 1)
    r = mx / my
    return r, (vx - 2 * r * cxy + r * r * vy) / (my * my * n)


def z_scores(S, design):
    """hold-direction z for every experiment and check, under the field's test and the reflex routes"""
    out = {}
    for key in sorted({k for k, _ in S.index}):
        c, t = S.loc[(key, "control")], S.loc[(key, "treatment")]
        z = {}
        for m in COL:
            rc, vc = _ratio(c, m)
            rt, vt = _ratio(t, m)
            pc, pt = c[m + "_sx"] / c["sy"], t[m + "_sx"] / t["sy"]
            pp = (c[m + "_sx"] + t[m + "_sx"]) / (c["sy"] + t["sy"])
            qc, qt = c[m + "_sq"] / c["n"], t[m + "_sq"] / t["n"]
            vqc = (c[m + "_sqq"] - c["n"] * qc * qc) / (c["n"] - 1)
            vqt = (t[m + "_sqq"] - t["n"] * qt * qt) / (t["n"] - 1)
            z[m] = dict(delta=(rt - rc) / sqrt(vc + vt),
                        naive=(pt - pc) / sqrt(pp * (1 - pp) * (1 / c["sy"] + 1 / t["sy"])),
                        mor=(qt - qc) / sqrt(vqc / c["n"] + vqt / t["n"]),
                        rel=(pt / pc - 1.0))
        ec, et = c["se"] / c["n"], t["se"] / t["n"]
        vec = (c["see"] - c["n"] * ec * ec) / (c["n"] - 1)
        vet = (t["see"] - t["n"] * et * et) / (t["n"] - 1)
        zw = (ec - et) / sqrt(vec / c["n"] + vet / t["n"])
        z["epu"] = dict(delta=zw, naive=zw, mor=zw, poisson=(ec - et) / sqrt(ec / c["n"] + et / t["n"]), rel=et / ec - 1.0)
        n = c["n"] + t["n"]
        p = design[key]
        zs = (n * p - t["n"]) / sqrt(n * p * (1 - p))
        z["share"] = dict(delta=zs, naive=zs, mor=zs, rel=(t["n"] / n) / p - 1.0)
        out[key] = z
    return out


def record(Z, inc, how):
    rec = {}
    for m in CHECKS:
        h = [k for k in Z if Z[k][m][how] > P.Z]
        rec[m] = dict(incidents=sum(1 for k in h if k in inc), none=sum(1 for k in h if k not in inc))
    return rec


def pick(rec, n_none):
    cap = floor(P.ALLOW * n_none + 1e-9)
    ok = [m for m in CHECKS if rec[m]["none"] <= cap]
    ok.sort(key=lambda m: (-rec[m]["incidents"], rec[m]["none"]))
    return ok[0], ok, cap


def moved_most(Z, inc):
    return max(CHECKS, key=lambda m: np.mean([abs(Z[k][m]["rel"]) for k in inc]))


def hold_line(ins, none_keys, m="gap", arms=("control", "treatment"), pooled=True):
    """the smallest difference a standard experiment holds at, in percentage points, from per-install variability"""
    d = ins[ins["key"].isin(none_keys) & ins["arm"].isin(arms)]
    c = COL[m]
    if pooled:
        x, y = d[c].astype(float).values, d["sess"].astype(float).values
        r = x.sum() / y.sum()
        s2 = ((x - r * y) ** 2).sum() / (len(x) - 1) / (y.mean() ** 2)
    else:
        parts = []
        for k, g in d.groupby(["key", "arm"]):
            x, y = g[c].astype(float).values, g["sess"].astype(float).values
            r = x.sum() / y.sum()
            parts.append(((x - r * y) ** 2).sum() / (len(x) - 1) / (y.mean() ** 2))
        s2 = float(np.mean(parts))
    return 100 * P.Z * sqrt(2 * s2 / P.STD_N)


def naive_line(ins, none_keys, m):
    d = ins[ins["key"].isin(none_keys)]
    c = COL[m]
    pr = d[c].sum() / d["sess"].sum()
    s_bar = d["sess"].mean()
    return 100 * P.Z * sqrt(2 * pr * (1 - pr) / (P.STD_N * s_bar))


def mor_line(ins, none_keys, m):
    d = ins[ins["key"].isin(none_keys)]
    q = d[COL[m]] / d["sess"]
    return 100 * P.Z * sqrt(2 * q.var(ddof=1) / P.STD_N)


def analyse(target, causes):
    """causes: experiment key -> the cause the reconciliation established (from the summary)"""
    D = load(target)
    inc = set(labels(D))
    keys = [e["key"] for e in D["reg"]]
    none_keys = [k for k in keys if k not in inc]
    design = {e["key"]: float(e["design"]["treatment"]) for e in D["reg"]}
    S = arm_stats(D["ins"])
    Z = z_scores(S, design)
    recs = {h: record(Z, inc, h) for h in ("delta", "naive", "mor")}
    picks = {h: pick(recs[h], len(none_keys)) for h in recs}
    line = hold_line(D["ins"], none_keys)
    A = dict(inc=sorted(inc), none=none_keys, Z=Z, recs=recs, picks=picks, line=line,
             line_naive_late=naive_line(D["ins"], none_keys, "late"), line_naive_gap=naive_line(D["ins"], none_keys, "gap"),
             line_mor_late=mor_line(D["ins"], none_keys, "late"), moved_most=moved_most(Z, inc))
    A["review"] = review_by_type(D, inc, causes)
    A["review_first_call"] = review_by_type(D, inc, first_calls(D))
    A["app_wide"] = app_wide(D)
    A["app_wide_summed"] = app_wide(D, summed=True)
    return A, D, S


def first_calls(D):
    by_title = {norm(e["title"]): e["key"] for e in D["reg"]}
    r = D["rgx"]
    ex = r[(r["scope"] == "experiment") & (r["status"] == "confirmed")]
    return {by_title[norm(t)]: ty for t, ty in zip(ex["experiment"], ex["incident_type"])}


def review_by_type(D, inc, types):
    rv = D["rev"]
    flagged = set(rv.loc[rv["action"] == "flag", "experiment_key"])
    out = {t: [0, 0] for t in TYPES}
    for k in inc:
        out[types[k]][0 if k in flagged else 1] += 1
    return out


def app_wide(D, summed=False):
    r = D["rgx"]
    a = r[r["scope"] == "app-wide"]
    out = []
    for iid, g in a.groupby("incident_id", sort=True):
        sess = int(g["sessions_in_window"].sum())
        gap = int(g["gap_sessions"].sum()) if summed else int(g["gap_sessions"].iloc[0])
        out.append(dict(incident=iid, opened=str(g["opened"].iloc[0]), platforms=list(g["platform"]), gap=gap,
                        sessions=sess, share=100.0 * gap / sess))
    return out
