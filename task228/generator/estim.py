"""The analysis, run on the shipped files: labels, every check's record under each route, the pick, the hold line,
and the installs that sent from SDK 9.4.1 still on it each day (the collector client summary)."""
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
    C = load_clients(target)
    A["sdk941"] = still_on(C, links(C))
    return A, D, S


# ------------------------------------------------------------------ the ask on SDK 9.4.1's installs (collector client summary)
CLIENTS = "collector_client_summary_2026-08.parquet"
DAYS941 = ["2026-08-%02d" % d for d in range(6, 20)]
PLATS = ["ios", "android"]


def load_clients(target):
    import pyarrow.parquet as pq
    t = pq.read_table(os.path.join(target, CLIENTS)).to_pandas()
    for c in ("first_batch", "last_batch"):
        t[c] = t[c].dt.tz_convert("Europe/Copenhagen")
    return t


def population(C, start="2026-08-03", end="2026-08-06"):
    """client IDs that sent from SDK 9.4.1 on a day from 3 to 6 August, Copenhagen time"""
    r = C[C["sdk_version"] == "9.4.1"]
    d0, d1 = r["first_batch"].dt.strftime("%Y-%m-%d"), r["last_batch"].dt.strftime("%Y-%m-%d")
    r = r[(d0 <= end) & (d1 >= start)]
    return dict(zip(r["client_id"], r["platform"]))


def links(C, tol=0):
    """a client ID first seen on 9.4.2 whose first sequence number is one above the last of a client ID on an earlier
    SDK that never sent from 9.4.2, on the same platform and after it: one install under a new client ID"""
    has942 = set(C.loc[C["sdk_version"] == "9.4.2", "client_id"])
    older = C[C["sdk_version"] != "9.4.2"]
    seen_older = set(older["client_id"])
    olds = older[~older["client_id"].isin(has942)]
    key = {}
    for cid, plat, ls, lb in zip(olds["client_id"], olds["platform"], olds["last_seq"], olds["last_batch"]):
        key.setdefault((plat, int(ls) + 1), []).append((cid, lb))
    new = C[(C["sdk_version"] == "9.4.2") & ~C["client_id"].isin(seen_older)]
    out = {}
    for cid, plat, fs, fb in zip(new["client_id"], new["platform"], new["first_seq"], new["first_batch"]):
        for k in ([0] if tol == 0 else range(-tol, tol + 1)):
            cand = [c for c, lb in key.get((plat, int(fs) - k), []) if lb < fb]
            if cand:
                out[cand[0]] = cid
                break
    return out


def timing_links(C, hours=48):
    """the over-cleaner: a client ID that stopped on 9.4.1 joined to the next new 9.4.2 client ID on its platform"""
    has942 = set(C.loc[C["sdk_version"] == "9.4.2", "client_id"])
    seen_older = set(C.loc[C["sdk_version"] != "9.4.2", "client_id"])
    stopped = C[(C["sdk_version"] == "9.4.1") & ~C["client_id"].isin(has942)].sort_values(["last_batch", "client_id"])
    new = C[(C["sdk_version"] == "9.4.2") & ~C["client_id"].isin(seen_older)].sort_values(["first_batch", "client_id"])
    out, j = {}, {p: 0 for p in PLATS}
    queue = {p: list(zip(new.loc[new["platform"] == p, "client_id"], new.loc[new["platform"] == p, "first_batch"])) for p in PLATS}
    for cid, plat, lb in zip(stopped["client_id"], stopped["platform"], stopped["last_batch"]):
        q = queue[plat]
        while j[plat] < len(q) and q[j[plat]][1] <= lb:
            j[plat] += 1
        if j[plat] < len(q) and (q[j[plat]][1] - lb).total_seconds() <= hours * 3600:
            out[cid] = q[j[plat]][0]
            j[plat] += 1
    return out


def still_on(C, link, pop=None, silent_days=None):
    """per day from 6 to 19 August and platform: installs of the population whose last batch by the day's end
    (Copenhagen time) came from 9.4.1; an install is its client ID joined to the client ID link gives it"""
    import pandas as pd
    pop = population(C) if pop is None else pop
    first942 = C[C["sdk_version"] == "9.4.2"].groupby("client_id")["first_batch"].min().to_dict()
    lastb = C.groupby("client_id")["last_batch"].max().to_dict()
    cids = sorted(pop)
    plat = np.array([pop[c] for c in cids])
    far = pd.Timestamp("2100-01-01", tz="Europe/Copenhagen")
    sw = np.array([(first942.get(c) or (first942.get(link[c]) if c in link else None) or far).value for c in cids])
    lb = np.array([lastb[c].value for c in cids])
    out = {}
    for d in DAYS941:
        end = pd.Timestamp(d + " 23:59:59", tz="Europe/Copenhagen").value
        keep = sw > end
        if silent_days is not None:
            keep &= lb >= end - silent_days * 86400 * 10 ** 9
        out[d] = {p: int((keep & (plat == p)).sum()) for p in PLATS}
    return out
