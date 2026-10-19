"""task165 yards: the September 2026 dome survey, the scale houses' weighings from 24 August to 24 September 2026,
the supplier's October dispatch schedules, the contractor's material returns and Fleet Services' work orders (with the
yard loading log, which the settling of the arterial cells reads and the pack does not carry). The clean truth for Ask
A (each dome's stock on 1 November 2026) and Ask B (each yard's Priority 1 arterial salt) is kept on the Yards object."""
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
# the first B-trains after each scale came back, still weighed on the way at the scale house that had been weighing
# for that yard: (receiving yard, day, which of that day's B-trains at its own scale, the scale house weighed at, the
# operator's remark, kg by which that scale house's own stored tare for the truck sits from the receiving yard's).
# Where the operator kept the outage remark the ticket went on the receiving yard's account and its stored tare, as
# the outage weighings had; where not, on the scale house's own account and its own stored tare for the truck
CHANGEOVER = [("LKS", dt.date(2026, 9, 15), 0, "RDG", "for Lakeshore", 0),
              ("LKS", dt.date(2026, 9, 16), 0, "RDG", "LKS", 0),
              ("LKS", dt.date(2026, 9, 16), 1, "RDG", "", -260),
              ("MPF", dt.date(2026, 9, 21), 0, "KLV", "MPF", 0),
              ("MPF", dt.date(2026, 9, 21), 1, "KLV", "", -240)]
