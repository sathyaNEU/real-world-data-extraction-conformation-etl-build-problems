"""task122 generator: what happens to each randomised patient in VMK-4410-202, before any extract is written.

Visits and their dates, potassium and the protocol's potassium rules (interruptions, restarts, permanent stops),
temporary holds for other reasons, dosing periods, background diuretic changes, and the true eGFR course: the
placebo course, the fall on starting the drug (haemodynamic for everyone, larger in patients already on a loop
diuretic), the recovery of the volume-related part once a diuretic is eased (only from the week-12 visit, when the
protocol first allows background changes), and the chronic benefit while on drug. Measured creatinine and the
central laboratory's eGFR follow, and the arms are calibrated to the design note's targets."""
from datetime import timedelta

import numpy as np

import params as P
import estim as E

KAPPA = {"F": 0.7, "M": 0.9}
ALPHA = {"F": -0.241, "M": -0.302}
KDELTA = {0: 0.0, 5: 0.10, 10: 0.19, 20: 0.37, 40: 0.60}


def ckd_epi_2021(scr_mgdl, age, sex):
    k, a = KAPPA[sex], ALPHA[sex]
    r = scr_mgdl / k
    g = 142.0 * min(r, 1.0) ** a * max(r, 1.0) ** -1.200 * 0.9938 ** age
    return g * (1.012 if sex == "F" else 1.0)


def scr_from_egfr(egfr, age, sex):
    """creatinine (mg/dL) giving this eGFR, by bisection on the monotone equation"""
    lo, hi = 0.2, 15.0
    for _ in range(56):
        mid = 0.5 * (lo + hi)
        if ckd_epi_2021(mid, age, sex) > egfr:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def report_creat(scr_mgdl, hub, age, sex):
    """the central laboratory's report: creatinine in the hub's unit and eGFR from the reported value"""
    if hub == "COPENHAGEN":
        umol = int(round(scr_mgdl * 88.42))
        mg = umol / 88.42
        orig, unit = str(umol), "umol/L"
    else:
        mg = round(scr_mgdl, 2)
        orig, unit = "%.2f" % mg, "mg/dL"
    return orig, unit, mg, int(round(ckd_epi_2021(mg, int(age), sex)))


def day_of(d, rand):
    return (d - rand).days + 1


class Course:
    """one patient's dosing and eGFR course; study day 1 is randomisation and the first dose"""

    def __init__(self, p, vd):
        self.p = p
        self.arm = p["ARM"]
        self.dose = P.DOSE[p["ARM"]]
        self.vd = vd
        self.rand = p["RANDDT"]
        self.off = []            # (first study day off, first day back on, or None for good)
        self.ease_day = None
        self.extra = []          # (study day, size) background diuretic changes unrelated to the drug
        self.last_day = None     # last study day in the study (withdrawal)
        self.end = None          # last dose day of a patient who completed treatment (the week-52 visit)

    def stopped_for_good(self):
        return any(b is None for a, b in self.off)

    def stop_day(self):
        for a, b in self.off:
            if b is None:
                return a
        return None

    def last_dose(self):
        return self.end if self.end is not None else self.stop_day() - 1

    def on(self, day):
        if day < 1 or (self.end is not None and day > self.end):
            return False
        return not any(day >= a and (b is None or day < b) for a, b in self.off)

    def years_on(self, day):
        if self.end is not None:
            day = min(day, self.end + 1)
        if day <= 1:
            return 0.0
        tot = day - 1
        for a, b in self.off:
            e = day if b is None else min(b, day)
            if e > a:
                tot -= (e - a)
        return max(tot, 0) / 365.25

    def state(self, day):
        """the on-drug state the fall follows: builds on starting, reverses on stopping"""
        if day < 1:
            return 0.0
        ev = [(1, 1)] + [(a, 0) for a, b in self.off] + [(b, 1) for a, b in self.off if b is not None]
        if self.end is not None:
            ev.append((self.end + 1, 0))
        ev.sort()
        s, cur, last = 0.0, 0, 1
        for t, kind in ev:
            if t > day:
                break
            tau = P.DIP_TAU_W if cur == 1 else 0.6
            s = cur + (s - cur) * np.exp(-((t - last) / 7.0) / tau)
            cur, last = kind, t
        tau = P.DIP_TAU_W if cur == 1 else 0.6
        return float(cur + (s - cur) * np.exp(-((day - last) / 7.0) / tau))


