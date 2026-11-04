"""The answer from the shipped files alone, on a path of its own: nothing here imports the generator's world or
simulation. Exact rational arithmetic throughout.

    python3 task488/generator/solve.py [target_dir]

The hydrant: every draw (tickets, idle-pit flushes, the low point drains) moves fuel through the register's network,
each segment a first-in first-out pipe moved only by the draws downstream of it. The refuellers: each tank one mixed
body of fuel, filled at the rack through the rack line's own volume, emptied by the tickets of whatever vehicle was
coupled to it, and the one recorded transfer."""
import csv
import datetime as dt
import os
import re
import sys
from fractions import Fraction

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
UTC_OFF = dt.timedelta(hours=7)
SUSPENSION = dt.datetime(2026, 10, 14, 5, 30)
EXPORT_OPEN = dt.datetime(2026, 10, 12, 0, 0)
F = {
    "scada": "hydrant_scada_2026-09-14_2026-10-14.csv", "register": "hydrant_network_register.xlsx",
    "shiftlog": "farm_shift_log_2026-10-12_14.pdf", "maint": "hydrant_maintenance_2026-wk42.xlsx",
    "corbel_tickets": "corbel_fuel_tickets_2026-10-12_14.csv", "ng_tickets": "northgarth_tickets_20261012-20261014.xlsx",
    "corbel_checks": "corbel_daily_checks_2026-10.csv", "ng_checks": "northgarth_qc_checks_oct2026.xlsx",
    "rack": "rack_loading_log_2026-10-12_14.csv", "equipment": "into_plane_equipment_register.xlsx",
    "ng_vehicles": "northgarth_vehicle_log_2026-10.csv", "corbel_equipment": "corbel_equipment_log_2026-10.csv",
}


