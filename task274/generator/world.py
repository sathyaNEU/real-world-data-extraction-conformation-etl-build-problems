"""The world before any record is written: the survey's sample and examinations, each adult's serum 25-hydroxyvitamin D,
the laboratory's analyzers, reagent lots, calibrator lots and calibrations, every result, the October accuracy-based
check and the December bridging run. Each part draws from its own random stream so a change in one leaves the others
where they were."""
from __future__ import annotations

import bisect
import datetime as dt
import math

import numpy as np

import common as K

STREAMS = {"pop": 1, "vit": 2, "lab": 3, "cal": 4, "chk": 5, "bridge": 6, "dsq": 7, "disp": 8, "log": 9, "track": 10,
           "assay": 11, "dsq2": 12, "roster": 13}


def rng(seed, name):
    return np.random.default_rng(np.random.SeedSequence([int(seed), STREAMS[name], 274]))


def days(a, b):
    """Every date from a to b inclusive."""
    out, d = [], a
    while d <= b:
        out.append(d)
        d += dt.timedelta(days=1)
    return out


def exam_days(c):
    a, b = K.STANDS[c]
    return [d for d in days(a, b) if d.weekday() < 6 and d not in K.HOLIDAYS]


def dst(d):
    """Mountain daylight time in 2025: 9 March to 2 November."""
    return dt.date(2025, 3, 9) <= d < dt.date(2025, 11, 2)


def to_utc(t):
    return t + dt.timedelta(hours=6 if dst(t.date()) else 7)


def season(d):
    """Serum 25(OH)D's seasonal swing on the log scale: highest at the end of August, lowest at the end of February."""
    doy = d.timetuple().tm_yday
    return 0.15 * math.sin(2 * math.pi * (doy - 150) / 365.0)


# county medians of serum 25(OH)D (ng/mL, reference scale) for a white non-supplement-using adult aged 50 at the
# year's mean season; the race mix, supplement use and season move each county's own distribution from there
CMED = [24.39, 27.23, 26.37, 25.15, 25.15, 21.69, 21.88, 21.99]
RACES = ["NHW", "NHB", "HSP", "OTH"]
RACE_EFFECT = {"NHW": 0.0, "NHB": -0.42, "HSP": -0.16, "OTH": -0.12}
RACE_MIX = [(0.78, 0.04, 0.12, 0.06), (0.64, 0.11, 0.18, 0.07), (0.82, 0.02, 0.10, 0.06), (0.70, 0.06, 0.17, 0.07),
            (0.58, 0.14, 0.20, 0.08), (0.84, 0.02, 0.09, 0.05), (0.72, 0.05, 0.16, 0.07), (0.76, 0.03, 0.15, 0.06)]
SIGMA = 0.36


def sample(seed):
    """The examined adults: county, exam date and session, age, sex, race and ethnicity, and the MEC exam weight."""
    r = rng(seed, "pop")
    P = []
    seqn = 140001
    for c, (code, name) in enumerate(K.COUNTIES):
        ed = exam_days(c)
        n = int(K.EXAM_TARGET[c] + r.integers(-18, 19))
        # sessions: morning (fasting), afternoon, evening; Saturdays morning and afternoon only
        per = r.dirichlet(np.ones(len(ed)) * 6.0)
        cnt = r.multinomial(n, per)
        rows = []
        for d, k in zip(ed, cnt):
            for _ in range(int(k)):
                sess = int(r.choice(3, p=[0.42, 0.38, 0.20] if d.weekday() < 5 else [0.55, 0.45, 0.0]))
                age = int(min(85, max(20, round(r.gamma(4.2, 11.5) + 12))))
                rows.append((d, sess, age))
        rows.sort(key=lambda x: (x[0], x[1]))
        mix = RACE_MIX[c]
        base = K.ADULTS[c] / len(rows)
        for d, sess, age in rows:
            race = RACES[int(r.choice(4, p=mix))]
            # oversampling of Black and Hispanic adults and of adults 60 and over lowers their weights
            adj = (0.55 if race in ("NHB", "HSP") else 1.0) * (0.75 if age >= 60 else 1.0)
            w = base * adj * float(np.exp(r.normal(0, 0.35)))
            P.append(dict(seqn=seqn, county=c, ccode=code, exam=d, session=sess, age=age,
                          sex=("M" if r.random() < 0.48 else "F"), race=race, w_raw=w))
            seqn += int(r.integers(1, 4))
    # rake the weights to each county's adults
    for c in range(len(K.COUNTIES)):
        idx = [i for i, p in enumerate(P) if p["county"] == c]
        tot = sum(P[i]["w_raw"] for i in idx)
        for i in idx:
            P[i]["wtmec"] = round(P[i]["w_raw"] * K.ADULTS[c] / tot, 2)
    return P


