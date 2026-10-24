"""The asks' figures on the generator's own line records (the clean truth), the naive and over-repaired readings beside
them, and each figure's distance to its bin's edge. checks.py asserts these against what solve.py reads from the pack."""
from collections import defaultdict

import params as P

fy = lambda d: P.FY0 <= d <= P.FY1


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def ask_a(L):
    """modules a lot of 50 carries: modules stores issued in the year, net of returns, per pack shipped in the year"""
    ships = defaultdict(int)
    for s in L.ships:
        if fy(s["verzonden"]):
            ships[s["platform"]] += 1
    gold, naive, dedup, units = defaultdict(float), defaultdict(float), defaultdict(float), defaultdict(float)
    seen = set()
    for q in L.reqs:
        if not fy(q["t"].date()):
            continue
        n, k = q["platform"], P.PER_UNIT[q["platform"]]
        gold[n] += q["true_qty"] * k
        naive[n] += q["aantal"] * k
        units[n] += q["aantal"]
        key = (q["pick"], q["artikel"], q["partij"], q["aantal"]) if q["soort"] == "UITGIFTE" else None
        if key is None or key not in seen:
            dedup[n] += q["aantal"] * k
        if key is not None:
            seen.add(key)
    out = {}
    for n in P.NAMES:
        f = lambda x: 50.0 * x / ships[n]
        out[n] = dict(gold=f(gold[n]), naive=f(naive[n]), dedup=f(dedup[n]), units=f(units[n]), ships=ships[n])
    return out


def _first_runs(L, key):
    first = {}
    for x in sorted(L.runs, key=lambda x: x["start"]):
        if x["resultaat"] == "ABORT":
            continue
        k = key(x)
        if k not in first:
            first[k] = x
    return first


def ask_b(L):
    """share of packs whose first end-of-line run (an aborted run is no test) fell in the year and passed"""
    wo_of = {b["bms"]: b["werkorder"] for b in L.bms}
    by_wo = _first_runs(L, lambda x: wo_of[x["pakket"]])
    by_pack = _first_runs(L, lambda x: x["pakket"])
    with_abort = {}
    for x in sorted(L.runs, key=lambda x: x["start"]):
        with_abort.setdefault(wo_of[x["pakket"]], x)
    out = {}
    for n in P.NAMES:
        def share(first):
            xs = [x for x in first.values() if x["platform"] == n and fy(x["start"].date())]
            return 100.0 * sum(x["resultaat"] == "PASS" for x in xs) / len(xs), len(xs)
        g, cnt = share(by_wo)
        nv, cnt2 = share(by_pack)
        ab, _ = share(with_abort)
        out[n] = dict(gold=g, naive=nv, abort_as_fail=ab, packs=cnt, pack_ids=cnt2)
    return out


def ask_c(L):
    """share of the cores received in the year that were rejected at intake, from the grade each core got at its dock"""
    out = {}
    scrapped_fy = {n: sum(1 for w in L.wo if w["platform"] == n and w.get("status_export") == "AFGEKEURD"
                          and w["afgesloten"] and fy(w["afgesloten"])) for n in P.NAMES}
    for n in P.NAMES:
        rows = [x for x in L.intake if x["platform"] == n and fy(x["ontvangen"].date())]
        rej = sum(x["keuring"] == "AFGEKEURD" for x in rows)
        shown = sum(x["keuring_export"] == "AFGEKEURD" for x in rows)
        line_scrap = shown - rej
        out[n] = dict(gold=100.0 * rej / len(rows), naive=100.0 * shown / len(rows),
                      both_out=100.0 * rej / (len(rows) - line_scrap),
                      count_scrapped=100.0 * (shown - scrapped_fy[n]) / len(rows),
                      cores=len(rows), line_scrap=line_scrap)
    return out


def report(L):
    A, B, C = ask_a(L), ask_b(L), ask_c(L)
    worst = []
    for n in P.NAMES:
        a, b, c = A[n], B[n], C[n]
        ea, eb, ec = edge(a["gold"], 1.0), edge(b["gold"], 0.1), edge(c["gold"], 0.1)
        worst += [ea / 1.0, eb / 0.1, ec / 0.1]
        print("%-14s A %6.2f (naive %6.2f dedup %6.2f units %6.2f; ships %4d; edge %.2f) | B %5.2f (naive %5.2f abort %5.2f;"
              " %d packs, %d ids; edge %.3f) | C %5.2f (naive %5.2f both-out %5.2f count %5.2f; %d cores, %d scrapped; edge %.3f)"
              % (n[:14], a["gold"], a["naive"], a["dedup"], a["units"], a["ships"], ea, b["gold"], b["naive"],
                 b["abort_as_fail"], b["packs"], b["pack_ids"], eb, c["gold"], c["naive"], c["both_out"],
                 c["count_scrapped"], c["cores"], c["line_scrap"], ec))
    print("worst edge in bins", round(min(worst), 3))
    return A, B, C
