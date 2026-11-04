"""task489: the world's fixed facts. Larchmere Resources Ltd's Deep Basin well sites, their wells and wellsite
separators, the pneumatic devices on them, the makers' ratings, the reporting standard's constants, the clocks
and the file names. Every figure the pack and the goldens carry is computed forward from these."""
import datetime as dt
import math
from zoneinfo import ZoneInfo

SEED = 4891
YEAR = 2026
TZ = ZoneInfo("America/Edmonton")
UTC = dt.timezone.utc
PROD_DAY_HOUR = 8                       # a production day runs 08:00 to 08:00 local (MRS-03 3.2)
AS_OF = dt.date(2027, 1, 25)            # the folder as the methane reduction lead assembled it
STAMP = (2027, 1, 25, 9, 12, 0)

ORG = "Larchmere Resources Ltd."
ORG_SHORT = "Larchmere"
CONTRACTOR = "Sheldrake Field Measurement Ltd."
MAKERS = {"Corrigan": "Corrigan Controls", "Aldous": "Aldous Valve and Instrument", "Brannick": "Brannick Instrument"}
PEOPLE = {"lead": "Stacy Frost", "contractor": "Kimberly Hinton", "accounting": "Valerie Sanders",
          "vp": "Gregory Cook"}
TITLES = {"lead": "Methane Reduction Lead", "contractor": "Measurement Lead", "accounting": "Production Accounting Supervisor",
          "vp": "Vice President, Operations"}

# ----------------------------------------------------------------------------------------- reporting constants
SCF_TO_M3 = 0.02826                     # MRS-03 4.3: one standard cubic foot (60 F, 14.696 psia) in m3 at 15 C, 101.325 kPa
CH4_KG_PER_M3 = 0.678                   # MRS-03 4.3: methane at 15 C and 101.325 kPa
LINE_T = 0.5                            # 2027 plan section 3: the conversion line, tonnes of methane a site's
                                        # intermittent-vent controllers vented in 2026
SUPPLY_KPA = 241                        # every site's instrument supply regulator (35 psig)

# ----------------------------------------------------------------------------------------- makers' ratings
# level controllers (snap acting, intermittent vent): supply gas per dump cycle, scf at 35 psig supply
LC_MODELS = {
    "CL-200": {"maker": "Corrigan", "scf_per_cycle": 0.62, "name": "CL-200 snap-acting liquid level controller"},
    "SV-40": {"maker": "Aldous", "scf_per_cycle": 0.88, "name": "SV-40 level controller and dump valve package"},
    "DLC-3": {"maker": "Brannick", "scf_per_cycle": 0.47, "name": "DLC-3 displacer level controller"},
}
# continuous-bleed controllers: steady bleed at 35 psig supply, scf per hour
BLEED_MODELS = {
    "CP-10": {"maker": "Corrigan", "scf_per_h": 0.35, "name": "CP-10 throttling pressure controller", "kind": "PC"},
    "PC-60": {"maker": "Aldous", "scf_per_h": 0.52, "name": "PC-60 low-bleed pressure controller", "kind": "PC"},
    "TC-5": {"maker": "Brannick", "scf_per_h": 0.28, "name": "TC-5 bath temperature controller", "kind": "TC"},
}


def band_m3(bore_in, span_in):
    """The liquid between a vertical vessel's controller settings: the bore's area times the span."""
    r = bore_in * 0.0254 / 2.0
    return math.pi * r * r * span_in * 0.0254


def kg_per_cycle(model, x_ch4):
    return LC_MODELS[model]["scf_per_cycle"] * SCF_TO_M3 * x_ch4 * CH4_KG_PER_M3


