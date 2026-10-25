"""task166's data files, written from the clean truth (world.py) in the layouts of the systems that hold them: the legacy
core's home equity loan master, the new core's monthly trial balance, the conversion cross-reference, the lending
system's funded-loan file with each application's senior lien, the credit union's own first-mortgage servicing file, the
county map, the posted rate sheet archive, the HELOC line extract and the county house price index."""
from __future__ import annotations

import datetime as dt
import math
import os

import numpy as np

import common as K
import world as WD

mo, ym = K.mo, K.ym

F_LEGACY = "legacy_he_loans_2019-01_2024-08.csv"
F_CORE = "core_he_trial_balance_2024-09_2026-11.csv"
F_XREF = "core_conversion_xref.csv"
F_LOS = "he_lending_file_2009-2026.csv"
F_SERV = "first_mortgage_servicing_2026-11.csv"
F_MAP = "county_region_map.csv"
F_RATES = "posted_rate_sheets_2018-12_2026-11.csv"
F_HELOC = "heloc_lines_2026-11.csv"
F_HPI = "county_house_price_index_2019q1_2026q3.csv"

SERVICERS = [("GREATBEND MORTGAGE", 0.13, False), ("NATL HOMELOAN SVCG", 0.12, False), ("FERNWICK MTG", 0.11, False),
             ("MARLSTONE HOME LOANS", 0.10, False), ("VELLACOTT MTG SVCS", 0.09, False), ("TOLLMERE HL SERVICING", 0.09, False),
             ("CORRAVEN TRUST MTG", 0.08, False), ("DUNMERE FIRST MTG", 0.08, False), ("BLUESTEM HOME FIN", 0.07, False),
             ("KEELBOAT FED SAVINGS", 0.07, False), ("ELDERMOOR MORTGAGE CO", 0.06, True)]
STREETS = ["Maple", "Oak", "Cherry", "Walnut", "Hickory", "Birch", "Elm", "Cedar", "Pine", "Spruce", "Willow", "Aspen",
           "Ridge", "Meadow", "Orchard", "Prairie", "Fairway", "Lincoln", "Washington", "Jefferson", "Madison", "Monroe",
           "Riverside", "Hillcrest", "Sunset", "Lakeview", "Park", "Grove", "Brookside", "Woodland", "Highland",
           "Kingsley", "Thornwood", "Ashford", "Wilshire", "Briarwood", "Stonegate", "Fox Run", "Deer Path", "Heritage"]
SUFFIX = ["St", "Ave", "Dr", "Ct", "Ln", "Rd", "Way", "Blvd", "Trl", "Cir"]
ZIPS = {"Grand Rapids": ["49503", "49504", "49505", "49506", "49507", "49508", "49525", "49546"],
        "Wyoming": ["49509", "49519"], "Kentwood": ["49508", "49512"], "Walker": ["49534", "49544"],
        "Grandville": ["49418"], "Rockford": ["49341"], "Cedar Springs": ["49319"], "Lowell": ["49331"],
        "Byron Center": ["49315"], "Comstock Park": ["49321"], "Ada": ["49301"], "Caledonia": ["49316"],
        "Sparta": ["49345"], "Ionia": ["48846"], "Belding": ["48809"], "Portland": ["48875"], "Saranac": ["48881"],
        "Hastings": ["49058"], "Middleville": ["49333"], "Nashville": ["49073"], "Delton": ["49046"],
        "Greenville": ["48838"], "Stanton": ["48888"], "Howard City": ["49329"], "Carson City": ["48811"],
        "Holland": ["49423", "49424"], "Grand Haven": ["49417"], "Zeeland": ["49464"], "Hudsonville": ["49426"],
        "Allendale": ["49401"], "Jenison": ["49428"], "Spring Lake": ["49456"], "Coopersville": ["49404"],
        "Allegan": ["49010"], "Otsego": ["49078"], "Plainwell": ["49080"], "Wayland": ["49348"], "Saugatuck": ["49453"],
        "Fennville": ["49408"], "Hamilton": ["49419"], "Kalamazoo": ["49001", "49006", "49007", "49008", "49009"],
        "Portage": ["49002", "49024"], "Vicksburg": ["49097"], "Schoolcraft": ["49087"], "Richland": ["49083"],
        "Galesburg": ["49053"], "Oshtemo": ["49009"], "Battle Creek": ["49014", "49015", "49017"],
        "Marshall": ["49068"], "Albion": ["49224"], "Springfield": ["49037"], "Homer": ["49245"],
        "South Haven": ["49090"], "Paw Paw": ["49079"], "Lawton": ["49065"], "Bangor": ["49013"], "Hartford": ["49057"],
        "Muskegon": ["49441", "49442", "49444"], "Norton Shores": ["49441", "49444"], "Muskegon Heights": ["49444"],
        "North Muskegon": ["49445"], "Whitehall": ["49461"], "Montague": ["49437"], "Fruitport": ["49415"],
        "Ravenna": ["49451"], "Fremont": ["49412"], "Newaygo": ["49337"], "White Cloud": ["49349"], "Grant": ["49327"],
        "Hart": ["49420"], "Shelby": ["49455"], "Pentwater": ["49449"], "New Era": ["49446"], "Ludington": ["49431"],
        "Scottville": ["49454"], "Custer": ["49405"]}
