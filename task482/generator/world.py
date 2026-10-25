"""The clean truth of task482's world (architecture 13): a clinically integrated network of thirteen independent primary
care practices and the commercial members of its three payers in 2025 and 2026.

Everything is generated forward from the parameters below with fixed seeds: each person's enrollment with a payer,
their primary care visits (the qualifying services attribution counts), every other claim with its allowed amount and
paid date, each payer's attribution (the final 2025 run, the monthly 2026 interim runs, the 2026 final run as truth),
and the care coordination fees each payer remits on its runs. The pack (pack.py) cuts the payers' feeds from this
truth; the golden (golden.py) reads only the pack."""
import datetime as dt
import math

import numpy as np

SEED = 482130
D = dt.date
YEARS = (2025, 2026)
RUN_DATE = D(2026, 10, 5)         # the October interim run
RUN_CUT = D(2026, 8, 31)          # on qualifying services incurred through 31 August 2026
RUN_PAID = D(2026, 9, 30)         # and paid by 30 September 2026
FEED_PAID = D(2026, 9, 30)        # the October feeds carry 2026 claims paid through 30 September 2026
FINAL_PAID = {2025: D(2026, 3, 31), 2026: D(2027, 3, 31)}   # a year's final run counts claims paid by 31 March after it
TREND = 1.052
MSR = 0.02
CAP = 250000.0
PAYERS = ("B", "M", "T")

# practice: code, kind, panel persons, chronic share, need scale, share of annual visits pulled into January to March by
# outreach, share pushed into October to December, payer mix (B, M, T), clinicians, hospital-based clinic, and the
# target position of the golden figure against the practice's threshold (MOVE below places it)
PRACTICES = [
    dict(code="P01", kind="IM", n=2500, chronic=0.36, need=1.06, camp=0.86, late=0.00, mix=(0.58, 0.28, 0.14), pcp=6, hosp=False, pos=-0.0837),
    dict(code="P02", kind="FM", n=2900, chronic=0.17, need=0.92, camp=0.02, late=0.40, mix=(0.50, 0.36, 0.14), pcp=7, hosp=False, pos=-0.0612),
    dict(code="P03", kind="FM", n=2500, chronic=0.26, need=0.98, camp=0.82, late=0.00, mix=(0.62, 0.24, 0.14), pcp=6, hosp=False, pos=-0.0584),
    dict(code="P04", kind="IM", n=2200, chronic=0.40, need=1.12, camp=0.84, late=0.00, mix=(0.47, 0.38, 0.15), pcp=5, hosp=False, pos=0.0527),
    dict(code="P05", kind="PED", n=2800, chronic=0.10, need=0.62, camp=0.04, late=0.36, mix=(0.55, 0.27, 0.18), pcp=7, hosp=True, pos=0.0543),
    dict(code="P06", kind="FM", n=2600, chronic=0.20, need=1.00, camp=0.03, late=0.38, mix=(0.60, 0.25, 0.15), pcp=6, hosp=False, pos=-0.0706),
    dict(code="P07", kind="FM", n=2300, chronic=0.30, need=1.04, camp=0.80, late=0.00, mix=(0.52, 0.30, 0.18), pcp=5, hosp=False, pos=-0.0771),
    dict(code="P08", kind="FM", n=2700, chronic=0.16, need=0.90, camp=0.02, late=0.42, mix=(0.57, 0.31, 0.12), pcp=6, hosp=False, pos=-0.0537),
    dict(code="P09", kind="IM", n=2100, chronic=0.44, need=1.18, camp=0.88, late=0.00, mix=(0.55, 0.29, 0.16), pcp=5, hosp=True, pos=0.0493),
    dict(code="P10", kind="FM", n=3000, chronic=0.18, need=0.94, camp=0.03, late=0.40, mix=(0.54, 0.33, 0.13), pcp=7, hosp=False, pos=-0.0794),
    dict(code="P11", kind="PED", n=2400, chronic=0.08, need=0.58, camp=0.02, late=0.38, mix=(0.58, 0.26, 0.16), pcp=6, hosp=False, pos=-0.0743),
    dict(code="P12", kind="IM", n=2000, chronic=0.38, need=1.10, camp=0.84, late=0.00, mix=(0.50, 0.34, 0.16), pcp=5, hosp=False, pos=0.0571),
    dict(code="P13", kind="FM", n=2500, chronic=0.21, need=0.97, camp=0.03, late=0.36, mix=(0.61, 0.25, 0.14), pcp=6, hosp=False, pos=-0.0629),
]
CODES = [p["code"] for p in PRACTICES]
PMAP = {p["code"]: p for p in PRACTICES}
# each practice's 2026 movement in allowed amounts outside primary care visits, set by the tuning pass that places the
# golden figure, read from the cut pack, at each practice's target position (worst miss 0.0001)
MOVE = {"P01": 0.0190, "P02": -0.1154, "P03": 0.0633, "P04": 0.1428, "P05": -0.1290, "P06": -0.0854, "P07": -0.0684,
        "P08": 0.0547, "P09": 0.1291, "P10": -0.0594, "P11": 0.1493, "P12": 0.1931, "P13": -0.1497}

