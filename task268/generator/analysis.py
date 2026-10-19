"""Every figure, computed from the shipped pack alone: the 2022 and 2023 cohort's follow-up assembled from the registry's
patients, visits and follow-up events and the two death sources, each hospital's two-year survival under every route a
solver might take (the ladder) and every form of the decisive estimator (the family), and the two asks with the
handlings the cracker and the over-cleaners use."""
import csv
import datetime as dt
import os

import numpy as np

import common as K

CLASS = {"I": 0, "II": 1, "III": 2, "IV": 3, "Class I": 0, "Class II": 1, "Class III": 2, "Class IV": 3,
         "1": 0, "2": 1, "3": 2, "4": 3, "NYHA 1": 0, "NYHA 2": 1, "NYHA 3": 2, "NYHA 4": 3}
INPATIENT = {"IP", "Inpatient", "INPT"}
HOSP = {"FEN": "FEN", "LIN": "LIN", "BRE": "BRE", "BRN": "BRE", "GUL": "GUL", "WRE": "WRE"}
H = K.CODES


def _rows(path, delim=","):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=delim))


def _d(s):
    return dt.date.fromisoformat(s)


def load(pack):
    import openpyxl
    f = lambda k: os.path.join(pack, K.FILES[k])
    D = dict(patients=_rows(f("patients")), visits=_rows(f("visits")), events=_rows(f("events")),
             exchange=_rows(f("exchange"), "|"), crosswalk=_rows(f("crosswalk")), lab=_rows(f("lab")))
    wb = openpyxl.load_workbook(f("fl_deaths"), read_only=True)
    ws = wb["Linked deaths"]
    D["fl"] = [dict(mrn=str(r[0]), dod=r[1].date() if hasattr(r[1], "date") else r[1])
               for r in ws.iter_rows(min_row=2, values_only=True) if r[0]]
    return D


# ---------------------------------------------------------------------------------------------- the cohort
def cohort(D, exchange_censors=False, basis="diagnosis", horizon=None, drop=(), exchange_deaths=True, raw_class=False):
    """One record per patient newly diagnosed in 2022 or 2023: hospital, time to death or loss within two years (days
    from diagnosis), and the clinic visits up to that time with the class each recorded. The keywords give the
    readings the fork table and the mess tests compare: the cohort chosen by enrolment date or by first clinic visit,
    two years as 730 days, patients dropped, the exchange's deaths left unread, the class kept as the record spells it."""
    lo, hi = K.COHORT
    leg2new = {r["legacy_mrn"]: r["new_mrn"] for r in D["crosswalk"]}
    first = {}
    if basis == "first_visit":
        for r in D["visits"]:
            v = _d(r["visit_date"])
            if r["registry_id"] not in first or v < first[r["registry_id"]]:
                first[r["registry_id"]] = v
    pts = {}
    for r in D["patients"]:
        dx = _d(r["diagnosis_date"])
        sel = {"diagnosis": dx, "enrolment": _d(r["enrolment_date"]),
               "first_visit": first.get(r["registry_id"], dx)}[basis]
        if not (lo <= sel <= hi) or not (lo <= dx) or r["registry_id"] in drop:
            continue
        mrn = r["mrn"]
        c0 = r["nyha_at_diagnosis"] if raw_class else CLASS[r["nyha_at_diagnosis"]]
        pts[r["registry_id"]] = dict(rid=r["registry_id"], h=HOSP[r["hospital"]], dx=dx, c0=c0,
                                     new=leg2new.get(mrn, mrn), death=None, end=None, why=None, visits=[], exch=None)
    by_new = {}
    for p in pts.values():
        by_new.setdefault(p["new"], []).append(p)
    for r in D["fl"]:
        for p in by_new.get(r["mrn"], []):
            p["death"] = r["dod"] if p["death"] is None else min(p["death"], r["dod"])
    for r in D["exchange"] if exchange_deaths else []:
        p = pts.get(r["PARTNER_ID"])
        if p:
            d = dt.datetime.strptime(r["DOD"], "%Y%m%d").date()
            p["death"] = d if p["death"] is None else min(p["death"], d)
    for r in D["events"]:
        p = pts.get(r["registry_id"])
        if not p:
            continue
        d = _d(r["event_date"])
        if r["event"] == "REL" and r["destination_state"] in K.EXCHANGE_STATES:
            p["exch"] = d
            if exchange_censors and (p["end"] is None or d < p["end"]):
                p["end"], p["why"] = d, "exchange"
            continue
        if p["end"] is None or d < p["end"]:
            p["end"], p["why"] = d, ("north" if r["event"] == "REL" else "consent")
    for r in D["visits"]:
        p = pts.get(r["registry_id"])
        if p:
            p["visits"].append((_d(r["visit_date"]), r["nyha_class"] if raw_class else CLASS[r["nyha_class"]]))
    out = []
    for p in pts.values():
        two = dt.date(p["dx"].year + 2, p["dx"].month, p["dx"].day) if horizon is None else p["dx"] + dt.timedelta(horizon)
        hor = (two - p["dx"]).days
        t_end = (p["end"] - p["dx"]).days if p["end"] is not None and p["end"] < two else None
        t_death = (p["death"] - p["dx"]).days if p["death"] is not None and p["death"] <= two else None
        if t_death is not None and (t_end is None or t_death <= t_end):
            T, E, lost = t_death, 1, None
        elif t_end is not None:
            T, E, lost = t_end, 0, p["why"]
        else:
            T, E, lost = hor, 0, None
        vis = sorted(((v - p["dx"]).days, c) for v, c in p["visits"] if 0 < (v - p["dx"]).days <= T)
        # the whole observed history, for the projection's class changes and death rates: deaths to the sources'
        # completeness date, follow-up to its end, visits to the extract
        rel = lambda x: (x - p["dx"]).days if x is not None else None
        out.append(dict(rid=p["rid"], h=p["h"], c0=p["c0"], T=T, E=E, lost=lost, hor=hor, visits=vis,
                        last=vis[-1][1] if vis else p["c0"], d_full=rel(p["death"]),
                        end_full=rel(p["end"]), why_full=p["why"], exch_full=rel(p["exch"]),
                        obs_full=rel(K.DEATHS_TO), allvis=sorted(((v - p["dx"]).days, c) for v, c in p["visits"])))
    out.sort(key=lambda x: x["rid"])
    return out


