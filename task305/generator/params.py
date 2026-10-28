"""task305 (architecture 3): Brindlecote Software's free-plan three-project limit, the world's constants.

Months are counted from January 2000 (m = 0); the research panel runs from January 2023 (276) to September 2026
(320), the limit starts on 1 January 2027 (324) and the year it is sized over ends in December 2027 (335)."""

ORG = "Brindlecote Software Ltd"
SEED = 30503

APPS = ["Tracewood", "Taskfold", "Ledgerline", "Formbox", "Notewell"]
CODE = {"Tracewood": "TRW", "Taskfold": "TSK", "Ledgerline": "LDG", "Formbox": "FBX", "Notewell": "NTW"}
OLD_NAME = {"Notewell": "Leafnote"}          # renamed in April 2025
RENAME_MONTH = 303                          # April 2025: the panel and the KPI carry the old name before it
LAUNCH = [161, 185, 177, 201, 146]          # Jun 2013, Jun 2015, Oct 2014, Oct 2016, Mar 2012 (by APPS order)

# Plus, a month, pounds before VAT (the price list), and the free-plan revenue per active free account a month
# (Finance's 2026 run rate: marketplace commission, advertising, partner referrals).
PLUS = [20.0, 8.0, 28.0, 13.0, 6.0]
FREE_REV = [2.00, 0.45, 1.00, 0.06, 0.80]

# sign-ups a month per app in the simulated full population, before seasonality
SIGNUPS = [2165, 850, 826, 993, 852]
SEASON = [1.16, 1.06, 1.02, 0.96, 0.94, 0.90, 0.88, 0.92, 1.10, 1.06, 1.00, 0.86]

M_PANEL0, M_EXTRACT, M_LIMIT, M_LAST = 276, 320, 324, 335
M_SIM0 = 146                                 # the first launch
PANEL_RATE = 25                              # one account in twenty-five, drawn at sign-up

CAP = 2048.0                                 # the free plan's storage allowance, MiB
STOP_AT = 2024.0                             # the next upload no longer fits
TRIM = (0.15, 0.45)                          # a trimmed account keeps this share of the allowance
LEARN = 0.35                                 # and fills it at this share of its old pace
RESPONSE = (0.05, 0.36)                      # a stopped free account: upgrades, leaves (the rest trims)
PAID_CHURN = 0.018                           # a Plus account cancels, a month
SKIP = 0.015                                 # an established free account goes a month unused


def own_rates(t):
    """own-accord upgrade and leave hazards a month by months since sign-up (scalars or numpy arrays)"""
    import numpy as np
    u = np.where(t == 0, 0.05, np.where(t <= 2, 0.012, 0.002))
    lv = np.where(t == 0, 0.35, np.where(t <= 2, 0.12, np.where(t <= 11, 0.02, 0.0028)))
    return u, lv


PROJ_BIRTH = (0.085, 0.70)                   # an account's project-creation rate a month: lognormal median, sigma
PROJ_DEATH = 0.02                            # each active project is archived with this chance a month
STORE_GROW = (32.0, 0.75)                    # MiB a month: lognormal median, sigma
STORE_TILT = 0.5                             # accounts that open many projects keep smaller files in them
CLEANUP = (0.03, 0.6, 0.9)                   # chance a month, and the share an account keeps after a clean-up

AS_OF = "2026-10-12"                         # the folder was put together
PEOPLE = {"head": "Lynne Powell", "cfo": "Leonard Young", "analyst": "Frederick Nicholls"}
DOMAIN = "brindlecote.co.uk"


def ym(m):
    return "%04d-%02d" % (2000 + m // 12, m % 12 + 1)


def month_of(year, month):
    return (year - 2000) * 12 + month - 1


FILES = {
    "paper": "free_plan_limit_paper_2027.pdf",
    "thread": "re_free_plan_limit_which_app_first.eml",
    "catalogue": "plan_catalogue_2026.csv",
    "kpi": "free_accounts_by_active_projects_2023_2026.xlsx",
    "panel_accounts": "research_panel_accounts.csv",
    "panel_months": "research_panel_account_months_2023_2026.csv",
    "subs": "billing_subscriptions_20250930.csv",
    "events": "billing_subscription_events_20251001_20260930.csv",
    "fx": "fx_plan_rates.csv",
    "policy": "recurring_revenue_policy_fin07.pdf",
    "ratings": "app_store_ratings_2023_2026.csv",
    "acquisition": "acquisition_spend_2026.xlsx",
}
