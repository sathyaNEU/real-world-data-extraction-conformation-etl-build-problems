"""The files only the asks read: the return-to-work work-status log (Ask A) and the WMS item master, its history and
the programme DCs' SKU pick summary (Ask B)."""
from __future__ import annotations

import csv
import datetime as dt
import io
import os

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import asks_world as AW
import common as K
import world as WD

F_RTW = "rtw_work_status_log_fy2026.csv"
F_ITEM = "wms_item_master_2026-11-01.csv"
F_ITEMH = "wms_item_master_history.csv"
F_PICKS = "wms_sku_picks_fy2026_p01_p11.parquet"

MANAGERS = ["cm.ahollis", "cm.bwade", "cm.dkerr", "cm.jmoss", "cm.lprice", "cm.nkhan", "cm.rtate", "cm.sowen"]
NOTES_BENIGN = ["", "", "", "", "Light duty assignment", "Per physician note", "Modified duty - no lifting over 20 lb",
                "Released to modified duty", "Follow-up visit scheduled", "Light duty assignment"]


def _no26(dn):
    """A DC's number in fiscal 2026 (Rockford is 318 from fiscal 2025 week 14)."""
    return WD.RECODE_NEW_NO if dn == WD.RECODE_DC else dn


def rtw_rows(W, C):
    """Every status row the case management system holds for fiscal 2026's return-to-work files. The associate's home
    DC on every record is the DC the associate belongs to now (the system overwrites it when an associate moves); an
    associate who moves while on restricted duty gets a new record at the receiving DC."""
    r = K.rng("rtw_rows")
    cases = AW.rtw_cases(W)
    key2pid = {}
    for row in C.itertuples():
        key2pid[(row.date, int(row.dc_no), row.hour, row.minute, row.employee_id)] = row.platform_id
    out = []
    seq = 3105
    for c in sorted(cases, key=lambda x: (x["date"], x["dc_no"], x["employee_id"])):
        pid = key2pid[c["key"]]
        seq += int(r.integers(1, 3))
        rid = "RTW-26-%05d" % seq
        cm = MANAGERS[int(r.integers(0, len(MANAGERS)))]
        moved = bool(c["moved_on"] and c["moved_on"] <= AW.EXTRACT and (c["sep_on"] is None or c["moved_on"] < c["sep_on"]))
        home = _no26(c["moved_to"] if moved else c["dc_no"])
        rows = []
        for kind, a, b in c["spells"]:
            if a > AW.EXTRACT:
                break
            rows.append([rid, pid, c["employee_id"], home, kind, a, cm])
        ended = False
        if moved:
            to = _no26(c["moved_to"])
            rows = [x for x in rows if x[5] <= c["moved_on"]]
            rows.append([rid, pid, c["employee_id"], home, "TRANSFER OUT", c["moved_on"], cm])
            seq += 1
            rid2 = "RTW-26-%05d" % seq
            cm2 = MANAGERS[int(r.integers(0, len(MANAGERS)))]
            rows.append([rid2, "", c["employee_id"], to, "RESTRICTED", c["moved_on"], cm2])
            if c["sep_on"] is not None and c["sep_on"] <= AW.EXTRACT:
                rows.append([rid2, "", c["employee_id"], to, "SEPARATED", c["sep_on"], cm2])
            elif c["full_duty"] <= AW.EXTRACT:
                rows.append([rid2, "", c["employee_id"], to, "FULL DUTY", c["full_duty"], cm2])
            ended = True
        if not ended:
            if c["sep_on"] is not None and c["sep_on"] <= AW.EXTRACT:
                # the spells after separation never happened
                rows = [x for x in rows if x[5] < c["sep_on"]]
                rows.append([rid, pid, c["employee_id"], home, "SEPARATED", c["sep_on"], cm])
            elif c["full_duty"] <= AW.EXTRACT:
                rows.append([rid, pid, c["employee_id"], home, "FULL DUTY", c["full_duty"], cm])
        for x in rows:
            eff = x[5]
            entered = eff + dt.timedelta(days=int(r.choice([0, 0, 0, 1, 1, 2, 3, 6])))
            entered = min(entered, K.PULL_DATE - dt.timedelta(days=1))
            note = NOTES_BENIGN[int(r.integers(0, len(NOTES_BENIGN)))] if x[4] in ("RESTRICTED", "TRANSFER") else ""
            if x[4] == "TRANSFER OUT":
                note = "Associate transferred"
            out.append(x[:6] + [entered, x[6], note])
    return out, cases


