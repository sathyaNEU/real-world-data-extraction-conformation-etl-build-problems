"""task306 architecture 5: the clean truth of Marches Primary Care Collaborative's world.

A GP federation's member practices in five primary care networks, their registered patients and registration
spells, the medicine courses the three candidate deprescribing reviews look at (each with who started it: the
practice, or a specialist service whose letter came first), the two trusts' medicine letters feed and the practices'
document workflow, the 2026 pilot in the Clun Valley network, and the pharmacist team's 2026 consultations in the hub
booking system, the practices' clinical systems and the group session register. Everything downstream (the pack, the
golden, the checks) is computed forward from what is drawn here; nothing is fitted to a target.
"""
import datetime as dt
import hashlib

import numpy as np
import pandas as pd

SEED = 3065
EPOCH = dt.date(1970, 1, 1)
AS_OF = dt.date(2026, 12, 31)
PULL = dt.date(2027, 1, 6)
FEED_OPEN = dt.date(2019, 10, 1)
COURSE_FLOOR = dt.date(2019, 11, 15)
REG_START = dt.date(2020, 1, 1)
MERGE_DATE = dt.date(2025, 4, 1)
PILOT_START = dt.date(2026, 1, 12)
PILOT_END = dt.date(2026, 6, 26)
WIN0, WIN1 = dt.date(2026, 7, 1), dt.date(2026, 12, 31)
OFF_DAYS = 183
MMH_SWITCH = dt.date(2026, 4, 7)
RESEND_FROM, RESEND_TO = dt.date(2026, 3, 9), dt.date(2026, 3, 30)
GPCONNECT = dt.date(2026, 10, 1)
BANK_HOLIDAYS = {dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1), dt.date(2026, 4, 3),
                 dt.date(2026, 4, 6), dt.date(2026, 5, 4), dt.date(2026, 5, 25), dt.date(2026, 8, 31),
                 dt.date(2026, 12, 25), dt.date(2026, 12, 28), dt.date(2027, 1, 1)}


def rng(tag):
    h = int(hashlib.sha256(("task306v5:%d:%s" % (SEED, tag)).encode()).hexdigest()[:16], 16)
    return np.random.default_rng(h)


def di(d):
    return (d - EPOCH).days


def dd(i):
    return EPOCH + dt.timedelta(days=int(i))


def working(d):
    return d.weekday() < 5 and d not in BANK_HOLIDAYS


def next_working(d):
    d = d + dt.timedelta(days=1)
    while not working(d):
        d = d + dt.timedelta(days=1)
    return d


# --------------------------------------------------------------------------------------------------------------------
# Networks and practices
# --------------------------------------------------------------------------------------------------------------------
PCNS = [("CV", "Clun Valley PCN"), ("WC", "Wrekinside Central PCN"), ("WN", "Wrekinside North PCN"),
        ("TV", "Teme Valley PCN"), ("SG", "Severn Gorge PCN")]
PCN_NAME = dict(PCNS)

# (ODS code, name, network, list size at 1 January 2020, share aged 65 and over, merged into)
PRACTICES = [
    ("M83614", "Clunford Medical Practice", "CV", 8940, 0.31, None),
    ("M85207", "Bettws Lane Surgery", "CV", 7615, 0.33, None),
    ("M81953", "Kerryhill Practice", "CV", 6933, 0.30, None),
    ("M86740", "Hopwas Cross Health Centre", "CV", 6210, 0.32, None),
    ("M82488", "Bishopsmoor Surgery", "CV", 5078, 0.34, None),
    ("M87125", "Martonbrook Surgery", "CV", 4419, 0.29, None),
    ("M84392", "Quarrygate Medical Group", "WC", 12502, 0.17, None),
    ("M80571", "Abbeymead Surgery", "WC", 11107, 0.19, None),
    ("M88216", "Weirbank Practice", "WC", 9010, 0.16, None),
    ("M83057", "Ashcote Health Centre", "WC", 8301, 0.21, None),
    ("M86613", "Kingsweir Surgery", "WC", 6883, 0.18, None),
    ("M81409", "Fennel Street Medical Practice", "WC", 5003, 0.22, None),
    ("M89034", "Wylecroft Surgery", "WC", 4096, 0.20, "M83057"),
    ("M85826", "Rodenmere Practice", "WN", 9446, 0.20, None),
    ("M82769", "Halcott Way Surgery", "WN", 7794, 0.22, None),
    ("M87342", "Elmscote Medical Centre", "WN", 7088, 0.24, None),
    ("M80915", "Hollins Rise Health Centre", "WN", 6179, 0.19, None),
    ("M84468", "Wemcott and Brannock Surgery", "WN", 5630, 0.26, None),
    ("M86197", "Hollybush Lane Surgery", "WN", 4544, 0.23, None),
    ("M88653", "Corrindale Medical Practice", "TV", 9323, 0.27, None),
    ("M81286", "Ashenford Road Surgery", "TV", 7376, 0.29, None),
    ("M83941", "Pellowdale Health Centre", "TV", 6552, 0.26, None),
    ("M85574", "Millbrook Mead Practice", "TV", 5589, 0.30, None),
    ("M87809", "The Coldbrook Surgery", "TV", 4860, 0.28, None),
    ("M80338", "Severnwick Surgery", "TV", 3122, 0.31, "M85574"),
    ("M82137", "Wharfside Medical Centre", "SG", 8848, 0.23, None),
    ("M86054", "Kilnworks Road Surgery", "SG", 7534, 0.25, None),
    ("M84721", "Furnace Lane Health Centre", "SG", 6648, 0.27, None),
    ("M89462", "Tilecroft Practice", "SG", 5763, 0.24, None),
    ("M83388", "Rushmere Court Surgery", "SG", 4830, 0.22, None),
]
CODES = [p[0] for p in PRACTICES]
PRACTICE = {p[0]: dict(code=p[0], name=p[1], pcn=p[2], list0=p[3], old=p[4], merged_into=p[5]) for p in PRACTICES}
PCN_OF = {p[0]: p[2] for p in PRACTICES}
MERGED = {p[0]: p[5] for p in PRACTICES if p[5]}
POSTCODE = {"CV": "SY7", "WC": "SY1", "WN": "SY4", "TV": "SY8", "SG": "TF8"}
# practices whose clinical system the hub pharmacists write into (the others receive a hub summary document)
SHARED_RECORD = {"M83614", "M85207", "M86740", "M84392", "M88216", "M83057", "M81409", "M85826", "M87342",
                 "M84468", "M88653", "M83941", "M85574", "M82137", "M84721", "M83388"}


def survivor(code, d):
    if code in MERGED and d >= MERGE_DATE:
        return MERGED[code]
    return code


def age_on(birth_year, birth_month, d):
    return d.year - birth_year - (1 if d.month < birth_month else 0)


def age_band(age):
    if age < 65:
        return "18 to 64"
    if age < 75:
        return "65 to 74"
    if age < 85:
        return "75 to 84"
    return "85 and over"


# --------------------------------------------------------------------------------------------------------------------
# Patients and registration spells
# --------------------------------------------------------------------------------------------------------------------
class World:
    pass


