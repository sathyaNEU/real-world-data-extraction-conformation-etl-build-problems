"""task122 generator: the CRO's SDTM-style extract of VMK-4410-202 as locked, one table per domain.

Demographics and screen failures, visits, dosing, disposition, laboratory results from the two central laboratory
hubs and the sites' local laboratories, adverse events, concomitant medications, vital signs and trough
concentrations. Every table is written from the simulated trial; nothing here moves an eGFR value at a scheduled
visit, which the simulation fixed before any table is cut."""
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

import params as P
import sim as S

STUDY = P.STUDY
CC3 = {"DK": "DNK", "SE": "SWE", "DE": "DEU", "PL": "POL", "ES": "ESP", "GB": "GBR"}
VNUM = {v: n for v, n, d, w in P.VISITS}
HUB_NAM = P.CENTRAL
HUB_PREFIX = {"COPENHAGEN": "CPH", "MADRID": "MAD"}
LOCAL_DEPT = {"DK": "Klinisk Biokemisk Afdeling", "SE": "Klinisk kemi", "DE": "Zentrallabor", "PL": "Laboratorium Diagnostyczne",
              "ES": "Laboratorio de Analisis Clinicos", "GB": "Clinical Biochemistry"}
# units a local laboratory reports in, by country: potassium and sodium, creatinine, glucose, and whether it reports eGFR
LOCAL_UNITS = {"DK": ("mmol/L", "umol/L", "mmol/L", True), "SE": ("mmol/L", "umol/L", "mmol/L", True),
               "DE": ("mmol/l", "mg/dl", "mg/dl", True), "PL": ("mmol/l", "mg/dl", "mg/dl", False),
               "ES": ("mEq/L", "mg/dL", "mg/dL", False), "GB": ("mmol/L", "umol/L", "mmol/L", True)}
LOCAL_EGFR_UNIT = {"DK": "mL/min/1.73m2", "SE": "mL/min/1.73m2", "DE": "ml/min/1,73m2", "GB": "mL/min/1.73m2"}


def usubjid(s):
    return "%s-%s" % (STUDY, s)


def d(dt):
    return dt.isoformat() if isinstance(dt, date) else ""


def sday(c, n):
    """the date of study day n for a course"""
    return c.rand + timedelta(days=n - 1)


def ckd_epi_2009(mg, age, sex):
    k, a = (0.7, -0.329) if sex == "F" else (0.9, -0.411)
    r = mg / k
    g = 141.0 * min(r, 1.0) ** a * max(r, 1.0) ** -1.209 * 0.993 ** age
    return g * (1.018 if sex == "F" else 1.0)


def age_on(p, dt):
    return int(p["AGE"] + (dt - p["SCRDT"]).days / 365.25)


# ------------------------------------------------------------------------------------------------ demographics
def consent_dates(rng, Wd):
    """the day each screened patient signed the consent form, a few days before the screening visit"""
    cons = {}
    for df in (Wd["pats"], Wd["fails"]):
        for _, p in df.sort_values("SUBJID").iterrows():
            cons[p["SUBJID"]] = p["SCRDT"] - timedelta(days=int(rng.integers(0, 6)))
    return cons


