"""The system extracts: the EAM asset register, the PSU rotating-item history, the work-order export,
substations, spares stock and Veldtek's RMA log."""
import datetime as dt
import zlib

import numpy as np
import pandas as pd

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


def _d(rng, y0, y1):
    d = dt.date(int(rng.integers(y0, y1 + 1)), int(rng.integers(1, 13)), int(rng.integers(1, 29)))
    return S.weekday(rng, d, sat=0.0)


def assets(rng, subs, fl, prog):
    """every protection asset at every station since 1988, with its bay, install and retirement dates"""
    rebuilt = dict(zip(prog["sub_code"], prog["retired_on"]))
    camp = fl.groupby("sub_code")["install"].min().to_dict()
    out = []
    for _, s in subs.iterrows():
        sc = s.sub_code
        ts = s.station_type == "TS"
        rb = rebuilt.get(sc)
        mine = fl[fl["sub_code"] == sc]
        for _, r in mine.iterrows():
            out.append(dict(model="VPR-340", sub_code=sc, bay=r.bay, install=r.install, retired=rb, relay_key=r.relay_key))
        nv = len(mine)
        if nv:
            extra = int(rng.integers(1, 5)) if ts else int(rng.integers(0, 3))
            for j in range(extra):
                y0 = max(camp[sc].year + 1, 2011)
                out.append(dict(model="NX-9", sub_code=sc, bay="F%02d" % (nv + j + 1), install=_d(rng, min(y0, 2026), 2026),
                                retired=None, relay_key=None))
            nfeed = nv + extra
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
            out.append(dict(model="NX-5", sub_code=sc, bay="T%d" % t, install=_d(rng, 1995, 2024), retired=rb, relay_key=None))
        for b in range(1, s.n_bus + 1):
            out.append(dict(model="KDR-30", sub_code=sc, bay="B%d" % b, install=_d(rng, 1996, 2022), retired=rb, relay_key=None))
        rtu = _d(rng, 2003, 2016)
        rret = rb
        if rb is None and rng.random() < 0.05:
            rret = _d(rng, 2021, 2025)
            out.append(dict(model="RT-600", sub_code=sc, bay="RTU", install=rret, retired=None, relay_key=None))
        out.append(dict(model="RT-400", sub_code=sc, bay="RTU", install=rtu, retired=rret, relay_key=None))
        if rb is not None:
            # station rebuild: everything retired on the day the new panels go in, new devices registered
            for k in [o for o in out if o["sub_code"] == sc and o["model"] != "VPR-340"]:
                if k["retired"] is None and k["install"] < rb:
                    k["retired"] = rb
            for j in range(nfeed):
                out.append(dict(model="NX-9", sub_code=sc, bay="F%02d" % (j + 1), install=rb, retired=None, relay_key=None))
            for t in range(1, s.n_tx + 1):
                out.append(dict(model="NX-5", sub_code=sc, bay="T%d" % t, install=rb, retired=None, relay_key=None))
            for b in range(1, s.n_bus + 1):
                out.append(dict(model="KDR-30", sub_code=sc, bay="B%d" % b, install=rb, retired=None, relay_key=None))
            out.append(dict(model="RT-600", sub_code=sc, bay="RTU", install=rb, retired=None, relay_key=None))
    a = pd.DataFrame(out)
    a = a[(a["retired"].isna() | (a["retired"] >= GOLIVE)) & (a["install"] <= W.ASOF)].copy()
    return a.reset_index(drop=True)


