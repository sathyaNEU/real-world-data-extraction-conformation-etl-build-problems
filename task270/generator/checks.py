"""task270 checks: the analyst test on the generator's clean truth, the call on the cut pack, the licensed family of
cycle readings and the ladder's wrong rungs, every semantic fork, the Layer 1 mess on the call's path, the pilot ask's
devices, stops and fairness, the separation of the ask from the call, the invented names and the pack's gates.
Exit 1 on any failure.

    python3 task270/generator/checks.py [TARGET]"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys

import numpy as np
import openpyxl
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A        # noqa: E402
import calc as C        # noqa: E402
import common as K      # noqa: E402
import cracker as CR    # noqa: E402
import docs as D        # noqa: E402
import pilot as PL      # noqa: E402
import records as R     # noqa: E402
import world as W       # noqa: E402

ROWS = []
DAY0 = K.YEAR_START.toordinal()
NDAYS = (K.YEAR_END - K.YEAR_START).days + 1
# real places a screen of the reference list misses, read from a gazetteer by hand: each sits within two edits of a
# name this build once used, or of a distinctive word it uses now
EXTRA_PLACES = ["grasmere", "kirstead", "corrany", "corran", "tarvin", "eskdale", "wembley", "halstead", "holme",
                "dillon", "thessaly", "corwen"]


def row(label, ok, detail=""):
    ROWS.append((label, bool(ok), detail))


def pct(sh):
    return {c: K.round_half_up(100 * v["share"], 1) for c, v in sh.items()}


def same_figures(a, b):
    return all(a[c]["n"] == b[c]["n"] and a[c]["low"] == b[c]["low"] for c in K.NETWORK_NAME)


def pdc_variant(items, start=None, union=False):
    """Specification 2.2 on (day, days) items; start overrides the first item's day; union counts each covered day
    once without moving an overlap forward."""
    items = sorted(items)
    first = items[0][0] if start is None else start
    cov = np.zeros(NDAYS + 900, bool)
    nxt = -400
    for d, n in items:
        st = d if union else max(d, nxt)
        if st < 0:
            n, st = n + st, 0
        if n > 0:
            cov[st:st + n] = True
        nxt = st + n
    return cov[first:NDAYS].sum() / (NDAYS - first)


def tier_of(T, mask, pdc_col="pdc"):
    out = {}
    for c in K.NETWORK_NAME:
        s = T[mask & (T["network"] == c)]
        out[c] = dict(n=int(len(s)), low=int((s[pdc_col] < K.PDC_LINE).sum()),
                      share=float((s[pdc_col] < K.PDC_LINE).mean()) if len(s) else float("nan"))
    return out


def clean_truth(pts, pracs):
    """Every patient on the year-end lists, aged 65 or over, two or more 2026 items, each 2026 proportion of days
    covered from the world's own items; the analyst's population (care home residents and coded aid patients out)
    and the specification's (the patients who collect and take their own statins)."""
    net = {p["code"]: p["network"] for p in pracs}
    rows = []
    for pt in pts:
        if pt["left"] or pt["yob"] > K.BORN_BY:
            continue
        it = [((d - K.YEAR_START).days, int(round(q / pt["tpd"]))) for d, _o, _p, q, _t in pt["items"]
              if K.YEAR_START <= d <= K.YEAR_END]
        if len(it) < 2:
            continue
        rows.append(dict(network=net[pt["practice"]], kind=pt["kind"], coded=pt["coded_aid"], pdc=C.pdc_of(it)))
    T = pd.DataFrame(rows)
    analyst = tier_of(T, (T["kind"] != "ch") & ~T["coded"])
    decisive = tier_of(T, T["kind"] == "sm")
    return analyst, decisive


