"""task197 architecture 2 pack builder: writes target/, generator/figures.json and metadata.json."""
import os, sys, json, shutil, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import sim, world, cases, market, antidotes, docs, pack
import analysis as an

TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
CODE_OF = {v: k for k, v in world.PRODUCT_CODE.items()}
MTIME = dt.datetime(2026, 11, 2, 18, 30).timestamp()


def write_pack(truth):
    if os.path.isdir(TGT):
        shutil.rmtree(TGT)
    os.makedirs(TGT)
    rows = cases.build(truth, sim.SEED + 101)
    docs.write_csv(os.path.join(TGT, pack.CASES), cases.COLUMNS, rows)
    rev, pre, totals, per = market.build(truth, sim.SEED + 202)
    head = ["period_ending", "period", "upc", "item_description", "channel", "units", "dollars"]
    docs.write_csv(os.path.join(TGT, pack.POS_REV), head, rev)
    docs.write_csv(os.path.join(TGT, pack.POS_PRE), head, pre)
    docs.register(os.path.join(TGT, pack.REGISTER), sim.PRODUCTS)
    docs.centers(os.path.join(TGT, "network/member_centers.csv"))
    docs.procedure(os.path.join(TGT, "packaging_review/crp_referral_procedure_issue4.pdf"))
    docs.call_letter(os.path.join(TGT, "packaging_review/call_for_referrals_2027_review.pdf"))
    anti = antidotes.simulate(sim.SEED + 303 + 4000)
    docs.write_csv(os.path.join(TGT, "hospitals/antidote_preparations_2024-07_2026-10.csv"),
                   ["hospital_code", "prepared_local", "product", "dose_mg", "diluent", "prepared_by"],
                   antidotes.rows(anti, sim.SEED + 304))
    docs.hospitals(os.path.join(TGT, "hospitals/network_hospitals.csv"))
    docs.census(os.path.join(TGT, "census/population_age_0_5_by_state.csv"), sim.SEED + 405)
    docs.adverse_events(os.path.join(TGT, "packaging_review/adverse_event_reports_watched_products.csv"), sim.SEED + 406)
    for root, _, files in os.walk(TGT):
        for f in files:
            os.utime(os.path.join(root, f), (MTIME, MTIME))
    return rows, totals, per, anti


def routes(series, change):
    ck = an.mkey(change)
    pre = list(range(an.mkey(sim.EXPORT_FROM), ck))
    post = list(range(ck + 1, ck + 13))
    pre12 = list(range(ck - 12, ck))
    L, h, nll = an.fit_drain(series, pre)
    obs, cf, eff = an.effect_stock(series, pre, post, L, h)
    lo, hi = an.profile_interval(series, pre, L, nll)
    fam = {"fit": eff}
    for nm, LL in (("drain_low", lo), ("drain_high", hi)):
        hh, _ = an.fit_hazard(series, pre, LL)
        fam[nm] = an.effect_stock(series, pre, post, LL, hh)[2]
    Lg, hg, ng = an.fit_drain(series, pre, kind="gamma")
    Lb, hb, nb = an.fit_drain(series, pre, kind="box")
    Lq, hq, _ = an.fit_drain(series, pre, grain="quarter")
    if ng - nll < 2.0:                     # a kernel the pre-change record does not refute
        fam["gamma"] = an.effect_stock(series, pre, post, Lg, hg, kind="gamma")[2]
    if nb - nll < 2.0:
        fam["box"] = an.effect_stock(series, pre, post, Lb, hb, kind="box")[2]
    fam["quarterly"] = an.effect_stock(series, pre, post, Lq, hq)[2]
    gamma_eff = an.effect_stock(series, pre, post, Lg, hg, kind="gamma")[2]
    box = an.effect_stock(series, pre, post, Lb, hb, kind="box")[2]
    bt = an.backtest(series, pre[:-12], pre[-12:])
    return dict(L=L, L_low=lo, L_high=hi, obs=obs, cf=cf, effect=eff, family=fam, dnll_gamma=ng - nll, gamma=gamma_eff,
                dnll_box=nb - nll, box=box, L_box=Lb,
                per_sold=an.effect_per_sold(series, post, pre12), raw=an.effect_raw(series, post, pre12),
                trailing=an.effect_trailing(series, post, pre12), its=an.effect_its(series, pre, post),
                backtest=dict(stock=bt["stock"], per_sold=bt["sold"], its=bt["its"], L=bt["L"], n=bt["n"]),
                pre_months=len(pre), window=[sim.key_to_date(post[0]).isoformat()[:7],
                                             sim.key_to_date(post[-1]).isoformat()[:7]])


