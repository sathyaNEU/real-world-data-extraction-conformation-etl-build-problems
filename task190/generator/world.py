"""Arahura Bank: the world the pack is cut from."""

BANK = "Arahura Bank"
GEO = "New Zealand"
CCY = "NZD"

# The AML/CFT Act 2009 threshold for a domestic physical cash transaction report.
THRESHOLD = 10000.00
BAND_LO, BAND_HI = 9000.00, 10000.00

YEAR_LO, YEAR_HI = "2026-07-01", "2027-06-30"          # the reporting year the figure is for
PRIOR_LO, PRIOR_HI = "2025-07-01", "2026-06-30"
EXTRACT = "2027-07-19"                                  # the as-of date of every extract
REPORT_DUE = "2027-09-30"                               # the annual report to the supervisor

MLRO = "Manaaki Little"                                 # money laundering reporting officer
ASSURANCE = "Emma Gullery"                              # the bank's assurance lead

# segment: key, name, cash deposits paid in during the reporting year, the decay its own
#          amount density runs at, customers, structured deposits planted in the reporting
#          year, planted in the prior year
SEGMENTS = [
    ("GRO", "Grocery and convenience", 15037, 9600.0, 1163, 94, 66),
    ("HOS", "Hospitality", 4723, 8200.0, 2247, 35, 24),
    ("TRA", "Transport and courier", 10261, 11500.0, 857, 172, 120),
    ("CON", "Trades and construction", 3118, 10400.0, 1538, 50, 35),
    ("RUR", "Rural supply and horticulture", 2396, 10900.0, 971, 0, 0),
    ("FUE", "Fuel and automotive", 4109, 9100.0, 418, 66, 46),
    ("PER", "Personal services", 3944, 7600.0, 1764, 50, 35),
    ("CLB", "Clubs and community", 2713, 8800.0, 643, 6, 4),
]

# the figure is stated to the nearest fifty deposits per segment: the granularity the record's own
# scatter supports, measured over the judge's candidate set
GRAIN = 50

SEG_NAME = {k: n for k, n, *_ in SEGMENTS}
SEG_KEYS = [k for k, *_ in SEGMENTS]

# The bank's own segment map was reissued in April 2027: the codes changed, the segments did not.
OLD_CODE = {"GRO": "B12", "HOS": "B14", "TRA": "B21", "CON": "B23",
            "RUR": "B31", "FUE": "B17", "PER": "B41", "CLB": "B52"}
NEW_CODE = {"GRO": "BB-RET-02", "HOS": "BB-HOS-01", "TRA": "BB-TRN-03", "CON": "BB-CON-01",
            "RUR": "BB-RUR-02", "FUE": "BB-RET-05", "PER": "BB-SRV-04", "CLB": "BB-COM-01"}
RECODE_DATE = "2027-04-06"

# branches: code, name, region, opened, closed (the Hastings pair merged in the window)
BRANCHES = [
    ("AR01", "Queen Street", "Auckland", "2009-03-02", ""),
    ("AR02", "Newmarket", "Auckland", "2011-08-15", ""),
    ("AR04", "Manukau", "Auckland", "2013-02-04", ""),
    ("AR07", "Hamilton Central", "Waikato", "2010-06-21", ""),
    ("AR09", "Tauranga", "Bay of Plenty", "2012-11-05", ""),
    ("AR11", "Hastings Heretaunga", "Hawke's Bay", "2008-04-07", "2026-11-27"),
    ("AR12", "Hastings Karamu", "Hawke's Bay", "2014-09-01", ""),
    ("AR15", "Palmerston North", "Manawatu", "2009-10-12", ""),
    ("AR18", "Wellington Lambton", "Wellington", "2007-02-05", ""),
    ("AR19", "Porirua", "Wellington", "2015-03-30", ""),
    ("AR23", "Christchurch Riccarton", "Canterbury", "2010-01-18", ""),
    ("AR25", "Timaru", "Canterbury", "2013-07-08", ""),
    ("AR28", "Dunedin Octagon", "Otago", "2011-04-11", ""),
    ("AR31", "Invercargill", "Southland", "2016-02-15", ""),
]
# AR11 closed into AR12 on 27 November 2026; AR12 was renamed on the same day.
MERGED_INTO = {"AR11": "AR12"}
RENAMED = {"AR12": ("Hastings Karamu", "Hastings", "2026-11-27")}

CHANNELS = ["counter", "machine"]

# The smart deposit machine estate, as the property register keeps it: machine, site, the day it
# went in and the day it came out. Deposits are taken only by a machine in service that day.
MACHINES = [
    ("SDM-0412", "AR01", "2019-03-18", ""),
    ("SDM-0413", "AR01", "2019-03-18", ""),
    ("SDM-0518", "AR02", "2020-07-06", ""),
    ("SDM-0641", "AR04", "2021-02-15", ""),
    ("SDM-0642", "AR04", "2021-02-15", ""),
    ("SDM-0703", "AR07", "2021-09-13", ""),
    ("SDM-0811", "AR09", "2022-05-09", ""),
    ("SDM-0907", "AR11", "2022-11-21", "2026-11-27"),
    ("SDM-1044", "AR12", "2023-04-03", ""),
    ("SDM-1045", "AR12", "2026-11-30", ""),
    ("SDM-1162", "AR15", "2023-10-16", ""),
    ("SDM-1208", "AR18", "2024-02-26", ""),
    ("SDM-1209", "AR18", "2024-02-26", ""),
    ("SDM-1317", "AR19", "2024-08-12", ""),
    ("SDM-1402", "AR23", "2025-01-20", ""),
    ("SDM-1403", "AR23", "2025-01-20", ""),
    ("SDM-1455", "AR25", "2025-06-02", ""),
    ("SDM-1509", "AR28", "2025-11-10", ""),
    ("SDM-1562", "AR31", "2026-09-07", ""),
    ("SDM-1577", "AR02", "2027-02-01", ""),
]
# Two sites run two machines and the vendor reports by site; these two sign off after restoring.
TWO_MACHINE_SITES = ["AR01", "AR04", "AR12", "AR18", "AR23"]
SIGNOFF_SITES = ["AR15", "AR19"]
# Machines in service through the year that raised no service call at all.
NO_INCIDENT = ["SDM-1455", "SDM-1562", "SDM-1509"]

ANZSIC = {
    "GRO": ["4110", "4121", "4129", "4123"],
    "HOS": ["4511", "4512", "4513", "4520"],
    "TRA": ["4610", "4621", "5101", "5102"],
    "CON": ["3231", "3232", "3234", "3242", "3099"],
    "RUR": ["0121", "0132", "0149", "3323"],
    "FUE": ["4000", "3912", "9411", "9412"],
    "PER": ["9511", "9512", "9520", "9531"],
    "CLB": ["9112", "9113", "9139", "9559"],
}
