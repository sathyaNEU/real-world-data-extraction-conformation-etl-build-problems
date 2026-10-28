"""task464 architecture 9: the rest of the pack.

The clinical events extract (the network's CVD code search: diagnoses, observations, results and the coded parts of
discharge summaries), the repeat change log, the product lookup, the practice profiles, and two files the solution
never reads: the 2025-26 QOF CVD indicators and the dispensed-items extract.
"""
import csv, json, os, collections
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
import world as W
import pack as PK

OUT = PK.OUT


def _rng(*k):
    return np.random.default_rng([46991] + list(k))


def events(w, pids):
    """The coded CVD events: the discharge summaries' coded entries plus routine observations and results."""
    rows = []
    for e in w.events:
        if W.KEEP_FROM <= e["t"] <= W.ASOF and e["filed"] <= W.ASOF + 1:
            rows.append((e["t"], e["pid"], W.BY_KEY[e["key"]]["code"], e["code"], e["term"], e["value"], e["unit"]))
    obs = [
        ("163030003", "Systolic blood pressure", "mmHg", 118, 168),
        ("1091811000000102", "Diastolic blood pressure", "mmHg", 62, 98),
        ("1005671000000105", "Serum cholesterol level", "mmol/L", 3.1, 6.9),
        ("1022191000000100", "Serum LDL cholesterol level", "mmol/L", 1.2, 4.6),
        ("1028981000000100", "Estimated glomerular filtration rate using creatinine CKD-EPI", "mL/min/1.73m2", 28, 96),
        ("1000731000000107", "Serum creatinine level", "umol/L", 58, 162),
        ("1003671000000109", "Haemoglobin A1c level", "mmol/mol", 34, 78),
        ("27113001", "Body weight", "kg", 52, 118),
    ]
    for pid in sorted(pids):
        P = w.patients[pid]
        r = _rng(int(pid[:8], 16) % 1000003)
        key = P["episodes"][-1][0]
        code = W.BY_KEY[key]["code"]
        n = int(r.integers(1, 5))
        for _ in range(n):
            t = W.EXTRACT_FROM + int(r.integers(0, W.ASOF - W.EXTRACT_FROM))
            # the practice an observation sits under is the one the patient was registered with on the day
            k2 = None
            for k, a, b, why in P["episodes"]:
                if a <= t and (b is None or t < b): k2 = k
            if k2 is None: continue
            c, term, unit, lo, hi = obs[int(r.integers(0, len(obs)))]
            v = lo + (hi - lo) * r.random()
            val = ("%.1f" % v) if unit in ("mmol/L",) else ("%d" % round(v))
            rows.append((t, pid, W.BY_KEY[k2]["code"], c, term, val, unit))
        if P["meds"].get("doac") and r.random() < 0.9:
            t = W.EXTRACT_FROM - int(r.integers(0, 380))
            rows.append((t, pid, code, "49436004", "Atrial fibrillation", "", ""))
        if r.random() < 0.35:
            t = W.EXTRACT_FROM + int(r.integers(0, W.ASOF - W.EXTRACT_FROM))
            rows.append((t, pid, code, "1085871000000105", "QRISK3 cardiovascular disease 10 year risk score",
                         "%.1f" % (4 + 26 * r.random()), "%"))
    rows = [x for x in rows if W.KEEP_FROM <= x[0] <= W.ASOF]
    rows.sort(key=lambda x: (x[0], x[2], x[1], x[3]))
    with open(os.path.join(OUT, "cvd_clinical_events_2023-2026.csv"), "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["patient_ref", "practice_code", "event_date", "snomed_concept_id", "term", "value", "units"])
        for t, pid, code, c, term, val, unit in rows:
            wr.writerow([pid, code, W.iso(t), c, term, val, unit])
    return len(rows)


def change_log(w):
    """The repeat change log the network's medicines safety search pulls: every edit to a repeat in place."""
    rows = []
    for e in w.edits:
        if W.EXTRACT_FROM <= e["t"] <= W.ASOF:
            tp = w.templates[e["tid"]]
            rows.append([e["t"], tp, e["field"], e["old"], e["new"], e["by"]])
    # wording-only edits (no change of dose), prescriber reassignments when a partner retired, and notes
    r = _rng(5)
    tps = [tp for tp in w.templates if tp["authorised"] <= W.ASOF and (tp["ended"] is None or tp["ended"] >= W.EXTRACT_FROM)]
    reword = {"ONE daily": "ONE in the morning", "1 daily": "ONE daily", "ONE at night": "Take ONE tablet at night",
              "1 at night": "ONE at night", "one a day": "ONE daily", "1 nocte": "ONE at night",
              "ONE twice a day": "ONE twice daily", "1 bd": "ONE twice a day", "TWO daily": "TWO to be taken each day"}
    for tp in tps:
        if r.random() < 0.035 and tp["directions"] in reword:
            t = max(tp["authorised"], W.EXTRACT_FROM) + int(r.integers(1, 200))
            if t <= min(W.ASOF, tp["ended"] or W.ASOF):
                rows.append([t, tp, "Dosage", tp["directions"], reword[tp["directions"]], "GP"])
        if r.random() < 0.02:
            t = max(tp["authorised"], W.EXTRACT_FROM) + int(r.integers(1, 250))
            if t <= min(W.ASOF, tp["ended"] or W.ASOF):
                note = ["Pt prefers to collect from branch surgery", "Check BP before next issue",
                        "Please synchronise with other repeats", "Pt has dosette - pharmacy aware",
                        "Requested via NHS App"][int(r.integers(0, 5))]
                rows.append([t, tp, "Notes", "", note, "Administrator"])
    retire = W.day("2025-07-31")
    for tp in tps:
        if tp["key"] == "E" and tp["authorised"] <= retire and (tp["ended"] is None or tp["ended"] > retire) and r.random() < 0.38:
            rows.append([retire, tp, "Authorising clinician", "G%07d" % 4417260, "G%07d" % 7130948, "Practice manager"])
    rows.sort(key=lambda x: (x[0], W.BY_KEY[x[1]["key"]]["code"], x[1]["pid"], x[2]))
    with open(os.path.join(OUT, "repeat_changes_2024-01_to_2026-11.csv"), "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["changed_on", "practice_code", "patient_ref", "repeat_ref", "item", "field", "old_value",
                     "new_value", "changed_by"])
        for t, tp, field, old, new, by in rows:
            item = PK.product_a(tp)
            if field == "Quantity":
                u = PK.unit_word(tp)
                old = "%s %s" % (old, u); new = "%s %s" % (new, u)
            wr.writerow([W.iso(t), W.BY_KEY[tp["key"]]["code"], tp["pid"], PK.tref(tp), item, field, old, new, by])
    return len(rows)


