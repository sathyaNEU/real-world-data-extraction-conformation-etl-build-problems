"""task489: simulate the 2026 world forward and compute the clean truth. Every shipped row is drawn here; the
golden and every rung of the ladder are computed from the rows as they will ship (rounded volumes, logged
cycles, counter readings), so nothing is reverse-engineered."""
import datetime as dt
import math

import numpy as np

import world as W

D = dt.timedelta


def rng(k):
    return np.random.default_rng(W.SEED * 1000 + k)


# ----------------------------------------------------------------------------------------------- the entities
def entities():
    r = rng(1)
    sites, wells, seps, bleeds = [], [], [], []
    ctl_serial = 20400
    for si, (code, area, lsd, x26, sep_spec, bleed_spec) in enumerate(W.SITES):
        lsd_parts = lsd.split("-")
        sec, twp, rge = int(lsd_parts[1]), int(lsd_parts[2]), lsd_parts[3]
        x25 = round(x26 + float(r.uniform(-0.012, 0.012)), 3)
        site = {"code": code, "area": area, "lsd": lsd, "x2026": x26, "x2025": x25, "idx": si,
                "name": "%s %d-%d" % (area, int(lsd_parts[0]), sec), "seps": [], "bleeds": []}
        for k, (grp, model, bore, span, tkg, ratio, auto) in enumerate(sep_spec):
            n = k + 1
            # bottom-hole location of a horizontal well drilled from the pad: an LSD in the section next door
            bh_lsd = int(r.integers(1, 17))
            bh_sec = sec + (1 if sec < 36 and r.random() < 0.6 else -1 if sec > 1 else 1)
            event = "00"
            uwi = "1%02d/%02d-%02d-%03d-%s/%s" % (n - 1, bh_lsd, bh_sec, twp, rge, event)
            wname = "LRL %s %d-%d #%d" % (area.upper(), int(lsd_parts[0]), sec, n)
            lift = "Flowing" if grp == "F" else "Plunger lift"
            w = {"uwi": uwi, "name": wname, "site": code, "n": n, "group": grp, "lift": lift,
                 "plunger": None, "ctl_serial": None, "firmware": None}
            if grp != "F":
                w["plunger"] = str(r.choice(["Conventional pad", "Bypass", "Brush", "Conventional solid"]))
                ctl_serial += int(r.integers(3, 41))
                w["ctl_serial"] = "PCX-%05d" % ctl_serial
                w["firmware"] = str(r.choice(["4.2.1", "4.2.1", "4.3.0"]))
            band = W.band_m3(bore, span)
            sep = {"tag": "V-%s%02d" % (code[1:], n), "lc_tag": "LC-%s%02d" % (code[1:], n), "site": code, "area": area,
                   "uwi": uwi, "well": wname, "group": grp, "model": model, "bore": bore, "span": span,
                   "band": band, "target_kg": tkg, "ratio": ratio, "auto": auto,
                   "kpc": W.kg_per_cycle(model, x26), "serial": "%s-%d" % (model.split("-")[0], int(r.integers(10000, 99999))),
                   "valve": str(r.choice(["1 in", "1 in", "2 in"])) if grp == "F" else str(r.choice(["1 in", "2 in"])),
                   "installed": dt.date(int(r.integers(2014, 2024)), int(r.integers(1, 13)), int(r.integers(1, 28)))}
            wells.append(w)
            seps.append(sep)
            site["seps"].append(sep)
        for tag, model in bleed_spec:
            b = {"site": code, "tag": tag, "model": model, "serial": "%s-%d" % (model.split("-")[0], int(r.integers(10000, 99999))),
                 "kind": W.BLEED_MODELS[model]["kind"], "installed": dt.date(int(r.integers(2013, 2024)), int(r.integers(1, 13)),
                                                                          int(r.integers(1, 28)))}
            bleeds.append(b)
            site["bleeds"].append(b)
        sites.append(site)
    physical(wells, seps)
    return sites, wells, seps, bleeds


TUBING_ID_M = {"60.3 mm": 0.0507, "73.0 mm": 0.0620}     # internal diameter of the production tubing
SEAM_IN = {20: 90, 24: 90, 30: 120, 36: 120, 42: 120, 48: 150}


def physical(wells, seps):
    """The facts the register keeps about each vessel and well: the level controller's lower setting and the high
    level shutdown above the bottom seam, the dump valve body, each well's tubing and, on a plunger well, the plunger's
    depth and the controller's own settings (median arrival speed, afterflow mode)."""
    r = rng(21)
    for sep, w in zip(seps, wells):
        sep["low_in"] = int(r.integers(8, 17))
        sep["lshh_in"] = int(round(SEAM_IN[sep["bore"]] * float(r.uniform(0.74, 0.82))))
        if sep["group"] != "F":
            sep["valve"] = "1 in"
        elif sep["target_kg"] / sep["kpc"] * sep["band"] / 8760.0 > 0.3:
            sep["valve"] = "2 in"
        w["tubing"] = "60.3 mm" if r.random() < (0.7 if sep["group"] != "F" else 0.4) else "73.0 mm"
        if sep["group"] == "F":
            w["depth_m"] = None
            continue
        w["depth_m"] = int(r.integers(2450, 3351))
        w["mode"] = "timer" if r.random() < 0.55 else "pressure"
        w["v_med"] = float(r.uniform(2.6, 4.2) if sep["group"] == "PB" else r.uniform(3.4, 5.4))
        w["v_sd"] = float(r.uniform(0.10, 0.20))


# ----------------------------------------------------------------------------------------------- daily volumes
def season(d):
    return 1.0 + 0.10 * math.cos(2 * math.pi * (d - 20) / 365.0)


