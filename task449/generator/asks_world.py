"""The Employer Services referral pipeline behind the asks: referrals to managed vacancies on both platforms, the
clients' job reports (consultant follow-ups and portal self-reports) and the Records of Employment received for
Workshore clients. Every record is cut from one truth per placement (start, length of the job) drawn here.

Reads the world (employers, postings, Employer Services cases) and writes four files to target/; returns the truth
the checks compare the target-only analysis against.
"""
import datetime as dt
import math
import os

import numpy as np

import common as C
import params as P
import world as W

REF_FROM = dt.date(2025, 4, 1)
GO_LIVE = P.MIGRATION
NOTICE = [(0, 0.10), (3, 0.08), (7, 0.30), (10, 0.10), (14, 0.30), (21, 0.12)]
NON_HIRE_RATE = {"Filled - Workshore referral": 1.6, "Filled - other source": 0.9, "Withdrawn by employer": 0.6,
                 "Open": 0.8}
NO_SHOW = 0.065
DELAY_SHARE = 0.22
ROE_SHARE = 0.85
END_REPORT_SHARE = 0.55
AMEND_SHARE = 0.07
BOUNDARY_GAP = 3            # no job ends within this many days of the 90-day mark (any convention gives one count)
SCHED_A = {o[0] for o in P.OCCUPATIONS}

REASONS = [("A", "Shortage of work / End of contract or season"), ("B", "Strike or lockout"),
           ("D", "Illness or injury"), ("E", "Quit"), ("F", "Maternity"), ("G", "Retirement"),
           ("H", "Work-Sharing"), ("J", "Apprentice training"), ("K", "Other"), ("M", "Dismissal or suspension"),
           ("N", "Leave of absence"), ("P", "Parental"), ("Z", "Compassionate Care/Family Caregiver")]


def _pick(rng, pairs):
    v = np.array([p for p, _ in pairs])
    w = np.array([q for _, q in pairs], dtype=float)
    return v[int(np.searchsorted(np.cumsum(w / w.sum()), rng.random()))]


class Ids:
    def __init__(self, rng):
        self.rng = rng
        self.used = set()

    def make(self, fmt, lo, hi):
        while True:
            x = fmt % int(self.rng.integers(lo, hi))
            if x not in self.used:
                self.used.add(x)
                return x


def typed_name(e, rng):
    """An employer's name as a client types it in the portal: the operating or legal name, in their own casing."""
    base = e["legal_name"] if (rng.random() < 0.25 and not e["legal_name"][0].isdigit()) else e["operating_name"]
    r = rng.random()
    if r < 0.58:
        s = base
    elif r < 0.80:
        s = base.lower()
    elif r < 0.86:
        s = base.upper()
    elif r < 0.94:
        s = " ".join(w.capitalize() for w in base.split(" "))
    else:
        s = base.replace(" ", "  ", 1) + " "
    return s


