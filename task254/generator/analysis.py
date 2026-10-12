"""The golden's code path over the shipped tables, with a switch for every wrong path the ladders price.

Every function takes the pack's tables as pandas DataFrames of strings, exactly as read from the files."""
import datetime as dt
import math

import numpy as np
import pandas as pd

import estimators as E

LOCK = dt.date(2026, 9, 30)
LOCK_TS = pd.Timestamp(LOCK)
INTERVAL_START = pd.Timestamp(2025, 10, 1)
RISK_OF = {"Interstitial lung disease": "ild", "Herpes zoster": "zoster", "Serious infections": "infection",
           "Venous thromboembolism": "vte", "Hepatotoxicity": "hepatic", "Neutropenia": "neutropenia"}
RISKS = ["ild", "zoster", "infection", "vte", "hepatic", "neutropenia"]
NEUT_FACTOR = {"10^9/L": 1.0, "G/l": 1.0, "/nl": 1.0, "10^3/µL": 1.0, "/mm3": 0.001, "cell/µL": 0.001, "/µl": 0.001}


def parse_full(s):
    """YYYY-MM-DD to Timestamp; anything else (partial, blank) to NaT."""
    return pd.to_datetime(s.where(s.str.len() == 10), format="%Y-%m-%d", errors="coerce")


def impute(s, day):
    full = parse_full(s)
    ym = s.where(s.str.len() == 7)
    imp = pd.to_datetime(ym + "-%02d" % day, format="%Y-%m-%d", errors="coerce")
    return full.fillna(imp)


class Pack:
    """The tables a solver reads, parsed once."""

    def __init__(self, listing, dosage, feed, labreg, dupreg, terms, changes):
        self.L = listing.copy()
        self.L["version_no"] = self.L["version_no"].astype(int)
        self.L["vrec"] = pd.to_datetime(self.L["version_receipt_date"])
        self.L["irec"] = pd.to_datetime(self.L["initial_receipt_date"])
        self.D = dosage.copy()
        self.F = feed.copy()
        self.R = labreg.copy()
        self.dup = set(dupreg["duplicate_case_no"])
        self.master_of = dict(zip(dupreg["duplicate_case_no"], dupreg["master_case_no"]))
        self.terms = terms
        self.changes = changes
        self._cache = {}

    def term_map(self, which="v4"):
        t = self.terms[self.terms["safety_concern"].isin(RISK_OF)]
        m = dict(zip(t["preferred_term"], t["safety_concern"].map(RISK_OF)))
        if which == "v3":
            for pt, ch in zip(self.changes["preferred_term"], self.changes["change"]):
                if ch == "Added":
                    m.pop(pt, None)
        return m

    def base(self, version="lock", dups="merge", study=False, postlock=False):
        key = (version, dups, study, postlock)
        if key in self._cache:
            return self._cache[key]
        L = self.L
        if version == "lock":
            v = L[L["vrec"] <= LOCK_TS]
            last = v.groupby("case_no")["version_no"].transform("max")
            v = v[v["version_no"] == last]
            if postlock:
                late = L[L["irec"] > LOCK_TS]
                lastl = late.groupby("case_no")["version_no"].transform("max")
                v = pd.concat([v, late[late["version_no"] == lastl]])
        elif version == "latest":
            last = L.groupby("case_no")["version_no"].transform("max")
            v = L[L["version_no"] == last]
            if not postlock:
                v = v[v["irec"] <= LOCK_TS]
        else:
            raise ValueError(version)
        if not study:
            v = v[v["report_type"] != "ST"]
        if dups == "merge":
            v = v[~v["case_no"].isin(self.dup)]
        self._cache[key] = v
        return v

    # ------------------------------------------------------------------ courses
    def lines(self):
        if "_lines" not in self._cache:
            D = self.D.copy()
            D["line_no"] = D["line_no"].astype(int)
            self._cache["_lines"] = {c: g.sort_values("line_no") for c, g in D.groupby("case_no")}
        return self._cache["_lines"]


