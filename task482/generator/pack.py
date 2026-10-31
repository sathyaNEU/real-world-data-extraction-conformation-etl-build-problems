"""Cut task482's pack (architecture 15) from the world's truth: Ridgeline's two adjudication platforms' claim extracts,
their predetermination logs, month-end accumulators and eligibility, the July 2025 member crosswalk, the PPO fee
schedule workbook, the orthodontic case schedule and payments, and two out-of-scope files."""
import csv
import datetime as dt
import io

import openpyxl
from openpyxl.styles import Font

import world as W

D = dt.date


def _csv(path, header, rows, crlf=True):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


def money(c):
    return "%.2f" % (c / 100.0)


def us(d):
    return d.strftime("%m/%d/%Y") if d else ""


def iso(d):
    return d.isoformat() if d else ""


# ------------------------------------------------------------------------------------------------------ identities
def identities(w):
    """Each person's legacy member id (subscriber number and suffix) where covered before the migration, and new
    member key where covered from it; the crosswalk pairs the two for everyone converted on 1 July 2025."""
    people = w["people"]
    r = W.rng("ids")
    emp_people = {}
    for p in people:
        emp_people.setdefault(p["emp"], []).append(p)
    legacy, new = {}, {}
    used = set()
    late = set(c["pid"] for c in w["claims"] if c["adjudicated"] >= W.MIGRATION)
    late |= set(w["claims"][cid]["pid"] for cid, a in w["adjust"].items() if a["date"] >= W.MIGRATION)
    late |= set(pr["pid"] for pr in w["predets"] if pr["received_local"].date() >= D(2025, 6, 28))
    for emp in sorted(emp_people):
        fam = emp_people[emp]
        kids = sorted((p for p in fam if p["kind"] == "C"), key=lambda p: (p["dob"], p["pid"]))
        for p in fam:
            if p["start"] < W.MIGRATION:
                if p["kind"] == "E":
                    sfx = "01"
                elif p["kind"] == "S":
                    sfx = "02"
                else:
                    sfx = "%02d" % (3 + kids.index(p))
                legacy[p["pid"]] = ("PC%06d" % emp, "PC%06d-%s" % (emp, sfx))
            if p["end"] is None or p["end"] >= W.MIGRATION or p["pid"] in late:
                while True:
                    k = "RBN%08d" % r.randint(10000000, 99999999)
                    if k not in used:
                        used.add(k)
                        break
                new[p["pid"]] = k
    sub_new = {}
    for emp, fam in emp_people.items():
        e = [p for p in fam if p["kind"] == "E"][0]
        sub_new[emp] = new.get(e["pid"])
    return dict(legacy=legacy, new=new, sub_new=sub_new)


def platform_of(day):
    return "new" if day >= W.MIGRATION else "legacy"


