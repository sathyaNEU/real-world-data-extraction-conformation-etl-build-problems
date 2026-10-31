"""Every graded figure, read back from target/ alone: the call and its components, the ladder's other routes, and
the three asks under the golden handling and the handlings checks.py and ceiling.py price.

    python3 task191/generator/estim.py        # prints the golden call
"""
import csv
import datetime as dt
import math
import os
import sys
from collections import defaultdict
from zoneinfo import ZoneInfo

import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
TZ = ZoneInfo("Europe/Madrid")
UTC = dt.timezone.utc
W0, W1 = dt.date(2026, 1, 1), dt.date(2026, 10, 31)
RATIO = 1.3
COLLISION = {"FCW", "PCW", "FWD_COLL", "PED_COLL"}
PCW = {"PCW", "PED_COLL"}
F = {
    "warnings": "adas_collision_warnings_2025-10_2026-10.csv",
    "fleet": "fleet_register_2026.xlsx",
    "network": "red_paradas_recorridos_2025_2026.xlsx",
    "return": "service_return_2025-10_2026-10.csv",
    "etm": "etm_logons_2026-10.csv",
    "hr": "hr_depot_assignments_2026.csv",
    "incidents": "incident_register_2026.xlsx",
    "bordereau": "insurer_bordereau_2026-01_2026-10.csv",
    "diversions": "mobility_diversions_register_2026.csv",
}
DEPOT_ORDER = ["San Lázaro", "Hornacho", "Valdeolmos", "El Quiñón", "Las Tenerías", "La Ribera", "Santa Clara"]


def dmy(s):
    return dt.datetime.strptime(s, "%d/%m/%Y").date()


def _csv(name, delim=","):
    with open(os.path.join(TARGET, F[name]), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=delim))


# ------------------------------------------------------------------ loading
def load():
    D = {}
    wb = load_workbook(os.path.join(TARGET, F["fleet"]), read_only=True)
    alloc = defaultdict(list)
    for row in list(wb["Allocations"].iter_rows(values_only=True))[1:]:
        fno, dep, a, b = row
        alloc[str(fno)].append((dmy(a), dmy(b) if b else dt.date(2099, 12, 31), dep))
    plates = {}
    for row in list(wb["Registrations"].iter_rows(values_only=True))[1:]:
        fno, p, a, b = row
        plates[p] = str(fno)
    D["alloc"], D["plate_to_fleet"] = alloc, plates
    wb = load_workbook(os.path.join(TARGET, F["network"]), read_only=True)
    stops = {}
    for row in list(wb["Paradas"].iter_rows(values_only=True))[1:]:
        c26, c25, name, lat, lon = row
        stops[str(c26)] = (float(lat), float(lon), name, c25)
    seqs = defaultdict(list)
    for row in list(wb["Recorridos Red 2026"].iter_rows(values_only=True))[1:]:
        line, sentido, orden, code, desde, hasta = row
        seqs[(str(line), sentido, dmy(desde), dmy(hasta) if hasta else dt.date(2099, 12, 31))].append((int(orden), str(code)))
    D["stops"] = stops
    D["seq26"] = {k: [c for _, c in sorted(v)] for k, v in seqs.items()}
    seq25 = defaultdict(list)
    for row in list(wb["Recorridos Red 2025"].iter_rows(values_only=True))[1:]:
        line, sentido, orden, code, hasta = row
        seq25[(str(line), sentido)].append((int(orden), str(code)))
    code25_to_26 = {v[3]: k for k, v in stops.items() if v[3]}
    D["seq25"] = {k: [code25_to_26[c] for _, c in sorted(v)] for k, v in seq25.items()}
    D["warnings"] = _csv("warnings")
    D["return"] = _csv("return", ";")
    return D


def depot_on(D, fno, day):
    for a, b, dep in D["alloc"][fno]:
        if a <= day <= b:
            return dep
    return None


