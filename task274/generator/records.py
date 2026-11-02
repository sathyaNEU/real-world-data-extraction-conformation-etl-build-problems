"""task274 records: every case, charge, docket event and provider report row the pack carries.

The lottery population comes from world.draw_main at the chosen seed and is never redrawn here; every
other record draws from its own stream (np.random.default_rng([274, k])), so adding or changing one kind
of record moves nothing else.
"""
import datetime as dt
import math
from collections import defaultdict

import numpy as np
from faker import Faker

import world as W

D = dt.date
TD = dt.timedelta

RETENTION = 0.05     # the share of each restitution payment the agreement lets the provider keep (clause 6)
MAIN_SEED = 276291   # found by world.pick_main_seed; checks.py re-asserts world.main_seed_ok on it

ELIG = W.ELIGIBLE_OFFENCES
ELIG_P = np.array([o[4] for o in ELIG]) / sum(o[4] for o in ELIG)
INELIG = [o for o in W.OFFENCES if not o[1]]
INELIG_P = np.array([o[4] for o in INELIG]) / sum(o[4] for o in INELIG)
OFF_INDEX = {o[0]: i for i, o in enumerate(W.OFFENCES)}


def rng_for(k):
    return np.random.default_rng([274, k])


def business_days(y, m):
    d = D(y, m, 1)
    out = []
    while d.month == m:
        if d.weekday() < 5 and d not in W.HOLIDAYS:
            out.append(d)
        d += TD(1)
    return out


def prev_month(d):
    return W.add_months(d, -1)


class Case:
    __slots__ = ("cid", "lottery", "lot", "offered", "path", "division", "ctype", "filed", "arraigned",
                 "offence_date", "charges", "defendant", "events", "disp", "convicted", "number_legacy",
                 "number_cms", "main", "site", "term_start", "term_end", "term_date", "agree", "k",
                 "exit_type", "requirement", "dup_charge")

    def __init__(self, **kw):
        for s in self.__slots__:
            setattr(self, s, kw.get(s))


def make_people(n, seed):
    fk = Faker("en_US")
    fk.seed_instance(seed)
    rng = rng_for(seed)
    out = []
    for i in range(n):
        sex = "F" if rng.uniform() < 0.32 else "M"
        first = fk.first_name_female() if sex == "F" else fk.first_name_male()
        last = fk.last_name()
        dob = D(1958, 1, 1) + TD(int(rng.integers(0, 365 * 46)))
        out.append(dict(first=first, last=last, dob=dob))
    return out


def offence_lag(rng, off):
    """Days from offense to complaint: drug possession waits on the crime laboratory."""
    if off[1] == "C" or off[0] == "Possession of a dangerous drug for sale":
        return int(rng.integers(20, 121))
    if rng.uniform() < 0.18:      # the suspect identified or found weeks after the offense
        return int(rng.integers(20, 151))
    return int(rng.integers(0, 22))


def pick_division(rng):
    return W.DIVISIONS[int(rng.choice(4, p=W.DIV_SHARE))]


def extra_charges(rng, off):
    """Secondary charges, eligible with eligible leads (the policy requires every count eligible)."""
    name = off[0]
    if name == "Possession of a controlled substance" and rng.uniform() < 0.45:
        return [W.OFFENCES[OFF_INDEX["Possession of drug paraphernalia"]]]
    if name == "Disorderly conduct" and rng.uniform() < 0.10:
        return [W.OFFENCES[OFF_INDEX["Criminal trespass"]]]
    if name == "Driving under the influence" and rng.uniform() < 0.35:
        return [W.OFFENCES[OFF_INDEX["Driving on a suspended license"]]]
    if name == "Assault, domestic violence" and rng.uniform() < 0.25:
        return [W.OFFENCES[OFF_INDEX["Criminal mischief, under 1,000"]]]
    if name == "Burglary, third degree" and rng.uniform() < 0.40:
        return [W.OFFENCES[OFF_INDEX["Theft, property under 1,000"]]]
    return []


def ordinary_outcome(rng, ctype, filed):
    med = 105 if ctype == "CM" else 165
    days = int(round(rng.lognormal(math.log(med), 0.55)))
    conv = rng.uniform() < (0.64 if ctype == "CM" else 0.70)
    return filed + TD(max(days, 9)), bool(conv)


