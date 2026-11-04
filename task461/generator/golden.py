"""The goldens, computed from the shipped pack alone (reader.py): the 2026 release at each loading point and quarter,
the tanks' releases by the protocol's tank method, and the terminal's stock account; and the wrong rungs on the same
records, for checks.py and ceiling.py."""
import bisect
import datetime as dt
import math
from collections import defaultdict

import reader as R
import world as W

D = dt.timedelta
BOUNDS = [dt.datetime(2026, 1, 1), dt.datetime(2026, 4, 1), dt.datetime(2026, 7, 1), dt.datetime(2026, 10, 1),
          dt.datetime(2027, 1, 1)]


def quarter(local):
    return (local.month - 1) // 3 + 1


def vap(key, temp, sat):
    return W.vapour_kg_per_kl(key, temp, sat)


def diesel_own(l):
    return l["gross"] / 1000.0 * vap("diesel", l["temp"], 0.6)


def petrol_pushed(l):
    return l["gross"] / 1000.0 * vap(W.grade_season(l["local"].month), l["temp"], 1.0)


def previous_drops(dk):
    idx = defaultdict(list)
    for d in dk:
        idx[(d["unit"], d["comp"])].append(d)
    for k in idx:
        idx[k].sort(key=lambda d: d["done"])
    keys = {k: [d["done"] for d in v] for k, v in idx.items()}
    return idx, keys


def last_before(idx, keys, unit, comp, t):
    ks = keys.get((unit, comp), [])
    i = bisect.bisect_left(ks, t) - 1
    return idx[(unit, comp)][i] if i >= 0 else None


def loading(target, window=None, convert_utc=True, tms_kw=None, temp_mode="meter", season_mode="load",
            volume="gross"):
    """Each distillate load's release and every rung's, by bay and quarter (tonnes). The keyword switches are the
    readings and mishandlings checks.py prices; the defaults are the golden's."""
    a, b = window or (dt.datetime(2026, 1, 1), dt.datetime(2027, 1, 1))
    loads = [l for l in R.tms_loads(target, **(tms_kw or {})) if a <= l["local"] < b]
    dk = R.dockets(target, convert_utc=convert_utc)
    month_mean = defaultdict(list)
    for l in loads:
        month_mean[l["local"].month].append(l["temp"])
    month_mean = {m: sum(v) / len(v) for m, v in month_mean.items()}
    idx, keys = previous_drops(dk)
    last_tms = {}
    out = {r: defaultdict(float) for r in ("R0", "R1", "R2", "G", "G_s06", "G_replace")}
    per_load = []
    missing = 0
    for l in loads:
        prev_tms = last_tms.get((l["unit"], l["comp"]))
        last_tms[(l["unit"], l["comp"])] = l["product"]
        if l["bay"] not in W.DISTILLATE_BAYS:
            continue
        q = quarter(l["local"])
        k = (l["bay"], q)
        p = last_before(idx, keys, l["unit"], l["comp"], l["local"])
        ll = dict(l)
        if temp_mode == "month":
            ll["temp"] = round(month_mean[l["local"].month], 1)
        if volume == "net":
            ll["gross"] = l["net"]
        own = diesel_own(ll)
        pet = petrol_pushed(ll)
        if season_mode == "previous" and p is not None:
            pet = ll["gross"] / 1000.0 * vap(W.grade_season(p["done"].month), ll["temp"], 1.0)
        if p is None:
            missing += 1
        switch = p is not None and p["product"] != "DSL" and p["vr"]
        out["R0"][k] += own
        out["R1"][k] += own + (pet if l["operator"] == "BRN" else 0.0)
        out["R2"][k] += own + (pet if (prev_tms is not None and prev_tms != "DSL") else 0.0)
        out["G"][k] += own + (pet if switch else 0.0)
        out["G_s06"][k] += own + (pet * 0.6 if switch else 0.0)
        out["G_replace"][k] += pet if switch else own
        per_load.append(dict(l=l, switch=switch, prev=p))
    res = {r: {k: v / 1000.0 for k, v in d.items()} for r, d in out.items()}
    return res, per_load, missing


