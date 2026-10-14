"""task136 constants and helpers shared by every generator module.

Mirrabee Energy (fictional), a regional electricity distributor in south-east Queensland: the eight 22 kV feeders out
of its Yarrabin zone substation, rooftop PV connected on each, Merindah City Council's Solar Streets bulk-buys, and the
FY2027-28 capital works program's one accelerated hosting-capacity augmentation."""
from __future__ import annotations

import csv
import datetime as dt
import io

import numpy as np

SEED = 1360412

# Calendar of the fiction
BASE = dt.date(2026, 8, 31)              # NPP-114 base date: the last day of the month before the forecast
REGISTER_RUN = dt.date(2026, 9, 1)       # connection register and network model extracts run
DER_RUN = dt.date(2026, 9, 1)            # DER Register extract as at 31 August 2026
LETTER_DATE = dt.date(2026, 8, 14)       # the council's letter on the 2026 campaigns
HCA_DATE = dt.date(2026, 7, 24)          # hosting capacity assessment issued
NPP_DATE = dt.date(2026, 3, 2)           # NPP-114 revision 3 effective
REQUEST = dt.date(2026, 10, 12)
REVIEW = dt.date(2026, 11, 24)           # executive leadership team investment review
DESIGN = dt.date(2029, 8, 31)            # design point (NPP-114 2.4)
YEARS_TO_DESIGN = 3                      # 31 August 2026 to 31 August 2029
PORTAL_SWITCH = dt.date(2024, 7, 1)      # installers' DER Register portal: NMI lodged with its checksum digit
MIGRATION = dt.date(2019, 7, 1)          # applications before this were migrated from the legacy system
TREND_FYS = [(dt.date(2023, 7, 1), dt.date(2024, 6, 30)), (dt.date(2024, 7, 1), dt.date(2025, 6, 30)),
             (dt.date(2025, 7, 1), dt.date(2026, 6, 30))]
LAST_FY = TREND_FYS[-1]
WORLD_START = dt.date(2009, 1, 1)

COMPANY = "Mirrabee Energy"
COUNCIL = "Merindah City Council"
PROGRAM = "Solar Streets"
ZONE = "Yarrabin"
ZS_CODE = "YRB"
FEEDERS = ["YRB21", "YRB22", "YRB23", "YRB24", "YRB25", "YRB26", "YRB27", "YRB28"]

PEOPLE = {
    "analyst": "Wanda Thornton",          # DER forecasting analyst (the requester; never in the pack's prose as such)
    "planning": "Ian Fletcher",           # Manager Network Planning, owner of NPP-114
    "council": "Julie Cochran",           # Sustainability Programs Officer, Merindah City Council
    "connections": "Bryan Nichols",       # Embedded Generation Connections Lead
    "gis": "Linda Ruiz",                  # GIS analyst, NMI-to-property cross-reference
    "customer": "Nicole Rocha",           # team leader, customer experience (battery rebate distractor owner)
    "consultant": "Tammy Buchanan",       # Buchanan Power Engineering, hosting capacity assessment
}

