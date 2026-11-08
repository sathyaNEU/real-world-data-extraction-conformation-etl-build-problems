## Tags

**Domain:** Education & Learning Sciences (item response theory and test equating: a schools' assessment trust pre-equating draft papers from its Rasch item bank).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Set Paper C for the November 2027 sitting: its expected mark at the Achieved standard is 25 of 50 (24.80), against 26 for Paper A (25.89) and 23 for Paper B (23.02).**

## 2. Critical Components

- The bank's Term 3 difficulties come from the August 2026 sitting, where 89 per cent of the responses to Term 3 items came before the candidate's own school had finished the unit (each session's New Zealand sitting day against the school's sequence in the course review's Appendix B).
- Each Term 3 item is re-estimated on the taught responses (104 to 176 per item) with abilities fixed on the Term 1 and 2 items at their final 2026 bank values; the scale stays on the anchor block.
- Expected marks at 0.35 logits: Paper A 25.89, Paper B 23.02, Paper C 24.80; the bank as calibrated gives 24.78, 20.64 and 21.58 and would set Paper A.
- Term 3 items per draft: Paper A 6, Paper B 11, Paper C 17.

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
- Candidates entered: Northern 1,915, Central 1,213, Capital 1,035, Southern 1,289.
- Candidates who sat, online or at a make-up session: Northern 1,874, Central 1,188, Capital 1,013, Southern 1,261.
- Candidates who sat a make-up paper: Northern 61, Central 37, Capital 27, Southern 45.
- Mean make-up mark: Northern 28.4, Central 25.8, Capital 23.8, Southern 25.3.
