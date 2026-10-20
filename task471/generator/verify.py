"""Independent verifier: reads only the shipped bundle with its own readers (the csv module and openpyxl), rebuilds the
anchor, the WA2 validity shift, Tucker, chained linear and chained equipercentile equating with its own code, the
Form 26A passing score, every program's completers counted, passers and rate, and the 2024-25 ask, and checks the
golden workbook, figures.json and submission.md against them, each figure at the precision the prompt asks for."""
import csv
import datetime as dt
import json
import os
import re

import numpy as np

FILES = dict(maps="ELI_item_maps_25A_26A.xlsx", conv="ELI_Form25A_raw_to_scale.csv",
             s25="pellmore_ELI_June2025_scores.csv", s26="arcwright_ELI_June2026_scores.csv",
             items26="arcwright_ELI_June2026_item_responses.csv", reads26="arcwright_ELI_June2026_written_assignment_reads.csv",
             qc26="arcwright_ELI_June2026_scoring_QC.xlsx", history="BESL_ELI_attempt_history_2019-2026.csv",
             crosswalk="BESL_arcwright_registration_crosswalk_2026.csv", completers="EPP_Title_II_completers_2025-26.xlsx",
             register="BESL_completer_register_2019-20_to_2024-25.csv", directory="BESL_EPP_directory_2026.csv")
WORKBOOK = "eli_2027_program_review.xlsx"
JUNE25, JUNE26 = "2025-06-14", "2026-06-13"
YEAR = (dt.date(2025, 7, 1), dt.date(2026, 6, 30))


def rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def key(s):
    return "".join(ch for ch in str(s or "").upper() if "A" <= ch <= "Z")


def day(s):
    s = str(s).strip()
    for f in ("%Y-%m-%d", "%m/%d/%Y", "%B %d, %Y"):
        try:
            return dt.datetime.strptime(s, f).date()
        except ValueError:
            continue
    raise ValueError(s)


def half_up(v):
    return int(np.floor(v + 0.5))


def rate(p, n):
    return float(np.floor(1000.0 * p / n + 0.5) / 10.0)


# ------------------------------------------------------------------------------------------------ equating, own code
def tucker(X, VX, Y, VY):
    w1 = len(X) / (len(X) + len(Y))
    w2 = 1 - w1
    g1 = np.cov(X, VX, bias=True)[0, 1] / np.var(VX)
    g2 = np.cov(Y, VY, bias=True)[0, 1] / np.var(VY)
    dm, dv = VX.mean() - VY.mean(), np.var(VX) - np.var(VY)
    mx = X.mean() - w2 * g1 * dm
    my = Y.mean() + w1 * g2 * dm
    vx = np.var(X) - w2 * g1 ** 2 * dv + w1 * w2 * g1 ** 2 * dm ** 2
    vy = np.var(Y) + w1 * g2 ** 2 * dv + w1 * w2 * g2 ** 2 * dm ** 2
    return lambda x: my + np.sqrt(vy / vx) * (x - mx)


def chained_linear(X, VX, Y, VY):
    return lambda x: Y.mean() + Y.std() / VY.std() * (VX.mean() + VX.std() / X.std() * (x - X.mean()) - VY.mean())


def _pr(vals, top):
    f = np.bincount(vals.astype(int), minlength=top + 1)[:top + 1] / len(vals)
    F = np.cumsum(f)

    def P(x):
        s = int(np.clip(np.floor(x + 0.5), 0, top))
        return (F[s - 1] if s > 0 else 0.0) + (x - s + 0.5) * f[s]

    def Pinv(p):
        s = int(np.searchsorted(F, p, side="right"))
        s = min(s, top)
        return (p - (F[s - 1] if s > 0 else 0.0)) / f[s] + s - 0.5
    return P, Pinv


def chained_equipercentile(X, VX, Y, VY, shift):
    Px, _ = _pr(X, 108)
    _, Qv1 = _pr(VX, 36)
    Pv2, _ = _pr(VY, 36)
    _, Qy = _pr(Y, 108)
    return lambda x: Qy(Pv2(Qv1(Px(x)) + shift))


def lowest_passing(e, target):
    return min(x for x in range(109) if half_up(e(x)) >= target)


