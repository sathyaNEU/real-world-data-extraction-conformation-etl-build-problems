"""Write the exports the district's systems hold, from the clean truth, each in its producing system's own layout:
Tamarack's and Ridgeline's electronic data deliverables, the gauging export, the monitoring point register with its
survey history, the sampler's October and April 2026 purge entries and instrument calibration entries, and the
program's neighbouring records."""
import csv
import datetime as dt
import json
import math
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font

import analytes as A
import sim
import world as W

EV = sim.EV
FILES = {
    "edd_a": "tamarack_edd_marten_creek_2018-2021.csv",
    "edd_b": "ridgeline_edd_MCL_2021-2026.txt",
    "gauging": "mcl_gauging_rounds_2018-2026.csv",
    "points": "mcl_monitoring_points.xlsx",
    "sap": "MCL_SAP_rev2_2018.pdf",
    "approval": "MCL_post-closure_approval_2017.pdf",
    "fieldproc": "Fieldstone_FS-03_groundwater_sampling.pdf",
    "purge": "fieldlog_purge_entries_2026.csv",
    "calib": "fieldlog_calibration_entries_2026.csv",
    "gas": "mcl_gas_probe_readings_2025-2026.csv",
    "precip": "hollis_coop_precip_daily_2018-2026.json",
    "inspect": "mcl_site_inspections_2024-2026.xlsx",
}
DISTRACTORS = ["gas", "precip", "inspect"]
STAMP = (2026, 11, 3, 7, 40, 0)


def rng(k):
    return np.random.default_rng(W.SEED * 1000 + k)


def write_csv(path, head, rows, delim=","):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=delim, lineterminator="\r\n")
        w.writerow(head)
        for r in rows:
            w.writerow(r)


def fmt(v, d):
    return ("%%.%df" % d) % v


def sigstr(v):
    """three significant figures as a laboratory prints them"""
    if v == 0:
        return "0"
    d = max(0, 3 - int(math.floor(math.log10(abs(v)))) - 1)
    return fmt(round(v, d), d)


# ---------------------------------------------------------------- the samples each event takes
def sample_plan():
    """{event: [(location, day_index, local datetime, sample_type, parent)]}; the October and April 2026 times are
    the chain of custody's: the minute each sample was collected, local time, as the sampler wrote it."""
    r = rng(1)
    plan = {}
    ftruth = SIM["field_truth"]
    for ei, e in enumerate(W.EVENTS):
        rows = []
        order = [list(d) for d in W.SAMPLING_ORDER]
        if ei < 9:   # MW-5 before its replacement
            order = [[("MW-5" if x == "MW-5R" else x) for x in d] for d in order]
        for di, wells in enumerate(order):
            t = dt.datetime.combine(e["days"][di], dt.time(11, 40) if di == 0 else dt.time(8, 50))
            for w in wells:
                if (EV[ei], w) in W.MISSED:
                    continue
                if (ei, w) in ftruth:
                    ts = ftruth[(ei, w)]["collect_time"].replace(second=0, microsecond=0)
                else:
                    t += dt.timedelta(minutes=float(r.uniform(62, 95)))
                    ts = t.replace(second=0, microsecond=0)
                rows.append((w, di, ts, "N", w))
                t = ts
        # the leachate sump and the creek points on the last field day
        last = e["days"][2]
        rows.append(("LS-1", 2, dt.datetime.combine(last, dt.time(14, int(r.integers(5, 40)))), "N", "LS-1"))
        rows.append(("SW-1", 2, dt.datetime.combine(last, dt.time(15, int(r.integers(5, 25)))), "N", "SW-1"))
        rows.append(("SW-2", 2, dt.datetime.combine(last, dt.time(15, int(r.integers(30, 55)))), "N", "SW-2"))
        # one field duplicate a event, rotating; one equipment blank on day 2; a trip blank with each cooler day
        wells_here = [x for x in rows if x[0].startswith("MW")]
        dup = wells_here[(ei * 5 + 3) % len(wells_here)]
        rows.append(("FD", dup[1], dup[2], "FD", dup[0]))
        eb_day = e["days"][1]
        rows.append(("EB", 1, dt.datetime.combine(eb_day, dt.time(13, int(r.integers(0, 50)))), "EB", "EB"))
        for di in range(3):
            rows.append(("TB", di, dt.datetime.combine(e["days"][di], dt.time(7, 30)), "TB", "TB"))
        plan[ei] = rows
    return plan


# ---------------------------------------------------------------- results
def leachate_and_creek(r):
    out = {}
    for ei in range(len(EV)):
        for k in W.INDICATORS:
            out[("LS-1", ei, k)] = sim.reported(k, W.LEACHATE[k] * math.exp(r.normal(0, 0.08)), sim.lab_of(ei))
            for p, base in (("SW-1", {"chloride": 14.2, "sodium": 8.6, "boron": 22.0}),
                            ("SW-2", {"chloride": 15.0, "sodium": 9.1, "boron": 24.0})):
                out[(p, ei, k)] = sim.reported(k, base[k] * math.exp(r.normal(0, 0.12)), sim.lab_of(ei))
    return out


