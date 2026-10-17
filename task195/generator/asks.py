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

    The nightly load carries the automatic call in hetx_call and leaves it empty where the duty
    bioinformatician reviewed the specimen, whose outcome sits in review_outcome. The month a
    specimen belongs to in the laboratory's reporting pack is the month its result was released.
    """
    rng = random.Random(W.SEED + 21)
    days = [(W.HIST_FROM + dt.timedelta(days=i)) for i in range((W.HIST_TO - W.HIST_FROM).days + 1)]
    days = [d for d in days if d.weekday() < 5]
    rows = []
    per_day = W.HIST_ROWS / len(days)
    k = 0
    for d in days:
        n = int(round(per_day * (0.82 + 0.36 * rng.random())))
        for _ in range(n):
            if k >= W.HIST_ROWS:
                break
            k += 1
            lag = rng.randint(4, 26)
            rel = d + dt.timedelta(days=lag)
            while rel.weekday() > 4:
                rel += dt.timedelta(days=1)
            r = rng.random()
            status = "WITHHELD" if r < 0.023 else ("SUPERSEDED" if r < 0.044 else "RELEASED")
            hour, minute = rng.randint(7, 22), rng.randint(0, 59)
            local = dt.datetime(d.year, d.month, d.day, hour, minute)
            offset = 2 if dt.date(d.year, 3, 29) <= d < dt.date(d.year, 10, 25) else 1
            rows.append({"sid": "NFG%s-%06d" % (str(d.year)[2:], 10000 + k * 5 + (k % 11)),
                         "project": rng.choice([p[0] for p in W.PROJECTS]),
                         "extraction": rng.choices(W.EXTRACTION, [0.6, 0.28, 0.12])[0],
                         "instrument": W.INSTRUMENTS[0] if rng.random() < 0.52 else W.INSTRUMENTS[1],
                         "plate": "GKP-%s%02d-%s%02d" % (str(d.year)[2:], d.month, "ABCD"[k % 4], (k % 23) + 1),
                         "received": d, "utc": local - dt.timedelta(hours=offset),
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

    out = []
    for r in rows:
        het = rng.gauss(37.8, 0.8) if r["flag"] else rng.gauss(34.0, 1.05)
        out.append([r["sid"], r["project"], r["extraction"], r["instrument"], r["plate"],
                    r["received"].isoformat(), r["utc"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "%.1f" % r["depth"], "%.2f" % het,
                    "REVIEWED" if r["reviewed"] else "AUTO",
                    "" if r["reviewed"] else ("FLAG" if r["flag"] else "CLEAR"),
                    ("FLAGGED" if r["flag"] else "CLEARED") if r["reviewed"] else "",
                    r["status"], r["released"].isoformat() if r["released"] else ""])
    out.sort(key=lambda r: (r[5], r[0]))
    PK._write(os.path.join(target, W.FILES["history"]),
              ["specimen_id", "project_code", "extraction_method", "instrument", "plate_id",
               "received_date", "received_utc", "mean_depth", "het_excess_pct", "call_source",
               "hetx_call", "review_outcome", "release_status", "released_date"], out)
    released = {m: len(p) for m, p in by_month.items()}
    flagged = {m: sum(1 for r in p if r["flag"]) for m, p in by_month.items()}
    return len(out), released, flagged


def _slack(rate):
    """How far a per-thousand figure sits from the nearest one-decimal bin edge."""
    return abs((rate * 10) % 1 - 0.5) / 10


def _slack3(value):
    """How far a figure sits from the nearest three-decimal bin edge."""
    return abs((value * 1000) % 1 - 0.5) / 1000


def volumes(target, released_by_month):
    """The laboratory's reporting pack: specimens released each reporting month."""
    rows = []
    for m in _months():
        rows.append([m, "{:,}".format(released_by_month.get(m, 0)).replace(",", " ")])
    PK._write(os.path.join(target, W.FILES["volumes"]),
              ["reporting_month", "specimens_released"], rows)
    return len(rows)


