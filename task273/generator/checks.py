"""task273 architecture 4: the generator's assertions. The ladder, the licensed family's agreement, the forks,
the three-rules block on the clean truth, the asks' devices, the separation line and the pack's hygiene."""
from __future__ import annotations

import csv
import os
import re

import numpy as np

import analysis as A
import params as P

FOUNDERS = {"SACS", "TMEM216", "SLC26A2"}


class Ck:
    def __init__(self):
        self.n = 0
        self.fail = []

    def __call__(self, label, ok, detail=""):
        self.n += 1
        if not ok:
            self.fail.append("%s: %s" % (label, detail))


def run(target, golden, w, S, fig):
    ck = Ck()
    R = S["rungs"]
    gold = R["golden"]
    # ------------------------------------------------------------------ the call and the ladder
    ck("CALL panel of 14", len(S["panel"]) == 14, S["panel"])
    ck("CALL the founders join, none leaves", set(S["joining"]) == FOUNDERS and not S["leaving"],
       (S["joining"], S["leaving"]))
    ck("CALL the eleven current conditions stay", set(S["panel_2026"]) <= set(S["panel"]))
    for r in A.FAMILY:
        ck("SF7 FAMILY %s files the panel" % r, A.panel(R[r]) == S["panel"], A.panel(R[r]))
        for g in gold:
            ck("SF7 FAMILY %s rounds %s alike" % (r, g), A.per_thousand(R[r][g]) == A.per_thousand(gold[g]),
               (R[r][g] * 1000, gold[g] * 1000))
    for g, v in gold.items():
        x = v * 1000
        spread = max(R[r][g] for r in A.FAMILY) * 1000 - min(R[r][g] for r in A.FAMILY) * 1000
        ck("EDGE %s clear of a rounding edge" % g, abs(x - np.floor(x) - 0.5) >= max(0.03, 1.5 * spread), (x, spread))
        ck("SF8 LINE %s clear of the line" % g, abs(x - 5.0) >= 0.5, x)
    for r in A.EASY:
        miss = set(A.panel(R[r])) ^ set(S["panel"])
        ck("LADDER %s misses exactly the founders" % r, miss == FOUNDERS, sorted(miss))
        for g in FOUNDERS:
            ck("LADDER %s leaves %s at most 4.65" % (r, g), R[r][g] * 1000 <= 4.65, R[r][g] * 1000)
    # the analyst test on the clean truth: the 10-read filter, every field read right
    ck("ANALYST the depth-filtered count files the eleven", A.panel(R["cc10"]) == sorted(S["panel_2026"]),
       A.panel(R["cc10"]))
    # the true carrier share (the generator's own truth) sides with the golden on every designation
    true = {g: (w.gene_carrier[g] & w.cohort).sum() / w.cohort.sum() for g in w.gene_carrier}
    for s in w.study_reclass:
        if A.class_on(s, P.CENSUS) in A.PLP:
            true[s["gene"]] = ((w.gene_carrier[s["gene"]] | w.carries[s["site_id"]]) & w.cohort).sum() / w.cohort.sum()
    ck("TRUTH the generator's carriers file the golden panel", A.panel(true) == S["panel"], A.panel(true))
    # ------------------------------------------------------------------ forks (the fork table's rows)
    nocohort = {}
    co = w.cohort
    allrel = ~w.qc_fail
    w.cohort = allrel
    nocohort = A.frequencies(w, "golden")
    w.cohort = co
    ck("SF1 every released member (withdrawals kept) files the same panel", A.panel(nocohort) == S["panel"])
    late = (~w.withdrawn) & (~w.qc_fail) & (~w.withdrawn_late)
    w.cohort = late
    early = A.frequencies(w, "golden")
    w.cohort = co
    ck("SF2 the late withdrawals dropped as well files the same panel", A.panel(early) == S["panel"])
    for g in gold:
        ck("SF2 late withdrawals move no rounded figure (%s)" % g, A.per_thousand(early[g]) == A.per_thousand(gold[g]))
    # register vintage: today's classes equal the census date's (no change after 1 November 2026)
    ck("SF3 no register change between the census and the extract",
       all(A.class_on(s, P.CENSUS) == A.class_on(s, P.EXTRACT) for s in w.sites))
    # GJB2 c.101T>C counted (its class before June 2026) moves GJB2's figure but not the panel
    m34 = [s for s in w.study_reclass if s["gene"] == "GJB2"][0]
    c = w.called[m34["site_id"]] & co
    add = sum(c[(w.phase == p) & co].sum() / w.sens[m34["site_id"]][(w.phase == p) & co].sum() * ((w.phase == p) & co).sum()
              for p in (1, 2)) / co.sum()
    ck("SF4 GJB2 with its downgraded variant stays on the panel", (gold["GJB2"] + add) >= P.PANEL_LINE)
    # a member called at two sites in one gene: none (each counted once either way)
    for g, *_ in P.CONDITIONS:
        sites = A.census_sites(w, g)
        tot = sum((w.called[s["site_id"]] & co).astype(int) for s in sites)
        ck("SF5 no member called twice in %s" % g, int(np.max(tot)) <= 1)
    # the binomial allele fraction read from the data: phase 2 heterozygous calls average half alternate reads
    fr2 = []
    for s in w.study_sites:
        m = w.called[s["site_id"]] & (w.phase == 2)
        if m.any():
            fr2.append((w.alt_reads[s["site_id"]][m] / w.depth[s["site_id"]][m]).mean())
    ck("SF6 heterozygous calls carry half their reads as the alternate", abs(np.mean(fr2) - 0.5) < 0.01, np.mean(fr2))
    # ------------------------------------------------------------------ the ask
    gb = S["ask_b"]
    sfid = {"result date": "SF9", "received date": "SF9", "carried-forward dropped": "SF10",
            "the export's class column": "SF11", "today's register": "SF11", "people not couples": "SF12"}
    for name, var in S["ask_b_variants"].items():
        diff = sum(1 for k in gb if var[k] != gb[k])
        ck("%s ASK_B %s moves figures" % (sfid[name], name), diff >= 3, diff)
    # separation: the programme's two reclassified variants have no Study carrier; no Study file names a couple
    for s in w.sites:
        if s["gene"] in ("ATP7B", "PAH") and s["history"]:
            ck("SEPARATION %s has no Study carrier" % s["c"], not w.carries[s["site_id"]].any())
    # ------------------------------------------------------------------ the pack
    files = sorted(os.listdir(target))
    ck("PACK eleven files", len(files) == 11, files)
    ck("PACK no file describes the data", not any(re.search(r"readme|dictionar|manifest|codebook|notes", f, re.I)
                                                  for f in files), files)
    with open(os.path.join(target, [f for f in files if "depth" in f][0])) as fh:
        rd = csv.reader(fh)
        head = next(rd)
        rows = list(rd)
    ck("PACK spine 25,000 rows or more", len(rows) >= 25000, len(rows))
    ph = dict(zip(w.sample_id, w.phase))
    lo = min(min(int(x) for x in r[1:]) if ph[r[0]] == 1 else 99 for r in rows)
    ck("PACK every phase 1 depth at its floor or above", lo >= P.CALLER[1]["floor"], lo)
    for f in files:
        if f.endswith((".csv", ".tsv")):
            txt = open(os.path.join(target, f), encoding="utf-8").read()
            ck("PACK no em dash in %s" % f, "—" not in txt and "–" not in txt)
            dates = re.findall(r"\b(20\d\d-\d\d-\d\d)\b", txt)
            ck("PACK no date after assembly in %s" % f, not dates or max(dates) <= P.ASSEMBLED.isoformat(),
               max(dates) if dates else "")
    # invented names against the real-place list
    ref = [x.strip().lower() for x in open(os.path.join(os.path.dirname(__file__), "h21_reference_places.txt"))
           if x.strip()]
    for nm_ in ("Ardvenny", "Morvaig", "Glenhaskel", "Kilvenny", "Quarrendale", "Strathvenny"):
        c_ = nm_.lower()
        near = [r for r in ref if (abs(len(r) - len(c_)) <= 2 and _ed(r, c_) <= 2) or c_ in r.split()]
        ck("H21 %s is not a real place's near twin" % nm_, not near, near[:3])
    print("checks: %d run, %d failed" % (ck.n, len(ck.fail)))
    for f in ck.fail[:40]:
        print("  FAIL", f)
    return not ck.fail


def _ed(a, b):
    m, n = len(a), len(b)
    d = list(range(n + 1))
    for i in range(1, m + 1):
        p = d[:]
        d[0] = i
        for j in range(1, n + 1):
            d[j] = min(p[j] + 1, d[j - 1] + 1, p[j - 1] + (a[i - 1] != b[j - 1]))
    return d[n]
