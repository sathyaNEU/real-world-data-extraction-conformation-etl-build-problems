"""task170 checks: the generator's assertions on the built pack (and on the clean truth where a rule says so).

    python3 task170/generator/checks.py task170/target

Every label is printed with PASS or FAIL; exit 1 on any FAIL. Labels R1 to R3c are the client's three rules
(dataset-generation 7.1); SFn are the design note's semantic fork rows."""
from __future__ import annotations

import json
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc  # noqa: E402
import common as C  # noqa: E402
import docs as DOCS  # noqa: E402
import pack as PK  # noqa: E402
import world as W  # noqa: E402

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", label, detail))


def rnd(v, unit):
    return int(round(v / float(unit))) * unit


def edge(v, unit):
    return unit / 2.0 - abs(v - rnd(v, unit))


def same_bins(F, G):
    """Every graded figure of the call rounds the same under F as under the golden G."""
    ok = rnd(F["total"], 500000) == rnd(G["total"], 500000) and rnd(F["heads_total"], 100) == rnd(G["heads_total"], 100)
    return ok and all(rnd(F["by"][h], 100000) == rnd(G["by"][h], 100000) for h in C.H_CODES)


def clean_truth_curves():
    """The world's own laws, no records: the join and cover curves, staying on the payroll and the match on a
    joiner's rate."""
    k = np.arange(1, calc.K + 1)
    chosen = W.INDUCTION + (1 - W.INDUCTION) * (1 - np.exp(-k / W.PACE))       # P(choice applies by month k)
    stay = W.EARLY_LEAVERS * np.exp(-(k - 1) / W.EARLY_MEAN) + (1 - W.EARLY_LEAVERS) * np.exp(-(k - 1) / W.STAY_MEAN)
    mb = float(sum(C.match_pct(r) * w for r, w in zip(W.RATES, W.RATE_W))) / 100
    return dict(C=W.P_SAVE * chosen, p=W.P_SAVE * float(chosen[-1]), G=W.Q_DROP * chosen, q=W.Q_DROP * float(chosen[-1]),
                Se=stay, mb=mb)


def text_of_pack(target):
    out = {}
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith((".csv", ".txt")):
            out[f] = open(p, encoding="utf-8").read()[:400000]
        elif f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(p) as z:
                out[f] = " ".join(z.read(n).decode("utf-8", "replace") for n in z.namelist() if n.endswith(".xml"))
        elif f.endswith(".pdf"):
            from pypdf import PdfReader
            out[f] = " ".join(pg.extract_text() for pg in PdfReader(p).pages)
    return out


