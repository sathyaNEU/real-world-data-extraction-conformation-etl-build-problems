"""Build the safety side of the world: cases, duplicates, laboratory samples, numbering, tables."""
import datetime as dt

import cases as K
import core as C
import frames as FR
import world as W

TD = dt.timedelta
DUP_SHARE = 0.031


def make_world(dup_filter=None):
    cases = K.assemble()
    K.apply_h1(cases)
    K.apply_added_reactions(cases)
    sq = C.Rng(71)
    dups = []
    for case in cases:
        if case["kind"] not in ("risk", "bg"):
            continue
        rec = case["rec"]
        u = sq()
        if rec.get("psp_dated") or "h1" in case or case.get("added_risk"):
            continue
        if u >= DUP_SHARE:
            continue
        if dup_filter is not None and not dup_filter(case):
            continue
        d = K.make_duplicate(case, sq)
        if d is not None:
            dups.append(d)
    allc = cases + dups
    # laboratory samples transferred by the patient support programme
    sl = C.Rng(72)
    lab_pick = C.Rng(73)
    psp_cases = [c for c in cases if c["kind"] in ("risk", "bg", "study")
                 and c["market"] in C.PSP_MARKETS
                 and (c["rec"].get("psp_mon") or c["report_type"] == "SO")
                 and c["kind"] != "study"]
    for c in psp_cases:
        labs = C.LAB_BY_MARKET[c["market"]]
        c["lab"] = labs[int(lab_pick() * len(labs))]
        c["samples"] = K.lab_samples(c, sl, c["lab"])
    K.number_cases(allc)
    # PSP patient references, per country in order of first dose
    n = {}
    for c in sorted(psp_cases, key=lambda c: (c["rec"]["lines"][0]["start"], c["case_no"])):
        n[c["market"]] = n.get(c["market"], 0) + 1
        c["psp_ref"] = "LYR-%s-%05d" % (c["market"], 1000 + 7 * n[c["market"]] + (n[c["market"]] * 13) % 7)
    return allc, dups


def tables(allc, dups):
    return dict(listing=FR.listing(allc), dosage=FR.dosage(allc), feed=FR.feed(allc), labreg=FR.lab_register(),
                dupreg=FR.dup_register(dups), terms=FR.term_list(), changes=FR.change_log())
