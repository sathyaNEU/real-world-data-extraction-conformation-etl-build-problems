"""The cracker's path, run on the cut pack.

The cracker landed the call, runs the hygiene battery (key uniqueness, exact and near-exact
duplicates, re-sent results, unmatched joins, fan-out, count ties against every control), executes
every rule the pack files, including the two the files now state in their own footers (the amended
record carries value_after; biobank_ref is the biobank's own reference for the vial), and reads every
document. For each ask this module computes what that path returns and scores it against the golden
within half a unit of the stated rounding. It is measurement, not argument.

What the battery sees, and why the path stops where it does:
- Ask 1: the register carries the laboratory accession on every row, which is the specimen's key at
  face value; its only repeats are re-sent results (a second result_seq) and second aliquots, both
  under one accession; every accession joins the biobank's register one to one, so no unmatched join
  or fan-out appears; the weekly reports' totals tie to the register's rows. Nothing on the path sets
  two accessions beside one vial.
- Ask 2: the release desk's footer says the amended record carries value_after, so the log is
  applied; a reviewed specimen counts by its review outcome; the correction released again under the
  same accession is a repeated key the battery folds; withheld and superseded rows are not releases.
  Every accession is then a specimen: a depth top-up carries an accession of its own, so no key
  repeats and no row near-duplicates another (its plate, depth, heterozygosity and release date are
  its own).
The full includer, the response that notices both devices and resolves them, is scored separately in
`full_includer` so the sheet can say what it keeps.
"""
import csv
import os
import sys

import golden as G
import world as W


def _rows(path, delim=","):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader((l for l in fh if not l.startswith("#")), delimiter=delim))


def _april_may(target):
    return [r for r in _rows(os.path.join(target, W.FILES["panel"]))
            if r["report_date"][:7] in ("2027-04", "2027-05")]


def ask1(target, key=None):
    """Distinct specimens per April and May report, on the register's own accession unless a key is
    given, and the excess of the report's results over them."""
    per = {}
    for r in _april_may(target):
        d = per.setdefault(r["report_ref"], {"rows": 0, "spec": set()})
        d["rows"] += 1
        d["spec"].add(key(r) if key else r["specimen_id"])
    return {k: {"specimens": len(v["spec"]), "difference": v["rows"] - len(v["spec"])}
            for k, v in per.items()}


def ask2(target, key=None):
    """The amended extract, a reviewed specimen by its review outcome, one per specimen and release
    month: on the accession unless a key is given."""
    amend = {(a["specimen_id"], a["field"]): a["value_after"]
             for a in _rows(os.path.join(target, W.FILES["amendments"]))}
    rel, flag, seen_r, seen_f = {}, {}, set(), set()
    for r in _rows(os.path.join(target, W.FILES["history"])):
        if r["release_status"] != "RELEASED" or not r["released_date"]:
            continue
        sid = r["specimen_id"]
        month = amend.get((sid, "released_date"), r["released_date"])[:7]
        field = "review_outcome" if r["call_source"] == "REVIEWED" else "hetx_call"
        call = amend.get((sid, field), r[field])
        k = (month, key(r) if key else sid)
        if k not in seen_r:
            seen_r.add(k)
            rel[month] = rel.get(month, 0) + 1
        if call in ("FLAG", "FLAGGED") and k not in seen_f:
            seen_f.add(k)
            flag[month] = flag.get(month, 0) + 1
    return {m: round(1000.0 * flag.get(m, 0) / rel[m], 1) for m in rel}


def _score(target, g, a1, a2):
    rows = []
    hits = 0
    for w in g["panel_weeks"]:
        got = a1.get(w["report_ref"], {})
        hits += sum(1 for k in ("specimens", "difference") if got.get(k) == w[k])
    rows.append(("A1", 2 * len(g["panel_weeks"]), hits))
    hits = sum(1 for b in g["baseline"]
               if abs(a2.get(b["month"], -1) - round(b["per_thousand"], 1)) < 0.05)
    rows.append(("A2", len(g["baseline"]), hits))
    return rows


def score(target, g=None):
    """Per ask: the figures the cracker's path returns, and how many land within half a unit of the
    golden at the rounding the asking sentence states."""
    g = g or G.compute(target)
    return _score(target, g, ask1(target), ask2(target))


def full_includer(target, g=None):
    """The response that notices both devices: accessions joined to their vial through the biobank's
    register, and accessions joined to their specimen through the extraction they were made from."""
    g = g or G.compute(target)
    vial = {r["specimen_id"]: r["biobank_ref"]
            for r in _rows(os.path.join(target, W.FILES["crosswalk"]), "\t")}
    return _score(target, g, ask1(target, key=lambda r: vial[r["specimen_id"]]),
                  ask2(target, key=lambda r: r["extraction_id"]))


def ceiling(rows):
    """supplemental-stumping Part 0: C = 38 + 7 + 55 Lc, S = r + 7 + 55 Ls with r about 5. The
    response off the call reads the asks the same way, so both rows carry the cracker's ask share."""
    total = sum(n for _a, n, _h in rows)
    kept = sum(h for _a, _n, h in rows)
    share = kept / float(total)
    c = 38 + 7 + 55 * share
    s = 5 + 7 + 55 * share
    return total, kept, share, (c + s) / 2.0, 100.0 * share


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    g = G.compute(tgt)
    rows = score(tgt, g)
    for ask, n, h in rows:
        print("%s: %d figures, cracker keeps %d, misses %d" % (ask, n, h, n - h))
    total, kept, share, pair, mirror = ceiling(rows)
    print("total %d figures, kept %d (%.1f per cent), pair ceiling %.1f, mirror leakage %.1f"
          % (total, kept, 100 * share, pair, mirror))
    full = full_includer(tgt, g)
    print("full includer: " + ", ".join("%s keeps %d of %d" % (a, h, n) for a, n, h in full))
