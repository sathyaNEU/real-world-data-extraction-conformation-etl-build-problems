"""task179 independent verifier: reads only the bundle under target/ (and the figures the write-up states), on its own
code path (csv, openpyxl, pypdf and scikit-learn rather than the generator's pandas and statsmodels), and recomputes
the call, the critical components and every ask figure.

    python3 verify.py <target>        exit 0 when every figure reproduces"""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import sys
from collections import defaultdict
from zoneinfo import ZoneInfo

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TZ = ZoneInfo("America/Chicago")
D = dt.date
FAIL = []


def ok(name, cond, detail=""):
    print("  %-4s %-58s %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond:
        FAIL.append(name)


def pdf_text(path):
    from pypdf import PdfReader
    return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)


def rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def iso(s):
    return D(int(s[0:4]), int(s[5:7]), int(s[8:10]))


def mdy(s):
    return D(int(s[6:10]), int(s[0:2]), int(s[3:5]))


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    files = sorted(os.listdir(target))
    exts = set(os.path.splitext(f)[1] for f in files)
    ok("input gate: ten or more files", len(files) >= 10, "%d files" % len(files))
    ok("input gate: three or more formats", len(exts) >= 3, ", ".join(sorted(exts)))

    # ------------------------------------------------------------ documents
    dtext = pdf_text(os.path.join(target, "directive_26-07_gps_placement.pdf"))
    ctext = pdf_text(os.path.join(target, "criminal_code_conversion_table_2024.pdf"))
    stext = pdf_text(os.path.join(target, "belvantis_service_schedule_2025.pdf"))
    flat = lambda t: " ".join(t.split())
    ok("directive read back (positive control)", "An episode is open from its start date through its close date" in flat(dtext))
    ok("directive: new charge is a new arrest", "records as a new arrest" in flat(dtext))
    ok("schedule read back (positive control)", "booking records show the client held for any part of the day" in flat(stext)
       and "same date suspend that one day" in flat(stext) and "six hours behind UTC" in flat(stext)
       and "offices or counties leaves the account where it is" in flat(stext))
    ok("conversion table read back (positive control)", "Former section" in ctext and "302.10" in ctext)
    app = flat(dtext).split("Appendix: Category V")[-1]
    sched_b = set(re.findall(r"\b(\d{3}\.\d{2})\b", app))
    ok("Category V read from the directive", len(sched_b) == 19, "%d sections" % len(sched_b))
    conv = {}
    for m in re.finditer(r"((?:21|8)-[0-9a-z/()]+)\s+(\d{3}\.\d{2})", ctext):
        conv[m.group(1)] = m.group(2)
    ok("conversion table parsed", len(conv) >= 45, "%d former sections" % len(conv))

    def new(c):
        c = c.strip()
        return conv.get(c, c)

    # ------------------------------------------------------------ episodes
    ep = rows(os.path.join(target, "cms_supervision_episodes_2018-2026.csv"))
    ok("spine has 25,000 or more rows, or a larger file does",
       len(ep) >= 25000 or os.path.getsize(os.path.join(target, "hpd_violent_incident_victims_2018-2026.csv")) > 1e7, "%d episodes" % len(ep))
    per = defaultdict(list)
    for r in ep:
        r["s"] = iso(r["start_date"])
        r["c"] = iso(r["close_date"]) if r["close_date"] else None
        r["x"] = iso(r["expiration_date"])
        per[r["cms_person_id"]].append(r)
    sid2p = {r["sid"]: r["cms_person_id"] for r in ep}

    def open_end(p, d):
        return [r for r in per[p] if r["s"] <= d and (r["c"] is None or r["c"] >= d)]

    def during(p, d):
        return any(r["s"] <= d and (r["c"] is None or r["c"] >= d) for r in per.get(p, []))

    def caseload(d):
        return sorted(p for p in per if open_end(p, d))

    c26 = caseload(D(2026, 12, 31))
    ok("caseload at the end of 2026", len(c26) == figs["cc_caseload_2026"], "%d against %d" % (len(c26), figs["cc_caseload_2026"]))

    # ------------------------------------------------------------ bookings
    import openpyxl
    bks = []
    darrow = defaultdict(list)
    for r in rows(os.path.join(target, "darrow_county_jail_booking_notices_2018-2026.csv")):
        darrow[r["booking_no"]].append(r)
    for bno, rs in darrow.items():
        r = rs[0]
        t = dt.datetime.strptime(r["booked"], "%Y-%m-%d %H:%M")
        rel = dt.datetime.strptime(r["released"], "%Y-%m-%d %H:%M") if r["released"] else None
        bks.append(dict(j="D", sid=r["sid"], t=t, rel=rel, new=r["booking_type"] == "NEW ARREST", ag=r["arresting_agency"],
                        case=r["agency_case_no"], ch=[new(x["statute"]) for x in rs if x["statute"]]))
    wb = openpyxl.load_workbook(os.path.join(target, "keswick_county_jail_bookings_2018-2026.xlsx"), read_only=True)
    ws = wb["Bookings"]
    first = True
    for row in ws.iter_rows(values_only=True):
        if first:
            first = False
            continue
        if row[0] is None:
            continue
        t = row[1].replace(tzinfo=dt.timezone.utc).astimezone(TZ).replace(tzinfo=None)
        rel = row[2].replace(tzinfo=dt.timezone.utc).astimezone(TZ).replace(tzinfo=None) if row[2] else None
        ch = []
        if row[10] and row[10] != "PROB/PAROLE VIOLATION":
            ch = [new(p.split(" ")[0]) for p in row[10].split(" | ")]
        bks.append(dict(j="K", sid=row[4], t=t, rel=rel, new=row[7] == "NA", ag=row[8], case=str(row[9]), ch=ch))
    for b in bks:
        b["d"] = b["t"].date()
        b["p"] = sid2p.get(b["sid"])
        b["b"] = any(c in sched_b for c in b["ch"])
        b["under"] = b["p"] is not None and during(b["p"], b["d"])
    nb = [b for b in bks if b["new"] and b["under"]]
    nsb = sum(1 for b in nb if b["b"])
    ok("Category V new-arrest bookings 2018 to 2026", nsb == figs["step_schedb_bookings_2018_2026"], "%d" % nsb)
    hist = defaultdict(list)
    for b in nb:
        hist[b["p"]].append((b["d"], b["b"]))

    # ------------------------------------------------------------ police victims
    key = {}
    for r in ep:
        ln = re.sub(r"[^A-Z]", "", re.sub(r"\b(JR|SR|II|III|IV)\b", " ", r["last_name"].upper()))
        fn = re.sub(r"[^A-Z]", "", r["first_name"].upper().split(" ")[0])
        key[(ln, fn, r["date_of_birth"])] = r["cms_person_id"]
    vic = defaultdict(set)
    hpd = rows(os.path.join(target, "hpd_violent_incident_victims_2018-2026.csv"))
    for r in hpd:
        if r["victim_type"] != "I" or r["victim_name"] == "JUVENILE" or not r["victim_dob"]:
            continue
        last, rest = r["victim_name"].split(", ", 1)
        ln = re.sub(r"[^A-Z]", "", re.sub(r"\b(JR|SR|II|III|IV)\b", " ", last))
        fn = re.sub(r"[^A-Z]", "", rest.split(" ")[0])
        dob = mdy(r["victim_dob"]).isoformat()
        p = key.get((ln, fn, dob))
        if p:
            vic[p].add(mdy(r["occurred_date"]))
    v26 = sum(1 for p in c26 if any(D(2026, 1, 1) <= x <= D(2026, 12, 31) for x in vic.get(p, ())))
    ok("caseload victims recorded in 2026", v26 == figs["cc_victims_on_caseload_2026"], "%d" % v26)

    # ------------------------------------------------------------ the model, on scikit-learn
    xw = {r["legacy_offender_number"]: r["cms_person_id"] for r in rows(os.path.join(target, "oms_cms_person_crosswalk_2022.csv"))}
    sc = defaultdict(list)
    for r in rows(os.path.join(target, "mras_assessments_2017-2026.csv")):
        sc[xw.get(r["offender_ref"], r["offender_ref"])].append((iso(r["assessment_date"]), int(r["total_score"])))
    for k in sc:
        sc[k].sort()
    fams = {"VIOLENT": [], "WEAPON": [], "PROPERTY": [], "DRUG": [], "DUI": []}
    famof = {}
    for m in re.finditer(r"((?:21|8)-[0-9a-z/()]+)\s+(\d{3}\.\d{2})\s+([^\n]+)", ctext):
        famof[m.group(2)] = m.group(3)

    def fam(code):
        c = new(code)
        if c in sched_b:
            return "WEAPON" if c.startswith("501") else "VIOLENT"
        if c[:1] == "4" and c not in ("403.05",):
            return "PROPERTY"
        if c[:1] == "6":
            return "DRUG"
        if c in ("701.01", "701.02"):
            return "DUI"
        return "OTHER"

    def frame(Y, outcome=True):
        o = D(Y, 12, 31)
        X, y = [], []
        for p in caseload(o):
            eps = sorted(open_end(p, o), key=lambda r: r["s"])
            r0 = eps[0]
            age = (o - iso(r0["date_of_birth"])).days / 365.25
            f = fam(sorted(eps, key=lambda r: (r["s"], r["episode_id"]))[0]["lead_offense_statute"])
            par = int(any(r["supervision_type"] == "PAROLE" for r in eps))
            kes = int(eps[-1]["county"] == "KESWICK")
            city = int(any(r["residence_city"] == "Halverton" and r["county"] == "DARROW" for r in eps))
            rem = min(12.0, max(0.0, (max(r["x"] for r in eps) - o).days / 30.4375))
            s0 = min(r["s"] for r in per[p] if r["s"] <= o and (r["c"] is None or r["c"] >= o))
            changed = True
            while changed:
                changed = False
                for r in per[p]:
                    if r["c"] is not None and r["s"] < s0 and (s0 - r["c"]).days <= 1:
                        s0, changed = r["s"], True
            tos12 = int((o - s0).days / 30.4375 < 12)
            pri = max(int(r["prior_felony_convictions"]) for r in eps)
            ss = [v for d, v in sc.get(p, []) if d <= o]
            h = hist.get(p, [])
            n12 = min(3, sum(1 for d, b in h if o - dt.timedelta(days=365) < d <= o))
            b12 = int(any(b for d, b in h if o - dt.timedelta(days=365) < d <= o))
            v12 = int(any(o - dt.timedelta(days=365) < x <= o for x in vic.get(p, ())))
            X.append([age, int(r0["sex"] == "M"), np.log1p(pri)] + [int(f == k) for k in fams] +
                     [par, kes, city, rem, tos12, ss[-1] if ss else np.nan, n12, b12, v12])
            if outcome:
                y.append(int(any(b for d, b in h if D(Y + 1, 1, 1) <= d <= D(Y + 1, 12, 31))))
        X = np.array(X, float)
        return X, np.array(y)

    from sklearn.linear_model import LogisticRegression
    Xs, ys = [], []
    for Y in range(2018, 2026):
        X, y = frame(Y)
        Xs.append(X)
        ys.append(y)
    X = np.vstack(Xs)
    y = np.concatenate(ys)
    med = np.nanmedian(X[:, 13])
    X[np.isnan(X[:, 13]), 13] = med
    X26, _ = frame(2026, outcome=False)
    X26[np.isnan(X26[:, 13]), 13] = np.nanmedian(X26[:, 13])
    mu, sd = X.mean(0), X.std(0) + 1e-12
    out = {}
    for name, cols in (("own", list(range(16))), ("linked", list(range(17)))):
        m = LogisticRegression(penalty=None, max_iter=5000, tol=1e-10)
        m.fit((X[:, cols] - mu[cols]) / sd[cols], y)
        out[name] = float(m.predict_proba((X26[:, cols] - mu[cols]) / sd[cols])[:, 1].sum())
    ok("the forecast (linked model)", abs(out["linked"] - figs["golden_unrounded"]) < 0.5,
       "%.2f against %.1f" % (out["linked"], figs["golden_unrounded"]))
    ok("the forecast prints the call", int(100 * np.floor(out["linked"] / 100 + 0.5)) == figs["call_forecast_2027"])
    ok("the own-attribute model", abs(out["own"] - figs["default_unrounded"]) < 0.5, "%.2f against %.1f" % (out["own"], figs["default_unrounded"]))
    vi = X[:, 16] == 1
    ok("victims' rate on the 2018 to 2025 year ends", abs(100 * y[vi].mean() - figs["cc_rate_victims_pct"]) < 0.051, "%.2f" % (100 * y[vi].mean()))
    ok("others' rate on the 2018 to 2025 year ends", abs(100 * y[~vi].mean() - figs["cc_rate_others_pct"]) < 0.051, "%.2f" % (100 * y[~vi].mean()))

    # ------------------------------------------------------------ ask A: Belvantis days
    g = json.load(open(os.path.join(target, "belvantis_r4_device_events_2025-2026.json")))
    evs = g["events"]
    dead = set(e["voids_event_id"] for e in evs if e["event"] == "VOID")
    by = defaultdict(list)
    rank = {"ENROL": 0, "DEVICE_RETURN": 1, "DEVICE_ISSUE": 2, "SUSPEND": 3, "RESUME": 4, "END": 5, "ACCOUNT_TRANSFER": 6}
    for e in evs:
        if e["event"] == "VOID" or e["event_id"] in dead:
            continue
        by[(e["client_ref"], xw.get(e["client_ref"], e["client_ref"]))].append((iso(e["effective_date"]), rank[e["event"]], e["event"]))
    p2sid = {v: k for k, v in sid2p.items()}
    custody = defaultdict(set)
    for b in bks:
        a = b["d"]
        z = b["rel"].date() if b["rel"] else D(2026, 12, 31)
        while a <= z:
            custody[b["sid"]].add(a)
            a += dt.timedelta(days=1)
    month = [0] * 12
    held_p, susp_p = defaultdict(set), defaultdict(set)
    for ref, lst in by.items():
        lst.sort()
        on = None
        held, susp = set(), set()
        for d, _, e in lst:
            if e == "ENROL":
                if on is None:
                    on = d
            elif e in ("END", "ACCOUNT_TRANSFER") and on is not None:
                held |= {on + dt.timedelta(days=k) for k in range((d - on).days + 1)}
                on = None
        if on is not None:
            held |= {on + dt.timedelta(days=k) for k in range((D(2026, 12, 31) - on).days + 1)}
        # Schedule C.2: each suspension through the first resumption effective on or after it, whatever the logged order
        open_res = sorted(d for d, _, e in lst if e == "RESUME")
        for a in sorted(d for d, _, e in lst if e == "SUSPEND"):
            b = next((r_ for r_ in open_res if r_ >= a), None)
            if b is not None:
                open_res.remove(b)
            z = b if b is not None else D(2026, 12, 31)
            susp |= {a + dt.timedelta(days=k) for k in range((z - a).days + 1)}
        p = ref[1]
        held_p[p] |= held
        susp_p[p] |= susp
    for p, held in held_p.items():
        cus = custody.get(p2sid.get(p), set())
        for d in held:
            if d.year == 2026 and d not in susp_p[p] and d not in cus and during(p, d):
                month[d.month - 1] += 1
    for m in range(12):
        ok("enrolment days 2026-%02d" % (m + 1), month[m] == figs["ask_gps_days_2026_%02d" % (m + 1)],
           "%d against %d" % (month[m], figs["ask_gps_days_2026_%02d" % (m + 1)]))

    # ------------------------------------------------------------ ask B: zones
    res = defaultdict(set)
    words = {"STREET": "ST", "AVENUE": "AVE", "DRIVE": "DR", "ROAD": "RD", "LANE": "LN", "COURT": "CT", "PLACE": "PL",
             "BOULEVARD": "BLVD", "APARTMENT": "UNIT", "APT": "UNIT", "#": "UNIT"}
    for r in hpd:
        if r["victim_type"] == "I" and r["victim_res_city"] == "HALVERTON" and r["victim_residence"]:
            toks = re.sub(r"[,.]", " ", r["victim_residence"].upper()).replace("#", " # ").split()
            res[r["incident_number"]].add(" ".join(words.get(t, t) for t in toks))
    cells = defaultdict(int)
    done = set()
    for b in sorted(nb, key=lambda b: b["t"]):
        if not (b["b"] and b["ag"] == "HPD"):
            continue
        m = re.fullmatch(r"(\d{2})-(\d{6})", b["case"]) if b["j"] == "D" else re.fullmatch(r"HPD(\d{2})(\d{6})", b["case"])
        if not m:
            continue
        num = "HPD-%s-%s" % m.groups()
        if (b["p"], num) in done:
            continue
        done.add((b["p"], num))
        if b["d"].year == 2026:
            cells[b["d"].month] += len(res.get(num, ()))
    for m in range(1, 13):
        ok("zones 2026-%02d" % m, cells[m] == figs["ask_zones_2026_%02d" % m], "%d against %d" % (cells[m], figs["ask_zones_2026_%02d" % m]))
    print("verify: %d failed" % len(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
