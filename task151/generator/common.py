"""task151 constants and helpers shared by every generator module.

The Raleigh Oaks, a club of a fictional 30-club major league, signed five free-agent hitters between November 24 and
December 10, 2026, each contract carrying plate-appearance bonuses for the 2027 championship season. The controller
books the bonus accrual at signing under the club's accounting policy FIN-14; the files were pulled by Friday
December 11, 2026 (the as-of). Every club, player, vendor and person is fictional."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import os
import re
import zipfile

import numpy as np

SEED = 1511                  # the world draw (chosen so that every defensible construction rounds alike)
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

CLUB = "RAL"
CLUB_NAME = "Raleigh Oaks"
CLUB_LEGAL = "Triangle Baseball Club, LLC"
VENDOR = "Harlan Voss Baseball Data"
VENDOR_SHORT = "Harlan Voss"

PEOPLE = {
    "controller": "Harry Barnes",       # controller, the requester (not in the prompt)
    "agm": "Steven Armstrong",          # assistant general manager, baseball operations (owns the depth chart)
    "payroll": "Matthew Wallace",       # payroll manager
}

ASOF = dt.date(2026, 12, 11)
PULL_STAMP = dt.datetime(2026, 12, 11, 16, 5, 0)
STAMP = dt.datetime(2026, 12, 11, 15, 40, 0)
HRIS_LIVE = dt.date(2025, 1, 1)          # the club's HRIS migration (payroll history before it keeps legacy codes)
STATS_PLATFORM = 2025                    # the League's statistics platform change (box-score layout)

HIST = [2021, 2022, 2023, 2024, 2025, 2026]
LEGACY_SEASONS = [2021, 2022, 2023, 2024]
NEW_SEASONS = [2025, 2026]
SEASON = {   # opening day, last scheduled day (186 days each), All-Star break (four days without games)
    2021: (dt.date(2021, 4, 1), dt.date(2021, 10, 3), dt.date(2021, 7, 12)),
    2022: (dt.date(2022, 4, 7), dt.date(2022, 10, 9), dt.date(2022, 7, 18)),
    2023: (dt.date(2023, 3, 30), dt.date(2023, 10, 1), dt.date(2023, 7, 10)),
    2024: (dt.date(2024, 3, 28), dt.date(2024, 9, 29), dt.date(2024, 7, 15)),
    2025: (dt.date(2025, 3, 27), dt.date(2025, 9, 28), dt.date(2025, 7, 14)),
    2026: (dt.date(2026, 3, 26), dt.date(2026, 9, 27), dt.date(2026, 7, 13)),
    2027: (dt.date(2027, 3, 25), dt.date(2027, 9, 26), dt.date(2027, 7, 12)),
}
GAMES = 162
WINTER_SNAPSHOT = {y: dt.date(y, 1, 31) for y in HIST}

POSITIONS = ["C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "DH"]
LINEUP_SLOTS = list(range(1, 10))

# The world's parameters (the truth; nothing here ships). Chosen by the prototype search recorded in the design note.
PAR = dict(
    spring_p=0.16, spring_mu=3.0, spring_sig=0.9,          # placements before opening day, games lost lognormal
    stint_rate=0.9, stint_mu=2.4, stint_sig=1.05,          # in-season stints a season, games lost 9 + lognormal
    concussion_share=0.04,
    dtd_rate=1.5, rest_rate=3.0, catcher_rest=38.0,
    job_loss_p=0.06, bench_rep_p=0.25, recall_again_p=0.15,
    team_pa_mean=38.3, team_pa_sd=3.6, home_adj=-0.4,
    late_sub_p=0.05,
    trade_p=0.02,
)

# The five free-agent signings (the key is the generator's; nothing keyed ships): new slot in the club's December
# depth chart, old club and slot, contract terms. Bonus amounts and lines are each contract's own.
SIGNINGS = {
    "P4": dict(pos="3B", slot=4, old_slot=4, signed=dt.date(2026, 11, 24), years=(2027, 2027),
               salary={2027: 9_500_000}, signing_bonus=1_000_000,
               bonus=[(350_000, 475), (350_000, 525), (350_000, 600)]),
    "P1": dict(pos="1B", slot=5, old_slot=2, signed=dt.date(2026, 11, 30), years=(2027, 2029),
               salary={2027: 14_000_000, 2028: 15_000_000, 2029: 15_500_000}, signing_bonus=4_000_000,
               bonus=[(450_000, 475), (450_000, 550), (450_000, 625)]),
    "P2": dict(pos="DH", slot=6, old_slot=3, signed=dt.date(2026, 12, 3), years=(2027, 2028),
               salary={2027: 11_000_000, 2028: 11_000_000}, signing_bonus=2_000_000,
               bonus=[(500_000, 500), (500_000, 550), (500_000, 625)]),
    "P3": dict(pos="LF", slot=7, old_slot=1, signed=dt.date(2026, 12, 8), years=(2027, 2030),
               salary={2027: 16_000_000, 2028: 17_000_000, 2029: 17_000_000, 2030: 18_000_000},
               signing_bonus=5_000_000, deferred={2027: 2_000_000, 2028: 2_000_000},
               bonus=[(560_000, 525), (560_000, 575), (560_000, 650)]),
    "P5": dict(pos="2B", slot=9, old_slot=1, signed=dt.date(2026, 12, 10), years=(2027, 2028),
               salary={2027: 8_000_000, 2028: 8_500_000}, signing_bonus=1_500_000,
               bonus=[(360_000, 450), (360_000, 500), (360_000, 575)]),
}
SIGN_ORDER = ["P4", "P1", "P2", "P3", "P5"]


def rng(*keys):
    """An independent stream per purpose (season, club, player, document), so one never re-rolls another."""
    h = hashlib.sha256(("task151|%d|" % SEED + "|".join(str(k) for k in keys)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def us(d):
    return d.strftime("%m/%d/%Y") if d else ""


def iso(d):
    return d.isoformat() if d else ""


def daterange(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


def write_csv(path, header, rows, delimiter=",", crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=delimiter, lineterminator="\r\n" if crlf else "\n")
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return len(rows)


def money(x):
    return "${:,.0f}".format(x)


# ---------------------------------------------------------------------------------------------------- deterministic OOXML
def repack_ooxml(data, path, stamp, app="Microsoft Excel", creator=None):
    """Re-zip an OOXML package with fixed entry times and document properties set to the fiction's save time."""
    zin = zipfile.ZipFile(io.BytesIO(data))
    out = io.BytesIO()
    zout = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
    iso_s = stamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    for info in zin.infolist():
        body = zin.read(info.filename)
        if info.filename == "docProps/core.xml":
            txt = body.decode("utf-8")
            txt = re.sub(r"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", r"\g<1>%s\g<2>" % iso_s, txt)
            txt = re.sub(r"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", r"\g<1>%s\g<2>" % iso_s, txt)
            if creator is not None:
                txt = re.sub(r"(<dc:creator>)[^<]*(</dc:creator>)", r"\g<1>%s\g<2>" % creator, txt)
                txt = re.sub(r"(<cp:lastModifiedBy>)[^<]*(</cp:lastModifiedBy>)", r"\g<1>%s\g<2>" % creator, txt)
            body = txt.encode("utf-8")
        if info.filename == "docProps/app.xml":
            txt = body.decode("utf-8")
            txt = re.sub(r"<Application>[^<]*</Application>", "<Application>%s</Application>" % app, txt)
            body = txt.encode("utf-8")
        zi = zipfile.ZipInfo(info.filename, date_time=(stamp.year, stamp.month, stamp.day, stamp.hour, stamp.minute, 0))
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = 0o600 << 16
        zout.writestr(zi, body)
    zout.close()
    with open(path, "wb") as f:
        f.write(out.getvalue())


def save_workbook(wb, path, stamp, creator, title=""):
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.title = title
    wb.properties.created = stamp
    wb.properties.modified = stamp
    buf = io.BytesIO()
    wb.save(buf)
    repack_ooxml(buf.getvalue(), path, stamp, creator=creator)


def fix_pdf(path, stamp, producer):
    """reportlab's comment line and invariant-mode dates replaced at equal byte length (the xref offsets stay valid)."""
    b = open(path, "rb").read()

    def same_length(m):
        rep = producer.encode("latin-1")
        return (rep + b" " * len(m.group(0)))[:len(m.group(0))]

    b = re.sub(rb"ReportLab [Gg]enerated PDF document[^\n]*", same_length, b)
    old = b"D:20000101000000+00'00'"
    new = ("D:%s+00'00'" % stamp.strftime("%Y%m%d%H%M%S")).encode()
    assert len(old) == len(new)
    b = b.replace(old, new)
    assert b"ReportLab" not in b and b"reportlab" not in b
    with open(path, "wb") as f:
        f.write(b)
