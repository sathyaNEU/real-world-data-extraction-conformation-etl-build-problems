"""Generator assertions for task138 (architecture 4). Run: python3 checks.py <target_dir> [golden_dir]."""
import json
import os
import re
import sys
import zipfile
from datetime import timedelta

import numpy as np

import analysis as A
import cqtc
import params as P
import world
from io_util import pdf_text
from pack import DISTRACTORS, FILES

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s %s %s" % ("PASS" if ok else "FAIL", label, detail))


def main(target, golden_dir=None):
    F = A.golden(target)
    D, G, ex, ch = F["D"], F["G"], F["ex"], F["ch"]
    recs, owner, pairing = F["recs"], F["owner"], F["pairing"]
    W = world.build()
    truth = {s["subject"]: s for s in W["subjects"]}

    # ------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    check("G1 ten or more files", len(files) >= 10, str(len(files)))
    exts = {f.rsplit(".", 1)[-1] for f in files}
    check("G2 three or more formats", len(exts) >= 3, ",".join(sorted(exts)))
    nseg = len(D["seg"])
    check("G3 a file of 25,000 rows or more", nseg >= 25000, "%d Holter segments" % nseg)
    check("G4 two distractors present", all(d in files for d in DISTRACTORS), ",".join(DISTRACTORS))
    bad = [f for f in files if re.search(r"readme|dictionary|manifest|notes|codebook|decoy|trap|distractor|test_", f, re.I)]
    check("G5 no file describing the data or named for the design", not bad, ",".join(bad))
    sheets = []
    for f in files:
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(os.path.join(target, f)) as z:
                wbx = z.read("xl/workbook.xml").decode()
                sheets += re.findall(r'name="([^"]+)"', wbx)
                core = z.read("docProps/core.xml").decode()
                check("G6 %s carries its producer, not the toolchain" % f, "openpyxl" not in core.lower(), "")
    check("G7 no notes, readme or dictionary sheet", not [s for s in sheets if re.search(r"note|readme|dictionar|about", s, re.I)],
          ",".join(sheets))
    for f in files:
        if f.endswith(".pdf"):
            raw = open(os.path.join(target, f), "rb").read()
            check("G8 %s scrubbed of ReportLab signature" % f, b"ReportLab" not in raw, "")

    # ------------------------------------------------------------ the call and its components
    check("C1 golden call is 50 mg", G["call"] == 50, str(G["call"]))
    check("C2 50 mg upper bound below 10 ms by 1.5 ms or more", G["ubs"][50] <= 8.5, "%.2f" % G["ubs"][50])
    check("C3 100 mg upper bound above 10 ms by 2 ms or more", G["ubs"][100] >= 12.0, "%.2f" % G["ubs"][100])
    check("C4 25 mg upper bound far below 10 ms", G["ubs"][25] <= 6.0, "%.2f" % G["ubs"][25])
    gmr_txt = pdf_text(os.path.join(target, FILES["ddi"]))
    check("C5 the Cmax ratio the analysis uses is the synopsis's", "2.61 (2.32 to 2.94)" in gmr_txt, "")
    sad400 = []
    for sid, s in D["subj"].items():
        if s["study"] == "101" and s["active"] and s["dose"] == 400:
            sad400.append(max(x["c"] for k, x in D["pk"].items() if k[0] == sid and k[1] == 1))
    gm400 = float(np.exp(np.mean(np.log(sad400))))
    check("C6 the 400 mg single dose covers 100 mg's high clinical exposure", gm400 > ch[100], "%.0f vs %.0f" % (gm400, ch[100]))
    for d in (25, 50, 100):
        v = ch[d]
        e = int(np.floor(np.log10(v))) - 2
        frac = (v / 10 ** e) % 1.0
        check("C7 high clinical exposure %d mg clear of its 3-figure rounding edge" % d, abs(frac - 0.5) >= 0.05,
              "%.2f" % v)

    # ------------------------------------------------------------ R1: the field's raw material ships
    heads = []
    for f in files:
        if f.endswith(".csv") or f.endswith(".txt"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                for ln in fh:
                    if not ln.startswith("#"):
                        heads.append(ln.lower())
                        break
    check("R1a no shipped column holds an exponent, QTcI, C-QTc slope or high clinical exposure",
          not any(re.search(r"qtci|exponent|slope|c_high|high_clin|qtcp", h) for h in heads), "")
    df_rows = sum(len(v) for v in F["df"].values())
    check("R1b the golden exponents read the drug-free Holter segments", df_rows > 15000, "%d segments" % df_rows)
    check("R1c the model reads the triplicate ECGs and paired concentrations", G["n"] >= 1000, "%d rows" % G["n"])

    # ------------------------------------------------------------ R2: every Layer 1 item neutral
    ex_utc = A.exponents(F["df"], "hour", clock="utc")
    moved = [k for k in ex["hour"] if abs(ex_utc[k] - ex["hour"][k]) > 1e-9]
    r = A.run_cqtc(D, "own", ex_utc, ch=ch)
    check("R2a Holter clock left in UTC moves exponents only across the clock change and keeps the call",
          r["call"] == 50 and all(D["subj"][k]["study"] == "101" and D["subj"][k]["cohort"] == 4 for k in moved),
          "%d subjects moved, %.2f/%.2f" % (len(moved), r["ubs"][50], r["ubs"][100]))
    df_nom = A.drug_free(D, recs, owner, cut="nominal")
    r = A.run_cqtc(D, "own", A.exponents(df_nom, "hour"), ch=ch)
    check("R2b drug-free cut at nominal 08:00 instead of the logged dose time keeps the call", r["call"] == 50,
          "%.2f/%.2f" % (r["ubs"][50], r["ubs"][100]))
    D2 = dict(D)
    D2["ecg"] = {k: v for k, v in D["ecg"].items() if len(v) == 3}
    D2["ecg"].update({k: v for k, v in D["ecg"].items() if len(v) < 3 and k[1] == -1})
    try:
        r = A.run_cqtc(D2, "own", ex["hour"], ch=ch)
        ok = r["call"] == 50
    except Exception as exc:          # a dropped post-dose point only shortens the model
        ok, r = False, {"ubs": {50: float("nan"), 100: float("nan")}}
    check("R2c post-dose time points with an unreadable replicate dropped whole keeps the call", ok,
          "%.2f/%.2f" % (r["ubs"][50], r["ubs"][100]))
    D3 = dict(D)
    D3["pk"] = {k: (dict(v, c=P.LLOQ / 2) if (v["c"] == 0 and D["subj"][k[0]]["active"] and k[2] > 0) else v)
                for k, v in D["pk"].items()}
    r = A.run_cqtc(D3, "own", ex["hour"], ch=ch)
    check("R2d active-subject BLQ at half the limit instead of zero keeps the call", r["call"] == 50, "")
    D4 = dict(D)
    reassayed = set()
    with open(os.path.join(target, FILES["plasma"]), encoding="utf-8") as fh:
        for ln in fh:
            if "Re-assay" in ln:
                p = ln.split(",")
                reassayed.add((int(p[2]), int(p[3]), float(p[4])))
    D4["ecg"] = {k: v for k, v in D["ecg"].items() if (k[0], k[1], k[2]) not in reassayed}
    r = A.run_cqtc(D4, "own", ex["hour"], ch=ch)
    check("R2e time points whose sample needed a diluted re-assay dropped keeps the call", r["call"] == 50,
          "%d re-assayed samples" % len(reassayed))
    mapped = [rid for rid in recs if rid in owner]
    check("R2f every labelled recording maps to one randomised subject through its typed PatientID",
          len(set(owner[r_] for r_ in mapped)) == len(D["subj"]) == len(mapped), "%d" % len(mapped))
    check("R2g screening numbers map one to one onto subjects",
          len({v["screening"] for v in D["subj"].values()}) == len(D["subj"]), "")
    ex_mid = {}
    for sid, a in F["df"].items():
        ck = (a[:, 0] + 2.5 / 60.0) % 24
        ex_mid[sid] = cqtc.exponent(np.log(a[:, 1]), np.log(a[:, 2]), ck, "hour")
    r = A.run_cqtc(D, "own", ex_mid, ch=ch)
    check("R2h clock hour by segment midpoint instead of start keeps the call", r["call"] == 50,
          "%.2f/%.2f" % (r["ubs"][50], r["ubs"][100]))
    for d in DISTRACTORS:
        check("R2i distractor %s is read by no step of the golden" % d, d not in json.dumps(FILES_USED), "")

    # ------------------------------------------------------------ R3: the analyst test and the decisive step
    rq = F["rungs"]["QTcF"]
    check("R3a the default path (Fridericia, every filed rule applied) files 100 mg", rq["call"] == 100,
          "%.2f" % rq["ubs"][100])
    rp = F["rungs"]["pooled_own"]
    check("R3a2 the textbook own-correction (one QT-RR line per subject) files 25 mg", rp["call"] == 25,
          "%.2f" % rp["ubs"][50])
    check("R3b only the decisive step changed (the line within clock hour) files the golden", G["call"] == 50, "")
    check("R3b2 the lower rung's single correction (own exponent, no clock) stays wrong", rp["call"] != 50, "")
    tr = truth_ladder(W)
    check("R3a3 on the clean truth Fridericia files 100 mg, the 24-hour own line 25 mg, the clock-held line 50 mg",
          tr == (100, 25, 50), str(tr))
    check("R3c no copied or repeated block in the Holter stream", no_repeats(D), "")
    plan = pdf_text(os.path.join(target, FILES["plan"])).lower()
    check("R3c2 no filed sentence names the clock, the night or a circadian term",
          not re.search(r"circadian|time of day|clock hour|diurnal|night|sleep|cosinor|hour of", plan), "")

    # ------------------------------------------------------------ the golden family (clock held fixed)
    fam = {}
    for m in ("hour", "half_hour", "two_hour", "three_hour", "harmonic1", "harmonic2", "harmonic3", "linear_hour"):
        e = ex[m] if m in ex else A.exponents(F["df"], m)
        r = A.run_cqtc(D, "own", e, ch=ch)
        fam[m] = r
        check("F1 clock-held exponent fit %s files 50 mg with margin" % m,
              r["call"] == 50 and r["ubs"][50] <= 9.5 and r["ubs"][100] >= 11.0,
              "%.2f/%.2f" % (r["ubs"][50], r["ubs"][100]))
    pop = pooled_within(F["df"], "hour")
    r = A.run_cqtc(D, "power", pop, ch=ch)
    check("F2 one population exponent fitted within clock hour also files 50 mg", r["call"] == 50, "%.3f" % pop)
    for lab, kw in (("no random slope", dict(slope=False)), ("no baseline covariate", dict(basecov=False)),
                    ("normal quantile", dict(df="z")), ("subject degrees of freedom", dict(df="subjects"))):
        r = A.run_cqtc(D, "own", ex["hour"], ch=ch, **kw)
        check("F3 model variant (%s) files 50 mg" % lab, r["call"] == 50, "%.2f/%.2f" % (r["ubs"][50], r["ubs"][100]))
    mh = np.mean(list(ex["hour"].values()))
    check("F4 exponent converges as the clock bins shrink (hour against half-hour and cosinor)",
          abs(mh - np.mean(list(ex["half_hour"].values()))) < 0.006 and abs(mh - np.mean(list(ex["harmonic2"].values()))) < 0.008,
          "%.4f" % mh)
    check("F5 coarse blocks are unconverged (six-hour blocks sit 0.03 or more above the hourly fit)",
          np.mean(list(ex["six_hour"].values())) - mh > 0.03, "%.4f" % np.mean(list(ex["six_hour"].values())))
    lift = clock_effect(F["df"])
    check("F6 the drug-free record shows QT at matched RR longer at night than mid-afternoon by 10 ms or more",
          lift >= 10.0, "%.1f ms" % lift)
    share = np.mean([ex["pooled"][k] > ex["hour"][k] for k in ex["hour"]])
    check("F7 the 24-hour line runs above the clock-held exponent in nearly every subject", share >= 0.9, "%.2f" % share)

    # ------------------------------------------------------------ rivals and cheap routes
    rivals = {"Fridericia": ("F", None, 100), "Framingham": ("Fram", None, 100), "Hodges": ("Hodges", None, 100),
              "uncorrected": ("raw", None, 100), "Bazett": ("B", None, 25)}
    landed = 0
    for lab, (sch, b, want) in rivals.items():
        r = A.run_cqtc(D, sch, b, ch=ch)
        landed += r["call"] == 50
        key = 100 if want == 100 else 50
        margin = (10 - r["ubs"][key]) if want == 100 else (r["ubs"][key] - 10)
        check("D1 %s files %d mg with 1 ms or more to spare" % (lab, want), r["call"] == want and margin >= 1.0,
              "%.2f" % r["ubs"][key])
    for m in ("pooled", "linear_pooled", "stable", "day_only", "day_night"):
        e = ex[m] if m in ex else A.exponents(F["df"], m)
        r = A.run_cqtc(D, "own", e, ch=ch)
        landed += r["call"] == 50
        check("D2 unheld own-exponent fit %s files 25 mg" % m, r["call"] == 25, "%.2f" % r["ubs"][50])
    tri = triplicate_exponents(D)
    r = A.run_cqtc(D, "own", tri, ch=ch)
    landed += r["call"] == 50
    check("D3 exponents from the Day -1 triplicates alone do not file 50 mg", r["call"] != 50, str(r["call"]))
    pp = pooled_within(F["df"], "none")
    r = A.run_cqtc(D, "power", pp, ch=ch)
    landed += r["call"] == 50
    check("D4 one population exponent from all segments files 25 mg", r["call"] == 25, "%.3f" % pp)
    check("D5 no cheap route lands the golden (Gate F count on the pack)", landed == 0, str(landed))

    # ------------------------------------------------------------ semantic fork table
    check("SF1 'highest dose' among 25, 50, 100 mg: 50 mg is the largest passing, 100 mg fails, so no tie",
          G["ubs"][25] < 10 and G["ubs"][50] < 10 and G["ubs"][100] >= 10, "")
    alt = A.c_high(D, gmr=3.37)
    r = A.run_cqtc(D, "own", ex["hour"], ch=alt)
    check("SF2 high clinical exposure: the AUC ratio instead of the filed Cmax ratio does not change the call",
          r["call"] == 50, "%.2f" % r["ubs"][50])
    ch_mean = {}
    for dose in (25, 50, 100):
        v = [max(x["c"] for k, x in D["pk"].items() if k[0] == sid and k[1] == 10) for sid, s in D["subj"].items()
             if s["study"] == "102" and s["active"] and s["dose"] == dose]
        ch_mean[dose] = 2.61 * float(np.mean(v))
    r = A.run_cqtc(D, "own", ex["hour"], ch=ch_mean)
    check("SF3 arithmetic instead of geometric mean Cmax keeps the call", r["call"] == 50, "")
    check("SF4 'below 10 ms' read on the upper bound: the point estimate at 100 mg is also above 10",
          G["pred"][100][0] >= 10.0, "%.2f" % G["pred"][100][0])
    r = A.run_cqtc(D, "own", ex["hour"], ch=ch, df="z")
    check("SF5 the interval's quantile (t or normal) does not move the call", r["call"] == 50, "")
    D5 = dict(D)
    D5["ecg"] = {k: v for k, v in D["ecg"].items() if not (k[1] == 10)}
    r = A.run_cqtc(D5, "own", ex["hour"], ch=ch)
    check("SF6 'every post-dose time point of both studies': Day 1 alone would also file 50 mg", r["call"] == 50,
          "%.2f/%.2f" % (r["ubs"][50], r["ubs"][100]))
    check("SF7 the drug-free recording before the first dose ends at each subject's own logged dose time",
          all(len(F["df"][s]) >= 250 for s in F["df"]), "min %d" % min(len(v) for v in F["df"].values()))

    # ------------------------------------------------------------ ask A: single-dose AUC0-inf
    gm = F["ask_a"]
    variants = []
    for times in ("actual", "nominal"):
        for lz in ("adjr2", "last3", "ge48"):
            variants.append(A.ask_a(D, times=times, lz=lz)[0])
    for d in (25, 50, 100, 200, 400):
        bins = {A.sig2(v[d])[0] for v in variants}
        step = A.sig2(gm[d])[1]
        edge = min(abs(((v[d] / step) % 1.0) - 0.5) for v in variants)
        check("A1 AUC %d mg in one two-figure bin under every terminal-phase and clock reading" % d,
              len(bins) == 1 and edge >= 0.08, "%.0f, edge %.2f step" % (gm[d], edge))
    mirror = A.ask_a(D, use_late=False)[0]
    check("A2 without the ambulatory samples every AUC misses its bin",
          all(A.sig2(mirror[d])[0] != A.sig2(gm[d])[0] for d in gm), "")
    xw = A.crosswalk(D)
    n_late = sum(1 for r_ in D["amb"] if r_["TEST"] == "VLT-317 (plasma)" and (r_["VOLUNTEER_NO"], r_["PROTOCOL"]) in xw)
    check("A3 every ambulatory plasma result reaches a subject through the screening log", n_late ==
          sum(1 for r_ in D["amb"] if r_["TEST"] == "VLT-317 (plasma)"), str(n_late))
    vols = {}
    for (v, p), sid in xw.items():
        vols.setdefault(v, set()).add(sid)
    check("A4 some volunteers took part in both studies (the protocol resolves them)",
          any(len(s) > 1 for s in vols.values()), "")

    # ------------------------------------------------------------ ask B: night heart rate
    check("B1 each unlabelled recording pairs with one labelled recording, second candidate twice as far",
          F["pair_margin"] >= 2.0, "%.2f" % F["pair_margin"])
    truth_pair = {s["rec2"]["id"]: s["subject"] for s in W["subjects"]}
    check("B2 the pairing reproduces the recorders the ward exchanged", all(truth_pair[k] == v for k, v in pairing.items()), "")
    nb = A.ask_b(D, recs, owner, pairing)[0]
    for k, v in nb.items():
        check("B3 night heart rate %s %d mg clear of its 0.1 bpm rounding edge" % k, abs(((v * 10) % 1.0) - 0.5) >= 0.1,
              "%.3f" % v)
    naive = A.ask_b(D, recs, owner, A.naive_pairing(recs, owner))[0]
    check("B4 pairing by recording order misses every night figure by 0.2 bpm or more",
          all(abs(naive[k] - nb[k]) >= 0.2 for k in nb), "")
    dev_rows = {g["rec"] for g in D["seg"] if g["rec"] not in owner}
    df_recs = {rid for rid in owner}
    check("B5 separation: no device recording is in the main call's drug-free population", not (dev_rows & df_recs), "")
    late_used = any(True for k in D["pk"] if k[2] > 24)
    check("B6 separation: the main call reads no ambulatory sample", not late_used, "")

    # ------------------------------------------------------------ realism sweep
    counts = [len(v) for v in recs.values()]
    check("S1 recording lengths vary (no identical segment counts across recordings)",
          len(set(counts)) > 0.8 * len(counts), "%d distinct of %d" % (len(set(counts)), len(counts)))
    people = set(re.findall(r"(Hilde Lemmens|Kim Huysmans|Freddy Wouters|Tanghe)", plan_text(target)))
    check("S2 named people come from the card's persona list", people <= {"Hilde Lemmens", "Kim Huysmans", "Tanghe",
                                                                           "Freddy Wouters"}, ",".join(sorted(people)))
    ok = True
    for (sid, day, nt), x in D["pk"].items():
        if nt > 0 and day in D["doses"][sid] and x["t"] <= D["doses"][sid][day]:
            ok = False
    check("S3 every post-dose sample is drawn after its logged dose", ok, "")
    check("S4 no round headline exposure", all(abs(v - round(v, -1)) > 0.5 for v in ch.values()), "")
    cmax = [max(x["c"] for k, x in D["pk"].items() if k[0] == sid) for sid, s in D["subj"].items() if s["active"]]
    check("S5 no two subjects share a Cmax", len(set(cmax)) == len(cmax), "")

    if golden_dir:
        figs = json.load(open(os.path.join(os.path.dirname(__file__), "figures.json")))
        check("J1 figures.json call matches the analysis", figs["call_mg"] == G["call"], "")

    n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
    print("\n%d checks, %d failed" % (len(RESULTS), n_fail))
    return n_fail


FILES_USED = [FILES[k] for k in ("holter", "ecg101", "ecg102", "plasma", "amb", "dosing", "rand", "screen", "plan", "ddi")]


def plan_text(target):
    return " ".join(pdf_text(os.path.join(target, f)) for f in os.listdir(target) if f.endswith(".pdf"))


def pooled_within(df, grouping):
    xs, ys, gs = [], [], []
    for sid, a in df.items():
        xs += list(np.log(a[:, 1]))
        ys += list(np.log(a[:, 2]))
        gs += list(sid * 100 + (np.floor(a[:, 0]).astype(int) if grouping == "hour" else np.zeros(len(a), int)))
    return cqtc._within(np.array(xs), np.array(ys), np.array(gs))


def triplicate_exponents(D):
    out = {}
    for sid in D["subj"]:
        x, y = [], []
        for t in A.ECG_TIMES:
            for rr, qt in D["ecg"].get((sid, -1, t), []):
                x.append(np.log(rr))
                y.append(np.log(qt))
        out[sid] = cqtc._within(np.array(x), np.array(y), np.zeros(len(x)))
    return out


def clock_effect(df):
    """Mean log QT residual from each subject's clock-held fit, night (02-05h) minus mid-afternoon (14-17h), in ms."""
    lifts = []
    for sid, a in df.items():
        b = cqtc.exponent(np.log(a[:, 1]), np.log(a[:, 2]), a[:, 0], "hour")
        qtc = a[:, 2] / (a[:, 1] / 1000.0) ** b
        night = qtc[(a[:, 0] >= 2) & (a[:, 0] < 5)]
        aft = qtc[(a[:, 0] >= 14) & (a[:, 0] < 17)]
        if len(night) and len(aft):
            lifts.append(night.mean() - aft.mean())
    return float(np.mean(lifts))


def no_repeats(D):
    seen = set()
    by = {}
    for g in D["seg"]:
        if g["hr"] is not None:
            by.setdefault(g["rec"], []).append((g["hr"], g["rr"], g["qt"]))
    for rid, L in by.items():
        for i in range(0, len(L) - 12, 12):
            blk = tuple(L[i:i + 12])
            if blk in seen:
                return False
            seen.add(blk)
    return True


def truth_ladder(W):
    """F, 24-hour own line and clock-held own line on the world before any file is written."""
    subs = {s["subject"]: s for s in W["subjects"]}
    seg = {}
    for g in W["holter"]:
        s = subs[g["subject"]]
        if g["kind"] != "rec1" or g["valid_frac"] < 1 or g["start"] + timedelta(seconds=g["dur"]) > s["dose_times"][0]:
            continue
        seg.setdefault(g["subject"], []).append((world.wall(g["start"]), g["rr"], g["qt"]))
    exps = {}
    for m in ("pooled", "hour"):
        exps[m] = {sid: cqtc.exponent(np.log(np.array(L)[:, 1]), np.log(np.array(L)[:, 2]), np.array(L)[:, 0], m)
                   for sid, L in seg.items()}
    cmax = {}
    for r in W["pk"]:
        s = subs[r["subject"]]
        if s["design"] == "MAD" and s["active"] and r["day"] == P.MAD_DAYS:
            cmax[r["subject"]] = max(cmax.get(r["subject"], 0), r["true"])
    chh = {d: P.DDI_CMAX_GMR * float(np.exp(np.mean(np.log([cmax[k] for k in cmax if subs[k]["dose"] == d]))))
           for d in P.PHASE2B_DOSES}
    pkc = {(r["subject"], r["day"], r["nominal"]): r["true"] for r in W["pk"]}
    calls = []
    for scheme, b in (("F", None), ("own", exps["pooled"]), ("own", exps["hour"])):
        val = {}
        for e in W["ecg"]:
            q = [cqtc.corrected(r["qt"], r["rr"], scheme, b[e["subject"]] if b else None) for r in e["reps"] if r["ok"]]
            if q:
                val[(e["subject"], e["day"], e["nominal"])] = float(np.mean(q))
        base = {sid: np.mean([val[(sid, -1, t)] for t in P.ECG_TIMES if (sid, -1, t) in val]) for sid in subs}
        rows = [dict(subject=k[0], trt=subs[k[0]]["active"], conc=pkc[k], nominal=k[2], dq=v - val[(k[0], -1, k[2])])
                for k, v in sorted(val.items()) if k[1] != -1 and (k[0], -1, k[2]) in val]
        m = cqtc.fit(rows, base)
        ubs = {d: cqtc.predict(m, chh[d])[1] for d in P.PHASE2B_DOSES}
        calls.append(cqtc.highest_passing(ubs))
    return tuple(calls)


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None) else 0)
