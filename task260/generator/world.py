"""The simulated world behind task260's pack: the service's film readers, the three reader studies (case sets,
every reading, sessions, resubmissions, practice cases), the imaging system's mammography records for the 12 months
to 30 September 2026 (with the migration's parallel run), the mobile units' visit schedule and the workforce list.

Every random draw comes from common.rng(label); nothing here reads a file."""
from __future__ import annotations

import datetime as dt
import hashlib

import numpy as np
from scipy import stats

import common as K

ROLES = (["Consultant radiologist"] * 8 + ["Consultant radiographer"] * 5 + ["Advanced practitioner radiographer"] * 9
         + ["Breast clinician"] * 4)


# ------------------------------------------------------------------ people

def names(n, label):
    from faker import Faker
    f = Faker("en_GB")
    f.seed_instance(int(K.rng(label).integers(1, 2 ** 31)))
    out, seen = [], set()
    while len(out) < n:
        first, last = f.first_name_female(), f.last_name()
        if (first, last) in seen or last in {l for _, l in out} or first in {fi for fi, _ in out}:
            continue
        seen.add((first, last))
        out.append((first, last))
    return out


def readers():
    """The service's 26 film readers in October 2026, with the traits the reading model gives them."""
    r = K.rng("readers")
    roles = list(ROLES)
    r.shuffle(roles)
    nm = names(26, "reader-names")
    out = []
    for k, role in enumerate(roles):
        yrs = {"Consultant radiologist": (6, 26), "Consultant radiographer": (9, 22),
               "Advanced practitioner radiographer": (2, 13), "Breast clinician": (3, 17)}[role]
        out.append(dict(code="FR%02d" % (k + 1), role=role, first=nm[k][0], last=nm[k][1],
                        years=int(r.integers(*yrs)),
                        skill=float(r.normal(0.08 if role == "Consultant radiologist" else 0.0, K.MODEL["skill_sd"])),
                        bias=float(r.normal(0, K.MODEL["bias_sd"])),
                        habit=str(r.choice(["1", "5", "10"], p=[0.5, 0.35, 0.15])),
                        recall_at=int(r.choice([20, 25, 30, 35, 40]))))
    return out


def panels(R):
    """Ten readers per study, drawn in proportion to the workforce's roles (three radiologists, five radiographers,
    two breast clinicians), half of them reading unaided first."""
    out = {}
    for S in K.STUDIES:
        r = K.rng("panel/" + S["sid"])
        by = lambda pred: [x for x in R if pred(x["role"])]
        pick = (list(r.choice(by(lambda s: s == "Consultant radiologist"), 3, replace=False))
                + list(r.choice(by(lambda s: "radiographer" in s), 5, replace=False))
                + list(r.choice(by(lambda s: s == "Breast clinician"), 2, replace=False)))
        pick = sorted(pick, key=lambda x: x["code"])
        first = np.array(["unaided"] * 5 + ["aided"] * 5)
        r.shuffle(first)
        ids = set()
        rows = []
        for x, f in zip(pick, first):
            while True:
                uid = ("u%05d" % r.integers(10000, 99999)) if S["platform"] == "4.1" else (
                    "R%04d" % r.integers(1000, 9999))
                if uid not in ids:
                    ids.add(uid)
                    break
            rows.append(dict(reader=x, uid=uid, first=f))
        out[S["sid"]] = rows
    return out


# ------------------------------------------------------------------ a reader study

def to_pom(X, habit):
    p = 100.0 / (1.0 + np.exp(-(X - K.MODEL["theta"]) * K.MODEL["slope"]))
    step = {"1": 1, "5": 5, "10": 10}[habit]
    return np.clip(np.round(p / step) * step, 0, 100).astype(int)


