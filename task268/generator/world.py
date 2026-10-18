"""The clean truth for task268: the six metros' tracts, their residents and jobs, the 2022 commuting flows into and out
of every core tract, and the national survey's respondents. No mess here; records.py writes the exports.

Commuting: inside each central county a doubly constrained gravity model per industry group carries every tract's
resident workers to every tract's jobs held by central-county residents; jobs held by people from outlying counties
and from outside the metro are drawn from those counties by destination; core residents also work in the outlying
counties and outside the metro. The flows touching a core tract are kept (the analytics team's extract)."""
import math

import numpy as np

import common as K

SEED = 268
G3 = K.GROUPS
# the survey's truth: share of the five weekdays on the employer's premises, by group and where the worker lives
ATT = {"SI01": {"C": .94, "O": .92, "X": .82}, "SI02": {"C": .90, "O": .80, "X": .36},
       "SI03": {"C": .74, "O": .44, "X": .12}}
# the survey's national residence mix by group (workers whose workplace is in a metropolitan area)
SMIX = {"SI01": {"C": .55, "O": .35, "X": .10}, "SI02": {"C": .60, "O": .30, "X": .10},
        "SI03": {"C": .48, "O": .30, "X": .22}}
OFF = 0.055      # share of weekdays not worked (leave, holidays, part-time days), every cell
EMP = 0.48       # resident workers per resident
REF = {"Halberdine": (40.212, -82.861), "Quillmere": (40.583, -86.297), "Corrisford": (34.682, -77.421),
       "Tessavon": (39.441, -104.583), "Ashcombe": (38.336, -92.617), "Dunnaway": (35.613, -86.874)}


def rm(c, o, x):
    return {"C": c, "O": o, "X": x}


def same(r):
    return {g: dict(r) for g in G3}


# Each core: its business district tracts and its other tracts (count, km2 each, residents per km2, jobs per km2 by
# group, where the workers live by group), the industry mix of its residents' jobs, and the share of the metro's
# out-of-metro workers who live in another state (the auxiliary part).
CORES = {
    "Halberdine": dict(
        cbd=(6, 0.50, 2700, {"SI03": 77790, "SI02": 2910, "SI01": 190},
             {"SI03": rm(0.249, 0.259, 0.492), "SI02": rm(0.269, 0.239, 0.492), "SI01": rm(0.5, 0.4, 0.1)}),
        rest=(30, .60, 7000, {"SI03": 2500, "SI02": 2000, "SI01": 300}, same(rm(.6, .3, .1))),
        mix={"SI01": .10, "SI02": .30, "SI03": .60}, aux=.45, pop=760000),
    "Quillmere": dict(
        cbd=(5, 0.60, 3000, {"SI03": 60120, "SI02": 3510, "SI01": 260},
             {"SI03": rm(0.37, 0.38, 0.25), "SI02": rm(0.417, 0.333, 0.25), "SI01": rm(0.5, 0.4, 0.1)}),
        rest=(33, .60, 6500, {"SI03": 2000, "SI02": 1500, "SI01": 300}, same(rm(.7, .25, .05))),
        mix={"SI01": .05, "SI02": .25, "SI03": .70}, aux=.20, pop=640000),
    "Corrisford": dict(
        cbd=(7, 0.60, 7700, {"SI03": 13760, "SI02": 34840, "SI01": 7800},
             {"SI03": rm(0.091, 0.272, 0.638), "SI02": rm(0.167, 0.196, 0.638), "SI01": rm(0.15, 0.35, 0.5)}),
        rest=(30, .60, 7500, {"SI03": 2000, "SI02": 3000, "SI01": 500}, same(rm(.6, .3, .1))),
        mix={"SI01": .15, "SI02": .45, "SI03": .40}, aux=.0, pop=600000),
    "Tessavon": dict(
        cbd=(6, 0.60, 7100, {"SI03": 49850, "SI02": 9220, "SI01": 400},
             {"SI03": rm(0.902, 0.08, 0.018), "SI02": rm(0.902, 0.08, 0.018), "SI01": rm(0.9, 0.08, 0.02)}),
        rest=(35, .50, 10300, {"SI03": 3500, "SI02": 2500, "SI01": 300}, same(rm(.88, .10, .02))),
        mix={"SI01": .05, "SI02": .25, "SI03": .70}, aux=.15, pop=980000),
    "Ashcombe": dict(
        cbd=(4, 0.70, 9000, {"SI03": 9740, "SI02": 6520, "SI01": 400},
             {"SI03": rm(0.604, 0.302, 0.094), "SI02": rm(0.604, 0.302, 0.094), "SI01": rm(0.6, 0.3, 0.1)}),
        rest=(60, .36, 19000, {"SI03": 1500, "SI02": 2000, "SI01": 300}, same(rm(.7, .25, .05))),
        mix={"SI01": .25, "SI02": .45, "SI03": .30}, aux=.15, pop=820000),
    "Dunnaway": dict(
        cbd=(5, 0.90, 3000, {"SI03": 12910, "SI02": 12430, "SI01": 7990},
             {"SI03": rm(0.453, 0.352, 0.195), "SI02": rm(0.453, 0.352, 0.195), "SI01": rm(0.45, 0.35, 0.2)}),
        rest=(48, .50, 10000, {"SI03": 1500, "SI02": 2000, "SI01": 800}, same(rm(.6, .3, .1))),
        mix={"SI01": .35, "SI02": .40, "SI03": .25}, aux=.15, pop=700000),
}
COUNTY_MIX = {"SI01": .16, "SI02": .24, "SI03": .60}   # resident workers' groups outside the cores


