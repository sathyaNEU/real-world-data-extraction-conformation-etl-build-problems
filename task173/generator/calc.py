"""task173 computations on the shipped pack only: the default path and its rivals, the golden and its family, and
the asks. Every function reads target/ files; nothing here touches the world.

    python3 calc.py <target>      prints the main figures"""
from __future__ import annotations

import csv
import datetime as dt
import os
import re
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402

LONG = {"STREET": "ST", "AVENUE": "AVE", "DRIVE": "DR", "LANE": "LN", "COURT": "CT", "TRAIL": "TRL", "ROAD": "RD",
        "BOULEVARD": "BLVD", "CIRCLE": "CIR", "PLACE": "PL", "PARKWAY": "PKWY"}
W0 = dt.date(2024, 10, 1)
W1 = dt.date(2026, 9, 30)


def pdate(s):
    if not s:
        return None
    if isinstance(s, dt.datetime):
        return s.date()
    if isinstance(s, dt.date):
        return s
    if "/" in s:
        m, d, y = s.split("/")
        return dt.date(int(y), int(m), int(d))
    return dt.date.fromisoformat(s[:10])


def norm_addr(a):
    a = re.sub(r"\s+", " ", a.strip().upper())
    parts = a.split(" ")
    if parts and parts[-1] in LONG:
        parts[-1] = LONG[parts[-1]]
    return " ".join(parts)


def rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def xlsx_rows(path):
    from openpyxl import load_workbook
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    it = ws.iter_rows(values_only=True)
    head = None
    out = []
    for r in it:
        if head is None:
            if r and r[0] is not None and str(r[0]).isupper():
                head = [str(x) for x in r]
            continue
        if r[0] is None:
            continue
        out.append(dict(zip(head, r)))
    return out


class Pack:
    """the shipped files, parsed once"""

    def __init__(self, target):
        self.t = target
        self.svc = rows(os.path.join(target, C.F_GIS_SVC))
        self.svc_by_addr = {}
        nodir = defaultdict(list)
        for s in self.svc:
            a = norm_addr(s["SERVICE_ADDRESS"])
            self.svc_by_addr[a] = s["SERVICE_ID"]
            p = a.split(" ")
            if len(p) > 2 and p[1] in ("N", "S", "E", "W"):
                nodir[" ".join([p[0]] + p[2:])].append(s["SERVICE_ID"])
        self.svc_nodir = {k: v[0] for k, v in nodir.items() if len(v) == 1}
        self.svc_attr = {s["SERVICE_ID"]: s for s in self.svc}
        self.prem = rows(os.path.join(target, C.F_PREM))
        self.prem_svc = {}
        for p in self.prem:
            sid = p["SERVICE_ID"] or self.match(p["SERVICE_ADDRESS"])
            self.prem_svc[p["PREMISE_ID"]] = sid
        self.meter = rows(os.path.join(target, C.F_METER))
        self.eam = xlsx_rows(os.path.join(target, C.F_EAM))
        self.legacy = rows(os.path.join(target, C.F_LEGACY))
        self.ami = rows(os.path.join(target, C.F_AMI))

    def match(self, addr):
        a = norm_addr(addr)
        if a in self.svc_by_addr:
            return self.svc_by_addr[a]
        p = a.split(" ")
        k = " ".join([p[0]] + p[2:]) if len(p) > 2 and p[1] in ("N", "S", "E", "W") else a
        return self.svc_nodir.get(k)

    # ------------------------------------------------------------------ the record's service leak repairs
    def repairs(self):
        """one row per leak repaired: (service id, completed date, component); EAM from the cutover, legacy before"""
        out = []
        for r in self.eam:
            if r["WORK_TYPE"] == "SERVICE LEAK" and r["WORK_CLASS"] == "REP" and r["STATUS"] == "CLOSED":
                out.append((r["ASSET_ID"], pdate(r["COMPLETED"]), r["COMPONENT"] or ""))
        for r in self.legacy:
            if r["WO_TYPE"] == "SVC LEAK" and r["STATUS"] == "CLOSED":
                out.append((self.match(r["ADDRESS"]), pdate(r["COMP_DATE"]), ""))
        return out

    def exchanges(self):
        """one row per meter exchange: (service id, the day the new meter was set, reason, performed by)"""
        rem = {}
        out = []
        for r in self.meter:
            if r["EVENT_TYPE"] == "REMOVE":
                rem[r["PREMISE_ID"]] = r
            elif r["EVENT_TYPE"] == "SET" and r["REASON"] != "NEW":
                x = rem.pop(r["PREMISE_ID"], None)
                out.append((self.prem_svc.get(r["PREMISE_ID"]), pdate(r["EVENT_DATE"]), r["REASON"], r["PERFORMED_BY"],
                            pdate(x["EVENT_DATE"]) if x else None))
        return out


