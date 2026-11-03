"""The clean truth for task399: the Halsey Coast region's District Court custody lists, October 2024 to September 2026.

Every first appearance from police custody at the four courthouses is drawn with the legally relevant pre-decision
factors, a counsel-of-record status and the minute it was called. At Kestrel Bay the custody list sits in courtroom 1
(mornings from 10:00, the remainder stood down to 14:15). From Monday 1 December 2025 the morning list (Monday to
Thursday) is presided over by a community magistrate, and an audio-visual (AVL) remand list sits in courtroom 2 on
most Monday to Thursday sitting days; the region keeps one rostered duty lawyer at Kestrel Bay, who serves both
lists. A custody-list defendant with no lawyer of record who is called while the AVL list sits stands unassisted.
EM bail assessments slow from November 2025, which lengthens custody remands but is never decided at a first
appearance.

The ask worlds ride their own random streams so that nothing added to them moves a main-call draw: the EM bail unit's
assessments (its legacy tracker until 30 January 2026, its case system from 2 February 2026) and the supported bail
houses (the provider's spreadsheet until 31 May 2026, its case app from 1 June 2026).

Nothing here is recorded as such in the pack: pack.py writes each system's own extract from these tables.
"""
from __future__ import annotations

import datetime as dt
import math

import numpy as np
import pandas as pd

SEED = 4147          # first appearances (the main call)
SEED_PEOPLE = 3996   # names, dates of birth, case numbers
SEED_LATER = 3991    # later appearances and the AVL list
SEED_EM = 3993       # the EM bail unit
SEED_BH = 3993       # the supported bail houses
START = dt.date(2024, 10, 1)
END = dt.date(2026, 9, 30)
P2_START = dt.date(2025, 10, 1)
REORG = dt.date(2025, 12, 1)          # the Kestrel Bay custody list reorganisation (magistrate and AVL list)
EM_SLOW = dt.date(2025, 11, 3)        # EM bail assessment turnaround lengthens
EM_SWITCH = dt.date(2026, 2, 2)       # the EM unit's case system goes live; open legacy orders migrate
BH_SWITCH = dt.date(2026, 6, 1)       # the bail houses' provider moves to its case app
EXTRACT = dt.date(2026, 11, 2)        # the date every extract was pulled

COURTS = ["KB", "DN", "AG", "RC"]
COURT_NAME = {"KB": "Kestrel Bay", "DN": "Dunmore", "AG": "Ashgrove", "RC": "Thornmere"}
COURT_CODE = {"KB": "KBY", "DN": "DUN", "AG": "ASH", "RC": "THM"}
COURT_NUM = {"KB": "041", "DN": "043", "AG": "044", "RC": "047"}
LAMBDA = {"KB": 34.0, "DN": 11.0, "AG": 9.0, "RC": 6.0}          # first appearances from custody per sitting day
DOW_MULT = [1.45, 0.95, 0.9, 0.9, 1.0]                          # Monday carries the weekend's arrests

HOLIDAYS = {
    dt.date(2024, 10, 28), dt.date(2024, 12, 25), dt.date(2024, 12, 26), dt.date(2025, 1, 1), dt.date(2025, 1, 2),
    dt.date(2025, 2, 6), dt.date(2025, 4, 18), dt.date(2025, 4, 21), dt.date(2025, 4, 25), dt.date(2025, 6, 2),
    dt.date(2025, 6, 20), dt.date(2025, 10, 27), dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1),
    dt.date(2026, 1, 2), dt.date(2026, 2, 6), dt.date(2026, 4, 3), dt.date(2026, 4, 6), dt.date(2026, 4, 27),
    dt.date(2026, 6, 1), dt.date(2026, 7, 10),
}

# Remand in custody at first appearance, logit scale. Status: own lawyer of record 0; no lawyer, duty lawyer at the
# call ASSIST; no lawyer, nobody at the call UNASSIST. No judicial officer carries an effect of its own.
B0 = -1.95
B_SER = [0.0, 0.0, 0.45, 0.95, 1.6, 2.4]          # seriousness band 1..5 (index 0 unused)
B_PRI = 0.30                                       # per ln(1 + prior convictions)
B_FTA = 0.42
B_ONBAIL = 0.62
B_FV = 0.38
B_NFA = 0.85
ASSIST = 0.12
UNASSIST = 2.00
P2_SHIFT = 0.04
LAST_AVL_GAP = 4                                   # (kept for reference) the shortest gap before the rising


