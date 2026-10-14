"""task258 constants and helpers shared by every generator module.

Brolga Media (fictional), Sydney: six web properties, the web platform team's one performance squad, the squad's
hero-image playbook and its eleven past engagements, November 2026 RUM, and the two ask paths (image egress, the DAM)."""
from __future__ import annotations

import datetime as dt
import hashlib

import numpy as np

SEED = 2580113

# Calendar of the fiction (Sydney is on daylight time, UTC+11, from 4 October 2026 to 4 April 2027)
UTC_OFFSET = 11
MONTH_START_UTC = dt.datetime(2026, 10, 31, 13, 0)      # 1 November 2026, 00:00 Sydney
MONTH_END_UTC = dt.datetime(2026, 11, 30, 13, 0)        # 1 December 2026, 00:00 Sydney
EXTRACT_START_UTC = dt.datetime(2026, 10, 31, 0, 0)     # the RUM and log extracts run by whole UTC days
EXTRACT_END_UTC = dt.datetime(2026, 12, 1, 0, 0)
EXTRACT_DATE = dt.date(2026, 12, 3)                     # the RUM and log extracts for the December planning
PLANNING_DATE = dt.date(2026, 12, 8)                    # the head of web platform assigns the squad
QUARTER_START = dt.date(2027, 1, 5)
GOOD_MS = 2500

GROUP = "Brolga Media"
PEOPLE = {"head": "Margaret Good", "lead": "Tasha Murillo", "sre": "Doris Rhodes"}
CDN_VENDOR = "Tallowood Edge Pty Ltd"

CDN_HOST = "img.brolgacdn.au"
AGENCY_HOSTS = ("images.pressframe-syndication.net", "cdn.wirelens.media")
AD_HOSTS = ("creative.adwattle.net",)
VIDEO_HOST = "poster.clipferry.net"

# code, name, origin, own image host, legacy alias (host, retired on, share of own images still on it),
# share of own images already on the group image CDN, page loads a month (millions, navigations reporting LCP),
# share of loads whose LCP element is the property's own image,
# own-image paint parts (median ms, log sd): time to first byte, load delay, load time, render delay,
# other loads' paint (median ms, log sd), device mix (mobile, desktop, tablet), hero slot (w, h)
PROPERTIES = [
    dict(code="tideline", name="Tideline", kind="news", origin="tideline.brolga.au",
         img="images.tideline.brolga.au", alias=None, cdn_share=0.04, loads=61.69, own=0.20,
         parts=((700, .50), (500, .70), (700, .60), (450, .60)), other=(2350, .45),
         devices=(0.71, 0.25, 0.04), hero=(1200, 675)),
    dict(code="matchday", name="Matchday", kind="sport", origin="matchday.brolga.au",
         img="images.matchday.brolga.au", alias=None, cdn_share=0.06, loads=36.5, own=0.31,
         parts=((1000, .45), (1300, .70), (650, .60), (600, .60)), other=(1800, .45),
         devices=(0.78, 0.18, 0.04), hero=(1200, 675)),
    dict(code="hearth", name="Hearth", kind="home", origin="hearth.brolga.au",
         img="images.hearth.brolga.au", alias=("media.hearth.brolga.au", dt.date(2026, 8, 14), 0.14), cdn_share=0.0,
         loads=26.27, own=0.85, parts=((1700, .35), (400, .60), (900, .55), (550, .50)), other=(2900, .40),
         devices=(0.66, 0.29, 0.05), hero=(1600, 900)),
    dict(code="ledger", name="Ledger", kind="personal finance", origin="ledger.brolga.au",
         img="images.ledger.brolga.au", alias=None, cdn_share=0.0, loads=39.2, own=0.65,
         parts=((1150, .22), (150, .30), (420, .40), (900, .25)), other=(2400, .30),
         devices=(0.58, 0.38, 0.04), hero=(1200, 675)),
    dict(code="trailhead", name="Trailhead", kind="travel", origin="trailhead.brolga.au",
         img="images.trailhead.brolga.au", alias=("media.trailhead.brolga.au", dt.date(2026, 8, 14), 0.09),
         cdn_share=0.0, loads=8.0, own=0.72, parts=((1300, .40), (700, .60), (1300, .50), (350, .50)),
         other=(2700, .45), devices=(0.69, 0.27, 0.04), hero=(1600, 900)),
    dict(code="pantry", name="Pantry", kind="food", origin="pantry.brolga.au",
         img="images.pantry.brolga.au", alias=None, cdn_share=0.25, loads=10.2, own=0.70,
         parts=((400, .45), (3200, .50), (900, .50), (220, .50)), other=(2200, .40),
         devices=(0.81, 0.15, 0.04), hero=(1080, 1080)),
]
CODES = [p["code"] for p in PROPERTIES]
BY_CODE = {p["code"]: p for p in PROPERTIES}