# Localities: name, feeder (at the base date; a transfer's earlier feeder is in TRANSFERS), kind, residential
# addresses (NMIs), owner-occupied houses, rented houses, townhouses, units, business NMIs, built (first year, last
# year), and lam, the owner-occupiers' propensity to take up rooftop PV (per unit of the year's pace) from 2013, with
# lam_boom (default lam) its propensity in the Solar Bonus Scheme years 2009 to 2012.
# Campaign suburbs carry their campaign key.
LOCALITIES = [
    dict(name="Glenmorrow", feeder="YRB21", kind="campaign", camp="GLM18", res=3159, oo=1200, rent=520, town=170,
         biz=38, built=(1972, 1996), lam=0.0240, lam_boom=0.1200),
    dict(name="Paperbark Grove", feeder="YRB21", kind="campaign", camp="PBG24", res=2881, oo=2072, rent=360, town=120,
         biz=22, built=(1988, 2004), lam=0.0320, lam_boom=0.0080),
    dict(name="Merindah Heights", feeder="YRB21", kind="rest", res=1150, oo=650, rent=230, town=60, biz=31,
         built=(1979, 2012), infill=22, lam=0.0246),
    dict(name="Kurrajong Park", feeder="YRB22", kind="campaign", camp="KJP19", res=4106, oo=3012, rent=480, town=160,
         biz=26, built=(1985, 2003), lam=0.0750, lam_boom=0.0200),
    dict(name="Hollow Creek", feeder="YRB22", kind="rest", res=2850, oo=1880, rent=470, town=150, biz=46,
         built=(1983, 2008), infill=30, lam=0.0269),
    dict(name="Silky Oak", feeder="YRB23", kind="campaign", camp="SKO22", res=3087, oo=1854, rent=420, town=230,
         biz=27, built=(1976, 1999), lam=0.0710, lam_boom=0.0060),
    dict(name="Tanners Flat", feeder="YRB23", kind="rest", res=1600, oo=880, rent=330, town=90, biz=58,
         built=(1968, 2006), infill=18, lam=0.0189),
    dict(name="Yarrabin North", feeder="YRB21", postcode="4514", kind="transfer", res=380, oo=250, rent=70, town=20, biz=6,
         built=(1990, 2010), infill=6, lam=0.0216),
    dict(name="Bindarra Waters", feeder="YRB24", kind="campaign26", camp="BDW26", res=6240, oo=5570, rent=390,
         town=210, biz=24, built=(2018, 2023), lam=0.0073),
    dict(name="Myrtle Vale", stream="Bindarra Road", feeder="YRB24", kind="rest", res=420, oo=330, rent=60, town=0, biz=9,
         built=(1975, 2015), infill=10, lam=0.0311),
    dict(name="Tallowwood Rise", feeder="YRB25", kind="campaign", camp="TWR21", res=5222, oo=2552, rent=2210, town=150,
         biz=21, built=(2012, 2018), lam=0.0140),
    dict(name="Coachwood Park", feeder="YRB25", kind="rest", res=950, oo=560, rent=200, town=50, biz=17,
         built=(1990, 2010), infill=14, lam=0.0224),
    dict(name="Bunya Ridge", feeder="YRB26", kind="campaign", camp="BNR23", res=5154, oo=2622, rent=760, town=340,
         biz=44, built=(1980, 2002), lam=0.0210, lam_boom=0.1050),
    dict(name="Bloodwood", stream="Mount Cotter", feeder="YRB26", kind="rest", res=650, oo=500, rent=110, town=0, biz=12,
         built=(1970, 2016), infill=12, lam=0.0285),
    dict(name="Wattleview", feeder="YRB27", kind="campaign26", camp="WTV26", res=5240, oo=4790, rent=150, town=60,
         biz=18, built=(2019, 2023), lam=0.0538),
    dict(name="Jacaranda Gardens", feeder="YRB27", kind="rest", res=2600, oo=1620, rent=520, town=140, biz=37,
         built=(1980, 2009), infill=24, lam=0.0238),
    dict(name="Ironbark Hill", feeder="YRB28", kind="campaign", camp="IBH22", res=2481, oo=1820, rent=300, town=90,
         biz=16, built=(1986, 2002), lam=0.0300, lam_boom=0.0500),
    dict(name="Ferndale Rise", feeder="YRB28", kind="rest", res=2200, oo=1380, rent=420, town=120, biz=33,
         built=(1982, 2011), infill=20, lam=0.0231),
]

# Load transfers between feeders: (locality, share of its streets moved, from, to, date). Yarrabin North moved whole
# when YRB21 was extended in 2023; the 2024-25 rebalancing moved sections of four localities. The network model
# carries each NMI's feeder at the base date; a record stamped earlier carries the feeder of its day.
TRANSFERS = [
    ("Yarrabin North", 1.00, "YRB23", "YRB21", dt.date(2023, 5, 15)),
    ("Coachwood Park", 0.30, "YRB25", "YRB22", dt.date(2024, 3, 18)),
    ("Jacaranda Gardens", 0.12, "YRB27", "YRB28", dt.date(2024, 8, 5)),
    ("Tanners Flat", 0.30, "YRB23", "YRB26", dt.date(2025, 2, 10)),
    ("Bloodwood", 0.35, "YRB26", "YRB24", dt.date(2025, 6, 16)),
]

