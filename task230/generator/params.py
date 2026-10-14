"""task230 architecture 3: the Office of the Registrar General of Aldmere, census 2026 occupation coding quality.
Every quantity the generator draws from is set here."""
from datetime import date

SEED = 230301
CENSUS_DAY = date(2026, 4, 21)
ONLINE_OPEN = date(2026, 4, 6)
CODING_START = date(2026, 5, 4)          # coding week 1 starts on this Monday
NRFU_LIST = date(2026, 6, 19)            # follow-up workload cut from the address register
NRFU_START = date(2026, 6, 22)
FIELD_CLOSE = date(2026, 10, 31)         # close of field operations
EXTRACT = date(2026, 11, 13)             # coding extract and study file pulled (Friday)
RULE_CHANGE = date(2026, 11, 16)         # acceptance score lowered from this Monday
CODING_CLOSE = date(2027, 1, 22)         # coding must be complete (processing plan)
RELEASE = date(2027, 3, 30)              # first occupation release (statutory)
OLD_ACCEPT, NEW_ACCEPT = 0.90, 0.80
WARNING = 2.0                            # per cent, either direction (OQ-4)

ROUTES = ["O", "P", "FS", "FP"]          # online self, paper self, follow-up household member, follow-up proxy

# addresses and households
N_EDS = 1104
ADDR_PER_ED = 527
VACANT, NONRES = 0.052, 0.011
EARLY_SR = {"O": 0.497, "P": 0.191}      # share of occupied households responding before the follow-up list is cut
LATE_SR = {"O": 0.094, "P": 0.031}       # share of follow-up occupied cases closed by a late self-response
HH_P = [0.30, 0.24, 0.18, 0.15, 0.12, 0.10]   # household member completes at visit k
PX_P = [0.0, 0.0, 0.35, 0.45, 0.55, 0.80]     # proxy taken at visit k when no household member completes
MOPUP = date(2026, 9, 1)                  # mop-up phase: supervisors push open cases to a close
PX_MOP = [0.0, 0.0, 0.66, 0.76, 0.85, 0.95]   # proxy taken at visit k in the mop-up phase
GAP_MOP = (3, 4.0)                        # days between calls in the mop-up phase
REFUSE = 0.05
FIRST_VISIT_BY = date(2026, 9, 18)   # enumerators work through their caseloads
GAP_MIN, GAP_MEAN = 6, 7.5          # days between calls at a case
REINTERVIEW = 0.03                       # a proxy return later replaced by a household member interview
REINTERVIEW_BY = date(2026, 9, 18)       # supervisors stop re-interview requests as the field winds down
WRITEINS = [(0, 0.30), (1, 0.33), (2, 0.29), (3, 0.06), (4, 0.02)]
BLANK = {"O": 0.010, "P": 0.020, "FS": 0.030, "FP": 0.150}   # persons in employment whose occupation is left blank
CUT = date(2026, 8, 13)                  # batches created up to this date are coded by the extract (calibrated)

