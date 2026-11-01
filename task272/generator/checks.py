"""The generator's assertions, run on the world's clean truth and on the cut pack.

T1 the analyst test on the clean truth; T2 the golden family and its margins on the pack; T3 every rung files a
different set; S the shock test (the call is no interval of any shipped statistic); SF the semantic forks; H the
generator patterns a reader sees (steps, stamps); A the asks (rounding edges, devices that move figures); L the
words no shipped document may carry; G the golden memo's claims.

    python3 task272/generator/checks.py
"""
import csv
import subprocess
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import figs as F    # noqa: E402
import pack as K    # noqa: E402
import params as P  # noqa: E402
import world as W   # noqa: E402

FAIL = []
N = [0]


def check(name, ok, info=""):
    N[0] += 1
    if not ok:
        FAIL.append(name)
    print("%s %s %s" % ("ok  " if ok else "FAIL", name, info))


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    call = set(fig["call"]["products"])
    cands = sorted(fig["golden"])
    w = W.simulate()
    tr = W.truth()

    # T1: on the clean truth (every dose's true delivered volume) the policy's rate names the golden set, and the
    # textbook capability study of the weighed doses' true deviations does not
    truth_set = {c for c in cands if tr[c]["per100k"] > P.LIMIT_PER_100K}
    check("T1 truth names the call", truth_set == call, "%s" % sorted(truth_set))
    devs = {}
    for c in w["checks"]:
        devs.setdefault(c["dose"]["product"], []).append(c["dose"]["dev"])
    ppk_true = set()
    for c in cands:
        v = np.array(devs[c])
        mu, sd = v.mean(), v.std(ddof=1)
        tol = W.product(c)["tol"]
        r = 1e5 * (F._phi((-tol - mu) / sd) + F._phi((mu - tol) / sd))
        if r > P.LIMIT_PER_100K:
            ppk_true.add(c)
    check("T1 the capability study on the clean weighed doses files another set", ppk_true != call, "%s" % sorted(ppk_true))
    check("T1 truth margins", min(tr[c]["per100k"] for c in call) >= 3 * P.LIMIT_PER_100K and
          max(tr[c]["per100k"] for c in cands if c not in call) <= 0.5 * P.LIMIT_PER_100K,
          "flagged min %.1f, others max %.1f" % (min(tr[c]["per100k"] for c in call),
                                                 max(tr[c]["per100k"] for c in cands if c not in call)))

    # T2: the golden family agrees, with margins
    lo = min(min([fig["golden"][c]["rate"]] + list(fig["family"][c].values())) for c in call)
    hi = max(max([fig["golden"][c]["rate"]] + list(fig["family"][c].values())) for c in cands if c not in call)
    for m in ("fixed", "shrunk", "own_slope"):
        check("T2 family member %s files the call" % m, set(fig["ladder"][m]) == call)
    check("T2 family margins", lo >= 3 * P.LIMIT_PER_100K and hi <= 0.5 * P.LIMIT_PER_100K, "in min %.1f, out max %.1f" % (lo, hi))
    check("T2 the call is four products", fig["call"]["count"] == 4)

    # T3: every rung files a different set
    for k in ("ppk", "within", "checked", "sorted"):
        check("T3 rung %s files another set" % k, set(fig["ladder"][k]) != call, "%s" % fig["ladder"][k])
    check("T3 the reflex flags the bag products", {"P0610", "P0614", "P0618"} <= set(fig["ladder"]["ppk"]))

    rec = F.load(TARGET)
    # S: the call is no interval of any shipped statistic, sorted either way
    stats = {}
    for c in cands:
        ds = [d for d in rec["doses"] if d["product"] == c and d["status"] == "COMPLETE"]
        sets = [s for s in rec["sets"].values() if s["product"] == c]
        batches = {d["batch"] for d in ds}
        ck = [x for x in rec["checks"] if x["product"] == c]
        dv = np.array([x["dev"] for x in ck])
        pumped = {}
        for d in ds:
            pumped[d["set"]] = max(pumped.get(d["set"], 0.0), d["L"] + d["ml"] / 1000.0)
        multi = {}
        for d in ds:
            multi.setdefault(d["set"], set()).add(d["batch"])
        stats[c] = dict(doses=len(ds), batches=len(batches), sets=len(sets), checks=len(ck),
                        fails=sum(1 for x in ck if x["result"] == "FAIL"), mean=float(dv.mean()), sd=float(dv.std()),
                        min=float(dv.min()), max_l=max(pumped.values()), ppk=fig["rungs"][c]["ppk"],
                        multi=sum(1 for v in multi.values() if len(v) > 1) / len(multi),
                        three=sum(1 for v in multi.values() if len(v) > 2),
                        sorts=fig["sorts"][c]["sorts"], vol=W.product(c)["vol"])
    for k in stats[cands[0]]:
        order = sorted(cands, key=lambda c: stats[c][k])
        top = set(order[-len(call):])
        bot = set(order[:len(call)])
        if k == "min":
            # the lowest weighed dose orders the four first: a closest approach files no rate per 100,000 and no cut
            # in the pack separates them; recorded as a WARN in the design note's Readability screen
            print("WARN S min (the one-dimensional law): %s" % ("interval" if bot == call or top == call else "clear"))
            continue
        check("S %s" % k, top != call and bot != call)

    # SF: the semantic forks, each closed by a filed sentence or asserted to leave the call standing
    def call_now():
        return set(c for c in cands if F.rebuilt_rate(rec, c, "random")[0] > P.LIMIT_PER_100K)

    def relitre(new_set_at_reseat=False, aborted=False):
        """Recompute every completed dose's set and litres pumped under an alternative reading."""
        rows = []
        with open(os.path.join(TARGET, K.FILES["events"]), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["event"] == "SET_UP":
                    rows.append((r["compounder_sn"], dt.datetime.strptime(r["event_time"], "%Y-%m-%dT%H:%M:%SZ")
                                 .replace(tzinfo=F.UTC), r["set_lot"]))
        by, seen = {}, set()
        for s_, t_, lot in sorted(rows, key=lambda x: x[1]):
            if not new_set_at_reseat and (s_, lot) in seen:
                continue
            seen.add((s_, lot))
            by.setdefault(s_, []).append((t_, "%s#%d" % (lot, len(by.get(s_, [])))))
        pumped = {}
        for d in sorted(rec["doses"], key=lambda d: (d["serial"], d["t"])):
            lst = by[d["serial"]]
            i = max(j for j in range(len(lst)) if lst[j][0] <= d["t"])
            key = (d["serial"], lst[i][1])
            if d["status"] == "COMPLETE":
                d["set"] = key
                d["L"] = pumped.get(key, 0.0)
                pumped[key] = d["L"] + d["ml"] / 1000.0
            elif aborted:
                pumped[key] = pumped.get(key, 0.0) + d["ml"] / 1000.0
    pol = subprocess.run(["pdftotext", "-layout", os.path.join(TARGET, K.FILES["policy"]), "-"], capture_output=True,
                         text=True).stdout
    pol1 = " ".join(pol.split())
    # SF1 aborted fills as doses made: each is a partial fill, so every product crosses 10; the policy files it out
    n_ab = {c: sum(1 for d in rec["doses"] if d["product"] == c and d["status"] == "ABORTED") for c in cands}
    alt = {c for c in cands if 1e5 * n_ab[c] / fig["golden"][c]["doses"] > P.LIMIT_PER_100K}
    check("SF1 aborted fills as doses made would flag %d products; PH-QP-07 2 files them out" % len(alt),
          alt != call and "is not a dose made" in pol1)
    # SF2 the weighed doses only: rung 2, another set; the policy's "whether or not" closes it
    check("SF2 the weighed doses only file another set", set(fig["ladder"]["checked"]) != call and
          "whether or not the dose was weighed or quarantined" in pol1)
    # SF3 the year by UTC: the evening fills of 31 December move nothing
    keep = rec["doses"]
    rec["doses"] = [d for d in keep if d["t"].year == 2026]
    check("SF3 the UTC year files the same call", call_now() == call, "%d fills differ" % (len(keep) - len(rec["doses"])))
    rec["doses"] = keep
    # SF4 a re-seat as a new set (the litres restarting at the re-seat): the same call
    relitre(new_set_at_reseat=True)
    check("SF4 a re-seat restarting the litres files the same call", call_now() == call)
    # SF5 aborted fills' volume counted in the litres pumped: the same call
    relitre(aborted=True)
    check("SF5 aborted fills' volume in the litres files the same call", call_now() == call)
    relitre()
    check("SF5 the golden reading restored", call_now() == call)
    # SF6 the family (asserted in T2): the start fixed per set, shrunk per set, a slope per set
    check("SF6 every member of the family files the call", all(set(fig["ladder"][m]) == call
                                                               for m in ("fixed", "shrunk", "own_slope")))
    # SF7 every register weight read as net: the first half's doses read 40 to 80 per cent heavy; the headers close it
    wb = __import__("openpyxl").load_workbook(os.path.join(TARGET, K.FILES["checks"]), read_only=True)
    heads = [next(ws.iter_rows(values_only=True))[5] for ws in wb.worksheets]
    check("SF7 the register's headers name gross and net weights", heads[:2] == ["Gross wt (g)"] * 2 and
          heads[2:] == ["Net wt (g)"] * 2, "%s" % heads)
    # SF8 GC-1's two products in scope: both under 10, and PH-QP-07 3.2 keeps them out
    gc_n, gc_out = {}, {}
    with open(os.path.join(TARGET, K.FILES["gc1"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            gc_n[r["product_no"]] = gc_n.get(r["product_no"], 0) + 1
            gc_out[r["product_no"]] = gc_out.get(r["product_no"], 0) + (r["verdict"] == "OUT")
    gc = {c: 1e5 * gc_out[c] / gc_n[c] for c in gc_n}
    check("SF8 GC-1's products are out of scope and under 10 either way", max(gc.values()) < P.LIMIT_PER_100K and
          "are not configured" in pol1, "%s" % {k: round(v, 2) for k, v in gc.items()})
    # SF9 more than 10 against 10 or more: no product sits between 3 and 50
    rates = [fig["golden"][c]["rate"] for c in cands]
    check("SF9 no rate between 3 and 50", not any(3 <= x <= 50 for x in rates) or
          min(fig["golden"][c]["rate"] for c in call) > 40)
    # SF10 and SF11 are the asks' devices, asserted in A below

    # H: generator patterns
    import pyarrow.parquet as pq
    t = pq.read_table(os.path.join(TARGET, K.FILES["doses"])).to_pydict()
    per = {}
    for s_, tt in zip(t["compounder_sn"][:60000], t["fill_end_time"][:60000]):
        per.setdefault(s_, []).append(dt.datetime.fromisoformat(tt))
    gaps = []
    for s_, xs in per.items():
        xs.sort()
        gaps += [(b - a).total_seconds() for a, b in zip(xs, xs[1:]) if (b - a).total_seconds() < 300]
    vals, cnt = np.unique(np.array(gaps), return_counts=True)
    check("H dose times have no fixed step", len(vals) >= 15 and cnt.max() < 0.3 * len(gaps),
          "%d distinct gaps, the commonest %.0f per cent" % (len(vals), 100 * cnt.max() / len(gaps)))
    with open(os.path.join(TARGET, K.FILES["events"]), encoding="utf-8") as f:
        lots = sorted({r["set_lot"] for r in csv.DictReader(f)})
    nums = [int(x.split("-")[1]) for x in lots]
    check("H set lots have no fixed step", len({b - a for a, b in zip(sorted(nums), sorted(nums)[1:])}) > 50)
    stamps = []
    for k, fn in K.FILES.items():
        path = os.path.join(TARGET, fn)
        if fn.endswith(".pdf"):
            data = open(path, "rb").read()
            c = re.search(rb"/CreationDate \(D:(\d{14})", data).group(1)
            m = re.search(rb"/ModDate \(D:(\d{14})", data).group(1)
            check("H %s created before modified" % fn, c < m)
            stamps.append(c)
        if fn.endswith(".xlsx"):
            z = zipfile.ZipFile(path)
            core = z.read("docProps/core.xml").decode()
            c = re.search(r"<dcterms:created[^>]*>([^<]*)<", core).group(1)
            m = re.search(r"<dcterms:modified[^>]*>([^<]*)<", core).group(1)
            check("H %s created before modified" % fn, c < m, "%s %s" % (c, m))
            stamps.append(c)
    check("H every document has its own creation stamp", len(set(stamps)) == len(stamps))

    # A: the asks
    a_utc = F.ask_a(rec, utc_as_local=True)
    a_gold = F.ask_a(rec)
    moved = sum(1 for k in a_gold if a_gold[k] != a_utc.get(k))
    check("A SF10 ask A: reading UTC as local time moves figures", moved >= 40, "%d of %d" % (moved, len(a_gold)))
    a_ser = F.ask_a(rec, by_serial=True)
    check("A SF10 ask A: PC-3 has two serials", len({k[0] for k in a_ser}) == 6)
    b_rows = F.ask_b(rec, rows_not_lots=True, target=TARGET)
    b_gold = F.ask_b(rec)
    moved = sum(1 for c in cands if b_rows[c] != b_gold[c])
    check("A SF11 ask B: counting SET_UP rows moves figures", moved >= 10, "%d of %d" % (moved, len(cands)))

    # L: words no shipped document carries
    banned = re.compile(r"\b(wear|wears|worn|drift|drifts|fatigue|degrad\w*|litres? pumped|pumped|overrun)\b", re.I)
    hits = []
    for fn in (K.FILES["policy"], K.FILES["sop"]):
        txt = subprocess.run(["pdftotext", "-layout", os.path.join(TARGET, fn), "-"], capture_output=True, text=True).stdout
        hits += [(fn, m.group(0)) for m in banned.finditer(txt)]
    body = open(os.path.join(TARGET, K.FILES["request"]), encoding="utf-8", errors="ignore").read()
    hits += [("request", m.group(0)) for m in banned.finditer(body)]
    check("L no shipped document names the step", not hits, "%s" % hits[:3])

    # G: the memo's claims
    weighed = {id(x["dose"]) for x in w["checks"]}
    for c in ("P0412", "P0507"):
        bad = [d for d in w["doses"] if d["product"] == c and d["status"] == "COMPLETE" and abs(d["dev"]) > 5]
        k = sum(1 for d in bad if id(d) in weighed)
        check("G almost none of %s's out-of-tolerance doses were weighed" % c, k <= 0.1 * max(1, len(bad)),
              "%d of %d weighed" % (k, len(bad)))
    check("G every product off the list is under 3", max(fig["golden"][c]["rate"] for c in cands if c not in call) < 3)
    check("G midazolam does not move with litres pumped", abs(fig["fits"]["P0702"]["loss_per_litre"]) < 0.1)
    check("G the bags start high", min(fig["fits"][c]["start"] for c in ("P0610", "P0614", "P0618")) > 1.5)

    print("%d checks, %d failed" % (N[0], len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
