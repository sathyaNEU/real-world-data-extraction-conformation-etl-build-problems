"""The service's estimates: county, district and state acres, production and yield by crop and practice,
1991 to 2025, in two vintages (before and after the county estimates for 2017 to 2021 were revised to the 2022
Census of Agriculture). Every figure is computed forward from the world's parameters; nothing is fitted to a target.

Rounding follows the service's practice: county and district acres to the nearest 10, production to the nearest
100 bushels (sunflower 1,000 pounds, hay 10 tons); a district's acres and production are the sums of its counties'
rounded estimates, published or not, and the state's the sums of its districts'; yields are production over
harvested acres to one decimal (sunflower whole pounds, hay hundredths of a ton).
"""
import numpy as np

import world as W

YEARS = np.array(W.YEARS)
N = len(YEARS)
T = YEARS - W.Y0


def rng(*k):
    return np.random.default_rng([W.STREAM] + list(k))


# ---------------------------------------------------------------- weather
def weather():
    """Each district's share of normal dryland yield potential by year, and a wheat-season factor."""
    out, wheat = {}, {}
    for d in W.DISTRICTS:
        r = rng(11, d)
        w = 1 + r.normal(0, 0.065, N)
        for y, v in W.DROUGHT.get(d, {}).items():
            w[y - W.Y0] = v
        if d not in W.DROUGHT:            # the other districts share the region's big years, less sharply
            for y, v in ((2002, 0.66), (2011, 0.58), (2012, 0.74), (2022, 0.68)):
                w[y - W.Y0] = v + r.normal(0, 0.04)
        out[d] = np.clip(w, 0.45, 1.18)
        ww = 1 + rng(12, d).normal(0, 0.08, N)
        for y, v in ((1996, 0.70), (2002, 0.78), (2006, 0.74), (2011, 0.62), (2014, 0.72), (2018, 0.80), (2022, 0.66)):
            ww[y - W.Y0] = v + rng(13, d, y).normal(0, 0.03)
        wheat[d] = np.clip(ww, 0.45, 1.2)
    return out, wheat


# ---------------------------------------------------------------- crops, county by county
CROPS = ("SORGHUM", "WHEAT", "CORN", "SOYBEANS", "SUNFLOWER", "HAY")


