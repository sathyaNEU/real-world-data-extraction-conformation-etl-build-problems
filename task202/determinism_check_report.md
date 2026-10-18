# task202 determinism judge report

**Order kept.** I worked the prompt and the 17-member pack first and wrote my own derivation to
`/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/task202_derivation.md`,
then opened `task202_graded_blocks.md`. Nothing in the repository outside this report was read.

- **Verdict:** NOT_DETERMINISTIC
- **Disposition:** SEND_BACK. The main call turns on a 0.043 percentage-point margin in a modelled
  share whose equally licensed variants straddle the line, so the repair moves the committed figure or
  the commitment it is tested against, and prior runs are invalidated. A rerun is required.
- **Governing taxonomy:** margin_or_boundary_fragility (main recommendation), with
  competing_defensible_answer on supplementary 1 and supplementary 3.
- **Fix location:** prompt (and the policy PDF, which is an input file).
- **Gate G:** `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`,
  `surface_read_dependency: no`, `sole_data_defect: no`. No reported figure in the pack is wrong; the
  difficulty is choosing how to recover an award-level distribution for the 76 per cent of awards that
  exist only as cell aggregates, which is a model-selection problem on honest data. Gate G passes.
- **Gate H:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. The deciding quantity is the
  referral share a household-size equivalence schedule would generate against the Desk's agreed
  reviewing capacity, which is benefit-schedule design, not a stated score (swap test: replacing
  households with clinics breaks the Schedule B equivalence scale and the capacity constraint, so the
  domain is not a backdrop). Layer 1: two return layouts across the window, PRELIM/REVISED reopened
  months, portal keys in four spellings, dd/mm/yyyy run dates, a year-to-date claim register. Layer 2:
  the award-level spread exists only for 22 of 88 partners, so the share has to be modelled before the
  threshold can be inverted. Easy route: treat the 528 partner-band average awards as the awards, which
  has no within-cell spread and files PHP 5,800, a schedule that actually refers 9.82 per cent; or use
  the portal alone and file PHP 6,600. Gate H passes.

## Gate table

| gate | result | the number or quotation that decides it |
|---|---|---|
| A correct | PASS, one qualification | Every load-bearing figure reproduced: 49,265 gross awards in 528 partner-band cells across 88 partners; 11,788 portal rows for 22 partners tying to the returns to the centavo (PHP 24,476,657.10 both sides); shape CV 0.7231; share 5.9429 per cent at 7,800 and 6.0432 per cent at 7,700; band table 3,900/5,600/6,800/7,800/8,800/9,600 with 6.2/5.8/5.8/6.1/6.0/5.7 of awards and 22.9/22.1/21.9/22.5/22.4/21.8 of value, 5.9 and 22.2 overall; the rejected mean-of-cells route files 5,800 and refers 9.820 per cent; KS 16.1x and 19.1x the 5 per cent critical value for the lognormal and the gamma. Qualification: supplementary 1 reproduces only under the de-duplication rule (below). |
| B facts present | PASS, two gaps | Clause 9.1 to 9.5 and Schedule B are in `hrg_operating_policy_2027_edition.pdf`; the window population is in the three return workbooks; the spread is in `portal_awards_2025-01_2027-03.csv`. Gaps: no shipped file says the claim register's amounts are year-to-date (the dictionary says only "the amount held back, in pesos"), and the words "instruction", "cumulative" and "year to date" return zero hits across all 17 files, so the committed basis "one payment instruction counted once" is named in vocabulary no file uses. |
| C uniquely forced | **FAIL** | Three separate ways to 7,700 or 8,100 instead of 7,800, below. |
| D analytical, not semantic | PASS | The good answers split on how to estimate the within-cell spread, not on what a word means; the 5,800 and 6,600 routes are analytical errors, not readings. |
| E prompt pins the decision | **FAIL (supplementaries and the 6.0 test)** | "by scheme quarter the pesos the payment runs transferred" does not say whether the 138 identical paired runs are one transfer or two, and "the claim-months with a hold by reason" does not say whether a claim-month is a partner's claim month (202 after the re-check drop, 231 before) or a calendar claim month (17/16/15/13/12). Clause 9.1's "at or below 6.0 per cent" does not say the share is tested before the rounding the prompt orders. |
| F stump power | STRONG, partly on the wrong axis | Both easy routes file a wrong number, and the write-up's exclusions of the pooled, rescaled, lognormal and gamma routes are real and reproduce. But the last 100 pesos of the answer rests on 0.043pp, so a model can do the intended analysis and still miss. |
| G stumping type | PASS | See the Gate G line above. |
| H three rules | PASS | See the Gate H line above. |

