"""The ask layer's ceiling on Part 0's weights (38 recommendation, 7 instruction-following, 55 asks), run on the cut pack.

One ask is left: hospital-clinic visits in each financial quarter of 2025-26 by specialty, counted by visit date (28
cells). Every route a careful solver could take is scored on its own code, read straight from the files (the queue
events' hospital-form check-ins and the clinic register), against figures.json, a hit being the exact whole number:

  register      the old codes named by matching their forms' issue weekdays to the register's clinic_days
  remedy        the same, after the battery's code-against-schedule check, re-deriving each off-schedule form's clinic
                from the one register row that lists its weekday (the item's literal remedy)
  validated     the careful solver: the register route tested on the forms the register already codes inside the
                ask's window; the test fails, the failures all fall before 1 April, so the clinics changed days then,
                and each old code is linked to the new code whose forms issued before 1 April share its weekdays
  rekey         the battery's re-keyed records across two systems: old PAS codes matched to new PAS codes on the
                weekdays of the forms issued either side of the switch, before the April templates
  rekey-all     the same match on every new-code form in the extract (a weekday set from all of them)
  rekey-april   the same match on the new codes' forms from 1 April (their weekday sets in the current templates)
  full          the full includer (figures.json's own route), the control

The cracker is the validated route (the ruling in the design note's Ask sheet: a careful solver tests the register's
clinic_days on the register-coded forms before naming 16,417 visits by them). The mirror files the default path's
42,500 and takes the ask the same way: the ask reads nothing the call constructs.
"""
import datetime as dt
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
FY0, FY1, APR = dt.date(2025, 4, 1), dt.date(2026, 3, 31), dt.date(2026, 4, 1)
DN = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4}
EVENTS = "phlebotomy_queue_events_2024-11-18_to_2026-09-30.csv"
REGISTER = "outpatient_clinic_codes.csv"