def shut_ins(r):
    """Whole shut-in days and partial days for one well: a list of hours on, one per production day."""
    hours = np.full(365, 24.0)
    for _ in range(int(r.integers(0, 4))):
        start = int(r.integers(5, 350))
        length = int(r.integers(1, 6))
        hours[start:start + length] = 0.0
        if start > 0 and hours[start - 1] == 24.0:
            hours[start - 1] = float(r.integers(5, 21))
        if start + length < 365:
            hours[start + length] = float(r.integers(4, 20))
    return hours


def donor_hours(hours, off):
    """Take a donor well's hours off for the span it stood without a plunger controller."""
    tm, tb = off
    h = hours.copy()
    for d, day in enumerate(W.DAYS):
        s, e = W.production_day_bounds_utc(day)
        lo, hi = max(s, tm), min(e, tb)
        if hi > lo:
            gone = (hi - lo).total_seconds() / 3600.0 * 24.0 / ((e - s).total_seconds() / 3600.0)
            h[d] = max(0.0, float(math.floor(min(h[d], 24.0 - gone))))
    return h


def simulate():
    sites, wells, seps, bleeds = entities()
    spans, donor_off = unit_plan(seps, wells)
    prod = {}            # uwi -> dict of arrays (gas e3m3, cond m3, water m3, hours)
    plan = {}            # uwi -> per-day arrivals and non-arrivals for plunger wells
    true_liq = {}        # uwi -> the liquid the separator actually received each day (m3), unrounded
    for sep, w in zip(seps, wells):
        rr = rng(100 + len(prod))
        hours = shut_ins(rr)
        if sep["uwi"] in donor_off:
            hours = donor_hours(hours, donor_off[sep["uwi"]])
        on = hours / 24.0
        f = np.array([season(d) * (1.0 + float(rr.normal(0, 0.05))) for d in range(365)])
        f = np.clip(f, 0.75, 1.3)
        gas_base = float(rr.uniform(18, 160))
        gas = np.round(gas_base * f * on, 1)
        water_share = float(rr.uniform(0.25, 0.85))
        if sep["group"] == "F":
            dumps_target = sep["target_kg"] / sep["kpc"]
            liq_annual = dumps_target * sep["band"]
            weights = f * on
            liq = liq_annual * weights / weights.sum()
            arrivals = nonarr = None
        else:
            cyc_target = sep["target_kg"] / sep["kpc"]
            weights = np.clip(f * on * (1 + rr.normal(0, 0.04, 365)), 0, None)
            raw = cyc_target * weights / weights.sum()
            arrivals = np.floor(raw + rr.random(365)).astype(int)
            arrivals[on == 0] = 0
            if sep["group"] == "PB":
                ratio = np.clip(sep["ratio"] * (1 + rr.normal(0, 0.12, 365)), 1.6, 4.6)
            else:
                ratio = np.clip(sep["ratio"] * (1 + rr.normal(0, 0.18, 365)), 0.012, 0.06)
            liq = arrivals * ratio * sep["band"]
            share_na = float(rr.uniform(0.02, 0.09))
            nonarr = rr.binomial(np.maximum(arrivals, 0), share_na)
        ws = np.clip(water_share + rr.normal(0, 0.03, 365), 0.05, 0.95)
        cond = np.round(liq * (1 - ws), 1)
        water = np.round(liq * ws, 1)
        # a plunger well's volumes are allocated to the tenth of a cubic metre; keep each day's slug inside its regime
        if sep["group"] != "F":
            for d in range(365):
                if arrivals[d] == 0:
                    cond[d] = water[d] = 0.0
                    continue
                tot = cond[d] + water[d]
                slug = tot / arrivals[d]
                if sep["group"] == "PB" and slug < 1.5 * sep["band"]:
                    need = math.ceil(1.5 * sep["band"] * arrivals[d] * 10 - 1e-9) / 10.0
                    water[d] = round(need - cond[d], 1)
                if sep["group"] == "PS" and slug > 0.065 * sep["band"]:
                    cap = math.floor(0.065 * sep["band"] * arrivals[d] * 10 + 1e-9) / 10.0
                    cond[d] = round(min(cond[d], cap), 1)
                    water[d] = round(max(cap - cond[d], 0.0), 1)
        prod[sep["uwi"]] = {"gas": gas, "cond": cond, "water": water, "hours": hours}
        if sep["group"] == "F":
            bias = float(rr.uniform(-0.016, 0.016))
            true_liq[sep["uwi"]] = (cond + water) * (1 + bias + rr.normal(0, 0.02, 365))
        else:
            plan[sep["uwi"]] = {"arrivals": arrivals, "nonarr": nonarr}
    cycles, aborted = make_cycles(seps, wells, prod, plan, spans)
    counters = make_counters(seps, prod, true_liq)
    world = {"sites": sites, "wells": wells, "seps": seps, "bleeds": bleeds, "prod": prod, "plan": plan,
             "cycles": cycles, "aborted": aborted, "counters": counters, "true_liq": true_liq, "spans": spans,
             "donor_off": donor_off}
    world["orders"], world["bleed_hist"] = make_bleed_history(world)
    world["survey"] = make_survey(world)
    world["ppa"], world["runs"] = make_adjustments(world)
    return world


# ----------------------------------------------------------------------------------------------- plunger cycles
def local_naive(t_utc):
    return t_utc.astimezone(W.TZ).replace(tzinfo=None)


def local_dt(tup):
    return dt.datetime(*tup, tzinfo=W.TZ)


