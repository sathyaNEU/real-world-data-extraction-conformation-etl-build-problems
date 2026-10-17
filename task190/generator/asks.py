"""The three ask files and their devices. None of them touches a deposit row."""
import datetime as dt
import os

import pack as PK
import sim
import world as W

QUARTERS = [("2026Q3", dt.date(2026, 7, 1), dt.date(2026, 9, 30)),
            ("2026Q4", dt.date(2026, 10, 1), dt.date(2026, 12, 31)),
            ("2027Q1", dt.date(2027, 1, 1), dt.date(2027, 3, 31)),
            ("2027Q2", dt.date(2027, 4, 1), dt.date(2027, 6, 30))]

TOLERANCE = [("2024-07-01", "2026-12-31", 25.00), ("2027-01-01", "", 15.00)]

def estate(lo=dt.date(2026, 7, 1), hi=dt.date(2027, 6, 30)):
    """The machines in service at some point in the reporting year, from the register."""
    out = []
    for mid, site, inst, wdr in W.MACHINES:
        a0 = dt.date(*[int(v) for v in inst.split("-")])
        b0 = dt.date(*[int(v) for v in wdr.split("-")]) if wdr else None
        if a0 <= hi and (b0 is None or b0 > lo):
            out.append((mid, site, a0, b0))
    return out


SITE_OF = {m[0]: m[1] for m in W.MACHINES}
SIGNOFF_SITES = tuple(W.SIGNOFF_SITES)   # the sites whose engineers sign off after restoring


