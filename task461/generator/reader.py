"""Read the shipped pack back the way an analyst conforms it: both TMS exports into one load register on the
terminal's local clock (shadow rows and cancelled transactions out, plates and tanker ids resolved to fleet units
and the dispatch system's compartment numbers), the dockets on the wall clock their offsets belong to, the CEMS by
its own offsets, the dips at 06:00 AEST, the outturns, the shift log by shift date and the PLC's returns. golden.py
and ceiling.py share it."""
import csv
import datetime as dt
import math
import os
import re

import openpyxl

import world as W

D = dt.timedelta
CANON_OLD = {v: k for k, v in W.NAME_OLD_TAS.items()}
CANON_NEW = {v: k for k, v in W.NAME_NEW_TAS.items()}
CANON_DOCKET = {v: k for k, v in W.NAME_DOCKET.items()}
CUTOVER = dt.datetime(2026, 7, 1)
# ASTM D1250 Table 54B constants (generalised products), for the reading that recomputes the legacy VCF unrounded
K54B = {"ULP": (346.4228, 0.4388), "P95": (346.4228, 0.4388), "P98": (346.4228, 0.4388), "DSL": (186.9696, 0.4862)}


def vcf_54b(product, temp_c, rho15):
    k0, k1 = K54B[product]
    a = k0 / rho15 ** 2 + k1 / rho15
    t = temp_c - 15.0
    return math.exp(-a * t * (1 + 0.8 * a * t))


