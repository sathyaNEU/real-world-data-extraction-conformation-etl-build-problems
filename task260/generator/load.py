"""Read the pack as a solver would: every table from target/, nothing from the generator's state."""
from __future__ import annotations

import json
import os

import pandas as pd

import common as K


def _xlsx(path, first_col, sheet=0):
    """A sheet whose header row is the first row starting with first_col (title and note rows above it)."""
    raw = pd.read_excel(path, sheet_name=sheet, header=None)
    hdr = next(i for i in range(len(raw)) if raw.iloc[i, 0] == first_col)
    df = pd.read_excel(path, sheet_name=sheet, header=hdr)
    return df.dropna(how="all")


def readings(path):
    """One ReadPoint export in a common shape: study, reader, case, cond, session, position, opened, submitted, pom
    (0 to 100), recall, revision (1 for the first submission)."""
    raw = pd.read_csv(path, dtype=str)
    if "pom" in raw.columns:
        df = pd.DataFrame(dict(study=raw["project"], reader=raw["user_id"], case=raw["case_code"],
                               cond=raw["arm"].map({"UNAIDED": "unaided", "AIDED": "aided"}),
                               session=raw["session_no"].astype(int), position=raw["position"].astype(int),
                               opened=pd.to_datetime(raw["opened_utc"]), submitted=pd.to_datetime(raw["submitted_utc"]),
                               pom=raw["pom"].astype(float), recall=raw["recall"] == "Y",
                               revision=raw["revision"].astype(int)))
    else:
        df = pd.DataFrame(dict(study=raw["project_code"], reader=raw["reader_ref"], case=raw["case_ref"],
                               cond=raw["condition"].map({"Unaided": "unaided", "AI-assisted": "aided"}),
                               session=raw["session"].astype(int), position=raw["seq"].astype(int),
                               opened=pd.to_datetime(raw["started_at"]).dt.tz_localize(None),
                               submitted=pd.to_datetime(raw["completed_at"]).dt.tz_localize(None),
                               pom=(raw["malignancy_probability"].astype(float) * 100).round(),
                               recall=raw["recall_decision"] == "Recall to assessment",
                               revision=raw["edit_count"].astype(int) + 1))
    return df


def read(target):
    p = lambda n: os.path.join(target, n)
    T = {"exports": {S["sid"]: readings(p(K.EXPORTS[S["sid"]])) for S in K.STUDIES}}
    T["cases"] = {S["sid"]: _xlsx(p(K.CASES), "Case", sheet=S["code"]) for S in K.STUDIES}
    T["panels"] = _xlsx(p(K.PANELS), "Study")
    T["ris"] = pd.read_csv(p(K.RIS), dtype={"images": "Int64"}, keep_default_na=False)
    T["codes"] = pd.read_csv(p(K.CODES))
    T["locations"] = json.load(open(p(K.LOCATIONS), encoding="utf-8"))
    T["visits"] = _xlsx(p(K.VISITS), "Unit")
    T["workforce"] = _xlsx(p(K.WORKFORCE), "Employee number")
    return T
