"""task232 world: the Coast and Ranges Local Health District's public health unit, the long day care services in the
district, the pathology laboratories that notify the unit, their clocks, and the people who own the files."""
import random
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import params as P

NSW = ZoneInfo("Australia/Sydney")
QLD = ZoneInfo("Australia/Brisbane")
UTC = timezone.utc

LHD = "Coast and Ranges Local Health District"
UNIT = "Coast and Ranges Public Health Unit"
PLATFORM = "Notifiable Conditions Platform"
PEOPLE = {
    "manager": "Haley Harper",       # manager, communicable disease surveillance
    "director": "Gilbert Ford",      # director, public health unit
    "interface": "Katrina Valdez",   # surveillance data officer, owns the feed register and the interface log
}

# The six laboratories whose electronic notifications reach the unit. clock: the clock of the authorisation and
# message timestamps the laboratory sends. codes: (sending facility code, from, to).
FEED = {
    "CRBH": dict(name="Coast and Ranges Base Hospital Laboratory", short="base hospital laboratory", clock="NSW",
                 codes=[("CRBH-MICRO", None, None)]),
    "LPG": dict(name="Larkspur Pathology", short="Larkspur", clock="NSW", codes=[("LARKSPUR", None, None)]),
    "HDN": dict(name="Halden Pathology", short="Halden", clock="NSW", codes=[("HALDEN", None, None)]),
    "KES": dict(name="Kestrel Pathology (Queensland)", short="Kestrel", clock="QLD", codes=[("KESTREL-QLD", None, None)]),
    "HPS": dict(name="Highfield Pathology Services", short="Highfield", clock="NSW",
                codes=[("HIGHFIELD", None, P.ACQUISITION - timedelta(days=1)), ("LARKSPUR-HF", P.ACQUISITION, None)]),
    "SERL": dict(name="State Enteric Reference Laboratory", short="reference laboratory", clock="UTC",
                 codes=[("SERL", None, None)]),
}


def facility_code(feed, d):
    for code, a, b in FEED[feed]["codes"]:
        if (a is None or d >= a) and (b is None or d <= b):
            return code
    raise ValueError(feed)


# New South Wales public holidays, the days centres close besides weekends and their own Christmas closure.
NSW_HOLIDAYS = [date(*t) for t in [
    (2021, 1, 1), (2021, 1, 26), (2021, 4, 2), (2021, 4, 3), (2021, 4, 4), (2021, 4, 5), (2021, 4, 25), (2021, 6, 14),
    (2021, 10, 4), (2021, 12, 25), (2021, 12, 26), (2021, 12, 27), (2021, 12, 28),
    (2022, 1, 1), (2022, 1, 3), (2022, 1, 26), (2022, 4, 15), (2022, 4, 16), (2022, 4, 17), (2022, 4, 18), (2022, 4, 25),
    (2022, 6, 13), (2022, 9, 22), (2022, 10, 3), (2022, 12, 25), (2022, 12, 26), (2022, 12, 27),
    (2023, 1, 1), (2023, 1, 2), (2023, 1, 26), (2023, 4, 7), (2023, 4, 8), (2023, 4, 9), (2023, 4, 10), (2023, 4, 25),
    (2023, 6, 12), (2023, 10, 2), (2023, 12, 25), (2023, 12, 26),
    (2024, 1, 1), (2024, 1, 26), (2024, 3, 29), (2024, 3, 30), (2024, 3, 31), (2024, 4, 1), (2024, 4, 25), (2024, 6, 10),
    (2024, 10, 7), (2024, 12, 25), (2024, 12, 26),
    (2025, 1, 1), (2025, 1, 27), (2025, 4, 18), (2025, 4, 19), (2025, 4, 20), (2025, 4, 21), (2025, 4, 25), (2025, 6, 9),
    (2025, 10, 6), (2025, 12, 25), (2025, 12, 26),
    (2026, 1, 1), (2026, 1, 26), (2026, 4, 3), (2026, 4, 4), (2026, 4, 5), (2026, 4, 6), (2026, 4, 25), (2026, 6, 8),
    (2026, 10, 5), (2026, 12, 25), (2026, 12, 26), (2026, 12, 28),
]]
HOLIDAY_SET = set(NSW_HOLIDAYS)