# E&M fee schedules (allowed, USD): established office visits 99211 to 99215 at the non-facility and facility rates,
# new-patient visits 99202 to 99205, preventive visits by age band (under 18, 18 to 39, 40 to 64)
EM = ("99211", "99212", "99213", "99214", "99215")
NEWPT = ("99202", "99203", "99204", "99205")
FEES = {
    ("B", 2025): dict(nf=(26.40, 57.10, 91.80, 129.90, 183.40), fa=(11.20, 38.60, 66.10, 98.70, 141.20),
                      new=(88.40, 131.70, 197.20, 258.80), prev=(141.60, 152.30, 167.80)),
    ("B", 2026): dict(nf=(27.10, 58.60, 92.60, 133.50, 188.40), fa=(11.50, 39.70, 67.90, 101.40, 145.10),
                      new=(90.80, 135.30, 202.60, 265.90), prev=(145.50, 156.50, 172.40)),
    ("M", 2025): dict(nf=(24.90, 54.80, 88.20, 125.10, 177.30), fa=(10.60, 37.10, 63.40, 95.20, 136.80),
                      new=(85.10, 126.90, 190.40, 249.70), prev=(136.20, 146.40, 161.30)),
    ("M", 2026): dict(nf=(25.60, 56.20, 90.50, 128.40, 181.90), fa=(10.90, 38.10, 65.10, 97.70, 140.40),
                      new=(87.30, 130.20, 195.40, 256.20), prev=(139.70, 150.20, 165.50)),
    ("T", 2025): dict(nf=(28.20, 60.40, 96.70, 136.80, 192.60), fa=(12.10, 41.30, 70.20, 104.10, 148.60),
                      new=(93.20, 138.80, 207.60, 272.50), prev=(149.80, 161.10, 177.50)),
    ("T", 2026): dict(nf=(29.00, 62.00, 99.30, 140.40, 197.70), fa=(12.40, 42.40, 72.00, 106.90, 152.50),
                      new=(95.70, 142.50, 213.10, 279.70), prev=(153.80, 165.40, 182.20)),
}
PREV_EST = ((0, "99391"), (1, "99392"), (5, "99393"), (12, "99394"), (18, "99395"), (40, "99396"))
QUALIFYING = set(EM) | set(NEWPT) | {c for _, c in PREV_EST} | {"99381", "99382", "99383", "99384", "99385", "99386"}
# Kesselcrest's E&M level review from 1 March 2026 pays a share of the level 5 claims at the level 4 rate; the claim
# keeps the code billed, and nothing on the feed marks the reviewed claims
LEVEL_REVIEW_FROM = D(2026, 3, 1)
LEVEL_REVIEW_SHARE = 0.37
CCF_RATE = {"B": 3.25, "M": 2.80, "T": 4.10}      # care coordination fee per attributed member per month, 2026
RUN_MONTHS = tuple(range(3, 11))                   # the 2026 interim runs, March to October
# claim columns, kept as parallel lists
COLS = ("cid", "pid", "year", "payer", "ctype", "svc", "end", "paid", "allowed", "code", "pos", "npi", "rev", "ndc",
        "days", "units", "mod")
# minor procedures a primary care clinician furnishes at a problem visit (code, Merrinlake 2026 non-facility allowed),
# the E&M then billed with modifier 25; Merrinlake allows an E&M billed with a same-day minor procedure at half its rate
MINOR_PROC = (("20610", 68.40), ("11102", 102.60), ("17110", 112.30), ("69210", 54.80), ("96372", 24.10), ("10060", 121.50),
              ("17000", 71.20), ("11200", 88.90))
