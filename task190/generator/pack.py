"""Cut the evidence pack."""
import csv
import datetime as dt
import os

import sim
import world as W

PULL = W.LEDGER_EXTRACT
BRANCH = None


def write_csv(target, name, header, rows):
    path = os.path.join(target, name)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return path


def enrich(lines, year=W.YEAR, seed=4471):
    """Give every payment line its references, supplier, run and date."""
    rng = sim.Rng(seed if year == W.YEAR else seed + 311)
    lo, hi = (W.YEAR_LO, W.YEAR_HI) if year == W.YEAR else (W.PRIOR_LO, W.PRIOR_HI)
    days = sim.dates(lo, hi)
    runs = []
    for i, d in enumerate(days):
        if d.weekday() not in (1, 4):             # payment runs go out Tuesdays and Fridays
            continue
        if d.isoformat() in W.HOLIDAYS:           # a public holiday: no run that day
            continue
        if d.isoformat() in W.MISSED_RUNS:        # the run did not go out, for its own reason
            continue
        runs.append(d)
    # a run's size is not uniform: the last run of a month clears the month's certified valuations
    # and the run after a missed one clears both weeks, so lines per run is a wide distribution
    wt = []
    for d in runs:
        nxt = [x for x in runs if x > d]
        w = 1.0
        if not nxt or nxt[0].month != d.month:
            w = 2.3
        elif (nxt[0] - d).days > 4:
            w = 1.7
        wt.append(w * (0.72 + 0.56 * ((sim.shash(d.isoformat()) % 1000) / 1000.0)))
    cw, acc = [], 0.0
    for w in wt:
        acc += w
        cw.append(acc)
    out = []
    inv = {}
    for n, L in enumerate(lines):
        code, amount, cls, taint = L
        import bisect
        day = runs[min(len(runs) - 1, bisect.bisect_left(cw, rng.u() * acc))]
        # several lines share an invoice: a certificate is one line, the rest group in twos and threes
        if cls == "certificate" or rng.u() < 0.42:
            iv = "INV-%s-%06d" % (year[2:], 1 + n * 3 + rng.below(3))
        else:
            key = (code, day)
            if key not in inv or rng.u() < 0.35:
                inv[key] = "INV-%s-%06d" % (year[2:], 1 + n * 3 + rng.below(3))
            iv = inv[key]
        sup = "S%05d" % (1100 + rng.below(380))
        out.append(dict(idx=n, code=code, amount=amount, cls=cls, taint=taint,
                        line="CPL-%s-%06d" % (year[2:], 10000 + n * 7 + rng.below(6)),
                        inv=iv, sup=sup, day=day,
                        run="PR-%s-%03d" % (year[2:], runs.index(day) + 1),
                        seq=0, status="paid", reverses="", delivery=1))
    # the ledger posts revenue and payroll lines in the same sequence, so an extract filtered to
    # the capital programme lines comes out with the gaps those left behind
    s = 0
    for r in out:
        s += 1 + (sim.shash("%s/seq/%d" % (year, r["idx"])) % 7 == 0) \
            + (sim.shash("%s/gap/%d" % (year, r["idx"])) % 23 == 0) * 3
        r["seq"] = s
    seen = set()
    for r in out:
        while r["line"] in seen:
            r["line"] = "CPL-%s-%06d" % (year[2:], int(r["line"][-6:]) + 1)
        seen.add(r["line"])
    return out, runs


