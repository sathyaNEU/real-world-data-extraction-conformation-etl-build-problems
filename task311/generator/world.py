"""task311 world: the Provincial Household Medicines Survey (PHMS) of Halvorsen University's Survey Research Centre.

Five health regions of sampled areas, an area panel visited in each of the 2023, 2024 and 2025 waves; households
selected from each area's listing; one interview per household with its health contact. The clean truth is built
here (areas, their selection weights and dwellings, persistent and wave-specific area effects, every issued
address and its outcome); the exports, the weights file, the crosswalk and the documents are cut from it in
pack.py and docs.py.

The ministry's reorganisation of 1 April 2024 moved areas between regions and renumbered every region's areas
consecutively; the contractor Northmark's case system took the new numbers up on 22 April 2024, so its 2024
cases carry the code in force in its system on the day each was assigned.
"""
import datetime as dt

import numpy as np

SEED = 312377
BOOST = 1200

# region number, name, the contractors' abbreviations
REGIONS = [(1, "North", "NOR"), (2, "Central Valley", "CVL"), (3, "Lakeshore", "LKS"),
           (4, "Southern Uplands", "SUP"), (5, "Metro", "MET")]
RNAME = {r: n for r, n, _ in REGIONS}
RABBR = {r: a for r, _, a in REGIONS}

# The 2025 design per region and stratum: areas, the take the issue was sized for, the response it was sized on,
# the stratum's share of the region's households, the 2025 logit mean and the area-effect sd (logit scale).
DESIGN = {
    1: [dict(stratum="1", k=20, take=35, rr=0.70, share=1.00, mu=-1.40, tau=1.22)],
    2: [dict(stratum="2", k=60, take=40, rr=0.62, share=0.66, mu=-2.33, tau=0.10),
        dict(stratum="2S", k=20, take=5, rr=0.62, share=0.34, mu=-2.33, tau=0.10)],
    3: [dict(stratum="3", k=100, take=12, rr=0.64, share=1.00, mu=-2.45, tau=0.10)],
    4: [dict(stratum="4", k=40, take=29, rr=0.66, share=1.00, mu=-2.02, tau=0.74)],
    5: [dict(stratum="5", k=60, take=42, rr=0.55, share=1.00, mu=-2.55, tau=0.58)],
}
HOUSEHOLDS = {1: 27_640, 2: 161_380, 3: 94_910, 4: 71_230, 5: 418_560}
WAVE_SHIFT = {2023: -0.09, 2024: -0.045, 2025: 0.0}     # logit drift of every region's mean by wave
PERSIST = 0.86                                         # share of the area-effect variance that persists across waves

# The reorganisation (old region, position in the old region's numbering) -> new region. Gained areas are appended to
# the new region's core numbering; the Central Valley supplement keeps its block after the core.
OLD_K = {1: 20, 2: 61, 3: 102, 4: 39, 5: 58}           # old-frame core areas per region (the supplement apart)
MOVES = {(1, 5): 3, (1, 11): 3, (1, 16): 3,                       # North to Lakeshore
         (3, 40): 1,                                              # Lakeshore to North
         (3, 15): 5, (3, 33): 5, (3, 61): 5, (3, 87): 5,          # Lakeshore to Metro
         (5, 9): 4, (5, 27): 4, (5, 44): 4,                       # Metro to Southern Uplands
         (4, 20): 5,                                              # Southern Uplands to Metro
         (4, 7): 2, (4, 31): 2,                                   # Southern Uplands to Central Valley
         (2, 50): 4,                                              # Central Valley to Southern Uplands
         (2, 18): 1, (2, 38): 1}                                  # Central Valley to North

REORG_EFFECTIVE = dt.date(2024, 4, 1)
NORTHMARK_SWITCH = dt.date(2024, 4, 22)

# fieldwork calendars: the Mondays the contractors assign new work on
ASSIGN_WEEKS = {
    2023: [dt.date(2023, 2, 6) + dt.timedelta(weeks=i) for i in range(14)],
    2024: [dt.date(2024, 3, 4) + dt.timedelta(weeks=i) for i in range(16)],
    2025: [dt.date(2025, 2, 3) + dt.timedelta(weeks=i) for i in range(14)],
}
FIELD_CLOSE = {2023: dt.date(2023, 6, 9), 2024: dt.date(2024, 7, 19), 2025: dt.date(2025, 6, 13)}

