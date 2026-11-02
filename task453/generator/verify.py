"""An independent verifier for task453: its own readers for every format (pdftotext for the survey reports and the
certificate, the csv module for the permits, ledgers and cycles, openpyxl for the workbooks, pyarrow for the plant
log) and its own implementation of every graded figure, compared with figures.json and the golden workbook. The
bypass intervals are found from the inlet temperature, not from the alarm rules the golden reads, and the account
credits are settled by a meet-in-the-middle subset search, not the golden's recursion. Positive controls show each
comparison can fail."""
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W   # noqa: E402

OUT = []


def check(label, cond, detail=""):
    OUT.append((label, bool(cond), detail))


def text(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout


# ---------------------------------------------------------------- the survey, read off the PDFs
def survey_cells(target):
    """(wave, sex, lowest age) -> mean teeth restored with amalgam per adult, as each report prints it."""
    cells = {}
    band = r"(18 to 24|\d\d to \d\d|\d\d and over)"
    t96 = text(os.path.join(target, W.FILES["s1996"]))
    part = t96[t96.index("Table 7."):]
    for m in re.finditer(r"(Men|Women|All adults) %s\s+([\d,]+)\s+(\d+\.\d)\s+(\d+\.\d\d)" % band, part):
        sx = {"Men": "M", "Women": "F", "All adults": "A"}[m.group(1)]
        cells[(1996, sx, int(m.group(2)[:2]))] = float(m.group(4))
    t06 = text(os.path.join(target, W.FILES["s2006"]))
    part = t06[t06.index("Table 3.4"):]
    for m in re.finditer(r"^\s*%s\s+([\d,]+)\s+(\d+\.\d)\s+[\d.]+ to [\d.]+\s+([\d,]+)\s+(\d+\.\d)\s+[\d.]+ to [\d.]+"
                         % band, part, re.M):
        lo = int(m.group(1)[:2])
        cells[(2006, "M", lo)] = float(m.group(3))
        cells[(2006, "F", lo)] = float(m.group(5))
    t16 = text(os.path.join(target, W.FILES["s2016"]))
    for k, sx in ((2, "M"), (3, "F"), (4, "A")):
        start = t16.index("Table 3.%d " % k)
        stop = t16.index("Table 3.%d " % (k + 1)) if k < 4 else len(t16)
        for m in re.finditer(r"^\s*%s\s+([\d,]+)\s+(\d+\.\d)\s+[\d.]+ to [\d.]+" % band, t16[start:stop], re.M):
            cells[(2016, sx, int(m.group(1)[:2]))] = float(m.group(3))
    return cells


def lookup(cells, y, s, a):
    a = max(a, 18)
    los = sorted(lo for (yy, ss, lo) in cells if yy == y and ss == s)
    lo = max(x for x in los if x <= a)
    return cells[(y, s, lo)]


# ---------------------------------------------------------------- the call
def register(target):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, W.FILES["register"]), read_only=True, data_only=True)
    comm, fac = {}, []
    for r in wb["Members"].iter_rows(min_row=5, values_only=True):
        if r[0]:
            comm[r[0]] = r[7].date() if r[7] else None
    for r in wb["Agency facility numbers"].iter_rows(min_row=2, values_only=True):
        if r[0]:
            fac.append((r[1], r[0], r[2].date(), r[3].date() if r[3] else dt.date(2100, 1, 1)))
    return comm, fac


