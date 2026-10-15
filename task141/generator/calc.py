"""The analysis from the shipped pack: the eligible first appearances and their screens, releases, windows and
new-offence arrests; each score's projected safety rate by every route on the ladder; the tier; and the three asks with
their stops. Reads only target/; deliver.py, checks.py and figures.json are written from it."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np
import openpyxl
import pandas as pd

import catalog as C
import common as K

DAY = dt.timedelta(days=1)
RELEASES = {"WPA", "UNSEC", "CUST", "BOND", "TS", "DISM", "CRTO"}


def _p(T, f):
    return os.path.join(T, f)


# ---------------------------------------------------------------------------------------------------- loading
def load(T):
    """Both first-appearance exports on one footing: booking numbers in the jail's form, case numbers in the new
    system's form, magistrates by employee number, charges by new code, the appearance time in Eastern wall time."""
    roster = pd.read_excel(_p(T, K.ROSTER), sheet_name="Magistrates", header=4, dtype=str)
    ini2emp = dict(zip(roster["Initials (legacy)"], roster["Employee no."]))
    xw = pd.read_excel(_p(T, K.CROSSWALK), sheet_name="Offense codes", header=4, dtype=str)
    leg2new = dict(zip(xw["Legacy code"], xw["New code"]))
    code_info = {r["New code"]: (r["G.S."], r["Class"]) for _, r in xw.iterrows()}

    leg = pd.read_csv(_p(T, K.FA_LEGACY), dtype=str, keep_default_na=False)
    a = pd.DataFrame({
        "fa_key": leg.APPEARANCE_NO,
        "sid": leg.SID,
        "booking": "B" + leg.BOOKING_NO.str[:2] + "-" + leg.BOOKING_NO.str[2:],
        "fa_t": pd.to_datetime(leg.APPEAR_DATE + " " + leg.APPEAR_TIME, format="%m/%d/%Y %H:%M"),
        "mag": leg.MAG.map(ini2emp),
        "cases": leg.CASE_NOS.str.replace(" ", "", regex=False).str.split(";"),
        "codes": leg.CHARGE_CODES.str.split(";").apply(lambda xs: [leg2new[x] for x in xs]),
        "detainer": leg.HOLD_OTHER == "Y",
        "cond": leg.CONDITION.map({"WPA": "WRITTEN_PROMISE", "UNSEC": "UNSECURED_BOND", "CUST": "CUSTODY_RELEASE",
                                   "SEC": "SECURED_BOND"}),
        "last": leg.DEF_LAST, "first": leg.DEF_FIRST, "dob": pd.to_datetime(leg.DOB, format="%m/%d/%Y").dt.date,
    })
    new = pd.read_csv(_p(T, K.FA_NEW), dtype=str, keep_default_na=False)
    chg = pd.read_csv(_p(T, K.FA_CHARGES), dtype=str, keep_default_na=False)
    cg = chg.groupby("fa_id")
    codes = cg.offense_code.apply(list)
    cnos = cg.case_number.apply(lambda s: list(dict.fromkeys(s)))
    b = pd.DataFrame({
        "fa_key": new.fa_id, "sid": new.sid, "booking": new.booking_number,
        "fa_t": pd.to_datetime(new.appearance_at, format="%Y-%m-%d %H:%M"),
        "mag": new.judicial_official_id,
        "cases": new.fa_id.map(cnos), "codes": new.fa_id.map(codes),
        "detainer": new.detainer_agency != "",
        "cond": new.release_condition,
        "last": new.defendant_last.str.upper(), "first": new.defendant_first.str.upper(),
        "dob": pd.to_datetime(new.dob, format="%Y-%m-%d").dt.date,
    })
    fa = pd.concat([a, b], ignore_index=True)
    fa["eligible"] = fa.apply(lambda r: (not r.detainer) and all(
        code_info[c][1] in C.MISD_CLASSES and not C.in_appendix_b(code_info[c][0]) for c in r.codes), axis=1)
    fa["felony"] = fa.codes.apply(lambda cs: any(code_info[c][1] not in C.MISD_CLASSES + ("DWI",) for c in cs))
    return fa