MINOR_PROC_SHARE = 0.07
PROC_PAYER = {"B": 1.0, "M": 0.96, "T": 1.04}
MLH_MOD25_FACTOR = 0.5
SAME_DAY_PROBLEM_SHARE = 0.12       # a preventive visit with a problem addressed the same day (E&M with modifier 25)
MA_RATE = 6.50                      # Kesselcrest's Medicare Advantage care coordination fee a member a month, 2026


def rng(*k):
    """A generator seeded from fixed integers only (never Python's salted hash)."""
    s = SEED
    for x in k:
        s = (s * 1000003 + int(x)) % (2 ** 63)
    return np.random.default_rng(s)


def month_days(y, m):
    return (D(y + (m == 12), m % 12 + 1, 1) - D(y, m, 1)).days


def npi_check(nine):
    """An NPI: nine digits and the Luhn check digit over the prefix 80840 and those nine."""
    digits = "80840" + nine
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            d = d - 9 if d > 9 else d
        total += d
    return nine + str((10 - total % 10) % 10)


def clinicians():
    """The network's primary care clinicians by practice with effective dates: one P03 clinician moved to P06 on
    1 July 2025, and P10 added a clinician on 1 April 2026."""
    g = rng(7)
    rows = []
    base = 104017733
    for p in PRACTICES:
        spec = "208000000X" if p["kind"] == "PED" else ("207R00000X" if p["kind"] == "IM" else "207Q00000X")
        for k in range(p["pcp"]):
            base += int(g.integers(1100, 98000))
            rows.append(dict(npi=npi_check("1" + str(base)[-8:]), practice=p["code"], start=D(2018, 7, 1), end=None, spec=spec))
    mover = [r for r in rows if r["practice"] == "P03"][-1]
    mover["end"] = D(2025, 6, 30)
    rows.append(dict(npi=mover["npi"], practice="P06", start=D(2025, 7, 1), end=None, spec=mover["spec"]))
    base += 51133
    rows.append(dict(npi=npi_check("1" + str(base)[-8:]), practice="P10", start=D(2026, 4, 1), end=None, spec="207Q00000X"))
    return rows


def specialists():
    g = rng(8)
    out = []
    base = 113300402
    for _ in range(420):
        base += int(g.integers(900, 41000))
        out.append(npi_check("1" + str(base)[-8:]))
    return out


def npi_practice(clin, npi, day):
    for r in clin:
        if r["npi"] == npi and r["start"] <= day and (r["end"] is None or day <= r["end"]):
            return r["practice"]
    return None


class Person(object):
    __slots__ = ("pid", "practice", "second", "share2", "age", "sex", "chronic", "need", "annual", "am", "sick", "cvis",
                 "payer", "span", "drugs", "spec", "dob")


def people():
    """Every person in a practice's panel: the members who would be attributed to it once they had a visit."""
    out = []
    pid = 0
    for pi, p in enumerate(PRACTICES):
        g = rng(1, pi)
        for i in range(p["n"]):
            q = Person()
            pid += 1
            q.pid = pid
            q.practice = p["code"]
            q.second, q.share2 = None, 0.0
            if g.random() < 0.03:
                q.second = CODES[(pi + 1 + int(g.integers(0, 12))) % 13]
                q.share2 = float(g.uniform(0.25, 0.6))
            if p["kind"] == "PED":
                q.age = int(g.integers(1, 18))
            elif p["kind"] == "IM":
                q.age = int(min(64, 24 + g.gamma(5.0, 5.2)))
            else:
                q.age = int(g.integers(1, 18)) if g.random() < 0.27 else int(g.integers(18, 65))
            q.dob = D(2025 - q.age - 1, int(g.integers(1, 13)), int(g.integers(1, 29)))
            q.sex = "F" if g.random() < 0.51 else "M"
            agef = 0.35 if q.age < 18 else (0.7 if q.age < 40 else 1.35)
            q.chronic = bool(g.random() < min(0.9, p["chronic"] * agef / 0.95))
            base = g.lognormal(0.85, 0.65) if q.chronic else g.lognormal(-0.75, 0.85)
            q.need = float(base * p["need"] * (0.75 if q.age < 18 else 1.0))
            boost = 1.30 if p["camp"] >= 0.6 else 1.0
            q.annual = bool(g.random() < min(0.97, boost * (0.92 if q.chronic else (0.80 if q.age < 18 else 0.58))))
            r = g.random()
            if r < p["camp"]:
                q.am = int(g.integers(0, 3))
            elif r < p["camp"] + p["late"]:
                q.am = int(g.integers(9, 12))
            else:
                q.am = int(g.integers(0, 12))
            q.sick = float((0.95 if q.age < 18 else 0.32) * (1.0 + 0.4 * min(q.need, 3.0)))
            q.cvis = float(3.0 + 1.6 * min(q.need, 4.0)) if q.chronic else 0.0
            q.drugs = int(g.choice([1, 2], p=[0.6, 0.4])) if q.chronic else 0
            q.spec = bool(q.chronic and g.random() < 0.035)
            pay25 = PAYERS[int(g.choice(3, p=p["mix"]))]
            sw = g.random()
            if sw < 0.055:
                pay26 = PAYERS[(PAYERS.index(pay25) + 1 + int(g.integers(0, 2))) % 3]
            elif sw < 0.085:
                pay26 = None
            else:
                pay26 = pay25
            if g.random() < 0.075:
                pay25 = None
            q.payer = {2025: pay25, 2026: pay26}
            q.span = {}
            for y in YEARS:
                if q.payer[y] is None:
                    q.span[y] = None
                    continue
                u = g.random()
                if u < 0.06:
                    q.span[y] = (int(g.integers(1, 12)), 12)
                elif u < 0.12:
                    q.span[y] = (0, int(g.integers(1, 12)))
                else:
                    q.span[y] = (0, 12)
            out.append(q)
    return out