def population(T):
    """Registered patients from before 1 January 2020 to the pull: deaths, moves out of the federation, moves
    between member practices and new registrations each year, then the two April 2025 mergers."""
    r = rng("population")
    np_ = len(CODES)
    n0 = np.array([PRACTICE[c]["list0"] for c in CODES])
    old = np.array([PRACTICE[c]["old"] for c in CODES])
    by, bm, sex, death, cur = [], [], [], [], []
    sp_pat, sp_prac, sp_start, sp_end, sp_reason = [], [], [], [], []

    def add_patients(prac_idx, at_int, newborn_mask, start_ints):
        n = len(prac_idx)
        is_old = r.random(n) < old[prac_idx]
        age = np.where(is_old, 65 + (40 * r.beta(1.1, 3.2, n)).astype(int), r.integers(0, 65, n))
        year = np.array([dd(a).year for a in at_int])
        b_y = np.where(newborn_mask, year - (r.random(n) < 0.3).astype(int), year - age - 1)
        b_m = r.integers(1, 13, n)
        sx = np.where(r.random(n) < 0.508, "F", "M")
        base = len(by)
        by.extend(b_y.tolist()); bm.extend(b_m.tolist()); sex.extend(sx.tolist())
        death.extend([None] * n)
        for k in range(n):
            st = int(start_ints[k])
            born = di(dt.date(int(b_y[k]), int(b_m[k]), 15))
            st = max(st, born)
            sp_pat.append(base + k); sp_prac.append(int(prac_idx[k])); sp_start.append(st)
            sp_end.append(-1); sp_reason.append("")
            cur.append(len(sp_pat) - 1)

    prac0 = np.repeat(np.arange(np_), n0)
    starts0 = di(REG_START) - r.integers(30, 12000, len(prac0))
    add_patients(prac0, np.full(len(prac0), di(REG_START)), np.zeros(len(prac0), bool), starts0)

    pcn_idx = np.array(["CV WC WN TV SG".split().index(PCN_OF[c]) for c in CODES])
    for year in range(2020, 2027):
        y0 = di(dt.date(year, 1, 1))
        span = 364 if year == 2026 else (366 if year % 4 == 0 else 365)
        curarr = np.array(cur)
        live = np.where(curarr >= 0)[0]
        ages = year - np.array(by)[live]
        pdie = np.where(ages < 65, 0.003, np.where(ages < 80, 0.018, 0.075))
        u = r.random(len(live))
        when = y0 + r.integers(0, span, len(live))
        die = u < pdie
        out = (u >= pdie) & (u < pdie + 0.021)
        move = (u >= pdie + 0.021) & (u < pdie + 0.021 + 0.025)
        for k in np.where(die)[0]:
            p = int(live[k]); s = cur[p]
            sp_end[s] = int(when[k]); sp_reason[s] = "Deceased"; death[p] = int(when[k]); cur[p] = -1
        for k in np.where(out)[0]:
            p = int(live[k]); s = cur[p]
            sp_end[s] = int(when[k]); sp_reason[s] = "Transferred out of the federation"; cur[p] = -1
        mv = np.where(move)[0]
        same = r.random(len(mv)) < 0.45
        pick = r.integers(0, 10 ** 6, len(mv))
        for j, k in enumerate(mv):
            p = int(live[k]); s = cur[p]
            src = sp_prac[s]
            d_ = dd(when[k])
            live_codes = [i for i in range(np_) if not (CODES[i] in MERGED and d_ >= MERGE_DATE)]
            src_surv = CODES.index(survivor(CODES[src], d_))
            pool = [i for i in live_codes if i != src_surv and i != src]
            if same[j]:
                sp = [i for i in pool if pcn_idx[i] == pcn_idx[src]]
                pool = sp or pool
            tgt = pool[pick[j] % len(pool)]
            if sp_start[s] >= int(when[k]):
                continue
            sp_end[s] = int(when[k]); sp_reason[s] = "Transferred to a member practice"
            sp_pat.append(p); sp_prac.append(tgt); sp_start.append(int(when[k])); sp_end.append(-1)
            sp_reason.append(""); cur[p] = len(sp_pat) - 1
        for i in range(np_):
            c = CODES[i]
            n_new = int(r.poisson(n0[i] * 0.045))
            at = y0 + r.integers(0, span, n_new)
            if c in MERGED:
                at = at[at < di(MERGE_DATE)]
            if not len(at):
                continue
            nb = r.random(len(at)) < 0.22
            add_patients(np.full(len(at), i), at, nb, at)
    S = pd.DataFrame({"p": sp_pat, "prac": [CODES[i] for i in sp_prac], "start": sp_start, "end": sp_end,
                      "reason": sp_reason})
    # the April 2025 mergers: spells open at a merged practice continue at the survivor
    m = di(MERGE_DATE)
    rows = []
    for rec in S.itertuples(index=False):
        if rec.prac in MERGED and rec.start < m and (rec.end == -1 or rec.end > m):
            rows.append((rec.p, rec.prac, rec.start, m, "Practice merger"))
            rows.append((rec.p, MERGED[rec.prac], m, rec.end, rec.reason))
        elif rec.prac in MERGED and rec.start >= m:
            rows.append((rec.p, MERGED[rec.prac], rec.start, rec.end, rec.reason))
        else:
            rows.append(tuple(rec))
    S = pd.DataFrame(rows, columns=["p", "prac", "start", "end", "reason"]).sort_values(["p", "start", "end"])
    # a transfer between a merged practice and its survivor after the merger is no move at all
    keep, prev = [], None
    for rec in S.itertuples(index=False):
        if prev is not None and prev[0] == rec.p and prev[1] == rec.prac and prev[3] == rec.start \
                and prev[4] == "Transferred to a member practice":
            prev = (prev[0], prev[1], prev[2], rec.end, rec.reason)
            keep[-1] = prev
            continue
        prev = tuple(rec)
        keep.append(prev)
    S = pd.DataFrame(keep, columns=["p", "prac", "start", "end", "reason"]).reset_index(drop=True)
    r2 = rng("pseudonyms")
    pids = set()
    plist = []
    while len(plist) < len(by):
        x = "".join(r2.choice(list("0123456789ABCDEF"), 10))
        if x not in pids and not x.isdigit():
            pids.add(x)
            plist.append(x)
    T.P = pd.DataFrame({"pid": plist, "birth_year": by, "birth_month": bm, "sex": sex,
                        "death": [d if d is not None else -1 for d in death]})
    S["pid"] = T.P["pid"].values[S["p"].values]
    T.S = S
    T.pid_index = {p: i for i, p in enumerate(plist)}
    sp = {}
    for rec in S.itertuples(index=False):
        sp.setdefault(int(rec.p), []).append((int(rec.start), int(rec.end), rec.prac, rec.reason))
    for v in sp.values():
        v.sort()
    T.spells_by_p = sp


def registered_on(T, d):
    """Patient index -> survivor practice code for spells covering d (start <= d < end)."""
    x = di(d)
    S = T.S
    m = (S["start"] <= x) & ((S["end"] == -1) | (S["end"] > x))
    sub = S.loc[m, ["p", "prac"]]
    return dict(zip(sub["p"].values, [survivor(c, d) for c in sub["prac"].values]))


def lineage_start(T):
    """For each patient's spell open at the as-of date, the start of the run of spells joined only by a merger."""
    out = {}
    for p, rows in T.spells_by_p.items():
        last = rows[-1]
        if last[1] != -1:
            continue
        st = last[0]
        for i in range(len(rows) - 2, -1, -1):
            if rows[i][3] == "Practice merger" and rows[i][1] == st:
                st = rows[i][0]
            else:
                break
        out[p] = (last[2], st)
    return out


# --------------------------------------------------------------------------------------------------------------------
# The reviews' medicines
# --------------------------------------------------------------------------------------------------------------------
# dm+d virtual medicinal products: (VMP code, name, class, quantity, days per issue)
PRODUCTS = [
    ("39695211000001102", "Risperidone 500microgram tablets", "AP", 56, 28),
    ("39695311000001105", "Risperidone 1mg tablets", "AP", 28, 28),
    ("42019111000001108", "Quetiapine 25mg tablets", "AP", 56, 28),
    ("42019211000001103", "Quetiapine 50mg tablets", "AP", 28, 28),
    ("39108211000001100", "Haloperidol 500microgram tablets", "AP", 28, 28),
    ("41961711000001106", "Olanzapine 2.5mg tablets", "AP", 28, 28),
    ("39732011000001107", "Diazepam 2mg tablets", "BZ", 28, 28),
    ("39732111000001108", "Diazepam 5mg tablets", "BZ", 28, 28),
    ("39710511000001109", "Temazepam 10mg tablets", "BZ", 28, 28),
    ("41967711000001104", "Lorazepam 1mg tablets", "BZ", 28, 28),
    ("42227611000001102", "Zopiclone 3.75mg tablets", "BZ", 28, 28),
    ("42227711000001106", "Zopiclone 7.5mg tablets", "BZ", 28, 28),
    ("39727811000001100", "Zolpidem 5mg tablets", "BZ", 28, 28),
    ("39720211000001108", "Clobazam 10mg tablets", "BZ", 56, 28),
    ("39778911000001102", "Pregabalin 75mg capsules", "GB", 56, 28),
    ("39779011000001109", "Pregabalin 150mg capsules", "GB", 56, 28),
    ("39694111000001100", "Gabapentin 300mg capsules", "GB", 84, 28),
    ("39694211000001106", "Gabapentin 600mg tablets", "GB", 84, 28),
    ("39720911000001103", "Codeine 30mg tablets", "OP", 112, 28),
    ("42098711000001107", "Co-codamol 30mg/500mg tablets", "OP", 100, 25),
    ("39725211000001104", "Tramadol 50mg capsules", "OP", 100, 25),
    ("41976611000001107", "Morphine 10mg modified-release tablets", "OP", 56, 28),
    ("42097311000001103", "Oxycodone 5mg capsules", "OP", 56, 28),
    ("39726111000001103", "Buprenorphine 10micrograms/hour transdermal patches", "OP", 4, 28),
]
PROD = {p[0]: dict(vmp=p[0], name=p[1], cls=p[2], qty=p[3], every=p[4]) for p in PRODUCTS}
REVIEWS = ["AP", "BZ", "GB"]
REVIEW_NAME = {"AP": "Antipsychotics in people aged 65 and over",
               "BZ": "Benzodiazepines and Z-drugs in people aged 65 and over",
               "GB": "Gabapentinoids taken with an opioid"}
