"""task163 golden computations, read from the shipped pack only (target/), on the generator's own code path.

The plan line: for each state, the 2025 share in the plan workbook times the employer business formations within four
quarters that a year of applications at the level of the twelve months to September 2026 will produce, summed over the
twelve states and rounded to the nearest 100 (the 2027 sizing standard).

The golden forecast of those formations. In the nine states without the integrated filing, formations are the state's
formation rate per application over every closed cohort, times its applications in the twelve months. In Ohio,
Pennsylvania and Michigan the applications are split into the ones the state would have had (its own level for each
calendar month before go-live, moved month by month with the nine states' applications against their level over the
same months) and the ones the integrated filing added (the rest, from the go-live month); the formations of the closed
cohorts since go-live, less the ordinary applications at the state's own pre-go-live rate, over the added applications
at that rate, give the added applications' yield relative to an ordinary application (pooled over the three states);
the twelve months' formations are the ordinary applications at the pre-go-live rate plus the added at that yield.

The asks, from the January 2026 extract: each sales territory's 2024 first-time employers (businesses whose first
payroll ever ran with Kilbourne, in the state they first employed in), how many Kilbourne still paid wages for in the
fourth quarter of 2025, their gross wages in their first quarter on payroll, and the 2024 first-time employers by
signup channel."""
from __future__ import annotations

import csv
import datetime as dt
import itertools
import json
import os

import numpy as np
import openpyxl

FIPS = {"39": "OH", "42": "PA", "26": "MI", "18": "IN", "27": "MN", "55": "WI", "21": "KY", "54": "WV", "47": "TN",
        "29": "MO", "19": "IA", "51": "VA"}
STATES = ["OH", "PA", "MI", "IN", "MN", "WI", "KY", "WV", "TN", "MO", "IA", "VA"]
NMON = 69                                   # January 2021 to September 2026


def mi(y, m):
    return (y - 2021) * 12 + (m - 1)


TTM = list(range(mi(2025, 10), mi(2026, 9) + 1))
LAST_CLOSED = mi(2025, 6)


# ------------------------------------------------------------------------------------------------- loading
def load_bfs(path):
    """{(state, series, sa): array over the 57 months, nan where the release has no value}."""
    with open(path, encoding="utf-8") as fh:
        rows = json.load(fh)
    head = rows[0]
    ix = {h: i for i, h in enumerate(head)}
    out = {}
    for r in rows[1:]:
        st = FIPS[r[ix["state"]]]
        y, m = (int(x) for x in r[ix["time"]].split("-"))
        key = (st, r[ix["data_type_code"]], r[ix["seasonally_adj"]])
        if key not in out:
            out[key] = np.full(NMON, np.nan)
        out[key][mi(y, m)] = float(r[ix["cell_value"]])
    return out


