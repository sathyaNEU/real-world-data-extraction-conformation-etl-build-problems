"""Write the evidence pack (target/) of architecture 3 from the truth in world.py. Each file is written the way its source system
writes it; nothing here describes the data."""
import csv
import datetime as dt
import os
import re
import zipfile

import params as P
import world as W

D = dt.date
TD = dt.timedelta
FIXED_ZIP_TIME = (2026, 10, 19, 8, 30, 0)


# ------------------------------------------------------------------------------------------------- helpers
def write_csv(path, header, rows, delim=","):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, delimiter=delim, lineterminator="\n")
        wr.writerow(header)
        for r in rows:
            wr.writerow(["" if v is None else v for v in r])


def normalise_zip(path, when="2026-10-01T07:40:00Z", app="Microsoft Excel"):
    """Rewrite an OOXML container with fixed member times and order and the document dates set to the export's own
    date, so two builds are byte-identical."""
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    fixed = []
    for name, data in items:
        if name == "docProps/app.xml":
            data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + app.encode() + b"</Application>", data)
            data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
        if name == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + when.encode() + rb"\g<2>", data)
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + when.encode() + rb"\g<2>",
                          data)
        fixed.append((name, data))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in fixed:
            zi = zipfile.ZipInfo(name, date_time=FIXED_ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)


def xlsx_props(wb, creator, title, when):
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = when
    wb.properties.modified = when
    wb.properties.title = title


def postcode(street):
    h = sum(ord(ch) * (i + 7) for i, ch in enumerate(street))
    num = 2981 + h % 17
    letters = "ABCDEGHJKLMNPRSTVWXZ"
    return "%d %s%s" % (num, letters[h % 20], letters[(h // 20) % 20])


def nl_local(t_utc):
    return t_utc + TD(hours=W.nl_offset_hours(t_utc))


def utc_from_local(y, m, d, hh, mm=0):
    """UTC datetime for a Dutch local wall time (no ambiguous hours are used)."""
    loc = dt.datetime(y, m, d, hh, mm)
    for off in (2, 1):
        u = loc - TD(hours=off)
        if W.nl_offset_hours(u) == off:
            return u, off
    raise ValueError(loc)


