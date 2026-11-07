"""task232 architecture 2: the Household Life Panel's world, simulated quarter by quarter from 2024 Q2 so that the
2025 and 2026 waves carry their earlier rotation groups.

Tobar Social Research runs a quarterly face-to-face household panel in eight Connacht and Munster counties. Each
quarter a new rotation group of dwellings enters every small area (PSU) and stays five quarters. Each PSU belongs to
one field interviewer's patch; a neighbouring interviewer covers a patch for the quarter its interviewer is on leave;
three patches change hands for good; non-contacts are reissued within the quarter to the county's senior
interviewer. Interviewers differ in how they roster (a few leave a member off, one counts a visitor as a resident)
and in which households agree to take part.

Everything here is the truth; pack.py writes what the organisation's systems record."""
import numpy as np

SEED = 23202
QUARTERS = ["2024Q2", "2024Q3", "2024Q4"] + ["%dQ%d" % (y, q) for y in (2025, 2026) for q in (1, 2, 3, 4)]
WINDOW = QUARTERS[3:]                     # 2025Q1 to 2026Q4, the files' window
COUNTIES = ["Galway", "Mayo", "Sligo", "Roscommon", "Clare", "Limerick", "Kerry", "Cork"]
CCODE = {"Galway": "GY", "Mayo": "MO", "Sligo": "SO", "Roscommon": "RN", "Clare": "CE", "Limerick": "LK",
         "Kerry": "KY", "Cork": "CK"}
PATCHES = {"Galway": 7, "Mayo": 5, "Sligo": 4, "Roscommon": 4, "Clare": 5, "Limerick": 6, "Kerry": 5, "Cork": 8}
PSU_PER_PATCH = 6
DW_PER_GROUP = 7
SENIOR_COUNTIES = [("Galway", "Mayo"), ("Sligo", "Roscommon"), ("Clare", "Limerick"), ("Kerry", "Cork")]
SENIOR_COUNTIES_2026 = [("Mayo", "Sligo"), ("Roscommon", "Galway"), ("Limerick", "Kerry"), ("Cork", "Clare")]

# PSU character: the household size the frame cannot see (beyond dwelling type, bedrooms and urban class)
PSU_TYPES = {"town_centre": -0.06, "suburb_family": 0.07, "rural": 0.0, "coastal_retired": -0.25,
             "student": 0.25, "estate_mixed": 0.03}
TYPE_MIX = {
    "Galway": ["town_centre", "student", "suburb_family", "rural", "estate_mixed", "coastal_retired"],
    "Mayo": ["rural", "coastal_retired", "rural", "estate_mixed", "suburb_family"],
    "Sligo": ["town_centre", "rural", "coastal_retired", "estate_mixed"],
    "Roscommon": ["rural", "rural", "suburb_family", "estate_mixed"],
    "Clare": ["coastal_retired", "rural", "suburb_family", "estate_mixed", "rural"],
    "Limerick": ["town_centre", "student", "suburb_family", "estate_mixed", "rural", "suburb_family"],
    "Kerry": ["coastal_retired", "rural", "coastal_retired", "estate_mixed", "town_centre"],
    "Cork": ["town_centre", "student", "suburb_family", "estate_mixed", "rural", "suburb_family", "coastal_retired",
             "rural"],
}


def _rng(*key):
    h = SEED
    for k in key:
        for ch in str(k):
            h = (h * 131 + ord(ch)) % 2147483647
    return np.random.default_rng(h)