# ---------------------------------------------------------------------------------------------- estimators
NDAY = 733


def wkm(pts, weight=None):
    """The product-limit estimate at each patient's own two-year date, with optional time-varying weights:
    weight(p) returns [(from_day, w), ...] in increasing day order, the weight in force from that day on."""
    N = np.zeros(NDAY + 2)
    Dd = np.zeros(NDAY + 2)
    for p in pts:
        segs = weight(p) if weight else [(0, 1.0)]
        T = p["T"]
        for j, (s, w) in enumerate(segs):
            e = segs[j + 1][0] if j + 1 < len(segs) else NDAY + 1
            a, b = max(s, 1), min(e, T + 1)
            if a < b:
                N[a] += w
                N[b] -= w
        if p["E"]:
            w = 1.0
            for s, ww in segs:
                if s <= T:
                    w = ww
            Dd[T] += w
    N = np.cumsum(N)
    S = 1.0
    for t in range(1, NDAY + 1):
        if Dd[t] > 0:
            S *= 1.0 - Dd[t] / N[t]
    return S


def censor_rates(pts, key="visit", time_key=None):
    """The chance a visit ends in a move north beyond the death linkage, by the class the visit recorded (or the class
    at diagnosis), from every visit while the patient was followed."""
    n = {}
    m = {}
    for p in pts:
        for d, c in p["visits"]:
            if d > p["T"]:
                break
            k = c if key == "visit" else p["c0"]
            if time_key:
                k = (k, min(8, int(round(d / 91.0))))
            n[k] = n.get(k, 0) + 1
            if p["lost"] in ("north", "exchange") and d == p["T"]:
                m[k] = m.get(k, 0) + 1
    return {k: min(0.9, m.get(k, 0) / n[k]) for k in n}


def ipcw_weights(rates, key="visit", time_key=False, stab=None):
    def f(p):
        segs = [(0, 1.0)]
        w = 1.0
        num = 1.0
        for d, c in p["visits"]:
            if d >= p["T"]:
                break
            k = c if key == "visit" else p["c0"]
            if time_key:
                k = (k, min(8, int(round(d / 91.0))))
            w /= 1.0 - rates.get(k, 0.0)
            if stab is not None:
                num *= 1.0 - stab
            segs.append((d + 1, w * num))
        return segs
    return f


def ipcw(pts, key="visit", pool=None, time_key=False, stabilise=False):
    rates = censor_rates(pool if pool is not None else pts, key, time_key)
    stab = None
    if stabilise:
        n = sum(1 for p in pts for d, c in p["visits"] if d <= p["T"])
        m = sum(1 for p in pts if p["lost"] == "north")
        stab = m / n
    return wkm(pts, ipcw_weights(rates, key, time_key, stab))


