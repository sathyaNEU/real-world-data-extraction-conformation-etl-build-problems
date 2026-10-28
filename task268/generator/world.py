"""The clean truth for task268: every patient the Heronmere Heart Failure Registry enrolled from 2022 to 2025, their
heart failure course a quarter at a time (NYHA class, death), the clinic visits that record it, the moves out of
Florida reported at those visits, the deaths each source can see, Wrenhaven's 2024 re-consent, the 2025 re-enrolments
after the record-number migration, and the hospitals' 2025 NT-proBNP results with the corrections the laboratory
system re-accessions. Each part draws from its own random stream so a change to one leaves the others where they were.

Days are counted from 1 January 2022 (day 0)."""
import datetime as dt

import numpy as np

import common as K

SEED = 273
DAY0 = dt.date(2022, 1, 1)
Q = 91                                   # a quarter, the clinic's visit interval in days
EXTRACT_DAY = (K.EXTRACT - DAY0).days
DEATHS_DAY = (K.DEATHS_TO - DAY0).days
RECONSENT_DAY = (K.RECONSENT - DAY0).days
MIGRATION_DAY = (K.MIGRATION - DAY0).days
SPLIT_DAY = (K.SPLIT - DAY0).days

# the course of heart failure a quarter at a time: class transitions and the chance of dying within the quarter,
# by the class at its start
T0 = np.array([[0.90, 0.09, 0.01, 0.00],
               [0.03, 0.88, 0.08, 0.01],
               [0.00, 0.04, 0.86, 0.10],
               [0.00, 0.00, 0.02, 0.98]])
D0 = np.array([0.008, 0.018, 0.050, 0.180])
# Gullhaven's patients are older and mostly diagnosed in class I or II, then worsen faster; in a given class every
# hospital's patients die at the same rate
WORSEN = {"GUL": 3.0}
MIX = {"FEN": (0.10, 0.36, 0.40, 0.14), "LIN": (0.22, 0.46, 0.26, 0.06), "BRE": (0.16, 0.42, 0.32, 0.10),
       "GUL": (0.30, 0.55, 0.13, 0.02), "WRE": (0.14, 0.40, 0.33, 0.13)}
PER_YEAR = {"FEN": 800, "LIN": 750, "BRE": 760, "GUL": 1500, "WRE": 850}
GROWTH = {2022: 1.0, 2023: 1.0, 2024: 1.02, 2025: 1.04}   # new diagnoses rise a little each year from 2024
AGE = {"FEN": (69, 12), "LIN": (72, 10), "BRE": (73, 10), "GUL": (79, 7), "WRE": (71, 11)}
# a move out of Florida reported at a clinic visit: north, beyond the death linkage, by a logistic in the hospital and
# the class recorded at that visit; or to a state the exchange covers, mostly while well
NORTH_A = {"GUL": -5.9}
NORTH_A_OTHER = -9.6
NORTH_B = np.array([0.0, 0.3, 0.6, 4.3])
EXCH = {"GUL": (0.030, 0.020, 0.005, 0.002)}
EXCH_OTHER = (0.004, 0.003, 0.001, 0.0)
RECONSENT_LOST = 0.90                    # Wrenhaven's patients who did not return the new consent form
MISSED_VISIT = 0.04


def expit(x):
    return 1.0 / (1.0 + np.exp(-x))


def matrices(h):
    T = T0.copy()
    w = WORSEN.get(h, 1.0)
    for a in range(4):
        T[a, a + 1:] *= w
        T[a, a] = 1.0 - T[a].sum() + T[a, a]
    return T, D0.copy()


def north_p(h):
    return expit(NORTH_A.get(h, NORTH_A_OTHER) + NORTH_B)


def exch_p(h):
    return np.array(EXCH.get(h, EXCH_OTHER))


def year_days(y):
    a = (dt.date(y, 1, 1) - DAY0).days
    return a, (dt.date(y, 12, 31) - DAY0).days


