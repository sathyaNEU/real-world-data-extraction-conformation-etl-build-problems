"""The ask layer's ceiling, measured on the cut pack.

This script shares no code with the generator. It reads the shipped files (the warehouse extract, the
release desk's amendment log, the 2025 platform validation report) and the golden figures in
figures.json, computes what each modelled response returns for the ask, and scores every figure
against the golden within half a unit of the stated rounding (counts exact, per thousand to one
decimal).

The responses, each a complete pipeline:
- the cracker: lands the call, runs the hygiene battery and executes every filed rule. On the ask it
  applies the release desk's amendments as the log's footer files them, takes a reviewed specimen by
  its review outcome, keeps the releases dated in the twelve months, counts each specimen once (the
  correction released again repeats its accession), and reads each record's extraction method from the
  record. Where the 2025 report's codes contradict the record's name, the battery re-derives from the
  finer key, which is the name the record carries; nothing in the pack dates the re-coding.
- the mirror: the best response off the call. It reads the ask the same way (the ask consumes nothing
  the call's construction produces) but stops earlier: the amendments not applied.
- stress rows, printed and not gated: the 2025 report's codes read on every record, the 2026 table on
  the 2026 records and the names on the 2027 ones, the switch taken on the receipt date, and the full
  includer, who reads each code by the table in force on the day the DNA was extracted.

Pair arithmetic on supplemental-stumping Part 0's weights: the landed call scores 38 + 7 + 55 L, the
best miss 5 + 7 + 55 L, L the share of the ask weight kept. The chart is the call's exhibit; it is
counted inside the ask weight here (the worse of the two accountings), four criteria: the increase per
cutoff, its interval, the zero line, the cutoff marked. The cracker draws it right; the mirror's
increases are the same point estimates and its zero line is right, but its intervals and the cutoff it
marks are the unpaired route's.
"""
import csv
import json
import os
import re
import statistics
import sys

ROUND = 1                     # per thousand to one decimal; counts whole
MONTHS = ["2026-%02d" % m for m in range(3, 13)] + ["2027-01", "2027-02"]


def _rows(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(l for l in fh if not l.startswith("#")))


def _report_codes(target):
    """The 2026 method table as the 2025 platform validation report prints it."""
    try:
        import pypdf
        text = "\n".join(p.extract_text() or "" for p in
                         pypdf.PdfReader(os.path.join(target, "extraction_platform_validation_2025.pdf")).pages)
    except Exception:
        return {}
    out = {}
    for m in re.finditer(r"(?m)^\s*([1-9])\s+(magnetic bead|silica column|salting out)\b", text):
        out[m.group(1)] = m.group(2)
    return out


def reading(target, method_of, amendments=True):
    """Per method: released, reviewed, flagged, per thousand, under one reading of the method."""
    amend = {}
    if amendments:
        for a in _rows(os.path.join(target, "release_amendments_2027-04_2027-06.csv")):
            amend[(a["specimen_id"], a["field"])] = a["value_after"]
    hist = _rows(os.path.join(target, "qc_screen_history_2026-02-15_2027-02-28.csv"))
    out, seen = {}, set()
    for r in hist:
        if r["release_status"] != "RELEASED" or not r["released_date"]:
            continue
        sid = r["specimen_id"]
        if amend.get((sid, "released_date"), r["released_date"])[:7] not in MONTHS or sid in seen:
            continue
        seen.add(sid)
        field = "review_outcome" if r["call_source"] == "REVIEWED" else "hetx_call"
        call = amend.get((sid, field), r[field])
        d = out.setdefault(method_of(r), [0, 0, 0])
        d[0] += 1
        d[1] += 1 if r["call_source"] == "REVIEWED" else 0
        d[2] += 1 if call in ("FLAG", "FLAGGED") else 0
    return {m: {"released": d[0], "reviewed": d[1], "flagged": d[2],
                "per_thousand": round(1000.0 * d[2] / d[0], ROUND) if d[0] else None}
            for m, d in out.items()}