def avl_margins(d):
    """Minutes from the AVL list's opening to its first call, and from its last call to its rising, on day d:
    the court's own rhythm, which varies by day (no random draw, so no stream moves)."""
    return 1 + (d.toordinal() * 7) % 4, 3 + (d.toordinal() * 11) % 6

OFFENCES = [  # code, description, seriousness band (the Ministry's offence seriousness scale)
    ("1112", "Disorderly behaviour", 1), ("1531", "Wilful trespass", 1), ("4412", "Theft (under 500)", 1),
    ("6211", "Breach of community work", 1), ("4411", "Shoplifting (500 to 1000)", 2),
    ("3651", "Breach of protection order", 2), ("6121", "Driving while disqualified", 2),
    ("5141", "Possession of cannabis for supply", 2), ("2131", "Male assaults female", 3),
    ("4211", "Burglary", 3), ("4321", "Unlawfully takes motor vehicle", 3), ("2161", "Assault on a person in a "
    "family relationship", 3), ("2121", "Assault with intent to injure", 4), ("5211", "Supply of methamphetamine", 4),
    ("2111", "Injuring with intent to injure", 4), ("3111", "Aggravated robbery", 5),
    ("2101", "Wounding with intent to cause grievous bodily harm", 5), ("3211", "Sexual violation", 5),
]


def sitting_days():
    d = START
    out = []
    while d <= END:
        if d.weekday() < 5 and d not in HOLIDAYS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


SITTING = None


def is_sitting(d):
    return d.weekday() < 5 and d not in HOLIDAYS


def add_sitting_days(d, k):
    """The k-th sitting day after d (k >= 1)."""
    while k > 0:
        d += dt.timedelta(days=1)
        if is_sitting(d):
            k -= 1
    return d


def period_of(d):
    return "P1" if d < P2_START else "P2"


def _officers():
    return {
        "KB": ["Judge A. Mercer", "Judge R. Takerei", "Judge S. Hollis", "Judge P. Varga", "Judge L. Fenwick"],
        "DN": ["Judge M. Okafor", "Judge T. Brannigan", "Judge R. Takerei"],
        "AG": ["Judge H. Liddell", "Judge S. Hollis", "Judge K. Ashdown"],
        "RC": ["Judge K. Ashdown", "Judge M. Okafor"],
    }


MAGISTRATE = "Community Magistrate J. Pellow"
AVL_OFFICERS = ["Judge P. Varga", "Judge L. Fenwick", "Judge A. Mercer"]


def _avl_session(rng, d):
    """The Kestrel Bay AVL remand list on day d (from the reorganisation), or None. Times in minutes after midnight."""
    if d < REORG:
        return None
    u = rng.random()
    if d.weekday() == 4:                # the remand prison's AVL suite serves another court on Fridays
        return None
    if u < 0.03:
        return None
    # the remand prison's AVL suite allocates the court a block whose start moves week to week
    kind = rng.choice(["early", "mid", "late", "aft"], p=[0.60, 0.20, 0.0, 0.20])
    if kind == "early":
        start = 600 + int(rng.integers(0, 4)) * 5
    elif kind == "mid":
        start = 640 + int(rng.integers(0, 7)) * 5
    elif kind == "late":
        start = 700 + int(rng.integers(0, 5)) * 5
    else:
        start = 855 + int(rng.integers(0, 6)) * 5
    length = 130 + int(rng.integers(0, 13)) * 5
    return (start, start + length)


def _settle_window(sess, calls, d):
    """Nudge the AVL window so its two readings converge: no custody call between the list's opening and its first
    call, and none between its last call and its rising."""
    start, end = sess
    m1, m2 = avl_margins(d)
    while any(start <= c < start + m1 for c in calls):
        start += 1
    while any(end - m2 < c < end for c in calls):
        end += 1
    return (start, end)


