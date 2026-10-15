"""task140 constants and helpers shared by every generator module.

Alisio Viajes, S.L. (fictional), an online travel marketplace with its head office in Barcelona, runs its own data
centres. MAD1 (Alcobendas, Madrid) holds five compute cells, C-21 to C-25. Cell C-22 hosts eleven firm tenants, two
platform services and the batch training tier. Its quarterly capacity review strikes the batch guarantee for 2027 Q1
on Tuesday 15 December 2026 under the Cell Capacity Standard CS-3."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

SEED = 1400206
UTC = dt.timezone.utc

# ---------------------------------------------------------------------------------------------------- calendar
EXPORT_START = dt.datetime(2025, 1, 1, 0, 0, tzinfo=UTC)          # first hour of the monitoring export
EXPORT_END = dt.datetime(2026, 12, 14, 0, 0, tzinfo=UTC)          # exclusive: the last hour is 13 December 23:00
PULL = dt.datetime(2026, 12, 14, 6, 10, tzinfo=UTC)               # the export's pull
REQUESTS_CLOSE = dt.datetime(2026, 12, 4, 17, 0, tzinfo=UTC)      # 18:00 Madrid
FREEZE_NOTE = dt.date(2026, 11, 27)
RATE_PUBLISHED = dt.date(2026, 12, 1)
MEMO_DATE = dt.date(2026, 12, 9)
HWPLAN_REV = dt.date(2026, 12, 11)
REVIEW = dt.date(2026, 12, 15)
REFRESH_IN_SERVICE = dt.datetime(2026, 12, 28, 8, 0, tzinfo=UTC)
Q3_START = dt.datetime(2026, 7, 1, tzinfo=UTC)
Q3_END = dt.datetime(2026, 10, 1, tzinfo=UTC)                     # exclusive
POWER_EVENT = dt.datetime(2026, 8, 19, 1, 40, tzinfo=UTC)          # hall 2 UPS transfer fault (03:40 CEST)
COLLECTOR_GAP = (dt.datetime(2026, 8, 19, 1, 0, tzinfo=UTC), dt.datetime(2026, 8, 19, 8, 0, tzinfo=UTC))
RECONCILER_STOP = (dt.datetime(2026, 8, 19, 1, 40, tzinfo=UTC), dt.datetime(2026, 8, 22, 12, 0, tzinfo=UTC))
RESENT_DAY = dt.date(2026, 3, 17)                                  # every tenant's rows for this day written twice

QUARTERS = ["2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2", "2026Q3", "2026Q4"]
NEXT_Q = "2027Q1"


def q_of(t):
    return "%dQ%d" % (t.year, (t.month - 1) // 3 + 1)


def q_start(q):
    y, n = int(q[:4]), int(q[-1])
    return dt.datetime(y, 3 * (n - 1) + 1, 1, tzinfo=UTC)


def q_end(q):
    y, n = int(q[:4]), int(q[-1])
    return dt.datetime(y + (n == 4), 1 if n == 4 else 3 * n + 1, 1, tzinfo=UTC)


def hours(a, b):
    """Hour starts from a (inclusive) to b (exclusive)."""
    t = a
    out = []
    while t < b:
        out.append(t)
        t += dt.timedelta(hours=1)
    return out


# ---------------------------------------------------------------------------------------------------- the cell
CORES = 96
OVERCOMMIT = 1.45
STORE_PER_MACHINE = 2.94       # cell-store's daemon CPU per machine in service (cores), the world's truth
STORE_PER_BATCH = 0.208        # cell-store's CPU per batch core running (dataset reads, checkpoint writes)
STORE_BASE = 37.0              # cell-store's metadata servers, whatever the load (cores)
STORE_NOISE = 13.0             # hourly jitter of a service summed over thousands of daemons (cores)
# what the two drivers do not carry: the small tenants' own reads and writes (Madrid's evening and midday), slow drift,
# the weekly rolling restart of the storage daemons (Tuesday 03:00 to 05:00 UTC, load falls while daemons rejoin) and
# hours in which part of the daemons' samples reach the collector late (the hour's sum reads low)
STORE_TENANTS = 25.0           # amplitude of the small tenants' daily cycle (cores)
STORE_DRIFT = (18.0, 0.75)     # hour-to-hour drift: marginal s.d. (cores), lag-one correlation
STORE_RESTART = (300.0, 550.0) # load missing in a restart hour (cores)
STORE_LATE = (0.04, 60.0, 260.0)   # share of hours with late samples, cores missing
STORE_LEVEL = 6.0              # the unmodelled load's mean over the export (cores)
STORE_TEXTURE_DRAW = 13
CTL_BASE = 1898.0              # cell-ctl at the start of 2025, before its daily swing (cores)
Q1_MACHINES = 5220
NEW_RACKS = 29                 # the December 2026 refresh: 29 racks of 20, in service from 28 December
RACK = 20
ROWS = ["2A", "2B", "2C", "2D", "2E", "2F", "2G", "2H", "2J", "2K", "2L", "2M"]

FIRM = ["search-api", "avail-cache", "pricing", "booking", "payments", "reviews", "reco-serve", "ads-listings",
        "notify", "partner-gw", "settle-batch"]
PLATFORM = ["cell-store", "cell-ctl"]
BATCH = "batch-train"
TENANTS = FIRM + PLATFORM + [BATCH]
TEAMS = ["ranking-ml", "pricing-ml", "fraud-ml", "reco-ml", "demand-ml", "nlp-ml"]

# the firm tenants: relative size at the end of 2026, quarterly growth, Q1 2027 request over the Q4 2026 reservation,
# cost centre and owning team (the Q4 levels, requests and budgets are set in world.py from the cell's history)
FIRM_INFO = {
    "search-api":   dict(w=118400, g=0.021, ratio=1.0523, cc="CC-4110 Search & Discovery",
                         owner="Search Platform", name="Search API"),
    "avail-cache":  dict(w=96300, g=0.018, ratio=1.0509, cc="CC-4120 Inventory & Availability",
                         owner="Inventory Engineering", name="Availability cache"),
    "pricing":      dict(w=71800, g=0.026, ratio=1.0711, cc="CC-4130 Pricing",
                         owner="Pricing Engineering", name="Pricing engine"),
    "booking":      dict(w=52600, g=0.012, ratio=1.0285, cc="CC-4210 Booking & Orders",
                         owner="Booking Engineering", name="Booking and orders"),
    "payments":     dict(w=31200, g=0.011, ratio=1.0222, cc="CC-4220 Payments",
                         owner="Payments Engineering", name="Payments"),
    "reviews":      dict(w=22700, g=0.009, ratio=1.0308, cc="CC-4310 Content & Reviews",
                         owner="Content Engineering", name="Reviews"),
    "reco-serve":   dict(w=48900, g=0.024, ratio=1.0798, cc="CC-4140 Recommendations",
                         owner="Recommendations", name="Recommendations serving"),
    "ads-listings": dict(w=36100, g=0.013, ratio=1.0332, cc="CC-4410 Sponsored Listings",
                         owner="Ads Engineering", name="Sponsored listings"),
    "notify":       dict(w=17900, g=0.010, ratio=1.0251, cc="CC-4230 Messaging",
                         owner="Messaging", name="Notifications"),
    "partner-gw":   dict(w=29400, g=0.016, ratio=1.0425, cc="CC-4510 Partner Connectivity",
                         owner="Partner Connectivity", name="Partner gateway"),
    "settle-batch": dict(w=21000, g=0.014, ratio=1.0286, cc="CC-4520 Partner Finance Systems",
                         owner="Finance Systems", name="Partner settlement runs"),
}
CAPPED = ["search-api", "pricing", "reco-serve"]     # the tenants whose Q1 requests outrun their frozen budgets

# rate card (EUR per reserved core per month), by effective date
RATES = [(dt.date(2025, 1, 1), 7.95), (dt.date(2025, 7, 1), 7.80), (dt.date(2026, 1, 1), 7.65),
         (dt.date(2026, 9, 1), 7.70), (dt.date(2027, 1, 1), 7.42)]


def rate_on(d):
    r = None
    for e, v in RATES:
        if e <= d:
            r = v
    return r


# ---------------------------------------------------------------------------------------------------- names
COMPANY = "Alisio Viajes, S.L."
COMPANY_SHORT = "Alisio"
DC = "MAD1"
DC_PLACE = "Alcobendas (Madrid)"
CELL = "C-22"
STANDARD = "CS-3"

PEOPLE = {
    "requester": "Alejandro Baena",      # head of compute operations, MAD1 (not in the prompt)
    "head": "Raúl Echevarría",           # head of infrastructure (signs CS-3 and the capacity memo)
    "storage": "María Ayala",            # storage platform lead
    "batch": "Jordana Sala",             # batch training platform lead
    "dcops": "Ruy Franco",               # MAD1 data-centre operations manager
    "fleet": "Esteban Madrigal",         # fleet and hardware
    "finance": "Georgina Quirós",        # technology controlling
    "sre": "Martina Pera",               # SRE (operations log entries)
}

# ---------------------------------------------------------------------------------------------------- the pack
STANDARD_PDF = "CS-3_cell_capacity_standard_rev2026-06.pdf"
MEMO = "capacity_memo_2027Q1.docx"
HWPLAN = "c22_hardware_plan_2027Q1_rev2026-12-11.xlsx"
REQUESTS = "capacity_requests_2027Q1.csv"
BUDGETS = "tech_budgets_2026_Q1-2027_freeze.xlsx"
RATECARD = "compute_rate_card.csv"
LEDGER = "c22_reservation_ledger_2025Q1-2026Q4.csv"
USAGE = "c22_usage_hourly_2025-01-01_2026-12-13.csv"
CELLHOURLY = "c22_cell_hourly_2025-01-01_2026-12-13.csv"
DIRECTORY = "tenant_directory.json"
CAPREPORT = "c22_capacity_report_2026Q3.pdf"
OPSLOG = "mad1_operations_log_2026H2.docx"
RUNS = "batch_runs_2026Q3.csv"
CHECKPOINTS = "batch_checkpoints_2026Q3.csv"
RESIZES = "batch_resizes_2026Q3.csv"
MEVENTS = "c22_machine_events_2026Q3.csv"
INVENTORY = "mad1_hardware_inventory_2026-12.xlsx"
QCHANGES = "quota_changes_2026Q3.csv"
QRUNS = "quota_reconciler_runs_2026Q3.csv"
CHARGEBACK = "chargeback_policy_2026.pdf"
DICTIONARY = "data_dictionary.xlsx"
README = "README_capacity_review_files.txt"
SISTERS = "mad1_cells_quarterly_summary_2025-2026.xlsx"
BATCH_DEMAND = "batch_training_demand_2027H1.pdf"
DISTRACTORS = [SISTERS, BATCH_DEMAND]

GOLD_BOOK = "c22_capacity_2027q1.xlsx"
GOLD_DECK = "c22_capacity_review_2027q1.pptx"


def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def write_csv(path, cols, rows, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(["" if r.get(c) is None else r.get(c) for c in cols] if isinstance(r, dict) else r)
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return n


def floor_to(x, step):
    return int(math.floor(x / step + 1e-12) * step)


def round_to(x, step):
    """Round half away from zero to a multiple of step (the deliverables' convention)."""
    q = x / step
    return int(math.floor(q + 0.5)) * step if q >= 0 else -int(math.floor(-q + 0.5)) * step


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def madrid(t):
    """UTC to Madrid wall time (CET, CEST from the last Sunday of March 01:00 UTC to the last Sunday of October)."""
    y = t.year

    def last_sunday(month):
        d = dt.datetime(y, month, 31, 1, 0, tzinfo=UTC)
        while d.weekday() != 6:
            d -= dt.timedelta(days=1)
        return d
    off = 2 if last_sunday(3) <= t < last_sunday(10) else 1
    return (t + dt.timedelta(hours=off)).replace(tzinfo=None), off
