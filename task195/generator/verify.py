"""An independent reader: the bundle and figures.json, nothing else.

It shares no code with the generator or with golden.py. It parses the shipped files itself, executes
KVAL-07 as written, and compares every figure the write-up is allowed to state.
"""
import datetime as dt
import json
import math
import os
import statistics
import sys
import zipfile
from xml.etree import ElementTree as ET

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
    with open(path, encoding="utf-8") as fh:
        lines = [l.rstrip("\n") for l in fh if not l.startswith("#")]
    head = lines[0].split(delim)
    return [dict(zip(head, l.split(delim))) for l in lines[1:] if l]


def sheet_rows(path, name):
    """Read a worksheet out of the workbook without a spreadsheet library."""
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    rel = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        target = {r.get("Id"): r.get("Target") for r in rels}
        sid = next(s.get(rel + "id") for s in wb.iter(ns + "sheet") if s.get("name") == name)
        part = "xl/" + target[sid].lstrip("/")
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            sst = ET.fromstring(z.read("xl/sharedStrings.xml"))
            shared = ["".join(t.text or "" for t in si.iter(ns + "t")) for si in sst]
        ws = ET.fromstring(z.read(part))
        out = []
        for row in ws.iter(ns + "row"):
            vals = []
            for c in row.iter(ns + "c"):
                v = c.find(ns + "v")
                text = v.text if v is not None else ""
                if c.get("t") == "s" and text != "":
                    text = shared[int(text)]
                elif c.get("t") == "inlineStr":
                    text = "".join(t.text or "" for t in c.iter(ns + "t"))
                vals.append(text)
            out.append(vals)
    return out


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

    biobank = {r["specimen_id"]: r["biobank_ref"]
               for r in table(os.path.join(target, "specimen_request_crosswalk.tsv"), "\t")}
    weeks = {}
    for r in table(os.path.join(target, "identity_panel_register_2027.csv")):
        day = dt.date.fromisoformat(r["report_date"])
        if day.year == 2027 and day.month in (4, 5):
            w = weeks.setdefault(r["report_ref"], {"rows": 0, "spec": set()})
            w["rows"] += 1
            w["spec"].add(biobank[r["specimen_id"]])
    same("report weeks", sorted(weeks), sorted(fig["panel_weeks"]))
    for ref, w in sorted(weeks.items()):
        same("%s specimens" % ref, len(w["spec"]), fig["panel_weeks"][ref]["specimens"])
        same("%s difference" % ref, w["rows"] - len(w["spec"]), fig["panel_weeks"][ref]["difference"])
        same("%s results issued" % ref, w["rows"], fig["panel_weeks"][ref]["results_issued"])

    amended = {}
    for a in table(os.path.join(target, "release_amendments_2026-03_2027-05.csv")):
        amended[(a["specimen_id"], a["field"])] = a["value_after"]
    months, rel_seen, flag_seen = {}, set(), set()
    with open(os.path.join(target, "qc_screen_history_2026-02-15_2027-02-28.csv"), encoding="utf-8") as fh:
        head = fh.readline().rstrip("\n").split(",")
        ix = {k: head.index(k) for k in ("specimen_id", "released_date", "release_status", "hetx_call",
                                         "review_outcome", "call_source")}
        for line in fh:
            f = line.rstrip("\n").split(",")
            if f[ix["release_status"]] != "RELEASED":
                continue
            sid = f[ix["specimen_id"]]
            released = amended.get((sid, "released_date"), f[ix["released_date"]])
            m = released[:7]
            key = (m, sid)
            d = months.setdefault(m, [0, 0])
            if key not in rel_seen:
                rel_seen.add(key)
                d[0] += 1
            field = "review_outcome" if f[ix["call_source"]] == "REVIEWED" else "hetx_call"
            call = amended.get((sid, field), f[ix[field]])
            if call in ("FLAG", "FLAGGED") and key not in flag_seen:
                flag_seen.add(key)
                d[1] += 1
    for m, row in sorted(fig["baseline"].items()):
        same("%s released" % m, months[m][0], row["released"])
        same("%s flagged" % m, months[m][1], row["flagged"])
        same("%s per thousand" % m, round(1000.0 * months[m][1] / months[m][0], 1), row["per_thousand"])
    vol = {r["reporting_month"]: int(r["results_released"].replace(" ", ""))
           for r in table(os.path.join(target, "release_volumes_monthly_2026-03_2027-02.csv"))}
    same("the reporting pack counts releases, not specimens",
         all(vol[m] >= fig["baseline"][m]["released"] for m in fig["baseline"]), True)

    book = os.path.join(target, "dilution_panel_2027q1.xlsx")
    prepared = {}
    for row in sheet_rows(book, "Prepared levels")[1:]:
        prepared[(row[0].strip(), row[1].strip().upper())] = float(row[3])
    results, stock = {}, {}
    for row in sheet_rows(book, "Replicate results")[1:]:
        if len(row) < 5 or row[4] in ("", None):
            continue
        key = row[0].strip().upper()
        stock[key] = row[1].strip()
        results.setdefault(key, []).append(float(row[4]))
    for lv, row in sorted(fig["dilution"].items()):
        vals = sorted(results[lv])
        level = prepared[(stock[lv], lv)]
        same("%s replicates" % lv, len(vals), row["replicates"])
        same("%s median recovery" % lv, round(statistics.median(vals) / level, 3),
             row["median_recovery"])
        same("%s within a fifth" % lv,
             sum(1 for v in vals if abs(v - level) <= 0.2 * level), row["within_fifth"])
    return CHECKS[0]


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    figs = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "figures.json")
    print("independent checks", run(tgt, figs))
