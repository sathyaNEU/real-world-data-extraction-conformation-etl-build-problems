"""Constants for task274: the Merrivane Health District's 2025 Health and Nutrition Examination Survey and the counties
where the district's 2027 vitamin D programme opens first. Every name, date and parameter the world, the records, the
documents and the analysis share lives here."""
import datetime as dt

SEED = 893
YEAR = 2025

DISTRICT = "Merrivane Health District"
DISTRICT_SHORT = "Merrivane"
CENTER = "Center for Health Statistics"
SURVEY = "Merrivane Health and Nutrition Examination Survey"
SURVEY_SHORT = "MHNES"
LAB = "Merrivane Regional Medical Center, Department of Laboratory Medicine"
LAB_SHORT = "MRMC Laboratory Medicine"
PROVIDER = "Brennick Reference Measurement Program"
MAKER = "Varnholt Diagnostics"
ASSAY = "25-OH Vitamin D Total"

REQUESTER = "Tanya Greene"          # chief statistician, Center for Health Statistics
LAB_DIRECTOR = "Bernard Weaver"
QUALITY = "Kaylee Lyons"            # the laboratory's quality manager
FIELD_LEAD = "Kathryn Serrano"      # the survey's field operations lead
HEALTH_OFFICER = "Anne Harrington"  # district health officer

# the eight counties, in the order the mobile examination centre (MEC) reached them in 2025
COUNTIES = [("01", "Wexmoor"), ("02", "Corvale"), ("03", "Lassiter"), ("04", "Ulverne"),
            ("05", "Vellance"), ("06", "Quennel"), ("07", "Yarrowmere"), ("08", "Inskeep")]
CNAME = dict(COUNTIES)
STANDS = [(dt.date(2025, 1, 6), dt.date(2025, 2, 12)), (dt.date(2025, 2, 18), dt.date(2025, 3, 27)),
          (dt.date(2025, 4, 1), dt.date(2025, 5, 8)), (dt.date(2025, 5, 13), dt.date(2025, 6, 19)),
          (dt.date(2025, 6, 24), dt.date(2025, 7, 31)), (dt.date(2025, 8, 5), dt.date(2025, 9, 11)),
          (dt.date(2025, 9, 16), dt.date(2025, 10, 23)), (dt.date(2025, 10, 28), dt.date(2025, 12, 4))]
# adults aged 20 and over (2020 census base carried to 1 July 2025), and the examined sample each stand aimed at
ADULTS = [61840, 118460, 44220, 87310, 152670, 39880, 73150, 56930]
EXAM_TARGET = [640, 700, 610, 660, 720, 599, 650, 630]
HOLIDAYS = {dt.date(2025, 1, 1), dt.date(2025, 1, 20), dt.date(2025, 2, 17), dt.date(2025, 5, 26),
            dt.date(2025, 6, 19), dt.date(2025, 7, 4), dt.date(2025, 9, 1), dt.date(2025, 11, 11),
            dt.date(2025, 11, 27), dt.date(2025, 11, 28), dt.date(2025, 12, 25)}

# the laboratory: two analyzers of one model, the results system's codes and the instruments' serial numbers
ANALYZERS = [("IA1", "VHD-82-21047"), ("IA2", "VHD-82-22318")]
# reagent lots: (lot number, loaded on IA1, loaded on IA2, bias against the reference procedure)
REAGENT_LOTS = [("41207", dt.date(2024, 12, 16), dt.date(2024, 12, 17), 0.17),
                ("41538", dt.date(2025, 2, 24), dt.date(2025, 2, 25), 0.19),
                ("41906", dt.date(2025, 4, 28), dt.date(2025, 4, 29), 0.21),
                ("42317", dt.date(2025, 7, 7), dt.date(2025, 7, 8), 0.10),
                ("42680", dt.date(2025, 8, 25), dt.date(2025, 8, 26), 0.12),
                ("43012", dt.date(2025, 10, 6), dt.date(2025, 10, 7), 0.13)]
RESTANDARDISED_FROM = "42317"
# calibrator lots: (lot number, first used on IA1, first used on IA2)
CAL_LOTS = [("C24117", dt.date(2024, 11, 18), dt.date(2024, 11, 18)),
            ("C25032", dt.date(2025, 4, 7), dt.date(2025, 4, 8)),
            ("C25071", dt.date(2025, 7, 21), dt.date(2025, 7, 21)),
            ("C25108", dt.date(2025, 11, 10), dt.date(2025, 11, 11))]
CAL_DAYS = 28                  # the assay's calibration interval
ANALYZER_OFFSET = [0.0, 0.04]  # IA2 reads above IA1 on the same calibrators
CAL_LOT_SD = 0.04              # spread of the calibrator lots' effect
RECAL_SD = 0.025               # spread of a routine recalibration's effect
ASSAY_CV = 0.025               # the assay's own imprecision (log scale)
REPORT_LOW, REPORT_HIGH = 4.0, 150.0

# the October accuracy-based check, and the December bridging run
CHECK_EVENT = "2025-B"
CHECK_RUN = dt.datetime(2025, 10, 15, 10, 41)
CHECK_TARGETS = [13.6, 19.8, 27.4, 38.9, 55.2]
CHECK_REPORT_DATE = dt.date(2025, 11, 14)
BRIDGE_FRACTION = 0.20
BRIDGE_PULL = dt.date(2025, 12, 15)
BRIDGE_RUN = dt.datetime(2025, 12, 16, 8, 5)
TZ_NAME = "America/Denver"

CUTOFF = 20.0                  # ng/mL on the reference measurement procedure's scale
LINE = 0.30                    # a county opens when more than 30 per cent of its adults are below the cut-off
BOARD_DATE = dt.date(2026, 12, 9)
REQUEST_DATE = dt.date(2026, 10, 19)
ASSEMBLED = dt.datetime(2026, 10, 19, 15, 20, 0)
COMPANY = DISTRICT

FILES = {
    "contents": "README_files.txt",
    "plan": "mhnes_2025_analysis_plan.pdf",
    "results": "lis_vitd_results_2025.csv",
    "bridge": "lis_vitd_bridging_run_2025-12-16.csv",
    "tracking": "mhnes_2025_specimen_tracking.csv",
    "persons": "mhnes_2025_examined_persons.csv",
    "events": "analyzer_event_log_2025.csv",
    "instruments": "instrument_register.csv",
    "check": "accuracy_program_report_2025-B.pdf",
    "closeout": "mhnes_2025_fieldwork_closeout.pdf",
    "counties": "county_codes.csv",
    "dictionary": "mhnes_2025_data_dictionary.pdf",
    "supplements": "mhnes_2025_dsq_products.csv",
    "labels": "supplement_label_extract_2025.xlsx",
    "rosters": "mhnes_2025_screener_rosters.csv",
    "status": "mhnes_2025_sp_status.csv",
    "notice": "varnholt_customer_notice_2025-06.pdf",
    "tables2021": "mhnes_2021_county_tables.pdf",
}
GOLDEN = "vitamin_d_status_2025.xlsx"
