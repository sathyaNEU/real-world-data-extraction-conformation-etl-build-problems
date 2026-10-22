"""The truth behind task482's pack: the Brackett Plains Community College System's Quantitative Placement Inventory
(QPI), its item bank, its 2026 testing year on two delivery platforms, and Form 27A. Nothing outside the generator
reads this module except pack.py (which writes the files from it) and checks.py (which compares the cut pack with it).

The response model is Rasch with a linear position term: a student of ability theta answers an item of position-free
difficulty a, presented at position p, correctly with probability 1 / (1 + exp(-(theta - a - GAMMA p))). A bank
difficulty is the difficulty the item showed where it was calibrated: the anchor block in place (positions 1 to 20),
the field-tested items in the old platform's field-test section (positions 61 to 70, reversed on version B, so a
mean position of 65.5)."""
import datetime as dt

import numpy as np

SEED = 4826
GAMMA = 0.0075                      # logits per position
FT_MEAN_POS = 65.5                 # old platform field-test section, versions A and B
UNIQUE_FT_SLOTS = list(range(21, 71))   # new platform: unique and field-test items shuffled together
STANDARDS = {"CA": 0.20, "CCA": -0.70}  # 2022 standard setting, bank scale (logits)
BU0, BU1 = 500.0, 100.0            # bank units: 500 + 100 x logit
PRACTICE = 0.12                    # a second sitting's gain
LEVELS = ("CA", "CCA", "DM")

SYSTEM = "Brackett Plains Community College System"
OFFICE = "Office of Assessment and Placement"
BOARD = "State Board of Community Colleges"
TEST = "Quantitative Placement Inventory"
OLD_PLATFORM = "Kestrel Testing Suite"
NEW_PLATFORM = "Northgate Assess"
BANK_SYSTEM = "Itemstore"
PEOPLE = {"director": "Breanna Graham", "psychometrician": "John Huang"}

# code, name, students in the 2026 testing year, ability mean, satellite centre
COLLEGES = [
    ("01", "Ashgrove Community College", 1150, -0.18, True),
    ("02", "Bramblewood Community College", 980, -0.30, True),
    ("03", "Calder Flats Community College", 870, -0.42, False),
    ("04", "Dellwood Community College", 820, -0.12, True),
    ("05", "Embervale Community College", 760, -0.36, False),
    ("06", "Fennimore Ridge Community College", 700, -0.24, True),
    ("07", "Gorseway Community College", 640, -0.48, False),
    ("08", "Hartmoor Creek Community College", 600, -0.20, False),
    ("09", "Iverton Prairie Community College", 560, -0.33, True),
    ("10", "Juniper Lake Community College", 520, -0.27, False),
    ("11", "Knollwood Community College", 470, -0.40, False),
    ("12", "Lowland Mesa Community College", 380, -0.15, True),
    ("13", "Marlow Fork Community College", 310, -0.52, False),
    ("14", "Nettlefield Community College", 240, -0.22, False),
]
CODES = [c[0] for c in COLLEGES]
NAMES = {c[0]: c[1] for c in COLLEGES}
STRANDS = ("NS", "AE", "LE", "FG", "QR")
STRAND_NAMES = {"NS": "Number sense and operations", "AE": "Algebraic expressions", "LE": "Linear equations and "
                "inequalities", "FG": "Functions and graphs", "QR": "Quantitative reasoning"}

YEAR_START = dt.date(2026, 3, 1)
CUTOVER = dt.date(2026, 7, 1)
REKEY = dt.date(2026, 10, 1)
EXTRACT_END = dt.date(2027, 1, 31)
# share of first sittings by month, March 2026 to January 2027
MONTHS = [(2026, 3, .07), (2026, 4, .09), (2026, 5, .11), (2026, 6, .09), (2026, 7, .12), (2026, 8, .15),
          (2026, 9, .06), (2026, 10, .06), (2026, 11, .08), (2026, 12, .09), (2027, 1, .08)]
# local time is US Central; the new platform stamps UTC
UTC_OFFSET_CDT, UTC_OFFSET_CST = 5, 6
SESSION_STARTS = [(9, 0), (13, 0), (17, 30)]