REVIEW_SHORT = {"AP": "Antipsychotics", "BZ": "Benzodiazepines and Z-drugs", "GB": "Gabapentinoids with an opioid"}
# product mix within each class, shared by every provenance (products carry no information on who started them)
MIX = {"AP": {"42019111000001108": 0.34, "42019211000001103": 0.12, "39695211000001102": 0.27,
              "39695311000001105": 0.12, "39108211000001100": 0.06, "41961711000001106": 0.09},
       "BZ": {"42227611000001102": 0.22, "42227711000001106": 0.20, "39732011000001107": 0.17,
              "39732111000001108": 0.11, "39710511000001109": 0.14, "41967711000001104": 0.08,
              "39727811000001100": 0.08},
       "GB": {"39778911000001102": 0.30, "39779011000001109": 0.18, "39694111000001100": 0.36,
              "39694211000001106": 0.16},
       "OP": {"39720911000001103": 0.22, "42098711000001107": 0.30, "39725211000001104": 0.20,
              "41976611000001107": 0.10, "42097311000001103": 0.08, "39726111000001103": 0.10}}
BRAND = {"Risperidone": "Risperdal", "Quetiapine": "Seroquel", "Olanzapine": "Zyprexa", "Haloperidol": "Haldol",
         "Pregabalin": "Lyrica", "Gabapentin": "Neurontin", "Zopiclone": "Zimovane", "Zolpidem": "Stilnoct",
         "Diazepam": "Valium", "Lorazepam": "Ativan"}

# serious harms per 100 patient-years of continued use (the programme specification's table)
HARM = {"AP": {"65 to 74": 6.7, "75 to 84": 9.3, "85 and over": 12.2},
        "BZ": {"65 to 74": 2.7, "75 to 84": 4.2, "85 and over": 6.3},
        "GB": {"18 to 64": 1.8, "65 to 74": 2.7, "75 to 84": 3.7, "85 and over": 4.5}}

# eligible-pool prevalence outside the pilot network: per 65-and-over patient (AP, BZ) or per adult (GB)
PREV = {"AP": 0.0150, "BZ": 0.0303, "GB": 0.0125}
# share of the pool started by a specialist service, by network
SPEC_SHARE = {"AP": {"WC": 0.885, "WN": 0.860, "TV": 0.845, "SG": 0.830},
              "BZ": {"WC": 0.075, "WN": 0.060, "TV": 0.050, "SG": 0.055},
              "GB": {"WC": 0.480, "WN": 0.440, "TV": 0.410, "SG": 0.400}}
PILOT_N = {"AP": 160, "BZ": 300, "GB": 240}
PILOT_SPEC = {"AP": 24, "BZ": 24, "GB": 48}
PILOT_SPEC_OFF = {"AP": 1, "BZ": 1, "GB": 2}
TAKEOFF_PRACTICE = {"AP": 0.463, "BZ": 0.246, "GB": 0.339}
PILOT_DIED = {"AP": 5, "BZ": 3, "GB": 2}

SPECIALIST_SERVICE = {
    "AP": [("MMH", "Memory Assessment Service"), ("MMH", "Older Adults Community Mental Health Team"),
           ("WTH", "Care of the Elderly"), ("MMH", "Old Age Psychiatry Liaison")],
    "BZ": [("MMH", "Older Adults Community Mental Health Team"), ("WTH", "Care of the Elderly"),
           ("WTH", "Acute Medicine")],
    "GB": [("WTH", "Pain Management Service"), ("WTH", "Neurology"), ("WTH", "Rheumatology"),
           ("WTH", "Spinal Surgery")],
}
TRUST_NAME = {"WTH": "Wrekinside Teaching Hospitals NHS Trust", "MMH": "Marches Mental Health NHS Trust"}

DX = {"psychosis": ("69322001", "Psychotic disorder"), "schizophrenia": ("58214004", "Schizophrenia"),
      "bipolar": ("13746004", "Bipolar disorder"), "epilepsy": ("84757009", "Epilepsy"),
      "palliative": ("1129481000000101", "On palliative care register"),
      "dementia": ("52448006", "Dementia"), "insomnia": ("193462001", "Insomnia"),
      "anxiety": ("197480006", "Anxiety disorder"), "neuropathic": ("247398009", "Neuropathic pain"),
      "back_pain": ("279039007", "Low back pain"), "fibromyalgia": ("203082005", "Fibromyalgia"),
      "delirium": ("2776000", "Delirium")}