def credit_notes(rows, rng):
    """Two payments reversed inside the year, and the lines that reverse them."""
    cand = [r for r in rows if r["cls"] == "sundry" and r["taint"] == 0
            and 2000 < r["amount"] < 40000]
    cand.sort(key=lambda r: r["line"])
    picked = [cand[len(cand) // 3], cand[(2 * len(cand)) // 3]]
    extra = []
    for i, r in enumerate(picked):
        r["status"] = "reversed"
        extra.append(dict(r, idx=-1, line="CPL-%s-9%05d" % (W.YEAR[2:], 1000 + i * 37),
                          amount=-r["amount"], status="credit_note", reverses=r["line"],
                          taint=0.0, cls="credit_note", seq=900000 + i,
                          day=r["day"] + dt.timedelta(days=21 + i * 9)))
    return extra, [r["line"] for r in picked]


def redelivered(rows, rng):
    """One payment run the bank feed delivered twice, with its own delivery sequence."""
    runs = {}
    for r in rows:
        runs.setdefault(r["run"], []).append(r)
    key = sorted(runs, key=lambda k: (abs(len(runs[k]) - 38), k))[0]
    dup = []
    for r in runs[key]:
        dup.append(dict(r, delivery=2))      # the same posting sequence, delivered again
    return dup, key, len(runs[key])


def write_lines(target, rows, year=W.YEAR):
    """The ledger extract, in the ledger's own posting sequence, which is how it comes out."""
    name = "capital_payment_lines_%s.csv" % year
    out = []
    for r in sorted(rows, key=lambda r: (r["seq"], r["delivery"])):
        out.append([r["seq"], r["line"], r["inv"], r["sup"], r["code"], "%.2f" % r["amount"],
                    r["day"].isoformat(), r["run"], r["status"], r["reverses"], r["delivery"]])
    return write_csv(target, name,
                     ["ledger_sequence", "line_ref", "invoice_ref", "supplier_no_ledger",
                      "programme_code", "amount_eur", "paid_date", "run_id", "line_status",
                      "reverses_line_ref", "delivery_sequence"], out)


# the revenue expenditure cost centres plan 4.4 tests, which are not on the capital register
REVENUE_CENTRES = ["RV-204", "RV-211", "RV-230", "RV-242"]


def revenue_sample(cross):
    """Internal audit's revenue expenditure sample, on the same working paper as the capital one.

    These are revenue ledger lines, not capital programme payment lines. They carry the revenue
    ledger's own reference prefix and a cost centre that is on no capital programme register, and
    they are in no capital extract. Nothing flags them as a different population: a reader finds
    them by joining the paper to the capital ledger and seeing which rows do not resolve.
    """
    import datetime as dt
    rng = sim.Rng(513377)
    out = []
    for k in range(17):
        day = dt.date(2026, 1, 1) + dt.timedelta(days=rng.below(360))
        amount = round(620.0 + rng.u() ** 2.2 * 48_000.0, 2)
        taint = 0.0 if rng.u() > 0.18 else round(0.09 + rng.u() * 0.14, 4)
        payable = round(amount * (1.0 - taint), 2)
        sup = sorted(cross.values())[rng.below(len(cross))]
        out.append(dict(code=REVENUE_CENTRES[k % len(REVENUE_CENTRES)], amount=amount,
                        payable=payable, taint=taint, day=day, cls="revenue",
                        line="REL-26-%06d" % (40_000 + k * 13 + rng.below(9)),
                        sup=sup, schedule_ref="%s/REL-26-%06d" % (sup, 40_000 + k * 13),
                        finding=("supporting order not produced" if taint > 0
                                 else "agreed to the order, no exception")))
    for i, r in enumerate(out):
        r["schedule_ref"] = "%s/%s" % (r["sup"], r["line"])
    return out


def write_programme_register(target):
    rows = []
    direc = {"CP-11": "Marine", "CP-14": "Marine", "CP-31": "Marine",
             "CP-21": "Terminals", "CP-23": "Terminals", "CP-44": "Terminals",
             "CP-34": "Estate", "CP-41": "Estate", "CP-47": "Estate"}
    for code, name, value, certs in W.PROGRAMMES:
        start, done = W.PROG_DATES[code]
        rows.append([code, name, direc[code],
                     "%d" % int(round(W.APPROVED_BUDGET[code] / 1000.0)), start, done])
    return write_csv(target, "capital_programme_register.csv",
                     ["programme_code", "programme_name", "directorate",
                      "approved_budget_eur_thousands", "start_date", "planned_completion"], rows)


def write_crosswalk(target, rows):
    sups = sorted({r["sup"] for r in rows})
    out = []
    rng = sim.Rng(81127)
    # the master's numbers were issued by a different system over years, in blocks as trades were
    # migrated, so they do not step from the ledger's by any stride
    blocks = [410000, 412000, 415000, 418000, 421000, 426000, 431000]
    for s in sups:
        b = blocks[sim.shash("blk/%s" % s) % len(blocks)]
        out.append([s, "SUP%06d" % (b + sim.shash("sup/%s" % s) % 1900)])
    seen = set()
    for r in out:
        while r[1] in seen:
            r[1] = "SUP%06d" % (int(r[1][3:]) + 1)
        seen.add(r[1])
    return write_csv(target, "supplier_number_crosswalk.csv",
                     ["supplier_no_ledger", "supplier_no_master"], out), dict(out)


SURNAMES = ["Breen", "Corrigan", "Delahunty", "Fitzmaurice", "Gallagher", "Hanafin", "Kiely",
            "Lenihan", "Mescall", "Nolan", "O'Donovan", "Prendergast", "Quigley", "Ruane",
            "Scannell", "Tierney", "Whelan", "Hourihane", "Coughlan", "Mulcahy"]
TRADES = ["Plant Hire", "Civil Engineering", "Marine Services", "Electrical Contracting",
          "Steel Fabrication", "Surfacing", "Dredging", "Scaffolding", "Joinery",
          "Security Systems", "Groundworks", "Mechanical Services", "Quarry Products",
          "Crane Hire", "Formwork", "Piling", "Drainage", "Roofing"]
PLACES = ["Ardfinnan", "Ballyhaunis", "Clonakilty", "Drumshanbo", "Eyeries", "Farranfore",
          "Glenbeigh", "Headford", "Inchigeela", "Kilmacthomas", "Leenane", "Moyvore",
          "Newmarket", "Oranmore", "Portumna", "Rathdowney", "Skibbereen", "Tullamore"]
SUFFIX = ["Limited", "Limited", "Limited", "Ltd", "& Sons Limited", "Group Limited",
          "(Ireland) Limited", "Contractors Limited"]


def _supplier_name(rng, used):
    """A supplier register is a mix of family firms, trade names and place names, not a grid."""
    for _ in range(40):
        u = rng.u()
        if u < 0.42:
            nm = "%s %s" % (SURNAMES[rng.below(len(SURNAMES))], SUFFIX[rng.below(len(SUFFIX))])
        elif u < 0.74:
            nm = "%s %s %s" % (PLACES[rng.below(len(PLACES))], TRADES[rng.below(len(TRADES))],
                               SUFFIX[rng.below(len(SUFFIX))])
        elif u < 0.90:
            nm = "%s %s" % (TRADES[rng.below(len(TRADES))], SUFFIX[rng.below(len(SUFFIX))])
        else:
            nm = "%s %s %s" % (SURNAMES[rng.below(len(SURNAMES))],
                               TRADES[rng.below(len(TRADES))], SUFFIX[rng.below(len(SUFFIX))])
        if nm not in used:
            used.add(nm)
            return nm
    return nm


def write_supplier_master(target, cross, cats, groups=None):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Suppliers"
    ws["A1"] = "%s: supplier master" % W.AUTHORITY
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Extracted %s. Risk categories were relabelled on %s; the map is in " \
               "supplier_risk_category_map.csv." % (PULL, W.RISK_RELABEL)
    ws["A2"].font = Font(size=9, italic=True)
    head = ["supplier_no_master", "supplier_name", "group_parent_no", "risk_category_current",
            "approved_from", "trading_status"]
    for j, h in enumerate(head):
        c = ws.cell(row=4, column=1 + j, value=h)
        c.font = Font(bold=True)
    rng = sim.Rng(55219)
    first = ["Ardfinnan", "Ballyhaunis", "Clonakilty", "Drumshanbo", "Eyeries", "Farranfore",
             "Glenbeigh", "Headford", "Inchigeela", "Kilmacthomas", "Leenane", "Moyvore",
             "Newmarket", "Oranmore", "Portumna", "Rathdowney", "Skibbereen", "Tullamore"]
    last = ["Plant Hire", "Civil Works", "Marine Services", "Electrical", "Steel Fabrication",
            "Surfacing", "Dredging", "Scaffolding", "Joinery", "Security Systems",
            "Groundworks", "Mechanical"]
    used = set()
    for i, (led, mas) in enumerate(sorted(cross.items())):
        nm = _supplier_name(rng, used)
        parent = (groups or {}).get(mas) or None
        ws.cell(row=5 + i, column=1, value=mas)
        ws.cell(row=5 + i, column=2, value=nm)
        ws.cell(row=5 + i, column=3, value=parent)
        ws.cell(row=5 + i, column=4,
                value=cats.get(parent or mas, cats.get(mas, "R-C")))
        ws.cell(row=5 + i, column=5,
                value=(dt.date(2019, 1, 7) + dt.timedelta(days=rng.below(2500))).isoformat())
        ws.cell(row=5 + i, column=6, value="active" if rng.u() < 0.93 else "dormant")
    for col, wd in (("A", 20), ("B", 40), ("C", 18), ("D", 20), ("E", 16), ("F", 16)):
        ws.column_dimensions[col].width = wd
    path = os.path.join(target, "supplier_master.xlsx")
    wb.save(path)
    return path


def write_dictionary(target):
    rows = [
        ("capital_payment_lines_2026.csv", "ledger_sequence", "The ledger's own posting sequence for the line. The extract comes out in this order."),
        ("capital_payment_lines_2026.csv", "line_ref", "The payment ledger's reference for one payment line."),
        ("capital_payment_lines_2026.csv", "invoice_ref", "The invoice the line pays. Several lines may pay one invoice."),
        ("capital_payment_lines_2026.csv", "amount_eur", "Euro and cents as recorded in the ledger. Negative on a credit note."),
        ("capital_payment_lines_2026.csv", "paid_date", "The date of the payment run that paid the line."),
        ("capital_payment_lines_2026.csv", "line_status", "paid, reversed where a credit note later reversed the line, or credit_note on the reversing line itself."),
        ("capital_payment_lines_2026.csv", "reverses_line_ref", "The line_ref this credit note reverses, where the ledger recorded one."),
        ("capital_payment_lines_2026.csv", "delivery_sequence", "The bank feed's delivery sequence for the line: 1 on the first delivery, 2 and up where the feed delivered it again."),
        ("capital_payment_lines_2026.csv", "supplier_no_ledger", "The ledger's supplier number. The supplier master uses its own; supplier_number_crosswalk.csv links them."),
        ("capital_programme_register.csv", "approved_budget_eur_thousands", "Thousands of euro, as the capital programme board approves them. Every other file states euro and cents."),
        ("internal_audit_testing_schedule_2026.pdf", "schedule_ref", "Internal audit's own reference for a tested line: the supplier number on the supplier master, then the ledger line reference."),
        ("internal_audit_testing_schedule_2026.pdf", "date_released", "The date the payment run carrying the line was released, as the payment run log records it."),
        ("internal_audit_testing_schedule_2026.pdf", "amount_properly_payable", "The amount the testing established was properly payable on the line. Equal to the recorded amount where the testing found nothing."),
        ("testing_schedule_extract_2025_2026.csv", "testing_year", "The year of the testing the row belongs to. The extract holds two years and was pulled once."),
        ("payment_run_log_2026.csv", "released_ts", "The time the run was released, in authority local time. A run whose release ran past midnight carries the following day's date."),
        ("payment_run_log_2026.csv", "reversed_value_eur", "The value of the run's lines later reversed by credit note, as a negative."),
        ("payment_release_cutoff_register.xlsx", "cutoff_time", "The latest release time for a run on the day. A run released at the cut-off is within it."),
        ("supplier_risk_approval_history.csv", "event_status", "accepted where the row is the approval register's record of the event, superseded where a later correction replaced it."),
        ("supplier_risk_approval_history.csv", "category_after", "The category the event moved the supplier to. Per supplier, the category moves one way across the year and never returns to a category that supplier has left."),
        ("supplier_master.xlsx", "group_parent_no", "Where the supplier is part of a trading group, the master number of the group's parent. Blank where the supplier is its own entity."),
        ("supplier_master.xlsx", "risk_category_current", "The category in force at the extract date, under the labelling from 1 October 2026."),
        ("grant_claim_2026.csv", "claim_period", "The funder's claim year, which runs to 31 March and is not the authority's financial year."),
    ]
    return write_csv(target, "field_dictionary.csv", ["file", "field", "definition"],
                     [[a, b, c] for a, b, c in rows])


def write_manifest(target, stats):
    rows = [
        ["capital_payment_lines_2026.csv", "Capital programme payment lines", "Year to 31 December 2026", "", "Payment ledger"],
        ["capital_payment_lines_2025.csv", "Capital programme payment lines", "Year to 31 December 2025", "", "Payment ledger"],
        ["internal_audit_testing_schedule_2026.pdf", "Internal audit testing schedule", "Year to 31 December 2026", "", "Internal audit"],
        ["testing_schedule_extract_2025_2026.csv", "Testing schedule extract, two years", "2025 and 2026", "", "Internal audit"],
        ["capital_programme_register.csv", "Capital programme register", "Current", "Thousands of euro", "Capital programme board"],
        ["supplier_master.xlsx", "Supplier master", "Extract date", "", "Procurement"],
        ["supplier_number_crosswalk.csv", "Ledger to master supplier numbers", "Current", "", "Finance systems"],
        ["payment_run_log_2026.csv", "Payment run log", "Year to 31 December 2026", "", "Finance operations"],
        ["payment_release_cutoff_register.xlsx", "Payment release cut-off register", "Current", "", "Finance operations"],
        ["supplier_risk_approval_history.csv", "Supplier risk approval history", "Year to 31 December 2026", "", "Procurement"],
        ["supplier_risk_category_map.csv", "Risk category labelling map", "From 1 October 2026", "", "Procurement"],
        ["audit_plan_2026.pdf", "Internal audit plan, section 4", "Year to 31 December 2026", "", "Internal audit"],
        ["audit_manual_part9.pdf", "Internal audit manual, part 9", "Current", "", "Internal audit"],
        ["grant_claim_2026.csv", "Funder grant claim", "Claim year to 31 March", "", "Finance"],
        ["revenue_expenditure_summary_2026.csv", "Revenue expenditure summary", "Year to 31 December 2026", "", "Finance"],
        ["field_dictionary.csv", "Field definitions across the extracts", "All files", "", "Finance systems"],
        ["provenance.md", "Extract notes for this cut", "All files", "", "Internal audit"],
        ["export_manifest.csv", "This manifest", "All files", "", "Internal audit"],
    ]
    return write_csv(target, "export_manifest.csv",
                     ["file", "contents", "period", "units", "source_system"], rows)


def write_provenance(target, stats):
    txt = """# Extract notes, internal audit

These files were pulled for the internal audit of the capital programme payments population for the year
to 31 December 2026. The payment ledger was extracted on %(pull)s and the testing was completed on
%(done)s. They are the authority's own records and are held under the retention rule in part 12 of the
internal audit manual.

| extract | source system | pulled |
|---|---|---|
| capital payment lines, both years | payment ledger | %(pull)s |
| testing schedule and its two-year extract | internal audit working papers | %(done)s |
| capital programme register | capital programme board papers | %(pull)s |
| supplier master and crosswalk | procurement and finance systems | %(pull)s |
| payment run log and cut-off register | finance operations | %(pull)s |
| supplier risk approval history and category map | procurement | %(pull)s |
| grant claim and revenue expenditure summary | finance | %(pull)s |

The payment ledger carries %(lines)s payment lines for the reporting year, two of which are credit notes. It is joined to the supplier master on
`supplier_no_ledger` through `supplier_number_crosswalk.csv`; the programme sits on every payment line.
Field definitions are in `field_dictionary.csv`.

The capital programme register states approved budgets in thousands of euro, which is how the board
approves them; every other file states euro and cents. Extracts are pulled once, after the year closes,
and are not re-pulled.
""" % dict(pull=PULL, done=W.TESTING_DONE, lines=format(stats["lines"], ","))
    path = os.path.join(target, "provenance.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(txt)
    return path
