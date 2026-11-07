"""Shared constants and deterministic writers for task181 (Kooralong Hospital's general surgery site infections)."""
import csv
import datetime as dt
import io
import os
import re
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

SEED = 181_2035
FILE_MTIME = (2028, 1, 4, 9, 30, 0)                   # the exports' in-fiction time, local
WIN0, WIN1 = dt.date(2027, 4, 1), dt.date(2027, 9, 30)  # the operations the response covers
REPAIR = dt.datetime(2027, 5, 12, 14, 40)              # steriliser 3 back in service after its repair, local
HIST0 = dt.date(2022, 1, 3)
TRACK0 = dt.date(2027, 1, 4)                           # the tracking export's first day
EXTRACT = dt.date(2028, 1, 4)


def rng(stream):
    """One independent stream per named purpose, so a change in one never shifts another."""
    h = 0
    for ch in stream:
        h = (h * 131 + ord(ch)) % (2 ** 31 - 1)
    return np.random.default_rng([SEED, h])


# ---- Victoria's clock: AEST (UTC+10), AEDT (UTC+11) from 02:00 on the first Sunday of October to 03:00 on the
# ---- first Sunday of April
def _first_sunday(y, m):
    d = dt.date(y, m, 1)
    return d + dt.timedelta(days=(6 - d.weekday()) % 7)


def utc_offset(t):
    """Hours ahead of UTC for a local wall-clock time."""
    y = t.year
    end = dt.datetime.combine(_first_sunday(y, 4), dt.time(3, 0))
    start = dt.datetime.combine(_first_sunday(y, 10), dt.time(2, 0))
    return 10 if end <= t < start else 11


def to_utc(t):
    return t - dt.timedelta(hours=utc_offset(t))


def to_local(u):
    """UTC to local wall clock (the offset read at the UTC instant)."""
    for h in (10, 11):
        t = u + dt.timedelta(hours=h)
        if utc_offset(t) == h:
            return t
    return u + dt.timedelta(hours=10)


# ---- the department
CONSULTANTS = ["GS-03", "GS-05", "GS-08", "GS-11", "GS-12", "GS-14", "GS-16", "GS-19", "GS-21", "GS-23"]
# share of each consultant's elective lists held in the afternoon (13:30 to about 19:30)
AFTERNOON = {"GS-03": 0.30, "GS-05": 0.25, "GS-08": 0.20, "GS-11": 0.35, "GS-12": 0.30, "GS-14": 0.25,
             "GS-16": 0.30, "GS-19": 0.25, "GS-21": 0.30, "GS-23": 0.20}
# preference trays over 10 kg (of four) each consultant holds: the colorectal open sets
HEAVY_TRAYS = {"GS-05": 4, "GS-12": 4, "GS-21": 2}
# the consultant's own effect on infection risk (the truth the review is about), by year
PRACTICE = {"GS-16": {2026: 2.4, 2027: 2.4}, "GS-21": {2027: 2.6}, "GS-08": {2025: 2.2}}
COLORECTAL = {"GS-05", "GS-12", "GS-16", "GS-21"}
EXP_RR = 4.5                                            # a tray dried short in steriliser 3 after the repair
PROCS = ["COLO", "SB", "XLAP", "APPY", "CHOL", "HER"]
PROC_NAME = {"COLO": "Colon surgery", "SB": "Small bowel surgery", "XLAP": "Exploratory laparotomy",
             "APPY": "Appendix surgery", "CHOL": "Gallbladder surgery", "HER": "Herniorrhaphy"}
# the Centre's 2026 published rates, per cent, by risk index 0 to 3 (index 3 pools 2 or more where thin)
RATES = {"COLO": (6.4, 10.3, 14.6, 19.9), "SB": (5.0, 7.9, 11.9, 16.2), "XLAP": (3.2, 5.6, 8.4, 12.4),
         "APPY": (1.7, 3.0, 4.8, 7.2), "CHOL": (1.0, 1.7, 3.0, 4.7), "HER": (1.4, 2.4, 3.7, 5.6)}
CUT_MIN = {"COLO": 180, "SB": 165, "XLAP": 145, "APPY": 75, "CHOL": 105, "HER": 115}
STERILISERS = ["S1", "S2", "S3", "S4"]


def risk_index(asa, wound, minutes, proc):
    return int(asa >= 3) + int(wound >= 3) + int(minutes > CUT_MIN[proc])


def expected_rate(proc, idx):
    return RATES[proc][min(idx, 3)] / 100.0


def poisson_upper(mu, q=0.975):
    """The Centre's upper control limit: the smallest count c with P(X <= c) >= q for X ~ Poisson(mu)."""
    from math import exp
    p = exp(-mu)
    cum = p
    c = 0
    while cum < q:
        c += 1
        p *= mu / c
        cum += p
    return c


# ---- writers
def set_mtime(path):
    t = dt.datetime(*FILE_MTIME).timestamp()
    os.utime(path, (t, t))


def write_csv(path, header, rows, newline="\n"):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator=newline)
    w.writerow(header)
    for r in rows:
        w.writerow(["" if v is None else v for v in r])
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    set_mtime(path)


def normalise_zip(path, created, modified, app="Microsoft Excel"):
    """Rewrite an xlsx or docx with fixed member order and stamps, and the owning office's save history."""
    with zipfile.ZipFile(path) as z:
        members = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    fixed = []
    for name, data in members:
        if name == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)",
                          lambda m: m.group(1) + created.encode() + m.group(2), data)
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                          lambda m: m.group(1) + modified.encode() + m.group(2), data)
        if name == "docProps/app.xml":
            data = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.'
                    b'openxmlformats.org/officeDocument/2006/extended-properties"><Application>' + app.encode() +
                    b'</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><LinksUpToDate>false'
                    b'</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged>'
                    b'<AppVersion>16.0300</AppVersion></Properties>')
        fixed.append((name, data))
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in fixed:
            zi = zipfile.ZipInfo(name, date_time=FILE_MTIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)
    os.replace(tmp, path)
    set_mtime(path)


def scrub_pdf(path):
    """Blank the writer's comment lines at equal byte length, so every xref offset stays where it was."""
    data = open(path, "rb").read()
    for sig in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)"):
        data = data.replace(sig, b" " * len(sig))
    open(path, "wb").write(data)