def indicator(loc, ei, k):
    if loc in W.BACKGROUND:
        return SIM["bg"][(loc, ei, k)]
    if (loc, ei, k) in SIM["cmp"]:
        return SIM["cmp"][(loc, ei, k)]
    return LCK[(loc, ei, k)]


def plume_f(loc, ei):
    if loc in W.BACKGROUND:
        return SIM["bg_frac"].get((loc, ei), 0.0)
    if loc == "LS-1":
        return 1.0
    return SIM["cmp_frac"].get((loc, ei), 0.0)


LEACH_OTHER = {"Alkalinity, Total (as CaCO3)": 3900.0, "Ammonia as N": 410.0, "Calcium": 210.0, "Magnesium": 160.0,
               "Potassium": 260.0, "Sulfate": 35.0, "Nitrate + Nitrite as N": 0.4, "Total Dissolved Solids": 6200.0,
               "Iron": 9.5, "Manganese": 1.9}
ATTENUATED = {"Ammonia as N": 0.02, "Potassium": 0.25, "Iron": 0.3, "Manganese": 0.4}


def other_inorganic(r, loc, ei, name, nat):
    f = plume_f(loc, ei)
    if loc.startswith("SW"):
        nat *= 0.7
    v = nat * math.exp(r.normal(0, 0.12))
    if f > 0:
        lv = LEACH_OTHER[name]
        if loc != "LS-1":
            lv *= ATTENUATED.get(name, 1.0)
        v = (1 - f) * v + f * lv
    if loc == "LS-1":
        v = LEACH_OTHER[name] * math.exp(r.normal(0, 0.1))
    return v


def results_for(sample, ei, r):
    """the analyses one sample receives: [(group, name, cas, value or None for a non-detect, unit, rl, fraction)]"""
    loc, di, ts, stype, parent = sample
    oct_event = W.EVENTS[ei]["month"] == 10
    pfas_on = EV.index(A.PFAS_FROM) <= ei
    out = []
    src = parent if stype in ("FD",) else loc
    if stype in ("N", "FD"):
        for name, cas, ma, mb, unit, rl, nat in A.INORGANIC:
            frac = "D" if name in A.DISSOLVED else "N"
            if name == "Chloride":
                v = indicator(src, ei, "chloride")
            elif name == "Sodium":
                v = indicator(src, ei, "sodium")
            elif name == "Boron":
                v = indicator(src, ei, "boron")
                if src.startswith("SW") or src == "LS-1":
                    frac = "T"
            else:
                v = other_inorganic(r, src, ei, name, nat)
                if name in ("Ammonia as N", "Iron", "Manganese") and v < rl:
                    v = None
            if stype == "FD" and v is not None and name in ("Chloride", "Sodium", "Boron"):
                v = sim.reported({"Chloride": "chloride", "Sodium": "sodium", "Boron": "boron"}[name],
                                 v * math.exp(r.normal(0, 0.025)), sim.lab_of(ei))
            if (EV[ei], src) in W.BORON_NOT_RUN and name == "Boron" and stype == "N":
                continue
            out.append(("inorg", name, cas, v, unit, rl, frac))
        if src.startswith("MW") or src == "LS-1":
            for name, cas, rl, nat in A.METALS:
                for frac in ("T", "D"):
                    v = None
                    if nat is not None:
                        v = nat * math.exp(r.normal(0, 0.25)) * (1.15 if frac == "T" else 1.0)
                        if src == "LS-1":
                            v *= 9.0
                        if v < rl:
                            v = None
                    out.append(("metal", name, cas, v, "ug/L", rl, frac))
            out.append(("metal", "Mercury", "7439-97-6", None, "ug/L", 0.2, "T"))
        if src.startswith("MW") or src == "LS-1":
            for name, cas, rl in A.VOCS:
                v = None
                if src == "LS-1" and name in ("Acetone", "2-Butanone (MEK)", "Benzene", "Toluene", "Ethylbenzene",
                                              "Xylenes, Total", "Tetrahydrofuran", "1,4-Dichlorobenzene",
                                              "4-Methyl-2-pentanone (MIBK)", "Chloroethane"):
                    v = rl * r.uniform(4, 60)
                elif src == "MW-6" and ei == W.EVAL and name in ("cis-1,2-Dichloroethene", "1,1-Dichloroethane",
                                                                  "Tetrahydrofuran"):
                    v = rl * r.uniform(1.3, 2.4)
                elif name in ("Acetone", "Methylene chloride") and r.random() < 0.06:
                    v = rl * r.uniform(0.35, 0.9)
                out.append(("voc", name, cas, v, "ug/L", rl, "N"))
            for name, cas in A.SURROGATES:
                out.append(("surr", name, cas, r.uniform(88, 112), "%REC", None, "N"))
        if oct_event and (src.startswith("MW") or src == "LS-1"):
            for name, cas in A.SVOCS:
                v = None
                rl = 10.0 if "nitro" in name.lower() or "phenol" in name.lower() else 5.0
                if name == "1,4-Dioxane":
                    rl = 2.0
                    if src == "LS-1":
                        v = r.uniform(18, 60)
                if src == "LS-1" and name in ("Phenol", "3&4-Methylphenol", "Diethyl phthalate"):
                    v = rl * r.uniform(2, 9)
                if name == "Bis(2-ethylhexyl)phthalate" and r.random() < 0.05:
                    v = rl * r.uniform(0.4, 0.9)
                out.append(("svoc", name, cas, v, "ug/L", rl, "N"))
            for name, cas in A.SVOC_SURROGATES:
                out.append(("ssurr", name, cas, r.uniform(42, 108), "%REC", None, "N"))
        if pfas_on and (src == "LS-1" or src.startswith("SW")):
            for name, cas in A.PFAS:
                v = None
                if src == "LS-1" and r.random() < 0.8:
                    v = r.uniform(40, 1800)
                elif src.startswith("SW") and r.random() < 0.25:
                    v = r.uniform(1.2, 6.0)
                out.append(("pfas", name, cas, v, "ng/L", 2.0, "N"))
    elif stype == "EB":
        for name, cas, ma, mb, unit, rl, nat in A.INORGANIC:
            out.append(("inorg", name, cas, None, unit, rl, "D" if name in A.DISSOLVED else "N"))
        for name, cas, rl in A.VOCS:
            v = rl * r.uniform(0.4, 0.9) if name in ("Acetone", "Methylene chloride") and r.random() < 0.2 else None
            out.append(("voc", name, cas, v, "ug/L", rl, "N"))
    elif stype == "TB":
        for name, cas, rl in A.VOCS:
            v = rl * r.uniform(0.4, 0.9) if name in ("Acetone", "Methylene chloride") and r.random() < 0.15 else None
            out.append(("voc", name, cas, v, "ug/L", rl, "N"))
        for name, cas in A.SURROGATES:
            out.append(("surr", name, cas, r.uniform(90, 110), "%REC", None, "N"))
    return out


