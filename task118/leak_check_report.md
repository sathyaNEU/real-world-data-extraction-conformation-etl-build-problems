# leak check, task118

**Verdict: LEAK.** 19 files read, 18 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: already, change, netting, archive, headlines, platform, nothing, decisive, editors, sizing, dashboard, shrunk, closed, inside, export, surfaces, opportunity, decision, realised, sentence, owners, embedding, reference, incremental, vertical

## 1 file names (LEAK 1, REVIEW 5)
- **LEAK** `cms_revisions_export_fields.txt`: a file whose name says it describes the data (cms_revisions_export_fields): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **REVIEW** `audience_plan_2027.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files
- **REVIEW** `audience_warehouse_field_reference.md`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data
- **REVIEW** `headline_squad_change_log.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files
- **REVIEW** `newsroom_staff_list_2026-10-12.xlsx`: a sheet named 'About': confirm it is the organisation's own notes and does not describe the data's columns or files
- **REVIEW** `panel_reference_workbook.xlsx`: a sheet named 'Definitions': confirm it is the organisation's own notes and does not describe the data's columns or files

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `headline_squad_2027_placement_brief.pdf`: carries 6 of 9 distinctive words of the committed call: 'Place the headline squad with Culture·national for 2027, where it adds 1,250,000 extra article clicks.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `audience_warehouse_field_reference.md`: 6 of 25 stump-paragraph terms appear (archive, platform, dashboard, inside, reference, vertical); read whether the document names the move
- **REVIEW** `editorial_standards_s7_corrections.pdf`: 3 of 25 stump-paragraph terms appear (change, headlines, editors); read whether the document names the move
- **REVIEW** `headline_squad_2027_placement_brief.pdf`: 8 of 25 stump-paragraph terms appear (change, headlines, editors, closed, decision, embedding); read whether the document names the move