ROOM_KINDS = {
    # kind: (places low, high, ratio, names)
    "Nursery": (8, 12, 4, ["Joeys", "Possums", "Bilbies", "Wrens", "Seedlings", "Honeyeaters", "Gumleaves"]),
    "Toddlers": (10, 15, 5, ["Koalas", "Wombats", "Echidnas", "Lorikeets", "Sprouts", "Platypus", "Gumnuts"]),
    "Preschool": (15, 22, 10, ["Kookaburras", "Emus", "Kangaroos", "Galahs", "Wattles", "Banksias", "Pelicans"]),
}
LAYOUTS = ["A", "B", "C"]      # the three attendance export layouts centres' management software produces


def _service_id(r, used):
    while True:
        s = "SE-%08d" % r.randint(40000000, 40999999)
        if s not in used:
            used.add(s)
            return s


def build_centres(seed=P.SEED):
    r = random.Random(seed + 11)
    used = set()
    out = []
    layout_w = [0.47, 0.31, 0.22]
    for i in range(P.N_CENTRES):
        border = i < P.BORDER_CENTRES
        lay = r.choices(LAYOUTS, weights=layout_w)[0]
        opens = r.choice([6.5, 6.5, 7.0, 6.75, 7.0, 7.5])
        closes = r.choice([18.0, 18.0, 18.5, 18.25, 17.75])
        nrooms = r.choice([2, 3, 3, 3, 4, 4])
        kinds = {2: ["Toddlers", "Preschool"], 3: ["Nursery", "Toddlers", "Preschool"],
                 4: ["Nursery", "Toddlers", "Preschool", "Preschool"]}[nrooms]
        rooms = []
        taken = set()
        for k in kinds:
            lo, hi, ratio, names = ROOM_KINDS[k]
            nm = r.choice([n for n in names if n not in taken])
            taken.add(nm)
            places = r.randint(lo, hi)
            rooms.append(dict(room=nm, kind=k, places=places, ratio=ratio))
        xmas_close = r.choice([(12, 23), (12, 24), (12, 21), (12, 24)])
        xmas_open = r.choice([(1, 2), (1, 5), (1, 6), (1, 3)])
        out.append(dict(sid=_service_id(r, used), layout=lay, border=border, opens=opens, closes=closes, rooms=rooms,
                        xmas=(xmas_close, xmas_open)))
    r.shuffle(out)
    return out


def centre_open(c, d):
    """A centre runs its rooms Monday to Friday, except New South Wales public holidays and its Christmas closure."""
    if d.weekday() >= 5 or d in HOLIDAY_SET:
        return False
    (cm, cd), (om, od) = c["xmas"]
    if (d.month, d.day) >= (cm, cd) or (d.month, d.day) < (om, od):
        return False
    return True


def local(d, hours):
    """An aware New South Wales datetime for a wall-clock time `hours` after midnight on date d."""
    h = int(hours)
    m = int(round((hours - h) * 60))
    if m == 60:
        h, m = h + 1, 0
    return datetime(d.year, d.month, d.day, h, m, tzinfo=NSW)


def wall(t):
    """Wall-clock hours after midnight, New South Wales time."""
    t = t.astimezone(NSW)
    return t.hour + t.minute / 60.0 + t.second / 3600.0


def call_time(t):
    """The unit calls the family and the centre at the first moment in its calling hours (07:00 to 21:00 New South Wales
    time, every day) at or after the result reaches it."""
    t = t.astimezone(NSW)
    h = wall(t)
    if P.CALL_FROM <= h < P.CALL_TO:
        return t
    d = t.date() if h < P.CALL_FROM else t.date() + timedelta(days=1)
    return local(d, P.CALL_FROM)


def add_hours(t, hours):
    """Elapsed hours on an aware time (the arithmetic runs in UTC, so a daylight saving change is crossed correctly)."""
    return (t.astimezone(UTC) + timedelta(hours=hours)).astimezone(NSW)
