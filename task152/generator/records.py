"""The exports the pack ships, each read off the world the way its own system writes it: the two SCADA layouts, the
2025 hourly inverter export, the met station's hourly file and the inverters' event log, the O&M contractor's work
orders, the district's account exports and service-point list, the desk's blotter, the irradiance provider's
long-term record and the forward curve. Nothing here is tuned; every value is a reading of the world."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import common as K
import world as Wm

UTC_OFF = dt.timedelta(hours=7)          # Arizona keeps mountain standard time: UTC = local + 7 hours
TMOD_NOISE, TAMB_NOISE = 0.15, 0.10      # the met station's daily temperature readings' scatter, degrees C

F_OLD = "hrs_scada_daily_report_2015-11-20_to_2020-03-02.csv"
F_NEW = "hadley_scada_daily_2020-03-03_to_2026-09-30.csv"
F_TAGS = "scada_tag_crosswalk.csv"
F_HOURLY = "inverter_hourly_ac_2025.csv"
F_MET = "met_station_hourly_2025.csv"
F_EVENTS = "inverter_event_log_2025.csv"
F_WO = "tresco_work_orders_hadley_ranch_2015-2026.xlsx"
F_LEGACY = "vsipd_acct_7731-0459_daily_legacy_2015-2020.txt"
F_MDM = "vsipd_acct_7731-0459_mdm_daily_2019-10-01_2025-12-31.csv"
F_SP = "vsipd_acct_7731-0459_service_points.csv"
F_BLOTTER = "power_forward_blotter_2015-2025.xlsx"
F_LT = "clearfield_hadley_ranch_poa_hourly_2001-2025.csv"
F_CURVE = "palo_verde_forwards_cal2027_2026-10-05.csv"

ACCOUNT = "7731-0459"
SP_GEN, SP_STN = "0417", "0418"
METER_GEN, METER_STN = "69R0417A", "12S0418C"


def tag_old(i):
    return K.OLD_TAGS[i]


def utc(t):
    return (t + UTC_OFF).strftime("%Y-%m-%dT%H:%M:%SZ")


def f4(x):
    return "%.4f" % (x + 0.0)


def f1(x):
    return "%.1f" % (x + 0.0)


# ---------------------------------------------------------------------------------------------------- the SCADA
def sensors(W):
    """The met station's readings as the SCADA keeps them: the pyranometer's daily irradiation (already carrying its
    scatter), the back-of-module sensor's irradiance-weighted daily temperature and the air temperature."""
    r = K.rng("sensors")
    nd = len(W.plant_days)
    W.tmod_w_meas = W.tmod_w + r.normal(0.0, TMOD_NOISE, nd)
    W.tamb_meas = W.tamb_d + r.normal(0.0, TAMB_NOISE, nd)
    r2 = K.rng("scada-meter")
    W.scada_exp = W.del_d * (1.0 + r2.normal(0.0, 0.0002, nd))
    W.scada_imp = W.rec_d * (1.0 + r2.normal(0.0, 0.0005, nd))
    # the original SCADA server's three lost days in August 2018 (a failed disk, rebuilt from backup without them)
    W.old_lost = {dt.date(2018, 8, 14), dt.date(2018, 8, 15), dt.date(2018, 8, 16)}


OLD_COLS = (["Date", "POA_Irr_kWh/m2", "TMod_IW_C", "TAmb_C"]
            + [c for t in K.OLD_TAGS for c in ("%s_DC_kWh" % t, "%s_AC_kWh" % t, "%s_OpHrs" % t)]
            + ["Meter_Export_kWh", "Meter_Import_kWh"])


def old_rows(W):
    for i, d in enumerate(W.plant_days):
        if d >= K.SCADA_CUTOVER:
            break
        if d in W.old_lost:
            continue
        row = ["%d/%d/%d" % (d.month, d.day, d.year), "%.3f" % W.pyr_d[i], f1(W.tmod_w_meas[i]), f1(W.tamb_meas[i])]
        for j in range(K.N_INV):
            row += [f1(W.dc_d[i, j]), f1(W.ac_d[i, j]), "%.2f" % W.op_hours[i, j]]
        row += [f1(W.scada_exp[i]), f1(W.scada_imp[i])]
        yield row


NEW_COLS = ["day_start_utc", "device", "point", "value", "unit"]