def courses(T):
    """Every course the three reviews look at, with who started it; the pools outside the pilot network, the pilot's
    reviewed patients, and the courses no review selects."""
    r = rng("courses")
    P = T.P
    lin = lineage_start(T)
    alive = P["death"].values == -1
    by, bmo = P["birth_year"].values, P["birth_month"].values
    cand = {pc: {"old": [], "adult": []} for pc, _ in PCNS}
    for p, (prac, st) in lin.items():
        if not alive[p] or st > di(dt.date(2025, 3, 1)):
            continue
        pc = PCN_OF[prac]
        a = age_on(by[p], bmo[p], AS_OF)
        if a >= 18:
            cand[pc]["adult"].append(p)
        if a >= 65:
            cand[pc]["old"].append(p)
    for pc in cand:
        cand[pc]["old"].sort()
        cand[pc]["adult"].sort()
    taken = set()
    rows = []
    dx = []
    cid = [610000]
    rid = rng("course_ids")

    def nid():
        cid[0] += int(rid.integers(2, 30))
        return "MC%07d" % cid[0]

    def weights(ps, cls):
        a = np.array([age_on(by[p], bmo[p], AS_OF) for p in ps], float)
        if cls == "AP":
            w = np.clip(a - 60, 1, None) ** 1.4
        elif cls == "BZ":
            w = np.clip(1 + (a - 60) / 18.0, 0.2, None)
        elif cls == "GB":
            w = np.where(a < 35, 0.3, np.where(a < 55, 1.0, np.where(a < 75, 1.4, 1.0)))
        else:
            w = np.ones(len(a))
        return w / w.sum()

    def choose(R, ps, n, cls, tag):
        ps = [p for p in ps if (p, tag) not in taken]
        if n > len(ps):
            raise AssertionError("pool too small for %s" % tag)
        idx = R.choice(len(ps), size=n, replace=False, p=weights(ps, cls))
        got = [ps[i] for i in sorted(idx)]
        for p in got:
            taken.add((p, tag))
        return got

    def product(R, cls):
        mix = MIX[cls]
        keys = sorted(mix)
        w = np.array([mix[k] for k in keys])
        return keys[int(R.choice(len(keys), p=w / w.sum()))]

    def start_between(R, p, lo, hi):
        st = lin[p][1] if p in lin else di(lo)
        a = max(di(lo), st + 30)
        b = di(hi)
        if a >= b:
            return None
        return int(R.integers(a, b))

    def add(R, p, cls, prov, role, start, end=-1, vmp=None, review=None):
        rows.append(dict(cid=nid(), p=p, cls=cls, vmp=vmp or product(R, cls), prov=prov, role=role, start=start,
                         end=end, review=review))
        return rows[-1]

    # --- the pools outside the pilot network, eligible on 31 December 2026 (one stream per pool)
    T.pool = {}
    for cls in REVIEWS:
        for pc in ("WC", "WN", "TV", "SG"):
            R = rng("pool:%s:%s" % (cls, pc))
            base = cand[pc]["old"] if cls in ("AP", "BZ") else cand[pc]["adult"]
            n = int(round(PREV[cls] * len(base)))
            got = choose(R, base, n, cls, cls)
            nspec = int(round(n * SPEC_SHARE[cls][pc]))
            flags = np.array(["specialist"] * nspec + ["practice"] * (n - nspec))[R.permutation(n)]
            for p, prov in zip(got, flags):
                s = start_between(R, p, COURSE_FLOOR, dt.date(2026, 5, 31))
                if s is None:
                    raise AssertionError("no start")
                add(R, p, cls, str(prov), "pool", s, review=cls)
                if cls == "GB":
                    s2 = start_between(R, p, COURSE_FLOOR, dt.date(2026, 5, 31))
                    add(R, p, "OP", "practice", "pool_opioid", s2)
                if cls == "BZ" and prov == "practice" and R.random() < 0.06:
                    s0 = rows[-1]["start"]
                    if s0 + 120 < di(dt.date(2026, 6, 15)):
                        s2 = int(R.integers(s0 + 120, di(dt.date(2026, 6, 15))))
                        first = rows[-1]["vmp"]
                        alt = [v for v in sorted(MIX["BZ"]) if PROD[v]["name"].split()[0] != PROD[first]["name"].split()[0]]
                        add(R, p, "BZ", "practice", "pool_second", s2, vmp=alt[int(R.integers(0, len(alt)))])
            T.pool[(cls, pc)] = got
    # --- the pilot network: patients meeting a protocol when the pilot began
    T.pilot = {}
    for cls in REVIEWS:
        R = rng("pilot_pool:%s" % cls)
        base = cand["CV"]["old"] if cls in ("AP", "BZ") else cand["CV"]["adult"]
        n = PILOT_N[cls]
        got = choose(R, base, n, cls, cls)
        flags = np.array(["specialist"] * PILOT_SPEC[cls] + ["practice"] * (n - PILOT_SPEC[cls]))[R.permutation(n)]
        T.pilot[cls] = []
        for p, prov in zip(got, flags):
            s = start_between(R, p, COURSE_FLOOR, dt.date(2025, 6, 30))
            if s is None:
                raise AssertionError("no pilot start")
            c = add(R, p, cls, str(prov), "pilot", s, review=cls)
            if cls == "GB":
                s2 = start_between(R, p, COURSE_FLOOR, dt.date(2025, 6, 30))
                add(R, p, "OP", "practice", "pilot_opioid", s2)
            T.pilot[cls].append(c)
    r = rng("courses")
    in_pool = {p for got_ in T.pool.values() for p in got_} | {c_["p"] for cs_ in T.pilot.values() for c_ in cs_}
    # --- the pilot patients who died before their six-month follow-up (dead by the as-of date, so outside every pool)
    dead_cv = sorted(p for p in range(len(P)) if P["death"].values[p] != -1
                     and dd(P["death"].values[p]) > dt.date(2026, 3, 1) and dd(P["death"].values[p]) < dt.date(2026, 11, 1)
                     and age_on(by[p], bmo[p], AS_OF) >= 70)
    dead_cv = [p for p in dead_cv if PCN_OF.get(_practice_at(T, p, PILOT_START) or "", "") == "CV"
               and _spell_start_at(T, p, PILOT_START) < di(dt.date(2024, 6, 1))]
    T.pilot_died = {}
    k = 0
    for cls in REVIEWS:
        T.pilot_died[cls] = []
        for _ in range(PILOT_DIED[cls]):
            p = dead_cv[(k * 37) % len(dead_cv)]
            k += 1
            while (p, cls) in taken:
                p = dead_cv[(k * 37) % len(dead_cv)]
                k += 1
            taken.add((p, cls))
            st = _spell_start_at(T, p, PILOT_START)
            s = int(r.integers(max(di(COURSE_FLOOR), st + 30), di(dt.date(2025, 6, 30))))
            c = add(r, p, cls, "practice", "pilot_died", s, end=int(P["death"].values[p]) - int(r.integers(3, 20)),
                    review=cls)
            if cls == "GB":
                add(r, p, "OP", "practice", "pilot_died_opioid", s + int(r.integers(0, 30)), end=c["end"])
            T.pilot_died[cls].append(c)
    # --- courses no review selects
    for pc, _ in PCNS:
        old = cand[pc]["old"]
        adult = cand[pc]["adult"]
        young = [p for p in adult if age_on(by[p], bmo[p], AS_OF) < 65]
        sc = len(adult) / 30000.0
        for p in choose(r, young, int(150 * sc), "AP", "AP"):
            add(r, p, "AP", "specialist" if r.random() < 0.75 else "practice", "texture",
                start_between(r, p, COURSE_FLOOR, dt.date(2026, 5, 31)))
            if r.random() < 0.85:
                k_ = ["psychosis", "schizophrenia", "bipolar"][int(r.integers(0, 3))]
                dx.append((p, k_, int(r.integers(di(dt.date(2008, 1, 1)), di(dt.date(2025, 6, 1))))))
        for p in choose(r, old, int(26 * sc), "AP", "AP"):
            add(r, p, "AP", "specialist", "texture_smi", start_between(r, p, COURSE_FLOOR, dt.date(2026, 5, 31)))
            k_ = ["psychosis", "schizophrenia", "bipolar"][int(r.integers(0, 3))]
            dx.append((p, k_, int(r.integers(di(dt.date(1995, 1, 1)), di(dt.date(2019, 6, 1))))))
        for p in choose(r, old, int(38 * sc), "AP", "AP"):
            s = start_between(r, p, COURSE_FLOOR, dt.date(2025, 3, 1))
            if s is None:
                continue
            add(r, p, "AP", "specialist" if r.random() < 0.6 else "practice", "texture_ended", s,
                end=int(r.integers(s + 90, di(dt.date(2026, 6, 20)))))
        for p in choose(r, young, int(300 * sc), "BZ", "BZ"):
            add(r, p, "BZ", "practice" if r.random() < 0.9 else "specialist", "texture",
                start_between(r, p, COURSE_FLOOR, dt.date(2026, 5, 31)))
        for p in choose(r, [p_ for p_ in old if p_ not in in_pool], int(16 * sc), "BZ", "BZ"):
            s = start_between(r, p, COURSE_FLOOR, dt.date(2025, 6, 1))
            if s is None:
                continue
            add(r, p, "BZ", "specialist", "texture_clobazam", s, vmp="39720211000001108")
            dx.append((p, "epilepsy", s - int(r.integers(60, 2000))))
        for p in choose(r, old, int(60 * sc), "BZ", "BZ"):
            s = start_between(r, p, dt.date(2025, 1, 1), dt.date(2026, 10, 1))
            if s is None:
                continue
            add(r, p, "BZ", "practice", "texture_short", s, end=s + int(r.integers(20, 50)))
        for p in choose(r, adult, int(330 * sc), "GB", "GB"):
            add(r, p, "GB", "practice" if r.random() < 0.6 else "specialist", "texture_no_opioid",
                start_between(r, p, COURSE_FLOOR, dt.date(2026, 5, 31)))
            taken.add((p, "OP"))
        for (cls_, pc_), got_ in T.pool.items():
            if cls_ == "GB" and pc_ == pc:
                for p in got_:
                    taken.add((p, "OP"))
        for c_ in T.pilot["GB"]:
            taken.add((c_["p"], "OP"))
        for p in choose(r, [p_ for p_ in adult if p_ not in in_pool], int(22 * sc), "GB", "GB"):
            s = start_between(r, p, COURSE_FLOOR, dt.date(2026, 5, 31))
            add(r, p, "GB", "specialist", "texture_epilepsy", s)
            add(r, p, "OP", "practice", "texture_epilepsy_opioid", start_between(r, p, COURSE_FLOOR, dt.date(2026, 5, 31)))
            dx.append((p, "epilepsy", s - int(r.integers(60, 3000))))
        for p in choose(r, adult, int(950 * sc), "OP", "OP"):
            add(r, p, "OP", "practice", "texture", start_between(r, p, COURSE_FLOOR, dt.date(2026, 5, 31)))
        # would-be eligible patients on the palliative care register (none of them in a pool or the pilot)
        for cls in REVIEWS:
            base = [p for p in (old if cls in ("AP", "BZ") else adult) if p not in in_pool]
            for p in choose(r, base, max(1, int({"AP": 5, "BZ": 7, "GB": 6}[cls] * sc)), cls, cls):
                s = start_between(r, p, COURSE_FLOOR, dt.date(2026, 5, 31))
                add(r, p, cls, "specialist" if r.random() < 0.5 else "practice", "texture_palliative", s)
                if cls == "GB":
                    add(r, p, "OP", "practice", "texture_palliative_opioid", start_between(r, p, COURSE_FLOOR, dt.date(2026, 5, 31)))
                dx.append((p, "palliative", int(r.integers(di(dt.date(2025, 9, 1)), di(dt.date(2026, 12, 20))))))
    C = pd.DataFrame(rows)
    C = C[C["start"].notna()].copy()
    C["start"] = C["start"].astype(int)
    T.C = C.reset_index(drop=True)
    # diagnoses the reviews' users carry (texture), plus the exclusions above
    rx = rng("diagnoses")
    for rec in T.C.itertuples(index=False):
        if rec.cls == "AP" and rx.random() < 0.55:
            k_ = "dementia" if rx.random() < 0.7 else "delirium"
            dx.append((rec.p, k_, rec.start - int(rx.integers(10, 900))))
        elif rec.cls == "BZ" and rx.random() < 0.5:
            dx.append((rec.p, "insomnia" if rx.random() < 0.6 else "anxiety", rec.start - int(rx.integers(0, 1500))))
        elif rec.cls == "GB" and rx.random() < 0.6:
            dx.append((rec.p, ["neuropathic", "back_pain", "fibromyalgia"][int(rx.integers(0, 3))],
                       rec.start - int(rx.integers(0, 2000))))
    T.DX = pd.DataFrame(dx, columns=["p", "dx", "date"]).drop_duplicates(["p", "dx"]).reset_index(drop=True)


