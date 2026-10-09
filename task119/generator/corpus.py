"""The national programme's escalation reviews in the four neighbouring regions: 34 reviewed trust-years
(41 attempts) with each year's referrals, unit stays, 08:00 bed returns and patient outcomes.

Confirmed deaths are an output: the deaths within 30 days of the decision among patients who waited more
than four hours from the decision to admit to the assignment of a bed, level-3 decisions, counted at the
referring trust, deaths before assignment kept. The neighbouring networks never ran a unit full, so every
long wait there passed beside an empty staffed bed of the trust's own unit.
"""
import datetime as dt
import heapq
from collections import defaultdict

import numpy as np

from common import CORPUS_REGIONS, TWIN_A, TWIN_B, WINDOW_CASE, rng, DAY

# (region, trust, reviewed calendar year, level-3 beds, trust type, confirmed); confirmed is a design target
REVIEWS = [
    ("Haskminster", "Feningby", 2021, 12, "District general", 9),
    ("Haskminster", "Barlewick", 2020, 16, "District general", 17),
    ("Haskminster", "Barlewick", 2023, 16, "District general", 0),
    ("Haskminster", "Calesgate", 2021, 10, "District general", 6),
    ("Haskminster", "Calesgate", 2024, 10, "District general", 0),
    ("Haskminster", "Ashenstow", 2022, 22, "Teaching", 29),
    ("Haskminster", "Ashenstow", 2024, 22, "Teaching", 13),
    ("Haskminster", "Feningby", 2023, 12, "District general", 0),
    ("Isterdale", "Ormerleby", 2022, 14, "District general", 24),
    ("Isterdale", "Elmowbury", 2020, 18, "District general", 21),
    ("Isterdale", "Elmowbury", 2022, 18, "District general", 19),
    ("Isterdale", "Rookerholm", 2021, 9, "District general", 0),
    ("Isterdale", "Rookerholm", 2023, 9, "District general", 5),
    ("Isterdale", "Vellesford", 2020, 26, "Teaching", 31),
    ("Isterdale", "Vellesford", 2023, 26, "Teaching", 18),
    ("Isterdale", "Ormerleby", 2024, 14, "District general", 12),
    ("Tevermouth", "Selarwell", 2023, 14, "District general", 11),
    ("Tevermouth", "Selarwell", 2020, 14, "District general", 8),
    ("Tevermouth", "Frithleton", 2021, 20, "Teaching", 22),
    ("Tevermouth", "Frithleton", 2024, 20, "Teaching", 0),
    ("Tevermouth", "Lestowe", 2022, 11, "District general", 7),
    ("Tevermouth", "Cranerby", 2021, 15, "District general", 14),
    ("Tevermouth", "Cranerby", 2023, 15, "District general", 4),
    ("Tevermouth", "Lestowe", 2024, 11, "District general", 0),
    ("Morrowcombe", "Morrerford", 2020, 17, "District general", 16),
    ("Morrowcombe", "Morrerford", 2022, 17, "District general", 14),
    ("Morrowcombe", "Tamarwell", 2021, 13, "District general", 9),
    ("Morrowcombe", "Tamarwell", 2024, 13, "District general", 0),
    ("Morrowcombe", "Esklecombe", 2022, 24, "Teaching", 26),
    ("Morrowcombe", "Esklecombe", 2024, 24, "Teaching", 19),
    ("Morrowcombe", "Kirkenstead", 2020, 12, "District general", 6),
    ("Morrowcombe", "Kirkenstead", 2023, 12, "District general", 5),
    ("Haskminster", "Barlewick", 2021, 16, "District general", 27),
    ("Tevermouth", "Frithleton", 2022, 20, "Teaching", 20),
]


