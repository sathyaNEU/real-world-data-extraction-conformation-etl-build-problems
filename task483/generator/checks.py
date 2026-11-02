"""task483 generator checks: the three rules (R1 to R3) on the clean truth, the fork table (SF rows), the ladder and
the shock test, the separation line, the ask devices, the realism sweep and the input gates. Run by build.py on every
build; a failure stops the ship."""
import csv
import json
import os
import re
from collections import Counter, defaultdict

import analysis as A
import pack as P
import world as W

RESULTS = []


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))
    return bool(cond)


def _slate(L, ch, n=None, floor=False):
    st = A.stopped(n, ch, L["order"], floor=floor)
    two, rk = A.slate(st)
    return set(two), st, rk


def run(target, gdir, x=None, meta_path=None, fig_path=None):
    del RESULTS[:]
    L = A.load(target)
    g = A.golden(L)
    n = g["pool"]
    GOLD = {"Morrow Cross", "Tamsey"}
    DEFAULT = {"Kesterby", "Ashwell Vale"}
    st = g["stopped"]
    rk = g["rank"]

    # --- R1 to R3: the three rules on the clean truth ---------------------------------------------------------
    ok("R1 the cultures ship at the specimen and organism grain with every drug's result",
       all(c in open(os.path.join(target, P.FILES["cultures"])).readline() for c in ("LabNo", "NITR", "MECI", "TRIM")))
    ok("R1 the issues ship one row per issue with date, product, problem and pseudonym",
       all(c in open(os.path.join(target, P.FILES["issues"])).readline() for c in
           ("IssueDate", "MedicationName", "LinkedProblem", "PatientPseudonym")))
    hdrs = " ".join(open(os.path.join(target, f)).readline().lower() for f in os.listdir(target) if f.endswith(".csv"))
    ok("R2 no column marks a culture as sent at a first consultation or after a failed course",
       not re.search(r"presentation|failure|failed|first[_ ]?course|episode|reason|clinical", hdrs))
    if x is not None:
        tr, ntr = W.presentation_truth(x["women"])
        pool_truth = defaultdict(int)
        for e in x["women"]:
            if e["day"].year == 2026 and not e["pregnant"]:
                pool_truth[(e["network"], e["drug"])] += 1
        tst = A.stopped(pool_truth, tr, L["order"])
        ttwo, trk = A.slate(tst)
        ok("R3 on the clean truth (every episode's organism) the placement is Morrow Cross and Tamsey",
           set(ttwo) == GOLD, "%s, third %s at %.1f" % (ttwo, trk[2], tst[trk[2]]))
        ok("R3 clean-truth margin of the second over the third at least 1.2", tst[trk[1]] / tst[trk[2]] >= 1.2,
           "%.3f" % (tst[trk[1]] / tst[trk[2]]))
    ab, niso = A.antibiogram(L)
    dset, dst, drk = _slate(L, ab, n)
    ok("R3 the analyst test: the cumulative antibiogram (women 16 to 64, community, first isolate a year) files "
       "Kesterby and Ashwell Vale", dset == DEFAULT, "%s" % drk[:3])
    ok("R3 nitrofurantoin reads at least 2.5 times higher in the antibiogram than at the consultation",
       ab["NIT"] / g["chances"]["NIT"] >= 2.5, "%.1f against %.1f" % (100 * ab["NIT"], 100 * g["chances"]["NIT"]))

    # --- the golden and its ladder ------------------------------------------------------------------------------
    ok("golden: the placement is Morrow Cross and Tamsey", set(g["slate"]) == GOLD, "%s" % g["slate"])
    ok("golden: the runner-up is Kesterby", rk[2] == "Kesterby", rk[2])
    ok("golden margin second over runner-up at least 1.2", st[rk[1]] / st[rk[2]] >= 1.2, "%.3f" % (st[rk[1]] / st[rk[2]]))
    ok("default margin (antibiogram) second over third at least 1.2", dst[drk[1]] / dst[drk[2]] >= 1.2,
       "%.3f" % (dst[drk[1]] / dst[drk[2]]))
    for d, lo, hi in (("NIT", 0.040, 0.070), ("MEC", 0.10, 0.15), ("FOS", 0.08, 0.12)):
        ok("golden chance %s inside its design band" % d, lo <= g["chances"][d] <= hi, "%.4f" % g["chances"][d])
    ok("presentation cultures at least 3,000", len(g["pres"]) >= 3000, "%d" % len(g["pres"]))

    # enumerated family (the cheap routes): every one misses the golden
    cheap = {
        "antibiogram all ages women": A.antibiogram(L, ages=(0, 120))[0],
        "antibiogram everyone": A.antibiogram(L, ages=(0, 120), sexes=("F", "M"))[0],
        "antibiogram E. coli only": A.antibiogram(L, ecoli_only=True)[0],
        "antibiogram every isolate": A.antibiogram(L, first_isolate=False)[0],
        "antibiogram any requester": A.antibiogram(L, practices_only=False)[0],
        "second-course route": A.second_course_rates(L, g["fc"]),
    }
    for name, ch in cheap.items():
        s2, _, r2 = _slate(L, ch, n)
        ok("cheap route misses: %s" % name, s2 != GOLD and not (GOLD & set(r2[:2])), "%s" % r2[:2])
    # the standing family (the cultures before any course, read any licensed way): every one lands the golden
    standing = {
        "same day only": A.chances(A.presentation(L, g["fc"], 0, 0)),
        "day before to day of": A.chances(A.presentation(L, g["fc"], -1, 0)),
        "two days either side": A.chances(A.presentation(L, g["fc"], -2, 2)),
        "weighted every culture by failure": A.weighted_all_cultures(L, g["fc"]),
    }
    for name, ch in standing.items():
        s2, st2, r2 = _slate(L, ch, n)
        ok("SF9 standing family lands the golden: %s" % name, s2 == GOLD, "%s" % r2[:3])
        ok("standing family keeps every graded nearest-10 figure: %s" % name,
           all(_r10(st2[k]) == _r10(st[k]) for k in st), "")
    win = [A.presentation(L, g["fc"], lo, hi) for lo, hi in ((0, 0), (-1, 1), (-2, 2), (-3, 2))]
    ok("SF4 C1 every window from the day of issue to two days either side selects the same cultures",
       len({tuple(sorted(s["lab"] for s in w)) for w in win}) == 1, "%s" % [len(w) for w in win])

    # --- the semantic fork table, asserted --------------------------------------------------------------------
    fc_rep = A.first_courses(L, include_repeat=True)
    ok("SF1 repeat issues counted as first courses: same call (no repeat issue to a woman aged 16 to 64)",
       len(fc_rep) == len(g["fc"]), "%d against %d" % (len(fc_rep), len(g["fc"])))
    for lb in (14, 21, 35, 42):
        fc2 = A.first_courses(L, lookback=lb)
        s2, _, _ = _slate(L, A.chances(A.presentation(L, fc2)), A.pool(fc2))
        ok("SF2 first-course lookback of %d days: same call" % lb, s2 == GOLD, "")
    by_drug = defaultdict(list)
    fcd = {(c["pid"], c["day"]): c["drug"] for c in g["fc"]}
    for s in g["pres"]:
        d0 = fcd.get((s["pid"], s["collected"]))
        if d0:
            by_drug[d0].append(s)
    cond = {d: sum(A.resistant(s, d) for s in by_drug[d]) / max(1, len(by_drug[d])) for d in A.DRUGS}
    s2, _, r2 = _slate(L, cond, n)
    ok("SF10 each chance read only on the first courses issued that antibacterial: same call and runner-up",
       s2 == GOLD and r2[2] == "Kesterby", "%s" % r2[:3])
    s2, _, _ = _slate(L, A.chances(A.presentation(L, g["fc"], pregnant=True)), n)
    ok("SF3 pregnancy-linked cultures added to the estimate: same call", s2 == GOLD)
    s2, _, _ = _slate(L, A.chances(g["pres"], per_isolate=True), n)
    ok("SF6 chance per isolate rather than per specimen: same call", s2 == GOLD)
    s2, _, _ = _slate(L, g["chances"], n, floor=True)
    ok("SF13 negative contributions floored at zero: same call", s2 == GOLD)
    s2, _, _ = _slate(L, A.chances(A.presentation(L, g["fc"], dedup_year=True)), n)
    ok("SF15 the estimate de-duplicated to a woman's first culture each year: same call", s2 == GOLD)
    s2, _, _ = _slate(L, A.chances(A.presentation(L, g["fc"], hub=False)), n)
    ok("SF8 hub courses' cultures left out of the estimate: same call", s2 == GOLD)
    issuer_pool = defaultdict(int)
    for c in g["fc"]:
        if c["day"].year == 2026:
            nn = A.network_of(L, c["issuer"]) or "hub"
            issuer_pool[(nn, c["drug"])] += 1
    s2, _, _ = _slate(L, g["chances"], issuer_pool)
    ok("SF7 courses counted to the issuing organisation (hub apart): same call", s2 == GOLD)
    dupes = Counter((s["pid"], s["collected"], tuple(sorted(o for o, _ in s["orgs"]))) for s in L["specs"])
    ok("SF18 a second pot from one consultation is in the export (realism) and never doubles a course's culture",
       sum(v > 1 for v in dupes.values()) > 50 and len({s["lab"] for s in g["pres"]}) == len(g["pres"]))
    any_i = sum(1 for s in L["specs"] for _, r in s["orgs"] if "I" in r.values())
    ok("SF5 no pathway antibacterial reports I (I appears only for ciprofloxacin and cefpodoxime)", any_i == 0,
       "%d" % any_i)

    # --- shock: the golden slate is not the top two of any single shipped statistic -----------------------------
    nets = L["order"]
    stats = {"courses on other antibacterials": {k: sum(n[(k, d)] for d in A.OFF) for k in nets},
             "all 2026 first courses": {k: sum(n[(k, d)] for d in A.DRUGS) for k in nets},
             "lowest nitrofurantoin share": {k: -n[(k, "NIT")] / sum(n[(k, d)] for d in A.DRUGS) for k in nets}}
    for d in A.OFF:
        stats["%s courses" % d] = {k: n[(k, d)] for k in nets}
        stats["%s share" % d] = {k: n[(k, d)] / sum(n[(k, dd)] for dd in A.DRUGS) for k in nets}
    for name, v in stats.items():
        top = set(sorted(v, key=lambda k: -v[k])[:2])
        ok("Shock: not the top two on %s" % name, top != GOLD, "%s" % sorted(top))

    # --- separation line, the ask devices --------------------------------------------------------------------
    main_rows = [s for s in L["specs"] if s["sex"] == "F" and 16 <= s["age"] <= 64]
    ask_rows = [s for s in L["specs"] if (s["sex"] == "F" and s["age"] >= 65) or (s["sex"] == "M" and s["age"] >= 16)]
    ok("separation: no specimen is in both the main call's population and the ask's",
       not ({s["lab"] for s in main_rows} & {s["lab"] for s in ask_rows}))
    scr = {s["lab"]: s for s in L["specs"]}
    L2 = dict(L)
    L2["specs"] = [dict(s, orgs=[("XXXX", r) for _, r in s["orgs"]]) for s in L["specs"]]
    g2 = A.golden(L2)
    ok("separation: the main call never reads the organism code (every code blanked, the same figures)",
       g2["stopped"] == g["stopped"])
    grid = g["grid"]
    crack = A.ask_grid(L, lambda c, lab: {"ENTC": "Enterococcus", "ENTE": "Enterococcus",
                                          "ECLO": "Enterobacter"}.get(c))
    for net in nets:
        for grp in A.GROUPS:
            ok("ask device moves %s %s" % (net, grp), grid.get((net, grp), 0) != crack.get((net, grp), 0),
               "%d against %d" % (grid.get((net, grp), 0), crack.get((net, grp), 0)))
    old_entc = [s for s in L["specs"] if s["lab"].startswith("H") and any(o == "ENTC" for o, _ in s["orgs"])]
    old_ente = [s for s in L["specs"] if s["lab"].startswith("H") and any(o == "ENTE" for o, _ in s["orgs"])]
    new_entc = [s for s in L["specs"] if not s["lab"].startswith("H") and any(o == "ENTC" for o, _ in s["orgs"])]
    amx = lambda ss, code: sum(r.get("AMX") == "R" for s in ss for o, r in s["orgs"] if o == code) / max(1, sum(
        1 for s in ss for o, _ in s["orgs"] if o == code))
    ok("fair: the old system's ENTC isolates are amoxicillin resistant (an Enterobacter's intrinsic AmpC) and its ENTE "
       "and the new ENTC isolates are not", amx(old_entc, "ENTC") > 0.95 and amx(old_ente, "ENTE") < 0.1 and
       amx(new_entc, "ENTC") < 0.1, "%.2f %.2f %.2f" % (amx(old_entc, "ENTC"), amx(old_ente, "ENTE"),
                                                       amx(new_entc, "ENTC")))
    ok("no per-row contradiction: the old system reports gentamicin and cefpodoxime for its ENTE and its ENTC alike",
       all(_has_gram_negative_panel(target, s["lab"]) for s in old_entc[:150]) and
       all(_panel_any(target, s["lab"]) for s in old_ente[:150]), "%d and %d" % (len(old_entc), len(old_ente)))
    ok("realism: no ECLO before the go-live and no ENTE after it",
       not any(o == "ECLO" for s in L["specs"] if s["lab"].startswith("H") for o, _ in s["orgs"]) and
       not any(o == "ENTE" for s in L["specs"] if not s["lab"].startswith("H") for o, _ in s["orgs"]))

    # --- realism sweep and input gates ---------------------------------------------------------------------------
    other = [sum(n[(k, d)] for d in A.OFF) for k in nets]
    ok("realism: no two networks with the same count of courses on other antibacterials", len(set(other)) == len(other))
    ok("realism: no round totals among the networks' pools", not any(v % 100 == 0 for v in other))
    files = sorted(os.listdir(target))
    ok("input gate: ten or more files", len(files) >= 10, "%d" % len(files))
    ok("input gate: three or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    big = max(sum(1 for _ in open(os.path.join(target, f))) - 1 for f in files if f.endswith(".csv"))
    ok("input gate: a file of 25,000 rows or more", big >= 25000, "%d" % big)
    ok("no describing file (readme, dictionary, notes, manifest, codebook, field guide)",
       not any(re.search(r"readme|dictionar|notes|manifest|codebook|field|schema|guide", f, re.I) for f in files))
    if meta_path:
        meta = json.load(open(meta_path))
        ok("metadata: two or more distractors, each a shipped file", len(meta["distractor_files"]) >= 2 and
           all(f in files for f in meta["distractor_files"]))
        ok("metadata: every shipped file has a source", set(files) <= {f for s in meta["sources"] for f in s["files"]})
    if fig_path and os.path.exists(fig_path):
        F = json.load(open(fig_path))
        ok("figures.json carries the slate and every network", F["slate"] == g["slate"] and len(F["networks"]) == 7)
    good = all(c for _, c, _ in RESULTS)
    for label, c, d in RESULTS:
        if not c:
            print("FAIL", label, d)
    print("checks: %d of %d pass" % (sum(c for _, c, _ in RESULTS), len(RESULTS)))
    return good


def _r10(v):
    q = abs(v) / 10.0
    r = int(q + 0.5) * 10
    return r if v >= 0 else -r


_PANEL = {}
_ANY = {}


def _panel_any(target, lab):
    if target not in _ANY:
        panel = _ANY[target] = {}
        with open(os.path.join(target, P.FILES["cultures"]), newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if r["OrganismCode"] == "ENTE":
                    panel.setdefault(r["LabNo"], []).append(bool(r["GENT"] or r["CPOD"]))
    return any(_ANY[target].get(lab, []))


def _has_gram_negative_panel(target, lab):
    if target not in _PANEL:
        panel = _PANEL[target] = {}
        with open(os.path.join(target, P.FILES["cultures"]), newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if r["OrganismCode"] == "ENTC":
                    panel.setdefault(r["LabNo"], []).append(bool(r["GENT"] or r["CPOD"]))
    return any(_PANEL[target].get(lab, []))
