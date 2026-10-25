"""task301 constants: Coast and Tablelands PHN, its five sub-regions, the quit outreach team's 2025 year in Eastern
Shore and the 2027 placement, the smoking-status record 2012 to 2026 and the seeds."""
import datetime as dt

ORG = "Coast and Tablelands PHN"
TEAM = "Quit outreach team"

SEED_WORLD = 30121         # patients, practices, smoking trajectories, status recordings
SEED_PILOT = 30122         # the 2025 Eastern Shore list and its calls
SEED_ASK = 30123           # ask files
SEED_DOCS = 30124          # documents and distractors

D0 = dt.date(2012, 1, 1)                                   # the status record starts (the extraction tool's window)
EXTRACT = dt.date(2026, 9, 30)                             # the active patient extract
PILOT_LIST = dt.date(2025, 1, 31)                          # the 2025 list: current smokers at the end of January
PILOT_CALLS = (dt.date(2025, 2, 3), dt.date(2025, 11, 28))  # the team's calling year in Eastern Shore
YEAR = 2027                                                # the placement year, calls spread evenly through it
HORIZON = dt.date(2028, 3, 31)                             # trajectories run to here (four weeks past December calls)
AS_OF = dt.date(2026, 10, 21)                              # the folder for the November executive meeting

REG = ["P", "A", "B", "C", "D"]
NAME = {"P": "Eastern Shore", "A": "Coastal Hinterland", "B": "Inner South", "C": "Northern Corridor",
        "D": "Western Plains"}
CAND = ["A", "B", "C", "D"]
# active adult patients at the extract (Eastern Shore's count is its January 2025 roll, before the year's leavers)
N = {"P": 46000, "A": 118000, "B": 41000, "C": 46000, "D": 42000}
# smoker to ex-smoker a year, ex-smoker to smoker a year (true rates of the world)
QUIT = {"P": 0.060, "A": 0.110, "B": 0.045, "C": 0.070, "D": 0.060}
RELAPSE = 0.015
# ever smoked, and current among the ever-smokers on 1 January 2012
EVER = 0.40
CUR0 = {"P": 0.46, "A": 0.56, "B": 0.46, "C": 0.46, "D": 0.46}
# status recordings a year at a consultation, without a chronic condition review (x LTC_MULT with one)
BASE = {"P": 0.16, "A": 0.035, "B": 0.20, "C": 0.15, "D": 0.38}
LTC_MULT = 3.2
REG_RECORD = 0.70          # a status taken on the new-patient form at registration
P_DRIVE = 0.70             # Eastern Shore's 2024 recording drive: share of active patients recorded once
P_DRIVE_WIN = (dt.date(2024, 2, 5), dt.date(2024, 11, 22))
PRACTICES = {"P": 11, "A": 22, "B": 9, "C": 10, "D": 9}
LEAVE_P = 0.07             # Eastern Shore patients on the January 2025 roll who left before the 2026 extract

# the team, as it worked in Eastern Shore in 2025 (true process parameters)
REACH = 0.76               # answers within the team's three attempts
QUIT_DATE = 0.31           # a current smoker reached sets a quit date
ABSTAIN = 0.52             # not smoking four weeks after the quit date
LTFU = 0.30                # of those smoking or unknown at four weeks, the share the team cannot contact

# recording noise
EX_AS_NEVER = 0.025        # an ex-smoker's status entered as never smoked or non-smoker
DUP_SAMEDAY = 0.015        # the same status entered twice in one consultation
CORRECT_SAMEDAY = 0.003    # a status entered then corrected in the same consultation

# clinical systems: vocabulary of each, with the current-smoker detail where the system records it
SYSTEMS = {"BP": "Best Practice", "MD": "Medical Director"}
VOCAB = {"BP": {"S": ["Daily smoker", "Weekly smoker", "Irregular smoker"], "E": "Ex-smoker", "N": "Never smoked"},
         "MD": {"S": ["Smoker"], "E": "Ex-smoker", "N": "Non-smoker"}}
BP_DETAIL = [0.80, 0.08, 0.12]
MIGRATION = ("A", dt.date(2021, 3, 15))    # one Coastal Hinterland practice moved from Medical Director to Best Practice

CALL_ROUND = 50            # the placement figure is given to the nearest 50
