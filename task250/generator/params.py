"""task250 world parameters: Kurier Warta's October 2026 network (six sort hubs, twelve delivery depots)."""
import datetime as dt

SEED = 250
ORG = "Kurier Warta sp. z o.o."
TZ_NOTE = "Europe/Warsaw"

# the month the scorecard covers: parcels unloaded at a delivery depot on the mornings of 1 to 31 October
MONTH_FIRST, MONTH_LAST = dt.date(2026, 10, 1), dt.date(2026, 10, 31)
FIRST_PICKUP = dt.date(2026, 9, 30)
LAST_PICKUP = dt.date(2026, 10, 30)
EXTRACT = dt.datetime(2026, 11, 6, 7, 40)          # the platform extract, local time
SUMMER_END = dt.date(2026, 10, 25)                  # CEST to CET at 03:00 local on Sunday 25 October

HUBS = [  # code, name, city, base miss rate (automated sorter)
    ("HPOZ", "Komorniki", "Poznan", 0.0058),
    ("HWRO", "Bielany Wroclawskie", "Wroclaw", 0.0068),
    ("HKTW", "Sosnowiec", "Sosnowiec", 0.0142),
    ("HKRK", "Modlniczka", "Krakow", 0.0063),
    ("HLDZ", "Strykow", "Strykow", 0.0056),
    ("HWAW", "Pruszkow", "Pruszkow", 0.0055),
]
HUB_NAME = {h[0]: h[1] for h in HUBS}

# delivery depots: code, name, home hub, share of the network's deliveries, share of its pickups
DEPOTS = [
    ("D-POZ1", "Poznan-Gluszyna", "HPOZ", 0.085, 0.080),
    ("D-POZ2", "Leszno", "HPOZ", 0.050, 0.045),
    ("D-WRO1", "Wroclaw-Pracze", "HWRO", 0.105, 0.090),
    ("D-WRO2", "Opole", "HWRO", 0.048, 0.042),
    ("D-KTW1", "Katowice-Zaleze", "HKTW", 0.095, 0.085),
    ("D-KTW2", "Bielsko-Biala", "HKTW", 0.058, 0.050),
    ("D-KRK1", "Krakow-Zablocie", "HKRK", 0.098, 0.088),
    ("D-KRK2", "Tarnow", "HKRK", 0.047, 0.040),
    ("D-LDZ1", "Lodz-Olechow", "HLDZ", 0.072, 0.190),
    ("D-LDZ2", "Piotrkow Trybunalski", "HLDZ", 0.050, 0.060),
    ("D-WAW1", "Warszawa-Okecie", "HWAW", 0.160, 0.130),
    ("D-WAW2", "Warszawa-Targowek", "HWAW", 0.132, 0.100),
]
KRK_MOVE = dt.date(2026, 10, 12)          # D-KRK1 moves to Krakow-Rybitwy and becomes D-KRK3 from this day
KRK_NEW = ("D-KRK3", "Krakow-Rybitwy")
OPOLE_REHOME = dt.date(2026, 10, 19)      # from the night of 19 October D-WRO2 is sorted at HKTW (plan revision)

# volume: parcels picked up a day, the weekday pattern and the October ramp
BASE_DAILY = 3650
WEEKDAY = {0: 1.15, 1: 1.07, 2: 0.98, 3: 0.95, 4: 0.85}
RAMP_PER_DAY = 0.0088                      # the volume ramp towards the November peak

# Pruszkow's sorter: parcels a night it sorts at its planned rate; the overflow goes to Strykow's manual line
WAW_CAPACITY = 1120
WAW_P_FLOOR, WAW_P_RISE, WAW_U0 = 0.0058, 0.0145, 0.92   # miss rate rises as its sorter nears capacity
MANUAL_MISS = 0.088                        # Strykow's manual line on the overflow
CAGE = 40                                  # parcels in a roll cage
FLEX_ORIGINS_EXCLUDE = ("D-WAW1", "D-WAW2")  # the Warsaw depots' own pickups go to Pruszkow by van

ALERT_TOLERANCE = 0.0100                   # TDS-4 2.3: the alert fires when the rate exceeds 1.00 per cent