# RUM sampling: share of page loads that send a beacon, effective-dated (UTC instant from which a rate applies)
SAMPLING = {
    "tideline": [(dt.datetime(2026, 6, 1, 0, 0), 0.0005), (dt.datetime(2026, 11, 9, 2, 0), 0.0006)],
    "matchday": [(dt.datetime(2026, 6, 1, 0, 0), 0.0008)],
    "hearth": [(dt.datetime(2026, 6, 1, 0, 0), 0.0010)],
    "ledger": [(dt.datetime(2026, 6, 1, 0, 0), 0.0010), (dt.datetime(2026, 11, 16, 3, 0), 0.0006)],
    "trailhead": [(dt.datetime(2026, 6, 1, 0, 0), 0.0012)],
    "pantry": [(dt.datetime(2026, 6, 1, 0, 0), 0.0010)],
}

# The playbook as the squad has run it, and the world's own response to it (never shipped as figures)
LEVEL_MS = 240          # the hero image's load delay once it is preloaded from the group image CDN (the connection)
LEVEL_SD_MS = 15      # the connection's spread from load to load
LOAD_TIME_RATIO = 0.48  # AVIF at the slot size against the source JPEG or PNG, across the engagements
# The group experimentation tool's anti-flicker snippet keeps a page hidden until the tool's script arrives or the
# snippet's timeout runs out. On these sections (and on two engaged sites) the script waits behind the consent
# manager and never arrives in time, so the page first paints at the timeout after its first byte; the image playbook
# leaves it where it is (never shipped as a figure)
GATED_SECTIONS = {"tideline": ("news", "politics"), "matchday": ("tennis",), "hearth": ("interiors",),
                  "trailhead": ("deals",), "pantry": ("recipes", "dinner", "quick-meals", "healthy")}
GATED_ENGAGEMENTS = ("E06", "E10")
GATE_TIMEOUT_MS = 3000

# Past engagements on the group's smaller sites: site, origin, (start of the before window, change shipped),
# before-window medians for the hero image's load delay and load time (ms), time to first byte and render delay,
# and how each landed (never shipped as figures): the after-delay's offset from the CDN connection level (ms) and the
# load time's ratio at the slot size
ENGAGEMENTS = [
    ("E01", "Clutch", "clutch.brolga.au", dt.date(2024, 3, 4), 2600, 1100, 900, 400, 3, 0.473),
    ("E02", "Tenancy", "tenancy.brolga.au", dt.date(2024, 6, 3), 420, 800, 1100, 600, -6, 0.497),
    ("E03", "Fairway", "fairway.brolga.au", dt.date(2024, 9, 2), 130, 700, 1200, 500, 7, 0.458),
    ("E04", "Undercurrent", "undercurrent.brolga.au", dt.date(2024, 11, 25), 1500, 900, 800, 450, -3, 0.486),
    ("E05", "Clutch", "clutch.brolga.au", dt.date(2025, 2, 24), 350, 600, 700, 300, 2, 0.479),
    ("E06", "Brolga Kids", "kids.brolga.au", dt.date(2025, 5, 19), 3000, 1300, 600, 350, -8, 0.468),
    ("E07", "Tidewater", "tidewater.brolga.au", dt.date(2025, 8, 11), 180, 650, 950, 700, 5, 0.451),
    ("E08", "Tenancy", "tenancy.brolga.au", dt.date(2025, 11, 3), 900, 1000, 1000, 550, -2, 0.492),
    ("E09", "Paddock", "paddock.brolga.au", dt.date(2026, 2, 23), 260, 500, 1300, 650, 6, 0.509),
    ("E10", "Fairway", "fairway.brolga.au", dt.date(2026, 5, 18), 2200, 1400, 750, 400, -4, 0.488),
    ("E11", "Undercurrent", "undercurrent.brolga.au", dt.date(2026, 8, 10), 600, 750, 850, 500, 0, 0.480),
]
ENGAGEMENT_BEACONS = 3000     # beacons a window, before and after
WINDOW_DAYS = 28

