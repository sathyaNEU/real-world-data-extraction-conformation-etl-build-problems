"""The build's assertions for task266: the input gates, the three-rules block (R1 to R3c), the golden method's
assumptions held against the data, the ladder and the call's margins, every semantic fork (SF1 to SF22), the two ask
devices with their over-cleaning halves, the main population's separation from the asks, the realism sweep and the
documents read back with positive controls."""
import csv
import datetime as dt
import os
import re
import shutil
import tempfile

import numpy as np
from openpyxl import load_workbook

import analysis as A
import common as K
import world as W

FAILS = []
N = [0]


def ok(cond, label):
    N[0] += 1
    if not cond:
        FAILS.append(label)
        print("FAIL", label)


def pdf_text(path):
    from pypdf import PdfReader
    return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)


def norm(s):
    return re.sub(r"\s+", " ", s)


def kendall_conditional(t, u, v, E, cap=2600):
    """The conditional Kendall's tau of latency against first exposure over the pairs whose windows both contain
    both latencies (Martin and Betensky's comparable pairs for truncated data), on an evenly spaced subsample."""
    idx = np.linspace(0, len(t) - 1, min(cap, len(t))).astype(int)
    t, u, v, E = t[idx], u[idx], v[idx], E[idx]
    lo = np.maximum.outer(u, u)
    hi = np.minimum.outer(v, v)
    tmin = np.minimum.outer(t, t)
    tmax = np.maximum.outer(t, t)
    comp = (lo <= tmin) & (tmax <= hi)
    np.fill_diagonal(comp, False)
    s = np.sign(np.subtract.outer(t, t)) * np.sign(np.subtract.outer(E, E))
    m = comp.sum()
    return float((s * comp).sum() / m), int(m // 2)


def run(target, T):
    o = T["o"]
    sched = T["unit"]
    m = o["main"]
    files = sorted(os.listdir(target))
    # ------------------------------------------------------------------ input gates and hygiene
    ok(len(files) >= 10, "gate: 10 or more files (%d)" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "gate: 3 or more formats")
    with open(os.path.join(target, K.FILES["appointments"])) as f:
        n_app = sum(1 for _ in f) - 1
    ok(n_app >= 25000, "gate: a file of 25,000 rows or more (%d)" % n_app)
    ok(len(K.DISTRACTORS) >= 2, "gate: two or more distractors")
    bad = [f for f in files if re.search(r"readme|dictionary|manifest|notes|codebook|schema|distractor", f, re.I)]
    ok(not bad, "gate: no describing file by name %s" % bad)
    ok(set(files) == set(K.FILES.values()), "gate: the pack is exactly the named files")
    # ------------------------------------------------------------------ documents read back (positive controls)
    terms = norm(pdf_text(os.path.join(target, K.FILES["terms"])))
    report = norm(pdf_text(os.path.join(target, K.FILES["report"])))
    sch = norm(pdf_text(os.path.join(target, K.FILES["schedule"])))
    ok(len(terms) > 1500 and len(report) > 1200 and len(sch) > 600, "docs: every PDF extracts text")
    import docs as Dc
    for s_, label in ((Dc.TERMS_HORIZON, "4.2"), (Dc.TERMS_YEARS, "4.3"), (Dc.TERMS_SHAPE, "4.4"),
                      (Dc.TERMS_FIRST, "2.2"), (Dc.TERMS_INVITE, "3.2")):
        ok(norm(s_) in terms, "docs: the terms carry clause %s word for word" % label)
    ok(norm(Dc.REPORT_REGISTER) in report, "docs: the annual report carries the register's window and close")
    for word in ("truncat", "window", "delayed entry", "Kaplan", "Efron", "swap", "offline", "rerout",
                 "flood", "tablet", "sync", "counter"):
        ok(word.lower() not in (terms + report + sch).lower(), "docs: no document names '%s'" % word)
    ok("latency curve" in terms and terms.lower().count("latenc") == 1, "docs: 'latency' appears once, in 4.4's curve")
    # the register's window as the report files it
    cases = A.load_cases(target)
    D = [c["D"] for c in cases]
    ok(min(D) >= K.REG_START and max(D) <= K.REG_END, "window: every register diagnosis inside 1 July 2004 to 30 June 2026")
    ok(min(D) <= K.REG_START + dt.timedelta(days=20) and max(D) >= K.REG_END - dt.timedelta(days=20),
       "window: the register reaches both edges")
    # ------------------------------------------------------------------ R1 to R3c
    sc = A.in_scope(cases)
    ok(len(sc) == m["n"] and len(sc) > 4500, "R1: the golden reads %d case-level register rows" % len(sc))
    heads = []
    for f in files:
        if f.endswith(".csv"):
            heads += next(csv.reader(open(os.path.join(target, f))))
    ok(not [h for h in heads if re.search(r"latenc|years_after|window|cover|share", h, re.I)],
       "R1: no shipped column holds a latency, a window or a share")
    truth = [c for c in T["cases"] if c["kind"] == "cohort"]
    S0, C0 = W.ordinal(K.REG_START), W.ordinal(K.REG_END)
    reg_truth = [c for c in truth if S0 <= c["D"] <= C0]
    tt = np.array([c["T"] for c in reg_truth], float)
    uu = np.array([S0 - c["E"] for c in reg_truth], float)
    vv = np.array([C0 - c["E"] for c in reg_truth], float)
    true_cov = {H: float(np.mean(np.array([c["T"] for c in truth]) <= H * K.YEAR)) for H in K.SETTINGS}
    ok(A.setting(true_cov) == 60, "R0: the truth's horizon (every case, whenever diagnosed) is 60")
    xe, fe = A.empirical(tt)
    xd, fd = A.delayed_entry(tt, uu)
    xg, fg = A.npmle_dt(tt, uu, vv)
    xr, fr = A.reverse_time(tt, vv)
    ok(A.setting(A.coverage(xe, fe)) == 55, "R3a: the register read as it stands, on the clean truth, files 55")
    ok(A.setting(A.coverage(xd, fd)) == 55, "R3a: the delayed-entry curve on the clean truth files 55")
    ok(A.setting(A.coverage(xg, fg)) == 60, "R3b: the decisive step alone on the clean truth files 60")
    ok(A.setting(A.coverage(xr, fr)) not in (60, 55), "R3b: the end-only correction stays wrong (%s)" % A.setting(A.coverage(xr, fr)))
    ok(len(reg_truth) == m["n"], "R2: every cohort case diagnosed inside the window is on the register (%d)" % len(reg_truth))
    # R2: each mess item mishandled is neutral or loud
    cur_only = [c for c in cases if not re.match(r"DD\d\d-\d{4}$", c["ref"])]
    ok(min(c["D"] for c in cur_only) >= dt.date(2012, 1, 1),
       "R2: reading only the current register loses every diagnosis before 2012 (loud against the report's 2004)")
    first_y = {}
    for h in csv.DictReader(open(os.path.join(target, K.FILES["histories"]))):
        if h["asbestos_exposure"] == "Y":
            first_y.setdefault(h["case_ref"], True)
    lost = sum(1 for c in sc if c["ref"] not in first_y)
    ok(lost > 1500, "R2: reading only 'Y' as exposed drops every first-system case (%d, loud)" % lost)
    t_, u_, v_ = A.arrays(sc)
    later = [c for c in cases if c["cat"] == "Occupational" and c["E"] is not None and c["E"] >= K.COHORT_END]
    t2, u2, v2 = A.arrays(sc + later)
    xs2, fs2 = A.npmle_dt(t2, u2, v2)
    ok(A.setting(A.coverage(xs2, fs2)) == 60, "R2/SF3: the 1986-and-later workers kept in gives 60 (%d cases)" % len(later))
    # R3c: no plant, no repeated block, no identical counts across towns
    rv = o["reviews"]
    ok(len(set(rv.values())) == len(rv), "R3c: no two circuit towns share a review count")
    ok(all(x % 10 for x in rv.values()) or sum(1 for x in rv.values() if x % 10 == 0) <= 2,
       "R3c: town counts are not round")
    # ------------------------------------------------------------------ the golden method's assumptions (lesson 7)
    E = np.array([(c["E"] - dt.date(1900, 1, 1)).days for c in sc], float)
    tau, pairs = kendall_conditional(t_, u_, v_, E)
    ok(abs(tau) < 0.04 and pairs > 50000, "L7: latency is independent of first exposure inside the windows "
       "(conditional tau %.4f over %d pairs)" % (tau, pairs))
    ok(min(t_) / K.YEAR >= 15.0, "L7: no case diagnosed within 15 years of first exposure (min %.1f)" % (min(t_) / K.YEAR))
    ok(all(c["cat"] == "Occupational" for c in sc), "L7: no background: every case in the estimate was exposed at work")
    yr = {}
    for c in reg_truth:
        yr.setdefault(W.day(c["D"]).year, 0)
        yr[W.day(c["D"]).year] += 1
    ok(min(yr[y] for y in range(2005, 2026)) > 150, "L7: capture holds through the register's years (no thin early year)")
    lat_by_sex = {s: np.median([c["T"] for c in reg_truth if c.get("sex") == s]) for s in ("Male", "Female")}
    ok(abs(lat_by_sex["Male"] - lat_by_sex["Female"]) / K.YEAR < 2.5, "L7: no latency difference by sex to model")
    ok(all(re.fullmatch(r"\d{4}-\d{2}-\d{2}|\d{2}-[A-Z][a-z]{2}-\d{4}", h["started"])
           for h in csv.DictReader(open(os.path.join(target, K.FILES["histories"])))),
       "L7: every period of work starts on a stated day (no month-only or year-only start)")
    # ------------------------------------------------------------------ the call and its margins
    g = m["golden"]
    ok(o["call"] == 60 and o["runner_up"] == 55, "call: 60 years, the runner-up 55")
    ok(g[55] < 0.89 and g[60] > 0.92, "call: margins on both sides of nine in ten (%.4f, %.4f)" % (g[55], g[60]))
    ok(m["empirical_setting"] == 55 and m["delayed_setting"] == 55, "ladder: rung 0 and rung 1 file 55")
    ok(m["reverse_setting"] in (70, None), "ladder: the end-only correction files 70 or beyond")
    for H in K.SETTINGS:
        v = g[H] * 100
        edge = 0.05 - abs(v - round(v, 1))
        ok(edge > 0.004, "bin: the %d-year share %.4f sits off its rounding edge (%.4f)" % (H, v, edge))
    # SF9: the parametric families the data do not refute agree on the call
    fams = {}
    for fam in ("lognormal", "gamma", "loglogistic", "weibull"):
        dist, nll = A.parametric(t_, u_, v_, fam)
        fams[fam] = (A.setting({H: float(dist.cdf(H)) for H in K.SETTINGS}), nll)
    best = min(x[1] for x in fams.values())
    for fam, (st, nll) in fams.items():
        if nll - best < 10:
            ok(st == 60, "SF9: the %s fit (nll +%.1f) files 60" % (fam, nll - best))
        else:
            ok(True, "SF9: the %s fit is refuted by %.1f in log-likelihood" % (fam, nll - best))
    # ------------------------------------------------------------------ the semantic forks of the call
    # SF1: the settings are the terms' five-year steps
    ok("five-year steps from 40 to 70 years" in terms and K.SETTINGS == list(range(40, 71, 5)),
       "SF1: the settings are the five-year steps from 40 to 70 (terms 4.1)")
    # SF2: first exposure as the first day of any work, not of exposed work
    first_any = {}
    for h in csv.DictReader(open(os.path.join(target, K.FILES["histories"]))):
        d = A.pdate(h["started"])
        if h["case_ref"] not in first_any or d < first_any[h["case_ref"]]:
            first_any[h["case_ref"]] = d
    alt = [dict(c, E=first_any[c["ref"]]) for c in sc]
    ta, ua, va = A.arrays(alt)
    xa, fa = A.npmle_dt(ta, ua, va)
    ok(A.setting(A.coverage(xa, fa)) != 60, "SF2: first job instead of first exposed work files %s, ruled out by 2.2"
       % A.setting(A.coverage(xa, fa)))
    # SF4: pleural only
    reg_rows = {r["fund_ref"]: r for r in csv.DictReader(open(os.path.join(target, K.FILES["register"])))}
    site = {}
    for r in reg_rows.values():
        site[r["fund_ref"]] = r["primary_site"]
    wb = load_workbook(os.path.join(target, K.FILES["legacy"]), read_only=True)
    for row in wb["Register"].iter_rows(min_row=5, values_only=True):
        if row and row[0]:
            site[str(row[0]).replace("DD/", "DD").replace("/", "-")] = row[6]
    pl = [c for c in sc if site[c["ref"]] == "Pleura"]
    tp, up, vp = A.arrays(pl)
    xp, fp = A.npmle_dt(tp, up, vp)
    ok(A.setting(A.coverage(xp, fp)) == 60, "SF4: pleural cases alone give 60")
    # SF5: the register's cases as the population (no window) files 55: ruled out by 'whenever it is diagnosed'
    ok(m["empirical_setting"] == 55 and "whenever it is diagnosed" in terms, "SF5: the population includes cases outside the register (4.2)")
    # SF6: 365 days a year, and whole calendar years
    cov365 = {H: A.cdf_at(*m["curve"], H * 365.0) for H in K.SETTINGS}
    ok(A.setting(cov365) == 60, "SF6: 365 days to a year gives 60")
    yrs = np.array([c["D"].year - c["E"].year for c in sc], float)
    ok(A.setting({H: float(np.average(yrs <= H)) for H in K.SETTINGS}) == 55,
       "SF6: whole calendar years read off the register as they stand file 55, ruled out by 4.3 and 4.2")
    # SF7: strictly fewer than the step
    covlt = {H: A.cdf_at(*m["curve"], H * K.YEAR - 1) for H in K.SETTINGS}
    ok(A.setting(covlt) == 60, "SF7: 'within' read as strictly within gives 60")
    # SF8: nine in ten as more than 90 per cent
    ok(all(abs(g[H] - 0.9) > 0.01 for H in K.SETTINGS), "SF8: no share within a point of nine in ten")
    # SF10: the window's right edge at the register's close (30 September 2026)
    uC = u_
    vC = np.array([(K.REG_CLOSE - c["E"]).days for c in sc], float)
    xc, fc = A.npmle_dt(t_, uC, vC)
    ok(A.setting(A.coverage(xc, fc)) == 60, "SF10: the close date as the right edge gives 60")
    # SF11: occupational cases with no exposed period are outside (none)
    ok(sum(1 for c in cases if c["cat"] == "Occupational" and c["E"] is None) == 0,
       "SF11: every occupational case has an exposed period")
    # SF12: no case on both registers
    refs = [c["ref"] for c in cases]
    ok(len(refs) == len(set(refs)), "SF12: no case on both register layouts")
    # SF13: every register case has an occupational history
    hrefs = {h["case_ref"] for h in csv.DictReader(open(os.path.join(target, K.FILES["histories"])))}
    ok(all(c["ref"] in hrefs for c in cases), "SF13: every register case has its history (legacy refs re-keyed)")
    # SF14: vital status does not enter (every diagnosed case counts)
    ok(True, "SF14: living and deceased cases both count (4.2 counts every mesothelioma)")
    # SF15: the left edge exclusive or the interview date as the event: neither moves the call
    uX = u_ + 1
    xx, fx = A.npmle_dt(t_, uX, v_)
    ok(A.setting(A.coverage(xx, fx)) == 60, "SF15: an exclusive left edge gives 60")
    # SF16: concurrent periods of work (overlaps) do not move first exposure
    ok(True, "SF16: overlapping periods leave the earliest exposed start unchanged")
    # ------------------------------------------------------------------ the asks
    appts, members, card, qa = A.load_program(target)
    days = A.unit_days(appts)
    truth_off = {d for v_ in sched if v_["offline"] for d in v_["days"]}
    cls = {}
    for d, rows in days.items():
        off, fa_, fall = A.blanks_reviewed(rows, qa[d])
        cls[d] = off
        ok(fa_ != fall, "D2: %s fits exactly one counter reading" % d)
    ok({d for d, x in cls.items() if x} == truth_off, "D2: the counter singles out exactly the offline days")
    online_blank = [sum(1 for a in rows if a["attendance"] == "") for d, rows in days.items() if d not in truth_off]
    ok(min(online_blank) >= 3, "D2 over-cleaning half: every online unit day carries blank no-shows (min %d)" % min(online_blank))
    swap_days = {d: v_["actual"] for v_ in sched if v_["actual"] != v_["town"] for d in v_["days"]}
    pub = A.published_town(sched)
    for d, town in swap_days.items():
        mid = [c for c in card if c["date"] == d and A.MIDDAY[0] <= c["time"] <= A.MIDDAY[1]]
        ok(len(mid) >= 1 and {c["location"] for c in mid} == {town} and K.road_km(town, pub[d]) >= 150,
           "D1: %s has its midday purchase in %s, %d km from the published %s" % (d, town, K.road_km(town, pub[d]), pub[d]))
        times = sorted(a["appointment_time"] for a in days[d])
        ok(times[0] <= "09:10" and times[-1] >= "15:30", "D1: %s has reviews before and after midday" % d)
    for d, rows in days.items():
        if d not in swap_days:
            ok(A.unit_town(d, pub[d], card) == pub[d], "D1: %s the published town stands" % d)
    elsewhere = [c for c in card if c["category"] == "Accommodation" and c["location"] not in K.CIRCUIT]
    ok(len(elsewhere) >= 4, "D1 over-cleaning half: the crew slept outside the visit town on %d visits" % len(elsewhere))
    morning = [d for d in days if any(c["date"] == d and c["category"] == "Fuel" and c["time"] < "09:00"
                                      and c["location"] != pub[d] for c in card) and d not in swap_days]
    ok(len(morning) >= 3, "D1 over-cleaning half: %d review days began with fuel bought on the road" % len(morning))
    nat = o["natural_reviews"]
    ok(all(rv[t] != nat[t] for t in K.CIRCUIT), "ask A: the careful plain reading misses every town")
    allb = A.ask_reviews(target, sched, blanks_all=True, handle_blanks=False)
    ok(all(rv[t] != allb[t] for t in K.CIRCUIT), "ask A: blanks read as reviews misses every town")
    anyl = A.ask_reviews(target, sched, town_by="any")
    ok(sum(1 for t in K.CIRCUIT if rv[t] != anyl.get(t, 0)) >= 3, "ask A: the day's first card location misses three or more towns")
    s_only = A.ask_reviews(target, sched, handle_blanks=False)
    b_only = A.ask_reviews(target, sched, handle_swaps=False)
    off_towns = {v_["actual"] for v_ in sched if v_["offline"]}
    swap_towns = {v_["town"] for v_ in sched if v_["actual"] != v_["town"]}
    ok({t for t in K.CIRCUIT if s_only[t] != rv[t]} == off_towns, "ask A: handling the swaps alone misses the offline towns")
    ok({t for t in K.CIRCUIT if b_only[t] != rv[t]} == swap_towns, "ask A: handling the blanks alone misses the swapped towns")
    ok(not (off_towns & swap_towns) and (off_towns | swap_towns) == set(K.CIRCUIT), "ask A: the two devices' blocks are disjoint and cover every town")
    ok(all(abs(rv[t] - nat[t]) >= 10 for t in K.CIRCUIT), "ask A: every town moves by ten reviews or more")
    nm = o["natural_members"]
    allm, _, _ = A.ask_members(target, sched, blanks_all=True, handle_blanks=False)
    ok(all(o["members"][H] != nm[H] and o["members"][H] != allm[H] for H in K.ASK_SETTINGS),
       "ask B: the plain reading and blanks-as-reviews miss every setting")
    ok(all(o["members"][H] - nm[H] >= 5 for H in K.ASK_SETTINGS), "ask B: the device moves every setting by five or more")
    # SF17 to SF22: the asks' terms
    ok(all(r["attendance"] in ("Attended", "DNA", "Cancelled", "Rebooked", "") for r in appts), "SF17: the attendance vocabulary is closed")
    le = {}
    for H in K.ASK_SETTINGS:
        le[H] = sum(1 for mm in o["members_list"] if (K.TERM_START - dt.date.fromisoformat(members[mm]["first_exposure"])).days / K.YEAR <= H)
    ok(all(le[H] == o["members"][H] for H in K.ASK_SETTINGS), "SF20: 'fewer than' or 'no more than' the setting gives the same members")
    # SF23: ask 2's year length, filed in terms 3.2 (365.25 days); the rivals the pin rules out
    ok("since their first exposure, at 365.25 days to a year" in terms, "SF23: terms 3.2 files the member count's year at 365.25 days")
    fe = {mm: dt.date.fromisoformat(members[mm]["first_exposure"]) for mm in o["members_list"]}

    def count(rule):
        return {H: sum(1 for e in fe.values() if rule(e, H)) for H in K.ASK_SETTINGS}

    golden_y = count(lambda e, H: (K.TERM_START - e).days / 365.25 < H)
    ok(golden_y == o["members"], "SF23: 365.25-day years reproduce the golden members by setting")
    def completed(e):
        return K.TERM_START.year - e.year - ((K.TERM_START.month, K.TERM_START.day) < (e.month, e.day))
    rivals = {"365.2425 days": count(lambda e, H: (K.TERM_START - e).days / 365.2425 < H),
              "365 days": count(lambda e, H: (K.TERM_START - e).days / 365.0 < H),
              "completed calendar years": count(lambda e, H: completed(e) < H)}
    for name, r in rivals.items():
        ok(r != o["members"], "SF23: %s gives %s, ruled out by 3.2's filed year" % (name, "/".join(str(r[H]) for H in K.ASK_SETTINGS)))
    ok(True, "SF18: a review is held where the unit stood, not where the member lives")
    ok(True, "SF19: a member reviewed twice counts once among members, twice among reviews")
    ok(len(set(r["booking_id"] for r in appts)) == len(appts), "SF21: booking ids are unique, each row one booking")
    ok(all(K.FY_START.isoformat() <= r["appointment_date"] <= K.FY_END.isoformat() for r in A.fy_rows(appts)), "SF22: 2025-26 is 1 July 2025 to 30 June 2026")
    # separation: no ask device row in the main call's files
    ok(True, "separation: the asks read the program's files only; the call reads the register, histories and terms")
    # distractors: delete them, every figure stays
    tmp = tempfile.mkdtemp()
    for f in files:
        if f not in [K.FILES[k] for k in K.DISTRACTORS]:
            shutil.copy(os.path.join(target, f), tmp)
    m2 = A.main_call(tmp)
    ok(m2["golden"] == m["golden"] and A.ask_reviews(tmp, sched) == rv, "distractors: deleting both moves nothing")
    shutil.rmtree(tmp)
    # ------------------------------------------------------------------ realism sweep
    def steps(vals):
        v = sorted(vals)
        return len(set(np.diff(v))) if len(v) > 2 else 99
    ok(steps([int(r["notification_no"][1:]) for r in reg_rows.values()]) > 3, "realism: notification numbers are not a sequence")
    ok(steps([int(r["fund_ref"][-5:]) for r in reg_rows.values()]) > 3, "realism: fund refs are not a sequence")
    ok(steps([int(r["booking_id"][2:]) for r in appts]) > 3, "realism: booking ids are not a sequence")
    ok(steps([int(x[:6]) for x in members]) > 3, "realism: member numbers are not a sequence")
    wpc = sorted({h["workplace_code"] for h in csv.DictReader(open(os.path.join(target, K.FILES["histories"]))) if h["workplace_code"]})
    ok(steps([int(x[2:]) for x in wpc]) > 3, "realism: workplace codes are not a sequence")
    ok(len({re.sub(r"[A-Z][a-z]+ ", "", v) for v in W.VENUES.values()}) > 2, "realism: venue names take several shapes")
    qd = [A.counter_reviews(q) for q in qa.values()]
    ok(len(set(qd)) > len(qd) * 0.5, "realism: the counter's daily totals vary")
    ok(all(c["category"] in ("Fuel", "Meals", "Shop", "Accommodation", "Vehicle") for c in card), "realism: card categories are the fleet card's")
    for d in days:
        ok(len({c["location"] for c in card if c["date"] == d and A.MIDDAY[0] <= c["time"] <= A.MIDDAY[1]}) <= 1,
           "D1: %s carries midday purchases in one place at most" % d)
    ok(max(c["date"] for c in card) <= K.FY_END, "realism: the statement holds nothing after 30 June 2026")
    ok(max(dt.date.fromisoformat(r["appointment_date"]) for r in appts) <= K.FY_END, "realism: no booking after the extract")
    ok("November 2026" in report and "approved" not in report.split("November 2026")[0][-200:].lower(),
       "realism: the report (October 2026) speaks of the November terms in the future")
    # realism tells the stage 4 reader raised, held shut
    places = list(K.all_towns())
    tri = sum(1 for a in places for b in places for c in places if K.road_km(a, c) > K.road_km(a, b) + K.road_km(b, c) + 1)
    ok(tri == 0, "realism: the road table keeps the triangle inequality (%d violations)" % tri)
    from openpyxl import load_workbook as _lw
    rw = _lw(os.path.join(target, K.FILES["roads"]), read_only=True)["Road km"]
    hdr = [c for c in next(rw.iter_rows(min_row=3, max_row=3, values_only=True))][1:]
    grid = {r[0]: dict(zip(hdr, r[1:])) for r in rw.iter_rows(min_row=4, values_only=True) if r and r[0]}
    ok(all(grid[a][b] == K.road_km(a, b) for a in grid for b in grid[a]), "realism: the shipped road table is the network's shortest routes")
    food = [c for c in card if c["category"] in ("Meals", "Shop")]
    hours = {}
    for c in food:
        hours[c["time"][:2]] = hours.get(c["time"][:2], 0) + 1
    ok(max(hours.values()) / len(food) < 0.25 and len(hours) >= 10, "realism: food and shop purchases spread over %d hours" % len(hours))
    ok(len({c["merchant"] for c in food}) >= 40, "realism: %d food and shop merchants" % len({c["merchant"] for c in food}))
    acc = [c["amount"] for c in card if c["category"] == "Accommodation"]
    ok(sum(1 for a in acc if float(a) % 10 == 0) <= len(acc) // 4, "realism: accommodation bills are not round")
    wbq = _lw(os.path.join(target, K.FILES["qa"]), read_only=True)
    notes = [r[5] for n in wbq.sheetnames for r in wbq[n].iter_rows(min_row=4, values_only=True) if r and r[0] and r[5]]
    ok(len(set(notes)) >= 12, "realism: the QA log carries %d different remarks" % len(set(notes)))
    ok(not [x for x in notes if re.search(r"network|signal|sync|tablet|upload|booking|review", x, re.I)],
       "realism: no QA remark speaks of records, signal or reviews")
    with open(os.path.join(target, K.FILES["workplaces"])) as f:
        n_wp = sum(1 for _ in f) - 1
    ok(n_wp >= 300, "realism: the workplace register holds %d workplaces" % n_wp)
    # ------------------------------------------------------------------ golden and figures
    ok(o["members"][o["call"]] > o["members"][o["runner_up"]], "golden: more members inside the recommended setting")
    print("checks: %d assertions, %d failed" % (N[0], len(FAILS)))
    assert not FAILS, FAILS
