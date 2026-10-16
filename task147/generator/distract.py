"""Two files the answer never reads: the competitor rate shop of 30 June 2027 and the city tourism office's monthly
hotel occupancy survey. Both are what a revenue or housekeeping office keeps beside the book."""
from __future__ import annotations

import datetime as dt

import common as K
import records as R

F_SHOP = "compset_rate_shop_2027-06-30.xlsx"
F_SURVEY = "callowfort_tourism_hotel_occupancy_survey_2019-2026.csv"
HOTELS = ["The Weighhouse Hotel", "Callowfort Plaza Hotel", "The Callowfort Arms", "Hotel Callowfort Central",
          "Callowfort Park Hotel", "Riverbank House Callowfort"]
FACT = [1.0, 1.08, 0.86, 0.93, 1.02, 1.15]


def shop_rows(full_nights):
    out = []
    for d in K.season_nights(K.YEAR):
        r = K.rng("shop", d.isoformat())
        row = [d]
        for h, f in zip(HOTELS, FACT):
            if h == HOTELS[0]:
                row.append("Sold out" if d in full_nights else R.bar(d))
                continue
            if d in K.CONCERT_NIGHTS and r.uniform() < 0.8:
                row.append("Sold out")
                continue
            v = R.bar(d) * f * float(r.uniform(0.94, 1.06))
            if d in K.CONCERT_NIGHTS:
                v *= 1.25
            if d.weekday() == 5 and (d - K.fest_open(K.YEAR)).days >= 0 and r.uniform() < 0.25:
                row.append("Min 2 nights")
                continue
            row.append(int(round(v)))
        out.append(row)
    return out


SURVEY_COLS = ["year", "month", "hotels_reporting", "rooms_reporting", "room_occupancy_pct", "bed_occupancy_pct"]


def survey_rows():
    base = {1: 58.2, 2: 63.5, 3: 69.8, 4: 74.1, 5: 79.4, 6: 84.9, 7: 87.6, 8: 89.9, 9: 83.1, 10: 77.5, 11: 68.3,
            12: 61.7}
    out = []
    for y in range(2019, 2027):
        for m in range(1, 13):
            r = K.rng("survey", y, m)
            v = base[m] + float(r.normal(0, 1.6)) + (y - 2022) * 0.35
            if y == 2020:
                v = (v * 0.42 if m >= 3 else v) if m not in (7, 8) else v * 0.55
            if y == 2021:
                v = v * (0.30 if m <= 5 else 0.78)
            hotels = 21 + int(r.integers(-2, 2)) + (1 if y >= 2024 else 0)
            rooms = 2840 + int(r.integers(-160, 120)) + (210 if y >= 2024 else 0)
            out.append([y, m, hotels, rooms, "%.1f" % v, "%.1f" % (v * float(r.uniform(0.71, 0.77)))])
    return out
