"""task445 architecture 3: the Arafura Examinations Board's 2026 Senior Certificate History Paper 2, simulated.

Candidates answer two of three optional essays (Questions 4, 5 and 6, 25 marks each) after a compulsory Section A
(40 marks). Each essay's mark follows the candidate's attainment, their knowledge of the essay's topic, their centre
and the question's own demand; candidates choose the essays whose topics they know, Question 6 looking hardest, so
few attempt it and those who do know its topic. About one candidate in twenty writes all three essays; the board
marks every essay and credits the best two. Every number is drawn from a fixed seed."""
import datetime as dt

import numpy as np

SEED = 4453
DEMAND = {"4": 0.0, "5": -0.3, "6": 1.95}          # marks harder than Question 4, for the same candidate
TOPIC_W, CHOICE_W, LOOK = 3.4, 2.0, {"4": 0.0, "5": 0.1, "6": 2.6}
INFRINGE = (0.035, 0.035)                          # base share writing all three, extra share below average
TIME_COST = 1.5                                    # marks a candidate writing three essays loses on each
BOUNDS = [("A", 66), ("B", 57), ("C", 48), ("D", 39), ("E", 30)]
LINE, ROUND_TO = 1.5, 1

REGIONS = [  # code, name, countries with (tz name, offset hours), centres, mean attainment shift
    ("NT", "Northern Territory", [("Australia", "Australia/Darwin", 9.5)], 34, -0.10),
    ("QT", "Queensland and Torres Strait", [("Australia", "Australia/Brisbane", 10.0)], 92, 0.05),
    ("WA", "Western Australia", [("Australia", "Australia/Perth", 8.0)], 71, 0.10),
    ("PC", "Pacific", [("Fiji", "Pacific/Fiji", 12.0), ("Papua New Guinea", "Pacific/Port_Moresby", 10.0),
                       ("Vanuatu", "Pacific/Efate", 11.0), ("Solomon Islands", "Pacific/Guadalcanal", 11.0)], 58, -0.25),
    ("ID", "Indonesia and Timor-Leste", [("Indonesia", "Asia/Jakarta", 7.0), ("Timor-Leste", "Asia/Dili", 9.0)], 47, -0.05),
    ("MS", "Malaysia and Singapore", [("Malaysia", "Asia/Kuala_Lumpur", 8.0), ("Singapore", "Asia/Singapore", 8.0)], 61, 0.20),
]
TOWNS = {"Australia/Darwin": ["Darwin", "Palmerston", "Katherine", "Alice Springs", "Nhulunbuy", "Tennant Creek"],
         "Australia/Brisbane": ["Brisbane", "Cairns", "Townsville", "Mackay", "Thursday Island", "Toowoomba", "Gladstone"],
         "Australia/Perth": ["Perth", "Broome", "Karratha", "Geraldton", "Kalgoorlie", "Albany", "Bunbury"],
         "Pacific/Fiji": ["Suva", "Nadi", "Lautoka", "Labasa"], "Pacific/Port_Moresby": ["Port Moresby", "Lae", "Madang"],
         "Pacific/Efate": ["Port Vila", "Luganville"], "Pacific/Guadalcanal": ["Honiara", "Gizo"],
         "Asia/Jakarta": ["Jakarta", "Bandung", "Surabaya", "Medan"], "Asia/Dili": ["Dili", "Baucau"],
         "Asia/Kuala_Lumpur": ["Kuala Lumpur", "Penang", "Johor Bahru", "Kota Kinabalu", "Kuching"],
         "Asia/Singapore": ["Singapore"]}
KINDS = ["College", "Grammar School", "Christian College", "International School", "Secondary College",
         "Catholic College", "Anglican School", "State High School", "Academy"]