# ---------------------------------------------------------------------------------------------------------- claims
def claim_rows(w, ids):
    """Every line on the platform that adjudicated it, with each correction as that platform writes it: the legacy
    platform voids the original and pays a replacement under a new number; the new platform restates the claim
    under a new number and marks the original superseded; a legacy claim corrected after the migration is restated
    on the new platform, its legacy original left as paid."""
    people = {p["pid"]: p for p in w["people"]}
    legacy_rows, new_rows = [], []
    seq_l, seq_n = [0], [0]
    gaps = W.rng("nexus-claim-ids")       # Nexus numbers claims across every client it administers

    def legacy_no(day):
        seq_l[0] += 1
        return "C%02d%03d%05d" % (day.year % 100, day.timetuple().tm_yday, seq_l[0] % 100000)

    def new_no():
        seq_n[0] += gaps.randint(1, 13)
        return "RN%010d" % (7004000000 + seq_n[0])

    def tooth_l(t):
        return "" if t is None else str(t)

    def tooth_n(t):
        return "" if t is None else "%02d" % t

    def quad(code, t):
        return {1: "UR", 2: "UL", 3: "LL", 4: "LR"}[t] if code == "D4341" else ""

    def leg_reason(ln):
        return {"MAX": "MX", "DED": "DD", "FRQ": "FQ", "": ""}[ln["reason"]]

    def new_carc(ln):
        return {"MAX": "119", "DED": "1", "FRQ": "151", "": ""}[ln["reason"]]

    def charge(ln, oon):
        base = W.FEES[2024][ln["code"]] if ln["allowed"] == 0 else ln["allowed"]
        return int(round(base * (1.38 if oon else 1.22) / 100.0)) * 100

    oon_set = set(w["providers"]["oon"])

    def leg_line(c, cno, k, ln, txn, orig, sign=1):
        p = people[c["pid"]]
        sub, mid = ids["legacy"][p["pid"]]
        oon = c["provider"] in oon_set
        return [cno, k + 1, mid, sub, us(c["dos"]), ln["code"][1:], tooth_l(ln["tooth"]), quad(ln["code"], ln["tooth"]),
                c["provider"], "N" if oon else "Y", money(sign * charge(ln, oon)), money(sign * ln["allowed"]),
                money(sign * ln["paid"]), money(sign * (ln["allowed"] - ln["paid"])), money(sign * ln["ded"]),
                leg_reason(ln), txn, orig, us(c["received"]), us(c["adjudicated"] if txn == "ORIG" else c["_adj_on"])]

    def new_line(c, cid, k, ln, status, prior, adj_day):
        p = people[c["pid"]]
        oon = c["provider"] in oon_set
        return [cid, k + 1, ids["new"][p["pid"]], ln["code"], tooth_n(ln["tooth"]),
                quad(ln["code"], ln["tooth"]), iso(c["dos"]), c["provider"], "OUT" if oon else "IN",
                money(charge(ln, oon)), money(ln["allowed"]), money(ln["paid"]), money(ln["allowed"] - ln["paid"]),
                money(ln["ded"]), new_carc(ln), status, prior, iso(c["received"]), iso(adj_day)]

    for c in sorted(w["claims"], key=lambda c: (c["adjudicated"], c["cid"])):
        adj = w["adjust"].get(c["cid"])
        if platform_of(c["adjudicated"]) == "legacy":
            cno = legacy_no(c["adjudicated"])
            for k, ln in enumerate(c["lines"]):
                legacy_rows.append((c["adjudicated"], leg_line(c, cno, k, ln, "ORIG", "")))
            if adj:
                if platform_of(adj["date"]) == "legacy":
                    c2 = dict(c, _adj_on=adj["date"])
                    for k, ln in enumerate(c["lines"]):
                        legacy_rows.append((adj["date"], leg_line(c2, cno, k, ln, "VOID", cno, sign=-1)))
                    rno = legacy_no(adj["date"])
                    for k, ln in enumerate(adj["lines"]):
                        legacy_rows.append((adj["date"], leg_line(c2, rno, k, ln, "REPL", cno)))
                else:
                    cid2 = new_no()
                    for k, ln in enumerate(adj["lines"]):
                        new_rows.append((adj["date"], new_line(c, cid2, k, ln, "PAID", cno, adj["date"])))
        else:
            cid = new_no()
            status = "SUPERSEDED" if adj else ("DENIED" if all(ln["reason"] == "FRQ" for ln in c["lines"]) else "PAID")
            for k, ln in enumerate(c["lines"]):
                new_rows.append((c["adjudicated"], new_line(c, cid, k, ln, status, "", c["adjudicated"])))
            if adj:
                cid2 = new_no()
                for k, ln in enumerate(adj["lines"]):
                    new_rows.append((adj["date"], new_line(c, cid2, k, ln, "PAID", cid, adj["date"])))
    legacy_rows.sort(key=lambda x: (x[0], x[1][0], x[1][1], x[1][16] != "ORIG"))
    new_rows.sort(key=lambda x: (x[0], x[1][0], x[1][1]))
    return [r for _, r in legacy_rows], [r for _, r in new_rows]


LEGACY_CLAIM_HEADER = ["CLAIM_NO", "LINE_NO", "MEMBER_ID", "SUBSCRIBER_ID", "DOS", "PROC", "TOOTH", "QUAD", "PROV_NPI",
                       "PAR", "CHARGE", "ALLOWED", "PAID", "MEMBER_RESP", "DEDUCT", "REASON", "TXN", "ORIG_CLAIM_NO",
                       "RECEIVED", "PROCESSED"]
NEW_CLAIM_HEADER = ["claim_id", "line_seq", "member_key", "cdt_code", "tooth_number", "quadrant", "service_date",
                    "rendering_npi", "network_status", "billed_amt", "allowed_amt", "plan_paid_amt", "patient_resp_amt",
                    "deductible_amt", "carc", "claim_status", "prior_claim_id", "received_date", "adjudicated_date"]


