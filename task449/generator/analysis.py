"""Reads target/ only and computes every rung of the ladder, the golden and its licensed variants.

The golden: each live posting on a reference date counts by the chance its position was still unfilled that day.
An Employer Services posting comes down on the outcome day, so it counts in full. A self-service posting counts in
full when its term was renewed or it was taken down after the date; when it ran to the end of its term untouched,
it counts by (S(a) - S(e)) / (S(s) - S(e)), S the occupation's time-to-end survival read from the Employer Services
postings (published to closed), a the posting's age on the date, s and e its term's start and end. The board's
positions then share out each sector's survey estimate, and the test reads jobseekers over vacancies summed over
the four dates.
"""
import datetime as dt
import json
import math
import os
import re
from collections import defaultdict

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)

REF_DATES = [dt.date(2025, 12, 31), dt.date(2026, 3, 31), dt.date(2026, 6, 30), dt.date(2026, 9, 30)]
EXTRACT = dt.date(2026, 11, 14)
TERM = 42
THRESHOLD = 1.5


# ---------------------------------------------------------------------------------------------- readers
def read_concordance(tgt):
    c = pd.read_csv(os.path.join(tgt, "noc_2016_v1.3_to_noc_2021_v1.0.csv"), dtype=str)
    return dict(zip(c["noc_2016"], c["noc_2021"]))


def read_snapshots(tgt):
    conc = read_concordance(tgt)
    o = pd.read_csv(os.path.join(tgt, "workshore_live_postings_2025-07_2026-01.csv"), dtype=str)
    old = pd.DataFrame({
        "snap": pd.to_datetime(o["snapshot_date"]).dt.date,
        "pid": o["posting_no"],
        "employer": o["employer_no"],
        "occ": o["noc_2016"].map(conc),
        "positions": o["positions"].astype(int),
        "posted": pd.to_datetime(o["date_posted"], format="%d/%m/%Y").dt.date,
        "channel": o["channel"].map({"SS": "S", "ES": "E"}),
        "term_last": pd.to_datetime(o["expiry_date"], format="%d/%m/%Y", errors="coerce").dt.date,
    })
    n = pd.read_csv(os.path.join(tgt, "workshore_live_postings_2026-02_2026-09.csv"), dtype=str, keep_default_na=False)
    new = pd.DataFrame({
        "snap": pd.to_datetime(n["extract_date"]).dt.date,
        "pid": [lr if lr else ji for lr, ji in zip(n["legacy_ref"], n["job_id"])],
        "employer": n["employer_number"],
        "occ": n["noc_2021"],
        "positions": n["openings"].astype(int),
        "posted": pd.to_datetime(n["posted_on"]).dt.date,
        "channel": n["source"].map({"Self-service": "S", "Employer Services": "E"}),
        "term_last": pd.to_datetime(n["term_end"].replace("", None), errors="coerce").dt.date,
    })
    s = pd.concat([old, new], ignore_index=True)
    assert s["occ"].notna().all() and s["channel"].notna().all()
    return s


def eastern_offset(d):
    y = d.year
    mar = dt.date(y, 3, 8)
    while mar.weekday() != 6:
        mar += dt.timedelta(days=1)
    nov = dt.date(y, 11, 1)
    while nov.weekday() != 6:
        nov += dt.timedelta(days=1)
    return 4 if mar <= d < nov else 5


def utc_to_local(ts):
    t = dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
    for off in (4, 5):
        loc = t - dt.timedelta(hours=off)
        if eastern_offset(loc.date()) == off:
            return loc
    return t - dt.timedelta(hours=5)