def _practice_at(T, p, d):
    x = di(d)
    for a, b, c, _ in T.spells_by_p.get(int(p), []):
        if a <= x and (b == -1 or x < b):
            return survivor(c, d)
    return None


def _spell_start_at(T, p, d):
    x = di(d)
    for a, b, c, _ in T.spells_by_p.get(int(p), []):
        if a <= x and (b == -1 or x < b):
            return a
    return None


# --------------------------------------------------------------------------------------------------------------------
# The pilot's outcomes and the issues
# --------------------------------------------------------------------------------------------------------------------
def pilot_outcomes(T):
    """Each pilot patient's review (January to June 2026) and six-month status. One or two specialist-started patients
    in each review came off; the practice-started came off at the review's rate, spread evenly over age band and sex."""
    r = rng("pilot")
    P = T.P
    out = {}
    span = (PILOT_END - PILOT_START).days
    for cls in REVIEWS:
        cs = T.pilot[cls]
        spec = [c for c in cs if c["prov"] == "specialist"]
        prac = [c for c in cs if c["prov"] == "practice"]
        off = set()
        pool = [c for c in T.C.itertuples(index=False) if c.role == "pool" and c.cls == cls and c.prov == "specialist"]
        fed_b, fed_s = {}, {}
        for c in pool:
            b = age_band(age_on(P["birth_year"].values[c.p], P["birth_month"].values[c.p], AS_OF))
            s = P["sex"].values[c.p]
            fed_b[b] = fed_b.get(b, 0) + 1
            fed_s[s] = fed_s.get(s, 0) + 1
        attrs = []
        for c in spec:
            a = age_on(P["birth_year"].values[c["p"]], P["birth_month"].values[c["p"]], AS_OF)
            attrs.append((age_band(a), P["sex"].values[c["p"]]))
        n_b, n_s = {}, {}
        for b, s in attrs:
            n_b[b] = n_b.get(b, 0) + 1
            n_s[s] = n_s.get(s, 0) + 1
        k = PILOT_SPEC_OFF[cls]
        N = len(pool)
        best, best_v = None, None
        import itertools
        order = [int(i) for i in r.permutation(len(spec))]
        for combo in itertools.combinations(order, k):
            ob, os_ = {}, {}
            for i in combo:
                ob[attrs[i][0]] = ob.get(attrs[i][0], 0) + 1
                os_[attrs[i][1]] = os_.get(attrs[i][1], 0) + 1
            base_ = N * k / len(spec)
            vb = sum(fed_b.get(b, 0) * ob.get(b, 0) / n_b[b] for b in n_b) + \
                sum(fed_b.get(b, 0) * k / len(spec) for b in fed_b if b not in n_b)
            vs = sum(fed_s.get(s, 0) * os_.get(s, 0) / n_s[s] for s in n_s) + \
                sum(fed_s.get(s, 0) * k / len(spec) for s in fed_s if s not in n_s)
            v = max(abs(vb - base_), abs(vs - base_))
            if best_v is None or v < best_v - 1e-12:
                best, best_v = combo, v
        for i in best:
            off.add(spec[i]["cid"])

        def key(c):
            a = age_on(P["birth_year"].values[c["p"]], P["birth_month"].values[c["p"]], AS_OF)
            return (age_band(a), P["sex"].values[c["p"]], float(r.random()))
        prac_sorted = sorted(prac, key=key)
        rate = TAKEOFF_PRACTICE[cls]
        acc = float(r.random())
        for c in prac_sorted:
            acc += rate
            if acc >= 1.0:
                acc -= 1.0
                off.add(c["cid"])
        res = []
        for c in cs:
            rv = PILOT_START + dt.timedelta(days=int(r.integers(0, span)))
            while not working(rv):
                rv = rv + dt.timedelta(days=1)
            if c["cid"] in off:
                outcome = "Stopped" if r.random() < 0.75 else "Taper agreed"
                status = "Off"
            else:
                outcome = ["Continued", "Dose reduced", "Continued, patient declined change", "Stopped"][
                    int(r.choice(4, p=[0.46, 0.27, 0.17, 0.10]))]
                status = "On"
            res.append(dict(c=c, review=rv, outcome=outcome, status=status))
        died = []
        for c in T.pilot_died[cls]:
            rv = PILOT_START + dt.timedelta(days=int(r.integers(0, 40)))
            while not working(rv):
                rv = rv + dt.timedelta(days=1)
            died.append(dict(c=c, review=rv, outcome=["Continued", "Dose reduced"][int(r.integers(0, 2))], status=None))
        out[cls] = (res, died)
    T.pilot_res = out


def issues(T):
    """Every issue of each course: about every 28 days from the first issue, a few days late at times. A pilot patient
    taken off has no issue after the review; one stopped at review but not off was restarted within six months."""
    r = rng("issues")
    stop_at, gap = {}, {}
    for cls in REVIEWS:
        res, died = T.pilot_res[cls]
        for x in res:
            c = x["c"]
            if x["status"] == "Off":
                stop_at[c["cid"]] = di(x["review"]) - 1
            elif x["outcome"] == "Stopped":
                gap[c["cid"]] = (di(x["review"]), di(x["review"]) + int(r.integers(30, 120)))
        for x in died:
            pass
    rows = []
    last, count = {}, {}
    for c in T.C.itertuples(index=False):
        every = PROD[c.vmp]["every"]
        t = c.start
        n = 0
        end = c.end if c.end != -1 else di(AS_OF)
        if c.cid in stop_at:
            end = min(end, stop_at[c.cid])
        lst = None
        while t <= end:
            if c.cid in gap and gap[c.cid][0] < t < gap[c.cid][1]:
                t = gap[c.cid][1]
                continue
            n += 1
            lst = t
            rows.append((c.cid, t, n))
            t = t + every + int(r.choice([-2, -1, 0, 0, 0, 1, 2, 3, 5, 8]))
        last[c.cid] = lst
        count[c.cid] = n
    T.C["last"] = T.C["cid"].map(last)
    T.C["n_issues"] = T.C["cid"].map(count)
    T.I = pd.DataFrame(rows, columns=["cid", "date", "seq"])