def dilution(target):
    """The quarter's in-house dilution panel: nine replicates at each prepared level."""
    rng = random.Random(W.SEED + 31)
    wb = openpyxl.Workbook()
    thin = Side(style="thin", color="FF8A8A8A")
    head = Font(name="Calibri", size=11, bold=True)
    ws = wb.active
    ws.title = "Prepared levels"
    ws.append(["Level", "Label", "Prepared level (fraction)", "Prepared", "Operator",
               "Replicates planned"])
    for lv, label, frac in W.DILUTION:
        ws.append([lv, label, frac, dt.date(2027, 3, 11), W.PEOPLE["lead"].split()[1][:2].upper(),
                   W.DILUTION_REPLICATES])
    ws["C1"].alignment = Alignment(wrap_text=True)
    results = []
    for li, (lv, label, frac) in enumerate(W.DILUTION):
        spread = 0.21 if lv in ("L1", "L2") else (0.15 if lv == "L3" else 0.085)
        # the run itself, with the level's recovery stepped until the median the panel reports sits
        # mid-bin at the three decimals the validation file states it to
        for attempt in range(60):
            lrng = random.Random(W.SEED + 31 + li * 7 + attempt)
            rec = W.DILUTION_RECOVERY[lv] + 0.0009 * attempt
            vals = [round(max(0.0002, frac * rec * (1.0 + lrng.gauss(0.0, spread))), 4)
                    for _ in range(W.DILUTION_REPLICATES)]
            median = sorted(vals)[W.DILUTION_REPLICATES // 2]
            if _slack3(median / frac) >= 0.00042:
                break
        for i, v in enumerate(vals):
            results.append([lv if i % 3 else lv.lower(), i + 1,
                            "RS27-D%05d" % (4100 + len(results) * 3),
                            v, round(lrng.uniform(31.0, 58.0), 1), None])
        if lv == "L3":
            results.append([lv, W.DILUTION_REPLICATES + 1, "RS27-D%05d" % (4100 + len(results) * 3),
                            None, round(lrng.uniform(31.0, 58.0), 1), "voided, control failure"])
    ws2 = wb.create_sheet("Replicate results")
    ws2.append(["Level", "Replicate", "Read set", "Recovered fraction", "Mean depth", "Note"])
    for r in results:
        ws2.append(r)
    ws3 = wb.create_sheet("Panel notes")
    for line in [["Analytical sensitivity panel, 2027Q1"],
                 ["Prepared by the method group on 11 March 2027 from two anonymised cell line DNAs."],
                 ["Levels are labelled as the second contributor's share in per cent; the prepared "
                  "level column is the gravimetric fraction."],
                 ["Replicates were sequenced on GSQ-B and processed with GKJ-PIPE v3.4.1."],
                 ["Replicates reported: %d" % len([r for r in results if r[3] != ""])],
                 ["Rows voided on a control failure are kept with no result."]]:
        ws3.append(line)
    for sheet in (ws, ws2, ws3):
        sheet.freeze_panes = "A2" if sheet is not ws3 else None
        for i, width in enumerate([14, 12, 24, 18, 14, 26][:sheet.max_column], start=1):
            sheet.column_dimensions[get_column_letter(i)].width = width
        if sheet is not ws3:
            for c in sheet[1]:
                c.font = head
                c.border = Border(bottom=thin)
    for row in ws2.iter_rows(min_row=2, min_col=4, max_col=4):
        for c in row:
            c.number_format = "0.0000"
    for row in ws.iter_rows(min_row=2, min_col=3, max_col=3):
        for c in row:
            c.number_format = "0.0000"
    for row in ws.iter_rows(min_row=2, min_col=4, max_col=4):
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
        for al in aliquots:
            hour = rng.randint(7, 17)
            rows.append([s["specimen_id"], al, "REQ-2027-%05d" % (41000 + rng.randint(0, 9999)),
                         "%sT%02d:%02d" % (s["received"].isoformat(), hour, rng.randint(0, 59)),
                         "Reception %s" % ("1" if rng.random() < 0.72 else "2"), s["project"],
                         s["agreement"], "B27%03d" % (rng.randint(100, 940)),
                         PK.nb(rng.uniform(36.3, 36.7), 2),
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
