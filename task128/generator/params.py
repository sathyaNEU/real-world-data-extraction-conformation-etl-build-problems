"""Fixed parameters of the task128 world (Sendalia Viajes, November 2026 patch tickets).

Everything here is a choice the fiction makes. Every figure the ladder grades is computed from the
records the generator writes, never from these constants directly.
"""
import datetime as dt

SEED = 128

AS_OF = dt.date(2026, 10, 23)            # scanner export and provider feed date
EXPORT_TIME = dt.datetime(2026, 10, 23, 6, 0)
SCORE_FIRST = dt.date(2026, 5, 1)
SCORE_LAST = dt.date(2026, 10, 22)       # latest exploit score in the history
CONVERGE_FROM = dt.date(2026, 9, 23)     # last 30 days of scores: nothing inside BAND from here
CUTS = [dt.date(2026, 5, 4), dt.date(2026, 6, 1), dt.date(2026, 7, 6), dt.date(2026, 8, 3),
        dt.date(2026, 9, 7), dt.date(2026, 10, 5)]
Q3_CUTS = CUTS[2:5]
NOV_CUT = dt.date(2026, 11, 2)
THRESH = 0.10
BAND = (0.07, 0.14)
TARGET_DAYS = 35                         # remediation target, days from first release
TICKETS = 300

ESTATES = ["payments", "checkout", "search", "media", "tools", "pipeline"]
COLO = ["payments", "checkout"]
CLOUD = ["search", "media", "tools", "pipeline"]
LABEL = {"payments": "Payments", "checkout": "Checkout", "search": "Search", "media": "Media",
         "tools": "Internal tools", "pipeline": "Data pipeline"}
CODE = {"payments": "PAY", "checkout": "CHK", "search": "SRC", "media": "MED", "tools": "INT",
        "pipeline": "DPL"}

# colocated estates (Centro de Datos Guadalhorce)
RACK = 40
TPS = {"payments": 52.0, "checkout": 34.0}
N_BY_MONTH = {"payments": {5: 444, 6: 448, 7: 452, 8: 456, 9: 460, 10: 460, 11: 460},
              "checkout": {5: 566, 6: 570, 7: 574, 8: 578, 9: 582, 10: 582, 11: 582}}
# window weekdays (Mon=0), local start hour, length in hours
WINDOWS = {"payments": ((1, 3), 20, 4), "checkout": ((0, 2), 22, 4)}
SUMMER_FREEZE = (dt.date(2026, 8, 1), dt.date(2026, 8, 16))
NOV_FREEZE = (dt.date(2026, 11, 23), dt.date(2026, 12, 1))
NOV_OFFICE = {"payments": [dt.date(2026, 11, 3), dt.date(2026, 11, 10), dt.date(2026, 11, 12),
                           dt.date(2026, 11, 17)],
              "checkout": [dt.date(2026, 11, 4), dt.date(2026, 11, 9), dt.date(2026, 11, 11),
                           dt.date(2026, 11, 16), dt.date(2026, 11, 18)]}
NOV_C = {"payments": [3, 3, 3, 3], "checkout": [3, 3, 3, 3, 3]}
NOV_C_DAY = {"payments": [3, 3, 2, 3], "checkout": [1, 1, 2, 1, 1]}
# the office's own change requests in the May to October corpus (one request per colocated ticket)
OFFICE_TEAM = "Vulnerability management"
OFFICE_N = {"payments": 25, "checkout": 23}
OFFICE_PART = {"payments": 4, "checkout": 4}

# host pools on the colocated estates: (pool, role, size, kind)
POOLS = {
    "payments": [("settle", "settlement batch", 124, "quiet"), ("report", "reporting", 56, "quiet"),
                 ("api", "payments api", 176, "active"),
                 ("gw", "api gateway", 16, "dense"), ("tok", "tokenisation", 18, "dense"),
                 ("frd", "fraud scoring", 20, "dense"), ("ntf", "notifications", 24, "dense"),
                 ("edge", "edge proxy", 26, "dense")],
    "checkout": [("basket", "basket service", 150, "quiet"), ("price", "pricing", 80, "quiet"),
                 ("web", "checkout web", 220, "active"),
                 ("gw", "api gateway", 20, "dense"), ("ses", "session store", 22, "dense"),
                 ("pro", "promotions", 26, "dense"), ("inv", "invoicing", 30, "dense"),
                 ("edge", "edge proxy", 34, "dense")],
}
# dense role package per dense pool, and its exploitable CVE count in the October advisory
DENSE = {"payments": [("gw", "nodejs", 7), ("tok", "openjdk-17-jre-headless", 6), ("frd", "python3.11", 5),
                      ("ntf", "ruby3.1", 4), ("edge", "haproxy", 3)],
         "checkout": [("gw", "envoy", 7), ("ses", "redis-server", 6), ("pro", "php8.2-fpm", 5),
                      ("inv", "dotnet-runtime-8.0", 4), ("edge", "traefik", 3)]}

# cloud estates
CLOUD_HOSTS = {"search": 640, "media": 910, "tools": 372, "pipeline": 718}
CLOUD_STANDBY = {"search": 24, "media": 31, "tools": 0, "pipeline": 17}
CLOUD_STOPPED = {"search": 6, "media": 9, "tools": 11, "pipeline": 5}
DOMAIN = {"search": "srch.sdv.internal", "media": "mda.sendalia.cloud", "tools": "tools.sdv.internal",
          "pipeline": "dp.sdv.internal"}
MEDIA_OLD_DOMAIN = "media.sdv.internal"
CLOUD_RELEASE = {"search": "noble", "media": "bookworm", "tools": "jammy", "pipeline": "noble"}
COLO_RELEASE = "el9"

PEOPLE = {"planner": "Reina Guzmán", "ciso": "Santiago Vidal", "sre": "Prudencio Cañete",
          "data": "Fabio Montalbán", "provider": "Felicia Infante", "dispatch": "Eva Mas"}
ORG = "Sendalia Viajes"
PROVIDER = "Centro de Datos Guadalhorce"
