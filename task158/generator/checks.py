"""task158 checks: every design claim asserted on the built pack (task158/target) and the goldens.

    python3 task158/generator/checks.py [target_dir]

Blocks: input gates; the three rules (R1 raw material, R2 mess neutral item by item, R3a analyst test, R3b the
decisive step alone, R3c no plant); the ladder and its margins; the semantic fork rows SF1 to SF14; the out-of-sample
check on the early-access tenant; Ask A and Ask B with every stop; the separation line; the realism sweep; the
distractor deletions; the figures, golden and write-up agreeing; the container scrub."""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402
import common as K          # noqa: E402
import docs as DOC          # noqa: E402
import metadata as MD       # noqa: E402
import records as R         # noqa: E402

TASK = os.path.dirname(HERE)
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %-74s %s" % ("PASS" if ok else "FAIL", label, detail))


def bin_margin(x, step):
    c = np.floor(x / step + 0.5) * step
    return step / 2.0 - abs(x - c)


def main(target):
    files = sorted(os.listdir(target))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))

    # ------------------------------------------------------------------ input gates
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    check("G2 three or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    big = max((MD.rows_of(os.path.join(target, f)) or 0, f) for f in files)
    check("G3 one file of 25,000 rows or more", big[0] >= 25000, "%s %d rows" % (big[1], big[0]))
    dis = meta["distractor_files"]
    check("G4 two or more distractors, declared and shipped", len(dis) >= 2 and all(d in files for d in dis),
          ", ".join(dis))
    check("G5 no distractor named as one", not any("distract" in f.lower() for f in files))
    check("G6 metadata lists every shipped file with source, date, licence",
          sorted(x["path"] for x in meta["files"]) == files and all(x["source"] and x["date"] and x["license"]
                                                                    for x in meta["files"]))

    # ------------------------------------------------------------------ the main call
    M = C.main_call(target)
    sf = M["sf"]
    gold = M["docs_peak"]
    check("M1 the stopgap goes to docs-prod", M["pick"] == "docs-prod", M["pick"])
    check("M2 docs-prod's Q1 peak-week shortfall rounds to 340", K.nearest(gold, 10) == 340, "%.2f" % gold)
    check("M3 the golden sits at least a quarter of a bin from either edge", bin_margin(gold, 10) >= 2.5,
          "margin %.2f" % bin_margin(gold, 10))
    check("M4 docs-prod's peak week is 2027-W13", M["docs_week"] == 13)
    check("M5 lc2's rates recovered from batch-prod's lc2 hours",
          abs(M["a"] / K.A_LC2 - 1) < 0.002 and abs(M["b"] / K.B_LC2 - 1) < 0.002, "%.7f %.6f" % (M["a"], M["b"]))
    check("M6 Docs leads Code by more than a tenth", gold > 1.1 * sf["code-prod"]["peak"],
          "%.1f against %.1f" % (gold, sf["code-prod"]["peak"]))
    others = sorted((sf[p]["peak"], p) for p in K.POOLS if p != "docs-prod")
    check("M7 no other pool within 30 GPUs of the golden", gold - others[-1][0] >= 30, "%s %.1f" % (others[-1][1],
                                                                                                    others[-1][0]))

    # ------------------------------------------------------------------ the ladder
    RG = C.rungs(M, target)
    code = sf["code-prod"]["peak"]
    under = [k for k in RG if k.startswith(("R0", "R1", "R2", "R3"))]
    over = [k for k in RG if k.startswith("R5")]
    check("L1 the default (R0) files Code at 300", RG["R0 Docs GPU-seconds per request"]["pick"] == "code-prod"
          and K.nearest(code, 10) == 300, "Code %.2f" % code)
    check("L2 every rung below the decisive one files Code, Docs at least 25 GPUs behind",
          all(RG[k]["pick"] == "code-prod" and code - RG[k]["docs"] >= 25 for k in under),
          "; ".join("%s %.0f" % (k.split()[0], RG[k]["docs"]) for k in under))
    check("L3 R4 alone files the golden", RG["R4 computed prompt and completion tokens at lc2's rates"]["pick"] ==
          "docs-prod" and abs(RG["R4 computed prompt and completion tokens at lc2's rates"]["docs"] - gold) < 1e-6)
    check("L4 every rung above the decisive one files Docs at least a bin away from 340",
          all(RG[k]["pick"] == "docs-prod" and K.nearest(RG[k]["docs"], 10) != 340 and RG[k]["docs"] - gold >= 10
              for k in over), "; ".join("%s %.0f" % (k.split()[0], RG[k]["docs"]) for k in over))
    r0rank = RG["R0 Docs GPU-seconds per request"]["ranks"].index("docs-prod") + 1
    check("L5 the default ranks Docs third or lower", r0rank >= 3, "rank %d" % r0rank)
    check("L6 the decisive move is the largest single move on the ladder",
          max(RG[k]["docs"] for k in under) < gold - 60, "nearest under-rung %.0f" % max(RG[k]["docs"] for k in under))

    # ------------------------------------------------------------------ the out-of-sample check
    P = C.pilot(M, target)
    rr = P["ratio"]
    check("O1 lc2's rates predict the tenant's excess within 3 per cent",
          abs(rr["computed prompt and completion at lc2's rates"] - 1) < 0.03,
          "%.3f" % rr["computed prompt and completion at lc2's rates"])
    check("O2 Docs' rate per request predicts about a fifth", 0.15 < rr["Docs GPU-seconds per request"] < 0.27,
          "%.3f" % rr["Docs GPU-seconds per request"])
    check("O3 a pack shared across a report's calls predicts under half", rr["the pack computed once a report"] < 0.5,
          "%.3f" % rr["the pack computed once a report"])
    a_own, b_own = P["own_fit"]
    check("O4 a two-rate fit on the tenant's own days is ill-conditioned (no answer key)",
          abs(a_own / K.A_LC2 - 1) > 0.5 or abs(b_own / K.B_LC2 - 1) > 0.5, "%.6f %.5f corr %.5f" %
          (a_own, b_own, P["corr_daily_tokens"]))
    check("O5 the tenant's calls are each their own session in billing",
          all(x["requests"] == x["sessions"] for x in C.read_billing(target) if x["channel"] == "report"))

    # ------------------------------------------------------------------ determinism variants of the golden
    intake, plan, live = M["intake"], M["plan"], M["live"]
    R_ = M["R"]

    def golden_with(a, b, gpr_docs=None, live_=None):
        cost = lambda c: c["calls"] * (a * c["pmax"] + b * c["qmax"])
        g = dict(M["gpr_exact"])
        if gpr_docs:
            g["docs-prod"] = gpr_docs
        s, pick = C.shortfalls(intake, plan, g, live_ or live, cost)
        return s["docs-prod"]["peak"], pick
    variants = {}
    a1, b1, _ = C.fit_two_rates(R_, intercept=True)
    variants["intercept"] = golden_with(a1, b1)
    for nm, (s, e) in {"Jun-Nov": (dt.datetime(2026, 6, 1), dt.datetime(2026, 12, 1)),
                       "Sep-Nov": (dt.datetime(2026, 9, 1), dt.datetime(2026, 12, 1)),
                       "Q3": (dt.datetime(2026, 7, 1), dt.datetime(2026, 10, 1))}.items():
        aa, bb, _ = C.fit_two_rates(R_, start=s, end=e)
        variants["window " + nm] = golden_with(aa, bb)
    d = R_["batch-prod"]
    m = np.array(["lc2" in x for x in d["model"]])
    X = np.c_[d["prompt_tokens"][m], d["completion_tokens"][m]].astype(float)
    y = d["gpu_busy_s"][m].astype(float)
    w = 1.0 / y
    cw = np.linalg.lstsq(X * w[:, None] ** 0.5, y * w ** 0.5, rcond=None)[0]
    variants["WLS"] = golden_with(cw[0], cw[1])
    ci = np.linalg.lstsq(X, y, rcond=None)[0]
    variants["rollout hours in"] = golden_with(ci[0], ci[1])
    days = sorted({t.date() for t, k in zip(d["t"], m) if k})
    di = {dd: i for i, dd in enumerate(days)}
    Xd = np.zeros((len(days), 2))
    yd = np.zeros(len(days))
    for t, k, p_, q_, b_ in zip(d["t"], m, d["prompt_tokens"], d["completion_tokens"], d["gpu_busy_s"]):
        if k:
            Xd[di[t.date()]] += (p_, q_)
            yd[di[t.date()]] += b_
    cd = np.linalg.lstsq(Xd, yd, rcond=None)[0]
    variants["daily fit"] = golden_with(cd[0], cd[1])
    variants["close-out gpr 1.630"] = golden_with(M["a"], M["b"], gpr_docs=M["gpr"]["docs-prod"])
    dd_ = R_["docs-prod"]
    on = np.array([dt.datetime(2026, 10, 5) <= t < dt.datetime(2026, 12, 1) for t in dd_["t"]])
    g_on = dd_["gpu_busy_s"][on].sum() / dd_["requests"][on].sum()
    variants["Oct-Nov gpr with the tenant"] = golden_with(M["a"], M["b"], gpr_docs=g_on)
    ea = dict(ref="EA", tier="RS-6", peak=150, golive=dt.date(2026, 10, 5), calls=6, pmax=24000, qmax=1600)
    variants["early-access agreement counted"] = golden_with(M["a"], M["b"], live_=live + [ea])
    variants["tenant and agreement both"] = golden_with(M["a"], M["b"], gpr_docs=g_on, live_=live + [ea])
    worst = min(bin_margin(v[0], 10) for v in variants.values())
    check("D1 every defensible construction files docs-prod at 340",
          all(v[1] == "docs-prod" and K.nearest(v[0], 10) == 340 for v in variants.values()),
          "; ".join("%s %.2f" % (k, v[0]) for k, v in variants.items()))
    singles = [k for k in variants if k != "tenant and agreement both"]
    check("D2 every single variant keeps a quarter bin of margin", min(bin_margin(variants[k][0], 10) for k in singles)
          >= 2.5, "worst %.2f" % min(bin_margin(variants[k][0], 10) for k in singles))
    check("D3 the combined variant keeps at least one GPU of margin", worst >= 1.0, "worst %.2f" % worst)
    # one sigma on the rates: the fit's standard errors move nothing
    resid = y - X @ ci
    cov = np.linalg.inv(X.T @ X) * (resid @ resid) / (len(y) - 2)
    se = np.sqrt(np.diag(cov))
    lo_ = golden_with(M["a"] - se[0], M["b"] - se[1])[0]
    hi_ = golden_with(M["a"] + se[0], M["b"] + se[1])[0]
    check("D4 one standard error on both rates leaves the bin", K.nearest(lo_, 10) == K.nearest(hi_, 10) == 340,
          "%.2f to %.2f" % (lo_, hi_))

    # ------------------------------------------------------------------ semantic fork rows
    check("SF1 one pool per product, six pools", sorted(intake) == sorted(K.POOLS) == sorted(plan))
    check("SF2 the policy assigns the cluster whole", "It is not split between pools" in " ".join(DOC.POLICY[0][1]))
    alt = {}
    for p in K.POOLS:
        wk = sf[p]["weekly"]
        req = [wk[i] + plan[p][i] for i in range(13)]
        alt[p] = wk[int(np.argmax(req))]
    check("SF3 largest weekly shortfall and shortfall in the peak-requirement week agree",
          abs(alt["docs-prod"] - gold) < 1e-6 and abs(alt["code-prod"] - code) < 1e-6)
    check("SF4 the intake's figures are busiest-hour figures", all("Busiest-hour" in M["unit"][p] for p in K.POOLS))
    check("SF5 busy is the rollup's gpu_busy_s, carried at 2,520", K.CARRY == 2520.0 and
          "as the fleet rollup counts them, divided by 2,520" in " ".join(DOC.POLICY[1][1]))
    spread = C.shortfalls(intake, plan, M["gpr_exact"], [dict(c, peak=c["peak"] * 0.0) for c in live], M["cost"])[0]
    q1_avg = {}
    rows = M["rows"]
    for c in live:
        r = [x for x in rows if x["Contract"] == c["ref"]][0]
        q1_avg[c["ref"]] = r["Q1 committed reports"] / (13 * 7 * 24.0)
    spread_live = [dict(c, peak=q1_avg[c["ref"]]) for c in live]
    sp = C.shortfalls(intake, plan, M["gpr_exact"], spread_live, M["cost"])[0]
    check("SF6 Q1 committed reports spread over the quarter's hours file Code (the policy holds contracted peaks)",
          max(K.POOLS, key=lambda p: sp[p]["peak"]) == "code-prod", "Docs %.1f" % sp["docs-prod"]["peak"])
    check("SF7 the early-access agreement counted leaves the bin", K.nearest(
        variants["early-access agreement counted"][0], 10) == 340)
    op = C.shortfalls(intake, plan, M["gpr_exact"], live, M["cost"],
                      alloc_override={p: [plan[p][0]] * 13 for p in K.POOLS})[0]
    check("SF8 the opening allocation all quarter files another bin (the week's allocation is filed)",
          K.nearest(op["docs-prod"]["peak"], 10) != 340, "%.1f" % op["docs-prod"]["peak"])
    check("SF9 every go-live is a Monday inside or before Q1", all(c["golive"].weekday() == 0 for c in live))
    check("SF10 the stopgap's GPUs are the fleet's part", "H100 SXM5 80GB" in " ".join(DOC.POLICY[0][1]))
    weekly_round = max(round(x / 10) * 10 for x in sf["docs-prod"]["weekly"])
    check("SF11 rounding once or per week gives the same figure", weekly_round == 340)
    check("SF12 October-November's pool rate with the tenant left in leaves the bin",
          K.nearest(variants["Oct-Nov gpr with the tenant"][0], 10) == 340)
    pa, pb = C.fit_pooled_models(R_)
    pooled = golden_with(pa, pb)[0]
    check("SF13 pooling lc1 and lc2 hours files another bin (ruled out by the model tag)",
          K.nearest(pooled, 10) != 340, "%.1f" % pooled)
    check("SF14 report calls count on docs-prod", "on the pool of the product that sold it" in " ".join(DOC.POLICY[2][1]))

    # ------------------------------------------------------------------ the three rules
    cols = set()
    for f in files:
        if f.endswith(".csv"):
            cols |= set(next(csv.reader(open(os.path.join(target, f), encoding="utf-8"))))
    check("R1a the field's raw material ships: hourly busy time against prompt and completion tokens",
          {"gpu_busy_s", "prompt_tokens", "completion_tokens", "sessions_new", "model"} <= cols)
    check("R1b no shipped column carries cached, computed or prefill tokens",
          not any(re.search(r"tok", c, re.I) and re.search(r"cach|comput|prefill|reuse|hit", c, re.I) for c in cols)
          and not any(re.search(r"prefill|cached|computed|reuse", c, re.I) for c in cols),
          ", ".join(c for c in sorted(cols) if "tok" in c))
    text = " ".join(open(os.path.join(target, f), encoding="utf-8", errors="ignore").read()
                    for f in files if f.endswith((".md", ".log")))
    docs_text = text + " " + " ".join(p for _, ps in DOC.POLICY for p in ps) + " " + \
        " ".join(p for _, ps in DOC.SCHEDULE for p in ps) + " " + " ".join(p for _, ps in DOC.LEASE for p in ps)
    check("R1c no shipped sentence names reuse, prefix caching or how a call's GPU work is priced",
          not re.search(r"prefix|cache|cached|reuse|re-use|per token|per request|GPU-seconds per", docs_text, re.I))
    # R2: each Layer 1 item mishandled leaves the call and the critical components
    ci2 = np.linalg.lstsq(X, y, rcond=None)[0]
    g_roll = golden_with(ci2[0], ci2[1])
    check("R2a the rollout's two-build tag mishandled (its hours kept) moves nothing",
          g_roll[1] == "docs-prod" and K.nearest(g_roll[0], 10) == 340, "%.2f" % g_roll[0])
    utc_ratio = C.pilot_ratio(M, target, utc_days=True)
    check("R2b UTC days for billing's Amsterdam days still separate the costings", abs(utc_ratio[0] - 1) < 0.05 and
          utc_ratio[1] < 0.3, "%.3f %.3f" % utc_ratio)
    vi = dict(intake)
    vi["voice-prod"] = [v / 3.6 for v in intake["voice-prod"]]
    vs, vp = C.shortfalls(vi, plan, M["gpr_exact"], live, M["cost"])
    check("R2c Voice's requests per second read as thousands moves nothing", vp == "docs-prod" and
          abs(vs["docs-prod"]["peak"] - gold) < 1e-9)
    allw1 = [dict(c, golive=K.Q1_WEEKS[0]) for c in live]
    gs, gp = C.shortfalls(intake, plan, M["gpr_exact"], allw1, M["cost"])
    check("R2d every contract counted from W01 (go-live weeks ignored) leaves the call and its bin",
          gp == "docs-prod" and K.nearest(gs["docs-prod"]["peak"], 10) == 340, "%.2f" % gs["docs-prod"]["peak"])
    check("R2e the rollup's missing hours sit outside Docs and Batch", all(
        len(R_[p]["t"]) == 8160 for p in ("docs-prod", "batch-prod")))
    check("R3a the easy route on the shipped data files Code at 300 (rules executed, close-out rates)",
          RG["R0 Docs GPU-seconds per request"]["pick"] == "code-prod" and K.nearest(code, 10) == 300)
    check("R3b changing the decisive step alone gives the golden; each lower rung alone does not",
          RG["R4 computed prompt and completion tokens at lc2's rates"]["docs"] == gold and
          all(RG[k]["pick"] != "docs-prod" for k in under))
    roll = R_["docs-prod"]
    rep = [k for k in range(1, len(roll["requests"])) if roll["requests"][k] == roll["requests"][k - 1]]
    check("R3c no copied block or repeated series in the rollup", len(rep) < 5, "%d repeats" % len(rep))
    check("R3c no document argues for a pool or ranks the pools on Q1", not re.search(
        r"\b(code-prod|Code)\b[^.]{0,60}\b(should|needs the|gets the)\b", docs_text))

    # ------------------------------------------------------------------ Ask A
    gh, lo = C.ask_a(target)
    check("A1 every pool's GPU-hours a quarter bin clear", all(bin_margin(gh[p], 10) >= 2.5 for p in K.POOLS),
          " ".join("%.1f" % gh[p] for p in K.POOLS))
    check("A2 every pool's longest stay a quarter bin clear", all(bin_margin(lo[p], 0.1) >= 0.025 for p in K.POOLS),
          " ".join("%.3f" % lo[p] for p in K.POOLS))
    stops = {"job log alone": C.ask_a(target, use_console=False),
             "job log, unpaired cordons dropped": C.ask_a(target, use_console=False, drop_unpaired=True)}
    for k, (g2, l2) in stops.items():
        check("A3 %s misses all twelve" % k, all(K.nearest(g2[p], 10) != K.nearest(gh[p], 10) and
                                                  round(l2[p], 1) != round(lo[p], 1) for p in K.POOLS))
    g3, l3 = C.ask_a(target, console_as_utc=True)
    check("A4 the console's times read as UTC miss five pools' GPU-hours",
          sum(K.nearest(g3[p], 10) != K.nearest(gh[p], 10) for p in K.POOLS) >= 5)
    g4, l4 = C.ask_a(target, use_job_complete=False)
    check("A5 jobs completed by hand missed: every pool's GPU-hours miss",
          all(K.nearest(g4[p], 10) != K.nearest(gh[p], 10) for p in K.POOLS))
    g5, l5 = C.ask_a(target, current_pool=True)
    check("A6 today's pool for every hour misses Chat and Agents", K.nearest(g5["chat-prod"], 10) != K.nearest(
        gh["chat-prod"], 10) and K.nearest(g5["agents-prod"], 10) != K.nearest(gh["agents-prod"], 10))
    gr = C.ask_a_rollup(target)
    check("A7 the rollup's hourly samples miss at least four pools' GPU-hours and give no stay length",
          sum(K.nearest(gr[p], 10) != K.nearest(gh[p], 10) for p in K.POOLS) >= 4)
    cons = C.read_console(target)
    nodes = C.read_nodes(target)
    jobs = C.read_jobs(target)
    jn = {e["job"]: e["node"] for e in jobs}
    per_pool = {p: 0 for p in K.POOLS}
    for c in cons:
        if c["action"] in ("node.uncordon", "fleetctl.job.complete"):
            t = K.ams_to_utc(c["local"])
            if K.NOV[0] <= t < K.NOV[1]:
                n = nodes[c["obj"] if c["action"] == "node.uncordon" else jn[c["obj"]]]
                per_pool[C._pool_of(n, t)] += 1
    check("A8 every pool has at least two stays closed from the console in November",
          all(v >= 2 for v in per_pool.values()), str(per_pool))
    check("A9 no shipped sentence links the console's actions to the job log", not re.search(
        r"console[^.]{0,80}(job|fleetctl)|(job|fleetctl)[^.]{0,80}console", text, re.I))

    # ------------------------------------------------------------------ Ask B
    acc, held = C.ask_b(target)
    check("B1 golden acceptance by rack", acc == {"R11": 48, "R12": 40, "R13": 48, "R14": 64}, str(acc))
    s1 = C.ask_b(target, gbit_fix=False)[0]
    check("B2 raw bus bandwidth against 360 misses all four racks", all(s1[r] != acc[r] for r in acc), str(s1))
    s2 = C.ask_b(target, racks_from_results=True)[0]
    check("B3 racks as the results record them miss R12 and R14", s2["R12"] != acc["R12"] and s2["R14"] != acc["R14"],
          str(s2))
    s3 = C.ask_b(target, divide_all=True)[0]
    check("B4 every run divided by eight misses", any(s3[r] != acc[r] for r in acc), str(s3))
    fab = list(csv.DictReader(open(os.path.join(target, R.F_FABRIC), encoding="utf-8")))
    check("B5 no column, run id or note names the unit change", "busbw" in fab[0] and not any(
        re.search(r"gbit|gb/s|unit|v2\.|release", " ".join(x.values()), re.I) for x in fab))
    check("B6 no shipped sentence names the re-racked nodes", not re.search(r"re-?rack|moved|rebalanc", text, re.I))

    # ------------------------------------------------------------------ separation line
    tmp = tempfile.mkdtemp(prefix="sep158_")
    try:
        for f in files:
            if f in (R.F_NODES, R.F_JOBS, R.F_CONSOLE, R.F_BURN, R.F_FABRIC, R.F_HANDOVER):
                continue
            shutil.copy(os.path.join(target, f), os.path.join(tmp, f))
        rows_ = list(csv.reader(open(os.path.join(tmp, R.F_ROLLUP), encoding="utf-8")))
        with open(os.path.join(tmp, R.F_ROLLUP), "w", encoding="utf-8", newline="") as fh:
            wr = csv.writer(fh, lineterminator="\n")
            wr.writerow(rows_[0])
            for r_ in rows_[1:]:
                r_[3], r_[9], r_[10] = "0", "0", "0"
                wr.writerow(r_)
        M2 = C.main_call(tmp)
        check("S1 the call with every ask file deleted and the in-service and TTFT columns blanked is unchanged",
              M2["pick"] == M["pick"] and abs(M2["docs_peak"] - gold) < 1e-9)
        for dfile in dis:
            if os.path.exists(os.path.join(tmp, dfile)):
                os.remove(os.path.join(tmp, dfile))
        M3 = C.main_call(tmp)
        check("S2 the call with every distractor deleted is unchanged", abs(M3["docs_peak"] - gold) < 1e-9)
    finally:
        shutil.rmtree(tmp)

    # ------------------------------------------------------------------ realism sweep
    people = set(K.PEOPLE.values()) | {"Demi Verhagen", "Vincent Palman", "Sam Kolen"}
    check("X1 personas drawn with guard.py names", people <= {
        "Janne Muijs", "Casper Heijmans", "Louise Hekker", "Mart Bosch", "Demi Verhagen", "Vincent Palman", "Sam Kolen"})
    bill = C.read_billing(target)
    check("X2 billing reconciles with the rollup's docs-prod requests within 0.2 per cent", recon(R_, bill) < 0.002,
          "%.4f" % recon(R_, bill))
    tot = [M["C"]["pools"][p]["busy_h"] for p in K.POOLS]
    check("X3 no close-out total on a round thousand", all(abs(x / 1000 - round(x / 1000)) > 0.002 for x in tot))
    late = []
    for f in files:
        if f.endswith(".csv") or f.endswith(".jsonl"):
            body = open(os.path.join(target, f), encoding="utf-8").read()
            for mm in re.finditer(r"20\d\d-\d\d-\d\d", body):
                if mm.group(0) > "2026-12-07" and f not in (R.F_NODES,):
                    late.append(f)
                    break
    check("X4 no extract carries a date after the pull", not late, ", ".join(late))
    names = [n for n in C.read_ledger(target)[0]]
    check("X5 the ledger's go-lives are Mondays in Q1 for signed contracts", all(
        dt.date.fromisoformat(r["Go-live"]).weekday() == 0 for r in names if r["Status"] == "Signed"))
    for f in files:
        if f.endswith(".xlsx"):
            z = zipfile.ZipFile(os.path.join(target, f))
            app = z.read("docProps/app.xml").decode()
            core = z.read("docProps/core.xml").decode()
            check("X6 %s carries no writer signature" % f, "openpyxl" not in app + core and "Microsoft Excel" in app)
        if f.endswith(".pdf"):
            b = open(os.path.join(target, f), "rb").read()
            check("X7 %s carries no writer banner" % f, b"ReportLab" not in b and b"reportlab" not in b)
    gpng = open(os.path.join(TASK, "golden", "pool_out_of_service_nov2026.png"), "rb").read()
    check("X8 the chart carries no writer signature", b"matplotlib" not in gpng.lower())
    em = [f for f in files if "\u2014" in open(os.path.join(target, f), encoding="utf-8", errors="ignore").read()]
    check("X9 no em dash in any text file", not em, ", ".join(em))
    import pypdf
    pdf_text = {f: " ".join(pg.extract_text() or "" for pg in pypdf.PdfReader(os.path.join(target, f)).pages)
                for f in files if f.endswith(".pdf")}
    check("X9b no em or en dash in any PDF's text", not any(("\u2014" in t or "\u2013" in t) for t in pdf_text.values()))
    every = " ".join(pdf_text.values()) + " " + text
    check("X10 nothing in the pack says it was built (H24)", not re.search(
        r"constructed|fictional|fictitious|invented|synthetic|this exercise|generated by", every, re.I))
    log = open(os.path.join(target, DOC.F_LOG), encoding="utf-8").read()
    check("X11 the pull log lists every shipped file but itself (H9)",
          set(re.findall(r"wrote (\S+)", log)) == set(files) - {DOC.F_LOG})
    sub_ = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    cited = set(re.findall(r"[\w\-\.]+\.(?:pdf|xlsx|csv|md|jsonl|log)", sub_)) - {"stopgap_q1_2027.xlsx"}
    check("X12 every file the write-up names ships (H8)", cited <= set(files), ", ".join(sorted(cited - set(files))))
    check("X13 the pack's people are the card's", not re.search(r"John Doe|Jane Doe|Acme|Company A", every))
    keys = set()
    dup = 0
    with open(os.path.join(target, R.F_ROLLUP), encoding="utf-8") as fh:
        for r_ in csv.DictReader(fh):
            k_ = (r_["hour_start_utc"], r_["pool"])
            dup += k_ in keys
            keys.add(k_)
    led = C.read_ledger(target)[0]
    ea_id = [x for x in led if x["Contract"].startswith("EA")][0]["Account id"]
    check("X14 one rollup row per pool-hour, one ledger row per contract, the tenant's id in billing",
          dup == 0 and len({x["Contract"] for x in led}) == len(led) and
          any(x["org"] == ea_id and x["channel"] == "report" for x in bill))

    # ------------------------------------------------------------------ figures, golden and write-up agree
    G = json.load(open(os.path.join(HERE, "figures.json")))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    check("F1 figures.json carries the call", G["call"]["pool"] == "docs-prod" and G["call"]["shortfall"] == "340"
          and G["call"]["runner_up"] == "code-prod" and G["call"]["runner_up_shortfall"] == "300")
    devs = [abs(1 - C.pilot_ratio(M, target, u, g)[0]) for u in (False, True) for g in (None, M["gpr"]["docs-prod"])]
    check("F1b the write-up's pilot bound holds on Amsterdam and UTC days, exact and printed rates, by half a point",
          all(d_ * 100 <= int(G["steps"]["pilot_within_pct"]) - 0.5 for d_ in devs), " ".join("%.4f" % d_ for d_ in devs))
    check("F2 the write-up states the call once in block 1", "**Give the stopgap cluster to docs-prod (Docs): its Q1 "
          "peak-week shortfall is 340 GPUs, in 2027-W13.**" in sub)
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(TASK, "golden", "stopgap_q1_2027.xlsx"), data_only=True)
    ws = wb["Out of service Nov 2026"]
    gold_rows = {r[0]: (r[1], r[2]) for r in ws.iter_rows(min_row=4, values_only=True) if r[0] in K.POOLS}
    check("F3 the golden workbook's out-of-service table equals figures.json", all(
        "{:,}".format(gold_rows[p][0]) == G["answers"]["out_of_service"][p]["gpu_hours"] and
        "%.1f" % gold_rows[p][1] == G["answers"]["out_of_service"][p]["longest"] for p in K.POOLS))
    wa = wb["Stopgap acceptance"]
    acc_rows = {r[0]: r[1] for r in wa.iter_rows(min_row=4, values_only=True) if r[0] in ("R11", "R12", "R13", "R14")}
    check("F4 the golden workbook's acceptance table equals figures.json", all(
        str(acc_rows[r]) == G["answers"]["acceptance"][r]["accepted"] for r in acc_rows))
    st = wb["Stopgap Q1 2027"]
    check("F5 the golden workbook states the pool and its shortfall", st["A5"].value == "docs-prod" and
          st["C5"].value == 340)
    check("F6 no em dash in the write-up", "\u2014" not in sub and "\u2013" not in sub)

    n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
    print("%d checks, %d FAIL" % (len(RESULTS), n_fail))
    return 0 if n_fail == 0 else 1


def recon(R_, bill):
    from collections import defaultdict
    d = R_["docs-prod"]
    by = defaultdict(float)
    for t, r in zip(d["t"], d["requests"]):
        by[K.utc_to_ams(t).date()] += r
    bb = defaultdict(float)
    for x in bill:
        bb[x["date"]] += x["requests"]
    days = [dd for dd in bb if dt.date(2026, 9, 1) <= dd <= dt.date(2026, 12, 6)]
    return abs(sum(by[dd] for dd in days) / sum(bb[dd] for dd in days) - 1)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")))
