"""Field visit history, the appeals register and the Q1 2027 rota.

These carry the two supplementary asks (confirmation history by patch, field capacity by patch).
None of their rows enters the referral screen, which reads only the meter, register, occupier,
heating-measure and degree-day files.
"""
import datetime as dt
import numpy as np
import world as W

MIGRATION_CUTOVER = dt.date(2024, 11, 18)     # FieldOps live; FieldLink read-only from this date
BACKLOAD_FROM = dt.date(2024, 11, 4)          # FieldLink jobs from this date were re-keyed into FieldOps
WINTERS = [(dt.date(2023, 10, 1), dt.date(2024, 3, 31), "2023/24"),
           (dt.date(2024, 10, 1), dt.date(2025, 3, 31), "2024/25"),
           (dt.date(2025, 10, 1), dt.date(2026, 3, 31), "2025/26")]

# per patch: access visits per winter, standing confirmations per winter, overturned on appeal per
# winter, no-access visits per winter (each followed by a revisit that is itself counted above)
HISTORY = {
    #        access          confirmed(standing)  overturned   noaccess
    "INV": ((22, 21, 21), (9, 8, 9),   (1, 1, 1), (4, 3, 4)),
    "NRN": ((12, 13, 13), (7, 8, 7),   (0, 1, 0), (2, 2, 1)),
    "FRS": ((10, 9, 11),  (5, 4, 5),   (1, 0, 1), (1, 2, 1)),
    "ELG": ((24, 23, 24), (13, 12, 12), (1, 2, 1), (4, 4, 3)),
    "SPY": ((11, 11, 11), (5, 5, 5),   (1, 1, 0), (2, 1, 2)),
    "LOC": ((7, 8, 7),    (5, 5, 5),   (2, 1, 2), (1, 1, 1)),
    "CAI": ((13, 14, 14), (6, 5, 6),   (1, 1, 1), (2, 3, 2)),
    "SKY": ((10, 9, 10),  (4, 5, 4),   (1, 1, 1), (2, 1, 2)),
}
OFF_SEASON_VISITS = {"INV": 9, "NRN": 4, "FRS": 4, "ELG": 10, "SPY": 5, "LOC": 3, "CAI": 6, "SKY": 4}

OFFICERS_HIST = ["Alan Khan", "Aaron O'Connor", "Jonathan Gibson", "Debra Martin"]


def _rand_day(rng, a, b, weekday_only=True):
    while True:
        d = a + dt.timedelta(int(rng.integers(0, (b - a).days + 1)))
        if not weekday_only or d.weekday() < 5:
            return d


def build_history(world, rng):
    prem_by_patch = {}
    for p in world["premises"]:
        if p["role"] == "ordinary" and not p["prepay"]:
            prem_by_patch.setdefault(p["patch"], []).append(p)
    visits = []          # one dict per real visit, truth
    job_seq = iter(range(318_400, 399_999, 7))
    new_seq = iter(range(1_002_215, 1_999_999, 13))
    for code, (acc, conf, over, noacc) in HISTORY.items():
        pool = prem_by_patch[code]
        rng.shuffle(pool)
        pi = 0
        for wi, (a, b, label) in enumerate(WINTERS):
            # in 2024/25, force some visits into the migration backload fortnight so they are re-keyed
            n_dup = {"INV": 3, "NRN": 4, "FRS": 1, "ELG": 3, "SPY": 2, "LOC": 2, "CAI": 2, "SKY": 1}[code] if wi == 1 else 0
            outcomes = (["CONF"] * conf[wi] + ["CONF_OVER"] * over[wi] +
                        ["NFF"] * (acc[wi] - conf[wi] - over[wi]))
            rng.shuffle(outcomes)
            for k, oc in enumerate(outcomes):
                prem = pool[pi]; pi += 1
                if k < n_dup:
                    d = _rand_day(rng, BACKLOAD_FROM, MIGRATION_CUTOVER - dt.timedelta(1))
                else:
                    d = _rand_day(rng, a + dt.timedelta(3), b - dt.timedelta(3))
                visits.append({"patch": code, "prem": prem, "date": d, "outcome": oc,
                               "winter": label})
            for k in range(noacc[wi]):
                # a no-access attempt on a premises later visited with access in the same winter
                tgt = [v for v in visits if v["patch"] == code and v["winter"] == label][k]
                d0 = tgt["date"] - dt.timedelta(int(rng.integers(5, 16)))
                if d0.weekday() >= 5:
                    d0 -= dt.timedelta(d0.weekday() - 4)
                if d0 < a:
                    d0 = a + dt.timedelta(2)
                visits.append({"patch": code, "prem": tgt["prem"], "date": d0, "outcome": "NOACC",
                               "winter": label})
        # off-season visits (April to September, and October-November 2026), outside every winter
        for k in range(OFF_SEASON_VISITS[code]):
            prem = pool[pi]; pi += 1
            yr = [2024, 2025, 2026][k % 3]
            d = _rand_day(rng, dt.date(yr, 4, 8), dt.date(yr, 9, 24))
            visits.append({"patch": code, "prem": prem, "date": d,
                           "outcome": ["NFF", "CONF", "NFF"][k % 3], "winter": None})
        for k in range(2):
            prem = pool[pi]; pi += 1
            d = _rand_day(rng, dt.date(2026, 10, 5), dt.date(2026, 11, 27))
            visits.append({"patch": code, "prem": prem, "date": d, "outcome": "NFF",
                           "winter": None})
    visits.sort(key=lambda v: (v["date"], v["prem"]["uprn"]))
    for v in visits:
        v["officer"] = OFFICERS_HIST[int(rng.integers(0, len(OFFICERS_HIST)))]
        v["assessed"] = (round(float(rng.uniform(380, 4200)), 0)
                         if v["outcome"] in ("CONF", "CONF_OVER") else None)
        if v["date"] < MIGRATION_CUTOVER:
            v["legacy_job"] = f"FL{next(job_seq):06d}"
        if v["date"] >= BACKLOAD_FROM:
            v["new_job"] = f"FO-{next(new_seq):07d}"
        v["mpan"] = v["prem"]["supplies"][0]["mpan"]
        # historical diversions leave their trace in the recorded consumption up to the visit
        if v["outcome"] in ("CONF", "CONF_OVER"):
            v["div_weeks"] = int(rng.integers(6, 21))
            v["div_f"] = float(rng.uniform(0.35, 0.55))
    return visits


