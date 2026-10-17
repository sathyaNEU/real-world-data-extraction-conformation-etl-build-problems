"""task158 constants and helpers shared by every generator module.

Slenk B.V. is an Amsterdam company that trains its own language models and serves them through six products, each
from its own GPU pool in two colocation halls in North Holland. A leased 240-GPU cluster (30 nodes of eight H100s)
is handed over on Monday 4 January 2027 and goes, for the first quarter, whole to one pool. The capacity desk pulled
every file on Monday 7 December 2026; the fleet rollup closes with the hour starting 23:00 UTC on Sunday 6 December.

The seed was fixed by rule before any data was generated: the task number, then the as-of month and day."""
from __future__ import annotations

import csv
import datetime as dt
import io
import json

import numpy as np

SEED = 1581207

ORG = "Slenk"
ORG_LEGAL = "Slenk B.V."
PEOPLE = {
    "capacity_lead": "Janne Muijs",      # fleet capacity lead: the stopgap policy, the fleet plan, the fleet notes
    "analyst": "Casper Heijmans",        # capacity analyst: the Q3 close-out, the pull
    "reports_pm": "Louise Hekker",       # report service product manager: the commitments ledger
    "infra": "Mart Bosch",               # infrastructure: the lease, the acceptance review
}

UTC = dt.timezone.utc

# ------------------------------------------------------------------------------------------------- calendar
ROLLUP_START = dt.datetime(2026, 1, 1, 0, 0)            # UTC, first hour
ROLLUP_END = dt.datetime(2026, 12, 6, 23, 0)            # UTC, last hour start
AS_OF = dt.date(2026, 12, 7)                            # Monday, the pull
PULL_AT = dt.datetime(2026, 12, 7, 7, 40)               # Amsterdam local
LC2_START = dt.datetime(2026, 5, 11, 6, 0)              # UTC, the rolling upgrade begins (tag changes)
LC2_END = dt.datetime(2026, 5, 12, 18, 0)               # UTC, every replica on lc2
PILOT_START = dt.date(2026, 10, 5)                      # Monday, the early-access tenant's first reports
PILOT_PAUSE = (dt.date(2026, 11, 19), dt.date(2026, 11, 20))  # the tenant's own system freeze, no reports
EA_END = dt.date(2026, 12, 18)
AGENTS_TO_CHAT = dt.datetime(2026, 11, 16, 9, 0)        # UTC, four Agents nodes join Chat
MAINT_WINDOW = (dt.datetime(2026, 10, 26, 0, 0), dt.datetime(2026, 12, 7, 0, 0))  # logs pulled, UTC
NOV = (dt.datetime(2026, 11, 1, 0, 0), dt.datetime(2026, 12, 1, 0, 0))            # UTC
CLOSEOUT_DATE = dt.date(2026, 10, 16)
LEASE_DATE = dt.date(2026, 11, 13)
POLICY_DATE = dt.date(2026, 11, 16)
INTAKE_DUE = dt.date(2026, 11, 27)
PLAN_DATE = dt.date(2026, 12, 1)
LEDGER_DATE = dt.date(2026, 12, 4)
HARNESS_CHANGE = dt.datetime(2026, 12, 1, 0, 0)         # UTC, the provider's fabric harness release
HARNESS_OLD, HARNESS_NEW = "nm-fabcheck 3.8.4", "nm-fabcheck 4.0.1"
REVIEW_LOCAL = dt.datetime(2026, 12, 4, 14, 0)            # the acceptance review, Amsterdam time (Schedule 3.3)
# the early-access tenant ran at the size of the contract it converted to: its busiest hour in a full week at
# RC-2026-031's contracted 400 reports an hour, against the hour shape's 1.18 peak
PILOT_BASE = round(400 / 1.18)
REVIEW_DATE = dt.date(2026, 12, 4)
HANDOVER = dt.date(2027, 1, 4)
Q1_WEEKS = [dt.date(2027, 1, 4) + dt.timedelta(weeks=i) for i in range(13)]   # Mondays of 2027-W01 .. W13
FEB_MOVE_WEEK = 7                                        # Monday 15 February 2027

NL_HOLIDAYS = {dt.date(2026, 1, 1), dt.date(2026, 4, 3), dt.date(2026, 4, 6), dt.date(2026, 4, 27),
               dt.date(2026, 5, 14), dt.date(2026, 5, 25), dt.date(2026, 12, 25), dt.date(2026, 12, 26)}