def case_set(S, r):
    """The study's 300 examinations from the 2019 to 2022 archive: 75 cancers then 225 normals (shuffled later)."""
    m, n = K.N_CANCER, K.N_NORMAL
    cases = []
    for k in range(m + n):
        cancer = k < m
        c = dict(cancer=cancer, density=str(r.choice(list("abcd"), p=[0.09, 0.42, 0.38, 0.11])),
                 age=str(r.choice(["50-54", "55-59", "60-64", "65-69", "70-74"], p=[0.27, 0.23, 0.21, 0.2, 0.09])),
                 year=int(r.choice([2019, 2020, 2021, 2022], p=[0.3, 0.12, 0.28, 0.3])),
                 archive="EP%07d" % r.integers(1000000, 9999999))
        if cancer:
            interval = r.random() < 0.35
            dcis = (not interval) and r.random() < 0.17
            c.update(route="Interval cancer" if interval else "Screen-detected",
                     months=int(r.integers(4, 36)) if interval else None, side=str(r.choice(["L", "R"])),
                     finding=str(r.choice(["Calcification"], p=[1.0])) if dcis else str(
                         r.choice(["Mass", "Calcification", "Distortion", "Asymmetry"], p=[0.5, 0.17, 0.18, 0.15])),
                     size=None if dcis else int(np.clip(r.gamma(2.6, 6.5), 3, 60)),
                     grade=("DCIS high" if r.random() < 0.6 else "DCIS intermediate") if dcis else int(
                         r.choice([1, 2, 3], p=[0.22, 0.5, 0.28])))
        else:
            c.update(route="Normal at next round", months=None, side=None, finding=None, size=None, grade=None)
        cases.append(c)
    return cases


def latent(S, panel, seed):
    """Final readings of one study as a (2, J, K) array of probabilities of malignancy (condition, reader, case) with
    the case list in the same order; the practice cases' readings; and the effects behind them."""
    p = S["params"]
    r = np.random.default_rng(seed)
    J, m, n = K.N_READERS, K.N_CANCER, K.N_NORMAL
    Kc = m + n
    M = K.MODEL
    cases = case_set(S, r)
    t = np.array([1.0 if c["cancer"] else 0.0 for c in cases])
    interval = np.array([c["route"] == "Interval cancer" for c in cases])
    dense = np.array([c["density"] in "cd" for c in cases])
    vis = (r.normal(0, M["vis_sd"], Kc) - 0.35 * interval) * t
    nd = (r.normal(0, M["norm_sd"], Kc) + 0.12 * dense) * (1 - t)
    rd = panel
    skill = np.array([x["reader"]["skill"] for x in rd])
    bias = np.array([x["reader"]["bias"] for x in rd])
    rc = r.normal(0, M["rc_sd"], (J, Kc))
    base = bias[:, None] + vis[None, :] + nd[None, :] + t[None, :] * (M["mu"] + skill[:, None]) + rc
    XU = base + r.normal(0, M["e_sd"], (J, Kc))
    eff = {}
    if S["kind"] == "readers":
        q = stats.norm.ppf((np.arange(J) + 0.5) / J)
        r.shuffle(q)
        cg = r.normal(0, p["case_sd"], Kc)
        XT = base + t[None, :] * (p["gain"] + p["reader_sd"] * q[:, None] + cg[None, :]) + r.normal(0, M["e_sd"], (J, Kc))
        eff = dict(reader_shift=p["reader_sd"] * q, case_shift=cg * t)
    else:
        score = p["alpha"] * t + r.normal(0, 1, Kc)
        lam = np.maximum(r.normal(p["lam"], p["lam_sd"], J), 0)
        XT = base + lam[:, None] * (score[None, :] - p["alpha"] / 2) + r.normal(0, M["e_sd"], (J, Kc))
        eff = dict(score=score, lam=lam)
    POM = np.stack([np.stack([to_pom(X[j], rd[j]["reader"]["habit"]) for j in range(J)]) for X in (XU, XT)])
    # practice cases: two cancers and three normals, read at the start of every session
    pt = np.array([1, 0, 0, 1, 0], dtype=float)
    pvis = r.normal(0.6, 0.4, 5) * pt
    pbase = bias[:, None] + pvis[None, :] + pt[None, :] * (M["mu"] + skill[:, None])
    PR = np.stack([np.stack([to_pom(pbase[j] + r.normal(0, 0.6, (K.SESSIONS, 5)), rd[j]["reader"]["habit"])
                             for j in range(J)]) for _ in range(2)])          # (2, J, sessions, 5)
    return dict(POM=POM, cases=cases, truth=t.astype(int), practice=PR, practice_truth=pt.astype(int), eff=eff,
                XU=XU, XT=XT)