def visit_dates(rng, pats):
    """scheduled visit dates; a few visits missed and a few patients leaving the study early"""
    vds, leave, missed = {}, {}, set()
    for _, p in pats.iterrows():
        r = p["RANDDT"]
        vd = {"SCREENING": p["SCRDT"], "DAY 1": r}
        for v, num, day, win in P.VISITS[2:]:
            jit = int(np.clip(np.round(rng.normal(0, max(1.0, win / 2.6))), -win, win))
            if rng.random() < 0.022:
                # a visit taken outside its window (holiday, illness), still entered under its scheduled name;
                # from week 24 the sites kept to the window
                jit = int(rng.choice([-1, 1, 1])) * (win + int(rng.integers(1, 7)))
                if day >= 169:
                    jit = int(np.sign(jit)) * win
            dt = r + timedelta(days=day - 1 + jit)
            sh = P.weekday_shift(dt)
            if sh and day >= 169 and abs(jit + sh) > win:
                sh = -2 if sh == 1 else 2      # Sunday to Friday, Saturday to Monday, to stay inside the window
            vd[v] = dt + timedelta(days=sh)
        vds[p["SUBJID"]] = vd
        if rng.random() < 0.026:
            leave[p["SUBJID"]] = int(rng.integers(45, 330))
        for v in list(vd):
            if v not in ("SCREENING", "DAY 1", "WEEK 52", "WEEK 56 FOLLOW-UP") and rng.random() < 0.016:
                missed.add((p["SUBJID"], v))
    return vds, leave, missed


def attended(vds, leave, missed, s):
    out = []
    for v, num, day, win in P.VISITS:
        if (s, v) in missed:
            continue
        if s in leave and v not in ("SCREENING", "DAY 1"):
            if day_of(vds[s][v], vds[s]["DAY 1"]) > leave[s]:
                continue
        out.append(v)
    return out


def plan_stops(rng, pats, vds, leave):
    """stops for good for reasons other than potassium (the patient's visits continue), withdrawals from the study,
    and temporary holds for other reasons (an intercurrent illness, a procedure) between two scheduled visits; in a
    few the site entered the hold on the disposition form as a permanent stop, then the patient restarted"""
    pre = {p["SUBJID"]: {"off": [], "stop_reason": None, "holds": [], "ds_wrong": None} for _, p in pats.iterrows()}
    rate = {0: 0.014, 5: 0.014, 10: 0.016, 20: 0.020, 40: 0.026}
    arm_of = dict(zip(pats["SUBJID"], pats["ARM"]))
    rand_of = dict(zip(pats["SUBJID"], pats["RANDDT"]))
    for s in pre:
        if s in leave:
            pre[s]["off"].append((leave[s], None))
            pre[s]["stop_reason"] = "WITHDRAWAL BY SUBJECT"
            continue
        if rng.random() < rate[P.DOSE[arm_of[s]]]:
            day = int(rng.integers(200, 345))
            pre[s]["off"].append((day, None))
            pre[s]["stop_reason"] = ["ADVERSE EVENT", "PATIENT DECISION", "ADVERSE EVENT", "PHYSICIAN DECISION"][int(rng.integers(0, 4))]
    gaps = [("WEEK 24", "WEEK 32"), ("WEEK 32", "WEEK 40"), ("WEEK 40", "WEEK 52"), ("WEEK 16", "WEEK 20"),
            ("WEEK 12", "WEEK 16")]
    for arm in P.ARMS:
        ids = [s for s in pre if arm_of[s] == arm and not pre[s]["off"]]
        rng.shuffle(ids)
        n_hold = int(rng.integers(4, 8))
        j = 0
        for s in ids[:n_hold]:
            g0, g1 = gaps[int(rng.integers(0, len(gaps)))]
            a = day_of(vds[s][g0], rand_of[s]) + int(rng.integers(5, 12))
            b = min(a + int(rng.integers(8, 16)), day_of(vds[s][g1], rand_of[s]) - 6)
            if b <= a + 3:
                continue
            pre[s]["off"].append((a, b))
            pre[s]["holds"].append((a, b))
            if j < 2:
                pre[s]["ds_wrong"] = a
            j += 1
    return pre