def demographics(rng, Wd, consent):
    pats, fails, cs = Wd["pats"], Wd["fails"], Wd["cs"]
    rows = []
    races = {"GB": (["WHITE", "BLACK OR AFRICAN AMERICAN", "ASIAN", "OTHER"], [0.78, 0.09, 0.11, 0.02]),
             "DE": (["WHITE", "ASIAN", "OTHER", "NOT REPORTED"], [0.88, 0.03, 0.02, 0.07])}
    for src, df in (("R", pats), ("F", fails)):
        for _, p in df.iterrows():
            cc = p["COUNTRY"]
            rc, pr = races.get(cc, (["WHITE", "ASIAN", "OTHER"], [0.95, 0.03, 0.02]))
            race = str(rng.choice(rc, p=pr))
            cons = consent[p["SUBJID"]]
            row = {"STUDYID": STUDY, "USUBJID": usubjid(p["SUBJID"]), "SUBJID": p["SUBJID"], "SITEID": p["SITEID"],
                   "COUNTRY": CC3[cc], "BRTHYR": int(cons.year - p["AGE"] - (1 if rng.random() < 0.5 else 0)),
                   "AGE": int(p["AGE"]), "AGEU": "YEARS", "SEX": p["SEX"], "RACE": race,
                   "ETHNIC": "HISPANIC OR LATINO" if cc == "ES" else ("NOT REPORTED" if cc == "DE" else "NOT HISPANIC OR LATINO"),
                   "RFICDTC": d(cons)}
            if src == "R":
                c = cs[p["SUBJID"]]
                arm = p["ARM"]
                row.update({"ARMCD": P.ARMCD[arm], "ARM": arm, "ACTARMCD": P.ARMCD[arm], "ACTARM": arm, "ARMNRS": "",
                            "RANDDTC": d(p["RANDDT"]), "RFXSTDTC": d(c.rand), "RFXENDTC": d(sday(c, c.last_dose())),
                            "STRATEGFR": "eGFR " + ("<45" if p["STRAT_EGFR"] == "<45" else ">=45"),
                            "STRATUACR": "UACR " + ("<1000 mg/g" if p["STRAT_UACR"] == "<1000" else ">=1000 mg/g")})
            else:
                row.update({"ARMCD": "", "ARM": "", "ACTARMCD": "", "ACTARM": "", "ARMNRS": "SCREEN FAILURE",
                            "RANDDTC": "", "RFXSTDTC": "", "RFXENDTC": "", "STRATEGFR": "", "STRATUACR": ""})
            rows.append(row)
    out = pd.DataFrame(rows)
    return out.sort_values(["SITEID", "SUBJID"]).reset_index(drop=True)


# ------------------------------------------------------------------------------------------------ laboratory
class Lab:
    """every laboratory sample: central at each attended visit and each recheck or recollection, local checks"""

    def __init__(self, rng, Wd):
        self.rng, self.Wd = rng, Wd
        self.samples = []

    def sample(self, s, dt, visit, vnum, nam, kind, hub, cc, tests, cond=""):
        self.samples.append({"SUBJID": s, "DATE": dt, "VISIT": visit, "VISITNUM": vnum, "LBNAM": nam, "KIND": kind,
                             "HUB": hub, "CC": cc, "TESTS": tests, "COND": cond,
                             "TIME": "%02d:%02d" % (int(self.rng.integers(7, 12)) if kind == "central" else int(self.rng.integers(9, 16)),
                                                     int(self.rng.integers(0, 60)))})


def _chem_central(rng, hub, creat_orig, creat_unit, creat_mg, egfr, k, na, glu_mmol, haem):
    t = {}
    t["CREAT"] = (creat_orig, creat_unit, round(creat_mg * 88.42, 1) if creat_unit == "mg/dL" else float(creat_orig), "umol/L", "")
    t["EGFR"] = (str(egfr), "mL/min/1.73m2", float(egfr), "mL/min/1.73m2", "CKD-EPI 2021")
    if haem:
        t["K"] = ("", "mmol/L", None, "mmol/L", "", "NOT DONE", "SAMPLE HAEMOLYSED")
    else:
        t["K"] = ("%.1f" % k, "mmol/L", round(k, 1), "mmol/L", "")
    t["SODIUM"] = (str(int(na)), "mmol/L", float(int(na)), "mmol/L", "")
    if hub == "COPENHAGEN":
        t["GLUC"] = ("%.1f" % glu_mmol, "mmol/L", round(glu_mmol, 1), "mmol/L", "")
    else:
        mg = int(round(glu_mmol * 18.016))
        t["GLUC"] = (str(mg), "mg/dL", round(mg / 18.016, 1), "mmol/L", "")
    return t


