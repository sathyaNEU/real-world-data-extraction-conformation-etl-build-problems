"""Cut the evidence pack: every file as the system that produces it would export it."""
import csv
import datetime as dt
import io
import json
import math
import os

import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

import postprocess as PP
import sim
import truth
import world as W

FILES = {
    "relay": "protection/feeder_relay_events_2025_2026.csv",
    "recloser": "protection/recloser_control_events_2025_2026.csv",
    "soe": "scada/soe_breakers_reclosers_2025_2026.csv",
    "oms": "oms/oms_outage_history_2025_2026.xlsx",
    "feeders": "assets/feeder_register.xlsx",
    "devices": "assets/protective_device_register.csv",
    "transformers": "assets/distribution_transformers.csv",
    "sps": "customers/service_points_2026-10-31.csv",
    "strokes": "weather/lightning_strokes_2025_2026.csv",
    "asos": "weather/airport_hourly_obs_2025_2026.csv",
    "subs": "gis/substations.geojson",
    "veg": "vegetation/line_clearance_work_2023_2026.csv",
    "blinks": "customers/blinking_lights_contacts_2025_2026.csv",
    "procedure": "procedures/DRP-04_distribution_reliability_procedure_rev6.pdf",
}
DISTRACTORS = ["veg", "blinks", "strokes"]
STATION = "KKFR"
EXPORT_STAMP = "2026-11-03T07:41:00Z"

LEGACY_CAUSE = {"lightning": "LTNG", "tree": "VEG", "wet_tree": "VEG", "storm_damage": "WTHR", "animal": "ANML",
                "ice": "WTHR",
                "equipment": "EQUIP", "vehicle": "PUB", "public": "PUB", "unknown": "UNK", "planned": "PLAN",
                "incipient": "UNK"}
NEW_CAUSE = {"LTNG": "LIGHTNING", "VEG": "VEGETATION", "WTHR": "WEATHER OTHER", "ANML": "ANIMAL",
             "EQUIP": "EQUIPMENT FAILURE", "PUB": "PUBLIC DAMAGE", "UNK": "UNKNOWN", "PLAN": "PLANNED"}


def path(target, key):
    p = os.path.join(target, FILES[key])
    os.makedirs(os.path.dirname(p), exist_ok=True)
    return p


def iso_utc(t, ms=True):
    u = sim.utc_dt(t)
    if ms:
        return u.strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (t % 1000)
    return u.strftime("%Y-%m-%dT%H:%M:%SZ")


def local_zone(t):
    return "CDT" if sim.offset_ms(t) == -5 * sim.MS_H else "CST"


def scada_time(t):
    l = sim.local_dt(t)
    return l.strftime("%Y-%m-%d %H:%M:%S.") + "%03d %s" % (t % 1000, local_zone(t))


def cst_time(t):
    return (sim.EPOCH + dt.timedelta(milliseconds=t - 6 * sim.MS_H)).strftime("%m/%d/%Y %H:%M:%S")


def legacy_time(t):
    return sim.local_dt(t).strftime("%m/%d/%Y %H:%M")


