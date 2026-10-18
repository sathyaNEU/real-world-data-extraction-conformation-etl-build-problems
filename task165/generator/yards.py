"""task165 yards: the September 2026 dome survey, the scale houses' weighings from 24 August to 24 September 2026,
the supplier's October dispatch schedules, the yard loading log and the contractor's material returns. The clean
truth for Ask A (each dome's stock on 1 November 2026) and Ask B (each yard's Priority 1 arterial salt) is kept on
the Yards object."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K

CAPACITY = {"KLV": 9200.0, "MPF": 8400.0, "RDG": 10800.0, "LKS": 7600.0}
SURVEY_DAY = {"KLV": dt.date(2026, 9, 8), "MPF": dt.date(2026, 9, 9), "RDG": dt.date(2026, 9, 10),
              "LKS": dt.date(2026, 9, 11)}
# capture windows, local (EDT); the report gives them in UTC
CAPTURE = {"KLV": ((7, 42), (8, 26)), "MPF": ((7, 35), (8, 14)), "RDG": ((7, 51), (8, 47)), "LKS": ((7, 38), (8, 19))}
SURVEY_STOCK = {"KLV": 4980.4, "MPF": 4212.7, "RDG": 6051.3, "LKS": 2744.8}
BULK_DENSITY = 1.20
LKS_SCALE_OUT = (dt.date(2026, 8, 24), dt.date(2026, 9, 14))   # Lakeshore's scale replaced: loads weighed at Ridge
MPF_SCALE_OUT = (dt.date(2026, 9, 14), dt.date(2026, 9, 18))   # Mapleford's scale recertified: loads weighed at Kelvin Road
LOG_START, LOG_END = dt.date(2026, 8, 24), dt.date(2026, 9, 24)
TRANSFER_DAYS = [dt.date(2026, 9, 16), dt.date(2026, 9, 17), dt.date(2026, 9, 18)]
HAULER = "Northgrit Transport"
PLATES_B = ["AV%d %s" % (4100 + i, x) for i, x in enumerate(["KRT", "LMN", "PQD", "RSW", "BTY", "CDF", "HJK", "WXZ",
                                                               "GHA", "NMB", "TRV", "ELP"])]
PLATES_T = ["AZ%d %s" % (7300 + i, x) for i, x in enumerate(["DRF", "GTN", "MLK", "PSV", "QWE", "RBC"])]


def _hm(d, h, m):
    return dt.datetime.combine(d, dt.time(h, m))


class Yards:
    def __init__(self, W, S):
        self.W, self.S = W, S
        self.rng = np.random.default_rng(W.seed + 40)
        self.scale = {y: [] for y in K.YARDS}     # sheet rows per scale house
        self.dispatch = {1: [], 2: []}
        self._scale_log()
        self._dispatch()
        self._stock_truth()

    # ------------------------------------------------------------------------------------------- scale houses
    def _scale_log(self):
        rng = self.rng
        tick = {y: 41000 + 1500 * i for i, y in enumerate(K.YARDS)}
        sup_tick = 2260411
        self.loads = []   # (yard_to, weighed_at, time_in, time_out, direction, net_t, kind, remark)
        d = LOG_START
        while d <= LOG_END:
            if d.weekday() < 5 and d != dt.date(2026, 9, 7):        # Labour Day
                for y in K.YARDS:
                    n = int(rng.integers(1, 4))
                    times = sorted(rng.uniform(6.4, 16.2, n))
                    if d == SURVEY_DAY[y]:
                        # the yard holds deliveries during the drone flight
                        (h0, m0), (h1, m1) = CAPTURE[y]
                        a, b = h0 + m0 / 60 - 0.25, h1 + m1 / 60 + 0.2
                        times = sorted([6.62 + 0.21 * (K.YARDS.index(y) % 2)] +
                                       [t for t in times if t < a or t > b] + [b + 0.55, 13.1 + 0.4 * K.YARDS.index(y)])
                    for t in times:
                        btrain = rng.random() < 0.72
                        net = float(rng.normal(43.2, 1.1) if btrain else rng.normal(29.4, 0.8))
                        tin = dt.datetime.combine(d, dt.time(0, 0)) + dt.timedelta(hours=float(t))
                        tin = tin.replace(second=0, microsecond=0)
                        tout = tin + dt.timedelta(minutes=int(rng.integers(14, 31)))
                        at = y
                        remark = ""
                        if y == "LKS" and LKS_SCALE_OUT[0] <= d <= LKS_SCALE_OUT[1]:
                            at = "RDG"
                            remark = ["LKS", "to LKS", "for Lakeshore", "LKS dome"][int(rng.integers(0, 4))]
                            tout = tin + dt.timedelta(minutes=int(rng.integers(6, 10)))
                        if y == "MPF" and MPF_SCALE_OUT[0] <= d <= MPF_SCALE_OUT[1]:
                            at = "KLV"
                            remark = ["MPF", "for Mapleford", "to MPF", "Mapleford dome"][int(rng.integers(0, 4))]
                            tout = tin + dt.timedelta(minutes=int(rng.integers(6, 10)))
                        sup_tick += int(rng.integers(1, 9))
                        self.loads.append({"to": y, "at": at, "in": tin, "out": tout, "dir": "IN", "net": round(net, 2),
                                           "kind": "SUPPLIER", "remark": remark, "btrain": btrain,
                                           "sup": "NG%07d" % sup_tick})
            d += dt.timedelta(days=1)
        # one wet load turned back at Mapleford: weighed in, inspected, weighed out still loaded
        rej_day = dt.date(2026, 9, 21)
        tin = _hm(rej_day, 10, 6)
        self.loads.append({"to": "MPF", "at": "MPF", "in": tin, "out": tin + dt.timedelta(minutes=41), "dir": "IN",
                           "net": 42.78, "kind": "SUPPLIER", "remark": "", "btrain": True, "sup": "NG2269874"})
        self.loads.append({"to": "MPF", "at": "MPF", "in": tin + dt.timedelta(minutes=41),
                           "out": tin + dt.timedelta(minutes=43), "dir": "OUT", "net": 42.78, "kind": "RETURN",
                           "remark": "returned to Northgrit, wet", "btrain": True, "sup": "NG2269874"})
        # Ridge to Lakeshore on city tandems, filling the rebuilt dome
        for d in TRANSFER_DAYS:
            for j in range(int(rng.integers(3, 5))):
                tout_r = _hm(d, 8 + 2 * j, int(rng.integers(0, 50)))
                net = round(float(rng.normal(18.6, 0.6)), 2)
                self.loads.append({"to": "LKS", "from": "RDG", "at": "RDG", "in": tout_r - dt.timedelta(minutes=9),
                                   "out": tout_r, "dir": "OUT", "net": net, "kind": "TRANSFER", "remark": "",
                                   "btrain": False, "sup": ""})
                tin_l = tout_r + dt.timedelta(minutes=int(rng.integers(38, 55)))
                net_l = round(net + float(rng.normal(0, 0.04)), 2)
                self.loads.append({"to": "LKS", "from": "RDG", "at": "LKS", "in": tin_l,
                                   "out": tin_l + dt.timedelta(minutes=7), "dir": "IN", "net": net_l,
                                   "kind": "TRANSFER", "remark": "", "btrain": False, "sup": ""})
        self.loads.sort(key=lambda r: (r["at"], r["in"]))
        # the transfers ran on one of Ridge's own tandems
        xfer_unit = sorted(u["unit_id"] for u in self.W.units if u["yard"] == "RDG" and u["class"] == "TANDEM"
                           and u["home_circuit"] not in self.W.contract_circuits)[1]
        for r in self.loads:
            tick[r["at"]] += 1
            r["ticket"] = "%s-%06d" % (r["at"], tick[r["at"]])
            if r["kind"] == "TRANSFER":
                r["carrier"], r["vehicle"] = "CITY OF QUELLBROOK", "Unit %s" % xfer_unit
            elif r["kind"] == "RETURN":
                r["carrier"], r["vehicle"] = HAULER, PLATES_B[3]
            else:
                r["carrier"] = HAULER
                r["vehicle"] = PLATES_B[int(rng.integers(0, len(PLATES_B)))] if r["btrain"] else \
                    PLATES_T[int(rng.integers(0, len(PLATES_T)))]
            tare = (float(rng.normal(17800, 260)) if r["btrain"] else float(rng.normal(13400, 210)))
            if r["kind"] == "TRANSFER":
                tare = float(rng.normal(15850, 120))
            r["tare_kg"] = int(round(tare / 20.0)) * 20
            r["gross_kg"] = r["tare_kg"] + int(round(r["net"] * 1000 / 20.0)) * 20
            r["net_kg"] = r["gross_kg"] - r["tare_kg"]

    # ------------------------------------------------------------------------------------------- dispatch
    def _dispatch(self):
        rng = np.random.default_rng(self.W.seed + 41)
        book = []
        d = dt.date(2026, 10, 1)
        ref = 88100
        while d <= dt.date(2026, 10, 30):
            if d.weekday() < 5 and d != dt.date(2026, 10, 12):      # Thanksgiving Monday
                for y in K.YARDS:
                    n = int(rng.integers(1, 4)) + (1 if y == "LKS" else 0)
                    for j in range(n):
                        ref += 1
                        bt = rng.random() < 0.7
                        book.append({"date": d, "yard": y, "trailer": "B-TRAIN" if bt else "TRI-AXLE",
                                     "planned_t": 43.0 if bt else 30.0, "ref": "BK%06d" % ref, "status": "BOOKED"})
            d += dt.timedelta(days=1)
        self.dispatch[1] = [dict(b) for b in book]
        rev = [dict(b) for b in book]
        # the 21 September issue: two loads cancelled, three moved into November, one added at Ridge
        idx = rng.choice(len(rev), 5, replace=False)
        for k, i in enumerate(sorted(idx)):
            if k < 2:
                rev[i]["status"] = "CANCELLED"
            else:
                rev[i]["date"] = dt.date(2026, 11, 2 + k)
                rev[i]["status"] = "BOOKED"
        ref += 1
        rev.append({"date": dt.date(2026, 10, 28), "yard": "RDG", "trailer": "B-TRAIN", "planned_t": 43.0,
                    "ref": "BK%06d" % ref, "status": "BOOKED"})
        rev.sort(key=lambda b: (b["date"], b["yard"], b["ref"]))
        self.dispatch[2] = rev

    # ------------------------------------------------------------------------------------------- truth
    def capture_end(self, y):
        (h1, m1) = CAPTURE[y][1]
        return _hm(SURVEY_DAY[y], h1, m1)

    def _stock_truth(self):
        self.stock = {}
        for y in K.YARDS:
            v = SURVEY_STOCK[y]
            cut = self.capture_end(y)
            for r in self.loads:
                if r["in"] <= cut:
                    continue
                if r["dir"] == "IN" and r["to"] == y and r["kind"] in ("SUPPLIER", "TRANSFER"):
                    v += r["net_kg"] / 1000.0
                if r["dir"] == "OUT" and r["kind"] == "RETURN" and r["to"] == y:
                    v -= r["net_kg"] / 1000.0
                if r["dir"] == "OUT" and r["kind"] == "TRANSFER" and r.get("from") == y:
                    v -= r["net_kg"] / 1000.0
            for b in self.dispatch[2]:
                if b["yard"] == y and b["status"] == "BOOKED" and b["date"] <= dt.date(2026, 10, 31):
                    v += b["planned_t"]
            self.stock[y] = v
        self.room = {y: CAPACITY[y] - self.stock[y] for y in K.YARDS}

    # ------------------------------------------------------------------------------------------- exports
    def scale_sheet(self, y):
        rows = []
        for r in self.loads:
            if r["at"] != y:
                continue
            rows.append((r["ticket"], r["in"].date(), r["in"].strftime("%H:%M"), r["out"].strftime("%H:%M"), r["dir"],
                         r["carrier"], r["vehicle"], r["sup"], "ROCK SALT", r["gross_kg"], r["tare_kg"], r["net_kg"],
                         r["remark"]))
        return rows

    def dispatch_rows(self, issue):
        return [(b["date"].isoformat(), "QB-%s" % b["yard"], b["trailer"], "%.1f" % b["planned_t"], b["ref"],
                 b["status"]) for b in self.dispatch[issue]]


# ---------------------------------------------------------------------------------------------- Ask B records
def loading_log(W, S, rng):
    """Salt loaded into each truck each shift at its yard (loader scale), 2023-24 to 2025-26; trucks carry what is
    left in the hopper into the next shift."""
    per = {}
    for p in S.passes:
        if p["winter"] not in K.NEW_WINTERS or p["contract"] or not p["rows"]:
            continue
        t = p["rows"][0]["entry"]
        if 7 <= t.hour < 19:
            sd, sh = t.date(), "DAY"
        else:
            sd = t.date() if t.hour >= 19 else t.date() - dt.timedelta(days=1)
            sh = "NIGHT"
        key = (p["unit"], sd, sh)
        per[key] = per.get(key, 0.0) + sum(r["t"] for r in p["rows"])
    rows = []
    carry = {}
    for (unit, sd, sh) in sorted(per, key=lambda k: (k[1], 0 if k[2] == "DAY" else 1, k[0])):
        spread = per[(unit, sd, sh)]
        c_in = carry.get(unit, 0.0)
        c_out = float(rng.uniform(0.2, 1.4))
        loaded = max(0.0, spread + c_out - c_in)
        carry[unit] = c_out
        u = W.unit_by_id[unit]
        yard = u["yard"]
        cap = 12.0 if u["class"] == "TANDEM" else 7.5
        loads = max(1, int(np.ceil(loaded / cap)))
        rows.append((yard, sd.isoformat(), sh, unit, loads, "%.1f" % loaded))
    return rows


def contractor_returns(W, S):
    """Kettlewood Road Services' monthly material returns for the contract circuits, from its own trucks' controllers."""
    out = {}
    for p in S.passes:
        if not p["contract"] or p["winter"] not in K.NEW_WINTERS:
            continue
        for r in p["rows"]:
            m = r["entry"].strftime("%Y-%m")
            key = (p["winter"], m, p["route_code"])
            out[key] = out.get(key, 0.0) + r["t"]
    return out
