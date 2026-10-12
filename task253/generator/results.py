"""The three NAPLAN sittings as student-by-test rows: Years 3 and 5, five tests, every enrolled student, the
non-participants scoreless. The Year 5 reading scores of participating students are core.py's; everything
else here is drawn on its own streams."""
import numpy as np
import pandas as pd

import core

TESTS = ["RD", "WR", "SP", "GP", "NU"]
MEANS = {3: {"RD": 426, "WR": 414, "SP": 409, "GP": 423, "NU": 404},
         5: {"RD": None, "WR": 478, "SP": 494, "GP": 499, "NU": 489}}
SDS = {3: {"RD": 78, "WR": 62, "SP": 70, "GP": 80, "NU": 68}, 5: {"WR": 63, "SP": 68, "GP": 74, "NU": 67}}
NONPART = ["A", "E", "W", "S"]
NONPART_P = [0.62, 0.21, 0.13, 0.04]


def build(W, seed):
    w = W["w"]
    S = w["S"]
    rng = np.random.default_rng([seed, 21])
    census = W["census"]
    # enrolments by year level and sitting: Year 5 from core; Year 3 from the census cohorts
    enr = {(5, j): w["enrol"][:, j] for j in range(3)}
    enr[(3, 2)] = np.maximum(4, census[:, 3] + rng.integers(-2, 3, S))
    enr[(3, 1)] = np.maximum(4, census[:, 4] + rng.integers(-2, 3, S))
    enr[(3, 0)] = np.maximum(4, w["enrol"][:, 2] + rng.integers(-3, 3, S))
    # student identifiers; the 2024 Year 3 cohort is mostly the 2026 Year 5 cohort
    pool = rng.choice(np.arange(30_000_000, 39_999_999), size=int(sum(v.sum() for v in enr.values())) + 5000,
                      replace=False)
    pi = [0]

    def take(k):
        out = pool[pi[0]:pi[0] + k]
        pi[0] += k
        return out
    ids = {}
    for i in range(S):
        for j in range(3):
            ids[(5, j, i)] = take(int(enr[(5, j)][i]))
        ids[(3, 1, i)] = take(int(enr[(3, 1)][i]))
        ids[(3, 2, i)] = take(int(enr[(3, 2)][i]))
        stay = ids[(5, 2, i)]
        k = int(enr[(3, 0)][i])
        keep = stay[rng.permutation(len(stay))[: min(len(stay), int(round(0.9 * k)))]]
        ids[(3, 0, i)] = np.concatenate([keep, take(k - len(keep))])
    # Year 5 reading: core's participating scores, the rest non-participants
    core_scores = {(i, j): y for i, j, y in w["scores"]}
    tables = []
    for j in range(3):
        rows = {"sitting": [], "school": [], "student": [], "year": [], "test": [], "part": [], "score": []}
        for i in range(S):
            for yl in (3, 5):
                sid = ids[(yl, j, i)]
                k = len(sid)
                if yl == 5:
                    y = core_scores[(i, j)]
                    npart = k - len(y)
                    order = rng.permutation(k)
                    part_mask = np.zeros(k, bool)
                    part_mask[order[: len(y)]] = True
                    abil = np.full(k, np.nan)
                    abil[part_mask] = (y - (core.MU + w["shift"] + w["u"][i] + w["v"][i, j])) / core.SD_STUDENT
                    status = np.array(["P"] * k, dtype=object)
                    status[~part_mask] = rng.choice(NONPART, size=npart, p=NONPART_P)
                    rd = np.full(k, np.nan)
                    rd[part_mask] = y
                else:
                    rate = rng.beta(60, 3.2)
                    part_mask = rng.random(k) < rate
                    status = np.array(["P"] * k, dtype=object)
                    status[~part_mask] = rng.choice(NONPART, size=int((~part_mask).sum()), p=NONPART_P)
                    abil = np.full(k, np.nan)
                    rd = None
                ab = np.where(np.isnan(abil), rng.normal(0, 1, k), abil)
                yg = rng.normal(0, 9)
                for t in TESTS:
                    if yl == 5 and t == "RD":
                        sc, st = rd, status
                    else:
                        st = status.copy()
                        # absence differs by test day; exempt and withdrawn students are out of every test
                        flip = (st == "P") & (rng.random(k) < 0.012)
                        st[flip] = "A"
                        back = (st == "A") & (rng.random(k) < 0.25)
                        st[back] = "P"
                        mean = MEANS[yl][t] + (w["u"][i] * (0.85 if yl == 5 else 0.75)) + w["shift"]
                        sd = SDS[yl][t]
                        sc = mean + yg + 0.72 * sd * ab + rng.normal(0, 0.69 * sd, k)
                        sc = np.where(st == "P", sc, np.nan)
                    sc = np.round(sc, 1) if j == 0 else np.round(sc)
                    rows["sitting"].append(np.full(k, core.SITTINGS[j]))
                    rows["school"].append(np.full(k, i))
                    rows["student"].append(sid)
                    rows["year"].append(np.full(k, yl))
                    rows["test"].append(np.full(k, t, dtype=object))
                    rows["part"].append(st)
                    rows["score"].append(sc)
        df = pd.DataFrame({c: np.concatenate(v) for c, v in rows.items()})
        tables.append(df)
    return tables
