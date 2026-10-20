"""The golden solution, computed from the pack alone (target/), the way an analyst holding only the files would.

    S = solve(target, F)   -> the bench list and every owed figure

The call. A molybdenum converter wears with the NO2 it reduces, so its efficiency is a function of the NO2 it has
converted since it went in, not of its age: a converter at a busy traffic station is spent in months, one at a rural
station lasts years. Every titration on file (both contractors) is a point on that curve once the archive gives the
NO2 the analyzer's converter had reduced by the titration (the analyzers' own hourly NO2, each hour once, summed
from the converter's change in the service log). The curve is pooled across the network and fitted with the
molybdenum's loss steepening past a knee. Each station analyzer's converter stands at its NO2 converted to the end of
2027; the station's own air from 1 January to its 2028 service, the mean of the same days of 2025, 2026 and 2027,
carries it forward. A converter whose efficiency would be below 95 per cent by the service goes to the bench.

The asks. The validated database's 2027 hours, each once, valid where the analyzer measured the station's air for 45
minutes or more: so not the hours a verification took more than 15 minutes of (the Delta sheets' times, Italian civil
time, put on the database's solar clock), which the database coded valid. BP07's three weeks on the store spare are
in the database under the store's code (MAG) and are BP07's; the six new loggers' hours at 0 degrees C are put back on
20 (1.91 against 2.05 to the ppb).
"""
import datetime as dt
import os
import zoneinfo

import numpy as np
import pandas as pd
from openpyxl import load_workbook

ROME = zoneinfo.ZoneInfo("Europe/Rome")
SOLAR = dt.timezone(dt.timedelta(hours=1))
UTC = dt.timezone.utc
TH = 0.95
UG20, UGL = 1.91, 2.05
Y27 = dt.datetime(2027, 1, 1)
YEARS = (2025, 2026, 2027)


# ------------------------------------------------------------------ reading the pack
def _xlsx(path, sheet=None):
    wb = load_workbook(path, data_only=True)
    ws = wb[sheet] if sheet else wb.active
    rows = list(ws.iter_rows(values_only=True))
    return pd.DataFrame(rows[1:], columns=rows[0])


def _date(v):
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    return dt.datetime.strptime(str(v)[:10], "%Y-%m-%d").date()


def legal_to_utc(d, hhmm):
    h, m = (int(x) for x in str(hhmm).split(":")[:2])
    return dt.datetime.combine(d, dt.time(h, m), tzinfo=ROME).astimezone(UTC).replace(tzinfo=None)


def load(target, F):
    p = {k: os.path.join(target, v) for k, v in F.items()}
    arc = pd.read_csv(p["archive"], dtype={"matricola": str})
    n_raw = len(arc)
    arc = arc.drop_duplicates().reset_index(drop=True)
    arc["t"] = pd.to_datetime(arc["data_ora_utc"], format="%Y-%m-%d %H:%M")
    reg = _xlsx(p["stations"])
    name2code = dict(zip(reg["nome"], reg["codice"]))
    ta = _xlsx(p["titr_a"])
    tb = pd.read_csv(p["titr_b"], dtype={"matricola": str})
    rows = []
    for r in ta.itertuples(index=False):
        d = _date(r[0])
        rows.append(dict(serial=r[4], station=name2code[r[3]], start=legal_to_utc(d, r[1]), end=legal_to_utc(d, r[2]),
                         kind=r[5], eta=float(r[7]) / float(r[6]), eta_printed=float(r[8]) / 100.0, who="A"))
    for r in tb.itertuples(index=False):
        d = _date(r.data)
        e = ((r.nox_finale_ppb - r.no_finale_ppb) - (r.nox_iniziale_ppb - r.no_iniziale_ppb)) / \
            (r.no_iniziale_ppb - r.no_finale_ppb)
        rows.append(dict(serial=r.matricola, station=r.codice_stazione, start=legal_to_utc(d, r.ora_inizio),
                         end=legal_to_utc(d, r.ora_fine), kind=r.tipo_verifica, eta=float(e),
                         eta_printed=float(r.efficienza), who="B"))
    tit = pd.DataFrame(rows).sort_values(["start", "serial"], kind="mergesort").reset_index(drop=True)
    log = _xlsx(p["service"])
    log["data"] = [_date(v) for v in log["data"]]
    plan = _xlsx(p["plan"])
    plan["manutenzione_2028"] = [_date(v) for v in plan["manutenzione_2028"]]
    db = pd.read_csv(p["database"], sep=";", decimal=",", dtype={"stazione": str, "codice": str})
    n_db_raw = len(db)
    db = db.drop_duplicates().reset_index(drop=True)
    db["t"] = pd.to_datetime(db["data_ora_solare"], format="%d/%m/%Y %H:%M")
    return dict(arc=arc, n_arc_raw=n_raw, reg=reg, tit=tit, log=log, plan=plan, db=db, n_db_raw=n_db_raw)


