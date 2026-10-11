# task445 design note

Seed ET02 (13F institutional ownership bridge). Objective Data Extraction & Conformation (ETL).
Client domain Quantitative Finance, task type `other` (institutional ownership analytics from
regulatory holdings filings). Architecture 1.

## DRAW

| Axis | Draw |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task445.json`, registered 2026-10-11, verdict WARN (answered below) |
| Shape | 03, bridge between two totals (the September walk from the SEC information-table lines to conformed institutional shares), carried inside a twelve-row flag file |
| Gate G mechanism | `method_or_model_selection` (how a period still inside its filing window is completed, chosen on a back-test the history supports) |
| Gap / pattern | time, then population / none of A to E |
| Generators | G12 (a manager with no December report yet is not a zero holder), G16 (completion method by back-test), G6 (late-filer mix differs by issuer), G19 on the asks |
| Decision type | designation set: which of the 12 watchlist names carry the crowded flag for the December 2022 quarter |
| Stakeholder | head of ownership research (role family `product_manager`) |
| Context artifact | register (the desk's manager register) |
| Calibration form | `censored_or_lagged_release`: the June and September 2022 filing windows, complete, with filing dates |
| Stump strategy | `maturity_censoring`; decisive rule filed: the estimand is filed (OM-4 s.2), the completion method is not; no official decoy, no validated decoy |
| Forum / forcing / org | the client (`customer_or_counterparty`) / the flag file's fixed issue date inside the filing window (`other`) / `professional_services` |
| People | Nancy Henderson (methodology owner), Jonathan Richardson (data engineering), drawn with guard.py names, seed 445 |
| Invented names | Quillfield Research LLC (the desk), Harrowby Point Partners (the client); all managers and issuers invented from word lists |

**WARN answered.** `repeat.decision` against task229: both commit to a set, but task229 fires an alert
per firmware build from a standard error built over the right unit; here the set is a threshold flag on
an ownership share whose numerator is censored at the extract and has to be completed holder by holder.
Different gap (time against population), different quantity, different construction.

**Similarity claim.** No prior build completes a filing period that is still open at the extract from
each reporter's last filed position; task130 v1 (lineage) built a future holding set forward from a past
snapshot, which is a forward roll of a known book, not a censored total with an issuer-skewed tail.

## The three rules

- **Domain (swap test).** The flag turns on ownership-data practice specific to 13F: holdings arrive over
  a 45-day window, filing lag tracks manager type (the index sponsors and multi-strategy funds file at the
  deadline), positions of slow filers persist quarter to quarter, and ownership is measured in shares
  against the issuer's cover-page count. Swap the nouns and the censoring structure, the manager-level
  carry and the shares denominator have nothing to attach to.
- **Two layers.** Layer 1 below; Layer 2 is the censored period.
- **Decisive step class: analytical.** Analyst test: a strong analyst who conforms every 13F line correctly
  (amendment types, value units by filing date, option lines out, CUSIPs repaired) and reads OM-4 correctly
  computes ownership on the reports in hand and flags WHII and JEMS only, or scales every name by one
  aggregate completion share and flags WHII, AMRB, TAAV, JEMS, FENN and SAF. Nothing they read is wrong;
  what is wrong is treating a filing window that closes on 14 February as closed on 3 February.

## Stump sentence

A competent solver conforms the December 2022 13F reports in hand perfectly and flags the names whose
institutional ownership on file is above 80 per cent (WHII and JEMS), or, seeing that the window closes on
14 February, scales every name by the aggregate share of value historically on file by the same day and
flags WHII, AMRB, TAAV, JEMS, FENN and SAF; both file the wrong set, because the step that decides it is
completing the period holder by holder: the 125 managers that filed for September and have not filed for
December are holders not yet reported, they are mostly index sponsors and multi-strategy funds, and they
sit in GLI, OTF and SAF's registers far more than in AMRB's or TAAV's.

## Data-native sentence

13F holdings arrive over a 45-day window and the managers that file at the deadline are a different slice
of each issuer's register, so the share of an issuer's final ownership on file on any day before the
deadline varies issuer by issuer (from 67 per cent to 95 per cent here), and only a holder-level
completion recovers it.

## The two layers

- **Layer 1 (mess, real system behaviour):** the SEC Form 13F data sets organised by submission quarter
  (so a period's reports are split across two drops), originals with RESTATEMENT and NEW HOLDINGS
  amendments, value in thousands before 2023-01-03 and dollars after, by filing date, with one filer still
  on the thousands basis after the switch (several did this in early 2023), put and call lines on the
  share CUSIP, filer-keyed CUSIPs (leading zeros dropped, lower case, one bad check digit), positions split
  across lines by investment discretion, cover-page share counts at as-of dates either side of a period
  end, affiliated managers filing under separate CIKs, 13F notice filers, combination reports.
- **Layer 2 (decides the call):** the December period is censored at the extract. Shortcut: read the
  reports in hand as the period, or one aggregate completion share. Expert move: complete holder by holder
  (each manager with a September report and no December report carried at its September share position),
  which the September window back-tests to within 2.6 points on every name (mean 0.7).

## Gate G

- Litmus: no reported number in the pack is wrong and no stakeholder conclusion is overturned. Every
  13F line is as filed; the difficulty is that the period's ownership is not all filed yet.
- Mechanism: `method_or_model_selection` (with `forecasting` support: the committed call is about a
  period whose filing window closes after the call).
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- Clean-data test: repair every Layer 1 device (amendments applied, units, CUSIPs) and the answer and
  the on-file read do not move (the main call's rows carry none of them, asserted). Instrument repair: had
  the instrument observed the December holdings of every manager, the task would be a sum; but the
  instrument is not defective, the period is open, and no file in the pack misreports anything.
- Lens swap: the naive read (reports in hand) and the answer (the period's reports) are different
  populations at different moments, not one population under two lenses.
- Delete every wrong number: there are none to delete; still hard.

## Entity, unit, decision

Quillfield Research publishes a quarterly crowded flag (institutional ownership above 80.0 per cent of
shares outstanding, OM-4 s.7) to a hedge fund client's watchlist, one file per period, not reissued
(OM-4 s.8). The flag file for the December 2022 quarter goes out on 8 February 2023; the extract holds
13F filings accepted through 3 February (day 34 of 45).

**Answer: WHII, GLI, OTF, JEMS and SAF carry the flag; AMRB, TAAV, FENN, ABBB, OLPD, HAMR and NOPR do not.**

## Ladder (each rung a complete pipeline; sets by name)

| Rung | Construction | Flags | Killed by |
|---|---|---|---|
| R0 | conformed ownership on the December reports in hand | WHII, JEMS | OM-4 s.2 counts every manager that files for the period; 125 September filers have no December report by 3 Feb, deadline 14 Feb (readme) |
| R1 | last complete quarter (September ownership) | WHII, GLI, JEMS, FENN, SAF | December reports in hand show the registers moved: OTF's filed managers added, FENN's sold |
| R2 | on-file ownership over the share of September filers that have filed (0.687) | all but ABBB, HAMR, NOPR | a filer count is not a holdings share: the managers still to file are the largest (index sponsors) |
| R3 | on-file ownership over the aggregate share of value on file by day 34 (0.820 in the September window; 0.815 June) | WHII, AMRB, TAAV, JEMS, FENN, SAF | the same-day back-test in the September window: one factor misses names by up to 22.3 points |
| R4 | issuer-level completion factor taken from the September window | all but ABBB, HAMR | the September window's day-34 share was depressed by one-off lateness (three managers filed September in January, one filed on 10 November); back-tested from June it misses by 3.6 to 8.7 points |
| R5 | holder-level completion: on-file December shares plus each pending manager's September shares | **WHII, GLI, OTF, JEMS, SAF** | survives: back-test error at most 2.6 points (mean 0.7) on every name |

Why each is satisfying to stop at: R0 is a perfect conformance of everything filed; R1 is the
conservative "publish the last complete quarter"; R2 and R3 are the standard ratio gross-ups; R4 is the
development-factor method an actuary would reach for. The decisive rung (R5) needs a group construction
(the set of managers with a September report and no December report, joined to their September lines),
not a row predicate, and has no arithmetic symptom: every reconciliation of the reports in hand ties.

Answer margins from the line (golden, unrounded): WHII 88.56, GLI 84.37, OTF 83.38, JEMS 84.83, SAF
91.42 (flagged); AMRB 76.23, TAAV 74.31, FENN 77.30, ABBB 62.31, OLPD 71.14, HAMR 55.20, NOPR 67.20.
Nearest to the line: FENN at 2.70 below, OTF at 3.38 above.

Convergence of rigorous variants (asserted): a matched-panel version (pending shares scaled by the
December/September ratio of managers that filed both) and a version that drops the register's inactive
managers both give the same five flags. The simulation's true completed December holdings give the same
five flags with every name within 1.0 point of the golden.

## 22-axis closure (determinism-check Part 1)

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | managers that file a holdings or combination report for the period (OM-4 s.2); notice filers excluded; C1 |
| 2 | Unit of account | shares (SH lines, no put/call), OM-4 s.3; filed |
| 3 | Attribution window | report period on the cover page, not the drop it arrived in; filed (readme says drops are by submission date) |
| 4 | As-of dating | share count with the latest as-of date on or before the period end, OM-4 s.5; filed; the Jan 10-K count moves no flag (asserted) |
| 5 | Version basis | report as amended, amendment types per readme; asserted separately on the September ask |
| 6 | Denominator | cover-page count, OM-4 s.5; filed |
| 7 | Weighting | none (a share of shares) |
| 8 | Window length | not applicable to the main call; back-test windows are the June and September windows at day 34 |
| 9 | Boundary inclusivity | "above 80.0 per cent"; nearest name 2.70 points away; C4 |
| 10 | Rounding path | flag on the unrounded figure; one-decimal figures asserted at least 0.02 from the half step |
| 11 | Tie-break | top holder ties: none within 8 per cent (asserted) |
| 12 | Maturity / censoring | the decisive axis: the December period is censored; holder-level completion selected by back-test (C2 as confirmation of the construction the estimand implies); every rival named and asserted wrong |
| 13 | Order of operations | amendments applied in filing order (RESTATEMENT replaces, NEW HOLDINGS adds); no pending manager has an amendment (asserted) |
| 14 | Row order | sums; order-free |
| 15 | Duplicate resolution | lines per position summed (OM-4 s.3); C1 for the main call |
| 16 | Identity normalisation | CUSIP to nine characters, check digit, name and title fallback (OM-4 s.4); no repaired line in the main call's rows (asserted) |
| 17 | Netting | none |
| 18 | Dimensional units | VALUE units only on the top-holder ask; the main call reads shares |
| 19 | Code semantics | PUTCALL, SSHPRNAMTTYPE, REPORTTYPE, AMENDMENTTYPE per readme |
| 20 | Integerisation | whole shares as filed; carried shares are whole |
| 21 | Scope of a clause | OM-4 s.2 governs the period; s.8 (not reissued) makes the call forward facing |
| 22 | Forward window contents | managers expected to file December = September filers without a December report by the extract; inactive-register variant converges (asserted) |

## Ask sheet and device ledger

Criteria arithmetic (shape 03 inside a twelve-row file): 12 flags + 12 December ownership + 12 December
share counts (main and critical components, 36) · 12 September ownership + 12 September share counts (24)
· 12 top holders + 12 values (24) · bridge start, three items and end (5) plus its named parts (one bar per
item, labels in whole shares, waterfall) · two files present. About 90 criteria.

| Ask | Use | Primary device | Other devices on the path | Wrong stops (asserted) |
|---|---|---|---|---|
| September ownership and share count, per name | the client compares the December flag with the restated September figure | D2 version: RESTATEMENT replaces a bank trust's whole September report; NEW HOLDINGS adds an adviser's confidential positions (filed 12 Jan 2023, in the daily build, in dollars) | D4 three managers' September reports filed in January sit in the next drop; D7 keyed CUSIPs (OTF, AMRB, OLPD, NOPR); D8 share count dated on or before 30 Sep, not the October count | own drop only: every name 2.4 to 5.8 points low; latest accession wins: 9 names low by 2.0 to 3.0; every accession summed: every name high by 1.6 to 2.9; exact CUSIP join: 5 names low by 0.5 to 9.5; count dated after the period end: every name high by 0.2 to 3.5 |
| Largest holder by market value at 31 Dec and the value, per name | the client sizes against who holds most | D3 units: Wexley Trust Wealth Advisors filed December on the thousands basis after the switch (implied prices a thousandth of every other filer's) | D6 Tregaron National Bank reports AMRB and OLPD across three lines; D7 two Shelby affiliates file separately (OM-4 s.6 does not combine) | as reported: GLI, ABBB, HAMR go to Prescott; largest single line: AMRB, OLPD go to Prescott; family combined: TAAV, NOPR go to the Shelby group |
| September bridge, twelve names combined | clients tie our September figures to the SEC files | D2 superseded lines (16,011,685) | options (5,183,600), keyed CUSIPs (9,304,719) | a walk without the restatement, without the repairs, or starting from one drop lands on a different end |

Separation (main call's declared rows: December lines in hand for the twelve CUSIPs, SH, no put/call,
columns CUSIP and SSHPRNAMT; pending managers' September lines for the twelve CUSIPs; the October-dated
cover counts): zero repaired CUSIPs, zero amendments, zero January September reports, zero option lines
among pending managers, every device manager not pending (asserted in `checks.py`). The thousands-basis
filer's December lines sit in the main rows but the device is in VALUE, a column the main call never reads.

Referee: the readme's VALUE definition plus every other filer's implied price for the same CUSIP.

Pair arithmetic (planning weights 38/7/55, r about 5): a response that lands the call keeps the 36 main
criteria; on the asks a strong conformer is expected to keep roughly a third (it handles amendment types
and options, misses some of the drop split, the count date, the thousands filer). Estimate: cracker
45 + 55 x 0.35 = 64; best miss 5 + 7 + 55 x 0.30 = 28.5; pair about 46, under the 50 bar and above the 40
target. The margin rests on the main ladder holding all but one response off the call.

## Input gates

19 files, 7 formats (csv, htm, md, pdf, tsv, txt, xlsx), largest file `form13f_2022q4/INFOTABLE.tsv`
at 39,301 rows. Distractors (in `metadata.json` only): the short interest file and the 13(f) list.

## Stopping rule

Two consecutive in-house rounds landing the call by holder-level completion file this architecture as
solved; harden by moving the decisive construction (not the devices). A round that lands R0, R1 or R3
licenses one repair of the ask layer only.

## Tried and rejected

- Seed ET02 as written (amendment-type supersession and filing-date value units deciding the flag):
  rule application and data semantics as the decisive step, banned; kept as Layer 1 on the asks.
- A top-holder ask with every manager in contention, including index sponsors still to file: the top
  holder would be unknowable at the extract; the large early complexes are made the top holders and every
  pending manager's carried value is asserted under 80 per cent of the top.
- The issuer-level completion factor as a rigorous variant: once the September window carried one-off
  lateness (January reports, a 10 November original) it stopped converging, so it is a wrong rung (R4),
  refuted by the June-to-September back-test.
- Whole-percent December ownership to absorb estimator spread: dropped; the back-test selects the
  holder-level construction and every graded figure is held at one decimal.
