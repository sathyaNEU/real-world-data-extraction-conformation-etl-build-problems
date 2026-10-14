# Verdict, task501 round 2

**Verdict:** DETERMINISTIC (no SOLUTION_WRONG; every golden figure reproduced). Residual forks are noted below.

**Disposition:** APPROVE. No block regeneration is needed. Two optional pins would sharpen determinism, but both change what solvers see and would need a rerun: (a) one filed sentence defining a duplicate case record, (b) one filed sentence that the winter runs in school term.

**Why:** Executed literally, with all 7 days and all contacts, the next-generation matrix built from term-time diaries only (2 to 26 May 2023, 168 per band) and scaled to R0 15 gives 1.30 with no catch-up. Option B gives 0.89 and A, C, D, E give 1.29 to 1.30. Only B is below one, so PS-07 3.6 forces B. The pooled-diary read gives 0.88 ("no catch-up needed") and is the lure. The data separates the two reads: at_school contacts are 17.5 percent of contacts in the May diaries and 2.2 percent in July and August. For 15 to 19-year-olds the figures are 59.8 percent and 1.1 percent. PS-07 3.1 requires the figure to stay below one "throughout" December to February.

**Evidence (recomputed from the bundle):**

| Item | Golden | My value | File and field |
|---|---|---|---|
| Susceptible share 15 to 19 | 11.2% | 11.22% (3,992 of 35,572, YOB 2008 to 2012) | profile per_cent_immune joined to projection persons by YOB; age = 2027 minus YOB |
| Susceptible share, region | 4.8% | 4.83% | same join |
| R, no catch-up (term) | 1.3 | 1.299 | participants and contacts, diary_date < 2023-06-01, mean contacts by participant and contact band, Unknown contacts dropped |
| R, option B | 0.9 | 0.892 | options paper expected immune 1,470, spread over the YOBs pro rata to susceptibles |
| R, options A, C, D, E | 1.3 each | 1.288, 1.292, 1.292, 1.289 | same method; E uses 1,590 and 660 as the options paper splits them |
| Residents A to E | 35,346 / 33,217 / 29,398 / 30,625 / 57,865 | identical | register_people_active: lho in LH20 to LH26, plus LH27 if lho_recorded < 2024-07-01, BT postcodes out |
| No valid dose / exactly one | A 3,545/4,720; B 4,286/6,091; C 2,857/3,960; D 4,971/7,302; E 8,526/11,793 | identical | events re-pointed through merges, GP lines with Replaced or Withdrawn outcomes dropped, date_given <= 2027-06-30, dose >= first birthday, 28-day interval from the previous counted dose |
| Confirmed cases / imported | A 9/2, B 10/2, C 11/3, D 10/3, E 16/5 | identical | NDS export: Confirmed, onset 2019-01-01 to 2027-06-30, legacy-number pairs merged, same DOB, sex and onset merged; "Imported" only |

Pooled and alternative variants (summary):

| Variant | R (none / A / B / C / D / E) |
|---|---|
| All diaries | 0.88 / 0.88 / 0.81 / 0.86 / 0.82 / 0.79 |
| Equal-period average of term and summer | 0.96 / 0.95 / 0.82 / 0.94 / 0.92 / 0.91 |
| Summer only | 0.83 (all below one) |
| Weekday-only term | 1.41 / 1.40 / 0.94 / 1.41 / 1.41 / 1.40 |
| Physical contacts only, term | 1.46 / 1.45 / 0.96 / 1.46 / 1.46 / 1.46 |

- Symmetrised, population-weighted term matrix: 1.298. Redistributing Unknown-age contacts: 1.301.
- The call (B) is robust to every variant that uses term diaries.
- The first-birthday rule matters only for option A (25 people). Ignoring the merges shifts 15 to 39 zero-dose people and 495 to 1,030 one-dose people per option. Ignoring the query log shifts 5 to 12 and 3 to 19. Applying the 28-day interval against the previous dose of any validity gives the same counts.

