"""The system extracts: the EAM asset register and work-order export, substations, spares stock, RMA log."""
import datetime as dt
import zlib

import numpy as np
import pandas as pd

import sim as S
import world as W

OTHER_MODELS = [
    ("VPR-220", "Veldtek Protection Systems", "Feeder protection"),
    ("NX-5", "Norland Controls", "Transformer differential"),
    ("KDR-30", "Kestrel Grid Devices", "Bus protection"),
    ("AT-7", "Arcwell Automation", "Recloser control"),
    ("NX-9", "Norland Controls", "Feeder protection"),
    ("RT-400", "Arcwell Automation", "Substation RTU"),
]
COMPONENTS = ["CPU", "IO", "DISP", "COMMS"]
REORG = dt.date(2024, 4, 1)


def _aid(rng, n, used):
    out = []
    while len(out) < n:
        a = "P%07d" % int(rng.integers(1000000, 9999999))
        if a not in used:
            used.add(a)
            out.append(a)
    return out


def register(rng, subs, fl, prog):
    """protection asset register: every asset in service on 1 Jan 2021 or installed later"""
    used = set()
    ret = dict(zip(prog["sub_code"], prog["retired_on"]))
    legacy = dict(zip(subs["sub_code"], subs["legacy_region"]))
    ids = _aid(rng, len(fl), used)
    fl = fl.copy()
    fl["asset_id"] = ids
    rows = []
    for _, r in fl.iterrows():
        rd = ret.get(r.sub_code)
        rows.append(dict(asset_id=r.asset_id, model="VPR-340", manufacturer="Veldtek Protection Systems",
                         function="Feeder protection", sub_code=r.sub_code,
                         bay="F%02d" % int(rng.integers(1, 17)), serial_no="VT340-%06d" % int(rng.integers(100000, 999999)),
                         install_date=r.install, status="RETIRED" if rd else "IN SERVICE",
                         retired_date=rd if rd else None, region=legacy[r.sub_code]))
    oth = []
    oids = _aid(rng, W.N_OTHER, used)
    for k in range(W.N_OTHER):
        mdl, man, fn = OTHER_MODELS[int(rng.integers(len(OTHER_MODELS)))]
        s = subs.iloc[int(rng.integers(len(subs)))]
        y = int(rng.integers(1990, 2026))
        inst = dt.date(y, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
        retd = None
        if rng.random() < 0.06:
            retd = dt.date(int(rng.integers(max(2021, y + 1), 2027)) if y < 2026 else 2026, int(rng.integers(1, 10)), 1)
            if retd <= inst or retd > W.ASOF:
                retd = None
        oth.append(dict(asset_id=oids[k], model=mdl, manufacturer=man, function=fn, sub_code=s.sub_code,
                        bay=("T%d" % int(rng.integers(1, 4))) if "Transformer" in fn else "F%02d" % int(rng.integers(1, 17)),
                        serial_no="%s-%06d" % (mdl.replace("-", ""), int(rng.integers(100000, 999999))),
                        install_date=inst, status="RETIRED" if retd else "IN SERVICE", retired_date=retd,
                        region=legacy[s.sub_code]))
    reg = pd.DataFrame(rows + oth)
    reg = reg.sort_values(["sub_code", "bay", "asset_id"], kind="mergesort").reset_index(drop=True)
    return reg, fl


def _region_at(subs_cur, subs_leg, sub, d):
    return subs_cur[sub] if d >= REORG else subs_leg[sub]


CREWS_LEGACY = {"Lakeshore": ["Lakeshore P&C 1", "Lakeshore P&C 2"], "Ridge": ["Ridge P&C"],
                "Valley": ["Valley P&C 1", "Valley P&C 2"], "Harbour": ["Harbour P&C"]}
CREWS_CURRENT = {"North": ["North P&C 1", "North P&C 2"], "Central": ["Central P&C 1", "Central P&C 2", "Central P&C 3"],
                 "South": ["South P&C 1", "South P&C 2"]}


def work_orders(rng, subs, reg, fl, fails):
    cur = dict(zip(subs["sub_code"], subs["region"]))
    leg = dict(zip(subs["sub_code"], subs["legacy_region"]))
    key2aid = dict(zip(fl["relay_key"], fl["asset_id"]))
    aid2sub = dict(zip(reg["asset_id"], reg["sub_code"]))
    inst = dict(zip(reg["asset_id"], reg["install_date"]))
    retd = dict(zip(reg["asset_id"], reg["retired_date"]))
    end_all = dt.date(2026, 10, 1)
    rows = []

    def in_service(aid, d):
        r = retd.get(aid)
        return inst[aid] <= d and (r is None or (isinstance(r, float)) or d < r)

    def crew(sub, d):
        pool = CREWS_CURRENT[cur[sub]] if d >= REORG else CREWS_LEGACY[leg[sub]]
        return pool[int(rng.integers(len(pool)))]

    def add(d, aid, sub, wt, st, comp, desc, hrs):
        done = None
        if st not in ("CANC",):
            done = min(d + dt.timedelta(days=int(rng.integers(0, 7))), W.ASOF)
        rows.append(dict(reported_date=d, asset_id=aid, sub_code=sub, work_type=wt, status=st,
                         failed_component=comp, description=desc, labour_hours=hrs, completed_date=done,
                         crew=crew(sub, d), region=_region_at(cur, leg, sub, d)))

    def status_for(d):
        return "CLOSE" if d < dt.date(2026, 6, 1) or rng.random() < 0.35 else "COMP"

    # PSU failures on the VPR-340 fleet, as recorded from the migration on
    fw = fails[fails["month"] >= W.MIGRATION].sort_values("date", kind="mergesort")
    texts = ["Relay dead, PSU failed, replaced module", "PSU fail - relay out of service, module swapped",
             "Power supply failure alarm, replaced PSU", "No front panel, PSU replaced from stores",
             "Relay healthy LED off. PSU changed", "Watchdog alarm, traced to power supply, replaced"]
    for _, f in fw.iterrows():
        aid = key2aid[f.relay_key]
        sub = aid2sub[aid]
        wt = "EM" if rng.random() < 0.3 else "CM"
        add(f.date, aid, sub, wt, status_for(f.date), "PSU", texts[int(rng.integers(len(texts)))],
            round(float(rng.uniform(2, 7)), 1))
        if rng.random() < 0.045:
            add(f.date, aid, sub, wt, "CANC", "PSU", "Duplicate - raised twice from SCADA alarm", 0.0)
        if rng.random() < 0.35:
            d2 = f.date + dt.timedelta(days=int(rng.integers(2, 20)))
            add(d2, aid, sub, "LOG", "COMP" if d2 > dt.date(2026, 6, 1) else "CLOSE", "PSU",
                "Ship failed PSU module to Veldtek under RMA", round(float(rng.choice([0.3, 0.5, 0.5, 0.8, 1.0])), 1))
    # other VPR-340 corrective faults
    vp = fl["asset_id"].tolist()
    months = S.months_between(W.MIGRATION, end_all)
    for m in months:
        for _ in range(int(rng.poisson(2.2))):
            aid = vp[int(rng.integers(len(vp)))]
            d = dt.date(m.year, m.month, int(rng.integers(1, 29)))
            if d > W.ASOF or not in_service(aid, d):
                continue
            add(d, aid, aid2sub[aid], "CM", status_for(d), COMPONENTS[int(rng.integers(4))],
                ["Card fault, replaced", "IO card failed self-test, replaced", "Display blank, replaced",
                 "Comms card replaced, SCADA restored"][int(rng.integers(4))], round(float(rng.uniform(1, 5)), 1))
    # corrective work on other models, with their own module returns
    others = reg[reg["model"] != "VPR-340"]["asset_id"].tolist()
    for m in months:
        for _ in range(int(rng.poisson(26))):
            aid = others[int(rng.integers(len(others)))]
            d = dt.date(m.year, m.month, int(rng.integers(1, 29)))
            if d > W.ASOF or not in_service(aid, d):
                continue
            comp = ["PSU", "CPU", "IO", "DISP", "COMMS"][int(rng.integers(5))]
            add(d, aid, aid2sub[aid], "CM" if rng.random() < 0.8 else "EM", status_for(d), comp,
                ["Fault found and repaired", "Module replaced from stores", "Reset and tested, fault cleared",
                 "Replaced failed card"][int(rng.integers(4))], round(float(rng.uniform(1, 6)), 1))
            if rng.random() < 0.25:
                d2 = d + dt.timedelta(days=int(rng.integers(2, 25)))
                if d2 <= W.ASOF:
                    add(d2, aid, aid2sub[aid], "LOG", status_for(d2), comp, "Return failed module to supplier",
                        round(float(rng.choice([0.3, 0.5, 0.8, 1.0, 1.5])), 1))
    # periodic maintenance tests, every three years per asset
    for _, a in reg.iterrows():
        d = W.MIGRATION + dt.timedelta(days=int(rng.integers(0, 1095)))
        end = a.retired_date or end_all
        while d < end and d <= W.ASOF:
            if d >= a.install_date:
                add(d, a.asset_id, a.sub_code, "PM", status_for(d), "",
                    "Routine relay test to P&C standard 3.2", round(float(rng.uniform(3, 9)), 1))
            d = d + dt.timedelta(days=int(1095 + rng.integers(-60, 61)))
    # substation panel inspections, monthly (a few missed), and quarterly battery checks (no asset)
    for _, s in subs.iterrows():
        for m in months:
            if rng.random() < 0.03:
                continue
            d = dt.date(m.year, m.month, int(rng.integers(1, 29)))
            if d > W.ASOF:
                continue
            add(d, "", s.sub_code, "INSP", status_for(d), "", "Monthly protection panel inspection",
                round(float(rng.choice([0.5, 1.0, 1.0, 1.5, 2.0])), 1))
            if m.month in (1, 4, 7, 10) and rng.random() < 0.95:
                d2 = min(d + dt.timedelta(days=int(rng.integers(0, 4))), W.ASOF)
                add(d2, "", s.sub_code, "INSP", status_for(d2), "", "Quarterly DC battery and charger check",
                    round(float(rng.choice([1.0, 1.5, 1.5, 2.0])), 1))
    # settings and firmware modifications
    for m in months:
        for _ in range(int(rng.poisson(30))):
            aid = reg["asset_id"].iloc[int(rng.integers(len(reg)))]
            d = dt.date(m.year, m.month, int(rng.integers(1, 29)))
            if d > W.ASOF or not in_service(aid, d):
                continue
            add(d, aid, aid2sub[aid], "MOD", status_for(d), "",
                "Settings change per protection coordination study" if rng.random() < 0.7 else "Firmware update",
                round(float(rng.uniform(1, 4)), 1))
    # work raised and then cancelled across every type (raised in error, superseded, access refused)
    n_canc = int(len(rows) * 0.012)
    pick = rng.choice(len(rows), n_canc, replace=False)
    for k in pick:
        r = dict(rows[int(k)])
        if r["work_type"] in ("CM", "EM") and r["failed_component"] == "PSU" and r["asset_id"] in set(vp):
            continue
        r["status"] = "CANC"
        r["completed_date"] = None
        r["labour_hours"] = 0.0
        r["description"] = ["Raised in error", "Superseded by planned outage work", "No access - rebooked",
                            "Duplicate of earlier work order"][int(rng.integers(4))]
        rows.append(r)
    wo = pd.DataFrame(rows)
    wo = wo[wo["reported_date"] <= W.ASOF]
    wo = wo.sort_values(["reported_date", "sub_code", "asset_id", "work_type", "status"], kind="mergesort").reset_index(drop=True)
    wo.insert(0, "wo_number", ["WO%07d" % (2100000 + i * 3 + int(zlib.crc32(str(i).encode()) % 3)) for i in range(len(wo))])
    late = wo["reported_date"] > dt.date(2026, 9, 20)
    wo.loc[late & (wo["status"] == "COMP") & (np.arange(len(wo)) % 3 == 0), "status"] = "INPRG"
    wo.loc[wo["status"] == "INPRG", "completed_date"] = None
    cols = ["wo_number", "reported_date", "completed_date", "work_type", "status", "asset_id", "sub_code", "region",
            "failed_component", "description", "crew", "labour_hours"]
    return wo[cols]


def stock():
    """spares on hand at the count, all P&C items; the VPR-340 PSU lines are the ones the buy uses"""
    rows = [
        ("VPR340-PSU-02", "Power supply module, VPR-340", "Central Stores (Barrie Road)", "SERVICEABLE", 10),
        ("VPR340-PSU-02", "Power supply module, VPR-340", "North Depot", "SERVICEABLE", 8),
        ("VPR340-PSU-02", "Power supply module, VPR-340", "South Depot", "SERVICEABLE", 5),
        ("VPR340-PSU-02", "Power supply module, VPR-340", "Central Stores (Barrie Road)", "QUARANTINE", 4),
        ("VPR340-PSU-02", "Power supply module, VPR-340", "South Depot", "QUARANTINE", 3),
        ("VPR340-PSU-02", "Power supply module, VPR-340", "Veldtek repair centre", "AT REPAIR", 11),
        ("VPR340-CPU-01", "Processor card, VPR-340", "Central Stores (Barrie Road)", "SERVICEABLE", 6),
        ("VPR340-IO-03", "Input/output card, VPR-340", "Central Stores (Barrie Road)", "SERVICEABLE", 9),
        ("VPR340-DSP-01", "Front panel display, VPR-340", "North Depot", "SERVICEABLE", 4),
        ("VPR220-PSU-01", "Power supply module, VPR-220", "Central Stores (Barrie Road)", "SERVICEABLE", 12),
        ("NX5-PSU", "Power supply, Norland NX-5", "Central Stores (Barrie Road)", "SERVICEABLE", 7),
        ("AT7-CTRL", "Control module, Arcwell AT-7", "South Depot", "SERVICEABLE", 3),
        ("KDR30-PSU", "Power supply, Kestrel KDR-30", "North Depot", "SERVICEABLE", 2),
    ]
    return pd.DataFrame(rows, columns=["item_code", "item_description", "location", "stock_state", "quantity"])


def rma_log(rng, wo):
    """Veldtek RMA returns for VPR-340 PSU modules: a vendor log, not the failure record"""
    ship = wo[(wo["work_type"] == "LOG") & (wo["failed_component"] == "PSU")]
    rows = []
    for i, (_, r) in enumerate(ship.iterrows()):
        recv = r.reported_date + dt.timedelta(days=int(rng.integers(5, 15)))
        res = "REPAIRED" if rng.random() < 0.84 else "BEYOND ECONOMIC REPAIR"
        back = recv + dt.timedelta(days=int(rng.integers(20, 60)))
        if back > W.ASOF:
            res, back = "OPEN", None
        rows.append(dict(rma_no="RMA-%05d" % (31000 + i), part_no="VPR340-PSU-02", customer_ref=r.wo_number,
                         received=recv, result=res, returned=back))
    df = pd.DataFrame(rows)
    return df[df["received"] <= W.ASOF]
