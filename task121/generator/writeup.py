"""submission.md for task121, every figure read from generator/figures.json.

    python3 task121/generator/writeup.py"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def num(x):
    return x.replace("-", "−") if False else x


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    w, m, fe = f["walk"], f["model"], f["feeders"]
    names = [n.replace(" Primary School", "").replace(" Community Primary School", "").replace(" Primary Academy", "")
             for n in fe["names"]]
    names = [n.replace(" Community", "") for n in names]
    A, B = f["annex_a"], f["annex_b"]
    order = ["Halwick Academy", "Brantholme Park Academy", "Fernlea Academy", "Coldwell Academy", "Mossgate Academy",
             "Saltmoor Academy", "Ridley Hey Academy", "Wrayfield Academy"]
    lines = []
    lines += ["## Tags", "",
              "**Domain:** Education & Learning Sciences (multilevel school effects research).",
              "**Analytical objective:** Root-Cause Analysis.", ""]
    lines += ["## 1. Final Recommendation", "",
              "**No: Halwick Academy's own effect accounts for almost none of its Progress 8 gap to the Larkhollow trust "
              "average (%s of the %s gap, pupils finishing key stage 4 in 2022 to 2024). The largest item is the "
              "remainder, %s: what its pupils bring from the seven primary schools that send it %s%% of its intake. "
              "Point the 2027 plan at the pupils Halwick admits from those schools, not at Halwick's teaching.**"
              % (w["own"], w["gap"], w["rem"], fe["share_of_halwick"]),
              "Those primaries' pupils average %s at the borough's other secondaries, close to their %s at Halwick, "
              "while Halwick's pupils from every other school average %s against the trust's %s. Read alone, Progress "
              "8 and a model of pupils within secondaries put %s on the academy itself."
              % (fe["p8_elsewhere"], fe["p8_at_halwick"], fe["p8_others_at_halwick"], f["trust_p8"],
                 f["default_path"]["own"]), ""]
    lines += ["## 2. Critical Components", "",
              "1. The walk in Progress 8 points: gap **%s** (Halwick %s against the trust's %s) = attendance **%s** + "
              "disadvantage **%s** + the academy's own effect **%s** + the remainder **%s**."
              % (w["gap"], f["halwick_p8"], f["trust_p8"], w["att"], w["dis"], w["own"], w["rem"]),
              "2. The academy's own effect is measured with every pupil classified by the school where they sat key "
              "stage 2 as well as by their secondary (fixed effects for both, all %s borough pupils with a Progress 8 "
              "score), so the same primaries' pupils at other secondaries carry their own shortfall; a model of pupils "
              "within secondaries alone books **%s** to the academy." % (format(f["pupils"]["borough"], ","),
                                                                       f["default_path"]["own"]),
              "3. Behind the remainder: %s and %s send **%s%%** of Halwick's pupils; their pupils' Progress 8 is "
              "**%s** at the other secondaries and **%s** at Halwick; Halwick's pupils from every other school "
              "average **%s**." % (", ".join(names[:-1]), names[-1], fe["share_of_halwick"], fe["p8_elsewhere"],
                                   fe["p8_at_halwick"], fe["p8_others_at_halwick"]), ""]
    lines += ["## 3. Step-by-Step Solution", "",
              "1. Took Paper 6, section 3: the gap pooled over the trust's pupils with a Progress 8 score in 2022 to "
              "2024; attendance and disadvantage each an effect times Halwick's difference from the trust; the "
              "academy's own effect as the same pupils at the trust's average academy, weighted by the trust's pupils; "
              "the remainder; every effect measured on all the borough's pupils and unshrunk.",
              "2. From the transfer file: the absence rate as authorised plus unauthorised sessions over sessions "
              "possible in year 11; the disadvantaged flag; the key stage 2 school, a converted academy read through "
              "the establishment register's predecessor URN.",
              "3. Fitted Progress 8 on the absence rate and the disadvantaged flag with a fixed effect for each "
              "secondary and each key stage 2 school, by least squares on all %s pupils." % format(
                  f["pupils"]["borough"], ","),
              "4. Attendance: %s per point of absence times Halwick's %s against the trust's %s, %s; disadvantage: "
              "%s times %s%% against %s%%, %s; the academy's own effect, Halwick's effect less the trust's "
              "pupil-weighted average, %s; the remainder %s; the gap %s." % (
                  m["b_absence"], m["absence_halwick"], m["absence_trust"], m["walk_3dp"]["att"], m["b_disadvantaged"],
                  m["disadvantaged_halwick_pct"], m["disadvantaged_trust_pct"], m["walk_3dp"]["dis"],
                  m["walk_3dp"]["own"], m["walk_3dp"]["rem"], m["walk_3dp"]["gap"]),
              "5. Annex A: each half-term row placed at the academy whose roll the pupil was on (the movements log "
              "dates each move; the extract labels every row with the current academy), the 2025/26 year group as the "
              "extract's less one for pupils still on roll, year 11's summer rows out; per pupil and academy, absence "
              "of 10 per cent or more persistent, 50 per cent or more severe.",
              "6. Annex B: each 2026 pupil's summer 2026 results with their year 10 entries from the summer 2025 file; "
              "for English, maths and the EBacc subjects the first entry, otherwise the higher score in a discount "
              "code; Attainment 8 and EBacc entry by the measures summary.",
              "7. The largest item is the remainder; the academy's own effect is not the main reason.", ""]
    lines += ["## 4. Deliverable Answers", "", "### halwick_progress8_walk_2022_2024.xlsx", "",
              "1. Is the academy's own effect the main reason: no",
              "2. The walk (Progress 8 points): gap %s; attendance %s; disadvantage %s; the academy's own effect %s; "
              "the remainder %s" % (w["gap"], w["att"], w["dis"], w["own"], w["rem"]),
              "3. Largest item: the remainder, what Halwick's pupils bring from the seven primary schools that send it "
              "%s%% of its pupils" % fe["share_of_halwick"],
              "4. Annex A, 2025/26 (per cent), persistent absence and severe absence:"]
    for k in order:
        lines.append("   - %s: %s and %s" % (k, A[k]["pa"], A[k]["sa"]))
    lines.append("5. Annex B, 2026 cohort, average Attainment 8 and EBacc entry (per cent):")
    for k in order:
        lines.append("   - %s: %s and %s" % (k, B[k]["a8"], B[k]["ebacc"]))
    lines += ["", "### halwick_progress8_walk.png", "",
              "1. The walk from the trust average (%s) to Halwick (%s): attendance %s, disadvantage %s, the academy's "
              "own effect %s, the remainder %s." % (f["trust_p8"], f["halwick_p8"], w["att"], w["dis"], w["own"],
                                                   w["rem"]), ""]
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(lines))


if __name__ == "__main__":
    main()