def write_claims(t, w, ids):
    leg, new = claim_rows(w, ids)
    _csv(t("legacy_claims"), LEGACY_CLAIM_HEADER, leg)
    _csv(t("new_claims"), NEW_CLAIM_HEADER, new)
    return len(leg), len(new)


# --------------------------------------------------------------------------------------------- predeterminations
def predet_rows(w, ids):
    """The legacy log holds one predetermination number per request with its lines; the new platform issues an
    estimate per tooth group, each with its own number and issue time, all carrying the request's receipt time."""
    people = {p["pid"]: p for p in w["people"]}
    legacy, new = [], []
    r = W.rng("predet-ids")
    pno, eno = 51000, 880000
    for pr in sorted(w["predets"], key=lambda x: (x["received_local"], x["pid"])):
        p = people[pr["pid"]]
        local = pr["received_local"]
        if local.date() < D(2025, 6, 28):
            pno += r.randint(1, 4)
            sub, mid = ids["legacy"][p["pid"]]
            resp = max(pr["responded_local"])
            for k, ln in enumerate(pr["lines"]):
                legacy.append([ "PD%06d" % pno, k + 1, mid, pr["provider"], local.strftime("%m/%d/%Y %H:%M"),
                                us(resp.date()), ln["code"][1:], "" if ln["tooth"] is None else str(ln["tooth"]),
                                money(int(round(ln["allowed"] * 1.22 / 100.0)) * 100), money(ln["allowed"]),
                                money(ln["ded"]), money(ln["est"]), money(ln["allowed"] - ln["est"])])
        else:
            utc = W.to_utc(local)
            for gi, glines in enumerate(pr["groups"]):
                eno += r.randint(1, 6)
                issued = W.to_utc(pr["responded_local"][gi])
                k = 0
                for ln in pr["lines"]:
                    if ln["group"] != gi:
                        continue
                    k += 1
                    new.append(["E%07d" % eno, k, ids["new"][p["pid"]], pr["provider"],
                                utc.strftime("%Y-%m-%dT%H:%M:00Z"), issued.strftime("%Y-%m-%dT%H:%M:00Z"), ln["code"],
                                "" if ln["tooth"] is None else "%02d" % ln["tooth"],
                                money(int(round(ln["allowed"] * 1.22 / 100.0)) * 100), money(ln["allowed"]),
                                money(ln["ded"]), money(ln["est"]), money(ln["allowed"] - ln["est"])])
    return legacy, new


LEGACY_PREDET_HEADER = ["PREDET_NO", "LINE_NO", "MEMBER_ID", "PROV_NPI", "RECEIVED", "RESPONDED", "PROC", "TOOTH",
                        "SUBMITTED", "EST_ALLOWED", "EST_DEDUCT", "EST_PLAN_PMT", "EST_MEMBER_PMT"]
NEW_PREDET_HEADER = ["estimate_id", "est_line", "member_key", "rendering_npi", "received_utc", "issued_utc", "cdt_code",
                     "tooth_number", "submitted_amt", "est_allowed_amt", "est_deductible_amt", "est_plan_amt",
                     "est_patient_amt"]


def write_predets(t, w, ids):
    leg, new = predet_rows(w, ids)
    _csv(t("legacy_predets"), LEGACY_PREDET_HEADER, leg)
    _csv(t("new_predets"), NEW_PREDET_HEADER, new)


# --------------------------------------------------------------------------------------------------- accumulators
def accumulator_rows(w, ids):
    """Month-end year-to-date plan payments toward the annual maximum by person, as each platform held them; the new
    platform opened on 1 July 2025 with each converted person's legacy year-to-date."""
    people = {p["pid"]: p for p in w["people"]}
    events = {}
    for c in w["claims"]:
        y = c["dos"].year
        paid = sum(ln["paid"] for ln in c["lines"])
        events.setdefault((c["pid"], y), []).append((c["adjudicated"], paid))
        adj = w["adjust"].get(c["cid"])
        if adj:
            events[(c["pid"], y)].append((adj["date"], sum(ln["paid"] for ln in adj["lines"]) - paid))
    legacy, new = [], []
    month_ends = []
    d = D(2024, 1, 31)
    while d <= D(2026, 9, 30):
        month_ends.append(d)
        d = W.month_end(d + dt.timedelta(days=1))
    for (pid, y), ev in sorted(events.items()):
        p = people[pid]
        cov = W.coverage_in_year(p, y)
        if not cov:
            continue
        for me in month_ends:
            if me.year != y or me < W.month_end(cov[0]) or me > W.month_end(cov[1]):
                continue
            ytd = sum(x for d0, x in ev if d0 <= me)
            reached = ""
            run = 0
            for d0, x in sorted(ev):
                if d0 > me:
                    break
                run += x
                if run >= W.MAXIMUM:
                    reached = d0
                    break
            row_pl = "legacy" if me < W.MIGRATION else "new"
            if row_pl == "legacy" and pid in ids["legacy"]:
                legacy.append([ids["legacy"][pid][1], us(me), y, money(ytd), money(W.MAXIMUM), us(reached) if reached else ""])
            elif row_pl == "new" and pid in ids["new"]:
                new.append([ids["new"][pid], iso(me), y, money(ytd), money(max(0, W.MAXIMUM - ytd)),
                            iso(reached) if reached else ""])
    return legacy, new


