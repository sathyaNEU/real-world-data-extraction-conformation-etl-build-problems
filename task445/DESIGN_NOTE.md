# task445 design note

Seed ET02 (13F institutional ownership bridge). Objective Data Extraction & Conformation (ETL).
Client domain Quantitative Finance, task type `other` (institutional ownership analytics from
regulatory holdings filings). Architecture 1, hardening loop 2 (paper half written 2026-10-12).

Loop 1 exists because portal round 1 failed determinism: OM-4 s.2 named the managers that "file" for the
period and filed no completion, so the literal reading counted only the reports on file and the golden's
completion read as an inference. Loop 1 filed the estimand literally (the managers still due are in the
population and their holdings are estimated) and a criterion that selects the estimation basis without naming
it, which moved the stump from WHAT to HOW: the basis. In-house round 2 stopped at flat carry; round 3 tested five
bases and landed the call on each register type's change pooled across the names.

Loop 2 makes that type-pooled step complete and still wrong, on the data's own structure. An index or ETF sponsor
holds a fixed slice of each company's float, so in shares its holding in a name moves with its creations (its
stake in every name grows 5.5 per cent a quarter, as in loop 1) and with that name's own share count (an offering,
a buyback, a tender, stock issued for an acquisition), while an active manager's share count moves with neither.
Most watchlist names now carry share-count moves in both windows and both directions, so the sponsors' change
pooled across the names in shares (about 4.5 per cent in the December window, 5.75 in the September window) is
right on no single name. The basis the filed criterion selects grows each sponsor still due by the change its filed
peers show in that name (equivalently, carries its September stake grown by the sponsors' stake growth and reads it
back against the December count), every other type flat. OM-4, the readme, the layout, `data_sources.md` and the
prompt are byte-identical; the flag set is unchanged; the ask layer keeps its design and is re-tuned on the new
September positions.

