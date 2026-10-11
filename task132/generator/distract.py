"""Files a protection team keeps that look relevant to the buy and do not size it."""
import datetime as dt

import numpy as np
import openpyxl
import pandas as pd
from openpyxl.styles import Font, PatternFill

Y0, Y1 = dt.date(2025, 1, 1), dt.date(2026, 1, 1)


def _in_2025(reg):
    ret = [r if isinstance(r, dt.date) else None for r in reg["retired_date"]]
    return reg[[i < Y1 and (r is None or r > Y0) for i, r in zip(reg["install_date"], ret)]]


def trip_operations_csv(path, rng, reg):
    """SCADA-logged protection operations per feeder relay or recloser control in 2025: each fault is a trip;
    feeders with reclosing enabled try once, and a fault the reclose does not clear ends in lockout"""
    live = _in_2025(reg[reg["function"].isin(["Feeder protection", "Recloser control"])])
    rows = []
    for _, a in live.iterrows():
        rural = a.model == "AT-7"
        n = int(rng.poisson(5.1 if rural else 2.6))
        reclose = rural or rng.random() < 0.72
        att = n if reclose else 0
        ok = int(rng.binomial(att, 0.81)) if att else 0
        rows.append(dict(asset_id=a.asset_id, sub_code=a.sub_code, bay=a.bay, year=2025, trip_operations=n,
                         reclose_attempts=att, successful_recloses=ok, lockouts=n - ok))
    pd.DataFrame(rows).to_csv(path, index=False)


def test_compliance_xlsx(path, rng, reg, subs):
    """P&C maintenance test compliance for 2025, by model and operating region, as reported to the OEB"""
    cur = dict(zip(subs["sub_code"], subs["region"]))
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "2025 compliance"
    ws.append(["Protection relay test compliance, calendar year 2025"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Prepared for the annual OEB reliability filing. Relays due a test under the P&C maintenance standard (two-yearly at TS, three-yearly at DS)."])
    hdr = ["Model", "Operating region", "Relays due a test", "Tested on time", "Tested late", "Not tested", "On-time %"]
    ws.append(hdr)
    for j in range(1, len(hdr) + 1):
        ws.cell(row=3, column=j).font = Font(bold=True)
        ws.cell(row=3, column=j).fill = PatternFill("solid", fgColor="E3E9F2")
    live = _in_2025(reg).copy()
    live["op_region"] = [cur[s] for s in live["sub_code"]]
    kind = dict(zip(subs["sub_code"], subs["station_type"]))
    for (m, r), g in live.groupby(["model", "op_region"]):
        due = int(sum(rng.random() < (0.5 if kind[s] == "TS" else 1 / 3) for s in g["sub_code"]))
        if due == 0:
            continue
        late = int(rng.binomial(due, 0.06))
        nt = int(rng.binomial(due - late, 0.02))
        ok = due - late - nt
        ws.append([m, r, due, ok, late, nt, round(100 * ok / due, 1)])
        ws.cell(row=ws.max_row, column=7).number_format = "0.0"
    for j, w in enumerate([12, 16, 16, 15, 12, 11, 11], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
    ws.freeze_panes = "A4"
    wb.save(path)
