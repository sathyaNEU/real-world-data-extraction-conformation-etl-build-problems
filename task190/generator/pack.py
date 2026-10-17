"""The bundle: the two deposit feeds, the registers, the dictionary and the context files."""
import csv
import datetime as dt
import os

import sim
import world as W

PULL = W.EXTRACT
DST = (dt.date(2026, 9, 27), dt.date(2027, 4, 4))     # NZDT in the reporting year


def write_csv(target, name, header, rows, nl="\r\n"):
    path = os.path.join(target, name)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator=nl)
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)
    return path


def offset(day):
    return 13 if DST[0] <= day < DST[1] else 12


def utc_stamp(day, hhmm, sec=0):
    local = dt.datetime(day.year, day.month, day.day, hhmm // 60, hhmm % 60, sec)
    return (local - dt.timedelta(hours=offset(day))).strftime("%Y-%m-%dT%H:%M:%SZ")


def shash_local(text):
    h = 2166136261
    for ch in text:
        h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    return h


def machines_on(day):
    """The machines in service at each site on a day."""
    out = {}
    for mid, site, inst, wdr in W.MACHINES:
        a = dt.date(*[int(v) for v in inst.split("-")])
        b = dt.date(*[int(v) for v in wdr.split("-")]) if wdr else None
        if a <= day and (b is None or day < b):
            out.setdefault(site, []).append(mid)
    return out


def enrich(custs, rows):
    """Give every deposit its reference, branch, clock and instrument."""
    rng = sim.Rng(880517)
    bycust = {c["cust"]: c for c in custs}
    # the deposit system's own customer number, which is not the master's
    acct = {}
    for i, c in enumerate(sorted(custs, key=lambda x: x["cust"])):
        acct[c["cust"]] = "%s-%05d" % (c["branch"][2:], 1301 + i * 3 + rng.below(3))
    seq = {"counter": 0, "machine": 0}
    tellers = {}
    for code, _n, _r, _o, _c in W.BRANCHES:
        tellers[code] = 6 + (shash_local(code) % 13)
    out = []
    for r in rows:
        c = bycust[r["cust"]]
        day = r["date"]
        br = c["branch"]
        if br == "AR11" and day >= dt.date(2026, 11, 27):
            br = "AR12"
        if rng.u() < 0.035:                       # paid in at another branch
            br = rng.pick([b[0] for b in W.BRANCHES if b[0] != br and
                            (b[4] == "" or day < dt.date(*[int(v) for v in b[4].split("-")]))])
        # counters are busiest mid morning and again at close; machines run later
        u = rng.u()
        if u < 0.34:
            hhmm = 9 * 60 + rng.below(100)
        elif u < 0.62:
            hhmm = 11 * 60 + rng.below(150)
        elif u < 0.86:
            hhmm = 14 * 60 + rng.below(140)
        else:
            hhmm = 16 * 60 + 20 + rng.below(110)
        here = machines_on(day).get(br, [])
        if r["channel"] == "machine" and not here:
            r = dict(r, channel="counter")
        if r["channel"] == "counter":
            seq["counter"] += 1
            out.append(dict(kind="counter",
                            ref="CD%07d" % (4100000 + seq["counter"] * 3 + rng.below(3)),
                            branch=br, teller="T%s%02d" % (br[2:], 1 + rng.below(tellers[br])),
                            acct=acct[r["cust"]], instrument="cash", amount=r["amount"],
                            day=day, hhmm=hhmm, sec=rng.below(60), cust=r["cust"], year=r["year"],
                            planted=r["planted"], resent=0))
        else:
            seq["machine"] += 1
            if rng.u() < 0.22:
                hhmm = min(19 * 60, hhmm + 120 + rng.below(90))
            out.append(dict(kind="machine",
                            ref="MD%07d" % (6200000 + seq["machine"] * 7 + rng.below(5)),
                            branch=br, machine=rng.pick(here),
                            acct=acct[r["cust"]], instrument="cash", amount=r["amount"],
                            day=day, hhmm=hhmm, sec=rng.below(60), cust=r["cust"], year=r["year"],
                            planted=r["planted"], resent=0))
    # no machine deposit in the band sits on a year boundary, so reading the UTC stamp as the
    # deposit date never moves the figure (SF9)
    for d in out:
        if d["kind"] == "machine" and W.BAND_LO <= d["amount"] < W.BAND_HI and \
                d["day"] in (dt.date(2026, 7, 1), dt.date(2027, 6, 30), dt.date(2025, 7, 1),
                             dt.date(2026, 6, 30)):
            d["day"] = d["day"] + dt.timedelta(days=2 if d["day"].day == 1 else -2)
        if d["kind"] == "machine" and d["hhmm"] < 8 * 60 + 30:
            d["hhmm"] = 8 * 60 + 30 + rng.below(120)
    return out, acct


def other_instruments(deposits, rng):
    """Cheque and electronic credits, which clause 7.4's count is not of."""
    extra = []
    n = 0
    for d in deposits:
        if d["kind"] != "counter":
            continue
        if rng.u() < 0.145:
            n += 1
            inst = "cheque" if rng.u() < 0.56 else "credit"
            amt = round(400 + rng.u() ** 1.6 * 26000, 2)
            extra.append(dict(d, ref="CD%07d" % (4800000 + n * 3), instrument=inst,
                              amount=amt, planted=0, resent=0))
    return extra


def write_feeds(target, deposits):
    rng = sim.Rng(20260714)
    counter = [d for d in deposits if d["kind"] == "counter"]
    machine = [d for d in deposits if d["kind"] == "machine"]
    counter = counter + other_instruments(deposits, rng)
    counter.sort(key=lambda d: (d["day"], d["hhmm"], d["ref"]))
    machine.sort(key=lambda d: (d["day"], d["hhmm"], d["ref"]))

    # two reversals, neither in the band, each with its own reversing row
    rev = []
    for d in counter:
        if len(rev) < 2 and d["instrument"] == "cash" and d["amount"] > 16000 and \
                d["year"] == "2027":
            rev.append(d)
    rev_rows = []
    for d in rev:
        rev_rows.append(dict(d, ref="CD%07d" % (4900000 + len(rev_rows) * 3),
                             amount=-d["amount"], reversal_of=d["ref"]))
    hdr = ["deposit_ref", "branch_code", "teller_id", "acct_customer_no", "instrument",
           "amount_nzd", "deposit_date", "deposit_time_local", "posted_date", "reversal_of",
           "pull_date"]
    rows = []
    posted_shift = 0
    for d in counter + rev_rows:
        day = d["day"]
        posted = day
        if rng.u() < 0.0068 and not (W.BAND_LO <= d["amount"] < W.BAND_HI):
            posted = day + dt.timedelta(days=1)
            posted_shift += 1
        rows.append([d["ref"], d["branch"], d["teller"], d["acct"], d["instrument"],
                     "%.2f" % d["amount"], day.isoformat(),
                     "%02d:%02d:%02d" % (d["hhmm"] // 60, d["hhmm"] % 60, d.get("sec", 0)),
                     posted.isoformat(),
                     d.get("reversal_of", ""), PULL])
    write_csv(target, "cash_deposit_counter_2026_2027.csv", hdr, rows)

    # the machine feed: UTC stamps, its own sequence, and a few re-sent rows outside the
    # amount range any profile is read over, so a kept duplicate moves no figure
    hdr2 = ["machine_deposit_ref", "machine_id", "site_code", "acct_customer_no", "amount_nzd",
            "deposit_ts_utc", "envelope_count", "pull_sequence", "pull_date"]
    rows2 = []
    resent = 0
    for d in machine:
        base = [d["ref"], d["machine"], d["branch"], d["acct"], "%.2f" % d["amount"],
                utc_stamp(d["day"], d["hhmm"], d.get("sec", 0)),
                1 + (1 if rng.u() < 0.21 else 0) + (1 if rng.u() < 0.06 else 0)]
        rows2.append(base + [1, PULL])
        if (d["amount"] < 4600 or d["amount"] > 17000) and rng.u() < 0.004:
            rows2.append(base + [2, PULL])
            resent += 1
    write_csv(target, "cash_deposit_machine_2026_2027.csv", hdr2, rows2)
    return dict(counter=len(rows), machine=len(rows2), resent=resent,
                posted_shift=posted_shift, reversals=[r["reversal_of"] for r in rev_rows],
                reversed_keys=[(d["cust"], d["day"], round(d["amount"], 2)) for d in rev],
                other=len(counter) - len([d for d in deposits if d["kind"] == "counter"]))


def write_register(target, custs, acct):
    """The business banking register as the relationship team keeps it: a wide workbook."""
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Business register"
    ws["A1"] = "%s: business banking customer register" % W.BANK
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Extract %s. One row per customer on the register at 30 June 2027." % PULL
    ws["A2"].font = Font(size=9, italic=True)
    ws["A3"] = "Segment codes were reissued on %s; both codings are shown." % W.RECODE_DATE
    ws["A3"].font = Font(size=9, italic=True)
    head = ["master_customer_no", "trading_name", "segment_code_current",
            "segment_code_to_2027_04_05", "segment_name", "home_branch_code",
            "relationship_opened", "anzsic_code"]
    for j, h in enumerate(head):
        c = ws.cell(row=5, column=1 + j, value=h)
        c.font = Font(bold=True)
        c.alignment = Alignment(horizontal="left")
    rng = sim.Rng(771103)
    FIRST = ["Kowhai", "Rimu", "Totara", "Waiata", "Harbourside", "Clearwater", "Northvale",
             "Sunnybank", "Riverton", "Fernhill", "Tussock", "Kererū", "Oakfield", "Mataī",
             "Springvale", "Eastgate", "Westbrook", "Pukeko", "Highfield", "Karaka"]
    SECOND = {"GRO": ["Food Market", "Superette", "Grocers", "Convenience", "Fresh Mart"],
              "HOS": ["Cafe", "Bistro", "Tavern", "Eatery", "Dining Rooms"],
              "TRA": ["Couriers", "Transport", "Freight", "Cabs", "Haulage"],
              "CON": ["Builders", "Plumbing", "Roofing", "Electrical", "Contracting"],
              "RUR": ["Rural Supplies", "Orchards", "Produce", "Farm Services", "Growers"],
              "FUE": ["Service Station", "Autos", "Motors", "Fuel Stop", "Tyres"],
              "PER": ["Hair Studio", "Barbers", "Beauty Rooms", "Laundry", "Clinic"],
              "CLB": ["Bowling Club", "Rugby Club", "Community Trust", "Social Club", "Hall"]}
    rows = []
    for c in sorted(custs, key=lambda x: x["cust"]):
        nm = "%s %s" % (rng.pick(FIRST), rng.pick(SECOND[c["seg"]]))
        if rng.u() < 0.22:
            nm += " Limited"
        rows.append([c["cust"], nm, W.NEW_CODE[c["seg"]], W.OLD_CODE[c["seg"]],
                     W.SEG_NAME[c["seg"]], c["branch"], c["opened"],
                     rng.pick(W.ANZSIC[c["seg"]])])
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            ws.cell(row=6 + i, column=1 + j, value=v)
    for col, wd in (("A", 18), ("B", 30), ("C", 20), ("D", 24), ("E", 30), ("F", 18),
                    ("G", 20), ("H", 14)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A6"
    path = os.path.join(target, "business_customer_register.xlsx")
    wb.save(path)
    return path, rows


def write_crosswalk(target, custs, acct):
    rows = []
    for c in sorted(custs, key=lambda x: x["cust"]):
        rows.append([acct[c["cust"]], c["cust"], "active", PULL])
    return write_csv(target, "customer_number_crosswalk.csv",
                     ["acct_customer_no", "master_customer_no", "link_status", "pull_date"], rows)


def write_branches(target):
    rows = []
    for code, name, region, opened, closed in W.BRANCHES:
        nm, newreg, when = W.RENAMED.get(code, (name, region, ""))
        rows.append([code, name, region, opened, closed,
                     W.MERGED_INTO.get(code, ""), nm if when else "", when])
    return write_csv(target, "branch_register.csv",
                     ["branch_code", "branch_name", "region", "opened", "closed",
                      "deposits_transferred_to", "renamed_to", "renamed_on"], rows)


def write_machine_register(target):
    """The property team's register of the smart deposit machine estate."""
    rows = []
    for mid, site, inst, wdr in W.MACHINES:
        rows.append([mid, site, inst, wdr, "NoteSafe 6200" if mid < "SDM-1100" else "NoteSafe 7100"])
    return write_csv(target, "deposit_machine_register.csv",
                     ["machine_id", "site_code", "installed_on", "withdrawn_on", "model"], rows)


def write_summary(target, deposits):
    """The branch cash summary the operations desk reconciles to: amounts, never band counts."""
    agg = {}
    for d in deposits:
        if d["instrument"] != "cash" or d["year"] != "2027":
            continue
        key = (d["branch"], d["day"].strftime("%Y-%m"))
        a = agg.setdefault(key, [0, 0.0])
        a[0] += 1
        a[1] += d["amount"]
    rows = [[b, m, n, "%.2f" % v] for (b, m), (n, v) in sorted(agg.items())]
    return write_csv(target, "branch_cash_summary_2027.csv",
                     ["branch_code", "month", "cash_deposits", "cash_paid_in_nzd"], rows)


def write_ptr(target, deposits):
    """Prescribed transaction reports: cash at or above the threshold. Never read by the figure."""
    rng = sim.Rng(50312)
    at_or_over = [d for d in deposits
                  if d["instrument"] == "cash" and d["amount"] >= W.THRESHOLD and
                  d["year"] == "2027"]
    at_or_over.sort(key=lambda d: (d["day"], d["ref"]))
    hdr = ["ptr_reference", "deposit_ref", "acct_customer_no", "amount_nzd", "transaction_date",
           "reported_on", "extract_status"]
    pre, rev = [], []
    for i, d in enumerate(at_or_over):
        rep = d["day"] + dt.timedelta(days=3 + rng.below(8))
        row = ["PTR2027%05d" % (i * 2 + 11), d["ref"], d["acct"], "%.2f" % d["amount"],
               d["day"].isoformat(), rep.isoformat()]
        if d["day"] <= dt.date(2027, 5, 16):
            pre.append(row + ["preliminary"])
        if d["day"] >= dt.date(2027, 4, 6):
            rev.append(row + ["revised"])
    write_csv(target, "prescribed_transaction_extract_preliminary.csv", hdr, pre)
    write_csv(target, "prescribed_transaction_extract_revised.csv", hdr, rev)
    return len(pre), len(rev), len(at_or_over)


def write_card(target, custs):
    """Merchant card settlements: the obvious way to judge a cash take, and never read."""
    rng = sim.Rng(66109)
    rows = []
    for c in sorted(custs, key=lambda x: x["cust"]):
        if rng.u() > 0.46:
            continue
        start = rng.below(3) if rng.u() < 0.18 else 0
        stop = 12 - (rng.below(3) if rng.u() < 0.12 else 0)
        term = 1 + rng.below(3)
        for m in range(start, stop):
            if rng.u() < 0.05:
                continue
            y, mm = (2026, 7 + m) if 7 + m <= 12 else (2027, 7 + m - 12)
            rows.append([c["cust"], "%04d-%02d" % (y, mm),
                         "%.2f" % round(c["weight"] * (2400 + rng.u() * 9000), 2), term])
    return write_csv(target, "card_settlement_summary_2027.csv",
                     ["master_customer_no", "month", "card_settled_nzd", "terminals"], rows)


DICT = [
    ("cash_deposit_counter_2026_2027.csv", "deposit_ref", "The teller system's reference for one deposit. Unique."),
    ("cash_deposit_counter_2026_2027.csv", "instrument", "cash, cheque or credit. Cash is notes and coin counted at the counter."),
    ("cash_deposit_counter_2026_2027.csv", "amount_nzd", "New Zealand dollars and cents as counted. Negative on a reversing row."),
    ("cash_deposit_counter_2026_2027.csv", "deposit_date", "The date the deposit was paid in, in branch local time."),
    ("cash_deposit_counter_2026_2027.csv", "deposit_time_local", "Branch local time, 24 hour."),
    ("cash_deposit_counter_2026_2027.csv", "posted_date", "The date the ledger run picked the deposit up. Later than the deposit date where a run was missed."),
    ("cash_deposit_counter_2026_2027.csv", "reversal_of", "The deposit_ref this row reverses. Blank on an ordinary row."),
    ("cash_deposit_counter_2026_2027.csv", "acct_customer_no", "The deposit system's customer number, branch prefixed. Not the master number."),
    ("cash_deposit_machine_2026_2027.csv", "machine_deposit_ref", "The smart deposit machine's reference for one deposit."),
    ("cash_deposit_machine_2026_2027.csv", "amount_nzd", "Dollars and cents as counted by the machine. Cash only; the machines take no other instrument."),
    ("cash_deposit_machine_2026_2027.csv", "deposit_ts_utc", "Coordinated Universal Time, as the machine estate stamps it. New Zealand local time is twelve hours ahead, thirteen in daylight saving."),
    ("cash_deposit_machine_2026_2027.csv", "envelope_count", "How many envelopes the customer fed in for this deposit. One deposit, whatever the count."),
    ("cash_deposit_machine_2026_2027.csv", "pull_sequence", "1 on the first delivery of a row, 2 where the estate re-sent it. A row is one deposit however many times it was delivered."),
    ("business_customer_register.xlsx", "segment_code_current", "The segment code in force at the extract date. Codes were reissued on 6 April 2027; the segments themselves did not change."),
    ("business_customer_register.xlsx", "segment_code_to_2027_04_05", "The code the same segment carried until 5 April 2027."),
    ("business_customer_register.xlsx", "master_customer_no", "The customer master's number. Deposits carry the deposit system's number; customer_number_crosswalk.csv links them."),
    ("branch_register.csv", "deposits_transferred_to", "Where a closed branch's deposits are taken up from the closing date."),
    ("till_balance_log_2026_2027.csv", "session_opened_ts", "Counter sessions are stamped in branch local time; machine collection sessions are stamped in UTC. collection_source says which."),
    ("till_balance_log_2026_2027.csv", "variance_nzd", "Counted cash less the system's expected balance. Negative is a shortage."),
    ("risk_rating_history.csv", "load_ts", "When the rating event reached the register. Two events may share an effective date; the later load is the one the register accepted."),
    ("risk_rating_history.csv", "event_status", "accepted or superseded. A superseded event was replaced by a correction carrying the same effective date."),
    ("machine_service_log_2027.csv", "machine_id", "One machine, as deposit_machine_register.csv names it. The vendor reports by site, summing the machines a site runs."),
    ("deposit_machine_register.csv", "installed_on", "The day the machine went into service at the site."),
    ("deposit_machine_register.csv", "withdrawn_on", "The day the machine came out of service. Blank where it is still in service at the extract date."),
    ("machine_service_log_2027.csv", "out_of_service_minutes", "Minutes unavailable in this incident. A machine with no row in a month had no incident recorded; a decommissioned machine has no rows at all."),
]


def write_dictionary(target):
    return write_csv(target, "field_dictionary.csv", ["file", "field", "definition"],
                     [[a, b, c] for a, b, c in DICT])


def write_manifest(target, stats):
    rows = [
        ["cash_deposit_counter_2026_2027.csv", "Teller cash and non-cash deposits, both reporting years",
         "1 July 2025 to 30 June 2027", "Machine deposits; deposits at closed branches after closure", "Teller system extract, pulled %s" % PULL],
        ["cash_deposit_machine_2026_2027.csv", "Smart deposit machine deposits, both reporting years",
         "1 July 2025 to 30 June 2027", "Counter deposits; non-cash instruments", "Machine estate extract, pulled %s" % PULL],
        ["business_customer_register.xlsx", "Business banking customers on the register at 30 June 2027",
         "At 30 June 2027", "Closed relationships", "Relationship management extract"],
        ["customer_number_crosswalk.csv", "Deposit system number to master number",
         "Active links at the pull date", "Links closed before July 2025", "Customer master extract"],
        ["branch_register.csv", "Branch estate with effective dates", "All branches", "Agencies and mobile units", "Property and estate register"],
        ["branch_cash_summary_2027.csv", "Cash paid in by branch and month", "Reporting year 2026/27", "Non-cash instruments", "Operations desk reconciliation pack"],
        ["prescribed_transaction_extract_preliminary.csv", "Cash transactions at or above the threshold, first extract",
         "1 July 2026 to 16 May 2027", "Transactions below the threshold", "Reporting engine, preliminary run"],
        ["prescribed_transaction_extract_revised.csv", "Cash transactions at or above the threshold, revised extract",
         "6 April 2027 to 30 June 2027", "Transactions below the threshold", "Reporting engine, revised run; supersedes the preliminary for the overlap"],
        ["card_settlement_summary_2027.csv", "Merchant card settlements by customer and month", "Reporting year 2026/27", "Customers without a merchant facility", "Merchant acquiring extract"],
        ["till_balance_log_2026_2027.csv", "Cash count sessions by branch", "1 July 2025 to 30 June 2027", "Sessions voided before completion", "Branch operations log"],
        ["cash_tolerance_register.xlsx", "Variance tolerances with effective dates", "All branches", "", "Branch operations standards"],
        ["risk_rating_history.csv", "Customer risk rating events", "Reporting year 2026/27", "Customers never rated", "Financial crime register"],
        ["rating_scale_map.csv", "Rating scale before and after the April 2027 relabel", "All bands", "", "Financial crime register"],
        ["machine_service_log_2027.csv", "Deposit machine service incidents", "Reporting year 2026/27", "Calls closed without an engineer attending", "Machine estate service log"],
        ["deposit_machine_register.csv", "The smart deposit machine estate with service dates", "At 19 July 2027", "Branch counters", "Property and estate register"],
        ["field_dictionary.csv", "Field definitions across the extracts", "All files", "", "Data management"],
        ["aml_programme_handbook.pdf", "Programme handbook part 7, reporting", "Version 9.2, approved 14 May 2026", "Parts 1 to 6 and 8", "Financial crime policy"],
        ["annual_report_extract_2026.pdf", "Extract of last year's filed annual report", "Year ended 30 June 2026", "Sections other than 2 and 5", "Filed copy held by the financial crime team"],
        ["vendor_service_report_2027.pdf", "Machine estate service report by site", "Reporting year 2026/27", "Machines withdrawn under the estate refresh", "Kaituna Cash Systems, contract ACS-4471"],
        ["provenance.md", "Extract notes for this cut", "All files", "", "Financial crime data team"],
    ]
    return write_csv(target, "export_manifest.csv",
                     ["file", "what_it_is", "covers", "omits", "how_it_was_made"], rows)


def write_provenance(target, stats):
    txt = """# Extract notes, financial crime data team

These files were pulled on %(pull)s for the annual report for the year ended 30 June 2027 and cover the
reporting years ended 30 June 2026 and 30 June 2027 unless `export_manifest.csv` says otherwise. They are
the bank's own records and are held under the retention rule at paragraph 9.1 of the programme handbook.
Nothing here may leave the financial crime team without the reporting officer's approval.

The teller feed carries %(counter)d rows and the machine feed %(machine)d. The two are joined on
`acct_customer_no` through `customer_number_crosswalk.csv`; neither feed carries a segment, which sits on
the customer register.

Known limits of this cut:

- The machine estate re-sent %(resent)d rows during the year. A re-sent row carries `pull_sequence` 2 and
  repeats the reference of the row already delivered.
- %(posted)d counter deposits have a posted date one day later than the deposit date, which is the
  overnight ledger run being missed.
- The branch at Hastings Heretaunga (AR11) closed on 27 November 2026 and its deposits are taken up at
  AR12 from that date. AR12 was renamed on the same day.
- Segment codes were reissued on %(recode)s. The register carries the current code and the one in force
  to 5 April 2027.
- The prescribed transaction extract was re-run on 18 May 2027 after a reporting engine upgrade. The two
  extracts overlap from 6 April to 16 May 2027; the revised run supersedes the preliminary one.
- The machine estate stamps in Coordinated Universal Time and the teller system in branch local time.
""" % dict(pull=PULL, counter=stats["counter"], machine=stats["machine"],
           resent=stats["resent"], posted=stats["posted_shift"], recode=W.RECODE_DATE)
    path = os.path.join(target, "provenance.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(txt)
    return path
