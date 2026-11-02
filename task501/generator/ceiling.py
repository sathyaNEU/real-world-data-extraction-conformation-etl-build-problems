"""task501 ask layer against the careful solver's routes, on the cut pack, read against the prompt as filed.

    python3 task501/generator/ceiling.py [target] [--prompt PATH]

The ask: for each option, the people born in its years whom the register holds as living in the region at 30 June
2027, how many of those have had no valid MMR dose by that date and how many exactly one (15 figures). Its two
devices, each a judgment across the register's records that no field announces:
- D-alpha: dates of birth the register holds ten years early. The child's own records place the birth ten years
  later: it was registered from the birth notification 6 to 45 days after the date ten years on, and the GP gave its
  first dose 12 to 17 months after that date. Read as held, every option's people move (A and B lose children to C
  and E, C trades with A and with D and E).
- D-beta: same-sex twins at practices whose returns carry no register number. The loader matched each GP line by
  surname, date of birth, sex and practice and loaded it to the first registration of the pair, so one twin holds two
  lines for each GP visit and the other none. One child has one dose at a visit: the second line is the co-twin's.
  Read as loaded, the co-twins' no-dose and one-dose figures move in every option.
Hazards the careful solver handles (work orders): LH27 reissued in July 2024 (the circular), merged registrations with
chains, replaced and withdrawn GP lines (the query log), pupils living in Northern Ireland held with no area code,
doses given on 1 and 2 July (the prompt's "by that date"), the guidelines' interval and first-birthday rules.

The cracker lands the call, reads every field by its plain meaning (date_of_birth as the child's date of birth, the
person number on an event as the person who had the dose, date_given as the day it was given), executes every filed
rule (the circular, guidelines 12.5, the as-at date) and runs the hygiene battery: keys unique; exact and near-exact
duplicates (two GP lines on one registration on one day read as one dose, which the interval rule already counts
once); re-sent school sessions; the merge table walked to the surviving record; the query log applied; orphans and
anti-joins (none); GP return lines tested for uniqueness across registrations (none shared); a person-duplicate check
on date of birth, sex and household fields, which finds the twins (kept as two children, the careful choice; merging
them is printed as its own route). The mirror is the best response off the call (no catch-up, every diary), scored on
readings of its own at their strongest: every hazard handling the battery offers, and at most one device cracked
beyond it, chosen against the answers, the worst honest number. The full includer handles both devices and must
reproduce figures.json exactly. Pair on the generated rubric's weights by the sheet's formula: 38 recommendation and
components, 7 instruction following, 55 for the ask's 15 figures; a wrong call keeps r = 5 (the deck's chart and
slide structure); each response keeps 8 per cent of the ask weight as method credit beside the figures it lands."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import re
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A        # noqa: E402
import bundle as B      # noqa: E402
import world as W       # noqa: E402

KEYS = ("A", "B", "C", "D", "E")
METHOD_CREDIT = 0.08    # the ask sheet's method credit on the ask paths, as a share of the ask weight
R_OFF = 5               # what a wrong call keeps of the recommendation block (chart and slide structure)
WINDOW = re.compile(r"\bhave had no valid MMR dose (?:by that date|by 30 June 2027|on or before 30 June 2027)\b")


def figure_keys(figs):
    out = {}
    for k in KEYS:
        out["residents %s" % k] = int(figs["ask1_register_residents"][k].replace(",", ""))
        out["none %s" % k] = int(figs["ask2_no_valid_dose"][k].replace(",", ""))
        out["one %s" % k] = int(figs["ask2_one_valid_dose"][k].replace(",", ""))
    return out


def run(f, area="golden", merge_how="chain", ev_how="golden", window="date given", dob_how="corrected",
        twins="reattributed", link="golden", unlisted="keep"):
    """One complete pipeline: its 15 figures."""
    a1 = A.ask1(f, how=area, link=link, unlisted=unlisted, dob_how=dob_how)
    ev = f["events"]
    keep = A.AS_AT
    if window == "loaded by 30 June":
        ev = ev[ev["loaded_on"] <= W.AS_AT.isoformat()]
    if window == "every row in the extract":
        A.AS_AT = pd.Timestamp("2099-12-31")
    try:
        a2 = A.ask2(f, pop=area, ev_how=ev_how, merge_how=merge_how, link=link, events=ev, unlisted=unlisted,
                    twins="loaded" if twins == "merged" else twins, dob_how=dob_how)
    finally:
        A.AS_AT = keep
    out = {}
    for k in KEYS:
        out["residents %s" % k] = a1[k]
        out["none %s" % k] = a2[k]["none"]
        out["one %s" % k] = a2[k]["one"]
    return out


def digest(target):
    zp = os.path.join(os.path.dirname(target.rstrip("/")), "target.zip")
    h = hashlib.sha256()
    for fn in sorted(os.listdir(target)):
        h.update(fn.encode())
        h.update(open(os.path.join(target, fn), "rb").read())
    z = hashlib.md5(open(zp, "rb").read()).hexdigest() if os.path.exists(zp) else "no target.zip"
    return h.hexdigest()[:16], z


def main(target, prompt_path):
    figs = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    truth = figure_keys(figs)
    total = len(truth)
    prompt = open(prompt_path, encoding="utf-8").read()
    win_filed = bool(WINDOW.search(prompt))
    f = B.ask_frames(target)
    d_pack, d_zip = digest(target)
    print("pack %s (target/ sha256 %s, target.zip md5 %s)" % (target, d_pack, d_zip))
    print("prompt %s (%d characters): doses dated by the day given %s; the ask: %d figures (people, no valid dose, "
          "exactly one, for each of five options); the deck's chart and call slide are scored with the recommendation "
          "(outside)" % (prompt_path, len(prompt), "FILED" if win_filed else "not filed", total))

    def hits(out):
        return sum(out[k] == truth[k] for k in truth)

    named = {
        "the natural path: current code list, no merges, every loaded line, dates of birth as held, lines as loaded":
            dict(area="current", merge_how="none", ev_how="all", dob_how="held", twins="loaded"),
        "the cracker: circular, merges walked, replaced and withdrawn lines out, dates of birth as held, lines as "
        "loaded, twins kept as two children": dict(dob_how="held", twins="loaded"),
        "the cracker with the twins its person check finds merged as one child (over-cleaning)":
            dict(dob_how="held", twins="merged", link="household"),
        "the cracker plus D-alpha (dates of birth read as born), lines as loaded": dict(twins="loaded"),
        "the cracker plus D-beta (the twins' lines given back), dates of birth as held": dict(dob_how="held"),
        "the cracker reading every registration 6 to 45 days after any birthday as a birth registration "
        "(over-cleaning D-alpha)": dict(dob_how="any_birthday", twins="loaded"),
        "the cracker with a person key on date of birth, sex and area code (over-cleaning)":
            dict(dob_how="held", twins="loaded", link="dob_sex_area"),
        "the cracker with registrations no practice lists left out": dict(dob_how="held", twins="loaded",
                                                                         unlisted="drop"),
        "full includer: both devices handled": dict(),
    }
    outs = {}
    for nm, kw in named.items():
        outs[nm] = run(f, **kw)
        print("  %-112s %2d of %d" % (nm, hits(outs[nm]), total))
    full = outs["full includer: both devices handled"]
    exact = all(full[k] == truth[k] for k in truth)
    print("full includer (every device handled): %d of %d ask figures, %s" % (
        hits(full), total, "reproduces figures.json exactly" if exact else "DOES NOT REPRODUCE"))
    if not exact:
        return 1
    cracker = outs["the cracker: circular, merges walked, replaced and withdrawn lines out, dates of birth as held, "
                   "lines as loaded, twins kept as two children"]
    kc = hits(cracker)
    print("  the cracker's misses by figure: %s" % ", ".join("%s %+d" % (k, cracker[k] - truth[k]) for k in truth))

    # the mirror: every hazard handling the battery offers, and at most one device cracked beyond it
    windows = ("date given",) if win_filed else ("date given", "every row in the extract", "loaded by 30 June")
    grid = {}
    for area, merge_how, ev_how, window, (dob_how, twins) in itertools.product(
            ("golden", "current"), ("chain", "one_hop"), ("golden", "all"), windows,
            (("held", "loaded"), ("corrected", "loaded"), ("held", "reattributed"), ("held", "merged"))):
        link = "household" if twins == "merged" else "golden"
        out = run(f, area=area, merge_how=merge_how, ev_how=ev_how, window=window, dob_how=dob_how, twins=twins,
                  link=link)
        grid[(area, merge_how, ev_how, window, dob_how, twins)] = hits(out)
    best = max(grid, key=lambda k: grid[k])
    km = grid[best]
    print("the mirror's grid: %d pipelines (2 area readings x 2 merge walks x 2 query handlings x %d dose-date "
          "handlings x 4 device handlings: neither, D-alpha, D-beta, the twins merged); its best keeps %d of %d (%s)"
          % (len(grid), len(windows), km, total, ", ".join(best)))

    def score(on_call, kept):
        L = kept / float(total) + METHOD_CREDIT
        return min(100.0, (38 + 7 + 55 * L) if on_call else (R_OFF + 7 + 55 * L))
    C, S = score(True, kc), score(False, km)
    print("cracker (on the call; circular, merges, queries, interval, dates of birth as held, lines as loaded): %d of %d "
          "ask figures, %.1f" % (kc, total, C))
    print("mirror (off the call, no catch-up on every diary; %s): %d of %d ask figures, %.1f" % (", ".join(best), km,
                                                                                               total, S))
    print("Cracker keeps: %d of %d ask figures" % (kc, total))
    print("Mirror leakage: %.1f per cent of ask weight (%d of %d figures, plus %.0f per cent method credit)" % (
        100.0 * km / total + 100 * METHOD_CREDIT, km, total, 100 * METHOD_CREDIT))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    Cm = score(True, km)
    print("both top responses on the call (the cracker and the mirror's ask route): %.1f and %.1f, pair %.1f" % (
        C, Cm, (C + Cm) / 2))
    for nm, key in (("also read the dates of birth as born (D-alpha)",
                     "the cracker plus D-alpha (dates of birth read as born), lines as loaded"),
                    ("also gave the twins' lines back (D-beta)",
                     "the cracker plus D-beta (the twins' lines given back), dates of birth as held")):
        k = hits(outs[key])
        print("  if the cracker %s: %d of %d, %.1f, pair with the mirror %.1f" % (nm, k, total, score(True, k),
                                                                               (score(True, k) + S) / 2))
    print("  if the cracker cracked both devices: %d of %d, %.1f, pair with the mirror %.1f" % (
        total, total, score(True, total), (score(True, total) + S) / 2))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", default=os.path.join(os.path.dirname(HERE), "target"))
    ap.add_argument("--prompt", default=os.path.join(os.path.dirname(HERE), "prompt.txt"))
    a = ap.parse_args()
    sys.exit(main(a.target, a.prompt))
