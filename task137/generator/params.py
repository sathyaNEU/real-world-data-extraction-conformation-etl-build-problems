"""Every constant of the world, in one place. Tarnfield Wholesale's delivery fleet, North East England and Cumbria."""
import datetime as dt

SEED = 13

AS_OF = dt.date(2026, 11, 2)                     # the day the claims-fund folder was put together
REC_START, REC_END = dt.date(2023, 10, 1), dt.date(2026, 9, 30)     # telematics record
LISTING_AS_AT = dt.date(2026, 10, 31)            # Ravensby's claims listing and the receipts run to here
FUND_YEAR = 2027

COMPANY = "Tarnfield Wholesale Ltd"
FASCIA = "Northfold Local"
INSURER = "Ravensby Insurance plc"
BODYSHOP = "Brantwick Accident Repair Ltd"
PLATFORM = "Gridtrak"

# depot code, name, site, postcode, latitude, longitude, trucks
DEPOTS = [
    ("CRA", "Cramlington", "Nelson Park West, Cramlington", "NE23 1WG", 55.0834, -1.5858, 73),
    ("GAT", "Gateshead", "Kingsway North, Team Valley, Gateshead", "NE11 0JH", 54.9352, -1.6204, 66),
    ("CAR", "Carlisle", "Kingmoor Park Central, Carlisle", "CA6 4SJ", 54.9183, -2.9617, 55),
    ("DAR", "Darlington", "Faverdale North, Darlington", "DL3 0QX", 54.5404, -1.5882, 70),
]
SPARE_SHARE = 0.04                               # spare trucks per depot, run when a route's truck is off the road

# collision rate per kilometre: base x traffic(local hour band) x darkness
BASE_PER_KM = 1.12e-5
DARK_MULT = 3.0
BAND_EDGES = [0, 4, 7, 9, 15, 19, 22, 24]        # local clock hours
TRAFFIC = [1.00, 1.00, 1.08, 1.00, 1.08, 1.00, 1.00]

# schedules (local clock hours)
STD_DEP = (7.50, 9.50)        # standard schedule, September to April
SUM_DEP = (3.75, 5.25)        # summer schedule, May to August
SUMMER_MONTHS = (5, 6, 7, 8)
PLAN_DEP = (3.75, 5.25)       # the 2027 schedule, all year
DUR_H = (8.0, 10.0)
KM_PER_H = (26.0, 33.0)
NO_RUN_DAYS = ((12, 25), (12, 26), (1, 1))       # Christmas Day, Boxing Day, New Year's Day

# claims
NOTIFY_LAG = [(0, 0.70), (1, 0.20), (2, 0.04), (3, 0.02), (5, 0.015), (7, 0.01), (14, 0.008), (30, 0.007)]
P_OD = 0.86            # own damage head
P_TPPD = 0.52          # third-party property damage head
P_TPI = 0.05           # third-party injury head
LIABILITY = [("ours", 0.55), ("theirs", 0.25), ("shared", 0.12), ("no_tp", 0.08)]
SHARES = [(0.5, 0.52), (2 / 3, 0.12), (0.75, 0.14), (1 / 3, 0.10), (0.25, 0.12)]   # the other side's share when shared
P_DUP_NOTIFY = 0.022   # a second notification of one collision, closed as a duplicate
P_WITHDRAWN = 0.016    # a notification later withdrawn, no incident
CARS = 58              # company cars on the same motor policy (a separate fund)
CAR_CLAIMS_PER_YEAR = 13.0

# own-damage repair costs (net of VAT) and invoices
REPAIR_MEDIAN = 2900.0
REPAIR_SIGMA = 0.62
P_SUPP1, P_SUPP2 = 0.38, 0.09
P_ADAS = 0.30                      # a repair that disturbs the forward sensors: each fitted sensor is calibrated
P_RADAR = 0.55                     # trucks fitted with a front radar beside the windscreen camera
ADAS_NET = 185.00                  # Brantwick's fixed price for one static calibration
P_LATE_CERT = 0.55                 # the radar calibration's certificate comes back days after the job is completed
P_WRITE_OFF = 0.028
RECOVERY_FEE = 95.00               # recovery and storage, invoiced through the bodyshop on some jobs
P_RECOVERY = 0.24
VAT = 0.20
DOUBLE_SEND = [(dt.date(2025, 2, 3), dt.date(2025, 3, 28)), (dt.date(2025, 10, 6), dt.date(2025, 11, 21)),
               (dt.date(2026, 4, 13), dt.date(2026, 5, 15))]   # the bodyshop's EDI feed sent each invoice twice

ASK_FROM, ASK_TO = dt.date(2025, 1, 1), dt.date(2026, 6, 30)      # the asks' collisions
RECEIPTS_FROM = dt.date(2024, 10, 1)             # the recovery account extract runs from here to LISTING_AS_AT

# recoveries from other insurers
P_OUR_REF = 0.54                   # receipts quoting Tarnfield's claim number
RECOVERY_LAG_D = (38, 190)
P_RECOVERED = 0.93                 # recoverable claims settled by the pack date (older collisions)

TP_INSURERS = ["Aldwyn General Insurance Ltd", "Bellmont Motor Underwriting Ltd", "Coquet Mutual Insurance",
               "Delamere Insurance plc", "Elsdon Direct Ltd", "Fenwick & Hart Insurance", "Greyfriars Assurance Ltd",
               "Halsall Motor Ltd", "Ingleby Insurance Company", "Kirkhaugh Insurance plc", "Lowther General Ltd",
               "Morrell Motor Insurance", "Northallerton Mutual", "Ottery Underwriting Ltd"]
TP_WEIGHTS = [0.12, 0.10, 0.09, 0.09, 0.08, 0.08, 0.07, 0.07, 0.06, 0.06, 0.05, 0.05, 0.04, 0.04]

PEOPLE = {"risk_manager": "Jenna Cole", "transport_director": "Darren Kirk", "workshop": "Leigh Riley",
          "finance_director": "Joshua Donnelly"}