def _course_start(lines, onset, origin, imp_day):
    """Start of the course (by `origin`) whose span holds the onset; None when a needed date is partial."""
    starts, stops = [], []
    for s, e in zip(lines["start_date"], lines["stop_date"]):
        if len(s) == 10:
            starts.append(pd.Timestamp(s))
        elif len(s) == 7 and imp_day:
            starts.append(pd.Timestamp(s + "-%02d" % imp_day))
        else:
            return None, None
        stops.append(pd.Timestamp(e) if len(e) == 10 else None)
    if origin == "listing":
        return starts[0], None
    groups = []
    for i in range(len(starts)):
        if i == 0:
            groups.append([i])
            continue
        prev_stop = stops[i - 1]
        gap = None if prev_stop is None else (starts[i] - prev_stop).days - 1
        if origin == "line":
            new = True
        elif origin == "gap0":
            new = gap is not None and gap >= 1
        else:
            new = gap is not None and gap > 28
        if new:
            groups.append([i])
        else:
            groups[-1].append(i)
    chosen = None
    for g in groups:
        st = starts[g[0]]
        if st <= onset:
            chosen = g
    if chosen is None:
        return None, None
    end = stops[chosen[-1]]
    return starts[chosen[0]], end


def lab_onsets(pack, risk, mode="rule", sex_of=None):
    """First sample meeting the case definition for each case in the PSP feed (annex 7 section 4)."""
    F = pack.F
    reg = pack.R
    if risk == "hepatic":
        f = F[F["analyte"] == "ALT"].copy()
        uln = reg[reg["analyte"] == "ALT"]
        f["val"] = f["value"].astype(float)
        f = f.merge(uln[["lab_code", "uln_male", "uln_female"]], on="lab_code", how="left")
        f["sex"] = f["case_no"].map(sex_of)
        u = np.where(f["sex"] == "M", f["uln_male"].astype(float), f["uln_female"].astype(float))
        if mode == "rule":
            q = f["val"] > 3 * u
        elif mode == "grade1":
            q = f["val"] > u
        elif mode == "units":
            q = f["val"] > 3 * 40.0
        else:
            raise ValueError(mode)
    else:
        f = F[F["analyte"] == "NEUT"].copy()
        f["val"] = f["value"].astype(float)
        if mode == "rule":
            q = f["val"] * f["unit"].map(NEUT_FACTOR) < 1.0
        elif mode == "grade1":
            lln = reg[reg["analyte"] == "NEUT"][["lab_code", "lln"]]
            f = f.merge(lln, on="lab_code", how="left")
            q = f["val"] < f["lln"].astype(float)
        elif mode == "units":
            q = f["val"] < 1.0
        else:
            raise ValueError(mode)
    f = f[q.values]
    f = f.assign(d=pd.to_datetime(f["sample_date"]))
    return f.groupby("case_no")["d"].min()


def tto(pack, risk, version="lock", dups="merge", study=False, postlock=False, terms="v4", origin="course",
        partial=None, lab="rule", per_term=False):
    """One row per case (or per mapped term) with onset day x and truncation time T for one risk."""
    v = pack.base(version, dups, study, postlock)
    tmap = pack.term_map(terms)
    rows = v[v["reaction_pt"].map(tmap) == risk]
    if rows.empty:
        return pd.DataFrame(columns=["case_no", "x", "T", "start", "onset"])
    on = impute(rows["onset_date"], partial) if partial else parse_full(rows["onset_date"])
    rows = rows.assign(on=on)
    if per_term:
        per = rows[["case_no", "on", "onset_date"]].copy()
    else:
        per = rows.groupby("case_no").agg(on=("on", "min"), blank=("onset_date", lambda s: (s == "").all()))
        per = per.reset_index()
    if risk in ("hepatic", "neutropenia") and lab != "drop":
        sex_of = dict(zip(v["case_no"], v["sex"]))
        lo = lab_onsets(pack, risk, lab, sex_of)
        if per_term:
            blank = per["onset_date"] == ""
        else:
            blank = per["blank"]
        fill = per["case_no"].map(lo)
        per.loc[blank, "on"] = fill[blank]
    per = per[per["on"].notna()]
    lines = pack.lines()
    out = []
    for c, onset in zip(per["case_no"], per["on"]):
        ln = lines.get(c)
        if ln is None:
            continue
        st, end = _course_start(ln, onset, origin, partial)
        if st is None:
            continue
        x = (onset - st).days + 1
        if x < 1:
            continue
        T = (LOCK_TS - st).days + 1
        out.append((c, x, T, st, onset, end))
    return pd.DataFrame(out, columns=["case_no", "x", "T", "start", "onset", "end"])


