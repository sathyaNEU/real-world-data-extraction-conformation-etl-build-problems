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
        value = sum(x["amount"] for x in rs)
        rev = sum(x["amount"] for x in rs if x["status"] == "reversed")
        out.append([run, day.isoformat(),
                    "%s %02d:%02d:00" % (day.isoformat(), mins // 60, mins % 60),
                    len(rs), "%.2f" % value, "%.2f" % (-rev), "released",
                    "FO%03d" % (11 + rng.below(14))])
        truth[run] = (day, mins, len(rs), value, -rev, cut)
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
    """Per quarter: runs released, those past the cut-off in force, net value reversed."""
    out = {}
    for name, lo, hi in QUARTERS:
        n, past, rev = 0, 0, 0.0
        for run, (day, mins, nl, value, r, cut) in truth.items():
            if not (lo <= day.isoformat() <= hi):
                continue
            n += 1
            ch, cm = [int(v) for v in cut.split(":")]
            if mins > ch * 60 + cm:
                past += 1
            rev += r
        out[name] = (n, past, round(rev, 2))
    return out


def a1_stops(truth):
    """The cracker's readings: one cut-off for the year, and counting the run on the cut-off."""
    stops = {}
    for name in ("cutoff_1500_only", "cutoff_1400_only", "on_the_cutoff_counted", "answer"):
        agg = {}
        for q, lo, hi in QUARTERS:
            n, past, rev = 0, 0, 0.0
            for run, (day, mins, nl, value, r, cut) in truth.items():
                if not (lo <= day.isoformat() <= hi):
                    continue
                n += 1
                use = ("15:00" if name == "cutoff_1500_only"
                       else "14:00" if name == "cutoff_1400_only" else cut)
                ch, cm = [int(v) for v in use.split(":")]
                if mins > ch * 60 + cm or (name == "on_the_cutoff_counted"
                                           and mins == ch * 60 + cm):
                    past += 1
                rev += r
            agg[q] = (n, past, round(rev, 2))
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
        if picked >= 9 or len(es) < 2 or sim.shash(sup) % 29:
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
            elif int(e["after"]) < int(e["before"]):
                down[e["after"]].append(sup)
    if mode == "events":
        return {b: (len(up[b]), len(down[b]), len(off[b])) for b in W.RISK_BANDS}
    return {b: (len(set(up[b])), len(set(down[b])), len(set(off[b]))) for b in W.RISK_BANDS}


# ---------------------------------------------------------------- A3, the schedule against the ledger
MONTHS = ["2026-%02d" % m for m in range(1, 13)]


def a3_golden(tested_rows, ledger_lines):
    """Per month: lines the schedule covers; schedule lines absent from the ledger; doubles."""
    ledger = {}
    for r in ledger_lines:
        ledger.setdefault(r["line"], 0)
        ledger[r["line"]] += 1
    bymonth = {m: 0 for m in MONTHS}
    absent, twice = [], []
    seen = {}
    for t in tested_rows:
        bymonth[t["day"].isoformat()[:7]] += 1
        if t["line"] not in ledger:
            absent.append(t["schedule_ref"])
        seen[t["line"]] = seen.get(t["line"], 0) + 1
    for line, n in sorted(seen.items()):
        if n > 1:
            twice.append(line)
    return bymonth, len(absent), sorted(absent), len(twice), sorted(twice)