def _urine(rng, hub, acr_mgg):
    """urine albumin, urine creatinine and their ratio as each hub reports them"""
    ucr = float(np.exp(rng.normal(np.log(8.5), 0.38)))      # mmol/L
    alb = acr_mgg * ucr * 0.11312                             # mg/L
    t = {}
    if hub == "COPENHAGEN":
        alb_r = max(round(alb, 1), 0.1)
        ucr_r = round(ucr, 1)
        acr = alb_r / ucr_r
        t["MALB"] = ("%.1f" % alb_r, "mg/L", alb_r, "mg/L", "")
        t["CREATU"] = ("%.1f" % ucr_r, "mmol/L", ucr_r, "mmol/L", "")
        t["ALBCREAT"] = ("%.1f" % acr, "mg/mmol", round(acr / 0.11312, 0), "mg/g", "")
    else:
        alb_r = max(round(alb, 1), 0.1)
        ucr_mgdl = round(ucr * 11.312, 1)
        acr = alb_r / (ucr_mgdl / 100.0)
        t["MALB"] = ("%.1f" % alb_r, "mg/L", alb_r, "mg/L", "")
        t["CREATU"] = ("%.1f" % ucr_mgdl, "mg/dL", round(ucr_mgdl / 11.312, 1), "mmol/L", "")
        t["ALBCREAT"] = ("%d" % int(round(acr)), "mg/g", float(int(round(acr))), "mg/g", "")
    return t


UACR_EFF = {0: 0.0, 5: -0.20, 10: -0.31, 20: -0.42, 40: -0.47}