def central_offset(d):
    """Hours behind UTC on date d (US Central: daylight time from the second Sunday of March to the first Sunday of
    November)."""
    y = d.year
    m3 = dt.date(y, 3, 8)
    dst_start = m3 + dt.timedelta(days=(6 - m3.weekday()) % 7)
    n1 = dt.date(y, 11, 1)
    dst_end = n1 + dt.timedelta(days=(6 - n1.weekday()) % 7)
    return UTC_OFFSET_CDT if dst_start <= d < dst_end else UTC_OFFSET_CST


def P(theta, d):
    return 1.0 / (1.0 + np.exp(-(theta - d)))


def _items(rng, pool_seed=None):
    """Every item the year touches, with its position-free difficulty and its bank record where it has one. The ready
    pool's calibration error comes from its own stream, so the 2026 year is the same whatever it draws."""
    rng_pool = np.random.default_rng(20000 + (POOL_SEED if pool_seed is None else pool_seed))
    items = {}

    def add(iid, legacy, strand, a, role, **kw):
        items[iid] = dict(id=iid, legacy=legacy, strand=strand, a=float(a), role=role, **kw)

    # anchor block: calibrated in place in the 2022 base calibration, kept in positions 1 to 20 on every form
    anchor_strands = [s for s in STRANDS for _ in range(4)]
    aA = rng.normal(-0.30, 0.75, 20)
    for k in range(20):
        num = 101 + k * 7
        add("QPI-%s-%04d" % (anchor_strands[k], num), "%s%03d" % (anchor_strands[k], num), anchor_strands[k], aA[k],
            "anchor", anchor_pos=k + 1)
    # the ready pool: field-tested on the old platform in 2023 to 2025 (field-test section, mean position 65.5)
    serial = 400
    for year, count in ((2023, 50), (2024, 55), (2025, 55)):
        for k in range(count):
            s = STRANDS[(serial + k) % 5]
            serial += 1
            add("QPI-%s-%04d" % (s, serial), "%s%03d" % (s, serial % 1000) if year < 2025 else "", s,
                rng.normal(0.20, 0.85), "pool", ft_year=year)
    # Form 26A and 26B unique items (retired with the forms) and the 2026 field-test sets
    for form in ("26A", "26B"):
        for k in range(40):
            s = STRANDS[k % 5]
            serial += 1
            add("QPI-%s-%04d" % (s, serial), "%s%03d" % (s, serial % 1000), s, rng.normal(0.15, 0.80), "unique",
                form=form, slot=k + 1)
    for st in range(8):
        for k in range(10):
            s = STRANDS[(st + k) % 5]
            serial += 1
            add("QPI-%s-%04d" % (s, serial), "%s%03d" % (s, serial % 1000), s, rng.normal(0.25, 0.90), "ft2026",
                ft_set=st + 1, slot=k + 1)
    # keys
    for it in sorted(items):
        items[it]["key"] = "ABCD"[int(rng.integers(4))]
    # bank records: anchors in place, pool items at the field-test section's mean position
    for it in sorted(items):
        r = items[it]
        if r["role"] == "anchor":
            n = int(rng.integers(5600, 6400))
            se = 1.0 / np.sqrt(n * 0.21)
            r.update(n=n, se=se, bank=r["a"] + GAMMA * r["anchor_pos"] + rng.normal(0, se))
        elif r["role"] in ("pool", "unique"):
            n = int(rng.integers(540, 900))
            se = 1.0 / np.sqrt(n * 0.21)
            noise = rng.normal(0, se)
            if r["role"] == "pool":
                noise = rng_pool.normal(0, se)
            r.update(n=n, se=se, bank=r["a"] + GAMMA * FT_MEAN_POS + noise)
    return items


def _assemble(items, rng):
    """Forms 27A and 27B from the ready pool: eight items a strand each, spread over the pool's difficulty."""
    pool = [items[i] for i in sorted(items) if items[i]["role"] == "pool"]
    forms = {}
    taken = set()
    for form in ("27A", "27B"):
        chosen = []
        for s in STRANDS:
            cand = sorted([r for r in pool if r["strand"] == s and r["id"] not in taken], key=lambda r: r["bank"])
            idx = np.linspace(1, len(cand) - 2, 8).round().astype(int)
            if form == "27B":
                idx = np.clip(idx + 1, 0, len(cand) - 1)
            pick = [cand[i] for i in idx]
            chosen += pick
            taken.update(p["id"] for p in pick)
        order = rng.permutation(len(chosen))
        forms[form] = [chosen[i]["id"] for i in order]
    return forms


