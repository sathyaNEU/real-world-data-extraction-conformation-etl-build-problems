"""The Water Order Procedure's arithmetic and every rung of the ladder, on inputs read from the pack (load) or handed
over from the simulation. Vectorised over fields with numpy; the verifier recomputes the same figures on its own
code path."""
from __future__ import annotations

import csv
import datetime as dt
import os

import numpy as np

import common as K


class Model:
    """The 2027 fields as the procedure sees them, the District's weather record and the procedure's tables."""

    def __init__(self, fields, wx, tables, last_delivery=None, turnout_last=None, cancelled_last=None):
        self.fields = fields
        self.ids = [f["id"] for f in fields]
        self.n = len(fields)
        self.wx = wx
        self.T = tables
        lat_index = {l: i for i, l in enumerate(K.LATERALS)}
        self.lat = np.array([lat_index[f["lateral"]] for f in fields])
        self.acres = np.array([f["acres"] for f in fields], dtype=float)
        self.kc = np.array([tables["kc"][f["crop"]] for f in fields], dtype=float)          # n x 12
        depth = []
        for f in fields:
            lim = tables["soils"][f["soil"]][1]
            root = tables["root"][f["crop"]]
            depth.append(root if lim is None else min(root, lim))
        self.taw = np.array([tables["soils"][f["soil"]][0] * d for f, d in zip(fields, depth)], dtype=float)
        self.raw = np.array([tables["mad"][f["crop"]] for f in fields], dtype=float) * self.taw
        self.ea = np.array([tables["ea"][f["method"]] for f in fields], dtype=float)
        self.loss = np.array([tables["loss"][l] for l in K.LATERALS], dtype=float)
        self.main = tables["main_loss"]
        self.last_delivery = last_delivery
        self.turnout_last = turnout_last
        self.cancelled_last = cancelled_last

    # -------------------------------------------------------------------------------------------- the daily balance
    def day(self, D, d, cap=True):
        e, r = self.wx[d]
        D = D + self.kc[:, d.month - 1] * e - r
        D = np.maximum(D, 0.0)
        return np.minimum(D, self.taw) if cap else D

    def carry(self, anchors, upto=dt.date(2027, 1, 31), cap=True):
        """Each field's depletion at the end of `upto`, from zero at the end of its anchor day (an irrigation)."""
        D = np.zeros(self.n)
        a_ord = np.array([a.toordinal() for a in anchors])
        for d in K.daterange(min(anchors) + dt.timedelta(days=1), upto):
            nd = self.day(D, d, cap)
            D = np.where(d.toordinal() > a_ord, nd, D)
        return D

    def replay(self, year, D0, monthly=False, drop_leap=False):
        """WOP 2.4, 3.1 to 3.5: the 2027 fields under year's 1 February to 31 October weather from depletion D0.
        Returns the headgate requirement (AF) and, if asked, by month (February to October)."""
        D = D0.copy()
        mon = np.zeros((9, self.n))
        for d in K.season_days(year):
            if drop_leap and d.month == 2 and d.day == 29:
                continue
            D = self.day(D, d)
            irr = D >= self.raw
            mon[d.month - 2] += np.where(irr, D, 0.0)
            D = np.where(irr, 0.0, D)
        farm_m = mon / self.ea * self.acres / 12.0                      # AF at the turnouts, 9 x n
        by_lat = np.zeros((9, 9))
        for k in range(9):
            by_lat[k] = np.bincount(self.lat, weights=farm_m[k], minlength=9)
        head_m = (by_lat / (1 - self.loss)).sum(axis=1) / (1 - self.main)
        if monthly:
            return float(head_m.sum()), head_m
        return float(head_m.sum())

    def thirty(self, start, drop_leap=False):
        """start(year) -> D0. The thirty replays' requirements and monthly requirements."""
        req, mon = {}, {}
        for y in K.REPLAY_YEARS:
            tot, m = self.replay(y, start(y), monthly=True, drop_leap=drop_leap)
            req[y], mon[y] = tot, m
        return req, mon

    # -------------------------------------------------------------------------------------------- starts (rungs)
    def start_full(self):
        z = np.zeros(self.n)
        return lambda y: z

    def start_golden(self):
        D = self.carry([self.last_delivery[i] for i in self.ids])
        self.D_golden = D
        return lambda y: D

    def start_turnout(self):
        D = self.carry([self.turnout_last[i] for i in self.ids])
        return lambda y: D

    def start_cancelled(self):
        D = self.carry([max(self.last_delivery[i], self.cancelled_last.get(i, self.last_delivery[i])) for i in self.ids])
        return lambda y: D

    def start_canal_close(self):
        D = self.carry([dt.date(2026, 10, 31)] * self.n)
        return lambda y: D

    def start_nocap(self):
        D = self.carry([self.last_delivery[i] for i in self.ids], cap=False)
        return lambda y: D

    def _model_season_then_winter(self, year, D):
        for d in K.season_days(year):
            D = self.day(D, d)
            D = np.where(D >= self.raw, 0.0, D)
        for d in K.daterange(dt.date(year, 11, 1), dt.date(year + 1, 1, 31)):
            D = self.day(D, d)
        return D

    def start_own_winter(self):
        """R1: each weather year from the state its own preceding autumn and winter left, the replay rule run through
        the year before from a full root zone on 1 February."""
        cache = {}

        def f(y):
            if y not in cache:
                cache[y] = self._model_season_then_winter(y - 1, np.zeros(self.n))
            return cache[y]
        return f

    def start_model_2026(self):
        """R2: the replay rule run through the 2026 season (from the state the 2025-26 winter left, itself from the
        rule run through 2025), then the observed autumn and winter."""
        D25 = self._model_season_then_winter(2025, np.zeros(self.n))
        D = self._model_season_then_winter(2026, D25)
        return lambda y: D


