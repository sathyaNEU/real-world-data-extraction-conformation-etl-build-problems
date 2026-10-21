"""Independent verifier: recomputes every graded figure from target/ with its own code (csv and openpyxl readers,
its own discretised gamma, its own truncated likelihood, growth fit and renewal loop), importing nothing from the
generator, and compares with generator/figures.json.

    python3 task179/generator/verify.py
"""
import csv
import datetime as dt
import json
import math
import os
import sys

import numpy as np
from scipy import optimize, special

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
D0 = dt.date(2026, 5, 25)
MAXLAG = 80


def dnum(s):
    s = s.strip()
    d = dt.date.fromisoformat(s[:10]) if "-" in s else dt.datetime.strptime(s, "%d/%m/%Y").date()
    return (d - D0).days


def rows(name, delim=","):
    with open(os.path.join(TARGET, name), newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh, delimiter=delim))


def gamma_pmf(shape, scale):
    edges = np.arange(0, MAXLAG + 1) + 0.5
    cdf = special.gammainc(shape, edges / scale)
    p = np.diff(cdf)
    return p / p.sum()


def call():
    ll = rows("tvd_line_list_dunmarrow_2026-10-18.csv")
    ln = rows("tvd_transmission_links_2026-10-18.csv")
    cases = [r for r in ll if r["classification"] in ("Confirmed", "Probable")]
    cases.sort(key=lambda r: (dnum(r["date_of_notification"]), r["case_number"]))
    first, alias, onset = {}, {}, {}
    for r in cases:
        sid = r["sample_id"]
        if sid and sid in first:
            alias[r["case_number"]] = first[sid]
            continue
        if sid:
            first[sid] = r["case_number"]
        onset[r["case_number"]] = dnum(r["date_of_onset"])
    T = (dt.date(2026, 10, 11) - D0).days
    seen, src, lag = set(), [], []
    for r in ln:
        a = alias.get(r["Source person"], r["Source person"])
        b = alias.get(r["Target person"], r["Target person"])
        if a in onset and b in onset and (a, b) not in seen:
            seen.add((a, b))
            if onset[b] <= T and onset[b] - onset[a] >= 1:
                src.append(onset[a])
                lag.append(onset[b] - onset[a])
    src, lag = np.array(src), np.array(lag)
    horizon = np.clip(T - src, 1, MAXLAG)

    def nll(th, trunc):
        p = gamma_pmf(math.exp(th[0]), math.exp(th[1]))
        c = np.cumsum(p)
        v = np.log(p[np.minimum(lag, MAXLAG) - 1] + 1e-300)
        if trunc:
            v = v - np.log(c[horizon - 1] + 1e-300)
        return -v.sum()

    def fit(trunc):
        m = lag.mean()
        res = optimize.minimize(nll, [math.log(2.5), math.log(m / 2.5)], args=(trunc,), method="Nelder-Mead",
                                options={"maxiter": 8000, "xatol": 1e-9, "fatol": 1e-9})
        return gamma_pmf(math.exp(res.x[0]), math.exp(res.x[1]))

    daily = np.zeros(T + 1)
    for d in onset.values():
        if d <= T:
            daily[d] += 1
    b0 = (dt.date(2026, 8, 31) - D0).days
    x = np.arange(b0, T + 1)
    r = np.polyfit(x, np.log(daily[x]), 1)[0]
    cut_from = (dt.date(2026, 11, 2) - D0).days
    w0, w1 = (dt.date(2026, 11, 30) - D0).days, (dt.date(2026, 12, 27) - D0).days
    out = {}
    for key, trunc in (("golden", True), ("default", False)):
        w = fit(trunc)
        R = 1.0 / float(np.sum(w * np.exp(-r * np.arange(1, MAXLAG + 1))))
        series = list(daily)
        for t in range(T + 1, w1 + 1):
            lam = 0.0
            for s in range(1, min(MAXLAG, t) + 1):
                lam += w[s - 1] * series[t - s] * (R if t - s < cut_from else R * 0.5)
            series.append(lam)
        out[key] = (sum(series[w0:w1 + 1]), R, float(np.dot(np.arange(1, MAXLAG + 1), w)), len(lag))
    return out