def logistic_rates(allpts):
    """A pooled logistic model of a visit ending in a move north: a term for each hospital and each class."""
    X, y = [], []
    for p in allpts:
        for d, c in p["visits"]:
            if d > p["T"]:
                break
            row = [1.0 if p["h"] == h else 0.0 for h in H] + [1.0 if c == k else 0.0 for k in (1, 2, 3)]
            X.append(row)
            y.append(1.0 if (p["lost"] == "north" and d == p["T"]) else 0.0)
    X, y = np.array(X), np.array(y)
    b = np.zeros(X.shape[1])
    b[:5] = -6.0
    lam = 1e-3
    for _ in range(100):
        eta = np.clip(X @ b, -30, 30)
        mu = 1.0 / (1.0 + np.exp(-eta))
        Wt = mu * (1 - mu) + 1e-12
        g = X.T @ (y - mu) - lam * b
        Hm = (X * Wt[:, None]).T @ X + lam * np.eye(X.shape[1])
        step = np.linalg.solve(Hm, g)
        step = np.clip(step, -2.0, 2.0)
        b += step
        if np.max(np.abs(step)) < 1e-10:
            break
    return {(h, c): 1.0 / (1.0 + np.exp(-np.clip(b[i] + (b[4 + c] if c else 0.0), -30, 30)))
            for i, h in enumerate(H) for c in range(4)}


def ipcw_logistic(pts, h, rates):
    return wkm(pts, ipcw_weights({c: rates[(h, c)] for c in range(4)}))


def gform(pts):
    """The multi-state projection: one-quarter class changes and deaths by the class at a visit, estimated from every
    patient's observed history, and every patient lost before two years carried from the class recorded at the loss
    to the two-year date. An interval runs from a visit to the next visit when it was kept a quarter later (survived,
    and the class it recorded); otherwise over a nominal quarter, counted only where a death or survival through it is
    on record."""
    Tn = np.zeros((4, 4))
    Dn = np.zeros(4)
    Nn = np.zeros(4)
    for p in pts:
        stop_clinic = min(x for x in (p["end_full"], p["exch_full"], 10 ** 6) if x is not None)
        dead_seen = min(x for x in ((p["end_full"] if p["why_full"] in ("north", "consent") else None), p["obs_full"])
                        if x is not None)
        dd = p["d_full"] if p["d_full"] is not None and p["d_full"] <= dead_seen else None
        vis = [(0, p["c0"])] + [v for v in p["allvis"] if v[0] <= stop_clinic]
        for j, (d, c) in enumerate(vis):
            if p["why_full"] == "north" and p["end_full"] is not None and d >= p["end_full"]:
                break
            if p["why_full"] == "consent" and p["end_full"] is not None and d >= p["end_full"]:
                break
            nxt = vis[j + 1] if j + 1 < len(vis) else None
            if dd is not None and d < dd and (nxt is None or nxt[0] > dd):
                if dd - d <= 91:
                    Nn[c] += 1
                    Dn[c] += 1
                break
            if nxt is not None and 60 <= nxt[0] - d <= 125:
                Nn[c] += 1
                Tn[c, nxt[1]] += 1
                continue
            # no visit kept a quarter later: a nominal quarter, survived if the record shows the patient alive past it
            if d + 91 <= dead_seen and (dd is None or dd > d + 91):
                Nn[c] += 1
            if p["exch_full"] is not None and d >= p["exch_full"]:
                break
    Th = Tn / np.maximum(Tn.sum(1), 1)[:, None]
    Dh = Dn / np.maximum(Nn, 1)
    gform.last_fit = (Th, Dh)
    tot = 0.0
    for p in pts:
        if p["E"]:
            continue
        if p["lost"] is None:
            tot += 1.0
            continue
        v = np.zeros(4)
        v[p["last"]] = 1.0
        rem = (p["hor"] - p["T"]) / 91.0
        full = int(rem)
        for _ in range(full):
            v = (v * (1 - Dh)) @ Th
        frac = rem - full
        tot += float((v * (1 - Dh * frac)).sum())
    return tot / len(pts)


def by_h(pts):
    return {h: [p for p in pts if p["h"] == h] for h in H}


def golden(D, **kw):
    """The golden estimator (each hospital's patients weighted visit by visit by the inverse of the hospital's chance
    of a move beyond the linkage at the class recorded) on the cohort under any of cohort()'s readings."""
    G = by_h(cohort(D, **kw))
    return {h: ipcw(G[h]) for h in H}


