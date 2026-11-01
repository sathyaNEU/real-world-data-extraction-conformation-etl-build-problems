"""Generator assertions on the clean truth and the cut pack (target/). Exit 1 on any failure."""
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import analysis as AN
import ceiling as CE
import truth as TR
from world import build_all
from common import PROVIDERS, FLOOR, VOLUME_2027, RENAME
from h21 import clashes

STANDING = [f + "_" + w for f in ("cell", "reg", "ipw", "pooled") for w in ("f30", "f90", "f90op", "f365")]


class Checker:
    def __init__(self):
        self.rows = []

    def check(self, label, ok, detail=""):
        self.rows.append((label, bool(ok), detail))
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, "" if ok else "   " + str(detail)[:300]))


def rnd(x):
    return int(math.floor(x + 0.5))


def setof(pl):
    return tuple(sorted(u for u in pl if pl[u] > 0))


def bin_dist(x):
    return abs(x - math.floor(x) - 0.5)


def interval(order, members):
    pos = sorted(order.index(m) for m in members)
    return pos == list(range(pos[0], pos[0] + len(pos)))


def main(target):
    K = Checker()
    target = str(target)
    A = build_all()
    res = AN.run(target)
    L, m, R, fam, cap, place = res["L"], res["m"], res["R"], res["fam"], res["cap"], res["place"]
    gold = R["GOLD"]
    gset = setof(place["GOLD"])
    units = sorted(gold)
    names = dict(zip(L["prov"].provider_code, L["prov"].provider_name))

    # ---------------------------------------------------------------- the golden against the truth
    gt, el, netE_t = TR.golden_truth(A)
    key = {str(p["key"]): p["key"] for p in PROVIDERS}
    K.check("golden from target equals the generator's truth on every provider",
            all(abs(gold[u] - gt[key[u]]) < 1e-9 for u in units), {u: (gold[u], gt[key[u]]) for u in units})
    K.check("eligible operations from target equal the truth's", len(m) == len(el), (len(m), len(el)))
    # full-information truth: every non-answer's real 12-month change (known to the world only)
    el = el.copy()
    el["d_full"] = el.pre_obs - el.post_score - el.E
    full = {str(k): netE_t + g.d_full.mean() for k, g in el.groupby("prov")}
    K.check("R2 the golden recovers the full-information outcome: same set and every provider within 0.6",
            setof(TR.place({int(u): full[u] for u in units})) == tuple(int(u) for u in gset)
            and all(abs(full[u] - gold[u]) < 0.6 for u in units), {u: round(full[u] - gold[u], 2) for u in units})

    # ---------------------------------------------------------------- R1 to R3: the three rules executed
    cols = []
    for fn in os.listdir(target):
        p = os.path.join(target, fn)
        if fn.endswith(".csv"):
            cols += list(pd.read_csv(p, nrows=0).columns)
        elif fn.endswith(".xlsx"):
            cols += [str(c) for c in pd.read_excel(p, nrows=0, skiprows=3 if "proms" in fn else 4).columns]
    bad = [c for c in cols if re.search(r"adjust|expected|readmi|complic|flag|respon|outcome|score_adj|case.?mix", c, re.I)
           and c not in ("odi_raw_score", "responses")]
    K.check("R1 the field's raw material ships, never the deciding quantity: no column holds an adjusted outcome, an "
            "expected change, a response or readmission flag", not bad, bad)
    K.check("R1 the estimator is the field's own: the outcome is indirect standardisation with Appendix B read from "
            "the policy PDF", abs(AN.COEF["intercept"] - 17.4) < 1e-9 and abs(AN.COEF["pre"] - 0.42) < 1e-9, AN.COEF)
    default = setof(place["R2_casemix_imputation"])
    K.check("R2 Layer 2 decides: on the clean pack the default (case-mix imputation) files another set",
            default != gset, (default, gset))
    K.check("R2 the default's answer is seven providers with all 1,250 placed (Ends on)",
            len(default) == 7 and sum(place["R2_casemix_imputation"].values()) == VOLUME_2027,
            place["R2_casemix_imputation"])
    K.check("R2 the golden is five providers, 910 placed and 340 held",
            len(gset) == 5 and sum(place["GOLD"].values()) == 910, place["GOLD"])
    pol = AN.pdf_text_cached if hasattr(AN, "pdf_text_cached") else None
    from io_util import pdf_text
    policy = pdf_text(os.path.join(target, "spinal_contracting_policy_2027-28.pdf"))
    vocab = re.compile(r"readmi|re-admi|complicat|emergenc|non-?respon|missing|imput|later spell|follow-up rate|"
                       r"did not return|unanswered|infection|reoperat", re.I)
    K.check("R3 no filed sentence names the decisive step (policy text)", not vocab.search(policy),
            vocab.findall(policy))
    K.check("R3 the policy names the population the default leaves out (whether or not returned)",
            "whether or not the patient returned the 12-month questionnaire" in policy)
    wrong = ["R0_raw_answerers", "R1_answerers_adjusted", "R2_casemix_imputation", "R2b_casemix_ipw",
             "R3_at_expected", "R3b_no_change", "R4_same_provider_only", "R4b_reoperation_only", "R4c_any_later_spell"]
    K.check("R3 every route that does not condition on the post-discharge admission files a wrong set",
            all(setof(place[k]) != gset for k in wrong), {k: setof(place[k]) for k in wrong})
    K.check("R3 every standing member (cell, regression, weighting, pooled effect; 30 or 90 days from discharge, 90 or "
            "365 from the operation) files the golden set", all(setof(place[k]) == gset for k in STANDING),
            [k for k in STANDING if setof(place[k]) != gset])
    s_sp = {u: max(fam[k][u] for k in STANDING) - min(fam[k][u] for k in STANDING) for u in units}
    K.check("R3 the standing family's spread is at most 0.3 points on every provider", max(s_sp.values()) <= 0.3, s_sp)
    other_em = A["spells"][A["spells"].kind == "other"]
    K.check("R3 no planted record: emergency admissions without a complication occur at every provider's patients, and "
            "complications at every provider", other_em.pid.map(A["ops"].set_index("pid").prov).nunique() == 10
            and A["ops"].groupby("prov").comp.mean().min() > 0.04, A["ops"].groupby("prov").comp.mean().round(3).to_dict())

    # ---------------------------------------------------------------- the data refute the case-mix routes
    resp_f = m.groupby("f90").resp.mean()
    K.check("response by post-discharge emergency admission: under 0.4 against over 0.6",
            resp_f[True] < 0.4 and resp_f[False] > 0.6, resp_f.to_dict())
    per = all(g[g.f90].resp.mean() < g[~g.f90].resp.mean() - 0.2 for u, g in m.groupby("unit"))
    K.check("the response gap holds within every provider", per)
    dd = m[m.resp].groupby("f90").d.mean()
    K.check("answerers' change minus expected: readmitted at least 12 points lower", dd[False] - dd[True] > 12, dd.to_dict())
    mm = m.assign(fem=(m.sex == "2").astype(float))
    smd = {}
    for c in ("pre", "E"):
        a, b = mm[mm.resp][c], mm[~mm.resp][c]
        smd[c] = (a.mean() - b.mean()) / math.sqrt((a.var() + b.var()) / 2)
    K.check("Back-test: the field's non-response check passes (|standardised difference| under 0.1 on the "
            "pre-operative score and the expected change)", all(abs(v) < 0.1 for v in smd.values()), smd)

    # ---------------------------------------------------------------- bins and the floor under every standing member
    dist = {u: min(bin_dist(fam[k][u]) for k in STANDING) for u in units}
    K.check("every provider's whole-point outcome sits at least 0.2 inside its bin under every standing member",
            min(dist.values()) >= 0.2, {u: round(v, 2) for u, v in dist.items()})
    K.check("every standing member puts each provider in the golden's whole-point bin",
            all(rnd(fam[k][u]) == rnd(gold[u]) for k in STANDING for u in units))
    fl = {u: min(abs(fam[k][u] - FLOOR) for k in STANDING) for u in units}
    K.check("no provider within 0.35 of the 14.5 floor under any standing member (SF15)", min(fl.values()) >= 0.35,
            {u: round(v, 2) for u, v in fl.items()})
    nonel = {u: max(abs(fam[k][u] - gold[u]) for k in fam if "nonel" in k) for u in units}
    K.check("Layer 1: counting onward transfers as admissions keeps the set and every bin",
            all(setof(place[k]) == gset for k in fam if "nonel" in k)
            and all(rnd(fam[k][u]) == rnd(gold[u]) for k in fam if "nonel" in k for u in units), nonel)

    # ---------------------------------------------------------------- Shock: the set is no interval of any sort
    stats = {
        "answerers adjusted": R["R1_answerers_adjusted"], "case-mix imputation": R["R2_casemix_imputation"],
        "raw change": R["R0_raw_answerers"],
        "90-day emergency admission rate": {u: g.f90.mean() for u, g in m.groupby("unit")},
        "response rate": {u: g.resp.mean() for u, g in m.groupby("unit")},
        "eligible operations": {u: len(g) for u, g in m.groupby("unit")},
        "capacity offered": cap,
        "pre-operative score": {u: g.pre.mean() for u, g in m.groupby("unit")},
    }
    ivals = [k for k, st in stats.items() if interval(sorted(units, key=lambda u: -st[u]), gset)]
    K.check("Shock: the golden set is not an interval of any shipped or default statistic's sort", not ivals, ivals)

    # ---------------------------------------------------------------- the semantic fork table
    g2 = {u: res["netE"] + g.d[g.resp].mean() * 0 + 0 for u, g in m.groupby("unit")}
    K.check("SF1 the outcome is the national expected plus the provider's mean observed-minus-expected",
            all(abs(gold[u] - (res["netE"] + AN.cell(m, "f90", 0.0)[u])) < 1e-9 for u in units))
    K.check("SF2 answerers only (R1) files another set", setof(place["R1_answerers_adjusted"]) != gset)
    K.check("SF3 every eligible operation has a scored pre-operative questionnaire and no death within the year",
            m.pre.notna().all())
    q = L["q"]
    ops, s = AN.index_ops(L["s"])
    lk = q[(q.pseudo != "") & q.score.notna()].merge(ops[["pseudo_nhs_number", "procedure_date"]], left_on="pseudo",
                                                      right_on="pseudo_nhs_number")
    d12 = (lk[lk.qtype == "m12"].completed - lk[lk.qtype == "m12"].procedure_date).dt.days
    K.check("SF4 no 12-month questionnaire completed 446 to 456 days after its operation", not ((d12 >= 446) & (d12 <= 456)).any())
    dpre = (lk[lk.qtype == "pre"].procedure_date - lk[lk.qtype == "pre"].completed).dt.days
    K.check("SF5 no pre-operative questionnaire completed 89 to 91 days before its operation",
            not ((dpre >= 89) & (dpre <= 91)).any())
    q10 = q.copy()
    q10.loc[q10.n < 10, "score"] = np.nan
    L10 = dict(L, q=q10)
    m10, _, R10, _ = AN.main_call(L10)
    K.check("SF6 unscorable questionnaires exist, and requiring all ten sections keeps the set",
            (q.n < 8).sum() > 50 and setof(AN.place(R10["GOLD"], cap)) == gset)
    K.check("SF7 the change read the other way round puts every provider below zero, so no reading but the filed one "
            "places volume", all(v > 10 for v in R["R0_raw_answerers"].values()), R["R0_raw_answerers"])
    K.check("SF8 Penderwick House is one provider: no call-window operation under its successor code, and the "
            "capacity return under the successor maps to it", not (ops[(ops.procedure_date <= AN.CALL_TO) &
                                                                       (ops.provider_code == str(RENAME["new_key"]))].shape[0])
            and str(RENAME["old_key"]) in cap)
    adm_ops = ops.copy()
    inwin_p = set(adm_ops[(adm_ops.procedure_date >= AN.CALL_FROM) & (adm_ops.procedure_date <= AN.CALL_TO)].spell_id)
    inwin_a = set(adm_ops[(adm_ops.admission_date >= AN.CALL_FROM) & (adm_ops.admission_date <= AN.CALL_TO)].spell_id)
    K.check("SF9 dating by admission moves at most a handful of operations and keeps the set",
            len(inwin_p ^ inwin_a) <= 5, len(inwin_p ^ inwin_a))
    od = AN.dedup
    AN.dedup = lambda x: x
    m_nd, _, R_nd, _ = AN.main_call(L)
    AN.dedup = od
    K.check("SF10 keeping every submission keeps the set and every bin",
            setof(AN.place(R_nd["GOLD"], cap)) == gset and all(rnd(R_nd["GOLD"][u]) == rnd(gold[u]) for u in units))
    oi = AN.index_ops

    def loose(sp):
        sp = AN.dedup(sp)
        return sp[sp.primary_procedure.isin(AN.APPX_A)].copy(), sp
    AN.index_ops = loose
    _, _, R_lo, _ = AN.main_call(L)
    AN.index_ops = oi
    K.check("SF11 any Appendix A spell as an index operation keeps the set", setof(AN.place(R_lo["GOLD"], cap)) == gset)
    de = L["deaths"].merge(ops[["pseudo_nhs_number", "procedure_date"]], on="pseudo_nhs_number")
    dd_days = (de.date_of_death - de.procedure_date).dt.days
    K.check("SF12 no death falls 361 to 380 days after an operation", not ((dd_days >= 361) & (dd_days <= 380)).any())
    sx = q[(q.qtype == "pre") & (q.pseudo != "")].merge(ops[["pseudo_nhs_number", "sex"]], left_on="pseudo",
                                                         right_on="pseudo_nhs_number")
    K.check("SF13 the questionnaire's sex agrees with the hospital record for every linked patient",
            (sx.sex_x.astype(int) == sx.sex_y.astype(int)).all())
    nEr = m[m.resp].E.mean()
    alt = {u: v - res["netE"] + nEr for u, v in gold.items()}
    K.check("SF14 the national expected over the answerers keeps the set and every bin",
            setof(AN.place(alt, cap)) == gset and all(rnd(alt[u]) == rnd(gold[u]) for u in units))
    K.check("SF16 the golden's eligible capacity is under the volume, so the order of offers cannot move it",
            sum(cap[u] for u in gset) < VOLUME_2027)
    capx = pd.read_excel(os.path.join(target, "spinal_capacity_returns_2027-28.xlsx"), skiprows=4)
    K.check("SF17 each capacity return's total equals its four quarters",
            (capx.iloc[:, 2:6].sum(axis=1) == capx.iloc[:, 6]).all())
    rd = {u: float(rnd(v)) for u, v in gold.items()}
    K.check("SF18 rounding before the floor keeps the set", setof(AN.place(rd, cap)) == gset)

    # ---------------------------------------------------------------- the asks
    Ag, An, Ac = res["askA"]["golden"], res["askA"]["natural"], res["askA"]["cracker"]
    K.check("SF19 the March submissions double-list patients moved in March at every sending trust",
            all(res["askA"]["no_dedupe"][u]["waiting"] > Ag[u]["waiting"] for u in ("40117", "40152", "40188")))
    K.check("SF20 the policy files both waiting thresholds in days",
            "more than 364 days" in policy and "126 days or fewer" in policy)
    K.check("SF21 every triaged patient on the 31 March list matches exactly one surgical routing",
            res["askA_ambiguous"] == 0)
    ow = AN.waits
    A14, _, _ = AN.waits(target, L["site"], L["prov"])
    K.check("SF21 the golden waiting figures do not depend on the order of the rows", A14 == Ag)
    Bg, Bn, Bc, Bh = (res["askB"][k] for k in ("golden", "natural", "cracker", "half"))
    un = q[(q.qtype == "pre") & (q.pseudo == "") & q.score.notna()]
    K.check("SF22 questionnaires with no NHS number exist at every site", un.site.nunique() == 10, un.site.nunique())
    for lab, F in (("natural", An), ("cracker", Ac)):
        K.check("Ask A: the %s route misses every figure" % lab,
                all(F[u]["over52"] != Ag[u]["over52"] and rnd(F[u]["within18"]) != rnd(Ag[u]["within18"]) for u in units),
                {u: (F[u]["over52"], Ag[u]["over52"]) for u in units})
    for lab, F in (("natural", Bn), ("cracker", Bc), ("half-handled", Bh)):
        K.check("Ask B: the %s route misses every figure" % lab, all(rnd(F[u]) != rnd(Bg[u]) for u in units),
                {u: (round(F[u], 1), round(Bg[u], 1)) for u in units})
    K.check("Ask B: every participation figure sits at least 0.15 inside its whole per cent",
            min(bin_dist(v) for v in Bg.values()) >= 0.15, {u: round(v, 2) for u, v in Bg.items()})
    K.check("Ask A: every share sits at least 0.05 inside its whole per cent",
            min(bin_dist(Ag[u]["within18"]) for u in units) >= 0.05)
    # separation: zero device rows in the main population
    me = m.merge(q[(q.qtype == "pre")][["pseudo", "sup_op", "completed", "score"]], left_on=["pseudo_nhs_number", "pre"],
                 right_on=["pseudo", "score"], how="left")
    K.check("separation: the supplier's operation date equals the hospital record's for every main-population "
            "questionnaire", (me.sup_op == me.procedure_date).all())
    w_ = A["ops"]
    win = set(w_[(w_.op_date >= dt.date(2023, 4, 1)) & (w_.op_date <= dt.date(2025, 3, 31))].pid)
    rg = A["reg"]
    K.check("separation: no registration of the call's operations lacks its NHS number link",
            (rg[rg.pid.isin(win)].pseudo != "").all())
    K.check("separation: the call reads no waiting-list, triage or participation file",
            not re.search(r"ptl_|msk_triage|fft_|cqc_", open(HERE / "analysis.py").read().split("def participation")[0]))

    # ---------------------------------------------------------------- the ceiling on the cut pack
    ce, _ = CE.run(target)
    K.check("pair ceiling at or under 60 (cracker and mirror on the cut pack)", ce["pair_ceiling"] <= 60, ce["pair_ceiling"])
    K.check("mirror keeps under half the ask weight", ce["mirror_leakage"] < 50, ce["mirror_leakage"])
    K.check("the cracker keeps no ask figure", ce["routes"]["cracker"]["asks_kept"] == 0, ce["routes"]["cracker"]["kept"])

    # ---------------------------------------------------------------- input gates and realism
    files = sorted(os.listdir(target))
    exts = {f.rsplit(".", 1)[1] for f in files}
    K.check("input gates: 10 or more files", len(files) >= 10, len(files))
    K.check("input gates: 3 or more formats", len(exts) >= 3, exts)
    big = pd.read_csv(os.path.join(target, "apc_spells_lumbar_cohort_2022-26.csv"), usecols=[0])
    K.check("input gates: a file of 25,000 or more rows", len(big) >= 25000, len(big))
    meta_d = json.load(open(HERE.parent / "metadata.json")) if (HERE.parent / "metadata.json").exists() else None
    K.check("input gates: two or more distractors named in metadata.json",
            meta_d is None or len(meta_d.get("distractors", [])) >= 2)
    K.check("the distractors are unused by the solution", not re.search(r"fft_|cqc_", open(HERE / "analysis.py").read()))
    K.check("no file describes the data (readme, dictionary, notes, manifest)",
            not [f for f in files if re.search(r"readme|dictionar|notes|manifest|schema|guide", f, re.I)])
    K.check("no file name carries the author's words",
            not [f for f in files if re.search(r"trap|decoy|test_|golden|answer|stump|distract", f, re.I)])
    texts = {}
    for f in files:
        p = os.path.join(target, f)
        if f.endswith((".csv", ".json")):
            texts[f] = open(p, encoding="utf-8").read()
        elif f.endswith(".pdf"):
            texts[f] = pdf_text(p)
        elif f.endswith(".xlsx"):
            with zipfile.ZipFile(p) as z:
                texts[f] = " ".join(z.read(n).decode("utf-8", "ignore") for n in z.namelist())
    bw = re.compile(r"\b(trap|decoy|rung|stump|golden|synthetic|generator|distractor|ladder|solver|answer key)\b|\u2014|\u2013", re.I)
    K.check("no author vocabulary or em or en dash in any shipped file",
            not [(k, mm_.group(0)) for k, t in texts.items() for mm_ in [bw.search(t)] if mm_])
    tool = [f for f, t in texts.items() if re.search(r"openpyxl|ReportLab|python-docx|pandas", t)]
    K.check("containers scrubbed: no toolchain signature in any shipped file", not tool, tool)
    late = []
    for f, t in texts.items():
        for y, mo, d in re.findall(r"\b(20\d\d)-(\d\d)-(\d\d)\b", t):
            if dt.date(int(y), int(mo), int(d)) > dt.date(2026, 10, 6):
                late.append((f, y, mo, d))
                break
    K.check("no date after the as-of date (6 October 2026) in any file", not late, late[:5])
    per_prov = m.groupby("unit").size()
    K.check("realism: no two providers carry the same eligible count", per_prov.is_unique, per_prov.to_dict())
    spc = L["s"].groupby("provider_code").size()
    K.check("realism: no two providers carry the same spell count", spc.is_unique)
    K.check("realism: the questionnaire deliveries' row counts are not round", all(
        n % 100 != 0 for n in (len(q[q.completed < pd.Timestamp("2025-04-01")]), len(q[q.completed >= pd.Timestamp("2025-04-01")]))))
    inv = ["Quenmoor and Kirkbeck Integrated Care Board", "Mossgill Outcomes"] + [p["name"] for p in PROVIDERS] + \
          [p["org"] for p in PROVIDERS] + [RENAME["new_name"], "Fernhollow Community Hospital",
                                          "Brackenholt Community Hospital", "Hawksmere District Hospital"]
    cl = clashes(inv)
    K.check("H21 invented names clear of real places, NHS organisations and other cards' names", not cl, cl)
    golden_dir = HERE.parent / "golden"
    if (golden_dir / "spinal_volume_2027-28.csv").exists():
        gc = pd.read_csv(golden_dir / "spinal_volume_2027-28.csv")
        allnames = " ".join(texts.values())
        K.check("every provider label the golden prints appears in a shipped file",
                all(n in allnames for n in gc.provider.dropna() if not str(n).startswith("Not placed")))
        uo = lambda c: L["site"][str(int(c))]
        K.check("the golden csv's figures equal the analysis", all(
            int(r.outcome_points) == rnd(gold[uo(r.provider_code)]) and int(r.operations_placed) == place["GOLD"][uo(r.provider_code)]
            for r in gc.dropna(subset=["provider_code"]).itertuples()))
    fails = [r for r in K.rows if not r[1]]
    print("\n%d checks, %d failed" % (len(K.rows), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else HERE.parent / "target"))
