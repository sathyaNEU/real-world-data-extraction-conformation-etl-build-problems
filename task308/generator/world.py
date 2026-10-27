"""The clean truth: ten recorded weather years at the cooperative's hub, the 2027 load and the contracted wind and
sun in them, every unit's forced outages, derates, planned work and the pipeline's curtailments of interruptible
service, the tie's outages, and the two renewable offers' modelled output. Nothing here is read by a solver; records.py
turns it into the pack."""
import numpy as np
import pandas as pd

import params as P


def hours():
    utc = pd.date_range(P.START_UTC, P.END_UTC, freq="h", tz="UTC")
    return utc, utc.tz_convert(P.TZ)


def _ar1(rng, n, phi, sd):
    e = rng.normal(0, sd, n)
    x = np.zeros(n)
    for i in range(1, n):
        x[i] = phi * x[i - 1] + e[i]
    return x


def weather(rng, utc, local):
    n = len(utc)
    doy = local.dayofyear.values
    hr = local.hour.values
    season = 45 - 33 * np.cos(2 * np.pi * (doy - 18) / 365.25)
    diurnal = 7 * np.sin(2 * np.pi * (hr - 9) / 24)
    temp = season + diurnal + _ar1(rng, n, 0.985, 1.1)
    cold = np.zeros(n)
    events = []
    for y in P.YEARS:
        for _ in range(int(rng.integers(1, 4))):
            day = int(rng.choice(list(range(2, 56)) + list(range(330, 362))))
            start = pd.Timestamp(y, 1, 1, tz=P.TZ) + pd.Timedelta(days=day, hours=int(rng.integers(0, 24)))
            s = int(np.searchsorted(utc, start.tz_convert("UTC")))
            dur = int(rng.integers(48, 120))
            depth = float(rng.uniform(14, 30))
            ramp = np.concatenate([np.linspace(0, 1, 18), np.ones(max(dur - 36, 1)), np.linspace(1, 0, 18)])
            L = min(len(ramp), n - s)
            if L <= 0:
                continue
            cold[s:s + L] = np.minimum(cold[s:s + L], -depth * ramp[:L])
            events.append((s, L, depth))
    temp = temp + cold
    return np.round(temp, 1), cold


def load_2027(rng, local, temp):
    hr = local.hour.values
    dow = local.dayofweek.values
    heat = np.clip(55 - temp, 0, None)
    cool = np.clip(temp - 72, 0, None)
    shape = 1 + 0.12 * np.sin(2 * np.pi * (hr - 13) / 24) + 0.05 * np.isin(hr, [7, 8, 18, 19])
    wk = np.where(dow >= 5, 0.94, 1.0)
    load = P.LOAD_SCALE * (1150 + 13.5 * heat + 0.11 * heat ** 2 + P.COOL_COEF * cool) * shape * wk
    return np.round(load + rng.normal(0, 25, len(load)), 1)


