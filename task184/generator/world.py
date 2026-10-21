"""The fixed world of task184 (architecture 2): Kelverstoke's Harbourgate quarter, the offence classes the 2027
tasking contract covers, the shape of each class's occurrence window, the week's four-hour patrol slots and the two
seasons on record. Every other module reads its constants from here."""
import datetime as dt

SEED = 184
LOC_SHIFT = 0.981                          # fixed at design: the quarter's location shares sit mid-bin
NUDGE = 37                               # fixed at design: the draw whose 43 graded figures sit mid-bin
CITY = "Kelverstoke"
QUARTER = "Harbourgate"
PARTNERSHIP = "Kelverstoke Community Safety Partnership"
FORCE = "Kelverstoke City Police"
CURRENCY = "GBP"
AS_OF = dt.date(2027, 1, 22)              # the extract Community Safety works from
PAPER_DATE = dt.date(2027, 1, 29)

SLOT_H = 4
SLOTS = [(d, h) for d in range(7) for h in range(0, 24, SLOT_H)]          # 42 candidates
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
CAP = 8                                   # slots the contract buys a week
SEASONS = [(dt.date(2025, 4, 1), dt.date(2025, 9, 30)), (dt.date(2026, 4, 1), dt.date(2026, 9, 30))]

# the quarter's five recorded locations
LOCATIONS = ["Harbourgate Street", "Quayside Multi-Storey", "Lamphouse Lane", "Fishmarket Square",
             "Netherbow Car Park"]

# class: (offences a season, window kind, weekday weights Monday first)
# The five classes the contract covers are offences against something that sits in the quarter all season
# and whose keeper looks at it on a routine, so their occurrence reaches the record as the gap in that
# routine it fell in: kind "routine", and the weekday weights are unused because the day of the week is part
# of the quarter's own clock (INTENSITY below). The four witnessed classes are reported as they happen and
# carry a time: kinds point_night (20:00 to 05:00) and point_day (the market from 04:00, and the trading
# day), with their own weekday weights.
CLASSES = {
    "Theft from a motor vehicle": (2600, "routine",      [1.0] * 7),
    "Theft of a pedal cycle":     (2100, "routine",      [1.0] * 7),
    "Criminal damage":            (3800, "routine",      [1.0] * 7),
    "Burglary business":          (2660, "routine",      [1.0] * 7),
    "Burglary residential":       (1350, "routine",      [1.0] * 7),
    "Theft from the person":      (780,  "point_day",    [1.10, 1.05, 1.05, 1.15, 1.35, 1.45, 0.75]),
    "Assault without injury":     (1186, "point_night",  [0.90, 0.80, 1.00, 1.30, 2.20, 2.70, 1.30]),
    "Public order":               (1465, "point_night",  [0.80, 0.80, 1.00, 1.20, 2.30, 2.80, 1.30]),
    "Shoplifting":                (2240, "point_day",    [1.20, 1.10, 1.10, 1.20, 1.40, 1.50, 0.60]),
}

# ---------------------------------------------------------------------------------------------------------
# The quarter's clock, and the keepers whose routines turn it into occurrence windows.
#
# A covered offence happens at an hour drawn from the quarter's own property-crime clock, against a target
# whose keeper looks at it on a routine. The force records the occurrence as the gap in that routine the
# hour fell in, which is what a victim can vouch for: the premises closed and opened again, the vehicle left
# and returned to, the cycle locked and found gone. An offence in a watched hour is seen at the time and
# carries a time to the minute instead.
#
# Two properties of the world, not of any clause, that the construction rests on.
#   * The routine belongs to the target and the hour to the clock, so which gap a recorded offence carries
#     does not depend on where inside that gap the offence fell: one routine's gaps tile the week.
#   * The gap covering a night is as long as that keeper's closure, so a keeper who shuts for the weekend
#     carries Friday and Saturday nights in one window of 39 to 64 hours and a midweek night in one of 14
#     to 16. The quarter's heaviest nights therefore sit inside its longest windows.
HOURS_WEEK = 168
_WK = (0, 1, 2, 3, 4)                      # Monday to Friday
_MF = (0, 1, 2, 3, 4, 5)                   # Monday to Saturday


def _daily(a, b, days=range(7)):
    return [(d * 24 + a, d * 24 + b) for d in days]


# The hours each keeper has eyes on its own property. The terminal kiosk, the bars and the long-stay bays
# are the seven-day keepers, which is why every four-hour slot edge of the week is an edge of some routine.
WATCHED = {
    "ferry":       _daily(4, 12) + _daily(16, 20),
    "bar":         _daily(20, 24) + _daily(11, 14),
    "shop":        _daily(9, 18, _MF),
    "market":      _daily(4, 12, _MF),
    "kiosk":       _daily(7, 15, _MF),
    "office":      _daily(8, 18, _WK),
    "depot":       _daily(8, 16, _WK),
    "store":       _daily(6, 14, _WK),
    "chandler":    _daily(8, 17, _MF) + _daily(10, 14, (6,)),
    "home_eve":    _daily(17, 23) + _daily(6, 8),
    "home_shift":  _daily(7, 19),
    "home_part":   _daily(18, 23, _WK) + _daily(7, 9, _WK) + _daily(9, 23, (5, 6)),
    "home_away":   [(5 * 24 + 10, 5 * 24 + 16)],
    "bay_two":     _daily(8, 9) + _daily(18, 19),
    "bay_one":     _daily(19, 20),
    "bay_commute": _daily(7, 8, _WK) + _daily(16, 17, _WK),
    "bay_week":    [(5 * 24 + 10, 5 * 24 + 12), (2 * 24 + 18, 2 * 24 + 19)],
    "rack_day":    _daily(8, 9, _WK) + _daily(17, 18, _WK),
    "rack_eve":    _daily(19, 20),
    "rack_store":  _daily(6, 7, _MF) + _daily(21, 22, _MF),
}