# contractor by wave and region: Northmark everywhere in 2023 and 2024; Ostrander took the Central Valley and
# Lakeshore from the 2025 wave
def contractor(wave, region):
    return "B" if (wave == 2025 and region in (2, 3)) else "A"


def expit(x):
    return 1.0 / (1.0 + np.exp(-x))


def rng_for(*keys):
    return np.random.default_rng([SEED] + [int(k) for k in keys])


# ---------------------------------------------------------------------------------------------------------------
# frames
# ---------------------------------------------------------------------------------------------------------------
def frames():
    """Every sampled area with its old (pre-April 2024) and new code and region, stratum and position.

    Old frame: region r's core areas r001..r0K, the Central Valley supplement 2062..2081 after its core.
    New frame: each region's remaining old core areas in old order, then the gained areas in old-code order, then
    (Central Valley) the supplement block.
    """
    old = []
    for r in (1, 2, 3, 4, 5):
        for i in range(1, OLD_K[r] + 1):
            old.append(dict(old_region=r, old_pos=i, old_code="%d%03d" % (r, i), supplement=False))
    for j in range(20):
        old.append(dict(old_region=2, old_pos=OLD_K[2] + 1 + j, old_code="%d%03d" % (2, OLD_K[2] + 1 + j),
                        supplement=True))
    for a in old:
        a["new_region"] = MOVES.get((a["old_region"], a["old_pos"]), a["old_region"])
    areas = []
    for r in (1, 2, 3, 4, 5):
        stay = [a for a in old if a["old_region"] == r and a["new_region"] == r and not a["supplement"]]
        gain = sorted([a for a in old if a["new_region"] == r and a["old_region"] != r], key=lambda a: a["old_code"])
        supp = [a for a in old if a["new_region"] == r and a["supplement"]]
        seq = stay + gain + supp
        for n, a in enumerate(seq, 1):
            a["new_code"] = "%d%03d" % (r, n)
            a["stratum"] = "2S" if a["supplement"] else str(r)
            areas.append(a)
    assert len(areas) == 300 and len({a["new_code"] for a in areas}) == 300
    k = {r: sum(1 for a in areas if a["new_region"] == r) for r in (1, 2, 3, 4, 5)}
    assert k == {1: 20, 2: 80, 3: 100, 4: 40, 5: 60}, k
    return areas


# ---------------------------------------------------------------------------------------------------------------
# the population of areas: weights, dwellings, effects
# ---------------------------------------------------------------------------------------------------------------
def populate(areas):
    rng = rng_for(1)
    for r in (1, 2, 3, 4, 5):
        for spec in DESIGN[r]:
            mem = [a for a in areas if a["new_region"] == r and a["stratum"] == spec["stratum"]]
            assert len(mem) == spec["k"], (r, spec["stratum"], len(mem))
            rel = rng.lognormal(0.0, 0.05 if spec["stratum"] != "2S" else 0.12, spec["k"])
            rel = rel / rel.sum() * spec["share"] * HOUSEHOLDS[r]          # each area's weighted households
            for a, wd in zip(mem, rel):
                a["spec"] = spec
                if spec["stratum"] == "2S":
                    occ = int(rng.integers(160, 430))
                elif r == 1:
                    occ = int(rng.integers(140, 520))
                else:
                    occ = int(rng.integers(230, 760))
                a["occupied"] = {2025: occ}
                a["design_weight"] = round(float(wd / occ), 2)
                tau2 = spec["tau"] ** 2
                a["u"] = float(rng.normal(0.0, np.sqrt(PERSIST * tau2)))
                a["e"] = {w: float(rng.normal(0.0, np.sqrt((1 - PERSIST) * tau2))) for w in (2023, 2024, 2025)}
                a["mu"] = spec["mu"]
    # occupied dwellings drift by listing (relisted every wave)
    for a in areas:
        o = a["occupied"][2025]
        g = 0.035 if a["stratum"] == "2S" else 0.008
        a["occupied"][2024] = max(60, int(round(o / (1 + g) + rng.normal(0, 3))))
        a["occupied"][2023] = max(60, int(round(a["occupied"][2024] / (1 + g) + rng.normal(0, 3))))
    return areas