def build(seed=SEED):
    rng = np.random.default_rng(seed)
    centres = []
    used = set()
    for code, rname, countries, n, shift in REGIONS:
        for k in range(n):
            country, tz, off = countries[k % len(countries)] if len(countries) > 1 and k % 3 else countries[0]
            while True:
                num = int(rng.integers(1100, 9800))
                if (code, num) not in used:
                    used.add((code, num))
                    break
            town = TOWNS[tz][int(rng.integers(0, len(TOWNS[tz])))]
            kind = KINDS[int(rng.integers(0, len(KINDS)))]
            centres.append(dict(code="%s%04d" % (code, num), region=code, region_name=rname, country=country, tz=tz,
                                offset=off, name="%s %s" % (town, kind), size=int(rng.integers(14, 160)),
                                effect=float(rng.normal(shift, 0.35))))
    # a 2025 merger of two Queensland school groups gave 18 centres new codes; the marking system still keys
    # those centres' scripts by the old codes, which the centres register keeps as merged_from
    qt = [c for c in centres if c["region"] == "QT"]
    for c in qt[:18]:
        while True:
            num = int(rng.integers(1100, 9800))
            if ("QL", num) not in used:
                used.add(("QL", num))
                break
        c["old_code"] = "QL%04d" % num
    cands = []
    serial = 104000
    for c in centres:
        for _ in range(c["size"]):
            serial += int(rng.integers(1, 4))
            cands.append(dict(no="26-%06d" % serial, centre=c["code"], region=c["region"], ceff=c["effect"]))
    n = len(cands)
    a = rng.normal(0, 1, n) + np.array([x["ceff"] for x in cands]) * 0.0
    ce = np.array([x["ceff"] for x in cands])
    t = rng.normal(0, 1, (n, 3))
    sec_a = np.clip(np.round(24 + 6.5 * a + 2.0 * ce + rng.normal(0, 2.6, n)), 0, 40).astype(int)
    qs = ["4", "5", "6"]
    raw = np.stack([13.0 + 3.6 * a + TOPIC_W * t[:, j] + 1.5 * ce - DEMAND[q] + rng.normal(0, 2.1, n)
                    for j, q in enumerate(qs)], 1)
    util = CHOICE_W * t + rng.normal(0, 0.7, (n, 3)) - np.array([LOOK[q] for q in qs])
    infr = rng.random(n) < (INFRINGE[0] + INFRINGE[1] * (a < -0.5))
    absent = rng.random(n) < 0.022
    order = np.argsort(-util, 1)
    for i, x in enumerate(cands):
        x["a"], x["t"] = float(a[i]), [float(v) for v in t[i]]
        x["section_a"] = int(sec_a[i])
        x["absent"] = bool(absent[i])
        x["infringer"] = bool(infr[i]) and not absent[i]
        chosen = [qs[j] for j in sorted(order[i, :2])] if not x["infringer"] else list(qs)
        if absent[i]:
            chosen = []
        marks = {}
        for j, q in enumerate(qs):
            if q in chosen:
                m = raw[i, j] - (TIME_COST if x["infringer"] else 0.0)
                marks[q] = int(min(25, max(0, round(m))))
        x["marks"] = marks
    # senior examiners re-mark a sample of essays (their mark stands), and a few scripts carry a clerical correction
    for x in cands:
        x["senior"] = {}
        for q in x["marks"]:
            if rng.random() < 0.045:
                d = int(rng.choice([-2, -1, -1, 1, 1, 2]))
                x["senior"][q] = int(min(25, max(0, x["marks"][q] + d)))
    # candidates who moved centre after entry: re-entered at the new centre under a new number; the old entry is
    # withdrawn and every script is under the new number
    moved = []
    idx = rng.choice(n, 160, replace=False)
    for i in sorted(idx):
        x = cands[i]
        serial += int(rng.integers(1, 4))
        other = centres[int(rng.integers(0, len(centres)))]
        x["prev_no"], x["prev_centre"] = x["no"], x["centre"]
        x["no"] = "26-%06d" % (500000 + serial % 99000)
        x["centre"], x["region"] = other["code"], other["region"]
        moved.append(x["no"])
    markers = []
    for k, (team, tz, off) in enumerate([("Darwin", "Australia/Darwin", 9.5), ("Brisbane", "Australia/Brisbane", 10.0),
                                         ("Perth", "Australia/Perth", 8.0)]):
        for j in range(22):
            markers.append(dict(id="HX%03d" % (100 + k * 30 + j), team=team, tz=tz, offset=off,
                                senior=j < 3))
    return dict(centres=centres, cands=cands, markers=markers, rng=rng)


def reviews_2025(W, seed=SEED + 25):
    """The 2025 post-results reviews: requests made between results day (12 December 2025) and the close on
    27 February 2026, one row per component reviewed, stamped in UTC by the review system."""
    rng = np.random.default_rng(seed)
    cents = W["centres"]
    rows = []
    start = dt.datetime(2025, 12, 12, 0, 0)
    req = 880000
    for k in range(1430):
        c = cents[int(rng.integers(0, len(cents)))]
        # requests cluster in the first fortnight and again after the new year
        u = rng.random()
        if u < 0.55:
            day = rng.exponential(5.0)
        elif u < 0.85:
            day = 20 + rng.exponential(9.0)
        else:
            day = 45 + rng.random() * 32
        day = min(day, 76.9)
        local = start + dt.timedelta(days=float(day), hours=float(8 + rng.random() * 15))
        # a cluster of late-evening requests on the last days of December and January
        if k % 41 == 0:
            local = dt.datetime(2026, 2, 1, 8, 0) + dt.timedelta(minutes=float(rng.integers(0, 180)))
        if k % 53 == 0:
            local = dt.datetime(2026, 1, 1, 7, 30) + dt.timedelta(minutes=float(rng.integers(0, 200)))
        utc = local - dt.timedelta(hours=c["offset"])
        req += int(rng.integers(1, 6))
        comps = ["P2"] if rng.random() < 0.52 else (["P1"] if rng.random() < 0.6 else ["P1", "P2"])
        if rng.random() < 0.08:
            comps = comps + ["IA"]
        cand = "25-%06d" % int(rng.integers(100000, 190000))
        for comp in comps:
            outc = rng.choice(["NC", "MC", "GC"], p=[0.62, 0.27, 0.11])
            rows.append(dict(request=req, candidate=cand, centre=c["code"], component=comp, utc=utc,
                             outcome=str(outc), local=local, region=c["region"]))
        if rng.random() < 0.04:   # withdrawn by the centre before the review began
            for r in rows[-len(comps):]:
                r["outcome"] = "WD"
    return rows
