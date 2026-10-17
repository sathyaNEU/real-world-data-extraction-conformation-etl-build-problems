"""The pack's data files, written from the world, and the bundle read back from them. Every figure calc.py and
asks.py compute comes from the bundle, so it is the shipped files' arithmetic."""
from __future__ import annotations

import collections
import csv
import datetime as dt
import json
import os

import numpy as np

import common as K
import world as W

HIST_DAYS = list(range(0, W.dnum(W.HIST_END) + 1))
# payroll's practice before its April 2026 transfer screen: a casual moving stores resigns at one and is re-engaged at
# the other under a new employee number, the re-engagement form defaulting the new cost centre's effective date to the
# day it is keyed. The moves agreed at the November 2025 roster review were keyed together on the review's date; the
# Ballarat school leavers' moves to Melbourne were keyed together on the Monday after the VCE results came out.
REENG_BEFORE = dt.date(2026, 4, 1)
REVIEW_KEYED = dt.date(2025, 11, 20)
RESULTS_KEYED = dt.date(2025, 12, 15)
XMAS_DAYS = list(range(W.dnum(W.PEAK26[0]), W.dnum(W.PEAK26[1]) + 1))
LEGACY_LAST = W.KWS_ROSTERS_FROM - dt.timedelta(days=1)


class World:
    pass


def prepare():
    """the world: people, the published rosters, every call-in of the history and its offers"""
    Wd = World()
    Wd.cas, Wd.perms = W.make_people(W.stream(1))
    Wd.crew = list(range(25))
    Wd.roster_h = W.build_rosters(W.stream(2), Wd.cas, Wd.perms, HIST_DAYS, crew=Wd.crew)
    Wd.roster_p = W.build_rosters(W.stream(3), Wd.cas, Wd.perms, XMAS_DAYS)
    needs, vac, absd = W.make_needs(W.stream(4), Wd.roster_h, Wd.cas, Wd.perms, set(HIST_DAYS))
    sim = W.Cascade(Wd.cas, Wd.roster_h, vac, absd, W.stream(5), W.stream(6), W.stream(7))
    sim.run(needs)
    Wd.needs, Wd.postings, Wd.offers, Wd.feats = needs, sim.postings, sim.offers, sim.feats
    Wd.vacated, Wd.absent_day = vac, absd
    keys(Wd)
    return Wd


# --------------------------------------------------------------------------- keys
def keys(Wd):
    """payroll numbers (one per engagement, issued in start order), KWS person codes, dates of birth"""
    rng = W.stream(11)
    starts = []
    for c in Wd.cas:
        starts.append((c.start, "C", c.idx, 0))
        if c.gap:
            starts.append((c.gap[1], "C", c.idx, 1))
    for p in Wd.perms:
        p_start = dt.date(2004, 1, 1) + dt.timedelta(days=int(rng.integers(0, 7600)))
        starts.append((p_start, "P", p.idx, 0))
    for m in Wd.crew:
        starts.append((dt.date(2025, 11, 3) + dt.timedelta(days=int(rng.integers(0, 10))), "R", m, 0))
    starts.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
    num = 104_117
    Wd.pay = {}
    Wd.perm_start = {}
    for d, kind, i, eng in starts:
        num += int(rng.integers(1, 9))
        Wd.pay[(kind, i, eng)] = num
        if kind == "P":
            Wd.perm_start[i] = d
    # KWS loaded every casual on its books at go-live in payroll-number order, then each new hire as set up
    live = W.D0 - dt.timedelta(days=21)
    first = sorted([c for c in Wd.cas if c.start <= live], key=lambda c: Wd.pay[("C", c.idx, 0)])
    later = sorted([c for c in Wd.cas if c.start > live], key=lambda c: (c.start, Wd.pay[("C", c.idx, 0)]))
    code = 30_000 + int(rng.integers(100, 900))
    Wd.code = {}
    for c in first + later:
        code += int(rng.integers(1, 4))
        Wd.code[c.idx] = "K%05d" % code
    # the re-engagements of the moves before April 2026: each numbered at its start, in the first number free after
    # the last one issued by then (the person code carries over)
    Wd.reeng = {}
    used = set(Wd.pay.values())
    issued = sorted((d, Wd.pay[(kind, i, eng)]) for d, kind, i, eng in starts)
    for c in sorted((c for c in Wd.cas if c.moves and c.moves[0][0] < REENG_BEFORE), key=lambda c: (c.moves[0][0], c.idx)):
        when, to, _ = c.moves[0]
        no = max(num for d, num in issued if d <= when) + 1
        while no in used:
            no += 1
        used.add(no)
        keyed = RESULTS_KEYED if c.store0 == "RG" else REVIEW_KEYED
        Wd.pay[("C", c.idx, "R")] = no
        Wd.reeng[c.idx] = dict(when=when, keyed=keyed, to=to, no=no)
    Wd.dob = {}
    for c in Wd.cas:
        lo, hi = {"school": (15.1, 17.9), "uni": (18.2, 23.5), "parent": (31.0, 48.0), "flex": (19.5, 63.0)}[c.typ0]
        if c.moves and c.moves[0][2] == "uni":
            lo, hi = 17.0, 17.9
        age = rng.uniform(lo, hi)
        Wd.dob[c.idx] = W.D0 - dt.timedelta(days=int(age * 365.25))


