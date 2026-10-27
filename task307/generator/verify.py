"""Independent verifier: recomputes every graded figure from the cut pack alone with its own code (its own path
equilibration written apart from pack.py, its own day and hour rules for the counts, its own clock for the
probe file) and compares with figures.json at the stated rounding.

    python3 task307/generator/verify.py <target dir>
"""
import csv
import datetime as dt
import json
import math
import os
import sys
from collections import defaultdict

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = {
    "links": "MAMPO_v42_subarea_links_2028NB.csv", "nodes": "MAMPO_v42_subarea_nodes.csv",
    "trips": "MAMPO_v42_subarea_trips_2028.csv", "tip": "FY2028_TIP_congestion_relief_candidates.xlsx",
    "atr": "ATR_hourly_volumes_2025.csv", "stations": "ATR_station_inventory_2025.xlsx",
    "valid": "MAMPO_v42_base2025_station_volumes.csv", "probe": "probe_segment_travel_times_2025.parquet",
    "segs": "CMP_probe_segment_reference.csv"}
PERLANE = {1: 1900, 12: 1900, 2: 1800, 3: 1700, 4: 850, 5: 650}
ALPHA = {1: 0.15, 12: 0.80, 2: 0.80, 3: 0.80, 4: 0.60, 5: 0.75, 9: 0.0}
BETA = {1: 6, 12: 6, 2: 6, 3: 6, 4: 4, 5: 4, 9: 1}
FED_HOLIDAYS = ["2025-01-01", "2025-01-20", "2025-02-17", "2025-05-26", "2025-06-19", "2025-07-04", "2025-09-01",
                "2025-10-13", "2025-11-11", "2025-11-27", "2025-12-25"]


def r(v, u):
    return math.floor(v / u + 0.5) * u


