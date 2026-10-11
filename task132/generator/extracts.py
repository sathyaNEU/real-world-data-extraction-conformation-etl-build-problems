"""The system extracts: the EAM asset register, the PSU rotating-item history, the work-order export,
substations, spares stock and Veldtek's RMA log."""
import datetime as dt
import zlib

import numpy as np
import openpyxl
import pandas as pd
from openpyxl.styles import Alignment, Font

import sim as S
import world as W

MODELS = {
    "VPR-340": ("Veldtek Protection Systems", "Feeder protection"),
    "VPR-220": ("Veldtek Protection Systems", "Feeder protection"),
    "NX-9": ("Norland Controls", "Feeder protection"),
    "AT-7": ("Arcwell Automation", "Recloser control"),
    "NX-5": ("Norland Controls", "Transformer differential"),
    "KDR-30": ("Kestrel Grid Devices", "Bus protection"),
    "RT-400": ("Arcwell Automation", "Substation RTU"),
    "RT-600": ("Arcwell Automation", "Substation RTU"),
}
SERIAL = {"VPR-340": "V340-%02d-%05d", "VPR-220": "V220-%02d-%05d", "NX-9": "N9-%02d-%05d", "NX-5": "N5-%02d-%05d",
          "AT-7": "AW7%02d%05d", "KDR-30": "K30%02d%04d", "RT-400": "AW4%02d%05d", "RT-600": "AW6%02d%05d"}
GOLIVE = W.MIGRATION
END = dt.date(2026, 10, 1)
# the device that goes into a bay when the old one comes out
NEW_DEVICE = {"VPR-340": "NX-9", "VPR-220": "NX-9", "NX-9": "NX-9", "NX-5": "NX-5", "KDR-30": "KDR-30",
              "RT-400": "RT-600", "AT-7": "AT-7"}
MFG_LAG = (20, 270)                    # days from manufacture to installation of a relay, control or RTU
STORES = {"North": "North Depot", "Central": "Central Stores (Barrie Road)", "South": "South Depot"}


def _d(rng, y0, y1):
    """a working day in a month drawn from y0 to y1"""
    first = dt.date(int(rng.integers(y0, y1 + 1)), int(rng.integers(1, 13)), 1)
    return S.pick_bday(rng, first, S.month_add(first, 1) - dt.timedelta(days=1))


def assets(rng, subs, fl, prog):
    """every protection asset at every station since 1988, with its bay, install and retirement dates"""
    cut = {sc: d for sc, d in zip(prog["sub_code"], prog["cut_days"]) if isinstance(d, list)}
    camp = fl.groupby("sub_code")["install"].min().to_dict()
    out = []
    for _, s in subs.iterrows():
        sc = s.sub_code
        ts = s.station_type == "TS"
        days = cut.get(sc)
        mine = fl[fl["sub_code"] == sc]
        for _, r in mine.iterrows():
            out.append(dict(model="VPR-340", sub_code=sc, bay=r.bay, install=r.install,
                            retired=r.retire if isinstance(r.retire, dt.date) else None, relay_key=r.relay_key))
        nv = len(mine)
        if nv:
            extra = int(rng.integers(1, 5)) if ts else int(rng.integers(0, 3))
            for j in range(extra):
                y0 = max(camp[sc].year + 1, 2011)
                out.append(dict(model="NX-9", sub_code=sc, bay="F%02d" % (nv + j + 1), install=_d(rng, min(y0, 2026), 2026),
                                retired=None, relay_key=None))
        else:
            nfeed = int(rng.integers(12, 21)) if ts else int(rng.integers(5, 13))
            rural = (not ts) and rng.random() < 0.35
            for j in range(nfeed):
                bay = "F%02d" % (j + 1)
                u = rng.random()
                if rural and u < 0.45:
                    out.append(dict(model="AT-7", sub_code=sc, bay=bay, install=_d(rng, 2000, 2020), retired=None, relay_key=None))
                elif u < 0.62:
                    inst = _d(rng, 1989, 2004)
                    ret = None
                    if rng.random() < 0.13:
                        ret = _d(rng, 2021, 2026)
                        if ret > W.ASOF:
                            ret = None
                    out.append(dict(model="VPR-220", sub_code=sc, bay=bay, install=inst, retired=ret, relay_key=None))
                    if ret:
                        out.append(dict(model="NX-9", sub_code=sc, bay=bay, install=ret, retired=None, relay_key=None))
                else:
                    out.append(dict(model="NX-9", sub_code=sc, bay=bay, install=_d(rng, 2010, 2026), retired=None, relay_key=None))
        for t in range(1, s.n_tx + 1):
            out.append(dict(model="NX-5", sub_code=sc, bay="T%d" % t, install=_d(rng, 1995, 2024), retired=None, relay_key=None))
        for b in range(1, s.n_bus + 1):
            out.append(dict(model="KDR-30", sub_code=sc, bay="B%d" % b, install=_d(rng, 1996, 2022), retired=None, relay_key=None))
        rtu = _d(rng, 2003, 2016)
        rret = None
        if days is None and rng.random() < 0.05:
            rret = _d(rng, 2021, 2025)
            out.append(dict(model="RT-600", sub_code=sc, bay="RTU", install=rret, retired=None, relay_key=None))
        out.append(dict(model="RT-400", sub_code=sc, bay="RTU", install=rtu, retired=rret, relay_key=None))
        if days:
            # station rebuild: each bay is cut over on its own working day and the new device goes in the day the old
            # one comes out; a device fitted in the two years before the rebuild stays in service
            keep_from = days[0] - dt.timedelta(days=730)
            new = []
            for o in [o for o in out if o["sub_code"] == sc]:
                if o["model"] == "VPR-340":
                    new.append(dict(model="NX-9", sub_code=sc, bay=o["bay"], install=o["retired"], retired=None, relay_key=None))
                elif o["retired"] is None and o["install"] < keep_from:
                    o["retired"] = S.cut_date(days, o["bay"], nv)
                    new.append(dict(model=NEW_DEVICE[o["model"]], sub_code=sc, bay=o["bay"], install=o["retired"],
                                    retired=None, relay_key=None))
            out.extend(new)
    a = pd.DataFrame(out)
    a = a[(a["retired"].isna() | (a["retired"] >= GOLIVE)) & (a["install"] <= W.ASOF)].copy()
    return a.reset_index(drop=True)