# --------------------------------------------------------------------------------------------------------------------
# The letters feed and the practices' document workflow
# --------------------------------------------------------------------------------------------------------------------
START_FORMS = ["Commenced {g} {s} at night", "Please start {g} {s}", "{G} {s} started on the ward, please continue",
               "Suggest starting {g} {s} and review in four weeks", "Started {g} ({b}) {s}",
               "We have started {g} {s}, please prescribe"]
OTHER_FORMS = {"Continue": ["Please continue {g} {s}", "Continue {g} {s} unchanged"],
               "Change dose": ["Please reduce {g} to {s}", "{G} dose changed to {s}, please update"],
               "Review": ["Please review the need for {g}", "{G} {s}: review at next appointment"],
               "Stop": ["Please stop {g}", "{G} stopped during admission"]}
BACKGROUND_MEDS = [
    ("Atorvastatin", "20mg"), ("Atorvastatin", "40mg"), ("Ramipril", "5mg"), ("Amlodipine", "5mg"),
    ("Bisoprolol", "2.5mg"), ("Apixaban", "5mg"), ("Edoxaban", "60mg"), ("Furosemide", "40mg"),
    ("Lansoprazole", "30mg"), ("Omeprazole", "20mg"), ("Sertraline", "50mg"), ("Mirtazapine", "15mg"),
    ("Metformin", "500mg"), ("Empagliflozin", "10mg"), ("Levothyroxine", "50microgram"), ("Prednisolone", "5mg"),
    ("Alendronic acid", "70mg"), ("Colecalciferol", "800unit"), ("Tamsulosin", "400microgram"),
    ("Donepezil", "5mg"), ("Clopidogrel", "75mg"), ("Methotrexate", "10mg"), ("Salbutamol", "100microgram"),
    ("Doxycycline", "100mg"), ("Nitrofurantoin", "50mg"), ("Paracetamol", "500mg"), ("Lithium carbonate", "400mg"),
    ("Venlafaxine", "75mg"), ("Citalopram", "20mg"), ("Ferrous fumarate", "210mg"),
]
BACKGROUND_SERVICES = [("WTH", "Cardiology", 0.12), ("WTH", "Respiratory Medicine", 0.08),
                       ("WTH", "Acute Medicine", 0.17), ("WTH", "Care of the Elderly", 0.10),
                       ("WTH", "Diabetes and Endocrinology", 0.07), ("WTH", "Rheumatology", 0.04),
                       ("WTH", "Urology", 0.05), ("WTH", "Gastroenterology", 0.06), ("WTH", "Orthopaedics", 0.07),
                       ("WTH", "Emergency Department", 0.09), ("WTH", "Renal Medicine", 0.02),
                       ("MMH", "Memory Assessment Service", 0.04), ("MMH", "Adult Community Mental Health Team", 0.05),
                       ("MMH", "Crisis Resolution Team", 0.02), ("MMH", "Older Adults Community Mental Health Team", 0.02)]


def med_text(r, generic, strength, kind):
    g = generic.lower()
    if kind == "Start":
        form = START_FORMS[int(r.integers(0, len(START_FORMS)))]
    else:
        forms = OTHER_FORMS[kind]
        form = forms[int(r.integers(0, len(forms)))]
    return form.format(g=g, G=generic, s=strength, b=BRAND.get(generic, generic))


def letters(T):
    """The trusts' medicine letters to member practices since the feed opened: one row per medicine line. The letter
    recommending a specialist-started course is dated 5 to 26 days before the practice's first issue."""
    r = rng("letters")
    P, S, C = T.P, T.S, T.C
    by, bmo = P["birth_year"].values, P["birth_month"].values
    L = []   # letter-level dicts with lines

    def prac_at(p, x):
        for a, b, c, _ in T.spells_by_p.get(int(p), []):
            if a <= x and (b == -1 or x < b):
                return c
        return None

    for c in C.itertuples(index=False):
        if c.cls not in REVIEWS:
            continue
        name = PROD[c.vmp]["name"]
        generic, strength = name.split()[0], name.split()[1]
        if c.prov == "specialist":
            ld = c.start - int(r.integers(5, 27))
            trust, service = SPECIALIST_SERVICE[c.cls][int(r.integers(0, len(SPECIALIST_SERVICE[c.cls])))]
            if c.cls == "BZ" and c.role == "texture_clobazam":
                trust, service = "WTH", "Neurology"
            # the mental health trust sent nothing from 31 March to 6 April 2026: a course begun then was recommended
            # by the hospital trust's service
            if trust == "MMH" and di(dt.date(2026, 3, 31)) <= ld < di(MMH_SWITCH):
                trust, service = "WTH", "Care of the Elderly"
            # a letter dated over Christmas reaches the practice in January, before the practice issues
            dl = dd(ld)
            if dt.date(dl.year, 12, 22) <= dl and c.start < di(dt.date(dl.year + 1, 1, 9)):
                ld = di(dt.date(dl.year, 12, 21)) - int(r.integers(0, 4))
            pr = prac_at(c.p, ld)
            if pr is None or ld < di(FEED_OPEN):
                raise AssertionError("initiation letter outside registration or feed")
            enc = ld - int(r.integers(0, 15))
            if trust == "MMH" and ld < di(dt.date(2026, 3, 31)):
                enc = min(enc, ld)
            L.append(dict(p=c.p, trust=trust, service=service, enc=enc, date=ld, prac=pr,
                          lines=[(med_text(r, generic, strength, "Start"), "Start")], kind="initiation",
                          cid=c.cid, cls=c.cls, start=c.start))
        if r.random() < (0.18 if c.prov == "practice" else 0.26):
            ld = c.start + int(r.integers(40, 700))
            lim = c.end if c.end != -1 else di(AS_OF)
            if ld <= lim:
                pr = prac_at(c.p, ld)
                if pr is not None:
                    trust, service = [("WTH", "Care of the Elderly"), ("WTH", "Acute Medicine"),
                                      ("WTH", "Orthopaedics"), ("MMH", "Older Adults Community Mental Health Team")][
                        int(r.integers(0, 4))]
                    rec = ["Continue", "Change dose", "Review", "Stop"][int(r.choice(4, p=[0.45, 0.2, 0.25, 0.1]))]
                    L.append(dict(p=c.p, trust=trust, service=service, enc=ld - int(r.integers(0, 12)), date=ld,
                                  prac=pr, lines=[(med_text(r, generic, strength, rec), rec)], kind="later",
                                  cid=c.cid, cls=c.cls))
    # background letters: any registered patient, medicines outside the reviews' classes and opioids
    rb = rng("background_letters")
    sv = np.array([s[2] for s in BACKGROUND_SERVICES])
    sv = sv / sv.sum()
    lo_f, hi_f = di(FEED_OPEN), di(AS_OF)
    Sx = S[S["prac"].isin(CODES)]
    a = np.maximum(Sx["start"].values, lo_f)
    b = np.where(Sx["end"].values == -1, hi_f, np.minimum(Sx["end"].values, hi_f))
    ok = b > a
    pp, aa, bb = Sx["p"].values[ok], a[ok], b[ok]
    mid_age = np.array([2023 - by[p] for p in pp])
    lam = 0.075 * np.where(mid_age < 40, 0.55, np.where(mid_age < 65, 1.0, 2.3)) * (bb - aa) / 365.25
    k = rb.poisson(lam)
    rep = np.repeat(np.arange(len(pp)), k)
    dates = aa[rep] + (rb.random(len(rep)) * (bb[rep] - aa[rep])).astype(int)
    svc = rb.choice(len(BACKGROUND_SERVICES), size=len(rep), p=sv)
    nlines = 1 + rb.poisson(0.3, len(rep))
    for j in range(len(rep)):
        p = int(pp[rep[j]])
        d_ = int(dates[j])
        trust, service, _ = BACKGROUND_SERVICES[int(svc[j])]
        lines = []
        used = set()
        for _ in range(int(nlines[j])):
            med = BACKGROUND_MEDS[int(rb.integers(0, len(BACKGROUND_MEDS)))]
            if med[0] in used:
                continue
            used.add(med[0])
            rec = ["Start", "Continue", "Change dose", "Stop", "Review"][int(rb.choice(5, p=[0.34, 0.27, 0.17, 0.14, 0.08]))]
            lines.append((med_text(rb, med[0], med[1], rec), rec))
        pr = prac_at(p, d_)
        if pr is None:
            continue
        L.append(dict(p=p, trust=trust, service=service, enc=d_ - int(rb.integers(0, 15)), date=d_, prac=pr,
                      lines=lines, kind="background", cid=None, cls=None))
    L = [x for x in L if di(FEED_OPEN) <= x["date"] <= di(AS_OF)]
    L.sort(key=lambda x: (x["date"], x["trust"], x["p"], x["lines"][0][0]))
    # references, identifiers and the hospitals' practice field
    rr = rng("letter_refs")
    seq = {"WTH": 2804400, "MMH": 180000, "MMHN": 4100}
    hn_seen, hn = set(), {}

    def hospnum(p, trust):
        key = (p, trust)
        if key not in hn:
            while True:
                x = ("RXW%07d" % rr.integers(1000000, 9999999)) if trust == "WTH" else ("M%06d" % rr.integers(100000, 999999))
                if x not in hn_seen:
                    hn_seen.add(x)
                    hn[key] = x
                    break
        return hn[key]

    for x in L:
        d_ = dd(x["date"])
        x["held"] = False
        if x["trust"] == "MMH" and dt.date(2026, 3, 31) <= d_ < MMH_SWITCH:
            x["date"] = di(MMH_SWITCH)
            x["held"] = True
            d_ = MMH_SWITCH
        seq_key = "MMHN" if (x["trust"] == "MMH" and d_ >= MMH_SWITCH) else x["trust"]
        seq[seq_key] += int(rr.integers(1, 7))
        if seq_key == "WTH":
            x["ref"] = "WTH-L%07d" % seq["WTH"]
        elif seq_key == "MMH":
            x["ref"] = "MMH/%d/%06d" % (d_.year, seq["MMH"])
        else:
            x["ref"] = "MMH-EPR-%07d" % seq["MMHN"]
        x["hn"] = hospnum(x["p"], x["trust"])
        x["hn_only"] = x["kind"] != "initiation" and rr.random() < 0.055
        # merged practices: the hospitals kept the old code on some records after the merger
        x["addressed"] = x["prac"]
        if x["prac"] in MERGED and d_ >= MERGE_DATE:
            x["addressed"] = x["prac"] if rr.random() < 0.35 else MERGED[x["prac"]]
        elif x["prac"] in MERGED:
            x["addressed"] = x["prac"]
        x["resend_of"] = None
    # the mental health trust's April 2026 switch: letters dated 9 to 30 March re-sent under the new system's numbers
    resend = []
    for x in L:
        if x["trust"] == "MMH" and di(RESEND_FROM) <= x["date"] <= di(RESEND_TO) and not x["held"]:
            y = dict(x)
            seq["MMHN"] += int(rr.integers(1, 7))
            y["ref"] = "MMH-EPR-%07d" % seq["MMHN"]
            y["date"] = di(MMH_SWITCH)
            y["resend_of"] = x["ref"]
            y["kind"] = x["kind"] + "_resend"
            resend.append(y)
    L = L + resend
    T.L = L
    T.hn = hn


