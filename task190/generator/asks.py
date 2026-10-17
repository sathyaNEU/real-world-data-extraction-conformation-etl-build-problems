"""The three supplemental asks and the files that carry them."""
import datetime as dt
import os

import pack as PK
import sim
import world as W

QUARTERS = [("2026Q1", "2026-01-01", "2026-03-31"), ("2026Q2", "2026-04-01", "2026-06-30"),
            ("2026Q3", "2026-07-01", "2026-09-30"), ("2026Q4", "2026-10-01", "2026-12-31")]


def _q(day):
    for name, lo, hi in QUARTERS:
        if lo <= day.isoformat() <= hi:
            return name
    return None


def cutoff_for(day):
    for lo, hi, t in W.CUTOFF:
        if lo <= day.isoformat() and (not hi or day.isoformat() <= hi):
            return t
    return W.CUTOFF[-1][2]


# ---------------------------------------------------------------- A1, payment runs
def run_log(target, rows, runs):
    """One row per payment run: when it was released, its value, and what was reversed."""
    rng = sim.Rng(330815)
    byrun = {}
    for r in rows:
        if r["delivery"] != 1:
            continue
        byrun.setdefault(r["run"], []).append(r)
    out, truth = [], {}
    for run in sorted(byrun):
        rs = byrun[run]
        day = rs[0]["day"]
        cut = cutoff_for(day)
        ch, cm = [int(v) for v in cut.split(":")]
        # most runs go out before the cut-off; some after; one lands exactly on it
        u = rng.u()
        if u < 0.74:
            mins = ch * 60 + cm - (5 + rng.below(220))
        elif u < 0.97:
            mins = ch * 60 + cm + (1 + rng.below(150))
        else:
            mins = ch * 60 + cm
        mins = max(8 * 60 + 5, min(20 * 60 + 55, mins))
        # A payment run pays the whole authority, not one population: plan 4.1 names three and the
        # capital programme payments are one of them. The log records the run as it went out, so
        # its value and its line count are the whole run, and the capital extract holds only the
        # capital part of it. Nothing says so: the excess shows only by summing the extract for a
        # run and comparing it with the run's own total, and it ties to the revenue expenditure
        # summary's monthly figures.
        cap_value = sum(x["amount"] for x in rs)
        cap_lines = len(rs)
        h = sim.shash("rev/%s" % run)
        rev_lines = 38 + h % 71
        rev_value = round(cap_value * (0.21 + (h % 997) / 997.0 * 0.26), 2)
        value = round(cap_value + rev_value, 2)
        rev = sum(x["amount"] for x in rs if x["status"] == "reversed")
        # a run is opened on one day and released on it, except where the release ran past
        # midnight: four of them in the year, and the quarter is the quarter it was released in
        rel = day
        last_of_quarter = any(day.isoformat() == hi for _n, _lo, hi in QUARTERS)
        if last_of_quarter or rng.u() < 0.04:
            rel = day + dt.timedelta(days=1)
            # minutes are measured from the run's own date, so a release that ran past midnight is
            # later than any cut-off on that date rather than earlier than all of them
            mins = 24 * 60 + (1 + rng.below(3)) * 60 + rng.below(60)
        out.append([run, day.isoformat(),
                    "%s %02d:%02d:00" % (rel.isoformat(), (mins // 60) % 24, mins % 60),
                    cap_lines + rev_lines, "%.2f" % value, "%.2f" % (-rev), "released",
                    "FO%03d" % (11 + rng.below(14))])
        truth[run] = (rel, mins, cap_lines + rev_lines, value, -rev, cut, day,
                      cap_value, cap_lines, rev_value, rev_lines)
        # one run was rejected by the bank and re-released, so the log carries it twice
        if run.endswith("017"):
            out.append([run, day.isoformat(),
                        "%s %02d:%02d:00" % ((day + dt.timedelta(days=3)).isoformat(),
                                             14, 12),
                        cap_lines + rev_lines, "%.2f" % value, "%.2f" % (-rev),
                        "re-released",
                        "FO%03d" % (11 + rng.below(14))])
    PK.write_csv(target, "payment_run_log_2026.csv",
                 ["run_id", "run_date", "released_ts", "lines_in_run", "run_value_eur",
                  "reversed_value_eur", "run_status", "operator_id"], out)
    return truth


def cutoff_register(target):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Cut-off"
    ws["A1"] = "%s: payment release cut-off" % W.AUTHORITY
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "A run released at the cut-off is within it. A run released after it is outside it."
    ws["A2"].font = Font(size=9, italic=True)
    for j, h in enumerate(["effective_from", "effective_to", "cutoff_time", "approved_by"]):
        c = ws.cell(row=4, column=1 + j, value=h)
        c.font = Font(bold=True)
    for i, (a, b, t) in enumerate(W.CUTOFF):
        ws.cell(row=5 + i, column=1, value=a)
        ws.cell(row=5 + i, column=2, value=b if b else "open")
        ws.cell(row=5 + i, column=3, value=t)
        ws.cell(row=5 + i, column=4, value="Finance operations standards group")
    for col, wd in (("A", 18), ("B", 18), ("C", 14), ("D", 40)):
        ws.column_dimensions[col].width = wd
    path = os.path.join(target, "payment_release_cutoff_register.xlsx")
    wb.save(path)
    return path


def a1_golden(truth):
    """Per quarter: runs released, those past the cut-off in force, and the value they carried.

    Both conventions are pinned in the asking sentence: a run falls in the quarter its release
    falls in, and a release is judged against the cut-off in force on the run's own date, which is
    what makes an overnight release late rather than moving it into the next quarter.
    """
    out = {}
    for name, lo, hi in QUARTERS:
        past, val = 0, 0.0
        for run, (day, mins, nl, value, r, cut, opened, cv, cl, rv, rl) in truth.items():
            if not (lo <= day.isoformat() <= hi):
                continue
            ch, cm = [int(v) for v in cut.split(":")]
            if mins > ch * 60 + cm:
                past += 1
                val += value
        out[name] = (past, round(val, 2))
    return out


def a1_stops(truth):
    """Every reading an ask ladder stop needs.

    `the_mirror` is the response that stops at the wrong rung and takes each obvious reading: one
    cut-off for the whole year, the run grouped on the date it opened, and the re-released run
    counted twice. `answer` is the reading the filed rules and the hygiene battery give, which is
    what the cracker executes.
    """
    stops = {}
    for name in ("cutoff_1500_only", "cutoff_1400_only", "on_the_cutoff_counted",
                 "grouped_on_the_opening_date", "the_mirror", "answer"):
        agg = {}
        for q, lo, hi in QUARTERS:
            n, past, val = 0, 0, 0.0
            for run, (day, mins, nl, value, r, cut, opened, cv, cl, rv, rl) in truth.items():
                d = opened if name in ("grouped_on_the_opening_date", "the_mirror") else day
                if not (lo <= d.isoformat() <= hi):
                    continue
                n += 1
                use = ("15:00" if name in ("cutoff_1500_only", "the_mirror")
                       else "14:00" if name == "cutoff_1400_only" else cut)
                ch, cm = [int(v) for v in use.split(":")]
                if mins > ch * 60 + cm or (name == "on_the_cutoff_counted"
                                           and mins == ch * 60 + cm):
                    past += 1
                    val += value
            if name == "the_mirror":                  # the re-released run counted twice
                n += 1 if lo <= "2026-05-01" <= hi else 0
            agg[q] = (past, round(val, 2))
        stops[name] = agg
    return stops


# ---------------------------------------------------------------- A2, supplier risk categories
def risk_history(target, cross):
    """Approval events, one chain per supplier: a category moves one way across the year."""
    rng = sim.Rng(624199)
    masters = sorted(cross.values())
    events, eid = [], 0
    for m in masters:
        if rng.u() > 0.46:
            continue
        cat = int(rng.pick(W.RISK_BANDS))
        rising = rng.u() < 0.52
        if cat >= 5:
            rising = False
        if cat <= 1:
            rising = True
        nev = 1 + (1 if rng.u() < 0.38 else 0) + (1 if rng.u() < 0.11 else 0)
        nev = min(nev, (5 - cat) if rising else (cat - 1)) or 1
        days = []
        while len(days) < nev:
            d = rng.below(360)
            if all(abs(d - x) >= 9 for x in days):
                days.append(d)
        days.sort()
        for k in range(nev):
            eid += 1
            after = cat + (1 if rising else -1)
            eff = dt.date(2026, 1, 1) + dt.timedelta(days=days[k])
            load = dt.datetime(eff.year, eff.month, eff.day, 9, 20) + \
                dt.timedelta(days=1 + rng.below(6), minutes=rng.below(420))
            events.append(dict(eid=eid, sup=m, before=str(cat), after=str(after), eff=eff,
                               load=load, status="accepted",
                               relab=eff.isoformat() >= W.RISK_RELABEL,
                               officer="PO%03d" % (21 + rng.below(19))))
            cat = after
    # a handful were filed wrong and corrected on the same effective date; the chain runs through
    byc, extra, picked = {}, [], 0
    for e in events:
        byc.setdefault(e["sup"], []).append(e)
    for sup in sorted(byc):
        es = sorted(byc[sup], key=lambda e: (e["eff"], e["eid"]))
        if picked >= 14 or len(es) < 2 or sim.shash(sup) % 7:
            continue
        e = es[0]
        e["status"] = "superseded"
        eid += 1
        b = int(e["before"])
        rise = int(e["after"]) > b
        fixed = min(5, b + 2) if rise else max(1, b - 2)
        if fixed == b:
            continue
        extra.append(dict(e, eid=eid, after=str(fixed), status="accepted",
                          load=e["load"] + dt.timedelta(days=1 + sim.shash(sup) % 6,
                                                        minutes=13 + sim.shash(sup) % 290)))
        cat = fixed
        keep = []
        for nxt in es[1:]:
            if (rise and cat >= 5) or (not rise and cat <= 1):
                break
            nxt["before"] = str(cat)
            cat = cat + (1 if rise else -1)
            nxt["after"] = str(cat)
            keep.append(nxt)
        for dead in es[1 + len(keep):]:
            dead["drop"] = True
        picked += 1
    events.extend(extra)
    events = [e for e in events if not e.get("drop")]
    events.sort(key=lambda e: (e["eff"], e["eid"]))
    rows = []
    for e in events:
        b = W.RISK_NEW[e["before"]] if e["relab"] else e["before"]
        a = W.RISK_NEW[e["after"]] if e["relab"] else e["after"]
        rows.append(["RA%06d" % (e["eid"] * 3 + 7), e["sup"], b, a, e["eff"].isoformat(),
                     e["load"].strftime("%Y-%m-%dT%H:%M:%S"), e["status"], e["officer"]])
    PK.write_csv(target, "supplier_risk_approval_history.csv",
                 ["event_id", "supplier_no_master", "category_before", "category_after",
                  "effective_date", "load_ts", "event_status", "officer_id"], rows)
    PK.write_csv(target, "supplier_risk_category_map.csv",
                 ["label_to_2026_09_30", "label_from_2026_10_01", "description"],
                 [[b, W.RISK_NEW[b], ["Lowest", "Low", "Medium", "High", "Highest"][i]]
                  for i, b in enumerate(W.RISK_BANDS)])
    return events, picked


def a2_unmapped(events):
    """The mirror's reading: the labels taken as they stand, so the October relabelling splits
    every category in two and no count is the register's."""
    byc = {}
    for e in events:
        if e["status"] != "accepted":
            continue
        byc.setdefault(e["sup"], []).append(e)
    lab = {}
    for b in W.RISK_BANDS:
        lab[b] = b
        lab[W.RISK_NEW[b]] = W.RISK_NEW[b]
    up = {}
    down = {}
    off = {}
    rank = {b: i for i, b in enumerate(W.RISK_BANDS)}
    rank.update({W.RISK_NEW[b]: i for i, b in enumerate(W.RISK_BANDS)})
    for sup, es in byc.items():
        es.sort(key=lambda e: (e["eff"], e["eid"]))
        for i, e in enumerate(es):
            b = W.RISK_NEW[e["before"]] if e["relab"] else e["before"]
            a = W.RISK_NEW[e["after"]] if e["relab"] else e["after"]
            if rank[a] > rank[b]:
                up.setdefault(a, set()).add(sup)
                if any((W.RISK_NEW[x["before"]] if x["relab"] else x["before"]) == a
                       for x in es[i + 1:]):
                    off.setdefault(a, set()).add(sup)
            elif rank[a] < rank[b]:
                down.setdefault(a, set()).add(sup)
    return {b: (len(up.get(b, ())), len(down.get(b, ())), len(off.get(b, ())))
            for b in W.RISK_BANDS}


def a2_golden(events, mode="answer"):
    """Per category: suppliers raised into it, removed from it, and raised in then removed."""
    use = events if mode == "all" else [e for e in events if e["status"] == "accepted"]
    byc = {}
    for e in use:
        byc.setdefault(e["sup"], []).append(e)
    up = {b: [] for b in W.RISK_BANDS}
    down = {b: [] for b in W.RISK_BANDS}
    off = {b: [] for b in W.RISK_BANDS}
    for sup, es in byc.items():
        es.sort(key=lambda e: (e["eff"], e["eid"]))
        for i, e in enumerate(es):
            if int(e["after"]) > int(e["before"]):
                up[e["after"]].append(sup)
                if any(int(x["before"]) == int(e["after"]) for x in es[i + 1:]):
                    off[e["after"]].append(sup)
            # "removed from it" is a move OUT of the category the supplier was in, which is the
            # asking sentence's own wording; a move INTO a lower category is not a removal from it
            if int(e["after"]) != int(e["before"]):
                down[e["before"]].append(sup)
    if mode == "events":
        return {b: (len(up[b]), len(down[b]), len(off[b])) for b in W.RISK_BANDS}
    return {b: (len(set(up[b])), len(set(down[b])), len(set(off[b]))) for b in W.RISK_BANDS}


# ---------------------------------------------------------------- A3, the schedule against the ledger
MONTHS = ["2026-%02d" % m for m in range(1, 13)]


def a3_golden(tested_rows, ledger_lines, invoices=None):
    """Per month: lines the schedule covers; schedule lines absent from the ledger; doubles."""
    ledger = {}
    for r in ledger_lines:
        ledger.setdefault(r["line"], 0)
        ledger[r["line"]] += 1
    # the monthly figure is DISTINCT ledger lines, pinned in the asking sentence, so the line the
    # schedule carries twice after a query counts once and the twelve months sum to the tested count
    bymonth = {q: set() for q, _lo, _hi in QUARTERS}
    absent, twice = [], []
    seen = {}
    inv = invoices or {}
    for t in tested_rows:
        ref = t["line"]
        if ref in inv:
            # the row is recorded at invoice level, so it covers every payment line on that
            # invoice, which is more lines than the selection chose
            for line in inv[ref]:
                bymonth[_q(t["day"])].add(line)
                seen[line] = seen.get(line, 0) + 1
            continue
        if ref not in ledger:
            # a row that resolves to neither a payment line nor an invoice in this ledger is no
            # part of this population, so it is counted as absent and counted in no month
            absent.append(t["schedule_ref"])
            continue
        bymonth[_q(t["day"])].add(ref)
        seen[ref] = seen.get(ref, 0) + 1
    bymonth = {m: len(v) for m, v in bymonth.items()}
    for line, n in sorted(seen.items()):
        if n > 1:
            twice.append(line)
    return bymonth, len(absent), sorted(absent), len(twice), sorted(twice)
