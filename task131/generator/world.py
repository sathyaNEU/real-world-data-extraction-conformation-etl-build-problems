"""Fixed world for task131: Talwerk Genossenschaft, its branches, regions, calendar and offers."""
import datetime as dt

SEED = 131_2026
EXTRACT_DATE = dt.date(2026, 9, 14)

# ISO weeks 2026-W15 (6 April) to 2026-W34 (17 to 23 August)
WEEKS = [f"2026-W{w:02d}" for w in range(15, 35)]
WEEK_START = {f"2026-W{w:02d}": dt.date.fromisocalendar(2026, w, 1) for w in range(15, 35)}
BASE = list(range(0, 8))        # W15..W22, 6 Apr to 31 May
TEST = list(range(8, 20))       # W23..W34, 1 Jun to 23 Aug
RUN = list(range(14, 20))       # W29..W34, 13 Jul to 23 Aug
EARLY = list(range(8, 14))      # W23..W28

# Regions of the network as reorganised on 1 July 2026
REGIONS = [
    ("SGS", "St. Gallen Stadt"),
    ("FUE", "Fürstenland"),
    ("RHT", "Rheintal"),
    ("TGO", "Thurgau Ost"),
    ("TOG", "Toggenburg"),
    ("APZ", "Appenzellerland"),
]
REGION_NAME = dict(REGIONS)

# branch_no, name, town, postcode, region (January 2026 edition), format, opened
BRANCHES = [
    ("1102", "St. Gallen Bahnhof", "St. Gallen", "9000", "SGS", "M", "1998-03-02"),
    ("1104", "St. Gallen Lachen", "St. Gallen", "9014", "SGS", "M", "1987-10-05"),
    ("1107", "St. Gallen Neudorf", "St. Gallen", "9008", "SGS", "L", "2004-04-19"),
    ("1109", "St. Gallen Rotmonten", "St. Gallen", "9010", "SGS", "S", "1979-06-11"),
    ("1111", "St. Gallen Winkeln", "St. Gallen", "9015", "SGS", "M", "2011-09-26"),
    ("1113", "St. Gallen St. Fiden", "St. Gallen", "9008", "SGS", "S", "1992-02-17"),
    ("1116", "Wittenbach Dorf", "Wittenbach", "9300", "SGS", "M", "2001-11-12"),
    ("2203", "Gossau Zentrum", "Gossau SG", "9200", "FUE", "L", "1995-05-08"),
    ("2205", "Gossau Mettendorf", "Gossau SG", "9200", "FUE", "S", "1983-08-29"),
    ("2207", "Flawil", "Flawil", "9230", "FUE", "M", "1990-03-12"),
    ("2209", "Degersheim", "Degersheim", "9113", "FUE", "M", "1976-04-05"),
    ("2211", "Uzwil", "Uzwil", "9240", "FUE", "M", "2006-10-16"),
    ("2214", "Oberuzwil", "Oberuzwil", "9242", "FUE", "S", "1999-01-25"),
    ("2216", "Niederbüren", "Niederbüren", "9246", "FUE", "S", "1985-07-01"),
    ("3101", "Altstätten", "Altstätten SG", "9450", "RHT", "L", "1993-09-20"),
    ("3104", "Heerbrugg", "Heerbrugg", "9435", "RHT", "M", "2008-03-31"),
    ("3107", "Rorschach Hafen", "Rorschach", "9400", "RHT", "M", "1989-05-22"),
    ("3109", "Widnau", "Widnau", "9443", "RHT", "M", "2002-06-03"),
    ("3112", "Goldach", "Goldach", "9403", "RHT", "S", "1981-11-30"),
    ("3115", "Thal", "Thal", "9425", "RHT", "S", "1997-08-18"),
    ("3118", "Oberriet", "Oberriet SG", "9463", "RHT", "S", "2010-02-08"),
    ("4101", "Arbon", "Arbon", "9320", "TGO", "L", "1994-10-03"),
    ("4103", "Romanshorn", "Romanshorn", "8590", "TGO", "M", "2000-05-15"),
    ("4105", "Egnach", "Egnach", "9322", "TGO", "S", "1978-09-04"),
    ("4107", "Amriswil", "Amriswil", "8580", "TGO", "M", "2005-03-21"),
    ("4109", "Bischofszell", "Bischofszell", "9220", "TGO", "M", "1991-12-09"),
    ("4111", "Roggwil TG", "Roggwil TG", "9325", "TGO", "S", "2013-06-24"),
    ("4113", "Sulgen", "Sulgen", "8583", "TGO", "S", "1986-02-03"),
    ("5102", "Wattwil", "Wattwil", "9630", "TOG", "L", "1996-04-29"),
    ("5104", "Lichtensteig", "Lichtensteig", "9620", "TOG", "S", "1980-10-20"),
    ("5106", "Ebnat-Kappel", "Ebnat-Kappel", "9642", "TOG", "M", "2003-07-07"),
    ("5108", "Bütschwil", "Bütschwil", "9606", "TOG", "S", "1988-01-18"),
    ("5110", "Nesslau", "Nesslau", "9650", "TOG", "S", "2009-05-04"),
    ("5112", "Bazenheid", "Bazenheid", "9602", "TOG", "M", "1997-11-24"),
    ("6101", "Herisau", "Herisau", "9100", "APZ", "L", "1990-08-13"),
    ("6103", "Appenzell", "Appenzell", "9050", "APZ", "M", "2001-03-05"),
    ("6105", "Teufen", "Teufen AR", "9053", "APZ", "M", "1995-09-11"),
    ("6107", "Gais", "Gais", "9056", "APZ", "S", "1984-06-25"),
    ("6109", "Heiden", "Heiden", "9410", "APZ", "S", "2007-01-29"),
    ("6111", "Urnäsch", "Urnäsch", "9107", "APZ", "S", "1982-04-12"),
    ("6113", "Speicher", "Speicher", "9042", "APZ", "S", "2012-10-01"),
    ("6115", "Trogen", "Trogen", "9043", "APZ", "S", "1977-05-30"),
]

# 1 July 2026 network: three Rorschach-area branches move from Rheintal to St. Gallen Stadt;
# two branches closed on 30 June, members transferred to a successor branch (Degersheim's members
# to Herisau, across the regional line; Egnach's to Arbon).
REGION_MOVES = {"3107": "SGS", "3112": "SGS", "3115": "SGS"}
CLOSURES = {"2209": "6101", "4105": "4101"}


def region_2027(branch):
    b = CLOSURES.get(branch, branch)
    if b in REGION_MOVES:
        return REGION_MOVES[b]
    return {x[0]: x[4] for x in BRANCHES}[b]


def region_january(branch):
    return {x[0]: x[4] for x in BRANCHES}[branch]


ARMS = ["K", "A", "B", "C", "D"]
OFFERS = ["A", "B", "C", "D"]
OFFER_NAME = {
    "A": "Frischbonus",
    "B": "Dreifachpunkte",
    "C": "Monatsziel",
    "D": "Wochenauswahl",
}

PEOPLE = {
    "requester": "Patrice Keller",       # head of the member programme (not named in the pack)
    "engine_owner": "Hansjürg Wolf",     # CRM and offer engine
    "finance": "Norah Burri",            # programme finance, owner of the 2027 plan
    "network": "Marta Braun",            # network planning
    "data": "Francis Amrein",            # data platform, extracts
    "analytics": "Mirjana Felder",       # programme analytics, owner of the standard
}
