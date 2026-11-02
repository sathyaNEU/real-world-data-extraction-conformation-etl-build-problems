"""The clean truth of the task301 world: the region's municipalities, the 2026 living conditions survey (its
fieldwork, households, persons, 2025 incomes, weights and tax links), the Complemento Familiar's administrative
register since its 2022 launch, and the 2025 survey wave kept as a distractor. Nothing here is messy; pack.py writes
the files the way the producing systems export them."""
import datetime as dt
import math

import numpy as np

import params as P

PREFIX = ["Villa", "Torre", "Fuente", "Nava", "Valde", "Castro", "Puebla", "Quintana", "Aldea", "Casas", "Mota",
          "Pozo", "Ríos", "Peña", "Cabeza", "Cerro", "Llano", "Olmeda", "Sotillo", "Robledo"]
SUFFIX = ["rubia", "nueva", "alba", "seca", "larga", "verde", "mayor", "fría", "honda", "clara", "llana", "blanca",
          "rasa", "alta", "baja", "oscura", "lengua", "pardilla", "moro", "carrasca"]
TAIL = ["", "", "", " de Arce", " del Campo", " de la Sierra", " de Abajo", " del Río", " de Tajuelo",
        " de los Montes", " del Valle", " de la Vega"]


def municipalities(rng):
    """Municipalities with INE-style codes, population shares within province and the fieldwork and benefits
    office that serves them. The last few municipalities of Sierra del Alba are served from Las Cuencas, and the
    last few of Las Cuencas from Valmesura (the offices nearest by road)."""
    out = []
    used = set()
    counts = {"81": 31, "82": 26, "83": 21}
    office = {"81": "VAL", "82": "CUE", "83": "SIE"}
    for pc, pname in P.PROVINCES:
        n = counts[pc]
        sizes = np.sort(rng.pareto(1.25, n) + 1.0)[::-1]
        sizes[0] *= 5.5 if pc == "81" else 3.2
        shares = sizes / sizes.sum()
        order = rng.permutation(n)
        for i in range(n):
            code = "%s%03d" % (pc, int(order[i]) * 3 + 1 + int(rng.integers(0, 3)))
            while code in used:
                code = "%s%03d" % (pc, int(code[2:]) + 1)
            used.add(code)
            if i == 0:
                name = {"81": "Valmesura", "82": "Cuenca del Arlés", "83": "Albadía"}[pc]
            else:
                while True:
                    name = rng.choice(PREFIX) + rng.choice(SUFFIX) + rng.choice(TAIL)
                    if name not in [m["name"] for m in out]:
                        break
            serve = office[pc]
            # border municipalities: small ones at the far end of the size ranking
            if pc == "83" and i >= n - 5:
                serve = "CUE"
            if pc == "82" and i >= n - 4:
                serve = "VAL"
            out.append({"code": code, "name": name, "prov": pc, "share": float(shares[i]), "office": serve})
    return out


def ages_for(t, rng):
    """(age on 1 January 2027, role) per member; role R reference, P partner, C child, G grandparent, O other."""
    m = []
    if t == "single":
        m = [(int(rng.integers(20, 67)), "R")]
    elif t == "couple":
        a = int(rng.integers(23, 67))
        m = [(a, "R"), (max(20, a + int(rng.integers(-6, 7))), "P")]
    elif t == "couple_kids":
        a = int(rng.integers(25, 57))
        m = [(a, "R"), (max(21, a + int(rng.integers(-5, 6))), "P")]
        k = int(rng.choice([1, 2, 3, 4], p=[.45, .42, .11, .02]))
        m += [(int(rng.integers(0, 18)), "C") for _ in range(k)]
        if rng.random() < 0.10:
            m.append((int(rng.integers(18, 25)), "C"))      # an adult son or daughter still at home
    elif t == "lone":
        a = int(rng.integers(21, 56))
        m = [(a, "R")]
        k = int(rng.choice([1, 2, 3], p=[.52, .36, .12]))
        m += [(int(rng.integers(0, 18)), "C") for _ in range(k)]
    elif t == "multi_kids":
        a = int(rng.integers(26, 51))
        m = [(a, "R"), (a + int(rng.integers(-4, 5)), "P"), (int(rng.integers(58, 85)), "G")]
        k = int(rng.choice([1, 2, 3], p=[.45, .40, .15]))
        m += [(int(rng.integers(0, 18)), "C") for _ in range(k)]
    elif t == "pens1":
        m = [(int(rng.integers(66, 93)), "R")]
    elif t == "pens2":
        a = int(rng.integers(66, 89))
        m = [(a, "R"), (a + int(rng.integers(-5, 6)), "P")]
    else:
        m = [(int(rng.integers(19, 70)), "R")] + [(int(rng.integers(19, 70)), "O") for _ in range(int(rng.integers(1, 4)))]
    return m


def oecd_scale(ages):
    big = sorted([a for a in ages if a >= 14], reverse=True)
    small = [a for a in ages if a < 14]
    if not big:
        return 1.0 + 0.3 * (len(small) - 1)
    return 1.0 + 0.5 * (len(big) - 1) + 0.3 * len(small)