def lag_days(g, ctype, payer):
    mult = {"B": 1.0, "M": 1.22, "T": 0.86}[payer]
    if ctype == "RX":
        return int(g.integers(0, 2))
    if ctype == "PROF":
        return int(4 + mult * g.gamma(2.0, 6.5))
    if ctype == "OUTPT":
        return int(6 + mult * g.gamma(2.2, 10.0))
    return int(9 + mult * g.gamma(2.4, 15.0))


def em_level(g, need, chronic):
    w = np.array([0.02, 0.17, 0.46, 0.27, 0.08]) if not chronic else np.array([0.01, 0.07, 0.36, 0.40, 0.16])
    w = w * np.array([1.0, 1.0, 1.0, 1.0 + 0.10 * min(need, 4), 1.0 + 0.25 * min(need, 4)])
    return int(g.choice(5, p=w / w.sum()))


def visit_days(q, y, g, enr):
    """The person's primary care visits in year y as (date, kind), kind 'prev' or 'prob'."""
    out = []
    months = [m for m in range(12) if enr[m]]
    if not months:
        return out
    if q.annual and g.random() < 0.9:
        m = int(min(11, max(0, q.am + int(g.choice([-1, 0, 1], p=[0.2, 0.6, 0.2])))))
        if enr[m]:
            out.append((D(y, m + 1, int(g.integers(1, month_days(y, m + 1) + 1))), "prev"))
    sw = np.array([1.5, 1.4, 1.2, 1.0, 0.8, 0.7, 0.6, 0.7, 0.9, 1.1, 1.3, 1.5])[months]
    sw = sw / sw.sum()
    for _ in range(int(g.poisson(q.sick * len(months) / 12.0))):
        m = months[int(g.choice(len(months), p=sw))]
        out.append((D(y, m + 1, int(g.integers(1, month_days(y, m + 1) + 1))), "prob"))
    for _ in range(int(g.poisson(q.cvis * len(months) / 12.0))):
        m = months[int(g.integers(0, len(months)))]
        out.append((D(y, m + 1, int(g.integers(1, month_days(y, m + 1) + 1))), "prob"))
    return sorted(out)