def build_cases(main_rows):
    """Every case in the extract: the lottery cases (main population) and every other filing."""
    rng = rng_for(1)
    cases = []
    # --- lottery cases: arraigned in the month before each draw, first-time defendants, eligible charges
    for r in main_rows:
        ld = r["draw"]
        pm = prev_month(ld)
        arr = business_days(pm.year, pm.month)
        arraigned = arr[int(rng.integers(0, len(arr)))]
        filed = arraigned - TD(int(rng.integers(2, 16)))
        off = ELIG[int(rng.choice(len(ELIG), p=ELIG_P))]
        offence_date = filed - TD(offence_lag(rng, off))
        ch = [off] + extra_charges(rng, off)
        c = Case(lottery=True, lot=r["lot"], offered=r["offered"], path=r["path"], division=pick_division(rng),
                 ctype=off[5], filed=filed, arraigned=arraigned, offence_date=offence_date, charges=ch,
                 disp=r["disp"], convicted=r["convicted"], main=r, term_start=r.get("term_start"),
                 term_end=r.get("term_end"), term_date=r.get("term_date"), agree=r.get("agree"), k=r.get("k"))
        cases.append(c)
    # --- every other filing, 1 April 2025 to 31 August 2026
    d = W.EXTRACT_FROM
    while d <= W.CUT:
        if d.weekday() < 5 and d not in W.HOLIDAYS:
            n_rep = rng.poisson(8.6)       # eligible offences, defendants with a record
            n_inel = rng.poisson(19.5)     # offences outside the programme
            # first-time eligible defendants arraigned outside the list months
            outside = (d < D(2025, 4, 22)) or (d >= D(2026, 4, 18))
            n_ft = rng.poisson(13.8) if outside else 0
            for kind, n in (("repeat", n_rep), ("inelig", n_inel), ("first", n_ft)):
                for _ in range(int(n)):
                    if kind == "inelig":
                        off = INELIG[int(rng.choice(len(INELIG), p=INELIG_P))]
                    else:
                        off = ELIG[int(rng.choice(len(ELIG), p=ELIG_P))]
                    filed = d
                    arraigned = filed + TD(int(rng.integers(2, 16)))
                    disp, conv = ordinary_outcome(rng, off[5], filed)
                    c = Case(lottery=False, lot=None, offered=None, path="ordinary", division=pick_division(rng),
                             ctype=off[5], filed=filed, arraigned=arraigned,
                             offence_date=filed - TD(offence_lag(rng, off)), charges=[off] + extra_charges(rng, off),
                             disp=disp, convicted=conv, main=None)
                    c.exit_type = kind
                    cases.append(c)
        d += TD(1)
    # filing order fixes case numbers
    cases.sort(key=lambda c: (c.filed, c.division, 0 if c.lottery else 1, c.offence_date, c.charges[0][0]))
    seq = defaultdict(int)
    gaps = rng_for(10)
    for i, c in enumerate(cases):
        c.cid = i
        yy = c.filed.year % 100
        # sealed and juvenile-transfer cases take numbers in the same series and are not in the extract
        seq[(c.division, yy, c.ctype)] += 1 + int(gaps.uniform() < 0.03)
        n = seq[(c.division, yy, c.ctype)]
        if c.filed < W.CUTOVER:
            c.number_legacy = "%s%02d%s%05d" % (c.division, yy, c.ctype, n)
            c.number_cms = "%02d-%s-%05d-%s" % (yy, c.ctype, n, c.division)
        else:
            c.number_legacy = None
            c.number_cms = "%02d-%s-%05d-%s" % (yy, c.ctype, n + 5000, c.division)
    # defendants: lottery and first-time defendants are new people; repeat defendants recur
    lot_or_first = [c for c in cases if c.lottery or c.exit_type == "first"]
    others = [c for c in cases if not (c.lottery or c.exit_type == "first")]
    people = make_people(len(lot_or_first) + 4200, 2741)
    for i, c in enumerate(lot_or_first):
        c.defendant = dict(people[i], pid=100000 + i)
    pool = people[len(lot_or_first):]
    prng = rng_for(2)
    for c in others:
        j = int(prng.integers(0, len(pool)))
        c.defendant = dict(pool[j], pid=200000 + j)
    return cases


# ---------------------------------------------------------------------------------------------------------
# docket events

