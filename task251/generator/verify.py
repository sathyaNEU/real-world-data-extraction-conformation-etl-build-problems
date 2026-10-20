"""An independent verifier: recomputes the list and the two indicators from the cut pack with its own reading of every
file (csv module, openpyxl, no import of solve.py) and its own arithmetic (section 7's mean of the meter over
laboratory ratios, accumulated pairing by pairing), and compares them with submission.md and the goldens.

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
DAYS = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]


def sheet(path, name):
    wb = load_workbook(path, read_only=True, data_only=True)
    it = wb[name].iter_rows(values_only=True)
    head = next(it)
    return [dict(zip(head, r)) for r in it]


def d_(v):
    return v.date() if isinstance(v, dt.datetime) else v


def pick(T, pre):
    return os.path.join(T, [f for f in os.listdir(T) if f.startswith(pre)][0])


def the_list(T):
    reg = sheet(pick(T, "anagrafica_glucometri"), "Glucometri")
    cal = {r["matricola"]: d_(r["ultima_taratura"]) for r in reg}
    hol = {d_(r["data"]) for r in sheet(pick(T, "piano_abbinamenti"), "Festività")}
    plan = {}
    for r in sheet(pick(T, "piano_abbinamenti"), "Piano"):
        wd = [DAYS.index(x) for x in re.split(r",\s*|\s+e\s+", r["giorni"])]
        d = d_(r["dal"])
        while d <= d_(r["al"]):
            if d.weekday() in wd:
                x = d
                while x in hol or x.weekday() == 6:
                    x += dt.timedelta(days=1)
                plan.setdefault(r["matricola"], set()).add(x)
            d += dt.timedelta(days=1)
    sm, sl = {}, {}
    for r in sheet(pick(T, "GlyLink_abbinamenti"), "Abbinamenti"):
        t = dt.datetime.strptime(r["data_ora_prelievo"], "%d/%m/%Y %H:%M")
        m = r["matricola"]
        if t.date() not in plan.get(m, ()) or not (dt.time(6, 0) <= t.time() <= dt.time(7, 30)):
            continue
        if t.date() <= cal[m] or not str(r["glucometro_mg_dl"]).isdigit():
            continue
        lab = float(r["laboratorio_mg_dl"]) / (1.035 if t.date() < dt.date(2027, 9, 13) else 1.0)
        sm[m] = sm.get(m, 0.0) + float(r["glucometro_mg_dl"]) / lab
        sl[m] = sl.get(m, 0) + 1
    err = {m: 100.0 * (sm[m] / sl[m] - 1) for m in sm}
    return err, sorted(m for m, e in err.items() if abs(e) > 5.0), reg


def the_asks(T):
    hist = {}
    for r in sheet(pick(T, "anagrafica_glucometri"), "Storico ubicazioni"):
        hist.setdefault(r["matricola"], []).append((d_(r["dal"]), d_(r["al"]) or dt.date(2099, 1, 1), r["presidio"],
                                                   r["reparto"]))
    first = {}
    with open(pick(T, "GlyLink_risultati"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["tipo"] != "PAZIENTE":
                continue
            k = (r["matricola"], r["n_memoria"])
            rec = dt.datetime.strptime(r["data_ora_ricezione"], "%Y-%m-%dT%H:%M:%SZ")
            if k not in first or rec < first[k][0]:
                first[k] = (rec, r["data_ora_test"])
    late, n, cnt = {}, {}, {}
    for (m, _), (rec, ts) in first.items():
        utc = dt.datetime.strptime(ts, "%d/%m/%Y %H:%M:%S") - dt.timedelta(hours=1)
        civ = utc.replace(tzinfo=UTC).astimezone(ROME).date()
        if civ.year != 2027:
            continue
        h, w = [(x[2], x[3]) for x in hist[m] if x[0] <= civ <= x[1]][0]
        q = (civ.month - 1) // 3 + 1
        n[(h, q)] = n.get((h, q), 0) + 1
        late[(h, q)] = late.get((h, q), 0) + ((rec - utc).total_seconds() > 7200)
        cnt[w] = cnt.get(w, 0) + 1
    return {k: 100.0 * late[k] / n[k] for k in n}, cnt


def main(T=None):
    T = T or os.path.join(TASK, "target")
    fails = []
    err, listed, reg = the_list(T)
    ward = {r["matricola"]: r["reparto"] for r in reg}
    hosp = {r["matricola"]: r["presidio"] for r in reg}
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    for m in listed:
        line = "   - %s, %s, %s: %+.1f per cent" % (m, ward[m], hosp[m], err[m])
        if line not in sub:
            fails.append("list line " + line)
    if not re.search(r"1\. The meters to recalibrate, %d " % len(listed), sub):
        fails.append("the list's count")
    if len(re.findall(r"^   - GX2-[A-Z]\d{3}[A-Z], \w+, Presidio di \w+: [+-]\d+\.\d per cent$", sub, re.M)) != len(listed):
        fails.append("the list carries another meter")
    a1, a2 = the_asks(T)
    names = {"CM": "Presidio di Castelmarne", "RB": "Presidio di Rivobello", "VD": "Presidio di Valdarena"}
    for h, name in names.items():
        line = "   - %s: first quarter %.1f per cent, second %.1f per cent, third %.1f per cent, fourth %.1f per cent" % (
            name, a1[(h, 1)], a1[(h, 2)], a1[(h, 3)], a1[(h, 4)])
        if line not in sub:
            fails.append("ask 1 " + line)
    for w, c in a2.items():
        if "   - %s: %s\n" % (w, format(c, ",")) not in sub:
            fails.append("ask 2 %s %d" % (w, c))
    gx = os.path.join(TASK, "golden", "ritiro_glucometri_gennaio_2028.xlsx")
    if os.path.exists(gx):
        wb = load_workbook(gx, data_only=True)
        ws = wb["Ritiro gennaio 2028"]
        got = {ws.cell(row=i, column=1).value: ws.cell(row=i, column=4).value for i in range(5, ws.max_row + 1)
               if ws.cell(row=i, column=1).value}
        if sorted(got) != listed or any(abs(got[m] - round(err[m], 1)) > 1e-9 for m in listed):
            fails.append("golden list sheet")
        ws = wb["Indicatori 2027"]
        for i, h in enumerate(("CM", "RB", "VD")):
            for q in (1, 2, 3, 4):
                if abs(ws.cell(row=5 + i, column=1 + q).value - round(a1[(h, q)], 1)) > 1e-9:
                    fails.append("golden ask 1 %s %d" % (h, q))
        rows = {str(ws.cell(row=i, column=1).value).split(" ")[0]: ws.cell(row=i, column=3).value
                for i in range(11, 24)}
        if rows != a2:
            fails.append("golden ask 2")
    print("verify: %d failures" % len(fails))
    for f in fails:
        print("  ", f)
    return fails


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else None) else 0)