def order_from(req):
    """WOP 2.3: the smallest whole number of hundreds covering the requirement in at least 24 of 30 years."""
    ranked = sorted(req.items(), key=lambda kv: kv[1])
    y24, v24 = ranked[23]
    return dict(order=K.ceil_hundred(v24), year=y24, req=v24, ranked=ranked)


def schedule(order, mon):
    """WOP 5.1: shares of the thirty years' summed monthly requirements, each month to the nearest 10 acre-feet,
    October the difference."""
    tot_m = np.zeros(9)
    for y in K.REPLAY_YEARS:
        tot_m += mon[y]
    shares = tot_m / tot_m.sum()
    raw = order * shares
    months = [K.round_to(x, 10) for x in raw[:8]]
    months.append(order - sum(months))
    return months, raw, shares


def headgate_from_farm_by_lateral(farm_by_lat, loss, main):
    return float((np.asarray(farm_by_lat) / (1 - np.asarray(loss))).sum() / (1 - main))


# ---------------------------------------------------------------------------------------------------- loading the pack

def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.reader(fh))


def load_tables(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    T = dict(kc={}, root={}, mad={}, soils={}, ea={}, loss={}, main_loss=None)

    def rows(ws):
        out = []
        for row in ws.iter_rows(values_only=True):
            out.append(row)
        return out

    for row in rows(wb["T1 Crop coefficients"]):
        if row and isinstance(row[0], str) and row[0] in K.CROPS and isinstance(row[2], (int, float)):
            T["kc"][row[0]] = [float(x) for x in row[2:14]]
    for row in rows(wb["T2 Crops"]):
        if row and isinstance(row[0], str) and row[0] in K.CROPS and isinstance(row[2], (int, float)):
            T["root"][row[0]] = float(row[2])
            T["mad"][row[0]] = float(row[3])
    for row in rows(wb["T3 Soil units"]):
        if row and row[0] is not None and str(row[0]) in K.SOILS and isinstance(row[2], (int, float)):
            lim = row[3]
            T["soils"][str(row[0])] = (float(row[2]), None if lim in (None, "", "none", "None") else float(lim))
    for row in rows(wb["T4 Application efficiency"]):
        if row and row[0] in K.METHODS and isinstance(row[1], (int, float)):
            T["ea"][row[0]] = float(row[1])
    for row in rows(wb["T5 Loss allowances"]):
        if row and isinstance(row[0], str) and row[0].startswith("Lateral ") and isinstance(row[1], (int, float)):
            T["loss"]["L" + row[0].split()[1]] = float(row[1]) / 100.0
        if row and isinstance(row[0], str) and row[0].startswith("Main canal") and isinstance(row[1], (int, float)):
            T["main_loss"] = float(row[1]) / 100.0
    return T


def load_weather(target):
    s39 = {}
    rows = read_csv(os.path.join(target, K.ST39))
    head = rows[0]
    i_date, i_eto, i_pr = head.index("Date"), head.index("ETo (mm)"), head.index("Precip (mm)")
    for r in rows[1:]:
        m, d_, y = (int(x) for x in r[i_date].split("/"))
        s39[dt.date(y, m, d_)] = (float(r[i_eto]) / 25.4, float(r[i_pr]) / 25.4)
    yard = {}
    rows = read_csv(os.path.join(target, K.YARD))
    head = rows[0]
    i_ts, i_e, i_r = head.index("Date"), head.index("ETo_in"), head.index("Rain_in")
    for r in rows[1:]:
        if r[i_e] == "" or r[i_r] == "":
            continue
        d = dt.date.fromisoformat(r[i_ts])
        yard[d] = (float(r[i_e]), float(r[i_r]))
    wx = {}
    for d in K.daterange(K.WEATHER_START, K.WEATHER_END):
        wx[d] = yard[d] if (d >= K.SPLICE and d in yard) else s39[d]
    return wx, s39, yard


def load_requests(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["Requests"]
    rows = list(ws.iter_rows(values_only=True))
    hi = next(i for i, r in enumerate(rows) if r and r[0] == "Request no.")
    head = list(rows[hi])
    out = []
    for r in rows[hi + 1:]:
        if not r or r[0] is None:
            continue
        out.append(dict(zip(head, r)))
    return out


def load(target):
    T = load_tables(os.path.join(target, K.WOP_TABLES))
    wx, s39, yard = load_weather(target)
    reqs = load_requests(os.path.join(target, K.REQUESTS))
    reg = {}
    rows = read_csv(os.path.join(target, K.REGISTER))
    head = rows[0]
    for r in rows[1:]:
        reg[r[head.index("field_id")]] = dict(zip(head, r))
    crop_by_name = {v: k for k, v in K.CROP_NAME.items()}
    fields = []
    for q in reqs:
        if q["Status"] != "Accepted":
            continue
        fid = q["Field"]
        g = reg[fid]
        crop = q["Crop code"]
        fields.append(dict(id=fid, lateral="L" + g["lateral"].split()[-1], soil=g["soil_unit"], crop=crop,
                           method=q["Irrigation method"], acres=float(q["Acres"]), turnout=g["turnout_id"]))
    fields.sort(key=lambda f: f["id"])
    # the orders: each field's last delivered 2026 set, each turnout's, and the latest cancelled order after it
    rows = read_csv(os.path.join(target, K.ORDERS))
    head = rows[0]
    ix = {c: head.index(c) for c in head}
    last, tlast, canc, t_of = {}, {}, {}, {}
    for r in rows[1:]:
        if r[ix["season"]] != "2026":
            continue
        day = dt.date.fromisoformat(r[ix["set_start"]][:10])
        end_day = dt.date.fromisoformat(r[ix["set_end"]][:10])
        fid, tid = r[ix["field_id"]], r[ix["turnout"]]
        t_of[fid] = tid
        if r[ix["status"]] == "Delivered":
            last[fid] = max(last.get(fid, end_day), end_day)
            tlast[tid] = max(tlast.get(tid, end_day), end_day)
        elif r[ix["status"]] == "Cancelled":
            canc[fid] = max(canc.get(fid, day), day)
    turnout_last = {f["id"]: tlast[t_of[f["id"]]] for f in fields}
    M = Model(fields, wx, T, last_delivery=last, turnout_last=turnout_last, cancelled_last=canc)
    M.s39, M.yard = s39, yard
    M.requests = reqs
    M.register = reg
    return M


# ---------------------------------------------------------------------------------------------------- the ladder

RUNGS = [("R0", "full on 1 February", "start_full"),
         ("R1", "each weather year's own preceding autumn and winter", "start_own_winter"),
         ("R2", "the replay rule run through 2026, then the observed winter", "start_model_2026"),
         ("R2b", "full at the canal's close (31 October 2026), then the observed winter", "start_canal_close"),
         ("R2c", "each turnout's last delivered 2026 set for every field on it", "start_turnout"),
         ("R2d", "a field's last 2026 order whatever its status", "start_cancelled"),
         ("R3", "each field's own last delivered 2026 set through the observed winter (golden)", "start_golden"),
         ("O2", "the golden start with the winter cap dropped", "start_nocap")]


def ladder(M):
    out = {}
    for key, label, meth in RUNGS:
        req, mon = M.thirty(getattr(M, meth)())
        o = order_from(req)
        months, raw, shares = schedule(o["order"], mon)
        out[key] = dict(label=label, reqs=req, mon=mon, months=months, raw_months=raw, **o)
    # O1: each full-start replay plus each field's 31 January depletion taken as a flat addition at the turnouts
    D = M.D_golden
    add_farm = D / M.ea * M.acres / 12.0
    add_lat = np.bincount(M.lat, weights=add_farm, minlength=9)
    add_head = headgate_from_farm_by_lateral(add_lat, M.loss, M.main)
    req = {y: v + add_head for y, v in out["R0"]["reqs"].items()}
    o = order_from(req)
    out["O1"] = dict(label="the full-start replays plus each field's 31 January depletion as a flat addition",
                     reqs=req, mon=None, months=None, raw_months=None, **o)
    return out


# ---------------------------------------------------------------------------------------------------- the asks

def tid_from_book(x):
    a, b = x.split("-")
    return "%02d-%03d" % (int(a), int(b))


def tid_from_gis(x):
    return "%s-%s" % (x[1:3], x[3:6])


def load_asks(target):
    import openpyxl
    A = {}
    # meters in service and the season's changes
    wb = openpyxl.load_workbook(os.path.join(target, K.SHOP_LOG), data_only=True)
    units, cap = {}, {}
    rows = list(wb["Meters in service"].iter_rows(values_only=True))
    hi = next(i for i, r in enumerate(rows) if r and r[0] == "Meter")
    for r in rows[hi + 1:]:
        if not r or r[0] is None:
            continue
        units[r[0]] = "AF" if r[3] == "acre-feet" else "HCF"
        cap[r[0]] = float(str(r[4]).replace(",", ""))
    changes = []
    rows = list(wb["2026 changes"].iter_rows(values_only=True))
    hi = next(i for i, r in enumerate(rows) if r and r[0] == "Date")
    for r in rows[hi + 1:]:
        if not r or r[0] is None:
            continue
        day = r[0].date() if isinstance(r[0], dt.datetime) else r[0]
        hh, mm = (int(x) for x in str(r[1]).split(":"))
        changes.append(dict(turnout=tid_from_gis(r[2]), when=dt.datetime(day.year, day.month, day.day, hh, mm),
                            old=r[3], removal=float(r[4]), new=r[5], installation=float(r[6])))
    A["units"], A["cap"], A["changes"] = units, cap, changes
    # the riders' reads
    reads = {}
    rows = read_csv(os.path.join(target, K.METER_BOOK))
    head = rows[0]
    ix = {c: head.index(c) for c in head}
    for r in rows[1:]:
        m, d_, y = (int(x) for x in r[ix["read_date"]].split("/"))
        hh, mm = (int(x) for x in r[ix["read_time"]].split(":"))
        tid = tid_from_book(r[ix["turnout"]])
        reads.setdefault(tid, []).append((dt.datetime(y, m, d_, hh, mm), r[ix["meter"]], float(r[ix["reading"]])))
    for v in reads.values():
        v.sort()
    A["reads"] = reads
    # the register's (current) lateral by turnout
    lat = {}
    rows = read_csv(os.path.join(target, K.REGISTER))
    head = rows[0]
    for r in rows[1:]:
        lat[tid_from_gis(r[head.index("turnout_id")])] = "L" + r[head.index("lateral")].split()[-1]
    A["lateral"] = lat
    # headings
    heads = []
    rows = read_csv(os.path.join(target, K.HEADINGS))
    head = rows[0]
    for r in rows[1:]:
        heads.append((dt.date.fromisoformat(r[0]), "L" + r[1].split()[-1], float(r[3]), r[4]))
    A["headings"] = heads
    # tail weirs and their structure
    wb = openpyxl.load_workbook(os.path.join(target, K.STRUCTURES), data_only=True)
    weir = {}
    rows = list(wb["Tail weirs"].iter_rows(values_only=True))
    hi = next(i for i, r in enumerate(rows) if r and r[0] == "Lateral")
    for r in rows[hi + 1:]:
        if not r or r[0] is None:
            continue
        weir["L" + r[0].split()[-1]] = (float(r[2]), float(r[3]), float(r[4]))
    A["weir"] = weir
    sheets = {}
    rows = read_csv(os.path.join(target, K.WEIRS))
    for r in rows[1:]:
        m, d_, y = (int(x) for x in r[0].split("/"))
        sheets.setdefault("L" + r[1].split()[-1], []).append((dt.date(y, m, d_), float(r[4]), r[5]))
    for v in sheets.values():
        v.sort()
    A["sheets"] = sheets
    return A


MOVED_FROM = dt.date(2026, 6, 15)


def turnout_intervals(A, tid, mode="chain"):
    """Acre-feet a turnout's meters recorded between consecutive reads, as (end of interval, AF).
    mode chain: within a meter's own reads, and across a change through the shop's removal and installation reads;
    mode serial: within a meter's own reads only; mode turnout: consecutive reads whatever the meter."""
    rd = A["reads"][tid]
    ch = [c for c in A["changes"] if c["turnout"] == tid]
    out = []

    def af(serial, a, b):
        c = A["cap"][serial]
        d = (b - a) % c
        return d / 435.6 if A["units"][serial] == "HCF" else d

    for (t0, s0, v0), (t1, s1, v1) in zip(rd, rd[1:]):
        if s0 == s1:
            out.append((t1, af(s0, v0, v1)))
        elif mode == "chain":
            c = next(c for c in ch if c["old"] == s0 and c["new"] == s1)
            out.append((t1, af(s0, v0, c["removal"]) + af(s1, c["installation"], v1)))
        elif mode == "turnout":
            out.append((t1, (v1 - v0) % A["cap"][s1] if A["units"][s1] == "AF" else ((v1 - v0) % A["cap"][s1]) / 435.6))
        # mode serial: the interval across the change is lost
    return out


def ask_a(A, mode="chain", as_of=True, drop_estimated=False):
    deliv = {l: 0.0 for l in K.LATERALS}
    for tid in A["reads"]:
        reg_lat = A["lateral"][tid]
        built = "L%d" % int(tid[:2])
        for t1, v in turnout_intervals(A, tid, mode):
            if as_of and built != reg_lat:
                lat = built if t1.date() <= MOVED_FROM else reg_lat
            else:
                lat = reg_lat
            deliv[lat] += v
    inflow = {l: 0.0 for l in K.LATERALS}
    for d, l, v, q in A["headings"]:
        if drop_estimated and q == "E":
            continue
        inflow[l] += v
    share = {l: 100.0 * (inflow[l] - deliv[l]) / inflow[l] for l in K.LATERALS}
    return deliv, share, inflow


def board_counts(A, lat):
    """Boards in place at each reading, from the riders' remarks (a change is made before that day's reading)."""
    n = 0
    out = {}
    for d, g, rem in A["sheets"][lat]:
        rem = (rem or "").lower()
        if len(rem) > 6 and rem[2] == ":" and rem[:2].isdigit() and rem[3:5].isdigit():
            rem = rem[6:]          # the time the rider noted for the change, ahead of that sheet's reading
        if rem in ("set one 2-inch board", "added a 2-inch board"):
            n += 1
        elif rem == "pulled one board":
            n -= 1
        elif rem == "pulled boards":
            n = 0
        out[d] = n
    return out


def ask_b(A, boards=True, fill=True):
    spill = {}
    for lat in K.LATERALS:
        L, crest, C_ = A["weir"][lat]
        bc = board_counts(A, lat)
        rd = {d: g for d, g, _ in A["sheets"][lat]}
        tot = 0.0
        cur = None
        for d in K.season_days(2026):
            if d in rd:
                cur = (rd[d], bc[d])
            elif not fill:
                continue
            g, nb = cur
            h = g - (crest + (2.0 / 12.0 * nb if boards else 0.0))
            if h > 0:
                tot += C_ * L * h ** 1.5 * K.AF_PER_CFS_DAY
        spill[lat] = tot
    return spill
