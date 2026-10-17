"""Read the shipped pack as a solver would: the gauge's climatic-year 7-day low flows from the daily values, the
water-works reports from the historical society's PDF, the Stage 2 periods from the notices, and the water supplied to
the town's own system from the plant's SCADA days, Elm Hollow's master meter and the wells."""
import csv
import datetime as dt
import os
import re

import numpy as np

import world as W


def path(target, key):
    return os.path.join(target, W.FILES[key])


def read_csv(target, key):
    with open(path(target, key), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def daterange(a, b):
    return [a + dt.timedelta(days=i) for i in range((b - a).days + 1)]


def gauge(target):
    """[(date, cfs, qual)] from the Survey's export: comment lines and the field-width row skipped."""
    out = []
    with open(path(target, "gauge"), encoding="utf-8") as fh:
        lines = [l.rstrip("\n") for l in fh if not l.startswith("#")]
    head = lines[0].split("\t")
    for line in lines[2:]:
        r = dict(zip(head, line.split("\t")))
        out.append((dt.date.fromisoformat(r["date"]), float(r["discharge_cfs"]), r["qual"]))
    return out


def gauge_minima(target, approved_only=True):
    """{climatic year: 7-day low flow} for the complete climatic years (of approved record unless told otherwise)."""
    rows = gauge(target)
    days = [d for d, _, _ in rows]
    q = np.array([v for _, v, _ in rows])
    qual = [c for _, _, c in rows]
    m7 = np.convolve(q, np.ones(7) / 7, mode="full")[:len(q)]
    out = {}
    years = sorted({W.climatic_year(d) for d in days})
    cy = [W.climatic_year(d) for d in days]
    for y in years:
        ys = [i for i, c in enumerate(cy) if c == y]
        if days[ys[0]] != dt.date(y, 4, 1) or days[ys[-1]] != dt.date(y + 1, 3, 31):
            continue
        idx = [i for i in ys if i >= 6]
        if approved_only and any(not qual[i].startswith("A") for i in idx):
            continue
        out[y] = float(min(m7[i] for i in idx))
    return out


def pdf_text(p):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in PdfReader(p).pages))


ROW = re.compile(r"\b(18[89]\d|19[0-4]\d|1950) (Report not found|No stoppage|"
                 r"(?:(?:Jan|Feb|March|April|May|June|July|Aug|Sept|Oct|Nov|Dec)\.? \d{1,2} to "
                 r"(?:Jan|Feb|March|April|May|June|July|Aug|Sept|Oct|Nov|Dec)\.? \d{1,2}(?:; )?)+)"
                 r"(?: ([\d,]+) gal\.| (\d+\.\d\d) sec\.-ft\.)?")


def reports(target):
    """{year: ("measured", cfs) | ("none", None) | ("missing", None)} from the transcription's table."""
    text = pdf_text(path(target, "reports"))
    out = {}
    for m in ROW.finditer(text):
        y = int(m.group(1))
        if y < W.FIRST_REPORT or y in out:
            continue
        status = m.group(2)
        if status == "Report not found":
            out[y] = ("missing", None)
        elif status == "No stoppage":
            out[y] = ("none", None)
        elif m.group(3):
            out[y] = ("measured", W.cfs(int(m.group(3).replace(",", "")) / 1e6))
        else:
            out[y] = ("measured", float(m.group(4)))
    return out


def annual_record(target):
    """{climatic year: (kind, cfs)}: gauged for 1951 to 2024, the reports' years before."""
    out = dict(reports(target))
    for y, v in gauge_minima(target).items():
        if W.FIT_YEARS[0] <= y <= W.FIT_YEARS[1]:
            out[y] = ("gauged", v)
    return out


def stage2_periods(target):
    rows = read_csv(target, "notices")
    out, open_ = [], None
    for r in rows:
        if r["stage"] != "Stage 2":
            continue
        if r["action"] == "Declared":
            open_ = dt.date.fromisoformat(r["in_effect_from"])
        elif open_:
            out.append((open_, dt.date.fromisoformat(r["in_effect_through"])))
            open_ = None
    return out


def scada(target):
    """{(date, tag): total}, one value per day and tag (the historian's re-sent rows carry the same values)."""
    out = {}
    for r in read_csv(target, "scada"):
        out[(dt.date.fromisoformat(r["Date"]), r["Tag"])] = float(r["DailyTotal"])
    return out


def elm_hollow(target):
    return {dt.date.fromisoformat(r["read_date"]): float(r["consumption_kgal"]) / 1000.0
            for r in read_csv(target, "elmhollow")}


def well_log(target):
    """{day: MG pumped} from the operator's round sheets: each morning's reading less the day before's closes that
    day."""
    rows = read_csv(target, "welllog")
    out = {}
    for a, b in zip(rows, rows[1:]):
        out[dt.date.fromisoformat(a["log_date"])] = (int(b["totalizer_gal"]) - int(a["totalizer_gal"])) / 1e6
    return out


def own_supply(target, log_shift=0):
    """{day: MG supplied to the Quillfield distribution system}: finished water less Elm Hollow's wholesale water, plus
    the wells (the historian until the wellfield telemetry failed, the operator's log after). log_shift=1 assigns each
    morning-to-morning difference to the later day instead."""
    sc = scada(target)
    eh = elm_hollow(target)
    wl = well_log(target)
    if log_shift:
        wl = {d + dt.timedelta(days=1): v for d, v in wl.items()}
    out = {}
    for (d, tag), v in sc.items():
        if tag != "WTP_FIN_TOTAL" or d not in eh:
            continue
        wells = wl.get(d) if d >= W.RADIO_FAILED else sc.get((d, "HR_WELLS_TOTAL"))
        if wells is None:
            continue
        out[d] = v - eh[d] + wells
    return out