def claims(ppl, clin, spec_npis):
    """Every claim of every person in both years, incurred January 2025 to December 2026, as parallel column lists."""
    col = {c: [] for c in COLS}
    cid = [700000000]
    rx_ndc = ("68180051301", "00093505898", "00378180110", "16714023401", "65862001090", "00591040810")

    def add(g, q, y, payer, ctype, svc, allowed, code="", pos="", npi="", rev="", ndc="", days=0, end=None, units=1, mod="",
            paid=None):
        cid[0] += int(1 + g.integers(0, 3))
        lag = svc + dt.timedelta(days=lag_days(g, ctype, payer))
        for k, v in (("cid", cid[0]), ("pid", q.pid), ("year", y), ("payer", payer), ("ctype", ctype), ("svc", svc),
                     ("end", end or svc), ("paid", paid or lag),
                     ("allowed", round(float(allowed), 2)), ("code", code), ("pos", pos), ("npi", npi), ("rev", rev),
                     ("ndc", ndc), ("days", days), ("units", units), ("mod", mod)):
            col[k].append(v)

    for q in ppl:
        for y in YEARS:
            payer = q.payer[y]
            if payer is None:
                continue
            g = rng(11, q.pid, y)
            g2 = rng(12, q.pid, y)
            s, e = q.span[y]
            enr = [s <= m < e for m in range(12)]
            mult = 1.0 if y == 2025 else 1.0 + MOVE[q.practice]
            fee = FEES[(payer, y)]
            age = q.age + (y - 2025)
            for (day, kind) in visit_days(q, y, g, enr):
                prac = q.second if (q.second and g.random() < q.share2) else q.practice
                npis = [r["npi"] for r in clin if r["practice"] == prac and r["start"] <= day and (r["end"] is None or day <= r["end"])]
                npi = npis[int(g.integers(0, len(npis)))]
                hosp = PMAP[prac]["hosp"]
                tele = kind == "prob" and g.random() < 0.11
                pos = "10" if tele and (hosp or g.random() < 0.7) else ("02" if tele else ("22" if hosp else "11"))
                if kind == "prev":
                    code = [c for a, c in PREV_EST if age >= a][-1]
                    allowed = fee["prev"][0 if age < 18 else (1 if age < 40 else 2)] * (0.86 if pos == "22" else 1.0)
                else:
                    lv = em_level(g, q.need, q.chronic)
                    if lv == 0 and pos in ("02", "10"):
                        lv = 1
                    code = EM[lv]
                    rate = fee["fa"] if (pos in ("22", "19") or (payer == "T" and pos in ("02", "10"))) else fee["nf"]
                    paid_lv = lv
                    if payer == "M" and lv == 4 and day >= LEVEL_REVIEW_FROM and g.random() < LEVEL_REVIEW_SHARE:
                        paid_lv = 3
                    allowed = rate[paid_lv]
                proc = None
                mod = "95" if pos in ("02", "10") else ""
                if kind == "prob" and not mod and g2.random() < MINOR_PROC_SHARE:
                    proc = MINOR_PROC[int(g2.integers(0, len(MINOR_PROC)))]
                    mod = "25"
                    if payer == "B":
                        allowed = round(allowed * MLH_MOD25_FACTOR, 2)
                add(g, q, y, payer, "PROF", day, allowed, code=code, pos=pos, npi=npi, mod=mod)
                if proc:   # billed with the visit, so adjudicated and paid with it
                    add(g2, q, y, payer, "PROF", day, proc[1] * PROC_PAYER[payer] * (0.82 if pos == "22" else 1.0), code=proc[0],
                        pos=pos, npi=npi, paid=col["paid"][-1])
                elif kind == "prev" and g2.random() < SAME_DAY_PROBLEM_SHARE:
                    lv = int(g2.choice([1, 2, 3], p=[0.25, 0.55, 0.20]))
                    rate = fee["fa"] if pos in ("22", "19") else fee["nf"]
                    add(g2, q, y, payer, "PROF", day, rate[lv], code=EM[lv], pos=pos, npi=npi, mod="25")
                if hosp and pos == "22":
                    add(g, q, y, payer, "OUTPT", day, g.lognormal(math.log(118.0), 0.18), rev="0510")
                if kind == "prob" and g.random() < 0.45:
                    add(g, q, y, payer, "RX", day + dt.timedelta(days=int(g.integers(0, 2))), mult * g.lognormal(math.log(19.0), 0.6),
                        ndc=rx_ndc[int(g.integers(0, 6))], days=10)
            h = q.need
            for m in range(12):
                if not enr[m]:
                    continue
                nd = month_days(y, m + 1)
                for _ in range(int(g.poisson(0.03 + 0.15 * h))):
                    if g.random() < 0.35:
                        lv = em_level(g, h, q.chronic)
                        add(g, q, y, payer, "PROF", D(y, m + 1, int(g.integers(1, nd + 1))), fee["nf"][lv] * 1.12,
                            code=EM[lv], pos="11", npi=spec_npis[int(g.integers(0, len(spec_npis)))])
                    else:
                        add(g, q, y, payer, "PROF", D(y, m + 1, int(g.integers(1, nd + 1))), mult * g.lognormal(math.log(160.0), 0.95),
                            code=("71046", "80053", "85025", "93000", "20610", "45378", "88305", "97110", "76700", "36415")[int(g.integers(0, 10))],
                            pos=("11", "22", "19", "81")[int(g.integers(0, 4))], npi=spec_npis[int(g.integers(0, len(spec_npis)))])
                for _ in range(int(g.poisson(0.012 + 0.045 * h))):
                    add(g, q, y, payer, "OUTPT", D(y, m + 1, int(g.integers(1, nd + 1))), mult * g.lognormal(math.log(1030.0), 1.05),
                        rev=("0450", "0320", "0300", "0360", "0610", "0250", "0730")[int(g.integers(0, 7))])
                if g.random() < 0.0012 + 0.0042 * h:
                    st = D(y, m + 1, int(g.integers(1, nd + 1)))
                    los = int(1 + g.gamma(1.6, 2.2))
                    add(g, q, y, payer, "INPT", st, mult * g.lognormal(math.log(19500.0), 0.75), rev="0120", days=los,
                        end=st + dt.timedelta(days=los))
                for k in range(q.drugs):
                    per90 = (q.pid + k) % 10 < 7
                    if per90 and m % 3 != (q.pid + k) % 3:
                        continue
                    mo = 3 if per90 else 1
                    add(g, q, y, payer, "RX", D(y, m + 1, int(min(nd, 1 + (q.pid * 7 + k * 11) % 28))),
                        mult * mo * g.lognormal(math.log(58.0), 0.9), ndc=rx_ndc[(q.pid + 2 * k) % 6], days=30 * mo, units=30 * mo)
                if q.spec:
                    add(g, q, y, payer, "RX", D(y, m + 1, int(min(nd, 3 + q.pid % 25))), mult * g.lognormal(math.log(5600.0), 0.15),
                        ndc="00074433906", days=28, units=2)
    return col


