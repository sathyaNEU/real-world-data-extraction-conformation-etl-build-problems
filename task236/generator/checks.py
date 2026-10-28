"""task236 checks: the three rules executed on the simulator's clean truth (R1 to R3c), every semantic fork row (SF1 to
SF15), the golden against the world's own ascertainment with its margins, the rungs and the corridor of index
constructions, the ask devices and their stops, the cracker sheet (every careful reading of the asks' rows misses every
figure), the separation of the call from the devices and the main side frozen against the shipped pack, the
documents' pins, the input gates and the realism sweep."""
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

import asks as AK
import estim as E
import params as P

N = [0]
GOLD = {"FN", "MS", "MW", "SC"}
DEFAULT = {"CW", "MN", "MS", "MW", "NC", "SC", "TB"}          # positivity: four false flags, the Far North missed
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))


def ok(cond, label):
    assert cond, label
    N[0] += 1


def _pdf_text(path):
    from pypdf import PdfReader
    return " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(path).pages)


# ------------------------------------------------------------------ the clean truth: the world before any record
def clean(W):
    """tests and positives by region and week straight from the simulator, the sentinel practices' influenza-like
    illness and list sizes, and their swabs' influenza share, with no record written"""
    tc = W.test_counts.assign(week=[d.isocalendar()[1] for d in W.test_counts.date])
    T = tc.groupby(["region", "week"]).tested.sum()
    Pos = tc.groupby(["region", "week"]).positive.sum()
    pr = W.practices[W.practices.returned]
    rate = pr.groupby(["region", "week"]).ili.sum() / pr.groupby(["region", "week"]).list_size.sum() * 1e5
    sw = W.swabs.groupby(["region", "week"]).flu_positive.mean()
    return T, Pos, rate, sw


def truth_cases(R):
    """the cases the protocol defines, from the records' own positives (the person's address as drawn, the region the
    person was tested in for an unknown address), every result received by the pull"""
    rows = sorted([x for x in R.positives if x[2] <= P.PULL], key=lambda x: (x[0]["key"], x[1], x[2]))
    out, cur = [], None
    for person, d, rec, method, ftype, region, setting in rows:
        k = person["key"]
        if cur is None or cur["key"] != k or (d - cur["first"]).days >= 14:
            pc = person["postcode"]
            reg = R.region_of.get(pc) if pc not in ("", "0000") else region
            cur = dict(key=k, first=d, rec=rec, region=reg)
            out.append(cur)
        else:
            cur["rec"] = min(cur["rec"], rec)
    c = pd.DataFrame(out)
    c["week"] = [d.isocalendar()[1] for d in c["first"]]
    return c[c.region.notna()]


def main_rows(D):
    """the gateway results rows the call reads, by count and sha256: each of the eight regions' change window and the
    South West and Far West in weeks 26 to 35, a row placed by its residential postcode under the concordance in
    force or, with none recorded, by the requesting service's"""
    r = D["res"]
    now = E.concordance_now(D)
    unk = r.residential_postcode.isin(E.UNKNOWN)
    reg = r.residential_postcode.map(now).where(~unk, r.requester_postcode.map(now))
    wk = E.iso_week(r.collection_date)
    win = {c: set(range(cw - E.WINDOW, cw + E.WINDOW)) for c, (_, cw, _) in E.changes(D).items()}
    win.update({c: set(range(26, 36)) for c in ("SW", "FW")})
    m = r[[g in win and w in win[g] for g, w in zip(reg, wk)]].sort_values("result_id")
    return len(m), hashlib.sha256(m.to_csv(index=False, lineterminator="\n").encode()).hexdigest()