**Residual forks (none moves the main call):**
1. R digits: the weekday-only and physical-only conventions move the no-catch-up figure to 1.4 or 1.5 and B to 0.9 or 1.0. The prompt and PS-07 do not define "contact" or day weighting. The literal reading (every listed contact, all days, which the codebook balances at one seventh per day) gives the golden. Low risk.
2. Winter in term: no shipped file states the school calendar. It is inferred from the at_school pattern in the data and from "throughout" in PS-07 3.1. This is the one place where outside knowledge helps the solver. It is a universally known fact and the data corroborates it. Residual Gate B/C risk: low to moderate.
3. Option B case count (10 versus 9): NDS-24-000133 (onset 18/02/2024) and NDS-24-000244 (onset 01/03/2024, "Household contact") share DOB 16/04/2010, sex M, county Louth. The golden keeps two cases (twin or household second case). A solver who merges on DOB and sex alone gets 9 for B (and the same totals for the other options). No filed definition of a duplicate record exists beyond the fields notes ("one row per case record"). This is a genuine competing reading on one supplementary figure (underspecified_objective, low).
4. BT-postcode residents are excluded as living in the UK. Including them gives B 33,435 and shifts the dose counts. The register notes and the exclusion logic make the exclusion the natural reading, but the prompt never says it. Low.

**Files/Hygiene:** PASS. 21 files in 5 formats (csv, pdf, txt, docx, xlsx). The largest tables are 279,819 event rows and 164,459 register rows. Records are system-like: dd/mm versus ISO dates, swapped day/month in migrated legacy records, a legacy numbering change at 1 March 2021, and a query log covering all ages. No authoring or benchmark language found, and dates are coherent with a 12 July 2027 snapshot. Distractors such as the stock return and the uptake report are present and unused. The cross-batch check could not be run in this isolation, and no exclusion-level finding exists.

**Stump power:** Moderate to good. The main lure is real: the full survey gives 0.88, which says no catch-up and passes a sloppy review. Fieldwork periods and quotas are visible in the codebook, so a careful model can find it, but many will pool. The asks add much hardness: 5 options × 3 register figures plus 2 case figures, with the merge re-pointing, the lho scheme change, the query log and the dose validity rules. Any slip costs graded figures, so partial credit should cap well below 50. Residual risk is the three small forks above.

**Stumping type:** `mechanism: method_or_model_selection` (representative contact data for the target season, on honest data), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported number is wrong. The task turns on matching the survey sample to the winter, with the matrix and eigenvalue computation done correctly. The ETL conformance of the register is a heavy supplementary layer. On clean data the term versus holiday structure would still stump.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. The field's own analysis, a next-generation matrix R from age-structured contacts and immunity, decides the call. A capable analyst who cleaned everything correctly takes the full survey (7,560 diaries) and gets R 0.88, "no catch-up needed". The golden is B. Layer 1: migrated and back-entered case records, a changed lho scheme, merged registrations, and superseded GP lines. Layer 2: seasonal representativeness of the contact matrix, plus the intervention applied to the right susceptibles.

**Fix:** none required (fix location: none). Optional, in the prompt: pin the duplicate-case definition and the school-term premise.

## Disposition

Approved as judged (the round 2 judge, one isolated thread at medium effort on the round 2 pack of commit 03b4877).
Gate G and Gate H as the verdict states them: `method_or_model_selection` on honest data, no surface-read dependency, no
sole data defect; domain, layers and decisive step pass, the decisive step analytical. The four residual forks were
closed in one generator pass without a pin, a document edit or a prompt edit, and no graded figure moved: `freeze.py
check task501 --mode determinism` PASS against the round 2 snapshot.

