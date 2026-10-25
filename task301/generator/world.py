"""The world behind task301: five sub-regions' active adult patients, each with a true smoking trajectory (a two-state
process, smoker and ex-smoker, at the sub-region's own quit and relapse rates), the statuses their practices recorded at
consultations from 2012, Eastern Shore's 2024 recording drive, and the quit outreach team's 2025 calls there.

Times are integer days from 1 January 2012. Everything is seeded and deterministic."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P

YD = 365.25


def day(d):
    return (d - P.D0).days


def date_of(n):
    return P.D0 + dt.timedelta(days=int(n))


E_DAY = day(P.EXTRACT)
H_DAY = day(P.HORIZON)
L_DAY = day(P.PILOT_LIST)


def _practices(rng):
    rows, k = [], 1
    for g in P.REG:
        m = P.PRACTICES[g]
        mult = np.exp(rng.normal(0, 0.30, m))
        mult = mult / mult.mean()
        for i in range(m):
            sysk = "BP" if rng.uniform() < 0.62 else "MD"
            rows.append(dict(practice_id="PR%03d" % k, reg=g, system=sysk, rec_mult=float(mult[i]), migrated=None))
            k += 1
    pr = pd.DataFrame(rows)
    # the Coastal Hinterland practice that moved from Medical Director to Best Practice
    g, when = P.MIGRATION
    idx = pr.index[(pr.reg == g)][3]
    pr.loc[idx, "system"] = "BP"
    pr.loc[idx, "migrated"] = when.isoformat()
    return pr


def simulate():
    rng = np.random.default_rng(P.SEED_WORLD)
    pr = _practices(rng)
    pats, sw_flat, sw_off = [], [], [0]
    recs = []
    pid = 0
    for g in P.REG:
        n = P.N[g]
        ids = pr[pr.reg == g].practice_id.values
        # practice sizes vary; patients assigned with a skewed share
        share = rng.gamma(2.0, 1.0, len(ids))
        share = share / share.sum()
        prac = rng.choice(ids, n, p=share)
        age = np.clip(18 + rng.gamma(2.6, 11.0, n), 18, 98)          # age at the extract
        sex = rng.choice(np.array(["F", "M"]), n, p=[0.52, 0.48])
        ltc = rng.uniform(size=n) < np.clip(0.08 + 0.006 * (age - 18), 0, 0.75)
        ever = rng.uniform(size=n) < P.EVER
        cur0 = ever & (rng.uniform(size=n) < P.CUR0[g])
        # the day each patient turned 15, and registration at the practice
        birth = E_DAY - age * YD
        start15 = np.maximum(0, np.ceil(birth + 15 * YD)).astype(int)
        pre = rng.uniform(size=n) < 0.55
        reg_day = np.where(pre, 0, rng.integers(0, E_DAY - 20, n))
        if g == "P":
            # Eastern Shore's roll is the January 2025 roll: nobody registers after the list date
            reg_day = np.where(pre, 0, rng.integers(0, L_DAY - 5, n))
        rec_start = np.maximum(start15, reg_day)
        leave = np.full(n, 10 ** 6)
        if g == "P":
            lv = rng.uniform(size=n) < P.LEAVE_P
            leave = np.where(lv, rng.integers(L_DAY + 5, E_DAY - 5, n), 10 ** 6)
        lam = P.BASE[g] * np.where(ltc, P.LTC_MULT, 1.0) * pr.set_index("practice_id").rec_mult.reindex(prac).values
        qd, rd = P.QUIT[g] / YD, P.RELAPSE / YD
        for i in range(n):
            # true trajectory from the later of 1 January 2012 and the patient's fifteenth birthday
            t0 = int(start15[i])
            s = bool(cur0[i])
            sw = []
            if ever[i]:
                t = float(t0)
                while True:
                    t += rng.exponential(1.0 / (qd if s else rd))
                    if t >= H_DAY:
                        break
                    sw.append(t)
                    s = not s
            sw_flat.extend(sw)
            sw_off.append(len(sw_flat))
            # recording days
            lo, hi = int(rec_start[i]), min(E_DAY, int(leave[i]))
            days = []
            if hi > lo:
                k = rng.poisson(lam[i] * (hi - lo) / YD)
                days = list(rng.integers(lo, hi + 1, k))
                if reg_day[i] > 0 and reg_day[i] >= start15[i] and rng.uniform() < P.REG_RECORD:
                    days.append(int(reg_day[i]))
                if g == "P" and rng.uniform() < P.P_DRIVE:
                    a, b = day(P.P_DRIVE_WIN[0]), day(P.P_DRIVE_WIN[1])
                    dd = int(rng.integers(a, b + 1))
                    if lo <= dd <= hi:
                        days.append(dd)
            for dd in days:
                recs.append((pid, dd))
            pats.append((pid, g, prac[i], float(age[i]), sex[i], bool(ltc[i]), bool(ever[i]), bool(cur0[i]),
                         int(t0), int(reg_day[i]), int(leave[i])))
            pid += 1
    pat = pd.DataFrame(pats, columns=["pid", "reg", "practice_id", "age", "sex", "ltc", "ever", "cur0", "t0", "reg_day",
                                      "leave"])
    sw = (np.array(sw_flat), np.array(sw_off))
    rec = pd.DataFrame(recs, columns=["pid", "day"]).sort_values(["pid", "day"], kind="stable").reset_index(drop=True)
    rec["true"] = true_state(pat, sw, rec.pid.values, rec.day.values)
    return pr, pat, sw, rec


def true_state(pat, sw, pids, days):
    """1 smoker, 0 ex-smoker, -1 never smoked, at each (patient, day)."""
    flat, off = sw
    pids = np.asarray(pids)
    days = np.asarray(days, dtype=float)
    ever = pat.ever.values[pids]
    cur0 = pat.cur0.values[pids]
    out = np.empty(len(pids), dtype=int)
    for j in range(len(pids)):
        p = pids[j]
        if not ever[j]:
            out[j] = -1
            continue
        a, b = off[p], off[p + 1]
        k = np.searchsorted(flat[a:b], days[j], side="right")
        cur = bool(cur0[j]) ^ (k % 2 == 1)
        out[j] = 1 if cur else 0
    return out


def frac_smoking(pat, sw, pids, d_from, d_to, n=52):
    """Share of each patient's days smoking over a window, on an even grid."""
    grid = np.linspace(d_from, d_to, n + 1)[:-1] + (d_to - d_from) / (2 * n)
    pids = np.asarray(pids)
    acc = np.zeros(len(pids))
    for gday in grid:
        acc += (true_state(pat, sw, pids, np.full(len(pids), gday)) == 1)
    return acc / n


if __name__ == "__main__":
    import pickle
    import sys
    pr, pat, sw, rec = simulate()
    out = sys.argv[1] if len(sys.argv) > 1 else "world.pkl"
    with open(out, "wb") as fh:
        pickle.dump((pr, pat, sw, rec), fh)
    print(len(pat), "patients", len(rec), "recordings")
