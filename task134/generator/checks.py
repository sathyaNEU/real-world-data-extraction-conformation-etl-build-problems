"""Every assertion the design note's Build record asks for, on the shipped bundle (target/) and the generator's world.

    python3 task134/generator/checks.py
"""
import datetime as dt
import itertools
import json
import os
import re
import subprocess
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import askcalc as AC
import asktune as AT
import estimators as E
import golden as G
import readpack as RP
import sim
import tune
import world as W

TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
N = [0]
FAILS = []


def ok(cond, msg):
    N[0] += 1
    if not cond:
        FAILS.append(msg)
        print("FAIL  " + msg)
    else:
        print("ok    " + msg)


def r10(x):
    return np.floor(np.asarray(x) / 10.0 + 0.5) * 10


def same_bin(a, b):
    return bool(np.all(r10(a) == r10(b)))


def edge_dist(x):
    x = np.asarray(x)
    return np.abs(x - (np.floor(x / 10.0 + 0.5) * 10)) * -1 + 5


def doc_text():
    """the text of every document and workbook in the pack"""
    from pypdf import PdfReader
    import docx
    import openpyxl
    out = {}
    for f in sorted(os.listdir(TGT)):
        p = os.path.join(TGT, f)
        if f.endswith(".docx"):
            out[f] = "\n".join(x.text for x in docx.Document(p).paragraphs)
        elif f.endswith(".pdf"):
            out[f] = "\n".join(pg.extract_text() for pg in PdfReader(p).pages)
        elif f.endswith(".txt"):
            out[f] = open(p, encoding="utf-8").read()
        elif f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(p, read_only=True)
            out[f] = "\n".join(" ".join(str(v) for v in r if v is not None) for ws in wb.worksheets
                               for r in ws.iter_rows(values_only=True))
    return out