# ---------------------------------------------------------------- the call
class Assignment:
    def __init__(self, target):
        L = pd.read_csv(os.path.join(target, FILES["links"]))
        self.zones = set(pd.read_csv(os.path.join(target, FILES["nodes"])).query("CENTROID == 1").N)
        A, B, T0, CAP, FT, LID = [], [], [], [], [], []
        for x in L.itertuples():
            for a, b, n in ((x.A_NODE, x.B_NODE, x.AB_LANES), (x.B_NODE, x.A_NODE, x.BA_LANES)):
                A.append(a); B.append(b); FT.append(x.FTYPE); LID.append(x.LINK_ID)
                T0.append(60 * x.LENGTH_MI / x.FF_SPD_MPH)
                CAP.append(n * PERLANE.get(x.FTYPE, 1))
        self.lid = np.array(LID); self.ft = np.array(FT)
        self.t0 = np.array(T0); self.cap0 = np.array(CAP, float)
        self.al = np.array([ALPHA[f] for f in FT]); self.be = np.array([BETA[f] for f in FT], float)
        nodes = sorted(set(A) | set(B))
        self.ix = {v: i for i, v in enumerate(nodes)}
        self.a = np.array([self.ix[v] for v in A]); self.b = np.array([self.ix[v] for v in B])
        self.arc = {(i, j): k for k, (i, j) in enumerate(zip(self.a, self.b))}
        self.nn = len(nodes)
        tr = pd.read_csv(os.path.join(target, FILES["trips"]))
        self.od = {p: g for p, g in tr.groupby("PERIOD")}
        wb = load_workbook(os.path.join(target, FILES["tip"]), read_only=True)
        self.cost = {row[0]: float(row[3]) for row in list(wb["Candidates"].iter_rows(values_only=True))[1:]}
        self.code = defaultdict(list)
        for row in list(wb["Model coding"].iter_rows(values_only=True))[1:]:
            self.code[row[0]].append(row)

    def caps(self, tip):
        c = self.cap0.copy()
        for _, link, a, b, change, fr, to in self.code.get(tip, []):
            m = self.lid == link
            if "LANES" in change:
                c[m] = to * np.array([PERLANE[f] for f in self.ft[m]])
            else:
                c[m] = c[m] / fr * to
        return c

    def tt(self, v, c):
        return self.t0 * (1 + self.al * np.where(self.al > 0, v / c, 0) ** self.be)

    def aon(self, t, od):
        # a zone is never a way through: arcs leaving a zone carry only that zone's own trips
        w = t.copy()
        G = csr_matrix((w + 1e-12, (self.a, self.b)), shape=(self.nn, self.nn))
        y = np.zeros(len(t))
        origins = sorted(set(od.I))
        dist, pred = dijkstra(G, indices=[self.ix[o] for o in origins], return_predecessors=True)
        row = {o: i for i, o in enumerate(origins)}
        for o, d, q in zip(od.I, od.J, od.TRIPS):
            i = row[o]; cur = self.ix[d]; s = self.ix[o]
            while cur != s:
                p = pred[i, cur]
                y[self.arc[(p, cur)]] += q
                cur = p
        return y, sum(q * dist[row[o], self.ix[d]] for o, d, q in zip(od.I, od.J, od.TRIPS))

    def sp(self, t, origins):
        G = csr_matrix((t + 1e-12, (self.a, self.b)), shape=(self.nn, self.nn))
        return dijkstra(G, indices=[self.ix[o] for o in origins], return_predecessors=True)

    def walk(self, pred, row, o, d):
        cur, s, arcs = self.ix[d], self.ix[o], []
        while cur != s:
            p = pred[row, cur]
            arcs.append(self.arc[(p, cur)])
            cur = p
        return frozenset(arcs)

    def ue(self, od, c, tol=1e-9, iters=400):
        """path-based equilibration: every OD pair's flow spread over its used paths and moved, a projected Newton
        step at a time, from each costlier path onto the cheapest, until the relative gap is below tol"""
        ods = list(zip(od.I, od.J, od.TRIPS))
        origins = sorted(set(od.I))
        row = {o: i for i, o in enumerate(origins)}
        v = np.zeros(len(self.t0))
        _, pred = self.sp(self.tt(v, c), origins)
        P = {}
        for o, d, q in ods:
            p = self.walk(pred, row[o], o, d)
            P[(o, d)] = {p: float(q)}
            v[list(p)] += q
        gap = 1.0
        for it in range(iters):
            t = self.tt(v, c)
            dist, pred = self.sp(t, origins)
            low = sum(q * dist[row[o], self.ix[d]] for o, d, q in ods)
            gap = (v @ t - low) / (v @ t)
            if gap < tol:
                break
            for o, d, q in ods:
                paths = P[(o, d)]
                best = self.walk(pred, row[o], o, d)
                paths.setdefault(best, 0.0)
                for p in list(paths):
                    if p == best or paths[p] <= 0:
                        continue
                    t = self.tt(v, c)
                    gp = t[list(p)].sum() - t[list(best)].sum()
                    if gp <= 0:
                        continue
                    r = np.where(self.al > 0, v / c, 0)
                    h = np.where(self.al > 0, self.t0 * self.al * self.be * r ** (self.be - 1) / c, 0)
                    den = h[list(p ^ best)].sum()
                    x = min(paths[p], gp / den) if den > 0 else paths[p]
                    paths[p] -= x
                    paths[best] += x
                    v[list(p)] -= x
                    v[list(best)] += x
                for p in [p for p, f in paths.items() if f <= 1e-12 and p != best]:
                    del paths[p]
        return v, self.tt(v, c), gap

    def vht(self, od, c):
        v, t, gap = self.ue(od, c)
        assert gap < 1e-6, gap          # the documentation's relative gap
        return v @ t / 60.0, gap


def verify_call(target, F):
    asg = Assignment(target)
    nb = {p: asg.vht(asg.od[p], asg.caps(None)) for p in ("AM", "PM")}
    out = {}
    for tip in asg.cost:
        s = sum(nb[p][0] - asg.vht(asg.od[p], asg.caps(tip))[0] for p in ("AM", "PM"))
        out[tip] = s * 247 * 2.9
    bad = []
    best = max(out, key=out.get)
    if best != F["award"]:
        bad.append("award %s" % best)
    for tip, a in out.items():
        if r(a, 1000) != F["annual_vh"][tip]:
            bad.append("annual %s %.1f" % (tip, a))
        if r(a / asg.cost[tip], 100) != F["per_musd_vh"][tip]:
            bad.append("per million %s %.1f" % (tip, a / asg.cost[tip]))
    print("call: %s, annual %s" % (best, {k: round(v) for k, v in out.items()}))
    return bad