def run(target, golden, o, X):
    N[0] = 0
    W, R = o["W"], o["R"]
    D = X["D"]
    ch = X["changes"]
    import build as B
    files = {k: os.path.join(target, f) for k, f in B.FILES.items()}
    prot = _pdf_text(files["prot"])
    sprot = _pdf_text(files["sprot"])
    dic = open(files["dict"]).read()
    res, ret, sw = D["res"], D["ret"], D["sw"]
    flags, ratio = X["flags"], X["ratio"]

    # ------------------------------------------------------------ the golden
    ok(flags == GOLD, "golden: flag %s" % sorted(flags))
    truth = W.truth()
    ok(E.flagged(truth) == GOLD, "golden: the world's own ascertainment changes flag the same four regions")
    ok(all(abs(ratio[c] / truth[c] - 1) < 0.10 for c in E.EIGHT),
       "golden: every region's estimate within 10 per cent of the world's ascertainment change")
    margin = min(min(abs(v / 1.25 - 1), abs(v / 0.75 - 1)) for v in ratio.values())
    ok(margin >= 0.15, "golden: every region 15 per cent or more from the line (%.3f)" % margin)
    ok({c: round(v, 2) for c, v in ratio.items() if c not in GOLD} == {"NC": 1.01, "TB": 1.0, "CW": 1.0, "MN": 0.99},
       "golden: the four unflagged regions within 0.01 of no change")

    # ------------------------------------------------------------ R1: the field's raw material ships, no deciding column
    banned = re.compile(r"case|episode|flag|share|index|ratio|positiv|ili_rate|rate|ascertain", re.I)
    for k in ("res", "ret", "sw", "conc", "pop", "svc"):
        cols = pd.read_csv(files[k], nrows=1).columns
        ok(not [c for c in cols if banned.search(c)], "R1 no column of %s holds a case, a rate, a share or a flag" % B.FILES[k])
    ok(len(res) >= 200_000 and res.patient_key.nunique() > 100_000,
       "R1 the gateway's results ship row by row (%d results, %d people)" % (len(res), res.patient_key.nunique()))
    ok(len(ret) == sum(P.SENTINEL_PRACTICES.values()) * 23 and len(sw) > 15_000,
       "R1 the sentinel returns ship by practice and week (%d) and the protocol swabs one by one (%d)" % (len(ret), len(sw)))
    ok(X["N"].sum() == len(X["cases"][X["cases"].notified_utc <= E.CUTOFF_UTC]),
       "R1 the golden's series counts the cases it builds from the results")

    # ------------------------------------------------------------ R3a: the analyst test on the clean truth
    T, Pos, rate, swp = clean(W)
    pos_truth = E.share_change(Pos, T, ch)
    ok(E.flagged(pos_truth) == DEFAULT, "R3a positivity on the clean truth flags %s" % sorted(E.flagged(pos_truth)))
    rg = E.rungs(D, X["N"], ch)
    ok(E.flagged(rg["positivity"]) == DEFAULT, "R3a positivity on the pack flags the same seven regions")
    ok(len(E.flagged(rg["positivity"]) ^ GOLD) == 4 + 1, "R3a the default path files 5 of the 8 regions wrong")
    ok(E.flagged(rg["notified_per_test"]) == DEFAULT, "R3a notified cases per test flag the same seven")
    ok(all(rg["positivity"][c] > 1.55 for c in ("NC", "TB", "CW", "MN")) and 0.85 < rg["positivity"]["FN"] < 1.15,
       "R3a positivity rises 1.55 times or more in the four unchanged regions and moves under 15 per cent in the Far North")
    # ------------------------------------------------------------ R3b: the decisive step alone, and the lower rungs
    gold_truth = E.share_change(Pos, (rate * swp).dropna(), ch)
    ok(E.flagged(gold_truth) == GOLD, "R3b positives against the sentinel index on the clean truth: the golden")
    ok(len(E.flagged(E.share_change(Pos, rate, ch)) ^ GOLD) == 4, "R3b against the ILI rate alone (clean truth): 4 wrong")
    ok(len(E.flagged(E.share_change(Pos, swp, ch)) ^ GOLD) == 4, "R3b against swab positivity alone (clean truth): 4 wrong")
    ok(E.flagged(rg["per_ili_rate"]) == set(E.EIGHT) and E.flagged(rg["per_swab_positivity"]) == set(E.EIGHT),
       "R3b on the pack: notifications per ILI rate and per swab positivity flag all eight")
    ok(len(E.flagged(rg["raw"]) ^ GOLD) == 5 and len(E.flagged(rg["against_unchanged_regions"]) ^ GOLD) == 5,
       "rungs: raw notifications and the comparison with the unchanged South West and Far West file 5 wrong each")
    ok(sum(1 for k, v in rg.items() if E.flagged(v) == GOLD) == 0, "rungs: no easy route lands the golden")

    # ------------------------------------------------------------ R2 and the corridor: each mess item and each construction
    cor = E.corridor(D, ch)
    for name, v in cor.items():
        ok(E.flagged(v) == GOLD, "R2/C3 %s: same call" % name)
    ok(min(min(abs(v[c] / 1.25 - 1), abs(v[c] / 0.75 - 1)) for v in cor.values() for c in E.EIGHT) >= 0.10,
       "C3 every construction keeps every region 10 per cent or more from the line")
    base = X["cases"]
    Xi = X["X"]
    for name, kw in (("residents of other states counted where tested", dict(interstate="requester")),
                     ("0000 read as a postcode outside the state", dict(unknown="blank_only")),
                     ("one case per person", dict(anchor="person"))):
        ok(E.flagged(E.share_change(E.series(E.cases(D, **kw)), Xi, ch)) == GOLD, "R2 %s: same call" % name)
    r2 = D["ret"].copy()
    r2.loc[r2.return_status != "received", ["consultations", "ili_consultations"]] = "0"
    r2["return_status"] = "received"
    ok(E.flagged(E.share_change(X["N"], E.index(*E.sentinel(dict(D, ret=r2))), ch)) == GOLD,
       "R2 returns not received read as no influenza-like illness: same call")
    s2 = D["sw"].copy()
    s2.loc[s2.influenza_a == "", ["influenza_a", "influenza_b"]] = "not detected"
    ok(E.flagged(E.share_change(X["N"], E.index(*E.sentinel(dict(D, sw=s2))), ch)) == GOLD,
       "R2 untested swabs read as negative: same call")
    r3 = D["ret"].copy()
    first = r3[r3.iso_week.astype(int) == 14].set_index("practice_code").list_size
    r3["list_size"] = r3.practice_code.map(first)
    ok(E.flagged(E.share_change(X["N"], E.index(*E.sentinel(dict(D, ret=r3))), ch)) == GOLD,
       "R2 the April list sizes kept through the July quarter: same call")
    ok((r3.list_size != D["ret"].list_size).sum() > 100, "R2 the July quarter revised list sizes")
    ok(E.flagged(E.share_change(X["N"], Xi, ch, how="weekly")) == GOLD, "C3 the mean of the weekly ratios: same call")

    # ------------------------------------------------------------ the semantic fork table, every row
    conf_only = E.cases(dict(D, res=res[res.method != "rapid antigen"]))
    ok(E.flagged(E.share_change(E.series(conf_only), Xi, ch)) != GOLD,
       "SF1 confirmed cases only would change the call; ruled out by s.2 (the series count confirmed and probable cases)")
    ok("the notified series count confirmed and probable cases" in prot, "SF1 pinned in CDB-FLU-03 s.2")
    ok(E.flagged(E.share_change(E.series(E.cases(D, anchor="rolling")), Xi, ch)) == GOLD
       and "within 14 days of the collection of a case's first positive specimen" in prot,
       "SF2 episodes anchored on the first or the previous positive: same call; s.2 anchors on the first")
    nw = base.assign(week=E.iso_week(pd.to_datetime(base.notified_utc.str.slice(0, 19)) + pd.Timedelta(hours=10)))
    ok(E.flagged(E.share_change(E.series(nw), Xi, ch)) == GOLD
       and "report week of its first positive specimen's collection date" in prot,
       "SF3 cases by week of notification instead of collection: same call; s.2 pins collection")
    ok(E.flagged(E.share_change(E.series(E.cases(D, asof=True)), Xi, ch)) == GOLD
       and "under the postcode concordance in force at the report" in prot,
       "SF4 regions as at collection or at the report: same call (no moved postcode in any window); s.2 pins the report")
    ok("Residents of other states are not counted" in prot and "counted in the region of the requesting service's postcode" in prot,
       "SF5 residents of other states and cases without a postcode pinned in s.2 (same call either way, R2)")
    late = base[base.notified_utc > E.CUTOFF_UTC]
    ok(late.week.eq(36).all() and len(late) > 100,
       "SF6 every case notified after the cut-off is a week 36 case (%d): every window is complete either way" % len(late))
    ok("09:00 on the Monday after its report week" in prot, "SF6 the cut-off pinned in s.2")
    alt = {}
    for code, (_, cw, _) in ch.items():
        b, a = list(range(cw - 4, cw)), list(range(cw + 1, cw + 5))
        alt[code] = (E.window_sum(X["N"], code, a) / E.window_sum(Xi, code, a)) / (
            E.window_sum(X["N"], code, b) / E.window_sum(Xi, code, b))
    ok(E.flagged(alt) == GOLD and "four report weeks from the week of the change with the four report weeks before it" in prot,
       "SF7 the four weeks from the week after the change: same call; s.4 pins the change week")
    ok(E.flagged(ratio, down=0.8) == GOLD and "raised or lowered the share" in prot
       and "by more than a quarter of its level before the change" in prot,
       "SF8 a quarter of the level before, either way; a quarter down read as 0.80 (a quarter up undone): same call")
    ok("Infections count whether or not the person sought care or was tested" in prot,
       "SF9 the population is every infection, seen or not (s.4)")
    reg = D["reg"]
    late_changes = reg[(reg.effective_date >= dt.date(2027, 7, 1)) & (reg.effective_date <= dt.date(2027, 8, 31))]
    ok(sorted(late_changes.region_code) == sorted(E.EIGHT) and len(reg) == 11,
       "SF10 the register's entries in late July and August are the eight regions, one each; the three earlier are not")
    ok(all(d.weekday() == 0 for d, _, _ in ch.values()), "SF11 every change takes effect on a Monday: its report week is plain")
    ok(all(abs(abs(v - 1) - 0.25) > 0.15 for v in ratio.values()), "SF12 compared unrounded or at two decimals: same call")
    ok(E.flagged(E.share_change(E.series(E.cases(D, finals_only=True)), Xi, ch)) == GOLD
       and "the gateway receives the first result reporting influenza for it" in prot,
       "SF13 final reports only for the call: same call; s.2 notifies on the first result reporting influenza")

    # ------------------------------------------------------------ the asks: fair, devices, stops
    tc = truth_cases(R)
    tA = tc[(tc.rec <= P.CUTOFF) & tc.week.between(14, 36)].groupby("region").size().reindex(E.EIGHT).to_dict()
    ok(tA == X["season"], "ask A fair: the golden equals the season to date of the world's own cases")
    pops = {r[0]: r[2] for r in P.REGIONS}
    n36 = tc[(tc.rec <= P.CUTOFF) & (tc.week == 36)].groupby("region").size()
    ok(all(E.round_half(n36[c] / pops[c] * 1e5) == X["rate36"][c] for c in E.EIGHT),
       "ask B fair: the world's week 36 cases over the regions' populations give the golden")
    ok(all(abs(X["erp"][c] - pops[c]) == 0 for c in E.EIGHT), "ask B: the concordance in force sums each region's ERP")
    A, Bs = E.ask_stops(D)
    gA, gB = X["season"], X["rate36"]
    for name in ("regions as at collection", "final reports only", "episodes anchored on the previous positive",
                 "cases without a postcode left out", "no cut-off", "cut-off read as 09:00 UTC",
                 "residents of other states counted where tested"):
        ok(all(A[name][c] != gA[c] for c in E.EIGHT), "ask A stop: %s moves all eight regions" % name)
    ok(sum(A["0000 read as a postcode outside the state"][c] != gA[c] for c in E.EIGHT) >= 4,
       "ask A hazard: 0000 read as outside the state moves the regions Northgate and Southern Districts serve")
    ok(all(A["final reports only"][c] < gA[c] for c in E.EIGHT) and all(A["no cut-off"][c] > gA[c] for c in E.EIGHT),
       "ask A: final reports alone read every region low, no cut-off every region high")
    for name in ("final reports only", "no cut-off", "cut-off read as 09:00 UTC", "cases without a postcode left out",
                 "population on the old boundaries"):
        ok(all(Bs[name][c] != gB[c] for c in E.EIGHT), "ask B stop: %s moves all eight regions" % name)
    ok(all(Bs["final reports only"][c] <= gB[c] - 0.25 for c in E.EIGHT),
       "ask B primary: final reports alone read every region 0.3 per 100,000 or more low")
    ok(sum(Bs["every concordance row summed"][c] != gB[c] for c in E.EIGHT) == 4,
       "ask B hazard: every concordance row summed moves the four regions that lost a postcode")
    ok(all(abs((X["rate36_raw"][c] * 10) % 1 - 0.5) >= 0.15 for c in E.EIGHT),
       "ask B: every rate 0.015 per 100,000 or more from a rounding edge")
    prelim = res[res.result_status == "P"]
    ok(len(prelim) > 5000 and prelim.result.str.contains("prelim|interim|PRELIM", regex=True).all(),
       "ask B device: %d preliminary reports, each worded as one by its laboratory" % len(prelim))
    fin_spec = set(res[res.result_status == "F"].specimen_id)
    ok(prelim.specimen_id.isin(fin_spec).mean() > 0.9, "ask B device: nine in ten preliminary reports already have a final")
    ok(not re.search(r"prelim|interim|final report", prot, re.I), "ban 1: the protocol names no preliminary or final report")
    moved = D["conc"][D["conc"].effective_to != ""]
    ok(sorted(set(moved.region_code) | set(D["conc"][D["conc"].postcode.isin(moved.postcode) & (D["conc"].effective_to == "")].region_code))
       == sorted(E.EIGHT), "ask A primary: the 28 June boundary review touches all eight regions")
    # ------------------------------------------------------------ separation: no device row in the call's windows
    straddle = base[(base.notified_utc <= E.CUTOFF_UTC)].merge(
        E.cases(D, finals_only=True)[["person", "first_collection", "notified_utc"]],
        on=["person", "first_collection"], how="left", suffixes=("", "_final"))
    straddle = straddle[straddle.notified_utc_final.isna() | (straddle.notified_utc_final > E.CUTOFF_UTC)]
    win = {(c, w) for c, (_, cw, _) in ch.items() for w in range(cw - 4, cw + 4)}
    ok(not any((r.region, r.week) in win for r in straddle.itertuples()) and len(straddle) > 40,
       "separation: the %d cases whose final report came after the cut-off are all outside the call's windows" % len(straddle))
    ok(not any((r.region, r.week) in win for r in late.itertuples()), "separation: no case notified after the cut-off is in a window")
    pre = base[base.postcode.isin(set(moved.postcode)) & (base.first_collection <= moved.effective_to.max())]
    ok(len(pre) >= 15 and pre.week.max() < 26, "separation: the %d cases in moved postcodes before the boundary are all before week 26" % len(pre))

    # ------------------------------------------------------------ the asks' rows (asks.py): the person matching and the
    # laboratories' two reporting systems, on people outside every change window
    man, res0 = o["man"], o["res0"]
    for kind in AK.KINDS:
        want = sum(sum(n for _, n in v[kind]) if kind == "address" else sum(v[kind]) for v in P.ASK_PLAN.values())
        ok(len(man[kind]) == want, "asks' rows: %d of %d planned %s instances placed" % (len(man[kind]), want, kind))
    elig = set(AK.eligible(res0, R).patient_key)
    changed = (o["res"] != res0).any(axis=1)
    touched = set(res0.loc[changed, "patient_key"])
    named = ({m["key"] for k in ("two_keys", "birthday", "address") for m in man[k]} | {m["infant"] for m in man["infant"]})
    ok(named <= touched <= elig, "separation: the %d changed rows belong to %d people, every one with each result "
       "outside its region's change window and at the gateway by the cut-off" % (changed.sum(), len(touched)))
    ok(touched <= elig and not (touched & set(base[base.notified_utc > E.CUTOFF_UTC].patient_key)),
       "separation: no changed row belongs to a case in a window or to a case notified after the cut-off")
    ok(res0.groupby("specimen_id").patient_key.nunique().max() == 1 and res0.groupby("patient_key").age_years.nunique().max() == 1,
       "asks' rows: before them every specimen sits under one key and every key shows one age")
    two = res.groupby("specimen_id").patient_key.nunique()
    two = two[two > 1]
    ok(sorted(two.index) == sorted(m["specimen"] for m in man["two_keys"]) and (two == 2).all(),
       "two keys: the %d specimens under two keys are the instances, no other" % len(two))
    pf = res[res.specimen_id.isin(two.index)]
    ok(all(set(x[x.result_status == "P"].patient_key) == {m["key"]} and set(x[x.result_status == "F"].patient_key) == {m["key2"]}
           and x.sex.nunique() == x.age_years.nunique() == x.residential_postcode.nunique() == 1
           for m in man["two_keys"] for x in [pf[pf.specimen_id == m["specimen"]]]),
       "two keys: each a preliminary under one key and its final under another, same sex, age and residential postcode")
    ages = res.groupby("patient_key").age_years.agg(lambda s: sorted({int(v) for v in s}))
    multi = ages[ages.map(len) > 1]
    moms, bdays = {m["mother"] for m in man["infant"]}, {m["key"] for m in man["birthday"]}
    ok(set(multi.index) == moms | bdays, "the %d keys showing two ages are the infants' mothers and the birthdays" % len(multi))
    ok(all(multi[k][0] == 0 and multi[k][1] >= 19 for k in moms) and all(multi[k][1] - multi[k][0] == 1 for k in bdays),
       "infant: each mother's key shows an infant of 0 and an adult of 19 or more; birthday: each age rises by one")
    now = E.concordance_now(D)
    ad = res[res.specimen_id.isin({m["specimen"] for m in man["address"]})]
    ok(all(x[x.result_status == "P"].residential_postcode.isin(E.UNKNOWN).all()
           and x[x.result_status == "F"].residential_postcode.map(now).eq(m["region"]).all()
           and x.requester_postcode.map(now).eq(m["to"]).all() and m["to"] != m["region"]
           for m in man["address"] for x in [ad[ad.specimen_id == m["specimen"]]]),
       "address: each preliminary has no residential postcode, its final has one in the region, the requester sits in "
       "the next region")
    flow = {c: sum(m["to"] == c for m in man["address"]) - sum(m["region"] == c for m in man["address"]) for c in E.EIGHT}
    ok(all(flow[c] for c in E.EIGHT), "address: every region's net of cases sent from a requester next door is non-zero %s" % flow)

    # ------------------------------------------------------------ the main side frozen against the shipped pack
    shipped = json.load(open(os.path.join(HERE, "shipped.json")))
    for f, h in shipped["files"].items():
        if f != B.FILES["res"]:
            ok(hashlib.sha256(open(os.path.join(target, f), "rb").read()).hexdigest() == h,
               "frozen: %s byte-identical to the shipped pack" % f)
    ok(hashlib.sha256(res0.to_csv(index=False, lineterminator="\n").encode()).hexdigest() == shipped["files"][B.FILES["res"]],
       "frozen: the gateway's results before the asks' rows are the shipped file byte for byte")
    n_main, h_main = main_rows(D)
    ok((n_main, h_main) == (shipped["main_rows"], shipped["main_rows_sha256"]),
       "frozen: the %d results rows the call reads byte-identical to the shipped pack" % n_main)
    names = {r[0]: r[1] for r in P.REGIONS}
    comp = shipped["call"]["components"]
    ok(sorted(names[c] for c in flags) == sorted(shipped["call"]["flags"])
       and all([X["windows"][c]["before"], X["windows"][c]["after"]] == comp["notified_before_after"][names[c]]
               and "%.2f" % round(ratio[c], 2) == comp["share_notified_after_over_before"][names[c]] for c in E.EIGHT),
       "frozen: the four flags, each region's notified cases either side of its change and its share-notified change as shipped")
    ok(all(X["season"][c] == shipped["asks"][c]["season_to_date"] and "%.1f" % X["rate36"][c] == shipped["asks"][c]["rate_week36"]
           for c in E.EIGHT), "the asks' golden figures as shipped: the asks' rows move no case in the clean truth")

    # ------------------------------------------------------------ the cracker sheet: every careful reading misses, and
    # no reading moves the call (SF14, SF15)
    for name, c in E.readings(D).items():
        a, b = E.season_to_date(c), E.week_rate(c, X["erp"])
        ok(all(a[k] != gA[k] for k in E.EIGHT) and all(abs(b[k] - gB[k]) >= 0.05 for k in E.EIGHT),
           "cracker sheet: %s misses all sixteen figures" % name)
        Nr = E.series(c)
        ok(E.flagged(E.share_change(Nr, Xi, ch)) == GOLD and all(
            int(E.window_sum(Nr, k, E.windows(cw)[0])) == X["windows"][k]["before"]
            and int(E.window_sum(Nr, k, E.windows(cw)[1])) == X["windows"][k]["after"] for k, (_, cw, _) in ch.items()),
           "SF14/SF15 %s: the same call and the same notified cases in every window" % name)

    # ------------------------------------------------------------ the documents
    sec4 = prot[prot.index("4. Testing-change break flags"):prot.index("5. Weekly checks")]
    ok(not re.search(r"sentinel|positiv|per test|swab|consultation|index|estimat", sec4, re.I),
       "s.4 files the share and names no way of estimating a region's infections")
    ok(not re.search(r"ascertain|share of infections|estimat|notified cases", sprot, re.I),
       "the sentinel protocol relates its figures to no notification count")
    ok("are not notified" in sprot and "the first two patients with ILI on each day it is open, up to ten in a week" in sprot,
       "the sentinel protocol: swabs not notified, swabbed to a fixed protocol")
    ok("blank, or 0000 at some services" in dic and "P for a preliminary report, F for a final report" in dic,
       "the dictionary describes the unknown postcodes and the report status flatly")
    ok(not re.search(r"first result|notif", dic.split("## sentinel")[0].split("| result_status")[1][:200], re.I),
       "the dictionary's result_status line says nothing of notification")

    # ------------------------------------------------------------ R3c, input gates, dates
    names = os.listdir(target)
    ok(len(names) >= 10 and len({f.rsplit(".", 1)[1] for f in names}) >= 3,
       "input gates: %d files, formats %s" % (len(names), sorted({f.rsplit(".", 1)[1] for f in names})))
    ok(max(sum(1 for _ in open(os.path.join(target, f))) for f in names if f.endswith(".csv")) >= 25_001,
       "input gate: a file of 25,000 rows or more")
    ok(res.received_utc.max() <= "2027-09-13T20:30:00Z" and res.collection_date.max() <= "2027-09-12",
       "no result after the extract, no specimen after week 36")
    ok(sw.collection_date.max() <= "2027-09-12" and ret.iso_week.astype(int).max() == 36, "sentinel data to week 36")
    for f in B.DISTRACTORS:
        ok(os.path.exists(files[f]), "distractor %s ships; the golden and both asks read none of it" % B.FILES[f])
    for path in (os.path.join(os.path.dirname(target), x) for x in ("submission.md", "DESIGN_NOTE.md", "prompt.txt")):
        if os.path.exists(path):
            ok("\u2014" not in open(path).read(), "no em dash in %s" % os.path.basename(path))
    for f in names:
        if f.endswith((".md", ".csv")):
            ok("\u2014" not in open(os.path.join(target, f)).read(), "no em dash in %s" % f)
    weekly = {c: tuple(int(X["N"].get((c, w), 0)) for w in range(14, 37)) for c in E.EIGHT + ["SW", "FW"]}
    ok(len(set(weekly.values())) == len(weekly), "R3c no two regions share a weekly series")

    # ------------------------------------------------------------ the pack's own registers (H9)
    readme = open(files["readme"]).read()
    listed = set(re.findall(r"`([^`]+\.(?:csv|xlsx|pdf|md))`", readme))
    ok(listed == set(names) - {"README.md"}, "H9 the readme lists every shipped file and nothing else")
    data_files = {f for f in names if f.endswith((".csv", ".xlsx"))}
    ok(data_files == set(re.findall(r"^## (\S+\.(?:csv|xlsx))$", dic, re.M)), "H9 the dictionary describes every data file")
    for path in (os.path.join(os.path.dirname(target), "submission.md"),):
        if os.path.exists(path):
            cited = set(re.findall(r"[\w.-]+\.(?:csv|xlsx|pdf)", open(path).read())) - {"influenza_testing_break_flags_week36_2027.xlsx"}
            ok(cited <= set(names), "H8 every file the write-up cites ships: %s" % sorted(cited - set(names)))

    # ------------------------------------------------------------ realism sweep
    for k in ("res", "ret", "sw", "conc", "pop"):
        df = D[k]
        const = [c for c in df.columns if df[c].nunique() == 1]
        ok(not const, "realism: no constant column in %s" % B.FILES[k])
    runs = 0
    for c, s in weekly.items():
        runs += sum(1 for i in range(len(s) - 2) if s[i] == s[i + 1] == s[i + 2] and s[i] > 5)
    ok(runs == 0, "realism: no region's weekly cases repeat three weeks running")
    daily = res.collection_date.value_counts().values
    ok(len(set(daily)) > 0.95 * len(daily), "realism: daily result counts vary")
    ok(len(base) % 100 and sum(X["season"].values()) % 100, "realism: no round headline total")
    card = json.load(open(os.path.join(REPO, ".claude", "skills", "fingerprint", "cards", "task236.json")))
    ok(set(P.PEOPLE.values()) == set(card["world"]["people"]), "realism: every persona drawn by guard.py names")
    scrub = os.path.join(REPO, ".claude", "skills", "reduce-house-fixes", "scripts", "scrub_producer_metadata.py")
    for folder in (target, golden):
        out = subprocess.run([sys.executable, scrub, folder], capture_output=True, text=True).stdout
        ok("clean, no producer signature" in out, "realism: containers scrubbed in %s" % os.path.basename(folder))
    return N[0]