def study(S, panel, seed):
    """One study end to end: the final readings (latent), the case codes, and the platform's reading log with session
    times, practice cases and resubmissions."""
    L = latent(S, panel, seed)
    r = np.random.default_rng(seed + 7919)
    J, Kc = K.N_READERS, K.N_CANCER + K.N_NORMAL
    order = r.permutation(Kc)
    code = {}
    for pos, k in enumerate(order):
        code[int(k)] = ("C%03d" % (pos + 1)) if S["platform"] == "4.1" else ("03-%03d" % (pos + 1))
    pcode = (["PRAC-%02d" % (k + 1) for k in range(5)] if S["platform"] == "4.1" else
             ["PRACTICE-%d" % (k + 1) for k in range(5)])
    days = K.screening_days(S["first_session"], S["first_session"] + dt.timedelta(days=70))
    p1 = [d for d in days if d < S["first_session"] + dt.timedelta(days=21)]
    log = []
    for j, x in enumerate(panel):
        rd = x["reader"]
        rj = np.random.default_rng(seed * 31 + j)
        d1 = sorted(rj.choice(p1, K.SESSIONS, replace=False))
        start2 = d1[-1] + dt.timedelta(days=K.WASHOUT_DAYS + 1 + int(rj.integers(0, 5)))
        p2 = [d for d in days if d >= start2]
        d2 = sorted(rj.choice(p2[:14], K.SESSIONS, replace=False))
        cond_days = {"unaided": d1, "aided": d2} if x["first"] == "unaided" else {"aided": d1, "unaided": d2}
        for ci, cond in enumerate(("unaided", "aided")):
            perm = rj.permutation(Kc)
            for s in range(K.SESSIONS):
                day = cond_days[cond][s]
                clock = dt.datetime.combine(day, dt.time(int(rj.integers(9, 15)), int(rj.choice([0, 15, 30, 45]))))
                clock = K.to_utc(clock) + dt.timedelta(seconds=int(rj.integers(0, 240)))
                seq = [("P", q) for q in range(5)] + [("S", int(k)) for k in perm[s * 75:(s + 1) * 75]]
                for posn, (kind, k) in enumerate(seq, 1):
                    secs = float(np.exp(rj.normal(3.55 + (0.1 if cond == "aided" else 0.0), 0.45)))
                    opened = clock
                    submitted = opened + dt.timedelta(seconds=round(secs, 1))
                    clock = submitted + dt.timedelta(seconds=float(rj.uniform(2, 9)))
                    if kind == "P":
                        pom = int(L["practice"][ci, j, s, k])
                        cc = pcode[k]
                    else:
                        pom = int(L["POM"][ci, j, k])
                        cc = code[k]
                    recall = pom >= rd["recall_at"]
                    if abs(pom - rd["recall_at"]) <= 5 and rj.random() < 0.15:
                        recall = not recall
                    log.append(dict(uid=x["uid"], case=cc, cond=cond, session=s + 1, day=day,
                                    position=posn, opened=opened, submitted=submitted, pom=pom, recall=recall, rev=1,
                                    reader=rd["code"], k=k if kind == "S" else None))
                # resubmissions: a reader reopens a case before closing the session and submits again
                sess_rows = [e for e in log if e["uid"] == x["uid"] and e["cond"] == cond and e["session"] == s + 1
                             and e["k"] is not None]
                for e in sess_rows:
                    if rj.random() < 0.012:
                        step = {"1": 1, "5": 5, "10": 10}[rd["habit"]]
                        delta = int(rj.choice([-1, 1]) * step * max(1, round(rj.integers(5, 21) / step)))
                        first = int(np.clip(e["pom"] - delta, 0, 100))
                        if first == e["pom"]:
                            first = int(np.clip(e["pom"] + delta, 0, 100))
                        again = dict(e)
                        again["rev"] = 2
                        again["opened"] = clock + dt.timedelta(seconds=float(rj.uniform(20, 300)))
                        again["submitted"] = again["opened"] + dt.timedelta(seconds=float(rj.uniform(8, 40)))
                        clock = again["submitted"] + dt.timedelta(seconds=3)
                        e["pom"] = first                     # the first submission held the earlier value
                        e["recall"] = first >= rd["recall_at"]
                        log.append(again)
    return dict(S=S, L=L, code=code, pcode=pcode, log=log, panel=panel, seed=seed)