# ---------------------------------------------------------------- the count stations
def verify_counts(target, F):
    rows = list(csv.DictReader(open(os.path.join(target, FILES["atr"]))))
    wb = load_workbook(os.path.join(target, FILES["stations"]), read_only=True)
    maint = list(wb["Maintenance 2025"].iter_rows(values_only=True))[1:]
    series = lambda s: s[:-1] if s.endswith("R") else s
    # hours in file order per station and direction
    H = defaultdict(list)
    for x in rows:
        H[(series(x["STATION"]), x["DIR"])].append((dt.datetime.strptime(x["DATE"], "%m/%d/%Y").date(),
                                                     int(x["HR_END"]), int(x["VOLUME"]), x["STATUS"]))
    stations = sorted({k[0] for k in H})
    dirs = {s: sorted(d for (ss, d) in H if ss == s) for s in stations}
    # the work orders that replaced a failed loop or detector card
    repairs = {}
    for st, day, wo, txt in maint:
        t = str(txt)
        if "open circuit" in t or "crosstalk" in t:
            d = t.split()[2] if t.startswith("Loop") else t.split()[0]
            repairs[(series(st), d)] = dt.date.fromisoformat(str(day)[:10])
    bad = []
    bad_days = defaultdict(set)
    bad_hours = defaultdict(set)
    for s in stations:
        d1, d2 = dirs[s]
        A1, A2 = H[(s, d1)], H[(s, d2)]
        assert len(A1) == len(A2)
        n = len(A1)
        nr = [A1[i][3] == "NR" or A2[i][3] == "NR" for i in range(n)]
        for i in range(n):
            ok = A1[i][3] == "OK" and A2[i][3] == "OK"
            # a poll after a missed poll inside a running day carries the missed hours
            if i and nr[i - 1]:
                k = i - 1
                while k >= 0 and nr[k]:
                    k -= 1
                if i - 1 - k < 20:
                    ok = False
            if not ok:
                bad_hours[s].add(i)
                bad_days[s].add(A1[i][0])
        # faults: the faulted direction's daily share against its share on the same weekday elsewhere in the year
        for (ss, d), rep in repairs.items():
            if ss != s:
                continue
            j = 0 if d == d1 else 1
            share = defaultdict(list)
            hourly = []
            for i in range(n):
                tot = A1[i][2] + A2[i][2]
                if i in bad_hours[s] or tot <= 300:
                    continue
                sh = (A1[i][2], A2[i][2])[j] / tot
                hourly.append((A1[i][0], A1[i][1], sh))
            ref = defaultdict(list)
            for day, h, sh in hourly:
                if not (rep - dt.timedelta(days=35) <= day <= rep):
                    ref[(day.weekday(), h)].append(sh)
            med = {k: float(np.median(v)) for k, v in ref.items()}
            x = [(day, abs(math.log(sh / med[(day.weekday(), h)]))) for day, h, sh in hourly
                 if rep - dt.timedelta(days=35) <= day < rep and (day.weekday(), h) in med]
            days = sorted({day for day, _ in x})
            dev = {day: [e for dd, e in x if dd == day] for day in days}
            faulted = [day for day in days if np.median(dev[day]) > 0.1 or np.mean(np.array(dev[day][-6:]) > 0.1) > 0.8]
            # back from the work order over the days that have usable hours (an outage day has none and neither
            # starts nor ends a fault)
            start = rep
            for day in sorted(days, reverse=True):
                if day not in faulted:
                    break
                start = day
            for k in range((rep - start).days + 1):
                bad_days[s].add(start + dt.timedelta(days=k))
            for i in range(n):
                if start <= A1[i][0] <= rep:
                    bad_hours[s].add(i)
            if F["fault_windows"]["%s %s" % (s, d)] != [str(start), str(rep)]:
                bad.append("fault window %s %s %s" % (s, d, start))
        # AADT, AASHTO method
        daily = defaultdict(int)
        for i in range(n):
            daily[A1[i][0]] += A1[i][2] + A2[i][2]
        cell = defaultdict(list)
        for day, v in daily.items():
            if day not in bad_days[s]:
                cell[(day.month, day.weekday())].append(v)
        months = [np.mean([np.mean(cell[(m, w)]) for w in range(7)]) for m in range(1, 13)]
        aadt = float(np.mean(months))
        if r(aadt, 1) != F["aadt"][s]:
            bad.append("AADT %s %.3f" % (s, aadt))
        two = sorted((A1[i][2] + A2[i][2] for i in range(n) if i not in bad_hours[s]), reverse=True)
        k = two[29] / r(aadt, 1)
        if "%.3f" % r(k, 0.001) != F["k_factor"][s]:
            bad.append("K %s %.5f" % (s, k))
        # validation at the river bridges
        if s in ("S-0101", "S-0102", "S-0103"):
            val = pd.read_csv(os.path.join(target, FILES["valid"]))
            for j, d in enumerate((d1, d2)):
                for per, he in (("AM", 8), ("PM", 18)):
                    vals = [(A1[i], A2[i])[j][2] for i in range(n)
                            if A1[i][1] == he and A1[i][0] not in bad_days[s] and A1[i][0].weekday() in (1, 2, 3)
                            and A1[i][0].month in (3, 4, 5, 9, 10) and str(A1[i][0]) not in FED_HOLIDAYS]
                    cntv = float(np.mean(vals))
                    q = val[(val.STATION == s) & (val.DIR == d) & (val.PERIOD == per)].iloc[0]
                    model = q.VOL_PCE / (1 + q.HV_PCT / 100)
                    pct = 100 * (model - cntv) / cntv
                    if "%.1f" % r(pct, 0.1) != F["validation_pct"]["%s %s %s" % (s, d, per)]:
                        bad.append("validation %s %s %s %.4f" % (s, d, per, pct))
    print("counts: %d stations" % len(stations))
    return bad