# Ask A: image requests a page load makes by slot, the share answered 304 (no body), each slot's size, and the AVIF
# bytes the squad's encoder produces at each slot (median over a sample of the property's images)
SLOT_SIZES = {
    "tideline": {"hero": (1200, 675), "inline": (640, 360), "thumbnail": (320, 180)},
    "matchday": {"hero": (1200, 675), "inline": (640, 360), "thumbnail": (320, 180)},
    "hearth": {"hero": (1600, 900), "inline": (800, 450), "thumbnail": (400, 225)},
    "ledger": {"hero": (1200, 675), "inline": (640, 360), "thumbnail": (320, 180)},
    "trailhead": {"hero": (1600, 900), "inline": (800, 450), "thumbnail": (400, 225)},
    "pantry": {"hero": (1080, 1080), "inline": (720, 720), "thumbnail": (360, 360)},
}
REQUESTS_PER_LOAD = {
    "tideline": {"hero": 0.72, "inline": 1.7, "thumbnail": 6.2},
    "matchday": {"hero": 0.66, "inline": 1.2, "thumbnail": 7.8},
    "hearth": {"hero": 0.93, "inline": 3.4, "thumbnail": 4.9},
    "ledger": {"hero": 0.78, "inline": 0.9, "thumbnail": 3.8},
    "trailhead": {"hero": 0.86, "inline": 2.6, "thumbnail": 5.7},
    "pantry": {"hero": 0.88, "inline": 4.2, "thumbnail": 6.6},
}
REVALIDATED = {"tideline": 0.24, "matchday": 0.19, "hearth": 0.11, "ledger": 0.27, "trailhead": 0.14, "pantry": 0.13}
AVIF_BYTES = {
    "tideline": {"hero": 58_380, "inline": 21_300, "thumbnail": 7_900},
    "matchday": {"hero": 61_900, "inline": 22_800, "thumbnail": 8_300},
    "hearth": {"hero": 96_690, "inline": 33_100, "thumbnail": 11_200},
    "ledger": {"hero": 47_300, "inline": 17_600, "thumbnail": 6_400},
    "trailhead": {"hero": 112_600, "inline": 38_400, "thumbnail": 12_900},
    "pantry": {"hero": 83_600, "inline": 41_700, "thumbnail": 13_800},
}
CDN_RATE_AUD_PER_GB = 0.071
# Ask B: the DAM. The image library moved into the group DAM on this date; each migrated asset kept its library
# record (old id) beside its DAM record, which carries the old id as legacy_id. The nightly crawl before the export.
DAM_CUTOVER = dt.date(2025, 3, 24)
LATEST_CRAWL = dt.date(2026, 12, 2)
RENDITIONS = ("original", "large", "web")

# The pack's files, in the group's own naming
CHARTER = "performance_squad_charter_2026.pdf"
BEACONS = "rum_lcp_beacons_2026-11.csv"
SAMPLING_CFG = "rum_sampling_config.csv"
ENG_LOG = "squad_change_log_2024-2026.xlsx"
ENG_BEACONS = "squad_engagement_beacons_2024-2026.csv"
RUNBOOK = "domains_runbook.md"
CDN_HOSTS = "cdn_host_list.csv"
NOTES = "rum_extract_field_notes.md"
CRUX = "crux_lcp_origins_2026-11.csv"
ANALYTICS = "analytics_pageviews_2026-11.csv"
IMG_LOGS = "image_host_logs_2026-11.csv"
LEGACY_LOGS = "legacy_media_server_log_2026-11.csv"
AVIF_TABLE = "squad_avif_size_table.xlsx"
CONTRACT = "image_cdn_contract_schedule_2026.pdf"
DAM = "dam_image_export_2026-11.csv"
EXTRACT_LOG = "extract_log_2026-12-03.csv"
DISTRACTORS = (CRUX, ANALYTICS)
DELIVERABLES = ("performance_squad_q1_2027.md", "lcp_reach_q1_2027.png")


def stream(*keys) -> np.random.Generator:
    """One RNG stream per named component, seeded by blake2b so no process salt reaches it."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8)
    return np.random.default_rng(int.from_bytes(h.digest(), "big"))


def sydney(t: dt.datetime) -> dt.datetime:
    return t + dt.timedelta(hours=UTC_OFFSET)


def rate_at(code: str, t: dt.datetime) -> float:
    rate = None
    for since, r in SAMPLING[code]:
        if t >= since:
            rate = r
    return rate