def potassium(rng, pats, vds, leave, missed, pre):
    """central potassium at every attended visit and the protocol's rules: above 6.0 the drug is held from the
    next day, rechecked within days and restarted at or below 5.0 about two weeks later; above 6.5, or above 6.0 a
    second time, it is stopped for good; between 5.2 and 6.0 a site often repeats the test, mostly at its local
    laboratory. A haemolysed sample's potassium is not reported and nothing follows from it."""
    recs, off, stops = {}, {}, {}
    for _, p in pats.iterrows():
        s, rand = p["SUBJID"], p["RANDDT"]
        dk = KDELTA[P.DOSE[p["ARM"]]] * p["K_MULT"]
        rr, oo, strikes, stop = [], [], 0, None
        pstop = next((a for a, b in pre[s]["off"] if b is None), None)
        for v in attended(vds, leave, missed, s):
            dd = vds[s][v]
            sday = day_of(dd, rand)
            allo = oo + pre[s]["off"]
            ended = (stop is not None and sday >= stop) or (pstop is not None and sday >= pstop)
            on = v not in ("SCREENING", "WEEK 56 FOLLOW-UP") and sday >= 1 and not ended
            held = any(sday >= a and b is not None and sday < b for a, b in allo)
            since = max([1] + [b for a, b in allo if b is not None and b <= sday])
            build = (1 - np.exp(-max(sday - since, 0) / 14.0)) if (on and not held) else 0.0
            k = p["K0"] + dk * build + rng.normal(0, 0.29)
            haem = bool(rng.random() < 0.022) and v != "SCREENING"
            rr.append({"day": sday, "date": dd, "visit": v, "k": round(float(k), 1), "src": "central", "haem": haem})
            if not on or held or v in ("DAY 1", "WEEK 52") or haem:
                continue
            if k > 6.0:
                strikes += 1
                a = sday + 1
                g1 = int(rng.integers(3, 6))
                g1 += P.weekday_shift(dd + timedelta(days=g1))
                k1 = max(p["K0"] + dk * 0.6 + rng.normal(0, 0.25), k - 0.5 + rng.normal(0, 0.2))
                rr.append({"day": sday + g1, "date": dd + timedelta(days=g1), "visit": "UNSCHEDULED", "k": round(float(k1), 1),
                           "src": "central", "haem": False})
                if k > 6.5 or strikes >= 2:
                    stop = a
                    oo.append((a, None))
                    continue
                back = a + int(rng.integers(10, 15))
                oo.append((a, back))
                bd = back - 1 + P.weekday_shift(rand + timedelta(days=back - 2))
                rr.append({"day": bd, "date": rand + timedelta(days=bd - 1), "visit": "UNSCHEDULED",
                           "k": round(float(p["K0"] + rng.normal(0.15, 0.2)), 1), "src": "central", "haem": False})
            elif 5.2 < k <= 6.0 and rng.random() < 0.55:
                g1 = int(rng.integers(4, 9))
                g1 += P.weekday_shift(dd + timedelta(days=g1))
                rr.append({"day": sday + g1, "date": dd + timedelta(days=g1), "visit": "UNSCHEDULED",
                           "k": round(float(k + rng.normal(-0.05, 0.33)), 1), "src": "local" if rng.random() < 0.7 else "central",
                           "haem": False})
        recs[s], off[s], stops[s] = rr, oo, stop
    return recs, off, stops


