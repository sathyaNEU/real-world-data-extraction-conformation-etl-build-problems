"""The answer computed from the cut pack alone: each meter's systematic error on the pairings the plan drew on the
morning round since the meter's last calibration, the laboratory's earlier analyzer carried onto the C900 by the
laboratory's note; the meters beyond 5 per cent; and the two indicators of section 8.

    python3 solve.py [target]"""
import datetime as dt
import os
import sys
import zoneinfo

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ROME = zoneinfo.ZoneInfo("Europe/Rome")
UTC = dt.timezone.utc
SWITCH = dt.date(2027, 9, 13)
ROUND = (6 * 60, 7 * 60 + 30)
TOL = 5.0
CRIT = (50, 400)
WEEK = {"lunedì": 0, "martedì": 1, "mercoledì": 2, "giovedì": 3, "venerdì": 4, "sabato": 5, "domenica": 6}


def load(T, FILES):
    p = lambda k: os.path.join(T, FILES[k])
    D = {}
    D["pairs"] = pd.read_excel(p("pairs"), sheet_name="Abbinamenti",
                               dtype={"glucometro_mg_dl": str, "n_accettazione": str})
    D["plan"] = pd.read_excel(p("plan"), sheet_name="Piano")
    D["holidays"] = pd.read_excel(p("plan"), sheet_name="Festività")
    D["reg"] = pd.read_excel(p("register"), sheet_name="Glucometri")
    D["hist"] = pd.read_excel(p("register"), sheet_name="Storico ubicazioni")
    D["export"] = pd.read_csv(p("export"), sep=";", dtype=str, keep_default_na=False)
    return D


def _d(v):
    return v.date() if isinstance(v, (dt.datetime, pd.Timestamp)) else v


A_OVER_B = 1.035          # the laboratory's note of 7 September 2027: divide the C600's values by 1.035


def factor(D, how="note"):
    return 1.0 / A_OVER_B


def planned(D, holiday_rule=True):
    hol = {_d(x) for x in D["holidays"]["data"]}
    out = {}
    for r in D["plan"].itertuples(index=False):
        wd = {WEEK[w.strip()] for w in r.giorni.replace(" e ", ", ").split(",")}
        d, b = _d(r.dal), _d(r.al)
        while d <= b:
            if d.weekday() in wd:
                x = d
                if holiday_rule:
                    while x in hol or x.weekday() == 6:
                        x += dt.timedelta(days=1)
                out.setdefault(r.matricola, set()).add(x)
            d += dt.timedelta(days=1)
    return out


def pairs_frame(D, fhow="note", holiday_rule=True):
    P = D["pairs"].copy()
    P["draw"] = pd.to_datetime(P["data_ora_prelievo"], format="%d/%m/%Y %H:%M")
    P["dd"] = P["draw"].dt.date
    P["mm"] = P["draw"].dt.hour * 60 + P["draw"].dt.minute
    P["num"] = pd.to_numeric(P["glucometro_mg_dl"], errors="coerce")
    P["lab"] = P["laboratorio_mg_dl"].astype(float)
    f = factor(D, fhow)
    P["lab_b"] = np.where(P["dd"] < SWITCH, P["lab"] * f, P["lab"])
    cal = {r.matricola: _d(r.ultima_taratura) for r in D["reg"].itertuples(index=False)}
    P["since"] = [d > cal[m] for m, d in zip(P["matricola"], P["dd"])]
    pl = planned(D, holiday_rule)
    P["sched"] = [(d in pl.get(m, ())) and ROUND[0] <= mm <= ROUND[1] for m, d, mm in zip(P["matricola"], P["dd"],
                                                                                         P["mm"])]
    return P


def estimate(M, L, est):
    r = M / L - 1
    if est == "mr":
        return r.mean()
    if est == "rm":
        return M.sum() / L.sum() - 1
    if est == "so":
        return (M @ L) / (L @ L) - 1
    if est == "lg":
        return np.exp(np.mean(np.log(M / L))) - 1
    if est == "med":
        return np.median(r)
    raise ValueError(est)


def call(D, est="mr", fhow="note", population="scheduled", since=True, harm=True, holiday_rule=True, P=None):
    """each meter's systematic error in per cent and the meters beyond 5 per cent"""
    P = P if P is not None else pairs_frame(D, fhow, holiday_rule)
    sel = P["num"].notna()
    if since:
        sel &= P["since"]
    if population == "scheduled":
        sel &= P["sched"]
    elif population == "noncritical":
        sel &= (P["num"] >= CRIT[0]) & (P["num"] <= CRIT[1])
    elif population == "trim15":
        r = P["num"] / P["lab_b"] - 1
        sel &= r.abs() <= 0.15
    lab = P["lab_b"] if harm else P["lab"]
    out = {}
    for m, g in P[sel].groupby("matricola"):
        out[m] = 100 * estimate(g["num"].values, lab[g.index].values, est)
    listed = sorted(m for m, e in out.items() if abs(e) > TOL)
    return out, listed