# ----------------------------------------------------------------------------------------- the sites
# Each separator: (group, LC model, bore in, span in, target kg, slug ratio, automated)
#   group F  flowing well, liquid arrives continuously;            target kg is the golden
#   group PB plunger well, slugs at or above the band (ratio>=1.5); target kg is the golden (one dump per arrival)
#   group PS plunger well, slugs far below the band (ratio<=0.065);  target kg is what one dump per arrival would vent
# Bleed devices: (tag, model)
SITES = [
    # code, area, surface LSD, x_CH4 2026, separators, bleed devices
    ("K0309", "Kakwa", "03-09-063-05W6", 0.861, [("F", "CL-200", 36, 10, 952, None, False)],
     [("TC-1", "TC-5"), ("PC-1", "CP-10")]),
    ("K1416", "Kakwa", "14-16-063-05W6", 0.848, [("F", "DLC-3", 30, 8, 404, None, False),
                                                 ("F", "CL-200", 24, 6, 349, None, False)],
     [("TC-1", "TC-5")]),
    ("K1122", "Kakwa", "11-22-063-05W6", 0.872, [("F", "SV-40", 42, 12, 878, None, True)],
     [("TC-1", "TC-5"), ("PC-1", "PC-60")]),
    ("K0627", "Kakwa", "06-27-063-05W6", 0.855, [("F", "CL-200", 36, 10, 527, None, True),
                                                 ("F", "DLC-3", 24, 6, 211, None, False)],
     [("PC-1", "CP-10")]),
    ("K0702", "Elmworth", "07-02-070-11W6", 0.842, [("F", "CL-200", 30, 8, 583, None, False),
                                                 ("PB", "DLC-3", 42, 4, 61, 3.2, False)],
     [("TC-1", "TC-5"), ("PC-1", "CP-10")]),
    ("K1011", "Elmworth", "10-11-070-09W6", 0.866, [("F", "SV-40", 36, 8, 661.4, None, False),
                                                 ("PB", "CL-200", 24, 8, 52, 2.4, False)],
     [("PC-1", "PC-60")]),
    ("K0114", "Kakwa", "01-14-064-04W6", 0.833, [("F", "DLC-3", 42, 10, 618, None, False),
                                                 ("PS", "SV-40", 42, 12, 86, 0.045, False)],
     [("TC-1", "TC-5")]),
    ("K1623", "Kakwa", "16-23-064-04W6", 0.879, [("F", "SV-40", 48, 12, 703, None, True),
                                                 ("PS", "CL-200", 42, 10, 71, 0.040, False),
                                                 ("PS", "DLC-3", 48, 8, 64, 0.035, False)],
     [("TC-1", "TC-5"), ("PC-1", "CP-10"), ("PC-2", "PC-60")]),
    ("E0503", "Elmworth", "05-03-069-10W6", 0.814, [("F", "DLC-3", 24, 8, 265, None, False),
                                                    ("PB", "SV-40", 24, 6, 71, 2.6, False),
                                                    ("PB", "CL-200", 20, 6, 62, 3.0, False)],
     [("TC-1", "TC-5"), ("PC-1", "PC-60"), ("PC-2", "CP-10")]),
    ("E0810", "Kakwa", "08-10-064-06W6", 0.826, [("PB", "CL-200", 24, 6, 81, 2.9, False),
                                                    ("PB", "SV-40", 36, 3, 72, 3.3, False),
                                                    ("PB", "DLC-3", 24, 8, 88, 2.6, False)],
     [("PC-1", "CP-10")]),
    ("E1215", "Elmworth", "12-15-069-10W6", 0.808, [("F", "CL-200", 30, 6, 291, None, False),
                                                    ("PB", "SV-40", 30, 5, 79, 3.5, False)],
     [("TC-1", "TC-5")]),
    ("E1322", "Kakwa", "13-22-062-05W6", 0.837, [("F", "DLC-3", 30, 8, 302.0, None, False),
                                                    ("PS", "SV-40", 48, 14, 172, 0.030, False),
                                                    ("PS", "SV-40", 42, 12, 163, 0.040, False)],
     [("TC-1", "TC-5"), ("PC-1", "CP-10")]),
    ("E0427", "Elmworth", "04-27-069-09W6", 0.851, [("PS", "SV-40", 48, 14, 216, 0.025, False),
                                                    ("PS", "SV-40", 48, 12, 209, 0.030, False),
                                                    ("PS", "CL-200", 48, 6, 201, 0.035, False)],
     [("PC-1", "PC-60")]),
    ("E0934", "Elmworth", "09-34-069-09W6", 0.829, [("F", "CL-200", 36, 8, 352, None, False),
                                                    ("PS", "SV-40", 48, 14, 268, 0.030, False)],
     [("TC-1", "TC-5"), ("PC-1", "CP-10")]),
    ("E0205", "Elmworth", "02-05-070-10W6", 0.894, [("F", "DLC-3", 24, 6, 121, None, False)],
     [("PC-1", "CP-10")]),
    ("E1508", "Elmworth", "15-08-070-10W6", 0.887, [("F", "CL-200", 30, 8, 185, None, False),
                                                    ("F", "DLC-3", 24, 6, 92, None, False)],
     [("TC-1", "TC-5")]),
    ("E0617", "Elmworth", "06-17-070-10W6", 0.902, [("F", "SV-40", 36, 10, 318, None, True)],
     [("TC-1", "TC-5"), ("PC-1", "PC-60")]),
    ("E1120", "Elmworth", "11-20-070-11W6", 0.881, [("F", "CL-200", 24, 6, 223, None, False)],
     [("PC-1", "CP-10")]),
    ("E0329", "Elmworth", "03-29-068-11W6", 0.819, [("PB", "CL-200", 20, 10, 59, 2.8, False)],
     [("TC-1", "TC-5")]),
    ("E1032", "Elmworth", "10-32-068-11W6", 0.823, [("PB", "DLC-3", 36, 4, 56, 3.1, False),
                                                    ("PB", "CL-200", 24, 8, 44, 2.0, False)],
     [("TC-1", "TC-5"), ("PC-1", "CP-10")]),
    ("K0835", "Kakwa", "08-35-062-06W6", 0.858, [("PS", "SV-40", 42, 12, 81, 0.050, False)],
     [("PC-1", "CP-10")]),
    ("K1236", "Kakwa", "12-36-062-06W6", 0.846, [("PS", "DLC-3", 42, 12, 96, 0.050, False),
                                                 ("PS", "SV-40", 30, 14, 117.5, 0.050, False)],
     [("TC-1", "TC-5")]),
    ("K0501", "Kakwa", "05-01-063-06W6", 0.869, [("F", "CL-200", 30, 8, 204, None, True),
                                                 ("F", "DLC-3", 24, 6, 149, None, False)],
     [("TC-1", "TC-5"), ("PC-1", "PC-60")]),
    ("K1312", "Kakwa", "13-12-063-06W6", 0.874, [("F", "DLC-3", 24, 6, 101, None, False),
                                                 ("F", "CL-200", 20, 4, 79, None, False),
                                                 ("F", "SV-40", 24, 6, 122, None, False)],
     [("PC-1", "CP-10")]),
    ("E0718", "Elmworth", "07-18-068-10W6", 0.831, [("F", "CL-200", 24, 6, 155, None, False),
                                                    ("PB", "DLC-3", 24, 6, 49, 2.8, False),
                                                    ("PS", "CL-200", 36, 14, 83, 0.050, False)],
     [("TC-1", "TC-5")]),
    ("E1424", "Elmworth", "14-24-068-10W6", 0.897, [("F", "SV-40", 36, 8, 412, None, False)],
     [("TC-1", "TC-5"), ("PC-1", "CP-10")]),
]

