"""Every rung, the golden and every ask figure of architecture 3, computed from target/ alone (no import of world.py)."""
import base64
import csv
import datetime as dt
import os
import re
import zlib
from collections import defaultdict

import numpy as np
import openpyxl

D = dt.date
CATCH = ("3841", "3842")
INTAKES = [2022, 2023, 2024, 2025, 2026]
FORE = [2027, 2028, 2029]


def find(target, prefix):
    for fn in sorted(os.listdir(target)):
        if fn.startswith(prefix):
            return os.path.join(target, fn)
    raise FileNotFoundError(prefix)


def pdf_text(path):
    raw = open(path, "rb").read()
    out, pos = [], 0
    while True:
        i = raw.find(b"stream", pos)
        if i < 0:
            break
        j = raw.find(b"endstream", i)
        head = raw[max(0, i - 160):i]
        body = raw[i + 6:j].strip(b"\r\n")
        pos = j + 9
        if b"ASCII85Decode" in head:
            body = base64.a85decode(body[:-2] if body.endswith(b"~>") else body)
        if b"FlateDecode" in head:
            try:
                body = zlib.decompress(body)
            except zlib.error:
                continue
        out += [m.decode("latin-1") for m in re.findall(rb"\(((?:[^()\\]|\\.)*)\)\s*Tj", body)]
    return " ".join(s.replace("\\(", "(").replace("\\)", ")") for s in out)


def read_csv(path, delim=";"):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=delim))


def dmy(s):
    return dt.datetime.strptime(s, "%d-%m-%Y").date() if s else None


def sheet(path, name, key):
    ws = openpyxl.load_workbook(path)[name]
    rows = list(ws.iter_rows(values_only=True))
    h = [i for i, r in enumerate(rows) if key in r][0]
    return [dict(zip(rows[h], r)) for r in rows[h + 1:] if r and r[0] is not None]


def asdate(x):
    return x.date() if isinstance(x, dt.datetime) else x


def load(target, main_only=False):
    T = {"brp": read_csv(find(target, "brp_uittreksel")), "roll": read_csv(find(target, "leerlingtellingen")),
         "plan": pdf_text(find(target, "huisvestingsplan"))}
    if main_only:
        return T
    T["gasreads"] = read_csv(find(target, "gas_telemetrie"))
    T["gas_conn"] = sheet(find(target, "meterstamgegevens_gas"), "Aansluitingen", "ean")
    T["gas_meters"] = sheet(find(target, "meterstamgegevens_gas"), "Meters", "ean")
    T["bso"] = read_csv(find(target, "bso_aanwezigheid"))
    T["bso_loc"] = sheet(find(target, "bso_locaties"), "Locaties", "locatiecode")
    T["bso_con"] = sheet(find(target, "bso_locaties"), "Contracten", "gezinsnummer")
    return T


# ------------------------------------------------------------------------------------------------- the main call
def cohort(b):
    y = b.year + 4
    return y if (b.month, b.day) <= (10, 1) else y + 1


def norm_add(s):
    return re.sub(r"[^0-9a-z]", "", (s or "").lower())


def persons(T):
    out = []
    for r in T["brp"]:
        out.append({"pid": r["persoonsnummer"], "hid": r["huishoudnummer"], "birth": dmy(r["geboortedatum"]),
                    "pc": r["postcode"].replace(" ", ""), "nr": int(r["huisnummer"]), "add": norm_add(r["huisletter"]),
                    "wijk": r["wijk"], "from": dmy(r["datum_adres"]), "to": dmy(r["datum_vertrek"])})
    return out


def lives(p, day):
    return p["from"] <= day and (p["to"] is None or day < p["to"])


def roll_index(T):
    """{count year: {(birth, postcode, number, addition): group}}"""
    idx = defaultdict(dict)
    for r in T["roll"]:
        y = int(r["teldatum"][-4:])
        key = (D.fromisoformat(r["geboortedatum"]), r["postcode"].replace(" ", ""), int(r["huisnummer"]),
               norm_add(r["toevoeging"]))
        idx[y][key] = int(r["groep"])
    return idx


def key(p):
    return (p["birth"], p["pc"], p["nr"], p["add"])


