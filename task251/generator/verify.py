"""An independent verifier: recomputes the bench list and the three asks from the cut pack with its own reading of
every file (csv module, openpyxl, no import of solve.py) and its own estimator (a cubic in NO2 converted, solved by
normal equations), and compares them with submission.md and the goldens.

    python3 task251/generator/verify.py [target]      exit 0 when everything agrees
"""
import csv
import datetime as dt
import os
import re
import sys
import zoneinfo

from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ROME = zoneinfo.ZoneInfo("Europe/Rome")
UTC = dt.timezone.utc


def rows(path, sheet=None):
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet] if sheet else wb.worksheets[0]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    return [dict(zip(head, r)) for r in it]


def d_(v):
    return v.date() if isinstance(v, dt.datetime) else v


def to_utc(day, hhmm):
    h, m = (int(x) for x in hhmm.split(":"))
    return dt.datetime.combine(day, dt.time(h, m), tzinfo=ROME).astimezone(UTC).replace(tzinfo=None)


def solve_lin(A, b):
    n = len(b)
    M = [row[:] + [bb] for row, bb in zip(A, b)]
    for i in range(n):
        piv = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[piv] = M[piv], M[i]
        for r in range(n):
            if r != i:
                f = M[r][i] / M[i][i]
                M[r] = [a - f * c for a, c in zip(M[r], M[i])]
    return [M[i][n] / M[i][i] for i in range(n)]


def cubic(xs, ys):
    X = [[1.0, x / 100, (x / 100) ** 2, (x / 100) ** 3] for x in xs]
    A = [[sum(r[i] * r[j] for r in X) for j in range(4)] for i in range(4)]
    b = [sum(r[i] * y for r, y in zip(X, ys)) for i in range(4)]
    c = solve_lin(A, b)
    return lambda x: sum(ci * (x / 100) ** k for k, ci in enumerate(c))


def files(T):
    names = os.listdir(T)
    pick = lambda pre: os.path.join(T, [f for f in names if f.startswith(pre)][0])
    return dict(arc=pick("archivio_analizzatori"), ta=pick("titolazioni_Tecnoaria"), tb=pick("titolazioni_Delta"),
                log=pick("registro_interventi"), plan=pick("piano_manutenzione"), reg=pick("anagrafica_stazioni"),
                db=pick("no2_orari_validati"))