NE_CITIES = {"Grand Rapids", "Walker", "Comstock Park"}


# ------------------------------------------------------------------------------------------------- identities
class Ids:
    """member numbers, loan numbers, addresses and the first's servicer for every stack, all keyed per stack"""

    def __init__(self, W):
        n = W.n
        g = K.rng(30)
        perm = g.permutation(np.arange(100000, 100000 + 3 * n))[:n]
        self.legacy_member = [int(x) for x in perm]
        self.new_member = []
        for m in self.legacy_member:
            base = "%09d" % (m * 7 % 999999937)
            self.new_member.append(base + str(_luhn_digit(base)))
        self.legacy_loan = []
        used = {}
        for i in range(n):
            gi = K.rng(31, i)
            sfx = int(gi.integers(40, 80))
            key = (self.legacy_member[i], sfx)
            while key in used:
                sfx = 40 + (sfx - 39) % 40
                key = (self.legacy_member[i], sfx)
            used[key] = 1
            self.legacy_loan.append("%d-%02d" % (self.legacy_member[i], sfx))
        perm2 = K.rng(32).permutation(np.arange(n)) + 1
        self.new_loan = ["77%010d" % (int(p) * 8191 % 9999999967) for p in perm2]
        assert len(set(self.new_loan)) == n
        self.street, self.zip, self.servicer, self.escrowed = [], [], [], []
        for i in range(n):
            gi = K.rng(33, i)
            city = W.city[i]
            num = int(gi.integers(100, 9900))
            st = STREETS[int(gi.integers(0, len(STREETS)))]
            sf = SUFFIX[int(gi.integers(0, len(SUFFIX)))]
            quad = (" " + ["NE", "NW", "SE", "SW"][int(gi.integers(0, 4))]) if city in NE_CITIES else ""
            self.street.append("%d %s %s%s" % (num, st, sf, quad))
            zs = ZIPS[city]
            self.zip.append(zs[int(gi.integers(0, len(zs)))])
            if W.cu_first[i]:
                self.servicer.append(K.CU_BUREAU)
                self.escrowed.append(False)
            else:
                p = np.array([w for _, w, _ in SERVICERS])
                k = int(gi.choice(len(SERVICERS), p=p / p.sum()))
                self.servicer.append(SERVICERS[k][0])
                self.escrowed.append(SERVICERS[k][2])
        # the credit union's own first mortgages: one loan number each
        self.mtg_loan = {}
        perm3 = K.rng(34).permutation(np.arange(200000)) + 300000
        k = 0
        for i in range(n):
            if W.cu_first[i]:
                self.mtg_loan[i] = "M%07d" % int(perm3[k])
                k += 1
        self.surname = [SURNAMES[int(K.rng(35, i).integers(0, len(SURNAMES)))] for i in range(n)]


