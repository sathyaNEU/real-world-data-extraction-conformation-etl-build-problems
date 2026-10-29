"""task464 architecture 10: the simulation (clean truth).

Builds the Copsewell Cross network from world.FEEDERS, every connection's half-hourly flow for 2025/26, each section's
net flow, the losses each project removes under each rung of the ladder, the metering each file records, and the
2023/24 to 2025/26 interruption record the asks read. One rng stream per process, all derived from world.SEED.
"""
import datetime as dt
import math
import numpy as np
import world as W

N = W.NHH
UTC = [W.UTC0 + dt.timedelta(minutes=30 * i) for i in range(N)]


def rng(tag):
    h = sum((i + 1) * ord(c) for i, c in enumerate(tag))
    return np.random.default_rng(W.SEED * 1009 + h)


def uk_offset_hours(t):
    """BST (+1) between the last Sundays of March and October at 01:00 UTC."""
    def last_sunday(y, m):
        d = dt.date(y, m, 31)
        while d.weekday() != 6:
            d -= dt.timedelta(days=1)
        return dt.datetime(d.year, d.month, d.day, 1, 0)
    return 1 if last_sunday(t.year, 3) <= t < last_sunday(t.year, 10) else 0


OFFSET = np.array([uk_offset_hours(t) for t in UTC])
LOCAL = [t + dt.timedelta(hours=int(o)) for t, o in zip(UTC, OFFSET)]
LOCAL_DATE = np.array([l.date() for l in LOCAL])
HOD = np.array([l.hour + l.minute / 60.0 + 0.25 for l in LOCAL])      # local clock, mid-half-hour
DOY = np.array([(l.date() - dt.date(2025, 4, 1)).days for l in LOCAL])
DOW = np.array([l.weekday() for l in LOCAL])
BANK = {dt.date(2025, 4, 18), dt.date(2025, 4, 21), dt.date(2025, 5, 5), dt.date(2025, 5, 26), dt.date(2025, 8, 25),
        dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1)}
HOLIDAY = np.array([d in BANK for d in LOCAL_DATE])
WORKDAY = (DOW < 5) & ~HOLIDAY
NDAY = int(DOY.max()) + 1
SEASON = np.cos(2 * np.pi * (DOY - 280) / 365.0)    # +1 in early January, -1 in early July

# ---------------------------------------------------------------- weather (one stream for the whole area)
_wr = rng("weather")
_tday = np.zeros(NDAY)
for d in range(NDAY):
    _tday[d] = (0.72 * _tday[d - 1] if d else 0) + _wr.normal(0, 2.1)
TEMP_DAY = 10.6 - 6.4 * np.cos(2 * np.pi * (np.arange(NDAY) - 105) / 365.0) + _tday   # coldest mid-January
CLOUD_DAY = np.clip(_wr.beta(1.4, 1.25, NDAY), 0.02, 0.99)          # 0 clear, 1 overcast
_cl_hh = np.clip(CLOUD_DAY[DOY] + _wr.normal(0, 0.10, N), 0, 1)
TEMP = TEMP_DAY[DOY] + 3.2 * np.sin(2 * np.pi * (HOD - 9) / 24.0)


def solar_elevation():
    """Solar elevation (radians) at the mid-point of each UTC half-hour."""
    out = np.zeros(N)
    for i, t in enumerate(UTC):
        tm = t + dt.timedelta(minutes=15)
        n = tm.timetuple().tm_yday
        decl = math.radians(23.44) * math.sin(2 * math.pi * (284 + n) / 365.0)
        b = 2 * math.pi * (n - 81) / 364.0
        eot = 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)
        solar_time = tm.hour + tm.minute / 60.0 + W.LON / 15.0 + eot / 60.0
        ha = math.radians(15 * (solar_time - 12))
        lat = math.radians(W.LAT)
        out[i] = math.asin(math.sin(lat) * math.sin(decl) + math.cos(lat) * math.cos(decl) * math.cos(ha))
    return out


ELEV = solar_elevation()
IRR = np.clip(np.sin(ELEV), 0, None) ** 1.15 * (1.0 - 0.78 * _cl_hh ** 1.6)   # relative to clear-sky noon at the equinox ~ 0.62

_wind = rng("wind")
_x = np.zeros(N)
_e = _wind.normal(0, 1, N)
for i in range(1, N):
    _x[i] = 0.986 * _x[i - 1] + 0.167 * _e[i]
WIND_MS = np.clip(7.0 + 2.7 * _x + 1.3 * SEASON, 0.0, None)


