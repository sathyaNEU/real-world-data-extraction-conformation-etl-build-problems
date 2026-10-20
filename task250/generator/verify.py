"""Independent recomputation of every graded figure from target.zip (or a target folder), by code that shares nothing
with solve.py, against figures.json and submission.md.   python3 verify.py [target.zip|target]"""
import datetime as dt
import email
import io
import json
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
FAILS = []
SETTINGS = (3.0, 3.5, 4.0, 4.5)
DISTRICTS = ["Cinco Villas", "Ribera Alta del Ebro", "Valdejalón", "Hoya de Huesca", "Monegros",
             "Somontano de Barbastro", "Cinca Medio", "Bajo Cinca"]


def check(cond, msg):
    print(("ok    " if cond else "FAIL  ") + msg)
    if not cond:
        FAILS.append(msg)


def unpack(src):
    if os.path.isdir(src):
        return {f: open(os.path.join(src, f), "rb").read() for f in os.listdir(src)}
    with zipfile.ZipFile(src) as z:
        return {n: z.read(n) for n in z.namelist() if not n.endswith("/")}


def pdf_text(b):
    return " ".join("\n".join(p.extract_text() for p in PdfReader(io.BytesIO(b)).pages).split())


def find(F, suffix, word):
    return [k for k in F if k.endswith(suffix) and word in k][0]


# ------------------------------------------------------------------ the documents
def documents(F):
    proc = pdf_text(F[find(F, ".pdf", "QC-02")])
    check("three stations of the network nearest to it" in proc and "within 75 km" in proc, "procedure: section 4 reads back")
    check("over the 14 days ending that day, when at least 10 of those days have a residual" in proc,
          "procedure: section 5 reads back")
    check("standard deviation (n − 1) of the drift statistic the quality control recorded" in proc,
          "procedure: section 6 reads back")
    check("The setting is 3.0, 3.5, 4.0 or 4.5" in proc and "planned on the three previous calendar years" in proc,
          "procedure: section 7 reads back")
    check("on any of the 14 days before" in proc and "either side" in proc
          and "a new year's configuration does not lift that hold" in proc, "procedure: section 8 reads back")
    check("one more than 1.0 °C out is replaced" in proc and "sensor history in the register" in proc
          and "its error goes on growing at the sensor's own rate until a check sets it right" in proc,
          "procedure: section 9 reads back")
    plan = pdf_text(F[find(F, ".pdf", "plan_campo")])
    m = re.search(r"Drift alerts\s+(\d+)\s", plan)
    check(m is not None, "plan: the drift-alert row reads back")
    m2 = re.search(r"runs (\d+) stations in 2028", plan)
    check(m2 is not None, "plan: the 2028 network reads back")
    summ = pdf_text(F[find(F, ".pdf", "resumen")])
    check("Drift alerts raised in 2027" in summ, "summary: reads back")
    msg = email.message_from_bytes(F[find(F, ".eml", "configuracion")])
    body = msg.get_payload(decode=True).decode("utf-8")
    check(("%s visits" % m.group(1)) in " ".join(body.split()) and msg["Date"].startswith("Wed, 5 Jan 2028"),
          "request: the eml parses, %s visits, 5 January 2028" % m.group(1))
    check("estadistico_14d" in F["data_dictionary.md"].decode("utf-8"), "dictionary: reads back")
    return int(m.group(1)), int(m2.group(1))


# ------------------------------------------------------------------ the register and the export
def register(F):
    wb = load_workbook(io.BytesIO(F[find(F, ".xlsx", "registro")]), read_only=True)
    rows = list(wb["Estaciones"].iter_rows(values_only=True))
    df = pd.DataFrame(rows[1:], columns=rows[0])
    hr = list(wb["Historial sensor T"].iter_rows(values_only=True))
    hist = pd.DataFrame(hr[1:], columns=hr[0])
    return df, hist


def export(F):
    q = pd.read_parquet(io.BytesIO(F[find(F, ".parquet", "control_calidad")]))
    return q