def county_crops(wx, wheat):
    """{(county, crop, practice): dict(planted, harvested, production)} true-world arrays, unrounded."""
    est = {}
    for c, (ansi, d, member, b, s, sens, nz, pl, irr) in W.COUNTIES.items():
        r = rng(21, int(ansi))
        w = wx[d]
        # dryland grain sorghum
        fac = np.clip(1 - sens * (1 - w) + r.normal(0, nz, N), 0.35, 1.30)
        y = (b + s * T) * fac
        hs = np.clip(0.95 - 0.85 * np.clip(0.82 - fac, 0, None), 0.45, 0.97)
        pa = pl * (1 + r.normal(0, 0.05, N)) * (1 - 0.006 * T)
        ha = pa * hs
        for (cc, yy), (fy, fa) in W.WITHHELD.items():
            if cc == c:
                i = yy - W.Y0
                y[i] = fy
                ha[i] = fa
        est[(c, "SORGHUM", "NON-IRRIGATED")] = dict(planted=pa, harvested=ha, production=ha * y)
        if irr:
            yi = (1.55 * b + 0.95 * s * T) * np.clip(1 - 0.22 * (1 - w) + r.normal(0, 0.03, N), 0.7, 1.15)
            pai = irr * (1 + r.normal(0, 0.08, N)) * (1 - 0.009 * T)
            hai = pai * np.clip(0.97 + r.normal(0, 0.01, N), 0.9, 0.99)
            est[(c, "SORGHUM", "IRRIGATED")] = dict(planted=pai, harvested=hai, production=hai * yi)
        # winter wheat, dryland everywhere, irrigated where the county irrigates
        wf = np.clip(wheat[d] + r.normal(0, 0.05, N), 0.4, 1.25)
        wy = (34 + 0.36 * T) * wf * (1 + 0.04 * (b - 46) / 46)
        wpa = (pl * 2.3) * (1 + r.normal(0, 0.04, N)) * (1 - 0.004 * T)
        wha = wpa * np.clip(0.93 - 0.6 * np.clip(0.75 - wf, 0, None), 0.5, 0.97)
        est[(c, "WHEAT", "NON-IRRIGATED")] = dict(planted=wpa, harvested=wha, production=wha * wy)
        if irr:
            wyi = (52 + 0.45 * T) * np.clip(1 + r.normal(0, 0.05, N), 0.8, 1.2)
            wpai = irr * 1.1 * (1 + r.normal(0, 0.07, N))
            whai = wpai * 0.97
            est[(c, "WHEAT", "IRRIGATED")] = dict(planted=wpai, harvested=whai, production=whai * wyi)
        # corn: irrigated where the county irrigates, a little dryland corn everywhere since 2000
        if irr:
            cy = (158 + 1.9 * T) * np.clip(1 + r.normal(0, 0.04, N), 0.85, 1.12)
            cpa = irr * 3.2 * (1 + r.normal(0, 0.06, N))
            cha = cpa * 0.96
            est[(c, "CORN", "IRRIGATED")] = dict(planted=cpa, harvested=cha, production=cha * cy)
        dpa = np.where(YEARS >= 2000, pl * 0.12 * (1 + 0.03 * (YEARS - 2000)) * (1 + r.normal(0, 0.15, N)), 0)
        dcy = (68 + 0.9 * T) * np.clip(1 - 1.15 * (1 - w) + r.normal(0, 0.06, N), 0.2, 1.3)
        dha = dpa * np.clip(0.9 - 0.9 * np.clip(0.8 - w, 0, None), 0.3, 0.95)
        est[(c, "CORN", "NON-IRRIGATED")] = dict(planted=dpa, harvested=dha, production=dha * dcy)
        # soybeans, irrigated only, where the county irrigates
        if irr:
            sy = (46 + 0.35 * T) * np.clip(1 + r.normal(0, 0.05, N), 0.8, 1.15)
            spa = irr * 1.4 * (1 + r.normal(0, 0.1, N)) * (1 + 0.01 * T)
            est[(c, "SOYBEANS", "IRRIGATED")] = dict(planted=spa, harvested=spa * 0.97, production=spa * 0.97 * sy)
        # sunflower, dryland, a few hundred to a few thousand acres
        fpa = pl * 0.05 * (1 + r.normal(0, 0.35, N)).clip(0.1)
        fy = (1250 + 9 * T) * np.clip(1 - 0.9 * (1 - w) + r.normal(0, 0.08, N), 0.3, 1.3)
        fha = fpa * np.clip(0.92 - 0.7 * np.clip(0.8 - w, 0, None), 0.4, 0.97)
        est[(c, "SUNFLOWER", "NON-IRRIGATED")] = dict(planted=fpa, harvested=fha, production=fha * fy)
        # alfalfa hay, all practices only
        hay_a = pl * 0.35 * (1 + r.normal(0, 0.05, N))
        hy = (2.6 + 0.012 * T) * np.clip(1 - 0.5 * (1 - w) + r.normal(0, 0.05, N), 0.5, 1.2)
        est[(c, "HAY", "ALL")] = dict(planted=None, harvested=hay_a, production=hay_a * hy)
    return est


UNIT = {"SORGHUM": ("BU", 100, 1), "WHEAT": ("BU", 100, 1), "CORN": ("BU", 100, 1), "SOYBEANS": ("BU", 100, 1),
        "SUNFLOWER": ("LB", 1000, 0), "HAY": ("TONS", 10, 2)}