def register(rng, subs, fl, prog):
    """protection asset register: every asset in service on 1 Jan 2021 or installed since"""
    a = assets(rng, subs, fl, prog)
    leg = dict(zip(subs["sub_code"], subs["legacy_region"]))
    cur = dict(zip(subs["sub_code"], subs["region"]))
    a["loaded"] = a["install"] < GOLIVE
    # EAM asset numbers: the go-live load in location order, then new assets as they were created; other asset
    # classes share the sequence, so protection numbers have gaps
    a["_o"] = [(0, s, b, str(i)) if l else (1, "", "", str(i)) for s, b, i, l in zip(a["sub_code"], a["bay"], a["install"], a["loaded"])]
    a = a.sort_values("_o", key=lambda c: c.map(lambda t: t), kind="mergesort").reset_index(drop=True)
    num, ids = 1000000, []
    for l in a["loaded"]:
        num += int(rng.integers(1, 9)) if l else int(rng.integers(4, 61))
        if not l and num < 1046000:
            num = 1046000 + int(rng.integers(0, 400))
        ids.append("P%07d" % num)
    a["asset_id"] = ids
    # manufacturer serials: year of manufacture and a running number per model
    a["serial_no"] = ""
    for m, g in a.groupby("model"):
        seq = int(rng.integers(100, 3000))
        for i in g.sort_values("install", kind="mergesort").index:
            seq += int(rng.integers(1, 23))
            yy = (a.at[i, "install"].year - int(rng.integers(0, 2))) % 100
            a.at[i, "serial_no"] = SERIAL[m] % (yy, seq)
    a["manufacturer"] = [MODELS[m][0] for m in a["model"]]
    a["function"] = [MODELS[m][1] for m in a["model"]]
    a["status"] = ["RETIRED" if r is not None and not pd.isna(r) else "IN SERVICE" for r in a["retired"]]
    a["region"] = [leg[s] if (l or i < W.REORG) else cur[s] for s, l, i in zip(a["sub_code"], a["loaded"], a["install"])]
    a["install_date"] = a["install"]
    a["retired_date"] = [None if (r is None or pd.isna(r)) else r for r in a["retired"]]
    reg = a.sort_values(["sub_code", "bay", "install_date", "asset_id"], kind="mergesort").reset_index(drop=True)
    cols = ["asset_id", "model", "manufacturer", "function", "sub_code", "bay", "serial_no", "install_date", "status",
            "retired_date", "region"]
    key2aid = {int(k): aid for k, aid in zip(reg["relay_key"], reg["asset_id"]) if k is not None and not pd.isna(k)}
    return reg[cols], key2aid


def psu_cycle(rng, sp, f, key2aid):
    """Module serials for every spell, and the failed modules sent back to Veldtek under RMA: repaired ones come
    back to stores and some are fitted again later."""
    sp = sp.copy()
    sp["serial"] = ""
    seq = {"n": 21000}

    def new_serial(year):
        seq["n"] += int(rng.integers(1, 9))
        return "PS02-%02d-%05d" % (year % 100, seq["n"])

    pool = []                          # (available from, serial)
    ships = []
    fw = f[f["month"] >= GOLIVE].sort_values("reported", kind="mergesort")
    fail_at = {(int(r.relay_key), int(r.module)): r for r in fw.itertuples()}
    order = sp.sort_values("fitted", kind="mergesort").index
    # walk the spells in fitting order; returns become available as their repairs complete
    events = []
    for i in order:
        events.append((sp.at[i, "fitted"], 0, i))
    for r in fw.itertuples():
        events.append((r.done, 1, (int(r.relay_key), int(r.module))))
    events.sort(key=lambda e: (e[0], e[1]))
    serial_of = {}
    for when, kind, ref in events:
        if kind == 0:
            i = ref
            if sp.at[i, "module"] == 0:
                s = new_serial(sp.at[i, "fitted"].year)
            else:
                avail = [p for p in pool if p[0] <= when]
                if when >= GOLIVE and avail and rng.random() < 0.45:
                    pick = min(avail)
                    pool.remove(pick)
                    s = pick[1]
                else:
                    s = new_serial(when.year - int(rng.integers(0, 3)))
            sp.at[i, "serial"] = s
            serial_of[(int(sp.at[i, "relay_key"]), int(sp.at[i, "module"]))] = s
        else:
            r = fail_at[ref]
            s = serial_of[ref]
            ship = S.weekday(rng, r.done + dt.timedelta(days=int(rng.integers(3, 21))), 0)
            if ship > W.ASOF - dt.timedelta(days=12) or rng.random() > 0.55:
                continue
            recv = ship + dt.timedelta(days=int(rng.integers(4, 10)))
            u = rng.random()
            res = "REPAIRED" if u < 0.78 else ("NO FAULT FOUND" if u < 0.82 else "BEYOND ECONOMIC REPAIR")
            back = recv + dt.timedelta(days=int(rng.integers(26, 76)))
            if res == "BEYOND ECONOMIC REPAIR":
                back = None
            elif back > W.ASOF:
                res, back = "OPEN", None
            else:
                pool.append((back + dt.timedelta(days=int(rng.integers(2, 9))), s))
            ships.append(dict(relay_key=ref[0], module=ref[1], serial=s, ship=ship, received=recv, result=res,
                              returned=back))
    sp["asset_id"] = [key2aid[int(k)] for k in sp["relay_key"]]
    return sp, pd.DataFrame(ships), len([p for p in pool])


