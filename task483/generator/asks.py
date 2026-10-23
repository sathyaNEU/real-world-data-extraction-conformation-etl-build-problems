"""task483's people and the records the two asks read.

People. Every student the pack names carries a state student ID (SSID, ten digits) and the ID of the student system
of the campus that served them: the older system at Fennimore and Ridgefield (seven-digit numbers), the newer one at
Copper Flats and Antelope Springs (LB and six digits). Career Training Grant participants carry a participant ID per
enrollment.

Ask A, the grant tuition. The college bills the board for each section's grant participants on the section's census
day (its eleventh day): a tuition line per participant and one materials and testing fee line per section. A
participant who leaves after the census day before the section's midpoint is refunded half the tuition, credited on
the campus's next invoice. From January 2025 the college's new billing office sends one invoice per campus per month,
covering every section whose census day fell in that month. The board pays each invoice in one payment. Its payment
system until December 2024 kept one row per payment under the invoice's program; the system that replaced it from
January 2025 exports one row per invoice line, and carries a section's fee on every participant's line of it.

Ask B, the federal loans. The college's aid office exports every Direct Loan disbursement it made since 2019-20 by
SSID. The aid system that went live on 1 July 2023 writes a disbursement's amount net of the origination fee; the one
before it wrote the gross amount. A borrower's principal is the gross amount of every disbursement they kept.
"""
import datetime as dt

import numpy as np

import world as W

D = dt.date
TD = dt.timedelta
FY25 = (D(2024, 7, 1), D(2025, 6, 30))
BILL_SWITCH = D(2025, 1, 1)          # consolidated monthly invoices from this invoice date
PAY_SWITCH = D(2025, 1, 1)           # the board's line-level payment export for payments from this date
AID_SWITCH = D(2023, 7, 1)           # the aid system that writes net disbursements
LOAN_VARIANT = 10                    # the loan draw's seed variant, set by tuning
FEE = 0.01057                        # Direct Loan origination fee, loans first disbursed from 1 October 2020
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


def section_id(code, campus, end):
    return "%s%s%s" % (code, campus, end.strftime("%y%m%d"))


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
    return dict(participants=parts, degree=degree, short_extra=extra)


# ---------------------------------------------------------------------------------------------------------------------
# ask A: invoices and the board's payments
def _business(d):
    while d.weekday() >= 5:
        d += TD(days=1)
    return d


def _month_end(d):
    n = D(d.year + (d.month == 12), 1 if d.month == 12 else d.month + 1, 1) - TD(days=1)
    while n.weekday() >= 5:
        n -= TD(days=1)
    return n


