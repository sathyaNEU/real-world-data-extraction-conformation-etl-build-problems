"""task464 architecture 12: the world's fixed facts (Quaywork, a UK job board, and its 2026 restart pilot).

Every number the simulation draws from lives here, so the pack, the goldens and the checks read one source.
"""
import datetime as dt

SEED = 464

BOARD = "Quaywork"
BOARD_LTD = "Quaywork Ltd"
ESP = "Postvane"            # the email platform since March 2025
ESP_OLD = "Inkrelay"      # the email platform before it
PEOPLE = {"head": "Marian Smith", "analyst": "Glenn Taylor", "cfo": "Tracy Parkes"}

START = dt.date(2025, 1, 1)
END = dt.date(2026, 11, 8)          # last day in the extracts
ASOF = dt.date(2026, 11, 16)        # the plan's date
MIGRATION = dt.date(2025, 3, 17)    # Inkrelay to Postvane
POOL_DATE = dt.date(2026, 4, 1)     # the paused pool is drawn
SENDS = [dt.date(2026, 4, 14) + dt.timedelta(days=28 * k) for k in range(6)]
WINDOW = 28                          # a send is judged over the 28 days from it
PILOT_END = SENDS[-1] + dt.timedelta(days=WINDOW - 1)   # 28 September 2026
SENDS_2027 = 13

PROVIDERS = ["Google", "Microsoft", "Yahoo", "Apple", "BT", "Sky", "Virgin Media", "TalkTalk", "Other"]
DOMAINS = {
    "Google": ["gmail.com", "googlemail.com"],
    "Microsoft": ["hotmail.co.uk", "hotmail.com", "outlook.com", "live.co.uk", "msn.com"],
    "Yahoo": ["yahoo.co.uk", "yahoo.com", "ymail.com", "aol.com", "aol.co.uk"],
    "Apple": ["icloud.com", "me.com", "mac.com"],
    "BT": ["btinternet.com", "btopenworld.com"],
    "Sky": ["sky.com"],
    "Virgin Media": ["virginmedia.com", "ntlworld.com", "blueyonder.co.uk"],
    "TalkTalk": ["talktalk.net", "tiscali.co.uk"],
    "Other": [],
}
# active jobseekers by provider, and their per-capita propensity to click a sponsored job
ACTIVE_SHARE = [0.47, 0.21, 0.07, 0.10, 0.04, 0.02, 0.03, 0.02, 0.04]
PROPENSITY = [1.00, 0.93, 0.86, 1.06, 0.82, 0.88, 0.90, 0.84, 0.95]
# the paused pool of 1 April 2026 skews to older addresses
POOL_SHARE = [0.36, 0.26, 0.12, 0.07, 0.06, 0.03, 0.03, 0.02, 0.05]
POOL_SIZE = 861_400
HOLDOUT = 0.10

# the mailbox providers that filed Quaywork's mail as junk after each restart send: peak share of alert clicks lost
JUNK_PEAK = {"Google": 0.338, "Microsoft": 0.472, "Yahoo": 0.42}
JUNK_TAU = 3.5            # days, the decay of the filing after its peak on the day after a send
JUNK_DAY0 = 0.55          # the send day's share of the peak (the send goes out mid-morning)
SUBSTITUTION = 0.35       # share of the alert clicks lost to junk that the same jobseekers make on the site or app

ACTIVE_BASE = 1_380_000
ALERT_RATE = 0.040        # sponsored clicks per active jobseeker per day from the alerts
SITE_RATE = 0.031         # from the website
APP_RATE = 0.025          # from the app (grows over the record)
WEEKDAY_ALERT = [1.22, 1.12, 1.05, 1.00, 0.86, 0.62, 0.80]
WEEKDAY_SITE = [1.15, 1.10, 1.06, 1.02, 0.90, 0.70, 0.86]

# the restart series: the share of mailed, deliverable, still-paused jobseekers who restart from each send
RESTART_P = [0.016, 0.0095, 0.007, 0.0058, 0.005, 0.0045]
SELF_RESTART_28 = 0.0022  # restarts on the site or app by paused jobseekers, per 28 days, with or without the email
DEAD_SHARE = 0.06         # addresses that hard bounce
RESTORED_RATE = 0.033     # sponsored clicks per restarted jobseeker per day
APP_SHARE_RESTORED = 0.45
LOGGED_OUT_APP = 0.22     # share of a restarted jobseeker's app clicks made logged out (device only)
REPAUSE_DAYS = 90

# link-scanning gateways at university and business addresses (and a few consumer ones)
GATEWAY_SHARE = {"Other": 0.30, "Microsoft": 0.016}
GATEWAY_SCAN_P = 0.24     # chance a gateway scans a given restart email
LINKS_PER_RESTART_EMAIL = 11