def ladder(D):
    """Each hospital's two-year survival under every rung and every form of the decisive estimator."""
    C = cohort(D)
    G = by_h(C)
    Cx = by_h(cohort(D, exchange_censors=True))
    logit = logistic_rates(C)
    R = {}
    for h in H:
        g = G[h]
        n = len(g)
        R.setdefault("crude", {})[h] = 1 - sum(p["E"] for p in g) / n
        known = [p for p in g if p["lost"] is None]
        R.setdefault("complete_case", {})[h] = sum(1 for p in known if not p["E"]) / len(known)
        R.setdefault("worst_case", {})[h] = sum(1 for p in g if not p["E"] and p["lost"] is None) / n
        R.setdefault("km", {})[h] = wkm(g)
        R.setdefault("km_exchange_censored", {})[h] = wkm(Cx[h])
        R.setdefault("ipcw_diagnosis_class", {})[h] = ipcw(g, key="diagnosis")
        R.setdefault("ipcw_pooled", {})[h] = ipcw(g, pool=C)
        R.setdefault("golden", {})[h] = ipcw(g)
        R.setdefault("ipcw_class_by_quarter", {})[h] = ipcw(g, time_key=True)
        R.setdefault("ipcw_stabilised", {})[h] = ipcw(g, stabilise=True)
        R.setdefault("ipcw_logistic", {})[h] = ipcw_logistic(g, h, logit)
        R.setdefault("projection", {})[h] = gform(g)
    R["_cohort"] = C
    return R


FAMILY = ["golden", "ipcw_class_by_quarter", "ipcw_stabilised", "ipcw_logistic", "projection"]
WRONG = ["crude", "complete_case", "worst_case", "km", "km_exchange_censored", "ipcw_diagnosis_class", "ipcw_pooled"]


def pick(v):
    o = sorted(H, key=lambda h: v[h])
    return o[0], o[1], v[o[1]] - v[o[0]]


# ---------------------------------------------------------------------------------------------- Ask A
def _num(t):
    if t.startswith(">"):
        return float(t[1:]) + 1.0
    if t.startswith("<"):
        return float(t[1:]) - 1.0
    return float(t)


def ask_a(D, handling="golden"):
    rows = [r for r in D["lab"] if r["released"][:4] == "2025"]
    if handling == "golden":
        last = {}
        for r in rows:
            k = (r["performing_lab"], r["mrn"], r["collected"])
            if k not in last or r["released"] > last[k]["released"]:
                last[k] = r
        rows = list(last.values())
    elif handling == "first":
        first = {}
        for r in rows:
            k = (r["performing_lab"], r["mrn"], r["collected"])
            if k not in first or r["released"] < first[k]["released"]:
                first[k] = r
        rows = list(first.values())
    elif handling == "day":
        last = {}
        for r in rows:
            k = (r["performing_lab"], r["mrn"], r["collected"][:10])
            if k not in last or r["released"] > last[k]["released"]:
                last[k] = r
        rows = list(last.values())
    out = {h: [0, 0] for h in H}
    for r in rows:
        h = r["performing_lab"]
        out[h][0] += 1
        out[h][1] += _num(r["result"]) >= K.REFERRAL
    return {h: tuple(v) for h, v in out.items()}


# ---------------------------------------------------------------------------------------------- Ask B
def diagnosed(r):
    """The diagnosis date as the record supports it: the date shown, or the enrolment date where the record shows the
    diagnosis after the enrolment (the diagnosis came on or before it)."""
    return min(r["diagnosis_date"], r["enrolment_date"])


def ask_b(D, handling="golden"):
    """golden: by the supported diagnosis date, a 2025 enrolment of a patient enrolled before (through the crosswalk)
    left out. plain: the registry as it stands, by the date shown. reader: the re-enrolments left out, by the date shown.
    enrolment: the re-enrolments left out, by the enrolment date. dated: the supported date, the re-enrolments kept.
    drop_crosswalked: by the supported date, every 2025 enrolment whose number is in the crosswalk dropped."""
    leg2new = {r["legacy_mrn"]: r["new_mrn"] for r in D["crosswalk"]}
    new_in_xwalk = set(leg2new.values())
    when = {"golden": diagnosed, "dated": diagnosed, "drop_crosswalked": diagnosed,
            "plain": lambda r: r["diagnosis_date"], "reader": lambda r: r["diagnosis_date"],
            "enrolment": lambda r: r["enrolment_date"]}[handling]
    enrolled_new = {}
    for r in D["patients"]:
        enrolled_new.setdefault(leg2new.get(r["mrn"], r["mrn"]), []).append(r)
    out = {h: [0, 0] for h in H}
    for r in D["patients"]:
        if when(r)[:4] != "2025":
            continue
        if handling in ("golden", "reader", "enrolment"):
            if any(q["registry_id"] != r["registry_id"] and when(q) < when(r) for q in enrolled_new.get(r["mrn"], [])):
                continue
        elif handling == "drop_crosswalked":
            if r["mrn"] in new_in_xwalk:
                continue
        h = HOSP[r["hospital"]]
        out[h][0] += 1
        out[h][1] += r["diagnosis_setting"] in INPATIENT
    return {h: tuple(v) for h, v in out.items()}


def asks(D):
    return dict(a=ask_a(D), b=ask_b(D))
