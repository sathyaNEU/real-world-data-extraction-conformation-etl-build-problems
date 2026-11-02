"""The clean truth of the VLT-317 phase 1 programme: subjects, dosing, PK, ECG and Holter, drawn from one seed."""
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import numpy as np

import params as P

BRU = ZoneInfo(P.TZ)
UTC = timezone.utc


def loc(dstr, hh=0, mm=0, ss=0):
    y, m, d = (int(x) for x in dstr.split("-"))
    return datetime(y, m, d, hh, mm, ss, tzinfo=BRU)


def wall(dt_local):
    """Local wall-clock hour of an aware datetime."""
    t = dt_local.astimezone(BRU)
    return t.hour + t.minute / 60.0 + t.second / 3600.0


def add(dt_local, minutes):
    """Elapsed-time addition (UTC arithmetic), returned in local time."""
    return (dt_local.astimezone(UTC) + timedelta(minutes=minutes)).astimezone(BRU)


def hours_between(a, b):
    return (b.astimezone(UTC) - a.astimezone(UTC)).total_seconds() / 3600.0


# ---------------------------------------------------------------- PK
def pk_micro(par):
    k10 = par["cl"] / par["v1"]
    k12 = par["q"] / par["v1"]
    k21 = par["q"] / par["v2"]
    s = k10 + k12 + k21
    disc = np.sqrt(s * s - 4 * k10 * k21)
    alpha = (s + disc) / 2
    beta = (s - disc) / 2
    return k10, k12, k21, alpha, beta


def conc_single(dt_h, dose_mg, par):
    """Plasma concentration (ng/mL) dt_h hours after one oral dose."""
    if dt_h <= 0:
        return 0.0
    k10, k12, k21, a, b = pk_micro(par)
    ka, v1 = par["ka"], par["v1"]
    D = dose_mg * 1000.0
    c = (D * ka / v1) * ((k21 - a) / ((ka - a) * (b - a)) * np.exp(-a * dt_h)
                         + (k21 - b) / ((ka - b) * (a - b)) * np.exp(-b * dt_h)
                         + (k21 - ka) / ((a - ka) * (b - ka)) * np.exp(-ka * dt_h))
    return float(max(c, 0.0))


def conc_at(t, dose_times, dose_mg, par):
    return sum(conc_single(hours_between(d, t), dose_mg, par) for d in dose_times)


# ---------------------------------------------------------------- physiology
def circ_q(h, s):
    return s["amp_q"] * np.cos(2 * np.pi * (h - s["phase_q"]) / 24.0)


def circ_h(h):
    return -P.PHYS["amp_h"] * np.cos(2 * np.pi * (h - P.PHYS["phase_h"]) / 24.0)