def laboratory(rng, Wd, ae_k):
    """the laboratory table: central samples at every attended visit (screening failures included), central
    potassium rechecks and recollections after a haemolysed sample, and the sites' local checks"""
    pats, fails, cs, cal, rsc = Wd["pats"], Wd["fails"], Wd["cs"], Wd["cal"], Wd["rsc"]
    sites = Wd["sites"].set_index("SITEID")
    eg = Wd["egfr"].set_index(["SUBJID", "VISIT"])
    L = Lab(rng, Wd)
    rng_panel = np.random.default_rng(P.SEED + 31)
    pi = pats.set_index("SUBJID")
    # screening failures: one central screening sample
    for _, p in fails.iterrows():
        hub, cc = p["LAB_HUB"], p["COUNTRY"]
        mg = S.scr_from_egfr(max(p["SCR_EGFR"], 9.0), int(p["AGE"]), p["SEX"])
        orig, unit, mgr, egfr = S.report_creat(mg, hub, p["AGE"], p["SEX"])
        glu = float(np.clip(rng.normal(7.4, 2.0), 4.0, 16.0)) if rng.random() < 0.56 else float(np.clip(rng.normal(5.5, 0.6), 4.0, 7.5))
        t = _chem_central(rng, hub, orig, unit, mgr, egfr, p["SCR_K"], rng.normal(139.5, 2.3), glu, False)
        t.update(_urine(rng, hub, p["UACR0"]))
        L.sample(p["SUBJID"], p["SCRDT"], "SCREENING", 1, HUB_NAM[hub], "central", hub, cc, t)
    for s, c in cs.items():
        p = pi.loc[s]
        hub, cc = p["LAB_HUB"], p["COUNTRY"]
        dm = c.dose
        diab = bool(p["DIAB"])
        kv = {r["visit"]: r for r in Wd["krec"][s] if r["visit"] != "UNSCHEDULED"}
        last_vnum = 1
        for r in Wd["krec"][s]:
            v, dt = r["visit"], r["date"]
            if v != "UNSCHEDULED":
                last_vnum = VNUM[v]
                e = eg.loc[(s, v)]
                st = c.state(r["day"]) if dm else 0.0
                na = rng.normal(139.6 - 0.025 * dm * st, 2.2)
                glu = float(np.clip(rng.normal(7.6, 2.1), 3.9, 18.0)) if diab else float(np.clip(rng.normal(5.5, 0.55), 3.9, 7.8))
                t = _chem_central(rng, hub, e["CREAT_ORIG"], e["CREAT_UNIT"], e["CREAT_MG"], int(e["EGFR"]), r["k"], na, glu,
                                  r["haem"])
                if v in P.URINE_VISITS:
                    acr = p["UACR0"] * float(np.exp(UACR_EFF[dm] * st + rng.normal(0, 0.33))) if v != "SCREENING" else p["UACR0"]
                    t.update(_urine(rng, hub, acr))
                L.sample(s, dt, v, VNUM[v], HUB_NAM[hub], "central", hub, cc, t, "HAEMOLYSED" if r["haem"] else "")
                if r["haem"] and v not in ("SCREENING", "WEEK 56 FOLLOW-UP"):
                    # the site recollects for potassium within days
                    g = int(rng.integers(2, 7))
                    g += P.weekday_shift(dt + timedelta(days=g))
                    day2 = r["day"] + g
                    if c.last_day is not None and day2 > c.last_day:
                        continue
                    dt2 = dt + timedelta(days=g)
                    k2 = _k_level(rng, Wd, c, p, day2)
                    t2 = _central_unsched(rng, c, p, day2, k2, cal, rsc, hub, diab)
                    rng.random()
                    # the site files the new sample under the visit it replaces
                    L.sample(s, dt2, v, VNUM[v], HUB_NAM[hub], "central", hub, cc, t2)
            else:
                day2 = r["day"]
                if r["src"] == "central":
                    t2 = _central_unsched(rng, c, p, day2, r["k"], cal, rsc, hub, diab)
                    if rng_panel.random() < 0.4:
                        # a renal panel requested for the recheck: no glucose or sodium
                        t2 = {k: v for k, v in t2.items() if k in ("CREAT", "EGFR", "K")}
                    L.sample(s, dt, "UNSCHEDULED", round(last_vnum + 0.01, 2), HUB_NAM[hub], "central", hub, cc, t2)
                else:
                    t2 = _local(rng, c, p, day2, r["k"], cal, rsc, cc, diab)
                    city = sites.loc[p["SITEID"], "CITY"]
                    L.sample(s, dt, "UNSCHEDULED", round(last_vnum + 0.01, 2), "%s, %s" % (LOCAL_DEPT[cc], city), "local",
                             hub, cc, t2)
    # local potassium checks behind the hyperkalaemia events reported between visits
    for s, dt, k, day2 in ae_k:
        c = cs[s]
        p = pi.loc[s]
        diab = bool(p["DIAB"])
        cc = p["COUNTRY"]
        t2 = _local(rng, c, p, day2, k, cal, rsc, cc, diab)
        city = sites.loc[p["SITEID"], "CITY"]
        vprev = max([VNUM[v] for v, n, dd, w in P.VISITS if v in c.vd and c.vd[v] <= dt] + [1])
        L.sample(s, dt, "UNSCHEDULED", round(vprev + 0.01, 2), "%s, %s" % (LOCAL_DEPT[cc], city), "local", p["LAB_HUB"], cc, t2)
    return L.samples


def _k_level(rng, Wd, c, p, day):
    from sim import KDELTA
    dk = KDELTA[c.dose] * p["K_MULT"]
    on = c.on(day)
    k = p["K0"] + (dk * 0.95 if on else 0.0) + rng.normal(0, 0.2)
    return float(min(k, 5.8))


def _central_unsched(rng, c, p, day, k, cal, rsc, hub, diab):
    g = S.true_egfr(c, day, cal, rsc)
    age = age_on(p, sday(c, day))
    mg = S.scr_from_egfr(max(g, 9.0), age, p["SEX"]) * float(np.exp(rng.normal(0, 0.021)))
    orig, unit, mgr, egfr = S.report_creat(mg, hub, age, p["SEX"])
    glu = float(np.clip(rng.normal(7.6, 2.1), 3.9, 18.0)) if diab else float(np.clip(rng.normal(5.5, 0.55), 3.9, 7.8))
    return _chem_central(rng, hub, orig, unit, mgr, egfr, k, rng.normal(139.4, 2.3), glu, False)


