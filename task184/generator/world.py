"""The fixed world of task184 (architecture 2): Kelverstoke's Harbourgate quarter, the offence classes the 2027
tasking contract covers, the shape of each class's occurrence window, the week's four-hour patrol slots and the two
seasons on record. Every other module reads its constants from here."""
import datetime as dt

SEED = 184
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
    "Theft from a motor vehicle": (2600, "mixed_park",   [1.15, 1.10, 1.32, 1.20, 1.35, 1.25, 0.85]),
    "Theft of a pedal cycle":     (2100, "lockup",       [1.20, 1.20, 1.15, 1.20, 1.30, 0.95, 0.70]),
    "Criminal damage":            (3800, "closed_hours", [0.760, 0.760, 1.000, 1.281, 3.125, 4.950, 1.978]),
    "Burglary business":          (2660, "closed_hours", [1.281, 1.281, 1.559, 1.281, 1.786, 1.000, 0.396]),
    "Burglary residential":       (1350, "absence",      [1.20, 1.20, 1.15, 1.10, 1.20, 0.90, 0.80]),
    "Theft from the person":      (780,  "point_day",    [1.10, 1.05, 1.05, 1.15, 1.35, 1.45, 0.75]),
    "Assault without injury":     (1180, "point_night",  [0.90, 0.80, 1.00, 1.30, 2.20, 2.70, 1.30]),
    "Public order":               (1460, "point_night",  [0.80, 0.80, 1.00, 1.20, 2.30, 2.80, 1.30]),
    "Shoplifting":                (2240, "point_day",    [1.20, 1.10, 1.10, 1.20, 1.40, 1.50, 0.60]),
}

# the classes the 2027 tasking contract covers
CONTRACTED = ("Theft from a motor vehicle", "Theft of a pedal cycle", "Criminal damage", "Burglary business",
              "Burglary residential")

PEOPLE = {
    "manager": ("Bethan Murray", "Community Safety Manager"),
    "analyst": ("Adrian Daniels", "Community Safety Analyst"),
    "inspector": ("Rosie Kelly", "Neighbourhood Inspector"),
    "chair": ("Joshua Davies", "Chair of the Partnership Board"),
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