def _luhn_digit(s):
    tot = 0
    for k, ch in enumerate(reversed(s)):
        d = int(ch)
        if k % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        tot += d
    return (10 - tot % 10) % 10


SURNAMES = ["Vander Molen", "DeVries", "Smith", "Johnson", "Brower", "Miller", "Kuipers", "Anderson", "Boersma",
            "Nelson", "Hoekstra", "Visser", "Martin", "Thompson", "Bakker", "Garcia", "Mulder", "Jansen", "Wilson",
            "Taylor", "Moore", "Jackson", "Lee", "Harris", "Clark", "Lewis", "Walker", "Hall", "Allen", "Young",
            "King", "Wright", "Scott", "Green", "Baker", "Adams", "Hill", "Campbell", "Mitchell", "Roberts", "Carter",
            "Phillips", "Evans", "Turner", "Torres", "Parker", "Collins", "Edwards", "Stewart", "Morris", "Murphy",
            "Cook", "Rogers", "Morgan", "Peterson", "Cooper", "Reed", "Bailey", "Bell", "Kowalski", "Nowak", "Schaap",
            "Postma", "Dykstra", "Van Dyke", "Haveman", "Zuidema", "Brinks", "Kamphuis", "Lamberts", "Ritsema",
            "Huizenga", "Grant", "Ortiz", "Nguyen", "Patel", "Hernandez", "Lopez", "Gonzalez", "Rivera", "Ward",
            "Brooks", "Kelly", "Sanders", "Price", "Bennett", "Wood", "Barnes", "Ross", "Henderson", "Coleman",
            "Jenkins", "Perry", "Powell", "Long", "Patterson", "Hughes", "Flores", "Washington", "Butler", "Simmons"]


def fmt_date(d, style):
    if d is None:
        return ""
    if style == "us":
        return "%02d/%02d/%04d" % (d.month, d.day, d.year)
    if style == "iso":
        return d.isoformat()
    raise ValueError(style)


def funded_month_of(W, i):
    return int(W.o2[i])


def bal_at(W, i, t):
    """month-end principal balance of loan i (truth), or None when not on the books at that month-end"""
    return W.bal.get((int(i), int(t)))


