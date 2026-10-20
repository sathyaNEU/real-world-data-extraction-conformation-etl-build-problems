"""The pack's data files, each as its source system exports it."""
import csv
import datetime as dt

import numpy as np
import openpyxl
import pyarrow as pa
import pyarrow.parquet as pq
from openpyxl.styles import Alignment, Font

import wind as WD
import world as W

SCADA = "scada_10min_2025-10_2026-09.parquet"
MAST = "metmast_M1_10min_2025-10_2026-09.csv"
ANM = "anm_instructions_glenrigg_2025-10_2026-09.csv"
STATES = "hallvard_H93_state_codes.xlsx"
LIFTS = "crane_lift_log_2026.xlsx"
LAYOUT = "site_layout_pads.csv"
REGISTER = "asset_register.xlsx"
COUNTERS = "monthly_production_2025-10_2026-09.csv"
WORKORDERS = "work_orders_2025-10_2026-09.csv"
METER = "export_meter_halfhourly_2025-10_2026-09.csv"
PRIOR = "lost_production_2024_25.xlsx"
BOLD = Font(bold=True)


def scada_stamp(k):
    """The SCADA's timestamp for interval k: its end, in UK local time on the site server, in UTC on the hosted
    platform from 3 February 2026."""
    e = W.end_of(k)
    if e <= W.MIGRATION:
        return e.astimezone(W.LONDON).replace(tzinfo=None)
    return e.replace(tzinfo=None)


def scada_table(m, T, ops):
    stamps = np.array([np.datetime64(scada_stamp(k), "s") for k in range(W.N)])
    cols = {c: [] for c in ("timestamp", "turbine", "wind_speed_mean", "wind_speed_sd", "nacelle_position",
                            "active_power_mean", "ambient_temperature", "state")}
    keep = {t: ~ops["silent"][t] for t in W.TURBINES}
    # rows in time order, the ten turbines within each interval
    idx = np.repeat(np.arange(W.N), len(W.TURBINES))
    tur = np.tile(np.arange(len(W.TURBINES)), W.N)
    mask = np.array([keep[W.TURBINES[j]][k] for k, j in zip(idx, tur)])
    idx, tur = idx[mask], tur[mask]
    v = np.vstack([np.round(T[t]["v"], 2) for t in W.TURBINES])
    sd = np.vstack([np.round(T[t]["sd"], 2) for t in W.TURBINES])
    nd = np.vstack([np.round(T[t]["ndir"], 1) for t in W.TURBINES])
    p = np.vstack([np.round(ops["power"][t], 1) for t in W.TURBINES])
    tc = np.vstack([np.round(T[t]["ntemp"], 1) for t in W.TURBINES])
    st = np.vstack([ops["state"][t] for t in W.TURBINES])
    names = np.array(W.TURBINES)
    table = pa.table({
        "timestamp": pa.array(stamps[idx], pa.timestamp("s")),
        "turbine": pa.array(names[tur].tolist(), pa.string()),
        "wind_speed_mean": pa.array(v[tur, idx], pa.float64()),
        "wind_speed_sd": pa.array(sd[tur, idx], pa.float64()),
        "nacelle_position": pa.array(nd[tur, idx], pa.float64()),
        "active_power_mean": pa.array(p[tur, idx], pa.float64()),
        "ambient_temperature": pa.array(tc[tur, idx], pa.float64()),
        "state": pa.array(st[tur, idx].astype(np.int16), pa.int16()),
    })
    return table, idx, tur


def write_scada(path, table):
    pq.write_table(table, path, compression="zstd", row_group_size=131072, use_dictionary=["turbine"])
    return table.num_rows


def mast_rows(m):
    """The mast logger's record: interval start in UTC, rounded as the logger stores it."""
    rows = []
    for k in range(W.N):
        rows.append((W.start_of(k).strftime("%Y-%m-%d %H:%M:%S"), "%.2f" % m["v"][k], "%.2f" % m["sd"][k],
                     "%.0f" % (m["dir"][k] % 360), "%.2f" % m["temp"][k], "%.1f" % m["pres"][k], "%.1f" % m["rh"][k]))
    return rows