def payroll_no(Wd, who, d):
    kind, i = who
    if kind == "C":
        c = Wd.cas[i]
        r = Wd.reeng.get(i)
        if r and d >= r["when"]:
            return Wd.pay[("C", i, "R")]
        return Wd.pay[("C", i, 1 if (c.gap and d >= c.gap[1]) else 0)]
    return Wd.pay[(kind, i, 0)]


# --------------------------------------------------------------------------- writers
def _csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)


def need_in_window(nd):
    return 0 <= nd["day"] <= W.dnum(W.HIST_END)


def write_register(path, Wd):
    rows = []
    ids = {}
    order = sorted((p for p in Wd.postings if need_in_window(Wd.needs[p["need"]])), key=lambda p: (p["raised"], p["pid"]))
    rng = W.stream(12)
    cid = 2_184_000 + int(rng.integers(0, 500))
    for p in order:
        cid += 1 + (1 if rng.random() < 0.08 else 0)
        ids[p["pid"]] = cid
        nd = Wd.needs[p["need"]]
        d = W.ddate(nd["day"])
        absent = "" if nd["absent"] is None else str(payroll_no(Wd, nd["absent"], d))
        rows.append([cid, K.LOC[nd["store"]], K.utc_str(nd["s"]), K.utc_str(nd["e"]), K.REASON[nd["kind"]], absent,
                     K.utc_str(p["raised"]), K.utc_str(p["closed"]), p["outcome"],
                     Wd.code[p["filled_by"]] if p["filled_by"] is not None else ""])
    _csv(path, ["callin_id", "location_id", "shift_start_utc", "shift_end_utc", "reason", "absent_payroll_no",
                "raised_at", "closed_at", "outcome", "filled_by"], rows)
    Wd.callin_id = ids
    return len(rows)


def write_offers(path, Wd):
    rows = []
    rng = W.stream(13)
    oid = 9_410_000 + int(rng.integers(0, 900))
    for (pid, idx, toff, tresp, resp) in sorted(Wd.offers, key=lambda o: (o[2], o[0], o[1])):
        if pid not in Wd.callin_id:
            continue
        nd = Wd.needs[Wd.postings[pid]["need"]]
        oid += 1
        n = nd["day"]
        rows.append(["OF%08d" % oid, Wd.callin_id[pid], K.LOC[nd["store"]], W.ddate(n).isoformat(),
                     K.hhmm(nd["s"] - n * 1440), K.hhmm(nd["e"] - n * 1440), Wd.code[idx], K.utc_str(toff),
                     K.ANSWER[resp], "" if resp == "N" else K.utc_str(tresp)])
    _csv(path, ["offer_id", "callin_id", "location_id", "shift_date", "shift_start", "shift_end", "person_code",
                "offered_at", "response", "responded_at"], rows)
    return len(rows)


def _who_str(Wd, ln, d):
    who = ln["who"]
    return "" if who is None else str(payroll_no(Wd, who, d))