# ---------------------------------------------------------------- profiles
def _shape(key):
    h = HOD
    if key == "dom":
        s = (0.52 + 0.30 * np.exp(-((h - 7.8) / 1.5) ** 2) + 0.78 * np.exp(-((h - 18.4) / 2.3) ** 2)
             - 0.22 * np.exp(-((h - 3.6) / 2.4) ** 2) + 0.12 * (~WORKDAY) * np.exp(-((h - 12.5) / 3) ** 2))
        s *= 1 + 0.30 * SEASON + 0.018 * np.clip(12 - TEMP, 0, None)
    elif key == "com":
        on = (h >= 7.5) & (h <= 18.5)
        s = 0.34 + 1.0 * on * WORKDAY + 0.32 * ((h >= 9) & (h <= 16.5)) * (~WORKDAY) * (DOW == 5)
        s *= 1 + 0.10 * SEASON + 0.012 * np.clip(TEMP - 19, 0, None)
    elif key == "ind":
        s = 0.48 + 0.62 * ((h >= 6) & (h <= 22)) * WORKDAY + 0.14 * WORKDAY
    elif key == "agr":
        s = (0.66 + 0.42 * np.exp(-((h - 6.2) / 1.9) ** 2) + 0.30 * np.exp(-((h - 17.0) / 2.4) ** 2))
        s *= 1 + 0.12 * SEASON
    elif key == "hosp":
        s = 0.78 + 0.34 * ((h >= 7.5) & (h <= 20)) + 0.05 * WORKDAY
        s *= 1 + 0.08 * SEASON
    elif key == "cold":
        s = 0.92 + 0.10 * ((h >= 6) & (h <= 20)) * WORKDAY + 0.06 * np.clip(TEMP - 14, 0, None) / 8
    elif key == "quarry":
        s = 0.22 + 1.05 * ((h >= 7) & (h <= 17)) * WORKDAY
    else:
        raise KeyError(key)
    return s


def connection_profile(tag, cls, mean_kw):
    pf, pv_share, key = W.CLASSES[cls]
    r = rng("load:" + tag)
    s = _shape(key)
    dn = np.repeat(r.normal(0, 0.04, NDAY), 48)[:N]
    s = s * (1 + dn) * (1 + r.normal(0, 0.03, N))
    p = mean_kw * s / s.mean()
    if pv_share > 0:
        p = p - pv_share * mean_kw * 1.6 * IRR * (1 + r.normal(0, 0.03, N))
    phi = math.acos(pf)
    q = np.abs(p) * math.tan(phi) * (1 + r.normal(0, 0.04, N)) * np.where(p >= 0, 1.0, 0.25)
    return p, q


def solar_export(tag, cap_kw):
    r = rng("solar:" + tag)
    gen = cap_kw * 1.62 * IRR * (1 + r.normal(0, 0.025, N))
    gen = np.clip(gen, 0, cap_kw)
    aux = np.where(gen < 1, 9.0 + r.normal(0, 1.2, N), 0.0)
    return gen, np.clip(aux, 0, None)          # export kW, import kW (auxiliaries at night)


def wind_export(tag, cap_kw):
    r = rng("wind:" + tag)
    ws = WIND_MS * (1 + r.normal(0, 0.03, N))
    pc = np.clip((ws - 3.4) / (12.6 - 3.4), 0, 1) ** 2.3
    pc[ws > 25] = 0
    gen = cap_kw * pc
    aux = np.where(gen < 1, 6.0, 0.0)
    return gen, aux


def chp_site(tag, site_kw, chp_kw):
    site_p, site_q = connection_profile(tag + ":site", "hosp", site_kw)
    r = rng("chp:" + tag)
    heating = (TEMP_DAY[DOY] < 13.5) | (SEASON > 0.35)
    run = heating & (HOD >= 5.5) & (HOD < 22.5)
    run &= np.repeat(r.random(NDAY) > 0.04, 48)[:N]           # occasional maintenance days
    g = chp_kw * run * (0.93 + 0.05 * r.random(N))
    net = site_p - g
    return net, site_q - 0.15 * g   # positive net imports, negative exports


# ---------------------------------------------------------------- the network
class Node:
    def __init__(self, nid, feeder, kind, parent_section=None):
        self.id, self.feeder, self.kind, self.parent_section = nid, feeder, kind, parent_section


