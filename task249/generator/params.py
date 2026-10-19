"""Constants for task249: the Rhenhagener Anzeiger's twelve local editions on one website, the analytics tag's
identifier under WebKit's seven-day limit on script-written storage, the paywall meter kept in the same storage, the
registration wall and print subscribers' digital access; the circulation system and the newsletter platform for the
media kit's other figures."""
import datetime as dt

SEED = 249_4
TZ = "Europe/Berlin"
HIST_START = dt.date(2027, 11, 1)          # simulated history starts here (local days; two months settle the readers)
WALL_START = dt.date(2028, 3, 1)           # the registration wall replaced the soft subscription prompt
Q4_START = dt.date(2028, 10, 1)
END = dt.date(2028, 12, 31)                # last simulated local day
AS_OF = dt.date(2029, 1, 15)               # the analysis; the kit goes to advertisers on 1 February 2029
KIT_DATE = dt.date(2029, 2, 1)
CAP_DAYS = 7.0                             # WebKit: script-written storage lasts 7 days from its last write
FREE = 5                                   # metered articles free per calendar month
P_REG = 0.40                               # a wall session ends in a free registration
P_SUB = 0.007                              # a wall session ends in a paid digital subscription
TOLERANCE = 0.25                           # the note: reported above the edition's browsers by more than a quarter
DEVICES = ("mobile", "tablet", "desktop")
TYPES = ("D", "R", "W", "O", "X")
# reader types: daily, regular, weekly, occasional, one-off.  P(a visit on a given day) for D and R; renewal gaps
# (gamma shape, mean days) for W, O and X
DAY_P = {"D": 0.80, "R": 0.55}
W_GAP = (25.0, 10.0)                       # about weekly, every eight to twelve days
O_GAP = (4.0, 14.0)
X_GAP = (1.0, 42.0)
SESS_PER_DAY = {"D": 1.15, "R": 1.10, "W": 1.12, "O": 1.08, "X": 1.04}   # mean sessions on a visit day
METERED = {"D": 1.7, "R": 1.5, "W": 1.45, "O": 1.75, "X": 1.2}          # metered reads per session (Poisson mean)
PAGES = {"D": 3.4, "R": 3.0, "W": 2.8, "O": 2.4, "X": 1.9}            # page views per session (1 + Poisson)
# print subscribers read online weekly or occasionally; their digital access is activated with the subscriber number
PRINT_P = {"D": 0.12, "R": 0.16, "W": 0.38, "O": 0.24, "X": 0.010}
REFUSER = 0.05                             # readers who never register at the wall
MULTI_EDITION = 0.05                       # browsers that also read a neighbouring edition
MULTI_SHARE = 0.30                         # share of such a browser's visit days on the second edition
BOT_SHARE = 0.018                          # platform-flagged automated sessions
INTERNAL_BROWSERS = 140                    # newsroom browsers (the group's own address range)
SHARED_ACCOUNTS = 0.22                     # signed-in browsers whose account also signs in on a second browser