# ---------------------------------------------------------------------- the main call
def default_path(P, reps=None):
    reps = reps if reps is not None else P.repairs()
    n = sum(1 for s, d, c in reps if d and W0 <= d <= W1)
    return n / 2.0


def per_year(reps):
    out = defaultdict(int)
    for s, d, c in reps:
        if d:
            out[d.year] += 1
    return dict(out)


def excess_per_exchange(P, reps, ex, W=120, since=None, base="pooled"):
    """leaks repaired on a service in the W days after its own exchange, less the service's own expected repairs in
    that window, per exchange; exchanges whose window closes after 30 September 2026 are left out"""
    by = defaultdict(list)
    for s, d, c in reps:
        if s and d:
            by[s].append(d)
    for s in by:
        by[s].sort()
    ex = [e for e in ex if e[0] and e[1] and e[1] + dt.timedelta(days=W) <= W1 and (since is None or e[1] >= since)]
    hits = 0
    for s, d, *_ in ex:
        for x in by.get(s, ()):
            if d < x <= d + dt.timedelta(days=W):
                hits += 1
    n = len(ex)
    # the base: repairs per service-day over the record outside every post-exchange window
    if base == "pooled":
        t0 = since or dt.date(2012, 1, 1)
        days = (W1 - t0).days + 1
        nsvc = len(P.svc)
        win = defaultdict(list)
        for s, d, *_ in ex:
            win[s].append(d)
        inside = 0
        for s, ds in win.items():
            for x in by.get(s, ()):
                if x >= t0 and any(d < x <= d + dt.timedelta(days=W) for d in ds):
                    inside += 1
        tot = sum(1 for s, d, c in reps if d and d >= t0)
        rate = (tot - inside) / (nsvc * days - n * W)
        bexp = rate * W * n
    elif base == "own":
        # each exchanged service's own repairs in the year before its exchange
        bexp = 0.0
        for s, d, *_ in ex:
            bexp += sum(1 for x in by.get(s, ()) if d - dt.timedelta(days=365) < x <= d) * W / 365.0
    return (hits - bexp) / n, hits, n, bexp