TYPES = [("single", .245), ("couple", .225), ("couple_kids", .205), ("lone", .052), ("multi_kids", .036),
         ("pens1", .10), ("pens2", .085), ("other", .052)]
MU = {"single": 9.856, "couple": 10.006, "couple_kids": 9.746, "lone": 9.446, "multi_kids": 9.626, "pens1": 9.726,
      "pens2": 9.866, "other": 9.826}
SD = {"single": .52, "couple": .48, "couple_kids": .50, "lone": .52, "multi_kids": .46, "pens1": .36, "pens2": .34,
      "other": .50}
PROV_EFFECT = {"81": 0.035, "82": -0.020, "83": -0.055}


RESECTION = dt.date(2026, 4, 1)


def fieldwork(rng, munis):
    """The 2026 sample of dwellings, first issue and reissue cases, with each case's outcome; the dwellings whose
    final outcome is a complete interview become the survey's households."""
    by_prov = {pc: [m for m in munis if m["prov"] == pc] for pc, _ in P.PROVINCES}
    n_issue = 17640
    alloc = {"81": int(n_issue * 0.44), "82": int(n_issue * 0.33)}
    alloc["83"] = n_issue - alloc["81"] - alloc["82"]
    dwellings = []
    seq = 0
    for pc, _ in P.PROVINCES:
        ms = by_prov[pc]
        shares = np.array([m["share"] for m in ms])
        shares = shares / shares.sum()
        picks = rng.choice(len(ms), size=alloc[pc], p=shares)
        for j in picks:
            m = ms[int(j)]
            seq += 1
            section = int(rng.integers(1, 40))
            dwellings.append({"muni": m["code"], "prov": m["prov"], "office": m["office"],
                              "ref": "%s-%03d-%04d" % (m["code"], section, int(rng.integers(1, 9999))),
                              "order": seq})
    # a dwelling's serial is unique within its municipality in the dwelling register
    seen = set()
    for d in dwellings:
        while d["ref"] in seen:
            d["ref"] = d["ref"][:-4] + "%04d" % int(rng.integers(1, 9999))
        seen.add(d["ref"])
    rs = np.random.default_rng(P.SEED + 4401)
    serials = set()
    for d in dwellings:
        while (d["muni"], d["ref"][-4:]) in serials:
            d["ref"] = d["ref"][:-4] + "%04d" % int(rs.integers(1, 9999))
        serials.add((d["muni"], d["ref"][-4:]))
    # the register's census sections were renumbered from 1 April 2026 in part of each municipality; a case issued
    # from that date carries the dwelling's new section
    renum = {}
    for m in munis:
        for sec in range(1, 40):
            if rs.random() < 0.50:
                renum[(m["code"], sec)] = 40 + int(rs.integers(0, 30))
    for d in dwellings:
        sec = int(d["ref"].split("-")[1])
        new_sec = renum.get((d["muni"], sec))
        d["ref_new"] = None if new_sec is None else "%s-%03d-%s" % (d["muni"], new_sec, d["ref"][-4:])
    rng.shuffle(dwellings)
    cases = []
    out_p = {"81": [0.630, 0.010, 0.150, 0.110, 0.019, 0.047, 0.021, 0.013],     # the capital's flats: more no-contact
             "82": [0.648, 0.009, 0.142, 0.094, 0.020, 0.052, 0.022, 0.013],
             "83": [0.665, 0.008, 0.132, 0.080, 0.021, 0.056, 0.025, 0.013]}    # villages: more empty dwellings
    codes = [11, 12, 21, 22, 23, 31, 32, 33]
    interviewers = {o: ["%s%02d" % (o[0], i) for i in range(1, 19)] for o in ("VAL", "CUE", "SIE")}
    for d in dwellings:
        o1 = int(rng.choice(codes, p=out_p[d["prov"]]))
        iv = str(rng.choice(interviewers[d["office"]]))
        start = dt.date(2026, 2, 2) + dt.timedelta(days=int(rng.integers(0, 120)))
        visits = 1 if o1 in (11, 12) and rng.random() < 0.55 else int(rng.integers(1, 6))
        c1 = {"dwelling": d, "issue": 1, "outcome": o1, "interviewer": iv, "visits": visits, "issued": start,
              "closed": start + dt.timedelta(days=int(rng.integers(3, 28)))}
        cases.append(c1)
        d["final"] = o1
        reissue_p = {22: 0.46, 21: 0.24, 23: 0.15}.get(o1, 0.0)
        if rng.random() < reissue_p and c1["closed"] < dt.date(2026, 6, 2):
            o2 = int(rng.choice([11, 21, 22], p=[0.44, 0.27, 0.29]))
            iv2 = str(rng.choice([x for x in interviewers[d["office"]] if x != iv]))
            c2 = {"dwelling": d, "issue": 2, "outcome": o2, "interviewer": iv2, "visits": int(rng.integers(1, 5)),
                  "issued": c1["closed"] + dt.timedelta(days=2),
                  "closed": min(dt.date(2026, 6, 30), c1["closed"] + dt.timedelta(days=int(rng.integers(10, 30))))}
            cases.append(c2)
            d["final"] = o2
    for c in cases:
        d = c["dwelling"]
        c["ref"] = d["ref_new"] if (d["ref_new"] and c["issued"] >= RESECTION) else d["ref"]
    return dwellings, cases