def write_legacy(path, Wd):
    rows = []
    for s in sorted(W.STORES, key=lambda s: K.STORE_NO[s]):
        for ln in sorted(Wd.roster_h[s], key=lambda l: (l["day"], l["start"], l["end"], l["code"])):
            d = W.ddate(ln["day"])
            if d > LEGACY_LAST:
                continue
            fri = W.ddate((ln["day"] // 7) * 7)
            status = "VACANT" if ln["who"] is None else ("RELIEF" if ln["who"][0] == "R" else "")
            rows.append([W.STORE_NAMES[s].upper(), fri.strftime("%d/%m/%Y"), d.strftime("%d/%m/%Y"), d.strftime("%a"),
                         ln["code"], K.ampm(ln["start"]), K.ampm(ln["end"]), "%.2f" % ((ln["end"] - ln["start"]) / 60.0),
                         _who_str(Wd, ln, d), status])
    _csv(path, ["Store", "Week Commencing", "Date", "Day", "Shift", "Start", "Finish", "Hrs", "Emp No", "Status"], rows)
    return len(rows)


def emp_type(Wd, who):
    if who is None:
        return ""
    if who[0] == "C":
        return "CAS"
    return Wd.perms[who[1]].emp_type


def write_kws_roster(path, Wd):
    rows = []
    for s in sorted(W.STORES, key=lambda s: K.STORE_NO[s]):
        for ln in sorted(Wd.roster_h[s], key=lambda l: (l["day"], l["start"], l["end"], l["code"])):
            d = W.ddate(ln["day"])
            if d < W.KWS_ROSTERS_FROM:
                continue
            fri = W.ddate((ln["day"] // 7) * 7)
            rows.append([K.LOC[s], fri.isoformat(), d.isoformat(), ln["code"], K.hhmm(ln["start"]), K.hhmm(ln["end"]),
                         "%.2f" % K.paid_hours(ln["start"], ln["end"]), _who_str(Wd, ln, d), emp_type(Wd, ln["who"]),
                         "OPEN" if ln["who"] is None else "ROSTERED"])
    _csv(path, ["location_id", "roster_week", "shift_date", "shift_code", "start_time", "end_time", "paid_hours",
                "payroll_no", "emp_type", "line_status"], rows)
    return len(rows)


def write_people(path, Wd):
    rows = []
    for c in sorted(Wd.cas, key=lambda c: Wd.code[c.idx]):
        status = "ACTIVE" if c.active(W.HIST_END) else "INACTIVE"
        rows.append([Wd.code[c.idx], payroll_no(Wd, ("C", c.idx), W.HIST_END), K.LOC[c.home(W.HIST_END)],
                     "Y" if c.opt_in else "N", W.service_date(c, W.HIST_END).isoformat(), status])
    _csv(path, ["person_code", "payroll_no", "home_location", "cluster_callins", "service_date", "status"], rows)
    return len(rows)


def write_payroll(path, Wd):
    rows = []
    far = ""
    for c in Wd.cas:
        engs = []
        r = Wd.reeng.get(c.idx)
        if c.gap:
            engs.append((Wd.pay[("C", c.idx, 0)], c.start, c.gap[0], "", None))
            engs.append((Wd.pay[("C", c.idx, 1)], c.gap[1], c.end, str(Wd.pay[("C", c.idx, 0)]), None))
        elif r:
            # a move recorded as a resignation and a re-engagement: the new cost centre from the day it was keyed
            engs.append((Wd.pay[("C", c.idx, 0)], c.start, r["when"] - dt.timedelta(days=1), "", None))
            engs.append((r["no"], r["when"], c.end, str(Wd.pay[("C", c.idx, 0)]), r["keyed"]))
        else:
            engs.append((Wd.pay[("C", c.idx, 0)], c.start, c.end, "", None))
        for no, a, b, prev, keyed in engs:
            end = "" if b > W.HIST_END else b.isoformat()
            # cost-centre periods inside the engagement
            cuts = [(a, c.store0)]
            for when, to, _ in c.moves:
                if a < when <= b:
                    cuts.append((when, to))
                elif when <= a:
                    cuts = [(a, to)]
            if keyed is not None:
                cuts[0] = (keyed, cuts[0][1])
            for k, (f, st) in enumerate(cuts):
                t = (cuts[k + 1][0] - dt.timedelta(days=1)).isoformat() if k + 1 < len(cuts) else end
                rows.append([no, Wd.dob[c.idx].isoformat(), "CASUAL", a.isoformat(), end, K.CC[st], f.isoformat(),
                             t, prev])
    rows.sort(key=lambda r: (r[0], r[6]))
    _csv(path, ["employee_no", "date_of_birth", "employment_type", "engagement_start", "engagement_end", "cost_centre",
                "cc_effective_from", "cc_effective_to", "previous_employee_no"], rows)
    return len(rows)


DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def availability_versions(c, first, last):
    """effective-dated weekly patterns: a new version starts on the first date whose own weekday's windows differ
    from that weekday's in the version running; no version runs while the casual is off the books"""
    out = []
    cur = None
    d = first
    while d <= last:
        if not c.active(d):
            if cur is not None:
                cur["to"] = d - dt.timedelta(days=1)
                out.append(cur)
                cur = None
            d += dt.timedelta(days=1)
            continue
        wd = DAYS[d.weekday()]
        w = W.windows(c, d)
        if cur is None:
            cur = {"from": d, "pat": {wd: w}}
        elif wd in cur["pat"] and cur["pat"][wd] != w:
            cur["to"] = d - dt.timedelta(days=1)
            out.append(cur)
            cur = {"from": d, "pat": {wd: w}}
        else:
            cur["pat"][wd] = w
        d += dt.timedelta(days=1)
    if cur is not None:
        cur["to"] = None if c.active(W.AS_OF) else last
        out.append(cur)
    # a weekday no date of a short version falls on carries the windows the casual declared for it going forward:
    # its next date after the version starts
    for v in out:
        for wd in DAYS:
            if wd in v["pat"]:
                continue
            dd = v["from"]
            while DAYS[dd.weekday()] != wd:
                dd += dt.timedelta(days=1)
            v["pat"][wd] = W.windows(c, dd) if c.active(dd) else []
    return out


def write_availability(path, Wd):
    first, last = W.D0, W.HIST_END
    people = []
    for c in sorted(Wd.cas, key=lambda c: Wd.code[c.idx]):
        vers = []
        for v in availability_versions(c, max(first, c.start), min(last, c.end)):
            vers.append({"effective_from": v["from"].isoformat(),
                         "effective_to": v["to"].isoformat() if v["to"] else None,
                         "weekly": {dname: [[K.hhmm(a), K.hhmm(b)] for a, b in v["pat"][dname]] for dname in DAYS}})
        people.append({"person_code": Wd.code[c.idx], "profiles": vers})
    doc = {"export": "KWS availability profiles", "extracted": "2026-11-12T07:40:00Z", "time_basis": "store time",
           "people": people}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return len(people)


def write_stores(path):
    rows = []
    for s in sorted(W.STORES, key=lambda s: K.STORE_NO[s]):
        rows.append([K.STORE_NO[s], W.STORE_NAMES[s], K.LOC[s], K.CC[s], K.CLUSTER_NAME[W.STORES[s]["cluster"]],
                     K.OPENED[s]])
    _csv(path, ["store_no", "store_name", "kws_location", "cost_centre", "callin_cluster", "opened"], rows)
    return len(rows)


def write_calendar(path):
    rows = []
    names = {0: "Term 3", 1: "Term 4", 2: "Term 1", 3: "Term 2", 4: "Term 3", 5: "Term 4"}
    for k, (a, b) in enumerate(W.TERMS):
        rows.append(["school term", "%s %d" % (names[k], a.year), a.isoformat(), b.isoformat(), "Victorian government schools"])
    for d, name in [(dt.date(2025, 9, 26), "Friday before the AFL Grand Final"), (dt.date(2025, 11, 4), "Melbourne Cup"),
                    (dt.date(2025, 12, 25), "Christmas Day"), (dt.date(2025, 12, 26), "Boxing Day"),
                    (dt.date(2026, 1, 1), "New Year's Day"), (dt.date(2026, 1, 26), "Australia Day"),
                    (dt.date(2026, 3, 9), "Labour Day"), (dt.date(2026, 4, 3), "Good Friday"),
                    (dt.date(2026, 4, 4), "Saturday before Easter Sunday"), (dt.date(2026, 4, 5), "Easter Sunday"),
                    (dt.date(2026, 4, 6), "Easter Monday"), (dt.date(2026, 4, 25), "ANZAC Day"),
                    (dt.date(2026, 6, 8), "King's Birthday"), (dt.date(2026, 9, 25), "Friday before the AFL Grand Final"),
                    (dt.date(2026, 11, 3), "Melbourne Cup"), (dt.date(2026, 12, 25), "Christmas Day"),
                    (dt.date(2026, 12, 26), "Boxing Day")]:
        note = "metropolitan Melbourne" if name == "Melbourne Cup" else "statewide"
        rows.append(["public holiday", name, d.isoformat(), d.isoformat(), note])
    rows.sort(key=lambda r: (r[2], r[0]))
    _csv(path, ["kind", "name", "from", "to", "applies"], rows)
    return len(rows)


def write_all(out, Wd):
    import docs as D
    import xlsx as X
    counts = collections.OrderedDict()
    counts[K.F_REGISTER] = write_register(os.path.join(out, K.F_REGISTER), Wd)
    counts[K.F_OFFERS] = write_offers(os.path.join(out, K.F_OFFERS), Wd)
    counts[K.F_LEGACY] = write_legacy(os.path.join(out, K.F_LEGACY), Wd)
    counts[K.F_KWS] = write_kws_roster(os.path.join(out, K.F_KWS), Wd)
    counts[K.F_PEOPLE] = write_people(os.path.join(out, K.F_PEOPLE), Wd)
    counts[K.F_PAYROLL] = write_payroll(os.path.join(out, K.F_PAYROLL), Wd)
    counts[K.F_AVAIL] = write_availability(os.path.join(out, K.F_AVAIL), Wd)
    counts[K.F_STORES] = write_stores(os.path.join(out, K.F_STORES))
    counts[K.F_CAL] = write_calendar(os.path.join(out, K.F_CAL))
    counts[K.F_XMAS] = X.write_christmas(os.path.join(out, K.F_XMAS), Wd)
    counts[K.F_PLAN] = X.write_plan(os.path.join(out, K.F_PLAN))
    D.write_all(out, Wd, counts)
    return counts