# ------------------------------------------------------------------ the call
def changes(D):
    """every converter change in the service log, per analyzer, in date order"""
    lg = D["log"]
    m = lg["intervento"].str.contains("convertitore", case=False) & ~lg["intervento"].str.contains("non eseguita")
    out = {}
    for r in lg[m].itertuples(index=False):
        out.setdefault(r.matricola, []).append(r.data)
    return {k: sorted(v) for k, v in out.items()}


def series(D, stato0=False):
    """each analyzer's hourly NO2 (ppb), its hours once"""
    a = D["arc"]
    if stato0:
        a = a[a["stato"] == 0]
    a = a[a["no2_ppb"].notna()]
    return {s: (g["t"].to_numpy(), g["no2_ppb"].to_numpy(dtype=float)) for s, g in a.groupby("matricola")}


def dose(ser, serial, t0, t1):
    """ppm-hours of NO2 the analyzer's converter reduced over [t0, t1), from its hourly NO2"""
    t, v = ser[serial]
    i0 = np.searchsorted(t, np.datetime64(t0))
    i1 = np.searchsorted(t, np.datetime64(t1))
    return float(v[i0:i1].sum()) / 1000.0


def change_time(d, at=12):
    return dt.datetime.combine(d, dt.time(at, 0))


def titration_points(D, ser, ch, at=12):
    """each titration's efficiency against the NO2 its converter had reduced"""
    pts = []
    for r in D["tit"].itertuples(index=False):
        if r.kind == "post-sostituzione":
            pts.append((r.serial, r.station, r.start, r.kind, 0.0, r.eta, r.eta_printed, r.who))
            continue
        inst = [c for c in ch[r.serial] if change_time(c, at) <= r.start]
        t0 = change_time(inst[-1], at)
        pts.append((r.serial, r.station, r.start, r.kind, dose(ser, r.serial, t0, r.start), r.eta, r.eta_printed,
                    r.who))
    return pd.DataFrame(pts, columns=["serial", "station", "start", "kind", "D", "eta", "eta_printed", "who"])


def fit(P, form="pw", post=True, col="eta"):
    """the pooled efficiency curve, eta against D"""
    q = P if post else P[P["kind"] != "post-sostituzione"]
    x, y = q["D"].to_numpy(), q[col].to_numpy()
    if form == "pw":
        best = None
        for kn in np.arange(30.0, 220.0, 2.5):
            X = np.c_[np.ones_like(x), x, np.maximum(0.0, x - kn) ** 2]
            c, *_ = np.linalg.lstsq(X, y, rcond=None)
            r = float(((X @ c - y) ** 2).sum())
            if best is None or r < best[0]:
                best = (r, kn, c)
        _, kn, c = best
        f = (lambda z, kn=kn, c=c: c[0] + c[1] * z + c[2] * np.maximum(0.0, z - kn) ** 2)
        f.params = {"knee": float(kn), "c": [float(v) for v in c]}
        return f
    deg = {"p2": 2, "p3": 3}[form]
    b = np.polyfit(x, y, deg)
    f = (lambda z, b=b: np.polyval(b, z))
    f.params = {"coef": [float(v) for v in b]}
    return f


