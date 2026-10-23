"""task486's generator checks: the three-rules block on the clean truth and on the pack, the golden against the people
actually served, the licensed resolutions' agreement, every semantic fork row, the separation of the asks, the ask
devices, the bins and the input gates. Exit 1 on any FAIL.

    python3 task486/generator/checks.py            builds the world and reads task486/target
"""
import collections
import copy
import datetime as dt
import json
import os
import re
import sys
import warnings

import numpy as np

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TASK = os.path.dirname(HERE)

import bundle as B     # noqa: E402
import methods as MT   # noqa: E402
import pack as P       # noqa: E402
import sim as S        # noqa: E402
import world as W      # noqa: E402

FAILS = []
DEFAULT = {"HAL": 7964889, "MEL": 4294829, "OND": 2972162, "PYR": 2132517, "DVC": 635602}    # the note's Ends on
GOLDEN = {"HAL": 7993704, "MEL": 4283337, "OND": 2962447, "PYR": 2125478, "DVC": 635035}     # the note's Golden


def check(name, ok):
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        FAILS.append(name)


def edge(v, unit):
    return unit / 2 - abs(v - round(v / unit) * unit)


def served_sub(I, act, comp, roots):
    groups = collections.defaultdict(list)
    for i in comp:
        groups[roots[i]].append(i)
    out = []
    for idx in groups.values():
        if not any(act[i]["active"] for i in idx):
            continue
        hm = [(act[i]["hmis_entry"], act[i]["hmis_coc"]) for i in idx if act[i]["hmis_entry"] is not None]
        if hm:
            out.append(max(hm)[1])
        elif any(act[i]["dv"] for i in idx):
            out.append("DVC")
        else:
            out.append(max((act[i]["last_other"], act[i]["other_coc"]) for i in idx
                           if act[i]["last_other"] is not None)[1])
    return tuple(sorted(out))


