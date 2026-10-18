"""The cracker and mirror sheets, run on the cut pack: every ask figure as the two natural careful paths compute it,
scored against the golden (a hit within half a unit of the asked rounding), and the pair ceiling.

The cracker lands the call, runs the hygiene battery and executes every documented handling: it converts the OMS
clock to local time, maps each outage line to its transformer's district, filters the cause list, takes the GIS changes
under PTR in the pilot window (blank work orders included, the reason code carrying them) and divides every charge on
the pilot's orders by them. The mirror stops at the default path on the call and reads the asks off the first file
that answers them: completed work orders, their planned sizes, the OMS district and dates as exported.

    python3 cracker.py [target]"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C  # noqa: E402

REC_W, CRIT_W, IF_W, ASK_W = 0.33, 0.05, 0.07, 0.55


def cracker_asks(P):
    c = P.chg.copy()
    c["date"] = pd.to_datetime(c["change_date"])
    dist = dict(zip(P.gis["xfmr_loc_id"], P.gis["district"]))
    c["district"] = c["xfmr_loc_id"].map(dist)
    ptr = c[(c.reason_code == "PTR") & (c.date >= C.PILOT_LO) & (c.date <= C.PILOT_HI) & c.district.isin(C.PILOT)]
    n = ptr.groupby("district").size().reindex(C.PILOT)
    kva = (ptr.installed_kva - ptr.removed_kva).groupby(ptr.district).sum().reindex(C.PILOT)
    wo_d = dict(zip(P.wo["Work Order"].astype(str), P.wo["District"]))
    cost = P.cost.copy()
    cost["amt"] = cost["amount_usd"].astype(float)
    tot = cost.groupby(cost["wo_number"].map(wo_d))["amt"].sum().reindex(C.PILOT)
    A = pd.DataFrame({"replaced": n, "kva_added": kva, "cost_per": tot / n})
    o = P.oms.copy()
    o["start"] = pd.to_datetime(o["outage_start_utc"]) - pd.Timedelta(hours=7)
    o["end"] = pd.to_datetime(o["restored_utc"]) - pd.Timedelta(hours=7)
    f = o[(o.cause_code == "EQ-XFMR") & (o.start >= pd.Timestamp("2026-06-01")) & (o.start < pd.Timestamp("2026-10-01"))].copy()
    f["district"] = f["xfmr_loc_id"].map(dist)
    f["hours"] = (f["end"] - f["start"]).dt.total_seconds() / 3600.0
    ch = (f["customers_out"] * f["hours"]).groupby(f["district"]).sum().reindex(C.NAMES)
    o8 = f[f.hours > 8].groupby("district")["customers_out"].sum().reindex(C.NAMES).fillna(0)
    B = pd.DataFrame({"customer_hours": ch, "over_8h": o8})
    return A, B


def mirror_asks(P):
    w = P.wo
    comp = w[w["Status"] == "COMP"]
    n = comp.groupby("District").size().reindex(C.PILOT)
    kva = (comp["Planned To kVA"] - comp["Planned From kVA"]).groupby(comp["District"]).sum().reindex(C.PILOT)
    wo_d = dict(zip(comp["Work Order"].astype(str), comp["District"]))
    cost = P.cost.copy()
    cost["amt"] = cost["amount_usd"].astype(float)
    tot = cost.groupby(cost["wo_number"].map(wo_d))["amt"].sum().reindex(C.PILOT)
    A = pd.DataFrame({"replaced": n, "kva_added": kva, "cost_per": tot / n})
    o = P.oms.copy()
    o["start"] = pd.to_datetime(o["outage_start_utc"])
    o["end"] = pd.to_datetime(o["restored_utc"])
    f = o[(o.cause_code == "EQ-XFMR") & (o.start >= pd.Timestamp("2026-06-01")) & (o.start < pd.Timestamp("2026-10-01"))].copy()
    f["hours"] = (f["end"] - f["start"]).dt.total_seconds() / 3600.0
    ch = (f["customers_out"] * f["hours"]).groupby(f["dispatch_district"]).sum().reindex(C.NAMES)
    o8 = f[f.hours > 8].groupby("dispatch_district")["customers_out"].sum().reindex(C.NAMES).fillna(0)
    B = pd.DataFrame({"customer_hours": ch, "over_8h": o8})
    return A, B


def score(A, B, GA, GB):
    rows = []
    for d in C.PILOT:
        rows.append(("A replaced " + d, A.loc[d, "replaced"], GA.loc[d, "replaced"], 0.5))
        rows.append(("A kVA added " + d, A.loc[d, "kva_added"], GA.loc[d, "kva_added"], 0.05))
        rows.append(("A cost per " + d, A.loc[d, "cost_per"], GA.loc[d, "cost_per"], 0.5))
    for d in C.NAMES:
        rows.append(("B customer-hours " + d, B.loc[d, "customer_hours"], GB.loc[d, "customer_hours"], 0.5))
        rows.append(("B over 8 h " + d, B.loc[d, "over_8h"], GB.loc[d, "over_8h"], 0.5))
    out = pd.DataFrame(rows, columns=["figure", "path", "golden", "tol"])
    out["hit"] = (out["path"] - out["golden"]).abs() < out["tol"]
    return out


def main(target=None):
    target = target or C.TARGET
    G = C.golden(target)
    P = G["P"]
    cA, cB = cracker_asks(P)
    mA, mB = mirror_asks(P)
    sc = score(cA, cB, G["A"], G["B"])
    sm = score(mA, mB, G["A"], G["B"])
    n = len(sc)
    chart = 3                                  # bars per district, value labels, title and axis
    # the chart's structure is banked by both; its labels carry the B figures
    Lc = (sc["hit"].sum() + 2) / (n + chart)
    Lm = (sm["hit"].sum() + 2) / (n + chart)
    Cs = 100 * (REC_W + CRIT_W + IF_W + ASK_W * Lc)
    Ms = 100 * (0.05 + IF_W + ASK_W * Lm)
    print(pd.DataFrame({"figure": sc["figure"], "golden": sc["golden"].round(2), "cracker": sc["path"].round(2),
                        "cracker hit": sc["hit"], "mirror": sm["path"].round(2), "mirror hit": sm["hit"]}).to_string(index=False))
    print("\ncracker keeps %d of %d ask figures, mirror %d" % (sc["hit"].sum(), n, sm["hit"].sum()))
    print("ask weight kept: cracker %.1f%%, mirror %.1f%%" % (100 * Lc, 100 * Lm))
    print("pair ceiling: (%.1f + %.1f) / 2 = %.1f" % (Cs, Ms, (Cs + Ms) / 2))
    return dict(cracker=sc, mirror=sm, Lc=Lc, Lm=Lm, pair=(Cs + Ms) / 2)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
