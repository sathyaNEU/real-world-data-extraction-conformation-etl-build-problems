"""task146 architecture 3: every figure computed from target/ alone (the golden route, the easy routes, the
defensible variants and the asks). The routes the checks price are parameters here."""
import csv
import datetime as dt
import math
import os
from zoneinfo import ZoneInfo

import numpy as np
from openpyxl import load_workbook

F = {"subjects": "vela2_subjects.csv", "dosing": "vela2_dosing_log.csv", "pasi": "vela2_pasi_assessments.csv",
     "pk": "vela2_pk_trough_samples.csv", "cm": "vela2_concomitant_medications.csv", "epro": "vela2_epro_diary.csv",
     "sites": "vela2_sites.csv", "devices": "vela2_epro_device_log.csv", "feas": "vela3_feasibility_survey_2026.xlsx"}
DOSE = {"PBO": 0, "HB25": 25, "HB50": 50, "HB100": 100, "HB200": 200}
ARMS = ["PBO", "HB25", "HB50", "HB100", "HB200"]
CANDIDATES = (50, 100, 200)
BAR = 0.70
LB = 0.45359237


def rows(target, k):
    with open(os.path.join(target, F[k]), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pdate(s):
    s = s.strip()
    if "." in s:
        d, m, y = s.split(".")
        return dt.date(int(y), int(m), int(d))
    return dt.date.fromisoformat(s)


class Pack:
    def __init__(self, target):
        self.target = target
        self.sub = {r["subject_id"]: r for r in rows(target, "subjects")}
        self.tz = {r["site"]: r["time_zone"] for r in rows(target, "sites")}
        self.d1 = {}
        for r in rows(target, "dosing"):
            d = pdate(r["dose_date"])
            if r["subject_id"] not in self.d1 or d < self.d1[r["subject_id"]]:
                self.d1[r["subject_id"]] = d
        self.pasi = {}
        for r in rows(target, "pasi"):
            self.pasi.setdefault(r["subject_id"], []).append((r["visit"], pdate(r["assessment_date"]),
                                                              float(r["pasi_total"])))
        self.cm = {}
        for r in rows(target, "cm"):
            self.cm.setdefault(r["subject_id"], []).append(r)
        self.pk = rows(target, "pk")
        self.epro = rows(target, "epro")
        self.devlog = rows(target, "devices")
        self.light = True        # NB-UVB and PUVA are phototherapy
        self.link = "log"        # handhelds linked to patients through the device log
        self._feas = None

    # ---- the week-16 composite --------------------------------------------------------------------------
    def baseline(self, sid, label=False):
        v = self.pasi[sid]
        if label:     # the record the file labels "Baseline"
            return [x for x in v if x[0] == "Baseline"][0][2]
        d1 = self.d1[sid]
        return max((x for x in v if x[1] <= d1), key=lambda x: x[1])[2]

    def week16(self, sid):
        w = [x for x in self.pasi[sid] if x[0] == "Week 16"]
        return (w[0][2], w[0][1]) if w else (None, None)

    def rescued_by(self, sid, last_date):
        d1 = self.d1[sid]
        for r in self.cm.get(sid, []):
            atc, med = r["atc_code"], r["medication"].lower()
            light = any(k in med for k in ("phototherapy", "uvb", "puva", "uva")) if self.light else (
                "phototherapy" in med)
            if not (atc.startswith("D07AC") or atc.startswith("D07AD") or light):
                continue
            st = pdate(r["start_date"])
            if d1 < st <= last_date:
                return True
        return False

    def responder(self, sid, cut=0.75, label=False, rescue=True):
        v16, d16 = self.week16(sid)
        if v16 is None:
            return 0
        b = self.baseline(sid, label=label)
        if b <= 0 or (b - v16) / b < cut - 1e-12:
            return 0
        if rescue and self.rescued_by(sid, d16):
            return 0
        return 1

    # ---- exposure ---------------------------------------------------------------------------------------
    def troughs(self, weeks=(4, 8, 12, 16)):
        out = []
        for r in self.pk:
            sid = r["subject_id"]
            d = DOSE[self.sub[sid]["arm"]]
            if d == 0 or r["concentration"].startswith("<"):
                continue
            wk = int(r["visit"].split()[1])
            if wk not in weeks:
                continue
            c = float(r["concentration"]) / (1000.0 if r["unit"] == "ng/mL" else 1.0)
            out.append((sid, wk, d, float(self.sub[sid]["weight_kg"]), c))
        return out

    def feas(self):
        if self._feas is None:
            wb = load_workbook(os.path.join(self.target, F["feas"]), read_only=True)
            out = []
            for name, conv in (("US sites", LB), ("Canadian sites", 1.0)):
                for i, r in enumerate(wb[name].iter_rows(values_only=True)):
                    if i == 0 or r[0] is None:
                        continue
                    out.append({"site": r[0], "weight": float(r[4]) * conv, "prior": r[6] == "Yes"})
            self._feas = out
        return self._feas


# ---- small fitting tools -----------------------------------------------------------------------------------
def ols(X, y):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return b, y - X @ b


def logistic(X, y, iters=60):
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-(X @ b)))
        W_ = p * (1 - p) + 1e-9
        g = X.T @ (y - p)
        H = X.T @ (X * W_[:, None])
        step = np.linalg.solve(H, g)
        b = b + step
        if np.max(np.abs(step)) < 1e-10:
            break
    return b


