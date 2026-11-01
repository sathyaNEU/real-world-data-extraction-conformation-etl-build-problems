"""task146 architecture 3: write the VELA-2 exports, the feasibility workbook and the documents into target/."""
import csv
import datetime as dt
import math
import os
from zoneinfo import ZoneInfo

import numpy as np
from openpyxl import Workbook

import postprocess as PP
import world as W

FILES = {
    "subjects": "vela2_subjects.csv",
    "dosing": "vela2_dosing_log.csv",
    "pasi": "vela2_pasi_assessments.csv",
    "pk": "vela2_pk_trough_samples.csv",
    "cm": "vela2_concomitant_medications.csv",
    "epro": "vela2_epro_diary.csv",
    "ae": "vela2_adverse_events.csv",
    "dlqi": "vela2_dlqi.csv",
    "sites": "vela2_sites.csv",
    "feas": "vela3_feasibility_survey_2026.xlsx",
    "sap": "vela2_statistical_analysis_plan_v2.0.pdf",
    "cdp": "hb231_clinical_development_plan_v2.1_section7.pdf",
    "email": "hb231_phase3_dose_request.eml",
}
DISTRACTORS = ("ae", "dlqi")
VISITS = [("Week 2", 14), ("Week 4", 28), ("Week 8", 56), ("Week 12", 84), ("Week 16", 112)]
UTC = ZoneInfo("UTC")


