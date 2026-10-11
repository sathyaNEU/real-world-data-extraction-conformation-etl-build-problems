"""The golden solve, from target/ alone: episodes, areas, the protocol's excess on every rung of the
ladder, the nowcast grid, and both asks. deliver.py writes the deliverables from solve(); checks.py
asserts on it; verify.py recomputes the answer and the ask figures on its own code path."""
import calendar
import datetime as dt
import os
import re
from collections import defaultdict
from zoneinfo import ZoneInfo

import numpy as np
import openpyxl
import pandas as pd

SYD = ZoneInfo("Australia/Sydney")
AREAS = ["Wagga Wagga", "Griffith", "Leeton", "Narrandera", "Murrumbidgee", "Hay", "Edward River", "Junee",
         "Cootamundra-Gundagai", "Snowy Valleys"]
EXTRACT_DAY = dt.date(2026, 10, 5)
FORTNIGHT = [EXTRACT_DAY - dt.timedelta(days=k) for k in range(14, 0, -1)]       # 21 Sep to 4 Oct
LAST_DAY = FORTNIGHT[-1]
CLUSTER_DAYS = (EXTRACT_DAY - dt.timedelta(days=30), LAST_DAY)
ASK = (dt.date(2026, 1, 1), dt.date(2026, 8, 31))
PRIOR = (2021, 2022, 2023, 2024, 2025)
HIST_HI = dt.date(2026, 8, 23)                       # specimens six weeks or more before the extract day
HIST_LO = {6: dt.date(2026, 2, 24), 12: dt.date(2025, 8, 24), 24: dt.date(2024, 8, 24)}
EPIDEMIC_2024 = (dt.date(2024, 8, 24), dt.date(2024, 12, 31))
FLOOR = 0.05                                         # a day below 5 per cent completeness is pooled
HOSP, PRIV = "Wagga Wagga Hospital Laboratory", "Inland Pathology"
SLIDE_HISTORY = (dt.date(2025, 8, 1), dt.date(2026, 7, 31))
LL = "pertussis_notifications_2019-2026.csv"


# ------------------------------------------------------------------ loading

def load(target):
    ll = pd.read_csv(os.path.join(target, LL), dtype=str, keep_default_na=False)
    ll["spec"] = pd.to_datetime(ll["specimen_date"]).dt.date
    recv = pd.to_datetime(ll["received_utc"], utc=True)
    ll["recv_local"] = recv.dt.tz_convert(SYD)
    ll["recv_day"] = ll["recv_local"].dt.date
    ll["delay"] = [(r - s).days for r, s in zip(ll["recv_day"], ll["spec"])]
    ll["dob_d"] = pd.to_datetime(ll["dob"]).dt.date
    wb = openpyxl.load_workbook(os.path.join(target, "postcode_lga_concordance.xlsx"), read_only=True)
    conc = defaultdict(list)
    for row in wb["Postcode to LGA"].iter_rows(min_row=5, values_only=True):
        if row[0]:
            conc[str(row[0])].append((row[2], float(row[4])))
    return ll, dict(conc)


def allocate(conc, postcode, rule="larger"):
    """PR-07 3.4. The other rules are the readings a solver might take instead: the first row listed, or
    any of the unit's areas the postcode touches."""
    rows = conc.get(postcode)
    if not rows:
        return None
    if rule == "first":
        best = rows[0]
    elif rule == "any_unit":
        inside = [r for r in rows if r[0] in AREAS]
        if not inside:
            return None
        best = max(inside, key=lambda r: r[1])
    else:
        best = max(rows, key=lambda r: r[1])
    return best[0] if best[0] in AREAS else None


# ------------------------------------------------------------------ episodes (PR-07 3.3) and areas (3.4)

def episodes(ll, conc, rule=True, alloc="larger"):
    """One row per case. rule=False takes every notification as a case (the episode rule ignored)."""
    out = []
    for pid, g in ll.sort_values(["spec", "recv_local"]).groupby("person_id", sort=True):
        groups = []
        for _, r in g.iterrows():
            if rule and groups and r["spec"] <= groups[-1][0]["spec"] + dt.timedelta(days=90):
                groups[-1].append(r)
            else:
                groups.append([r])
        for grp in groups:
            first = grp[0]
            out.append(dict(
                person_id=pid, date=first["spec"], area=allocate(conc, first["postcode"], alloc),
                postcode=first["postcode"],
                status="Confirmed" if any(x["case_status"] == "Confirmed" for x in grp) else "Probable",
                lab=first["notifying_lab"], first_recv=min(x["recv_day"] for x in grp), dob=first["dob_d"],
                mrn=next((x["mrn"] for x in grp if x["mrn"]), ""),
                school=next((x["school_or_childcare"] for x in grp if x["school_or_childcare"]), ""),
                role=next((x["school_role"] for x in grp if x["school_role"]), ""),
                n_notifications=len(grp)))
    return pd.DataFrame(out)