def simulate_asks(emps, posts, cases, rng):
    ext = W.d2i(P.EXTRACT)
    lo = W.d2i(REF_FROM)
    gl = W.d2i(GO_LIVE)
    emp_by_no = {e["employer_no"]: e for e in emps}
    ids = Ids(rng)
    n_clients = 15500
    clients = [ids.make("%08d", 30000000, 49999999) for _ in range(n_clients)]
    hired_windows = {}           # client -> list of (start_day) of placements, to keep one placement per client a quarter
    referrals = []               # dicts
    placements = []
    for (opened, cn, ref, en, occ, npos, outcome, od, p) in cases:
        a = max(p["start"], lo)
        b = min(p["listing_end"] - 1, ext)
        if b < a:
            continue
        n_h = 0
        if outcome == "Filled - Workshore referral":
            n_h = 1 if npos == 1 else 1 + int(rng.binomial(npos - 1, 0.55))
        n_o = int(rng.poisson(NON_HIRE_RATE[outcome]))
        odi = W.d2i(od) if od is not None else None
        if n_h and (odi is None or odi - 1 < a):
            n_h = 0
        used = set()

        def client_for(span=None):
            """A client not already referred to this case; for a hire, one with no other placement job within 30 days
            of this one's span (no client holds two placements at once)."""
            for _ in range(200):
                c = clients[int(rng.integers(n_clients))]
                if c in used:
                    continue
                if span is not None:
                    a0, b0 = span
                    if any(a0 - 30 <= y and x <= b0 + 30 for x, y in hired_windows.get(c, [])):
                        continue
                used.add(c)
                return c
            raise AssertionError("client pool exhausted")

        # hires: the last on the outcome day, the others between the first referral and it
        hire_days = []
        if n_h:
            hire_days = sorted([odi] + [int(rng.integers(a + 1, odi + 1)) for _ in range(n_h - 1)])
        for hd in hire_days:
            ref_day = int(rng.integers(a, max(a + 1, hd)))
            ref_day = min(ref_day, hd - 1) if hd - 1 >= a else a
            planned = hd + int(_pick(rng, NOTICE))
            show = rng.random() >= NO_SHOW
            if show:
                delay = int(rng.integers(1, 29)) if rng.random() < DELAY_SHARE else 0
                start = planned + delay
                while True:
                    L = int(math.ceil(rng.weibull(0.8) * 400.0))
                    if abs(L - 90) > BOUNDARY_GAP and abs(L - 91) > BOUNDARY_GAP:
                        break
                span = (start, start + L)
            else:
                start, L = None, None
                span = (planned, planned)
            c = client_for(span)
            hired_windows.setdefault(c, []).append(span)
            pl = {"client": c, "case": cn, "post": p, "employer_no": en, "occ": occ, "ref_day": ref_day,
                  "hire_day": hd, "planned": planned, "start": start, "L": L, "show": show}
            placements.append(pl)
            referrals.append({"client": c, "post": p, "ref_day": ref_day, "status": "Hired", "status_day": hd,
                              "planned": planned, "pl": pl})
        for _ in range(n_o):
            ref_day = int(rng.integers(a, b + 1))
            c = client_for()
            if outcome == "Withdrawn by employer" and rng.random() < 0.7:
                st = "Vacancy withdrawn"
                sd = odi if odi is not None else ref_day + 10
            else:
                st = _pick(rng, [("Not selected", 0.62), ("Declined by client", 0.17), ("No response", 0.21)])
                sd = ref_day + int(rng.integers(3, 31))
                if odi is not None:
                    sd = min(sd, odi)
            sd = max(sd, ref_day)
            if sd > ext:
                st, sd = "Referred", None
            referrals.append({"client": c, "post": p, "ref_day": ref_day, "status": str(st), "status_day": sd,
                              "planned": None, "pl": None})
    return clients, referrals, placements



def write_referrals(referrals, rng, tgt):
    ext = W.d2i(P.EXTRACT)
    gl = W.d2i(GO_LIVE)
    ids = Ids(rng)
    old_rows, new_rows = [], []
    for r in sorted(referrals, key=lambda r: (r["ref_day"], r["client"])):
        p = r["post"]
        if r["ref_day"] < gl:
            pending_at_close = r["status_day"] is None or r["status_day"] >= gl
            rno = ids.make("R%07d", 1000000, 9999999)
            if pending_at_close:
                old_rows.append([rno, p["old_no"], r["client"], W.i2d(r["ref_day"]), "Referred", None, None])
                # carried to the new platform at go-live: a new record, created on go-live day, for the same referral
                new_rows.append((gl, r, p["new_id"]))
                r["carried"] = True
            else:
                old_rows.append([rno, p["old_no"], r["client"], W.i2d(r["ref_day"]), r["status"],
                                 W.i2d(r["status_day"]),
                                 W.i2d(r["planned"]) if r["status"] == "Hired" else None])
                r["carried"] = False
        else:
            new_rows.append((r["ref_day"], r, p["new_id"]))
            r["carried"] = False
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Referrals"
    ws.append(["Referral no.", "Posting no.", "Client no.", "Referred", "Status", "Status date", "Start date"])
    for c in ws[1]:
        c.font = Font(bold=True)
    rix = 1
    for row in old_rows:
        ws.append(row)
        rix += 1
        for col in (4, 6, 7):
            if ws.cell(row=rix, column=col).value is not None:
                ws.cell(row=rix, column=col).number_format = "dd/mm/yyyy"
    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 12
    ws.column_dimensions["E"].width = 18
    C.save_workbook(wb, os.path.join(tgt, "workshore_referrals_2025-04-01_2026-02-01.xlsx"),
                    dt.datetime(2026, 2, 1, 23, 40), "Workshore")
    out = []
    for day, r, jid in sorted(new_rows, key=lambda t: (t[0], t[1]["client"], t[2])):
        rid = ids.make("RF%09d", 100000000, 999999999)
        st = r["status"]
        sd = r["status_day"]
        out.append([rid, jid, r["client"], W.i2d(day).isoformat(), st, W.i2d(sd).isoformat() if sd is not None else "",
                    W.i2d(r["planned"]).isoformat() if st == "Hired" else ""])
    C.write_csv(os.path.join(tgt, "workshore_referrals_2026-02-02_2026-11-14.csv"),
                ["referral_id", "job_id", "client_id", "referred_on", "status", "status_date", "expected_start"], out,
                crlf=False)
    return len(old_rows), len(out)


