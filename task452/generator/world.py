"""task452 (architecture 2): the world every file is computed from.

A lowland forest emission reductions program in a Spanish-speaking tropical country reports its 2024-2025
emission reductions to a results-based climate fund. The deforested area of the reporting period is estimated
from 4,000 reference points interpreted on high-resolution imagery. The points were drawn in January 2026 by
stratified random sampling on the preliminary 2024-2025 change map; the final map, reprocessed in April 2026 with
radar and late-season imagery, removed most of the preliminary map's cloud-shadow false alarms and some real
clearings, and caught a few of the clearings the preliminary map had missed. Nothing in the pack names a country,
agency, fund or program that exists.
"""
import numpy as np

SEED = 452
SAMPLE_SEED = 54533         # the draw of 20 January 2026

PROGRAM = "Lowland Forest Emission Reductions Program"
FUND = "Rainforest Results Facility"
MINISTRY = "Ministry of Environment"
LAB = "University Remote Sensing Laboratory"
NFMS = "National Forest Monitoring System"
PEOPLE = {"head": "Lilia Solano", "maps": "César Verduzco", "reference": "Raquel Saavedra"}

# the program's twelve districts on the 2019 district layer (code, name, total area ha, forest on 1 January 2024 ha,
# true deforestation 2024-2025 ha, a cloudiness factor for the preliminary map's errors)
DISTRICTS = [
    ("01", "Caoba Alta", 1_120_000, 820_000, 6_200, 1.3),
    ("02", "Caoba Baja", 1_340_000, 560_000, 19_800, 1.0),
    ("03", "Cerro Azul", 760_000, 610_000, 2_900, 1.4),
    ("04", "El Encanto", 980_000, 450_000, 11_600, 0.9),
    ("05", "La Esperanza", 1_460_000, 690_000, 21_400, 1.1),
    ("06", "Las Palmas", 1_050_000, 380_000, 13_700, 0.8),
    ("07", "Llano Grande", 1_230_000, 290_000, 9_800, 0.7),
    ("08", "Montealto", 690_000, 560_000, 2_100, 1.5),
    ("09", "Puerto Viejo", 840_000, 330_000, 8_300, 1.0),
    ("10", "Río Verde", 1_150_000, 610_000, 16_900, 1.2),
    ("11", "Tres Ríos", 620_000, 410_000, 5_100, 1.3),
    ("12", "Arroyo Hondo", 560_000, 290_000, 3_500, 1.1),
]
DCODE = [d[0] for d in DISTRICTS]
DNAME = {d[0]: d[1] for d in DISTRICTS}
R = len(DISTRICTS)

# the six highland districts outside the accounting area (the change map covers the whole country)
HIGHLANDS = [("13", "Cumbre Alta", 1_380), ("14", "Valle Frío", 2_210), ("15", "Páramo Grande", 640),
             ("16", "San Isidro de la Sierra", 1_870), ("17", "Mesa Larga", 1_290), ("18", "Loma Verde", 2_050)]

# the 2025 district reform: new codes, and La Esperanza split into La Esperanza and Nueva Esperanza
D2025 = {"01": "LT-01", "02": "LT-02", "03": "LT-03", "04": "LT-04", "05": "LT-05", "06": "LT-07", "07": "LT-08",
         "08": "LT-09", "09": "LT-10", "10": "LT-11", "11": "LT-12", "12": "LT-13",
         "13": "SR-01", "14": "SR-02", "15": "SR-03", "16": "SR-04", "17": "SR-05", "18": "SR-06"}
SPLIT_NEW = ("LT-06", "Nueva Esperanza")      # carved out of 2019 district 05 La Esperanza
SPLIT_SHARE = 0.38                             # Nueva Esperanza's share of La Esperanza's change

# preliminary map (January 2026): the share of each true class's area in each preliminary class; the cloudiness
# factor scales the false alarms and the omissions
PRELIM_FALSE_F = 0.0060        # stable forest mapped as deforestation (cloud shadow, leaf-off), at cloudiness 1
PRELIM_FALSE_N = 0.0040        # non-forest mapped as deforestation (burnt pasture, harvests)
PRELIM_OMIT = 0.39             # deforestation the preliminary map left in stable forest, at cloudiness 1
PRELIM_OMIT_N = 0.05           # deforestation mapped as non-forest
PRELIM_N_AS_F = 0.010          # non-forest mapped as stable forest

# final map (April 2026), given each pixel's true class and preliminary class
FINAL = {("D", "PD"): {"FD": .88, "FF": .11, "FN": .01}, ("D", "PF"): {"FD": .04, "FF": .94, "FN": .02},
         ("D", "PN"): {"FD": .10, "FN": .90},
         ("F", "PD"): {"FD": .12, "FF": .86, "FN": .02}, ("F", "PF"): {"FD": .0002, "FF": .9996, "FN": .0002},
         ("F", "PN"): {"FF": .30, "FN": .70},
         ("N", "PD"): {"FD": .15, "FF": .05, "FN": .80}, ("N", "PF"): {"FF": .70, "FN": .30},
         ("N", "PN"): {"FD": .0003, "FF": .0007, "FN": .9990}}

# the reference sample: stratified random sampling on the preliminary map's three classes
STRATA = [("S1", "PD", "deforestation 2024-2025"), ("S2", "PF", "stable forest"), ("S3", "PN", "non-forest")]
N_SAMPLE = {"S1": 400, "S2": 2400, "S3": 1200}
QC_SHARE = 0.20

# the payment agreement and the reference level
RL_HA_YEAR = 89_950.0          # reference level, deforestation 2015-2022 (ha a year): 719,600 ha over 8 years
EF = 497.0                     # emission factor, tCO2e per hectare deforested
BUFFER = 0.18                  # buffer set aside against reversals
PRICE = 5.00                   # USD per tonne of CO2e offered
YEARS = 2
AREA_ROUND = 100               # the area of deforestation is reported to the nearest hundred hectares

PIXEL_HA = 0.09                # a 30 m pixel
EXTRACT = "2026-05-22"
REPORT_DUE = "2026-06-30"

# the interpreters' legend (main campaign) and the national forest definition
LEGEND = {1: "dense forest", 2: "open forest", 3: "woodland and shrub", 4: "tree plantation", 5: "cropland",
          6: "pasture", 7: "settlement and bare soil", 8: "water and wetland"}
CANOPY = {"A": "under 10 per cent", "B": "10 to 30 per cent", "C": "30 to 60 per cent", "D": "over 60 per cent"}
FOREST_CODES = (1, 2)