# ------------------------------------------------------------------ the protocol's counts (PR-07 4.2, 4.3)

def same_days(year):
    return [dt.date(year, d.month, d.day) for d in FORTNIGHT]


def expected(cases, basis="specimen", statuses=("Confirmed", "Probable")):
    res = (cases["area"].notna()) & cases["status"].isin(statuses)
    col = "date" if basis == "specimen" else "first_recv"
    e = {}
    for a in AREAS:
        sub = cases[res & (cases["area"] == a)]
        tot = 0
        for y in PRIOR:
            days = same_days(y)
            tot += int(((sub[col] >= days[0]) & (sub[col] <= days[-1])).sum())
        e[a] = tot / len(PRIOR)
    return e


def notified(cases, basis="specimen", statuses=("Confirmed", "Probable")):
    col = "date" if basis == "specimen" else "first_recv"
    sub = cases[cases["area"].notna() & cases["status"].isin(statuses)
                & (cases[col] >= FORTNIGHT[0]) & (cases[col] <= LAST_DAY)]
    return {a: int((sub["area"] == a).sum()) for a in AREAS}


def ranking(score):
    order = sorted(AREAS, key=lambda a: (-score[a], a))
    return order


def lead(score):
    o = ranking(score)
    first, second = score[o[0]], score[o[1]]
    return o[0], o[1], (first / second if second > 0 else float("inf"))


# ------------------------------------------------------------------ the nowcast

def week_start(d):
    return d - dt.timedelta(days=d.weekday())


def history(ll, months, drop_epidemic=False):
    lo = HIST_LO[months]
    h = ll[(ll["spec"] >= lo) & (ll["spec"] <= HIST_HI)]
    if drop_epidemic:
        h = h[~((h["spec"] >= EPIDEMIC_2024[0]) & (h["spec"] <= EPIDEMIC_2024[1]))]
    return h


def F_daily(delays):
    d = np.asarray(delays)
    if len(d) == 0:
        return None
    return lambda L: float((d <= L).mean())


