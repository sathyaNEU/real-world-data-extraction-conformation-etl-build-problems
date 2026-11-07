"""Shared constants and deterministic writers for task191 (Kestrel Pay's transaction-monitoring tuning set)."""
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

SEED = 191_2604
FILE_MTIME = (2026, 11, 2, 8, 6, 0)                     # the pack's in-fiction save time, Eastern
WARM0 = dt.date(2025, 1, 2)                             # the world runs from here, so July 2025 opens mid-stream
DATA0 = dt.date(2025, 7, 1)                             # the alert export's first business date
DATA0_UTC = dt.datetime(2025, 7, 1, 4, 0)               # midnight Eastern opening 1 July 2025
DATA1 = dt.date(2026, 11, 1)                            # the last nightly run before the extract
P0, P1 = dt.date(2025, 10, 1), dt.date(2026, 9, 30)     # the tuning year, by business date
EXTRACT_UTC = dt.datetime(2026, 11, 2, 11, 0)           # the figures are drawn on Monday 2 November 2026, 06:00 Eastern
RERUN_DATE = dt.date(2026, 3, 10)                       # the business date whose run was raised again on 11 March
REPLACED_ON = dt.date(2026, 4, 1)                       # XB-HRJ replaced by XB-HRJ2 from this business date
FLOOR = 3.0                                             # per cent: productivity below it sends a scenario to tuning

# code, name, alerts per day, escalation share, SAR share of escalated, SAR decision median days and its spread,
# no-SAR investigation decision median days
SCEN = [
    ("CSH-LDS", "Cash loads under the reporting threshold at retail partners", 17.0, 0.30, 0.285, 52, 0.28, 34),
    ("CSH-VEL", "Cash-load velocity against the account's profile", 20.0, 0.10, 0.19, 70, 0.30, 38),
    ("XB-HRJ", "Cross-border transfers with high-risk jurisdictions", 8.0, 0.24, 0.24, 84, 0.30, 44),
    ("RMF-P2P", "Funds moved in and out within 72 hours", 11.0, 0.38, 0.10, 214, 0.15, 28),
    ("MUL-INF", "Many unrelated senders into one wallet", 13.5, 0.36, 0.115, 210, 0.15, 28),
    ("FAN-OUT", "Payments out to many new recipients", 10.0, 0.22, 0.285, 145, 0.21, 50),
    ("CHB-ABU", "Merchant chargeback and refund abuse", 4.0, 0.32, 0.235, 58, 0.30, 40),
    ("ATM-WDL", "Card withdrawals at many ATMs in one day", 6.0, 0.22, 0.236, 76, 0.28, 40),
    ("PRF-DEV", "Activity far outside the account's expected profile", 30.0, 0.08, 0.175, 92, 0.30, 45),
    ("DRM-REA", "Dormant account reactivated with large flows", 8.5, 0.11, 0.165, 82, 0.30, 40),
    ("MER-RND", "Round-amount payments into a merchant from few payers", 9.0, 0.44, 0.078, 228, 0.15, 30),
    ("CRY-OFF", "Transfers out to virtual asset exchanges", 7.5, 0.13, 0.155, 116, 0.24, 48),
    ("ELD-EXP", "Older customer paying new payees after a contact change", 4.6, 0.30, 0.27, 88, 0.28, 44),
    ("GMB-SPL", "Payments split across gambling merchants", 3.0, 0.35, 0.20, 96, 0.28, 46),
]
CODES = [s[0] for s in SCEN]
NAME = {s[0]: s[1] for s in SCEN}
REPLACEMENT = {"XB-HRJ": "XB-HRJ2"}


def rng(stream):
    """One independent stream per named purpose, so a change in one never shifts another."""
    h = 0
    for ch in stream:
        h = (h * 131 + ord(ch)) % (2 ** 31 - 1)
    return np.random.default_rng([SEED, h])


# ---- US Eastern time: EDT (UTC-4) from 02:00 on the second Sunday of March to 02:00 on the first Sunday of November
def _nth_sunday(y, m, n):
    d = dt.date(y, m, 1)
    d = d + dt.timedelta(days=(6 - d.weekday()) % 7)
    return d + dt.timedelta(days=7 * (n - 1))


def eastern_offset(t):
    """Hours behind UTC for an Eastern wall-clock time."""
    y = t.year
    start = dt.datetime.combine(_nth_sunday(y, 3, 2), dt.time(2, 0))
    end = dt.datetime.combine(_nth_sunday(y, 11, 1), dt.time(2, 0))
    return 4 if start <= t < end else 5


def to_utc(t):
    return t + dt.timedelta(hours=eastern_offset(t))


def to_eastern(u):
    for h in (4, 5):
        t = u - dt.timedelta(hours=h)
        if eastern_offset(t) == h:
            return t
    return u - dt.timedelta(hours=5)


def iso_z(u):
    return u.strftime("%Y-%m-%dT%H:%M:%SZ")


def quarter_label(d):
    return "%d Q%d" % (d.year, (d.month - 1) // 3 + 1)


def write_csv(path, header, rows, newline="\n"):
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


def normalise_zip(path, created, modified, app="Microsoft Excel", author="Miguel Swanson", editor=None):
    """Rewrite an Office container with fixed member order and timestamps and the workbook's own save history."""
    editor = editor or author
    with zipfile.ZipFile(path) as z:
        members = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    fixed = []
    for name, data in members:
        if name == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)",
                          lambda m: m.group(1) + created.encode() + m.group(2), data)
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                          lambda m: m.group(1) + modified.encode() + m.group(2), data)
            data = re.sub(rb"(<dc:creator[^>]*>)[^<]*(</dc:creator>)", lambda m: m.group(1) + author.encode() + m.group(2), data)
            data = re.sub(rb"(<cp:lastModifiedBy[^>]*>)[^<]*(</cp:lastModifiedBy>)",
                          lambda m: m.group(1) + editor.encode() + m.group(2), data)
            if b"<cp:lastModifiedBy" not in data:
                data = data.replace(b"</cp:coreProperties>",
                                    b"<cp:lastModifiedBy>" + editor.encode() + b"</cp:lastModifiedBy></cp:coreProperties>")
        if name == "docProps/app.xml":
            data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + app.encode() + b"</Application>", data)
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


def scrub_pdf(path, created, modified, producer=b"Kestrel Pay Document Services"):
    """Blank the writer's comment lines at equal length and set the document's own dates."""
    data = open(path, "rb").read()
    for sig in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)",
                b"ReportLab PDF Library - www.reportlab.com"):
        data = data.replace(sig, b" " * len(sig))
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (" + created.encode() + b")", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (" + modified.encode() + b")", data)
    open(path, "wb").write(data)
    set_mtime(path)