def attach_screens(T, fa):
    sc = pd.read_csv(_p(T, K.SCREENS), dtype=str, keep_default_na=False)
    sc["t"] = pd.to_datetime(sc.screened_at, format="%m/%d/%Y %I:%M %p")
    sc["nca"] = sc.nca_score.astype(int)
    sc["fta"] = sc.fta_score.astype(int)
    by_bk = sc[sc.booking_number != ""].set_index("booking_number")
    fa = fa.copy()
    fa["nca"] = fa.booking.map(by_bk.nca)
    fa["fta"] = fa.booking.map(by_bk.fta)
    # paper screens: no booking number; the defendant's state number and the next appearance within twelve hours
    paper = sc[sc.booking_number == ""]
    if len(paper):
        idx = fa.sort_values("fa_t").groupby("sid")
        groups = {k: g for k, g in idx}
        for _, s in paper.iterrows():
            g = groups.get(s.sid)
            if g is None:
                continue
            m = g[(g.fa_t >= s.t) & (g.fa_t <= s.t + pd.Timedelta(hours=12))]
            if len(m):
                k = m.index[0]
                fa.at[k, "nca"] = s.nca
                fa.at[k, "fta"] = s.fta
    return fa


def attach_release(T, fa):
    """Released within 24 hours of the appearance: the booking's first release in the jail export (UTC, read in
    Eastern time) of a releasing type, no later than a day after the appearance."""
    j = pd.read_csv(_p(T, K.JAIL), dtype=str, keep_default_na=False)
    j = j[j.booking_type == "NEW"]
    rel = j.set_index("booking_number")
    fa = fa.copy()
    rt = fa.booking.map(rel.release_type)
    ru = fa.booking.map(rel.released_utc)
    loc = ru.apply(lambda s: K.utc_to_eastern(dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")) if s else None)
    fa["rel_t"] = pd.to_datetime(loc)
    fa["rel_type"] = rt
    fa["released24"] = rt.isin(RELEASES) & (fa.rel_t <= fa.fa_t + pd.Timedelta(hours=24))
    return fa


def attach_outcomes(T, fa, window_days=365, cap="last", start_from="rel24"):
    """The window from the day after release to 365 days or the disposition of the last charge, whichever first; a
    new-offence arrest is an arrest of type NEW for an offence dated inside it."""
    cases = pd.read_csv(_p(T, K.CASES), dtype=str, keep_default_na=False)
    disp = dict(zip(cases.case_number, cases.disposition_date))
    ar = pd.read_csv(_p(T, K.ARRESTS), dtype=str, keep_default_na=False)
    ar = ar[ar.arrest_type == "NEW"].drop_duplicates(["arrest_id"])
    ar["off"] = pd.to_datetime(ar.offense_date).dt.date
    offs = ar.groupby("sid").off.apply(lambda s: sorted(s))
    fa = fa.copy()
    out = []
    for r in fa.itertuples():
        if not r.released24:
            out.append(np.nan)
            continue
        s = r.rel_t.date()
        ds = [disp.get(c, "") for c in r.cases]
        if cap == "none" or any(d == "" for d in ds):
            dend = None
        else:
            dl = [dt.date.fromisoformat(d) for d in ds]
            dend = max(dl) if cap == "last" else min(dl)
        e = s + dt.timedelta(days=window_days)
        if dend is not None:
            e = min(e, dend)
        lst = offs.get(r.sid, [])
        out.append(float(any(s < o <= e for o in lst)))
    fa["y"] = out
    return fa


def history(fa, lo=K.HIST_START, hi=K.HIST_LAST):
    h = fa[(fa.fa_t.dt.date >= lo) & (fa.fa_t.dt.date <= hi) & fa.eligible & fa.nca.notna()].copy()
    h["nca"] = h.nca.astype(int)
    h["A"] = np.where(h.released24, h.y.fillna(0.0), 0.0)
    return h


# ---------------------------------------------------------------------------------------------------- estimates
def naive(h):
    return {s: float(g[g.released24].y.mean()) for s, g in h.groupby("nca")}


def held_as_safe(h):
    return {s: float(g.A.mean()) for s, g in h.groupby("nca")}


def held_as_arrested(h):
    return {s: float((g.A + (~g.released24).astype(float)).mean()) for s, g in h.groupby("nca")}


def mag_table(h, s, key="mag"):
    g = h[h.nca == s].groupby(key).agg(n=("A", "size"), R=("released24", "mean"), A=("A", "mean"))
    return g


def leniency_wls(h, key="mag", weighted=True, quad=False):
    out = {}
    for s in range(1, 7):
        g = mag_table(h, s, key)
        X = np.c_[np.ones(len(g)), g.R.values]
        if quad:
            X = np.c_[X, g.R.values ** 2]
        w = np.sqrt(g.n.values) if weighted else np.ones(len(g))
        b = np.linalg.lstsq(X * w[:, None], g.A.values * w, rcond=None)[0]
        out[s] = float(b.sum())
    return out


def leniency_iv(h):
    """Leave-out leniency as the instrument for release, case by case; the new-offence rate at full release from the
    pooled point along the instrumented slope."""
    out = {}
    for s in range(1, 7):
        g = h[h.nca == s]
        tot = g.groupby("mag").released24.transform("sum")
        cnt = g.groupby("mag").released24.transform("size")
        z = (tot - g.released24) / (cnt - 1)
        zc = z - z.mean()
        sl = float((zc * (g.A - g.A.mean())).sum() / (zc * (g.released24 - g.released24.mean())).sum())
        out[s] = float(g.A.mean() + sl * (1 - g.released24.mean()))
    return out


def leniency_halves(h):
    out = {}
    for s in range(1, 7):
        g = h[h.nca == s]
        lr = g.groupby("mag").released24.mean().sort_values(ascending=False)
        top = set(lr.index[: len(lr) // 2])
        a, b = g[g.mag.isin(top)], g[~g.mag.isin(top)]
        late = (a.A.mean() - b.A.mean()) / (a.released24.mean() - b.released24.mean())
        out[s] = float(g.A.mean() + late * (1 - g.released24.mean()))
    return out


def released_rate_line(h):
    """Each magistrate's released defendants' rate on his release share, weighted by the released, read at full
    release."""
    out = {}
    for s in range(1, 7):
        g = h[h.nca == s]
        t = g.groupby("mag").agg(n=("A", "size"), R=("released24", "mean"), k=("released24", "sum"), a=("A", "sum"))
        t = t[t.k > 0]
        m = t.a / t.k
        X = np.c_[np.ones(len(t)), t.R.values]
        w = np.sqrt(t.k.values)
        b = np.linalg.lstsq(X * w[:, None], m.values * w, rcond=None)[0]
        out[s] = float(b.sum())
    return out


def leniency_iv_all(h):
    """Leave-out leniency over every eligible appearance the magistrate heard (all scores) as the instrument, the
    slope estimated within the score."""
    out = {}
    tot = h.groupby("mag").released24.transform("sum")
    cnt = h.groupby("mag").released24.transform("size")
    z_all = (tot - h.released24) / (cnt - 1)
    for s in range(1, 7):
        sel = (h.nca == s).values
        g = h[sel]
        z = z_all[sel]
        zc = z - z.mean()
        sl = float((zc * (g.A - g.A.mean())).sum() / (zc * (g.released24 - g.released24.mean())).sum())
        out[s] = float(g.A.mean() + sl * (1 - g.released24.mean()))
    return out


def lenient_fifth(h):
    """The most lenient fifth of the magistrates (by release share across their eligible appearances): their own
    released defendants' rate at each score."""
    lr = h.groupby("mag").released24.mean().sort_values(ascending=False)
    top = set(lr.index[: max(1, len(lr) // 5)])
    return {s: float(g[g.mag.isin(top) & g.released24].y.mean()) for s, g in h.groupby("nca")}


def safety(rates):
    return {s: 1.0 - v for s, v in rates.items()}


def tier(saf, floor=K.FLOOR):
    k = 0
    for s in range(1, 7):
        if saf.get(s, 0) >= floor:
            k = s
        else:
            break
    return k


def logistic_on_released(h):
    """A logistic model of a new-offence arrest on the released defendants' charge mix and the appearance month,
    averaged over every eligible appearance at the score (an adjustment for what the record shows)."""
    from scipy.optimize import minimize
    rel = h[h.released24].copy()
    feats = lambda d: np.c_[np.ones(len(d)), *[(d.nca == s).astype(float).values for s in range(2, 7)],
                            d.n_charges.values, d.has_drug.values, d.has_theft.values]
    X, y = feats(rel), rel.y.values

    def nll(b):
        z = X @ b
        return float(np.sum(np.logaddexp(0, z)) - y @ z)

    def grad(b):
        p = 1 / (1 + np.exp(-(X @ b)))
        return X.T @ (p - y)
    b = minimize(nll, np.zeros(X.shape[1]), jac=grad, method="L-BFGS-B").x
    p_all = 1 / (1 + np.exp(-(feats(h) @ b)))
    return {s: float(p_all[(h.nca == s).values].mean()) for s in range(1, 7)}


def add_features(h):
    h = h.copy()
    h["n_charges"] = h.codes.apply(len)
    h["has_drug"] = h.codes.apply(lambda cs: float(any(c.startswith("35") for c in cs)))
    h["has_theft"] = h.codes.apply(lambda cs: float(any(c[:2] in ("25", "23", "26", "24") for c in cs)))
    return h


def ipw_on_released(h):
    """The released defendants reweighted to every eligible appearance at the score by the inverse of the release
    share in their cell of the observed record (score, charge count, drug, theft)."""
    out = {}
    hh = h.copy()
    hh["cell"] = list(zip(hh.nca, hh.n_charges.clip(upper=3), hh.has_drug, hh.has_theft))
    p = hh.groupby("cell").released24.transform("mean")
    hh["w"] = np.where(hh.released24, 1 / p, 0.0)
    for s, g in hh.groupby("nca"):
        r = g[g.released24]
        out[s] = float((r.w * r.y).sum() / r.w.sum())
    return out


def ladder(fa, h):
    """Every rung's safety by score and tier."""
    hf = add_features(h)
    R = {}
    R["R0 released defendants' rate"] = safety(naive(h))
    lo_last = K.HIST_LAST - dt.timedelta(days=364)
    R["R0b latest closed year"] = safety(naive(h[h.fa_t.dt.date >= lo_last]))
    R["R0c held as not arrested"] = safety(held_as_safe(h))
    R["R1 logistic on the released"] = safety(logistic_on_released(hf))
    R["R1b reweighted to the eligible"] = safety(ipw_on_released(hf))
    R["R2 held as arrested"] = safety(held_as_arrested(h))
    R["R3 leniency gradient (golden)"] = safety(leniency_wls(h))
    R["V ols"] = safety(leniency_wls(h, weighted=False))
    R["V leave-out instrument"] = safety(leniency_iv(h))
    R["V halves"] = safety(leniency_halves(h))
    R["V quadratic"] = safety(leniency_wls(h, quad=True))
    R["V released-rate line"] = safety(released_rate_line(h))
    R["V instrument, all scores"] = safety(leniency_iv_all(h))
    R["V lenient fifth"] = safety(lenient_fifth(h))
    return R


# ---------------------------------------------------------------------------------------------------- the asks
_CACHE = {}


def jail_segments(T):
    if ("jail", T) in _CACHE:
        return _CACHE[("jail", T)].copy()
    j = _jail_segments(T)
    _CACHE[("jail", T)] = j
    return j.copy()


def _jail_segments(T):
    j = pd.read_csv(_p(T, K.JAIL), dtype=str, keep_default_na=False)
    for c in ("booked_utc", "released_utc"):
        j[c + "_loc"] = j[c].apply(lambda s: K.utc_to_eastern(dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")) if s else None)
    return j


def halsey_stays(T):
    wb = openpyxl.load_workbook(_p(T, K.HALSEY), data_only=True)
    rows = []
    for ws in wb.worksheets:
        hdr = None
        for row in ws.iter_rows(values_only=True):
            if row and row[0] == "Halsey booking":
                hdr = row
                continue
            if hdr and row and row[0] and str(row[0]).startswith("HC"):
                rows.append(dict(hbk=row[0], name=row[1], dob=row[2].date() if hasattr(row[2], "date") else row[2],
                                 ref=row[3] or "", din=row[4].date() if hasattr(row[4], "date") else row[4],
                                 dout=(row[5].date() if hasattr(row[5], "date") else row[5]) if row[5] else None,
                                 days=int(row[6]), sheet=ws.title))
    df = pd.DataFrame(rows)
    st = df.groupby("hbk").agg(name=("name", "first"), dob=("dob", "first"), ref=("ref", "first"), din=("din", "min"),
                               dout=("dout", lambda s: max([x for x in s if x is not None]) if any(x is not None for x in s) else None),
                               billed=("days", "sum"))
    return st.reset_index(), df


def _utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ") if s else None


def ask_a(T, fa, mode="golden"):
    """Bed-days in custody to 30 September 2026 of the eligible defendants held after a first appearance in the year,
    by score. golden: each stay from booking to final release through annex moves (TRF), a boarding at Halsey (BO)
    and a return (BI), or to the date out on Halsey's bills for a defendant released there; one bed-day for each
    Eastern midnight held, the count at 00:00 on 30 September the last. The stops: S1 BO read as the release; S2 BO
    chained to the defendant's next booking; S3 Halsey's billed days for the boarded part; S4 UTC midnights; S5 BO
    chained to a return, else read as the release; S6 days or part of a day; S7 Halsey's month lines each counted
    from their dates."""
    j = jail_segments(T)
    hs, hlines = halsey_stays(T)
    yr = fa[(fa.fa_t.dt.date >= K.FY26_START) & (fa.fa_t.dt.date <= K.EXTRACT_END) & fa.eligible & fa.nca.notna()
            & ~fa.released24].copy()
    jj = j[j.sid.isin(set(yr.sid))]
    by_sid = {k: g.sort_values("booked_utc_loc") for k, g in jj.groupby("sid")}
    names = {}
    for r in hs.itertuples():
        names.setdefault((r.name, r.dob), []).append(r)
    lines_by = {k: g for k, g in hlines.groupby("hbk")}
    end_t = K.d2dt(K.EXTRACT_END + DAY)
    res = {}

    def nat(x):
        return x is None or pd.isna(x)
    for r in yr.itertuples():
        g = by_sid[r.sid]
        cur = g[g.booking_number == r.booking].iloc[0]
        pieces = []                 # (start, end or None, where) in Eastern time; where DC or HC
        hstay = None
        start = cur.booked_utc_loc
        while True:
            typ, end = cur.release_type, cur.released_utc_loc
            if typ == "TRF":
                nxt = g[(g.booking_type == "TRF") & (g.booked_utc_loc == end)]
                cur = nxt.iloc[0]
                continue
            if typ == "BO" and mode != "S1":
                if mode == "S2":
                    later = g[g.booked_utc_loc > end]
                    if len(later):
                        cur = later.iloc[0]
                        continue
                    pieces.append((start, None, "DC"))
                    break
                ret = g[(g.booking_type == "BI") & (g.booked_utc_loc > end)
                        & (g.booked_utc_loc <= end + pd.Timedelta(days=60))]
                if len(ret):
                    pieces.append((start, end, "DC"))
                    nb = ret.iloc[0]
                    pieces.append((end, nb.booked_utc_loc, "HC"))
                    cur, start = nb, nb.booked_utc_loc
                    continue
                if mode == "S5":
                    pieces.append((start, end, "DC"))
                    break
                cand = [c for c in names.get((r.last + ", " + r.first, r.dob), []) if c.din == end.date()]
                pieces.append((start, end, "DC"))
                hstay = cand[0]
                hend = None if hstay.dout is None or pd.isna(hstay.dout) else K.d2dt(hstay.dout) + dt.timedelta(hours=12)
                pieces.append((end, hend, "HC"))
                break
            pieces.append((start, None if nat(end) else end, "DC"))
            break
        cnt = 0
        if mode in ("golden", "S1", "S2", "S5"):
            a = pieces[0][0]
            b = pieces[-1][1]
            b = end_t if b is None else b
            cnt = sum(1 for d in K.midnights(a.to_pydatetime() if hasattr(a, "to_pydatetime") else a,
                                             b.to_pydatetime() if hasattr(b, "to_pydatetime") else b) if d <= K.EXTRACT_END)
        elif mode == "S4":
            # the same stays, the midnights read off the export's UTC clock
            a = K.eastern_to_utc(pieces[0][0].to_pydatetime())
            b = pieces[-1][1]
            b = K.d2dt(K.EXTRACT_END + DAY) + dt.timedelta(hours=4) if b is None else K.eastern_to_utc(
                b.to_pydatetime() if hasattr(b, "to_pydatetime") else b)
            cnt = sum(1 for d in K.midnights(a, b) if d <= K.EXTRACT_END)
        elif mode == "S6":
            a = pieces[0][0]
            b = pieces[-1][1]
            last = K.EXTRACT_END if b is None else min(b.date(), K.EXTRACT_END)
            cnt = (last - a.date()).days + 1
        elif mode in ("S3", "S7"):
            for (a, b, where) in pieces:
                if where == "DC":
                    bb = end_t if b is None else b
                    cnt += sum(1 for d in K.midnights(a.to_pydatetime() if hasattr(a, "to_pydatetime") else a,
                                                      bb.to_pydatetime() if hasattr(bb, "to_pydatetime") else bb)
                               if d <= K.EXTRACT_END)
                else:
                    din = a.date()
                    # the Halsey bills' lines for this stay: by name, date of birth and date in
                    hits = [c for c in names.get((r.last + ", " + r.first, r.dob), []) if c.din == din]
                    if not hits:
                        continue
                    lines = lines_by[hits[0].hbk]
                    if mode == "S3":
                        cnt += int(lines.days.sum())
                    else:
                        for ln in lines.itertuples():
                            if ln.dout is not None and not pd.isna(ln.dout):
                                out = ln.dout
                            else:
                                m0 = dt.datetime.strptime(ln.sheet, "%b %Y").date()
                                out = min(dt.date(m0.year + (m0.month == 12), m0.month % 12 + 1, 1) - DAY, K.EXTRACT_END)
                            cnt += (out - ln.din).days
        res[int(r.nca)] = res.get(int(r.nca), 0) + cnt
    return res


def case_family(T):
    cases = pd.read_csv(_p(T, K.CASES), dtype=str, keep_default_na=False)
    sup = cases[cases.district_case_ref != ""]
    fam = {}
    for r in sup.itertuples():
        fam.setdefault(r.district_case_ref, []).append(r.case_number)
    return cases, fam


def ask_b(T, fa, mode="golden"):
    """Releases at first appearances from 1 October 2025 to 30 June 2026 followed within 90 days by an order for
    arrest for a failure to appear on those charges, by failure-to-appear score: (count, releases)."""
    ev = pd.read_csv(_p(T, K.EVENTS), dtype=str, keep_default_na=False)
    fta = ev[ev.event_code == "FTA"]
    by_case = fta.groupby("case_number").event_date.apply(lambda s: sorted(dt.date.fromisoformat(x) for x in s))
    cases, fam = case_family(T)
    party = dict(zip(cases.case_number, cases.party_id))
    by_party = cases.groupby("party_id").case_number.apply(list)
    yr = fa[(fa.fa_t.dt.date >= K.FY26_START) & (fa.fa_t.dt.date <= K.ASKB_LAST) & fa.released24 & fa.fta.notna()]
    out = {}
    for r in yr.itertuples():
        s = r.rel_t.date()
        e = s + dt.timedelta(days=90)
        cs = list(r.cases)
        if mode == "golden":
            for c in list(cs):
                cs += fam.get(c, [])
        elif mode == "S2":
            ps = {party.get(c) for c in cs}
            cs = sorted({x for p in ps for x in by_party.get(p, [])})
        hit = any(s <= d <= e for c in cs for d in by_case.get(c, []))
        k = int(r.fta)
        n, m = out.get(k, (0, 0))
        out[k] = (n + int(hit), m + 1)
    return out


def ask_c(T, fa, mode="golden", eligible_only=False):
    """Days on electronic monitoring to 30 September 2026 of the defendants released at a first appearance in the
    year, by new-criminal-activity score."""
    em = pd.read_csv(_p(T, K.EM), dtype=str, keep_default_na=False)
    em["s"] = pd.to_datetime(em.enroll_date, format="%m/%d/%Y").dt.date
    em["e"] = em.end_date.apply(lambda x: dt.datetime.strptime(x, "%m/%d/%Y").date() if x else None)
    em["dob_d"] = pd.to_datetime(em.dob, format="%m/%d/%Y").dt.date
    yr = fa[(fa.fa_t.dt.date >= K.FY26_START) & (fa.fa_t.dt.date <= K.EXTRACT_END) & fa.released24].copy()
    if eligible_only:
        yr = yr[yr.eligible]
    case2rel = {}
    for r in yr.itertuples():
        for c in r.cases:
            case2rel[c] = r.Index
    namekey = {}
    for r in yr.itertuples():
        namekey.setdefault((r.last, r.first, r.dob), []).append((r.rel_t.date(), r.Index))
    # one row per enrollment: its dates (the end from the last line that carries one)
    enr = em.groupby("participant_no").agg(last=("last_name", "first"), first=("first_name", "first"),
                                           dob=("dob_d", "first"), case=("court_case", "max"), s=("s", "first"),
                                           e=("e", lambda x: max([v for v in x if v is not None]) if any(v is not None for v in x) else None),
                                           billed=("billable_days", lambda x: int(sum(int(v) for v in x))),
                                           lines=("billable_days", "size"))
    owner = {}
    for pno, r in enr.iterrows():
        k = case2rel.get(r.case) if r.case else None
        if k is None:
            c = namekey.get((r["last"].upper(), r["first"].upper(), r.dob), [])
            c = [x for x in c if x[0] <= r.s]
            if c:
                k = max(c)[1]
        owner[pno] = k if (k is not None and not pd.isna(yr.loc[k, "nca"])) else None
    res = {}
    if mode == "S1":
        for pno, r in enr.iterrows():
            k = owner[pno]
            if k is None:
                continue
            sc = int(yr.loc[k, "nca"])
            res[sc] = res.get(sc, 0) + r.billed
        return res
    if mode == "S2":
        for _, ln in em.iterrows():
            k = owner.get(ln.participant_no)
            if k is None:
                continue
            e = ln.e or K.EXTRACT_END
            sc = int(yr.loc[k, "nca"])
            res[sc] = res.get(sc, 0) + (e - ln.s).days + 1
        return res
    days = {}
    for pno, r in enr.iterrows():
        k = owner[pno]
        if k is None:
            continue
        e = r.e or K.EXTRACT_END
        span = {r.s + dt.timedelta(days=i) for i in range((e - r.s).days + 1)}
        if mode == "S3":
            days.setdefault(k, []).append(len(span))
        else:
            days.setdefault(k, set()).update(span)
    for k, v in days.items():
        sc = int(yr.loc[k, "nca"])
        res[sc] = res.get(sc, 0) + (sum(v) if mode == "S3" else len(v))
    return res


def everything(T):
    fa = load(T)
    fa = attach_screens(T, fa)
    fa = attach_release(T, fa)
    fa = attach_outcomes(T, fa)
    h = history(fa)
    return fa, h