def rerun_counts(reg, q, network, cut=None, use_export=False):
    """QC-02 sections 4, 5 and 8 with `network` (station codes) as the stations an estimate may use (or the export's
    own statistic, as it ran); the limits from the export's recorded statistic; alerts over 2025 to 2027 at the
    network's stations, a year, plus, with `cut` (station, alert day, repair day), one for every drift the alerts
    never reached from a fortnight before the alert that sent its visit to its repair"""
    codes = list(reg["codigo"])
    days = pd.date_range("2025-01-01", "2027-12-31", freq="D")
    an = q.pivot(index="fecha", columns="estacion", values="anomalia").reindex(index=days, columns=codes)
    st = q.pivot(index="fecha", columns="estacion", values="estadistico_14d").reindex(index=days, columns=codes)
    sd = st.std(ddof=1)
    x = reg.set_index("codigo")["x_utm"].astype(float) / 1000
    y = reg.set_index("codigo")["y_utm"].astype(float) / 1000
    net = [c for c in codes if c in network]
    stat = {}
    for c in ([] if use_export else net):
        d = np.hypot(x[net] - x[c], y[net] - y[c])
        d = d[(d.index != c) & (d <= 75.0)].sort_values(kind="mergesort")
        num = pd.Series(0.0, index=days)
        den = pd.Series(0.0, index=days)
        got = pd.Series(0, index=days)
        for nb, dist in d.items():
            a = an[nb]
            use = a.notna() & (got < 3)
            w = 1.0 / dist ** 2
            num[use] += w * a[use]
            den[use] += w
            got[use] += 1
            if (got >= 3).all():
                break
        resid = (an[c] - num / den).where((got >= 3) & an[c].notna())
        s = resid.rolling(14, min_periods=10).mean()
        stat[c] = s.where(an[c].notna())
    if use_export:
        stat = {c: st[c] for c in net}
    out = {}
    for k in SETTINGS:
        n = 0
        hit = {}
        for c in net:
            s = stat[c].to_numpy()
            last = None
            for t in np.flatnonzero(np.abs(np.nan_to_num(s, nan=0.0)) > k * sd[c]):
                if last is None or t - last > 14:
                    n += 1
                    last = t
                    hit.setdefault(c, []).append(days[t])
        if cut is not None:
            for c, a, r in cut:
                if c in network and not any(a - pd.Timedelta(days=14) <= x <= r for x in hit.get(c, [])):
                    n += 1
        out[k] = n / 3.0
    return out


def drifts_cut_short(hist, q):
    """each adjustment or replacement the sensor history enters at a drift-alert visit, with the station's latest alert
    on or before it in the export"""
    h = hist[(hist["motivo"] == "Alerta de deriva") & hist["error_encontrado_C"].notna()]
    al = q.loc[q["alerta"] == "S", ["estacion", "fecha"]]
    out = []
    for c, d in zip(h["codigo"], pd.to_datetime(h["fecha"])):
        a = al[(al["estacion"] == c) & (al["fecha"] <= d) & (al["fecha"] >= d - pd.Timedelta(days=10))]["fecha"].max()
        out.append((c, a, d))
    return out


# ------------------------------------------------------------------ the field visits
def field(F, reg, q):
    """every 2027 field visit with its kind. The old contractor's closed orders carry the visit's day (Visita); the new
    contractor's closing date is not the visit's, and each of its visits has a check: a station of a closed order was
    visited on the first day of the order's span on which the calibration database read the station there, every
    reading that day inside the range the station's logger recorded"""
    xb = io.BytesIO(F[find(F, ".xlsx", "ordenes")])
    old = pd.read_excel(xb, sheet_name=0)
    new = pd.read_excel(xb, sheet_name=1)
    ck = pd.read_csv(io.BytesIO(F[find(F, ".csv", "comprobaciones")]))
    ck["dia"] = pd.to_datetime(ck["fecha_hora"]).dt.normalize()
    dl = pd.read_csv(io.BytesIO(F[find(F, ".csv", "estaciones_diario")]), sep=";", decimal=",")
    dl["dia"] = pd.to_datetime(dl["fecha"], format="%d/%m/%Y")
    dl = dl.drop_duplicates(["estacion", "dia"])[["estacion", "dia", "tmin", "tmax"]]
    ck["lo"] = ck[["t_estacion", "t_patron"]].min(axis=1)
    ck["hi"] = ck[["t_estacion", "t_patron"]].max(axis=1)
    g = ck.groupby(["estacion", "dia"], as_index=False).agg(lo=("lo", "min"), hi=("hi", "max"))
    g = g.merge(dl, on=["estacion", "dia"], how="left")
    days = g.loc[g["tmin"].isna() | ((g["lo"] >= g["tmin"]) & (g["hi"] <= g["tmax"])), ["estacion", "dia"]]
    al = q.loc[q["alerta"] == "S", ["estacion", "fecha"]].rename(columns={"fecha": "alerta"})

    def last_alert(df, ref_col, days_):
        m = df.merge(al, on="estacion", how="left")
        m = m[(m["alerta"] <= m[ref_col]) & (m["alerta"] >= m[ref_col] - pd.Timedelta(days=days_))]
        return m.sort_values("alerta").groupby(["orden", "estacion"], as_index=False).last()[["orden", "estacion", "alerta"]]

    oc = old[(old["Estado"] == "Cerrada") & old["Visita"].notna()].rename(columns={"Nº orden": "orden", "Estación": "estacion"})
    oc = oc.assign(dia=pd.to_datetime(oc["Visita"]), aviso=pd.to_datetime(oc["Aviso"]))
    od = oc[oc["Tipo"] == "Alerta deriva"]
    od = od.merge(last_alert(od, "aviso", 3), on=["orden", "estacion"], how="left")
    ob = oc[oc["Tipo"] == "Avería"]
    nc = new[(new["status"] == "Closed") & new["visit_date"].notna()].rename(columns={"order_ref": "orden"})
    nc = nc.assign(estacion=nc["station"].astype(str).str.split(" / ")).explode("estacion")
    nc = nc.assign(d0=pd.to_datetime(nc["opened"]), d1=pd.to_datetime(nc["visit_date"]))
    nc = nc[nc["work_type"] == "Corrective"]
    m = nc.merge(days, on="estacion")
    m = m[(m["dia"] >= m["d0"]) & (m["dia"] <= m["d1"])]
    m = m.sort_values("dia").groupby(["orden", "estacion"], as_index=False).first()
    m = m.merge(last_alert(m, "d0", 3), on=["orden", "estacion"], how="left")
    drift = pd.concat([od[["orden", "estacion", "dia", "alerta"]],
                       m.loc[m["alerta"].notna(), ["orden", "estacion", "dia", "alerta"]]])
    bd = pd.concat([ob[["estacion", "dia"]], m.loc[m["alerta"].isna(), ["estacion", "dia"]]])
    return drift[drift["dia"].dt.year == 2027], bd.loc[bd["dia"].dt.year == 2027, ["estacion"]]


