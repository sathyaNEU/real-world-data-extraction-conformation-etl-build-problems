"""Constants and file helpers shared by the task188 generator.

Harlow Reach Credit Union is fictional; every member, acquirer, platform, supplier and person in the pack
is invented. The pack is the credit union's own extracts for the Financial Intelligence Unit's January 2027
review of its cash-intensive business members.
"""
import csv
import datetime as dt
import io
import os
import re
import zipfile

SEED = 18802
YEAR = 2026
PULL = dt.date(2027, 1, 8)          # the extract date every shipped file carries
EXPORT_TIME = (2027, 1, 8, 7, 40, 0)
MEETING = dt.date(2027, 1, 20)

ORG = "Harlow Reach Credit Union"
ORG_SHORT = "HRCU"
PRODUCER = "Harlow Reach Credit Union, Compliance"

# Pacific time: UTC-8 standard, UTC-7 daylight from the second Sunday of March to the first Sunday of
# November (2026: 8 March 02:00 to 1 November 02:00 local).
DST_START = dt.datetime(2026, 3, 8, 10, 0)   # 02:00 PST in UTC
DST_END = dt.datetime(2026, 11, 1, 9, 0)     # 02:00 PDT in UTC


def utc_offset_hours(local_naive):
    """Offset of Pacific local time from UTC for a naive local datetime in 2026 or early 2027."""
    if dt.datetime(2026, 3, 8, 2, 0) <= local_naive < dt.datetime(2026, 11, 1, 2, 0):
        return -7
    return -8


def local_to_utc(local_naive):
    return local_naive - dt.timedelta(hours=utc_offset_hours(local_naive))


def utc_to_local(utc_naive):
    if DST_START <= utc_naive < DST_END:
        return utc_naive + dt.timedelta(hours=-7)
    return utc_naive + dt.timedelta(hours=-8)


# British Columbia statutory holidays in 2026 on which the credit union is closed, plus 26 December.
HOLIDAYS = {dt.date(2026, 1, 1), dt.date(2026, 2, 16), dt.date(2026, 4, 3), dt.date(2026, 5, 18),
            dt.date(2026, 7, 1), dt.date(2026, 8, 3), dt.date(2026, 9, 7), dt.date(2026, 9, 30),
            dt.date(2026, 10, 12), dt.date(2026, 11, 11), dt.date(2026, 12, 25), dt.date(2026, 12, 26),
            dt.date(2027, 1, 1)}


def is_business_day(d):
    return d.weekday() < 5 and d not in HOLIDAYS


def next_business_day(d, k=1):
    """The k-th business day after d."""
    out = d
    n = 0
    while n < k:
        out = out + dt.timedelta(days=1)
        if is_business_day(out):
            n += 1
    return out


def business_day_on_or_after(d):
    out = d
    while not is_business_day(out):
        out = out + dt.timedelta(days=1)
    return out


DAYS = [dt.date(2026, 1, 1) + dt.timedelta(days=i) for i in range(365)]


def quarter_of(d):
    return (d.month - 1) // 3 + 1


def money(x):
    """Round to the cent the way the core writes it."""
    return float("%.2f" % (x + 0.0))


def write_csv(path, header, rows, crlf=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n" if crlf else "\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def freeze_zip(path, app_name, stamp_iso="2027-01-08T07:40:00Z", app_version="16.0300"):
    """Rewrite an Office file so two builds give identical bytes: fixed member times, the issuing
    organisation as the application, fixed core property dates and no author."""
    with zipfile.ZipFile(path) as zf:
        items = []
        for i in sorted(zf.infolist(), key=lambda x: x.filename):
            data = zf.read(i.filename)
            if i.filename == "docProps/app.xml":
                data = re.sub(rb"<Application>[^<]*</Application>",
                              b"<Application>" + app_name.encode() + b"</Application>", data)
                data = re.sub(rb"<AppVersion>[^<]*</AppVersion>",
                              b"<AppVersion>" + app_version.encode() + b"</AppVersion>", data)
            if i.filename == "docProps/core.xml":
                data = re.sub(rb">[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]{8}(\.[0-9]+)?Z<",
                              b">" + stamp_iso.encode() + b"<", data)
                for tag in (rb"dc:creator", rb"cp:lastModifiedBy", rb"dc:description"):
                    data = re.sub(rb"(<" + tag + rb"[^>]*>)[^<]*(</" + tag + rb">)", rb"\1\2", data)
            items.append((i, data))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for info, data in items:
            zi = zipfile.ZipInfo(info.filename, date_time=EXPORT_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = info.external_attr
            zf.writestr(zi, data)
