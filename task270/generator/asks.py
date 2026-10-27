"""The asks' golden, read from the pack: each network's population (the call's construction on every network), and
the 2025-26 pilot's first consultations and six-week follow-ups by quarter in Krathwold and Lathcombe.

The pilot's records are the portal's export joined to the payment statements: a record in a statement and not in the
export (recorded after the export was pulled) is added from the statement; a recovered first consultation whose
patient has another first consultation the federation did not recover is that consultation recorded a second time and is
dropped, while every other recovered record is a consultation held and claimed late, and stays; each pharmacy's
network is where it stood on the day of the consultation; each patient is carried through the pseudonym crosswalk."""
from __future__ import annotations

import datetime as dt
import os

import openpyxl
import pandas as pd

from common import TARGET
import pilot as PL
import records as R

NETS = {"Krathwold": "KRT", "Lathcombe": "LTH"}


def load_pilot(target=TARGET):
    X = pd.read_csv(os.path.join(target, R.F_XWALK), dtype=str)
    xmap = dict(zip(X["old_pseudonym"], X["new_pseudonym"]))
    E = pd.read_csv(os.path.join(target, PL.F_PORTAL), dtype=str)
    E["date"] = pd.to_datetime(E["consultation_date"], dayfirst=True).dt.date
    wb = openpyxl.load_workbook(os.path.join(target, PL.F_STATEMENTS), read_only=True)
    S = []
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        for r in rows[1:]:
            S.append(dict(ods=r[0], record_id=r[1], patient_ref=r[2], consultation_type=r[3],
                          date=r[4].date() if hasattr(r[4], "date") else r[4], amount=r[5], line=r[6],
                          statement=ws.title))
    S = pd.DataFrame(S)
    P = pd.read_csv(os.path.join(target, PL.F_PHARMACIES), dtype=str).fillna("")
    return E, S, P, xmap


def pilot_figures(target=TARGET):
    E, S, P, xmap = load_pilot(target)
    recovered = set(S.loc[S["line"] == "Recovery", "record_id"])
    pay = S[S["line"] == "Payment"]
    late = pay[~pay["record_id"].isin(set(E["record_id"]))]
    rows = E[["record_id", "pharmacy_ods", "patient_ref", "consultation_type", "date"]].copy()
    add = late.rename(columns={"ods": "pharmacy_ods"})[["record_id", "pharmacy_ods", "patient_ref",
                                                         "consultation_type", "date"]]
    rows = pd.concat([rows, add], ignore_index=True)
    rows["pat"] = rows["patient_ref"].map(lambda k: xmap.get(k, k))
    rows["recovered"] = rows["record_id"].isin(recovered)
    is_first = rows["consultation_type"] == "First consultation"
    kept_first = set(rows.loc[is_first & ~rows["recovered"], "pat"])
    second = is_first & rows["recovered"] & rows["pat"].isin(kept_first)
    rows = rows[~second]
    loc = {r.ods_code: (r.locality, r.relocated_on, r.previous_locality) for r in P.itertuples()}

    def net_on(ods, d):
        l, when, prev = loc[ods]
        if when and d < dt.date.fromisoformat(when):
            l = prev
        return NETS.get(l)

    F = rows[(rows["consultation_type"] == "First consultation") & (rows["date"] >= PL.PILOT_START)
             & (rows["date"] <= PL.PILOT_END)].copy()
    F["net"] = [net_on(o, d) for o, d in zip(F["pharmacy_ods"], F["date"])]
    F = F[F["net"].notna()]
    fu = rows[rows["consultation_type"] == "Follow-up"].groupby("pat")["date"].apply(list).to_dict()
    C1 = {(n, q): 0 for n in ("KRT", "LTH") for q in (1, 2, 3, 4)}
    C2 = dict(C1)
    for r in F.itertuples():
        k = (r.net, PL.quarter(r.date))
        C1[k] += 1
        if any(0 < (d - r.date).days <= 42 for d in fu.get(r.pat, [])):
            C2[k] += 1
    return C1, C2
