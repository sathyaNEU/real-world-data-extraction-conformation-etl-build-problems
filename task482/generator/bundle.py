"""Reads task482's cut pack the way a solver must and computes every figure from it: each store's 2026 hours with its
vaccine above 8.0 degrees C under the golden handling and under each rung and licensed variant, each store's doses
unaccounted for (ask A) and each store's Brannon service spend (ask B). golden.py, checks.py and ceiling.py call it;
verify.py recomputes the golden without it.

The golden handling of the hours: every record put on UTC (Frostline's offsets, Kelvra's UTC and Fahrenheit,
Brumal's standard time, Tellvane's UTC) and joined to its store through the monitoring roster; at each pilot store
the in-carton sensor from its first reading, the store's logger before it. The vaccine's temperature behind a logger
record is the logger record carried through a first-order lag, each record holding over the ten minutes it stands for,
with the time constant fitted per logger make on the pilot stores' overlaps (the old logger's records after the
in-carton sensor's first reading, against the sensor). A record counts its ten minutes when the vaccine's temperature
at its time stamp is above 8.0."""
import csv
import datetime as dt
import os
from collections import defaultdict

import numpy as np

LIMIT, LINE = 8.0, 24.0
STEP = 10
Y0, Y1 = 360, 360 + 525600                       # the local (Central) year in UTC minutes from 2026-01-01T00:00Z
UPDATE = dt.datetime(2026, 6, 1)
PLATFORM = dt.date(2026, 7, 1)
TAX = 0.06
FILES = {
    "stores": "penwick_store_list_2027-01.xlsx", "roster": "refrigerator_monitoring_roster_2026.xlsx",
    "frostline": "frostline_temperature_logs_2026.csv", "kelvra": "kelvra_logger_export_2026.csv",
    "brumal": "brumal_downloads_2026.txt", "tellvane": "tellvane_sensor_readings_2026.csv",
    "invoices": "meridale_vaccine_invoices_2026.csv", "items": "vaccine_item_master_2026.xlsx",
    "admin": "pharmacy_vaccine_administrations_2026.csv", "writeoffs": "vaccine_writeoff_log_2026.csv",
    "credits": "meridale_credit_memos_2026.csv", "transfers": "vaccine_store_transfers_2026.csv",
    "inventory": "vaccine_physical_inventory_ye2025_ye2026.xlsx", "brannon": "brannon_service_history_2026-01_2027-01.xlsx",
    "agreement": "brannon_service_agreement_2025.pdf",
}
_D0 = dt.date(2026, 1, 1).toordinal()


def hround(x):
    """Round half away from zero (the deliverables' rounding)."""
    return int(np.floor(abs(x) + 0.5)) * (1 if x >= 0 else -1)


def _csv(target, key, skip=0):
    with open(os.path.join(target, FILES[key]), newline="", encoding="utf-8") as f:
        for _ in range(skip):
            f.readline()
        return list(csv.DictReader(f))


def _sheet(target, key, name, header_row=1):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, FILES[key]), read_only=True, data_only=True)
    rows = list(wb[name].iter_rows(values_only=True))
    head = rows[header_row - 1]
    return [dict(zip(head, r)) for r in rows[header_row:] if any(v is not None for v in r)]


def pdf_text(path):
    import subprocess
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout


def _day(y, m, d):
    return dt.date(y, m, d).toordinal() - _D0


def ifilter(x, c, y0, block=800):
    """y[n] = c[n] * y[n-1] + (1 - c[n]) * x[n], y[-1] = y0"""
    x = np.asarray(x, float)
    c = np.broadcast_to(np.asarray(c, float), x.shape)
    y = np.empty_like(x)
    prev = float(y0)
    for s in range(0, len(x), block):
        xs, cs = x[s:s + block], c[s:s + block]
        p = np.cumprod(cs)
        y[s:s + block] = p * (prev + np.cumsum((1.0 - cs) * xs / p))
        prev = y[s + len(xs) - 1]
    return y