def contacts():
    rg = rows("contact_registry_dunmarrow_w36-w42.csv")
    for r in rg:
        r["dl"] = dt.datetime.strptime(r["date_listed"], "%d/%m/%Y").date()
        r["end"] = dt.datetime.strptime(r["follow_up_end"], "%d/%m/%Y").date()
        r["age"] = int(r["age_years"])
        r["who"] = (r["district"], r["household_code"], r["initials"], r["sex"], r["age"])
    tablets = {}
    for r in rg:
        if r["follow_up_team"] == "LMR":
            tablets.setdefault((r["source_case_number"], r["household_code"], r["initials"], r["sex"]), []).append(r)
    for r in rg:
        if r["follow_up_team"] != "PHD":
            continue
        for t in tablets.get((r["source_case_number"], r["household_code"], r["initials"], r["sex"]), []):
            if abs((r["dl"] - t["dl"]).days) <= 1 and 1 <= abs(r["age"] - t["age"]) <= 3:
                r["who"] = t["who"]
                break
    out = {}
    lo, hi = dt.date(2026, 9, 7), dt.date(2026, 9, 27)
    for z in ("Tamberlow", "Quillmarsh", "Kettlebank North", "Brindlecourt"):
        per = {}
        for r in rg:
            if r["district"] == z:
                per.setdefault(r["who"], []).append(r)
        people = [p for p, ls in per.items() if lo <= min(x["dl"] for x in ls) <= hi]
        done = 0
        for p in people:
            ls = per[p]
            last = max(x["end"] for x in ls)
            done += any(x["status"] == "Follow-up completed" for x in ls if x["end"] == last)
        out[z] = (len(people), 100.0 * done / len(people))
    return out


def lab():
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(TARGET, "tamberlow_field_lab_pcr_w36-w42.xlsx"), read_only=True)
    final = {}
    fmt = "%d/%m/%Y %H:%M"
    for ws in wb.worksheets:
        it = ws.iter_rows(values_only=True)
        head = list(next(it))
        for v in it:
            r = dict(zip(head, v))
            if r["Reason"] != "Diagnostic":
                continue
            res = dt.datetime.strptime(r["Result time (analyser)"], fmt) + dt.timedelta(hours=1)
            coll = dt.datetime.strptime(r["Collected"], fmt)
            k = r["Sample no."]
            if k not in final or res >= final[k][0]:
                final[k] = (res, coll)
    out = {}
    for wk in (38, 39, 40, 41):
        h = [(res - coll).total_seconds() / 3600 for res, coll in final.values() if coll.isocalendar()[1] == wk]
        out[wk] = (sum(h) / len(h), 100.0 * sum(1 for v in h if v <= 24) / len(h))
    return out


def r1(v):
    return float("%.1f" % (v + 1e-9))


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []
    c = call()
    g, d = c["golden"], c["default"]
    pairs = [("call.cases_w49_52", int(round(g[0], -3)), F["call"]["cases_w49_52"]),
             ("components.R", r1(g[1]), F["components"]["R"]),
             ("components.serial_interval_days", int(round(g[2])), F["components"]["serial_interval_days"]),
             ("components.pairs", g[3], F["components"]["pairs"]),
             ("rivals.register_cases_w49_52", int(round(d[0], -3)), F["rivals"]["register_cases_w49_52"]),
             ("rivals.register_R", r1(d[1]), F["rivals"]["register_R"]),
             ("rivals.register_interval_days", int(round(d[2])), F["rivals"]["register_interval_days"])]
    for z, (n, s) in contacts().items():
        pairs += [("a1_%s.people" % z, n, F["a1_%s" % z]["people"]), ("a1_%s.pct_completed" % z, r1(s), F["a1_%s" % z]["pct_completed"])]
    for w, (m, s) in lab().items():
        pairs += [("a2_w%d.mean_hours" % w, r1(m), F["a2_w%d" % w]["mean_hours"]),
                  ("a2_w%d.pct_within_24h" % w, r1(s), F["a2_w%d" % w]["pct_within_24h"])]
    for k, mine, theirs in pairs:
        if mine != theirs:
            bad.append("%s verifier %s figures.json %s" % (k, mine, theirs))
    print("verify: golden %.1f cases (R %.4f, interval %.3f), default %.1f; %d figures compared, %d differ" % (
        g[0], g[1], g[2], d[0], len(pairs), len(bad)))
    for b in bad:
        print("  DIFF", b)
    return not bad


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
