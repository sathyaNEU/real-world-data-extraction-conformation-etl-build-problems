"""task170 shared constants: the in-fiction calendar, Carvanne Vale Railways' depots and fleets, file names, random
streams and byte-stable writers.

Elsmarra is a fictional country. Carvanne Vale Railways, its depots, units, staff numbers and every record are
invented; the Elsmarra Office of Rail Safety is a fictional regulator. ETCS, the European Train Control System, is
the signalling standard the operator fits, as any operator in Europe would."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io

import numpy as np

TASK = "task170"
OPERATOR = "Carvanne Vale Railways"
COUNTRY = "Elsmarra"
REGULATOR = "Elsmarra Office of Rail Safety"

D = dt.date
RECORD_END = D(2026, 10, 31)       # the last day in the extracts (local)
ASSEMBLED = D(2026, 11, 9)         # the pack assembled for the Phase 4 safety case
ROSTER_DATE = D(2026, 10, 31)
DUTY_START, DUTY_END = D(2026, 1, 1), D(2026, 10, 31)   # the Phase 4 depots' 2026 duty records
DUTY_MONTHS = 10

# depot code, name, phase, ETCS go-live (local date), drivers at go-live
RECORD_DEPOTS = [
    ("BRN", "Brennick", 1, D(2024, 3, 4)),
    ("TLM", "Tolmarnie", 1, D(2024, 3, 25)),
    ("ALR", "Ashlarrick Road", 2, D(2024, 11, 11)),
    ("KDB", "Keddarby", 2, D(2024, 12, 2)),
    ("MWB", "Morwennick Bridge", 2, D(2025, 1, 13)),
    ("FNJ", "Finnachy Junction", 3, D(2025, 5, 12)),
    ("SNH", "Strannoch", 3, D(2025, 7, 7)),
    ("CNC", "Cairnmorlie Central", 3, D(2025, 9, 1)),
]
PHASE4_DEPOTS = [
    ("GLH", "Glenhowrie", 4, D(2027, 2, 1)),
    ("DRC", "Drumcarra", 4, D(2027, 3, 1)),
    ("KVN", "Kilvennach", 4, D(2027, 3, 29)),
    ("ADM", "Ardmorrow", 4, D(2027, 4, 26)),
    ("MSB", "Mossbrackie", 4, D(2027, 5, 24)),
    ("FBK", "Fellbrackan", 4, D(2027, 6, 21)),
]
DEPOTS = RECORD_DEPOTS + PHASE4_DEPOTS
DEPOT = {d[0]: d for d in DEPOTS}
REC_CODES = [d[0] for d in RECORD_DEPOTS]
P4_CODES = [d[0] for d in PHASE4_DEPOTS]
# each depot's staff number block: the first two digits of every staff number Resourcing issues at that depot
BLOCK = {"BRN": 11, "TLM": 12, "ALR": 21, "KDB": 22, "MWB": 23, "FNJ": 31, "SNH": 32, "CNC": 33,
         "GLH": 41, "DRC": 42, "KVN": 43, "ADM": 44, "MSB": 45, "FBK": 46}
FLEET_BLOCK = 90                   # fleet technicians' staff numbers (test start-ups)

# file names in the pack
F_SOM = "obr_start_of_mission_log_2024-03_2026-10.csv"
F_REG = "safety_desk_register_2024-2026.xlsx"
F_ROSTER = "driver_roster_2026-10-31.xlsx"
F_XWALK = "staff_number_crosswalk.csv"
F_DUTY = "phase4_duty_records_2026.csv"
F_ROLL = "etcs_rollout_plan_2024-2027.pdf"
F_CONV = "phase4_safety_case_conventions.pdf"
F_GUIDE = "safety_desk_reporting_guidance.pdf"
F_ALLOC = "fleet_allocation_2027.csv"
F_WORKS = "etcs_fitment_works_records.xlsx"
F_FORM = "unit_formations_2026-10-31.csv"
F_RENUM = "unit_renumbering_register.csv"
F_ACCEPT = "fleet_etcs_acceptance_note.pdf"
F_DICT = "data_dictionary.txt"
F_PUNC = "punctuality_by_depot_2024-2026.xlsx"
F_WX = "depot_weather_daily_2024-2026.csv"
DISTRACTORS = [F_PUNC, F_WX]

DELIV_XLSX = "phase4_data_entry_forecast.xlsx"
DELIV_SVG = "phase4_depot_readiness.svg"

SALT = ""      # screening only: another world draw; the shipped world uses the empty salt


def stream(name):
    h = int.from_bytes(hashlib.sha256(("task170v5/" + SALT + name).encode()).digest()[:8], "little")
    return np.random.default_rng(h)


def write_csv(path, head, rows, crlf=True):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(head)
    n = 0
    for r in rows:
        w.writerow(["" if v is None else v for v in r])
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return n


def is_bst(t):
    """t a naive UTC datetime: True when Elsmarra keeps summer time (last Sunday in March 01:00 UTC to last Sunday
    in October 01:00 UTC), as the country's clocks follow the European rule"""
    y = t.year

    def last_sunday(m):
        d = dt.date(y, m, 31)
        return d - dt.timedelta(days=(d.weekday() + 1) % 7)
    start = dt.datetime.combine(last_sunday(3), dt.time(1, 0))
    end = dt.datetime.combine(last_sunday(10), dt.time(1, 0))
    return start <= t < end


def utc_to_local(t):
    return t + dt.timedelta(hours=1) if is_bst(t) else t


def local_to_utc(t):
    """naive local to naive UTC (the autumn repeated hour read as summer time)"""
    cand = t - dt.timedelta(hours=1)
    return cand if is_bst(cand) else t
