"""The designed long waits: every wait inside the remit, by trust and four-quarter year, plus the
legacy rows that carry the ask devices. Counts here are the design note's targets; the generator
places them on the clock in world.py and every figure is recomputed from the shipped files.

A wait is a dict with: letter, year, cls ('cap' | 'own' | 'alloc'), died (death within 30 days of the
decision), golden (inside the remit), tags (device membership), outcome ('admitted' | 'died_waiting'),
and per-tag timing needs. A patient with two waits (DV2b) carries the same 'pid' on both.
"""
from common import LETTERS

# golden targets per four-quarter year: (patients, deaths, confirmable)
TARGETS = {
    1: {"A": (140, 40, 3), "B": (33, 9, 0), "C": (114, 34, 3), "D": (90, 25, 25), "E": (178, 53, 0),
        "F": (47, 13, 6), "G": (68, 22, 14), "H": (25, 8, 3)},
    2: {"A": (148, 42, 3), "B": (35, 10, 0), "C": (119, 35, 2), "D": (93, 28, 28), "E": (191, 56, 0),
        "F": (47, 14, 0), "G": (79, 20, 17), "H": (25, 7, 0)},
    3: {"A": (150, 44, 2), "B": (36, 10, 0), "C": (118, 35, 0), "D": (92, 27, 27), "E": (190, 56, 0),
        "F": (46, 13, 0), "G": (74, 21, 15), "H": (25, 7, 0)},
}

# class composition per trust-year: cls -> (waits, deaths). Every patient here holds one wait; DV2b
# patients add a second wait below, so waits exceed patients by one per DV2b patient.
COMPOSITION = {
    1: {"A": {"own": (3, 1), "alloc": (5, 2), "cap": (132, 37)},
        "B": {"cap": (33, 9)},
        "C": {"alloc": (8, 3), "cap": (106, 31)},
        "D": {"alloc": (90, 25)},
        "E": {"cap": (178, 53)},
        "F": {"own": (20, 6), "cap": (27, 7)},
        "G": {"alloc": (3, 1), "own": (45, 13), "cap": (20, 8)},
        "H": {"own": (10, 3), "cap": (15, 5)}},
    2: {"A": {"own": (10, 3), "cap": (138, 39)},
        "B": {"cap": (35, 10)},
        "C": {"own": (3, 1), "alloc": (3, 1), "cap": (113, 33)},
        "D": {"alloc": (93, 28)},
        "E": {"cap": (191, 56)},
        "F": {"cap": (47, 14)},
        "G": {"own": (59, 17), "cap": (20, 3)},
        "H": {"cap": (25, 7)}},
    3: {"A": {"own": (7, 2), "cap": (143, 42)},
        "B": {"cap": (36, 10)},
        "C": {"cap": (118, 35)},
        "D": {"alloc": (92, 27)},
        "E": {"cap": (190, 56)},
        "F": {"cap": (46, 13)},
        "G": {"own": (52, 15), "cap": (22, 6)},
        "H": {"cap": (25, 7)}},
}