# ------------------------------------------------------------------ the imaging system (RIS)

def _ref(i):
    return hashlib.sha256(("%d/woman/%d" % (K.SEED, i)).encode()).hexdigest()[:10]


def ris():
    """Every mammography record in the new RIS for study dates 1 October 2025 to 30 September 2026 (the legacy
    system's history loaded in), with the truth behind each row."""
    r = K.rng("ris")
    first, last = K.WINDOW
    pre = first - dt.timedelta(days=30)
    days = K.screening_days(pre, last)
    rate = {"CRBBS": 27.5, "WDLBS": 21.5, "CPLBS": 24.0, "TLWBS": 26.0}
    van_rate = {"MBSU1": 36.0, "MBSU2": 38.0, "MBSU3": 35.0}
    host_static = {s["ris"]: s["code"] for s in K.SITES}
    rows, attend = [], []
    woman = [0]

    def new_woman():
        woman[0] += 1
        return _ref(woman[0])

    def host_of(loc, day):
        if loc in host_static:
            return host_static[loc]
        if loc == "MBSU2":
            return K.MU2_OLD_HOST if day <= K.MU2_OLD_LAST else "WDL"
        return K.MOBILE[loc]

    # van calendars: blocks at practices, some weeks off the road
    van_days = {}
    for loc in van_rate:
        rv = K.rng("van/" + loc)
        on = []
        for d in days:
            if loc == "MBSU2" and K.MU2_OLD_LAST < d < K.MU2_NEW_FIRST:
                continue
            if rv.random() < 0.80:
                on.append(d)
        van_days[loc] = set(on)
    radiographers = {h: ["%s%02d" % (h[:2], k) for k in range(1, 9)] for h in K.SITE_ORDER}
    for d in days:
        for loc in list(rate) + list(van_rate):
            if loc in rate:
                if r.random() > 0.93:
                    continue
                n = int(max(4, r.normal(rate[loc], 5.5)))
            else:
                if d not in van_days[loc]:
                    continue
                n = int(max(6, r.normal(van_rate[loc], 5.0)))
            t0 = dt.datetime.combine(d, dt.time(8, 30)) + dt.timedelta(minutes=int(r.integers(0, 25)))
            for i in range(n):
                local = t0 + dt.timedelta(minutes=int(i * (480 / max(n, 1)) + r.integers(0, 6)))
                attend.append(dict(woman=new_woman(), loc=loc, host=host_of(loc, d), local=local,
                                   implant=r.random() < 0.014, tr=r.random() < 0.022,
                                   cancel=r.random() < 0.010, recall=r.random() < 0.041,
                                   rg=str(r.choice(radiographers[host_of(loc, d)]))))
    # each attendance's studies
    stud = []
    for a in attend:
        if a["cancel"]:
            stud.append(dict(a, exam="MAMS", status="CANCELLED", local=a["local"], images=None, views=None, kind="cancel"))
            continue
        stud.append(dict(a, exam="MAMS", status="COMPLETED", images=4, views="RCC RMLO LCC LMLO", kind="screen"))
        if a["implant"]:
            stud.append(dict(a, exam="MAMS", status="COMPLETED", images=4, views="RCC-ID RMLO-ID LCC-ID LMLO-ID",
                             local=a["local"] + dt.timedelta(minutes=int(r.integers(4, 13))), kind="implant"))
        if a["tr"]:
            nv = int(r.choice([1, 2], p=[0.45, 0.55]))
            views = " ".join(sorted(r.choice(["RCC", "RMLO", "LCC", "LMLO"], nv, replace=False)))
            if r.random() < 0.55:
                stud.append(dict(a, exam="MAMT", status="COMPLETED", images=nv, views=views,
                                 local=a["local"] + dt.timedelta(minutes=int(r.integers(3, 16))), kind="tr_same"))
            else:
                later = a["local"].date() + dt.timedelta(days=int(r.integers(5, 26)))
                while later.weekday() >= 5 or later in K.BANK_HOLIDAYS:
                    later += dt.timedelta(days=1)
                loc2 = a["loc"] if r.random() < 0.5 else next(s["ris"] for s in K.SITES if s["code"] == a["host"])
                coded = "MAMS" if (r.random() < 0.30 and a["local"].date() >= first) else "MAMT"
                lt = dt.datetime.combine(later, dt.time(int(r.integers(9, 16)), int(r.integers(0, 60))))
                stud.append(dict(a, exam=coded, status="COMPLETED", images=nv, views=views, local=lt, loc=loc2,
                                 host=host_of(loc2, later), kind="tr_later"))
        if a["recall"]:
            later = a["local"].date() + dt.timedelta(days=int(r.integers(7, 22)))
            while later.weekday() >= 5 or later in K.BANK_HOLIDAYS:
                later += dt.timedelta(days=1)
            clinic = "CRBAS" if a["host"] in ("CRB", "WDL") else "TLWAS"
            nv = int(r.integers(1, 4))
            stud.append(dict(a, exam="MAMA", status="COMPLETED", images=nv, views=None, loc=clinic,
                             host=host_static.get(clinic[:3] + "BS", clinic[:3]),
                             local=dt.datetime.combine(later, dt.time(int(r.integers(9, 16)), int(r.integers(0, 60)))),
                             kind="assess"))
    # symptomatic clinics
    for d in days:
        for loc, mu in (("CRBSY", 18.0), ("CPLSY", 12.0)):
            if r.random() > 0.95:
                continue
            n_ = int(max(3, r.normal(mu, 4)))
            for i in range(n_):
                lt = dt.datetime.combine(d, dt.time(9, 0)) + dt.timedelta(minutes=int(i * 450 / n_ + r.integers(0, 12)))
                stud.append(dict(woman=new_woman(), loc=loc, host=loc[:3], local=lt, exam="MAMD", status="COMPLETED",
                                 images=int(r.integers(2, 5)), views=None, rg=str(r.choice(radiographers[loc[:3]])),
                                 kind="sympt"))
    stud = [s for s in stud if first <= s["local"].date() <= last]
    # which system each study was registered in
    site_of_loc = lambda s: s["host"] if s["loc"] not in ("MBSU2",) else (
        K.MU2_OLD_HOST if s["local"].date() <= K.MU2_OLD_LAST else "WDL")
    out = []
    leg_no, new_no = [4417700], [26004100]
    stud.sort(key=lambda s: s["local"])
    for s in stud:
        site = s["loc"][:3] if s["loc"][:3] in K.SITE_ORDER else site_of_loc(s)
        golive, dual_end = K.GO_LIVE[site]
        d = s["local"].date()
        if d < golive:
            native, legacy = False, True
        elif d <= dual_end:
            share = 0.30 + 0.30 * K.rng("dualshare/%s/%s" % (site, d)).random()
            native, legacy = True, bool(r.random() < share)
        else:
            native, legacy = True, False
        if native:
            new_no[0] += int(r.integers(1, 4))
            out.append(dict(s, accession="MW%08d" % new_no[0], system="native", utc=K.to_utc(s["local"]), copy=False,
                            site=site))
        if legacy:
            leg_no[0] += int(r.integers(1, 3))
            out.append(dict(s, accession="LR%07d" % leg_no[0], system="migrated", utc=s["local"], copy=native,
                            site=site))
    return out