def _w(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(head)
        wr.writerows(rows)
    return len(rows)


class Records:
    """Everything the exports hold, drawn once from the world so every file agrees."""

    def __init__(self, w):
        self.w = w
        r = np.random.default_rng(W.SEED + 7)
        self.r = r
        seq = {}
        for p in w.pat:
            seq[p["site"]] = seq.get(p["site"], 0) + 1
            p["sid"] = "201-%s-%03d" % (p["site"], seq[p["site"]])
            p["scr"] = "S%05d" % (10000 + 37 * p["i"] + int(r.integers(0, 30)))
            # the visit calendar from the first dose; a discontinued patient leaves between week 4 and week 12
            p["leave"] = int(r.choice([28, 56, 84])) if p["disc"] else None
            p["scr_date"] = p["d1"] - dt.timedelta(days=int(r.integers(14, 29)))
            # a washout of prior topical treatment lets the plaques flare between screening and the first dose
            p["pasi_scr"] = p["pasi0"] * float(np.exp(r.normal(-0.30, 0.07)))
            p["vdates"] = {}
            for name, day in VISITS:
                if p["leave"] is not None and day > p["leave"]:
                    break
                p["vdates"][name] = p["d1"] + dt.timedelta(days=day + int(r.integers(-3, 4)))
            p["resc_day"] = int(r.integers(30, 105)) if p["resc"] else None
            p["doses"] = [p["d1"] + dt.timedelta(days=28 * k + (int(r.integers(-2, 3)) if k else 0))
                          for k in range(4) if p["leave"] is None or 28 * k < p["leave"]]

    def pasi_at(self, p, day):
        """PASI on a study day, the improvement building to week 16."""
        f = min(1.0, max(0.0, day / 84.0)) ** 0.7
        return max(0.0, p["pasi0"] * (1 - p["imp16"] * f))


def fmt_pasi(p, v):
    return "%d" % int(round(v)) if p["pasi_fmt"] == "int" else "%.1f" % v


def write_subjects(R, path):
    rows = []
    for p in R.w.pat:
        disp = "Discontinued" if p["disc"] else "Ongoing"
        ddate = (p["d1"] + dt.timedelta(days=p["leave"] + 9)).isoformat() if p["disc"] else ""
        reason = "" if not p["disc"] else ["Lack of efficacy", "Withdrawal by subject", "Adverse event",
                                           "Lost to follow-up"][p["i"] % 4]
        rows.append([p["sid"], p["scr"], p["site"], p["country"], p["arm"], p["rdate"].isoformat(), p["sex"],
                     p["age"], "%.1f" % p["weight"], "%.0f" % p["height"], "Y" if p["prior_bio"] else "N", disp,
                     ddate, reason])
    return _w(path, ["subject_id", "screening_no", "site", "country", "arm", "randomisation_date", "sex", "age",
                     "weight_kg", "height_cm", "prior_biologic", "status_at_lock", "discontinuation_date",
                     "discontinuation_reason"], rows)


def write_dosing(R, path):
    rows = []
    kit = 40000
    for p in R.w.pat:
        for k, d in enumerate(p["doses"]):
            kit += int(R.r.integers(1, 9))
            rows.append([p["sid"], k + 1, d.isoformat(), "K%06d" % kit, "Administered"])
    rows.sort(key=lambda x: (x[2], x[0]))
    return _w(path, ["subject_id", "dose_number", "dose_date", "kit_number", "status"], rows)


def write_pasi(R, path):
    rows = []
    r = R.r
    for p in R.w.pat:
        fi = p["ecrf"] == "fi"
        # the Finnish sites' eCRF build labels the screening assessment "Baseline" and the first-dose one "Day 1"
        rows.append([p["sid"], "Baseline" if fi else "Screening", p["scr_date"].isoformat(),
                     fmt_pasi(p, p["pasi_scr"]), "%d" % int(round(p["pasi_scr"] * 1.3)), 3 if p["pasi_scr"] < 20 else 4])
        rows.append([p["sid"], "Day 1" if fi else "Baseline", p["d1"].isoformat(), fmt_pasi(p, p["pasi0"]),
                     "%d" % int(round(p["pasi0"] * 1.3)), 3 if p["pasi0"] < 20 else 4])
        for name, day in VISITS:
            if name not in p["vdates"]:
                break
            if name == "Week 16":
                v = p["pasi0"] * (1 - p["imp16"])
            else:
                v = R.pasi_at(p, day) * float(np.exp(r.normal(0, 0.06)))
            iga = 0 if v < 1 else 1 if v < 4 else 2 if v < 10 else 3
            rows.append([p["sid"], name, p["vdates"][name].isoformat(), fmt_pasi(p, max(0.0, v)),
                         "%d" % int(round(max(0.0, v) * 1.3)), iga])
    return _w(path, ["subject_id", "visit", "assessment_date", "pasi_total", "bsa_percent", "iga"], rows)


def write_pk(R, path):
    rows = []
    r = R.r
    for p in R.w.pat:
        lund = p["site"] == "SE05"
        for wk in (4, 8, 12, 16):
            name = "Week %d" % wk
            if name not in p["vdates"]:
                continue
            if p["dose"] == 0:
                c = 0.0
            else:
                c = p["dose"] * W.ACC[wk] / (p["cl"] * 28.0) * float(np.exp(r.normal(0, W.RESID)))
            t = "%02d:%02d" % (int(r.integers(7, 12)), int(r.integers(0, 60)))
            if c < W.LLOQ:
                val, unit = ("<100" if lund else "<0.10"), ("ng/mL" if lund else "ug/mL")
            elif lund:
                val, unit = "%.0f" % (c * 1000), "ng/mL"
            else:
                val, unit = "%.2f" % c, "ug/mL"
            rows.append([p["sid"], name, p["vdates"][name].isoformat(), t, val, unit,
                         "Lund University Hospital Clinical Chemistry" if lund else "Nordic Bioanalytical Central Lab"])
    return _w(path, ["subject_id", "visit", "sample_date", "sample_time", "concentration", "unit", "laboratory"], rows)


BACKGROUND = [("Atorvastatin", "C10AA05", "Hypercholesterolaemia"), ("Metformin", "A10BA02", "Type 2 diabetes"),
              ("Amlodipine", "C08CA01", "Hypertension"), ("Paracetamol", "N02BE01", "Pain"),
              ("Cetirizine", "R06AE07", "Allergic rhinitis"), ("Levothyroxine", "H03AA01", "Hypothyroidism"),
              ("Emollient cream", "D02AX", "Dry skin"), ("Omeprazole", "A02BC01", "Dyspepsia")]
RESCUE = [("Clobetasol propionate 0.05% cream", "D07AD01", "Psoriasis flare"),
          ("Betamethasone dipropionate 0.05% ointment", "D07AC01", "Psoriasis flare"),
          ("Narrowband UVB phototherapy", "", "Psoriasis")]


def _dmy(d, ctry):
    return d.strftime("%d.%m.%Y") if ctry in ("FI", "NO") else d.isoformat()


def write_cm(R, path):
    rows = []
    r = R.r
    for p in R.w.pat:
        for _ in range(int(r.integers(0, 3))):
            m = BACKGROUND[int(r.integers(0, len(BACKGROUND)))]
            st = p["d1"] - dt.timedelta(days=int(r.integers(30, 2000)))
            rows.append([p["sid"], m[0], m[1], m[2], _dmy(st, p["country"]), "Ongoing"])
        if p["resc"]:
            m = RESCUE[int(r.integers(0, len(RESCUE)))]
            st = p["d1"] + dt.timedelta(days=p["resc_day"])
            rows.append([p["sid"], m[0], m[1], m[2], _dmy(st, p["country"]),
                         _dmy(st + dt.timedelta(days=int(r.integers(10, 40))), p["country"])])
        # a mild topical for the scalp before the first dose, outside the rescue window
        if r.random() < 0.18:
            st = p["d1"] - dt.timedelta(days=int(r.integers(40, 300)))
            rows.append([p["sid"], "Hydrocortisone 1% cream", "D07AA02", "Psoriasis (face)", _dmy(st, p["country"]),
                         _dmy(st + dt.timedelta(days=int(r.integers(5, 25))), p["country"])])
    return _w(path, ["subject_id", "medication", "atc_code", "indication", "start_date", "stop_date"], rows)


def itch_base(p, R):
    return float(min(9.6, max(2.0, R.r.normal(6.6, 1.5))))


def write_epro(R, path):
    rows = []
    r = R.r
    for p in R.w.pat:
        tz = ZoneInfo(p["tz"])
        b = itch_base(p, R)
        last = 112 if p["leave"] is None else p["leave"] + 4
        miss = 0.10 + 0.08 * r.random()
        for day in range(-10, last + 1):
            if r.random() < miss:
                continue
            f = min(1.0, max(0.0, day / 70.0)) ** 0.8
            gain = 5.6 * max(-0.1, p["imp16"]) * f + (0.6 if day > 3 else 0.0)
            itch = int(round(min(10, max(0, b - gain + r.normal(0, 1.1)))))
            sleep = int(round(min(10, max(0, 0.7 * itch + r.normal(0, 1.2)))))
            ldate = p["d1"] + dt.timedelta(days=day)
            # the evening diary opens at 19:00; about one entry in six is completed after midnight
            if r.random() < 0.16:
                t = dt.datetime.combine(ldate + dt.timedelta(days=1), dt.time(0, 0)) + dt.timedelta(
                    minutes=int(r.integers(5, 170)))
            else:
                t = dt.datetime.combine(ldate, dt.time(19, 0)) + dt.timedelta(minutes=int(r.integers(0, 290)))
            u = t.replace(tzinfo=tz).astimezone(UTC)
            rows.append([p["sid"], u.strftime("%Y-%m-%dT%H:%M:%SZ"), itch, sleep])
    rows.sort(key=lambda x: (x[1], x[0]))
    return _w(path, ["subject_id", "entry_utc", "itch_nrs", "sleep_nrs"], rows)


def write_ae(R, path):
    rows = []
    r = R.r
    terms = [("Nasopharyngitis", "Infections and infestations"), ("Headache", "Nervous system disorders"),
             ("Injection site erythema", "General disorders and administration site conditions"),
             ("Upper respiratory tract infection", "Infections and infestations"),
             ("Arthralgia", "Musculoskeletal and connective tissue disorders"),
             ("Fatigue", "General disorders and administration site conditions"),
             ("Diarrhoea", "Gastrointestinal disorders"), ("Tinea pedis", "Infections and infestations")]
    k = 0
    for p in R.w.pat:
        for _ in range(int(r.poisson(0.9))):
            t = terms[int(r.integers(0, len(terms)))]
            k += 1
            st = p["d1"] + dt.timedelta(days=int(r.integers(1, 112)))
            rows.append(["AE%05d" % k, p["sid"], t[0], t[1], st.isoformat(),
                         ["Mild", "Mild", "Moderate", "Severe"][int(r.integers(0, 4))], "N"])
    return _w(path, ["ae_id", "subject_id", "preferred_term", "system_organ_class", "onset_date", "severity",
                     "serious"], rows)


def write_dlqi(R, path):
    rows = []
    r = R.r
    for p in R.w.pat:
        base = int(min(30, max(2, r.normal(13, 5))))
        rows.append([p["sid"], "Baseline", p["d1"].isoformat(), base])
        if "Week 16" in p["vdates"]:
            v = int(max(0, round(base * (1 - 0.85 * max(0.0, p["imp16"])) + r.normal(0, 2))))
            rows.append([p["sid"], "Week 16", p["vdates"]["Week 16"].isoformat(), v])
    return _w(path, ["subject_id", "visit", "assessment_date", "dlqi_total"], rows)


def write_sites(R, path):
    rows = [[s[0], s[1], s[2], s[3]] for s in W.SITES]
    return _w(path, ["site", "country", "city", "time_zone"], rows)


def write_feas(R, path):
    wb = Workbook()
    us = wb.active
    us.title = "US sites"
    ca = wb.create_sheet("Canadian sites")
    us.append(["Site", "Candidate ref", "Sex", "Age", "Weight (lb)", "PASI", "Prior biologic"])
    ca.append(["Site", "Candidate ref", "Sex", "Age", "Weight (kg)", "PASI", "Prior biologic"])
    n = {}
    for c in R.w.cand:
        n[c["site"]] = n.get(c["site"], 0) + 1
        ref = "%s-%03d" % (c["site"], n[c["site"]])
        if c["country"] == "US":
            us.append([c["site"], ref, c["sex"], c["age"], int(round(c["weight"] / 0.45359237)),
                       round(c["pasi"], 1), "Yes" if c["prior_bio"] else "No"])
        else:
            ca.append([c["site"], ref, c["sex"], c["age"], round(c["weight"], 1), round(c["pasi"], 1),
                       "Yes" if c["prior_bio"] else "No"])
    notes = wb.create_sheet("Notes")
    for line in ["VELA-3 site feasibility survey, North America, closed 30 October 2026.",
                 "Each site listed the patients in its own records who meet the VELA-3 eligibility criteria and "
                 "would be approached.",
                 "Compiled by Clinical Operations, Hvidore Biologics A/S."]:
        notes.append([line])
    wb.save(path)
    PP.normalize_xlsx(path, "Clinical Operations", "2026-09-14T08:12:00Z", "2026-10-31T16:47:00Z")
    return len(R.w.cand)
