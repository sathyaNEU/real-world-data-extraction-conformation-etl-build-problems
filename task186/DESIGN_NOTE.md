# task186 design note

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task186.json`, architecture v1, drawn 2026-10-12 from seed AD09 (a
  regulator deciding which fuel brands to examine for levy pass-through). The world, the decision and the quantity are
  the seed's; the seed's pitfall (the ownership flag is not who sets the price) is not used for the call, and the
  pitfall is re-found from the stations' margin record.
- **Pairing:** Survey Research & Official Statistics, anomaly detection (the task type serves Anomaly Detection &
  Diagnostics). The monitor sits in the provincial statistics bureau, which runs the mandatory price-reporting scheme;
  scoring each unit's period change against an empirical reference of comparable changes is official statistics' own
  anomaly detection (as Hidiroglou-Berthelot scores period ratios against the spread of the other units' ratios).
  Secondary domain Economics & Econometrics (retail fuel margins and levy pass-through). General Statistics & Data
  Science x Anomaly Detection was the first draw and is blocked against task185 (`ban.pairing`).
- **Niche:** the Provincial Statistics Bureau's Prices Division runs the fuel price monitor under the Fuel Price
  Transparency Act and recommends to the Fuel Price Commissioner the one brand the Commissioner's pass-through inquiry
  examines before each 1 January rise of the provincial carbon levy. The monitoring standard finds, station by
  station, where the January 2026 rise was passed on in excess, with the false discovery rate across every examined
  station held at 5 per cent, and the inquiry goes to the brand with the largest share of its examined stations found,
  if that share is at least one in ten.
- **Forcing and forum:** the 1 January 2027 levy rise; the inquiry notice is served before it
  (`statutory_or_regulatory_filing`); the Commissioner decides (`regulator_or_inspector`); the organisation is a
  statistics office (`research_or_statistics_office`); the stakeholder is the head of the Prices Division
  (`statistical_office_head`).
- **Call:** the brand the 2027 inquiry examines (or none), with each brand's share of examined stations found, to the
  nearest ten per cent.
- **Shape 01** (ranked list under a cap, each candidate): the inquiry is capped at one brand; each of the seven brands
  carries its share found (7), its stations priced by the brand on 1 December 2026 (7) and its regular litres in each
  month of the first quarter of 2026 (21); the call (1), a chart of the litres (4 parts), files and units (3). Criteria
  arithmetic: 43.
- **Strategy and mechanism:** `uncertainty_hold` family (signal against noise across many simultaneous tests); gap rule
  then time (the filed false discovery rate entitles only a null that holds it, and the data's time structure, the
  areas' price cycles, decides what that null is); decisive G2 (the unit of independent evidence is a 28-day period
  change of an area's cycle, not a station-day), G17 supporting; Gate G `signal_vs_noise_or_hold`; calibration
  `none` (the null comes from the record itself).
- **Data-native sentence:** every urban area's regular-gasoline margins cycle over five to nine weeks as stations
  undercut each other down and then restore together, so a 28-day before-and-after margin change carries the area's
  cycle phase, which no station's own day-to-day variation shows; only the changes between periods when the levy did
  not move (or the same-area competitors at the same dates) give the null that holds the error rate.
- **Mechanisms read** (`guard.py mechanisms --objective anomaly-detection`, 18 builds): 25 and 28 a second-source
  inflow and a reachable share; 33 forward yield cut by an intervention; 48 a two-sided grain; 54 exposure while in
  custody; 68 a matched panel through identity successions; 76 a look-back class with zero conversion; 85 a unit's own
  observation window; 103 a fan-out through authorisations; 104 a self-adapting scorer replayed at another setting;
  119 waits a unit could shorten; 182 a lagged response to a shared driver; 183 repeat failers in parts; 125 a
  recruitment filter's carried difference; 180 detection by the quiet hours; 181 crossings of moving units; 184 host
  stand-down crowd-out; 185 a reading-dependent instrument conversion. None tests many units at once, none turns on
  the null distribution of a period change under shared local cycles.
- **Guard:** WARN `overuse.objective` (this is the Anomaly Detection lane). Nearest drivers at 0.06 (task121 v3, a
  self-controlled exposure comparison for complaint attribution; task500 v2, a spillover through links): neither
  tests many units against a null; the abstraction test maps neither onto this driver.
- **Sources:** the seed (AD09) gives the world (a regulator's minute-stamped price log, a station register with an
  ownership flag, closed levy changes) and the decision; its corpus-fit panel rule is not used. The client's official
  statistics anomaly pattern (robust ratio tests against the cross-section, not raw z-scores) teaches that an anomaly
  is judged against the spread of comparable changes; this build moves that to many simultaneous tests whose
  theoretical null is wrong. The client's multiple-testing pattern (FDR on the whole family) is kept as a filed rule
  and is not the stump. The client's two-layer example "comparing against the right group, not a simple before and
  after" is the lesson, carried by the null rather than a control arm.

## Default path

1. Read the monitoring standard: the daily price (time-weighted, 06:00 to 22:00 local), the daily margin (price net of
   the 5 per cent sales tax, less the levy in force and the terminal rack price), the margin change (the 28 days from
   1 January 2026 against the 28 days before), the examined-station rule, findings at a 5 per cent false discovery
   rate, and the inquiry rule (largest share of a brand's examined stations found, at least one in ten).
2. Rebuild every station's daily regular price from the minute log (UTC stamps to local time, the June 2026
   renumbering through the crosswalk), join the rack prices and the levy, and keep the stations examined.
3. Test each examined station's margin change against its own day-to-day variation: a one-sided Welch t-test of the
   28 daily margins after against the 28 before (a Mann-Whitney test or Newey-West errors give the same findings).
4. Apply Benjamini-Hochberg at 5 per cent across every examined station and take each brand's share found.

Ends on: Harbourline Fuels.
Golden: Tallis Petroleum.

On the built pack the default path finds 46 of Harbourline's 52 examined stations (88 per cent), Pellow Gas next at 70
per cent and Tallis last of the seven at 40; the golden finds 28 of Tallis's 92 (30 per cent) and no station of the
other six brands.

## Stump sentence

The default path tests each station's 28-day margin change against the station's own day-to-day variation, which
cannot see that every area's margins cycle over five to nine weeks, so it finds nearly every station in the two areas
whose cycles restored around the turn of the year and sends the inquiry to Harbourline Fuels; a null built from the
stations' changes between periods when the levy did not move holds the false discovery rate and leaves only Tallis
Petroleum's company-run stations, which kept about 3 cents a litre more than the rise.

## Three rules

Rewritten at the stage-2 re-measurement of 2026-10-21, which refuses this architecture. Each line says what was
measured on the generator's clean truth, not what the design intended. Three lines fail, and they are the three the
client's check turns on.

- Task type: survey-research-official-statistics / anomaly-detection, which serves anomaly-detection: the monitor
  scores each unit's period change against the spread of comparable changes. The task type is right, and it is also
  the problem, because that score is reached by a one-column outlier screen (see Not rule application).
- Domain test: the deciding quantity, the number of a brand's stations whose retail margin rose by more than the levy
  judged against what the town's own price cycle moves a 28-day margin anyway, is the field's own quantity, and this
  line holds. Town-level cycles of undercutting and restoration run five to nine weeks (measured: every area's period
  36 to 62 days, amplitude 2.45 to 3.05 cents a litre), so the cycle alone moves a station's 28-day margin by up to
  1.4927 cents a litre, which is the largest change among the 341 stations the golden does not find. What fails is not
  the quantity but the step the design calls decisive.
- Swap: put clinics and wait times in place of stations and margins and the task no longer stands, because there is no
  levy to net out of a margin, no rack price and no five-to-nine-week cycle of undercutting and restoration. This line
  holds.
- Layer 1: a minute-stamped price-change log in UTC read against a local-time daily window across daylight-saving
  changes; station numbers renumbered by the reporting platform in June 2026 with a crosswalk; terminal rack prices
  published per business day in dollars a litre, weekends and holidays carried; a register whose brand changes are
  effective-dated; changes resubmitted after six intake outages. None is planted, each is asserted neutral for the
  call, and this line holds.
- Layer 2: the design files estimand_identification, the counterfactual movement of a station's margin without the
  levy change. Measured, that counterfactual never has to be estimated to answer the call: the 28 stations the golden
  finds are exactly the top 28 of 369 by the standard's own 28-day margin change, clear of the 29th by 1.2233 cents a
  litre, so the layer that was meant to decide is decoration on every graded figure.
- Decisive step: FAILS on measurement. The design's decisive step is the choice of reference distribution for many
  simultaneous tests. On the clean truth 7 of 15 data-free cuts on the standard's own margin-change column file the
  golden call and all seven printed bins, at a maximum absolute difference of 0.0000 percentage points and with an
  identical found set; three of the seven are plain outlier reflexes (the cross-section's median plus three MAD, its
  median plus 1.5 interquartile ranges, its mean plus two standard deviations). Choosing the null is therefore not the
  step that decides the call: one group-by, one robust spread and one comparison decide it.
- Not semantics: holds. Every field, unit and code (UTC stamps, the crosswalk, the rack's dollars a litre, the sales
  tax, the levy in force, the register's brand on the day) is read the same on the easy route and the golden one, and a
  reader who reads them all correctly and tests each station against its daily variation still files Harbourline.
- Not rule application: FAILS on the measured spread, which is the half of this line that was never answered. The
  standard files the margin, the windows, the false discovery rate and the inquiry rule and names no null, so the
  design's old line was answered against the question "does a filed rule name the method". Asked the right question,
  "is anything left to decide once every filed rule is read", the answer is nothing. Across the 13 licensed
  reference-distribution constructions (the station's own 28-day changes at non-levy dates one-sided, two-sided, by a
  normal approximation, before the change only, after it only, pooled over every station, pooled within each area; the
  cross-section at the change by median and IQR, by median and MAD, by mean and SD; same-area competitors on MAD, IQR
  and SD scale) the spread on six of the seven graded shares is exactly 0.0 percentage points, and 12 of the 13 file
  Tallis at 30 per cent with every other brand at 0. The 13th, the cross-section's mean and standard deviation, finds
  nothing. The Spearman correlation of the golden's own statistic with the plain margin-change column is +0.9837.
- Analyst test: the easy route still ends wrong, and that is no longer enough. A strong analyst who rebuilds every
  station's daily margin from the minute log, applies the standard's windows and examined-station rule and tests each
  margin change against the station's day-to-day variation before Benjamini-Hochberg at 5 per cent finds 195 of 369
  stations and sends the inquiry to Harbourline Fuels (88.5 per cent of its stations found, Tallis seventh of seven at
  40.2 per cent). The same analyst reaching instead for the cross-section's robust spread, the reflex this task type is
  named for, files the golden without ever asking what the counterfactual is, so the test separates two reflexes rather
  than a reflex from an analysis.
- Estimand: the monitoring standard's finding sentence (a station passed on more than the rise when its margin rose by
  more across the change than it would have had the levy not changed), the false discovery rate across every examined
  station held at 5 per cent, and the inquiry rule; filed literally in PM-04 and unchanged by this reading.
- No decoy: holds. No memo, bulletin, briefing or stakeholder figure names a brand, a share or a finding; the bureau's
  published weekly averages rank nothing on pass-through and are a distractor.
- No certified replay: holds. No certified or published figure is reproduced to recover the method, and the reference
  distribution comes from the record itself.
- Lesson: none this architecture can teach. The intended lesson, that evidence for many units at once must be judged
  against how much such changes move when nothing happened, is not what this data makes necessary: the quantity the
  lesson corrects is separated by 1.2233 cents a litre, and any ordinary outlier rule on one column reaches the same 28
  stations. The number is re-rooted at stage 1.

## Readability screen

The six tests per rung (1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear), verdict last.

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 each brand's average margin change | the standard defines the margin change | the log, the rack and the levy schedule | yes | no | no | one subtraction | readable |
| R1 each station's change tested against its day-to-day variation, Benjamini-Hochberg at 5 per cent (the default path) | the standard files the false discovery rate | no | yes: a t-test per station | no | no | no | readable |
| R2 robust (Newey-West) errors, a rank test, two-sided tests | no | no | yes | no | no | no | readable |
| R3 (decisive) the null from the stations' 28-day changes when the levy did not move, from same-area competitors at the change, or from the bulk of the cross-section | no: the finding sentence is met on its face by a margin held flat without the change | no column carries a cycle, a phase or a reference change | no: the defaults (t-tests, robust errors, rank tests, stratifying by brand or area) each keep Harbourline | none ships | the battery is clean on every path | no: a reference distribution per station or per area, never a subtraction | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a station's daily price | the time-weighted average of its posted regular prices from 06:00 to 22:00 local time | the mean of the day's posted prices; the price in force at noon; the 24-hour average | same call, same shares (asserted) | the standard's daily-price sentence, and same call |
| SF2 | the daily margin | the daily price net of the 5 per cent sales tax, less the levy in force and the day's rack price | the price with tax | same call, same shares (asserted) | the standard's margin sentence, and same call |
| SF3 | the margin change | the mean daily margin over 1 to 28 January 2026 less the mean over 4 to 31 December 2025 | other window lengths | not executed | the standard's windows |
| SF4 | an examined station | a station carrying one of the seven brands on the register on 1 January 2026 with a posted price on at least 20 of each 28 days | every registered station | same call (asserted) | the standard |
| SF5 | passed on more than the rise | a one-sided finding (margin rose by more than full pass-through leaves) | a two-sided test | same call, same shares (asserted) | the finding sentence, and same call |
| SF6 | the false discovery rate procedure | Benjamini-Hochberg at 5 per cent across every examined station | Storey's adaptive procedure; Benjamini-Yekutieli | Storey: same call, same shares (asserted); Benjamini-Yekutieli finds no station, its bar for 369 stations below the smallest p-value the stations' own changes can give | the standard names Benjamini-Hochberg |
| SF7 | what full pass-through would leave | the margin's movement over a 28-day change when the levy does not move, measured from the stations' own changes at every date whose windows hold no levy change | the bulk of the stations' changes at the change (an empirical null, median with IQR or MAD); same-area competitors of other brands (MAD, IQR or SD scale); the stations' own changes before the change only, after it only, two-sided or by a normal approximation; the area-relative margin against its own changes | same call, same shares (asserted for every one) | same call |
| SF8 | a station's brand | the brand on the register's brand history on 1 January 2026 | the brand today | same call (asserted) | the standard's examined-station sentence |
| SF9 | the share | findings over the brand's examined stations | findings over every station the brand carries | not executed | the standard's inquiry sentence |
| SF10 | the share's rounding | to the nearest ten per cent; no share within two points of a five-point edge (asserted) | whole per cent | same call | the prompt |
| SF11 | the inquiry rule | the brand with the largest share, if that share is at least one in ten; no tie (asserted) | several brands | same call | the standard's inquiry sentence |
| SF12 | rack price on a weekend or holiday | the previous business day's price carried | interpolated | same call (asserted) | the rack file's notes, and same call |
| SF13 | the daily window across daylight saving | local time | UTC days | same call (asserted) | the standard says local time |
| SF14 | a change resubmitted after an outage | one change per station and minute (exact repeats) | kept twice; the received time read as the effective time | same call, same shares (asserted for both) | same call |
| SF15 | stations renumbered in June 2026 | one station across both numbers through the crosswalk | the numbers as two stations | same call (asserted: the change window is wholly under the old numbers) | the crosswalk, and same call |

## Ladder

Built figures (seed 186), each asserted by name in `generator/checks.py`.

| Rung | Construction | Inquiry | Harbourline | Pellow | Tallis | Others |
|---|---|---|---|---|---|---|
| R0 | each brand's average margin change, largest | Harbourline | +0.88 c/L | +0.42 | +0.70 | +0.23 to +0.36 |
| R1, the default path | each station tested against its day-to-day variation (Welch), Benjamini-Hochberg 5 per cent | Harbourline | 88 per cent | 70 | 40 | 42 to 48 |
| R2 | a rank test (Mann-Whitney), Newey-West errors (3, 7 or 14 lags), or the province's daily mean margin taken out first | Harbourline | 46 to 92 | 9 to 74 | 33 to 41 | 7 to 59 |
| R2b | the cross-section scored on its plain standard deviation, or a placebo of one date in 28 | none | 0 | 0 | 0 | 0 |
| R3, decisive | the null from the station's own changes when the levy did not move (or same-area competitors, or the bulk of the cross-section by median and spread) | Tallis | 0 | 0 | 30 | 0 |

- **Kills, one fact each:** R0 by the standard (findings, not averages); R1 and R2 by the record's own changes at dates
  with no levy change (at the first of each month away from the change the same test finds a median of 27 to 43 per
  cent of each brand's stations, every one a false finding); R2b because neither can report a finding (the plain
  standard deviation counts the 28 Tallis stations in its own scale and masks them; one date in 28 leaves 20 reference
  changes, whose smallest p-value, 1 in 21, is above Benjamini-Hochberg's bar at every rank a finding could take); R3
  stands.
- **Why each is satisfying:** R1 is the textbook per-unit test under a filed false discovery rate; R2 answers the
  autocorrelation worry with robust errors; both reconcile station by station.
- **Separation:** on the default path Harbourline leads Pellow by 1.26 times and Tallis is last; on the rank test
  Harbourline leads Pellow by 1.24, on every Newey-West variant by 1.6 or more, on the province-relative variant by
  1.41 (Tallis second); on the golden Tallis's share is three times the rule's one in ten and no other brand has a
  finding. Accepted against the fourth-or-fifth rule: Tallis is last on the default path (40 per cent, in the 40 per
  cent bin with Wexcombe and Oxbury, every share off its golden bin), because most of its dealers trade in the five
  towns whose cycles were falling at the change; it is second on R0 (Harbourline 1.26 times its average change), on the
  province-relative variant (1.41 times its share) and on Newey-West at 3 lags (2.4 times), third or lower elsewhere.
- **Robustness:** every null that holds the error rate files Tallis at 30 per cent and every other brand at 0, finding
  28 or 29 Tallis stations: the stations' own changes at every date, before the change only, after it only, two-sided
  or by a normal approximation; the bulk of the cross-section by median with IQR or MAD; same-area competitors of other
  brands on MAD, IQR or SD; Storey's adaptive procedure. The write-up's components state the shares, not the count. Every
  within-window test (Welch, Mann-Whitney, Newey-West at 3, 7 or 14 lags, the province-relative margin) sends the
  inquiry to Harbourline.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | stations carrying one of the seven brands on 1 January 2026 with posted prices on 20 or more days of each window | the standard's examined-station sentence |
| 2 | Unit of account | the station for findings, the brand for shares | the standard |
| 3 | Attribution window | 4 December 2025 to 28 January 2026 | the standard's windows |
| 4 | As-of dating | the change examined is 1 January 2026; the extract runs to 15 November 2026 | the standard (the previous change) and the extract notes |
| 5 | Version basis | changes resubmitted after outages are exact repeats | C1: same call (SF14) |
| 6 | Denominator | the brand's examined stations | the standard's inquiry sentence |
| 7 | Weighting | each station equally | the standard |
| 8 | Window length | 28 days each side | the standard |
| 9 | Boundary inclusivity | a finding at the 5 per cent false discovery rate; an inquiry at a share of one in ten or more | the standard |
| 10 | Rounding path | shares rounded once, to the nearest ten per cent | the prompt (SF10) |
| 11 | Tie-break | none needed | asserted: no tie at the top |
| 12 | Maturity and censoring | the change closed ten months before the extract | none needed |
| 13 | Order of operations | daily price, margin, change, finding, share, inquiry | the standard's order |
| 14 | Row order | none affects a time-weighted price or a sum | C1 |
| 15 | Duplicate resolution | exact repeats after outages | C1 (SF14) |
| 16 | Identity normalisation | the June 2026 renumbering | the crosswalk (SF15) |
| 17 | Netting | the levy in force netted out of the margin | the standard (SF2) |
| 18 | Dimensional units | cents a litre in the log, dollars a litre in the rack file | units in the data and the rack notes |
| 19 | Code and status semantics | brand codes, rack product codes | the brand register and the rack notes |
| 20 | Integerisation | findings are counts | none needed |
| 21 | Clause scope | the inquiry rule reads the previous change only | the standard's inquiry sentence |
| 22 | Forward window contents | the 2027 inquiry examines the brand the 2026 change names | the standard |

## Literal reader

Executing the standard word for word: the daily price, the margin, the windows, the examined stations, the false
discovery rate and the inquiry rule are filed and execute to one set of numbers; the finding sentence asks whether a
station's margin rose across the change by more than it would have had the levy not changed. The record shows every
area's margins moving between 28-day periods by up to about 1.4 cents a litre with no levy change, so the literal
counterfactual is that movement, measured from the stations' own changes at dates when the levy did not move or from
same-area competitors at the change; a day-to-day standard error measures something else, and holding the false
discovery rate at 5 per cent is impossible with it (the same procedure finds about three stations in ten at any date).
Every null that holds the rate (SF7) finds the same stations within a share bin, so every literal reading lands on
Tallis; the easy answer comes only from the easy null on the same estimand.

## Oracles

- The record's own changes at dates with no levy change: they show the default path finding about three stations in
  ten at any date and the golden's null finding none; no shipped figure states either, and the record is the same on
  every path.
- The bureau's weekly price bulletin (area average prices, a distractor): ranks nothing on pass-through and ties on
  no path.
- No published pass-through figure, finding or share ships.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| C, each brand's share of examined stations found | 7, nearest ten per cent | the call's case, one result per candidate | the Commissioner sees why one brand and not the six others | none: the construction layer (the decisive null) | none | price log, rack prices, levy schedule, register, crosswalk, standard (6 files, 12 columns) | the default path's shares (every brand off its bin: Harbourline 100 against 0, Tallis about 50 against 30, the others 40 to 60 against 0); the answer | the monitor's own findings table |
| V, litres of regular sold at the stations carrying each brand in January, February and March 2026 | 21, thousands of litres | the stakes of each candidate's case: the litres over which the 2026 rise was passed on | the inquiry notice states the brand's volume; the Commissioner weighs the cases | D7, survey reference numbers reissued: a number freed when a dealer closed between April and early June 2026 is given to a station that had traded all along but joined the frame from August, so the frame snapshot names the new holder (with a brand in every month) while the January to March returns belong to the closed station, which only the return's site address, the frame's joining date and the register's closed stations show (a dealer's return names its operator's business, never the brand) | revisions (the latest revision of a return supersedes); late returns processed in the next month (reference month against processing month); rebrandings effective on the first of a month (brand for the month) | survey returns, survey frame, register (stations, brand history), brand register, notes (5 files, 14 columns) | every revision summed by processing month on today's brands (every brand off); latest revision by reference month through today's frame (every brand off by the reissued stations' litres); returns dropped where the frame holder joined after the month (every brand off); the answer | a sales survey frame reuses freed reference numbers, and a monthly return carries the station's name as the operator typed it |
| P, stations each brand prices itself on 1 December 2026 | 7, counts | the scope of an inquiry into each candidate: the stations whose pump prices the brand sets | the notice's information request goes to those stations | D3, two meanings one column apart: the register's ownership column says who owns a site, not who sets its price (commission agents are dealer-owned and brand-priced, company-owned dealer-run sites are dealer-priced); the November submission log shows the brand's pricing desk pushing its stations' prices through the API at the same minutes of the day (its push times) | API submissions from dealer groups and a POS vendor (the API channel is not the brand); stations moved from brand to dealer pricing in October; rebrandings (shared with V) | submission log, register, brand register, notes (4 files, 9 columns) | the ownership column (every brand off: 26, 14, 11, 9, 10, 6, 7 against 27, 15, 13, 10, 8, 9, 5); every station with an API submission (every brand two over: dealer groups and a vendor); company-owned stations with API submissions (five or more brands off); the answer | a price-reporting platform records each change's channel and minute, and a register records ownership, not pricing |
| Chart, litres by brand and month | 4 named parts | the exhibit of V on the memo's second page | the Commissioner reads the stakes at a glance | inherits V's device | inherits V's hazards | V's path | V's stops on every bar | a regulator's standard exhibit |

- **Main population zero-counts:** no survey row, frame row, submission-log row or ownership value is read by the main
  call; the 2026 rebrandings change no examined station's brand on 1 January 2026 (asserted); asserted by count in
  `checks.py`.
- **Hazard table:** rebrandings, read at today's brand, move V for the brands involved (Tallis, Wexcombe and Garrow in
  every month, Pellow and Oxbury in January, asserted cell by cell) and P's 1 December counts; revisions and late
  returns move V in every month they touch; the September and October changes of pricing (a Tallis commission agency
  to a dealer, a Strathlowe company site leased to a dealer) move P's ownership stop; the dealer groups' and the
  vendor's API submissions move P's channel stop for every brand.
- **Referee:** none; the survey and the submission log tie to nothing the call reads.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| C shares by brand | the golden's null | right | outside |
| V litres by brand and month | latest revision, reference month, the frame's holder, brand for the month | every cell off by a closed dealer's litres, carried silently to the new holder's brand | miss |
| P stations priced by the brand | the register's ownership column | 26, 14, 11, 9, 10, 6, 7 against 27, 15, 13, 10, 8, 9, 5 | miss |
| Chart values | V's cracker path | every bar off | miss |

Mirror leakage: about 6 per cent of the ask weight (the chart's title and axis parts; every share, litre and count
misses on the default path).
Pair ceiling: about 36 (the cracker at about 58 with the call, the shares and the chart's presence parts, the mirror at
about 15).

## Build record

- Generator: `world.py`, `market.py`, `analysis.py`, `survey.py`, `records.py`, `docs.py`, `deliver.py`, `checks.py`,
  `verify.py`, `metadata.py`, `build.py`, `postprocess.py`; `python3 task186/generator/build.py` builds the pack, the
  goldens, `metadata.json` and `generator/figures.json`, runs the checks (1,289 assertions) and the verifier, rebuilds
  into scratch for the byte comparison and cuts `target.zip`.
- Pack: 14 files in 5 formats; the price-change log 199,123 rows; distractors the weekly price bulletin and the
  Commissioner's price complaints register.
- Mess neutrality (R2), each asserted to file Tallis at 30 per cent and every other brand at 0: the daily window read
  in UTC; the received time read as the effective time with every outage repeat kept; old station numbers read as
  stations of their own; the rack interpolated over unpublished days; today's brand for the brand at the change; the
  margin with tax; the noon price, the mean posted price or the 24-hour average for the daily price.
- Layer 1 inventory: the platform stores every change in UTC (log, submissions; misread as local, the window shifts
  four or five hours); the platform renumbered stations on 8 June 2026 (log, register, crosswalk; misread, a station
  splits in two); the terminal publishes on business days only (rack file; misread, weekends have no rack); the
  platform re-sent queued changes after six intake outages (log, operations log; misread, a change counts twice); the
  register dates every brand change (register; misread, a station takes today's brand). Survey revisions and late
  returns, the reissued survey references and the register's ownership column sit on the asks' rows only.

## Judge record

- Pass 1 (stage 4): DETERMINISTIC, SOLUTION_WRONG, FIX_NOW. The call (Tallis, 28 of 92, 30 per cent, every other brand
  0) reproduced under every null the judge tried (own-history changes with or without the plus one, 2025-only or
  2026-only dates, one or two-sided, a normal z, a robust cross-sectional z, Bonferroni); the naive t-test or a raw
  margin-rise count names Harbourline, judged not defensible. All 21 litre cells and the seven scope counts
  reproduced. Findings: a closed Wexcombe station's open brand row made a literal read examine 370 (fixed in the data:
  the register ends a closed station's brand, the notes end a price at the closing day; 369 asserted on the literal
  read); "every one a station Tallis prices itself" was false in November for a commission agency since passed to its
  dealer (the component now states the shares; the memo says Tallis priced them at the change). Left open by design:
  "prices itself" is read from the November push times, not the register's ownership column (the ask's device; the
  register's About sheet defines site_ownership as who owns the site); the partial-month March station and the
  reassigned references are the asks' Layer 1, resolved from the records. Gate G statistical_rigor,
  analytical_non_defect; Gate H domain pass, layers pass, decisive step analytical (the swap line rewritten to answer
  the swap test from the fuel market's own cycles).
- Pass 2 (the one re-judge): DETERMINISTIC, FIX_NOW on one prompt clause. 369 examined, 28 found, all Tallis, every
  null variant the same (own-history dates before or after only, the plus one or not, a pooled null, an area-median
  control); the naive routes name Harbourline (all its stations up; Welch 46 of 52). All 21 litre cells and the seven
  scope counts reproduced, the push-time split exactly 0 or 1 per station. The clause: the litres ask did not say how a
  station that opened or closed during a month counts (a Harbourline dealer closed on 16 March, a Wexcombe station
  opened on 9 March); the prompt now says it counts in full under the brand it traded that month, the workbook notes
  say the same, no figure moved. Gate G statistical_rigor, analytical_non_defect; Gate H domain pass, layers pass,
  decisive step analytical.

## Pre-ship check

- Call: the 2027 pass-through inquiry examines Tallis Petroleum: 30 per cent of its examined stations found (28 of 92),
  no station of the other six brands; the stations found are Tallis's company-run sites and commission agents, which
  Tallis priced itself at the change, in Hollinsby, Greyford, Duncarrow and Marrowby, at about 3 cents a litre above
  full pass-through.
- Default path: Welch per station with Benjamini-Hochberg ends on Harbourline at 88 per cent (Pellow 70, Tallis 40);
  every within-window variant ends on Harbourline; the masked or powerless routes find no station; every null that
  holds the error rate files the same call and shares (28 or 29 Tallis stations).
- Gates: 1,289 checks with the R1 to R3c block, independent verifier from target/ alone, two byte-identical builds,
  figures_check 52 figures, precut 49 checks, voice-check PASS, scrub clean (target and golden), leak.py REVIEW (no
  LEAK), guard surface promotes task185 (back to back, a different domain and driver, the shared gap key only) and
  task184 (two apart, decision type only), heart WARN (Anomaly Detection overuse only, nearest driver 0.06).
- Deliverables: pass_through_inquiry_2027.docx (page 1 the call, the explanation, the findings table and the scope
  paragraph; page 2 the chart of litres by brand and month), inquiry_scope_2027.xlsx (seven brands: stations priced by
  the brand on 1 December 2026, litres in each month, notes); target.zip from the final rebuild, 14 files.
- Leak: four isolated reads (the last on the prompt's month clause), no decisive-step sentence, no ranking file,
  question 6 analytical; the complaints attractor, the batch of closures and the open brand row fixed on the way.
- Judge: pass 1 DETERMINISTIC, SOLUTION_WRONG, FIX_NOW (369 against a literal 370, a false component claim), fixed in
  the data and the write-up; pass 2 DETERMINISTIC, FIX_NOW on one prompt clause (the month rule for the litres), applied.
- Card current: answer, spine rows 199,123, stump and driver at the built values.

## Leak record

- `leak.py --asof 2026-11-16`: REVIEW, no LEAK. Sweep 4: the extract notes carry 6 and the standard 11 of the stump
  paragraph's terms, all the monitor's ordinary vocabulary (station, change, margin, register, standard, false
  discovery); neither names a cycle, a reference period or a null (asserted silent in `checks.py`). Sweep 6: the survey
  returns name four brands only as the registered owners filing for their company-run sites, beside litres; the
  register names every brand in trading names beside dates; neither ranks anything on pass-through.

## Tried and rejected

- General Statistics & Data Science, multiple testing and selective inference, as the domain: blocked by
  `ban.pairing` against task185 (General Statistics & Data Science x Anomaly Detection in this draw's window).
- The seed's panel rule fitted to the closed levy changes: a corpus-fit withheld rule (the guard's banned
  architecture), and the ownership-flag question it rests on is a field reading.
- Brand-level pass-through with town-clustered errors as the filed measure: a brand-level test is not what the
  standard files and its clustered errors leave Tallis short of significance, a competing answer.
- A pooled empirical null with some areas not cycling: the null distribution is a spike and a slab, central matching
  fits the spike and finds the cycling areas' stations, so the empirical null and the placebo null disagree; every
  urban area cycles in the build.
- Pellow's dealer mix with as many company-owned dealer sites as commission agents (6 against 5 and a new company
  site): its ownership count equalled its brand-priced count, so the ownership read hit Pellow's scope figure; two of
  Pellow's company dealer sites made dealer-owned.
- The litres golden reading a station's brand on the first of the month: it dropped the Wexcombe station opened on 9
  March 2026; the brand is read from the station's first day open in the month.
- Survey returns naming the station by its trading name (brand, town and street): the brand could be read off the
  return, which bypassed the reissued references; a dealer's return names its operator's business and carries the
  site address.
- Stations priced by the brand read from minute stamps shared with three or more of the brand's submissions: Garrow's
  five stations change together in twos and threes on quiet days, so a bar of four or a share of four in five dropped
  them; read from the brand's push times (minutes of the day), which every priced station keeps whatever the bar.
- A Canadian-level rack price (0.96 dollars a litre): the price stream moved and Tallis's share on the default path
  fell into the golden's 30 per cent bin; the rack stays at the record's level (pump prices 92 to 132 cents a litre in
  a province whose only fuel taxes are the levy and the sales tax).
- Cairnmore Energy, Pembry, Fennick and Cresswold: each a letter or two from a real company or place (Cairn Energy,
  Pembrey, Fenwick, Cresswell); renamed Strathlowe Energy, Duncarrow, Marrowby and Brindlecote.
- Eight closing dealers on one day (1 April 2026) and new stations opened to take their references: the shared day
  read as a batch marking the device's rows, and a holder with no brand in January failed loudly on the brand join;
  the dealers close on eight days from April to early June and their references go to stations trading all year that
  joined the frame from August, so the frame join succeeds and is wrong.
- The complaints register naming the brand of each complaint: Tallis, the largest brand, drew most complaints, an
  attractor toward the golden; the register keeps area and category only.
- Tallis's dealers placed 42 in the five towns whose cycles were falling at the change and 6 in the three rising
  Pellow towns: Tallis's share on the default path sat at 35.9 per cent, a point from the edge of the golden's 30 per
  cent bin; 38 and 10 put it at 39 per cent.
- One random stream for every station's prices: moving one dealer's closing day moved every later station's prices,
  so each fix to the asks re-rolled the main call's default path; each station now draws its own stream.
- A closed station's brand row left open in the register: a literal read of PM-04 3.2 (the price standing until the
  next change) examined a Wexcombe station closed in June 2025 (370 stations, judge pass 1); the register ends a closed
  station's brand the day before it closed and the extract notes end a price at the closing day.
- Critical components carrying the count of stations found: the same-area null finds 29 Tallis stations where the
  stations' own changes find 28, both 30 per cent; the components state the shares.
- Widening the magnitudes at stage 2, which is what a `FAILED_TO_STUMP` on measurement normally takes: refused on
  measurement. The golden's 28 found stations are exactly the top 28 of 369 by the standard's own 28-day margin change
  and clear of the 29th by 1.2233 cents a litre, so any cut in a 1.2233-cent-wide window reproduces the found set
  exactly; 7 of 15 data-free cuts on that one column file the call and all seven printed bins at a maximum absolute
  difference of 0.0000 percentage points, three of them plain outlier reflexes (median plus three MAD, median plus 1.5
  interquartile ranges, mean plus two standard deviations). The same seven land it on the shipped bundle read through
  `generator/verify.py`. The decisive step is arithmetic, so no magnitude repairs it.
- The signal dial (Tallis's excess pass-through) as the way to widen the separation: one-ended, both ends read, at
  exA10 (no call, the golden finds nothing, 0 of 13 agree, 0 of 5 crude routes land it), exA15 (gap -0.348, 2 of 13
  agree, 0 of 5 crude routes land it), exA20 (gap 0.225, 9 of 13 agree, 1 of 5 crude routes land it), exA25 (gap
  0.720, 12 of 13 agree, 4 of 5 crude routes land it), base (gap 1.223, 12 of 13 agree, 4 of 5 crude routes land it),
  exA40 (gap 2.225, 13 of 13 agree, 4 of 5 crude routes land it), exA50 (gap 3.223, 13 of 13 agree, 4 of 5 crude
  routes land it), exA60 (gap 4.225, 13 of 13 agree, 4 of 5 crude routes land it). No setting has the step both needed
  and determinate.
- The cycle-amplitude dial as the way to widen it: the same one-ended curve from the other side, at ampB050 (gap
  2.120, 13 of 13 agree, 4 of 5 crude routes land it), ampB075 (gap 1.687, 13 of 13 agree, 4 of 5 crude routes land
  it), base (gap 1.223, 12 of 13 agree, 4 of 5 crude routes land it), ampB150 (gap 0.357, 9 of 13 agree, 1 of 5 crude
  routes land it), ampB200 (gap -0.578, 5 of 13 agree, 0 of 5 crude routes land it).
- The phase-spread dial (how far the coastal areas' cycle phase at the change sits above Tallis's four towns'), which
  is the only axis that moves the default path at all: one-ended too, at phC040 (gap 2.050, 13 of 13 agree, 4 of 5
  crude routes land it), phC070 (gap 1.544, 12 of 13 agree, 4 of 5 crude routes land it), base (gap 1.223, 12 of 13
  agree, 4 of 5 crude routes land it), phC130 (gap 0.970, 10 of 13 agree, 4 of 5 crude routes land it), phC160 (gap
  0.972, 10 of 13 agree, 3 of 5 crude routes land it), and it fails three ways as it widens. Compressed to 0.40 the
  default path itself files Tallis (Harbourline no longer leads: Tallis first at 30.4 per cent, lead 3.17 times), so
  the ladder inverts. Widened to 1.30 and 1.60 the default path's own lead over Pellow falls to 1.14 and 1.13 times,
  under the 1.15 times floor, while the licensed family drops to 10 of 13 and 4 of 5 then 3 of 5 crude routes still
  land the golden.
- Tuning any of the three dials to find a cell where the separation is wide and the licensed family still unanimous:
  there is no such cell, and the reason is algebraic rather than a matter of search. The decisive step is the choice
  of the scale a one-dimensional unit statistic is read against, so the licensed constructions differ only in the
  location and spread they divide that statistic by. They agree on the found set exactly when no admissible scale
  reorders the units, which is exactly when one sort on the statistic is the answer. Measured over 16 settings,
  Spearman corr(crude routes landing the golden, licensed constructions agreeing) = +0.8837.
- The default path's own separation as the thing to widen, which is what this build's resume line ordered: the
  within-window route is insensitive to the signal dial (Harbourline 88.5 per cent, lead 1.27 times over Pellow,
  Tallis seventh of seven at 40.2 per cent at every excess from 1.0 to 5.0 cents a litre), so nothing on that axis
  moves a reader's crossing.
- The readability screen's reflex row on the decisive rung, accepted at the first stage 2: measured on an incomplete
  enumeration. The row lists t-tests, robust errors, rank tests and stratifying by brand or area, every one of them a
  within-window test, and omits two reflexes that each file the golden's exact printed answer: the cross-section's own
  robust spread, which is the Hidiroglou-Berthelot move this note's `## Draw` names as official statistics' anomaly
  detection, and the default path's own Welch test run after the town's daily mean margin is removed (30 stations
  found, Tallis 31.5 per cent, printed bins 30 and six zeros, the golden's bins exactly). Removing the town mean is
  the first control anyone reaches for against town-level cycles; `checks.py` tested the area-relative margin only
  against the placebo null, never against the within-window test.
- **(2026-10-25, measured) THE ONE BUILD IN THIS LANE WHOSE CALL HELD.** One isolated Sonnet reader at medium effort, holding only the pack, the prompt and the emitted key list, filed **Harbourline Fuels** against the golden **Tallis Petroleum**, and filed 195 of 369 stations found against the golden 28, with every brand's share wrong (HBL 90 per cent against a golden 0, TAL 40 against 30). It ran a one-sided Welch t-test of daily margins after against before and Benjamini Hochberg at 5 per cent across all 369 stations pooled, and read "more than the levy rise" as a margin increase above zero because the margin already subtracts the levy. It took **34 of 59 ask figures, 57.6 per cent**. With both top responses missing the call the pair sits at about 12 plus 55 times the ask keep, so this build measures at about **43.7 and already clears the 50 bar**; at the asks' own spec it sits near 23. So this is the one FAILED_TO_STUMP number the measurement does not condemn: its repair is `/fix-rubric` on the ask layer with the call frozen, not a re-root.
- **(2026-10-25, /fix-rubric pass 1) The pack narrated two of ask V's four elements, and that sentence is removed.** The shipped `extract_notes_2026-11-16.md` carried "In the survey, reference_month is the month a return reports and processing_month the run that processed it; a later revision of a return replaces the earlier one", which hands over both of ask V's hazards in one line and is `supplemental-stumping` ban 1, nothing narrates a device. It is cut. The convention still converges without it, because a `revision` column beside `reference_month` and `processing_month` admits one sensible reading, so no fork opens. The remaining three notes lines (the UTC and DST rule, the price-stands rule, the 8 June renumbering) serve the main call and stay. Rebuild clean: 1,289 assertions, `verify` agreeing on an independent recomputation, `figures_check` 51, `voice-check` PASS, `leak.py` REVIEW with no new line, and `freeze.py check --mode rubric` PASS with the main call, the stump and every frozen figure unchanged. It moves no graded figure by design, so `freeze.py` warns that nothing on the ask side moved: correct, since the repair makes the ask harder to reach rather than changing its answer, and the test is a re-read.
- **(2026-10-25, measured) Where ask V's 21 of 21 came from, and what is still owed.** The leak is ask V alone: asks C and P held at 0 of 14 together (the shares and found-counts ride the missed call, and the priced-by-brand counts held outright), while ask V's litres went 21 of 21. Four candidate replacements for its D7 primary were worked and refused, each for a stated reason: a dealership-grain return needing an allocation weight (no exact remedy, and allocation is not determinate); a multi-site dealership whose second station is off the frame (an unmatched join, which the hygiene battery runs); a four-weekly trading period against the calendar month (the apportionment is a method choice, so the ask stops being determinate); and a rejected-revision device evidenced by a control total (a control that ties only under the golden is ban 3, an oracle). **The one that survives screening is the sample-grossing device:** a monthly fuel sales survey is a stratified sample, the frame carries a stratum rather than a weight, and the stratum populations sit in the published bulletin, so the grossing factor has to be reconstructed as population over sample count before any figure appears. Its remedy is multi-purpose under readability test 7 (a bulletin states its coverage and a frame records its strata for reasons entirely their own), no hygiene sweep asks whether a file is a census, and it moves all 21 figures per brand and month. It needs the ask's wording loosened from "the fuel sales survey's litres" to "the litres", keeping all 21 figures, the unit and the rounding, because as worded the raw reported sum is the defensible reading and the ask must stay determinate.
