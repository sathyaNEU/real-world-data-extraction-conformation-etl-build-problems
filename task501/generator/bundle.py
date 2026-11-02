"""Read the shipped pack back. The golden, the ladder and the checks compute from these readers, never from the
simulation; verify.py reads the same files on its own code path."""
import csv
import datetime as dt
import os
import re

import numpy as np
import pandas as pd

import pack as PK

UK_BST = [(dt.datetime(2025, 3, 30, 1), dt.datetime(2025, 10, 26, 1)), (dt.datetime(2026, 3, 29, 1), dt.datetime(2026, 10, 25, 1))]


def path(target, key):
    return os.path.join(target, PK.FILES[key])


def local_to_utc(t):
    """Wall-clock time in the UK to UTC."""
    for a, b in UK_BST:
        if a + dt.timedelta(hours=1) <= t < b + dt.timedelta(hours=1):
            return t - dt.timedelta(hours=1)
    return t


def pdf_text(target, key):
    from pypdf import PdfReader
    txt = " ".join(p.extract_text() for p in PdfReader(path(target, key)).pages)
    return re.sub(r"\s+", " ", txt)


def _sheet_rows(ws):
    rows = list(ws.iter_rows(values_only=True))
    hdr = list(rows[2])
    return [dict(zip(hdr, r)) for r in rows[3:]]


def register(target):
    import openpyxl
    wb = openpyxl.load_workbook(path(target, "register"), data_only=True)
    mains = _sheet_rows(wb["Mains"])
    valves = _sheet_rows(wb["Valves"])
    dmas = _sheet_rows(wb["Districts"])
    return mains, valves, dmas


def flows(target):
    """District inflows as an hour x district frame (UTC hours), exact re-sent rows dropped, blank hours NaN."""
    df = pd.read_csv(path(target, "flows"), dtype=str, keep_default_na=False)
    n0 = len(df)
    df = df.drop_duplicates()
    df["flow"] = pd.to_numeric(df["flow_l_s"].replace("", np.nan))
    wide = df.pivot(index="reading_utc", columns="dma", values="flow").sort_index()
    wide.index = pd.to_datetime(wide.index)
    return wide, dict(rows=n0, unique=len(df), dup=n0 - len(df))


def outlet(target):
    df = pd.read_csv(path(target, "outlet"))
    s = pd.Series(df["outlet_flow_l_s"].values, index=pd.to_datetime(df["reading_utc"]))
    return s


def valve_log(target):
    df = pd.read_csv(path(target, "valvelog"), dtype=str, keep_default_na=False)
    df["local"] = pd.to_datetime(df["date"] + " " + df["time"], format="%d/%m/%Y %H:%M")
    df["utc"] = [local_to_utc(t.to_pydatetime()) for t in df["local"]]
    return df


def plan(target):
    """The outage plan's valve operations (valve, Open or Shut) in its own order, the works dates and its date."""
    txt = pdf_text(target, "plan")
    sec = txt[txt.index("Step Valve Main Location Set to"):txt.index("are supplied from Coldharbour")]
    ops = re.findall(r"\b(V\d{5})\b.*?\b(Open|Shut)\b", sec)
    works = re.search(r"out of service from (\d{1,2} \w+) to (\d{1,2} \w+ \d{4})", txt)
    date = re.search(r"1\.0 (\d{1,2} \w+ \d{4})", txt)
    return dict(ops=ops, works=works.groups() if works else None, date=date.group(1) if date else None, text=txt)


def turbidity(target):
    df = pd.read_csv(path(target, "turbidity"), dtype=str, keep_default_na=False)
    df["ntu"] = pd.to_numeric(df["turbidity_ntu"].replace("", np.nan))
    df["t"] = pd.to_datetime(df["reading_utc"])
    return df


def jobs(target):
    df = pd.read_csv(path(target, "jobs"), dtype=str, keep_default_na=False)
    return df


def supply(target):
    import openpyxl
    wb = openpyxl.load_workbook(path(target, "supply"), data_only=True)
    rows = _sheet_rows(wb["Supply points"])
    return pd.DataFrame(rows)


def consumption(target):
    return pd.read_csv(path(target, "consumption"), dtype={"spid": str, "month": str, "basis": str})


def amr(target):
    df = pd.read_csv(path(target, "amr"), dtype={"logger_id": str, "read_start_local": str})
    return df