def write_job_reports(placements, clients, emps, rng, tgt):
    """Job start and end reports: consultant follow-ups (employer number) and client portal reports (employer name
    as typed); a consultant records a hire that did not start. At a multi-site employer a report may name the
    location's own account (its number, or its name as the client types it)."""
    import pack
    ext = W.d2i(P.EXTRACT)
    lo = W.d2i(REF_FROM)
    emp_by_no = {e["employer_no"]: e for e in emps}
    sib = {}
    for a in pack.sibling_accounts(emps):
        sib.setdefault(a["parent_no"], []).append(a)

    def ident(pl, ch):
        """The account a report names for a placement: the posting's, or the location's sibling account."""
        e = emp_by_no[pl["employer_no"]]
        alt = sib.get(pl["employer_no"])
        if alt and pl.setdefault("at_sibling", rng.random() < 0.6):
            a = alt[0]
            if ch == "consultant":
                return a["employer_no"], None
            return None, (a["operating_name"] if rng.random() < 0.8 else a["operating_name"].lower())
        if ch == "consultant":
            return pl["employer_no"], None
        return None, typed_name(e, rng)

    recs = []
    for pl in placements:
        e = emp_by_no[pl["employer_no"]]
        if not pl["show"]:
            rd = pl["planned"] + int(rng.integers(3, 21))
            if rd <= ext:
                recs.append((rd, {"client": pl["client"], "source": "consultant", "event": "did_not_start",
                                  "employer_no": pl["employer_no"], "date": W.i2d(pl["planned"]).isoformat()}))
                pl["dns_reported"] = True
            else:
                pl["dns_reported"] = False
            continue
        s = pl["start"]
        r = rng.random()
        chans = ["consultant"] if r < 0.45 else (["portal"] if r < 0.75 else ["consultant", "portal"])
        pl["start_channels"] = chans
        for ch in chans:
            rd = s + (int(rng.integers(20, 41)) if ch == "consultant" else int(rng.integers(0, 15)))
            if rd > ext:
                rd = ext
            rec = {"client": pl["client"], "source": ch, "event": "job_start", "date": W.i2d(s).isoformat()}
            num, name = ident(pl, ch)
            if num is not None:
                rec["employer_no"] = num
            else:
                rec["employer_name"] = name
            recs.append((max(rd, s), rec))
        last = s + pl["L"] - 1
        pl["last"] = last
        if last < ext:
            has_roe = rng.random() < ROE_SHARE
            has_rep = rng.random() < END_REPORT_SHARE
            if not has_roe and not has_rep:
                if rng.random() < 0.5:
                    has_roe = True
                else:
                    has_rep = True
            pl["roe"] = has_roe
            pl["end_report"] = has_rep
            if has_rep:
                rd = min(ext, last + int(rng.integers(0, 31)))
                ch = "consultant" if rng.random() < 0.5 else "portal"
                rec = {"client": pl["client"], "source": ch, "event": "job_end", "date": W.i2d(last).isoformat()}
                num, name = ident(pl, ch)
                if num is not None:
                    rec["employer_no"] = num
                else:
                    rec["employer_name"] = name
                recs.append((rd, rec))
                pl["end_channel"] = ch
        else:
            pl["roe"] = False
            pl["end_report"] = False
    # jobs clients found on their own: starts and ends at other employers, reported the same two ways
    def nn(x):
        return " ".join(str(x).split()).casefold()

    placed_names = {}
    for pl in placements:
        pe = emp_by_no[pl["employer_no"]]
        nm = {nn(pe["operating_name"]), nn(pe["legal_name"])}
        for a in sib.get(pl["employer_no"], []):
            nm |= {nn(a["operating_name"]), nn(a["legal_name"])}
        placed_names.setdefault(pl["client"], set()).update(nm)
    own = []
    for k in range(5200):
        c = clients[int(rng.integers(len(clients)))]
        s = int(rng.integers(lo - 30, ext - 5))
        L = int(math.ceil(rng.weibull(0.8) * 300.0))
        if rng.random() < 0.55:
            e = emps[int(rng.integers(len(emps)))]
            if {nn(e["operating_name"]), nn(e["legal_name"])} & placed_names.get(c, set()):
                continue        # a client's own job is never with an employer named like one that hired them
            enum, ename = e["employer_no"], typed_name(e, rng)
        else:
            e = None
            enum = None
            ename = _outside_employer_name(rng)
        own.append((c, s, L, enum, ename, e))
        if s >= lo:
            ch = "portal" if (enum is None or rng.random() < 0.7) else "consultant"
            rec = {"client": c, "source": ch, "event": "job_start", "date": W.i2d(s).isoformat()}
            if ch == "consultant":
                rec["employer_no"] = enum
            else:
                rec["employer_name"] = ename
            recs.append((min(ext, s + int(rng.integers(0, 20))), rec))
        if s + L - 1 < ext and rng.random() < 0.5 and s + L - 1 >= lo:
            ch = "portal" if (enum is None or rng.random() < 0.7) else "consultant"
            rec = {"client": c, "source": ch, "event": "job_end", "date": W.i2d(s + L - 1).isoformat()}
            if ch == "consultant":
                rec["employer_no"] = enum
            else:
                rec["employer_name"] = ename
            recs.append((min(ext, s + L - 1 + int(rng.integers(0, 25))), rec))
    recs.sort(key=lambda t: (t[0], t[1]["client"], t[1]["event"], t[1]["date"]))
    out = []
    for rd, rec in recs:
        o = {"client_no": rec["client"], "reported_on": W.i2d(rd).isoformat(), "source": rec["source"],
             "event": rec["event"]}
        if "employer_no" in rec:
            o["employer_no"] = rec["employer_no"]
        else:
            o["employer_name"] = rec["employer_name"]
        o["date"] = rec["date"]
        out.append(o)
    C.write_jsonl(os.path.join(tgt, "workshore_client_job_reports_2025-04_2026-11.jsonl"), out)
    return own


