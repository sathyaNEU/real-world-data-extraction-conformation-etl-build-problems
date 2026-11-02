"""task473 ask layer against the careful solver's routes, on the cut pack.

    python3 task473/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The ask is the
guidelines' 3.1 baselines, 28 figures: for each county, the impaired-driving offenses committed there in 2025 that its
county court had prosecuted by 28 February 2027 (one for each person charged and offense) and the per cent of them
that had ended in an impaired-driving conviction by then. A figure is kept when it equals figures.json's in its
printed cell (whole numbers, per cents to one decimal).

The cracker is the careful solver, never a narrowed one. It lands the call (the band catch rates, bundle.golden_g),
runs the hygiene battery on the courts' extract (exact and near-exact duplicate rows, one row per court and case
number, case numbers in filing order, both dates on each row, every label read as written) and executes every filed
rule as worded: guidelines 3.1's offenses committed in 2025 (the offense date), the county court, one for each person
charged and offense, a conviction for impaired driving (a guilty plea or verdict on an impaired-driving charge, the
convicted_charge column's own words), by 28 February 2027. The extract carries no party identifier, so the careful
solver's person and offense is the court's case. Its handling is written here, apart from bundle.ask_court. The
mirror stops at the default path (R6, one unarrested share) and, the ask being decoupled from the call, reads the
ask as the cracker does. The over-cleaner (one prosecution per court, offense date and arresting agency) is printed
as a stop. The full includer is the golden's own route (bundle.ask_court: a case dismissed on the day its court
opened another for the same offense date and agency is one prosecution with it) and has to give back figures.json
exactly.

The pair is the ask sheet's formula: 38 recommendation and components (the list 6, the 14 rates, the 14 deaths, the
chart 4, scaled to 38), 7 instruction following, 55 asks over the 28 figures. Exit 0 when the gate holds (the cracker
keeps no ask figure, the pair at or under 60, the mirror under half the ask weight, two careful responses on the call
under 70), 2 when it does not, 1 when a control fails. The script modifies nothing and never runs inside the build."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bundle as B     # noqa: E402  (the verifier's readers)
import methods as M    # noqa: E402  (the ladder's routes, run on the bundle's reading)

TASK = os.path.dirname(HERE)
W_CALL, W_INSTR, W_ASK = 38.0, 7.0, 55.0
GATE = 60.0


def pack_dir(arg):
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling473-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    return tmp, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(tmp)),
                                                hashlib.md5(open(src, "rb").read()).hexdigest())


# ------------------------------------------------------------------------------------------------ the ask, the cracker
IMPAIRED = "UNDER THE INFLUENCE"


def battery(rows):
    """the hygiene battery a careful analyst runs on the courts' extract before counting"""
    out = []
    full = [tuple(r.values()) for r in rows]
    out.append(("exact duplicate rows", len(full) == len(set(full)), "%d rows" % len(full)))
    keys = [(r["county_fips"], r["case_number"]) for r in rows]
    out.append(("one row per court and case number", len(keys) == len(set(keys)),
                "%d case numbers repeat across courts, none within one" % (len(keys) - len({r["case_number"]
                                                                                         for r in rows}))))
    near = Counter(tuple(v for k, v in r.items() if k != "case_number") for r in rows)
    twins = [k for k, v in near.items() if v > 1]
    in_ask = [k for k in twins if IMPAIRED in k[6] and k[3].startswith("2025")]
    out.append(("near-exact duplicates (every field but the case number)", not in_ask,
                "%d pairs, each a night's co-arrested drivers still open, none an impaired-driving offense of 2025"
                % len(twins) if not in_ask else "%d pairs in the ask's window" % len(in_ask)))
    seq = True
    by = defaultdict(list)
    for r in rows:
        by[(r["county_fips"], r["filed_date"][:4])].append(r)
    for g in by.values():
        g.sort(key=lambda r: r["case_number"])
        seq &= all(g[i]["filed_date"] <= g[i + 1]["filed_date"] for i in range(len(g) - 1))
    out.append(("case numbers in filing order within each court and year", seq, "%d court-years" % len(by)))
    both = all(r["offense_date"] <= r["filed_date"] and (not r["disposition_date"] or
                                                         r["filed_date"] <= r["disposition_date"]) for r in rows)
    out.append(("both dates on a row: offense before filing, filing before disposition", both, ""))
    labels = Counter(r["disposition"] or "(none)" for r in rows)
    out.append(("dispositions as labelled", True, ", ".join("%s %d" % kv for kv in sorted(labels.items()))))
    return out


def ask_cracker(rows):
    """each county's 2025 impaired-driving prosecutions and per cent convicted, the careful solver's way: an
    impaired-driving lead charge by its words, the offense date in 2025, each case one person and offense (no party
    identifier), a conviction a guilty plea or verdict whose convicted charge is impaired driving"""
    out = defaultdict(lambda: [0, 0])
    for r in rows:
        if IMPAIRED not in r["lead_charge"] or not r["offense_date"].startswith("2025"):
            continue
        out[r["county_fips"]][0] += 1
        out[r["county_fips"]][1] += r["disposition"] in ("GUILTY PLEA", "GUILTY VERDICT") and \
            IMPAIRED in r["convicted_charge"]
    return {f: (n, 100.0 * h / n) for f, (n, h) in out.items()}


