"""Write target/ from the clean truth world.py returns: every export the way its producing system writes it.

Systems and their clocks:
  point of sale (forecourt controller to head office): one row per hose and business day, the business day
      running 05:00 to 05:00 on the site's wall clock; monthly exports, December exported twice;
  tank gauge consoles at the gas bars: the shift-close reading at 05:00 on the site's wall clock, stamped
      with the zone the console shows (CST in Saskatchewan, CDT or CST in Manitoba);
  terminal bills of lading: loading time on the terminal's wall clock; the gas bar's receiver writes the
      drop time on the bill at an attended site, nobody signs at an unattended cardlock;
  the head-office tank monitoring service (cardlock consoles): CST throughout;
  the cardlock host: transaction times in UTC;
  service contractors, the vacuum hauler, the testing contractor: their own records and wording.
"""
import csv
import datetime as dt
import json
import math
import os

import numpy as np
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill

import params as P
import world as W
import docs as D

TD = dt.timedelta


def _rng(name):
    return W._rng("pack-" + name)


# ----------------------------------------------------------------- clocks

def _nth_sunday(y, m, n):
    d = dt.date(y, m, 1)
    while d.weekday() != 6:
        d += TD(days=1)
    return d + TD(days=7 * (n - 1))


def mb_dst(ts_cst):
    """Manitoba on daylight time at this instant (given in CST)?"""
    y = ts_cst.year
    start = dt.datetime.combine(_nth_sunday(y, 3, 2), dt.time(2, 0))      # 02:00 CST
    end = dt.datetime.combine(_nth_sunday(y, 11, 1), dt.time(1, 0))       # 02:00 CDT = 01:00 CST
    return start <= ts_cst < end


def wall(ts_cst, prov):
    if prov == "MB" and mb_dst(ts_cst):
        return ts_cst + TD(hours=1), "CDT"
    return ts_cst, "CST"


def wall_to_cst(ts_wall, prov):
    if prov == "MB":
        cand = ts_wall - TD(hours=1)
        if mb_dst(cand):
            return cand
    return ts_wall


def fmt_wall(ts_cst, prov):
    w, z = wall(ts_cst, prov)
    return "%s %s" % (w.strftime("%Y-%m-%d %H:%M"), z)


TERMINAL_PROV = {"Regina": "SK", "Saskatoon": "SK", "Brandon": "MB"}
SITE = {s[0]: s for s in P.SITES}
CL = {c[0]: c for c in P.CARDLOCKS}
POS_GRADE = {"R": "REG 87", "P": "PREM 91", "D": "DSL"}
ATG_PRODUCT = {"R": "UNLEADED", "P": "PREMIUM", "D": "DIESEL"}
BOL_PRODUCT = {"R": "Regular Unleaded", "P": "Premium Unleaded", "D": "ULS Diesel"}
TANK_NO = {"R": 1, "P": 2, "D": 3}


def prov_of(code):
    return SITE[code][2] if code in SITE else CL[code][2]


def town_of(code):
    return SITE[code][1] if code in SITE else CL[code][1]


def write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return len(rows)


# ----------------------------------------------------------------- prices (for the sales amounts)

