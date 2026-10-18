"""Read the cut pack back into the view the call's computation reads, the way an analyst has to: the legacy rows
linked to the national identifier through the crosswalk and their regimen lines coded, the June 2024 visits held in
both systems kept once, the EPR rows re-sent after a failed sync dropped, the patient master's dates of birth and
outcomes. Shared by checks.py (which compares it with the generator's clean view) and cracker.py."""
from __future__ import annotations

import csv
import datetime as dt
import os

import numpy as np
import pandas as pd

D = dt.date


def _rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _iso(s):
    return D.fromisoformat(s) if s else None


def _dmy(s):
    d, m, y = s.split("/")
    return D(int(y), int(m), int(d))


def register_view(pack, drop_resent=True, link_legacy=True, dedupe_overlap=True):
    codes = {r["legacy_register_text"]: r["regimen_code"] for r in _rows(os.path.join(pack, "national_regimen_codes_2026.csv"))}
    cw = {r["art_no"]: r["upid"] for r in _rows(os.path.join(pack, "art_number_crosswalk_2024-06.csv"))}
    epr = pd.read_csv(os.path.join(pack, "paed_register_visits_epr_2024-06_2026-08.csv"), dtype=str, keep_default_na=False)
    if drop_resent:
        epr = epr.sort_values("synced_at").drop_duplicates(
            ["upid", "facility_code", "visit_date", "encounter_type", "weight_kg", "regimen_code", "months_dispensed",
             "next_appointment"], keep="first")
    ev = pd.DataFrame(dict(uid=epr.upid.values, date=[D.fromisoformat(x) for x in epr.visit_date],
                           weight=[float(x) if x else np.nan for x in epr.weight_kg], regimen=epr.regimen_code.values,
                           months=epr.months_dispensed.astype(int).values,
                           next_appt=[D.fromisoformat(x) for x in epr.next_appointment], src="epr"))
    leg = pd.read_csv(os.path.join(pack, "paed_register_visits_legacy_2023-01_2024-06.csv"), dtype=str, keep_default_na=False)
    uid = [cw.get(a) if link_legacy else a for a in leg.art_no]
    lv = pd.DataFrame(dict(uid=uid, date=[_dmy(x) for x in leg.visit_date],
                           weight=[float(x) if x else np.nan for x in leg.weight_kg],
                           regimen=[codes[x] for x in leg.regimen], months=leg.months_dispensed.astype(int).values,
                           next_appt=[_dmy(x) for x in leg.next_visit], src="legacy"))
    v = pd.concat([lv, ev], ignore_index=True)
    if dedupe_overlap:
        v = v.sort_values(["uid", "date", "src"]).drop_duplicates(["uid", "date"], keep="last")
    v = v.drop(columns="src").sort_values(["uid", "date"]).reset_index(drop=True)
    pts = pd.read_csv(os.path.join(pack, "paed_register_patients_2026-09-02.csv"), dtype=str, keep_default_na=False)
    code = {"Lost to follow-up": "LTFU", "Transferred out": "TO", "Died": "DIED", "Transferred to adult care": "ADULT"}
    kids = pd.DataFrame(dict(uid=pts.upid.values, dob=[D.fromisoformat(x) for x in pts.date_of_birth],
                             sex=pts.sex.values, art_start=[D.fromisoformat(x) for x in pts.art_start_date],
                             outcome=[code[x] if x else None for x in pts.outcome],
                             outcome_date=[_iso(x) for x in pts.outcome_date]))
    return kids, v