def _students(rng):
    studs = []
    sid = 0
    for code, name, n, mu, _ in COLLEGES:
        for k in range(n):
            sid += 1
            age = 17 + int(rng.gamma(1.3, 2.4)) if rng.random() < 0.80 else int(rng.integers(24, 58))
            age = min(age, 61)
            dob = dt.date(2026 - age, 1, 1) + dt.timedelta(days=int(rng.integers(0, 365)))
            studs.append(dict(k=sid, college=code, theta=float(rng.normal(mu, 1.0)), dob=dob,
                              sex="F" if rng.random() < 0.56 else "M"))
    return studs


def _month_day(rng, after=None):
    while True:
        m = MONTHS[int(rng.choice(len(MONTHS), p=np.array([w for *_, w in MONTHS]) / sum(w for *_, w in MONTHS)))]
        d = dt.date(m[0], m[1], 1) + dt.timedelta(days=int(rng.integers(0, 31)))
        if d.month != m[1] or d > EXTRACT_END:
            continue
        if d.weekday() == 6 or (d.weekday() == 5 and rng.random() < 0.7):
            continue
        if after is None or d > after:
            return d


def _weekday_after(d, rng, lo, hi):
    for _ in range(200):
        e = d + dt.timedelta(days=int(rng.integers(lo, hi)))
        if e.weekday() < 5:
            return e
    return None


def form_items(items, form):
    """Form 26A or 26B's scored items (anchors in place, then the unique items by slot) and the 2026 field-test sets."""
    anchors = sorted([i for i in items.values() if i["role"] == "anchor"], key=lambda r: r["anchor_pos"])
    unique = sorted([i for i in items.values() if i["role"] == "unique" and i["form"] == form], key=lambda r: r["slot"])
    return [r["id"] for r in anchors], [r["id"] for r in unique]


def ft_set_items(items, st):
    return [r["id"] for r in sorted([i for i in items.values() if i["role"] == "ft2026" and i["ft_set"] == st],
                                    key=lambda r: r["slot"])]


def bank_expected(items, ids, theta):
    return float(sum(P(theta, items[i]["bank"]) for i in ids))


def program_scores(items, form):
    """The programme's own 2026 placement scores for a form: the lowest whole raw score at or above the bank
    curve at each standard (the bank difficulties as filed)."""
    anc, uni = form_items(items, form)
    return {lv: int(np.ceil(bank_expected(items, anc + uni, STANDARDS[lv]) - 1e-9)) for lv in ("CA", "CCA")}


def level_of(raw, scores):
    return "CA" if raw >= scores["CA"] else ("CCA" if raw >= scores["CCA"] else "DM")


def _positions(platform, version, rng):
    """Delivered positions of the 40 unique slots and the 10 field-test slots."""
    if platform == "old":
        u = np.arange(21, 61) if version == "A" else np.arange(60, 20, -1)
        f = np.arange(61, 71) if version == "A" else np.arange(70, 60, -1)
        return u, f
    perm = rng.permutation(np.arange(21, 71))
    return perm[:40], perm[40:]


def _centres():
    out = []
    for code, name, _, _, sat in COLLEGES:
        out.append(("TC%s1" % code, code, "main"))
        if sat:
            out.append(("TC%s2" % code, code, "satellite"))
    return out


SWITCH_SEED = 68
POOL_SEED = 29
FEEDER = [0.30, 0.22, 0.16, 0.13, 0.11, 0.08]
SIZES = {c[0]: c[2] for c in COLLEGES}