def invoices(P):
    """the college's invoice register: [dict(invoice, date, campus, lines=[dict(section_id, code, pid, kind, amount)])]"""
    r = np.random.default_rng(W.SEED * 31 + 13)
    by_sec = {}
    for p in P["participants"]:
        by_sec.setdefault((p["code"], p["campus"], p["section"]), []).append(p)
    secs = []
    for (code, camp, (s, e)), ps in by_sec.items():
        census = s + TD(days=10)
        billed = [p for p in ps if not (p["left"] and p["exit_day"] < census)]
        secs.append(dict(code=code, campus=camp, start=s, end=e, census=census, billed=billed,
                         section_id=section_id(code, camp, e)))
    # refunds: left after census and before the midpoint, half the tuition
    credits = []
    for sc in secs:
        mid = sc["start"] + (sc["end"] - sc["start"]) / 2
        for p in sc["billed"]:
            if p["left"] and p["exit_day"] < mid:
                credits.append(dict(campus=sc["campus"], day=p["exit_day"], section_id=sc["section_id"],
                                    code=sc["code"], pid=p["pid"], amount=-round(TUITION[sc["code"]][0] / 2.0, 2)))
    out = []
    seq = {"A": 4100, "B": 5200, "C": 6300, "D": 7400}

    def number(camp, day):
        seq[camp] += 1
        return "LB%s-%s-%04d" % (camp, day.strftime("%y%m"), seq[camp])
    # per-section invoices on the census day before the switch; monthly campus invoices after
    sec_inv = sorted((sc for sc in secs if sc["census"] < BILL_SWITCH), key=lambda sc: (sc["census"], sc["section_id"]))
    month_inv = {}
    for sc in secs:
        if sc["census"] >= BILL_SWITCH:
            month_inv.setdefault((sc["campus"], _month_end(sc["census"])), []).append(sc)
    events = [(sc["census"], sc["campus"], "sec", sc) for sc in sec_inv]
    events += [(day, camp, "month", scs) for (camp, day), scs in month_inv.items()]
    events.sort(key=lambda t: (t[0], t[1], t[2]))
    pending = sorted(credits, key=lambda c: (c["day"], c["pid"]))
    for day, camp, kind, obj in events:
        scs = [obj] if kind == "sec" else sorted(obj, key=lambda sc: (sc["code"], sc["section_id"]))
        lines = []
        for sc in scs:
            for p in sorted(sc["billed"], key=lambda p: p["pid"]):
                lines.append(dict(section_id=sc["section_id"], code=sc["code"], true_code=sc["code"], pid=p["pid"],
                                  kind="tuition", amount=float(TUITION[sc["code"]][0])))
            lines.append(dict(section_id=sc["section_id"], code=sc["code"], true_code=sc["code"], pid="", kind="fee",
                              amount=float(TUITION[sc["code"]][1])))
        take = [c for c in pending if c["campus"] == camp and c["day"] < day]
        for c in take:
            pending.remove(c)
            # the old billing process wrote a credit under the section of the invoice that carried it; the monthly
            # invoices name the section the credit refunds
            sid, code = (obj["section_id"], obj["code"]) if kind == "sec" else (c["section_id"], c["code"])
            lines.append(dict(section_id=sid, code=code, true_code=c["code"], true_section=c["section_id"], pid=c["pid"],
                              kind="credit", amount=c["amount"], left=c["day"]))
        out.append(dict(invoice=number(camp, day), date=day, campus=camp, lines=lines,
                        program=max(sorted({l["code"] for l in lines if l["kind"] != "credit"}),
                                    key=lambda c: sum(l["amount"] for l in lines if l["code"] == c and l["kind"] != "credit"))))
    # the board's payments: 18 to 40 days after the invoice, posted the same day to two business days later, payments
    # in the last days of June posted in July
    for inv in out:
        pay = _business(inv["date"] + TD(days=int(r.integers(18, 41))))
        lag = int(r.integers(0, 3))
        post = pay + TD(days=lag)
        if pay.month == 6 and pay.day >= 25:
            post = _business(D(pay.year, 7, 1) + TD(days=lag))
        inv["paid"] = pay
        inv["posted"] = _business(post)
        inv["payment_id"] = "PMT%07d" % int(r.integers(1000000, 9999999))
    return out


def ledger_rows(invs):
    """the board's payment rows for Larkspur as its two systems export them: one row per payment under the invoice's
    program until December 2024, one row per invoice line from January 2025 with the section's fee on every
    participant's line"""
    rows = []
    for inv in invs:
        if inv["paid"] < PAY_SWITCH:
            rows.append(dict(payment_id=inv["payment_id"], paid=inv["paid"], posted=inv["posted"], invoice=inv["invoice"],
                             program=inv["program"], pid="", tuition=None, fees=None, credits=None,
                             amount=round(sum(l["amount"] for l in inv["lines"]), 2)))
            continue
        fee = {l["section_id"]: l["amount"] for l in inv["lines"] if l["kind"] == "fee"}
        for l in inv["lines"]:
            if l["kind"] == "fee":
                continue
            if l["kind"] == "tuition":
                t, f, c = l["amount"], fee[l["section_id"]], 0.0
            else:
                t, f, c = 0.0, 0.0, l["amount"]
            rows.append(dict(payment_id=inv["payment_id"], paid=inv["paid"], posted=inv["posted"], invoice=inv["invoice"],
                             program=l["true_code"], pid=l["pid"], tuition=t, fees=f, credits=c, amount=round(t + f + c, 2)))
    return rows