def write_mast(path, rows):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["TIMESTAMP_UTC", "WS_80m_Avg", "WS_80m_Std", "WD_78m_Avg", "T_76m_Avg", "P_76m_Avg", "RH_76m_Avg"])
        w.writerows(rows)
    return len(rows)


def anm_rows(instr):
    rows = []
    for j, (a, b, lim) in enumerate(instr):
        sa, sb = W.start_of(a), W.start_of(b)
        issued = sa - dt.timedelta(minutes=4 + (j * 7) % 11, seconds=(j * 13) % 60)
        ref = "GZ-%s-%04d" % (sa.strftime("%y%m"), 101 + j)
        rows.append((ref, issued.strftime("%Y-%m-%dT%H:%M:%SZ"), sa.strftime("%Y-%m-%dT%H:%M:%SZ"),
                     sb.strftime("%Y-%m-%dT%H:%M:%SZ"), "%.1f" % lim, "Trip" if lim == 0 else "Export limit"))
    return rows


def write_anm(path, rows):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["instruction_ref", "issued_utc", "start_utc", "end_utc", "export_limit_mw", "instruction"])
        w.writerows(rows)
    return len(rows)


def _sheet(ws, header, widths):
    ws.append(header)
    for c in ws[1]:
        c.font = BOLD
    for i, wd in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wd
    ws.freeze_panes = "A2"


STATE_ROWS = [
    (10, W.STATE_TEXT[10], "Generating", "Turbine connected and producing"),
    (11, W.STATE_TEXT[11], "Generating", "Active power setpoint below rated: network operator limit via the park "
                                         "controller, or a noise mode"),
    (20, W.STATE_TEXT[20], "Available, not generating", "Rotor idling; turbine restarts automatically"),
    (21, W.STATE_TEXT[21], "Available, not generating", "Stops above 25 m/s; restarts below 20 m/s"),
    (22, W.STATE_TEXT[22], "Not available", "Ice detection system tripped the turbine; restart after the ice clears"),
    (30, W.STATE_TEXT[30], "Not available", "Service switch in the nacelle or tower base set by a technician"),
    (40, W.STATE_TEXT[40], "Not available", "Automatic stop on an alarm; remote reset possible for most alarms"),
    (41, W.STATE_TEXT[41], "Not available", "Fault awaiting or under repair; set after two hours in fault"),
    (50, W.STATE_TEXT[50], "Not available", "Stopped by the operator from the SCADA"),
    (60, W.STATE_TEXT[60], "Not available", "Stop signal from the network operator's ANM via the park controller"),
    (61, W.STATE_TEXT[61], "Not available", "Grid voltage or frequency outside limits, or grid absent"),
]


