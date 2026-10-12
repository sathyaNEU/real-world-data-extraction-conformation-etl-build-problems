"""The Holmvik Area Control Centre world: sectors, traffic flows, operators, dates and the people who sign the
documents. Everything here is fiction (Aldmark, its air navigation service provider, its airports and operators);
the external airports are real ICAO locations used only as origins and destinations of traffic."""
import datetime as dt
from zoneinfo import ZoneInfo

UTC = dt.timezone.utc
LOCAL = ZoneInfo("Europe/Copenhagen")      # Aldmark keeps Central European time, summer time per the EU calendar

ANSP = "Aldmark Air Navigation"
UNIT = "Holmvik Area Control Centre"
UNIT_SHORT = "Holmvik ACC"

# eight elementary en-route sectors, FL245 to FL660
SECTORS = ["TRV", "MSB", "GRD", "LNM", "KRW", "LYS", "HAL", "SDV"]
NAME = {"TRV": "Tarvik", "MSB": "Mosby", "GRD": "Grendal", "LNM": "Linmark", "KRW": "Karrow", "LYS": "Lysvik",
        "HAL": "Hallin", "SDV": "Sandvik"}
CODE = {v: k for k, v in NAME.items()}
FREQ = {"TRV": "128.355", "MSB": "132.880", "GRD": "125.105", "LNM": "134.230", "KRW": "127.680", "LYS": "131.455",
        "HAL": "129.930", "SDV": "126.555"}
ADJACENT = {"TRV": ["GRD", "LYS", "MSB", "LNM"], "MSB": ["TRV", "LNM", "SDV", "KRW"], "GRD": ["TRV", "KRW", "HAL"],
            "LNM": ["MSB", "TRV", "HAL"], "KRW": ["GRD", "HAL", "MSB", "SDV"], "LYS": ["TRV", "SDV"],
            "HAL": ["KRW", "GRD", "LNM"], "SDV": ["MSB", "LYS", "KRW"]}
TV = {s: "AH" + s for s in SECTORS}        # network manager traffic volume of each sector

HUB, BREKKA, SKARNES = "EXHM", "EXBK", "EXSK"
AIRPORT_NAME = {HUB: "Holmvik", BREKKA: "Brekka", SKARNES: "Skarnes"}

# the record and the forward season
ACTUAL_START = dt.datetime(2025, 1, 1, tzinfo=UTC)
ACTUAL_END = dt.datetime(2026, 10, 1, tzinfo=UTC)          # exclusive
EXTRACT_DAY = dt.date(2026, 10, 12)
PLAN_ISSUED = dt.date(2026, 10, 9)
BOARD_DAY = dt.date(2026, 11, 4)


def season(year):
    """The summer season, 1 June to 31 August local time, as UTC instants [start, end)."""
    a = dt.datetime(year, 6, 1, tzinfo=LOCAL).astimezone(UTC)
    b = dt.datetime(year, 9, 1, tzinfo=LOCAL).astimezone(UTC)
    return a, b


REROUTE_W = dt.datetime(2026, 3, 19, tzinfo=UTC)          # AIRAC 2603: western arrivals all onto the Hallin descent
CONFIG_REV9 = dt.datetime(2026, 7, 14, 6, 0, tzinfo=LOCAL)  # configuration table revision 9 in force
TOLERANCE = 40.0

# cruise level sets (flight levels)
EAST = [330, 350, 370, 390]
WEST = [340, 360, 380, 400]
NORTH = [310, 330, 350, 370, 390]
SOUTH = [300, 320, 340, 360, 380]
LOWC = [250, 270, 290]

# external airports by direction
WEST_AP = ["EGLL", "EGKK", "EHAM", "EBBR", "EIDW", "EGCC", "LFPG", "EGSS"]
EAST_AP = ["EFHK", "EETN", "EVRA", "EYVI", "EPWA", "ESSA"]
NORTH_AP = ["ENGM", "ENBR", "ENVA", "ESGG", "ENZV"]
SOUTH_AP = ["LEMD", "LEBL", "LIRF", "LPPT", "LFMN", "LSZH", "LOWW", "LGAV", "LEPA", "LIMC"]
NW_AP = ["BIKF", "ENBR", "EGPH", "EGPF"]
SW_AP = ["EDDF", "EDDM", "LSGG", "EDDL", "EDDH"]

