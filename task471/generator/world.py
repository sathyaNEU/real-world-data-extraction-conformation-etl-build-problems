"""task471 world: an unnamed state's Department of Health, its Private Well Program and the 2025-26 Private Well
Nitrate Survey, sampled separately from two overlapping lists of private domestic wells in each of sixteen counties;
the 2027 Well Water Assistance allocation goes to the counties with an estimated 250 or more such wells above the
nitrate standard."""
import datetime as dt

SEED = 471
DEPT = "Department of Health"
OFFICE = "Office of Environmental Public Health"
PROGRAM = "Private Well Program"
SURVEY = "2025-26 Private Well Nitrate Survey"
ALLOCATION = "Well Water Assistance"
PEOPLE = {"manager": "Tina Hurley",            # Private Well Program manager
          "epi": "Steven Nguyen",              # environmental epidemiologist who designed the survey
          "assist": "Carlos Phillips"}         # Well Water Assistance coordinator

STANDARD_N = 10.0          # mg/L nitrate as nitrogen
NO3_PER_N = 4.427          # mg/L nitrate (as NO3) per mg/L nitrate as nitrogen
QUALIFY = 250              # estimated wells above the standard for a county to qualify
PERMITS_SINCE = 1986       # domestic wells drilled under permit since
SURVEY_START = dt.date(2025, 9, 8)
TESTS_CLOSE = dt.date(2026, 4, 30)
RETESTS_CLOSE = dt.date(2026, 6, 30)
AS_OF = dt.date(2026, 8, 14)

LABS = {"HAL": "Halvorsen Analytical", "CED": "Cedarline Environmental Laboratories", "KIN": "Kinsale Water Testing"}

# county: name, code, wells on either list, share permit-only, share parcel-only, share both, nitrate median (mg/L N)
# for permit-only, parcel-only and both, log-spread, tested from the permit list, tested from the parcel list, lab.
# The numbers are placed by calibrate.py (see the design note's Ladder); geology and land use set the medians.
COUNTIES = [
    ("Alderwick", "C01"), ("Brannock", "C02"), ("Corwell", "C03"), ("Dunmere", "C04"),
    ("Eskvale", "C05"), ("Farrowdale", "C06"), ("Glenmoor", "C07"), ("Hallowcroft", "C08"),
    ("Ivyridge", "C09"), ("Kestrel Plains", "C10"), ("Lindmark", "C11"), ("Morrowfield", "C12"),
    ("Netherby", "C13"), ("Oakmere", "C14"), ("Quarrington", "C15"), ("Rushbrook", "C16"),
]
LAB_OF = {"C01": "HAL", "C02": "HAL", "C03": "CED", "C04": "KIN", "C05": "HAL", "C06": "CED", "C07": "CED",
          "C08": "KIN", "C09": "HAL", "C10": "KIN", "C11": "CED", "C12": "HAL", "C13": "KIN", "C14": "CED",
          "C15": "HAL", "C16": "KIN"}