def register(rng, subs, fl, prog):
    """protection asset register: every asset in service on 1 Jan 2021 or installed since. Returns the register, the
    asset number of each VPR-340 relay, and each VPR-340 relay's date of manufacture."""
    a = assets(rng, subs, fl, prog)
    leg = dict(zip(subs["sub_code"], subs["legacy_region"]))
    cur = dict(zip(subs["sub_code"], subs["region"]))
    a["loaded"] = a["install"] < GOLIVE
    # EAM asset numbers: the go-live load in location order, then new assets as they were created; other asset
    # classes share the sequence, so protection numbers have gaps
    a["_o"] = [(0, s, b, str(i)) if l else (1, str(i), s, b) for s, b, i, l in zip(a["sub_code"], a["bay"], a["install"], a["loaded"])]
    a = a.sort_values("_o", key=lambda c: c.map(lambda t: t), kind="mergesort").reset_index(drop=True)
    num, ids = 1000000, []
    for l in a["loaded"]:
        num += int(rng.integers(1, 9)) if l else int(rng.integers(4, 61))
        if not l and num < 1046000:
            num = 1046000 + int(rng.integers(0, 400))
        ids.append("P%07d" % num)
    a["asset_id"] = ids
    # manufacturer serials: the year of manufacture and the maker's running number, in order of manufacture (the
    # maker numbers every unit it builds, so ours have gaps)
    a["mfg"] = [i - dt.timedelta(days=int(rng.integers(*MFG_LAG))) for i in a["install"]]
    a["serial_no"] = ""
    for m, g in a.groupby("model"):
        seq = int(rng.integers(100, 3000))
        for i in g.sort_values(["mfg", "asset_id"], kind="mergesort").index:
            seq += int(rng.integers(1, 23))
            a.at[i, "serial_no"] = SERIAL[m] % (a.at[i, "mfg"].year % 100, seq)
    a["manufacturer"] = [MODELS[m][0] for m in a["model"]]
    a["function"] = [MODELS[m][1] for m in a["model"]]
    a["status"] = ["RETIRED" if r is not None and not pd.isna(r) else "IN SERVICE" for r in a["retired"]]
    a["region"] = [leg[s] if (l or i < W.REORG) else cur[s] for s, l, i in zip(a["sub_code"], a["loaded"], a["install"])]
    a["install_date"] = a["install"]
    a["retired_date"] = [None if (r is None or pd.isna(r)) else r for r in a["retired"]]
    reg = a.sort_values(["sub_code", "bay", "install_date", "asset_id"], kind="mergesort").reset_index(drop=True)
    cols = ["asset_id", "model", "manufacturer", "function", "sub_code", "bay", "serial_no", "install_date", "status",
            "retired_date", "region"]
    keyed = [(int(k), aid, mf) for k, aid, mf in zip(reg["relay_key"], reg["asset_id"], reg["mfg"]) if k is not None and not pd.isna(k)]
    return reg[cols], {k: aid for k, aid, _ in keyed}, {k: mf for k, _, mf in keyed}