def ll(ref, x, y):
    """Planar km from the core's centre to latitude and longitude."""
    lat = ref[0] + y / 110.95
    lon = ref[1] + x / (111.32 * math.cos(math.radians(ref[0])))
    return round(lat, 7), round(lon, 7)


def tract_codes(r, n, start, step=100):
    """Tract codes in the county's numbering: whole hundreds, a few split tracts carrying .01 and .02."""
    out, code = [], start
    while len(out) < n:
        if r.random() < .12 and len(out) < n - 1:
            out += ["%06d" % (code + 1), "%06d" % (code + 2)]
        else:
            out.append("%06d" % code)
        code += step
    return out[:n]


def build_metro(m, r):
    st, stname = K.STATES[m["st"]]
    spec = CORES[m["name"]]
    ref = REF[m["name"]]
    cc = st + m["central"][1]
    tracts = []   # dicts: geoid, county, kind, x, y, area, R, jobs{g}, ring{g}, core

    # the core: business district tracts at the centre (their spread fixed, so the district's shape is designed),
    # then the rest of the core
    n_cbd, a_cbd, r_cbd, j_cbd, ring_cbd = spec["cbd"]
    n_rest, a_rest, r_rest, j_rest, ring_rest = spec["rest"]
    codes = tract_codes(r, n_cbd + n_rest, 100)
    jmul = np.linspace(1.32, .70, n_cbd)
    amul = np.array([.86, 1.12, .94, 1.20, 1.0, .90, 1.08, .97][:n_cbd])
    for k in range(n_cbd + n_rest):
        cbd = k < n_cbd
        area, rd, jd, ring = (a_cbd, r_cbd, j_cbd, ring_cbd) if cbd else (a_rest, r_rest, j_rest, ring_rest)
        ang = r.uniform(0, 2 * math.pi)
        rad = r.uniform(0, 1.3) if cbd else r.uniform(1.4, 4.2)
        if cbd:
            ar = area * float(amul[k]) * float(r.lognormal(0, .04))
            f, fj = float(r.lognormal(0, .2)), float(jmul[k]) * float(r.lognormal(0, .04))
        else:
            ar = area * float(r.lognormal(0, .22))
            f, fj = float(r.lognormal(0, .25)), float(r.lognormal(0, .33))
        tracts.append(dict(geoid=cc + codes[k], county=cc, kind="cbd" if cbd else "core", core=True,
                           x=rad * math.cos(ang), y=rad * math.sin(ang), area=ar, R=rd * ar * f,
                           jobs={g: jd.get(g, 0) * ar * fj for g in G3}, ring=ring))
    # one water-only tract inside two of the cores (a river channel), listed by the planning map
    if m["name"] in ("Corrisford", "Tessavon"):
        tracts.append(dict(geoid=cc + "980100", county=cc, kind="water", core=True, x=0.9, y=-0.4, area=0.0, water=0.31,
                           R=0.0, jobs={g: 0.0 for g in G3}, ring=same(rm(1, 0, 0))))
    core_R = sum(t["R"] for t in tracts)
    # the rest of the central county: suburbs from 4 to 22 km, enough of them that the county's own resident
    # workers in each group can fill the core's jobs held by central-county residents with room to spare
    pop_sub = spec["pop"] - core_R
    for g in G3:
        d = sum(t["jobs"][g] * t["ring"][g]["C"] for t in tracts)
        o = sum(EMP * t["R"] * spec["mix"][g] * .91 for t in tracts)
        pop_sub = max(pop_sub, 1.45 * max(0.0, d - o) / (EMP * .91 * COUNTY_MIX[g]))
    n_out = int(round(pop_sub / 4300))
    codes = tract_codes(r, n_out, 8000)
    for k in range(n_out):
        ang, rad = r.uniform(0, 2 * math.pi), 4.4 + 17.6 * math.sqrt(r.random())
        pop = float(r.lognormal(math.log(4300), .28))
        dens = 6500 * math.exp(-rad / 7.5) * float(r.lognormal(0, .3))
        tracts.append(dict(geoid=cc + codes[k], county=cc, kind="county", core=False, x=rad * math.cos(ang),
                           y=rad * math.sin(ang), area=pop / dens, R=pop, jobs={g: 0.0 for g in G3}, ring=same(rm(1, 0, 0))))
    # outlying counties, each a sector from 22 to 60 km; outside counties from 60 to 110 km
    for i, (nm, code) in enumerate(m["outlying"]):
        base = 2 * math.pi * i / len(m["outlying"]) + r.uniform(-.3, .3)
        n = int(r.integers(26, 64))
        codes = tract_codes(r, n, 9500 if r.random() < .5 else 200)
        for k in range(n):
            ang, rad = base + r.uniform(-.9, .9), 22 + 38 * math.sqrt(r.random())
            pop = float(r.lognormal(math.log(4100), .3))
            dens = 900 * math.exp(-(rad - 22) / 18) * float(r.lognormal(0, .4))
            tracts.append(dict(geoid=st + code + codes[k], county=st + code, kind="outlying", core=False,
                               x=rad * math.cos(ang), y=rad * math.sin(ang), area=pop / dens, R=pop,
                               jobs={g: 0.0 for g in G3}, ring=same(rm(1, 0, 0))))
    for i, (nm, code, other) in enumerate(m["outside"]):
        base = r.uniform(0, 2 * math.pi)
        n = int(r.integers(14, 34))
        codes = tract_codes(r, n, 9600 if r.random() < .5 else 100)
        for k in range(n):
            ang, rad = base + r.uniform(-.5, .5), 60 + 50 * r.random()
            pop = float(r.lognormal(math.log(3900), .3))
            dens = 250 * float(r.lognormal(0, .5))
            tracts.append(dict(geoid=st + code + codes[k], county=st + code, kind="outside", core=False,
                               x=rad * math.cos(ang), y=rad * math.sin(ang), area=pop / dens, R=pop,
                               jobs={g: 0.0 for g in G3}, ring=same(rm(1, 0, 0))))
    for t in tracts:
        t["lat"], t["lon"] = ll(ref, t["x"], t["y"])
        t["metro"] = m["name"]
        t["st"] = m["st"]
    return dict(metro=m, tracts=tracts, spec=spec, central=cc,
                outlying={st + c for _, c in m["outlying"]}, outside={st + c for _, c, _ in m["outside"]})


