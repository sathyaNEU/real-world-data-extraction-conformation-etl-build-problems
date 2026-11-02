"""Write the pack under target/ from the world simulation.  python3 generator/build.py [outdir]"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W      # noqa: E402
import docs            # noqa: E402
import common          # noqa: E402

TASK = os.path.dirname(HERE)
OPCS_TEXT = {"J183": "Laparoscopic cholecystectomy", "T202": "Inguinal hernia repair (mesh)", "T204": "Inguinal hernia repair (laparoscopic)",
             "T241": "Umbilical hernia repair", "H511": "Haemorrhoidectomy", "H581": "Excision of pilonidal sinus",
             "S061": "Excision of skin lesion", "T962": "Excision of lipoma", "H562": "Lateral internal sphincterotomy"}
EM_OTHER = [("K35.8", 0.13), ("R10.4", 0.17), ("R10.1", 0.06), ("K56.6", 0.07), ("K57.3", 0.08), ("K40.3", 0.03),
            ("L02.2", 0.07), ("K61.0", 0.06), ("K92.2", 0.04), ("N39.0", 0.03), ("T81.4", 0.03), ("K59.0", 0.05),
            ("K29.7", 0.04), ("K85.2", 0.03), ("K85.9", 0.02), ("K82.8", 0.01), ("K91.5", 0.01), ("K63.1", 0.02),
            ("C18.7", 0.03), ("S36.1", 0.02)]
METHOD_TEXT = {"21": "Emergency - A&E", "22": "Emergency - GP", "28": "Emergency - other", "2A": "Emergency - SDEC",
               "11": "Elective - waiting list", "13": "Elective - planned"}


def legacy(site, date):
    return site == "FEN" and date < W.MIGRATION


def icd(code, leg, rng):
    c = code.replace(".", "")
    if leg:
        return c if rng.random() < 0.9 else c + "X"
    return code if rng.random() < 0.93 else (code + ("0" if rng.random() < 0.5 else " D"))


def build(out):
    os.makedirs(out, exist_ok=True)
    S = W.simulate()
    rng = np.random.default_rng(W.SEED + 1)
    persons = S["persons"]
    nper = len(persons)
    epr = rng.choice(np.arange(1_000_000, 9_999_999), size=nper + 70000, replace=False)
    fnum = rng.choice(np.arange(100_000, 999_999), size=nper + 70000, replace=False)
    epr_no = lambda pid: "M%07d" % epr[pid]
    f_no = lambda pid: "F%06d" % fnum[pid]
    used_f = set()

    def hosp_no(pid, site, date):
        if legacy(site, date):
            used_f.add(pid)
            return f_no(pid)
        return epr_no(pid)

    rec_end = W.RECORD_END
    # ---------------------------------------------------------------- filler spells (other general surgery activity)
    spells = [s for s in S["spells"] if s["admit"] <= rec_end]
    codes, pr = zip(*EM_OTHER)
    pr = np.array(pr) / sum(pr)
    for m in range(W.REC_MONTHS):
        for _ in range(rng.poisson(430 * W.SCALE * W.season(m) ** 0.3)):
            pid = len(persons)
            persons.append({"id": pid, "sex": "F" if rng.random() < 0.5 else "M", "age0": int(np.clip(rng.normal(52, 21), 16, 97)),
                            "district": "Marlstead" if rng.random() < 0.57 else ("Coldvale" if rng.random() < 0.93 else "Other")})
            site = "MGH" if (rng.random() < (0.9 if persons[pid]["district"] == "Marlstead" else 0.2)) else "FEN"
            adm = W.month_date(m) + dt.timedelta(days=int(rng.integers(0, 28)))
            los = int(rng.choice([0, 0, 1, 2, 3, 4, 6, 9, 14]))
            spells.append({"kind": "EM_OT", "site": site, "person": pid, "admit": adm, "discharge": adm + dt.timedelta(days=los),
                           "dx": str(rng.choice(codes, p=pr)), "proc": None, "route": str(rng.choice(["AE", "AE", "GP", "SDEC"])), "spec": "100"})
        for _ in range(rng.poisson(160 * W.SCALE)):
            pid = len(persons)
            persons.append({"id": pid, "sex": "F" if rng.random() < 0.5 else "M", "age0": int(np.clip(rng.normal(58, 16), 18, 95)),
                            "district": "Marlstead" if rng.random() < 0.58 else "Coldvale"})
            site = "MGH" if rng.random() < 0.55 else "FEN"
            adm = W.month_date(m) + dt.timedelta(days=int(rng.integers(0, 28)))
            spells.append({"kind": "EL_PL", "site": site, "person": pid, "admit": adm, "discharge": adm,
                           "dx": str(rng.choice(["Z09.0", "K62.1", "D12.6", "Z98.8"])), "proc": str(rng.choice(["H251", "H221", "T962"])),
                           "route": "PL", "spec": "100", "dc": True})
    spells.sort(key=lambda s: (s["admit"], s["site"], s["person"]))
    # ---------------------------------------------------------------- episodes
    rows = []
    spell_seq = {"MGH": 4_100_000, "FEN": 880_000}
    for s in spells:
        p = persons[s["person"]]
        leg = legacy(s["site"], s["admit"])
        spell_seq[s["site"]] += int(rng.integers(1, 4))
        spno = ("FS%07d" if leg else "SP%08d") % (spell_seq[s["site"]] + (0 if leg else 20_000_000 if s["site"] == "FEN" else 0))
        age = int(p["age0"] + (s["admit"] - W.M0).days / 365.25)
        meth = {"AE": "21", "GP": "22", "SDEC": "2A" if not leg else "21", "WL": "11", "PL": "13"}[s["route"]]
        if s["kind"] in ("EM_GS", "EM_OT") and rng.random() < 0.03:
            meth = "28"
        meth_out = meth if leg else METHOD_TEXT[meth]
        los = (s["discharge"] - s["admit"]).days
        n_ep = 1 if los <= 1 or s["kind"].startswith("EL") else min(los, int(rng.choice([1, 1, 2, 2, 3])))
        cuts = sorted(rng.choice(np.arange(1, los), size=n_ep - 1, replace=False)) if n_ep > 1 else []
        bounds = [0] + [int(c) for c in cuts] + [los]
        for e in range(n_ep):
            st, en = s["admit"] + dt.timedelta(days=bounds[e]), s["admit"] + dt.timedelta(days=bounds[e + 1])
            if e == 0:
                dx = s["dx"]
                tf = s.get("spec", "100")
            else:
                dx = s["dx"] if rng.random() < 0.7 else str(rng.choice(["R10.1", "K80.2", "E87.1", "J18.9", "N17.9"])) if s["kind"] == "EM_GS" else s["dx"]
                tf = str(rng.choice(["100", "100", "301", "430"]))
            proc = s["proc"] if (s["proc"] and e == n_ep - 1) else None
            pdate = None
            if proc:
                pdate = st if s["kind"].startswith("EL") else st + dt.timedelta(days=int(rng.integers(0, max(1, (en - st).days) + 1)))
                pdate = min(pdate, en)
            if s["kind"].startswith("EL"):
                pc = "2" if s.get("dc") or s["kind"] == "EL_CANC" else "1"
            else:
                pc = "1"
            rows.append({
                "provider_spell_no": spno, "episode_no": e + 1,
                "hospital_number": hosp_no(p["id"], s["site"], s["admit"]),
                "site_code": {"MGH": "MGH01", "FEN": "FEN01"}[s["site"]] if not leg else "FENH",
                "sex": {"F": "2", "M": "1"}[p["sex"]] if leg else ("Female" if p["sex"] == "F" else "Male"),
                "age_on_admission": age, "la_of_residence": p["district"] if p["district"] != "Other" else "Out of area",
                "admission_method": meth_out, "admission_date": s["admit"].isoformat(),
                "episode_start_date": st.isoformat(), "episode_end_date": en.isoformat(),
                "discharge_date": s["discharge"].isoformat() if e == n_ep - 1 else "",
                "treatment_function_code": tf, "patient_classification": pc,
                "primary_diagnosis": icd(dx, leg, rng),
                "primary_procedure": (proc[:3] + "." + proc[3:] if not leg else proc) if proc else "",
                "procedure_date": pdate.isoformat() if pdate else ""})
    ep = pd.DataFrame(rows)
    ep = ep[pd.to_datetime(ep.episode_start_date) <= pd.Timestamp(rec_end)]
    ep.loc[pd.to_datetime(ep.discharge_date.replace("", None)) > pd.Timestamp(rec_end), "discharge_date"] = ""
    ep.loc[pd.to_datetime(ep.episode_end_date) > pd.Timestamp(rec_end), "episode_end_date"] = ""
    ep.loc[pd.to_datetime(ep.procedure_date.replace("", None)) > pd.Timestamp(rec_end), ["procedure_date", "primary_procedure"]] = ""
    ep.to_csv(os.path.join(out, "pas_inpatient_episodes_2021_2026.csv"), index=False)

    # ---------------------------------------------------------------- ED attendances with abdominal pain (ECDS extract)
    ed = []
    cc = ["Abdominal pain", "Abdominal pain", "Vomiting", "Jaundice", "Back pain"]
    dxs = [("Biliary colic", 0.10), ("Abdominal pain", 0.48), ("Constipation", 0.10), ("Gastritis", 0.08), ("Urinary tract infection", 0.08),
           ("Renal colic", 0.07), ("Gastroenteritis", 0.09)]
    dn, dp = zip(*dxs)
    dp = np.array(dp) / sum(dp)
    for s in spells:
        if s["route"] == "AE" and s["admit"] >= dt.date(2023, 4, 1):
            ed.append((s["admit"], s["site"], s["person"], "Admitted", "Biliary colic" if s["dx"].startswith(("K80", "K81", "K83")) else
                       ("Acute pancreatitis" if s["dx"].startswith("K85") else str(rng.choice(dn, p=dp)))))
    for m in range(24, W.REC_MONTHS):
        for _ in range(rng.poisson(640 * W.SCALE)):
            pid = len(persons)
            persons.append({"id": pid, "sex": "F" if rng.random() < 0.55 else "M", "age0": int(np.clip(rng.normal(41, 19), 16, 97)), "district": "Marlstead"})
            ed.append((W.month_date(m) + dt.timedelta(days=int(rng.integers(0, 28))), "MGH" if rng.random() < 0.62 else "FEN", pid,
                       str(rng.choice(["Discharged - no follow up", "Discharged - GP follow up", "Discharged - clinic follow up", "Left before treatment"],
                                      p=[0.42, 0.36, 0.14, 0.08])), str(rng.choice(dn, p=dp))))
    ed.sort(key=lambda r: (r[0], r[1], r[2]))
    edr = []
    for i, (d, site, pid, dest, dxn) in enumerate(ed):
        t = dt.datetime.combine(d, dt.time(0, 0)) + dt.timedelta(minutes=int(rng.integers(0, 1440)))
        edr.append({"attendance_ref": "ED%s%07d" % (site[0], 1_000_000 + i), "arrival_time": t.strftime("%Y-%m-%d %H:%M"),
                    "department": {"MGH": "Marlstead General ED", "FEN": "Fennick ED"}[site],
                    "hospital_number": epr_no(pid), "chief_complaint": str(rng.choice(cc)), "diagnosis": dxn, "discharge_destination": dest})
    pd.DataFrame(edr).to_csv(os.path.join(out, "ecds_abdominal_pain_attendances_2023_2026.csv"), index=False)

    # ---------------------------------------------------------------- theatre case log, April 2024 onwards
    th = []
    for s in spells:
        if s["proc"] and s["admit"] >= dt.date(2024, 4, 1) and s["kind"] != "EL_PL":
            st = dt.datetime.combine(s["admit"] if s["kind"].startswith("EL") else s["admit"] + dt.timedelta(days=1),
                                     dt.time(8 if s["kind"].startswith("EL") else 13, 30)) + dt.timedelta(minutes=int(rng.integers(0, 300)))
            dur = int(rng.normal(62 if s["proc"] == "J183" else 48, 14))
            th.append({"case_ref": "", "session_date": st.date().isoformat(), "theatre": ("MGH-T%d" if s["site"] == "MGH" else "FEN-T%d") % int(rng.integers(1, 6)),
                       "hospital_number": epr_no(s["person"]), "procedure": OPCS_TEXT.get(s["proc"], s["proc"]),
                       "urgency": "Elective" if s["kind"].startswith("EL") else "Emergency (NCEPOD 2B)",
                       "knife_to_skin": st.strftime("%H:%M"), "closure": (st + dt.timedelta(minutes=max(dur, 20))).strftime("%H:%M")})
    th = [r for r in th if r["session_date"] <= rec_end.isoformat()]
    th = pd.DataFrame(th).sort_values(["session_date", "theatre", "knife_to_skin"]).reset_index(drop=True)
    th["case_ref"] = ["TC%06d" % (200_000 + i) for i in range(len(th))]
    th.to_csv(os.path.join(out, "theatre_case_log_2024_2026.csv"), index=False)

    # ---------------------------------------------------------------- PTL snapshots
    pws = S["pathways"]
    pid_fen_seq, pid_epr_seq = {}, {}
    ptl = []
    ers = {r["ubrn"]: r for r in S["referrals"]}
    for m in range(W.REC_MONTHS):
        snap = W.month_end(m)
        for pw in pws:
            if pw["added"] > snap:
                continue
            end = pw.get("stale_until") or pw["removed"]
            if end is not None and end <= snap:
                continue
            leg = legacy(pw["site"], snap)
            if leg:
                pwid = "FPW%06d" % (300_000 + pw["id"])
            else:
                pwid = "PW%07d" % (5_000_000 + pw["id"] * 3)
            clock = pw["clock"]
            if pw["site"] == "FEN" and pw["ubrn"] and pw["added"] >= W.MIGRATION and pw.get("first_appt"):
                clock = pw["first_appt"]             # Fennick's EPR build reads the clock off the first appointment
            if pw.get("moved_from") is not None:
                src = pws[pw["moved_from"]]
                if src["ubrn"] and src["added"] >= W.MIGRATION and src.get("first_appt"):
                    clock = src["first_appt"]        # the moved pathway carries the clock the Fennick record held
            tci = ""
            if pw["removed"] is not None and pw["reason"] in ("treated_elective", "cancelled_relisted") and (pw["removed"] - snap).days <= 42:
                tci = pw["removed"].isoformat()
            ptl.append({"snapshot_date": snap.isoformat(), "site": pw["site"] if not leg else "FENH",
                        "pathway_id": pwid, "hospital_number": hosp_no(pw["person"], pw["site"], snap),
                        "ubrn": pw["ubrn"] or "", "specialty": "100" if not leg else "GS",
                        "planned_procedure": OPCS_TEXT[pw["opcs"]], "opcs_code": pw["opcs"],
                        "priority": pw["priority"], "date_added": pw["added"].isoformat(),
                        "rtt_clock_start": clock.isoformat() if clock else "", "tci_date": tci})
    ptl = pd.DataFrame(ptl)
    ptl.to_parquet(os.path.join(out, "admitted_ptl_snapshots_2021_2026.parquet"), index=False, compression="snappy")

    # ---------------------------------------------------------------- e-RS referrals
    er = []
    svc = {"chole": "Upper GI and Hepatobiliary Surgery", "hernia": "Hernia and Abdominal Wall Surgery", "other": "General Surgery"}
    for r in S["referrals"]:
        if r["received"] > rec_end or r["received"] < W.M0 - dt.timedelta(days=900):
            continue
        er.append({"ubrn": r["ubrn"], "referral_received": r["received"].isoformat(),
                   "service": "%s - %s" % (svc[r["group"]], {"MGH": "Marlstead General", "FEN": "Fennick"}[r["site"]]),
                   "referral_priority": r["priority"],
                   "first_appointment_date": r["appt"].isoformat() if r["appt"] <= rec_end else ""})
    er = pd.DataFrame(er).sort_values(["referral_received", "ubrn"])
    er.to_csv(os.path.join(out, "ers_referrals_general_surgery_2019_2026.csv"), index=False)

    # ---------------------------------------------------------------- crosswalk
    cw = pd.DataFrame({"fennick_pas_number": [f_no(i) for i in sorted(used_f)], "epr_hospital_number": [epr_no(i) for i in sorted(used_f)]})
    cw.to_csv(os.path.join(out, "fennick_pas_to_epr_number_map.csv"), index=False)

    # ---------------------------------------------------------------- population
    pop = S["pop"]
    with pd.ExcelWriter(os.path.join(out, "population_mid_year_estimates_2018_2025.xlsx")) as xw:
        for d in W.DISTRICTS:
            t = []
            for yr in range(2018, 2026):
                for s in ("F", "M"):
                    t.append([yr, "Females" if s == "F" else "Males"] + list(pop.at(d, s, yr, "est")))
            pd.DataFrame(t, columns=["mid_year", "sex"] + W.BANDS).to_excel(xw, sheet_name=d, index=False)
    with pd.ExcelWriter(os.path.join(out, "population_projections_2022_based.xlsx")) as xw:
        for d in W.DISTRICTS:
            t = []
            for yr in range(2022, 2033):
                for s in ("F", "M"):
                    t.append([yr, "Females" if s == "F" else "Males"] + list(pop.at(d, s, yr, "proj")))
            pd.DataFrame(t, columns=["mid_year", "sex"] + W.BANDS).to_excel(xw, sheet_name=d, index=False)

    # ---------------------------------------------------------------- the plan's trajectory, from the simulated future
    traj = {}
    for m in range(W.REC_MONTHS, W.N_MONTHS):
        snap = W.month_end(m)
        for g in ("chole", "hernia", "other"):
            n = sum(1 for pw in pws if pw["group"] == g and pw["added"] <= snap and (pw["removed"] is None or pw["removed"] > snap))
            traj[(g, snap)] = int(round(n / 10.0) * 10)
    S["traj"] = traj
    docs.write_all(out, S)
    for f in ("population_mid_year_estimates_2018_2025.xlsx", "population_projections_2022_based.xlsx"):
        common.freeze_xlsx(os.path.join(out, f), "Population Analysis Team")
    return S


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    build(out)
    print("built", out)
