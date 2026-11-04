"""Read the pack under target/ the way a solver must: every figure the golden, the checks and the ceiling use comes
from these parsers, never from the simulation."""
import csv
import datetime as dt
import os
import re

import pdfplumber
from openpyxl import load_workbook

import world as W

PST = dt.timezone(dt.timedelta(hours=-8))
PDT = dt.timezone(dt.timedelta(hours=-7))


def _p(target, key):
    return os.path.join(target, W.FILES[key])


def pdf_text(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join((pg.extract_text() or "") for pg in pdf.pages)


def stage(target):
    lines = open(_p(target, "stage"), encoding="utf-8").read().splitlines()
    i0 = next(i for i, l in enumerate(lines) if l.startswith("Date Time"))
    out = []
    for r in csv.reader(lines[i0 + 1:]):
        if not r:
            continue
        t = dt.datetime.strptime(r[0], "%Y-%m-%d %H:%M").replace(tzinfo=PST)
        out.append((t, float(r[1])))
    return out


def rating_table(target):
    wb = load_workbook(_p(target, "register"), read_only=True)
    ws = wb["Rating 7"]
    tab = {}
    for r in list(ws.iter_rows(values_only=True))[1:]:
        if r[0] is None:
            continue
        tab[round(float(r[0]), 2)] = float(r[1])
    return tab


def high_segment(target):
    txt = re.sub(r"\s+", " ", pdf_text(_p(target, "rating_report")))
    m = re.search(r"above (\d+\.\d+) ft: Q = ([\d.]+) \+ ([\d.]+) \(GH - (\d+\.\d+)\)\^([\d.]+?),", txt)
    return dict(top=float(m.group(1)), base=float(m.group(2)), k=float(m.group(3)), p=float(m.group(5).rstrip(".")))


def visits(target):
    out = []
    for r in csv.DictReader(open(_p(target, "visits"), encoding="utf-8")):
        d = dt.date.fromisoformat(r["visit_date"])
        s = dt.datetime.combine(d, dt.time.fromisoformat(r["meas_start_pdt"])).replace(tzinfo=PDT)
        e = dt.datetime.combine(d, dt.time.fromisoformat(r["meas_end_pdt"])).replace(tzinfo=PDT)
        a = dt.datetime.combine(d, dt.time.fromisoformat(r["arrival_pdt"])).replace(tzinfo=PDT)
        out.append(dict(date=d, arrival=a, start=s, end=e, mid=s + (e - s) / 2, gh=float(r["meas_mean_gh_ft"]),
                        q=float(r["meas_discharge_cfs"]), staff=float(r["staff_gh_ft"]), logger=float(r["logger_gh_ft"]),
                        control=r["control"], remarks=r["remarks"]))
    return out


def minimums(target):
    txt = re.sub(r"\s+", " ", pdf_text(_p(target, "license")))
    m = re.search(r"minimum flow of (\d+) cubic feet per second \(cfs\) from July 1 through September 30 and (\d+) cfs", txt)
    hi, lo = float(m.group(1)), float(m.group(2))
    return lambda day: hi if dt.date(day.year, 7, 1) <= day <= dt.date(day.year, 9, 30) else lo


def load(target):
    return dict(target=target, stage=stage(target), table=rating_table(target), hi=high_segment(target),
                visits=visits(target), minimum=minimums(target))
