"""Write the shipped extracts under target/ from the world and the ledger.

Every file is written the way the system that keeps it exports it: the core banking postings with UTC
posting times and the branch business date, the membership register with its accounts, the CDD profile
extract, the LCTR submission log, the branch network directory, Regional Cash Services' pickup manifests and
bag register, and three files the Unit keeps beside them (STR submissions, its own case register and the
international wire log).
"""
import datetime as dt
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import common as C
import world as W

P_POSTINGS = "core_banking/hrcu_business_postings_2026.csv"
P_REGISTER = "membership/member_register_2026-12-31.xlsx"
P_CDD = "membership/cdd_profiles_extract_2027-01-06.csv"
P_LCTR = "compliance/lctr_submissions_2026.csv"
P_STR = "compliance/str_submissions_2025_2026.csv"
P_CASES = "compliance/fiu_case_register_2026.xlsx"
P_DIR = "branch_network/branch_atm_depository_directory.xlsx"
P_CIT = "cash_services/cit_pickup_manifests_2026.csv"
P_BAGS = "cash_services/night_deposit_bag_register.csv"
P_WIRES = "payments/international_wires_2026.csv"
P_PROG = "compliance/hrcu_aml_atf_compliance_programme_v6-1.pdf"
P_TOR = "compliance/aml_compliance_committee_terms_of_reference.docx"

HEAD = Font(bold=True)
FILL = PatternFill("solid", fgColor="DCE3EA")


def _iso(d):
    return d.isoformat() if d else ""