# re-analyses: (event label, location, analyte) reported twice, the second reportable
REANALYSIS = {("2019-OCT", "LS-1", "Chloride"): ("DILUTION", 10), ("2022-OCT", "MW-2", "Chloride"): ("REANALYSIS", 1),
              ("2024-APR", "MW-8", "Sodium"): ("REANALYSIS", 1), ("2025-OCT", "LS-1", "Boron"): ("DILUTION", 20),
              ("2020-APR", "MW-3", "Chloride"): ("REANALYSIS", 1), ("2026-OCT", "MW-10", "Chloride"): ("REANALYSIS", 1)}


def write_edds(tgt):
    plan = sample_plan()
    r = rng(2)
    rows_a, rows_b = [], []
    seq = {"A": 18040211, "B": 2110001}
    for ei, e in enumerate(W.EVENTS):
        lab = sim.lab_of(ei)
        recv = e["days"][2] + dt.timedelta(days=1)
        for s in plan[ei]:
            loc, di, ts, stype, parent = s
            res = results_for(s, ei, r)
            seq[lab] += int(r.integers(1, 3))
            lab_id = ("T%08d" % seq["A"]) if lab == "A" else ("R%s-%04d" % (ts.strftime("%y%m"), seq["B"] % 10000))
            for group, name, cas, v, unit, rl, frac in res:
                key = (e["label"], parent if stype == "N" else "", name)
                tests = [("INITIAL", 1, True)]
                if (e["label"], loc, name) in REANALYSIS and stype == "N":
                    kind, dil = REANALYSIS[(e["label"], loc, name)]
                    tests = [("INITIAL", 1, False), (kind, dil, True)]
                for tt, dil, rep in tests:
                    vv = v
                    if v is not None and len(tests) == 2 and not rep:
                        vv = v * (0.93 if tt == "INITIAL" else 1.0) if loc != "LS-1" else min(v, 960.0)
                    anl = recv + dt.timedelta(days=int(r.integers(1, 6)) + (3 if tt != "INITIAL" and not rep else 0))
                    if lab == "A":
                        rows_a.append(edd_a_row(lab_id, loc, parent, ts, stype, group, name, cas, vv, unit, rl, frac,
                                                tt, dil, rep, anl, ei))
                    else:
                        rows_b.append(edd_b_row(lab_id, loc, parent, ts, stype, group, name, cas, vv, unit, rl, frac,
                                                tt, dil, rep, anl, ei))
        # Ridgeline's own batch QC: a matrix spike and spike duplicate on one well sample, and a method blank and a
        # blank spike per batch of each analysis group
        if lab == "B":
            ms_src = [x for x in plan[ei] if x[3] == "N" and x[0].startswith("MW")][(ei * 3 + 1) % 8]
            for qc in ("MS", "SD"):
                for group, name, cas, v, unit, rl, frac in results_for(ms_src, ei, r):
                    if group in ("surr", "ssurr", "pfas"):
                        continue
                    rec = r.uniform(78, 118)
                    rows_b.append(["%s-%s" % (qc, ms_src[0].replace("-", "") + ms_src[2].strftime("%Y%m%d")), "",
                                   ms_src[0], ms_src[2].strftime("%Y-%m-%d %H:%M"), qc, "WG",
                                   METHOD_B.get(group, "EPA 200.7") if group != "inorg" else [x for x in A.INORGANIC if x[0] == name][0][3],
                                   name, cas, frac, fmt(rec, 1), fmt(rec, 1), "%REC", "Y", "", "", "", "1", "INITIAL",
                                   "Yes", (recv + dt.timedelta(days=3)).strftime("%Y-%m-%d")])
            groups = [("metal", [(n, c, rl) for n, c, rl, _ in A.METALS])]
            if W.EVENTS[ei]["month"] == 10:
                groups.append(("svoc", [(n, c, 5.0) for n, c in A.SVOCS]))
            if EV.index(A.PFAS_FROM) <= ei:
                groups.append(("pfas", [(n, c, 2.0) for n, c in A.PFAS]))
            for group, lst in groups:
                for qc in ("LB", "BS"):
                    for name, cas, rl in lst:
                        v = None if qc == "LB" else r.uniform(75, 125)
                        rows_b.append(["%s-%s-%s" % (qc, recv.strftime("%y%m%d"), group.upper()), "", "",
                                       recv.strftime("%Y-%m-%d"), qc, "WQ", METHOD_B[group], name, cas,
                                       "T" if group == "metal" else "N", "" if v is None else fmt(v, 1),
                                       "" if v is None else fmt(v, 1), "%REC" if qc == "BS" else
                                       ("ug/L" if group != "pfas" else "ng/L"), "Y" if v is not None else "N",
                                       "" if qc == "BS" else sigstr(rl), "", "", "1", "INITIAL", "Yes",
                                       (recv + dt.timedelta(days=4)).strftime("%Y-%m-%d")])
            for qc in ("LB", "BS"):
                for name, cas, ma, mb, unit, rl, nat in A.INORGANIC:
                    v = None if qc == "LB" else r.uniform(92, 108)
                    rows_b.append(["%s-%s-%02d" % (qc, recv.strftime("%y%m%d"), 1), "", "", recv.strftime("%Y-%m-%d"),
                                   qc, "WQ", mb, name, cas, "D" if name in A.DISSOLVED else "N",
                                   "" if v is None else fmt(v, 1), "" if v is None else fmt(v, 1),
                                   "%REC" if qc == "BS" else unit, "Y" if v is not None else "N",
                                   "" if qc == "BS" else sigstr(rl), "", "", "1", "INITIAL", "Yes",
                                   (recv + dt.timedelta(days=2)).strftime("%Y-%m-%d")])
                for name, cas, rl in A.VOCS:
                    v = None if qc == "LB" else r.uniform(80, 120)
                    rows_b.append(["%s-%s-%02d" % (qc, recv.strftime("%y%m%d"), 2), "", "", recv.strftime("%Y-%m-%d"),
                                   qc, "WQ", "SW8260D", name, cas, "N", "" if v is None else fmt(v, 1),
                                   "" if v is None else fmt(v, 1), "%REC" if qc == "BS" else "ug/L",
                                   "Y" if v is not None else "N", "" if qc == "BS" else sigstr(rl), "", "", "1",
                                   "INITIAL", "Yes", (recv + dt.timedelta(days=3)).strftime("%Y-%m-%d")])
    head_a = ["Lab_Sample_ID", "Client_Sample_ID", "Location", "Sample_Date", "Sample_Time", "Matrix", "Sample_Type",
              "Method", "Parameter", "CAS_No", "Result", "Units", "RL", "MDL", "Qualifier", "Dilution", "Analysis_Date",
              "Reportable"]
    head_b = ["sys_sample_code", "lab_sample_id", "sys_loc_code", "sample_date", "sample_type_code", "matrix_code",
              "lab_anl_method_name", "chemical_name", "cas_rn", "fraction", "result_value", "result_text",
              "result_unit", "detect_flag", "reporting_detection_limit", "method_detection_limit", "lab_qualifiers",
              "dilution_factor", "test_type", "reportable_result", "analysis_date"]
    write_csv(os.path.join(tgt, FILES["edd_a"]), head_a, rows_a)
    write_csv(os.path.join(tgt, FILES["edd_b"]), head_b, rows_b, delim="\t")
    return len(rows_a), len(rows_b), plan