def supplements_effect(seed, P):
    """Each adult's vitamin D from supplements in the 30 days before the interview (IU a day), drawn here because it
    moves serum 25(OH)D; the questionnaire records that carry it are written in records.py."""
    r = rng(seed, "dsq")
    for p in P:
        older = p["age"] >= 60
        pr = 0.30 + (0.18 if older else 0.0) + (0.06 if p["sex"] == "F" else 0.0)
        uses = r.random() < pr
        iu = 0.0
        if uses:
            iu = float(r.choice([400, 600, 800, 1000, 1000, 2000, 2000, 5000], p=[.16, .1, .1, .24, .1, .16, .08, .06]))
            iu *= float(r.choice([1.0, 1.0, 1.0, 0.5, 0.8]))
        p["supp_iu"] = iu
    return P


def vitamin_d(seed, P, cmed=None):
    r = rng(seed, "vit")
    cm = CMED if cmed is None else cmed
    for p in P:
        lg = (math.log(cm[p["county"]]) + season(p["exam"]) + RACE_EFFECT[p["race"]]
              + 0.0035 * (p["age"] - 50) + 0.20 * math.log1p(p["supp_iu"] / 1000.0) + r.normal(0, SIGMA))
        p["true"] = math.exp(lg)
    return P


def lab_flow(seed, P):
    """Blood draw, vials, shipments, receipt, the run each primary vial went into, and the duplicate vial."""
    r = rng(seed, "lab")
    drawn = []
    for p in P:
        p["blood"] = r.random() > 0.045            # refused, contraindicated or failed venipuncture
        if not p["blood"]:
            continue
        p["dup"] = r.random() > 0.035              # too little serum for the stored duplicate
        p["reject"] = ("HEM" if r.random() < 0.013 else ("QNS" if r.random() < 0.004 else ""))
        drawn.append(p)
    # the MEC ships on Mondays and Thursdays everything drawn since the last shipment; the laboratory receives it
    # the next day and runs the survey's vitamin D on weekdays, a receipt's vials in racks of up to 40
    by_ship = {}
    for p in drawn:
        d = p["exam"] + dt.timedelta(days=1)
        while d.weekday() not in (0, 3):
            d += dt.timedelta(days=1)
        p["shipped"] = d
        p["received"] = d + dt.timedelta(days=1)
        by_ship.setdefault(p["received"], []).append(p)
    runs = []
    for rec in sorted(by_ship):
        vials = [p for p in by_ship[rec] if not p["reject"]]
        vials.sort(key=lambda p: p["seqn"])
        lag = int(r.integers(0, 4))
        d = rec
        k = 0
        while k < lag or d.weekday() >= 5 or d in K.HOLIDAYS:
            d += dt.timedelta(days=1)
            if d.weekday() < 5 and d not in K.HOLIDAYS:
                k += 1
        start = 0
        while start < len(vials):
            rack = vials[start:start + 40]
            an = int(r.random() < 0.46)
            t0 = dt.datetime.combine(d, dt.time(8, 0)) + dt.timedelta(minutes=int(r.integers(0, 360)))
            run = dict(day=d, analyzer=an, start=t0, n=len(rack))
            for j, p in enumerate(rack):
                p["run_time"] = t0 + dt.timedelta(seconds=int(84 * j + r.integers(0, 50)))
                p["analyzer"] = an
            runs.append(run)
            start += 40
            if start < len(vials) and r.random() < 0.5:
                d2 = d + dt.timedelta(days=1)
                while d2.weekday() >= 5 or d2 in K.HOLIDAYS:
                    d2 += dt.timedelta(days=1)
                d = d2
    return P, runs


