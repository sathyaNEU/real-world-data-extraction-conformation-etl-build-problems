"""The golden for task482 (architecture 15), read from the cut pack alone.

Conform Ridgeline's two platforms into one set of claim lines per covered person (the legacy platform's voided
originals out, its replacements in; the new platform's superseded lines out; a legacy claim restated on the new
platform taken from its restatement; every member through the July 2025 crosswalk). Price the 2025 plan year at the
2027 fee schedule: each person's plan-paid amount before the maximum (each covered line at its class's coinsurance
after the deductible the plan applied to it, the lines the maximum cut at their full share), plus the predetermined
work the person put off to the next plan year: 2025 estimate lines whose person, procedure and tooth do not reappear
in the person's 2025 claims and do reappear in the claims within the estimate's twelve months. The plan's cost at a
maximum is the sum over 2025's covered persons of the lesser of that amount and the maximum, per covered person month
of 2025; each option's increase is set against the cost at the current 1,500 dollars.

The asks: the predetermination service standard by quarter (requests received in the quarter, a request on the new
platform being every estimate issued for one member and dentist at one receipt time, answered when its last estimate
is issued, its receipt day under Schedule C's 5:00 p.m. Central rule and holidays), and the orthodontic payments the
plan still owes on 30 September 2026 by the year treatment began (a child's treatment under a second orthodontist is
the same treatment, and a child no longer covered is owed nothing)."""
import csv
import datetime as dt
import os
import sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W   # noqa: E402  (the plan's published constants and Schedule C's calendar only)

D = dt.date
YEAR = 2025
CUT = D(2026, 9, 30)
QUARTERS = ("2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2", "2026Q3")
START_YEARS = (2024, 2025, 2026)
FILES = dict(legacy_claims="rba_classic_claims_2024-01_2025-06.csv", new_claims="rba_nexus_claim_lines_2025-07_2026-10.csv",
             legacy_predets="rba_classic_predeterminations_2024-01_2025-06.csv",
             new_predets="rba_nexus_estimates_2025-06_2026-09.csv", legacy_elig="rba_classic_eligibility_2025-06-30.csv",
             new_elig="rba_nexus_eligibility_2026-10-09.csv", crosswalk="rba_member_crosswalk_2025-07-01.csv",
             fees="ridgeline_ppo_fee_schedule_2024-2027.xlsx", ortho_cases="rba_ortho_case_schedule_2026-09-30.csv",
             ortho_payments="rba_ortho_payments_2024-01_2026-09.csv")


