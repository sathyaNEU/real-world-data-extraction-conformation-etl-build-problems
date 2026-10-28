"""task270 constants and helpers shared by every generator module.

Ostrevale is an English shire county whose county council is the fire authority. Ostrevale Fire and Rescue Service
runs six wholetime stations (two in the county town, Calderstow, one in each of the market towns Tollesham, Wrenfold,
Hollinbury and Pelmarsh) and eighteen on-call stations in the villages, across seven districts. Its 2027-2031 community
risk management plan names each district where a free engine could reach fewer than three quarters of the homes within
ten minutes across 2026. Every file was taken on Tuesday 16 February 2027 for the plan's response review."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import json
import math

import numpy as np

SEED = 2702027

COUNTY = "Ostrevale"
COUNCIL = "Ostrevale County Council"
SERVICE = "Ostrevale Fire and Rescue Service"
SERVICE_SHORT = "OFRS"
DOMAIN = "ostrevalefire.gov.uk"

PEOPLE = {
    "review": "Valerie Leach",        # area manager for response and resilience: the response review (the requester)
    "control": "Declan Evans",        # head of fire control: the mobilising system and its status codes
    "cabinet": "Roger Sykes",         # cabinet member for community safety: the cabinet report
}

AS_OF = dt.date(2027, 2, 16)          # every file taken for the response review
YEAR = 2026
MINUTES = 365 * 1440                  # the 525,600 minutes of 2026
LINE = 75.0                           # the cover standard: a district below 75 per cent is named
STANDARD_MIN = 10.0                   # attendance standard, minutes, turnout included
TURNOUT = {"Wholetime": 2.0, "On-call": 5.0}

DISTRICTS = ["Calderstow", "Tollesham", "Wrenfold", "Hollinbury", "Pelmarsh", "Altmoor", "Skirwold"]
RURAL = ["Altmoor", "Skirwold"]
LAD_CODE = {"Calderstow": "E07000291", "Tollesham": "E07000292", "Wrenfold": "E07000293", "Hollinbury": "E07000294",
            "Pelmarsh": "E07000295", "Altmoor": "E07000296", "Skirwold": "E07000297"}

# wholetime stations (code, name, x km, y km, engines) and on-call stations by district (codes, village names)
WT_STATIONS = [("10", "Calderstow", 31.4, 25.6, 2), ("11", "Calderstow East", 34.6, 24.1, 2),
               ("20", "Tollesham", 13.2, 11.3, 1), ("30", "Wrenfold", 50.8, 11.2, 1),
               ("40", "Hollinbury", 52.1, 38.7, 1), ("50", "Pelmarsh", 13.1, 38.8, 1)]
OC_STATIONS = {"Calderstow": [("12", "Midmere"), ("13", "Brinheath")],
               "Tollesham": [("21", "Skelbury"), ("22", "Cauldhope")],
               "Wrenfold": [("31", "Dunmarsh"), ("32", "Burheath")],
               "Hollinbury": [("41", "Oakhope"), ("42", "Velheath")],
               "Pelmarsh": [("51", "Nestmere"), ("52", "Thackbury")],
               "Altmoor": [("61", "Thornstead"), ("62", "Fernmere"), ("63", "Kescombe"), ("64", "Foxmoor")],
               "Skirwold": [("71", "Nedbeck"), ("72", "Langgarth"), ("73", "Ludwold"), ("74", "Kelmoor")]}
TRAINING_CENTRE = ("Brandeth", 37.0, 28.0)
TOWNS = {"Calderstow": (32.0, 25.0, 3.0, 38000), "Tollesham": (13.0, 11.0, 1.8, 12000),
         "Wrenfold": (51.0, 11.0, 1.7, 11000), "Hollinbury": (52.0, 39.0, 1.8, 12000),
         "Pelmarsh": (13.0, 39.0, 1.7, 11000)}
E0, N0 = 438000, 262000               # grid origin of the local km frame, metres

UTC = dt.timezone.utc
T0 = dt.datetime(2026, 1, 1)          # minute 0 is 00:00 UTC on 1 January 2026 (GMT, so local midnight too)

# file names
F_LOG = "mobilising_resource_log_2026.csv"
F_FLEET = "fleet_and_stations_2026.xlsx"
F_NODES = "routing_network_nodes.csv"
F_LINKS = "routing_network_links.csv"
F_ADDR = "address_register_extract.csv"
F_OALOOK = "output_area_lookup.xlsx"
F_STANDARD = "emergency_cover_standard_2027.pdf"
F_CABINET = "cabinet_report_crmp_2027_2031.pdf"
F_BOOK = "oncall_availability_bookings_2026.csv"
F_CREW = "oncall_crew_register_2026.xlsx"
F_POLICY = "oncall_duty_system_policy.pdf"
F_INC = "incident_records_2022_2026.csv"
F_CODES = "incident_classification_codes.xlsx"
F_POP = "population_estimates_mid2025.xlsx"
F_ESTAB = "station_establishment_2026.xlsx"
DISTRACTORS = [F_POP, F_ESTAB]

G_BOOK = "district_fire_cover_2026.xlsx"
G_CHART = "district_fire_cover_2026.png"


# ------------------------------------------------------------------------------------------------- clocks
def _last_sunday(y, m):
    d = (dt.date(y, m + 1, 1) - dt.timedelta(days=1)) if m < 12 else dt.date(y, 12, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def bst(t_utc):
    """True when UK clocks are on British Summer Time at UTC time t (01:00 UTC on the last Sunday of March to 01:00 UTC
    on the last Sunday of October)."""
    y = t_utc.year
    return dt.datetime.combine(_last_sunday(y, 3), dt.time(1)) <= t_utc < dt.datetime.combine(_last_sunday(y, 10), dt.time(1))


def local(t_utc):
    return t_utc + dt.timedelta(hours=1 if bst(t_utc) else 0)


def bst_minutes(year=YEAR):
    """Minute indices (from T0) of the start and end of British Summer Time in the year."""
    a = dt.datetime.combine(_last_sunday(year, 3), dt.time(1))
    b = dt.datetime.combine(_last_sunday(year, 10), dt.time(1))
    return int((a - T0).total_seconds() // 60), int((b - T0).total_seconds() // 60)


def stamp(t):
    return t.strftime("%Y-%m-%d %H:%M:%S")


# ------------------------------------------------------------------------------------------------- randomness
def rng(*keys):
    """An independent numpy stream per name (blake2b of the seed and the keys; hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def token(*keys, n=8, alphabet="0123456789"):
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=32).digest()
    return "".join(alphabet[b % len(alphabet)] for b in h[:n])


# ------------------------------------------------------------------------------------------------- writing
def write_csv(path, cols, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(["" if r.get(c) is None else r.get(c) for c in cols] if isinstance(r, dict) else r)
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return n


def write_json(path, obj, indent=None):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=indent, separators=(",", ":") if indent is None else (",", ": "))
        fh.write("\n")


def round_half_up(x, nd=0):
    q = x * 10 ** nd
    return math.floor(q + 0.5 + 1e-12) / 10 ** nd


def bin_clearance(x, step):
    """Distance from x to the nearest edge of its rounding cell, in the step's units (step/2 is the centre)."""
    q = x / step
    return step * (0.5 - abs(q - math.floor(q + 0.5)))


def long_date(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)
