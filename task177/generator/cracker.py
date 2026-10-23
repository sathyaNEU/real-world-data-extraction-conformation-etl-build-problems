"""task177 cracker and mirror sheets, run on the cut pack: each ask figure on the routes a careful solver takes after
landing the call (the cracker) and after stopping on the default path (the mirror), scored against figures.json at half
the stated rounding, and the pair ceiling on Part 0's weights (38 call, 7 instruction following, 55 asks, a wrong call
keeping about 5).

The asks consume nothing the call's construction produces (separation is asserted in checks.py), so both responses
take the same ask routes; each route is scored separately below, and the worst honest one is the gated figure.

    python3 task177/generator/cracker.py task177/target"""
from __future__ import annotations

import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402

TOL = 500.0


def _sched(target):
    S = pd.read_csv(os.path.join(target, C.F_SCHED), dtype={"member_id": str, "employer_nit": str})
    S["contribution"] = S["contribution"].astype(float)
    A = pd.read_excel(os.path.join(target, C.F_AGREE), dtype=str)
    sec = dict(zip(A["employer_nit"], A["sector"]))
    tot = S.groupby(["schedule_no", "employer_nit", "period", "filed_on"])["contribution"].sum().reset_index()
    tot["sector"] = tot["employer_nit"].map(sec)
    return tot, sec


def _received_by_nit(target):
    """the statement's employer transfers by payer and reference month, a returned transfer netted"""
    T = pd.read_csv(os.path.join(target, C.F_STMT), dtype={"payer_id": str})
    cr = T[T["description"] == "TRANSFERENCIA RECIBIDA"].copy()
    cr["amt"] = cr["credit"].astype(float)
    db = T[T["description"] == "DEVOLUCION TRANSFERENCIA"].copy()
    db["amt"] = -db["debit"].astype(float)
    X = pd.concat([cr, db])
    X["per"] = X["reference"].str.extract(r"(\d\d)/(\d{4})").apply(lambda r: "%s-%s" % (r[1], r[0]), axis=1)
    return X.groupby(["payer_id", "per"])["amt"].sum().to_dict()


def ask_a_routes(target):
    tot, sec = _sched(target)
    t26 = tot[tot["period"].str.startswith("2026")]
    rec = _received_by_nit(target)
    out = {}
    # version reflex: the latest filed schedule per employer and month
    latest = t26.sort_values(["filed_on", "schedule_no"]).groupby(["employer_nit", "period"]).tail(1)
    # sum reflex: every schedule
    for name, base in (("latest_schedule", latest), ("all_schedules", t26)):
        per = base.groupby(["employer_nit", "period"])["contribution"].sum().reset_index()
        per["got"] = [rec.get((n, p), 0.0) for n, p in zip(per["employer_nit"], per["period"])]
        per["short"] = (per["contribution"] - per["got"]).clip(lower=0)
        per["sector"] = per["employer_nit"].map(sec)
        out[name] = dict(deducted=per.groupby("sector")["contribution"].sum().to_dict(),
                         outstanding=per.groupby("sector")["short"].sum().to_dict())
    return out


def ask_b_routes(target):
    Rc = pd.read_csv(os.path.join(target, C.F_RECEIPTS), dtype={"originating_account": str, "loan_reference": str})
    D = pd.read_csv(os.path.join(target, C.F_DEFAULTS), dtype={"loan_reference": str})
    L = pd.read_csv(os.path.join(target, C.F_LOANS), dtype={"loan_no": str}, usecols=["loan_no", "unit_type"])
    typ = dict(zip(L["loan_no"], L["unit_type"]))
    Rc["amount"] = Rc["amount"].astype(float)
    D["year"] = D["default_date"].str[:4].astype(int)
    out = {}
    for name, keep in (("all_receipts", lambda r: r), ("no_0731_transfers",
                                                       lambda r: r[~r["originating_account"].fillna("").str.startswith("0731-")])):
        g = keep(Rc)
        res = {}
        for y in (2023, 2024):
            loans = set(D[D["year"] == y]["loan_reference"])
            h = g[g["loan_reference"].isin(loans)]
            res[str(y)] = h.groupby(h["loan_reference"].map(typ))["amount"].sum().to_dict()
        out[name] = res
    return out


def score(fig, target):
    A = ask_a_routes(target)
    B = ask_b_routes(target)
    rows = []
    for route, v in A.items():
        hits = 0
        n = 0
        for key in ("deducted", "outstanding"):
            for s in C.SECTORS:
                n += 1
                hits += abs(v[key].get(s, 0.0) - fig["ask_a_%s" % key][s]) <= TOL
        rows.append(("A", route, hits, n))
    for route, v in B.items():
        hits = 0
        n = 0
        for y in ("2023", "2024"):
            for t in C.AGENCY_TYPES:
                n += 1
                hits += abs(v[y].get(t, 0.0) - fig["ask_b_recovered"][y][t]) <= TOL
        rows.append(("B", route, hits, n))
    return rows


def pair(rows):
    nA = max(r[3] for r in rows if r[0] == "A")
    nB = max(r[3] for r in rows if r[0] == "B")
    keepA = max(r[2] for r in rows if r[0] == "A")
    keepB = max(r[2] for r in rows if r[0] == "B")
    L = (keepA + keepB) / float(nA + nB)
    cracker = 38 + 7 + 55 * L
    mirror = 5 + 7 + 55 * L
    return (cracker + mirror) / 2, 100 * L, cracker, mirror


def main(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    rows = score(fig, target)
    for a, route, hits, n in rows:
        print("ask %s  %-20s keeps %d of %d" % (a, route, hits, n))
    pc, ml, cr, mi = pair(rows)
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight" % (cr, mi, pc, ml))
    return pc, ml


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