def unit_plan(seps, wells):
    """For every plunger well, the controller units that ran it in 2026 and the host label each unit's data
    carried: a list of (from_utc, to_utc, serial, label) spans, plus the donor shut-in spans."""
    by = {(s["site"], int(s["tag"][-2:]) - 1): (s, w) for s, w in zip(seps, wells)}
    spans = {s["uwi"]: [(W.WINDOW_START_UTC - D(days=2), W.WINDOW_END_UTC + D(days=2), w["ctl_serial"], w["name"])]
             for s, w in zip(seps, wells) if s["group"] != "F"}
    donor_off = {}
    new_serial = 31700
    for (dsite, di), (rsite, ri), moved, fixed, back in W.MOVES:
        dsep, dwell = by[(dsite, di)]
        rsep, rwell = by[(rsite, ri)]
        tm, tf, tb = local_dt(moved).astimezone(W.UTC), local_dt(fixed).astimezone(W.UTC), local_dt(back).astimezone(W.UTC)
        a0, a1, ser_d, lab_d = spans[dsep["uwi"]][0]
        new_serial += 113
        spans[dsep["uwi"]] = [(a0, tm, ser_d, lab_d), (tb, a1, "PCX-%05d" % new_serial, lab_d)]
        donor_off[dsep["uwi"]] = (tm, tb)
        b0, b1, ser_r, lab_r = spans[rsep["uwi"]][0]
        spans[rsep["uwi"]] = [(b0, tm, ser_r, lab_r), (tm, tf, ser_d, lab_d), (tf, b1, ser_d, lab_r)]
    return spans, donor_off