LEG = {
    "FIL": "COMPLAINT FILED",
    "ARR": "ARRAIGNMENT HELD - NOT GUILTY PLEA ENTERED",
    "PTC": "PRETRIAL CONFERENCE HELD",
    "CNT": "HEARING CONTINUED",
    "WAR": "BENCH WARRANT ISSUED - FAILURE TO APPEAR",
    "WRR": "WARRANT RETURNED - DEFENDANT IN COURT",
    "DVO": "NOTICE OF OFFER OF PRETRIAL DIVERSION FILED",
    "DVX": "DEFENDANT DECLINED PRETRIAL DIVERSION",
    "DVA": "PRETRIAL DIVERSION AGREEMENT FILED - CASE CONTINUED FOR DIVERSION TERM",
    "STS": "DIVERSION STATUS REVIEW",
    "DVT": "NOTICE OF TERMINATION FROM DIVERSION - CASE RESTORED TO CALENDAR",
    "DVC": "DISMISSED - DIVERSION COMPLETED",
    "DGP": "DISPOSED - PLEA OF GUILTY ACCEPTED",
    "DGT": "DISPOSED - FOUND GUILTY AT TRIAL",
    "DSR": "DISPOSED - FOUND GUILTY ON STIPULATED RECORD",
    "DDM": "DISPOSED - DISMISSED ON MOTION OF THE STATE",
    "DNP": "DISPOSED - NOLLE PROSEQUI",
    "DAQ": "DISPOSED - ACQUITTED",
    "SEN": "SENTENCE IMPOSED",
}
CMS = {
    "FIL": "Complaint Filed",
    "ARR": "Arraignment - Plea of Not Guilty",
    "PTC": "Pretrial Conference",
    "CNT": "Hearing Continued",
    "WAR": "Bench Warrant Issued (FTA)",
    "WRR": "Bench Warrant Returned",
    "DVO": "Notice of Pretrial Diversion Offer",
    "DVX": "Pretrial Diversion Declined",
    "DVA": "Pretrial Diversion Agreement",
    "STS": "Diversion Review Hearing",
    "DVT": "Pretrial Diversion Terminated - Restored to Calendar",
    "DVC": "Dismissed - Pretrial Diversion Completed",
    "DGP": "Disposition - Guilty Plea",
    "DGT": "Disposition - Guilty Verdict",
    "DSR": "Disposition - Guilty, Stipulated Record",
    "DDM": "Disposition - Dismissed (State's Motion)",
    "DNP": "Disposition - Nolle Prosequi",
    "DAQ": "Disposition - Not Guilty",
    "SEN": "Sentencing",
}
EFILED = {"FIL", "DVO", "DVX", "DVA"}     # filed electronically by counsel, any hour
CONVICTION_CODES = {"DGP", "DGT", "DSR"}
DISPOSITION_CODES = {"DGP", "DGT", "DSR", "DDM", "DNP", "DAQ", "DVC"}


def fmt_term(c):
    return "TERM %s TO %s" % (c.term_start.strftime("%m/%d/%Y"), c.term_end.strftime("%m/%d/%Y"))


def case_events(c, rng):
    """(date, code, detail) for one case, every event through the evaluation date and none after it."""
    ev = [(c.filed, "FIL", ""), (c.arraigned, "ARR", "")]
    if c.lottery:
        ld = c.main["draw"]
        if c.offered:
            ev.append((ld + TD(int(rng.integers(1, 4))), "DVO", ""))
        if c.path == "declined":
            ev.append((c.main["declined_on"], "DVX", ""))
        if c.path in ("not_offered", "declined"):
            p1 = max(c.arraigned + TD(int(rng.integers(24, 46))), ld + TD(int(rng.integers(8, 30))))
            if p1 < c.disp:
                ev.append((p1, "PTC", ""))
                if rng.uniform() < 0.35 and p1 + TD(30) < c.disp:
                    ev.append((p1 + TD(int(rng.integers(26, 40))), "PTC", ""))
            ev += disposition_events(c, rng)
        else:
            ev.append((c.agree, "DVA", fmt_term(c)))
            review = W.add_months(c.term_start, 6) + TD(int(rng.integers(3, 20)))
            if c.path == "completed" or (c.term_date and review < c.term_date):
                ev.append((review, "STS", ""))
            if c.path == "terminated":
                ev.append((c.term_date, "DVT", ""))
                p1 = c.term_date + TD(int(rng.integers(14, 36)))
                if p1 < c.disp:
                    ev.append((p1, "PTC", ""))
                ev += disposition_events(c, rng, after_termination=True)
            else:
                ev.append((c.disp, "DVC", ""))
    else:
        if rng.uniform() < 0.08:
            w = c.arraigned + TD(int(rng.integers(20, 60)))
            if w < c.disp - TD(10):
                ev.append((w, "WAR", ""))
                ev.append((w + TD(int(rng.integers(3, max(4, min(90, (c.disp - w).days - 2))))), "WRR", ""))
        p1 = c.arraigned + TD(int(rng.integers(24, 46)))
        while p1 < c.disp - TD(5):
            ev.append((p1, "PTC", ""))
            if rng.uniform() < 0.12:
                ev.append((p1, "CNT", ""))
            p1 += TD(int(rng.integers(28, 56)))
        ev += disposition_events(c, rng)
    ev = [e for e in ev if e[0] <= W.CUT]
    ev.sort(key=lambda e: (e[0], list(LEG).index(e[1])))
    return ev