TRAVEL = {"RDG": (38, 50), "KLV": (27, 36)}   # minutes from that scale house to the receiving yard's
# Northgrit's terminal to each yard's scale house, minutes, and its loadout: a truck reaches a City scale no sooner
# than its drive back from the yard it last tipped at, the loadout and the drive out
TERMINAL_MIN = {"KLV": 48, "MPF": 70, "RDG": 52, "LKS": 84}
LOADOUT_MIN = 25
TIP_MIN = 15                                  # tipping at a yard whose own scale was out
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
        # the transfers ran on one of Ridge's own tandems; the supplier trucks, their stored tares and the dockets set
        # here are provisional until assign_trucks, which keeps every net
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
        # the wet load leaves on the truck that brought it, weighed out still loaded on its stored tare
        for r in self.loads:
            if r["kind"] == "RETURN":
                d_ = next(x for x in self.loads if x["kind"] == "SUPPLIER" and x["sup"] == r["sup"])
                r["vehicle"], r["tare_kg"], r["gross_kg"], r["net_kg"] = \
                    d_["vehicle"], d_["tare_kg"], d_["gross_kg"], d_["net_kg"]

    def add_changeover_weighings(self):
        """The first B-trains bound for Lakeshore after its new scale came into use (15 September) and for Mapleford
        after its scale was back from recertification (21 September) still weighed at Ridge and Kelvin Road on the
        way, as the outage routing had them do: a gross on the stored tare, no tipping, and the operator's remark kept
        on some. Each B-train carries a docket per trailer, and the two scale houses keyed one each. The truck tipped
        at its own yard, so the earlier weighing is no load in to either dome; it is built after the dome edges are
        settled so that it carries the gross the receiving yard's scale printed, on the stored tare of the account the
        ticket went to (assign_trucks)."""
        dockets = {r["sup"] for r in self.loads if r["sup"]}
        added = []
        for to, day, k, at, remark, tare_off in CHANGEOVER:
            own = sorted((r for r in self.loads if r["to"] == to and r["at"] == to and r["dir"] == "IN"
                          and r["kind"] == "SUPPLIER" and r["btrain"] and r["in"].date() == day
                          and not any(x["kind"] == "RETURN" and x["sup"] == r["sup"] for x in self.loads)),
                         key=lambda r: r["in"])
            o = own[k]
            lo, hi = TRAVEL[at]
            travel = lo + K.stable_int(o["sup"], "travel") % (hi - lo + 1)
            dwell = 6 + K.stable_int(o["sup"], "dwell") % 4
            n = int(o["sup"][2:])
            sup = "NG%07d" % (n + 1) if "NG%07d" % (n + 1) not in dockets else "NG%07d" % (n - 1)
            assert sup not in dockets
            dockets.add(sup)
            tin = o["in"] - dt.timedelta(minutes=travel + dwell)
            added.append({"to": to, "at": at, "in": tin, "out": tin + dt.timedelta(minutes=dwell), "dir": "IN",
                          "net": o["net"], "kind": "SUPPLIER", "remark": remark, "btrain": True, "sup": sup,
                          "carrier": o["carrier"], "vehicle": o["vehicle"], "tare_kg": o["tare_kg"] + tare_off,
                          "gross_kg": o["gross_kg"], "net_kg": o["net_kg"] - tare_off, "copy": True,
                          "orig_sup": o["sup"], "account": to if tare_off == 0 else at, "tare_off": tare_off})
        self.loads.extend(added)
        self.loads.sort(key=lambda r: (r["at"], r["in"]))
        tick = {y: 41000 + 1500 * i for i, y in enumerate(K.YARDS)}
        for r in self.loads:
            tick[r["at"]] += 1
            r["ticket"] = "%s-%06d" % (r["at"], tick[r["at"]])
        self._stock_truth()

    def assign_trucks(self):
        """Northgrit runs twelve B-trains and six tri-axles from its terminal, so a truck reaches a City scale no sooner
        than its drive back from the yard it last tipped at, the loadout and the drive out. Each scale house weighs a
        truck on the tare it stores for that truck on the account the ticket goes to (the outage weighings on the
        receiving yard's), and the terminal numbers its dockets in loadout order, one to a tri-axle and one to each
        trailer of a B-train, the lead trailer's keyed at the yard. Built after the changeover weighings, so that each
        truck's day holds them; no net moves."""
        rng = np.random.default_rng(self.W.seed + 43)
        before = {id(r): r["net_kg"] for r in self.loads if not r.get("copy")}
        trips = {}
        for r in self.loads:
            if r["kind"] in ("SUPPLIER", "RETURN"):
                trips.setdefault(r.get("orig_sup", r["sup"]), []).append(r)
        days = {}
        for key, rows in sorted(trips.items()):
            rows.sort(key=lambda r: (r["in"], r["dir"]))
            first, last = rows[0], max(rows, key=lambda r: r["out"])
            end = last["out"]
            if last["at"] != last["to"]:
                lo, hi = TRAVEL[last["at"]]
                end += dt.timedelta(minutes=(lo + hi) // 2 + TIP_MIN)
            days.setdefault(first["in"].date(), []).append(
                {"key": key, "rows": rows, "start": first["in"], "start_at": first["at"], "end": end,
                 "end_at": last["to"], "btrain": first["btrain"]})
        for d in sorted(days):
            free = {}
            for t in sorted(days[d], key=lambda t: (t["start"], t["key"])):
                pool = PLATES_B if t["btrain"] else PLATES_T
                ok = [v for v in pool if v not in free or free[v][0] + dt.timedelta(
                    minutes=TERMINAL_MIN[free[v][1]] + LOADOUT_MIN + TERMINAL_MIN[t["start_at"]]) <= t["start"]]
                assert ok, (d, t["start"])
                v = ok[int(rng.integers(0, len(ok)))]
                free[v] = (t["end"], t["end_at"])
                for r in t["rows"]:
                    r["vehicle"] = v
        # each scale house's stored tares: the truck's empty weight as that scale last tared it
        base = {v: float(rng.normal(17800, 170)) for v in PLATES_B}
        base.update({v: float(rng.normal(13400, 140)) for v in PLATES_T})
        table = {y: {v: int(round((base[v] + float(rng.normal(0, 110))) / 20.0)) * 20 for v in sorted(base)}
                 for y in K.YARDS}
        for r in self.loads:
            if r.get("copy") and r["account"] == r["at"]:
                table[r["at"]][r["vehicle"]] = table[r["to"]][r["vehicle"]] + r["tare_off"]
        unit_base = float(rng.normal(15850, 60))
        unit_tare = {y: int(round((unit_base + float(rng.normal(0, 40))) / 20.0)) * 20 for y in K.YARDS}
        for r in self.loads:
            if r["kind"] == "TRANSFER":
                r["tare_kg"] = unit_tare[r["at"]]
                r["gross_kg"] = r["tare_kg"] + r["net_kg"]
            elif r["kind"] == "SUPPLIER" and not r.get("copy"):
                r["tare_kg"] = table[r["to"]][r["vehicle"]]
                r["gross_kg"] = r["tare_kg"] + r["net_kg"]
        for r in self.loads:
            if r["kind"] == "RETURN" or r.get("copy"):
                o = next(x for x in trips[r.get("orig_sup", r["sup"])]
                         if x["kind"] == "SUPPLIER" and not x.get("copy"))
                r["gross_kg"] = o["gross_kg"]
                r["tare_kg"] = o["tare_kg"] if r["kind"] == "RETURN" else table[r["account"]][r["vehicle"]]
                r["net_kg"] = r["gross_kg"] - r["tare_kg"]
        # dockets in loadout order
        n = 2260411
        order = sorted((t for d in days for t in days[d]),
                       key=lambda t: (t["start"] - dt.timedelta(minutes=TERMINAL_MIN[t["start_at"]]), t["key"]))
        for t in order:
            n += 1 + int(rng.integers(0, 6))
            lead = n
            if t["btrain"]:
                n += 1
            for r in t["rows"]:
                r["sup"] = "NG%07d" % (lead + 1 if r.get("copy") else lead)
        assert all(r["net_kg"] == before[id(r)] for r in self.loads if not r.get("copy"))
        stock = dict(self.stock)
        self._stock_truth()
        assert self.stock == stock

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
                if r["in"] <= cut or r.get("copy"):
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
    for p in list(S.passes) + list(S.patrols):
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


# ---------------------------------------------------------------------------------------------- Fleet Services
WO_START, WO_END = dt.date(2023, 7, 1), dt.date(2026, 9, 23)
# (system, the work as technicians sign it off, labour hours range, parts dollars range); a tandem's list adds the wing
# and the pre-wet
WO_REPAIRS = [
    ("PLOW", ["Plow cutting edge replaced", "Plow cutting edge replaced, centre section", "Cutting edge worn, replaced"],
     (1.5, 3.0), (180, 420)),
    ("PLOW", ["Plow trip springs replaced", "Trip spring broken, replaced both"], (1.0, 2.5), (90, 210)),
    ("PLOW", ["Plow shoes and mouldboard bolts replaced", "Plow shoe replaced, left"], (1.0, 2.0), (40, 120)),
    ("SPREADER", ["Spinner motor replaced", "Spinner motor seized, replaced"], (1.5, 3.0), (380, 720)),
    ("SPREADER", ["Conveyor chain adjusted, two links replaced", "Conveyor chain tensioned", "Conveyor chain jammed, "
                  "cleared and adjusted"], (1.0, 2.5), (40, 160)),
    ("SPREADER", ["Spinner disc replaced", "Spinner disc cracked, replaced"], (0.75, 1.5), (120, 260)),
    ("SPREADER", ["Spreader controller display fault, reset and reflashed", "Controller screen blank, reseated "
                  "connector"], (0.5, 1.5), (0, 0)),
    ("SPREADER", ["Ground speed sensor replaced", "No ground speed to controller, sensor replaced"], (0.5, 1.5),
     (90, 210)),
    ("HYDRAULIC", ["Hydraulic hose replaced at the valve bank", "Hose burst at the valve bank, replaced",
                   "Hydraulic hose to the box replaced"], (1.0, 2.5), (60, 240)),
    ("HYDRAULIC", ["Hydraulic oil leak at the pump, resealed", "Pump shaft seal leaking, replaced"], (1.5, 3.5),
     (40, 180)),
    ("BRAKES", ["Brake chamber replaced, axle 2 right", "Brake chamber replaced, axle 1 left", "Brake chamber replaced"],
     (1.0, 2.0), (90, 260)),
    ("BRAKES", ["Slack adjusters adjusted, brake lines checked", "Brakes out of adjustment, adjusted"], (0.5, 1.5),
     (0, 40)),
    ("ELECTRICAL", ["Strobe and work lights repaired", "Rear strobe out, replaced", "Work light wiring repaired"],
     (0.5, 2.0), (20, 160)),
    ("ELECTRICAL", ["Batteries replaced", "No start, batteries replaced"], (0.5, 1.0), (260, 420)),
    ("ENGINE", ["DEF sensor replaced", "Check engine light, DEF sensor replaced"], (1.0, 2.5), (150, 480)),
    ("ENGINE", ["Coolant hose replaced", "Coolant leak at the lower hose, replaced"], (1.0, 2.0), (40, 120)),
    ("TIRES", ["Tire replaced, left steer", "Tire replaced, right drive", "Flat, tire replaced"], (0.5, 1.0), (380, 640)),
]
WO_TANDEM = [
    ("PLOW", ["Wing plow hydraulic cylinder resealed", "Wing cylinder leaking, resealed"], (2.0, 4.5), (60, 240)),
    ("PLOW", ["Wing plow cutting edge replaced"], (1.0, 2.5), (140, 320)),
    ("SPREADER", ["Pre-wet pump seal replaced", "Pre-wet pump leaking at the seal, replaced"], (1.0, 2.0), (60, 150)),
    ("SPREADER", ["Pre-wet nozzles and line cleared of salt", "Pre-wet line plugged, cleared"], (0.5, 1.5), (0, 30)),
    ("SPREADER", ["Pre-wet tank strainer cleaned, sight gauge replaced"], (0.5, 1.0), (20, 70)),
]
WO_SUMMER = [
    ("BODY", ["Dump body floor patched and painted", "Box floor rusted through, patched"], (4.0, 9.0), (180, 520)),
    ("BODY", ["Hopper rust repair and paint", "Hopper sides patched and painted"], (3.0, 7.0), (120, 380)),
    ("HYDRAULIC", ["Hoist cylinder rebuilt"], (3.0, 6.0), (320, 780)),
    ("ENGINE", ["DPF cleaned", "DPF regen fault, filter cleaned"], (2.0, 4.0), (380, 900)),
]
WO_INSPECTION = ["Annual safety inspection, passed", "Annual safety inspection, passed", "Annual safety inspection, "
                 "passed", "Annual safety inspection, passed after brake adjustment", "Annual safety inspection, "
                 "passed after lamp replaced"]


def _holidays(y):
    """Ontario statutory holidays and the civic holiday, when the City's garage is closed."""
    def nth(month, wd, n):
        d = dt.date(y, month, 1)
        while d.weekday() != wd:
            d += dt.timedelta(days=1)
        return d + dt.timedelta(days=7 * (n - 1))
    a = y % 19
    b, c = divmod(y, 100)
    dd, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - dd - g + 15) % 30
    i, k = divmod(c, 4)
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    month = (h + l_ - 7 * m + 114) // 31
    day = ((h + l_ - 7 * m + 114) % 31) + 1
    easter = dt.date(y, month, day)
    victoria = dt.date(y, 5, 24)
    while victoria.weekday() != 0:
        victoria -= dt.timedelta(days=1)
    return {dt.date(y, 1, 1), nth(2, 0, 3), easter - dt.timedelta(days=2), victoria, dt.date(y, 7, 1),
            nth(8, 0, 1), nth(9, 0, 1), nth(10, 0, 2), dt.date(y, 12, 25), dt.date(y, 12, 26)}