def new_rows(W):
    for i, d in enumerate(W.plant_days):
        if d < K.SCADA_CUTOVER:
            continue
        stamp = utc(dt.datetime(d.year, d.month, d.day))
        yield [stamp, "MET-01", "H_POA", "%.3f" % W.pyr_d[i], "kWh/m2"]
        yield [stamp, "MET-01", "T_MOD_IW", f1(W.tmod_w_meas[i]), "degC"]
        yield [stamp, "MET-01", "T_AMB", f1(W.tamb_meas[i]), "degC"]
        for j in range(K.N_INV):
            tag = K.new_tag(j, d)
            for pt, v, u in (("E_DC", W.dc_d[i, j] / 1000.0, "MWh"), ("E_AC", W.ac_d[i, j] / 1000.0, "MWh"),
                             ("T_OP", W.op_hours[i, j], "h")):
                yield [stamp, tag, pt, f4(v) if u == "MWh" else "%.2f" % v, u]
        yield [stamp, "PLANT-RM", "E_EXP", f4(W.scada_exp[i] / 1000.0), "MWh"]
        yield [stamp, "PLANT-RM", "E_IMP", f4(W.scada_imp[i] / 1000.0), "MWh"]


TAG_COLS = ["original_tag", "scada_tag", "block", "in_service_from", "in_service_to", "note"]