def load_share(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["Share 2025"]
    out = {}
    for row in ws.iter_rows(min_row=1, values_only=True):
        if row and isinstance(row[0], str) and len(row[0]) == 2 and row[0] in STATES:
            out[row[0]] = {"count": int(row[2]), "base": int(row[3]), "share": float(row[4])}
    return out


def load_changes(path):
    """{state: (go-live date, older route closed date)} for the integrated EIN filings in the research log."""
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["Log"]
    head = None
    live, closed = {}, {}
    for row in ws.iter_rows(values_only=True):
        if head is None:
            if row and row[0] == "Logged":
                head = {h: i for i, h in enumerate(row)}
            continue
        if not row or row[head["State"]] is None:
            continue
        kind = row[head["Change type"]]
        st = row[head["State"]]
        eff = row[head["Effective"]]
        eff = eff.date() if isinstance(eff, dt.datetime) else eff
        if kind == "Integrated EIN application":
            live[st] = eff
        elif kind == "Older filing route closed":
            closed[st] = eff
    return {s: (live[s], closed.get(s)) for s in live}


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


class Pack:
    def __init__(self, target):
        p = lambda f: os.path.join(target, f)
        self.bfs = load_bfs(p("bfs_state_api_2026-10-14.json"))
        self.share = load_share(p("plan_2027_workbook.xlsx"))
        self.changes = load_changes(p("state_filing_changes_log.xlsx"))
        self.target = target


# ------------------------------------------------------------------------------------------------- the plan line
def series(P, st, name, sa="no"):
    return P.bfs[(st, name, sa)]


def same_month_mean(x, lo, hi, t):
    idx = [u for u in range(lo, hi + 1) if u % 12 == t % 12]
    return float(np.mean(x[idx]))


def counterfactual(P, st, kind, controls, launch_idx, sa="no"):
    """The ordinary applications a state would have had, month by month, from the control states' path. Every kind
    rests on months before the state's go-live: its own level for each calendar month before go-live (CF1), in 2021
    and 2022 (CF2) or in the twelve months before go-live (CF3), moved with the controls' applications against their level on
    the same months (pooled, or the controls' ratios averaged in CF4); or the state's ratio to the controls' total
    before go-live (CF5), or that ratio for each calendar month (CF6)."""
    BA = {s: series(P, s, "BA_BA", sa) for s in STATES}
    L = launch_idx
    if kind in ("CF1", "CF2", "CF3", "CF4"):
        lo, hi = {"CF1": (0, L - 1), "CF2": (0, mi(2022, 12)), "CF3": (L - 12, L - 1), "CF4": (0, L - 1)}[kind]
        if kind == "CF4":
            idx = np.array([np.mean([BA[o][t] / same_month_mean(BA[o], lo, hi, t) for o in controls])
                            for t in range(NMON)])
        else:
            idx = np.array([sum(BA[o][t] for o in controls) / sum(same_month_mean(BA[o], lo, hi, t) for o in controls)
                            for t in range(NMON)])
        return np.array([same_month_mean(BA[st], lo, hi, t) for t in range(NMON)]) * idx
    nine = np.array([sum(BA[o][t] for o in controls) for t in range(NMON)])
    if kind == "CF5":
        return BA[st][:L].sum() / nine[:L].sum() * nine
    out = np.zeros(NMON)
    for t in range(NMON):
        idx = [u for u in range(0, L) if u % 12 == t % 12]
        out[t] = BA[st][idx].sum() / nine[idx].sum() * nine[t]
    return out


def own_counterfactual(P, st, launch_idx):
    """The before-and-after read: the state's own level before go-live for each calendar month, no comparison."""
    BA = series(P, st, "BA_BA")
    return np.array([same_month_mean(BA, 0, launch_idx - 1, t) for t in range(NMON)])


def launch_index(d):
    return mi(d.year, d.month)


def plan(P, cf="CF1", y="Y1", a="A1", nine_y="all", vol="no", controls=None, cf_override=None):
    """The plan line under one construction. Returns a dict with the total, each state's formations and the parts."""
    reform = sorted(P.changes)
    controls = controls or [s for s in STATES if s not in reform]
    L = {s: launch_index(P.changes[s][0]) for s in reform}
    BA = {s: series(P, s, "BA_BA") for s in STATES}
    F4 = {s: series(P, s, "BF_BF4Q") for s in STATES}
    G = {s: (cf_override[s] if cf_override else counterfactual(P, s, cf, controls, L[s])) for s in reform}
    Y = {}
    for s in STATES:
        if s in reform:
            lo, hi = {"Y1": (0, L[s] - 1), "Y2": (0, mi(2022, 12)), "Y3": (L[s] - 12, L[s] - 1)}[y]
        else:
            lo, hi = {"all": (0, LAST_CLOSED), "latest": (LAST_CLOSED - 11, LAST_CLOSED),
                      "pre": (0, mi(2022, 12))}[nine_y]
        Y[s] = F4[s][lo:hi + 1].sum() / BA[s][lo:hi + 1].sum()
    I = {s: np.where(np.arange(NMON) >= L[s], BA[s] - G[s], 0.0) for s in reform}
    post = {s: list(range(L[s], LAST_CLOSED + 1)) for s in reform}
    rel = {}
    if a in ("A1", "A5"):
        sh = 1 if a == "A5" else 0
        num = sum((F4[s][L[s] + sh:LAST_CLOSED + 1] - Y[s] * G[s][L[s] + sh:LAST_CLOSED + 1]).sum() for s in reform)
        den = sum((Y[s] * I[s][L[s] + sh:LAST_CLOSED + 1]).sum() for s in reform)
        rel = {s: ("rel", num / den) for s in reform}
    elif a == "A2":
        num = sum((F4[s][post[s]] - Y[s] * G[s][post[s]]).sum() for s in reform)
        den = sum(I[s][post[s]].sum() for s in reform)
        rel = {s: ("abs", num / den) for s in reform}
    elif a == "A3":
        rel = {s: ("rel", (F4[s][post[s]] - Y[s] * G[s][post[s]]).sum() / (Y[s] * I[s][post[s]]).sum()) for s in reform}
    elif a == "A4":
        x = np.concatenate([Y[s] * I[s][post[s]] for s in reform])
        yy = np.concatenate([(F4[s] - Y[s] * G[s])[post[s]] for s in reform])
        rel = {s: ("rel", float((x * yy).sum() / (x * x).sum())) for s in reform}
    elif a == "A6":
        for s in reform:
            X = np.vstack([G[s][post[s]], I[s][post[s]]]).T
            b = np.linalg.lstsq(X, F4[s][post[s]], rcond=None)[0]
            rel[s] = ("joint", b)
    elif a == "A7":
        rows, yy = [], []
        for j, s in enumerate(reform):
            for t in range(0, LAST_CLOSED + 1):
                x = [0.0] * (len(reform) + 1)
                x[j] = G[s][t] if t >= L[s] else BA[s][t]
                x[-1] = max(0.0, I[s][t]) if t >= L[s] else 0.0
                rows.append(x)
                yy.append(F4[s][t])
        b = np.linalg.lstsq(np.array(rows), np.array(yy), rcond=None)[0]
        rel = {s: ("joint", (b[j], b[-1])) for j, s in enumerate(reform)}
    out = {"F": {}, "added_ttm": {}, "ordinary_ttm": {}, "yield": Y, "rel": rel}
    total = 0.0
    for s in STATES:
        vol_s = series(P, s, "BA_BA", vol)[TTM].sum()
        if s in reform:
            scale = vol_s / BA[s][TTM].sum()
            g = G[s][TTM].sum() * scale
            i = vol_s - g
            k, v = rel[s]
            if k == "rel":
                f = Y[s] * g + v * Y[s] * i
            elif k == "abs":
                f = Y[s] * g + v * i
            else:
                f = v[0] * g + v[1] * i
            out["added_ttm"][s], out["ordinary_ttm"][s] = i, g
        else:
            f = Y[s] * vol_s
        out["F"][s] = f
        total += P.share[s]["share"] * f
    out["total"] = total
    return out


def golden(P):
    return plan(P)


CF_KINDS = ("CF1", "CF2", "CF3", "CF4", "CF5", "CF6")
Y_KINDS = ("Y1", "Y2", "Y3")
A_KINDS = ("A1", "A2", "A3", "A4", "A5", "A7")


def family(P, wide=False):
    """Every construction the design admits: counterfactual, ordinary rate window, added-yield estimator, the nine
    states' rate window, unadjusted or adjusted volume, and the control set with or without the states whose filing
    systems changed in ways that do not touch the EIN application."""
    out = {}
    nine_opts = ("all", "latest") if not wide else ("all", "latest", "pre")
    reform = sorted(P.changes)
    others = [s for s in STATES if s not in reform]
    ctl_opts = {"nine": others, "six": [s for s in others if s not in ("IN", "KY", "TN")]}
    for cf, y, a in itertools.product(CF_KINDS, Y_KINDS, A_KINDS):
        for ny in nine_opts:
            for vol in ("no", "yes"):
                for cn, ctl in ctl_opts.items():
                    if cn == "six" and not (ny == "all" and vol == "no"):
                        continue
                    out[(cf, y, a, ny, vol, cn)] = plan(P, cf, y, a, ny, vol, ctl)["total"]
    # the comparison read as a regression: formations on applications across the twelve states with state and month
    # effects, and each reform state's formations on its applications from go-live with month terms
    for name, fn in REGRESSION_FORMS.items():
        out[("regression", name, "", "", "", "")] = fn(P)
    return out


# ------------------------------------------------------------------------------------------------- the rungs
def rate(P, s, lo, hi, num="BF_BF4Q", den="BA_BA"):
    return series(P, s, num)[lo:hi + 1].sum() / series(P, s, den)[lo:hi + 1].sum()


def rung_latest_closed(P):
    """Rung 0: each state's formations per application over its latest four closed quarters (July 2024 to June 2025
    applications) carried onto the twelve months."""
    return sum(P.share[s]["share"] * rate(P, s, LAST_CLOSED - 11, LAST_CLOSED) * series(P, s, "BA_BA")[TTM].sum()
               for s in STATES)


def rung_all_closed(P):
    return sum(P.share[s]["share"] * rate(P, s, 0, LAST_CLOSED) * series(P, s, "BA_BA")[TTM].sum() for s in STATES)


def rung_latest_quarter(P):
    return sum(P.share[s]["share"] * rate(P, s, LAST_CLOSED - 2, LAST_CLOSED) * series(P, s, "BA_BA")[TTM].sum()
               for s in STATES)


def rung_pre_reform_rate(P):
    """Every application at the state's pre-go-live rate (the added treated as ordinary)."""
    tot = 0.0
    for s in STATES:
        if s in P.changes:
            L = launch_index(P.changes[s][0])
            r = rate(P, s, 0, L - 1)
        else:
            r = rate(P, s, 0, LAST_CLOSED)
        tot += P.share[s]["share"] * r * series(P, s, "BA_BA")[TTM].sum()
    return tot


def rung_zero_added(P):
    """The added applications never form: only the counterfactual applications at the pre-go-live rate."""
    g = plan(P)
    tot = 0.0
    for s in STATES:
        if s in P.changes:
            tot += P.share[s]["share"] * g["yield"][s] * g["ordinary_ttm"][s]
        else:
            tot += P.share[s]["share"] * g["F"][s]
    return tot


def rung_before_after(P):
    """The split read before and after against the state's own level before go-live, no comparison states."""
    reform = sorted(P.changes)
    G = {s: own_counterfactual(P, s, launch_index(P.changes[s][0])) for s in reform}
    return plan(P, cf_override=G)["total"]


def rung_effect_level(P):
    """The reflex comparison: the filing's effect on formations measured against the nine states as a monthly level over
    the closed cohorts since go-live, and that level carried onto the twelve months."""
    g = plan(P)
    tot = 0.0
    for s in STATES:
        if s in P.changes:
            L = launch_index(P.changes[s][0])
            G = counterfactual(P, s, "CF1", [o for o in STATES if o not in P.changes], L)
            F4 = series(P, s, "BF_BF4Q")
            post = list(range(L, LAST_CLOSED + 1))
            excess = (F4[post] - g["yield"][s] * G[post]).mean()
            tot += P.share[s]["share"] * (g["yield"][s] * g["ordinary_ttm"][s] + 12 * excess)
        else:
            tot += P.share[s]["share"] * g["F"][s]
    return tot


def rung_volume_regression(P, dummies=False):
    """Each reform state's monthly formations regressed on its applications over every closed cohort (with an
    intercept, and calendar-month terms if asked), the fit carried onto the twelve months; the nine at their rate."""
    tot = 0.0
    for s in STATES:
        BA, F4 = series(P, s, "BA_BA"), series(P, s, "BF_BF4Q")
        if s in P.changes:
            t = np.arange(0, LAST_CLOSED + 1)
            X, Xf = [np.ones(len(t)), BA[t]], [np.ones(len(TTM)), BA[TTM]]
            if dummies:
                for m in range(1, 12):
                    X.append((t % 12 == m).astype(float))
                    Xf.append((np.array(TTM) % 12 == m).astype(float))
            b = np.linalg.lstsq(np.vstack(X).T, F4[t], rcond=None)[0]
            f = float(np.vstack(Xf).T.dot(b).sum())
        else:
            f = rate(P, s, 0, LAST_CLOSED) * BA[TTM].sum()
        tot += P.share[s]["share"] * f
    return tot


def rung_volume_regression_post(P):
    """Each reform state's monthly formations regressed on its applications with calendar-month terms over the closed
    cohorts from its go-live month, the fit carried onto the twelve months; the nine at their rate."""
    tot = 0.0
    for s in STATES:
        BA, F4 = series(P, s, "BA_BA"), series(P, s, "BF_BF4Q")
        if s in P.changes:
            L = launch_index(P.changes[s][0])
            t = np.arange(L, LAST_CLOSED + 1)
            X, Xf = [np.ones(len(t)), BA[t]], [np.ones(len(TTM)), BA[TTM]]
            for m in range(1, 12):
                X.append((t % 12 == m).astype(float))
                Xf.append((np.array(TTM) % 12 == m).astype(float))
            b = np.linalg.lstsq(np.vstack(X).T, F4[t], rcond=None)[0]
            f = float(np.vstack(Xf).T.dot(b).sum())
        else:
            f = rate(P, s, 0, LAST_CLOSED) * BA[TTM].sum()
        tot += P.share[s]["share"] * f
    return tot


def rung_panel_fe(P, time_effects=False, logs=False):
    """Formations on applications across all twelve states and every closed cohort, with state effects and month
    effects (calendar-month terms, or a term for each month with the twelve months carried at the same calendar
    month's term from the latest closed year), the fit carried onto the twelve months."""
    rows, ys, keys = [], [], []
    t_all = list(range(0, LAST_CLOSED + 1))
    nT = len(t_all)
    for j, s in enumerate(STATES):
        BA, F4 = series(P, s, "BA_BA"), series(P, s, "BF_BF4Q")
        for t in t_all:
            x = np.zeros(len(STATES) + (nT if time_effects else 12) + 1)
            x[j] = 1.0
            if time_effects:
                x[len(STATES) + t] = 1.0
            else:
                x[len(STATES) + (t % 12)] = 1.0
            x[-1] = np.log(BA[t]) if logs else BA[t]
            rows.append(x)
            ys.append(np.log(F4[t]) if logs else F4[t])
    X = np.array(rows)
    # one effect is dropped for identification: the last state's
    X = np.delete(X, len(STATES) - 1, axis=1)
    b = np.linalg.lstsq(X, np.array(ys), rcond=None)[0]
    st = np.append(b[:len(STATES) - 1], 0.0)
    me = b[len(STATES) - 1:-1]
    slope = b[-1]
    tot = 0.0
    for j, s in enumerate(STATES):
        BA = series(P, s, "BA_BA")
        f = 0.0
        for u in TTM:
            if time_effects:
                same = [t for t in range(LAST_CLOSED - 11, LAST_CLOSED + 1) if t % 12 == u % 12][0]
                m_eff = me[same]
            else:
                m_eff = me[u % 12]
            v = st[j] + m_eff + slope * (np.log(BA[u]) if logs else BA[u])
            f += float(np.exp(v)) if logs else float(v)
        tot += P.share[s]["share"] * f
    return tot


REGRESSION_FORMS = {
    "two-way panel, state and month effects": lambda P: rung_panel_fe(P, time_effects=True),
    "panel, state and calendar-month effects": lambda P: rung_panel_fe(P),
    "panel, state and calendar-month effects, logs": lambda P: rung_panel_fe(P, logs=True),
    "each reform state after go-live, month terms": lambda P: rung_volume_regression_post(P),
}


def rung_flags(P, flag):
    """Formations per flagged application (high-propensity or planned wages) over the latest four closed quarters,
    carried onto the twelve months' flagged applications."""
    return sum(P.share[s]["share"] * rate(P, s, LAST_CLOSED - 11, LAST_CLOSED, den=flag) *
               series(P, s, flag)[TTM].sum() for s in STATES)


def rung_flags_all(P, flag):
    """Formations per flagged application over every closed cohort, carried onto the twelve months' flagged
    applications."""
    return sum(P.share[s]["share"] * rate(P, s, 0, LAST_CLOSED, den=flag) * series(P, s, flag)[TTM].sum()
               for s in STATES)


def carry_2025(P):
    return float(sum(P.share[s]["count"] for s in STATES))


def growth_routes(P):
    """Kilbourne's 2025 first-time employers grown with the applications, every window an analyst would pick."""
    c = carry_2025(P)
    BA = lambda sa="no": sum(series(P, s, "BA_BA", sa) for s in STATES)
    nsa, sa = BA("no"), BA("yes")
    out = {}
    out["ttm_over_cal2025"] = c * nsa[TTM].sum() / nsa[mi(2025, 1):mi(2025, 12) + 1].sum()
    out["ttm_over_base_window"] = c * nsa[TTM].sum() / nsa[mi(2024, 7):mi(2025, 6) + 1].sum()
    out["ttm_over_prior_ttm"] = c * nsa[TTM].sum() / nsa[mi(2024, 10):mi(2025, 9) + 1].sum()
    out["six_quarters_sa"] = c * sa[mi(2026, 7):mi(2026, 9) + 1].sum() / sa[mi(2024, 10):mi(2024, 12) + 1].sum()
    out["ytd_yoy"] = c * nsa[mi(2026, 1):mi(2026, 9) + 1].sum() / nsa[mi(2025, 1):mi(2025, 9) + 1].sum()
    return out


def rung_trend(P):
    """Each state's monthly formations (closed cohorts from July 2023) on a straight line, carried to the cohorts of the
    twelve months."""
    tot = 0.0
    for s in STATES:
        f = series(P, s, "BF_BF4Q")
        t = np.arange(mi(2023, 7), LAST_CLOSED + 1)
        b1, b0 = np.polyfit(t, f[t], 1)
        tot += P.share[s]["share"] * float(sum(b0 + b1 * u for u in TTM))
    return tot


def rungs(P):
    out = {"latest_closed": rung_latest_closed(P), "all_closed": rung_all_closed(P),
           "latest_quarter": rung_latest_quarter(P), "pre_reform_rate": rung_pre_reform_rate(P),
           "zero_added": rung_zero_added(P), "before_after": rung_before_after(P),
           "effect_level": rung_effect_level(P), "volume_regression": rung_volume_regression(P),
           "volume_regression_months": rung_volume_regression(P, True),
           "wba_all_closed": rung_flags_all(P, "BA_WBA"), "hba_all_closed": rung_flags_all(P, "BA_HBA"),
           "hba": rung_flags(P, "BA_HBA"), "wba": rung_flags(P, "BA_WBA"), "carry_2025": carry_2025(P),
           "trend": rung_trend(P)}
    out.update({"growth_" + k: v for k, v in growth_routes(P).items()})
    return out


# ------------------------------------------------------------------------------------------------- the bypasses
def _proj_months(f, start, log=False):
    """A straight line (or a log-linear one) through a monthly series from `start` to the last closed month, summed
    over the twelve months' cohorts."""
    t = np.arange(start, LAST_CLOSED + 1)
    y = np.log(f[t]) if log else f[t]
    b1, b0 = np.polyfit(t, y, 1)
    v = b0 + b1 * np.array(TTM, dtype=float)
    return float(np.exp(v).sum() if log else v.sum())


def _annual(x, first_month):
    """Twelve-month totals of closed cohorts for years starting in `first_month` (1-12): {(start index): total}."""
    out = {}
    for t0 in range(0, LAST_CLOSED - 10):
        if (t0 % 12) + 1 == first_month and t0 + 11 <= LAST_CLOSED:
            out[t0] = float(x[t0:t0 + 12].sum())
    return out


def bypasses(P):
    """Every route that sizes the line without splitting the applications: straight lines through the closed
    formations (monthly, adjusted or not, linear or log, and annual totals by calendar, fiscal and July years), the
    rate per application on a line, and the 2025 first-time employers carried or grown with formations or with
    applications over every window an analyst would pick."""
    out = {}
    sh = {s: P.share[s]["share"] for s in STATES}
    for nm, start in (("2021-01", mi(2021, 1)), ("2022-01", mi(2022, 1)), ("2022-07", mi(2022, 7)),
                      ("2023-01", mi(2023, 1)),
                      ("2023-07", mi(2023, 7)), ("2024-01", mi(2024, 1)), ("2024-07", mi(2024, 7))):
        out["formation line, monthly from " + nm] = sum(sh[s] * _proj_months(series(P, s, "BF_BF4Q"), start)
                                                       for s in STATES)
        out["formation line, monthly adjusted from " + nm] = sum(
            sh[s] * _proj_months(series(P, s, "BF_BF4Q", "yes"), start) for s in STATES)
        out["formation log line, monthly from " + nm] = sum(
            sh[s] * _proj_months(series(P, s, "BF_BF4Q"), start, log=True) for s in STATES)
        if start >= mi(2023, 1):
            tot = 0.0
            for s in STATES:
                f, a = series(P, s, "BF_BF4Q"), series(P, s, "BA_BA")
                t = np.arange(start, LAST_CLOSED + 1)
                b1, b0 = np.polyfit(t, f[t] / a[t], 1)
                tot += sh[s] * float(sum((b0 + b1 * u) * a[u] for u in TTM))
            out["rate per application on a line from " + nm] = tot
    mid_ttm = float(np.mean(TTM))
    for nm, fm in (("calendar", 1), ("fiscal February", 2), ("fiscal October", 10), ("July", 7)):
        tot = 0.0
        ok = True
        for s in STATES:
            ann = _annual(series(P, s, "BF_BF4Q"), fm)
            keys = sorted(ann)[-3:]
            if len(keys) < 2:
                ok = False
                break
            xs = np.array([k + 5.5 for k in keys])
            b1, b0 = np.polyfit(xs, np.array([ann[k] for k in keys]), 1)
            tot += sh[s] * float(b0 + b1 * mid_ttm)
        if ok:
            out["formation line, %s-year totals" % nm] = tot
    carry = sum(P.share[s]["count"] for s in STATES)
    out["2025 first-time employers carried"] = carry
    groups = {"nine": [s for s in STATES if s not in P.changes], "twelve": STATES}
    lc = LAST_CLOSED
    for gname, grp in groups.items():
        f = sum(series(P, s, "BF_BF4Q") for s in grp)
        out["2025 grown by the %s states' formation growth, latest year on the one before" % gname] = \
            carry * f[lc - 11:lc + 1].sum() / f[lc - 23:lc - 11].sum()
        a = sum(series(P, s, "BA_BA") for s in grp)
        for wn, (w0, w1) in (("calendar 2024", (mi(2024, 1), mi(2024, 12))), ("calendar 2025", (mi(2025, 1),
                                                                                                 mi(2025, 12))),
                             ("October 2023 to September 2024", (mi(2023, 10), mi(2024, 9))),
                             ("October 2024 to September 2025", (mi(2024, 10), mi(2025, 9))),
                             ("February 2024 to January 2025", (mi(2024, 2), mi(2025, 1))),
                             ("July 2024 to June 2025", (mi(2024, 7), mi(2025, 6))),
                             ("January to September 2025", (mi(2025, 1), mi(2025, 9)))):
            if wn == "January to September 2025":
                g = a[mi(2026, 1):mi(2026, 9) + 1].sum() / a[w0:w1 + 1].sum()
            else:
                g = a[TTM].sum() / a[w0:w1 + 1].sum()
            out["2025 grown by the %s states' applications from %s" % (gname, wn)] = carry * g
    tot = 0.0
    for s in STATES:
        a = series(P, s, "BA_BA")
        tot += P.share[s]["count"] * a[TTM].sum() / a[mi(2025, 1):mi(2025, 12) + 1].sum()
    out["each state's 2025 first-time employers grown by its own applications"] = tot
    return out


def round100(x):
    return int(100 * np.floor(x / 100.0 + 0.5))


# ------------------------------------------------------------------------------------------------- the asks
def ein_key(e):
    d = "".join(ch for ch in e if ch.isdigit())
    return d.zfill(9)


def transposed(a, b):
    """True when two nine-digit numbers differ only by one pair of adjacent digits swapped."""
    if len(a) != 9 or len(b) != 9 or a == b:
        return False
    d = [i for i in range(9) if a[i] != b[i]]
    return len(d) == 2 and d[1] == d[0] + 1 and a[d[0]] == b[d[1]] and a[d[1]] == b[d[0]]


def opened_date(r):
    v = r["opened_at"]
    if "/" in v:
        return dt.datetime.strptime(v, "%m/%d/%Y %H:%M").date()
    return dt.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ").date()


class Book:
    """The January 2026 extract, read and joined."""

    def __init__(self, target):
        p = lambda f: os.path.join(target, f)
        self.acc = read_csv(p("onboarding_accounts_2022-2025.csv"))
        self.xw = read_csv(p("client_migration_crosswalk_2024-06-15.csv"))
        self.leg = read_csv(p("legacy_quarterly_wages_2022Q1-2024Q2.csv"))
        self.cur = read_csv(p("quarterly_wages_2024Q2-2025Q4.csv"))
        self.reg = read_csv(p("state_tax_registrations_2026-01-09.csv"))
        self.suta = read_csv(p("suta_successor_transfers_2022-2025.csv"))
        self.terr = {r["state"]: r["territory"] for r in read_csv(p("sales_territories_2025.csv"))}
        self.by_acct = {r["account_id"]: r for r in self.acc}
        self.legacy_of = {r["account_id"]: r["legacy_client_no"] for r in self.xw}
        self.code_of = {r["account_id"]: r["legacy_source_code"] for r in self.xw}
        self.acct_of_legacy = {r["legacy_client_no"]: r["account_id"] for r in self.xw}
        self.regs = {}
        for r in self.reg:
            self.regs.setdefault(r["account_id"], []).append(r)
        self.by_ein = {}
        for r in self.acc:
            self.by_ein.setdefault(ein_key(r["ein"]), []).append(r)
        # wages by account and quarter: legacy (company-level group 00, cents) and current (dollars)
        self.wq = {}
        for r in self.leg:
            if r["pay_group"] != "00":
                continue
            a = self.acct_of_legacy[r["client_no"]]
            k = (a, int(r["tax_year"]), int(r["tax_qtr"]))
            self.wq[k] = self.wq.get(k, 0) + int(r["gross_wages"])
        for r in self.cur:
            y, q = r["quarter"].split("-Q")
            k = (r["account_id"], int(y), int(q))
            self.wq[k] = self.wq.get(k, 0) + int(round(float(r["gross_wages"]) * 100))
        # the first quarter we paid each account wages in
        self.first_q = {}
        for (a, y, q), c in self.wq.items():
            if c > 0 and (a not in self.first_q or (y, q) < self.first_q[a]):
                self.first_q[a] = (y, q)
        self.succ_of = {}
        for r in self.suta:
            self.succ_of.setdefault(ein_key(r["predecessor_ein"]), []).append(ein_key(r["successor_ein"]))
        self.successor_eins = {ein_key(r["successor_ein"]) for r in self.suta}
        # a client re-opened under its corrected EIN: the same legal name, trade name, industry and entity type, the
        # first account cancelled the day before the second opened, the two EINs one swap of adjacent digits apart
        named = {}
        for r in self.acc:
            named.setdefault((r["legal_name"].upper(), r["dba_name"].upper(), r["naics"], r["entity_type"]),
                             []).append(r)
        self.rekeyed = []
        for rs in named.values():
            if len(rs) < 2:
                continue
            for x in rs:
                if x["status"] != "Cancelled" or not x["cancelled_on"]:
                    continue
                for y in rs:
                    if y is not x and (opened_date(y) - dt.date.fromisoformat(x["cancelled_on"])).days == 1 and \
                            transposed(ein_key(x["ein"]), ein_key(y["ein"])):
                        self.rekeyed.append((ein_key(x["ein"]), ein_key(y["ein"])))
        parent = {e: e for e in self.by_ein}

        def find(e):
            while parent[e] != e:
                parent[e] = parent[parent[e]]
                e = parent[e]
            return e

        for a, b in self.rekeyed:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)
        self.group = {}
        for e in self.by_ein:
            self.group.setdefault(find(e), []).append(e)
        self.root = {e: find(e) for e in self.by_ein}

    def first_state(self, accts):
        """The state the business first employed in: its registration with the earliest liability date."""
        regs = [r for a in accts for r in self.regs.get(a["account_id"], [])]
        return min(regs, key=lambda r: (r["liability_date"], r["filing_start"]))["state"]

    def liable_before(self, accts, d):
        """True when a state registration of any of the accounts shows the business liable for wages before date d."""
        return any(r["liability_date"] < d for a in accts for r in self.regs.get(a["account_id"], []))

    def business_accounts(self, eins, rekey=True):
        """Every account of the business: its EINs' accounts and each successor EIN's, followed through the register
        (and across a re-keyed EIN)."""
        seen, todo, out = set(), list(eins), []
        while todo:
            e = todo.pop()
            if e in seen:
                continue
            seen.add(e)
            out.extend(self.by_ein.get(e, []))
            todo.extend(self.succ_of.get(e, []))
            if rekey and e in self.root:
                todo.extend(self.group[self.root[e]])
        return out