# placed by calibrate.py (pattern GBECEBAECCBEAEEC: A qualifies on every route; G qualifies on every route but the
# parcel list's, its permit-only wells running high; B qualifies but pooling drops it; C falls short but adding the two
# lists' estimates lifts it over; E falls short on every route)
PLACED = [
    {'N': 2977, 'po': 0.432, 'qo': 0.161, 'mPo': 4.97, 'mQo': 2.03, 'mB': 1.38, 'sigma': 0.99, 'nP': 211, 'nQ': 66, 'accept': 0.69, 'retest': 0.71, 'phone': 0.31, 'tries': 0},
    {'N': 1438, 'po': 0.082, 'qo': 0.495, 'mPo': 1.61, 'mQo': 6.53, 'mB': 2.41, 'sigma': 1.01, 'nP': 60, 'nQ': 58, 'accept': 0.56, 'retest': 0.77, 'phone': 0.3, 'tries': 14},
    {'N': 1073, 'po': 0.181, 'qo': 0.255, 'mPo': 1.93, 'mQo': 5.56, 'mB': 2.9, 'sigma': 0.92, 'nP': 77, 'nQ': 34, 'accept': 0.6, 'retest': 0.74, 'phone': 0.3, 'tries': 2},
    {'N': 2703, 'po': 0.068, 'qo': 0.134, 'mPo': 1.62, 'mQo': 3.04, 'mB': 2.43, 'sigma': 0.94, 'nP': 188, 'nQ': 79, 'accept': 0.6, 'retest': 0.65, 'phone': 0.18, 'tries': 0},
    {'N': 1683, 'po': 0.187, 'qo': 0.194, 'mPo': 1.45, 'mQo': 4.17, 'mB': 2.18, 'sigma': 1.0, 'nP': 112, 'nQ': 43, 'accept': 0.66, 'retest': 0.79, 'phone': 0.3, 'tries': 17},
    {'N': 2306, 'po': 0.121, 'qo': 0.418, 'mPo': 1.28, 'mQo': 5.18, 'mB': 1.91, 'sigma': 1.01, 'nP': 121, 'nQ': 83, 'accept': 0.65, 'retest': 0.63, 'phone': 0.21, 'tries': 5},
    {'N': 10833, 'po': 0.204, 'qo': 0.233, 'mPo': 1.26, 'mQo': 3.61, 'mB': 1.88, 'sigma': 0.94, 'nP': 689, 'nQ': 378, 'accept': 0.6, 'retest': 0.77, 'phone': 0.25, 'tries': 0},
    {'N': 1380, 'po': 0.173, 'qo': 0.27, 'mPo': 1.77, 'mQo': 5.1, 'mB': 2.66, 'sigma': 0.86, 'nP': 78, 'nQ': 44, 'accept': 0.62, 'retest': 0.77, 'phone': 0.2, 'tries': 16},
    {'N': 3469, 'po': 0.063, 'qo': 0.155, 'mPo': 1.41, 'mQo': 2.64, 'mB': 2.11, 'sigma': 0.93, 'nP': 227, 'nQ': 111, 'accept': 0.62, 'retest': 0.8, 'phone': 0.28, 'tries': 9},
    {'N': 3435, 'po': 0.09, 'qo': 0.094, 'mPo': 1.26, 'mQo': 2.36, 'mB': 1.89, 'sigma': 1.02, 'nP': 309, 'nQ': 140, 'accept': 0.68, 'retest': 0.72, 'phone': 0.19, 'tries': 4},
    {'N': 2631, 'po': 0.146, 'qo': 0.405, 'mPo': 1.21, 'mQo': 4.92, 'mB': 1.81, 'sigma': 0.96, 'nP': 111, 'nQ': 82, 'accept': 0.59, 'retest': 0.73, 'phone': 0.21, 'tries': 1},
    {'N': 839, 'po': 0.102, 'qo': 0.224, 'mPo': 1.51, 'mQo': 4.35, 'mB': 2.27, 'sigma': 0.92, 'nP': 60, 'nQ': 31, 'accept': 0.61, 'retest': 0.76, 'phone': 0.19, 'tries': 14},
    {'N': 4573, 'po': 0.208, 'qo': 0.221, 'mPo': 2.13, 'mQo': 6.11, 'mB': 3.19, 'sigma': 0.87, 'nP': 250, 'nQ': 154, 'accept': 0.71, 'retest': 0.62, 'phone': 0.26, 'tries': 0},
    {'N': 866, 'po': 0.192, 'qo': 0.185, 'mPo': 1.68, 'mQo': 4.83, 'mB': 2.52, 'sigma': 0.96, 'nP': 70, 'nQ': 26, 'accept': 0.6, 'retest': 0.79, 'phone': 0.27, 'tries': 2},
    {'N': 981, 'po': 0.169, 'qo': 0.28, 'mPo': 1.71, 'mQo': 4.92, 'mB': 2.57, 'sigma': 1.01, 'nP': 58, 'nQ': 30, 'accept': 0.67, 'retest': 0.8, 'phone': 0.18, 'tries': 1},
    {'N': 1411, 'po': 0.095, 'qo': 0.086, 'mPo': 2.14, 'mQo': 4.01, 'mB': 3.21, 'sigma': 0.98, 'nP': 119, 'nQ': 48, 'accept': 0.7, 'retest': 0.68, 'phone': 0.23, 'tries': 0},
]
