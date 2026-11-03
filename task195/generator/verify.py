"""An independent reader: the bundle and figures.json, nothing else.

It shares no code with the generator or with golden.py. It parses the shipped files itself, executes
KVAL-07 as written, and compares every figure the write-up is allowed to state.
"""
import datetime as dt
import json
import math
import os
import sys

Z = 1.959963985
AS_OF = dt.date(2027, 6, 21)
RUN = (dt.date(2027, 3, 1), dt.date(2027, 5, 31))
CUTOFFS = ["0.050", "0.030", "0.020", "0.015", "0.010"]
COHORTS = {"NHU3", "BARN2", "KARDIA", "OSTEO", "SEPSIS"}
CHECKS = [0]


def same(label, a, b):
    CHECKS[0] += 1
    if a != b:
        raise AssertionError("%s: bundle %r against figures.json %r" % (label, a, b))


def table(path, delim=","):
    import csv
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader((l for l in fh if not l.startswith("#")), delimiter=delim))


def run(target, figures_path):
    CHECKS[0] = 0
    fig = json.load(open(figures_path, encoding="utf-8"))

    qc = {}
    for name in ("qc_screen_calls_gsqa_2027-03_2027-05.csv", "qc_screen_calls_gsqb_2027-03_2027-05.csv"):
        for r in table(os.path.join(target, name), ";"):
            if r["read_accepted"] == "Y":
                qc[r["specimen_id"]] = r
    mf = {r["specimen_id"]: float(r["mixture_fraction"])
          for r in table(os.path.join(target, "mixture_fraction_rerun_v34.csv"))
          if r["read_set_accepted"] == "Y"}
    panel = {}
    for r in table(os.path.join(target, "identity_panel_register_2027.csv")):
        if dt.date.fromisoformat(r["report_date"]) <= AS_OF:
            panel.setdefault(r["specimen_id"], set()).add(r["verdict"])

    population = []
    for sid, r in qc.items():
        day = dt.date.fromisoformat(r["received_date"])
        if not (RUN[0] <= day <= RUN[1]):
            continue
        if r["agreement_ref"] or r["project_code"] not in COHORTS:
            continue
        if sid not in mf or not (panel.get(sid, set()) & {"MIXED", "CONCORDANT"}):
            continue
        population.append((sid, r["hetx_call"] == "FLAG", mf[sid], "MIXED" in panel[sid]))
    same("comparison specimens", len(population), fig["comparison_specimens"])
    events = [p for p in population if p[3]]
    clean = [p for p in population if not p[3]]
    same("confirmed events", len(events), fig["confirmed_events"])
    same("panel-clean specimens", len(clean), fig["panel_clean"])
    service = sum(1 for p in events if p[1])
    same("the screen in service's detections", service, fig["service_detected"])
    service_false = sum(1 for p in clean if p[1])
    same("the screen in service's false calls", service_false, fig["service_false_calls"])
    same("the screen in service's false-call rate",
         round(100.0 * service_false / len(clean), 2), fig["service_false_rate_pct"])

    n = len(events)
    decision = "hold"
    for key in CUTOFFS:
        cut = float(key)
        det = sum(1 for p in events if p[2] >= cut)
        b = sum(1 for p in events if p[2] >= cut and not p[1])
        c = sum(1 for p in events if p[2] < cut and p[1])
        fp = sum(1 for p in clean if p[2] >= cut)
        gain = det - service
        # the variance of a difference of two proportions measured on one set of specimens
        var = (b + c) / float(n * n) - (gain * gain) / float(n ** 3)
        half = Z * math.sqrt(var)
        lo, hi = gain / n - half, gain / n + half
        established = lo > 0
        ceiling = fp / len(clean) <= service_false / len(clean)
        row = fig["cutoffs"][key]
        same("%s detections" % key, det, row["detected"])
        same("%s increase" % key, gain, row["gain"])
        same("%s increase in points" % key, round(100.0 * gain / n, 2), row["gain_pp"])
        same("%s false calls" % key, fp, row["false_calls"])
        same("%s false-call rate" % key, round(100.0 * fp / len(clean), 2), row["false_rate_pct"])
        same("%s established" % key, "Yes" if established else "No", row["established"])
        same("%s false-call rate not higher" % key, "Yes" if ceiling else "No", row["ceiling_ok"])
        same("%s interval" % key, [round(100 * lo, 2), round(100 * hi, 2)], row["interval_pp"])
        if decision == "hold" and established and ceiling:
            decision = key
    same("the call", decision, fig["call"])
    same("the chosen cutoff's detections", fig["cutoffs"][decision]["detected"], fig["chosen_detected"])
    same("the chosen cutoff's increase", fig["cutoffs"][decision]["gain"], fig["chosen_gain"])
    same("the chosen cutoff's increase in points", fig["cutoffs"][decision]["gain_pp"], fig["chosen_gain_pp"])
    same("the chosen cutoff's false-call rate", fig["cutoffs"][decision]["false_rate_pct"],
         fig["chosen_false_rate_pct"])

    # the ask: per extraction method, the twelve reporting months to February 2027
    import re
    try:
        import pypdf
        report = "\n".join(p.extract_text() or "" for p in pypdf.PdfReader(
            os.path.join(target, "extraction_platform_validation_2025.pdf")).pages)
    except Exception:
        report = ""
    table_2026 = {m.group(1): m.group(2) for m in re.finditer(
        r"(?m)^\s*([1-9])\s+(magnetic bead|silica column|salting out)\b", report)}
    same("the 2026 method table as the platform validation prints it",
         sorted(table_2026.items()), [("1", "magnetic bead"), ("2", "silica column"), ("3", "salting out")])
    amended = {}
    for a in table(os.path.join(target, "release_amendments_2027-04_2027-06.csv")):
        amended[(a["specimen_id"], a["field"])] = a["value_after"]
    hist = table(os.path.join(target, "qc_screen_history_2026-02-15_2027-02-28.csv"))
    first_new = min(r["extracted_date"] for r in hist if r["extraction_method_code"] not in table_2026)
    same("the day the method table was re-coded", first_new, fig["method_table_recoded"])
    months = ["2026-%02d" % m for m in range(3, 13)] + ["2027-01", "2027-02"]
    per, seen = {}, set()
    for r in hist:
        if r["release_status"] != "RELEASED" or not r["released_date"]:
            continue
        sid = r["specimen_id"]
        if amended.get((sid, "released_date"), r["released_date"])[:7] not in months or sid in seen:
            continue
        seen.add(sid)
        # the code is the one the extraction was booked under; before the re-coding it reads on the
        # 2026 table, after it on the table the warehouse names it by
        method = (table_2026[r["extraction_method_code"]] if r["extracted_date"] < first_new
                  else r["extraction_method"])
        field = "review_outcome" if r["call_source"] == "REVIEWED" else "hetx_call"
        call = amended.get((sid, field), r[field])
        d = per.setdefault(method, [0, 0, 0])
        d[0] += 1
        d[1] += 1 if r["call_source"] == "REVIEWED" else 0
        d[2] += 1 if call in ("FLAG", "FLAGGED") else 0
    same("the methods", sorted(per), sorted(fig["methods"]))
    for m, row in sorted(fig["methods"].items()):
        same("%s released" % m, per[m][0], row["released"])
        same("%s reviewed" % m, per[m][1], row["reviewed"])
        same("%s flagged" % m, per[m][2], row["flagged"])
        same("%s per thousand" % m, round(1000.0 * per[m][2] / per[m][0], 1), row["per_thousand"])

    return CHECKS[0]


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    figs = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "figures.json")
    print("independent checks", run(tgt, figs))