def _receipt_lag(r, d):
    """Days from a letter's date to its arrival in the practice's workflow: most the same or next day, a tail to a
    fortnight; letters dated over Christmas wait for the trusts' document teams to return."""
    lag = int(r.choice(13, p=[0.30, 0.22, 0.12, 0.08, 0.06, 0.05, 0.04, 0.04, 0.03, 0.02, 0.02, 0.01, 0.01]))
    x = d + dt.timedelta(days=lag)
    if dt.date(d.year, 12, 22) <= d <= dt.date(d.year, 12, 31):
        x = max(x, dt.date(d.year + 1, 1, 2) + dt.timedelta(days=int(r.integers(0, 4))))
    while x.weekday() >= 5 or x in BANK_HOLIDAYS:
        x = x + dt.timedelta(days=1)
    return x


def workflow(T):
    """The practices' document workflow: each document received from the two trusts with the time it arrived, the
    practice that received it, the patient it was filed to and the sender's reference (WTH documents received through
    GP Connect from October 2026 carry the message id instead). Non-medicine documents are received too."""
    r = rng("workflow")
    rows = []
    for x in T.L:
        d_ = dd(x["date"])
        recv = _receipt_lag(r, d_)
        if x["resend_of"]:
            recv = MMH_SWITCH + dt.timedelta(days=int(r.integers(0, 2)))
        elif x["kind"] == "initiation":
            cap = dd(x["start"]) - dt.timedelta(days=2)
            if recv > cap:
                recv = max(d_, cap)
                while recv.weekday() >= 5 or recv in BANK_HOLIDAYS:
                    recv = recv - dt.timedelta(days=1)
                recv = max(recv, d_)
        x["received"] = recv
        prac = survivor(x["addressed"], recv)
        x["recv_prac"] = prac
        if recv < dt.date(2026, 1, 1) or recv > PULL:
            continue
        rows.append(dict(p=x["p"], trust=x["trust"], service=x["service"], docdate=d_, recv=recv, prac=prac,
                         ref=x["ref"], med=True, letter=x))
    # other documents (results, letters with no medicine change) for registered patients in 2026
    rb = rng("other_docs")
    S = T.S
    lo, hi = di(dt.date(2025, 12, 1)), di(dt.date(2026, 12, 31))
    Sx = S[S["prac"].isin(CODES)]
    a = np.maximum(Sx["start"].values, lo)
    b = np.where(Sx["end"].values == -1, hi, np.minimum(Sx["end"].values, hi))
    ok = b > a
    pp, aa, bb = Sx["p"].values[ok], a[ok], b[ok]
    k = rb.poisson(0.11 * (bb - aa) / 365.25)
    rep = np.repeat(np.arange(len(pp)), k)
    dates = aa[rep] + (rb.random(len(rep)) * (bb[rep] - aa[rep])).astype(int)
    kinds = [("WTH", "Pathology report", 0.30), ("WTH", "Radiology report", 0.22), ("WTH", "Outpatient letter", 0.25),
             ("WTH", "Emergency Department attendance", 0.13), ("MMH", "Mental health letter", 0.10)]
    kw = np.array([k_[2] for k_ in kinds])
    kk = rb.choice(len(kinds), size=len(rep), p=kw / kw.sum())
    med_keys = {(x["p"], x["trust"], x["date"]) for x in T.L}
    # no other document from the same trust for a patient within 30 days of a medicine letter (2026 receipts)
    near = {}
    for x in T.L:
        if x["date"] >= di(dt.date(2025, 11, 1)):
            near.setdefault((x["p"], x["trust"]), []).append(x["date"])
    seqo = {"WTH": 900000, "MMH": 52000}
    for j in range(len(rep)):
        p = int(pp[rep[j]])
        d_ = int(dates[j])
        trust, dtype, _ = kinds[int(kk[j])]
        if (p, trust, d_) in med_keys or any(abs(d_ - y) <= 30 for y in near.get((p, trust), [])):
            continue
        pr = None
        for s0, s1, c, _ in T.spells_by_p.get(p, []):
            if s0 <= d_ and (s1 == -1 or d_ < s1):
                pr = c
                break
        if pr is None:
            continue
        recv = _receipt_lag(rb, dd(d_))
        if recv < dt.date(2026, 1, 1) or recv > PULL:
            continue
        seqo[trust] += int(rb.integers(1, 9))
        ref = ("WTH-D%07d" % seqo["WTH"]) if trust == "WTH" else ("MMH-EPR-D%06d" % seqo["MMH"])
        rows.append(dict(p=p, trust=trust, service=dtype, docdate=dd(d_), recv=recv, prac=survivor(pr, recv),
                         ref=ref, med=False, letter=None))
    rows.sort(key=lambda z: (z["recv"], z["prac"], z["ref"]))
    rg = rng("gpconnect")
    rt = rng("recv_times")
    did = 7700000
    for z in rows:
        did += int(rg.integers(1, 5))
        z["doc_id"] = did
        z["recv_at"] = dt.datetime.combine(z["recv"], dt.time(int(rt.integers(7, 19)), int(rt.integers(0, 60)),
                                                              int(rt.integers(0, 60))))
        if z["trust"] == "WTH" and z["recv"] >= GPCONNECT:
            # GP Connect: the message id for a reference and the message's own date for the document date
            z["ext"] = "%08x-%04x-4%03x-%04x-%012x" % (rg.integers(0, 2 ** 32), rg.integers(0, 2 ** 16),
                                                     rg.integers(0, 2 ** 12), 0x8000 + rg.integers(0, 2 ** 14),
                                                     rg.integers(0, 2 ** 48))
            z["docdate"] = z["recv"]
        else:
            z["ext"] = z["ref"]
        if z["letter"] is not None:
            z["letter"]["recv_doc"] = z
    T.W = rows


