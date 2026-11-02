"""Generator assertions on the clean truth and on the cut pack: the three rules (R1 to R3c), the call and its ladder,
the separation the golden's classification rests on, every fork row (SF1 to SF22), the cheap routes, both ask devices
with their forcing and every careful route through them, the realism sweep, the containers, the distractors and the
input gates. Exit 1 on any failure."""
import os, sys, json, csv, re, copy, shutil, subprocess, tempfile, zipfile, itertools, collections, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from world import *
import build, calc, reader, sim

FAIL = []
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
GD = os.path.join(TASK, "golden")


def ok(cond, label, detail=""):
    print(("PASS " if cond else "FAIL ") + label + ((": " + detail) if detail else ""))
    if not cond:
        FAIL.append(label)


def pdf_text(path):
    from pypdf import PdfReader
    return " ".join(" ".join(p.extract_text().split()) for p in PdfReader(path).pages)


def main():
    W = build.world()
    cards, rpop = W["cards"], W["rpop"]
    w4 = {h: round(v, 4) for h, v in W["weight"].items()}
    sa2_region = {x["sa2"]: x["region"] for x in W["sa2s"]}
    shared_split = {x["sa2"]: SHARED[x["sa2_name"]] for x in W["sa2s"] if x["sa2_name"] in SHARED}
    G = calc.golden(cards, w4, rpop)
    gold = set(G["set"])
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    P = reader.load(T)
    names = P["names"]

    # ---- the call
    ok(list(G["set"]) == list(figs["call_codes"]), "golden set matches figures.json", ", ".join(G["set"]))
    ok(G["margin"] >= 1.20, "golden margin fifth over sixth at least 1.20", "%.3f" % G["margin"])
    D = calc.default(cards, w4, rpop, sa2_region, shared_split, by="month")
    ok(set(D["set"]) != gold, "rung 0 (statement address in force each month) files another set", ", ".join(D["set"]))
    ok(D["margin"] >= 1.15, "rung 0 margin at least 1.15", "%.3f" % D["margin"])
    for r in gold - set(D["set"]):
        pos = D["order"].index(r) + 1
        ok(pos in (6, 7), "golden member %s sits sixth or seventh on rung 0" % r, str(pos))
    for label, V in (("stratum", calc.default(cards, w4, rpop, sa2_region, shared_split, by="stratum")),
                     ("shared SA2 split by share", calc.default_split(cards, w4, rpop, sa2_region, shared_split))):
        ok(set(V["set"]) == set(D["set"]), "rung 0 variant (%s) files the same set" % label, ", ".join(V["set"]))
    R1 = calc.adjacency(cards, w4, rpop, sa2_region, shared_split)
    ok(set(R1["set"]) not in (gold, set(D["set"])), "rung 1 (neighbouring regions' cards as locals) files a third set", ", ".join(R1["set"]))
    ok(R1["margin"] >= 1.15, "rung 1 margin at least 1.15", "%.3f" % R1["margin"])
    # rung 0 on the clean truth is the rung 0 a solver computes on the pack (the statement SA2s as shipped)
    def home(sa2):
        if sa2 in P["shares"] and P["shares"][sa2]:
            return max(P["shares"][sa2], key=P["shares"][sa2].get)
        return P["sa2_region"].get(sa2, "IS")
    pop = reader.region_pop(P)
    qd = reader.visitor_spend(P, lambda row: home(row[3]) != row[1])
    prd = {r: sum(qd[r]) / pop[r] for r in qd}
    ok(all(abs(prd[r] - D["per_resident"][r]) < 0.01 for r in ELIGIBLE), "rung 0 on the clean truth equals rung 0 read from the pack, region by region")
    # dominance: for each region the step displaces and each region it brings in, the golden's edge on the decisive
    # axis is at least 1.2 times the displaced region's advantage on the address route
    worst = min((G["per_resident"][w_] / G["per_resident"][d_]) / (D["per_resident"][d_] / D["per_resident"][w_])
                for d_ in set(D["set"]) - gold for w_ in gold - set(D["set"]))
    ok(worst >= 1.2, "dominance: edge on the decisive axis over the carried advantage, worst displaced pair", "%.3f" % worst)
    # ---- the three rules, executed on the clean truth
    cols = {"apn_pos_research_extract_2026.csv": ["card_id", "merchant_region", "month", "statement_sa2", "spend_aud", "transactions", "active_days"]}
    with open(os.path.join(T, "apn_pos_research_extract_2026.csv")) as f:
        hdr = next(csv.reader(f))
    ok(hdr == cols["apn_pos_research_extract_2026.csv"], "R1 the field's raw material ships: one row per sampled card, merchant region and month with spending and days, no visitor flag or routine column")
    months, days = reader.presence(P)
    routine = lambda cid, reg: len(months[(cid, reg)]) >= 6 and days[(cid, reg)] >= 30
    qv = reader.visitor_spend(P, lambda row: not routine(row[0], row[1]))
    ok(all([int(round(x / 1000.0)) * 1000 for x in qv[r]] == figs["q_%s" % r] for r in ELIGIBLE),
       "R1 the golden's decisive computation reads those rows: each card's presence by region and month, then its spending, recomputed from the pack")
    shipped_cols = set()
    for fn in os.listdir(T):
        if fn.endswith(".csv"):
            with open(os.path.join(T, fn)) as f:
                shipped_cols |= {c.lower() for c in next(csv.reader(f))}
    ok(not any(w in c for c in shipped_cols for w in ("visitor", "usual", "routine", "trip", "resident_type", "home_region", "local")),
       "R1 no shipped column holds the deciding quantity (a visitor flag, a home region, a routine set)", ", ".join(sorted(shipped_cols)[:6]) + "...")
    # R2: every mess item mishandled leaves the call where it is
    blank = copy.deepcopy(cards)
    for c in blank:
        c.sa2, c.sa2_change = None, None
    G2 = calc.golden(blank, w4, rpop)
    ok(all(G2["q"][r] == G["q"][r] for r in ELIGIBLE), "R2 statement SA2s that change during the year (SF16): the golden's figures are identical with every statement SA2 blanked")
    rpop_whole = collections.defaultdict(float)
    for x in W["sa2s"]:
        rpop_whole[x["region"]] += x["erp26"]
    ok(set(calc.summary(G["q"], rpop_whole)["set"]) == gold, "R2 Schedule 1's shared areas counted whole to their main region: same set")
    rpop25 = sim.region_erp(W["sa2s"], "erp25")
    ok(set(calc.summary(G["q"], rpop25)["set"]) == gold, "R2 SF9 the 2025 revised release used as the denominator: same set")
    U = calc.golden(cards, {h: 1.0 for h in w4}, rpop)
    ok(set(U["set"]) == gold, "R2 SF6 the opaque strata ignored (the sample unweighted): same set")
    is_codes = {row[3] for row in P["rows"] if row[3] not in P["sa2"]}
    ok(len(is_codes) > 0 and set(G["set"]) == gold, "R2 statement SA2 codes outside the state (%d codes) do not enter the golden, which reads no address" % len(is_codes))
    # R3a the analyst test; R3b the decisive step alone; R3c no plant
    ok(set(D["set"]) != gold, "R3a the easy route on the clean truth, every field read right and every filed rule applied, files %s" % ", ".join(D["set"]))
    ok(set(R1["set"]) != gold and set(G["set"]) == gold,
       "R3b the address route with only the classification changed (each card's routine regions from its own presence) files the golden; the lower rung's single correction (neighbours as locals) files %s" % ", ".join(R1["set"]))
    sig = collections.Counter(tuple(sorted((r, m, round(v[0], 2), v[1], v[2]) for (r, m), v in c.rows.items())) for c in cards if len(c.rows) >= 3)
    ok(max(sig.values()) == 1, "R3c no copied block: no two sampled cards with three rows or more carry the same rows")
    gtext = pdf_text(os.path.join(T, "rvif_2027_round_guidelines.pdf")).lower()
    ctext = pdf_text(os.path.join(T, "rtip_closure_decision_2026.pdf")).lower()
    ok(not re.search(r"\$\d[\d,]* per resident|visitor spending of \$|ranked (first|second)", gtext + ctext),
       "R3c no decoy: no shipped document states a region's visitor spending or a ranking")

    # ---- SF2 separation: every card-region pair is a trip pair or a routine pair, nothing between
    trip = routine_ = between = 0
    for c in cards:
        for r in {rr for (rr, m) in c.rows}:
            k, d = len(c.months_in(r)), c.days_in(r)
            if k <= 3 and d <= 21:
                trip += 1
            elif k >= 8 and d >= 50:
                routine_ += 1
            else:
                between += 1
    ok(between == 0, "SF2 no card-region pair between a trip pattern (at most 3 months, 21 days) and a routine one (8 months, 50 days)",
       "%d trip, %d routine, %d between" % (trip, routine_, between))
    base = {r: [round(x, 2) for x in G["q"][r]] for r in ELIGIBLE}
    same = True
    for mm in range(4, 9):
        for md in (22, 30, 40, 50):
            V = calc.golden(cards, w4, rpop, mm, md)
            same &= all([round(x, 2) for x in V["q"][r]] == base[r] for r in ELIGIBLE)
    for md in range(22, 51, 4):
        V = calc.summary(calc.spend_by(cards, w4, lambda c, r, m, md=md: c.days_in(r) < md), rpop)
        same &= all([round(x, 2) for x in V["q"][r]] == base[r] for r in ELIGIBLE)
    for mm in range(4, 9):
        V = calc.summary(calc.spend_by(cards, w4, lambda c, r, m, mm=mm: len(c.months_in(r)) < mm), rpop)
        same &= all([round(x, 2) for x in V["q"][r]] == base[r] for r in ELIGIBLE)
    ok(same, "SF2 every months threshold 4 to 8, days threshold 22 to 50 and joint rule gives the golden's figures to the cent")
    M = calc.modal_home(cards, w4, rpop)
    ok(set(M["set"]) != gold, "SF3 a single anchor per card (the region holding most of its days) is refuted by the data: it makes each interstate visitor a resident of the region it toured and files another set", ", ".join(M["set"]))
    V = calc.summary(calc.spend_by(cards, w4, lambda c, r, m: c.stratum == "IS" or not calc.routine(c, r)), rpop)
    ok(set(V["set"]) == gold, "SF14 reading every interstate card as a visitor files the same set; its figures for the regions holding interstate workers and students differ, and the cards' presence rules it out")
    a, b = G["per_resident"][G["fifth"]], G["per_resident"][G["sixth"]]
    ok(int(round(a)) - int(round(b)) == int(round(a - b)) == figs["gap_per_resident"], "SF17 the gap reads one way", str(figs["gap_per_resident"]))
    banned = ("usual environment", "postcode", "statement", "address", "resident of", "routine", "presence", "month after")
    ok(not any(w in gtext or w in ctext for w in banned) and "international recommendations for tourism statistics 2008" in gtext,
       "SF1 the guidelines cite the standard's visitor and no document names an address, a postcode or a presence (positive control: the citation is read)")
    ok("in person" in gtext and "cards issued in australia" in gtext, "SF4 SF5 section 4 names in-person spending on cards issued in Australia")
    ok(all(1 <= m <= 12 for c in cards for (r, m) in c.rows), "SF7 SF13 every row is a month of the 2026 calendar year")
    ok(all(r in CODES for c in cards for (r, m) in c.rows), "SF8 every row's merchant region is a schedule region")
    ok(all(abs(sum(v.values()) - 1) < 1e-9 for v in SHARED.values()), "SF10 each shared SA2's shares sum to one")
    diff = [r for r in ELIGIBLE if sum(int(round(x / 1000.0)) * 1000 for x in G["q"][r]) != int(round(sum(G["q"][r]) / 1000.0)) * 1000]
    ok(all(figs["total_%s" % r] == int(round(sum(G["q"][r]) / 1000.0)) * 1000 for r in ELIGIBLE), "SF11 each 2026 total is rounded from the unrounded quarters", "%d regions where the two paths differ" % len(diff))
    pr_rounded = {r: int(round(figs["total_%s" % r] / rpop[r])) for r in ELIGIBLE}
    ok(set(calc.ranking(pr_rounded)[:5]) == gold, "SF11 per resident taken from the rounded 2026 totals files the same set",
       "%d regions a dollar apart" % sum(1 for r in ELIGIBLE if pr_rounded[r] != figs["per_resident_%s" % r]))
    prs = sorted(G["per_resident"].values())
    ok(all(b - a > 1 for a, b in zip(prs, prs[1:])), "SF12 no tie within a dollar per resident")
    ok(all(abs(G["per_resident"][r] - sum(G["q"][r]) / rpop[r]) < 1e-9 for r in ELIGIBLE), "SF15 per resident is the year's total over the population")
    ok(all(p["paid_on"].year == 2026 for p in W["payments"]), "SF22 every transfer in the payments file is dated in 2026")
    ok(all(a["status"] in ("Open", "Acquitted", "Withdrawn") for a in W["agreements"]) and all((a["acquitted"] is None) == (a["status"] == "Open") for a in W["agreements"]),
       "SF19 an agreement is open at 31 December 2026 exactly when the register gives it no acquittal or withdrawal date")
    ok("approved amount less what the program had paid on it by 31 december 2026" in ctext and "because it did not spend it" in ctext and "less what remains of the agreements the fund takes over" in ctext,
       "SF18 SF20 SF21 the closure decision files what remains, unspent money and the round's total")

    # ---- the cheap routes on the clean truth: none files the golden set
    def counts(vis):
        cnt = {r: 0.0 for r in ELIGIBLE}
        for c in cards:
            for r in {rr for (rr, m) in c.rows}:
                if r in cnt and vis(c, r):
                    cnt[r] += w4[c.stratum]
        return calc.summary({r: [cnt[r], 0, 0, 0] for r in ELIGIBLE}, rpop)
    hm = lambda c: c.stratum
    routes = {
        "distinct cards billed outside the region per resident": counts(lambda c, r: hm(c) != r),
        "all card spending per resident": calc.summary(calc.spend_by(cards, w4, lambda c, r, m: True), rpop),
        "cards billed in the state only": calc.summary(calc.spend_by(cards, w4, lambda c, r, m: hm(c) not in (r, "IS")), rpop),
        "cards billed interstate only": calc.summary(calc.spend_by(cards, w4, lambda c, r, m: hm(c) == "IS"), rpop),
        "rung 0 unweighted": calc.default(cards, {h: 1.0 for h in w4}, rpop, sa2_region, shared_split),
        "population, smallest first": calc.summary({r: [1.0 / rpop[r] ** 2, 0, 0, 0] for r in ELIGIBLE}, rpop),
    }
    for cap in range(500, 20001, 250):
        def cap_rule(c, r, m, cap=cap):
            if hm(c) == r:
                return False
            return sum(v[0] for (rr, mm), v in c.rows.items() if rr == r) < cap
        routes["address route keeping cards that spent under $%d in the region" % cap] = calc.summary(calc.spend_by(cards, w4, cap_rule), rpop)
    landed = [k for k, v in routes.items() if set(v["set"]) == gold]
    ok(not landed, "no cheap route files the golden set (%d routes)" % len(routes), "; ".join(landed[:3]))
    ok(set(D["set"]) != gold, "clean-data test: the address route on the clean truth files %s" % ", ".join(D["set"]))

    # ---- the asks: every careful route on the clean truth, and the same routes read from the pack
    A, B, total, grant = calc.asks(W["agreements"], W["claims"], W["payments"], W["receipts"])
    RT = calc.ask_routes(W["agreements"], W["claims"], W["payments"], W["receipts"])
    RP = reader.ask_routes(P)
    for r in ELIGIBLE:
        ok(round(A[r]) == figs["remaining_%s" % r] and round(B[r]) == figs["unspent_%s" % r], "ask figures for %s match figures.json" % r)
        ok(round(A[r]) > 0 and round(B[r]) > 0, "ask figures for %s are not zero (no blind nil response keeps them)" % r)
    Ac, Bc = RT["cracker"]
    ok(all(abs(round(A[r]) - round(Ac[r])) >= 1000 and abs(round(B[r]) - round(Bc[r])) >= 1000 for r in ELIGIBLE),
       "the cracker misses every region on both asks by $1,000 or more", "nearest %d and %d" % (
           min(abs(round(A[r]) - round(Ac[r])) for r in ELIGIBLE), min(abs(round(B[r]) - round(Bc[r])) for r in ELIGIBLE)))
    tc = ROUND_BUDGET + sum(Bc.values()) - sum(Ac.values())
    ok(abs(round(grant) - round(tc / N_FUNDED)) >= 1000, "the grant each funded region receives: the cracker misses", "%d vs %d" % (round(grant), round(tc / N_FUNDED)))
    caps = {"claims all paid": (0, 0), "claims a transfer equals": (0, 0), "claims by payment timing": (5, 0),
            "every receipt": (0, 0), "register, closed in 2026": (0, 3), "register, every closure": (0, 3)}
    for k, (ca, cb) in caps.items():
        A2, B2 = RT[k]
        ka = sum(1 for r in ELIGIBLE if round(A2[r]) == round(A[r])); kb = sum(1 for r in ELIGIBLE if round(B2[r]) == round(B[r]))
        ok(ka <= ca and kb <= cb, "stop %r keeps at most %d remaining and %d unspent figures" % (k, ca, cb), "%d and %d" % (ka, kb))
    for k in RT:
        A2, B2 = RT[k]
        Ap, Bp = RP[k if k in RP else "golden"]
        ok(all(round(A2[r]) == round(Ap[NAME[r]]) for r in ELIGIBLE) and all(round(B2[r]) == round(Bp[NAME[r]]) for r in ELIGIBLE),
           "ask route %r computes the same figures on the clean truth and read from the pack" % k)
    An, Bn = RP["receipts net of every repeat"]
    kn = sum(1 for r in ELIGIBLE if round(Bn[NAME[r]]) == round(B[r]))
    ok(kn <= 8, "stop 'receipts net of every repeat' keeps at most 8 unspent figures: three councils still owed their repeat at the year end", str(kn))
    # device A forcing (lesson 8): each transfer equals the claims it pays; a transfer carrying an acquitted agreement's
    # retention with an open agreement's milestone has exactly one split, and the retention is what that agreement
    # needed to reach its final cost
    ag = {a["agreement"]: a for a in W["agreements"]}
    cl = {c["claim"]: c for c in W["claims"]}
    forced, nA, regions_A, unique = True, 0, set(), True
    for p in W["payments"]:
        if p.get("repeat_of"):
            continue
        cs = [cl[k] for k in p["claims"]]
        forced &= abs(sum(c["approved_amt"] for c in cs) - p["amount"]) < 0.005
        kinds = {(ag[c["agreement"]]["status"], c["milestone"] == "Retention") for c in cs}
        if ("Acquitted", True) in kinds and any(ag[c["agreement"]]["status"] == "Open" for c in cs):
            nA += 1
            regions_A.add(ag[p["claims"][0] and cs[0]["agreement"]]["region"])
            for c in cs:
                if c["milestone"] == "Retention":
                    a = ag[c["agreement"]]
                    forced &= abs(a["paid_before"] + c["approved_amt"] - a["final_cost"]) < 0.005
            window = [c for c in W["claims"] if c["council"] == p["payee"] and c["approved_on"] < p["paid_on"]]
            fits = [combo for k in (1, 2, 3) for combo in itertools.combinations(window, k)
                    if abs(sum(c["approved_amt"] for c in combo) - p["amount"]) < 0.005]
            unique &= len(fits) == 1
    ok(forced and nA > 0, "device A: every transfer equals the claims it pays; %d transfers settle an acquitted agreement's retention with an open agreement's milestone, each retention exactly what its agreement needed to reach its final cost" % nA)
    ok(unique, "device A: each such transfer has exactly one combination of its council's claims that sums to it")
    ok(set(ELIGIBLE) <= regions_A, "device A reaches every region", ", ".join(sorted(set(ELIGIBLE) - regions_A)))
    unpaid = [c for c in W["claims"] if not c["paid"]]
    ok(all(c["hold"] or c["approved_on"] >= dt.date(2026, 12, 28) for c in unpaid) and len(unpaid) > 0,
       "SF23 Ask A hazards: %d claims approved in 2026 had no 2026 transfer (approved in the program's last days, or held), and each stays on its agreement" % len(unpaid))
    reg_of = {c[0]: c[1] for c in COUNCILS}
    ok(set(ELIGIBLE) <= {reg_of[c["council"]] for c in unpaid}, "Ask A hazards: every region has a claim unpaid at the year end, so taking every approved claim as paid misses it")
    # device B forcing: a receipt returning a repeat with unspent money exceeds that money by exactly the repeat
    nB, forcedB, regions_B = 0, True, set()
    for r in W["receipts"]:
        kinds = {k for k, _, _ in r["parts"]}
        if kinds == {"unspent", "repeat"}:
            nB += 1; regions_B.add(reg_of[r["payer"]])
            un = sum(x for k, _, x in r["parts"] if k == "unspent")
            rp = sum(x for k, _, x in r["parts"] if k == "repeat")
            forcedB &= abs(r["amount"] - un - rp) < 0.005 and rp > 0
            for k, ref, x in r["parts"]:
                if k == "unspent":
                    a = ag[ref]
                    forcedB &= abs(a["paid_before"] - a["final_cost"] - x) < 0.005
    ok(forcedB and nB > 0, "device B: %d receipts return a repeat of the 19 March run with an acquitted agreement's unspent money; each exceeds that money by exactly the repeat" % nB)
    ok(set(ELIGIBLE) <= regions_B, "device B reaches every region", ", ".join(sorted(set(ELIGIBLE) - regions_B)))
    owed = W["vendor_ref"]["repeat_owed_at_year_end"]
    held_back = True
    for payee, pid, amt in owed:
        rs = [r for r in W["receipts"] if r["payer"] == payee]
        closed = [a["paid_before"] - a["final_cost"] for a in W["agreements"] if a["council"] == payee and a["final_cost"] is not None]
        held_back &= all(abs(r["amount"] - amt) > 0.005 and not any(abs(r["amount"] - amt - u) < 0.005 for u in closed) for r in rs)
    ok(held_back and len(owed) >= 2, "SF24 device B's over-cleaning half: %d councils' repeats sit in no 2026 receipt (neither alone nor beside a closed agreement's unspent money)" % len(owed))
    amts = collections.Counter((p["payee"], round(p["amount"], 2)) for p in W["payments"])
    ok(all(v <= 2 for v in amts.values()), "transfer amounts are unique within each payee apart from the repeated run")
    # the round's total and the grant read one way
    sA = sum(int(round(A[r])) for r in ELIGIBLE); sB = sum(int(round(B[r])) for r in ELIGIBLE)
    ok(figs["round_total"] == ROUND_BUDGET + sB - sA and int(round(total)) == figs["round_total"] and int(round(grant)) == figs["grant_each"] == int(round(figs["round_total"] / N_FUNDED)),
       "SF21 the round's total and each grant are the same from the cents and from the dollar figures", "%d, %d" % (figs["round_total"], figs["grant_each"]))

    # ---- the realism sweep and the containers
    def steps(vals):
        return {b - a for a, b in zip(vals, vals[1:])}
    rows = list(csv.DictReader(open(os.path.join(T, "rtip_claims_2026.csv"))))
    ok(len(steps(sorted(int(r["claim_no"][3:]) for r in rows))) > 1, "realism: claim numbers do not advance in one fixed step")
    pays = list(csv.DictReader(open(os.path.join(T, "ap_payments_rtip_2026.csv"))))
    ok(len(steps(sorted(int(p["payment_id"][2:]) for p in pays))) > 1, "realism: payment ids do not advance in one fixed step")
    recs = list(csv.DictReader(open(os.path.join(T, "ar_receipts_rtip_2026.csv"))))
    ok(len(steps(sorted(int(r["receipt_no"][2:]) for r in recs))) > 1, "realism: receipt numbers do not advance in one fixed step")
    ok(sorted(p["payment_id"] for p in pays) == [p["payment_id"] for p in sorted(pays, key=lambda p: (p["paid_on"], p["payment_id"]))],
       "realism: payment ids rise with the payment date, as the finance system raises them")
    ok(sorted(r["receipt_no"] for r in recs) == [r["receipt_no"] for r in sorted(recs, key=lambda r: (r["receipted_on"], r["receipt_no"]))],
       "realism: receipt numbers rise with the receipt date")
    by_round = collections.defaultdict(list)
    for a in W["agreements"]:
        by_round[a["round"]].append(int(a["agreement"][-3:]))
    ok(all(len(steps(sorted(v))) > 1 for v in by_round.values() if len(v) > 3), "realism: agreement numbers within a round carry the gaps of unfunded applications")
    tok = sorted(P["weight"])
    ok(all(re.fullmatch(r"[0-9a-f]{12}", t) for t in tok) and len(steps([int(t, 16) for t in tok])) > 1000, "realism: card tokens are twelve hexadecimal characters with no step")
    ok([r for r in CODES] != sorted(CODES) and [NAME[r] for r in CODES] != sorted(NAME[r] for r in CODES), "realism: regions are not in alphabetical order")
    shapes = {re.sub(r"[A-Z][a-z]+( [A-Z][a-z]+)*", "X", c[0], count=1) for c in COUNCILS}
    ok(len(shapes) > 2, "realism: council names take %d shapes" % len(shapes))
    def abn_ok(s):
        d = [int(x) for x in s.replace(" ", "")]
        d[0] -= 1
        return sum(a * b for a, b in zip([10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19], d)) % 89 == 0
    ok(all(abn_ok(p["payee_abn"]) for p in pays) and all(abn_ok(r["payer_abn"]) for r in recs), "realism: every ABN carries a valid check")
    weekday = all(dt.datetime.strptime(r["approved_on"], "%d/%m/%Y").weekday() < 5 for r in rows) and \
        all(dt.date.fromisoformat(p["paid_on"]).weekday() < 5 for p in pays) and all(dt.date.fromisoformat(r["receipted_on"]).weekday() < 5 for r in recs)
    ok(weekday, "realism: approvals, payments and receipts fall on working days")
    tots = {r: sum(x["erp"] for x in P["sa2"].values() if P["sa2_region"][[k for k, v in P["sa2"].items() if v is x][0]] == r) for r in CODES}
    ok(all(v % 100 != 0 for v in tots.values()), "realism: no region's population sums to a round hundred")
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    pulls = {"rtip_claims_2026.csv": max(dt.datetime.strptime(r["approved_on"], "%d/%m/%Y").date() for r in rows),
             "ap_payments_rtip_2026.csv": max(dt.date.fromisoformat(p["paid_on"]) for p in pays),
             "ar_receipts_rtip_2026.csv": max(dt.date.fromisoformat(r["receipted_on"]) for r in recs)}
    ok(all(v <= dt.date.fromisoformat(meta["files"][k]["date"]) for k, v in pulls.items()), "realism: no extract carries a date after its own pull")
    # containers: the writer's signature scrubbed, every document dated by its issuer, created before modified
    scrub = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "scrub_producer_metadata.py")
    out = subprocess.run([sys.executable, scrub, T], capture_output=True, text=True).stdout
    ok("clean" in out, "H1 the scrub audit finds no writer signature in the pack", out.strip().splitlines()[0][:90] if out.strip() else "")
    out = subprocess.run([sys.executable, scrub, GD], capture_output=True, text=True).stdout
    ok("clean" in out, "H1 the scrub audit finds no writer signature in the goldens", out.strip().splitlines()[0][:90] if out.strip() else "")
    stamps = {}
    for d in (T, GD):
        for fn in sorted(os.listdir(d)):
            p = os.path.join(d, fn)
            if fn.endswith((".xlsx", ".docx")):
                core = zipfile.ZipFile(p).read("docProps/core.xml").decode()
                c0 = re.search(r"<dcterms:created[^>]*>([^<]+)<", core).group(1); m0 = re.search(r"<dcterms:modified[^>]*>([^<]+)<", core).group(1)
                stamps[fn] = (c0, m0)
                ok(c0 <= m0 and "2026-01-01" <= c0 <= "2027-02-05T23:59:59Z", "H13 %s created %s, modified %s" % (fn, c0[:10], m0[:10]))
            elif fn.endswith(".pdf"):
                raw = open(p, "rb").read()
                cd = re.search(rb"/CreationDate \(D:(\d{8})", raw).group(1).decode()
                md = re.search(rb"/ModDate \(D:(\d{8})", raw).group(1).decode()
                stamps[fn] = (cd, md)
                ok(cd <= md and "20260101" <= cd <= "20270205" and b"ReportLab" not in raw, "H13 %s dated %s by its issuer, no writer comment" % (fn, cd))
    ok(len({v[0] for v in stamps.values()}) == len(stamps), "H13 every document carries its own creation stamp")
    from pypdf import PdfReader
    for fn in ("rvif_2027_round_guidelines.pdf", "rtip_closure_decision_2026.pdf"):
        p = os.path.join(T, fn)
        strict = " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(p, strict=True).pages)
        pt = " ".join(subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True).stdout.split())
        key = "less what remains of the agreements" if "closure" in fn else "International Recommendations for Tourism Statistics 2008"
        ok(len(strict) > 500 and key in strict and key in pt, "H25 %s reads under the strict reader and pdftotext, the filed sentence in both" % fn)
    # the goldens agree with figures.json
    gcsv = list(csv.DictReader(open(os.path.join(GD, "regional_visitor_spend_2026.csv"))))
    ok(all(int(r["visitor_spend_per_resident_aud"]) == figs["per_resident_%s" % r["region_code"]] and int(r["visitor_spend_2026_aud"]) == figs["total_%s" % r["region_code"]]
           and [int(r["visitor_spend_q%d_aud" % i]) for i in (1, 2, 3, 4)] == figs["q_%s" % r["region_code"]] for r in gcsv) and len(gcsv) == len(ELIGIBLE),
       "the golden CSV carries figures.json for every eligible region")
    from docx import Document
    doc = Document(os.path.join(GD, "rvif_2027_round_paper.docx"))
    dtext = " ".join(p.text for p in doc.paragraphs) + " " + " ".join(c.text for t in doc.tables for row in t.rows for c in row.cells)
    need = ["${:,}".format(figs["grant_each"]), "${:,}".format(figs["gap_per_resident"]), "${:,}".format(figs["round_total"])] + \
        ["${:,}".format(figs["remaining_%s" % r]) for r in ELIGIBLE] + ["${:,}".format(figs["unspent_%s" % r]) for r in ELIGIBLE]
    ok(all(x in dtext for x in need) and all(n in dtext for n in figs["call"]), "the golden paper carries the call, the gap, both tables' figures, the round's total and the grant")
    ok("\u2014" not in dtext and "\u2013" not in dtext, "the golden paper carries no em or en dash")

    # ---- the distractors: deleted one at a time, every graded figure is unchanged
    for dfile in meta["distractors"]:
        tmp = tempfile.mkdtemp(prefix="t454_")
        try:
            for fn in os.listdir(T):
                if fn != dfile:
                    shutil.copy(os.path.join(T, fn), tmp)
            P2 = reader.load(tmp)
            pop2 = reader.region_pop(P2)
            m2, d2 = reader.presence(P2)
            q2 = reader.visitor_spend(P2, lambda row: not (len(m2[(row[0], row[1])]) >= 6 and d2[(row[0], row[1])] >= 30))
            A2, B2 = reader.ask_routes(P2)["golden"]
            same = all(int(round(sum(q2[r]) / pop2[r])) == figs["per_resident_%s" % r] and round(A2[NAME[r]]) == figs["remaining_%s" % r]
                       and round(B2[NAME[r]]) == figs["unspent_%s" % r] for r in ELIGIBLE)
            ok(same, "distractor %s deleted: the call and every ask figure are unchanged" % dfile)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # ---- the input gates and the pack's hygiene
    files = sorted(os.listdir(T))
    ok(len(files) >= 10, "at least 10 files", str(len(files)))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "at least 3 formats", str(sorted({f.rsplit(".", 1)[1] for f in files})))
    with open(os.path.join(T, "apn_pos_research_extract_2026.csv")) as f:
        n = sum(1 for _ in f) - 1
    ok(n >= 25000 and n == figs["sample_rows"], "a file of 25,000 rows or more", str(n))
    ok(set(meta["files"]) == set(files) and all(v.get("source") and v.get("date") and v.get("licence") for v in meta["files"].values()),
       "metadata.json gives source, date and licence for every shipped file")
    ok(len(meta["distractors"]) >= 2 and all(d in files for d in meta["distractors"]), "two or more distractors named in metadata.json")
    bad = [f for f in files if any(w in f.lower() for w in ("readme", "dictionary", "notes", "manifest", "layout", "codebook", "distractor"))]
    ok(not bad, "no file describes the data or names its role", ", ".join(bad))
    with zipfile.ZipFile(os.path.join(TASK, "target.zip")) as z:
        same = sorted(i.filename for i in z.infolist()) == sorted(files) and \
            all(z.read(f) == open(os.path.join(T, f), "rb").read() for f in files)
    ok(same, "target.zip holds exactly the files of target/, byte for byte, with no enclosing folder (H4)")
    print("\n%d failures" % len(FAIL))
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
