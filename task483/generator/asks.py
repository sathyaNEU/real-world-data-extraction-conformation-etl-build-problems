"""task483's people and the records the two asks read.

People. Every student the pack names carries a state student ID (SSID, ten digits) and the ID of the student system
of the campus that served them: the older system at Fennimore and Ridgefield (seven-digit numbers), the newer one at
Copper Flats and Antelope Springs (LB and six digits). Career Training Grant participants carry a participant ID per
enrollment, and each section a five-digit course reference number (CRN) in the college's schedule.

Ask A, the clock hours. The college's attendance system records each grant participant's attended time at every
session of their section, from the day they enrolled to the day they left or completed, and exports a session's time as
hours and minutes after a point (7.30 for seven hours and thirty minutes). A section meets on its weekdays, and a
program's clock hours are its sessions times their length. A participant misses a session now and then, and arrives
late or leaves early at some. The export carries the week of 3 March 2025 twice.

Ask B, the federal loans. The college's aid office exports every Direct Loan disbursement it made since 2019-20 by
SSID. The aid system before 1 July 2024 wrote each disbursement's gross amount; the one that went live on 1 July 2024
writes the loan's gross amount for its award year on each of the loan's disbursements. A borrower's principal is the
gross amount of every disbursement they kept.
"""
import datetime as dt

import numpy as np

import world as W

D = dt.date
TD = dt.timedelta
FY25 = (D(2024, 7, 1), D(2025, 6, 30))
AID_SWITCH = D(2024, 7, 1)           # the aid system that writes a loan's amount on each of its disbursements
LOAN_VARIANT = 8                     # the loan draw's seed variant, set by tuning
FEE = 0.01057                        # Direct Loan origination fee (the cost of attendance states it; amounts are gross)
LATE = 0.05                          # share of a section's participants who enroll after its census day
ATT_VARIANT = 17                     # the attendance draw's seed variant, set by tuning
ABSENT, PARTIAL = 0.05, 0.07         # a session missed; a session attended in part (late or early, 15 to 150 minutes)
RESENT = (D(2025, 3, 3), D(2025, 3, 7))          # the week the attendance export carries twice
# sessions per section and minutes per session: their product is the inventory's clock hours
SESSIONS = {"CDL": (20, 480), "CNA": (16, 450), "PHL": (20, 420), "PHT": (40, 450), "EMT": (24, 450),
            "WLF": (40, 480), "MCD": (48, 450), "ITS": (40, 450), "HVC": (32, 450), "WHS": (10, 480), "FRK": (5, 480)}
OLD_SIS, NEW_SIS = ("A", "B"), ("C", "D")

# short-term programs: tuition per participant, materials and testing fee per section, dollars
TUITION = {"CDL": (4950, 1450), "CNA": (1180, 380), "PHL": (1640, 260), "PHT": (2960, 420), "EMT": (1980, 610),
           "WLF": (3640, 880), "MCD": (3380, 150), "ITS": (2890, 300), "HVC": (2580, 540), "WHS": (690, 120),
           "FRK": (390, 90)}
# completers of the short-term programs in 2024-25 who were not grant participants
EXTRA = dict(CDL=8, CNA=14, PHL=3, PHT=5, EMT=6, WLF=6, MCD=4, ITS=8, HVC=4, WHS=12, FRK=2)
# degree programs: share of completers who borrow, years enrolled before the completing year
BORROW = {"RN": .52, "RAD": .48, "WLD": .38, "DSL": .40, "BUS": .44, "ECE": .46, "MA": .50, "IT": .36, "CJ": .42,
          "AUT": .40, "CUL": .45, "PAR": .40}
TERMS = ((D(2024, 8, 2), .10), (D(2024, 12, 13), .22), (D(2025, 5, 9), .68))   # conferral dates in 2024-25


class Ids:
    """unique identifiers drawn from one stream"""

    def __init__(self, seed):
        self.r = np.random.default_rng(seed)
        self.seen = set()

    def draw(self, fmt, lo, hi):
        while True:
            v = fmt % int(self.r.integers(lo, hi))
            if v not in self.seen:
                self.seen.add(v)
                return v

    def ssid(self):
        return self.draw("%010d", 7000000000, 7999999999)

    def sis(self, campus):
        return self.draw("%07d", 1000000, 2999999) if campus in OLD_SIS else self.draw("LB%06d", 100000, 999999)

    def participant(self):
        return self.draw("CTG-%06d", 100000, 999999)