def apply_history_to_consumption(world, visits):
    import sim
    for v in visits:
        if v["outcome"] not in ("CONF", "CONF_OVER") or v["outcome"] == "CONF_OVER":
            continue
        b = sim.day_index(v["date"])
        a = b - 7 * v["div_weeks"]
        if b <= 0:
            continue
        a = max(a, 0)
        s = v["prem"]["supplies"][0]
        s["kwh"] = s["kwh"].copy()
        s["kwh"][a:b] = np.round(s["kwh"][a:b] * (1 - v["div_f"]), 3)


# Q1 2027 rota -------------------------------------------------------------------------------
Q1 = (dt.date(2027, 1, 1), dt.date(2027, 3, 31))
HOLIDAYS = [  # (date, name, region)
    (dt.date(2027, 1, 1), "New Year's Day", "England and Wales"),
    (dt.date(2027, 3, 26), "Good Friday", "England and Wales"),
    (dt.date(2027, 3, 29), "Easter Monday", "England and Wales"),
    (dt.date(2027, 1, 1), "New Year's Day", "Scotland"),
    (dt.date(2027, 1, 4), "2nd January (substitute day)", "Scotland"),
    (dt.date(2027, 3, 26), "Good Friday", "Scotland"),
]
TEAM = [  # name, grade, field start date
    ("Matthew Gill", "Senior Revenue Protection Officer", dt.date(2024, 5, 13)),
    ("Aaron O'Connor", "Revenue Protection Officer", dt.date(2023, 2, 6)),
    ("Chloe Lewis", "Revenue Protection Officer", dt.date(2027, 2, 15)),
]
LEAVE = [  # name, date, code
    ("Matthew Gill", dt.date(2027, 1, 5), "AL"), ("Matthew Gill", dt.date(2027, 1, 6), "AL"),
    ("Matthew Gill", dt.date(2027, 2, 22), "TRN"), ("Matthew Gill", dt.date(2027, 1, 4), "AL"),
    ("Matthew Gill", dt.date(2027, 3, 30), "AL"), ("Matthew Gill", dt.date(2027, 3, 31), "AL"),
    ("Aaron O'Connor", dt.date(2027, 1, 4), "AL"), ("Aaron O'Connor", dt.date(2027, 2, 8), "AL"),
    ("Aaron O'Connor", dt.date(2027, 2, 9), "AL"), ("Aaron O'Connor", dt.date(2027, 2, 10), "AL"),
    ("Aaron O'Connor", dt.date(2027, 2, 11), "AL"), ("Aaron O'Connor", dt.date(2027, 2, 12), "AL"),
    ("Aaron O'Connor", dt.date(2027, 2, 22), "TRN"), ("Aaron O'Connor", dt.date(2027, 3, 29), "AL"),
    ("Chloe Lewis", dt.date(2027, 2, 15), "IND"), ("Chloe Lewis", dt.date(2027, 2, 16), "IND"),
    ("Chloe Lewis", dt.date(2027, 2, 17), "IND"), ("Chloe Lewis", dt.date(2027, 2, 22), "TRN"),
    ("Chloe Lewis", dt.date(2027, 3, 12), "STBY"),
]
# field working standard FW-3
SHIFT_MIN = 450
VISIT_MIN = 70
LOCAL_TRAVEL = {"INV": 12, "NRN": 21, "FRS": 26, "ELG": 17, "SPY": 33, "LOC": 44, "CAI": 39, "SKY": 52}