def main(target):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    G = calc.golden(target)
    cv, P = G["cv"], G["P"]

    # ------------------------------------------------------------------ the call and its bins
    check("call figure", F["call_match_fy2027_tnk"] == rnd(G["total"], 500000), "%.0f" % G["total"])
    check("call mid-bin", edge(G["total"], 500000) >= 0.01 * G["total"], "edge %.0f" % edge(G["total"], 500000))
    for h in C.H_CODES:
        v = G["by"][h]
        check("hospital %s figure and mid-bin" % h, F["call_match_fy2027_%s" % h] == rnd(v, 100000) and
              edge(v, 100000) >= 0.006 * v, "%.0f edge %.0f" % (v, edge(v, 100000)))
    check("December contributors mid-bin", edge(G["heads_total"], 100) >= 15, "%.1f" % G["heads_total"])
    check("components mid-bin", edge(100 * cv["p"], 1) >= 0.15 and edge(100 * G["chosen"][12], 1) >= 0.25,
          "prefer %.2f, chosen by the twelfth payroll %.2f" % (100 * cv["p"], 100 * G["chosen"][12]))

    # ------------------------------------------------------------------ the golden family
    h = cv["hires"]
    jm, rate = calc.joins(target, h)
    f = np.array(h["f"])
    lk = np.array([x if x is not None else 10 ** 6 for x in h["left_k"]])
    jk = np.array([(jm[i] - s + 1) if i in jm else 10 ** 6 for i, s in enumerate(h["s"])])
    Ccc = np.array([((jk <= k) & (f >= k) & (lk >= k)).sum() / max(((f >= k) & (lk >= k)).sum(), 1)
                    for k in range(1, calc.K + 1)])
    Secc = np.array([(lk >= k)[(f >= k) | (lk < k)].mean() for k in range(1, calc.K + 1)])
    fam = {}
    for Kp in (36, 48, 72, 84):
        fam["SF8 plateau read at %d months" % Kp] = dict(p=float(cv["C"][Kp - 1]))
    fam["SF8 plateau read at the curve's end"] = dict(p=float(cv["C"][-1]))
    fam["SF9 complete cohorts for the join curve"] = dict(C=Ccc, p=float(Ccc[calc.PLATEAU - 1]))
    fam["SF9 complete cohorts for staying on the payroll"] = dict(Se=Secc)
    fam["SF9 complete cohorts for both"] = dict(C=Ccc, p=float(Ccc[calc.PLATEAU - 1]), Se=Secc)
    reg = pd.read_excel(os.path.join(target, PK.F_REG), dtype={"employer_ref": str})
    cur = dict(zip(zip(reg["employer_ref"], pd.to_datetime(reg["joined"]).dt.date), reg["current_rate_pct"]))
    w_pay = [C.SCALE_2027[h["grade"][i]] * float(h["fte"][i]) for i in rate]
    fam["SF11 pay-weighted match on joiners' rates"] = dict(mb=float(np.average([C.match_pct(r) for r in rate.values()],
                                                                                 weights=w_pay)) / 100)
    fam["SF11 current rates for joiners"] = dict(mb=float(np.mean([C.match_pct(r) for r in reg["current_rate_pct"]])) / 100)
    for name, kw in fam.items():
        c = dict(cv)
        c.update(kw)
        Fv = calc.forecast(target, c, "golden", P)
        check(name, same_bins(Fv, G), "%.0f (%+.2f%%)" % (Fv["total"], 100 * (Fv["total"] / G["total"] - 1)))
    Fi = calc.forecast(target, cv, "ipc_clock", P)
    check("SF10 the clock read from the cover's cancellations", same_bins(Fi, G),
          "%.0f (%+.2f%%), chosen by the twelfth payroll %.1f" % (Fi["total"], 100 * (Fi["total"] / G["total"] - 1),
                                                                 100 * cv["G"][11] / cv["q"]))
    check("SF10 the cover's clock gives the same components", int(round(100 * cv["G"][11] / cv["q"])) ==
          F["component_chosen_by_12th_payroll_pct"], "%.2f" % (100 * cv["G"][11] / cv["q"]))
    # SF7: a choice dated by calendar months from the start date rather than by the payroll it applies to
    check("SF7 the payroll a choice applies to", True, "joins are dated by their first contribution's payroll; the cover "
          "by the cut-off rule, asserted under SF10")
    # SF12: rehires as their own hires, or first spells only
    first_only = h[h["spell"] == "1"].reset_index(drop=True)
    jm1, rate1 = calc.joins(target, first_only)
    jk1 = [(jm1[i] - s + 1) if i in jm1 else None for i, s in enumerate(first_only["s"])]
    c1 = dict(cv)
    c1["C"] = calc.km_incidence(jk1, first_only["f"])
    c1["p"] = float(c1["C"][calc.PLATEAU - 1])
    c1["Se"] = calc.on_payroll(first_only)
    F1 = calc.forecast(target, c1, "golden", P)
    check("SF12 first spells only", same_bins(F1, G), "%.0f" % F1["total"])
    # SF6: each hospital from its own hires moves hospital figures (closed by the amendment's sentence)
    check("SF6 the amendment pools the hospitals", "all six hospitals taken together" in DOCS.AMEND[3][1], "section 4")
    check("SF1 the intake is the approved requisitions", "the approved requisitions in the 2027 hiring plan" in DOCS.AMEND[3][1],
          "%d requisitions" % len(P))
    check("SF2 FY2027 is the January to December 2027 payrolls", "(the January to December 2027 payrolls)" in DOCS.AMEND[3][1])
    check("SF3 the 2027 scale for every 2027 payroll", "The 2027 scale applies to every payroll from January to December "
          "2027." in open(os.path.join(HERE, "docs.py")).read())
    check("SF4 enrolment at 3 per cent from the first payroll", "at a contribution of 3 per cent of basic pay from the first "
          "payroll" in DOCS.AMEND[2][1])
    check("SF5 the match formula is the rules' section 4", "100 per cent of the member's contribution up to 3 per cent"
          in DOCS.RULES[3][1][0])
    check("SF13 contributing on the December payroll counts the default and chosen rates", True,
          "heads = not yet chosen plus joined at own rate: %.0f of %.0f" % (G["heads_total"], G["staff_total"]))
    check("SF14 the forecast counts nobody hired before 2027", "counts nobody hired before 2027" in DOCS.AMEND[3][1])

    # ------------------------------------------------------------------ the ladder: every rung in its own bin
    rungs = {"R0 the cover's cancellations as the plan's opt-outs": "ipc_carry",
             "R1 the same with joiners at their own rates": "ipc_carry_joiners",
             "R2 the join curve read as the share who have chosen": "joined_as_chosen",
             "R3 nobody opts out": "nobody_leaves",
             "R4 only those who prefer to save, from the first payroll": "preference",
             "R5 those who prefer to save, at 3 per cent": "preference_default",
             "R6 the opt-in record replayed": "opt_in"}
    lad = {}
    for name, mode in rungs.items():
        Fr = calc.forecast(target, cv, mode, P)
        lad[name] = Fr["total"]
        check("ladder %s off the golden's bin" % name, rnd(Fr["total"], 500000) != rnd(G["total"], 500000) and
              abs(Fr["total"] / G["total"] - 1) > 0.15, "%.0f (%+.1f%%)" % (Fr["total"], 100 * (Fr["total"] / G["total"] - 1)))
    check("default path's figure", rnd(lad["R0 the cover's cancellations as the plan's opt-outs"], 500000) ==
          F["rival_cover_carry_tnk"], str(F["rival_cover_carry_tnk"]))

    # ------------------------------------------------------------------ the three rules
    T = clean_truth_curves()
    Fa = calc.forecast(target, T, "ipc_carry", P)
    Fb = calc.forecast(target, T, "golden", P)
    Fc = calc.forecast(target, T, "joined_as_chosen", P)
    check("R3a the analyst test on the clean truth files the wrong answer", rnd(Fa["total"], 500000) != rnd(G["total"], 500000),
          "%.0f" % Fa["total"])
    check("R3b the decisive step alone files the golden on the clean truth", rnd(Fb["total"], 500000) ==
          rnd(G["total"], 500000), "%.0f" % Fb["total"])
    check("R3b the lower rung alone stays wrong on the clean truth", rnd(Fc["total"], 500000) != rnd(G["total"], 500000),
          "%.0f" % Fc["total"])
    texts = text_of_pack(target)
    check("R1 the field's raw material ships", os.path.getsize(os.path.join(target, PK.F_HR)) > 10 ** 6 and
          os.path.getsize(os.path.join(target, PK.F_IPC)) > 10 ** 6, "HR history and the bordereau at record grain")
    bad = [f for f, t in texts.items() if re.search(r"opt[- ]out rate|participation rate|take-up|inertia|procrastinat|"
                                                    r"per cent of (new )?hires (join|opt)|join curve|default effect", t, re.I)]
    check("R1 no shipped sentence states a join curve, a take-up or an opt-out rate", not bad, ", ".join(bad) or "none")
    nums = re.findall(r"\b4[0-9]\.[0-9] per cent|\b7[0-9] per cent", " ".join(texts.values()))
    check("R1 no shipped figure states the five-year join share or the share chosen", not nums, ", ".join(nums) or "none")
    # R2: the Layer 1 mess on the call's path is neutral
    hr = calc.hires(target)
    idm = calc.id_map(hr)
    refs = list(reg["employer_ref"])
    check("R2 every register reference maps through one of the two employee numbers", all(r in idm for r in refs),
          "%d memberships, %d V-numbers" % (len(refs), sum(r.startswith("V") for r in refs)))
    ipc = pd.read_csv(os.path.join(target, PK.F_IPC), dtype=str, keep_default_na=False)
    check("R2 every bordereau reference maps", all(r in idm for r in ipc["employer_ref"]), "%d policies" % len(ipc))
    E_only = {e: e for e in hr["employee_no"]}
    lost = sum(1 for r in refs if r not in E_only)
    check("R2 joining on E-numbers alone loses most joins (loud, not silent)", lost > 0.5 * len(refs), "%d lost" % lost)
    lrc = (hr["hospital"] == "LRC").sum()
    check("R2 LRC spells sit outside the 2027 plan and pool with the rest", lrc > 0 and "LRC" not in set(P["hospital"]),
          "%d LRC spells" % lrc)
    # R3c no plant
    check("R3c no repeated spell in the HR history", not hr.duplicated(["employee_no", "spell"]).any(), "%d rows" % len(hr))
    check("R3c no repeated membership", not reg.duplicated(["member_no", "membership"]).any(), "%d rows" % len(reg))
    check("R3c no shipped document carries a method for the FY2027 line", not re.search(
        r"forecast (?:is|should be) (?:made|built)|multiply|curve|clock", DOCS.AMEND[3][1], re.I))

    # ------------------------------------------------------------------ the asks and the separation line
    ded = calc.deductions(target)
    paid = calc.match_paid_2026(target, "golden", ded)
    for h_ in C.H_CODES:
        check("ask A %s figure" % h_, F["ask_match_paid_2026_%s" % h_] == rnd(paid[h_], 1000), "%.2f" % paid[h_])
    alt = calc.match_paid_2026(target, "lines", ded)
    hit = [h_ for h_ in C.H_CODES if rnd(alt[h_], 1000) == F["ask_match_paid_2026_%s" % h_]]
    check("ask A every ERM line summed misses every hospital", not hit, ", ".join(hit) or "none")
    alt = calc.match_paid_2026(target, "no_negatives", ded)
    check("ask A the reversal lines dropped misses Rendholm", rnd(alt["RDH"], 1000) != F["ask_match_paid_2026_RDH"],
          "%.0f" % alt["RDH"])
    alt = calc.match_paid_2026(target, "main_only", ded)
    hit = [h_ for h_ in C.H_CODES if rnd(alt[h_], 1000) == F["ask_match_paid_2026_%s" % h_]]
    check("ask A the first run alone misses Rendholm", "RDH" not in hit, ", ".join(hit))
    mem = calc.members_pre2019(target, "golden", ded)
    for h_ in C.H_CODES:
        check("ask B %s figure" % h_, F["ask_members_pre2019_%s" % h_] == mem[h_], str(mem[h_]))
    alt = calc.members_pre2019(target, "register", ded)
    hit = [h_ for h_ in C.H_CODES if alt[h_] == mem[h_]]
    check("ask B the register's Active rows miss every hospital", not hit, ", ".join(hit) or "none")
    multi = ded[(ded["code"] == "ERM") & (ded["assignment"] == "2")]
    check("separation: the call reads no deduction line", "deductions" not in open(os.path.join(HERE, "calc.py")).read()
          .split("# ------------------------------------------------------------------------------------------------"
                 "---- the asks")[0], "%d bank-post ERM lines" % len(multi))
    pre = reg[pd.to_datetime(reg["joined"]).dt.date < C.D(2019, 1, 1)]
    hE = cv["hires"]
    by_emp = {}
    for idx, (emp, s0, e0) in enumerate(zip(hE["employee_no"], hE["s"], hE["e"])):
        by_emp.setdefault(emp, []).append((s0, None if e0 is None else int(e0), idx))
    inside = sum(1 for r, j in zip(pre["employer_ref"], pre["joined"])
                 if calc.spell_of(by_emp, idm[r], calc.mi(pd.Timestamp(j).date())) is not None)
    check("separation: ask B's memberships are none of the call's joins", inside == 0,
          "%d memberships opened before 2019, %d on a 2019 to 2026 hire" % (len(pre), inside))

    # ------------------------------------------------------------------ the realism sweep
    plan_x = pd.read_excel(os.path.join(target, PK.F_PLAN), sheet_name="Requisitions")
    dup = {f: int(df.duplicated().sum()) for f, df in ((PK.F_HR, hr), (PK.F_REG, reg), (PK.F_IPC, ipc), (PK.F_PLAN, plan_x))}
    check("realism: no repeated row in the HR history, register, bordereau or plan", not any(dup.values()), str(dup))
    hm = hr[hr["s"] >= C.mindex(C.HIST_START)].groupby(["hospital", "s"]).size()
    flat = [h_ for h_ in C.H_CODES if hm.loc[h_].nunique() < 5]
    check("realism: monthly hires vary in every hospital", not flat, "%d hospital-months" % len(hm))
    by_m = ded[ded["code"] == "ERM"].groupby("payroll")["amount"].apply(lambda x: round(x.astype(float).sum()))
    check("realism: no two payrolls carry the same match total", by_m.is_unique, "%d payrolls" % len(by_m))
    check("realism: no round headline", G["total"] % 1000 > 1 and all(v % 100 > 0.5 for v in G["by"].values()),
          "%.0f" % G["total"])
    names = set(re.findall(r"\b(?:Caroline|Erik|Alfred|Kristina|Angelica)\s+[A-Z][a-z]+", " ".join(texts.values())))
    check("realism: the pack names only the card's people", names <= {"Caroline Hagman", "Erik Palm", "Alfred Sundberg"},
          ", ".join(sorted(names)) or "none")

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    check("input gate: ten or more files", len(files) >= 10, str(len(files)))
    check("input gate: three or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3,
          ", ".join(sorted({f.rsplit(".", 1)[1] for f in files})))
    nded = sum(1 for _ in open(os.path.join(target, PK.F_DED))) - 1
    check("input gate: a file of 25,000 rows or more", nded >= 25000, "%d deduction lines" % nded)
    fails = [r for r in RESULTS if not r[1]]
    print("\n%d checks, %d failed" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else C.TARGET))