class Inputs:
    """every file the figures read, parsed once"""

    def __init__(self, target):
        self.target = target
        st = _sheet(target, "stores", "Stores")
        self.order = [int(r["Store"]) for r in st]
        self.make = {}
        self.ship_to = {str(r["Meridale ship-to"]): int(r["Store"]) for r in st}
        self.former = {r["Former name"]: int(r["Store"]) for r in st if r["Former name"]}
        self.site = {r["Brannon site"]: int(r["Store"]) for r in st}
        self.unit = {int(r["Store"]): r["Vaccine refrigerator"] for r in st}
        ro = _sheet(target, "roster", "Devices")
        self.serial = {}
        self.sensor = {}
        for r in ro:
            no = int(r["Store"])
            if r["Device type"] == "Data logger":
                self.serial[r["Serial or sensor id"]] = no
                self.make[no] = r["Make"]
            else:
                self.sensor[r["Serial or sensor id"]] = no
        self.pilot = sorted(self.sensor.values())
        self._temps()
        self._stock()
        self._service()

    # ------------------------------------------------------------------------------------------------ temperatures
    def _temps(self):
        rec = defaultdict(list)
        with open(os.path.join(self.target, FILES["frostline"]), encoding="utf-8") as f:
            f.readline()
            for line in f:
                ser, loc, ts, v = line.rstrip("\n").split(",")
                d = _day(int(ts[0:4]), int(ts[5:7]), int(ts[8:10]))
                off = int(ts[20:22]) * 60
                rec[self.serial[ser]].append((d * 1440 + int(ts[11:13]) * 60 + int(ts[14:16]) + off, float(v)))
        with open(os.path.join(self.target, FILES["kelvra"]), encoding="utf-8") as f:
            for _ in range(4):
                f.readline()
            for line in f:
                ser, d_, t_, v = line.rstrip("\n").split(",")
                d = _day(int(d_[6:10]), int(d_[0:2]), int(d_[3:5]))
                rec[self.serial[ser]].append((d * 1440 + int(t_[0:2]) * 60 + int(t_[3:5]),
                                              (float(v) - 32.0) * 5.0 / 9.0))
        ser = None
        with open(os.path.join(self.target, FILES["brumal"]), encoding="utf-8") as f:
            for line in f:
                if line.startswith("Serial number:"):
                    ser = line.split(":", 1)[1].strip()
                elif len(line) > 10 and line[2] == "/" and "\t" in line:
                    d_, t_, v = line.rstrip("\n").split("\t")
                    d = _day(int(d_[6:10]), int(d_[0:2]), int(d_[3:5]))
                    rec[self.serial[ser]].append((d * 1440 + int(t_[0:2]) * 60 + int(t_[3:5]) + 360, float(v)))
        self.rec = {}
        self.dups = 0
        for no, lst in rec.items():
            lst.sort()
            u = np.array([a for a, _ in lst], dtype=np.int64)
            x = np.array([b for _, b in lst])
            keep = np.ones(len(u), bool)
            keep[1:] = u[1:] != u[:-1]
            self.dups += int((~keep).sum())
            self.rec[no] = (u[keep], x[keep])
        cl = defaultdict(list)
        with open(os.path.join(self.target, FILES["tellvane"]), encoding="utf-8") as f:
            f.readline()
            for line in f:
                sid, ts, v = line.rstrip("\n").split(",")
                d = _day(int(ts[0:4]), int(ts[5:7]), int(ts[8:10]))
                cl[self.sensor[sid]].append((d * 1440 + int(ts[11:13]) * 60 + int(ts[14:16]), float(v)))
        self.cl = {}
        for no, lst in cl.items():
            lst.sort()
            self.cl[no] = (np.array([a for a, _ in lst], dtype=np.int64), np.array([b for _, b in lst]))
        self.switch = {no: int(self.cl[no][0][0]) for no in self.cl}

    # ------------------------------------------------------------------------------------------------------ stock
    def _stock(self):
        items = _sheet(self.target, "items", "Vaccine items")
        self.dpp = {r["NDC"]: int(r["Doses per package"]) for r in items}
        self.vial = {r["NDC"]: "vial" in str(r["Package"]) for r in items}
        self.ndc_of11 = {}
        for n10 in self.dpp:
            a, b, c = n10.split("-")
            self.ndc_of11[a.zfill(5) + b.zfill(4) + c.zfill(2)] = n10
        self.counts = {}
        for yr in (2025, 2026):
            rows = _sheet(self.target, "inventory", "YE %d" % yr)
            tot = defaultdict(int)
            when = {}
            for r in rows:
                no = int(r["Store"])
                tot[no] += int(r["Doses on hand"])
                when[no] = r["Count closed"]
            self.counts[yr] = (dict(tot), when)
        self.receipts = []
        for r in _csv(self.target, "invoices"):
            no = self.ship_to.get(r["SHIP_TO"])
            if no is None:
                no = self.former["Lindqvist Apothecary #%d" % int(r["SHIP_TO_NAME"].split("#")[1])]
            n10 = self.ndc_of11[r["NDC"]]
            self.receipts.append((no, dt.datetime.strptime(r["DELIVERED"], "%m/%d/%Y %H:%M"),
                                  dt.datetime.strptime(r["INVOICE_DATE"], "%m/%d/%Y"),
                                  int(r["QTY_SHIPPED"]) * self.dpp[n10]))
        self.admin = [(int(r["store"]), dt.datetime.strptime(r["administered_at"], "%Y-%m-%d %H:%M"),
                       int(r["doses"])) for r in _csv(self.target, "admin")]
        self.writeoffs = [(int(r["store"]), dt.datetime.strptime(r["written_off_at"], "%Y-%m-%d %H:%M"), r["ndc"],
                           int(r["quantity"]), float(r["cost"])) for r in _csv(self.target, "writeoffs")]
        self.credits = []
        for r in _csv(self.target, "credits"):
            no = self.ship_to.get(r["SHIP_TO"])
            n10 = self.ndc_of11[r["NDC"]]
            per_unit = self.dpp[n10] if r["UOM"] == "VL" else 1
            self.credits.append((no, dt.datetime.strptime(r["MEMO_DATE"], "%m/%d/%Y"), int(r["QTY"]) * per_unit))
        self.transfers = [(int(r["from_store"]), int(r["to_store"]),
                           dt.datetime.strptime(r["shipped_at"], "%Y-%m-%d %H:%M"),
                           dt.datetime.strptime(r["received_at"], "%Y-%m-%d %H:%M"), int(r["doses"]))
                          for r in _csv(self.target, "transfers")]

    # ---------------------------------------------------------------------------------------------------- service
    def _service(self):
        import re
        self.pm_price = {}
        for line in pdf_text(os.path.join(self.target, FILES["agreement"])).splitlines():
            m = re.match(r"\s*(\w+ [A-Z]{1,2}-\d+)\s+(Pharmaceutical-grade|Household-style)\s+(\d+\.\d\d)\s*$", line)
            if m:
                self.pm_price[m.group(1)] = float(m.group(3))
        rows = _sheet(self.target, "brannon", "Service history", header_row=4)
        self.visits = []
        for r in rows:
            vd = r["Visit date"]
            idt = r["Invoice date"]
            self.visits.append(dict(store=self.site[r["Site"]], wo=r["Work order"], visit=int(r["Visit"]),
                                    date=vd.date() if hasattr(vd, "date") else vd, invoice=str(r["Invoice"]),
                                    invoice_date=idt.date() if hasattr(idt, "date") else idt,
                                    amount=float(r["Invoice amount"])))