def _local(rng, c, p, day, k, cal, rsc, cc, diab):
    ku, cu, gu, has_egfr = LOCAL_UNITS[cc]
    g = S.true_egfr(c, day, cal, rsc)
    age = age_on(p, sday(c, day))
    mg = S.scr_from_egfr(max(g, 9.0), age, p["SEX"]) * float(np.exp(rng.normal(0.015, 0.03)))
    t = {}
    t["K"] = ("%.1f" % k, ku, round(k, 1), "mmol/L", "")
    na = int(round(rng.normal(139.0, 2.4)))
    t["SODIUM"] = (str(na), ku, float(na), "mmol/L", "")
    if cu == "umol/L":
        um = int(round(mg * 88.42))
        t["CREAT"] = (str(um), cu if cc != "DK" else "µmol/L", float(um), "umol/L", "")
        mgr = um / 88.42
    else:
        mgr = round(mg, 2)
        t["CREAT"] = ("%.2f" % mgr, cu, round(mgr * 88.42, 1), "umol/L", "")
    glu = float(np.clip(rng.normal(7.6, 2.1), 3.9, 18.0)) if diab else float(np.clip(rng.normal(5.6, 0.6), 3.9, 7.8))
    if gu == "mmol/L":
        t["GLUC"] = ("%.1f" % glu, gu, round(glu, 1), "mmol/L", "")
    else:
        gm = int(round(glu * 18.016))
        t["GLUC"] = (str(gm), gu, round(gm / 18.016, 1), "mmol/L", "")
    if has_egfr:
        e9 = int(round(ckd_epi_2009(mgr, age, p["SEX"])))
        t["EGFR"] = (str(e9) if e9 < 90 else ">90", LOCAL_EGFR_UNIT[cc], float(e9) if e9 < 90 else None, "mL/min/1.73m2", "CKD-EPI 2009")
    return t


TEST = {"CREAT": ("Creatinine", "CHEMISTRY", "SERUM"), "EGFR": ("Glomerular Filtration Rate, Estimated", "CHEMISTRY", "SERUM"),
        "K": ("Potassium", "CHEMISTRY", "SERUM"), "SODIUM": ("Sodium", "CHEMISTRY", "SERUM"),
        "GLUC": ("Glucose", "CHEMISTRY", "SERUM"), "MALB": ("Microalbumin", "URINALYSIS", "URINE"),
        "CREATU": ("Creatinine", "URINALYSIS", "URINE"), "ALBCREAT": ("Albumin/Creatinine", "URINALYSIS", "URINE")}
RANGE = {"CREAT": {"M": (64, 104), "F": (49, 90)}, "EGFR": (60, None), "K": (3.5, 5.1), "SODIUM": (136, 145),
         "GLUC": (3.9, 7.8), "MALB": (None, 20), "CREATU": (None, None), "ALBCREAT": (None, 30)}
LOCAL_K_HI = {"DK": 4.6, "SE": 5.0, "DE": 5.1, "PL": 5.1, "ES": 5.1, "GB": 5.3}


