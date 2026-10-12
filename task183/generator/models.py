"""Every forecast of 2027 cable failures by feeder the ladder and the grid need, computed from the two shipped
files the main call reads (the work orders and the GIS section register) as data frames. Used by checks.py on the
built pack; verify.py carries its own code."""
import datetime as dt

import numpy as np
import pandas as pd

FEEDERS = ["HR12", "HR14", "ML03", "ML07", "QH21", "QH22", "SP05", "SP09"]
CABLE = ("INS", "SPL", "TRM")
ARCH0 = dt.date(2012, 1, 1)
CUT = dt.date(2026, 9, 30)
W5 = (dt.date(2021, 10, 1), dt.date(2026, 9, 30))


def prep(wo, reg, causes=CABLE):
    """Failures per section (sorted dates) under the cause filter, and the register keyed by section."""
    w = wo if causes is None else wo[wo["cause_code"].isin(causes)]
    fails = {}
    for sid, d in zip(w["section_id"], w["fault_date"]):
        fails.setdefault(sid, []).append(d)
    for v in fails.values():
        v.sort()
    return w, fails


def exposures(reg, fails, start=ARCH0, end=CUT):
    """Section-year exposure split by calendar year and by failures so far (exact time), with the failures that
    end each piece: rows (section_id, feeder, insulation, install_year, year, k, years, events). A failure ends its
    piece and moves the section to the next count; the section's failures before the window still count in k."""
    rows = []
    for r in reg.itertuples(index=False):
        lo = max(r.install_date, start)
        ret = r.retired_date
        hi = end if (ret is None or (isinstance(ret, float) and np.isnan(ret)) or pd.isna(ret)) else min(ret, end)
        if hi <= lo:
            continue
        fl = fails.get(r.section_id, [])
        cuts = sorted(set([lo, hi] + [dt.date(y, 1, 1) for y in range(lo.year + 1, hi.year + 1)] +
                          [d for d in fl if lo < d < hi]))
        for a, b in zip(cuts[:-1], cuts[1:]):
            # a piece runs from a to b and ends at a failure on b; a failure on a ended the piece before (so it is
            # already in k), except on the window's first day, where it belongs to the first piece
            k = sum(1 for d in fl if d < a or (d == a and a != lo))
            ev = sum(1 for d in fl if a < d <= b or (d == a == lo))
            rows.append((r.section_id, r.feeder_id, r.insulation, r.install_date.year, a.year, k,
                         (b - a).days / 365.25, ev))
    return pd.DataFrame(rows, columns=["section_id", "feeder_id", "insulation", "install_year", "year", "k", "years",
                                       "events"])


def stock(reg, fails, pool="in_service"):
    s = reg[reg["status"] == "IS"] if pool == "in_service" else reg
    s = s.copy()
    s["k"] = [len(fails.get(x, [])) for x in s["section_id"]]
    s["age27"] = 2027 - s["install_date"].map(lambda d: d.year)
    return s


