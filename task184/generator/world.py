"""The fixed world of task184 (architecture 2): Kelverstoke's Harbourgate quarter, the offence classes the 2027
tasking contract covers, the shape of each class's occurrence window, the week's four-hour patrol slots and the two
seasons on record. Every other module reads its constants from here."""
import datetime as dt

SEED = 184
LOC_SHIFT = 0.9675                         # fixed at design: the quarter's location shares sit mid-bin
NUDGE = 26                               # fixed at design: the draw whose 43 graded figures sit mid-bin
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
# window kinds: point_night (witnessed, 20:00 to 05:00), point_day (witnessed, the market from 04:00 and the
# trading day), mixed_park (a vehicle left at a commuter or an evening park), lockup (a cycle locked up),
# closed_hours (a premises closed or a thing last seen in the evening and found in the morning),
# absence (a dwelling empty for a working day or a trip)
CLASSES = {
    "Theft from a motor vehicle": (2600, "mixed_park",   [0.94, 0.92, 1.32, 1.22, 1.42, 1.30, 0.86]),
    "Theft of a pedal cycle":     (2100, "lockup",       [0.98, 0.96, 1.16, 1.22, 1.38, 1.00, 0.70]),
    "Criminal damage":            (3800, "closed_hours", [0.690, 0.670, 1.000, 1.330, 3.240, 5.050, 1.978]),
    "Burglary business":          (2660, "closed_hours", [1.060, 1.040, 1.559, 1.320, 1.880, 1.000, 0.396]),
    "Burglary residential":       (1350, "absence",      [1.02, 0.99, 1.16, 1.12, 1.28, 0.92, 0.80]),
    "Theft from the person":      (780,  "point_day",    [1.10, 1.05, 1.05, 1.15, 1.35, 1.45, 0.75]),
    "Assault without injury":     (1186, "point_night",  [0.90, 0.80, 1.00, 1.30, 2.20, 2.70, 1.30]),
    "Public order":               (1465, "point_night",  [0.80, 0.80, 1.00, 1.20, 2.30, 2.80, 1.30]),
    "Shoplifting":                (2240, "point_day",    [1.20, 1.10, 1.10, 1.20, 1.40, 1.50, 0.60]),
}

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