def delay_profile(P, reps, ex, W=180):
    """the share of an exchange's excess repairs by days after it, net of the base, 10-day bins"""
    by = defaultdict(list)
    for s, d, c in reps:
        if s and d:
            by[s].append(d)
    ex = [e for e in ex if e[0] and e[1] and e[1] + dt.timedelta(days=W) <= W1]
    hist = np.zeros(W // 10)
    for s, d, *_ in ex:
        for x in by.get(s, ()):
            k = (x - d).days
            if 0 < k <= W:
                hist[(k - 1) // 10] += 1
    floor = np.median(hist[-6:])
    net = np.clip(hist - floor, 0, None)
    cdf = np.concatenate([[0], np.cumsum(net) / net.sum()])
    return cdf


def ami_exchanges(P):
    out = []
    for r in P.ami:
        if r["WORK_TYPE"] == "METER EXCHANGE":
            out.append(pdate(r["PLANNED_WEEK_OF"]))
    return out


def golden(P, W=120, base="pooled", since=None, reps=None, ex=None):
    reps = reps if reps is not None else P.repairs()
    ex = ex if ex is not None else P.exchanges()
    e, hits, n, bexp = excess_per_exchange(P, reps, ex, W=W, since=since, base=base)
    cdf = delay_profile(P, reps, ex)
    wk = ami_exchanges(P)
    frac = []
    for d in wk:
        rem = (dt.date(2027, 12, 31) - (d + dt.timedelta(days=2))).days
        frac.append(np.interp(min(rem, 180), np.arange(0, 181, 10), cdf))
    induced = e * float(np.sum(frac))
    hist = default_path(P, reps)
    ex_win = sum(1 for x in ex if x[1] and W0 <= x[1] <= W1) / 2.0
    base27 = hist - e * ex_win
    return {"total": base27 + induced, "base": base27, "induced": induced, "excess": e, "hits": hits, "n_exch_hist": n,
            "n_ami": len(wk), "hist_rate": hist, "ex_per_year": ex_win, "bexp": bexp}


if __name__ == "__main__":
    import time
    t = time.time()
    P = Pack(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
    print("loaded %.1fs" % (time.time() - t))
    reps = P.repairs()
    ex = P.exchanges()
    print("repairs", len(reps), "unmatched", sum(1 for s, d, c in reps if not s), "per year", sorted(per_year(reps).items()))
    print("exchanges", len(ex), "unmatched", sum(1 for e in ex if not e[0]))
    print("default", default_path(P, reps))
    for W in (60, 90, 120, 180, 365):
        g = golden(P, W=W, reps=reps, ex=ex)
        print("W", W, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in g.items()})
    g = golden(P, W=120, base="own", reps=reps, ex=ex)
    print("own-base", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in g.items()})
    g = golden(P, W=120, since=dt.date(2021, 6, 1), reps=reps, ex=ex)
    print("EAM only", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in g.items()})


# ---------------------------------------------------------------------- the asks
FY_MONTHS = [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]
MON = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov",
       12: "Dec"}
GROUPS = {"0410": "Asphalt pavement", "0420": "Concrete pavement", "0430": "Sidewalk and driveway",
          "0431": "Sidewalk and driveway", "0440": "Sod"}
GROUP_ORDER = ["Asphalt pavement", "Concrete pavement", "Sidewalk and driveway", "Sod"]


def main_centres(target):
    return {r["MAIN_ID"]: r["SVC_CENTER"] for r in rows(os.path.join(target, C.F_GIS_MAIN))}


def ask_breaks(P, route="golden"):
    """fiscal 2026 main breaks by service centre and month of the permanent repair"""
    cen = main_centres(P.t)
    yard_cen = {v: k for k, v in C.YARD.items()}
    rr = [r for r in P.eam if r["WORK_TYPE"] == "MAIN BREAK" and r["WORK_CLASS"] in ("REP", "REPC")]
    if route != "with_cancelled":
        rr = [r for r in rr if r["STATUS"] == "CLOSED"]
    out = defaultdict(int)
    if route in ("golden", "with_cancelled", "golden_yard", "asset_reported"):
        brk = {}
        for r in rr:
            k = (r["ASSET_ID"], r["REPORTED"]) if route == "asset_reported" else (r["ASSET_ID"], r["REPORTED"], r["ADDRESS"])
            d = pdate(r["COMPLETED"])
            if d is None:
                continue
            if k not in brk or d > brk[k][0]:
                brk[k] = (d, r)
        items = [(d, r) for d, r in brk.values()]
    elif route == "rows":
        items = [(pdate(r["COMPLETED"]), r) for r in rr if r["COMPLETED"]]
    elif route == "rep_only":
        items = [(pdate(r["COMPLETED"]), r) for r in rr if r["COMPLETED"] and r["WORK_CLASS"] == "REP"]
    elif route == "first_row":
        brk = {}
        for r in sorted(rr, key=lambda x: pdate(x["COMPLETED"]) or dt.date(2099, 1, 1)):
            k = (r["ASSET_ID"], r["REPORTED"], r["ADDRESS"])
            if k not in brk and r["COMPLETED"]:
                brk[k] = (pdate(r["COMPLETED"]), r)
        items = list(brk.values())
    elif route == "asset_initiated":
        brk = {}
        for r in rr:
            k = (r["ASSET_ID"], pdate(r["INITIATED"]))
            d = pdate(r["COMPLETED"])
            if d and (k not in brk or d > brk[k][0]):
                brk[k] = (d, r)
        items = list(brk.values())
    for d, r in items:
        if not (C.FY26[0] <= d <= C.FY26[1]):
            continue
        c = yard_cen[r["CREW_YARD"]] if route == "golden_yard" else cen.get(r["ASSET_ID"])
        out[(c, d.month)] += 1
    return {(c, m): out.get((c, m), 0) for c in C.CENTERS for m in FY_MONTHS}


