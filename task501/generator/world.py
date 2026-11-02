"""The fiction: Lydden Valley Water's Stavenham trunk network, its districts, the 2025-26 operating year and the
2027 relining of the Ferrars Lane main. Internal keys (T01, X04, D04 ...) never ship; the pack carries the register's
own identifiers."""
import datetime as dt

SEED = 501005
COMPANY = "Lydden Valley Water"
TOWN = "Stavenham"

# ---------------------------------------------------------------- people (guard.py names --geo england --seed 501)
PEOPLE = dict(planner="Lauren Dobson", head_ops="Karl North", wq="Georgina Cooper", asset="Connor Wyatt")
TITLES = dict(planner="Network Operations Planner", head_ops="Head of Network Operations",
              wq="Water Quality Manager", asset="Asset Engineer, Trunk Mains")

# ---------------------------------------------------------------- junctions (internal node -> register name)
NODES = {
    "W": "Copt Hill works outlet", "N1": "Stavenham Cross", "N2": "Market Hill", "N3": "Ferrars Corner",
    "N4": "Mill Bridge", "N10": "Sallowby Gate", "N5": "Eastgate Bar", "N6": "Brook End", "N13": "Coldharbour",
    "N8": "North Lodge", "N9": "Highfield Top",
}

# ---------------------------------------------------------------- mains: key -> (id, name, from, to, dn, material,
# lining, year, length m). Trunk mains run from -> to in normal service; interconnectors list their two ends.
MAINS = {
    "T01": ("TM101", "Copt Hill outlet main", "W", "N1", 600, "Ductile iron", "Cement mortar", 2011, 2870),
    "T02": ("TM102", "Stavenham town main", "N1", "N2", 450, "Ductile iron", "Cement mortar", 2011, 1940),
    "T03": ("TM107", "Ferrars Lane main", "N2", "N3", 375, "Cast iron", "Unlined", 1931, 2310),
    "T04": ("TM108", "Mill Road main", "N3", "N4", 300, "Cast iron", "Unlined", 1931, 1660),
    "T10": ("TM115", "Sallowby Road main", "N4", "N10", 300, "Cast iron", "Unlined", 1954, 2050),
    "T05": ("TM104", "Eastgate main", "N1", "N5", 375, "Cast iron", "Unlined", 1938, 1780),
    "T06": ("TM105", "Brook Street main", "N5", "N6", 300, "Cast iron", "PE close-fit (2026)", 1938, 1420),
    "T13": ("TM112", "Coldharbour Road main", "N5", "N13", 300, "Cast iron", "Unlined", 1962, 1370),
    "T08": ("TM109", "North Road main", "N2", "N8", 375, "Cast iron", "Unlined", 1935, 2120),
    "T09": ("TM110", "Highfield main", "N8", "N9", 300, "Cast iron", "Unlined", 1957, 1590),
    "X05": ("IC02", "Coldharbour-Brook interconnector", "N13", "N6", 250, "Cast iron", "Unlined", 1971, 760),
    "X02": ("IC03", "Highfield-Sallowby interconnector", "N9", "N10", 300, "Cast iron", "Unlined", 1966, 1260),
    "X04": ("IC05", "Coldharbour-Ferrars interconnector", "N13", "N3", 300, "Cast iron", "Unlined", 1971, 980),
    "X07": ("IC08", "Brook-Mill interconnector", "N6", "N4", 250, "Cast iron", "Unlined", 1968, 1140),
}
TRUNK = [k for k in MAINS if k.startswith("T")]
INTER = [k for k in MAINS if k.startswith("X")]
MAIN_ID = {k: v[0] for k, v in MAINS.items()}
KEY_OF = {v[0]: k for k, v in MAINS.items()}
# mains whose wall carries no loose deposit: cement-lined ductile iron, and the Brook Street main once PE-lined
LINED = {"T01", "T02"}
T06_LINED_FROM = dt.datetime(2026, 6, 19, 14, 0)      # UTC, phase 1 recommissioned