# write-ins and coding
PHRASES = {
    "office": ("4110", 0.833, 0.895), "business": ("3339", 0.906, 0.990), "accounts": ("4311", 0.915, 0.990),
    "computers": ("3512", 0.892, 0.956), "IT": ("3512", 0.814, 0.901), "engineer": ("3115", 0.700, 0.853),
    "labourer": ("9313", 0.907, 0.986), "factory": ("9329", 0.719, 0.907), "hospital": ("5321", 0.739, 0.799),
    "shop": ("5223", 0.898, 0.973), "farm": ("9211", 0.775, 0.956), "driver": ("8322", 0.830, 0.925),
}
# per true sub-major group: self-report vague rate (online; paper and household-member follow-up by SELF_MULT), proxy
# vague rate, self phrase mix, proxy phrase mix
VAGUE = {
    "24": (0.0336, 0.2132, {"office": 1.0}, {"accounts": 0.55, "office": 0.25, "business": 0.2}),
    "25": (0.0105, 0.1500, {"computers": 1.0}, {"IT": 0.85, "computers": 0.15}),
    "71": (0.0015, 0.1932, {"labourer": 1.0}, {"labourer": 1.0}),
    "72": (0.0203, 0.0427, {"factory": 1.0}, {"factory": 0.6, "engineer": 0.4}),
    "21": (0.0074, 0.0196, {"engineer": 1.0}, {"engineer": 1.0}),
    "74": (0.0011, 0.0240, {"labourer": 1.0}, {"engineer": 0.6, "labourer": 0.4}),
    "26": (0.0238, 0.0199, {"office": 1.0}, {"office": 1.0}),
    "12": (0.0081, 0.0333, {"office": 0.7, "business": 0.3}, {"office": 0.6, "business": 0.4}),
    "43": (0.0247, 0.0613, {"office": 1.0}, {"office": 1.0}),
    "75": (0.0051, 0.0353, {"factory": 1.0}, {"factory": 1.0}),
    "81": (0.0274, 0.0350, {"factory": 1.0}, {"factory": 1.0}),
    "22": (0.0052, 0.1436, {"hospital": 1.0}, {"hospital": 1.0}),
    "32": (0.0043, 0.0525, {"hospital": 1.0}, {"hospital": 1.0}),
    "14": (0.0029, 0.0523, {"shop": 1.0}, {"shop": 1.0}),
    "61": (0.0010, 0.0309, {"farm": 1.0}, {"farm": 1.0}),
    "96": (0.0051, 0.0323, {"driver": 1.0}, {"driver": 1.0}),
}
SELF_MULT = {"O": 1.0, "P": 1.3, "FS": 2.2}
RECOVER = {"O": 0.862, "P": 0.849, "FS": 0.838, "FP": 0.672}   # clerical coder finds a vague write-in's own group
SPEC_RIGHT = 0.92          # autocoder's suggestion is the write-in's own unit group
SPEC_SLIP = 0.005          # suggestion in a related group of another sub-major group (the rest: same sub-major group)
CLER_SLIP = 0.004          # clerical code in a related group of another sub-major group
CLER_INSIDE = 0.055        # clerical code in another unit group of the same sub-major group
CLER_NATIONAL = 0.08       # clerical code's national fifth digit chosen afresh (it may differ from the reference's)
SLIP_PAIRS = [("2221", "3221"), ("2411", "3313"), ("2144", "3115"), ("2142", "3112"), ("2341", "5312"),
              ("5120", "9412"), ("1420", "5222"), ("3343", "4120"), ("2423", "4416"), ("3322", "5223"),
              ("1120", "1219"), ("1321", "3122"), ("3434", "5120"), ("4222", "5244"), ("5414", "9629"),
              ("6222", "8350"), ("7322", "8189"), ("8219", "9329"), ("9112", "5153"),
              ("1345", "2359"), ("2330", "2320"), ("7411", "7412"), ("3412", "2635"),
              ("4226", "4110"), ("5131", "9412"), ("7212", "7214"), ("3511", "2522"), ("1412", "5131")]

SLIP_MULT = {0: 1.32, 1: 0.69, 2: 2.98, 3: 0.65, 4: 0.54, 5: 0.98, 6: 0.34, 7: 2.11, 8: 1.08, 9: 3.0, 10: 3.0,
             11: 0.98, 12: 0.63, 13: 0.65, 14: 1.45, 15: 0.41, 16: 0.99, 17: 1.41, 18: 0.57, 19: 2.25,
             20: 0.64, 21: 0.34, 22: 0.43, 23: 1.13, 24: 0.61, 25: 0.42, 26: 1.91, 27: 3.0}   # pair index: multiplier on the pair's slip rates

# coding quality study: selection interval by batch type and coding path (one record in k)
STUDY_K = {("SELF", "A"): 10, ("SELF", "C"): 4, ("NRFU", "A"): 2, ("NRFU", "C"): 2}
ADJUDICATED = (0.06, 0.34)  # share of studied records whose two expert codes disagreed: specific, vague
