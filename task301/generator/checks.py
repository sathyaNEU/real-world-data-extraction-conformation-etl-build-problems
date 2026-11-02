"""The generator's assertions on the cut pack (task301/target) and the clean truth: the three-rules block (R1 to R3c),
the ladder, every semantic fork (SF1 to SF18), mess neutrality, the asks and their devices, the separation line, the
input gates, the realism sweep, the leak sweep and every graded figure's distance to its rounding edge. Exit 1 on any
failure."""
import collections
import copy
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import analysis as AN  # noqa: E402
import golden as GD  # noqa: E402
import io_util as IO  # noqa: E402
import pack  # noqa: E402
import params as P  # noqa: E402
import register as RG  # noqa: E402
import world  # noqa: E402

T = os.path.join(TASK_DIR, "target")
RESULTS = []
CLAIMED, AUTOMATIC = AN.CLAIMED, AN.AUTOMATIC


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def order(d):
    return sorted(d, key=lambda m: -d[m])


def margin(d):
    o = order(d)
    return d[o[0]] / d[o[1]]


def r3(H, F, L, lag=None, curves=None, modes=None, T_=1.0):
    """Children brought above the line in 2027 by each measure, the golden construction on given inputs: C's
    newly entitled claim along the April 2024 cohort's cumulative share of its band, B's and D's along the launch's."""
    lag = L["paces"]["lag"] if lag is None else lag
    curves = curves or {"B": L["L"][AN.GOLD][0], "C": L["W"][AN.GOLD][0], "D": L["L"][AN.GOLD][0]}
    out = {}
    for m in ("A", "B", "C", "D", "E"):
        if m in AUTOMATIC and not (modes and m in modes):
            out[m] = AN.static(H, F, m)
        else:
            mode, curve = (modes or {}).get(m, ("pace", curves.get(m)))
            out[m] = AN.first_year(H, F, m, curve, lag, T_, mode)
    return out


def edge(v, unit=100):
    return unit / 2.0 - abs(v - unit * round(v / unit))


# ---------------------------------------------------------------- the clean truth (the world before the pack)
def clean_households(W):
    out = []
    for h in W["hh"]:
        out.append({"hid": None, "prov": h["prov"], "w": h["w"], "eq": h["eq"], "kids": h["kids"],
                    "disp": h["disp25"], "cfv": h["cfv_recv25"], "now": h["cfv_now"], "filed": h["filed"],
                    "gross": h["gross25"] if h["filed"] else None, "renting": h["renting"],
                    "base27": h["disp25"] * P.UPRATE_2025_2027, "comp_eq": h["comp_eq"]})
    return out


def clean_curves(W, R):
    """The two openings' cumulative claims as a share of their band, from the world's own claims and households."""
    g = [a for a in R["awards"] if a["tipo"] == "I" and a["res"] == "C" and not a["appeal"]]
    hh = [h for h in W["hh"] if h["kids"]]
    stock_w = sum(h["w"] for h in hh if P.CFV_LIMIT_OLD <= h["comp_eq"] < P.CFV_LIMIT)
    stock_l = sum(h["w"] for h in hh if h["comp_eq"] < P.CFV_LIMIT_OLD)

    def curve(sel, t_open, stock):
        cnt = collections.Counter(RG.t_of(a["claim"].year, a["claim"].month) - t_open + 1 for a in sel)
        out, acc = [], 0
        for k in range(1, 13):
            acc += cnt.get(k, 0)
            out.append(acc / stock)
        return out
    widen = curve([a for a in g if P.CFV_LIMIT_OLD <= a["inc"] < P.CFV_LIMIT and a["claim"] >= P.CFV_LIMIT_RISE],
                  RG.RISE_T, stock_w)
    launch = curve([a for a in g if a["claim"] < P.CFV_LIMIT_RISE and a["inc"] < P.CFV_LIMIT_OLD], 0, stock_l)
    lag = collections.Counter(a["first"] - RG.t_of(a["claim"].year, a["claim"].month) for a in g)
    n = sum(lag.values())
    return {"widening": widen, "launch": launch, "lag": [(k, v / n) for k, v in sorted(lag.items())]}


def clean_take_up(W, R):
    tD = RG.t_of(2025, 12)
    paid = set(a["fid"] for a in R["awards"] if a["res"] == "C" and a["first"] is not None and a["first"] <= tD
               and (a["last"] is None or a["last"] >= tD) and a["dec"] <= RG.YEAR_END)
    ent = sum(h["w"] for h in W["hh"] if h["kids"] and h["assessed"] < P.CFV_LIMIT) if "assessed" in W["hh"][0] else None
    return paid, ent