# Campaigns: key, suburb, sign-ups open, sign-ups close, appointed installer, information sessions, and eps, the
# campaign's own departure from the suburb's uplift (the installer's offer, the season, the sessions).
CAMPAIGNS = [
    dict(key="GLM18", suburb="Glenmorrow", open=dt.date(2018, 9, 3), close=dt.date(2018, 11, 23),
         installer="SunCoast Solar Installations", sessions=2, eps=0.0060),
    dict(key="KJP19", suburb="Kurrajong Park", open=dt.date(2019, 9, 2), close=dt.date(2019, 11, 22),
         installer="Brightline Energy Solutions", sessions=2, eps=-0.0580),
    dict(key="TWR21", suburb="Tallowwood Rise", open=dt.date(2021, 9, 6), close=dt.date(2021, 11, 26),
         installer="Brightline Energy Solutions", sessions=3, eps=0.0450),
    dict(key="SKO22", suburb="Silky Oak", open=dt.date(2022, 3, 7), close=dt.date(2022, 5, 27),
         installer="Greenhaven Electrical", sessions=2, eps=0.1400),
    dict(key="IBH22", suburb="Ironbark Hill", open=dt.date(2022, 9, 5), close=dt.date(2022, 11, 25),
         installer="Greenhaven Electrical", sessions=2, eps=-0.0080),
    dict(key="BNR23", suburb="Bunya Ridge", open=dt.date(2023, 9, 4), close=dt.date(2023, 11, 24),
         installer="SunCoast Solar Installations", sessions=3, eps=-0.1270),
    dict(key="PBG24", suburb="Paperbark Grove", open=dt.date(2024, 9, 2), close=dt.date(2024, 11, 22),
         installer="Riverstone Solar", sessions=2, eps=-0.0450),
]
UPLIFT = 1.18          # a campaign's systems per first application from its suburb's owner-occupied houses in the
                       # year before sign-ups opened (the clean truth; each campaign departs from it by eps)
CAMPAIGNS_2026 = [
    dict(key="BDW26", suburb="Bindarra Waters", feeder="YRB24", open=dt.date(2026, 9, 1), close=dt.date(2026, 11, 27)),
    dict(key="WTV26", suburb="Wattleview", feeder="YRB27", open=dt.date(2026, 9, 1), close=dt.date(2026, 11, 27)),
]
CAMP = {c["key"]: c for c in CAMPAIGNS}

# Base excess over hosting capacity (MW) before the 2026 campaigns, by feeder: the hosting capacity assessment's
# 2029 figures are set from these after the simulation; YRB27's is set from its golden excess.
TARGET_BASE_EXCESS = {"YRB21": 1.112, "YRB22": 1.208, "YRB23": 0.438, "YRB24": 1.004, "YRB25": 1.063,
                      "YRB26": -0.657, "YRB28": 0.712}
TARGET_GOLDEN_YRB27 = 1.903

# File names (the pack)
REGISTER = "eg_connection_applications_20260901.csv"
LEGACY = "legacy_inverter_equipment.csv"
NETWORK = "nmi_network_model_20260831.csv"
XREF = "nmi_property_xref_2026.csv"
RATES = "merindah_rates_roll_2026-27.csv"
PROGRAM_LOG = "solar_streets_program_summary.xlsx"
LETTER = "solar_streets_2026_letter_to_mirrabee.pdf"
NPP = "NPP-114_micro_EG_forecasting_rev3.pdf"
HCA = "yarrabin_hosting_capacity_assessment_2026.pdf"
DER = "der_register_extract_yarrabin_20260901.csv"
REALLOC = "nmi_reallocations_2019-2026.csv"
DICTIONARY = "data_dictionary.xlsx"
MANIFEST = "export_manifest.csv"
PEAK = "feeder_peak_demand_forecast_2027-31.xlsx"
REBATE = "home_battery_rebate_approvals_fy2025-26.csv"
DISTRACTORS = [PEAK, REBATE]

# Golden deliverables
GOLD_BOOK = "feeder_upgrade_2029.xlsx"
GOLD_CHART = "yarrabin_pv_vs_hosting_2029.png"


def rng(*keys):
    """One independent stream per key path, so changing one locality or one file never re-rolls another."""
    h = 0
    for k in keys:
        for ch in str(k):
            h = (h * 131 + ord(ch)) % (2 ** 61 - 1)
    return np.random.default_rng([SEED, h])


def nmi_checksum(nmi10):
    """The NEM NMI checksum: from the rightmost character, double every second character's ASCII value, sum the
    digits of every value, and take the distance to the next multiple of ten."""
    total = 0
    double = True
    for ch in reversed(nmi10):
        v = ord(ch)
        if double:
            v *= 2
        total += sum(int(d) for d in str(v))
        double = not double
    return str((10 - total % 10) % 10)


def fy_of(d):
    return d.year + 1 if d.month >= 7 else d.year


def fy_label(end_year):
    return "FY%d-%02d" % (end_year - 1, end_year % 100)


def add_days(d, n):
    return d + dt.timedelta(days=int(n))


def business_day(d):
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return d


def iso(d):
    return d.isoformat() if d else ""


def write_csv(path, header, rows, crlf=False):
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(header)
    n = 0
    for r in rows:
        w.writerow(["" if v is None else v for v in r])
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return n


def long_date(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)