def everything(switch_seed=None):
    rng = np.random.default_rng(SEED)
    rng_sw = np.random.default_rng(10000 + (SWITCH_SEED if switch_seed is None else switch_seed))
    items = _items(rng)
    forms = _assemble(items, rng)
    studs = _students(rng)
    scores26 = {f: program_scores(items, f) for f in ("26A", "26B")}
    centres = _centres()
    by_college = {}
    for c in centres:
        by_college.setdefault(c[1], []).append(c[0])
    # identity: each college's student system issues 7-digit numbers from its own counter (the counters overlap)
    csn_next = {code: 1000000 + int(rng.integers(0, 600000)) for code in CODES}
    used_sys, used_ss = set(), set()

    def new_id(pool):
        while True:
            v = int(rng.integers(100000000, 999999999))
            if v not in used_sys and v not in used_ss:
                pool.add(v)
                return v

    hs_codes = {code: sorted(int(x) for x in rng.choice(np.arange(140000, 149999), 15, replace=False)) for code in CODES}
    attempts = []
    seen4 = set()
    for s in studs:
        code = s["college"]
        first = _month_day(rng)
        s["registered"] = first - dt.timedelta(days=int(rng.integers(3, 160)))
        s["_first"] = first
        # most entrants come from a handful of feeder high schools in the college's district
        u = rng.random()
        if u < 0.10:
            s["hs"] = "GED"
        elif u < 0.80:
            s["hs"] = str(hs_codes[code][int(rng.choice(6, p=FEEDER))])
        elif u < 0.92:
            s["hs"] = str(hs_codes[code][6 + int(rng.integers(9))])
        else:
            s["hs"] = str(int(rng.integers(100000, 999999)))
        while (s["dob"], s["sex"], s["hs"], s["registered"]) in seen4:
            s["registered"] -= dt.timedelta(days=1)
        seen4.add((s["dob"], s["sex"], s["hs"], s["registered"]))
        s["csn"] = None
        s["first"] = first
        # registering college history: a student may move their registration to another college, most often in
        # the weeks after a summer sitting, and most often towards the larger colleges
        s["switch"] = None
        p_sw = 0.13 if CUTOVER <= first < REKEY else (0.07 if first >= REKEY else 0.04)
        if rng_sw.random() < p_sw:
            d = first + dt.timedelta(days=int(rng_sw.integers(10, 76)))
            other = [c for c in CODES if c != code]
            w = np.array([SIZES[c] ** 1.5 for c in other])
            to = other[int(rng_sw.choice(len(other), p=w / w.sum()))]
            if d <= EXTRACT_END:
                s["switch"] = (d, to)
        s["attempts"] = []
    # first sittings, then retests
    def college_on(s, d):
        if s["switch"] and d >= s["switch"][0]:
            return s["switch"][1]
        return s["college"]

    def sit(s, d, form, retest):
        platform = "old" if d < CUTOVER else "new"
        reg = college_on(s, d)
        if platform == "old":
            centre = by_college[reg][0] if len(by_college[reg]) == 1 or rng.random() < 0.7 else by_college[reg][1]
        else:
            if rng.random() < 0.88:
                centre = by_college[reg][int(rng.integers(len(by_college[reg])))]
            else:
                oc = [c for c in CODES if c != reg]
                centre = by_college[oc[int(rng.integers(len(oc)))]][0]
        slot = SESSION_STARTS[int(rng.choice(3, p=[0.45, 0.4, 0.15]))]
        start = dt.datetime(d.year, d.month, d.day, slot[0], slot[1]) + dt.timedelta(minutes=int(rng.integers(0, 9)))
        version = "AB"[int(rng.integers(2))] if platform == "old" else ""
        ft = int(rng.integers(1, 9))
        anc, uni = form_items(items, form)
        fts = ft_set_items(items, ft)
        upos, fpos = _positions(platform, version, rng)
        ids = anc + uni + fts
        pos = np.r_[np.arange(1, 21), upos, fpos]
        a = np.array([items[i]["a"] for i in ids])
        th = s["theta"] + (PRACTICE if retest else 0.0)
        y = (rng.random(70) < P(th, a + GAMMA * pos)).astype(int)
        omit = rng.random(70) < 0.008
        y[omit] = 0
        raw = int(y[:60].sum())
        dur = int(rng.integers(68, 132))
        at = dict(student=s["k"], date=d, start=start, end=start + dt.timedelta(minutes=dur), platform=platform,
                  form=form, version=version, ft_set=ft, centre=centre, reg=reg, items=ids, pos=pos.tolist(),
                  y=y.tolist(), omit=omit.tolist(), raw=raw, level=level_of(raw, scores26[form]), retest=retest,
                  letters=[])
        for i, iid in enumerate(ids):
            key = items[iid]["key"]
            if omit[i]:
                at["letters"].append("")
            elif y[i]:
                at["letters"].append(key)
            else:
                at["letters"].append([c for c in "ABCD" if c != key][int(rng.integers(3))])
        s["attempts"].append(at)
        attempts.append(at)
        return at

    for s in studs:
        a1 = sit(s, s["first"], "26A", False)
        sc = scores26["26A"]
        near = any(0 < sc[lv] - a1["raw"] <= 3 for lv in ("CA", "CCA"))
        p = 0.40 if near else (0.08 if a1["level"] != "CA" else 0.015)
        if rng.random() < p:
            d2 = _weekday_after(s["first"], rng, 14, 150)
            if d2 and d2 <= EXTRACT_END:
                sit(s, d2, "26B", True)
    attempts.sort(key=lambda r: (r["start"], r["student"]))
    # identities: legacy numbers for students who sat on the old platform, system ids at the cutover or on first
    # registering with the new platform, state ids from 1 October for every attempt from then on
    for s in sorted(studs, key=lambda r: (r["first"], r["k"])):
        olds = [a for a in s["attempts"] if a["platform"] == "old"]
        s["csn"] = {}
        for a in olds:
            c = a["reg"]
            if c not in s["csn"]:
                s["csn"][c] = csn_next[c]
                csn_next[c] += int(rng.integers(1, 4))
        s["sysid"] = new_id(used_sys) if (olds or any(a["date"] < REKEY for a in s["attempts"])) else None
        s["ssid"] = new_id(used_ss) if any(a["date"] >= REKEY for a in s["attempts"]) else None
        for a in s["attempts"]:
            if a["platform"] == "old":
                a["sid"] = s["csn"][a["reg"]]
                a["site"] = a["reg"]
            else:
                a["sid"] = s["sysid"] if a["date"] < REKEY else s["ssid"]
            # the new platform's college column: the student profile as now held (the system-id profile froze
            # on 30 September when the state ids replaced it)
            if a["platform"] == "new":
                held_on = REKEY - dt.timedelta(days=1) if a["date"] < REKEY else EXTRACT_END
                a["college_held"] = college_on(s, held_on)
    # score reports: the automatic report to the college the student was registered through when they sat;
    # a student who moves registration asks for earlier scores to be sent to the new college
    reports = []
    for s in studs:
        for a in s["attempts"]:
            reports.append(dict(attempt=a, to=a["reg"], kind="automatic", sent=a["end"] + dt.timedelta(minutes=2)))
        if s["switch"]:
            d, to = s["switch"]
            for a in s["attempts"]:
                if a["date"] < d:
                    t = dt.datetime(d.year, d.month, d.day, 10, 0) + dt.timedelta(minutes=int(rng.integers(0, 400)))
                    reports.append(dict(attempt=a, to=to, kind="requested", sent=t))
        elif rng.random() < 0.03 and s["attempts"]:
            a = s["attempts"][0]
            to = [c for c in CODES if c != a["reg"]][int(rng.integers(13))]
            sent = a["end"] + dt.timedelta(days=int(rng.integers(2, 40)))
            if sent.date() <= EXTRACT_END:
                reports.append(dict(attempt=a, to=to, kind="requested", sent=sent))
    # sessions and irregularities
    sessions = {}
    for a in attempts:
        key = (a["centre"], a["date"], a["start"].replace(minute=0 if a["start"].hour != 17 else 30).strftime("%H:%M"))
        sessions.setdefault(key, []).append(a)
    for i, key in enumerate(sorted(sessions)):
        for a in sessions[key]:
            a["session"] = key
    cand = sorted([k for k, v in sessions.items() if len(v) >= 5])
    pick = [cand[int(i)] for i in rng.choice(len(cand), 10, replace=False)]
    pick.sort()
    irregular = []
    for j, key in enumerate(pick):
        reinstated = j in (2, 5, 8)
        irregular.append(dict(session=key, reinstated=reinstated))
        for a in sessions[key]:
            a["invalid"] = not reinstated
    for a in attempts:
        a.setdefault("invalid", False)
    e = dict(items=items, forms=forms, students=studs, attempts=attempts, reports=reports, sessions=sessions,
             irregular=irregular, scores26=scores26, centres=centres, hs_codes=hs_codes)
    return e


if __name__ == "__main__":
    e = everything()
    print(len(e["items"]), {k: len(v) for k, v in e["forms"].items()}, len(e["students"]), len(e["attempts"]))
    print("2026 scores", e["scores26"])
