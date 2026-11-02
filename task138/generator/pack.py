"""Write the evidence pack (target/) from the world, as each producing system exports it."""
import os
from datetime import timedelta, timezone

import numpy as np
import openpyxl
from openpyxl.styles import Font

import docs
import params as P
import world
from io_util import repack_xlsx, write_csv

UTC = timezone.utc
BRU = world.BRU

FILES = {
    "holter": "holter_5min_segments_VLT317-101-102.txt",
    "ecg101": "corelab_ecg_VLT317-101_transfer3.xlsx",
    "ecg102": "corelab_ecg_VLT317-102_transfer2.csv",
    "plasma": "bioanalysis_plasma_VLT317-101-102.csv",
    "amb": "ambulatory_lab_results_2026.csv",
    "dosing": "dosing_log_VLT317-101-102.csv",
    "rand": "randomisation_unblinded_VLT317-101-102.xlsx",
    "screen": "screening_log_2026.csv",
    "vitals": "vital_signs_VLT317-101-102.csv",
    "safety": "safety_ecg_machine_VLT317-101-102.csv",
    "plan": "VLT-317_CQTc_analysis_plan_v2.0.pdf",
    "ddi": "VLT-317-103_CSR_synopsis.pdf",
}
DISTRACTORS = [FILES["vitals"], FILES["safety"]]


def sig3(x):
    if x >= 1000:
        return "%d" % int(round(x, -int(np.floor(np.log10(x))) + 2))
    if x >= 100:
        return "%d" % int(round(x))
    if x >= 10:
        return "%.1f" % x
    if x >= 1:
        return "%.2f" % x
    return "%.3f" % x


def lt(t, fmt):
    return t.astimezone(BRU).strftime(fmt)


def patient_id(s, rng):
    sub = s["subject"]
    styles = {("101", 1): "{st}-{n}", ("101", 2): "{n}", ("101", 3): "VLT317-{st}-{n}", ("101", 4): "{st}/{n}",
              ("101", 5): "{n}", ("102", 1): "{st}-{n}", ("102", 2): "{n}", ("102", 3): "{st} {n}"}
    f = styles[(s["study"], s["cohort"])]
    if rng.random() < 0.25:
        f = "{st}-{n}"
    return f.format(st=s["study"], n=sub)


