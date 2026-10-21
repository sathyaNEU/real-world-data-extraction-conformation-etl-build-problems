"""The world behind task251 architecture 4: every station's true vehicles and occupancy hour by hour in 2027, the loops'
count of them, and the summer validation day.

Each direction carries a daily demand shaped by an hourly profile (the morning peak in the inbound direction, the
evening peak outbound), the school term, the month and the holidays. Where a bottleneck lies downstream (one lane each
way on the Kessel River bridges, a signalised junction or a lane drop elsewhere) demand above its capacity waits as a
queue, the station sees the bottleneck's flow at a high occupancy, and the queue carries into the next hour. Beyond a
bridge the same vehicles run free on two lanes again. The loops count each vehicle with the station's sensitivity
(1 + b) and lose a share LOSS_SLOPE * (occupancy - LOSS_KNEE) of the vehicles in an hour whose occupancy is above the
knee, where queued vehicles close up and two share one pulse; free flow never reaches the knee."""
import datetime as dt
import zoneinfo

import numpy as np

import params as P

TZ = zoneinfo.ZoneInfo("America/Toronto")
UTC = dt.timezone.utc
START_UTC = dt.datetime(P.YEAR, 1, 1, 5, 0, tzinfo=UTC)
NH = int((dt.datetime(P.YEAR + 1, 1, 1, 5, 0, tzinfo=UTC) - START_UTC).total_seconds() // 3600)

BASE = np.array([.006, .004, .003, .003, .005, .015, .045, .075, .070, .050, .045, .047, .050, .050, .052, .060, .075,
                 .080, .062, .045, .036, .028, .020, .012])
WEEKEND = np.array([.012, .008, .006, .005, .005, .008, .015, .025, .040, .055, .065, .070, .072, .072, .070, .068,
                    .066, .064, .058, .050, .042, .035, .028, .020])
MONTH = dict(zip(range(1, 13), (0.90, 0.93, 0.97, 1.00, 1.03, 1.04, 1.02, 1.02, 1.03, 1.02, 0.99, 0.95)))


def profile(inbound):
    p = BASE.copy()
    if inbound:
        p[6:10] *= 1.5
    else:
        p[15:19] *= 1.5
    return p / p.sum()


def calendar():
    """local time of every UTC hour of the year, and each local day's type"""
    t = [START_UTC + dt.timedelta(hours=i) for i in range(NH)]
    loc = [x.astimezone(TZ) for x in t]
    hol = set(P.HOLIDAYS)

    def kind(d):
        if d in hol or d.weekday() == 6:
            return "sun"
        if d.weekday() == 5:
            return "sat"
        if any(a <= d <= b for a, b in P.TERMS):
            return "term"
        return "summer" if d.month in (6, 7, 8, 9) else "break"
    days = sorted({x.date() for x in loc})
    return dict(utc=t, loc=loc, date=[x.date() for x in loc], hour=np.array([x.hour for x in loc]),
                kind={d: kind(d) for d in days}, days=days)


DAYFAC = dict(term=1.10, brk=0.88, summer=0.66, sat=0.85, sun=0.70)


def occ_free(per_lane):
    """occupancy (per cent) of free-flowing traffic at a flow per lane (vehicles an hour)"""
    return 100.0 * per_lane * 0.0072 / (100.0 - 22.0 * np.clip(per_lane / 1850.0, 0, 1.2) ** 2)


def loss(occ):
    return P.LOSS_SLOPE * np.clip(np.asarray(occ, float) - P.LOSS_KNEE, 0, None)


def stations():
    st = []
    for i, b in enumerate(P.BRIDGES):
        for side in ("south", "north"):
            st.append(dict(code=b[side], road=b["road"], km=b["s_km" if side == "south" else "n_km"], axis="NS",
                           lanes=2, district=P.BRIDGE_DISTRICT[side], kind="bridge", bridge=i, side=side,
                           congested=True))
    for code, road, km, axis, lanes, district, cong in P.OTHERS:
        st.append(dict(code=code, road=road, km=km, axis=axis, lanes=lanes, district=district, kind="other",
                       bridge=None, side=None, congested=cong))
    for x in st:
        x["dirs"] = ("NB", "SB") if x["axis"] == "NS" else ("EB", "WB")
    return st


def _demand(rng, C, daily_base, inbound, noise):
    """each UTC hour's demand for one direction"""
    pin, pout, pwe = profile(True), profile(False), WEEKEND / WEEKEND.sum()
    d = np.empty(NH)
    for i in range(NH):
        day = C["date"][i]
        k = C["kind"][day]
        fac = DAYFAC["brk" if k == "break" else k] * MONTH[day.month] * noise[day]
        prof = (pin if inbound else pout) if k in ("term", "break", "summer") else pwe
        d[i] = daily_base * fac * prof[C["hour"][i]]
    return d


def _queue(rng, dem, cap, lanes):
    """serve the demand through a bottleneck of capacity cap: flow, occupancy, queued flag, hour by hour"""
    q = np.empty(NH)
    occ = np.empty(NH)
    queued = np.zeros(NH, bool)
    backlog = 0.0
    for i in range(NH):
        want = dem[i] + backlog
        if cap is not None and want > cap:
            q[i] = cap * (1 + rng.normal(0, 0.008))
            backlog = want - cap
            queued[i] = True
            occ[i] = 27.0 + 18.0 * min(1.0, backlog / (0.5 * cap)) + rng.normal(0, 1.2)
        else:
            q[i] = rng.poisson(max(want, 0.0))
            backlog = 0.0
            occ[i] = occ_free(q[i] / lanes) + rng.normal(0, 0.25)
    return q, np.clip(occ, 0.2, None), queued


def world(seed=P.SEED):
    rng = np.random.default_rng(seed)
    C = calendar()
    st = stations()
    noise = {}
    for x in st:
        for d in x["dirs"]:
            noise[(x["code"], d)] = {day: float(v) for day, v in zip(C["days"], rng.lognormal(0, 0.04, len(C["days"])))}
    true = {}
    peak_share = profile(True)[8] * DAYFAC["term"]
    # bridges: the upstream approach of each direction queues behind the one-lane deck
    for b in P.BRIDGES:
        cap = float(rng.uniform(1560, 1720))
        for d, up, dn in (("NB", b["south"], b["north"]), ("SB", b["north"], b["south"])):
            inbound = d == "NB"
            daily = cap * rng.uniform(1.15, 1.40) / peak_share
            dem = _demand(rng, C, daily, inbound, noise[(up, d)])
            q, occ, qd = _queue(rng, dem, cap, 2)
            q = np.round(q * rng.lognormal(0, 0.002, NH))
            true[(up, d)] = dict(q=q, occ=occ, queued=qd)
            # past the deck: the same vehicles, a few minutes later, free on two lanes
            lag = np.where(qd, 6.0, 1.5) / 60.0
            moved = np.round(q * lag)
            qdn = q - moved + np.concatenate([[0.0], moved[:-1]])
            true[(dn, d)] = dict(q=qdn, occ=np.clip(occ_free(qdn / 2) + rng.normal(0, 0.25, NH), 0.2, None),
                                 queued=np.zeros(NH, bool))
    for x in st:
        if x["kind"] != "other":
            continue
        inbound_dir = x["dirs"][int(rng.integers(2))]
        for d in x["dirs"]:
            lanes = x["lanes"]
            capf = 1850.0 * lanes
            if x["congested"]:
                cap = capf * float(rng.uniform(0.56, 0.68))
                daily = cap * rng.uniform(1.12, 1.40) / peak_share
            else:
                cap = None
                daily = capf * rng.uniform(0.22, 0.48) / peak_share
            dem = _demand(rng, C, daily, d == inbound_dir, noise[(x["code"], d)])
            q, occ, qd = _queue(rng, dem, cap, lanes)
            true[(x["code"], d)] = dict(q=np.round(q), occ=occ, queued=qd)
    # each station's loss over the year at sensitivity 1
    for x in st:
        num = den = 0.0
        for d in x["dirs"]:
            t = true[(x["code"], d)]
            num += (t["q"] * (1 - loss(t["occ"]))).sum()
            den += t["q"].sum()
        x["L"] = 1 - num / den
    # sensitivities: every station's true error at least 1.1 points from the line
    for x in st:
        for _ in range(5000):
            b = float(rng.normal(0, P.B_SD))
            e = (1 + b) * (1 - x["L"]) - 1
            if abs(abs(e) - P.TOLERANCE) >= 0.011 and abs(abs(b) - P.TOLERANCE) >= 0.006:
                break
        x["b"] = b
        x["b_dir"] = {d: b + float(rng.normal(0, 0.004)) for d in x["dirs"]}
    rec = {}
    for x in st:
        for d in x["dirs"]:
            t = true[(x["code"], d)]
            r = t["q"] * (1 + x["b_dir"][d]) * (1 - loss(t["occ"])) * (1 + rng.normal(0, 0.014, NH))
            rec[(x["code"], d)] = np.round(np.clip(r, 0, None))
    # validation: one summer weekday per station, every station on its own day
    summer = [day for day in C["days"] if day.month in (7, 8) and C["kind"][day] == "summer"]
    vdays = sorted(rng.choice(len(summer), size=len(st), replace=False).tolist())
    order = rng.permutation(len(st))
    for k, x in zip(vdays, [st[i] for i in order]):
        x["vday"] = summer[k]
    return dict(C=C, st=st, true=true, rec=rec, seed=seed)


def truth(W):
    out = {}
    for x in W["st"]:
        num = sum(W["rec"][(x["code"], d)].sum() for d in x["dirs"])
        den = sum(W["true"][(x["code"], d)]["q"].sum() for d in x["dirs"])
        out[x["code"]] = num / den - 1
    return out