def disposition_events(c, rng, after_termination=False):
    if c.convicted:
        if after_termination:
            code = "DSR" if rng.uniform() < 0.85 else "DGP"
        else:
            code = "DGP" if rng.uniform() < 0.9 else "DGT"
        return [(c.disp, code, ""), (c.disp + TD(0 if code == "DGP" else int(rng.integers(14, 30))), "SEN", "")]
    code = rng.choice(["DDM", "DNP", "DAQ"], p=[0.6, 0.3, 0.1]) if not after_termination else "DDM"
    return [(c.disp, str(code), "")]


def local_offset(d):
    """Central time: UTC-5 from the second Sunday of March to the first Sunday of November, else UTC-6."""
    y = d.year
    mar = D(y, 3, 8)
    while mar.weekday() != 6:
        mar += TD(1)
    nov = D(y, 11, 1)
    while nov.weekday() != 6:
        nov += TD(1)
    return 5 if mar <= d < nov else 6


def cms_stamp(d, code, rng, migrated):
    """The CMS keeps every event in UTC; migrated events carry local midnight."""
    off = local_offset(d)
    if migrated:
        local = dt.datetime(d.year, d.month, d.day, 0, 0)
    elif code in EFILED:
        # counsel e-file from early morning to late evening; never across a month end for an agreement
        hi = 23 if not (code == "DVA" and (d + TD(1)).day == 1) else 17
        local = dt.datetime(d.year, d.month, d.day, int(rng.integers(7, hi)), int(rng.integers(0, 60)))
    else:
        local = dt.datetime(d.year, d.month, d.day, int(rng.integers(8, 17)), int(rng.integers(0, 60)))
    return local + TD(hours=off)


def build_events(cases):
    rng = rng_for(3)
    legacy, cms = [], []
    clerks = ["JMR", "TLK", "AVB", "DSW", "KRP", "MEL", "CJH"]
    for c in cases:
        ev = case_events(c, rng)
        c.events = ev
        disposed_pre = any(code in DISPOSITION_CODES and d < W.CUTOVER for d, code, _ in ev)
        in_legacy = c.filed < W.CUTOVER
        in_cms = (c.filed >= W.CUTOVER) or (in_legacy and not disposed_pre)
        for d, code, detail in ev:
            if in_legacy and d < W.CUTOVER:
                txt = LEG[code] + ((" - " + detail) if detail else "")
                row = (c.number_legacy, c.division, d.strftime("%m/%d/%Y"), code, txt, clerks[int(rng.integers(0, len(clerks)))])
                legacy.append(row)
                if rng.uniform() < 0.012:
                    legacy.append(row)   # clerk re-entry
            if in_cms:
                migrated = d < W.CUTOVER
                ts = cms_stamp(d, code, rng, migrated)
                det = detail.title().replace(" To ", " to ") if detail else ""
                cms.append((c.number_cms, W.DIV_NAME[c.division], ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
                            CMS[code], det, "MIGRATED" if migrated else ("E-FILED" if code in EFILED else "CLERK")))
    legacy.sort(key=lambda r: (dt.datetime.strptime(r[2], "%m/%d/%Y"), r[0], r[3]))
    cms.sort(key=lambda r: (r[2], r[0], r[3]))
    return legacy, cms


# ---------------------------------------------------------------------------------------------------------
# charges