def write_rtw(W, C, out):
    rows, cases = rtw_rows(W, C)
    rows.sort(key=lambda x: (x[0], x[5], ["AWAY", "RESTRICTED", "TRANSFER", "TRANSFER OUT", "SEPARATED", "FULL DUTY"].index(x[4])))
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["RTW_CASE_ID", "EHS_CASE_NO", "ASSOCIATE_NO", "HOME_DC", "STATUS", "EFFECTIVE_DATE", "ENTERED_ON",
                "CASE_MANAGER", "NOTE"])
    for x in rows:
        w.writerow([x[0], x[1], x[2], x[3], x[4], x[5].isoformat(), x[6].isoformat(), x[7], x[8]])
    with open(os.path.join(out, F_RTW), "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())
    return rows, cases


# ---------------------------------------------------------------------------------------------------- Ask B
def shipped_weight(it):
    """The case weight as the item master stores it: kilograms for items set up through the vendor portal."""
    if it.source == "PORTAL":
        return round(it.weight_lb / 2.20462, 1)
    return it.weight_lb


def write_items(W, I, out):
    cur = I[((I.version == 2) | ((I.version == 1) & (I.reissue_period == 0))) & (I.purged_period == 0)].copy()
    cur = cur.sort_values("sku")
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["SKU", "DESCRIPTION", "CATEGORY", "CASE_WEIGHT", "CASE_CUBE_FT3", "WEIGHT_SOURCE", "SETUP_DATE", "STATUS"])
    for it in cur.itertuples():
        w.writerow([it.sku, it.desc, it.category, "%.1f" % shipped_weight(it), "%.2f" % it.cube, it.source,
                    it.setup.isoformat(), "ACTIVE"])
    with open(os.path.join(out, F_ITEM), "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())
    # history: every version with its dates, benign attribute changes among them
    r = K.rng("item_hist")
    rows = []
    for it in I.sort_values(["sku", "version"]).itertuples():
        eff_from = it.eff_from
        eff_to = it.eff_to if not pd.isna(it.eff_to) else None
        reason = "NEW ITEM"
        if it.version == 2:
            reason = "NEW ITEM"
        if it.purged_period:
            eff_to = K.week_start(2026, K.period_weeks(2026, int(it.purged_period))[0]) - dt.timedelta(days=1)
        rows.append([it.sku, it.version, it.desc, "%.1f" % shipped_weight(it), "%.2f" % it.cube, it.source,
                     eff_from.isoformat(), eff_to.isoformat() if eff_to else "", reason])
        # benign later edits (description or cube re-measure) on a share of items: same weight
        if it.version == 1 and not it.purged_period and r.random() < 0.05:
            d = it.setup + dt.timedelta(days=int(r.integers(200, 2400)))
            if d < dt.date(2026, 10, 1):
                rows[-1][7] = (d - dt.timedelta(days=1)).isoformat()
                rows.append([it.sku, 1, it.desc, "%.1f" % shipped_weight(it), "%.2f" % round(it.cube * float(np.exp(r.normal(0, 0.04))), 2),
                             it.source, d.isoformat(), eff_to.isoformat() if eff_to else "", "CUBE UPDATE"])
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["SKU", "ITEM_VERSION", "DESCRIPTION", "CASE_WEIGHT", "CASE_CUBE_FT3", "WEIGHT_SOURCE", "EFFECTIVE_FROM",
                "EFFECTIVE_TO", "CHANGE_TYPE"])
    for x in rows:
        w.writerow(x)
    with open(os.path.join(out, F_ITEMH), "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())
    return cur


def write_picks(W, I, out):
    S0 = AW.sku_picks(W, I)
    S = S0.copy()
    info = W.dcs.set_index("dc_no")
    S["loc_code"] = [info.wms_code[d] for d in S.dc_no]
    S = S.groupby(["loc_code", "per", "sku"], as_index=False).agg(cases=("cases", "sum"))
    S = S.sort_values(["loc_code", "per", "sku"], kind="mergesort").reset_index(drop=True)
    tbl = pa.Table.from_pydict({"loc_code": S.loc_code.tolist(), "fiscal_year": [2026] * len(S),
                                "fiscal_period": S.per.astype(int).tolist(), "sku": S.sku.astype(int).tolist(),
                                "cases_picked": S.cases.astype(int).tolist()},
                               schema=pa.schema([("loc_code", pa.string()), ("fiscal_year", pa.int16()),
                                                 ("fiscal_period", pa.int8()), ("sku", pa.int32()),
                                                 ("cases_picked", pa.int32())]))
    tbl = tbl.replace_schema_metadata({"source": "WMS pick history summary", "dcs": "FY2027 ergonomics program DCs",
                                       "through": "FY2026 week 44"})
    pq.write_table(tbl, os.path.join(out, F_PICKS), compression="snappy", use_dictionary=True, write_statistics=False)
    return S0, S
