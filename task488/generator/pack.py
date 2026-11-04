"""Write each system's record of the three days: the pump station historian, the hydrant network register, the
maintenance record, both agents' ticket exports and check records, the batch certificates, the truck rack's loading
log, the equipment register, the agents' vehicle and equipment logs and the distractors. The documents are docs.py."""
import csv
import datetime as dt

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import model
import names as N
import sim
import world
from rng import Rng
from sim import DAY, H, M, T0, T1, T_RACK, T_SUSP

D = dt.timedelta
HEAD = Font(name="Calibri", bold=True)
GREY = PatternFill("solid", fgColor="D9DEE3")


# ------------------------------------------------------------------------------------------------ the world
def the_world():
    """The chosen world (names.SEED, names.RK), Monday's refuellers, ticket numbers and every sample's reading."""
    W = model.build(N.SEED, N.RK)
    ok, rep = model.screen(W)
    rok, rrep = model.screen_refuellers(W)
    assert ok and rok, (rep, rrep)
    W["screen"], W["screen_ref"] = rep, rrep
    mups, mloads, dips = world.monday_refuellers(W["rng"], W["fleet"], W["opening"])
    for i, u in enumerate(mups):
        u.uid = 7000 + i
    W["mon_rups"], W["mon_loads"], W["dips"] = mups, mloads, dips
    r = W["rng"].fork("pack")
    # ticket numbers in start order within each agent
    every = sorted([u for u in W["ups"]] + list(W["rups"]) + mups, key=lambda u: (u.start, u.equip or "", u.uid))
    nxt = {"Corbel": 418201, "Northgarth": 2690117}
    for u in every:
        u.ticket = ("CB%06d" if u.agent == "Corbel" else "NG%07d") % nxt[u.agent]
        nxt[u.agent] += 1 + (1 if r.chance(1, 9) else 0)        # numbers spoilt at the printer are skipped
    W["every"] = every
    # the operator initials on each ticket and check
    W["initials"] = {u.uid: r.choice(N.CORBEL_INITIALS if u.agent == "Corbel" else N.NG_INITIALS) for u in every}
    # one Corbel hydrant ticket voided for a mistyped registration and re-issued
    cand = [u for u in W["ups"] if u.agent == "Corbel" and 10 * H <= u.start < 11 * H + 30 * M
            and sim.PIT_SECTION[u.pit] == "A"]
    W["void"] = cand[r.below(len(cand))]
    reg = W["void"].reg
    k = len(reg) - 1
    W["void_reg"] = reg[:k] + ("Q" if reg[k] != "Q" else "O")
    W["void_ticket"] = W["void"].ticket + "A"
    W["readings"] = readings(W, Rng(N.SEED).fork("readings"))
    return W


def readings(W, r):
    """Each sample's recorded density at 15 C, observed density and temperature, and the Operator's conductivity."""
    out = {}
    G = W["gold"]["labels"]
    for s in W["samples"]:
        k = (s["time"], s["pit"])
        batch = N.LABEL_BATCH[G[k]]
        d15 = N.DENSITY[batch] + r.between(-2, 2) / 10.0
        if "up" in s:
            temp = s["up"].temp10 / 10.0 + r.between(-3, 3) / 10.0
        else:
            temp = world.fuel_temp(r, s["time"]) / 10.0
        dobs = d15 - 0.66 * (temp - 15.0)
        cond = N.CONDUCTIVITY[batch] + r.between(-6, 6)
        out[k] = {"batch": batch, "d15": round(d15, 1), "dobs": round(dobs, 1), "temp": round(temp, 1), "cond": cond}
    return out


# ------------------------------------------------------------------------------------------------ writers
def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(cols)
        w.writerows(rows)
    return len(rows)