1. **Residual fork 1 (weekday-only or physical-only matrices, 1.4 or 1.5 and B 0.9 or 1.0).** Closed by the literal
   reading, as the judge found it: the codebook defines a contact as "a conversation of at least three words in each
   other's presence, or any skin-to-skin contact" and balances diary days at one seventh per day in each band and
   period, and PS-07 3.1's reproduction number is the people one case infects. Fork rows SF20 (term weekdays: 1.41, B
   0.94) and SF26 (physical contacts only: 1.46, B 0.96), both the same call with figures a quoted sentence refuses;
   asserted in `checks.py` with SF19's day balance.
2. **Residual fork 2 (the winter runs in school term).** Not pinned: a filed sentence or a 2027-28 school calendar names
   the decisive step and would turn the choice of diaries into a rule to execute (the design note's `## Tried and
   rejected`). Recorded as fork row SF25 and closed in the data: at-school contacts are 17.5 per cent of all contacts in
   the May diaries against 2.2 in July and August (15 to 19-year-olds 59.8 against 1.1), the options paper puts the
   school team's sessions in schools from 15 September to 20 November, and PS-07 3.1 binds the figure throughout
   December to February; asserted in `checks.py`, with no call document naming term, the holidays or a school calendar.
3. **Residual fork 3 (option B's confirmed cases, 10 against 9).** Closed in the data, figure-neutral. NDS-24-000133
   and NDS-24-000244 are the 2024 outbreak's twins, built as two boys, so a date of birth and sex key joined them; the
   second twin is now a girl (one field on one record), keeping the pair's own distinguishing fields (onsets 12 days
   apart, the second epi-linked to the first as a household contact). Fork row SF27, asserted: no two people share
   date of birth, sex and county among the case records (every such group is one person, joined by its legacy number
   or its single onset), and once the 2019 back-entries are joined through their legacy numbers every person key (date
   of birth and sex; with onset; with onsets within 14 days; with county) gives every Ask 3 figure, in `checks.py` and
   on its own code path in `verify.py`. Option B stays at 10 confirmed and 2 imported; only a key without sex, which
   joins a boy and a girl, gives 9. The optional duplicate-case definition was declined: it would adjudicate both Ask 3
   devices.
4. **Residual fork 4 (BT postcodes, B 33,435 if counted).** Fork row SF23, closed by the meaning of living in the
   region: the extract notes define postcode as "Postcode of that address" and lho_code as the local health office of
   the person's address, every recorded postcode is an Eircode or a BT postcode, a BT postcode is an address in the UK,
   and the national code list holds no office outside the State, so the school's code beside a BT postcode cannot be
   the address's; asserted. The register's own region code does not decide it, by design. The call reads no register
   file, so the call is the same under either reading; the ask figures are kept, as the judge accepted them.
5. **Realism (the round 2 leak reader).** The extract notes' container scrubbed: the template thumbnail, the customXml
   bibliography store and the preview setting dropped with their references, the duplicate Company element merged, the
   body byte-identical. The stock return's batch numbers now carry their manufacturers' lot formats (a distractor; only
   the batch column changed). The options paper's budget sentence is left as filed: a document change would need
   another reader pass, and no figure or reading turns on it.
6. **Rebuild and free gates.** `checks.py` 307 PASS; `verify.py` PASS; two builds byte-identical (21 pack files, 2
   goldens, figures.json); `figures_check.py` exit 0 (59 figures); `precut.py` exit 0 (27 fork rows); `voice-check.py`
   exit 0; `leak.py --asof 2027-07-12` REVIEW (no LEAK, sweep 11 clean, the same five lines as before, answered in the
   design note); the container audit clean on target/ and golden/; `guard.py surface` 0 promoted pairs (nearest task132
   at 0.100); `guard.py heart` WARN, no BLOCK; `guard.py validate` 169 cards, 0 invalid. Changed under target/: the case
   export (one record's sex), the stock return (its batch column) and the extract notes (container only). Both goldens,
   figures.json, metadata.json and submission.md are byte-identical to the judged build, and target.zip is cut from the
   final rebuild (21 members, identical to target/). No re-judge: the verdict was APPROVE and the repair moved no graded
   figure and no document's text.