def main(src):
    F = unpack(src)
    print("bundle: %d files" % len(F))
    check(len(F) >= 10 and len({f.rsplit(".", 1)[1] for f in F}) >= 3, "input gates: files and formats")
    budget, n_net = documents(F)
    reg, hist = register(F)
    q = export(F)
    check(len(q) >= 25000, "the export has %d rows" % len(q))
    keep = set(reg.loc[reg["baja_prevista"].isna(), "codigo"])
    check(len(keep) == n_net, "the register's stations with no closing date are the plan's 2028 network (%d)" % len(keep))
    cut = drifts_cut_short(hist, q)
    check(all(pd.notna(a) for c, a, r in cut), "every drift-alert adjustment in the history follows an alert (%d)" % len(cut))
    per = rerun_counts(reg, q, keep, cut)
    whole = {k: int(round(v)) for k, v in per.items()}
    ok_ = [k for k in SETTINGS if per[k] <= budget]
    setting = min(ok_) if ok_ else None
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    check(setting == fig["call"]["setting"], "the setting: %.1f (figures.json %.1f)" % (setting, fig["call"]["setting"]))
    check({"%.1f" % k: whole[k] for k in SETTINGS} == fig["call"]["per_setting_alerts_a_year"],
          "alerts a year by setting: %s" % {k: whole[k] for k in SETTINGS})
    check(fig["call"]["alerts_a_year"] == whole[setting] and fig["steps"]["drift_alert_visits_in_plan"] == budget, "the setting's count and the budget")
    for k, v in per.items():
        check(0.5 - abs(v - round(v)) >= 0.49, "bin: %.1f at %.2f a year, %.2f from its rounding edge" % (k, v, 0.5 - abs(v - round(v))))
    for nm, alt in (("the 2028 network re-run alone", rerun_counts(reg, q, keep)),
                    ("the cut-short drifts added to the record as it ran", rerun_counts(reg, q, keep, cut, use_export=True)),
                    ("the record as it ran", rerun_counts(reg, q, keep, use_export=True))):
        ok_a = [k for k in SETTINGS if alt[k] <= budget]
        check(ok_a and min(ok_a) != setting, "%s files another setting: %s" % (nm, {k: round(v, 1) for k, v in alt.items()}))
    drift, bd = field(F, reg, q)
    dist = dict(zip(reg["codigo"], reg["comarca"]))
    drift = drift.assign(d=drift["estacion"].map(dist), wait=(drift["dia"] - drift["alerta"]).dt.days)
    A_v = {d: int((drift["d"] == d).sum()) for d in DISTRICTS}
    A_w = {d: int(drift.loc[drift["d"] == d, "wait"].sum()) for d in DISTRICTS}
    bdk = bd[bd["estacion"].isin(keep)]
    B_ = {d: int((bdk["estacion"].map(dist) == d).sum()) for d in DISTRICTS}
    check(A_v == fig["asks"]["drift_alert_visits_2027"], "ask: drift-alert visits 2027 %s" % list(A_v.values()))
    check(A_w == fig["asks"]["days_alerts_waited_2027"], "ask: days alerts waited 2027 %s" % list(A_w.values()))
    check(B_ == fig["asks"]["breakdown_visits_2027_stations_kept"], "ask: breakdown visits 2027 at kept stations %s" % list(B_.values()))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    blk4 = sub.split("## 4. Deliverable Answers")[1]
    for k in SETTINGS:
        check("   - %.1f: %d" % (k, whole[k]) in blk4, "submission: %.1f's count in block 4" % k)
    for d in DISTRICTS:
        check("   - %s: %d visit%s, %d days" % (d, A_v[d], "" if A_v[d] == 1 else "s", A_w[d]) in blk4
              and "   - %s: %d" % (d, B_[d]) in blk4,
              "submission: %s's ask figures in block 4" % d)
    check("Run the %.1f setting" % setting in sub.split("## 2.")[0], "submission: block 1 commits to %.1f" % setting)
    print("\n%d failures" % len(FAILS))
    return FAILS


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    sys.exit(1 if main(src) else 0)