def diagnosis_days(r, n, y):
    """Diagnosis dates over a year, a little heavier in the winter months."""
    a, b = year_days(y)
    span = b - a + 1
    out = []
    while len(out) < n:
        d = r.integers(0, span, 2 * n)
        doy = d / span
        keep = r.random(2 * n) < 0.82 + 0.18 * np.cos(2 * np.pi * doy)
        out.extend((a + d[keep]).tolist())
    return np.array(sorted(out[:n]), dtype=int)


def course(r, h, dx):
    """The quarter-by-quarter course of each patient from diagnosis: clinic visits about every 91 days (day 0 is the
    diagnosis), the class recorded at each visit, death at a uniform time between two visits with the chance set by
    the class at the earlier one, and the moves reported at visits."""
    n = len(dx)
    T, D = matrices(h)
    npn, epn = north_p(h), exch_p(h)
    kmax = (EXTRACT_DAY - int(dx.min())) // Q + 2
    jit = r.integers(-10, 11, size=(n, kmax + 1))
    jit[:, 0] = 0
    vday = dx[:, None] + np.arange(kmax + 1)[None, :] * Q + jit
    cls = np.full((n, kmax + 1), -1, dtype=int)
    cls[:, 0] = r.choice(4, size=n, p=MIX[h])
    death = np.full(n, -1, dtype=int)
    north = np.full(n, -1, dtype=int)
    exch = np.full(n, -1, dtype=int)
    vatt = np.zeros((n, kmax + 1), dtype=bool)
    vatt[:, 0] = True
    alive = np.ones(n, dtype=bool)
    infl = np.ones(n, dtype=bool)
    u_d, u_t, u_m, u_v, u_w = (r.random((n, kmax + 1)) for _ in range(5))
    cum = np.cumsum(T, axis=1)
    for k in range(1, kmax + 1):
        a, b = vday[:, k - 1], vday[:, k]
        c = np.clip(cls[:, k - 1], 0, 3)
        live = alive & (a <= EXTRACT_DAY + Q)
        dies = live & (u_d[:, k] < D[c])
        death[dies] = a[dies] + 1 + (u_w[:, k][dies] * (b - a)[dies] - 1).clip(0).astype(int)
        alive &= ~dies
        live &= ~dies
        nxt = (u_t[:, k][:, None] > cum[c]).sum(axis=1)
        cls[live, k] = nxt[live]
        at = live & infl & (b <= EXTRACT_DAY) & (u_v[:, k] >= MISSED_VISIT)
        vatt[:, k] = at
        cc = np.clip(cls[:, k], 0, 3)
        um = u_m[:, k]
        go_n = at & (um < npn[cc])
        go_e = at & ~go_n & (um < npn[cc] + epn[cc])
        north[go_n] = b[go_n]
        exch[go_e] = b[go_e]
        infl &= ~(go_n | go_e)
    return dict(c0=cls[:, 0], cls=cls, death=death, north=north, exch=exch, vday=vday, vatt=vatt)