def readings(target):
    codes = _report_codes(target)
    if sorted(codes) != ["1", "2", "3"]:
        # nothing to measure the includer and two of the stress rows against: refuse, never pass
        raise SystemExit("ceiling.py: could not read the 2026 method codes from "
                         "extraction_platform_validation_2025.pdf (found %r)" % codes)
    hist = _rows(os.path.join(target, "qc_screen_history_2026-02-15_2027-02-28.csv"))
    if not hist:
        raise SystemExit("ceiling.py: the warehouse extract has no rows to score")
    # the day a code the 2026 table does not hold was first booked: the full includer's switch
    switch = min(r["extracted_date"] for r in hist if r["extraction_method_code"] not in codes)
    by_name = lambda r: r["extraction_method"]
    return {
        "cracker": reading(target, by_name),
        "mirror": reading(target, by_name, amendments=False),
        "the 2025 codes on every record": reading(
            target, lambda r: codes.get(r["extraction_method_code"], r["extraction_method"])),
        "the 2026 table for 2026 records": reading(
            target, lambda r: codes[r["extraction_method_code"]]
            if r["extracted_date"] < "2027-01-01" and r["extraction_method_code"] in codes
            else r["extraction_method"]),
        "the switch on the receipt date": reading(
            target, lambda r: codes.get(r["extraction_method_code"], r["extraction_method"])
            if r["received_date"] < switch else r["extraction_method"]),
        "full includer": reading(
            target, lambda r: codes[r["extraction_method_code"]] if r["extracted_date"] < switch
            else r["extraction_method"]),
    }, switch


def score(got, golden):
    """Figures kept within half a unit of the stated rounding."""
    kept = 0
    for m, g in golden.items():
        x = got.get(m)
        if not x:
            continue
        kept += sum(1 for k in ("released", "reviewed", "flagged") if x[k] == g[k])
        kept += 1 if x["per_thousand"] is not None and abs(x["per_thousand"] - g["per_thousand"]) < 0.05 else 0
    return kept


def measure(target, figures_path):
    golden = json.load(open(figures_path, encoding="utf-8")).get("methods") or {}
    n_ask = 4 * len(golden)
    if not n_ask:
        raise SystemExit("ceiling.py: figures.json carries no ask figure under 'methods'; nothing to score")
    rd, switch = readings(target)
    chart = {"cracker": 4, "mirror": 2}
    rows = {name: score(r, golden) for name, r in rd.items()}
    lc = (rows["cracker"] + chart["cracker"]) / float(n_ask + 4)
    ls = (rows["mirror"] + chart["mirror"]) / float(n_ask + 4)
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * ls
    asks_only = ((38 + 7 + 55 * rows["cracker"] / float(n_ask)) + (5 + 7 + 55 * rows["mirror"] / float(n_ask))) / 2
    return {"figures": n_ask, "kept": rows, "readings": rd, "switch": switch, "cracker_score": c,
            "mirror_score": s, "pair": (c + s) / 2.0, "pair_asks_only": asks_only,
            "mirror_leakage_pct": 100.0 * ls, "golden": golden}


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(here), "target")
    figs = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "figures.json")
    out = measure(tgt, figs)
    g = out["golden"]
    print("ask figures %d (4 methods x released, reviewed, flagged, per thousand); switch read %s"
          % (out["figures"], out["switch"]))
    for name, r in out["readings"].items():
        cells = "; ".join("%s %d/%d/%d/%s" % (m, r.get(m, {}).get("released", 0),
                                              r.get(m, {}).get("reviewed", 0),
                                              r.get(m, {}).get("flagged", 0),
                                              r.get(m, {}).get("per_thousand"))
                          for m in g)
        print("%-34s keeps %2d of %d  [%s]" % (name, out["kept"][name], out["figures"], cells))
    print("golden                             %s" % "; ".join(
        "%s %d/%d/%d/%.1f" % (m, v["released"], v["reviewed"], v["flagged"], v["per_thousand"])
        for m, v in g.items()))
    print("cracker %.1f (lands the call, 0 + chart 4 of %d ask criteria), mirror %.1f"
          % (out["cracker_score"], out["figures"] + 4, out["mirror_score"]))
    print("pair ceiling %.1f with the chart in the ask weight; %.1f on the ask figures alone; "
          "mirror leakage %.1f per cent" % (out["pair"], out["pair_asks_only"], out["mirror_leakage_pct"]))