# ------------------------------------------------------------------------------------------------- the fleet
POOLS = ["chat-prod", "code-prod", "agents-prod", "docs-prod", "batch-prod", "voice-prod"]
PRODUCT = {"chat-prod": "Chat", "code-prod": "Code", "agents-prod": "Agents", "docs-prod": "Docs",
           "batch-prod": "Batch API", "voice-prod": "Voice"}
MODEL_TAG = {"chat-prod": "l3-2025.10", "code-prod": "c2-2025.12", "agents-prod": "l3-2025.10",
             "voice-prod": "s2rt-2025.09"}
LC1_TAG, LC2_TAG = "lc1-2025.11", "lc2-2026.05"

# the long-context models' cost of serving, GPU-seconds per prompt token computed and per completion token
A_LC2, B_LC2 = 0.000248, 0.00185
A_LC1, B_LC1 = 0.000360, 0.00280
# the other models (cost per computed prompt token, per completion token)
COST = {"l3": (0.000150, 0.000920), "c2": (0.000300, 0.00250), "s2rt": (0.000060, 0.00085)}

# GPUs allocated to each pool through 2026 (start date inclusive), eight per node
ALLOC_2026 = {
    "chat-prod": [(dt.datetime(2026, 1, 1), 1456), (AGENTS_TO_CHAT, 1488)],
    "code-prod": [(dt.datetime(2026, 1, 1), 640), (dt.datetime(2026, 9, 7, 9, 0), 664)],
    "agents-prod": [(dt.datetime(2026, 1, 1), 512), (AGENTS_TO_CHAT, 480)],
    "docs-prod": [(dt.datetime(2026, 1, 1), 576), (dt.datetime(2026, 7, 6, 9, 0), 608)],
    "batch-prod": [(dt.datetime(2026, 1, 1), 328)],
    "voice-prod": [(dt.datetime(2026, 1, 1), 272)],
}
# the Q1 2027 fleet plan, GPUs by ISO week W01..W13
PLAN_Q1 = {
    "chat-prod": [1488] * 13, "code-prod": [664] * 13, "agents-prod": [480] * 13,
    "docs-prod": [608] * 6 + [656] * 7, "batch-prod": [328] * 6 + [280] * 7, "voice-prod": [272] * 13,
}
BUSY_TARGET = 0.70
CARRY = 3600 * BUSY_TARGET          # busy GPU-seconds one GPU carries in an hour at the target

# ------------------------------------------------------------------------------------------------- report service
TIERS = {   # calls per report, prompt token limit per call, completion token limit per call, list price per report
    "RS-6": (6, 24000, 1600, 0.44),
    "RM-8": (8, 40000, 900, 0.95),
    "RL-12": (12, 64000, 800, 2.60),
}


# ------------------------------------------------------------------------------------------------- time helpers
def last_sunday(y, m):
    d = dt.date(y, m + 1, 1) - dt.timedelta(days=1) if m < 12 else dt.date(y, 12, 31)
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)


def ams_offset_utc(t):
    """Hours Amsterdam sits ahead of UTC at UTC time t (EU rules: CEST from 01:00 UTC on the last Sunday of March
    to 01:00 UTC on the last Sunday of October)."""
    y = t.year
    start = dt.datetime.combine(last_sunday(y, 3), dt.time(1, 0))
    end = dt.datetime.combine(last_sunday(y, 10), dt.time(1, 0))
    return 2 if start <= t < end else 1


def utc_to_ams(t):
    return t + dt.timedelta(hours=ams_offset_utc(t))


def ams_to_utc(t):
    """Local (naive) Amsterdam time to UTC; times in the autumn's repeated hour are read as the first pass."""
    for off in (2, 1):
        u = t - dt.timedelta(hours=off)
        if ams_offset_utc(u) == off:
            return u
    return t - dt.timedelta(hours=1)


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def hours():
    out, t = [], ROLLUP_START
    while t <= ROLLUP_END:
        out.append(t)
        t += dt.timedelta(hours=1)
    return out


def alloc_at(pool, t):
    a = None
    for start, g in ALLOC_2026[pool]:
        if t >= start:
            a = g
    return a


def round_half_up(x, nd=0):
    q = 10 ** nd
    return np.floor(x * q + 0.5) / q


def nearest(x, step):
    return int(np.floor(x / step + 0.5) * step)


# ------------------------------------------------------------------------------------------------- writers
def write_csv(path, cols, rows, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(r)
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return n


def write_jsonl(path, objs):
    n = 0
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for o in objs:
            f.write(json.dumps(o, separators=(",", ":"), ensure_ascii=False) + "\n")
            n += 1
    return n


def fmt_int(n):
    return "{:,}".format(int(n))
