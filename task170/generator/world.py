"""The clean truth: facilities, children on ART and every clinic visit from enrolment, simulated month by month.

Growth. A child's weight from five and a half rises on its own straight line, w9 + v (age - 9), with a slow AR(1)
wander around it, a season (heavier after the harvest) and puberty's extra gain from its own onset; before five and a
half it follows a concave curve from birth weight. The children diagnosed in infancy (born 2005 to 2026, fewer each
year as PMTCT improved) sit near 25.6 kg at nine and gain about 3.0 kg a year; the 2021-22 catch-up campaign's
children (born 2011 to 2018, diagnosed at three to ten) are the more stunted, and grow the more slowly, the older they
were diagnosed.

Weighing. A clinic weighing reads the child's weight plus clothing (0.3 kg on average) plus the site scale's own offset
and a scatter of about 1.25 kg times the scale's own factor, to 0.1 kg (to 0.5 kg on the legacy register's
paper-captured sites); an infant's reading scatters less below 10 kg. A caregiver collecting a child's medicines records
no weight. A child on a first-line paediatric regimen moves onto TLD at the first weighing that reads the band (35 kg
until the 2026 guidelines took effect on 1 March 2026, 30 kg from then) or, for about one in ten, at the next clinical
visit; a child on TLD is never moved back. A child on the second-line paediatric regimen moves onto the adult second
line instead.

Visits. Each child keeps a dispensing interval of one, two or three months (mostly one before the 2026 guidelines; from
a month of the March to August 2026 rollout, its own on a paediatric regimen and its own on an adult one) and is seen
on about the same day of the month; the next appointment is the visit date plus the interval. Exits (lost to
follow-up, transferred out of the programme, died) come at a monthly hazard by age; a child is lost to follow-up 28
days after the first appointment missed."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as C

D = dt.date

P = dict(sig=1.25, bias=0.3, sdb=0.25, rho=0.85,
         fac_bias_sd=0.25, fac_sig_sd=0.08,               # each site's scale: an offset (kg) and a scatter multiplier
         season=0.08,                                     # kg either side of the year's mean, highest in September
         bg_n0=1900, bg_decay=0.11,                       # perinatal infections diagnosed in infancy, by birth year
         catch_max=12000, catch_n=7040,                   # the 2021-22 catch-up campaign: children enrolled (placed)
         catch_years=(2011, 2018), catch_w=(0.05, 0.09, 0.14, 0.18, 0.19, 0.16, 0.11, 0.08),
         catch_enrol=(C.mi(2021, 2), 15),
         w9_bg=25.6, w9_catch=22.3, w9_sd=1.5, v_bg=3.0, v_catch=2.4, v_sd=0.6, w9_age=-0.6, v_age=-0.12,
         pub_f=12.5, pub_m=13.5, pub_sd=0.6, pub_delay=1.5, pub_dv_f=2.5, pub_dv_m=3.0, pub_s=0.4,
         cad_pre=(0.75, 0.20, 0.05), mmd_start=C.mi(2026, 3), mmd_ramp=6, cad_paed=(0.35, 0.45, 0.20),
         cad_tld=(0.25, 0.15, 0.60),
         h_lo=0.002, h_hi=0.003, p_pickup=0.04, p_second=0.03, p_transfer=0.035, lag=0.10,
         thr_old=35.0, thr_from=C.mi(2026, 3),            # TLD from 35 kg until the 2026 guidelines, 30 kg from March
         paper_share=0.40, small=10.0, small_floor=0.2)


def _luhn_digit(s):
    tot = 0
    for k, ch in enumerate(reversed(s)):
        d = int(ch)
        if k % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        tot += d
    return str((10 - tot % 10) % 10)


def facilities(rng):
    """ART sites by district: one district hospital each, health centres, clinics; mission hospitals in the rural
    districts, private sites in the capital. MFL codes are national five-digit numbers."""
    out = []
    code = 10013
    for dc, dn, reg, reg_old, share in C.DISTRICTS:
        n = int(round(share * 410))
        types = ["District hospital"] + ["Health centre"] * max(2, n // 4)
        if reg in ("Capital",):
            types += ["Private clinic"] * 3
        elif rng.random() < 0.5:
            types += ["Mission hospital"]
        types += ["Clinic"] * max(0, n - len(types))
        for t in types:
            code += int(rng.integers(3, 29))
            size = {"District hospital": 9.0, "Mission hospital": 5.0, "Health centre": 2.6, "Private clinic": 1.0,
                    "Clinic": 1.0}[t] * float(rng.lognormal(0, 0.35))
            out.append(dict(mfl=str(code), type=t, district=dc, region=reg, region_old=reg_old, size=size,
                            paper=bool(rng.random() < C_P_PAPER(t)), day=int(rng.integers(2, 27)), closing=False))
    # seven small sites in districts the boundary change left alone close in early 2026 (their codes are reissued);
    # one in each region where one exists, adult patients only
    pool = [k for k, f in enumerate(out) if f["type"] in ("Clinic", "Private clinic", "Mission hospital")
            and f["region"] == f["region_old"]]
    order = [pool[j] for j in rng.permutation(len(pool))]
    used, chosen = set(), []
    for k in order:
        if out[k]["region"] in used and len(used) < 6:
            continue
        chosen.append(k)
        used.add(out[k]["region"])
        if len(chosen) == 7:
            break
    for k in chosen:
        out[k]["closing"] = True
    return out


def C_P_PAPER(t):
    return {"District hospital": 0.1, "Mission hospital": 0.3, "Health centre": 0.35, "Private clinic": 0.0,
            "Clinic": 0.55}[t]


def simulate(seed=C.SEED, **kw):
    PP = dict(P)
    PP.update(kw)
    rng = np.random.default_rng(seed)
    F = facilities(rng)
    fsize = np.array([0.0 if f["closing"] else f["size"] for f in F])
    # each site's scale: an offset and a scatter of its own
    fbias = rng.normal(0, PP["fac_bias_sd"], len(F))
    fsig = np.exp(rng.normal(0, PP["fac_sig_sd"], len(F)))
    # children: perinatal infections diagnosed in infancy, born 2005-2026; the 2021-22 catch-up campaign's children,
    # born 2011-2018 and diagnosed at three to ten. Every child of the campaign's largest size is drawn, and the
    # first catch_n of them kept, so the campaign's size changes nothing else in the world.
    rows = []
    for by in range(2005, 2027):
        n = int(PP["bg_n0"] * np.exp(-PP["bg_decay"] * (by - 2005))) + 40
        b = C.mi(by, 1) + rng.integers(0, 12, n)
        e = b + np.maximum(1, rng.gamma(1.5, 8.0, n).astype(int))
        ok = (e >= b + 1) & (e <= C.M_COUNT)
        rows.append((b[ok], e[ok], np.zeros(int(ok.sum()), int)))
    nmax = PP["catch_max"]
    y0, y1 = PP["catch_years"]
    by = rng.choice(np.arange(y0, y1 + 1), nmax, p=list(PP["catch_w"]))
    b = C.mi(2000, 1) + (by - 2000) * 12 + rng.integers(0, 12, nmax)
    e0, e1 = PP["catch_enrol"]
    e = e0 + rng.integers(0, e1, nmax)
    rows.append((b, e, np.ones(nmax, int)))
    bm = np.concatenate([r[0] for r in rows])
    enrol = np.concatenate([r[1] for r in rows])
    kind = np.concatenate([r[2] for r in rows])
    N = len(bm)
    cidx = np.cumsum(kind) - 1
    sel = (kind == 0) | (cidx < PP["catch_n"])
    sex = rng.integers(0, 2, N)
    # the campaign's children are the more stunted, and grow the more slowly, the older they were diagnosed
    ae = np.where(kind == 1, (enrol - bm) / 12.0 - 6.0, 0.0)
    w9 = rng.normal(np.where(kind == 1, PP["w9_catch"] + PP["w9_age"] * ae, PP["w9_bg"]), PP["w9_sd"])
    v = np.maximum(1.2, rng.normal(np.where(kind == 1, PP["v_catch"] + PP["v_age"] * ae, PP["v_bg"]), PP["v_sd"]))
    # puberty: growth quickens from an age of its own (later for boys, later still after a late diagnosis)
    ap = rng.normal(np.where(sex == 0, PP["pub_f"], PP["pub_m"]), PP["pub_sd"]) + np.where(kind == 1, PP["pub_delay"], 0.0)
    dv = np.where(sex == 0, PP["pub_dv_f"], PP["pub_dv_m"]) * np.exp(rng.normal(0, 0.15, N))
    T = C.M_END_SIM + 1
    tm = np.arange(T)
    age = (tm[None, :] - bm[:, None]) / 12.0
    # growth: the child's own straight line from five and a half (w9 at nine, v a year), a concave curve from birth
    # weight up to it, puberty's extra gain from its onset
    w55 = (w9 - 3.5 * v)[:, None]
    vv = v[:, None]
    s_ = PP["pub_s"]
    pub = dv[:, None] * s_ * np.logaddexp(0, (age - ap[:, None]) / s_)
    pub -= (dv * s_ * np.logaddexp(0, (9.0 - ap) / s_))[:, None]
    base = np.where(age >= 5.5, w55 + vv * (age - 5.5) + np.maximum(pub, 0),
                    3.2 + (w55 - 3.2) * (np.clip(age, 0, 5.5) / 5.5) ** 0.55)
    del pub
    # the season: heaviest after the harvest (September), lightest in the hungry months (March)
    season = PP["season"] * np.sin(2 * np.pi * ((tm % 12) - 5) / 12.0)
    base = (base + np.where(age >= 2, season[None, :], 0.0)).astype(np.float32)
    rho, sdb = PP["rho"], PP["sdb"]
    bdev = np.zeros((N, T), np.float32)
    bdev[:, 0] = rng.normal(0, sdb, N)
    ein = rng.normal(0, sdb * np.sqrt(1 - rho ** 2), (N, T)).astype(np.float32)
    for t in range(1, T):
        bdev[:, t] = rho * bdev[:, t - 1] + ein[:, t]
    del ein
    # dispensing interval: each child's own before the 2026 guidelines; from a month in their rollout, its own on a
    # paediatric regimen and its own on an adult one
    cad_pre = rng.choice([1, 2, 3], N, p=list(PP["cad_pre"]))
    cad_paed = rng.choice([1, 2, 3], N, p=list(PP["cad_paed"]))
    cad_tld = rng.choice([1, 2, 3], N, p=list(PP["cad_tld"]))
    mmd_m = PP["mmd_start"] + rng.integers(0, PP["mmd_ramp"], N)
    # facility, second line, transfers
    p = fsize / fsize.sum()
    fac0 = rng.choice(len(F), N, p=p)
    second = rng.random(N) < PP["p_second"]
    tr_month = np.where(rng.random(N) < PP["p_transfer"], rng.integers(C.mi(2023, 1), C.mi(2026, 7), N), -1)
    fac1 = rng.choice(len(F), N, p=p)
    # exits: monthly hazard by age from the month after enrolment
    U = rng.random((N, T)).astype(np.float32)
    hz = np.where(age < 12, PP["h_lo"], PP["h_hi"]).astype(np.float32)
    ex = (U < hz) & (tm[None, :] > enrol[:, None])
    del U, hz, age
    exitm = np.where(ex.any(1), ex.argmax(1), 10 ** 6)
    del ex
    # transfer to adult care at the twentieth birthday
    adult = bm + 240
    exitm_adult = np.where(adult < exitm, adult, 10 ** 6)
    exitm = np.minimum(exitm, exitm_adult)
    xtype = rng.choice(["LTFU", "TO", "DIED"], N, p=[0.6, 0.3, 0.1])
    xtype = np.where(exitm == exitm_adult, "ADULT", xtype)
    day0 = rng.integers(2, 27, N)
    noise = rng.normal(0, PP["sig"], (N, T)).astype(np.float32)
    upick = rng.random((N, T)).astype(np.float32)
    ulag = rng.random((N, T)).astype(np.float32)
    jitter = rng.integers(-3, 4, (N, T)).astype(np.int8)
    # the campaign's size: the first catch_n of its children kept
    keep = np.where(sel)[0]
    (bm, enrol, kind, sex, w9, v, ap, base, bdev, cad_pre, cad_paed, cad_tld, mmd_m, fac0, fac1, tr_month, second,
     exitm, xtype, day0, noise, upick, ulag, jitter) = [
        x[keep] for x in (bm, enrol, kind, sex, w9, v, ap, base, bdev, cad_pre, cad_paed, cad_tld, mmd_m, fac0, fac1,
                          tr_month, second, exitm, xtype, day0, noise, upick, ulag, jitter)]
    N = len(keep)
    W = dict(P=PP, F=F, N=N, bm=bm, enrol=enrol, kind=kind, sex=sex, w9=w9, v=v, ap=ap, base=base, bdev=bdev,
             cad_pre=cad_pre, cad_paed=cad_paed, cad_tld=cad_tld, mmd_m=mmd_m, fac0=fac0, fac1=fac1, tr_month=tr_month, second=second,
             exitm=exitm, xtype=xtype, day0=day0, noise=noise, upick=upick, ulag=ulag, jitter=jitter, fbias=fbias,
             fsig=fsig, rng=rng)
    visits(W)
    return W


def cadence(W, i, t, adult=False):
    """Months dispensed at a visit in month t: the child's interval before the rollout; after it, the child's own
    interval on a paediatric regimen or on an adult one (children under two or in their first six months of
    treatment stay monthly)."""
    if t < W["mmd_m"][i]:
        return int(W["cad_pre"][i])
    if (t - W["bm"][i]) < 24 or (t - W["enrol"][i]) < 6:
        return 1
    return int(W["cad_tld"][i] if adult else W["cad_paed"][i])


def visit_date(W, i, t):
    y, m = C.ym(t)
    d = int(min(28, max(1, W["day0"][i] + W["jitter"][i, t])))
    return D(y, m, d)


def visits(W):
    """Every visit from enrolment to the exit (or to December 2027 for the truth beyond the count): month, date,
    weighing (None for a caregiver collection, which dispenses the last clinical visit's regimen), regimen, months
    dispensed. A reading is the child's weight plus the site scale's offset, the clothing allowance and the scale's
    scatter; a small child's reading (an infant or baby scale, light clothing) scatters less below 15 kg. Paper-captured
    legacy sites record to 0.5 kg. A child on a paediatric first line weighed at 30.0 kg or more moves onto TLD at that
    visit, or at the next clinical visit where the clinician waits for TLD or for a second weighing; once on TLD a
    child is not moved back."""
    PP = W["P"]
    N = W["N"]
    F = W["F"]
    stop_all = C.M_END_SIM + 1
    vi, vt, vw, vreg, vcad, vfac = [], [], [], [], [], []
    switch = np.full(N, 10 ** 6)
    paper = np.array([f["paper"] for f in F])
    fbias, fsig = W["fbias"], W["fsig"]
    for i in range(N):
        t = int(W["enrol"][i])
        stop = int(min(W["exitm"][i], stop_all))
        on_adult = False
        pending = False
        sec = bool(W["second"][i])
        reg = None
        while t < stop:
            fac = int(W["fac1"][i]) if (W["tr_month"][i] >= 0 and t >= W["tr_month"][i]) else int(W["fac0"][i])
            first = t == W["enrol"][i]
            if (not first) and W["upick"][i, t] < PP["p_pickup"]:
                w = None
            else:
                sz = float(W["base"][i, t])
                sc = 1.0 if sz >= PP["small"] else max(PP["small_floor"], sz / PP["small"])
                x = sz + float(W["bdev"][i, t]) + (float(fbias[fac]) + PP["bias"] + float(W["noise"][i, t]) * float(fsig[fac])) * sc
                if t <= C.mi(2024, 5) and paper[fac]:
                    w = round(round(x * 2) / 2, 1)
                else:
                    w = round(x, 1)
            if not on_adult and w is not None:
                thr = 30.0 if t >= PP["thr_from"] else PP["thr_old"]
                if pending:
                    on_adult = True
                elif w >= thr:
                    if W["ulag"][i, t] < PP["lag"]:
                        pending = True
                    else:
                        on_adult = True
                if on_adult:
                    switch[i] = t
            if on_adult:
                reg = "A2-TD3DRV" if sec else C.REG_TLD
            elif w is None and reg is not None:
                pass
            elif sec:
                reg = "P2-AZ3LR"
            else:
                wt = float(W["base"][i, t] + W["bdev"][i, t]) if w is None else w
                reg = "P1-AB3D10" if wt < 20.0 else "P1-AB3D50"
            cd = cadence(W, i, t, on_adult)
            vi.append(i)
            vt.append(t)
            vw.append(np.nan if w is None else w)
            vreg.append(reg)
            vcad.append(cd)
            vfac.append(fac)
            t += cd
    W["switch"] = switch
    W["V"] = dict(i=np.array(vi), t=np.array(vt), w=np.array(vw), reg=np.array(vreg), cad=np.array(vcad),
                  fac=np.array(vfac))