def lab_table(samples, pats_all):
    sex = dict(zip(pats_all["SUBJID"], pats_all["SEX"]))
    samples = sorted(samples, key=lambda x: (x["DATE"], x["TIME"], x["SUBJID"], x["LBNAM"]))
    acc = {"COPENHAGEN": 4100000, "MADRID": 7300000}
    rows = []
    for smp in samples:
        ref = ""
        if smp["KIND"] == "central":
            acc[smp["HUB"]] += 1
            ref = "%s%d" % (HUB_PREFIX[smp["HUB"]], acc[smp["HUB"]])
        for cd in ["CREAT", "EGFR", "K", "SODIUM", "GLUC", "MALB", "CREATU", "ALBCREAT"]:
            if cd not in smp["TESTS"]:
                continue
            t = smp["TESTS"][cd]
            orres, oru, stn, stu, meth = t[:5]
            stat, reas = (t[5], t[6]) if len(t) > 5 else ("", "")
            name, cat, spec = TEST[cd]
            rg = RANGE[cd]
            lo, hi = rg[sex[smp["SUBJID"]]] if isinstance(rg, dict) else rg
            if cd == "K" and smp["KIND"] == "local":
                hi = LOCAL_K_HI[smp["CC"]]
            ind = ""
            if stn is not None and stat == "":
                if hi is not None and stn > hi:
                    ind = "HIGH"
                elif lo is not None and stn < lo:
                    ind = "LOW"
                else:
                    ind = "NORMAL"
            if cd == "EGFR" and stn is None and orres.startswith(">"):
                ind = "NORMAL"
            rows.append({"STUDYID": STUDY, "USUBJID": usubjid(smp["SUBJID"]), "LBREFID": ref, "LBTESTCD": cd, "LBTEST": name,
                         "LBCAT": cat, "LBSPEC": spec, "LBORRES": orres, "LBORRESU": oru,
                         "LBSTRESC": ("%g" % stn) if stn is not None else (orres if stat == "" else ""),
                         "LBSTRESN": stn, "LBSTRESU": stu, "LBSTNRLO": lo, "LBSTNRHI": hi, "LBNRIND": ind, "LBSTAT": stat,
                         "LBREASND": reas, "LBSPCCND": smp["COND"] if cd == "K" else "", "LBMETHOD": meth,
                         "LBNAM": smp["LBNAM"], "VISITNUM": smp["VISITNUM"], "VISIT": smp["VISIT"],
                         "LBDTC": "%sT%s" % (smp["DATE"].isoformat(), smp["TIME"])})
    lb = pd.DataFrame(rows)
    lb = lb.sort_values(["USUBJID", "LBDTC", "LBCAT", "LBTESTCD"], kind="mergesort").reset_index(drop=True)
    lb.insert(2, "LBSEQ", lb.groupby("USUBJID").cumcount() + 1)
    return lb


# ------------------------------------------------------------------------------------------------ visits
def pickups(Wd):
    """dispensing visits a patient missed: the bottles were collected at the site on the visit's planned day"""
    out = []
    for s, c in Wd["cs"].items():
        for v in P.DISPENSE[1:]:
            if (s, v) not in Wd["missed"]:
                continue
            dday = S.day_of(c.vd[v], c.rand)
            if dday > c.last_dose() or (s in Wd["leave"] and dday > Wd["leave"][s]):
                continue
            out.append((s, v, c.vd[v]))
    return out


def visits(Wd, samples):
    rows = []
    for s, v, dt in pickups(Wd):
        rows.append((s, float(VNUM[v] - 1), "UNSCHEDULED", dt, "STUDY DRUG DISPENSING"))
    for _, p in Wd["fails"].iterrows():
        rows.append((p["SUBJID"], 1.0, "SCREENING", p["SCRDT"], ""))
    for s, c in Wd["cs"].items():
        for v in S.attended(Wd["vds"], Wd["leave"], Wd["missed"], s):
            rows.append((s, float(VNUM[v]), v, Wd["vds"][s][v], ""))
    seen = set()
    for smp in samples:
        if smp["VISIT"] != "UNSCHEDULED":
            continue
        key = (smp["SUBJID"], smp["DATE"])
        if key in seen:
            continue
        seen.add(key)
        why = "LOCAL LABORATORY TEST" if smp["KIND"] == "local" else "REPEAT LABORATORY TEST"
        rows.append((smp["SUBJID"], float(smp["VISITNUM"]), "UNSCHEDULED", smp["DATE"], why))
    sv = pd.DataFrame(rows, columns=["SUBJID", "VISITNUM", "VISIT", "DT", "SVUPDES"])
    sv = sv.sort_values(["SUBJID", "DT", "VISITNUM"]).reset_index(drop=True)
    # unscheduled visits numbered within the scheduled visit they follow
    n = {}
    vn = []
    for _, r in sv.iterrows():
        if r["VISIT"] == "UNSCHEDULED":
            base = int(r["VISITNUM"])
            n[(r["SUBJID"], base)] = n.get((r["SUBJID"], base), 0) + 1
            vn.append(round(base + 0.01 * n[(r["SUBJID"], base)], 2))
        else:
            vn.append(r["VISITNUM"])
    sv["VISITNUM"] = vn
    return pd.DataFrame({"STUDYID": STUDY, "USUBJID": sv["SUBJID"].map(usubjid), "VISITNUM": sv["VISITNUM"],
                         "VISIT": sv["VISIT"], "SVSTDTC": sv["DT"].map(d), "SVENDTC": sv["DT"].map(d),
                         "SVUPDES": sv["SVUPDES"]})