def build(seed=P.SEED, phys=None, drug=None, streams=None, holter=True):
    phys = dict(P.PHYS, **(phys or {}))
    drug = dict(P.DRUG, **(drug or {}))
    streams = dict(P.STREAMS, **(streams or {}))
    rng = np.random.default_rng(seed)
    W = {"subjects": [], "doses": [], "ecg": [], "pk": [], "amb": [], "holter": [], "recordings": [],
         "screening": [], "vitals": [], "safety_ecg": [], "phys": phys, "drug": drug}

    # volunteer panel and screening numbers
    vol_pool = sorted(rng.choice(np.arange(10120, 18990), size=160, replace=False).tolist())
    rng.shuffle(vol_pool)
    vol_iter = iter(vol_pool)
    scr_no = [0]

    def next_scr():
        scr_no[0] += 1
        return "E26-%04d" % (scr_no[0] + 113)

    sad_volunteers = []
    for study, design, cohorts, n_act, n_pl in P.STUDIES:
        subj_base = 1000 if study == "101" else 2000
        sn = 0
        for ci, (dose, dm1) in enumerate(cohorts):
            n = n_act + n_pl
            arms = [1] * n_act + [0] * n_pl
            rng.shuffle(arms)
            day_m1 = loc(dm1)
            # screening for this cohort: some failures, some re-screens, MAD reuses SAD volunteers
            scr_date = day_m1 - timedelta(days=int(rng.integers(9, 21)))
            for k in range(int(rng.integers(3, 6))):
                W["screening"].append(dict(volunteer="V%05d" % next(vol_iter), screening=next_scr(),
                                           date=(scr_date + timedelta(days=int(rng.integers(0, 4)))).date(),
                                           study=study, outcome="Screen failure"))
            for bed in range(1, n + 1):
                sn += 1
                subj = subj_base + sn
                reuse = (study == "102" and ci >= 1 and bed in (2, 7) and sad_volunteers)
                if reuse:
                    vol = sad_volunteers.pop(0)
                else:
                    vol = "V%05d" % next(vol_iter)
                    if study == "101" and ci <= 2 and bed in (3, 5):
                        sad_volunteers.append(vol)
                # a re-screen: first attempt failed for an earlier window, second randomised
                if (subj % 11) == 4:
                    W["screening"].append(dict(volunteer=vol, screening=next_scr(),
                                               date=(scr_date - timedelta(days=int(rng.integers(30, 60)))).date(),
                                               study=study, outcome="Screen failure"))
                scr = next_scr()
                W["screening"].append(dict(volunteer=vol, screening=scr,
                                           date=(scr_date + timedelta(days=int(rng.integers(0, 5)))).date(),
                                           study=study, outcome="Randomised"))
                s = dict(subject=subj, study=study, design=design, cohort=ci + 1, dose=dose, active=arms[bed - 1],
                         bed=bed, screening=scr, volunteer=vol, day_m1=day_m1,
                         beta=float(rng.normal(phys["beta_mu"], phys["beta_sd"])),
                         qtc0=float(rng.normal(phys["qtc0_mu"], phys["qtc0_sd"])),
                         hr0=float(rng.normal(phys["hr0_mu"], phys["hr0_sd"])),
                         amp_q=float(max(4.0, rng.normal(phys["amp_q_mu"], phys["amp_q_sd"]))),
                         phase_q=float(rng.normal(phys["phase_q_mu"], phys["phase_q_sd"])),
                         pr0=float(rng.normal(158, 16)), qrs0=float(rng.normal(94, 7)),
                         age=int(rng.integers(19, 55)), weight=round(float(rng.normal(76, 9)), 1))
                s["pk"] = dict(cl=P.PK["cl"] * np.exp(rng.normal(0, P.PK["cv_cl"])),
                               v1=P.PK["v1"] * np.exp(rng.normal(0, P.PK["cv_v1"])),
                               q=P.PK["q"] * np.exp(rng.normal(0, P.PK["cv_q"])),
                               v2=P.PK["v2"] * np.exp(rng.normal(0, P.PK["cv_v2"])),
                               ka=P.PK["ka"] * np.exp(rng.normal(0, P.PK["cv_ka"])))
                W["subjects"].append(s)

    # ------------------------------------------------------------ dosing and sampling per subject
    for s in W["subjects"]:
        s["rng_c"] = np.random.default_rng([seed, 1, s["subject"]])
        s["rng_h"] = np.random.default_rng([seed, 2, s["subject"]])
        s["rng_l"] = np.random.default_rng([streams["late"], s["subject"]])
    for s in W["subjects"]:
        rng = s["rng_c"]
        day1 = s["day_m1"] + timedelta(days=1)
        stagger = 4 * (s["bed"] - 1)
        ndays = P.MAD_DAYS if s["design"] == "MAD" else 1
        dts = []
        for d in range(ndays):
            date = (day1 + timedelta(days=d)).date().isoformat()
            jitter = int(rng.integers(-40, 75)) if d == 0 else int(rng.integers(-60, 150))
            t = loc(date, 8, 0) + timedelta(minutes=stagger, seconds=jitter)
            dts.append(t)
            W["doses"].append(dict(subject=s["subject"], study=s["study"], day=d + 1, time=t, dose=s["dose"]))
        s["dose_times"] = dts

    def conc(s, t):
        if not s["active"]:
            return 0.0
        return conc_at(t, s["dose_times"], s["dose"], s["pk"])

    # PK samples (inpatient) and triplicate ECGs
    for s in W["subjects"]:
        rng = s["rng_c"]
        rng_late = s["rng_l"]
        days = [1] + ([P.MAD_DAYS] if s["design"] == "MAD" else [])
        for d in days:
            t0 = s["dose_times"][d - 1]
            for nt in P.PK_TIMES:
                if nt == 0:
                    ts = add(t0, -float(rng.integers(12, 34)))
                else:
                    ts = add(t0, nt * 60 + float(rng.integers(3, 9)) + rng.uniform(0, 1))
                c = conc(s, ts)
                W["pk"].append(dict(subject=s["subject"], study=s["study"], day=d, nominal=nt, time=ts, true=c,
                                    obs=c * float(np.exp(rng.normal(0, P.PK["assay_cv"])))))
        if s["design"] == "MAD":
            for d in range(2, P.MAD_DAYS):
                ts = add(s["dose_times"][d - 1], -float(rng.integers(10, 30)))
                c = conc(s, ts)
                W["pk"].append(dict(subject=s["subject"], study=s["study"], day=d, nominal=0, time=ts, true=c,
                                    obs=c * float(np.exp(rng.normal(0, P.PK["assay_cv"])))))
        # ambulatory late samples (own stream)
        last = s["dose_times"][-1]
        lates = P.AMB_TIMES_SAD if s["design"] == "SAD" else P.AMB_TIMES_MAD
        for nt in lates:
            ts = add(last, nt * 60 + float(rng_late.integers(-55, 95)))
            c = conc(s, ts)
            W["amb"].append(dict(subject=s["subject"], volunteer=s["volunteer"], study=s["study"], nominal=nt,
                                 time=ts, true=c, obs=c * float(np.exp(rng_late.normal(0, P.PK["assay_cv"])))))
        # ECG triplicates: Day -1 at the Day 1 clock times, Day 1, Day 10
        ecg_days = [(-1, s["dose_times"][0] - timedelta(days=1))] + [(1, s["dose_times"][0])]
        if s["design"] == "MAD":
            ecg_days.append((P.MAD_DAYS, s["dose_times"][-1]))
        dose_wall = s["dose_times"][0].astimezone(BRU)
        base_naive = datetime(s["day_m1"].year, s["day_m1"].month, s["day_m1"].day,
                              dose_wall.hour, dose_wall.minute, dose_wall.second)
        for d, t0 in ecg_days:
            for nt in P.ECG_TIMES:
                back = float(rng.integers(4, 9))
                if d == -1:
                    # time-matched baseline: the same wall-clock times on the day before dosing
                    te = (base_naive + timedelta(minutes=nt * 60 - back)).replace(tzinfo=BRU)
                else:
                    te = add(t0, nt * 60 - back)
                h = wall(te)
                c = conc(s, te) if d != -1 else 0.0
                hr_tp = (s["hr0"] + phys["supine_circ_share"] * circ_h(h) + drug["s_hr"] * c
                         + rng.normal(0, phys["tp_hr_sd"]))
                qtc_tp = s["qtc0"] + circ_q(h, s) + drug["s_qt"] * c + rng.normal(0, phys["tp_qtc_sd"])
                reps = []
                for r in range(3):
                    hr = hr_tp + rng.normal(0, phys["rep_hr_sd"])
                    rr = 60000.0 / hr
                    qt = qtc_tp * (rr / 1000.0) ** s["beta"] + rng.normal(0, phys["rep_qt_sd"])
                    pr = s["pr0"] - 0.35 * (hr - s["hr0"]) + rng.normal(0, 4)
                    qrs = s["qrs0"] + rng.normal(0, 2.5)
                    readable = rng.random() > 0.016
                    reps.append(dict(rr=rr, hr=hr, qt=qt, pr=pr, qrs=qrs, ok=readable,
                                     time=add(te, 0.5 * r + rng.uniform(0, 0.3))))
                W["ecg"].append(dict(subject=s["subject"], study=s["study"], day=d, nominal=nt, time=te,
                                     conc=c, reps=reps))

    # ------------------------------------------------------------ Holter recordings
    if not holter:
        return W
    rng3 = np.random.default_rng([seed, 3])
    serials = sorted(rng3.choice(np.arange(40100, 48900), size=60, replace=False).tolist())
    rec_no = [0]

    def rec_id():
        rec_no[0] += 1
        return "H26-%04d" % (rec_no[0] + 380)

    cohorts = {}
    for s in W["subjects"]:
        cohorts.setdefault((s["study"], s["cohort"]), []).append(s)
    for key in sorted(cohorts):
        subs = sorted(cohorts[key], key=lambda x: x["bed"])
        n = len(subs)
        day_m1 = subs[0]["day_m1"]
        day1 = (day_m1 + timedelta(days=1)).date().isoformat()
        day2 = (day_m1 + timedelta(days=2)).date().isoformat()
        pool = list(rng3.permutation(serials))
        rng_x = np.random.default_rng([streams["exchange"], int(key[0]), key[1]])
        # exchange after the 12-hour extraction, bed by bed (own stream)
        x = loc(day1, 20, 52 if n > 8 else 40) + timedelta(seconds=int(rng_x.integers(0, 120)))
        powers = loc(day1, 20, 31) + timedelta(seconds=int(rng_x.integers(0, 50)))
        order = list(rng_x.permutation(n))
        for i, s in enumerate(subs):
            hook = loc(day_m1.date().isoformat(), 7, 10) + timedelta(minutes=4 * (s["bed"] - 1),
                                                                      seconds=int(rng3.integers(0, 150)))
            s["rec1"] = dict(id=rec_id(), serial="RX-%d" % pool[2 * i], start=hook, stop=x)
            s["rec2"] = dict(id=None, serial="RX-%d" % pool[2 * i + 1],
                             start=powers + timedelta(seconds=int(order[i] * 22 + rng_x.integers(0, 12))),
                             attach=x + timedelta(seconds=int(rng_x.integers(62, 135))),
                             stop=loc(day2, 9, 0) + timedelta(minutes=3 * (s["bed"] - 1),
                                                              seconds=int(rng_x.integers(0, 100))))
            x = x + timedelta(seconds=int(rng_x.integers(780, 960)))
        for s in sorted(subs, key=lambda q: q["rec2"]["start"]):
            s["rec2"]["id"] = rec_id()
        for s in subs:
            rng = s["rng_h"]
            sleep_on = [loc((day_m1 + timedelta(days=k)).date().isoformat(), 23, 0)
                        + timedelta(minutes=float(rng.uniform(8, 42))) for k in range(2)]
            wake = [loc((day_m1 + timedelta(days=k + 1)).date().isoformat(), 6, 30)
                    + timedelta(minutes=float(rng.uniform(0, 16))) for k in range(2)]

            def asleep(t):
                return any(a <= t < b for a, b in zip(sleep_on, wake))

            z = 0.0
            sl = 0.0
            for which in ("rec1", "rec2"):
                r = s[which]
                W["recordings"].append(dict(id=r["id"], serial=r["serial"], subject=s["subject"], study=s["study"],
                                            cohort=s["cohort"], start=r["start"], stop=r["stop"],
                                            kind=which, attach=r.get("attach")))
                t = r["start"]
                while t < r["stop"]:
                    end = min(t + timedelta(seconds=300), r["stop"])
                    dur = (end - t).total_seconds()
                    if dur < 30:
                        break
                    on_from = r.get("attach") or r["start"]
                    valid_frac = max(0.0, min(1.0, (end - max(t, on_from)).total_seconds() / dur))
                    mid = t + timedelta(seconds=dur / 2)
                    h = wall(mid)
                    a = asleep(mid)
                    z = phys["act_phi"] * z + np.sqrt(1 - phys["act_phi"] ** 2) * rng.normal()
                    sl = 0.8 * sl + 0.6 * rng.normal()
                    act = 0.0 if a else phys["act_scale"] * max(0.0, z + 0.25)
                    c = conc(s, mid)
                    hr = (s["hr0"] + phys["ambul_offset"] + circ_h(h) - (phys["sleep_drop"] if a else 0.0)
                          + act + (1.2 * sl if a else 0.0) + drug["s_hr"] * c + rng.normal(0, phys["seg_hr_sd"]))
                    rr = 60000.0 / hr
                    qt = ((s["qtc0"] + circ_q(h, s) + drug["s_qt"] * c + rng.normal(0, phys["seg_qtc_sd"]))
                          * (rr / 1000.0) ** s["beta"] + rng.normal(0, phys["seg_qt_sd"]))
                    noise = 100.0 * (1 - valid_frac)
                    if valid_frac >= 1.0:
                        noise = float(min(40.0, rng.gamma(1.3, 2.2)))
                        if rng.random() < 0.012 and not a:
                            noise = float(rng.uniform(55, 96))
                    W["holter"].append(dict(rec=r["id"], serial=r["serial"], subject=s["subject"], study=s["study"],
                                            cohort=s["cohort"], start=t, dur=dur, hr=hr, rr=rr, qt=qt,
                                            noise=noise, valid_frac=valid_frac, asleep=a, conc=c, kind=which,
                                            vpb=int(rng.poisson(0.25 if not a else 0.12))))
                    t = end
    return W


def drug_free_segments(W, subject):
    s = next(x for x in W["subjects"] if x["subject"] == subject)
    return [g for g in W["holter"] if g["subject"] == subject and g["kind"] == "rec1"
            and g["start"] + timedelta(seconds=g["dur"]) <= s["dose_times"][0]]
