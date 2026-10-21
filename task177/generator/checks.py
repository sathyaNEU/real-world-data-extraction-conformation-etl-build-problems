"""task177 checks: the generator's own assertions on the built pack and on the clean truth behind it.

    python3 task177/generator/checks.py <target>

The three-rules block (R1 to R3c), the ladder on the pack, the golden's family and bin, the one-sigma move, every
semantic-fork row (SF), the Layer 1 items mishandled one at a time, the ask devices and the separation line, the
distractors, the input gates and the realism sweep. Exit 1 on any FAIL."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as K       # noqa: E402
import common as C     # noqa: E402
import docs as DOC     # noqa: E402
import model as M      # noqa: E402

ROWS = []


def check(label, ok, detail=""):
    ROWS.append((label, bool(ok), detail))
    print("%-4s %-58s %s" % ("PASS" if ok else "FAIL", label, detail), flush=True)


def in_bin(v, target_pct):
    """the forecast prints in the golden's cell: the nearest 5 per cent, as the prompt asks"""
    return C.pct5(v) == target_pct


# the pack the stage 4 readers and judge saw (target.zip 2c536aaa): the files the call reads that no ask touches; the
# acceptance summary left the list in round 4, when its resolved count re-centred the forecast in its cell
JUDGED = {
    "claims_register_2026.csv": "be407db35fc60906d6c75ea4265a610dcde1b03caa85e48726d707335972d9c2",
    "contact_details_crosswalk.csv": "540a58def6081741c0c7409e6b686e310ffc66eca0dbf24d43559a2fb9faf208",
    "contact_legs_2026.csv": "ec5472f533e9a09afb79a17b6634eb69200ddeede60e70f85a7e7df69b11b118",
    "overflow_episodes_2026.csv": "64364c04a67d34d7131bdf1eb48e005bdce6cbe2146e673e058b6581ef69f07d",
    "post_contact_survey_2026.csv": "7efb9911d46ea03cfe6fc8bfe493bb2650cf5858643f2ae413f7b2998ad74266",
    "telephony_migration_codes.xlsx": "c5500172f1e136515f510eb515c068b4726d54d65c49d1420dfd9b8ee1e22b94",
    "usage_tier_order_form_2027.pdf": "f641b76233e2726fb3a66e2e03517b1215e619a71abb1b9941bdb9091a782358",
}
JUDGED_SESSIONS = "abce448196c2b03e7c268d0405abf37ff48440ee19c5e51fdc1f18f299a289cf"


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def golden_of(D, fi, rows, spec="split", reps=200, seed=17, P=None, fit_rows=None, aux_over=None, pop=None):
    S, aux = K.inputs(D, rows)
    aux["p_new"], aux["cycle"] = fi["p_new"], fi["cycle"]
    if aux_over:
        aux.update(aux_over)
    fit_on = None
    if fit_rows is not None:
        fit_on, _ = K.inputs(D, fit_rows)
    o = K.forecast(D, spec=spec, reps=reps, seed=seed, S=S, aux=aux, P=P, fit_on=fit_on, pop=pop)
    return o


