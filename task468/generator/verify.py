"""The independent verifier: reads only the shipped pack, the golden workbook and figures.json, and recomputes the
determination and the bonus figures with its own code (no generator module but the file names and the threshold)."""
import csv
import datetime as dt
import json
import os
import sys

import openpyxl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import world as W   # noqa: E402  (file names, the 1.15 line and the 2 per cent only)

DELIVERY = {"768", "783", "784", "785", "786", "787", "788", "796", "797", "798", "805", "806", "807"}


def iso(s):
    return dt.date.fromisoformat(s)


def main(target, golden_dir):
    p = lambda k: os.path.join(target, W.FILES[k])
    npi = {r["npi"]: r["hospital_name"] for r in csv.DictReader(open(p("roster"), encoding="utf-8"))}
    mem, cmg = {}, {}
    for r in csv.DictReader(open(p("enrollment"), encoding="utf-8")):
        m, d, y = r["birth_date"].split("/")
        last = r["last_name"]
        mem[r["member_id"]] = (dt.date(int(y), int(m), int(d)),
                               "N" if r["ssn_last4"] else ("C" if (" " in last or "-" in last) else "S"))
        if r["cmg_member_no"]:
            cmg[r["cmg_member_no"]] = r["member_id"]
    # stays, as last corrected
    claims = list(csv.DictReader(open(p("claims"), encoding="utf-8")))
    gone = {r["original_claim_number"] for r in claims if r["type_of_bill"] == "0118"}
    repl = {r["original_claim_number"]: r for r in claims if r["type_of_bill"] == "0117"}
    stays, pay = [], {h: 0.0 for h in W.CANDIDATES}
    carried = {}                                   # claim: (the day its replacement paid, the change it made)
    for r in claims:
        if r["type_of_bill"] != "0111" or r["claim_number"] in gone:
            continue
        fin = repl.get(r["claim_number"], r)
        stays.append((r["member_id"], npi.get(r["billing_npi"]), r["billing_npi"], iso(r["admission_date"]),
                      iso(r["statement_thru_date"]), r["patient_status"], fin["drg"]))
        if fin is not r:
            ch = float(fin["paid_amount"]) - float(r["paid_amount"]) if fin["claim_number"].startswith("HC") else \
                float(fin["paid_amount"])
            carried[r["claim_number"]] = (iso(fin["paid_date"]), ch)
        if npi.get(r["billing_npi"]) and dt.date(2025, 7, 1) <= iso(r["statement_thru_date"]) <= dt.date(2026, 6, 30):
            a = float(r["paid_amount"])
            if fin is not r:
                a = float(fin["paid_amount"]) if fin["claim_number"].startswith("HC") else a + float(fin["paid_amount"])
            pay[npi[r["billing_npi"]]] += a
    # Provider Disputes' awards paid on fiscal 2026 stays, those a replacement bill already paid left out
    lg = openpyxl.load_workbook(p("disputes"), read_only=True)["Log"].iter_rows(values_only=True)
    hd = list(next(lg))
    for row in lg:
        d = dict(zip(hd, row))
        if d["PDR No."] is None or d["Determination"] not in ("Overturned", "Partially overturned"):
            continue
        h, paid, dis = npi.get(str(d["Provider NPI"])), d["Payment Date"], d["Discharge Date"].date()
        if h is None or paid is None or not (dt.date(2025, 7, 1) <= dis <= dt.date(2026, 6, 30)):
            continue
        c = carried.get(str(d["Claim No."]))
        if c and c[0] == paid.date() and abs(c[1] - float(d["Additional Payment"])) < 0.005:
            continue
        pay[h] += float(d["Additional Payment"])
    enc = [l.split("|") for l in open(p("encounters"), encoding="utf-8").read().splitlines() if l.startswith("D|")]
    edel = {e[3] for e in enc if e[2] == "8"}
    erep = {e[3]: e for e in enc if e[2] == "7"}
    us = lambda s: dt.date(2000 + int(s[6:8]), int(s[0:2]), int(s[3:5]))
    for e in enc:
        if e[2] != "1" or e[1] in edel:
            continue
        fin = erep.get(e[1], e)
        stays.append((cmg[e[4]], npi.get(e[5]), e[5], us(e[6]), us(e[7]), e[8], fin[9]))
    by_m = {}
    for s in stays:
        if s[1]:
            by_m.setdefault(s[0], []).append(s)
    wb = openpyxl.load_workbook(p("scores"), read_only=True)
    score = {(str(r[0]), r[1].date().isoformat() if hasattr(r[1], "date") else str(r[1])[:10], str(r[2])): r[4]
             for r in wb["Scores"].iter_rows(min_row=2, values_only=True)}
    link = {}
    for r in csv.DictReader(open(p("linkage"), encoding="utf-8")):
        a, d = r["ADMIT_DATE"], r["DATE_OF_DEATH"]
        link[(r["HCHP_MEMBER_ID"], dt.date(int(a[:4]), int(a[4:6]), int(a[6:])))] = dt.date(int(d[:4]), int(d[4:6]),
                                                                                         int(d[6:]))
    seen = {}
    with open(p("activity"), encoding="utf-8") as fh:
        rd = csv.reader(fh)
        next(rd)
        for m, d, _c, _s in rd:
            if d > seen.get(m, ""):
                seen[m] = d
    rows = []
    for m, v in by_m.items():
        v.sort(key=lambda s: (s[3], s[4]))
        for s in v:
            if not (dt.date(2025, 7, 1) <= s[3] <= dt.date(2026, 6, 30)):
                continue
            if (s[3] - mem[m][0]).days < 18 * 365.25 or s[6] in DELIVERY or s[5] == "07":
                continue
            end = s[3] + dt.timedelta(days=30)
            chain = [s]
            while chain[-1][5] == "02":
                nxt = [t for t in v if t[1] != chain[-1][1] and 0 <= (t[3] - chain[-1][4]).days <= 1]
                if not nxt:
                    break
                chain.append(nxt[0])
            dead = any(t[5] == "20" for t in chain) or any(
                t[5] == "20" and t not in chain and t[3] >= s[3] and t[4] <= end for t in v)
            last_alive = max([seen.get(m, "0000")] + [t[3].isoformat() for t in v] +
                             [t[4].isoformat() for t in v if t[5] != "20"])
            rows.append((s[1], mem[m][1], score[(m, s[3].isoformat(), s[2])], dead, (m, s[3]) in link,
                         last_alive > end.isoformat()))
            break
    rate = {}
    for c in "NSC":
        pos = [r for r in rows if r[1] == c and r[3]]
        neg = [r for r in rows if r[1] == c and r[5]]
        rate[c] = (sum(r[4] for r in pos) / len(pos), sum(r[4] for r in neg) / len(neg))
    ratio = {}
    for h in W.CANDIDATES:
        hr = [r for r in rows if r[0] == h]
        d = float(sum(r[3] for r in hr))
        for c in "NSC":
            u = [r for r in hr if r[1] == c and not r[3] and not r[5]]
            rr, ff = rate[c]
            d += max((sum(r[4] for r in u) - ff * len(u)) / (rr - ff), 0.0)
        ratio[h] = d / sum(r[2] for r in hr)
    lose = sorted(h for h in W.CANDIDATES if ratio[h] > W.THRESHOLD)
    fig = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json"), encoding="utf-8"))
    ok = lose == fig["lose_full"]
    bonus = {h: int(round(W.BONUS_RATE * pay[h] / 100.0)) * 100 for h in W.CANDIDATES}
    ok &= all(bonus[r["name"]] == r["bonus"] and abs(ratio[r["name"]] - r["ratio"]) < 0.005 for r in fig["hospitals"])
    ok &= int(round(W.BONUS_RATE * sum(pay.values()) / 100.0)) * 100 == fig["total_bonus"]
    g = openpyxl.load_workbook(os.path.join(golden_dir, W.GOLDEN["workbook"]), data_only=True)["Determination"]
    ok &= all((g.cell(row=i, column=8).value == "Loses") == (g.cell(row=i, column=1).value in lose) and
              g.cell(row=i, column=10).value == bonus[g.cell(row=i, column=1).value] for i in range(5, 19))
    print("verify: %s; %d lose the bonus (%s); %d index admissions; bonus figures and total %s" % (
        "PASS" if ok else "FAIL", len(lose), ", ".join(W.SHORT[h] for h in lose), len(rows),
        "match" if ok else "differ"))
    if not ok:
        raise SystemExit("verify failed")
    return ok


if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(base, "target"),
         sys.argv[2] if len(sys.argv) > 2 else os.path.join(base, "golden"))