def courses(rng, pats, vds, leave, missed, pre, koff, kstop):
    """dosing periods: potassium holds and stops, the other stops, withdrawals and holds, the diuretic easing from
    week 12 and unrelated background diuretic changes; a potassium stop before another stop is the one recorded"""
    cs, info = {}, {}
    for _, p in pats.iterrows():
        s = p["SUBJID"]
        c = Course(p, vds[s])
        po = list(pre[s]["off"])
        reason = pre[s]["stop_reason"]
        if kstop[s] is not None:
            po = [(a, b) for a, b in po if b is not None and a < kstop[s]]
            reason = "ADVERSE EVENT (POTASSIUM)"
        c.off = sorted(list(koff[s]) + po, key=lambda x: x[0])
        if s in leave and kstop[s] is None:
            c.last_day = leave[s]
        elif s in leave:
            c.last_day = leave[s]
        cs[s] = c
        info[s] = {"stop_reason": reason if c.stopped_for_good() else None,
                   "ds_wrong": pre[s]["ds_wrong"] if not c.stopped_for_good() else None,
                   "holds": [h for h in pre[s]["holds"] if h in c.off], "khold": [(a, b) for a, b in koff[s] if b is not None]}
    for s, c in cs.items():
        p = c.p
        if p["LOOP"] and c.dose > 0:
            fall = P.H[c.dose] * p["H_MULT"] + P.V[c.dose] * p["V_MULT"]
            prob = 0.86 / (1.0 + np.exp(-(fall - 4.0) / 0.9))
            if p["EASE_U"] < prob:
                v = "WEEK %d" % int(p["EASE_V"])
                if (s, v) not in missed and (s not in leave or day_of(c.vd[v], c.rand) <= leave[s]):
                    c.ease_day = day_of(c.vd[v], c.rand)
        if p["LOOP"] and rng.random() < 0.12:
            v = ["WEEK 12", "WEEK 16", "WEEK 20", "WEEK 24", "WEEK 32", "WEEK 40"][int(rng.integers(0, 6))]
            c.extra.append((day_of(c.vd[v], c.rand), float(rng.choice([-1.0, 1.0]) * rng.uniform(0.4, 1.2))))
    distinct_stops(cs, info, leave, missed)
    for c in cs.values():
        if not c.stopped_for_good():
            c.end = day_of(c.vd["WEEK 52"], c.rand)
    nudge_exposure(cs, info, leave)
    return cs, info