def vru(target):
    return R.vru_release_by_quarter(R.cems(target))


def header_at(lineups, t, first_from):
    """The diesel header's tank at local time t from the shift log's changes."""
    tank = first_from
    for lu in lineups:
        if lu["local"] <= t:
            tank = lu["to"]
        else:
            break
    return tank


def manual_loads(target, per_line=False):
    """Loads the petrol rack made on manual bills of lading while its terminal automation controller was down: the
    dispatch dockets carry them, one bill quantity per compartment on each line that compartment delivered
    (per_line=True sums every line, counting a split compartment twice)."""
    seen = {}
    for d in R.dockets(target):
        if d["terminal"] == "WARRENBY" and d["ref"].startswith("MB-"):
            k = (d["ref"], d["unit"], d["comp"]) if not per_line else (d["ref"], d["unit"], d["comp"], d["site"])
            if k not in seen:
                seen[k] = dict(local=d["arr"], product=d["product"], net=d["loaded"])
    return list(seen.values())


def stock_account(target, night_shift_dates=True, dip_offset=True, with_returns=True, with_lineup=True,
                  with_transfers=True, tms_kw=None, returns_to_tk1=False, with_manual=True, manual_per_line=False):
    """kL gain (+) or loss (-) per tank and quarter; the keyword switches are the wrong routes ceiling.py prices."""
    loads = R.tms_loads(target, **(tms_kw or {}))
    lineups, transfers = R.shift_log(target)
    if not night_shift_dates:
        lineups, transfers = _naive_shift(target)
    first_from = lineups[0]["frm"]
    dips = R.gauging(target)
    rec = R.outturns(target)
    rets = R.plc_returns(target, follow_lineups=not returns_to_tk1)
    pet_tank = {"ULP": "TK-1", "P95": "TK-2", "P98": "TK-3"}

    def tank_of(l):
        if l["product"] in pet_tank:
            return pet_tank[l["product"]]
        if with_lineup:
            return header_at(lineups, l["local"], first_from)
        return "TK-4" if (l["local"].day + l["local"].hour) % 2 == 0 else "TK-5"
    disp = [(l["local"], tank_of(l), l["net"]) for l in loads]
    if with_manual:
        disp += [(m["local"], pet_tank[m["product"]], m["net"]) for m in manual_loads(target, manual_per_line)]

    def dip_local(d):
        return d["local"] if dip_offset else d["utc"] + D(hours=10)
    stock_mid = {}
    for b in BOUNDS:
        for tk in W.TANKS:
            ds = [d for d in dips if d["tank"] == tk and dip_local(d).date() == b.date()]
            assert len(ds) == 1, (tk, b)
            dl = dip_local(ds[0])
            out_ = sum(v for t, k, v in disp if k == tk and b <= t < dl)
            back = sum(r["litres"] for r in rets if r["tank"] == tk and b <= r["local"] < dl) if with_returns else 0
            assert not any(r_["tank"] == tk and r_["start"] < dl and r_["end"] > b for r_ in rec)
            assert not any((tr["src"] == tk or tr["dst"] == tk) and tr["start"] < dl and tr["end"] > b
                           for tr in transfers)
            stock_mid[(tk, b)] = ds[0]["nsv"] + out_ - back
    gain = {}
    parts = {}
    for qi in range(4):
        a, b = BOUNDS[qi], BOUNDS[qi + 1]
        for tk in W.TANKS:
            received = sum(r_["shore"] for r_ in rec if r_["tank"] == tk and a <= r_["start"] < b)
            dispatched = sum(v for t, k, v in disp if k == tk and a <= t < b)
            back = sum(r["litres"] for r in rets if r["tank"] == tk and a <= r["local"] < b) if with_returns else 0
            t_in = sum(tr["litres"] for tr in transfers if tr["dst"] == tk and a <= tr["end"] < b) if with_transfers else 0
            t_out = sum(tr["litres"] for tr in transfers if tr["src"] == tk and a <= tr["end"] < b) if with_transfers else 0
            g = stock_mid[(tk, b)] - stock_mid[(tk, a)] - received - back - t_in + dispatched + t_out
            gain[(tk, qi + 1)] = g / 1000.0
            parts[(tk, qi + 1)] = dict(opening=stock_mid[(tk, a)], received=received, returned=back, t_in=t_in,
                                       dispatched=dispatched, t_out=t_out, closing=stock_mid[(tk, b)])
    return gain, parts