def build_charges(cases):
    rng = rng_for(4)
    legacy, cms = [], []
    for c in cases:
        disposed_pre = c.disp < W.CUTOVER
        in_legacy = c.filed < W.CUTOVER
        in_cms = (c.filed >= W.CUTOVER) or (in_legacy and not disposed_pre)
        defn = c.defendant
        name = "%s, %s" % (defn["last"].upper(), defn["first"].upper())
        for seq, off in enumerate(c.charges, 1):
            code_as_charged = off[2] if c.offence_date < W.RECODE else off[3]   # the law in force on the offense date
            if in_legacy:
                row = (c.number_legacy, c.division, c.ctype, c.filed.strftime("%m/%d/%Y"), str(defn["pid"]), name,
                       defn["dob"].strftime("%m/%d/%Y"), c.offence_date.strftime("%m/%d/%Y"), str(seq), code_as_charged)
                legacy.append(row)
                if rng.uniform() < 0.01:
                    legacy.append(row)
            if in_cms:
                # the conversion carried every open case's charges to the 2026 sections; a case filed in the new
                # system is charged under the sections in force on the offense date
                code_now = off[3] if c.filed < W.CUTOVER else code_as_charged
                cms.append((c.number_cms, W.DIV_NAME[c.division], "Misdemeanor" if c.ctype == "CM" else "Felony",
                            c.filed.isoformat(), "%s %s" % (defn["first"], defn["last"]), defn["dob"].isoformat(),
                            c.offence_date.isoformat(), str(seq), code_now))
    return legacy, cms


# ---------------------------------------------------------------------------------------------------------
# the lottery roster


def roster(cases):
    rows = defaultdict(list)
    for c in cases:
        if c.lottery:
            rows[c.lot].append(c)
    out = {}
    rng = rng_for(5)
    for L, cs in rows.items():
        cs = sorted(cs, key=lambda c: (c.arraigned, c.number_legacy or c.number_cms))
        lines = []
        for c in cs:
            num = c.number_legacy if c.number_legacy else c.number_cms
            code = c.charges[0][2] if c.offence_date < W.RECODE else c.charges[0][3]
            lines.append((num, "%s, %s" % (c.defendant["last"], c.defendant["first"]), W.DIV_NAME[c.division],
                          c.arraigned, code, "Y" if c.offered else "N"))
        out[L] = lines
    return out


# ---------------------------------------------------------------------------------------------------------
# the provider: participants, sites, community service and restitution, month by month


def court_ref_variant(num, rng):
    div, yy, typ, n = num[:2], num[2:4], num[4:6], num[6:]
    k = int(rng.integers(0, 5))
    if k == 0:
        return num
    if k == 1:
        return "%s-%s-%s-%s" % (div, yy, typ, n)
    if k == 2:
        return "%s%s%d %s" % (yy, typ, int(n), div)
    if k == 3:
        return "%s %s %s %d" % (div, yy, typ, int(n))
    return "20%s-%s-%s (%s)" % (yy, typ, n, div)


