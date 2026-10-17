"""task238 analysis from the pack's files alone: the contact strategy test's completes built under the test plan's
rules, each headline index's mode effect read through the letters (the Wald estimator), the monitor's band, and the
asks' figures (the response rate under each letter in each quarter, each index's valid answers online and by
telephone). The wrong routes are here too, for the checks."""
import datetime as dt
import os
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

import params as P

MT = ZoneInfo(P.TZ)
UTC = dt.timezone.utc
VALID = {"Q01": range(0, 11), "Q02": range(0, 11), "Q03": range(0, 11), "Q04": range(0, 11), "Q10": range(1, 6),
         "Q11": range(1, 4), "Q12": range(1, 6), "Q13": range(1, 6), "Q14": range(1, 4), "Q15": range(0, 8),
         "Q16": range(1, 3), "Q17": range(1, 6)}
COUNTED = {"LN": (4, 5), "TR": (1,), "SF": (1, 2), "GH": (1, 2), "SM": (1, 2), "BD": tuple(range(1, 8)), "VL": (1,),
           "FS": (4, 5)}
ITEMS = ["Q01", "Q02", "Q03", "Q04", "Q10", "Q11", "Q12", "Q13", "Q14", "Q15", "Q16", "Q17"]
CATI_DEMO = {"AGE": "age", "SEX": "sex", "QUAL": "qual", "EMP": "emp", "TENURE": "tenure", "HHSIZE": "hhsize"}


def close_utc(quarter):
    d = P.Q_END[quarter]
    return pd.Timestamp(dt.datetime(d.year, d.month, d.day, 23, 59, tzinfo=MT).astimezone(UTC))


def load(target, files):
    p = lambda k: os.path.join(target, files[k])
    iss = pd.read_csv(p("issued"), dtype=str)
    web = pd.read_csv(p("web"), dtype={"login_code": str, "submitted_utc": str})
    cati = pd.read_csv(p("cati"), dtype={"ADDRESS_ID": str, "SEX": str})
    return iss, web, cati


def completes(iss, web, cati, late_rule="local", teens=False, staff_as="cati", order="true", keep="first"):
    """the test's completes under the plan's rules; the keyword arguments switch on one mishandling at a time"""
    a = iss.set_index("login_code")
    w = web[web["last_section"] == 6].copy()
    w["address_id"] = a.loc[w["login_code"], "address_id"].values
    w["quarter"] = a.loc[w["login_code"], "quarter"].values
    w["t"] = pd.to_datetime(w["submitted_utc"], utc=True)
    if late_rule == "local":
        w = w[w["t"] <= w["quarter"].map(close_utc)]
    elif late_rule == "fixed12":
        lim = w["quarter"].map(lambda q: pd.Timestamp(dt.datetime(P.Q_END[q].year, P.Q_END[q].month, P.Q_END[q].day,
                                                                  23, 59) - dt.timedelta(hours=12), tz="UTC"))
        w = w[w["t"] <= lim]
    elif late_rule == "utcdate":
        w = w[w["t"].dt.date <= w["quarter"].map(lambda q: P.Q_END[q])]
    if not teens:
        w = w[w["age"].isna() | (w["age"] >= 18)]
    local = w["t"].dt.tz_convert(P.TZ)
    outage = (local.dt.date >= P.OUTAGE[0]) & (local.dt.date <= P.OUTAGE[1]) & (w["opened_by"] == "staff")
    w["mode"] = np.where(outage & (staff_as == "cati"), "cati", "web")
    c = cati[cati["RESULT"] == "C"].copy().rename(columns=CATI_DEMO)
    c["address_id"] = c["ADDRESS_ID"]
    c["quarter"] = a.reset_index().set_index("address_id").loc[c["address_id"], "quarter"].values
    c["sex"] = c["sex"].map({"M": 1, "F": 2, "X": 3})
    end = pd.to_datetime(c["END_TIME"])
    if order == "true":
        c["t"] = end.dt.tz_localize(P.TZ, ambiguous="NaT", nonexistent="shift_forward").dt.tz_convert("UTC")
    elif order == "fixed12":
        c["t"] = (end - pd.Timedelta(hours=12)).dt.tz_localize("UTC")
    elif order == "naive":
        c["t"] = end.dt.tz_localize("UTC")
    c["mode"] = "cati"
    cols = ["address_id", "quarter", "t", "mode"] + ITEMS + list(CATI_DEMO.values())
    s = pd.concat([w[cols], c[cols]], ignore_index=True).sort_values(["t", "mode"])
    if keep == "first":
        s = s.drop_duplicates("address_id", keep="first")
    s = s.merge(iss[["address_id", "letter", "region_code"]], on="address_id", how="left")
    return s.reset_index(drop=True)


