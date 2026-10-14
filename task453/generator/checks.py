"""task453's assertions, run on every build: the input gates, the golden from the bundle, the corridor of every
reasonable implementation, every wrong route by name, the margins, every semantic-fork row (SF1 to SF14), the
three-rules block (R1 to R3c) on the clean truth, mess neutrality, the ask's stops and cracker, the separation of the
ask from the main call, the distractors' deletion test and the realism sweep."""
import json
import os
import re
import shutil
import tempfile

import numpy as np
import pandas as pd

import golden as GD
import methods as M
import pack as P
import survey as S
import world as W

RESULTS = []


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))


def restate(x):
    return M.restated(x)


def nat_cells(une, lab):
    un, ln = une.sum(1), lab.sum(1)
    t, g = np.meshgrid(np.arange(W.T), np.arange(6), indexing="ij")
    return dict(t=t.ravel(), r=np.zeros(t.size, int), g=g.ravel(), y=(100 * un / ln).ravel(), w=ln.ravel(),
                new=M.NEWM.ravel(), m=M.MISM.ravel())


def sexage_cells(S_):
    une = S_["une"].astype(float)
    lab = (S_["une"] + S_["emp"]).astype(float)
    tt, rr, gg, ss, aa = np.meshgrid(np.arange(W.T), np.arange(W.R), np.arange(6), np.arange(2), np.arange(5),
                                     indexing="ij")
    return dict(t=tt.ravel(), r=(rr * 10 + ss * 5 + aa).ravel(), g=gg.ravel(), y=(100 * une / lab).ravel(),
                w=lab.ravel(), new=M.NEWM[tt, gg].ravel(), m=M.MISM[tt, gg].ravel())


def fe_sparse(F, cols, use, weighted):
    from scipy import sparse
    from scipy.sparse.linalg import lsqr
    key = F["t"][use] * 1000 + F["r"][use]
    _, idx = np.unique(key, return_inverse=True)
    n = int(use.sum())
    X1 = sparse.csr_matrix((np.ones(n), (np.arange(n), idx)))
    M5 = sparse.csr_matrix(np.column_stack([(F["m"][use] == j) for j in range(2, 7)]).astype(float))
    C = sparse.csr_matrix(np.column_stack([np.asarray(c)[use] for c in cols]).astype(float))
    X = sparse.hstack([X1, M5, C]).tocsr()
    sw = np.sqrt(F["w"][use] / F["w"][use].mean()) if weighted else np.ones(n)
    b = lsqr(sparse.diags(sw) @ X, F["y"][use] * sw, atol=1e-12, btol=1e-12, iter_lim=50000)[0]
    return b[-len(cols):]