# operators: designator, the kind of flying, three-digit or alphanumeric flight numbers
OPERATORS = {
    "AMK": "Aldmark national carrier (hub Holmvik)", "NLY": "Nordlys Air (low-cost, Brekka base from summer 2027)",
    "VSK": "low-cost, pan-European", "HXA": "network carrier", "GML": "network carrier", "PXR": "low-cost",
    "MRN": "regional", "DXT": "charter", "KRB": "cargo", "TQA": "network carrier", "ZBL": "low-cost",
    "OVN": "long-haul", "RFX": "cargo", "LNX": "regional", "CWA": "charter", "BRT": "regional (Brekka)",
}
TYPES = {"short": ["A320", "A20N", "B738", "B38M", "A321", "A21N", "A319", "E195", "E190", "CRJ9"],
         "long": ["B789", "A333", "B77W", "A359", "B763", "A332"],
         "regional": ["E190", "E195", "CRJ9", "A220", "E75L"]}

# flows: the sectors each flight crosses (sector, entry level, exit level, minutes), "C" is the flight's cruise
# level; levels drawn from lv with weights w; base is flights per day at summer 2026 traffic
FLOWS = {
    "EW_E": dict(path=[("GRD", "C", "C", 18), ("TRV", "C", "C", 20), ("LYS", "C", "C", 16)], lv=EAST,
                 w=[.15, .3, .35, .2], base=230, dep=WEST_AP, arr=EAST_AP, ops=["HXA", "VSK", "GML", "PXR", "TQA", "ZBL", "OVN", "AMK", "RFX"], kind="mix"),
    "EW_W": dict(path=[("LYS", "C", "C", 16), ("TRV", "C", "C", 20), ("GRD", "C", "C", 18)], lv=WEST,
                 w=[.15, .3, .35, .2], base=230, dep=EAST_AP, arr=WEST_AP, ops=["HXA", "VSK", "GML", "PXR", "TQA", "ZBL", "OVN", "AMK", "RFX"], kind="mix"),
    "NS_S": dict(path=[("LNM", "C", "C", 20), ("MSB", "C", "C", 18), ("SDV", "C", "C", 18)], lv=SOUTH,
                 w=None, base=150, dep=NORTH_AP, arr=SOUTH_AP, ops=["VSK", "PXR", "DXT", "CWA", "GML", "ZBL", "HXA"], kind="short"),
    "NS_N": dict(path=[("SDV", "C", "C", 18), ("MSB", "C", "C", 18), ("LNM", "C", "C", 20)], lv=NORTH,
                 w=None, base=150, dep=SOUTH_AP, arr=NORTH_AP, ops=["VSK", "PXR", "DXT", "CWA", "GML", "ZBL", "HXA"], kind="short"),
    "DG_SW": dict(path=[("HAL", "C", "C", 19), ("KRW", "C", "C", 19)], lv=SOUTH, w=None, base=110,
                  dep=NW_AP, arr=SW_AP, ops=["TQA", "HXA", "MRN", "LNX", "KRB", "VSK"], kind="short"),
    "DG_NE": dict(path=[("KRW", "C", "C", 19), ("HAL", "C", "C", 19)], lv=NORTH, w=None, base=110,
                  dep=SW_AP, arr=NW_AP, ops=["TQA", "HXA", "MRN", "LNX", "KRB", "VSK"], kind="short"),
    "HUB_DEP_S": dict(path=[("MSB", 245, "C", 14), ("SDV", "C", "C", 16)], lv=SOUTH, w=None, base=34,
                      dep=[HUB], arr=SOUTH_AP, ops=["AMK", "VSK", "PXR"], kind="short"),
    "HUB_DEP_SH": dict(path=[("MSB", 245, "C", 10)], lv=LOWC, w=None, base=8, dep=[HUB], arr=["EKBI", "EKAH", "ESMS"],
                       ops=["AMK", "MRN"], kind="regional"),
    "HUB_DEP_E": dict(path=[("TRV", 245, "C", 9), ("LYS", "C", "C", 14)], lv=LOWC, w=None, base=40, dep=[HUB],
                      arr=EAST_AP, ops=["AMK", "MRN", "LNX"], kind="regional"),
    "HUB_DEP_W": dict(path=[("KRW", 245, "C", 13), ("GRD", "C", "C", 15)], lv=WEST, w=None, base=28, dep=[HUB],
                      arr=WEST_AP, ops=["AMK", "HXA", "VSK"], kind="short"),
    "HUB_ARR_N": dict(path=[("LNM", "C", 245, 14)], lv=NORTH, w=None, base=38, dep=NORTH_AP, arr=[HUB],
                      ops=["AMK", "VSK", "MRN", "GML"], kind="short"),
    "HUB_ARR_E": dict(path=[("LYS", "C", 245, 13)], lv=WEST, w=None, base=40, dep=EAST_AP, arr=[HUB],
                      ops=["AMK", "MRN", "LNX"], kind="regional"),
    "HUB_ARR_ET": dict(path=[("LYS", "C", "C", 16), ("TRV", "C", 245, 12)], lv=[360, 380], w=None, base=18,
                       dep=EAST_AP, arr=[HUB], ops=["AMK", "HXA", "OVN"], kind="mix"),
    "HUB_ARR_W": dict(path=[("HAL", "C", 245, 13)], lv=EAST, w=None, base=30, dep=WEST_AP + NW_AP, arr=[HUB],
                      ops=["AMK", "HXA", "VSK", "TQA"], kind="short"),
    "HUB_ARR_WK": dict(path=[("KRW", "C", 245, 12)], lv=EAST, w=None, base=10, dep=WEST_AP + SW_AP, arr=[HUB],
                       ops=["AMK", "HXA", "VSK", "TQA"], kind="short"),
    "SKN_DEP": dict(path=[("GRD", 245, "C", 12)], lv=WEST, w=None, base=19, dep=[SKARNES], arr=WEST_AP,
                    ops=["MRN", "VSK", "AMK"], kind="short"),
    "SKN_ARR": dict(path=[("GRD", "C", 245, 12)], lv=EAST, w=None, base=19, dep=WEST_AP, arr=[SKARNES],
                    ops=["MRN", "VSK", "AMK"], kind="short"),
    "SOUTH_ARR": dict(path=[("SDV", "C", 245, 13)], lv=NORTH, w=None, base=30, dep=SOUTH_AP, arr=[HUB],
                      ops=["AMK", "VSK", "PXR", "DXT"], kind="short"),
    "BRK_DEP_S": dict(path=[("MSB", 245, "C", 12), ("SDV", "C", "C", 16)], lv=SOUTH, w=None, base=8, dep=[BREKKA],
                      arr=SOUTH_AP, ops=["BRT", "DXT"], kind="regional"),
    "BRK_ARR": dict(path=[("MSB", "C", 245, 12)], lv=NORTH, w=None, base=8, dep=SOUTH_AP, arr=[BREKKA],
                    ops=["BRT", "DXT"], kind="regional"),
    # the new base, summer 2027 only
    "BRK_DEP_E": dict(path=[("TRV", 245, "C", 12), ("LYS", "C", "C", 14)], lv=[370, 390], w=[.6, .4], base=26,
                      dep=[BREKKA], arr=EAST_AP + ["EPKK", "EPGD", "LKPR"], ops=["NLY"], kind="lcc"),
    "BRK_ARR_E": dict(path=[("LYS", "C", "C", 14), ("TRV", "C", 245, 12)], lv=[380, 400], w=[.6, .4], base=26,
                      dep=EAST_AP + ["EPKK", "EPGD", "LKPR"], arr=[BREKKA], ops=["NLY"], kind="lcc"),
}
NEW_2027 = ("BRK_DEP_E", "BRK_ARR_E")

# daily traffic shape (local hour of entering the first sector) and the seasonal and yearly factors
HOURS = [1, 0.5, 0.4, 0.4, 0.6, 2, 5, 7, 7, 6.5, 6, 6, 6, 6, 6, 6.5, 7, 7, 6.5, 5.5, 4.5, 3.5, 2.5, 1.5]
MONTH = {1: .70, 2: .72, 3: .78, 4: .86, 5: .93, 6: 1.0, 7: 1.04, 8: 1.02, 9: .95, 10: .86, 11: .74, 12: .72}
YEAR = {2024: .95, 2025: .97, 2026: 1.0, 2027: 1.025}
WEEKDAY = [1.0, .97, .98, 1.0, 1.04, .9, .95]

# losses of separation per pair of aircraft in one sector at once whose levels change order (ATM contribution
# direct or indirect, and none), and ACAS resolution advisory encounters
LAMBDA_ATM = 2.45e-4
LAMBDA_NON = 0.20e-4
LAMBDA_RA = 3.9e-4

PEOPLE = {"safety": "Dorte Koch", "planning": "Erik Sørensen", "data": "Paw Frandsen"}