def dist(a, b):
    return math.hypot(a["x"] - b["x"], a["y"] - b["y"]) + 0.6


def flows_metro(M, r):
    """Expected flows (home tract, work tract, group) -> count, then integer draws. Returns rows and the
    out-of-state origins."""
    T = M["tracts"]
    spec = M["spec"]
    central = [t for t in T if t["county"] == M["central"] and t["kind"] != "water"]
    core = [t for t in T if t["core"] and t["kind"] != "water"]
    outl = [t for t in T if t["kind"] == "outlying"]
    outs = [t for t in T if t["kind"] == "outside"]
    for t in T:
        mix = spec["mix"] if t["core"] else COUNTY_MIX
        t["E"] = {g: EMP * t["R"] * mix[g] for g in G3}
    exp = {}   # (h, w, g) -> expected count

    def add(h, w, g, v):
        if v > 0:
            exp[(h, w, g)] = exp.get((h, w, g), 0.0) + v

    # where central-county resident workers work: 91 per cent in the county, 6 in an outlying county, 3 outside
    in_cty, to_o, to_x = .91, .06, .03
    for g in G3:
        O = np.array([t["E"][g] * in_cty for t in central])
        Dcore = {t["geoid"]: t["jobs"][g] * t["ring"][g]["C"] for t in core}
        need = O.sum() - sum(Dcore.values())
        assert need > 0, (M["metro"]["name"], g, need)
        # the county's other jobs, where its own residents work, spread with the suburbs' size and nearness
        wts = np.array([0.0 if t["core"] else t["R"] * math.exp(-math.hypot(t["x"], t["y"]) / 9) * float(r.lognormal(0, .5))
                        for t in central])
        D = np.array([Dcore.get(t["geoid"], 0.0) for t in central]) + need * wts / wts.sum()
        for t, d in zip(central, D):
            if not t["core"]:
                t["jobs"][g] = d       # suburban jobs held by the county's residents
        cost = np.array([[math.exp(-dist(a, b) / 6.0) for b in central] for a in central])
        A, B = np.ones(len(central)), np.ones(len(central))
        for _ in range(60):
            A = 1.0 / (cost @ (B * D))
            B = 1.0 / ((A * O) @ cost)
        flow = (A * O)[:, None] * cost * (B * D)[None, :]
        idx = {t["geoid"]: i for i, t in enumerate(central)}
        for t in core:
            j = idx[t["geoid"]]
            for i, h in enumerate(central):
                add(h["geoid"], t["geoid"], g, flow[i, j])             # into the core from the county
            for jj, w in enumerate(central):
                if not w["core"]:
                    add(t["geoid"], w["geoid"], g, flow[j, jj])        # core residents to the rest of the county
        # core residents' jobs in the outlying counties and outside the metro
        for t in core:
            e = t["E"][g]
            wo = np.array([w["R"] * math.exp(-dist(t, w) / 15) for w in outl])
            for w, v in zip(outl, e * to_o * wo / wo.sum()):
                add(t["geoid"], w["geoid"], g, v)
            wx = np.array([w["R"] * math.exp(-dist(t, w) / 40) for w in outs])
            for w, v in zip(outs, e * to_x * wx / wx.sum()):
                add(t["geoid"], w["geoid"], g, v)
        # jobs in the core held by people from the outlying counties and from outside the metro
        for t in core:
            jo, jx = t["jobs"][g] * t["ring"][g]["O"], t["jobs"][g] * t["ring"][g]["X"]
            wo = np.array([h["E"][g] * math.exp(-dist(t, h) / 25) for h in outl])
            for h, v in zip(outl, jo * wo / wo.sum()):
                add(h["geoid"], t["geoid"], g, v)
            aux = spec["aux"] * (1.0 if g == "SI03" else .4)
            wx = np.array([h["E"][g] * math.exp(-dist(t, h) / 60) for h in outs])
            for h, v in zip(outs, jx * (1 - aux) * wx / wx.sum()):
                add(h["geoid"], t["geoid"], g, v)
            if aux > 0:
                for h, v in zip(M["far"], jx * aux * M["far_w"]):
                    add(h, t["geoid"], g, v)
    rows = {}
    for (h, w, g), v in sorted(exp.items()):
        n = int(r.poisson(v))
        if n:
            rows.setdefault((h, w), {gg: 0 for gg in G3})[g] += n
    return rows