class Section:
    def __init__(self, sid, feeder, frm, to, metres, code, project=False):
        self.id, self.feeder, self.frm, self.to, self.metres, self.code, self.project = sid, feeder, frm, to, metres, code, project
        self.down = []        # connection keys beyond this section


class Conn:
    def __init__(self, key, feeder, node, kind, name, **kw):
        self.key, self.feeder, self.node, self.kind, self.name = key, feeder, node, kind, name
        self.__dict__.update(kw)


def _ids():
    r = rng("ids")
    node_ids, sec_ids = [], []
    v = 4130
    for _ in range(400):
        v += int(r.integers(3, 47))
        node_ids.append(v)
    s = 20417
    for _ in range(400):
        s += int(r.integers(5, 91))
        sec_ids.append(s)
    r.shuffle(node_ids)
    site = [int(x) for x in r.choice(np.arange(300000, 899999), 400, replace=False)]
    mpan = [int(x) for x in r.choice(np.arange(10 ** 9, 10 ** 10 - 1), 60, replace=False)]
    return node_ids, sec_ids, site, mpan


def build_network():
    node_ids, sec_ids, sites, mpans = _ids()
    ni, si, ki, mi = iter(node_ids), iter(sec_ids), iter(sites), iter(mpans)
    nodes, sections, conns = {}, [], []
    feeders = []
    cref = iter([2011 + (i % 9) for i in range(40)])

    def new_node(feeder, kind):
        n = Node("WX%d" % next(ni), feeder, kind)
        n.asset = None
        nodes[n.id] = n
        return n

    def lay(fcode, start, segments, attach, proj_idx=None):
        prev = start
        trunk_nodes = [start]
        for k, (m, code) in enumerate(segments):
            nxt = new_node(fcode, "RMU")
            sec = Section("HV-%d" % next(si), fcode, prev.id, nxt.id, m, code,
                          project=(proj_idx is not None and k in proj_idx))
            nxt.parent_section = sec.id
            sections.append(sec)
            trunk_nodes.append(nxt)
            prev = nxt
        for k, items in sorted(attach.items()):
            at = trunk_nodes[k]
            for it in items:
                if it[0] == "B":
                    lay(fcode, at, it[1], it[2])
                    continue
                spur = it[-1]
                if spur is not None:
                    node = new_node(fcode, "Substation")
                    sec = Section("HV-%d" % next(si), fcode, at.id, node.id, spur[0], spur[1])
                    node.parent_section = sec.id
                    sections.append(sec)
                else:
                    node = at
                if it[0] == "S":
                    _, name, kva, cls, mean_kw, _sp = it
                    node.kind = "Ground-mounted substation" if kva >= 500 else "Pole-mounted substation"
                    c = Conn("S:" + name, fcode, node.id, "S", name, kva=kva, cls=cls, mean_kw=mean_kw,
                             site=next(ki), host=node.id)
                    node.asset = c.key
                else:
                    _, name, kind, params, _sp = it
                    node.kind = "HV customer substation"
                    c = Conn("H:" + name, fcode, node.id, "H", name, hvkind=kind, params=params,
                             mpan_import=next(mi), mpan_export=(next(mi) if kind in ("solar", "wind", "chp") else None),
                             host=node.id, site=next(ki), agreement="CA-%d-%04d" % (next(cref), 100 + int(next(ki)) % 8900))
                    node.asset = c.key
                conns.append(c)
        return trunk_nodes

    for f in W.FEEDERS:
        bus = Node("WX%d" % next(ni), f["code"], "Busbar")
        bus.asset = None
        nodes[bus.id] = bus
        tn = lay(f["code"], bus, f["trunk"], f["attach"], proj_idx=set(f["project"]))
        feeders.append(dict(f, bus=bus.id, trunk_nodes=[n.id for n in tn]))
    # normally-open interconnectors between feeder ends (closed only to back-feed during faults)
    fend = {f["code"]: f["trunk_nodes"][-1] for f in feeders}
    nops = []
    for a, b, m, code in W.NOP_LINKS:
        sec = Section("HV-%d" % next(si), a, fend[a], fend[b], m, code)
        sec.normally_open = True
        sec.far_feeder = b
        sections.append(sec)
        nops.append(sec)
    parent = {s.to: s for s in sections if not getattr(s, "normally_open", False)}
    for c in conns:
        n = c.host
        while n in parent:
            parent[n].down.append(c.key)
            n = parent[n].frm
    neigh = []
    for name, kva, cls, mean_kw in W.NEIGHBOUR_SUBS:
        neigh.append(Conn("S:" + name, "LUD", None, "S", name, kva=kva, cls=cls, mean_kw=mean_kw, site=next(ki), host=None))
    for name, kind, params in W.NEIGHBOUR_HV:
        neigh.append(Conn("H:" + name, "LUD", None, "H", name, hvkind=kind, params=params, mpan_import=next(mi),
                          mpan_export=None, host=None, site=next(ki),
                          agreement="CA-%d-%04d" % (next(cref), 100 + int(next(ki)) % 8900)))
    return feeders, nodes, sections, conns, neigh