def capacity(T):
    return int(re.search(r"capacity of\s*(\d+)\s*pupils", T["plan"].replace("  ", " ")).group(1))


def main_call(target, T=None):
    T = T or load(target, main_only=True)
    ps = persons(T)
    idx = roll_index(T)
    by_hh = defaultdict(list)
    for p in ps:
        by_hh[p["hid"]].append(p)
    C = capacity(T)
    tot = {True: [0, 0], False: [0, 0]}
    by_wijk = defaultdict(lambda: [0, 0])
    yearly = {}
    out_n = {}
    for Y in INTAKES:
        day = D(Y, 10, 1)
        n = e = 0
        for p in ps:
            if cohort(p["birth"]) != Y or not lives(p, day) or p["pc"][:4] not in CATCH:
                continue
            sib = any(q is not p and q["birth"] < p["birth"] and lives(q, day) and key(q) in idx[Y] for q in by_hh[p["hid"]])
            ent = key(p) in idx[Y]
            tot[sib][0] += 1
            tot[sib][1] += ent
            by_wijk[p["wijk"]][0] += 1
            by_wijk[p["wijk"]][1] += ent
            n += 1
            e += ent
        yearly[Y] = (n, e)
        out_n[Y] = sum(1 for k_, g in idx[Y].items() if g == 1 and k_[1][:4] not in CATCH)
    rates = {k: v[1] / v[0] for k, v in tot.items()}
    pooled = (tot[True][1] + tot[False][1]) / (tot[True][0] + tot[False][0])
    mean_yearly = float(np.mean([e / n for n, e in yearly.values()]))
    wijk_rate = {k: v[1] / v[0] for k, v in by_wijk.items()}
    out_avg = sum(out_n.values()) / len(INTAKES)
    base = idx[2026]
    day26 = D(2026, 10, 1)
    future = []
    for p in ps:
        c = cohort(p["birth"])
        if not (2027 <= c <= 2029) or not lives(p, day26) or p["pc"][:4] not in CATCH:
            continue
        sib = any(q is not p and q["birth"] < p["birth"] and lives(q, day26) and key(q) in base and
                  base[key(q)] + (c - 2026) <= 8 for q in by_hh[p["hid"]])
        future.append((c, sib, p["wijk"]))
    xs = np.array(INTAKES, float)
    ys = np.array([e / n for n, e in [yearly[y] for y in INTAKES]])
    b1, b0 = np.polyfit(xs, ys, 1)

    def fc(rate_of):
        res = {}
        for Y in FORE:
            stay = sum(1 for g in base.values() if g + (Y - 2026) <= 8)
            ent = sum(rate_of(c, s, wk) for c, s, wk in future if c <= Y)
            res[Y] = stay + ent + out_avg * (Y - 2026)
        return res
    routes = {
        "golden": fc(lambda c, s, wk: rates[s]),
        "pooled": fc(lambda c, s, wk: pooled),
        "mean_yearly": fc(lambda c, s, wk: mean_yearly),
        "by_wijk": fc(lambda c, s, wk: wijk_rate[wk]),
        "trend": fc(lambda c, s, wk: b0 + b1 * c),
        "everyone": fc(lambda c, s, wk: 1.0),
    }

    def first_short(r):
        return next((Y for Y in FORE if r[Y] > C), None)
    calls = {k: first_short(v) for k, v in routes.items()}
    n_fut = {Y: (sum(1 for c, s, wk in future if c == Y and s), sum(1 for c, s, wk in future if c == Y)) for Y in FORE}
    return {"T": T, "C": C, "rates": rates, "tot": tot, "pooled": pooled, "mean_yearly": mean_yearly, "wijk_rate": wijk_rate,
            "out_avg": out_avg, "out_n": out_n, "yearly": yearly, "routes": routes, "calls": calls, "n_fut": n_fut,
            "base_n": len(base), "trend": (b0, b1), "future": future}