def round_county(est):
    """Rounded county estimates: {(county, crop, practice): {item: array}} with ALL practices added up."""
    out = {}
    for (c, crop, pr), v in est.items():
        step = UNIT[crop][1]
        rec = {"harvested": np.round(v["harvested"], -1), "production": np.round(v["production"] / step) * step}
        if v["planted"] is not None:
            rec["planted"] = np.maximum(np.round(v["planted"], -1), rec["harvested"])
        out[(c, crop, pr)] = rec
    for c in W.COUNTIES:
        for crop in CROPS:
            prs = [k for k in out if k[0] == c and k[1] == crop and k[2] != "ALL"]
            if not prs:
                continue
            keys = set.intersection(*[set(out[k]) for k in prs])
            out[(c, crop, "ALL")] = {i: sum(out[k][i] for k in prs) for i in keys}
    return out


def revise(cty):
    """The county estimates for 2017 to 2021 as revised to the 2022 Census of Agriculture: acres and production of
    every published-practice estimate moved by a few per cent, withheld cells left as they were."""
    out = {k: {i: a.copy() for i, a in v.items()} for k, v in cty.items()}
    for (c, crop, pr), v in out.items():
        if pr == "ALL":
            continue
        r = rng(31, int(W.COUNTIES[c][0]), CROPS.index(crop), len(pr))
        step = UNIT[crop][1]
        for y in range(W.REVISED[0], W.REVISED[1] + 1):
            i = y - W.Y0
            if (c, y) in W.WITHHELD and crop == "SORGHUM":
                continue
            da, dp = r.uniform(-0.03, 0.03), r.uniform(-0.025, 0.025)
            v["harvested"][i] = np.round(v["harvested"][i] * (1 + da), -1)
            v["production"][i] = np.round(v["production"][i] * (1 + da + dp) / step) * step
            if "planted" in v:
                v["planted"][i] = max(np.round(v["planted"][i] * (1 + da), -1), v["harvested"][i])
    for c in W.COUNTIES:                    # ALL practices re-added
        for crop in CROPS:
            prs = [k for k in out if k[0] == c and k[1] == crop and k[2] != "ALL"]
            if prs:
                keys = set.intersection(*[set(out[k]) for k in prs])
                out[(c, crop, "ALL")] = {i: sum(out[k][i] for k in prs) for i in keys}
    return out


def other_districts(wx, wheat):
    """District-level estimates for the seven districts whose counties the pull does not hold."""
    out = {}
    for d in W.DISTRICTS:
        if d in W.COUNTY_DISTRICTS:
            continue
        r = rng(41, d)
        w = wx[d]
        scale = r.uniform(0.6, 1.6)
        sh = np.clip(0.95 - 0.85 * np.clip(0.82 - w, 0, None), 0.45, 0.97)
        pa = 230000 * scale * (1 - 0.006 * T) * (1 + r.normal(0, 0.04, N))
        y = (45 + 0.54 * T) * np.clip(w + r.normal(0, 0.03, N), 0.35, 1.25)
        out[(d, "SORGHUM", "NON-IRRIGATED")] = dict(planted=pa, harvested=pa * sh, production=pa * sh * y)
        ipa = 20000 * scale * (1 + r.normal(0, 0.06, N))
        out[(d, "SORGHUM", "IRRIGATED")] = dict(planted=ipa, harvested=ipa * 0.97,
                                                 production=ipa * 0.97 * (72 + 0.5 * T))
        wpa = 520000 * scale * (1 + r.normal(0, 0.03, N))
        wy = (34 + 0.36 * T) * np.clip(wheat[d] + r.normal(0, 0.03, N), 0.4, 1.25)
        out[(d, "WHEAT", "NON-IRRIGATED")] = dict(planted=wpa, harvested=wpa * 0.92, production=wpa * 0.92 * wy)
        cpa = 60000 * scale * (1 + r.normal(0, 0.05, N))
        out[(d, "CORN", "IRRIGATED")] = dict(planted=cpa, harvested=cpa * 0.96, production=cpa * 0.96 * (158 + 1.9 * T))
        hay = 80000 * scale * (1 + r.normal(0, 0.04, N))
        out[(d, "HAY", "ALL")] = dict(planted=None, harvested=hay, production=hay * (2.6 + 0.012 * T))
    rounded = {}
    for k, v in out.items():
        step = UNIT[k[1]][1]
        rec = {"harvested": np.round(v["harvested"], -1), "production": np.round(v["production"] / step) * step}
        if v["planted"] is not None:
            rec["planted"] = np.maximum(np.round(v["planted"], -1), rec["harvested"])
        rounded[k] = rec
    for d in {k[0] for k in rounded}:
        for crop in CROPS:
            prs = [k for k in rounded if k[0] == d and k[1] == crop and k[2] != "ALL"]
            if prs:
                keys = set.intersection(*[set(rounded[k]) for k in prs])
                rounded[(d, crop, "ALL")] = {i: sum(rounded[k][i] for k in prs) for i in keys}
    return rounded