def tag_rows():
    out = []
    for i in range(K.N_INV):
        if i == K.INV07:
            out.append([K.OLD_TAGS[i], K.NEW_TAGS[i], "B%d" % (i // 4 + 1), K.COD.isoformat(),
                        (K.INV07_SWAP - dt.timedelta(days=1)).isoformat(), "power stage fire 2 Mar 2021, unit scrapped"])
            out.append(["", K.NEW_TAG_07R, "B%d" % (i // 4 + 1), K.INV07_SWAP.isoformat(), "",
                        "replacement inverter, same array and transformer"])
        else:
            out.append([K.OLD_TAGS[i], K.NEW_TAGS[i], "B%d" % (i // 4 + 1), K.COD.isoformat(), "", ""])
    out.append(["MET", "MET-01", "", K.COD.isoformat(), "", "plane-of-array pyranometer and back-of-module sensor, block 2"])
    out.append(["METER", "PLANT-RM", "", K.COD.isoformat(), "", "revenue meter read by the SCADA (district meter 69R0417A)"])
    return out


# ---------------------------------------------------------------------------------------------------- 2025, hourly
def hours_2025(W):
    a = W.day_index[dt.date(2025, 1, 1)]
    b = W.day_index[dt.date(2025, 12, 31)]
    return a, b


MET_COLS = ["hour_beginning_mst", "poa_wm2", "ghi_wm2", "tamb_c", "tmod_c", "wind_ms"]


def met_rows(W):
    a, b = hours_2025(W)
    r = K.rng("met-hourly")
    for i in range(a, b + 1):
        d = W.plant_days[i]
        scale = W.pyr_d[i] / W.poa_d[i] if W.poa_d[i] > 0 else 1.0
        for h in range(24):
            poa = W.poa[i, h] * scale
            ghi = W.ghi[i, h] * (1.0 + r.normal(0.0, 0.004))
            yield ["%s %02d:00" % (d.isoformat(), h), f1(max(poa, 0.0)), f1(max(ghi, 0.0)), f1(W.tamb[i, h]),
                   f1(W.tmod[i, h] + r.normal(0.0, 0.2)), f1(W.wind[i, h])]


HOURLY_COLS = ["interval_end_utc", "device", "ac_kwh", "ac_register_kwh"]


def hourly_rows(W):
    """Each inverter's AC energy in each hour of 2025 and its lifetime AC register at the hour's end, as the four
    block data loggers forward them. While a logger's link is down its block's hours are not forwarded; the
    inverters' registers keep counting."""
    a, b = hours_2025(W)
    start_reg = np.zeros(K.N_INV)
    swap = W.day_index[K.INV07_SWAP]
    r = K.rng("registers")
    base = r.integers(18, 140, K.N_INV).astype(float)      # factory and commissioning energy on each counter
    for j in range(K.N_INV):
        lo = swap if j == K.INV07 else 0
        start_reg[j] = base[j] + W.ac_d[lo:a, j].sum()
    gap_hours = set()
    for (blk, st, hrs) in W.logger_gaps:
        for k in range(hrs):
            gap_hours.add((blk, st + dt.timedelta(hours=k)))
    cum = start_reg.copy()
    for i in range(a, b + 1):
        d = W.plant_days[i]
        for h in range(24):
            t0 = dt.datetime(d.year, d.month, d.day, h)
            end = utc(t0 + dt.timedelta(hours=1))
            for j in range(K.N_INV):
                e = float(W.ac_h[i, h, j])
                cum[j] += e
                if (K.BLOCK_OF[j], t0) in gap_hours:
                    continue
                yield [end, K.new_tag(j, d), f1(e), "%d" % math.floor(cum[j])]


EVENT_COLS = ["event_id", "device", "code", "description", "raised_utc", "cleared_utc", "ack_by"]
CODES = {"F-305": "POWER STAGE FAULT", "F-217": "AC GRID FAULT", "S-020": "REMOTE STOP", "W-410": "POWER STAGE DERATE",
         "W-118": "FAN FAULT"}
CONTROL_ROOM = ["swhitehead", "jdavila", "ryang", "hstout"]


def event_rows(W):
    r = K.rng("event-log")
    y0, y1 = dt.datetime(2025, 1, 1), dt.datetime(2026, 1, 1)
    rows = []

    def push(tag, code, raised, cleared, who):
        rows.append([tag, code, CODES[code], raised, cleared, who])

    for ev in W.events:
        if not (y0 <= ev["start"] < y1):
            continue
        invs = list(range(K.N_INV)) if ev["inv"] is None else [ev["inv"]]
        if ev["cause"] == "line":
            for j in invs:
                ra = ev["start"] + dt.timedelta(seconds=int(r.integers(0, 9)))
                cl = ev["end"] - dt.timedelta(seconds=int(r.integers(0, 80)))
                push(K.new_tag(j, ev["start"].date()), "F-217", ra, cl, "")
        elif ev["cause"] == "relay":
            j = invs[0]
            push(K.new_tag(j, ev["start"].date()), "F-217", ev["start"] + dt.timedelta(seconds=int(r.integers(0, 50))),
                 ev["end"], CONTROL_ROOM[int(r.integers(1, 4))])
        elif ev["cause"] == "fault":
            j = invs[0]
            tag = K.new_tag(j, ev["start"].date())
            who = CONTROL_ROOM[int(r.integers(1, 4))]
            push(tag, "F-305", ev["start"] + dt.timedelta(seconds=int(r.integers(0, 50))), ev["end"], who)
            work = dt.timedelta(minutes=int(r.integers(70, 260)))
            st = max(ev["start"] + dt.timedelta(minutes=20), ev["end"] - work)
            push(tag, "S-020", st, ev["end"] - dt.timedelta(minutes=int(r.integers(1, 4))), who)
        elif ev["cause"] == "owner":
            j = invs[0]
            push(K.new_tag(j, ev["start"].date()), "S-020", ev["start"], ev["end"], "swhitehead")
    for (j, t, dur) in W.derates:
        d0 = W.plant_days[t]
        if d0.year != 2025:
            continue
        d1 = W.plant_days[min(t + dur - 1, len(W.plant_days) - 1)]
        ra = dt.datetime(d0.year, d0.month, d0.day, 6, int(r.integers(10, 55)))
        cl = dt.datetime(d1.year, d1.month, d1.day, 17, int(r.integers(30, 59)))
        push(K.new_tag(j, d0), "W-410", ra, cl, CONTROL_ROOM[int(r.integers(1, 4))])
    a, _ = hours_2025(W)
    for j in range(K.N_INV):
        for _ in range(int(r.integers(3, 9))):
            t = a + int(r.integers(120, 270))          # the hot months
            d = W.plant_days[t]
            ra = dt.datetime(d.year, d.month, d.day, int(r.integers(11, 16)), int(r.integers(0, 60)))
            push(K.new_tag(j, d), "W-118", ra, ra + dt.timedelta(minutes=int(r.integers(4, 95))), "")
    rows.sort(key=lambda x: (x[3], x[0], x[1]))
    out = []
    for n, (tag, code, desc, ra, cl, who) in enumerate(rows):
        out.append(["E25-%05d" % (10417 + n), tag, code, desc, utc(ra), utc(cl), who])
    return out


# ---------------------------------------------------------------------------------------------------- work orders
WO_COLS = ["WO #", "Type", "Asset", "Description", "Created", "Completed", "Labor hrs", "Assigned"]
TECHS = ["jdavila", "ryang", "hstout"]


def _block_asset(b):
    return "BLK%d" % (b + 1)


def _cln_text(rc, n, done, annual):
    """A wash work order's description as the crews type it into the CMMS: the block in whatever form, a few notes,
    now and then a typo or a bare entry."""
    pick = lambda xs: xs[int(rc.integers(0, len(xs)))]
    blk = pick(["Block %d", "Blk %d", "BLK%d", "B%d", "blk %d", "block %d", "Blk%d"]) % n
    if rc.random() < 0.06:
        return pick(["%s wash" % blk, "WASH %s - see crew sheet" % blk, "cleaning %s" % blk, "%s" % blk,
                     "wash %s, notes on daily log" % blk])
    head = pick(["Full wash %s" % blk, "%s full module wash" % blk, "Module wash %s" % blk, "Wash %s complete" % blk,
                 "%s washed, all rows" % blk, "PV module cleaning %s" % blk, "Cleaned %s modules" % blk,
                 "%s wash - all tables" % blk, "Panel wash %s" % blk, "Washed %s" % blk])
    notes = []
    water = ["DI water", "DI trailer + 2 water trucks", "Well 2 water thru DI unit", "DI resin changed mid shift",
             "TDS at nozzle %d ppm" % int(rc.integers(3, 10)), "brush tractor + DI rinse", "soft brush, no pressure washer",
             "water truck #2 down, finished w/ #1", "DI unit alarm at 0545, reset", ""]
    crew = ["crew of %d" % int(rc.integers(4, 9)), "%d techs + %d temp labor" % (int(rc.integers(2, 4)), int(rc.integers(2, 5))),
            "night crew, started %02d:%02d" % (int(rc.integers(3, 5)), int(rc.integers(0, 4)) * 15),
            "started 0%d%02d" % (int(rc.integers(3, 5)), int(rc.integers(0, 4)) * 15),
            "done ~%s" % done.strftime("%H%M"), "finished by %s" % done.strftime("%H:%M"), ""]
    seen = ["heavy dust on lower edge of modules", "bird droppings rows %d-%d" % (int(rc.integers(10, 40)), int(rc.integers(41, 80))),
            "2nd pass on rows 1-%d (caked)" % int(rc.integers(8, 25)), "light dust only", "no damage found",
            "1 module w/ broken glass row %d, tagged" % int(rc.integers(1, 100)),
            "combiner %d door latch broken, reported" % int(rc.integers(1, 25)), "gate code changed by owner",
            "wind came up, paused %d min" % int(rc.integers(2, 6) * 10), "access road soft, trucks slow",
            "fence line weeds noted for VEG", "inverter pads hosed down", "", "", ""]
    for pool in (water, crew, seen):
        x = pick(pool)
        if x:
            notes.append(x)
    if annual and rc.random() < 0.25:
        notes.append(pick(["annual wash per sched 2", "Sched 2 annual", "1 blk/wk per well permit"]))
    txt = head + (". " if rc.random() < 0.6 else ", ") + ", ".join(notes) if notes else head
    if rc.random() < 0.08:
        for a, b in (("wash", "wahs"), ("modules", "modlues"), ("complete", "compelte"), ("Block", "Blcok"),
                     ("trailer", "trialer"), ("finished", "finsihed"), ("techs", "tecs")):
            if a in txt:
                txt = txt.replace(a, b, 1)
                break
    if rc.random() < 0.15:
        txt = txt.upper()
    elif rc.random() < 0.5:
        txt = txt + "."
    return txt


def wo_rows(W):
    r = K.rng("work-orders")
    rows = []
    wash_texts = [
        "Full module wash, Block {b}. DI water, two trucks, night shift.",
        "Module wash Blk {b} complete, all tables.",
        "Wash Block {b} modules (full wash).",
        "Block {b} full wash done. Water from Well 2 via DI trailer.",
        "Full wash B{b}, all strings. Crew of 6, started 04:30.",
    ]
    by_no = {}
    for no, b, d in W.wash_events:
        by_no.setdefault(no, []).append((b, d))
    rc = K.rng("work-orders-cln")
    for no in sorted(by_no):
        for b, d in by_no[no]:
            if no != 1:
                r.integers(0, len(wash_texts))           # the export's first text draw, kept so later fields hold
            done = dt.datetime(d.year, d.month, d.day, int(r.integers(9, 12)), int(r.integers(0, 60)))
            made = done - dt.timedelta(days=int(r.integers(5, 15)), hours=int(r.integers(1, 7)))
            txt = ("Post-construction module wash, Block %d (handover)." % (b + 1)) if no == 1 else \
                _cln_text(rc, b + 1, done, d.year >= 2021)
            rows.append(["CLN", _block_asset(b), txt, made, done, round(float(r.uniform(38, 56)), 1),
                         TECHS[int(r.integers(0, 3))]])
    stage_by = {}
    for (i, t_end, stage, loss) in W.stage_events:
        stage_by[(i, t_end)] = stage
    for ev in W.events:
        invs = list(range(K.N_INV)) if ev["inv"] is None else [ev["inv"]]
        if ev["start"].date() > K.HIST_END:
            continue
        if ev["cause"] in ("fault", "fire"):
            j = invs[0]
            asset = K.OLD_TAGS[j] if ev["start"].date() < K.SCADA_CUTOVER else K.new_tag(j, ev["start"].date())
            t_end = (ev["end"].date() - K.COD).days
            st = stage_by.get((j, t_end))
            if ev["cause"] == "fire":
                rows.append(["CM", asset, "Power stage fire on inverter. Site isolated, fire crew attended. Unit "
                             "destroyed, replacement inverter ordered.", ev["start"], ev["start"] + dt.timedelta(hours=6),
                             9.5, "jdavila"])
                rows.append(["CM", K.NEW_TAG_07R, "Replacement inverter set on pad, terminated and commissioned. New "
                             "SCADA tag B2-INV3R.", ev["end"] - dt.timedelta(days=9), ev["end"], 64.0, "jdavila"])
                continue
            if st:
                txt = ("F-305 power stage fault. PS%d failed, replaced with refurbished exchange stage (S/N RX-%04d). "
                       "Tested and returned to service." % (st, int(r.integers(1000, 9999))))
            else:
                ps = int(r.integers(1, 3))
                txt = ["F-305 trip. Replaced gate driver board on PS%d, returned to service." % ps,
                       "Inverter down on F-305. DC link fuse F%d replaced, restarted." % int(r.integers(1, 7)),
                       "F-305 power stage fault. Reseated IGBT connectors on PS%d, tested, back online." % ps,
                       "Power stage fault F-305. Swapped control board (spare from stores), restarted after checks.",
                       "F-305 on PS%d. Cooling fan seized, fan and filter replaced, cleared and restarted." % ps,
                       "F-305. Found burnt snubber capacitor on PS%d, replaced, insulation test OK, back in service." % ps,
                       "Inverter tripped F-305. Reset failed; replaced current sensor on PS%d, returned to service." % ps,
                       "F-305 power stage fault. Waited on part from vendor (IGBT driver), fitted and tested."][
                    int(r.integers(0, 8))]
            hrs = round(float(r.uniform(2.5, 9.0)), 1)
            rows.append(["CM", asset, txt, ev["start"] + dt.timedelta(minutes=int(r.integers(5, 90))), ev["end"], hrs,
                         TECHS[int(r.integers(0, 3))]])
        elif ev["cause"] == "relay":
            j = invs[0]
            asset = K.OLD_TAGS[j] if ev["start"].date() < K.SCADA_CUTOVER else K.new_tag(j, ev["start"].date())
            txt = ["Inverter offline, F-217. AC relay found latched, reset, inverter restarted.",
                   "F-217 on inverter. Reset AC contactor relay, back online.",
                   "Reset AC relay after F-217 trip. No fault found on AC side.",
                   "Found inverter stopped on F-217, grid voltage normal at the time. Relay reset, running.",
                   "F-217 latched. Checked AC breaker and relay coil, reset, restarted OK.",
                   "Inverter off on F-217 since the morning round. AC relay reset; logged for vendor follow-up."][
                int(r.integers(0, 6))]
            rows.append(["CM", asset, txt, ev["start"] + dt.timedelta(minutes=int(r.integers(10, 80))), ev["end"],
                         round(float(r.uniform(0.5, 1.5)), 1), TECHS[int(r.integers(0, 3))]])
    for invs, a, b, why in W.owner_stops:
        names = ", ".join(K.new_tag(j, a.date()) for j in invs)
        rows.append(["OWN", "SITE", "Owner request (S. Sloan): stop %s for %s. Stopped %s, restarted %s." % (
            names, why, a.strftime("%H:%M"), b.strftime("%H:%M")), a - dt.timedelta(days=6), b, 2.0, "jdavila"])
    # routine work: night PM on each inverter twice a year, the met station, vegetation and the substation yard
    d = dt.date(2016, 1, 1)
    while d <= K.HIST_END:
        if d.month in (3, 9) and d.day == 1:
            for j in range(K.N_INV):
                dd = d + dt.timedelta(days=int(r.integers(2, 26)))
                done = dt.datetime(dd.year, dd.month, dd.day, int(r.integers(1, 5)), int(r.integers(0, 60)))
                asset = K.OLD_TAGS[j] if dd < K.SCADA_CUTOVER else K.new_tag(j, dd)
                rows.append(["PM", asset, "Night PM: filters, torque check, IR scan of AC bus, firmware check.",
                             done - dt.timedelta(days=20), done, round(float(r.uniform(3.0, 5.5)), 1),
                             TECHS[int(r.integers(0, 3))]])
        if d.day == 1:
            dd = d + dt.timedelta(days=int(r.integers(0, 10)))
            done = dt.datetime(dd.year, dd.month, dd.day, int(r.integers(7, 11)), int(r.integers(0, 60)))
            rows.append(["PM", "MET-01", "Met station monthly check: pyranometer dome cleaned, level checked, module "
                         "temperature sensor bond checked.", done - dt.timedelta(days=3), done, 0.8,
                         TECHS[int(r.integers(0, 3))]])
            if d.month in (4, 10):
                dd = d + dt.timedelta(days=int(r.integers(10, 20)))
                done = dt.datetime(dd.year, dd.month, dd.day, 15, int(r.integers(0, 60)))
                rows.append(["VEG", "SITE", "Weed and brush control, all blocks and perimeter road.",
                             done - dt.timedelta(days=12), done, round(float(r.uniform(20, 34)), 1), "hstout"])
            if d.month == 6:
                dd = d + dt.timedelta(days=int(r.integers(3, 20)))
                done = dt.datetime(dd.year, dd.month, dd.day, 14, int(r.integers(0, 60)))
                rows.append(["PM", "MET-01", "Annual pyranometer exchange for the recalibrated spare.",
                             done - dt.timedelta(days=15), done, 1.5, "jdavila"])
        d += dt.timedelta(days=1)
    for y in range(2016, 2026):
        dd = dt.date(y, 5, int(r.integers(5, 25)))
        done = dt.datetime(dd.year, dd.month, dd.day, 13, int(r.integers(0, 60)))
        rows.append(["INSP", "SITE", "Annual IR survey of the array (drone).", done - dt.timedelta(days=21), done,
                     round(float(r.uniform(14, 22)), 1), "ryang"])
    special = [
        (dt.datetime(2019, 6, 20, 15, 10), "INSP", "SITE", "Backsheet cracking found on modules in all blocks during IR "
         "survey follow-up. Sample of 400 modules logged, photos to owner."),
        (dt.datetime(2025, 9, 26, 16, 0), "PROJ", "BLK3", "Install two side-by-side tables (Corvane) at north edge of "
         "block 3 with string inverters and DC meters."),
        (dt.datetime(2025, 9, 30, 11, 30), "PROJ", "BLK3", "Side-by-side tables energised, data to Corvane logger. "
         "Weekly wash of both tables added to site rounds."),
        (dt.datetime(2026, 10, 5, 7, 0), "PROJ", "BLK1", "Block 1 locked out for module removal (replacement works "
         "start). Inverters B1-INV1 to B1-INV4 isolated."),
    ]
    for when, typ, asset, txt in special:
        rows.append([typ, asset, txt, when - dt.timedelta(days=4), when, 6.0, "jdavila"])
    rows.sort(key=lambda x: (x[3], x[1], x[0], x[2]))
    out = []
    for n, row in enumerate(rows):
        typ, asset, txt, made, done, hrs, who = row
        if made.year < 2016:
            no = "WO-15-%04d" % (n + 1)
        else:
            no = "WO-%s-%05d" % (str(made.year)[2:], 20417 + n)
        out.append([no, typ, asset, txt, made, done, hrs, who])
    return out


def write_xlsx(path, sheet, cols, rows, widths, datefmt="mm/dd/yyyy hh:mm", date_cols=(), num_cols=()):
    wb = Workbook()
    ws = wb.active
    ws.title = sheet
    ws.append(cols)
    for c in range(1, len(cols) + 1):
        ws.cell(row=1, column=c).font = Font(bold=True)
        ws.cell(row=1, column=c).fill = PatternFill("solid", fgColor="D9E1EA")
    for row in rows:
        ws.append(row)
    for c, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(c)].width = w
    for c in date_cols:
        for rr in range(2, len(rows) + 2):
            ws.cell(row=rr, column=c).number_format = datefmt
    for c, fmt in num_cols:
        for rr in range(2, len(rows) + 2):
            ws.cell(row=rr, column=c).number_format = fmt
    ws.freeze_panes = "A2"
    wb.save(path)
    return len(rows)


# ---------------------------------------------------------------------------------------------------- the district
def district(W):
    """The district's view of the account: service point 0417 (the generation interconnection, channels as the
    district sees them: REC the energy it received from the plant, DEL the energy it delivered to it) and, to its
    retirement on 17 April 2024, service point 0418 (the 12 kV retail supply to the control building and well)."""
    r = K.rng("district")
    nd = len(W.plant_days)
    W.sp_rec = np.round(W.del_d * (1.0 + r.normal(0.0, 0.00005, nd)), 1)
    W.sp_del = np.round(W.rec_d * (1.0 + r.normal(0.0, 0.00005, nd)), 1)
    W.sp418 = np.round(np.where(np.array([d < K.STATION_SERVICE_END for d in W.plant_days]),
                                W.station_d * (1.0 + r.normal(0.0, 0.06, nd)), 0.0), 1)
    # the meter's communication failure of June 2025: the meter data system estimated the days, then loaded the
    # actual reads after the manual download
    W.mdm_est_days = [dt.date(2025, 6, 3) + dt.timedelta(days=k) for k in range(7)]
    W.mdm_est = {}
    for d in W.mdm_est_days:
        i = W.day_index[d]
        prev = [W.day_index[d - dt.timedelta(days=7 * k)] for k in (1, 2)]
        W.mdm_est[d] = (round(float(np.mean([W.sp_rec[p] for p in prev])), 1),
                        round(float(np.mean([W.sp_del[p] for p in prev])), 1))


def legacy_lines(W):
    """The district's legacy billing system's daily export, fixed width: account, service point, meter, channel,
    the interval's end date and time (a day's total ends at 0000 of the next day), kWh to one decimal, read
    status."""
    out = []
    for i, d in enumerate(W.plant_days):
        if d > dt.date(2020, 2, 29):
            break
        end = d + dt.timedelta(days=1)
        stamp = "%s 0000" % end.strftime("%Y%m%d")
        recs = [(SP_GEN, METER_GEN, "REC", W.sp_rec[i]), (SP_GEN, METER_GEN, "DEL", W.sp_del[i])]
        if d < K.STATION_SERVICE_END:
            recs.append((SP_STN, METER_STN, "DEL", W.sp418[i]))
        for sp, meter, ch, v in recs:
            out.append("%-10s%-6s%-10s%-4s%s %13.1f A" % (ACCOUNT.replace("-", ""), sp, meter, ch, stamp, v))
    return out


MDM_COLS = ["service_point", "meter_id", "channel", "read_date", "kwh", "read_type", "version", "loaded_utc"]


def mdm_rows(W):
    """The district's meter data system from its go-live (history loaded back to 1 October 2019) to the end of 2025:
    one row per service point, channel and day, every version kept."""
    r = K.rng("mdm")
    out = []
    golive = dt.datetime(2020, 3, 9, 14, 12)
    for i, d in enumerate(W.plant_days):
        if d < dt.date(2019, 10, 1) or d > dt.date(2025, 12, 31):
            continue
        if d < dt.date(2020, 3, 1):
            loaded = golive + dt.timedelta(minutes=int(r.integers(0, 40)))
        else:
            loaded = dt.datetime(d.year, d.month, d.day, 9, 0) + dt.timedelta(days=1, minutes=int(r.integers(0, 90)))
        loaded_s = (loaded + UTC_OFF).strftime("%Y-%m-%d %H:%M:%S")
        if d in W.mdm_est:
            er, ed = W.mdm_est[d]
            out.append([SP_GEN, METER_GEN, "REC", d.isoformat(), "%.1f" % er, "E", "1", loaded_s])
            out.append([SP_GEN, METER_GEN, "DEL", d.isoformat(), "%.1f" % ed, "E", "1", loaded_s])
            later = (dt.datetime(2025, 6, 12, 15, 41) + UTC_OFF).strftime("%Y-%m-%d %H:%M:%S")
            out.append([SP_GEN, METER_GEN, "REC", d.isoformat(), "%.1f" % W.sp_rec[i], "A", "2", later])
            out.append([SP_GEN, METER_GEN, "DEL", d.isoformat(), "%.1f" % W.sp_del[i], "A", "2", later])
        else:
            out.append([SP_GEN, METER_GEN, "REC", d.isoformat(), "%.1f" % W.sp_rec[i], "A", "1", loaded_s])
            out.append([SP_GEN, METER_GEN, "DEL", d.isoformat(), "%.1f" % W.sp_del[i], "A", "1", loaded_s])
        if d < K.STATION_SERVICE_END:
            out.append([SP_STN, METER_STN, "DEL", d.isoformat(), "%.1f" % W.sp418[i], "A", "1", loaded_s])
    return out


SP_COLS = ["account", "service_point", "rate_code", "rate_name", "premise", "meter_id", "voltage_kv", "status",
           "start_date", "end_date"]


def sp_rows():
    return [
        [ACCOUNT, SP_GEN, "GEN-IC", "Generator interconnection (wholesale)", "Hadley Ranch Solar, 69 kV point of "
         "interconnection, Hadley Ranch substation", METER_GEN, "69", "ACTIVE", "2015-10-29", ""],
        [ACCOUNT, SP_STN, "GS-3", "General service, secondary, demand metered", "Hadley Ranch Solar control building "
         "and Well 2, 12 kV Vado Seco feeder 12-14", METER_STN, "12.47", "FINAL", "2015-06-01", "2024-04-17"],
    ]


# ---------------------------------------------------------------------------------------------------- the desk
def hedges(W):
    """The desk's trades: each autumn the next calendar year sold forward to Westmark at the volume the desk then set
    (in one or two tranches), the 2019 and 2022 buy-backs, and the 2021 and 2024 amendments, which the confirmations
    carry and the blotter does not."""
    r = K.rng("desk")
    net = {y: float(W.sp_rec[[i for i, d in enumerate(W.plant_days) if d.year == y]].sum()
                    - W.sp_del[[i for i, d in enumerate(W.plant_days) if d.year == y]].sum()) / 1000.0
           for y in range(2016, 2026)}
    W.net_year = net
    vols = {}
    prev = 69.0
    for y in range(2016, 2027):
        if y == 2016:
            v = 69000
        else:
            base = net[min(y - 1, 2025)] if y - 1 <= 2025 else net[2025]
            v = int(math.floor((base * float(r.uniform(0.915, 0.955))) / 1000.0)) * 1000
            v = min(v, int(prev * 1000))
        vols[y] = v
        prev = v / 1000.0
    W.sold_original = vols
    W.buybacks = {2019: 1400, 2022: 1100}
    W.amended = {2021: vols[2021] - 2500, 2024: vols[2024] - 1800}
    trades = []
    for y in range(2016, 2027):
        td = dt.date(y - 1, 10, int(r.integers(9, 20)))
        while td.weekday() >= 5:
            td += dt.timedelta(days=1)
        q = vols[y]
        if y in (2016, 2019, 2023):
            q1 = int(round(q * 0.6 / 1000.0)) * 1000
            parts = [q1, q - q1]
        else:
            parts = [q]
        for k, qq in enumerate(parts):
            trades.append(dict(date=td + dt.timedelta(days=7 * k), year=y, side="S", qty=qq,
                               price=round(float(r.uniform(27.5, 48.0)) + (y - 2016) * 0.9, 2)))
    trades.append(dict(date=dt.date(2019, 6, 11), year=2019, side="B", qty=W.buybacks[2019], price=31.85))
    trades.append(dict(date=dt.date(2022, 8, 23), year=2022, side="B", qty=W.buybacks[2022], price=58.40))
    trades.sort(key=lambda t: (t["date"], t["year"]))
    W.trades = []
    for n, t in enumerate(trades):
        t["id"] = "MVB-%s-%03d" % (t["date"].strftime("%y%m"), 11 + n)
        W.trades.append(t)
    W.amend_trade = {}
    for y in (2021, 2024):
        W.amend_trade[y] = [t for t in W.trades if t["year"] == y and t["side"] == "S"][0]["id"]


BLOTTER_COLS = ["Trade ID", "Trade date", "Counterparty", "Product", "Delivery", "B/S", "Quantity (MWh)",
                "Price ($/MWh)", "Status", "Trader"]


def blotter_rows(W):
    out = []
    for t in W.trades:
        out.append([t["id"], t["date"], "Westmark Power Trading LLC", "PV Solar Fixed Volume (Hadley Ranch shape)",
                    "CY%d" % t["year"], t["side"], t["qty"], t["price"], "Confirmed", "klara"])
    return out


CURVE_COLS = ["contract_month", "on_peak_usd_mwh", "off_peak_usd_mwh", "solar_shape_usd_mwh", "curve_date"]


def curve_rows():
    r = K.rng("curve")
    shape = {1: 0.82, 2: 0.80, 3: 0.71, 4: 0.64, 5: 0.66, 6: 0.97, 7: 1.32, 8: 1.36, 9: 1.08, 10: 0.78, 11: 0.79, 12: 0.86}
    out = []
    for m in range(1, 13):
        on = 46.0 * shape[m] * float(r.uniform(0.97, 1.03)) + 8.0
        off = on * float(r.uniform(0.74, 0.84))
        sol = on * float(r.uniform(0.70, 0.80))
        out.append(["2027-%02d" % m, "%.2f" % on, "%.2f" % off, "%.2f" % sol, "2026-10-05"])
    return out


# ---------------------------------------------------------------------------------------------------- the long-term record
LT_COLS = ["period_end_utc", "ghi_wm2", "dhi_wm2", "poa_wm2"]


def lt_header():
    return [
        "# Clearfield Solar Resource, site-adapted irradiance time series",
        "# Site: Hadley Ranch Solar, Pinal County, Arizona. Latitude 32.940 N, longitude 111.620 W, elevation 471 m",
        "# Plane of array: fixed, tilt 25 degrees, azimuth 180 degrees (south), ground albedo 0.27",
        "# Period: 2001-01-01 to 2025-12-31, hourly. Time stamps are the end of each hour in UTC (site time is UTC-7)",
        "# Values: mean irradiance over the hour, W/m2. POA is the global irradiance on the plane of array",
        "# Site adaptation: satellite model series adapted to the plant's plane-of-array pyranometer, 2016 to 2024",
        "# Delivered: 20 January 2026, order CSR-26-0071",
    ]


def lt_rows(W):
    """The provider's hourly series: the site's own weather seen through a satellite model, its hourly and daily
    errors left in and its long-run level adapted to the plant's pyranometer."""
    for y in range(2001, 2026):
        w = W.wx[y]
        r = K.rng("provider", y)
        n = w["n"]
        hr = np.exp(r.normal(0.0, 0.07, 24 * n) - 0.07 ** 2 / 2)
        dy = np.repeat(np.exp(r.normal(0.0, 0.018, n) - 0.018 ** 2 / 2), 24)
        yr = 1.0 + float(r.normal(0.0, 0.003))
        f = hr * dy * yr
        ghi = np.where(w["ghi"] > 0, w["ghi"] * f, 0.0)
        dhi = np.where(w["dhi"] > 0, np.minimum(w["dhi"] * f * np.exp(r.normal(0.0, 0.05, 24 * n)), ghi), 0.0)
        poa = np.where(w["poa"] > 0, w["poa"] * f, 0.0)
        for k in range(24 * n):
            d = w["dates"][k // 24]
            t0 = dt.datetime(d.year, d.month, d.day, k % 24)
            yield [(t0 + dt.timedelta(hours=1) + UTC_OFF).strftime("%Y-%m-%d %H:%M"), "%d" % round(ghi[k]),
                   "%d" % round(dhi[k]), "%d" % round(poa[k])]
