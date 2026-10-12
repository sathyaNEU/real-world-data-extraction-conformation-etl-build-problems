"""The buildings' meters and the records the asks run on: service meters (one per service line), the sub-meters
inside eight buildings, the vault meters read by handheld on work orders, the change-outs, the Science Annex's
removal and Larch Hall's new meter; month-end registers, the water each meter recorded, and every ask figure
under the golden handling and under each mishandling."""
import datetime as dt
import itertools

import numpy as np

import core
import world as WD

# sub-meters: purpose, parent building, size (in), basis, share, location
SUBS = [
    ("Cooling tower make-up", 501, 3.0, "cool", 0.56, "CT deck, CT-1 make-up line"),
    ("Cooling tower make-up", 501, 3.0, "cool", 0.44, "CT deck, CT-2 make-up line"),
    ("Concessions", 401, 1.5, "stadium", (0.020, 0.30), "West concourse, concessions"),
    ("Concessions", 401, 1.5, "stadium", (0.016, 0.26), "East concourse, concessions"),
    ("Pool fill", 402, 2.0, "all", 0.12, "Pool mechanical room, fill line"),
    ("Kitchen", 111, 2.0, "all", 0.30, "Dining kitchen mechanical room"),
    ("RO/DI feed", 301, 1.0, "all", 0.10, "Lab water room 1B"),
    ("Vivarium", 301, 1.5, "all", 0.12, "Vivarium mechanical room"),
]
# service meters read by handheld from their endpoints' logs (vaults the fixed network cannot hear):
# (building, line index)
VAULT = {(202, 0), (204, 0), (304, 0), (121, 0), (107, 0), (403, 0), (502, 0), (701, 0), (801, 1)}
CHANGEOUTS = {102: dt.datetime(2025, 11, 12, 9, 15), 203: dt.datetime(2026, 2, 17, 10, 45),
              208: dt.datetime(2026, 3, 24, 14, 15), 501: dt.datetime(2026, 4, 8, 13, 30),
              404: dt.datetime(2026, 6, 3, 11, 0), 124: dt.datetime(2026, 7, 21, 10, 30)}
TWO_LINE_SHARE = {101: 0.54, 103: 0.47, 302: 0.62, 801: 0.58}
PURPOSE_2 = {101: ("Domestic, east wing", "Domestic, west wing"), 103: ("Domestic, north wing", "Domestic, south wing"),
             302: ("Domestic", "Process water"), 801: ("Domestic, Inn", "Kitchen and laundry")}