def psu_cycle(rng, sp, f, key2aid, relay_mfg):
    """Module serials for every spell, and the failed modules sent back to Veldtek under RMA: repaired ones come
    back to stores and some are fitted again later. A new module's serial carries its year of manufacture and
    Veldtek's running number in order of manufacture; a repaired module keeps its serial."""
    sp = sp.copy()
    fw = f[f["month"] >= GOLIVE].sort_values("reported", kind="mergesort")
    fail_at = {(int(r.relay_key), int(r.module)): r for r in fw.itertuples()}
    spell_of = {(int(k), int(m)): i for i, k, m in zip(sp.index, sp["relay_key"], sp["module"])}
    events = [(sp.at[i, "fitted"], 0, i) for i in sp.sort_values("fitted", kind="mergesort").index]
    events += [(r.done, 1, (int(r.relay_key), int(r.module))) for r in fw.itertuples()]
    events.sort(key=lambda e: (e[0], e[1]))
    made, origin, pool, ships = {}, {}, [], []
    for when, kind, ref in events:
        if kind == 0:
            i = ref
            key, mod = int(sp.at[i, "relay_key"]), int(sp.at[i, "module"])
            if mod == 0:
                made[i] = relay_mfg[key] - dt.timedelta(days=int(rng.integers(7, 45)))     # built into the relay
            elif sp.at[i - 1, "reason"] == "CAMPAIGN":
                made[i] = when - dt.timedelta(days=int(rng.integers(30, 160)))            # built for the bulletin
            else:
                avail = [p for p in pool if p[0] <= when]
                if when >= GOLIVE and avail and rng.random() < 0.45:
                    pick = min(avail)
                    pool.remove(pick)
                    origin[i] = pick[1]
                else:
                    made[i] = when - dt.timedelta(days=int(rng.integers(45, 900)))       # from stores stock
        else:
            r = fail_at[ref]
            ship = S.add_bdays(r.done, int(rng.integers(2, 15)))
            if ship > W.ASOF - dt.timedelta(days=12) or rng.random() > 0.55:
                continue
            recv = S.add_bdays(ship, int(rng.integers(2, 6)))
            u = rng.random()
            res = "REPAIRED" if u < 0.78 else ("NO FAULT FOUND" if u < 0.82 else "BEYOND ECONOMIC REPAIR")
            back = S.add_bdays(recv, int(rng.integers(18, 54)))
            if res == "BEYOND ECONOMIC REPAIR":
                back = None
            elif back > W.ASOF:
                res, back = "OPEN", None
            else:
                pool.append((S.add_bdays(back, int(rng.integers(1, 6))), spell_of[ref]))
            ships.append(dict(relay_key=ref[0], module=ref[1], spell=spell_of[ref], ship=ship, received=recv, result=res,
                              returned=back))
    serial, n = {}, 21000
    for i in sorted(made, key=lambda j: (made[j], j)):
        n += int(rng.integers(1, 9))
        serial[i] = "PS02-%02d-%05d" % (made[i].year % 100, n)

    def serial_of(i):
        while i in origin:
            i = origin[i]
        return serial[i]

    sp["serial"] = [serial_of(i) for i in sp.index]
    sp["asset_id"] = [key2aid[int(k)] for k in sp["relay_key"]]
    ships = pd.DataFrame(ships)
    ships["serial"] = [serial_of(i) for i in ships["spell"]]
    return sp, ships, len(pool)


CREWS_LEGACY = {"Lakeshore": [("Lakeshore P&C 1", 0.6), ("Lakeshore P&C 2", 0.4)], "Ridge": [("Ridge P&C", 1.0)],
                "Valley": [("Valley P&C 1", 0.55), ("Valley P&C 2", 0.45)], "Harbour": [("Harbour P&C", 0.8), ("Harbour Test", 0.2)]}
CREWS_CURRENT = {"North": [("North P&C 1", 0.57), ("North P&C 2", 0.43)],
                 "Central": [("Central P&C 1", 0.42), ("Central P&C 2", 0.36), ("Central P&C 3", 0.22)],
                 "South": [("South P&C 1", 0.52), ("South P&C 2", 0.48)]}
# hours a crew books for the round trip to site, and its pace on the job; the north and lakeshore crews cover the
# rural stations
CREW = {"Lakeshore P&C 1": (1.2, 1.00), "Lakeshore P&C 2": (1.4, 1.05), "Ridge P&C": (0.9, 1.00),
        "Valley P&C 1": (0.7, 0.95), "Valley P&C 2": (0.8, 1.05), "Harbour P&C": (0.5, 1.00), "Harbour Test": (0.4, 0.90),
        "North P&C 1": (1.5, 1.00), "North P&C 2": (1.7, 1.05), "Central P&C 1": (0.4, 0.95), "Central P&C 2": (0.5, 1.00),
        "Central P&C 3": (0.6, 1.10), "South P&C 1": (0.8, 1.00), "South P&C 2": (0.9, 0.95)}
PSU_TEXT = ["SCADA relay fail alarm. PSU module u/s, replaced from {store} stock and function tested",
            "Power supply failure, relay out of service. PSU swapped, settings verified",
            "No front panel, no healthy LED. Replaced PSU module, relay back in service",
            "Watchdog alarm traced to power supply. PSU replaced, trip test OK",
            "Relay rebooting intermittently, PSU output low on test. Module replaced from {store}",
            "PSU fail alarm {name}. Module changed, event records downloaded",
            "Relay unresponsive, DC supply OK at terminals. PSU module replaced",
            "Burnt smell at panel, PSU module failed. Replaced and panel cleaned",
            "Relay found dead on site, healthy LED off. PSU failed, new module from {store}, tested OK"]
STORM_TEXT = "Healthy LED off after the {day} storm. PSU failed, replaced from {store} stock"
KIND = {"VPR-340": "relay", "VPR-220": "relay", "NX-9": "relay", "NX-5": "relay", "KDR-30": "relay", "AT-7": "recloser",
        "RT-400": "rtu", "RT-600": "rtu"}
# corrective work orders per device-year at ten years old; older devices fail more (rate x (0.6 + 0.04 x age))
CM_BASE = {"VPR-340": 0.035, "VPR-220": 0.05, "NX-9": 0.035, "NX-5": 0.04, "KDR-30": 0.035, "AT-7": 0.06,
           "RT-400": 0.055, "RT-600": 0.04}
COMP = {"relay": (["CPU", "IO", "DISP", "COMMS", "PSU"], [0.18, 0.33, 0.12, 0.22, 0.15]),
        "recloser": (["PSU", "CPU", "IO", "DISP", "COMMS"], [0.35, 0.12, 0.25, 0.08, 0.20]),
        "rtu": (["CPU", "IO", "COMMS", "PSU"], [0.15, 0.35, 0.35, 0.15])}