# Plunger controller units moved in 2026: a receiving well's controller failed and the unit from a lower-rate well
# went on it, the donor shut in until a new unit arrived; the SCADA host kept the unit's old well label until its
# tag mapping was corrected. (donor site, idx), (receiver site, idx), moved, label corrected, donor back on
MOVES = [(("E0427", 0), ("E0427", 2), (2026, 6, 3, 10, 5), (2026, 6, 14, 9, 0), (2026, 6, 20, 13, 10)),
         (("K0835", 0), ("K1236", 1), (2026, 7, 8, 11, 30), (2026, 7, 21, 15, 0), (2026, 7, 25, 10, 40)),
         (("E1322", 2), ("E0934", 1), (2026, 8, 18, 9, 15), (2026, 8, 26, 16, 40), (2026, 9, 2, 12, 0)),
         (("K1623", 2), ("K0114", 1), (2026, 9, 29, 14, 0), (2026, 10, 13, 10, 20), (2026, 10, 16, 15, 30))]
# Radio outages after which the host loaded the controller's buffer and the overnight backfill loaded it again
OUTAGES = [(("K1236", 0), (2026, 2, 11, 6, 0), 61), (("E0718", 2), (2026, 4, 27, 19, 0), 38),
           (("K1623", 1), (2026, 11, 20, 3, 0), 74), (("E1322", 1), (2026, 12, 2, 13, 0), 49),
           (("E0427", 1), (2026, 7, 30, 22, 0), 30)]