def main():
    truth = sim.simulate(sim.TRUTH_SEED)
    rows, totals, per, anti = write_pack(truth)
    prod, changes, ser = pack.series(TGT, sim.DAY0)
    eff = {}
    for pc, change in sorted(changes.items()):
        code = CODE_OF[pc]
        eff[code] = routes(ser[pc], change)
        eff[code]["product"] = prod[pc]["name"]
        eff[code]["product_code"] = pc
        eff[code]["change"] = change.isoformat()
    order = sorted(eff, key=lambda c: -eff[c]["effect"])
    call, runner = order[0], order[1]
    thr = docs.THRESHOLD
    pr = lambda x: round(x + 1e-12, 1)
    nac, dfo_c = antidotes.ask_truth(anti)
    F = {
        "call": eff[call]["product"], "call_code": call, "call_effect": pr(eff[call]["effect"]),
        "runner_up": eff[runner]["product"], "runner_up_code": runner, "runner_up_effect": pr(eff[runner]["effect"]),
        "gap": round(pr(eff[call]["effect"]) - pr(eff[runner]["effect"]), 1),
        "threshold": thr,
        "effects": [dict(product=eff[c]["product"], code=c, product_code=eff[c]["product_code"],
                         change=eff[c]["change"], window=eff[c]["window"], effect=pr(eff[c]["effect"]),
                         reaches=bool(eff[c]["effect"] >= thr), observed=eff[c]["obs"],
                         expected=round(eff[c]["cf"], 1)) for c in order],
        "antidote": [dict(hospital=h[0], name=h[1], half=lab, acetylcysteine_courses=nac[(h[0], lab)],
                          deferoxamine_courses=dfo_c[(h[0], lab)], antidote_courses=nac[(h[0], lab)] + dfo_c[(h[0], lab)])
                     for h in world.HOSPITALS for lab, _, _ in antidotes.ASK_HALVES],
        "detail": {c: {k: v for k, v in eff[c].items() if k not in ("product",)} for c in eff},
        "counts": {"case_rows": len(rows)},
        "procedure_sections_cited": ["2", "3.1", "3.2", "3.3", "4"],
    }
    json.dump(F, open(os.path.join(HERE, "figures.json"), "w"), indent=1, default=str)
    meta(F)
    print("call", call, F["call_effect"], "runner", runner, F["runner_up_effect"], "gap", F["gap"])
    for c in order:
        e = eff[c]
        print("%-4s eff %.3f fam %.3f-%.3f L %.1f (%.1f-%.1f) | sold %.3f raw %.3f trail %.3f its %.3f | box %.3f d%.0f | bt %.1f/%.1f/%.1f" % (
            c, e["effect"], min(e["family"].values()), max(e["family"].values()), e["L"], e["L_low"], e["L_high"],
            e["per_sold"], e["raw"], e["trailing"], e["its"], e["box"], e["dnll_box"],
            e["backtest"]["stock"], e["backtest"]["per_sold"], e["backtest"]["its"]))