def work_orders(W, S):
    """Fleet Services' work orders on the City's winter units, 1 July 2023 to 23 September 2026: each autumn's
    pre-season service and spreader calibration, each spring's post-season service, the annual safety inspection, the
    repairs between, and the four spreader controllers replaced in the summer of 2025. The garage works weekdays, and
    no unit is booked in on a day it spread or patrolled."""
    rng = np.random.default_rng(W.seed + 52)
    busy = {}
    for p in list(S.passes) + list(S.patrols):
        if p["contract"]:
            continue
        for r in p["rows"]:
            busy.setdefault(p["unit"], set()).add(r["entry"].date())
            busy[p["unit"]].add(r["exit"].date())
    hol = set()
    for y in range(2023, 2027):
        hol |= _holidays(y)

    def open_days(unit, a, b, span=1):
        out = []
        d = a
        while d <= b:
            ds = [d + dt.timedelta(days=j) for j in range(span)]
            if all(x.weekday() < 5 and x not in hol and x not in busy.get(unit, ()) and x <= WO_END for x in ds):
                out.append(d)
            d += dt.timedelta(days=1)
        return out

    def pick(unit, a, b, span=1):
        days = open_days(unit, a, b, span)
        return days[int(rng.integers(0, len(days)))]

    def cost(lo_hi):
        lo, hi = lo_hi
        return 0.0 if hi == 0 else round(float(rng.uniform(lo, hi)), 2)

    def hours(lo_hi):
        return round(float(rng.uniform(*lo_hi)) * 4) / 4

    out = []
    units = sorted((u for u in W.units if u["home_circuit"] not in W.contract_circuits), key=lambda u: u["unit_id"])
    for u in units:
        uid, tandem = u["unit_id"], u["class"] == "TANDEM"
        repairs = WO_REPAIRS + (WO_TANDEM if tandem else [])

        def cal():
            return "Pre-season spreader calibration: granular by catch test at three settings, within %.1f per cent%s" \
                % (float(rng.uniform(0.3, 4.6)), "; pre-wet checked at 40 L/t" if tandem else "")
        for y in (2023, 2024, 2025, 2026):
            a, b = (dt.date(y, 10, 2), dt.date(y, 10, 30)) if y < 2026 else (dt.date(2026, 9, 8), dt.date(2026, 9, 23))
            if y == 2026 and K.stable_int(uid, "pre2026") % 5 > 1:
                continue
            d = pick(uid, a, b)
            out.append((uid, d, d, "PM", "Pre-season service: fluids and filters, lights, plow and spreader mounted",
                        hours((2.5, 4.5)), cost((90, 260))))
            d2 = pick(uid, d, d + dt.timedelta(days=9))
            out.append((uid, d2, d2, "SPREADER", cal(), hours((1.0, 2.0)), 0.0))
        for y in (2024, 2025, 2026):
            d = pick(uid, dt.date(y, 4, 6), dt.date(y, 4, 30))
            out.append((uid, d, d, "PM", "Post-season service: plow and spreader off, washed, inspected and stored",
                        hours((2.0, 4.0)), cost((40, 180))))
        for y in (2023, 2024, 2025, 2026):
            a = dt.date(y, 7, 4) if y == 2023 else dt.date(y, 6, 1)
            d = pick(uid, a, dt.date(y, 8, 28))
            out.append((uid, d, d, "INSPECTION", WO_INSPECTION[int(rng.integers(0, len(WO_INSPECTION)))],
                        hours((1.5, 3.0)), cost((0, 140)) if rng.random() < 0.6 else 0.0))
            if rng.random() < 0.25:
                s_, descs, hr, pc = WO_SUMMER[int(rng.integers(0, len(WO_SUMMER)))]
                span = 2 if hr[1] > 6 else 1
                d = pick(uid, a, dt.date(y, 8, 28), span)
                out.append((uid, d, d + dt.timedelta(days=span - 1), s_, descs[int(rng.integers(0, len(descs)))],
                            hours(hr), cost(pc)))
        for w in K.NEW_WINTERS:
            a, b = K.SEASON[w]
            for _ in range(int(rng.poisson(1.7 if tandem else 1.4))):
                s_, descs, hr, pc = repairs[int(rng.integers(0, len(repairs)))]
                d = pick(uid, a, b)
                out.append((uid, d, d, s_, descs[int(rng.integers(0, len(descs)))], hours(hr), cost(pc)))
        if u["controller"] == "M410" and u["retrofit"] is not None:
            closed = u["retrofit"] - dt.timedelta(days=1)
            while closed.weekday() >= 5 or closed in hol:
                closed -= dt.timedelta(days=1)
            opened = closed - dt.timedelta(days=1)
            while opened.weekday() >= 5 or opened in hol:
                opened -= dt.timedelta(days=1)
            out.append((uid, opened, closed, "SPREADER",
                        "Spreader controller replaced, M410 to M720 (M410 out of support); harness adapted, spreader "
                        "recalibrated, pre-wet checked at 40 L/t", hours((5.5, 7.5)), cost((2900, 3400))))
    out.sort(key=lambda r: (r[1], r[0], r[3], r[4]))
    rows, n = [], 418230
    for uid, opened, closed, system, desc, hr, pc in out:
        n += int(rng.integers(3, 26))
        rows.append(("WO-%06d" % n, uid, opened.isoformat(), closed.isoformat(), system, desc, "%.2f" % hr,
                     "%.2f" % pc))
    return rows
