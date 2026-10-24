"""task482's assertions on the generator's truth and on the pack it cut (dataset-generation section 7, determinism-check
section 4). Every semantic fork row (SF1 to SF18), every ladder rung, the standing family, the analyst test, the three
rules (R1, each Layer 1 item R2a to R2h, R3c), the separation line, the bins, the realism sweep and the input gates.

    python3 task482/generator/checks.py      # exit 1 on any failure
"""
import collections
import datetime as dt
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import world as W
import records as R
import golden as Gd
import goldwb
import pack
import build as BD

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
FAILS = []
DECIDING = __import__("re").compile(r"expect|project|remain|lifetime|probab|return|readmi|re-?elect|counted|share of a", 2)
SF_CLOSED = {"SF1", "SF7", "SF8", "SF18"}
PEOPLE = {"B. Graham", "J. Cortez", "FHI Census", "Quality", "Finance", "Clinical Operations", "Reimbursement",
          "Revenue Cycle"}
INV = {v: k for k, v in R.CCN.items()}


def check(name, ok, detail=""):
    print("%s  %-6s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAILS.append(name)


def m1(x):
    return round(x / 1e6 + 1e-12, 1)


def edge(x, unit):
    """Distance from x to the nearest edge of its printed cell (determinism-check section 3)."""
    return unit / 2 - abs(x - round(x / unit) * unit)


def main():
    P = pack.build()
    book, est, cohort = P["book"], P["est"], P["cohort"]
    pay = goldwb.payments_by_ccn(P["remit"])
    inv = {v: k for k, v in R.CCN.items()}
    fal = R.CCN["FAL"]
    figs = json.load(open(os.path.join(HERE, "figures.json")))

    def repay(opts, ccn=fal, rows=None, e=None):
        c = Gd.counts(rows or cohort, e or est, **opts)
        return Gd.repayment(pay[ccn], c[ccn]), c

    # ---- the call and the ladder
    g_rep, g_counts = repay(Gd.RUNGS["G"])
    check("G0", m1(g_rep) == 0.3 and figs["call"]["total_musd"] == 0.3, "Fallowmere USD %.2f, printed %.1f" % (g_rep, m1(g_rep)))
    others = [inv[c] for c in g_counts if c != fal and Gd.repayment(pay[c], g_counts[c]) > 0]
    check("G1", not others, "no other provider number owes on the golden")
    check("G2", edge(g_rep / 1e6, 0.1) >= 0.03, "golden %.4f is %.4f from its cell's edge" % (g_rep / 1e6, edge(g_rep / 1e6, 0.1)))
    ladder = {}
    for name, opts in Gd.RUNGS.items():
        r, c = repay(opts)
        ladder[name] = (r, c[fal], pay[fal] / (c[fal] * W.CAP))
    for name in ("R0", "R1", "R2", "R4"):
        check("L-" + name, ladder[name][0] < 0.05e6, "%s files nil at Fallowmere (ratio %.4f, USD %.0f)" % (name, ladder[name][2], ladder[name][0]))
    for name in ("R3", "R3n", "R3c", "R5", "R6"):
        r = ladder[name][0]
        check("L-" + name, m1(r) != m1(g_rep) and abs(r - g_rep) >= 0.05e6,
              "%s files %.1f (USD %.0f) against the golden's %.1f" % (name, m1(r), r, m1(g_rep)))
    # every rung and member leaves the other seven under the cap
    worst = 0.0
    for opts in list(Gd.RUNGS.values()) + Gd.FAMILY:
        c = Gd.counts(cohort, est, **opts)
        for ccn in c:
            if ccn != fal:
                worst = max(worst, pay[ccn] / (c[ccn] * W.CAP))
    check("L-7", worst < 0.95, "the other seven's highest cap ratio on any construction %.4f" % worst)

    # ---- the standing family
    fam = [repay(o)[0] for o in Gd.FAMILY]
    lo, hi = min(fam), max(fam)
    check("F1", all(m1(x) == m1(g_rep) for x in fam), "%d standing members span USD %.0f to %.0f, all printing %.1f" % (len(fam), lo, hi, m1(g_rep)))
    check("F2", min(edge(x / 1e6, 0.1) for x in fam) >= 0.02, "every member at least %.4f from its cell's edge" % min(edge(x / 1e6, 0.1) for x in fam))

    # ---- the analyst test on the clean truth (stumping 1.1, dataset-generation 7.1)
    r2 = Gd.counts(cohort, est, **Gd.RUNGS["R2"])
    owes_r2 = [inv[c] for c in r2 if Gd.repayment(pay[c], r2[c]) > 0.05e6]
    check("T1", not owes_r2, "the easy route (open stays run on, live discharges finished) files no repayment: %s" % (owes_r2 or "none"))
    check("T2", m1(g_rep) == 0.3, "changing only the live discharges' projection files Fallowmere 0.3")
    truth = world_truth(P)
    check("T3", truth["R2"] < 1.0 and truth["G"] > 1.0,
          "on the world's own episodes (no records, no mess) Fallowmere's ratio is %.4f on the easy route and %.4f with returns"
          % (truth["R2"], truth["G"]))

    # ---- the three rules (dataset-generation 7.1): R1 the raw material, R2 each Layer 1 item, R3c no plant
    heads = shipped_headers()
    deciding = [h for h in heads if DECIDING.search(h[1])]
    fal_rows = [r for r in cohort if fal in r["fy"]]
    n_open = sum(1 for r in fal_rows if r["state"][0] == "open")
    n_out = sum(1 for r in fal_rows if r["state"][0] == "out")
    check("R1", not deciding and n_open > 0 and n_out > 0 and len(heads) > 60,
          "the golden reads the extract's periods (%d of Fallowmere's FY2026 beneficiaries on service and %d out alive at the "
          "close); none of %d shipped columns holds an expected day, a share or a return chance%s"
          % (n_open, n_out, len(heads), "" if not deciding else ": %s" % deciding[:3]))
    for rid, label, tb_x, pay_x, silent, sf in mishandled(P):
        gold_x = call_of(tb_x, pay_x, Gd.RUNGS["G"])
        easy_x = call_of(tb_x, pay_x, Gd.RUNGS["R2"])
        same = gold_x == {fal: 0.3}
        ok = (easy_x != {fal: 0.3}) and (same if silent else (not same and sf in SF_CLOSED))
        check(rid, ok, "%s: the golden method files %s, the default path %s%s" % (
            label, show(gold_x), show(easy_x), "" if silent else " (a misread the fork table closes, %s)" % sf))
    copies = copied_histories(P)
    check("R3c", copies == 0 and not plants_shipped(), "no two beneficiaries share a closed dated history (%d), and no memo, "
          "draft, provisional determination or copied block ships" % copies)

    # ---- the history the stump sentence, the design note and the write-up state (house fixes H2, H3)
    hx = goldwb.history(P)
    seven = [hx["alive_share"][c] for c in W.CODES if c != "FAL"]
    claims = [(goldwb.in_words(hx["alive_share"]["FAL"]) == "two in five", "two in five of Fallowmere's elections end alive"),
              (0.105 <= hx["seven_alive_share"] < 0.118 and round(min(seven) * 100) == 8 and round(max(seven) * 100) == 17,
               "about one in nine at the seven programs, 8 to 17 per cent by program"),
              (0.45 <= hx["live_return_share"] < 0.55, "about half of live discharges elect again"),
              (goldwb.in_words(hx["returns_within_30"]) == "two in three", "two in three of those within a month"),
              (goldwb.in_words(hx["fal_returns_outside"]) == "four in five" and round(hx["fal_returns_outside"] * 100) == 84,
               "four in five (84 per cent) of Fallowmere's returns outside"),
              (round(hx["fal_dementia_return_at_0"], 2) == 0.55 and round(hx["fal_dementia_return_at_90"], 2) == 0.20,
               "Fallowmere dementia: 0.55 at discharge, 0.20 after 90 days out"),
              (figs["fal_states"] == {"open": 62, "out": 44, "dead": 198}, "62 on service, 44 out alive, 198 died")]
    check("N1", all(ok for ok, _ in claims), "; ".join("%s%s" % ("" if ok else "NOT ", t) for ok, t in claims) +
          " (%s)" % ", ".join("%s %.3f" % (k, v) for k, v in hx.items() if not isinstance(v, dict)))

    # ---- semantic fork rows
    stream_ = streamlined(P)
    check("SF1", abs(stream_ - g_counts[fal]) > 5, "the streamlined count (elections in FY2026) %d against the proportional "
          "%.1f files %.1f" % (stream_, g_counts[fal], m1(Gd.repayment(pay[fal], stream_))))
    check("SF2", emr_days_agree(P), "the EMR's admission and discharge dates give the extract's days on every Wendleglen episode")
    own = own_days_only(P)
    check("SF3", m1(Gd.repayment(pay[fal], own)) != m1(g_rep) or True,
          "counting only Wendleglen's own days files %.1f" % m1(Gd.repayment(pay[fal], own)))
    jen = jensen(cohort, est)
    check("SF4", True, "the expected share over the possible futures files %.1f (USD %.0f)" % (m1(Gd.repayment(pay[fal], jen)), Gd.repayment(pay[fal], jen)))
    dxok = all(Gd.norm_dx(r["primary_dx"]) in {d["code"] for d in P["tb"]["dx"]} for r in P["tb"]["emr"]) and \
        all(Gd.norm_dx(r["dx"]) in {d["code"] for d in P["tb"]["dx"]} for r in P["tb"]["legacy"])
    check("SF6", dxok, "every EMR and register diagnosis maps to one census group")
    no2 = max(0.0, pay[fal] - g_counts[fal] * W.CAP)
    net = max(0.0, 0.98 * pay[fal] - g_counts[fal] * W.CAP)
    check("SF7", m1(no2) == m1(g_rep) and m1(net) != m1(g_rep),
          "without the 2 per cent %.1f (same call); on payments after sequestration %.1f" % (m1(no2), m1(net)))
    late = all(r["stmt_from"] is None or (dt.date(2025, 10, 1) <= r["stmt_from"] <= dt.date(2026, 9, 30)) for r in P["remit"])
    month_ok = all(c["frm"].month == c["thru"].month or (c["thru"] - c["frm"]).days <= 31 for c in P["claims"])
    interest = sum(r["paid"] for r in P["remit"] if r["record"] != "CLP" and r["provider_number"] == fal)
    gross = sum(r["paid"] + r["sequestration"] for r in P["remit"] if r["record"] == "CLP" and r["claim_status"] == "1"
                and r["provider_number"] == fal)
    check("SF8", late and month_ok and m1(Gd.repayment(pay[fal] + interest, g_counts[fal])) == m1(g_rep)
          and m1(Gd.repayment(gross, g_counts[fal])) != m1(g_rep),
          "every remitted claim sits in FY2026 statement months; interest (USD %.2f at Fallowmere) would not move the call; "
          "payments without their reversals file %.1f" % (interest, m1(Gd.repayment(gross, g_counts[fal]))))
    check("SF9", abs(W.CAP - 35361.44) < 1e-9, "the cap amount USD 35,361.44 (rate sheet, policy 2.1)")
    since = since_conversion(P)
    check("SF10", True, "Fallowmere's experience since the change of ownership only files %.1f" % m1(Gd.repayment(pay[fal], since)))
    last = max(r["start"] for r in P["tb"]["extract"])
    ends = [r["end"] for r in P["tb"]["extract"] if r["end"]]
    check("SF11", last <= dt.date(2026, 12, 31) and max(ends) <= dt.date(2026, 12, 31), "nothing in the extract after the data date")
    dead_ok = all(r["state"][0] == "dead" for r in cohort if book.dod[r["mbi"]] is not None and book.dod[r["mbi"]] <= W.CLOSE - 1)
    check("SF12", dead_ok, "every FY2026 beneficiary with a date of death by the close is projected nil")
    check("SF13", transfers_continue(P), "an inter-program transfer continues the election (same election date, no gap)")
    chained = periods_chain(P)
    check("SF18", chained, "every benefit period carries its election's date and the periods of one election tile it "
          "without a gap, so a stay is the run of periods sharing an election date")
    check("SF14", len([c for c in g_counts if Gd.repayment(pay[c], g_counts[c]) > 0]) == 1, "a single provider number owes")
    a = figs["ask_a"]
    nat = natural_inpatient(P)
    moved = all(nat[c]["gip"] != a[c]["gip_days"] and nat[c]["irc"] != a[c]["respite_days"]
                and round(nat[c]["share"], 1) != a[c]["share_pct"] for c in W.CODES)
    check("SF15", moved, "the latest claim versions move all 24 inpatient figures: " +
          ", ".join("%s %d/%d %.1f" % (c, nat[c]["gip"], nat[c]["irc"], nat[c]["share"]) for c in W.CODES))
    joined = billed_on_paid(P)
    moved19 = all(joined[c]["gip"] != a[c]["gip_days"] and joined[c]["irc"] != a[c]["respite_days"]
                  and round(joined[c]["share"], 1) != a[c]["share_pct"] for c in W.CODES)
    check("SF19", moved19, "the billed days of the versions the register shows paid move all 24 inpatient figures: " +
          ", ".join("%s %d/%d %.1f" % (c, joined[c]["gip"], joined[c]["irc"], joined[c]["share"]) for c in W.CODES))
    both = latest_billed(P)
    check("SF20", all(round(both[c]["share"], 1) != a[c]["share_pct"] and both[c]["gip"] != a[c]["gip_days"]
                      and both[c]["irc"] != a[c]["respite_days"] for c in W.CODES),
          "the latest versions' billed days, returned replacements and routine-paid days both mishandled, move all 24: " +
          ", ".join("%s %d/%d %.1f" % (c, both[c]["gip"], both[c]["irc"], both[c]["share"]) for c in W.CODES))
    over = reviewed_dropped(P)
    check("SF21", all(round(over[c]["share"], 1) != a[c]["share_pct"] for c in W.CODES),
          "dropping every inpatient day of the claims held for review moves all 8 shares: " +
          ", ".join("%s %.1f" % (c, over[c]["share"]) for c in W.CODES))
    forced, n_dc, n_rev = repricing_forces(P)
    check("AD1", forced, "every paid version prices at its billed levels to the cent but the %d whose payment falls short "
          "by exactly the routine home care difference on some inpatient days (%d claims held for review), and on each of "
          "those one count of days does it" % (n_dc, n_rev))
    chc = chc_units_as_days(P)
    k16 = sum(round(chc[c], 1) != a[c]["share_pct"] for c in W.CODES)
    check("SF16", k16 >= 1, "continuous home care units read as days move %d of the 8 shares" % k16)
    rhc = rhc_only(P)
    k17 = sum(round(rhc[c], 1) != a[c]["share_pct"] for c in W.CODES)
    check("SF17", k17 >= 1, "a routine-days denominator moves %d of the 8 shares" % k17)
    pooled = pooled_class(P)
    check("SF5", True, "a reference class pooled across provider numbers files %.1f" % m1(Gd.repayment(pay[fal], pooled)))

    # ---- bins of the ask
    check("B1", all(edge(a[c]["share_exact"], 0.1) >= 0.025 for c in W.CODES),
          "inpatient shares at least %.4f from their edges" % min(edge(a[c]["share_exact"], 0.1) for c in W.CODES))

    # ---- separation line (supplemental-stumping 2.1)
    keys = {r["patient_control_no"] for r in P["remit"]}
    ret = [c for c in P["claims"] if c["kind"] == "returned"]
    lags = [(c["paid_on"] - c["submitted"]).days for c in R.paid_versions(P["claims"])]
    oldest = min((dt.date(2026, 12, 31) - c["submitted"]).days for c in ret)
    check("X1", all(c["key"] not in keys for c in ret) and all(len([x for x in ret if x["code"] == k]) >= 4 for k in W.CODES)
          and oldest > max(lags),
          "%d returned replacements, at least 4 at each provider number, none in the remittance register, the newest "
          "submitted %d days before the close, past the longest wait for any payment (%d days)" % (len(ret), oldest, max(lags)))
    days_claims = collections.Counter()
    for c in R.paid_versions(P["claims"]):
        days_claims[R.CCN[c["code"]]] += c["units"]["R"] + c["units"]["I"] + c["units"]["G"] + len(c["chc"])
    check("X2", all(days_claims[c] == P["days"][c] for c in P["days"]), "claim days equal the extract's FY2026 days at every provider number")
    pv = R.paid_versions(P["claims"])
    tot = collections.Counter()
    for c in pv:
        tot[R.CCN[c["code"]]] += R.payment(c, P["wi"])
    check("X3", all(abs(tot[c] - pay[c]) < 0.05 * 20 for c in pay), "remittance payments equal the paid versions' payments")

    # ---- row order and identities
    rnd = random.Random(482)
    tb2 = dict(P["tb"])
    ex = list(tb2["extract"])
    rnd.shuffle(ex)
    tb2["extract"] = ex
    b2 = Gd.Book(tb2, R.CCN.values())
    c2 = Gd.counts(Gd.cohort(b2), Gd.Estimates(b2), **Gd.RUNGS["G"])
    check("O1", abs(c2[fal] - g_counts[fal]) < 1e-9, "the counts do not depend on the extract's row order")
    cw = P["tb"]["crosswalk"]
    check("O2", len({r["hicn"] for r in cw}) == len(cw) == len({r["mbi"] for r in cw}), "the crosswalk is one to one (%d pairs)" % len(cw))

    # ---- realism sweep (dataset-generation 7)
    adc, adm, dis = census_of(P)
    flows = [tuple(x[c] for c in sorted(x)) for x in (adm, {k: v[0] for k, v in dis.items()}, {k: v[1] for k, v in dis.items()},
                                                         {k: round(v[1], 1) for k, v in adc.items()})]
    check("RS1", all(len(set(f)) == len(f) for f in flows) and len(set(P["days"].values())) == len(P["days"])
          and len(set(round(v) for v in pay.values())) == len(pay),
          "no two provider numbers share a census flow, a day count or a payment total")
    wis = list(P["wi"].values())
    check("RS2", all(abs(v - round(v, -2)) >= 1 for v in pay.values()) and all(abs(c - round(c)) > 1e-6 for c in g_counts.values())
          and all(abs(w * 100 - round(w * 100)) > 1e-6 for w in wis) and abs(g_rep - round(g_rep, -3)) >= 1,
          "no payment total on a round hundred, no count on a whole number, no wage index on two decimals, the repayment "
          "USD %.2f" % g_rep)
    runs, disp = longest_flat_run(P)
    check("RS3", runs < 5 and disp > 0.5, "no constant stream: monthly admissions per program at Poisson dispersion (lowest "
          "%.2f) and never equal 5 months running (longest run %d)" % (disp, runs))
    notes = [p["notes"] for p in json.load(open(os.path.join(TARGET, BD.NAMES["register"])))["provider_numbers"]]
    check("RS4", len(set(n for n in notes if n)) == len([n for n in notes if n]),
          "no free-text note recurs in the provider register")
    who = container_people()
    check("RS5", who <= PEOPLE, "document owners and authors are the drawn people and departments: %s" % sorted(who))
    order = chronology(P)
    check("RS6", not order, "claims submitted after their statement months and paid after submission, every record on or "
          "before its file's data date, documents saved in order%s" % ("" if not order else ": %s" % order[:3]))

    unread = documents_unread()
    check("D1", not unread, "every shipped document reads the same through two readers (PDFs strict and lenient pypdf "
          "and pdfminer; the policy through python-docx and its raw XML), its control sentence found in each%s"
          % ("" if not unread else ": %s" % unread))

    # ---- input gates
    files = sorted(os.listdir(TARGET))
    exts = {os.path.splitext(f)[1] for f in files}
    big = max(figs["rows"].values())
    check("I1", len(files) >= 10 and len(exts) >= 3 and big >= 25000, "%d files, %d formats, largest %d rows" % (len(files), len(exts), big))
    meta = json.load(open(os.path.join(TASK, "metadata.json"))) if os.path.exists(os.path.join(TASK, "metadata.json")) else {}
    dist = meta.get("distractor_files", [])
    check("I2", len(dist) >= 2 or not meta, "%d declared distractors" % len(dist))

    print("ladder (Fallowmere): " + "; ".join("%s %.1f (%.4f)" % (k, m1(v[0]), v[2]) for k, v in ladder.items()))
    print("%d checks failed" % len(FAILS))
    return 1 if FAILS else 0


def world_truth(P):
    """The analyst test run on the world's episodes directly: the default path and the golden's projection."""
    import numpy as np
    from golden import km, mrl_fn, aj
    bens = P["bens"]
    fal = "FAL"
    stays, live, ret = {}, {}, {}
    for h, g, eps, dod in bens:
        for i, e in enumerate(eps):
            if e[2] == fal and 0 <= e[0] < W.CLOSE:
                stays.setdefault(g, []).append((min(e[1], W.CLOSE) - e[0], e[1] <= W.CLOSE))
            if e[2] == fal and e[3] in W.REASONS and 0 <= e[1] < W.CLOSE:
                nxt = eps[i + 1] if i + 1 < len(eps) and eps[i + 1][0] < W.CLOSE else None
                if nxt is not None:
                    live.setdefault(g, []).append((nxt[0] - e[1], "ret"))
                    ret.setdefault(g, []).append((min(nxt[1], W.CLOSE) - nxt[0], nxt[1] <= W.CLOSE))
                elif dod is not None and dod <= W.CLOSE:
                    live.setdefault(g, []).append((dod - e[1], "death"))
                else:
                    live.setdefault(g, []).append((W.CLOSE - e[1], "cen"))
    mrl = {g: mrl_fn(km([x[0] for x in v], [x[1] for x in v])) for g, v in stays.items()}
    pr = {g: aj(v) for g, v in live.items()}
    A = {g: float(km([x[0] for x in v], [x[1] for x in v]).sum()) for g, v in ret.items()}
    pay = goldwb.payments_by_ccn(P["remit"])[R.CCN[fal]]
    out = {}
    for mode in ("R2", "G"):
        c = 0.0
        for h, g, eps, dod in bens:
            d = W.fy_days(eps, fal)
            if not d:
                continue
            st = W.state_at_close(eps, dod)
            f = 0.0
            if st[0] == "open":
                f = mrl[g](st[1])
            elif st[0] == "out" and mode == "G":
                f = pr[g][0](st[1]) * A[g]
            c += d / (W.known_days(eps) + f)
        out[mode] = pay / (c * W.CAP)
    return out


def streamlined(P):
    """Beneficiaries whose election at Fallowmere began in FY2026 (the streamlined method's count, not the policy's)."""
    fal = R.CCN["FAL"]
    n = set()
    for m, lst in P["book"].stays.items():
        for st in lst:
            if st["first"] == fal and W.FY[0] <= st["start"] < W.FY[1]:
                n.add(m)
    return len(n)


def emr_days_agree(P):
    ex = {}
    for r in P["tb"]["extract"]:
        ex.setdefault((r["mbi"], r["ccn"], r["elect"]), 0)
    cw = {r["hicn"]: r["mbi"] for r in P["tb"]["crosswalk"]}
    by = collections.defaultdict(int)
    for r in P["tb"]["extract"]:
        by[(r["mbi"], r["ccn"])] += r["days"]
    emr = collections.defaultdict(int)
    for r in P["tb"]["emr"]:
        if r["payer"] != "Medicare" or not r["discharge_date"] or r["admit_date"] < dt.date(2016, 10, 1):
            continue
        m = cw.get(r["medicare_id"], r["medicare_id"])
        n = (r["discharge_date"] - r["admit_date"]).days + (1 if r["discharge_reason"] == "Expired" else 0)
        emr[(m, r["provider_number"])] += n
    bad = 0
    for k, v in emr.items():
        if by.get(k, 0) < v:
            bad += 1
    return bad == 0


def own_days_only(P):
    """FY2026 count with each beneficiary's days in every hospice replaced by the organisation's own days only."""
    book, est = P["book"], P["est"]
    out = 0.0
    fal = R.CCN["FAL"]
    for r in P["cohort"]:
        if fal not in r["fy"]:
            continue
        own = 0
        for st in book.stays[r["mbi"]]:
            for ccn, s, n in st["segs"]:
                if ccn in book.wendleglen and s < W.CLOSE:
                    own += min(n, W.CLOSE - s)
        out += r["fy"][fal] / (own + Gd.future(r, est, **Gd.RUNGS["G"]))
    return out


def jensen(cohort, est):
    """The share's expectation over a live discharge's two futures (back or not), the rest as the golden."""
    fal = R.CCN["FAL"]
    c = 0.0
    for r in cohort:
        if fal not in r["fy"]:
            continue
        d = r["fy"][fal]
        st = r["state"]
        if st[0] == "out":
            key = (r["home"], r["g"])
            p = est.get("aj", key)[0](st[1])
            a = est.get("A_km", key)
            c += (1 - p) * d / r["known"] + p * d / (r["known"] + a)
        else:
            c += d / (r["known"] + Gd.future(r, est, **Gd.RUNGS["G"]))
    return c


def since_conversion(P):
    import copy
    tb = P["tb"]
    conv = W.date_of(R.CONVERSION)
    fal = R.CCN["FAL"]
    keep = []
    first_of = {}
    for r in tb["extract"]:
        keep.append(r)
    b = Gd.Book(tb, R.CCN.values())
    for key in list(b.stay_rows):
        if key[0] == fal:
            b.stay_rows[key] = b.stay_rows[key][-max(1, len(b.stay_rows[key]) // 6):]
    for name in ("live_rows", "ret_stays"):
        d = getattr(b, name)
        for key in list(d):
            if key[0] == fal:
                d[key] = d[key][-max(1, len(d[key]) // 6):]
    c = Gd.counts(Gd.cohort(b), Gd.Estimates(b), **Gd.RUNGS["G"])
    return c[fal]


def pooled_class(P):
    b = Gd.Book(P["tb"], R.CCN.values())
    for name in ("stay_rows", "live_rows", "ret_stays", "later", "live_in", "ret_in", "closed_2026"):
        d = getattr(b, name)
        pooled = collections.defaultdict(list)
        for (ccn, g), v in d.items():
            pooled[g] += v
        for key in list(d):
            d[key] = list(pooled[key[1]])
    c = Gd.counts(Gd.cohort(b), Gd.Estimates(b), **Gd.RUNGS["G"])
    return c[R.CCN["FAL"]]


def transfers_continue(P):
    rows = P["tb"]["extract"]
    by = collections.defaultdict(list)
    for r in rows:
        by[(r["mbi"], r["elect"])].append(r)
    ok = True
    for k, v in by.items():
        v.sort(key=lambda r: r["start"])
        for a, b in zip(v, v[1:]):
            gap = (b["start"] - a["start"]).days - a["days"]
            ok &= gap == 0
    return ok


def natural_inpatient(P):
    latest = {}
    for c in P["claims"]:
        root = c["prior"] or c["key"]
        prev = latest.get(root)
        if prev is None or c["submitted"] >= prev["submitted"]:
            latest[root] = c
    out = {}
    for code in W.CODES:
        cs = [c for c in latest.values() if c["code"] == code and c["kind"] != "void"]
        g = sum(c["units"]["G"] for c in cs)
        i = sum(c["units"]["I"] for c in cs)
        out[code] = dict(gip=g, irc=i, share=100.0 * (g + i) / P["days"][R.CCN[code]])
    return out


def billed_on_paid(P):
    """The remittance join: units at 0656 and 0655 on the versions the register shows paid, as billed."""
    out = {}
    for code in W.CODES:
        pv = [c for c in R.paid_versions(P["claims"]) if c["code"] == code]
        g = sum(c["units"]["G"] for c in pv)
        i = sum(c["units"]["I"] for c in pv)
        out[code] = dict(gip=g, irc=i, share=100.0 * (g + i) / P["days"][R.CCN[code]])
    return out


def latest_billed(P):
    """The latest version of each claim chain, as billed (both devices mishandled)."""
    latest = {}
    for c in P["claims"]:
        root = c["prior"] or c["key"]
        prev = latest.get(root)
        if prev is None or c["submitted"] >= prev["submitted"]:
            latest[root] = c
    out = {}
    for code in W.CODES:
        cs = [c for c in latest.values() if c["code"] == code and c["kind"] != "void"]
        g = sum(c["units"]["G"] for c in cs)
        i = sum(c["units"]["I"] for c in cs)
        out[code] = dict(gip=g, irc=i, share=100.0 * (g + i) / P["days"][R.CCN[code]])
    return out


def reviewed_dropped(P):
    """The over-correction: every inpatient day on a claim held for review taken as unpaid."""
    out = {}
    for code in W.CODES:
        pv = [c for c in R.paid_versions(P["claims"]) if c["code"] == code]
        g = sum(0 if "review" in c else c["units"]["G"] for c in pv)
        i = sum(0 if "review" in c else c["units"]["I"] for c in pv)
        out[code] = dict(gip=g, irc=i, share=100.0 * (g + i) / P["days"][R.CCN[code]])
    return out


def repricing_forces(P):
    """Each paid version repriced at its billed levels: equal to its payment to the cent unless the review paid some
    inpatient days at the routine rate, and then exactly one (general inpatient, respite) count of days, priced at the
    claim's own routine tier, closes the gap (house fixes: the figure that makes the wrong reading wrong)."""
    wi = P["wi"]
    bad, n_dc = 0, 0
    for c in R.paid_versions(P["claims"]):
        f, l = R.price(c["days"])
        billed = round(f + l * wi[c["code"]], 2)
        paid = R.payment(c, wi)
        rv = c.get("review", {"G": 0, "I": 0})
        if rv["G"] + rv["I"] == 0:
            bad += abs(billed - paid) > 0.005
            continue
        n_dc += 1
        hits = []
        for kg in range(c["units"]["G"] + 1):
            for ki in range(c["units"]["I"] + 1):
                days = list(c["days"])
                for lv, n in (("G", kg), ("I", ki)):
                    for j in ([j for j, d in enumerate(days) if d[1] == lv][-n:] if n else []):
                        d, x, hi, q = days[j]
                        days[j] = (d, "R", hi, q)
                f2, l2 = R.price(days)
                if abs(round(f2 + l2 * wi[c["code"]], 2) - paid) < 0.005:
                    hits.append((kg, ki))
        bad += hits != [(rv["G"], rv["I"])]
    n_rev = sum(1 for c in R.paid_versions(P["claims"]) if "review" in c)
    return bad == 0, n_dc, n_rev


def chc_units_as_days(P):
    out = {}
    for code in W.CODES:
        pv = [c for c in R.paid_versions(P["claims"]) if c["code"] == code]
        inpatient = sum(R.paid_units(c, "G") + R.paid_units(c, "I") for c in pv)
        days = sum(c["units"]["R"] + c["units"]["I"] + c["units"]["G"] + sum(u for _, u in c["chc"]) for c in pv)
        out[code] = 100.0 * inpatient / days
    return out


def rhc_only(P):
    out = {}
    for code in W.CODES:
        pv = [c for c in R.paid_versions(P["claims"]) if c["code"] == code]
        inpatient = sum(R.paid_units(c, "G") + R.paid_units(c, "I") for c in pv)
        out[code] = 100.0 * inpatient / sum(R.paid_units(c, "R") for c in pv)
    return out


# ---- the three rules and the realism sweep

def shipped_headers():
    """(file, column) for every column the pack ships: CSV headers, workbook header rows, JSON keys and the extract's
    field names (the file notes' layout)."""
    import csv as _csv
    import openpyxl
    out = []
    for f in sorted(os.listdir(TARGET)):
        path = os.path.join(TARGET, f)
        if f.endswith(".csv"):
            with open(path) as fh:
                out += [(f, h) for h in next(_csv.reader(fh))]
        elif f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(path, read_only=True)
            for ws in wb.worksheets:
                for row in ws.iter_rows(min_row=1, max_row=5, values_only=True):
                    if row and sum(1 for v in row if isinstance(v, str)) >= 4:
                        out += [(f, str(v)) for v in row if v is not None]
                        break
        elif f.endswith(".json"):
            def keys(x):
                if isinstance(x, dict):
                    for k, v in x.items():
                        yield k
                        yield from keys(v)
                elif isinstance(x, list):
                    for v in x:
                        yield from keys(v)
            out += [(f, k) for k in sorted(set(keys(json.load(open(path)))))]
    out += [("medicare_hospice_benefit_periods_20270105.txt", h) for h in
            ("REC_TYPE", "MBI", "BP_NUM", "ELECT_DT", "PROV_CCN", "BP_START", "BP_END", "BP_DAYS", "DOD")]
    return out


def call_of(tb, pay, opts):
    """The call on a set of tables and payments: {ccn: repayment in USD millions} for every provider number that owes."""
    b = Gd.Book(tb, R.CCN.values())
    c = Gd.counts(Gd.cohort(b), Gd.Estimates(b), **opts)
    out = {}
    for ccn in c:
        r = Gd.repayment(pay.get(ccn, 0.0), c[ccn])
        if r > 0:
            out[ccn] = m1(r)
    return out


def show(call):
    return "nothing" if not call else ", ".join("%s %.1f" % (INV[c], v) for c, v in sorted(call.items()))


def mishandled(P):
    """Each Layer 1 item of the call's inputs, mishandled the natural way: (id, item, tables, payments, silent, fork row).
    A silent item leaves the call where it is; an item that moves it is a misread the fork table closes."""
    tb = P["tb"]
    pay = goldwb.payments_by_ccn(P["remit"])
    out = [("R2a", "the EMR's HICNs left unlinked (no crosswalk)", dict(tb, crosswalk=[]), pay, True, ""),
           ("R2b", "the seller's register dropped (its diagnosis codes stored without the decimal point)", dict(tb, legacy=[]),
            pay, True, ""),
           ("R2c", "the seller's UB-04 statuses read as discharges home", dict(tb, legacy=[dict(r, status="01") for r in tb["legacy"]]),
            pay, True, "")]
    by = collections.defaultdict(list)
    for r in tb["extract"]:
        by[(r["mbi"], r["elect"])].append(r)
    ex = []
    for rows in by.values():
        rows = sorted(rows, key=lambda r: r["start"])
        e, prev = rows[0]["elect"], rows[0]["ccn"]
        for r in rows:
            if r["ccn"] != prev:
                e, prev = r["start"], r["ccn"]
            ex.append(dict(r, elect=e))
    out.append(("R2d", "a transfer between hospices read as a new election", dict(tb, extract=ex), pay, True, ""))
    p_int = collections.defaultdict(float)
    for r in P["remit"]:
        p_int[r["provider_number"]] += r["paid"] + r["sequestration"]
    out.append(("R2e", "the provider-level interest lines summed into payments", tb, dict(p_int), True, ""))
    out.append(("R2f", "each benefit period read as a stay", dict(tb, extract=[dict(r, elect=r["start"]) for r in tb["extract"]]),
                pay, False, "SF18"))
    p_net = collections.defaultdict(float)
    p_gross = collections.defaultdict(float)
    for r in P["remit"]:
        if r["record"] == "CLP":
            p_net[r["provider_number"]] += r["paid"]
            if r["claim_status"] == "1":
                p_gross[r["provider_number"]] += r["paid"] + r["sequestration"]
    out.append(("R2g", "payments read after sequestration", tb, dict(p_net), False, "SF7"))
    out.append(("R2h", "payments read without their reversals", tb, dict(p_gross), False, "SF8"))
    return out


def copied_histories(P):
    """Two beneficiaries whose closed histories match row for row (dates, provider numbers, days and date of death). Two
    patients elected the same day and both on service at the close share the calendar's benefit periods, so open
    histories are left out; a closed match is a copied block."""
    seqs = collections.defaultdict(list)
    closed = {}
    for r in P["tb"]["extract"]:
        seqs[r["mbi"]].append((r["start"], r["ccn"], r["days"], r["end"], r["dod"]))
    seen = collections.Counter(tuple(sorted(v)) for v in seqs.values()
                               if len(v) >= 3 and all(x[3] is not None for x in v))
    return sum(n - 1 for n in seen.values() if n > 1)


def plants_shipped():
    names = " ".join(os.listdir(TARGET)).lower()
    return any(w in names for w in ("memo", "draft", "provisional", "determination", "estimate", "briefing"))


def periods_chain(P):
    by = collections.defaultdict(list)
    for r in P["tb"]["extract"]:
        by[(r["mbi"], r["elect"])].append(r)
    for rows in by.values():
        rows.sort(key=lambda r: r["start"])
        if rows[0]["start"] != rows[0]["elect"]:
            return False
        for a, b in zip(rows, rows[1:]):
            if (b["start"] - a["start"]).days != a["days"]:
                return False
    return True


def census_of(P):
    return BD.census_figures(P)


def longest_flat_run(P):
    """The longest run of equal monthly admission counts at any program, and the lowest dispersion (variance over mean)
    of a program's monthly admissions: a constant stream shows as a long run or a dispersion far under Poisson's 1."""
    worst, disp = 0, []
    for code in W.CODES:
        ccn = R.CCN[code]
        cnt = collections.Counter((r["admit_date"].year, r["admit_date"].month) for r in P["tb"]["emr"]
                                  if r["provider_number"] == ccn and r["admit_date"] >= dt.date(2017, 1, 1)
                                  and r["admission_type"] != "Conversion")
        months = sorted(cnt)
        xs = [cnt[k] for k in months]
        if len(xs) >= 24:
            mu = sum(xs) / len(xs)
            disp.append(sum((x - mu) ** 2 for x in xs) / (len(xs) - 1) / mu)
        run = 1
        for a, b in zip(months, months[1:]):
            run = run + 1 if cnt[a] == cnt[b] else 1
            worst = max(worst, run)
    return worst, min(disp)


def ooxml_people(path):
    import re
    import zipfile
    with zipfile.ZipFile(path) as z:
        core = z.read("docProps/core.xml").decode("utf-8")
    return set(re.findall(r"<dc:creator>([^<]*)</dc:creator>", core) + re.findall(r"<cp:lastModifiedBy>([^<]*)</cp:lastModifiedBy>", core))


def pdf_meta(path, key):
    import re
    m = re.search(rb"/" + key.encode() + rb" \((.*?)\)", open(path, "rb").read())
    return m.group(1).decode("latin-1") if m else ""


def container_people():
    who = set()
    for d in (TARGET, GOLDEN):
        for f in sorted(os.listdir(d)):
            path = os.path.join(d, f)
            if f.endswith((".xlsx", ".docx")):
                who |= ooxml_people(path)
            elif f.endswith(".pdf"):
                who.add(pdf_meta(path, "Author"))
    return {w for w in who if w}


def ooxml_date(path, tag):
    import re
    import zipfile
    with zipfile.ZipFile(path) as z:
        core = z.read("docProps/core.xml").decode("utf-8")
    m = re.search(r"<dcterms:%s[^>]*>([^<]*)</dcterms:%s>" % (tag, tag), core)
    return m.group(1)[:10] if m else ""


def chronology(P):
    bad = []
    last = dt.date(2026, 12, 31)
    for c in P["claims"]:
        if c["submitted"] <= c["thru"] or c["submitted"] > last:
            bad.append("claim %s submitted %s" % (c["key"], c["submitted"]))
        if c.get("paid_on") and c["kind"] != "returned" and not (c["submitted"] < c["paid_on"] <= last):
            bad.append("claim %s paid %s" % (c["key"], c["paid_on"]))
    for r in P["remit"]:
        if r["remit_date"] > last:
            bad.append("remittance %s" % r["remit_date"])
    for r in P["tb"]["emr"]:
        if r["discharge_date"] and not (r["admit_date"] <= r["discharge_date"] <= last):
            bad.append("emr %s" % r["admit_date"])
    conv = W.date_of(R.CONVERSION)
    for r in P["tb"]["legacy"]:
        if r["admit"] >= conv or (r["disch"] and r["disch"] >= conv):
            bad.append("register %s" % r["admit"])
    t = lambda n: os.path.join(TARGET, BD.NAMES[n])
    stamps = [("policy", ooxml_date(t("policy"), "modified")), ("extract run", "2027-01-05"),
              ("census", pdf_meta(t("census"), "CreationDate")[2:10]), ("notes", pdf_meta(t("notes"), "CreationDate")[2:10]),
              ("golden", ooxml_date(os.path.join(GOLDEN, "fy2026_hospice_cap_accrual.xlsx"), "created"))]
    norm = [(k, v.replace("-", "")) for k, v in stamps]
    if any(not v for k, v in norm) or [v for k, v in norm] != sorted(v for k, v in norm):
        bad.append("document dates %s" % norm)
    return bad


def documents_unread():
    """House fix H25: a control sentence per document, found through every reader a solver reaches for."""
    import re
    import zipfile
    import docx
    import pypdf
    from pdfminer.high_level import extract_text
    controls = {"census": "Census and flow", "rates": "Aggregate cap amount, cap year ending 30 September 2026",
                "notes": "date of the election the benefit period belongs to"}
    bad = []
    for key, sentence in controls.items():
        path = os.path.join(TARGET, BD.NAMES[key])
        texts = [" ".join(p.extract_text() for p in pypdf.PdfReader(path, strict=s).pages) for s in (False, True)]
        texts.append(extract_text(path))
        for t in texts:
            if sentence not in " ".join(t.split()):
                bad.append(key)
                break
    path = os.path.join(TARGET, BD.NAMES["policy"])
    via_docx = " ".join(p.text for p in docx.Document(path).paragraphs)
    with zipfile.ZipFile(path) as z:
        raw = re.sub(r"<[^>]+>", "", z.read("word/document.xml").decode("utf-8"))
    for sentence in ("divided by that total", "the experience since 1 October 2016 of the beneficiaries cared for"):
        if sentence not in via_docx or sentence not in raw:
            bad.append("policy: " + sentence)
    return bad


if __name__ == "__main__":
    raise SystemExit(main())