def _utc(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def _sheet(ws, header, rows, widths):
    ws.append(header)
    for c in ws[1]:
        c.font = HEAD
        c.fill = FILL
        c.alignment = Alignment(vertical="top", wrap_text=True)
    for r in rows:
        ws.append(list(r))
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"


def postings(target, sim):
    rows = []
    for p in sim.postings:
        rows.append((p["posting_id"], p["account_number"], _utc(p["posted_at_utc"]), p["effective_date"].isoformat(),
                     p["transaction_code"], p["channel"], p["transit"], p["terminal_id"], p["description"],
                     ("%.2f" % p["debit"]) if p["debit"] != "" else "", ("%.2f" % p["credit"]) if p["credit"] != "" else "",
                     ("%.2f" % p["cash_portion"]) if p["cash_portion"] != "" else "", p["item_count"]))
    C.write_csv(os.path.join(target, P_POSTINGS),
                ["posting_id", "account_number", "posted_at_utc", "effective_date", "transaction_code", "channel",
                 "transit", "terminal_id", "description", "debit", "credit", "cash_portion", "cheque_items"], rows)
    return len(rows)


def register(target, members):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Members"
    rows = []
    order = sorted(members, key=lambda m: m.number)
    for m in order:
        home = W.LANGLEY_NEW if m.home == W.LANGLEY_OLD else m.home
        rows.append((m.number, m.legal_name, m.op_name, m.trade, W.TRADE[m.trade][1], home, m.since, "CIB", "Active"))
    _sheet(ws, ["member_number", "legal_name", "operating_name", "business_type_code", "business_type",
                "home_transit", "member_since", "monitoring_segment", "status"], rows, [14, 40, 34, 10, 32, 12, 13, 12, 9])
    for r in ws.iter_rows(min_row=2, min_col=7, max_col=7):
        for c in r:
            c.number_format = "yyyy-mm-dd"
    ws2 = wb.create_sheet("Accounts")
    arows = []
    rng = np.random.default_rng(C.SEED + 11)
    for m in order:
        for k, a in enumerate(m.accounts):
            prod = "Business Chequing" if k == 0 else str(rng.choice(["Business Savings", "Business Chequing Plus"]))
            opened = m.since if k == 0 else m.since + dt.timedelta(days=int(rng.integers(30, 1500)))
            opened = min(opened, dt.date(2025, 11, 28))
            dom = W.LANGLEY_NEW if a.startswith(W.LANGLEY_OLD) else a.split("-")[0]
            arows.append((a, m.number, prod, opened, dom))
    _sheet(ws2, ["account_number", "member_number", "product", "opened", "domicile_transit"], arows, [16, 14, 24, 12, 16])
    for r in ws2.iter_rows(min_row=2, min_col=4, max_col=4):
        for c in r:
            c.number_format = "yyyy-mm-dd"
    path = os.path.join(target, P_REGISTER)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wb.save(path)
    C.freeze_zip(path, "Harlow Reach Membership Services")


BANDS = [(0, 250_000, "Under 250,000"), (250_000, 1_000_000, "250,000 to 999,999"),
         (1_000_000, 2_500_000, "1,000,000 to 2,499,999"), (2_500_000, 10**12, "2,500,000 and over")]


def band_of(x):
    for lo, hi, t in BANDS:
        if lo <= x < hi:
            return t
    return BANDS[-1][2]


def cdd(target, members, sim, truth):
    """Each member's CDD profile as the onboarding or last periodic review recorded it."""
    rng = np.random.default_rng(C.SEED + 13)
    rows = []
    profile = {}
    for m in sorted(members, key=lambda m: m.number):
        t = truth[m.number]
        if m.role in ("front_a", "front_b"):
            review = dt.date(2025, 3, 11) if m.role == "front_a" else dt.date(2025, 5, 20)
            exp_cash = t["cash"] / 12.0 * 1.08
            exp_dep = t["credits"] / 12.0 * 1.05
            rtype, risk = "Periodic", "Medium"
        elif m.role == "stale_k":
            review, rtype, risk = dt.date(2018, 6, 19), "Periodic", "Medium"
            exp_cash = t["cash"] / 12.0 / 3.52
            exp_dep = t["credits"] / 12.0 / 2.8
        elif m.role == "stale_s":
            review, rtype, risk = dt.date(2019, 9, 3), "Onboarding", "Low"
            exp_cash = t["cash"] / 12.0 / 3.61
            exp_dep = t["credits"] / 12.0 / 2.7
        else:
            u = rng.random()
            if u < 0.30:
                review = dt.date(2017, 1, 1) + dt.timedelta(days=int(rng.integers(0, 1800)))
                g = float(rng.uniform(1.15, 2.25))
            elif u < 0.70:
                review = dt.date(2022, 1, 1) + dt.timedelta(days=int(rng.integers(0, 1090)))
                g = float(rng.uniform(1.0, 1.45))
            else:
                review = dt.date(2025, 1, 1) + dt.timedelta(days=int(rng.integers(0, 700)))
                g = float(rng.uniform(0.92, 1.15))
            review = max(review, m.since)
            review = min(review, dt.date(2026, 11, 30))
            rtype = "Onboarding" if review == m.since else str(rng.choice(["Periodic", "Periodic", "Event-driven"]))
            risk = str(rng.choice(["Low", "Medium", "Medium", "High"]))
            exp_cash = t["cash"] / 12.0 / g * float(rng.uniform(0.88, 1.22))
            exp_dep = t["credits"] / 12.0 / g * float(rng.uniform(0.85, 1.20))
        exp_cash = round(exp_cash, -2)
        exp_dep = round(exp_dep, -3)
        band = band_of(exp_dep * 12)
        profile[m.number] = dict(review=review, exp_cash=exp_cash, exp_dep=exp_dep, band=band, risk=risk)
        rows.append((m.number, "Business", review.isoformat(), rtype, risk, band, "%d" % exp_cash, "%d" % exp_dep,
                     _next_review(review, risk).isoformat()))
    C.write_csv(os.path.join(target, P_CDD),
                ["member_number", "profile_type", "last_review_date", "review_type", "risk_rating",
                 "anticipated_annual_turnover_band", "anticipated_monthly_cash_deposits_cad",
                 "anticipated_monthly_deposits_cad", "next_review_due"], rows)
    return profile


def _next_review(review, risk):
    years = {"High": 1, "Medium": 2, "Low": 3}[risk]
    try:
        return review.replace(year=review.year + years)
    except ValueError:
        return review.replace(year=review.year + years, day=28)


def lctr_log(target, members, sim):
    """The LCTR submissions as the old reporting module made them: one report per account and business
    date on which the account took CAD 10,000 or more in cash, and the reports for every other member the
    credit union reported on."""
    rng = np.random.default_rng(C.SEED + 17)
    seg = {a: m.number for m in members for a in m.accounts}
    # the people who bring a business's cash in: a branch keying a report by hand puts the conductor's own
    # personal membership in the member field, as the FINTRAC form's conductor section asks
    orng = np.random.default_rng(C.SEED + 18)
    taken = {m.number for m in members}
    owners = {}
    for m in members:
        k = 1 if orng.random() < 0.7 else 2
        owners[m.number] = []
        for _ in range(k):
            while True:
                v = int(orng.integers(1_000_000, 9_999_999))
                if v not in taken:
                    taken.add(v)
                    break
            owners[m.number].append(v)
    acc_day = {}
    acc_branch = {}
    for p in sim.postings:
        if p["cash_portion"] == "" or not p["cash_portion"]:
            continue
        key = (p["account_number"], p["effective_date"])
        acc_day[key] = acc_day.get(key, 0.0) + p["cash_portion"]
        place = p["transit"] or "ATM"
        acc_branch.setdefault(key, {}).setdefault(place, 0.0)
        acc_branch[key][place] += p["cash_portion"]
    rows = []
    used = set()
    for (acct, d), amt in sorted(acc_day.items()):
        if amt < 10_000 or d.year != 2026:
            continue
        ref = _ref(rng, used)
        u = rng.random()
        lag = int(rng.integers(16, 38)) if u < 0.07 else (int(rng.integers(13, 16)) if u < 0.24 else int(rng.integers(2, 13)))
        sub = d + dt.timedelta(days=lag)
        places = acc_branch[(acct, d)]
        place = max(sorted(places), key=lambda k: places[k])
        who = seg[acct]
        if place != "ATM" and rng.random() < 0.24:
            who = owners[seg[acct]][int(rng.integers(len(owners[seg[acct]])))]
        rows.append([ref, "Original", who, acct, d.isoformat(), "%.2f" % amt, place, sub.isoformat(), "Accepted"])
        if rng.random() < 0.04:
            sub2 = sub + dt.timedelta(days=int(rng.integers(1, 9)))
            rows.append([ref, "Correction 1", seg[acct], acct, d.isoformat(), "%.2f" % amt, place, sub2.isoformat(), "Accepted"])
        if rng.random() < 0.012:
            rows.append(list(rows[-1]))
    # December 2025 business filed in January 2026, and the rest of the credit union's reporting
    for k in range(int(rng.integers(835, 925))):
        d = dt.date(2025, 12, 1) + dt.timedelta(days=int(rng.integers(0, 395)))
        if d > dt.date(2026, 12, 31):
            d = dt.date(2026, 12, 31) - dt.timedelta(days=int(rng.integers(0, 40)))
        if not C.is_business_day(d):
            d = C.business_day_on_or_after(d)
            if d.year == 2027:
                d = dt.date(2026, 12, 30)
        ref = _ref(rng, used)
        member = int(rng.integers(1_000_000, 9_999_999))
        while member in {m.number for m in members}:
            member = int(rng.integers(1_000_000, 9_999_999))
        br = W.BRANCHES[int(rng.integers(len(W.BRANCHES)))][0]
        acct = "%s-%07d" % (br, int(rng.integers(1_000_000, 9_999_999)))
        amt = float(np.round(np.exp(rng.normal(9.6, 0.35)) + 10_000, 2))
        sub = d + dt.timedelta(days=int(rng.integers(2, 14)))
        rows.append([ref, "Original", member, acct, d.isoformat(), "%.2f" % amt, br, sub.isoformat(), "Accepted"])
    rows = [r for r in rows if r[7] <= C.PULL.isoformat()]
    rows.sort(key=lambda r: (r[7], r[0], r[1]))
    C.write_csv(os.path.join(target, P_LCTR),
                ["report_reference", "report_version", "member_number", "account_number", "transaction_date",
                 "cash_amount_cad", "location", "submitted_date", "fintrac_status"], rows)
    return rows


def _ref(rng, used):
    while True:
        v = "LC26%07d" % int(rng.integers(0, 9_999_999))
        if v not in used:
            used.add(v)
            return v


def directory(target, sim):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Branches"
    rows = []
    for b in W.BRANCHES:
        rows.append((b[0], b[1], b[3], b[2], b[5], b[6] or "", "Branch" if b[4] else "Regional Cash Services"))
    rows.append((W.CASH_CENTRE[0], W.CASH_CENTRE[1], W.CASH_CENTRE[3], W.CASH_CENTRE[2], dt.date(2016, 9, 6), "", "n/a"))
    _sheet(ws, ["transit", "name", "street_address", "municipality", "opened", "closed", "night_deposits_counted_by"],
           rows, [9, 26, 34, 16, 12, 12, 26])
    for col in (5, 6):
        for r in ws.iter_rows(min_row=2, min_col=col, max_col=col):
            for c in r:
                if c.value:
                    c.number_format = "yyyy-mm-dd"
    ws2 = wb.create_sheet("ATMs")
    arows = sorted(((t, loc, tr, op, cl or "", dep) for (t, loc, tr, op, cl, dep) in sim.atm_rows), key=lambda r: (r[2], r[0]))
    _sheet(ws2, ["terminal_id", "location", "transit", "installed", "removed", "takes_deposits"], arows, [12, 34, 9, 12, 12, 14])
    ws3 = wb.create_sheet("Night depositories")
    drows = sorted(((d, tr, inst, rem or "") for (d, tr, inst, rem) in sim.depo_rows), key=lambda r: r[1])
    _sheet(ws3, ["depository_id", "transit", "installed", "removed"], drows, [14, 9, 12, 12])
    for wsx in (ws2, ws3):
        for r in wsx.iter_rows(min_row=2):
            for c in r:
                if isinstance(c.value, dt.date):
                    c.number_format = "yyyy-mm-dd"
    path = os.path.join(target, P_DIR)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wb.save(path)
    C.freeze_zip(path, "Harlow Reach Facilities")


def cit(target, sim):
    """Regional Cash Services' pickup manifests: the bags the armoured car took from each depository it
    serves, on the morning they were counted."""
    rng = np.random.default_rng(C.SEED + 19)
    by_stop = {}
    for (bag, member, depo, drop, count, cash, where, br) in sim.night_bags:
        if where != "cash_centre":
            continue
        key = (count.date(), depo)
        by_stop.setdefault(key, []).append(bag)
    rows = []
    used = set()
    for (day, depo) in sorted(by_stop):
        while True:
            man = "M%s-%04d" % (day.strftime("%y%m%d"), int(rng.integers(100, 9999)))
            if man not in used:
                used.add(man)
                break
        t = dt.datetime(day.year, day.month, day.day) + dt.timedelta(seconds=int(rng.integers(6 * 3600 + 600, 8 * 3600 + 1500)))
        for bag in sorted(by_stop[(day, depo)]):
            seal = "S%07d" % int(rng.integers(0, 9_999_999))
            rows.append((man, day.isoformat(), t.strftime("%H:%M"), depo, bag, seal, "Blueline Armoured Transport"))
    C.write_csv(os.path.join(target, P_CIT),
                ["manifest_number", "pickup_date", "pickup_time_local", "depository_id", "bag_number", "seal_number",
                 "carrier"], rows)
    return len(rows)


def bags(target, sim):
    rows = []
    for bag in sorted(sim.bag_issue):
        member, transit, issued = sim.bag_issue[bag]
        rows.append((bag, member, transit, issued.isoformat(), "Active"))
    C.write_csv(os.path.join(target, P_BAGS), ["bag_number", "member_number", "issuing_transit", "issued_date", "status"], rows)


def str_log(target, members, by_role):
    rng = np.random.default_rng(C.SEED + 23)
    skip = {m.number for m in by_role.values()}
    seg = [m.number for m in members if m.number not in skip]
    cats = ["Rapid movement of funds", "Third-party cash deposits", "Wire activity inconsistent with profile",
            "Structuring below reporting threshold", "Account activity inconsistent with stated occupation",
            "Possible mule account", "Online banking takeover", "Unusual cheque activity"]
    rows = []
    used = set()
    for k in range(int(rng.integers(120, 150))):
        d = dt.date(2025, 1, 2) + dt.timedelta(days=int(rng.integers(0, 725)))
        while True:
            ref = "STR%s%05d" % (d.strftime("%y"), int(rng.integers(0, 99999)))
            if ref not in used:
                used.add(ref)
                break
        if rng.random() < 0.12:
            subj = int(rng.choice(seg))
        else:
            subj = int(rng.integers(1_000_000, 9_999_999))
        rows.append((ref, d.isoformat(), subj, str(rng.choice(cats)),
                     "%.2f" % float(np.round(np.exp(rng.normal(10.3, 0.9)), 2)), "Submitted"))
    rows.sort(key=lambda r: (r[1], r[0]))
    C.write_csv(os.path.join(target, P_STR), ["str_reference", "submitted_date", "subject_member_number",
                                              "primary_indicator", "amount_involved_cad", "status"], rows)


def case_register(target, members, by_role):
    rng = np.random.default_rng(C.SEED + 29)
    skip = {m.number for m in by_role.values()}
    seg = [m.number for m in members if m.number not in skip]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cases 2026"
    trig = ["Transaction monitoring alert", "STR follow-up", "Law enforcement request", "Production order",
            "Branch referral", "Negative news"]
    outs = ["Closed, no further action", "STR submitted", "Relationship exited", "Open"]
    rows = []
    for k in range(int(rng.integers(48, 66))):
        op = dt.date(2026, 1, 5) + dt.timedelta(days=int(rng.integers(0, 340)))
        o = str(rng.choice(outs, p=[0.45, 0.25, 0.12, 0.18]))
        cl = "" if o == "Open" else op + dt.timedelta(days=int(rng.integers(12, 120)))
        if cl and cl > dt.date(2026, 12, 31):
            cl, o = "", "Open"
        subj = int(rng.choice(seg)) if rng.random() < 0.15 else int(rng.integers(1_000_000, 9_999_999))
        rows.append(("FIU-26-%03d" % (k + 1 + int(rng.integers(0, 2)) * 0), op, cl, subj,
                     "Business" if rng.random() < 0.35 else "Personal", str(rng.choice(trig)), o))
    rows.sort(key=lambda r: r[1])
    numbered, n = [], 0
    for r in rows:
        # a number taken for a case that was merged into another or withdrawn before it opened is not reused
        n += 2 if rng.random() < 0.07 else 1
        numbered.append(("FIU-26-%03d" % n,) + r[1:])
    rows = numbered
    _sheet(ws, ["case_number", "opened", "closed", "subject_member_number", "subject_type", "trigger", "outcome"],
           rows, [13, 12, 12, 20, 12, 30, 26])
    for r in ws.iter_rows(min_row=2, min_col=2, max_col=3):
        for c in r:
            if c.value:
                c.number_format = "yyyy-mm-dd"
    path = os.path.join(target, P_CASES)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wb.save(path)
    C.freeze_zip(path, "Harlow Reach Compliance")


def wires(target, members):
    rng = np.random.default_rng(C.SEED + 31)
    gro = [m for m in members if m.trade in ("GRO", "RFS") and m.role == "honest"]
    rows = []
    used = set()
    ctry = ["CN", "IN", "VN", "PH", "KR", "IT", "MX", "US", "HK", "TW", "TH", "PT"]
    for k in range(int(rng.integers(780, 860))):
        d = C.business_day_on_or_after(dt.date(2026, 1, 2) + dt.timedelta(days=int(rng.integers(0, 362))))
        if d.year != 2026:
            continue
        while True:
            ref = "HRW%07d" % int(rng.integers(0, 9_999_999))
            if ref not in used:
                used.add(ref)
                break
        if rng.random() < 0.45:
            m = gro[int(rng.integers(len(gro)))]
            acct = m.accounts[0]
            direction = "OUT"
        else:
            br = W.BRANCHES[int(rng.integers(len(W.BRANCHES)))][0]
            acct = "%s-%07d" % (br, int(rng.integers(1_000_000, 9_999_999)))
            direction = "OUT" if rng.random() < 0.6 else "IN"
        rows.append((ref, d.isoformat(), acct, direction, "%.2f" % float(np.round(np.exp(rng.normal(9.4, 1.0)), 2)),
                     str(rng.choice(["USD", "CNY", "EUR", "INR", "PHP", "HKD", "CAD"])), str(rng.choice(ctry)),
                     str(rng.choice(["Goods", "Goods", "Services", "Family support", "Tuition", "Property"]))))
    rows.sort(key=lambda r: (r[1], r[0]))
    C.write_csv(os.path.join(target, P_WIRES), ["wire_reference", "value_date", "account_number", "direction",
                                                "amount_cad", "instructed_currency", "counterparty_country", "purpose"], rows)