def ask_a(invs, basis="golden"):
    """each short-term program's net grant tuition paid in fiscal 2025, whole dollars.
    golden: the invoice lines of every payment made in the fiscal year, each line to its own section's program and
    each credit to the program of the participant it refunds. ledger: the board's rows as exported, by their program;
    ledger_posted: the same by posting date. register: the invoice lines by the section each is written under.
    posted: the golden by posting date. invoice_date: by invoice date. no_credits: the golden without the credits"""
    out = {c: 0.0 for c in W.SHORT}
    inside = lambda d: FY25[0] <= d <= FY25[1]
    if basis in ("ledger", "ledger_posted"):
        for row in ledger_rows(invs):
            d = row["posted"] if basis == "ledger_posted" else row["paid"]
            if inside(d):
                out[row["program"]] += row["amount"]
        return {c: int(np.floor(v + 0.5)) for c, v in out.items()}
    for inv in invs:
        d = inv["posted"] if basis == "posted" else inv["date"] if basis == "invoice_date" else inv["paid"]
        if not inside(d):
            continue
        for l in inv["lines"]:
            if basis == "no_credits" and l["kind"] == "credit":
                continue
            out[l["code"] if basis == "register" else l["true_code"]] += l["amount"]
    return {c: int(np.floor(v + 0.5)) for c, v in out.items()}


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
    college's other borrowers, amount as the aid system of the day wrote it"""
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
                    sub = int(round(sub * r.uniform(0.45, 0.95), -1))
                    uns = int(round(uns * r.uniform(0.3, 0.9), -1)) if r.random() < 0.7 else 0
                plans += [("Sub", sub), ("Unsub", uns)]
            if (not indep and r.random() < 0.06) or plus_only:
                plans.append(("PLUS", int(round(r.uniform(2000, 6000), -2))))
            for typ, g in plans:
                if g <= 0:
                    continue
                lid = ids.draw("DL%09d", 100000000, 999999999)
                parts = _split(g) if len(dates) == 2 else [int(g // 2)]
                for no, (dd, gg) in enumerate(zip(dates, parts), 1):
                    net = round(gg - round(gg * FEE, 2), 2) if dd >= AID_SWITCH else float(gg)
                    rows.append(dict(ssid=ssid, ay=AY(y), type=typ, loan_id=lid, no=no, date=dd, gross=float(gg),
                                     amount=net, status="Disbursed"))
                    if r.random() < 0.025:
                        back = dd + TD(days=int(r.integers(14, 110)))
                        rows.append(dict(ssid=ssid, ay=AY(y), type=typ, loan_id=lid, no=no, date=back, gross=-float(gg),
                                         amount=-net, status="Returned"))
    for c in P["degree"]:
        u = r.random()
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
    and the median principal they borrowed, to the nearest 10 dollars.
    golden: each disbursement's gross amount (the aid system's net amounts from July 2023 grossed up), returns netted,
    parent PLUS loans left out. net: the amounts as exported. disbursed_only: returned rows dropped. with_plus: the
    parent loans kept"""
    per = {}
    for x in rows:
        if x["type"] == "PLUS" and basis != "with_plus":
            continue
        if basis == "disbursed_only" and x["status"] != "Disbursed":
            continue
        if basis == "net":
            v = x["amount"]
        else:
            v = x["amount"] if x["date"] < AID_SWITCH else round(x["amount"] / (1 - FEE))
        per[x["ssid"]] = per.get(x["ssid"], 0.0) + v
    out = {}
    for code in W.DEGREE:
        vals = sorted(per[c["ssid"]] for c in P["degree"] if c["code"] == code and per.get(c["ssid"], 0) > 0.005)
        med = float(np.median(vals)) if vals else 0.0
        out[code] = (len(vals), int(np.floor(med / 10.0 + 0.5)) * 10, med)
    return out
