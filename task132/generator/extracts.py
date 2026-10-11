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
CREWS = ["P&C North 1", "P&C North 2", "P&C Central 1", "P&C Central 2", "P&C Central 3", "P&C South 1", "P&C South 2"]
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


def work_orders(rng, subs, reg, fl, fails):
    cur = dict(zip(subs["sub_code"], subs["region"]))
    leg = dict(zip(subs["sub_code"], subs["legacy_region"]))
    key2aid = dict(zip(fl["relay_key"], fl["asset_id"]))
    aid2sub = dict(zip(reg["asset_id"], reg["sub_code"]))
    live = reg.copy()
    rows = []

    def add(d, aid, sub, wt, st, comp, desc, hrs, done=None):
        rows.append(dict(reported_date=d, asset_id=aid, sub_code=sub, work_type=wt, status=st,
                         failed_component=comp, description=desc, labour_hours=hrs,
                         completed_date=done if done is not None else (min(d + dt.timedelta(days=int(rng.integers(0, 7))), W.ASOF) if st != "CANC" else None),
                         crew=CREWS[int(rng.integers(len(CREWS)))], region=_region_at(cur, leg, sub, d)))

    # PSU failures on the VPR-340 fleet, as recorded from the migration on
    fw = fails[fails["month"] >= W.MIGRATION].sort_values("date", kind="mergesort")
    texts = ["Relay dead, PSU failed, replaced module", "PSU fail - relay out of service, module swapped",
             "Power supply failure alarm, replaced PSU", "No front panel, PSU replaced from stores",
             "Relay healthy LED off. PSU changed", "Watchdog alarm, traced to power supply, replaced"]
    for _, f in fw.iterrows():
        aid = key2aid[f.relay_key]
        sub = aid2sub[aid]
        wt = "EM" if rng.random() < 0.3 else "CM"
        st = "CLOSE" if f.date < dt.date(2026, 6, 1) or rng.random() < 0.4 else "COMP"
        add(f.date, aid, sub, wt, st, "PSU", texts[int(rng.integers(len(texts)))], round(float(rng.uniform(2, 7)), 1))
        if rng.random() < 0.045:
            add(f.date, aid, sub, wt, "CANC", "PSU", "Duplicate - raised twice from SCADA alarm", 0.0)
        if rng.random() < 0.35:
            add(f.date + dt.timedelta(days=int(rng.integers(2, 20))), aid, sub, "LOG", "COMP", "PSU",
                "Ship failed PSU module to Veldtek under RMA", 0.5)
    # other VPR-340 corrective faults
    vp = fl["asset_id"].tolist()
    for m in S.months_between(W.MIGRATION, dt.date(2026, 10, 1)):
        for _ in range(int(rng.poisson(2.2))):
            aid = vp[int(rng.integers(len(vp)))]
            d = dt.date(m.year, m.month, int(rng.integers(1, 29)))
            add(d, aid, aid2sub[aid], "CM", "CLOSE" if d < dt.date(2026, 6, 1) else "COMP",
                COMPONENTS[int(rng.integers(4))], "Card fault, replaced", round(float(rng.uniform(1, 5)), 1))
    # corrective work on other models
    others = reg[reg["model"] != "VPR-340"]["asset_id"].tolist()
    for m in S.months_between(W.MIGRATION, dt.date(2026, 10, 1)):
        for _ in range(int(rng.poisson(26))):
            aid = others[int(rng.integers(len(others)))]
            d = dt.date(m.year, m.month, int(rng.integers(1, 29)))
            add(d, aid, aid2sub[aid], "CM" if rng.random() < 0.8 else "EM",
                "CLOSE" if d < dt.date(2026, 6, 1) else "COMP",
                ["PSU", "CPU", "IO", "DISP", "COMMS"][int(rng.integers(5))], "Fault found and repaired",
                round(float(rng.uniform(1, 6)), 1))
    # periodic maintenance tests, every three years per asset
    for _, a in reg.iterrows():
        first = W.MIGRATION + dt.timedelta(days=int(rng.integers(0, 1095)))
        d = first
        end = a.retired_date or dt.date(2026, 10, 1)
        while d < end and d < dt.date(2026, 10, 1):
            if d >= a.install_date:
                add(d, a.asset_id, a.sub_code, "PM", "CLOSE" if d < dt.date(2026, 6, 1) else "COMP", "",
                    "Routine relay test to P&C standard 3.2", round(float(rng.uniform(3, 9)), 1))
            d = d + dt.timedelta(days=int(1095 + rng.integers(-40, 41)))
    # substation panel inspections, monthly, and quarterly battery checks (no asset)
    for _, s in subs.iterrows():
        for m in S.months_between(W.MIGRATION, dt.date(2026, 10, 1)):
            d = dt.date(m.year, m.month, int(rng.integers(1, 29)))
            add(d, "", s.sub_code, "INSP", "CLOSE" if d < dt.date(2026, 6, 1) else "COMP", "",
                "Monthly protection panel inspection", 1.0)
            if m.month in (1, 4, 7, 10):
                add(d + dt.timedelta(days=1), "", s.sub_code, "INSP", "CLOSE" if d < dt.date(2026, 6, 1) else "COMP",
                    "", "Quarterly DC battery and charger check", 1.5)
    # settings and firmware modifications
    for m in S.months_between(W.MIGRATION, dt.date(2026, 10, 1)):
        for _ in range(int(rng.poisson(30))):
            aid = reg["asset_id"].iloc[int(rng.integers(len(reg)))]
            d = dt.date(m.year, m.month, int(rng.integers(1, 29)))
            add(d, aid, aid2sub[aid], "MOD", "CLOSE" if d < dt.date(2026, 6, 1) else "COMP", "",
                "Settings change per protection coordination study" if rng.random() < 0.7 else "Firmware update",
                round(float(rng.uniform(1, 4)), 1))
    wo = pd.DataFrame(rows)
    wo = wo[wo["reported_date"] <= W.ASOF]
    wo = wo.sort_values(["reported_date", "sub_code", "asset_id", "work_type"], kind="mergesort").reset_index(drop=True)
    wo.insert(0, "wo_number", ["WO%07d" % (2100000 + i * 3 + int(zlib.crc32(str(i).encode()) % 3)) for i in range(len(wo))])
    # a work order not yet completed carries no completion date
    late = wo["reported_date"] > dt.date(2026, 9, 20)
    wo.loc[late & (wo["status"] == "COMP") & (np.arange(len(wo)) % 3 == 0), "status"] = "INPRG"
    wo.loc[wo["status"] == "INPRG", "completed_date"] = None
    cols = ["wo_number", "reported_date", "completed_date", "work_type", "status", "asset_id", "sub_code", "region",
            "failed_component", "description", "crew", "labour_hours"]
    return wo[cols]


def stock():
    """spares on hand at the count, all P&C items; the VPR-340 PSU lines are the ones the buy uses"""
    rows = [
        ("VPR340-PSU-02", "Power supply module, VPR-340", "Central Stores (Barrie Road)", "SERVICEABLE", 17),
        ("VPR340-PSU-02", "Power supply module, VPR-340", "North Depot", "SERVICEABLE", 11),
        ("VPR340-PSU-02", "Power supply module, VPR-340", "South Depot", "SERVICEABLE", 8),
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
