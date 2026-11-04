"""The fiction's names, files and fixed facts, in one place."""
import datetime as dt

SEED = 4882
RK = 53          # the refueller day's fork of the seed (model.search)
AS_OF = "2026-10-14"

AIRPORT = "Windrell International Airport"
CORP = "Windrell Fuel Facilities Corporation"
OPERATOR = "Pellacre Aviation Services"
CORBEL = "Corbel Into-Plane Services"
NORTHGARTH = "Northgarth Aviation Fuelling"
SUPPLIER = "Teverell Fuels"
QM_MANAGER = "Natalie Daugherty"          # the Operator's fuel quality manager at Windrell
CHAIR = "William Hopkins"                 # chair of the corporation's fuel quality committee

FILES = {
    "scada": "hydrant_scada_2026-09-14_2026-10-14.csv",
    "register": "hydrant_network_register.xlsx",
    "shiftlog": "farm_shift_log_2026-10-12_14.pdf",
    "maint": "hydrant_maintenance_2026-wk42.xlsx",
    "corbel_tickets": "corbel_fuel_tickets_2026-10-12_14.csv",
    "ng_tickets": "northgarth_tickets_20261012-20261014.xlsx",
    "corbel_checks": "corbel_daily_checks_2026-10.csv",
    "ng_checks": "northgarth_qc_checks_oct2026.xlsx",
    "certs": "batch_certificates_register_2026.csv",
    "rack": "rack_loading_log_2026-10-12_14.csv",
    "equipment": "into_plane_equipment_register.xlsx",
    "ng_vehicles": "northgarth_vehicle_log_2026-10.csv",
    "corbel_equipment": "corbel_equipment_log_2026-10.csv",
    "recall": "recall_notice_RN-2026-031.pdf",
    "qm09": "QM-09_product_quarantine_and_recall.pdf",
    "pits_q3": "pit_valve_inspections_2026-q3.xlsx",
    "stock": "stock_reconciliation_2026-09.pdf",
}
GOLDEN = {"csv": "j26-1187_recall_uplifts.csv", "pdf": "hydrant_resumption_plan.pdf"}
DISTRACTORS = ["pits_q3", "stock"]

TUE = dt.datetime(2026, 10, 13, 0, 0, 0)       # local second 0
UTC_OFFSET = dt.timedelta(hours=7)               # PDT


def local(t):
    return TUE + dt.timedelta(seconds=t)


def utc(t):
    return local(t) + UTC_OFFSET


# hydrant line-ups over the SCADA export, local time: (when, tank)
LINEUPS = [
    (dt.datetime(2026, 8, 28, 13, 5), 2), (dt.datetime(2026, 9, 4, 10, 15), 3),
    (dt.datetime(2026, 9, 10, 7, 30), 1), (dt.datetime(2026, 9, 16, 14, 20), 2),
    (dt.datetime(2026, 9, 22, 6, 45), 4), (dt.datetime(2026, 9, 28, 11, 10), 3),
    (dt.datetime(2026, 10, 3, 8, 35), 1), (dt.datetime(2026, 10, 8, 9, 40), 2),
    (dt.datetime(2026, 10, 13, 6, 0), 3), (dt.datetime(2026, 10, 13, 15, 40), 1),
]
SUSPENDED = dt.datetime(2026, 10, 14, 5, 30)
PROVING = dt.datetime(2026, 10, 13, 10, 47)      # the pump station meter's proving: the totaliser restarts at zero

# the certificates register: batch, tank, received, certified, released (local), density at 15 C, conductivity,
# flash point, freezing point, status
BATCHES = [
    ("J-26-1102", 4, "2026-08-13", "2026-08-15", "2026-08-18 06:30", 799.0, 151, 41.5, -51.2, "ISSUED"),
    ("J-26-1110", 2, "2026-08-23", "2026-08-26", "2026-08-28 13:05", 802.8, 219, 42.5, -50.6, "ISSUED"),
    ("J-26-1117", 3, "2026-08-30", "2026-09-02", "2026-09-04 10:15", 796.9, 197, 41.0, -52.1, "ISSUED"),
    ("J-26-1129", 1, "2026-09-05", "2026-09-08", "2026-09-10 07:30", 802.2, 205, 42.0, -49.8, "ISSUED"),
    ("J-26-1143", 2, "2026-09-12", "2026-09-15", "2026-09-16 14:20", 797.7, 264, 40.5, -52.6, "ISSUED"),
    ("J-26-1150", 4, "2026-09-17", "2026-09-20", "2026-09-22 06:45", 800.6, 188, 43.0, -50.4, "ISSUED"),
    ("J-26-1158", 3, "2026-09-23", "2026-09-26", "2026-09-28 11:10", 804.1, 172, 44.5, -48.9, "ISSUED"),
    ("J-26-1166", 1, "2026-09-29", "2026-10-01", "2026-10-03 08:35", 798.5, 243, 41.0, -51.7, "ISSUED"),
    ("J-26-1171", 2, "2026-10-04", "2026-10-07", "2026-10-08 09:40", 803.6, 236, 43.5, -49.3, "ISSUED"),
    ("J-26-1179", 1, "2026-10-09", "2026-10-12", "2026-10-13 15:40", 801.3, 312, 42.5, -50.1, "IN SERVICE"),
    ("J-26-1187", 3, "2026-10-10", "2026-10-12", "2026-10-13 06:00", 795.4, 88, 40.0, -53.0, "RECALLED 2026-10-14 05:12"),
    ("J-26-1192", 4, "2026-10-13", "", "", 800.9, 0, 0.0, 0.0, "SETTLING"),
]
LABEL_BATCH = {"aged": "J-26-1102", "old": "J-26-1171", "batch": "J-26-1187", "new": "J-26-1179"}
DENSITY = {b[0]: b[5] for b in BATCHES}
CONDUCTIVITY = {b[0]: b[6] for b in BATCHES}

CORBEL_INITIALS = ["JT", "MR", "SK", "AL", "DP", "WN", "EB"]
NG_INITIALS = ["KB", "RO", "TV", "HM", "CE", "LF"]
OPERATOR_INITIALS = ["R.M.", "K.T.", "J.O.", "P.S."]

# litres received into each tank in each batch (cubic metres at 15 C), for the stock reconciliation
RECEIPT_M3 = {"J-26-1110": 14086.3, "J-26-1117": 13951.8, "J-26-1129": 14112.6, "J-26-1143": 14047.9,
              "J-26-1150": 13978.4, "J-26-1158": 14135.2, "J-26-1166": 14020.7}
