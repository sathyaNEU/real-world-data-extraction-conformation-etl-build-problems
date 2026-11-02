"""Fixed parameters of the task238 world (architecture 2): Saltmarsh Market, a fictional Nova Scotia grocery chain,
its fourth quarter of 2026 and the Price Watch decision for the first quarter of 2027."""
import datetime as dt

SEED = 23802
TZ = "America/Halifax"
Q_START = dt.date(2026, 10, 1)          # a Thursday
Q_END = dt.date(2026, 12, 31)           # a Thursday
ASOF = dt.date(2027, 1, 15)             # the review's date; every export pulled 2027-01-12
PULL = dt.date(2027, 1, 12)
STAMP = (2027, 1, 12, 9, 30, 0)         # mtime of every shipped file

LINE = 99.0                             # PI-2 section 4.1: below 99.0 per cent goes on Price Watch
BASE_ERR = 0.00012                       # stray-label share at any moment (missing, wrong item, torn)

# Designated retail closing days in Nova Scotia that fall in the quarter (stores closed all day).
CLOSED = [dt.date(2026, 10, 12), dt.date(2026, 11, 11), dt.date(2026, 12, 25), dt.date(2026, 12, 26)]
SHORT_CLOSE = {dt.date(2026, 12, 24): 18, dt.date(2026, 12, 31): 18}   # close at 18:00
OPEN_H = 8
CLOSE_H = 22
SUN_OPEN, SUN_CLOSE = 9, 21

# Stores: number, POS name, audit-handheld name, printer device prefix, zone, crew pattern, size, flyer-shopper
# share of a changeover Thursday (changed items' share of the day's scans), morning bump, typical print hour
# (local, Thursday; overnight crews print the Wednesday before, given as a negative offset from midnight),
# weekly spread of the print hour (hours), extra delay in the big holiday weeks (hours).
STORES = [
    # no,  pos name,                    audit name,                    dev,   zone, crew,  size,  share, morn, print, sd,  hol
    (101, "SALTMARSH QUINPOOL",       "Quinpool Road",                "QNP", 1, "night", 23800, 0.205, 0.55, -1.30, 0.30, 0.0),
    (102, "SALTMARSH SPRYFIELD",      "Spryfield",                    "SPR", 1, "day",   15400, 0.2913, 1.05, 10.55, 0.35, 0.70),
    (103, "SALTMARSH CLAYTON PK",     "Clayton Park",                 "CLP", 1, "day",   19100, 0.192, 0.70,  7.35, 0.25, 0.30),
    (104, "SALTMARSH BEDFORD PL",     "Bedford Place",                "BDF", 1, "night", 21700, 0.198, 0.40, -1.55, 0.30, 0.0),
    (105, "SALTMARSH PORTLAND ST",    "Dartmouth - Portland St",      "PTL", 1, "night", 24600, 0.214, 0.60, -1.10, 0.35, 0.0),
    (106, "SALTMARSH COLE HBR",       "Cole Harbour",                 "CLH", 1, "day",   16800, 0.1684, 0.00, 10.90, 0.40, 0.60),
    (107, "SALTMARSH SACKVILLE",      "Lower Sackville",              "SKV", 1, "day",   17900, 0.2500, 0.95, 10.85, 0.35, 0.80),
    (201, "SALTMARSH TRURO",          "Truro (Prince St)",            "TRU", 2, "night", 18300, 0.226, 0.50, -1.40, 0.30, 0.0),
    (202, "SALTMARSH NEW GLASGOW",    "New Glasgow",                  "NGL", 2, "day",   14200, 0.2350, 0.85,  8.30, 0.30, 0.45),
    (203, "SALTMARSH ANTIGONISH",     "Antigonish",                   "ANT", 2, "day",   11600, 0.2751, 0.30, 12.00, 0.45, 0.50),
    (204, "SALTMARSH KENTVILLE",      "Kentville",                    "KTV", 2, "night", 16900, 0.219, 0.45, -1.25, 0.30, 0.0),
    (205, "SALTMARSH BRIDGEWATER",    "Bridgewater",                  "BRW", 2, "day",   13900, 0.2825, 0.65,  9.40, 0.30, 3.60),
    (206, "SALTMARSH YARMOUTH",       "Yarmouth",                     "YAR", 2, "day",   12400, 0.2630, 1.10, 12.30, 0.40, 0.50),
    (207, "SALTMARSH AMHERST",        "Amherst",                      "AMH", 2, "day",   10900, 0.185, 0.35,  8.20, 0.35, 0.40),
]

HANG_RATE = 9.5        # labels a minute a day crew hangs (three associates and a cart)
HANG_RATE_SD = 0.8
NIGHT_RATE = 5.0

# Weekly changeovers, Thursdays at 00:00 local. Big holiday flyers carry more price changes.
CHANGEOVERS = [Q_START + dt.timedelta(days=7 * k) for k in range(14)]
HOLIDAY_WEEKS = {dt.date(2026, 10, 8), dt.date(2026, 10, 29), dt.date(2026, 12, 10), dt.date(2026, 12, 17),
                 dt.date(2026, 12, 24)}

AUDIT_LABELS = 160      # random price audit, labels a store a week
CHECK_LABELS = 20       # Thursday changeover check, changed labels a store a visit
CHECK_FROM, CHECK_TO = 8.0, 17.0

FILES = {
    "standard": "PI-2_price_integrity_standard_rev3.pdf",
    "hourly": "pos_hourly_item_scans_2026Q4.csv",
    "movement": "price_change_item_movement_2026Q4.csv",
    "printer": "label_printer_fleet_jobs_2026-10-01_2026-12-31.jsonl",
    "checks": "thursday_changeover_checks_Q4-2026.xlsx",
    "audits": "price_audit_results_2026Q4.csv",
    "stores": "store_directory_2027-01.xlsx",
    "desk": "service_desk_adjustments_Q4_2026.xlsx",
    "overrides": "pos_price_overrides_2026Q4.csv",
    "adplan": "flyer_ad_plan_wk40-wk53_2026.csv",
    "pricefile": "weekly_price_change_releases_2026Q4.xlsx",
    "adsales": "flyer_item_weekly_units_2026Q4.csv",
    "contacts": "customer_care_price_contacts_2026Q4.csv",
    "markdowns": "clearance_markdown_labels_2026Q4.csv",
}
DISTRACTORS = ["contacts", "markdowns"]