def write_states(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "State codes"
    _sheet(ws, ["code", "description", "operating category", "remarks"], (8, 46, 26, 86))
    for r in STATE_ROWS:
        ws.append(list(r))
    for row in ws.iter_rows(min_row=2):
        row[3].alignment = Alignment(wrap_text=True, vertical="top")
    ws2 = wb.create_sheet("Notes")
    ws2.append(["Hallvard H93-2.3 controller, software 7.4: the state written with each ten-minute record is the "
                "controller state at the end of the interval."])
    ws2.append(["Operating categories follow the turbine supply agreement's availability schedule."])
    ws2.column_dimensions["A"].width = 120
    wb.save(path)


def lift_rows():
    p9, p6 = W.PAD["CH09"], W.PAD["CH06"]
    sup = W.PEOPLE["lifts"][0]
    return [
        ("BC-26-0311", dt.date(2026, 4, 20), "07:40", p9, "LTM 1500-8.1, 500 t", "Rotor assembly lowered to laydown: hub "
         "%s with blades %s" % (HUB["CH09"], ", ".join(BLADES["CH09"])), HUB["CH09"], 58.6, sup),
        ("BC-26-0312", dt.date(2026, 4, 21), "09:15", p9, "LTM 1500-8.1, 500 t", "Main bearing housing removed from "
         "nacelle to laydown", "MBH-3381", 21.4, sup),
        ("BC-26-0313", dt.date(2026, 4, 22), "13:05", p9, "LTM 1500-8.1, 500 t", "Main bearing housing (exchange unit) "
         "lifted and fitted", "MBH-4027", 21.6, sup),
        ("BC-26-0314", dt.date(2026, 4, 24), "08:35", p9, "LTM 1500-8.1, 500 t", "Rotor assembly lifted from laydown and "
         "fitted: hub %s with blades %s" % (POOL_HUB, ", ".join(POOL_BLADES)), POOL_HUB, 58.9, sup),
        ("BC-26-0315", dt.date(2026, 4, 24), "15:10", p9, "LTM 1500-8.1, 500 t", "Rotor assembly %s loaded to "
         "transport" % HUB["CH09"], HUB["CH09"], 58.6, sup),
        ("BC-26-0702", dt.date(2026, 7, 13), "07:55", p6, "LTM 1350-6.1, 350 t", "Gearbox removed from nacelle to "
         "laydown", "GB-H23-7719", 18.9, sup),
        ("BC-26-0703", dt.date(2026, 7, 15), "10:20", p6, "LTM 1350-6.1, 350 t", "Gearbox (exchange unit) lifted and "
         "fitted", "GB-H23-8102", 19.1, sup),
    ]


def write_lifts(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Lifts 2026"
    _sheet(ws, ["lift_no", "date", "start_local", "pad", "crane", "load", "serial", "weight_t", "lift_supervisor"],
           (12, 11, 11, 6, 20, 92, 13, 9, 15))
    for r in lift_rows():
        ws.append(list(r))
    for row in ws.iter_rows(min_row=2):
        row[1].number_format = "dd/mm/yyyy"
        row[5].alignment = Alignment(wrap_text=True, vertical="top")
        row[7].number_format = "0.0"
    wb.save(path)


def write_layout(path):
    rows = []
    for t in sorted(W.TURBINES, key=lambda t: W.PAD[t]):
        x, y = W.XY[t]
        rows.append((W.PAD[t], t, x, y, W.ELEVATION[t], "%.0f" % W.HUB_M, "%.0f" % W.ROTOR_D, W.MODEL, W.NACELLE_SERIAL[t]))
    rows.append(("M1", "", W.MAST_XY[0], W.MAST_XY[1], W.MAST_ELEVATION, "80", "", "Met mast, 80 m lattice", ""))
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["pad", "turbine", "easting_m", "northing_m", "ground_level_m_aod", "hub_height_m",
                    "rotor_diameter_m", "description", "nacelle_serial"])
        w.writerows(rows)
    return len(rows)


def _serials():
    """Hub and blade serials as the register holds them: each turbine's three blades from one production batch
    (close but not consecutive numbers), hubs from the hub line."""
    import wind as WD
    g = WD.rng("serials")
    blades, hubs = {}, {}
    base = 20380
    for t in W.TURBINES:
        base += int(g.integers(19, 47))
        b0 = base
        steps = sorted(int(x) for x in g.choice(np.arange(1, 9), 2, replace=False))
        blades[t] = ["93B-%05d" % (b0 + s) for s in [0] + steps]
        base = b0 + steps[-1]
        hubs[t] = "HB-93-%04d" % (588 + 4 * W.TURBINES.index(t) + int(g.integers(0, 3)))
    return blades, hubs


BLADES, HUB = _serials()
POOL_HUB, POOL_BLADES = "HB-93-0477", ["93B-19846", "93B-19851", "93B-19853"]


def write_register(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Turbines"
    _sheet(ws, ["turbine", "pad", "model", "nacelle_serial", "commissioned", "hub_serial", "blade_A", "blade_B",
                "blade_C", "blade_type"], (9, 6, 17, 14, 13, 13, 11, 11, 11, 18))
    for t in W.TURBINES:
        ws.append([t, W.PAD[t], W.MODEL, W.NACELLE_SERIAL[t], W.COMMISSIONED, HUB[t]] + BLADES[t] + ["HB45.2 (45.2 m)"])
    for row in ws.iter_rows(min_row=2):
        row[4].number_format = "dd/mm/yyyy"
    ws2 = wb.create_sheet("Register")
    ws2.append(["Asset register, Cairnhollow Community Wind Farm. Last reviewed 30 June 2025 by %s." % W.PEOPLE["asset_manager"][0]])
    ws2.append(["Blade serials as fitted at commissioning unless a later exchange is recorded here."])
    ws2.column_dimensions["A"].width = 100
    wb.save(path)


def read_schedule():
    """When each turbine's revenue counter is actually read.

    The asset manager does not read ten counters at local midnight. A technician walks the site on the
    monthly round, taking the pads in the construction order they are numbered in, and the round itself
    slips with the weather and the working week. So each month's reads are spread over the round, the
    turbines at the far pads are read later than those by the access road, and the twelve-month window the
    registers span is not the twelve months the board asks about. Returns, per turbine, the interval index
    of each of the thirteen reads; indices are interval boundaries, so a register is the cumulative energy
    at one of them exactly and the part-windows are recoverable from the ten-minute record.
    """
    months = []
    d = dt.date(2025, 10, 1)
    while d <= dt.date(2026, 10, 1):
        months.append(d)
        d = (d.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    # The round goes out on the month's first working day, which is where it falls in the calendar and not a
    # matter of chance, and runs for two days: the first six pads on day one, the rest on day two. So the
    # offset between a month's start and its read is two days after a weekend and none after a Tuesday, and
    # the window the registers span differs from the calendar month by whatever the calendar gives.
    order = sorted(W.TURBINES, key=lambda t: W.PAD[t])
    reads = {t: [] for t in W.TURBINES}
    for x in months:
        day0 = dt.datetime(x.year, x.month, 1, tzinfo=W.LONDON)
        while day0.weekday() >= 5:                        # Saturday or Sunday waits for the Monday
            day0 += dt.timedelta(days=1)
        begin = day0 + dt.timedelta(hours=8, minutes=20)
        for j, t in enumerate(order):
            day = 0 if j < 6 else 1
            at = begin + dt.timedelta(days=day, minutes=40 * (j if j < 6 else j - 6))
            k = W.interval_index(at.astimezone(W.UTC))
            reads[t].append((x, at, int(min(max(k, 0), W.N))))
    return months, reads


def counters(ops):
    """Each turbine's revenue counter as the monthly round reads it (kWh), with the read stamp it carries."""
    months, reads = read_schedule()
    out = {}
    start = {t: 4.0e7 + 3.1e6 * j + 1234.0 * (j * j) for j, t in enumerate(W.TURBINES)}
    for t in W.TURBINES:
        e = np.cumsum(np.maximum(ops["power"][t], 0.0)) / 6.0
        e = np.concatenate([[0.0], e])
        seq = reads[t]
        out[t] = [(seq[i][0], seq[i][1], seq[i + 1][1], start[t] + e[seq[i][2]], start[t] + e[seq[i + 1][2]])
                  for i in range(len(seq) - 1)]
    return out


def write_counters(path, cnt):
    """One row per turbine per month: the read that opened the month's window and the read that closed it."""
    rows = 0
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["month", "turbine", "read_from_local", "read_to_local", "meter_start_kwh", "meter_end_kwh",
                    "energy_kwh"])
        for i in range(len(cnt[W.TURBINES[0]])):
            for t in W.TURBINES:
                mth, ra, rb, a, b = cnt[t][i]
                a_, b_ = int(np.floor(a)), int(np.floor(b))
                w.writerow([mth.strftime("%Y-%m"), t, ra.strftime("%Y-%m-%d %H:%M"), rb.strftime("%Y-%m-%d %H:%M"),
                            a_, b_, b_ - a_])
                rows += 1
    return rows


def hhmm(x):
    return "%02d:%02d" % (x // 60, x % 60)


def when(t, day):
    """A work-order time: the local clock time, with its date when it falls on another day than the order's."""
    lt_ = t.astimezone(W.LONDON)
    return lt_.strftime("%H:%M") if lt_.date() == day else lt_.strftime("%Y-%m-%d %H:%M")


def work_order_rows(ops, m):
    import ops as OP
    rows = []
    svc = ops["services"]
    for t in W.TURBINES:
        s = svc[t]
        tech = ", ".join(W.TECHNICIANS[i] for i in s["techs"])
        d1, d2 = s["d1"], s["d2"]
        rows.append([d1, t, "Annual service", hhmm(s["arrive1"]), when(s["stop1"], d1), when(s["stop1"], d1),
                     when(s["iso1_end"], d1), when(s["back1"], d1), hhmm(s["leave1"]), tech,
                     "Annual service, day 1 of 2: hub, pitch system, yaw system, tower"])
        rows.append([d2, t, "Annual service", hhmm(s["arrive2"]), when(s["stop2"], d2), when(s["iso2_from"], d2),
                     when(s["iso2_to"], d2), when(s["iso2_to"], d2), hhmm(s["leave2"]), tech,
                     "Annual service, day 2 of 2: drive train, converter, HV switchgear and transformer"])
    for t, (a, b) in sorted(OP.POWER_LOSS.items()):
        d = b.astimezone(W.LONDON).date()
        rows.append([d, t, "Corrective", when(b - dt.timedelta(minutes=40), d), when(a, d), "", "",
                     when(b + dt.timedelta(minutes=50), d), when(b + dt.timedelta(minutes=80), d),
                     W.TECHNICIANS[len(t) % 5], "Converter main breaker tripped, auxiliary supply lost; breaker reset "
                     "and converter checks"])
    for t, (f0, c0, c1, back) in sorted(OP.MAJOR.items()):
        d = f0.astimezone(W.LONDON).date()
        what = "Main bearing exchange with a Hallvard pool rotor" if t == "CH09" else "Gearbox exchange"
        rows.append([d, t, "Major component", "", when(f0, d), when(c0, d), when(c1, d), when(back, d), "",
                     "Hallvard Service UK major component team", what])
    import wind as WD
    gw = WD.rng("work order text")
    found = ["Pitch axis 2 battery voltage low; battery pack replaced", "Yaw brake pressure low; accumulator recharged",
             "Converter cooling fan failed; fan replaced", "Pitch axis 1 encoder fault; encoder replaced",
             "Gearbox oil filter differential pressure high; filter element changed",
             "Hydraulic pressure low; leaking fitting on pitch cylinder 3 remade",
             "Generator slip ring brush wear alarm; brushes replaced", "Main shaft speed sensor fault; sensor replaced",
             "Grid-side converter module fault; module replaced", "Tower base UPS fault; batteries replaced",
             "Yaw motor 2 overload; motor brake adjusted", "Nacelle cooling water pressure low; system topped up",
             "Pitch axis 3 motor overtemperature; fan and thermal switch replaced",
             "Hub controller communication fault; slip ring cleaned and connector remade"]
    for t in W.TURBINES:
        for k0, dur in ops["faults"][t]:
            if dur <= 18:
                continue
            a, b = W.start_of(k0), W.start_of(k0 + dur)
            d = b.astimezone(W.LONDON).date()
            rows.append([d, t, "Corrective", when(b - dt.timedelta(minutes=90), d), when(a, d), "", "", when(b, d),
                         when(b + dt.timedelta(minutes=25), d), W.TECHNICIANS[(k0 // 7) % 5],
                         found[int(gw.integers(0, len(found)))]])
    rows.sort(key=lambda r: (r[0], r[1]))
    for j, r in enumerate(rows):
        r.insert(0, "WO-%d" % (25840 + 3 * j + (j * j) % 3))
    return rows


def write_work_orders(path, rows):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["wo_number", "date", "turbine", "type", "arrived", "turbine_stopped", "isolated_from", "isolated_to",
                    "returned_to_service", "departed", "technicians", "summary"])
        for r in rows:
            w.writerow([r[0], r[1].isoformat()] + r[2:])
    return len(rows)


def meter_rows(ops):
    """The connection meter, half-hourly in UTC settlement periods, after the farm's transformer and cable losses.

    A connection meter has two registers and keeps them apart: it records what the farm sent out and what it
    drew in, and neither is the net. In the half-hours when the turbines are stopped the farm still draws
    its auxiliaries, the transformer is still energised and the site supplies still run, so the export
    register writes nothing at all and the import register carries the whole of it. Writing the net into an
    export column would make the import unrecoverable, so both registers ship.
    """
    tot = np.sum([ops["power"][t] for t in W.TURBINES], axis=0) / 6.0
    hh = tot.reshape(-1, 3).sum(1)
    # Site demand: the transformer's no-load loss plus the turbines' own auxiliaries, which run whether or
    # not the rotors do, plus the mast and the site supplies.
    # The transformer's no-load loss, the met mast, the switchroom and the site supplies run continuously;
    # each stopped turbine adds its own yaw, pitch, lighting and heating standby draw on top.
    stopped = np.sum([(ops["power"][t] <= 0.0).astype(float) for t in W.TURBINES], axis=0)
    aux_hh = (36.0 + 6.0 * stopped).reshape(-1, 3).sum(1) / 6.0
    loss = 0.0165 + 0.000004 * np.maximum(hh, 0.0)
    out = []
    for j, e in enumerate(hh):
        t = W.START + dt.timedelta(minutes=30 * j)
        net = e * (1 - loss[j]) - aux_hh[j]
        exp_, imp_ = (net, 0.0) if net >= 0 else (0.0, -net)
        out.append((t.strftime("%Y-%m-%d"), "%02d:%02d" % (t.hour, t.minute), "%.1f" % exp_, "%.1f" % imp_))
    return out


def write_meter(path, rows):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["settlement_date_utc", "period_start_utc", "export_kwh", "import_kwh"])
        w.writerows(rows)
    return len(rows)


def prior_year():
    """Last year's lost-production summary by turbine as the asset manager filed it for the 2025 board."""
    g = WD.rng("prior")
    out = []
    for t in W.TURBINES:
        down = float(np.round(g.gamma(3.0, 22.0) + 18.0, 1))
        curt = float(np.round(g.normal(205.0, 14.0), 1))
        out.append((t, down, curt))
    return out


def write_prior(path, rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Lost production 2024-25"
    _sheet(ws, ["turbine", "downtime_mwh", "grid_curtailment_mwh", "total_mwh"], (10, 15, 21, 12))
    for t, a, b in rows:
        ws.append([t, a, b, round(a + b, 1)])
    n = len(rows) + 1
    ws.append(["Farm", "=SUM(B2:B%d)" % n, "=SUM(C2:C%d)" % n, "=SUM(D2:D%d)" % n])
    for row in ws.iter_rows(min_row=2, min_col=2, max_col=4):
        for c in row:
            c.number_format = "#,##0.0"
    for c in ws[n + 1]:
        c.font = BOLD
    ws2 = wb.create_sheet("Notes")
    for line in ("Twelve months October 2024 to September 2025. Prepared for the board meeting of 13 November 2025.",
                 "Lost production by OM-07 revision 2: potential power from the warranted curve at the met mast's wind.",
                 "Figures in MWh to one decimal place."):
        ws2.append([line])
    ws2.column_dimensions["A"].width = 110
    wb.save(path)