def flows(conns, onf=None):
    """Each connection's half-hourly P and Q (kW, kVAr) at its connection, positive drawn from the network.

    A generator with an active network management floor exports no more than its feeder's other connections draw,
    less the floor, so the feeder head never reverses (the scheme's purpose at the primary's reverse-power relay)."""
    out = {}
    anm = []
    one = np.ones(N)
    for c in conns:
        f = onf.get(c.key, one) if onf else one
        if c.kind == "S":
            p, q = connection_profile(c.key, c.cls, c.mean_kw)
            if c.name == "Redburn Meadows":
                ramp = np.clip((LOCAL_DATE.astype("datetime64[D]") - np.datetime64(W.REDBURN_MEADOWS_ENERGISED)).astype(int) / 60.0, 0, 1)
                ramp = np.where(LOCAL_DATE.astype("datetime64[D]") < np.datetime64(W.REDBURN_MEADOWS_ENERGISED), 0.0, 0.25 + 0.75 * ramp)
                p, q = p * ramp, q * ramp
            out[c.key] = dict(p=p * f, q=q * f, imp=None, exp=None)
        else:
            k = c.hvkind
            if k == "demand":
                p, q = connection_profile(c.key, c.params["cls"], c.params["mean_kw"])
                p, q = p * f, q * f
                out[c.key] = dict(p=p, q=q, imp=np.clip(p, 0, None), exp=np.zeros(N), qimp=np.clip(q, 0, None), qexp=np.zeros(N))
            elif k == "solar":
                g, aux = solar_export(c.key, c.params["cap_kw"])
                g, aux = g * f, aux * f
                if c.params.get("anm_floor_kw"):
                    anm.append(c)
                p = aux - g
                q = np.where(g > 0, -0.02 * g, 2.0)      # unity power factor bar a trace, small night draw
                out[c.key] = dict(p=p, q=q, imp=aux, exp=g, qimp=np.clip(q, 0, None), qexp=np.clip(-q, 0, None))
            elif k == "wind":
                g, aux = wind_export(c.key, c.params["cap_kw"])
                g, aux = g * f, aux * f
                if c.params.get("anm_floor_kw"):
                    anm.append(c)
                p = aux - g
                q = 0.18 * g + 1.5
                out[c.key] = dict(p=p, q=q, imp=aux, exp=g, qimp=np.clip(q, 0, None), qexp=np.zeros(N))
            elif k == "chp":
                net, q = chp_site(c.key, c.params["site_kw"], c.params["chp_kw"])
                net, q = net * f, q * f
                out[c.key] = dict(p=net, q=q, imp=np.clip(net, 0, None), exp=np.clip(-net, 0, None),
                                  qimp=np.clip(q, 0, None), qexp=np.clip(-q, 0, None))
    for c in anm:
        others = [o for o in conns if o.feeder == c.feeder and o.key != c.key]
        draw = sum(out[o.key]["p"] for o in others)
        cap = np.clip(draw - c.params["anm_floor_kw"], 0, None)
        d = out[c.key]
        g = np.minimum(d["exp"], cap)
        d["exp"] = g
        d["p"] = d["imp"] - g
        if c.hvkind == "solar":
            q = np.where(g > 0, -0.02 * g, 2.0)
        else:
            q = 0.18 * g + 1.5
        d["q"], d["qimp"], d["qexp"] = q, np.clip(q, 0, None), np.clip(-q, 0, None)
    return out


def section_losses_kwh(S_kva, ohm):
    """kWh lost in one half-hour on a section of total resistance ohm carrying apparent power S_kva at 11 kV."""
    return S_kva ** 2 * ohm / (W.V_NOM_KV ** 2) / 1000.0 * 0.5


def ohms(sec, code=None):
    return W.CONDUCTORS[code or sec.code][2] * sec.metres / 1000.0