_QIDX = {}


def qualifying_index(col):
    key = id(col)
    if key not in _QIDX:
        ct, code = col["ctype"], col["code"]
        _QIDX.clear()
        _QIDX[key] = [i for i in range(len(ct)) if ct[i] == "PROF" and code[i] in QUALIFYING]
    return _QIDX[key]


def attribute(col, clin, payer, year, svc_to, paid_to):
    """One payer's attribution run: each of its members with a qualifying primary care service from a network clinician,
    incurred in the year through svc_to and paid by paid_to, goes to the practice with the most qualifying days, ties to
    the practice of the latest such day. Returns {pid: (practice, days, last_day)}."""
    days = {}
    pay, yr, ct, code, npi, svc, paid, pid = (col["payer"], col["year"], col["ctype"], col["code"], col["npi"], col["svc"],
                                              col["paid"], col["pid"])
    pmap_cache = {}
    for i in qualifying_index(col):
        if pay[i] != payer or yr[i] != year:
            continue
        if svc[i] > svc_to or paid[i] > paid_to:
            continue
        key = (npi[i], svc[i])
        if key not in pmap_cache:
            pmap_cache[key] = npi_practice(clin, npi[i], svc[i])
        pr = pmap_cache[key]
        if pr is None:
            continue
        days.setdefault(pid[i], {}).setdefault(pr, set()).add(svc[i])
    out = {}
    for p, byp in days.items():
        best = sorted(byp.items(), key=lambda kv: (-len(kv[1]), -max(kv[1]).toordinal(), kv[0]))[0]
        out[p] = (best[0], len(best[1]), max(best[1]))
    return out


def build():
    ppl = people()
    clin = clinicians()
    spec = specialists()
    col = claims(ppl, clin, spec)
    att = {}
    for payer in PAYERS:
        att[("final", payer, 2025)] = attribute(col, clin, payer, 2025, D(2025, 12, 31), FINAL_PAID[2025])
        att[("aug", payer, 2025)] = attribute(col, clin, payer, 2025, D(2025, 8, 31), D(2025, 9, 30))
        att[("augany", payer, 2025)] = attribute(col, clin, payer, 2025, D(2025, 8, 31), FINAL_PAID[2025])
        att[("final", payer, 2026)] = attribute(col, clin, payer, 2026, D(2026, 12, 31), FINAL_PAID[2026])
        for k in RUN_MONTHS:
            cut = D(2026, k - 2, month_days(2026, k - 2)) if k > 2 else D(2025, 12, 31)
            pcut = D(2026, k - 1, month_days(2026, k - 1))
            att[("run", payer, k)] = attribute(col, clin, payer, 2026, cut, pcut)
    return dict(people=ppl, claims=col, clinicians=clin, specialists=spec, att=att)