# ---------------------------------------------------------------- districts: key -> (code, name, junction)
DISTRICTS = {
    "D01": ("BRK111", "Copt Hill", "N1"), "D02": ("BRK118", "Market Hill", "N2"),
    "D03": ("BRK121", "Church Lane", "N2"), "D04": ("BRK134", "Ferrars", "N3"),
    "D05": ("BRK137", "St Anne's", "N3"), "D06": ("BRK142", "Mill Bridge", "N4"),
    "D07": ("BRK146", "Weir Lane", "N4"), "D08": ("BRK153", "Sallowby", "N10"),
    "D09": ("BRK155", "Sallowby Park", "N10"), "D18": ("BRK168", "Hollow Lane", "N10"),
    "D10": ("BRK172", "Eastgate", "N5"), "D11": ("BRK176", "Brook Street", "N6"),
    "D12": ("BRK179", "Tannery Yard", "N6"), "D13": ("BRK183", "Coldharbour", "N13"),
    "D14": ("BRK190", "North Lodge", "N8"), "D15": ("BRK194", "Northfield", "N8"),
    "D16": ("BRK205", "Highfield", "N9"), "D17": ("BRK209", "Pinfold", "N9"),
}
DCODE = {k: v[0] for k, v in DISTRICTS.items()}
DKEY = {v[0]: k for k, v in DISTRICTS.items()}
DNODE = {k: v[2] for k, v in DISTRICTS.items()}
# residential average draw (l/s), leakage (l/s), small non-household average (l/s)
RES = dict(D01=15.5, D02=12.0, D03=10.5, D04=9.2, D05=7.4, D06=12.6, D07=9.0, D08=11.8, D09=8.6, D18=6.9,
           D10=12.2, D11=10.4, D12=8.1, D13=5.9, D14=13.2, D15=7.3, D16=9.1, D17=5.2)
LEAK = dict(D01=3.9, D02=3.3, D03=2.7, D04=2.3, D05=2.1, D06=3.4, D07=2.5, D08=3.1, D09=2.6, D18=2.0,
            D10=3.2, D11=2.9, D12=2.4, D13=1.8, D14=3.6, D15=2.2, D16=2.7, D17=1.6)
NH_SMALL = dict(D01=1.9, D02=2.6, D03=1.2, D04=1.4, D05=0.8, D06=1.7, D07=1.1, D08=1.5, D09=1.0, D18=0.7,
                D10=1.8, D11=1.6, D12=1.3, D13=0.9, D14=1.4, D15=0.8, D16=1.1, D17=0.6)

# ---------------------------------------------------------------- time
T0 = dt.datetime(2025, 11, 1, 0, 0)          # UTC, first hour of the reference year
T1 = dt.datetime(2026, 11, 1, 0, 0)          # UTC, exclusive
BST = [(dt.datetime(2025, 3, 30, 1, 0), dt.datetime(2025, 10, 26, 1, 0)),
       (dt.datetime(2026, 3, 29, 1, 0), dt.datetime(2026, 10, 25, 1, 0)),
       (dt.datetime(2027, 3, 28, 1, 0), dt.datetime(2027, 10, 31, 1, 0))]   # UTC bounds of British Summer Time


def utc_offset_hours(t_utc):
    return 1 if any(a <= t_utc < b for a, b in BST) else 0


def to_local(t_utc):
    return t_utc + dt.timedelta(hours=utc_offset_hours(t_utc))


def to_utc(t_local):
    """Local wall time to UTC (no event is logged inside a clock change's ambiguous or missing hour)."""
    guess = t_local - dt.timedelta(hours=1)
    return guess if utc_offset_hours(guess) == 1 else t_local


PLAN_DATE = dt.date(2026, 11, 16)
WORKS = (dt.date(2027, 3, 15), dt.date(2027, 9, 15))
REPLAY = (dt.date(2026, 3, 15), dt.date(2026, 9, 15))        # the same dates a year earlier, inclusive
HEAT = [  # (first day, last day, peak amplitude, peak day) of 2026's hot spells, local dates
    (dt.date(2026, 6, 23), dt.date(2026, 6, 29), 0.09, dt.date(2026, 6, 25)),
    (dt.date(2026, 7, 15), dt.date(2026, 7, 25), 0.33, dt.date(2026, 7, 21)),
    (dt.date(2026, 8, 18), dt.date(2026, 8, 23), 0.12, dt.date(2026, 8, 20)),
]