OUTSIDE_NOUNS = ["Security", "Moving & Storage", "Courier Services", "Car Wash", "Laundromat", "Gas Bar",
                 "Tire & Lube", "Florist", "Pet Grooming", "Print Shop", "Landscaping", "Painting", "Roofing",
                 "Daycare", "Dental Office", "Vet Clinic", "Liquor Store", "Bowling Lanes"]


def _outside_employer_name(rng):
    n = "%s %s" % (W.FIRST_WORDS[int(rng.integers(len(W.FIRST_WORDS)))],
                   OUTSIDE_NOUNS[int(rng.integers(len(OUTSIDE_NOUNS)))])
    return n if rng.random() < 0.7 else n.lower()


def write_roes(placements, own, clients, emps, rng, tgt):
    """Records of Employment received for Workshore clients: one per interruption of earnings, amended ROEs
    replacing earlier ones."""
    ext = W.d2i(P.EXTRACT)
    lo = W.d2i(REF_FROM)
    ids = Ids(rng)
    emp_by_no = {e["employer_no"]: e for e in emps}
    rp2 = {e["employer_no"] for e in emps if rng.random() < 0.10}
    acct_bn = {e["bn9"] for e in emps}
    rows = []

    def bn15(e, alt=False):
        return e["bn9"] + ("RP0002" if (alt and e["employer_no"] in rp2) else "RP0001")

    def add(client, bn, first, last, reason, truth_amend=None):
        """One ROE; with truth_amend=(orig_last, orig_reason) an earlier wrong ROE is issued first and amended."""
        iss = last + int(rng.integers(1, 17))
        if truth_amend is not None:
            o_last, o_reason = truth_amend
            o_iss = o_last + int(rng.integers(1, 12))
            s1 = ids.make("W%08d", 10000000, 99999999)
            rows.append((o_iss, [s1, "", client, bn, W.i2d(first), W.i2d(o_last), o_reason, W.i2d(o_iss)]))
            iss2 = max(o_iss, iss) + int(rng.integers(5, 45))
            s2 = ids.make("W%08d", 10000000, 99999999)
            rows.append((iss2, [s2, s1, client, bn, W.i2d(first), W.i2d(last), reason, W.i2d(iss2)]))
        else:
            s1 = ids.make("W%08d", 10000000, 99999999)
            rows.append((iss, [s1, "", client, bn, W.i2d(first), W.i2d(last), reason, W.i2d(iss)]))

    for pl in placements:
        if not pl["show"] or not pl.get("roe"):
            continue
        e = emp_by_no[pl["employer_no"]]
        reason = _pick(rng, [("E", 0.46), ("A", 0.30), ("M", 0.17), ("K", 0.07)])
        s, last = pl["start"], pl["last"]
        amend = None
        if rng.random() < AMEND_SHARE and last + 80 < ext:
            # the first ROE carried a wrong last day for which paid; the amendment corrects it
            while True:
                d = int(rng.integers(3, 41)) * (1 if rng.random() < 0.5 else -1)
                o_last = last + d
                if o_last >= s and abs(o_last - (s + 89)) > BOUNDARY_GAP and abs(o_last - (s + 90)) > BOUNDARY_GAP:
                    break
            amend = (o_last, reason)
        pl["roe_amended"] = amend is not None
        add(pl["client"], bn15(e, True), s, last, str(reason), amend)
    # earlier jobs with the same employers (seasonal returns) and with others, and the jobs clients found themselves
    placed = [pl for pl in placements if pl["show"]]
    for pl in placed:
        if rng.random() < 0.03:
            e = emp_by_no[pl["employer_no"]]
            last = pl["start"] - int(rng.integers(120, 300))
            first = last - int(rng.integers(60, 200))
            if last >= lo - 10:
                add(pl["client"], bn15(e), first, last, "A")
    for (c, s, L, enum, ename, e) in own:
        last = s + L - 1
        if last >= ext or last < lo - 15 or rng.random() > 0.8:
            continue
        if e is not None:
            bn = bn15(e)
        else:
            while True:
                b9 = "%09d" % int(rng.integers(100000000, 999999999))
                if b9 not in acct_bn:
                    break
            bn = b9 + "RP0001"
        add(c, bn, s, last, str(_pick(rng, [(k, w) for k, w in zip("ADEFGKMNP", [0.34, 0.05, 0.27, 0.04, 0.02,
                                                                                    0.05, 0.12, 0.06, 0.05])])))
    for k in range(4200):
        c = clients[int(rng.integers(len(clients)))]
        last = int(rng.integers(lo - 15, ext - 20))
        first = last - int(math.ceil(rng.weibull(0.9) * 500.0))
        while True:
            b9 = "%09d" % int(rng.integers(100000000, 999999999))
            if b9 not in acct_bn:
                break
        bn = "%sRP%04d" % (b9, int(rng.choice([1, 1, 1, 2, 3])))
        add(c, bn, first, last, str(_pick(rng, [(k2, w) for k2, w in zip("ADEFGKMNPZ", [0.38, 0.05, 0.25, 0.04, 0.03,
                                                                                         0.05, 0.11, 0.04, 0.04,
                                                                                         0.01])])))
    rows = [r for r in rows if r[0] <= ext and r[0] >= lo]
    rows.sort(key=lambda t: (t[0], t[1][0]))
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "ROE"
    ws.append(["Records of Employment received for Workshore clients, 1 April 2025 to 14 November 2026"])
    ws["A1"].font = Font(bold=True)
    ws.append(["Service Canada, ROE Web, provincial data share (Laurentide)"])
    ws.append([])
    hdr = ["Serial no.", "Amended serial no.", "Workshore client no.", "Business number (BN15)", "First day worked",
           "Last day for which paid", "Reason for issuing", "Date issued"]
    ws.append(hdr)
    for c in ws[4]:
        c.font = Font(bold=True)
    rix = 4
    for _, r in rows:
        ws.append(r)
        rix += 1
        for col in (5, 6, 8):
            ws.cell(row=rix, column=col).number_format = "yyyy-mm-dd"
    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["D"].width = 20
    ws2 = wb.create_sheet("Reason codes")
    ws2.append(["Code", "Reason for issuing"])
    for c in ws2[1]:
        c.font = Font(bold=True)
    for code, txt in REASONS:
        ws2.append([code, txt])
    ws2.column_dimensions["B"].width = 44
    C.save_workbook(wb, os.path.join(tgt, "roe_received_workshore_clients_2025-04-01_2026-11-14.xlsx"),
                    dt.datetime(2026, 11, 14, 6, 15), "Service Canada")
    return len(rows)


def write_asks(emps, posts, cases, tgt, seed):
    rng = np.random.default_rng(seed)
    clients, referrals, placements = simulate_asks(emps, posts, cases, rng)
    write_referrals(referrals, np.random.default_rng(seed + 1), tgt)
    own = write_job_reports(placements, clients, emps, np.random.default_rng(seed + 2), tgt)
    write_roes(placements, own, clients, emps, np.random.default_rng(seed + 3), tgt)
    return {"referrals": referrals, "placements": placements}