def lookup():
    rows = []
    for d, s, f, _ in W.ACE_ARB:
        cls = "ACE inhibitor" if d in W.ACE_NAMES else "Angiotensin II receptor antagonist"
        rows.append((d, s, f, cls, "2.5.5.1" if cls == "ACE inhibitor" else "2.5.5.2"))
    for d, s, a, b in W.STATINS:
        rows.append((d, s, "tablets", "Statin", "2.12"))
    rows.append(("Fluvastatin", "40mg", "capsules", "Statin", "2.12"))
    rows.append(("Ezetimibe", "10mg", "tablets", "Cholesterol absorption inhibitor", "2.12"))
    for d, s, doses, _ in W.DOACS:
        rows.append((d, s, "tablets", "Direct oral anticoagulant", "2.8.2"))
    rows.append(("Ticagrelor", "90mg", "tablets", "P2Y12 inhibitor", "2.9"))
    rows.append(("Ticagrelor", "60mg", "tablets", "P2Y12 inhibitor", "2.9"))
    rows.append(("Clopidogrel", "75mg", "tablets", "P2Y12 inhibitor", "2.9"))
    rows.append(("Ramipril", "5mg", "tablets", "ACE inhibitor", "2.5.5.1"))
    # the rest of the crosswalk: strengths and products the network's searches map whether or not any issue in
    # this extract carries them
    for d, s, f, cls, bnf in (
            ("Atorvastatin", "10mg", "tablets", "Statin", "2.12"), ("Simvastatin", "10mg", "tablets", "Statin", "2.12"),
            ("Rosuvastatin", "5mg", "tablets", "Statin", "2.12"), ("Rosuvastatin", "20mg", "tablets", "Statin", "2.12"),
            ("Pravastatin", "10mg", "tablets", "Statin", "2.12"), ("Pravastatin", "20mg", "tablets", "Statin", "2.12"),
            ("Fluvastatin", "20mg", "capsules", "Statin", "2.12"),
            ("Ramipril", "1.25mg", "capsules", "ACE inhibitor", "2.5.5.1"), ("Ramipril", "10mg", "tablets", "ACE inhibitor", "2.5.5.1"),
            ("Lisinopril", "5mg", "tablets", "ACE inhibitor", "2.5.5.1"), ("Enalapril", "10mg", "tablets", "ACE inhibitor", "2.5.5.1"),
            ("Perindopril erbumine", "2mg", "tablets", "ACE inhibitor", "2.5.5.1"),
            ("Losartan", "25mg", "tablets", "Angiotensin II receptor antagonist", "2.5.5.2"),
            ("Candesartan", "4mg", "tablets", "Angiotensin II receptor antagonist", "2.5.5.2"),
            ("Candesartan", "16mg", "tablets", "Angiotensin II receptor antagonist", "2.5.5.2"),
            ("Valsartan", "80mg", "capsules", "Angiotensin II receptor antagonist", "2.5.5.2"),
            ("Rivaroxaban", "15mg", "tablets", "Direct oral anticoagulant", "2.8.2"),
            ("Edoxaban", "30mg", "tablets", "Direct oral anticoagulant", "2.8.2"),
            ("Dabigatran etexilate", "150mg", "capsules", "Direct oral anticoagulant", "2.8.2"),
            ("Prasugrel", "10mg", "tablets", "P2Y12 inhibitor", "2.9")):
        rows.append((d, s, f, cls, bnf))
    rows = sorted(set(rows), key=lambda x: (x[4], x[0], x[1], x[2], x[3]))
    with open(os.path.join(OUT, "cvd_product_lookup.csv"), "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["system_a_drug", "system_b_product", "vtm", "strength", "form", "bnf_class", "bnf_section"])
        for d, s, f, cls, bnf in rows:
            r = dict(drug=d, strength=s, form=f)
            wr.writerow([PK.product_a(r), PK.product_b(r), d, s, f, cls, bnf])
    return len(rows)


def profiles():
    wb = Workbook(); ws = wb.active; ws.title = "Practices"
    ws.append(["Hensey Vale PCN member practices, list sizes at 1 October 2026"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    hdr = ["ODS code", "Practice", "Clinical system", "Registered list", "GP WTE", "Nurse WTE",
           "PCN clinical pharmacist sessions a week (Jul to Dec 2026)", "Dispensing", "Branch sites"]
    ws.append(hdr)
    for c in ws[3]:
        c.font = Font(bold=True); c.fill = PatternFill("solid", fgColor="E8E8E8"); c.alignment = Alignment(wrap_text=True)
    extra = {"A": (7.6, 4.2, 2, "No", 1), "B": (4.3, 2.6, 1, "No", 0), "C": (3.9, 2.2, 1, "No", 0),
             "D": (6.8, 3.9, 1, "No", 1), "E": (3.4, 1.8, 1, "No", 0), "F": (4.7, 2.9, 2, "Yes", 0),
             "G": (3.1, 1.6, 0, "No", 0)}
    for p in W.PRACTICES:
        g, n, s, disp, br = extra[p["key"]]
        ws.append([p["code"], p["name"], "System %s" % p["system"], p["list_size"], g, n, s, disp, br])
    for col, wdt in zip("ABCDEFGHI", (10, 28, 15, 15, 9, 10, 22, 11, 12)):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "A4"
    wb.save(os.path.join(OUT, "pcn_practice_profiles_2026.xlsx"))
    return 7


def qof(w):
    """Distractor: the practices' 2025-26 QOF CVD indicator achievement as published."""
    r = _rng(9)
    rows = []
    for p in W.PRACTICES:
        for ind, desc, lo, hi in (("CHOL003", "CVD: on statin therapy", 0.78, 0.9),
                                  ("CHOL004", "CVD: latest LDL 1.8 mmol/L or less (or non-HDL 2.5 or less)", 0.38, 0.58),
                                  ("HYP008", "Hypertension aged 79 or under: last BP 140/90 or less", 0.6, 0.76),
                                  ("AF008", "AF with CHA2DS2-VASc 2 or more: on a DOAC", 0.82, 0.94)):
            den = int(p["list_size"] * {"CHOL003": 0.045, "CHOL004": 0.045, "HYP008": 0.11, "AF008": 0.018}[ind] * (0.9 + 0.2 * r.random()))
            num = int(den * (lo + (hi - lo) * r.random()))
            rows.append([p["code"], p["name"], ind, desc, num, den, "%.1f" % (100 * num / den)])
    with open(os.path.join(OUT, "qof_cvd_achievement_2025-26.csv"), "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["practice_code", "practice_name", "indicator", "description", "numerator", "denominator",
                     "achievement_pct"])
        for x in rows: wr.writerow(x)
    return len(rows)


def epact(w):
    """Distractor: items dispensed by practice, month and chemical, 2025-26 financial year (from dispensing)."""
    lo, hi = W.day("2025-04-01"), W.day("2026-03-31")
    cnt = collections.Counter(); qty = collections.Counter()
    r = _rng(11)
    for x in w.issues:
        if x["cancelled"] or not (lo - 5 <= x["t"] <= hi): continue
        disp = x["t"] + (0 if r.random() < 0.8 else int(r.integers(1, 5)))
        if not (lo <= disp <= hi): continue
        d = W.date_of(disp)
        k = (W.BY_KEY[x["key"]]["code"], "%04d-%02d" % (d.year, d.month), x["drug"])
        cnt[k] += 1; qty[k] += x["qty"]
    with open(os.path.join(OUT, "dispensed_items_cvd_2025-26.csv"), "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["year_month", "practice_code", "bnf_chemical_substance", "items", "total_quantity"])
        for k in sorted(cnt, key=lambda k: (k[1], k[0], k[2])):
            wr.writerow([k[1], k[0], k[2], cnt[k], qty[k]])
    return len(cnt)


def write_all(w, pids):
    return dict(events=events(w, pids), changes=change_log(w), lookup=lookup(), profiles=profiles(),
                qof=qof(w), epact=epact(w))
