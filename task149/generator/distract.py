"""The two distractors: the workers' compensation third-party administrator's loss run and the behaviour-based safety
observation counts. Both look worth weighing for an injury forecast; neither is read by the call or the asks."""
from __future__ import annotations

import csv
import datetime as dt
import io
import os

import numpy as np

import common as K
import xlsx_util as XU

F_WC = "wc_loss_run_valued_2026-09-30.xlsx"
F_BBS = "bbs_observations_fy2025_fy2026.csv"


def write_wc(W, C, out):
    r = K.rng("wc")
    info = W.dcs.set_index("dc_no")
    wb = XU.Workbook()
    ws = wb.sheet("Loss run")
    ws.rows.append(["Ostrander Logistics - Workers' Compensation Loss Run (all states)", None, None, None, None, None, None, None, None, None, None, None])
    ws.rows.append(["Valued as of 09/30/2026. Prepared by the third-party administrator. Claims with accident dates 01/01/2021 to 09/30/2026.", None, None, None, None, None, None, None, None, None, None, None])
    ws.rows.append([None] * 12)
    ws.rows.append(["Claim No", "Location", "State", "Claimant ID", "Accident Date", "Report Date", "Claim Type", "Status",
                    "Paid Medical", "Paid Indemnity", "Paid Expense", "Outstanding Reserve"])
    ws.header_row = 4
    sel = C[(C.kind.isin(["REC", "FA"])) & (C.date <= dt.date(2026, 9, 30))]
    n = 41000
    rows = []
    for c in sel.itertuples():
        p = 0.74 if c.kind == "REC" else 0.05
        if r.random() > p or c.employer != K.ORG:
            continue
        n += int(r.integers(1, 9))
        indem = c.kind == "REC" and c.case_type == "DAFW" and (c.away_true or 0) > 7
        med = round(float(np.exp(r.normal(7.4 if c.kind == "REC" else 6.0, 0.9))), 2)
        ind = round(float(np.exp(r.normal(8.6, 1.0))), 2) if indem else 0.0
        exp_ = round(med * float(r.uniform(0.04, 0.16)), 2)
        rep = c.date + dt.timedelta(days=int(r.integers(0, 12)))
        open_ = (dt.date(2026, 9, 30) - c.date).days < 200 and r.random() < 0.5
        res = round(float(np.exp(r.normal(8.0, 1.0))), 2) if open_ else 0.0
        rows.append([("WC%d" % n), info.ehs_site[c.dc_no], info.state[c.dc_no], c.employee_id, c.date.strftime("%m/%d/%Y"),
                     rep.strftime("%m/%d/%Y"), "Indemnity" if indem else "Medical Only", "Open" if open_ else "Closed",
                     med, ind, exp_, res])
    rows.sort(key=lambda x: (x[4][6:], x[4][:5], x[0]))
    ws.rows.extend(rows)
    ws.widths = [11, 22, 6, 12, 12, 12, 13, 8, 13, 14, 12, 16]
    wb.save(os.path.join(out, F_WC), title="WC loss run 09/30/2026", creator="Claims Administration")


def write_bbs(W, out):
    r = K.rng("bbs")
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["dc_no", "fiscal_year", "fiscal_week", "observations", "at_risk_behaviors", "observers_active"])
    for dn in sorted(W.dcs.dc_no):
        lvl = float(np.exp(r.normal(np.log(58), 0.35)))
        risk = float(np.clip(r.normal(0.07, 0.02), 0.02, 0.15))
        for fy in (2025, 2026):
            nw = K.fy_weeks(fy) if fy < K.LAST_FY else K.LAST_WEEK
            for wk in range(1, nw + 1):
                obs = int(max(0, r.poisson(lvl * (0.7 if wk in (52, 1) else 1.0))))
                w.writerow([dn if not (dn == 311 and (fy, wk) >= (2025, 14)) else 318, fy, wk, obs,
                            int(r.binomial(obs, risk)), int(max(1, r.poisson(9)))])
    with open(os.path.join(out, F_BBS), "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())