def make_cycles(seps, wells, prod, plan, spans):
    """One row per cycle a plunger controller ran: the unit's serial, the host's well label for that unit, the
    unit's own cycle number, open time, travel seconds (blank when the plunger did not arrive), result,
    afterflow, casing and tubing pressure at open, and the time the host received the row. Each well's cycles run
    in turn: travel, then afterflow, then the off time to the next opening; travel is the plunger's depth over its
    speed, which varies about the well's median and rises with casing pressure; afterflow is the well's timer or,
    in casing pressure mode, ends when the casing falls to its close set point."""
    out = []
    aborted = []
    counters = {}
    arr_ctr = {}
    for j, (sep, w) in enumerate(zip(seps, wells)):
        if sep["group"] == "F":
            continue
        rr = rng(500 + j)
        ra = rng(1500 + j)
        abort_p = float(rng(700 + j).uniform(*W.ABORT_SHARE))
        p = plan[sep["uwi"]]
        hours = prod[sep["uwi"]]["hours"]
        casing0 = float(rr.uniform(1900, 3600))
        n_max = max(int(p["arrivals"][d]) + int(p["nonarr"][d]) for d in range(365))
        spacing_min = 0.7 * 86400.0 / max(n_max, 1)
        # a well that cycles often runs a light, fast plunger: its median trip takes under half the shortest spacing
        w["v_med"] = max(w["v_med"], w["depth_m"] / (0.5 * spacing_min))
        v_floor = 2.1 if sep["group"] == "PB" else 1.9
        w["travel_timer_s"] = int(math.ceil(w["depth_m"] / v_floor / 60.0) * 60)
        af_room = (spacing_min - w["depth_m"] / w["v_med"] - 150.0) / 60.0
        w["af_set"] = int(max(2, min(45, round(af_room * float(ra.uniform(0.35, 0.65))))))
        rows_w = []
        for d in range(-1, 365):
            # production day 2025-12-31 runs to 08:00 on 1 January and sits in the controllers' 2026 log too
            day = W.DAYS[0] - D(days=1) if d < 0 else W.DAYS[d]
            dd = max(d, 0)
            n_arr, n_na = int(p["arrivals"][dd]), int(p["nonarr"][dd])
            n = n_arr + n_na
            if n == 0 or (d < 0 and hours[0] < 24.0):
                continue
            s_utc, e_utc = W.production_day_bounds_utc(day)
            span_s = (e_utc - s_utc).total_seconds() * min(hours[dd], 24.0) / 24.0
            if hours[dd] < 24.0 and d > 0 and hours[d - 1] == 0.0:
                start = e_utc - D(seconds=span_s)      # the well came back on during the day
            else:
                start = s_utc
            kinds = np.array([1] * n_arr + [0] * n_na)
            rr.shuffle(kinds)
            gap = span_s / n
            for i in range(n):
                u = float(rr.uniform(0.05, 0.85))
                t = start + D(seconds=gap * (i + 0.35 + 0.3 * (u - 0.05) / 0.8))
                t = t.replace(microsecond=0)
                arrived = bool(kinds[i])
                if arrived:                    # the plan's own draws, kept so every cycle stays where it was planned
                    rr.integers(240, 1500)
                    rr.integers(4, 45)
                casing = round(casing0 * (1 + float(rr.normal(0, 0.035))), 0)
                tubing = round(casing * float(rr.uniform(0.55, 0.85)), 0)
                serial, label = next((s3, l3) for a, b, s3, l3 in spans[sep["uwi"]] if a <= t < b)
                if serial not in counters:
                    counters[serial] = int(rng(800 + int(serial[-5:])).integers(20000, 90000))
                elif (rr.random() < abort_p and clear_of_edges(t, spans[sep["uwi"]])
                      and clear_of_edges(t - D(seconds=int(gap * 0.4)), spans[sep["uwi"]])):
                    # an opening closed again on the line pressure interlock: counted, never sent to the host
                    counters[serial] += 1
                    aborted.append({"serial": serial, "uwi": sep["uwi"], "cycle_no": counters[serial],
                                    "near_utc": t - D(seconds=int(gap * 0.4))})
                counters[serial] += 1
                if serial not in arr_ctr:
                    arr_ctr[serial] = int(rng(900 + int(serial[-5:])).integers(10000, 60000))
                if arrived:
                    arr_ctr[serial] += 1
                extra = int(rr.integers(20, 75))
                lag = int(rr.integers(4, 95))
                v = w["v_med"] * math.exp(w["v_sd"] * float(ra.normal(0, 1))) * (casing / casing0) ** 0.6
                v = max(v, v_floor * 1.03)
                travel = int(round(w["depth_m"] / v)) if arrived else None
                if w["mode"] == "timer":
                    af = w["af_set"]
                else:
                    af = max(1, int(round(w["af_set"] * math.exp(0.35 * float(ra.normal(0, 1))))))
                rows_w.append({"serial": serial, "label": label, "cycle_no": counters[serial],
                               "arrival_no": arr_ctr[serial], "open_utc": t, "travel_s": travel,
                               "result": "ARRIVE" if arrived else "NO ARRIVAL", "afterflow_min": af if arrived else 0,
                               "casing_kpa": int(casing), "tubing_kpa": int(tubing), "uwi": sep["uwi"], "recv_utc": None,
                               "resent": False, "_extra": extra, "_lag": lag})
        # the cycles run in turn: afterflow ends, and a missed plunger's travel timer runs out, before the next opening
        rows_w.sort(key=lambda c: c["open_utc"])
        for k, c in enumerate(rows_w):
            nxt = rows_w[k + 1]["open_utc"] if k + 1 < len(rows_w) else c["open_utc"] + D(hours=6)
            room = (nxt - c["open_utc"]).total_seconds() - 90.0 - c["_extra"]
            if c["result"] == "ARRIVE":
                c["travel_s"] = int(max(min(c["travel_s"], room - 60.0), w["depth_m"] / 9.0))
                c["afterflow_min"] = int(max(0, min(c["afterflow_min"], (room - c["travel_s"]) // 60)))
                busy = c["travel_s"] + c["afterflow_min"] * 60
            else:
                busy = min(w["travel_timer_s"], max(room, 60.0))
            close = c["open_utc"] + D(seconds=busy + c.pop("_extra"))
            c["recv_utc"] = close + D(seconds=c.pop("_lag"))
        out.extend(rows_w)
    # radio outages: rows queued in the controller reach the host at reconnection, and the overnight backfill
    # loads the same rows again
    by = {(s["site"], int(s["tag"][-2:]) - 1): s for s in seps}
    extra = []
    for (site, idx), start, hrs in W.OUTAGES:
        sep = by[(site, idx)]
        t0 = local_dt(start).astimezone(W.UTC)
        t1 = t0 + D(hours=hrs)
        nightly = (t1.astimezone(W.TZ) + D(days=1)).replace(hour=2, minute=14, second=0, tzinfo=None)
        nightly = dt.datetime(nightly.year, nightly.month, nightly.day, 2, 14, tzinfo=W.TZ).astimezone(W.UTC)
        for c in out:
            if c["uwi"] == sep["uwi"] and t0 <= c["open_utc"] < t1:
                c["recv_utc"] = t1 + D(seconds=int((c["open_utc"] - t0).total_seconds() // 600))
                dup = dict(c)
                dup["recv_utc"] = nightly + D(seconds=int((c["open_utc"] - t0).total_seconds() // 900))
                dup["resent"] = True
                extra.append(dup)
    out.extend(extra)
    out.sort(key=lambda c: (c["recv_utc"], c["serial"], c["cycle_no"]))
    return out, aborted


def clear_of_edges(t, spans):
    """An aborted opening is drawn only where its well and production day are beyond doubt: three hours or more
    from the reporting year's ends and from any change of controller unit on the well."""
    edges = [W.WINDOW_START_UTC, W.WINDOW_END_UTC] + [a for a, b, s3, l3 in spans] + [b for a, b, s3, l3 in spans]
    return all(abs((t - e).total_seconds()) > 3 * 3600 for e in edges)


# ----------------------------------------------------------------------------------------------- dump counters
def make_counters(seps, prod, true_liq):
    """Hourly historian samples of each automated separator's dump counter (16-bit, wraps at 65,536)."""
    out = {}
    t0 = W.WINDOW_START_UTC - D(hours=40)
    t1 = W.WINDOW_END_UTC + D(hours=30)
    for sep in seps:
        if not sep["auto"]:
            continue
        rr = rng(900 + len(out))
        liq = true_liq[sep["uwi"]]
        hours_on = prod[sep["uwi"]]["hours"]
        level = float(rr.uniform(0, sep["band"]))
        count = int(rr.integers(1000, 60000))
        rows = []
        t = t0
        while t <= t1:
            # the liquid arriving this hour, from the production day it falls in
            day = local_naive(t - D(hours=W.PROD_DAY_HOUR)).date()
            d = (day - W.DAYS[0]).days
            if 0 <= d < 365:
                rate = liq[d] / max(hours_on[d], 1e-9) if hours_on[d] > 0 else 0.0
                lday = local_naive(t)
                # off-hours sit at the end of a partially shut-in day
                on_frac = 1.0 if hours_on[d] >= 24 else (1.0 if (lday.hour - W.PROD_DAY_HOUR) % 24 < hours_on[d] else 0.0)
                inflow = rate * on_frac
            else:
                inflow = float(np.mean(liq[:5] if d < 0 else liq[-5:])) / 24.0
            level += inflow
            while level >= sep["band"]:
                level -= sep["band"]
                count += 1
            rows.append((t, count % 65536))
            t += D(hours=1)
        out[sep["uwi"]] = rows
    return out


# ----------------------------------------------------------------------------------------------- bleed devices
def make_bleed_history(wd):
    """Work orders for 2026 and each continuous-bleed device's in-service hours and rate basis. Returns
    (orders, history) where history maps (site, serial) to the device's 2026 record."""
    r = rng(3)
    orders = []
    hist = {}
    ystart = dt.datetime(2026, 1, 1, 8)
    yend = dt.datetime(2027, 1, 1, 8)
    for b in wd["bleeds"]:
        hist[(b["site"], b["serial"])] = {"site": b["site"], "tag": b["tag"], "model": b["model"], "serial": b["serial"],
                                          "from": ystart, "to": yend, "kind": b["kind"], "off_h": 0.0, "removed": False}
    wo = 260410

    def add(created, site, tag, wtype, text, tech):
        nonlocal wo
        wo += int(r.integers(7, 60))
        orders.append({"wo": "WO-%d" % wo, "created": created, "site": site, "tag": tag, "type": wtype, "text": text,
                       "tech": tech, "status": "Closed"})
    techs = ["G. Ward", "L. Rollins", "J. Castillo", "B. Phillips", "D. Thompson"]
    # a pressure controller replaced with another maker's model (the register keeps only the new one)
    swaps = [("K0702", "PC-1", "PC-60", dt.datetime(2026, 8, 14, 13, 20)),
             ("E1032", "PC-1", "PC-60", dt.datetime(2026, 4, 22, 10, 5))]
    for site, tag, new_model, when in swaps:
        old = next(b for b in wd["bleeds"] if b["site"] == site and b["tag"] == tag)
        h = hist[(site, old["serial"])]
        h["to"] = when
        new_serial = "%s-%d" % (new_model.split("-")[0], int(r.integers(10000, 99999)))
        hist[(site, new_serial)] = {"site": site, "tag": tag, "model": new_model, "serial": new_serial, "from": when,
                                   "to": yend, "kind": "PC", "off_h": 0.0, "removed": False}
        add(when - D(days=int(r.integers(2, 9))), site, tag, "Corrective",
            "Sales PC hunting. Replaced controller %s at %s with %s %s s/n %s, old unit s/n %s returned to Grande Prairie shop"
            % (when.strftime("%b %d"), when.strftime("%H:%M"), W.MAKERS[W.BLEED_MODELS[new_model]["maker"]], new_model,
               new_serial, old["serial"]), techs[int(r.integers(0, 5))])
    # a line heater taken out of service: its bath controller leaves the register
    for (site, tag, out_t), (site2, tag2, in_t) in W.RELOCATED:
        b = next(b for b in wd["bleeds"] if b["site"] == site and b["tag"] == tag)
        h = hist[(site, b["serial"])]
        h["to"] = dt.datetime(*out_t)
        h["removed"] = True
        hist[(site2, b["serial"])] = {"site": site2, "tag": tag2, "model": b["model"], "serial": b["serial"],
                                      "from": dt.datetime(*in_t), "to": yend, "kind": "TC", "off_h": 0.0, "removed": False}
        pad = {s["code"]: s["name"] for s in wd["sites"]}
        add(dt.datetime(*out_t) - D(days=int(r.integers(1, 6))), site, tag, "Decommission",
            "Line heater no longer required on this pad. Isolated fuel and instrument supply %s at %s, heater package incl. "
            "bath TC s/n %s pulled for reuse" % (dt.datetime(*out_t).strftime("%b %d"), dt.datetime(*out_t).strftime("%H:%M"),
                                                 b["serial"]), techs[int(r.integers(0, 5))])
        add(dt.datetime(*in_t) - D(days=int(r.integers(1, 4))), site2, tag2, "Project",
            "Set refurbished line heater (ex %s) on second well, bath TC s/n %s, fuel and instrument supply tied in and on "
            "%s at %s" % (pad[site], b["serial"], dt.datetime(*in_t).strftime("%b %d"), dt.datetime(*in_t).strftime("%H:%M")),
            "Northline Fab crew")
    # turnarounds: the site depressured, so supply gas was off
    depres = [("K1122", dt.datetime(2026, 6, 2, 9, 0), 5 * 24 + 7), ("E0617", dt.datetime(2026, 9, 15, 7, 30), 3 * 24 + 2)]
    for site, when, hrs in depres:
        for b in wd["bleeds"]:
            if b["site"] == site:
                hist[(site, b["serial"])]["off_h"] += hrs
        add(when - D(days=3), site, "", "Turnaround",
            "Pad turnaround, site depressured and instrument supply isolated %s to %s" % (
                when.strftime("%b %d %H:%M"), (when + D(hours=hrs)).strftime("%b %d %H:%M")), techs[int(r.integers(0, 5))])
    # plunger controller units moved between wells, and the donors' new units
    by = {(s["site"], int(s["tag"][-2:]) - 1): (s, w) for s, w in zip(wd["seps"], wd["wells"])}
    for (dsite, di), (rsite, ri), moved, fixed, back in W.MOVES:
        dsep, dwell = by[(dsite, di)]
        rsep, rwell = by[(rsite, ri)]
        ser_d = dwell["ctl_serial"]
        new = next(sp[2] for sp in wd["spans"][dsep["uwi"]] if sp[2] != ser_d)
        tm = dt.datetime(*moved)
        tb = dt.datetime(*back)
        add(tm - D(minutes=int(r.integers(30, 200))), rsite, rsep["lc_tag"].replace("LC", "PLC"), "Corrective",
            "Plunger controller dead on %s (no display, no comms). Pulled controller s/n %s off %s and had it running "
            "here at %s to keep the well cycling. %s shut in until a replacement controller arrives." % (
                rwell["name"], ser_d, dwell["name"], tm.strftime("%H:%M"), dwell["name"]), techs[int(r.integers(0, 5))])
        add(tb - D(hours=int(r.integers(2, 20))), dsite, dsep["lc_tag"].replace("LC", "PLC"), "Corrective",
            "Installed new plunger controller s/n %s on %s at %s, timers set from old unit's settings, well back on "
            "production" % (new, dwell["name"], tb.strftime("%H:%M")), techs[int(r.integers(0, 5))])
    for site, done in W.RETAGGED:
        when = dt.datetime(*done, 16, 30)
        add(when - D(days=int(r.integers(10, 25))), site, "", "Project",
            "Re-pipe of sales and fuel gas headers per P&ID rev D, sales PCs relocated to the new header", "Northline Fab crew")
    # routine work on the pads' other equipment, each job on the kind of tag it belongs to; planned work on day
    # shift, corrective work mostly on day shift with call-outs at night and at weekends
    r2 = rng(33)
    jobs = {
        "V": [("Preventive", "Annual PSV test, all set points OK"), ("Corrective", "Cleaned sand from separator"),
              ("Preventive", "Tested high level shutdown, tripped and reset OK"), ("Corrective", "Painted separator skid"),
              ("Corrective", "Replaced sight glass gaskets, weeping at bottom cock")],
        "LC": [("Corrective", "Changed out dump valve trim, LLC re-zeroed"),
               ("Preventive", "LLC pilot cleaned, stroked through span"),
               ("Corrective", "Dump valve stem packing weeping, repacked")],
        "PLC": [("Corrective", "Replaced battery in plunger controller"), ("Preventive", "Cleaned solar panel, charging OK"),
                ("Preventive", "Plunger inspected, within wear limits, returned to service"),
                ("Corrective", "Lubricator spring replaced"), ("Corrective", "Arrival sensor cable chafed, re-routed and tested")],
        "FE": [("Preventive", "Calibrated sales meter, no change"), ("Preventive", "Orifice plate inspected, no change")],
        "H": [("Preventive", "Line heater fire tube inspected"), ("Corrective", "Line heater pilot out, relit")],
        "PCV": [("Corrective", "Replaced instrument supply regulator, set 241 kPa")],
    }
    wo2 = [wo + 900]

    def shift_time(day, wtype):
        if wtype == "Preventive" or r2.random() < 0.78:
            while day.weekday() >= 5:
                day = day + D(days=1)
            return dt.datetime.combine(day, dt.time(7, 0)) + D(minutes=int(r2.integers(0, 10 * 60)))
        return dt.datetime.combine(day, dt.time(0, 0)) + D(minutes=int(r2.choice([int(r2.integers(0, 6 * 60)),
                                                                                   int(r2.integers(18 * 60, 24 * 60))])))
    heater_sites = {b["site"] for b in wd["bleeds"] if b["kind"] == "TC"}
    for _ in range(118):
        s = wd["sites"][int(r2.integers(0, len(wd["sites"])))]
        sep = s["seps"][int(r2.integers(0, len(s["seps"])))]
        kinds = ["V", "V", "LC", "LC", "FE", "PCV"] + (["PLC", "PLC", "PLC"] if sep["group"] != "F" else []) + \
                (["H"] if s["code"] in heater_sites else [])
        kind = kinds[int(r2.integers(0, len(kinds)))]
        wtype, text = jobs[kind][int(r2.integers(0, len(jobs[kind])))]
        tag = {"V": sep["tag"], "LC": sep["lc_tag"], "PLC": sep["lc_tag"].replace("LC", "PLC"),
               "FE": "FE-%s1" % s["code"][1:], "H": "H-%s1" % s["code"][1:], "PCV": "PCV-%s1" % s["code"][1:]}[kind]
        day = dt.date(2026, 1, 2) + D(days=int(r2.integers(0, 360)))
        wo2[0] += int(r2.integers(3, 41))
        status = "Closed" if r2.random() < 0.88 else ("Completed" if r2.random() < 0.75 else "Cancelled")
        orders.append({"wo": "WO-%d" % wo2[0], "created": shift_time(day, wtype), "site": s["code"], "tag": tag,
                       "type": wtype, "text": text, "tech": techs[int(r2.integers(0, 5))], "status": status})
    orders.sort(key=lambda o: o["created"])
    return orders, hist


def bleed_hours(h):
    return (h["to"] - h["from"]).total_seconds() / 3600.0 - h["off_h"]


# ----------------------------------------------------------------------------------------------- the survey
def make_survey(wd):
    """Sheldrake's spring 2026 survey: an hour on each tested level controller (dump cycles seen, gas vented)
    and a steady-state reading on each tested bleed device."""
    r = rng(4)
    lcs = []
    by_code = {s["code"]: s for s in wd["sites"]}
    day0 = dt.date(2026, 5, 25)
    for i, (code, k) in enumerate(W.CAMPAIGN_LCS):
        sep = by_code[code]["seps"][k]
        d = (day0 - W.DAYS[0]).days + i // 3
        liq = wd["prod"][sep["uwi"]]["cond"][d] + wd["prod"][sep["uwi"]]["water"][d]
        hrs = max(wd["prod"][sep["uwi"]]["hours"][d], 1.0)
        mean = liq / sep["band"] / hrs
        seen = max(int(r.poisson(mean)), 0)
        per = W.LC_MODELS[sep["model"]]["scf_per_cycle"] * float(r.uniform(0.965, 1.035))
        lcs.append({"date": day0 + D(days=i // 3), "site": code, "tag": sep["lc_tag"], "serial": sep["serial"],
                    "model": sep["model"], "minutes": 60, "cycles": seen, "scf": round(seen * per, 2)})
    bl = []
    # the bleed devices measured; tags are the field tags painted on the devices at the time
    tested = [("K0309", "PC-1"), ("K1122", "PC-1"), ("K1623", "PC-1"), ("E0503", "PC-1"), ("E0617", "TC-1"),
              ("K0702", "PC-1"), ("E1032", "PC-1"), ("E0718", "TC-1"), ("E1424", "PC-1"), ("K1416", "TC-1"),
              ("E0934", "TC-1"), ("E1322", "PC-1")]
    mult = [0.92, 1.4, 1.9, 2.62, 1.1, 3.1, 1.65, 2.2, 1.25, 2.85, 1.05, 1.78]
    rb = rng(41)
    for j, (code, tag) in enumerate(tested):
        when = dt.datetime.combine(day0 + D(days=j // 3), dt.time(11, 0))
        b = next(h for h in wd["bleed_hist"].values() if h["site"] == code and h["tag"] == tag and h["from"] <= when < h["to"])
        rated = W.BLEED_MODELS[b["model"]]["scf_per_h"]
        meas = round(rated * mult[j] * float(rb.uniform(0.96, 1.04)), 2)
        bl.append({"date": when.date(), "site": code, "tag": tag, "serial": b["serial"], "model": b["model"],
                   "scf_h": meas})
    return {"lcs": lcs, "bleeds": bl}


# ----------------------------------------------------------------------------------------------- adjustments
def make_adjustments(wd):
    """Allocation runs (one original run per production month, re-runs where volumes changed) and the
    volumetric adjustment journal that posts each re-run's gas differences by posting date."""
    r = rng(5)
    runs = []
    rid = 1458
    month_runs = {}
    for m in list(range(1, 13)) + [12]:
        pass
    months = [(2025, 12)] + [(2026, m) for m in range(1, 13)]
    for (y, m) in months:
        rid += int(r.integers(1, 4))
        close = dt.date(y + (1 if m == 12 else 0), 1 if m == 12 else m + 1, int(r.integers(14, 20)))
        runs.append({"run": "AR-%06d" % rid, "prod_month": "%04d-%02d" % (y, m), "run_date": close, "kind": "Original"})
        month_runs[(y, m)] = "AR-%06d" % rid
    ppa = []
    jno = 88310
    # re-runs: a meter correction for three 2026 months at two sites, a December 2025 fix posted in January 2026,
    # and a November and December 2026 fix posted in January 2027
    cases = [((2025, 12), dt.date(2026, 1, 28), ["K1623", "E0503"], "Orifice plate bore entered as 2.000 in, field plate 2.250 in"),
             ((2026, 7), dt.date(2026, 10, 21), ["E1215", "K0835"], "Chart integration error, re-run on corrected differential"),
             ((2026, 8), dt.date(2026, 10, 21), ["E1215", "K0835"], "Chart integration error, re-run on corrected differential"),
             ((2026, 9), dt.date(2026, 10, 22), ["E1215"], "Chart integration error, re-run on corrected differential"),
             ((2026, 11), dt.date(2027, 1, 19), ["K0114", "E0934", "K1312"], "Sales meter flow computer clock fault, volumes re-run"),
             ((2026, 12), dt.date(2027, 1, 20), ["K0114", "E0934"], "Sales meter flow computer clock fault, volumes re-run")]
    for (y, m), posted, codes, why in cases:
        rid += int(r.integers(1, 3))
        rr_id = "AR-%06d" % rid
        runs.append({"run": rr_id, "prod_month": "%04d-%02d" % (y, m), "run_date": posted - D(days=2), "kind": "Re-run"})
        for code in codes:
            site = next((s for s in wd["sites"] if s["code"] == code), None)
            if site is None:
                continue
            for sep in site["seps"]:
                if (y, m) == (2025, 12):
                    base = float(np.mean(wd["prod"][sep["uwi"]]["gas"][:10])) * 31
                else:
                    idx = [i for i, d in enumerate(W.DAYS) if (d.year, d.month) == (y, m)]
                    base = float(wd["prod"][sep["uwi"]]["gas"][idx].sum())
                frac = float(r.uniform(0.035, 0.11)) * (1 if r.random() < 0.8 else -1)
                jno += int(r.integers(1, 9))
                ppa.append({"journal": "VJ-%d" % jno, "posted": posted, "run": rr_id, "uwi": sep["uwi"], "product": "GAS",
                            "vol": round(base * frac, 1), "text": why})
    # a posting and its reversal (keyed to the wrong well, reversed the same week)
    s0 = wd["sites"][5]["seps"][0]
    jno += 4
    ppa.append({"journal": "VJ-%d" % jno, "posted": dt.date(2026, 10, 21), "run": runs[-4]["run"], "uwi": s0["uwi"],
                "product": "GAS", "vol": 41.7, "text": "Chart integration error, re-run on corrected differential"})
    ppa.append({"journal": "VJ-%d" % (jno + 6), "posted": dt.date(2026, 10, 27), "run": runs[-4]["run"], "uwi": s0["uwi"],
                "product": "GAS", "vol": -41.7, "text": "Reverse VJ-%d, posted to wrong well" % jno})
    ppa.sort(key=lambda p: (p["posted"], p["journal"]))
    return ppa, runs


# ----------------------------------------------------------------------------------------------- the truth
def window_cycles(wd, uwi):
    """Logged cycles of one well inside the 2026 production days, true wells only (no re-sends)."""
    return [c for c in wd["cycles"] if c["uwi"] == uwi and not c["resent"]
            and W.WINDOW_START_UTC <= c["open_utc"] < W.WINDOW_END_UTC]


def counter_dumps(rows):
    a = next(v for t, v in rows if t == W.WINDOW_START_UTC)
    b = next(v for t, v in rows if t == W.WINDOW_END_UTC)
    total = 0
    prev = None
    for t, v in rows:
        if t < W.WINDOW_START_UTC or t > W.WINDOW_END_UTC:
            continue
        if prev is not None:
            total += (v - prev) % 65536
        prev = v
    assert (b - a) % 65536 == total % 65536
    return total


def dumps_by_route(wd, sep):
    """Dump cycles for one level controller under every route on the ladder."""
    p = wd["prod"][sep["uwi"]]
    liq = p["cond"] + p["water"]
    vol = float(liq.sum()) / sep["band"]
    cond_only = float(p["cond"].sum()) / sep["band"]
    out = {"volume": vol, "cond_only": cond_only}
    if sep["auto"]:
        out["counter"] = counter_dumps(wd["counters"][sep["uwi"]])
    if sep["group"] == "F":
        out["arrivals"] = None
        out["golden"] = out.get("counter", vol)
        out["min_rule"] = out["golden"]
        out["ceil_rule"] = out["golden"]
        return out
    cyc = window_cycles(wd, sep["uwi"])
    arr = [c for c in cyc if c["result"] == "ARRIVE"]
    out["arrivals"] = len(arr)
    # the level, arrival by arrival: each arrival brings that production day's liquid shared over its arrivals
    by_day = {}
    for c in arr:
        day = local_naive(c["open_utc"] - D(hours=W.PROD_DAY_HOUR)).date()
        by_day.setdefault(day, []).append(c)
    lvl, n = 0.0, 0
    mn = 0.0
    ce = 0.0
    for d, day in enumerate(W.DAYS):
        a = len(by_day.get(day, []))
        if a == 0:
            continue
        s = float(liq[d]) / a
        for _ in range(a):
            lvl += s
            if lvl >= sep["band"] - 1e-12:
                n += 1
                lvl = 0.0
        mn += min(a, float(liq[d]) / sep["band"])
        ce += a / max(math.ceil(sep["band"] / s - 1e-12), 1) if s > 0 else 0.0
    out["golden"] = n
    out["min_rule"] = mn
    out["ceil_rule"] = ce
    return out


def truth(wd):
    """Per controller and per site: dumps and methane under every route; the golden set and every route's set."""
    camp = wd["survey"]["lcs"]
    ef_scf_h = sum(c["scf"] for c in camp) / sum(c["minutes"] for c in camp) * 60.0
    lc = []
    for sep in wd["seps"]:
        site = next(s for s in wd["sites"] if s["code"] == sep["site"])
        dr = dumps_by_route(wd, sep)
        k = sep["kpc"]
        row = {"sep": sep, "x": site["x2026"], "dumps": dr, "kg": {}}
        for key in ("golden", "volume", "cond_only", "min_rule", "ceil_rule"):
            row["kg"][key] = dr[key] * k
        if sep["auto"]:
            row["kg"]["volume_noctr"] = dr["volume"] * k
        row["kg"]["label"] = (dr["arrivals"] if dr["arrivals"] is not None else dr.get("counter", dr["volume"])) * k
        row["kg"]["max_route"] = max(row["kg"]["label"], (dr.get("counter", dr["volume"])) * k)
        row["kg"]["r1"] = dr.get("counter", dr["volume"]) * k
        row["kg"]["ps_volume"] = (dr.get("counter", dr["volume"]) if sep["group"] != "PB" else dr["golden"]) * k
        row["kg"]["ef"] = ef_scf_h * 8760 * W.SCF_TO_M3 * site["x2026"] * W.CH4_KG_PER_M3
        hours = float(wd["prod"][sep["uwi"]]["hours"].sum())
        row["kg"]["ef_hours"] = ef_scf_h * hours * W.SCF_TO_M3 * site["x2026"] * W.CH4_KG_PER_M3
        lc.append(row)
    routes = ["golden", "r1", "label", "max_route", "ef", "ef_hours", "cond_only", "min_rule", "ceil_rule", "ps_volume"]
    site_t = {}
    for s in wd["sites"]:
        rows = [x for x in lc if x["sep"]["site"] == s["code"]]
        site_t[s["code"]] = {k: sum(x["kg"][k] for x in rows) / 1000.0 for k in routes}
    sets = {k: sorted(c for c, v in site_t.items() if v[k] > W.LINE_T) for k in routes}
    return {"lc": lc, "site_t": site_t, "sets": sets, "ef_scf_h": ef_scf_h}


# ----------------------------------------------------------------------------------------------- the asks' truth
def bleed_truth(wd):
    """Each continuous-bleed device's 2026 methane: its rate (the survey's reading where the survey read that
    device, by serial, otherwise its maker's rating) times the hours its supply was on, at its site's 2026 gas."""
    meas = {m["serial"]: m["scf_h"] for m in wd["survey"]["bleeds"]}
    out = []
    for key, h in sorted(wd["bleed_hist"].items(), key=lambda kv: (kv[1]["site"], kv[1]["tag"], kv[1]["from"])):
        site = next(s for s in wd["sites"] if s["code"] == h["site"])
        rate = meas.get(h["serial"], W.BLEED_MODELS[h["model"]]["scf_per_h"])
        hrs = bleed_hours(h)
        kg = rate * hrs * W.SCF_TO_M3 * site["x2026"] * W.CH4_KG_PER_M3
        out.append(dict(h, rate=rate, measured=h["serial"] in meas, hours=hrs, kg=kg))
    return out


def nonarrival_truth(wd):
    """Each plunger well's 2026 cycles that ended without the plunger arriving, on the well that actually ran
    them, each cycle once: the logged non-arrivals and the openings aborted on the line pressure interlock."""
    out = {}
    for sep in wd["seps"]:
        if sep["group"] == "F":
            continue
        cyc = window_cycles(wd, sep["uwi"])
        ab = [a for a in wd["aborted"] if a["uwi"] == sep["uwi"] and W.WINDOW_START_UTC <= a["near_utc"] < W.WINDOW_END_UTC]
        out[sep["uwi"]] = sum(1 for c in cyc if c["result"] == "NO ARRIVAL") + len(ab)
    return out


def bleed_by_maker_area(bt, wd):
    """The sales gas pressure controllers' 2026 methane for each maker in each area, kg."""
    area = {s["code"]: s["area"] for s in wd["sites"]}
    out = {}
    for b in bt:
        if b["kind"] != "PC":
            continue
        k = (W.BLEED_MODELS[b["model"]]["maker"], area[b["site"]])
        out[k] = out.get(k, 0.0) + b["kg"]
    return out


def gas_truth(wd):
    """Each site's 2026 gas, e3m3: the daily allocations plus every adjustment whose run re-allocated a 2026
    production month, posted by the as-of date."""
    month_of = {r["run"]: r["prod_month"] for r in wd["runs"]}
    adj = {}
    for p in wd["ppa"]:
        if month_of[p["run"]].startswith("2026") and p["posted"] <= W.AS_OF:
            adj[p["uwi"]] = adj.get(p["uwi"], 0.0) + p["vol"]
    out = {}
    for s in wd["sites"]:
        tot = 0.0
        for sep in s["seps"]:
            tot += float(wd["prod"][sep["uwi"]]["gas"].sum()) + adj.get(sep["uwi"], 0.0)
        out[s["code"]] = tot
    return out