# ------------------------------------------------------------------------------------------------ scoring
def kept(by, gold, names):
    n = sum(by.get(f, (0, 0))[0] == gold[names[f]]["prosecuted"] for f in names)
    p = sum("%.1f" % by.get(f, (0, 0.0))[1] == "%.1f" % gold[names[f]]["pct_conv"] for f in names)
    return n, p


def main(arg=None):
    folder, scratch, stamp = pack_dir(arg)
    try:
        return run(folder, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


def run(target, stamp):
    print("pack: " + stamp)
    F = json.load(open(os.path.join(HERE, "figures.json")))
    dr = B.directory(target)
    names = {str(f): n for f, n in dr["counties"].items()}
    cr = B.census(target, dr)
    obs = B.observed(cr, B.complete_agencies(dr))
    miles = B.vmt(target)
    g = B.golden_g(obs, miles)
    gold_call = sorted(names[f] for f, v in g["rates"].items() if v >= 0.60)
    mir = M.route(obs, "R6")
    mir_rate = M.rate(mir, miles)
    mir_call = sorted(names[f] for f, v in mir_rate.items() if v >= 0.60)
    on, off = gold_call == sorted(F["high"]), mir_call != sorted(F["high"])
    print("cracker's call: %s (%s)" % (", ".join(gold_call), "lands the golden" if on else "MISSES"))
    print("mirror's call (R6, one unarrested share): %s (%s)" % (", ".join(mir_call), "off" if off else "ON THE CALL"))
    if not (on and off):
        return 1
    keep_rate = sum("%.2f" % mir_rate[f] == "%.2f" % g["rates"][f] for f in miles)
    keep_death = sum(int(round(mir[f])) == int(round(g["deaths"][f])) for f in miles)
    mirror_call = W_CALL / 38.0 * (keep_rate + keep_death + 2.0)

    rows = B.court(target)
    print("\nthe cracker's hygiene battery on the courts' extract:")
    for c, ok, d in battery(rows):
        print("  %-4s %s%s" % ("ok" if ok else "FAIL", c, (" (%s)" % d) if d else ""))
    gold = F["ask_court"]
    full = kept(B.ask_court(rows), gold, names)
    print("\nfull includer (control, the golden's route): %d + %d of 28" % full)
    if full != (14, 14):
        print("CONTROL FAILED: the route code does not reproduce figures.json")
        return 1
    crk_by = ask_cracker(rows)
    ck = kept(crk_by, gold, names)
    over = kept(B.ask_court(rows, "cell"), gold, names)
    gap_n = [crk_by[f][0] - gold[names[f]]["prosecuted"] for f in names]
    gap_p = [round(crk_by[f][1] - gold[names[f]]["pct_conv"], 1) for f in names]
    print("\nper route, figures kept of 28 (prosecutions + per cents):")
    print("  %-72s %2d + %2d" % ("cracker (lands the call, battery run, every filed rule; a case each)", ck[0], ck[1]))
    print("  %-72s %2d + %2d" % ("mirror (R6, off the call; the ask as the cracker)", ck[0], ck[1]))
    print("  %-72s %2d + %2d" % ("stop: one prosecution per court, offense date and agency (over-clean)", over[0],
                                over[1]))
    print("  %-72s %2d + %2d" % ("full includer (control)", full[0], full[1]))
    print("the cracker's misses: prosecutions %+d to %+d, per cents %+.1f to %+.1f points" % (
        min(gap_n), max(gap_n), min(gap_p), max(gap_p)))
    kc = ck[0] + ck[1]
    lc = kc / 28.0
    cracker = W_CALL + W_INSTR + W_ASK * lc
    mirror = mirror_call + W_INSTR + W_ASK * lc
    pair = (cracker + mirror) / 2.0
    print("\nthe mirror keeps %d of 14 rates and %d of 14 deaths in their cells (%.1f of the 38)" % (
        keep_rate, keep_death, mirror_call))
    print("cracker %.1f, mirror %.1f; two careful responses on the call %.1f each" % (cracker, mirror, cracker))
    print("  if the cracker alone finds the refiled prosecutions (keeps 28): pair %.1f" % (
        (W_CALL + W_INSTR + W_ASK + mirror) / 2.0))
    print("\nCracker keeps: %d of 28 ask figures" % kc)
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * lc))
    print("Pair ceiling: %.1f" % pair)
    held = kc == 0 and pair <= GATE and lc < 0.5 and cracker < 70.0
    print("gate: %s" % ("HOLDS" if held else "SPENT (the cracker keeps ask figures; the pair over 60)"))
    return 0 if held else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