FAULT_TEXT = {
    ("relay", "CPU"): ["Processor card fault, card replaced and settings reloaded", "CPU self-test failure, processor card swapped",
                       "Relay locked up, processor card replaced, firmware reloaded"],
    ("relay", "IO"): ["Input card failed self-test, card replaced", "Binary input chatter traced to IO card, card replaced",
                      "Output contact welded, IO card replaced and trip tested"],
    ("relay", "DISP"): ["Display blank, front panel replaced", "Keypad unresponsive, front panel module changed"],
    ("relay", "COMMS"): ["Lost SCADA comms to relay, comms card replaced", "DNP3 link down, comms card reset then replaced",
                         "Fibre transceiver on comms card failed, card replaced"],
    ("relay", "PSU"): ["Relay power supply failed, module replaced and relay tested", "PSU fault alarm, module replaced and tested"],
    ("recloser", "PSU"): ["Control battery failed load test, battery replaced", "Recloser control charger failed, PSU module replaced"],
    ("recloser", "CPU"): ["Recloser control locked up, processor board replaced and settings loaded"],
    ("recloser", "IO"): ["Trip/close output on recloser control failed, IO board replaced", "Recloser status input stuck, IO board replaced"],
    ("recloser", "DISP"): ["Control panel display faded, front panel replaced"],
    ("recloser", "COMMS"): ["Radio link to recloser control lost, comms module replaced",
                            "SCADA polling to recloser failed, comms module changed"],
    ("rtu", "CPU"): ["RTU processor card failed, replaced and configuration reloaded"],
    ("rtu", "IO"): ["RTU status input card failed, replaced, points checked with control room",
                    "RTU analog input card drifting, replaced and calibrated",
                    "RTU control output card failed, replaced, controls tested with control room"],
    ("rtu", "COMMS"): ["RTU comms to control centre lost, comms card replaced", "DNP3 link to master down, RTU port card replaced"],
    ("rtu", "PSU"): ["RTU power supply failed, module replaced, points verified"],
}
NFF_TEXT = {"relay": ["Relay fail alarm, reset and monitored, no fault found", "Spurious relay alarm, event records reviewed, no fault found",
                      "Alarm investigated, loose wiring at panel retightened"],
            "recloser": ["Recloser control alarm, battery and charger checked, no fault found"],
            "rtu": ["RTU alarm investigated, points checked with control room, no fault found"]}
HOLD = {"relay": "backup protection in service", "rtu": "affected points on manual reporting",
        "recloser": "recloser left on non-reclose"}
PART = {"CPU": "processor card", "IO": "IO card", "DISP": "display", "COMMS": "comms card", "PSU": "power supply"}
MAKER = {"Veldtek Protection Systems": "Veldtek", "Norland Controls": "Norland", "Arcwell Automation": "Arcwell",
         "Kestrel Grid Devices": "Kestrel"}
RELAY_PM = ["Routine relay test to P&C std 3.2 - {bay}", "{bay} relay test, settings and trip check",
            "Maintenance test {bay}, secondary injection", "Periodic test {bay} per P&C std 3.2"]
RTU_PM = ["RTU functional check and point-to-point test", "RTU annual maintenance, I/O and comms checked",
          "RTU functional test, SCADA points verified with control room"]
AT7_PM = ["Recloser control test and battery load test - {bay}", "Annual recloser control check {bay}, battery replaced"]


def _crew(rng, region_pool):
    names = [c for c, _ in region_pool]
    w = np.array([p for _, p in region_pool])
    return names[int(rng.choice(len(names), p=w / w.sum()))]


def _hours(rng, crew, mu, sd, lo=0.25, travel=True):
    """task hours at the crew's pace plus the crew's travel to site, booked to the quarter hour"""
    trip, pace = CREW[crew]
    h = float(np.exp(rng.normal(np.log(mu), sd))) * pace
    if travel:
        h += trip * float(np.exp(rng.normal(0.0, 0.3)))
    return max(lo, round(h * 4) / 4)


def _lag(rng, kind):
    """days from raising to completion: calendar days for corrective work, working days for planned work"""
    u = rng.random()
    if kind == "CM":
        return 0 if u < 0.45 else 1 if u < 0.66 else int(rng.integers(2, 5)) if u < 0.82 else int(rng.integers(5, 15)) if u < 0.94 else int(rng.integers(15, 46))
    if kind == "EM":
        return 0 if u < 0.8 else 1 if u < 0.95 else int(rng.integers(2, 4))
    if kind == "PM":
        return 0 if u < 0.7 else int(rng.integers(1, 4)) if u < 0.9 else int(rng.integers(4, 13))
    if kind == "INSP":
        return 0 if u < 0.85 else 1 if u < 0.95 else int(rng.integers(2, 6))
    if kind == "MOD":
        return 0 if u < 0.55 else int(rng.integers(1, 6)) if u < 0.85 else int(rng.integers(6, 21)) if u < 0.97 else int(rng.integers(21, 61))
    return 0 if u < 0.6 else int(rng.integers(1, 4)) if u < 0.95 else int(rng.integers(4, 9))


