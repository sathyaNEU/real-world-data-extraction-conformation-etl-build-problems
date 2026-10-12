"""The fixed world of task185: Southward Mutual's vineyard heat-day cover for Merrin Valley Winegrowers Co-operative,
priced off the Merrin Flat weather station, whose glass maximum thermometer in a large wooden screen gave way on
1 November 1995 to an electronic probe in a small plastic shield. Every other module reads its constants here."""
import datetime as dt

SEED = 185
INSURER = "Southward Mutual"
COOP = "Merrin Valley Winegrowers Co-operative"
COOP_SHORT = "Merrin Valley Winegrowers"
SERVICE = "National Climate Service"
STATION = "Merrin Flat"
OLD_ID = "041207"            # the station number while the glass was read by the research station's observer
NEW_ID = "041391"            # the number the network gave the automatic station
AS_OF = dt.date(2027, 8, 27)            # the extracts the quote is built from
QUOTE_DATE = dt.date(2027, 9, 6)
RENEWAL = dt.date(2027, 11, 1)          # the co-operative's cover renews
COVER_START = dt.date(2027, 12, 1)      # the 2027/28 season the quote prices

# the station record
RECORD_START = dt.date(1964, 7, 1)
CHANGE = dt.date(1995, 11, 1)           # the probe in the small shield becomes the official instrument
CHECK_END = dt.date(1998, 4, 30)        # the glass was read beside it as a check to here
APPROVED_TO = dt.date(2027, 6, 30)      # approved automatic-station readings; provisional after
RECORD_END = AS_OF
FIRST_SEASON, LAST_SEASON = 1965, 2026  # pricing record: 1965/66 to 2026/27
PRICED_SEASON = 2027                    # 2027/28

# the cover's 2027/28 terms (per insured hectare, per season)
HEAT_C, SEVERE_C = 35.0, 40.0
DEDUCTIBLE_DAYS = 14
HEAT_RATE = 40.0          # dollars for each heat day after the season's first fourteen
SEVERE_RATE = 60.0        # dollars for each severe heat day (a severe day is also a heat day)
CAP = 1500.0              # dollars a hectare a season
LOADING = 1.32

# the co-operative's sub-districts (the 2025 redraw kept the four names and moved blocks between them)
SUB_DISTRICTS = ["Upper Merrin", "Lower Merrin", "Kerrin Flats", "Tolbin"]
REDRAW = dt.date(2025, 7, 1)
COVER_FIRST_SEASON = 2019     # the co-operative has held the cover since 2019/20
BOOK_SALT = 0                 # the book's random stream (chosen so every sub-district's figures move under each device)

# the terms each season was written on (the 2027/28 quote's terms above): deductible days, heat-day and severe-day
# rates, cap a hectare
TERMS_HISTORY = {2019: (16, 36.4, 52.8, 1200.0), 2020: (16, 36.4, 52.8, 1200.0), 2021: (16, 36.4, 52.8, 1200.0),
                 2022: (16, 36.4, 52.8, 1200.0), 2023: (15, 38.6, 55.7, 1350.0), 2024: (15, 38.6, 55.7, 1350.0),
                 2025: (15, 38.6, 55.7, 1350.0), 2026: (15, 38.6, 55.7, 1350.0)}
# the day the Service released each season's approved readings, and the mutual's final run after it
APPROVAL = {2019: dt.date(2020, 6, 29), 2020: dt.date(2021, 7, 19), 2021: dt.date(2022, 8, 8),
            2022: dt.date(2023, 6, 27), 2023: dt.date(2024, 7, 15), 2024: dt.date(2025, 9, 2),
            2025: dt.date(2026, 7, 23), 2026: dt.date(2027, 7, 21)}

PEOPLE = {
    "portfolio": ("Rachel Ballard", "Weather Portfolio Manager, " + INSURER),
    "analyst": ("Jack Castro", "Pricing Analyst, " + INSURER),
    "climate": ("Richard Strickland", "Climate Data Officer, " + SERVICE),
    "coop": ("Bonnie Barr", "General Manager, " + COOP),
}


def season_of(d):
    """The season (named by its first year) a date falls in, or None outside 1 December to the end of February."""
    if d.month == 12:
        return d.year
    if d.month in (1, 2):
        return d.year - 1
    return None


def season_days(s):
    d0, d1 = dt.date(s, 12, 1), dt.date(s + 1, 3, 1) - dt.timedelta(days=1)
    return [d0 + dt.timedelta(k) for k in range((d1 - d0).days + 1)]


def season_label(s):
    return "%d/%02d" % (s, (s + 1) % 100)