def write(W, out):
    os.makedirs(out, exist_ok=True)
    subs = {s["subject"]: s for s in W["subjects"]}
    rng = np.random.default_rng([P.SEED, 9])

    # ---------------------------------------------------------------- Holter segment export (station, UTC)
    pid = {}
    for s in W["subjects"]:
        pid[s["rec1"]["id"]] = patient_id(s, rng)
        pid[s["rec2"]["id"]] = ""
    rows = []
    for g in sorted(W["holter"], key=lambda g: (g["rec"], g["start"])):
        valid = g["noise"] <= 50
        beats = int(round(g["hr"] * g["dur"] * g["valid_frac"] / 60.0)) if g["valid_frac"] > 0 else 0
        rows.append([g["rec"], g["serial"], pid[g["rec"]], g["start"].astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                     int(round(g["dur"])), beats,
                     "%.1f" % g["hr"] if valid else "", "%d" % round(g["rr"]) if valid else "",
                     "%d" % round(g["qt"]) if valid else "", "%d" % round(g["noise"]), g["vpb"] if valid else 0])
    write_csv(os.path.join(out, FILES["holter"]),
              ["RecordingID", "RecorderSN", "PatientID", "SegmentStart_UTC", "Dur_s", "Beats", "HR_bpm", "RR_ms",
               "QT_ms", "Noise_pct", "VPB"], rows, newline="\n", delimiter="\t",
              preamble=["# HS-2 Holter station, segment export", "# Exported 2026-08-03 16:41 by F. Wouters"])

    # ---------------------------------------------------------------- core lab ECG, study 101 (wide, RR in ms)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Intervals"
    head = ["STUDY", "SCREENING_NO", "VISIT", "NOMINAL_H", "EXTRACT_START"] + \
        ["RR_%d" % i for i in (1, 2, 3)] + ["QT_%d" % i for i in (1, 2, 3)] + ["PR_%d" % i for i in (1, 2, 3)] + \
        ["QRS_%d" % i for i in (1, 2, 3)] + ["READ_%d" % i for i in (1, 2, 3)]
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True)
    for e in sorted([e for e in W["ecg"] if e["study"] == "101"],
                    key=lambda e: (subs[e["subject"]]["screening"], e["day"], e["nominal"])):
        s = subs[e["subject"]]
        reps = e["reps"]
        ws.append(["VLT-317-101", s["screening"], "Day %d" % e["day"], e["nominal"],
                   lt(e["time"], "%Y-%m-%d %H:%M")]
                  + [int(round(r["rr"])) for r in reps]
                  + [int(round(r["qt"])) if r["ok"] else None for r in reps]
                  + [int(round(r["pr"])) for r in reps] + [int(round(r["qrs"])) for r in reps]
                  + ["" if r["ok"] else "U" for r in reps])
    ws.column_dimensions["E"].width = 17
    ws2 = wb.create_sheet("Transfer")
    for r in [["Transfer", "3"], ["Study", "VLT-317-101"], ["Issued", "2026-05-19"],
              ["Reader", "Semi-automated, single blinded reader per subject"], ["Units", "ms"],
              ["Replaces", "Transfer 2 (2026-04-07)"]]:
        ws2.append(r)
    p = os.path.join(out, FILES["ecg101"])
    wb.save(p)
    repack_xlsx(p, "CardioRead Labs", "CardioRead Labs", "2026-05-19T10:12:00Z", "2026-05-19T10:12:00Z",
                "VLT-317-101 transfer 3", "CardioRead Labs BV")

    # ---------------------------------------------------------------- core lab ECG, study 102 (long, HR in bpm)
    rows = []
    for e in sorted([e for e in W["ecg"] if e["study"] == "102"],
                    key=lambda e: (subs[e["subject"]]["screening"], e["day"], e["nominal"])):
        s = subs[e["subject"]]
        tpt = ("%gH" % e["nominal"]).replace(".", "P")
        for i, r in enumerate(e["reps"], 1):
            rows.append(["VLT-317-102", s["screening"], "DAY %d" % e["day"], tpt, i,
                         r["time"].astimezone(BRU).isoformat(timespec="seconds"), "%.1f" % r["hr"],
                         "%d" % round(r["qt"]) if r["ok"] else "", "%d" % round(r["pr"]), "%d" % round(r["qrs"]),
                         "" if r["ok"] else "QT NOT EVALUABLE"])
    write_csv(os.path.join(out, FILES["ecg102"]),
              ["STUDYID", "SCRNO", "VISIT", "TPT", "REPNUM", "EGDTC", "HR", "QT", "PR", "QRS", "EGSTAT"], rows)

    # ---------------------------------------------------------------- bioanalysis, inpatient plasma samples
    rows = []
    run_of = {}
    for r in sorted(W["pk"], key=lambda r: (r["study"], r["subject"], r["day"], r["nominal"])):
        s = subs[r["subject"]]
        key = (s["study"], s["cohort"], r["day"] if r["day"] in (1, 10) else 5)
        run_of.setdefault(key, "R26-%03d" % (len(run_of) * 2 + 41))
        sid = "P%s%04d%02d%03d" % (s["study"][-1], r["subject"] % 10000, r["day"], int(round(r["nominal"] * 10)))
        if not s["active"] or r["obs"] < P.LLOQ:
            res = "BLQ"
        elif r["obs"] > P.ULOQ:
            res = ">ULOQ"
        else:
            res = sig3(r["obs"])
        rows.append([sid, "VLT-317-" + s["study"], r["subject"], r["day"], ("%g" % r["nominal"]),
                     lt(r["time"], "%d/%m/%Y %H:%M"), res, run_of[key], ""])
        if res == ">ULOQ":
            rows.append([sid, "VLT-317-" + s["study"], r["subject"], r["day"], ("%g" % r["nominal"]),
                         lt(r["time"], "%d/%m/%Y %H:%M"), sig3(r["obs"]),
                         "R26-%03d" % (int(run_of[key][-3:]) + 1), "Re-assay after 1:5 dilution"])
    write_csv(os.path.join(out, FILES["plasma"]),
              ["SAMPLE_ID", "STUDY", "SUBJECT", "STUDY_DAY", "NOMINAL_H", "COLLECTED", "RESULT_NG_ML", "RUN",
               "COMMENT"], rows)

    # ---------------------------------------------------------------- ambulatory visits (unit lab, by volunteer)
    rows = []
    for r in sorted(W["amb"], key=lambda r: (r["time"], r["volunteer"])):
        s = subs[r["subject"]]
        day = int(round((s["dose_times"][-1].date() - s["day_m1"].date()).days)) + int(r["nominal"] // 24)
        visit = "Day %d" % day
        spec = "A%s%05d" % (lt(r["time"], "%m%d"), int(r["volunteer"][1:]))
        res = "BLQ" if (not s["active"] or r["obs"] < P.LLOQ) else sig3(r["obs"])
        rows.append([r["volunteer"], "VLT-317-" + s["study"], visit, lt(r["time"], "%Y-%m-%d"),
                     lt(r["time"], "%H:%M"), spec, "VLT-317 (plasma)", res, "ng/mL" if res != "BLQ" else ""])
        last = (s["design"] == "SAD" and r["nominal"] == 144) or (s["design"] == "MAD" and r["nominal"] == 96)
        if last:
            lab = [("ALT", "%d" % rng.integers(12, 41), "U/L"), ("AST", "%d" % rng.integers(14, 35), "U/L"),
                   ("Creatinine", "%.2f" % rng.uniform(0.72, 1.12), "mg/dL"),
                   ("Potassium", "%.1f" % rng.uniform(3.7, 4.9), "mmol/L")]
            for test, val, unit in lab:
                rows.append([r["volunteer"], "VLT-317-" + s["study"], visit, lt(r["time"], "%Y-%m-%d"),
                             lt(r["time"], "%H:%M"), spec.replace("A", "C", 1), test, val, unit])
    write_csv(os.path.join(out, FILES["amb"]),
              ["VOLUNTEER_NO", "PROTOCOL", "VISIT", "VISIT_DATE", "DRAW_TIME", "SPECIMEN_ID", "TEST", "RESULT",
               "UNIT"], rows)

    # ---------------------------------------------------------------- dosing log
    rows = []
    nurses = ["AV", "LD", "JM", "SB", "TC"]
    for d in sorted(W["doses"], key=lambda d: (d["study"], d["subject"], d["day"])):
        s = subs[d["subject"]]
        rows.append([d["subject"], "VLT-317-" + d["study"], d["day"], lt(d["time"], "%Y-%m-%d"),
                     lt(d["time"], "%H:%M:%S"), d["dose"], "K%s-%03d" % (d["study"], (d["subject"] % 100) + 100),
                     nurses[int(rng.integers(0, len(nurses)))]])
    write_csv(os.path.join(out, FILES["dosing"]),
              ["SUBJECT", "STUDY", "STUDY_DAY", "DOSE_DATE", "DOSE_TIME", "DOSE_LEVEL_MG", "KIT_NO", "ADMIN_BY"], rows)

    # ---------------------------------------------------------------- randomisation (unblinded)
    wb = openpyxl.Workbook()
    first = True
    for study in ("101", "102"):
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = "VLT-317-" + study
        ws.append(["COHORT", "SUBJECT", "SCREENING_NO", "RANDOMISED", "DOSE_LEVEL_MG", "TREATMENT"])
        for c in ws[1]:
            c.font = Font(bold=True)
        for s in sorted([s for s in W["subjects"] if s["study"] == study], key=lambda s: s["subject"]):
            ws.append([s["cohort"], s["subject"], s["screening"], (s["day_m1"]).strftime("%Y-%m-%d"), s["dose"],
                       "VLT-317" if s["active"] else "Placebo"])
    p = os.path.join(out, FILES["rand"])
    wb.save(p)
    repack_xlsx(p, "Kim Huysmans", "Kim Huysmans", "2026-08-11T07:45:00Z", "2026-08-11T08:02:00Z",
                "Unblinded randomisation VLT-317-101 and 102", "Ekerstede CPU")

    # ---------------------------------------------------------------- screening log
    rows = [[r["volunteer"], r["screening"], r["date"].isoformat(), "VLT-317-" + r["study"], r["outcome"]]
            for r in sorted(W["screening"], key=lambda r: (r["date"], r["screening"]))]
    write_csv(os.path.join(out, FILES["screen"]),
              ["VOLUNTEER_NO", "SCREENING_NO", "SCREEN_DATE", "PROTOCOL", "OUTCOME"], rows)

    # ---------------------------------------------------------------- vital signs (supine, scheduled)
    rows = []
    for s in W["subjects"]:
        days = [1] + ([P.MAD_DAYS] if s["design"] == "MAD" else [])
        for d in days:
            t0 = s["dose_times"][d - 1]
            for nt in (-0.5, 1, 2, 4, 8, 12, 24):
                t = world.add(t0, nt * 60 + float(rng.integers(-6, 6)))
                c = world.conc_at(t, s["dose_times"], s["dose"], s["pk"]) if s["active"] and nt > 0 else 0.0
                if s["design"] == "MAD" and d == P.MAD_DAYS and s["active"] and nt < 0:
                    c = world.conc_at(t, s["dose_times"], s["dose"], s["pk"])
                pulse = s["hr0"] + 0.6 * world.circ_h(world.wall(t)) + W["drug"]["s_hr"] * c + rng.normal(0, 3.5)
                rows.append([s["subject"], "VLT-317-" + s["study"], d, "%g" % nt, lt(t, "%H:%M"), "Supine",
                             int(round(rng.normal(118, 9))), int(round(rng.normal(72, 7))), int(round(pulse))])
    rows.sort(key=lambda r: (r[1], r[0], r[2], float(r[3])))
    write_csv(os.path.join(out, FILES["vitals"]),
              ["SUBJECT", "STUDY", "STUDY_DAY", "NOMINAL_H", "TIME", "POSITION", "SBP_MMHG", "DBP_MMHG", "PULSE_BPM"],
              rows)

    # ---------------------------------------------------------------- safety ECGs, machine reads
    rows = []
    for s in sorted(W["subjects"], key=lambda s: s["subject"]):
        for visit, off in (("Screening", -17), ("Admission", -1), ("Discharge", 2 if s["design"] == "SAD" else 11),
                           ("Follow-up", 7 if s["design"] == "SAD" else 17)):
            hr = s["hr0"] + rng.normal(0, 4)
            rr = 60.0 / hr
            qt = (s["qtc0"] + rng.normal(0, 6)) * rr ** s["beta"]
            rows.append([s["subject"], "VLT-317-" + s["study"], visit,
                         (s["day_m1"] + timedelta(days=off + 1)).strftime("%Y-%m-%d"), int(round(hr)),
                         int(round(s["pr0"] + rng.normal(0, 6))), int(round(s["qrs0"] + rng.normal(0, 4))),
                         int(round(qt)), int(round(qt / rr ** 0.5)), int(round(qt / rr ** (1 / 3))),
                         "Sinus bradycardia" if hr < 50 else "Sinus rhythm"])
    write_csv(os.path.join(out, FILES["safety"]),
              ["SUBJECT", "STUDY", "VISIT", "ECG_DATE", "HR", "PR", "QRS", "QT", "QTCB", "QTCF", "INTERPRETATION"],
              rows)

    # ---------------------------------------------------------------- governing documents
    docs.analysis_plan(os.path.join(out, FILES["plan"]))
    docs.ddi_synopsis(os.path.join(out, FILES["ddi"]))
    return FILES
