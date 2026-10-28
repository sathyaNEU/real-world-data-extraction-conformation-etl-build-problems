"""Independent verifier: reads only target.zip (csv module and openpyxl, no pandas, none of solve.py), recomputes
every graded figure and compares with figures.json."""
import csv
import datetime as dt
import io
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from collections import defaultdict

import openpyxl

D = dt.date
HERE = os.path.dirname(os.path.abspath(__file__))


def pd_(s):
    if isinstance(s, dt.datetime):
        return s.date()
    if isinstance(s, dt.date):
        return s
    s = (s or "").strip()
    if not s:
        return None
    if "/" in s:
        a, b, c = s.split("/")
        return D(int(c), int(b), int(a))
    return D.fromisoformat(s[:10])


def rows(z, name):
    with z.open("target/" + name) as f:
        return list(csv.DictReader(io.TextIOWrapper(f, encoding="utf-8")))


def main(zpath):
    z = zipfile.ZipFile(zpath)
    names = [n[len("target/"):] for n in z.namelist()]
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    n = [0]

    def check(label, cond, detail=""):
        n[0] += 1
        if not cond:
            raise AssertionError("VERIFY FAIL %s %s" % (label, detail))

    pick = lambda pre: [x for x in names if x.startswith(pre)][0]
    # the pilot
    pilot = rows(z, pick("van_pilot_2018-19"))
    arrived = len(pilot)
    tested = sum(r["tested_by_van"] == "Y" for r in pilot)
    react = sum(r["tested_by_van"] == "Y" and r["antibody"] == "Reactive" for r in pilot)
    det = [r for r in pilot if r["rna"] == "Detected"]
    s12 = sum(1 for r in det if r["treatment_started"] == "Y" and (pd_(r["start_date"]) - pd_(r["test_date"])).days <= 84)
    t_share, l_share = tested / arrived, s12 / len(det)
    check("pilot", (tested, arrived, s12, len(det)) == (fig["pilot_tested"], fig["pilot_arrived"],
                                                         fig["pilot_started12"], fig["pilot_detected"]))
    # the laboratory
    lab = {}
    for r in rows(z, pick("virology_hcv_results")):
        lab[r["lab_number"]] = r
    labr = list(lab.values())
    first = {}
    rna = defaultdict(list)
    for r in labr:
        d = pd_(r["sample_taken"])
        if r["test_code"] in ("HCVAB", "HCV-AB-EIA") and r["result"] == "Reactive":
            if r["pseudonym"] not in first or (d, r["lab_number"]) < first[r["pseudonym"]]:
                first[r["pseudonym"]] = (d, r["lab_number"])
        if r["test_code"] in ("HCVPCR", "HCV-RNA-VL"):
            rna[r["pseudonym"]].append((d, "N" if r["result"] == "Not detected" else "D"))
    k = m = 0
    for p, (d, _) in first.items():
        h = sorted(x for x in rna.get(p, []) if 0 <= (x[0] - d).days <= 30)
        if h:
            m += 1
            k += h[0][1] == "D"
    ratio = k / m
    check("lab_ratio", round(ratio, 2) == fig["lab_ratio"], "%.4f" % ratio)
    # the register and the prison workbook
    reg = rows(z, pick("hcv_treatment_register"))
    cure, span = defaultdict(list), defaultdict(list)
    for r in reg:
        last = pd_(r["stopped_on"]) if r["outcome"] == "Stopped" else pd_(r["planned_end"])
        span[r["pseudonym"]].append((pd_(r["start_date"]), last))
        if r["svr12_result"] == "Not detected":
            cure[r["pseudonym"]].append(pd_(r["svr12_date"]))
    with z.open("target/" + pick("corvane_hcv_courses")) as f:
        wb = openpyxl.load_workbook(io.BytesIO(f.read()), read_only=True)
    pcure, pspan, prna = defaultdict(list), defaultdict(list), defaultdict(list)
    for sheet, (ci, cs, ce, cd, cr) in (("Courses 2017-20", (2, 3, 6, 8, 9)), ("Courses 2021-26", (2, 3, 6, 9, 10))):
        for i, row in enumerate(wb[sheet].iter_rows(values_only=True)):
            if i == 0:
                continue
            p = str(row[ci]).upper()
            pspan[p].append((pd_(row[cs]), pd_(row[ce])))
            if row[cr] == "Not detected":
                pcure[p].append(pd_(row[cd]))
    for i, row in enumerate(wb["Reception BBV positives"].iter_rows(values_only=True)):
        if i:
            prna[str(row[2]).upper()].append((pd_(row[3]), "D" if row[5] == "Detected" else "N"))
    # arrivals and the peer team's tests
    arr = rows(z, pick("setting_arrivals"))
    py = lambda d: 1 if D(2024, 10, 1) <= d <= D(2025, 9, 30) else (2 if D(2025, 10, 1) <= d <= D(2026, 9, 30) else 0)
    people = defaultdict(lambda: defaultdict(set))
    arrs = defaultdict(list)
    for r in arr:
        d = pd_(r["arrival_date"])
        y = py(d)
        if y:
            people[r["setting"]][y].add(r["pseudonym"])
            arrs[r["pseudonym"]].append((d, r["setting"]))
    out = {}
    for r in rows(z, pick("peer_testing_log")):
        if r["result"] not in ("Reactive", "Non-reactive") or not r["pseudonym"]:
            continue
        d = pd_(r["test_date"])
        hits = [x for x in arrs.get(r["pseudonym"], []) if 0 <= (d - x[0]).days <= 60]
        if hits:
            s = max(hits)[1]
            out.setdefault(s, []).append((r["pseudonym"], d, r["result"] == "Reactive"))

    def status(p, d):
        sp = span.get(p, []) + pspan.get(p, [])
        if any(a and a <= d and (b is None or b >= d) for a, b in sp):
            return 0.0
        cures = [x for x in cure.get(p, []) + pcure.get(p, []) if x and x < d]
        rs = sorted([x for x in rna.get(p, []) if x[0] < d] + [x for x in prna.get(p, []) if x[0] < d])
        if cures:
            return 1.0 if any(x[0] > max(cures) and x[1] == "D" for x in rs) else 0.0
        if rs:
            return 1.0 if rs[-1][1] == "D" else 0.0
        return ratio

    starts = {}
    for s, ts in out.items():
        A = (len(people[s][1]) + len(people[s][2])) / 2
        pos = [t for t in ts if t[2]]
        v = sum(status(p, d) for p, d, _ in pos) / len(pos)
        active = A * t_share * len(pos) / len(ts) * v
        st = active * l_share
        starts[s] = st
        check("active_%s" % s, int(10 * round(active / 10)) == fig["active10"][s], "%.2f" % active)
        check("starts_%s" % s, int(10 * round(st / 10)) == fig["starts10"][s], "%.2f" % st)
    ap = [(p, d) for p, d, rx in out["AP"] if rx]
    po = sum(1 for p, d in ap if any(x and x < d for x in pcure.get(p, [])) and not any(x and x < d for x in cure.get(p, [])))
    check("ap_prison_pct", int(round(100.0 * po / len(ap))) == fig["ap_prison_pct"], "%d of %d" % (po, len(ap)))
    order = sorted(starts, key=lambda s: -starts[s])
    check("call", order[0] == fig["order"][0] and order[1] == fig["order"][1])
    check("gap", int(10 * round((starts[order[0]] - starts[order[1]]) / 10)) == fig["gap10"])
    # the ask: clinic outcomes
    lims = defaultdict(set)
    for r in labr:
        lims[r["lims_patient_id"]].add(r["pseudonym"])
    alias = {p: sorted(ps) for ps in lims.values() for p in ps}
    got = defaultdict(lambda: [0, 0])
    for r in reg:
        if r["outcome"] == "Stopped":
            last = pd_(r["stopped_on"])
        elif r["outcome"] == "Completed":
            last = pd_(r["planned_end"])
        else:
            continue
        if not (D(2024, 10, 1) <= last <= D(2025, 9, 30)):
            continue
        h = 1 if last <= D(2025, 3, 31) else 2
        key = "%s_%d" % (r["clinic_code"], h)
        got[key][0] += 1
        ids = alias.get(r["pseudonym"], [r["pseudonym"]])
        aft = sorted(x for i in ids for x in rna.get(i, []) if (x[0] - last).days >= 84 and x[0] <= D(2026, 9, 30))
        c = bool(aft) and aft[0][1] == "N"
        if r["svr12_result"] == "Not detected" and (pd_(r["svr12_date"]) - last).days >= 84:
            c = True
        got[key][1] += int(c)
    for key, v in fig["AH"].items():
        check("ask_%s" % key, got[key][1] == v["confirmed"], "%s vs %s" % (got[key], v))
    # every format read back, with a positive control on each document
    tmp = tempfile.mkdtemp()
    for nm in names:
        if nm.endswith(".pdf"):
            p = os.path.join(tmp, nm)
            open(p, "wb").write(z.read("target/" + nm))
            txt = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout
            check("pdf_%s" % nm, len(txt) > 400, nm)
    check("pathway_rule", "twelve weeks or more after the last dose" in subprocess.run(
        ["pdftotext", os.path.join(tmp, pick("fenwold_hcv_pathway")), "-"], capture_output=True, text=True).stdout.replace("\n", " "))
    print("verify: %d checks passed on %s" % (n[0], os.path.basename(zpath)))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target.zip"))