def _sheet(ws, cols, rows, widths, fmt=None, start=1, freeze=True):
    for j, c in enumerate(cols, start=1):
        cell = ws.cell(row=start, column=j, value=c)
        cell.font = HEAD
        cell.fill = GREY
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    for i, row in enumerate(rows, start=start + 1):
        for j, v in enumerate(row, start=1):
            cell = ws.cell(row=i, column=j, value=None if v == "" else v)
            if fmt and fmt.get(j):
                cell.number_format = fmt[j]
    for j, w in enumerate(widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
    if freeze:
        ws.freeze_panes = "A%d" % (start + 1)
    return len(rows)


def hm(t):
    return N.local(t).strftime("%H:%M")


def ymd(t):
    return N.local(t).strftime("%Y-%m-%d")


# ------------------------------------------------------------------------------------------------ SCADA
def _minute_litres(draws):
    """Litres through the pump station meter in each local minute, from every draw on the hydrant."""
    out = {}
    for u in draws:
        t = u.start
        while t < u.end:
            v = u.cum(t + M) - u.cum(t)
            if v:
                out[t] = out.get(t, 0) + v
            t += M
    return out


def _background(r, day0, day1):
    """Minute litres for the days before the exports open: each stand's turns as steady draws, the same
    banks of traffic as the exported days, so the historian reads the same way throughout."""
    out = {}
    for d in range(day0, day1):
        base = d * DAY
        wk = (dt.date(2026, 10, 13) + D(days=d)).weekday()
        busy = 0 if wk in (1, 2) else (1 if wk in (4, 6) else 0)
        for sec, n_st, lo, hi, rate, turns in (("A", 9, 4600, 13600, 1100, 6), ("B", 8, 11200, 24400, 1350, 5),
                                               ("C", 6, 42000, 108000, 2800, 2), ("E", 4, 22000, 64000, 2600, 1),
                                               ("F", 5, 8000, 13000, 1100, 1)):
            for s in range(n_st):
                n = turns + busy + r.between(-1, 1) if turns > 1 else r.between(0, 1)
                if n <= 0:
                    continue
                gap = (17 * H) // n
                phase = r.between(0, gap // M) * M
                for k in range(n):
                    t = base + 5 * H + 35 * M + phase + k * gap + r.between(-20, 20) * M
                    g = world.odd_litres(r, r.between(lo, hi))
                    dur = sim.dur_for(g, rate)
                    for m in range(0, dur, M):
                        v = g * (m + M) // dur - g * m // dur
                        out[t + m] = out.get(t + m, 0) + v
    return out


def scada_rows(W):
    r = W["rng"].fork("scada")
    start_utc = dt.datetime(2026, 9, 14, 0, 0)
    end_utc = dt.datetime(2026, 10, 14, 14, 30)           # the pull at 07:30 local
    lit = _minute_litres(W["hyd"])
    first_day = int((start_utc - N.UTC_OFFSET - N.TUE).total_seconds() // DAY) - 1
    back = _background(r, first_day, -1)
    lineups = N.LINEUPS
    tot = 48213406                                            # the totaliser in litres when the export opens
    proving = int((N.PROVING - N.TUE).total_seconds())
    rows = []
    t_utc = start_utc
    while t_utc < end_utc:
        loc = t_utc - N.UTC_OFFSET
        t = int((loc - N.TUE).total_seconds())
        if t >= T_SUSP:
            flow = 0
        elif t >= -DAY:
            flow = lit.get(t, 0)
        else:
            flow = back.get(t, 0)
        read = flow + (flow * r.between(-25, 25) + 5000) // 10000 if flow else 0
        if t == proving:
            tot = 0
        tot += read
        tank = [k for when, k in lineups if when <= loc][-1]
        pumps = 0 if read == 0 else min(4, 1 + read // 2600)
        press = (1104 - read // 260 + r.between(-6, 6)) if t < T_SUSP else (1086 + r.between(-4, 4))
        valves = ["OPEN" if k == tank else "CLOSED" for k in (1, 2, 3, 4)]
        rows.append([t_utc.strftime("%Y-%m-%d %H:%M"), read, "%.3f" % (tot / 1000.0), press, pumps] + valves)
        t_utc += D(minutes=1)
    return rows


# ------------------------------------------------------------------------------------------------ the register
MATERIAL = {"FARM": "Carbon steel, epoxy lined", "MAIN": "Carbon steel, epoxy lined"}
LAID = {"FARM": 1998, "MAIN": 1998, "A": 1998, "B": 2004, "C": 2011, "E": 2015, "F": 2008, "G": 2001}


def write_register(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Segments"
    rows = []
    for seg, sec, a, b, length, idmm in sim.SEGMENTS:
        rows.append([seg, sec, a, b, length, idmm, MATERIAL.get(sec, "Carbon steel, epoxy lined"), LAID[sec]])
    _sheet(ws, ["Segment ID", "Section code", "From node", "To node", "Length (m)", "Internal diameter (mm)",
                "Pipe material", "Year laid"], rows, [10, 9, 10, 9, 11, 14, 26, 7])
    ws2 = wb.create_sheet("Draw points")
    rows = []
    for pt, node, stand, sec in sim.PITS:
        if stand:
            rows.append([pt, "Hydrant pit", node, stand, sec, "4 in. API pit valve", "2026-%02d" % (7 + (len(rows) % 3))])
        else:
            rows.append([pt, "Low point drain", node, "", sec, "1 in. drain valve", ""])
    _sheet(ws2, ["Point ID", "Point type", "Node ID", "Stand no", "Section code", "Valve type", "Last inspected"], rows,
           [9, 15, 7, 7, 8, 20, 13])
    ws3 = wb.create_sheet("Sections")
    rows = []
    for sec in sim.SECTIONS:
        segs = [s[0] for s in sim.SEGMENTS if s[1] == sec]
        rows.append([sec, sim.SECTION_NAMES[sec], "SV-%s" % sec, "%s to %s" % (segs[0], segs[-1]), sim.section_fill(sec)])
    rows.append(["", "Hydrant network", "", "", sim.TOTAL_FILL])
    _sheet(ws3, ["Section code", "Section name", "Section valve", "Segment range", "Line fill (L)"], rows,
           [8, 22, 13, 16, 13],
           fmt={5: "#,##0"})
    ws4 = wb.create_sheet("Rack")
    _sheet(ws4, ["Line ID", "From point", "To point", "Length (m)", "Internal diameter (mm)", "Line fill (L)"],
           [["RK-01", "Farm valve manifold", "Loading arms 1 and 2", 86, 250, world.RACK_HEADER]],
           [8, 20, 21, 11, 14, 13], fmt={6: "#,##0"})
    wb.save(path)


# ------------------------------------------------------------------------------------------------ maintenance
def write_maintenance(path, W):
    r = W["rng"].fork("maint")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Low point drains"
    rows = []
    for wk, day in ((3, dt.date(2026, 9, 21)), (2, dt.date(2026, 9, 28)), (1, dt.date(2026, 10, 5))):
        t = dt.datetime.combine(day, dt.time(9, 0)) + D(minutes=r.between(0, 25))
        for sec in sim.BRANCHES:
            d15 = N.DENSITY["J-26-1102"] + r.between(-2, 2) / 10.0
            rows.append([day.isoformat(), t.strftime("%H:%M"), sim.LPD[sec], sec, r.between(33, 48), "C&B", "Nil",
                         round(d15, 1), N.CONDUCTIVITY["J-26-1102"] + r.between(-5, 5), r.choice(["P.S.", "J.O."])])
            t += D(minutes=r.between(17, 31))
    for c in W["checks"]:
        if c["kind"] != "lpd":
            continue
        k = (c["time"], c["pit"])
        rd = W["readings"][k]
        d = c["drain"]
        rows.append([ymd(d.start), hm(d.start), d.pit, c["section"], d.gross, "C&B", "Nil", rd["d15"], rd["cond"], "P.S."])
    _sheet(ws, ["Round date", "Drain time", "Drain point", "Section code", "Drained (L)", "Visual check", "Water test",
                "Density at 15 C (kg/m3)", "Conductivity (pS/m)", "Tech"], rows, [11, 7, 11, 8, 11, 11, 7, 13, 13, 6], fmt={8: "0.0"})
    ws2 = wb.create_sheet("Filter vessels")
    rows = []
    for d in range(-8, 2):
        day = dt.date(2026, 10, 13) + D(days=d)
        for fv in ("FV-1", "FV-2", "FV-3", "FV-4"):
            if day == dt.date(2026, 10, 14) and fv in ("FV-3", "FV-4"):
                continue
            rows.append([day.isoformat(), "06:%02d" % r.between(10, 40), fv, 31 + r.between(0, 19) + (4 if fv == "FV-2" else 0),
                         r.between(1900, 5400), r.choice(["R.M.", "K.T.", "J.O."])])
    _sheet(ws2, ["Reading date", "Reading time", "Vessel ID", "Differential pressure (kPa)", "Flow at reading (L/min)",
                 "Tech"], rows,
           [11, 7, 8, 14, 14, 6])
    ws3 = wb.create_sheet("Pit valve tests")
    rows = []
    pits = [p[0] for p in sim.PITS if p[2]]
    for i in range(14):
        pit = pits[(i * 5 + 3) % len(pits)]
        day = dt.date(2026, 10, 12) + D(days=i // 9)
        rows.append([day.isoformat(), "%02d:%02d" % (13 + i % 4, r.between(0, 59)), pit,
                     r.choice(["Lanyard release", "Deadman response", "Pressure control"]),
                     "Pass" if i != 6 else "Pass after adjustment", r.choice(["P.S.", "J.O."])])
    _sheet(ws3, ["Test date", "Test time", "Pit ID", "Test type", "Test result", "Tech"], rows, [11, 7, 8, 18, 20, 6])
    wb.save(path)


# ------------------------------------------------------------------------------------------------ tickets
def _stand_code(u):
    return "NA-" + u.stand if u.kind == "refueller" else u.pit


def corbel_rows(W):
    rows = []
    void = W["void"]
    for u in W["every"]:
        if u.agent != "Corbel":
            continue
        ini = W["initials"][u.uid]
        if u.kind == "hydrant":
            gross, net = u.gross, u.net
        else:
            gross, net = "", u.gross
        acct = sim.ACCOUNT_OF[u.airline]
        base = [ymd(u.start), hm(u.start), hm(u.end), acct, u.airline, u.flight]
        tail = [_stand_code(u), u.equip, gross, "%.1f" % (u.temp10 / 10.0), net, ini]
        if u is void:
            rows.append((u.start, 0, [u.ticket, "VOID", ""] + base + [W["void_reg"]] + tail))
            rows.append((u.start, 1, [W["void_ticket"], "ISSUED", u.ticket] + base + [u.reg] + tail))
        else:
            rows.append((u.start, 0, [u.ticket, "ISSUED", ""] + base + [u.reg] + tail))
    rows.sort(key=lambda x: (x[0], x[1], x[2][0]))
    return [x[2] for x in rows]


CORBEL_COLS = ["ticket_no", "tkt_status", "reissue_of", "tkt_date", "start_local", "end_local", "acct_no",
               "customer_name", "flight_no", "acft_reg", "loc_code", "unit_no", "litres_gross", "fuel_degc", "litres_15c",
               "op_init"]


def ng_rows(W):
    rows = []
    for u in W["every"]:
        if u.agent != "Northgarth":
            continue
        rows.append([u.ticket, sim.ACCOUNT_OF[u.airline], u.airline, u.flight, u.reg, u.stand, u.equip,
                     N.utc(u.start), N.utc(u.end), u.net if u.kind == "hydrant" else u.gross,
                     round(u.temp10 / 10.0, 1), W["initials"][u.uid]])
    return rows


NG_COLS = ["Ticket No", "Acct", "Operator Name", "Flt", "Reg", "Stand No", "Unit ID", "Start (UTC)", "Stop (UTC)",
           "Vol @15C (L)", "Temp (C)", "By"]


def write_ng_tickets(path, W):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tickets"
    rows = ng_rows(W)
    _sheet(ws, NG_COLS, rows, [11, 8, 19, 6, 9, 7, 6, 17, 17, 12, 9, 5],
           fmt={8: "yyyy-mm-dd hh:mm", 9: "yyyy-mm-dd hh:mm", 10: "#,##0", 11: "0.0"})
    ws.auto_filter.ref = "A1:L%d" % (len(rows) + 1)
    wb.save(path)
    return len(rows)


# ------------------------------------------------------------------------------------------------ checks
def corbel_check_rows(W):
    r = W["rng"].fork("corbel-checks")
    rows = []
    for c in W["checks"]:
        if c["who"] != "Corbel":
            continue
        rd = W["readings"][(c["time"], c["pit"])]
        kind = "IDLE PIT FLUSH" if c["kind"] == "idle" else "SHIFT START"
        rows.append((c["time"], [ymd(c["time"]), hm(c["time"]), c["disp"], c["pit"], kind,
                                 c["litres"] if c["kind"] == "idle" else "", "C&B", "PASS", "%.1f" % rd["temp"],
                                 "%.1f" % rd["dobs"], "%.1f" % rd["d15"], W["initials"][c["up"].uid]]))
    for veh in ("RF-21", "RF-22", "RF-23", "RF-24"):
        for ss in (-DAY + 5 * H, -DAY + 17 * H, 5 * H, 17 * H, DAY + 4 * H):
            if veh == "RF-23" and ss >= world.RF23_OFF:
                continue
            t = ss + r.between(8, 35) * M
            rows.append((t, [ymd(t), hm(t), veh, "North apron", "SUMP", "", "C&B", "PASS", "", "", "",
                             r.choice(N.CORBEL_INITIALS)]))
    rows.sort(key=lambda x: (x[0], x[1][2]))
    return [x[1] for x in rows]


CORBEL_CHECK_COLS = ["chk_date", "chk_time", "unit_no", "loc_code", "chk_type", "flush_l", "visual", "water_det",
                     "fuel_degc", "density_obs", "density_15c", "op_init"]


def write_ng_checks(path, W):
    r = W["rng"].fork("ng-checks")
    rows = []
    for c in W["checks"]:
        if c["who"] != "Northgarth":
            continue
        rd = W["readings"][(c["time"], c["pit"])]
        kind = "Idle pit flush" if c["kind"] == "idle" else "Shift start"
        rows.append((c["time"], [N.utc(c["time"]), c["disp"], sim.PIT_STAND[c["pit"]], kind,
                                 c["litres"] if c["kind"] == "idle" else "", "Clear & bright", "Pass", rd["temp"],
                                 rd["dobs"], rd["d15"], W["initials"][c["up"].uid]]))
    for veh in ("N-7", "N-8", "N-12"):
        for ss in (-DAY + 5 * H, -DAY + 17 * H, 5 * H, 17 * H, DAY + 4 * H):
            t = ss + r.between(8, 35) * M
            rows.append((t, [N.utc(t), veh, "N apron", "Sump", "", "Clear & bright", "Pass", "", "", "",
                             r.choice(N.NG_INITIALS)]))
    rows.sort(key=lambda x: (x[0], x[1][1]))
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "QC"
    _sheet(ws, ["Date/Time (UTC)", "Unit ID", "Stand No", "Check type", "Flushed (L)", "Visual", "Water det.", "Temp C",
                "Dens obs", "Dens 15C", "By"], [x[1] for x in rows], [17, 6, 7, 14, 10, 14, 10, 8, 9, 9, 5],
           fmt={1: "yyyy-mm-dd hh:mm", 8: "0.0", 9: "0.0", 10: "0.0"})
    wb.save(path)
    return len(rows)


# ------------------------------------------------------------------------------------------------ certificates
def cert_rows():
    rows = []
    for b, tank, rec, cert, rel, d15, cond, flash, frz, status in N.BATCHES:
        rows.append([b, "Jet A-1", "Tank %d" % tank, rec, cert, rel, "%.1f" % d15, cond if cond else "",
                     "%.1f" % flash if flash else "", "%.1f" % frz if frz else "", "<5" if cert else "", status])
    return rows


CERT_COLS = ["batch_no", "grade", "tank_no", "received_on", "certified_on", "released_local", "density_15c_kg_m3",
             "conductivity_ps_m", "flash_point_c", "freezing_point_c", "fame_mg_kg", "batch_status"]


# ------------------------------------------------------------------------------------------------ the rack
def rack_rows(W):
    r = W["rng"].fork("rack")
    rows = []
    cards = {}
    bol = 26311
    loads = sorted(list(W["mon_loads"]) + list(W["loads"]), key=lambda ld: ld["start"])
    for i, ld in enumerate(loads):
        tank = ld["tank"]
        agent, cap, plate = world.TANKS[tank]
        shift = (ld["start"] - 5 * H) // (12 * H)
        key = (ld["veh"], shift)
        if key not in cards:
            cards[key] = ("CB-D0%02d" if agent == "Corbel" else "NG-D1%02d") % r.between(11, 79)
        preset = -(-(ld["net"] + 30) // 500) * 500
        temp = world.fuel_temp(r, ld["start"]) / 10.0 + r.between(4, 16) / 10.0
        rows.append([str(bol), ymd(ld["start"]), N.local(ld["start"]).strftime("%H:%M:%S"),
                     N.local(ld["start"] + ld["dur"]).strftime("%H:%M:%S"), 1 + (i % 2), agent.split()[0], tank, plate,
                     cards[key], preset, ld["net"], "%.1f" % temp])
        bol += 1 + (1 if r.chance(1, 7) else 0)
    return rows


RACK_COLS = ["bol_no", "load_date", "start_local", "end_local", "arm_no", "agent_code", "tank_unit", "plate_no",
             "driver_card", "preset_l", "loaded_l_15c", "product_degc"]


# ------------------------------------------------------------------------------------------------ equipment
def write_equipment(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Equipment"
    rows = []
    for k in range(1, 9):
        rows.append([N.CORBEL, "HD-0%d" % k, "Hydrant dispenser", "WFL 6%03d" % (11 + 7 * k), "", "", "HM-%04d" % (2140 + k),
                     "", "In service", "2026-0%d" % (6 + k % 3)])
    for veh, (agent, cap, plate) in world.TANKS.items():
        if agent != "Corbel":
            continue
        rows.append([N.CORBEL, veh, "Refueller, rigid", plate, cap, 1, "RM-%04d" % (3300 + int(veh[-2:])), "",
                     "In service", "2026-0%d" % (5 + int(veh[-1]) % 4)])
    for k in range(1, 6):
        rows.append([N.NORTHGARTH, "ND-%d" % k, "Hydrant dispenser", "NGA 31%02d" % (k * 3), "", "", "NM-%04d" % (870 + k),
                     "", "In service", "2026-0%d" % (5 + k % 4)])
    for trac, plate in world.TRACTORS.items():
        rows.append([N.NORTHGARTH, trac, "Refueller tractor (pump, filter, meter)", plate, "", "", "NM-%04d" % (890 + int(trac[-1])),
                     world.REGISTER_PAIRING[trac], "In service", "2026-07"])
    for veh in ("T-31", "T-32", "T-35"):
        agent, cap, plate = world.TANKS[veh]
        rows.append([N.NORTHGARTH, veh, "Refueller trailer (tank)", plate, cap, 1, "", "" if veh != "T-35" else "Spare",
                     "In service", "2026-0%d" % (4 + int(veh[-1]) % 5)])
    agent, cap, plate = world.TANKS["N-12"]
    rows.append([N.NORTHGARTH, "N-12", "Refueller, rigid", plate, cap, 1, "NM-0912", "", "In service", "2026-08"])
    _sheet(ws, ["Agent name", "Fleet no", "Equipment type", "Plate no", "Tank capacity (L)", "Compartments", "Meter ID",
                "Usual trailer", "Fleet status", "Last inspection"], rows, [28, 8, 34, 10, 12, 12, 9, 12, 11, 12], fmt={5: "#,##0"})
    wb.save(path)


# ------------------------------------------------------------------------------------------------ vehicle logs
def ng_vehicle_rows(W):
    r = W["rng"].fork("ng-vehicles")
    ev = []
    for when, trac, trl in world.COUPLINGS:
        if when < 0:
            ev.append((when, trac, "COUPLE", "Coupled to %s" % trl, ""))
    for tank in ("T-31", "T-32", "T-35", "N-12"):
        ev.append((world.MONDAY_DIP + r.between(2, 20) * M, tank, "WEEKLY DIP", "Weekly stock dip, contents L at 15 C",
                   W["dips"][tank]))
    for ss in (-DAY + 5 * H, 5 * H, DAY + 4 * H):
        for unit in ("N-7", "N-8", "N-12"):
            ev.append((ss + r.between(3, 25) * M, unit, "DAILY INSPECTION", "Pre-use inspection complete", ""))
    ev.append((-DAY + 13 * H + 22 * M, "N-8", "TYRE CHECK", "Trailer T-32 tyre pressures adjusted", ""))
    ev.append((-DAY + 20 * H + 40 * M, "N-12", "WASH", "Exterior wash", ""))
    ev.append((world.T31_OFF - 8 * M, "N-7", "DEFECT", "Driver reports T-31 axle 2 bearing running hot", ""))
    ev.append((world.T31_OFF, "N-7", "UNCOUPLE", "T-31 left at workshop bay 2 for bearing inspection", ""))
    for when, trac, trl in world.COUPLINGS:
        if when > 0:
            ev.append((when, trac, "COUPLE", "Coupled to %s" % trl, ""))
    ev.append((15 * H + 15 * M, "T-31", "WORKSHOP", "Axle 2 bearing replacement, part due Thu; trailer stood down", ""))
    ev.append((19 * H + 5 * M, "N-8", "DEFECT", "Hose reel rewind slow, logged for workshop", ""))
    ev.append((DAY + 5 * H + 31 * M, "N-7", "SUSPENDED", "Fuelling suspended by Operator duty supervisor", ""))
    ev.append((DAY + 5 * H + 31 * M, "N-8", "SUSPENDED", "Fuelling suspended by Operator duty supervisor", ""))
    ev.append((DAY + 5 * H + 32 * M, "N-12", "SUSPENDED", "Fuelling suspended by Operator duty supervisor", ""))
    ev.sort(key=lambda e: (e[0], e[1]))
    return [[N.utc(t).strftime("%Y-%m-%dT%H:%MZ"), unit, kind, detail, litres, r.choice(N.NG_INITIALS)]
            for t, unit, kind, detail, litres in ev]


NG_VEHICLE_COLS = ["time_utc", "unit_id", "event_code", "remarks", "qty_l", "user_id"]


def corbel_equipment_rows(W):
    r = W["rng"].fork("corbel-equipment")
    ev = []
    for tank in ("RF-21", "RF-22", "RF-23", "RF-24"):
        ev.append((world.MONDAY_DIP + r.between(2, 20) * M, tank, "WEEKLY DIP", "Weekly stock dip, contents L at 15 C",
                   W["dips"][tank]))
    for d in (-DAY, 0):
        for k in range(1, 9):
            ev.append((d + 5 * H + r.between(30, 200) * M, "HD-0%d" % k, "FILTER DP", "Filter monitor DP %d kPa" %
                       r.between(28, 61), ""))
    ev.append((-DAY + 14 * H + 10 * M, "RF-22", "HOSE INSPECTION", "Delivery hose monthly inspection, pass", ""))
    ev.append((-DAY + 16 * H + 45 * M, "HD-04", "DEFECT", "Deadman handle sticky, replaced from stores", ""))
    x = W["xfers"][0]
    ev.append((x["start"] - 12 * M, "RF-23", "DEFECT", "Hose reel bearing seized, reel will not rewind", ""))
    ev.append((x["start"], "RF-23", "TRANSFER", "Product pumped to RF-24 through RF-23 meter before workshop", x["litres"]))
    ev.append((world.RF23_OFF, "RF-23", "WORKSHOP", "In for hose reel bearing; tank not drained", ""))
    ev.append((10 * H + 5 * M, "RF-21", "METER CHECK", "Meter check against rack prover, within tolerance", ""))
    ev.append((16 * H + 20 * M, "HD-07", "HOSE INSPECTION", "Inlet hose monthly inspection, pass", ""))
    ev.append((DAY + 5 * H + 31 * M, "ALL", "SUSPENDED", "Fuelling suspended by Operator duty supervisor", ""))
    ev.sort(key=lambda e: (e[0], e[1]))
    return [[N.local(t).strftime("%Y-%m-%d %H:%M"), unit, kind, detail, litres, r.choice(N.CORBEL_INITIALS)]
            for t, unit, kind, detail, litres in ev]


CORBEL_EQUIPMENT_COLS = ["datetime_local", "unit_no", "event_code", "remarks", "qty_l", "user_id"]


# ------------------------------------------------------------------------------------------------ distractor
def write_pit_inspections(path, W):
    r = W["rng"].fork("pits-q3")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Q3 2026"
    rows = []
    for i, (pt, node, stand, sec) in enumerate(p for p in sim.PITS if p[2]):
        day = dt.date(2026, 7, 6) + D(days=(i * 37) % 84)
        rows.append([pt, stand, sec, day.isoformat(), "Pass", "Pass", "Pass" if i % 11 else "Weep at stem, repacked",
                     "%.1f" % (0.4 + r.between(0, 14) / 10.0), r.choice(["P.S.", "J.O.", "K.T."])])
    _sheet(ws, ["Pit ID", "Stand no", "Section code", "Inspection date", "Valve function", "Lanyard release",
                "Leak test", "Coupler wear (mm)", "Inspected by"], rows, [8, 7, 8, 11, 13, 14, 22, 15, 9])
    wb.save(path)


# ------------------------------------------------------------------------------------------------ September's stock
def september_stock(W, scada):
    """September's reconciliation by tank in cubic metres at 15 C: hydrant issues from the historian (14 to 30
    September) and the farm's own records before it, by the tank lined up; rack issues; receipts by batch; every
    line and total adds. The historian's litres are at fuel temperature, the reconciliation's at 15 C (about 0.2
    per cent more), so the two agree to the correction and not to the litre."""
    r = W["rng"].fork("stock")
    lineups = N.LINEUPS
    by_tank = {1: 0, 2: 0, 3: 0, 4: 0}
    sep1, oct1 = dt.datetime(2026, 9, 1), dt.datetime(2026, 10, 1)
    export0 = dt.datetime(2026, 9, 14) - N.UTC_OFFSET
    early = _background(W["rng"].fork("scada-early"), -43, -29)
    for t, v in early.items():
        loc = N.local(t)
        if sep1 <= loc < export0:
            tank = [k for w, k in lineups if w <= loc][-1]
            by_tank[tank] += v
    for row in scada:
        loc = dt.datetime.strptime(row[0], "%Y-%m-%d %H:%M") - N.UTC_OFFSET
        if loc < oct1:
            tank = [k for w, k in lineups if w <= loc][-1]
            by_tank[tank] += row[1]
    receipts = {k: 0.0 for k in by_tank}
    for b in N.BATCHES:
        if b[0] in N.RECEIPT_M3 and b[2].startswith("2026-09"):
            receipts[b[1]] += N.RECEIPT_M3[b[0]]
    rows = []
    for tank in (1, 2, 3, 4):
        hyd = round(by_tank[tank] * 1.0019 / 1000.0, 1)
        rack = round(hyd * r.between(150, 260) / 10000.0, 1)
        opening = round(max(300, hyd + rack - receipts[tank] + r.between(400, 1600)) + r.between(0, 999) / 10.0, 1)
        close_book = round(opening + receipts[tank] - hyd - rack, 1)
        assert close_book > 300, (tank, close_book)
        gl = round(-(hyd + rack) * r.between(1, 9) / 10000.0, 1)
        rows.append(("Tank %d" % tank, opening, round(receipts[tank], 1), hyd, rack, round(close_book + gl, 1)))
    return rows