def the_call(T):
    F = files(T)
    reg = rows(F["reg"])
    name2code = {r["nome"]: r["codice"] for r in reg}
    serial_of = {r["codice"]: r["analizzatore_nox"] for r in reg}
    # each hour once
    no2 = {}
    with open(F["arc"], encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["no2_ppb"] == "":
                continue
            no2.setdefault(r["matricola"], {})[dt.datetime.strptime(r["data_ora_utc"], "%Y-%m-%d %H:%M")] = \
                float(r["no2_ppb"])
    series = {s: sorted(v.items()) for s, v in no2.items()}

    def dose(serial, t0, t1):
        return sum(v for t, v in series[serial] if t0 <= t < t1) / 1000.0

    changes = {}
    for r in rows(F["log"]):
        w = r["intervento"]
        if "convertitore" in w and "non eseguita" not in w:
            changes.setdefault(r["matricola"], []).append(d_(r["data"]))
    for s in changes:
        changes[s].sort()
    tit = []
    for r in rows(F["ta"]):
        day = d_(r["Data"])
        tit.append((r["Matricola"], to_utc(day, r["Ora inizio"]), r["Tipo verifica"],
                    r["NO2 misurato (ppb)"] / r["NO2 generato (ppb)"]))
    with open(F["tb"], encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            day = dt.date.fromisoformat(r["data"])
            ni, nf = float(r["no_iniziale_ppb"]), float(r["no_finale_ppb"])
            xi, xf = float(r["nox_iniziale_ppb"]), float(r["nox_finale_ppb"])
            tit.append((r["matricola"], to_utc(day, r["ora_inizio"]), r["tipo_verifica"],
                        ((xf - nf) - (xi - ni)) / (ni - nf)))
    xs, ys = [], []
    for serial, start, kind, e in tit:
        if kind == "post-sostituzione":
            xs.append(0.0)
        else:
            c = [d for d in changes[serial] if dt.datetime.combine(d, dt.time(12)) <= start][-1]
            xs.append(dose(serial, dt.datetime.combine(c, dt.time(12)), start))
        ys.append(e)
    f = cubic(xs, ys)
    plan = {r["stazione"]: d_(r["manutenzione_2028"]) for r in rows(F["plan"])}
    end = max(t for s in series for t, _ in series[s][-1:]) + dt.timedelta(hours=1)
    goes = {}
    for code, serial in serial_of.items():
        inst = dt.datetime.combine(changes[serial][-1], dt.time(12))
        d_now = dose(serial, inst, end)
        until = plan[code]
        fut = []
        for y in (2025, 2026, 2027):
            a, b = dt.datetime(y, 1, 1) - dt.timedelta(hours=1), dt.datetime(y, until.month, until.day) - \
                dt.timedelta(hours=1)
            vals = [v for t, v in series[serial] if a <= t < b]
            fut.append(sum(vals) / len(vals) * ((b - a).total_seconds() / 3600) / 1000.0)
        goes[code] = f(d_now + sum(fut) / 3) < 0.95
    return goes


def the_asks(T):
    F = files(T)
    seen = set()
    recs = []
    with open(F["db"], encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            key = tuple(r.values())
            if key in seen:
                continue
            seen.add(key)
            t = dt.datetime.strptime(r["data_ora_solare"], "%d/%m/%Y %H:%M")
            recs.append([r["stazione"], t, r["no2_ugm3"], r["codice"]])
    log = rows(F["log"])
    stints = [(r["stazione"], d_(r["data"])) for r in log if "scorta" in r["intervento"]]
    stint = {}
    for code, d in sorted(stints, key=lambda x: x[1]):
        stint.setdefault(code, []).append(d)
    for r in recs:
        if r[0] == "MAG":
            for code, ds in stint.items():
                if r[1].year == 2027 and ds[-2] <= r[1].date() <= ds[-1] and ds[-1].year == 2027:
                    r[0] = code
    # hours a titration took more than 15 minutes of, on the solar clock
    occ = set()
    with open(F["tb"], encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            day = dt.date.fromisoformat(r["data"])
            s = to_utc(day, r["ora_inizio"]) + dt.timedelta(hours=1)
            e = to_utc(day, r["ora_fine"]) + dt.timedelta(hours=1)
            h = s.replace(minute=0)
            while h < e:
                if (min(e, h + dt.timedelta(hours=1)) - max(s, h)).total_seconds() > 900:
                    occ.add((r["codice_stazione"], h))
                h += dt.timedelta(hours=1)
    # the new loggers at 0 degrees C, between the M blocks of the install and the setting visits
    inst = {r["stazione"]: d_(r["data"]) for r in log if "installazione nuovo registratore" in r["intervento"]}
    fix = {r["stazione"]: d_(r["data"]) for r in log if "impostate a 20" in r["intervento"]}
    win = {}
    for code in inst:
        m0 = max(r[1] for r in recs if r[0] == code and r[3] == "M" and r[1].date() == inst[code])
        m1 = min(r[1] for r in recs if r[0] == code and r[3] == "M" and r[1].date() == fix[code])
        win[code] = (m0, m1)
    vals = {}
    for code, t, v, c in recs:
        if code == "MAG" or c not in ("V", "R") or v == "" or t.year != 2027 or (code, t) in occ:
            continue
        x = float(v.replace(",", "."))
        if code in win and win[code][0] < t < win[code][1]:
            x = x * 1.91 / 2.05
        vals.setdefault(code, []).append(x)
    out = {}
    for code, v in vals.items():
        v.sort(reverse=True)
        out[code] = (len(v), sum(v) / len(v), v[18])
    return out


def main(T=None):
    T = T or os.path.join(TASK, "target")
    fails = []
    goes = the_call(T)
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    for code, g in goes.items():
        m = re.search(r"- %s, [^\n]*\): (book on the bench|stays)" % code, sub)
        if not m or (m.group(1) == "book on the bench") != g:
            fails.append("call %s" % code)
    n = sum(goes.values())
    if "The bench list: %s, %d analyzers." % (", ".join(sorted(c for c, g in goes.items() if g)), n) not in sub:
        fails.append("the bench list line")
    asks = the_asks(T)
    for code in sorted(asks):
        v, m, p = asks[code]
        line = "- %s: %d valid hours, mean %.1f µg/m³, 19th highest %d µg/m³" % (code, v, m, int(round(p)))
        if line not in sub:
            fails.append("asks %s: %s" % (code, line))
    gx = os.path.join(TASK, "golden", "turno_banco_convertitori_2028.xlsx")
    if os.path.exists(gx):
        wb = load_workbook(gx, data_only=True)
        ws = wb["Banco gennaio 2028"]
        for i in range(5, 21):
            code = ws.cell(row=i, column=1).value
            if (ws.cell(row=i, column=11).value == "al banco") != goes[code]:
                fails.append("golden bench %s" % code)
        ws = wb["NO2 2027"]
        for i in range(5, 21):
            code = ws.cell(row=i, column=1).value
            v, m, p = asks[code]
            if (ws.cell(row=i, column=3).value != v or ws.cell(row=i, column=4).value != round(m, 1)
                    or ws.cell(row=i, column=5).value != int(round(p))):
                fails.append("golden NO2 2027 %s" % code)
    print("verify: %d failures" % len(fails))
    for f in fails:
        print("  ", f)
    return fails


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else None) else 0)
