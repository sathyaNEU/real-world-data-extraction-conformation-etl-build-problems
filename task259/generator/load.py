"""Read the pack as shipped: every frame the analysis uses comes from target/, parsed the way the files say."""
from __future__ import annotations

import datetime as dt
import os

import openpyxl
import pandas as pd

import common as K


def _csv(target, name, dates=(), **kw):
    df = pd.read_csv(os.path.join(target, name), keep_default_na=False, na_values=[""], **kw)
    for c in dates:
        df[c] = pd.to_datetime(df[c], format="%Y-%m-%d").dt.date
        df[c] = df[c].where(df[c].notna(), None)
    return df


def extract(target):
    return _csv(target, K.EXTRACT, dates=("filed_on", "previous_filed_on"), dtype={"state": "string"})


def profiles(target):
    return _csv(target, K.PROFILES)


def crosswalk(target):
    return _csv(target, K.CROSSWALK, dates=("effective_from", "effective_to"))


def survey_match(target):
    """The survey match the job architecture gives the Data Engineer job: (family, primary focus)."""
    wb = openpyxl.load_workbook(os.path.join(target, K.ARCHITECTURE), read_only=True, data_only=True)
    ws = wb["Jobs"]
    rows = list(ws.iter_rows(values_only=True))
    head = [str(c) for c in rows[K.ARCH_HEADER_ROW]]
    for row in rows[K.ARCH_HEADER_ROW + 1:]:
        rec = dict(zip(head, row))
        if rec.get("Job") == "Data Engineer":
            return rec["Tallyband family"], rec["Tallyband primary focus"]
    raise KeyError("Data Engineer")


def hris(target):
    return _csv(target, K.HRIS, dates=("effective_date",))


def zones(target):
    return _csv(target, K.ZONES, dates=("effective_from", "effective_to"))


def ats(target):
    return _csv(target, K.ATS, dates=("opened_on", "closed_on", "status_date"))


def as_date(s):
    return dt.date.fromisoformat(s)