# ---------------------------------------------------------------------------------------------------- the hours
def states(u, x, tau, prev=False):
    """the lag's state at each record's time stamp: the input over each interval is the record that opens it (or,
    prev=True, the record that closes it)"""
    c = np.exp(-np.diff(u).astype(float) / tau)
    v = np.empty(len(x))
    v[0] = x[0]
    v[1:] = ifilter(x[1:] if prev else x[:-1], c, x[0])
    return v


def overlap(I, no):
    u, x = I.rec[no]
    cu, cx = I.cl[no]
    k = (cu >= I.switch[no]) & (cu < u[-1] + STEP)
    return cu[k], cx[k]


def sse(I, nos, tau):
    s, n = 0.0, 0
    for no in nos:
        u, x = I.rec[no]
        v = states(u, x, tau)
        cu, cx = overlap(I, no)
        k = np.searchsorted(u, cu, side="right") - 1
        est = x[k] + (v[k] - x[k]) * np.exp(-(cu - u[k]) / tau)
        s += float(((est - cx) ** 2).sum())
        n += len(cx)
    return s, n


def fit(I, nos, lo=20.0, hi=80.0):
    g = 0.6180339887498949
    a, b = lo, hi
    for _ in range(70):
        c, d = b - (b - a) * g, a + (b - a) * g
        if sse(I, nos, c)[0] < sse(I, nos, d)[0]:
            b = d
        else:
            a = c
    t = (a + b) / 2
    return t, float(np.sqrt(sse(I, nos, t)[0] / sse(I, nos, t)[1]))