def quarter_of(d):
    return int(d[:4]), (int(d[5:7]) - 1) // 3 + 1


def paid_by_us(acct, y, q):
    if acct["product"] == "Tax filing only" and acct["product_since"]:
        qs = dt.date(y, 3 * q - 2, 1).isoformat()
        if acct["product_since"] <= qs:
            return False
    return True


def cohort_2024(B):
    """The businesses whose first payroll ever ran with Kilbourne in 2024: a business's accounts (an EIN's, joined
    across a re-keyed EIN) were first paid wages in 2024, it is not a successor carrying on an existing business, and no
    state registration shows it liable for wages before the quarter of that first payroll."""
    out = []
    for root, eins in sorted(B.group.items()):
        accts = [a for e in eins for a in B.by_ein[e]]
        qs = [B.first_q[a["account_id"]] for a in accts if a["account_id"] in B.first_q]
        if not qs:
            continue
        fq = min(qs)
        if fq[0] != 2024 or any(e in B.successor_eins for e in eins):
            continue
        if B.liable_before(accts, dt.date(fq[0], 3 * fq[1] - 2, 1).isoformat()):
            continue
        first = min(accts, key=lambda r: (B.first_q.get(r["account_id"], (9999, 9)), r["first_pay_date"],
                                          r["account_id"]))
        out.append((root, eins, first, fq))
    return out