def work_orders(rng, subs, reg, f, sp, ships, rebuilt):
    cur = dict(zip(subs["sub_code"], subs["region"]))
    leg = dict(zip(subs["sub_code"], subs["legacy_region"]))
    names = dict(zip(subs["sub_code"], subs["sub_name"]))
    kind_of = dict(zip(subs["sub_code"], subs["station_type"]))
    aid2sub = dict(zip(reg["asset_id"], reg["sub_code"]))
    model = dict(zip(reg["asset_id"], reg["model"]))
    maker = dict(zip(reg["asset_id"], reg["manufacturer"]))
    inst = dict(zip(reg["asset_id"], reg["install_date"]))
    retd = {a: (r if isinstance(r, dt.date) else None) for a, r in zip(reg["asset_id"], reg["retired_date"])}
    key2aid = dict(zip(sp["relay_key"], sp["asset_id"]))
    aid2key = {a: k for k, a in key2aid.items()}
    rows = []

    def in_service(aid, d):
        r = retd.get(aid)
        return inst[aid] <= d and (r is None or d < r)

    def crew(sub, d):
        return _crew(rng, CREWS_CURRENT[cur[sub]] if d >= W.REORG else CREWS_LEGACY[leg[sub]])

    def add(d, aid, sub, wt, comp, desc, done, hours, key=None, cr=None, status=None):
        """hours: (mu, sd, lo) of the task, or a callable of the crew; done: completion date, None while open"""
        cr = cr or crew(sub, d)
        h = hours(cr) if callable(hours) else _hours(rng, cr, *hours)
        rows.append(dict(reported_date=d, asset_id=aid, sub_code=sub, work_type=wt, status=status, failed_component=comp,
                         description=desc, labour_hours=h, completed_date=done, crew=cr,
                         region=cur[sub] if d >= W.REORG else leg[sub], _key=key))

    def planned_done(d, kind):
        return S.add_bdays(d, _lag(rng, kind))

    storms = {}
    for day, regions in W.STORMS:
        for g in regions:
            storms.setdefault(g, []).append(day)

    def after_storm(sub, d):
        hit = [s for s in storms.get(cur[sub], []) if 0 <= (d - s).days <= 2]
        return hit[0] if hit else None

    # PSU failures on the VPR-340 fleet as recorded from the go-live; the paperwork now and then closes a day or two
    # after the new module went in
    fw = f[f["month"] >= GOLIVE].sort_values("reported", kind="mergesort")
    for r in fw.itertuples():
        aid = key2aid[r.relay_key]
        sub = aid2sub[aid]
        store = STORES[cur[sub]]
        storm = after_storm(sub, r.reported)
        if storm is not None:
            t = STORM_TEXT.format(day=storm.strftime("%d %b").lstrip("0"), store=store)
        else:
            t = PSU_TEXT[int(rng.integers(len(PSU_TEXT)))].format(store=store, name=names[sub])
        wt = "EM" if r.em else "CM"
        done = r.done
        if rng.random() < 0.12:
            late = done + dt.timedelta(days=int(rng.integers(1, 3)))
            done = late if late <= W.ASOF else done
        add(r.reported, aid, sub, wt, "PSU", t, done, (2.2, 0.35, 1.0), key=("F", int(r.relay_key), int(r.module)))
        if rng.random() < 0.045:
            add(r.reported, aid, sub, wt, "PSU", "Duplicate - raised twice from SCADA alarm", None, lambda c: 0.0, status="CANC")
    for s in ships.itertuples():
        aid = key2aid[s.relay_key]
        add(s.ship, aid, aid2sub[aid], "LOG", "PSU",
            ["Ship failed PSU s/n %s to Veldtek, RMA requested", "Return PSU %s to Veldtek repair centre",
             "Courier failed module %s to Veldtek under RMA"][int(rng.integers(3))] % s.serial,
            planned_done(s.ship, "LOG"), (0.4, 0.4, 0.25, False), key=("L", int(s.relay_key), int(s.module)))
    months = S.months_between(GOLIVE, END)

    # corrective work on every device (other than the VPR-340 PSU failures above): monthly at a rate that rises with
    # the device's age; the crew records the failed card, or nothing when no fault is found
    ids = reg["asset_id"].to_numpy()
    mdl = reg["model"].to_numpy()
    base = np.array([CM_BASE[m] for m in mdl])
    ins = np.array([d.toordinal() for d in reg["install_date"]])
    ret = np.array([d.toordinal() if isinstance(d, dt.date) else 10 ** 7 for d in reg["retired_date"]])
    for m in months:
        mid = (m + dt.timedelta(days=14)).toordinal()
        live = (ins <= mid) & (ret > mid)
        age = np.maximum(0.0, (mid - ins) / 365.25)
        k = rng.poisson(np.where(live, base * (0.6 + 0.04 * age) / 12.0, 0.0))
        last = (S.month_add(m, 1) - dt.timedelta(days=1)).day
        for j in np.nonzero(k)[0]:
            for _ in range(int(k[j])):
                aid = ids[j]
                d = dt.date(m.year, m.month, int(rng.integers(1, last + 1)))
                if d > W.ASOF or not in_service(aid, d):
                    continue
                sub = aid2sub[aid]
                kd = KIND[mdl[j]]
                a_age = (d - inst[aid]).days / 365.25
                wt = "CM" if rng.random() < 0.82 else "EM"
                if rng.random() < 0.1:
                    add(d, aid, sub, wt, "", NFF_TEXT[kd][int(rng.integers(len(NFF_TEXT[kd])))],
                        d + dt.timedelta(days=_lag(rng, wt)), (1.5, 0.4, 0.5))
                    continue
                comps, p = COMP[kd]
                if mdl[j] == "VPR-340":
                    comps, p = comps[:4], np.array(p[:4]) / sum(p[:4])
                comp = comps[int(rng.choice(len(comps), p=p))]
                opts = FAULT_TEXT[(kd, comp)]
                t = opts[int(rng.integers(len(opts)))]
                warranty = a_age < 2.0
                if warranty:
                    t += ", under warranty"
                elif a_age >= 25 and mdl[j] in ("VPR-220", "VPR-340") and comp != "PSU":
                    t += ". Card from recovered spares"
                wait = (dt.date(2026, 3, 1) <= d <= dt.date(2026, 8, 31) and mdl[j] != "VPR-340"
                        and comp in ("CPU", "IO", "COMMS") and rng.random() < 0.15)
                if wait:
                    add(d, aid, sub, wt, comp, t.split(",")[0] + ". Awaiting replacement %s from %s, %s"
                        % (PART[comp], MAKER[maker[aid]], HOLD[kd]), None, (2.0, 0.4, 0.5))
                    continue
                done = d + dt.timedelta(days=_lag(rng, wt))
                add(d, aid, sub, wt, comp, t, done, (2.4, 0.45, 0.5))
                ships_back = warranty or (comp in ("CPU", "IO", "COMMS") and mdl[j] in ("NX-9", "NX-5", "KDR-30", "RT-600", "AT-7", "VPR-340")
                                          and rng.random() < 0.3)
                if ships_back:
                    d2 = S.add_bdays(done, int(rng.integers(2, 11)))
                    if d2 <= W.ASOF:
                        add(d2, aid, sub, "LOG", comp, ("Return failed %s to %s under warranty" if warranty else
                                                        "Ship failed %s to %s for repair") % (PART[comp], MAKER[maker[aid]]),
                            planned_done(d2, "LOG"), (0.4, 0.4, 0.25, False))

    # periodic tests: relays two-yearly at transformer stations and three-yearly at distribution stations, recloser
    # controls and RTUs every year
    for a in reg.itertuples():
        kd = KIND[a.model]
        cyc = 365 if kd in ("rtu", "recloser") else (730 if kind_of[a.sub_code] == "TS" else 1095)
        texts = RTU_PM if kd == "rtu" else AT7_PM if kd == "recloser" else RELAY_PM
        d = GOLIVE + dt.timedelta(days=int(rng.integers(0, cyc)))
        end = a.retired_date if isinstance(a.retired_date, dt.date) else END
        while d < end and d <= W.ASOF:
            dd = S.pick_bday(rng, max(GOLIVE, d - dt.timedelta(days=3)), d + dt.timedelta(days=3))
            if a.install_date <= dd < end and dd <= W.ASOF:
                mu = 4.5 if a.model in ("NX-5", "KDR-30") else 5.0 if kd == "rtu" else 3.0 if kd == "recloser" else 3.5
                add(dd, a.asset_id, a.sub_code, "PM", "", texts[int(rng.integers(len(texts)))].format(bay=a.bay),
                    planned_done(dd, "PM"), (mu, 0.3, 1.0))
            d = d + dt.timedelta(days=int(cyc + rng.integers(-30, 31) if cyc == 365 else cyc + rng.integers(-45, 46)))

    # station inspections: monthly (a few missed), a second walkdown at transformer stations, quarterly DC checks,
    # a yearly battery discharge test and infrared scan, half-yearly relay record reviews at transformer stations
    for s in subs.itertuples():
        crc = zlib.crc32(s.sub_code.encode())
        for m in months:
            if rng.random() < 0.025:
                continue
            d = S.pick_bday(rng, m, m + dt.timedelta(days=24))
            if d > W.ASOF:
                continue
            add(d, "", s.sub_code, "INSP", "",
                ["Monthly station inspection", "Monthly inspection - no defects", "Monthly P&C panel walkdown",
                 "Monthly insp, annunciator test OK"][int(rng.choice(4, p=[0.55, 0.2, 0.15, 0.1]))],
                planned_done(d, "INSP"), (0.6, 0.35, 0.5))
            if s.station_type == "TS":
                d4 = S.pick_bday(rng, d + dt.timedelta(days=12), d + dt.timedelta(days=16))
                if d4 <= W.ASOF and rng.random() < 0.93:
                    add(d4, "", s.sub_code, "INSP", "", "TS walkdown, alarms and panel lamps checked", planned_done(d4, "INSP"),
                        (0.5, 0.35, 0.5))
                if m.month in (3, 9) and rng.random() < 0.9:
                    d5 = S.pick_bday(rng, d + dt.timedelta(days=1), d + dt.timedelta(days=10))
                    if d5 <= W.ASOF:
                        add(d5, "", s.sub_code, "INSP", "", "Relay event and disturbance records downloaded and reviewed",
                            planned_done(d5, "INSP"), (1.5, 0.3, 0.5))
            if m.month in (1, 4, 7, 10) and rng.random() < 0.96:
                d2 = S.pick_bday(rng, d, d + dt.timedelta(days=6))
                if d2 <= W.ASOF:
                    add(d2, "", s.sub_code, "INSP", "", "Quarterly DC battery and charger check", planned_done(d2, "INSP"),
                        (1.0, 0.3, 0.5))
            if m.month == 5 + crc % 6 and rng.random() < 0.95:
                d6 = S.pick_bday(rng, d + dt.timedelta(days=2), d + dt.timedelta(days=12))
                if d6 <= W.ASOF:
                    add(d6, "", s.sub_code, "INSP", "", "Annual DC battery discharge test, cells within limits",
                        planned_done(d6, "INSP"), (3.0, 0.3, 1.0))
            if m.month == 2 + (crc >> 4) % 9:
                d7 = S.pick_bday(rng, d + dt.timedelta(days=1), d + dt.timedelta(days=12))
                if d7 <= W.ASOF:
                    add(d7, "", s.sub_code, "INSP", "", "Annual settings check, as-left settings compared with approved files",
                        planned_done(d7, "INSP"), (2.0, 0.35, 0.5))
            if m.month == (3 + crc % 7) and (s.station_type == "TS" or rng.random() < 0.6):
                d3 = S.pick_bday(rng, d + dt.timedelta(days=1), d + dt.timedelta(days=10))
                if d3 <= W.ASOF:
                    add(d3, "", s.sub_code, "INSP", "", "Annual infrared scan, P&C panels", planned_done(d3, "INSP"),
                        (1.5, 0.3, 0.5))
    # checks after the storms that brought crews out across a region (any day, raised as the calls came in)
    for day, regions in W.STORMS:
        for s in subs.itertuples():
            if cur[s.sub_code] in regions and rng.random() < 0.35:
                d = day + dt.timedelta(days=int(rng.integers(0, 2)))
                add(d, "", s.sub_code, "INSP", "", "Post-storm station check, alarms reviewed and reset",
                    d + dt.timedelta(days=int(rng.random() < 0.15)), (1.0, 0.35, 0.5))

    # settings and firmware modifications, a few held open
    allids = reg["asset_id"].tolist()
    for m in months:
        last = S.month_add(m, 1) - dt.timedelta(days=1)
        for _ in range(int(rng.poisson(58))):
            aid = allids[int(rng.integers(len(allids)))]
            d = S.pick_bday(rng, m, last)
            if d > W.ASOF or not in_service(aid, d):
                continue
            u = rng.random()
            t = ("Settings change per protection coordination study" if u < 0.55 else
                 ("Firmware update to vendor release" if u < 0.8 else "Settings file reissued after feeder reconfiguration"))
            done = planned_done(d, "MOD")
            if u < 0.55 and dt.date(2026, 4, 1) <= d <= dt.date(2026, 8, 31) and rng.random() < 0.02:
                t, done = "Settings change on hold pending revised coordination study", None
            add(d, aid, aid2sub[aid], "MOD", "", t, done, (1.6, 0.4, 0.25))

    # replacements: every retirement is a cutover to the new device in the same bay on the same day
    newdev = {(s, b, d): mo for s, b, d, mo in zip(reg["sub_code"], reg["bay"], reg["install_date"], reg["model"])}
    for a in reg[reg["status"] == "RETIRED"].itertuples():
        d1 = a.retired_date
        nm = newdev.get((a.sub_code, a.bay, d1), a.model)
        if a.sub_code in rebuilt:
            t = "Rebuild cutover %s: %s removed, %s commissioned" % (a.bay, a.model, nm)
            if a.bay == "RTU":
                t += ", SCADA points verified"
        elif a.bay == "RTU":
            t = "RTU replacement: %s removed, %s commissioned, point-to-point test with control room" % (a.model, nm)
        else:
            t = "Replace %s on %s with %s, commissioned and trip tested" % (a.model, a.bay, nm)
        d0 = S.pick_bday(rng, max(GOLIVE, d1 - dt.timedelta(days=21)), d1)
        key = ("R", int(aid2key[a.asset_id])) if a.asset_id in aid2key else None
        add(d0, a.asset_id, a.sub_code, "MOD", "", t, d1, (7.0 if a.bay == "RTU" else 4.5, 0.3, 2.0), key=key)

    # work raised and then cancelled across every type (raised in error, superseded, access refused)
    plain = [k for k, r in enumerate(rows) if r["_key"] is None and r["status"] is None]
    for k in rng.choice(plain, int(len(rows) * 0.012), replace=False):
        r = dict(rows[int(k)])
        r.update(status="CANC", completed_date=None, labour_hours=0.0, _key=None,
                 description=["Raised in error", "Superseded by planned outage work", "No access - rebooked",
                              "Duplicate of earlier work order"][int(rng.integers(4))])
        rows.append(r)

    # status at the extract: open work is in progress; completed work is closed after supervisor review, which takes
    # days to weeks, and a little older work is never closed
    for r in rows:
        if r["status"] == "CANC":
            r["completed_date"] = None
            continue
        done = r["completed_date"]
        if done is None or done > W.ASOF:
            r["status"], r["completed_date"] = "INPRG", None
        elif rng.random() < 0.012:
            r["status"] = "COMP"
        else:
            review = 1 + float(rng.gamma(1.6, 7.0))
            r["status"] = "CLOSE" if done + dt.timedelta(days=review) <= W.ASOF else "COMP"
    wo = pd.DataFrame(rows)
    wo = wo[wo["reported_date"] <= W.ASOF]
    wo = wo.sort_values(["reported_date", "sub_code", "asset_id", "work_type", "status"], kind="mergesort").reset_index(drop=True)
    # EAM work-order numbers run in raise order and are shared with the lines and metering crews
    n, nums = 2104000, []
    for _ in range(len(wo)):
        n += int(rng.geometric(0.28)) + (int(rng.integers(20, 300)) if rng.random() < 0.004 else 0)
        nums.append("WO%07d" % n)
    wo.insert(0, "wo_number", nums)
    keymap = {k: w for k, w in zip(wo["_key"], wo["wo_number"]) if k is not None and not (isinstance(k, float))}
    cols = ["wo_number", "reported_date", "completed_date", "work_type", "status", "asset_id", "sub_code", "region",
            "failed_component", "description", "crew", "labour_hours"]
    return wo[cols], keymap