def _naive_shift(target):
    """The shift log read as calendar dates: a night shift's after-midnight entries left on the shift's date."""
    import csv
    import os
    import re
    lineups, transfers, open_tr = [], [], {}
    with open(os.path.join(target, W.FILES["shiftlog"]), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d0 = dt.datetime.strptime(r["shift_date"], "%d/%m/%Y")
            hh, mi = (int(x) for x in r["time"].split(":"))
            t = d0 + D(hours=hh, minutes=mi)
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


def tank_voc(target, seal_history=True):
    """kg per tank over 2026 by the protocol's tank method (5.2 and 5.3)."""
    reg = R.tank_register(target)
    works = R.seal_works(target)
    vents = R.vent_works(target)
    rec = R.outturns(target)
    out = {}
    for tk, t in reg.items():
        dia = t["diameter"]
        standing = 0.0
        day = dt.datetime(2026, 1, 1)
        while day.year == 2026:
            if t["roof"].startswith("Fixed"):
                pv = t["vents"].startswith("Pressure-vacuum")
                if seal_history and tk in vents and day < vents[tk]:
                    pv = False
                rate = W.STANDING["fixed_distillate_pv"] if pv else W.STANDING["fixed_distillate"]
            else:
                has_secondary = "secondary" in t["seal"]
                if seal_history and tk in works and day < works[tk]:
                    has_secondary = False
                rate = W.STANDING["ifr_secondary"] if has_secondary else W.STANDING["ifr_primary"]
            standing += rate * dia
            day = day + D(days=1)
        ml = sum(r_["shore"] for r_ in rec if r_["tank"] == tk and r_["start"].year == 2026) / 1e6
        wrate = W.WORKING["distillate_fixed"] if t["roof"].startswith("Fixed") else W.WORKING["petrol_ifr"]
        out[tk] = standing + wrate * ml
    return out


def compute(target):
    load, per_load, missing = loading(target)
    stack = vru(target)
    gain, parts = stock_account(target)
    tanks = tank_voc(target)
    g = load["G"]
    q = {}
    for qi in range(1, 5):
        q[("VRU-1", qi)] = stack[qi]
        q[("BAY-4", qi)] = g.get((4, qi), 0.0)
        q[("BAY-5", qi)] = g.get((5, qi), 0.0)
    total = sum(q.values())
    monthly = defaultdict(float)
    for pl in per_load:
        l = pl["l"]
        kg = diesel_own(l) + (petrol_pushed(l) if pl["switch"] else 0.0)
        monthly[("BAY-%d" % l["bay"], l["local"].month)] += kg / 1000.0
    rows = R.cems(target)
    # monthly stack figures on the same protocol arithmetic
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
    for r, rate in zip(rows, rates):
        monthly[("VRU-1", W.to_local(r["utc"]).month)] += rate * 0.25 / 1000.0
    return dict(load=load, per_load=per_load, missing=missing, stack=stack, quarters=q, total=total,
                over=total > W.LIMIT_T, excess=total - W.LIMIT_T, gain=gain, parts=parts, tanks=tanks,
                monthly=dict(monthly))