def legacy_rows(W, ids):
    """one row per loan on the legacy core's books at any month-end from December 2018 to August 2024"""
    rows = []
    last = K.CONV_M - 1
    for i in range(W.n):
        o2 = int(W.o2[i])
        ex = int(W.exit_m[i])
        if o2 > last:
            continue
        if ex >= 0 and ex < K.REC0:
            continue
        opened = W.d2[i]
        mat = _add_months(opened, int(W.n2[i]))
        bal18 = bal_at(W, i, K.REC0 - 1)
        if o2 <= K.REC0 - 1 and bal18 is None:
            continue
        status, close_dt, close_cd, ret = "", None, "", ""
        if 0 <= ex <= last:
            close_dt = W.exit_day[i]
            close_cd = {"SALE": "PIF", "REFI": "PIF", "PAYOFF": "PIF", "MATURED": "MAT", "CHARGEOFF": "CO"}[W.exit_kind[i]]
            ret = "%.2f" % W.exit_bal[i]
            status = "CLOSED"
        else:
            status = "CNV"
        conv_bal = bal_at(W, i, last) if status == "CNV" else None
        rows.append([ids.legacy_loan[i], ids.legacy_member[i], "HEF%d" % (int(W.n2[i]) // 12), fmt_date(opened, "us"),
                     "{:,.2f}".format(W.H0[i]), "%.3f" % W.r2[i], int(W.n2[i]), "%.2f" % W.pmt2[i], fmt_date(mat, "us"),
                     ("%.2f" % bal18) if (bal18 is not None and o2 <= K.REC0 - 1) else "",
                     status, fmt_date(close_dt, "us"), close_cd, ret,
                     ("%.2f" % conv_bal) if conv_bal is not None else ""])
    rows.sort(key=lambda r: (r[1], r[0]))
    return rows


LEGACY_COLS = ["LOAN_NO", "MBR_NO", "PROD_CD", "OPEN_DT", "ORIG_AMT", "NOTE_RT", "TERM_MOS", "PMT_AMT", "MAT_DT",
               "BAL_12_31_2018", "STATUS", "CLOSE_DT", "CLOSE_CD", "PRIN_AT_CLOSE", "BAL_AT_CONV"]


def _add_months(d, k):
    y, m = d.year, d.month + k
    y += (m - 1) // 12
    m = (m - 1) % 12 + 1
    day = min(d.day, [31, 29 if y % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return dt.date(y, m, day)


def core_rows(W, ids):
    """the new core's monthly trial balance: one row per home equity loan per month-end it was on the books, from
    September 2024 to November 2026, the closing month included"""
    rows = []
    for t in range(K.CONV_M, K.ASOF_M + 1):
        me = K.month_end(t)
        for i in range(W.n):
            o2 = int(W.o2[i])
            ex = int(W.exit_m[i])
            if o2 > t or (0 <= ex < t):
                continue
            b = bal_at(W, i, t)
            prev = bal_at(W, i, t - 1)
            if o2 == t:
                prev = None
            r = W.r2[i]
            if ex == t:
                kind = W.exit_kind[i]
                code = {"SALE": "PIF", "REFI": "PIF", "PAYOFF": "PIF", "MATURED": "MAT", "CHARGEOFF": "CHGOFF"}[kind]
                p0 = W.exit_bal[i]
                interest = 0.0 if kind == "CHARGEOFF" else p0 * r / 1200.0
                paid = 0.0 if kind == "CHARGEOFF" else p0
                sched = W.sched.get((int(i), t), min(p0, max(W.pmt2[i] - interest, 0.0)))
                if kind != "MATURED":
                    sched = min(p0, max(W.pmt2[i] - interest, 0.0))
                rows.append([ids.new_loan[i], ids.new_member[i], "FHE%d" % int(W.n2[i]), me.isoformat(),
                             W.d2[i].isoformat(), "%.2f" % W.H0[i], "%.4f" % (r / 100.0), int(W.n2[i]),
                             "%.2f" % W.pmt2[i], "0.00", "%.2f" % sched, "%.2f" % paid, "%.2f" % interest, code,
                             W.exit_day[i].isoformat(), 0])
                continue
            if b is None:
                continue
            if prev is None:
                sched = 0.0
                paid = 0.0
                interest = 0.0
            else:
                interest = prev * r / 1200.0
                sched = W.sched.get((int(i), t), 0.0)
                paid = prev - b
            rows.append([ids.new_loan[i], ids.new_member[i], "FHE%d" % int(W.n2[i]), me.isoformat(),
                         W.d2[i].isoformat(), "%.2f" % W.H0[i], "%.4f" % (r / 100.0), int(W.n2[i]), "%.2f" % W.pmt2[i],
                         "%.2f" % b, "%.2f" % sched, "%.2f" % paid, "%.2f" % interest, "ACTIVE", "",
                         _dpd(i, t)])
    return rows


CORE_COLS = ["LoanNumber", "MemberNumber", "ProductCode", "AsOfDate", "OpenDate", "OriginalAmount", "InterestRate",
             "TermMonths", "PaymentAmount", "PrincipalBalance", "ScheduledPrincipal", "PrincipalPaid", "InterestPaid",
             "LoanStatus", "CloseDate", "DaysPastDue"]


def _dpd(i, t):
    g = K.rng(40, i, t)
    u = g.random()
    if u < 0.955:
        return 0
    if u < 0.985:
        return int(g.integers(1, 30))
    if u < 0.996:
        return int(g.integers(30, 60))
    return int(g.integers(60, 120))


def xref_rows(W, ids):
    rows = []
    for i in range(W.n):
        o2 = int(W.o2[i])
        ex = int(W.exit_m[i])
        if o2 <= K.CONV_M - 1 and (ex < 0 or ex >= K.CONV_M):
            rows.append([ids.legacy_loan[i], ids.new_loan[i], ids.legacy_member[i], ids.new_member[i], "2024-09-01"])
    rows.sort(key=lambda r: r[0])
    return rows


XREF_COLS = ["legacy_loan_no", "loan_number", "legacy_member_no", "member_number", "converted_on"]


def los_rows(W, ids):
    """the lending system's funded home equity loans since 2009, with the senior lien the underwriter took from the
    applicant's credit report"""
    rows = []
    for i in range(W.n):
        g = K.rng(41, i)
        funded = W.d2[i]
        app = funded - dt.timedelta(days=int(g.integers(24, 52)))
        pi = WD.payment(W.F0[i], W.r1[i], W.n1[i])
        if W.kind[i] == "purchase":
            # a second funded with the purchase: the first's terms come from the purchase file, not a tradeline
            rep_m = int(W.o1[i])
            fb = float(W.F0[i])
            pay = int(round(pi))
            term = str(int(W.n1[i]))
            rate1 = "%.3f" % W.r1[i]
        else:
            rep_m = mo(app.year, app.month) - 1                  # the tradeline's last reported month
            k = rep_m - int(W.o1[i])
            fb = float(WD.sched_balance(W.F0[i], W.r1[i], W.n1[i], k))
            escrow = 0.0
            if ids.escrowed[i]:
                escrow = round(W.value[i] * float(g.uniform(0.016, 0.024)) / 12.0 + float(g.uniform(70, 140)), 0)
            pay = int(round(pi + escrow))
            term = "" if g.random() < 0.07 else str(int(W.n1[i]))
            rate1 = ""
        y1, m1 = ym(int(W.o1[i]))
        loan_no = ids.legacy_loan[i] if int(W.o2[i]) < K.CONV_M else ids.new_loan[i]
        dti = round(float(np.clip(g.normal(0.33, 0.07), 0.12, 0.47)), 3)
        rows.append(["", funded.isoformat(), loan_no,
                     ids.legacy_member[i] if int(W.o2[i]) < K.CONV_M else ids.new_member[i],
                     ids.street[i], W.city[i], W.county[i], "MI", ids.zip[i], int(W.value[i]),
                     "%.1f" % (100 * W.cltv[i]), int(W.score[i]), "%.1f" % (100 * dti), "%.2f" % W.H0[i],
                     "%.2f" % W.r2[i], int(W.n2[i]), ids.servicer[i], "%02d%04d" % (m1, y1), int(round(W.F0[i])), term,
                     int(round(fb)), "%02d%04d" % (ym(rep_m)[1], ym(rep_m)[0]), pay, rate1])
    rows.sort(key=lambda r: (r[1], r[2]))
    # application numbers run in funding order within each year, with the gaps withdrawn and declined applications leave
    g = K.rng(39)
    seq = {}
    for r in rows:
        y = int(r[1][:4])
        seq[y] = seq.get(y, 0) + 1 + int(g.integers(0, 4))
        r[0] = "HE%02d-%05d" % (y % 100, seq[y])
    return rows


LOS_COLS = ["application_id", "funded_date", "loan_number", "member_number", "property_street", "property_city",
            "property_county", "property_state", "property_zip", "appraised_value", "cltv_pct", "credit_score",
            "dti_pct", "loan_amount", "note_rate_pct", "term_months", "senior_lien_creditor", "senior_lien_opened",
            "senior_lien_original_amount", "senior_lien_term_months", "senior_lien_balance", "senior_lien_balance_as_of",
            "senior_lien_monthly_payment", "senior_lien_note_rate_pct"]


def servicing_rows(W, ids):
    """the credit union's own first mortgages behind its members' home equity loans, and its other first mortgages,
    as the servicing system lists them at 30 November 2026 (loans paid off since 1 January 2025 included)"""
    rows = []
    for i, mln in ids.mtg_loan.items():
        o1 = int(W.o1[i])
        y1, m1 = ym(o1)
        opened = K.business_day(dt.date(y1, m1, 1 + int(K.rng(42, i).integers(0, 26))))
        if opened.month != m1:
            opened = K.business_day(dt.date(y1, m1, 1))
        ex = int(W.exit_m[i])
        stack_gone = ex >= 0 and W.exit_kind[i] in ("SALE", "REFI")
        mat = _add_months(opened, int(W.n1[i]))
        sched_end = o1 + int(W.n1[i])
        if stack_gone:
            if ex < mo(2025, 1):
                continue
            fb = float(WD.sched_balance(W.F0[i], W.r1[i], W.n1[i], ex - o1))
            rows.append([mln, ids.new_member[i], ids.street[i], W.city[i], ids.zip[i], opened.isoformat(),
                         "%.2f" % W.F0[i], "%.3f" % W.r1[i], int(W.n1[i]), mat.isoformat(), "PAID IN FULL",
                         W.exit_day[i].isoformat(), "%.2f" % fb, "0.00"])
        else:
            if sched_end <= K.ASOF_M:
                continue
            fb = float(WD.sched_balance(W.F0[i], W.r1[i], W.n1[i], K.ASOF_M - o1))
            rows.append([mln, ids.new_member[i], ids.street[i], W.city[i], ids.zip[i], opened.isoformat(),
                         "%.2f" % W.F0[i], "%.3f" % W.r1[i], int(W.n1[i]), mat.isoformat(), "ACTIVE", "", "",
                         "%.2f" % fb])
    # the credit union's first mortgages with no home equity loan behind them
    g = K.rng(43)
    nmtg = 2400
    perm = K.rng(44).permutation(np.arange(200000)) + 520000
    for k in range(nmtg):
        o1 = int(g.integers(mo(2010, 1), mo(2026, 10)))
        y1, m1 = ym(o1)
        opened = K.business_day(dt.date(y1, m1, int(g.integers(1, 27))))
        n1 = 180 if g.random() < 0.18 else 360
        r1 = round(WD.M30[o1] - (WD.M15_SPREAD if n1 == 180 else 0.0) + g.normal(0, 0.17), 3)
        F0 = round(float(g.uniform(120e3, 420e3)), -2)
        city_key = list(K.CITIES)[int(g.integers(0, len(K.CITIES)))]
        city = K.CITIES[city_key][int(g.integers(0, len(K.CITIES[city_key])))]
        street = "%d %s %s" % (int(g.integers(100, 9900)), STREETS[int(g.integers(0, len(STREETS)))],
                               SUFFIX[int(g.integers(0, len(SUFFIX)))])
        member = "%09d" % int(g.integers(10 ** 8, 10 ** 9 - 1))
        member = member + str(_luhn_digit(member))
        mat = _add_months(opened, n1)
        gone = g.random() < 0.12 and o1 < mo(2026, 6)
        if gone:
            pm = int(g.integers(max(o1 + 3, mo(2025, 1)), K.ASOF_M + 1))
            pd = K.business_day(dt.date(*ym(pm), int(g.integers(1, 27))))
            fb = float(WD.sched_balance(F0, r1, n1, pm - o1))
            rows.append(["M%07d" % int(perm[k]), member, street, city, ZIPS[city][0], opened.isoformat(), "%.2f" % F0,
                         "%.3f" % r1, n1, mat.isoformat(), "PAID IN FULL", pd.isoformat(), "%.2f" % fb, "0.00"])
        else:
            if o1 + n1 <= K.ASOF_M:
                continue
            fb = float(WD.sched_balance(F0, r1, n1, K.ASOF_M - o1))
            rows.append(["M%07d" % int(perm[k]), member, street, city, ZIPS[city][0], opened.isoformat(), "%.2f" % F0,
                         "%.3f" % r1, n1, mat.isoformat(), "ACTIVE", "", "", "%.2f" % fb])
    rows.sort(key=lambda r: r[0])
    return rows


SERV_COLS = ["mortgage_loan_number", "member_number", "property_street", "property_city", "property_zip", "note_date",
             "original_amount", "note_rate_pct", "term_months", "maturity_date", "status", "paid_in_full_date",
             "principal_paid_at_payoff", "principal_balance_2026_11_30"]


def map_rows():
    rows = []
    for rc, cs in K.COUNTIES.items():
        reg = [k for k, v in K.RCODE.items() if v == rc][0]
        for c, _ in cs:
            rows.append([c, "MI", reg, "2016-01-01"])
    # counties in the field of membership with no regional lending center of their own
    rows.append(["Lake", "MI", "Muskegon and the North", "2016-01-01"])
    rows.append(["St. Joseph", "MI", "Kalamazoo and Battle Creek", "2019-07-01"])
    return sorted(rows)


MAP_COLS = ["county", "state", "regional_lending_center", "effective_date"]


def rate_rows():
    """the credit union's posted rate sheets, every Monday from 3 December 2018 to 30 November 2026, with mid-week
    reprices in moving weeks; the rates in effect over a month average to the month's posted level"""
    rows = []
    d = dt.date(2018, 12, 3)
    end = dt.date(2026, 11, 30)
    sheets = []
    g = K.rng(45)
    while d <= end:
        o = mo(d.year, d.month)
        lvl = WD.M30[o]
        wob = float(g.normal(0, 0.035))
        sheets.append((d, round(lvl + wob, 3)))
        if g.random() < 0.18:
            d2 = d + dt.timedelta(days=int(g.integers(2, 4)))
            sheets.append((d2, round(lvl + wob + float(g.choice([-1, 1])) * float(g.uniform(0.04, 0.10)), 3)))
        d += dt.timedelta(days=7)
    # re-centre each month so the day-weighted average of the rate in effect equals the posted monthly level
    sheets.sort()
    by_month = {}
    for k, (d0, r) in enumerate(sheets):
        nxt = sheets[k + 1][0] if k + 1 < len(sheets) else dt.date(2026, 12, 7)
        day = d0
        while day < nxt:
            by_month.setdefault(mo(day.year, day.month), []).append(k)
            day += dt.timedelta(days=1)
    adj = {}
    for o, ks in by_month.items():
        if o < mo(2018, 12) or o > K.ASOF_M:
            continue
        avg = sum(sheets[k][1] for k in ks) / len(ks)
        adj[o] = WD.M30[o] - avg
    out = []
    for d0, r in sheets:
        o = mo(d0.year, d0.month)
        r30 = round(r + adj.get(o, 0.0), 3)
        r15 = round(r30 - WD.M15_SPREAD + float(K.rng(46, d0.toordinal()).normal(0, 0.02)), 3)
        he = {t: round(r30 + WD.HE_SPREAD[t] + float(K.rng(47, d0.toordinal(), t).normal(0, 0.02)), 3)
              for t in (120, 180, 240)}
        out.append((d0, r30, r15, he))
    for d0, r30, r15, he in out:
        for prod, rate, term, fees in (("30 YR FIXED MORTGAGE", r30, 360, 0.0105), ("15 YR FIXED MORTGAGE", r15, 180, 0.0105),
                                       ("HOME EQUITY FIXED 10 YR", he[120], 120, 0.0035),
                                       ("HOME EQUITY FIXED 15 YR", he[180], 180, 0.0035),
                                       ("HOME EQUITY FIXED 20 YR", he[240], 240, 0.0035)):
            rows.append([d0.isoformat(), prod, "%.3f" % rate, "%.3f" % _apr(rate, term, fees)])
    return rows


RATE_COLS = ["effective_date", "product", "rate_pct", "apr_pct"]


def _apr(rate, term, fees):
    """the annual percentage rate of a $200,000 loan at the posted rate with the product's finance charges (a share of
    the amount), the rate whose payment on the net amount equals the note's payment"""
    pmt = WD.payment(200000.0, rate, term)
    net = 200000.0 * (1.0 - fees)
    lo, hi = rate, rate + 2.0
    for _ in range(50):
        mid = (lo + hi) / 2
        if WD.payment(net, mid, term) < pmt:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def heloc_rows(W, ids):
    """the credit union's home equity lines of credit at 30 November 2026 (a separate product)"""
    g = K.rng(48)
    rows = []
    regs = list(K.COUNTIES)
    perm = K.rng(49).permutation(np.arange(100000)) + 410000
    for k in range(2650):
        rc = regs[int(g.choice(4, p=[0.42, 0.24, 0.17, 0.17]))]
        cty = WD._pick(g, K.COUNTIES[rc])
        city = K.CITIES[cty][int(g.integers(0, len(K.CITIES[cty])))]
        opened = K.business_day(dt.date(int(g.integers(2012, 2027)), int(g.integers(1, 13)), int(g.integers(1, 27))))
        if opened > K.AS_OF:
            opened = K.business_day(dt.date(2026, int(g.integers(1, 11)), 12))
        limit = round(float(g.choice([25e3, 30e3, 40e3, 50e3, 60e3, 75e3, 100e3, 125e3, 150e3])), 0)
        util = float(np.clip(g.beta(1.6, 2.4), 0, 1)) if g.random() < 0.78 else 0.0
        bal = round(limit * util, 2)
        margin = round(float(g.choice([-0.25, 0.0, 0.25, 0.50, 0.75, 1.00])), 2)
        draw_end = _add_months(opened, 120)
        status = "OPEN" if g.random() < 0.95 else "FROZEN"
        member = "%09d" % int(g.integers(10 ** 8, 10 ** 9 - 1))
        rows.append(["L%07d" % int(perm[k]), member + str(_luhn_digit(member)), opened.isoformat(), "%.2f" % limit,
                     "%.2f" % bal, "PRIME", "%.2f" % margin, "%.2f" % (7.00 + margin), draw_end.isoformat(), status,
                     cty, ZIPS[city][0]])
    rows.sort(key=lambda r: r[0])
    return rows


HELOC_COLS = ["line_number", "member_number", "open_date", "credit_limit", "balance_2026_11_30", "index", "margin_pct",
              "rate_pct", "draw_period_end", "line_status", "property_county", "property_zip"]


def hpi_rows():
    """a quarterly all-transactions house price index by county (1995 Q1 = 100), constructed"""
    g = K.rng(50)
    rows = []
    for rc, cs in K.COUNTIES.items():
        for c, _ in cs:
            lvl = float(g.uniform(260, 330))
            for y in range(2019, 2027):
                for q in range(1, 5):
                    if y == 2026 and q == 4:
                        break
                    gr = {2019: 0.016, 2020: 0.022, 2021: 0.040, 2022: 0.028, 2023: 0.012, 2024: 0.014, 2025: 0.010,
                          2026: 0.008}[y]
                    lvl *= 1.0 + gr + float(g.normal(0, 0.006))
                    rows.append([c, "MI", "%dQ%d" % (y, q), "%.2f" % lvl])
    return rows


HPI_COLS = ["county", "state", "quarter", "index_1995q1_100"]


def write_all(out, W):
    ids = Ids(W)
    n = {}
    n[F_LEGACY] = K.write_csv(os.path.join(out, F_LEGACY), LEGACY_COLS, legacy_rows(W, ids), crlf=True)
    n[F_CORE] = K.write_csv(os.path.join(out, F_CORE), CORE_COLS, core_rows(W, ids))
    n[F_XREF] = K.write_csv(os.path.join(out, F_XREF), XREF_COLS, xref_rows(W, ids))
    n[F_LOS] = K.write_csv(os.path.join(out, F_LOS), LOS_COLS, los_rows(W, ids))
    n[F_SERV] = K.write_csv(os.path.join(out, F_SERV), SERV_COLS, servicing_rows(W, ids))
    n[F_MAP] = K.write_csv(os.path.join(out, F_MAP), MAP_COLS, map_rows())
    n[F_RATES] = K.write_csv(os.path.join(out, F_RATES), RATE_COLS, rate_rows())
    n[F_HELOC] = K.write_csv(os.path.join(out, F_HELOC), HELOC_COLS, heloc_rows(W, ids))
    n[F_HPI] = K.write_csv(os.path.join(out, F_HPI), HPI_COLS, hpi_rows())
    return ids, n