# --------------------------------------------------------------------------------------------------------------------
# The pharmacist team's 2026 consultations
# --------------------------------------------------------------------------------------------------------------------
HUBS = {"MPC-HUB-W": ("Wrekinside Hub", ["WC", "WN"]), "MPC-HUB-T": ("Teme and Gorge Hub", ["TV", "SG"]),
        "MPC-HUB-C": ("Clun Valley Hub", ["CV"])}
PHARMACISTS = ["CP01", "CP02", "CP03", "CP04", "CP05", "CP06", "CP07", "CP08", "CP09", "CP10"]
HUB_SHARE = {"CV": 0.28, "WC": 0.50, "WN": 0.46, "TV": 0.41, "SG": 0.43}
TYPES = ["Structured medication review", "Medication review", "Telephone medication review", "Polypharmacy review",
         "Medicines monitoring review"]


def consultations(T):
    r = rng("consultations")
    P = T.P
    by, bmo = P["birth_year"].values, P["birth_month"].values
    days = [dt.date(2026, 1, 1) + dt.timedelta(days=i) for i in range(365)]
    days = [x for x in days if working(x)]
    reg_cache = {}
    # patients seen are weighted towards older people
    lin = {}
    S = T.S
    x0 = di(dt.date(2026, 1, 1))
    cand = S[(S["prac"].isin(CODES)) & ((S["end"] == -1) | (S["end"] > x0)) & (S["start"] <= di(AS_OF))]["p"].unique()
    cand = np.sort(cand)
    ages = np.array([2026 - by[p] for p in cand])
    w = np.where(ages < 18, 0.05, np.where(ages < 50, 0.5, np.where(ages < 65, 1.2, np.where(ages < 80, 2.6, 3.2))))
    w = w / w.sum()

    def prac_on(p, d):
        x = di(d)
        for a, b, c, _ in T.spells_by_p.get(p, []):
            if a <= x and (b == -1 or x < b):
                return survivor(c, d)
        return None

    hub_rows, prac_rows, groups = [], [], []
    seen = {}   # (patient, pharmacist) -> list of dates with any contact, to keep hub and practice contacts apart
    aid, cid = 52000, 300000
    for day in days:
        n = int(r.poisson(44))
        picks = r.choice(len(cand), size=n, p=w)
        for j in picks:
            p = int(cand[j])
            code = prac_on(p, day)
            if code is None:
                continue
            pc = PCN_OF[code]
            ph = PHARMACISTS[int(r.integers(0, len(PHARMACISTS)))]
            ctype = TYPES[int(r.choice(5, p=[0.30, 0.26, 0.24, 0.12, 0.08]))]
            hub = r.random() < HUB_SHARE[pc] and ctype != "Telephone medication review"
            near = seen.get((p, ph), [])
            if any(abs((day - q).days) <= 10 for q in near):
                continue
            hh, mm = int(r.integers(8, 17)), int(r.choice([0, 15, 30, 45]))
            if hh == 8 and mm < 30:
                mm = 30
            t = dt.datetime.combine(day, dt.time(hh, mm))
            dur = int(r.choice([20, 30, 30, 45]))
            if hub:
                site = [h for h, v in HUBS.items() if pc in v[1]][0]
                outcome = ["Attended", "Did not attend", "Cancelled by patient", "Cancelled by hub"][
                    int(r.choice(4, p=[0.85, 0.08, 0.05, 0.02]))]
                aid += int(r.integers(1, 4))
                hub_rows.append(dict(aid="HB%06d" % aid, site=site, t=t, dur=dur, ph=ph, ctype=ctype, p=p,
                                     outcome=outcome, code=code))
                seen.setdefault((p, ph), []).append(day)
                if outcome == "Attended" and code in SHARED_RECORD:
                    q_end = dt.date(2026, ((day.month - 1) // 3) * 3 + 3, 1) + dt.timedelta(days=31)
                    q_end = dt.date(q_end.year, q_end.month, 1) - dt.timedelta(days=1)
                    nxt = next_working(day)
                    if r.random() < 0.36 and nxt <= q_end:
                        wt = dt.datetime.combine(nxt, dt.time(int(r.integers(8, 11)), int(r.integers(0, 60))))
                    else:
                        wt = t + dt.timedelta(minutes=dur + int(r.integers(5, 150)))
                    cid += int(r.integers(1, 6))
                    prac_rows.append(dict(cid="%s-%07d" % (code, cid), code=code, t=wt, ph=ph, ctype=ctype, p=p,
                                          hub_of=hub_rows[-1]["aid"]))
            else:
                cid += int(r.integers(1, 6))
                prac_rows.append(dict(cid="%s-%07d" % (code, cid), code=code, t=t, ph=ph, ctype=ctype, p=p,
                                      hub_of=None))
                seen.setdefault((p, ph), []).append(day)
                if r.random() < 0.025:
                    t2 = t + dt.timedelta(minutes=int(r.integers(90, 240)))
                    if t2.hour < 18:
                        cid += int(r.integers(1, 6))
                        prac_rows.append(dict(cid="%s-%07d" % (code, cid), code=code, t=t2, ph=ph,
                                              ctype="Telephone medication review", p=p, hub_of=None))
        if r.random() < 0.14:
            site = list(HUBS)[int(r.choice(3, p=[0.47, 0.35, 0.18]))]
            pcs = HUBS[site][1]
            k = int(r.integers(6, 13))
            att = []
            tries = 0
            while len(att) < k and tries < 2000:
                tries += 1
                p = int(cand[int(r.choice(len(cand), p=w))])
                code = prac_on(p, day)
                if code and PCN_OF[code] in pcs and 2026 - by[p] >= 60 and p not in [a_[0] for a_ in att]:
                    att.append((p, "Yes" if r.random() < 0.82 else "No"))
            aid += int(r.integers(1, 4))
            t = dt.datetime.combine(day, dt.time(int(r.choice([10, 13, 14])), 0))
            groups.append(dict(aid="HB%06d" % aid, site=site, t=t, dur=90,
                               ph=PHARMACISTS[int(r.integers(0, len(PHARMACISTS)))],
                               topic=["Falls and your medicines", "Pain medicines: what helps", "Sleeping without tablets",
                                      "Getting the best from your inhalers"][int(r.integers(0, 4))], attendees=att))
    T.hub, T.prac_cons, T.groups = hub_rows, prac_rows, groups


def list_sizes(T):
    """Patients registered at each member practice on the first of each month of 2026 and on 1 January 2027."""
    S = T.S
    out = []
    months = [dt.date(2026, m, 1) for m in range(1, 13)] + [dt.date(2027, 1, 1)]
    for d in months:
        x = di(d)
        m = (S["start"] <= x) & ((S["end"] == -1) | (S["end"] > x))
        sub = S.loc[m, "prac"].map(lambda c: survivor(c, d))
        vc = sub.value_counts()
        for c in CODES:
            if c in MERGED:
                continue
            out.append((c, d, int(vc.get(c, 0))))
    T.LS = pd.DataFrame(out, columns=["practice", "date", "patients"])


_CACHE = {}


def build():
    if "T" in _CACHE:
        return _CACHE["T"]
    T = World()
    population(T)
    courses(T)
    pilot_outcomes(T)
    issues(T)
    letters(T)
    workflow(T)
    consultations(T)
    list_sizes(T)
    _CACHE["T"] = T
    return T