_CRN = {}


def section_id(code, campus, end):
    """the section's course reference number in the college's schedule"""
    if not _CRN:
        ids = Ids(W.SEED * 31 + 23)
        keys = sorted({(e + TD(weeks=k), c, camp) for c in W.SHORT for camp, s, e, per in W.sections(c)
                       for k in (-52, 0, 52)})
        for e, c, camp in keys:
            _CRN[(c, camp, e)] = ids.draw("%05d", 20000, 59999)
    return _CRN[(code, campus, end)]


def late_adds(parts):
    """mark the participants who enrolled after their section's census day, a share of each section of three weeks or
    more: p["late"] is the day they enrolled, or None"""
    r = np.random.default_rng(W.SEED * 31 + 29)
    by_sec = {}
    for p in parts:
        p["late"] = None
        by_sec.setdefault((p["code"], p["campus"], p["section"]), []).append(p)
    for code, camp, (s, e) in sorted(by_sec, key=lambda k: (k[2], k[0], k[1])):
        for p in sorted(by_sec[(code, camp, (s, e))], key=lambda p: p["pid"]):
            cen = s + TD(days=10)
            if (e - s).days >= 17 and (not p["left"] or p["exit_day"] > cen + TD(days=8)) and r.random() < LATE:
                p["late"] = s + TD(days=10 + int(r.integers(1, 5)))


def people():
    """everyone the pack names: the grant participants (one person each), the 2024-25 degree completers and the other
    2024-25 short-term completers. Returns dict(participants, degree, short_extra)"""
    ids = Ids(W.SEED * 31 + 7)
    parts = []
    for code in W.SHORT:
        for p in W.participants(code):
            q = dict(p)
            q["pid"] = ids.participant()
            q["ssid"] = ids.ssid()
            q["sis"] = ids.sis(p["campus"])
            q["section_id"] = section_id(code, p["campus"], p["section"][1])
            parts.append(q)
    r = np.random.default_rng(W.SEED * 31 + 11)
    degree = []
    for code, (name, cip, cip10, award, cells, comp) in W.DEGREE.items():
        for camp in sorted(comp):
            for i in range(comp[camp]):
                u = r.random()
                term = TERMS[0][0] if u < TERMS[0][1] else TERMS[1][0] if u < TERMS[0][1] + TERMS[1][1] else TERMS[2][0]
                degree.append(dict(code=code, campus=camp, ssid=ids.ssid(), sis=ids.sis(camp), conferred=term,
                                   award=award))
    extra = []
    for code, n in EXTRA.items():
        secs = [(camp, s, e) for camp, s, e, per in W.sections(code)]
        for i in range(n):
            camp, s, e = secs[int(r.integers(0, len(secs)))]
            extra.append(dict(code=code, campus=camp, ssid=ids.ssid(), sis=ids.sis(camp), section=(s, e),
                              section_id=section_id(code, camp, e)))
    late_adds(parts)
    return dict(participants=parts, degree=degree, short_extra=extra)


# ---------------------------------------------------------------------------------------------------------------------
# ask A: the attendance export
def _business(d):
    while d.weekday() >= 5:
        d += TD(days=1)
    return d


def sessions(code, start, end):
    """a section's session days (its weekdays, evenly spread) and the minutes of a session"""
    days = [start + TD(days=k) for k in range((end - start).days + 1) if (start + TD(days=k)).weekday() < 5]
    n, mins = SESSIONS[code]
    pick = [int(round(i * (len(days) - 1) / (n - 1))) for i in range(n)] if n > 1 else [0]
    return [days[i] for i in pick], mins


