"""The clean truth: every index lumbar operation, its patient, case-mix, complication, follow-up
answer and later spells, before any system writes a record or any mess is applied."""
import datetime as dt
import numpy as np
import pandas as pd
from common import SEED, PROVIDERS, FY, CASEMIX, NHS_KEYS, EXTRACT_DATE

FY_ORDER = ["2022-23", "2023-24", "2024-25", "2025-26"]


def stream(*keys):
    return np.random.default_rng(np.random.SeedSequence([SEED] + [int(k) for k in keys]))


def weekdays(start, end):
    d, out = start, []
    while d <= end:
        if d.weekday() < 5:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


BANK = {dt.date(2022, 4, 15), dt.date(2022, 4, 18), dt.date(2022, 5, 2), dt.date(2022, 6, 2), dt.date(2022, 6, 3),
        dt.date(2022, 8, 29), dt.date(2022, 9, 19), dt.date(2022, 12, 26), dt.date(2022, 12, 27), dt.date(2023, 1, 2),
        dt.date(2023, 4, 7), dt.date(2023, 4, 10), dt.date(2023, 5, 1), dt.date(2023, 5, 8), dt.date(2023, 5, 29),
        dt.date(2023, 8, 28), dt.date(2023, 12, 25), dt.date(2023, 12, 26), dt.date(2024, 1, 1), dt.date(2024, 3, 29),
        dt.date(2024, 4, 1), dt.date(2024, 5, 6), dt.date(2024, 5, 27), dt.date(2024, 8, 26), dt.date(2024, 12, 25),
        dt.date(2024, 12, 26), dt.date(2025, 1, 1), dt.date(2025, 4, 18), dt.date(2025, 4, 21), dt.date(2025, 5, 5),
        dt.date(2025, 5, 26), dt.date(2025, 8, 25), dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1)}


def odi_sections(total, rng):
    """Ten section answers (0-5) whose total is close to the ODI total (0-100 -> 0-50)."""
    target = int(round(total / 2.0))
    target = max(0, min(50, target))
    base = np.full(10, target // 10)
    rem = target - base.sum()
    idx = rng.permutation(10)[:rem]
    base[idx] += 1
    # spread: move single points between sections without changing the total
    for _ in range(int(rng.integers(2, 7))):
        a, b = rng.integers(0, 10, 2)
        if base[a] > 0 and base[b] < 5 and a != b:
            base[a] -= 1
            base[b] += 1
    return base


def build_world():
    ops = []
    pid = 0
    for pi, p in enumerate(PROVIDERS):
        for fi, fy in enumerate(FY_ORDER):
            n = p["vol"][fi - 1] if fi > 0 else int(round(0.93 * p["vol"][0]))
            r = stream(p["key"], fi, 1)
            days = [d for d in weekdays(*FY[fy]) if d not in BANK]
            if p["kind"] == "IS":
                sat = [d for d in [FY[fy][0] + dt.timedelta(days=k) for k in range(366)]
                       if d.weekday() == 5 and d <= FY[fy][1]]
                days = days + sat[::3]
            opd = sorted(r.choice(len(days), size=n, replace=True))
            for j in range(n):
                pid += 1
                op_date = days[opd[j]]
                age = float(np.clip(r.normal(56 + 4 * p["sev"], 13.5), 19, 91))
                female = bool(r.random() < 0.53)
                stenosis = bool(r.random() < 1 / (1 + np.exp(-(age - 60) / 7.0)))
                smoker = bool(r.random() < 0.19 - 0.04 * (age > 65))
                prev = bool(r.random() < 0.10 + 0.05 * p["sev"])
                symp12 = bool(r.random() < 0.44 + 0.08 * stenosis)
                pre = float(np.clip(r.normal(44 + 3.5 * p["sev"] + 3.0 * stenosis, 13.5), 8, 90))
                ops.append(dict(pid=pid, prov=p["key"], fy=fy, op_date=op_date, age=age, female=female,
                                stenosis=stenosis, smoker=smoker, prev=prev, symp12=symp12, pre_true=pre,
                                rkey=(p["key"], fi, j)))
    w = pd.DataFrame(ops)
    w["disc"] = ~w["stenosis"]
    # filed case-mix model on the true pre-operative score
    E = (CASEMIX["intercept"] + CASEMIX["pre_odi_minus_45"] * (w.pre_true - 45) + CASEMIX["age_minus_55"] * (w.age - 55)
         + CASEMIX["female"] * w.female + CASEMIX["smoker"] * w.smoker + CASEMIX["previous_lumbar_surgery"] * w.prev
         + CASEMIX["symptoms_over_12_months"] * w.symp12 + CASEMIX["disc_herniation"] * w.disc)
    w["E_true"] = E
    pmap = {p["key"]: p for p in PROVIDERS}
    comp, imp, drop, resp, death, los, tr, pre_done = [], [], [], [], [], [], [], []
    for row in w.itertuples():
        p = pmap[row.prov]
        r = stream(row.rkey[0], row.rkey[1], row.rkey[2] + 1000, 2)
        mult = 1 + 0.45 * (row.age > 70) + 0.35 * row.smoker + 0.45 * row.prev
        c = bool(r.random() < min(0.9, p["c"] * mult / 1.18))
        comp.append(c)
        d = float(np.clip(r.normal(17.5, 4.5), 6, 32)) if c else 0.0
        drop.append(d)
        imp.append(float(row.E_true + p["u"] + r.normal(0, 11.5) - d))
        pd_ = 0.004 + (0.012 if c else 0.0) + 0.004 * (row.age > 78)
        death.append(bool(r.random() < pd_))
        pr = p["r"] * (1 + 0.006 * (row.age - 55))
        pr = pr * (0.32 if c else 1.0)
        resp.append(bool(r.random() < min(0.95, pr)))
        base_los = 0 if (row.disc and r.random() < 0.45) else int(r.choice([1, 1, 2, 2, 2, 3, 4]))
        if row.age > 72 and r.random() < 0.3:
            base_los += int(r.integers(1, 4))
        los.append(base_los)
        tr.append(bool(p["kind"] == "NHS" and row.age > 70 and r.random() < 0.16))
        pre_done.append(bool(r.random() < 0.885))
    w["comp"] = comp
    w["drop"] = drop
    w["imp_true"] = imp
    w["died_12m"] = death
    w["resp_12m"] = resp
    w["los"] = los
    w["transfer"] = tr
    w["pre_done"] = pre_done
    w["post_true"] = np.clip(w.pre_true - w.imp_true, 0, 100)
    return w


if __name__ == "__main__":
    w = build_world()
    print(len(w), w.groupby("fy").size().to_dict())
    print(w.groupby("prov")[["comp", "resp_12m", "imp_true"]].mean().round(3))