CREWS_LEGACY = {"Lakeshore": [("Lakeshore P&C 1", 0.6), ("Lakeshore P&C 2", 0.4)], "Ridge": [("Ridge P&C", 1.0)],
                "Valley": [("Valley P&C 1", 0.55), ("Valley P&C 2", 0.45)], "Harbour": [("Harbour P&C", 0.8), ("Harbour Test", 0.2)]}
CREWS_CURRENT = {"North": [("North P&C 1", 0.57), ("North P&C 2", 0.43)],
                 "Central": [("Central P&C 1", 0.42), ("Central P&C 2", 0.36), ("Central P&C 3", 0.22)],
                 "South": [("South P&C 1", 0.52), ("South P&C 2", 0.48)]}
PSU_TEXT = ["Relay dead on arrival, PSU failed. Fitted new module from stores, tested OK",
            "SCADA relay fail alarm. PSU module u/s, replaced and function tested",
            "Power supply failure, relay out of service. PSU swapped, settings verified",
            "No front panel, no healthy LED. Replaced PSU module, relay back in service",
            "Watchdog alarm traced to power supply. PSU replaced, trip test OK",
            "Relay rebooting intermittently, PSU output low on test. Module replaced",
            "Healthy LED off after storm. PSU failed - replaced from %s stores",
            "PSU fail alarm %s. Module changed, event records downloaded",
            "Relay unresponsive, DC supply OK at terminals. PSU module replaced",
            "Burnt smell at panel, PSU module failed. Replaced and panel cleaned"]
CM_TEXT = {"CPU": ["Processor card fault, card replaced", "CPU self-test failure, replaced processor card",
                   "Relay locked up, processor card swapped and settings reloaded"],
           "IO": ["Input card failed self-test, replaced", "Binary input chatter, IO card replaced",
                  "Output contact welded, IO card replaced"],
           "DISP": ["Display blank, front panel replaced", "Keypad unresponsive, front panel module changed"],
           "COMMS": ["Lost SCADA comms to relay, comms card replaced", "DNP3 link down, comms card reset then replaced",
                     "Fibre transceiver on comms card failed, card replaced"],
           "PSU": ["Power supply failed, replaced from stores", "PSU fault alarm, module replaced and tested"]}
OTHER_TEXT = ["Fault found and repaired", "Replaced failed card, tested OK", "Reset and tested, fault cleared",
              "Alarm investigated, loose wiring retightened", "Firmware lock-up, power cycled and monitored",
              "Card replaced under warranty", "Spurious alarm, no fault found", "Contact output replaced, trip tested"]


def _crew(rng, region_pool):
    names = [c for c, _ in region_pool]
    w = np.array([p for _, p in region_pool])
    return names[int(rng.choice(len(names), p=w / w.sum()))]


def _hours(rng, mu, sd, lo=0.25):
    h = float(np.exp(rng.normal(np.log(mu), sd)))
    return max(lo, round(h * 4) / 4)


