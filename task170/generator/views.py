"""The clean view of the register as it stood at the pull, built from the simulated truth (no Layer 1 mess: one
layout, one key, no re-sent rows), and the realised outcome over the window for reference."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import common as C
import world as WD

D = dt.date


def outcome_dates(W):
    """Outcome code, date and the date it was posted, for every child that leaves before December 2027. A child is
    lost to follow-up 28 days after the first appointment missed; a transfer out or a death is dated in the month the
    child left; the transfer to adult care on the twentieth birthday."""
    if "odate" in W:
        return
    rng = np.random.default_rng(C.SEED + 11)
    V = W["V"]
    N = W["N"]
    # last visit before the exit, per child
    order = np.lexsort((V["t"], V["i"]))
    last_idx = {}
    for k in order:
        last_idx[V["i"][k]] = k
    odate = [None] * N
    posted = [None] * N
    for i in range(N):
        e = int(W["exitm"][i])
        if e > C.M_END_SIM:
            continue
        typ = W["xtype"][i]
        k = last_idx.get(i)
        if k is None:
            continue
        lv = WD.visit_date(W, i, int(V["t"][k]))
        nxt = add_months(lv, int(V["cad"][k]))
        if typ == "LTFU":
            od = nxt + dt.timedelta(days=28)
        elif typ == "ADULT":
            bm = int(W["bm"][i])
            y, m = C.ym(bm + 240)
            od = D(y, m, 15)
        else:
            y, m = C.ym(e)
            od = max(lv + dt.timedelta(days=1), D(y, m, int(rng.integers(1, 28))))
        odate[i] = od
        posted[i] = od + dt.timedelta(days=int(rng.integers(0, 76)))
    W["odate"] = odate
    W["oposted"] = posted


def add_months(d, k):
    y, m = d.year + (d.month - 1 + k) // 12, (d.month - 1 + k) % 12 + 1
    return D(y, m, min(d.day, 28))


def dob_of(W, i):
    y, m = C.ym(int(W["bm"][i]))
    return D(y, m, int(1 + (i * 7919) % 28))


def truth_view(W, upto=C.COUNT, ship_from=C.SHIP_FROM):
    outcome_dates(W)
    N = W["N"]
    kids = []
    for i in range(N):
        y, m = C.ym(int(W["enrol"][i]))
        st = D(y, m, int(1 + (i * 104729) % 28))
        od, po = W["odate"][i], W["oposted"][i]
        known = (od is not None) and (po <= C.PULL) and (od <= upto)
        kids.append(dict(uid=i, dob=dob_of(W, i), sex="F" if W["sex"][i] == 0 else "M", art_start=st,
                         outcome=W["xtype"][i] if known else None, outcome_date=od if known else None))
    kids = pd.DataFrame(kids)
    V = W["V"]
    sel = (V["t"] >= C.month_of(ship_from)) & (V["t"] <= C.month_of(upto))
    rows = []
    for k in np.where(sel)[0]:
        i = int(V["i"][k]); t = int(V["t"][k])
        d = WD.visit_date(W, i, t)
        if d > upto:
            continue
        rows.append((i, d, V["w"][k], V["reg"][k], int(V["cad"][k]), add_months(d, int(V["cad"][k]))))
    visits = pd.DataFrame(rows, columns=["uid", "date", "weight", "regimen", "months", "next_appt"])
    return kids, visits


def realised(W):
    """Bottles the children under 15 at the count would actually take over the window, from the simulation's own
    future (switches and exits): for reference only, never graded."""
    N = W["N"]
    pop = ((C.M_COUNT - W["bm"]) / 12 < 15) & (W["enrol"] <= C.M_COUNT) & (W["exitm"] > C.M_COUNT)
    tld = pop & ~W["second"]
    cm = []
    for m in C.M_WIN:
        cm.append(int((tld & (W["switch"] <= m) & (W["exitm"] > m)).sum()))
    return sum(cm) + C.MAX_MONTHS * cm[-1], cm
