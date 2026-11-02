"""The ask layer's ceiling, measured on the cut pack. Rows:

- cracker: the careful solver on the call. It lands the call, reads every field by its plain meaning (FM-1 is the
  licence meter, the telemetry's time_utc is UTC and the licence day is local, the register restarts at the October
  2025 meter change, a ticket's date is its date, the product master's pack size is the size), executes every filed
  rule as worded and runs the hygiene battery (exact re-sent ticket rows dropped, the clock converted, the meter swap
  bridged, the OB2 casing change applied, the kPa converted).
- mirror: the same careful solver off the call (Theis on the 2014 test, the default path).
- includer, ticket-dated: notices the bulk loads were never metered and adds every ticket on its own date.
- over-cleaner: reads every line 3 size off the QC net fill weights, sparkling included.
- full includer: every device handled; must reproduce figures.json or the script exits 1.

Scored on 38 (recommendation and critical components), 7 (instruction following) and 55 (asks), a figure hit when
within half a unit of its stated rounding."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C        # noqa: E402
import common as K      # noqa: E402
import deliver as DL    # noqa: E402

TASK = os.path.dirname(HERE)


def main_figs(b, image):
    mc = C.main_call(b)
    T, S, img, prot = mc["T"], mc["S"], mc["img"], mc["prot"]
    g = C.largest(prot, T, S, img if image else None)
    at = {n: C.nearest(C.assessment(K.APPLIED_QD, xy, T, S, img if image else None), 1.0) for n, xy, _ in prot}
    passes = all(C.assessment(K.APPLIED_QD, xy, T, S, img if image else None) <= av for n, xy, av in prot)
    return dict(largest=C.nearest(g[0], 100.0), limiting=g[1], passes=passes, at1800=at, T=round(T), S=round(S * 1e4, 1))


def ask_figs(b, tankers, shift, sizes):
    a = C.ask_a(b, tankers=tankers, shift_dating=shift)
    bb = C.ask_b(b, sizes)
    out = {}
    for k in DL.MONTHS_A:
        lab = "%04d_%02d" % k
        out["askA_volume_%s" % lab] = C.nearest(a[k][0], 100.0)
        out["askA_days_%s" % lab] = a[k][1]
    for k in DL.MONTHS_B:
        out["askB_l3_%04d_%02d" % k] = round(bb[k], 2)
    return out


def score_main(m, figs):
    hits = [m["largest"] == figs["call_largest_m3d"], m["limiting"] == figs["call_limiting"], not m["passes"],
            m["T"] == figs["T_m2d"], m["S"] == figs["S_e4"]]
    hits += [m["at1800"][n] == figs["at1800_%s_m" % n.split()[0].lower()] for n in m["at1800"]]
    hits += [m["limiting"] == figs["call_limiting"]]                  # the chart is drawn for the limiting borehole
    return sum(hits) / len(hits)


def score_asks(a, figs):
    keys = [k for k in figs if k.startswith("askA_volume_") or k.startswith("askA_days_") or k.startswith("askB_l3_")]
    hit = 0
    per = {}
    for k in keys:
        unit = 100.0 if "volume" in k else (1.0 if "days" in k else 0.01)
        h = abs(a[k] - figs[k]) <= unit / 2.0 + 1e-9
        hit += h
        blk = k.split("_")[0] + "_" + k.split("_")[1]
        per.setdefault(blk, [0, 0])
        per[blk][0] += h
        per[blk][1] += 1
    return hit / len(keys), per


def main():
    target = os.path.join(TASK, "target")
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    b = C.bundle(target)
    on, off = main_figs(b, True), main_figs(b, False)
    rows = []
    for name, m, asks in (("cracker (careful, on the call)", on, ask_figs(b, False, True, "master")),
                          ("mirror (careful, off the call)", off, ask_figs(b, False, True, "master")),
                          ("includer, ticket-dated (on the call)", on, ask_figs(b, True, False, "master")),
                          ("over-cleaner (on the call)", on, ask_figs(b, False, True, "qc")),
                          ("full includer (on the call)", on, ask_figs(b, True, True, "true"))):
        ms = score_main(m, figs)
        sa, per = score_asks(asks, figs)
        total = 38.0 * ms + 7.0 + 55.0 * sa
        rows.append((name, ms, sa, total, per))
        print("%-38s main %5.1f%%  asks kept %5.1f%%  total %5.1f  %s" % (name, 100 * ms, 100 * sa, total,
              ", ".join("%s %d/%d" % (k, v[0], v[1]) for k, v in sorted(per.items()))))
    full = rows[-1]
    if full[2] < 1.0 or full[1] < 1.0:
        raise SystemExit("the full includer does not reproduce figures.json")
    cracker, mirror = rows[0], rows[1]
    pair = (cracker[3] + mirror[3]) / 2.0
    print("Pair ceiling: %.1f (cracker %.1f, mirror %.1f); Mirror leakage: %.1f per cent of ask weight; "
          "two careful responses on the call: %.1f each" % (pair, cracker[3], mirror[3], 100 * mirror[2], cracker[3]))
    if pair > 60.0 or cracker[3] >= 70.0:
        raise SystemExit("ceiling above the bar")
    return rows, pair


if __name__ == "__main__":
    main()
