"""The cooperative's world: sections, transformers, five years of interruptions, the restoration steps, the
recloser operations, crew time, weather and the registers. Everything is drawn from one seed; nothing here
writes a file (pack.py does)."""
import numpy as np
import pandas as pd

P = dict(seed=434, wseed=37, sseed=5, st1=0.09, st2=0.03, p_unst=0.42, p_st=0.003, xf_p=0.0016, conn_share=0.25, r_shift=40,
         lam0=0.0019, r_t=-20.0)
D0 = pd.Timestamp("2020-10-01")                      # day 0, start of fiscal 2021
NDAY = (pd.Timestamp("2026-10-01") - D0).days        # through fiscal 2026
def day(s):
    return (pd.Timestamp(s) - D0).days
Y2 = day("2025-10-01"); R_DAY = day("2025-11-01"); G_DAY = day("2025-12-01"); E_DAY = day("2026-01-01")
F_DAY = day("2026-02-01"); GIS_DAY = day("2023-03-01"); RESECT = day("2026-06-01"); X0 = day("2021-10-01")
DISTRICTS = ["North", "Lakes", "Prairie", "River"]
_h = np.arange(1440) / 60.0
DIURNAL = 1 + 0.8 * np.exp(-((_h - 7.5) / 1.5) ** 2) + 0.9 * np.exp(-((_h - 18) / 2.0) ** 2) + 0.2 * (_h > 10) * (_h < 16)
DIURNAL = DIURNAL / DIURNAL.sum()


def uuid4s(rng, n):
    b = rng.integers(0, 256, size=(n, 16), dtype=np.uint8)
    b[:, 6] = (b[:, 6] & 0x0F) | 0x40
    b[:, 8] = (b[:, 8] & 0x3F) | 0x80
    h = [x.tobytes().hex() for x in b]
    return ["%s-%s-%s-%s-%s" % (s[:8], s[8:12], s[12:16], s[16:20], s[20:]) for s in h]


def weather(P):
    """Hourly temperature (C) at the headquarters substation, UTC hours, and the local-day mean."""
    rng = np.random.default_rng(P["wseed"])
    n = NDAY
    doy = (np.arange(n) + 274) % 365
    base = 5.5 - 17.5 * np.cos(2 * np.pi * (doy - 20) / 365)
    e = 0.0; dm = np.zeros(n)
    for i in range(n):
        e = 0.78 * e + rng.normal(0, 4.2); dm[i] = base[i] + e
    # fiscal 2026's winter ran colder than fiscal 2025's
    w26 = (np.arange(n) >= day("2025-11-20")) & (np.arange(n) < day("2026-03-05"))
    w25 = (np.arange(n) >= day("2024-11-20")) & (np.arange(n) < day("2025-03-05"))
    dm = dm - 3.0 * w26 + 2.5 * w25
    hrs = pd.date_range(D0 + pd.Timedelta(hours=6), periods=n * 24, freq="h")       # UTC hours of local days
    hh = np.tile(np.arange(24), n)
    amp = 4.0 + 1.5 * rng.random(n)
    t = np.repeat(dm, 24) - np.repeat(amp, 24) * np.cos(2 * np.pi * (hh - 9) / 24) + rng.normal(0, 0.6, n * 24)
    return dm, pd.DataFrame({"utc": hrs, "temp_c": np.round(t, 1)})