def build_participants(cases):
    """One record per participant: site, requirement, and dated hours and payments."""
    rng = rng_for(6)
    parts = []
    for c in cases:
        if not (c.lottery and c.path in ("terminated", "completed")):
            continue
        site_div = c.division if rng.uniform() < 0.86 else W.DIVISIONS[int(rng.integers(0, 4))]
        site = W.DIV_NAME[site_div]
        req = 24 if c.ctype == "CM" else 40
        end = c.term_date if c.path == "terminated" else c.term_end
        if c.path == "terminated":
            if c.k == 12:
                exit_type = "final review"
            else:
                exit_type = "new arrest" if rng.uniform() < 0.48 else "non-compliance"
        else:
            exit_type = "completed"
        # community service shifts: hours accrue month by month until the requirement is met
        shifts = []
        done = 0
        m0 = c.term_start
        while m0 <= min(end, W.CUT):
            me = W.month_end(m0)
            if done < req:
                weak = c.path == "terminated" and exit_type != "final review"
                h = int(rng.choice([0, 0, 2, 3, 4, 4, 5, 5, 6, 8] if not weak else [0, 0, 0, 2, 3, 4]))
                if exit_type == "final review":
                    h = int(rng.choice([0, 0, 2, 3, 4]))
                h = int(min(h, req - done))
                if h > 0:
                    pieces = [h] if h <= 4 or rng.uniform() < 0.4 else [h - h // 2, h // 2]
                    for pc in pieces:
                        day = m0 + TD(int(rng.integers(0, (me - m0).days + 1)))
                        if day <= min(end, W.CUT):
                            shifts.append((day, pc))
                            done += pc
            m0 = W.add_months(m0, 1)
        # restitution: theft and damage cases, most of them, round monthly instalments
        pays = []
        cls = c.charges[0][1]
        if cls in ("A", "B") and rng.uniform() < 0.74:
            owed = 25 * int(rng.integers(4, 61))
            inst = int(rng.choice([25, 40, 50, 75, 100]))
            paid = 0
            m0 = c.term_start
            while m0 <= min(end, W.CUT) and paid < owed:
                me = W.month_end(m0)
                if rng.uniform() < 0.85:
                    amt = min(inst, owed - paid)
                    day = m0 + TD(int(rng.integers(0, (me - m0).days + 1)))
                    if day <= min(end, W.CUT):
                        pays.append((day, amt))
                        paid += amt
                m0 = W.add_months(m0, 1)
        parts.append(dict(case=c, site=site, req=req, exit_type=exit_type, end=end, shifts=shifts, pays=pays,
                          ref=court_ref_variant(c.number_legacy, rng) if c.number_legacy else c.number_cms,
                          name="%s %s" % (c.defendant["first"], c.defendant["last"])))
    parts.sort(key=lambda p: (p["case"].agree, p["case"].cid))
    ids = rng_for(11)
    n = 1000
    for p in parts:
        n += 1 + int(ids.choice([0, 0, 0, 1, 1, 2, 3]))   # the provider numbers its other programs' clients too
        p["client_no"] = "C%04d" % n
    # the new system took the open caseload in client-number order on 16 January, then numbers new intakes
    m = 0
    for p in parts:
        m += 1 + int(ids.choice([0, 1, 1, 2, 3, 4, 6, 9, 13]))   # the new system numbers every program's intakes
        p["pid_new"] = "P26%05d" % m
    return parts


def report_months():
    """(label, first day, last day, system) for every monthly report, July 2025 to August 2026."""
    out = []
    m = D(2025, 7, 1)
    while m <= D(2026, 8, 1):
        me = W.month_end(m)
        if m.year == 2026 and m.month == 1:
            out.append(("January 2026", m, D(2026, 1, 15), "old"))
            out.append(("January 2026", D(2026, 1, 16), me, "new"))
        else:
            out.append((m.strftime("%B %Y"), m, me, "old" if m < D(2026, 1, 1) else "new"))
        m = W.add_months(m, 1)
    return out


def report_rows(parts, start, end, system):
    rows = []
    for p in parts:
        c = p["case"]
        if c.term_start > end or p["end"] < start:
            continue
        if system == "old" and p["end"] < start:
            continue
        exited = p["end"] <= end and (c.path == "terminated" or p["end"] <= end)
        status = "Active"
        exit_date = exit_txt = ""
        if c.path == "terminated" and c.term_date <= end:
            status = "Terminated"
            exit_date = c.term_date
            exit_txt = {"new arrest": "Unsuccessful - new arrest", "non-compliance": "Unsuccessful - non-compliance",
                        "final review": "Unsuccessful - conditions not met at final review"}[p["exit_type"]]
        elif c.path == "completed" and c.term_end <= end:
            status = "Completed"
            exit_date = c.term_end
            exit_txt = "Successful completion"
        hrs = sum(h for d, h in p["shifts"] if start <= d <= end)
        cum = sum(h for d, h in p["shifts"] if d <= end)
        pay = sum(a for d, a in p["pays"] if start <= d <= end)
        rows.append(dict(p=p, status=status, exit_date=exit_date, exit_txt=exit_txt, hrs=hrs, cum=cum, pay=pay))
    return rows


# ---------------------------------------------------------------------------------------------------------


def build_all():
    main_rows = W.draw_main(MAIN_SEED)
    cases = build_cases(main_rows)
    legacy_ev, cms_ev = build_events(cases)
    legacy_ch, cms_ch = build_charges(cases)
    ros = roster(cases)
    parts = build_participants(cases)
    return dict(main_rows=main_rows, cases=cases, legacy_ev=legacy_ev, cms_ev=cms_ev, legacy_ch=legacy_ch,
                cms_ch=cms_ch, roster=ros, parts=parts)


if __name__ == "__main__":
    import time
    t = time.time()
    A = build_all()
    print("cases", len(A["cases"]), "lottery", sum(c.lottery for c in A["cases"]))
    print("legacy events", len(A["legacy_ev"]), "cms events", len(A["cms_ev"]))
    print("legacy charges", len(A["legacy_ch"]), "cms charges", len(A["cms_ch"]))
    print("participants", len(A["parts"]))
    fy = [c for c in A["cases"] if W.FY_START <= c.filed <= W.FY_END and c.charges[0][1]]
    from collections import Counter
    print("FY26 eligible filings", len(fy), Counter(c.charges[0][1] for c in fy), Counter(c.division for c in fy))
    print("seconds", round(time.time() - t, 1))