def module_history(sp, keymap):
    """EAM rotating-item installation history for VPR340-PSU-02: every module in a VPR-340 position since the
    go-live (modules in place at go-live were loaded with the fitted date the legacy system held)"""
    h = sp[(sp["removed"].isna()) | (sp["removed"] >= GOLIVE)].copy()
    h["removal_wo"] = [keymap.get(("F", int(k), int(m)), "") if r == "FAILED" else keymap.get(("R", int(k)), "") if r == "RETIRED"
                       else "" for k, m, r in zip(h["relay_key"], h["module"], h["reason"])]
    h["fitting_wo"] = [keymap.get(("F", int(k), int(m) - 1), "") if (m > 0 and f >= GOLIVE) else "" for k, m, f in
                       zip(h["relay_key"], h["module"], h["fitted"])]
    h["removal_reason"] = [{"FAILED": "FAILED", "RETIRED": "ASSET RETIRED"}.get(r, "") if isinstance(r, str) else "" for r in h["reason"]]
    h["record_source"] = ["GO-LIVE LOAD" if f < GOLIVE else "EAM" for f in h["fitted"]]
    h["item_code"] = "VPR340-PSU-02"
    out = pd.DataFrame(dict(serial_no=h["serial"], item_code=h["item_code"], asset_id=h["asset_id"],
                            fitted_date=h["fitted"], fitting_wo=h["fitting_wo"],
                            removed_date=[None if (r is None or pd.isna(r)) else r for r in h["removed"]],
                            removal_reason=h["removal_reason"], removal_wo=h["removal_wo"],
                            record_source=h["record_source"]))
    return out.sort_values(["asset_id", "fitted_date"], kind="mergesort").reset_index(drop=True)