def far_origins(M, r, n=420):
    """Tracts in other states where the metro's out-of-state workers live (homes of staff the establishments carry,
    many working remotely): real state codes, county and tract codes as the agency writes them."""
    others = ["01", "04", "05", "06", "09", "12", "13", "17", "19", "20", "21", "22", "24", "25", "26", "27", "28",
              "31", "34", "36", "40", "41", "42", "45", "48", "49", "51", "53", "55"]
    st = K.STATES[M["metro"]["st"]][0]
    near = {"39": ["18", "21", "26", "42", "54"], "18": ["17", "21", "26", "39"], "37": ["13", "45", "47", "51"],
            "08": ["04", "20", "31", "35", "49", "56"], "29": ["05", "17", "19", "20", "31", "40"],
            "47": ["01", "05", "13", "21", "28", "37", "51"]}[st]
    out = set()
    while len(out) < n:
        s = near[int(r.integers(len(near)))] if r.random() < .55 else others[int(r.integers(len(others)))]
        if s == st:
            continue
        c = "%03d" % (2 * int(r.integers(0, 90)) + 1)
        tr = "%06d" % (int(r.integers(1, 400)) * 100 + (0 if r.random() < .85 else int(r.integers(1, 3))))
        out.add(s + c + tr)
    far = sorted(out)
    w = r.lognormal(0, 1.0, len(far))
    return far, w / w.sum()