LOC_A = {"LS-1": "LEACHATE SUMP", "SW-1": "SW-01", "SW-2": "SW-02", "EB": "EQUIP BLANK", "TB": "TRIP BLANK"}


def loc_a(loc):
    if loc in LOC_A:
        return LOC_A[loc]
    if loc.startswith("MW-"):
        return "MW-%02d" % int(loc[3:]) if loc[3:].isdigit() else loc
    return loc


METHOD_A = {"metal": "EPA 200.8", "voc": "EPA 8260C", "surr": "EPA 8260C", "svoc": "EPA 8270D", "ssurr": "EPA 8270D",
            "pfas": "EPA 537.1"}
METHOD_B = {"metal": "EPA 200.8", "voc": "SW8260D", "surr": "SW8260D", "svoc": "SW8270E", "ssurr": "SW8270E",
            "pfas": "EPA 1633"}


def edd_a_row(lab_id, loc, parent, ts, stype, group, name, cas, v, unit, rl, frac, tt, dil, rep, anl, ei):
    """Tamarack: mg/L for every metal and for boron and sodium, the dissolved fraction in the parameter name,
    zero-padded well codes, a blind DUP code for the field duplicate, U for a non-detect"""
    pname = name
    u = unit
    val = v
    if group == "inorg":
        meth = [x for x in A.INORGANIC if x[0] == name][0][2]
        if name == "Boron":
            u = "mg/L"
            val = None if v is None else v / 1000.0
        if frac == "D":
            pname = name + ", Dissolved"
        elif frac == "T" and name == "Boron":
            pname = "Boron, Total"
    elif group == "metal":
        meth = METHOD_A[group]
        u = "mg/L"
        val = None if v is None else v / 1000.0
        rl = rl / 1000.0
        pname = name + (", Dissolved" if frac == "D" else ", Total")
    else:
        meth = METHOD_A[group]
    location = "DUP-1" if stype == "FD" else loc_a(loc)
    client = "MC-%s-%s" % (location.replace("-", "").replace(" ", ""), ts.strftime("%m%y"))
    matrix = {"LS-1": "LCH", "SW-1": "SW", "SW-2": "SW", "EB": "WQ", "TB": "WQ"}.get(loc, "GW")
    if val is None:
        res, qual = "", "U"
    else:
        if group == "inorg" and name == "Boron":
            res = fmt(val, 3)
        elif group == "metal":
            res = fmt(val, 4)
        elif group in ("inorg",):
            res = sigstr(val)
        else:
            res = sigstr(val)
        qual = ""
        if rl is not None and val < rl:
            qual = "J"
    rlv = "" if rl is None else (fmt(rl, 4) if u == "mg/L" and rl < 0.1 else sigstr(rl))
    return [lab_id, client, location, ts.strftime("%m/%d/%Y"), ts.strftime("%H:%M"), matrix, stype, meth, pname, cas,
            res, u, rlv, "", qual, str(dil), anl.strftime("%m/%d/%Y"), "Y" if rep else "N"]


