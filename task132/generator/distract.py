"""Files a protection team keeps that look relevant to the buy and do not size it."""
import datetime as dt

import numpy as np
import openpyxl
import pandas as pd
from openpyxl.styles import Font, PatternFill


def trip_operations_csv(path, rng, reg):
    """SCADA-logged protection operations per feeder relay in 2025 (faults cleared, reclose attempts)"""
    live = reg[(reg["status"] == "IN SERVICE") & (reg["function"] == "Feeder protection")]
    rows = []
    for _, a in live.iterrows():
        n = int(rng.poisson(3.2))
        rows.append(dict(asset_id=a.asset_id, sub_code=a.sub_code, bay=a.bay, year=2025,
                         trip_operations=n, reclose_attempts=int(rng.binomial(n, 0.7)) if n else 0,
                         successful_recloses=0, lockouts=0))
    df = pd.DataFrame(rows)
    df["successful_recloses"] = [int(rng.binomial(r, 0.8)) if r else 0 for r in df["reclose_attempts"]]
    df["lockouts"] = [int(max(0, t - s - int(rng.integers(0, 2)))) for t, s in zip(df["trip_operations"], df["successful_recloses"])]
    df.to_csv(path, index=False)


def test_compliance_xlsx(path, rng, reg):
    """P&C maintenance test compliance for 2025, by model and region, as reported to the regulator"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "2025 compliance"
    ws.append(["Protection relay test compliance, calendar year 2025 (OEB reporting basis)"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    hdr = ["Model", "Region", "Relays due a test", "Tested on time", "Tested late", "Not tested", "On-time %"]
    ws.append(hdr)
    for j in range(1, len(hdr) + 1):
        ws.cell(row=3, column=j).font = Font(bold=True)
        ws.cell(row=3, column=j).fill = PatternFill("solid", fgColor="E3E9F2")
    live = reg[reg["status"] == "IN SERVICE"]
    for (m, r), g in live.groupby(["model", "region"]):
        due = int(round(len(g) / 3))
        late = int(rng.binomial(due, 0.06))
        nt = int(rng.binomial(due - late, 0.02))
        ok = due - late - nt
        ws.append([m, r, due, ok, late, nt, round(100 * ok / due, 1) if due else None])
    for j, w in enumerate([12, 12, 16, 15, 12, 11, 11], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
    wb.save(path)
