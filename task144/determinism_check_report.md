# Verdict, task144 re-judge

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE (no repair needed, no rerun). Residual risks listed below are optional notes, not blockers.

**Why:** Executed literally, memo s2 (external first star, non-bot, non-member at the time, UTC day 1 = made_public_at, day 90 inclusive, stars not yet made counted) plus the prompt give one answer: slidewell, about 12,000 in 90 days, about 9,000 added by the spotlight. Every figure I recomputed matches the golden. The lottery sheet holds 21 randomly drawn spotlights with full star histories. Their lift tracks each repository's feed stars per follower view, and that rate fits the lottery far better than any fixed average lift. Slidewell wins under every rate-driven lift model I tried (structural cascade, linear fit on rate).

## Evidence (recomputed from the shipped files)

| Item | Result | Source |
|---|---|---|
| External first stars (bots out, org members at the time out, merged accounts mapped) | Matches the rollup `external_first_stars` for all 2,245 repo-days of the 28 repos with events. By 27 Sept: tracewire 3,876, slidewell 2,766, ferrolog 1,892, hullcheck 1,912, shiftgres 1,826, timeloom 1,299, kilnkit 1,245. Chart values to the nearest thousand reproduce. | event files, accounts parquet, memberships, rollup |
| Newsletter stars per subscriber | 52,892 newsletter first stars (v5 `nl` mapped via the crosswalk) over 7,309,469 subscribers over the 21 drawn issues = 0.7236%. Times 433,812 = 3,139. | both event files, lottery xlsx |
| Mean followers of newsletter starrers; of feed starrers | 85.0; 10.2 | accounts parquet |
| Feed stars per follower view | slidewell 1.796%, tracewire 0.098%. Kilnkit 0.651%, ferrolog 0.463%, shiftgres 0.352%, hullcheck 0.280%, timeloom 0.243%. | events, accounts |
| No-spotlight forecast to day 90 (stars to date + 7-day pace x runner-up ratio, 114 runner-ups) | slidewell 2,955, tracewire 5,713, ferrolog 3,695, shiftgres 3,835, kilnkit 2,133, hullcheck 3,172, timeloom 2,078 | rollup |
| Added by spotlight, N(1 + r x 85/(1 - r x 10.2)) | slidewell 9,006, tracewire 3,403, ferrolog 4,436, shiftgres 4,113, kilnkit 5,000, hullcheck 3,908, timeloom 3,804 | derived |
| Totals | slidewell 11,961, tracewire 9,116, ferrolog 8,131, shiftgres 7,948, kilnkit 7,133, hullcheck 7,080, timeloom 5,882. Rounded, these are 12k, 9k, 8k, 8k, 7k, 7k, 6k, as in the golden. | derived |
| Postwerk/Relaymark delivered subscribers (first two Sluis batches per issue; test seed and Product News excluded; third send is a resend) | Apr 391,299; May 399,160; Jun 406,891; Jul 429,444; Aug 429,291; Sep 429,949. All reproduce. | campaign files |
| Click-through share (distinct subscribers clicking the issue's spotlighted repo link in any send / distinct delivered) | 1.4886 (1.49), 1.5219 (1.52), 1.5319 (1.53), 1.5220 (1.52), 1.4419 (1.44), 1.4895 (1.49). All reproduce. | link report, click log |
| Nominators (repository names normalised incl. URL forms and the kiln-ui and imagelint renames; people = account or email hash, merge chains followed to the final survivor) | slidewell 58; tracewire 47, 91.49%; ferrolog 37, 81.08%; shiftgres 31, 90.32%; kilnkit 27, 81.48%; hullcheck 26, 88.46%; timeloom 19. All reproduce. | nominations, renames, accounts, memberships |

### Literal-reading forks and the competing answers

- **Lift model (the one that moves the call).**
  - Lottery average lift gives tracewire first, at about 9.5k to 11k, with 4k to 5k added. The lottery rejects this: the lift ratio (spotlight stars over newsletter stars) runs 1.1 to 2.6 across the 21 draws and correlates about 0.95 with the repository's feed rate.
  - Lift scaled by a repository's own feed share is also wrong. Its correlation with the lift ratio is 0.17, and it also puts tracewire first.
  - Rate-driven models agree on slidewell: structural cascade 11,961 against tracewire 9,116; linear fit of lift on rate 11,820 against 9,024.
  - With a clean estimate of the spotlight's feed excess (baseline feed share held from pre-issue), the structural cascade reproduces all 21 lottery lifts to RMSE 0.029 in lift ratio. Linear leave-one-out gives 0.048.
  - Rounded to the nearest thousand, slidewell's total and its added stars (12k and 9k) come out the same under the structural and linear models. Only a first-generation-only cascade gives 11k and 8k, and the lottery fit rejects it.
- **Baseline method.** Pace windows of 7 and 14 days and the sum-of-ratios, mean-of-ratios and median-of-ratios variants leave every rounded total unchanged. A 3-day pace moves shiftgres to 7,487 (rounds to 7k, not 8k). A leave-one-out backtest on the runners-up puts 3-day pace at 5.2% MAPE against 3.1% for 7-day and 2.3% for 14-day. Cumulative-multiple methods are far worse (16 to 19%), so the data separates the methods.
- **Resend.** Nothing in the files labels the third Sluis send a resend. It is forced by the data:
  - Summing all three sends exceeds the list size in the lottery log (June: 656k against 410,609).
  - The first two batches have zero clicker overlap, while the third overlaps both (about 20 each).
  - Counting only first-send clickers would give 1.21% in April. Counting clicks by delivered subscribers on any send is the literal reading of "share of them who clicked through".
- **People dedup.** Following a merge chain to the final survivor is required (3197968 to 5377621 to 7703873; 4603956 to 5464224 to 7458354). A single-hop dedup gives tracewire 48 and ferrolog 38. The accounts-file definition ("the surviving account's id") supports the chain reading.
- **Same-name repositories under other owners** (ravi-kok/slidewell and others) do not resolve to shortlisted repositories and are correctly excluded.

## Files/Hygiene: PASS

19 files; formats are parquet, csv (several, semicolon and comma), json, pdf, xlsx and md. The rollup, event files, clicks and parquet are all above 25k rows. Two distractors are present and unused: the daily trending lists and the repository traffic file. Neither decides the call. Documents read as system exports or internal memos; the xlsx and pdf metadata are clean (author names are in-fiction). No authoring or benchmark language found. The parquet writer signature (arrow) and the spreadsheet "Microsoft Excel" tag are normal. Timeline is coherent: the memo is dated 15 Sep, the extract 28 Sep, and the log's October row is a no-draw note. Minor: the log is dated 24 Sep but its note mentions the 27 Sep extract and the 30 Sep meeting, which is plausible as planning text. `extract_contents` records source and date but no licence column; the data is fictional, so there is no licensing exposure. No exclusion-level finding.

## Stump power

Good. The easy route is the lottery's average lift (or lift on feed share) added to each trajectory. That puts tracewire first at about 9.5k to 11k, a wrong call. Getting the right one needs reasoning about feed exposure (followers of starrers), noticing the 21 randomised spotlights are heterogeneous and validating a lift model on them, plus a forward baseline built from runners-up. The extraction asks (resend and batch dedup, test seeds, rename and URL-form resolution, merge chains, pre-public versus created dates) add independent places to lose points.

## Stumping type

`mechanism: method_or_model_selection` (heterogeneous spotlight-lift model chosen on the randomised lottery; baseline forecast validated on runner-ups), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.

No reported number is wrong. The data is honest; the difficulty is choosing the lift model the lottery supports. On clean data the task still stumps.

## Three rules

`domain: pass`, `layers: pass`, `decisive_step: analytical`.

- **Swap test:** the deciding quantity is expected 90-day star growth under a newsletter feature, estimated from a randomised spotlight lottery with an exposure (follower) cascade. That is product-growth and developer-relations analytics. Another field's nouns would not read the same.
- **Layer 1:** v5/v6 schema codes, UTC against Amsterdam times, made_public against created dates, renames, merged accounts, batch sends with a resend, two ESP exports.
- **Layer 2:** counterfactual lift modelling and a validated forward baseline.
- **Easy route:** average (or feed-share) lift on each trajectory. A strong analyst who cleaned everything correctly still files tracewire, about 11,000 with about 5,000 added.

## Fix

none (fix location: none). Optional, not required: nothing that changes what solvers see.
