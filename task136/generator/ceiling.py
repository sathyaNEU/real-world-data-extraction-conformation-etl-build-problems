"""task136 ask layer against the careful solver's routes, on the cut pack.

    python3 task136/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The asks give 32 figures:
per feeder, the energy its head sent back to the zone substation in each of June, July and August 2026 (MWh to the
nearest 10) and its largest half-hour reverse flow over those months (MW to one decimal). Each route below is a complete
pipeline over the feeder-head SCADA historian and the zone substation's two 22 kV check meters, scored figure by figure
against figures.json; a figure is kept within half a unit of the prompt's rounding (5 MWh, 0.05 MW).

The cracker is the careful solver. It lands the call; reads every field by its plain meaning (the historian's half
hours by their start in Queensland time, each tag's bus section and feeder, the meters' interval ends, import against
export); and runs the hygiene battery: duplicate and re-sent rows (none), the clock from the hour profile (midday
reverse flow at 12:00, no shift), the meter's half hour aligned to the historian's (an interval end closes the half hour
before it), and the totals that should tie. Each bus section's historian total does not tie to its check meter (the
meter sees 36 to 37 per cent more energy), so the cracker repairs it the way a control that does not tie is repaired,
pro rata: one factor per bus section fitted to its meter. Its other repairs are scored beside it (each section's factor
as the ratio of its totals, under which they tie exactly; one factor fitted to both meters; each section's export
register shared among its feeders by the historian's reverse energy or by their connected capacity; the historian kept
as recorded). The mirror is the best response off the call (the default path)
on the natural read, the historian as recorded, and on the cracker's path. The single crack is the per-feeder
decomposition, each bay's own factor from its section's meter; the full includer makes it and has to give back
figures.json exactly (the route code's control).

The pair is the ask sheet's formula: 36 recommendation and components, 9 instruction following, 55 asks over 32
figures, a method credit of 8 per cent on every figure not kept, a response off the call keeping 4 of the 36; the same
on the comparable 38, 7 and 55 (a wrong call keeping 5) is printed beside it. Pair ceiling is the worst of the measured
pair and the single crack, on either weighting."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C     # noqa: E402
import common as K   # noqa: E402

TASK = os.path.dirname(HERE)
CREDIT = 0.08                         # the sheet's method credit on an ask figure not kept
WEIGHTS = {"ask sheet (36, 9, 55; off the call keeps 4)": (36.0, 9.0, 55.0, 4.0),
           "comparable (38, 7, 55; off the call keeps 5)": (38.0, 7.0, 55.0, 5.0)}
ASKS = [("june_mwh", "Ask 1, energy sent back in June (MWh)", 0, 5.0),
        ("july_mwh", "Ask 1, energy sent back in July (MWh)", 1, 5.0),
        ("august_mwh", "Ask 1, energy sent back in August (MWh)", 2, 5.0),
        ("largest_mw", "Ask 2, largest half-hour reverse flow (MW)", 3, 0.05)]
CRACKER = "section"
CRACKER_OTHERS = {"each section's factor as the ratio of its totals (the totals tie exactly)": "totals",
                  "one factor fitted to both meters": "one_factor",
                  "each section's metered reverse energy shared by the historian's": "share",
                  "each section's metered reverse energy shared by connected capacity": "pv_share",
                  "the historian kept as recorded (the meters taken for another quantity)": "recorded"}
MIRROR = "recorded"
FULL = "golden"


def golden():
    rf = json.load(open(os.path.join(HERE, "figures.json")))["reverse_flow"]
    return {f: {k: float(str(rf[f][k]).replace(",", "")) for k, _, _, _ in ASKS} for f in K.FEEDERS}


def kept(fig, gold):
    """Per ask column, the figures within half a unit of the prompt's rounding."""
    return {name: sum(abs(fig[f][i] - gold[f][k]) <= half + 1e-9 for f in K.FEEDERS) for k, name, i, half in ASKS}


def pair(kc, km, n, w):
    rec, ins, ask, off = w
    pts = lambda k: ask * (k + CREDIT * (n - k)) / n
    c, s = rec + ins + pts(kc), off + ins + pts(km)
    return c, s, (c + s) / 2.0


def pack_dir(arg):
    """The pack as a folder: target.zip unpacked into a scratch folder (removed after), or the folder given."""
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling136-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    inner = os.path.join(tmp, "target") if os.path.isdir(os.path.join(tmp, "target")) else tmp
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return inner, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(inner)), md5)


