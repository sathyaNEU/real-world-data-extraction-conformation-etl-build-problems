"""task482 architecture 17: the generator's assertions on the shipped seed. The main call's screens, every semantic
fork row (SF1 to SF15), the literal execution of every filed sentence, the three-rules block on the clean truth,
the separation line and the asks' device mass. Exit 1 on any failure."""
import datetime as dt
import json
import os
import sys

import numpy as np

import core as C
import golden as G
import params as P
import rasch as RA

HERE = os.path.dirname(os.path.abspath(__file__))
FAIL = []


def check(name, ok, detail=""):
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAIL.append(name)


def edge(x, step):
    f = x / step
    return abs((f - np.floor(f)) - 0.5) * step


def main():
    res = G.compute()
    w, dr, bb, bg = res["w"], res["drafts"], res["b_bank"], res["b_gold"]
    pl, sch = w["pool"], w["schools"]
    items = pl["items"]
    gold, bank = res["gold"], res["bank"]

    # ---- screen 1: levels and the lever; the golden mid-bin with margin
    check("golden picks Paper C", res["pick"] == "C", str({d: round(v, 3) for d, v in gold.items()}))
    check("golden marks mid-bin (0.25 of a mark from every rounding edge)",
          all(edge(v, 1.0) >= 0.25 for v in gold.values()))
    check("golden margin: the nearest other draft at least 0.5 marks further from 25",
          min(res["dist"][d] for d in "AB") - res["dist"]["C"] >= 0.5)
    # ---- screen 3 and the literal execution of every filed sentence (the specification, the standard-setting
    # record, the bank's final run, the renumbering; nothing re-estimated): Paper A
    check("default path and literal execution file Paper A", C.pick(bank) == "A", str({d: round(v, 3) for d, v in bank.items()}))
    check("the default path's whole marks differ from the golden's on every draft",
          all(round(bank[d]) != round(gold[d]) for d in "ABC"))
    rv = C.rivals(w, bb, dr)
    # ---- screen 2: the golden's own method holds (SF8 clock, SF9 boundary and lag, SF13 the recalibration's form)
    for k, sf in (("lag2", "SF9"), ("lag4", "SF9"), ("utc_day", "SF8"), ("wle", "SF13"), ("joint", "SF13"),
                  ("one_shift", "SF13")):
        ok = C.pick(rv[k]) == "C" and all(round(rv[k][d]) == round(gold[d]) for d in "ABC")
        check("%s %s files C at the golden's whole marks" % (sf, k), ok, str({d: round(v, 2) for d, v in rv[k].items()}))
    # ---- screen 4: the careful readers land wrong
    for k in ("outline_weeks", "outline_last_week", "whole_school", "last_days", "trend", "national_weeks"):
        check("reader %s does not file C" % k, C.pick(rv[k]) != "C", str({d: round(v, 2) for d, v in rv[k].items()}))
    check("SF12 each school's weeks on the national calendar files another call (the appendix header rules it out)",
          C.pick(rv["national_weeks"]) != res["pick"])
    # ---- structure the closures rest on
    check("no school's first Term 3 unit ends before its first sitting day",
          all(s["end1"] > s["days"][0] for s in sch))
    check("SF9 no session on a school's unit-end day", all(p["day"] != sch[p["school"]]["end1"] for p in w["online"]))
    check("SF8 every first unit ends on a Friday", all(s["end1"].weekday() == 4 for s in sch))
    check("SF11 every second Term 3 unit ends at the school's term end, after the window",
          all(s["term_end"] > P.WINDOW[-1] for s in sch))
    check("SF14 every core unit ends by its school's Term 3 end, before November 2027",
          all(s["term_end"] < dt.date(2027, 11, 1) for s in sch))
    T = res["T"]
    resp = w["M"] > 0
    t3 = pl["t3"]
    share = (T[:, t3] & resp[:, t3]).sum() / resp[:, t3].sum()
    check("taught share of the Term 3 responses under one in five", share < 0.2, "%.3f" % share)
    # ---- axis 21: every draft meets the strand ranges; the Term 3 counts
    for d, ix in dr.items():
        ok = all(lo <= sum(1 for i in ix if items[i]["strand"] == st) <= hi for st, (lo, hi) in P.STRAND_RANGE.items())
        check("draft %s meets the specification's strand ranges and has 50 items" % d, ok and len(ix) == 50)
    check("Term 3 items per draft", res["t3_count"] == {"A": 6, "B": 11, "C": 17}, str(res["t3_count"]))
    # ---- screen 5: fit parity and the back-test
    infit, outfit = RA.fit_stats(w["R"], w["M"], C.thetas_t12(w, bb), bb)
    _, thb = C.bank_run(w)
    infit, outfit = RA.fit_stats(w["R"], w["M"], thb, bb)
    t12 = pl["t12"]
    check("Term 3 infit inside the Term 1 and 2 items' infit range",
          infit[t3].min() >= infit[t12].min() - 0.02 and infit[t3].max() <= infit[t12].max() + 0.02,
          "T3 %.3f-%.3f, T12 %.3f-%.3f" % (infit[t3].min(), infit[t3].max(), infit[t12].min(), infit[t12].max()))
    check("every item's outfit inside 0.7 to 1.3", outfit.min() > 0.7 and outfit.max() < 1.3,
          "%.3f-%.3f" % (outfit.min(), outfit.max()))
    anc = pl["anchors"]
    free = [i for i in range(len(bb)) if i not in anc]
    th_na = RA.fit_theta(w["R"][:, free], w["M"][:, free], bb[free])
    ba = RA.fit_b(w["R"][:, anc], w["M"][:, anc], th_na, b0=bb[anc])
    check("anchor block's free 2026 estimates within 0.10 logits of their banked values",
          np.abs(ba - bb[anc]).max() < 0.10, "%.3f" % np.abs(ba - bb[anc]).max())
    for f in range(P.N_FORMS):
        rows = [r for r, p in enumerate(w["online"]) if p["form"] == f]
        obs = w["R"][rows][:, pl["forms"][f]].sum(1).mean()
        exp = RA.sig(thb[rows][:, None] - bb[pl["forms"][f]][None, :]).sum(1).mean()
        check("the bank reproduces form %d's observed mean mark" % (f + 1), abs(obs - exp) < 0.05, "%.2f %.2f" % (obs, exp))
    sh = bb[t3].mean() - bb[t12].mean()
    check("Shock: the Term 3 items' banked mean within 0.35 logits of the Term 1 and 2 items'", abs(sh) < 0.35, "%.3f" % sh)
    # ---- SF6 the preliminary run; SF10 duplicates; SF5 the scale; SF4 rounding; axis 14 row order
    bp, _ = C.bank_run(w, upto=P.PRELIM_CUTOFF)
    check("SF6 the preliminary run: default A, golden C", C.pick(C.marks(bp, dr)) == "A" and
          C.pick(C.marks(C.recal_t3(w, bp, T.astype(float)), dr)) == "C")
    for keep in ("first", "both"):
        R2, M2 = C.matrices(w, keep)
        b2, _ = C.bank_run(w, R2, M2)
        g2 = C.marks(C.recal_t3(w, b2, T.astype(float), R2, M2), dr)
        check("SF10 re-answered items kept %s: default A, golden C at its whole marks" % keep,
              C.pick(C.marks(b2, dr)) == "A" and C.pick(g2) == "C" and all(round(g2[d]) == round(gold[d]) for d in "ABC"))
    rc = bg - np.nanmean(bg)
    check("SF5 re-centring the recalibrated bank on every item's mean keeps C (the scale is held by the anchors)",
          C.pick(C.marks(rc, dr)) == "C", str({d: round(v, 2) for d, v in C.marks(rc, dr).items()}))
    check("SF4 rounded marks compared give the same call",
          min((abs(round(v) - 25), d) for d, v in gold.items())[1] == "C")
    perm = np.random.default_rng(1).permutation(len(w["online"]))
    th1 = C.thetas_t12(w, bb)
    b1 = C.recal_t3(w, bb, T.astype(float), th=th1)
    MP, RP, TP = w["M"][perm], w["R"][perm], T[perm]
    b1p = C.recal_t3(w, bb, TP.astype(float), R=RP, M=MP, th=th1[perm])
    check("axis 14 row order does not move an estimate", np.nanmax(np.abs(b1 - b1p)) < 1e-9)
    # ---- SF1 SF2 SF3 SF7 SF15: the WHAT and identities
    check("SF1 SF2 SF3 the expected mark is the sum of 50 item probabilities at the record's 0.35 logits",
          abs(RA.expected_mark(bg[dr["C"]], P.THETA_ACHIEVED) - gold["C"]) < 1e-12 and P.THETA_ACHIEVED == 0.35)
    codes = {it["code"] for it in items}
    check("SF7 no card number reads as a bank code", all("S10-%04d" % it["card"] not in codes for it in items))
    online = {p["entry"] for p in w["online"]}
    a = w["asks"]
    check("SF15 no make-up candidate is in the response export", all(x["entry"] not in online for x in a["roster"]))
    # ---- separation line and the asks' device mass
    old_entries = {o for o, _ in a["transfers"]}
    check("separation: no transferred candidate's old entry and no withdrawn entry is in the response export",
          not (old_entries & online) and not (set(a["withdrawn"]) & online))
    region_of = {s["code"]: s["region"] for s in sch}
    host_codes = {sch[h]["code"] for h in set(a["host_of"].values())}
    naive_sat = {r: sum(1 for p in w["online"] if sch[p["school"]]["region"] == r) for r in P.REGIONS}
    naive_mk = {r: [] for r in P.REGIONS}
    for x in a["scripts"]:
        naive_sat[region_of[x["school"]]] += 1
        naive_mk[region_of[x["school"]]].append(x["mark"])
    check("P1 the host-centre code misses sat in every region", all(naive_sat[r] != a["sat"][r] for r in P.REGIONS),
          str(naive_sat))
    check("P1 the host-centre code alone moves every region's mean make-up mark past half a unit, or leaves it blank",
          all((not naive_mk[r]) or abs(np.mean(naive_mk[r]) - a["makeup_mean"][r]) > 0.05 for r in P.REGIONS),
          str({r: (round(float(np.mean(v)), 2) if v else None) for r, v in naive_mk.items()}))
    roster_sat = {r: sum(1 for p in w["online"] if sch[p["school"]]["region"] == r) for r in P.REGIONS}
    for x in a["roster"]:
        roster_sat[sch[x["home"]]["region"]] += 1
    check("P1 counting roster lines (no-shows included) misses sat in every region with a no-show",
          sum(1 for r in P.REGIONS if roster_sat[r] != a["sat"][r]) >= 3, str(roster_sat))
    nsn_entered = {}
    seen = set()
    for e in a["entries"]:
        if e["status"] != "E":
            continue
        key = ("nsn", e["nsn"]) if e["nsn"] else ("entry", e["entry"])
        if key in seen:
            continue
        seen.add(key)
        r = region_of[e["school"]]
        nsn_entered[r] = nsn_entered.get(r, 0) + 1
    check("P2 an NSN match misses entered in every region by 2 or more",
          all(nsn_entered[r] - a["entered"][r] >= 2 for r in P.REGIONS), str(nsn_entered))
    sd_entered = {}
    seen = set()
    for e in a["entries"]:
        if e["status"] != "E":
            continue
        key = (e["surname"], e["dob"])
        if key in seen:
            continue
        seen.add(key)
        r = region_of[e["school"]]
        sd_entered[r] = sd_entered.get(r, 0) + 1
    check("P2 a surname and birth-date match misses entered in every region (twins merged)",
          all(sd_entered[r] != a["entered"][r] for r in P.REGIONS), str(sd_entered))
    full = {}
    seen = set()
    for e in a["entries"]:
        if e["status"] != "E":
            continue
        key = (e["first"], e["surname"], e["dob"])
        if key in seen:
            continue
        seen.add(key)
        full[region_of[e["school"]]] = full.get(region_of[e["school"]], 0) + 1
    check("P2 the golden handling (first name, surname, birth date) reproduces entered", full == a["entered"], str(full))
    # P4 (D4): unbooked candidates who sat at a host reach only the keyed file; the typed roster never lists them
    rost = {x["script"]: x["home"] for x in a["roster"] if x["script"]}
    walk_reg = {r: sum(1 for x in a["walkins"] if sch[x["home"]]["region"] == r) for r in P.REGIONS}
    check("P4 walk-ins in every region", all(v >= 1 for v in walk_reg.values()), str(walk_reg))
    fi_sat = {r: sum(1 for p in w["online"] if sch[p["school"]]["region"] == r) for r in P.REGIONS}
    fi_n = {r: 0 for r in P.REGIONS}
    fi_mk = {r: [] for r in P.REGIONS}
    for x in a["scripts"]:
        if x["script"] in rost:
            reg = sch[rost[x["script"]]]["region"]
            fi_sat[reg] += 1
            fi_n[reg] += 1
            fi_mk[reg].append(x["keyed_mark"] / 2 if x["keyed_mark"] > 50 else x["keyed_mark"])
    check("P4 the roster join (unmatched scripts dropped) misses sat in every region",
          all(fi_sat[r] != a["sat"][r] for r in P.REGIONS), str(fi_sat))
    check("P4 the roster join misses every region's make-up count", all(fi_n[r] != a["makeup_n"][r] for r in P.REGIONS))
    fi_mean = {r: (sum(v) / len(v) if v else None) for r, v in fi_mk.items()}
    check("P4 with P3, the full includer's roster join misses every region's mean at one decimal",
          all(fi_mean[r] is None or round(fi_mean[r], 1) != round(a["makeup_mean"][r], 1) for r in P.REGIONS),
          str({r: (round(v, 2) if v is not None else None) for r, v in fi_mean.items()}))
    hk = {r: [] for r in P.REGIONS}
    for x in a["scripts"]:
        reg = sch[rost[x["script"]]]["region"] if x["script"] in rost else region_of[x["school"]]
        hk[reg].append(x["keyed_mark"] / 2 if x["keyed_mark"] > 50 else x["keyed_mark"])
    hk_mean = {r: (sum(v) / len(v) if v else None) for r, v in hk.items()}
    check("P4 unmatched scripts placed by the keyed code still miss every region's mean at one decimal",
          all(hk_mean[r] is None or round(hk_mean[r], 1) != round(a["makeup_mean"][r], 1) for r in P.REGIONS),
          str({r: (round(v, 2) if v is not None else None) for r, v in hk_mean.items()}))
    check("P4 benign twin: the keyed file carries entry numbers on rostered scripts too",
          any(x["entry"] and not x["walkin"] for x in a["scripts"]))
    # AF1 (ask B's keying fork, closed by the roster's header: M26 out of 50, the cover's mark and percentage, a
    # keyer's session one batch on one template). Every treatment but the whole batch halved breaks a filed fact
    # and moves a graded mean.
    off = {x["batch"] for x in a["scripts"] if x["keyed_mark"] > 50}
    check("AF1 exactly one batch holds values over 50, and it is the percentage batch",
          len(off) == 1 and all((x["batch"] in off) == x["pct"] for x in a["scripts"]))
    check("AF1 every value in that batch is even", all(x["keyed_mark"] % 2 == 0 for x in a["scripts"] if x["batch"] in off))
    roster_scripts = {x["script"] for x in a["roster"] if x["script"]}

    def means_under(rule):
        vals = {r: [] for r in P.REGIONS}
        for x in a["scripts"]:
            v = rule(x)
            if v is not None:
                vals[sch[x["home"]]["region"]].append(v)
        return {r: (round(sum(v) / len(v), 1) if v else None) for r, v in vals.items()}, vals
    inb = lambda x: x["batch"] in off
    treat = {
        "halve the whole batch": (lambda x: x["keyed_mark"] / 2 if inb(x) else x["keyed_mark"], set()),
        "halve the batch's rostered scripts only": (lambda x: x["keyed_mark"] / 2 if inb(x) and x["script"] in roster_scripts
                                                    else x["keyed_mark"], {"one template"}),
        "halve all but the batch's last script": (lambda x: x["keyed_mark"] / 2 if inb(x) and x["script"] != max(
            y["script"] for y in a["scripts"] if inb(y)) else x["keyed_mark"], {"one template"}),
        "drop marks over 50": (lambda x: None if x["keyed_mark"] > 50 else x["keyed_mark"], {"every sitter"}),
        "drop the batch": (lambda x: None if inb(x) else x["keyed_mark"], {"every sitter"}),
        "halve only marks over 50": (lambda x: x["keyed_mark"] / 2 if x["keyed_mark"] > 50 else x["keyed_mark"],
                                     {"one template"}),
        "as keyed": (lambda x: x["keyed_mark"], {"out of 50"}),
    }
    gold_pair = None
    for name, (rule, broken) in treat.items():
        m, vals = means_under(rule)
        facts = set()
        if any(v > 50 for vs in vals.values() for v in vs):
            facts.add("out of 50")
        if sum(len(v) for v in vals.values()) != len(a["scripts"]):
            facts.add("every sitter")
        for bt in off:
            units = {(rule(x) == x["keyed_mark"]) for x in a["scripts"] if x["batch"] == bt and rule(x) is not None}
            if len(units) > 1:
                facts.add("one template")
        pair = (m["Central"], m["Capital"])
        if name == "halve the whole batch":
            gold_pair = pair
            check("AF1 the whole batch halved breaks no filed fact and gives the golden means",
                  not facts and all(m[r] == round(a["makeup_mean"][r], 1) for r in P.REGIONS), str(m))
        else:
            check("AF1 %s breaks a filed fact (%s) and moves the Central or Capital mean" % (name, ", ".join(sorted(facts))),
                  bool(facts) and broken <= facts and pair != gold_pair, str(pair))
    pct = [x for x in a["scripts"] if x["pct"]]
    check("P3 the percentage batch has rows both over and at or under 50",
          any(x["keyed_mark"] > 50 for x in pct) and any(x["keyed_mark"] <= 50 for x in pct))
    naive_mean = {}
    for r in P.REGIONS:
        v = [(x["keyed_mark"] / 2 if x["keyed_mark"] > 50 else x["keyed_mark"]) for x in a["scripts"]
             if sch[x["home"]]["region"] == r]
        naive_mean[r] = sum(v) / len(v)
    check("P3 halving only marks over 50 misses the Central and Capital means by 0.1 or more",
          all(abs(naive_mean[r] - a["makeup_mean"][r]) >= 0.1 for r in ("Central", "Capital")),
          str({r: round(v, 2) for r, v in naive_mean.items()}))
    check("ask means mid-bin (0.015 from a rounding edge at one decimal)",
          all(edge(v, 0.1) >= 0.015 for v in a["makeup_mean"].values()))
    check("the host codes are the three host schools'", len(host_codes) == 3)
    # ---- the 20-redraw screens (screens.py writes screens.json)
    sp = os.path.join(HERE, "screens.json")
    if os.path.exists(sp):
        s = json.load(open(sp))["routes"]
        check("redraws: golden C in 20 of 20", s["golden"]["picks"] == "C" * 20)
        for k in ("lag2", "utc_day", "wle", "joint", "one_shift"):
            check("redraws: %s C in 20 of 20" % k, s[k]["picks"] == "C" * 20)
        check("redraws: lag4 (every Monday sitter dropped) C in at least 19 of 20", s["lag4"]["picks"].count("C") >= 19)
        check("redraws: the bank A in 20 of 20", s["bank"]["picks"] == "A" * 20)
        for k in ("outline_weeks", "outline_last_week", "whole_school", "last_days", "trend"):
            check("redraws: %s never C" % k, "C" not in s[k]["picks"])
        check("redraws: national weeks C in at most 3 of 20", s["national_weeks"]["picks"].count("C") <= 3)
    else:
        check("screens.json present", False)
    print("%d failures" % len(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