def work_orders(rng, subs, reg, f, sp, ships):
    cur = dict(zip(subs["sub_code"], subs["region"]))
    leg = dict(zip(subs["sub_code"], subs["legacy_region"]))
    names = dict(zip(subs["sub_code"], subs["sub_name"]))
    kind = dict(zip(subs["sub_code"], subs["station_type"]))
    aid2sub = dict(zip(reg["asset_id"], reg["sub_code"]))
    aid2bay = dict(zip(reg["asset_id"], reg["bay"]))
    inst = dict(zip(reg["asset_id"], reg["install_date"]))
    retd = dict(zip(reg["asset_id"], reg["retired_date"]))
    key2aid = dict(zip(sp["relay_key"], sp["asset_id"]))
    rows = []

    def in_service(aid, d):
        r = retd.get(aid)
        return inst[aid] <= d and (r is None or (isinstance(r, float)) or d < r)

    def crew(sub, d):
        pool = CREWS_CURRENT[cur[sub]] if d >= W.REORG else CREWS_LEGACY[leg[sub]]
        return _crew(rng, pool)

    def add(d, aid, sub, wt, st, comp, desc, hrs, done=None, key=None):
        if done is None and st not in ("CANC",):
            lag = int(rng.integers(0, 4)) if wt in ("INSP", "MOD", "LOG") else int(rng.integers(0, 9))
            done = min(d + dt.timedelta(days=lag), W.ASOF)
        if st == "CANC":
            done = None
        rows.append(dict(reported_date=d, asset_id=aid, sub_code=sub, work_type=wt, status=st,
                         failed_component=comp, description=desc, labour_hours=hrs, completed_date=done,
                         crew=crew(sub, d), region=cur[sub] if d >= W.REORG else leg[sub], _key=key))

    def status_for(d):
        return "CLOSE" if d < dt.date(2026, 6, 1) or rng.random() < 0.35 else "COMP"

    # PSU failures on the VPR-340 fleet as recorded from the go-live
    fw = f[f["month"] >= GOLIVE].sort_values("reported", kind="mergesort")
    for r in fw.itertuples():
        aid = key2aid[r.relay_key]
        sub = aid2sub[aid]
        t = PSU_TEXT[int(rng.integers(len(PSU_TEXT)))]
        if "%s" in t:
            t = t % (names[sub] if "stores" not in t else ["Central", "North", "South", "depot"][int(rng.integers(4))])
        wt = "EM" if r.em else "CM"
        add(r.reported, aid, sub, wt, status_for(r.reported), "PSU", t, _hours(rng, 3.2, 0.35, 1.0), done=r.done,
            key=("F", int(r.relay_key), int(r.module)))
        if rng.random() < 0.045:
            add(r.reported, aid, sub, wt, "CANC", "PSU", "Duplicate - raised twice from SCADA alarm", 0.0)
    for s in ships.itertuples():
        aid = key2aid[s.relay_key]
        add(s.ship, aid, aid2sub[aid], "LOG", status_for(s.ship), "PSU",
            ["Ship failed PSU s/n %s to Veldtek, RMA requested", "Return PSU %s to Veldtek repair centre",
             "Courier failed module %s to Veldtek under RMA"][int(rng.integers(3))] % s.serial,
            [0.25, 0.5, 0.5, 0.75, 1.0][int(rng.integers(5))], key=("L", int(s.relay_key), int(s.module)))
    months = S.months_between(GOLIVE, END)
    # other VPR-340 corrective faults
    vp = reg[reg["model"] == "VPR-340"]["asset_id"].tolist()
    for m in months:
        for _ in range(int(rng.poisson(2.4))):
            aid = vp[int(rng.integers(len(vp)))]
            d = dt.date(m.year, m.month, int(rng.integers(1, 29)))
            if d > W.ASOF or not in_service(aid, d):
                continue
            comp = ["CPU", "IO", "DISP", "COMMS"][int(rng.choice(4, p=[0.2, 0.35, 0.2, 0.25]))]
            add(d, aid, aid2sub[aid], "CM", status_for(d), comp, CM_TEXT[comp][int(rng.integers(len(CM_TEXT[comp])))],
                _hours(rng, 2.5, 0.45))
    # corrective work on other models, with their own module returns
    others = reg[reg["model"] != "VPR-340"]["asset_id"].tolist()
    for m in months:
        for _ in range(int(rng.poisson(40))):
            aid = others[int(rng.integers(len(others)))]
            d = dt.date(m.year, m.month, int(rng.integers(1, 29)))
            if d > W.ASOF or not in_service(aid, d):
                continue
            comp = ["PSU", "CPU", "IO", "DISP", "COMMS"][int(rng.choice(5, p=[0.18, 0.17, 0.3, 0.12, 0.23]))]
            add(d, aid, aid2sub[aid], "CM" if rng.random() < 0.82 else "EM", status_for(d), comp,
                OTHER_TEXT[int(rng.integers(len(OTHER_TEXT)))], _hours(rng, 2.8, 0.5))
            if rng.random() < 0.22:
                d2 = S.weekday(rng, d + dt.timedelta(days=int(rng.integers(3, 26))), 0)
                if d2 <= W.ASOF:
                    add(d2, aid, aid2sub[aid], "LOG", status_for(d2), comp,
                        ["Return failed module to supplier", "Ship card to vendor for repair", "RMA return to manufacturer"][int(rng.integers(3))],
                        [0.25, 0.5, 0.75, 1.0][int(rng.integers(4))])
    # periodic relay tests: two-yearly at transformer stations, three-yearly at distribution stations
    for a in reg.itertuples():
        cyc = 730 if kind[a.sub_code] == "TS" else 1095
        d = GOLIVE + dt.timedelta(days=int(rng.integers(0, cyc)))
        end = a.retired_date if isinstance(a.retired_date, dt.date) else END
        while d < end and d <= W.ASOF:
            dd = S.weekday(rng, d, 0.03)
            if dd >= a.install_date and dd < end and dd <= W.ASOF:
                add(dd, a.asset_id, a.sub_code, "PM", status_for(dd), "",
                    ["Routine relay test to P&C std 3.2 - %s", "%s relay test, settings and trip check",
                     "Maintenance test %s, secondary injection", "Periodic test %s per P&C std 3.2"][int(rng.integers(4))] % a.bay,
                    _hours(rng, 4.5 if a.model in ("NX-5", "KDR-30") else 3.5, 0.3, 1.0))
            d = d + dt.timedelta(days=int(cyc + rng.integers(-45, 46)))
    # station inspections: monthly (a few missed or late), quarterly DC checks, yearly thermal scans
    for s in subs.itertuples():
        for m in months:
            if rng.random() < 0.025:
                continue
            d = S.weekday(rng, dt.date(m.year, m.month, int(rng.integers(1, 26))), 0.02)
            if d > W.ASOF:
                continue
            add(d, "", s.sub_code, "INSP", status_for(d), "",
                ["Monthly station inspection", "Monthly inspection - no defects", "Monthly P&C panel walkdown",
                 "Monthly insp, annunciator test OK"][int(rng.choice(4, p=[0.55, 0.2, 0.15, 0.1]))],
                [0.5, 1.0, 1.0, 1.5, 2.0][int(rng.integers(5))])
            if s.station_type == "TS":
                # transformer stations get a second, mid-month walkdown
                d4 = S.weekday(rng, d + dt.timedelta(days=int(rng.integers(12, 17))), 0.02)
                if d4 <= W.ASOF and rng.random() < 0.93:
                    add(d4, "", s.sub_code, "INSP", status_for(d4), "", "TS walkdown, alarms and panel lamps checked",
                        [0.5, 0.75, 1.0, 1.0][int(rng.integers(4))])
            if m.month in (1, 4, 7, 10) and rng.random() < 0.96:
                d2 = S.weekday(rng, d + dt.timedelta(days=int(rng.integers(0, 6))), 0)
                if d2 <= W.ASOF:
                    add(d2, "", s.sub_code, "INSP", status_for(d2), "", "Quarterly DC battery and charger check",
                        [1.0, 1.5, 1.5, 2.0, 2.5][int(rng.integers(5))])
            if m.month == (3 + zlib.crc32(s.sub_code.encode()) % 7) and (s.station_type == "TS" or rng.random() < 0.6):
                d3 = S.weekday(rng, d + dt.timedelta(days=int(rng.integers(1, 10))), 0)
                if d3 <= W.ASOF:
                    add(d3, "", s.sub_code, "INSP", status_for(d3), "", "Annual infrared scan, P&C panels",
                        [1.5, 2.0, 2.5, 3.0][int(rng.integers(4))])
    # settings and firmware modifications
    allids = reg["asset_id"].tolist()
    for m in months:
        for _ in range(int(rng.poisson(50))):
            aid = allids[int(rng.integers(len(allids)))]
            d = S.weekday(rng, dt.date(m.year, m.month, int(rng.integers(1, 29))), 0.02)
            if d > W.ASOF or not in_service(aid, d):
                continue
            u = rng.random()
            add(d, aid, aid2sub[aid], "MOD", status_for(d), "",
                "Settings change per protection coordination study" if u < 0.55 else
                ("Firmware update to vendor release" if u < 0.8 else "Settings file reissued after feeder reconfiguration"),
                _hours(rng, 2.0, 0.4))
    # work raised and then cancelled across every type (raised in error, superseded, access refused)
    n_canc = int(len(rows) * 0.012)
    pick = rng.choice(len(rows), n_canc, replace=False)
    for k in pick:
        r = dict(rows[int(k)])
        if r["work_type"] in ("CM", "EM", "LOG") and r["failed_component"] == "PSU" and r["asset_id"] in set(vp):
            continue
        r.update(status="CANC", completed_date=None, labour_hours=0.0, _key=None,
                 description=["Raised in error", "Superseded by planned outage work", "No access - rebooked",
                              "Duplicate of earlier work order"][int(rng.integers(4))])
        rows.append(r)
    wo = pd.DataFrame(rows)
    wo = wo[wo["reported_date"] <= W.ASOF]
    wo = wo.sort_values(["reported_date", "sub_code", "asset_id", "work_type", "status"], kind="mergesort").reset_index(drop=True)
    # EAM work-order numbers run in raise order and are shared with the lines and metering crews
    n, nums = 2104000, []
    for _ in range(len(wo)):
        n += int(rng.geometric(0.28)) + (int(rng.integers(20, 300)) if rng.random() < 0.004 else 0)
        nums.append("WO%07d" % n)
    wo.insert(0, "wo_number", nums)
    late = (wo["reported_date"] > dt.date(2026, 9, 18)) & (wo["status"] == "COMP")
    keep = ~(wo["work_type"].isin(["CM", "EM"]) & (wo["failed_component"] == "PSU") & wo["asset_id"].isin(set(vp)))
    flip = late & keep & (pd.Series(rng.random(len(wo))) < 0.45)
    wo.loc[flip, "status"] = "INPRG"
    wo.loc[wo["status"] == "INPRG", "completed_date"] = None
    keymap = {k: w for k, w in zip(wo["_key"], wo["wo_number"]) if k is not None and not (isinstance(k, float))}
    cols = ["wo_number", "reported_date", "completed_date", "work_type", "status", "asset_id", "sub_code", "region",
            "failed_component", "description", "crew", "labour_hours"]
    return wo[cols], keymap


def module_history(sp, keymap):
    """EAM rotating-item installation history for VPR340-PSU-02: every module in a VPR-340 position since the
    go-live (modules in place at go-live were loaded with the fitted date the legacy system held)"""
    h = sp[(sp["removed"].isna()) | (sp["removed"] >= GOLIVE)].copy()
    h["removal_wo"] = [keymap.get(("F", int(k), int(m)), "") if r == "FAILED" else "" for k, m, r in
                       zip(h["relay_key"], h["module"], h["reason"])]
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
    """Veldtek's RMA register for VPR340-PSU-02 returns from Ironwood (Veldtek's numbering runs across customers)"""
    s = ships.sort_values("received", kind="mergesort").reset_index(drop=True)
    n, nums = 24180, []
    for _ in range(len(s)):
        n += int(rng.integers(6, 41))
        nums.append("RMA-%05d" % n)
    return pd.DataFrame(dict(rma_no=nums, part_no="VPR340-PSU-02", serial_no=s["serial"],
                             customer="Ironwood Hydro Distribution",
                             customer_ref=[keymap[("L", int(k), int(m))] for k, m in zip(s["relay_key"], s["module"])],
                             received=s["received"], result=s["result"], returned=s["returned"]))