def emax_fit(x, y, w=None):
    """Least squares Emax on x >= 0: E0 + Emax x^h / (ED50^h + x^h), by a coarse grid then refinement."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    w = np.ones_like(y) if w is None else np.asarray(w, float)
    best = None
    for h in np.linspace(0.6, 3.5, 30):
        for ed in np.geomspace(max(1e-3, np.min(x[x > 0]) / 4), np.max(x) * 3, 60):
            f = np.where(x > 0, x ** h / (ed ** h + x ** h), 0.0)
            A = np.c_[np.ones_like(f), f]
            b, *_ = np.linalg.lstsq(A * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)
            sse = float(np.sum(w * (y - A @ b) ** 2))
            if best is None or sse < best[0]:
                best = (sse, h, ed, b)
    _, h, ed, b = best
    return lambda z: b[0] + b[1] * np.where(np.asarray(z) > 0, np.asarray(z, float) ** h /
                                            (ed ** h + np.asarray(z, float) ** h), 0.0)


# ---- the routes ------------------------------------------------------------------------------------------
def composite(P, label=False, cut=0.75):
    return {sid: P.responder(sid, cut=cut, label=label) for sid in P.sub}


def arm_rates(P, resp):
    out = {}
    for a in ARMS:
        ids = [s for s, r in P.sub.items() if r["arm"] == a]
        out[a] = 100.0 * sum(resp[s] for s in ids) / len(ids)
    return out


def pk_model(P, wexp=None, weeks=(4, 8, 12, 16)):
    """log C - log dose = visit effect + b log(W/85): returns the week-16 intercept, b and the residual SD."""
    t = P.troughs(weeks)
    wks = sorted(set(x[1] for x in t))
    y = np.array([math.log(c) - math.log(d) for _, _, d, _, c in t])
    lw = np.array([math.log(w / 85.0) for _, _, _, w, _ in t])
    D = np.array([[1.0 if x[1] == k else 0.0 for k in wks] for x in t])
    if wexp is None:
        b, res = ols(np.c_[D, lw], y)
        a16, bw = b[wks.index(16)], b[-1]
    else:
        b, res = ols(D, y + wexp * lw)
        a16, bw = b[wks.index(16)], -wexp
    return a16, bw, float(np.std(res, ddof=D.shape[1] + 1))


def ctyp(a16, bw, dose, w):
    return dose * math.exp(a16 + bw * math.log(w / 85.0))


def golden(P, resp=None, wexp=None, form="logistic", prior=False):
    """Expected week-16 PASI 75 in the phase 3 population at each candidate dose: the trough each patient's dose
    and weight give (the population PK model on the VELA-2 troughs), the composite response on that exposure
    (fitted on VELA-2's active arms), averaged over the feasibility survey's candidates."""
    resp = composite(P) if resp is None else resp
    a16, bw, _ = pk_model(P, wexp=wexp)
    act = [s for s, r in P.sub.items() if DOSE[r["arm"]] > 0]
    lc = np.array([math.log(ctyp(a16, bw, DOSE[P.sub[s]["arm"]], float(P.sub[s]["weight_kg"]))) for s in act])
    y = np.array([resp[s] for s in act], float)
    feas = P.feas()
    out = {}
    if form == "logistic":
        cols = [np.ones_like(lc), lc]
        if prior:
            cols.append(np.array([1.0 if P.sub[s]["prior_biologic"] == "Y" else 0.0 for s in act]))
        b = logistic(np.c_[tuple(cols)], y)
        for d in CANDIDATES:
            z = []
            for c in feas:
                v = b[0] + b[1] * math.log(ctyp(a16, bw, d, c["weight"]))
                if prior:
                    v += b[2] * (1.0 if c["prior"] else 0.0)
                z.append(1 / (1 + math.exp(-v)))
            out[d] = 100.0 * float(np.mean(z))
    else:
        f = emax_fit(np.exp(lc), y)
        for d in CANDIDATES:
            out[d] = 100.0 * float(np.mean([f(ctyp(a16, bw, d, c["weight"])) for c in feas]))
    return out, (a16, bw)


def dose_weight_logistic(P, resp=None):
    resp = composite(P) if resp is None else resp
    act = [s for s, r in P.sub.items() if DOSE[r["arm"]] > 0]
    X = np.array([[1.0, math.log(DOSE[P.sub[s]["arm"]]), math.log(float(P.sub[s]["weight_kg"]) / 85.0)]
                  for s in act])
    b = logistic(X, np.array([resp[s] for s in act], float))
    return {d: 100.0 * float(np.mean([1 / (1 + math.exp(-(b[0] + b[1] * math.log(d) + b[2] *
                                                         math.log(c["weight"] / 85.0)))) for c in P.feas()]))
            for d in CANDIDATES}


def observed_er(P, resp=None, draws=400, seed=11):
    """Response on each patient's observed week-16 trough, carried to phase 3 with the between-patient spread."""
    resp = composite(P) if resp is None else resp
    a16, bw, sd = pk_model(P)
    t = {x[0]: x[4] for x in P.troughs(weeks=(16,))}
    act = [s for s, r in P.sub.items() if DOSE[r["arm"]] > 0 and s in t]
    X = np.c_[np.ones(len(act)), np.log([t[s] for s in act])]
    b = logistic(X, np.array([resp[s] for s in act], float))
    rng = np.random.default_rng(seed)
    eta = rng.normal(0, sd, draws)
    out = {}
    for d in CANDIDATES:
        z = []
        for c in P.feas():
            lc = math.log(ctyp(a16, bw, d, c["weight"])) + eta
            z.append(float(np.mean(1 / (1 + np.exp(-(b[0] + b[1] * lc))))))
        out[d] = 100.0 * float(np.mean(z))
    return out


def easy_routes(P, resp=None):
    resp = composite(P) if resp is None else resp
    rates = arm_rates(P, resp)
    act = [s for s, r in P.sub.items() if DOSE[r["arm"]] > 0]
    X = np.c_[np.ones(len(act)), np.log([DOSE[P.sub[s]["arm"]] for s in act])]
    b = logistic(X, np.array([resp[s] for s in act], float))
    logd = {d: 100.0 / (1 + math.exp(-(b[0] + b[1] * math.log(d)))) for d in CANDIDATES}
    x = [DOSE[a] for a in ARMS]
    f = emax_fit(x, [rates[a] for a in ARMS])
    emx = {d: float(f(d)) for d in CANDIDATES}
    return {"arm": {d: rates["HB%d" % d] for d in CANDIDATES}, "logdose": logd, "emax_dose": emx}


def pick(est):
    for d in CANDIDATES:
        if est[d] >= 100 * BAR:
            return d
    return None


# ---- the asks ---------------------------------------------------------------------------------------------
def ask_pasi(P, label=False):
    out = {}
    for cut, name in ((0.75, "PASI 75"), (0.90, "PASI 90")):
        r = arm_rates(P, composite(P, label=label, cut=cut))
        for a in ARMS:
            out[(name, a)] = round(r[a], 1)
    return out


def diary_days(P, first_dose="dose"):
    """Each subject's entries by diary day (local time, after-midnight entries to the evening before)."""
    out = {}
    if P.link == "log":
        dev = {r["device_id"]: r["subject_id"] for r in P.devlog}
    else:                    # the subject listing's handheld only
        dev = {r["epro_device"]: s for s, r in P.sub.items()}
    for r in P.epro:
        sid = dev.get(r["device_id"])
        if sid is None:
            continue
        tz = ZoneInfo(P.tz[P.sub[sid]["site"]])
        u = dt.datetime.strptime(r["entry_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("UTC"))
        loc = u.astimezone(tz)
        day = loc.date() - dt.timedelta(days=1) if loc.hour < 3 else loc.date()
        out.setdefault(sid, {})[day] = int(r["itch_nrs"])
    return out


def study_window(d1, lo, hi):
    def sd(k):
        return d1 + dt.timedelta(days=k - 1) if k > 0 else d1 + dt.timedelta(days=k)
    return sd(lo), sd(hi)


def ask_itch(P, anchor="dose"):
    days = diary_days(P)
    out = {}
    for wk, (lo, hi) in (("Week 12", (78, 84)), ("Week 16", (106, 112))):
        for a in ARMS:
            den = num = 0
            for sid, r in P.sub.items():
                if r["arm"] != a:
                    continue
                d1 = P.d1[sid] if anchor == "dose" else dt.date.fromisoformat(r["randomisation_date"])
                e = days.get(sid, {})

                def wmean(lo_, hi_):
                    s0, s1 = study_window(d1, lo_, hi_)
                    v = [e[d] for d in e if s0 <= d <= s1]
                    return sum(v) / len(v) if len(v) >= 4 else None
                b = wmean(-7, -1)
                if b is None or b < 4:
                    continue
                den += 1
                m = wmean(lo, hi)
                last = study_window(d1, lo, hi)[1]
                if m is not None and b - m >= 4 and not P.rescued_by(sid, last):
                    num += 1
            out[(wk, a)] = round(100.0 * num / den, 1) if den else 0.0
    return out
