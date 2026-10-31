"""Shared constants and deterministic writers for task191 (Lorvega's municipal buses, the 2027 driver-attention
programme)."""
import csv
import datetime as dt
import io
import os
import re
import zipfile
from zoneinfo import ZoneInfo

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

SEED = 191_2026
TZ = ZoneInfo("Europe/Madrid")
UTC = dt.timezone.utc
FILE_MTIME = (2026, 11, 9, 9, 15, 0)          # every shipped file's in-fiction export time (Monday 9 November 2026)

EXTRACT_FROM = dt.date(2025, 10, 1)           # the telematics extract's first local day
WINDOW = (dt.date(2026, 1, 1), dt.date(2026, 10, 31))   # the programme's period, local dates
NETWORK_2026 = dt.date(2025, 12, 14)          # Red 2026 in service
LAST_DAY = dt.date(2026, 11, 1)               # the extract runs to the end of Sunday 1 November, local
RATIO = 1.3                                   # the programme's threshold, times the fleet's rate


def rng(stream):
    """One independent stream per named purpose, so a change in one never shifts another."""
    h = 0
    for ch in stream:
        h = (h * 131 + ord(ch)) % (2 ** 31 - 1)
    return np.random.default_rng([SEED, h])


def days(a, b):
    """Every date from a to b inclusive."""
    out, d = [], a
    while d <= b:
        out.append(d)
        d += dt.timedelta(days=1)
    return out


def local_to_utc(d, seconds):
    """A local wall-clock time (date plus seconds after midnight, may run past 24 h) as an aware UTC datetime."""
    base = dt.datetime(d.year, d.month, d.day) + dt.timedelta(seconds=int(seconds))
    return base.replace(tzinfo=TZ).astimezone(UTC)


def utc_to_local(t):
    return t.astimezone(TZ)


def iso_z(t):
    return t.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_z(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


# ---- deterministic writers ----
def set_mtime(path):
    t = dt.datetime(*FILE_MTIME).timestamp()
    os.utime(path, (t, t))


def write_csv(path, header, rows, newline="\n", delimiter=","):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator=newline, delimiter=delimiter)
    w.writerow(header)
    for r in rows:
        w.writerow(["" if v is None else v for v in r])
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    set_mtime(path)


def read_csv(path, delimiter=","):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=delimiter))


def normalise_zip(path, app="Microsoft Excel"):
    """Rewrite an OOXML container (xlsx, docx) with fixed member order and timestamps."""
    with zipfile.ZipFile(path) as z:
        members = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    stamp = "%04d-%02d-%02dT%02d:%02d:%02dZ" % FILE_MTIME
    fixed = []
    for name, data in members:
        if name == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*(</dcterms:)",
                          lambda m: m.group(1) + stamp.encode() + m.group(2), data)
            # openpyxl writes the creator with its namespace inline, so the tags are matched with any attributes.
            data = re.sub(rb"(<dc:creator[^>]*>)[^<]*(</dc:creator>)", lambda m: m.group(1) + b"EMAL" + m.group(2), data)
            data = re.sub(rb"(<cp:lastModifiedBy[^>]*>)[^<]*(</cp:lastModifiedBy>)",
                          lambda m: m.group(1) + b"EMAL" + m.group(2), data)
        if name == "docProps/app.xml":
            data = (('<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
                     '<Application>%s</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
                     '<LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
                     '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')
                    % app).encode()
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
    """Blank the writer's signature comments at equal byte length, so every xref offset stays where it was."""
    data = open(path, "rb").read()
    for sig in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)",
                b"http://www.reportlab.com", b"ReportLab"):
        data = data.replace(sig, b" " * len(sig))
    open(path, "wb").write(data)
    set_mtime(path)