def build():
    r = _rng("world")
    # interviewers: patch interviewers per county, then four seniors
    ivs = {}
    code_pool = list(range(2104, 2104 + 400, 7))
    r.shuffle(code_pool)
    ci = 0
    patches = []
    for c in COUNTIES:
        for k in range(PATCHES[c]):
            code = "%d" % code_pool[ci]
            ci += 1
            ivs[code] = {"code": code, "county": c, "grade": "Field interviewer", "start": "2019Q1", "end": None}
            patches.append({"county": c, "idx": k, "iv": code, "type": TYPE_MIX[c][k % len(TYPE_MIX[c])]})
    seniors = {}
    seniors26 = {}
    for pair, pair26 in zip(SENIOR_COUNTIES, SENIOR_COUNTIES_2026):
        code = "%d" % code_pool[ci]
        ci += 1
        ivs[code] = {"code": code, "county": pair[0], "grade": "Senior interviewer", "start": "2016Q1", "end": None}
        for c in pair:
            seniors[c] = code
        for c in pair26:
            seniors26[c] = code
    # permanent hand-overs: three patches change interviewer (leaver, new code)
    changes = {}
    for pi, q in ((3, "2025Q3"), (17, "2026Q1"), (30, "2025Q4")):
        old = patches[pi]["iv"]
        new = "%d" % code_pool[ci]
        ci += 1
        ivs[old]["end"] = QUARTERS[QUARTERS.index(q) - 1]
        ivs[new] = {"code": new, "county": patches[pi]["county"], "grade": "Field interviewer", "start": q,
                    "end": None}
        changes[pi] = (q, old, new)
    # recording behaviour and cooperation skill
    codes = sorted(ivs)
    for code in codes:
        rr = _rng("iv", code)
        ivs[code]["omit"] = 0.0
        ivs[code]["add"] = float(rr.uniform(0.0, 0.025))
        ivs[code]["skill"] = float(rr.normal(0.0, 0.6))
    # the shortcutters (patch interviewers in family, rural and mixed patches) and the one who counts visitors
    by_type = {}
    for pi, p in enumerate(patches):
        by_type.setdefault(p["type"], []).append(pi)
    gone = {3, 17, 30}
    fam = [pi for pi in by_type["suburb_family"] if pi not in gone]
    rur = [pi for pi in by_type["rural"] if pi not in gone]
    mix = [pi for pi in by_type["estate_mixed"] if pi not in gone]
    ret = [pi for pi in by_type["coastal_retired"] if pi not in gone]
    town = [pi for pi in by_type["town_centre"] if pi not in gone]
    short = [ret[2], rur[2], mix[2], fam[3], rur[4], town[2]]
    add_rates = [0.215, 0.33, 0.28, 0.40, 0.36, 0.30]
    for pi, a in zip(short, add_rates):
        ivs[patches[pi]["iv"]]["add"] = a
    adder = short[-1]
    # cooperation skill that tilts which households take part (strong on families, weak on them)
    tilt = {by_type["coastal_retired"][1]: -1.6, by_type["student"][1]: 1.5, by_type["town_centre"][1]: -1.4,
            by_type["suburb_family"][2]: 1.4, by_type["rural"][0]: -1.3}
    for pi, s in tilt.items():
        ivs[patches[pi]["iv"]]["skill"] = s
    for c, code in seniors.items():
        ivs[code]["skill"] = 0.2
    # leave: each patch interviewer takes one quarter in the window, covered by the next patch in the county
    leave = {}
    for pi, p in enumerate(patches):
        rr = _rng("leave", pi)
        qs = sorted(rr.choice(len(WINDOW), size=2, replace=False))
        same = [j for j, o in enumerate(patches) if o["county"] == p["county"] and j != pi]
        leave[pi] = {WINDOW[qs[0]]: same[int(rr.integers(0, len(same)))],
                     WINDOW[qs[1]]: same[int(rr.integers(0, len(same)))]}
    # PSUs and dwellings
    psus = []
    for pi, p in enumerate(patches):
        for k in range(PSU_PER_PATCH):
            rr = _rng("psu", pi, k)
            t = p["type"] if rr.uniform() < 0.8 else TYPE_MIX[p["county"]][int(rr.integers(0, len(TYPE_MIX[p["county"]])))]
            psus.append({"psu": "%s%03d" % (CCODE[p["county"]], len(psus) + 101), "county": p["county"], "patch": pi,
                         "type": t, "noise": float(rr.normal(0, 0.04)),
                         "urban": t in ("town_centre", "student", "suburb_family", "estate_mixed")})
    dwellings = []
    for si, s in enumerate(psus):
        for qi, q in enumerate(QUARTERS[:len(QUARTERS)]):
            seg = float(_rng("seg", si, q).normal(0.0, 0.55))
            for k in range(DW_PER_GROUP):
                rr = _rng("dw", si, q, k)
                if s["urban"]:
                    dtype = rr.choice(["Apartment", "Terraced house", "Semi-detached house", "Detached house"],
                                      p=[0.28, 0.32, 0.28, 0.12])
                else:
                    dtype = rr.choice(["Apartment", "Terraced house", "Semi-detached house", "Detached house"],
                                      p=[0.04, 0.10, 0.26, 0.60])
                beds = int(np.clip(rr.normal({"Apartment": 1.8, "Terraced house": 2.9, "Semi-detached house": 3.2,
                                              "Detached house": 3.8}[dtype], 0.8), 1, 6) + 0.5)
                beds = int(np.clip(beds, 1, 6))
                dwellings.append({"dw": len(dwellings), "psu": si, "group": qi, "dtype": str(dtype), "beds": beds,
                                  "seg": seg})
    # households: one spell per occupancy; size and composition evolve quarter by quarter
    hh = []          # spells
    occ = {}         # (dw, quarter index) -> spell index
    for d in dwellings:
        s = psus[d["psu"]]
        quarters = list(range(d["group"], min(d["group"] + 5, len(QUARTERS))))
        if not quarters:
            continue
        rr = _rng("hh", d["dw"])
        mu = (0.70 + 0.55 * d["beds"] + {"Apartment": -0.25, "Terraced house": 0.0, "Semi-detached house": 0.05,
                                         "Detached house": 0.10}[d["dtype"]]
              + (0.0 if s["urban"] else 0.15) + PSU_TYPES[s["type"]] + s["noise"] + d["seg"])
        spell = None
        seq = 0
        for qi in quarters:
            if spell is None or rr.uniform() < 0.025:
                size = int(max(1, min(9, np.round(rr.normal(mu, 1.0)))))
                spell = len(hh)
                seq += 1
                hh.append({"spell": spell, "dw": d["dw"], "start": qi, "size": {}, "kind": _kind(size, s, rr),
                           "seq": seq})
                cur = size
            else:
                u = rr.uniform()
                if u < 0.018:
                    cur += 1
                elif u < 0.030 and cur > 1:
                    cur -= 1
                elif u < 0.036:
                    cur += 1
            hh[spell]["size"][qi] = cur
            occ[(d["dw"], qi)] = spell
    return {"ivs": ivs, "patches": patches, "seniors": seniors, "seniors26": seniors26, "changes": changes, "leave": leave, "psus": psus,
            "dwellings": dwellings, "hh": hh, "occ": occ, "short": [patches[pi]["iv"] for pi in short],
            "adder": patches[adder]["iv"]}


