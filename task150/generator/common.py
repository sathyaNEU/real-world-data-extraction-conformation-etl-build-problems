"""task150 constants and helpers shared by every generator module.

Sorrel Creek School District RE-6 serves about 5,400 pupils in kindergarten to grade 5 at seven attendance-area
elementary schools in Brandt County on Colorado's northern Front Range. Voters approved a bond on November 4, 2025 whose
Elementary Capacity program funds 24 permanent classrooms, built during 2027-28 and in use for the school years 2028-29
to 2032-33. Board Policy FEA-R2 (adopted March 12, 2026) places them; the planning office pulled the October 1, 2026
count and its other files by Friday October 9, 2026 (the as-of)."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import os
import re
import zipfile

import numpy as np

SEED = 50
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

DISTRICT = "Sorrel Creek School District RE-6"
DISTRICT_SHORT = "Sorrel Creek RE-6"
DISTRICT_CODE = "2745"
COUNTY = "Brandt County"
COUNTY_HEALTH = "Brandt County Public Health"

PEOPLE = {
    "planning": "Stacy Frazier",    # executive director of planning and enrollment (the requester; not in the prompt)
    "sis": "Mariah Henry",          # student information systems manager
    "gis": "Joseph Hanson",         # GIS analyst
    "facilities": "Troy Medina",    # director of facilities
    "registrar": "Brian Owen",      # Brandt County vital records registrar
}

ASOF = dt.date(2026, 10, 9)                 # the planning office's pull (Friday)
PULL_STAMP = dt.datetime(2026, 10, 9, 15, 42, 0)
BOND_ELECTION = dt.date(2025, 11, 4)
POLICY_ADOPTED = dt.date(2026, 3, 12)
BOARD_MEETING = dt.date(2026, 11, 12)

# the seven schools, in the order the simulation keys them (zone letters are the generator's, never shipped)
ZONES = ["A", "B", "P", "C", "D", "E", "F"]
SCHOOLS = {
    "A": dict(name="Ortega Elementary", short="Ortega", state="6142", local="103", old_name="ORTEGA ELEM", area="ORTEGA"),
    "B": dict(name="Bluestem Elementary", short="Bluestem", state="6158", local="104", old_name="BLUESTEM ELEM", area="BLUESTEM"),
    "P": dict(name="Fifth Street Elementary", short="Fifth Street", state="6111", local="101", old_name="FIFTH ST ELEM", area="FIFTH STREET"),
    "C": dict(name="Lincoln Elementary", short="Lincoln", state="6116", local="102", old_name="LINCOLN ELEM", area="LINCOLN"),
    "D": dict(name="Kessler Elementary", short="Kessler", state="6175", local="105", old_name="SOUTHEAST ELEM", area="KESSLER"),
    "E": dict(name="Prairie Rose Elementary", short="Prairie Rose", state="6163", local="106", old_name="PRAIRIE ROSE ELEM", area="PRAIRIE ROSE"),
    "F": dict(name="North Fork Elementary", short="North Fork", state="6189", local="107", old_name="NORTH FORK ELEM", area="NORTH FORK"),
}
# the order the district lists its schools (by state code) in every shipped file
LIST_ORDER = sorted(ZONES, key=lambda z: SCHOOLS[z]["state"])
KESSLER_RENAMED = dt.date(2020, 7, 1)        # Southeast Elementary renamed for Dorothy Kessler, principal 1994-2016

# October count days: October 1, or the school day nearest it when October 1 falls on a weekend
COUNT_DAY = {
    2013: dt.date(2013, 10, 1), 2014: dt.date(2014, 10, 1), 2015: dt.date(2015, 10, 1), 2016: dt.date(2016, 9, 30),
    2017: dt.date(2017, 10, 2), 2018: dt.date(2018, 10, 1), 2019: dt.date(2019, 10, 1), 2020: dt.date(2020, 10, 1),
    2021: dt.date(2021, 10, 1), 2022: dt.date(2022, 9, 30), 2023: dt.date(2023, 10, 2), 2024: dt.date(2024, 10, 1),
    2025: dt.date(2025, 10, 1), 2026: dt.date(2026, 10, 1),
}
def count_day(y):
    """The October count day: October 1, or the nearest school day when it falls on a weekend."""
    if y in COUNT_DAY:
        return COUNT_DAY[y]
    d = dt.date(y, 10, 1)
    if d.weekday() == 5:
        return d - dt.timedelta(days=1)
    if d.weekday() == 6:
        return d + dt.timedelta(days=1)
    return d


FIRST_DAY = {   # first day of school each August
    2004: dt.date(2004, 8, 18), 2005: dt.date(2005, 8, 17), 2006: dt.date(2006, 8, 16), 2007: dt.date(2007, 8, 15),
    2008: dt.date(2008, 8, 13), 2009: dt.date(2009, 8, 19), 2010: dt.date(2010, 8, 18), 2011: dt.date(2011, 8, 17),
    2012: dt.date(2012, 8, 15), 2013: dt.date(2013, 8, 14), 2014: dt.date(2014, 8, 13), 2015: dt.date(2015, 8, 19),
    2016: dt.date(2016, 8, 17), 2017: dt.date(2017, 8, 16), 2018: dt.date(2018, 8, 15), 2019: dt.date(2019, 8, 14),
    2020: dt.date(2020, 8, 24), 2021: dt.date(2021, 8, 18), 2022: dt.date(2022, 8, 17), 2023: dt.date(2023, 8, 16),
    2024: dt.date(2024, 8, 14), 2025: dt.date(2025, 8, 13), 2026: dt.date(2026, 8, 17),
}
LAST_DAY_2027 = dt.date(2027, 5, 27)
OLD_YEARS = list(range(2013, 2019))     # the legacy student system's Octobers
NEW_YEARS = list(range(2019, 2027))     # the current system's Octobers (from the summer 2019 conversion)
YEARS = OLD_YEARS + NEW_YEARS
WINDOW = list(range(2028, 2033))        # the October counts the standard averages (2028-29 to 2032-33)
FUT = list(range(2027, 2033))
BIRTH_YEARS_SHIPPED = list(range(2008, 2026))

TOTAL_CLASSROOMS = 24
SITE_CAP = 8
SEATS = 24

# the world's parameters (the truth; nothing here ships). Chosen by the seed search recorded in the design note.
PAR = dict(
    births={
        "A": [[1999, 225], [2003, 230], [2012, 330], [2016, 330], [2022, 210], [2027, 204]],
        "B": [[1999, 98], [2027, 96]],
        "P": [[1999, 118], [2008, 150], [2012, 152], [2018, 122], [2025, 102], [2027, 100]],
        "C": [[1999, 130], [2027, 133]],
        "D": [[1999, 120], [2027, 114]],
        "E": [[1999, 84], [2011, 86], [2019, 132], [2025, 150], [2027, 152]],
        "F": [[1999, 110], [2027, 104]],
    },
    kratio={"A": 0.66, "B": 1.00, "P": 0.94, "C": 0.97, "D": 0.95, "E": 0.97, "F": 0.95},
    moves={"A>B": 0.10, "A>C": 0.004, "A>D": 0.04, "A>P": 0.005, "A>E": 0.004, "A>F": 0.004,
           "B>C": 0.004, "B>D": 0.003, "B>A": 0.004,
           "P>D": 0.009, "P>F": 0.006, "P>A": 0.004,
           "C>B": 0.004, "C>D": 0.003,
           "D>C": 0.004, "D>B": 0.004, "D>P": 0.003,
           "E>F": 0.005, "E>C": 0.003,
           "F>E": 0.005, "F>D": 0.004},
    out={"A": 0.060, "B": 0.028, "P": 0.060, "C": 0.025, "D": 0.035, "E": 0.035, "F": 0.040},
    ext={"A": 7.0, "B": 2.0, "P": 16.0, "C": 2.5, "D": 4.0, "E": 14.0, "F": 3.0},
    retain=[0.022, 0.008, 0.006, 0.004, 0.003, 0.0],
    yr_eff={2014: 1.02, 2015: 1.04, 2016: 1.03, 2017: 1.0, 2018: 0.98, 2019: 1.0, 2020: 0.92, 2021: 1.06,
            2022: 1.02, 2023: 0.96, 2024: 0.99, 2025: 1.01, 2026: 1.0},
    noise=0.5,
    # target excess (pupils above rated capacity in the golden's five-year average): each sits mid-bin
    target={"A": -100, "B": 86, "P": 108, "C": 132, "D": 60, "E": 156, "F": 12},
)


def rng(*keys):
    """An independent stream per purpose (attributes, ask worlds, documents), so one never re-rolls another."""
    h = hashlib.sha256(("task150|%d|" % SEED + "|".join(str(k) for k in keys)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def us(d):
    return d.strftime("%m/%d/%Y") if d else ""


def iso(d):
    return d.isoformat() if d else ""


def school_year(y):
    return "%d-%02d" % (y, (y + 1) % 100)


def write_csv(path, header, rows, delimiter=","):
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=delimiter, lineterminator="\r\n" if delimiter == "|" else "\n")
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return len(rows)


# ---------------------------------------------------------------------------------------------------- deterministic OOXML
STAMP = dt.datetime(2026, 10, 9, 15, 30, 0)


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


def lin(pts, y):
    xs = [p[0] for p in pts]
    vs = [p[1] for p in pts]
    return float(np.interp(y, xs, vs))