def survey(rng, munis, dwellings):
    """Households on the dwellings with a complete final interview, their members and 2025 incomes."""
    names = [t for t, _ in TYPES]
    probs = np.array([p for _, p in TYPES])
    probs = probs / probs.sum()
    hh = []
    complete = [d for d in dwellings if d["final"] == 11]
    for i, d in enumerate(complete):
        t = names[int(rng.choice(len(names), p=probs))]
        members = ages_for(t, rng)
        ages = [a for a, _ in members]
        eq = oecd_scale(ages)
        mu = MU[t] + PROV_EFFECT[d["prov"]]
        inc_eq = float(math.exp(rng.normal(mu, SD[t])))
        kids = sum(1 for a in ages if a <= 17)
        young = min(ages) < 40 or kids > 0
        p_rent = 0.62 if inc_eq < 12000 else (0.38 if inc_eq < 17000 else 0.17)
        if not young:
            p_rent *= 0.45
        renting = rng.random() < p_rent
        hh.append({"dwelling": d, "type": t, "members": members, "ages": ages, "eq": eq, "kids": kids,
                   "inc_eq25": inc_eq, "renting": renting, "prov": d["prov"]})
    return hh


def finish_survey(rng, hh):
    """Weights, tax links and Complemento receipt for each household; disposable income including it."""
    # weights: province base weights to the target population, varied within province
    persons = {pc: sum(len(h["ages"]) for h in hh if h["prov"] == pc) for pc, _ in P.PROVINCES}
    target = {pc: P.TARGET_PERSONS * s for (pc, _), s in zip(P.PROVINCES, P.PROV_SHARE)}
    for h in hh:
        base = target[h["prov"]] / persons[h["prov"]]
        adj = float(np.exp(rng.normal(0.0, 0.16)))
        if h["type"] in ("single", "other"):
            adj *= 1.08          # nonresponse is higher among single adults
        h["w"] = base * adj
    # tax link: a 2025 return filed, and its household gross income
    for h in hh:
        disp = h["inc_eq25"] * h["eq"]
        if disp > 16000:
            pf = 0.975
        elif disp > 9000:
            pf = 0.80
        else:
            pf = 0.36
        h["filed"] = bool(rng.random() < pf)
        factor = 1.06 + 0.16 * min(1.0, max(0.0, (disp - 9000.0) / 60000.0)) + float(rng.normal(0, 0.012))
        h["gross25"] = round(disp * factor, 2) if h["filed"] else None
    # Complemento: assessed on the latest closed tax year at award or review, so the assessed income differs a
    # little from 2025's; entitled when the assessed computable income per equivalent adult is under the limit
    for h in hh:
        h["cfv_recv25"] = 0.0
        h["cfv_now"] = False
        h["cfv_months25"] = 0
        if h["kids"] == 0:
            h["comp_eq"] = h["inc_eq25"]
            continue
        assessed = h["inc_eq25"] * float(np.exp(rng.normal(0.0, 0.07)))
        h["assessed"] = assessed
        entitled = assessed < P.CFV_LIMIT
        if entitled and rng.random() < 0.82:
            start = 1 if rng.random() < 0.86 else int(rng.integers(2, 12))
            end = 12 if rng.random() < 0.93 else int(rng.integers(start, 12))
            months = end - start + 1
            amt = 0.0
            for mth in range(start, end + 1):
                amt += (95.0 if mth <= 6 else 100.0) * h["kids"]
            h["cfv_recv25"] = round(amt, 2)
            h["cfv_months25"] = months
            h["cfv_now"] = end == 12 and rng.random() < 0.95
        h["comp_eq"] = h["inc_eq25"]
    for h in hh:
        h["disp25"] = round(h["inc_eq25"] * h["eq"] + h["cfv_recv25"], 2)
        # computable income: disposable less the Complemento, per equivalent adult
        h["comp_eq"] = (h["disp25"] - h["cfv_recv25"]) / h["eq"]
    return hh


def poverty_line(hh):
    """60 per cent of the weighted person median of 2025 equivalised disposable income, carried to 2027 with the
    uprating and rounded to ten euros: the figure the department files."""
    vals = sorted((h["disp25"] / h["eq"], h["w"] * len(h["ages"])) for h in hh)
    tot = sum(w for _, w in vals)
    acc = 0.0
    for v, w in vals:
        acc += w
        if acc >= tot / 2.0:
            med = v
            break
    return med, int(round(0.6 * med * P.UPRATE_2025_2027 / 10.0)) * 10


def build(seed=P.SEED):
    rng = np.random.default_rng(seed)
    munis = municipalities(rng)
    dwellings, cases = fieldwork(rng, munis)
    hh = survey(rng, munis, dwellings)
    hh = finish_survey(rng, hh)
    med, line = poverty_line(hh)
    return {"munis": munis, "dwellings": dwellings, "cases": cases, "hh": hh, "rng": rng, "median25": med,
            "line": line}
