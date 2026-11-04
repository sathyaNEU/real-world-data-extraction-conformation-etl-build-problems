"""task476 architecture 4: the fixed world. Cinder Fork Timber Company's stands, permanent plots and species, the
2006 to 2021 inventory cycles held in the company's CFI database, the 2026 contract remeasurement, the 2024
underburns, the beetle stands and the 2025 lightning fire. Every figure the pack carries is drawn here or in sim.py
from fixed seeds, so two builds are byte-identical."""
import numpy as np

SEED = 476_04
COMPANY = "Cinder Fork Timber Company"
FARM = "Cinder Fork Tree Farm"
CONTRACTOR = "Tolan Ridge Forestry"
MANAGER = "Tamara Larson"
FORESTER = "Brandon Freeman"
CHAIR = "Nicholas Wolf"
BURN_BOSS = "J. Ochoa"
PLOT_AC = 0.2
PLOT_R = 52.7
BA_K = 0.005454
LINE = 0.15
SAW_MIN = 11.0
POLICY_NO = "7.4"
CYCLES = [2006, 2011, 2016, 2021]
NEW_TAG0 = 70001

# species: alpha code (company collector), FIA code (contract collector), common name, scientific name, group
SPECIES = [("PP", 122, "ponderosa pine", "Pinus ponderosa", "conifer"),
           ("SP", 117, "sugar pine", "Pinus lambertiana", "conifer"),
           ("WF", 15, "white fir", "Abies concolor", "conifer"),
           ("DF", 202, "Douglas-fir", "Pseudotsuga menziesii", "conifer"),
           ("IC", 81, "incense-cedar", "Calocedrus decurrens", "conifer"),
           ("BO", 818, "California black oak", "Quercus kelloggii", "hardwood")]
PINES = (0, 1)
HARDWOOD = (5,)

# stands: (stand, acres, kind); kinds: burn (fall 2024 underburn), beetle, wild (2025 lightning fire), plain
STANDS = [("CF-101", 212, "plain"), ("CF-104", 168, "burn"), ("CF-107", 254, "plain"), ("CF-112", 131, "beetle"),
          ("CF-115", 296, "plain"), ("CF-118", 187, "burn"), ("CF-121", 143, "plain"), ("CF-126", 228, "plain"),
          ("CF-129", 176, "burn"), ("CF-133", 119, "plain"), ("CF-138", 263, "wild"), ("CF-141", 154, "plain"),
          ("CF-144", 201, "burn"), ("CF-149", 238, "plain"), ("CF-152", 172, "beetle"), ("CF-156", 147, "plain"),
          ("CF-160", 219, "burn"), ("CF-163", 136, "plain"), ("CF-167", 245, "plain"), ("CF-170", 158, "plain"),
          ("CF-174", 189, "plain"), ("CF-178", 207, "plain")]
BURN_DATES = {"CF-104": "2024-10-22", "CF-118": "2024-10-24", "CF-129": "2024-11-05", "CF-144": "2024-11-07",
              "CF-160": "2024-11-12"}
WILDFIRE = ("CF-138", "2025-08-14", "Juniper Saddle Fire")
THINNED_2012 = ("CF-107", "CF-126", "CF-167")
ROAD_2023 = ("CF-115", "CF-170")
ACQUIRED = ("CF-174", "CF-178")          # bought in 2010; plots installed 2011
SMOKE_DAYS = ("2026-07-20", "2026-07-21", "2026-07-22", "2026-07-23", "2026-07-24")

FILES = {
    "db": "inventory/cfi_database.sqlite",
    "t2026": "inventory/trf_cfi_remeasurement_2026.csv",
    "revisit": "inventory/trf_height_revisit_2026-09.csv",
    "register": "inventory/plot_register.xlsx",
    "species": "inventory/species_codes.csv",
    "manual": "inventory/cfi_field_manual_rev2026.pdf",
    "stands": "gis/stand_table_2026.csv",
    "policy": "policy/salvage_marking_policy_2026.pdf",
    "burns": "operations/prescribed_burn_reports_2024.pdf",
    "fire": "operations/juniper_saddle_fire_report_2025.pdf",
    "ads": "operations/aerial_detection_survey_2025.csv",
    "logs": "markets/delivered_log_prices_2026q3.csv",
}

# Scribner Decimal C (tens of board feet) by 2-inch DBH class and 16-foot logs, the company's table
VOL_DBH = list(range(12, 52, 2))
VOL_LOGS = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]


def scribner_c(dbh_class, logs):
    v = 0.0118 * (dbh_class ** 2.35) * (logs ** 0.92) - 0.9 * logs
    return max(1, int(round(v)))


def stand_params():
    rng = np.random.default_rng(SEED)
    out = {}
    # stand centroids on the farm, laid out as the stand numbers run across the ownership
    for i, (sid, ac, kind) in enumerate(STANDS):
        n_plots = int(np.clip(round(ac / 15 + rng.normal(0, 1.4)), 8, 19))
        ftype = "pine" if kind == "beetle" or rng.random() < 0.4 else "mixed"
        cx = 676200 + (i % 6) * 1450 + rng.normal(0, 240)
        cy = 4418800 - (i // 6) * 1300 + rng.normal(0, 220)
        out[sid] = dict(sid=sid, acres=ac, kind=kind, n_plots=n_plots, ftype=ftype, cx=cx, cy=cy, idx=i,
                        site=int(rng.choice([2, 3, 3, 4])))
    return out


STAND = stand_params()
SIDS = [s for s, _, _ in STANDS]


def neighbours(sid):
    c = STAND[sid]
    d = sorted((((STAND[o]["cx"] - c["cx"]) ** 2 + (STAND[o]["cy"] - c["cy"]) ** 2) ** 0.5, o) for o in SIDS if o != sid)
    return [o for _, o in d[:3]]
