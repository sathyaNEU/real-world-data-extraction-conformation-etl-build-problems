"""Read the pack as shipped: every file through its own notes (US dates, UTC timestamps to Central time, cents to
dollars, voids on their own dates)."""
from __future__ import annotations

import os

import pandas as pd

import common as K


def _p(target, key):
    return os.path.join(target, K.F[key])


def _central(s: pd.Series) -> pd.Series:
    """UTC ISO timestamps to naive Central-time datetimes (NaT stays NaT)."""
    t = pd.to_datetime(s, utc=True, errors="coerce")
    return t.dt.tz_convert(K.CENTRAL).dt.tz_localize(None)


def legacy_claims(target):
    d = pd.read_csv(_p(target, "legacy_claims"), dtype=str)
    d["key"] = d.CLM_NO + "-" + d.FEAT_NO
    for c, n in (("LOSS_DT", "acc"), ("RPT_DT", "rep"), ("CLS_DT", "cls")):
        d[n] = pd.to_datetime(d[c], format="%m/%d/%Y")
    d["reopen_ct"] = d.REOPEN_CT.astype(int)
    return d


def legacy_payments(target):
    d = pd.read_csv(_p(target, "legacy_pay"), dtype=str)
    d["key"] = d.CLM_NO + "-" + d.FEAT_NO
    d["acc"] = pd.to_datetime(d.LOSS_DT, format="%m/%d/%Y")
    d["date"] = pd.to_datetime(d.TRANS_DT, format="%m/%d/%Y")
    d["amount"] = d.AMOUNT.astype(float)
    return d


def features(target):
    d = pd.read_csv(_p(target, "features"), dtype=str, keep_default_na=False)
    d["acc"] = pd.to_datetime(d.accident_date)
    d["rep"] = pd.to_datetime(d.reported_date)
    for c in ("created_at", "closed_at", "reopened_at"):
        d[c.replace("_at", "")] = _central(d[c].replace("", None))
    return d


def events(target):
    d = pd.read_csv(_p(target, "events"), dtype=str, keep_default_na=False)
    d["at"] = _central(d.event_at)
    return d


def payments(target):
    d = pd.read_csv(_p(target, "pay"), dtype=str, keep_default_na=False)
    d["amount"] = d.amount_cents.astype(int) / 100.0
    d["issued"] = _central(d.issued_at)
    d["voided"] = _central(d.voided_at.replace("", None))
    return d


def ledger(target):
    d = pd.read_csv(_p(target, "gl"), dtype=str)
    d["date"] = pd.to_datetime(d.posting_date)
    d["amount"] = d.amount.astype(float)
    return d


def booked(target):
    import openpyxl
    wb = openpyxl.load_workbook(_p(target, "register"), data_only=True)
    ws = wb.active
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[1] == "Bodily injury" and row[2] == "Loss":
            return float(row[3]) * 1000.0
    raise ValueError("no bodily injury loss line in the register")
