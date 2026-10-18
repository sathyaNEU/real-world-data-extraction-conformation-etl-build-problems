"""task172 world: the clean truth before any record is written.

Sallowmere Software's Global Mobility team files work-permit renewals (Form I-765) through its outside counsel for
employees whose green-card applications are pending (category (c)(9)) and for the spouses of employees in H-1B status
((c)(26)). The world holds the households, every card each holder has held, every renewal the team (or, rarely, the
applicant) filed, and how each renewal's wait ran: the lockbox, the fingerprint appointment or the reuse of earlier
fingerprints, the officer's review, and, for renewals filed from 30 October 2025, the team's expedite request on the
day the filer's card expires if the renewal is still pending then.

Every process parameter below was fixed by rule before any outcome was measured; the seed is the build number."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as C

SIM_START = dt.date(2021, 1, 1)
SIM_END = dt.date(2027, 12, 31)

# --- how a renewal's wait runs (receipt to decision) -------------------------------------------------------------
P_APPT = {"(c)(26)": 0.70,          # renewals USCIS sends to a new fingerprint appointment; the rest reuse fingerprints
          "(c)(9)": 0.30}           # (c)(9) renewals mostly reuse the biometrics taken for the adjustment application
L_OLD = (28.0, 6.0)                # receipt to appointment, mean and sd in days, the 2024 and 2025 base (Seattle)
LEAD_RISE = 0.9                    # days a month the base rose after 30 October 2025, filers no longer waiting out
                                   # the extension
LEAD_SEASON = (-1.0, -2.0, -1.5, 0.0, 1.0, 2.0, 3.0, 2.5, 0.5, -0.5, -1.0, 1.5)   # by calendar month, days
LEAD_DRIFT = (0.6, 1.6)            # month-to-month drift of the base, AR(1) coefficient and innovation sd, days
STATE_LEAD = {"WA": 1.00, "CA": 1.12, "TX": 0.90, "NY": 1.18, "MA": 1.05, "NC": 0.94, "GA": 0.91, "VA": 1.07}
L_NEW = (119.0, 18.0)              # the same once USCIS set appointments about seventeen weeks out (Seattle)
RAMP = (dt.date(2026, 8, 24), dt.date(2026, 9, 14))   # receipts in this span move linearly from the old to the new
P_RESCHED_APPLICANT = (0.045, 0.006)   # applicants' reschedules, before and after 30 October 2025 (once a pending
                                       # renewal no longer extends the card, coordinators send conflicts to walk-in
                                       # biometrics and only emergencies are rescheduled)
P_RESCHED_USCIS = 0.02             # appointments USCIS moves (a closed support centre, weather)
RESCHED_USCIS = (16.0, 7.0)        # days a USCIS move adds (closures rebook first)
Q_MED, Q_SIG = 70.0, 0.32          # officer's review from the appointment (or from receipt where fingerprints reuse)
P_RFE = 0.08                       # requests for evidence
RFE_AT = 0.55                      # the request goes out this far into the base review
RFE_RESP = (30.0, 9.0)             # the applicant's response, days
RFE_DEC = (50.0, 14.0)             # decision after the response, days
P_TRANSFER = 0.04                  # cases moved to another office during review (adds up to ten days)
P_DENY = 0.015
# --- the team's filing practice -----------------------------------------------------------------------------------
OPEN_BEFORE = 180                  # the team opens a renewal this many days before the card expires
PAPER_MEAN = 21                    # opening to dispatch (packet assembly, signatures), main component, days; set by
                                   # the design note's re-centre rule (nearest 5.50 months among the values that
                                   # clear every construction)
P_PAPER_LATE = 0.15                # packets held for documents or the employee's travel
PAPER_LATE = (42.0, 14.0)
P_REJECT = 0.035                   # lockbox rejections of a team packet
P_APPLICANT_ONLY = 0.22            # rejection notices that went to the applicant only (the attorney's G-28 not accepted)
P_REREJECT = 0.08
P_COURIER = 0.012                  # packets the courier brought back undelivered
# --- the cut at the card's expiry, renewals filed from 30 October 2025 -----------------------------------------
P_REQ_EARLY = 0.12                 # requests filed 3 to 10 days before the card expires (the review plainly unfinished)
P_REQ_LATE = 0.18                  # requests filed 2 to 10 days after it (the leave letter, a holiday)
E_RESP = (9.0, 3.5)                # expedite request to decision, days
P_EXP_OK = 0.85
# --- people -------------------------------------------------------------------------------------------------------
ATTRITION = 0.085                  # program employees leaving per year
P_SPOUSE_ENROLLED = 0.70           # spouses on the company's benefits when first entered
P_DROP_2026 = 0.03                 # enrolled spouses who left the plan at the 2026 open enrolment
P_COBRA = 0.12                     # departed employees whose spouse kept coverage under COBRA through the export
P_LATE_ENROLL = 0.35               # spouses off the plan at intake who join it later (open enrolment or a life event)
P_UPLOAD_RENEWAL = 0.80            # spouses who upload a renewed card to the benefits portal
P_UPLOAD_C9 = 0.75                 # derivative spouses who upload their (c)(9) card
P_STALE_LABEL = 0.85               # switchers whose uploaded (c)(9) card kept the (c)(26) label of their earlier entry
N_H4_STOCK = 7400
H4_INFLOW = 1250.0                 # new H-4 spouses with a first work permit per year

STATES = (("WA", 0.62), ("CA", 0.12), ("TX", 0.08), ("NY", 0.06), ("MA", 0.04), ("NC", 0.03), ("GA", 0.03),
          ("VA", 0.02))
FAMILIES = (("Software Engineering", 0.58), ("Program Management", 0.09), ("Data Science", 0.08),
            ("Hardware Engineering", 0.05), ("Product Management", 0.05), ("Site Reliability", 0.05),
            ("Security Engineering", 0.04), ("Design and Research", 0.03), ("Finance", 0.015),
            ("Legal", 0.005), ("Sales Engineering", 0.03))
COUNTRY = (("India", 0.74), ("China", 0.13), ("All other", 0.13))


def month_frac(d):
    return d.year + (d.timetuple().tm_yday - 1) / 365.25


def _drift():
    rng = C.stream("lead drift")
    out, x = {}, 0.0
    y, m = 2020, 1
    while (y, m) <= (2028, 12):
        x = LEAD_DRIFT[0] * x + LEAD_DRIFT[1] * float(rng.standard_normal())
        out[(y, m)] = x
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


DRIFT = _drift()


def paper_days(rng):
    """opening to dispatch, days"""
    if rng.random() < P_PAPER_LATE:
        return gam(rng, *PAPER_LATE)
    return gam(rng, float(PAPER_MEAN), PAPER_MEAN / 3.0)


def lead_mean(recv, state="WA"):
    """receipt to the fingerprint appointment USCIS sets, mean in days, for a filer in `state`"""
    f = STATE_LEAD.get(state, 1.0)
    old = L_OLD[0] + LEAD_SEASON[recv.month - 1] + DRIFT[(recv.year, recv.month)]
    if recv > C.IFR:
        old += LEAD_RISE * min((recv - C.IFR).days, (RAMP[0] - C.IFR).days) / 30.4
    a, b = RAMP
    if recv <= a:
        return old * f
    if recv >= b:
        return L_NEW[0] * f
    w = (recv - a).days / (b - a).days
    return (old + w * (L_NEW[0] - old)) * f


def lead_sd(m):
    return max(L_OLD[1] * m / L_OLD[0] if m < 60 else 0.0, L_NEW[1] * m / L_NEW[0], 4.0)


def gam(rng, mean, sd):
    k = (mean / sd) ** 2
    return float(rng.gamma(k, sd * sd / mean))


def pick(rng, table):
    r, acc = rng.random(), 0.0
    for v, p in table:
        acc += p
        if r < acc:
            return v
    return table[-1][0]


def draw_wait(rng, cat, state, received, expiry, counsel=True, term=None):
    """one renewal's wait under the generating process, from receipt: the route, the appointment (and any
    reschedule), the officer's review with its requests for evidence and transfers, and, for a renewal filed from
    30 October 2025 still pending when its card expires, the team's expedite request and USCIS's answer"""
    post = received >= C.IFR
    o = dict(route="appointment" if rng.random() < P_APPT[cat] else "reuse", resched=None, rfe_at=None,
             rfe_resp=None, transfer_at=None, capped=False, exp_req=None, exp_ok=None, exp_out=None, walkin=None)
    m = lead_mean(received, state)
    lead = gam(rng, m, lead_sd(m))
    o["lead_first"] = lead
    u = rng.random()
    p_app = P_RESCHED_APPLICANT[1 if post else 0]
    if o["route"] == "appointment" and u < p_app:
        o["resched"] = "applicant"           # the next open slot, about one queue length on
        lead += gam(rng, m + 8.0, 0.35 * (m + 8.0))
    elif o["route"] == "appointment" and u < p_app + P_RESCHED_USCIS:
        o["resched"] = "uscis"
        lead += gam(rng, *RESCHED_USCIS)
    o["lead"] = lead if o["route"] == "appointment" else 0.0
    base_q = Q_MED * math.exp(Q_SIG * float(rng.standard_normal()))
    q = base_q
    o["rfe"] = rng.random() < P_RFE
    if o["rfe"]:
        o["rfe_at"] = RFE_AT * base_q
        o["rfe_resp"] = o["rfe_at"] + gam(rng, *RFE_RESP)
        q = o["rfe_resp"] + gam(rng, *RFE_DEC)
    o["transfer"] = rng.random() < P_TRANSFER
    if o["transfer"]:
        o["transfer_at"] = float(rng.uniform(0.2, 0.8)) * q
        q += float(rng.uniform(0, 10))
    o["q"] = q
    start = o["lead"]
    w_nat = start + q
    o["w_nat"] = w_nat
    o["denied"] = rng.random() < P_DENY
    w = w_nat
    u = rng.random()
    if u < P_REQ_EARLY:
        req = C.prev_busday(expiry - dt.timedelta(days=int(rng.integers(3, 11))))
    elif u < P_REQ_EARLY + P_REQ_LATE:
        req = C.next_busday(expiry + dt.timedelta(days=int(rng.integers(2, 11))))
    else:
        req = C.next_busday(expiry)
    r_days = (req - received).days
    e_draw = gam(rng, *E_RESP)
    ok = rng.random() < P_EXP_OK
    out_lag = int(rng.integers(2, 9))
    wk = int(rng.integers(4, 11))
    rfe_gap = float(rng.uniform(5, 12))
    if post and counsel and w_nat > r_days and not (term is not None and term <= req):
        o["exp_req"], o["exp_ok"] = req, ok
        o["exp_out"] = C.next_busday(req + dt.timedelta(days=out_lag))
        if ok:
            walkin = None
            if o["route"] == "appointment" and start > r_days - 3:
                walkin = C.next_busday(req + dt.timedelta(days=wk))     # USCIS books an earlier walk-in
                floor_t = (walkin - received).days + 4
            else:
                floor_t = start + 7 if o["route"] == "appointment" else 5
            if o["rfe"] and start + o["rfe_at"] < r_days:
                floor_t = max(floor_t, start + o["rfe_resp"] + rfe_gap)    # an open request for evidence is answered first
            t_dec = max(r_days + e_draw, floor_t)
            if t_dec < w_nat:
                w = t_dec
                o["capped"] = True
                o["walkin"] = walkin
    o["w"] = w
    return o


class Emp:
    __slots__ = ("id", "hire", "term", "state", "family", "enroll", "country", "basis", "spouse", "gc_filed",
                 "gc_approved", "pd", "i140", "h1b_end", "cobra", "tracker")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


class Sp:
    __slots__ = ("id", "principal", "enrolled", "dropped", "cobra", "switch", "gc_approved", "dob_year", "derivative",
                 "late_enroll", "dep_id")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


class Card:
    __slots__ = ("holder", "htype", "cat", "number", "valid_from", "valid_to", "basis", "case", "roster",
                 "roster_cat", "entered_on", "entered_via", "roster_holder")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


class Case:
    """one renewal of one card"""
    __slots__ = ("id", "holder", "htype", "cat", "card", "principal", "opened", "sends", "received", "filed_by",
                 "route", "lead", "lead_first", "resched", "q", "rfe", "rfe_at", "rfe_resp", "transfer", "transfer_at",
                 "w_nat", "capped", "exp_req", "exp_ok", "exp_out", "decided", "denied", "withdrawn", "withdraw_req",
                 "withdraw_ack", "stop", "new_card", "regime", "appt", "appt_first", "walkin", "card_events",
                 "matter", "receipt", "office", "register_seq", "reject_trail", "legacy_id", "new_id", "case_ref",
                 "reg_lag")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


class World:
    def __init__(self):
        self.emps, self.spouses, self.cards, self.cases = [], [], [], []
        self.kids = []          # dependants who are children (benefits only)
        self.others = []        # program employees without a spouse permit in the team's care


def _id_pool(rng, n, lo, hi):
    out = set()
    while len(out) < n:
        out.update(int(x) for x in rng.integers(lo, hi, n - len(out)))
    out = sorted(out)
    rng.shuffle(out)
    return out


def _h1b_end(rng, after, years):
    """an H-1B (and so H-4) end date about `years` after `after`; a quarter of petitions run to 30 September"""
    base = after + dt.timedelta(days=int(365.25 * years))
    if rng.random() < 0.25:
        y = base.year if base.month >= 7 else base.year - 1 if base.month < 3 else base.year
        return dt.date(y, 9, 30)
    return base + dt.timedelta(days=int(rng.integers(-40, 41)))


def c9_valid_to(approved):
    if approved >= C.C9_18M:
        y, m = approved.year + (approved.month + 18 - 1) // 12, (approved.month + 18 - 1) % 12 + 1
        day = min(approved.day, [31, 29 if y % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
        return dt.date(y, m, day) - dt.timedelta(days=1)
    if approved >= C.C9_5Y:
        return dt.date(approved.year + 5, approved.month, min(approved.day, 28)) - dt.timedelta(days=1)
    return dt.date(approved.year + 2, approved.month, min(approved.day, 28)) - dt.timedelta(days=1)


def _card_number(rng, office):
    return "%s%010d" % (office, int(rng.integers(10 ** 9, 10 ** 10)))


def build(seed_note="172"):
    W = World()
    r_emp = C.stream("employees")
    r_sp = C.stream("spouses")
    r_proc = C.stream("process")
    r_card = C.stream("cards")
    r_gc = C.stream("greencard")
    emp_ids = _id_pool(r_emp, 26000, 210000, 989999)
    dep_ids = _id_pool(r_sp, 30000, 1000000, 9999999)
    mp_ids = _id_pool(r_sp, 9000, 10000, 99999)
    ben_ids = _id_pool(r_emp, 26000, 10000000, 99999999)
    it_e, it_d, it_m, it_b = iter(emp_ids), iter(dep_ids), iter(mp_ids), iter(ben_ids)

    def new_emp(hire, country=None, basis="H-1B"):
        e = Emp(id="%06d" % next(it_e), hire=hire, state=pick(r_emp, STATES), family=pick(r_emp, FAMILIES),
                enroll="BEN%08d" % next(it_b), country=country or pick(r_emp, COUNTRY), basis=basis)
        start = max(hire, SIM_START)
        t = r_emp.exponential(1 / ATTRITION)
        term = start + dt.timedelta(days=int(t * 365.25))
        e.term = term if term <= SIM_END else None
        if e.term and e.term.weekday() >= 5:
            e.term = C.prev_busday(e.term)
        e.cobra = bool(e.term and r_emp.random() < P_COBRA)
        W.emps.append(e)
        return e

    def new_spouse(e, entered, derivative=False):
        enrolled = r_sp.random() < P_SPOUSE_ENROLLED
        sid = ("D%07d" % next(it_d)) if enrolled else ("MP-%05d" % next(it_m))
        s = Sp(id=sid, principal=e, enrolled=enrolled, dropped=enrolled and r_sp.random() < P_DROP_2026,
               cobra=e.cobra, dob_year=int(r_sp.integers(1979, 1998)), derivative=derivative)
        e.spouse = s
        W.spouses.append(s)
        return s

    # ---------------------------------------------------------------- the H-4 households, (c)(26)
    h4 = []
    for _ in range(N_H4_STOCK):
        hire = SIM_START - dt.timedelta(days=int(r_emp.integers(200, 365 * 12)))
        e = new_emp(hire)
        s = new_spouse(e, SIM_START)
        vt = SIM_START + dt.timedelta(days=int(r_sp.integers(15, 3 * 365)))
        if r_sp.random() < 0.25:
            vt = dt.date(vt.year if vt.month >= 10 or vt.year == 2021 else vt.year, 9, 30)
            if vt < SIM_START + dt.timedelta(days=15):
                vt = dt.date(2021, 9, 30)
        vf = vt - dt.timedelta(days=int(r_sp.choice([1095, 1095, 1095, 730, 365])))
        h4.append((e, s, vf, vt, "initial" if r_sp.random() < 0.3 else "renewal"))
    t = 0.0
    while True:
        t += r_sp.exponential(1 / H4_INFLOW)
        d = SIM_START + dt.timedelta(days=int(t * 365.25))
        if d > dt.date(2027, 6, 30):
            break
        if r_emp.random() < 0.45:
            e = new_emp(d - dt.timedelta(days=int(r_emp.integers(0, 120))))
        else:
            e = new_emp(d - dt.timedelta(days=int(r_emp.integers(365, 365 * 9))))
            if e.term and e.term <= d:
                e.term = None if r_emp.random() < 0.5 else d + dt.timedelta(days=int(r_emp.integers(200, 2000)))
                if e.term and e.term > SIM_END:
                    e.term = None
        s = new_spouse(e, d)
        vt = _h1b_end(r_sp, d, float(r_sp.choice([3, 3, 3, 2, 1.5])))
        h4.append((e, s, d, vt, "initial"))

    # the summer 2025 green-card wave: some H-4 households file I-485s and the spouse moves to (c)(9)
    for e, s, vf, vt, basis in h4:
        e.basis = "H-1B"
        if e.country == "All other" and r_gc.random() < 0.55:
            # non-backlogged principals file I-485 a year or two after the H-4 card starts and are approved fast
            f = vf + dt.timedelta(days=int(r_gc.integers(300, 900)))
            e.gc_filed = f
            e.gc_approved = f + dt.timedelta(days=int(r_gc.integers(240, 700)))
            s.switch = f
        elif vf >= dt.date(2025, 6, 2) or e.hire >= dt.date(2025, 6, 2):
            continue
        elif e.country == "India" and r_gc.random() < 0.075:
            e.gc_filed = dt.date(2025, 6, 2) + dt.timedelta(days=int(r_gc.integers(0, 120)))
            e.gc_approved = None if r_gc.random() < 0.9 else e.gc_filed + dt.timedelta(days=int(r_gc.integers(330, 520)))
            s.switch = e.gc_filed
        elif e.country == "China" and r_gc.random() < 0.10:
            e.gc_filed = dt.date(2025, 6, 2) + dt.timedelta(days=int(r_gc.integers(0, 120)))
            e.gc_approved = None if r_gc.random() < 0.8 else e.gc_filed + dt.timedelta(days=int(r_gc.integers(300, 500)))
            s.switch = e.gc_filed
        if s.switch and e.gc_approved:
            s.gc_approved = e.gc_approved

    # ---------------------------------------------------------------- the (c)(9) households without an H-4 phase
    c9 = []

    def c9_house(filed, pending_until, n_cards_known):
        hire = filed - dt.timedelta(days=int(r_emp.integers(700, 365 * 9)))
        e = new_emp(hire, country="India" if r_gc.random() < 0.82 else "China", basis="I-485 pending")
        if e.term and e.term < SIM_START:
            e.term = SIM_START + dt.timedelta(days=int(r_emp.integers(30, 2400)))
            e.term = e.term if e.term <= SIM_END else None
        e.gc_filed = filed
        e.gc_approved = pending_until
        s = None
        if r_sp.random() < 0.6:
            s = new_spouse(e, filed, derivative=True)
            s.gc_approved = pending_until
        c9.append((e, s))
        return e, s

    for _ in range(820):                     # the October 2020 wave, still pending into 2024 for most
        f = dt.date(2020, 10, 1) + dt.timedelta(days=int(r_gc.integers(0, 60)))
        appr = None if r_gc.random() < 0.55 else dt.date(2024, 1, 1) + dt.timedelta(days=int(r_gc.integers(0, 1100)))
        c9_house(f, appr, 3)
    for _ in range(420):                     # filings through 2022 and to September 2023 (two-year cards)
        f = dt.date(2022, 1, 10) + dt.timedelta(days=int(r_gc.integers(0, 600)))
        appr = None if r_gc.random() < 0.7 else f + dt.timedelta(days=int(r_gc.integers(700, 1500)))
        c9_house(f, appr, 2)
    for _ in range(260):                     # filings from late 2023 into 2025 (five-year cards)
        f = dt.date(2023, 9, 1) + dt.timedelta(days=int(r_gc.integers(0, 640)))
        appr = None if r_gc.random() < 0.75 else f + dt.timedelta(days=int(r_gc.integers(500, 1200)))
        c9_house(f, appr, 1)
    for _ in range(430):                     # the summer 2025 wave of households new to the team's care
        f = dt.date(2025, 6, 2) + dt.timedelta(days=int(r_gc.integers(0, 120)))
        appr = None if r_gc.random() < 0.9 else f + dt.timedelta(days=int(r_gc.integers(330, 520)))
        c9_house(f, appr, 1)
    for _ in range(300):                     # filings through 2026
        f = dt.date(2025, 10, 6) + dt.timedelta(days=int(r_gc.integers(0, 400)))
        if f > C.EXPORT - dt.timedelta(days=20):
            continue
        appr = None
        c9_house(f, appr, 1)

    # program employees with no spouse permit in the team's care (they fill the roster as real HR extracts do)
    for _ in range(5200):
        hire = dt.date(2008, 1, 1) + dt.timedelta(days=int(r_emp.integers(0, 365 * 18.8)))
        e = new_emp(hire, basis=pick(r_emp, (("H-1B", 0.78), ("L-1", 0.09), ("O-1", 0.03), ("TN", 0.02),
                                             ("E-3", 0.03), ("H-1B1", 0.01), ("I-485 pending", 0.04))))
        W.others.append(e)

    # ---------------------------------------------------------------- cards and renewals
    seq = [0]

    def make_card(holder, htype, cat, vf, vt, basis, office=None, case=None):
        office = office or ("MSC" if cat == "(c)(9)" and r_card.random() < 0.3 else
                            str(r_card.choice(["IOE", "IOE", "IOE", "EAC", "WAC", "LIN", "SRC"])))
        c = Card(holder=holder, htype=htype, cat=cat, number=_card_number(r_card, office), valid_from=vf,
                 valid_to=vt, basis=basis, case=case)
        W.cards.append(c)
        return c

    def active(e, d):
        return e.term is None or e.term > d

    def renew_chain(holder, htype, cat, card, principal, stop_at=None):
        """renew `card` while the holder stays in the team's care; each renewal's card feeds the next"""
        while card.valid_to < SIM_END + dt.timedelta(days=200):
            opened = card.valid_to - dt.timedelta(days=OPEN_BEFORE)
            if opened > SIM_END:
                return
            if not active(principal, opened):
                return
            if stop_at and opened >= stop_at:
                return
            if cat == "(c)(9)" and principal.gc_approved and principal.gc_approved <= opened:
                return
            case = run_case(holder, htype, cat, card, principal)
            if case is None or case.new_card is None:
                return
            card = case.new_card

    def run_case(holder, htype, cat, card, principal):
        seq[0] += 1
        rng = r_proc
        opened = C.next_busday(card.valid_to - dt.timedelta(days=OPEN_BEFORE))
        cs = Case(id=seq[0], holder=holder, htype=htype, cat=cat, card=card, principal=principal, opened=opened,
                  filed_by="Counsel", sends=[], reject_trail=[])
        # dispatch, the lockbox, rejections and courier returns
        sent = C.next_busday(opened + dt.timedelta(days=max(4.0, paper_days(rng))))
        received = None
        tries = 0
        while received is None and tries < 5:
            tries += 1
            arrive = C.next_busday(sent + dt.timedelta(days=int(rng.integers(1, 4))))
            send = dict(sent=sent, arrive=arrive, outcome="Receipted", returned=None, notice=None, copy=None)
            cs.sends.append(send)
            if rng.random() < P_COURIER:
                send["outcome"] = "Courier"
                send["returned"] = C.next_busday(sent + dt.timedelta(days=int(rng.integers(3, 9))))
                sent = C.next_busday(send["returned"] + dt.timedelta(days=max(1.0, gam(rng, 4.0, 2.0))))
                continue
            p_rej = P_REJECT if tries == 1 else P_REREJECT
            if rng.random() < p_rej:
                send["outcome"] = "Rejected"
                notice = C.next_busday(arrive + dt.timedelta(days=max(3.0, gam(rng, 12.0, 4.0))))
                send["notice"] = notice
                applicant_only = rng.random() < P_APPLICANT_ONLY
                send["copy"] = "Applicant" if applicant_only else "Counsel"
                if applicant_only:
                    send["returned"] = C.next_busday(notice + dt.timedelta(days=int(rng.integers(7, 26))))
                else:
                    send["returned"] = C.next_busday(notice + dt.timedelta(days=int(rng.integers(5, 15))))
                fate = rng.random()
                if fate < 0.04:
                    cs.reject_trail.append("abandoned")
                    cs.received = None
                    W.cases.append(cs)
                    return cs
                if fate < 0.04 + (0.35 if applicant_only else 0.03):
                    # the applicant refiled online herself; the team registers the new filing when told of it
                    rec = C.next_busday(notice + dt.timedelta(days=max(4.0, gam(rng, 16.0, 6.0))))
                    cs.reject_trail.append("self")
                    received = rec
                    cs.filed_by = "Applicant"
                    break
                sent = C.next_busday(send["returned"] + dt.timedelta(days=max(1.0, gam(rng, 9.0, 4.0))))
                continue
            received = arrive
        if received is None:
            W.cases.append(cs)
            return cs
        # "within 30 days" of a rejection notice reads one way: no refiling lands on day 30 or 31
        for s in cs.sends:
            if s["outcome"] == "Rejected" and (received - s["notice"]).days in (30, 31):
                received = C.next_busday(received + dt.timedelta(days=2))
                if cs.filed_by == "Counsel":
                    cs.sends[-1]["arrive"] = received
        cs.received = received
        cs.regime = "post" if received >= C.IFR else "pre"
        # the wait's stages
        st = draw_wait(rng, cat, principal.state, received, card.valid_to, cs.filed_by == "Counsel", principal.term)
        for k in ("route", "lead", "lead_first", "resched", "q", "rfe", "rfe_at", "rfe_resp", "transfer",
                  "transfer_at", "w_nat", "denied", "capped", "exp_req", "exp_ok", "exp_out", "walkin"):
            setattr(cs, k, st[k])
        w = st["w"]
        expiry = card.valid_to
        decided = C.next_busday(received + dt.timedelta(days=w))
        cs.decided = decided
        cs.appt = C.next_busday(received + dt.timedelta(days=cs.lead)) if cs.route == "appointment" else None
        cs.appt_first = C.next_busday(received + dt.timedelta(days=cs.lead_first)) if cs.resched else cs.appt
        if cs.walkin and not (cs.appt and cs.walkin < cs.appt):
            cs.walkin = None
        # the card it produces
        if not cs.denied:
            if cat == "(c)(26)":
                ext = float(rng.choice([3, 3, 3, 3, 3, 3, 2, 2, 1, 2.5]))
                vt = _h1b_end(rng, expiry, ext) if rng.random() < 0.15 else \
                    expiry + dt.timedelta(days=int(round(365.25 * ext)))
                if vt <= decided:
                    vt = decided + dt.timedelta(days=365)
            else:
                vt = c9_valid_to(decided)
            cs.new_card = make_card(holder, htype, cat, decided, vt, "renewal", case=cs)
        W.cases.append(cs)
        return cs

    # (c)(26) chains
    for e, s, vf, vt, basis in h4:
        card = make_card(s, "Spouse", "(c)(26)", vf, vt, basis)
        renew_chain(s, "Spouse", "(c)(26)", card, e, stop_at=s.switch)
        if s.switch:
            # the spouse files as a derivative with the I-485; her (c)(9) card comes about four months later
            appr = C.next_busday(s.switch + dt.timedelta(days=int(r_gc.integers(80, 170))))
            if appr < SIM_END and active(e, s.switch):
                c = make_card(s, "Spouse", "(c)(9)", appr, c9_valid_to(appr), "initial")
                if not (e.gc_approved and e.gc_approved <= appr):
                    renew_chain(s, "Spouse", "(c)(9)", c, e)
            ae = C.next_busday(e.gc_filed + dt.timedelta(days=int(r_gc.integers(80, 170))))
            if ae < SIM_END and active(e, e.gc_filed):
                c = make_card(e, "Employee", "(c)(9)", ae, c9_valid_to(ae), "initial")
                e.basis = "I-485 pending"
                if not (e.gc_approved and e.gc_approved <= ae):
                    renew_chain(e, "Employee", "(c)(9)", c, e)

    # (c)(9) chains for the households without an H-4 phase
    for e, s in c9:
        for holder, htype in ((e, "Employee"), (s, "Spouse")):
            if holder is None:
                continue
            appr = C.next_busday(e.gc_filed + dt.timedelta(days=int(r_gc.integers(80, 170))))
            card = make_card(holder, htype, "(c)(9)", appr, c9_valid_to(appr), "initial")
            # cards before the record renewed in the team's earlier system: walk the chain to the record
            while card.valid_to < dt.date(2023, 12, 1) + dt.timedelta(days=OPEN_BEFORE) and \
                    (e.gc_approved is None or e.gc_approved > card.valid_to) and active(e, card.valid_to):
                d = card.valid_to - dt.timedelta(days=int(r_gc.integers(25, 90)))
                card = make_card(holder, htype, "(c)(9)", d, c9_valid_to(d), "renewal")
            if active(e, card.valid_from):
                renew_chain(holder, htype, "(c)(9)", card, e)

    # departures stop the team's work on a pending renewal; green cards withdraw it
    for cs in W.cases:
        if cs.received is None:
            continue
        p = cs.principal
        if p.term and cs.opened <= p.term <= cs.received and cs.filed_by == "Counsel":
            cs.stop = p.term          # the team stopped before USCIS had the filing in hand: no receipt in its care
            cs.received = None
            if cs.new_card is not None:
                cs.new_card.case = None
                cs.new_card.basis = "void"
            cs.new_card = None
            continue
        if p.term and cs.received < p.term < cs.decided:
            cs.stop = p.term
        if cs.cat == "(c)(9)" and p.gc_approved and cs.received < p.gc_approved < cs.decided:
            cs.withdraw_req = C.next_busday(p.gc_approved + dt.timedelta(days=int(r_proc.integers(1, 7))))
            ack = C.next_busday(cs.withdraw_req + dt.timedelta(days=int(r_proc.integers(18, 46))))
            if ack < cs.decided:
                cs.withdrawn = True
                cs.withdraw_ack = ack
                cs.new_card = None
    # the cards that a withdrawn or stopped renewal would have produced do not exist in anyone's hands at the export
    W.cards = [c for c in W.cards if c.basis != "void" and not (c.case is not None and c.case.withdrawn)]

    # spouses off the plan at intake who joined it later: Benefits gives each a dependant ID from that day
    r_le = C.stream("late enrollment")
    first = {}
    for c in W.cards:
        if c.htype == "Spouse" and (id(c.holder) not in first or c.valid_from < first[id(c.holder)]):
            first[id(c.holder)] = c.valid_from
    for s in W.spouses:
        s.late_enroll, s.dep_id = None, None
        if s.enrolled or id(s) not in first:
            continue
        u, v = r_le.random(), r_le.random()
        if u >= P_LATE_ENROLL:
            continue
        start = max(first[id(s)], dt.date(2021, 1, 1)) + dt.timedelta(days=60)
        if v < 0.6:                                   # open enrolment: coverage from the next 1 January
            d = dt.date(start.year + 1 + int(r_le.integers(0, 3)), 1, 1)
        else:                                         # a life event (her own employer's cover ended)
            d = start + dt.timedelta(days=int(r_le.integers(0, 1400)))
        e = s.principal
        if d > C.EXPORT or (e.term is not None and e.term <= d):
            continue
        s.late_enroll = d
        s.dep_id = "D%07d" % next(it_d)
    return W


def forward_truth(W):
    """the renewals the team files from 1 January to 31 March 2027 (received in the quarter), withdrawn ones left out:
    their true waits in days"""
    out = []
    for cs in W.cases:
        if cs.received and C.Q_START <= cs.received <= C.Q_END and cs.filed_by == "Counsel" and not cs.withdrawn:
            out.append((cs.decided - cs.received).days)
    return out


def process_q80(W, reps=200, seed="process"):
    """the generator's process 80th percentile for the quarter: every renewal counsel files that is received from 1
    January to 31 March 2027, with its own category, state, receipt and card, its wait re-drawn `reps` times under the
    generating process; withdrawn renewals left out as standard 4.2 leaves them out"""
    rng = C.stream("process truth/" + seed)
    fw = [cs for cs in W.cases if cs.received and C.Q_START <= cs.received <= C.Q_END and cs.filed_by == "Counsel"]
    waits = []
    for _ in range(reps):
        for cs in fw:
            o = draw_wait(rng, cs.cat, cs.principal.state, cs.received, cs.card.valid_to, True, cs.principal.term)
            dec = C.next_busday(cs.received + dt.timedelta(days=o["w"]))
            p = cs.principal
            if cs.cat == "(c)(9)" and p.gc_approved and cs.received < p.gc_approved < dec:
                req = C.next_busday(p.gc_approved + dt.timedelta(days=int(rng.integers(1, 7))))
                ack = C.next_busday(req + dt.timedelta(days=int(rng.integers(18, 46))))
                if ack < dec:
                    continue
            waits.append((dec - cs.received).days)
    w = np.asarray(waits, float)
    return float(np.quantile(w, 0.8)), len(fw), w