def the_call(target, cells):
    comm, fac = register(target)
    hg, ab, n = {}, {}, 0
    with open(os.path.join(target, W.FILES["permits"]), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = dt.date.fromisoformat(r["date_of_cremation"])
            if d.year != 2026:
                continue
            n += 1
            code = [c for f, c, a, b in fac if f == r["crematorium_facility_no"] and a <= d <= b][0]
            age = int(r["age"]) if r["age_unit"] == "Y" else 0
            if age < 18:
                teeth = 0.0
            else:
                c16 = lookup(cells, 2016, r["sex"], age - 10)
                c06 = lookup(cells, 2006, r["sex"], age - 20)
                teeth = max(0.0, c16 + (c16 - c06))
            g = 0.55 * teeth
            hg[code] = hg.get(code, 0.0) + g
            if comm[code] is not None and d > comm[code]:
                ab[code] = ab.get(code, 0.0) + g
    tot = sum(hg.values())
    share = 100 * sum(ab.values()) / tot
    cand = sorted((c for c in hg if comm[c] is None), key=lambda c: -hg[c])
    des, cur = [], sum(ab.values())
    for c in cand:
        if 100 * cur / tot >= 55:
            break
        des.append(c)
        cur += hg[c]
    return share, des, n


# ---------------------------------------------------------------- the levies
INC = {"BRV-CREM", "BRV-CRMC", "BRV-DIRC", "BRV-CHAP", "BRV-XTND", "BRV-ORGN", "BRV-WEBC", "BRV-MEMB", "BRV-SCAT",
       "BRV-CERT", "CRM", "DCR", "CHP", "CHX", "ORG", "WEB", "BOR", "SCT", "CRT", "Cremation", "Cremation - child",
       "Direct cremation", "Chapel 40 min", "Chapel 40 min (child)", "Chapel extension 20 min", "Organist",
       "Webcast & recording", "Memorial book entry", "Garden scattering", "Certified copy - cremation certificate"}
ADJ = {"BRV-ADJ", "ADJ", "Credit - account"}


def ledger(target):
    rows = []
    with open(os.path.join(target, W.FILES["ar_halbrook"]), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            code = {"HMC": "CM-0417", "OHC": "CM-0738"}[r["site"]]
            rows.append(("H", code, r["doc_type"], r["posting_date"], r["customer_no"], r["service_date"],
                         r["item_code"], round(float(r["net_amount"]) * 100)))
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, W.FILES["ar_shoreline"]), read_only=True, data_only=True)
    loc = {"Fenwick Harbour": "CM-1182", "Stannard Bay": "CM-2034", "Port Alder": "CM-1768", "Sorrel Bay": "CM-2409"}
    for r in wb["Receivables"].iter_rows(min_row=2, values_only=True):
        rows.append(("S", loc[r[0]], "INV" if r[2] == "Invoice" else "CRN", r[1].date().isoformat(), r[4],
                     r[6].date().isoformat() if r[6] else "", r[7], round(float(r[10]) * 100)))
    with open(os.path.join(target, W.FILES["ar_members"]), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append(("F" + r["fund_code"], r["fund_code"], "INV" if r["record"] == "FEE" else "CRN", r["week_ending"],
                         r["fd_account"], r["service_date"], r["fee_code"], round(float(r["amount_ex_tax"]) * 100)))
    return rows


def subset_effects(amount, items, kmax=4):
    """items: list of (cents, key). Every way of choosing up to kmax items summing to amount, by its effect."""
    from itertools import combinations
    items = sorted(items)
    pairs = {}
    idx = list(range(len(items)))
    for k in (1, 2):
        for comb in combinations(idx, k):
            s = sum(items[i][0] for i in comb)
            if s <= amount:
                pairs.setdefault(s, []).append(comb)
    effects = set()
    for s, combs in pairs.items():
        rest = amount - s
        if rest == 0:
            for comb in combs:
                effects.add(_eff(items, comb))
        elif rest in pairs:
            for c1 in combs:
                for c2 in pairs[rest]:
                    if max(c1) < min(c2) and len(c1) + len(c2) <= kmax:
                        effects.add(_eff(items, c1 + c2))
    return effects


def _eff(items, comb):
    out = {}
    for i in comb:
        out[items[i][1]] = out.get(items[i][1], 0) + items[i][0]
    return tuple(sorted(out.items()))


def levies(target):
    comm, _ = register(target)
    rows = ledger(target)
    ab = lambda code, d: comm[code] is not None and d > comm[code]
    base = {}
    inv = [r for r in rows if r[2] == "INV"]
    by = {}
    for r in inv:
        by.setdefault((r[0], r[4]), []).append(r)
        if r[6] in INC and r[5][:4] == "2026":
            k = (r[1], ab(r[1], dt.date.fromisoformat(r[5])))
            base[k] = base.get(k, 0) + r[7]
    for r in rows:
        if r[2] != "CRN":
            continue
        if r[6] not in ADJ:
            if r[6] in INC and r[5][:4] == "2026":
                k = (r[1], ab(r[1], dt.date.fromisoformat(r[5])))
                base[k] = base.get(k, 0) + r[7]
            continue
        end = dt.date.fromisoformat(r[3])
        items = []
        for x in by[(r[0], r[4])]:
            d = dt.date.fromisoformat(x[5])
            if 0 <= (end - d).days <= 200:
                items.append((x[7], (x[1], d.year, ab(x[1], d), x[6] in INC)))
        eff = subset_effects(-r[7], items)
        if len(eff) != 1:
            return None
        for (code, y, a, inc), cts in next(iter(eff)):
            if inc and y == 2026:
                base[(code, a)] = base.get((code, a), 0) - cts
    out = {}
    for c in W.CREMATORIA:
        un, a = base.get((c[0], False), 0), base.get((c[0], True), 0)
        v = (un * 45 + a * 15) / 1000.0 / 100.0
        out[c[0]] = int(v + 0.5) if v >= 0 else -int(-v + 0.5)
    return out


# ---------------------------------------------------------------- bypassed cremations, from the inlet temperature
def bypass_from_trace(target):
    import pyarrow.parquet as pq
    t = pq.read_table(os.path.join(target, W.FILES["plant"])).to_pydict()
    comm, _ = register(target)
    et = ZoneInfo(W.TZ_NAME)
    by_code = {}
    for code, ts, rec, ev, temp in zip(t["fund_code"], t["logged_utc"], t["record"], t["event"], t["inlet_temp_c"]):
        by_code.setdefault(code, []).append((ts, rec, ev, temp))
    cyc = {}
    with open(os.path.join(target, W.FILES["cycles"]), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["cycle_type"] != "CREMATION":
                continue
            s = dt.datetime.strptime(r["charge_et"], "%Y-%m-%d %H:%M").replace(tzinfo=et)
            e = dt.datetime.strptime(r["end_et"], "%Y-%m-%d %H:%M").replace(tzinfo=et)
            cyc.setdefault(r["fund_code"], []).append((s, e))
    out = {}
    for code, recs in by_code.items():
        recs.sort(key=lambda x: (x[0], x[1] != "READING"))
        stopped, warming, runs, cur = False, False, [], None
        for ts, rec, ev, temp in recs:
            if rec == "EVENT":
                if ev == "PLANT STOP":
                    stopped = True
                if ev == "PLANT START":
                    stopped, warming = False, True
                continue
            if warming and temp is not None and temp >= 100:
                warming = False
            cold = temp is not None and temp < 60 and not stopped and not warming
            if cold and cur is None:
                cur = [ts, ts]
            elif cold:
                cur[1] = ts
            elif cur is not None:
                runs.append((cur[0] - dt.timedelta(minutes=20), ts))
                cur = None
        hits = {}
        for s, e in cyc.get(code, []):
            if any(s <= b1 and e >= b0 for b0, b1 in runs):
                q = (s.month - 1) // 3 + 1
                hits[q] = hits.get(q, 0) + 1
        c = comm[code]
        first = 1 if c.year < 2026 else (c.month - 1) // 3 + 1
        out[code] = {"Q%d" % q: hits.get(q, 0) for q in range(first, 5)}
    return out


def main(target, golden_dir):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    cells = survey_cells(target)
    check("survey: every published cell read back off the three reports (1996 13 bands, 2006 and 2016 15, by sex)",
          sum(1 for k in cells if k[0] == 1996 and k[1] in "MF") == 26 and
          sum(1 for k in cells if k[0] == 2006) == 30 and sum(1 for k in cells if k[0] == 2016 and k[1] in "MF") == 30,
          "%d cells" % len(cells))
    import survey as S
    tab = S.tables(W.SEED)
    same = all(abs(cells[k] - tab[k]["amalgam"]) < 1e-9 for k in cells)
    check("survey: the PDFs print the generator's cells exactly", same)
    share, des, n = the_call(target, cells)
    names = {c[0]: c[2] for c in W.CREMATORIA}
    check("call: recomputed from the permits, the register and the PDFs' cells", [names[c] for c in des] ==
          fig["call"]["designated"] and abs(share - fig["call"]["share_pct"]) < 0.01 and n == fig["call"]["cremations_2026"],
          "%.2f per cent, %s" % (share, ", ".join(names[c] for c in des)))
    cert = " ".join(text(os.path.join(golden_dir, W.GOLDEN["cert"])).split())
    check("certificate: names the designated crematoria and the share as recomputed",
          all(names[c] in cert for c in des) and ("about %d per cent" % int(round(share))) in cert)
    lev = levies(target)
    check("levies: recomputed with an independent subset search, every crematorium equal to figures.json",
          lev == fig["levy"], "" if lev == fig["levy"] else str({k: (lev[k], fig["levy"][k]) for k in fig["levy"]
                                                                  if lev and lev[k] != fig["levy"][k]}))
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(golden_dir, W.GOLDEN["book"]), read_only=True, data_only=False)
    ws_lev = {r[0]: r[5] for r in wb["Levy 2026"].iter_rows(min_row=2, values_only=True) if r[0]}
    check("workbook: the levy sheet carries the recomputed levies", ws_lev == lev)
    byp = bypass_from_trace(target)
    check("bypass: found from the inlet temperature alone, every cell equal to figures.json", byp == fig["bypass"],
          "" if byp == fig["bypass"] else str(byp))
    ws_b = {}
    for r in wb["Bypassed cremations 2026"].iter_rows(min_row=2, values_only=True):
        ws_b.setdefault(r[0], {})[r[2].split()[1]] = r[3]
    check("workbook: the bypass sheet carries the recomputed counts", ws_b == byp)
    # positive controls: each comparison fails on a wrong figure
    bad = dict(fig["levy"])
    k0 = sorted(bad)[0]
    bad[k0] += 1
    check("positive control: a levy one dollar off is caught", bad != lev)
    bad_b = json.loads(json.dumps(fig["bypass"]))
    bad_b["CM-0417"]["Q1"] += 1
    check("positive control: a bypass count one off is caught", bad_b != byp)
    cells2 = dict(cells)
    k1 = (2016, "F", 70)
    cells2[k1] = cells2[k1] + 2.0
    s2, d2, _ = the_call(target, cells2)
    check("positive control: a survey cell misread moves the recomputed share", abs(s2 - share) > 0.05)
    fails = [o for o in OUT if not o[1]]
    for label, good, detail in OUT:
        print("%s  %s%s" % ("PASS" if good else "FAIL", label, ("  [%s]" % detail) if detail else ""))
    print("verify: %d checks, %d failures" % (len(OUT), len(fails)))
    return not fails


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    sys.exit(0 if main(os.path.join(task, "target"), os.path.join(task, "golden")) else 1)