MONTHS = [dt.date(2025, 10, 1)] + [dt.date(2025 + (9 + k) // 12, (9 + k) % 12 + 1, 1) for k in range(1, 13)]
SEED_ASKS = 4120


def mult_of(size):
    return 1 if size <= 2.0 else (10 if size <= 4.0 else 100)


def model_of(rng, size, year):
    s = {1.0: "1in", 1.5: "1-1/2in", 2.0: "2in", 3.0: "3in", 4.0: "4in", 6.0: "6in"}[size]
    if size <= 2.0:
        return "%s %s" % (rng.choice(["Badger Recordall", "Neptune T-10", "Sensus SRII"]), s)
    if size <= 4.0:
        return "%s %s" % (rng.choice(["Sensus OMNI T2", "Neptune HP Turbine", "Badger Recordall Turbo"]), s)
    return "%s %s" % ("Sensus OMNI F2" if year >= 2018 else "Neptune HP Protectus III", s)


def step_index(t_local):
    t = t_local.replace(tzinfo=core.ET).astimezone(core.UTC)
    i = (t - core.T0).total_seconds() / (core.STEP * 60)
    assert abs(i - round(i)) < 1e-9, t_local
    return int(round(i))


def month_instants():
    return [dt.datetime(m.year, m.month, 1, 0, 0) for m in MONTHS]


def meters(W):
    """Every meter with its step series and register history."""
    rng = np.random.default_rng(SEED_ASKS)
    G, bsteps = W["G"], W["bsteps"]
    n = G["n"]
    di, lh, nin = G["di"], G["lhour"], G["nin"]
    out = []
    serials = iter(rng.permutation(np.arange(1000, 7000))[:400])

    def new_no():
        return "M-%04d" % next(serials)

    def endpoint():
        return "%d" % rng.integers(1_500_000_000, 1_599_999_999)

    size_of = {}
    for b in core.B + [core.ANNEX]:
        w = b["w"]
        cat = b["cat"]
        if b["no"] == 501:
            s = 6.0
        elif cat == "Residence Hall":
            s = 3.0 if (b["lines"] == 2 or w < 700) else 4.0
        elif cat in ("Research", "Athletics") or w >= 200:
            s = 4.0 if w >= 150 else 3.0
        elif w >= 90:
            s = 3.0
        elif w >= 40:
            s = 2.0
        else:
            s = 1.5
        size_of[b["no"] if b is not core.ANNEX else "annex"] = s
    size_of[47] = 4.0
    t_inst = month_instants()
    for b in sorted(core.B + [core.ANNEX], key=lambda x: (x["no"], x is core.ANNEX)):
        key = "annex" if b is core.ANNEX else b["no"]
        series_b = bsteps[key]
        for j in range(b["lines"]):
            share = 1.0 if b["lines"] == 1 else (TWO_LINE_SHARE[b["no"]] if j == 0 else 1 - TWO_LINE_SHARE[b["no"]])
            s = series_b * share
            size = size_of[key] if b["lines"] == 1 else (3.0 if b["no"] in (101, 103, 302, 801) and j == 1 else 4.0)
            if b["no"] in (101, 103):
                size = 3.0
            purpose = "Domestic" if b["lines"] == 1 else PURPOSE_2[b["no"]][j]
            if b["no"] == 501:
                purpose = "Domestic and process"
            vault = (b["no"], j) in VAULT and key != "annex"
            m = dict(key=key, bldg=b["no"], line=j, size=size, mult=mult_of(size), purpose=purpose, service=True,
                     sub=False, vault=vault, series=s, cat=b["cat"], name=b["name"])
            out.append(m)
    for purpose, parent, size, basis, share, loc in SUBS:
        if basis == "cool":
            base = W["C"]["cep_c"] * share * np.exp(rng.normal(0, 0.03, len(G["days"])))
            s = base[di] * WD.SHAPES["cool"][lh] / nin
        elif basis == "stadium":
            a, g = share
            stad = W["vols"][401]["ath"] - W["C"]["game"]
            daily = (a * stad + g * W["C"]["game"]) * np.exp(rng.normal(0, 0.05, len(G["days"])))
            s = daily[di] * WD.SHAPES["ath"][lh] / nin
        else:
            f = share * np.exp(rng.normal(0, 0.04, len(G["days"])))
            s = bsteps[parent] * f[di]
        pb = next(x for x in core.B if x["no"] == parent)
        out.append(dict(key=parent, bldg=parent, line=None, size=size, mult=mult_of(size), purpose=purpose,
                        service=False, sub=True, vault=False, series=s, cat=pb["cat"], name=pb["name"], location=loc))
    # lifecycles: a meter in place all year, a change-out pair, the annex's removal, Larch Hall's install
    final = []
    for m in out:
        m["cum"] = np.concatenate([[0.0], np.cumsum(m["series"])])
        if m["key"] == "annex":
            m.update(no=new_no(), start=None, end=core.ANNEX_REMOVED, installed=dt.date(1998, 6, 9))
            final.append(m)
        elif m["key"] == 47:
            m.update(no=new_no(), start=core.LARCH_INSTALL, end=None, installed=core.LARCH_INSTALL.date())
            final.append(m)
        elif m["service"] and m["key"] in CHANGEOUTS and m["line"] == 0:
            tc = CHANGEOUTS[m["key"]]
            old = dict(m, no=new_no(), start=None, end=tc, installed=dt.date(int(rng.integers(1996, 2012)),
                                                                            int(rng.integers(1, 13)), 15))
            new = dict(m, no=new_no(), start=tc, end=None, installed=tc.date())
            final += [old, new]
        else:
            m.update(no=new_no(), start=None, end=None,
                     installed=dt.date(int(rng.integers(1994, 2025)), int(rng.integers(1, 13)), int(rng.integers(1, 28))))
            final.append(m)
    # registers: gallons on the dial at the year's start or at install; endpoints for the fixed network
    for m in final:
        mult = m["mult"]
        if m["start"] is None:
            lo, hi = {1: (2_000_000, 64_000_000), 10: (180_000, 8_400_000), 100: (40_000, 860_000)}[mult]
            m["g0"] = float(rng.integers(lo, hi)) * mult + float(rng.integers(0, mult))
            m["i0"] = 0
            m["set_read"] = int(rng.integers(0, 60)) // mult
        else:
            m["g0"] = float(rng.integers(0, 4)) * mult
            m["i0"] = step_index(m["start"])
        m["i1"] = step_index(m["end"]) if m["end"] is not None else n
        m["endpoint"] = None if m["vault"] else endpoint()
    # a change-out keeps the endpoint on the new meter
    by = {}
    for m in final:
        if m["service"] and m["key"] in CHANGEOUTS and m["line"] == 0:
            by.setdefault(m["key"], []).append(m)
    for k, (old, new) in by.items():
        new["endpoint"] = old["endpoint"]
    for m in final:
        m["reg"] = lambda i, m=m: int(np.floor((m["g0"] + m["cum"][i] - m["cum"][m["i0"]]) / m["mult"]))
        m["initial_read"] = m["reg"](m["i0"]) if m["start"] is not None else int(m["set_read"])
        m["final_read"] = m["reg"](m["i1"]) if m["end"] is not None else None
        m["reads"] = {}
        for t in t_inst:
            i = step_index(t)
            if m["i0"] <= i <= m["i1"] and not (m["end"] is not None and i == m["i1"]) and \
                    not (m["start"] is not None and i == m["i0"]):
                m["reads"][t] = m["reg"](i)
    return final


def recorded(m, k, partial=True, mult=True):
    """The water meter m recorded in month k (between month instants k and k+1), in gallons."""
    t = month_instants()
    a, b = t[k], t[k + 1]
    ra, rb = m["reads"].get(a), m["reads"].get(b)
    f = m["mult"] if mult else 1
    if ra is not None and rb is not None:
        return (rb - ra) * f
    if not partial:
        return 0
    if ra is not None and m["end"] is not None and a < m["end"] <= b:
        return (m["final_read"] - ra) * f
    if rb is not None and m["start"] is not None and a <= m["start"] < b:
        return (rb - m["initial_read"]) * f
    if m["start"] is not None and m["end"] is not None and a <= m["start"] and m["end"] <= b:
        return (m["final_read"] - m["initial_read"]) * f
    return 0


def category(m, p2="golden"):
    """The ask's group a meter's water counts in, or None. p2: golden, current (building 47 read as Larch Hall),
    drop (the annex's reads dropped)."""
    if m["key"] == "annex":
        if p2 == "current":
            return "res"
        if p2 == "drop":
            return None
        return "acad"
    if m["cat"] == "Residence Hall":
        return "res"
    if m["cat"] in ("Academic", "Research"):
        return "acad"
    if m["cat"] == "Athletics":
        return "ath"
    if m["bldg"] == 501:
        return "cep"
    return None


GROUPS = ["res", "acad", "ath", "cep"]


def metered(final, subs=False, vault=True, partial=True, mult=True, p2="golden", by_group=False):
    """Monthly metered water (12 months) under a handling; by group over the year when by_group."""
    tot = np.zeros(12, dtype=np.int64)
    grp = {g: 0 for g in GROUPS}
    for m in final:
        if m["sub"] and not subs:
            continue
        if m["vault"] and not vault:
            continue
        for k in range(12):
            r = recorded(m, k, partial, mult)
            tot[k] += r
            g = category(m, p2)
            if g is not None:
                grp[g] += r
    return grp if by_group else tot


def used_by_month(W, storage=True):
    Bal = W["Bal"]
    days = Bal["days"]
    out = np.zeros(12)
    for k in range(12):
        sel = [i for i, d in enumerate(days) if (d.year, d.month) == (MONTHS[k].year, MONTHS[k].month)]
        out[k] = Bal["P"][sel].sum() - (Bal["dS"][sel].sum() if storage else 0.0)
    return np.round(out).astype(np.int64)


def figures(W, final):
    used = used_by_month(W)
    prod = used_by_month(W, storage=False)
    gold_m = metered(final)
    lost = used - gold_m
    share = 100.0 * lost.sum() / used.sum()
    groups = metered(final, by_group=True)
    stops = {}
    for subs, vault, partial, mult, use in itertools.product([False, True], [True, False], [True, False],
                                                             [True, False], ["used", "prod"]):
        mm = metered(final, subs, vault, partial, mult)
        u = used if use == "used" else prod
        lm = u - mm
        stops[(subs, vault, partial, mult, use)] = dict(lost=lm, year=int(lm.sum()),
                                                        share=100.0 * lm.sum() / u.sum())
    gstops = {}
    for subs, vault, partial, mult, p2 in itertools.product([False, True], [True, False], [True, False],
                                                            [True, False], ["golden", "current", "drop"]):
        gstops[(subs, vault, partial, mult, p2)] = metered(final, subs, vault, partial, mult, p2, by_group=True)
    sub_by_month = metered(final, subs=True) - gold_m
    return dict(used=used, prod=prod, metered=gold_m, lost=lost, year=int(lost.sum()), share=share,
                used_year=int(used.sum()), groups=groups, stops=stops, gstops=gstops, sub_by_month=sub_by_month)


if __name__ == "__main__":
    W = WD.build()
    final = meters(W)
    F = figures(W, final)
    print(len(final), "meters;", sum(m["sub"] for m in final), "sub;", sum(m["vault"] for m in final), "vault")
    print("used", F["used"].sum(), "metered", F["metered"].sum(), "lost", F["year"], "share %.3f" % F["share"])
    print("lost by month", list(F["lost"]))
    print("sub by month", list(F["sub_by_month"]))
    print("groups", F["groups"])
    s = F["stops"]
    for k in [(True, True, True, True, "used"), (False, False, True, True, "used"), (True, False, True, True, "used"),
              (False, True, False, True, "used"), (False, True, True, True, "prod")]:
        print(k, s[k]["year"], "%.2f" % s[k]["share"])
    for k in [(True, True, True, True, "golden"), (False, True, True, True, "current"),
              (False, True, True, True, "drop"), (True, True, True, True, "current")]:
        print(k, F["gstops"][k])