# designed rows inside the golden population (all in the legacy months, year 1). Each entry:
# (tag, letter, cls, died, count)
GOLDEN_DEVICE_ROWS = [
    # DV9: a temporary identity the links never resolve; the patient died in hospital, so the death is on the
    # temporary-key spell's discharge method only (no date of death anywhere)
    ("DV9", "A", "cap", True, 1), ("DV9", "B", "cap", True, 1), ("DV9", "C", "cap", True, 1),
    ("DV9", "D", "alloc", True, 1), ("DV9", "E", "cap", True, 3), ("DV9", "F", "cap", True, 1),
    ("DV9", "G", "alloc", True, 1), ("DV9", "H", "cap", True, 1),
    # DV2b: temporary identity on the first long wait, a second long wait months later under the verified key
    ("DV2b", "A", "cap", False, 1), ("DV2b", "B", "cap", False, 1), ("DV2b", "C", "cap", False, 1),
    ("DV2b", "D", "alloc", False, 1), ("DV2b", "E", "cap", False, 2), ("DV2b", "F", "cap", False, 1),
    ("DV2b", "G", "cap", False, 1), ("DV2b", "H", "cap", False, 1),
    # HZ1: a planned patient moved between beds inside a capacity wait (legacy bed-episode rows)
    ("HZ1", "A", "cap", True, 2), ("HZ1", "C", "cap", True, 2), ("HZ1", "G", "cap", True, 4),
    # HZ1oc: an allocation wait whose planned admission is the readmission of a patient discharged
    # from the same unit hours earlier
    ("HZ1oc", "A", "alloc", True, 1), ("HZ1oc", "C", "alloc", True, 1),
    # HZ2: pilot-ward referrals entered on both systems during the parallel run
    ("HZ2", "A", "cap", True, 2), ("HZ2", "B", "cap", True, 2), ("HZ2", "C", "cap", True, 2),
    ("HZ2", "D", "alloc", True, 4), ("HZ2", "E", "cap", True, 2), ("HZ2", "F", "cap", True, 2),
    ("HZ2", "G", "cap", True, 2), ("HZ2", "H", "cap", True, 2),
    ("HZ2", "A", "cap", False, 1), ("HZ2", "E", "cap", False, 2), ("HZ2", "D", "alloc", False, 1),
    ("HZ2", "C", "cap", False, 1),
    # HZ2oc: a genuine second referral on the same day after a stand-down
    ("HZ2oc", "A", "cap", True, 1), ("HZ2oc", "B", "cap", False, 1), ("HZ2oc", "C", "cap", False, 1),
    ("HZ2oc", "E", "cap", True, 1), ("HZ2oc", "E", "cap", False, 1), ("HZ2oc", "G", "cap", False, 1),
    # DV1rc: a capacity wait in the summer legacy months with a planned admission in the hour before it
    ("DV1rc", "A", "cap", True, 2), ("DV1rc", "G", "cap", True, 2),
    # DV1oc: winter legacy waits between 4h10 and 4h50 (a blanket one-hour shift drops them)
    ("DV1oc", "A", "cap", True, 1), ("DV1oc", "A", "cap", False, 1), ("DV1oc", "B", "cap", False, 1),
    ("DV1oc", "C", "cap", False, 1), ("DV1oc", "D", "alloc", True, 1), ("DV1oc", "E", "cap", True, 1),
    ("DV1oc", "E", "cap", False, 2), ("DV1oc", "G", "cap", False, 1),
    # DV4oc: legacy level-3 waits whose level history records a change (escalation, or a step-down after)
    ("DV4oc", "A", "cap", True, 1), ("DV4oc", "A", "cap", False, 1), ("DV4oc", "B", "cap", True, 1),
    ("DV4oc", "C", "cap", False, 1), ("DV4oc", "D", "alloc", False, 1), ("DV4oc", "E", "cap", True, 1),
    ("DV4oc", "E", "cap", False, 1), ("DV4oc", "F", "cap", False, 1), ("DV4oc", "G", "cap", False, 1),
]

# designed rows outside the golden population (legacy months)
# DV4: requested level 3, decided level 2, waited over four hours, died within 30 days
DV4_ROWS = {"A": "cap", "B": "dw", "C": "cap", "D": "alloc", "E": "dw", "F": "cap", "G": "cap", "H": "own_dw"}
# DV1 spurious: true waits of 3h10 to 3h50 in the summer legacy months that read as long on the UTC clock.
# (letter, kind, died): kind 'empty' = own unit held an empty bed from an hour before the decision;
# 'planned' = a planned admission to the own unit in the hour before the decision; 'any' = no own-unit event
DV1_SPURIOUS = [("A", "empty", True), ("A", "planned", True), ("A", "any", False), ("A", "any", False),
                ("B", "any", True), ("B", "any", True), ("C", "empty", True), ("C", "planned", True),
                ("D", "planned", True), ("D", "planned", True), ("E", "any", True), ("E", "any", True),
                ("E", "any", False), ("E", "any", False), ("F", "empty", True), ("F", "empty", True),
                ("G", "empty", True), ("G", "empty", True), ("H", "any", True), ("H", "any", True)]

# bureau transfers admitted to the referring trust's own full unit inside its capacity waits, per year and
# trust: (waits ending in a death, waits survived). Untagged capacity waits only. The year-3 deaths at C sit
# on days C's own 08:00 return showed a vacancy.
TX_INSIDE = {1: {"A": (24, 74), "C": (6, 16), "G": (0, 2), "F": (3, 6)},
             2: {"A": (32, 80), "C": (6, 16), "G": (1, 3)},
             3: {"A": (35, 82), "C": (6, 17), "G": (2, 4)}}