def _csv(target, key):
    with open(os.path.join(target, W.FILES[key]), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def utc_to_local(utc):
    return W.to_local(utc)


def register(target):
    wb = openpyxl.load_workbook(os.path.join(target, W.FILES["tankers"]), read_only=True)
    ws = wb["Units"]
    rows = list(ws.iter_rows(values_only=True))
    head = rows[0]
    units = {}
    plates = []          # (plate, uid, trailer, valid_from, valid_to)
    by_tms = {}
    for r in rows[1:]:
        if not r[0]:
            continue
        rec = dict(zip(head, r))
        uid = rec["Fleet unit"]
        cfg = rec["Configuration"]
        units[uid] = dict(config=cfg, operator=rec["Operator"], tms=rec["TMS tanker ID"])
        by_tms[rec["TMS tanker ID"]] = uid
        cur = {"lead": rec["Lead trailer rego"], "dog": rec["Dog trailer rego"] or None}
        prev = rec["Previous regos"] or ""
        starts = {"lead": dt.datetime(2000, 1, 1), "dog": dt.datetime(2000, 1, 1)}
        for part in [p.strip() for p in prev.split(";") if p.strip()]:
            m = re.match(r"(lead|dog) (\S+) until (\d\d/\d\d/\d{4})", part)
            tr, old, until = m.group(1), m.group(2), dt.datetime.strptime(m.group(3), "%d/%m/%Y")
            plates.append((old, uid, tr, dt.datetime(2000, 1, 1), until + D(days=1)))
            starts[tr] = until + D(days=1)
        for tr in ("lead", "dog"):
            if cur[tr]:
                plates.append((cur[tr], uid, tr, starts[tr], dt.datetime(2100, 1, 1)))
    return units, plates, by_tms


def plate_lookup(plates, plate, when):
    for p, uid, tr, a, b in plates:
        if p == plate and a <= when < b:
            return uid, tr
    raise KeyError((plate, when))


def tms_loads(target, keep_shadow=False, keep_cancelled=False, dog_through=True, current_plates_only=False,
              round_net=False, vcf_table=False):
    """One row per compartment load at the terminal, on local time (the keyword switches are Layer 1 mishandlings
    checks.py prices)."""
    units, plates, by_tms = register(target)
    out = []
    for r in _csv(target, "tas_old"):
        t = dt.datetime.strptime(r["LOAD_DATE"] + " " + r["LOAD_TIME"], "%d/%m/%Y %H:%M:%S")
        if t >= CUTOVER:
            continue
        try:
            if current_plates_only:
                cands = [(u, tr) for p, u, tr, a, b in plates if p == r["TRAILER_REGO"] and b.year == 2100]
                if not cands:
                    continue
                uid, tr = cands[0]
            else:
                uid, tr = plate_lookup(plates, r["TRAILER_REGO"], t)
        except KeyError:
            continue
        comp = int(r["COMP"]) + (5 if (tr == "dog" and dog_through) else 0)
        gross = int(r["GROSS_L"])
        f = (vcf_54b(CANON_OLD[r["PRODUCT"]], float(r["TEMPERATURE"]), float(r["DENS15"])) if vcf_table
             else float(r["VCF"]))
        out.append(dict(local=t, bay=int(r["BAY"]), product=CANON_OLD[r["PRODUCT"]], unit=uid, comp=comp,
                        gross=gross, temp=float(r["TEMPERATURE"]),
                        net=round(gross * f) if round_net else gross * f,
                        operator="BRN" if r["CARRIER"] == "BRN" else "OAK", src="old"))
    wb = openpyxl.load_workbook(os.path.join(target, W.FILES["tas_new"]), read_only=True)
    ws = wb["Transactions"]
    rows = list(ws.iter_rows(values_only=True))
    hi = [i for i, r in enumerate(rows) if r and r[0] == "Transaction ID"][0]
    head = rows[hi]
    for r in rows[hi + 1:]:
        if not r or r[0] is None:
            continue
        rec = dict(zip(head, r))
        if rec["Status"] != "Complete" and not keep_cancelled:
            continue
        t = dt.datetime.strptime(rec["Loaded (local)"], "%Y-%m-%d %H:%M:%S")
        if t < CUTOVER and not keep_shadow:
            continue
        out.append(dict(local=t, bay=int(rec["Bay"]), product=CANON_NEW[rec["Product"]], unit=by_tms[rec["Tanker"]],
                        comp=int(rec["Compartment"]), gross=int(rec["Gross obs L"]), temp=float(rec["Temp C"]),
                        net=float(rec["Net 15C L"]), operator="BRN" if rec["Account"] == "BRENNOCK" else "OAK",
                        src="new"))
    out.sort(key=lambda d: (d["local"], d["unit"], d["comp"]))
    return out


def dockets(target, convert_utc=True):
    """Docket times carry their own offset, so the wall time before it is the terminal clock; convert_utc=False
    is the mishandling that reads that wall time as UTC and moves it to local a second time."""
    out = []
    conv = (lambda t: t) if convert_utc else utc_to_local
    for r in _csv(target, "dockets"):
        a = dt.datetime.strptime(r["arrived_at"][:19], "%Y-%m-%dT%H:%M:%S")
        b = dt.datetime.strptime(r["completed_at"][:19], "%Y-%m-%dT%H:%M:%S")
        out.append(dict(unit=r["fleet_unit"], comp=int(r["compartment"]), product=CANON_DOCKET[r["product"]],
                        vr=r["vr1_hose"] == "Y", arr=conv(a), done=conv(b), site=r["site_code"],
                        litres=int(r["litres_delivered"]), terminal=r["source_terminal"], ref=r["source_doc"],
                        loaded=int(r["bol_litres_15c"])))
    out.sort(key=lambda d: (d["done"], d["unit"], d["comp"]))
    return out


def parse_iso_off(s):
    base, off = s[:19], s[19:]
    t = dt.datetime.strptime(base, "%Y-%m-%dT%H:%M:%S")
    sign = 1 if off[0] == "+" else -1
    hh, mm_ = int(off[1:3]), int(off[4:6])
    return t - sign * D(hours=hh, minutes=mm_)        # UTC


def cems(target):
    """Each 15-minute interval: UTC start, kg/h (None where no valid reading), status."""
    out = []
    for r in _csv(target, "vru_cems"):
        u = parse_iso_off(r["interval_start"])
        v = r["value"]
        if r["status"] == "CAL" or v == "":
            rate = None
        elif r["unit"] == "g/min":
            rate = float(v) * 60.0 / 1000.0
        else:
            rate = float(v)
        out.append(dict(utc=u, rate=rate, status=r["status"]))
    out.sort(key=lambda d: d["utc"])
    return out


def vru_release_by_quarter(rows):
    """Protocol 3.1 and 3.2: tonnes per quarter of the intervals beginning in it."""
    rates = []
    n = len(rows)
    for i, r in enumerate(rows):
        if r["status"] == "OFF":
            rates.append(0.0)
        elif r["rate"] is None:
            nb = [rows[j]["rate"] for j in range(max(0, i - 4), min(n, i + 5))
                  if j != i and rows[j]["rate"] is not None and rows[j]["status"] == "OK"]
            rates.append(sum(nb) / len(nb))
        else:
            rates.append(r["rate"])
    q = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}
    for r, rate in zip(rows, rates):
        loc = W.to_local(r["utc"])
        q[(loc.month - 1) // 3 + 1] += rate * 0.25 / 1000.0
    return q


def gauging(target):
    """The tank gauging system keeps AEST all year (shift log at each daylight-saving change; work order TGS-1)."""
    out = []
    for r in _csv(target, "gauging"):
        u = dt.datetime.strptime(r["dip_time"], "%d/%m/%Y %H:%M") - D(hours=10)
        out.append(dict(utc=u, local=W.to_local(u), tank=r["tank"], nsv=int(r["nsv_l"])))
    return out


def outturns(target):
    wb = openpyxl.load_workbook(os.path.join(target, W.FILES["outturns"]), read_only=True)
    ws = wb["Outturns 2026"]
    rows = list(ws.iter_rows(values_only=True))
    head = rows[0]
    out = []
    for r in rows[1:]:
        if not r or r[0] is None:
            continue
        rec = dict(zip(head, r))
        out.append(dict(tank=rec["Shore tank"], start=rec["Commenced"], end=rec["Completed"],
                        shore=int(rec["Shore received L15"]), report=rec["Report date"], grade=rec["Grade"]))
    return out


def _log_local(r):
    d0 = dt.datetime.strptime(r["shift_date"], "%d/%m/%Y")
    hh, mi = (int(x) for x in r["time"].split(":"))
    t = d0 + D(hours=hh, minutes=mi)
    if r["shift"] == "N" and hh < 18:
        t = t + D(days=1)
    return t


def absorber_lineups(target):
    """VRU-1's absorber tank over time from the shift log: (local time, tank), TK-1 before the first change."""
    out = []
    for r in _csv(target, "shiftlog"):
        m = re.match(r"VRU-1 absorber supply and return lined up from TK-\d to (TK-\d)", r["entry"])
        if m:
            out.append((_log_local(r), m.group(1)))
        elif "VRU-1 absorber supply and return back on TK-1" in r["entry"]:
            out.append((_log_local(r), "TK-1"))
    return sorted(out)


def shift_log(target):
    """Line-up changes and transfers, each on the local clock: a night shift's entries after midnight carry the
    date the shift started."""
    lineups, transfers = [], []
    open_tr = {}
    for r in _csv(target, "shiftlog"):
        d0 = dt.datetime.strptime(r["shift_date"], "%d/%m/%Y")
        hh, mi = (int(x) for x in r["time"].split(":"))
        t = d0 + D(hours=hh, minutes=mi)
        if r["shift"] == "N" and hh < 18:
            t = t + D(days=1)
        e = r["entry"]
        m = re.match(r"Diesel header changed over (TK-\d) to (TK-\d)", e)
        if m:
            lineups.append(dict(local=t, frm=m.group(1), to=m.group(2)))
        m = re.match(r"Transfer (TK-\d) to (TK-\d) (commenced|completed), transfer meter ([\d,]+) L", e)
        if m:
            key = (m.group(1), m.group(2))
            v = int(m.group(4).replace(",", ""))
            if m.group(3) == "commenced":
                open_tr[key] = (t, v)
            else:
                t0, v0 = open_tr.pop(key)
                transfers.append(dict(start=t0, end=t, src=m.group(1), dst=m.group(2), litres=v - v0))
    lineups.sort(key=lambda d: d["local"])
    return lineups, transfers


def plc_returns(target, follow_lineups=True):
    """The absorber return pump's deliveries, each to the tank the shift log had the absorber lined up to
    (follow_lineups=False books every one to TK-1, the absorber's usual tank)."""
    lus = absorber_lineups(target) if follow_lineups else []
    out = []
    for r in _csv(target, "vru_plc"):
        if r["event"] != "PRODUCT RETURN":
            continue
        t = dt.datetime.strptime(r["event_time"], "%d/%m/%Y %H:%M:%S")
        tank = "TK-1"
        for when, tk in lus:
            if when <= t:
                tank = tk
        out.append(dict(local=t, litres=int(r["litres_15c"]), tank=tank))
    return out


def tank_register(target):
    wb = openpyxl.load_workbook(os.path.join(target, W.FILES["tankreg"]), read_only=True)
    rows = list(wb["Tanks"].iter_rows(values_only=True))
    head = rows[0]
    out = {}
    for r in rows[1:]:
        if r and r[0] and str(r[0]).startswith("TK-"):
            rec = dict(zip(head, r))
            out[rec["Tank"]] = dict(roof=rec["Roof"], seal=rec["Rim seal"], vents=rec["Vents"],
                                    diameter=float(rec["Diameter (m)"]))
    return out


def seal_works(target):
    """Each internal floating roof's secondary seal completion, from the maintenance work orders."""
    out = {}
    for r in _csv(target, "workorders"):
        if "secondary seal" in r["description"] and r["completed"]:
            out[r["asset_tag"]] = dt.datetime.strptime(r["completed"], "%d/%m/%Y %H:%M")
    return out


def vent_works(target):
    """Each fixed-roof tank's pressure-vacuum vent completion, from the maintenance work orders."""
    out = {}
    for r in _csv(target, "workorders"):
        if "pressure-vacuum vents" in r["description"] and r["completed"]:
            out[r["asset_tag"]] = dt.datetime.strptime(r["completed"], "%d/%m/%Y %H:%M")
    return out