# Which keepers hold each covered class's targets, and in what proportion.
ROUTINE_MIX = {
    'Criminal damage': [(0.017903, 'bar'), (0.054061, 'ferry'), (0.262271, 'shop'), (0.161398, 'market'), (0.181572, 'depot'), (0.201747, 'chandler'), (0.121048, 'kiosk')],
    'Burglary business': [(0.013283, 'bar'), (0.045840, 'ferry'), (0.256603, 'shop'), (0.192452, 'market'), (0.235219, 'office'), (0.256603, 'store')],
    'Burglary residential': [(0.339692, 'home_eve'), (0.119891, 'home_shift'), (0.382795, 'home_part'), (0.157622, 'home_away')],
    'Theft from a motor vehicle': [(0.243614, 'bay_two'), (0.170530, 'bay_one'), (0.433967, 'bay_commute'), (0.151888, 'bay_week')],
    'Theft of a pedal cycle': [(0.458507, 'rack_day'), (0.187193, 'rack_eve'), (0.354301, 'rack_store')],
}

# The quarter's property-crime clock: one night mode per night of the week, cresting at NIGHT_CREST hours
# after that day's midnight (so a value over 24 crests after it), plus a daytime shoulder from the hours the
# premises and the bays stand empty. Midweek the licences end at 23:00 and the quarter empties before
# midnight; Friday and Saturday they run late, which is why the crest moves past it.
NIGHT_CREST = [22, 21, 22, 22, 26, 26, 22]
NIGHT_AMP = [0.575027, 0.51316, 0.580725, 1.112095, 0.94908, 1.074442, 0.755436]
NIGHT_WID = 0.998287
DAY_CREST = 14.668528
DAY_WID = 2.825037
DAY_AMP = 0.224221
DAY_DOW = [0.919876, 0.913618, 0.891382, 1.022261, 1.6, 0.962006, 0.708922]
FLOOR = 0.06

# the classes the 2027 tasking contract covers
CONTRACTED = ("Theft from a motor vehicle", "Theft of a pedal cycle", "Criminal damage", "Burglary business",
              "Burglary residential")

PEOPLE = {
    "manager": ("Bethan Murray", "Community Safety Manager"),
    "analyst": ("Mitchell Webb", "Community Safety Analyst"),
    "inspector": ("Rosie Kelly", "Neighbourhood Inspector"),
    "chair": ("Joshua Davies", "Chair of the council's Community Safety Committee"),
}


def season_days(i):
    d0, d1 = SEASONS[i]
    out, d = [], d0
    while d <= d1:
        out.append(d)
        d += dt.timedelta(days=1)
    return out


def slot_label(s):
    return "%s %02d:00-%02d:00" % (DAYS[s[0]], s[1], s[1] + SLOT_H)


# the quarter's trading hours, from the business improvement district's schedule: the fish market opens at 04:00,
# the licensed premises close at 02:00 and the taxi rank clears at 05:00
TRADING = {
    0: (6, 24), 1: (6, 24), 2: (6, 24), 3: (6, 26), 4: (6, 27), 5: (4, 29), 6: (4, 24),
}

# sensor: (location, hours of the week it counts, the season it was installed)
SENSORS = {
    "FG-01": ("Harbourgate Street", "the quarter's main street at the ferry end"),
    "FG-02": ("Fishmarket Square", "the market colonnade"),
    "FG-04": ("Lamphouse Lane", "the lane between the two car parks"),
    "FG-07": ("Quayside Multi-Storey", "the car park's pedestrian exit"),
}

# the migration from the legacy crime information system to the records management system, class by class
MIGRATION = {
    "Theft from a motor vehicle": dt.date(2025, 1, 13),
    "Theft of a pedal cycle": dt.date(2025, 1, 13),
    "Criminal damage": dt.date(2025, 2, 10),
    "Burglary business": dt.date(2025, 2, 10),
    "Burglary residential": dt.date(2025, 2, 10),
    "Theft from the person": dt.date(2025, 7, 28),
    "Assault without injury": dt.date(2025, 7, 28),
    "Public order": dt.date(2025, 7, 28),
    "Shoplifting": dt.date(2025, 7, 28),
}
PARALLEL = (dt.date(2025, 7, 14), dt.date(2025, 7, 27))      # the fortnight both systems were written to

# the legacy system's own class names
LEGACY_NAMES = {
    "Theft from the person": "THEFT - FROM PERSON",
    "Assault without injury": "ASSAULT - NO INJURY",
    "Public order": "PUBLIC ORDER OFFENCE",
    "Shoplifting": "THEFT - SHOP PREMISES",
}
