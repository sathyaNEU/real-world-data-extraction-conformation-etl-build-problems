# Task158 targeted re-check, after the early-access tenant scale-up

## Verdict: HOLDS

## 1. Main call
Recomputed from the pack with the filed policy: intake busiest-hour traffic at the Q3 close-out GPU-seconds per request (Voice rps x 3,600), plus the eleven signed contracts at contracted peak from their go-live Monday, priced with the lc2 fit, less the fleet-plan allocation, largest of 13 weeks.
- lc2 fit (batch-prod, 4,998 pure lc2-2026.05 hours): 0.24801 ms per prompt token, 1.84997 ms per completion token (graded 0.248 / 1.85).
- Eleven signed contracts at peak: 249.42 GPUs once all live (graded about 250).
- Peak-week shortfall: docs-prod 338.8 GPUs (2027-W13), code-prod 299.3, agents-prod 151.0, voice-prod 21.5, chat-prod -78.0, batch-prod -80.1.
- Rounded to the nearest 10: docs-prod 340, code-prod 300. Matches the graded answer.

## 2. Early-access check
- Tenant org-Q8X9T2KE (report channel), 5 Oct to 4 Dec (43 rows, 61 Amsterdam days): 894,042 calls, 149,007 reports (exactly 6 calls per report), 17,693,763,289 prompt tokens, 1,206,609,425 completion tokens.
- Docs rollup over the same Amsterdam days: busy 6.64M GPU-s above own requests; own requests = rollup requests less the tenant's calls (app+api billed requests give the same figure within 28 requests). Rollup sessions_new exceeds billing app+api sessions by 894,007, i.e. one per call (35 short of 894,042, noise level).
- Realised excess busy GPU-s at 1.6297 per own request: 6,642,388.
- lc2-fit prediction for the tenant's calls: 6,620,421. Ratio predicted/realised = 0.99669 (realised/predicted = 1.00332), within 0.4 per cent.
- Rescaling both rates by 1.00332: docs-prod shortfall 339.6 (W13), still the 340 bin. code-prod stays 299.3. The 335 to 345 bin holds for any rescale between about 0.985 and 1.025, so the check is robust to the ratio at several times its observed gap.

## 3. Rivals (ratio of predicted to realised excess; stopgap pool)
- Docs per-request rate 1.6297 x 894,042 = 1,457,020: ratio 0.219 (about a fifth). Docs peak shortfall 124.3, so code-prod (299.3) gets the stopgap.
- Two-rate fit on Docs' own hours: the mixed-model fit over all Docs hours is unusable (negative prompt coefficient, collinear tokens per request, ratio 3.6 or nonsense); the sensible version fits Docs' own lc2 hours only: 0.0413 / 2.282 ms, ratio 0.525. Docs shortfall 180.1, so code-prod gets the stopgap. (A non-negative fit on all Docs hours puts all weight on completion tokens, ratio 1.01 but no prompt rate; with a per-request term it is 0.26 and Docs 8 weeks of sparse variation. These fits are not what a careful analyst files as "Docs' own hours", and would need the model split to be defensible; flagged below.)
- Source pack computed once per report (shared across 6 calls), pack share f of the prompt: f=1.0 ratio 0.446, Docs 160.2; f=0.9 ratio 0.50, Docs 178.1; f=0.75 ratio 0.58, Docs 204.9; f=0.5 ratio 0.72, Docs 249.5. Every case leaves code-prod (299.3) first. The pack share is not in the pack, so the "under half" statement in the submission holds only for f of about 0.9 and above; at f=0.5 the ratio is 0.72, still 28 per cent short and still sends the stopgap to code-prod.
- All three rivals miss the excess by 28 per cent or more and flip the call to code-prod; only the fitted per-token costing lands on the excess.

## 4. New forks, inconsistencies, realism
No fork on the main call. Notes, none decisive:
- Tenant size: 3,960 reports per day on a settled day (~165 per hour averaged, under its 400 per hour contracted peak), 0.2 per cent of Docs' requests but about 1.3 busy GPUs on average. Plausible, not out of proportion.
- Submission step 4 says "within 2 per cent" and "a source pack computed once per report under half"; the data give 0.4 per cent and, for a pack computed once, a ratio of 0.45 to 0.72 depending on a pack share that is unfiled. The "under half" claim is true only if the whole prompt is the shared pack. Suggest softening to "well short" or filing the pack share. Not a determinism issue for the graded call.
- Contract figures: tenant contract RC-2026-031 (same org as early-access EA-2026-007) commits 148,700 reports for Q1 while the early-access tenant already ran 149,007 reports in 61 days (about 360k per 13 weeks at its current run rate). A committed volume below actual run rate is not contradictory (it is a floor and the policy uses contracted peak), but a careful reader could query it. Peak 400 per hour and RS-6 tier agree across the commitments, tiers, and usage files.
- Close-out Docs 1.6297 reproduces from the rollup (1.62965 over Q3); the early-access window's overall Docs rate is 1.6405, as expected with the tenant's load on top.
- Submission step wording "Docs' rate per request predicts about a fifth" matches 0.219.

## Summary
HOLDS. Main call unchanged: docs-prod 338.8 (to 340), code-prod 299.3 (to 300). Early-access ratio 0.9967 (rates fit within 0.4 per cent); rescaled Docs shortfall 339.6, in the 340 bin. Rivals predict 0.22 (per-request), 0.52 (own lc2 fit), 0.45 to 0.72 (pack once) and all send the stopgap to code-prod. Only soft findings: loosen the "within 2 per cent" and "under half" wording, and the pack share is unfiled.