## Why the main call is not forced

**1. The grain of the cell is unpinned and it moves the answer.** The committed method pairs cells at
partner-band grain (each partner-band's twelve-month average level) with a shape measured at the same
grain. Measuring both one step finer, cells and shape at partner-band-month grain (each claim month's
own level, CV 0.5848), is equally internally consistent and at least as faithful to clause 9.2's "the
award volumes and award levels of the twelve months to 31 March 2027": it gives 6.0813 per cent at
7,600 and 5.8193 per cent at 7,700, so the answer is **PHP 7,700**. Pairing monthly cells with the
partner-band shape gives **PHP 8,100** (6.0719 per cent at 8,000, 5.8909 at 8,100). Nothing in the
policy, the dictionary, the manifest or the prompt chooses among the three, and the write-up's
exclusions do not touch them: they rule out the pooled, the rescaled, the lognormal and the gamma, all
of which I confirm, but not the same empirical-shape method at another grain.

**2. The decisive 0.043pp sits inside the sampling noise of the only shape sample there is.** The shape
is estimated from 11,788 portal awards. Bootstrapping it (60 resamples) puts the share at 7,700 at
6.033 per cent with an sd of 0.189pp, and 47 per cent of resamples fall at or below 6.0; clustering the
bootstrap by portal partner gives 6.024 per cent, sd 0.123pp, 43 per cent at or below 6.0. The margin
that rejects 7,700 is a quarter of a standard error. This is Gate C case (b) exactly: the input error
band is far wider than the lead, so agreement with 7,800 is close to chance even for a solver who runs
the committed method.

**3. The rounding of the share, which the prompt itself orders, licenses 7,700.** The prompt says
"Round ... shares to one decimal place" and clause 9.1 commits to a share "at or below 6.0 per cent".
At 7,700 the share is 6.0432 per cent, which the deliverable reports as 6.0 per cent, i.e. at the
commitment. A literal reader who applies the test to the figure the policy asks to be reported files
7,700 and can quote both sentences. The committed answer needs the test applied to the unrounded share,
and no shipped sentence says so.

No shipped sentence makes either easy answer correct, which is the one good news here: clause 9.2 says
"all accredited partners", which rules out the portal-only route on the text alone, and nothing blesses
a dispersion-free reading of the cell averages.

## Supplementary answers

| ask | committed | my reading | status |
|---|---|---|---|
| 1 transferred by scheme quarter | 32,135,504 / 30,755,712 / 24,385,079 / 26,754,851 / 39,755,121 / 39,301,120 | 35,627,385 / 33,616,978 / 26,125,629 / 29,770,915 / 42,575,957 / 42,606,146 | **FORKED.** Both reproduce. The committed figures drop the second of 138 paired runs recorded at identical gross, net and recoveries, 9 per cent of archived partner-months, PHP 17,235,623 in all. But those are distinct runs with distinct refs, run dates and value dates (DR-202411-1 on 08/11/2024 and DR-202411-2 on 22/11/2024, both PHP 206,504.48 for HRG-ALB-001's 2024-10 claim, whose return totals exactly 206,504.48), there is no reversal, cancellation or recovery against them, and the email's own question is "whether what the Treasury actually sent out ties to what partners claimed". "The pesos the payment runs transferred" read literally is the sum of what the runs record. A second fork sits beside it: the quarter of the claim month (committed, and the reading I agree with) against the quarter of the run date, which gives 22,603,226 / 36,899,855 / 26,693,590 / 28,211,044 / 37,955,407 / 45,056,571 plus a seventh quarter of 12,903,316. |
| 2 held back by scheme quarter | 267,012 / 147,874 / 270,559 / 165,711 / 275,978 / 228,163 | identical | **PASS.** Forced on the data even though no file says the register is year-to-date: `amount_passed_php` steps by exactly the Treasury's net for the month (403,606.50 - 225,205.96 = 178,400.54), `amount_held_php` is flat in months with no new hold (8,775.61 in Jan, Feb and Mar 2025) and both reset each July. The movement basis is also invariant to the re-check question. The naive row sum (612,782 / 1,129,191 / 1,839,943 / 2,450,004 / 640,670 / 1,423,619, total 8,096,209) is the wrong set of six numbers, which is the intended device. |
| 3 claim-months with a hold, by reason | 73 / 46 / 36 / 30 / 17 and 76 not recorded | 73 / 46 / 36 / 30 / 17 and 76 reproduce exactly on the movement basis after dropping the 38 pre-receipt re-check rows; 231 (82/52/45/33/19) before the drop; 17/16/15/13/12 on distinct calendar claim months | **FORKED on the unit and on the re-check rows.** The deliverable answer calls them "partner claim-months", a gloss the prompt does not carry, and nothing in the pack states that a check dated before the return was received (e.g. CK-202407-0154 checked 2024-07-28, received 2024-08-06) is superseded; that it is, is only inferable because the later row's passed amount is the one the Treasury's net ties to (6 of 6 testable cases). The 26 surface spellings of `hold_reason` normalise cleanly to the five reasons, so that part is convergent. |

Scheme quarter itself is convergent, which answers the fourth thing to test: the scheme year starts
1 July (the manifest dates fiscal year 2024/25 as claim months July 2024 to June 2025), so the scheme
quarters are Jul-Sep, Oct-Dec, Jan-Mar, Apr-Jun, the same month groupings as calendar quarters. Only
the labels differ, every figure is identical, and the words "scheme quarter" appear in no shipped file
but need not.

The Schedule B schedule itself is clean, which answers the second thing to test: with factors 0.500,
0.707, 0.866, 1.000, 1.118, 1.225 (sqrt of the band's lower bound over four, 3 dp) each band's ceiling
follows from the committed one by one round-up to the nearest 100, applied once, and using the
unrounded square root instead changes no ceiling at 7,700, 7,800 or 8,100. Only the reference band's
product lands on a 100 boundary, and it lands on the committed figure itself.

## Files and hygiene

FAIL, one in-house item, nothing exclusion-level. 17 files, 5 formats (9 csv, 3 xlsx, 2 pdf, 1 eml,
1 md), 26,195-row portal export, distractors that read as genuine (the 2026 follow-up survey carries no
amounts and no decision-relevant field; the annual report extract is published, pre-restatement and on
the wrong window). No authoring or benchmark disclosure ("synthetic", "generated", "benchmark" all
return zero hits), no golden figure anywhere in the pack, temporal order coherent (extract 2027-04-30,
request 2027-05-06, policy approved 2027-02-12, portal to 2027-03-31). The mess is the right kind:
layout change at July 2026, HH against B band codes, four spellings of the portal partner reference,
PP-1911 bound to two accounts, PRELIM/REVISED, one recovery line, dd/mm/yyyy run dates.

The one defect: **both PDFs are unopenable by pdfminer.six and pdfplumber**, which raise
`Invalid dictionary construct` on a malformed `/Info` Producer string (`Banahaw Relief Foundation,
Inc. docum` followed by a bare `)`); `pdftotext` prints "Illegal character ')'" and recovers the text,
and pypdf with `strict=False` reads it. The governing clause 9 and Schedule B live in that file, so a
solver on the commonest Python route cannot read the decisive rule at all. In-house fix: regenerate both
PDFs with escaped metadata, content unchanged.

## Fix

1. **Prompt or clause 9.1:** state that the share is tested before rounding, and widen the step. As
   built, 7,700 fails by 0.043pp of a bootstrapped quantity with an sd of 0.12 to 0.19pp. Move the
   commitment (or the data) so the preceding multiple of 100 fails by more than about 0.3pp.
2. **Clause 9.2:** pin the grain, for example "an award's level is the average award of its partner's
   band over the twelve months" (which makes 7,800 forced) or "of its partner's band in its claim
   month" (which makes 7,700 forced). Without that sentence the method the write-up itself uses has
   three equally licensed readings.
3. **Supplementary 1:** say the basis in the asking sentence, "by the scheme quarter of the claim month,
   counting every run the archive records", and then either accept 35,627,385 and the rest as the
   committed figures or state in a shipped file that a run repeating an earlier run's amount for the
   same partner and claim month is the same instruction re-issued.
4. **Supplementary 3:** ask for "the number of partner claim-months in which the check recorded a hold,
   by reason" and say in the register's dictionary entry that a later check supersedes an earlier one
   for the same partner and claim month.
5. **Input files:** regenerate the two PDFs with valid `/Info` metadata.
