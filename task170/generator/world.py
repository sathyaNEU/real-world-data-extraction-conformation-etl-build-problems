"""The clean truth: facilities, children on ART and every clinic visit from enrolment, simulated month by month.

Growth. A child's weight from age six rises on its own straight line, w9 + v (age - 9), with a slow AR(1) wander
around it; before six it follows a concave curve from birth to the line. The children diagnosed early (the
background, born 2005 to 2026, fewer each year as PMTCT improved) sit near 25.6 kg at nine and gain about 3.0 kg a
year; the cohort the 2021-22 catch-up campaign put on treatment (born around January 2016, diagnosed at five or six)
sits near 22.3 kg at nine and gains about 2.4 kg a year.

Weighing. A clinic weighing reads the child's weight plus clothing (0.3 kg on average) plus a scatter of 1.3 kg, to
0.1 kg (to 0.5 kg on the legacy register's paper-captured sites). A caregiver collecting a child's medicines records
no weight. A child on a first-line paediatric regimen moves onto TLD at the first weighing that reads 30.0 kg or more
and stays on it; a child on the second-line paediatric regimen moves onto the adult second line instead.

Visits. Each child keeps a dispensing interval of one, two or three months (some moved from monthly to multi-month
dispensing during 2023-25) and is seen on about the same day of the month; the next appointment is the visit date plus
the interval. Exits (lost to follow-up, transferred out of the programme, died) come at a monthly hazard by age; a
child is lost to follow-up 28 days after the first appointment missed."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as C

D = dt.date

P = dict(sig=1.3, bias=0.3, sdb=0.25, rho=0.85,
         surge_n=14000, surge_c=C.mi(2016, 1), surge_sd=5.0, surge_enrol=(C.mi(2021, 2), 15),
         bg_n0=1900, bg_decay=0.11, w9_bg=25.6, w9_surge=22.3, w9_sd=1.5,
         v_bg=3.0, v_surge=2.4, v_sd=0.25,
         cad_final=(0.65, 0.27, 0.08), p_cad_change=0.30,
         h_lo=0.004, h_hi=0.006, p_pickup=0.04, p_second=0.03, p_transfer=0.035,
         paper_share=0.40, small=15.0, small_floor=0.2)


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
    fdist = np.array([f["district"] for f in F])
    # children: background births 2005-2026, the 2015-16 cohort
    rows = []
    for by in range(2005, 2027):
        n = int(PP["bg_n0"] * np.exp(-PP["bg_decay"] * (by - 2005))) + 40
        b = C.mi(by, 1) + rng.integers(0, 12, n)
        e = b + np.maximum(1, rng.gamma(1.5, 8.0, n).astype(int))
        rows.append((b, e, np.zeros(n, int)))
    n = PP["surge_n"]
    e0, e1 = PP["surge_enrol"]
    b = np.round(PP["surge_c"] + rng.normal(0, PP["surge_sd"], n)).astype(int)
    e = e0 + rng.integers(0, e1, n)
    rows.append((b, e, np.ones(n, int)))
    bm = np.concatenate([r[0] for r in rows])
    enrol = np.concatenate([r[1] for r in rows])
    kind = np.concatenate([r[2] for r in rows])
    keep = (enrol >= bm + 1) & (enrol <= C.M_COUNT)
    bm, enrol, kind = bm[keep], enrol[keep], kind[keep]
    N = len(bm)
    sex = rng.integers(0, 2, N)
    w9 = rng.normal(np.where(kind == 1, PP["w9_surge"], PP["w9_bg"]), PP["w9_sd"])
    v = np.maximum(1.2, rng.normal(np.where(kind == 1, PP["v_surge"], PP["v_bg"]), PP["v_sd"]))
    T = C.M_END_SIM + 1
    tm = np.arange(T)
    age = (tm[None, :] - bm[:, None]) / 12.0
    w6 = w9 - 3 * v
    base = np.where(age >= 6, w9[:, None] + v[:, None] * (age - 9),
                    3.2 + (w6[:, None] - 3.2) * np.clip(age, 0, 6) ** 0.75 / 6 ** 0.75).astype(np.float32)
    rho, sdb = PP["rho"], PP["sdb"]
    bdev = np.zeros((N, T), np.float32)
    bdev[:, 0] = rng.normal(0, sdb, N)
    ein = rng.normal(0, sdb * np.sqrt(1 - rho ** 2), (N, T)).astype(np.float32)
    for t in range(1, T):
        bdev[:, t] = rho * bdev[:, t - 1] + ein[:, t]
    del ein
    # dispensing interval: final interval, and for some children monthly until a change month
    cad_final = rng.choice([1, 2, 3], N, p=list(PP["cad_final"]))
    change = np.where((cad_final > 1) & (rng.random(N) < PP["p_cad_change"]),
                      rng.integers(C.mi(2023, 3), C.mi(2025, 10), N), -1)
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
    del U, hz
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
    jitter = rng.integers(-3, 4, (N, T)).astype(np.int8)
    W = dict(P=PP, F=F, N=N, bm=bm, enrol=enrol, kind=kind, sex=sex, w9=w9, v=v, base=base, bdev=bdev,
             cad_final=cad_final, change=change, fac0=fac0, fac1=fac1, tr_month=tr_month, second=second,
             exitm=exitm, xtype=xtype, day0=day0, noise=noise, upick=upick, jitter=jitter, rng=rng)
    visits(W)
    return W


def cadence(W, i, t):
    c = W["change"][i]
    if c >= 0 and t < c:
        return 1
    return int(W["cad_final"][i])


def visit_date(W, i, t):
    y, m = C.ym(t)
    d = int(min(28, max(1, W["day0"][i] + W["jitter"][i, t])))
    return D(y, m, d)


def visits(W):
    """Every visit from enrolment to the exit (or to December 2027 for the truth beyond the count): month, date,
    weighing (None for a caregiver collection), regimen, months dispensed. The switch is taken on the visit's
    reading. Paper-captured legacy sites record to 0.5 kg. A small child's reading (an infant or baby scale, light
    clothing) scatters less: the scatter and the clothing allowance shrink in proportion below 15 kg."""
    PP = W["P"]
    N = W["N"]
    F = W["F"]
    stop_all = C.M_END_SIM + 1
    vi, vt, vw, vreg, vcad, vfac = [], [], [], [], [], []
    switch = np.full(N, 10 ** 6)
    paper = np.array([f["paper"] for f in F])
    for i in range(N):
        t = int(W["enrol"][i])
        stop = int(min(W["exitm"][i], stop_all))
        on_adult = False
        sec = bool(W["second"][i])
        while t < stop:
            fac = int(W["fac1"][i]) if (W["tr_month"][i] >= 0 and t >= W["tr_month"][i]) else int(W["fac0"][i])
            first = t == W["enrol"][i]
            if (not first) and W["upick"][i, t] < PP["p_pickup"]:
                w = None
            else:
                if float(W["base"][i, t]) >= PP["small"]:
                    x = float(W["base"][i, t] + W["bdev"][i, t] + PP["bias"] + W["noise"][i, t])
                else:
                    sc = max(PP["small_floor"], float(W["base"][i, t]) / PP["small"])
                    x = float(W["base"][i, t] + W["bdev"][i, t]) + (PP["bias"] + float(W["noise"][i, t])) * sc
                if t <= C.mi(2024, 5) and paper[fac]:
                    w = round(round(x * 2) / 2, 1)
                else:
                    w = round(x, 1)
            if (w is not None) and w >= 30.0 and not on_adult:
                on_adult = True
                switch[i] = t
            if on_adult:
                reg = "A2-TD3DRV" if sec else C.REG_TLD
            else:
                if sec:
                    reg = "P2-AZ3LR"
                else:
                    wt = float(W["base"][i, t] + W["bdev"][i, t]) if w is None else w
                    reg = "P1-AB3D10" if wt < 20.0 else "P1-AB3D50"
            cd = cadence(W, i, t)
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