def write_csv(p, header, rows, crlf=False):
    with open(p, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return len(rows)


# --------------------------------------------------------------------------- names the systems carry
def breaker_id(net, fid, day):
    return W.breaker_name(net, fid, day)


def scada_point(net, dev, day):
    D = net["devices"][dev]
    fid = D["feeder"]
    spec = W.FEEDERS[W.FIX[fid]]
    if D["type"] == "BREAKER":
        if spec.get("legacy") and day < W.REBUILD:
            return "COTTER.%s.CB" % spec["legacy"][3:]
        return "%s.F%s.CB" % (D["feeder"][:3], fid[-1])
    return "%s.%s.REC" % (fid.replace("-", ""), dev.replace("-", ""))


SUB_DIGIT = {"BLV": "1", "CTR": "2", "MLR": "3", "NYD": "4", "SYC": "5"}


def present_ids(net):
    """The numbers the customer system and the asset register carry. Service points set up before 2025 are
    numbered by substation in meter-route order along each feeder; services connected from 2025 on take the
    connection series in the order they were connected. Transformers and tap fuses are numbered by substation along
    each feeder, new transformers after the old. Gaps are retired and cancelled numbers. The numbering draws on its
    own stream, so nothing the systems record moves with it."""
    if "_ids" in net:
        return net["_ids"]
    rng = np.random.default_rng(W.SEED + 91)
    fpos = {f["id"]: i for i, f in enumerate(W.FEEDERS)}
    new_t = set()
    by_t = {}
    for sp, v in net["sps"].items():
        by_t.setdefault(v["transformer"], []).append(v)
    for tid, vs in by_t.items():
        if all(v["connected"] >= W.DATA0 for v in vs):
            new_t.add(tid)
    tmap, fmap, smap = {}, {}, {}
    for sub, digit in sorted(SUB_DIGIT.items(), key=lambda x: x[1]):
        fus = sorted((L for L in net["laterals"].values() if L["feeder"][:3] == sub),
                     key=lambda L: (fpos[L["feeder"]], L["tap"], L["id"]))
        k = int(rng.integers(120, 900))
        for L in fus:
            fmap[L["id"]] = "F-%s%04d" % (digit, k)
            k += int(rng.integers(3, 41))
        assert k < 10000
        trs = [T for T in net["transformers"].values() if T["feeder"][:3] == sub]
        trs.sort(key=lambda T: (T["id"] in new_t, fpos[T["feeder"]], T["pos"], T["lpos"], T["id"]))
        k = int(rng.integers(1000, 4000))
        for T in trs:
            tmap[T["id"]] = "T%s%05d" % (digit, k)
            k += int(rng.integers(1, 12))
        assert k < 100000
    order_t = {tid: i for i, tid in enumerate(sorted(tmap, key=lambda t: tmap[t]))}
    old = [(sp, v) for sp, v in net["sps"].items() if v["connected"] < W.DATA0]
    for sub, digit in sorted(SUB_DIGIT.items(), key=lambda x: x[1]):
        mine = sorted(((sp, v) for sp, v in old if net["transformers"][v["transformer"]]["feeder"][:3] == sub),
                      key=lambda x: (order_t[x[1]["transformer"]], x[1]["connected"], x[0]))
        k = int(rng.integers(100000, 400000))
        for sp, v in mine:
            smap[sp] = "%s%07d" % (digit, k)
            k += int(rng.integers(1, 9))
        assert k < 10000000
    new = sorted(((sp, v) for sp, v in net["sps"].items() if v["connected"] >= W.DATA0),
                 key=lambda x: (x[1]["connected"], order_t[x[1]["transformer"]], x[0]))
    k = int(rng.integers(1000000, 2000000))
    for sp, v in new:
        smap[sp] = "8%07d" % k
        k += int(rng.integers(1, 4))
    assert len(set(smap.values())) == len(smap) == len(net["sps"])
    assert len(set(tmap.values())) == len(tmap) == len(net["transformers"])
    assert len(set(fmap.values())) == len(fmap) == len(net["laterals"])
    net["_ids"] = dict(sp=smap, t=tmap, fuse=fmap)
    return net["_ids"]


def shown(net, dev):
    """A device, transformer or service point under the number its system carries."""
    ids = present_ids(net)
    for k in ("sp", "t", "fuse"):
        if dev in ids[k]:
            return ids[k][dev]
    return dev


def shown_pole(net, T):
    """A tap transformer's pole carries its lateral's number."""
    if not T["lateral"]:
        return T["pole"]
    head, tail = T["pole"].split("-", 1)
    return "L%s-%s" % (shown(net, T["lateral"])[2:], tail)


def terminal_of(net, dev, phases):
    order = net["devices"][dev]["terminals"]
    ts_ = sorted(order.index(p) + 1 for p in phases)
    if len(ts_) == 1:
        return "%d-G" % ts_[0]
    return "-".join(str(x) for x in ts_)


# --------------------------------------------------------------------------- protection records
def write_relay(target, net, S, rng):
    rows = []
    evno = {}
    busy = {}
    for op in S["ops"]:
        if net["devices"][op["device"]]["type"] != "BREAKER":
            continue
        busy.setdefault((op["device"], op["day"]), 0)
        busy[(op["device"], op["day"])] += len(op["trips"])
    dropped = 0
    for op in sorted(S["ops"], key=lambda o: o["t"]):
        dev = op["device"]
        if net["devices"][dev]["type"] != "BREAKER":
            continue
        fid = op["feeder"]
        relay = breaker_id(net, fid, op["day"])
        heavy = busy[(dev, op["day"])] >= 4 and not (W.WIN0 <= op["day"] <= W.WIN1) and op["cause"] != "incipient"
        for (tt, shot), rec in zip(op["trips"], op["rec"]):
            if relay not in evno:
                evno[relay] = int(rng.integers(1200, 9800))
            evno[relay] += int(rng.choice([1, 1, 1, 2, 2, 3]))
            if heavy and rng.random() < 0.45:
                dropped += 1
                continue
            ph = op["phases"]
            etype = (ph + "G" if len(ph) == 1 else ph) + " T"
            elem = ("50G1" if len(ph) == 1 else "50P1") if shot == 0 else ("51G" if len(ph) == 1 else "51P")
            rows.append([evno[relay], relay, iso_utc(tt), etype, shot, int(round(rec["A"])), int(round(rec["B"])),
                         int(round(rec["C"])), int(round(rec["G"])), elem,
                         "%.2f" % (60 + float(rng.normal(0, 0.012)))])
    rows.sort(key=lambda r: (r[2], r[1]))
    write_csv(path(target, "relay"), ["event_no", "relay", "utc_time", "event_type", "shot", "ia_a", "ib_a",
                                      "ic_a", "ig_a", "trip_element", "freq_hz"], rows)
    return len(rows), dropped


def _restore_close(S, op):
    """When a device that locked out was closed back in: the desk's test close, the first step of a stepped
    restoration, or the crew's restoration."""
    if op.get("test_close"):
        return op["test_close"], "REMOTE"
    o = op.get("outage_ref")
    if o is None:
        return None, None
    t = o["steps"][0][0] if o["steps"] else o["restore"]
    return t + 17000, "LOCAL"


def write_recloser(target, net, S, rng):
    rows = []
    for op in sorted(S["ops"], key=lambda o: o["t"]):
        dev = op["device"]
        if net["devices"][dev]["type"] != "RECLOSER":
            continue
        term = terminal_of(net, dev, op["phases"])
        for k, ((tt, shot), rec) in enumerate(zip(op["trips"], op["rec"])):
            ka = max(rec[p] for p in op["phases"]) / 1000.0
            rows.append([dev, cst_time(tt), "TRIP", shot + 1, term, "%.3f" % ka, ""])
            if k < len(op["closes"]):
                rows.append([dev, cst_time(op["closes"][k]), "RECLOSE", shot + 1, "", "", "AUTO"])
        if op["lockout"]:
            rows.append([dev, cst_time(op["lockout"]), "LOCKOUT", len(op["trips"]), "", "", ""])
            t, src = _restore_close(S, op)
            if t is not None:
                rows.append([dev, cst_time(t), "CLOSE", 0, "", "", src])
    rows.sort(key=lambda r: (dt.datetime.strptime(r[1], "%m/%d/%Y %H:%M:%S"), r[0]))
    write_csv(path(target, "recloser"), ["control", "time_cst", "event", "op_count", "fault_terminals",
                                         "fault_ka", "close_source"], rows)
    return len(rows)


def write_soe(target, net, S, rng):
    rows = []
    for op in S["ops"]:
        dev = op["device"]
        D = net["devices"][dev]
        if not (D["type"] == "BREAKER" or D.get("scada")):
            continue
        for (tt, shot) in op["trips"]:
            pt = scada_point(net, dev, sim.local_day(tt))
            rows.append((tt + sim.soe_open_lag(tt), pt, "OPEN"))
        for c in op["closes"]:
            rows.append((c + sim.soe_close_lag(c), scada_point(net, dev, sim.local_day(c)), "CLOSED"))
        if op["lockout"]:
            t, _ = _restore_close(S, op)
            if t is not None:
                if op.get("test_close"):
                    t = op["test_close"]
                rows.append((t, scada_point(net, dev, sim.local_day(t)), "CLOSED"))
    rows.sort()
    out = [[scada_time(t), p, s, "GOOD"] for t, p, s in rows]
    write_csv(path(target, "soe"), ["time", "point", "state", "quality"], out, crlf=True)
    return len(out)


# --------------------------------------------------------------------------- outage management system
def ticket_rows(net, S, TR, rng):
    """The OMS's own tickets: one per sustained interruption still on after fifteen minutes."""
    legacy, inc, steps = [], [], []
    seq25, seq26 = int(rng.integers(1400, 2600)), int(rng.integers(1100, 2300))
    inc_no = int(rng.integers(150, 420))
    rng_main, rng_later = rng, np.random.default_rng(W.SEED + 61)
    for o in sorted(TR["outages"], key=lambda o: o["start"]):
        if o.get("no_ticket"):
            continue
        rng = rng_later if o.get("later_found") else rng_main
        d = sim.local_day(o["start"])
        dev = o["device"]
        fid = o["feeder"]
        if dev in net["sps"]:
            dtype, did = "SERVICE", shown(net, dev)
        elif dev in net["transformers"]:
            dtype, did = "TRANSFORMER", shown(net, dev)
        else:
            dtype = net["devices"][dev]["type"]
            did = breaker_id(net, fid, d) if dtype == "BREAKER" else shown(net, dev)
        cause = LEGACY_CAUSE.get(o["cause"], "UNK")
        if o["cause"] in ("tree", "lightning", "animal", "wet_tree") and rng.random() < 0.13:
            cause = "UNK"
        n = o["n_all"]
        crew = "C%d" % int(rng.choice([11, 12, 14, 15, 21, 22, 23, 31]))
        if d < W.OMS_CUTOVER:
            if d.year == 2025:
                seq25 += int(rng.choice([1, 1, 2, 3]))
                tno = "T25-%06d" % seq25
            else:
                seq26 += int(rng.choice([1, 1, 2, 3]))
                tno = "T26-%06d" % seq26
            circuit = W.legacy_name(fid, d)
            legacy.append([tno, "", circuit, did, dtype, legacy_time(o["start"]), legacy_time(o["restore"]), n,
                           cause, crew])
            for k, (t, cnt) in enumerate(o["step_counts"][:-1]):
                logged = t - int(rng.integers(3, 13)) * sim.MS_MIN
                legacy.append(["%s-%d" % (tno, k + 1), tno, circuit, did, dtype, legacy_time(logged), legacy_time(t),
                               cnt, cause, crew])
        else:
            inc_no += int(rng.choice([1, 1, 1, 2]))
            iid = "INC-2026-%05d" % inc_no
            inc.append([iid, fid, did, dtype, iso_utc(o["start"], ms=False), iso_utc(o["restore"], ms=False), n,
                        NEW_CAUSE[cause]])
            if o["steps"]:
                for k, (t, cnt) in enumerate(o["step_counts"]):
                    steps.append([iid, k + 1, iso_utc(t, ms=False), cnt])
    return legacy, inc, steps


def write_oms(target, net, S, TR, rng):
    legacy, inc, steps = ticket_rows(net, S, TR, rng)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Legacy tickets"
    hdr = ["Ticket", "Parent Ticket", "Circuit", "Device", "Device Type", "Out", "Energized", "Customers", "Cause",
           "Crew"]
    _sheet(ws, hdr, legacy, widths=[14, 14, 9, 13, 13, 17, 17, 10, 7, 6])
    ws2 = wb.create_sheet("Incidents")
    _sheet(ws2, ["Incident", "Feeder", "Device", "Device Class", "Start (UTC)", "End (UTC)", "Customers Out", "Cause"],
           inc, widths=[16, 8, 13, 13, 21, 21, 13, 19])
    ws3 = wb.create_sheet("Restoration Steps")
    _sheet(ws3, ["Incident", "Step", "Step Time (UTC)", "Customers Restored"], steps, widths=[16, 6, 21, 18])
    p = path(target, "oms")
    wb.save(p)
    PP.normalize_ooxml(p, "omsreport", "omsreport", "2026-11-03T07:38:12Z", "2026-11-03T07:38:12Z", excel=True)
    return len(legacy), len(inc), len(steps)


def _sheet(ws, header, rows, widths=None, bold=True):
    ws.append(header)
    for r in rows:
        ws.append([None if x == "" else x for x in r])
    if bold:
        for c in ws[1]:
            c.font = Font(bold=True)
    if widths:
        for i, w in enumerate(widths):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w
    ws.freeze_panes = "A2"


# --------------------------------------------------------------------------- assets and customers
def write_devices(target, net, rng):
    rows = []
    for fid in W.FID:
        F = net["feeders"][fid]
        spec = W.FEEDERS[W.FIX[fid]]
        inst = lambda: (W.DATA0 - dt.timedelta(days=int(rng.integers(400, 9000)))).isoformat()
        if spec.get("legacy"):
            old = spec["legacy"].replace("-", "") + "-BKR"
            rows.append([old, "BREAKER", spec["legacy"], "%s-P000" % F["prefix"], "", inst(),
                         (W.REBUILD - dt.timedelta(days=1)).isoformat(), "COTTER.%s.CB" % spec["legacy"][3:], 3, "", ""])
            rows.append([F["breaker"], "BREAKER", fid, "%s-P000" % F["prefix"], "", W.REBUILD.isoformat(), "",
                         scada_point(net, F["breaker"], W.REBUILD), 3, "", ""])
        else:
            rows.append([F["breaker"], "BREAKER", fid, "%s-P000" % F["prefix"], "", inst(), "",
                         scada_point(net, F["breaker"], W.DATA1), 3, "", ""])
        for rid in F["reclosers"]:
            D = net["devices"][rid]
            ph = "-".join(D["terminals"])
            sp = scada_point(net, rid, W.DATA1) if D.get("scada") else ""
            par = D["parent"]
            if spec.get("legacy") and par == F["breaker"]:
                old = spec["legacy"].replace("-", "") + "-BKR"
                rows.append([rid, "RECLOSER", spec["legacy"], D["pole"], old, inst(),
                             (W.REBUILD - dt.timedelta(days=1)).isoformat(), sp, 4, ph, ""])
                rows.append([rid, "RECLOSER", fid, D["pole"], par, W.REBUILD.isoformat(), "", sp, 4, ph, ""])
            else:
                rows.append([rid, "RECLOSER", fid, D["pole"], par, inst(), "", sp, 4, ph, ""])
        for lat in F["laterals"]:
            L = net["laterals"][lat]
            size = str(rng.choice(["25K", "40K", "40K", "65K", "65K", "80T", "100T"]))
            par = L["parent"]
            installed = inst()
            seg = []
            if spec.get("legacy") and par == F["breaker"]:
                old = spec["legacy"].replace("-", "") + "-BKR"
                seg.append((spec["legacy"], old, installed, W.REBUILD - dt.timedelta(days=1)))
                start2 = W.REBUILD
            elif spec.get("legacy"):
                seg.append((spec["legacy"], par, installed, W.REBUILD - dt.timedelta(days=1)))
                start2 = W.REBUILD
            else:
                start2 = None
            if L["moved"]:
                mv = L["moved"]
                if start2 is not None and mv["date"] > start2:
                    seg.append((fid, par, start2.isoformat(), mv["date"] - dt.timedelta(days=1)))
                elif start2 is None:
                    seg.append((fid, par, installed, mv["date"] - dt.timedelta(days=1)))
                seg.append((mv["feeder"], mv["parent"], mv["date"].isoformat(), None))
            else:
                seg.append((fid, par, start2.isoformat() if start2 else installed, None))
            for (feeder, parent, a, b) in seg:
                rows.append([lat, "FUSE", feeder, L.get("pole_id") or "%s-P%03d" % (F["prefix"], L["tap_pole"]),
                             parent, a if isinstance(a, str) else a.isoformat(), b.isoformat() if b else "", "", "", "",
                             size])
    legacy_of = {f["legacy"]: f["id"] for f in W.FEEDERS if f.get("legacy")}
    for r in rows:
        r.append(available_fault(net, r[0], r[1], legacy_of.get(r[2], r[2])))
        if r[1] == "FUSE":
            r[0] = shown(net, r[0])
    order = {k: i for i, k in enumerate(rng.permutation(len(rows)))}
    rows = [r for _, r in sorted(((order[i], r) for i, r in enumerate(rows)), key=lambda x: (x[1][2], x[0]))]
    write_csv(path(target, "devices"), ["device_id", "device_type", "feeder", "pole", "upstream_device",
                                        "in_service_from", "in_service_to", "scada_point", "shots_to_lockout",
                                        "terminal_phasing", "fuse_link", "available_fault_slg_a"], rows)
    return len(rows)


def available_fault(net, dev, dtype, feeder):
    """The protection study's bolted single-line-to-ground fault current at a device's location (to 10 A)."""
    if dtype == "BREAKER":
        sub = W.SUBS[net["feeders"][feeder]["sub"]]
        z1, z0 = sub[3], sub[4]
    elif dtype == "RECLOSER":
        z1, z0 = W.z_at(net, feeder, net["devices"][dev]["pos"])
    else:
        L = net["laterals"][dev]
        if L["moved"] and feeder == L["moved"]["feeder"]:
            z1, z0 = W.z_at(net, feeder, 0.0, dev, 0.0, L["moved"]["date"])
        else:
            z1, z0 = W.z_at(net, L["feeder"], L["tap"])
    return int(round(W.fault_current(z1, z0, "A", 0.0) / 10.0)) * 10


def write_transformers(target, net, rng):
    rows = []
    for tid, T in sorted(net["transformers"].items()):
        day = W.DATA1
        fid = W.device_feeder(net, T["device"], day) if T["lateral"] else T["feeder"]
        dev = T["device"]
        if net["devices"].get(dev, {}).get("type") == "BREAKER":
            dev = W.breaker_name(net, T["feeder"], day)
        rows.append([shown(net, tid), fid, shown_pole(net, T), T["phase"], T["kva"], shown(net, dev)])
    rows.sort(key=lambda r: (r[1], r[2], r[0]))
    write_csv(path(target, "transformers"), ["transformer_id", "feeder", "pole", "phase", "kva",
                                             "protective_device"], rows)
    return len(rows)


def write_sps(target, net, rng):
    rows = []
    for sp, v in sorted(net["sps"].items()):
        T = net["transformers"][v["transformer"]]
        fid = W.device_feeder(net, T["device"], W.DATA1) if T["lateral"] else T["feeder"]
        rows.append([shown(net, sp), shown(net, v["transformer"]), fid, v["cls"], v["connected"].isoformat(),
                     v["disconnected"].isoformat() if v["disconnected"] else ""])
    rows.sort(key=lambda r: (r[2], r[1], r[0]))
    write_csv(path(target, "sps"), ["service_point", "transformer_id", "feeder", "rate_class", "service_connected",
                                    "service_disconnected"], rows)
    return len(rows)


def write_feeders(target, net, rng):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Feeders"
    rows = []
    for f in W.FEEDERS:
        F = net["feeders"][f["id"]]
        plan = int(round(f["cust"] * float(rng.uniform(0.985, 1.01))))
        rows.append([f["id"], W.SUBS[f["sub"]][0], 12.47, round(F["main"] + F["lat_mi"], 1), f["ug"],
                     len(F["laterals"]), plan, F["breaker"]])
    _sheet(ws, ["Feeder", "Substation", "kV", "Overhead miles", "Underground miles", "Fused taps",
                "Customers (2025 plan)", "Feeder breaker"], rows, widths=[8, 13, 6, 15, 18, 11, 20, 14])
    ws2 = wb.create_sheet("Cotter Road 2026-03-14")
    rows2 = []
    for f in W.FEEDERS:
        if f.get("legacy"):
            F = net["feeders"][f["id"]]
            rows2.append([f["legacy"], f["id"], f["legacy"].replace("-", "") + "-BKR", F["breaker"],
                          "COTTER.%s.CB" % f["legacy"][3:], scada_point(net, F["breaker"], W.REBUILD)])
    _sheet(ws2, ["Old feeder", "New feeder", "Old breaker", "New breaker", "Old SCADA point", "New SCADA point"],
           rows2, widths=[11, 11, 12, 13, 16, 16])
    p = path(target, "feeders")
    wb.save(p)
    PP.normalize_ooxml(p, "Shawn Hartman", "Shawn Hartman", "2024-02-19T15:02:44Z", "2026-03-16T13:27:05Z",
                       excel=True)
    return len(rows)


def write_subs(target):
    feats = []
    for sid, (name, x, y, _, _) in W.SUBS.items():
        lat, lon = W.to_latlon(x, y)
        feats.append({"type": "Feature", "properties": {"substation": sid, "name": name, "voltage_kv": "69/12.47"},
                      "geometry": {"type": "Point", "coordinates": [round(lon, 5), round(lat, 5)]}})
    gj = {"type": "FeatureCollection", "name": "substations", "crs": {"type": "name", "properties":
          {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}, "features": feats}
    with open(path(target, "subs"), "w") as fh:
        json.dump(gj, fh, indent=1)
        fh.write("\n")
    return len(feats)


# --------------------------------------------------------------------------- weather
def write_strokes(target, stk, rng):
    rows = []
    for (t, x, y, amp, kind) in stk:
        lat, lon = W.to_latlon(x, y)
        rows.append([iso_utc(t), "%.4f" % lat, "%.4f" % lon, "%.1f" % amp, kind,
                     "%.1f" % float(rng.uniform(0.2, 1.9)), int(rng.integers(4, 23))])
    write_csv(path(target, "strokes"), ["utc_time", "latitude", "longitude", "peak_current_ka", "type",
                                        "semi_major_km", "sensors"], rows)
    return len(rows)


def write_asos(target, wx, rng):
    rows = []
    for j, h in enumerate(wx["hours"]):
        h = int(h)
        if h < sim.T0 - 7 * sim.MS_H or h > sim.T1 + sim.MS_H:
            continue
        t = h + 53 * sim.MS_MIN
        miss = rng.random() < 0.004
        wxc = []
        if wx["ts"][j]:
            wxc.append("TSRA" if wx["precip"][j] > 0.02 else "TS")
        elif wx["precip"][j] > 0.08:
            wxc.append("RA")
        elif wx["precip"][j] > 0.0:
            wxc.append("-RA")
        if wx["fog"][j]:
            wxc.append("FG")
        elif wx["mist"][j]:
            wxc.append("BR")
        g = wx["gust"][j]
        rows.append([STATION, iso_utc(t, ms=False)[:16].replace("T", " "),
                     "M" if miss else "%.1f" % wx["temp"][j], "M" if miss else "%.1f" % wx["dew"][j],
                     "M" if miss else "%.2f" % wx["rh"][j], int(round(wx["wspd"][j])),
                     int(round(g)) if g > 0 else "M", "%.2f" % wx["vis"][j],
                     "%.2f" % wx["precip"][j] if wx["precip"][j] >= 0.005 else ("T" if wx["precip"][j] > 0 else "0.00"),
                     " ".join(wxc) if wxc else "M"])
    write_csv(path(target, "asos"), ["station", "valid", "tmpf", "dwpf", "relh", "sknt", "gust", "vsby", "p01i",
                                     "wxcodes"], rows)
    return len(rows)


# --------------------------------------------------------------------------- distractors
def write_veg(target, net, rng):
    rows = []
    wo = int(rng.integers(30000, 34000))
    contractors = ["Weller Line Clearance", "Hackberry Hollow Tree Co.", "Brennan Utility Forestry"]
    plan = {"MLR-2": [(W.CLEARANCE[0], W.CLEARANCE[1])]}
    for f in W.FEEDERS:
        fid = f["id"]
        F = net["feeders"][fid]
        jobs = plan.get(fid, [])
        if fid not in plan and fid != "NYD-2":
            k = int(rng.integers(1, 3))
            for _ in range(k):
                d0 = dt.date(2023, 1, 9) + dt.timedelta(days=int(rng.integers(0, 1300)))
                jobs.append((d0, d0 + dt.timedelta(days=int(rng.integers(3, 21)))))
        for (a, b) in sorted(jobs):
            wo += int(rng.integers(3, 40))
            full = fid == "MLR-2"
            miles = round(F["main"] + F["lat_mi"], 1) if full else round(float(rng.uniform(0.8, 0.55 * (F["main"] + F["lat_mi"]))), 1)
            rows.append(["VM-%d" % wo, fid if (fid not in ("CTR-1", "CTR-2", "CTR-3") or a >= W.REBUILD) else
                         W.FEEDERS[W.FIX[fid]]["legacy"], a.isoformat(), b.isoformat(), miles,
                         "FULL CIRCUIT" if full else str(rng.choice(["HOT SPOT", "MID-CYCLE", "HOT SPOT"])),
                         contractors[int(rng.integers(0, 3))]])
    rows.sort(key=lambda r: (r[2], r[1]))
    no = int(rows[0][0][3:])
    for r in rows:
        r[0] = "VM-%d" % no
        no += int(rng.integers(4, 61))
    write_csv(path(target, "veg"), ["work_order", "circuit", "start_date", "completed", "miles_cleared", "scope",
                                    "contractor"], rows)
    return len(rows)


def write_blinks(target, net, S, TR, rng):
    R = truth.Reach(net)
    rows = []
    by_dev = {}
    for sp, v in net["sps"].items():
        by_dev.setdefault(v["transformer"], []).append(sp)
    for e in TR["events"]:
        lt = sim.local_dt(e["t"])
        awake = 0.25 if (lt.hour < 6 or lt.hour >= 23) else (0.6 if lt.hour < 8 else 1.0)
        n = int(rng.poisson(0.0011 * e["n"] * awake))
        if n == 0:
            continue
        trs = R.transformers(e["device"], e["day"])
        for _ in range(n):
            tid = trs[int(rng.integers(0, len(trs)))]
            sps = by_dev.get(tid, [])
            if not sps:
                continue
            sp = sps[int(rng.integers(0, len(sps)))]
            t = e["t"] + int(rng.uniform(4, 600)) * sim.MS_MIN
            rows.append([sim.local_dt(t).strftime("%Y-%m-%d %H:%M"), sp, str(rng.choice(["PHONE", "PHONE", "WEB", "IVR"])),
                         str(rng.choice(["LIGHTS BLINKING", "LIGHTS BLINKING", "FLICKER", "CLOCKS RESET"]))])
    rows.sort()
    out = []
    no = int(rng.integers(500000, 600000))
    for r in rows:
        no += int(rng.integers(1, 30))
        out.append(["C%d" % no, r[0], shown(net, r[1])] + r[2:])
    write_csv(path(target, "blinks"), ["contact_id", "contact_time", "service_point", "channel", "reason"], out)
    return len(out)