# ------------------------------------------------------------------ warnings and places
def collision_warnings(D, w0=W0, w1=W1, utc_dates=False):
    """The window's collision warnings, one per camera event, with local date, depot and whether braked."""
    seen = set()
    out = []
    for r in D["warnings"]:
        if r["warning_type"] not in COLLISION:
            continue
        if r["event_id"] in seen:
            continue
        seen.add(r["event_id"])
        tu = dt.datetime.strptime(r["event_time_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
        t = tu.astimezone(TZ)
        if not (w0 <= (tu.date() if utc_dates else t.date()) <= w1):
            continue
        if r["firmware"].startswith("1."):
            braked = r["brake_2s"] == "Y"
        else:
            ms = r["brake_reaction_ms"]
            braked = ms != "" and int(ms) <= 2000
        out.append(dict(eid=r["event_id"], fleet=r["fleet_no"], local=t, day=t.date(), dep=depot_on(D, r["fleet_no"], t.date()),
                        lat=float(r["latitude"]), lon=float(r["longitude"]), speed=float(r["speed_kmh"]),
                        pcw=r["warning_type"] in PCW, braked=braked))
    return out


class Segments:
    """The physical stop-to-stop segments of Red 2026 and the bus passes over each in the window."""

    def __init__(self, D, w0=W0, w1=W1):
        self.D = D
        st = D["stops"]
        lat0 = np.mean([v[0] for v in st.values()])
        self.kx = 111_320.0 * math.cos(math.radians(lat0))
        self.ky = 111_320.0
        self.lat0, self.lon0 = lat0, np.mean([v[1] for v in st.values()])
        keys = set()
        self.periods = {}
        for (line, sentido, a, b), seq in D["seq26"].items():
            if b < w0 or a > w1:
                continue
            segs = [tuple(sorted((seq[i], seq[i + 1]))) for i in range(len(seq) - 1)]
            self.periods[(line, sentido, a, b)] = segs
            keys.update(segs)
        self.keys = sorted(keys)
        self.index = {k: i for i, k in enumerate(self.keys)}
        A = np.array([self.xy(*st[k[0]][:2]) for k in self.keys])
        B = np.array([self.xy(*st[k[1]][:2]) for k in self.keys])
        self.A, self.B = A, B
        self.L = np.hypot(*(B - A).T)
        # Passes: operated trips of every line and direction over each segment of the sequence in force that day.
        self.passes = np.zeros(len(self.keys))
        per = defaultdict(int)
        for r in D["return"]:
            day = dmy(r["fecha"])
            if not (w0 <= day <= w1):
                continue
            for (line, sentido, a, b) in self.periods:
                if line == r["linea"] and sentido == r["sentido"] and a <= day <= b:
                    per[(line, sentido, a, b)] += int(r["expediciones_realizadas"])
                    break
        for k, n in per.items():
            for s in self.periods[k]:
                self.passes[self.index[s]] += n
        # Segments that Red 2025 did not have.
        old = set()
        for seq in D["seq25"].values():
            old.update(tuple(sorted((seq[i], seq[i + 1]))) for i in range(len(seq) - 1))
        self.new = np.array([k not in old for k in self.keys])

    def xy(self, lat, lon):
        return ((lon - self.lon0) * self.kx, (lat - self.lat0) * self.ky)

    def snap(self, ws):
        """Each warning's nearest segment and its distance along it from the segment's first stop, in metres."""
        P = np.array([self.xy(w["lat"], w["lon"]) for w in ws])
        seg = np.empty(len(ws), dtype=int)
        pos = np.empty(len(ws))
        d = self.B - self.A
        dd = (d ** 2).sum(1)
        for i in range(0, len(ws), 1500):
            p = P[i:i + 1500][:, None, :]
            t = np.clip(((p - self.A[None]) * d[None]).sum(2) / dd[None], 0, 1)
            proj = self.A[None] + t[..., None] * d[None]
            dist = np.hypot(*(p - proj).transpose(2, 0, 1))
            j = dist.argmin(1)
            seg[i:i + 1500] = j
            pos[i:i + 1500] = t[np.arange(len(j)), j] * self.L[j]
        for w, s, x in zip(ws, seg, pos):
            w["seg"], w["pos"] = int(s), float(x)
        return ws


def places(ws, S, bin_m=10.0, min_count=30):
    """Clusters of warnings: bins of `bin_m` metres along each segment, adjacent busy bins merged."""
    bins = defaultdict(list)
    for w in ws:
        bins[(w["seg"], int(w["pos"] // bin_m))].append(w)
    busy = sorted(k for k, v in bins.items() if len(v) >= min_count)
    out = []
    used = set()
    for k in busy:
        if k in used:
            continue
        grp = [k]
        used.add(k)
        j = k[1] + 1
        while (k[0], j) in bins and len(bins[(k[0], j)]) >= min_count:
            grp.append((k[0], j))
            used.add((k[0], j))
            j += 1
        members = [w for g in grp for w in bins[g]]
        # Take in the near tail on either side of the core.
        lo, hi = grp[0][1] - 1, grp[-1][1] + 1
        for g in ((k[0], lo), (k[0], hi)):
            if g in bins and g not in used:
                members += bins[g]
                used.add(g)
        n = len(members)
        out.append(dict(seg=k[0], bins=(lo, hi), n=n, passes=float(S.passes[k[0]]),
                        share=n / S.passes[k[0]] if S.passes[k[0]] else float("inf"),
                        nobrake=sum(not w["braked"] for w in members) / n, ids={w["eid"] for w in members},
                        new=bool(S.new[k[0]]), pcw=sum(w["pcw"] for w in members) / n,
                        speed=float(np.median([w["speed"] for w in members]))))
    out.sort(key=lambda p: -p["n"])
    return out


def rates(ws, drop=frozenset()):
    n = defaultdict(int)
    nb = defaultdict(int)
    for w in ws:
        if w["eid"] in drop:
            continue
        n[w["dep"]] += 1
        nb[w["dep"]] += 0 if w["braked"] else 1
    fleet = sum(nb.values()) / sum(n.values())
    res = {}
    for d in DEPOT_ORDER:
        rate = nb[d] / n[d]
        res[d] = dict(n=n[d], nobrake=nb[d], rate=rate, ratio=rate / fleet)
    return res, fleet, sum(n.values()), sum(nb.values())


def taken(res):
    return sorted(d for d, v in res.items() if v["ratio"] >= RATIO)


def false_places(pl, threshold=0.10):
    return [p for p in pl if p["share"] >= threshold]


def call(D=None, threshold=0.10, bin_m=10.0):
    D = D or load()
    ws = collision_warnings(D)
    S = Segments(D)
    S.snap(ws)
    pl = places(ws, S, bin_m=bin_m)
    fp = false_places(pl, threshold)
    drop = set().union(*[p["ids"] for p in fp]) if fp else set()
    res, fleet, n, nb = rates(ws, drop)
    out = dict(res=res, fleet=fleet, n=n, nobrake=nb, taken=taken(res), places=pl, false=fp, ws=ws, S=S)
    below = [(v["ratio"], d) for d, v in res.items() if v["ratio"] < RATIO]
    out["closest"] = max(below)[1] if below else None
    return out


# ------------------------------------------------------------------ ask A: hours on service, October 2026
WEEKS = [dt.date(2026, 10, 5), dt.date(2026, 10, 12), dt.date(2026, 10, 19), dt.date(2026, 10, 26)]
DST_END = dt.datetime(2026, 10, 25, 3, 0, 0)


def hr_depot(D):
    if "hr" not in D:
        rows = _csv("hr", ";")
        h = defaultdict(list)
        for r in rows:
            h[r["empleado"]].append((dmy(r["desde"]), dmy(r["hasta"]) if r["hasta"] else dt.date(2099, 12, 31), r["cochera"]))
        D["hr"] = h
    return D["hr"]


def ask_a(D, dedupe=True, dst=True, overlap=True, service_only=True):
    rows = _csv("etm", ";")
    hr = hr_depot(D)
    seen = set()
    sess = []
    for r in rows:
        key = tuple(r.values())
        if dedupe and key in seen:
            continue
        seen.add(key)
        if service_only and r["linea"] in ("000", "ESC"):
            continue
        on = dt.datetime.strptime(r["inicio_local"], "%Y-%m-%d %H:%M:%S")
        off = dt.datetime.strptime(r["fin_local"], "%Y-%m-%d %H:%M:%S")
        sess.append(dict(emp=r["empleado"], on=on, off=off))
    if overlap:
        by = defaultdict(list)
        for s in sess:
            by[s["emp"]].append(s)
        for lst in by.values():
            lst.sort(key=lambda s: s["on"])
            for a, b in zip(lst, lst[1:]):
                if a["off"] > b["on"]:
                    a["off"] = b["on"]
    out = {d: [0.0] * 4 for d in DEPOT_ORDER}
    for s in sess:
        day = s["on"].date()
        k = None
        for i, w0 in enumerate(WEEKS):
            if w0 <= day <= w0 + dt.timedelta(days=6):
                k = i
        if k is None:
            continue
        dep = None
        for a, b, d in hr[s["emp"]]:
            if a <= day <= b:
                dep = d
        h = (s["off"] - s["on"]).total_seconds() / 3600.0
        if dst and s["on"] < DST_END <= s["off"]:
            h += 1.0
        out[dep][k] += h
    return {d: [int(math.floor(x + 0.5)) for x in v] for d, v in out.items()}, out


# ------------------------------------------------------------------ ask B: at-fault collisions and claims
def ask_b(D, dedupe=True, chains=True, plates_all=True):
    wb = load_workbook(os.path.join(TARGET, F["incidents"]), read_only=True)
    rows = list(wb.active.iter_rows(values_only=True))[1:]
    reports = []
    for parte, fecha, hora, coche, lugar, tipo, culpa, por in rows:
        t = dt.datetime.combine(dmy(fecha), dt.datetime.strptime(hora, "%H:%M").time())
        reports.append(dict(ref=parte, t=t, day=t.date(), fleet=str(coche), fault=culpa, by=por))
    reports.sort(key=lambda x: (x["fleet"], x["t"]))
    incidents = []
    for x in reports:
        if dedupe and incidents and incidents[-1]["fleet"] == x["fleet"] and \
                abs((x["t"] - incidents[-1]["t"]).total_seconds()) <= 20 * 60 and incidents[-1]["fault"] == x["fault"]:
            continue
        incidents.append(dict(x))
    bord = _csv("bordereau")
    last = {}
    for r in bord:
        if r["snapshot"] == "2026-10-31":
            last[r["claim_no"]] = r
    reopened = {r["reopened_from"] for r in last.values() if r["reopened_from"]}
    if plates_all:
        p2f = D["plate_to_fleet"]
    else:
        # Only the plates the fleet carries now.
        wb2 = load_workbook(os.path.join(TARGET, "fleet_register_2026.xlsx"), read_only=True)
        p2f = {}
        for fno, p, a, b in list(wb2["Registrations"].iter_rows(values_only=True))[1:]:
            if not b:
                p2f[p] = str(fno)
    paid_by_inc = defaultdict(float)
    for no, r in last.items():
        if chains and no in reopened:
            continue                # the reopening claim carries this claim's payments forward
        fno = p2f.get(r["vehicle_plate"])
        if fno is None:
            continue
        day = dt.date.fromisoformat(r["incident_date"])
        it = dt.datetime.combine(day, dt.datetime.strptime(r["incident_time_local"], "%H:%M").time())
        cands = [x for x in incidents if x["fleet"] == fno and x["day"] == day]
        if not cands:
            continue
        x = min(cands, key=lambda x: abs((x["t"] - it).total_seconds()))
        paid_by_inc[id(x)] += float(r["paid_to_date_eur"])
    count = {d: 0 for d in DEPOT_ORDER}
    paid = {d: 0.0 for d in DEPOT_ORDER}
    for x in incidents:
        if x["fault"] not in ("A", "C"):
            continue
        dep = depot_on(D, x["fleet"], x["day"])
        count[dep] += 1
        paid[dep] += paid_by_inc.get(id(x), 0.0)
    return count, {d: int(math.floor(v + 0.5)) for d, v in paid.items()}, paid


# ------------------------------------------------------------------ ask C: kilometres in service, July to October
MONTHS = [7, 8, 9, 10]
# The lines each depot operates from 14 December 2025, as the Red 2026 service notice's depot table lists them.
NOTICE_LINES = {"San Lázaro": "1 3 7 9 N1", "Hornacho": "12 14 27 33 N2", "Valdeolmos": "40 41 44 46 N3",
                "El Quiñón": "5 16 21 N4", "Las Tenerías": "2 8 19 23 25 N5", "La Ribera": "4 10 17 29 N6",
                "Santa Clara": "6 11 31 35 N7"}
LINE_DEPOT = {ln: d for d, s in NOTICE_LINES.items() for ln in s.split()}


def ask_c(D, operating=True, metres=True, diversions=True):
    out = {d: [0.0] * 4 for d in DEPOT_ORDER}
    ops = {}
    for r in D["return"]:
        day = dmy(r["fecha"])
        if day.year != 2026 or day.month not in MONTHS:
            continue
        km = float(r["km_realizados"].replace(",", "."))
        if metres and r["linea"] in ("40", "41", "44", "46") and day >= dt.date(2026, 7, 1):
            km /= 1000.0
        dep = LINE_DEPOT[r["linea"]] if operating else r["centro"]
        out[dep][MONTHS.index(day.month)] += km
        ops[(day, r["linea"], r["sentido"])] = (int(r["expediciones_realizadas"]), dep)
    if diversions:
        for r in _csv("diversions", ";"):
            a, b = dmy(r["desde"]), dmy(r["hasta"])
            kmt = float(r["km_por_expedicion"].replace(",", "."))
            d = a
            while d <= b:
                if d.month in MONTHS:
                    for line in r["lineas"].split("/"):
                        for s in r["sentidos"].split("/"):
                            if (d, line, s) in ops:
                                n, dep = ops[(d, line, s)]
                                out[dep][MONTHS.index(d.month)] += n * kmt
                d += dt.timedelta(days=1)
    return {d: [int(math.floor(x + 0.5)) for x in v] for d, v in out.items()}, out


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    c = call()
    print("fleet rate %.4f  taken %s  closest %s" % (c["fleet"], c["taken"], c["closest"]))
    for d, v in c["res"].items():
        print("  %-14s n %6d  not braked %5d  rate %.4f  ratio %.4f" % (d, v["n"], v["nobrake"], v["rate"], v["ratio"]))
    for p in c["places"][:12]:
        print("  place seg %4d n %5d passes %7d share %.4f nobrake %.3f new %s pcw %.2f speed %.1f" %
              (p["seg"], p["n"], p["passes"], p["share"], p["nobrake"], p["new"], p["pcw"], p["speed"]))