def rows(target, key):
    with open(os.path.join(target, FILES[key]), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def cents(s):
    return int(round(float(s) * 100)) if s not in ("", None) else 0


def usdate(s):
    m, d, y = s.split("/")
    return D(int(y), int(m), int(d))


def isodate(s):
    return D(*map(int, s[:10].split("-")))


def utc_local(s):
    """An ISO UTC stamp as America/Chicago local time."""
    t = dt.datetime(int(s[0:4]), int(s[5:7]), int(s[8:10]), int(s[11:13]), int(s[14:16]))
    for off in (-5, -6):
        loc = t + dt.timedelta(hours=off)
        if W.central_offset(loc) == off:
            return loc
    return t - dt.timedelta(hours=6)


def load(target):
    p = dict((k, rows(target, k)) for k in FILES if k != "fees")
    wb = openpyxl.load_workbook(os.path.join(target, FILES["fees"]), data_only=True)
    fees, cls = {}, {}
    for ws in wb.worksheets:
        y = int(ws.title)
        fees[y] = {}
        for r in ws.iter_rows(min_row=5, values_only=True):
            if r[0] and str(r[0]).startswith("D"):
                fees[y][r[0]] = int(round(float(r[3]) * 100))
                cls[r[0]] = {"I": 1, "II": 2, "III": 3}[r[2]]
    p["fees"], p["cls"] = fees, cls
    return p


# ------------------------------------------------------------------------------------------------------- persons
def person_keys(p):
    """One key per covered person: the new member key where the person has one, the legacy id otherwise."""
    xw = {r["legacy_member_id"]: r["member_key"] for r in p["crosswalk"]}
    return lambda ref: xw.get(ref, ref)


def member_months(p, key):
    """2025 covered months per person: legacy spans run to the June 2025 conversion at most (the legacy extract
    writes an open span as 12/31/9999), new spans from it."""
    months = {}

    def add(k, a, b):
        a, b = max(a, D(YEAR, 1, 1)), min(b, D(YEAR, 12, 31))
        if a > b:
            return
        s = months.setdefault(k, set())
        m = D(a.year, a.month, 1)
        while m <= b:
            s.add(m.month)
            m = D(m.year + (m.month == 12), m.month % 12 + 1, 1)
    for r in p["legacy_elig"]:
        end = usdate(r["TERM_DATE"])
        add(key(r["MEMBER_ID"]), usdate(r["EFF_DATE"]), min(end, D(2025, 6, 30)))
    for r in p["new_elig"]:
        end = isodate(r["coverage_end"]) if r["coverage_end"] else D(2099, 12, 31)
        add(r["member_key"], isodate(r["coverage_start"]), end)
    return {k: len(v) for k, v in months.items()}


def relationship(p, key):
    rel = {}
    for r in p["legacy_elig"]:
        rel[key(r["MEMBER_ID"])] = {"01": "Employee", "02": "Spouse"}.get(r["REL"], "Child")
    for r in p["new_elig"]:
        rel[r["member_key"]] = {"EE": "Employee", "SP": "Spouse", "CH": "Child"}[r["relationship"]]
    return rel


# --------------------------------------------------------------------------------------------------- claim lines
def conformed_lines(p, key):
    """[(person, dos, code, tooth, allowed, paid, deduct, reason)] for every line at its final version."""
    voided = set(r["ORIG_CLAIM_NO"] for r in p["legacy_claims"] if r["TXN"] == "VOID")
    restated = set(r["prior_claim_id"] for r in p["new_claims"] if r["prior_claim_id"])
    out = []
    for r in p["legacy_claims"]:
        if r["TXN"] == "VOID" or (r["TXN"] == "ORIG" and (r["CLAIM_NO"] in voided or r["CLAIM_NO"] in restated)):
            continue
        out.append((key(r["MEMBER_ID"]), usdate(r["DOS"]), "D" + r["PROC"], r["TOOTH"],
                    cents(r["ALLOWED"]), cents(r["PAID"]), cents(r["DEDUCT"]),
                    {"MX": "MAX", "DD": "DED", "FQ": "FRQ", "": ""}[r["REASON"]]))
    for r in p["new_claims"]:
        if r["claim_status"] == "SUPERSEDED":
            continue
        out.append((r["member_key"], isodate(r["service_date"]), r["cdt_code"], r["tooth_number"].lstrip("0"),
                    cents(r["allowed_amt"]), cents(r["plan_paid_amt"]), cents(r["deductible_amt"]),
                    {"119": "MAX", "1": "DED", "151": "FRQ", "": ""}[r["carc"]]))
    return out


def demand(p, lines, year=YEAR, fee_year=2027):
    """Each person's plan-paid amount before the maximum for year's services at fee_year's fees."""
    fees, cls = p["fees"][fee_year], p["cls"]
    out = {}
    for who, dos, code, tooth, allowed, paid, ded, reason in lines:
        if dos.year != year or reason == "FRQ":
            continue
        out[who] = out.get(who, 0) + (fees[code] - ded) * W.COINS[cls[code]] // 100
    return out


# ------------------------------------------------------------------------------------------- the put-off work
def utc_naive(s):
    return dt.datetime(int(s[0:4]), int(s[5:7]), int(s[8:10]), int(s[11:13]), int(s[14:16]))


def estimate_lines(p, key, conv=utc_local):
    """[(person, receipt local, issued local date, code, tooth, est_allowed, est_deduct, est_plan, request id, npi,
    estimate id)]: a request on the new platform is every estimate issued for one member and dentist at one receipt
    time. conv reads the new platform's UTC stamps (Central time by default; the variants read them otherwise)."""
    out = []
    for r in p["legacy_predets"]:
        out.append((key(r["MEMBER_ID"]), dt.datetime.strptime(r["RECEIVED"], "%m/%d/%Y %H:%M"), usdate(r["RESPONDED"]),
                    "D" + r["PROC"], r["TOOTH"], cents(r["EST_ALLOWED"]), cents(r["EST_DEDUCT"]),
                    cents(r["EST_PLAN_PMT"]), ("L", r["PREDET_NO"]), r["PROV_NPI"], r["PREDET_NO"]))
    for r in p["new_predets"]:
        out.append((r["member_key"], conv(r["received_utc"]), conv(r["issued_utc"]).date(), r["cdt_code"],
                    r["tooth_number"].lstrip("0"), cents(r["est_allowed_amt"]), cents(r["est_deductible_amt"]),
                    cents(r["est_plan_amt"]), ("N", r["member_key"], r["rendering_npi"], r["received_utc"]),
                    r["rendering_npi"], r["estimate_id"]))
    return out


def put_off_work(p, key, lines, est=None, fee_year=2027, require_cut=True, window="validity", need_later=True):
    """Each person's 2025 predetermined work not claimed in 2025 and claimed within the estimate's twelve months,
    priced at fee_year's fees; the variants are the fork table's rows."""
    est = est if est is not None else estimate_lines(p, key)
    fees, cls = p["fees"][fee_year], p["cls"]
    claimed = {}
    for who, dos, code, tooth, *_ in lines:
        claimed.setdefault((who, code, tooth), []).append(dos)
    # a request is cut when the maximum cuts any of its lines: the member decides on the treatment as estimated
    cut = set()
    for who, recv, issued, code, tooth, allowed, ded, plan, req, npi, eid in est:
        if plan < (allowed - ded) * W.COINS[cls[code]] // 100:
            cut.add(req)
    seen, out = set(), {}
    for who, recv, issued, code, tooth, allowed, ded, plan, req, npi, eid in est:
        if issued.year != YEAR:
            continue
        if require_cut and req not in cut:
            continue
        k = (who, code, tooth)
        if k in seen:
            continue
        dates = claimed.get(k, [])
        if any(recv.date() <= d0 <= D(YEAR, 12, 31) for d0 in dates):
            continue
        if need_later:
            end = D(issued.year + 1, issued.month, min(issued.day, 28)) if window == "validity" else D(YEAR + 1, 6, 30)
            if not any(D(YEAR + 1, 1, 1) <= d0 <= end for d0 in dates):
                continue
        seen.add(k)
        out[who] = out.get(who, 0) + fees[code] * W.COINS[cls[code]] // 100
    return out


# ------------------------------------------------------------------------------------------------------- the call
def costs(dem, put, mm, options=W.OPTIONS):
    persons = [k for k, m in mm.items() if m > 0]
    months = sum(mm[k] for k in persons)
    base = sum(min(dem.get(k, 0), W.MAXIMUM) for k in persons)
    out = {}
    for m in options:
        cost = sum(min(dem.get(k, 0) + (put.get(k, 0) if m > W.MAXIMUM else 0), m) for k in persons)
        out[m] = dict(cost=cost, pmpm=cost / 100.0 / months, raw_increase=(cost - base) / 100.0 / months,
                      increase_pct=100.0 * (cost - base) / base)
    for m in options:
        # the costing standard states amounts per covered person month to the cent
        out[m]["pmpm_c"] = round(out[m]["pmpm"] + 1e-9, 2)
        out[m]["increase"] = round(out[m]["pmpm_c"] - out[W.MAXIMUM]["pmpm_c"], 2)
    return dict(base=base, months=months, persons=len(persons), options=out)


def call(c, limit=W.LIMIT, menu=(200000, 300000)):
    fits = [m for m in menu if round(c["options"][m]["increase"] * 100) <= limit]
    return max(fits) if fits else W.MAXIMUM


# --------------------------------------------------------------------------------------------------------- ask A
def turnaround(p, key, est=None, group_new=True, rule=True, holidays=True):
    """{quarter: (requests received, answered within five business days)} under Schedule C: a request is answered
    when its last estimate is issued; group_new=False counts each of the new platform's estimates as a request."""
    est = est if est is not None else estimate_lines(p, key)
    reqs = {}
    for who, recv, issued, code, tooth, allowed, ded, plan, req, npi, eid in est:
        rid = req if group_new or req[0] == "L" else ("E", eid)
        reqs.setdefault(rid, [recv, issued])
        reqs[rid][1] = max(reqs[rid][1], issued)
    hol = W.HOLIDAY_SET if holidays else set()

    def business(d):
        return d.weekday() < 5 and d not in hol

    def nxt(d):
        while not business(d):
            d += dt.timedelta(days=1)
        return d

    out = {}
    for rid, (recv, done) in reqs.items():
        d = recv.date()
        if rule and (not business(d) or recv.time() >= dt.time(17, 0)):
            d = nxt(d + dt.timedelta(days=1))
        elif not rule:
            d = nxt(d)
        q = "%dQ%d" % (d.year, (d.month - 1) // 3 + 1)
        if q not in QUARTERS:
            continue
        n, x = 0, d
        while x < done:
            x += dt.timedelta(days=1)
            if business(x):
                n += 1
        tot, ok = out.get(q, (0, 0))
        out[q] = (tot + 1, ok + (n <= 5))
    return dict(sorted(out.items()))


# --------------------------------------------------------------------------------------------------------- ask B
def ortho_owed(p, key, by_child=True, check_coverage=True):
    """The orthodontic payments the plan still owes on 30 September 2026 and the children in treatment, by the year
    each child's treatment began."""
    pays = {}
    for r in p["ortho_payments"]:
        pays[r["case_id"]] = pays.get(r["case_id"], 0) + cents(r["amount"])
    cases = {}
    for r in p["ortho_cases"]:
        k = key(r["member_ref"]) if by_child else r["case_id"]
        cases.setdefault(k, []).append(r)
    cover = {}
    for r in p["new_elig"]:
        end = isodate(r["coverage_end"]) if r["coverage_end"] else D(2099, 12, 31)
        cover[r["member_key"]] = (isodate(r["coverage_start"]), end)
    for r in p["legacy_elig"]:
        k = key(r["MEMBER_ID"])
        if k not in cover:
            end = usdate(r["TERM_DATE"])
            cover[k] = (usdate(r["EFF_DATE"]), min(end, D(2025, 6, 30)) if end.year == 9999 else end)
    owed = dict((y, 0) for y in START_YEARS)
    kids = dict((y, 0) for y in START_YEARS)
    for k, cs in cases.items():
        cs = sorted(cs, key=lambda r: r["banding_date"])
        active = cs[-1]
        began = isodate(cs[0]["banding_date"]).year
        ends = W.add_months(isodate(active["banding_date"]), int(active["treatment_months"]))
        who = key(active["member_ref"])
        if check_coverage:
            a, b = cover.get(who, (D(1900, 1, 1), D(1900, 1, 1)))
            if not (a <= CUT <= b):
                continue
        if ends <= CUT:
            continue
        left = cents(active["plan_benefit"]) - pays.get(active["case_id"], 0)
        if left <= 0 or began not in owed:
            continue
        owed[began] += left
        kids[began] += 1
    return owed, kids


# ---------------------------------------------------------------------------------------------------------- solve
def solve(target):
    p = load(target)
    key = person_keys(p)
    lines = conformed_lines(p, key)
    mm = member_months(p, key)
    dem = demand(p, lines)
    est = estimate_lines(p, key)
    put = put_off_work(p, key, lines, est)
    gold = costs(dem, put, mm)
    naive = costs(dem, {}, mm)
    owed, kids = ortho_owed(p, key)
    rel = relationship(p, key)
    paid25 = {}
    for who, dos, code, tooth, allowed, paid, ded, reason in lines:
        if dos.year == YEAR:
            paid25[who] = paid25.get(who, 0) + paid
    return dict(p=p, key=key, lines=lines, mm=mm, dem=dem, put=put, gold=gold, naive=naive, call=call(gold),
                naive_call=call(naive), ask_a=turnaround(p, key, est), ortho=(owed, kids), rel=rel, paid25=paid25,
                est=est)


if __name__ == "__main__":
    res = solve(os.path.join(os.path.dirname(HERE), "target"))
    g, n = res["gold"], res["naive"]
    print("persons %d, months %d, base %.2f" % (g["persons"], g["months"], g["base"] / 100))
    for m in W.OPTIONS:
        print("max %d: golden %.4f pmpm (+%.2f, raw %.4f, %.2f%%) | naive %.4f pmpm (+%.2f, raw %.4f)" % (
            m // 100, g["options"][m]["pmpm"], g["options"][m]["increase"], g["options"][m]["raw_increase"],
            g["options"][m]["increase_pct"], n["options"][m]["pmpm"], n["options"][m]["increase"],
            n["options"][m]["raw_increase"]))
    print("call", res["call"], "naive call", res["naive_call"], "put-off persons", len(res["put"]),
          "amount %.2f" % (sum(res["put"].values()) / 100))
    print("ask A", res["ask_a"])
    print("ask B", res["ortho"])