def main():
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    T, I, g, rungs, ask, counts, stops = G.compute(TGT)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    tot = g["total"]
    golden = tot

    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(TGT))
    ok(len(files) == 14, "input gate: 14 files (%d)" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(fmts) >= 3, "input gate: %d formats %s" % (len(fmts), sorted(fmts)))
    nl = len(T["li"])
    ok(nl >= 25000, "input gate: the spine fpnc_payment_lines has %d rows (25,000 or more)" % nl)
    ok(len(meta["distractors"]) >= 2 and all(d in files for d in meta["distractors"]),
       "input gate: %d distractors named in metadata.json and present" % len(meta["distractors"]))
    ok(not any("distractor" in f.lower() for f in files), "no file name says distractor")
    ok(set(meta["deliverables"]) == {G.XLSX, G.PNG}, "metadata names the two deliverables")
    # distractors unused: the golden and the ask recompute with them deleted
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp()
    for f in files:
        if f not in meta["distractors"]:
            shutil.copy(os.path.join(TGT, f), tmp)
    T2, I2, g2, _, ask2, _, _ = G.compute(tmp)
    shutil.rmtree(tmp)
    ok(np.allclose(g2["total"], tot) and np.allclose(AC.vec(ask2), AC.vec(ask)),
       "distractors deleted: the call and the 20 ask figures unchanged")
    offer_txt = doc_text()["nchc_draft_offer_2027-28.pdf"]
    ok("has not been agreed" in offer_txt, "the draft offer says it is not agreed (wrong-basis distractor ruled out)")
    draft_net = []
    for loc in W.LOCS:
        for ct, k in (("Residential", 0), ("Nursing", 1)):
            draft_net.append(ask[(loc, ct)][1] + W.NCHC_DRAFT_2027[k] - W.NCHC[2026][k])
    ok(np.all(np.abs(np.array(draft_net) - AC.vec(ask)[1::2]) >= 1.5), "the draft-offer read moves every net cell by 1.5 or more")

    # ---------------------------------------------------------------- the golden
    stated = np.array([figs["call"][q]["stated"] for q in W.QLABEL])
    ok(np.all(stated == r10(tot)), "figures.json carries the call as computed: %s" % stated.tolist())
    ok(np.all(edge_dist(tot) >= 2.0), "every golden figure at least 2.0 from a bin edge: %s" % np.round(edge_dist(tot), 2).tolist())
    ok(not np.any(stated % 50 == 0), "no golden figure a multiple of 50")
    ok(np.all(np.diff(tot) > 0), "the forecast rises through the year")

    # ---------------------------------------------------------------- the ladder
    for k in ("R0", "R1", "R1b", "R2", "R3", "R4"):
        ok(not np.allclose(rungs[k], tot, atol=0.5), "rung %s on its own vector %s" % (k, np.round(rungs[k], 1).tolist()))
    for k in ("R0", "R1", "R1b", "R2", "R3"):
        ok(tot[3] - rungs[k][3] >= 25, "rung %s at least 25 below at 31 March 2028 (%.1f)" % (k, tot[3] - rungs[k][3]))
    ok(rungs["R4"][3] - tot[3] >= 25, "rung R4 at least 25 above at 31 March 2028 (%.1f)" % (rungs["R4"][3] - tot[3]))
    ok(np.all(r10(rungs["R1"]) != r10(tot)), "the default R1 outside the golden's bin at every quarter end %s" % np.round(rungs["R1"], 1).tolist())
    ok(np.all(np.abs(rungs["R1"] - tot) >= 9), "the default at least 9 from the golden at every quarter end (thinnest %.1f)" % np.abs(rungs["R1"] - tot).min())
    vecs = [tuple(r10(rungs[k])) for k in ("R0", "R1", "R1b", "R2", "R3", "R4")] + [tuple(r10(tot))]
    ok(tuple(r10(tot)) not in vecs[:-1], "no rung lands on the golden's four stated figures")
    # the census trend agrees with the default (the cross-check the default files)
    ok(abs(rungs["R0"][3] - rungs["R1"][3]) < 15, "the census trend sits near the default (%.1f against %.1f)" % (rungs["R0"][3], rungs["R1"][3]))
    # conversions steady: the register's yearly conversions do not trend up
    cy = figs["conversions_by_year"]
    vals = [cy[str(y)] for y in range(2021, 2027)]
    ok(max(vals) - min(vals) <= 25 and len(set(vals)) == len(vals), "conversions by year steady and not identical %s" % vals)

    # ---------------------------------------------------------------- the golden family
    fam = [dict(lo=W.dn(dt.date(2022, 4, 1))), dict(lo=W.dn(dt.date(2023, 4, 1))), dict(lo=W.dn(dt.date(2022, 1, 1))),
           dict(lo=W.dn(dt.date(2023, 1, 1))), dict(band=3.0), dict(band=6.0), dict(step=0.25), dict(exits="care"),
           dict(clock="cal"), dict(sf_clock="award"), dict(post_asof_sf=True), dict(adm_window=(2021, 2026)),
           dict(adm_window=(2026, 2026)), dict(adm_window=(2022, 2026)), dict(cf_clock="entry"),
           dict(band=3.0, exits="care"), dict(step=0.25, clock="cal")]
    worst = 0
    for kw in fam:
        v = E.golden(I, **kw)["total"]
        worst = max(worst, np.abs(v - tot).max())
        ok(same_bin(v, tot) and np.all(edge_dist(v) >= 0.5),
           "golden family %s in the bin at every date %s" % (kw, np.round(v, 1).tolist()))
    print("      golden family: widest move %.2f" % worst)
    pa = E.golden(I, post_asof_sf=True)["total"]
    ok(abs(pa[3] - tot[3]) < 1.0, "self-funders admitted after the as-of date move 31 March 2028 by under 1 (%.2f)" % (pa[3] - tot[3]))
    # the competing-risk projection agrees with the true hazards' expectation within a bin
    S = sim.simulate(W.SEED)
    rec = json.load(open(os.path.join(HERE, "build_record.json")))
    tune.apply(S, [tuple(m) for m in rec["centring_moves"]])
    import observe as OB
    lag0 = OB.ask_attributes(S, None, np.random.default_rng(W.SEED + 404)).lag0
    unrec = int(((S.conv <= W.ASOF) & (S.conv + lag0 > W.EXTRACT) & (S.exit > W.ASOF)).sum())
    ok(int(sim.cf_on(S, W.ASOF).sum()) - unrec == g["n_cf"],
       "the as-of stock read from the files (%d) is the timeline's less the %d conversions not yet recorded" % (g["n_cf"], unrec))

    # ---------------------------------------------------------------- semantic forks
    defs = doc_text()["care_home_budget_definitions_2027-28.docx"]
    quotes = {
        "SF1": "Self-funding residents who receive free personal care or free nursing care payments are not council-funded residents",
        "SF2": "Respite, short-break and interim placements are excluded",
        "SF3": "in place at the end of that day",
        "SF4": "including residents temporarily in hospital and residents placed in care homes outside Strathallan",
        "SF5": "including residents temporarily in hospital",
        "SF7": "a decision recorded after a date but effective on or before it counts on that date",
        "SF8": "counted once",
        "SF12": "whenever they were admitted",
    }
    for k, q in quotes.items():
        ok(q in defs, "%s: the ruling sentence is in the budget definitions" % k)
    alt = {}
    # SF1: self-funders on free personal and nursing care counted as council-funded
    on = E.pool(I)
    o, HX, HC, HS = g["o"], g["HX"], g["HC"], g["HS"]
    d0 = E.months(I["sf_admit"][on], np.full(on.sum(), W.ASOF))
    qm = E.qmonths("days")
    sf_surv = np.array([np.exp(-(HX[0].H(d0 + q) - HX[0].H(d0))).sum() for q in qm])
    alt["SF1"] = tot + sf_surv
    # SF2: interim and respite placements kept
    I2, st2, _ = RP.inputs(T["pl"], T["li"], T["cw"], T["dl"], types=("PERM", "INT", "RESP"))
    I2["cf_route"] = np.where(I2["cf_route"] == "", "DIRECT", I2["cf_route"])
    alt["SF2"] = E.golden(I2)["total"]
    # SF3: anyone placed at any time in the quarter
    q0 = W.dn(dt.date(2026, 10, 1))
    e, x = I["cf_entry"], I["cf_exit"]
    extra = ((e <= W.ASOF) & (x > q0 - 1)).sum() - ((e <= W.ASOF) & (x > W.ASOF)).sum()
    alt["SF3"] = tot + extra
    # SF4: homes in Strathallan only
    regs = set(T["reg"]["service_no"])
    st = RP.stays(T["pl"], T["cw"], T["dl"])
    ooa = np.array([s["rows"][-1].service_no not in regs for s in st])
    I4 = {k: (v[~ooa] if k.startswith("cf_") else v) for k, v in I.items()}
    alt["SF4"] = E.golden(I4)["total"]
    # SF7: a conversion counted from the date it was recorded
    _, deb = RP.resolver(T["cw"])
    a = T["ass"]
    late = set()
    for r in a.itertuples(index=False):
        if r.outcome in ("ASSESSED", "NIL") and RP.day(r.completed) > W.ASOF and RP.day(r.effective_from) <= W.ASOF:
            late.add((deb.get(r.debtor_ref), RP.day(r.effective_from)))
    lateconv = np.array([(s["cl"], s["entry"]) in late and s["route"] == "CONV" for s in st])
    ok(lateconv.sum() >= 2, "SF7: %d conversions effective in December 2026 were recorded in January 2027" % lateconv.sum())
    I7 = {k: (v[~lateconv] if k.startswith("cf_") else v) for k, v in I.items()}
    alt["SF7"] = E.golden(I7)["total"]
    # SF12: today's residents and their survival only
    alt["SF12"] = g["survivors"]
    for k, v in alt.items():
        ok(not same_bin(v, tot), "%s: the alternative reading lands elsewhere %s and is refused by the quoted sentence" % (k, np.round(v, 1).tolist()))
    # SF5, SF6, SF8, SF9, SF10, SF11: the same call
    ok(set(T["pl"]["end_reason"]) <= {"", "FEE", "MOVE", "SVC", "DIED", "DISCH", "ENDED"}, "SF5: the register carries no absence episodes")
    perm = T["pl"][T["pl"]["placement_type"] == "PERM"]
    ok(set(perm["route"]) == {"DIRECT", "CONV"}, "SF6: every long-stay placement is one Strathallan funds (route DIRECT or CONV)")
    overl = 0
    by = {}
    for s in RP.stays(T["pl"], T["cw"], T["dl"], types=("PERM", "INT", "RESP")):
        by.setdefault(s["cl"], []).append((s["entry"], s["exit"]))
    for cl, ivs in by.items():
        ivs.sort()
        for (a1, b1), (a2, b2) in zip(ivs, ivs[1:]):
            if a2 < b1:
                overl += 1
    ok(overl == 0, "SF8: no person has two placements in place at the end of any day")
    ok([W.dd(q).isoformat() for q in W.QEND] == ["2027-06-30", "2027-09-30", "2027-12-31", "2028-03-31"], "SF9: the four dates")
    cut = "2026-12-31"
    late_dates = 0
    for col in ("admitted", "start_date", "end_date"):
        late_dates += (T["pl"][col] > cut).sum()
    for col in ("admitted", "award_start", "period_start", "period_end", "award_end"):
        late_dates += (T["li"][col] > cut).sum()
    late_dates += (T["dl"]["date_of_death"] > cut).sum()
    ok(late_dates == 0, "SF10: no admission, placement date, payment period or death after 31 December 2026")
    comp = np.array([[figs["components"][q][k] for k in ("today_residents", "direct_admissions", "conversions")] for q in W.QLABEL])
    ok(same_bin(np.round(comp).sum(axis=1), tot), "SF11: components rounded to whole residents first land in the same bins")

    # ---------------------------------------------------------------- C1 convergences
    evd = 0
    for col in ("start_date", "end_date", "admitted"):
        evd += (perm[col] == cut).sum()
    evd += ((T["li"]["award_end"] == cut)).sum()
    ok(evd == 0, "C1: nothing starts, ends or converts on 31 December 2026")
    li = T["li"]
    refs_per_client = {}
    for ref in li["debtor_ref"].unique():
        refs_per_client.setdefault(deb.get(ref, ref), set()).add(ref)
    ok(all(len(v) == 1 for v in refs_per_client.values()), "C1: one payment-line history per person (one pool member per person)")
    aw = li.groupby("debtor_ref").first()
    cf_end = {deb.get(r): RP.day(row["award_end"]) + 1 for r, row in aw.iterrows() if row["end_reason"] == "CF"}
    conv_st = [s for s in st if s["route"] == "CONV" and s["entry"] >= W.HIST_START + 120]
    linked = sum(1 for s in conv_st if cf_end.get(s["cl"]) == s["entry"])
    ok(linked == len(conv_st), "C1: every conversion since August 2021 links to one award ended for council funding (%d of %d)" % (linked, len(conv_st)))
    # no later-completed assessment takes effect before an earlier one, per person
    a = T["ass"][T["ass"]["outcome"] != "SELF"].copy()
    a["cl"] = [deb.get(r) for r in a["debtor_ref"]]
    bad = 0
    for cl, gg in a.groupby("cl"):
        gg = gg.sort_values("completed", kind="stable")
        e_ = list(gg["effective_from"])
        bad += sum(1 for p, q in zip(e_, e_[1:]) if q < p)
    ok(bad == 0, "C1: no later-completed assessment takes effect before an earlier one")
    # every ask resident has exactly one in-force assessment row selected
    con = AC.contributions(T["ass"], T["cw"])
    res = AC.residents(T["pl"], T["cw"], T["dl"])
    ok(all(r["cl"] in con for r in res), "every council-funded resident on 31 December 2026 has an assessment in force")

    # ---------------------------------------------------------------- Layer 1 slips priced on both paths
    slips = {
        "interim and respite kept": dict(types=("PERM", "INT", "RESP")),
        "stays not stitched": dict(stitch=False),
        "crosswalk not used": dict(use_crosswalk=False),
        "death linkage unread": dict(use_deaths=False),
    }
    for name, kw in slips.items():
        Is, sts, _ = RP.inputs(T["pl"], T["li"], T["cw"], T["dl"], **kw)
        Is["cf_route"] = np.where(Is["cf_route"] == "", "DIRECT", Is["cf_route"])
        rs = E.rungs(Is, RP.census(sts, RP.month_ends()))
        ok(np.all(r10(rs["R1"]) != r10(tot)), "slip '%s': the default %s stays outside the golden's bin" % (name, np.round(rs["R1"], 1).tolist()))
        print("      slip '%s': golden path %s" % (name, np.round(rs["golden"], 1).tolist()))
    for name, Ix in (("out-of-area dropped", I4), ("January-recorded conversions dropped", I7)):
        rs = E.rungs(Ix)
        ok(np.all(r10(rs["R1"]) != r10(tot)), "slip '%s': the default %s stays outside the golden's bin" % (name, np.round(rs["R1"], 1).tolist()))

    # ---------------------------------------------------------------- clean-data and lens-swap tests
    It = sim.truth_inputs(S)
    rt = E.rungs(It)
    ok(rt["golden"][3] - rt["R1"][3] >= 25, "clean-data test: on the true timeline with every Layer 1 device repaired the default %.1f and the golden %.1f stay apart" % (rt["R1"][3], rt["golden"][3]))
    ok(np.abs(rt["golden"] - tot).max() < 3, "clean-data test: the golden moves under 3 (%.2f)" % np.abs(rt["golden"] - tot).max())
    o_, HX_, _, _ = E.fit(I)
    A_, _ = E.survivors(I, o_, HX_)
    ok(np.allclose(A_.sum(axis=1), g["survivors"]), "lens swap: the default and the golden carry the same residents on the same dates; they differ only in the conversions")

    # ---------------------------------------------------------------- separation: the ask's columns and files never move the call
    Ts = {k: v.copy() for k, v in T.items()}
    rng = np.random.default_rng(5)
    Ts["pl"]["locality"] = rng.permutation(Ts["pl"]["locality"].values)
    Ts["pl"]["weekly_fee"] = rng.permutation(Ts["pl"]["weekly_fee"].values)
    Is, _, _ = RP.inputs(Ts["pl"], Ts["li"], Ts["cw"], Ts["dl"])
    ok(np.allclose(E.golden(Is)["total"], tot, atol=1e-9), "separation: scrambling the locality and fee columns leaves the call unchanged at full precision")
    mcw = Ts["cw"].copy()
    mcw.loc[mcw["merged_into"] != "", "debtor_ref"] = "399999999"
    Is, _, _ = RP.inputs(Ts["pl"], Ts["li"], mcw, Ts["dl"])
    ok(np.allclose(E.golden(Is)["total"], tot, atol=1e-9), "separation: the merged records' second debtor references do not move the call")
    # the ask does not read the payment lines (mirror sheet identical on the ask)
    Ta = {k: v for k, v in T.items()}
    Ta["li"] = T["li"].iloc[:0]
    ok(np.allclose(AC.vec(AC.compute(Ta)), AC.vec(ask)), "mirror: the ask is computed without the payment lines, so the default and the golden answer it alike")

    # ---------------------------------------------------------------- the ask: golden, stops, cracker sheet
    gv = AC.vec(ask)
    fr = np.abs(gv - np.round(gv))
    ok(np.all(fr <= 0.2), "every ask figure within 0.2 of its whole pound (mid-bin): worst %.2f" % fr.max())
    order, top = AC.chart(ask)
    gn = np.array([ask[(l, "Nursing")][1] for l in W.LOCS])
    ok(np.diff(np.sort(gn)).min() >= 1.0, "chart: no two nursing figures within 1 pound (%.2f)" % np.diff(np.sort(gn)).min())
    ok(figs["chart"]["order"] == order and figs["chart"]["title_locality"] == top, "chart order and title in figures.json")
    s1 = AC.vec(AC.compute(T, **AC.STOPS["s1"]))
    ok(np.all(np.abs(s1 - gv) >= 1.5), "cracker (s1): all 20 figures off by 1.5 or more (least %.2f)" % np.abs(s1 - gv).min())
    for k in ("s1", "s2", "o1"):
        o_k, t_k = AC.chart(AC.compute(T, **AC.STOPS[k]))
        ok(o_k != order and t_k != top, "chart under %s: order %s and title %s differ from the golden" % (k, o_k, t_k))
    s1n = s1[1::2]
    ok(np.all(np.round(s1n) != np.round(gv[1::2])), "cracker (s1): every chart value label differs")
    thr = {"s2": 1.2, "s3": 1.2, "o1": 1.2, "lazy": 2.0}
    for k, t in thr.items():
        v = AC.vec(AC.compute(T, **AC.STOPS[k]))
        ok(np.all(np.abs(v - gv) >= t), "stop %s: all 20 off by %.1f or more (least %.2f)" % (k, t, np.abs(v - gv).min()))
    v = AC.vec(AC.compute(T, **AC.STOPS["s5"]))
    ok(np.all(np.abs(v - gv)[1::2] >= 1.5), "stop s5 (schedule rate as the fee): every net cell off by 1.5 or more")
    v = AC.vec(AC.compute(T, **AC.STOPS["s4"]))
    d4 = np.abs(v - gv)
    idx = [W.LOCS.index(l) * 4 + j for l in ("Braeburn", "Dunmorrow") for j in range(4)]
    ok((d4[idx] >= 1.0).sum() >= 4 and np.allclose(np.delete(d4, idx), 0), "stop s4 (active registrations only): %d of the re-registered homes' locality cells off, no other cell moves" % (d4[idx] >= 1.0).sum())
    # necessity matrix
    need = {"placements_locality": 20, "assessments_latest": 20, "crosswalk_one_ref": 6, "register_active_only": 4,
            "lookup_unread": 20, "deaths_unread": 2, "definitions_interim_kept": 10, "codes_unread": 10}
    for k, n in need.items():
        v = AC.vec(AC.compute(T, **AC.NECESSITY[k]))
        moved = int((np.round(v) != np.round(gv)).sum())
        ok(moved >= n, "necessity: %s moves %d of 20 (target %d)" % (k, moved, n))
    # composed mishandlings
    worst_p, worst_h1 = 0, 0
    for sub in AT.SUBSETS:
        v = AC.vec(AC.compute(T, **AT.composite(sub)))
        kept = AC.kept(v, gv)
        if "primary" in sub:
            worst_p = max(worst_p, kept)
        elif "h1" in sub:
            worst_h1 = max(worst_h1, kept)
    ok(worst_p == 0, "composed: no mishandling that includes the primary keeps a figure")
    ok(worst_h1 <= 2, "composed: no mishandling that includes the latest-completed read keeps more than 2 (%d)" % worst_h1)
    # the pair ceiling at planning weights 38 / 7 / 55 over 31 criteria
    call_crit = 5
    mirror_call = sum(1 for k in range(4) if r10(rungs["R1"][k]) == r10(tot[k])) / call_crit
    cracker = 38 + 7 + 55 * 0 / 23
    mirror = 38 * mirror_call + 7 + 55 * 0 / 23
    pair = (cracker + mirror) / 2
    ok(pair <= 40, "pair ceiling %.1f at or under 40 (cracker %.1f, mirror %.1f)" % (pair, cracker, mirror))
    ok(pair + 55 / 20 <= 40, "pair ceiling with a twentieth of the ask weight each: %.1f" % (pair + 55 / 20))

    # ---------------------------------------------------------------- silence and realism
    texts = doc_text()
    banned = ["months since admission", "hazard", "competing", "cohort", "survival", "run rate", "depletion", "deplete",
              "kaplan", "aalen", "johansen", "cumulative incidence", "forecast", "distractor", "projection"]
    for f, t in texts.items():
        low = t.lower()
        hits = [b for b in banned if b in low]
        ok(not hits, "silence: %s carries none of the method words %s" % (f, hits))
    allt = "\n".join(texts.values())
    for f in files:
        if f.endswith((".csv", ".txt")):
            allt += open(os.path.join(TGT, f), encoding="utf-8").read()
    ok("—" not in allt and "–" not in allt, "no em or en dashes anywhere in the pack")
    # no file carries a forecast, a conversion count by year or a census
    hdrs = " ".join(pd.read_csv(os.path.join(TGT, f), nrows=0).columns.str.lower().str.cat(sep=" ") for f in files if f.endswith(".csv"))
    ok(not re.search(r"forecast|census|conversion", hdrs), "no column carries a forecast, a census or a conversion count")
    # realism: yearly flows are not identical, monthly streams not constant, headline totals not round
    pl = T["pl"]
    d_adm = pl[(pl["placement_type"] == "PERM") & (pl["route"] == "DIRECT")].drop_duplicates("admitted")
    st_ = [s for s in st if s["route"] == "DIRECT"]
    by_y = {}
    by_m = {}
    for s in st_:
        d = W.dd(s["entry"])
        if 2021 <= d.year <= 2026:
            by_y[d.year] = by_y.get(d.year, 0) + 1
            by_m[(d.year, d.month)] = by_m.get((d.year, d.month), 0) + 1
    yv = [by_y[y] for y in range(2022, 2027)]
    ok(len(set(yv)) == len(yv), "realism: direct admissions differ year to year %s" % yv)
    ok(len(set(by_m.values())) >= 8, "realism: monthly direct admissions vary (%d distinct counts)" % len(set(by_m.values())))
    ok(g["n_cf"] % 10 != 0 and g["n_sf"] % 10 != 0, "realism: the as-of stock (%d) and pool (%d) are not round" % (g["n_cf"], g["n_sf"]))
    ok(np.all(np.abs(gv - np.round(gv)) > 0.001), "realism: no ask average is a whole pound exactly")
    li_types = T["li"]["line_type"].value_counts()
    ok(set(li_types.index) == {"FPC", "FNC", "ADJ", "HOSP"}, "payment lines carry every line type %s" % dict(li_types))
    # containers: the fiction's authors and dates
    people = set(W.PEOPLE.values())
    card = json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task134.json")))
    ok(people <= set(card["world"]["people"]), "every persona is on the card (drawn with guard.py names)")
    for f in files:
        p = os.path.join(TGT, f)
        if f.endswith((".docx", ".xlsx")):
            core = zipfile.ZipFile(p).read("docProps/core.xml").decode()
            who = re.findall(r"<dc:creator>([^<]*)</dc:creator>", core) + re.findall(r"<cp:lastModifiedBy>([^<]*)</cp:lastModifiedBy>", core)
            ok(all(w in people for w in who), "%s: authors %s are the fiction's" % (f, who))
            stamps = re.findall(r"<dcterms:(?:created|modified)[^>]*>([^<]*)<", core)
            ok(all("2021" <= x[:10] <= "2027-01-18" for x in stamps), "%s: dates inside the fiction %s" % (f, stamps))
        if f.endswith(".pdf"):
            from pypdf import PdfReader
            m = PdfReader(p).metadata
            ok(m.get("/Author") in people and str(m.get("/CreationDate", "")).startswith("D:2026"), "%s: author %s and date %s" % (f, m.get("/Author"), m.get("/CreationDate")))
        mt = dt.datetime.fromtimestamp(os.path.getmtime(p), W.LON)
        ok(dt.datetime(2026, 4, 1, tzinfo=W.LON) <= mt <= dt.datetime(2027, 1, 19, tzinfo=W.LON), "%s: saved %s" % (f, mt.date()))

    print("\n%d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
