"""The cracker and the mirror, scored on the asks.

The cracker lands the call, runs the hygiene battery (key uniqueness, exact duplicates, unmatched joins, fan-out),
executes every filed rule (the funding clause with the declared times, one count per nurse per scheduled shift read
off the billing lines, Crestfield's UTC converted, the roster's keys) and reads Inland Seas' payroll date as the date a
shift was worked. The mirror stops at the most attractive wrong rung of the asks: the census night's level for the
whole day, the agencies' bill-to as the funding test. Each is scored figure by figure against the golden (a hit is
an exact whole shift), and the pair is computed on the house weights: 38 for the call and its components, 7 for
instruction-following, 55 for the asks.

    python3 cracker.py [pack]     score on the cut pack (target/ by default)
    python3 cracker.py --truth    score on the generator's clean truth, the agency reports' layouts simulated"""
from __future__ import annotations

import collections
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import common as C  # noqa: E402

D = dt.date
WEEK0 = D(2025, 11, 3)
N_WEEKS = 21
CHART_PARTS = 5          # one bar per week across the stated weeks, split by agency, block weeks marked, axis, title
W_CALL, W_IF, W_ASK, R_MISS = 38.0, 7.0, 55.0, 5.0


def week_of(d):
    k = (d - WEEK0).days // 7
    return k if 0 <= k < N_WEEKS else None


def score(lines, gold, iv, census_level=None):
    """lines: (facility_id, agency, start, surge_unit, bill) as a response counts them. Returns the response's Ask A,
    Ask B and busiest-week figures."""
    f, b, wk = collections.Counter(), collections.Counter(), collections.Counter()
    for fid, ag, st, su, bill in lines:
        if not (D(2025, 11, 1) <= st.date() <= D(2026, 3, 31)):
            continue
        if census_level is not None:
            act = census_level.get((fid, st.date()), 0) > 0
        else:
            act = any(a <= st < e for a, e, _ in iv[fid])
        fu = su and act
        if fu:
            f[fid] += 1
            k = week_of(st.date())
            if k is not None:
                wk[(k, ag)] += 1
        if bill == "POOL" and not fu:
            b[fid] += 1
    tot = collections.Counter()
    for (k, ag), v in wk.items():
        tot[k] += v
    busiest = max(tot.values()) if tot else 0
    return f, b, busiest


def pair(kept_cracker, kept_mirror, n_ask):
    c = W_CALL + W_IF + W_ASK * kept_cracker / n_ask
    s = R_MISS + W_IF + W_ASK * kept_mirror / n_ask
    return c, s, (c + s) / 2


def report(rows, gold_f, gold_b, gold_busiest, south, quiet=False):
    n_ask = 2 * len(south) + 1 + CHART_PARTS
    out = {}
    for name, (f, b, busy) in rows.items():
        hf = sum(1 for fid in south if f[fid] == gold_f[fid])
        hb = sum(1 for fid in south if b[fid] == gold_b[fid])
        hw = 1 if busy == gold_busiest else 0
        out[name] = (hf, hb, hw, hf + hb + hw + CHART_PARTS)
        if not quiet:
            print("%-34s funded %2d/%d  billed-not-funded %2d/%d  busiest week %d/1  kept %2d of %d" % (
                name, hf, len(south), hb, len(south), hw, hf + hb + hw + CHART_PARTS, n_ask))
    c, s, p = pair(out["cracker"][3], out["mirror"][3], n_ask)
    c2, s2, p2 = pair(out["cracker, A2 cracked"][3], out["mirror"][3], n_ask)
    c3, s3, p3 = pair(out["cracker, B1 cracked"][3], out["mirror"][3], n_ask)
    leak = 100.0 * out["mirror"][3] / n_ask
    if not quiet:
        print("pair ceiling %.1f (cracker %.1f, mirror %.1f); with A2 cracked %.1f; with B1 cracked %.1f" % (
            p, c, s, p2, p3))
        print("mirror leakage %.1f per cent of ask weight" % leak)
    return out, p, p2, p3, leak


def truth_mode():
    import world as W
    hs, wp, truth = W.simulate()
    decl = W.declarations(hs, truth)
    sh = W.agency_shifts(hs, truth, decl)
    iv = {h["facility_id"]: W.active_intervals(decl, h["facility_id"]) for h in hs}
    south = [h["facility_id"] for h in hs if h["region"] != "NO"]
    lvl = {(fid, r["date"]): r["level"] for fid in truth for r in truth[fid]}

    def lines(split_cracked, date_cracked):
        out = []
        for s in sh:
            st = s["start"]
            if s["agency"] == "I" and s["shift"] == "N" and not date_cracked:
                st = st + dt.timedelta(days=1)
            out.append((s["facility_id"], s["agency"], st, s["surge_unit"], s["bill"]))
            if s["agency"] == "C" and s["shift"] == "N" and not split_cracked:
                out.append((s["facility_id"], s["agency"], s["start"] + dt.timedelta(hours=5), s["surge_unit"], s["bill"]))
        return out
    gold = score(lines(True, True), None, iv)
    rows = {
        "golden": gold,
        "cracker": score(lines(False, False), None, iv),
        "cracker, A2 cracked": score(lines(True, False), None, iv),
        "cracker, B1 cracked": score(lines(False, True), None, iv),
        "mirror": score(lines(False, False), None, iv, census_level=lvl),
    }
    return report(rows, gold[0], gold[1], gold[2], south)


def pack_mode(pack=None, quiet=False):
    import pack_read as P
    return P.cracker_report(report, pack, quiet)


if __name__ == "__main__":
    if "--truth" in sys.argv:
        truth_mode()
    else:
        pack_mode(next((a for a in sys.argv[1:] if not a.startswith("--")), None))
