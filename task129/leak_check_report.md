# leak check, task129

**Verdict: REVIEW.** 18 files read, 23 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: decisive, population, device, service, default, release, deploy, separating, groups, sentence, effects, puzzles, golden, decision, client, silent, control, composition, registry, headline, record, effect, carried, deploys, reading

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `rum_export_field_guide.md`: \bthe model\b x1: .... `form_factor` is phone or tablet; `perf_band` (low, mid, high) is the model's band on the group's CPU benchmark and is the phone class used in...

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `page_delivery_service_level_v3.pdf`: carries 9 of 12 distinctive words of the committed call: "The operations squad should fix Bølge's front end in Q4: at August's traffic the fix brings back about 1,460,000 mobile "

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `page_delivery_service_level_v3.pdf`: 6 of 25 stump-paragraph terms appear (device, service, release, deploy, registry, reading); read whether the document names the move
- **REVIEW** `paywall_terms_subscriber_layout_2026.pdf`: 3 of 25 stump-paragraph terms appear (device, record, effect); read whether the document names the move
- **REVIEW** `rum_export_field_guide.md`: 8 of 25 stump-paragraph terms appear (device, release, deploy, puzzles, client, registry); read whether the document names the move

## 8 column names (REVIEW 2)
- **REVIEW** `device_registry_2026-09.csv`: columns a generator names and an organisation does not: device_model
- **REVIEW** `image_cdn_delivery_2026.csv`: columns a generator names and an organisation does not: device_class

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `subscription_register_extract_2026-09-05.csv`: 181 ISO dates after 2026-09-07, e.g. 2026-10-31

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Three isolated reads (medium effort), each on a fresh copy of prompt.txt and target/ only.

### First read (before the realism and determinism repairs)

#### Q1
None. No sentence or file names the decisive step or the fix and its recovered views. Closest: the Service Level (page_delivery_service_level_v3.pdf) s.3 "Before-and-after comparisons of the share for a change use the 28 days either side of the release that switched it on." and s.4 "A fix is valued on the mobile views it brings back under the line at the latest full month's traffic." These fix the frame (window, valuation basis), not which change or the number. Ove Schmidt in service_review_prep_thread.txt ("It's the consent banner. The numbers turned the week it went in...") argues one candidate, not the answer. The change_register and rollout log supply dates and overlap (Prebid and Bolge ship together, wave by wave, ad-free layout switched at once on 30 June) but give no attribution.

#### Q2
None. digital_ops_q3_service_closeout.xlsx gives July/August share over line by title and says it "does not attribute the share to any release". The change_register lists the five changes with dates only. The AMP and desktop summaries are context (flat AMP ~5-6%, desktop drifting 6 to 8%). Ove's email ranks the banner first, informally, and that is a view, not a score.

#### Q3
Nothing obviously analyst-only. Closest: service_review_prep_thread.txt (a tidy, short thread that frames the one-fix choice and plants the consent-banner view), and the digital_ops_q3_service_closeout.xlsx, which covers only July and August (so cannot be used for the before/after of earlier changes) and uses "current masthead". The decoys (desktop_field_summary, amp_landing_views, newsletter_sends, paywall terms) are plausible org records. change_register_2026.xlsx lists exactly the five changes in the prompt, with the Prebid/Bolge overlap spelled out in the Scope column; it reads as an organisation record but is unusually tidy for the task.

