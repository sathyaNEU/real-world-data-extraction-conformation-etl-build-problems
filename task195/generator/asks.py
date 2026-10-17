"""The files the supplemental asks run on, and the operating records that come with them."""
import csv
import datetime as dt
import os
import random

import openpyxl
from openpyxl.styles import Alignment, Border, Font, Side
from openpyxl.utils import get_column_letter

import pack as PK
import world as W


def _months():
    out, d = [], W.BASE_FROM
    while d <= W.BASE_TO:
        out.append("%04d-%02d" % (d.year, d.month))
        d = (d.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    return out


def history(target):
    """The quality-control warehouse extract: the twelve reporting months before the parallel run.

    The nightly load carries the screen's automatic call in hetx_call and the duty bioinformatician's
    outcome, where a specimen was reviewed, in review_outcome. The review stands: a reviewed specimen
    counts as the reviewer left it. The month a specimen belongs to in the laboratory's reporting pack
    is the month its result was released.
    """
    rng = random.Random(W.SEED + 21)
    trng = random.Random(W.SEED + 81)        # accessions, intake hours and heterozygosity texture
    days = [(W.HIST_FROM + dt.timedelta(days=i)) for i in range((W.HIST_TO - W.HIST_FROM).days + 1)]
    days = [d for d in days if d.weekday() < 5]
    serial = [10007]
    rows = []
    per_day = W.HIST_ROWS / len(days)
    k = 0
    for d in days:
        n = int(round(per_day * (0.82 + 0.36 * rng.random())))
        for _ in range(n):
            if k >= W.HIST_ROWS:
                break
            k += 1
            serial[0] += trng.randint(2, 11)
            lag = rng.randint(4, 26)
            rel = d + dt.timedelta(days=lag)
            while rel.weekday() > 4:
                rel += dt.timedelta(days=1)
            r = rng.random()
            status = "WITHHELD" if r < 0.023 else ("SUPERSEDED" if r < 0.044 else "RELEASED")
            rng.randint(7, 22)                   # the warehouse's own intake draw
            minute = rng.randint(0, 59)
            hour = min(21, max(6, int(trng.gauss(10.8, 2.9)) if trng.random() < 0.74
                               else int(trng.gauss(15.2, 1.9))))
            # the laboratory is closed on a holiday, so the receipt is logged on a nearby open day
            rec = d
            if rec in W.HOLIDAYS:
                near = [d + dt.timedelta(days=delta) for delta in (-1, -2, 1, 2, -3, 3)]
                near = [c for c in near if c.weekday() < 5 and c not in W.HOLIDAYS
                        and W.HIST_FROM <= c <= rel]
                rec = near[k % len(near)] if near else rel - dt.timedelta(days=1)
            local = dt.datetime(rec.year, rec.month, rec.day, hour, minute)
            offset = 2 if dt.date(rec.year, 3, 29) <= rec < dt.date(rec.year, 10, 25) else 1
            rows.append({"sid": "NFG%s-%06d" % (str(d.year)[2:], serial[0]),
                         "project": rng.choice([p[0] for p in W.PROJECTS]),
                         "extraction": rng.choices(W.EXTRACTION, [0.6, 0.28, 0.12])[0],
                         "instrument": W.INSTRUMENTS[0] if rng.random() < 0.52 else W.INSTRUMENTS[1],
                         "plate": "GKP-%s%02d-%s%02d" % (str(d.year)[2:], d.month, "ABCD"[k % 4], (k % 23) + 1),
                         "received": rec, "utc": local - dt.timedelta(hours=offset),
                         "depth": rng.uniform(24.0, 73.0), "status": status,
                         "released": rel if status == "RELEASED" else None,
                         "month": "%04d-%02d" % (rel.year, rel.month) if status == "RELEASED" else "",
                         "flag": False, "reviewed": False})

    # the flagged specimens of each reporting month: the month's own rate, placed so the rate the
    # reporting pack carries sits mid-bin at one decimal
    by_month = {}
    for r in rows:
        if r["status"] == "RELEASED":
            by_month.setdefault(r["month"], []).append(r)
    for month, pool in sorted(by_month.items()):
        den = len(pool)
        rate = W.HIST_FLAG_RATE.get(month)
        if rate is None:
            num = sum(1 for _ in pool if rng.random() < 0.0165)
        else:
            base = int(round(rate * den))
            num = min((n for n in range(max(0, base - 3), base + 4)),
                      key=lambda n: (-_slack(1000.0 * n / den), abs(n - base)))
        picks = sorted(pool, key=lambda r: r["sid"])
        rng.shuffle(picks)
        for r in picks[:num]:
            r["flag"] = True
    for r in rows:
        if r["status"] != "RELEASED" and rng.random() < 0.0165:
            r["flag"] = True
    # borderline specimens are the ones the duty bioinformatician looks at
    for r in rows:
        r["reviewed"] = rng.random() < (0.183 if r["flag"] else 0.028)

    # the duty bioinformatician's review stands over the automatic call, and the warehouse keeps both
    for r in rows:
        r["auto"] = r["flag"]
        if r["reviewed"]:
            if r["flag"] and trng.random() < 0.58:
                r["auto"] = False      # the rule missed it and the reviewer flagged it
            elif not r["flag"] and trng.random() < 0.085:
                r["auto"] = True       # the rule flagged it and the reviewer cleared it

    # a correction is released again inside the same reporting month, so the warehouse holds a second
    # release row for the specimen, carrying the same call
    rerun = []
    for r in rows:
        if r["status"] != "RELEASED" or trng.random() >= 0.052:
            continue
        again = dict(r)
        rel = r["released"] + dt.timedelta(days=trng.randint(2, 13))
        while rel.weekday() > 4 or rel in W.HOLIDAYS:
            rel += dt.timedelta(days=1)
        if "%04d-%02d" % (rel.year, rel.month) != r["month"]:
            rel = r["released"]
            while (rel + dt.timedelta(days=1)).month == r["released"].month:
                rel += dt.timedelta(days=1)
            while rel.weekday() > 4 or rel in W.HOLIDAYS:
                rel -= dt.timedelta(days=1)
            if rel <= r["released"]:
                continue
        again["released"] = rel
        again["plate"] = r["plate"][:-2] + "%02d" % ((int(r["plate"][-2:]) % 23) + 1)
        again["depth"] = r["depth"] * (0.88 + 0.2 * trng.random())
        rerun.append(again)
    rows.extend(rerun)
    rows.sort(key=lambda r: (r["received"], r["sid"], r["released"] or dt.date(2026, 1, 1)))

    # the release desk amends a record after the month has been reported: a release booked on the
    # wrong day, a call corrected on a second look. The warehouse extract predates the amendments, so
    # it holds the value before each one.
    amend = []
    pool = [r for r in rows if r["status"] == "RELEASED" and r["released"]]
    pool.sort(key=lambda r: (r["released"], r["sid"]))
    step = max(1, len(pool) // 430)
    for i in range(0, len(pool), step):
        r = pool[i]
        if r.get("stale"):
            continue
        if trng.random() < 0.72:
            shift = (-1 if trng.random() < 0.5 else 1) * trng.randint(3, 19)
            was = r["released"] - dt.timedelta(days=shift)
            while was.weekday() > 4 or was in W.HOLIDAYS:
                was -= dt.timedelta(days=1)
            if was >= r["received"] + dt.timedelta(days=2):
                amend.append([r["sid"], "released_date", was.isoformat(), r["released"].isoformat(),
                              (max(was, r["released"]) + dt.timedelta(days=trng.randint(6, 40))).isoformat(),
                              "release booked on the wrong day"])
                r["stale_released"] = was
                r["stale"] = True
        else:
            # the desk amends the column that holds the call of record for that specimen: the review
            # outcome where a bioinformatician reviewed it, the screen's own call where none did
            when = (r["released"] + dt.timedelta(days=trng.randint(6, 40))).isoformat()
            why = "flag raised on plate review" if r["flag"] else "flag cleared on plate review"
            if r["reviewed"]:
                amend.append([r["sid"], "review_outcome", "CLEARED" if r["flag"] else "FLAGGED",
                              "FLAGGED" if r["flag"] else "CLEARED", when, why])
                r["stale_review"] = not r["flag"]
            else:
                amend.append([r["sid"], "hetx_call", "CLEAR" if r["flag"] else "FLAG",
                              "FLAG" if r["flag"] else "CLEAR", when, why])
                r["stale_auto"] = not r["flag"]
            r["stale"] = True
    amend.sort(key=lambda x: (x[4], x[0]))

    out = []
    for r in rows:
        # heterozygosity carries a plate effect and a right tail, and the flagged specimens sit in it
        plate_shift = (int(r["plate"][-2:]) % 11 - 5) * 0.042
        stored_auto = r["stale_auto"] if "stale_auto" in r else r["auto"]
        stored_flag = r["stale_review"] if "stale_review" in r else (
            r["stale_auto"] if "stale_auto" in r else r["flag"])
        stored_rel = r.get("stale_released", r["released"])
        if stored_auto:
            het = 36.9 + abs(trng.gauss(0.0, 1.25)) + plate_shift
        else:
            het = trng.gauss(33.86, 0.93) + plate_shift
            if trng.random() < 0.09:
                het += abs(trng.gauss(0.0, 1.5))
            het = min(het, 36.44)
        out.append([r["sid"], r["project"], r["extraction"], r["instrument"], r["plate"],
                    r["received"].isoformat(), r["utc"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "%.1f" % r["depth"], "%.2f" % het,
                    "REVIEWED" if r["reviewed"] else "AUTO",
                    "FLAG" if stored_auto else "CLEAR",
                    ("FLAGGED" if stored_flag else "CLEARED") if r["reviewed"] else "",
                    r["status"], stored_rel.isoformat() if stored_rel else ""])
    out.sort(key=lambda r: (r[5], r[0]))
    PK._write(os.path.join(target, W.FILES["history"]),
              ["specimen_id", "project_code", "extraction_method", "instrument", "plate_id",
               "received_date", "received_utc", "mean_depth", "het_excess_pct", "call_source",
               "hetx_call", "review_outcome", "release_status", "released_date"], out)
    released = {m: len(p) for m, p in by_month.items()}
    flagged = {m: sum(1 for r in p if r["flag"]) for m, p in by_month.items()}
    events = {}
    for r in rows:
        if r["status"] == "RELEASED" and r["released"]:
            stored = r.get("stale_released", r["released"])
            m = "%04d-%02d" % (stored.year, stored.month)
            events[m] = events.get(m, 0) + 1
    return len(out), released, flagged, events, amend


def _slack(rate):
    """How far a per-thousand figure sits from the nearest one-decimal bin edge."""
    return abs((rate * 10) % 1 - 0.5) / 10


def _slack3(value):
    """How far a figure sits from the nearest three-decimal bin edge."""
    return abs((value * 1000) % 1 - 0.5) / 1000


def volumes(target, events_by_month):
    """The laboratory's reporting pack: results released each reporting month."""
    rows = []
    for m in _months():
        rows.append([m, "{:,}".format(events_by_month.get(m, 0)).replace(",", " ")])
    PK._write(os.path.join(target, W.FILES["volumes"]),
              ["reporting_month", "results_released"], rows)
    return len(rows)


def dilution(target):
    """The quarter's in-house dilution panel: nine replicates at each prepared level."""
    rng = random.Random(W.SEED + 31)
    wb = openpyxl.Workbook()
    thin = Side(style="thin", color="FF8A8A8A")
    head = Font(name="Calibri", size=11, bold=True)
    ws = wb.active
    ws.title = "Prepared levels"
    ws.append(["Stock", "Level", "Label", "Prepared level (fraction)", "Prepared", "Operator",
               "Replicates planned"])
    stock_of = {lv: "NS-27-04" for lv, _l, _f in W.DILUTION}
    for stock, day, scale in (("NS-27-07", dt.date(2027, 3, 18), W.DILUTION_SECOND_PREP),
                              ("NS-27-04", dt.date(2027, 3, 11), 1.0)):
        for lv, label, frac in W.DILUTION:
            ws.append([stock, lv, label, round(frac * scale, 4), day,
                       W.PEOPLE["lead"].split()[1][:2].upper(), W.DILUTION_REPLICATES])
    ws["D1"].alignment = Alignment(wrap_text=True)
    results = []
    for li, (lv, label, frac) in enumerate(W.DILUTION):
        spread = 0.21 if lv in ("L1", "L2") else (0.15 if lv == "L3" else 0.085)
        level = frac * (1.0 if stock_of[lv] == "NS-27-04" else W.DILUTION_SECOND_PREP)
        level = round(level, 4)
        # the run itself, with the level's recovery stepped until the median the panel reports sits
        # mid-bin at the three decimals the validation file states it to
        for attempt in range(60):
            lrng = random.Random(W.SEED + 31 + li * 7 + attempt)
            rec = W.DILUTION_RECOVERY[lv] + 0.0009 * attempt
            vals = [round(max(0.0002, level * rec * (1.0 + lrng.gauss(0.0, spread))), 4)
                    for _ in range(W.DILUTION_REPLICATES)]
            median = sorted(vals)[W.DILUTION_REPLICATES // 2]
            if _slack3(median / level) >= 0.00042:
                break
        for i, v in enumerate(vals):
            results.append([lv.lower() if rng.random() < 0.21 else lv, stock_of[lv], i + 1,
                            "RS27-D%05d" % (4100 + len(results) * 3),
                            v, round(rng.uniform(31.0, 58.0), 1), None])
        if lv == "L3":
            results.append([lv, stock_of[lv], W.DILUTION_REPLICATES + 1,
                            "RS27-D%05d" % (4100 + len(results) * 3),
                            None, round(rng.uniform(31.0, 58.0), 1), "voided, control failure"])
    ws2 = wb.create_sheet("Replicate results")
    ws2.append(["Level", "Stock", "Replicate", "Read set", "Recovered fraction", "Mean depth", "Note"])
    for r in results:
        ws2.append(r)
    ws3 = wb.create_sheet("Panel notes")
    for line in [["Analytical sensitivity panel, 2027Q1"],
                 ["Prepared by the method group from two anonymised cell line DNAs. The series is made "
                  "up from a stock each time a stock is drawn; the workbook keeps the series of every "
                  "stock the group has made up."],
                 ["Levels are labelled as the second contributor's share in per cent; the prepared "
                  "level column is the gravimetric fraction."],
                 ["Replicates were sequenced on GSQ-B and processed with GKJ-PIPE v3.4.1."],
                 ["Replicates reported: %d" % len([r for r in results if r[3] != ""])],
                 ["Rows voided on a control failure are kept with no result."]]:
        ws3.append(line)
    for sheet in (ws, ws2, ws3):
        sheet.freeze_panes = "A2" if sheet is not ws3 else None
        for i, width in enumerate([12, 10, 12, 24, 14, 12, 20, 26][:sheet.max_column], start=1):
            sheet.column_dimensions[get_column_letter(i)].width = width
        if sheet is not ws3:
            for c in sheet[1]:
                c.font = head
                c.border = Border(bottom=thin)
    for row in ws2.iter_rows(min_row=2, min_col=5, max_col=5):
        for c in row:
            c.number_format = "0.0000"
    for row in ws.iter_rows(min_row=2, min_col=4, max_col=4):
        for c in row:
            c.number_format = "0.0000"
    for row in ws.iter_rows(min_row=2, min_col=5, max_col=5):
        for c in row:
            c.number_format = "yyyy-mm-dd"
    wb.save(os.path.join(target, W.FILES["dilution"]))
    return results


def run_log(target, specimens):
    """The LIMS run log: one row per received aliquot, with the batch's control thresholds."""
    rng = random.Random(W.SEED + 41)
    rows = []
    for s in specimens:
        aliquots = ["A1", "A2"] if s["replated"] else ["A1"]
        batch = "B27%03d" % (100 + (s["received"].toordinal() % 7) * 3 + s["instrument"].count("B"))
        # the control threshold is set for the instrument and held; it was lowered after the March
        # control review
        threshold = 36.50 if s["received"] >= dt.date(2027, 4, 12) else 36.60
        for al in aliquots:
            hour = min(17, max(7, int(rng.gauss(11.4, 2.6))))
            rows.append([s["specimen_id"], al, s["request_id"],
                         "%sT%02d:%02d" % (s["received"].isoformat(), hour, rng.randint(0, 59)),
                         "Reception %s" % ("1" if rng.random() < 0.72 else "2"), s["project"],
                         s["agreement"], batch, PK.nb(threshold, 2),
                         W.PEOPLE["lead"].split()[1][:2].upper() if rng.random() < 0.3 else "TK"])
    rows.sort(key=lambda r: (r[3], r[0], r[1]))
    PK._write(os.path.join(target, W.FILES["runlog"]),
              ["specimen_id", "aliquot_id", "request_id", "received_local", "reception_point",
               "project_code", "agreement_ref", "batch_id", "control_threshold_het_pct",
               "received_by"], rows, delim=";")
    return len(rows)


def costs(target):
    rows = [["identity panel, per specimen", "1 184", "2027-01-01", "partner laboratory price list"],
            ["DNA re-extraction, per specimen", "? 612".replace("? ", ""), "2027-01-01", "internal rate"],
            ["re-sequencing, per specimen", "2 940", "2027-01-01", "internal rate"],
            ["confirmatory review, per hour", "1 075", "2027-01-01", "internal rate"],
            ["courier, per batch", "486", "2027-01-01", "framework agreement"]]
    PK._write(os.path.join(target, W.FILES["costs"]),
              ["item", "unit_cost_nok", "effective_from", "source"], rows)
    return len(rows)