def write_accumulators(t, w, ids):
    leg, new = accumulator_rows(w, ids)
    _csv(t("legacy_accum"), ["MEMBER_ID", "PERIOD_END", "PLAN_YEAR", "YTD_APPLIED", "ANNUAL_MAX", "MAX_MET_DATE"], leg)
    _csv(t("new_accum"), ["member_key", "period_end", "plan_year", "ytd_applied_amt", "remaining_amt", "max_met_date"],
         new)


# ---------------------------------------------------------------------------------------------------- eligibility
def write_eligibility(t, w, ids):
    leg, new = [], []
    rel_new = {"E": "EE", "S": "SP", "C": "CH"}
    for p in w["people"]:
        if p["pid"] in ids["legacy"]:
            sub, mid = ids["legacy"][p["pid"]]
            end = p["end"] if p["end"] and p["end"] < W.MIGRATION else None
            leg.append([mid, sub, mid[-2:], us(p["dob"]), p["sex"], us(p["start"]),
                        us(end) if end else "12/31/9999", "DPPO1"])
        if p["pid"] in ids["new"]:
            start = max(p["start"], W.MIGRATION)
            new.append([ids["new"][p["pid"]], ids["sub_new"][p["emp"]], rel_new[p["kind"]], iso(p["dob"]),
                        {"M": "1", "F": "2"}[p["sex"]], iso(start), iso(p["end"]) if p["end"] else "", "PCC-DENTAL-PPO"])
    leg.sort()
    new.sort()
    _csv(t("legacy_elig"), ["MEMBER_ID", "SUBSCRIBER_ID", "REL", "DOB", "SEX", "EFF_DATE", "TERM_DATE", "PLAN"], leg)
    _csv(t("new_elig"), ["member_key", "subscriber_key", "relationship", "birth_date", "gender_code", "coverage_start",
                         "coverage_end", "plan_code"], new)


def write_crosswalk(t, w, ids):
    rows = sorted([ids["legacy"][pid][1], ids["new"][pid], "2025-07-01"] for pid in ids["legacy"] if pid in ids["new"])
    _csv(t("crosswalk"), ["legacy_member_id", "member_key", "converted_on"], rows)


# ---------------------------------------------------------------------------------------------------- fee schedule
def write_fees(t):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for y in (2024, 2025, 2026, 2027):
        ws = wb.create_sheet(str(y))
        ws.append([W.TPA + " - PPO dental fee schedule, " + W.COMPANY + " Dental Plan"])
        ws.append(["Network maximum allowable fees effective 1 January %d" % y])
        ws.append([])
        ws.append(["Code", "Description", "Class", "Allowed fee"])
        ws["A1"].font = Font(bold=True)
        for c in ws[4]:
            c.font = Font(bold=True)
        for code, (desc, cls, _, _) in W.PROCS.items():
            ws.append([code, desc, {1: "I", 2: "II", 3: "III"}[cls], W.FEES[y][code] / 100.0])
        for row in ws.iter_rows(min_row=5, min_col=4, max_col=4):
            for c in row:
                c.number_format = "#,##0.00"
        ws.column_dimensions["A"].width = 8
        ws.column_dimensions["B"].width = 62
        ws.column_dimensions["C"].width = 7
        ws.column_dimensions["D"].width = 12
    wb.save(t("fees"))