#### Q4
No figure reads as the answer. The close-out shares (Aug 25.17% group vs July 23.33%) read as context. The only name that reads like an answer is the consent banner (Ove's email, "It's the consent banner"), which is the stated suspect, and the prompt's "the pictures are a suspect too" hints the image pipeline is a second suspect. Nothing in the files states which one wins.

#### Q5
- page_delivery_service_level_v3.pdf s.1: "A mobile view is a page view on a device whose model the device registry lists with form factor phone." Fixes the population: phone rows only (tablets out), resolved via device_registry_2026-09.csv.
- s.2: "A page view misses the line when its largest contentful paint exceeds 4.0 seconds. A view with no paint timing ... is not scored." Fixes the outcome (lcp_ms > 4000, strictly; null lcp excluded from the denominator).
- s.3: "use the 28 days either side of the release that switched it on." Fixes the window for the change comparison (28 days before/after the release's deployed_at; offsets per release_train_log).
- s.4: "A fix is valued on the mobile views it brings back under the line at the latest full month's traffic." Fixes the unit and basis: views a month at August traffic (the latest full month). The result is a views-per-month number, not computed here.
- rum_export_field_guide.md: "sum [sample_weight] to count views"; "Reporting months are Copenhagen calendar months"; "A kilobyte (kB) is 1,000 bytes". Fixes weighting, month boundary (Copenhagen not UTC) and kB.
- image_cdn_vendor_appendix.pdf: "A request is counted in edge_hits or in origin_fills, never in both" (requests = edge_hits + origin_fills); "The fallback vendor reports this field in kilobytes (1,000 bytes)"; log_date is UTC day. Fixes the image-request and byte arithmetic for the second ask.
- paywall_terms 4.2/4.3 plus subscription register: signed-in subscribers get the ad-free layout, so ad-stack effects apply to non-subscribers only (needs the register's start_date/end_date inclusive).
None of these says how a before/after attribution should handle overlapping changes (e.g. Bolge+Prebid, the banner against concurrent traffic mix or the 3 June collector v2 change).

#### Q6
Largely an analytical choice, but with substantial rule-application and data-semantics content. The literal service-level text (28 days either side, phone only, 4.0 s, latest full month) can be executed as a procedure; the hard part is separating overlapping changes (Prebid ad stack vs Bolge shipped together wave by wave, ad-free layout switched at once so ad-free subscribers are a natural control, the image pipeline limited to hero templates, the fonts and banner on all templates) with the seasonal/mix drift, which is a design/estimation decision not stated anywhere. The semantics traps (collector v2 sampling weights, tz, tablets via registry, fallback vendor kB, edition moves of Bjerre and Tolstrup from LA to KD on 2026-03-16 so "title" vs current masthead, back-forward null LCP) are on top. Risk: if the 28-day literal window comparison per release already yields the ranking (window rule does the work), the decisive step is rule application. Nothing looks planted as a decoy memo apart from Ove's opinion.

#### Q7
Mostly realistic. Observations:
- Release train log notes are cycled from a small phrase list (e.g. "Tracking plan v14", "Obituaries upload form", "Sitemap generation fix" repeat many times); every deploy is approved by Mette Johansen, always about 04:42-05:22 local, which reads synthetic.
- Close-out figures and desktop summary are rounded to multiples of 50 or 100 (views like 23296050), and the desktop and AMP files are suspiciously smooth; "v1.2" provenance is fine.
- Bolge rollout wave dates are exactly 7 days apart from 30 June (7 Jul, 14, 21, 28, 4 Aug), a very tidy schedule.
- The field guide, the change register and the SLA are very neat and exhaustive; the thread is four short polite emails, with a convenient "Same format as the July cut" and "Noted."
- Device registry has perfectly clean tiers; AMP rows show an identical ad_integration string every row.
- Names are Danish-plausible and consistent; dates are consistent (export_manifest pulled 2026-09-05, matching the register extract).
- Parquet sample: first row timestamp 2026-01-31 23:00 UTC (Copenhagen 1 Feb), consistent with the field guide; sample_weight is 200 in v1.

### Second read (after the realism repairs and the pass-1 closures)

#### Q1
None. No sentence or file names which change to fix or how many views come back. Closest: page_delivery_service_level_v3.pdf s.3 "Before-and-after comparisons of the share for a change use the 28 days either side of the moment the release that switched it on was deployed." and s.4 "A fix is valued on the mobile views it brings back under the line at the latest full month's traffic, counted over that month's scored views that the change now reaches." These give window and valuation basis, not the decisive step (the staggered Bølge/Prebid waves, ad-free vs ad-supported layouts, which the change register and rollout log expose as raw structure only).

#### Q2
None. digital_ops_q3_service_closeout.xlsx says "it does not attribute the share to any release"; it only gives share by title for Jul/Aug. change_register_2026.xlsx lists 28 changes with dates and releases, no scores. desktop_field_summary and amp_landing_views are context series, not rankings.

#### Q3
None clearly exists only to help. rum_export_field_guide.md and the prep thread are plausible filed documents. The two the closest to analyst aids: the field guide (tells you to sum sample_weight, resolve device_model via the registry) and the closeout xlsx (pre-computed shares), both plausible internal artifacts. The distractors (desktop_field_summary, amp_landing_views, newsletter_sends, paywall terms pdf) are plausible org records.

#### Q4
No figure reads as the answer. Closeout shares (e.g. group 23.34% July, 25.23% August) are context; the "latest full month" (August) traffic is given in the closeout (59,715,050 mobile views) but that is a population total, not a fix value. The change register's "Bølge ... ad-free layout on all six at once, ad-supported layout wave by wave" and "Header-bidding ... then the Bølge template groups wave by wave" slightly foreshadow the confound between Bølge and Prebid, but are descriptive scope text.

#### Q5
- SLA s.1: "A mobile view is a page view on a device whose model the device registry lists with form factor phone." Fixes population: phones only, via registry (tablets out).
- SLA s.2: "A page view misses the line when its largest contentful paint exceeds 4.0 seconds. A view with no paint timing ... is not scored." Fixes outcome and denominator: lcp_ms > 4000, rows with empty lcp excluded.
- SLA s.3: 28 days either side of the deploy of the switching release. Fixes the comparison window (28 days before/after deployed_at, local time with offset).
- SLA s.4: valued at latest full month's (August) scored views the change "now reaches". Fixes valuation month and the reached population.
- Field guide: sample_weight sums to views; Copenhagen-date reporting months; kB = 1,000 bytes; vendor appendix: fallback vendor reports bytes_served in kB; CDN log_date is UTC; a request is in edge_hits or origin_fills never both (requests = sum of both, excluding bot/desktop classes presumably). These fix the ask-side figures (image requests and kB per mobile view). Literal results not computed.
- Paywall terms 4.2/4.3: signed-in subscribers get ad-free layout, others ad-supported; with subscription register (active start..end inclusive) defines who reaches the ad stack. Fixes who the Prebid change reaches.

#### Q6
For the main call the stated pieces are rules about window/population/valuation (SLA s.1-4), and the real work is attribution: separating overlapping, staggered changes (Bølge waves vs Prebid on ad-supported only vs ad-free layout; consent banner 2026-05-05, fonts 03-03, images 04-07) using the 28-day pre/post window, a comparison group (ad-free signed-in readers got Bølge on 06-30 without ads, other wave template groups not yet switched are controls), and valuing at August reach. That is an analytical choice (design of the attribution/comparison), with moderate rule-application scaffolding in the SLA. Not a planted decoy: distractors (AMP, desktop, newsletter) are unused-but-plausible. A risk: the SLA s.3 + s.4 plus the rollout log nearly dictate the execution procedure, and the data-semantics layer (device registry, tablets, sample weights, UTC vs Copenhagen, subscription end dates, edition register remap of Bjerre/Tolstrup from LA to KD on 2026-01-12, "title = masthead at the time of view") is Layer 1 mess, which could decide the figures if not cleaned. The image-ask side turns on semantics (fallback kB unit, UTC day, bots/desktop classes, kB=1000).

#### Q7
Mostly realistic: named staff with plausible Danish names, real-looking email thread, release hashes, deploy times 04:44-05:22 with DST offsets, wave dates one week apart (neat and regular: Tuesdays 30 Jun then 7, 14, 21, 28 Jul, 4 Aug), edition register changes, vendor appendix. Mild tells: the Bølge rollout switch times and weekly cadence are very tidy; closeout over-line view counts all end in 50 (e.g. 5,416,650; 6,121,250), consistent with sample_weight multiples (round numbers from weights of 50/200), plausible. amp and desktop series are smooth noise on round-ish levels. The thread sentence "if there is anything I should look at first, say so now" and Caroline's request for the CDN log with appendix is slightly staged to introduce the picture suspect. The prompt says "the pictures are a suspect too" matching that. No obvious leaks of answers.

### Third read (the shipped bundle, after the section 4 and paywall 4.2 wording)

#### Reader answers (task129)

#### Q1
None. No file names the fix or its figure. Closest procedural text is page_delivery_service_level_v3.pdf s3 ("Before-and-after comparisons of the share for a change use the 28 days either side of the moment the release that switched it on was deployed.") and s4 ("A fix is valued on the mobile views it brings back under the line at the latest full month's traffic, counted over all of that month's scored views on the pages and layouts the change is live on today."). These give the window and the valuation footing, not the choice. The change_register scope text for Bolge ("ad-free layout on all six at once, ad-supported layout wave by wave") and CHG-2611 ("Ad-supported layout: spil pages, then the Bolge template groups wave by wave"), plus boelge_rollout_log.csv, hint that ad stack and Bolge overlap and are staggered, i.e. that separating them needs the staggered waves and the ad-free vs ad-supported split. That is a hint at structure, not an answer.

#### Q2
None. digital_ops_q3_service_closeout.xlsx gives only shares over line by title/month and states "it does not attribute the share to any release". amp_landing_views_2026.csv and desktop_field_summary_2026.csv give shares for other populations (desktop shares also rise, AMP flat); they do not rank the five changes. change_register_2026.xlsx lists changes and dates, no effects.

#### Q3
Nothing is blatantly analyst-only. Closest: service_review_prep_thread.txt (a thin mail export whose only content is "One fix, so it has to be the right one" and a request that the CDN log be filed) and export_manifest.csv (a tidy index; plausible as a handover sheet). rum_export_field_guide.md is explanatory but plausible as an ops-team doc. The three distractors (desktop_field_summary, amp_landing_views, newsletter_sends) exist as decoys relevant-but-unused; they read as organisational records.

#### Q4
No figure or name reads as the answer. Mild context-weight items: the closeout's 23-25% over-line shares and the prompt's list of five changes. The desktop summary shows share climbing from ~6% to ~8% on desktop, which could nudge a solver toward a site-wide cause, but it is not a named answer.

#### Q5
- SLA s1: "A mobile view is a page view on a device whose model the device registry lists with form factor phone. Tablets and desktop browsers ... are not part of this service level." Fixes population: phones only (registry join on device_model, tablets excluded).
- SLA s2: "A page view misses the line when its largest contentful paint exceeds 4.0 seconds. A view with no paint timing ... is not scored." Fixes outcome (lcp_ms > 4000, strictly), denominator = scored views (lcp non-null). Also "reported monthly by title".
- SLA s3: "28 days either side of the moment the release that switched it on was deployed." Fixes comparison window (+/-28 days around deploy time from release_train_log, local time with offset).
- SLA s4: "valued on the mobile views it brings back under the line at the latest full month's traffic, counted over all of that month's scored views on the pages and layouts the change is live on today." Fixes unit/population: August 2026 scored views on the template/layout cells the change is live on now (so ad-supported Bolge cells vs ad-free, Bolge waves all on by 4 Aug). Literal result not computed.
- paywall_terms s4.2/4.3: signed-in active subscribers get ad-free layout on every template; others (incl. free accounts) ad-supported. Fixes who sees the ad stack (needs account_key joined to subscription_register with inclusive start/end dates).
- field guide: "Reporting months are Copenhagen calendar months"; "sum [sample_weight] to count views"; "a kilobyte (kB) is 1,000 bytes". Fix month boundaries (UTC to Copenhagen), weighting, unit.
- vendor appendix: fallback vendor bytes_served is in kilobytes; "A request is counted in edge_hits or in origin_fills, never in both" (requests = hits + fills); log_date is UTC day; fallback 9 June-21 July. Fixes the CDN per-view figures (requests per view, kB per view) and the unit conversion; device_class in the vendor log is vendor's own classification, so mobile-vs-phone alignment is a semantics point.
- edition_register: effective-dated mastheads (Bjerre, Tolstrup move LA to KD from 2026-01-12) fix how /lokal/<edition>/ views map to titles; field guide says `title` is masthead at time of view while closeout uses "current masthead".
- change_register / rollout log: dates for fonts (3 Mar), image pipeline (7 Apr), banner (5 May), ad stack (24 Jun), Bolge (30 Jun) with release ids; release_train_log gives exact deploy timestamps.

#### Q6
The prompt/SLA fix the estimand (phones, scored views, >4.0 s, +/-28 days, August traffic on live cells), so much of the execution is rule application and data semantics (registry join, UTC to Copenhagen, kB units, collector v2 sample_weight, masthead). The files that make the call non-trivial are structural: the staggered Bolge waves vs staggered ad-stack rollout (CHG-2611 overlaps CHG-2598 across the same six releases), ad-free subscribers vs ad-supported on the same release (a within-release control that the register and paywall terms point at), and the fonts/banner/image changes landing in sequence before. Separating the ad stack from Bolge appears to need an analytical choice (use ad-free layout and unswitched template groups as controls, handle overlapping before/after windows and the preliminary trend), not a single field reading. A literal-rule solver could still do a naive 28-day before/after per release and get confounded numbers, which is the analytical gap. No planted note or decoy memo argues a wrong answer; the distractors (desktop, AMP, newsletter) are unused context. Risk: the ask parts (CDN requests/kB per view) are decided by unit/definition reading (fallback kB, UTC day, hits+fills), which is semantics, but these are asks not the main call.

#### Q7
Mostly realistic: believable Danish names/places, plausible emails, release ids with deploy times clustered at ~05:00 local, content hashes, a mail thread with understated tone, vendor appendix with "Internal. Vendor contract references on file". Possible tells: rollout log has 6 waves exactly one week apart on consecutive Tuesdays (30 Jun, 7, 14, 21, 28 Jul, 4 Aug) with near-identical text blocks and a single signer; change register CHG-2598 scope text is a long explanatory sentence that reads like an author's note rather than a register entry; change register is not in id/date order (CHG-2600 dated 5 Jun after CHG-2598 dated 30 Jun); service level text is tidy and includes the exact rules "28 days", "latest full month" in a way that reads as designed (s3/s4); field guide says title is e.g. "ST Sønderå Tidende" but parquet holds "ST" codes (small mismatch, fine). Round numbers: closeout counts all end in 0/50 (rounded weights of 50/200 sampling), consistent with sample_weight. Closeout and amp shares are random-looking (AMP shares flat 5-6% with noisy values). Mail thread is oddly empty (a prep thread with no substantive content) and the manifest, though plausible, is very orderly. Dates: all before 5 Sept 2026; thread 2 Sep predates the 5 Sep export it discusses (fine, it is planned). Nothing obviously after the setting date.

### Rulings

- Question 1, all three reads: nothing quoted; the service level's sections 3 and 4 fix the window and the valuation, the register and rollout log show the overlap as plain scope, none gives the split.
- Question 6, all three reads: the deciding step is the analytical choice of how to separate the co-switched changes.
- First-read realism tells (a register of only five changes, cycling release notes, one approver, the banner belief in the thread, the AMP report's constant column, the desktop summary's rounding): fixed in the generator.
- Later-read tells, harmless and true to the fiction: weekly Tuesday waves on the release train with the programme lead signing; counts ending in 50 from the sampling weights the field guide states; change numbers assigned when raised, so a change raised in spring can go live after later numbers; the thread's request for the CDN log is the image ask's own reason; the AMP and desktop summaries are distractors.
- leak.py REVIEW lines: harmless, one line each in the design note's Leak check section.