def taus(I, group="make"):
    """the fitted time constant behind each store: per make (golden), pooled, or each pilot store's own"""
    if group == "pooled":
        t = fit(I, I.pilot)[0]
        return {no: t for no in I.order}
    by = {}
    for mk in sorted(set(I.make.values())):
        by[mk] = fit(I, [no for no in I.pilot if I.make[no] == mk])[0]
    out = {no: by[I.make[no]] for no in I.order}
    if group == "store":
        for no in I.pilot:
            out[no] = fit(I, [no])[0]
    return out


def _dur(u, end):
    return np.clip(np.minimum(np.diff(np.append(u, end)), STEP), 0, None)


def _count(u, y, end):
    m = (u >= Y0) & (u < Y1)
    return float((_dur(u, end) * (y > LIMIT) * m).sum()) / 60.0


def logger_part(I, no):
    u, x = I.rec[no]
    end = I.switch.get(no, Y1)
    k = u < end
    return u, x, k, min(end, Y1)


def tellvane_hours(I, no):
    if no not in I.cl:
        return 0.0
    cu, cx = I.cl[no]
    return _count(cu, cx, Y1)


def store_hours(I, no, est):
    """hours above 8.0: the logger estimate before the switch, the in-carton sensor after"""
    u, x, k, end = logger_part(I, no)
    return _count(u[k], est[k], end) + tellvane_hours(I, no)


def golden_hours(I, tau=None, prev=False, conv="start", shift=0.0):
    tau = tau or taus(I)
    out = {}
    for no in I.order:
        u, x = I.rec[no]
        t = tau[no] + shift
        v = states(u, x, t, prev=prev)
        if conv == "mean":
            dts = np.minimum(np.diff(np.append(u, u[-1] + STEP)), STEP).astype(float)
            v = x + (v - x) * t / dts * (1 - np.exp(-dts / t))
        elif conv == "end":
            v = np.append(states(u, x, t)[1:], x[-1])
        out[no] = store_hours(I, no, v)
    return out


def runs(I, no, keep):
    """the logger's runs above 8.0 (pre-switch), kept by a rule on (duration in minutes, peak, start)"""
    u, x, k, end = logger_part(I, no)
    u, x = u[k], x[k]
    d = _dur(u, end)
    m = (u >= Y0) & (u < Y1)
    hot = (x > LIMIT) & m
    tot, i = 0.0, 0
    n = len(u)
    while i < n:
        if not hot[i]:
            i += 1
            continue
        j = i
        while j < n and hot[j]:
            j += 1
        dur = float(d[i:j].sum())
        if keep(dur, float(x[i:j].max()), int(u[i])):
            tot += dur
        i = j
    return tot / 60.0 + tellvane_hours(I, no)


def trailing(u, x, k):
    cs = np.concatenate([[0.0], np.cumsum(x)])
    lo = np.searchsorted(u, u - k + 1e-9, side="left")
    idx = np.arange(len(x))
    return (cs[idx + 1] - cs[lo]) / (idx + 1 - lo)


def overlap_ratio(I):
    """in-carton hours over logger hours above 8.0 across the pilot stores' overlaps"""
    a = b = 0.0
    for no in I.pilot:
        u, x = I.rec[no]
        k = u >= I.switch[no]
        b += _count(u[k], x[k], u[-1] + STEP)
        cu, cx = overlap(I, no)
        a += _count(cu, cx, cu[-1] + STEP if len(cu) else Y1)
    return a / b if b else 0.0


def rung_hours(I, rung):
    """each wrong rung's hours by store"""
    out = {}
    if rung == "R3":
        ratio = overlap_ratio(I)
    if rung == "R6":
        dl = defaultdict(list)
        for (no, t, inv, doses) in I.receipts:
            dl[no].append(local_to_u(t))
    for no in I.order:
        u, x = I.rec[no]
        if rung == "R0":
            out[no] = store_hours(I, no, x)
        elif rung in ("R1a", "R1b"):
            lim = 30 if rung == "R1a" else 60
            out[no] = runs(I, no, lambda dur, pk, st: dur >= lim)
        elif rung == "R1c":
            out[no] = runs(I, no, lambda dur, pk, st: pk > 10.0)
        elif rung.startswith("MA"):
            out[no] = store_hours(I, no, trailing(u, x, int(rung[2:])))
        elif rung == "R3":
            uu, xx, k, end = logger_part(I, no)
            out[no] = _count(uu[k], xx[k], end) * ratio + tellvane_hours(I, no)
        elif rung == "R4":
            out[no] = runs(I, no, lambda dur, pk, st: not (pk < 9.5 and 25 <= dur <= 75))
        elif rung == "R6":
            ds = np.array(sorted(dl[no]))
            out[no] = runs(I, no, lambda dur, pk, st: not np.any((st >= ds - 10) & (st <= ds + 50)))
        else:
            raise KeyError(rung)
    return out