def calibrations(seed, horizon=dt.date(2025, 12, 31)):
    """Every accepted calibration of each analyzer from the last of 2024 to the end of 2025: at each reagent lot's
    loading, at each new calibrator lot, when the 28-day interval runs out, and after a QC failure or a repair. Each
    sets the assay's bias until the next: the reagent lot's, the calibrator lot's, the analyzer's own and the
    calibration's own share."""
    r = rng(seed, "cal")
    keff = r.normal(0, K.CAL_LOT_SD, len(K.CAL_LOTS))
    lotb = [math.log1p(b) + r.normal(0, 0.008) for (_, _, _, b) in K.REAGENT_LOTS]
    cals = []
    for an in (0, 1):
        loads = [(lot[1 + an], i) for i, lot in enumerate(K.REAGENT_LOTS)]
        calch = [(cl[1 + an], i) for i, cl in enumerate(K.CAL_LOTS)]
        d = dt.date(2024, 12, 1)
        cur_lot = max(i for (dd, i) in loads if dd <= d) if any(dd <= d for dd, i in loads) else 0
        cur_cal = max(i for (dd, i) in calch if dd <= d)
        last = None
        unsched_next = d + dt.timedelta(days=int(r.integers(20, 70)))
        while d <= horizon:
            reason = None
            newlot = [i for (dd, i) in loads if dd == d]
            newcal = [i for (dd, i) in calch if dd == d]
            if newlot:
                cur_lot, reason = newlot[0], "LOT"
            if newcal:
                cur_cal = newcal[0]
                reason = reason or "CALLOT"
            if reason is None and last is not None and (d - last).days >= K.CAL_DAYS:
                reason = "EXPIRY"
            if reason is None and d >= unsched_next:
                reason = "QC"
                unsched_next = d + dt.timedelta(days=int(r.integers(25, 75)))
            if last is None:
                reason = reason or "START"
            if reason:
                t = dt.datetime.combine(d, dt.time(6, 0)) + dt.timedelta(minutes=int(r.integers(5, 55)))
                if reason == "QC":
                    t = dt.datetime.combine(d, dt.time(7, 20)) + dt.timedelta(minutes=int(r.integers(0, 40)))
                b = lotb[cur_lot] + keff[cur_cal] + K.ANALYZER_OFFSET[an] + r.normal(0, K.RECAL_SD)
                cals.append(dict(analyzer=an, time=t, lot=cur_lot, calot=cur_cal, reason=reason, bias=float(b)))
                last = d
            d += dt.timedelta(days=1)
    cals.sort(key=lambda c: (c["analyzer"], c["time"]))
    for i, c in enumerate(cals):
        c["id"] = i
    return cals, keff, lotb


def cal_at(cals, an, t):
    """The calibration in force on an analyzer at a moment."""
    best = None
    for c in cals:
        if c["analyzer"] == an and c["time"] <= t:
            best = c
    return best


def assay(seed, P, cals):
    r = rng(seed, "assay")
    by_an = {0: [c for c in cals if c["analyzer"] == 0], 1: [c for c in cals if c["analyzer"] == 1]}
    times = {a: [c["time"] for c in by_an[a]] for a in (0, 1)}
    for p in P:
        if not p.get("blood") or p.get("reject") or "run_time" not in p:
            continue
        a = p["analyzer"]
        i = bisect.bisect_right(times[a], p["run_time"]) - 1
        c = by_an[a][i]
        p["cal"] = c["id"]
        p["lot"] = c["lot"]
        v = p["true"] * math.exp(c["bias"] + r.normal(0, K.ASSAY_CV))
        p["result"] = round(v, 1)
    return P


def check(seed, cals):
    r = rng(seed, "chk")
    c = cal_at(cals, 0, K.CHECK_RUN)
    lab = [round(t * math.exp(c["bias"] + r.normal(0, K.ASSAY_CV)), 1) for t in K.CHECK_TARGETS]
    pct = [round(100.0 * (x - t) / t, 1) for x, t in zip(lab, K.CHECK_TARGETS)]
    mean = round(float(np.mean([100.0 * (x - t) / t for x, t in zip(lab, K.CHECK_TARGETS)])), 1)
    return dict(cal=c["id"], lab=lab, pct=pct, mean=mean, lot=c["lot"], calot=c["calot"])


def bridge(seed, P, cals):
    r = rng(seed, "bridge")
    elig = [p for p in P if p.get("result") is not None and p.get("dup")]
    elig.sort(key=lambda p: p["seqn"])
    pick = [p for p in elig if r.random() < K.BRIDGE_FRACTION]
    out = []
    t = K.BRIDGE_RUN
    for j, p in enumerate(pick):
        if j and j % 40 == 0:
            t += dt.timedelta(minutes=int(r.integers(8, 25)))
        if t.hour >= 17:
            t = dt.datetime.combine(t.date() + dt.timedelta(days=1), dt.time(8, 0)) + dt.timedelta(
                minutes=int(r.integers(0, 20)))
        c = cal_at(cals, 0, t)
        v = p["true"] * math.exp(c["bias"] + r.normal(0, K.ASSAY_CV))
        out.append(dict(seqn=p["seqn"], time=t, cal=c["id"], result=round(v, 1)))
        t += dt.timedelta(seconds=int(84 + r.integers(0, 40)))
    return out


def simulate(seed=K.SEED, cmed=None):
    P = sample(seed)
    P = supplements_effect(seed, P)
    P = vitamin_d(seed, P, cmed)
    P, runs = lab_flow(seed, P)
    cals, keff, lotb = calibrations(seed)
    P = assay(seed, P, cals)
    chk = check(seed, cals)
    br = bridge(seed, P, cals)
    return dict(seed=seed, P=P, runs=runs, cals=cals, keff=keff, lotb=lotb, check=chk, bridge=br)