def first_appearances(seed=SEED):
    rng = np.random.default_rng(seed)
    days = sitting_days()
    judges = _officers()
    rows, sessions, avl = [], [], []
    did = 0
    for d in days:
        dow = d.weekday()
        sess = _avl_session(rng, d)
        for c in COURTS:
            n = int(rng.poisson(LAMBDA[c] * DOW_MULT[dow]))
            if n == 0:
                continue
            am_officer = (MAGISTRATE if (c == "KB" and d >= REORG and dow <= 3)
                          else judges[c][int(rng.integers(0, len(judges[c])))])
            pm_officer = judges[c][int(rng.integers(0, len(judges[c])))]
            order = []
            for _ in range(n):
                did += 1
                ser = int(rng.choice([1, 2, 3, 4, 5], p=[0.22, 0.30, 0.25, 0.15, 0.08]))
                pri = int(rng.negative_binomial(1.1, 0.13))
                fta = int(rng.random() < min(0.75, 0.12 + 0.025 * pri))
                onb = int(rng.random() < min(0.6, 0.10 + 0.018 * pri))
                fv = int(rng.random() < 0.31)
                nfa = int(rng.random() < 0.075)
                lo = -0.62 + 0.08 * (ser - 3) - 0.22 * math.log1p(pri) - 0.55 * nfa
                own = int(rng.random() < 1.0 / (1.0 + math.exp(-lo)))
                dur = 3 + int(rng.integers(0, 6)) + (5 if ser >= 4 else 0) + (2 if not own else 0)
                order.append(dict(def_id=did, ser=ser, pri=pri, fta=fta, onb=onb, fv=fv, nfa=nfa, own=own, dur=dur))
            rng.shuffle(order)
            # call times first (no random draw), then the AVL window is settled against them, then the outcomes
            t = 600 if c != "RC" else 615
            for m in order:
                if t + m["dur"] > 775 and c == "KB":           # Kestrel Bay stands the rest down to 14:15
                    t = max(t, 855)
                m["session"] = "am" if t < 840 else "pm"
                m["call"] = t
                t += m["dur"]
            if c == "KB" and sess is not None:
                sess = _settle_window(sess, {m["call"] for m in order}, d)
                taken = {m["call"] for m in order}
                for m in order:
                    if m["call"] == sess[1]:
                        nxt = m["call"] + 1
                        while nxt in taken:
                            nxt += 1
                        taken.discard(m["call"])
                        m["call"] = nxt
                        taken.add(nxt)
                avl.append(dict(date=d, court="KB", courtroom="2", start=sess[0], end=sess[1]))
            for m in order:
                officer = am_officer if m["session"] == "am" else pm_officer
                away = (sess is not None and c == "KB" and sess[0] <= m["call"] < sess[1])
                status = "own" if m["own"] else ("unassisted" if away else "assisted")
                lp = (B0 + B_SER[m["ser"]] + B_PRI * math.log1p(m["pri"]) + B_FTA * m["fta"] + B_ONBAIL * m["onb"]
                      + B_FV * m["fv"] + B_NFA * m["nfa"] + (P2_SHIFT if d >= P2_START else 0.0)
                      + (ASSIST if status == "assisted" else UNASSIST if status == "unassisted" else 0.0))
                p = 1.0 / (1.0 + math.exp(-lp))
                ric = int(rng.random() < p)
                rows.append(dict(def_id=m["def_id"], date=d, period=period_of(d), court=c, session=m["session"],
                                 officer=officer, call_min=m["call"], dur=m["dur"], own=m["own"], status=status,
                                 ser=m["ser"], pri=m["pri"], fta=m["fta"], onb=m["onb"], fv=m["fv"], nfa=m["nfa"],
                                 ric=ric, p_ric=p, during_avl=int(away)))
            sessions.append(dict(date=d, court=c, am_officer=am_officer, pm_officer=pm_officer, n=n))
    return pd.DataFrame(rows), pd.DataFrame(avl), pd.DataFrame(sessions)


