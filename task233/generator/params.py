"""task233 parameters: the school-leaver destinations survey of a fictional island state, its 2025 nonresponse follow-up and
the 2026 release whose quality flags the survey director signs."""
import numpy as np

SEED = 233
TRACE_FRAC = 0.85            # share of close-time nonrespondents the 2025 follow-up resolved (the world's traced set)
SAMPLE_EXTRA = 0.034         # further sampled nonrespondents the field team could not resolve (share of all nonrespondents)
DUP_SHARE = 0.045            # resolved cases found by two routes (two rows, one outcome)
LATE_SHARE = 0.028           # 2025 leavers who returned after the 2025 close (respondents in the final file)
ADDED_SHARE = 0.012          # 2025 leavers added to the frame after the close (schools' late leaver lists)
ADDED_RETURNED = 0.30        # of those, the share who returned a form late

# the departure the follow-up measures: one odds ratio for NEET and one for higher education, every band and district
OR_N, OR_H = 2.6, 0.40
D_N, D_H = np.log(OR_N), np.log(OR_H)

# attainment bands, index 0 lowest points (AB4) to 3 highest (AB1)
B = 4
BAND_LABEL = ["AB4", "AB3", "AB2", "AB1"]
bN = np.array([1.45, 0.50, -0.40, -1.35])
bH = np.array([-2.0, -0.70, 0.45, 1.55])
UREL = np.array([1.8, 1.15, 0.75, 0.45])            # relative nonresponse by band
AFF = np.array([.08, .20, .36, .36]); DEP = np.array([.32, .34, .24, .10])
# the remainder (not NEET, not HE) split into further education, apprenticeship or training, employment, by band
REST = np.array([[.30, .30, .40], [.38, .27, .35], [.40, .22, .38], [.45, .15, .40]])
CATS = ["HE", "FE", "APP", "EMP", "NEET"]

# districts in the simulation's order (most affluent first); code order is geographic
#            name              code   aN     aH    t     m24    m25    m26   followed up in 2025
DISTRICTS = [
    ("Southern Shore",  "ED06", -4.10,  0.95, 0.12, 0.150, 0.190, 0.1175, 0),
    ("Upper Valley",    "ED08", -3.80,  1.05, 0.15, 0.080, 0.190, 0.115, 1),
    ("Glen Villages",   "ED07", -3.55,  0.35, 0.22, 0.090, 0.100, 0.11, 0),
    ("Hill Country",    "ED09", -3.30,  0.65, 0.26, 0.140, 0.150, 0.23, 0),
    ("Northern Plains", "ED10", -2.75,  0.20, 0.32, 0.150, 0.190, 0.2325, 1),
    ("Market Towns",    "ED11", -2.50,  0.05, 0.42, 0.130, 0.150, 0.1475, 0),
    ("Coastal Strip",   "ED05", -2.20, -0.20, 0.50, 0.120, 0.135, 0.135, 0),
    ("Riverside",       "ED03", -1.90, -0.45, 0.58, 0.140, 0.190, 0.2225, 1),
    ("City West",       "ED02", -1.60, -0.75, 0.66, 0.120, 0.140, 0.185, 0),
    ("City East",       "ED01", -1.30, -1.05, 0.74, 0.130, 0.190, 0.1775, 1),
    ("Old Docks",       "ED04", -1.20, -1.60, 0.82, 0.090, 0.100, 0.12, 0),
    ("Mill Towns",      "ED12", -1.25, -1.95, 0.88, 0.120, 0.190, 0.1325, 1),
]
ND = len(DISTRICTS)
NAME = [d[0] for d in DISTRICTS]
CODE = [d[1] for d in DISTRICTS]
TRACED = [i for i, d in enumerate(DISTRICTS) if d[8]]

# the two schools that moved district on the 2026 map: (simulation district on the 2026 map, district on the 2025 map)
MOVED = [(4, 3), (11, 10)]

# flag bands on the sensitivity shift, percentage points
BAND_CAUTION, BAND_SUPPRESS = 1.0, 3.0

# calendar
CENSUS_2025, CENSUS_2026 = "2025-10-01", "2026-10-01"
CLOSE_2025 = "2025-10-24T16:00:00Z"     # 17:00 Irish Summer Time
CLOSE_2026 = "2026-10-30T17:00:00Z"     # 17:00 Greenwich Mean Time (clocks went back on 25 October)
EDITION_SWITCH = "2026-10-02T08:00:00Z" # the 2026 edition of the online form went live at 09:00 local the next morning
FOLLOWUP_DRAWN = "2025-10-31"
ALLOC_RUN_2026 = "2026-11-09"
EXTRACT_2026 = "2026-11-10"
RELEASE_2026 = "2026-12-10"
FINAL_2025 = "2026-03-31"

PEOPLE = {"head": "Polly Ganley", "field": "Emmett Phelan", "method": "Leanne Henebry"}
ORG = "Social Survey Unit"
DIVISION = "Leaver Destinations Survey"
