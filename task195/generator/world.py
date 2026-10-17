"""Genomkjernen: the fixed world behind the June 2027 contamination screen change."""
import datetime as dt

SEED = 195
AS_OF = dt.date(2027, 6, 21)              # the validation extract date
REVIEW = dt.date(2027, 6, 30)             # the laboratory quality review sits
Q_FROM = dt.date(2027, 7, 1)              # the quarter the change would take effect
RUN_FROM = dt.date(2027, 3, 1)            # the parallel run's receipt window
RUN_TO = dt.date(2027, 5, 31)
HIST_FROM = dt.date(2026, 2, 15)          # the quality-control warehouse extract
HIST_TO = dt.date(2027, 2, 28)
BASE_FROM = dt.date(2026, 3, 1)           # the twelve reporting months the baseline covers
BASE_TO = dt.date(2027, 2, 28)

LAB = "Genomkjernen"
INSTITUTE = "Nordfjell forskningsinstitutt"
PARTNER = "Bergsvik Analyse AS"
CITY = "Nordfjell"
PEOPLE = {"lead": "Laila Johannessen",    # screening lead, requests the validation
          "quality": "Dag Rasmussen"}     # quality manager, approves KVAL-07

PIPELINE = "GKJ-PIPE v3.4"
SCREEN_IN_SERVICE = "HETX"                # per specimen heterozygosity-excess screen
CANDIDATE = "MF"                          # mixture-fraction screen from the v3.4 re-run
CUTOFFS = [0.050, 0.030, 0.020, 0.015, 0.010]

# the comparison, as the parallel run's records make it
N_MIXED = 393                             # confirmed contamination events
N_CONCORDANT = 5446                       # panel-clean specimens in the comparison
INC_DETECT = 292                          # events the screen in service flags
INC_FALSE = 91                            # panel-clean specimens it flags
# per cutoff, in CUTOFFS order
ONLY_SERVICE = [12, 7, 6, 5, 4]           # events the screen in service flags and the candidate does not
ONLY_CANDIDATE = [14, 23, 24, 32, 38]     # events the candidate flags and the screen in service does not
CAND_FALSE = [61, 74, 80, 85, 104]        # panel-clean specimens the candidate flags

# specimens received in the window that the comparison does not hold
OUT_OF_SCOPE = 579                        # contract agreement receipts, outside the re-run's project list
NO_ACCEPTED_READ = 38                     # every read voided on a failed instrument control
NO_ESTIMATE = 176                         # archived read sets below the pipeline's depth floor
PENDING_VERDICT = 194                     # panel verdict not reported by the extract date
INCONCLUSIVE = 35                         # panel verdict INCONCLUSIVE
TWO_READ_SETS = 139                       # specimens with a depth top-up library
REPLATED = 73                             # specimens re-plated after a failed batch control

PROJECTS = [("NHU3", "Nordfjell helseundersokelse 3", 0.41),
            ("BARN2", "Barnekohort 2", 0.17),
            ("KARDIA", "Kardia Nordfjell", 0.19),
            ("OSTEO", "Osteo-N", 0.13),
            ("SEPSIS", "Sepsisregister Nordfjell", 0.10)]
CONTRACT = [("KT-ALPHA", "AVT-2026-114"), ("KT-BORG", "AVT-2027-031")]
EXTRACTION = ["magnetic bead", "silica column", "salting out"]
INSTRUMENTS = ["GSQ-A", "GSQ-B"]
DEPTH_FLOOR = 20                          # the pipeline's minimum mean depth
PANEL_MARKERS = 96
PANEL_LOD = 0.005                         # the panel calls MIXED above this second-contributor share

# the laboratory is closed on these days, so nothing is received on them
HOLIDAYS = {dt.date(2026, 4, 2), dt.date(2026, 4, 3), dt.date(2026, 4, 6), dt.date(2026, 5, 1),
            dt.date(2026, 5, 14), dt.date(2026, 5, 25), dt.date(2026, 12, 24), dt.date(2026, 12, 25),
            dt.date(2027, 1, 1), dt.date(2027, 3, 25), dt.date(2027, 3, 26), dt.date(2027, 3, 29),
            dt.date(2027, 5, 6), dt.date(2027, 5, 17)}
# receipts by weekday: the courier runs are heaviest early in the week
DAY_WEIGHT = [1.12, 1.07, 1.01, 0.95, 0.85]

HIST_ROWS = 31200                         # rows in the warehouse extract
REVIEWED_SHARE = 0.031                    # specimens whose call the duty bioinformatician reviewed

REACCESSIONED = 214        # specimens re-accessioned for a repeat panel, typed under a second accession
RERELEASED = 0             # set from the warehouse build: results released a second time after a correction

DILUTION = [("L1", "0.4 %", 0.0041), ("L2", "1.6 %", 0.0163), ("L3", "6.4 %", 0.0629)]
DILUTION_REPLICATES = 9
# the series ran out of stock part way through, so the second half of every level's replicates was
# prepared from a fresh stock dilution with its own gravimetric fraction
DILUTION_SECOND_PREP = 0.963

FILES = {
    "qc_a": "qc_screen_calls_gsqa_2027-03_2027-05.csv",
    "qc_b": "qc_screen_calls_gsqb_2027-03_2027-05.csv",
    "mf": "mixture_fraction_rerun_v34.csv",
    "panel": "identity_panel_register_2027.csv",
    "weekly": "identity_panel_weekly_reports_2027.pdf",
    "history": "qc_screen_history_2026-02-15_2027-02-28.csv",
    "volumes": "release_volumes_monthly_2026-03_2027-02.csv",
    "dilution": "dilution_panel_2027q1.xlsx",
    "crosswalk": "specimen_request_crosswalk.tsv",
    "protocol": "method_validation_protocol_kval07.pdf",
    "modelcard": "mixture_estimator_model_card_v34.pdf",
    "dictionary": "validation_extract_dictionary.csv",
    "config": "rerun_pipeline_config_v34.json",
    "manifest": "export_manifest.csv",
    "runlog": "lims_run_log_2027-03_2027-05.csv",
    "amendments": "release_amendments_2026-03_2027-05.csv",
    "costs": "assay_unit_costs_2027.csv",
    "platform": "extraction_platform_validation_2025.pdf",
    "plates": "plate_layout_map_2027q2.csv",
}
DISTRACTORS = ["runlog", "costs", "platform", "plates"]

# the twelve reporting months' flag propensity in the warehouse extract, as the screen in service
# ran: higher through the winter wave, when intake is heaviest and extraction is rushed
HIST_FLAG_RATE = {"2026-03": 0.0163, "2026-04": 0.0151, "2026-05": 0.0144, "2026-06": 0.0138,
                  "2026-07": 0.0129, "2026-08": 0.0147, "2026-09": 0.0172, "2026-10": 0.0186,
                  "2026-11": 0.0191, "2026-12": 0.0178, "2027-01": 0.0203, "2027-02": 0.0169}
DILUTION_RECOVERY = {"L1": 0.861, "L2": 0.948, "L3": 0.991}
