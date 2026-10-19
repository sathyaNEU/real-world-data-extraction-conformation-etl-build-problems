"""The cut pack read back as the golden reads it: the two systems' ACE-III sittings joined on the NHS number through
the master index, the diagnoses on the record, the episodes, appointments and the pathway tracker."""
import datetime as dt
import os
import pandas as pd
import common as K

YEAR = 365.25


def digits(s):
    return s.astype(str).str.replace(r"\D", "", regex=True)


def load(target):
    f = lambda k: os.path.join(target, K.FILES[k])
    P = {}
    pmi = pd.read_csv(f("pmi"), dtype=str, keep_default_na=False)
    pmi["hpn"] = pmi.hpn.str.strip()
    pmi["nhs"] = digits(pmi.nhs_number)
    P["pmi"] = pmi
    hpn2nhs = dict(zip(pmi.hpn, pmi.nhs))
    reg = pd.read_excel(f("clinics"), sheet_name="Clinics", dtype=str)
    cis2clinic = {r["CIS clinic code"]: r["Clinic"] for _, r in reg.iterrows() if isinstance(r["CIS clinic code"], str)}
    site2clinic = dict(zip(reg["EPR site code"], reg["Clinic"]))
    P["cis2clinic"], P["site2clinic"] = cis2clinic, site2clinic
    # the old system's forms
    cis = pd.read_csv(f("cis_ace"), dtype=str, keep_default_na=False)
    cis["nhs"] = cis.hpn.str.strip().map(hpn2nhs)
    cis["date"] = pd.to_datetime(cis.assessment_date, format="%d/%m/%Y").dt.date
    cis["clinic"] = cis.clinic_code.map(cis2clinic)
    cis["completed"] = cis.form_status == "C"
    cis["total"] = cis.total.astype(int)
    cis["system"] = "CIS"
    cis["set"] = cis.form_id
    # the electronic record's sets
    obs = pd.read_csv(f("epr_obs"), dtype=str, keep_default_na=False)
    obs = obs[obs.set_status != "Entered in error"]
    tot = obs[obs.item_code == "ACE3_TOTAL"].copy()
    tot["nhs"] = digits(tot.nhs_number)
    tot["date"] = pd.to_datetime(tot.performed_at.str[:10]).dt.date
    tot["clinic"] = tot.site_code.map(site2clinic)
    tot["completed"] = tot.set_status == "Final"
    tot["total"] = tot.value.astype(int)
    tot["system"] = "EPR"
    tot["set"] = tot.obs_set_id
    cols = ["nhs", "date", "clinic", "completed", "total", "system", "set"]
    s = pd.concat([cis[cols], tot[cols]], ignore_index=True)
    s = s.sort_values(["nhs", "date", "set"]).reset_index(drop=True)
    # completed sittings before each one, over the patient's whole record
    s["k"] = s.groupby("nhs").completed.transform(lambda c: c.astype(int).cumsum().shift(fill_value=0))
    P["sittings"] = s
    # the diagnoses on the record
    cd = pd.read_csv(f("cis_dx"), dtype=str, keep_default_na=False)
    cd["nhs"] = cd.hpn.str.strip().map(hpn2nhs)
    cd["date"] = pd.to_datetime(cd.diagnosis_date, format="%d/%m/%Y").dt.date
    cd["code"] = cd.icd10_code
    cd["order"] = 0
    ed = pd.read_csv(f("epr_dx"), dtype=str, keep_default_na=False)
    ed["nhs"] = digits(ed.nhs_number)
    ed["date"] = pd.to_datetime(ed.recorded_on).dt.date
    ed["code"] = ed.problem_code
    ed["order"] = (ed.source == "EPR").astype(int) + 1
    dx = pd.concat([cd[["nhs", "date", "code", "order"]], ed[["nhs", "date", "code", "order"]]], ignore_index=True)
    P["dx"] = dx.sort_values(["nhs", "date", "order"]).reset_index(drop=True)
    P["episodes"] = pd.read_csv(f("episodes"), dtype=str, keep_default_na=False)
    P["appts"] = pd.read_csv(f("appts"), dtype=str, keep_default_na=False)
    P["tracker"] = pd.read_excel(f("tracker"), sheet_name="Pathways", dtype={"NHS number": str})
    return P


def in_scope(code):
    return code.startswith("F00") or code.startswith("G30") or code == "F06.7"


def latest_dx(P, day=K.WINDOW[1]):
    d = P["dx"]
    d = d[d.date <= day]
    return d.groupby("nhs").tail(1).set_index("nhs").code


def frame(P):
    """The paper's population with each sitting's time in years and the step (a completed sitting before)."""
    s = P["sittings"]
    w0, w1 = K.WINDOW
    lat = latest_dx(P)
    w = s[s.completed & (s.date >= w0) & (s.date <= w1)].copy()
    w["latest"] = w.nhs.map(lat)
    w = w[w.latest.fillna("").map(in_scope)]
    w = w[w.groupby("nhs").date.transform("size") >= 2].copy()
    w["t"] = (pd.to_datetime(w.date) - pd.Timestamp(w0)).dt.days / YEAR
    w["step"] = (w.k >= 1).astype(float)
    w["s"] = w.total.astype(float)
    w["pid"] = w.nhs
    first = s[s.completed].groupby("nhs").date.min()
    w["first_t"] = (pd.to_datetime(w.nhs.map(first)) - pd.Timestamp(w0)).dt.days / YEAR
    return w


def history(P):
    """Every completed sitting of every patient with two or more, for the gain read off the whole record."""
    s = P["sittings"]
    h = s[s.completed].copy()
    h = h[h.groupby("nhs").date.transform("size") >= 2].copy()
    h["t"] = (pd.to_datetime(h.date) - pd.Timestamp(K.WINDOW[0])).dt.days / YEAR
    h["step"] = (h.k >= 1).astype(float)
    h["s"] = h.total.astype(float)
    h["pid"] = h.nhs
    return h