Loop 1 ask layer (designer pass, 2026-10-11, after round 2's ASKS LEAK): the main call, OM-4 s.2, the ladder
and every main-call row and figure stay byte-identical. The September counts, the top holder and the old
device set are retired as asks because each was a work order an OM-4 rule or a filed field points at; the
layer is rebuilt on two silent devices no filed sentence speaks to (two amendments filed the same day,
ordered by amendment number against the file's order, and a restatement whose submission header carries the
wrong period), carried by the September figures the filed criterion is run against. The prompt is
`prompt.txt`; the client layout moves to v4. The builder's instructions close the ask sheet. Round 3 measured
the layer at 18 per cent of the ask weight with the call landed; loop 2 keeps it.

## DRAW

| Axis | Draw |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task445.json`, rewritten in place for loop 2 (2026-10-12; the loop 1 driver moved to `lineage` beside loop 0's) and re-filed with `guard.py register --force`; `check` and `heart` answered below |
| Shape | 03, bridge between two totals (the September walk from the SEC information-table lines to conformed institutional shares), carried inside a twelve-row flag file |
| Gate G mechanism | `method_or_model_selection` (the completion basis, chosen by the back-test OM-4 s.2 files), with `forecasting` support (the period is still inside its filing window) |
| Gap / pattern | time, then population / E: the completion factor for the class that holds slices of each company is conditioned on the company (its share count), against one factor per class pooled across the names |
| Generators | G14 (the sponsors' completion factor is conditioned on the name), G16 (basis selected by back-test), G6 (each name's share count moves under the share metric), G19 on the asks |
| Decision type | designation set: which of the 12 watchlist names carry the crowded flag for the December 2022 quarter |
| Stakeholder | head of ownership research (role family `product_manager`) |
| Context artifact | register (the desk's manager register, which carries each manager's type) |
| Calibration form | `censored_or_lagged_release`: the September 2022 window, closed, re-run at its own day 34 (3 November 2022), completing from June |
| Stump strategy | `forecast_method_backtest`; decisive rule filed: the estimand and the criterion that selects the basis (OM-4 s.2); the basis is not filed; no official decoy, no validated decoy |
| Forum / forcing / org | the client (`customer_or_counterparty`) / the flag file's fixed issue date inside the filing window (`other`) / `professional_services` |
| People | Nancy Henderson (methodology owner); Brian Guerra (data engineering), drawn with `guard.py names --geo 'United States' --seed 445` |
| Invented names | Quillfield Research LLC (the desk), Harrowby Point Partners (the client); managers and issuers from word lists |

**Guard verdict answered** (loop 2, 2026-10-12, card as rewritten; `check`, `register --force`, `heart`, `validate`):

- `BLOCK ban.forum` against task228 (v2). The registration-order artifact recorded at loop 1: task228's v2 card
  was filed on main at 16:21 on 2026-10-11, after this card was registered at 15:47; same-day draws sort by task
  number, so task228 reads as this card's predecessor although neither guard saw the other at draw time. The
  forum is the client the flag file goes to and has not moved since the original PASS registration; this loop does
  not move it. Re-filed with `register --force`, the reason in the card's `notes`.
- `WARN people.last` Henderson against task117 (older): answered at the draw, kept.
- `WARN repeat.gate_g` and `WARN repeat.decision` against task230: task230 designates which patient-app KPI series
  carry a series-break flag, read against a counterfactual built within each usage band; here the mechanism is a
  completion basis selected by a filed back-test and the designation set is the client's flag file, inherent to the
  build.
- `NOTE driver.near` 0.19 against this slot's own loop 1 driver (lineage), differentiated on the card: loop 1 moved
  each missing reporter by its class's drift pooled across the units, which round 3 landed and which is loop 2's
  stump rung; loop 2's claim is that the drifting class holds fractions of each unit, so its change has to be applied
  unit by unit with each unit's own size change. task181 is out of the nearest drivers (it was 0.08 at loop 1).
- `heart`: nearest driver or stump text on file 0.05 (task107 v4's stump, task125's driver); no template, no
  duplicate. `validate`: 138 cards, 0 invalid.

**Similarity claim.** No prior build completes an open reporting period by moving each missing holder of the class
that keeps a fixed fraction of each unit with that unit's own size change and the class's change in fraction, while
the other classes keep their amounts. task181 nowcasts how much of a period is still in transit from each route's
own arrival history; here who is missing is known exactly and the question is what they now hold, and neither their
own history (own trend is a rival here: OTF 79.3) nor a factor pooled across the units answers it. task446 backs a
forward count out of a screen's flagged share through error rates that hold while the yield moves with the base rate.
task107 v4 carries units past a dated pay step that earlier entrants show. task130 v1 built a holding set forward
from a past snapshot. This slot's loop 1 (one class drift pooled across the units) is loop 2's stump rung.
Differentiation lines for task181, task107, task446 and the slot's own lineage are on the card.

**Examples read, and how this build differs.** The client's longitudinal pattern (clinical repeated measures: last
observation carried forward biases the endpoint when units drift) is the general lesson behind loop 1. The missing-data
pattern (`general-statistics-data-science/missing-data-censoring-measurement-error`: an imputation has to condition on
what drives the missing value) is loop 2's: the type-pooled completion imputes a missing index sponsor's December
holding without the variable that drives it, the issuer's own share count; learned, not copied, because the driver here
is a 13F mechanism (index funds hold the index weight, so in shares they hold a slice of each float) and it binds only
for one class of filer. task181 taught that a pooled correction across units fails where units differ; here the
correction is pooled across companies for a class whose holdings are proportional to each company. The measured-miss
catalogue's "a close match accepted" is the habit this stumps: the type-pooled change wins every basis the default path
builds (0.66 against 1.01 and up) and the solver stops.

## Three rules

- **Domain test:** the call turns on 13F ownership practice: holdings arrive over a 45-day window, the deadline filers
  are index and ETF sponsors and multi-strategy funds, and an index sponsor holds the index weight, so in shares it
  holds a fixed slice of each constituent's float (it buys into an offering and sells into a buyback or a tender) and
  that slice grows with its creations at one rate in every name, while an active manager's share count follows
  neither; ownership is measured in shares against the cover-page count. Swap the nouns and there is no float to
  track, no creation mechanism and no filing window.
- **Analyst test:** a strong analyst who conforms every 13F line correctly, reads OM-4 s.2 literally and back-tests the
  natural bases, the change by register type among them, grows each manager still due by its type's change pooled
  across the twelve names (index and ETF sponsors about 4.5 per cent in shares, every other type flat), sees it win
  the back-test against every basis it builds (prototype 0.66 points against 1.01 to 26.6), and flags WHII, GLI, JEMS
  and SAF with OTF at about 79.2; only moving each sponsor still due with the change its filed peers show in that name
  (equivalently its September stake grown by the sponsors' stake growth), the basis the filed criterion selects
  (prototype 0.04), flags WHII, GLI, OTF, JEMS and SAF. Nothing they read is wrong; what is wrong is treating the
  sponsors' quarter as one factor across companies whose share counts moved differently. Decisive step class:
  analytical (round 3 landed the type-pooled basis with every stated rule applied; that basis is now the stump rung).
- **Layer 1:** the SEC 13F data sets organised by submission quarter with the current quarter in a nightly
  build; amendment chains (two amendments to one report filed the same day; one restatement whose
  submission header carries the previous quarter's period; a September report's options added in January
  when confidential treatment ended); options keyed only in the title of class; filer-keyed and failed
  CUSIPs; value in thousands before 3 January 2023 and dollars after; cover counts dated either side of a
  period end and an amended quarterly report's later count (section The two layers).
- **Layer 2:** the basis that completes the managers still due: one change per register type pooled across the
  names (or carry, or one rate) against moving each index sponsor still due with its filed peers' change in that
  name (its stake growth times the name's share-count move), every other type flat, which the filed September-window
  criterion selects.

## Default path

The competent default pipeline, from the prompt's words and the files' grain (round 3's own path, step for step,
which now ends wrong). Figures are the scratch prototype's (loop 2 dynamics on the shipped pack's decomposition); the
builder lands its own and writes them here.

1. Union SUBMISSION, COVERPAGE and INFOTABLE from `form13f_2022q3/`, `form13f_2022q4/` and
   `edgar13f_daily_20230103_20230203/`; key each report to its period; apply amendments; keep SH lines,
   drop put and call lines, read CUSIPs per OM-4 s.4; take cover counts per s.5 from `fsds_cover_extract/`.
2. Read OM-4 s.2: the 129 managers with a September holdings or combination report and nothing for
   December are in the population and their holdings are estimated on the basis the criterion selects.
3. Build the natural bases from the files' grain: the December reports on file alone, each manager still due
   carried at its September position, every filed manager's change pooled and per name, and, from the register's
   `manager_type`, each type's change pooled across the twelve names (index and ETF sponsors up about 5.75 per cent
   in the September window and 4.5 in the December window in shares, every other type flat).
4. Run the criterion on the September window at 3 November 2022, completing from June: the type-pooled change misses
   by at most 0.66 points against 1.01 for every filed manager's pooled change, 1.38 for flat carry, 2.56 for the
   per-name change and 26.6 for the reports on file, so choose the type-pooled change.
5. Grow each of the 129 by its type's pooled change (sponsors about 1.045, every other type about 1.000), add the
   December reports on file, divide by the October-dated counts and flag above 80.0 per cent (OM-4 s.7).

Ends on: WHII, GLI, JEMS and SAF carry the flag; OTF does not.
Golden: WHII, GLI, OTF, JEMS and SAF carry the flag.

## Stump sentence

A competent solver executes OM-4 literally, sees that the index and ETF sponsors that have filed grew their share
holdings while every other register type held flat, grows each of the 129 managers still due by its own type's change
pooled across the twelve names, sees that basis beat every other it builds in the September back-test (largest miss
about 0.66 points against 1.01 for every filed manager's change, 1.38 for flat carry and 2.56 per name), and flags
WHII, GLI, JEMS and SAF with OTF at about 79.2; the step that lands it there is treating the sponsors' change as one
factor for every name, when an index sponsor holds a fixed slice of each company, so in shares it moves with that
name's share count as well as with its creations: OTF issued 4.6 per cent more shares in October and its sponsors
still due, 23 per cent of OTF, took their slice, which the two filed sponsors' OTF holdings show (up about 10.4 per cent
against 4.5 pooled), so the basis the filed criterion selects grows each sponsor still due by the change its filed
peers show in that name (largest miss about 0.04), which puts OTF at 80.4 and keeps FENN, whose managers still due are
multi-strategy funds, at 79.6.

## Data-native sentence

13F filers that file at the deadline are not a random slice: index and ETF sponsors and multi-strategy funds file last.
An index sponsor's shares in a company are its slice of that company's float, so they move with the company's own share
count (an offering, a buyback, a tender, stock issued for an acquisition) and with the sponsor's creations, while a fund's
share count moves with neither. In a quarter when the watchlist's share counts moved by -5.4 to +4.8 per cent name by
name, the managers still due in OTF are index sponsors and OTF issued 4.6 per cent more shares in October, so any one
sponsor factor across the names misses OTF exactly where the decision is made, and moving every manager still due with
the name, which fits the sponsors, lifts FENN, whose managers still due are funds and whose count rose 4.8 per cent.

## Literal reader

Executed word for word, OM-4 s.2 counts the shares at 31 December of every manager with a December holdings or
combination report on file (272 in the loop 1 pack) and every manager with a September holdings or combination report
and no December notice (the 129 still due; the 4 September notice filers with nothing yet for December are outside it,
which settles the old 128 against 125), divides by the cover-page count with the latest as-of date on or before 31
December (s.5), and estimates the holdings of the 129 on the basis that, applied with only the reports filed by 3
November 2022 (the same 34 days after 30 September as 3 February is after 31 December), comes closest to September's
ownership on all the reports since filed, by the largest miss across the twelve names. Every basis in the back-test
table is an estimate of that one estimand. Run over the whole family, the criterion selects growing each index and ETF
sponsor still due by the change the filed sponsors show in that name, every other type by its own pooled change, which
is flat (prototype 0.04 points, against 0.66 for the type-pooled change and 0.91 to 26.6 for every other basis), and
the two formulations of it converge on every name: the per-name change in shares, and the September stake (read against
s.5's September count) grown by the filed sponsors' stake change and read back against the December count. The easy
answers come only from easy methods on the same estimand (one change per type across the names, flat carry, one rate,
every manager carried at its stake), which the filed criterion rejects. No filed sentence names a basis, a stake, float
tracking or an index weight, and no filed rule, read literally, gives another estimand.

Asks, read literally: September ownership is OM-4 s.2 to s.5 on every report for the quarter ended 30
September, each taken as amended. Where the text is silent the records decide, and every reading is listed
in the ask sheet: the order of two amendments to one report filed on the same day (one order only is in the
records, the amendment numbers; the restatement numbered 2 already carries every share the new holdings
amendment numbered 1 adds), and the period of a restatement whose submission header says 30 June while its
cover page says 30 September (the cover page is the form's own statement; its holdings, priced at the 30
September close every other filer implies, match the filer's September report and not its June one). No
filed sentence, read literally, gives another September figure or another bridge.

## OM-4 text for the builder (exact)

Section 2 replaces the shipped section 2 in full:

> **2. Institutional ownership.** Institutional ownership of an issuer for a report period is the number
> of its shares held at the period end by the managers that report holdings for the period, divided by the
> issuer's shares outstanding. The managers that report holdings for a period are every manager that has
> filed a Form 13F holdings report or combination report for the period, and every manager that filed a
> holdings report or combination report for the previous period and has not filed a 13F notice for this
> one. A manager that files a 13F notice reports no holdings of its own; its holdings sit in another
> manager's report. Each report is taken as amended.
>
> Where a flag file is issued before the period's filing deadline, the holdings in reports not yet filed
> are estimated and the flag is set on the estimate. The estimate is made on the basis that, applied to the
> previous period with only the reports filed by the same number of days after its end as the reports in
> hand, comes closest to that period's ownership on all the reports since filed for it, on every security
> in the flag file; closeness is the largest difference, in percentage points, across those securities.

Section 3, first sentence only (drop "with no put or call entry", so a call keyed in the title of class
is a call line under the literal reading):

> Information-table lines reported in shares (SH). Put and call lines are exposure, not ownership, and are
> left out. (Rest of section 3 unchanged.)

OM-4 never names carry, growth, development factors or manager types, and no other section changes. The
revision line and "Changes from OM-3" stay as shipped.

Other filed text: the readme's PUTCALL row reads "Put or Call, as reported." (the shipped "where the line reports an
option" is a counter-pin against A2); Wexley's December cover page keeps ADDITIONALINFORMATION "Market values in
this report are stated in thousands of dollars." (texture now: no ask reads December values); every restatement's
cover page carries "Amendment restates the report in its entirety." and the first new holdings amendment "Amendment
adds the holdings of one trust account omitted from the original report."; `data_sources.md` describes the cover
extract as "cover pages of covered issuers' quarterly and annual reports accepted 1 May 2022 to 3 Feb 2023" and
names Brian Guerra. Loop 1 ask layer: OM-4 was byte-identical (s.8 named layout v3 until `45981f4` made it name v4,
the inconsistency the last reader found; the v4 layout's own header says it replaces v3 from the 2022Q4 files, and
the prompt names v4); the readme is byte-identical; `client_flag_file_layout.md` is replaced by the v4 text in the
ask sheet. No filed sentence names the order of two amendments filed the same day, or which of the submission header
and the cover page carries a report's period.

Loop 2: OM-4 (s.8 names layout v4 since `45981f4`), the readme, the layout v4 text, `data_sources.md` and
`prompt.txt` are byte-identical; loop 2 changes no filed sentence, and none names a basis, a stake, float
tracking, an index weight or a share count to track.

## The two layers

- **Layer 1 (mess, real system behaviour):** the SEC Form 13F data sets organised by submission quarter
  (June reports in one drop, September in the next, December in the nightly build), originals with
  RESTATEMENT and NEW HOLDINGS amendments (two to one report filed the same day through two filing agents;
  one restatement whose submission header carries the previous quarter's period; a September report's
  option positions added in January when confidential treatment ended), put and call lines on the share
  CUSIP (some carrying the option only in the title of class), filer-keyed CUSIPs (leading zeros dropped,
  lower case, failed check digits under abbreviated issuer names), value in thousands before 3 January 2023
  and dollars after, by filing date, with one filer still on thousands, cover counts dated either side of a
  period end and an amended quarterly report's later count, positions split across lines by discretion,
  affiliates under separate CIKs, a filer renamed between quarters, 13F notice filers, combination reports.
  The loop-0 restatement filed under the original form type is retired (that filing becomes a plain
  13F-HR/A).
- **Layer 2 (decides the call):** the basis that completes the managers still due. Shortcut: one change per register
  type pooled across the names (round 3's landing), or carry, or one rate for everyone. Expert move: an index sponsor
  holds a slice of each company, so each sponsor still due moves with its filed peers' change in that name (its stake
  growth, 5.5 per cent, times the name's share-count move), every other type flat; the September-window back-test
  selects it with a margin of about 0.6 points. The share-count moves are the issuers' own cover-page counts, correct
  as filed; they are the data's generating process, not a device.

## Gate G

- Litmus: no reported number in the pack is wrong and no stakeholder conclusion is overturned. Every 13F
  line is as filed, every cover count is the issuer's own, and every September position of a manager still due is
  what it reported; the task estimates holdings not yet reported, and the difficulty is which estimate, which the
  filed criterion and the data settle.
- Mechanism: `method_or_model_selection`. `surface_read_dependency: no` · `stumping_family:
  analytical_non_defect` · `sole_data_defect: no`.
- Clean-data test: repair every Layer 1 device (amendments typed, ordered and dated correctly, header
  periods, titles, CUSIPs, counts, units, the rename) and the answer and the naive answer do not move (no
  device sits on the main call's rows, asserted). The share-count moves are not repaired because nothing is wrong
  with them. Instrument test: the instrument is not defective; the December reports of the managers still due do not
  exist yet, and an estimate of a forward quantity is the decision's own quantity.
- Lens swap: the naive answer and the answer are two estimates of the same filed estimand by two methods,
  separated by a filed criterion on data; not one population read under two definitions.
- Delete every wrong number: there are none to delete; still hard.

## Entity, unit, decision

Quillfield Research publishes a quarterly crowded flag (institutional ownership above 80.0 per cent of
shares outstanding, OM-4 s.7) to a hedge fund client's watchlist, one file per period, not reissued
(OM-4 s.8). The flag file for the December 2022 quarter goes out on 8 February 2023; the extract holds 13F
filings accepted through 3 February (day 34 of 45, deadline 14 February).

**Answer: WHII, GLI, OTF, JEMS and SAF carry the flag; AMRB, TAAV, FENN, ABBB, OLPD, HAMR and NOPR do not.**

## Ladder (each rung a complete pipeline; sets by name)

Values are the scratch prototype's: the loop 2 dynamics (each sponsor's holding = its stake of the name's OM-4 count,
the stake growing 5.5 per cent a quarter; the share-count table below) applied to the shipped pack's decomposition,
every other type as shipped. The builder lands its own values and asserts every set and margin by name.

| Rung | Construction | Flags | Back-test largest miss | Killed by |
|---|---|---|---|---|
| R0 | December reports on file | WHII, JEMS | 26.6 | OM-4 s.2: the managers still due report holdings for the period |
| R1 | last quarter's ownership (September's figure as December's) | WHII, GLI, JEMS, FENN, SAF | 5.2 | the filed criterion |
| R2 | on file over the share of September filers that have filed | about ten names (builder) | about 34 | the filed criterion |
| R3 | on file over the aggregate share of September value on file by day 34 | WHII, AMRB, TAAV, JEMS, SAF (builder) | about 15 | the filed criterion |
| R4 | one factor or none across the names: each manager still due at its September position (1.38); every filed manager's change pooled (1.01) or per name (2.56); the issuer-level completion factor (builder, about 2.6); each sponsor still due at its September stake with no growth (1.15) | WHII, GLI, JEMS, SAF | 1.01 to 2.6 | the filed criterion |
| R4' (stump) | each register type's change pooled across the names, in shares: round 3's basis (sponsors about 1.045 in December, every other type about 1.000); the same pooled over every security; the sponsors' pooled change with every other type flat | WHII, GLI, JEMS, SAF (OTF 79.15) | 0.66 | the filed criterion: the per-name sponsor basis misses by 0.04 |
| R4b | one quantity for everyone: the sponsors' pooled change for every manager still due (1.18); every manager still due at its September stake (1.17) | WHII, GLI, JEMS, FENN, SAF | 1.17 to 1.18 | the filed criterion |
| R4c | the name for everyone: the sponsors' per-name change for every manager still due (1.34); each type's change measured in stakes, on every manager's stake (0.91); each type's change per name, the type by name grid (11.0) | WHII, GLI, OTF, JEMS, FENN, SAF | 0.91 to 11.0 | the filed criterion |
| R5 (decisive) | each sponsor still due grown by the change its filed peers show in that name (equivalently its September stake grown by the sponsors' stake change and read against the December count); every other type by its own pooled change (flat) | **WHII, GLI, OTF, JEMS, SAF** | 0.04 | survives |

The type change as a mean of per-manager ratios (builder; loop 1 1.171 in the back-test) flags FENN through the active
types' mean ratios and leaves OTF near the sponsors' pooled change; asserted by name, never ANS.

Own trend (each manager still due by its own June-to-September change) cannot be applied at day 34 of the September
window (no March reports ship), so the criterion cannot select it; it is no longer a golden variant: it moves each
sponsor with last quarter's count move and lands WHII, GLI, JEMS, SAF (OTF 79.28).

**The stump rung is R4'**: the completion round 3 landed, now one factor across companies whose counts moved
differently. It executes OM-4 literally, wins every basis the default path builds by 0.35 points or more, and is
where a careful analyst files. R4 is round 2's stop. R4b and R4c are the over-corrections of a solver who sees
the sponsors move with the name and moves everyone with it, or carries everyone as a stake. R0 is a rule violation
(the bottom rung, data semantics of s.2); R1 to R3 are the standard aggregate shortcuts.

**Why each is satisfying to stop at.** R0 is a perfect conformance of everything filed. R1 is "publish the
last complete quarter". R2 and R3 are the standard ratio gross-ups. R4 is the 13F completion every vendor
runs. R4' is the register-type completion: the sponsors visibly grew and every other type held flat, and it beats
every other basis the default path builds. R4b and R4c fix R4's visible bias with one number or one name.

**Share-count table** (cover-page counts, OM-4 s.5; d the December window, the September count to the October-dated
count; e the September window, the June count to the September count; the builder keeps `S_oct` and sets the others):

| Name | d | the December window | e | the September window |
|---|---|---|---|---|
| WHII | 0.970 | buyback | 0.985 | buyback |
| GLI | 0.992 (shipped) | | 1.050 | July follow-on offering |
| OTF | 1.046 | October follow-on offering | 0.996 (shipped) | |
| AMRB | 0.975 | buyback | 0.990 | buyback |
| TAAV | 1.012 | at-the-market issuance | 1.021 (A5, shipped) | August offering, in the September 10-Q/A count |
| JEMS | 0.968 | buyback | 0.988 | buyback |
| FENN | 1.048 | shares issued for an acquisition | 1.003 (shipped) | |
| ABBB | 0.946 (shipped tender) | September tender offer | 1.000 (shipped) | |
| OLPD | 1.015 | at-the-market issuance | 1.025 (A5, shipped) | August offering, in the September 10-Q/A count |
| SAF | 0.981 (shipped) | buyback | 0.960 | July modified Dutch tender |
| HAMR | 0.990 (shipped) | | 1.013 (A5, shipped) | August offering, in the September 10-Q/A count |
| NOPR | 0.960 | accelerated repurchase | 0.980 | buyback |

**Live December ownership, prototype** (golden; the builder lands each figure mid-bin on a non-round value):

| | WHII | GLI | OTF | AMRB | TAAV | JEMS | FENN | ABBB | OLPD | SAF | HAMR | NOPR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R5 golden | 88.60 | 84.42 | **80.39** | 76.19 | 74.31 | 84.80 | **79.59** | 62.31 | 71.09 | 91.40 | 55.20 | 67.19 |
| R4' type-pooled | 88.67 | 84.39 | 79.15 | 76.25 | 74.20 | 84.85 | 79.55 | 62.50 | 70.97 | 91.54 | 55.20 | 67.33 |
| R4 flat carry | 88.52 | 83.74 | 78.22 | 76.08 | 73.99 | 84.76 | 79.53 | 62.32 | 70.76 | 90.87 | 55.08 | 67.13 |
| R4 stake, no growth | 88.42 | 83.62 | 79.18 | 75.98 | 74.05 | 84.69 | 79.56 | 62.10 | 70.83 | 90.59 | 55.05 | 66.95 |
| R4b one rate | 88.78 | 84.93 | 79.30 | 76.43 | 74.33 | 84.92 | 80.27 | 62.70 | 71.15 | 91.96 | 55.38 | 67.51 |
| R4b every manager's stake | 88.34 | 83.52 | 79.33 | 75.88 | 74.08 | 84.64 | 80.32 | 61.86 | 70.89 | 90.42 | 55.01 | 66.79 |
| R4c stake change by type | 88.56 | 84.52 | 80.61 | 76.16 | 74.40 | 84.78 | 80.78 | 62.17 | 71.22 | 91.41 | 55.23 | 67.09 |
| R4c the sponsors' per-name change for everyone | 88.66 | 84.98 | 80.73 | 76.30 | 74.51 | 84.84 | 81.28 | 62.30 | 71.37 | 91.73 | 55.38 | 67.24 |

The September ownership targets (Ask A, `WATCH` `sep`) and the December targets (`WATCH` `A`) are kept; the
type-pooled rung keeps the golden's one-decimal December figure on three names only (GLI, FENN, HAMR in the
prototype), because the December-window count moves spread its error over every name.

Holdings of the managers still due at the December level, per cent of the October count (unchanged targets): OTF
index sponsors 23.2 and other types 3.2; FENN 0.7 and 16.0; GLI 15.4 and 12.1; SAF 15.7 and 9.2; every other name
under 6 in all.

**The two names nearest the line decide it.** OTF's managers still due are index sponsors and OTF's count rose 4.6
per cent in the December window; FENN's are multi-strategy funds and FENN's count rose 4.8 per cent. One sponsor
factor across the names (about 4.5 per cent) leaves OTF's sponsors short by OTF's own count move (OTF 79.15); moving
everyone with the name or carrying everyone's stake lifts FENN's funds with FENN's count (FENN 80.3 to 81.3); one rate
for every manager still due crosses the line on FENN from 2.9 per cent and on OTF only from 7.4 per cent, so no single
rate gives the golden set (asserted: FENN's crossing rate at least 3 points below OTF's; no rate from 0 to 20 per cent
in 0.05 steps lands it). The decisive rung's worth on the graded quantity: OTF 80.39 against 79.15 (1.24 points).

**The grid** (prototype, 24 cells). The sponsors' factor (none, the sponsors' change pooled across the names, the
stake without growth, the filed sponsors' change in that name) against every other type's (flat, its own pooled change,
its own per-name change, its stake, the sponsors' pooled change, the sponsors' per-name change). Only (per name, flat)
and (per name, own pooled) land on the golden set. The six cells with the sponsors flat, pooled or at a stake and the
other types flat or pooled land on WHII, GLI, JEMS, SAF (OTF 78.2 to 79.2); the twelve with the sponsors flat, pooled
or at a stake and the other types moved with a name, a stake or the sponsors' change add FENN (FENN 80.2 to 86.4); the
four with the sponsors per name and the other types moved add FENN to the golden set (the R4c set, FENN 80.3 to 86.4).
The nearest wrong cell is (per name, the sponsors' pooled change for the others), FENN at 80.31. Asserted cell by cell.

**Convergence of the golden's own variants (prototype, asserted in the build).** The filed sponsors' per-name change
for each sponsor still due, with every other type flat or by its own pooled change over the twelve; and the
September stake grown by the sponsors' stake change pooled over the twelve, or over every covered security, read back
against the December count: every name within 0.01 of the golden, the same flags and the same one-decimal figures, each
back-test miss 0.039 to 0.040. The two filed complexes give the same per-name change to 0.0005, so either alone gives
the golden too. The simulation's true December holdings give the same flags with every name within 0.15 of the golden.

## Back-test table (the filed criterion; targets for the builder)

September 2022 completed at 3 November 2022 from the June reports, against September's ownership on all
the reports since filed; largest miss across the twelve names, percentage points. Prototype values as in the ladder.

| Basis | Prototype | Target |
|---|---|---|
| golden: each sponsor still due by its filed peers' change in that name; every other type by its own pooled change | 0.039 | at most 0.15 |
| golden variants: every other type flat; the September stake grown by the sponsors' stake change (twelve names, every security) | 0.040 | each at most 0.15; every December figure within 0.01 of the golden |
| each type's change pooled across the twelve names, in shares (round 3's basis); the same over every security; the sponsors' pooled change with every other type flat | 0.660 (over every security about 0.66) | each 0.5 to 0.9; the three below every other rival by at least 0.05, and round 3's basis the smallest of the default path's five by at least 0.15 |
| each type's change measured in stakes, applied to every manager's stake | 0.912 | at least 0.6 |
| every filed manager's change, pooled | 1.013 | at least 0.6 |
| each sponsor still due at its September stake, no growth | 1.153 | at least 0.9 |
| every manager still due at its September stake | 1.168 | at least 0.9 |
| one rate for every manager still due (the sponsors' pooled change) | 1.180 | at least 0.6 |
| the sponsors' per-name change for every manager still due | 1.337 | at least 0.6 |
| type change as a mean of per-manager ratios | builder | at least 0.6 |
| flat carry at the September position | 1.380 | at least 0.9 |
| every filed manager's change, per name | 2.559 | at least 1.5 |
| issuer-level completion factor | builder | at least 1.5 |
| last quarter's ownership | 5.202 | at least 3.0 |
| type change per type and per name (the grid) | 11.020 | at least 1.5 |
| aggregate share of value on file | builder | at least 8 |
| aggregate share of filers that have filed | builder | at least 15 |
| reports on file only | 26.599 | at least 15 |

The golden basis wins by at least 0.4 points and 3x over every rival (prototype 0.62 points and 17x over the
type-pooled change), asserted. The default path's five (round 3's set: on file, flat carry, every filed manager's
change pooled and per name, the type-pooled change) are ordered with the type-pooled change first (0.66 against 1.01,
1.38, 2.56 and 26.6), asserted. With every ask device and count hazard mishandled, alone and in every combination, the
golden basis keeps the smallest miss by at least 0.3 (asserted): every September device host is a bank trust that files
all its September reports by 3 November, so its handling enters the day-34 estimate and the final figure identically and
cancels; the count hazards rescale a name's misses, and the golden's share-ratio formulation reads no count at all.

Sponsor dynamics as filed peers show them (prototype): the two filed sponsors' twelve-name share change pooled across
the names is 1.0575 in the September window and 1.0445 in the December window; their stake change pooled across the
names is 1.055 in both; their per-name share change is 1.055 times the name's count move to 0.0005 (OTF 1.104, FENN
1.106, ABBB 0.998 in December; GLI 1.108, SAF 1.013 in September).

## Readability screen

One row per rung of the main ladder; a test fires when the pack makes the move past the rung a reading or a
reflex. Measured as well as argued: round 2 stopped at R4 with every filed rule executed, and round 3 built the
type-pooled change from the register's `manager_type` and stopped there with the call landed; in loop 2 that stop is
R4', and the move past it is the decisive rung.

| Rung | 1 filed sentence | 2 schema | 3 reflex correction | 4 control bench | 5 hygiene battery | 6 linear arithmetic | Verdict |
|---|---|---|---|---|---|---|---|
| R0 reports on file | fires: s.2 counts the managers still due | no | no | fires: the criterion scores it at 26.6 | no | no | readable |
| R1 last quarter's ownership | no | no | no | fires: 5.2 in the back-test | no | no | readable |
| R2 and R3 aggregate gross-ups | no | no | the standard completion reflex | fires: 15 to 34 | no | yes, one ratio | readable |
| R4 one factor or none across the names (flat carry, every filed manager's change, the issuer factor, a stake without growth) | no | no | it is the reflex | fires once R4' is built: 1.01 to 2.6 against 0.66 | no | no | readable |
| R4' the type-pooled change (the stump rung, the default path's end) | no: s.2 names no basis | no: the cut past it that the schema offers (type by CUSIP for every type) fails the bench at 11.0 | no: the reflex past it (condition every type on the name) fails the same way | no: it wins every basis the default path builds (0.66 against 1.01 and up) | no | no | silent |
| R4b and R4c everyone moved, or everyone a stake (one rate, every manager's stake, each type's stake change, the sponsors' per-name change for everyone, the type by name grid) | no | the grid is the schema's own cut (type by CUSIP) | "condition on every visible attribute" | fires once tried: 0.91 to 11.0 | no | no | readable |
| R5 the per-name sponsor completion (decisive) | no: OM-4 names the criterion, never a basis, a stake, a float, an index weight or a share count to track | no: the type by CUSIP cut over every type fails the bench (11.0); restricting the per-name change to the sponsors is a reason about how an index fund holds, not a column, and no header proposes it | no: the reflex conditions every type on every attribute and fails, and round 3 at high effort stopped at the pooled type change | no: the bench scores only bases a solver builds and nominates nothing; the cover counts are counts and tie no candidate | no | no: a ratio per name over the filed sponsors, applied manager by manager to one type only | silent |

## Semantic fork table

One row per term of the main ask and per convention the main computation depends on, loop 2's mechanism included.
The stump is none of the readings: every row lands on the same call or is refused by the cited text. Each id is tagged
on its assertion in `generator/checks.py` (SF9 to SF13 tagged at the sites the loop 2 builder extends).

| Id | Term or convention | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "the managers that report holdings for the period" | December holdings or combination filers on file plus September holdings or combination filers with no December notice (272 and 129 in the loop 1 pack) | the 4 September notice filers counted as still due (133) | same call: a notice carries no holdings to estimate | OM-4 s.2, "A manager that files a 13F notice reports no holdings of its own" |
| SF2 | "shares outstanding" for December | the cover count with the latest as-of date on or before 31 December (the October-dated 10-Q) | the January 10-K count | same call (no flag moves, asserted) | OM-4 s.5 "on or before the report period end" |
| SF3 | what counts as a holding | SH lines without put or call | December option lines counted | same call (asserted) | OM-4 s.3 |
| SF4 | "above 80.0 per cent" | strictly above, on the unrounded estimate | at or above, or on the one-decimal figure | same call: OTF 80.39 and FENN 79.59 in the prototype, every golden variant at least 0.3 from the line (asserted) | OM-4 s.7; checks.py distance assertion |
| SF5 | "the same number of days after its end" | 34 days, so 3 November 2022 | business days, or the gap to the deadline | same call: the same 129 managers are still due in both windows | OM-4 s.2 (3 February is day 34 after 31 December) |
| SF6 | "each report taken as amended" for December | no December report is amended | an amendment applied in some order | same call: none exists (asserted zero) | the records; checks.py separation |
| SF7 | "every security in the flag file" | the twelve watchlist names, as the criterion's scope and as the pooling scope of any change | every security in the information tables | same call: the golden basis also wins the back-test scored over every security, and the sponsors' stake change pooled over every security is the same 5.5 per cent (asserted) | OM-4 s.2 |
| SF8 | the latest count on or before 31 December | the October-dated 10-Q count | a 10-Q/A for the September quarter with a later date | same call: no September-quarter 10-Q/A exists (asserted) | the records; OM-4 s.5 |
| SF9 | "shares outstanding" against which a September holding is read as a stake (the stake formulation only) | s.5's September count: the latest as-of date on or before 30 September (the August 10-Q cover; the September 10-Q/A for TAAV, OLPD and HAMR) | the first count after 30 September (the October cover); the original 10-Q count for the three names | the October cover moves OTF to about 79.4 under the stake formulation, a different call; the 10-Q count moves TAAV, OLPD and HAMR by at most 0.12, the same call; the share-ratio formulation reads no count, the same call | OM-4 s.5 "with the latest as-of date on or before the report period end" |
| SF10 | "the holdings in reports not yet filed are estimated" | share holdings at 31 December (s.3, lines in shares), divided by the s.5 count | the estimate made directly in percentage points (a stake carried and grown) | same call: ownership is shares over the same count, so the two formulations are one figure (asserted within 0.01 on every name) | same call (C1) |
| SF11 | the per-name peer set ("the change its filed peers show in that name") | the index and ETF sponsors that filed both the September and the December report by 3 February, in that name | each filed complex alone; every sponsor with a December report; the sponsors' stake change pooled over the twelve or over every security | same call: both filed complexes hold all twelve names in all three quarters and their stakes grow 5.5 per cent in every security (asserted within 0.0005 per name and 0.01 on every December figure) | same call (C1) |
| SF12 | "that period's ownership on all the reports since filed" (the back-test's target) | September ownership as amended by the cover-page period and the amendment numbers, s.3 to s.5 | any reading of the ask devices (two period sources, seven amendment orders, the line hazards, three count readings) | same selection: the golden basis keeps the smallest miss by at least 0.3 in every combination (asserted) | same call (the device hosts file every September report by 3 November, so each handling cancels) |
| SF13 | the client layout | OM-4 s.8 names layout v4 (since 45981f4), the layout file is v4, the prompt names v4 | layout v3 (OM-4 s.8 as shipped before 45981f4) | closed: no filed text names v3 as current, and the v4 header says it replaces v3 from the 2022Q4 files; the flags do not depend on the layout | OM-4 s.8 "The file layout is client flag file layout v4." |

## Oracles

- The September window (closed): the filed criterion's own bench. On the default path it confirms the type-pooled
  change against every basis the default path builds and refutes nothing the default solver did; it ties under no
  basis and nominates only bases a solver builds. Not an oracle.
- The cover-page counts: counts, no total of anything; they show each name's share-count move to anyone who reads
  them, and they tie no candidate.
- The filed sponsors' own December positions: peers' filed holdings, read by the golden and by every per-name rival
  alike; they tie nothing.
- The ask layer's referee: the 30 September price every other filer's September lines imply for each CUSIP
  (VALUE times 1,000 over SSHPRNAMT on the September reports). It dates a report's holdings to a quarter end and states
  no share level, so it arbitrates the header-period disagreement without handing over a figure.
- No summary-page totals, no published ownership figure, no prior flag file, no control total and no index
  constituent, weight or float file ship. `short_interest_20221230.csv` and `13flist2022q4.txt` (the declared
  distractors) carry no ownership figure.
- None ties only under the golden.

## Generator changes (builder brief, loop 2)

A fresh builder at medium effort builds from this commit. What does not move: OM-4 (s.8 names layout v4), the readme,
the layout v4 text, `data_sources.md`, `prompt.txt`, the watchlist, the register, the distractors, every ask device
and its role, the WATCH December targets (`A`) and September targets (`sep`), the PEND holdings of the managers still
due, the 129 still due and the population rules, every active type's dynamics (flat in aggregate, the IPF balance,
late active filers at 0.7 per cent a position, the manager-level flows), and the device hosts. Loop 1's main-call
brief (as built at `4c2bcbb`) stands except where this list changes it.

1. **Share counts (`sim.py`, the share-count block; `world.py` constants).** Keep `S_oct` (the December count) for
   every issuer. Watchlist September counts from the table's d: set `OCT_U` (September count over October count) to
   `1/d - 1` for WHII 0.970, OTF 1.046, AMRB 0.975, TAAV 1.012, JEMS 0.968, FENN 1.048, OLPD 1.015 and NOPR 0.960
   (GLI, SAF and HAMR keep their shipped values; W08's tender stays as built; the A5 names keep their mechanics:
   the September count is the 10-Q/A's `S_A5`, the original 10-Q's `S_jul = S_A5 / (1 + A5_V)`). June counts from the
   table's e: a new `APR_E` with WHII 0.985, GLI 1.050, AMRB 0.990, JEMS 0.988, SAF 0.960 and NOPR 0.980 sets
   `S_apr = S_sep / e`; every other non-A5 name keeps the shipped draw (the `rr.normal` draw is still consumed). Every
   move sits between the two cover dates that bound its window (the stories in the table). Non-watchlist covered
   securities: as built, plus about one in ten with a 3 to 8 per cent move in one window, either direction, from a new
   salted stream.
2. **Index and ETF sponsors (`sim.py`, positions), all seven complexes, every covered security.** Each complex holds a
   stake of each security fixed at the December level (as built: PEND for the late five on the watchlist, the P0 and P1
   draws, the non-watchlist splits), and its holding each quarter is that stake read against the quarter's OM-4 count,
   the stake growing 5.5 per cent a quarter (`W.GROW`, now the stake growth): with `dq = S_oct / S_sep` and
   `jq = S_sep / S_apr` per issuer, the late complexes' `s3 = v / (W.GROW * dq)`,
   `p4 = s3 * W.GROW * dq * (1 + N(0, 0.0002))`,
   `p2 = s3 / (W.GROW * jq) * (1 + N(0, 0.0002))`, and P0 and P1 likewise (`p3 = p4 / (W.GROW * dq) * (1 + N)`,
   `p2 = p3 / (W.GROW * jq) * (1 + N)`). One G for every complex, so the late complexes' stakes move exactly as the
   filed complexes' do. Nothing else in the position code changes; the IPF then hits the September and June targets
   with the new sponsor positions inside `fixed`.
3. **Golden (`golden.py`).** `window()` takes the per-name counts of both quarters and declares `sponsors_per_name` the
   golden (each sponsor still due times the filed sponsors' summed December shares over their summed September shares
   in that name; every other type by its own pooled change over the twelve). Variants: `sponsors_per_name_flat` (every
   other type flat) and `sponsors_stake` (each sponsor still due: its September shares over the s.5 September count,
   times the filed sponsors' summed December stakes over their summed September stakes across the twelve, times the
   s.5 December count; every other type flat). New rivals: `stake_sponsors` (the September stake read against the
   December count, no growth; others flat), `stake_all` (every manager still due at its September stake),
   `stake_type_pooled_all` (each type's pooled change measured in stakes, applied to each manager's stake),
   `one_rate_per_name` (the filed sponsors' change in that name for every manager still due). `type_pooled`,
   `type_allsec` and `sponsors_only` become rivals; `own_trend` becomes a rival rung (December only). `make_backtest()`
   carries every basis through `delta` as now, and recomputes the stake bases with `Ssep` when a count hazard is passed
   (a solver who reads the wrong September count reads it in the stake too). `res["dec_io"]` comes from
   `sponsors_per_name`; `res["dec_variants"]` holds the two variants; `res["rungs"]` every other basis plus own trend.
4. **Checks (`checks.py`).** `ANS` unchanged. `variants = ("sponsors_per_name", "sponsors_per_name_flat",
   "sponsors_stake")`; every other back-test key is a rival with the floors in the back-test table; the golden at
   most 0.15; the golden first by at least 0.4 points and 3x; the type-pooled family (`type_pooled`, `type_allsec`,
   `sponsors_only`) each 0.5 to 0.9 and below every other rival by at least 0.05, and `type_pooled` the smallest of
   the default path's five (`onfile`, `flat`, `all_pooled`, `all_per_name`, `type_pooled`) by at least 0.15. The
   ladder by name (`expect`): `onfile` {W01, W06}; `R1_last_quarter` {W01, W02, W06, W07, W10}; `flat`,
   `all_pooled`, `all_per_name`, `issuer_factor`, `stake_sponsors`, `type_pooled`, `type_allsec`, `sponsors_only`,
   `own_trend` {W01, W02, W06, W10}; `one_rate`, `stake_all` {W01, W02, W06, W07, W10}; `one_rate_per_name`,
   `stake_type_pooled_all`, `type_per_name` ANS plus W07; `type_mean_ratio` (FENN flagged by the active types' mean
   ratios, OTF as the build lands it), R2 and R3 as the build lands them, each asserted by name and none equal to
   ANS. Margins: `type_pooled` OTF at most 79.6; every R4 rung's OTF at most 79.7; R4b's FENN at least 80.1; R4c's
   FENN at least 80.2. The 24-cell grid of the ladder section, each cell's flags by
   name. One rate for every manager still due: FENN's crossing rate at least 3 points below OTF's, and no rate from 0
   to 20 per cent in 0.05 steps lands ANS. Sponsor dynamics (replacing the loop 1 `abs(v - 1.055)` check): the filed
   sponsors' per-name share change equals 1.055 times the name's count move within 0.0005 in both windows; their
   stake change pooled over the twelve and over every security (from the simulation's counts) within 0.0005 of 1.055;
   every other type's pooled share change 0.998 to 1.002 and never exactly 1.0000. Variants within 0.01 of the golden
   on every name with the same bins and flags, the stake change over every security included; OTF and FENN at least 0.3
   from 80.0 under every variant; every graded figure at least 0.015 inside its bin. Truth within 0.15. The SF rows:
   SF9 (the stake formulation read against the October count moves OTF under the line, refused by s.5; against the
   original 10-Q count for the A5 names, the same call), SF10 and SF11 (the formulations and the peer sets converge),
   SF12 (the robust margin), SF13 (OM-4 s.8 and the layout header both name v4). The robust margin over every device
   and count combination at least 0.3, stake bases included. The separation zero-counts, the ask assertions and the
   hygiene battery as built.
5. **Main-call snapshot.** Once the new main call is asserted and two builds are byte-identical, rewrite
   `generator/main_call_ref.json` with `python3 maincall.py target` once (the loop 1 snapshot pins the main call loop 2
   replaces), then build again and run every ask-layer check against it; write the as-built population counts into the
   ask sheet.
6. **Ask layer.** Keep every device and stop as designed. Re-run the DV-1 and DV-2 size search (`DV1_T`, `DV2_O`) on the
   new September positions and counts: every mishandled cell at least 0.06 points from the golden and in another bin on
   every touched name; the October count now moves every name by 1 to 4.8 per cent and stays in the grid. Keep the Ask A
   golden figures where the `sep` targets put them; the bridge's share figures move with the September counts and are
   recomputed; re-assert every stop range in shares and record any deviation at its as-built value, as loop 1 did.
7. **`verify.py`.** Recompute from `target/` alone the golden in both formulations (the filed sponsors' per-name change;
   the stake grown by the sponsors' stake change), the type-pooled rival and flat carry in the back-test (assert the
   per-name basis has the smallest miss and is under 0.15), the December figures and flags, and every ask figure.
8. **`make.py`.** `figures.json` replaces `type_change_sponsors_pct` with the figures block 2 states (for example the filed
   sponsors' OTF change and their change pooled across the names, both in per cent to one decimal) and writes the
   back-test figures block 3 quotes (`sponsors_per_name`, `type_pooled`, `flat`); `golden_figures.json` keeps every rung,
   variant and back-test value.
9. **`submission.md`**, through `submission-writeup`: block 1's contrast sentences (not the December reports alone; not one
   change per type across the names, which leaves OTF's sponsors short of OTF's October issue; not carry; not every
   manager moved with the name or carried at its stake, which lifts FENN); block 2 (129 still due; the filed sponsors'
   OTF change against their pooled change; the flagged names' December figures; FENN and AMRB); block 3 step 5 (the
   criterion's result) and step 6 (the per-name sponsor completion); block 4 regenerated; `figures_check.py` exit 0.
10. **Card and gates.** The card's `spine.rows` after the cut, `guard.py surface`; generator checks, `verify`, two builds
    byte-identical, the realism sweep, `leak.py`, `voice-check.py`, `precut.py`, `figures_check.py`; then `target.zip`.
    No document and not the prompt changes in loop 2, so the leak reader re-reads only if a build step changes one;
    then a fresh solver round (round 4).

## Closure table (22 axes, determinism-check; re-walked for loop 2)

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | OM-4 s.2 literally: December holdings or combination filers on file, plus September holdings or combination filers with no December notice; notice filers report none, so the September notice filers not yet in are outside (count forced literally; C1 on every figure, since a notice carries no lines) |
| 2 | Unit of account | shares (SH); put and call lines left out by PUTCALL or title of class (s.3, readme PUTCALL "as reported"); no title-only option line in the main call's rows (asserted); the estimate is in shares, and a stake formulation is converted back with the s.5 count (SF10, C1) |
| 3 | Attribution window | report period on the cover page, not the drop; filed (readme: data sets by submission date). Asks: one bank trust's September restatement carries 30 June in its submission header and 30 September on its cover page; the cover page governs (the form's own statement, its holdings priced at the 30 September close the referee implies); every reading enumerated in the ask sheet; the main call converges under both (asserted: its rows are untouched and the back-test cancels) |
| 4 | As-of dating | count with the latest as-of date on or before the period end (s.5), now load-bearing twice: as every period's denominator and as the count a stake formulation reads (SF9); every share-count move sits between the two cover dates bounding its window, and the index sponsors' holdings track exactly the s.5 counts (simulation, asserted through the per-name change); the January 10-K count moves no flag (asserted); A5's amended count is a June-quarter report dated in September, never the latest on or before 31 December (asserted: no 10-Q/A for the September quarter) |
| 5 | Version basis | report as amended, by cover-page type, in filing order with the amendment number ordering amendments filed the same day; no amendment of any kind in the main call's rows (asserted); every September amendment that moves shares is a bank trust's, filed by 3 November, and the one filed in January adds option lines only |
| 6 | Denominator | cover-page count (s.5); filed; the share-count moves are the issuers' own counts |
| 7 | Weighting | ownership is a share of shares; the golden's per-name change is a ratio of the filed sponsors' summed shares in that name, its stake formulation a ratio of their summed stakes across the names; both converge (C1, within 0.01); the share change pooled across the names, the mean of per-manager ratios and the type by name grid are rivals the criterion rejects |
| 8 | Window length | fixed by s.2: the previous period at the same number of days after its end as the reports in hand (34, so 3 November 2022), completing from June; one window, filed |
| 9 | Boundary inclusivity | "above 80.0"; nearest names OTF 80.4 and FENN 79.6 under every golden variant (at least 0.3 away, asserted) |
| 10 | Rounding path | flag on the unrounded estimate; every one-decimal figure at least 0.015 inside its bin under every golden variant (asserted) |
| 11 | Tie-break | golden variants that tie under the criterion converge on every live figure (C1: the per-name change with the other types flat or pooled, the stake grown by the stake change over the twelve or every security, either filed complex alone); same-day amendments are ordered by amendment number, the only order the records carry (C1 on the asks: the restatement numbered 2 contains every share the amendment numbered 1 adds, asserted); no top holder is graded |
| 12 | Maturity and censoring | the decisive axis: the December period is open; s.2 files the estimate and the criterion; C2 confirmation: the golden basis at the noise floor (prototype 0.04, the late active filers' own position moves) against 0.66 to 26.6 for the eighteen rivals in the back-test table, every rival's miss asserted; no basis can beat the floor without the unfiled reports, so any basis the criterion could prefer converges on the golden's sponsor treatment |
| 13 | Order of operations | the per-name change multiplies each sponsor's September position, so per manager or per name before summing gives the same figure; the stake formulation divides each manager's September shares by the September count, applies the stake change and multiplies by the December count, an identity with the per-name share change when every complex's stake grows alike (asserted within 0.01) |
| 14 | Row order | sums; order-free |
| 15 | Duplicate resolution | lines per position summed (s.3); split lines (Tregaron) sum to the position |
| 16 | Identity normalisation | CUSIP per s.4; no repaired or failing CUSIP in the main call's rows (asserted); every failing check digit sits on a bank trust's September line; issuer stems are unique across every covered issuer, so "exactly one covered security fits" holds under either reading of "covered" (C1) |
| 17 | Netting | none |
| 18 | Dimensional units | no graded figure reads VALUE; the referee reads September VALUE in thousands (every September filing predates 3 January 2023) only to date a report's holdings; Wexley's December note is texture |
| 19 | Code semantics | PUTCALL and TITLEOFCLASS (s.3, readme); REPORTTYPE (notice reports none, s.2); ISAMENDMENT, AMENDMENTNO and AMENDMENTTYPE from the cover page; `manager_type` from the register (read for the population's types by every completion rung); no SUBMISSIONTYPE disagrees with its cover page |
| 20 | Integerisation | whole shares as filed; the estimate is a real number of shares and the flag is set on it; no estimated share count is graded |
| 21 | Scope of a clause | s.2's estimate clause governs flag files issued before the deadline, which this one is (8 February against 14 February); "every security in the flag file" is the twelve, and the alternative scope gives the same selection and the same stake change (SF7, asserted) |
| 22 | Forward window contents | the managers still due are every September holdings or combination filer with nothing for December (literal); nobody stops filing in either window (asserted), so no due manager is a non-reporter in disguise; no share-count move falls after the October cover dates, so the December window holds no count change the s.5 count cannot see |

## Ask sheet and device ledger (loop 1 ask layer, rebuilt after round 2, kept in loop 2)

**Loop 2 (2026-10-12).** The ask layer keeps its design: Ask A and Ask B, DV-1 to DV-3, the hazards, the referee,
the stops and the cracker sheet. Two things move under it. Every index sponsor's September position is now its stake
read against the September count, and the September counts move on eight names (the ladder's share-count table), so
the bridge's share figures and the device hosts' positions in shares move with them, while the Ask A golden figures
stay at the `sep` targets. And the October-dated count, a hazard on Ask A's denominator, now sits 1 to 4.8 per cent
from the September count on every name. The builder re-runs the DV-1 and DV-2 size search and every stop and grid
assertion on the new positions (Generator changes, item 6) and writes the as-built values into this sheet; the
figures below are loop 1's as built until then. The cracker (now landing the per-name sponsor completion) and the
mirror (now the type-pooled response) stand on the same stops, because no ask reads the estimate. Loop 2's mirror
keeps eleven of twelve flags and about three of the twelve December figures (prototype: GLI, FENN, HAMR), against one
of twelve for loop 1's flat-carry mirror, because the December-window count moves spread the type-pooled error over
every name.

**What died and why** (supplemental-stumping Part 4). Round 2 missed the call at R4 and kept every ask
figure: each device (A1 to A5, the rename, Wexley's units, the split lines, the affiliates) was a work order
an OM-4 clause, a readme row, a layout pin or a cover-page note adjudicates. The December share counts and
the top holder carry no device at all that the main call's separation and the literal rules leave room for
(December twelve-name lines must stay clean; VALUE is fixed by the readme's filing-date rule and OM-4 s.6;
the holder's name needs a pin to be determinate), so they leave the deliverable. What stays graded is the
September figure the filed criterion is run against, per name and as the client's tie-out to the SEC's
files, now carried by two devices no filed sentence speaks to.

**The main call's declared row population** (zero device rows and zero hazard rows inside it, asserted with
the counts written here by the builder; loop 1 as built: 2,337 December lines for the twelve CUSIPs, 353
September lines of the managers still due, 58,981 June, September and December lines of the peers whose type
changes are applied, all clean):
- December reports accepted by 3 February 2023: SH lines with no put or call for the twelve CUSIPs as
  written; columns CUSIP, SSHPRNAMT, SSHPRNAMTTYPE, PUTCALL, TITLEOFCLASS; submission and cover rows (CIK,
  period, filing date, report type, amendment fields).
- September reports, as amended, of the managers still due: the same lines and columns.
- September and December reports of the filed managers of every register type with a manager still due
  (index and ETF sponsors, multi-strategy, long-only, registered advisers, pension and insurance): the same
  columns, every security (for the all-securities variant).
- The register's `cik` and `manager_type` for those five types; the cover counts dated on or before 31
  December.
- The back-test's selection is not a row population: it is asserted robust under every device handling.

Every ask device sits on a bank trust department's September report, its amendments and their submission
header rows, a September-period amendment filed in January that adds option lines only, or a cover count
dated in September or October. Bank trusts never have a manager still due and their type change is never
applied; every September amendment that moves shares is filed by 3 November 2022, so its handling enters the
day-34 estimate and the final September figure alike and cancels in the back-test.

**The deliverables.** `crowded_flags_2022q4.csv` in the client's layout v4 (exact text for
`client_flag_file_layout.md`, replacing v3):

> # Client flag file layout, v4
>
> Owner: client services. In use from the 2022Q4 files; replaces v3, in use from the 2021Q2 files.
>
> One CSV per report period and watchlist, UTF-8, comma-separated, header row, one row per watchlist
> security in watchlist sequence.
>
> | Column | Content |
> |---|---|
> | `report_period` | Report period end, YYYY-MM-DD |
> | `cusip` | Nine-character CUSIP from the watchlist |
> | `ticker` | Ticker from the watchlist |
> | `inst_own_pct` | Institutional ownership for the report period, per cent |
> | `crowded` | `Y` or `N` |
> | `prior_inst_own_pct` | Institutional ownership for the previous report period, per cent |
>
> Changes from v3: the share-count and holder columns are dropped; the client takes share counts and
> holder detail from its own vendor feeds. Rows for securities with no institutional holders carry `0.0`
> and `N`.

`sep_quarter_bridge.png`: the September waterfall, twelve names combined, start, put and call lines, lines
in reports replaced by a later amendment, CUSIPs keyed off-format and matched back, end, each bar labelled in
whole shares, the title naming the gap between the two totals in millions of shares.

**Criteria arithmetic** (shape 03 inside a twelve-row file): 12 flags and 12 December ownership figures
(the call and its critical components) · 12 September ownership figures (Ask A) · the bridge's start, three
items and end, and its title (Ask B, 6) · two chart parts (one bar per item, every bar labelled in shares) ·
two files. About 46 criteria, of which about 20 are ask criteria.

**The asks.**

| Ask | Figures | Construction | Primary device | Hazards | Files on the causal path | Columns (15 or fewer named) | Named use | H18 home |
|---|---|---|---|---|---|---|---|---|
| A | September institutional ownership per name, per cent, one decimal (12) | OM-4 s.2 to s.5 on every report for the quarter ended 30 September, each as amended | DV-1 same-day amendments (D2, version) | DV-2 header period (D7), A2 and title variants (D3), A3 and keyed CUSIPs (D7), A5 and October counts (D8) | 8: `form13f_2022q4/` SUBMISSION, COVERPAGE, INFOTABLE; `fsds_cover_extract/` sub, num; the watchlist; the readme; OM-4 | ACCESSION_NUMBER, FILING_DATE, PERIODOFREPORT, CIK; REPORTCALENDARORQUARTER, AMENDMENTNO, AMENDMENTTYPE, REPORTTYPE; CUSIP, SSHPRNAMT, PUTCALL, TITLEOFCLASS; num ddate, value; Issuer CIK | the client sets December's flag against September's restated figure (the September file it holds went out on an estimate) | the target the filed criterion selects the basis against (OM-4 s.2, "that period's ownership on all the reports since filed"), audited per name |
| B | the September bridge, twelve names combined, whole shares: start, three items, end, and the title's gap (6) | September-period information-table lines carrying a watchlist CUSIP as written, walked to the September institutional shares of Ask A | DV-2 header period (D7, key in another field) | DV-1 (D2), DV-3 options added in January (D5), A2 (D3), A3 and keyed CUSIPs (D7) | 9: `form13f_2022q4/` and `edgar13f_daily_20230103_20230203/` SUBMISSION, COVERPAGE, INFOTABLE (6); the watchlist; the readme; OM-4 | ACCESSION_NUMBER, FILING_DATE, PERIODOFREPORT, CIK; REPORTCALENDARORQUARTER, ISAMENDMENT, AMENDMENTNO, AMENDMENTTYPE; CUSIP, SSHPRNAMT, PUTCALL, TITLEOFCLASS, NAMEOFISSUER; watchlist CUSIP | the client ties our September figures to the SEC's own files (they asked) | a reconciliation of the criterion's target to another system's total (the SEC data sets' lines), the gap made of the devices |

Both asks are decoupled from the call: neither reads the estimate, the type change or any December line, so
the response that lands the call and the one at flat carry stand identically on them. Neither is a split or
a sensitivity of the committed figure.

**Device ledger** (hosts are bank trust departments that file every September report and amendment that
moves shares by 3 November 2022; the golden handling reproduces each host's simulated September position
exactly, so the golden September figures, the back-test and every rung are unchanged):

- **DV-1, primary of Ask A: two amendments to one report filed the same day (D2, the version of record).**
  Host: the loop-0 new-holdings host (2.0 to 3.0 per cent of every name). Its original (13F-HR, about 14
  October) leaves out a second trust account's positions in all twelve names (the trust account holds 25 to
  30 per cent of each position, 0.5 to 0.9 per cent of each name's September count). On one day (31
  October) it files amendment 1, a NEW HOLDINGS amendment adding the trust account (one line per name), and
  amendment 2, a RESTATEMENT of the whole report with each name's position on one merged line (own plus
  trust account, equal to the simulated position). The two go through different filing agents, so the
  restatement's accession number sorts before the new holdings amendment's, and the data set lists them in
  that order. Root cause: the department's compliance team filed the new holdings amendment, then the
  custodian's agent filed a clean full restatement the same afternoon; EDGAR dates both to the day and the
  data set carries no time. Correct handling, forced by the records: amendment 2 after amendment 1 (the only
  order the records give), and amendment 2's merged lines equal the original's lines plus amendment 1's line
  for every name, exactly. No filed sentence orders same-day amendments; the readme's AMENDMENTTYPE row says
  what each type does, not in which order. Silent: four accessions, unique keys, every join holds, nothing to
  tie; same-day filings by one manager, other amendment chains and both agents occur elsewhere in the drop,
  so no column isolates the pair. Moves: Ask A on every name; Ask B's superseded bar and end.
- **DV-2, primary of Ask B: a restatement whose submission header carries the previous quarter (D7, the
  true key in another field).** Host: the loop-0 restatement host (1.6 to 2.6 per cent of every name). Its
  original (13F-HR, about 7 October) overstates every twelve-name position by 22 to 28 per cent (a
  terminated custody account left in the run); its RESTATEMENT (13F-HR/A, about 28 October, AMENDMENTNO 1)
  restates every position at the simulated figure, adds four to six call and put lines on twelve-name
  CUSIPs that the original left out (PUTCALL filled, 0.25 to 0.40 million shares in all) and keys three or
  four twelve-name CUSIPs off-format (leading zeros dropped, one lower case; 0.6 million shares or more).
  The restatement's cover page reads REPORTCALENDARORQUARTER 30-SEP-2022; its SUBMISSION row reads
  PERIODOFREPORT 30-JUN-2022. Root cause: the agent reused the June submission template for the header; EDGAR
  takes the header period into SUBMISSION and the form's cover page into COVERPAGE as filed. Correct handling,
  forced by the records: the cover page's period (the form's own statement), confirmed by the referee (the
  restatement's holdings are priced at the 30 September close; the host's June report, filed in August, is
  priced at 30 June and is a separate original). No filed sentence says which field carries a report's
  period. Silent: on the header reading the restatement is an ordinary June amendment to an existing June
  original and the September original stands as a complete, valid report; every key joins; only a
  SUBMISSION against COVERPAGE comparison shows it. Moves: Ask B's start, put-and-call bar, superseded bar,
  CUSIP bar and end; Ask A on every name. The main call is untouched under both readings (asserted: on the
  header reading the September original is on file at day 34 and in the final figure alike).
- **DV-3, hazard (D5, a September report's lines outside the September filing quarter's drop).** Host: a
  bank trust department (a new role) whose September report kept option positions confidential; on about 17
  January 2023 it files a NEW HOLDINGS amendment with CONFDENIEDEXPIRED Y adding three to five call and put
  lines on twelve-name CUSIPs (0.15 million shares or more), values in dollars. It sits in the nightly
  build. No SH line moves, so the back-test and Ask A are untouched. Adjudicated by the readme and
  `data_sources.md` (drops by submission date), so a hazard only. Moves: Ask B's start and put-and-call bar
  for a solver who reads September from `form13f_2022q4/` alone.
- **Hazards kept from loop 1** (adjudicated by OM-4 s.3 to s.5 or the readme, so they stop a careless
  solver and not a careful one): A2 options keyed only in the title (D3), the title variants (D3), A3
  failed check digits under abbreviated names and the keyed CUSIPs (D7), A5 the June-quarter 10-Q/A count
  dated in September and the October-dated counts (D8, Ask A's denominator). As-built single deltas, loop 1:
  A2 kept GLI +1.28, TAAV +0.80, OLPD +0.61, HAMR +0.45 (bridge end +2,096,500); COM-only WHII -0.50, FENN
  -0.49, SAF -0.44 (end -856,986); A3 exact WHII -0.83, AMRB -0.22, JEMS -0.58, ABBB -0.39, SAF -0.55, NOPR
  -0.53 (end -1,560,404); keyed exact OTF -0.41, AMRB -0.50, OLPD -0.30, NOPR -0.52 (end -948,452); the
  10-Q's own count TAAV +1.62, OLPD +1.78, HAMR +0.82; the October count +0.40 to +3.39 on every name.
- **Retired as primaries, kept as texture:** the loop-0 misfiled restatement becomes a plain 13F-HR/A
  (its SUBMISSIONTYPE disagreement would teach a solver to read the cover page, which is DV-2's antidote);
  the top holder's rename, Wexley's December thousands, Tregaron's split lines and the Shelby affiliates
  stay in the pack and are graded nowhere.

**Stops** (targets; the builder lands its own values, asserts each, and every stop sits outside the
golden's bin: at least 0.06 points from it and in another one-decimal bin on every name for Ask A, and for
Ask B more than 0.5 per cent of the golden bar and not equal to it):

| Ask | Stop | Handling | Moves (targets) |
|---|---|---|---|
| A | S1 natural careful | period from SUBMISSION, amendments in the file's order, every OM-4 rule | +0.85 to +1.6 points on every name (DV-1 and DV-2 together) |
| A | S2 | cover-page period, file order | +0.5 to +0.9 on every name (trust account counted twice) |
| A | S3 | SUBMISSION period, amendment-number order | +0.35 to +0.7 on every name (the overstated original stands) |
| A | S4 over-cleaner | the latest accession per manager and period wins | the DV-1 host keeps only the trust account, -1.4 to -2.3 on every name |
| A | S5 | cover-page period, amendment-number order | golden |
| B | S1 natural careful | period from SUBMISSION, file order | start lower by the restatement's as-written watchlist lines (about 15 to 17 million); options lower by the restatement's option lines; superseded lower by the overstated original and by amendment 1; CUSIPs lower by the restatement's keyed lines; end higher by the trust account and the overstatement (about 7.5 to 11 million) |
| B | S2 | cover-page period, file order | superseded lower and end higher by the trust account (3.9 to 6.9 million) |
| B | S3 | SUBMISSION period, amendment-number order | start, options, superseded, CUSIPs and end as S1 less the trust account's part |
| B | S4 | September read from `form13f_2022q4/` alone | start and options lower by DV-3's lines |
| B | S5 | cover-page period, amendment-number order, every drop | golden |

**Hazard table** (per-ask movement when the hazard alone is mishandled; targets): DV-2 on Ask A +0.35 to
+0.7 on every name; DV-1 on Ask B end +3.9 to +6.9 million and superseded by the same; DV-3 on Ask B start
and options by 0.15 million or more; A2 on Ask A (four names) and Ask B (options bar and end, 2.1 million);
A3 and keyed CUSIPs on Ask A (eight names) and Ask B (CUSIP bar and end, 0.95 to 2.5 million); A5 and the
October counts on Ask A only. Every subset of mishandlings leaves every touched Ask A figure at least 0.06
from the golden and the Ask B end at least 3.0 million shares from it (asserted over the full grid).

**As built (builder, ask layer, 2026-10-11; generator 26,221 checks green, verifier recomputes every ask
figure and every stop, two builds byte-identical).** Main call: `generator/main_call_ref.json` is the snapshot
of the 4c2bcbb pack (every main-call figure, the flags, the back-test, every rung and variant, and sha256
digests of the declared population on its declared columns: 2,337 December twelve-name lines, 353 September
lines of the 129 managers still due, 58,981 peer lines, 862 filing rows, 313 register rows, 747 counts);
`checks.py` asserts the build reproduces all of it exactly, and the separation counts are zero (December
device rows, December amendments, title options, due-manager amendments and device rows, peer amendments,
device rows and option rows, amendments inside the population, header-period disagreements inside it).
Back-test margin under every reading (two period sources, seven amendment orders) and every hazard and count
combination: 0.418 at worst (asserted 0.3). Sizes: DV-1 trust account 25 to 30 per cent of the position on
every name; DV-2 overstatement 22 to 28 per cent on eleven names and 19 per cent on SAF (the search found no
value inside the range clearing 0.06 points on SAF in every cell). Ask A golden unchanged (85.1, 81.7, 78.8,
74.1, 75.4, 81.8, 81.6, 59.8, 69.7, 88.9, 49.1, 65.5). Ask A stops, points from the golden by name (WHII to
NOPR): S1 +1.41 +1.22 +1.26 +1.32 +1.12 +1.16 +1.33 +1.25 +1.30 +1.10 +1.01 +1.35; S2 +0.75 +0.69 +0.74
+0.70 +0.61 +0.65 +0.72 +0.77 +0.89 +0.76 +0.55 +0.71; S3 +0.66 +0.53 +0.52 +0.62 +0.52 +0.51 +0.60 +0.47
+0.41 +0.34 +0.46 +0.64; S4 -2.18 -1.66 -1.79 -1.82 -1.48 -1.65 -1.85 -1.85 -2.07 -2.21 -1.62 -2.18 (the
over-cleaner also drops DV-3's host, whose latest September accession is the January option amendment). Grid:
2,012 mishandled cells, every touched name at least 0.067 from the golden and in another bin. Ask B golden:
start 598,531,990; put and call lines -8,203,900; lines in reports replaced by a later amendment -50,938,469
(the three ordinary same-day re-filings' originals among them); CUSIPs keyed off-format, matched back
+6,452,942; end 545,842,563; gap 52.7 million. Ask B stops against the golden: S1 start -12,515,399, options
-301,000, superseded -25,509,742, CUSIPs -3,944,086, end +9,351,257; S2 superseded -5,277,437, end
+5,277,437; S3 start -12,515,399, options -301,000, superseded -20,232,305, CUSIPs -3,944,086, end
+4,073,820; S4 start and options -187,000. Single deltas (natural read): DV-1 file order Ask A +0.55 to
+0.89 on every name, Ask B end +5,277,437; DV-2 header period Ask A +0.34 to +0.66 on every name, Ask B as
S3; DV-3 Ask B start and options -187,000, Ask A untouched; the filed-after reading converges on the golden
(asserted). Deviations from the targets above, each asserted at its as-built value: S3 on SAF +0.34 (target
+0.35); S4 of Ask B moves the start by 187,000 shares, 0.03 per cent of the start bar, not more than 0.5 per
cent (asserted at 150,000 or more; a 0.5 per cent move would need about 3 million shares of options from one
department); the full-grid end floor of 3.0 million is met by every stop but not by every hazard subset (A2
kept alone moves the end 2.1 million; with DV-1 or DV-2 mishandled beside the negative hazards the end comes
within 12,431 shares at the closest, the original-alone reading with A2 kept and A3 exact), so the grid
asserts every mishandled cell's end differs from the golden and records the minimum. Referee: 2,485 September
twelve-name lines worth 200 thousand dollars or more, every implied price within 0.24 per cent of its CUSIP's
median, DV-2's restatement among them; the June and September closes more than 2 per cent apart on all
twelve names. The three ordinary same-day pairs are September re-filings in full by three bank trust
departments through the two agents, not June amendments (Tried and rejected).

**Referee.** The 30 September price each CUSIP's other September filers imply (VALUE times 1,000 over
SSHPRNAMT on the September reports). It arbitrates DV-2's disagreement (the restatement's holdings sit at
the September close; the host's June original sits at the June close) and states no share level. It is
byte-clean: every September line is in thousands, filed before 3 January 2023, and no device touches a
value. Nothing else in the pack ties under one handling only.

**Cracker sheet.** The response that lands the call (the per-name sponsor completion), runs the battery
(key uniqueness, exact duplicates, unmatched joins, fan-out, counts that tie), executes every filed rule
(OM-4 s.2 to s.7, the readme's amendment types and value units, the layout v4) and so clears A2, the title
variants, A3, the keyed CUSIPs, A5, the October counts and DV-3, and takes the two choices no filed rule
makes the way its pipeline is built: the period from the SUBMISSION table it lists filings from, and
amendments in the order the data set lists them.

| Row | Golden | Cracker's figure (stop S1) | Distance | Cracker verdict |
|---|---|---|---|---|
| Ask A, September ownership, each of the 12 names | the golden September ownership (loop 1: 85.1, 81.7, 78.8, 74.1, 75.4, 81.8, 81.6, 59.8, 69.7, 88.9, 49.1, 65.5) | golden plus the trust account plus the overstatement | +0.85 to +1.6 points, every name in another bin | miss |
| Ask B start | golden start | less the restatement's as-written watchlist lines | about 15 to 17 million shares | miss |
| Ask B put and call lines | golden options bar | less the restatement's option lines | 0.25 to 0.40 million | miss |
| Ask B lines in reports replaced by a later amendment | golden superseded bar | less the overstated original and amendment 1 | about 24 to 28 million | miss |
| Ask B CUSIPs keyed off-format, matched back | golden CUSIP bar | less the restatement's keyed lines | 0.6 million or more | miss |
| Ask B end, September institutional shares | the golden end (545,842,563 in loop 1; recomputed in loop 2) | plus the trust account and the overstatement | about 7.5 to 11 million | miss |
| Ask B title, the gap between the totals | golden gap in millions | start lower and end higher | 20 million or more | miss |

**Mirror sheet.** The response at the type-pooled change (R4', loop 2's stump rung) runs the same pipeline and
stands on every ask row exactly where the cracker stands, because no ask reads the estimate; the two sheets differ
only in the recommendation criteria. A response that clears DV-1 alone keeps Ask B's start, options and CUSIP bars
and nothing of Ask A; one that clears DV-2 alone keeps those three bars and nothing else; only both clear both.

**Pair ceiling:** 35.0 on paper (loop 2), planning weights 38 / 7 / 55 and about 20 ask criteria at 2.75 each. The
cracker keeps the recommendation block, instruction following and the two chart parts: 38 + 7 + 5.5 = 50.5.
The mirror, now the type-pooled response, keeps about 7 of the recommendation block (eleven of twelve flags and
three of the twelve December figures, GLI, FENN and HAMR in the prototype), instruction following and the two chart
parts: 7 + 7 + 5.5 = 19.5. (50.5 + 19.5) / 2 = 35.0 (loop 1's flat-carry mirror gave 34.0). Stated plainly: the bar rests
on the main ladder keeping at least one of the top two off the call and on DV-1 and DV-2 each stopping a
careful solver; a response that clears both devices keeps every ask figure (a cracker that does reaches
100), and each device is a convention a careful solver picks without a rule, so the round measures how
often. If the generated rubric files the twelve December ownership figures as asks rather than critical
components, the pair rises to about 44; the writer files them as critical components (submission-writeup).

**Ask-level determinism** (supplemental-stumping Part 3; every reading computed by the generator and the
verifier):

- DV-1 orders: amendment number (golden); file or accession order (S1, S2); the latest restatement plus every
  new holdings amendment filed on or after its date (= S2); the same with "filed after" (converges on the
  golden); the latest accession wins (S4); every version summed (2 x the position); the original alone
  (position less the trust account). Pinned by the records: the amendment numbers, and amendment 2's merged
  lines equal to the original's plus amendment 1's on every name.
- DV-2 readings: the cover page's period (golden); the submission header's period (S1, S3). Pinned by the
  records: the form's cover page, the September-close pricing the referee shows, the host's separate June
  original filed in August. Neither field description says it governs the other.
- DV-3 readings: every drop (golden); the September filing quarter's drop alone (S4 on Ask B). Pinned by the
  readme and `data_sources.md` (drops by submission date).
- No filed sentence, read literally, gives another Ask A figure or another bridge: OM-4 s.2 to s.5, the
  readme's AMENDMENTTYPE and VALUE rows and the layout v4 are executed word for word on the golden path.
- Every golden Ask A figure sits at least 0.015 inside its one-decimal bin (loop 1 as built, unchanged); the
  bridge figures are whole shares, exact.

**Main-call invariance** (asserted in `checks.py` against the committed `generator/golden_figures.json` of
loop 1 at `4c2bcbb`): `dec_io`, `sep_io`, `jun_io`, `rungs`, `variants`, `type_change`,
`type_change_allsec`, `type_change_sep_window`, `dec_onfile_shares` and `backtest` identical; the flags
identical; the declared population's rows identical on their declared columns; the criterion keeps the
golden basis first by at least 0.3 points under every combination of DV-1 (seven orders), DV-2 (two
readings), DV-3 (two), A2 (two), the title variants (two), A3 (three), the keyed CUSIPs (two) and the counts
(three). The separation zero-counts are written into this sheet by the builder. Loop 2 replaces the main call: the
builder re-snapshots `main_call_ref.json` once the loop 2 main call is asserted (Generator changes, item 5), and the
invariance then pins the loop 2 main call while the ask layer is re-tuned.

**Loop 1 ask-layer builder instructions** (done at `a78cb74` and kept as the record of how the layer was built; the
loop 2 builder follows Generator changes, which moves the main call and keeps this layer):

1. `docs.py`: `layout()` writes the v4 text above verbatim; nothing else in `docs.py` changes (OM-4 and the
   readme stay byte-identical).
2. `sim.py`: DV-1 on the loop-0 new-holdings host (the original omits the trust account in all twelve names;
   amendments 1 and 2 on 31 October through two filing agents, the restatement's accession sorting first,
   the restatement one merged line per name); DV-2 on the loop-0 restatement host (the original overstates
   every twelve-name position by 22 to 28 per cent, the restatement on about 28 October adds four to six
   option lines and keys three or four twelve-name CUSIPs off-format); DV-3 on a new bank-trust role (a
   January NEW HOLDINGS amendment with CONFDENIEDEXPIRED Y adding option lines only); the loop-0 misfiled
   restatement filed as a plain 13F-HR/A; A2, the title variants, A3, the keyed CUSIPs, A5 and the October
   counts as they are. Every simulated position stays as it is. Device randomness comes from new salted
   streams, and device filings take accession numbers and surrogate keys from their own streams, so every
   other row keeps its bytes where the writer allows; sizes come from a deterministic search for the
   separations above.
3. `pack.py`: DV-2's SUBMISSION row carries PERIODOFREPORT 30-JUN-2022 and its COVERPAGE row
   REPORTCALENDARORQUARTER 30-SEP-2022; DV-3's cover page carries CONFDENIEDEXPIRED Y and its dates;
   ADDITIONALINFORMATION as in the OM-4 section's other filed text. Add at least three ordinary same-day
   filing pairs by one manager elsewhere (for example a June amendment and a September original on one day)
   and keep both filing agents active across the drop, so the device pair is blended.
4. `golden.py`: the period from REPORTCALENDARORQUARTER (as now); amendments in filing order with AMENDMENTNO
   ordering filings of one day (the loop-1 sort by accession is the S2 stop and must go); Ask A is `sep_io`;
   Ask B is the bridge over September-period reports from every drop; compute every stop in the stop table
   explicitly; the December and September counts and the top holder leave the deliverable (counts stay in
   the main call's computation).
5. `deliver.py`: the flag file in layout v4 (`report_period`, `cusip`, `ticker`, `inst_own_pct`, `crowded`,
   `prior_inst_own_pct`); the bridge PNG as now with the third bar named "Lines in reports replaced by a later
   amendment" and the title on the gap.
6. `checks.py`: the main-call invariance list above; every stop and every grid cell outside the bin (Ask A at
   least 0.06 and another one-decimal bin on every name; Ask B more than 0.5 per cent of each golden bar and
   the end at least 3.0 million shares away); the cracker's and the mirror's stops equal on every ask figure;
   the lazy sweep (S1) and the over-cleaner (S4) on their designed values; the hygiene battery clean on S1
   (unique keys per drop, every SUBMISSION row joins its COVERPAGE row, CIK, period and AMENDMENTNO unique
   under both period readings, no exact duplicate line within an accession); the referee: every September
   twelve-name line's implied price within 0.5 per cent of the CUSIP's median, DV-2's restatement among them;
   the separation zero-counts; keep the SF1 to SF8 tags.
7. `verify.py`: recompute Ask A and the bridge from `target/` alone with the same conventions and compare with
   the goldens.
8. `submission.md` through `submission-writeup`: block 4 by file (the flag file per name: December ownership,
   flag, September ownership; the bridge: the five figures and the gap); the twelve December ownership
   figures stay critical components; `figures.json` and `figures_check.py`.
9. `metadata.json`: `prompt_shape` without the top holder; deliverables and distractors unchanged. The card:
   `layer1` loses the misfiled restatement and gains the same-day amendments, the header-period slip and the
   January confidential-treatment amendment; `guard.py validate` and `heart`.
10. Two builds byte-identical, the realism sweep, `leak.py`, `voice-check.py`, `precut.py`, then `target.zip`.

## Input gates

As shipped plus the Q1 cover counts: 19 files, 7 formats (csv, htm, md, pdf, tsv, txt, xlsx), largest
`form13f_2022q4/INFOTABLE.tsv` (about 39,000 rows). Distractors (in `metadata.json` only): the short
interest file and the 13(f) list. The loop 1 ask layer adds no file: `client_flag_file_layout.md` carries
the v4 text, DV-1 and DV-2 sit in `form13f_2022q4/`, DV-3 in the nightly build. Loop 2 adds no file and changes no document.

## Realism debts

- Index and ETF sponsors' stakes grow 5.5 per cent a quarter in every name and every complex (creations), the pace of
  the fast-growing ETF complexes in 2022 rather than the industry's 2 to 3; kept from loop 1 because the register-type
  signal it gives is what draws the default path to the type-pooled change, and a lower rate makes the stake without
  growth the closest rival (Tried and rejected). One rate for the early and the late complexes alike.
- Every sponsor's holdings track the s.5 counts exactly: the index providers' quarterly share updates take the latest
  cover count, and every share-count move sits between the two cover dates bounding its window. No index-provider
  share or float file ships; the issuers' cover counts are the only record of the moves.
- The watchlist's share-count moves: OTF's October follow-on (4.6 per cent), FENN's shares issued for an acquisition
  (4.8), ABBB's September tender (5.4 down), GLI's July follow-on (5.0), SAF's July modified Dutch tender (4.0 down),
  at-the-market issuance at TAAV and OLPD after their August offerings, buybacks at WHII, AMRB, JEMS, NOPR and SAF; a
  busy year for mid-cap capital actions (2022 was a record buyback year), every one in the issuer's own cover counts.
  About one in ten other covered securities carries a 3 to 8 per cent move as texture.
- OTF is index-heavy (about 40 per cent of its shares with sponsors, 23 of it with the late five), a mid-cap in
  several indexes; FENN is fund-heavy (16 per cent with funds still due).
- Every active type is flat in aggregate quarter to quarter (within 0.2 per cent); forced so the golden's
  variants converge on one-decimal figures. Individual positions turn over normally and names move.
- Late active filers' positions move about 0.7 per cent a quarter; forced so the golden's back-test miss sits at the
  noise floor (about 0.04 points).
- Nobody stops filing in either window.
- Active managers' books move by a manager-level flow each quarter (multi-strategy 25 per cent, long-only 15,
  advisers 18, one standard deviation) on top of position turnover; forced so the mean of per-manager ratios
  sits away from the pooled change. The type aggregates stay flat by construction.
- HAMR is the balancing name for the September type totals: 49.1 in September against 55.2 in December, an
  accumulation of about 6 points by managers already on file.
- DV-1: one department filing a new holdings amendment and a full restatement of the same report on one day
  through two agents is uncommon but real; the restatement's merged lines (own plus trust account) keep the
  pair from showing as duplicate lines.
- DV-2: a header period that disagrees with the form's cover page is a filing-agent template slip the SEC
  data sets carry as filed; one such filing in the quarter.
- The client's move to a six-column layout v4 for the 2022Q4 files (share counts and holder detail from its
  own vendor feeds) is a client-side change the pack records once, in the layout's own header.

## Stopping rule

Loop 2 is the second of three hardening loops for architecture 1 (CLAUDE.md: three loops per architecture, then
re-root). A round that lands the call by the per-name sponsor completion, or its stake formulation, sends the build to
loop 3 with the decisive step moved again by the data's own structure, never by a filed sentence; a third landing files
architecture 1 as solved and the slot re-roots in the same objective and number. A round that stops at R4' or any R4
rung passes the ladder gate. A round that lands R0 means s.2's estimate clause was missed: read it as a leak-reader
question on the clause's prominence, never as a reason to name the basis. Ask layer: a round that misses the call and
reads ASKS LEAK means a solver cleared both DV-1 and DV-2; the next repair moves the layer's weight (a third silent
device on a new quantity), never a filed sentence or a marker, and a second leak after that files the ask layer as at
its ceiling for this world.

## Pre-ship check (client two-layer standard)

- Domain: institutional ownership analytics from 13F, completing a quarter still inside its filing window by
  what each kind of filer holds: an index sponsor a slice of each company's float, an active manager a share count;
  the float tracking, the creation mechanism and the 45-day window break the swap test.
- Layer 1: amendments (two filed the same day, one with a header period that disagrees with its cover page,
  one adding options in January after confidential treatment ended), title-of-class options, keyed and failed
  CUSIPs under abbreviated names, value units by filing date, counts dated either side of a period end and an
  amended count, split lines, affiliates, a rename; all real 13F and EDGAR behaviour, none planted, none on the main
  call's rows (asserted).
- Decisive step: a methodological choice, the completion basis, selected by a filed criterion the data
  settles; not a planted catch, not a field reading, not a stated rule applied (no filed sentence names a basis, a
  stake or float tracking).
- Analyst test: a strong analyst who conforms every line and reads OM-4 literally pools each type's change across the
  names (or carries the managers still due, or moves everyone with the name) and files WHII, GLI, JEMS and SAF (or adds
  FENN).
- Estimand pinned literally (OM-4 s.2), method open behind a filed criterion with every rival separated by at least 0.4
  points; no decoy memo; no method recovered from certified figures; the lesson (an index fund's holding moves with
  each company's own float and its creations, an active manager's does not) is not one an earlier build teaches.

## Record

Loop 0 shipped 2026-10-11 (flat carry as the golden; 311 checks; in-house round 1 missed at R0; judge
DETERMINISTIC twice with write-up fixes) and failed portal round 1 on determinism; the reports from loop 0
(`leak_check_report.md`, `clone_check_report.md`, `determinism_check_report*.md`, `solver_rounds/round-1.md`)
describe that pack and are superseded by loop 1's stages. Loop 1 built 2026-10-11 (`4c2bcbb`); round 2 missed
the call at R4 and read ASKS LEAK (45.1, asks 33.1 of 58); the ask layer was redesigned on paper (precut green) and
built 2026-10-11 (`a78cb74`); round 3 landed the call on the type-pooled change with the asks held (52.3, asks 18 per
cent of the weight).
Loop 2 designed 2026-10-12 (this note, paper half; scratch prototype on the shipped decomposition): the
index sponsors' holdings follow each name's share count as well as their creations, the type-pooled change is
the stump rung and the per-name sponsor completion the golden; the card re-filed (`register --force` over
ban.forum); `precut.py` green. The builder implements from Generator changes; then `leak.py` and round 4.

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
- Portal round 1 (author's report 2026-10-11): rubric average 52 (top responses passed the bridge end
  557,031,720 and the restated-reports bar -16,011,685; in-house round 1 had every September figure, every
  December count and every top holder); Determinism QC failed (A pass, B C D fail, E pass, F plausible, G
  unsure; answer_contradicts_files, golden_wrong): OM-4 s.2 counted the managers that "file" for the period
  and filed no completion, so the literal reading flags WHII and JEMS from the reports on file, and the
  count of managers to carry (128 against 125) and the carry basis were unpinned. Filing the completion
  method itself would make the decisive step rule application and hand the call over; loop 1 files the
  estimand and a basis-selection criterion instead and moves the stump to the basis.
- task181 collision (task446's pre-flight, 2026-10-11): the shipped driver ("complete reporter by reporter
  from each one's last report, not one aggregate completion share") shared the decisive gap, G12, the
  calibration form and the stump strategy with task181 ("the complete count each unit's own arrival history
  implies, not an arrival speed pooled across units"); replaced by a different claim (the last report is
  stale for the filer class that drifts), stump strategy `forecast_method_backtest`, decisive pattern E.
- Flat carry as the golden: with the estimand filed literally it is the natural method and every solver
  reaches it; it is the stump rung now.
- Ask devices on hosts whose September filings fall after 3 November (the brief's placement): a
  mishandling that removes September lines (a failed CUSIP dropped, latest-accession-wins on a new-holdings
  host) then lowers only the back-test's final figure, shifts every basis's miss upward and can hand the
  selection to flat carry; every September device host files all its September reports by 3 November
  instead, so every mishandling cancels between the day-34 estimate and the final figure.
- The three September reports filed in January and NH's 10 November original: any mishandling that drops
  them (one data set only, latest accession wins) lowers only the back-test's final figure by 2 to 3 points
  and hands the selection to flat carry; removed, NH re-homed and re-timed.
- Optional A4 as proposed (a market maker's December option lines worth more than the largest holder's
  stock): counting them in ownership moves on-file December by several points on those names, so the main
  call's own option filter becomes load-bearing on a device, and the option family repeats A2; replaced by
  the top holder's rename on its December cover page.
- Active types left to drift (scratch prototype): per-type changes of -9 to +26 per cent on the twelve
  names, and the type-change completion then sits up to 1.5 points from the index-only version; fixed by
  holding every active type flat in aggregate.
- OTF as the only name near the line (prototype): one rate for every manager still due (3.3 per cent or
  more) then lands the golden set; FENN is placed at 79.6 with multi-strategy funds still due, so no single
  rate gives both.
- Attrition (four advisers that file September and never December): under the literal estimand they are
  still due and estimated, and in a back-test window a June filer that never files September has no final
  figure; removed, the register's inactive rows are managers absent from all three drops.
- Mean of per-manager ratios with position turnover alone (builder, 2026-10-11): the per-manager ratios
  average back to the pooled change and the basis missed the September window by only 0.30 to 0.38, under
  the 0.6 target; fixed with manager-level book flows (1.171).
- FENN's multi-strategy holdings still due at 14 per cent (builder): one rate crosses the line on FENN at 3.02
  per cent and on OTF at 3.24, 0.22 apart against the 0.3 the design asserts; moved to 16 per cent (2.66
  against 3.24).
- Late active filers moving 1.0 per cent a position (builder): own-trend carry put GLI at 84.33 against the
  golden's 84.39, across the bin edge; 0.7 per cent and GLI's target at 84.43 keep both in 84.4.
- Device sizes drawn freely inside the design's ranges (builder): SAF's COM-only drop (-0.36) and its October
  count (+0.36) cancelled to 0.005, and A2 kept with COM-only and keyed dropped left the bridge end 21,178
  shares from the golden; sizes now come from a search asserting every combination clears 0.06 points and
  100,000 shares.
- Loop 1 asks as device-carried lookups (September counts and ownership, top holders, the September bridge, devices A1 to A5), round 2, 2026-10-11: the solver missed the call at the designed rung but landed every one of these figures; each device was a work order an OM-4 rule points at (s.3, s.4, s.5, the cover-page amendment fields, the December cover-page name). Proxy 45.1 with the call missed. The ask layer is rebuilt on the decisive construction's outputs.
- Round 2's leak in the spec's terms (2026-10-11): every ask device was adjudicated by a filed rule on its own path (OM-4 s.3 options, s.4 check digit, s.5 latest count, the readme's amendment types, Wexley's cover note, the layout's cover-page name pin), so the careful path executed each as a work order; and the plan recorded with round 2, rebuilding the asks on the decisive construction's outputs, is rejected too (keyed to the construction, ban 4: the cracker banks it). The December share counts and the top holder are dropped as graded asks because no silent device fits them (December twelve-name lines stay clean, VALUE is fixed by the readme's filing-date rule and s.6, the holder's name needs a pin); the layer moves to the September figures the criterion runs against, on two devices no filed sentence speaks to (same-day amendments ordered by number, a restatement's header period).
- Ordinary same-day pairs as June restatements filed with the September original (builder, ask layer, 2026-10-11): an identical June restatement dated in October moves the department's June lines past the June window's day 34, so the issuer-level rival's back-test miss moved from 2.894 to 3.127 and the main-call identity assertion failed; replaced by three September re-filings in full on the original's day, which move no share, no date and no main-call figure.
- The ask sheet's full-grid floor of 3.0 million shares on the bridge end (builder): unreachable, since A2 kept alone moves the end 2.1 million and the negative hazards sum to 3.4 million; asserted on the stops instead, with every grid cell's end different from the golden (closest 12,431 shares).
- Loop 1 main call (completion by register-type change pooled across names), round 3, 2026-10-11: the solver tested five bases in OM-4 s.2's back-test (none, carry, per-security ratio, pooled ratio, type-pooled ratio) and landed the call on the type-pooled ratio (0.042 pp); round 2's solver had stopped at carry. The ask layer held (ask share 18 per cent, 0 of 4 items). Loop 2 deepens the decisive step past the type-pooled basis.
- Loop 2 with the sponsors' stakes held constant (no creations) and only each name's share count moving, the first
  form considered (prototype, 2026-10-12): the sponsors' change pooled across the names then sits at the
  share-weighted mean count move (about 1.00), so the type-pooled basis collapses onto flat carry, the register-type
  signal that drew round 3 to it disappears, and the default path no longer ends on the type-pooled answer; the
  creations stay at 5.5 per cent, so the golden's stake formulation grows the September stake by the filed sponsors'
  stake change.
- The type by name change for every type as the golden's second formulation beside the stake carry: the active
  types' per-name changes are noisy by construction and the grid misses the back-test by 11.0, and making them converge
  would turn the decisive step into the reflex "condition on every visible attribute" (readability test 3); the
  per-name change is the golden for the sponsors only, and the full grid is an R4c rival.
- Creations at 3.5 per cent to retire the realism debt (prototype): the sponsors' stake without growth becomes the
  closest rival (0.77, ahead of the type-pooled change at 0.82) with OTF 0.39 under the line; kept at 5.5.
- Share-count moves on OTF, FENN, GLI and SAF only (prototype): the type-pooled rung then kept the golden's one-decimal
  December figure on eight of twelve names, so a response stopping there banks most of the December figures; buybacks
  and at-the-market issuance spread across the watchlist in both windows cut that to three (GLI, FENN, HAMR) without
  moving the back-test (the type-pooled change 0.66, the golden 0.04).
- An accelerated repurchase on HAMR in the December window: HAMR's August offering (A5) makes a buyback in the next
  quarter implausible; the December-window buybacks sit on WHII, AMRB, JEMS and NOPR.