def enrolled_months(q, y, upto=12):
    if q.span.get(y) is None:
        return 0
    s, e = q.span[y]
    return max(0, min(e, upto) - s)


# ---- names, people and identifiers of the fiction ----
NETWORK = "Larrowbrook Physician Network"
NETWORK_SHORT = "Larrowbrook"
PAYER_NAMES = {"B": "Merrinlake Health Plan", "M": "Kesselcrest Benefit Partners", "T": "Pemberglen Mutual Health"}
PRACTICE_NAMES = {
    "P01": "Ostrelwood Internal Medicine", "P02": "Callowglen Family Practice", "P03": "Thornelfield Family Medicine",
    "P04": "Haddelcrest Internal Medicine", "P05": "Birrelhaven Children's Clinic", "P06": "Raddelview Family Physicians",
    "P07": "Jesselford Family Medicine", "P08": "Nerrincreek Family Practice", "P09": "Wexelmoor Internal Medicine",
    "P10": "Torrinridge Family Medicine", "P11": "Mallowcrest Pediatrics", "P12": "Prestelglen Internal Medicine",
    "P13": "Garrowdale Family Practice"}
PEOPLE = {"president": "Andre O'Connor", "analytics": "Joel Brewer", "payer": "Carlos Howard"}
TINS = {c: "39-%07d" % (1184402 + 37717 * i) for i, c in enumerate(CODES)}


def member_ids(ppl):
    """Each payer's member identifier for each person it covers; a person who changes payer gets the new payer's."""
    g = rng(21)
    ids = {}
    used = set()
    for q in ppl:
        for y in YEARS:
            payer = q.payer[y]
            if payer is None or (q.pid, payer) in ids:
                continue
            while True:
                if payer == "B":
                    v = "MLH%08d" % int(g.integers(10000000, 99999999))
                elif payer == "M":
                    v = "K%09d" % int(g.integers(100000000, 999999999))
                else:
                    v = "PG-%06d-%02d" % (int(g.integers(100000, 999999)), int(g.integers(1, 5)))
                if v not in used:
                    used.add(v)
                    break
            ids[(q.pid, payer)] = v
    return ids


def completion_factors(col):
    """Each payer's completion of 2025 allowed by incurred month when paid through 30 September 2025 against paid
    through 31 March 2026, the lag study the payers apply to their September-paid interim files."""
    out = {}
    pay, yr, svc, paid, amt = col["payer"], col["year"], col["svc"], col["paid"], col["allowed"]
    for payer in PAYERS:
        num = [0.0] * 12
        den = [0.0] * 12
        for i in range(len(pay)):
            if pay[i] != payer or yr[i] != 2025 or paid[i] > FINAL_PAID[2025]:
                continue
            m = svc[i].month - 1
            den[m] += amt[i]
            if paid[i] <= D(2025, 9, 30):
                num[m] += amt[i]
        out[payer] = [round(num[m] / den[m], 3) if den[m] else 1.0 for m in range(8)]
    return out


def remittances(w):
    """The care coordination fees each payer paid on its 2026 interim runs, March to October: on each run, the fee for
    the run's month for every member on it enrolled that month, and for a member on the run for the first time the fees
    for the year's earlier months the member was enrolled. Lines are by payer, run, practice, coverage month and type."""
    ppl = {q.pid: q for q in w["people"]}
    att = w["att"]
    lines = []
    for payer in PAYERS:
        seen = set()
        for k in RUN_MONTHS:
            run = att[("run", payer, k)]
            agg = {}
            for pid, (prac, nd, last) in run.items():
                q = ppl[pid]
                s, e = q.span[2026]
                if s <= k - 1 < e:
                    agg[(prac, k, "CURRENT")] = agg.get((prac, k, "CURRENT"), 0) + 1
                if pid not in seen:
                    for m in range(1, k):
                        if s <= m - 1 < e:
                            agg[(prac, m, "CATCHUP")] = agg.get((prac, m, "CATCHUP"), 0) + 1
            seen.update(run.keys())
            for (prac, m, typ), n in sorted(agg.items()):
                lines.append(dict(payer=payer, run=k, practice=prac, cov=m, type=typ, members=n,
                                  amount=round(n * CCF_RATE[payer], 2)))
    # Kesselcrest pays its Medicare Advantage care coordination fee to the same practice TINs each month, from January,
    # on its prospective MA attribution
    ma = ma_members()
    for m in range(1, max(RUN_MONTHS) + 1):
        for c in CODES:
            n = sum(1 for r in ma if r["practice"] == c and r["start"].month <= m)
            if n:
                lines.append(dict(payer="M", run=m, practice=c, cov=m, type="MA", members=n, amount=round(n * MA_RATE, 2)))
    return lines