# ------------------------------------------------------------------ estimators over a tto table

def cuts(t, est="lb", p=(0.8, 0.95), **kw):
    x = t["x"].to_numpy(dtype=float)
    T = t["T"].to_numpy(dtype=float)
    if est == "lb":
        s, F = E.reverse_km(x, T)
        return [E.month_cut(s, F, q) for q in p]
    if est == "lb_interp":
        s, F = E.reverse_km(x, T)
        return [E.month_of(E.q_interp(s, F, q)) for q in p]
    if est == "lb_minus":
        d = kw["d"]
        s, F = E.reverse_km(x, T - d)
        return [E.month_cut(s, F, q) for q in p]
    if est in ("lb_month_floor", "lb_month_ceil"):
        xm = np.ceil(x / 30.0)
        Tm = np.floor(T / 30.0) if est == "lb_month_floor" else np.ceil(T / 30.0)
        s, F = E.reverse_km(xm, Tm)
        return [int(s[int(np.argmax(F >= q - 1e-12))]) for q in p]
    if est == "lb_window":
        end = t["end"]
        caused = kw["caused"]
        W = T.copy()
        for i, (e, c) in enumerate(zip(end, t["case_no"])):
            if e is not None and not pd.isna(e) and (kw.get("all") or c not in caused):
                W[i] = min(W[i], (e - t["start"].iloc[i]).days + 1)
        s, F = E.reverse_km(x, W)
        return [E.month_cut(s, F, q) for q in p]
    if est == "naive":
        return [E.month_of(E.np_quantile(x, q, kw.get("method", "inverted_cdf"))) for q in p]
    if est == "mature":
        sub = x[T >= kw["L"]]
        return [E.month_of(E.np_quantile(sub, q, kw.get("method", "inverted_cdf"))) for q in p]
    if est == "cohort":
        sub = x[t["start"] <= pd.Timestamp(kw["until"])]
        return [E.month_of(E.np_quantile(sub, q, kw.get("method", "inverted_cdf"))) for q in p]
    if est == "ipw":
        G = kw["G"]
        w = 1.0 / np.array([G(v) for v in x])
        s, F = E.empirical(x, w)
        return [E.month_cut(s, F, q) for q in p]
    if est == "weibull":
        k, lam = E.weibull_fit(x)
        return [E.month_of(E.weibull_q(k, lam, q)) for q in p]
    if est == "trunc_weibull":
        k, lam = E.trunc_weibull_fit(x, T)
        return [E.month_of(E.weibull_q(k, lam, q)) for q in p]
    if est == "trunc_lognormal":
        mu, sg = E.trunc_lognormal_fit(x, T)
        return [E.month_of(E.lognormal_q(mu, sg, q)) for q in p]
    raise ValueError(est)


def lb_detail(t, p):
    x = t["x"].to_numpy(dtype=float)
    T = t["T"].to_numpy(dtype=float)
    s, F = E.reverse_km(x, T)
    q = E.q_step(s, F, p)
    m = E.month_of(q)
    return dict(q=q, m=m, F_lo=E.cdf_at(s, F, 30 * (m - 1)), F_hi=E.cdf_at(s, F, 30 * m), qi=E.q_interp(s, F, p))


