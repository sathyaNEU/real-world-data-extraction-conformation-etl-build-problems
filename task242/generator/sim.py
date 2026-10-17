"""task242 simulator: each zone's 2027 dengue infections by day of onset, the cases the city's surveillance notified,
the post-season household serosurvey (who was infected by the day their specimen was taken, and whether the IgM assay
found it), and the laboratory's verification panel. Every stream has its own seed so one part's draws never move
another's."""
import numpy as np

import params as P

LO, HI = -92, 372                         # 1 October 2026 to 8 January 2028
DAYS = np.arange(LO, HI + 1)


def rng(seed, k):
    return np.random.default_rng([seed, k])


def se_patient(t, fade):
    """chance a patient's serum is IgM-reactive t days after onset, for a patient whose IgM fades around `fade`"""
    t = np.clip(np.asarray(t, float), -50, 10 ** 4)
    rise = 1.0 / (1.0 + np.exp(-(t - P.SE_RISE) / P.SE_RISE_S))
    out = P.SE_MAX * rise / (1.0 + np.exp((t - fade) / P.SE_FADE_S))
    return np.where(t < 0, 0.0, out)


FADE_SD = 9.0                             # patient-to-patient spread of the fade


def se_true(t):
    """the population's detection curve: the patient curve averaged over the spread of fades"""
    q = np.linspace(-3, 3, 61)
    w = np.exp(-0.5 * q * q)
    w /= w.sum()
    t = np.atleast_1d(np.asarray(t, float))
    return np.sum([wi * se_patient(t, P.SE_FADE + qi * FADE_SD) for qi, wi in zip(q, w)], axis=0)


def zone_curve(z):
    """the zone's 2027 infections by onset day as a share of its population: waves plus the dry-season trickle"""
    code, name, kind, mid, waves, att = z[:6]
    c = np.zeros(DAYS.size)
    for lag, m, sd in waves:
        c += m * np.exp(-0.5 * ((DAYS - (mid - lag)) / sd) ** 2) / sd
    c[DAYS < 0] = 0.0
    c /= c.sum()
    bg = (DAYS >= 0).astype(float) * (0.35 + np.exp(-DAYS.clip(0) / 60.0) + 0.6 * np.exp(-0.5 * ((DAYS - 200) / 30.0) ** 2))
    bg /= bg.sum()
    return att * ((1 - P.BG_SHARE) * c + P.BG_SHARE * bg)


def tail_2026(z, k):
    """the 2026 north-east monsoon wave, onsets from October 2026, by day, as a share of the population"""
    peak = -52 + 6 * ((k * 7) % 5 - 2)
    c = np.exp(-0.5 * ((DAYS - peak) / 17.0) ** 2)
    c[DAYS >= 20] = 0.0
    return (0.025 + 0.004 * (k % 4)) * c / c.sum()


def read(W, i, day):
    """whether resident i was infected before `day` and whether the assay reads their serum taken that day as reactive"""
    i, day = np.asarray(i), np.asarray(day)
    inf = W["inf_day"][i] < day
    pos = np.where(inf, W["u_pos"][i] < se_patient(day - W["inf_day"][i], W["fade"][i]), W["u_fp"][i] < 1 - P.SP)
    return inf, pos


def make(seed=P.SEED):
    W = {"zones": []}
    for k, z in enumerate(P.ZONES):
        code, name, kind, mid, waves, att, pop, notif, nhh = z
        c, t = zone_curve(z), tail_2026(z, k)
        W["zones"].append(dict(code=code, name=name, kind=kind, mid=mid, start=mid - P.FIELD_HALF,
                               end=mid + P.FIELD_HALF, att=att, pop=pop, notif=notif, nhh=nhh,
                               curve=c + t * (DAYS >= 0), tail=t * (DAYS < 0)))
    # notified cases: each zone's infections thinned by its notified share, day by day
    r = rng(seed, 1)
    cases = []
    for k, z in enumerate(W["zones"]):
        lam = z["pop"] * (z["curve"] + z["tail"]) * z["notif"]
        n = r.poisson(lam)
        for d, m in zip(DAYS, n):
            cases.extend([(k, int(d))] * int(m))
    W["cases"] = np.array(cases, dtype=int)
    # the serosurvey: households, members, collection days; infection by collection day and the assay's reading
    r = rng(seed, 2)
    people = []
    for k, z in enumerate(W["zones"]):
        cum = np.cumsum(z["curve"])
        for h in range(z["nhh"]):
            day = int(r.integers(z["start"], z["end"] + 1))
            size = int(r.choice([1, 2, 3, 4, 5, 6, 7, 8], p=[0.06, 0.13, 0.19, 0.25, 0.18, 0.10, 0.05, 0.04]))
            for m in range(size):
                people.append((k, h, m, day))
    people = np.array(people, dtype=int)
    W["people"] = people
    k_, d_ = people[:, 0], people[:, 3]
    # each resident's infection day is fixed by one uniform through the zone's cumulative curve, so whether they were
    # infected by any day, and when, is the same whichever day their specimen is taken
    r = rng(seed, 3)
    u_inf, u_pos, u_fp = r.random(len(people)), r.random(len(people)), r.random(len(people))
    fade = P.SE_FADE + FADE_SD * r.standard_normal(len(people))
    inf_day = np.full(len(people), 10 ** 6)
    for k, z in enumerate(W["zones"]):
        cum = np.cumsum(z["curve"])
        m = k_ == k
        j = np.searchsorted(cum, u_inf[m], side="right")
        inf_day[m] = np.where(j < DAYS.size, DAYS[np.minimum(j, DAYS.size - 1)], 10 ** 6)
    W["u_pos"], W["u_fp"], W["fade"], W["inf_day"] = u_pos, u_fp, fade, inf_day
    W["A"] = np.array([np.cumsum(W["zones"][k]["curve"])[d - LO - 1] for k, d in zip(k_, d_)])
    W["inf"], W["igm"] = read(W, np.arange(len(people)), d_)
    # the verification panel: patients of the 2026 follow-up clinic, each seen at some scheduled visits, and controls
    r = rng(seed, 4)
    npat = 230
    fades = P.SE_FADE + FADE_SD * r.standard_normal(npat)
    onsets = r.integers(-150, -40, npat)            # onset days, August to November 2026
    panel = []
    for vday, spread, n in P.PANEL_VISITS:
        who = r.choice(npat, size=n, replace=False)
        for i in sorted(who):
            t = vday + int(r.integers(-spread, spread + 1))
            panel.append(("CASE", int(i), int(onsets[i]), t, bool(r.random() < se_patient(t, fades[i]))))
    r = rng(seed, 8)
    for j in range(P.PANEL_CONTROLS):
        panel.append(("CONTROL", j, None, None, bool(r.random() < 1 - P.SP)))
    W["panel"] = panel
    return W