# ------------------------------------------------------------------ mobile units' visit schedule

PRACTICES = ["Lindhallow Health Centre", "Corrowby Leisure Centre", "Pellinghurst Village Hall",
             "Ullerwick Medical Centre", "Quellbury Community Hospital", "Marrowick Retail Park",
             "Dunsmere Health Centre", "Harlingford Leisure Centre", "Kelsford East Medical Centre",
             "Merrowdale North Retail Park", "Wendlow Valley Health Centre", "Tallowmere Village Hall",
             "Ullerwick Retail Park", "Quellbury Medical Centre", "Marrowick Health Centre", "Dunsmere Village Hall",
             "Harlingford Medical Centre", "Pellinghurst Health Centre", "Lindhallow Retail Park",
             "Corrowby Health Centre", "Kelsford West Leisure Centre", "Merrowdale South Health Centre",
             "Wendlow Community Centre", "Tallowmere Health Centre"]


def visits(R):
    """Visit blocks per mobile unit, from the days each unit screened in the RIS records (truth)."""
    days = {}
    for s in R:
        if s["loc"].startswith("MBSU") and not s["copy"]:
            days.setdefault(s["loc"], set()).add(s["local"].date())
    r = K.rng("visits")
    out = []
    pool = list(PRACTICES)
    r.shuffle(pool)
    assign = {"MBSU1": pool[:8], "MBSU2": pool[8:13], "MBSU2b": pool[13:18], "MBSU3": pool[18:]}
    for loc in sorted(days):
        ds = sorted(days[loc])
        blocks, cur = [], [ds[0]]
        for d in ds[1:]:
            if (d - cur[-1]).days > 6 or len(cur) >= int(r.integers(14, 26)):
                blocks.append(cur)
                cur = [d]
            else:
                cur.append(d)
        blocks.append(cur)
        k = {"MBSU1": 0, "MBSU2": 0, "MBSU2b": 0, "MBSU3": 0}
        for b in blocks:
            old = loc == "MBSU2" and b[-1] <= K.MU2_OLD_LAST
            key = "MBSU2b" if (loc == "MBSU2" and not old) else loc
            prac = assign[key][k[key] % len(assign[key])]
            k[key] += 1
            veh = K.VEHICLES[loc][0] if (loc != "MBSU2" or old) else K.VEHICLES[loc][1]
            host = (K.MU2_OLD_HOST if old else "WDL") if loc == "MBSU2" else K.MOBILE[loc]
            out.append(dict(unit=loc, vehicle=veh, host=host, practice=prac, start=b[0], end=b[-1], days=len(b)))
    return out