def run(P=P, full=True):
    rng = np.random.default_rng(P["seed"])
    dm, wx = weather(P)
    nf = 190
    nsec_f = rng.integers(2, 5, nf)
    sec_f = np.repeat(np.arange(nf), nsec_f); ns = len(sec_f)
    f_dist = rng.choice(4, nf, p=[0.27, 0.24, 0.26, 0.23])
    cust = np.clip(rng.lognormal(np.log(203), 0.55, ns), 35, 1000).round().astype(int)
    eheat = np.clip(rng.beta(2.2, 4, nf), 0.02, 0.9)[sec_f]
    ehm = np.round(cust * eheat).astype(int)
    urd = rng.random(ns) < 0.45
    oh = ~urd
    conn = (eheat > 0.18) & (rng.random(ns) < P["conn_share"])
    S = pd.DataFrame(dict(sec=np.arange(ns), feeder=sec_f, district=f_dist[sec_f], members=cust, eheat=eheat,
                          eheat_members=ehm, urd=urd, conn=conn))
    first = np.r_[True, sec_f[1:] != sec_f[:-1]]
    S["device"] = np.where(first, "SECT", np.where(rng.random(ns) < 0.38, "RCLR", "FUSE"))
    # feeders re-balanced on 1 June 2026: a few sections move to a neighbouring feeder in the same district
    S["feeder_new"] = S.feeder
    for dist in (2, 3):
        fs = np.where(f_dist == dist)[0]
        movers = rng.choice(np.where((S.district.values == dist) & ~first & (S.device.values != "RCLR"))[0], 5, replace=False)
        for s in movers:
            cand = [f for f in fs if f != sec_f[s]]
            S.loc[s, "feeder_new"] = int(rng.choice(cand))
    S["inst_trip"] = np.isin(S.district.values, [0, 1])
    # service transformers, about nine members each
    nx = np.maximum(1, np.round(cust / rng.uniform(7.5, 10.5, ns))).astype(int)
    X = pd.DataFrame(dict(sec=np.repeat(np.arange(ns), nx)))
    X["xf"] = np.arange(len(X))
    m = np.zeros(len(X), int)
    for s in range(ns):
        idx = np.where(X.sec.values == s)[0]
        m[idx] = rng.multinomial(cust[s], np.ones(len(idx)) / len(idx))
    X["members"] = np.maximum(m, 1)
    # rebate transformers on connected sections, each with its own connection date
    X["rebate"] = False; X["conn_day"] = -1
    for s in np.where(conn)[0]:
        idx = np.where(X.sec.values == s)[0]
        k = min(len(idx), int(rng.integers(3, 25)))
        pick = rng.choice(idx, k, replace=False)
        X.loc[pick, "rebate"] = True
        X.loc[pick, "conn_day"] = R_DAY + np.minimum(rng.gamma(1.6, 38, k).astype(int), 330)
    ev = []   # rows: sec, xf(-1 for section level), start minute, dur (min), kind, ci
    storm = (np.random.default_rng(P["sseed"]).random(NDAY) < np.where(np.arange(NDAY) < Y2, P["st1"], P["st2"])) \
        * np.random.default_rng(P["sseed"] + 1).gamma(1.6, 7.0, NDAY)
    _mj = np.random.default_rng(P["sseed"] + 2)
    for fy in range(6):                                   # one to three major storms a year
        for d in _mj.choice(np.arange(fy * 365 + 150, fy * 365 + 330), _mj.integers(1, 4), replace=False):
            storm[d] = _mj.uniform(45, 90)
    # animal guard sites (overhead lateral taps), riser terminations (underground sections)
    nsite = rng.integers(2, 7, ns) * oh
    G = pd.DataFrame(dict(sec=np.repeat(np.arange(ns), nsite)))
    G["site"] = np.arange(len(G))
    G["list_year"] = rng.choice([0, 2022, 2023, 2024, 2025, 2026], len(G), p=[0.62, 0.07, 0.07, 0.08, 0.08, 0.08])
    G["fit_day"] = np.where(G.list_year > 0, [day("%d-01-05" % y) if y else 0 for y in G.list_year], 10 ** 6)
    G["fit_day"] = G.fit_day + rng.integers(0, 24, len(G))
    G.loc[G.list_year == 2026, "fit_day"] = 10 ** 6                     # the programme ended before fitting
    nris = rng.integers(1, 4, ns) * urd
    Rr = pd.DataFrame(dict(sec=np.repeat(np.arange(ns), nris)))
    Rr["riser"] = np.arange(len(Rr))
    Rr["aged"] = rng.random(len(Rr)) < 0.42
    Rr["list_year"] = np.where(Rr.aged, rng.choice([0, 2022, 2023, 2024, 2025], len(Rr), p=[0.30, 0.16, 0.16, 0.16, 0.22]), 0)
    Rr["rep_day"] = [day("%d-10-06" % y) + int(rng.integers(0, 30)) if y and y < 2025 else 10 ** 6 for y in Rr.list_year]
    # transformer units: supplier and fit day per position
    U = pd.DataFrame(dict(xf=X.xf, fit_day=-rng.integers(400, 9000, len(X)), supplier="Halvorsen Electric"))
    new_units = []
    for d in range(NDAY):
        t = dm[d]
        lam = P["lam0"] * (1 + 0.8 * (t < -15) + 0.5 * (t > 27) + storm[d])
        n = rng.poisson(lam, ns)
        for s in np.repeat(np.arange(ns), n):
            m0 = d * 1440 + int(rng.choice(1440, p=DIURNAL))
            k = "storm" if storm[d] > 0 else "base"
            ev.append((s, -1, m0 + rng.random(), rng.lognormal(np.log(85), 0.75), k, cust[s]))
            if storm[d] > 0 and rng.random() < 0.06:
                ev.append((s, -1, m0 + ev[-1][3] + rng.integers(45, 300) + rng.random(), rng.lognormal(np.log(60), 0.6), "stormrep", cust[s]))
        # a section's own protection tripping on peak load on the hardest days (every year alike)
        if t < -22 or t > 30:
            for s in np.where(rng.random(ns) < 0.0009 * (0.4 + eheat * (t < 0)))[0]:
                ev.append((s, -1, d * 1440 + int(rng.choice(1440, p=DIURNAL)) + rng.random(), rng.lognormal(np.log(70), 0.5), "secovl", cust[s]))
        # transformer-level background (equipment, animal, weather, vehicle, rare overload)
        nb = rng.poisson(1.05 * (1 + 0.6 * (t < -18) + 0.7 * (t > 28) + 0.8 * storm[d]))
        for xf in rng.integers(0, len(X), nb):
            ev.append((X.sec.values[xf], xf, d * 1440 + rng.integers(0, 1440) + rng.random(), rng.lognormal(np.log(110), 0.6), "xbg", X.members.values[xf]))
        # animal contacts at overhead lateral sites; a guarded site after fitting almost never
        mo = (D0 + pd.Timedelta(days=int(d))).month
        season = 0.0 if mo in (12, 1, 2) else (1.6 if mo in (4, 5, 9, 10) else 1.0)
        pa = np.where(G.fit_day.values <= d, 0.000004, np.where(G.list_year.values > 0, 0.00019, 0.00006) * season)
        for gi in np.where(rng.random(len(G)) < pa)[0]:
            s = G.sec.values[gi]
            ev.append((s, -1, d * 1440 + rng.integers(330, 1230) + rng.random(), rng.lognormal(np.log(70), 0.5), "animal:%d" % gi, cust[s]))
        # riser termination failures in frost; a replaced termination is new
        if t < -10:
            pr = np.where(Rr.rep_day.values <= d, 0.0, np.where(Rr.aged.values, 0.0011, 0.00008)) * (1 + (t < -20))
            for ri in np.where(rng.random(len(Rr)) < pr)[0]:
                s = Rr.sec.values[ri]
                ev.append((s, -1, d * 1440 + rng.integers(0, 1440) + rng.random(), rng.lognormal(np.log(110), 0.5), "term:%d" % ri, cust[s]))
        # the heat pump policy's own harm: rebate transformers connected without a study blow fuses on peak cold
        if d >= R_DAY and t < P["r_t"] + 3:
            live = X.index[(X.rebate.values) & (X.conn_day.values <= d)]
            hit = live[rng.random(len(live)) < P["xf_p"] * (1 + (t < P["r_t"]) * 2.0)]
            for xf in hit:
                ev.append((X.sec.values[xf], xf, d * 1440 + int(rng.choice(1440, p=DIURNAL)) + rng.random(), rng.lognormal(np.log(95), 0.5), "hpovl", X.members.values[xf]))
        # unit failures: infant failures of new-supplier units, background ageing of the rest
        if d >= F_DAY:
            for _ in range(rng.poisson(1.2)):
                xf = int(rng.integers(0, len(X)))
                new_units.append((xf, d))
    # new-supplier units fitted from 1 February 2026; infant failures in their first months
    NU = pd.DataFrame(new_units, columns=["xf", "fit_day"]).drop_duplicates("xf")
    # the old supplier's replacement units fitted from fiscal 2022 until the change, with their own infant failures
    ou = []
    r2 = np.random.default_rng(P["seed"] + 77)
    for d in range(X0, F_DAY):
        for _ in range(r2.poisson(1.2)):
            ou.append((int(r2.integers(0, len(X))), d))
    OU = pd.DataFrame(ou, columns=["xf", "fit_day"]).drop_duplicates("xf")
    OU = OU[~OU.xf.isin(NU.xf)]
    ou_ev = []
    for xf, fd in OU.itertuples(index=False):
        if r2.random() < 0.004:
            fday = fd + int(r2.integers(10, 150))
            if fday < NDAY:
                ou_ev.append((X.sec.values[xf], xf, fday * 1440 + r2.integers(0, 1440) + r2.random(), r2.lognormal(np.log(150), 0.5), "oldunit", X.members.values[xf]))
    for xf, fd in NU.itertuples(index=False):
        if rng.random() < 0.075:
            fday = fd + int(rng.integers(10, 150))
            if fday < NDAY:
                ev.append((X.sec.values[xf], xf, fday * 1440 + rng.integers(0, 1440) + rng.random(), rng.lognormal(np.log(150), 0.5), "newunit", X.members.values[xf]))
    E = pd.DataFrame(ev, columns=["sec", "xf", "t0", "repair", "kind", "ci"])
    # restoration: before the revision, heating-season pickups after an hour or more were stepped
    E["d"] = (E.t0 // 1440).astype(int)
    E["temp"] = dm[np.minimum(E.d.values, NDAY - 1)]
    sec_lvl = E.xf.values < 0
    heat = np.isin((D0 + pd.to_timedelta(E.d.values, "D")).month, [11, 12, 1, 2, 3])
    long_ = E.repair.values >= 60
    staged = sec_lvl & heat & long_ & (E.t0.values + E.repair.values < G_DAY * 1440)
    nst = np.where(staged, rng.integers(2, 5, len(E)), np.where(sec_lvl & (rng.random(len(E)) < 0.2), 2, 1))
    gapm = rng.uniform(5, 15, len(E))
    E["steps"] = nst
    E["t_end"] = E.t0 + E.repair + (nst - 1) * gapm
    # cold load re-trips after a restoration of an hour or more in frost
    q = sec_lvl & (E.repair.values >= 60) & (E.temp.values <= -3) & ~np.isin(E.kind.values, ["stormrep"])
    x = (np.minimum(E.repair.values, 360) - 60) / 60.0 * np.maximum(-E.temp.values - 3, 0) / 10.0 \
        * np.maximum(eheat[E.sec.values] - 0.12, 0) * 5.0
    pre = E.t_end.values < G_DAY * 1440
    p = np.where(pre, P["p_st"], P["p_unst"]) * (1 - np.exp(-np.maximum(x, 0)))
    r = q & (rng.random(len(E)) < p)
    RT = pd.DataFrame(dict(sec=E.sec.values[r], xf=-1, t0=E.t_end.values[r] + rng.integers(0, 4, r.sum()) + rng.random(r.sum()),
                           repair=rng.lognormal(np.log(40), 0.4, r.sum()), kind="retrip", ci=cust[E.sec.values[r]]))
    RT["d"] = (RT.t0 // 1440).astype(int); RT["temp"] = dm[np.minimum(RT.d.values, NDAY - 1)]
    RT["steps"] = rng.integers(2, 4, len(RT)); RT["t_end"] = RT.t0 + RT.repair + (RT.steps - 1) * rng.uniform(5, 15, len(RT))
    inyr = (E.t_end.values >= G_DAY * 1440) & (E.t_end.values < NDAY * 1440)
    G_true = float(((P["p_unst"] - P["p_st"]) * (1 - np.exp(-np.maximum(x, 0))) * cust[E.sec.values] * (q & inyr)).sum())
    OE = pd.DataFrame(ou_ev, columns=["sec", "xf", "t0", "repair", "kind", "ci"])
    OE["d"] = (OE.t0 // 1440).astype(int); OE["temp"] = dm[np.minimum(OE.d.values, NDAY - 1)]
    OE["steps"] = 1; OE["t_end"] = OE.t0 + OE.repair
    E = pd.concat([E, RT, OE], ignore_index=True)
    E = E[E.t0 < NDAY * 1440].sort_values("t0").reset_index(drop=True)
    # members re-counted onto sibling transformers at the GIS audit: a few rebate transformers that tripped serve fewer
    hv = E[(E.kind == "hpovl") & (E.t0 >= Y2 * 1440)].groupby("xf").size()
    moved = 0
    for xf in hv[hv >= 2].index:
        if moved >= P.get("r_shift", 0):
            break
        s = X.sec.values[xf]
        sib = [i for i in X.index[X.sec.values == s] if not X.rebate.values[i] and i != xf and not (E.xf.values == i).any()]
        if not sib or X.members.values[xf] <= 3:
            continue
        X.loc[xf, "members"] -= 1; X.loc[sib[0], "members"] += 1
        E.loc[E.xf == xf, "ci"] = E.loc[E.xf == xf, "ci"] - 1
        moved += int(hv[xf])
    W = dict(S=S, X=X, G=G, Rr=Rr, U=U, NU=NU, OU=OU, E=E, dm=dm, wx=wx, storm=storm, rng=rng,
             G_true=G_true)
    return W