def band(age, width=10):
    return np.minimum(np.maximum(age, 0) // width, 70 // width)


def rank(fc):
    order = sorted(fc, key=lambda f: (-fc[f], f))
    lead = fc[order[0]] / fc[order[1]] if fc[order[1]] > 0 else float("inf")
    return order, lead


def history(wo, reg, causes=CABLE, pool="in_service", years=5):
    w, _ = prep(wo, reg, causes)
    lo = dt.date(W5[1].year - years, 10, 1)
    w = w[(w["fault_date"] >= lo) & (w["fault_date"] <= W5[1])]
    if pool == "in_service":
        w = w[w["section_id"].isin(set(reg.loc[reg["status"] == "IS", "section_id"]))]
    feeder = dict(zip(reg["section_id"], reg["feeder_id"]))
    c = w["section_id"].map(feeder).value_counts()
    return {f: float(c.get(f, 0)) / years for f in FEEDERS}


def rates_by(ex, keys):
    g = ex.groupby(keys)[["years", "events"]].sum()
    g["rate"] = g["events"] / g["years"].where(g["years"] > 0)
    return g


def attributes(wo, reg, causes=CABLE, pool="in_service", start=ARCH0, width=10):
    _, fails = prep(wo, reg, causes)
    ex = exposures(reg, fails, start=start)
    ex["band"] = band(ex["year"] - ex["install_year"], width)
    r = rates_by(ex, ["insulation", "band"])["rate"]
    ins_r = rates_by(ex, ["insulation"])["rate"]
    st = stock(reg, fails, pool)
    st["band"] = band(st["age27"], width)
    fc = {f: 0.0 for f in FEEDERS}
    for row in st.itertuples(index=False):
        v = r.get((row.insulation, row.band), np.nan)
        if not np.isfinite(v):
            v = ins_r.get(row.insulation)
        fc[row.feeder_id] += v
    return fc


def kmodel(wo, reg, causes=CABLE, pool="in_service", start=ARCH0, top=3):
    _, fails = prep(wo, reg, causes)
    ex = exposures(reg, fails, start=start)
    ex["kc"] = np.minimum(ex["k"], top)
    r = rates_by(ex, ["kc"])["rate"]
    st = stock(reg, fails, pool)
    fc = {f: 0.0 for f in FEEDERS}
    for row in st.itertuples(index=False):
        fc[row.feeder_id] += r.get(min(row.k, top), r.iloc[-1])
    return fc, r


def k_attributes(wo, reg, causes=CABLE, pool="in_service", start=ARCH0, width=10, min_years=30.0):
    """Rate by (insulation, age band, failures so far); a thin cell borrows the insulation-and-age rate times the
    network's ratio for its failure count."""
    _, fails = prep(wo, reg, causes)
    ex = exposures(reg, fails, start=start)
    ex["band"] = band(ex["year"] - ex["install_year"], width)
    ex["kc"] = np.minimum(ex["k"], 3)
    cell = rates_by(ex, ["insulation", "band", "kc"])
    ab = rates_by(ex[ex["kc"] == 0], ["insulation", "band"])["rate"]
    kr = rates_by(ex, ["kc"])["rate"]
    st = stock(reg, fails, pool)
    st["band"] = band(st["age27"], width)
    fc = {f: 0.0 for f in FEEDERS}
    for row in st.itertuples(index=False):
        kc = min(row.k, 3)
        key = (row.insulation, row.band, kc)
        if key in cell.index and cell.loc[key, "years"] >= min_years:
            v = cell.loc[key, "rate"]
        else:
            base = ab.get((row.insulation, row.band), np.nan)
            if not np.isfinite(base):
                base = kr.get(0)
            v = base * kr.get(kc) / kr.get(0) if kc else base
            if kc >= 2:
                v = kr.get(kc)
        fc[row.feeder_id] += v
    return fc


def poisson_glm(wo, reg, causes=CABLE, pool="in_service", start=ARCH0, feeder_effect=False, attrs=True):
    """Log-linear Poisson regression of failures on section-year exposure: failure-count class, plus insulation
    and age band (attrs) and the feeder (feeder_effect). Fitted by iteratively reweighted least squares."""
    _, fails = prep(wo, reg, causes)
    ex = exposures(reg, fails, start=start)
    ex = ex[ex["years"] > 0].copy()
    ex["kc"] = np.minimum(ex["k"], 3).astype(str)
    ex["band"] = band(ex["year"] - ex["install_year"]).astype(str)
    cols = ["kc"] + (["insulation", "band"] if attrs else []) + (["feeder_id"] if feeder_effect else [])
    X = pd.get_dummies(ex[cols], drop_first=True).astype(float)
    X.insert(0, "const", 1.0)
    y = ex["events"].to_numpy(float)
    off = np.log(ex["years"].to_numpy(float))
    beta = np.zeros(X.shape[1])
    beta[0] = np.log(y.sum() / ex["years"].sum())
    A = X.to_numpy()
    pen = 1e-3 * np.eye(A.shape[1])
    pen[0, 0] = 0.0
    for _ in range(100):
        eta = np.clip(A @ beta + off, -30, 30)
        mu = np.exp(eta)
        grad = A.T @ (y - mu) - pen @ beta
        H = A.T @ (A * mu[:, None]) + pen
        step = np.linalg.solve(H, grad)
        beta = beta + step
        if np.max(np.abs(step)) < 1e-9:
            break
    st = stock(reg, fails, pool)
    st["kc"] = np.minimum(st["k"], 3).astype(str)
    st["band"] = band(st["age27"]).astype(str)
    S = pd.get_dummies(st[cols], drop_first=False).astype(float)
    S = S.reindex(columns=X.columns, fill_value=0.0)
    S["const"] = 1.0
    pred = np.exp(S.to_numpy() @ beta)
    fc = {f: 0.0 for f in FEEDERS}
    for f, p in zip(st["feeder_id"], pred):
        fc[f] += p
    return fc


def kmodel_window_only(wo, reg, causes=CABLE, start=W5[0]):
    """Failure counts taken only inside the window (failures before it unseen), rates on the window's exposure."""
    w, _ = prep(wo, reg, causes)
    w = w[w["fault_date"] >= start]
    fails = {}
    for sid, d in zip(w["section_id"], w["fault_date"]):
        fails.setdefault(sid, []).append(d)
    for v in fails.values():
        v.sort()
    ex = exposures(reg, fails, start=start)
    ex["kc"] = np.minimum(ex["k"], 3)
    r = rates_by(ex, ["kc"])["rate"]
    st = stock(reg, fails)
    fc = {f: 0.0 for f in FEEDERS}
    for row in st.itertuples(index=False):
        fc[row.feeder_id] += r.get(min(row.k, 3), r.iloc[-1])
    return fc


def kmodel_inherited(wo, reg, causes=CABLE):
    """A replacement section inherits its predecessor's failures (the predecessor pointer followed back)."""
    w, fails = prep(wo, reg, causes)
    pred = dict(zip(reg["section_id"], reg["predecessor_section_id"]))
    inh = {}
    for sid in reg["section_id"]:
        out, x = list(fails.get(sid, [])), pred.get(sid) or ""
        while x:
            out = fails.get(x, []) + out
            x = pred.get(x) or ""
        if out:
            inh[sid] = sorted(out)
    ex = exposures(reg, inh)
    ex["kc"] = np.minimum(ex["k"], 3)
    r = rates_by(ex, ["kc"])["rate"]
    st = stock(reg, inh)
    fc = {f: 0.0 for f in FEEDERS}
    for row in st.itertuples(index=False):
        fc[row.feeder_id] += r.get(min(row.k, 3), r.iloc[-1])
    return fc


def trend(wo, reg, causes=CABLE, pool="in_service"):
    """A straight line through each feeder's calendar-year counts 2021 to 2025 plus 2026 annualised, at 2027."""
    w, _ = prep(wo, reg, causes)
    if pool == "in_service":
        w = w[w["section_id"].isin(set(reg.loc[reg["status"] == "IS", "section_id"]))]
    feeder = dict(zip(reg["section_id"], reg["feeder_id"]))
    w = w.assign(f=w["section_id"].map(feeder), y=w["fault_date"].map(lambda d: d.year))
    fc = {}
    for f in FEEDERS:
        ys = np.arange(2021, 2027)
        c = np.array([float(((w["f"] == f) & (w["y"] == y)).sum()) for y in ys])
        c[-1] = c[-1] * 365 / 273
        b, a = np.polyfit(ys, c, 1)
        fc[f] = float(max(a + b * 2027, 0.0))
    return fc


def last_year(wo, reg, causes=CABLE, pool="in_service"):
    w, _ = prep(wo, reg, causes)
    w = w[(w["fault_date"] >= dt.date(2025, 10, 1)) & (w["fault_date"] <= CUT)]
    if pool == "in_service":
        w = w[w["section_id"].isin(set(reg.loc[reg["status"] == "IS", "section_id"]))]
    feeder = dict(zip(reg["section_id"], reg["feeder_id"]))
    c = w["section_id"].map(feeder).value_counts()
    return {f: float(c.get(f, 0)) for f in FEEDERS}


def per_mile(fc, reg):
    st = reg[reg["status"] == "IS"]
    miles = st.groupby("feeder_id")["length_ft"].sum() / 5280.0
    return {f: fc[f] / float(miles[f]) for f in FEEDERS}


def kmodel_projected(wo, reg, causes=CABLE, quarter=0.25):
    """Calendar 2027 from 1 January: each section's October to December 2026 failure expected at its rate, which
    moves it to the next count with that probability (no replacements, as none is recorded after the cut)."""
    _, fails = prep(wo, reg, causes)
    _, r = kmodel(wo, reg, causes)
    st = stock(reg, fails)
    fc = {f: 0.0 for f in FEEDERS}
    for row in st.itertuples(index=False):
        k = min(row.k, 3)
        q = 1 - np.exp(-r.get(k) * quarter)
        fc[row.feeder_id] += (1 - q) * r.get(k) + q * r.get(min(k + 1, 3))
    return fc


def by_wo_feeder(wo, reg, causes=CABLE):
    """The k-model with each section placed on the feeder its last work order carries (or the register's when it has
    none)."""
    w, fails = prep(wo, reg, causes)
    last = {}
    for sid, f, d in zip(wo["section_id"], wo["feeder_id"], wo["fault_date"]):
        if sid not in last or d >= last[sid][0]:
            last[sid] = (d, f)
    reg2 = reg.copy()
    reg2["feeder_id"] = [last[s][1] if s in last else f for s, f in zip(reg2["section_id"], reg2["feeder_id"])]
    return kmodel(wo, reg2, causes)[0]


def by_completion(wo, reg, causes=CABLE):
    wo2 = wo.copy()
    wo2["fault_date"] = wo2["completed_date"]
    return kmodel(wo2, reg, causes)[0]