def main():
    meta = json.load(open(os.path.join(TASK_DIR, "metadata.json")))
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    L = AN.ladder(T)
    F, H, PC, TU = L["F"], L["H"], L["paces"], L["T"]
    G = AN.golden(T)
    W = world.build(P.SEED)
    R = RG.build(np.random.default_rng(P.SEED + 77), W)
    reg = AN.register(T)

    # ------------------------------------------------------------------ R1 to R3c, the three rules executed
    hh_h, _ = IO.read_csv(os.path.join(T, pack.FILES["households"]), delimiter=";")
    pe_h, pe_r = IO.read_csv(os.path.join(T, pack.FILES["persons"]), delimiter=";")
    rg_h, rg_r = IO.read_csv(os.path.join(T, pack.FILES["register"]), delimiter="|")
    check("R1a raw material: household microdata with weights and income components, persons with birth years",
          {"household_weight", "disposable_income_2025", "complemento_familiar_2025", "irpf_gross_income_2025"}
          <= set(hh_h) and "birth_year" in pe_h, "%d households, %d persons" % (len(H), len(pe_r)))
    check("R1b raw material: the register holds claims with dates, computable incomes and months paid, and no pace, "
          "take-up, cohort or eligibility column", {"claim_date", "decision_date", "computable_income_per_eq_adult",
                                                    "first_month_paid"} <= set(rg_h)
          and not any(re.search(r"pace|take.?up|cohort|eligib|newly|band", c, re.I) for c in rg_h + hh_h + pe_h))
    check("R1c the decisive construction reads the register's own claim records month by month",
          PC["n_widening"] > 2000 and PC["n_launch"] > 2000, "%d widening, %d launch claims" % (PC["n_widening"],
                                                                                              PC["n_launch"]))
    H_clean = clean_households(W)
    CC = clean_curves(W, R)
    paid, ent = clean_take_up(W, R)
    Tc = round(len(paid) / ent, 3) if ent else TU
    R0c = {m: AN.static(H_clean, F, m) for m in ("A", "B", "C", "D", "E")}
    R1c = {m: (Tc * R0c[m] if m in CLAIMED else R0c[m]) for m in R0c}
    check("R3a analyst test on the clean truth: static microsimulation at the coverage rate files C",
          order(R1c)[0] == "C" and margin(R1c) > 1.5, "C %.0f, next %.0f, A %.0f (coverage %.3f)" % (
              R1c["C"], sorted(R1c.values())[-2], R1c["A"], Tc))
    gold_c = {"B": CC["launch"], "C": CC["widening"], "D": CC["launch"]}
    R3c_ = r3(H_clean, F, L, lag=CC["lag"], curves=gold_c)
    check("R3b the decisive step alone on the clean truth: the widening's own claims for C's newly entitled file A",
          order(R3c_)[0] == "A" and margin(R3c_) > 1.4, "A %.0f, C %.0f, B %.0f, D %.0f" % (
              R3c_["A"], R3c_["C"], R3c_["B"], R3c_["D"]))
    R2c = r3(H_clean, F, L, lag=CC["lag"], curves={m: CC["launch"] for m in CLAIMED})
    R1bc = r3(H_clean, F, L, lag=CC["lag"], modes={m: ("once", None) for m in CLAIMED}, T_=Tc)
    check("R3b' each lower rung's correction alone stays on C on the clean truth (claims at once, the launch's pace)",
          all(order(d)[0] == "C" for d in (R1bc, R2c)),
          "once C %.0f, launch C %.0f, A %.0f" % (R1bc["C"], R2c["C"], R2c["A"]))
    dups = len(rg_r) - len(set(tuple(r) for r in rg_r))
    check("R3c no plant: no duplicated register row, no copied claim sequence", dups == 0, "%d exact duplicates" % dups)
    docs_txt = " ".join(IO.pdf_text(os.path.join(T, pack.FILES[k])) for k in ("proposals", "rules", "coverage",
                                                                            "results"))
    docs_txt += " " + IO.docx_text(os.path.join(T, pack.FILES["guidance"]))
    check("R3c' no plant: no memo, draft or stakeholder figure; no document names a claiming pace, a first-year "
          "share, a phasing or a cohort", not re.search(r"\bpace\b|first[- ]year|phas|ramp|cohort|build[- ]up|"
                                                        r"claim(s|ing)? (rate|speed)|take-up curve|memo|draft",
                                                        docs_txt, re.I))

    # ------------------------------------------------------------------ the ladder
    R0, R1, R1b, R2, R2e_, R3 = L["R0"], L["R1"], L["R1b"], L["R2"], L["R2e"], L["R3"]
    check("L1 R0 static: C first, A 4th or 5th", order(R0)[0] == "C" and order(R0).index("A") >= 3,
          " > ".join("%s %.0f" % (m, R0[m]) for m in order(R0)))
    check("L2 R1 at the coverage rate (the default path): C first by 1.15 or more, A not first or second",
          order(R1)[0] == "C" and margin(R1) >= 1.15 and order(R1).index("A") >= 2, "C %.0f, margin %.2f" % (
              R1["C"], margin(R1)))
    check("L3 R1b claims at the opening: C first by 1.15 or more, A not second",
          order(R1b)[0] == "C" and margin(R1b) >= 1.15 and order(R1b).index("A") >= 2, "C %.0f, A %.0f" % (
              R1b["C"], R1b["A"]))
    check("L4 R2 C at the launch's pace: C first, A second by 1.2 or more (the one rung A is second on)",
          order(R2)[0] == "C" and R2["C"] / R2["A"] >= 1.2 and order(R2).index("A") == 1,
          "C %.0f against A %.0f, %.2f" % (R2["C"], R2["A"], R2["C"] / R2["A"]))
    check("L5 R3 golden: A first, final margin 1.5 or more", order(R3)[0] == "A" and margin(R3) >= 1.5,
          "A %.0f, next %.0f, %.2f" % (R3["A"], sorted(R3.values())[-2], margin(R3)))
    lic = L["licensed"]
    for name, d in lic.items():
        best = max((v, m) for m, v in d.items() if m != "A")
        check("L6 licensed estimator files A by 1.3 or more: %s" % name, order(d)[0] == "A" and d["A"] / best[0] >= 1.3,
              "A %.0f against %s %.0f, %.2f" % (d["A"], best[1], best[0], d["A"] / best[0]))
    cmax = max(d["C"] for d in lic.values())
    check("L6b C stays under A by 1.5 or more under every licensed estimator", R3["A"] / cmax >= 1.5,
          "C at most %.0f, %.2f" % (cmax, R3["A"] / cmax))
    wr = L["wrong"]
    check("L7 every wrong route files a measure other than A (the full-year, coverage, at-once, launch-pace and phasing "
          "routes)", sum(1 for d in wr.values() if order(d)[0] != "A") >= len(wr) - 1,
          "%d of %d off A; on A: %s" % (sum(1 for d in wr.values() if order(d)[0] != "A"), len(wr),
                                        ", ".join(k for k, d in wr.items() if order(d)[0] == "A") or "none"))
    check("L8 A is automatic: its figure is the same on every rung and every construction",
          len({round(d["A"], 6) for d in list(lic.values()) + list(wr.values())}) == 1)
    wg, lg = L["W"][AN.GOLD][0][11], L["L"][AN.GOLD][0][11]
    check("L9 the launch's claims run about twice the April 2024 band's in the first year (the quiet ruling-out)",
          lg / wg >= 1.5, "%.2f times at month 12 (%.3f against %.3f of each band)" % (lg / wg, lg, wg))
    rival = max(v for d in lic.values() for m, v in d.items() if m != "A")
    check("L10 every rival stays under the stated bound of 3,000 in every licensed construction", rival < GD.RIVAL_BOUND,
          "max %.0f" % rival)
    check("L11 the estimated claim rates of the April 2024 band sit far below the 4 per cent a month at which C would "
          "pass A", L["Wpar"]["lam1"] < 0.03 and L["Wpar"]["lam2"] < 0.035,
          "full band %.4f, not yet claiming %.4f, fitted mu %.4f" % (L["Wpar"]["lam1"], L["Wpar"]["lam2"],
                                                                    L["Wpar"]["mu"]))

    # ------------------------------------------------------------------ semantic forks
    def alt_survey(**kw):
        F2 = dict(F)
        F2.update(kw)
        return F2, AN.survey(T, F2)
    F1, H1 = alt_survey(born_from=2010)
    a1 = r3(H1, F1, L)
    check("SF1 children as members born 2010 or later: the call stays A", order(a1)[0] == "A", "A %.0f" % a1["A"])

    def lifted_strict(h, line, pay):
        return h["base27"] / h["eq"] < line < (h["base27"] + pay) / h["eq"]
    saved = AN.lifted
    AN.lifted = lifted_strict
    try:
        a2 = r3(H, F, L)
    finally:
        AN.lifted = saved
    check("SF2 strictly above the line: same call and A's figure unchanged", order(a2)[0] == "A"
          and abs(a2["A"] - R3["A"]) < 1e-6)
    gtxt = IO.docx_text(os.path.join(T, pack.FILES["guidance"]))
    check("SF3 the full-year and coverage-rate bases file C and break the guidance: payments as received in calendar "
          "2027, a claimed measure paying only once claimed and decided (3.9), so no newly entitled family is paid "
          "for January", order(R1)[0] == "C" and "calendar 2027" in gtxt and "actually receives during 2027" in gtxt
          and "has claimed and its claim has been decided" in gtxt and min(k for k, _ in PC["lag"]) >= 1)
    F4, H4 = alt_survey(age_base=2027)
    a4 = r3(H4, F4, L)
    check("SF4 ages as 2027 less the birth year: the call stays A", order(a4)[0] == "A")
    H5 = [dict(h, base27=(h["disp"] - h["cfv"]) * F["uprate"]) for h in H]
    a5 = r3(H5, F, L)
    check("SF5 the 2025 Complemento left out of the base: the call stays A", order(a5)[0] == "A")
    H6 = [dict(h, comp_eq=h["comp_eq"] * F["uprate"]) for h in H]
    a6 = r3(H6, F, L)
    check("SF6 eligibility income raised 6.1 per cent: the call stays A", order(a6)[0] == "A")
    H7 = [dict(h, w=1.0) for h in H]
    a7 = r3(H7, F, L)
    check("SF7 unweighted sample children: the call stays A", order(a7)[0] == "A")
    saved_p = AN.pays

    def pays_c_all(F_):
        d = saved_p(F_)
        d["C"] = lambda h: 12 * F_["cfv_rate"] * h["kids"] if (h["kids"] and F_["C_old"] <= h["comp_eq"] < F_["C_new"]) else 0.0
        return d
    AN.pays = pays_c_all
    try:
        a8 = r3(H, F, L)
    finally:
        AN.pays = saved_p
    prop = IO.pdf_text(os.path.join(T, pack.FILES["proposals"]))
    check("SF8 C's newly covered families are filed as those in the band who do not receive the Complemento, and "
          "counting current recipients again still files A", "who do not receive it" in prop and order(a8)[0] == "A",
          "C %.0f under the other reading" % a8["C"])

    def pays_a_all(F_):
        d = saved_p(F_)
        d["A"] = lambda h: 12 * F_["A_rate"] * h["kids"] if (h["kids"] and (h["gross"] is None or h["gross"] < F_["A_limit"])) else 0.0
        return d
    AN.pays = pays_a_all
    try:
        a9 = r3(H, F, L)
    finally:
        AN.pays = saved_p
    check("SF9 non-filers reached by A: the call stays A", order(a9)[0] == "A")
    a10 = r3(H, F, L, modes={"E": ("pace", L["L"][AN.GOLD][0])})
    check("SF10 E claimed at the launch's pace: the call stays A", order(a10)[0] == "A")
    a11 = r3(H, F, L, lag=[(0, 1.0)])
    check("SF11 claimed measures paid from the claim month: the call stays A", order(a11)[0] == "A",
          "C %.0f" % a11["C"])
    a12 = r3(H, F, L, lag=[(k + 1, v) for k, v in PC["lag"]])
    check("SF12 each month's payment received a month in arrears: the call stays A", order(a12)[0] == "A")
    check("SF13 A's province figures add to its region figure (the survey province is the only province)",
          abs(sum(G["A_by_prov"].values()) - G["A_total"]) < 1e-6)
    check("SF14 the rounded province figures add to the rounded region figure",
          sum(G["A_by_prov_r"].values()) == G["A_total_r"], "%s = %d" % (G["A_by_prov_r"], G["A_total_r"]))
    keys = list(lic)
    pick = lambda frag: [k for k in keys if frag in k]
    for sf, names in (("SF15", pick("normalised curve at the coverage rate")),
                      ("SF16", pick("golden curves, ")),
                      ("SF17", pick("flat") + pick("fitted") + pick("first month paid") + pick("pending"))):
        check("%s licensed readings (%d): the call stays A" % (sf, len(names)),
              names and all(order(lic[k])[0] == "A" for k in names))
    rtxt = IO.pdf_text(os.path.join(T, pack.FILES["rules"]))
    inc_all = AN.incidents(T)
    may = [r for r in inc_all if r["type"] == "Child reached 18"]
    ended_bad = 0
    for r in may:
        t = AN.mi((r["date"].year, r["date"].month))
        fam_rows = [x for x in reg if x["fam"] == r["fam"] and x["res"] == "GRANTED" and x["first"] is not None]
        cov = [x for x in fam_rows if AN.mi(x["first"]) <= t and (x["last"] is None or AN.mi(x["last"]) >= t)]
        if cov and max(x["kids"] for x in cov) == 1:
            if any(x["last"] is None or AN.mi(x["last"]) > t for x in cov) or any(AN.mi(x["first"]) > t for x in fam_rows):
                ended_bad += 1
    check("SF19 the last child reaching 18 ends the award with that month (rules 8), and the register agrees",
          "the award ends with that month" in rtxt and ended_bad == 0, "%d inconsistent families" % ended_bad)
    check("SF20 suspended months lifted within three months are months the award pays for (rules 7.2)",
          "award pays for the suspended months" in rtxt)
    a21 = [r3(H, F, L, T_=1.0)]
    Lsave = L["T"]
    check("SF21 the coverage rate is kept off the golden: the call and every claimed figure are the same at any rate",
          all(abs(r3(H, F, L)[m] - R3[m]) < 1e-6 for m in R3) and Lsave == TU)
    fh, frows = IO.read_csv(os.path.join(T, pack.FILES["fieldwork"]))
    fx = {k: i for i, k in enumerate(fh)}
    by_case = {r[fx["case"]]: r for r in frows}
    re2 = [r for r in frows if r[fx["issue"]] == "2"]
    linked = all(r[fx["reissue_of"]] in by_case and by_case[r[fx["reissue_of"]]][fx["issue"]] == "1" and
                 by_case[r[fx["reissue_of"]]][fx["dwelling"]][:5] == r[fx["dwelling"]][:5] for r in re2)
    check("SF22 a dwelling issued twice: every reissue names the case it reissues, in the same municipality",
          re2 and linked, "%d reissues" % len(re2))
    near = [h for h in H if h["kids"] and h["gross"] is not None and abs(h["gross"] - F["A_limit"]) < 1.0]
    near += [h for h in H if h["kids"] and not h["now"] and min(abs(h["comp_eq"] - x) for x in (F["C_old"],
                                                                                              F["C_new"])) < 0.5]
    near += [h for h in H if h["kids"] and abs(h["comp_eq"] - F["line"]) < 0.5]
    near += [h for h in H if h["kids"] and abs(h["base27"] / h["eq"] - F["line"]) < 0.01]
    payA = AN.pays(F)["A"]
    near += [h for h in H if payA(h) and abs((h["base27"] + payA(h)) / h["eq"] - F["line"]) < 0.01]
    check("SF18 no household on a boundary (A's income limit, the C band, the line, A's lifted line)", not near,
          "%d households" % len(near))

    # ------------------------------------------------------------------ mess neutrality (Layer 1, one line per item)
    zero_dev = [r for r in reg if r["type"] == "INITIAL" and r["res"] in ("REVOKED",)]
    check("R2.1 revocations sit on renewals only: zero REVOKED initial claims in the call's population", not zero_dev)
    single = collections.Counter(r["case"] for r in reg)
    gi = AN.granted_initial(reg)
    stock_w, stock_l = PC["w_stock"], PC["l_stock"]

    def abs_curve(dates, open_month, stock):
        cnts = AN.monthly(dates, open_month, 12)
        return [sum(cnts[:k]) / stock for k in range(1, 13)]
    w_noapp = abs_curve([r["claim"] for r in gi if single[r["case"]] == 1 and F["cfv_old_limit"] <= r["inc"] <
                         F["cfv_limit"] and r["claim"] >= F["rise_date"]], (2024, 4), stock_w)
    a_app = r3(H, F, L, curves={"B": L["L"][AN.GOLD][0], "C": w_noapp, "D": L["L"][AN.GOLD][0]})
    check("R2.2 appeals left out of the widening cohort: the call stays A", order(a_app)[0] == "A")
    launch_dm = []
    for r in gi:
        if r["claim"] < F["rise_date"] and r["inc"] < F["cfv_old_limit"]:
            c = r["claim"]
            launch_dm.append(dt.date(c.year, c.day, c.month) if c.day <= 12 else c)
    l_dm = abs_curve(launch_dm, (2022, 10), stock_l)
    a_dm = r3(H, F, L, curves={"B": l_dm, "C": L["W"][AN.GOLD][0], "D": l_dm})
    check("R2.3 the migration's legacy dates read month first where they parse: the call stays A", order(a_dm)[0] == "A")
    tmp = tempfile.mkdtemp(prefix="t301_ask_")
    for f in os.listdir(T):
        if f not in (pack.FILES["incidents"], pack.FILES["fieldwork"], pack.FILES["codes"]):
            shutil.copy(os.path.join(T, f), tmp)
    L2 = AN.ladder(tmp)
    check("R2.4 the incident log, the fieldwork export and the code list deleted: the call and A's figures unchanged "
          "(the office column, moves and re-sectioned references never reach the call)",
          order(L2["R3"])[0] == "A" and abs(L2["R0"]["A"] - R0["A"]) < 1e-6 and L2["A_by_prov"] == L["A_by_prov"])
    shutil.rmtree(tmp)
    check("R2.5 the call's population carries no renewal, change of claimant or revocation row (overlaps, suspensions, "
          "extinctions and revocations are ask-side)", all(r["type"] == "INITIAL" for r in gi))
    rate_hist = sorted({r["first"] for r in gi if r["first"]})
    check("R2.6 the mid-2025 uprating: C is appraised at the 2027 amount whatever the register's monthly amounts",
          F["cfv_rate"] == P.CFV_RATE_2027 and len(rate_hist) > 30)

    # ------------------------------------------------------------------ ask 1: the Complemento's 2025 families
    fam = G["families"]
    moves = {}
    for r in R["incidents"]:
        if r["type"] == "DOM":
            moves.setdefault(r["fid"], []).append((r["date"], r["dato"]))
    first_muni = {f["fid"]: f["muni"] for f in R["fams"]}
    truth = {}
    for ym in AN.QUARTER_ENDS:
        t = RG.t_of(*ym)
        fs = set()
        for a in R["awards"]:
            if a["res"] == "C" and a["first"] is not None and a["dec"] is not None and a["dec"] <= RG.YEAR_END \
                    and a["first"] <= t and (a["last"] is None or a["last"] >= t):
                fs.add(a["fid"])
        cnt = collections.Counter()
        for fid in fs:
            muni = first_muni[fid]
            for d, new in sorted(moves.get(fid, [])):
                if RG.t_of(d.year, d.month) + 1 <= t:
                    muni = new
            cnt[muni[:2]] += 1
        truth[ym] = dict(cnt)
    check("K1 ask 1 equals the clean truth in all 12 cells", truth == fam, "%s" % {k: v for k, v in fam.items()})
    crack = ask1_cracker(T)
    keep = sum(1 for ym in fam for pc in fam[ym] if crack[ym].get(pc) == fam[ym][pc])
    check("K2 device mass: the careful route (granted rows only, every hazard handled) misses all 12 cells",
          keep == 0, "%d kept" % keep)
    revk = collections.Counter()
    for a in R["awards"]:
        if a.get("revoked"):
            assert a["revoked"] > RG.YEAR_END
    check("K3 every revocation is dated in 2026, after the cut-off, and sits on the case of the award it revokes",
          all(r["dec"] > AN.CUTOFF for r in reg if r["type"] == "REVOCATION") and
          {r["case"] for r in reg if r["type"] == "REVOCATION"} == {r["case"] for r in reg if r["res"] == "REVOKED" and
                                                                    r["type"] != "REVOCATION"})
    for name, mode in (("the register's province column as residence", "office"), ("every row counted", "rows"),
                       ("moves ignored", "nomoves"), ("moves from the month recorded", "samemonth")):
        alt = ask1_cracker(T, mode, revoked=True)
        k = sum(1 for ym in fam for pc in fam[ym] if alt[ym].get(pc) == fam[ym][pc])
        revk[name] = k
    check("K4 each hazard moves cells on its own (office column, overlap rows, moves, the move's month)",
          revk["the register's province column as residence"] <= 3 and revk["every row counted"] == 0
          and revk["moves ignored"] < 12 and revk["moves from the month recorded"] < 12, "%s" % dict(revk))

    # ------------------------------------------------------------------ ask 2: the ECVV 2026 fieldwork
    fw = G["fieldwork"]
    tru = {}
    for d in W["dwellings"]:
        e = tru.setdefault(d["prov"], [0, 0])
        if d["final"] not in (31, 32, 33):
            e[0] += 1
            if d["final"] == 11:
                e[1] += 1
    check("F1 ask 2 equals the clean truth in every province", all(fw[pc][0] == tru[pc][0] and fw[pc][1] == tru[pc][1]
                                                                    for pc in tru))
    fc = ask2_cracker(T)
    kept_el = sum(1 for pc in fw if fc[pc][0] == fw[pc][0])
    kept_rate = sum(1 for pc in fw if fc[pc][2] == fw[pc][2])
    kept_co = sum(1 for pc in fw if fc[pc][1] == fw[pc][1])
    check("F2 device mass: the reference as the dwelling misses every province's eligible dwellings and response rate",
          kept_el == 0 and kept_rate == 0, "eligible kept %d, rate kept %d, complete kept %d" % (kept_el, kept_rate,
                                                                                               kept_co))
    resect = [r for r in re2 if by_case[r[fx["reissue_of"]]][fx["dwelling"]] != r[fx["dwelling"]]]
    same_serial = all(by_case[r[fx["reissue_of"]]][fx["dwelling"]][-4:] == r[fx["dwelling"]][-4:] for r in resect)
    check("F3 the reissues whose reference changed (renumbered census sections) keep the dwelling's municipality and "
          "serial and link to their first issue only through reissue_of", resect and same_serial,
          "%d such reissues" % len(resect))
    fo = ask2_cracker(T, "office")
    check("F4 the office column as the province moves the border provinces' figures",
          sum(1 for pc in fw if fo[pc][1] != fw[pc][1]) >= 2)

    # ------------------------------------------------------------------ separation, input gates, distractors
    files = sorted(os.listdir(T))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check("S1 zero ask device rows in the call's population (no revoked status, no revocation, no fieldwork case "
          "among the granted initial claims it reads)", not [r for r in gi if r["res"] != "GRANTED"])
    check("I1 ten or more files in three or more formats", len(files) >= 10 and len(fmts) >= 3,
          "%d files %s" % (len(files), sorted(fmts)))
    check("I2 a file of 25,000 rows or more", len(pe_r) >= 25000 and len(rg_r) >= 25000, "persons %d, register %d" % (
        len(pe_r), len(rg_r)))
    check("I3 two or more distractors named in metadata.json", len(meta["distractor_files"]) >= 2 and all(
        f in files for f in meta["distractor_files"]), ", ".join(meta["distractor_files"]))
    tmp = tempfile.mkdtemp(prefix="t301_dx_")
    for f in files:
        if f not in meta["distractor_files"]:
            shutil.copy(os.path.join(T, f), tmp)
    G2 = AN.golden(tmp)
    check("I4 every distractor deleted: the call and every graded figure unchanged",
          G2["call"] == G["call"] and G2["A_by_prov_r"] == G["A_by_prov_r"] and G2["families"] == G["families"]
          and G2["fieldwork"] == G["fieldwork"])
    shutil.rmtree(tmp)
    check("I5 every file carries source, date and licence in metadata.json",
          all({"source", "date", "license"} <= set(f) for f in meta["files"]) and len(meta["files"]) == len(files))

    # ------------------------------------------------------------------ realism
    cells = [v for ym in fam for v in fam[ym].values()]
    check("Z1 realism: the 12 family counts are all different and none is a round hundred",
          len(set(cells)) == 12 and not any(v % 100 == 0 for v in cells))
    rates = [fw[pc][2] for pc in fw]
    check("Z2 realism: the three response rates differ", len(set(rates)) == 3, "%s" % rates)
    ok_order = True
    by_year = collections.defaultdict(list)
    for r in reg:
        if r["type"] in ("INITIAL", "RENEWAL", "CHANGE OF CLAIMANT") and r["claim"]:
            by_year[r["case"][4:8]].append((int(r["case"][-6:]), r["claim"]))
    for y, lst in by_year.items():
        lst = sorted(set(lst))
        if any(b[1] < a[1] for a, b in zip(lst, lst[1:])):
            ok_order = False
    check("Z3 realism: case numbers run in claim-date order within each year", ok_order)
    latest = max(r["dec"] or r["claim"] for r in reg)
    check("Z4 realism: nothing in the register after the pull (2 November 2026) and nothing after the as-of date",
          latest <= P.REGISTER_PULL, "latest %s" % latest)
    births = [int(r[pe_h.index("birth_year")]) for r in pe_r]
    earn_kids = sum(1 for r in pe_r if 2026 - int(r[pe_h.index("birth_year")]) < 18 and
                    IO.uncomma(r[pe_h.index("net_earnings_2025")] or "0"))
    check("Z5 realism: no child with earnings; birth years plausible", earn_kids == 0 and min(births) >= 1920)
    monthly = collections.Counter((r["claim"].year, r["claim"].month) for r in gi if r["claim"] >= F["rise_date"])
    check("Z6 realism: monthly initial claims vary (no constant stream)", len(set(monthly.values())) > 20)
    xl = IO.sheet_names(os.path.join(T, pack.FILES["incidents"]))
    import zipfile
    core = zipfile.ZipFile(os.path.join(T, pack.FILES["incidents"])).read("docProps/core.xml").decode("utf-8")
    gcore = zipfile.ZipFile(os.path.join(TASK_DIR, "golden", "appraisal_annex_2027.xlsx")).read(
        "docProps/core.xml").decode("utf-8")
    check("Z7 realism: the personas (guard names) appear only as document authors", "Diego Hervia" in core and
          "Guiomar Iñiguez" in gcore and "Hervia" not in docs_txt and "Iñiguez" not in docs_txt, ", ".join(xl))

    # ------------------------------------------------------------------ leaks, describing files, figures.json
    check("X1 leak: no file under target/ describes the data (readme, dictionary, notes, manifest)",
          not any(re.search(r"readme|dictionary|notes|manifest|codebook|schema", f, re.I) for f in files)
          and not any(re.search(r"notes|readme|dictionary", s, re.I) for s in xl))
    check("X2 leak: no file name names the device or the trap",
          not re.search(r"pace|cohort|revok|widen|first.?year|section|trap|take.?up", " ".join(files), re.I))
    check("X3 leak: no shipped document names the golden, the stump or the author's intent",
          not re.search(r"golden|stump|decoy|trap|intended", docs_txt, re.I))
    owed = [GD.fmt(G["A_total_r"])] + [GD.fmt(v) for v in G["A_by_prov_r"].values()]
    owed += [GD.fmt(v) for ym in fam for v in fam[ym].values()]
    owed += [GD.fmt(fw[pc][0]) for pc in fw] + [GD.fmt(fw[pc][1]) for pc in fw] + ["%.1f" % fw[pc][2] for pc in fw]
    check("X4 figures.json carries every graded figure", all(o in figs for o in owed))

    # ------------------------------------------------------------------ rounding edges
    edges = [edge(G["A_total"])] + [edge(v) for v in G["A_by_prov"].values()]
    check("E1 every graded children figure sits 10 or more from its rounding edge", min(edges) >= 10,
          "%s" % ", ".join("%.0f" % e for e in edges))
    redges = [0.05 - abs(fw[pc][3] - round(fw[pc][3], 1)) for pc in fw]
    check("E2 every response rate sits 0.01 points or more from its rounding edge", min(redges) >= 0.01,
          "%s" % ", ".join("%.4f" % fw[pc][3] for pc in fw))

    bad = [r for r in RESULTS if not r[1]]
    for label, ok, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    print("%d checks, %d failed" % (len(RESULTS), len(bad)))
    return 1 if bad else 0