def renumber_unscheduled(samples, sv):
    """give each unscheduled sample the visit number its visit carries in the visits table"""
    m = {}
    for _, r in sv[sv["VISIT"] == "UNSCHEDULED"].iterrows():
        m[(r["USUBJID"], r["SVSTDTC"])] = r["VISITNUM"]
    for smp in samples:
        if smp["VISIT"] == "UNSCHEDULED":
            smp["VISITNUM"] = m[(usubjid(smp["SUBJID"]), smp["DATE"].isoformat())]
    return samples


# ------------------------------------------------------------------------------------------------ dosing
def dosing(Wd):
    """one row per bottle period: from the dispensing visit to the next one, both days inclusive, split around an
    interruption and cut at the last dose"""
    rows = []
    pick = pickups(Wd)
    for s, c in Wd["cs"].items():
        att = S.attended(Wd["vds"], Wd["leave"], Wd["missed"], s)
        picked = {v for s_, v, dt in pick if s_ == s}
        disp = [v for v in P.DISPENSE if v in att or v in picked]
        last = c.last_dose()
        starts = [S.day_of(c.vd[v], c.rand) for v in disp]
        disp = ["UNSCHEDULED" if v in picked else v for v in disp]
        segs = []
        for i, a in enumerate(starts):
            if a > last:
                break
            b = starts[i + 1] if i + 1 < len(starts) else last
            b = min(b, last)
            segs.append([a, b, disp[i]])
        holds = sorted((a, b) for a, b in c.off if b is not None)
        out = []
        for a, b, v in segs:
            pieces = [(a, b)]
            for ha, hb in holds:
                nxt = []
                for x, y in pieces:
                    if hb <= x or ha > y:
                        nxt.append((x, y))
                        continue
                    if x <= ha - 1:
                        nxt.append((x, ha - 1))
                    if hb <= y:
                        nxt.append((hb, y))
                pieces = nxt
            for x, y in pieces:
                out.append((x, y, v))
        dose = P.DOSE[c.arm]
        for x, y, v in out:
            rows.append({"STUDYID": STUDY, "USUBJID": usubjid(s), "EXTRT": "VMK-4410" if dose else "PLACEBO",
                         "EXDOSE": dose, "EXDOSU": "mg", "EXDOSFRM": "TABLET", "EXDOSFRQ": "QD", "EXROUTE": "ORAL",
                         "VISIT": v, "EXSTDTC": d(sday(c, x)), "EXENDTC": d(sday(c, y))})
    ex = pd.DataFrame(rows).sort_values(["USUBJID", "EXSTDTC"]).reset_index(drop=True)
    ex.insert(2, "EXSEQ", ex.groupby("USUBJID").cumcount() + 1)
    return ex


# ------------------------------------------------------------------------------------------------ disposition
DS_TERM = {"ADVERSE EVENT": ["Adverse event", "Adverse event: dizziness", "Adverse event: hypotension", "AE - fatigue"],
           "PATIENT DECISION": ["Patient wish", "Patient decided to stop study medication", "Subject's own decision"],
           "PHYSICIAN DECISION": ["Investigator decision", "Physician decision: polypharmacy", "Investigator decision: hospitalisation"]}