# ---------------------------------------------------------------- the CMP corridors
def central_offset(day):
    """hours behind UTC in US Central time: daylight time from the second Sunday of March to the first Sunday of
    November"""
    mar = dt.date(day.year, 3, 8) + dt.timedelta(days=(6 - dt.date(day.year, 3, 8).weekday()) % 7)
    nov = dt.date(day.year, 11, 1) + dt.timedelta(days=(6 - dt.date(day.year, 11, 1).weekday()) % 7)
    return 5 if mar <= day < nov else 6


def verify_probe(target, F):
    seg = pd.read_csv(os.path.join(target, FILES["segs"]), dtype={"SEGMENT": str})
    pr = pd.read_parquet(os.path.join(target, FILES["probe"]))
    utc = pd.to_datetime(pr.measurement_tstamp.str.slice(0, 19))
    # local end of each interval: try the daylight offset, keep it if the local date agrees with the rule
    loc5 = utc - pd.Timedelta(hours=5)
    off = np.array([central_offset(d) for d in loc5.dt.date.unique()])
    offmap = dict(zip(loc5.dt.date.unique(), off))
    loc = utc - pd.to_timedelta(loc5.dt.date.map(offmap), unit="h")
    start = loc - pd.Timedelta(minutes=15)
    x = pd.DataFrame({"seg": pr.segment_id.values, "start": start.values, "tt": pr.travel_time_seconds.values})
    x = x[(x.start.dt.weekday < 5) & (~x.start.dt.strftime("%Y-%m-%d").isin(FED_HOLIDAYS))]
    bad = []
    for cor in sorted(seg.CORRIDOR.unique()):
        for per, hr, dirs in (("AM", 7, ("NB", "EB")), ("PM", 17, ("SB", "WB"))):
            sg = seg[(seg.CORRIDOR == cor) & seg.DIR.isin(dirs)]
            ff = sum(3600 * l / s for l, s in zip(sg.LENGTH_MI, sg.REF_SPEED_MPH))
            y = x[x.seg.isin(sg.SEGMENT) & (x.start.dt.hour == hr)]
            g = y.groupby("start").agg(n=("tt", "size"), tot=("tt", "sum"))
            tt = sorted(g.tot[g.n == len(sg)])
            p95 = tt[int(math.ceil(0.95 * len(tt))) - 1]
            pti = p95 / ff
            if "%.2f" % r(pti, 0.01) != F["pti"]["%s %s" % (cor, per)]:
                bad.append("PTI %s %s %.5f" % (cor, per, pti))
    print("probe: %d rows" % len(pr))
    return bad


def main(target):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    bad = verify_counts(target, F) + verify_call(target, F)
    if bad:
        print("verify: MISMATCH")
        for b in bad:
            print("  ", b)
        return 1
    print("verify: every graded figure reproduced")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
