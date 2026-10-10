"""The fourteen watch-list sections, built forward from the 30 June 2026 holdings.

Every figure the pack reports is computed from the records these specs produce; nothing here is a
reported number. Holder ids are symbolic and mapped to registered names and NIFs in world.py.

hold      holder -> large-holder dwellings in the section on 30 June 2026 (conformed)
carried   holders whose 30 June 2026 picture stands on a return lodged before 1 April 2026
          (no-change rule), each with the number of buildings their dwellings sit in
crow      the holder whose latest 2026T2 lodgement is a complementary return, and how many of its
          section rows the complementary return carries (the rest sit in the original)
oprs      option and reservation rows lodged in the section on 2026T2 returns
mal       malformed cadastral references among the section's 2026T2 dwelling rows
flows     ('deed', month, seller, n, scheduled) sale to private buyers executed in Jul to Sep 2026
          ('buy', month, buyer, n) purchase from small owners executed in Jul to Sep 2026
          ('swap', month, seller, n, buyer, scheduled) sale between large holders in Jul to Sep 2026
          ('sched', agreed_date, seller, n, buyer) agreement in force on 30 June 2026, completing as
                agreed after 30 September (buyer 'private' or a holder id)
          ('tk', case, seller, n, buyer, commit_dates, agreed_date) agreement in force on 30 June
                2026 that the agency has committed to buy (buyer 'private' or a holder id)
vac       (empty with nobody registered, empty with only lapsed registrations) among the section's
          large-holder dwellings on 1 January 2027
"""
from common import D

# case codes for the agency's commitments: agreed before or after 1 Jan 2027, completion
# (commitment + 120 days) before or after, agreed buyer a large holder or not
CASES = {"c1": ("before", "before", "lh"), "c2": ("before", "before", "private"),
         "c3": ("before", "after", "lh"), "c4": ("before", "after", "private"),
         "c5": ("after", "before", "lh"), "c6": ("after", "before", "private"),
         "c7": ("after", "after", "private")}

Q_COMMITS = [D(2026, 9, 15), D(2026, 9, 15), D(2026, 9, 16), D(2026, 9, 16), D(2026, 9, 17),
             D(2026, 9, 17), D(2026, 9, 21), D(2026, 9, 21), D(2026, 9, 22), D(2026, 9, 22),
             D(2026, 9, 23), D(2026, 9, 23), D(2026, 9, 24), D(2026, 9, 24)]
Q_AGREED = [D(2026, 12, 10), D(2026, 12, 10), D(2026, 12, 2), D(2026, 12, 3), D(2026, 12, 4),
            D(2026, 12, 9), D(2026, 12, 11), D(2026, 12, 14), D(2026, 12, 15), D(2026, 12, 16),
            D(2026, 12, 17), D(2026, 12, 1), D(2026, 12, 18), D(2026, 12, 16)]
TWIN_DATE, TWIN_PRICE = D(2026, 12, 10), 128000

