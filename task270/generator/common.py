"""Constants for task270: Kleerwissel's 2027 proxy metric for six-month retention. Dates, metric keys, the layers of
the experimentation platform, the file names and the people, in one place so the world, the pack and the goldens read
the same values."""
import datetime as dt

SEED = 59
ORG = "Kleerwissel"
PULL = dt.date(2026, 10, 23)              # the scorecard export and the registry extract
ASSEMBLED = dt.datetime(2026, 10, 26, 9, 40)
FIRST_DAY = dt.date(2024, 1, 8)           # the first onboarding experiment of the archive starts
LAST_DAY = dt.date(2026, 10, 9)           # the last sign-up day the export carries
RENAME = dt.date(2025, 3, 3)              # metric store migration: the scorecard keys renamed
LATE_EVENTS = (dt.date(2025, 7, 1), dt.date(2025, 9, 10))   # two-week reads computed before the late iOS events
RECOMPUTED = dt.date(2025, 9, 15)
HOLDOUT_YEARS = {2025: 0.05, 2026: 0.05}  # the global holdout's share of new consumer users
HOLDOUT_2027 = 0.03

CAND = ["active_days_d1_14", "sessions_d1_14", "first_purchase_d14", "items_saved_d1_14", "push_opens_d1_14"]
RET = "retained_m6"
GUARD = ["uninstalled_d14", "support_contacts_d14"]
METRICS = CAND + [RET] + GUARD
OLD_KEY = {"active_days_d1_14": "act_days_14", "sessions_d1_14": "sess_count_14", "first_purchase_d14": "first_buy_14",
           "items_saved_d1_14": "fav_saves_14", "push_opens_d1_14": "push_open_14", "retained_m6": "ret_d180",
           "uninstalled_d14": "uninst_14", "support_contacts_d14": "cs_contacts_14"}
LABEL = {"active_days_d1_14": "active days, days 1 to 14", "sessions_d1_14": "sessions, days 1 to 14",
         "first_purchase_d14": "first purchase within 14 days", "items_saved_d1_14": "items saved, days 1 to 14",
         "push_opens_d1_14": "push notifications opened, days 1 to 14", "retained_m6": "retained at six months"}
SHORT = {"active_days_d1_14": "Active days", "sessions_d1_14": "Sessions", "first_purchase_d14": "First purchase",
         "items_saved_d1_14": "Items saved", "push_opens_d1_14": "Push opens", "retained_m6": "Six-month retention"}
LAYERS = ["signup_flow", "first_feed", "notifications"]
TEAMS = {"signup_flow": ["Activation", "Identity"], "first_feed": ["Discovery", "Buyer Experience"],
         "notifications": ["Messaging", "Lifecycle"]}

FILES = {
    "scorecards": "experiment_scorecards_2024_2026.csv",
    "registry": "onboarding_experiments_2024_2026.csv",
    "holdout": "global_holdout_users_2025.csv",
    "catalogue": "metric_catalogue.yaml",
    "standard": "proxy_metric_standard_2027.pdf",
    "export_notes": "scorecard_export_notes.txt",
    "guide": "experimentation_platform_guide.pdf",
    "calendar": "onboarding_calendar_2027q1.csv",
    "forecast": "new_user_forecast_2027.csv",
    "cohorts": "signup_cohorts_2025.csv",
    "ratings": "app_store_ratings_2024_2026.csv",
    "spend": "acquisition_spend_2026.xlsx",
}
DISTRACTORS = ["ratings", "spend"]
DELIVERABLES = ["proxy_metric_review_2027.pptx", "proxy_metric_scores_2027.xlsx"]
DECK, BOOK = DELIVERABLES

HEAD_EXP = "Fiene Kronenberg"     # head of experimentation, owner of the standard
ENGINEER = "Giel Lansink"          # data engineer, the export notes and the platform guide
ANALYST = "Saar Reimes"           # growth analyst, the metric catalogue and the 2027 calendar

Z_POWER = 1.959963984540054 + 0.8416212335729143   # two-sided 5 per cent test, 80 per cent power


def r(x, n):
    """round half away from zero at n decimals, the way the deliverables print"""
    from decimal import Decimal, ROUND_HALF_UP
    q = Decimal(1).scaleb(-n)
    return float(Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP))