def dev_weeks(spec, recv):
    return [(week_start(r) - week_start(s)).days // 7 for s, r in zip(spec, recv)]


def F_weekly(h):
    if len(h) == 0:
        return None
    k = np.asarray(dev_weeks(h["spec"], h["recv_day"]))
    return lambda K: float((k <= K).mean())


def chain_ladder(tri_rows, weekly):
    """Completeness by development from a reporting triangle of every cohort in the window up to the
    last day of the fortnight (recent cohorts at their partial development included)."""
    if len(tri_rows) == 0:
        return None
    if weekly:
        coh = np.array([week_start(s) for s in tri_rows["spec"]])
        dev = np.array(dev_weeks(tri_rows["spec"], tri_rows["recv_day"]))
        last = week_start(LAST_DAY)
        age = np.array([(last - c).days // 7 for c in coh])
        K = 7
    else:
        coh = np.array(list(tri_rows["spec"]))
        dev = np.array(list(tri_rows["delay"]))
        age = np.array([(LAST_DAY - c).days for c in coh])
        K = 45
    cohorts = sorted(set(coh))
    cage = {c: a for c, a in zip(coh, age)}
    cum = defaultdict(lambda: np.zeros(K + 1))
    for c, k in zip(coh, dev):
        cum[c][min(k, K):] += 1
    f = []
    for k in range(K):
        num = sum(cum[c][k + 1] for c in cohorts if cage[c] >= k + 1)
        den = sum(cum[c][k] for c in cohorts if cage[c] >= k + 1)
        f.append(num / den if den > 0 else None)
    G = {}
    for L in range(K + 1):
        prod, ok = 1.0, True
        for k in range(L, K):
            if f[k] is None:
                ok = False
                break
            prod *= f[k]
        G[L] = (1.0 / prod) if ok and prod > 0 else 0.0
    return lambda L: G[min(L, K)]


def pooled_inflate(counts, comp):
    """counts, comp: lists over cohorts, oldest first. Cohorts below the floor are merged into the nearest
    older cohort at or above it; a merged bin is its count over the mean completeness of its cohorts."""
    total, pend_n, pend_c = 0.0, 0, []
    for n, c in reversed(list(zip(counts, comp))):
        c = 0.0 if c is None else c
        if c < FLOOR:
            pend_n += n
            pend_c.append(c)
            continue
        total += (n + pend_n) / float(np.mean([c] + pend_c))
        pend_n, pend_c = 0, []
    if pend_n:
        raise ValueError("no cohort at or above the floor")
    return total


def estimate(n_by_day, est, F=None, Fw=None, G=None, weekly=False):
    """n_by_day: counts over the fortnight's 14 specimen days, oldest first."""
    if sum(n_by_day) == 0:
        return 0.0
    if weekly:
        n = [sum(n_by_day[:7]), sum(n_by_day[7:])]
        if est == "aggregate":
            return sum(n) / np.mean([Fw(1), Fw(0)])
        comp = [Fw(1), Fw(0)] if est == "perday" else [G(1), G(0)]
        return pooled_inflate(n, comp)
    Ls = [(LAST_DAY - d).days for d in FORTNIGHT]
    if est == "aggregate":
        return sum(n_by_day) / np.mean([F(L) for L in Ls])
    comp = [F(L) for L in Ls] if est == "perday" else [G(L) for L in Ls]
    return pooled_inflate(n_by_day, comp)


def fortnight_by_day(cases, key=None):
    """{(area, key): [14 counts]} for the cases with specimens in the fortnight."""
    sub = cases[cases["area"].notna() & (cases["date"] >= FORTNIGHT[0]) & (cases["date"] <= LAST_DAY)]
    out = defaultdict(lambda: [0] * 14)
    for _, r in sub.iterrows():
        k = (r["area"], r[key] if key else None)
        out[k][(r["date"] - FORTNIGHT[0]).days] += 1
    return out


def nowcast(ll, cases, est, months, strata, bins, drop_epidemic=False, case_level=False):
    """Estimated cases with specimens in the fortnight, by area. strata: route, area or pooled."""
    weekly = bins == "weekly"
    h = history(ll, months, drop_epidemic)
    if case_level:
        h = h[h["notification_id"].isin(first_notification_ids(ll))]
    tri = ll[(ll["spec"] >= HIST_LO[months]) & (ll["spec"] <= LAST_DAY)]
    if drop_epidemic:
        tri = tri[~((tri["spec"] >= EPIDEMIC_2024[0]) & (tri["spec"] <= EPIDEMIC_2024[1]))]

    def fns(hsub, tsub):
        return dict(F=F_daily(hsub["delay"]), Fw=F_weekly(hsub), G=chain_ladder(tsub, weekly))

    out = {}
    if strata == "route":
        nb = fortnight_by_day(cases, "lab")
        fn = {lab: fns(h[h["notifying_lab"] == lab], tri[tri["notifying_lab"] == lab]) for lab in (HOSP, PRIV)}
        for a in AREAS:
            out[a] = sum(estimate(nb[(a, lab)], est, weekly=weekly, **fn[lab]) for lab in (HOSP, PRIV))
    elif strata == "area":
        nb = fortnight_by_day(cases)
        ha = h.copy()
        ta = tri.copy()
        conc = CONC[0]
        ha["area"] = [allocate(conc, p) for p in ha["postcode"]]
        ta["area"] = [allocate(conc, p) for p in ta["postcode"]]
        for a in AREAS:
            n = nb[(a, None)]
            out[a] = estimate(n, est, weekly=weekly, **fns(ha[ha["area"] == a], ta[ta["area"] == a])) if sum(n) else 0.0
    else:
        nb = fortnight_by_day(cases)
        fn = fns(h, tri)
        for a in AREAS:
            out[a] = estimate(nb[(a, None)], est, weekly=weekly, **fn)
    return out


CONC = [None]


def first_notification_ids(ll):
    first = ll.sort_values(["spec", "recv_local"]).groupby("person_id").head(1)
    return set(first["notification_id"])


def route_share(ll, lab, days=14):
    h = ll[(ll["notifying_lab"] == lab) & (ll["spec"] >= SLIDE_HISTORY[0]) & (ll["spec"] <= SLIDE_HISTORY[1])]
    return float((h["delay"] <= days).mean()), len(h)


# ------------------------------------------------------------------ the call and its ladder

ESTIMATORS = ("aggregate", "perday", "chainladder")
WINDOWS = (6, 12, 24)
BINS = ("daily", "weekly")


def ladder(ll, cases):
    E = expected(cases)
    En = expected(cases, basis="notification")
    N = notified(cases)
    Nn = notified(cases, basis="notification")
    rungs = {
        "R0 notified cases, specimens in the fortnight": dict(N),
        "R1 notified less expected (PR-07 4.2, 4.3)": {a: N[a] - E[a] for a in AREAS},
        "R1b notified by notification date less expected": {a: Nn[a] - E[a] for a in AREAS},
        "R1b' notified by notification date less expected by notification date": {a: Nn[a] - En[a] for a in AREAS},
        "R2 notified over expected": {a: (N[a] / E[a] if E[a] > 0 else (float("inf") if N[a] else 0.0)) for a in AREAS},
    }
    pooled = nowcast(ll, cases, "aggregate", 12, "pooled", "daily")
    rungs["R3 nowcast on one delay pooled across the unit, less expected"] = {a: pooled[a] - E[a] for a in AREAS}
    route = nowcast(ll, cases, "aggregate", 12, "route", "daily")
    rungs["R4 nowcast on each laboratory route's own delay, less expected (the answer)"] = {a: route[a] - E[a] for a in AREAS}
    return E, En, N, Nn, rungs


def grid(ll, cases, E):
    cells = {}
    for est in ESTIMATORS:
        for m in WINDOWS:
            for st in ("route", "area", "pooled"):
                for b in BINS:
                    nc = nowcast(ll, cases, est, m, st, b)
                    cells[(est, m, st, b)] = {a: nc[a] - E[a] for a in AREAS}
    return cells


# ------------------------------------------------------------------ the asks

def add_months(d, n):
    y, m = divmod(d.month - 1 + n, 12)
    y += d.year
    m += 1
    return dt.date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def load_links(target):
    adm = pd.read_csv(os.path.join(target, "respiratory_admissions_2019-2026.csv"), dtype=str, keep_default_na=False)
    adm["admit"] = pd.to_datetime(adm["admission_date"], format="%d/%m/%Y").dt.date
    births = pd.read_csv(os.path.join(target, "birth_records_2024-2026.csv"), dtype=str, keep_default_na=False)
    reg = pd.read_parquet(os.path.join(target, "antenatal_vaccinations_2019-2026.parquet"))
    return adm, births, reg


def digits(s):
    return re.sub(r"\D", "", str(s))


def ask_a(cases, adm, births, reg, adm_window=14, vacc_rule="pregnancy14", infant_months=6,
          statuses=("Confirmed", "Probable")):
    sub = cases[cases["area"].notna() & (cases["date"] >= ASK[0]) & (cases["date"] <= ASK[1]) & cases["status"].isin(statuses)]
    adm_by = defaultdict(list)
    for m, d in zip(adm["mrn"], adm["admit"]):
        adm_by[int(m)].append(d)
    bmap = {}
    for _, b in births.iterrows():
        bmap[int(b["baby_mrn"])] = b
    reg = reg.copy()
    reg["card"] = [digits(x) for x in reg["medicare_card"]]
    reg["key"] = reg["card"] + reg["irn"].astype(str)
    doses = defaultdict(list)
    for k, d, ag in zip(reg["key"], reg["dose_date"], reg["antigen"]):
        doses[k].append((pd.Timestamp(d).date(), ag))
    rows = {}
    for a in AREAS:
        s = sub[sub["area"] == a]
        conf = int((s["status"] == "Confirmed").sum())
        prob = int((s["status"] == "Probable").sum())
        inf = s[[d < add_months(b, infant_months) for d, b in zip(s["date"], s["dob"])]]
        admitted = vacc = 0
        for _, c in inf.iterrows():
            mrn = int(c["mrn"]) if c["mrn"] else None
            if mrn is not None and any((adm_window is None) or abs((x - c["date"]).days) <= adm_window for x in adm_by.get(mrn, [])):
                admitted += 1
            b = bmap.get(mrn)
            if b is None:
                continue
            born = dt.date.fromisoformat(b["birth_date"])
            start = born - dt.timedelta(days=7 * int(b["gestation_weeks"]))
            key = digits(b["mother_medicare_no"])
            ok = False
            for d, ag in doses.get(key, []):
                if vacc_rule == "pregnancy14" and ag == "dTpa" and start <= d <= born - dt.timedelta(days=14):
                    ok = True
                elif vacc_rule == "anytime" and ag == "dTpa" and d < born:
                    ok = True
                elif vacc_rule == "any_vaccine" and start <= d <= born - dt.timedelta(days=14):
                    ok = True
            vacc += ok
        rows[a] = dict(confirmed=conf, probable=prob, infants=len(inf), admitted=admitted, vaccinated=vacc)
    return rows


def school_key(text, roster_names):
    """Resolve an interview's free-text school to a roster school (None when it is not one)."""
    t = text.lower().replace("'", "")
    t = re.sub(r"[^a-z ]", " ", t)
    rep = {"ps": "public school", "p s": "public school", "pub": "public", "ave": "avenue", "av": "avenue",
           "rd": "road", "st": "street", "hs": "high school", "nth": "north"}
    words = []
    for w in t.split():
        words.append(rep.get(w, w))
    t = " ".join(words)
    t = t.replace("p s", "public school")
    for town in ("griffith", "wagga", "tumut", "leeton", "cootamundra", "narrandera"):
        t = re.sub(r"\b%s\b" % town, " ", t)
    t = " ".join(t.split())
    best = None
    for key, name in roster_names.items():
        n = name.lower().replace("'", "")
        for town in ("griffith",):
            n = re.sub(r"\b%s\b" % town, " ", n)
        n = " ".join(n.split())
        core = n.replace(" public school", "").replace(" high school", "")
        if "preschool" in t or "pre school" in t:
            continue
        if t.startswith(core) and (("high" in n) == ("high" in t) or "high" not in t):
            best = key
    return best


def load_rosters(target):
    wb = openpyxl.load_workbook(os.path.join(target, "school_rosters_term3_2026.xlsx"), read_only=True)
    out = {}
    for ws in wb.worksheets:
        vals = list(ws.iter_rows(min_row=1, max_row=6, values_only=True))
        name = vals[0][0]
        lga = next(v[1] for v in vals if v[0] == "LGA")
        out[ws.title] = dict(name=name, lga=lga)
    return out


def ask_b(cases, rosters, window="specimen", roles=("Student",), statuses=("Confirmed", "Probable"),
          match="normalised", episode_cases=None):
    c = episode_cases if episode_cases is not None else cases
    col = "date" if window == "specimen" else "first_recv"
    sub = c[(c[col] >= CLUSTER_DAYS[0]) & (c[col] <= CLUSTER_DAYS[1]) & c["role"].isin(roles)
            & c["status"].isin(statuses) & (c["school"] != "")]
    names = {k: v["name"] for k, v in rosters.items()}
    counts = defaultdict(int)
    for t in sub["school"]:
        if match == "exact":
            k = next((kk for kk, n in names.items() if n == t), None)
        elif match == "fuzzy":
            k = school_key(t.replace("Preschool", "Public School").replace("Pre-school", "Public School"), names)
        else:
            k = school_key(t, names)
        if k:
            counts[k] += 1
    clusters = sorted(((rosters[k]["name"], rosters[k]["lga"], n) for k, n in counts.items() if n >= 2),
                      key=lambda x: (-x[2], x[0]))
    return clusters


def clusters_in(clusters, area):
    """PR-07 5.1: the slide lists the clusters at schools in the area the team goes to (the school's area as its
    roster gives it), which are the team's school visits that week."""
    return [c for c in clusters if c[1] == area]


# ------------------------------------------------------------------ everything

def solve(target, with_grid=True):
    ll, conc = load(target)
    CONC[0] = conc
    cases = episodes(ll, conc)
    E, En, N, Nn, rungs = ladder(ll, cases)
    g = {"E": E, "En": En, "N": N, "Nn": Nn, "rungs": rungs}
    final = rungs["R4 nowcast on each laboratory route's own delay, less expected (the answer)"]
    g["answer"] = ranking(final)[0]
    g["route_share"] = {lab: route_share(ll, lab) for lab in (HOSP, PRIV)}
    g["route_share_7"] = {lab: route_share(ll, lab, 7) for lab in (HOSP, PRIV)}
    if with_grid:
        g["grid"] = grid(ll, cases, E)
    if os.path.exists(os.path.join(target, "respiratory_admissions_2019-2026.csv")):
        adm, births, reg = load_links(target)
        g["ask_a"] = ask_a(cases, adm, births, reg)
        rosters = load_rosters(target)
        g["rosters"] = rosters
        g["ask_b_all"] = ask_b(cases, rosters)
        g["ask_b"] = clusters_in(g["ask_b_all"], g["answer"])
    return dict(ll=ll, conc=conc, cases=cases), g