def build(seed=SEED):
    """The registry's patients, enrolment by enrolment, with their course."""
    W = dict(seed=seed, patients=[])
    seq = {}
    for y in K.YEARS_ENROLLED:
        for hi, h in enumerate(K.CODES):
            r = np.random.default_rng([seed, y, hi, 1])
            n = int(round(PER_YEAR[h] * GROWTH[y])) + int(r.integers(-25, 26))
            dx = diagnosis_days(r, n, y)
            C = course(r, h, dx)
            am, asd = AGE[h]
            x = r.normal(am, asd, n)
            x = np.where(x > 96, 96 + 0.45 * (x - 96), np.where(x < 40, 40 - 0.5 * (40 - x), x))   # thinner tails
            ages = np.clip(np.round(x), 24, 108).astype(int)
            sex = np.where(r.random(n) < (0.46 if h == "GUL" else 0.43), "F", "M")
            ef = r.choice(["HFrEF", "HFmrEF", "HFpEF"], size=n, p=(0.42, 0.18, 0.40))
            setting = r.choice(["Inpatient", "Outpatient", "Emergency department"], size=n, p=(0.58, 0.32, 0.10))
            lag = r.integers(0, 21, n)
            sat = (h == "BRE") & (r.random(n) < 0.35)          # diagnosed at Brenmoor's north campus
            for i in range(n):
                seq[y] = seq.get(y, 0) + 1
                W["patients"].append(dict(
                    rid="HF%02d-%05d" % (y % 100, seq[y]), year=y, hosp=h, sat=bool(sat[i]), dx=int(dx[i]),
                    enrol=int(dx[i] + lag[i]), age=int(ages[i]), sex=str(sex[i]), ef=str(ef[i]), setting=str(setting[i]),
                    c0=int(C["c0"][i]), cls=C["cls"][i], death=int(C["death"][i]), north=int(C["north"][i]),
                    exch=int(C["exch"][i]), vday=C["vday"][i], vatt=C["vatt"][i], wd=-1, reenrol=None))
    reconsent(W, seed)
    numbers(W, seed)
    reenrolments(W, seed)
    problem_list(W, seed)
    recorded(W, seed)
    W["lab"] = lab_results(W, seed)
    return W


def reconsent(W, seed):
    """Wrenhaven re-consented its patients enrolled before 2024; those who had not returned the form by the deadline
    (common.RECONSENT) left the registry's follow-up that day, at random."""
    r = np.random.default_rng([seed, 7])
    for p in W["patients"]:
        if p["hosp"] != "WRE" or p["year"] >= 2024:
            continue
        alive = p["death"] < 0 or p["death"] > RECONSENT_DAY
        followed = p["north"] < 0 or p["north"] > RECONSENT_DAY
        u = r.random()
        if alive and followed and u < RECONSENT_LOST:
            p["wd"] = RECONSENT_DAY


def numbers(W, seed):
    """Record numbers: a legacy number for everyone the system knew before the June 2024 migration, a new number for
    everyone from it; the crosswalk maps one to the other."""
    r = np.random.default_rng([seed, 11])
    used_l, used_n = set(), set()

    def legacy():
        while True:
            x = "H%07d" % r.integers(100000, 9999999)
            if x not in used_l:
                used_l.add(x)
                return x

    def new():
        while True:
            x = "10%08d" % r.integers(10000000, 99999999)
            if x not in used_n:
                used_n.add(x)
                return x
    W["xwalk"] = []
    for p in W["patients"]:
        p["mrn_new"] = new()
        known_before = p["enrol"] < MIGRATION_DAY or r.random() < 0.72
        p["mrn_legacy"] = legacy() if known_before else None
        if p["mrn_legacy"]:
            W["xwalk"].append((p["mrn_legacy"], p["mrn_new"]))
    # other patients of the system in the crosswalk extract the registry team holds (anyone with a 2022 to 2024
    # encounter at a cardiology or medicine service)
    W["others"] = []
    for _ in range(26000):
        a, b = legacy(), new()
        W["xwalk"].append((a, b))
        W["others"].append(b)
    W["new_numbers"] = used_n


