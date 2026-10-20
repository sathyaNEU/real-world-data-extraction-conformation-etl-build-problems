"""The fixed world: Hollister Gas, the city-owned gas utility of a fictional northern U.S. city, its twelve
distribution districts, the frost season in which cast-iron and bare-steel mains crack, the yearly district leak
surveys and the public's odor reports. Every other module reads its parameters from here."""
import datetime as dt

CITY = "Hollister"
UTILITY = "Hollister Gas"
DEPT = "Distribution Integrity"
PEOPLE = {"engineer": ("Marissa Harmon", "Distribution Integrity Engineer"),
          "manager": ("Nicholas Wolf", "Gas Operations Manager")}
SEED = 476
YEAR = 2026
END = dt.date(2026, 12, 31)
EXTRACT = dt.date(2027, 3, 15)
GUIDELINE_DATE = "11 January 2027"
MEMO_DATE = "20 April 2027"
HEARING_DATE = "18 May 2027"
LINE = 3.30                  # tonnes of methane per mile of cast-iron and bare-steel main, 2026; at or above designates

# the share of leak starts by calendar month on cast-iron and bare-steel mains (frost cracking); plastic and coated
# steel leak at a low even rate
SEASON = [0.170, 0.158, 0.118, 0.061, 0.038, 0.029, 0.027, 0.030, 0.040, 0.062, 0.104, 0.163]

# emission rate by grade, kilograms of methane per hour (the program's table)
RATE = {1: 1.62, 2: 0.54, 3: 0.21}

# district: survey month, miles of cast iron, bare steel, coated steel, plastic; leak starts per CI/BS mile a year;
# the share of leaks the public reports by odor (near buildings); repair practice (days to repair a grade 2, share of
# grade 3 repaired within the year)
DISTRICTS = {
    "Ashby":        (4,  38.2, 12.1, 40.5, 96.3, 1.0951, 0.28, 64, 0.35),
    "Brennan Hill": (10, 31.4, 18.9, 22.0, 71.2, 1.6517, 0.31, 71, 0.30),
    "Calder":       (6,  44.7, 9.3, 35.1, 102.8, 1.1353, 0.26, 58, 0.42),
    "Dorrance":     (9,  27.6, 15.2, 30.4, 88.0, 1.0956, 0.33, 92, 0.25),
    "Elmwood":      (3,  41.3, 11.8, 28.7, 79.5, 2.2503, 0.29, 61, 0.38),
    "Fenwick":      (11, 35.9, 14.4, 26.3, 83.1, 1.3319, 0.27, 66, 0.33),
    "Glenmora":     (5,  39.8, 16.6, 31.9, 94.4, 1.3947, 0.30, 55, 0.40),
    "Harlow":       (12, 29.1, 13.7, 24.6, 77.0, 1.8439, 0.32, 74, 0.31),
    "Ivers":        (8,  33.5, 10.9, 37.2, 99.6, 1.8271, 0.28, 69, 0.36),
    "Juniper":      (2,  36.8, 15.3, 29.0, 81.7, 1.5202, 0.30, 63, 0.34),
    "Kessel":       (7,  30.2, 12.8, 33.4, 90.9, 0.8844, 0.29, 77, 0.29),
    "Lockwood":     (1,  37.4, 14.1, 27.8, 85.2, 1.2399, 0.31, 60, 0.37),
}
OTHER_RATE = 0.06           # leak starts per coated-steel or plastic mile a year, any month
GRADE_P = (0.12, 0.38, 0.50)
FIRST_YEAR = 2016

FILES = {
    "guidelines": "amr_program_guidelines_2027.pdf",
    "finds": "leak_survey_finds_2016_2026.csv",
    "odor": "odor_call_log_2016_2026.csv",
    "repairs": "leak_repair_orders_2016_2027.csv",
    "schedule": "leak_survey_schedule_2015_2026.csv",
    "mains": "gis_main_segments_2026-12-31.csv",
    "notes": "integrity_data_extract_notes.txt",
    "costs": "work_order_cost_lines_2025_2026.csv",
    "closeouts": "work_order_closeouts_2025_2026.csv",
    "tickets": "service_interruption_tickets_2026.csv",
    "meters": "meter_premises_2027-03.csv",
    "customers": "district_customer_counts_2026.xlsx",
    "lauf": "lauf_annual_report_2026.pdf",
}
GOLDEN = {"workbook": "leak_methane_inventory_2026.xlsx", "memo": "main_replacement_designations_2027.pdf"}