def paid_revisions(tot, revs, ap, route="golden"):
    """the revision of each estimate that Finance paid: a voucher's gross equals one revision's total, or the sum of
    two estimates' revisions where one invoice covered two months"""
    gross = [round(float(r["GROSS_AMOUNT"]), 2) for r in ap]
    pick = {}
    if route in ("latest", "first"):
        return {e: (max(rs) if route == "latest" else min(rs)) for e, rs in revs.items()}
    left = []
    for gv in gross:
        m = [(e, rv) for (e, rv), t in tot.items() if abs(round(t, 2) - gv) < 0.005]
        if len(m) == 1:
            pick[m[0][0]] = m[0][1]
        else:
            left.append(gv)
    if route in ("one_to_one_latest", "one_to_one_first"):
        for e, rs in revs.items():
            if e not in pick:
                pick[e] = max(rs) if route.endswith("latest") else min(rs)
        return pick
    open_e = sorted(e for e in revs if e not in pick)
    for gv in left:
        hit = [(a, ra, b, rb) for i, a in enumerate(open_e) for b in open_e[i + 1:] for ra in revs[a] for rb in revs[b]
               if abs(round(tot[(a, ra)] + tot[(b, rb)], 2) - gv) < 0.005]
        if len(hit) == 1:
            a, ra, b, rb = hit[0]
            pick[a], pick[b] = ra, rb
    return pick


def ask_restoration(target, route="golden"):
    """fiscal 2026 restoration square yards by surface type and quarter of completion, on the accepted revision"""
    lines = xlsx_rows(os.path.join(target, C.F_PAYEST))
    ap = rows(os.path.join(target, C.F_AP))
    paid = {r["INVOICE_NO"]: float(r["GROSS_AMOUNT"]) for r in ap}
    tot = defaultdict(float)
    revs = defaultdict(set)
    for x in lines:
        tot[(x["ESTIMATE_NO"], int(x["REVISION"]))] += float(x["AMOUNT"])
        revs[x["ESTIMATE_NO"]].add(int(x["REVISION"]))
    pick = paid_revisions(tot, revs, ap, route)
    out = defaultdict(float)
    for x in lines:
        g = GROUPS.get(str(x["ITEM"]))
        if g is None:
            continue
        if route != "all" and int(x["REVISION"]) != pick.get(x["ESTIMATE_NO"]):
            continue
        d = pdate(x["WORK_COMPLETED"])
        if route == "golden_period":
            y, m = str(x["PERIOD"]).split("-")
            d = dt.date(int(y), int(m), 1)
        fy, q = C.fy_quarter(d)
        if fy != 2026:
            continue
        out[(g, q)] += float(x["QTY"])
    return {(g, q): out.get((g, q), 0.0) for g in GROUP_ORDER for q in (1, 2, 3, 4)}