def districts(cty):
    """District estimates where the pull holds the counties: the sums of their counties' rounded estimates,
    published or not."""
    out = {}
    for d in W.COUNTY_DISTRICTS:
        cs = [c for c, v in W.COUNTIES.items() if v[1] == d]
        for crop in CROPS:
            for pr in ("NON-IRRIGATED", "IRRIGATED", "ALL"):
                ks = [(c, crop, pr) for c in cs if (c, crop, pr) in cty]
                if not ks:
                    continue
                keys = set.intersection(*[set(cty[k]) for k in ks])
                out[(d, crop, pr)] = {i: sum(cty[k][i] for k in ks) for i in keys}
    return out


def state(dist, other):
    allk = {}
    for src in (dist, other):
        for (d, crop, pr), v in src.items():
            allk.setdefault((crop, pr), []).append(v)
    out = {}
    for k, vs in allk.items():
        keys = set.intersection(*[set(v) for v in vs])
        out[k] = {i: sum(v[i] for v in vs) for i in keys}
    return out


# ---------------------------------------------------------------- publication
def published_mask(cty):
    """True where the service publishes a county estimate (every item of a practice together). A practice is not
    published when it rests on fewer than five reports: the dryland sorghum years too few farms harvested in the
    sandy counties, and the small irrigated, dryland corn and sunflower estimates whose harvested acres fall under
    the reports a county estimate needs. An all-practices estimate is published when it meets the standard itself."""
    pub = {}
    floors = {"SUNFLOWER": 900, "SOYBEANS": 1500, "CORN": 900, "SORGHUM": 1500, "WHEAT": 3000, "HAY": 2000}
    for k, v in cty.items():
        c, crop, pr = k
        if crop == "SORGHUM" and pr in ("NON-IRRIGATED", "ALL") and any(w[0] == c for w in W.WITHHELD):
            m = np.array([(c, int(y)) not in W.WITHHELD for y in YEARS])
        elif crop == "SORGHUM" and pr in ("NON-IRRIGATED", "ALL"):
            m = np.ones(N, bool)
        else:
            m = v["harvested"] >= floors[crop]
        pub[k] = m
    return pub


def cv_percent(c, crop, pr, harvested, year):
    """The coefficient of variation the service prints beside a published county yield, from 2008."""
    if year < 2008:
        return None
    r = rng(51, int(W.COUNTIES[c][0]), CROPS.index(crop), len(pr), year)
    base = 4.0 + 900.0 / np.sqrt(max(harvested, 50.0))
    return round(float(np.clip(base * r.uniform(0.85, 1.15), 3.0, 29.5)), 1)


def world():
    wx, wh = weather()
    est = county_crops(wx, wh)
    cty_old = round_county(est)
    cty_new = revise(cty_old)
    other = other_districts(wx, wh)
    d_old, d_new = districts(cty_old), districts(cty_new)
    return dict(weather=wx, wheat=wh, est=est, cty_old=cty_old, cty_new=cty_new, other=other,
                dist_old=d_old, dist_new=d_new, state_old=state(d_old, other), state_new=state(d_new, other),
                pub=published_mask(cty_old))


def current(x):
    """The estimates as the service now publishes them: the revised county figures from 2017 on, the first
    vintage before (they are the same outside the revised years)."""
    return x["cty_new"], x["dist_new"]