def index_values(s, code, item, kind):
    v = s[item]
    ok = v.isin(list(VALID[item]))
    if kind == "score":
        y = v[ok].astype(float)
    else:
        y = v[ok].isin(COUNTED[code]).astype(float) * 100
    return ok, y


def wald(s, code, item, kind):
    ok, y = index_values(s, code, item, kind)
    t = s.loc[ok]
    A = (t["letter"] == "A").values
    webm = (t["mode"] == "web").values
    yv = y.values
    itt = yv[A].mean() - yv[~A].mean()
    dw = webm[A].mean() - webm[~A].mean()
    return itt / dw, itt, dw


def design(t):
    age = t["age"].astype(float)
    cols = [np.ones(len(t)), (age - 49) / 10, ((age - 49) / 10) ** 2, (t["sex"] == 2).astype(float),
            (t["qual"] == 3).astype(float), (t["qual"] == 4).astype(float), (t["emp"] == 1).astype(float),
            (t["tenure"] == 3).astype(float), t["hhsize"].astype(float)]
    cols += [(t["region_code"].astype(int) == r).astype(float) for r in range(2, 7)]
    return np.column_stack(cols)


def routes(s, code, item, kind):
    """every route's estimate of an index's mode effect"""
    ok, y = index_values(s, code, item, kind)
    t = s.loc[ok]
    keep = t[["age", "sex", "qual", "emp", "tenure", "hhsize"]].notna().all(axis=1).values
    yv = y.values
    webm = (t["mode"] == "web").values
    A = (t["letter"] == "A").values
    raw = yv[webm].mean() - yv[~webm].mean()
    X = design(t[keep])
    adj = np.linalg.lstsq(np.column_stack([X, webm[keep]]), yv[keep], rcond=None)[0][-1]
    itt = yv[A].mean() - yv[~A].mean()
    dw = webm[A].mean() - webm[~A].mean()
    Z = np.column_stack([X, A[keep]])
    what = Z @ np.linalg.lstsq(Z, webm[keep].astype(float), rcond=None)[0]
    tsls = np.linalg.lstsq(np.column_stack([X, what]), yv[keep], rcond=None)[0][-1]
    pp = yv[A & webm].mean() - yv[~A & ~webm].mean()
    return dict(raw=raw, adj=adj, itt=itt, wald=itt / dw, tsls=tsls, perprotocol=pp, dw=dw)


def band_of(effects):
    widest = {code: 100 * tol / abs(effects[code]) for code, name, item, kind, tol, th in P.INDEXES}
    bind = min(widest, key=widest.get)
    return int(np.floor(widest[bind])), bind, widest


def response(iss, s, how="gold"):
    """completes over eligible addresses: those issued less those found vacant, not a private dwelling or not found;
    an address that produced a complete was a household's home, whatever code the field team gave it"""
    out = {}
    done = set(s["address_id"])
    for q in P.QUARTERS:
        for L in ("A", "B"):
            g = iss[(iss["quarter"] == q) & (iss["letter"] == L)]
            has = g["address_id"].isin(done)
            inel = g["final_outcome"].isin(["4.1", "4.2", "4.3"])
            if how == "gold":
                n, d = int(has.sum()), int((~inel | has).sum())
            elif how == "sms_codes_only":
                n, d = int((has & ~inel).sum()), int((~inel).sum())
            elif how == "mixed":
                n, d = int(has.sum()), int((~inel).sum())
            elif how == "sms":
                n, d = int((g["final_outcome"] == "1.1").sum()), int((~inel).sum())
            out[(q, L)] = dict(completes=n, eligible=d, rate=100.0 * n / d)
    return out


def valid_by_mode(s):
    out = {}
    for code, name, item, kind, tol, th in P.INDEXES:
        ok = s[item].isin(list(VALID[item]))
        out[code] = dict(web=int((ok & (s["mode"] == "web")).sum()), cati=int((ok & (s["mode"] == "cati")).sum()))
    return out


def solve(target, files):
    iss, web, cati = load(target, files)
    s = completes(iss, web, cati)
    eff, parts = {}, {}
    for code, name, item, kind, tol, th in P.INDEXES:
        eff[code], itt, dw = wald(s, code, item, kind)
        parts[code] = dict(itt=itt, dw=dw)
    band, bind, widest = band_of(eff)
    order = sorted(widest, key=widest.get)
    return dict(s=s, iss=iss, web=web, cati=cati, effects=eff, parts=parts, band=band, bind=bind, widest=widest,
                runner=order[1], response=response(iss, s), valid=valid_by_mode(s),
                web_share={L: float((s[s["letter"] == L]["mode"] == "web").mean()) for L in ("A", "B")})