def area_p(a, wave):
    return float(expit(a["mu"] + WAVE_SHIFT[wave] + a["u"] + a["e"][wave]))


# ---------------------------------------------------------------------------------------------------------------
# fieldwork: every issued address and its outcome
# ---------------------------------------------------------------------------------------------------------------
# outcome classes in the clean truth
COMPLETE, PROXY, PARTIAL, REFUSAL, NONCONTACT, VACANT, OTHER, WITHDRAWN = "C", "CP", "P", "R", "NC", "V", "O", "W"


# 2024 schedule: the areas whose new number repeats a pre-2024 number that moved region are worked after Northmark's
# switch; the areas that moved region are worked in the first three weeks of April; one area whose new number the
# pre-2024 numbering never had opens on the switch day.
POST_2024 = {"1005", "1011", "1016", "2018", "2038", "2050", "3015", "3033", "3040", "3061", "3087", "4007", "4020",
             "4031", "5009", "5027", "5044", "2061", "2062", "2063"}
APRIL_2024 = {"1018": 4, "1019": 5, "1020": 6, "2059": 4, "2060": 5, "3098": 6, "3099": 4, "3100": 5, "4037": 6,
              "4038": 4, "4039": 5, "4040": 6, "5056": 4, "5057": 5, "5058": 6, "5060": 4}
SWITCH_DAY_2024 = {"5059": 7}
FRIDAY_2024 = {"2080": dt.date(2024, 4, 19)}         # a supplement area's late workload, sent out on a Friday


def _main_week(a, wave, rng, n_weeks):
    code = a["new_code"]
    if wave == 2024:
        if code in SWITCH_DAY_2024:
            return SWITCH_DAY_2024[code]
        if code in APRIL_2024:
            return APRIL_2024[code]
        if code in POST_2024:
            return int(rng.integers(7, n_weeks - 4))
        return int(rng.integers(0, n_weeks - 4))
    return int(rng.integers(0, n_weeks - 4))


def _friday_after(d):
    return d + dt.timedelta(days=(4 - d.weekday()) % 7)


def fieldwork(areas):
    """cases[wave] = one dict per issued case (a reissue is a case of its own).

    The centre works each area to a fixed take of completed interviews: a first batch of addresses sized on the
    expected response goes out on the area's Monday, top-up batches follow on later Mondays until the take is
    reached, refusals may be reissued for conversion on a Friday, and addresses still open when the take is
    reached are withdrawn. Every area draws its outcomes from its own stream, so one wave's schedule never moves
    another wave's sample."""
    cases = {}
    for wave in (2023, 2024, 2025):
        weeks = ASSIGN_WEEKS[wave]
        out = []
        for idx, a in enumerate(areas):
            rng = rng_for(2, wave, idx)
            rng_l = rng_for(3, wave, idx)
            spec = a["spec"]
            p = area_p(a, wave)
            rr = spec["rr"] * float(np.clip(rng.normal(1.0, 0.07), 0.8, 1.2))
            take = spec["take"]
            used = a.setdefault("used_lines", set())
            pool = [ln for ln in range(1, int(a["occupied"][wave] * 1.07) + 1) if ln not in used]
            rng_l.shuffle(pool)
            when = weeks[_main_week(a, wave, rng, len(weeks))]
            if wave == 2024 and a["new_code"] in FRIDAY_2024:
                when = FRIDAY_2024[a["new_code"]]
            done = 0
            batch_no = 0
            reissue_q = []
            area_cases = []
            while done < take and batch_no < 6 and when < FIELD_CLOSE[wave] - dt.timedelta(days=12):
                need = take - done
                size = int(np.ceil(need / (rr * 0.94))) + (1 if batch_no else 0)
                lines = sorted(pool[:size])
                pool = pool[size:]
                batch = [_one_case(rng, a, wave, when, int(ln), p, rr) for ln in lines]
                batch += reissue_q
                reissue_q = []
                over = rng.random() < 0.09          # an interview already booked when the take is reached is kept
                for c in sorted(batch, key=lambda c: (c["outcome_date"], c["assigned"], c["line"])):
                    if done >= take and over and c["cls"] in (COMPLETE, PROXY):
                        over = False
                        done += 1
                        used.add(c["line"])
                        area_cases.append(c)
                        continue
                    if done >= take:
                        c["cls"] = WITHDRAWN
                        c.pop("y", None)
                        c.pop("item", None)
                        c.pop("hh_size", None)
                        c["outcome_date"] = max(c["assigned"], min(c["outcome_date"], c["assigned"] + dt.timedelta(days=int(rng.integers(3, 12)))))
                    elif c["cls"] in (COMPLETE, PROXY):
                        done += 1
                    elif c["cls"] == REFUSAL and c["reissue_of"] is None and rng.random() < 0.34:
                        fri = _friday_after(c["outcome_date"] + dt.timedelta(days=int(rng.integers(5, 12))))
                        if fri < FIELD_CLOSE[wave] - dt.timedelta(days=10):
                            reissue_q.append(_one_case(rng, a, wave, fri, c["line"], p, rr, reissue_of=c))
                    used.add(c["line"])
                    area_cases.append(c)
                batch_no += 1
                when = when + dt.timedelta(weeks=int(rng.integers(2, 4)))
            out.extend(area_cases)
        cases[wave] = out
    return cases


