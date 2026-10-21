"""The world's fixed parameters: each group's breast cancer risk by 70 for a woman who carries it (net of other
causes of death) and its number of families, the population's age-specific incidence, the testing pathway's rates,
and the seed the search chose."""
import numpy as np

# first primary breast cancer, women, per person-year, by 5-year band from age 0 (the system's own registry rates)
POP = np.array([0, 0, 0, 0, 1.5, 8, 25, 55, 120, 190, 220, 255, 320, 390, 430, 440, 420, 380, 380, 380]) / 1e5

# group code: (risk by 70 for a carrier, families)
TRUTH = {
    "PALB2-PTV": (0.40, 450), "PALB2-MIS": (0.42, 110), "ATM-PTV": (0.17, 450), "ATM-MIS": (0.18, 130),
    "CHEK2-PTV": (0.235, 700), "CHEK2-MIS": (0.10, 500), "BARD1-PTV": (0.15, 160), "RAD51C-PTV": (0.14, 150),
    "RAD51D-PTV": (0.14, 120), "BRIP1-PTV": (0.09, 200),
}
RR_DECLINE = 0.015          # a carrier's relative risk falls with age

# cascade testing: an affected relative and an unaffected relative's chance of a test after the family's letter,
# counsellor-led at intake (direct) or through the proband after a late result (proband-mediated)
A_DIRECT, U_DIRECT = 0.85, 0.65
A_LATE, U_LATE = 0.60, 0.12
TAU_AFFECTED, TAU_UNAFFECTED = 0.3, 1.0     # years from the letter to the test
OWN_CARE = 0.90                              # a patient diagnosed with breast cancer has a panel at diagnosis
PATIENT = {"first": 0.42, "second": 0.15, "partner": 0.50}

SEED = 5187
CLINICAL_SEED = 271301      # the asks' clinical records draw from their own stream