def minute(d, h=0, m=0):
    return int((dt.datetime(d.year, d.month, d.day, h, m) - dt.datetime(2020, 1, 1)).total_seconds() // 60)


def to_str(m):
    return (dt.datetime(2020, 1, 1) + dt.timedelta(minutes=int(m))).strftime("%Y-%m-%d %H:%M")


def to_date(m):
    return (dt.datetime(2020, 1, 1) + dt.timedelta(minutes=int(m))).date()


def make_review(idx, spec, r, twin_overrides=None):
    region, trust, year, beds, ttype, n = spec
    d0, d1 = dt.date(year, 1, 1), dt.date(year, 12, 31)
    days = (d1 - d0).days + 1
    pats = []

    def rnd_dta(lo_h=8, hi_h=22):
        d = d0 + dt.timedelta(days=int(r.integers(0, days)))
        return minute(d, int(r.integers(lo_h, hi_h)), int(r.integers(0, 60)))

    def add(kind, level_req, level_dec, wait, died_day, outcome="admitted", recv_delay=None, arr_extra=None,
            post=False, dta=None):
        dta = dta if dta is not None else rnd_dta()
        recv_delay = recv_delay if recv_delay is not None else int(np.clip(np.exp(r.normal(np.log(30), 0.6)), 5, 90))
        rec = dta - recv_delay
        end = dta + wait
        p = {"kind": kind, "level_req": level_req, "level_dec": level_dec, "received": rec, "dta": dta,
             "outcome": outcome, "end": end}
        if outcome == "admitted":
            p["assigned"] = end
            p["arrived"] = end + (arr_extra if arr_extra is not None else int(r.integers(10, 55)))
        elif outcome == "died":
            p["assigned"] = None
            p["arrived"] = None
        else:
            p["assigned"] = None
            p["arrived"] = None
        dta_day = to_date(dta)
        if died_day is not None:
            dd = dta_day + dt.timedelta(days=int(died_day))
            if outcome == "died":
                dd = to_date(end)
            p["death"] = dd
            if outcome == "died":
                p["hosp_out"] = dd
            elif post:
                p["hosp_out"] = dd - dt.timedelta(days=int(r.integers(1, 4)))
            else:
                p["hosp_out"] = dd
        else:
            p["death"] = None
            p["hosp_out"] = to_date(end) + dt.timedelta(days=int(r.integers(3, 16)))
        pats.append(p)
        return p

    def long_wait():
        # four hours ten minutes or more; a share between four and six hours
        if r.random() < 0.47:
            return int(r.integers(250, 356))
        return int(r.integers(366, 720))

    # ---- the filed set: n deaths after a long wait (decided level 3)
    W = int(round(0.12 * n + (0.5 if n >= 6 else 0)))
    P_ = int(round(0.25 * n))
    if (trust, year) == WINDOW_CASE:
        P_ = 3
    S = int(round(0.42 * n))
    E = int(round(0.08 * n))
    late_idx = set(int(x) for x in r.choice(np.arange(n), size=min(S, n), replace=False)) if n else set()
    post_pool = [i for i in range(W, n)]
    post_idx = set(post_pool[:P_])
    for i in range(n):
        dw = i < W
        day = int(r.integers(8, 25)) if i in late_idx else int(r.integers(0, 8))
        req = 2 if (i >= n - E and i not in post_idx) else 3
        add("filed", req, 3, long_wait(), day, outcome="died" if dw else "admitted", post=(i in post_idx))
    # survivors of long waits
    for i in range(int(round(2.4 * n)) + int(r.integers(2, 6))):
        add("lw_alive", 3, 3, long_wait(), None)
    # ---- extras that only a rival counts
    k_r = int(round(0.16 * n)) + int(r.integers(0, 2))
    k_a = int(round(0.12 * n)) + int(r.integers(0, 2))
    k_k = int(round(0.15 * n)) + int(r.integers(0, 2))
    k_l = int(round(0.16 * n)) + int(r.integers(0, 2))
    k_2 = int(round(0.15 * n)) + int(r.integers(0, 2))
    if n == 0:
        k_r, k_a, k_k, k_l, k_2 = [1 + int(x) for x in r.integers(0, 2, size=5)]
    if (trust, year) == WINDOW_CASE:
        k_l = 5
    if (trust, year) == ("Esklecombe", 2022):
        k_2 = 6
    for i in range(k_r):       # short from the decision, long from receipt
        add("x_receipt", 3, 3, int(r.integers(100, 180)), int(r.integers(0, 24)), recv_delay=int(r.integers(150, 221)))
    for i in range(k_a):       # bed assigned inside four hours, arrival after
        add("x_arrival", 3, 3, int(r.integers(190, 225)), int(r.integers(0, 24)), arr_extra=int(r.integers(60, 121)))
    for i in range(k_k):       # three to four hours
        add("x_three", 3, 3, int(r.integers(186, 234)), int(r.integers(0, 24)))
    for i in range(k_l):       # long wait, died after day 35
        lo, hi = (31, 61) if (trust, year) == WINDOW_CASE else (36, 89)
        add("x_late", 3, 3, long_wait(), int(r.integers(max(lo, 36), hi)), post=(r.random() < 0.6))
    for i in range(k_2):       # level-2 decision, long wait, died
        add("x_level2", 3 if i % 2 == 0 else 2, 2, long_wait(), int(r.integers(0, 24)))
    # ---- background
    V = twin_overrides["referrals"] if twin_overrides else int(r.integers(900, 1400)) + beds * 18
    while len(pats) < V:
        lvl = 3 if r.random() < 0.45 else 2
        u = r.random()
        wait = int(np.clip(np.exp(r.normal(np.log(45), 0.7)), 5, 170))
        if u < 0.82:
            died = int(r.integers(0, 90)) if r.random() < (0.16 if lvl == 3 else 0.06) else None
            if died is not None and 24 < died < 36:
                died = None
            add("bg", lvl, lvl, wait, died)
        else:
            add("bg_sd", lvl, lvl, int(r.integers(20, 170)), None, outcome="stood_down")
    return {"idx": idx, "region": region, "trust": trust, "year": year, "beds": beds, "type": ttype, "n": n,
            "patients": pats}


def unit_records(rev, r, extra_seed=0):
    """Admissions to the reviewed trust's own unit, never full; 08:00 returns from the census."""
    beds = rev["beds"]
    year = rev["year"]
    adm = []
    cap = {}
    for i, p in enumerate(rev["patients"]):
        if p["outcome"] == "admitted":
            adm.append((p["assigned"], i, "01"))
            last = p["death"] if p["death"] is not None else p["hosp_out"]
            cap[i] = minute(min(last, p["hosp_out"]), 23, 0) if p["death"] is None else minute(p["death"], 12, 0)
    d0 = dt.date(year, 1, 1)
    for k in range(int(r.integers(140, 260))):
        d = d0 + dt.timedelta(days=int(r.integers(0, 365)))
        if d.weekday() < 5:
            adm.append((minute(d, int(r.integers(10, 17)), int(r.integers(0, 60))), -1 - k, "04"))
    adm.sort()
    occ = []          # heap of (discharge, key)
    stays = []
    by_key = {}
    for t, key, typ in adm:
        while occ and occ[0][0] <= t:
            heapq.heappop(occ)
        if len(occ) >= beds - 1:
            # the longest-staying occupant steps down before this admission
            live = sorted(occ, key=lambda x: by_key[x[1]]["admit"])
            dis, k2 = live[0]
            occ.remove((dis, k2))
            heapq.heapify(occ)
            st = by_key[k2]
            st["discharge"] = t - int(r.integers(1, 30))
            assert st["discharge"] > st["admit"], (rev["trust"], t)
        los = int(np.exp(r.normal(np.log(2.6 * DAY if typ == "01" else 1.3 * DAY), 0.6)))
        los = max(los, 6 * 60)
        dis = t + los
        if key in cap:
            dis = min(dis, max(t + 60, cap[key]))
        s = {"key": key, "admit": t, "discharge": dis, "type": typ}
        by_key[key] = s
        stays.append(s)
        heapq.heappush(occ, (s["discharge"], key))
    # census at 08:00 and a check that the unit never filled
    ev = sorted([(s["admit"], 1) for s in stays] + [(s["discharge"], -1) for s in stays], key=lambda x: (x[0], x[1]))
    c, peak = 0, 0
    for t, dlt in ev:
        c += dlt
        peak = max(peak, c)
    assert peak <= beds - 1, (rev["trust"], rev["year"], peak, beds)
    returns = []
    adm_t = sorted(s["admit"] for s in stays)
    dis_t = sorted(s["discharge"] for s in stays)
    import bisect
    for k in range(365 + (1 if year % 4 == 0 else 0)):
        d = d0 + dt.timedelta(days=k)
        t = minute(d, 8, 0)
        occn = bisect.bisect_right(adm_t, t) - bisect.bisect_right(dis_t, t)
        returns.append((d, beds, occn))
    return stays, returns


def build_corpus():
    r = rng("corpus")
    revs = []
    for i, spec in enumerate(REVIEWS):
        rr = rng("review", i)
        revs.append(make_review(i, spec, rr))
    # twin pair: identical on every column the log shows
    ia = [i for i, x in enumerate(REVIEWS) if (x[1], x[2]) == TWIN_A][0]
    ib = [i for i, x in enumerate(REVIEWS) if (x[1], x[2]) == TWIN_B][0]
    revs[ia] = make_twin(ia, REVIEWS[ia], "A")
    revs[ib] = make_twin(ib, REVIEWS[ib], "B")
    for rev in revs:
        rr = rng("unit", rev["idx"])
        rev["stays"], rev["returns"] = unit_records(rev, rr)
    # equal mean 08:00 occupancy for the twins: reseed the second until the published figure matches
    A_mean = round(np.mean([x[2] for x in revs[ia]["returns"]]), 1)
    for k in range(400):
        rr = rng("unit", ib, "twin", k)
        st, rt = unit_records(revs[ib], rr)
        if round(np.mean([x[2] for x in rt]), 1) == A_mean:
            revs[ib]["stays"], revs[ib]["returns"] = st, rt
            break
    else:
        raise RuntimeError("twin occupancy")
    return revs


def make_twin(idx, spec, which):
    """Ormerleby 2022 and Selarwell 2023: same trust type, beds, referrals, screen count, occupancy and
    all-cause 30-day deaths among level-3 referrals; confirmed 24 and 11. Selarwell's delays sat before
    the decision, so fewer of its waits run four hours from the decision."""
    r = rng("twin", which)
    region, trust, year, beds, ttype, n = spec
    d0 = dt.date(year, 1, 1)
    pats = []

    def dta_rand():
        d = d0 + dt.timedelta(days=int(r.integers(0, 365)))
        return minute(d, int(r.integers(8, 22)), int(r.integers(0, 60)))

    def add(level_req, level_dec, wait, recv, death_day, outcome="admitted", kind="bg", post=False):
        dta = dta_rand()
        end = dta + wait
        p = {"kind": kind, "level_req": level_req, "level_dec": level_dec, "received": dta - recv, "dta": dta,
             "outcome": outcome, "end": end,
             "assigned": end if outcome == "admitted" else None,
             "arrived": end + int(r.integers(10, 50)) if outcome == "admitted" else None}
        dta_day = to_date(dta)
        if death_day is None:
            p["death"] = None
            p["hosp_out"] = to_date(end) + dt.timedelta(days=int(r.integers(3, 14)))
        else:
            dd = to_date(end) if outcome == "died" else dta_day + dt.timedelta(days=int(death_day))
            p["death"] = dd
            p["hosp_out"] = dd - dt.timedelta(days=int(r.integers(1, 4))) if post else dd
        pats.append(p)

    lw = lambda: int(r.integers(250, 560))
    if which == "A":
        for i in range(24):
            add(3, 3, lw(), int(r.integers(10, 60)), int(r.integers(0, 22)), outcome="died" if i < 3 else "admitted",
                kind="filed", post=(i % 5 == 2))
        for i in range(44):
            add(3, 3, lw(), int(r.integers(10, 60)), None, kind="lw_alive")
        for i in range(3):           # receipt-long, decision-short, survived
            add(3, 3, int(r.integers(150, 200)), int(r.integers(100, 141)), None, kind="x_receipt_alive")
    else:
        for i in range(11):
            add(3, 3, lw(), int(r.integers(10, 60)), int(r.integers(0, 22)), outcome="died" if i < 1 else "admitted",
                kind="filed", post=(i % 5 == 2))
        for i in range(27):
            add(3, 3, lw(), int(r.integers(10, 60)), None, kind="lw_alive")
        for i in range(13):          # the delay sat before the decision: long from receipt, short from the decision
            add(3, 3, int(r.integers(100, 200)), int(r.integers(160, 231)), int(r.integers(0, 22)), kind="x_receipt")
        for i in range(20):
            add(3, 3, int(r.integers(100, 200)), int(r.integers(160, 231)), None, kind="x_receipt_alive")
    # 71 level-3 referrals waited more than four hours from receipt in both years; background stays inside
    # three hours fifty from receipt. All-cause 30-day deaths among level-3 referrals: 96 in both.
    target_deaths = 96
    dead_l3 = sum(1 for p in pats if p["level_dec"] == 3 and p["death"] is not None
                  and (p["death"] - to_date(p["dta"])).days <= 30)
    need = target_deaths - dead_l3
    k = 0
    while len(pats) < 1184:
        lvl = 3 if (k % 9) < 4 else 2
        wait = int(np.clip(np.exp(r.normal(np.log(40), 0.6)), 5, 150))
        recv = int(r.integers(5, 60))
        if lvl == 3 and need > 0:
            add(3, 3, wait, recv, int(r.integers(0, 24)), kind="bg")
            need -= 1
        else:
            dd = int(r.integers(40, 90)) if r.random() < 0.05 else None
            add(lvl, lvl, wait, recv, dd, kind="bg")
        k += 1
    return {"idx": idx, "region": region, "trust": trust, "year": year, "beds": beds, "type": ttype, "n": n,
            "patients": pats}


# ------------------------------------------------------------------------------------------ the rules
CLOCKS = ("decision_to_bed", "receipt_to_bed", "decision_to_arrival")
WINDOWS = ("30d", "in_hospital", "7d", "90d")
LEVELS = ("decided_3", "requested_3", "decided_2_or_3")
DBA = ("kept", "dropped")
THRESH = (240, 180, 360)
FILED = ("decision_to_bed", "30d", "decided_3", "kept", 240)


def rule_count(pats, rule):
    clock, window, level, dba, thr = rule
    n = 0
    for p in pats:
        if level == "decided_3" and p["level_dec"] != 3:
            continue
        if level == "requested_3" and p["level_req"] != 3:
            continue
        if p["outcome"] == "stood_down":
            continue
        died_waiting = p["outcome"] == "died"
        if dba == "dropped" and died_waiting:
            continue
        start = p["received"] if clock == "receipt_to_bed" else p["dta"]
        if died_waiting:
            end = p["end"]
        elif clock == "decision_to_arrival":
            end = p["arrived"]
        else:
            end = p["assigned"]
        if end - start <= thr:
            continue
        dd = p["death"]
        if dd is None:
            continue
        off = (dd - to_date(p["dta"])).days
        if window == "30d" and off > 30:
            continue
        if window == "7d" and off > 7:
            continue
        if window == "90d" and off > 90:
            continue
        if window == "in_hospital" and dd > p["hosp_out"]:
            continue
        n += 1
    return n


def all_rules():
    out = []
    for c in CLOCKS:
        for w in WINDOWS:
            for l in LEVELS:
                for b in DBA:
                    for t in THRESH:
                        out.append((c, w, l, b, t))
    return out