def local_to_u(t):
    """a Central local wall time to UTC minutes"""
    d = t.date().toordinal() - _D0
    m = d * 1440 + t.hour * 60 + t.minute
    dst = dt.datetime(2026, 3, 8, 2) <= t < dt.datetime(2026, 11, 1, 1)
    return m + (300 if dst else 360)


def covered(h):
    return sorted(no for no, v in h.items() if v >= LINE)


def nearest_below(h):
    below = [(v, no) for no, v in h.items() if v < LINE]
    if not below:
        return None
    v, no = max(below)
    return no, v, LINE - v


# ------------------------------------------------------------------------------------------------------- ask A
def unaccounted(I, cut=True, vials=True, credits=False):
    """each store's doses unaccounted for: its count at the start of the year and its receipts, less what left its
    stock and its count at the year's end. cut=True takes the flows between the two counts' own times (False: the
    calendar year, the counts read as the year's ends); vials=True reads the write-off log's multi-dose vial quantities
    before the 1 June 2026 update as vials; credits=True also takes Meridale's return credits off"""
    (o, ow), (c, cw) = I.counts[2025], I.counts[2026]
    a = {no: ow[no] if cut else dt.datetime(2026, 1, 1) for no in I.order}
    b = {no: cw[no] if cut else dt.datetime(2026, 12, 31, 23, 59, 59) for no in I.order}

    def inside(no, t):
        return (a[no] < t <= b[no]) if cut else (a[no] <= t <= b[no])
    bal = {no: o.get(no, 0) - c.get(no, 0) for no in I.order}
    for (no, t, inv, doses) in I.receipts:
        if inside(no, t):
            bal[no] += doses
    for (no, t, doses) in I.admin:
        if inside(no, t):
            bal[no] -= doses
    for (no, t, ndc, q, cost) in I.writeoffs:
        if inside(no, t):
            bal[no] -= q * (I.dpp[ndc] if (vials and I.vial[ndc] and t < UPDATE) else 1)
    for (fr, to, ts, tr, doses) in I.transfers:
        if inside(fr, ts):
            bal[fr] -= doses
        if inside(to, tr):
            bal[to] += doses
    if credits:
        for (no, t, doses) in I.credits:
            if inside(no, t):
                bal[no] -= doses
    return bal


# ------------------------------------------------------------------------------------------------------- ask B
def service(I, tax=True, by_invoice_date=True, dedupe=True, completed=True, split=True):
    """each store's Brannon spend for work completed in 2026, as invoiced with sales tax: one amount per invoice
    (dedupe), the tax added to the invoices from before the 1 July 2026 platform move (by invoice date, or False: by
    the visit's date), work completed in 2026 (or False: each visit's own date), and an invoice whose visits are at
    several stores (a maintenance route) split by each store's unit's maintenance price (split; False: the whole
    amount to each of its stores)"""
    wo = defaultdict(list)
    for v in I.visits:
        wo[v["invoice"]].append(v)
    out = defaultdict(float)
    for inv, vs in wo.items():
        last = max(v["date"] for v in vs)
        stores = sorted(set(v["store"] for v in vs))
        if dedupe:
            first = {}
            for v in vs:
                first.setdefault(v["store"], v)
            rows = [first[no] for no in stores]
        else:
            rows = vs
        prices = {no: I.pm_price[I.unit[no]] for no in stores}
        for v in rows:
            when = last if completed else v["date"]
            if when.year != 2026:
                continue
            amt = v["amount"]
            pre = (v["invoice_date"] < PLATFORM) if by_invoice_date else (v["date"] < PLATFORM)
            if tax and pre:
                amt = round(amt + round(amt * TAX + 1e-9, 2), 2)
            if split and len(stores) > 1:
                amt = amt * prices[v["store"]] / sum(prices.values())
            out[v["store"]] += amt
    return {no: round(out[no], 2) for no in I.order}