def run(target, golden_dir, world=None, meta_path=None, fig_path=None):
    del FAILS[:]
    w = world or S.World()
    g = B.Golden(target)
    I, act = g.I, g.act

    # ------------------------------------------------------------------------------------------ three rules (7.1)
    wact = MT.record_activity(w)
    truth = MT.counts(MT.people_served(w, [r["pid"] for r in w.records], wact))
    easy = MT.counts(MT.people_served(w, MT.resolve(w.records, w.links, constrained=False), wact))
    step = MT.counts(MT.people_served(w, MT.resolve(w.records, w.links), wact))
    check("T1 clean truth: every chain of LINK findings merged, every filed rule applied, files the default path's "
          "amounts %s" % MT.allocation(easy), MT.allocation(easy) == DEFAULT)
    check("T1 clean truth: the decisive step alone (strongest first, no two records of one source in a person) files "
          "the golden %s" % MT.allocation(step), MT.allocation(step) == GOLDEN)
    check("T2 the golden is the people actually served, by recipient %s" % truth, step == truth)
    check("T3 the pack's golden equals the generator's: %s" % g.counts, g.counts == truth and g.amounts == GOLDEN)
    dflt = I.counts(I.served(I.resolve(constrained=False), act))
    check("T4 on the pack, every chain merged files %s" % B.allocation(dflt), B.allocation(dflt) == DEFAULT)

    # ------------------------------------------------------------------------------------------ the family (F1)
    roots_c = I.resolve(constrained=False)
    grp = collections.defaultdict(list)
    for i, r in enumerate(roots_c):
        grp[r].append(i)
    conf = [sorted(v) for v in grp.values()
            if any(n > 1 for n in collections.Counter(I.records[i][0] for i in v).values())]
    check("F0 %d merged groups hold two records of one source (%d with FY2026 service)" % (
        len(conf), sum(1 for v in conf if any(act[i]["active"] for i in v))), len(conf) == 225)
    recs = [{"src": r[0]} for r in I.records]
    score = {(min(a, b), max(a, b)): s for a, b, s in I.links + I.nonlinks}
    by_rec = collections.defaultdict(list)
    for l in I.links:
        by_rec[l[0]].append(l)
    rng = np.random.default_rng(11)
    bad, members_seen = 0, collections.Counter()
    gold_r = g.roots
    for comp in conf:
        cset = set(comp)
        sub = [l for i in comp for l in by_rec[i] if l[1] in cset]
        ref = served_sub(I, act, comp, gold_r)
        mem = MT.family(recs, comp, sub, score, rng, trials=12)
        live = [i for i in comp if act[i]["active"]]
        lset = set(live)
        lsub = sorted((l for l in sub if l[0] in lset and l[1] in lset), key=lambda t: (-t[2], t[0], t[1]))
        lroots = {i: i for i in comp}
        if live:
            lroots.update(MT._local_resolve(recs, live, lsub, lsub))
        mem.append(("strongest first, FY2026 records only", lroots))
        for name, roots in mem:
            members_seen[name] += 1
            if served_sub(I, act, comp, roots) != ref:
                bad += 1
    check("F1 every licensed resolution of every conflicted group returns the golden's people and recipients "
          "(%d member runs: %s)" % (sum(members_seen.values()), dict(members_seen)), bad == 0)
    for name, roots in (("R2 chains merged on FY2026 records only",
                         I.resolve(constrained=False, keep={i for i, a in enumerate(act) if a["active"]})),
                        ("R4 quarantine", I.quarantine()), ("R0 no linkage", list(range(len(I.records))))):
        c = I.counts(I.served(roots, act))
        al = B.allocation(c)
        check("F2 %s keeps none of the five amounts (%d people)" % (name, sum(c.values())),
              all(al[k] != g.amounts[k] for k in al))

    # ------------------------------------------------------------------------------------------ the fork table
    lo, hi = B.LO, B.HI
    late = [c for c in I.contacts if c["date"] in (dt.date(2025, 9, 30), dt.date(2026, 9, 30)) and
            int(c["time"][11:13]) >= 16]
    a_utc = I.activity(hot_utc=True)
    check("SF4 no outreach contact after 16:00 local on 30 September (%d), and the UTC reading gives the golden" %
          len(late), not late and I.counts(I.served(g.roots, a_utc)) == g.counts)
    ex_first = [e for e in I.enrollments if e["exit"] == lo]
    check("SF5 no HMIS exit on 1 October 2025 (%d), and the nights reading of an open enrollment gives the golden" %
          len(ex_first), not ex_first and I.counts(I.served(g.roots, I.activity(exit_night=True))) == g.counts)
    dv_first = [s for s in I.dv_stays if s["end"] == lo]
    check("SF6 no coalition stay ends on 1 October 2025 (%d), and StayEnd read as a night gives the golden" %
          len(dv_first), not dv_first and I.counts(I.served(g.roots, I.activity(dv_end_inclusive=True))) == g.counts)
    c7 = I.counts(I.served(g.roots, I.activity(clinic_any_status=True)))
    check("SF7 counting every clinic encounter (Doubling Up and Unknown too) gives %d people and moves all five "
          "amounts" % sum(c7.values()), all(B.allocation(c7)[k] != g.amounts[k] for k in c7))
    groups = collections.defaultdict(list)
    for i, r in enumerate(g.roots):
        groups[r].append(i)
    ties = 0
    for idx in groups.values():
        hm = [(act[i]["hmis_entry"], act[i]["hmis_coc"]) for i in idx if act[i]["hmis_entry"] is not None]
        if hm and len({c for d, c in hm if d == max(hm)[0]}) > 1:
            ties += 1
    check("SF8 no person's latest open enrollment ties across Continuums (%d)" % ties, ties == 0)
    multi = 0
    enc_coc = collections.defaultdict(set)
    for e in I.encounters:
        enc_coc[I.index[("WSH", e["key"])]].add(I.site_coc[e["site"]])
    for idx in groups.values():
        cocs = set()
        for i in idx:
            if I.records[i][0] == "HOT":
                cocs.add("HAL")
            cocs |= enc_coc.get(i, set())
        if len(cocs) > 1:
            multi += 1
    check("SF9 every person's outreach contacts and clinic encounters fall in one Continuum (%d otherwise)" % multi,
          multi == 0)
    pool = B.FUND * (1 - B.ADMIN)
    total = sum(g.counts.values())
    exact = {k: pool * g.counts[k] / total for k in B.RECIPIENTS}
    floor = {k: int(v) for k, v in exact.items()}
    need = int(round(pool)) - sum(floor.values())
    order = sorted(B.RECIPIENTS, key=lambda k: -(exact[k] - floor[k]))
    lr = {k: floor[k] + (1 if k in order[:need] else 0) for k in B.RECIPIENTS}
    check("SF10 each amount rounded to the dollar sums to %d; a largest-remainder split to 18,000,000 differs on %s" % (
        sum(g.amounts.values()), [k for k in lr if lr[k] != g.amounts[k]]),
        sum(lr.values()) == 18000000 and any(lr[k] != g.amounts[k] for k in lr))
    full = {k: int(round(B.FUND * g.counts[k] / total)) for k in B.RECIPIENTS}
    check("SF11 splitting the whole 18,750,000 moves all five amounts", all(full[k] != g.amounts[k] for k in full))
    keep = {i for i, a in enumerate(act) if a["active"]}
    check("SF12 the constrained resolution on FY2026 records only gives the golden",
          I.counts(I.served(I.resolve(keep=keep), act)) == g.counts)
    dv_hmis = 0
    for idx in groups.values():
        if any(act[i]["dv"] for i in idx) and any(act[i]["hmis_entry"] is not None for i in idx):
            dv_hmis += 1
    check("SF13 %d survivors with an HMIS enrollment open in the year are placed with their Continuum, not the "
          "coalition" % dv_hmis, dv_hmis > 0)
    hm_only = I.counts(I.served(g.roots, [a if I.records[i][0].startswith("HMIS") else
                                          dict(a, active=False) for i, a in enumerate(act)]))
    check("SF14 counting HMIS records only moves all five amounts",
          all(B.allocation(hm_only)[k] != g.amounts[k] for k in B.RECIPIENTS))
    days = [int(e.split("/")[1]) for e in
            [r["EntryDate"] for r in B._csv(os.path.join(target, B.FILES["enrollment"])) if r["SourceCoC"] == "MEL"]]
    check("SF15 Melbray's EntryDate carries days over 12 in the second place (%d), so it reads month/day/year" %
          sum(1 for d in days if d > 12), sum(1 for d in days if d > 12) > 0)
    check("SF16 the region is the five recipients' people together (%d)" % total, total == 40023)
    nd = B.shelter_nights(I, dedup=False)
    check("SF17 summing each stay's nights moves all 16 cells",
          all(nd[c][q] != g.nights[c][q] for c in B.COCS for q in range(4)))
    ns = B.shelter_nights(I, nbn_by_beds=False)
    check("SF18 the respite read by its enrollment span moves Halvering's winter quarters only",
          [(c, q) for c in B.COCS for q in range(4) if ns[c][q] != g.nights[c][q]] == [("HAL", 0), ("HAL", 1)])
    th = sum(1 for e in I.enrollments if e["type"] == 2)
    check("SF19 transitional housing (%d enrollments) is outside ask A's project types" % th, th > 0)
    ra = B.rrh_waits(I, rows="all")
    check("SF20 every row carrying a move-in date moves Ondrava's households with children and the region's",
          B.hround(ra[("OND", True)], 1) != B.hround(g.rrh[("OND", True)], 1) and
          B.hround(ra[("ALL", True)], 1) != B.hround(g.rrh[("ALL", True)], 1))
    rr = [e for e in I.enrollments if e["type"] == 13]
    ex_by = collections.defaultdict(list)
    for e in I.enrollments:
        if e["exit"] is not None:
            ex_by[(e["coc"], e["pid"])].append(e["exit"])
    gaps = sum(1 for e in rr for x in ex_by.get((e["coc"], e["pid"]), ()) if 1 <= (e["entry"] - x).days <= 2)
    rn = B.rrh_waits(I, chain=None)
    check("SF21 no rapid re-housing entry one or two days after an exit of the same person (%d); the move-in "
          "enrollment's own entry moves all 10 figures" % gaps,
          gaps == 0 and all(B.hround(rn[k], 1) != B.hround(g.rrh[k], 1) for k in g.rrh if k != "n"))
    for t in B.TYPES:
        mm = sum(g.rrh[(c, t)] for c in B.COCS) / 4
        check("SF22 the mean of the four Continuums' averages (%.2f) differs from the region's (%.2f), %s" % (
            mm, g.rrh[("ALL", t)], B.TYPE_NAME[t]), B.hround(mm, 1) != B.hround(g.rrh[("ALL", t)], 1))
    kids = sum(1 for e in I.enrollments if e["rel"] == 2)
    check("SF23 household type reads from RelationshipToHoH 2 (%d child rows)" % kids, kids > 0)
    check("SF1 counting records as people moves all five amounts",
          all(B.allocation(I.counts(I.served(list(range(len(I.records))), act)))[k] != g.amounts[k]
              for k in B.RECIPIENTS))
    inside = sum(1 for i, j, s in I.nonlinks if g.roots[i] == g.roots[j])
    check("SF2 no NONLINK pair sits inside a golden person (%d)" % inside, inside == 0)
    lk = [s for a, b, s, f in I.pairs if f == "LINK"]
    nl = [s for a, b, s, f in I.pairs if f == "NONLINK"]
    check("SF3 every LINK scores 9.0 or more and every NONLINK 4.0 to 8.9", min(lk) >= 9.0 and 4.0 <= min(nl) and
          max(nl) < 9.0)

    # ------------------------------------------------------------------------------------------ separation
    J = copy.copy(I)
    J.enrollments = [dict(e, move_in=None) for e in I.enrollments]
    J.beds = []
    check("X1 the call reads no move-in date and no bed night: the golden without them is the same",
          J.counts(J.served(J.resolve(), J.activity())) == g.counts)
    K = copy.copy(I)
    K.pairs, K.links, K.nonlinks = [], [], []
    K.dv_stays, K.encounters, K.contacts = [], [], []
    check("X2 the asks read no linkage finding and no coalition, clinic or outreach row",
          B.shelter_nights(K) == g.nights and B.rrh_waits(K) == g.rrh)

    # ------------------------------------------------------------------------------------------ ask devices
    nde = B.shelter_nights(I, drop_earlier=True)
    check("A1 the pack's nights equal the generator's (same conventions)", g.nights == MT.shelter_nights(w))
    check("A2 dropping the earlier of two overlapping stays moves all 16 cells",
          all(nde[c][q] != g.nights[c][q] for c in B.COCS for q in range(4)))
    wr = MT.rrh_waits(w)
    check("B1 the pack's waits equal the generator's to the printed decimal",
          all(B.hround(wr[c], 1) == B.hround(sum(g.rrh[(c, t)] * g.rrh["n"][(c, t)] for t in B.TYPES) /
                                             sum(g.rrh["n"][(c, t)] for t in B.TYPES), 1) for c in B.COCS))
    rh = B.rrh_waits(I, chain="hoh")
    moved = [k for k in g.rrh if k != "n" and B.hround(rh[k], 1) != B.hround(g.rrh[k], 1)]
    check("B2 chaining through heads of household only moves every figure for households with children %s" % moved,
          all((c, True) in moved for c in B.COCS + ["ALL"]))
    swaps = sum(1 for st in w.rrh_stays if st["x"] is not None and st["first"][0]["pid"] != st["final"][0]["pid"])
    trs = sum(1 for st in w.rrh_stays if st["x"] is not None)
    check("B3 %d rapid re-housing stays changed project before move-in, %d with another head of household" % (
        trs, swaps), trs > 0 and swaps > 0)

    # ------------------------------------------------------------------------------------------ bins
    fr = min(abs((exact[k] - int(exact[k])) - 0.5) for k in exact)
    check("M1 every amount clears its half-dollar edge by 0.05 or more (min %.3f)" % fr, fr >= 0.05)
    ed = min(edge(v, 0.1) for k, v in g.rrh.items() if k != "n")
    check("M2 every average clears its one-decimal edge by 0.025 or more (min %.3f)" % ed, ed >= 0.025)
    if fig_path:
        f = json.load(open(fig_path))
        ok = all(f["amount|" + k] == g.amounts[k] and f["people|" + k] == g.counts[k] for k in B.RECIPIENTS)
        check("F3 figures.json carries the golden's graded figures", ok)

    # ------------------------------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    fmts = {os.path.splitext(x)[1] for x in files}
    rows = max(sum(1 for _ in open(os.path.join(target, x), encoding="utf-8")) - 1
               for x in files if x.endswith((".csv", ".jsonl")))
    check("I1 %d files, %d formats, the largest table %d rows" % (len(files), len(fmts), rows),
          len(files) >= 10 and len(fmts) >= 3 and rows >= 25000)
    if meta_path:
        meta = json.load(open(meta_path))
        dis = meta.get("distractor_files", [])
        read = set(B.FILES.values())
        check("I2 the distractors named in metadata.json are in the pack and read by no figure %s" % dis,
              len(dis) >= 2 and all(d in files and d not in read for d in dis))
    dash = re.compile("[–—]")
    texts = [os.path.join(target, x) for x in files if x.endswith((".csv", ".txt", ".jsonl"))]
    texts += [os.path.join(TASK, "prompt.txt")]
    if os.path.exists(os.path.join(TASK, "submission.md")):
        texts.append(os.path.join(TASK, "submission.md"))
    check("I3 no em or en dash in the pack's text files, the prompt or the submission",
          not any(dash.search(open(p, encoding="utf-8").read()) for p in texts))
    print()
    print("%d FAIL" % len(FAILS) if FAILS else "all checks pass")
    return not FAILS


if __name__ == "__main__":
    ok = run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), meta_path=os.path.join(TASK, "metadata.json"),
             fig_path=os.path.join(HERE, "figures.json"))
    sys.exit(0 if ok else 1)