def read_events(tgt):
    o = pd.read_csv(os.path.join(tgt, "workshore_board_events_2025-10-01_2026-02-01.csv"), dtype=str)
    kind_old = {"PUBLISHED": "PUBLISHED", "RENEWED": "RENEWED", "REMOVED_BY_EMPLOYER": "REMOVED",
                "EXPIRED": "EXPIRED", "CLOSED_ES": "CLOSED"}
    conc = read_concordance(tgt)
    rows = [(p, pd.Timestamp(t).date(), kind_old[k], conc.get(nc) if isinstance(nc, str) else None,
             {"SS": "S", "ES": "E"}.get(ch) if isinstance(ch, str) else None)
            for t, p, k, nc, ch in zip(o["event_time"], o["posting_no"], o["event"], o["noc_2016"], o["channel"])]
    legacy = {}
    recs = []
    with open(os.path.join(tgt, "workshore_board_events_2026-02-02_2026-11-14.jsonl"), encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            recs.append(r)
            if r["type"] == "migrated":
                legacy[r["job_id"]] = r["legacy_ref"]
    kind_new = {"posted": "PUBLISHED", "renewed": "RENEWED", "taken_down_by_employer": "REMOVED", "expired": "EXPIRED",
                "closed_by_employer_services": "CLOSED"}
    for r in recs:
        if r["type"] == "migrated":
            continue
        rows.append((legacy.get(r["job_id"], r["job_id"]), utc_to_local(r["ts"]).date(), kind_new[r["type"]],
                     r.get("noc"), {"self_service": "S", "employer_services": "E"}.get(r.get("source"))))
    ev = pd.DataFrame(rows, columns=["pid", "date", "kind", "occ", "channel"])
    return ev


def read_employers(tgt):
    e = pd.read_csv(os.path.join(tgt, "workshore_employer_accounts.csv"), dtype=str)
    return e


def read_qevs(tgt):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(tgt, "qevs_2026q3_release_tables.xlsx"), data_only=True)
    ws = wb["Table 1"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[4]
    dates = {}
    for j, h in enumerate(hdr):
        if isinstance(h, str) and re.match(r"\d\d [A-Z][a-z]{2} \d{4}$", h):
            dates[j] = dt.datetime.strptime(h, "%d %b %Y").date()
    est, naics = {}, {}
    for r in rows[5:]:
        if not r or r[0] in (None, "All sectors") or not isinstance(r[1], str) or not r[1]:
            continue
        naics[r[0]] = r[1]
        for j, d in dates.items():
            est[(r[0], d)] = int(r[j])
    return est, naics


def naics_sector(naics_code, naics_groups):
    two = int(str(naics_code)[:2])
    for title, spec in naics_groups.items():
        for part in spec.split(","):
            part = part.strip()
            if "-" in part:
                a, b = part.split("-")
                if int(a) <= two <= int(b):
                    return title
            elif int(part) == two:
                return title
    raise KeyError(naics_code)


def read_jobseekers(tgt):
    j = pd.read_csv(os.path.join(tgt, "workshore_registered_jobseekers_schedule_a.csv"), dtype=str)
    j["run"] = pd.to_datetime(j["run_date"])
    j = j.sort_values("run").drop_duplicates(["month_end", "noc_2021"], keep="last")
    return {(r.noc_2021, dt.date.fromisoformat(r.month_end)): int(r.registered_jobseekers) for r in j.itertuples()}


def schedule_a(tgt):
    """The Schedule A codes, read from the program guide's table."""
    import sys
    sys.path.insert(0, HERE)
    from pdftext import pdf_text
    txt = pdf_text(os.path.join(tgt, "in_demand_occupations_order_2027_program_guide.pdf"))
    i = txt.find("Schedule A. Occupations tested")
    return sorted(set(re.findall(r"\b(\d{5})\b", txt[i:])))


# ---------------------------------------------------------------------------------------------- survival
def km_table(durs, events):
    d = np.asarray(durs, dtype=float)
    e = np.asarray(events, dtype=int)
    order = np.argsort(d, kind="mergesort")
    d, e = d[order], e[order]
    times, surv = [], []
    S, n, i = 1.0, len(d), 0
    at_risk = n
    while i < n:
        t = d[i]
        j = i
        ev = 0
        while j < n and d[j] == t:
            ev += e[j]
            j += 1
        if ev:
            S *= 1.0 - ev / at_risk
            times.append(t)
            surv.append(S)
        at_risk -= j - i
        i = j
    return (np.array(times), np.array(surv))


def S_at(tab, a):
    times, surv = tab
    k = np.searchsorted(times, a, side="right") - 1
    return 1.0 if k < 0 else float(surv[k])


def weibull_table(durs, events):
    """Weibull fitted by maximum likelihood with right censoring, returned as a function on ages."""
    from scipy.optimize import minimize
    d = np.asarray(durs, dtype=float)
    e = np.asarray(events, dtype=float)

    def nll(th):
        k, lam = math.exp(th[0]), math.exp(th[1])
        z = d / lam
        return -(e * (math.log(k) - math.log(lam) + (k - 1) * np.log(z)) - z ** k).sum()

    r = minimize(nll, [0.2, math.log(max(np.median(d), 1.0))], method="Nelder-Mead", options={"xatol": 1e-8, "fatol": 1e-10, "maxiter": 4000})
    k, lam = math.exp(r.x[0]), math.exp(r.x[1])
    return ("weibull", k, lam)


def S_any(tab, a):
    if isinstance(tab, tuple) and isinstance(tab[0], str) and tab[0] == "weibull":
        _, k, lam = tab
        return math.exp(-((max(a, 0.0) / lam) ** k))
    return S_at(tab, a)


def es_durations(snap, ev, source="board", tgt=None):
    """Durations of Employer Services postings from publication to closure, by occupation."""
    if source == "cases":
        import openpyxl
        wb = openpyxl.load_workbook(os.path.join(tgt, "employer_services_vacancy_cases.xlsx"), data_only=True)
        out = defaultdict(lambda: ([], []))
        for ws in wb.worksheets:
            for r in ws.iter_rows(min_row=5, values_only=True):
                if not r or r[0] is None:
                    continue
                opened = r[5].date() if hasattr(r[5], "date") else r[5]
                if opened < dt.date(2025, 10, 1):
                    continue
                occ = str(r[3])
                if r[7] is not None:
                    od = r[7].date() if hasattr(r[7], "date") else r[7]
                    out[occ][0].append((od - opened).days)
                    out[occ][1].append(1)
                else:
                    out[occ][0].append((EXTRACT - opened).days)
                    out[occ][1].append(0)
        return out
    pub = ev[ev["kind"] == "PUBLISHED"].drop_duplicates("pid").set_index("pid")
    clo = ev[ev["kind"] == "CLOSED"].drop_duplicates("pid").set_index("pid")["date"]
    out = defaultdict(lambda: ([], []))
    for pid, r in pub.iterrows():
        if r["channel"] != "E":
            continue
        if pid in clo.index:
            out[r["occ"]][0].append((clo[pid] - r["date"]).days)
            out[r["occ"]][1].append(1)
        else:
            out[r["occ"]][0].append((EXTRACT - r["date"]).days)
            out[r["occ"]][1].append(0)
    return out


def survival_tables(durs, kind="km", pooled=False):
    if pooled:
        allD = sum((v[0] for v in durs.values()), [])
        allE = sum((v[1] for v in durs.values()), [])
        t = km_table(allD, allE) if kind == "km" else weibull_table(allD, allE)
        return defaultdict(lambda: t)
    out = {}
    for occ, (dd, ee) in durs.items():
        out[occ] = km_table(dd, ee) if kind == "km" else weibull_table(dd, ee)
    return out


# ---------------------------------------------------------------------------------------------- weights
def next_events(ev):
    by = defaultdict(list)
    for pid, d, k, _o, _c in ev.itertuples(index=False):
        by[pid].append((d, k))
    for pid in by:
        by[pid].sort()
    return by


def posting_weight(row, d, evby, tabs, mode):
    if row.channel == "E" or mode in ("live", "raw"):
        return 1.0
    if mode == "eonly":
        return 0.0
    e_last = row.term_last
    s = e_last - dt.timedelta(days=TERM - 1)       # the current term's first day
    e = e_last + dt.timedelta(days=1)             # the first day after the term
    a = (d - row.posted).days
    a_s = (s - row.posted).days
    a_e = (e - row.posted).days
    evs = [(x, k) for x, k in evby.get(row.pid, []) if s <= x <= e]
    renewed = any(k == "RENEWED" for x, k in evs)
    removed_after = any(k == "REMOVED" and x > d for x, k in evs)
    expired = any(k == "EXPIRED" for x, k in evs) and not renewed
    tab = tabs[row.occ]
    if mode == "uncond":
        return S_any(tab, a) / max(S_any(tab, a_s), 1e-12)
    if mode == "drop_expired":
        return 0.0 if expired else 1.0
    if renewed or removed_after:
        return 1.0
    if expired:
        num = S_any(tab, a) - S_any(tab, a_e)
        den = S_any(tab, a_s) - S_any(tab, a_e)
        return 0.0 if den <= 1e-12 else min(1.0, max(0.0, num / den))
    raise AssertionError("posting %s live on %s has no outcome in its term" % (row.pid, d))


def compute(tgt, mode="gold", surv="km", dur_source="board", cache=None):
    c = cache if cache is not None else {}
    if "snap" not in c:
        c["snap"] = read_snapshots(tgt)
        c["ev"] = read_events(tgt)
        c["evby"] = next_events(c["ev"])
        c["emp"] = read_employers(tgt)
        c["qevs"], c["naics"] = read_qevs(tgt)
        c["js"] = read_jobseekers(tgt)
        c["sched"] = schedule_a(tgt)
        c["sector_of"] = {r.employer_number: naics_sector(r.naics_2017, c["naics"]) for r in c["emp"].itertuples()}
    snap, evby, qevs, js, sched = c["snap"], c["evby"], c["qevs"], c["js"], c["sched"]
    key = ("durs", dur_source)
    if key not in c:
        c[key] = es_durations(snap, c["ev"], dur_source, tgt)
    durs = c[key]
    tabs = survival_tables(durs, "km" if surv == "km" else "weibull", pooled=(mode == "pooled"))
    V = defaultdict(float)
    per_date = {}
    for d in REF_DATES:
        live = snap[snap["snap"] == d]
        wsec = defaultdict(float)
        wocc = defaultdict(float)
        for row in live.itertuples(index=False):
            w = posting_weight(row, d, evby, tabs, "gold" if mode == "pooled" else mode)
            sec = c["sector_of"][row.employer]
            wsec[sec] += w * row.positions
            wocc[(row.occ, sec)] += w * row.positions
        vd = defaultdict(float)
        for (occ, sec), x in wocc.items():
            if mode == "raw":
                vd[occ] += x
            elif wsec[sec] > 0:
                vd[occ] += qevs[(sec, d)] * x / wsec[sec]
        per_date[d] = dict(vd)
        for occ, x in vd.items():
            V[occ] += x
    J = {o: sum(js[(o, d)] for d in REF_DATES) for o in sched}
    R = {o: (J[o] / V[o] if V[o] > 0 else float("inf")) for o in sched}
    listed = sorted(o for o in sched if R[o] <= THRESHOLD)
    return {"V": dict(V), "J": J, "R": R, "listed": listed, "per_date": per_date}


def ladder(tgt):
    cache = {}
    out = {}
    for name, kw in [("gold", dict(mode="gold")), ("live", dict(mode="live")), ("raw", dict(mode="raw")),
                     ("drop_expired", dict(mode="drop_expired")), ("pooled", dict(mode="pooled")),
                     ("uncond", dict(mode="uncond")), ("eonly", dict(mode="eonly")),
                     ("gold_weibull", dict(mode="gold", surv="weibull")),
                     ("gold_cases", dict(mode="gold", dur_source="cases"))]:
        out[name] = compute(tgt, cache=cache, **kw)
    return out, cache


if __name__ == "__main__":
    import sys
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    res, _ = ladder(tgt)
    for k, v in res.items():
        print(k, len(v["listed"]), v["listed"])
