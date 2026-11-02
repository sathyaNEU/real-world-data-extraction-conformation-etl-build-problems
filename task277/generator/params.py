"""Fixed parameters of the Venlo world: calendar, assortment, customers, the pick process and its error rates."""
import datetime as dt

SEED = 27702
YEAR = 2026
EXPORT_DATE = dt.date(2027, 1, 4)            # the planning folder was pulled on the first working Monday of 2027
UPGRADE_LAST_OLD = dt.date(2026, 6, 12)      # last day picked on the old WMS (Friday)
UPGRADE_FIRST_NEW = dt.date(2026, 6, 15)     # first day on the new WMS (Monday); Saturday 13 June not picked
PORTAL_RELEASE = dt.date(2026, 7, 20)        # the store portal came back from its release counting units
PORTAL_DOWN = (dt.date(2026, 7, 11), dt.date(2026, 7, 19))   # the portal offline for the release
HOLIDAYS = {dt.date(2026, 1, 1), dt.date(2026, 4, 6), dt.date(2026, 4, 27), dt.date(2026, 5, 14),
            dt.date(2026, 5, 25), dt.date(2026, 12, 25), dt.date(2026, 12, 26)}
NEW_INNER_FROM = dt.date(2027, 1, 11)        # first receipt of the Daily range in inners of four
KPI = 99.80

# code, name, articles, inner (2026), store pack (the trade order unit), multiples k and weights,
# trade weight, webshop weight
RANGES = [
    ("DLY", "Daily", 140, 6, 6, ([1, 2, 3, 4], [.52, .26, .14, .08]), 0.50, 0.40),
    ("HAI", "Hair", 90, 12, 6, ([1, 2, 4], [.65, .25, .10]), 0.20, 0.22),
    ("SKN", "Skin", 70, 6, 3, ([1, 2, 4], [.55, .35, .10]), 0.12, 0.17),
    ("KID", "Kids", 40, 4, 4, ([1, 2, 3], [.45, .40, .15]), 0.08, 0.08),
    ("MEN", "Men", 60, 6, 4, ([1, 2, 3], [.15, .55, .30]), 0.06, 0.10),
    ("SUN", "Sun", 30, 6, 4, ([1, 2, 3], [.40, .40, .20]), 0.04, 0.03),
]
INNER_2027 = {"DLY": 4}
SUN_SEASON = {1: .25, 2: .35, 3: .7, 4: 1.3, 5: 1.9, 6: 2.1, 7: 1.7, 8: 1.0, 9: .45, 10: .25, 11: .2, 12: .3}
WEB_QTY = ([1, 2, 3, 4, 5, 6, 8, 10], [.55, .22, .10, .04, .02, .04, .02, .01])
WEB_SEASON = {1: .95, 2: .9, 3: .95, 4: 1.0, 5: 1.0, 6: .92, 7: .88, 8: .9, 9: 1.0, 10: 1.05, 11: 1.25, 12: 1.35}

# human error probability per order line by the pick it calls for; the first twenty working days on the floor
HEP = {"whole": 0.00058, "loose": 0.00105, "mixed": 0.0100}
NEW_PICKER_FACTOR = 1.7
NEW_DAYS = 20

# trade customers: code, name, stores, claim route, reference the route quotes
GROUPS = [
    ("RAV", "Ravelijn Drogist", 58, "EDI", "delivery"),
    ("HGH", "Hooghuys Drogisterij", 44, "EDI", "po"),
    ("VLM", "Vlietmarkt Supermarkten", 36, "PORTAL", "delivery"),
    ("ZLF", "Zelfstandige drogisten", 72, "PORTAL", "delivery"),
]
PLAN_GROWTH = {"T": 1.00, "W": 1.04}
