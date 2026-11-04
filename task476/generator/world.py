"""task476 architecture 3: the fixed world. Ochre Flats Farming Company's wells, accounts, loggers, meters, parcels,
the agency's allocation and the utility's tariff. Every figure the pack carries is drawn here or in sim.py from fixed
seeds, so two builds are byte-identical."""
import datetime as dt
from zoneinfo import ZoneInfo

import numpy as np

SEED = 476_03
PST = dt.timezone(dt.timedelta(hours=-8))          # the loggers' clock all year
LA = ZoneInfo("America/Los_Angeles")               # local prevailing time
UTC = dt.timezone.utc
T0 = dt.datetime(2025, 8, 1, 0, 0, tzinfo=PST)     # hour index 0 of the simulation, on the loggers' clock
PACK_START = dt.datetime(2025, 9, 1, 0, 0, tzinfo=PST)   # the exports and logger files start here
T1 = dt.datetime(2026, 11, 1, 0, 0, tzinfo=PST)    # end (exclusive)
NH = int((T1 - T0).total_seconds() // 3600)
WY_START = dt.datetime(2025, 10, 1, 0, 0, tzinfo=LA)
WY_END = dt.datetime(2026, 10, 1, 0, 0, tzinfo=LA)
CUTOVER_UTC = dt.datetime(2026, 4, 1, 7, 0, tzinfo=UTC)   # the utility's portal change, midnight 1 April local
AF_GAL = 325851.0
KWH_AF_FT = 1.0241                                 # kWh per acre-foot per foot of head at 100 per cent efficiency

COMPANY = "Ochre Flats Farming Company"
SHORT = "Ochre Flats"
AGENCY = "Sallow Plains Groundwater Sustainability Agency"
AGENCY_SHORT = "Sallow Plains GSA"
SUBBASIN = "Sallow Plains Subbasin"
UTILITY = "Valley Rural Power"
DISTRICT = "Alkali Slough Water District"
TESTER_A = "Gutierrez Pump Testing"
TESTER_B = "Basin Hydrotech Services"
WATER_MANAGER = "Melinda Walter"
PARTNER = "Nicholas Wolf"
AGENCY_PM = "Tamara Larson"

ALLOC_RATE = 2.85        # acre-feet per gross acre, water year 2026 (sustainable yield 1.10 plus transitional 1.75)
SY_RATE, TR_RATE = 1.10, 1.75
CARRYOVER = 480          # acre-feet carried from water year 2025
TRANSFER_BLOCK = 50
TRANSFER_PRICE = 1185    # dollars an acre-foot, the agency's posted reference price for intra-basin transfers

# Parcels: (APN, gross acres). The acres are set so the ranch's position against its allocation sits where the
# design note's ladder puts it; they are fixed numbers, not tuned per build.
PARCELS = [("042-110-07", 1004.6), ("042-110-08", 652.1), ("042-120-15", 1281.3), ("042-120-19", 487.9),
           ("042-130-02", 846.4), ("042-130-11", 948.4)]

# Well identities: (well, ranch name, state well number, agency well ID, APN, aquifer, metered)
IDS = [
    ("W-01", "Pump 1 (Sec 3 North)", "18S/21E-03D01M", "SPG-0412", "042-110-07", "Upper", True),
    ("W-02", "Pump 2 (Sec 3 South)", "18S/21E-03M02M", "SPG-0413", "042-110-07", "Upper", True),
    ("W-03", "Pump 4 (Sec 10 Shop)", "18S/21E-10C01M", "SPG-0415", "042-110-08", "Upper", True),
    ("W-04", "Pump 5 (Sec 10 East)", "18S/21E-10H03M", "SPG-0416", "042-120-15", "Upper", True),
    ("W-05", "Pump 6 (Sec 11 Res)", "18S/21E-11E01M", "SPG-0418", "042-120-15", "Upper", False),
    ("W-06", "Pump 9 (Sec 14 West)", "18S/21E-14D02M", "SPG-0421", "042-120-19", "Upper", False),
    ("W-07", "Deep 1 (Sec 3 Main)", "18S/21E-03F05M", "SPG-0414", "042-110-07", "Lower", False),
    ("W-08", "Deep 2 (Sec 10 Main)", "18S/21E-10K02M", "SPG-0417", "042-110-08", "Lower", False),
    ("W-09", "Deep 3 (Sec 11 Res)", "18S/21E-11G04M", "SPG-0419", "042-120-15", "Lower", False),
    ("W-10", "Deep 4 (Sec 14 Main)", "18S/21E-14B01M", "SPG-0422", "042-120-19", "Lower", False),
    ("W-11", "Deep 5 (Sec 15 North)", "18S/21E-15A03M", "SPG-0424", "042-130-02", "Lower", False),
    ("W-12", "Deep 6 (Sec 15 South)", "18S/21E-15P01M", "SPG-0425", "042-130-02", "Lower", False),
    ("W-13", "Deep 7 (Sec 22 North)", "18S/21E-22C02M", "SPG-0427", "042-130-11", "Lower", False),
    ("W-14", "Deep 8 (Sec 22 Res)", "18S/21E-22J01M", "SPG-0428", "042-130-11", "Lower", False),
    ("W-15", "Deep 9 (Sec 23 West)", "18S/21E-23E02M", "SPG-0430", "042-130-11", "Lower", False),
]
WELLS = [i[0] for i in IDS]
UPPER = [i[0] for i in IDS if i[5] == "Upper"]
LOWER = [i[0] for i in IDS if i[5] == "Lower"]
METERED = [i[0] for i in IDS if i[6]]
ENROLLED = UPPER                     # the agency's upper-aquifer level network: these report static depths
REPLACED_2024 = {"W-08": "2024-02-21", "W-11": "2024-03-06", "W-13": "2024-02-28"}   # pump and bowls replaced

# Logger serials as installed now (the register's view) and the June 2026 swap the download log records.
LOGGER_NOW = {"W-01": "2079416", "W-02": "2081044", "W-03": "2079433", "W-04": "2081107", "W-05": "2080962",
              "W-06": "2079458", "W-07": "922341", "W-08": "922357", "W-09": "922362", "W-10": "922380",
              "W-11": "922394", "W-12": "922401", "W-13": "922415", "W-14": "922428", "W-15": "922433"}
SWAP_DATE = dt.datetime(2026, 6, 10, 10, 0, tzinfo=PST)    # W-02's and W-04's loggers swapped at a download visit
SWAP = ("W-02", "W-04")
BARO = "2066318"


def logger_at(well, t):
    """The serial logging in a well at time t (before the swap W-02 held W-04's present logger and vice versa)."""
    if well in SWAP and t < SWAP_DATE:
        other = SWAP[1] if well == SWAP[0] else SWAP[0]
        return LOGGER_NOW[other]
    return LOGGER_NOW[well]


SCHED_SWITCH = dt.datetime(2026, 6, 1, 0, 0, tzinfo=LA)       # accounts moved from AG-2T to AG-3T on the utility's letter
SWITCHED = [w for w in WELLS if w not in ("W-01", "W-03")]

HOLIDAYS_2026 = ["2026-01-01", "2026-02-16", "2026-05-25", "2026-07-03", "2026-09-07", "2026-11-11", "2026-11-26",
                 "2026-12-25"]
# energy rates, dollars a kWh, effective 1 March 2026; summer is June to September
TARIFF = {
    "AG-2T": {"summer": {"peak": 0.38914, "part": 0.27642, "off": 0.21318}, "winter": {"part": 0.26183, "off": 0.22406}},
    "AG-3T": {"summer": {"peak": 0.33120, "part": 0.23968, "off": 0.18755}, "winter": {"part": 0.22827, "off": 0.19641}},
}


def tou_period(local):
    """The schedule's period for a local prevailing time (minute resolution)."""
    season = "summer" if 6 <= local.month <= 9 else "winter"
    wk = local.weekday() < 5 and local.strftime("%Y-%m-%d") not in HOLIDAYS_2026
    m = local.hour * 60 + local.minute
    if season == "summer":
        if wk and 12 * 60 <= m < 18 * 60:
            return season, "peak"
        if wk and (8 * 60 + 30 <= m < 12 * 60 or 18 * 60 <= m < 21 * 60 + 30):
            return season, "part"
        return season, "off"
    if wk and 8 * 60 + 30 <= m < 21 * 60 + 30:
        return season, "part"
    return season, "off"


def _accounts():
    rng = np.random.default_rng(SEED + 7)
    old = {w: "%010d" % int(rng.integers(4_400_000_000, 4_499_999_999)) for w in WELLS}
    new = {w: "SA-%07d" % int(rng.integers(1_100_000, 1_999_999)) for w in WELLS}
    return old, new


SA_OLD, SA_NEW = _accounts()


def _params():
    rng = np.random.default_rng(SEED)
    out = {}
    for w, name, swn, gid, apn, aq, met in IDS:
        if aq == "Lower":
            base = rng.uniform(292, 318)          # mean depth to static water, feet below ground
            amp = rng.uniform(52, 64)             # seasonal half-swing, deepest late August
            trend = rng.uniform(6, 10)            # feet a year of chronic decline
            sc = rng.uniform(32, 44)              # gpm per foot of drawdown
            q_bep = rng.uniform(1500, 1950)
            tau_rec = rng.uniform(10, 16)         # hours, recovery time constant after a stop
            depth = int(rng.integers(980, 1260))
            hp = int(rng.choice([300, 300, 350, 400]))
            stick = round(float(rng.uniform(1.6, 2.6)), 2)
        else:
            base = rng.uniform(118, 146)
            amp = rng.uniform(2.0, 3.6)
            trend = rng.uniform(0.2, 0.6)
            sc = rng.uniform(46, 66)
            q_bep = rng.uniform(950, 1300)
            tau_rec = rng.uniform(3.0, 5.0)
            depth = int(rng.integers(390, 470))
            hp = int(rng.choice([100, 125, 125, 150]))
            stick = round(float(rng.uniform(1.0, 2.0)), 2)
        disch = rng.uniform(36, 44) * 2.31
        col = rng.uniform(6, 11)
        h_mid = base + q_bep / sc + disch + col
        h0 = h_mid * rng.uniform(1.30, 1.38)
        a = (h0 - h_mid) / q_bep ** 2
        eta_max = rng.uniform(0.71, 0.78)
        motor = rng.uniform(0.925, 0.945)
        bowl = int(round(base + amp + 2 * q_bep / sc + rng.uniform(55, 80))) if aq == "Lower" else \
            int(round(base + 2 * q_bep / sc + rng.uniform(60, 90)))
        out[w] = dict(well=w, name=name, swn=swn, gid=gid, apn=apn, aq=aq, metered=met, base=base, amp=amp,
                      trend=trend, sc=sc, q_bep=q_bep, tau_rec=tau_rec, depth=depth, hp=hp, stick=stick,
                      disch=disch, col=col, h0=h0, a=a, eta_max=eta_max, motor=motor, bowl=bowl,
                      sensor=round(base + amp + 2 * q_bep / sc + (30 if aq == "Lower" else 25) + float(rng.uniform(0, 12)), 1))
    return out


P = _params()

FILES = {
    "power_old": "power/vrp_usage_export_2025-09-01_2026-03-31.csv",
    "power_new": "power/vrp_interval_data_2026-04-01_2026-10-31.csv",
    "rate_letter": "power/vrp_rate_change_confirmation_2026-05-14.pdf",
    "tariff": "power/vrp_agricultural_tou_schedules_2026.pdf",
    "register": "ranch/ochre_flats_well_register.xlsx",
    "meters": "ranch/totalizer_reads_wy2026.xlsx",
    "download_log": "levels/logger_download_log.csv",
    "baro": "levels/%s_barologger.csv" % BARO,
    "notice": "agency/sallow_plains_gsa_wy2026_allocation_notice.pdf",
    "template": "agency/wy2026_extraction_return_template.csv",
    "district": "district/alkali_slough_wd_deliveries_wy2026.csv",
    "cimis": "weather/sallow_plains_west_station_daily_2025-09_2026-10.csv",
}


def logger_file(serial):
    return "levels/%s.csv" % serial


def test_file(job):
    return "pump_tests/%s.pdf" % job
