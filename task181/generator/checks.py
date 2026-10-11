"""Assertion regime for task181. Run after build.py: python3 checks.py  (exit 1 on any failure).

Every figure is computed from the shipped files through golden.py's loaders; nothing here reads generator
state. Results are written to $T181_RESULTS (default: the system temp directory) for the design note.
"""
import datetime as dt
import functools
import inspect
import json
import os
import sys

import numpy as np
import pandas as pd

import golden as G

FAILS, PASSES = [], []
R = {}


def check(name, cond, detail=""):
    (PASSES if cond else FAILS).append((name, detail))
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def pct(x, ans):
    return 100.0 * (x - ans) / ans


def exp_set(tid, modes="contact"):
    return G.all_exposures(modes).get(tid, frozenset())


def count(tids, modes="contact", status="open"):
    toks = set()
    for t in tids:
        toks |= exp_set(t, modes)
    if status == "open":
        toks &= G.open_cards()
    return len(toks)


def main():
    vic = G.victims()
    a = G.auth()
    files = sorted(os.listdir(G.TARGET))

    # ---------------------------------------------------------------- input gates
    exts = {os.path.splitext(f)[1] for f in files}
    check("13 files shipped, 10 or more", len(files) == 13, str(len(files)))
    check("3 or more formats", len(exts) >= 3, ",".join(sorted(exts)))
    check("authorisation log over 1,000,000 rows", len(a) > 1_000_000, str(len(a)))
    check("authorisation log between 1.1 and 1.4 million messages", 1_100_000 <= len(a) <= 1_400_000, str(len(a)))
    for f in files:
        check(f"no 'distractor' in file name {f}", "distractor" not in f.lower())
    meta = json.load(open(os.path.join(G.HERE, "..", "metadata.json"))) if os.path.exists(
        os.path.join(G.HERE, "..", "metadata.json")) else {"distractor_files": []}
    dfiles = meta.get("distractor_files", [])
    check("two distractors named in metadata.json and shipped", len(dfiles) == 2 and all(d in files for d in dfiles),
          str(dfiles))
    src = inspect.getsource(G)
    for d in ("online_banking_logins", "atm_cash_replenishment"):
        check(f"distractor {d} never read by the golden", d not in src)
    c, rep, mem = G.cards()
    act = a.card_token.nunique()
    R["active_card_numbers"] = int(act)
    check("about 15,000 member cards in use (card slots), card numbers active in the log", 14_000 <= act <= 18_000,
          str(act))
    ct = G.card_type_of()
    by_type = pd.Series([ct[t] for t in a.card_token.unique()]).value_counts().to_dict()
    R["active_by_type"] = by_type
    check("every token in the log is in the card history", set(a.card_token.unique()) <= set(c.card_token))

    # ---------------------------------------------------------------- victims and their sources
    check("283 counterfeit cards", len(vic) == 283, str(len(vic)))
    check("first counterfeit use is 24 August 2026", min(vic.values()) == dt.date(2026, 8, 24))
    s = G.solve()
    R["solve"] = json.loads(G.printable(s))
    opt6, sco2 = s["terminals"] if len(s["terminals"]) == 2 else (None, None)
    check("sequential attribution names two terminals", len(s["terminals"]) == 2, str(s["terminals"]))
    pooled = s["pooled"]
    mids = a.drop_duplicates("terminal_id").set_index("terminal_id").merchant_id
    md = G.merchants().set_index("merchant_id")
    name = lambda t: md.loc[mids[t], "name"] if t in mids.index else t
    check("first terminal is the plaza pay-at-pump", "Pay at Pump" in name(opt6), name(opt6))
    check("second terminal is at Lombard Market", name(sco2) == "Lombard Market", name(sco2))
    pmd = md[md.address == md.loc[mids[opt6], "address"]]
    plaza = a[a.merchant_id.isin(pmd.index)]
    coffee = plaza[plaza.merchant_id == pmd.index[pmd.name.str.contains("Coffee")][0]].terminal_id.dropna().unique()
    wash = plaza[plaza.merchant_id == pmd.index[pmd.name.str.contains("Car Wash")][0]].terminal_id.dropna().unique()
    check("one coffee counter terminal and one car wash terminal", len(coffee) == 1 and len(wash) == 1)
    cof, wsh = coffee[0], wash[0]
    pv = G.victims_read_at(vic, opt6)
    sv = G.victims_read_at(vic, sco2)
    rest = set(vic) - pv - sv
    R["victims_by_source"] = {"pump": len(pv), "pinpad": len(sv), "background": len(rest)}
    check("205 counterfeit cards read at the pump in their lookback", len(pv) == 205, str(len(pv)))
    check("47 read at the PIN pad", len(sv) == 47, str(len(sv)))
    check("31 read at neither", len(rest) == 31, str(len(rest)))
    any_opt6 = set(a.card_token[(a.terminal_id == opt6)]) & set(vic)
    any_sco2 = set(a.card_token[(a.terminal_id == sco2)]) & set(vic)
    check("no PIN-pad or background card ever read at the pump terminal", any_opt6 == pv, str(len(any_opt6 - pv)))
    check("no pump or background card ever read at the PIN pad", any_sco2 == sv, str(len(any_sco2 - sv)))
    pf = sorted(vic[t] for t in pv)
    sf = sorted(vic[t] for t in sv)
    R["first_use_ranges"] = {"pump": [str(pf[0]), str(pf[-1])], "pinpad": [str(sf[0]), str(sf[-1])]}
    check("pump victims first used 24 Aug to 30 Sep", pf[0] == dt.date(2026, 8, 24) and pf[-1] <= dt.date(2026, 9, 30))
    check("PIN pad victims first used 28 Aug to 2 Oct", sf[0] >= dt.date(2026, 8, 28) and sf[-1] <= dt.date(2026, 10, 2))
    # travel in lookback
    away = set(md.index[(md.country != "CA") | (~md.province_state.isin(["ON"]))])
    cpres = a[a.pos_entry_mode.isin(G.CARD_PRESENT) & a.merchant_id.isin(away) & a.card_token.isin(list(vic))]
    cfr = G.cases()
    disputed = set(cfr.retrieval_ref)
    cpres = cpres[~cpres.retrieval_ref.isin(disputed)]
    trav = {t for t, d in zip(cpres.card_token, cpres.ldate) if vic[t] - dt.timedelta(60) <= d < vic[t]}
    R["travellers"] = {"background": len(trav & rest), "pinpad": len(trav & sv)}
    check("all 31 background cards were used outside Ontario in their lookback", len(trav & rest) == 31,
          str(len(trav & rest)))
    check("none of the 47 PIN pad cards was used outside Ontario in its lookback", len(trav & sv) == 0)

    # ---------------------------------------------------------------- the pooled screen (main column)
    look = lambda t: pooled.loc[t] if t in pooled.index else None
    L6, LC, LW, LS = (look(t) for t in (opt6, cof, wsh, sco2))
    R["pooled"] = {k: {"v": int(r.v), "b": int(r.b), "base_pct": round(100 * r.base, 2), "lift": round(float(r.lift), 2)}
                   for k, r in (("pump", L6), ("coffee", LC), ("car_wash", LW), ("pin_pad", LS))}
    R["pooled_n_active"] = pooled.attrs["n_act"]
    check("pump leads the pooled screen", L6.lift == pooled[pooled.v >= 10].lift.max(), f"{L6.lift:.2f}")
    check("pump lift at least 25", L6.lift >= 25, f"{L6.lift:.2f}")
    check("coffee counter second, at least 1.8x the twin", LC.lift >= 1.8 * LS.lift, f"{LC.lift:.2f} vs {LS.lift:.2f}")
    check("pump at least 2.5x the coffee counter", L6.lift >= 2.5 * LC.lift)
    check("twin: car wash and PIN pad read the same number of counterfeit cards (47)", LW.v == LS.v == 47,
          f"{LW.v} {LS.v}")
    check("twin: same member base", LW.b == LS.b, f"{LW.b} {LS.b}")
    check("twin: identical pooled lift", LW.lift == LS.lift, f"{LW.lift:.4f}")
    cof_v = G.victims_read_at(vic, cof)
    wsh_v = G.victims_read_at(vic, wsh)
    check("every coffee-counter counterfeit card was a pump card", cof_v <= pv, str(len(cof_v - pv)))
    check("every car-wash counterfeit card was a pump card", wsh_v <= pv, str(len(wsh_v - pv)))
    others = pooled[(pooled.v >= 10) & ~pooled.index.isin([opt6, cof, wsh, sco2])]
    R["pooled_max_other"] = {"terminal": str(others.index[0]), "name": name(others.index[0]), "v": int(others.v.iloc[0]),
                             "lift": round(float(others.lift.iloc[0]), 2)}
    check("every other terminal with 10+ counterfeit cards has lift at most 3", others.lift.max() <= 3.0,
          f"{others.lift.max():.2f}")
    check("twin stands at least 1.4x above every other 10+ terminal", LS.lift >= 1.4 * others.lift.max())

    # residual screens
    r78 = {k: f for k, f in vic.items() if k not in pv}
    sc78 = G.screen(r78)
    s78 = sc78.loc[sco2]
    R["residual78"] = {"pin_pad": {"v": int(s78.v), "share_pct": round(100 * s78.share_v, 1),
                                   "base_pct": round(100 * s78.base, 2), "lift": round(float(s78.lift), 2)}}
    check("78 cards left after the pump", len(r78) == 78)
    check("PIN pad reads 47 of the 78", s78.v == 47)
    check("coffee counter and car wash read none of the 78", cof not in sc78.index and wsh not in sc78.index)
    nxt = sc78[(sc78.v >= 3) & (sc78.index != sco2)]
    R["residual78"]["next"] = {"terminal": str(nxt.index[0]), "name": name(nxt.index[0]), "v": int(nxt.v.iloc[0]),
                               "lift": round(float(nxt.lift.iloc[0]), 2)}
    check("PIN pad leads the residual screen by 1.3x over any terminal with 3+ cards", s78.lift >= 1.3 * nxt.lift.max(),
          f"{s78.lift:.2f} vs {nxt.lift.max():.2f}")
    r31 = {k: f for k, f in r78.items() if k not in sv}
    sc31 = G.screen(r31)
    m31 = sc31[sc31.v >= 3]
    R["residual31_max_lift_3plus"] = round(float(m31.lift.max()), 2) if len(m31) else 0.0
    check("after both sources, no terminal with 3+ of the 31 cards has lift above 3", (m31.lift <= 3.0).all(),
          f"{m31.lift.max() if len(m31) else 0:.2f}")
    m31b = sc31[sc31.v >= 2]
    R["residual31_max_lift_2plus"] = round(float(m31b.lift.max()), 2) if len(m31b) else 0.0

    # ---------------------------------------------------------------- the answer and the rungs
    ans = s["reissue"]
    R["answer"] = ans
    n_pump = count([opt6])
    n_pp = count([sco2])
    ov = len((exp_set(opt6) & G.open_cards()) & (exp_set(sco2) & G.open_cards()))
    R["by_terminal"] = {"pump": n_pump, "pin_pad": n_pp, "overlap": ov}
    check("answer is the union of the two terminals' open exposed cards", ans == n_pump + n_pp - ov)
    check("overlap between the two terminals of 5 to 20 cards", 5 <= ov <= 20, str(ov))
    rungs = {"pump only (rung 1, 1b)": [opt6], "pump and coffee (rung 0)": [opt6, cof],
             "pump, coffee and car wash": [opt6, cof, wsh], "all four (rung 0)": [opt6, cof, wsh, sco2]}
    R["rungs"] = {}
    for k, tids in rungs.items():
        n = count(tids)
        R["rungs"][k] = {"cards": n, "pct": round(pct(n, ans), 1)}
        check(f"rung {k}: {n} is at least 6 per cent from {ans}", abs(pct(n, ans)) >= 6.0, f"{pct(n, ans):+.1f}%")
    check("rung 1 under-counts and rung 0 over-counts (bracketing)",
          R["rungs"]["pump only (rung 1, 1b)"]["cards"] < ans < R["rungs"]["pump and coffee (rung 0)"]["cards"])
    # other readings of the count
    alt = {}
    n_all, toks_all = G.reissue([opt6, sco2], vic, status="none")
    alt["no status filter (CP-14 s6)"] = n_all
    alt["only the counterfeit cards removed (CP-14 s6)"] = G.reissue([opt6, sco2], vic, status="drop_victims")[0]
    alt["all card-present reads count (CP-14 s3)"] = count([opt6, sco2], modes="cp")
    alt["terminals summed, overlap counted twice (CP-14 s2)"] = n_pump + n_pp
    R["readings"] = {k: {"cards": v, "pct": round(pct(v, ans), 1)} for k, v in alt.items()}
    for k, v in alt.items():
        if "overlap" in k:
            check(f"reading '{k}' differs and is a unit violation", v != ans, f"{v} ({pct(v, ans):+.1f}%)")
        else:
            check(f"reading '{k}' at least 6 per cent away", abs(pct(v, ans)) >= 6.0, f"{v} ({pct(v, ans):+.1f}%)")
    # convergent readings
    for edge in ("eastern_dates", "utc_dates"):
        n = G.reissue([opt6, sco2], vic, edge=edge)[0]
        check(f"window edges converge: {edge}", n == ans, str(n))
    only05 = a[a.terminal_id.isin([opt6, sco2]) & a.pos_entry_mode.isin(["80", "90"])]
    t0a, t1a = G.window(opt6, vic)
    t0b, t1b = G.window(sco2, vic)
    inw = only05[((only05.terminal_id == opt6) & (only05.txn_datetime_utc >= t0a) & (only05.txn_datetime_utc <= t1a)) |
                 ((only05.terminal_id == sco2) & (only05.txn_datetime_utc >= t0b) & (only05.txn_datetime_utc <= t1b))]
    check("chip-only reading converges: no fallback or stripe read inside either window", len(inw) == 0, str(len(inw)))
    dec = a[a.terminal_id.isin([opt6, sco2]) & (a.response_code != "00")]
    dec = dec[((dec.terminal_id == opt6) & (dec.txn_datetime_utc >= t0a) & (dec.txn_datetime_utc <= t1a)) |
              ((dec.terminal_id == sco2) & (dec.txn_datetime_utc >= t0b) & (dec.txn_datetime_utc <= t1b))]
    check("approved-only reading converges: no declined message inside either window", len(dec) == 0, str(len(dec)))
    # window edges clean
    for tid, t0, t1, retire in ((opt6, t0a, t1a, dt.date(2026, 9, 1)), (sco2, t0b, t1b, dt.date(2026, 9, 15))):
        at = a[a.terminal_id == tid]
        after = at[at.txn_datetime_utc > t1]
        check(f"{tid}: no message after the last counterfeit-card read", len(after) == 0, str(len(after)))
        last_any = at.txn_datetime_utc.max()
        check(f"{tid}: terminal ID retired by {retire}", last_any.tz_convert(G.TZ).date() < retire)
        eve = pd.Timestamp(dt.datetime.combine(t0.tz_convert(G.TZ).date() - dt.timedelta(1), dt.time(20, 0)),
                           tz=G.TZ).tz_convert("UTC")
        before = at[(at.txn_datetime_utc >= eve) & (at.txn_datetime_utc < t0)]
        check(f"{tid}: nothing from 20:00 the evening before to the first counterfeit-card read", len(before) == 0)
        check(f"{tid}: window edges fall on the same day in UTC and Eastern time",
              t0.date() == t0.tz_convert(G.TZ).date() and t1.date() == t1.tz_convert(G.TZ).date())
        R.setdefault("windows", {})[tid] = [str(t0), str(t1)]

    # ---------------------------------------------------------------- the grid
    cols = [(L, b, m) for L in (45, 60, 90) for b in ("span", "period") for m in ("contact", "cp")]
    R["grid"] = {}
    nearest = (None, 1e9)
    for L, b, m in cols:
        key = f"L{L}_{b}_{m}"
        sc = G.screen(vic, L, b, m)
        seq = G.sequential(vic, L, b, m)[0]
        cov = G.set_cover(vic, L, b, m)[0]
        lgt = G.logistic(vic, L, b, m)[0]
        check(f"{key}: sequential attribution returns pump and PIN pad", seq == [opt6, sco2], str(seq))
        check(f"{key}: set cover returns pump and PIN pad", cov == [opt6, sco2], str(cov))
        if m == "contact":
            check(f"{key}: joint logistic returns pump and PIN pad", sorted(lgt) == sorted([opt6, sco2]), str(lgt))
        else:
            check(f"{key}: joint logistic keeps the pump", opt6 in lgt, str(lgt))
            R.setdefault("logistic_all_modes", {})[key] = lgt
        if m == "contact":
            check(f"{key}: coffee counter stands above the PIN pad", sc.loc[cof].lift > sc.loc[sco2].lift,
                  f"{sc.loc[cof].lift:.2f} vs {sc.loc[sco2].lift:.2f}")
        R["grid"][key] = {"lift": {k: round(float(sc.loc[t].lift), 2) for k, t in
                                   (("pump", opt6), ("coffee", cof), ("car_wash", wsh), ("pin_pad", sco2))},
                          "cells": {}}
        for floor in (0, 10):
            for thr in (3, 5, 8, 10, 15, 20, 30):
                sel = sc[(sc.lift > thr) & (sc.v >= max(floor, 1))]
                tids = list(sel.index)
                n = count(tids, modes=m) if tids else 0
                cell = f"floor{floor}_t{thr}"
                R["grid"][key]["cells"][cell] = {"terminals": len(tids), "cards": n}
                bad = set(tids) == {opt6, sco2}
                check(f"{key} {cell}: pooled set is not pump and PIN pad", not bad, str(len(tids)))
                d = abs(pct(n, ans))
                check(f"{key} {cell}: {n} cards, at least 6 per cent from the answer", d >= 6.0, f"{pct(n, ans):+.1f}%")
                if d < nearest[1]:
                    nearest = (f"{key} {cell}", d, n)
        if m == "cp":
            n = count([opt6, sco2], modes="cp")
            check(f"{key}: conditional terminals with all-mode exposure count far from the answer",
                  abs(pct(n, ans)) >= 6.0, f"{n}")
    R["nearest_grid_cell"] = {"cell": nearest[0], "pct": round(nearest[1], 1), "cards": nearest[2]}

    # ---------------------------------------------------------------- ask A
    A = G.ask_a()
    R["ask_a"] = A
    for k in ("Debit", "Credit"):
        for f in ("gross", "recovered", "net"):
            v = A[k][f]
            check(f"ask A {k} {f} is an exact cent figure", abs(round(v * 100) - v * 100) < 1e-6, f"{v:.2f}")
            check(f"ask A {k} {f} is not a round hundred", abs(v - round(v, -2)) > 0.5, f"{v:.2f}")
    stops = {"workbook amount as dollars (currency)": dict(currency="workbook"),
             "no de-duplication (re-opened cases)": dict(dedup="none"),
             "de-duplicated on card, merchant, amount and date": dict(dedup="card_merchant_amount_date"),
             "credits only (pre-arbitration ignored)": dict(recover="credits_only"),
             "every chargeback in the file": dict(scope="all_chargebacks")}
    R["ask_a_stops"] = {}
    for k, kw in stops.items():
        S_ = G.ask_a(**kw)
        R["ask_a_stops"][k] = S_
        moved = [(ct_, f) for ct_ in ("Debit", "Credit") for f in ("gross", "recovered", "net")
                 if abs(S_[ct_][f] - A[ct_][f]) >= 50.0]
        both = {ct_ for ct_, _ in moved} == {"Debit", "Credit"}
        check(f"ask A stop '{k}' moves debit and credit figures by $50 or more", both, str(moved))
    # ask B
    B = G.ask_b()
    R["ask_b"] = B
    bstops = {"UTC day as the report day": dict(clock="utc"), "calendar days": dict(calendar=True),
              "no holidays": dict(holidays_rule="none"), "re-opened case as a new claim": dict(reopen="new_claim")}
    R["ask_b_stops"] = {}
    for k, kw in bstops.items():
        S_ = G.ask_b(**kw)
        R["ask_b_stops"][k] = S_
        moved = [(ct_, f) for ct_ in ("Debit", "Credit") for f in ("within", "longest") if S_[ct_][f] != B[ct_][f]]
        check(f"ask B stop '{k}' moves debit and credit figures", {x for x, _ in moved} == {"Debit", "Credit"},
              str(moved))
        check(f"ask B stop '{k}' moves at least three of the four figures", len(moved) >= 3, str(moved))
    # the longest waits are re-opened claims (the committee paper says so)
    hol = set(G.holidays())
    wc = cfr[cfr.fraud_type == "Counterfeit"]
    for k in ("Debit", "Credit"):
        best = None
        for c_ in G.claims():
            if c_["refunded_on"] is None or ct[c_["card_token"]] != k:
                continue
            d0 = c_["first_report_utc"].tz_convert(G.TZ).date()
            while not G.is_bd(d0, hol):
                d0 += dt.timedelta(1)
            w_ = G.bd_wait(d0, c_["refunded_on"], hol)
            n_cases = wc[wc.card_token == c_["card_token"]].case_number.nunique()
            if best is None or w_ > best[0]:
                best = (w_, n_cases)
        check(f"ask B: the longest {k.lower()} wait is a re-opened claim", best[0] == B[k]["longest"] and best[1] >= 2,
              str(best))
    # a generic federal calendar (30 September) is not the credit union's
    hol_fed = set(G.holidays()) | {dt.date(2026, 9, 30)}
    _h = G.holidays
    G.holidays = lambda: frozenset(hol_fed)
    S_ = G.ask_b()
    G.holidays = _h
    R["ask_b_stops"]["federal 30 September counted as a holiday"] = S_
    check("ask B: the MS-3 calendar, not a federal one, decides at least one figure", S_ != B)

    # ---------------------------------------------------------------- decoupling and separation
    gold_a, gold_b = A, B
    saved = G.auth.__wrapped__ if hasattr(G.auth, "__wrapped__") else None
    full = G.auth()
    stripped = full[~full.terminal_id.isin([opt6, sco2, cof, wsh])]
    G.auth.cache_clear()
    G.auth = functools.lru_cache(maxsize=None)(lambda: stripped)
    a2, b2 = G.ask_a(), G.ask_b()
    G.auth = functools.lru_cache(maxsize=None)(lambda: full)
    check("decoupling: asks unchanged with every read at the four screened terminals removed",
          a2 == gold_a and b2 == gold_b)
    for fn in (G.ask_a, G.ask_b, G.claims, G.posted_cad):
        s_ = inspect.getsource(fn)
        check(f"decoupling: {fn.__name__} never reads terminal or entry-mode fields",
              "terminal_id" not in s_ and "pos_entry_mode" not in s_)
    dup = cfr[cfr.duplicated("retrieval_ref", keep=False)]
    v2 = cfr.drop_duplicates("retrieval_ref").query("fraud_type == 'Counterfeit'").groupby("card_token").txn_date.min().to_dict()
    check("separation: re-opened rows change no victim or first-use date", v2 == vic, str(len(dup)))
    lb_reads = full[full.card_token.isin(list(vic)) & full.retrieval_ref.isin(disputed)]
    inlb = [d < vic[t] for t, d in zip(lb_reads.card_token, lb_reads.ldate)]
    check("separation: no disputed transaction sits inside any lookback", not any(inlb), str(sum(inlb)))
    twins = cfr[cfr.fraud_type == "Counterfeit"].groupby(["card_token", "merchant_as_on_statement", "amount", "txn_date"]).retrieval_ref.nunique()
    R["twin_withdrawals"] = int((twins > 1).sum())
    check("genuine identical-looking withdrawals present on debit and credit cards",
          (twins > 1).sum() >= 5 and {ct[t] for t in twins[twins > 1].reset_index().card_token} == {"Debit", "Credit"})
    reo = cfr[cfr.fraud_type == "Counterfeit"].groupby("retrieval_ref").case_number.nunique()
    R["reopened_claims"] = int(cfr[cfr.retrieval_ref.isin(reo[reo > 1].index)].card_token.nunique())
    check("re-opened claims present", R["reopened_claims"] >= 6)
    neg = G.chargebacks()
    R["prearb_reversals"] = int((neg.amount_cad < 0).sum())
    check("credits taken back at pre-arbitration present", (neg.amount_cad < 0).sum() >= 4)
    usd = full[full.retrieval_ref.isin(disputed) & (full.currency_txn == "840")]
    check("US dollar counterfeit transactions present on both card types",
          {ct[t] for t in usd.card_token} == {"Debit", "Credit"})
    # first use agrees between the workbook and the log
    cfl = full[full.retrieval_ref.isin(set(cfr[cfr.fraud_type == 'Counterfeit'].retrieval_ref)) &
               (full.response_code == "00")]
    f_log = cfl.groupby("card_token").ldate.min().to_dict()
    check("first counterfeit date agrees between the workbook and the log", f_log == vic)

    # ---------------------------------------------------------------- the write-up and the shipped text
    task = os.path.dirname(G.HERE)
    sub_p = os.path.join(task, "submission.md")
    if os.path.exists(sub_p):
        import re
        sub = open(sub_p).read()
        money = lambda x: "${:,.2f}".format(x)
        owed = [str(ans), "205", "78", "47", str(n_pump), str(n_pp), str(ov), opt6, sco2,
                "5 August 2026", "31 August 2026", "13 August 2026", "14 September 2026"]
        for k in ("Debit", "Credit"):
            owed += [money(A[k][f]) for f in ("gross", "recovered", "net")]
            owed += ["%d counterfeit cases refunded" % B[k]["within"], "%d business days" % B[k]["longest"]]
        for tok in owed:
            check(f"submission states {tok}", tok in sub)
        allowed = set(owed) | {"283", "60", "2026", "05", "80", "90", "24", "4", "5", "6", "7", "8", "10", "13", "14",
                               "31", "1", "2", "3", "181"}
        # figures in the prose: file and column names in backticks are not figures, and a number never starts
        # inside an identifier (LT723511) or swallows the comma that ends a clause
        prose = re.sub(r"`[^`]*`", " ", sub)
        nums = set(re.findall(r"(?<![A-Za-z0-9])\$?\d+(?:,\d{3})*(?:\.\d+)?", prose))
        stray = sorted(n for n in nums if n not in allowed and not any(n in o for o in owed))
        check("submission carries no figure outside the owed set", not stray, str(stray))
    texts = {"prompt.md": open(os.path.join(task, "prompt.md")).read()}
    for nm in ("submission.md", "DESIGN_NOTE.md"):
        if os.path.exists(os.path.join(task, nm)):
            texts[nm] = open(os.path.join(task, nm)).read()
    from pypdf import PdfReader
    from docx import Document
    for fn in files:
        p_ = os.path.join(G.TARGET, fn)
        if fn.endswith((".md", ".txt", ".csv")):
            texts[fn] = open(p_).read()
        elif fn.endswith(".pdf"):
            texts[fn] = "\n".join(pg.extract_text() or "" for pg in PdfReader(p_).pages)
        elif fn.endswith(".docx"):
            texts[fn] = "\n".join(par.text for par in Document(p_).paragraphs)
    gold_dir = os.path.join(task, "golden")
    if os.path.isdir(gold_dir):
        for fn in sorted(os.listdir(gold_dir)):
            if fn.endswith(".pdf"):
                texts["golden/" + fn] = "\n".join(pg.extract_text() or "" for pg in PdfReader(os.path.join(gold_dir, fn)).pages)
    for nm, t in texts.items():
        check(f"no em dash in {nm}", "\u2014" not in t)

    print(f"\n{len(PASSES)} passed, {len(FAILS)} failed")
    import tempfile
    out = os.environ.get("T181_RESULTS", os.path.join(tempfile.gettempdir(), "t181_checks.json"))
    with open(out, "w") as fh:
        json.dump(R, fh, indent=1, default=str)
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