def main(target=K.TARGET):
    pracs, pharms, pts = W.build()
    analyst, truth = clean_truth(pts, pracs)
    tset = C.tier(truth)
    # ------------------------------------------------------------------ the three rules on the clean truth
    row("R3a ANALYST the easy route on the clean truth (care home residents and coded aid patients out) names "
        "another set", C.tier(analyst) != tset, "%s against %s" % (C.tier(analyst), tset))
    row("R3a ANALYST the easy route leaves out exactly Briskdale and Grevmoor, the two Synaris networks with the most "
        "aid patients",
        set(tset) - set(C.tier(analyst)) == {"BRK", "GRV"} and set(C.tier(analyst)) <= set(tset),
        str(sorted(set(tset) - set(C.tier(analyst)))))
    row("R3b DECISIVE the self-managing patients alone, on the clean truth, name six networks", len(tset) == 6, str(tset))
    # ------------------------------------------------------------------ the call on the pack
    T = C.patient_table(target)
    gold = C.shares(T, C.route_mask(T, "G", "cyc1"))
    gset = C.tier(gold)
    row("CALL the golden on the pack names the clean truth's set", gset == tset, str(gset))
    row("CALL every network's population and fallen-behind count on the pack equal the clean truth's",
        same_figures(gold, truth), "")
    gap = min(abs(v["share"] - K.TIER_LINE) for v in gold.values())
    row("CALL every network's share sits 1.5 points or more from 30 per cent", gap >= 0.015, "%.3f points" % (100 * gap))
    below = max((c for c in K.NETWORK_NAME if c not in gset), key=lambda c: gold[c]["share"])
    low_in = min(gset, key=lambda c: gold[c]["share"])
    row("CALL the first network below the line and the lowest one over it", True,
        "%s %.2f, %s %.2f" % (below, 100 * gold[below]["share"], low_in, 100 * gold[low_in]["share"]))
    clear = min(K.bin_clearance(100 * v["share"], 0.1) for v in gold.values())
    row("CALL no share sits on a rounding edge of its one-decimal bin", clear > 0.001, "%.4f of a step" % clear)
    # ------------------------------------------------------------------ the family of cycle readings
    elig = T[T["eligible_base"]]
    coded = elig[elig["coded_aid"]]
    kind = {pt["new_key"]: pt["kind"] for pt in pts}
    T["kind"] = T["patient"].map(kind)
    for col, label in (("cyc1", "steps within a day of 7 or 28 on nine in ten (the golden)"),
                       ("cyc2w", "steps within two days on nine in ten, on one weekday"),
                       ("cyc3w", "steps within three days on four in five, on one weekday")):
        sh = C.shares(T, C.route_mask(T, "G", col))
        row("FAMILY %s flags every coded aid patient" % label, bool(coded[col].all()),
            "%d of %d" % (int(coded[col].sum()), len(coded)))
        row("FAMILY %s names the golden set with every population and share the golden's" % label,
            C.tier(sh) == gset and same_figures(sh, gold), "")
        row("FAMILY %s flags no self-managing patient and misses no aid patient (the world's own kinds)" % label,
            int((T[col] & (T["kind"] == "sm")).sum()) == 0 and int((~T[col] & (T["kind"] == "aid")).sum()) == 0, "")
    T["wkstep"] = T["weekday"] & T["patient"].isin(set(T.loc[T["cyc1"] | T["cyc2"] | T["cyc3"], "patient"]))
    sh = C.shares(T, C.route_mask(T, "G", "wkstep"))
    row("FAMILY one weekday with any of the step readings names the golden set and figures",
        C.tier(sh) == gset and same_figures(sh, gold), "")
    for col, label in (("cyc2", "steps within two days, any weekday"), ("cyc3", "steps within three days, any weekday")):
        sh = C.shares(T, C.route_mask(T, "G", col))
        diff = [c for c in K.NETWORK_NAME if sh[c]["n"] != gold[c]["n"] or pct(sh)[c] != pct(gold)[c]]
        row("RECORD %s names the golden set (figures differ in %d networks; it flags %d self-managing patients whose "
            "items fall on several weekdays, against the guidance's same-day supply)"
            % (label, len(diff), int((T[col] & (T["kind"] == "sm")).sum())), C.tier(sh) == gset, ", ".join(diff))
    sh0 = C.shares(T, C.route_mask(T, "G", "cyc0"))
    row("RECORD exact steps only miss coded aid patients whose packs moved round a bank holiday (refuted by the coded "
        "patients), and name the golden set", int((~coded["cyc0"]).sum()) > 50 and C.tier(sh0) == gset,
        "%d of %d coded aid patients missed" % (int((~coded["cyc0"]).sum()), len(coded)))
    # ------------------------------------------------------------------ the ladder's rungs and Gate F
    routes = {r: C.shares(T, C.route_mask(T, r)) for r in ("R0", "R1", "R2", "R3", "R4")}
    for r, sh in routes.items():
        row("RUNG %s (%s) names another set" % (r, C.ROUTES[r]), C.tier(sh) != gset, str(C.tier(sh)))
    row("RUNG R2, the analyst's route, names four networks, leaving out Briskdale and Grevmoor",
        C.tier(routes["R2"]) == ["COR", "FEL", "KRT", "NVG"], str(C.tier(routes["R2"])))
    base = T["eligible_base"] & ~T["care_home"]
    cheap = {
        "coded or weekly items out": base & ~T["coded_aid"] & ~T["weekly_items"],
        "full cover 95 per cent or more out": base & ~(T["pdc"] >= 0.95),
        "full cover 97 per cent or more out": base & ~(T["pdc"] >= 0.97),
        "full cover 100 per cent out": base & ~(T["pdc"] >= 1.0),
        "coded out and full cover out": base & ~T["coded_aid"] & ~(T["pdc"] >= 0.99),
        "thirteen or more 2026 items out": base & ~(T["n_items"] >= 13),
        "coded out and thirteen or more items out": base & ~T["coded_aid"] & ~(T["n_items"] >= 13),
    }
    land = 0
    for name, m in cheap.items():
        st = C.tier(C.shares(T, m))
        land += st == gset
        row("RUNG cheap route (%s) names another set" % name, st != gset, str(st))
    row("GATE F cheap routes landing the call on the pack", land == 0 and all(C.tier(s) != gset for s in routes.values()),
        "%d of %d" % (land, len(cheap) + len(routes)))
    # ------------------------------------------------------------------ semantic forks
    Dp, pop = C.load(target)
    y = Dp[(Dp["date"] >= K.YEAR_START) & (Dp["date"] <= K.YEAR_END)].copy()
    y["d"] = y["date"].map(lambda x: x.toordinal() - DAY0)
    grp = {k: list(zip(g["d"], g["days"])) for k, g in y.groupby("patient")}
    mask_g = C.route_mask(T, "G", "cyc1")
    spec = " ".join(p for _, ps in D.SPEC for p in ps)

    def variant(pdc_map, mask=mask_g, col="pdc_v"):
        T[col] = T["patient"].map(pdc_map)
        return tier_of(T, mask & T[col].notna(), col)

    T1 = T.copy()
    m1 = T1["eligible_base"] & ~T1["care_home"] & ~T1["cyc1"] & ~T1["coded_aid"] & (T1["yob"] <= 1960)
    row("SF1 aged 65 or over on 31 December 2026 (filed 2.1); born 1960 or earlier instead, same call",
        "born in 1961 or earlier" in spec and C.tier(tier_of(T1, m1)) == gset, C.tier(tier_of(T1, m1)))
    left = set(y["patient"]) - set(pop["patient"])
    row("SF2 registered on 31 December 2026 (filed 2.1): the year-end lists hold no patient who left during 2026, "
        "whose items stay in the dispensing", len(left) > 300, "%d dispensed-to patients not on the lists" % len(left))
    P = pd.read_csv(os.path.join(target, R.F_PRACTICES), dtype=str).fillna("")
    early = {r.practice_ods: r.network.replace(" PCN", "") for r in P.itertuples() if r.member_to}
    name_to = {v: k for k, v in K.NETWORK_NAME.items()}
    first_day = y.groupby("patient")["date"].min()
    T2 = T.copy()
    T2["network"] = [name_to[early[p]] if p in early and first_day.get(k, K.YEAR_END) < K.NETWORK_MOVE else n
                     for k, p, n in zip(T2["patient"], T2["practice"], T2["network"])]
    row("SF3 each network as its practices stood on 31 December 2026 (filed 3.1); a moved practice's patients in its "
        "old network when their first 2026 item came before the move, same call",
        "as its practices stood on 31 December 2026" in spec and C.tier(tier_of(T2, mask_g)) == gset,
        str(C.tier(tier_of(T2, mask_g))))
    main_prod = y.groupby("patient")["product_description"].agg(lambda s: s.value_counts().index[0])
    per_prod = {}
    for k, g in y.groupby("patient"):
        g2 = g[g["product_description"] == main_prod[k]]
        if len(g2) >= 1:
            per_prod[k] = pdc_variant(list(zip(g2["d"], g2["days"])), start=int(g["d"].min()))
    row("SF4 every statin counts and a change of statin continues the supply (filed 2.2, in those words); the patient's "
        "main product alone would read a switch as a stop", "Every statin counts, so a change of statin continues the "
        "supply" in spec, "main product alone: %s" % C.tier(variant(per_prod)))
    asdir = set(y.loc[y["dosage_instructions"].str.upper().str.contains("AS DIRECTED"), "patient"])
    row("SF5 an item's days from its quantity and the dosage's tablets a day, AS DIRECTED one a day (filed 2.2); the "
        "AS DIRECTED patients left out instead, same call",
        "or one tablet a day where they give none" in spec
        and C.tier(tier_of(T, mask_g & ~T["patient"].isin(asdir))) == gset, "%d AS DIRECTED patients" % len(asdir))
    uni = {k: pdc_variant(v, union=True) for k, v in grp.items() if len(v) >= 2}
    row("SF6 an overlap moves to follow the earlier supply (filed 2.2); covered days counted once instead, same call",
        "starts when that supply ends" in spec and C.tier(variant(uni)) == gset, str(C.tier(variant(uni))))
    pre = Dp[(Dp["date"] < K.YEAR_START)].copy()
    pre["d"] = pre["date"].map(lambda x: x.toordinal() - DAY0)
    carry = {}
    pre_g = {k: list(zip(g["d"], g["days"])) for k, g in pre.groupby("patient")}
    for k, v in grp.items():
        if len(v) >= 2:
            carry[k] = pdc_variant(pre_g.get(k, []) + v, start=min(d for d, _ in v))
    cal = {k: pdc_variant(v, start=0) for k, v in grp.items() if len(v) >= 2}
    row("SF7 from the first 2026 item, 2025 items not counted (filed 2.2); December 2025 supply carried in instead, "
        "same call", "Items dispensed before 1 January 2026 are not counted" in spec and C.tier(variant(carry)) == gset,
        str(C.tier(variant(carry))))
    row("SF7 the days counted run from the patient's first 2026 item (filed 2.2, in those words), not from 1 January",
        "the days from the date of the patient's first statin item dispensed in 2026 to 31 December 2026" in spec,
        "from 1 January without carry-in: %s" % C.tier(variant(cal)))
    one = {k: C.pdc_of(v) for k, v in grp.items() if len(v) == 1}
    T["pdc1"] = T["patient"].map(lambda k: one.get(k, np.nan))
    T["pdc_any"] = T["pdc"].fillna(T["pdc1"])
    m8 = (T["aged65"] & (T["n_items"] >= 1)) & ~T["care_home"] & ~T["cyc1"] & ~T["coded_aid"]
    row("SF8 two or more 2026 items (filed 2.1); one or more instead, same call",
        "two or more statin items" in spec and C.tier(tier_of(T, m8, "pdc_any")) == gset,
        "%d one-item patients" % int((T["n_items"] == 1).sum()))
    at80 = int(((T["pdc"] - 0.8).abs() < 1e-12).sum())
    T["pdc_le"] = np.where((T["pdc"] - 0.8).abs() < 1e-12, 0.79, T["pdc"])
    row("SF9 under 80 per cent is strict (filed 2.3); at 80 per cent counted as fallen behind too, same call",
        "is under 80 per cent has fallen behind" in spec and C.tier(tier_of(T, mask_g, "pdc_le")) == gset,
        "%d patients at exactly 80 per cent" % at80)
    row("SF10 30 per cent or more is inclusive (filed 3.1), and no network sits within 1.5 points of it",
        "30 per cent or more" in spec and gap >= 0.015, "%.2f points" % (100 * gap))
    aid_mid = [pt for pt in pts if pt["kind"] == "aid" and pt["aid_from"]]
    row("SF11 the compliance-aid patients at the year end or at any time in 2026: no patient moved onto an aid during "
        "the year, so both readings take the same patients", not aid_mid, "%d" % len(aid_mid))
    Q = pd.read_csv(os.path.join(target, R.F_QUARVIS), dtype=str).fillna("")
    qd = pd.to_datetime(Q.loc[Q["care_home_since"] != "", "care_home_since"], dayfirst=True)
    wb = openpyxl.load_workbook(os.path.join(target, R.F_SYNARIS), read_only=True)
    trows = list(wb["Lipid cohort"].iter_rows(values_only=True))[1:]
    td = [r[5] for r in trows if str(r[4]).startswith("Care home")]
    row("SF12 care home residence at the year end or at any time in 2026: every resident's record dates from before "
        "2026 on both lists", qd.max() < pd.Timestamp(K.YEAR_START) and max(td) < dt.datetime(2026, 1, 1),
        "%s, %s" % (qd.max().date(), max(td).date()))
    Xw = pd.read_csv(os.path.join(target, R.F_XWALK), dtype=str)
    raw = Dp.copy()
    raw["patient"] = raw["patient_pseudonym"]
    nox = {}
    yr = raw[(raw["date"] >= K.YEAR_START) & (raw["date"] <= K.YEAR_END)].copy()
    yr["d"] = yr["date"].map(lambda x: x.toordinal() - DAY0)
    for k, g in yr.groupby("patient"):
        if len(g) >= 2:
            nox[k] = C.pdc_of(list(zip(g["d"], g["days"])))
    shx = variant(nox)
    moved = [c for c in K.NETWORK_NAME if shx[c]["n"] != gold[c]["n"] or pct(shx)[c] != pct(gold)[c]]
    row("SF13 the pre-July pseudonyms carried through the crosswalk; read apart, every network's figures move "
        "(a Layer 1 stop)", len(moved) == 12 and len(Xw) > 20000, "%d networks move, %d crosswalk rows" % (len(moved), len(Xw)))
    row("SF14 the reading that marks a cycle: every standing reading names the golden set with its figures (FAMILY rows)",
        True, "")
    row("SF15 shares to one decimal of a per cent: the standing readings print the same share in every network "
        "(FAMILY rows) and none sits on a rounding edge", clear > 0.001, "")
    ph = pd.read_csv(os.path.join(target, PL.F_PHARMACIES), dtype=str).fillna("")
    dsp = set(ph.loc[ph["contract_type"] == "Distance selling", "ods_code"])
    nd = y[~y["dispenser_ods"].isin(dsp)]
    gnd = {k: list(zip(g["d"], g["days"])) for k, g in nd.groupby("patient")}
    T["n_nd"] = T["patient"].map(lambda k: len(gnd.get(k, [])))
    T["pdc_nd"] = T["patient"].map(lambda k: C.pdc_of(gnd[k]) if len(gnd.get(k, [])) >= 2 else np.nan)
    m16 = T["aged65"] & (T["n_nd"] >= 2) & ~T["care_home"] & ~T["cyc1"] & ~T["coded_aid"]
    row("SF16 a distance-selling pharmacy's items count (filed 2.1); left out instead, same call",
        "distance-selling pharmacies included" in spec and C.tier(tier_of(T, m16, "pdc_nd")) == gset,
        "%d items from %s" % (int(y["dispenser_ods"].isin(dsp).sum()), ", ".join(sorted(dsp))))
    # ------------------------------------------------------------------ Layer 1 on the call's path
    old = Dp["patient_pseudonym"].str.fullmatch(r"\d{12}")
    row("L1 the data service's re-keying: items before 1 July carry the old twelve-digit pseudonym",
        bool(old.any()) and (Dp.loc[old, "date"].max() < K.REKEY) and (Dp.loc[~old, "date"].min() >= K.REKEY),
        "%d old-key rows" % int(old.sum()))
    row("L1 two practices moved network on 1 April 2026 and carry a row for each network", len(early) == 2, str(early))
    texts = set(Dp["dosage_instructions"])
    row("L1 dosage instructions as prescribers typed them, two-a-day and AS DIRECTED among them",
        len(texts) >= 12 and any("TWO" in t or t.startswith("2") for t in texts) and "AS DIRECTED" in texts,
        "%d distinct" % len(texts))
    row("L1 branded and generic statins, and a change of statin in the year",
        Dp["product_description"].str.contains(r"\(").any() and int((y.groupby("patient")["product_description"]
                                                                       .nunique() > 1).sum()) > 100, "")
    row("L1 the dispensing extract runs from 1 December 2025, as its name says", Dp["date"].min() >= K.EXTRACT_START
        and Dp["date"].min() < dt.date(2025, 12, 8) and Dp["date"].max() <= K.YEAR_END, str(Dp["date"].min()))
    labels = {str(r[4]) for r in trows}
    row("L1 Synaris's residence labels include sheltered housing and not recorded, neither a care home",
        {"Sheltered housing", "Not recorded"} <= labels, ", ".join(sorted(labels)))
    # ------------------------------------------------------------------ the pilot ask
    pr2, ph2, pts2 = pracs, pharms, pts
    pilots, mvd, ev = PL.build(ph2, pts2)
    C1t, C2t = PL.truth(ev, pilots, mvd)
    C1, C2 = A.pilot_figures(target)
    row("ASK fair: the golden's handling of the pack reproduces the pilot's truth in all 16 figures",
        C1 == C1t and C2 == C2t, "")
    copies = [e for e in ev if e["dup_of"] is not None]
    late = [e for e in ev if e.get("late")]
    row("ASK every hand-keyed copy is recovered, and its system record is not",
        all(not e["dup_of"].get("late") for e in copies) and len(copies) >= 30, "%d copies" % len(copies))
    row("ASK copies reach the portal both before and after their system record (first-recorded is no rule)",
        sum(e["rec"] < e["dup_of"]["rec"] for e in copies) >= 5 and sum(e["rec"] > e["dup_of"]["rec"] for e in copies) >= 5,
        "%d before, %d after" % (sum(e["rec"] < e["dup_of"]["rec"] for e in copies),
                                 sum(e["rec"] > e["dup_of"]["rec"] for e in copies)))
    twins = {e["pt"]["pid"] for e in copies}
    row("ASK every late claim is a consultation held: no late-claimed record belongs to a patient recorded twice, and "
        "each was recorded after its fifth working day", all(e["pt"]["pid"] not in twins and e["rec"] > PL.deadline(e["date"])
                                                             for e in late), "%d late claims" % len(late))
    on_time = [e for e in ev if not e.get("late") and e["dup_of"] is None]
    row("ASK every other record was claimed by its fifth working day", all(e["rec"] <= PL.deadline(e["date"]) for e in on_time), "")
    E, S, Pp, xmap = A.load_pilot(target)
    rec_ids = set(S.loc[S["line"] == "Recovery", "record_id"])
    ids_late = {e["id"] for e in late}
    ids_copy = {e["id"] for e in copies}
    row("ASK the statements recover exactly the copies and the late claims", rec_ids == ids_late | ids_copy,
        "%d recoveries" % len(rec_ids))
    gold1, gold2, out = CR.run(target)
    crack = out[0]
    row("ASK the cracker keeps none of the 16 figures", not crack[4] and not crack[5],
        "%d kept" % (len(crack[4]) + len(crack[5])))
    for name, desc, c1, c2, h1, h2 in out[1:]:
        row("ASK route %s (%s) keeps %d of 16" % (name, desc, len(h1) + len(h2)), len(h1) + len(h2) <= 13, "")
    row("ASK no route but the golden's keeps more than 13 of 16", max(len(o[4]) + len(o[5]) for o in out) <= 13, "")
    for cell in gold1:
        row("ASK stop %s quarter %d: the cracker's first consultations and follow-ups both miss" % cell,
            crack[2][cell] != gold1[cell] and crack[3][cell] != gold2[cell],
            "%d/%d against %d/%d" % (crack[2][cell], crack[3][cell], gold1[cell], gold2[cell]))
    # ------------------------------------------------------------------ separation
    src = open(os.path.join(HERE, "calc.py"), encoding="utf-8").read()
    row("SEP the call reads none of the pilot's files (the export, the statements, the pharmacy list)",
        not re.search(r"F_PORTAL|F_STATEMENTS|F_PHARMACIES|pilot", src), "")
    row("SEP no ask device sits in a file the call reads: copies, late claims and the relocation live in the pilot's "
        "files, and the dispensing carries no pilot record", "record_id" not in Dp.columns, "")
    # ------------------------------------------------------------------ names, dashes, gates
    places = [x.strip().lower() for x in open(os.path.join(HERE, "h21_reference_places.txt")) if x.strip()]
    places += EXTRA_PLACES
    names = sorted({n for _c, n, *_ in K.NETWORKS} | set(W.EXTRA_PLACES) | {"Quarvis", "Synaris", "Iversford",
                                                                             "Vellmarsh", "Pellhope", "Ravensholt",
                                                                             "Drevanholm"})
    near = ["%s (%s)" % (nm, p) for nm in names for p in places
            if _ed(nm.lower(), p) <= 2 or (len(p) >= 5 and (p in nm.lower() or nm.lower() in p))]
    row("H21 every invented place, system and owner name (%d) is three or more edits from every reference place"
        % len(names), not near, ", ".join(near[:6]))
    text = " ".join(p for _, ps in D.SPEC + D.GUIDE + D.CPCF for p in ps)
    row("no em or en dash in the documents", "—" not in text and "–" not in text, "")
    files = sorted(os.listdir(target))
    row("GATE files", len(files) >= 10, str(len(files)))
    row("GATE formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3, str(sorted({f.rsplit('.', 1)[1] for f in files})))
    row("GATE a file of 25,000 rows or more", len(Dp) >= 25000, str(len(Dp)))
    row("H16 no dispensing after 31 December 2026 and nothing in the export after its pull",
        Dp["date"].max() <= K.YEAR_END and pd.to_datetime(E["recorded_on"], dayfirst=True).max().date() <= PL.PORTAL_PULL, "")
    meta = os.path.join(os.path.dirname(HERE), "metadata.json")
    if os.path.exists(meta):
        M = json.load(open(meta))
        dis = M.get("distractor_files", [])
        row("GATE two or more distractors named in metadata.json, each shipped and none in a graded computation",
            len(dis) >= 2 and all(f in files for f in dis) and not any(
                re.search(re.escape(f), open(os.path.join(HERE, m), encoding="utf-8").read())
                for f in dis for m in ("calc.py", "asks.py")), ", ".join(dis))
        row("GATE metadata.json lists every shipped file", sorted(f["path"] for f in M.get("files", [])) == files, "")
    bad = [r for r in ROWS if not r[1]]
    for label, ok, detail in ROWS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [%s]" % detail) if detail else ""))
    print("checks: %d run, %d failed" % (len(ROWS), len(bad)))
    return 1 if bad else 0


def _ed(a, b):
    if abs(len(a) - len(b)) > 2:
        return 9
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        prev = cur
    return prev[-1]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else K.TARGET))
