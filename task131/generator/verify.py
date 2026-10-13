"""task131 independent verifier: reads only the shipped bundle and recomputes every graded figure on its own code
path (no generator module is imported).

    python3 task131/generator/verify.py <target dir> [--record record.json]

Prints each recomputed figure and exits 1 if any differs from the record the generator wrote."""
import csv
import json
import os
import re
import sys
import zipfile
from collections import defaultdict
from datetime import date, timedelta
from xml.etree import ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
FROM, TO = date(2025, 11, 1), date(2026, 2, 28)
T0, T1 = date(2025, 12, 1), date(2026, 2, 28)
HOL = {date(2025, 12, 25), date(2025, 12, 26), date(2026, 1, 1), date(2026, 1, 26)}


def days():
    d, out = FROM, []
    while d <= TO:
        out.append(d)
        d += timedelta(1)
    return out


DAYS = days()


def xlsx_rows(path, sheet):
    z = zipfile.ZipFile(path)
    sst = []
    if "xl/sharedStrings.xml" in z.namelist():
        root = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in root.findall("m:si", NS):
            sst.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rid = {r.get("Id"): r.get("Target") for r in rels}
    target = None
    for s in wb.find("m:sheets", NS):
        if s.get("name") == sheet:
            target = rid[s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")]
    root = ET.fromstring(z.read("xl/" + target.lstrip("/").replace("xl/", "")))
    rows = []
    for r in root.iter("{%s}row" % NS["m"]):
        vals = {}
        for c in r.findall("m:c", NS):
            ref = c.get("r")
            col = "".join(ch for ch in ref if ch.isalpha())
            v = c.find("m:v", NS)
            if v is None:
                continue
            x = v.text
            if c.get("t") == "s":
                x = sst[int(x)]
            vals[col] = x
        rows.append(vals)
    return rows


def col(i):
    return "ABCDEFGHIJKLMNOP"[i]


def nem(tgt):
    """(nmi, register) -> {day: [48 kWh]}: latest update per meter serial and day, summed across serials"""
    best = defaultdict(dict)
    for fn in sorted(f for f in os.listdir(tgt) if f.startswith("MRP_NEM12_")):
        with open(os.path.join(tgt, fn)) as fh:
            cur = None
            for line in fh:
                p = line.strip().split(",")
                if p[0] == "200":
                    cur = (p[1], p[4], p[6], int(p[8]))
                elif p[0] == "300":
                    nmi, reg, ser, il = cur
                    n = 96 if il == 15 else 48
                    v = [float(x) for x in p[2:2 + n]]
                    if n == 96:
                        v = [v[2 * k] + v[2 * k + 1] for k in range(48)]
                    d = date(int(p[1][:4]), int(p[1][4:6]), int(p[1][6:]))
                    upd = p[2 + n + 4]
                    k = (ser, d)
                    if k not in best[(nmi, reg)] or upd > best[(nmi, reg)][k][0]:
                        best[(nmi, reg)][k] = (upd, v)
    out = {}
    for key, recs in best.items():
        dd = {}
        for (ser, d), (_, v) in recs.items():
            dd[d] = v if d not in dd else [a + b for a, b in zip(dd[d], v)]
        out[key] = dd
    return out


def main(tgt, record=None):
    reads = nem(tgt)
    reg = xlsx_rows(os.path.join(tgt, "summer_pricing_trial_register.xlsx"), "Register")
    head = [reg[0][col(i)] for i in range(len(reg[0]))]
    reg = [{head[i]: r.get(col(i)) for i in range(len(head))} for r in reg[1:]]
    fc = xlsx_rows(os.path.join(tgt, "murrandi_demand_forecast_2026.xlsx"), "Design day 2027-28")
    curve = [float(r["C"]) for r in fc[1:]]
    cust = xlsx_rows(os.path.join(tgt, "murrandi_demand_forecast_2026.xlsx"), "Customers")
    n_flat = int(float([r for r in cust[1:] if r["A"] == "2027"][0]["B"]))
    hist = list(csv.DictReader(open(os.path.join(tgt, "account_tariff_history_2026-03-12.csv"))))
    for h in hist:
        h["f"] = date.fromisoformat(h["valid_from"])
        h["t"] = date.fromisoformat(h["valid_to"]) if h["valid_to"] else None
    wx = {}
    for r in csv.DictReader(open(os.path.join(tgt, "IDCJAC0010_013027_1800_Data.csv"))):
        if r["Maximum temperature (Degree C)"]:
            wx[date(int(r["Year"]), int(r["Month"]), int(r["Day"]))] = float(r["Maximum temperature (Degree C)"])
    design_tmax = max(float(r["D"]) for r in fc[1:])
    work = [d for d in DAYS if T0 <= d <= T1 and d.weekday() < 5 and d not in HOL]
    hot = [d for d in work if abs(wx.get(d, 0.0) - design_tmax) <= 1.0]

    # each household's premise by day, by customer number
    by_c = defaultdict(list)
    for h in hist:
        if h["register"] == "E1" and not (h["t"] and h["t"] < h["f"]):
            by_c[h["customer_id"]].append(h)

    def premise(cust, d):
        for h in by_c[cust]:
            if h["f"] <= d and (h["t"] is None or h["t"] >= d):
                return h["nmi"]
        return None

    def demand(nmi, d):
        e1 = reads.get((nmi, "E1"), {}).get(d)
        if e1 is None:
            return None
        e2 = reads.get((nmi, "E2"), {}).get(d, [0.0] * 48)
        b1 = reads.get((nmi, "B1"), {}).get(d, [0.0] * 48)
        return [2.0 * (x + y - z) for x, y, z in zip(e1, e2, b1)]

    eff = {}
    for a in "ABC":
        prof = [0.0] * 48
        for d in hot:
            sa, sc, na, nc = [0.0] * 48, [0.0] * 48, 0, 0
            for r in reg:
                if r["arm"] not in ("DESIGN " + a, "CONTROL"):
                    continue
                nmi = premise(r["customer_id"], d)
                if nmi is None or nmi != r["nmi"]:
                    continue
                v = demand(nmi, d)
                if v is None:
                    continue
                if r["arm"] == "CONTROL":
                    sc = [x + y for x, y in zip(sc, v)]
                    nc += 1
                else:
                    sa = [x + y for x, y in zip(sa, v)]
                    na += 1
            prof = [p + x / na - y / nc for p, x, y in zip(prof, sa, sc)]
        eff[a] = [p / len(hot) for p in prof]
    md = max(curve)
    out = {"hot_days": [d.isoformat() for d in hot]}
    for a in "ABC":
        new = [c + n_flat * e / 1000.0 for c, e in zip(curve, eff[a])]
        out[a] = {"change": md - max(new), "ti": new.index(max(new)) + 1}
    out["call"] = max("ABC", key=lambda a: out[a]["change"])
    print("hot workdays", out["hot_days"])
    for a in "ABC":
        print("Design %s: change %.3f MW, maximum in trading interval %d" % (a, out[a]["change"], out[a]["ti"]))
    print("call: Design %s" % out["call"])

    # ask A: where each design's households stood on 28 February 2026
    on = date(2026, 2, 28)
    code = {"A": "TRA", "B": "TRB", "C": "TRC"}
    ret = {}
    for a in "ABC":
        s = b = g = 0
        for r in reg:
            if r["arm"] != "DESIGN " + a:
                continue
            rows = by_c[r["customer_id"]]
            live = [h for h in rows if h["f"] <= on and (h["t"] is None or h["t"] >= on)]
            if not live:
                g += 1
            elif live[0]["tariff_code"] == code[a]:
                s += 1
            elif live[0]["tariff_code"] == "RH1" and any(h["tariff_code"] == "RH1" and h["start_reason"] in ("CUSTOMER REQUEST", "SELF SERVICE") for h in rows):
                b += 1
        ret[a] = {"still": s, "back": b, "gone": g}
        print("Design %s: still on it %d, back on the Home Plan at own request %d, no longer customers %d" % (a, s, b, g))
    out["ret"] = ret

    # ask B: charges against the Home Plan, general supply, GST inclusive, cents
    # the gazetted charges as Schedule 1 prints them
    from pypdf import PdfReader
    sched = " ".join(pg.extract_text() for pg in PdfReader(os.path.join(tgt, "residential_charges_2025-26.pdf")).pages)
    sched = re.sub(r"\s+", " ", sched)

    def charge(pat):
        m = re.search(pat, sched)
        assert m, pat
        return [float(x) for x in m.groups()]
    flat, fsup = charge(r"Home Plan RH1 ([0-9.]+) ([0-9.]+)")
    pa = charge(r"Trial Design A TRA peak ([0-9.]+); off-peak ([0-9.]+) ([0-9.]+)")
    pb = charge(r"Trial Design B TRB peak ([0-9.]+); off-peak ([0-9.]+) ([0-9.]+)")
    pc = charge(r"Trial Design C TRC peak ([0-9.]+); shoulder ([0-9.]+); off-peak ([0-9.]+) ([0-9.]+)")
    pr = {"A": (pa[0], None, pa[1]), "B": (pb[0], None, pb[1]), "C": (pc[0], pc[1], pc[2])}
    sup = {"A": pa[2], "B": pb[2], "C": pc[3]}
    win = {"A": (30, 42), "B": (32, 40), "C": (32, 40)}
    bills = {}
    for a in "ABC":
        diffs = []
        for r in reg:
            if r["arm"] != "DESIGN " + a:
                continue
            tot = 0.0
            for h in by_c[r["customer_id"]]:
                if h["tariff_code"] != code[a]:
                    continue
                d, end = max(h["f"], T0), min(h["t"] or T1, T1)
                while d <= end:
                    v = reads[(h["nmi"], "E1")][d]
                    pk, sh, off = pr[a]
                    for k, x in enumerate(v):
                        if d.weekday() < 5 and d not in HOL and win[a][0] <= k < win[a][1]:
                            rate = pk
                        elif a == "C" and d.weekday() < 5 and d not in HOL and (28 <= k < 32 or 40 <= k < 44):
                            rate = sh
                        else:
                            rate = off
                        tot += x * (rate - flat)
                    tot += sup[a] - fsup
                    d += timedelta(1)
            diffs.append(tot / 100.0)
        bills[a] = {"more": sum(1 for x in diffs if x > 0), "mean": sum(diffs) / len(diffs)}
        print("Design %s: charged more %d, mean difference $%.2f" % (a, bills[a]["more"], bills[a]["mean"]))
    out["bills"] = bills

    # ask C: the March survey, first submitted response per household, likely or very likely to stay
    resp = [r for r in csv.DictReader(open(os.path.join(tgt, "trial_survey_responses_2026-03.csv"))) if r["complete"] == "Y"]
    resp.sort(key=lambda r: (r["submitted_at"], r["response_id"]))
    first = {}
    for r in resp:
        first.setdefault(r["trial_id"], r)
    armof = {r["trial_id"]: r["arm"] for r in reg}
    sv = {}
    for a in "ABC":
        ans = [r for t, r in first.items() if armof.get(t) == "DESIGN " + a and r["q4_stay"] != ""]
        like = [r for r in ans if (int(r["q4_stay"]) <= 2 if r["mode"] == "WEB" else int(r["q4_stay"]) >= 4)]
        sv[a] = 100.0 * len(like) / len(ans)
        print("Design %s: %d of %d likely or very likely to stay, %.1f per cent" % (a, len(like), len(ans), sv[a]))
    out["survey"] = sv

    if record:
        rec = json.load(open(record))
        bad = []
        for a in "ABC":
            if round(out[a]["change"]) != round(rec["change"][a]):
                bad.append("change %s" % a)
            if out["ret"][a] != rec["ret"][a]:
                bad.append("retention %s" % a)
            if round(out["bills"][a]["mean"], 2) != round(rec["bills"][a]["mean"], 2) or out["bills"][a]["more"] != rec["bills"][a]["more"]:
                bad.append("bills %s" % a)
            if round(out["survey"][a], 1) != round(rec["survey"][a], 1):
                bad.append("survey %s" % a)
        if out["call"] != rec["call"]:
            bad.append("call")
        print("verify: %d figures, %s" % (3 * 7 + 1, "all agree" if not bad else "DIFFER: " + ", ".join(bad)))
        print("")
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    rec = sys.argv[sys.argv.index("--record") + 1] if "--record" in sys.argv else None
    if rec in args:
        args.remove(rec)
    sys.exit(main(args[0], rec))