def _one_case(rng, a, wave, assign, line, p, rr, reissue_of=None):
    c = dict(area=a, wave=wave, assigned=assign, line=line, reissue_of=reissue_of)
    u = rng.random()
    if reissue_of is not None:
        cls = PROXY if u < 0.02 else (COMPLETE if u < 0.25 else (REFUSAL if u < 0.80 else NONCONTACT))
    elif u < 0.06:
        cls = VACANT
    else:
        v = rng.random()
        if v < rr:
            cls = PROXY if rng.random() < 0.075 else COMPLETE
        elif v < rr + 0.03:
            cls = PARTIAL
        elif v < rr + 0.03 + (1 - rr - 0.03) * 0.56:
            cls = REFUSAL
        elif v < 0.995:
            cls = NONCONTACT
        else:
            cls = OTHER
    c["cls"] = cls
    lag = int(rng.integers(1, 30))
    c["outcome_date"] = min(assign + dt.timedelta(days=lag), FIELD_CLOSE[wave])
    if cls in (COMPLETE, PROXY, PARTIAL):
        y = int(rng.random() < p)
        c["y"] = y
        item = "yes" if y == 1 else ("noRx" if rng.random() < 0.37 else "no")
        w = rng.random()
        if w < 0.0055:
            item = "dk"
        elif w < 0.008:
            item = "ref"
        if cls == PARTIAL and rng.random() < 0.55:
            item = None
        c["item"] = item
        c["hh_size"] = int(rng.choice([1, 2, 2, 2, 3, 3, 4, 4, 5, 6]))
    return c


def world():
    areas = populate(frames())
    cases = fieldwork(areas)
    return dict(areas=areas, cases=cases)


# ---------------------------------------------------------------------------------------------------------------
# clean analysis tables, straight from the truth (no exports, no codes)
# ---------------------------------------------------------------------------------------------------------------
def usable(c):
    return c["cls"] in (COMPLETE, PROXY) and c.get("item") in ("yes", "no", "noRx")


def wave_table(w, wave):
    """Per new region: arrays of area index, take, weight share, y for the wave's usable completes, from the truth.

    The weight of a completed interview is the area's design weight x occupied dwellings / completed interviews
    (every complete, the item answered or not)."""
    areas = w["areas"]
    comp = {}
    for c in w["cases"][wave]:
        if c["cls"] in (COMPLETE, PROXY):
            comp.setdefault(id(c["area"]), []).append(c)
    out = {}
    for r in (1, 2, 3, 4, 5):
        rows = []
        for a in areas:
            if a["new_region"] != r:
                continue
            cs = comp.get(id(a), [])
            m_all = len(cs)
            if m_all == 0:
                continue
            wt = a["design_weight"] * a["occupied"][wave] / m_all
            ys = [c["y"] for c in cs if usable(c)]
            rows.append(dict(code=a["new_code"], stratum=a["stratum"], m_all=m_all, w=wt, y=np.array(ys, float),
                             wd=a["design_weight"] * a["occupied"][wave]))
        out[r] = rows
    return out