SECTIONS = [
    dict(code="4625001005", role="A1", N=812, dist="01", street="Ciutat Vella",
         hold={"G1a": 50, "G1b": 22, "X1": 14, "G2a": 45, "G2b": 15, "sA1a": 8, "sA1b": 6, "sA1c": 7,
               "CAR1": 40, "sA1d": 18, "sA1e": 16, "sA1f": 12, "sA1g": 10},
         carried={"CAR1": 4}, crow=("sA1d", 8), oprs=3, mal=2,
         flows=[("swap", 8, "sA1f", 4, "G1b", True), ("deed", 7, "G1a", 1, True), ("deed", 9, "G2a", 1, True),
                ("sched", D(2026, 11, 12), "sA1e", 1, "private"),
                ("tk", "c5", "sA1a", 3, "sA1b", [D(2026, 7, 14)] * 3, D(2027, 3, 10)),
                ("tk", "c2", "sA1c", 2, "private", [D(2026, 8, 4)] * 2, D(2026, 12, 14))],
         vac=(11, 3)),
    dict(code="4625002007", role="A2", N=689, dist="02",
         hold={"G3a": 58, "X2": 12, "G4a": 38, "G4c": 10, "sA2a": 9, "sA2b": 6, "CAR2": 30,
               "sA2c": 35, "sA2d": 7},
         carried={"CAR2": 3}, crow=("sA2c", 5), oprs=2, mal=1,
         flows=[("swap", 7, "sA2c", 4, "G3a", False), ("deed", 8, "G4a", 1, False), ("deed", 9, "G3a", 1, True),
                ("sched", D(2026, 12, 7), "sA2d", 1, "private"),
                ("tk", "c4", "sA2a", 3, "private", [D(2026, 9, 22)] * 3, D(2026, 12, 9)),
                ("tk", "c7", "sA2b", 1, "private", [D(2026, 9, 29)], D(2027, 3, 16))],
         vac=(7, 2)),
    dict(code="4625011004", role="A3", N=931, dist="11",
         hold={"G1a": 70, "X1": 20, "G1b": 15, "G5a": 50, "G5b": 18, "sA3a": 10, "sA3b": 8,
               "sA3c": 9, "sA3d": 6, "CAR3": 50, "sA3e": 22, "sA3f": 18, "sA3g": 20},
         carried={"CAR3": 5}, crow=("sA3e", 10), oprs=4, mal=3,
         flows=[("swap", 9, "sA3g", 4, "G1b", True), ("deed", 7, "G5a", 1, True), ("deed", 8, "G1a", 1, False),
                ("sched", D(2026, 10, 21), "sA3f", 1, "private"),
                ("tk", "c1", "sA3a", 3, "sA3b", [D(2026, 7, 21)] * 3, D(2026, 11, 10)),
                ("tk", "c3", "sA3c", 2, "sA3d", [D(2026, 9, 16)] * 2, D(2026, 11, 25))],
         vac=(14, 3)),
    dict(code="0301401008", role="A4", N=561, dist="01",
         hold={"G6a": 40, "X3": 15, "G7a": 30, "sA4a": 9, "CAR4": 12, "sA4c": 20, "sA4d": 18,
               "sA4e": 10, "sA4f": 8},
         carried={"CAR4": 2}, crow=None, oprs=3, mal=1,
         flows=[("swap", 7, "sA4c", 4, "G6a", True), ("deed", 8, "G6a", 1, True), ("sched", D(2026, 11, 19), "sA4d", 1, "private"),
                ("tk", "c6", "sA4a", 3, "private", [D(2026, 7, 28)] * 3, D(2027, 3, 2))],
         vac=(6, 2)),
    dict(code="4625001012", role="P", N=757, dist="01",
         hold={"G2a": 60, "G2b": 12, "G8a": 40, "sPa": 22, "sPb": 10, "CAR5": 8, "sPc": 15,
               "sPd": 12, "sPe": 10, "sPf": 9, "sPg": 7},
         carried={"CAR5": 1}, crow=None, oprs=4, mal=1,
         flows=[("swap", 8, "sPd", 4, "G2b", False), ("deed", 7, "G2a", 1, True), ("sched", D(2026, 10, 15), "sPc", 1, "private"),
                ("tk", "c5", "sPa", 20, "sPb", [D(2026, 7, 9)] * 20, D(2027, 2, 16))],
         vac=(9, 2)),
    dict(code="4625011016", role="S", N=641, dist="11",
         hold={"G5a": 35, "G5b": 10, "G9a": 20, "G9b": 8, "Y1": 22, "X5": 4, "sSa": 19, "sSb": 6,
               "CAR6": 25, "sSc": 9, "sSd": 11},
         carried={"Y1": 2, "CAR6": 3}, crow=("sSc", 0), oprs=2, mal=1,
         flows=[("swap", 7, "sSd", 4, "G5b", True), ("deed", 8, "G5a", 1, True), ("sched", D(2026, 11, 26), "sSd", 1, "private"),
                ("tk", "c1", "sSa", 17, "sSb", [D(2026, 8, 5)] * 17, D(2026, 11, 19))],
         vac=(5, 2)),
    dict(code="0301402014", role="Q", N=603, dist="02",
         hold={"G1c": 30, "X1": 8, "G7a": 32, "sQa": 24, "sQb": 12, "CAR7": 12, "sQc": 14,
               "sQd": 18, "sQe": 15},
         carried={"CAR7": 2}, crow=("sQc", 4), oprs=4, mal=5,
         flows=[("deed", 7, "sQb", 2, True), ("deed", 8, "sQb", 2, False), ("deed", 9, "sQb", 2, True),
                ("sched", D(2026, 12, 1), "sQa", 1, "private"), ("sched", D(2026, 12, 3), "sQa", 1, "private"),
                ("sched", D(2026, 12, 15), "sQa", 1, "private"), ("sched", D(2026, 12, 17), "sQa", 1, "private"),
                ("tk", "c4", "sQa", 14, "private", Q_COMMITS, None)],
         vac=(7, 2)),
    dict(code="4625002019", role="T", N=722, dist="02",
         hold={"G4a": 45, "G4b": 20, "X2": 10, "G3b": 40, "sTa": 8, "sTb": 5, "sQa": 6, "sTc": 18,
               "sTd": 15, "sTe": 12, "sTf": 8},
         carried={"G4b": 2, "G3b": 4}, crow=None, oprs=1, mal=2,
         flows=[("deed", 7, "G4a", 6, True), ("deed", 8, "G4a", 7, True), ("deed", 9, "G4a", 6, False),
                ("sched", TWIN_DATE, "sQa", 2, "private"),
                ("tk", "c1", "sTa", 3, "sTb", [D(2026, 7, 7)] * 3, D(2026, 10, 22))],
         vac=(9, 3)),
    dict(code="4625012009", role="U", N=538, dist="12",
         hold={"G9a": 30, "G9b": 6, "G10a": 20, "G10b": 6, "Y1": 10, "Y2": 8, "X5": 5, "sUa": 7,
               "sUb": 12, "sUc": 9, "sUd": 13},
         carried={"Y1": 1, "Y2": 1}, crow=("sUc", 6), oprs=1, mal=1,
         flows=[("buy", 8, "G9a", 18), ("tk", "c6", "sUa", 3, "private", [D(2026, 8, 18)] * 3, D(2027, 2, 9))],
         vac=(11, 2)),
    dict(code="4625005013", role="O1", N=879, dist="05",
         hold={"G8a": 34, "G8b": 10, "G9a": 30, "Y1": 20, "sO1a": 9, "sO1b": 7, "sO1c": 14,
               "sO1d": 12, "sO1e": 16, "sO1f": 13, "sO1g": 12, "sO1h": 11},
         carried={"Y1": 2}, crow=("sO1d", 6), oprs=4, mal=2,
         flows=[("swap", 9, "sO1c", 4, "G8b", True), ("deed", 8, "G8a", 1, True), ("sched", D(2026, 12, 2), "sO1e", 1, "private"),
                ("tk", "c5", "sO1a", 3, "sO1b", [D(2026, 8, 11)] * 3, D(2027, 2, 24))],
         vac=(7, 3)),
    dict(code="4625013021", role="O2", N=748, dist="13",
         hold={"G10a": 35, "G10b": 10, "G5b": 25, "Y2": 15, "sO2a": 8, "sO2b": 12, "sO2c": 10,
               "sO2d": 14, "sO2e": 11, "sO2f": 11},
         carried={"Y2": 2}, crow=("sO2c", 5), oprs=2, mal=1,
         flows=[("swap", 8, "sO2b", 4, "G10b", False), ("deed", 7, "G10a", 1, True), ("sched", D(2026, 11, 4), "sO2d", 1, "private"),
                ("tk", "c4", "sO2a", 3, "private", [D(2026, 9, 28)] * 3, D(2026, 12, 3))],
         vac=(4, 2)),
    dict(code="0301405003", role="O3", N=612, dist="05",
         hold={"G6a": 28, "X3": 12, "G10c": 22, "Y2": 10, "sO3a": 9, "sO3b": 6, "CAR8": 8,
               "sO3c": 9, "sO3d": 10},
         carried={"Y2": 1, "CAR8": 1}, crow=("sO3d", 6), oprs=1, mal=1,
         flows=[("deed", 9, "sO3c", 1, True),
                ("tk", "c1", "sO3a", 4, "sO3b", [D(2026, 8, 6)] * 4, D(2026, 11, 5))],
         vac=(3, 2)),
    dict(code="1204001006", role="O4", N=688, dist="01",
         hold={"G12a": 40, "X4": 14, "G13a": 30, "OPH": 10, "CAR9": 10, "sO4a": 15, "sO4b": 12,
               "sO4c": 13, "sO4d": 12},
         carried={"CAR9": 1}, crow=("sO4b", 8), oprs=34, mal=1,
         flows=[("deed", 8, "sO4a", 1, True), ("sched", D(2026, 12, 9), "sO4c", 1, "private")],
         vac=(9, 0)),
    dict(code="1204003011", role="O5", N=516, dist="03",
         hold={"G13a": 25, "G12a": 12, "X4": 14, "CAR10": 8, "sO5a": 12, "sO5b": 10, "sO5c": 12},
         carried={"CAR10": 1}, crow=("sO5b", 7), oprs=2, mal=1,
         flows=[("sched", D(2026, 11, 18), "sO5c", 1, "private")],
         vac=(6, 0)),
]