def ipw_G(pack, source="listing"):
    """Share of courses old enough to show an onset on day x, from every case's start in the database."""
    v = pack.base("lock", "merge", False, False)
    if source == "listing":
        st = parse_full(v.drop_duplicates("case_no")["therapy_start_date"]).dropna()
    else:
        D = pack.D
        firsts = D[D["case_no"].isin(set(v["case_no"]))].copy()
        firsts = firsts[firsts["start_date"].str.len() == 10]
        st = pd.to_datetime(firsts.groupby("case_no")["start_date"].max())
    T = np.sort(((LOCK_TS - st).dt.days + 1).to_numpy())
    n = len(T)

    def G(x):
        return (n - np.searchsorted(T, x, side="left")) / n
    return G


def case_counts(pack, risk, window="launch", version="lock", dups="merge", study=False, postlock=False, terms="v4"):
    v = pack.base(version, dups, study, postlock)
    tmap = pack.term_map(terms)
    rows = v[v["reaction_pt"].map(tmap) == risk]
    if window == "interval":
        rows = rows[rows["irec"] >= INTERVAL_START]
    return rows["case_no"].nunique()


# ------------------------------------------------------------------ exposure from supply (PSUR section 5)

class Supply:
    """Sell-in, call-offs, the national-code master and the xEVMPD presentations, parsed once."""

    def __init__(self, sellin, calloff, master, presentations):
        self.S = sellin.copy()
        self.S["qty"] = self.S["quantity"].astype(int)
        self.C = calloff.copy()
        self.M = master.copy()
        self.P = presentations  # eu number -> (strength mg, pack size)
        key = {}
        for code, ctype, mk, eu in zip(self.M["national_code"], self.M["code_type"], self.M["market"],
                                       self.M["eu_presentation"]):
            key[(mk, code.lstrip("0"))] = eu
        self.key = key
        self.S["eu"] = [key.get((c, n.lstrip("0"))) for c, n in zip(self.S["country"], self.S["national_code"])]
        self.C["eu"] = [key.get((c, g.lstrip("0"))) for c, g in zip(self.C["country"], self.C["gtin"])]
        self.C["date"] = pd.to_datetime(self.C["delivery_date"])

    def patient_days(self, window="launch", channels="all", pack="chain", cases=True, returns="net", foc="keep",
                     cutoff="lock", dose="tablet", strength=None):
        S = self.S
        if returns == "gross":
            S = S[S["billing_type"] != "RE"]
        if foc == "drop":
            S = S[S["billing_type"] != "FOC"]
        last = "2026-10" if cutoff == "export" else "2026-09"
        S = S[S["posting_period"] <= last]
        if window == "interval":
            S = S[S["posting_period"] >= "2025-10"]
        rows = [(eu, q) for eu, q in zip(S["eu"], S["qty"])]
        if channels == "all":
            Cc = self.C
            end = pd.Timestamp(2026, 10, 6) if cutoff == "export" else LOCK_TS
            Cc = Cc[Cc["date"] <= end]
            if window == "interval":
                Cc = Cc[Cc["date"] >= INTERVAL_START]
            f = 10 if cases else 1
            rows += [(eu, int(q) * f) for eu, q in zip(Cc["eu"], Cc["qty"])]
        days = 0.0
        for eu, q in rows:
            st, ps = self.P[eu]
            if strength is not None and st != strength:
                continue
            tabs = q * (28 if pack == "all28" else ps)
            days += tabs * (st / 15.0 if dose == "ddd" else 1.0)
        return days

    def patient_years(self, **kw):
        return self.patient_days(**kw) / 365.25


def read_presentations(xml_text):
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml_text)
    ns = {"x": root.tag.split("}")[0].strip("{")}
    out = {}
    for ap in root.findall("x:authorisedProduct", ns):
        eu = ap.find("x:authorisationNumber", ns).text
        st = int(float(ap.find("x:strength", ns).get("numerator")))
        ps = int(ap.find("x:package/x:packSize", ns).text)
        out[eu] = (st, ps)
    return out
