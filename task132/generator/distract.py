"""Files a protection team keeps that look relevant to the buy and do not size it."""
import datetime as dt

import numpy as np
import openpyxl
import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill

import world as W

Y0, Y1 = dt.date(2025, 1, 1), dt.date(2026, 1, 1)
SHOTS = {0: "OFF", 1: "1 SHOT", 2: "2 SHOT"}
AS_AT = dt.date(2026, 1, 31)           # the compliance report's status date
ON_TIME_DAYS = 30


def _in_2025(reg):
    ret = [r if isinstance(r, dt.date) else None for r in reg["retired_date"]]
    return reg[[i < Y1 and (r is None or r > Y0) for i, r in zip(reg["install_date"], ret)]]


def trip_operations_csv(path, rng, reg):
    """SCADA-logged protection operations per feeder relay or recloser control in 2025. Each feeder has its own
    reclosing: off (mostly cable feeders), one shot or two shots (rural overhead feeders and recloser controls).
    A fault trips the breaker; each reclose either holds or is followed by another trip, and a fault the last shot
    does not clear ends in lockout. Trip operations count every trip the breaker logged, so they also take in trips
    operators made for switching and trips with reclosing blocked under a hot-line hold, which have no reclose
    attempt and no lockout."""
    live = _in_2025(reg[reg["function"].isin(["Feeder protection", "Recloser control"])])
    rx = np.random.default_rng([W.SEED, 2, 1])
    rows = []
    for _, a in live.iterrows():
        rural = a.model == "AT-7"
        shots = int(rng.choice(3, p=[0.0, 0.3, 0.7] if rural else [0.28, 0.47, 0.25]))
        faults = int(rng.poisson(5.1 if rural else 2.6))
        trips = attempts = held = lockouts = 0
        for _ in range(faults):
            trips += 1
            transient = rng.random() < (0.8 if shots else 0.7)
            cleared = False
            for k in range(shots):
                attempts += 1
                if transient and rng.random() < (0.88 if k == 0 else 0.6):
                    held += 1
                    cleared = True
                    break
                trips += 1
            if not cleared:
                lockouts += 1
        if not rural and rx.random() < 0.08:
            trips += int(rx.integers(1, 4))                  # operator trips for switching
        if shots and rx.random() < 0.05:
            trips += 1                                       # fault with reclosing blocked under a hot-line hold
        rows.append(dict(asset_id=a.asset_id, sub_code=a.sub_code, bay=a.bay, year=2025, reclosing=SHOTS[shots],
                         trip_operations=trips, reclose_attempts=attempts, successful_recloses=held, lockouts=lockouts))
    pd.DataFrame(rows).to_csv(path, index=False)


def compliance_counts(reg, subs, wo):
    """tests due in 2025 by model and operating region from the PM work orders, and how each stood at the report's
    status date: done within 30 days of falling due, done later, or not done"""
    cur = dict(zip(subs["sub_code"], subs["region"]))
    model = dict(zip(reg["asset_id"], reg["model"]))
    pm = wo[(wo["work_type"] == "PM") & (wo["status"] != "CANC") & wo["asset_id"].isin(model.keys())]
    pm = pm[[Y0 <= d < Y1 for d in pm["reported_date"]]]
    out = {}
    for aid, sub, due, done in zip(pm["asset_id"], pm["sub_code"], pm["reported_date"], pm["completed_date"]):
        k = (model[aid], cur[sub])
        c = out.setdefault(k, [0, 0, 0, 0])
        c[0] += 1
        done = done if isinstance(done, dt.date) and done <= AS_AT else None
        if done is None:
            c[3] += 1
        elif (done - due).days <= ON_TIME_DAYS:
            c[1] += 1
        else:
            c[2] += 1
    return out


def test_compliance_xlsx(path, reg, subs, wo):
    """P&C maintenance test compliance for 2025, by model and operating region, for the maintenance program"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "2025 compliance"
    ws.append(["P&C maintenance test compliance, calendar year 2025"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["P&C maintenance program report. Tests due: periodic test work orders raised in 2025 under P&C Standard "
               "3.2, cancelled work orders excluded. On time: done within 30 days of the due date. Status at 31 January 2026."])
    hdr = ["Model", "Operating region", "Tests due", "Done on time", "Done late", "Not done", "On-time %"]
    ws.append(hdr)
    for j in range(1, len(hdr) + 1):
        ws.cell(row=3, column=j).font = Font(bold=True)
        ws.cell(row=3, column=j).fill = PatternFill("solid", fgColor="E3E9F2")
    counts = compliance_counts(reg, subs, wo)
    order = ["VPR-340", "VPR-220", "NX-9", "NX-5", "KDR-30", "AT-7", "RT-400", "RT-600"]
    regions = ["North", "Central", "South"]
    first = 4
    for m in order:
        for r in regions:
            c = counts.get((m, r))
            if not c:
                continue
            ws.append([m, r] + c)
            n = ws.max_row
            ws.cell(row=n, column=7, value="=D%d/C%d" % (n, n)).number_format = "0.0%"
    last = ws.max_row
    ws.append(["All models", None] + ["=SUM(%s%d:%s%d)" % (col, first, col, last) for col in "CDEF"])
    n = ws.max_row
    ws.cell(row=n, column=7, value="=D%d/C%d" % (n, n)).number_format = "0.0%"
    for j in range(1, 8):
        ws.cell(row=n, column=j).font = Font(bold=True)
    for j, w in enumerate([12, 16, 11, 13, 11, 10, 11], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
    ws.freeze_panes = "A4"
    wb.save(path)