def main(arg=None):
    folder, scratch, stamp = pack_dir(arg)
    try:
        return run(folder, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


def run(folder, stamp):
    print("pack: " + stamp)
    L = C.load(folder)
    gold = golden()
    n = 4 * len(K.FEEDERS)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    fc = C.forecast(L)
    call = (fc["winner"], round(fc["excess"][fc["winner"]] + 1e-12, 1), fc["runner"])
    gcall = figs["call"]
    on_call = call == (gcall["feeder"], float(gcall["excess_mw"]), gcall["runner_up"])
    r0 = C.forecast(L, measure="systems", basis="letterboxed")
    print("cracker's call: %s %.1f MW over hosting capacity, runner-up %s (%s the golden)" % (
        call + ("lands" if on_call else "MISSES",)))
    print("mirror's call (default path): %s %.1f MW, runner-up %s (%s)" % (
        r0["winner"], r0["excess"][r0["winner"]], r0["runner"],
        "off the call" if r0["winner"] != gcall["feeder"] else "ON THE CALL"))
    if not on_call or r0["winner"] == gcall["feeder"] or r0["runner"] == gcall["runner_up"]:
        print("the rows below assume the cracker on the call and the mirror off it with another runner-up: they are not")
        return 1

    full = kept(C.reverse_flow(L, FULL), gold)
    if sum(full.values()) != n:
        print("CONTROL FAILED: the full includer's route gives %s of %d, the route code does not reproduce the golden"
              % (full, n))
        return 1
    hw, mw = L["scada"], L["meters"]
    for t in sorted(mw.columns):
        fs = [f for f in K.FEEDERS if L["section"][f] == t]
        x, y = hw[fs].sum(axis=1), mw[t]
        print("the totals the cracker ties: bus section %s, the meter carries %.1f per cent more energy than its four "
              "feeder heads (the ratio of totals %.4f; one factor fitted to the meter %.4f)" % (
                  t, 100 * (float(y.sum() / x.sum()) - 1), float(y.sum() / x.sum()), float((x * y).sum() / (x * x).sum())))
    kfit, rms = C.bay_factors(L)
    print("the single crack's fit: " + ", ".join("%s %.4f" % (f, kfit[f]) for f in K.FEEDERS) +
          "; rms residual " + ", ".join("%s %.4f MW" % kv for kv in sorted(rms.items())))

    def scored(how):
        k = kept(C.reverse_flow(L, how), gold)
        return k, sum(k.values())

    kc_by, kc = scored(CRACKER)
    km_by, km = scored(MIRROR)
    for who, how in (("cracker (one factor per bus section)", CRACKER), ("mirror (the historian as recorded)", MIRROR)):
        fig = C.reverse_flow(L, how)
        print("\n%s's figures by feeder (golden in brackets):" % who)
        for k, name, i, half in ASKS:
            fmt = "{:,.0f}" if half >= 1 else "{:.1f}"
            print("  %-44s %s" % (name, "; ".join("%s %s (%s)" % (f, fmt.format(fig[f][i]), fmt.format(gold[f][k]))
                                                  for f in K.FEEDERS)))
    print("\nper ask column, figures kept of %d each:" % len(K.FEEDERS))
    print("  %-44s %-9s %-9s %s" % ("", "cracker", "mirror", "full includer (control)"))
    for _, name, _, _ in ASKS:
        print("  %-44s %-9d %-9d %d" % (name, kc_by[name], km_by[name], full[name]))
    print("  %-44s %-9d %-9d %d of %d" % ("all asks", kc, km, sum(full.values()), n))
    print("\nthe cracker's other repairs, figures kept of %d:" % n)
    worst_cr = kc
    for name, how in CRACKER_OTHERS.items():
        k = scored(how)[1]
        worst_cr = max(worst_cr, k)
        print("  %-72s %d" % (name, k))

    worst = []
    for wname, w in WEIGHTS.items():
        c, s, p = pair(kc, km, n, w)
        print("\n%s: cracker %.1f, mirror %.1f, pair %.1f" % (wname, c, s, p))
        worst.append(p)
        pw = pair(worst_cr, km, n, w)[2]
        worst.append(pw)
        print("  the cracker on its best other repair: %d of %d, pair %.1f" % (worst_cr, n, pw))
        km2 = scored(CRACKER)[1]
        pm = pair(kc, km2, n, w)[2]
        worst.append(pm)
        print("  if the mirror runs the cracker's ask path (off the call): %d of %d, pair %.1f" % (km2, n, pm))
        ps = pair(n, km, n, w)[2]
        worst.append(ps)
        print("  if the cracker finds the device (the per-feeder decomposition, the single crack): %d of %d, pair %.1f"
              % (n, n, ps))
        two = w[0] + w[1] + w[2] * (kc + CREDIT * (n - kc)) / n
        print("  two careful responses both on the call, neither finding the device: %.1f each, pair %.1f" % (two, two))
    print("\nCracker keeps: %d of %d ask figures" % (kc, n))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * (km + CREDIT * (n - km)) / n))
    print("Pair ceiling: %.1f (the worst of the measured pair, the cracker's other repairs, the mirror on the cracker's "
          "path and the single crack, on either weighting)" % max(worst))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