VARIANTS = {
    "golden": {},
    "every pairing since the calibration, on the C900": dict(population="all"),
    "every pairing, the laboratory as reported": dict(population="all", harm=False),
    "the scheduled pairings, the laboratory as reported": dict(harm=False),
    "the scheduled pairings since July 2026": dict(since=False),
    "every pairing with a non-critical meter value": dict(population="noncritical"),
    "every pairing within 15 per cent of the laboratory": dict(population="trim15"),
    "every pairing since the calibration, ratio of totals": dict(population="all", est="rm"),
    "every pairing since the calibration, median": dict(population="all", est="med"),
}
FAMILY = [dict(est=e) for e in ("mr", "rm", "so", "lg", "med")]


# ---- the two indicators of section 8 -------------------------------------------------------------------------------

def _hist_lookup(D):
    h = {}
    for r in D["hist"].itertuples(index=False):
        h.setdefault(r.matricola, []).append((_d(r.dal), _d(r.al) if isinstance(r.al, (dt.date, dt.datetime,
                                                                                            pd.Timestamp)) and not pd.isna(r.al) else dt.date(2099, 1, 1),
                                               r.presidio, r.reparto))
    return h


def results(D, dedupe="first", clock="solar", where="history", date="civil"):
    """the patient results, one per test, with the test's instant in UTC, its civil date, ward and hospital"""
    E = D["export"]
    E = E[E["tipo"] == "PAZIENTE"].copy()
    E["rec"] = pd.to_datetime(E["data_ora_ricezione"], format="%Y-%m-%dT%H:%M:%SZ")
    E["met"] = pd.to_datetime(E["data_ora_test"], format="%d/%m/%Y %H:%M:%S")
    if dedupe == "first":
        E = E.sort_values(["rec", "id_risultato"]).drop_duplicates(["matricola", "n_memoria"], keep="first")
    elif dedupe == "last":
        E = E.sort_values(["rec", "id_risultato"]).drop_duplicates(["matricola", "n_memoria"], keep="last")
    if clock == "solar":
        E["utc"] = E["met"] - pd.Timedelta(hours=1)
    elif clock == "utc":
        E["utc"] = E["met"]
    else:      # the meter's clock read as civil time
        loc = E["met"].dt.tz_localize(ROME, ambiguous="NaT", nonexistent="shift_forward")
        E["utc"] = loc.dt.tz_convert(UTC).dt.tz_localize(None)
        E = E[E["utc"].notna()]
    civ = E["utc"].dt.tz_localize(UTC).dt.tz_convert(ROME).dt.tz_localize(None)
    if date == "civil":
        E["day"] = civ.dt.date
    elif date == "utc":
        E["day"] = E["utc"].dt.date
    else:
        E["day"] = E["met"].dt.date
    if where == "history":
        H = _hist_lookup(D)
        hw = []
        for m, d in zip(E["matricola"], E["day"]):
            x = [r for r in H[m] if r[0] <= d <= r[1]]
            hw.append((x[0][2], x[0][3]) if x else (None, None))
        E["hosp"] = [a for a, b in hw]
        E["ward"] = [b for a, b in hw]
    else:
        E["hosp"], E["ward"] = E["presidio"], E["reparto"]
    E["late"] = (E["rec"] - E["utc"]).dt.total_seconds() > 7200
    return E


def asks(D, **kw):
    E = results(D, **kw)
    y = E[[d.year == 2027 for d in E["day"]]].copy()
    y["q"] = [(d.month - 1) // 3 + 1 for d in y["day"]]
    a1 = {}
    for (h, q), g in y.groupby(["hosp", "q"]):
        a1[(h, int(q))] = 100.0 * g["late"].mean()
    a2 = {w: int(n) for w, n in y.groupby("ward").size().items()}
    return a1, a2


def solve(T=None):
    sys.path.insert(0, HERE)
    import build as B
    T = T or os.path.join(TASK, "target")
    D = load(T, B.FILES)
    P = pairs_frame(D)
    e, listed = call(D, P=P)
    a1, a2 = asks(D)
    return dict(D=D, P=P, errors=e, listed=listed, ask1=a1, ask2=a2)


if __name__ == "__main__":
    S = solve(sys.argv[1] if len(sys.argv) > 1 else None)
    print("listed:", S["listed"])
    for m in S["listed"]:
        print("  %s %+.1f" % (m, S["errors"][m]))
    print("ask1:", {k: round(v, 1) for k, v in sorted(S["ask1"].items())})
    print("ask2:", S["ask2"])
