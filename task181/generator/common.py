"""Shared constants and deterministic writers for task181 (Dalisay City dengue hotspot response)."""
import csv
import datetime as dt
import io
import os
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

SEED = 181_2027
EXPORT_DATE = dt.datetime(2027, 10, 11, 8, 0, 0)          # the line list extract, Monday of MW 41
FILE_MTIME = (2027, 10, 11, 9, 30, 0)                      # every shipped file's in-fiction export time
WINDOW = (37, 40)                                          # morbidity weeks the trigger reads, 2027
RESPONSE = (41, 44)
TRIGGER = 40


def rng(stream):
    """One independent stream per named purpose, so a change in one never shifts another."""
    h = 0
    for ch in stream:
        h = (h * 131 + ord(ch)) % (2 ** 31 - 1)
    return np.random.default_rng([SEED, h])


# ---- morbidity weeks (Sunday to Saturday; week 1 of each year as the DOH calendar sets it) ----
MW1_START = {
    2022: dt.date(2022, 1, 2),
    2023: dt.date(2023, 1, 1),
    2024: dt.date(2023, 12, 31),
    2025: dt.date(2024, 12, 29),
    2026: dt.date(2026, 1, 4),
    2027: dt.date(2027, 1, 3),
}
WEEKS_IN = {2022: 52, 2023: 52, 2024: 52, 2025: 53, 2026: 52, 2027: 52}


def mw_start(year, week):
    return MW1_START[year] + dt.timedelta(days=7 * (week - 1))


def mw_of(d):
    """(year, week) of a date under the calendar above."""
    if isinstance(d, dt.datetime):
        d = d.date()
    for y in sorted(MW1_START, reverse=True):
        if d >= MW1_START[y]:
            w = (d - MW1_START[y]).days // 7 + 1
            if y in WEEKS_IN and w > WEEKS_IN[y]:
                return (y + 1, w - WEEKS_IN[y])
            return (y, w)
    raise ValueError(d)


def all_weeks(last=(2027, 40)):
    out = []
    for y in sorted(MW1_START):
        for w in range(1, WEEKS_IN[y] + 1):
            if (y, w) > last:
                return out
            out.append((y, w))
    return out


# ---- deterministic writers ----
def write_csv(path, header, rows, newline="\r\n"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator=newline)
    w.writerow(header)
    for r in rows:
        w.writerow(["" if v is None else v for v in r])
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    set_mtime(path)


def set_mtime(path):
    t = dt.datetime(*FILE_MTIME).timestamp()
    os.utime(path, (t, t))


def normalise_zip(path):
    """Rewrite a zip container (xlsx, docx) with fixed member order and timestamps."""
    import re
    with zipfile.ZipFile(path) as z:
        members = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    stamp = "%04d-%02d-%02dT%02d:%02d:%02dZ" % FILE_MTIME
    fixed = []
    for name, data in members:
        if name == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*(</dcterms:)", lambda m: m.group(1) + stamp.encode() + m.group(2), data)
        if name == "docProps/app.xml":
            data = (b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
                    b'<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
                    b'<LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged>'
                    b'<AppVersion>16.0300</AppVersion></Properties>')
        fixed.append((name, data))
    members = fixed
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in members:
            zi = zipfile.ZipInfo(name, date_time=FILE_MTIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)
    os.replace(tmp, path)
    set_mtime(path)


def fmt_dmy(d):
    return d.strftime("%d/%m/%Y")


def fmt_iso(d):
    return d.strftime("%Y-%m-%d")


def scrub_pdf(path):
    """Blank the writer's comment lines at equal byte length, so every xref offset stays where it was."""
    data = open(path, "rb").read()
    for sig in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)"):
        data = data.replace(sig, b" " * len(sig))
    open(path, "wb").write(data)