# DV5: waits across the spring clock change, 3h10 to 3h50 elapsed and 4h10 to 4h50 on the wall clock. The
# decision falls on the evening before the change. kind: 'own' an empty staffed bed at the own unit from before
# the decision to the bed; 'cap' the own unit full; 'none' no own level-3 unit (admitted elsewhere).
DV5_NIGHTS = {
    "2024-03-30": [("A", "cap", True), ("B", "none", False), ("C", "cap", True), ("D", "own", True),
                   ("D", "own", True), ("E", "none", True), ("F", "own", True), ("F", "own", True), ("G", "cap", True),
                   ("H", "own", True), ("H", "own", True)],
    "2025-03-29": [("A", "cap", True), ("B", "none", False), ("C", "cap", True), ("D", "own", True),
                   ("D", "own", True), ("E", "none", True), ("F", "none", False), ("G", "cap", True), ("H", "none", True)],
}
# tagged capacity waits that also carry a bureau transfer inside: (year, letter, tag) -> deaths
TX_TAGGED = {(1, "G", "HZ2"): 2}
# the bureau's placements inside A's waits: a planned post-operative transfer (03) from a trust without level-3 beds,
# referred after A's waiting patient, on every death-wait and on every other survivor wait; unplanned (02), referred
# before, on the rest and at C, F and G. Year-1 transfers inside waits sit in the legacy months (the held-bed device).
TX_PLANNED_LETTERS = "A"
PLANNED_TX_DTA = (18 * 60 + 45, 20 * 60 + 10)     # A's waiting patient's decision on a list-day evening
PLANNED_TX_LATEST = 22 * 60 + 10                 # the planned transfer's bed by 22:10

# DV8: legacy transfers between trusts, whose bed the bureau allocated (bed_confirmed_at) before the patient arrived;
# the legacy feed dates the stay from the arrival. Near misses: allocation wait 3h10 to 3h52, arrival past 4h15.
# (letter, died) rows in the winter legacy months (GMT, so the UTC device cannot touch them).
DV8_NEAR = [("E", True), ("E", True), ("E", False), ("E", False), ("B", True), ("B", False), ("H", True), ("H", False)]
DV8_ALLOC_WAIT = (190, 232)
DV8_PLACED_MIN = 255
TRANSIT = (40, 110)                              # legacy transfer: minutes from allocation to arrival
LEGACY_TX_MAX_WAIT = 190                         # every other legacy transfer: allocation wait <= 3h10
LEGACY_TX_MAX_PLACED = 232                       # and arrival inside 3h52 of the decision

# Stennock's elective centre: its planned post-operative patients come to STN-ACC as planned transfers in (03),
# referred from the centre's recovery 10 to 90 minutes before the bed
EC_WAIT = (10, 90)

# DV7: genuine repeat patients, two long waits under one verified key at one trust, both in year 2: discharged
# alive from the first stay, referred again 8 to 13 days after the first decision, dead after the second stay.
DV7_PER_TRUST = 2
# not at D: every D long wait is confirmable, and a pair there moves the confirmable total onto a cancellation
DV7_TRUSTS = "ABCEFGH"

# deaths before a bed was assigned among the golden waits, by year (others die after admission)
DIED_WAITING = {3: {"E": 10, "A": 3, "C": 2, "B": 2, "F": 2, "H": 1},
                2: {"E": 9, "A": 3, "C": 2, "B": 1, "F": 2, "H": 1},
                1: {"E": 8, "A": 2, "C": 1, "B": 1, "H": 1}}

# rung-2 and 08:00-network targets for year 3 (deaths on days with an 08:00 vacancy)
Y3_C_VAC_DEATHS = 34          # of C's 35 deaths, on days C's own 08:00 return showed an empty bed
Y3_E_VAC_DEATHS = 21          # of E's 56, on days any unit's 08:00 return showed an empty bed
Y3_A_VAC_DEATHS_MAX = 16      # of A's 44
Y3_G_OWNVAC_DEATHS = 4        # of G's 15 own-empty deaths, on days G's own 08:00 return showed a vacancy


def check_tables():
    for y in (1, 2, 3):
        for L in LETTERS:
            comp = COMPOSITION[y][L]
            pats = sum(v[0] for v in comp.values())
            deaths = sum(v[1] for v in comp.values())
            conf = sum(v[1] for k, v in comp.items() if k in ("own", "alloc"))
            assert (pats, deaths, conf) == TARGETS[y][L], (y, L, pats, deaths, conf, TARGETS[y][L])
    tot = {y: tuple(sum(TARGETS[y][L][i] for L in LETTERS) for i in range(3)) for y in (1, 2, 3)}
    assert tot == {1: (695, 204, 54), 2: (737, 212, 50), 3: (731, 213, 44)}, tot
    rec = {L: tuple(sum(TARGETS[y][L][i] for y in (1, 2, 3)) for i in range(3)) for L in LETTERS}
    assert rec == {"A": (438, 126, 8), "B": (104, 29, 0), "C": (351, 104, 5), "D": (275, 80, 80),
                   "E": (559, 165, 0), "F": (140, 40, 6), "G": (221, 63, 46), "H": (75, 22, 3)}, rec
    return tot, rec