def ma_members():
    """Kesselcrest's Medicare Advantage members attributed to the network's adult and family practices for 2026 (its
    quarterly refresh of 15 July): member number, plan, practice, attribution start, risk score, E&M visits."""
    g = rng(45)
    used = set()
    rows = []
    for c in CODES:
        pr = PMAP[c]
        if pr["kind"] == "PED":
            continue
        for _ in range(int(g.poisson(pr["n"] * (0.16 if pr["kind"] == "IM" else 0.09)))):
            while True:
                mid = "KMA%08d" % int(g.integers(10000000, 99999999))
                if mid not in used:
                    used.add(mid)
                    break
            start = D(2026, 1, 1) if g.random() < 0.83 else D(2026, int(g.integers(2, 8)), 1)
            rows.append(dict(mid=mid, plan=("KBP Medicare Advantage HMO", "KBP Medicare Advantage PPO")[int(g.random() < 0.38)],
                             practice=c, start=start, raf=round(float(g.lognormal(math.log(1.02), 0.42)), 3),
                             visits=int(1 + g.poisson(3.4))))
    return rows


# ---- 2025 quality measures (the payers' settlement quality gate; not part of the network measure) ----
# measure: code, name, commercial median rate, eligible share of an adult (or child) panel
QUALITY_MEASURES = {
    "adult": (("BCS-E", "Breast Cancer Screening", 0.74, 0.10), ("COL-E", "Colorectal Cancer Screening", 0.63, 0.30),
              ("CBP", "Controlling High Blood Pressure", 0.66, 0.11), ("GSD", "Glycemic Status Assessment, <8.0%", 0.61, 0.07),
              ("CCS-E", "Cervical Cancer Screening", 0.72, 0.25)),
    "child": (("CIS-E", "Childhood Immunization Status, Combination 10", 0.41, 0.05),
              ("IMA-E", "Immunizations for Adolescents, Combination 2", 0.36, 0.05),
              ("WCV", "Child and Adolescent Well-Care Visits", 0.57, 0.85), ("W30", "Well-Child Visits in the First 30 Months", 0.71, 0.08)),
}
QUALITY_TARGET = {"B": -0.020, "M": -0.010, "T": -0.025}     # each payer's target against the commercial median


def quality_table():
    """Rows of (payer, practice, code, name, denominator, numerator, target) for 2025, each payer scoring the measures
    its contract carries for the practice's panel (adult measures for internal medicine, child measures for paediatrics,
    both for family medicine) where the denominator reaches 12."""
    g = rng(53)
    skill = {c: float(g.normal(0.0, 0.05)) for c in CODES}
    rows = []
    for payer in PAYERS:
        for c in CODES:
            pr = PMAP[c]
            sets = {"IM": (("adult", 1.0),), "PED": (("child", 1.0),), "FM": (("adult", 0.7), ("child", 0.3))}[pr["kind"]]
            members = pr["n"] * pr["mix"][PAYERS.index(payer)]
            for s, share in sets:
                for code, name, median, elig in QUALITY_MEASURES[s]:
                    den = int(g.poisson(members * elig * share * 0.9))
                    if den < 12:
                        continue
                    p = min(0.97, max(0.05, median + skill[c] + float(g.normal(0.0, 0.03))))
                    num = int(g.binomial(den, p))
                    rows.append((payer, c, code, name, den, num, round(median + QUALITY_TARGET[payer], 3)))
    return rows


def quality_multipliers():
    """Each payer's 2025 quality multiplier by practice: 1.00 where every scored measure meets its target, 0.95 where
    three quarters or more do, 0.90 where half or more do, else 0.85."""
    met = {}
    for payer, c, code, name, den, num, target in quality_table():
        m = met.setdefault((payer, c), [0, 0])
        m[0] += int(num / den >= target)
        m[1] += 1
    out = {}
    for k, (a, b) in met.items():
        share = a / b
        out[k] = 1.0 if a == b else 0.95 if share >= 0.75 else 0.90 if share >= 0.5 else 0.85
    return out
