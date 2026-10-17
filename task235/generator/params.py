"""task235 parameters: Fogbell Games' match-3 game Kittiwake Cove, its twelve production builds, the analytics SDK's
delivery, the players and the purchase catalogue. Times are UTC unless a name says otherwise."""
import datetime as dt

SEED = 235
WORLD_SEED = 19                      # players, devices, sessions, purchases (sim.World)
EVENT_SEED = 238009                  # SDK delivery and losses (sim.World.events)
RECORD_SEED = SEED * 7 + 3           # ids, prices, rates, distractors (records.Records)

STUDIO = "Fogbell Games"
GAME = "Kittiwake Cove"
SDK = "Tern"
PEOPLE = {"dq": "Amelia Seery", "sdk": "Padraic Cormick", "release": "Darragh Boylan"}

T0 = dt.datetime(2026, 10, 5, 0, 0)            # the session export starts
RUN = dt.datetime(2026, 11, 9, 7, 0)            # Monday's run (07:00 Irish time = UTC in November)
WIN0 = dt.datetime(2026, 10, 11, 23, 0)         # 12 October 00:00 Irish Summer Time
WIN1 = dt.datetime(2026, 11, 9, 0, 0)           # 9 November 00:00 Irish (GMT)
IST_END = dt.datetime(2026, 10, 25, 1, 0)       # Irish Summer Time ends 25 October 01:00 UTC
LINE = 0.02                                     # the alert line

# builds: platform, version, build number (iOS CFBundleVersion, Android versionCode), released, SDK, minimum OS
BUILDS = [
    ("ios", "7.38.2", "4417", dt.datetime(2026, 8, 12, 16), "4.6.3", "iOS 15"),
    ("ios", "7.39.1", "4521", dt.datetime(2026, 9, 2, 16), "4.6.3", "iOS 15"),
    ("ios", "7.40.0", "4588", dt.datetime(2026, 9, 23, 16), "4.6.3", "iOS 15"),
    ("ios", "7.41.0", "4652", dt.datetime(2026, 10, 14, 16), "4.6.3", "iOS 16"),
    ("ios", "7.41.1", "4671", dt.datetime(2026, 10, 21, 16), "4.6.3", "iOS 16"),
    ("ios", "7.42.0", "4730", dt.datetime(2026, 11, 5, 16), "5.0.1", "iOS 16"),
    ("android", "7.38.1", "7380100", dt.datetime(2026, 8, 13, 15), "4.6.3", "Android 8"),
    ("android", "7.39.0", "7390000", dt.datetime(2026, 9, 2, 15), "4.6.3", "Android 8"),
    ("android", "7.40.2", "7400200", dt.datetime(2026, 9, 28, 15), "4.6.3", "Android 8"),
    ("android", "7.41.0", "7410000", dt.datetime(2026, 10, 14, 15), "4.6.3", "Android 8"),
    ("android", "7.41.3", "7410300", dt.datetime(2026, 10, 24, 15), "4.6.3", "Android 8"),
    ("android", "7.42.0", "7420000", dt.datetime(2026, 11, 5, 15), "5.0.1", "Android 8"),
]
# 7.42.0's staged rollout: the share of automatic updates offered it from each date
ROLLOUT = [(dt.datetime(2026, 11, 5, 16), 0.30), (dt.datetime(2026, 11, 6, 9), 0.55), (dt.datetime(2026, 11, 7, 9), 0.80)]

# the two builds that drop purchase events (share of purchases whose event is never created), and every build's
# background loss (an event dropped with the app's data, a queue lost to a crash on write)
DROP = {("android", "7.41.0"): 0.065, ("ios", "7.42.0"): 0.050}
BASE_DROP = 0.003

# a purchase event is late when the player leaves the game before the SDK's next upload (4.6: every 30 s in the
# foreground); 5.0 sends it at once on iOS, while on Android it waits for the system's job scheduler, which holds it
# when the game leaves the foreground
LATE = {"heavy": 0.08, "regular": 0.11, "casual": 0.30, "tablet": 0.40}
LATE_50_IOS = 0.03
LATE_50_ANDROID = 3.0                           # times the 4.6 share
QUICK_RETURN = 0.15                             # back within 30 minutes: no new session, the queue goes then

# players: share, mean hours between sessions; casual players come back after 5 to 13 days most of the time
CLASSES = {"heavy": (0.25, 14.0), "regular": (0.45, 30.0), "casual": (0.30, 40.0)}
CASUAL_LONG = 0.70
CASUAL_LONG_DAYS = (6.0, 17.0)
AUTO_UPDATE = {"heavy": 0.93, "regular": 0.85, "casual": 0.25}
N_ACCOUNTS = {"ios": 5200, "android": 6400}
TABLET = {"ios": 0.40, "android": 0.06}                 # signed-in players with a tablet as well
OLD_IPAD = 0.80                                 # of iPads: models that 7.41.0's minimum (iOS 16) leaves on 7.40.0
BUY = 0.09                                      # purchase chance per session at unit intensity
BUY_CASUAL = 2.0
BUY_TABLET = 3.0
QUIT = 0.002                                    # chance a device stops playing after a session
REINSTALL = 0.0015                              # chance a session is the first after a reinstall (new device id)
UPGRADE = 0.45                                  # guests who sign in (upgrade) after a purchase in the window
UPGRADE_PROMPT = 0.85                           # guests on 7.42.0, which asks them to sign in after a purchase
OLD_ACCOUNT = 0.50                              # upgrading guests who sign in to an account they made before (no link)
MERGE_AFTER_UPGRADE = 0.30                      # upgraded players whose older signed-in account support then merges
MERGE = 0.03                                    # other signed-in accounts merged by player support

# products: id, kind, price tier in EUR (the store's tier for the euro storefronts)
PRODUCTS = [
    ("kc.coins.250", "consumable", 1.99, 0.30), ("kc.coins.1200", "consumable", 5.49, 0.24),
    ("kc.coins.3000", "consumable", 10.99, 0.10), ("kc.coins.8000", "consumable", 21.99, 0.04),
    ("kc.boosters.starter", "consumable", 2.99, 0.14), ("kc.boosters.mega", "consumable", 8.99, 0.06),
    ("kc.lives.unlimited_2h", "consumable", 1.09, 0.08), ("kc.harbour_pass.monthly", "subscription", 6.99, 0.04),
]
# storefronts: country, currency, share of players, price multiplier against the euro tier, VAT-inclusive pricing
STOREFRONTS = [
    ("US", "USD", 0.30, 1.0000, False), ("GB", "GBP", 0.10, 0.9000, True), ("DE", "EUR", 0.09, 1.0, True),
    ("FR", "EUR", 0.06, 1.0, True), ("IE", "EUR", 0.02, 1.0, True), ("NL", "EUR", 0.03, 1.0, True),
    ("BR", "BRL", 0.07, 5.0000, True), ("JP", "JPY", 0.05, 150.0, True), ("CA", "CAD", 0.05, 1.3800, False),
    ("AU", "AUD", 0.04, 1.5300, True), ("MX", "MXN", 0.04, 17.900, True), ("PL", "PLN", 0.03, 4.3000, True),
    ("SE", "SEK", 0.02, 11.000, True), ("IN", "INR", 0.04, 80.000, True), ("KR", "KRW", 0.06, 1450.0, True),
]