def meta(F):
    files = []
    for root, _, fs in os.walk(TGT):
        for f in sorted(fs):
            p = os.path.relpath(os.path.join(root, f), TASK)
            files.append(p)
    src = {
        "target/network/case_export_watched_products.csv": ("%s case export: member centers' exposure cases involving the watched products, one row per substance line" % world.NETWORK, "calls recorded 1 January 2019 to 31 October 2026", "2026-11-02"),
        "target/network/member_centers.csv": ("%s member center list" % world.NETWORK, "the nine member centers", "2026-11-02"),
        "target/market/halcyon_pos_4wk_revised.csv": ("%s point-of-sale data, revised release" % world.PROVIDER, "four-week periods from January 2008, watched products' UPCs", "2026-11-02"),
        "target/market/halcyon_pos_4wk_preliminary.csv": ("%s point-of-sale data, preliminary release" % world.PROVIDER, "the latest four-week period", "2026-11-02"),
        "target/register/watched_products_register.xlsx": ("%s watched-product register" % world.NETWORK, "watched products and their packaging changes", "2026-10-30"),
        "target/packaging_review/crp_referral_procedure_issue4.pdf": ("%s referral procedure CRP-3, issue 4" % world.OFFICE, "the 2027 review", "2026-03-09"),
        "target/packaging_review/call_for_referrals_2027_review.pdf": ("%s call for referrals" % world.OFFICE, "the 2027 review", "2026-09-21"),
        "target/hospitals/antidote_preparations_2024-07_2026-10.csv": ("Network hospitals' pharmacy antidote preparation records, de-identified", "1 July 2024 to 31 October 2026", "2026-11-02"),
        "target/hospitals/network_hospitals.csv": ("%s hospital list" % world.NETWORK, "children's hospitals returning antidote records", "2026-11-02"),
        "target/census/population_age_0_5_by_state.csv": ("State population estimates, ages 0 to 5", "2019 to 2026", "2026-07-01"),
        "target/packaging_review/adverse_event_reports_watched_products.csv": ("%s adverse event reports for the watched products" % world.OFFICE, "2019 to 2026", "2026-10-15"),
    }
    M = {
        "task": "task197",
        "objective": "anomaly-detection",
        "domain": "pharmacology-pharmacoepidemiology-safety",
        "task_type": "safety-signal-detection",
        "as_of": sim.AS_OF.isoformat(),
        "decision": "which watched over-the-counter product, if any, the %s refers to the %s's 2027 Child-Resistant Packaging Review" % (world.NETWORK, world.OFFICE),
        "deliverables": ["packaging_referral.docx", "referral_tables.xlsx", "effects_chart.png"],
        "source": "synthetic. Every file is generated by task197/generator from a seeded simulation; no real organisation, product, person or record is represented.",
        "licence": "CC0-1.0 (synthetic data, generated for this task)",
        "generator": "task197/generator: python3 build.py, then goldens.py, submit.py and archive.py",
        "distractor_files": ["target/census/population_age_0_5_by_state.csv",
                             "target/packaging_review/adverse_event_reports_watched_products.csv"],
        "distractors": [
            {"path": "target/census/population_age_0_5_by_state.csv",
             "why_it_looks_relevant": "the number of young children in the network's states, which reads as the population at risk of an accidental exposure",
             "why_the_solution_never_reads_it": "the procedure's effect compares a product's own exposures with the number its packs would have produced, which no state population changes"},
            {"path": "target/packaging_review/adverse_event_reports_watched_products.csv",
             "why_it_looks_relevant": "the Office's own reports on the watched products, a second record of harm",
             "why_the_solution_never_reads_it": "the procedure counts the cases the network's member centers recorded, and these reports are a different system's"}],
        "files": [{"path": p, "format": p.rsplit(".", 1)[1], "source": src[p][0], "covers": src[p][1],
                   "issued_or_extracted": src[p][2], "licence": "CC0-1.0"} for p in files],
    }
    json.dump(M, open(os.path.join(TASK, "metadata.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