# ------------------------------------------------------------------------------------------------- ask 1: gas per school year
def gas_by_year(T):
    desc = {}
    for g in T["gas_conn"]:
        desc.setdefault(g["omschrijving"], []).append(str(g["ean"]))
    meters = defaultdict(list)
    for m in T["gas_meters"]:
        meters[str(m["ean"])].append(m)
    reads = defaultdict(list)
    seen = set()
    for r in T["gasreads"]:
        k = (r["ean"], r["meternummer"], r["tijdstip"], r["meterstand_m3"], r["soort"])
        if k in seen:
            continue
        seen.add(k)
        reads[(r["ean"], r["meternummer"])].append((r["tijdstip"][:16], int(r["meterstand_m3"])))
    out = {}
    for sy in (2023, 2024, 2025):
        a, b = "%d-08-01T06:00" % sy, "%d-08-01T06:00" % (sy + 1)
        da, db = D(sy, 8, 1), D(sy + 1, 8, 1)
        tot = 0
        for eans in desc.values():
            for ean in eans:
                for m in meters[ean]:
                    placed, gone = asdate(m["geplaatst"]), asdate(m["verwijderd"])
                    if gone and gone <= da or placed >= db:
                        continue
                    rs = sorted(x for x in reads.get((ean, str(m["meternummer"])), []) if a <= x[0] <= b)
                    first = int(m["beginstand_m3"]) if placed > da and m["beginstand_m3"] is not None else rs[0][1]
                    last = int(m["eindstand_m3"]) if gone and gone < db and m["eindstand_m3"] is not None else rs[-1][1]
                    tot += last - first
        out[sy] = tot
    return out


# ------------------------------------------------------------------------------------------------- ask 2: after-school care
def bso_by_weekday(T):
    dep = {r["locatiecode"] for r in T["bso_loc"] if r["adres"] == "Molenwiek 4"}
    school = {r["gezinsnummer"]: r["school"] for r in T["bso_con"]}
    out = {k: 0 for k in range(5)}
    for r in T["bso"]:
        if r["locatiecode"] in dep and school.get(r["gezinsnummer"]) == "De Kwikstaart" and r["status"] == "aanwezig":
            out[dmy(r["datum"]).weekday()] += int(r["aantal_kinderen"])
    return out


def rnd(x, unit):
    from decimal import Decimal, ROUND_HALF_UP
    return int((Decimal(repr(float(x))) / Decimal(unit)).quantize(Decimal(1), rounding=ROUND_HALF_UP)) * unit


def figures(target):
    M = main_call(target, load(target))
    T = M["T"]
    g = M["routes"]["golden"]
    gas = gas_by_year(T)
    bso = bso_by_weekday(T)
    F = {
        "call": "%d-%s" % (M["calls"]["golden"], str(M["calls"]["golden"] + 1)[-2:]) if M["calls"]["golden"] else "none",
        "capacity": M["C"],
        "rate_sibling_pct": rnd(100 * M["rates"][True], 1), "rate_other_pct": rnd(100 * M["rates"][False], 1),
        "rate_pooled_pct": rnd(100 * M["pooled"], 1),
        "intake_children": {str(k): v for k, v in {True: M["tot"][True][0], False: M["tot"][False][0]}.items()},
        "intake_entered": {str(k): v for k, v in {True: M["tot"][True][1], False: M["tot"][False][1]}.items()},
        "future_sibling": {str(Y): M["n_fut"][Y][0] for Y in FORE},
        "future_children": {str(Y): M["n_fut"][Y][1] for Y in FORE},
        "pupils": {str(Y): rnd(g[Y], 10) for Y in FORE},
        "pupils_exact": {str(Y): round(g[Y], 1) for Y in FORE},
        "excess_2029": rnd(g[2029] - M["C"], 10),
        "excess_2029_exact": round(g[2029] - M["C"], 1),
        "roll_2026": M["base_n"],
        "out_avg": round(M["out_avg"], 1),
        "pooled_pupils": {str(Y): round(M["routes"]["pooled"][Y], 1) for Y in FORE},
        "gas_m3": {str(sy): rnd(v, 1000) for sy, v in gas.items()},
        "gas_m3_exact": {str(sy): v for sy, v in gas.items()},
        "bso": {str(k): v for k, v in bso.items()},
    }
    return F, M


if __name__ == "__main__":
    import json
    import sys
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    F, M = figures(tgt)
    print(json.dumps(F, indent=1))
    print("calls", M["calls"])
    for k, v in M["routes"].items():
        print(k, {y: round(x, 1) for y, x in v.items()})
