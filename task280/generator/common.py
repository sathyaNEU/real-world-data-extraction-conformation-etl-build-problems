"""Constants for task280: the Orlenford Valley Cable Commission, its franchisee Tollard Cable, the eight hubs, the
plans, the node classes, the measurement window, the people, the dates and the pack's file names."""
import datetime as dt

SEED = 7
REC_SEED = 7                                  # the record-level draw (households that moved in the window)
COMMISSION = "Orlenford Valley Cable Commission"
COMMISSION_SHORT = "OVCC"
FRANCHISEE = "Tollard Cable"
FRANCHISEE_LEGAL = "Tollard Cable Communications, LLC"
COMPANY = COMMISSION
PANEL = "Orlenford Valley Broadband Measurement Panel"
ASSEMBLED = dt.datetime(2026, 11, 24, 10, 15)
SCHEDULE_DATE = dt.date(2024, 6, 12)          # the renewed franchise agreement's Network Performance Schedule
NOTICE_DUE = dt.date(2026, 12, 15)
WINDOW_START = dt.date(2026, 9, 14)           # a Monday
WINDOW_END = dt.date(2026, 11, 13)            # a Friday
DAYS = (WINDOW_END - WINDOW_START).days + 1   # 61
STANDARD = 0.80                               # of the plan's advertised download speed
LINE = 20.0                                   # per cent of the weekday evening peak
PEAK_FROM, PEAK_TO = 19, 23                   # local hours, Monday to Friday
EXTRACT_FROM, EXTRACT_TO = 17, 24             # the panel's evening extract, local hours
FILING_FROM, FILING_TO = 16, 25               # the utilisation filing's evening intervals, local hours (to 1 am)

# code, name
HUBS = [("BW", "Bellwick"), ("CM", "Carrow Mills"), ("DF", "Dunfield"), ("EH", "Eastholm"), ("GH", "Greyhaven"),
        ("KB", "Kesterbrook"), ("LM", "Larchmoor"), ("SC", "Sedgecombe")]
HUB = [h[0] for h in HUBS]
HUB_NAME = dict(HUBS)

# code, name, advertised download Mbit/s, advertised upload Mbit/s, monthly price USD
PLANS = [("E100", "Essential 100", 100, 10, 49.99), ("P300", "Plus 300", 300, 20, 64.99),
         ("M600", "Max 600", 600, 35, 79.99), ("G1000", "Gig 1000", 1000, 35, 94.99)]
PLAN_DOWN = {p[0]: p[2] for p in PLANS}
PLAN_NAME = {p[0]: p[1] for p in PLANS}

# node class: name, downstream capacity Mbit/s as the register gives it
NODE_CLASSES = {"D30-24": ("DOCSIS 3.0, 24 channels", 880), "D30-32": ("DOCSIS 3.0, 32 channels", 1170),
                "D31": ("DOCSIS 3.1, 32 channels and one OFDM block", 3050)}

PEOPLE = {
    "director": "Travis Delgado",        # the Commission's executive director, signs the notice
    "panel": "Kathleen Mcdonald",        # the panel manager
    "tollard": "Donna Atkins",           # Tollard's director of regulatory affairs
}

FILES = {
    "contents": "ovcc_2026_review_pack_index.txt",
    "schedule": "franchise_network_performance_schedule.pdf",
    "methods": "panel_methods_note_2026.pdf",
    "dictionary": "ovcc_panel_data_dictionary.pdf",
    "closeout": "designation_closeout_2025.pdf",
    "tests": "panel_download_tests_2026_evening.csv",
    "units": "panel_units.csv",
    "households": "panel_households.csv",
    "plans": "tollard_plan_catalogue.csv",
    "subs": "tollard_subscription_history.csv",
    "nodes": "tollard_node_register.csv",
    "addr": "tollard_address_node_table.csv",
    "util": "tollard_node_utilisation_2026q3q4.csv",
    "outages": "tollard_outage_reports_2026.csv",
    "subcounts": "tollard_node_subscriber_counts_2026.xlsx",
    "complaints": "ovcc_consumer_complaints_2026.csv",
    "latency": "panel_latency_2026_evening.csv",
}
DISTRACTORS = ("complaints", "latency")
GOLDEN = "hub_peak_congestion_2026.xlsx"
CHART = "hub_peak_congestion_2026.png"
DELIVERABLES = (GOLDEN, CHART)

UTC = dt.timezone.utc
DST_END_UTC = dt.datetime(2026, 11, 1, 6, 0)  # 2:00 am EDT on Sunday 1 November 2026


def offset_hours(local_naive):
    """US Eastern offset from UTC for a local wall time in the window: -4 (EDT) before the 1 November change, -5
    (EST) from it; a wall time in the repeated hour is read as the first (EDT) one."""
    return -4 if local_naive < dt.datetime(2026, 11, 1, 2, 0) else -5


def to_utc(local_naive):
    return local_naive - dt.timedelta(hours=offset_hours(local_naive))


def to_local(utc_naive):
    return utc_naive + dt.timedelta(hours=-4 if utc_naive < DST_END_UTC else -5)


def day(i):
    return WINDOW_START + dt.timedelta(days=i)


def weekday(i):
    return day(i).weekday() < 5


HOLIDAYS = {dt.date(2026, 10, 12): "Columbus Day", dt.date(2026, 11, 11): "Veterans Day"}
