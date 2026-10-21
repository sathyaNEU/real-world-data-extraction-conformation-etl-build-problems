"""task251 architecture 4: the world's fixed facts. Halbrook Region (fictional, southern Ontario) counts traffic at 30
permanent stations on its regional roads; five pairs stand on the two approaches of its Kessel River bridges."""
import datetime as dt

SEED = 91
ORG = "Regional Municipality of Halbrook"
DEPT = "Transportation Services, Traffic Data Program"
STANDARD = "TDP-03"
CONTRACTOR_VAL = "Northline Traffic Data Inc."
CONTRACTOR_MAINT = "Carrick Signal & Systems Ltd."
SYSTEM = "TrafficVault"
PEOPLE = dict(coordinator="Miranda Harris", validation="Andrew Wong", maintenance="Yvonne Larson")
TOLERANCE = 0.05
YEAR = 2027
REPORT_DUE = dt.date(2028, 3, 31)
ROUND_START = dt.date(2028, 4, 10)

DISTRICTS = ("Ashby", "Kessel", "Marlow")

# Ontario 2027 statutory holidays as the region observes them (offices closed)
HOLIDAYS = [dt.date(2027, 1, 1), dt.date(2027, 2, 15), dt.date(2027, 3, 26), dt.date(2027, 5, 24),
            dt.date(2027, 7, 1), dt.date(2027, 8, 2), dt.date(2027, 9, 6), dt.date(2027, 10, 11),
            dt.date(2027, 12, 27), dt.date(2027, 12, 28)]
# school terms (the commuter peaks follow them)
TERMS = [(dt.date(2027, 1, 4), dt.date(2027, 3, 12)), (dt.date(2027, 3, 22), dt.date(2027, 6, 25)),
         (dt.date(2027, 9, 7), dt.date(2027, 12, 17))]

# bridges over the Kessel River: road, structure name, km from and to, lanes each way on the deck
BRIDGES = [
    dict(road=4, name="Wexford Bridge", km=(8.62, 9.05), lanes=1, south="R04-02", north="R04-03", s_km=8.21, n_km=9.48),
    dict(road=11, name="Mill Race Bridge", km=(3.91, 4.27), lanes=1, south="R11-01", north="R11-02", s_km=3.44, n_km=4.79),
    dict(road=17, name="Hannon Bridge", km=(12.48, 12.93), lanes=1, south="R17-03", north="R17-04", s_km=12.07, n_km=13.36),
    dict(road=22, name="Lockhart Bridge", km=(6.15, 6.58), lanes=1, south="R22-01", north="R22-02", s_km=5.72, n_km=7.02),
    dict(road=29, name="Ferrier Bridge", km=(15.30, 15.71), lanes=1, south="R29-02", north="R29-03", s_km=14.86, n_km=16.18),
]

# the other twenty stations: code, road, km, axis, lanes each way, district, congested (a bottleneck downstream)
OTHERS = [
    ("R01-01", 1, 2.36, "NS", 2, "Marlow", False), ("R02-01", 2, 5.12, "EW", 2, "Marlow", True),
    ("R03-02", 3, 7.84, "NS", 1, "Ashby", False), ("R05-01", 5, 1.67, "EW", 3, "Kessel", True),
    ("R06-01", 6, 9.25, "NS", 2, "Kessel", False), ("R07-02", 7, 4.48, "EW", 2, "Ashby", False),
    ("R08-01", 8, 3.03, "NS", 2, "Kessel", True), ("R09-01", 9, 11.36, "EW", 1, "Ashby", False),
    ("R10-03", 10, 6.71, "NS", 3, "Marlow", True), ("R12-01", 12, 2.94, "EW", 2, "Kessel", False),
    ("R13-02", 13, 8.05, "NS", 2, "Ashby", False), ("R14-01", 14, 4.62, "EW", 2, "Marlow", True),
    ("R15-01", 15, 10.18, "NS", 1, "Ashby", False), ("R16-02", 16, 3.77, "EW", 2, "Kessel", False),
    ("R18-01", 18, 5.53, "NS", 3, "Kessel", True), ("R19-01", 19, 7.29, "EW", 2, "Marlow", False),
    ("R20-02", 20, 2.18, "NS", 2, "Ashby", False), ("R23-01", 23, 9.64, "EW", 3, "Marlow", True),
    ("R25-01", 25, 1.92, "NS", 2, "Kessel", False), ("R31-01", 31, 6.37, "EW", 2, "Ashby", False),
]
BRIDGE_DISTRICT = dict(south="Ashby", north="Kessel")

# controllers replaced during 2027: the station takes a new number from the replacement date
RENUMBERED = {"R08-01": ("R08-05", dt.date(2027, 5, 12)), "R19-01": ("R19-03", dt.date(2027, 9, 21))}
# controller generation: the newer TCX-4 reports occupancy in integer tenths of a per cent
NEW_CONTROLLERS = {"R02-01", "R05-01", "R10-03", "R11-01", "R11-02", "R14-01", "R18-01", "R22-01", "R22-02",
                   "R23-01", "R08-01", "R19-01"}

LOSS_KNEE = 20.0     # occupancy (per cent) above which the loops start to lose vehicles in queued traffic
LOSS_SLOPE = 0.0100  # share of vehicles lost per point of occupancy above the knee
B_SD = 0.034         # spread of the stations' sensitivities
