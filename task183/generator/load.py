"""Read the built pack back from target/ into data frames, the way an analyst would open it."""
import datetime as dt
import json
import os

import openpyxl
import pandas as pd

import records as R


def _d(x):
    if x is None or x is pd.NaT or (isinstance(x, float) and pd.isna(x)) or (isinstance(x, str) and x == ""):
        return None
    if isinstance(x, dt.datetime):
        return x.date()
    if isinstance(x, dt.date):
        return x
    x = str(x)
    if "/" in x:                                   # MM/DD/YYYY, the work management export
        m, d, y = x.split("/")
        return dt.date(int(y), int(m), int(d))
    return dt.date.fromisoformat(x[:10])


def work_orders(target):
    wo = pd.read_csv(os.path.join(target, R.WO), dtype=str)
    wo["fault_date"] = wo["fault_date"].map(_d)
    wo["completed_date"] = wo["completed_date"].map(_d)
    return wo


def register(target):
    wb = openpyxl.load_workbook(os.path.join(target, R.REGISTER), read_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    hdr_i = next(i for i, r in enumerate(rows) if r and r[0] == "SECTION_ID")
    cols = [c.lower() for c in rows[hdr_i]]
    df = pd.DataFrame([r for r in rows[hdr_i + 1:] if r and r[0]], columns=cols)
    for c in ("install_date", "retired_date", "last_edit"):
        df[c] = pd.Series([_d(x) for x in df[c]], index=df.index, dtype=object)
    df["predecessor_section_id"] = df["predecessor_section_id"].fillna("")
    return df


def oms(target):
    return pd.read_csv(os.path.join(target, R.OMS), dtype={"outage_id": str, "customers_out": int})


def steps(target):
    return pd.read_csv(os.path.join(target, R.STEPS), dtype={"outage_id": str})


def connectivity(target):
    c = pd.read_parquet(os.path.join(target, R.CONN))
    c["eff_from"] = c["eff_from"].map(_d)
    c["eff_to"] = pd.Series([_d(x) for x in c["eff_to"]], index=c.index, dtype=object)
    return c


def devices(target):
    return json.load(open(os.path.join(target, R.DEVICES)))


def cis(target):
    c = pd.read_csv(os.path.join(target, R.CIS), dtype=str)
    c.columns = [x.lower() for x in c.columns]
    c["service_address"] = c["service_address"].str.strip()
    return c


def meds(target):
    return pd.read_csv(os.path.join(target, R.MED), dtype=str)