def attendance(P):
    """[dict(pid, code, crn, date, minutes)]: every session each grant participant attended, from the day they enrolled
    (the section's first day, or a late enrollee's day) to the day they left or the section's last day"""
    r = np.random.default_rng(W.SEED * 31 + 43 + 1000 * ATT_VARIANT)
    rows = []
    for p in sorted(P["participants"], key=lambda p: (p["section"][0], p["code"], p["campus"], p["pid"])):
        s, e = p["section"]
        days, mins = sessions(p["code"], s, e)
        first, last = p["late"] or s, p["exit_day"] if p["left"] else e
        for d in days:
            if d < first or d > last:
                continue
            if r.random() < ABSENT:
                continue
            m = mins - (int(r.integers(15, 151)) if r.random() < PARTIAL else 0)
            rows.append(dict(pid=p["pid"], code=p["code"], crn=p["section_id"], date=d, minutes=m))
    return rows


def hmm(minutes):
    """a session's time as the attendance export writes it: hours and minutes after a point"""
    return "%d.%02d" % divmod(minutes, 60)


def ask_a(rows, basis="golden"):
    """each short-term program's clock hours its grant participants attended from July 2024 to June 2025, whole hours:
    {code: (hours, unrounded)}.
    golden: every session dated in the year once, its time read as hours and minutes. decimal: the time read as decimal
    hours. resent: the re-sent week counted twice. decimal_resent: both. by_end: the sessions of the sections that ended
    in the year. completers: the completers' sessions only"""
    out = {c: 0.0 for c in W.SHORT}
    for x in rows:
        if not (FY25[0] <= x["date"] <= FY25[1]):
            continue
        h = float(hmm(x["minutes"])) if basis in ("decimal", "decimal_resent") else x["minutes"] / 60.0
        k = 2 if (basis in ("resent", "decimal_resent") and RESENT[0] <= x["date"] <= RESENT[1]) else 1
        out[x["code"]] += k * h
    return {c: (int(np.floor(v + 0.5)), v) for c, v in out.items()}


# ---------------------------------------------------------------------------------------------------------------------
# ask B: Direct Loans
AY = lambda y: "%d-%02d" % (y, (y + 1) % 100)


def _loan_years(r, award, conferred):
    """the award years (by their first calendar year) a completer borrowed in, ending with the completing year"""
    last = 2024 if conferred >= D(2024, 7, 1) else 2023
    if conferred == D(2024, 8, 2):
        last = 2023
    if award == "C2":
        n = 1 + int(r.random() < 0.5)
    else:
        n = 2 + int(r.random() < 0.35) + int(r.random() < 0.10)
    return [last - k for k in range(n)][::-1]