# ----------------------------------------------------------------------------------------------------- orthodontics
def ortho_tables(w, ids):
    """The orthodontic module's case schedule (one row per case as set up from the orthodontist's banding claim) and
    its payments (the banding payment and the monthly installments), each payment under the member identifier of
    the platform that made it; a case handed to a second orthodontist is set up again as that orthodontist's case."""
    people = {p["pid"]: p for p in w["people"]}
    cases, pays = [], []
    cno = 3100
    gaps = W.rng("ortho-case-ids")
    for case in sorted(w["ortho"], key=lambda c: (c["band"], c["pid"])):
        p = people[case["pid"]]
        legs = [(case["ortho"], case["band"], case["fee"], case["months"])]
        if case["transfer"]:
            done = (case["transfer"]["date"].year - case["band"].year) * 12 + case["transfer"]["date"].month - case["band"].month
            legs.append((case["transfer"]["ortho"], case["transfer"]["date"], case["transfer"]["fee"],
                         max(3, case["months"] - done)))
        used = 0
        for li, (ortho, band, fee, months) in enumerate(legs):
            if band > W.SERVICE_END:
                continue            # the schedule stands at 30 September 2026: a later banding is not set up yet
            cno += gaps.randint(3, 11)
            benefit = min(fee * W.ORTHO_COINS // 100, W.ORTHO_LIFETIME - used)
            initial = benefit // 4
            inst = (benefit - initial) // max(1, months - 1)
            stop = None
            if li == 0 and case["transfer"]:
                stop = case["transfer"]["date"]
            member = lambda d: ids["new"].get(p["pid"]) if d >= W.MIGRATION else ids["legacy"].get(p["pid"], ("", ""))[1]
            cases.append(["OC%05d" % cno, member(band) or member(W.MIGRATION), ortho, iso(band), money(fee), months,
                          money(benefit), money(initial), money(inst)])
            paid = 0
            if W.covered(p, band):
                pays.append(["OC%05d" % cno, member(band), iso(band), "D8080", money(initial)])
                paid += initial
            for k in range(1, months):
                d = W.add_months(D(band.year, band.month, 1), k)
                if d > W.SERVICE_END or (stop and d >= stop) or not W.covered(p, d):
                    break
                amt = inst if k < months - 1 else benefit - initial - inst * (months - 2)
                pays.append(["OC%05d" % cno, member(d), iso(d), "D8670", money(amt)])
                paid += amt
            used += paid
    return cases, pays


def write_ortho(t, w, ids):
    cases, pays = ortho_tables(w, ids)
    _csv(t("ortho_cases"), ["case_id", "member_ref", "orthodontist_npi", "banding_date", "case_fee", "treatment_months",
                            "plan_benefit", "initial_payment", "monthly_installment"], cases)
    _csv(t("ortho_payments"), ["case_id", "member_ref", "payment_date", "cdt_code", "amount"], pays)


# ------------------------------------------------------------------------------------------------------ distractors
def write_distractors(t, w):
    r = W.rng("network")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Access"
    ws.append([W.TPA + " - network access report, " + W.COMPANY + " Dental Plan, quarter ending 30 June 2026"])
    ws.append([])
    ws.append(["ZIP3", "Employees", "General dentists in network", "Accepting new patients", "Specialists in network",
               "Employees within 10 miles of two general dentists"])
    for c in ws[3]:
        c.font = Font(bold=True)
    for z in ("640", "641", "644", "645", "646", "647", "648", "650", "651", "652", "653", "654", "655", "656", "657"):
        e = r.randint(30, 420)
        g = r.randint(3, 40)
        ws.append([z, e, g, max(1, g - r.randint(0, g // 3)), r.randint(0, 9), round(min(1.0, 0.55 + g / 60.0), 3)])
    ws.column_dimensions["A"].width = 7
    for col in "BCDEF":
        ws.column_dimensions[col].width = 16
    wb.save(t("network"))
    rows = []
    d = D(2025, 1, 1)
    while d <= D(2026, 9, 1):
        n = sum(1 for p in w["people"] if p["kind"] == "E" and W.covered(p, d))
        rate = 425 if d.year == 2025 else 438
        rows.append(["INV-%s" % d.strftime("%Y%m"), iso(d), n, money(rate), money(n * rate)])
        d = W.add_months(d, 1)
    _csv(t("admin_fees"), ["invoice_no", "billing_month", "employees_enrolled", "fee_per_employee", "invoice_amount"], rows)