# ---------------------------------------------------------------- the operating year's temporary arrangements
# Each: local start (the last valve that makes the arrangement), local end (the first valve that ends it), mains taken
# out, interconnectors opened, and the valve sequence the control room logged (local times).
EVENTS = [
    dict(key="nov_t06", start=dt.datetime(2025, 11, 18, 22, 58), end=dt.datetime(2025, 11, 19, 4, 5),
         out={"T06"}, open={"X05"}, job="NW/25/2291", kind="planned",
         seq=[("2025-11-18 22:35", "X05", "B", "OPEN"), ("2025-11-18 22:50", "T06", "B", "CLOSE"),
              ("2025-11-18 22:58", "T06", "A", "CLOSE"), ("2025-11-19 04:05", "T06", "A", "OPEN"),
              ("2025-11-19 04:12", "T06", "B", "OPEN"), ("2025-11-19 04:31", "X05", "B", "CLOSE")]),
    dict(key="jan_t10", start=dt.datetime(2026, 1, 13, 23, 31), end=dt.datetime(2026, 1, 14, 5, 20),
         out={"T10"}, open={"X02"}, job="NW/26/0047", kind="repair",
         seq=[("2026-01-13 23:10", "X02", "B", "OPEN"), ("2026-01-13 23:25", "T10", "A", "CLOSE"),
              ("2026-01-13 23:31", "T10", "B", "CLOSE"), ("2026-01-14 05:20", "T10", "B", "OPEN"),
              ("2026-01-14 05:27", "T10", "A", "OPEN"), ("2026-01-14 05:41", "X02", "B", "CLOSE")]),
    dict(key="phase1", start=dt.datetime(2026, 4, 13, 7, 15), end=dt.datetime(2026, 6, 19, 15, 30),
         out={"T06"}, open={"X05"}, job="CP/26/0006", kind="planned",
         seq=[("2026-04-13 06:40", "X05", "B", "OPEN"), ("2026-04-13 07:05", "T06", "A", "CLOSE"),
              ("2026-04-13 07:15", "T06", "B", "CLOSE"), ("2026-06-19 15:30", "T06", "A", "OPEN"),
              ("2026-06-19 15:41", "T06", "B", "OPEN"), ("2026-06-19 16:02", "X05", "B", "CLOSE")]),
    dict(key="june_t04", start=dt.datetime(2026, 6, 24, 5, 20), end=dt.datetime(2026, 6, 27, 3, 40),
         out={"T04"}, open={"X02"}, job="NW/26/1388", kind="planned",
         seq=[("2026-06-24 05:05", "X02", "B", "OPEN"), ("2026-06-24 05:20", "T04", "A", "CLOSE"),
              ("2026-06-24 05:32", "T04", "B", "CLOSE"), ("2026-06-27 03:40", "T04", "B", "OPEN"),
              ("2026-06-27 03:48", "T04", "A", "OPEN"), ("2026-06-27 04:06", "X02", "B", "CLOSE")]),
    dict(key="july_t04", start=dt.datetime(2026, 7, 20, 5, 9), end=dt.datetime(2026, 7, 22, 23, 35),
         out={"T04"}, open={"X07"}, job="NW/26/1702", kind="burst", dark=(dt.datetime(2026, 7, 20, 4, 52),
                                                                          dt.datetime(2026, 7, 20, 5, 9)),
         seq=[("2026-07-20 04:52", "T04", "A", "CLOSE"), ("2026-07-20 05:01", "T04", "B", "CLOSE"),
              ("2026-07-20 05:09", "X07", "B", "OPEN"), ("2026-07-22 23:35", "T04", "B", "OPEN"),
              ("2026-07-22 23:44", "T04", "A", "OPEN"), ("2026-07-22 23:58", "X07", "B", "CLOSE")]),
    dict(key="oct_t13", start=dt.datetime(2026, 10, 6, 22, 5), end=dt.datetime(2026, 10, 7, 5, 10),
         out={"T13"}, open={"X05"}, job="NW/26/2214", kind="planned",
         seq=[("2026-10-06 21:40", "X05", "B", "OPEN"), ("2026-10-06 21:55", "T13", "A", "CLOSE"),
              ("2026-10-06 22:05", "T13", "B", "CLOSE"), ("2026-10-07 05:10", "T13", "A", "OPEN"),
              ("2026-10-07 05:18", "T13", "B", "OPEN"), ("2026-10-07 05:36", "X05", "B", "CLOSE")]),
]
BURST_LOSS = (dt.datetime(2026, 7, 20, 4, 18), dt.datetime(2026, 7, 20, 4, 52), 74.0)   # local, l/s lost on TM108

# the 2027 relining arrangement: out of service, opened
PLAN_OUT = {"T03", "T10"}
PLAN_OPEN = {"X04", "X02"}

CANDIDATES = ["T05", "T13", "T08", "T09", "X02", "X04"]     # mains the relining sends more water through
GOLDEN_FLUSH = ["T13", "X04"]

# monitored district inlets (turbidity)
TURB_SITES = ["D02", "D04", "D06", "D08", "D10", "D11", "D13", "D14", "D16"]

# ---------------------------------------------------------------- the ask records
PROGRAMME = (dt.date(2025, 9, 1), dt.date(2026, 3, 27))
ASK_YEARS = (2025, 2026)
DIAMETERS = (75, 100, 150, 225, 300)
CREW_DIST, CREW_TRUNK = "C14", "C22"
RUNNING_FROM = dt.date(2025, 12, 1)        # crew C14 books its meter display from this night on
REROUTED = ["D04", "D05", "D06", "D07", "D08", "D09", "D18"]
ASK_B_WINDOW = ("2025-11", "2026-10")