EDITIONS = [
 # ladder role in the comment; population, device mix (m, t, d), WebKit share (m, t, d), print scale, print Apple
 # skew, weekly tilt, one-off and regular multipliers
 dict(code="RHS", name="Rhenhagen Stadt", state="HE", pop=12600, dev=(.68, .08, .24), wk=(0.5127, 0.7689, 0.1954), print_scale=0.45, skew=1.25, tilt=1.20, xmult=0.80, rmult=1.00),   # high
 dict(code="KBR", name="Kirchbrunn", state="RP", pop=12000, dev=(.62, .11, .27), wk=(0.3093, 0.5743, 0.1106), print_scale=2.00, skew=2.60, tilt=0.90, xmult=1.70, rmult=1.00),   # print
 dict(code="ALH", name="Altenhorst", state="HE", pop=6600, dev=(.63, .10, .27), wk=(0.2859, 0.5830, 0.1044), print_scale=0.90, skew=1.30, tilt=0.80, xmult=1.00, rmult=1.00),   # low
 dict(code="WBR", name="Wiesbrück", state="HE", pop=10800, dev=(.66, .09, .25), wk=(0.4161, 0.6615, 0.1547), print_scale=0.22, skew=1.20, tilt=1.55, xmult=1.00, rmult=1.00),   # meter
 dict(code="HOL", name="Hollerfeld", state="RP", pop=6000, dev=(.61, .12, .27), wk=(0.2875, 0.5215, 0.1044), print_scale=2.10, skew=2.80, tilt=0.85, xmult=1.80, rmult=1.00),   # print
 dict(code="SOW", name="Sonnweiler", state="HE", pop=9600, dev=(.67, .09, .24), wk=(0.4144, 0.6628, 0.1469), print_scale=0.18, skew=1.20, tilt=1.45, xmult=1.20, rmult=1.00),   # meter
 dict(code="MST", name="Mühlenstedt", state="RP", pop=7200, dev=(.63, .10, .27), wk=(0.3348, 0.6248, 0.1173), print_scale=1.80, skew=2.60, tilt=0.90, xmult=1.50, rmult=1.00),   # print
 dict(code="GRH", name="Grauheim", state="HE", pop=6000, dev=(.65, .10, .25), wk=(0.4127, 0.6341, 0.1508), print_scale=0.25, skew=1.20, tilt=1.60, xmult=1.10, rmult=1.00),   # meter
 dict(code="EIT", name="Eichtal", state="RP", pop=5400, dev=(.61, .11, .28), wk=(0.2091, 0.4012, 0.0712), print_scale=2.10, skew=2.80, tilt=0.60, xmult=3.00, rmult=0.60),   # low, print
 dict(code="BST", name="Bergstetten", state="HE", pop=6300, dev=(.66, .09, .25), wk=(0.4397, 0.7099, 0.1689), print_scale=0.30, skew=1.20, tilt=0.70, xmult=1.50, rmult=1.00),   # low
 dict(code="LDN", name="Lindenau", state="HE", pop=8100, dev=(.69, .08, .23), wk=(0.3651, 0.5435, 0.1315), print_scale=0.30, skew=1.30, tilt=1.80, xmult=1.00, rmult=1.00),   # meter
 dict(code="FKR", name="Falkenried", state="RP", pop=5100, dev=(.60, .12, .28), wk=(0.2378, 0.4566, 0.0810), print_scale=2.00, skew=2.70, tilt=0.60, xmult=2.80, rmult=0.60),   # low, print
]
BASE_MIX = {"mobile": (.22, .17, .21, .22, .24), "tablet": (.30, .17, .20, .19, .20), "desktop": (.32, .19, .17, .17, .21)}
CODES = [e["code"] for e in EDITIONS]
OLD_CODE = {"HOL": "HKR"}                  # Hollerfeld's content group before the URL change of 1 November 2028
RECODE_DAY = dt.date(2028, 11, 1)

# browsers and their user-agent families, by device class and engine
UA_FAMILIES = {
    ("mobile", True): [("ios_safari", .66), ("ios_chrome", .16), ("ios_inapp", .08), ("ios_gsa", .06), ("ios_firefox", .02), ("ios_edge", .02)],
    ("mobile", False): [("and_chrome", .68), ("and_samsung", .20), ("and_firefox", .04), ("and_webview", .05), ("and_opera", .03)],
    ("tablet", True): [("ipad_safari", .82), ("ipad_chrome", .14), ("ipad_firefox", .04)],
    ("tablet", False): [("andtab_chrome", .75), ("andtab_samsung", .20), ("andtab_firefox", .05)],
    ("desktop", True): [("mac_safari", 1.0)],
    ("desktop", False): [("win_chrome", .52), ("win_edge", .24), ("win_firefox", .08), ("mac_chrome", .10), ("mac_firefox", .03), ("linux_firefox", .03)],
}

NEWSROOM_PREFIX = "85.214.110.0/24"

PEOPLE = {"head": "Nadin Schleich", "analytics": "Karl-Hans Schenk", "accounts": "Eugenia Oderwald", "sales": "Almut Ladeck"}
ORG = "Rhenhagen Mediengruppe"
PAPER = "Rhenhagener Anzeiger"

# publication: Monday to Saturday, not on public holidays (Hesse and Rhineland-Palatinate)
HOLIDAYS = {"HE": [dt.date(2028, 10, 3), dt.date(2028, 12, 25), dt.date(2028, 12, 26)],
            "RP": [dt.date(2028, 10, 3), dt.date(2028, 11, 1), dt.date(2028, 12, 25), dt.date(2028, 12, 26)]}