def rung_savings(feeders, sections, conns, fl):
    """MWh a year each project removes under the four constructions of the ladder."""
    bykey = {c.key: c for c in conns}
    out = {}
    for f in feeders:
        secs = [s for s in sections if s.feeder == f["code"] and not getattr(s, "normally_open", False)]
        bus = f["bus"]
        top = [s for s in secs if s.frm == bus]
        assert len(top) == 1
        allkeys = top[0].down
        headP = sum(fl[k]["p"] for k in allkeys)
        headQ = sum(fl[k]["q"] for k in allkeys)
        S_head = np.sqrt(headP ** 2 + headQ ** 2)
        kva_all = sum(bykey[k].kva for k in allkeys if bykey[k].kind == "S")
        res = {"R0": 0.0, "R1": 0.0, "R2": 0.0, "R3": 0.0, "R3_summer": 0.0, "R3_winter": 0.0, "R3_rev_hh": 0, "R3_q": [0.0] * 4}
        summer = (DOY < 183)
        quarter = np.minimum(DOY // 91, 3)
        for s in secs:
            if not s.project:
                continue
            dR = ohms(s) - ohms(s, f["new"])
            P = sum(fl[k]["p"] for k in s.down)
            Q = sum(fl[k]["q"] for k in s.down)
            S3 = np.sqrt(P ** 2 + Q ** 2)
            Pl = sum(np.clip(fl[k]["p"], 0, None) if bykey[k].kind == "H" else fl[k]["p"] for k in s.down)
            Ql = sum(fl[k]["q"] if bykey[k].kind == "S" else np.clip(fl[k]["q"], 0, None) for k in s.down)
            S2 = np.sqrt(Pl ** 2 + Ql ** 2)
            share = sum(bykey[k].kva for k in s.down if bykey[k].kind == "S") / kva_all
            res["R0"] += section_losses_kwh(S_head, dR).sum() / 1000
            res["R1"] += section_losses_kwh(S_head * share, dR).sum() / 1000
            res["R2"] += section_losses_kwh(S2, dR).sum() / 1000
            l3 = section_losses_kwh(S3, dR)
            res["R3"] += l3.sum() / 1000
            res["R3_summer"] += l3[summer].sum() / 1000
            res["R3_winter"] += l3[~summer].sum() / 1000
            for qq in range(4):
                res["R3_q"][qq] += l3[quarter == qq].sum() / 1000
            res["R3_rev_hh"] = max(res["R3_rev_hh"], int((P < 0).sum()))
        out[f["code"]] = res
    return out


def simulate():
    """The network, its interruption record, and every connection's half-hourly flow while it was on supply."""
    import rel
    feeders, nodes, sections, conns, neigh = build_network()
    R = rel.simulate(dict(feeders=feeders, sections=sections, conns=conns, neigh=neigh))
    onf = rel.on_supply(R, conns)
    fl = flows(conns + neigh, onf)
    return dict(feeders=feeders, nodes=nodes, sections=sections, conns=conns, neigh=neigh, flows=fl, rel=R, onf=onf,
                rungs=rung_savings(feeders, sections, conns, fl))


if __name__ == "__main__":
    import time
    t0 = time.time()
    w = simulate()
    print("simulated in %.1fs" % (time.time() - t0))
    names = {f["code"]: f["name"] for f in w["feeders"]}
    print("%-14s %8s %8s %8s %8s %8s %8s %6s" % ("feeder", "R0", "R1", "R2", "R3", "summer", "winter", "rev"))
    for code, r in w["rungs"].items():
        print("%-14s %8.1f %8.1f %8.1f %8.1f %8.1f %8.1f %6d" % (names[code], r["R0"], r["R1"], r["R2"], r["R3"],
                                                              r["R3_summer"], r["R3_winter"], r["R3_rev_hh"]))
    for lab in ("R0", "R1", "R2", "R3"):
        o = sorted(w["rungs"].items(), key=lambda kv: -kv[1][lab])
        print(lab, names[o[0][0]], round(o[0][1][lab], 1), "next", names[o[1][0]], round(o[1][1][lab], 1),
              "margin %.3f" % (o[0][1][lab] / o[1][1][lab]))
    # the feeder heads
    bykey = {c.key: c for c in w["conns"]}
    for f in w["feeders"]:
        top = [s for s in w["sections"] if s.feeder == f["code"] and s.frm == f["bus"]][0]
        P = sum(w["flows"][k]["p"] for k in top.down)
        e = P.sum() * 0.5 / 1000
        print(f["name"], "head mean kW %.0f, min %.0f, reverse hh %d, energy MWh %.0f" % (P.mean(), P.min(), (P < 0).sum(), e))