## 5 announcements (REVIEW 1)
- **REVIEW** `prompt`: Which desk on the shortlist (Politics·national, Sport·metro, Business·national, Sport·national, Local·metro or Culture·national) should the headline-testing squad join for 2027, and how many extra article clicks would it add there in 2027?

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 2 author vocabulary (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

### Read 1 (first rebuilt pack, 2026-10-12)

### 1. Which sentence or file tells the decisive step?
No filed sentence states a step or method for the extra-clicks figure. The nearest candidates:
- Brief: "The squad is judged on incremental article clicks in the twelve months after it embeds, counted at the owning desk on every click an article earns from publication, the hours its headline is under test included." This fixes the base (all clicks, owning desk, from publication, test hours included), not a lift or a method.
- Field reference, `canonical_headline`: "It is the headline carried in the article's RSS and partner feeds, its search and social metadata, Discover-style cards, newsletters and alerts. Not included in the pageview extracts." Next to the source-code table this lists which surfaces carry the stored headline, so it points toward the idea that headline-driven exposure differs by source surface. It does not say to restrict or weight anything. Mild hint, the closest thing to an intent signal.
- Change log notes define `realised_holdback_lift_pct` (versus a 5 per cent holdback) and the field reference defines the dashboard "winning lift". Both are context for choosing a lift, neither is called the right one.
- Audience plan: "New initiatives for 2027, including the headline squad's embedding, are planned on top of these figures." Context.
So none states the decisive step.

### 2. Does any file rank, score or state the call, figure, runner-up, gap or workbook figures?
No. `audience_plan_2027.xlsx` gives per-desk clicks (Oct25-Sep26 and plan, identical) but no lift or ranking. `experimentation_dashboard_export` is by vertical (lifts 2.22 to 4.69) and ranks nothing for the desks; the vertical grouping (Sport and Politics merge national and metro) is a mild wrong-basis lure, shipped as context. `panel_monthly_audience` has raw monthly rows per release, no averages. `headline_squad_change_log.xlsx` has only app-desk embeddings. Kayla Torres's email line "it goes where the readers are. The panel numbers are in the folder." states the naive default path (readers) but not the call or any figure. No file gives readers, visits or correction-minutes averages.

### 3. Files that exist only to help the analyst
- `panel_reference_workbook.xlsx` is a bit analyst-facing (tidy Release log with notes about replacement, Definitions sheet), but a panel vendor/audience team could plausibly keep this. Its release-log notes are unusually explicit about which releases replace which, which is a small tell.
- `cms_revisions_export_fields.txt` is a plausible export note, though sentences like "A note put back after a save that left it off is the earlier notice, not a new correction" read as author guidance (see Q6).
- `audience_data_export_log.csv` is plausible as a provenance log. Its dates (15 and 16 Oct 2026) postdate the brief (12 Oct) and the thread's first emails (13 to 14 Oct) only mildly; harmless.
Nothing is clearly synthetic-only; distractors (newsletter, syndication agreement, standards bulletin, s7 corrections PDF, staff list) look like ordinary records.

### 4. Figure or name reading as the answer
None. The nearest is the dashboard's highest vertical lift (Politics 4.69) and the readers-first email from Kayla Torres, both framed as the common default and not the stated call. The "Sport" vertical on the dashboard spans two shortlist desks.

### 5. Literal execution
Main figure. No sentence defines the lift or the clicks it applies to beyond the brief sentence quoted in Q1. Executed literally, "incremental article clicks ... counted at the owning desk on every click an article earns from publication, the hours its headline is under test included" means: base = all article pageviews at the desk's articles, all 11 source codes, all age bands, test hours included, over 2027 (plan = Oct25-Sep26 level). The incremental amount needs a lift rate, which no sentence fixes (change log "realised_holdback_lift_pct" is the only measured in-year lift and exists only for app desks; dashboard "winning lift" is a different definition). So the literal text pins the click base but not the rate or any exposure restriction; a literal reader would apply some lift to the full all-source base. Whether that equals the golden depends on the design; this is the point to check on the author's side.

Workbook measures.
- Readers: panel definition "Estimated number of different people aged 14 and over who visited the section at least once in the month, on any device"; "average monthly readers" over "the twelve months to September 2026" = mean of the 12 monthly `unique_audience` values per desk. A literal reader sums the desk's section(s) across sites (SPT-N vs SPT-M etc. are separate desks, so no cross-site sum is needed, since each desk maps to one section code). Summing sections within a desk is not needed; no dedup issue arises.
- Visits: "Estimated visits to the section in the month", mean of 12 months.
- Release per month: Release log notes say R26-04H "figures replace the earlier releases for those months" (Nov 2025 to Feb 2026) and R26-07B "replace those published in R26-05, R26-06 and R26-07" (Apr to Jun 2026). A literal reader uses R26-04H for Nov-Feb and R26-07B for Apr-Jun. Observed data: release R26-08 (published 9 Aug) carries 36 rows for Apr to Jul 2026, with no log note. A literal reader taking "latest release for each month" would take R26-08 for Apr-Jun (it is later than R26-07B) and the log does not say it is or is not superseding. This is an unfiled convention in the pack; the literal reading is ambiguous between R26-07B and R26-08 for Apr-Jun. Oct 2025 comes only from R25-11 and Sep 2026 from R26-10. Section codes change on 1 Mar 2026 (Section history sheet: valid_from 2026-03-01); R26-04H reruns Nov-Feb on the 2026 taxonomy so the "current" mapping applies to it, while older releases (R25-11 to R26-03) use the old codes. A literal reader maps by valid_from/valid_to of the period.
- Minutes: no sentence in the pack defines "minutes from an article going live to its first headline correction" except through the CMS notes: status `live` save is going live; a scheduled revision's `publish_at` is "the time the editor set for the CMS to publish the document"; "A headline correction is logged on the revision that publishes the corrected headline" (s7 7.4); correction_note copying and the ten-minute pairing rule. Clock: `saved_at` is stated "UTC, to the minute"; `publish_at` has no stated clock. A literal reader would treat both as the same clock (UTC) since only one clock is named in the notes, which is not stated and so is an unfiled gap if the data are in AEST/local. `published_date` in the field reference is AEST, and the brief/export scope says "(AEST)" for the window, so a reader may be unsure which clock applies to publish_at.

### 6. Sentences signalling special handling
Yes, in `cms_revisions_export_fields.txt`:
- "The CMS copies the note to every later revision until an editor clears it. A note put back after a save that left it off is the earlier notice, not a new correction. A fix and its note go on the same save, or on two saves within ten minutes of each other."
- `restored_from_doc`: "Set on documents recreated when the Brisbane instance was restored on 14 November 2025" and `migrated_from`: "Set on documents moved from the previous CMS at the migration on 1 October 2025".
- "A post is an entry in the live blog named in parent_doc, with a headline of its own."
These are field semantics that tell the solver there are copied notes, duplicate/restored docs, migrated docs and posts, i.e. they flag that rows need special handling beyond ordinary version handling, although they stop short of saying how to treat them. In the panel workbook, the Release log notes ("These figures replace ...") do the same for panel rows. The brief, thread and field reference contain no such sentence.

### Review lines
- Brief, 6 of 9 words of the committed call: harmless. The overlap is the shortlist desk names, "headline squad", "2027" and "extra article clicks"; the brief names Culture·national only as one of six shortlist rows and states no call or figure.
- Field reference, 5 of 25 terms: harmless. Platform, section, counts, dashboard and publish are ordinary field definitions; it defines the sources and canonical_headline surfaces but names no move or step (the canonical_headline surface list is a mild context hint only, noted in Q1).
- Standards s7 corrections, 4 of 25 terms: harmless. Generic standards text on corrections; 7.4 defines where a headline correction is logged, which is a definition, not the decisive step.
- Prompt: harmless. It is the task question itself, restated by the sweep, and it states no method or answer.

### Rulings on read 1

- Questions 1, 2 and 4: nothing quoted; no file ranks the desks or states a figure. Harmless.
- Question 3: the panel release log's notes name what each rerun replaces, as a panel provider's release log does; the CMS field notes' put-back line is the pin an earlier judge pass required. Harmless, kept.
- Question 5, main figure: the brief's counting phrase ("counted at the owning desk on every click an article earns from publication, the hours its headline is under test included") reads literally as an all-sources click base. Fixed in the generator: the brief now pins only the period ("counted at the owning desk from each article's publication, the hours its headline is under test included") and names no click base; SF3 and SF5 assert it.
- Question 5, readers and visits: the literal reading of the filed notes gives R26-04H for November to February and R26-07B for April to June, the golden; taking the July release for April to June needs an unfiled latest-release convention, and the July file's April to June rows are byte for byte the R26-05 to R26-07 figures R26-07B replaces. The device, forced by the records; not a fork.
- Question 5, minutes: `publish_at` names no clock. The device, forced by the records: read on UTC, 87 per cent of scheduled articles would have gone live by hand a median 528 minutes before their set time; read on AEST, 75 per cent go live at the set time and the rest 10 to 120 minutes early, and the pack's clock is AEST. Not a fork.
- Question 6: the field notes' lines on copied notes, restored and migrated documents and posts are the corrections hazards, filed by design. Harmless.

### Read 2 (the brief reworded, 2026-10-12)

### 1. Decisive step
No sentence or file names the decisive step. Nearest: the brief's "The squad is judged on incremental article clicks in the twelve months after it embeds, counted at the owning desk from each article's publication, the hours its headline is under test included." This fixes the scope (owning desk, from publication, test hours included) but does not say which click sources a lift applies to or how to size a lift. The field reference's canonical_headline paragraph ("the headline carried in the article's RSS and partner feeds, its search and social metadata, Discover-style cards, newsletters and alerts") is the closest hint at which sources a headline change reaches, but it is a schema description, and it does not say the squad's lift is limited to those sources. The change log's "realised_holdback_lift_pct" note and the dashboard's "Winning lift" definition are context showing two lift measures, with no instruction to choose either. Both lean toward a source-restricted, holdback-based reading, which is mild.

### 2. Ranking, scoring or the call
None. audience_plan_2027.xlsx lists clicks per desk (an all-sources base, plan = trailing 12 months) but does not rank on the decision. The dashboard gives avg_winning_lift_pct by vertical (Politics 4.69 highest), which is a wrong-basis pointer, not the call. Kayla's email ("it goes where the readers are"; panel numbers) is a colleague's wrong default (readers/panel), not the answer. No file states the call, figure, runner-up or gap.

### 3. Analyst-only files
Nothing clearly out of place for a newsroom. Closest: cms_revisions_export_fields.txt and audience_data_export_log.csv ("requested_by Standards") are plausible records. The cms revisions file was "asked for by Standards", yet it exists in the planning folder to give the correction-time minutes column; this is plausible and not a leak. The field reference is a real warehouse artifact. The staff list, newsletter file and syndication agreement are plausible context or distractors.

### 4. Answer-like figures or names
None reads as the answer. The all-sources clicks per desk in the plan (Politics·national 376,236,959 highest) and the dashboard's Politics 4.69 percent are headline numbers that would point to wrong answers, but they are context and not marked as the call. The change log's holdback lifts (0.695 to 2.554) are context.

### 5. Filed sentences that fix the main figure
- Brief: "The squad is judged on incremental article clicks in the twelve months after it embeds, counted at the owning desk from each article's publication, the hours its headline is under test included." Literal execution fixes: outcome = incremental article clicks; window = the twelve months after embedding (11 Jan 2027 on, per "Moving in January"); counted at the owning desk (desk_code); counted from each article's publication including the in-test hours (so no age band excluded). It does NOT fix which click sources a lift applies to: read literally, "incremental article clicks" are all article clicks at the desk, including every source, so the sentence gives no restriction to headline-sensitive sources. It also leaves open the size of the lift (which lift rate: dashboard winning lift, holdback lift, or other), the ramp/ageing of articles published before the embedding (whether clicks in the year on older articles count; "from each article's publication" suggests articles published in the window), and whether "twelve months" means 2027 calendar year or 12 months from 11 Jan.
- Audience plan notes: "2027 clicks are held at the twelve months to September 2026 for every desk, with no change assumed in where clicks come from." Fixes the 2027 base volume and source mix per desk. Leaves the lift open. "New initiatives... are planned on top of these figures."
- Field reference: "in planning papers clicks and pageviews are the same measure" fixes clicks = pageviews with source codes; "Winning lift, as reported on the experimentation dashboard, is the shipped package's click-through rate over the control's, minus one, and zero when the control is kept" defines one lift measure but is not stated to be the one for sizing. Change log note defines realised_holdback_lift_pct (CTR vs 5 percent holdback). Literal execution of each defines a rate; neither says which governs.
- Brief: "The squad joins one desk in January and stays for the year" and prompt "for 2027": one desk, a year.
- Not fixed anywhere: source set, lift rate, treatment of the 2027 window beyond the above.

### Review lines
- brief vs committed call: harmless. The overlap is the shared vocabulary of the question (place, headline squad, desk names, 2027, extra article clicks); the brief names no desk as the pick and states no figure. The shortlist lists all six desks neutrally.
- field reference: harmless. The terms (platform, section, counts, dashboard, publish) are ordinary schema vocabulary; the document defines fields and sources and names no move. The canonical_headline paragraph lists the surfaces carrying the headline, which is a mild hint at source relevance but is a legitimate warehouse description and states no rule for the squad's lift.
- editorial standards s7: harmless. Generic corrections policy (7.4 says a headline correction is logged on the revision that publishes it, which is a data convention for the minutes column, not the stump). Terms are common words.
- prompt: harmless. It is the question itself, and states desk, figure and rounding with no method hint.

### Rulings on read 2

- Questions 1 to 4: nothing quoted; no file ranks the desks or states the call or a figure. Harmless.
- Question 5: the brief now fixes the outcome, window, owning desk and counting period and names no click base. The two readings the reader lists as open converge: calendar 2027 and twelve months from the January move sum the same flat plan (SF2), and clicks on articles published before the embedding are under 1 per cent of platform clicks past seven days at every desk (closure axis 3). Harmless.
- Review lines: all harmless.

### Read 3 (the related_links row added, the pack as shipped, 2026-10-12)

### 1. Decisive step
No sentence or file names the decisive step. The nearest text is in the placement brief: "The squad is judged on incremental article clicks in the twelve months after it embeds, counted at the owning desk from each article's publication, the hours its headline is under test included." That fixes the estimand (incremental clicks, 12 months from embedding, owning desk, counted from publication). It does not say which click sources a test can move or how to get from lift to clicks. The audience plan note says "2027 clicks are held at the twelve months to September 2026 for every desk, with no change assumed in where clicks come from." That is a baseline statement, not a method. Nothing says "restrict to headline-sensitive surfaces" or "exclude app-only desks' lift".

### 2. Ranking / call / figure / runner-up / gap
No file ranks or scores the six desks on incremental clicks or states a call, figure, runner-up or gap. audience_plan_2027.xlsx gives each desk's flat Oct25-Sep26 clicks (total and per desk, e.g. POL-N 376,236,959; SPT-N 340,990,504) and is explicitly "planned on top of" for the squad. Those are baselines, and ranking by them (largest desk) is the naive path. Kayla's email, "it goes where the readers are," points at the wrong basis but is an opinion, not a score. The dashboard export ranks verticals by avg_winning_lift_pct (Politics 4.69 highest), a lift not a click figure, and the field reference defines it as a CTR ratio, so it is a plausible-looking wrong-basis ranking (reads as context/distractor, not the answer).

### 3. Files existing only to help the analyst
None clearly. audience_data_export_log.csv and cms_revisions_export_fields.txt are plausible records of warehouse extracts. The standards bulletin and s7 corrections PDF and newsfold agreement and newsletter file are plausible distractors for real newsroom folders. The field reference is the closest to analyst-oriented, but a warehouse data dictionary is normal. Its sentence "in planning papers clicks and pageviews are the same measure" and the "Winning lift, as reported on the experimentation dashboard..." definition are definitional.

### 4. Figure or name reading as the answer
None reads as the answer. Candidates that read as context-that-could-mislead: the dashboard's Politics 4.69 percent average winning lift; the largest plan baseline POL-N 376,236,959; Kayla's "goes where the readers are"; change-log realised_holdback_lift_pct values (0.695 to 2.554, app desks only) that sit well below the dashboard's winning lifts. No desk is named as recommended anywhere.

### 5. Sentences that fix how the figure is computed
- Brief: "judged on incremental article clicks in the twelve months after it embeds, counted at the owning desk from each article's publication, the hours its headline is under test included." Literal execution fixes: unit is article clicks (pageviews, per field reference), attributed to the article's owning desk_code, period is 12 months after the 11 January 2027 embedding (brief: "moves on Monday 11 January 2027"), and clicks accrue from each article's publication (so clicks across the article's life, including the under-test hours, for articles in that window). Leaves open: whether articles published before embedding count; the exact lift to apply (dashboard winning lift vs holdback realised lift); which sources a headline change reaches; how to project 2027 clicks by source/age.
- Field reference, pageviews: "`source_code` | The surface the reader clicked to reach the article" and "A click on a link to an article counts when the article page loads; in planning papers clicks and pageviews are the same measure." Fixes clicks = article pageviews by source surface and age band. Leaves open which sources count.
- Source table, literal: home_web, section_web, feed_app, section_app list surfaces; `related_links` "each showing the linked article's current headline"; the other surfaces carry no statement about their headline. Combined with `canonical_headline`: "The headline stored with the article at publication. It is the headline carried in the article's RSS and partner feeds, its search and social metadata, Discover-style cards, newsletters and alerts." Read literally, search, social, discover, partner_apps, newsletter and alerts show the canonical headline stored at publication, so a test (which changes what is shown in a test slot, per `impressions`: "Times the package's headline was shown in a test slot") does not change them. home_web, section_web, feed_app, section_app (front/tab slots) and related_links ("current headline") are the surfaces whose headline a test can change. This is a strong implied statement: it is stated as what canonical_headline feeds, but it never says outright that tests cannot alter canonical_headline, and it does not say the test-slot surfaces are exactly the four fronts plus related links. Also leaves open how a shipped headline propagates (whether it replaces canonical).
- Field reference: "Winning lift, as reported on the experimentation dashboard, is the shipped package's click-through rate over the control's, minus one, and zero when the control is kept." Fixes the dashboard measure, but it is an impression-level CTR in test slots, not realised incremental clicks. The change log's `realised_holdback_lift_pct` ("against the 5 per cent holdback ... minus one") gives realised lift, only for app-only desks.
- Plan Notes: "2027 clicks are held at the twelve months to September 2026 for every desk, with no change assumed in where clicks come from." Fixes baseline = Oct25-Sep26 clicks and constant source mix. Leaves open the ageing profile of clicks for 2027 articles.
- Desk register `distribution`: "App-only items have no web URL, feed entry, search listing, alert or newsletter." Context for the shortlisted web desks.

### Review lines
- Brief, 6 of 9 words of the committed call: harmless. The overlap is generic nouns (headline, squad, 2027, article, clicks, desk, Culture·national in the shortlist table); the brief names no desk as the pick and no figure, and the shortlist lists all six equally.
- Field reference, 5 of 25 stump terms (archive, platform, dashboard, vertical, source): harmless. These are ordinary data-dictionary vocabulary; the document defines fields and surfaces and names no move. (Note for the author, not a fix: the canonical_headline row plus source table implies which surfaces tests can change, which is the filed definitional text the task relies on, not an announcement of the step.)
- Standards s7 corrections, 3 terms (change, editors, headlines): harmless. Generic words in a standards policy; section 7.4 only says a headline correction is logged on the revision that publishes it, which is context for the minutes-to-correction metric, not the main call.
- Brief, 7 terms (change, closed, vertical, decision, editors, headlines): harmless. Ordinary planning vocabulary (change log, closed embeddings, vertical column, editors); no method or answer is named.
- Prompt: harmless. The flagged line is the question itself, listing the shortlist and asking for the desk and figure; it names no method, source restriction or answer.

### Rulings on read 3

- Questions 1 to 4: nothing quoted. Harmless.
- Question 5: the field reference now states, in the `related_links` row, that related-story links show the linked article's current headline (the judge's pass-2 fork), and the reader executes the source table with `canonical_headline` to the golden's surface classes. That is rung 3, readable by design; the decisive netting is named nowhere. Harmless.
- Review lines: all five harmless.