def _kind(size, s, rr):
    if size == 1:
        return "single_working" if rr.uniform() < (0.7 if s["type"] in ("town_centre", "student") else 0.35) else "single_home"
    if size == 2:
        return "couple_working" if rr.uniform() < 0.55 else "couple_home"
    return "family"


CONTACT = {"single_working": 0.64, "single_home": 0.94, "couple_working": 0.76, "couple_home": 0.95, "family": 0.92}


def field(W):
    """Who worked each issued case each quarter, the contact and cooperation outcomes, and the roster each
    interviewer recorded. Returns case and interview lists in quarter order."""
    ivs, patches, psus = W["ivs"], W["patches"], W["psus"]
    cases, interviews = [], []
    for d in W["dwellings"]:
        s = psus[d["psu"]]
        pi = s["patch"]
        for qi in range(d["group"], min(d["group"] + 5, len(QUARTERS))):
            q = QUARTERS[qi]
            wave = qi - d["group"] + 1
            iv = patches[pi]["iv"]
            if pi in W["changes"]:
                cq, old, new = W["changes"][pi]
                iv = new if QUARTERS.index(q) >= QUARTERS.index(cq) else old
            cover = W["leave"][pi].get(q)
            if cover is not None:
                same = [j for j, o in enumerate(patches) if o["county"] == s["county"] and j != pi]
                cover = same[int(_rng("cover", d["psu"], q).integers(0, len(same)))]
                iv = patches[cover]["iv"]
                if cover in W["changes"]:
                    cq, old, new = W["changes"][cover]
                    iv = new if QUARTERS.index(q) >= QUARTERS.index(cq) else old
            spell = W["occ"][(d["dw"], qi)]
            h = W["hh"][spell]
            size = h["size"][qi]
            rr = _rng("case", d["dw"], q)
            eligible = rr.uniform() > 0.035
            case = {"dw": d["dw"], "q": qi, "wave": wave, "iv": iv, "spell": spell, "eligible": eligible,
                    "reissue": None, "outcome": None}
            if not eligible:
                case["outcome"] = "ineligible"
                cases.append(case)
                continue
            contact = rr.uniform() < CONTACT[h["kind"]]
            if not contact:
                case["outcome"] = "non_contact"
                senior = (W["seniors26"] if q.startswith("2026") else W["seniors"])[s["county"]]
                if rr.uniform() < 0.85:
                    re = {"iv": senior, "outcome": None}
                    if rr.uniform() < 0.58:
                        re["outcome"] = _cooperate(rr, ivs[senior], size)
                    else:
                        re["outcome"] = "non_contact"
                    case["reissue"] = re
                    if re["outcome"] == "complete":
                        interviews.append(_interview(rr, ivs[senior], case, h, size, reissue=True))
                cases.append(case)
                continue
            case["outcome"] = _cooperate(rr, ivs[iv], size)
            if case["outcome"] == "complete":
                interviews.append(_interview(rr, ivs[iv], case, h, size, reissue=False))
            cases.append(case)
    return cases, interviews


def _cooperate(rr, iv, size):
    p = 0.80 + 0.06 * iv["skill"] * (min(size, 6) - 2.6) / 1.4
    return "complete" if rr.uniform() < min(0.97, max(0.35, p)) else "refusal"


def _interview(rr, iv, case, h, size, reissue):
    rec = size
    if size >= 2 and rr.uniform() < iv["omit"]:
        rec -= 1
    visitor = rr.uniform() < iv["add"]
    return {"dw": case["dw"], "q": case["q"], "wave": case["wave"], "iv": iv["code"], "spell": case["spell"],
            "true": size, "recorded": rec, "visitor_as_resident": visitor,
            "recorded_resident": rec + (1 if visitor else 0), "reissue": reissue}