def price_series():
    rng = _rng("prices")
    out = {}
    n = W.ND
    base = {"R": 1.47, "P": 1.67, "D": 1.62}
    walk = np.cumsum(rng.normal(0, 0.012, n // 7 + 2))
    for prov, off in (("SK", 0.0), ("MB", 0.035)):
        for g in "RPD":
            wk = np.repeat(walk, 7)[:n]
            season = 0.05 * np.sin(2 * np.pi * (np.arange(n) - 120) / 365.25)
            extra = 0.04 * (np.arange(n) / n) if g == "D" else 0.0
            out[(prov, g)] = np.round(base[g] + off + wk + season + extra, 3)
    return out


# ----------------------------------------------------------------- point of sale

def pos_rows(gb):
    rng = _rng("pos")
    prices = price_series()
    fills = {"R": 36.0, "P": 31.0, "D": 82.0}
    rows = []
    prelim = []
    cal_test = {}
    for code in [s[0] for s in P.SITES]:
        for prod in "RPD":
            t = gb[(code, prod)]
            for h, (fp, g) in enumerate(t["hoses"]):
                tot = float(rng.uniform(2.1e6, 7.8e6)) if not (code == "GB-121" and g == "D") else float(rng.uniform(1.6e7, 2.4e7))
                if code == "GB-124" and W.dispenser_of(code, fp) == 2:
                    tot = float(rng.uniform(4.0e6, 6.0e6))
                for i, d in enumerate(W.DAYS):
                    v = float(t["hose_litres"][h, i])
                    # test drafts on the calibration day go through the meter and back to the tank
                    test = 0.0
                    for s, disps in W.calibration_events(code):
                        if s == d and (disps is None or W.dispenser_of(code, fp) in disps):
                            test = float(rng.choice([80.0, 100.0, 120.0]))
                    swapped = any(c == code and W.dispenser_of(code, fp) == disp and W._date(sd) == d
                                  for (c, disp, sd) in P.DISPENSER_SWAPS)
                    if swapped:
                        tot = round(float(rng.uniform(40, 90)), 2)     # the new dispenser's factory totaliser
                    tot += v + test
                    fill = fills[g] * (3.2 if code == "GB-121" and g == "D" else 1.0)
                    n = int(rng.poisson(v / fill)) if v > 0 else 0
                    if v > 0:
                        n = max(n, 1)
                    pr = prices[(prov_of(code), g)][i]
                    rows.append([code, d, fp, POS_GRADE[g], round(v, 2), round(v * pr, 2), n, round(tot, 2)])
    rows.sort(key=lambda r: (r[1], r[0], r[2], r[3]))
    out = []
    for r in rows:
        d = r[1]
        batch = "%04d-%02d" % (d.year, d.month)
        nxt = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 2)
        exported = dt.datetime.combine(nxt, dt.time(6, 10)) + TD(minutes=int((d.month * 7) % 23))
        if (d.year, d.month) == (2026, 12):
            exported = dt.datetime(2027, 1, 5, 8, 12)
        out.append([r[0], d.isoformat(), r[2], r[3], "%.2f" % r[4], "%.2f" % r[5], r[6], "%.2f" % r[7],
                    batch, exported.strftime("%Y-%m-%d %H:%M")])
        if (d.year, d.month) == (2026, 12):
            vol, amt, n = r[4], r[5], r[6]
            if r[0] == P.POS_REEXPORT["site"] and d == P.POS_REEXPORT["day"]:
                keep = 1.0 - P.POS_REEXPORT["held_share"]
                vol, amt, n = round(vol * keep, 2), round(amt * keep, 2), int(round(n * keep))
            prelim.append([r[0], d.isoformat(), r[2], r[3], "%.2f" % vol, "%.2f" % amt, n, "%.2f" % r[7],
                           "2026-12P", "2027-01-02 07:41"])
    # the preliminary December export sits before the re-export in the head office's file
    dec0 = next(i for i, r in enumerate(out) if r[8] == "2026-12")
    return out[:dec0] + prelim + out[dec0:]


# ----------------------------------------------------------------- tank gauges at the gas bars

def ground_temp(i, prod):
    t = (W.DAYS[min(i, W.ND - 1)] - dt.date(W.DAYS[min(i, W.ND - 1)].year, 1, 1)).days
    return 7.5 + 5.5 * math.sin(2 * math.pi * (t - 150) / 365.25) + (0.6 if prod == "D" else 0.0)


def atg_rows(gb):
    rng = _rng("atg")
    rows = []
    gaps = set()
    # the odd missed reading (console comms), never the quarter boundaries
    for key in sorted(gb):
        for _ in range(int(rng.integers(0, 3))):
            i = int(rng.integers(5, W.ND - 5))
            if W.DAYS[i] in (dt.date(2026, 10, 1), dt.date(2026, 7, 1), dt.date(2026, 4, 1)):
                continue
            if any(abs((W.DAYS[i] - dt.date(y, m, 1)).days) <= 1 for y in (2024, 2025, 2026) for m in (1, 4, 7, 10)):
                continue
            gaps.add((key, i))
    for (code, prod) in sorted(gb):
        t = gb[(code, prod)]
        prov = prov_of(code)
        cap = t["cap"]
        water = float(rng.uniform(2, 9))
        for i in range(W.ND + 1):
            d = P.START + TD(days=i)
            if ((code, prod), i) in gaps:
                continue
            for (c, pr, s, wl, pl) in P.VACUUM_PUMPOUTS:
                if c == code and pr == prod and W._date(s) + TD(days=1) == d:
                    water = float(rng.uniform(0, 2))
            water += float(rng.uniform(0, 0.02))
            ts_wall = dt.datetime.combine(d, dt.time(5, 0))
            ts_cst = wall_to_cst(ts_wall, prov)
            label = wall(ts_cst, prov)[1]
            net = int(t["atg"][i])
            temp = ground_temp(i, prod) + float(rng.normal(0, 0.25))
            rows.append([code, TANK_NO[prod], ATG_PRODUCT[prod], "%s 05:00 %s" % (d.isoformat(), label), net,
                         "%.1f" % temp, int(round(water)), int(round(0.95 * cap - net))])
    rows.sort(key=lambda r: (r[3][:10], r[0], r[1]))
    return rows


# ----------------------------------------------------------------- bills of lading

def vcf_gross(net, temp, prod):
    a = 0.00083 if prod == "D" else 0.00125
    return net * (1 + a * (temp - 15.0))


def terminal_temp(day, prod, offset):
    t = (day - dt.date(day.year, 1, 1)).days
    return 6.0 + 13.0 * math.sin(2 * math.pi * (t - 110) / 365.25) + offset


def bol_rows(gb, cl):
    rng = _rng("bol")
    drops = []
    initials = {}
    for s in P.SITES:
        initials[s[0]] = ["".join(rng.choice(list("ABCDEGHJKLMNPRSTW"), 2)) for _ in range(4)]
    for (code, prod), t in sorted(gb.items()):
        prov = prov_of(code)
        for dr in t["drops"]:
            drop_wall = dt.datetime.combine(dr["day"], dt.time(dr["hour"], dr["minute"]))
            drop_cst = wall_to_cst(drop_wall, prov)
            load_cst = drop_cst - TD(hours=dr["load_hours"])
            temp = terminal_temp(load_cst.date(), prod, dr["temp_offset"])
            drops.append(dict(site=code, prod=prod, carrier=dr["carrier"], load_cst=load_cst, drop_cst=drop_cst,
                              net=dr["net"], temp=temp, attended=True,
                              recv=str(rng.choice(initials[code]))))
    # cardlocks: the simulated quarter, and before it a plain delivery cycle per tank
    cl_carriers = list(P.CARRIERS_CL.keys())
    cw = list(P.CARRIERS_CL.values())
    for (code, prod), c in sorted(cl.items()):
        for dr in c["drops"]:
            load_cst = W.time_of(dr["load"])
            if load_cst.year > 2026:
                continue
            drops.append(dict(site=code, prod=prod, carrier=dr["carrier"], load_cst=load_cst,
                              drop_cst=W.time_of(dr["start"]), net=dr["bol"],
                              temp=terminal_temp(load_cst.date(), prod, dr["temp_offset"]), attended=False, recv=""))
        daily = CL[code][5] if prod == "D" else CL[code][6]
        q = 34000.0 if prod == "D" else 17500.0
        first_world = min(W.time_of(dr["load"]) for dr in c["drops"])
        tcur = dt.datetime(2024, 1, 1, 0, 0) + TD(hours=float(rng.uniform(0, 72)))
        while True:
            gap = q / daily * float(rng.uniform(0.85, 1.15))
            tcur = tcur + TD(days=gap)
            if tcur >= first_world - TD(hours=30):
                break
            carrier = str(rng.choice(cl_carriers, p=cw))
            hr = float(rng.uniform(21, 31)) if (carrier == "Whitesand Tankline" and rng.uniform() < 0.6) else float(rng.uniform(7, 17))
            drop = dt.datetime.combine(tcur.date(), dt.time(0)) + TD(hours=hr)
            transit = TD(minutes=int(rng.integers(150, 361)) if carrier == "Whitesand Tankline" else int(rng.integers(90, 241)))
            net = math.floor(q * float(rng.uniform(0.8, 1.1)) / 500.0) * 500.0
            drops.append(dict(site=code, prod=prod, carrier=carrier, load_cst=drop - transit, drop_cst=drop, net=net,
                              temp=terminal_temp((drop - transit).date(), prod, float(rng.normal(0, 1.5))),
                              attended=False, recv=""))
    drops = [x for x in drops if dt.datetime(2024, 1, 1) <= x["load_cst"] < dt.datetime(2027, 1, 1)
             or (x["site"].startswith("GB") and x["drop_cst"] >= dt.datetime(2024, 1, 1, 5))]
    # bill numbers run per terminal in loading order
    seq = {"Regina": 418200, "Saskatoon": 772050, "Brandon": 230410}
    pre = {"Regina": "RGA", "Saskatoon": "STN", "Brandon": "BDN"}
    drops.sort(key=lambda x: (x["load_cst"], x["site"], x["prod"]))
    rows = []
    for x in drops:
        term = P.TERMINAL_OF[x["site"]]
        seq[term] += int(rng.integers(3, 19))                 # other customers' loads in between
        tprov = TERMINAL_PROV[term]
        gross = vcf_gross(x["net"], x["temp"], x["prod"])
        consignee = "%s %s" % (x["site"], town_of(x["site"]) + (" Cardlock" if x["site"].startswith("CL") else " Gas Bar"))
        delivered = fmt_wall(x["drop_cst"], prov_of(x["site"])) if x["attended"] else ""
        rows.append(["%s-%d" % (pre[term], seq[term]), term, x["carrier"], fmt_wall(x["load_cst"], tprov), consignee,
                     BOL_PRODUCT[x["prod"]], int(round(gross)), int(x["net"]), "%.1f" % x["temp"], delivered, x["recv"]])
    return rows


# ----------------------------------------------------------------- work orders

def work_orders(gb):
    rng = _rng("wo")
    contractor_of = {}
    for name, cfg in P.CONTRACTORS.items():
        for s in cfg["sites"]:
            contractor_of[s] = name
    disp_count = {}
    for code in [s[0] for s in P.SITES]:
        disp_count[code] = sorted({W.dispenser_of(code, fp) for (fp, g) in W.hose_layout()[code]})
    meters = {code: len(W.hose_layout()[code]) for code in disp_count}
    items = []

    def tech(code):
        return str(rng.choice(P.CONTRACTORS[contractor_of[code]]["techs"]))

    for code in disp_count:
        con = contractor_of[code]
        for s, disps in W.calibration_events(code):
            dl = disp_count[code] if disps is None else disps
            nm = sum(1 for (fp, g) in W.hose_layout()[code] if W.dispenser_of(code, fp) in dl)
            if con.startswith("Quill"):
                if disps is None:
                    txt = "Scheduled meter calibration. Proved and adjusted all meters, %d in all. Measurement Canada " \
                          "seals renewed. Test volumes returned to tanks." % nm
                else:
                    txt = "Meter calibration, dispensers %s (%d meters). Seals renewed. Test volumes returned to tanks." % (
                        ", ".join(str(x) for x in dl), nm)
            else:
                if disps is None:
                    txt = "W&M prove/adjust - all disps, %d meters, sealed. Product returned to UST." % nm
                else:
                    rng_d = "D%d-D%d" % (dl[0], dl[-1]) if len(dl) > 1 else "D%d" % dl[0]
                    txt = "W&M prove/adjust - %s, %d meters, sealed. Product returned to UST." % (rng_d, nm)
                if code == "GB-142" and disps is not None:
                    txt += " D5 diesel not done, locked out for breakaway/nozzle repair - rebook."
            items.append((s, code, con, "Meter calibration", txt, "Dispensers", round(float(rng.uniform(4.5, 9.0)), 1)))
    for (code, disp, s) in P.DISPENSER_SWAPS:
        items.append((W._date(s), code, contractor_of[code], "Dispenser replacement",
                      "Removed dispenser %d (failed hydraulics, unit beyond repair) and installed new dispenser, same "
                      "position, fuelling points %d and %d. New unit factory calibrated and sealed; totalisers start "
                      "from new." % (disp, 2 * disp - 1, 2 * disp), "Dispenser %d" % disp, 11.5))
    for (code, fp, g, s) in P.METER_SWAPS:
        con = contractor_of[code]
        txt = ("Replaced meter, FP %d %s (leaking seal). New meter sealed." % (fp, POS_GRADE[g])) if con.startswith("Quill") \
            else "Meter swap FP%d %s - leaking, new meter installed & sealed." % (fp, POS_GRADE[g])
        items.append((W._date(s), code, con, "Meter replacement", txt, "FP %d" % fp, 2.5))
    for (code, g, s) in P.STP_REPLACEMENTS:
        con = contractor_of[code]
        txt = ("Replaced submersible pump, %s tank (motor failed). Reinstalled mechanical line leak detector." % ATG_PRODUCT[g].lower()) \
            if con.startswith("Quill") else "STP replaced - %s, motor seized. LLD refitted." % ATG_PRODUCT[g].title()
        items.append((W._date(s), code, con, "Submersible pump", txt, "Tank %d STP" % TANK_NO[g], round(float(rng.uniform(5, 8)), 1)))
    for (code, g, s, step) in P.PROBE_REPLACEMENTS:
        con = contractor_of[code]
        items.append((W._date(s), code, con, "Tank gauge", "Replaced inventory probe, tank %d (%s), probe fault alarm. "
                      "Console reprogrammed." % (TANK_NO[g], ATG_PRODUCT[g].lower()), "Tank %d probe" % TANK_NO[g], 3.0))
    # routine calls
    routine = [("Nozzle/hose", "Replaced hose and breakaway, FP %d."), ("Nozzle/hose", "Replaced nozzle FP %d (sticking latch)."),
               ("Sump inspection", "Annual sump and UDC inspection, all dry. Photos on file."),
               ("Sump inspection", "Annual sump and UDC inspection, all dry. Photos on file."),
               ("Spill containment", "Cleaned out fill spill buckets, tank %d lid gasket replaced."),
               ("Tank gauge", "Console alarm call - delivery needed alarm reset, no fault."),
               ("Filters", "Changed dispenser filters, diesel FP %d."),
               ("Electrical", "Reset tripped breaker, dispenser %d, checked wiring.")]
    for code in disp_count:
        n = int(rng.integers(9, 16))
        for _ in range(n):
            d = P.START + TD(days=int(rng.integers(0, W.ND)))
            cat, txt = routine[int(rng.integers(0, len(routine)))]
            if cat == "Sump inspection" and "single-wall" in P.TANK_BUILD[code][2]:
                cat, txt = "Line test", "Annual line tightness test, all product lines, by line tester. Results to site file."
            if "%d" in txt:
                if "FP" in txt:
                    txt = txt % int(rng.integers(1, SITE[code][3] + 1))
                elif "tank" in txt:
                    txt = txt % int(rng.integers(1, 4))
                else:
                    txt = txt % int(rng.integers(1, len(disp_count[code]) + 1))
            items.append((d, code, contractor_of[code], cat, txt, "", round(float(rng.uniform(0.8, 3.5)), 1)))
    items.sort(key=lambda x: (x[0], x[1], x[3]))
    rows = []
    n = 24117
    for (d, code, con, cat, txt, eq, hrs) in items:
        n += int(rng.integers(1, 9))
        rows.append(["WO-%d" % n, d, "%s %s" % (code, town_of(code)), con, tech(code), cat, txt, eq, hrs])
    return rows


# ----------------------------------------------------------------- the forecourt controller configuration

def fcc_config():
    rng = _rng("fcc")
    serial = {}
    out = {"exported_at": "2027-01-05T07:58:12-06:00", "controller_software": "FCC 6.4.2", "sites": []}
    for s in P.SITES:
        code = s[0]
        layout = W.hose_layout()[code]
        fps = sorted({fp for fp, g in layout})
        site = {"site": code, "name": "%s Gas Bar" % s[1], "fuelling_points": []}
        for fp in fps:
            disp = W.dispenser_of(code, fp)
            if (code, disp) not in serial:
                yr = 2025 if any(c == code and dd == disp for (c, dd, x) in P.DISPENSER_SWAPS) else int(rng.integers(2009, 2021))
                serial[(code, disp)] = "%s%02d%05d" % ("WA" if yr >= 2015 else "GV", yr % 100, int(rng.integers(10000, 99999)))
            hoses = []
            for hn, g in enumerate([g for (f, g) in layout if f == fp], start=1):
                hoses.append({"hose": hn, "grade": POS_GRADE[g], "tank": TANK_NO[g]})
            site["fuelling_points"].append({"fp": fp, "dispenser_serial": serial[(code, disp)], "hoses": hoses})
        out["sites"].append(site)
    return out, serial


# ----------------------------------------------------------------- registers

def register_book(path, gb, serial):
    rng = _rng("register")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tanks"
    hdr = ["Site", "Location", "Prov", "Tank", "Product", "Capacity (L)", "Construction", "Installed", "Piping",
           "Pump", "Leak detection (lines)"]
    ws.append(hdr)
    for s in P.SITES:
        code, town, prov = s[0], s[1], s[2]
        for prod in "RPD":
            cap = gb[(code, prod)]["cap"]
            con, inst, piping = P.TANK_BUILD_EXCEPT.get((code, prod), P.TANK_BUILD[code])
            ws.append([code, town, prov, TANK_NO[prod], {"R": "Regular", "P": "Premium", "D": "Diesel"}[prod], cap, con, inst,
                       piping, "Submersible, pressurised", "Mechanical LLD"])
    for c in P.CARDLOCKS:
        code, town, prov = c[0], c[1], c[2]
        for prod, cap in (("D", c[7]), ("R", c[8])):
            ws.append([code, town + " Cardlock", prov, 1 if prod == "D" else 2, "Diesel" if prod == "D" else "Regular",
                       cap, "Double-wall steel AST", int(rng.integers(2011, 2020)), "Aboveground", "Suction",
                       "Interstitial sensor"])
    ws2 = wb.create_sheet("Dispensers")
    ws2.append(["Site", "Dispenser", "Serial", "Make/model", "Fuelling points", "Grades", "Temp. compensated",
                "In service", "Out of service"])
    for s in P.SITES:
        code = s[0]
        layout = W.hose_layout()[code]
        disps = sorted({W.dispenser_of(code, fp) for fp, g in layout})
        for dno in disps:
            fps = sorted({fp for fp, g in layout if W.dispenser_of(code, fp) == dno})
            grades = []
            for fp, g in layout:
                if W.dispenser_of(code, fp) == dno and POS_GRADE[g] not in grades:
                    grades.append(POS_GRADE[g])
            swap = [x for x in P.DISPENSER_SWAPS if x[0] == code and x[1] == dno]
            model = "Wayne Ovation" if serial[(code, dno)].startswith("WA") else "Gilbarco Encore 500"
            if swap:
                d0 = W._date(swap[0][2])
                ws2.append([code, dno, "GV%02d%05d" % (int(rng.integers(9, 14)), int(rng.integers(10000, 99999))),
                            "Gilbarco Encore 500", "%d-%d" % (fps[0], fps[-1]), ", ".join(grades), "Yes (15 C)",
                            dt.date(2011, 5, 2), d0])
                ws2.append([code, dno, serial[(code, dno)], model, "%d-%d" % (fps[0], fps[-1]), ", ".join(grades),
                            "Yes (15 C)", d0, None])
            else:
                ws2.append([code, dno, serial[(code, dno)], model, "%d-%d" % (fps[0], fps[-1]) if len(fps) > 1 else str(fps[0]),
                            ", ".join(grades), "Yes (15 C)", dt.date(2009, 1, 1) + TD(days=int(rng.integers(0, 3600))), None])
    ws3 = wb.create_sheet("Cardlock pumps")
    ws3.append(["Cardlock", "Pump", "Product", "Tank", "Meter", "Temp. compensated"])
    for c in P.CARDLOCKS:
        for p in range(1, c[3] + c[4] + 1):
            prod = "Diesel" if p <= c[3] else "Regular"
            ws3.append([c[0], p, prod, 1 if p <= c[3] else 2, "Hi-flow" if prod == "Diesel" else "Standard", "Yes (15 C)"])
    for w in wb.worksheets:
        for cell in w[1]:
            cell.font = Font(bold=True)
        w.freeze_panes = "A2"
        for col in w.columns:
            width = max(len(str(c.value)) if c.value is not None else 0 for c in col)
            w.column_dimensions[col[0].column_letter].width = min(48, max(9, width + 2))
        for row in w.iter_rows(min_row=2):
            for cell in row:
                if isinstance(cell.value, dt.date):
                    cell.number_format = "yyyy-mm-dd"
    wb.save(path)
    D.finalise_xlsx(path, "Site and tank register", "Roy Turner", "Roy Turner", "Tamarack Prairie Co-operative Ltd.",
                    "2019-03-11T15:22:40", "2026-12-18T21:07:13")


def work_order_book(path, rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Work orders"
    ws.append(["WO #", "Date", "Site", "Contractor", "Technician", "Category", "Work done", "Equipment", "Hours"])
    for r in rows:
        ws.append(r)
    for cell in ws[1]:
        cell.font = Font(bold=True)
    ws.freeze_panes = "A2"
    widths = [11, 11, 22, 30, 17, 19, 96, 15, 7]
    for i, wdt in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wdt
    for row in ws.iter_rows(min_row=2):
        row[1].number_format = "yyyy-mm-dd"
        row[6].alignment = Alignment(wrap_text=False)
    wb.save(path)
    D.finalise_xlsx(path, "Service work orders", "Roy Turner", "Roy Turner", "Tamarack Prairie Co-operative Ltd.",
                    "2024-01-08T16:40:02", "2027-01-04T22:31:55")


# ----------------------------------------------------------------- vacuum truck

def vacuum_rows():
    rng = _rng("vac")
    rows = []
    n = 60381
    events = sorted(P.VACUUM_PUMPOUTS, key=lambda x: (x[2], x[0]))
    extra = [("GB-118", None, "2025-04-29", 0, 0), ("GB-153", None, "2026-05-12", 0, 0), ("GB-121", None, "2024-06-04", 0, 0)]
    for (code, prod, s, water, product) in sorted(events + extra, key=lambda x: (x[2], x[0])):
        n += int(rng.integers(2, 40))
        if prod is None:
            rows.append(["M%d" % n, s, "Assiniboine Valley Vac Services", "V-12", "%s %s" % (code, town_of(code)), "",
                         "Spill buckets and sumps - rainwater", int(rng.integers(30, 70)), "Yorkton waste transfer",
                         P.PEOPLE["vac_driver"]])
        else:
            rows.append(["M%d" % n, s, "Assiniboine Valley Vac Services", "V-12", "%s %s" % (code, town_of(code)),
                         "Tank %d (%s)" % (TANK_NO[prod], {"R": "regular", "P": "premium", "D": "diesel"}[prod]),
                         "Tank bottom water draw-off, water/product mix", water + product, "Yorkton waste transfer",
                         P.PEOPLE["vac_driver"]])
    return rows


# ----------------------------------------------------------------- cardlocks

def cardlock_files(cl):
    rng = _rng("cl")
    reports, hourly, txns = [], [], []
    h0 = W.minute_of(dt.datetime(2026, 9, 30, 0, 0))           # the extract runs a day either side
    h1 = W.minute_of(dt.datetime(2027, 1, 2, 0, 0))
    for (code, prod) in sorted(cl):
        c = cl[(code, prod)]
        pulls = [W.minute_of(t) for t in P.REPORT_PULLS if (t, code) not in P.PULL_MISSED]
        tank = 1 if prod == "D" else 2
        lev = c["level"]
        rep = sorted([d for d in c["drops"] if not d["outage"]], key=lambda d: d["rep_end"])
        for T in pulls:
            done = [d for d in rep if d["rep_end"] <= T][-P.REPORT_DEPTH:]
            for d in done:
                s_v = round(float(lev[d["rep_start"]]), 1)
                e_v = round(float(lev[d["rep_end"]]), 1)
                day = W.time_of(d["rep_start"]).date()
                tmp = 4.0 - 7.0 * ((day - dt.date(2026, 10, 1)).days / 92.0)
                trng = W._rng("cl-temp-%s-%s-%d" % (code, prod, d["delivery_no"]))
                reports.append([code, tank, "DIESEL" if prod == "D" else "UNLEADED", d["delivery_no"],
                                W.time_of(d["rep_start"]).strftime("%Y-%m-%d %H:%M"),
                                W.time_of(d["rep_end"]).strftime("%Y-%m-%d %H:%M"),
                                "%.1f" % s_v, "%.1f" % e_v, "%.1f" % (e_v - s_v), "%.1f" % (tmp + float(trng.normal(0, 0.3))),
                                "%.1f" % (tmp + 3.5 + float(trng.normal(0, 0.4))),
                                W.time_of(T).strftime("%Y-%m-%d %H:%M")])
        for m in range(h0, h1, 60):
            ts = W.time_of(m)
            if code == P.OUTAGE["site"] and W.O_S < m < W.O_E:
                continue
            day = ts.date()
            tmp = 4.0 - 7.0 * ((day - dt.date(2026, 10, 1)).days / 92.0) + 1.5 * math.sin(2 * math.pi * (ts.hour - 9) / 24)
            hourly.append([code, tank, "DIESEL" if prod == "D" else "UNLEADED", ts.strftime("%Y-%m-%d %H:%M"),
                           "%.1f" % float(lev[m]), "%.1f" % (tmp + float(rng.normal(0, 0.2))), int(rng.integers(0, 3))])
    # transactions: start and end in UTC to the second
    accounts = ["F%05d" % int(x) for x in rng.choice(np.arange(10000, 99999), 160, replace=False)]
    acct_w = rng.dirichlet(np.full(len(accounts), 0.7))
    cards = {}
    for (code, prod) in sorted(cl):
        c = cl[(code, prod)]
        for (s, e, lit, pump) in c["txns"]:
            if not (h0 <= s < h1):
                continue
            ss = int(rng.integers(0, 60))
            es = int(rng.integers(0, 60))
            st = W.time_of(s) + TD(seconds=ss) + TD(hours=6)
            en = W.time_of(e) + TD(seconds=es) + TD(hours=6)
            if en <= st:
                en = st + TD(seconds=30)
            a = str(rng.choice(accounts, p=acct_w))
            if a not in cards:
                cards[a] = ["%04d" % int(x) for x in rng.integers(0, 9999, int(rng.integers(1, 6)))]
            card = "7083 05** **** " + str(rng.choice(cards[a]))
            txns.append([st, en, code, pump, "DIESEL" if prod == "D" else "REGULAR", "%.2f" % lit, a, card])
    txns.sort(key=lambda r: (r[0], r[2], r[3]))
    out_t = []
    steps = np.cumsum(rng.integers(1, 7, len(txns)))       # the host numbers every site's sales, not only these
    for i, r in enumerate(txns):
        out_t.append(["T%07d" % (5170000 + int(steps[i])), r[2], r[3], r[4], r[5],
                      r[0].strftime("%Y-%m-%dT%H:%M:%SZ"), r[1].strftime("%Y-%m-%dT%H:%M:%SZ"), r[7], r[6]])
    reports.sort(key=lambda r: (r[11], r[0], r[1], r[3]))
    hourly.sort(key=lambda r: (r[3], r[0], r[1]))
    return reports, hourly, out_t


# ----------------------------------------------------------------- distractors

def weather_rows():
    rng = _rng("wx")
    rows = []
    for i, d in enumerate(W.DAYS):
        t = (d - dt.date(d.year, 1, 1)).days
        mean = 2.0 + 18.5 * math.sin(2 * math.pi * (t - 112) / 365.25) + float(rng.normal(0, 4.0))
        rngd = float(rng.uniform(7, 15))
        precip = float(rng.choice([0, 0, 0, 0, rng.gamma(1.2, 3.0)]))
        snow = 0 if 100 < t < 300 else int(max(0, 18 + 10 * math.cos(2 * math.pi * t / 365.25) + rng.normal(0, 4)))
        rows.append([d.isoformat(), "%.1f" % (mean + rngd / 2), "%.1f" % (mean - rngd / 2), "%.1f" % mean,
                     "%.1f" % precip, snow])
    return rows


def lld_rows(gb):
    rng = _rng("lld")
    rows = []
    for s in P.SITES:
        code = s[0]
        d = dt.date(2026, 8, 24) + TD(days=int(rng.integers(0, 40)))
        for prod in "RPD":
            rows.append([code, s[1], TANK_NO[prod], {"R": "Regular", "P": "Premium", "D": "Diesel"}[prod], d.isoformat(),
                         "Mechanical", "FX1V", "3.0 gph @ 10 psi", "PASS",
                         "%.1f" % float(rng.uniform(1.6, 2.9)), P.PEOPLE["lld_tech"]])
    return rows


# ----------------------------------------------------------------- PDFs

def standard_pdf(path):
    S = D.styles()
    f = []
    f.append(D.Paragraph("Tamarack Prairie Co-operative Ltd. - Petroleum Division", S["ref"]))
    f.append(D.Paragraph("PD-07 Release detection for underground tank systems at gas bars", S["title"]))
    f.append(D.Paragraph("Revision 3. Effective 1 October 2026. Owner: Petroleum Manager. Approved by the General "
                         "Manager, 22 September 2026.", S["ref"]))
    f.append(D.Spacer(1, 6))
    sec = [
        ("1. Purpose", "This standard sets how the Petroleum Division watches each underground tank system at its gas "
                       "bars for a release of product, and what it does when one is suspected. It meets the provincial "
                       "petroleum storage regulations in Saskatchewan and Manitoba and does not replace them."),
        ("2. Scope", "A tank system is one underground storage tank together with its submersible pump and the "
                     "pressurised underground piping from the pump to the dispensers. Every gas bar tank system is in "
                     "scope. The cardlock tanks are aboveground, double-walled and monitored by interstitial sensors "
                     "under PD-09; they are outside this standard."),
        ("3. Inventory records", "Each gas bar keeps a daily inventory record for each tank system for every business "
                                 "day, the business day running from 05:00 to 05:00 on the site's clock. The record "
                                 "holds the tank gauge's net volume at the close, the product received, and the "
                                 "product sold. Volumes are litres at 15 C. Product received is taken at the bill of "
                                 "lading's net volume on the business day of the drop; product sold is taken as the "
                                 "point-of-sale volume."),
        ("4. Quarterly review", "After each calendar quarter the Controller's office reviews every gas bar tank "
                                "system. The quantity reviewed is the product the tank system lost to the ground over "
                                "the quarter, stated as an average in litres per hour of the hours that elapsed in "
                                "the quarter. Product lost to the ground is product that left the tank system other "
                                "than through a dispenser nozzle, that is, product that escaped from the tank or "
                                "from its piping."),
        ("5. Action", "A tank system that lost more than 0.75 litres an hour to the ground over the quarter is put on "
                      "the tightness-testing work order for the month after the review, for a precision test of the "
                      "tank and its lines by the testing contractor, and is reported to the province as a suspected "
                      "release within 24 hours of the review. A tank system at or under 0.75 litres an hour stays on "
                      "monthly monitoring."),
        ("6. Records and roles", "The Controller's office keeps the inventory records, the quarterly review and the "
                                 "work order for seven years. The Petroleum Manager issues the work order and makes "
                                 "the report to the province. Site managers send the gauge report, the point-of-sale "
                                 "export and the drop paperwork to the Controller's office by the 3rd business "
                                 "day of each month."),
    ]
    for h, p in sec:
        f.append(D.Paragraph(h, S["h"]))
        f.append(D.Paragraph(p, S["p"]))
    f.append(D.Paragraph("Revision history", S["h"]))
    f.append(D.table([["Rev", "Effective", "Change"],
                      ["1", "2012-04-01", "First issue"],
                      ["2", "2018-01-15", "Manitoba gas bars added after the Swan Valley Co-op amalgamation"],
                      ["3", "2026-10-01", "Quarterly review in litres an hour; cardlock tanks moved to PD-09"]],
                     [14 * D.mm, 26 * D.mm, 128 * D.mm]))
    D.write_pdf(path, dict(title="PD-07 Release detection for underground tank systems at gas bars",
                           author="Roy Turner", subject="Petroleum Division standard", creator="Microsoft Word",
                           producer="Microsoft: Print To PDF"),
                "Tamarack Prairie Co-operative Ltd. | PD-07 Rev. 3", "Controlled copy. Printed copies are uncontrolled.",
                f, "2026-09-22 14:18:37")


def cp_pdf(path, gb):
    rng = _rng("cp")
    S = D.styles()
    f = []
    f.append(D.Paragraph("Corrosion survey report", S["title"]))
    f.append(D.Paragraph("Cathodic protection survey, steel underground tanks, Tamarack Prairie Co-operative gas bars. "
                         "Survey dates 14 to 18 September 2026. Surveyed by %s, CP tester (NACE CP2)." % P.PEOPLE["cp_tech"],
                         S["ref"]))
    f.append(D.Spacer(1, 6))
    f.append(D.Paragraph("Method", S["h"]))
    f.append(D.Paragraph("Structure-to-soil potentials were measured with a copper/copper sulphate reference electrode "
                         "placed directly over each tank at the fill and at the far end, with protective current "
                         "applied where the system has an impressed current source. The criterion applied is a "
                         "potential of -850 mV or more negative with protection applied, or 100 mV of polarisation.",
                         S["p"]))
    rows = [["Site", "Tank", "Structure", "Fill end (mV)", "Far end (mV)", "Result"]]
    steel = [("GB-127", "R"), ("GB-127", "P"), ("GB-127", "D"), ("GB-131", "P"), ("GB-131", "D"), ("GB-131", "R"),
             ("GB-146", "R"), ("GB-146", "P"), ("GB-146", "D"), ("GB-160", "D")]
    for code, prod in steel:
        if (code, prod) == ("GB-131", "R"):
            a, b, res, st = -742, -688, "Below criterion", "Single-wall steel, galvanic anodes"
        else:
            a, b = int(rng.integers(-1010, -890)), int(rng.integers(-985, -870))
            res, st = "Meets criterion", "STI-P3 steel"
        rows.append(["%s %s" % (code, town_of(code)), "%d (%s)" % (TANK_NO[prod], {"R": "regular", "P": "premium", "D": "diesel"}[prod]),
                     st, str(a), str(b), res])
    f.append(D.Paragraph("Results", S["h"]))
    f.append(D.table(rows, [38 * D.mm, 24 * D.mm, 50 * D.mm, 20 * D.mm, 20 * D.mm, 26 * D.mm], align=[3, 4], small=True))
    f.append(D.Spacer(1, 6))
    f.append(D.Paragraph("Comments", S["h"]))
    f.append(D.Paragraph("Ituna tank 1 is protected by galvanic anodes installed in 1987 that appear to be near the end of "
                         "their life. Supplementary anodes or an impressed current retrofit should be quoted before the "
                         "next survey. All STI-P3 tanks meet the criterion. Fibreglass tanks and flexible piping are not "
                         "surveyed.", S["p"]))
    D.write_pdf(path, dict(title="Cathodic protection survey 2026", author="J. Peterson", subject="CP survey",
                           creator="Microsoft Word", producer="Microsoft: Print To PDF"),
                "CP survey - Tamarack Prairie Co-operative - September 2026", "Survey report, 2026",
                f, "2026-09-29 10:52:04")


# ----------------------------------------------------------------- write everything

FILES = {}


def write_all(w, out):
    os.makedirs(out, exist_ok=True)
    gb, cl = w["gasbars"], w["cardlocks"]
    n = write_csv(os.path.join(out, "pos_fuel_sales_by_hose_2024_2026.csv"),
                  ["site", "business_date", "fp", "grade", "volume_l", "amount_cad", "txns", "totaliser_l",
                   "export_batch", "exported_at"], pos_rows(gb))
    FILES["pos_fuel_sales_by_hose_2024_2026.csv"] = n
    n = write_csv(os.path.join(out, "atg_shift_close_inventory_2024_2026.csv"),
                  ["site", "tank", "product", "read_at", "net_volume_l", "product_temperature_c", "water_mm", "ullage_l"],
                  atg_rows(gb))
    FILES["atg_shift_close_inventory_2024_2026.csv"] = n
    n = write_csv(os.path.join(out, "bills_of_lading_2024_2026.csv"),
                  ["bol_no", "terminal", "carrier", "loaded_at", "consignee", "product", "gross_l", "net_l_15c",
                   "load_temperature_c", "delivered_at", "received_by"], bol_rows(gb, cl))
    FILES["bills_of_lading_2024_2026.csv"] = n
    wo = work_orders(gb)
    work_order_book(os.path.join(out, "service_work_orders_2024_2026.xlsx"), wo)
    FILES["service_work_orders_2024_2026.xlsx"] = len(wo)
    cfg, serial = fcc_config()
    with open(os.path.join(out, "forecourt_controller_config_2027-01-05.json"), "w") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")
    FILES["forecourt_controller_config_2027-01-05.json"] = sum(len(s["fuelling_points"]) for s in cfg["sites"])
    register_book(os.path.join(out, "tpc_site_tank_register.xlsx"), gb, serial)
    FILES["tpc_site_tank_register.xlsx"] = 36 + 8
    n = write_csv(os.path.join(out, "vacuum_truck_manifests_2024_2026.csv"),
                  ["manifest_no", "date", "hauler", "unit", "site", "tank", "description", "liquid_l", "disposal",
                   "driver"], vacuum_rows())
    FILES["vacuum_truck_manifests_2024_2026.csv"] = n
    reports, hourly, txns = cardlock_files(cl)
    FILES["cardlock_gauge_delivery_reports_q4_2026.csv"] = write_csv(
        os.path.join(out, "cardlock_gauge_delivery_reports_q4_2026.csv"),
        ["site", "tank", "product", "delivery_no", "start_cst", "end_cst", "start_net_l", "end_net_l",
         "increase_net_l", "start_temperature_c", "end_temperature_c", "pulled_cst"], reports)
    FILES["cardlock_gauge_hourly_inventory_q4_2026.csv"] = write_csv(
        os.path.join(out, "cardlock_gauge_hourly_inventory_q4_2026.csv"),
        ["site", "tank", "product", "read_cst", "net_volume_l", "product_temperature_c", "water_mm"], hourly)
    FILES["cardlock_transactions_q4_2026.csv"] = write_csv(
        os.path.join(out, "cardlock_transactions_q4_2026.csv"),
        ["txn_id", "site", "pump", "product", "litres", "started_utc", "ended_utc", "card", "account"], txns)
    FILES["yorkton_daily_weather_2024_2026.csv"] = write_csv(
        os.path.join(out, "yorkton_daily_weather_2024_2026.csv"),
        ["Date/Time", "Max Temp (\u00b0C)", "Min Temp (\u00b0C)", "Mean Temp (\u00b0C)", "Total Precip (mm)",
         "Snow on Grnd (cm)"], weather_rows())
    FILES["line_leak_detector_tests_2026.csv"] = write_csv(
        os.path.join(out, "line_leak_detector_tests_2026.csv"),
        ["site", "location", "tank", "product", "test_date", "detector", "model", "test_leak_rate", "result",
         "trip_time_s", "tester"], lld_rows(gb))
    standard_pdf(os.path.join(out, "pd07_release_detection_standard.pdf"))
    FILES["pd07_release_detection_standard.pdf"] = 2
    cp_pdf(os.path.join(out, "cathodic_protection_survey_2026.pdf"), gb)
    FILES["cathodic_protection_survey_2026.pdf"] = 1
    return FILES


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "target")
    files = write_all(W.build(), out)
    for k, v in sorted(files.items()):
        print("%-48s %d" % (k, v))