def _people(fa, seed):
    """Names, dates of birth, person ids and case numbers on their own stream."""
    from faker import Faker
    fk = Faker("en_NZ")
    fk.seed_instance(seed)
    rng = np.random.default_rng(seed)
    n = len(fa)
    # repeat defendants: about one first appearance in six belongs to a person seen earlier in the window
    person = np.zeros(n, dtype=int)
    pool = []
    pid = 0
    reuse = rng.random(n) < 0.16
    for i in range(n):
        if reuse[i] and len(pool) > 50:
            person[i] = pool[int(rng.integers(0, len(pool)))]
        else:
            pid += 1
            person[i] = pid
            pool.append(pid)
    names, dobs = {}, {}
    for p in range(1, pid + 1):
        g = "M" if rng.random() < 0.82 else "F"
        first = fk.first_name_male() if g == "M" else fk.first_name_female()
        names[p] = (fk.last_name(), first)
        age = int(np.clip(rng.gamma(4.0, 7.5) + 17, 17, 74))
        dobs[p] = dt.date(2025 - age, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
    fa = fa.copy()
    gaps = np.cumsum(rng.integers(1, 23, size=pid + 1))
    fa["person"] = [400000 + int(gaps[p]) for p in person]
    fa["surname"] = [names[p][0] for p in person]
    fa["given"] = [names[p][1] for p in person]
    fa["dob"] = [dobs[p] for p in person]
    seq = {}
    crn = []
    for d, c in zip(fa["date"], fa["court"]):
        key = (d.year, c)
        seq[key] = seq.get(key, 0) + 1
        crn.append("CRI-%d-%s-%06d" % (d.year, COURT_NUM[c], 1000 + seq[key] * 3 + (d.toordinal() % 3)))
    fa["crn"] = crn
    offs = [o for o in OFFENCES]
    by_band = {b: [o for o in offs if o[2] == b] for b in range(1, 6)}
    pick = [by_band[s][int(rng.integers(0, len(by_band[s])))] for s in fa["ser"]]
    fa["offence_code"] = [o[0] for o in pick]
    fa["offence"] = [o[1] for o in pick]
    return fa


def later_appearances(fa, avl, seed):
    """Every appearance after the first, on its own stream, and the AVL list's calls filling each sitting window."""
    rng = np.random.default_rng(seed)
    judges = _officers()
    avl_days = sorted(avl["date"]) if len(avl) else []
    avl_set = set(avl_days)
    rows = []
    em_orders = []
    due_avl = {}
    avl_officer = {}
    for r in fa.itertuples(index=False):
        d = r.date
        if r.ric:
            nd = add_sitting_days(d, int(rng.integers(3, 8)))
            if r.court == "KB" and nd >= REORG:
                while nd not in avl_set and nd <= END + dt.timedelta(days=40):
                    nd = add_sitting_days(nd, 1)
                if nd in avl_set:
                    due_avl.setdefault(nd, []).append(r)
                    continue
            rows.extend(_remand_chain(rng, r, nd, judges, em_orders))
        else:
            if rng.random() < 0.18:      # disposed on the day
                continue
            rows.extend(_bail_chain(rng, r, add_sitting_days(d, int(rng.integers(15, 35))), judges))
    # the AVL list: every due case is called in the window, the last call LAST_AVL_GAP before the rising
    for a in avl.itertuples(index=False):
        due = due_avl.get(a.date, [])
        due.sort(key=lambda x: x.crn)
        n = len(due)
        m1, m2 = avl_margins(a.date)
        span = a.end - m2 - (a.start + m1)
        officer = AVL_OFFICERS[int(rng.integers(0, len(AVL_OFFICERS)))]
        avl_officer[a.date] = officer
        jit = np.random.default_rng([seed, a.date.toordinal()])
        inner = sorted(int(x) for x in jit.choice(np.arange(1, max(span, 2)), size=max(n - 2, 0),
                                                  replace=max(n - 2, 0) > max(span - 1, 1))) if n > 2 else []
        times = ([a.start + m1] + [a.start + m1 + x for x in inner] + [a.end - m2]) if n > 1 else [a.start + m1]
        for k, r in enumerate(due):
            call = times[k]
            rows.extend(_remand_chain(rng, r, a.date, judges, em_orders, avl_call=call, avl_officer=officer,
                                      last=(k == n - 1)))
    avl = avl.copy()
    avl["officer"] = [avl_officer.get(d) for d in avl["date"]]
    return pd.DataFrame(rows), pd.DataFrame(em_orders), avl


def _sub_row(r, d, kind, court, courtroom, lst, call, officer, outcome, nxt, counsel):
    return dict(crn=r.crn, person=r.person, surname=r.surname, given=r.given, dob=r.dob, court=court,
                courtroom=courtroom, list=lst, appearance_type=kind, date=d, call_min=call, officer=officer,
                counsel=counsel, outcome=outcome, next_date=nxt, offence_code=r.offence_code, offence=r.offence,
                first=0)


def _remand_chain(rng, r, d, judges, em_orders, avl_call=None, avl_officer=None, last=False):
    rows = []
    if d > END:
        return rows
    counsel = r.own
    if avl_call is not None:
        court, room, lst, call, officer = r.court, "2", "AVL remand", avl_call, avl_officer
    else:
        court, room, lst = r.court, "1", "Custody"
        call = 600 + int(rng.integers(0, 30)) * 6
        officer = judges[r.court][int(rng.integers(0, len(judges[r.court])))]
        if r.court == "KB" and d >= REORG and d.weekday() <= 3 and call < 775:
            officer = MAGISTRATE
    u = rng.random()
    if u < 0.45:
        outcome = "Remanded on bail"
        nd = add_sitting_days(d, int(rng.integers(15, 35)))
        rows.append(_sub_row(r, d, "Bail application", court, room, lst, call, officer, outcome, nd, counsel))
        rows.extend(_bail_chain(rng, r, nd, judges))
    elif u < 0.65 and d >= dt.date(2025, 8, 1):
        outcome = "Remanded in custody, EM bail address assessment ordered"
        rows.append(_sub_row(r, d, "Bail application", court, room, lst, call, officer, outcome, None, counsel))
        em_orders.append(dict(crn=r.crn, person=r.person, surname=r.surname, given=r.given, dob=r.dob,
                              court=r.court, order_date=d))
    else:
        outcome = "Remanded in custody"
        nd = add_sitting_days(d, int(rng.integers(10, 20)))
        rows.append(_sub_row(r, d, "Bail application", court, room, lst, call, officer, outcome, nd, counsel))
        if nd <= END and rng.random() < 0.7:
            c2 = 600 + int(rng.integers(0, 30)) * 6
            o2 = judges[r.court][int(rng.integers(0, len(judges[r.court])))]
            rows.append(_sub_row(r, nd, "Remand appearance", r.court, "1", "Custody", c2, o2,
                                 "Remanded in custody" if rng.random() < 0.6 else "Convicted and sentenced",
                                 None, counsel))
    return rows


def _bail_chain(rng, r, d, judges):
    rows = []
    k = int(rng.integers(1, 3))
    for i in range(k):
        if d > END:
            break
        kind = "Case review" if i < k - 1 else rng.choice(["Callover", "Sentencing", "Case review"])
        call = 600 + int(rng.integers(0, 40)) * 6
        officer = judges[r.court][int(rng.integers(0, len(judges[r.court])))]
        if rng.random() < 0.07:
            outcome = "Warrant to arrest issued"
        elif i == k - 1:
            outcome = rng.choice(["Convicted and sentenced", "Discharged without conviction", "Withdrawn"])
        else:
            outcome = "Remanded on bail"
        nd = add_sitting_days(d, int(rng.integers(15, 40))) if outcome == "Remanded on bail" else None
        rows.append(_sub_row(r, d, kind, r.court, "3", "General", call, officer, outcome, nd, r.own))
        if nd is None:
            break
        d = nd
    return rows


def em_world(em_orders, seed):
    """The EM bail unit's truth: one order may assess several addresses; the turnaround runs from the order to the
    first filing of the assessment report; an amended report is a second filing."""
    rng = np.random.default_rng(seed)
    rows = []
    for i, o in enumerate(em_orders.sort_values(["order_date", "crn"]).itertuples(index=False)):
        n_addr = int(rng.choice([1, 2, 3], p=[0.78, 0.19, 0.03]))
        slow = o.order_date >= EM_SLOW
        base = rng.gamma(6.0, 1.5) if not slow else rng.gamma(9.0, 2.1)
        days = int(min(30, max(3, round(base + 2.2 * (n_addr - 1)))))
        filed = o.order_date + dt.timedelta(days=days)
        while filed.weekday() >= 5:
            filed += dt.timedelta(days=1)
        lag = int(rng.choice([0, 1, 2, 3], p=[0.10, 0.45, 0.30, 0.15]))
        logged = add_sitting_days(o.order_date, lag) if lag else o.order_date
        amended = None
        if rng.random() < 0.16:
            amended = filed + dt.timedelta(days=int(rng.integers(3, 11)))
            while amended.weekday() >= 5:
                amended += dt.timedelta(days=1)
        rows.append(dict(order_id=i + 1, crn=o.crn, person=o.person, surname=o.surname, given=o.given, dob=o.dob,
                         court=o.court, order_date=o.order_date, logged=logged, n_addr=n_addr, filed=filed,
                         amended=amended, suitable=int(rng.random() < 0.68),
                         crn_on_tracker=int(rng.random() < 0.85)))
    return pd.DataFrame(rows)


def bail_house_world(fa_bailed, seed):
    """The supported bail houses' truth: placements (the first night and the day the resident left), the exit as the
    provider's incident system logged it, the nights each resident was away in police custody or hospital, and from
    the case app (1 June 2026) the approved overnight leave it introduced. Until 31 May 2026 the provider's
    spreadsheet recorded a placement's end on the working day the exit was processed, after the resident had left;
    from 1 June 2026 the case app's start column carries the day the placement was approved, before the resident
    arrived. The incident system logs each arrival and each exit when it happens."""
    rng = np.random.default_rng(seed)
    houses = {"KB": ("Kestrel Bay house", 8), "DN": ("Dunmore house", 6)}
    occupied = {h: [] for h in houses}
    placements, absences = [], []
    pid = 0
    cand = fa_bailed.sort_values(["date", "crn"]).reset_index(drop=True)
    for r in cand.itertuples(index=False):
        h = "KB" if r.court in ("KB", "RC") else "DN"
        if r.date < dt.date(2025, 7, 1) or r.date > dt.date(2026, 9, 25):
            continue
        if rng.random() > 0.045:
            continue
        start = r.date
        cap = houses[h][1]
        occ = [p for p in occupied[h] if p[0] <= start < p[1]]
        if len(occ) >= cap:
            continue
        stay = int(np.clip(rng.gamma(2.2, 24.0), 7, 150))
        end = start + dt.timedelta(days=stay)
        pid += 1
        occupied[h].append((start, end))
        exit_reason = rng.choice(["Case concluded", "Bail varied to another address", "Returned to custody",
                                  "Left without notice"], p=[0.55, 0.15, 0.2, 0.1])
        # the exit as the incident system logged it (local minutes on the day the resident left)
        if exit_reason == "Returned to custody":
            exit_type, exit_min = "Taken into police custody", int(rng.integers(19 * 60, 23 * 60 + 40))
        elif exit_reason == "Left without notice":
            exit_type, exit_min = "Resident did not return", int(rng.integers(22 * 60, 23 * 60 + 50))
        else:
            exit_type, exit_min = "Resident moved out", int(rng.integers(9 * 60, 16 * 60))
        # the spreadsheet's end: the working day the exit was processed (the app records the day itself)
        lag = int(rng.choice([0, 1, 1, 2, 2, 3]))
        recorded = end
        k = lag
        while k > 0:
            recorded += dt.timedelta(days=1)
            if recorded.weekday() < 5:
                k -= 1
        # the case app's start column carries the day the placement was approved, before the resident arrived
        early = int(rng.choice([1, 2, 2, 3, 3, 4]))
        start_rec = start - dt.timedelta(days=early) if start >= BH_SWITCH + dt.timedelta(days=4) else start
        placements.append(dict(placement=pid, crn=r.crn, surname=r.surname, given=r.given, dob=r.dob,
                               house=houses[h][0], start=start, end=end, exit=exit_reason, exit_type=exit_type,
                               exit_min=exit_min, end_recorded=(recorded if end < BH_SWITCH else end),
                               start_recorded=start_rec, arrive_min=int(rng.integers(11 * 60, 18 * 60))))
        # absences inside the stay: police custody (most), hospital (few); approved leave once the app allowed it
        t = start + dt.timedelta(days=int(rng.integers(3, 12)))
        while t < end - dt.timedelta(days=3):
            u = rng.random()
            if u < 0.30:
                kind = "custody" if rng.random() < 0.88 else "hospital"
                nights = int(rng.choice([1, 1, 1, 2, 2, 3, 4, 5]))
                out_min = (int(rng.integers(19 * 60, 23 * 60 + 50)) if kind == "custody"
                           else int(rng.integers(600, 1260)))
            elif u < 0.48 and t >= BH_SWITCH:
                kind = "leave"
                nights = int(rng.choice([1, 1, 2, 2, 3]))
                out_min = int(rng.integers(15 * 60, 19 * 60))
            else:
                t += dt.timedelta(days=int(rng.integers(8, 30)))
                continue
            back = t + dt.timedelta(days=nights)
            back_min = int(rng.integers(9 * 60, 17 * 60))
            if back < end:
                absences.append(dict(placement=pid, kind=kind, out_date=t, out_min=out_min, back_date=back,
                                     back_min=back_min, nights=nights))
            t = back + dt.timedelta(days=int(rng.integers(6, 25)))
    return pd.DataFrame(placements), pd.DataFrame(absences)


def build_world(seed: int = SEED, seed_em: int = SEED_EM, seed_bh: int = SEED_BH):
    fa, avl, sessions = first_appearances(seed)
    fa = _people(fa, SEED_PEOPLE)
    later, em_orders, avl = later_appearances(fa, avl, SEED_LATER)
    em = em_world(em_orders, seed_em)
    bailed = fa[(fa.ric == 0)]
    bh_place, bh_abs = bail_house_world(bailed, seed_bh)
    return dict(first=fa, avl=avl, sessions=sessions, later=later, em=em, bh_place=bh_place, bh_abs=bh_abs,
                magistrate=MAGISTRATE, seed=seed)