def reenrolments(W, seed):
    """After the migration, a 2022 or 2023 patient still under the clinic who is seen again with heart failure in 2025
    is sometimes enrolled afresh under the new record number: a second enrolment for a patient not newly diagnosed.
    Only patients past their two-year date and never lost to a move or the re-consent."""
    r = np.random.default_rng([seed, 13])
    seq = max(int(p["rid"][5:]) for p in W["patients"] if p["year"] == 2025)
    add = []
    for h in K.CODES:
        pool = [p for p in W["patients"] if p["hosp"] == h and p["year"] in (2022, 2023) and p["north"] < 0
                and p["exch"] < 0 and p["wd"] < 0]
        a, b = year_days(2025)
        cands = []
        for p in pool:
            dxd = DAY0 + dt.timedelta(days=p["dx"])
            two = (dt.date(dxd.year + 2, dxd.month, dxd.day) - DAY0).days
            lo = max(a, two + 30)
            top = b if p["death"] < 0 else min(b, p["death"] - 5)
            if top - lo > 20:
                cands.append((p, lo, top))
        m = int(r.integers(15, 41))
        pick = r.choice(len(cands), size=m, replace=False)
        for j in sorted(pick):
            p, lo, top = cands[j]
            d = int(r.integers(lo, top))
            seq += 1
            setting = "Inpatient" if r.random() < 0.66 else ("Emergency department" if r.random() < 0.3 else "Outpatient")
            q = dict(rid="HF25-%05d" % seq, year=2025, hosp=h, sat=p["sat"], dx=d, enrol=d + int(r.integers(0, 15)),
                     age=p["age"] + (d - p["dx"]) // 365, sex=p["sex"], ef=p["ef"], setting=setting,
                     c0=int(p["cls"][min(len(p["cls"]) - 1, (d - p["dx"]) // Q)]), cls=None, death=-1, north=-1,
                     exch=-1, vday=None, vatt=None, wd=-1, reenrol=p["rid"], mrn_new=p["mrn_new"], mrn_legacy=None)
            p["reenrolled_as"] = q["rid"]
            p["reenrol_day"] = d
            add.append(q)
    W["patients"].extend(add)


def recorded(W, seed):
    """The registry records a relocation when it processes the note of the visit at which the patient said so, one to
    four days after the visit."""
    r = np.random.default_rng([seed, 29])
    for p in W["patients"]:
        lag = int(r.integers(1, 5))
        p["north_rec"] = p["north"] + lag if p["north"] >= 0 else -1
        p["exch_rec"] = p["exch"] + lag if p["exch"] >= 0 else -1


def problem_list(W, seed):
    """Between the registry module's November 2024 update and the February 2025 release that fixed it, a new
    enrolment's diagnosis date was overwritten with the date of the heart failure entry on the patient's problem list
    when that entry was added after the registry nurse had enrolled the patient, so the record shows a diagnosis date
    after the enrolment date; an entry added after the fix overwrote nothing. Enrolments of patients diagnosed the
    year before, and January's enrolments, are left as entered."""
    r = np.random.default_rng([seed, 19])
    lo, hi = (K.MODULE_UPDATE - DAY0).days, (K.MODULE_FIX - DAY0).days
    for p in W["patients"]:
        if not (lo <= p["enrol"] < hi) or p["reenrol"] is not None:
            continue
        u, lag = r.random(), int(r.integers(3, 41))
        e = DAY0 + dt.timedelta(days=p["enrol"])
        d = DAY0 + dt.timedelta(days=p["dx"])
        alive = p["death"] < 0 or p["death"] > p["enrol"] + lag
        if u < 0.35 and alive and p["enrol"] + lag < hi and d.year == e.year and e.month != 1:
            p["dx_shown"] = p["enrol"] + lag


def shown(v):
    """The result as the analyser reports it: a whole number within its range, text outside it."""
    return ">35000" if v >= 35000 else ("<35" if v < 35 else int(round(v)))


def lab_results(W, seed):
    """Each hospital laboratory's NT-proBNP results released in the export window, with genuine same-day second
    specimens and the corrections the laboratory system re-accessions (a new accession, the same patient and collection
    time, released later, both rows final)."""
    r = np.random.default_rng([seed, 17])
    rr = np.random.default_rng([seed, 23])
    a, b = (K.LAB_FROM - DAY0).days, (K.LAB_TO - DAY0).days
    reg = [p for p in W["patients"] if p["cls"] is not None]

    def here(p, day):
        """Alive and still in the hospitals' reach on the day the specimen was collected."""
        return not any(0 <= x <= day for x in (p["death"], p["north"], p["exch"]))
    per_lab = {"FEN": 10400, "LIN": 8170, "BRE": 8800, "GUL": 11640, "WRE": 9300}
    rows = []
    others = W["others"]
    for h in K.CODES:
        mine = [p for p in reg if p["hosp"] == h]
        n = per_lab[h] + int(r.integers(-200, 201))
        # collection times across the window and the days either side of it
        days = r.integers(a - 3, b - 2, n)
        mins = r.integers(0, 1440, n)
        for i in range(n):
            p = None
            if r.random() < 0.30 and mine:
                p = mine[int(r.integers(0, len(mine)))]
                mrn = p["mrn_new"]
                base = 7.3 + 0.5 * p["c0"]
            else:
                mrn = others[int(r.integers(0, len(others)))]
                base = 6.1
            v = float(np.exp(r.normal(base, 1.25)))
            col = int(days[i]) * 1440 + int(mins[i])
            if p is not None and not here(p, col // 1440):
                mrn = others[int(rr.integers(0, len(others)))]      # the specimen is another patient's
            rec = col + int(r.integers(8, 90))
            rel = rec + int(r.integers(35, 300))
            loc = r.choice(["ED", "INPT", "OUTPT", "PCN"], p=(0.36, 0.30, 0.20, 0.14))
            rows.append(dict(lab=h, acc=None, mrn=mrn, col=col, rec=rec, rel=rel, val=v, loc=str(loc), kind="result",
                             sat=(h == "BRE" and r.random() < 0.3)))
            if r.random() < 0.028:                       # a genuine second specimen the same day, hours later
                col2 = col + int(r.integers(180, 720))
                rows.append(dict(lab=h, acc=None, mrn=mrn, col=col2, rec=col2 + 30, rel=col2 + 30 + int(r.integers(35, 300)),
                                 val=float(v * np.exp(r.normal(0, 0.25))), loc=str(loc), kind="repeat", sat=rows[-1]["sat"]))
    # corrections: a released result corrected after release, re-accessioned
    rows.sort(key=lambda x: (x["lab"], x["rel"], x["col"], x["mrn"]))
    out = []
    corrections = []
    for h in K.CODES:
        mine = [x for x in rows if x["lab"] == h and a * 1440 <= x["rel"] < (a + 360) * 1440 and x["kind"] == "result"]
        m = int(r.integers(34, 82))
        pick = r.choice(len(mine), size=m, replace=False)
        for j in pick:
            x = mine[int(j)]
            kind = r.random()
            if kind < 0.45:                           # a value keyed with a slipped decimal, mostly a dropped point
                v2 = x["val"] * (0.1 if r.random() < 0.85 else 10.0)
            else:                                     # a re-run after a flagged specimen
                v2 = x["val"] * float(np.exp(r.normal(0, 0.6)))
            rel2 = x["rel"] + int(r.integers(180, 4300))
            if shown(v2) == shown(x["val"]):          # a re-run that reports the same result is not a correction
                continue
            if (v2 >= K.REFERRAL - 0.5) != (x["val"] >= K.REFERRAL - 0.5):
                continue                              # the corrections kept here never move a result across the referral level
            corrections.append(dict(lab=h, acc=None, mrn=x["mrn"], col=x["col"], rec=x["rec"],
                                    rel=rel2, val=v2, loc=x["loc"], kind="correction",
                                    sat=x["sat"]))
    allrows = rows + corrections
    for x in allrows:
        x["acc_at"] = x["rec"] if x["kind"] != "correction" else x["rel"] - int(r.integers(10, 40))
    allrows.sort(key=lambda x: (x["lab"], x["acc_at"]))
    for h in K.CODES:
        nxt = int(r.integers(1000000, 1900000))
        for x in allrows:
            if x["lab"] == h:
                nxt += int(r.integers(1, 4))
                x["acc"] = nxt
    by_old = {}
    for x in allrows:
        if x["kind"] != "correction":
            by_old[(x["lab"], x["mrn"], x["col"])] = x["acc"]
    for x in allrows:
        if x["kind"] == "correction":
            x["corrects"] = by_old[(x["lab"], x["mrn"], x["col"])]
    keep = [x for x in allrows if a * 1440 <= x["rel"] <= (b + 1) * 1440 - 1]
    keep.sort(key=lambda x: (x["rel"], x["lab"], x["acc"]))
    return keep
