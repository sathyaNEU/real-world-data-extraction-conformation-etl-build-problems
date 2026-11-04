"""task476 architecture 5: the fixed world. Tallis Creek Paper Company's mill's run-of-river hydro project, its bypassed reach and
gauge BP-1, the gauge's Rating 7, the 2026 season's inflows, the plant's bypass setpoints and the 27 July storm that left
gravel on the gauge's riffle control. Every figure the pack carries is drawn here or in sim.py from fixed seeds."""
import datetime as dt

SEED = 476_05
COMPANY = "Tallis Creek Paper Company"
PROJECT = "Tallis Creek Mill Hydroelectric Project"
CREEK = "Tallis Creek"
CONSULTANT = "Corvid Hydrometric Services"
GAUGE = "BP-1"
MANAGER = "Marissa Harmon"          # compliance manager
HYDROGRAPHER = "Melinda Walter"     # consultant hydrographer
SUPER = "Krista Soto"               # plant superintendent
REGULATOR = "the Commission"

PST = dt.timezone(dt.timedelta(hours=-8))
PDT = dt.timezone(dt.timedelta(hours=-7))
STEP_MIN = 10
REC_START = dt.datetime(2026, 4, 28, 0, 0, tzinfo=PST)
REC_END = dt.datetime(2026, 11, 4, 0, 0, tzinfo=PST)          # exclusive
SEASON = (dt.date(2026, 5, 1), dt.date(2026, 10, 31))

# Rating 7 (2023): low-water segment on the riffle control, high-water segment on the channel above 4.00 ft
R7_E, R7_C, R7_B = 0.80, 22.0, 2.30
R7_TOP = 4.00
R7_HI_A, R7_HI_K, R7_HI_P = None, 260.0, 1.60      # Q = Q_low(4.00) + K (h - 4.00)^P above the break
TABLE_LO, TABLE_HI = 1.00, 4.00
SHIFT_FT = 0.10                     # gravel on the control: the riffle's zero-flow stage rises by this
STORM_PEAK = dt.datetime(2026, 7, 27, 22, 40, tzinfo=PST)

TURBINE_MAX, TURBINE_MIN = 150.0, 25.0

# Article 403 minimum flows (local calendar days) and the plant's setpoints (rated cfs, local time)
def requirement(day):
    return 50.0 if dt.date(2026, 7, 1) <= day <= dt.date(2026, 9, 30) else 30.0


SETPOINTS = [  # (local time, rated cfs, log text)
    (dt.datetime(2026, 4, 1, 0, 0, tzinfo=PDT), 34.0, "Bypass target 34 cfs (Article 403 minimum 30 cfs, Oct to Jun)"),
    (dt.datetime(2026, 7, 1, 0, 0, tzinfo=PDT), 54.0, "Bypass target 54 cfs (Article 403 minimum 50 cfs, Jul to Sep)"),
    (dt.datetime(2026, 9, 14, 0, 0, tzinfo=PDT), 64.0, "Bypass target 64 cfs, fall pulse under the fisheries agreement"),
    (dt.datetime(2026, 9, 21, 0, 0, tzinfo=PDT), 54.0, "Bypass target 54 cfs, pulse ended"),
    (dt.datetime(2026, 10, 1, 0, 0, tzinfo=PDT), 33.0, "Bypass target 33 cfs (Article 403 minimum 30 cfs, Oct to Jun)"),
]
UNIT_TRIP = dt.datetime(2026, 7, 27, 21, 10, tzinfo=PDT)
UNIT_BACK = dt.datetime(2026, 7, 28, 9, 30, tzinfo=PDT)

VISITS = [  # the hydrographer's visits: local arrival, minutes to set up, minutes measuring, the staff plate's reading
    # less the logger's at arrival (ft), and the measurement's error against the flow the reach carried while it ran
    (dt.datetime(2026, 5, 6, 10, 40, tzinfo=PDT), 14, 36, 0.00, -0.0024),
    (dt.datetime(2026, 6, 9, 11, 20, tzinfo=PDT), 23, 64, 0.00, 0.0021),
    (dt.datetime(2026, 7, 1, 13, 5, tzinfo=PDT), 9, 31, 0.00, 0.0208),
    (dt.datetime(2026, 7, 26, 10, 15, tzinfo=PDT), 12, 27, -0.01, -0.0219),
    (dt.datetime(2026, 7, 29, 9, 40, tzinfo=PDT), 18, 42, -0.01, -0.0021),
    (dt.datetime(2026, 8, 25, 14, 30, tzinfo=PDT), 11, 33, 0.01, 0.0069),
    (dt.datetime(2026, 9, 16, 10, 50, tzinfo=PDT), 16, 38, 0.00, 0.0003),
    (dt.datetime(2026, 10, 6, 12, 20, tzinfo=PDT), 8, 26, -0.01, -0.0058),
]
CONTROL = ["clear", "clear", "clear", "light algae", "clear", "light algae", "clear", "leaves"]

FILES = {
    "stage": "gauge/bp1_stage_2026.csv",
    "register": "gauge/bp1_station_register.xlsx",
    "rating_report": "gauge/bp1_rating7_report_2023.pdf",
    "visits": "gauge/bp1_field_visits_2026.csv",
    "temp": "gauge/bp1_water_temperature_2026.csv",
    "release": "operations/bypass_release_log_2026.csv",
    "generation": "operations/daily_generation_2026.csv",
    "license": "license/license_order_excerpt_2019.pdf",
    "plan": "license/flow_monitoring_plan_2024.pdf",
    "precip": "weather/powerhouse_precipitation_2026.csv",
    "prior": "reports/2025_annual_flow_compliance_report.pdf",
}
SPRING_ARTICLE_AF = 20000      # Article 404: the bypass passes at least this in May and June


def q_rating7(h):
    """The published relation, both segments."""
    if h <= R7_E:
        return 0.0
    lo = R7_C * (h - R7_E) ** R7_B
    if h <= R7_TOP:
        return lo
    top = R7_C * (R7_TOP - R7_E) ** R7_B
    return top + R7_HI_K * (h - R7_TOP) ** R7_HI_P


def q_true(h, t):
    """The channel as it was: Rating 7 until the storm's peak, the same relation on a control raised by SHIFT_FT after."""
    return q_rating7(h - SHIFT_FT) if t >= STORM_PEAK else q_rating7(h)


def h_for(q, rel, t=None):
    lo, hi = 0.80, 9.0
    for _ in range(80):
        m = (lo + hi) / 2
        v = rel(m) if t is None else rel(m, t)
        if v < q:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2