# ---------------------------------------------------------------- the careful routes the ask devices are priced on
def ask1_cracker(target, mode="careful", revoked=False):
    """Ask 1 by a careful route: resolutions decided by 31 December 2025 whose decision reads GRANTED (or, with
    revoked=True, the golden's reading of REVOKED), each family once, in the province of its municipality, moves from
    the incident log the month after. mode varies one hazard's handling."""
    reg = AN.register(target)
    codes = AN.territorial(target)
    moves = collections.defaultdict(list)
    for r in AN.incidents(target):
        if r["type"] == "Change of address":
            moves[r["fam"]].append((r["date"], r["detail"]))
    out = {}
    for ym in AN.QUARTER_ENDS:
        m = AN.mi(ym)
        fams, rows = {}, collections.Counter()
        for r in reg:
            if r["type"] == "REVOCATION" or r["first"] is None or r["dec"] is None or r["dec"] > AN.CUTOFF:
                continue
            if r["res"] != "GRANTED" and not (revoked and r["res"] == "REVOKED"):
                continue
            if AN.mi(r["first"]) <= m and (r["last"] is None or AN.mi(r["last"]) >= m):
                prev = fams.get(r["fam"])
                if prev is None or r["dec"] > prev["dec"]:
                    fams[r["fam"]] = r
                rows[r["fam"]] += 1
        cnt = collections.Counter()
        for f, r in fams.items():
            if mode == "office":
                cnt[r["prov"]] += 1
                continue
            muni = r["muni"]
            if mode != "nomoves":
                for d, new in sorted(moves.get(f, [])):
                    if AN.mi((d.year, d.month)) + (0 if mode == "samemonth" else 1) <= m:
                        muni = new
            cnt[codes[muni]] += rows[f] if mode == "rows" else 1
        out[ym] = dict(cnt)
    return out


def ask2_cracker(target, mode="careful"):
    """Ask 2 by a careful route: each dwelling reference once at its last issue, in the province of its municipality
    (mode 'office' takes the office's province)."""
    h, rows = IO.read_csv(os.path.join(target, pack.FILES["fieldwork"]))
    ix = {k: i for i, k in enumerate(h)}
    codes = AN.territorial(target)
    office = {"VAL": "81", "CUE": "82", "SIE": "83"}
    last = {}
    for r in rows:
        key = r[ix["dwelling"]]
        iss = int(r[ix["issue"]])
        if key not in last or iss > last[key][0]:
            last[key] = (iss, r[ix["result"]], r[ix["office"]])
    out = {}
    for ref, (iss, res, off) in last.items():
        pc = office[off] if mode == "office" else codes[ref[:5]]
        e = out.setdefault(pc, [0, 0])
        if res not in AN.NOT_ELIGIBLE:
            e[0] += 1
            if res == "complete interview":
                e[1] += 1
    return {pc: (v[0], v[1], round(100.0 * v[1] / v[0], 1)) for pc, v in out.items()}


if __name__ == "__main__":
    sys.exit(main())
