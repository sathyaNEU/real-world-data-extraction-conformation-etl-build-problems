"""task445 architecture 3: submission.md and metadata.json, every figure from figures.json and the golden run."""
import json

import golden as G
import pack as PK

RNAME = {"NT": "Northern Territory", "QT": "Queensland and Torres Strait", "WA": "Western Australia",
         "PC": "Pacific", "ID": "Indonesia and Timor-Leste", "MS": "Malaysia and Singapore"}
MNAME = {"2025-12": "December 2025", "2026-01": "January 2026", "2026-02": "February 2026"}


def t(x):
    return "{:,}".format(x)


def submission(fig, S, path):
    d = fig["demand_1dp"]
    g = fig["grades"]
    r6 = fig["call"]["raise_marks"]
    rung = max(S["rungs"][h]["6"] for h in S["rungs"])
    gl = ", ".join("%s **%s**" % (k, t(g[k])) for k in ["A", "B", "C", "D", "E", "U"])
    gp = ", ".join("%s %s" % (k, t(g[k])) for k in ["A", "B", "C", "D", "E", "U"])
    L = ["## Tags", "",
         "**Domain:** Education & Learning Sciences (item response theory and test equating: optional essay questions "
         "on a senior-certificate History paper).",
         "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
         "## 1. Final Recommendation", "",
         "**Scale Question 6 of the 2026 History Paper 2: raise every candidate's mark on it by %d marks before the "
         "best two essays are credited and the grade boundaries are applied.**" % r6,
         "For the %s candidates who wrote all three essays, Question 6 was more demanding than Questions 4 and 5 "
         "taken together by %d marks to the nearest whole mark, over the code's 1.5; read from the candidates who "
         "chose it, it looks only about half a mark harder, because those who chose it knew its topic. Questions 4 "
         "and 5 are not more demanding and are not changed." % (t(fig["all_three_candidates"]), r6), "",
         "## 2. Critical Components", "",
         "1. Question 6's demand against Questions 4 and 5 taken together, from the candidates who wrote all three "
         "essays: **%d marks** to the nearest whole mark, over the 1.5 line; Questions 4 and 5 are less demanding "
         "than the others." % r6,
         "2. The candidates who chose Question 6 knew its topic: their question means, a Section A adjustment and "
         "each two-essay candidate's own pair all put it under the 1.5 line, so every chooser route files no "
         "scaling.",
         "3. Grades after Question 6 is raised by %d: %s, of **%s** candidates graded; **%s** grades change." % (
             r6, gl, t(fig["candidates_graded"]), t(fig["grade_changed"])), "",
         "## 3. Step-by-Step Solution", "",
         "1. Conformed the marking export to one final mark per candidate and essay (a senior examiner's re-mark "
         "stands, code 3.1), with absent candidates set aside (code 2.3).",
         "2. Placed every script's centre in its region through the centres register, the merged Queensland centres "
         "under the codes they held before the merger (code 2.1).",
         "3. Took the candidates who wrote all three essays (each essay marked, code 3.2) and, for each question, "
         "averaged each candidate's mean mark on the other two less their mark on it: Question 6 over 1.5, Questions "
         "4 and 5 below zero.",
         "4. Raised every Question 6 mark by %d (its demand to the nearest whole mark, over 1.5, no mark above 25), "
         "credited each candidate's best two essays, added Section A and applied the committee's boundaries." % r6,
         "5. Counted each region's candidates who sat and each optional question's answers, credited or not, from "
         "the conformed marks.",
         "6. Placed each 2025 review request in its centre's local month, Paper 2 only, withdrawn requests out, "
         "grade changes by outcome GC (code 6.2 and 6.3).", "",
         "## 4. Deliverable Answers", "", "### p2_question_scaling_2026.docx", "",
         "1. Question 6 is scaled: every candidate's Question 6 mark is raised by %d marks." % r6,
         "2. Only Question 6 is more demanding than the other optional questions; Questions 4 and 5 are not.",
         "3. Chart of each optional question's demand against the 1.5 line.",
         "4. Grades after scaling: %s; %s grades change." % (gp, t(fig["grade_changed"])), "",
         "### history_p2_results_2026.csv", "",
         "1. One row for each of the %s candidates who sat, Question 6 raised by %d, the best two essays credited, "
         "the paper total and the grade (the counts above)." % (t(fig["candidates_graded"]), r6), "",
         "### history_p2_entries_2026.xlsx", "",
         "1. Candidates who sat Paper 2, and answers to Questions 4, 5 and 6, by region:"]
    for r in G.REGIONS:
        e = fig["ask_a"][r]
        L.append("   - %s: sat %s; Question 4 %s, Question 5 %s, Question 6 %s" % (
            RNAME[r], t(e["sat"]), t(e["q4"]), t(e["q5"]), t(e["q6"])))
    L.append("2. Paper 2 post-results reviews requested, and of them the reviews that changed a grade, by month and "
             "region:")
    for m in ["2025-12", "2026-01", "2026-02"]:
        L.append("   - %s: %s" % (MNAME[m], "; ".join(
            "%s %s and %s" % (RNAME[r], fig["ask_b"][m][r]["requests"], fig["ask_b"][m][r]["grade_changes"])
            for r in G.REGIONS)))
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")


SOURCES = {
    "marks": ("synthetic: the board's essay marking export, one row per marking event", "2026-11-28"),
    "sec_a": ("synthetic: the scanning system's Section A extract", "2026-11-28"),
    "entries": ("synthetic: the board's entries register for History", "2026-11-28"),
    "centres": ("synthetic: the board's centres register", "2026-10-14"),
    "code": ("synthetic: the board's code of practice for examining and awarding, 2026", "2026-03-19"),
    "minute": ("synthetic: the History Awarding Committee's minute of 24 November 2026", "2026-11-25"),
    "email": ("synthetic: the Executive Officer (Results)'s request to Research and Standards", "2026-12-01"),
    "reviews": ("synthetic: the 2025 post-results review log, one row per component reviewed", "2026-03-02"),
    "predicted": ("synthetic: centres' predicted grades for History, 2026", "2026-09-30"),
    "stats25": ("synthetic: the 2025 History Paper 2 question statistics", "2025-12-03"),
    "markers": ("synthetic: the board's examiners for History Paper 2, 2026", "2026-10-30"),
}
WHY = {"predicted": "teachers' predictions say what a centre expected of a candidate, not what any essay demanded",
       "stats25": "the 2025 paper's questions are not the 2026 paper's, so its statistics say nothing about 2026's "
                  "demand"}


def metadata(path):
    files = []
    for k, name in PK.FILES.items():
        src, date = SOURCES[k]
        files.append({"name": name, "role": "distractor" if k in PK.DISTRACTORS else "evidence", "source": src,
                      "date": date, "license": "CC0 1.0 (synthetic, authored for this task)"})
    meta = {"task": "task445", "architecture": 3, "setting": "2026-12-01",
            "files": sorted(files, key=lambda f: f["name"]),
            "distractors": [PK.FILES[k] for k in PK.DISTRACTORS],
            "distractor_reasons": {PK.FILES[k]: WHY[k] for k in PK.DISTRACTORS},
            "stated_inputs": ["1.5", "25", "40", "90", "66", "57", "48", "39", "30"],
            "deliverables": ["p2_question_scaling_2026.docx", "history_p2_results_2026.csv",
                             "history_p2_entries_2026.xlsx"]}
    json.dump(meta, open(path, "w"), indent=1)