def stock(n_open):
    """spares on hand at the count, all P&C items; the VPR-340 PSU lines are the ones the buy uses"""
    psu = ("300-14522", "VPR340-PSU-02", "Power supply module, VPR-340, 48-250 V DC")
    rows = [psu + (loc, b, "SERVICEABLE", "EA", q, 1418.40) for loc, b, q in W.SERVICEABLE]
    rows += [psu + (loc, b, "QUARANTINE", "EA", q, 1418.40) for loc, b, q in W.QUARANTINE]
    rows += [psu + ("Veldtek repair centre", "", "AT REPAIR", "EA", n_open, 1418.40)]
    rows += [
        ("300-14523", "VPR340-CPU-01", "Processor card, VPR-340", "Central Stores (Barrie Road)", "A-14-04", "SERVICEABLE", "EA", 6, 2210.00),
        ("300-14524", "VPR340-IO-03", "Input/output card, VPR-340", "Central Stores (Barrie Road)", "A-14-05", "SERVICEABLE", "EA", 9, 865.75),
        ("300-14526", "VPR340-DSP-01", "Front panel display, VPR-340", "North Depot", "N-02-12", "SERVICEABLE", "EA", 4, 640.00),
        ("300-11870", "VPR220-PSU-01", "Power supply module, VPR-220", "Central Stores (Barrie Road)", "A-11-01", "SERVICEABLE", "EA", 12, 905.20),
        ("300-11870", "VPR220-PSU-01", "Power supply module, VPR-220", "Central Stores (Barrie Road)", "Q-01-04", "QUARANTINE", "EA", 2, 905.20),
        ("300-20115", "NX5-PSU", "Power supply, Norland NX-5", "Central Stores (Barrie Road)", "A-20-02", "SERVICEABLE", "EA", 7, 1290.00),
        ("300-20131", "NX9-PSU", "Power supply, Norland NX-9", "North Depot", "N-04-03", "SERVICEABLE", "EA", 5, 1105.00),
        ("300-31007", "AT7-CTRL", "Control module, Arcwell AT-7", "South Depot", "S-01-09", "SERVICEABLE", "EA", 3, 3480.00),
        ("300-26402", "KDR30-PSU", "Power supply, Kestrel KDR-30", "North Depot", "N-03-02", "SERVICEABLE", "EA", 2, 1675.50),
        ("300-31040", "RT400-CPU", "RTU processor, Arcwell RT-400", "Central Stores (Barrie Road)", "A-31-01", "SERVICEABLE", "EA", 2, 4120.00),
    ]
    return pd.DataFrame(rows, columns=["item_no", "item_code", "item_description", "location", "bin", "stock_state", "uom",
                                       "quantity", "unit_cost_cad"])