# ---------------------------------------------------------------- A1, till variance
def till_log(target):
    """Cash count sessions. Machine collection sessions are stamped UTC, counter ones local."""
    rng = sim.Rng(330815)
    rows, truth = [], {}
    sid = 0
    for code, _n, _r, opened, closed in W.BRANCHES:
        for day in sim.dates("2025-07-01", "2027-06-30"):
            if day.weekday() >= 5:
                continue
            if closed and day >= dt.date(*[int(v) for v in closed.split("-")]):
                continue
            for src in ("counter", "machine"):
                if src == "machine" and not any(m[1] == code for m in W.MACHINES):
                    continue
                if rng.u() > (0.86 if src == "counter" else 0.42):
                    continue
                sid += 1
                # a machine collection runs at midday, so its UTC stamp falls on the same
                # calendar day as the local one and the quarter does not turn on which is read
                hhmm = (16 * 60 + 40 + rng.below(70)) if src == "counter" else (13 * 60 + rng.below(50))
                expected = round(2400 + rng.u() ** 1.7 * 48000, 2)
                v = 0.0
                u = rng.u()
                if u < 0.46:
                    v = round((rng.u() - 0.5) * 9.4, 2)
                elif u < 0.78:
                    v = round((rng.u() - 0.5) * 38.0, 2)
                else:
                    v = round((rng.u() - 0.5) * 96.0, 2)
                if sid % 1301 == 0:          # a count that came out exactly on the tolerance
                    v = (25.00 if day < dt.date(2027, 1, 1) else 15.00) * (1 if sid % 2 else -1)
                counted = round(expected + v, 2)
                if src == "counter":
                    ts = "%sT%02d:%02d:00" % (day.isoformat(), hhmm // 60, hhmm % 60)
                else:
                    ts = PK.utc_stamp(day, hhmm)
                rows.append([("TS%06d" % (sid * 3 + 7)), code, src, ts,
                             "%.2f" % counted, "%.2f" % expected, "%.2f" % v,
                             "OP%s%02d" % (code[2:], 1 + rng.below(9)), "complete", PK.PULL])
                truth[("TS%06d" % (sid * 3 + 7))] = (code, src, day, hhmm, v)
    PK.write_csv(target, "till_balance_log_2026_2027.csv",
                 ["session_id", "branch_code", "collection_source", "session_opened_ts",
                  "counted_nzd", "expected_nzd", "variance_nzd", "operator_id",
                  "session_status", "pull_date"], rows)
    return truth


def tolerance_register(target):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Tolerances"
    ws["A1"] = "%s: branch cash count variance tolerances" % W.BANK
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "A session's variance passes where its absolute value is at or under the tolerance."
    ws["A2"].font = Font(size=9, italic=True)
    for j, h in enumerate(["effective_from", "effective_to", "tolerance_nzd", "approved_by"]):
        c = ws.cell(row=4, column=1 + j, value=h)
        c.font = Font(bold=True)
    for i, (a, b, t) in enumerate(TOLERANCE):
        ws.cell(row=5 + i, column=1, value=a)
        ws.cell(row=5 + i, column=2, value=b if b else "open")
        ws.cell(row=5 + i, column=3, value=t)
        ws.cell(row=5 + i, column=4, value="Branch operations standards committee")
    for col, wd in (("A", 18), ("B", 18), ("C", 16), ("D", 40)):
        ws.column_dimensions[col].width = wd
    path = os.path.join(target, "cash_tolerance_register.xlsx")
    wb.save(path)
    return path


def a1_golden(truth):
    """Per quarter: sessions recorded, sessions over the tolerance in force, net variance."""
    out = {}
    for q, lo, hi in QUARTERS:
        n, over, net = 0, 0, 0.0
        for sid, (code, src, day, hhmm, v) in truth.items():
            if not (lo <= day <= hi):
                continue
            n += 1
            tol = 25.00 if day < dt.date(2027, 1, 1) else 15.00
            if abs(v) > tol:
                over += 1
            net += v
        out[q] = (n, over, round(net, 2))
    return out


def a1_stops(truth):
    """The ladder: raw stamps, tolerance fixed, double counted, the answer."""
    stops = {}
    for name in ("tolerance_25_only", "tolerance_15_only", "on_the_tolerance_counted", "answer"):
        agg = {}
        for q, lo, hi in QUARTERS:
            n, over, net = 0, 0, 0.0
            for sid, (code, src, day, hhmm, v) in truth.items():
                if not (lo <= day <= hi):
                    continue
                n += 1
                tol = (25.00 if name == "tolerance_25_only"
                       else 15.00 if name == "tolerance_15_only"
                       else (25.00 if day < dt.date(2027, 1, 1) else 15.00))
                if abs(v) > tol or (name == "on_the_tolerance_counted" and abs(v) == tol):
                    over += 1
                net += v
            agg[q] = (n, over, round(net, 2))
        stops[name] = agg
    return stops


# ---------------------------------------------------------------- A2, risk ratings
BANDS = ["1", "2", "3", "4", "5"]
NEWBANDS = {"1": "A", "2": "B", "3": "C", "4": "D", "5": "E"}


def rating_history(target, custs):
    """Rating events, one chain per customer: every event starts where the last one left off."""
    rng = sim.Rng(624199)
    pool = sorted(custs, key=lambda c: c["cust"])
    events = []
    eid = 0
    for c in pool:
        if rng.u() > 0.21:
            continue
        nev = 1 + (1 if rng.u() < 0.34 else 0) + (1 if rng.u() < 0.08 else 0)
        band = int(rng.pick(BANDS))
        # a customer's rating drifts one way over the year: it never returns to a band it left,
        # so a band it was raised into and later moved off is a band it is not in at year end
        rising = rng.u() < 0.56
        if band >= 5:
            rising = False
        if band <= 1:
            rising = True
        nev = min(nev, 4 - band if rising else band - 1) or 1
        # one event per effective date, so no customer carries two accepted moves on one day
        days = []
        while len(days) < nev:
            d = rng.below(364)
            if all(abs(d - x) >= 7 for x in days):
                days.append(d)
        days.sort()
        for k in range(nev):
            eid += 1
            up = rising
            if band >= 5:
                up = False
            if band <= 1:
                up = True
            after = band + (1 if up else -1)
            eff = dt.date(2026, 7, 1) + dt.timedelta(days=days[k])
            load = dt.datetime(eff.year, eff.month, eff.day, 9, 15) + \
                dt.timedelta(days=1 + rng.below(5), minutes=rng.below(400))
            events.append(dict(eid=eid, cust=c["cust"], before=str(band), after=str(after),
                               eff=eff, load=load, status="accepted",
                               relab=eff >= dt.date(2027, 4, 6),
                               reviewer="RV%03d" % (11 + rng.below(27))))
            band = after
    # some events were filed wrong and corrected the same effective date; the register took the
    # correction, and the chain runs through it
    extra = []
    byc = {}
    for e in events:
        byc.setdefault(e["cust"], []).append(e)
    picked = 0
    for cust in sorted(byc):
        es = sorted(byc[cust], key=lambda e: (e["eff"], e["eid"]))
        if picked >= 11 or len(es) < 2:
            continue
        if sim.shash(cust) % 37:
            continue
        e = es[0]
        e["status"] = "superseded"
        eid += 1
        b = int(e["before"])
        # the correction lands two steps where the wrong filing put one, in the same direction
        fixed = min(5, b + 2) if int(e["after"]) > b else max(1, b - 2)
        if fixed == b:
            fixed = b + 1 if b < 5 else b - 1
        corr = dict(e, eid=eid, after=str(fixed), status="accepted",
                    load=e["load"] + dt.timedelta(days=1 + sim.shash(cust) % 5,
                                                  minutes=11 + sim.shash(cust) % 300))
        extra.append(corr)
        # the rest of the customer's chain runs on from the correction
        band = fixed
        keep = []
        rise = fixed > b
        for nxt in es[1:]:
            if (rise and band >= 5) or (not rise and band <= 1):
                break                      # the chain stops rather than turning back
            nxt["before"] = str(band)
            band = band + (1 if rise else -1)
            nxt["after"] = str(band)
            keep.append(nxt)
        for dead in es[1 + len(keep):]:
            dead["drop"] = True            # a gap in the register: the move was never filed
        picked += 1
    events.extend(extra)
    events = [e for e in events if not e.get("drop")]
    events.sort(key=lambda e: (e["eff"], e["eid"]))
    rows = []
    for e in events:
        b = NEWBANDS[e["before"]] if e["relab"] else e["before"]
        aa = NEWBANDS[e["after"]] if e["relab"] else e["after"]
        rows.append(["RE%06d" % (e["eid"] * 3 + 5), e["cust"], b, aa, e["eff"].isoformat(),
                     e["load"].strftime("%Y-%m-%dT%H:%M:%S"), e["status"], e["reviewer"], PK.PULL])
    PK.write_csv(target, "risk_rating_history.csv",
                 ["event_id", "master_customer_no", "rating_before", "rating_after",
                  "effective_date", "load_ts", "event_status", "reviewer_id", "pull_date"], rows)
    PK.write_csv(target, "rating_scale_map.csv",
                 ["scale_to_2027_04_05", "scale_from_2027_04_06", "label"],
                 [[b, NEWBANDS[b], ["Low", "Low to medium", "Medium", "Medium to high",
                                    "High"][i]] for i, b in enumerate(BANDS)])
    return events, picked


def a2_golden(events, mode="answer"):
    """Per band: the customers raised into it, lowered into it, and raised into it then off it.

    mode "answer"    the events the register accepted, counted by distinct customer
    mode "all"       every row, the superseded ones counted alongside their corrections
    mode "events"    accepted, but counted by event rather than by customer
    """
    use = events if mode == "all" else [e for e in events if e["status"] == "accepted"]
    byc = {}
    for e in use:
        byc.setdefault(e["cust"], []).append(e)
    raised = {b: [] for b in BANDS}
    lowered = {b: [] for b in BANDS}
    off = {b: [] for b in BANDS}
    for cust, es in byc.items():
        es.sort(key=lambda e: (e["eff"], e["eid"]))
        for i, e in enumerate(es):
            if int(e["after"]) > int(e["before"]):
                raised[e["after"]].append(cust)
                if any(int(x["before"]) == int(e["after"]) for x in es[i + 1:]):
                    off[e["after"]].append(cust)
            elif int(e["after"]) < int(e["before"]):
                lowered[e["after"]].append(cust)
    if mode == "events":
        return {b: (len(raised[b]), len(lowered[b]), len(off[b])) for b in BANDS}
    return {b: (len(set(raised[b])), len(set(lowered[b])), len(set(off[b]))) for b in BANDS}


# ---------------------------------------------------------------- A3, machine availability
def service_log(target):
    """Service calls on the estate, month by month, machine by machine."""
    rng = sim.Rng(905311)
    rows, truth = [], {}
    inc = 0
    for mid, site, inst, wdr in estate():
        if mid in W.NO_INCIDENT:
            continue
        for m in range(12):
            y, mm = (2026, 7 + m) if 7 + m <= 12 else (2027, 7 + m - 12)
            first = dt.date(y, mm, 1)
            last = dt.date(y + (1 if mm == 12 else 0), 1 if mm == 12 else mm + 1, 1) - \
                dt.timedelta(days=1)
            if inst > last or (wdr and wdr <= first):
                continue
            n = 0 if rng.u() < 0.31 else 1 + rng.below(3)
            hi_day = (min(last, wdr - dt.timedelta(days=1)) if wdr else last)
            taken = []                     # (start, end) already used on this machine
            for _ in range(n):
                dayspan = max(1, (hi_day - max(inst, first)).days + 1)
                placed = None
                for _try in range(40):
                    day = max(inst, first) + dt.timedelta(days=rng.below(dayspan))
                    if day > hi_day:
                        continue
                    mins = 25 + rng.below(430)
                    # a fault is reported at any hour: the estate runs unattended overnight
                    rep = dt.datetime(day.year, day.month, day.day, rng.below(24), rng.below(60),
                                      rng.below(60))
                    end = rep + dt.timedelta(minutes=mins)
                    # one machine is out once at a time, so the month's hours out of service are
                    # the sum of its incidents and their union alike
                    if all(end <= a or rep >= b for a, b in taken):
                        placed = (rep, end, mins)
                        break
                if placed is None:
                    continue
                rep, end, mins = placed
                taken.append((rep, end))
                inc += 1
                # the restored stamp is when the engineer closed the call; a few logs carry the
                # minutes the engineer wrote on the docket instead, which is not the difference
                shown = mins
                if inc % 83 == 0:
                    shown = mins - (1 + inc % 4)
                rows.append(["SI%06d" % (inc * 3 + 11 + rng.below(3)), mid, site,
                             rep.strftime("%Y-%m-%dT%H:%M:%S"),
                             end.strftime("%Y-%m-%dT%H:%M:%S"),
                             shown, rng.pick(["NOTE-JAM", "NOTE-JAM", "COMMS", "PRINTER",
                                              "SAFE-FULL", "CARD-READER", "POWER", "VALIDATOR"]),
                             "EN%04d" % (120 + rng.below(80))])
                key = (mid, "%04d-%02d" % (rep.year, rep.month))
                truth[key] = truth.get(key, 0) + shown
    # a month's hours are stated to one decimal, so only a total exactly half way between two
    # tenths of an hour has two readings. Six minutes is a tenth, so that is a total three
    # minutes past a multiple of six, and only those few are nudged.
    by_month = {}
    for i, r in enumerate(rows):
        by_month.setdefault(r[3][:7], []).append(i)
    for mo, idx in sorted(by_month.items()):
        tot = sum(rows[i][5] for i in idx)
        if tot % 6 == 3:
            i = idx[-1]
            add = 1
            rows[i][5] += add
            key = (rows[i][1], mo)
            truth[key] = truth.get(key, 0) + add
    rows.sort(key=lambda r: (r[3], r[1]))
    PK.write_csv(target, "machine_service_log_2027.csv",
                 ["incident_id", "machine_id", "site_code", "reported_ts", "restored_ts",
                  "out_of_service_minutes", "fault_code", "engineer_ref"], rows)
    return truth


def vendor_rows(truth):
    """The vendor reports by site, summing the machines a site runs, and counts from the
    dispatch call to the engineer's sign off, which runs past the bank's restored stamp."""
    by_site = {}
    for (mid, month), mins in sorted(truth.items()):
        site = SITE_OF[mid]
        extra = 0
        if site in SIGNOFF_SITES:
            extra = int(mins * 0.34)
        by_site[(site, month)] = by_site.get((site, month), 0) + mins + extra
    out = []
    for (site, month), mins in sorted(by_site.items()):
        out.append((site, month, mins, 1 + (mins // 240)))
    return out


MONTHS = ["2026-07", "2026-08", "2026-09", "2026-10", "2026-11", "2026-12",
          "2027-01", "2027-02", "2027-03", "2027-04", "2027-05", "2027-06"]


def a3_golden(truth, vrows):
    """Per month: the estate's hours out of service; the machines with no service record; the
    sites whose own hours differ from the vendor's by more than two hours over the year."""
    per_month = {}
    for mo in MONTHS:
        mins = sum(v for (mid, m), v in truth.items() if m == mo)
        per_month[mo] = round(mins / 60.0, 1)
    logged = {mid for mid, _m in truth}
    no_record = sorted(mid for mid, site, inst, wdr in estate() if mid not in logged)
    bank_site, vend_site = {}, {}
    for (mid, m), v in truth.items():
        bank_site[SITE_OF[mid]] = bank_site.get(SITE_OF[mid], 0) + v
    for site, month, mins, visits in vrows:
        vend_site[site] = vend_site.get(site, 0) + mins
    differ = sorted(s for s in set(list(bank_site) + list(vend_site))
                    if abs(vend_site.get(s, 0) - bank_site.get(s, 0)) > 120)
    return per_month, len(no_record), no_record, differ