def rnd(v, unit):
    v = Fraction(v)
    return int((v / unit + Fraction(1, 2)) // 1) * unit


def sheet(path, name):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[name]
    rows = list(ws.iter_rows(values_only=True))
    head = rows[0]
    return [dict(zip(head, r)) for r in rows[1:] if any(v is not None for v in r)]


def rows_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def when(date, hhmm):
    return dt.datetime.strptime(date + " " + hhmm[:5], "%Y-%m-%d %H:%M")


# ------------------------------------------------------------------------------------------------ the register
class Net:
    def __init__(self, target):
        p = os.path.join(target, F["register"])
        self.segs = []
        for r in sheet(p, "Segments"):
            d = Fraction(r["Internal diameter (mm)"], 1000)
            vol = Fraction(355, 113) / 4 * d * d * r["Length (m)"] * 1000      # litres
            self.segs.append((r["Segment ID"], r["Section code"], r["From node"], r["To node"], rnd(vol, 1)))
        self.points = sheet(p, "Draw points")
        self.sections = [r["Section code"] for r in sheet(p, "Sections") if r["Section code"]]
        self.rack_fill = sheet(p, "Rack")[0]["Line fill (L)"]
        self.fill = {s[0]: s[4] for s in self.segs}
        self.section_of = {s[0]: s[1] for s in self.segs}
        self.frm = {s[0]: s[2] for s in self.segs}
        self.to = {s[0]: s[3] for s in self.segs}
        self.into = {s[3]: s[0] for s in self.segs}
        self.kids = {}
        for s in self.segs:
            self.kids.setdefault(s[2], []).append(s[0])
        self.node_of = {p["Point ID"]: p["Node ID"] for p in self.points}
        self.pit_of_stand = {str(p["Stand no"]): p["Point ID"] for p in self.points if p["Stand no"]}
        self.at_node = {}
        for p in self.points:
            self.at_node.setdefault(p["Node ID"], []).append(p["Point ID"])
        self.order = []
        root = [s[2] for s in self.segs if s[2] not in self.into][0]

        def walk(n):
            for s in self.kids.get(n, []):
                self.order.append(s)
                walk(self.to[s])
        walk(root)
        self.root = root
        self.below = {}
        for s in reversed(self.order):
            pts = list(self.at_node.get(self.to[s], []))
            for k in self.kids.get(self.to[s], []):
                pts += self.below[k]
            self.below[s] = pts


# ------------------------------------------------------------------------------------------------ the records
def correction_slope(target):
    """The volume correction per degree, read off Corbel's hydrant tickets (gross and 15 C litres at the printed fuel
    temperature): the least-squares slope through the origin of (15 C over gross, less one) on (15 less the
    temperature), in exact rationals."""
    sxy = sxx = Fraction(0)
    for r in rows_csv(os.path.join(target, F["corbel_tickets"])):
        if r["tkt_status"] == "VOID" or not r["loc_code"].startswith("P-"):
            continue
        x = 15 - Fraction(r["fuel_degc"])
        y = Fraction(int(r["litres_15c"]), int(r["litres_gross"])) - 1
        sxy += x * y
        sxx += x * x
    return sxy / sxx


def hydrant_draws(target, net, litres="15c", drains=True):
    """Every draw on the hydrant from the export's opening to the suspension: (key, point, start, end, litres).
    litres '15c' moves the 15 C litres both exports print; 'gross' moves Corbel's litres at fuel temperature and
    Northgarth's at 15 C; 'gross_all' also takes Northgarth's back to fuel temperature by Corbel's own correction."""
    out = []
    slope = correction_slope(target) if litres == "gross_all" else None
    for r in rows_csv(os.path.join(target, F["corbel_tickets"])):
        if r["tkt_status"] == "VOID" or not r["loc_code"].startswith("P-"):
            continue
        a, b = when(r["tkt_date"], r["start_local"]), when(r["tkt_date"], r["end_local"])
        if b <= a:
            b += dt.timedelta(days=1)
        v = int(r["litres_15c"]) if litres == "15c" else int(r["litres_gross"])
        out.append((r["ticket_no"], r["loc_code"], a, b, v))
    for r in sheet(os.path.join(target, F["ng_tickets"]), "Tickets"):
        if not str(r["Unit ID"]).startswith("ND-"):
            continue
        v = int(r["Vol @15C (L)"])
        if slope is not None:
            v = rnd(Fraction(v) / (1 + slope * (15 - Fraction(str(r["Temp (C)"])))), 1)
        out.append((r["Ticket No"], net.pit_of_stand[str(r["Stand No"])], r["Start (UTC)"] - UTC_OFF,
                    r["Stop (UTC)"] - UTC_OFF, v))
    if not drains:
        return out
    for r in rows_csv(os.path.join(target, F["corbel_checks"])):
        if r["chk_type"] == "IDLE PIT FLUSH":
            t = when(r["chk_date"], r["chk_time"])
            out.append(("flush " + r["loc_code"] + " " + r["chk_time"], r["loc_code"], t - dt.timedelta(minutes=5),
                        t - dt.timedelta(minutes=1), int(r["flush_l"])))
    for r in sheet(os.path.join(target, F["ng_checks"]), "QC"):
        if r["Check type"] == "Idle pit flush":
            t = r["Date/Time (UTC)"] - UTC_OFF
            pit = net.pit_of_stand[str(r["Stand No"])]
            out.append(("flush " + pit + " " + t.strftime("%H:%M"), pit, t - dt.timedelta(minutes=5),
                        t - dt.timedelta(minutes=1), int(r["Flushed (L)"])))
    for r in sheet(os.path.join(target, F["maint"]), "Low point drains"):
        t = when(r["Round date"], r["Drain time"])
        if EXPORT_OPEN <= t < SUSPENSION:
            out.append(("drain " + r["Drain point"], r["Drain point"], t, t + dt.timedelta(minutes=3), int(r["Drained (L)"])))
    return out


def hydrant_lineups(target):
    """When the hydrant suction moved to Tank 3 and off it, from the historian's valve states (local time)."""
    on = off = None
    prev = None
    with open(os.path.join(target, F["scada"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            t = dt.datetime.strptime(r["timestamp_utc"], "%Y-%m-%d %H:%M") - UTC_OFF
            v = r["tk3_hyd_valve"]
            if t >= dt.datetime(2026, 10, 13) and prev is not None and v != prev:
                if v == "OPEN" and on is None:
                    on = t
                elif v == "CLOSED" and on is not None and off is None:
                    off = t
            prev = v
    return on, off


def rack_lineups(target):
    """The rack pump's line-ups from the farm shift log: Tank 3 on with the hydrant at 06:00, off when the rack moved."""
    import pdfplumber
    with pdfplumber.open(os.path.join(target, F["shiftlog"])) as pdf:
        text = " ".join((pg.extract_text() or "") for pg in pdf.pages)
    text = re.sub(r"\s+", " ", text)
    on = re.search(r"(\d\d:\d\d) Tank 3 \(J-26-1187\) lined up to the hydrant pumps and the rack pump", text).group(1)
    off = re.search(r"(\d\d:\d\d) Rack pump moved to Tank 1", text).group(1)
    return when("2026-10-13", on), when("2026-10-13", off)


# ------------------------------------------------------------------------------------------------ the hydrant
def trace(net, draws, on, off, upto=SUSPENSION):
    """Batch litres each draw took and the batch litres standing in each section at `upto`."""
    pipes = {s: [["other", Fraction(net.fill[s])]] for s in net.order}
    cuts = {on, off, upto}
    for _, _, a, b, _ in draws:
        if a < upto:
            cuts.add(a)
            cuts.add(min(b, upto))
    times = sorted(t for t in cuts if t <= upto)
    took = {d[0]: Fraction(0) for d in draws}
    for a, b in zip(times, times[1:]):
        lab = "batch" if on <= a < off else "other"
        draw = {}
        users = {}
        for key, pt, s, e, v in draws:
            if s < b and e > a:
                q = Fraction(v) * Fraction(int((b - a).total_seconds()), int((e - s).total_seconds()))
                draw[pt] = draw.get(pt, 0) + q
                users.setdefault(pt, []).append((key, q))
        if not draw:
            continue
        inflow = {net.root: [[lab, sum(draw.values())]]}
        for s in net.order:
            q = sum(draw.get(p, 0) for p in net.below[s])
            if q == 0:
                continue
            src = inflow[net.frm[s]]
            tot = sum(v for _, v in src)
            pipe = pipes[s]
            for l, v in src:
                part = v * q / tot
                if pipe[-1][0] == l:
                    pipe[-1][1] += part
                else:
                    pipe.append([l, part])
            out, need = [], q
            while need > 0:
                l, v = pipe[0]
                if v <= need:
                    out.append([l, v])
                    need -= v
                    pipe.pop(0)
                else:
                    out.append([l, need])
                    pipe[0][1] = v - need
                    need = 0
            inflow[net.to[s]] = out
            here = [(k, x) for p in net.at_node.get(net.to[s], []) for k, x in users.get(p, [])]
            if here:
                batch_share = sum(v for l, v in out if l == "batch") / q
                for k, x in here:
                    took[k] += x * batch_share
    stand = {sec: Fraction(0) for sec in net.sections}
    seg_batch = {}
    for s, pipe in pipes.items():
        b = sum(v for l, v in pipe if l == "batch")
        stand[net.section_of[s]] += b
        if b > 0:
            seg_batch[s] = b
    return took, stand, seg_batch


def hydrant(target, litres="15c", drains=True, shift=(0, 0)):
    """litres: '15c' moves every ticket's litres at 15 C (the one basis both exports print); 'gross' moves Corbel's
    litres at fuel temperature where its export prints them. drains=False leaves the flushes and the low point drains
    out. shift moves the two line-up instants by so many seconds (the readings of the historian's minute)."""
    net = Net(target)
    draws = hydrant_draws(target, net, litres, drains)
    on, off = hydrant_lineups(target)
    on, off = on + dt.timedelta(seconds=shift[0]), off + dt.timedelta(seconds=shift[1])
    took, stand, seg_batch = trace(net, draws, on, off)
    tickets = {d[0] for d in draws if not d[0].startswith(("flush", "drain"))}
    return {"net": net, "draws": draws, "on": on, "off": off, "segments": seg_batch,
            "took": {k: v for k, v in took.items() if k in tickets and v > 0}, "standing": stand}


def tickets(target):
    """Every live ticket's record as the recall return wants it, keyed by ticket number."""
    net = Net(target)
    out = {}
    for r in rows_csv(os.path.join(target, F["corbel_tickets"])):
        if r["tkt_status"] == "VOID":
            continue
        a = when(r["tkt_date"], r["start_local"])
        out[r["ticket_no"]] = {"agent": "Corbel", "operator": r["customer_name"], "flight": r["flight_no"],
                               "reg": r["acft_reg"], "start_utc": a + UTC_OFF, "unit": r["unit_no"],
                               "location": r["loc_code"] if r["loc_code"].startswith("P-") else r["unit_no"],
                               "litres_15c": int(r["litres_15c"]), "hydrant": r["loc_code"].startswith("P-")}
    for r in sheet(os.path.join(target, F["ng_tickets"]), "Tickets"):
        hyd = str(r["Unit ID"]).startswith("ND-")
        out[r["Ticket No"]] = {"agent": "Northgarth", "operator": r["Operator Name"], "flight": str(r["Flt"]),
                               "reg": r["Reg"], "start_utc": r["Start (UTC)"], "unit": r["Unit ID"],
                               "location": net.pit_of_stand[str(r["Stand No"])] if hyd else r["Unit ID"],
                            "litres_15c": int(r["Vol @15C (L)"]), "hydrant": hyd}
    return out


def reckoning(target, hy=None):
    """The field's product change reckoning: when one line fill of the whole network (the register's total) has
    passed the pump station meter after each line-up change, from the historian's minute flows, and the hydrant
    uplifts that drew inside that window (the rung-0 answer)."""
    hy = hy or hydrant(target)
    total = sum(r["Line fill (L)"] for r in sheet(os.path.join(target, F["register"]), "Sections")
                if not r["Section code"])
    flows = []
    with open(os.path.join(target, F["scada"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            flows.append((dt.datetime.strptime(r["timestamp_utc"], "%Y-%m-%d %H:%M") - UTC_OFF,
                          int(r["pump_station_flow_lpm"])))
    edges = []
    for change in (hy["on"], hy["off"]):
        acc = 0
        for t, v in flows:
            if t >= change:
                if acc + v >= total:
                    secs = (Fraction(total - acc) / v * 60).__floor__()     # where in the minute the line fill passes
                    edges.append(t + dt.timedelta(seconds=int(secs)))
                    break
                acc += v
    a, b = edges
    took = []
    for key, pt, s_, e, v in hy["draws"]:
        if key.startswith(("flush", "drain")):
            continue
        if s_ < b and e > a:
            took.append(key)
    return {"line_fill": total, "edges": (a, b), "uplifts": len(took), "keys": took}


# ------------------------------------------------------------------------------------------------ the refuellers
def _take(queue, v):
    """v litres off the front of a first-in first-out tank: the runs taken, oldest first."""
    out, need = [], Fraction(v)
    while need > 0 and queue:
        lab, w = queue[0]
        take = min(w, need)
        out.append([lab, take])
        if take == w:
            queue.pop(0)
        else:
            queue[0][1] = w - take
        need -= take
    return out


def refuellers(target, pairing="log", transfer=True, header=True, tank_model="mixed"):
    """Each refueller tank's batch litres at the suspension and the batch litres each refueller uplift delivered.
    pairing='log' maps a tractor's tickets to the trailer the vehicle log coupled; 'register' to the equipment
    register's usual trailer. transfer=False leaves the recorded transfer out; header=False reads every load as the
    tank the rack was lined up to at its start. tank_model='mixed' takes each tank as one mixed body of fuel (QM-09
    2.3); 'fifo' draws every delivery from the oldest fuel in the tank, the reading QM-09 rules out."""
    eq = sheet(os.path.join(target, F["equipment"]), "Equipment")
    rigid = {r["Fleet no"] for r in eq if str(r["Equipment type"]).startswith("Refueller, rigid")}
    usual = {r["Fleet no"]: r["Usual trailer"] for r in eq if r["Usual trailer"] and r["Usual trailer"] != "Spare"}
    tanks, events = {}, []
    for r in rows_csv(os.path.join(target, F["corbel_equipment"])):
        t = dt.datetime.strptime(r["datetime_local"], "%Y-%m-%d %H:%M")
        if r["event_code"] == "WEEKLY DIP" and t.date() == dt.date(2026, 10, 12):
            tanks[r["unit_no"]] = [Fraction(0), Fraction(int(r["qty_l"]))]
        elif r["event_code"] == "TRANSFER" and transfer:
            dst = re.search(r"to (RF-\d\d)", r["remarks"]).group(1)
            events.append((t, 1, "xfer", (r["unit_no"], dst, int(r["qty_l"]))))
    couplings = []
    for r in rows_csv(os.path.join(target, F["ng_vehicles"])):
        t = dt.datetime.strptime(r["time_utc"], "%Y-%m-%dT%H:%MZ") - UTC_OFF
        if r["event_code"] == "WEEKLY DIP" and t.date() == dt.date(2026, 10, 12):
            tanks[r["unit_id"]] = [Fraction(0), Fraction(int(r["qty_l"]))]
        elif r["event_code"] == "COUPLE":
            couplings.append((t, r["unit_id"], re.search(r"(T-\d\d)", r["remarks"]).group(1)))
    couplings.sort()

    def tank_of(unit, t):
        if unit in rigid:
            return unit
        if pairing == "register":
            return usual[unit]
        cur = None
        for c_t, trac, trl in couplings:
            if trac == unit and c_t <= t:
                cur = trl
        return cur
    for r in rows_csv(os.path.join(target, F["rack"])):
        t = dt.datetime.strptime(r["load_date"] + " " + r["start_local"], "%Y-%m-%d %H:%M:%S")
        events.append((t, 0, "load", (r["tank_unit"], int(r["loaded_l_15c"]))))
    ups = []
    for r in rows_csv(os.path.join(target, F["corbel_tickets"])):
        if r["tkt_status"] != "VOID" and r["loc_code"].startswith("NA-"):
            t = when(r["tkt_date"], r["start_local"])
            ups.append((r["ticket_no"], "Corbel", r["customer_name"], r["unit_no"], t, int(r["litres_15c"])))
    for r in sheet(os.path.join(target, F["ng_tickets"]), "Tickets"):
        if not str(r["Unit ID"]).startswith("ND-"):
            ups.append((r["Ticket No"], "Northgarth", r["Operator Name"], r["Unit ID"], r["Start (UTC)"] - UTC_OFF,
                        int(r["Vol @15C (L)"])))
    for u in ups:
        if u[4] < SUSPENSION:
            events.append((u[4], 2, "up", u))
    events.sort(key=lambda e: (e[0], e[1]))
    on, off = rack_lineups(target)
    hdr = [["other", Fraction(net_rack_fill(target))]] if header else []
    fifo = {k: [["other", v[1]]] for k, v in tanks.items()}
    delivered = {}
    for t, _, kind, x in events:
        if kind == "load":
            tank, v = x
            lab = "batch" if on <= t < off else "other"
            if header:
                hdr.append([lab, Fraction(v)])
                parts = _take(hdr, v)
            else:
                parts = [[lab, Fraction(v)]]
            got = sum(w for l, w in parts if l == "batch")
            tk = tanks[tank]
            tk[0] += got
            tk[1] += v - got
            fifo[tank] += [list(p) for p in parts]
        elif kind == "xfer":
            src, dst, v = x
            s_, d_ = tanks[src], tanks[dst]
            if tank_model == "fifo":
                parts = _take(fifo[src], v)
                fifo[dst] += parts
                b = sum(w for l, w in parts if l == "batch")
            else:
                b = Fraction(v) * s_[0] / (s_[0] + s_[1])
            s_[0] -= b
            s_[1] -= v - b
            d_[0] += b
            d_[1] += v - b
        else:
            key, agent, airline, unit, ut, v = x
            tank = tank_of(unit, ut)
            tk = tanks[tank]
            if tank_model == "fifo":
                b = sum(w for l, w in _take(fifo[tank], v) if l == "batch")
            else:
                b = Fraction(v) * tk[0] / (tk[0] + tk[1])
            tk[0] -= b
            tk[1] -= v - b
            if b > 0:
                delivered[key] = (b, airline, agent, unit, ut, v, tank)
    return {"held": {k: v[0] for k, v in tanks.items()}, "totals": {k: v[0] + v[1] for k, v in tanks.items()},
            "delivered": delivered}


def net_rack_fill(target):
    return sheet(os.path.join(target, F["register"]), "Rack")[0]["Line fill (L)"]


def row_bands(target, hy=None):
    """For each hydrant row the batch's head or tail crossed during the uplift, the golden batch litres and the band
    that holds every reading of the records' conventions: litres at fuel temperature where printed or recovered by the
    exports' own correction, the flushes and drains left out, each line-up instant a minute and a half either side. The
    band is the widest departure plus 250 L, rounded up to a whole 100 L."""
    hy = hy or hydrant(target)
    tk = tickets(target)
    variants = [hydrant(target, litres="gross"), hydrant(target, litres="gross_all"), hydrant(target, drains=False)]
    for a in (-90, 90):
        for b in (-90, 90):
            variants.append(hydrant(target, shift=(a, b)))
    out = {}
    for key, gold in hy["took"].items():
        full = tk[key]["litres_15c"]
        if gold >= full - 5:
            continue
        dev = max(abs(v["took"].get(key, 0) - gold) for v in variants)
        out[key] = {"batch_10": rnd(gold, 10), "litres_15c": full,
                    "band": -(-(int(dev) + 251) // 100) * 100, "departure": dev}
    return out


# ------------------------------------------------------------------------------------------------ the answer
def answer(target):
    hy = hydrant(target)
    rf = refuellers(target)
    stand = {s: v for s, v in hy["standing"].items() if v > 0}
    held = {k: v for k, v in rf["held"].items() if v > 0}
    by_air = {}
    for key, (b, airline, *_rest) in rf["delivered"].items():
        by_air[airline] = by_air.get(airline, Fraction(0)) + b
    return {
        "sections": sorted(stand),
        "standing_100": {s: rnd(v, 100) for s, v in stand.items()},
        "hydrant_uplifts": len(hy["took"]),
        "refuellers": sorted(held),
        "held_10": {k: rnd(v, 10) for k, v in held.items()},
        "refueller_uplifts": len(rf["delivered"]),
        "by_air_10": {a: rnd(v, 10) for a, v in by_air.items()},
        "hy": hy, "rf": rf,
    }


def main(target):
    a = answer(target)
    print("hydrant sections holding J-26-1187 at 05:30:", ", ".join("%s %s L" % (s, "{:,}".format(a["standing_100"][s]))
                                                              for s in a["sections"]))
    print("hydrant uplifts that took batch fuel:", a["hydrant_uplifts"])
    print("refuellers holding it:", ", ".join("%s %s L" % (k, "{:,}".format(a["held_10"][k])) for k in a["refuellers"]))
    print("refueller uplifts that delivered it:", a["refueller_uplifts"])
    print("refuellers' batch litres by airline:", ", ".join("%s %s L" % (k, "{:,}".format(v))
                                                         for k, v in sorted(a["by_air_10"].items())))
    return a


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))