ROLE = {s["role"]: s for s in SECTIONS}
MUNI = {"46250": ("València", "46"), "03014": ("Alacant", "03"), "12040": ("Castelló de la Plana", "12")}

# the agency's commitments outside the large holders' scheduled sales (small owners), and its
# settled first-offer purchases (committed January to May 2026, deeds May to September 2026)
SETTLED_COMMITS = [D(2026, 1, 13), D(2026, 1, 21), D(2026, 1, 28), D(2026, 2, 10), D(2026, 2, 17),
                   D(2026, 3, 3), D(2026, 3, 10), D(2026, 3, 17), D(2026, 3, 24), D(2026, 3, 31),
                   D(2026, 4, 7), D(2026, 4, 14), D(2026, 4, 15), D(2026, 4, 21), D(2026, 4, 28),
                   D(2026, 4, 29), D(2026, 5, 5), D(2026, 5, 6), D(2026, 5, 12), D(2026, 5, 13),
                   D(2026, 5, 19), D(2026, 5, 20), D(2026, 5, 21)]

# four more settled first-offer purchases of privately owned dwellings whose notified deed date lay
# beyond commitment plus 120 days: the agency still executed on day 120, before the date the parties
# had agreed (deeds July to September 2026)
SETTLED_EARLY = [D(2026, 3, 12), D(2026, 4, 2), D(2026, 4, 23), D(2026, 5, 14)]

# holders inscribed in the register after 30 June 2026, with no return lodged by the extract: their
# watch-list dwellings, all bought from private owners between July 2024 and June 2026 (never in July
# to December 2025 and never after 30 June 2026), and the inscription day
REGISTRANTS = [
    dict(key="RX", name="Habitatges Cornisa SL", prov="46", inscribed=D(2026, 9, 17),
         holds={"4625011016": 18}, early=5),
    dict(key="RW", name="Pòrtic Residencial SL", prov="46", inscribed=D(2026, 7, 23),
         holds={"4625001005": 5, "4625013021": 6}, early=4),
    dict(key="RV", name="Inversions Mènsula SL", prov="03", inscribed=D(2026, 8, 27), holds={}, early=0),
    dict(key="RZ", name="Riostra Lloguers SL", prov="12", inscribed=D(2026, 7, 9), holds={}, early=0),
]