def main(target):
    D = K.load(target)
    fi = K.filed_inputs(target)
    rows = K.contacts(D)
    figs = json.load(open(os.path.join(HERE, "figures.json"))) if os.path.exists(os.path.join(HERE, "figures.json")) \
        else None
    gold = golden_of(D, fi, rows, reps=400)
    g = gold["share"]
    G = C.pct5(g)
    P = gold["P"]
    check("golden: the share of own contacts started in the assistant", True,
          "%.4f, printed %d per cent (nearest 5)" % (g, G))
    check("golden: inside its cell by a point or more (the nearest 5 per cent)", C.edge(100 * g, C.FORECAST_UNIT) >= 1.0,
          "edge distance %.3f" % C.edge(100 * g, C.FORECAST_UNIT))
    if figs:
        check("figures.json carries the golden", figs["call_share"] == G, "%s" % figs["call_share"])

    # ------------------------------------------------------------------------------------- R1: the raw material
    check("R1 the golden reads row-level contacts from the two exports", len(rows) > 300000,
          "%d contacts rebuilt from %s and %s" % (len(rows), C.F_LEGS, C.F_CONV))
    heads = []
    for f in os.listdir(target):
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                heads += next(csv.reader(fh))
    with open(os.path.join(target, C.F_CONV), encoding="utf-8") as fh:
        heads += list(json.loads(fh.readline()).keys())
    bad = [h for h in heads if re.search(r"forced|imposed|learn|propens|prefer|q_val|_rate|ratio|weight", h, re.I)]
    check("R1 no shipped column holds the deciding quantity", not bad, ", ".join(bad) or "none")
    n_red = sum(r[3] for r in rows)
    check("R1 the transfers the decisive step reads are a minority of the contacts", n_red / len(rows) < 0.05,
          "%d of %d" % (n_red, len(rows)))

    # ----------------------------------------------------------------------------- R3: the analyst test (clean truth)
    import pack as PK
    import world as W
    world, rec = PK.records()
    R = world.R
    ct = world.ct
    cl = world.claims
    S_t = M.Seq(ct.who, R["choice"], R["red"], R["res"].astype(float))
    pop = world.pop
    op = [cl.opened[i].astype(dt.date) for i in pop]
    sch = np.array([K.schedule(o, fi["cycle"]) for o in op])
    lo = np.maximum(cl.opened, np.datetime64(C.REC_START))
    hi = np.minimum(cl.closed, np.datetime64(C.REC_END) + np.timedelta64(1, "D"))
    days_open = np.maximum((hi - lo).astype(int), 0)
    adhoc = float((~ct.kind).sum() / days_open.sum())
    p_phone = float(R["res"][~R["choice"] & ~R["red"]].mean())
    p_over = float(R["red"].sum() / (~R["choice"]).sum())
    has = np.array([i in S_t.index for i in pop])
    rws = np.array([S_t.index.get(i, 0) for i in pop])

    def clean_forecast(spec, Pt=None, reps=200):
        if Pt is None:
            Pt, _, _ = M.fit(S_t, M.SPECS[spec])
        _, st = M.run(Pt, S_t, M.SPECS[spec], want_ll=False)
        qb = np.where(has, st["qb"][rws], Pt["q0b"])
        qp = np.where(has, st["qp"][rws], Pt["q0p"])
        la = np.where(has, st["last"][rws], 0.0)
        return M.simulate(Pt, M.SPECS[spec], qb, qp, la, np.full(pop.size, adhoc), K.AF_DAYS, K.WIN_DAYS,
                          fi["p_new"], p_phone, p_over, reps=reps, seed=23, sched_af=sch[:, 0],
                          sched_free=sch[:, 1])["share"], Pt
    easy, P_easy = clean_forecast("one_rate")
    check("R3a analyst test: one learning rate on the clean truth files the wrong answer",
          C.pct5(easy) >= G + 10, "%.4f (%d per cent) against the golden's %d" % (easy, C.pct5(easy), G))
    right, P_right = clean_forecast("split")
    check("R3b the decisive step alone (a separate rate for transfers) files the golden on the clean truth",
          in_bin(right, G), "%.4f" % right)
    tn, _ = clean_forecast("teach_nothing")
    P_as = dict(P_right)
    P_as["a_forced"] = P_right["a_free"]
    asc, _ = clean_forecast("split", Pt=P_as)
    check("R3b transfers taught nothing (a lower rung's correction) stays wrong", C.pct5(tn) <= G - 5,
          "%.4f" % tn)
    check("R3b transfers learned at the chosen rate stays wrong", C.pct5(asc) >= G + 10, "%.4f" % asc)
    truth = W.forecast_truth(cl, R, world.P, reps=12)
    check("R3 the clean truth's own window lands in the golden's bin", in_bin(truth["share"], G),
          "%.4f" % truth["share"])
    # R3c: no plant, no repeated block, no copied stream
    daily = {}
    for r in rows:
        k = C.to_local(r[1]).date()
        daily[k] = daily.get(k, 0) + 1
    vals = [daily[k] for k in sorted(daily)]
    blocks = set()
    rep = 0
    for i in range(0, len(vals) - 7):
        b = tuple(vals[i:i + 7])
        rep += b in blocks
        blocks.add(b)
    check("R3c no repeated block of daily contacts", rep == 0, "%d repeats of a 7-day block" % rep)
    names = " ".join(os.listdir(target)).lower()
    check("R3c no memo, draft or briefing file", not re.search(r"memo|draft|brief|notes?\b|known", names), names[:80])

    # ------------------------------------------------------------------------------------------- the ladder (pack)
    S, aux = K.inputs(D, rows)
    aux["p_new"], aux["cycle"] = fi["p_new"], fi["cycle"]
    fits = {}
    for name in ("one_rate", "teach_nothing", "split_no_persev", "split_persev_exp", "split_q0", "one_rate_q0"):
        Pn, ll, _ = M.fit(S, M.SPECS[name])
        fits[name] = (Pn, ll)
    ll_g = M.run(P, S, M.SPECS["split"])[0]
    o1 = K.forecast(D, spec="one_rate", reps=200, S=S, aux=aux, P=fits["one_rate"][0])["share"]
    check("L0 rung 0, one learning rate (the default path), files its own wrong answer", C.pct5(o1) >= G + 10,
          "%.4f (%d)" % (o1, C.pct5(o1)))
    check("L0 the split model beats one rate on the record by a visible margin", ll_g - fits["one_rate"][1] > 300,
          "%.1f log-likelihood units" % (ll_g - fits["one_rate"][1]))
    g_fix, g_est = ll_g - fits["one_rate"][1], fits["split_q0"][1] - fits["one_rate_q0"][1]
    check("L0 the gain over one rate clears the write-up's floor, starting values fixed or estimated",
          figs is None or min(g_fix, g_est) > figs["ll_gain_floor"],
          "%.1f and %.1f against %s" % (g_fix, g_est, figs and figs["ll_gain_floor"]))
    otn = K.forecast(D, spec="teach_nothing", reps=200, S=S, aux=aux, P=fits["teach_nothing"][0])["share"]
    check("L1 transfers teach nothing: outside the bin", C.pct5(otn) <= G - 5, "%.4f" % otn)
    check("L1 the record rejects transfers teaching nothing", ll_g - fits["teach_nothing"][1] > 30,
          "%.1f units" % (ll_g - fits["teach_nothing"][1]))
    ope = K.forecast(D, spec="split_persev_exp", reps=200, S=S, aux=aux, P=fits["split_persev_exp"][0])["share"]
    check("L2 pull to the last channel met (a form of the split): rejected by the record%s" % (
          ", and at the nearest 5 per cent it prints the golden's cell" if in_bin(ope, G) else " and outside the bin"),
          ll_g - fits["split_persev_exp"][1] > 30, "%.1f units, %.4f" % (ll_g - fits["split_persev_exp"][1], ope))
    check("L every route without the decisive step stays out of the golden's cell",
          not any(in_bin(v, G) for v in (o1,)) and not in_bin(otn, G), "one rate %.4f, transfers teach nothing %.4f"
          % (o1, otn))
    check("L2 no pull to the last choice: rejected by the record", ll_g - fits["split_no_persev"][1] > 300,
          "%.1f units" % (ll_g - fits["split_no_persev"][1]))
    import ladder as LD
    lg = LD.logit_pooled(D, rows, S, aux, fi)
    check("L3 a pooled last-four logistic of the choice: outside the bin", C.pct5(lg) >= G + 5, "%.4f" % lg)
    mk = LD.markov_pooled(D, rows, S, aux, fi)
    check("L3 a pooled first-order Markov chain: outside the bin", C.pct5(mk) >= G + 5, "%.4f" % mk)
    nl = LD.no_learning(D, rows)
    check("L4 no learning (the last eight weeks of 2026 carried): outside the bin", C.pct5(nl) <= G - 10, "%.4f" % nl)
    rh = LD.rate_hat(D, rows, S, aux, P)
    check("L5 contacts from each jobseeker's 2026 rate, check-ins ignored (against plan 4.1): the same call",
          in_bin(rh, G), "%.4f" % rh)

    # ------------------------------------------------------------------------- the golden's family on the pack
    fam, fam_af, fam_ratio, fam_rates = {}, {}, {}, {}

    def fam_add(k, o):
        fam[k], fam_af[k] = o["share"], o["share_af"]
        fam_ratio[k] = o["P"]["a_forced"] / o["P"]["a_free"]
        fam_rates[k] = (o["P"]["a_free"], o["P"]["a_forced"])
    fam_add("second Monte Carlo seed", golden_of(D, fi, rows, reps=400, seed=5, P=P))
    fam_add("starting values estimated", golden_of(D, fi, rows, spec="split_q0", P=fits["split_q0"][0]))
    popd = K.population(D)
    fam_add("fitted on the planning population only", golden_of(D, fi, rows, fit_rows=[r for r in rows if r[0] in popd]))
    cut = dt.datetime(2026, 11, 1, 6)
    fam_add("fitted on contacts to 31 October", golden_of(D, fi, rows, fit_rows=[r for r in rows if r[1] < cut]))
    fam_add("no overflow transfers after 1 March", golden_of(D, fi, rows, P=P, aux_over=dict(p_over=0.0)))
    fam["questions at each jobseeker's own 2026 rate"] = LD.adhoc_own(D, rows, S, aux, P)
    fam["claims closing at the register's 2026 rate"] = LD.with_closures(D, rows, S, aux, P)
    for k, v in fam.items():
        check("F family: %s" % k, in_bin(v, G), "%.4f" % v)
    GA = C.pct(gold["share_af"])
    check("F family: the assistant-first weeks' share prints the golden's whole per cent in every member",
          all(C.pct(v) == GA for v in fam_af.values()) and (figs is None or figs["share_af"] == GA),
          "%d: %s" % (GA, ", ".join("%.4f" % v for v in fam_af.values())))
    check("F family: the transfers' rate is about a fifth of the chosen rate in every fit",
          all(int(round(1 / r)) == 5 for r in fam_ratio.values()),
          "%s; chosen %.4f to %.4f, transfers %.4f to %.4f" % (
              ", ".join("%.3f" % r for r in fam_ratio.values()), min(a for a, _ in fam_rates.values()),
              max(a for a, _ in fam_rates.values()), min(b for _, b in fam_rates.values()),
              max(b for _, b in fam_rates.values())))
    # the one-sigma move of the transfer rate
    lo_s, hi_s = LD.one_sigma(D, rows, S, aux, P)
    check("F one standard error of the transfer rate leaves the printed share", in_bin(lo_s, G) and in_bin(hi_s, G),
          "%.4f to %.4f" % (lo_s, hi_s))

    # ------------------------------------------------------------------------------- R2: Layer 1 mishandled
    r2 = {}
    for label, alt, alt_pop in LD.mishandlings(D, rows):
        v = golden_of(D, fi, alt, pop=alt_pop)["share"]
        r2[label] = v
        check("R2 %s: the call holds" % label, in_bin(v, G), "%.4f" % v)
    check("R2 the overflow log and the transfer legs mark the same calls", LD.log_matches_transfers(D, target),
          "every transfer inside a logged episode and every claimant-queue call in one transferred")
    unl = LD.unlinked_internal(D)
    check("R2 the internal accounts typed claimant never join a case", unl == 0, "%d conversations join" % unl)

    # ---------------------------------------------------------------------------------- SF: semantic fork rows
    ev = LD.semantic_forks(D, fi, rows, G, golden_of, P)
    check("SF1 contacts jobseekers start themselves: plan 5.1 defines them", ev["plan51a"])
    check("SF2 a transfer is a call, not an assistant start: plan 5.1", ev["plan51b"])
    check("SF3 a conversation counts once: plan 5.2, and every-session reading holds the call",
          ev["plan52"] and in_bin(r2["every session counted as a contact"], G))
    check("SF4 the population is the register on 3 January 2027: the prompt", ev["prompt_pop"])
    check("SF5 nobody joining after 3 January: the prompt's date, and no member opened later", ev["prompt_pop"] and
          ev["no_later"])
    check("SF6 the window's edges on UTC dates: same call", in_bin(ev["sf6"], G), "%.4f" % ev["sf6"])
    check("SF7 the assistant-first routing covers calls only: plan 2.1 and 2.3", ev["plan21_23"])
    check("SF8 release 4.0's resolution is the acceptance test's, its intents reweighted the same call",
          ev["accept"] and in_bin(ev["sf8b"], G), "%.4f" % ev["sf8b"])
    check("SF9 the phone's resolution from July to December only: same call", in_bin(ev["sf9"], G), "%.4f" % ev["sf9"])
    check("SF10 the overflow off from 1 March: same call; plan 3.2 keeps it on", ev["plan32"] and in_bin(ev["sf10"], G),
          "%.4f" % ev["sf10"])
    check("SF11 check-ins every 14 days on their due dates: plan 4.1; own 2026 rates, check-ins ignored, the same call",
          ev["plan41"] and in_bin(rh, G))
    check("SF12 rounding once at the end: the prompt's closing sentence", ev["prompt_round"])
    check("SF13 the contacts' order on one clock or read unconverted: same call",
          in_bin(r2["sessions' times read as UTC"], G))
    check("SF14 calls keyed by the case number or the caller's number: same call",
          in_bin(r2["calls keyed by the caller's number"], G))
    check("SF15 release 4.0 resolves the conversations jobseekers open at its acceptance rate: plan 1.3; the 2026 rate "
          "kept for them files another call", ev["plan13"] and not in_bin(ev["sf15"], G),
          "%.4f with the 2026 rate %.3f" % (ev["sf15"], ev["p_chat26"]))
    check("SF16 a transfer after 1 March meets release 4.0 on the voice service: plan 1.3", ev["plan13"],
          "%.4f with the 2026 voice rate %.3f" % (ev["sf16"], ev["p_voice26"]))
    # round 3's judge: the readings an outside reproduction took, under the conventions plan 4.1 and 5.1 now file
    jr = LD.judge_readings(D, fi, rows, golden_of, P, S)
    for label, (v, closed) in jr.items():
        if in_bin(v, G):
            check("J3 %s: the same call at the nearest 5 per cent" % label, True, "%.4f" % v +
                  (" (the record rejects the form by %.1f units)" % closed if not isinstance(closed, bool) else ""))
        elif closed is True:
            check("J3 %s: another call, and the plan's filed sentence rules it out" % label,
                  ev["plan41"] if "check-in" in label else ev["plan51a"] and ev["plan51b"], "%.4f" % v)
        else:
            check("J3 %s: another call, from a model form the record rejects" % label,
                  not isinstance(closed, bool) and closed > 30, "%.4f, rejected by %.1f units" % (v, closed))
    late_mix = [v for k, v in jr.items() if k.startswith("check-ins late as in 2026")][0][0]
    check("SF17 the denominator is every contact started: plan 5.1; transferred calls left out, the same call",
          ev["plan51a"] and in_bin(jr["transfers left out of the denominator"][0], G),
          "%.4f" % jr["transfers left out of the denominator"][0])
    check("SF18 a check-in on its due date: plan 4.1; as late as 2026's, the same call", ev["plan41"] and
          in_bin(late_mix, G), "%.4f" % late_mix)
    check("SF19 the other contacts at the 2026 rate or the last eight weeks': the same call",
          in_bin(jr["other contacts at the last eight weeks' rate"][0], G),
          "%.4f" % jr["other contacts at the last eight weeks' rate"][0])
    # round 4's diagnosis: an outsider's re-implementation of the same model class, choice by choice
    orr = LD.outsider_readings(D, fi, rows, golden_of, P, S)
    sf = {"the values started at 0 rather than halfway": "SF20", "the values started at 1 rather than halfway": "SF20",
          "the assistant-first calls setting the pull to the assistant they met": "SF21",
          "the transferred calls' choice left out of the likelihood": "SF22",
          "the jobseekers with no 2026 contact at the others' mean state": "SF23",
          "both of the open readings together": "SF22, SF23"}
    for label, (v, kind, gap) in orr.items():
        tag = sf.get(label, "SF24")
        if kind == "c":
            check("%s (c, open) %s: inside the golden's cell by a point or more" % (tag, label),
                  in_bin(v, G) and C.edge(100 * v, C.FORECAST_UNIT) >= 1.0,
                  "%.4f, edge %.2f" % (v, C.edge(100 * v, C.FORECAST_UNIT)))
        elif kind == "a":
            check("%s (a, filed) %s: plan 3.3 files the phone's outcome%s" % (
                tag, label, ", and the reading prints the same call" if in_bin(v, G) else ""), ev["plan33"], "%.4f" % v)
        else:
            check("%s (b, settled) %s: the record rejects it by %.1f units%s" % (
                tag, label, gap, ", and it prints the same call" if in_bin(v, G) else ""), gap > 30, "%.4f" % v)
    check("J3 the round 3 judge's own figures (25.8, 26.4 to 27.2, reported on 8ab100af, not recomputed) sit in the cell",
          all(C.pct5(x / 100) == G for x in (25.8, 26.4, 27.2)), "cell %.1f to %.1f" % (G - 2.5, G + 2.5))

    # --------------------------------------------------------------------------------------------- the asks
    emp, own = K.ask_counts(D, bn=fi["bn"], vendor_bn=fi["vendor_bn"])
    truth_emp, truth_own = __import__("ask").golden_counts(rec)
    check("A the employers' counts equal the generator's truth", emp == truth_emp, "%s" % emp)
    check("A our own use equals the generator's truth", own == truth_own, "%s" % own)
    dev = LD.ask_devices(D, fi, emp, own)
    for label, ok, detail in dev:
        check(label, ok, detail)
    # separation: no ask device row in the call's population
    sep = LD.separation(D, rows)
    for label, ok, detail in sep:
        check(label, ok, detail)
    # the stage 4 repair moved ask rows and the plan only: every file the call reads and no ask touches is the judged
    # pack's byte for byte, and so are the call's own session rows
    for f, h in JUDGED.items():
        check("J unchanged since the judged pack: %s" % f, sha(os.path.join(target, f)) == h, "")
    xw = {r["detail_value"] for r in D["xwalk"] if r["detail_type"] == "assistant_account"}
    hh = hashlib.sha256()
    with open(os.path.join(target, C.F_CONV), "rb") as fh:
        for line in fh:
            ss = json.loads(line)
            if ss["channel"] == "voice" or ss["account_ref"] in xw:
                hh.update(line)
    check("J the call's own session rows are the judged pack's", hh.hexdigest() == JUDGED_SESSIONS, "")

    # --------------------------------------------------------------- the default path's own back-test (card 1)
    bt = K.backtest(D, rows)
    check("B fitted to October, one rate predicts November and December's share within a point",
          abs(bt["one_rate"]["pred"] - bt["one_rate"]["obs"]) < 0.01,
          "%.4f against %.4f" % (bt["one_rate"]["pred"], bt["one_rate"]["obs"]))
    check("B the split predicts the held-out choices better", bt["split"]["ll"] - bt["one_rate"]["ll"] > 50,
          "%.1f units" % (bt["split"]["ll"] - bt["one_rate"]["ll"]))
    red = LD.heldout_reduced(D, rows, S)
    for k, v in red.items():
        check("B the record selects the learning model: the split beats a %s on held-out choices" % k,
              bt["split"]["ll"] - v > 300, "%.1f units" % (bt["split"]["ll"] - v))
    if figs:
        check("B figures.json carries the back-test", figs["bt_one_rate_pred"] == C.pct(bt["one_rate"]["pred"]) and
              figs["bt_ll_gain"] == int(round(bt["split"]["ll"] - bt["one_rate"]["ll"])), "")

    # ------------------------------------------------------------------------------------ registers and dates
    with open(os.path.join(target, C.F_MANIFEST), encoding="utf-8") as fh:
        listed = {r["file"] for r in csv.DictReader(fh)}
    check("H9 the manifest lists every shipped file but itself", listed == set(os.listdir(target)) - {C.F_MANIFEST},
          "%d listed" % len(listed))
    pull_utc = "2027-01-04T06:00:00Z"
    last_leg = max(lg["start_utc"] for lg in D["legs"])
    last_sess = max(s["started"] for s in D["sessions"])
    with open(os.path.join(target, C.F_SURVEY), encoding="utf-8") as fh:
        last_sv = max(r["sent_utc"] for r in csv.DictReader(fh))
    last_claim = max(max(r["opened"], r["closed"] or "") for r in D["claims"])
    check("H16 no leg, session, survey or claim dated after the record's last day",
          last_leg < pull_utc and last_sess < "2027-01-04T00:00:00" and last_sv < pull_utc and last_claim <= "2027-01-03",
          "%s, %s, %s, %s" % (last_leg, last_sess, last_sv, last_claim))

    # ------------------------------------------------------------------------------------ distractors and gates
    reads = set(K.READS)
    for f in C.DISTRACTORS:
        check("D distractor never read by the golden: %s" % f, f not in reads and os.path.exists(os.path.join(target, f)),
              "")
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[-1] for f in files})
    check("G input gate: 10 or more files", len(files) >= 10, "%d" % len(files))
    check("G input gate: 3 or more formats", len(fmts) >= 3, ", ".join(fmts))
    n_legs = sum(1 for _ in open(os.path.join(target, C.F_LEGS), encoding="utf-8")) - 1
    check("G input gate: a file of 25,000 rows or more", n_legs >= 25000, "%s %d rows" % (C.F_LEGS, n_legs))
    for label, ok, detail in LD.realism(D, target, rows):
        check(label, ok, detail)
    if figs:
        for label, ok, detail in LD.realism_figures(figs):
            check(label, ok, detail)
    for label, ok, detail in LD.documents(target, fi):
        check(label, ok, detail)

    fails = [r for r in ROWS if not r[1]]
    print("%s: %d checks, %d FAIL" % ("PASS" if not fails else "FAIL", len(ROWS), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