# each metro's own stream, chosen so every graded figure sits away from its rounding edge and no core tract sits
# within 2 per cent of the dense-tract cut (generator/tune.py)
METRO_SEED = {"Halberdine": 0, "Quillmere": 3, "Corrisford": 40, "Tessavon": 9, "Ashcombe": 80, "Dunnaway": 4}


def build_one(m, seed=SEED, sub=None):
    i = K.METROS.index(m)
    s = METRO_SEED[m["name"]] if sub is None else sub
    M = build_metro(m, np.random.default_rng([seed, i, 1, s]))
    M["far"], M["far_w"] = far_origins(M, np.random.default_rng([seed, i, 2, s]))
    M["flows"] = flows_metro(M, np.random.default_rng([seed, i, 3, s]))
    return M


def build(seed=SEED):
    W = {"metros": [], "survey": None}
    for m in K.METROS:
        W["metros"].append(build_one(m, seed))
    W["survey"] = survey(np.random.default_rng([seed, 99]))
    return W


# ------------------------------------------------------------------------------------------------- the survey
AGE_BANDS = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
AGE_W = [.11, .23, .22, .20, .18, .06]
EDUC = ["High school or less", "Some college", "Bachelor's degree", "Graduate degree"]
SECTOR_W = {"11": .012, "21": .004, "22": .008, "23": .062, "31-33": .088, "42": .038, "44-45": .098, "48-49": .052,
            "51": .021, "52": .045, "53": .016, "54": .074, "55": .015, "56": .061, "61": .088, "62": .139,
            "71": .016, "72": .082, "81": .038, "92": .044}
WAVES = ["2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07",
         "2026-08", "2026-09"]
EMPLOYED = [161.42, 161.18, 160.71, 159.96, 160.33, 160.88, 161.35, 161.92, 162.40, 162.77, 162.55, 162.19]  # millions


def survey(r, n_per=5000):
    rows = []
    rid = 1500000
    secs = list(SECTOR_W)
    sw = np.array([SECTOR_W[s] for s in secs]); sw = sw / sw.sum()
    for wi, wave in enumerate(WAVES):
        n = n_per + int(r.integers(-260, 260))
        for _ in range(n):
            rid += int(r.integers(1, 9))
            sec = secs[int(r.choice(len(secs), p=sw))]
            g = K.SECTOR_GROUP[sec]
            u = r.random()
            if u < .072:
                rel = "4"              # no usual workplace, or a workplace outside any metropolitan area
            elif u < .081:
                rel = "9"              # not reported
            else:
                mix = SMIX[g]
                v = r.random()
                rel = "1" if v < mix["C"] else ("2" if v < mix["C"] + mix["O"] else "3")
            ring = {"1": "C", "2": "O", "3": "X"}.get(rel)
            a = ATT[g][ring] if ring else .55
            off = int(r.binomial(5, OFF))
            work = 5 - off
            if work == 0:
                prem = home = 0
            else:
                # each worked day on the premises with the cell's probability, given a worker-level propensity
                q = min(1.0, a / (1 - OFF))
                lam = float(np.clip(r.beta(max(.05, q * 1.3), max(.05, (1 - q) * 1.3)), 0, 1))
                prem = int(r.binomial(work, lam))
                home = work - prem
            age = AGE_BANDS[int(r.choice(6, p=AGE_W))]
            edu = EDUC[int(r.choice(4, p=[.30, .27, .27, .16]))]
            sex = "1" if r.random() < .53 else "2"
            rows.append(dict(wave=wave, rid=rid, sector=sec, group=g, rel=rel, ring=ring, prem=prem, home=home,
                             off=off, age=age, edu=edu, sex=sex))
    # weights: the panel under-represents the young and those without a degree; each wave's weights total that
    # month's employed adults
    adj = {"18-24": 1.55, "25-34": 1.12, "35-44": .96, "45-54": .93, "55-64": .97, "65+": 1.20}
    eadj = {"High school or less": 1.38, "Some college": 1.05, "Bachelor's degree": .82, "Graduate degree": .74}
    for wi, wave in enumerate(WAVES):
        sub = [x for x in rows if x["wave"] == wave]
        raw = np.array([adj[x["age"]] * eadj[x["edu"]] * float(r.lognormal(0, .18)) for x in sub])
        raw = raw / raw.sum() * EMPLOYED[wi] * 1e6
        for x, wgt in zip(sub, raw):
            x["weight"] = float(wgt)
    return rows