# ------------------------------------------------------------------ the workforce list

def workforce(RD):
    """The breast screening workforce as HR holds it in October 2026: the 26 film readers (one also on a bank
    contract, one whose post changed in July), a reader retiring on 31 March 2027, two appointed readers starting in
    2027, a reader who left in August 2026, and the mammographers and assistant practitioners who do not read films."""
    r = K.rng("workforce")
    used = set()

    def emp():
        while True:
            e = "%08d" % r.integers(20000000, 39999999)
            if e not in used:
                used.add(e)
                return e

    def reg(role):
        return ("GMC %07d" % r.integers(4000000, 7999999)) if role in ("Consultant radiologist", "Breast clinician") \
            else ("HCPC RA%06d" % r.integers(10000, 99999))
    rows = []
    site_pool = K.SITE_ORDER
    extra = names(30, "workforce-names")
    ix = r.permutation(len(RD))
    changed = next(RD[i]["code"] for i in ix if RD[i]["role"] == "Advanced practitioner radiographer")
    retiree, bank = [RD[i]["code"] for i in ix if RD[i]["code"] != changed][:2]
    for x in RD:
        body_reg = reg(x["role"])
        start = dt.date(2026 - x["years"] + int(r.integers(0, 2)), int(r.integers(1, 13)), 1)
        base = dict(name="%s, %s" % (x["last"], x["first"]), role=x["role"], reg=body_reg, reads="Y",
                    site=str(r.choice(site_pool)), person=x["code"])
        if x["code"] == changed:
            rows.append(dict(base, emp=emp(), role="Advanced practitioner radiographer", contract="Substantive",
                             fte=0.8, start=start, end=dt.date(2026, 6, 30)))
            rows.append(dict(base, emp=emp(), role="Consultant radiographer", contract="Substantive", fte=1.0,
                             start=dt.date(2026, 7, 1), end=None))
            continue
        end = dt.date(2027, 3, 31) if x["code"] == retiree else None
        rows.append(dict(base, emp=emp(), contract="Substantive", fte=float(r.choice([0.6, 0.8, 1.0, 1.0, 1.0])),
                         start=start, end=end))
        if x["code"] == bank:
            middle = names(1, "bank-middle")[0][0]
            rows.append(dict(base, emp=emp(), contract="Bank", fte=None, start=dt.date(2024, 9, 1), end=None,
                             name="%s, %s %s" % (x["last"], x["first"], middle), reg=body_reg.split(" ", 1)[1]))
    k = 0
    for role, start in (("Consultant radiologist", dt.date(2027, 2, 1)),
                        ("Advanced practitioner radiographer", dt.date(2027, 4, 1))):
        f, l = extra[k]
        k += 1
        rows.append(dict(name="%s, %s" % (l, f), role=role, reg=reg(role), reads="Y", site=str(r.choice(site_pool)),
                         person="NEW%d" % k, emp=emp(), contract="Substantive", fte=1.0, start=start, end=None))
    f, l = extra[k]
    k += 1
    rows.append(dict(name="%s, %s" % (l, f), role="Advanced practitioner radiographer", reg=reg("x"), reads="Y",
                     site=str(r.choice(site_pool)), person="LEFT", emp=emp(), contract="Substantive", fte=1.0,
                     start=dt.date(2019, 4, 1), end=dt.date(2026, 8, 31)))
    for role, cnt in (("Mammographer", 16), ("Assistant practitioner", 6), ("Screening office manager", 1)):
        for _ in range(cnt):
            f, l = extra[k]
            k += 1
            rows.append(dict(name="%s, %s" % (l, f), role=role, reg=reg("x") if role == "Mammographer" else "",
                             reads="N", site=str(r.choice(site_pool)), person="STAFF%d" % k, emp=emp(),
                             contract=str(r.choice(["Substantive", "Substantive", "Bank"])),
                             fte=float(r.choice([0.6, 0.8, 1.0])), start=dt.date(int(r.integers(2008, 2026)),
                                                                                 int(r.integers(1, 13)), 1),
                             end=None))
    # A mammographer who also works bank shifts: the same pattern as the reader's double contract, on a non-reader
    twin = next(x for x in rows if x["role"] == "Mammographer" and x["contract"] == "Substantive")
    rows.append(dict(twin, emp=emp(), contract="Bank", start=dt.date(min(max(twin["start"].year + 3, 2019), 2025), 9, 1)))
    # Bank rows come from the staff bank's own system: full legal names, the registration without its register's
    # prefix and no contracted hours
    legal = iter(names(12, "bank-legal-names"))
    for x in rows:
        if x["contract"] == "Bank" and x["person"] != bank:
            x["fte"] = None
            x["reg"] = x["reg"].split(" ", 1)[-1]
            first = next(legal)[0]
            if len(x["name"]) % 2 == 0 or x["person"] == twin["person"]:
                x["name"] = "%s %s" % (x["name"], first)
    order = r.permutation(len(rows))
    return [rows[i] for i in order], dict(retiree=retiree, bank=bank, changed=changed)