def disposition(rng, Wd, sv, cons):
    pats, fails, cs, info = Wd["pats"], Wd["fails"], Wd["cs"], Wd["info"]
    rows = []
    for _, p in fails.iterrows():
        s = p["SUBJID"]
        rows.append((s, "INFORMED CONSENT OBTAINED", "INFORMED CONSENT OBTAINED", "PROTOCOL MILESTONE", "", "SCREENING", cons[s]))
        why = p["FAILREASON"]
        term = {"EGFR OUT OF RANGE": "Inclusion criterion 3 not met (eGFR)", "UACR OUT OF RANGE": "Inclusion criterion 4 not met (UACR)",
                "POTASSIUM ABOVE 4.8": "Exclusion criterion 6 met (serum potassium)"}.get(why, why.capitalize())
        rows.append((s, term, "SCREEN FAILURE", "DISPOSITION EVENT", "STUDY PARTICIPATION", "SCREENING",
                     p["SCRDT"] + timedelta(days=int(rng.integers(3, 12)))))
    last_visit = {}
    for _, r in sv.iterrows():
        last_visit[r["USUBJID"]] = max(last_visit.get(r["USUBJID"], ""), r["SVSTDTC"])
    for _, p in pats.iterrows():
        s = p["SUBJID"]
        c = cs[s]
        rows.append((s, "INFORMED CONSENT OBTAINED", "INFORMED CONSENT OBTAINED", "PROTOCOL MILESTONE", "", "SCREENING", cons[s]))
        rows.append((s, "RANDOMIZED", "RANDOMIZED", "PROTOCOL MILESTONE", "", "TREATMENT", p["RANDDT"]))
        inf = info[s]
        if c.stopped_for_good():
            why = inf["stop_reason"]
            when = sday(c, c.last_dose())
            if why == "ADVERSE EVENT (POTASSIUM)":
                rows.append((s, "Hyperkalaemia", "ADVERSE EVENT", "DISPOSITION EVENT", "STUDY DRUG", "TREATMENT", when))
            elif why == "WITHDRAWAL BY SUBJECT":
                rows.append((s, "Consent withdrawn", "WITHDRAWAL BY SUBJECT", "DISPOSITION EVENT", "STUDY DRUG", "TREATMENT", when))
            else:
                term = DS_TERM[why][int(rng.integers(0, len(DS_TERM[why])))]
                dec = "WITHDRAWAL BY SUBJECT" if why == "PATIENT DECISION" else why
                rows.append((s, term, dec, "DISPOSITION EVENT", "STUDY DRUG", "TREATMENT", when))
        elif inf["ds_wrong"] is not None:
            # entered as a permanent stop when the drug was held; the patient restarted and the form was not reopened
            why = ["ADVERSE EVENT", "PHYSICIAN DECISION"][int(rng.integers(0, 2))]
            term = DS_TERM[why][int(rng.integers(0, len(DS_TERM[why])))]
            rows.append((s, term, why, "DISPOSITION EVENT", "STUDY DRUG", "TREATMENT", sday(c, inf["ds_wrong"] - 1)))
        else:
            rows.append((s, "Completed study treatment", "COMPLETED", "DISPOSITION EVENT", "STUDY DRUG", "TREATMENT",
                         sday(c, c.end)))
        lv = date.fromisoformat(last_visit[usubjid(s)])
        if s in Wd["leave"]:
            rows.append((s, "Consent withdrawn", "WITHDRAWAL BY SUBJECT", "DISPOSITION EVENT", "STUDY PARTICIPATION",
                         "FOLLOW-UP", lv))
        else:
            rows.append((s, "Completed study", "COMPLETED", "DISPOSITION EVENT", "STUDY PARTICIPATION", "FOLLOW-UP", lv))
    ds = pd.DataFrame(rows, columns=["SUBJID", "DSTERM", "DSDECOD", "DSCAT", "DSSCAT", "EPOCH", "DT"])
    ds = ds.sort_values(["SUBJID", "DT", "DSCAT"], kind="mergesort").reset_index(drop=True)
    out = pd.DataFrame({"STUDYID": STUDY, "USUBJID": ds["SUBJID"].map(usubjid)})
    out["DSSEQ"] = out.groupby("USUBJID").cumcount() + 1
    for col in ["DSTERM", "DSDECOD", "DSCAT", "DSSCAT", "EPOCH"]:
        out[col] = ds[col]
    out["DSSTDTC"] = ds["DT"].map(d)
    return out