def station_serial(D):
    return dict(zip(D["reg"]["codice"], D["reg"]["analizzatore_nox"]))


def climatology(D, ser, serial, until, years=YEARS, fill=True):
    """the station's own air from 1 January to its 2028 service day, ppm-hours, the mean over the years given"""
    t, v = ser[serial]
    per = []
    for y in years:
        a = dt.datetime(y, 1, 1) - dt.timedelta(hours=1)               # solar midnight, in UTC
        b = dt.datetime(y, until.month, until.day) - dt.timedelta(hours=1)
        i0, i1 = np.searchsorted(t, np.datetime64(a)), np.searchsorted(t, np.datetime64(b))
        n = int((b - a).total_seconds() // 3600)
        if fill:
            per.append(float(v[i0:i1].mean()) * n / 1000.0 if i1 > i0 else 0.0)
        else:
            per.append(float(v[i0:i1].sum()) / 1000.0)
    return float(np.mean(per))


def end_of_archive(D):
    return D["arc"]["t"].max() + dt.timedelta(hours=1)


def call(D, form="pw", post=True, stato0=False, years=YEARS, fill=True, at=12, col="eta"):
    ser = series(D, stato0)
    ch = changes(D)
    P = titration_points(D, ser, ch, at)
    f = fit(P, form, post, col)
    t_end = end_of_archive(D)
    plan = D["plan"].set_index("stazione")
    rows = []
    for code, serial in station_serial(D).items():
        until = plan.loc[code, "manutenzione_2028"]
        inst = change_time(ch[serial][-1], at)
        d_now = dose(ser, serial, inst, t_end)
        d_fut = climatology(D, ser, serial, until, years, fill)
        e_now, e_svc = float(f(d_now)), float(f(d_now + d_fut))
        rows.append(dict(station=code, serial=serial, installed=ch[serial][-1], service=until, D_now=d_now,
                         D_future=d_fut, D_service=d_now + d_fut, eta_now=e_now, eta_service=e_svc,
                         goes=e_svc < TH))
    R = pd.DataFrame(rows)
    return dict(points=P, curve=f, table=R, goes=sorted(R.loc[R["goes"], "station"]), t_end=t_end)


VARIANTS = [dict(form=fm, post=po, stato0=s0, years=yr, fill=fi, at=at, col=co)
            for fm in ("pw", "p3") for po in (True, False) for s0 in (False, True)
            for yr in (YEARS, (2026, 2027), (2027,)) for fi in (True, False) for at in (12,) for co in ("eta",)] + \
           [dict(form="p2"), dict(at=0), dict(at=23), dict(col="eta_printed"), dict(form="p3", col="eta_printed")]


# ------------------------------------------------------------------ the asks
def occupied_hours(D, year=2027, cest=True):
    """per station, the database hours (solar) of which a verification took more than 15 minutes, so that the
    analyzer measured the station's air for less than 45: the sheets' start and end, Italian civil time, on the
    database's solar clock"""
    out = {}
    for r in D["tit"].itertuples(index=False):
        s = r.start + dt.timedelta(hours=1)                 # UTC to solar
        e = r.end + dt.timedelta(hours=1)
        if not cest:                                        # the sheets' times read as if they were solar all year
            off = dt.datetime.combine(s.date(), s.time(), tzinfo=UTC).astimezone(ROME).utcoffset() - \
                dt.timedelta(hours=1)
            s, e = s + off, e + off
        if s.year != year and e.year != year:
            continue
        h = s.replace(minute=0, second=0)
        while h < e:
            mins = (min(e, h + dt.timedelta(hours=1)) - max(s, h)).total_seconds() / 60
            if mins > 15:
                out.setdefault(r.station, set()).add(h)
            h += dt.timedelta(hours=1)
    return out


def logger_windows(D):
    """per station, the hours its new logger stored at 0 degrees C: from the install visit to the visit that set it
    to 20, each visit's hours being the maintenance-coded block of its day"""
    lg, db = D["log"], D["db"]
    out = {}
    ins = lg[lg["intervento"].str.contains("installazione nuovo registratore")]
    fix = lg[lg["intervento"].str.contains("impostate a 20")]
    for r in ins.itertuples(index=False):
        d1 = fix.loc[fix["stazione"] == r.stazione, "data"].iloc[0]
        g = db[db["stazione"] == r.stazione]
        m0 = g[(g["codice"] == "M") & (g["t"].dt.date == r.data)]["t"]
        m1 = g[(g["codice"] == "M") & (g["t"].dt.date == d1)]["t"]
        out[r.stazione] = (m0.max(), m1.min())          # 0 degrees C strictly between the two blocks
    return out


def spare_stints(D):
    """the store spare's stints at stations, from the service log: (station, first day, last day)"""
    lg = D["log"]
    sw = lg[lg["intervento"].str.contains("scorta")].sort_values("data")
    out = []
    for code, g in sw.groupby("stazione"):
        g = g.sort_values("data")
        for a, b in zip(g["data"].iloc[0::2], g["data"].iloc[1::2]):
            out.append((code, a, b))
    return out


def station_hours(D, gpt=True, cest=True, spare=True, logger="scale", r_valid=True, dedupe=True):
    """every station's valid 2027 hours with their value, ug/m3 at 20 degrees C"""
    db = D["db"] if dedupe else D["db_raw"]
    db = db[db["t"].dt.year == 2027].copy()
    if spare:
        # the spare's hours, filed under the store's code, belong to the station it stood in for
        for code, a, b in spare_stints(D):
            m = (db["stazione"] == "MAG") & (db["t"].dt.date >= a) & (db["t"].dt.date <= b)
            db.loc[m, "stazione"] = code
    db = db[db["stazione"] != "MAG"]
    ok = db["codice"].isin(["V", "R"] if r_valid else ["V"]) & db["no2_ugm3"].notna()
    db = db[ok]
    vh = occupied_hours(D, cest=cest) if gpt else {}
    lw = logger_windows(D) if logger else {}
    arc_by = None
    out = {}
    for code, g in db.groupby("stazione"):
        g = g[~g["t"].isin(vh.get(code, set()))]
        v = g["no2_ugm3"].to_numpy(dtype=float)
        t = g["t"]
        if code in lw:
            a, b = lw[code]
            m = ((t > a) & (t < b)).to_numpy()
            if logger == "scale":
                v = np.where(m, v * UG20 / UGL, v)
            elif logger == "archive":
                if arc_by is None:
                    arc_by = {s: gg.set_index("t")["no2_ppb"] for s, gg in D["arc"].groupby("matricola")}
                serial = station_serial(D)[code]
                ppb = arc_by[serial].reindex(t[m] - dt.timedelta(hours=1)).to_numpy(dtype=float)
                v = v.copy()
                v[m] = ppb * UG20
        out[code] = pd.DataFrame({"t": t.to_numpy(), "v": v})
    return out


def stats(H):
    out = {}
    for code, h in H.items():
        v = np.sort(h["v"].to_numpy())[::-1]
        out[code] = dict(valid=int(len(v)), mean=float(v.mean()), p19=float(v[18]))
    return out


def asks(D, **kw):
    return stats(station_hours(D, **kw))


def solve(target, F):
    D = load(target, F)
    D["db_raw"] = pd.read_csv(os.path.join(target, F["database"]), sep=";", decimal=",",
                              dtype={"stazione": str, "codice": str})
    D["db_raw"]["t"] = pd.to_datetime(D["db_raw"]["data_ora_solare"], format="%d/%m/%Y %H:%M")
    C = call(D)
    A = asks(D)
    return {"D": D, "call": C, "asks": A}