# Pads whose two pressure controllers were renumbered in the register after a re-pipe (the survey's field tags
# predate it): site, the date the re-pipe was completed
RETAGGED = [("K1623", (2026, 7, 16)), ("E0503", (2026, 7, 29))]
# Line heaters taken off one pad and set on another, their bath controllers with them:
# (from site, tag, out of service), (to site, new tag, in service)
RELOCATED = [(("E0718", "TC-1", (2026, 6, 23, 15, 40)), ("K1236", "TC-2", (2026, 7, 14, 13, 5))),
             (("K1416", "TC-1", (2026, 9, 9, 11, 10)), ("E1215", "TC-2", (2026, 10, 5, 10, 45)))]
# Plunger controllers count every motor valve opening; an opening the controller closes again on its line pressure
# interlock is counted and never sent to the host. Share of openings aborted, by controller.
ABORT_SHARE = (0.012, 0.034)

# Surveys done in 2026 by the contractor: which level controllers (site code, separator index) were tested
CAMPAIGN_LCS = [("K0309", 0), ("K1416", 0), ("K1122", 0), ("K0627", 0), ("K1011", 0), ("K1623", 0),
                ("E0503", 0), ("E1508", 0), ("E0617", 0), ("K0501", 1), ("K1312", 2), ("E1424", 0)]

FILES = {
    "cycles": "plunger_cycles_2026.csv",
    "prod": "daily_well_volumes_2026.csv",
    "ppa": "volumetric_adjustments_2026.csv",
    "runs": "allocation_runs_2026.csv",
    "register": "deep_basin_equipment_register.xlsx",
    "analyses": "gas_analyses_2025_2026.csv",
    "counters": "scada_dump_counters_2026.csv",
    "orders": "deep_basin_work_orders_2026.csv",
    "standard": "MRS-03_methane_measurement_and_reporting_standard_rev4.pdf",
    "plan": "methane_reduction_plan_2027.docx",
    "template": "MRS-03_annex_B_source_inventory_template.xlsx",
    "survey": "sheldrake_pneumatic_survey_2026.pdf",
    "sheet_corrigan": "corrigan_CL-200_CP-10_data_sheet.pdf",
    "sheet_aldous": "aldous_SV-40_PC-60_data_sheet.pdf",
    "sheet_brannick": "brannick_DLC-3_TC-5_data_sheet.pdf",
    "sheet_trellick": "trellick_PCX-300_plunger_controller_spec.pdf",
    "ogi": "ogi_leak_survey_2026.csv",
    "tanks": "tank_vent_measurements_2026.xlsx",
}
DISTRACTORS = ["ogi_leak_survey_2026.csv", "tank_vent_measurements_2026.xlsx", "volumetric_adjustments_2026.csv",
               "allocation_runs_2026.csv"]
DELIVERABLES = ["larchmere_source_inventory_2026.xlsx", "controller_conversion_2027.pptx"]


def production_day_bounds_utc(day):
    """[start, end) of a production day in UTC."""
    s = dt.datetime(day.year, day.month, day.day, PROD_DAY_HOUR, tzinfo=TZ)
    e = s.date() + dt.timedelta(days=1)
    e = dt.datetime(e.year, e.month, e.day, PROD_DAY_HOUR, tzinfo=TZ)
    return s.astimezone(UTC), e.astimezone(UTC)


DAYS = [dt.date(YEAR, 1, 1) + dt.timedelta(days=i) for i in range(365)]
WINDOW_START_UTC = production_day_bounds_utc(DAYS[0])[0]
WINDOW_END_UTC = production_day_bounds_utc(DAYS[-1])[1]