def distinct_stops(cs, info, leave, missed):
    """arms whose count of patients stopping study drug for good equals an earlier arm's take one more stop for good,
    between the week-32 and week-40 visits, in a patient with no other change to study drug"""
    seen = set()
    for arm in P.ARMS:
        ids = sorted(s for s, c in cs.items() if c.arm == arm)
        n = sum(cs[s].stopped_for_good() for s in ids)
        while n in seen:
            cand = [s for s in ids if not cs[s].off and s not in leave and info[s]["ds_wrong"] is None
                    and ("WEEK 40" not in [v for (x, v) in missed if x == s])]
            s = cand[(len(cand) * 7) // 11]
            c = cs[s]
            day = (day_of(c.vd["WEEK 32"], c.rand) + day_of(c.vd["WEEK 40"], c.rand)) // 2
            c.off.append((day, None))
            info[s]["stop_reason"] = "PATIENT DECISION"
            n += 1
        seen.add(n)


def days_before_week52(c, left):
    """days on study drug before the week-52 visit (every day of a patient who left the study)"""
    cut = 10 ** 6 if left else day_of(c.vd["WEEK 52"], c.rand)
    last = min(c.last_dose(), cut - 1)
    tot = last
    for a, b in c.off:
        e = last + 1 if b is None else min(b, last + 1)
        if e > a:
            tot -= (e - a)
    return tot


def nudge_exposure(cs, info, leave):
    """lengthen or shorten a few of an arm's temporary holds (each still ending at least six days before the next
    visit) so the arm's patient-years before the week-52 visit sit well inside their one-decimal rounding bin"""
    taken = set()
    for arm in P.ARMS:
        ids = sorted(s for s, c in cs.items() if c.arm == arm)
        tot = sum(days_before_week52(cs[s], s in leave) for s in ids)
        v = tot / 365.25 * 10
        k = np.floor(v + 0.5)
        r = v - k
        if k in taken or k % 10 == 0:
            # another arm already rounds to this tenth: move into the neighbouring bin on the nearer side
            d = 1 if r >= 0 else -1
            need = int(round((k + d - 0.18 * d - v) * 36.525))
            taken.add(k + d)
        elif abs(r) <= 0.25:
            taken.add(k)
            continue
        else:
            need = int(round((np.sign(r) * 0.18 - r) * 36.525))   # days to add (shorter holds) or remove (longer holds)
            taken.add(k)
        holds = [(s, h) for s in ids for h in info[s]["holds"]]
        for s, (a, b) in holds:
            if need == 0:
                break
            c = cs[s]
            nxt = min(day_of(c.vd[v_], c.rand) for v_ in c.vd if v_ not in ("SCREENING",) and day_of(c.vd[v_], c.rand) > a)
            if need > 0:
                nb = max(a + 4, b - need)
            else:
                nb = min(nxt - 6, b - need)
            if nb == b:
                continue
            need -= (b - nb)
            c.off = sorted([(x, (nb if (x, y) == (a, b) else y)) for x, y in c.off], key=lambda t: t[0])
            info[s]["holds"] = [(x, (nb if (x, y) == (a, b) else y)) for x, y in info[s]["holds"]]


def noise_plan(rng, pats, vds, leave, missed):
    """fixed measurement draws for every attended visit, so a course can be measured again after calibration"""
    rows = []
    for _, p in pats.iterrows():
        s = p["SUBJID"]
        for v in attended(vds, leave, missed, s):
            dd = vds[s][v]
            rows.append({"SUBJID": s, "ARM": p["ARM"], "VISIT": v, "DATE": dd, "DAY": day_of(dd, p["RANDDT"]),
                         "AGE": p["AGE"] + (dd - p["SCRDT"]).days / 365.25, "SEX": p["SEX"], "HUB": p["LAB_HUB"]})
    return redraw(rng, rows)


def redraw(rng, rows):
    """the visit-level measurement error of creatinine (and the screening sample's)"""
    e = rng.normal(0, 0.021, (len(rows), 2))
    return [dict(r, E1=float(a), SCR_E=float(b)) for r, (a, b) in zip(rows, e)]


def parts(c, day, rsc):
    """the parts of a patient's true eGFR on a study day that do not move with the arm calibration"""
    p, d = c.p, c.dose
    base = p["G0"] + p["SLOPE"] * max(day - 1, 0) / 365.25
    for sd, size in c.extra:
        if day > sd:
            base += size * (1 - np.exp(-((day - sd) / 7.0) / P.REC_TAU_W))
    h0 = v = c0 = st = yo = 0.0
    if d > 0 and day >= 1:
        h0 = P.H[d] * p["H_MULT"]
        v = P.V[d] * p["V_MULT"] if p["LOOP"] else 0.0
        if c.ease_day is not None and day > c.ease_day:
            rho = min(p["RHO"] * rsc[d], 1.0)
            v *= 1 - rho * (1 - np.exp(-((day - c.ease_day) / 7.0) / P.REC_TAU_W))
        c0 = P.C[d] + p["C_DEV"]
        st, yo = c.state(day), c.years_on(day)
    return base, h0, v, c0, st, yo


def true_egfr(c, day, cal, rsc):
    base, h0, v, c0, st, yo = parts(c, day, rsc)
    if c.dose == 0 or day < 1:
        return base
    lvl, slo = cal[c.dose]
    return base - (h0 + lvl + v) * st + (c0 + slo) * yo


def components(cs, plan, rsc):
    """per measured visit, the parts of the true eGFR that do not move with the arm-level calibration"""
    import pandas as pd
    out = []
    for r in plan:
        c = cs[r["SUBJID"]]
        p, d, day = c.p, c.dose, r["DAY"]
        base, h0, v, c0, st, yo = parts(c, day, rsc)
        set_aside = bool(c.stopped_for_good() and r["VISIT"] != "SCREENING" and day >= c.stop_day())
        out.append(dict(r, BASE_G=base, H0=h0, VEFF=v, C0=c0, STATE=st, YO=yo, DOSE=d, G0=p["SCR_EGFR"],
                        SET_ASIDE=set_aside, W=E.NOMINAL.get(r["VISIT"])))
    return pd.DataFrame(out)


def ckd_vec(mg, age, female):
    k = np.where(female, 0.7, 0.9)
    a = np.where(female, -0.241, -0.302)
    r = mg / k
    g = 142.0 * np.minimum(r, 1.0) ** a * np.maximum(r, 1.0) ** -1.200 * 0.9938 ** age
    return g * np.where(female, 1.012, 1.0)


def scr_vec(egfr, age, female):
    lo, hi = np.full(len(egfr), 0.2), np.full(len(egfr), 15.0)
    for _ in range(56):
        mid = 0.5 * (lo + hi)
        up = ckd_vec(mid, age, female) > egfr
        lo, hi = np.where(up, mid, lo), np.where(up, hi, mid)
    return 0.5 * (lo + hi)


def measure(comp, cal):
    """the central laboratory's creatinine and eGFR at every attended scheduled visit, under the arm calibration"""
    df = comp.copy()
    lvl = df["DOSE"].map(lambda d: cal.get(d, (0.0, 0.0, 1.0))[0])
    slo = df["DOSE"].map(lambda d: cal.get(d, (0.0, 0.0, 1.0))[1])
    true = df["BASE_G"] - (df["H0"] + np.where(df["DOSE"] > 0, lvl, 0.0) + df["VEFF"]) * df["STATE"] + \
        (df["C0"] + np.where(df["DOSE"] > 0, slo, 0.0)) * df["YO"]
    scr = df["VISIT"].eq("SCREENING")
    true = np.where(scr, df["G0"], true)
    age = df["AGE"].astype(int).to_numpy()
    fem = df["SEX"].eq("F").to_numpy()
    mg = scr_vec(np.maximum(true, 9.0), age, fem) * np.where(scr, 1.0, np.exp(df["E1"]))
    cph = df["HUB"].eq("COPENHAGEN").to_numpy()
    umol = np.round(mg * 88.42)
    rep = np.where(cph, umol / 88.42, np.round(mg, 2))
    df["TRUE"] = true
    df["CREAT_MG"] = rep
    df["CREAT_ORIG"] = np.where(cph, umol.astype(int).astype(str), np.char.mod("%.2f", np.round(mg, 2)))
    df["CREAT_UNIT"] = np.where(cph, "umol/L", "mg/dL")
    df["EGFR"] = np.round(ckd_vec(rep, age, fem)).astype(int)
    return df


def recovery_scale(cs):
    """scale each arm's recovery so the arm's mean recovered fall matches the design's R"""
    cal = {}
    for d in (5, 10, 20, 40):
        tot, n = 0.0, 0
        for c in cs.values():
            if c.dose != d:
                continue
            n += 1
            if c.ease_day is not None and c.p["LOOP"]:
                tot += c.p["RHO"] * P.V[d] * c.p["V_MULT"]
        cal[d] = P.R_T[d] / (tot / n) if (tot > 0 and P.R_T[d] > 0) else 0.0
    return cal


def calibrate(comp, iters=4):
    """the arm-level level and slope shifts that put the measured week-52 difference and the 36-month difference
    from the chronic phase after week 24 on the design's targets"""
    cal = {d: (0.0, 0.0) for d in (5, 10, 20, 40)}
    for _ in range(iters):
        rt = E.routes(measure(comp, cal))
        new = {}
        for a in E.DOSES:
            d = P.DOSE[a]
            dw = P.W52_T[d] - rt[a]["w52"]
            dg = P.GOLD_T[d] - rt[a]["k24"]
            slo = (dg - dw) / 2.0
            lvl = dw - slo
            l0, s0 = cal[d]
            new[d] = (l0 - lvl, s0 + slo)
        cal = new
    return cal, measure(comp, cal)


def simulate(seed=P.SEED, noise_seed=None):
    """the whole trial before any extract is written: sites, patients, visits, potassium, dosing, the calibrated
    eGFR at every scheduled visit"""
    import world as W
    st = W.sites(np.random.default_rng(seed + 1))
    pats, fails = W.screen_and_randomise(np.random.default_rng(seed + 2), st, np.random.default_rng(seed + 900 + P.R_SHIFT))
    pats = W.baseline(np.random.default_rng(seed + 3), pats)
    vds, leave, missed = visit_dates(np.random.default_rng(seed + P.V_SHIFT), pats)
    pre = plan_stops(np.random.default_rng(seed + P.S_SHIFT), pats, vds, leave)
    krec, koff, kstop = potassium(np.random.default_rng(seed + P.K_SHIFT), pats, vds, leave, missed, pre)
    cs, info = courses(np.random.default_rng(seed + 8), pats, vds, leave, missed, pre, koff, kstop)
    plan = noise_plan(np.random.default_rng(seed + 7 if noise_seed is None else noise_seed), pats, vds, leave, missed)
    rsc = recovery_scale(cs)
    comp = components(cs, plan, rsc)
    cal, egfr = calibrate(comp)
    return {"sites": st, "pats": pats, "fails": fails, "vds": vds, "leave": leave, "missed": missed, "krec": krec,
            "cs": cs, "info": info, "rsc": rsc, "cal": cal, "comp": comp, "egfr": egfr}