def edd_b_row(lab_id, loc, parent, ts, stype, group, name, cas, v, unit, rl, frac, tt, dil, rep, anl, ei):
    """Ridgeline: EQuIS-style, ug/L for metals and boron, the fraction in its own column, the parent well's code on
    a field duplicate"""
    if group == "inorg":
        meth = [x for x in A.INORGANIC if x[0] == name][0][3]
    else:
        meth = METHOD_B[group]
    sloc = parent if stype == "FD" else ("" if stype in ("EB", "TB") else loc)
    code = "MCL-%s-%s" % ((sloc or stype).replace("-", ""), ts.strftime("%Y%m%d"))
    if stype == "FD":
        code = "MCL-DUP%02d-%s" % (ei % 7 + 1, ts.strftime("%Y%m%d"))
    matrix = {"LS-1": "LL", "SW-1": "SW", "SW-2": "SW"}.get(loc, "WG" if stype in ("N", "FD") else "WQ")
    if v is None:
        rv, rt, df, q = "", "<%s" % sigstr(rl if rl else 1.0), "N", "U"
    else:
        if group == "inorg" and name in ("Chloride", "Sodium", "Boron"):
            rv = sigstr(v)
        else:
            rv = sigstr(v)
        rt, df, q = rv, "Y", ""
        if rl is not None and v < rl:
            q = "J"
    return [code, lab_id, sloc, ts.strftime("%Y-%m-%d %H:%M"), stype, matrix, meth, name, cas, frac, rv, rt, unit, df,
            "" if rl is None else sigstr(rl), "" if rl is None else sigstr(rl * 0.3), q, str(dil), tt,
            "Yes" if rep else "No", anl.strftime("%Y-%m-%d")]


# ---------------------------------------------------------------- water levels and the point register
def write_gauging(tgt):
    r = rng(3)
    rows = []
    for ei, e in enumerate(W.EVENTS):
        day = e["days"][0]
        t = dt.datetime.combine(day, dt.time(8, int(r.integers(2, 20))))
        order = ["PZ-1", "MW-1", "PZ-2", "MW-2", "PZ-3", "MW-3", "MW-11", "MW-9", "MW-8", "MW-7", "MW-6", "PZ-4",
                 "MW-5" if ei < 9 else "MW-5R", "MW-4", "MW-10"]
        for p in order:
            if (p, ei) not in SIM["heads"]:
                continue
            h = SIM["heads"][(p, ei)]
            remark = ""
            if p == "MW-8" and ei == 13:
                remark = "riser reset after frost heave, measured from new top of casing"
            elif r.random() < 0.06:
                remark = r.choice(["lock replaced", "standing water in protective casing", "J-plug cracked, replaced",
                                   "ants in protective casing", "flush mount lid stiff"])
            rows.append([e["label"], p, day.strftime("%Y-%m-%d"), t.strftime("%H:%M"), fmt(h["dtw"], 2),
                         r.choice(["WC", "JM", "WC", "DR"]) if ei >= 6 else r.choice(["TS", "DR"]),
                         "SL-%d" % (1 if ei < 10 else 2), remark])
            t += dt.timedelta(minutes=float(r.uniform(6, 15)))
    write_csv(os.path.join(tgt, FILES["gauging"]), ["event", "location", "date", "time", "dtw_ft_btoc", "measured_by",
                                                    "sounder", "remarks"], rows)
    return len(rows)