def run(target, golden_dir, world=None, meta_path=None):
    RESULTS.clear()
    S_ = world
    X = world["golden"] if world and "golden" in world else GD.compute(target)
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path)) if meta_path else {}

    # ---------------------------------------------------------------- input gates
    ok("gate: ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("gate: three or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    ok("gate: a file of 25,000 rows or more", world["counts"]["old"] >= 25000 and world["counts"]["field"] >= 25000,
       "%d and %d" % (world["counts"]["old"], world["counts"]["field"]))
    dis = meta.get("distractor_files", [])
    ok("gate: two or more distractors in metadata.json", len(dis) >= 2 and all(d in files for d in dis), dis)
    ok("gate: no file name says distractor or answer", not any(re.search("distract|answer|known_issue", f) for f in files))
    ok("gate: every pack file has a source and licence in metadata.json",
       sorted(x["path"] for x in meta.get("files", [])) == files and all(x.get("license") for x in meta["files"]))

    # ---------------------------------------------------------------- the golden, from the bundle
    ok("golden: change rounds to 0.5 points", X["change"] == 0.5, "%.4f" % X["G"])
    ok("golden: restated trigger 6.5", X["trigger"] == 6.5)
    ok("golden: designated Eastern Ranges, Western Coast, River Delta, Highlands",
       X["designated"] == ["05", "07", "08", "09"], X["designated"])
    F = X["F"]
    truthF = None
    if S_ is not None:
        Fg = M.cells_from(S_["une"].sum(axis=(3, 4)), (S_["une"] + S_["emp"]).sum(axis=(3, 4)))
        ok("golden: the bundle's cells equal the generator's", np.allclose(Fg["y"], F["y"], atol=5e-6) and
           np.allclose(Fg["w"], F["w"], rtol=1e-9, atol=1.0))

    # ---------------------------------------------------------------- the corridor (C3)
    var = M.variants(F)
    une, lab = GD.read_cells(target)
    Fn = nat_cells(une, lab)
    for pre in (24, 36, 42):
        u = Fn["t"] >= W.PHASE - pre
        var[("national", pre, "each")] = float(M.mis_effects(Fn, u, True, True).mean())
        b = M.fe(Fn, [Fn["new"], Fn["new"] * (Fn["m"] >= 2)], u, True)
        var[("national", pre, "first/later")] = float(b[0] + 5.0 / 6.0 * b[1])
    if S_ is not None:
        Fc = sexage_cells(S_)
        u = Fc["t"] >= W.PHASE - 42
        for wt in (True, False):
            e = fe_sparse(Fc, [Fc["new"] * (Fc["m"] == j) for j in range(1, 7)], u, wt)
            var[("sex and age cells", wt)] = float(e.mean())
    vals = np.array(list(var.values()))
    ok("C3 corridor: every implementation rounds to 0.5", all(round(v + 1e-9, 1) == 0.5 for v in vals),
       "%.4f to %.4f over %d" % (vals.min(), vals.max(), len(vals)))
    ok("C3 corridor: every implementation 0.02 or more from a rounding edge",
       vals.min() >= 0.47 and vals.max() <= 0.53, "%.4f to %.4f" % (vals.min(), vals.max()))
    ok("golden: the first-interview effect is negative and the later ones positive",
       X["eff"][0] < -0.3 and (X["eff"][1:] > 0.4).all(), np.round(X["eff"], 3).tolist())

    # ---------------------------------------------------------------- the wrong routes, by name
    wr = M.wrong_routes(F, X["nat"])
    ok("R0: no restatement files 6.0", restate(0.0) == 6.0)
    ok("R1 (default): the arm gap files 7.2", restate(wr["R1 arm gap"]) == 7.2, "%.3f" % wr["R1 arm gap"])
    ok("R1': the rotation-group letter held fixed files 7.2", restate(wr["R1 rotation letter held fixed"]) == 7.2,
       "%.3f" % wr["R1 rotation letter held fixed"])
    r2 = wr["R2 one effect"]
    ok("R2: one effect within month in sample files 6.3 or 6.4 on every implementation",
       all(restate(v) in (6.3, 6.4) for v in r2.values()) and max(r2.values()) <= 0.42,
       "%.3f to %.3f" % (min(r2.values()), max(r2.values())))
    r3 = wr["R3 continuing households"]
    ok("R3': the continuing households' effect files 6.7", all(restate(v) == 6.7 for v in r3.values()),
       "%.3f to %.3f" % (min(r3.values()), max(r3.values())))
    ok("event: 2026 against 2024 in the published rate files 6.8", restate(wr["event 2026 against 2024"]) == 6.8,
       "%.3f" % wr["event 2026 against 2024"])
    sets = {"R0": M.designated(X["avg"], 6.0), "R2 6.3": M.designated(X["avg"], 6.3),
            "R2 6.4": M.designated(X["avg"], 6.4), "R3'": M.designated(X["avg"], 6.7),
            "event": M.designated(X["avg"], 6.8), "R1": M.designated(X["avg"], 7.2)}
    ok("ladder: every wrong route designates another set",
       all(v != X["designated"] for v in sets.values()), {k: v for k, v in sets.items()})
    ok("ladder: R0 designates six, R2 five, the golden four, R1 two",
       (len(sets["R0"]), len(sets["R2 6.3"]), len(sets["R2 6.4"]), len(X["designated"]), len(sets["R1"])) ==
       (6, 5, 5, 4, 2))
    ok("dominance: the nearest wrong routes sit 0.07 or more from the golden's corridor",
       min(abs(np.array(list(r2.values())) - vals.min()).min(),
           abs(np.array(list(r3.values())) - vals.max()).min()) >= 0.07)

    # ---------------------------------------------------------------- margins and the semantic fork table
    edge = np.abs((X["avg"] * 100) % 1 - 0.5)
    ok("bins: no region's 2026 average sits on a two-decimal rounding edge", edge.min() >= 0.15,
       "%.3f" % edge.min())
    ok("margin: no region's 2026 average within 0.04 of 6.5", np.abs(X["avg"] - 6.5).min() >= 0.04,
       "%.3f" % np.abs(X["avg"] - 6.5).min())
    act_text = pdf_text(os.path.join(target, P.FILES["act"]))
    ok("SF1: the Act's trigger is 6.0 per cent", "The trigger rate is 6.0 per cent" in act_text)
    ok("SF2: the change rounded then added equals the sum rounded",
       round(6.0 + round(X["G"], 1), 1) == round(6.0 + X["G"] + 1e-9, 1) == 6.5)
    ok("SF3: a comparison of periods (2026 against 2024) files another trigger",
       restate(wr["event 2026 against 2024"]) != 6.5)
    ok("SF4: weighted and unweighted regional cells both round to 0.5",
       all(round(v + 1e-9, 1) == 0.5 for k, v in var.items() if isinstance(k, tuple) and len(k) == 5))
    ok("SF5: the phase-in as seen (the arm gap) files another trigger", restate(wr["R1 arm gap"]) != 6.5)
    ok("SF6: half up and half to even agree", round(X["G"], 1) == float(np.round(X["G"], 1)))
    ok("SF7: at or above and strictly above designate the same regions",
       [c for i, c in enumerate(W.RCODE) if X["avg"][i] > 6.5] == X["designated"])
    unr = S.published(S_)[0] if S_ is not None else None
    if unr is not None:
        avg_unr = unr[W.Y26:].mean(0)
        tot = (S_["une"].sum(axis=(2, 3, 4))[W.Y26:].sum(0) / (S_["une"] + S_["emp"]).sum(axis=(2, 3, 4))[W.Y26:].sum(0)) * 100
        ok("SF8: every reading of the twelve-month average designates the same regions",
           M.designated(avg_unr, 6.5) == X["designated"] == M.designated(tot, 6.5),
           "North Coast %.3f %.3f %.3f" % (X["avg"][2], avg_unr[2], tot[2]))
    ok("SF9: every rotation group answers the redesigned questionnaire in every month of 2026",
       all(W.redesigned(t, g) for t in range(W.Y26, W.T) for g in range(6)))
    F19 = dict(F)
    remap = {W.RCODE.index(c): W.RCODE.index(W.CODE19[c]) for c in W.RCODE}
    F19["r"] = np.array([remap[r] if t < W.MONTHS.index("2025-01") else r for t, r in zip(F["t"], F["r"])])
    ok("SF10: reading the 2019 codes as 2025 codes leaves the change unchanged",
       abs(M.golden_break(F19)[0] - X["G"]) < 1e-9)
    gcsv = pd.read_csv(os.path.join(golden_dir, GD.CSV_NAME), dtype={"region": str})
    pre = gcsv[gcsv["month"] < "2025-07"]
    ok("SF11: months before July 2025 restated by the change as determined (one decimal place) for every region alike",
       np.allclose(pre["redesigned_basis_rate"] - pre["published_rate"], X["change"], atol=1e-9))
    ph = gcsv[gcsv["month"] >= "2025-07"]
    ok("SF12: July 2025 on carried as published (the transition months marked)",
       np.allclose(ph["redesigned_basis_rate"], ph["published_rate"], atol=1e-9) and
       set(gcsv[(gcsv["month"] >= "2025-07") & (gcsv["month"] <= "2025-11")]["collected_on"]) ==
       {"both questionnaires (as published)"})
    gs = pd.read_csv(os.path.join(golden_dir, GD.CSV_NAME), dtype=str)
    ok("SF12: every CSV rate carries one decimal place, as the release publishes",
       gs["published_rate"].str.fullmatch(r"\d+\.\d").all() and gs["redesigned_basis_rate"].str.fullmatch(r"\d+\.\d").all())
    trunc = [float(M.mis_effects(F, F["t"] <= W.PHASE + k).mean()) for k in (4, 5)]
    ok("SF15: reading the effects only from the months before full use (to November or December 2025) files another "
       "trigger, which the Act's 'once the change is in full use' rules out", all(restate(v) != 6.5 for v in trunc),
       "%.3f and %.3f" % tuple(trunc))
    fw = pd.read_parquet(os.path.join(target, P.FILES["field"]))
    ok("SF13: the fieldwork file holds the contact months October to December 2026",
       sorted(fw["contact_month"].unique()) == ["2026-10", "2026-11", "2026-12"])
    st = M.dwellings_q4_stops(X["rows"], X["psu_region"])
    ok("SF14: full interviews only gives another count", st["complete only"]["all"] != X["q4"]["all"],
       "%d against %d" % (st["complete only"]["all"], X["q4"]["all"]))

    # ---------------------------------------------------------------- the three rules, executed
    ok("R1 the field's raw material ships: estimation cells by month, region, rotation group, sex and age on both "
       "questionnaires", world["counts"]["old"] > 60000 and world["counts"]["new"] > 8000)
    heads = open(os.path.join(target, P.FILES["old"])).readline() + open(os.path.join(target, P.FILES["new"])).readline()
    ok("R1 no shipped column holds month in sample, the change or a designation",
       not re.search(r"(?i)mis\b|month_in_sample|interview|effect|change|designat|trigger", heads), heads.strip())
    if S_ is not None:
        L = (S_["lf"]).sum(axis=(3, 4)).astype(float)
        truth = (S_["p"] * S_["lf"]).sum(axis=(3, 4)) / L
        Ft = M.cells_from(truth * L / 100.0, L)
        ag = M.arm_gap(Ft)
        ok("R3a analyst test: on the clean truth the arm gap files 7.2 and designates River Delta and Highlands",
           restate(ag) == 7.2 and M.designated(X["avg"], restate(ag)) == ["08", "09"], "%.3f" % ag)
        gt, et = M.golden_break(Ft)
        ok("R3b the decisive step alone: the six effects averaged on the clean truth file 6.5", restate(gt) == 6.5,
           "%.4f" % gt)
        one = float(M.fe(Ft, [Ft["new"]], Ft["t"] >= 0, True)[0])
        ok("R3b the first correction alone (one effect, month in sample fixed) files 6.3 or 6.4 on the clean truth",
           restate(one) in (6.3, 6.4), "%.3f" % one)
        ok("R3b the clean truth's effects: first interview %.2f, later %.2f (within 0.015, the sampled sex and age mix)"
           % (W.FIRST_EFFECT, W.LATER_EFFECT),
           abs(et[0] - W.FIRST_EFFECT) < 0.015 and np.allclose(et[1:], W.LATER_EFFECT, atol=0.015),
           np.round(et, 3).tolist())
    reg_rel = X["reg"]
    rep = any((reg_rel[t] == reg_rel[t + 12]).all() for t in range(W.T - 12))
    ok("R3c no copied or repeated block in the published regional rates", not rep)
    docs_text = pdf_text(os.path.join(target, P.FILES["note"])) + act_text
    ok("R3c no document states a change, a restated trigger or a designation",
       not re.search(r"restated (trigger )?(rate )?(is|of|at) \d|\b6\.[1-9] per cent|designat\w+ (are|is) [A-Z]", docs_text))
    Fk = dict(F)
    oldq = np.array([not W.redesigned(t, g) for t, g in zip(F["t"], F["g"])])
    Fk["w"] = np.where(oldq, F["w"] / 1000.0, F["w"])
    gk = M.golden_break(Fk)[0]
    ok("R2 mess: CAI 2014's thousands left unconverted (cells weighted 1,000 times too light) still files 6.5",
       restate(gk) == 6.5, "%.4f" % gk)
    early = M.designated(reg_rel[W.Y26 - 1:W.Y26 + 11].mean(0), 6.5)
    ok("R2 mess: the release's Table 2 read one month early still designates the same regions",
       early == X["designated"], early)

    # ---------------------------------------------------------------- the ask
    ok("ask: golden counts", X["q4"]["all"] == sum(X["q4"][c] for c in W.RCODE), X["q4"])
    ok("ask cracker (dwelling references counted) misses every figure",
       all(st["slots"][k] != X["q4"][k] for k in W.RCODE + ["all"]), st["slots"])
    for k in ("interviews", "every dwelling", "complete only", "eligible"):
        ok("ask stop '%s' misses every figure" % k, all(st[k][c] != X["q4"][c] for c in W.RCODE + ["all"]))
    ok("ask: no golden count is round", all(X["q4"][k] % 100 for k in W.RCODE + ["all"]))
    tmp = tempfile.mkdtemp()
    try:
        for f in files:
            if f not in (P.FILES["field"], P.FILES["psu"]):
                shutil.copy(os.path.join(target, f), tmp)
        une2, lab2 = GD.read_cells(tmp)
        F2 = M.cells_from(une2, lab2)
        reg2, _ = GD.read_release(tmp)
        ok("separation: the change and the designation need no fieldwork row or unit lookup",
           M.golden_break(F2)[0] == X["G"] and M.designated(M.averages_2026(reg2), restate(M.golden_break(F2)[0])) ==
           X["designated"])
        for f in dis:
            if os.path.exists(os.path.join(tmp, f)):
                os.remove(os.path.join(tmp, f))
        une3, lab3 = GD.read_cells(tmp)
        ok("distractors: the golden is unchanged with every distractor deleted",
           M.golden_break(M.cells_from(une3, lab3))[0] == X["G"])
    finally:
        shutil.rmtree(tmp)

    # ---------------------------------------------------------------- realism sweep
    q4v = [X["q4"][c] for c in W.RCODE]
    ok("realism: no two regions share a count or a 2026 average", len(set(q4v)) == W.R and
       len(set(np.round(X["avg"], 3))) == W.R)
    ok("realism: the published national rate is never flat for five months",
       not any(len(set(X["nat"][t:t + 5])) == 1 for t in range(W.T - 4)))
    cells = pd.read_csv(os.path.join(target, P.FILES["new"]))
    g_ = cells.groupby(["region", "rotation_group", "sex", "age_band"])["unemployed"]
    ok("realism: ICS cells vary (a weighted count repeats within under 3 per cent of cell series, as chance gives "
       "for counts of this size)",
       (g_.nunique() != g_.count()).mean() < 0.03, "%d of %d" % ((g_.nunique() != g_.count()).sum(), g_.ngroups))
    people = set(W.PEOPLE.values())
    repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    card = json.load(open(os.path.join(repo, ".claude", "skills", "fingerprint", "cards", "task453.json")))
    ok("realism: every persona in the pack is on the card", people <= set(card["world"]["people"]), sorted(people))
    raw = b"".join(open(os.path.join(target, f), "rb").read() for f in files if f.endswith((".pdf", ".xlsx")))
    ok("realism: containers carry no writing library's name",
       not re.search(rb"ReportLab|reportlab|openpyxl|matplotlib", raw))
    txt = "".join(open(os.path.join(target, f), encoding="utf-8").read() for f in files if f.endswith(".csv"))
    ok("realism: no em or en dash in any text file", "—" not in txt and "–" not in txt and
       "—" not in docs_text and "–" not in docs_text)
    figs = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    exc = []
    for pre in (24, 36, 42):
        for wt in (True, False):
            use = (F["t"] < W.PHASE) & (F["t"] >= W.PHASE - pre)
            b = M.fe(F, [(F["m"] == j).astype(float) for j in range(2, 7)], use, wt, mis_fe=False)
            prof = np.concatenate([[0.0], b])
            exc.append(prof[0] - prof.mean())
    ok("figures: the first-interview excess rounds to 1.3 on every implementation",
       all(round(e + 1e-9, 1) == 1.3 for e in exc) and figs["first_interview_excess_points"] == 1.3,
       "%.3f to %.3f" % (min(exc), max(exc)))
    ok("figures: the arm gap rounds to 1.2 and files 7.2", figs["arm_gap_points"] == 1.2 and
       figs["arm_gap_trigger_pct"] == 7.2)
    nc = 6.5 - float(X["avg"][W.RCODE.index("03")])
    ok("figures: North Coast misses the restated trigger by its computed shortfall, 0.04 or more",
       figs["north_coast_shortfall_points"] == round(nc, 2) and nc >= 0.04, "%.4f" % nc)
    ok("figures.json: the call as computed", figs["restated_trigger_pct"] == X["trigger"] and
       figs["change_points"] == X["change"] and figs["q4_responding_dwellings"]["all"] == X["q4"]["all"])

    bad = [r for r in RESULTS if not r[1]]
    for label, good, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if good else "FAIL", label, ("  [%s]" % (detail,)) if detail != "" else ""))
    print("checks: %d, failed %d" % (len(RESULTS), len(bad)))
    return not bad


def pdf_text(path):
    from pypdf import PdfReader
    return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)