CODE_CHANNEL = {"ACCT": "accountant referral", "CPA": "accountant referral", "BANK": "bank partner",
                "BP": "bank partner", "WEB": "web sign-up", "OUT": "outbound", "TEL": "outbound",
                "MKT": "partner marketplace", "APX": "partner marketplace"}


def asks(B):
    """The golden ask tables: by territory (signed, still with us in the fourth quarter of 2025, gross wages in cents in
    the first quarter on payroll and in 2024) and by signup channel."""
    T = {t: {"signed": 0, "still": 0, "wages_cents": 0, "wages_2024_cents": 0} for t in sorted(set(B.terr.values()))}
    ch = {}
    cohort = cohort_2024(B)
    for root, eins, first, fq in cohort:
        own = [a for e in eins for a in B.by_ein[e]]
        allacc = B.business_accounts(eins)
        t = B.terr[B.first_state(own)]
        T[t]["signed"] += 1
        if any(B.wq.get((a["account_id"], 2025, 4), 0) > 0 and paid_by_us(a, 2025, 4) for a in allacc):
            T[t]["still"] += 1
        T[t]["wages_cents"] += sum(B.wq.get((a["account_id"], fq[0], fq[1]), 0) for a in allacc)
        T[t]["wages_2024_cents"] += sum(B.wq.get((a["account_id"], 2024, qq), 0) for a in allacc for qq in (1, 2, 3, 4)
                                        if paid_by_us(a, 2024, qq))
        code = B.code_of.get(first["account_id"])
        channel = CODE_CHANNEL[code] if code else first["signup_channel"]
        ch[channel] = ch.get(channel, 0) + 1
    return T, ch, cohort