# ------------------------------------------------------------------------------------------------------- the check
def main(target, golden):
    import openpyxl
    t = lambda k: os.path.join(target, FILES[k])
    ok = True

    def say(label, cond, extra=""):
        nonlocal ok
        ok &= bool(cond)
        print("verify %s  %s%s" % ("ok  " if cond else "FAIL", label, ("  [%s]" % extra) if extra else ""))

    task = os.path.dirname(os.path.abspath(target))
    fig = json.load(open(os.path.join(task, "generator", "figures.json"), encoding="utf-8"))

    # the forms: shared items by identifier, the shared written assignment
    wb = openpyxl.load_workbook(t("maps"), read_only=True)
    mc, wa = {}, {}
    for form in ("25A", "26A"):
        body = list(wb["Form %s" % form].iter_rows(min_row=2, values_only=True))
        mc[form] = {r[1]: int(r[0]) for r in body if r[2] == "Multiple choice"}
        wa[form] = [r[1] for r in body if r[2] == "Written assignment"]
    shared = set(mc["25A"]) & set(mc["26A"])
    swa = [wa["26A"].index(w) for w in wa["26A"] if w in wa["25A"]]
    say("20 shared items and one shared assignment", len(shared) == 20 and len(swa) == 1, "WA%d" % (swa[0] + 1))
    k = swa[0] + 1
    pos25 = sorted(mc["25A"][i] for i in shared)

    # first attempts from the history, voided attempts left out
    hist, who = {}, {}
    for r in rows(t("history")):
        if r["RESULT"] == "VOID":
            continue
        hist.setdefault(r["EDUCATOR_ID"], []).append((r["TEST_DATE"], r["RESULT"]))
        who[r["EDUCATOR_ID"]] = (key(r["LAST_NAME"]), key(r["FIRST_NAME"]), day(r["BIRTH_DATE"]))
    first = {e: min(v) for e, v in hist.items()}

    Y, VY = [], []
    for r in rows(t("s25")):
        if first.get(r["CAND_ID"], ("",))[0] != JUNE25:
            continue
        w2 = 2 * int(r["WA%d_R3" % k]) if r["WA%d_R3" % k] else int(r["WA%d_R1" % k]) + int(r["WA%d_R2" % k])
        Y.append(int(r["TOTAL_RAW"]))
        VY.append(sum(int(r["ITEM_SCORES"][p - 1]) for p in pos25) + 2 * w2)
    cw = {r["REG_ID"]: r["EDUCATOR_ID"] for r in rows(t("crosswalk"))}
    anchor = {}
    for r in rows(t("items26")):
        if r["ITEM_ID"] in shared:
            anchor[r["REG_ID"]] = anchor.get(r["REG_ID"], 0) + int(r["ITEM_SCORE"])
    X, VX, raw26 = [], [], {}
    for r in rows(t("s26")):
        e = cw[r["REG_ID"]]
        raw26[e] = int(r["RAW_TOTAL"])
        if first.get(e, ("",))[0] != JUNE26:
            continue
        X.append(int(r["RAW_TOTAL"]))
        VX.append(anchor[r["REG_ID"]] + 2 * int(r["WA%d_SCORE" % k]))
    X, VX, Y, VY = (np.array(a, float) for a in (X, VX, Y, VY))
    say("first-attempt samples", (len(Y), len(X)) == (fig["n_first_2025"], fig["n_first_2026"]), "%d and %d" % (len(Y), len(X)))

    # WA2 on the 2025 standard: the validity papers from the 2025 scoring
    qc = openpyxl.load_workbook(t("qc26"), read_only=True)
    papers = {r[0]: int(r[3]) for r in qc["Validity papers"].iter_rows(min_row=2, values_only=True)
              if r[1] == "WA%d" % k and "2025" in str(r[2])}
    d = [int(r["SCORE"]) - papers[r["RESPONSE_ID"]] for r in rows(t("reads26"))
         if r["READ_TYPE"] == "VALIDITY" and r["RESPONSE_ID"] in papers]
    bias = float(np.mean(d))
    shift = -2 * 2 * bias
    say("WA2 validity shift", abs(bias - fig["validity_bias"]) < 5e-5 and abs(shift - fig["anchor_shift"]) < 0.005
        and len(papers) == fig["wa2_papers"] and len(d) == fig["wa2_validity_reads"], "%.4f per read, %.2f" % (bias, shift))

    conv = {int(r["RAW_SCORE"]): int(r["SCALE_SCORE"]) for r in rows(t("conv"))}
    pass25 = min(v for v, s in conv.items() if s >= 240)
    cuts = {"Tucker": lowest_passing(tucker(X, VX + shift, Y, VY), pass25),
            "chained linear": lowest_passing(chained_linear(X, VX + shift, Y, VY), pass25),
            "chained equipercentile": lowest_passing(chained_equipercentile(X, VX, Y, VY, shift), pass25)}
    say("Form 26A raw passing score", set(cuts.values()) == {fig["raw_cut"]}, str(cuts))
    naive = {"Tucker": lowest_passing(tucker(X, VX, Y, VY), pass25),
             "chained equipercentile": lowest_passing(chained_equipercentile(X, VX, Y, VY, 0.0), pass25)}
    say("the anchor as scored files another score", fig["raw_cut"] not in naive.values(), str(naive))
    cut = fig["raw_cut"]

    # completers counted, passers and rates
    lists = openpyxl.load_workbook(t("completers"), read_only=True)
    names = {r["PROGRAM_CODE"]: r["PROGRAM_NAME"] for r in rows(t("directory"))}
    mine = {}
    for code in lists.sheetnames:
        body = list(lists[code].iter_rows(values_only=True))
        head = list(body[4])
        ids = []
        for r in body[5:]:
            if not r or r[0] is None:
                continue
            d_ = dict(zip(head, r))
            if "Educator ID" in d_:
                e, area, done = d_["Educator ID"], d_["Pathway"], d_["Completion Date"]
            elif "STATE ID" in d_:
                e, area, done = "E" + str(d_["STATE ID"]).zfill(7), d_["PROGRAM AREA"], d_["DATE COMPLETED"]
            else:
                e, area, done = "E" + re.sub(r"\D", "", str(d_["Educator #"])).zfill(7), d_["Licensure Area"], d_["Residency Exit"]
            if not str(area).upper().startswith("ELEM") or not YEAR[0] <= day(done) <= YEAR[1] or e in ids:
                continue
            ids.append(e)
        mine[code] = ids
    got = {}
    for code, ids in mine.items():
        n = p = 0
        for e in ids:
            if e not in first or first[e][0] > JUNE26:
                continue
            n += 1
            p += int(raw26[e] >= cut) if first[e][0] == JUNE26 else int(first[e][1] == "PASS")
        got[code] = (n, p)
    figp = {q["code"]: q for q in fig["programs"]}
    say("sixteen programs", set(got) == set(figp) and all(names[c] == figp[c]["name"] for c in got))
    say("completers counted and passers", all(got[c] == (figp[c]["counted"], figp[c]["passed"]) for c in got),
        str({c: got[c] for c in got if got[c] != (figp[c]["counted"], figp[c]["passed"])}))
    say("rates", all(rate(got[c][1], got[c][0]) == figp[c]["rate"] for c in got))
    review = sorted(names[c] for c, (n, p) in got.items() if p / n < 0.70)
    say("programs on review", review == sorted(fig["review"]), "; ".join(review))
    edge = min(abs(p - 0.7 * n) for n, p in got.values())
    say("no program within one completer of the line", edge >= 1.0, "%.1f" % edge)

    # the ask: the 2024-25 completers in the register, by educator ID, else by name and birth date
    by_name = {}
    for e, nm in who.items():
        by_name.setdefault(nm, []).append(e)
    prior = {c: [0, 0] for c in got}
    for r in rows(t("register")):
        if r["PROGRAM_YEAR"] != "2024-25" or not r["PATHWAY"].upper().startswith("ELEM") or r["PROGRAM_CODE"] not in prior:
            continue
        e = r["EDUCATOR_ID"]
        if e not in hist:
            c_ = by_name.get((key(r["LAST_NAME"]), key(r["FIRST_NAME"]), day(r["BIRTH_DATE"])), [])
            e = c_[0] if len(c_) == 1 else e
        if e not in first or first[e][0] > JUNE25:
            continue
        prior[r["PROGRAM_CODE"]][0] += 1
        prior[r["PROGRAM_CODE"]][1] += int(first[e][1] == "PASS")
    say("2024-25 completers tested and their rate", all(prior[c][0] == figp[c]["prior_tested"] and
                                                         rate(prior[c][1], prior[c][0]) == figp[c]["prior_rate"]
                                                         for c in prior))

    # the golden workbook and the write-up
    gw = openpyxl.load_workbook(os.path.join(golden, WORKBOOK), data_only=True)
    rv = {r[0]: r for r in gw["Reviews 2027"].iter_rows(min_row=5, values_only=True) if r[0] in got}
    say("workbook review sheet", all(rv[c][2:6] == (got[c][0], got[c][1], rate(got[c][1], got[c][0]),
                                                    "Yes" if names[c] in review else "No") for c in got))
    say("workbook passing score", str(cut) in str(gw["Reviews 2027"]["A2"].value))
    pr = {r[0]: r for r in gw["2024-25 completers"].iter_rows(min_row=2, values_only=True)}
    say("workbook 2024-25 sheet", all(pr[c][2] == prior[c][0] and pr[c][4] == rate(prior[c][1], prior[c][0])
                                      for c in prior))
    sub = open(os.path.join(task, "submission.md"), encoding="utf-8").read()
    blk = sub[sub.index("## 4. Deliverable Answers"):]
    lines_ok = True
    for c in got:
        n, p = got[c]
        lines_ok &= ("   - %s: %d completers, %d passed, %.1f\n" % (names[c], n, p, rate(p, n))) in blk
        lines_ok &= ("   - %s: %d completers, %.1f\n" % (names[c], prior[c][0], rate(prior[c][1], prior[c][0]))) in blk
    say("write-up block 4: counts whole, rates to one decimal", lines_ok)
    say("write-up passing score", "Form 26A raw passing score: **%d**." % cut in blk)
    print("verify: %s" % ("all checks pass" if ok else "FAILED"))
    return ok


if __name__ == "__main__":
    import sys
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raise SystemExit(0 if main(os.path.join(here, "target"), os.path.join(here, "golden")) else 1)