def survey_rows():
    rows = []
    r = rng(4)
    for p, v in W.POINTS.items():
        toc = v[3] + v[4]
        installed = dt.date.fromisoformat(v[8])
        if installed.year < 2022:
            sdate = "2014-07-08" if installed.year == 2014 else "2017-09-19"
            rows.append([p, sdate, "NGVD 29", fmt(toc, 2), fmt(v[3], 2), "Hollis Land Surveying", ""])
        if p == "MW-5":
            continue
        t22 = toc + W.DATUM_SHIFT + r.normal(0, 0.004)
        rows.append([p, "2022-06-14", "NAVD 88", fmt(t22, 2), fmt(v[3] + W.DATUM_SHIFT, 2), "Driftless Survey Co.",
                     "network resurvey after MW-5R install" if p == "MW-5R" else ""])
        if p == "MW-8":
            rows.append([p, "2024-06-03", "NAVD 88", fmt(t22 - W.MW8_TRIM, 2), fmt(v[3] + W.DATUM_SHIFT, 2),
                         "Driftless Survey Co.", "riser trimmed after frost heave"])
    return rows


def write_points(tgt):
    wb = Workbook()
    ws = wb.active
    ws.title = "Points"
    ws.append(["point_id", "type", "program", "easting_ft", "northing_ft", "installed", "abandoned", "screen_top_ft_bgs",
               "screen_bottom_ft_bgs", "casing_dia_in", "notes"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for p, v in W.POINTS.items():
        role = {"background": "Background", "compliance": "Compliance", "piezometer": "Water level only"}[v[0]]
        ws.append([p, "Piezometer" if v[0] == "piezometer" else "Monitoring well", role, v[1], v[2], v[8],
                   "2022-05-10" if p == "MW-5" else None, v[5], v[6], v[7],
                   "replaced by MW-5R" if p == "MW-5" else ("replaces MW-5" if p == "MW-5R" else None)])
    ws2 = wb.create_sheet("Survey")
    ws2.append(["point_id", "survey_date", "vertical_datum", "toc_elev_ft", "ground_elev_ft", "surveyor", "note"])
    for c in ws2[1]:
        c.font = Font(bold=True)
    for row in survey_rows():
        ws2.append([row[0], row[1], row[2], float(row[3]), float(row[4]), row[5], row[6] or None])
    for wsx in (ws, ws2):
        for col in wsx.columns:
            wsx.column_dimensions[col[0].column_letter].width = max(10, min(36, max(len(str(c.value or "")) for c in col) + 2))
    wb.properties.creator = W.PEOPLE["hydrogeologist"]
    wb.save(os.path.join(tgt, FILES["points"]))


# ---------------------------------------------------------------- the sampler's purge entries (asks)
def write_purge(tgt):
    r = rng(5)
    rows = []
    for x in SIM["field_rows"]:
        utc = (x["time"] + dt.timedelta(hours=5)).strftime("%Y-%m-%dT%H:%M:%SZ")   # CDT to UTC in April and October
        if x["kind"] in ("decon", "bottles"):
            rows.append([x["day"].strftime("%Y-%m-%d"), x["location"], utc, "", fmt(x["counter_l"], 2), "", "", "", "",
                         "", "", "", "WC" if x["day"].weekday() != 2 else "JM",
                         "decon rinse" if x["kind"] == "decon" else "bottles filled, pump off"])
            continue
        meter = x["meter"]
        if x["event"] == W.EVAL and x["day"] == W.EVENTS[W.EVAL]["days"][2] and x["location"] in W.METER_UNPAIRED:
            meter = ""      # the app lost the meter's pairing after MW-9 on the third day; the meter was not changed
        rows.append([x["day"].strftime("%Y-%m-%d"), x["location"], utc, str(x["flow_ml_min"]), fmt(x["counter_l"], 2),
                     fmt(x["temp_c"], 1), str(x["spc"]), fmt(x["ph"], 2), fmt(x["do"], 2), str(x["orp"]),
                     fmt(x["turb"], 1), meter, "WC" if x["day"].weekday() != 2 else "JM", ""])
    write_csv(os.path.join(tgt, FILES["purge"]), ["visit_date", "location", "entry_utc", "flow_ml_min", "controller_l",
                                                  "temperature_c", "spc_us_cm", "ph_su", "do_mg_l", "orp_mv", "turb_ntu",
                                                  "meter_sn", "entered_by", "remark"], rows)
    return len(rows)


# ---------------------------------------------------------------- the field app's instrument calibration entries (asks)
CAL_HEAD = ["cal_date", "entry_utc", "meter_sn", "meter_model", "meter_owner", "sensor", "std_name", "std_lot",
            "std_temperature_c", "expected_value", "as_found", "as_left", "reading_units", "check_type", "cal_result",
            "cal_by"]


def write_calibration(tgt):
    """the sondes' morning calibrations and end-of-day checks for the April and October 2026 events, one entry per
    standard as the field app exports them: the standard's temperature, the value the sonde should read in the units
    it reports, and the reading as found and as left"""
    r = rng(12)
    days = {}
    for x in SIM["field_rows"]:
        d = days.setdefault((x["event"], x["day"]), {"first": x["time"], "last": x["time"], "meter": None})
        d["first"], d["last"] = min(d["first"], x["time"]), max(d["last"], x["time"])
        if x["kind"] == "reading":
            d["meter"] = x["meter"]
    lots = {}

    def lot(ei, std):
        if (ei, std) not in lots:
            yy = 25 if W.EVENTS[ei]["month"] == 4 else 26
            lots[(ei, std)] = "%02d%s%04d" % (yy, "ABCDEFGHJKLM"[int(r.integers(0, 12))], int(r.integers(1000, 9999)))
        return lots[(ei, std)]

    rows, seen = [], set()
    for (ei, day), d in sorted(days.items()):
        meter, by = d["meter"], ("WC" if day.weekday() != 2 else "JM")
        comp = W.COND_COMPENSATED[meter]
        third = day == W.EVENTS[ei]["days"][2]
        sessions = [("calibration", dt.datetime.combine(day, dt.time(7, 12)) + dt.timedelta(minutes=float(r.uniform(0, 28))),
                     r.uniform(11.5, 15.5) if W.EVENTS[ei]["month"] == 10 else r.uniform(10.0, 14.0))]
        eod = (dt.datetime.combine(day, dt.time(16, 4)) + dt.timedelta(minutes=float(r.uniform(0, 24))) if third
               else d["last"] + dt.timedelta(minutes=float(r.uniform(18, 44))))
        sessions.append(("end-of-day check", eod, r.uniform(16.0, 20.5)))
        for kind, t0, tstd in sessions:
            entries = []
            if kind == "calibration" and (ei, meter) not in seen:
                seen.add((ei, meter))
                ref = round(tstd + r.normal(0, 0.1), 1)
                entries.append(["Temperature", "reference thermometer TH-0213", "", fmt(ref, 1), fmt(ref, 1),
                                fmt(ref + r.normal(0, 0.1), 1), "", "C", "", "temperature check"])
            stds = [("pH", "pH 7.00 buffer", 7.0, 0.04), ("pH", "pH 4.00 buffer", 4.0, 0.05),
                    ("pH", "pH 10.00 buffer", 10.0, 0.07)] if kind == "calibration" else [("pH", "pH 7.00 buffer", 7.0, 0.05)]
            for sensor, name, val, sd in stds:
                T = round(tstd + r.normal(0, 0.15), 1)
                entries.append([sensor, name, lot(ei, name), fmt(T, 1), fmt(val, 2), fmt(val + r.normal(0, sd), 2),
                                fmt(val, 2) if kind == "calibration" else "", "SU", "Y", kind])
            T = round(tstd + r.normal(0, 0.15), 1)
            exp = W.KCL_STD_US_CM if comp else int(round(W.KCL_STD_US_CM * (1 + W.TEMP_COEF * (T - 25))))
            entries.append(["Conductivity", "KCl %d uS/cm at 25 C" % W.KCL_STD_US_CM, lot(ei, "KCl"), fmt(T, 1), str(exp),
                            str(int(round(exp * (1 + r.normal(0, 0.012 if kind == "calibration" else 0.006))))),
                            str(exp) if kind == "calibration" else "", "uS/cm at 25 C" if comp else "uS/cm",
                            "Y" if comp else "N", kind])
            if kind == "calibration":
                T = round(tstd + r.normal(0, 0.15), 1)
                sat = round(100.0 * r.uniform(733.0, 746.0) / 760.0, 1)
                entries.append(["Dissolved oxygen", "water-saturated air", "", fmt(T, 1), fmt(sat, 1),
                                fmt(sat * (1 + r.normal(0, 0.02)), 1), fmt(sat, 1), "% sat", "Y", kind])
                T = round(tstd + r.normal(0, 0.15), 1)
                orp = int(round(231 + 1.4 * (25 - T)))
                entries.append(["ORP", "Zobell solution", lot(ei, "Zobell"), fmt(T, 1), str(orp),
                                str(orp + int(round(r.normal(0, 6)))), str(orp), "mV", "N", kind])
                for val, sd in ((0.0, None), (124.0, 0.025)):
                    T = round(tstd + r.normal(0, 0.15), 1)
                    found = abs(r.normal(0.3, 0.15)) if sd is None else val * (1 + r.normal(0, sd))
                    name = "turbidity %d NTU" % val
                    entries.append(["Turbidity", name, lot(ei, name), fmt(T, 1), fmt(val, 1), fmt(found, 1), fmt(val, 1),
                                    "NTU", "", kind])
            t = t0
            for e in entries:
                utc = (t + dt.timedelta(hours=5)).strftime("%Y-%m-%dT%H:%M:%SZ")      # CDT to UTC in April and October
                # the export carries the reading units the sonde reports; the app keeps no separate compensation field
                rows.append([day.strftime("%Y-%m-%d"), utc, meter, W.SONDE_MODEL, W.SONDE_OWNER[meter]] + e[:8]
                            + [e[9], "pass", by])
                t += dt.timedelta(seconds=float(r.uniform(50, 160)))
    rows.sort(key=lambda x: x[1])
    write_csv(os.path.join(tgt, FILES["calib"]), CAL_HEAD, rows)
    return len(rows)


# ---------------------------------------------------------------- the program's neighbouring records (distractors)
def write_distractors(tgt):
    r = rng(6)
    rows = []
    probes = {"GP-1": 0.0, "GP-2": 0.0, "GP-3": 0.4, "GP-4": 0.0, "GP-5": 1.1, "GP-6": 0.0, "GP-7": 0.2, "GP-8": 0.0}
    d = dt.date(2025, 1, 14)
    while d <= dt.date(2026, 10, 20):
        baro = r.normal(29.92, 0.18)
        for p, base in probes.items():
            ch4 = max(0.0, base * math.exp(r.normal(0, 0.5)) - (0.0 if base else 0.0))
            rows.append([d.strftime("%Y-%m-%d"), p, fmt(ch4, 1), fmt(max(0.1, r.normal(2.4 + 3 * base, 0.8)), 1),
                         fmt(max(4.0, r.normal(17.8 - 2 * base, 1.1)), 1), fmt(r.normal(0.02, 0.03), 2), fmt(baro, 2),
                         "GEM5000 G503112"])
        d += dt.timedelta(days=int(28 + r.integers(0, 9)))
    write_csv(os.path.join(tgt, FILES["gas"]), ["date", "probe", "ch4_pct_vol", "co2_pct_vol", "o2_pct_vol",
                                                "static_pressure_inh2o", "baro_inhg", "instrument"], rows)
    data = []
    d = dt.date(2018, 1, 1)
    while d <= dt.date(2026, 10, 31):
        wet = 0.32 if d.month in (4, 5, 6, 7, 8, 9) else 0.22
        lab = "%d-%s" % (d.year, "OCT" if d.month >= 7 else "APR")
        if lab in W.DRY and d.month in (7, 8, 9):
            wet *= 0.45
        v = r.exponential(0.32) if r.random() < wet else 0.0
        val = "T" if 0 < v < 0.01 else ("%.2f" % v)
        if r.random() < 0.004:
            val = "M"
        data.append([d.strftime("%Y-%m-%d"), val])
        d += dt.timedelta(days=1)
    js = {"meta": {"uid": 31877, "name": "HOLLIS 2 NE", "state": "WI", "elev": 1104.0, "sids": ["474912 2", "USC00474912 6"]},
          "data": data}
    with open(os.path.join(tgt, FILES["precip"]), "w", encoding="utf-8") as f:
        json.dump(js, f, separators=(",", ":"))
    wb = Workbook()
    ws = wb.active
    ws.title = "Inspections"
    ws.append(["date", "inspector", "item", "condition", "action"])
    for c in ws[1]:
        c.font = Font(bold=True)
    d = dt.date(2024, 1, 22)
    items = ["final cover", "vegetation", "drainage swales", "leachate sump LS-1", "gas probes", "monitoring wells",
             "perimeter fence", "access road"]
    while d <= dt.date(2026, 10, 15):
        for it in items:
            cond, act = "good", ""
            if it == "drainage swales" and r.random() < 0.3:
                cond, act = "minor erosion at outlet", "rip-rap added"
            if it == "monitoring wells" and d.year == 2024 and d.month in (4, 5):
                cond, act = "MW-8 protective casing heaved", "casing reset, riser trimmed 5/21"
            if it == "final cover" and r.random() < 0.2:
                cond, act = "animal burrows north slope", "backfilled"
            if it == "leachate sump LS-1" and r.random() < 0.15:
                cond, act = "pump 2 tripped", "reset by operator"
            ws.append([d.strftime("%Y-%m-%d"), r.choice(["K. Bonilla", "D. Ruiz", "K. Bonilla"]), it, cond, act or None])
        d += dt.timedelta(days=int(85 + r.integers(0, 14)))
    wb.save(os.path.join(tgt, FILES["inspect"]))
    return len(rows), len(data)


SIM = None
LCK = None


def cut(tgt, S):
    global SIM, LCK
    SIM = S
    LCK = leachate_and_creek(rng(7))
    na, nb, plan = write_edds(tgt)
    ng = write_gauging(tgt)
    write_points(tgt)
    npg = write_purge(tgt)
    write_distractors(tgt)
    ncal = write_calibration(tgt)
    return {"edd_a_rows": na, "edd_b_rows": nb, "gauging_rows": ng, "purge_rows": npg, "calib_rows": ncal, "plan": plan}
