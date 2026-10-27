"""task144 constants and helpers shared by every generator module.

Grachtwerk B.V. (fictional) runs a code-hosting platform from Amsterdam. Its monthly developer newsletter, Sluis,
spotlights one new repository an issue; from January 2025 to September 2026 the spotlight was drawn by lot among the
editors' shortlist of seven, and from the October 2026 issue it goes to the shortlisted repository with the most
expected external stars in its first 90 days public if spotlighted. The pick is locked on Wednesday 30 September
2026 from the events warehouse extract to Sunday 27 September 2026; the issue goes out on Tuesday 6 October 2026."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import json
import math

import numpy as np

SEED = 1440930

UTC = dt.timezone.utc

# ---------------------------------------------------------------------------------------------------- calendar
CUT = dt.datetime(2026, 9, 27, 23, 59, 59)          # the warehouse extract's last second (UTC, naive)
CUT_DATE = dt.date(2026, 9, 27)
PICK_DATE = dt.date(2026, 9, 30)                    # the editorial meeting that locks the pick
SCHEMA_V6 = dt.datetime(2026, 3, 2, 0, 0, 0)        # the star stream's schema v6 from this instant (UTC)
ESP_SWITCH = dt.date(2026, 6, 2)                    # Sluis sends through Relaymark from this day (Postwerk before)
MEMO_DATE = dt.date(2026, 9, 15)
NOMINATIONS = (dt.date(2026, 9, 1), dt.date(2026, 9, 20))   # the October nominations window (Amsterdam days)
PACK_STAMP = dt.datetime(2026, 9, 28, 6, 42, tzinfo=UTC)    # Monday 28 September 2026 08:42 Amsterdam


def first_tuesday(y, m):
    d = dt.date(y, m, 1)
    while d.weekday() != 1:
        d += dt.timedelta(days=1)
    return d


def amsterdam_offset(t_utc):
    """Hours Amsterdam is ahead of UTC at a naive UTC instant: CEST +2 from the last Sunday of March 01:00 UTC to the
    last Sunday of October 01:00 UTC, CET +1 otherwise."""
    y = t_utc.year

    def last_sunday(month):
        d = dt.date(y, month, 31)
        while d.weekday() != 6:
            d -= dt.timedelta(days=1)
        return dt.datetime.combine(d, dt.time(1, 0))
    return 2 if last_sunday(3) <= t_utc < last_sunday(10) else 1


def to_amsterdam(t_utc):
    return t_utc + dt.timedelta(hours=amsterdam_offset(t_utc))


def from_amsterdam(t_local):
    for off in (1, 2):
        u = t_local - dt.timedelta(hours=off)
        if to_amsterdam(u) == t_local:
            return u
    raise ValueError(t_local)


# Sluis issues: the first Tuesday of each month, sent at 09:00 Amsterdam time.
LOTTERY_MONTHS = [(2025, m) for m in range(1, 13)] + [(2026, m) for m in range(1, 10)]
OCT = (2026, 10)


def issue_send_utc(y, m):
    return from_amsterdam(dt.datetime.combine(first_tuesday(y, m), dt.time(9, 0)))


ISSUE_SEND = {ym: issue_send_utc(*ym) for ym in LOTTERY_MONTHS + [OCT]}
OCT_SEND = ISSUE_SEND[OCT]                           # 2026-10-06 07:00 UTC

MONTH_NAME = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October", 11: "November", 12: "December"}
MON3 = {k: v[:3] for k, v in MONTH_NAME.items()}
WINDOW_DAYS = 90                                     # the first 90 days public: the public UTC day is day 1

# ---------------------------------------------------------------------------------------------------- the platform
ORG = "Grachtwerk B.V."
PLATFORM = "Grachtwerk"
HOST = "grachtwerk.dev"
NEWSLETTER = "Sluis"
OLD_ESP = "Postwerk"
NEW_ESP = "Relaymark"
CREDIT = "Grachtwerk Pipelines"

PEOPLE = {
    "editor": "Sylvie Kramer",        # editor of Sluis: the requester, author of the featuring memo
    "devrel": "Twan Evers",           # head of developer relations, owns the Pipelines sponsorship
    "data": "Vigo Hulshouts",         # data engineer, the events warehouse extract
    "growth": "Laura Rijntjes",       # growth analyst who ran the spotlight lottery
}

# The October 2026 shortlist: key -> (name, owner, owner_type, public UTC time, language, description)
OCT_SHORTLIST = [
    ("tracewire", "meridian-observe", "organization", dt.datetime(2026, 8, 26, 9, 14, 7), "Go",
     "Distributed tracing from the command line: follow a request across services without a collector"),
    ("slidewell", "pjvdlinden", "user", dt.datetime(2026, 8, 24, 19, 41, 52), "TypeScript",
     "Write slides in Markdown, present them in the browser or the terminal"),
    ("shiftgres", "lindengracht-dev", "organization", dt.datetime(2026, 9, 3, 7, 2, 33), "Rust",
     "Online schema migrations for Postgres with no table locks"),
    ("kilnkit", "kilnworks", "organization", dt.datetime(2026, 8, 29, 13, 25, 40), "TypeScript",
     "Accessible UI components for server-rendered web apps"),
    ("hullcheck", "dokwerf-labs", "organization", dt.datetime(2026, 9, 5, 10, 51, 18), "Go",
     "Lint container images against your own rules before they ship"),
    ("timeloom", "inestavares", "user", dt.datetime(2026, 9, 1, 21, 6, 45), "Python",
     "A terminal time tracker that reads your git history"),
    ("ferrolog", "ferro-collective", "organization", dt.datetime(2026, 9, 7, 8, 37, 29), "Rust",
     "Structured logging for Rust services, fast enough for hot paths"),
]
OCT_NAMES = [r[0] for r in OCT_SHORTLIST]
RENAMED = {"kilnkit": ("kiln-ui", dt.datetime(2026, 9, 9, 11, 3, 51)),
           "hullcheck": ("imagelint", dt.datetime(2026, 9, 11, 15, 47, 12))}

# ---------------------------------------------------------------------------------------------------- the pack
EV25 = "grachtwerk_star_events_2024-12-08_to_2026-03-01.csv"
EV26 = "grachtwerk_star_events_2026-03-02_to_2026-09-27.csv"
ROLLUP = "repo_daily_external_stars_2024-11-24_to_2026-09-27.csv"
ACCOUNTS = "accounts_snapshot_2026-09-27.parquet"
MEMBERS = "organization_memberships_2026-09-27.csv"
REPOS = "repositories_2026-09-27.json"
CROSSWALK = "star_surface_code_crosswalk_2026-03-02.csv"
LOTTERY = "sluis_spotlight_lottery_2025-2026.xlsx"
MEMO = "sluis_featuring_memo_2026-09.pdf"
PW_CAMP = "postwerk_campaigns_2026-04_to_2026-05.csv"
PW_LINKS = "postwerk_link_report_2026-04_to_2026-05.csv"
RM_CAMP = "relaymark_campaigns_2026-06_to_2026-09.json"
RM_LINKS = "relaymark_link_clicks_2026-06_to_2026-09.csv"
NOMS = "sluis_nominations_2026-10.csv"
RENAMES = "repository_renames_2026.csv"
TRAFFIC = "repository_traffic_2026-08-24_to_2026-09-27.csv"
TRENDING = "trending_daily_2026-08-24_to_2026-09-27.csv"
DISTRACTORS = [TRAFFIC, TRENDING]
CALL_FILES = [EV25, EV26, ROLLUP, ACCOUNTS, MEMBERS, REPOS, CROSSWALK, LOTTERY, MEMO]
ASK_FILES = [PW_CAMP, PW_LINKS, RM_CAMP, RM_LINKS, NOMS, RENAMES]

GOLD_BOOK = "sluis_spotlight_2026-10.xlsx"
GOLD_CHART = "shortlist_forecast_2026-10.png"

SURFACES_V6 = ["feed", "newsletter", "repo_page", "search", "explore", "api"]
V5_OF = {"feed": "dash", "newsletter": "nl", "repo_page": "repo", "search": "srch", "explore": "expl", "api": "api"}


def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def hexid(*keys, n=16):
    return hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=n // 2).hexdigest()


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


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def round_to(x, step):
    """Round half away from zero to a multiple of step (the deliverables' convention)."""
    q = x / step
    return int(math.floor(q + 0.5)) * step if q >= 0 else -int(math.floor(-q + 0.5)) * step


def round_half_up(x, nd=0):
    f = 10 ** nd
    return math.floor(x * f + 0.5 + 1e-9) / f


def iso_z(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def utc_of(stamp):
    """A naive UTC datetime from an ISO 8601 stamp written with Z or with an offset (+02:00)."""
    t = dt.datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    return t.astimezone(UTC).replace(tzinfo=None)


def day_index(public_utc, t_utc):
    """Day number in the repository's life: 1 on the UTC day it went public."""
    return (t_utc.date() - public_utc.date()).days + 1
