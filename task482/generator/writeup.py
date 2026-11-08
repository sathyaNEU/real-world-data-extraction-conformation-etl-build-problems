"""task482 architecture 17: submission.md and metadata.json, every figure from golden.compute()."""
import json

import params as P

REG = P.REGIONS


def submission(res, path):
    g, b, n = res["gold"], res["bank"], res["t3_count"]
    fmt = lambda d: ", ".join("%s %s" % (r, d[r]) for r in REG)
    ent = {r: "{:,}".format(res["entered"][r]) for r in REG}
    sat = {r: "{:,}".format(res["sat"][r]) for r in REG}
    mk = {r: "%.1f" % res["makeup_mean"][r] for r in REG}
    txt = """## Tags

**Domain:** Education & Learning Sciences (item response theory and test equating: a schools' assessment trust pre-equating draft papers from its Rasch item bank).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Set Paper C for the November 2027 sitting: its expected mark at the Achieved standard is 25 of 50 ({gC:.2f}), against 26 for Paper A ({gA:.2f}) and 23 for Paper B ({gB:.2f}).**

## 2. Critical Components

- The bank's Term 3 difficulties come from the August 2026 sitting, where {un} per cent of the responses to Term 3 items came before the candidate's own school had finished the unit (each session's New Zealand sitting day against the school's sequence in the course review's Appendix B).
- Each Term 3 item is re-estimated on the taught responses ({tmin} to {tmax} per item) with abilities fixed on the Term 1 and 2 items at their final 2026 bank values; the scale stays on the anchor block.
- Expected marks at 0.35 logits: Paper A {gA:.2f}, Paper B {gB:.2f}, Paper C {gC:.2f}; the bank as calibrated gives {bA:.2f}, {bB:.2f} and {bC:.2f} and would set Paper A.
- Term 3 items per draft: Paper A {nA}, Paper B {nB}, Paper C {nC}.

## 3. Step-by-Step Solution

1. Map each draft's card numbers to bank codes through the 2025 renumbering and take the final 2026 run's difficulties.
2. Put each session's start into New Zealand time and join the candidate's school to its Term 3 start and sequence in Appendix B (names through member_schools.csv), weeks counted from the school's own start.
3. Mark each response to an item from the two late units taught when its sitting date is after its school's last date for that unit; each school's second late unit runs to its term's end.
4. Keep the later answer where an item was answered again after a reconnect.
5. Estimate abilities on the Term 1 and 2 items at their bank values, then re-estimate each Term 3 item on its taught responses with those abilities fixed.
6. Sum each draft's Rasch probabilities at 0.35 logits and set the draft nearest 25 before rounding.
7. Entered: standing entries (status E) once per candidate on first name, surname and birth date; sat: online candidates plus each keyed script at its home school (typed roster by script number, otherwise the keyed entry number through the register); make-up marks with the one keying batch that holds values over 50 halved whole.

## 4. Deliverable Answers

### council_memo.docx

- Set Paper C.
- Expected marks at the Achieved standard: Paper A 26, Paper B 23, Paper C 25.

### achieved_marks.png

- Paper A 26, Paper B 23, Paper C 25, against the specification's 25.

### paper_choice.xlsx

- Expected marks at the Achieved standard (nearest whole mark): Paper A 26, Paper B 23, Paper C 25.
- Candidates entered: {ent}.
- Candidates who sat, online or at a make-up session: {sat}.
- Candidates who sat a make-up paper: {mkn}.
- Mean make-up mark: {mk}.
""".format(gA=g["A"], gB=g["B"], gC=g["C"], bA=b["A"], bB=b["B"], bC=b["C"], nA=n["A"], nB=n["B"], nC=n["C"],
           un=res["untaught_pct"], tmin=res["taught_min"], tmax=res["taught_max"], ent=fmt(ent), sat=fmt(sat),
           mkn=fmt(res["makeup_n"]), mk=fmt(mk))
    with open(path, "w") as fh:
        fh.write(txt)


FILES = [
    ("y10sci_aug2026_responses.csv", "evidence", "the delivery platform's response export for the August 2026 online sitting, one row per scored response", "2026-08-24"),
    ("y10sci_aug2026_sessions.csv", "evidence", "the delivery platform's session log for the August 2026 sitting (UTC)", "2026-08-24"),
    ("corlinn_item_bank_2026.xlsx", "evidence", "the Year 10 science item bank after the final 2026 calibration", "2026-09-08"),
    ("bank_calibration_runs.csv", "evidence", "the bank's 2025 final and 2026 preliminary and final calibration runs", "2026-09-07"),
    ("item_renumbering_2025.csv", "evidence", "the bank's 2025 renumbering from item card numbers to bank codes", "2025-02-01"),
    ("y10sci_2027_drafts.xlsx", "evidence", "the drafting panels' three draft papers for 2027, by item card number", "2026-11-02"),
    ("y10sci_paper_specification_2027.pdf", "governing", "the Assessment Committee's 2027 paper specification", "2026-11-04"),
    ("standard_setting_record_y10sci.pdf", "governing", "the standard-setting record (standards on the bank scale)", "2026-03-04"),
    ("council_minute_2026_10_14.pdf", "governing", "the Council's minutes of 14 October 2026 (the 2027 sitting dates)", "2026-10-16"),
    ("y10sci_course_review_2026.pdf", "evidence", "the Curriculum Committee's 2026 course review with member schools' sequences", "2026-09-09"),
    ("member_schools.csv", "evidence", "the Trust's member schools with codes and regions", "2026-08-31"),
    ("paper_choice_request.eml", "context", "the head of assessment's request", "2026-11-06"),
    ("entries_register_aug2026.xlsx", "evidence", "the Trust's entries register for the August 2026 sitting", "2026-08-31"),
    ("makeup_roster_aug2026.pdf", "evidence", "the make-up sitting's typed roster by host centre", "2026-08-31"),
    ("makeup_scripts_keyed.csv", "evidence", "the office's keyed make-up scripts", "2026-09-10"),
    ("candidate_survey_2026.csv", "distractor", "the post-sitting survey of candidates' attitudes to science", "2026-08-24"),
    ("member_bell_times_2026.json", "distractor", "member schools' Term 3 bell times from the timetabling system", "2026-08-31"),
]


def metadata(path):
    d = {"task": "task482", "architecture": 17, "setting": "2026-11-06",
         "files": [{"name": f, "role": r, "source": "synthetic: " + s, "date": dt,
                    "license": "CC0 1.0 (synthetic, authored for this task)"} for f, r, s, dt in sorted(FILES)],
         "distractors": ["candidate_survey_2026.csv", "member_bell_times_2026.json"],
         "distractor_reasons": {
             "candidate_survey_2026.csv": "candidates' attitudes after the sitting: relevant to how the cohort felt "
                                          "about the paper, unused by the pre-equating or the regional counts",
             "member_bell_times_2026.json": "each school's period times: relevant to when sessions ran, unused because "
                                            "the session log carries every sitting's own time"},
         "stated_inputs": ["the paper specification's targeting rule (nearest 25 at the Achieved standard)",
                           "the standard-setting record's Achieved standard, 0.35 logits on the bank scale",
                           "the Council's November 2027 sitting dates"],
         "deliverables": ["council_memo.docx", "achieved_marks.png", "paper_choice.xlsx"]}
    with open(path, "w") as fh:
        json.dump(d, fh, indent=1)
        fh.write("\n")
