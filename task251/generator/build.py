"""Write the pack: every file under target/, from the seeded world.   B.run(target) -> the world and the records"""
import datetime as dt
import os

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

import docs
import params as P
import postprocess
import records as RC
import sim

SEED = P.SEED
FILES = dict(
    manual="AQBP-QA-07_manuale_qualita_NOx_rev4.pdf",
    archive="archivio_analizzatori_NOx_2024-2027.csv",
    titr_a="titolazioni_Tecnoaria_2025-2026.xlsx",
    titr_b="titolazioni_Delta_2026-2027.csv",
    service="registro_interventi_2024-2027.xlsx",
    plan="piano_manutenzione_2028.xlsx",
    stations="anagrafica_stazioni.xlsx",
    database="no2_orari_validati_2027.csv",
    mail="laboratorio_banco_gennaio_2028.eml",
    dictionary="dizionario_dati.md",
    met="meteo_stazioni_2027.csv",
    pm10="pm10_gravimetrico_2027.xlsx",
)
PACK = list(FILES)
DISTRACTORS = ["met", "pm10"]
CONTEXT = ["mail"]
STAMP_PDF = {"manual": "2026-06-24T15:20:00"}


def _sheet(path, title, df, widths, date_cols=(), formats=None):
    wb = Workbook()
    ws = wb.active
    ws.title = title
    ws.append(list(df.columns))
    for r in df.itertuples(index=False):
        ws.append([None if (isinstance(v, float) and v != v) else v for v in r])
    for row in ws.iter_rows(min_row=2):
        for j in date_cols:
            row[j].number_format = "dd/mm/yyyy"
        for j, fmt in (formats or {}).items():
            row[j].number_format = fmt
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    for c in ws[1]:
        c.font = Font(bold=True)
    ws.freeze_panes = "A2"
    wb.save(path)


def _met(seed):
    rng = np.random.default_rng(seed + 91)
    rows = []
    t0 = dt.datetime(2027, 1, 1)
    for code in ("BP01", "BP09", "BP15"):
        for j in range(8760):
            t = t0 + dt.timedelta(hours=j)
            doy, hr = t.timetuple().tm_yday, t.hour
            tm = 13.5 - 11.0 * np.cos(2 * np.pi * (doy - 15) / 365.25)
            ta = tm + 4.0 * np.sin(2 * np.pi * (hr - 9) / 24) + rng.normal(0, 1.2)
            rh = min(100, max(18, 72 + 14 * np.cos(2 * np.pi * (doy - 15) / 365.25) - 2.5 * (ta - tm) +
                                rng.normal(0, 6)))
            ws = max(0.1, 1.6 + 0.9 * np.sin(np.pi * max(0, hr - 7) / 13) + rng.normal(0, 0.6))
            wd = int((260 + rng.normal(0, 70)) % 360)
            mh = max(40, (180 + 900 * max(0, np.sin(np.pi * (hr - 7) / 12)) * (0.55 + 0.45 * np.sin(
                2 * np.pi * (doy - 100) / 365.25))) * rng.lognormal(0, 0.25))
            rows.append((code, t.strftime("%Y-%m-%d %H:%M"), round(ta, 1), int(round(rh)), round(ws, 1), wd,
                         int(round(mh, -1))))
    return pd.DataFrame(rows, columns=["stazione", "data_ora_solare", "temperatura_c", "umidita_pct", "vento_ms",
                                       "direzione_gradi", "altezza_rimescolamento_m"])


def _pm10(path, seed):
    rng = np.random.default_rng(seed + 92)
    st = ["BP01", "BP03", "BP05", "BP09", "BP12", "BP15"]
    lvl = [38, 34, 31, 29, 26, 23]
    rows = []
    d = dt.date(2027, 1, 1)
    while d.year == 2027:
        doy = d.timetuple().tm_yday
        f = 1 + 0.6 * np.cos(2 * np.pi * (doy - 15) / 365.25)
        reg = rng.lognormal(0, 0.35)
        row = [d]
        for L in lvl:
            if rng.random() < 0.04:
                row.append(None)
            else:
                row.append(round(L * f * reg * rng.lognormal(0, 0.15), 1))
        rows.append(row)
        d += dt.timedelta(days=1)
    df = pd.DataFrame(rows, columns=["data"] + st)
    _sheet(path, "PM10 2027", df, [12] + [9] * 6, date_cols=(0,), formats={j: "0.0" for j in range(1, 7)})


def world():
    W = sim.world(SEED)
    R = RC.build(W, SEED)
    return W, R


def run(target):
    os.makedirs(target, exist_ok=True)
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    W, R = world()
    a = R["archive"].copy()
    a.to_csv(F["archive"], index=False, encoding="utf-8", float_format="%.2f",
             header=["matricola", "data_ora_utc", "no_ppb", "no2_ppb", "nox_ppb", "stato"])
    _sheet(F["titr_a"], "Titolazioni", R["titrations_A"], [11, 10, 9, 32, 13, 17, 18, 18, 26, 15, 13],
           date_cols=(0,), formats={6: "0.0", 7: "0.0", 8: "0.0"})
    R["titrations_B"].to_csv(F["titr_b"], index=False, encoding="utf-8")
    _sheet(F["service"], "Interventi", R["service_log"], [11, 9, 13, 96, 13], date_cols=(0,))
    _sheet(F["plan"], "Piano", R["plan"], [9, 32, 13, 9, 18, 60], date_cols=(4,))
    _sheet(F["stations"], "Stazioni", R["register"], [8, 32, 16, 9, 9, 17, 9, 12, 15], date_cols=(8,),
           formats={3: "0.0000", 4: "0.0000"})
    db = R["database"].copy()
    db["no2_ugm3"] = ["" if (v is None or v != v) else ("%.1f" % v).replace(".", ",") for v in db["no2_ugm3"]]
    db.to_csv(F["database"], sep=";", index=False, encoding="utf-8")
    docs.manual(F["manual"], FILES)
    docs.lab_mail(F["mail"], FILES)
    docs.dictionary(F["dictionary"], FILES)
    m = _met(SEED)
    m.to_csv(F["met"], index=False, encoding="utf-8")
    _pm10(F["pm10"], SEED)
    postprocess.scrub(F["manual"], "Microsoft Word 2019", STAMP_PDF["manual"])
    for k in ("titr_a", "service", "plan", "stations", "pm10"):
        postprocess.scrub(F[k], P.ORG, "2028-01-03")
        postprocess.finish_office(F[k], "2028-01-03T10:05:00Z", "2028-01-03T10:11:00Z", P.ORG)
    return {"W": W, "R": R}