def quarter(d):
    return "Q%d" % (((d.month - 4) % 12) // 3 + 1)


def load(target):
    ev = pd.read_csv(os.path.join(target, EVENTS), dtype=str)
    h = ev[(ev.event_type == "CHECKED_IN") & (ev.request_type == "HOSP")].copy()
    h["d"] = pd.to_datetime(h.event_utc, utc=True).dt.tz_convert("Europe/London").dt.date
    h["rd"] = pd.to_datetime(h.request_date).dt.date
    h["wd"] = [x.weekday() for x in h.rd]
    reg = pd.read_csv(os.path.join(target, REGISTER), dtype=str)
    spec = dict(zip(reg.clinic_code, reg.specialty))
    days = {r.clinic_code: frozenset(DN[x.strip()] for x in r.clinic_days.split(",")) for r in reg.itertuples()}
    return h, spec, days


def table(h, code_spec, names):
    y = h[(h.d >= FY0) & (h.d <= FY1)].copy()
    y["sp"] = y.request_org.map(code_spec)
    y["q"] = [quarter(d) for d in y.d]
    t = y.groupby(["sp", "q"]).size()
    return {sp: {q: int(t.get((sp, q), 0)) for q in ("Q1", "Q2", "Q3", "Q4")} for sp in names}


def match(old_wd, new_wd):
    out = {}
    for c, w in old_wd.items():
        hit = [n for n, x in new_wd.items() if x == w]
        out[c] = hit[0] if len(hit) == 1 else None
    return out


def routes(target):
    h, spec, days = load(target)
    old = sorted(set(h.request_org) - set(spec))
    old_wd = {c: frozenset(h[h.request_org == c].wd) for c in old}
    newf = h[h.request_org.isin(list(spec))]
    out = {}
    # register: old codes by weekday against the register's clinic_days
    m = match(old_wd, days)
    reg_map = dict(spec, **{c: spec[n] for c, n in m.items() if n})
    out["register"] = (table(h, reg_map, spec.values()), m)
    # remedy: off-schedule register-coded forms re-derived from the one register row listing their weekday
    hr = h.copy()
    lists = {w: [c for c, x in days.items() if w in x] for w in range(5)}
    off = hr.request_org.isin(list(spec)) & pd.Series(
        [w not in days.get(c, frozenset(range(5))) for c, w in zip(hr.request_org, hr.wd)], index=hr.index)
    rederived = 0
    for i in hr.index[off]:
        cand = lists[hr.at[i, "wd"]]
        if len(cand) == 1:
            hr.at[i, "request_org"] = cand[0]
            rederived += 1
    out["remedy"] = (table(hr, reg_map, spec.values()), {"off-schedule forms": int(off.sum()), "re-derived": rederived})
    # validated: the register route tested on the register-coded forms inside the ask's window
    y = newf[(newf.d >= FY0) & (newf.d <= FY1)]
    fails = int(sum(1 for c, w in zip(y.request_org, y.wd) if w not in days[c]))
    off_all = [(r, c) for r, c, w in zip(newf.rd, newf.request_org, newf.wd) if w not in days[c]]
    before = sum(1 for r, _ in off_all if r < APR)
    pre = newf[newf.rd < APR]
    pre_wd = {n: frozenset(pre[pre.request_org == n].wd) for n in spec}
    m3 = match(old_wd, pre_wd)
    val_map = dict(spec, **{c: spec[n] for c, n in m3.items() if n})
    out["validated"] = (table(h, val_map, spec.values()),
                        {"register-coded 2025-26 visits": len(y), "off the listed weekdays": fails,
                         "off-schedule forms in the extract": len(off_all), "of them issued before 1 April": before})
    # rekey: old to new PAS codes on the forms issued either side of the switch (before the April templates)
    out["rekey"] = (table(h, val_map, spec.values()), m3)
    # rekey-all: weekday sets from every new-code form in the extract
    all_wd = {n: frozenset(newf[newf.request_org == n].wd) for n in spec}
    m5 = match(old_wd, all_wd)
    out["rekey-all"] = (table(h, dict(spec, **{c: spec[n] for c, n in m5.items() if n}), spec.values()), m5)
    # rekey-april: weekday sets from the new codes' forms in the current templates
    apr = newf[newf.rd >= APR]
    apr_wd = {n: frozenset(apr[apr.request_org == n].wd) for n in spec}
    m6 = match(old_wd, apr_wd)
    out["rekey-april"] = (table(h, dict(spec, **{c: spec[n] for c, n in m6.items() if n}), spec.values()), m6)
    return out


def hits(F, tab):
    return sum(int(tab.get(sp, {}).get(q) == v) for sp, qq in F["hospital_visits_2025_26"].items() for q, v in qq.items())


def score(target):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    cells = sum(len(q) for q in F["hospital_visits_2025_26"].values())
    R = routes(target)
    kept = {}
    for name in ("register", "remedy", "validated", "rekey", "rekey-all", "rekey-april"):
        tab, info = R[name]
        kept[name] = hits(F, tab)
        print("ask A, %-12s %2d of %d   %s" % (name, kept[name], cells, info))
    print("ask A, %-12s %2d of %d   (figures.json's own route)" % ("full", cells, cells))
    r = 5.0

    def pair(kc, km):
        C = 38 + 7 + 55.0 * kc / cells
        S = r + 7 + 55.0 * km / cells
        return C, S, (C + S) / 2.0
    for label, route in (("the careful cracker (validated)", "validated"), ("a cracker that skips the validation (register)", "register")):
        k = kept[route]
        C, S, P = pair(k, k)
        print("%s: on the call %.1f, the mirror at 42,500 on the same ask route %.1f, pair %.1f, mirror leakage %.1f per cent"
              % (label, C, S, P, 100.0 * k / cells))
        print("  two careful responses on the call: %.1f each" % C)
    C, S, P = pair(kept["validated"], kept["validated"])
    print("Pair ceiling: %.1f" % P)
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * kept["validated"] / cells))
    print("Cracker: %s" % ("misses every row" if kept["validated"] == 0 else "keeps %d of %d rows" % (kept["validated"], cells)))
    return P, 100.0 * kept["validated"] / cells, kept


if __name__ == "__main__":
    score(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