def _split(g):
    a = int(g // 2)
    return [a, int(g - a)]


def loans(P):
    """[dict(ssid, ay, type, loan_id, no, date, gross, amount, status)] for the 2024-25 degree completers and the
    college's other borrowers: gross is the disbursement's gross amount, amount what the aid system of the day wrote
    (the disbursement's gross before July 2024, the loan's gross for its award year from July 2024)"""
    r = np.random.default_rng(W.SEED * 31 + 17 + 1000 * LOAN_VARIANT)
    ids = Ids(W.SEED * 31 + 19)
    ids.seen |= {p["ssid"] for p in P["participants"]} | {c["ssid"] for c in P["degree"]} | \
        {c["ssid"] for c in P["short_extra"]}
    rows = []

    def borrower(ssid, years, conferred=None, plus_only=False):
        indep = r.random() < 0.40
        for k, y in enumerate(years):
            fall, spring = _business(D(y, 8, 26)), _business(D(y + 1, 1, 13))
            dates = [fall, spring]
            if conferred is not None and conferred == D(2024, 12, 13) and y == 2024:
                dates = [fall]
            plans = []
            if not plus_only:
                sub = 3500 if k == 0 else 4500
                uns = 6000 if indep else 2000
                full = r.random() < 0.6
                if not full:
                    sub = int(round(sub * r.uniform(0.45, 0.95) / 20.0)) * 20
                    uns = int(round(uns * r.uniform(0.3, 0.9) / 20.0)) * 20 if r.random() < 0.7 else 0
                plans += [("Sub", sub), ("Unsub", uns)]
            if (not indep and r.random() < 0.06) or plus_only:
                plans.append(("PLUS", int(round(r.uniform(2000, 6000), -2))))
            for typ, g in plans:
                if g <= 0:
                    continue
                lid = ids.draw("DL%09d", 100000000, 999999999)
                parts = _split(g) if len(dates) == 2 else [int(g // 2)]
                new = dates[0] >= AID_SWITCH
                loan = float(sum(parts))
                for no, (dd, gg) in enumerate(zip(dates, parts), 1):
                    rows.append(dict(ssid=ssid, ay=AY(y), type=typ, loan_id=lid, no=no, date=dd, gross=float(gg),
                                     amount=loan if new else float(gg), status="Disbursed"))
                    if not new and r.random() < 0.025:
                        back = dd + TD(days=int(r.integers(14, 110)))
                        rows.append(dict(ssid=ssid, ay=AY(y), type=typ, loan_id=lid, no=no, date=back, gross=-float(gg),
                                         amount=-float(gg), status="Returned"))
    # who borrows: each program's share, its borrower count made odd by the one completer nearest the line
    dec = np.random.default_rng(W.SEED * 31 + 41 + 1000 * LOAN_VARIANT)
    us = [dec.random() for c in P["degree"]]
    for code in W.DEGREE:
        idx = [i for i, c in enumerate(P["degree"]) if c["code"] == code]
        if sum(us[i] < BORROW[code] for i in idx) % 2 == 0:
            i = min(idx, key=lambda i: abs(us[i] - BORROW[code]))
            us[i] = BORROW[code] + 0.03 if us[i] < BORROW[code] else BORROW[code] - 1e-6
    for c, u in zip(P["degree"], us):
        if u < BORROW[c["code"]]:
            borrower(c["ssid"], _loan_years(r, c["award"], c["conferred"]), c["conferred"])
        elif u < BORROW[c["code"]] + 0.02:
            borrower(c["ssid"], _loan_years(r, c["award"], c["conferred"])[-1:], c["conferred"], plus_only=True)
    for i in range(2300):                         # the college's other borrowers, 2019-20 to 2025-26
        y0 = int(r.integers(2019, 2026))
        yrs = [y for y in range(y0, y0 + 1 + int(r.integers(0, 3))) if y <= 2025]
        borrower(ids.ssid(), yrs)
    rows.sort(key=lambda x: (x["date"], x["ssid"], x["loan_id"], x["no"], x["status"]))
    return rows


def ask_b(P, rows, basis="golden"):
    """each degree program's 2024-25 completers who borrowed Direct Loans (subsidized or unsubsidized) at the college,
    and the median of all the principal they borrowed there, to the nearest 10 dollars: {program: (borrowers, median,
    unrounded)}.
    golden: each disbursement's gross amount before July 2024 (returns netted), each loan's amount once from July
    2024, parent PLUS loans left out. rows: every row's amount as exported. per_loan: one amount per loan in every year.
    dedupe: rows alike in borrower, loan, amount and status kept once. with_plus: the parent loans kept.
    disbursed_only: returned rows dropped. ay2425: the 2024-25 award year alone. gross_up: the golden with every amount
    read as net of the origination fee"""
    per, seen = {}, set()
    for x in rows:
        if x["type"] == "PLUS" and basis != "with_plus":
            continue
        if basis == "disbursed_only" and x["status"] != "Disbursed":
            continue
        if basis == "ay2425" and x["ay"] != "2024-25":
            continue
        if basis == "rows":
            pass
        elif basis == "per_loan":
            if x["status"] == "Disbursed":
                if x["loan_id"] in seen:
                    continue
                seen.add(x["loan_id"])
        elif basis == "dedupe":
            key = (x["ssid"], x["loan_id"], x["amount"], x["status"])
            if key in seen:
                continue
            seen.add(key)
        elif x["date"] >= AID_SWITCH:
            if x["loan_id"] in seen:
                continue
            seen.add(x["loan_id"])
        v = x["amount"]
        if basis == "gross_up":
            v = round(v / (1 - FEE))
        per[x["ssid"]] = per.get(x["ssid"], 0.0) + v
    out = {}
    for code in W.DEGREE:
        vals = sorted(per[c["ssid"]] for c in P["degree"] if c["code"] == code and per.get(c["ssid"], 0) > 0.005)
        med = float(np.median(vals)) if vals else 0.0
        out[code] = (len(vals), int(np.floor(med / 10.0 + 0.5)) * 10, med)
    return out