def renewables(rng, local, cold):
    n = len(local)
    doy = local.dayofyear.values
    hr = local.hour.values
    ws = _ar1(rng, n, 0.97, 0.25)
    wcf = 1 / (1 + np.exp(-(ws + 0.1 + 0.25 * np.cos(2 * np.pi * (doy - 60) / 365.25))))
    wcf = np.clip(wcf * np.where(cold < -8, 0.35, 1.0) * 0.9, 0, 1)
    dl = 12 + 3 * np.cos(2 * np.pi * (doy - 172) / 365.25)
    elev = np.clip(np.sin(np.pi * (hr + 0.5 - (12 - dl / 2)) / dl), 0, None)
    cloud = np.clip(rng.beta(2, 1.2, n // 24 + 2).repeat(24)[:n], 0.1, 1)
    scf = elev * cloud * (0.75 + 0.2 * np.cos(2 * np.pi * (doy - 172) / 365.25))
    # the offers' sites: Sandhill Draw sits 60 miles west of the contracted farms, Coulee Flats beside them
    wcf_new = np.clip(wcf * (0.88 + 0.24 * rng.random(n)) + _ar1(rng, n, 0.9, 0.01), 0, 0.98)
    scf_new = np.clip(scf * (0.93 + 0.1 * rng.random(n)), 0, 0.95)
    return wcf, scf, wcf_new, scf_new


def markov(rng, n, efor, mttr):
    """an hourly two-state process with the unit's forced outage rate and mean repair time: runs of hours out"""
    lam = efor / ((1 - efor) * mttr)
    mu = 1.0 / mttr
    st = np.ones(n, dtype=bool)
    up = True
    r = rng.random(n)
    for i in range(n):
        if up and r[i] < lam:
            up = False
        elif (not up) and r[i] < mu:
            up = True
        st[i] = up
    return st


def curtailment(temp):
    n = len(temp)
    curt = np.zeros(n, dtype=bool)
    run = 0
    for i in range(n):
        run = run + 1 if temp[i] < P.CURT_TEMP_F else 0
        if run >= P.CURT_PERSIST_H:
            curt[i - P.CURT_PERSIST_H + 1:i + P.CURT_TAIL_H + 1] = True
    return curt


def build(seed=P.SEED):
    rng = np.random.default_rng(seed)
    utc, local = hours()
    n = len(utc)
    temp, cold = weather(rng, utc, local)
    load = load_2027(rng, local, temp)
    wcf, scf, wcf_new, scf_new = renewables(rng, local, cold)
    curt = curtailment(temp)
    units = P.UNITS + P.RETIRED
    state = {}
    for code, plant, unit, cls, mw, efor, mttr, gas in units:
        state[code] = markov(rng, n, efor, mttr)
    tie = markov(rng, n, P.TIE_FOR, P.TIE_MTTR)
    return dict(utc=utc, local=local, temp=temp, cold=cold, load=load, wind_ex=np.round(P.WIND_EX_MW * wcf, 1),
                solar_ex=np.round(P.SOLAR_EX_MW * scf, 1), wcf_new=np.round(wcf_new, 4), scf_new=np.round(scf_new, 4),
                curt=curt, state=state, tie=tie, rng=rng)


# ------------------------------------------------------------------------------------------------ members, 2025
SUBSTATIONS = ["Ashby", "Bremer", "Cady Lake", "Dunmore", "Elmwood", "Fairhaven", "Garnet", "Hollins", "Ivanhoe",
               "Juniper", "Kettle Falls", "Larkin", "Mapleton", "Norway Center", "Oakes", "Pelican", "Quarry Road",
               "Rushford", "Sabin", "Thorpe", "Ulen", "Vining", "Waubun", "Yellow Bank", "Zumbro", "Alden",
               "Brandt", "Clontarf", "Danvers", "Esko", "Flom", "Gully", "Hanska", "Isle", "Jasper", "Kragnes",
               "Lowry", "Milan", "Nassau", "Odessa"]


def members(W, seed=P.SEED + 50):
    """each delivery point's true hourly delivered and received energy in 2025, and the field facts behind the
    metering devices"""
    rng = np.random.default_rng(seed)
    local = W["local"]
    m25 = local.year == P.METER_YEAR
    utc = W["utc"][m25]
    loc = local[m25]
    sysload = W["load"][m25] / 1.07 * 0.97
    hr = loc.hour.values
    doy = loc.dayofyear.values
    dps = []
    k = 0
    for mi, (name, share, ndp) in enumerate(zip(P.MEMBERS, P.MEMBER_SHARE, P.DP_PER_MEMBER)):
        w = rng.dirichlet(np.full(ndp, 3.0)) * share
        for j in range(ndp):
            kind = "industrial" if rng.random() < 0.18 else "rural"
            dps.append(dict(dp=f"DP-{101 + k:03d}", substation=SUBSTATIONS[k], member=name, weight=float(w[j]), kind=kind))
            k += 1
    true = {}
    for d in dps:
        base = sysload * d["weight"]
        if d["kind"] == "industrial":
            base = 0.6 * base.mean() + 0.4 * base
        load = base * (1 + rng.normal(0, 0.035, len(base))) * 1000.0      # kWh in the hour
        true[d["dp"]] = np.clip(load, 0, None)
    # member-owned generation behind six delivery points (a landfill gas engine and five solar arrays)
    gen_dps = [dps[i]["dp"] for i in rng.choice(len(dps), 6, replace=False)]
    elev = np.clip(np.sin(np.pi * (hr + 0.5 - 6.5) / 13), 0, None) * (0.7 + 0.3 * np.cos(2 * np.pi * (doy - 172) / 365.25))
    gen = {}
    for i, dp in enumerate(gen_dps):
        if i == 0:
            gen[dp] = np.full(len(hr), 3000.0) * (rng.random(len(hr)) > 0.05)
        else:
            gen[dp] = elev * rng.uniform(2500, 5500) * np.clip(rng.beta(2, 1.2, len(hr)), 0.1, 1)
    # instrument transformer replacements: every member has at least one; the MDM picked up most of the new
    # multipliers weeks after the field work (lagged), a few on the day (benign)
    by_member = {}
    for d in dps:
        by_member.setdefault(d["member"], []).append(d["dp"])
    swaps = []
    used = set()
    for mname, lst in by_member.items():
        dp = str(rng.choice(lst))
        used.add(dp)
        swaps.append(dp)
    extra = [d["dp"] for d in dps if d["dp"] not in used]
    swaps += list(rng.choice(extra, 2, replace=False))
    benign = [d for d in extra if d not in swaps]
    benign = list(rng.choice(benign, 4, replace=False))
    swap_rows = []
    for dp in swaps + benign:
        day = pd.Timestamp(P.METER_YEAR, 1, 1, tz=P.TZ) + pd.Timedelta(days=int(rng.integers(8, 330)),
                                                                       hours=int(rng.integers(8, 15)))
        old = int(rng.choice([40, 80, 120]))
        lag = 0 if dp in benign else int(rng.integers(30, 100))
        swap_rows.append(dict(dp=dp, when=day, old=old, new=old * 2, lag_days=lag))
    # meters left on standard time after the spring change, one in every member, until a technician reset them
    tr_dp = by_member["Lone Elm Cooperative"][0]
    stuck = []
    for mname, lst in by_member.items():
        cand = [dp for dp in lst if dp not in swaps and dp not in benign and dp != tr_dp]
        kinds = {d["dp"]: d["kind"] for d in dps}
        cand = [dp for dp in cand if kinds[dp] == "rural"] or cand
        dp = str(rng.choice(cand))
        reset = pd.Timestamp(P.METER_YEAR, int(rng.integers(6, 11)), int(rng.integers(1, 26)),
                             int(rng.integers(9, 15)), tz=P.TZ)
        stuck.append(dict(dp=dp, reset=reset))
    # a delivery point moved between members on 1 July (the Lone Elm and Marais service territory agreement)
    transfer = dict(dp=tr_dp, from_=P.MEMBERS[2], to=P.MEMBERS[3],
                    when=pd.Timestamp(P.METER_YEAR, 7, 1, tz=P.TZ))
    return dict(dps=dps, utc=utc, local=loc, true=true, gen=gen, swaps=swap_rows, stuck=stuck, transfer=transfer,
                rng=rng)
