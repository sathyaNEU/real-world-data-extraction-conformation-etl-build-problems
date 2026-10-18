"""task164 checks: the three rules executed on the clean truth (R1 to R3c), the family and its holes, the bins, the
ladder, every semantic fork row (SF1 to SF16), the asks and their devices, the cracker sheet, the separation line,
the distractors, the input gates and the realism sweep. Run by build.py after the pack is written.

    T164_CACHE=1 python3 checks.py [target]"""
from __future__ import annotations

import inspect
import json
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("T164_CACHE", "1")
import asks as AK       # noqa: E402
import calc as C        # noqa: E402
import common as K      # noqa: E402
import cracker as CR    # noqa: E402
import docs as DOC      # noqa: E402
import forward as FW    # noqa: E402
import ladder as LD     # noqa: E402
import pack as PK       # noqa: E402
import truth            # noqa: E402

TASK = os.path.dirname(HERE)
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %-14s %s" % ("PASS" if ok else "FAIL", label, detail))


def edge(v, unit=1.0):
    """Distance from v to the nearest edge of its printed cell at the given unit."""
    return unit / 2 - abs(v - round(v / unit) * unit)


def main(target=None):
    target = target or os.path.join(TASK, "target")
    T = truth.load()
    B = PK.Bundle(T)
    G = C.golden(target)
    P, pn = G["P"], G["pn"]
    Lp, ls, inc = C.ladder(G)
    gold_c, gold_a = G["counts"], G["alloc"]

    # --------------------------------------------------------------------------------------- R1: the raw material
    rows = {y: len(P.tlm[y]) for y in K.SUMMERS}
    check("R1a", all(v == len(T.tx) for v in rows.values()) and len(P.dmv) > 25000,
          "TLM %s rows a summer, DMV %d notifications, rate log %d changes" % (rows[2026], len(P.dmv), len(P.rate)))
    cols = " ".join(sum([list(pd.read_csv(os.path.join(target, f), nrows=2).columns) for f in os.listdir(target)
                         if f.endswith(".csv")], [])).lower()
    check("R1b", not re.search(r"increment|coincid|diversi|per_vehicle|at_risk|forecast", cols),
          "no shipped column holds a per-vehicle peak increment, a coincidence factor or an at-risk flag")
    check("R1c", gold_c.equals(T.counts.reindex(C.NAMES)) and gold_a.equals(T.alloc.reindex(C.NAMES)),
          "the golden from the pack (TLM peaks by DMV and rate states) equals the truth: %s" % dict(gold_c))

    # --------------------------------------------------------------------------------------- R2: mess neutral
    fam_counts = {k: v[0] for k, v in Lp.items() if k.startswith("FAM ")}
    check("R2-legacy", fam_counts["FAM 2025 to 2026 only"].equals(gold_c),
          "the 2024 legacy-layout run left out of the panel: counts unchanged")
    keys = [set(P.tlm[y]["loc"]) for y in K.SUMMERS] + [set(P.gis["loc"])]
    check("R2-keys", all(k == keys[-1] for k in keys) and set(P.sp["loc"]) <= keys[-1],
          "every TLM LOC_NO, TLM 5 location and service point joins the GIS register once the T and the zeros go")
    um = B.D[(B.D["_vi"] >= 0) & (B.D["matched_sp_id"] == "")].copy()
    um["matched_sp_id"] = um["_pi"].map(lambda p: str(int(B.SP[p])))
    pn_um = C.Panel(P, use_unmatched=um.drop(columns=["_pi", "_vi"])).build()
    c_um = C.at_risk(pn_um, C.forecast(pn_um, C.increments(C.transitions(pn_um))))
    check("R2-unmatched", c_um.equals(gold_c), "%d notifications the matcher left blank, placed at their service points: "
                                               "counts unchanged" % len(um))
    pn_ap = C.Panel(P).build()
    pn_ap.k1, pn_ap.e1 = pn_ap.state(pd.Series(pd.Timestamp(K.AS_OF), index=pn_ap.locs))
    c_ap = C.at_risk(pn_ap, C.forecast(pn_ap, G["tab"]))
    check("R2-april", c_ap.equals(gold_c), "the %d registrations of 1 to 4 April 2027 counted as if on the record date: "
                                           "counts unchanged" % len(B.april))
    out = P.dmv[P.dmv["matched_sp_id"].isna()]
    check("R2-outside", len(out) >= len(um), "%d notifications with no service point (outside addresses and the matcher's "
                                             "misses): none placed by the golden" % len(out))
    low = set()
    for y in (2025, 2026):
        t = pd.read_csv(os.path.join(target, PK.F_TLM[y]))
        low |= set(t.loc[t.ami_read_pct < 99.5, "xfmr_loc_id"])
    t = pd.read_csv(os.path.join(target, PK.F_TLM[2024]), dtype={"LOC_NO": str})
    low |= set(t.loc[t.AMI_PCT < 99.5, "LOC_NO"].astype(int))
    Pt = G["Pt"]
    c_ami = C.at_risk(pn, C.forecast(pn, C.increments(Pt[~Pt.index.isin(low)])))
    check("R2-ami", c_ami.equals(gold_c), "transitions on %d transformers with partial AMI reads dropped: counts unchanged" % len(low))
    k26 = P.tlm[2026].set_index("loc")["kva"].reindex(pn.locs).values
    check("R2-tlmkva", bool(np.all(k26 == pn.kva.values)), "the 2026 TLM run's kVA equals the register's at every location")

    # --------------------------------------------------------------------------------------- R3: the analyst test
    Lt = LD.Ladder(T)
    rt = Lt.table(T.fam)
    r0_t = rt["R0 average 4-9 pm demand per vehicle, by rate, every change"][1]
    check("R3a", r0_t["Foothill"] != T.alloc["Foothill"] and int((r0_t != T.alloc).sum()) >= 10,
          "the default path on the clean truth (average 4 to 9 pm demand by rate, every filed rule applied) gives "
          "Foothill %d against %d, %d districts off" % (r0_t["Foothill"], T.alloc["Foothill"], int((r0_t != T.alloc).sum())))
    r0 = Lp["R0"][1]
    check("R3a-pack", r0["Foothill"] == 59 and int((r0 != gold_a).sum()) >= 10,
          "the same path from the pack: Foothill %d, %d at risk, %d districts off" % (r0["Foothill"], Lp["R0"][0].sum(),
                                                                                   int((r0 != gold_a).sum())))
    check("R3b", Lp["FAM pooled by rate"][1].equals(gold_a),
          "the default path with only the per-vehicle figure changed (recorded-peak rise by rate, pooled) files the golden")
    lower = {k: Lp[k][1] for k in ("R0b", "R1", "R1b", "R2", "R2b")}
    check("R3b-lower", all(not a.equals(gold_a) for a in lower.values()),
          "each lower correction alone stays wrong: " + ", ".join("%s Foothill %d" % (k, a["Foothill"]) for k, a in lower.items()))
    t25 = pd.read_csv(os.path.join(target, PK.F_TLM[2025])).set_index("xfmr_loc_id")["peak_kva"]
    t26 = pd.read_csv(os.path.join(target, PK.F_TLM[2026])).set_index("xfmr_loc_id")["peak_kva"]
    eqp = (t25.reindex(t26.index) == t26).values
    runs, cur = 0, 0
    for x in eqp:
        cur = cur + 1 if x else 0
        runs = max(runs, cur)
    check("R3c", runs <= 3 and eqp.mean() < 0.03, "no copied block: %.2f%% of locations repeat their 2025 peak to the "
                                                  "hundredth, the longest run of consecutive locations doing so %d" % (100 * eqp.mean(), runs))
    doc_text = " ".join(DOC.DEC_FINDINGS + DOC.DEC_ORDERS + DOC.TAR_SPECIAL + [p for _, ps, _, _ in DOC.TARIFF for p in ps])
    check("R3c-docs", not re.search(r"kVA per vehicle|coincid|diversit|load study|average", doc_text, re.I),
          "no document states a per-vehicle figure, a coincidence factor or the load study")

    # --------------------------------------------------------------------------------------- the family and its holes
    check("FAMILY-truth", "family_mismatch" not in T.log, "all ten build members give the same district counts")
    check("FAMILY-pack", all(c.equals(gold_c) for c in fam_counts.values()),
          "%d members from the pack give the same district counts" % len(fam_counts))
    tx = T.tx
    chg = (T.k1 != tx.k2026.values) | (T.e1 != tx.e2026.values)
    ms = np.array([[FW.forecast(tab, s, a, b, c, d, p) for s, a, b, c, d, p in
                    zip(tx.sg[chg], tx.k2026[chg], tx.e2026[chg], T.k1[chg], T.e1[chg], tx.pk2026[chg])] for tab in T.fam.values()])
    ms = ms - K.THRESH * tx.kva.values[chg]
    clear = np.all(ms > FW.DELTA, axis=0) | np.all(ms < -FW.DELTA, axis=0)
    check("HOLES", bool(clear.all()), "every one of %d transformers whose vehicles changed since its 2026 peak sits %.1f kVA or "
                                      "more from the line under every member" % (int(chg.sum()), FW.DELTA))

    # --------------------------------------------------------------------------------------- bins
    q = G["q"]
    dq = (q - np.floor(q) - 0.5).abs()
    check("BIN-quota", float(dq.min()) >= 0.25, "every district's proportional share %.3f or more from a half (%s)" % (
        dq.min(), dq.idxmin()))
    check("BIN-plain", bool((np.round(q).astype(int) == gold_a).all()) and gold_a.sum() == 400,
          "plain rounding of the shares gives the largest-remainder allocation")
    check("BIN-distinct", gold_c.nunique() == 12, "twelve distinct district at-risk counts")
    one = 400.0 / gold_c.sum()
    check("BIN-one", float(dq.min()) > one, "a single transformer moves a share %.3f, inside the %.3f clearance" % (one, dq.min()))
    A, Bq = G["A"], G["B"]
    check("BIN-cost", all(edge(v) >= 0.25 for v in A["cost_per"]), "cost per replacement clearances %s" % [
        round(edge(v), 2) for v in A["cost_per"]])
    check("BIN-ch", all(edge(v) >= 0.25 for v in Bq["customer_hours"]), "customer-hours clearances min %.2f" % min(
        edge(v) for v in Bq["customer_hours"]))
    _, f = C.ask_b(P)
    check("BIN-8h", float((f.hours - 8).abs().min()) >= 0.19, "no failure line within 11 minutes of eight hours (closest %.2f h)" % float(
        (f.hours - 8).abs().min()))
    check("BIN-kva", all(abs(v * 2 - round(v * 2)) < 1e-9 for v in A["kva_added"]), "kVA added are exact halves: %s" % list(A["kva_added"]))

    # --------------------------------------------------------------------------------------- the ladder
    fh = {k: int(v[1]["Foothill"]) for k, v in Lp.items()}
    off = {k: int((v[1] != gold_a).sum()) for k, v in Lp.items()}
    for k in ("H", "R0", "R0b", "R1", "R1b", "R2", "R2b", "R3", "R4", "R5", "MED", "AVG3"):
        check("LADDER-" + k, off[k] >= 1, "Foothill %d, %d districts off, %d at risk" % (fh[k], off[k], Lp[k][0].sum()))
    check("LADDER-sep", fh["R0"] != fh["GOLD"] and fh["R2b"] != fh["GOLD"] and fh["R1b"] != fh["GOLD"],
          "Foothill: default %d, rating %d, increment with R-EV2 nil %d, golden %d" % (fh["R0"], fh["R1b"], fh["R2b"], fh["GOLD"]))
    check("LADDER-ls", 0.4 < ls["avg_tou"] < 0.9 and ls["avg_ev"] < 0.05 and inc["tou_pooled"] > 6 * ls["avg_tou"],
          "load study %.2f and %.3f kVA against recorded-peak rises %.2f and %.2f kVA" % (ls["avg_tou"], ls["avg_ev"],
                                                                                       inc["tou_pooled"], inc["ev_pooled"]))
    land = []
    for t_ in np.arange(3.6, 7.01, 0.2):
        for e_ in (0.0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5):
            a_c = C.allocate(C.at_risk(pn, C.constant_forecast(pn, t_, e_)))[0]
            if a_c.equals(gold_a):
                land.append((round(t_, 1), e_))
    ts_, es_ = [x for x, _ in land], [y for _, y in land]
    check("CORRIDOR", bool(land) and min(ts_) > 3 * ls["busy_tou"] and max(ts_) < 0.9 * ls["rating"],
          "constant per-vehicle figures land the golden allocation only for a default-rate figure of %.1f to %.1f kVA "
          "(R-EV2 %.1f to %.1f): above three times the load study's busiest quarter hour (%.2f) and under 0.9 of the "
          "charging rate (%.2f), a coincidence factor of %.2f to %.2f on it" % (
              min(ts_), max(ts_), min(es_), max(es_), ls["busy_tou"], ls["rating"], min(ts_) / ls["rating"],
              max(ts_) / ls["rating"]))

    def alloc_by(w):
        return C.allocate(pd.Series(w, dtype=float).reindex(C.NAMES))[0]

    by = lambda v: pd.Series(v, index=pn.locs).groupby(pn.district).sum()
    iepr_ = pd.read_excel(os.path.join(target, PK.F_IEPR)).set_index("District")["YE 2027"]
    fl_ = P.oms[P.oms.cause_code == "EQ-XFMR"]
    routes = {
        "IEPR 2027 vehicles": alloc_by(iepr_),
        "vehicles on the record date": alloc_by(by(pn.k1 + pn.e1)),
        "default-rate vehicles on the record date": alloc_by(by(pn.k1)),
        "vehicles added since the peak": alloc_by(by(np.clip(pn.k1 - pn.k[2026], 0, None) + np.clip(pn.e1 - pn.e[2026], 0, None))),
        "2026 overloads alone": alloc_by(by(pn.pk[2026].values > 1.2 * pn.kva.values)),
        "2026 peaks over 1.15": alloc_by(by(pn.pk[2026].values > 1.15 * pn.kva.values)),
        "2025 to 2026 rise repeated": alloc_by(by(2 * pn.pk[2026].values - pn.pk[2025].values > 1.2 * pn.kva.values)),
        "2024 to 2026 trend": alloc_by(by(1.5 * pn.pk[2026].values - 0.5 * pn.pk[2024].values > 1.2 * pn.kva.values)),
        "summer 2026 failures": alloc_by(fl_.xfmr_loc_id.str[1:].astype(int).map(pn.district).value_counts()),
        "transformer counts": alloc_by(pn.district.value_counts()),
    }
    I_ = P.lsi
    mins_ = I_.interval_ending.dt.hour * 60 + I_.interval_ending.dt.minute
    w_ = I_[(mins_ >= 975) & (mins_ <= 1260)].copy()
    w_["rate"] = w_.participant_id.map(dict(zip(P.lsp.participant_id, P.lsp.rate_schedule)))
    pmax = (w_.kwh * 4 / K.PF).groupby([w_.rate, w_.participant_id]).max().groupby(level=0).mean()
    routes["each participant's 4 to 9 pm maximum (%.2f, %.2f)" % (pmax["R-TOU4"], pmax["R-EV2"])] = C.allocate(
        C.at_risk(pn, C.constant_forecast(pn, pmax["R-TOU4"], pmax["R-EV2"])))[0]
    check("ROUTES", all(not a.equals(gold_a) for a in routes.values()),
          "; ".join("%s Foothill %d, %d off" % (k, a["Foothill"], int((a != gold_a).sum())) for k, a in routes.items()))
    cf_land = [cf for cf in np.arange(0.50, 1.001, 0.01) if C.allocate(C.at_risk(pn, C.constant_forecast(
        pn, cf * ls["rating"], 0.0)))[0].equals(gold_a)]
    check("ROUTES-cf", len(cf_land) > 0 and min(cf_land) > 0.6 and max(cf_land) < 0.8,
          "a coincidence factor on the charging rate with R-EV2 nil lands the allocation from %.2f to %.2f" % (
              min(cf_land), max(cf_land)))
    bt = C.backtest(G)
    a_, b_ = bt["load study average"], bt["2024-25 recorded-peak rises"]
    check("BACKTEST", a_["mean_error_gained_default"] > 3.0 and abs(b_["mean_error_gained_default"]) < 0.6 and
          abs(b_["mean_error"]) < abs(a_["mean_error"]),
          "2026 peaks forecast from 2025: the load study's averages leave %.2f kVA unforecast on transformers that gained a "
          "default-rate vehicle, the 2024-25 rises %.2f (mean errors %.2f and %.2f over %d changed transformers)" % (
              a_["mean_error_gained_default"], b_["mean_error_gained_default"], a_["mean_error"], b_["mean_error"], a_["n"]))

    # --------------------------------------------------------------------------------------- semantic forks
    m = G["f"] - K.THRESH * pn.kva.values
    eq = int((np.abs(m) < 1e-9).sum())
    check("SF1", True, "exceeds against reaches 120 percent: %d transformers exactly on the line; 'exceeds' (OP 3) is strict" % eq)
    check("SF2", not Lp["AVG3"][1].equals(gold_a), "a three-summer base (Foothill %d) is ruled out by OP 4's recorded 2026 peak" % fh["AVG3"])
    check("SF3", bool(np.all(k26 == pn.kva.values)), "nameplate: the register and the 2026 TLM run agree at every location (OP 5)")
    check("SF4", c_um.equals(gold_c), "registrations the matcher missed: same call either way")
    alt = {}
    for d in ("2026-09-30", "2026-06-01"):
        p2 = C.Panel(P).build()
        p2.k[2026], p2.e[2026] = p2.state(pd.Series(pd.Timestamp(d), index=p2.locs))
        alt[d] = C.allocate(C.at_risk(p2, C.forecast(p2, G["tab"])))[0]
    check("SF5", all(not a.equals(gold_a) for a in alt.values()) and "on the day of its recorded 2026 peak" in " ".join(DOC.DEC_ORDERS),
          "the base state is the peak day by OP 4's words; summer-end and summer-start bases move %d and %d districts" % tuple(
              int((a != gold_a).sum()) for a in alt.values()))
    P2 = C.Pack(target)
    P2.rate = P2.rate.copy()
    P2.rate["effective_date"] = P2.rate["request_date"]
    p3 = C.Panel(P2).build()
    c_req = C.at_risk(p3, C.forecast(p3, C.increments(C.transitions(p3))))
    a_req = C.allocate(c_req)[0]
    check("SF6", a_req.equals(gold_a) and "takes effect on the customer's next regular meter reading date" in " ".join(DOC.TAR_SPECIAL),
          "rate in effect = effective_date (tariff, dictionary); dated at the request instead: allocation unchanged, %d at-risk "
          "count(s) differ" % int((c_req != gold_c).sum()))
    check("SF7", c_ap.equals(gold_c), "vehicles registered after the record date (OP 4): same call if counted")
    check("SF8", (P.tlm[2026].set_index("loc")["district"].reindex(pn.locs).values == pn.district.values).all(),
          "district: the register and the TLM district codes agree at every location (OP 3)")
    check("SF9", not Lp["MED"][1].equals(gold_a), "median rises (Foothill %d) are ruled out by OP 4's expected effect" % fh["MED"])
    check("SF10", bool((np.round(q).astype(int) == gold_a).all()), "largest remainder and plain rounding agree (OP 2)")
    pk26 = P.tlm[2026]["date"]
    check("SF11", bool(((pk26 >= "2026-06-01") & (pk26 <= "2026-09-30")).all()), "every 2026 peak date inside 1 June to 30 September")
    t24 = pd.read_csv(os.path.join(target, PK.F_TLM[2024]), dtype={"LOC_NO": str})
    beg = pd.to_datetime(t24["PEAK_INTV_BEG"], format="%H:%M")
    check("SF12", bool(((beg.dt.hour * 60 + beg.dt.minute >= 960) & (beg.dt.hour * 60 + beg.dt.minute <= 1245)).all()),
          "the 2024 run labels the same 4 to 9 pm quarter hours by their start (16:00 to 20:45)")
    check("SF13", "power factor of 0.95" in " ".join(d for _, d in DOC.DICT["tlm_summer_peaks_2025/2026"]),
          "TLM peaks are kVA at 0.95; the golden adds kVA to kVA")
    check("SF14", len(P.gis) == len(T.tx) and (P.gis["status"] == "IN SERVICE").all(),
          "every location in service at the record date is in the register; none added or removed after it")
    dm = P.dmv.copy()
    dm_sd = pd.to_datetime(dm["status_date"], errors="coerce")
    check("SF15", int((dm_sd == pd.Timestamp(K.RECORD_DATE)).sum()) == 0 and int((pd.to_datetime(dm["reg_start_date"]) ==
                                                                                pd.Timestamp(K.RECORD_DATE)).sum()) >= 0,
          "no registration ends on the record date itself")
    check("SF16", "recorded 2026 summer peak adjusted by the expected effect" in " ".join(DOC.DEC_ORDERS),
          "the forecast 2027 summer peak is defined by OP 4")

    # --------------------------------------------------------------------------------------- the asks
    tA = T.pilot.groupby("district").size().reindex(C.PILOT)
    tK = (T.pilot.kva_new - T.pilot.kva_old).groupby(T.pilot.district).sum().reindex(C.PILOT)
    check("ASK-A", (A["replaced"].values == tA.values).all() and np.allclose(A["kva_added"].values, tK.values),
          "pilot replacements %s, kVA %s from the pack equal the truth" % (list(A["replaced"]), list(A["kva_added"])))
    tot = B.L.assign(d=B.L.wo_number.map(dict(zip(B.wos.wo_number, B.wos.district)))).groupby("d")["amount"].sum().reindex(C.PILOT)
    check("ASK-A-cost", np.allclose(A["total_cost"].values, tot.values, atol=0.005), "charges by district equal the ledger")
    ch_t, o8_t, _ = AK.ask_b_golden(T, B.O)
    check("ASK-B", np.allclose(Bq["customer_hours"].values, ch_t.values, atol=0.01) and (Bq["over_8h"].values == o8_t.values).all(),
          "customer-hours and customers over eight hours from the pack equal the truth")
    corr = T.corr
    check("DEV-A", all(len(corr[corr.district == d]) >= 1 for d in C.PILOT),
          "record corrections under PTR with an unchanged serial in every pilot district: %s" % dict(corr.groupby("district").size()))
    fo = f.copy()
    nl = fo.groupby("event_id").size()
    multi = fo[fo.event_id.map(nl) > 1]
    check("DEV-B", multi["district"].nunique() == 12 and (multi.customers_out > multi.sp).all(),
          "failure events covering several transformers in all twelve districts, customers_out above every line's own")
    cr = CR.main(target)
    check("CRACKER", int(cr["cracker"]["hit"].sum()) == 0, "the cracker misses all %d ask figures" % len(cr["cracker"]))
    check("MIRROR", 100 * cr["Lm"] < 35, "the mirror keeps %.1f%% of ask weight" % (100 * cr["Lm"]))
    check("PAIR", cr["pair"] <= 40, "pair ceiling %.1f" % cr["pair"])

    # --------------------------------------------------------------------------------------- separation and distractors
    src_main = inspect.getsource(C.Panel) + inspect.getsource(C.transitions) + inspect.getsource(C.increments) + \
        inspect.getsource(C.forecast) + inspect.getsource(C.at_risk)
    check("SEP", not re.search(r"\.oms|\.wo\b|\.cost|\.chg|\.lsi|\.lsp", src_main),
          "the main call reads the register, TLM, service points, rate changes and DMV only; no ask file")
    reg = P.gis.set_index("loc")["kva_rating"]
    corr_locs = [B.loc[t] for t in T.corr.ti]
    check("SEP-corr", all(reg[l] == float(T.tx.loc[t, "kva"]) for l, t in zip(corr_locs, T.corr.ti)),
          "the register carries the true rating at every pilot record correction (the device sits in the change log only)")
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    dis = meta["distractor_files"]
    csrc = open(os.path.join(HERE, "calc.py")).read()
    check("DIST", len(dis) >= 2 and all(os.path.exists(os.path.join(target, d)) for d in dis) and
          not any(d in csrc for d in dis), "distractors %s ship, and the golden never opens them" % dis)
    iepr = pd.read_excel(os.path.join(target, PK.F_IEPR))
    fdr = pd.read_csv(os.path.join(target, PK.F_FDR))
    check("DIST-rel", set(iepr["District"]) == set(C.NAMES) and set(fdr["district"]) == set(C.NAMES),
          "both distractors carry the twelve districts (the IEPR's 2027 vehicles, summer 2026 feeder peaks)")
    check("DIST-name", not any("distract" in f.lower() for f in os.listdir(target)), "no file named for its role")

    # --------------------------------------------------------------------------------------- input gates
    files = sorted(os.listdir(target))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check("GATE-files", len(files) >= 10, "%d files" % len(files))
    check("GATE-formats", len(fmts) >= 3, "formats %s" % sorted(fmts))
    check("GATE-rows", max(x["rows"] or 0 for x in meta["files"]) >= 25000, "largest %s, %d rows" % (
        meta["input_gates"]["largest_file"], meta["input_gates"]["largest_file_rows"]))
    check("GATE-meta", all(x.get("source") and x.get("date") and x.get("license") for x in meta["files"]) and
          len(meta["files"]) == len(files), "source, date and licence for every file")

    # --------------------------------------------------------------------------------------- realism
    people = set(K.PEOPLE.values())
    creators = set()
    for fn in files:
        if fn.endswith(".xlsx"):
            core = zipfile.ZipFile(os.path.join(target, fn)).read("docProps/core.xml").decode()
            creators |= set(x.replace("&amp;", "&") for x in re.findall(r"<dc:creator>([^<]*)</dc:creator>", core))
    check("REAL-people", creators <= people | {"Forecasting & Analytics"}, "workbook authors %s" % sorted(creators))
    blob = b""
    for fn in files:
        blob += open(os.path.join(target, fn), "rb").read()[:4000000] if not fn.endswith(".parquet") else b""
    check("REAL-scrub", b"ReportLab" not in blob and b"openpyxl" not in blob and b"reportlab" not in blob,
          "no writing library named in a container")
    check("REAL-dash", chr(0x2014).encode() not in blob and chr(0x2013).encode() not in blob, "no em or en dash in the pack")
    mt = {int(os.path.getmtime(os.path.join(target, fn))) for fn in files}
    check("REAL-mtime", len(mt) == 1, "one export stamp for every file")
    latest = []
    for fn in files:
        if fn.endswith(".csv"):
            d = pd.read_csv(os.path.join(target, fn), dtype=str)
            for c in d.columns:
                if re.search(r"(date|_utc|_ending|_start|_DT)$", c) and not d[c].dropna().str.fullmatch(r"\d{1,2}:\d{2}").all():
                    v = pd.to_datetime(d[c], errors="coerce", format="mixed")
                    if v.notna().any():
                        latest.append((v.max(), fn, c))
    lmax = max(latest)
    check("REAL-asof", lmax[0] <= pd.Timestamp(K.AS_OF) + pd.Timedelta(hours=23), "latest date in the pack %s (%s %s)" % (
        lmax[0], lmax[1], lmax[2]))
    man = pd.read_csv(os.path.join(target, PK.F_MAN))
    ext = dict(zip(man["file"], pd.to_datetime(man["extract_date"])))
    late = [(fn, c, str(v.date())) for v, fn, c in latest if fn in ext and v > ext[fn] + pd.Timedelta(days=1)
            and not (fn == PK.F_OMS and c == "restored_utc")]
    check("REAL-extract", not late, "every extract's dates on or before its manifest extract date%s" % (
        "" if not late else ": " + str(late[:4])))
    check("REAL-manifest", set(man["file"]) == set(files) - {PK.F_MAN}, "the manifest lists every shipped file but itself")
    dict_files = set(DOC.DICT)
    data_files = {f.rsplit(".", 1)[0] for f in files if f.rsplit(".", 1)[1] in ("csv", "xlsx", "parquet")} - {
        DOC.F_DICT.rsplit(".", 1)[0]}
    names = set()
    for k in dict_files:
        if "/" in k:
            head, tail = k.split("/")
            names |= {head, head[:-len(tail)] + tail}
        else:
            names.add(k)
    covered = data_files & names
    check("REAL-dictionary", covered == data_files, "the dictionary defines every data file%s" % (
        "" if covered == data_files else ": missing " + str(sorted(data_files - covered))))
    rem = pd.read_excel(os.path.join(target, PK.F_WO))["Remarks"].dropna()
    check("REAL-text", rem.value_counts().max() <= 6, "no crew remark recurs more than %d times" % rem.value_counts().max())
    check("REAL-round", gold_c.sum() % 100 != 0 and all(v % 10 != 0 for v in A["replaced"]),
          "no round headline: %d at risk, pilot %s" % (gold_c.sum(), list(A["replaced"])))
    ntx = P.gis.groupby("district").size()
    check("REAL-counts", ntx.nunique() == 12 and all(v % 100 != 0 for v in ntx), "district transformer counts %s" % dict(ntx))

    # --------------------------------------------------------------------------------------- documents read back
    from pypdf import PdfReader
    dec = " ".join(p.extract_text() for p in PdfReader(os.path.join(target, DOC.F_DEC)).pages)
    dec = re.sub(r"\s+", " ", dec)
    check("DOC-dec", all(s in dec for s in ("largest fractional parts", "exceeds 120 percent of its nameplate rating",
                                             "on the day of its recorded 2026 peak", "The record date is March 31, 2027")),
          "the decision excerpt carries OP 2 to OP 5 as filed")
    tar = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(os.path.join(target, DOC.F_TAR)).pages))
    check("DOC-tariff", "Peak 4:00 p.m. to 9:00 p.m." in tar and "next regular meter reading date" in tar,
          "the tariff excerpt carries the 4 to 9 pm peak and the effective-date rule")
    dic = pd.read_excel(os.path.join(target, DOC.F_DICT), sheet_name="Fields")
    check("DOC-dict", dic["Definition"].str.contains("power factor of 0.95").any() and
          dic["Definition"].str.contains("UTC").any(), "the dictionary carries the kVA basis and the OMS clock")

    n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
    print("\n%d checks, %d FAIL" % (len(RESULTS), n_fail))
    return n_fail


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else None) else 0)