def rma_log(rng, ships, keymap):
    """Veldtek's RMA register for VPR340-PSU-02 returns from Tarrock (Veldtek's numbering runs across customers)"""
    s = ships.sort_values(["received", "ship"], kind="mergesort").reset_index(drop=True)
    n, nums = 24180, []
    for _ in range(len(s)):
        n += int(rng.integers(6, 41))
        nums.append("RMA-%05d" % n)
    return pd.DataFrame(dict(rma_no=nums, part_no="VPR340-PSU-02", serial_no=s["serial"],
                             customer="Tarrock Hydro Distribution",
                             customer_ref=[keymap[("L", int(k), int(m))] for k, m in zip(s["relay_key"], s["module"])],
                             received=s["received"], result=s["result"], returned=s["returned"]))


def rma_xlsx(path, rma):
    """the register as Veldtek's service centre keeps it in Excel"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "RMA register"
    hdr = ["RMA No.", "Part No.", "Serial No.", "Customer", "Customer Ref.", "Date Received", "Result", "Date Returned"]
    ws.append(hdr)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(horizontal="center", vertical="center")
    for r in rma.itertuples(index=False):
        ws.append([r.rma_no, r.part_no, r.serial_no, r.customer, r.customer_ref, r.received, r.result,
                   r.returned if isinstance(r.returned, dt.date) else None])
    for row in ws.iter_rows(min_row=2):
        for j in (5, 7):
            if row[j].value is not None:
                row[j].number_format = "dd-mmm-yyyy"
    for j, w in enumerate([12, 15, 16, 28, 15, 14, 24, 14], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:H%d" % ws.max_row
    wb.save(path)
