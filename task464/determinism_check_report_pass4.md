# task464 determinism, pass 4: the main call's fork is not repairable, and the four procedural fingerprints

Architecture 3. Written by the build thread, not by a judge, after the stage-4 re-judge returned
NOT_DETERMINISTIC, SEND_BACK, and the author ruled that the architecture's decisive step is spent. The raw
verdict is beside this file as `determinism_check_report_pass4_raw_verdict.md`. Architecture 2's two reports
and pass 3 are history and are untouched.

## The verdict, as the judge filed it

`competing_defensible_answer` on the MAIN CALL, by `underspecified_objective`. Schedule 4 clause 4.2 defines
deliverable positions as "the treatment positions a Site is able to operate simultaneously" and nothing in the
pack files what evidence fixes that count, so three readings are reachable and each one changes the call:

| Reading of clause 4.2 | Positions | Weekly treatment slots | Areas below the standard |
|---|---|---|---|
| the concurrency sweep over the four-year record (the golden) | 274 | 3,886 | 6 |
| the stations the provider directory attests | 327 | 4,668 | 3 |
| the stations the state licence register holds | 351 | 5,006 | 2 |

Only inference, or the write-up's own "Not the stations the directory attests", picks the golden. Every golden
figure reproduces from the bundle, so there is no `solution_incorrect`: the finding is the objective, not the
arithmetic.

## Why no closure was attempted

The judge's own suggested fix is the thing rule 3 bans. It asks for a sentence in clause 4.2 filing that
positions are evidenced by "the site's own treatments running at the same time in the encounter extract".
"Running at the same time" is the concurrency sweep, so that sentence files the HOW and turns the decisive step
into rule application.

The stump test from `/fix-determinism` step 3 then fires in both directions. The default path's entire error is
taking the attested 327, so any closure that forces the golden reading tells the analyst not to take it, and the
construction becomes the only route left. A selection criterion in general terms (the Site's own delivered
service record, not a count it attests or is licensed for) is section 1's named escape and is WHAT rather than
HOW, but its second half is the insight itself. Deleting the attested and licensed counts closes Gate C and
kills Gate F together. Gate C and Gate F ride one dial in this architecture with no middle, which is what
task184 and task198 each measured from their own slots the same day. Keeping the fork open to keep the stump is
banned outright, so the architecture is re-rooted rather than repaired, and the author's ruling supersedes the
earlier one that the build ships with the Gate F risk recorded.

## The three residual ask-side forks the judge named, for the redesign's note

- The `line_no` 0 claim header lines in the out-of-network claims: the judge read Ammerly H1 as 667 treatments
  and 11.1 per cent against the golden's 572 and 9.7. This is ask A's primary device and it is working, but the
  asking sentence does not say which line grain counts a treatment.
- The four sites whose 2026 filing area differs from the directory and the register, with ask 4 not saying
  "current area" in the asking sentence.
- Ask 4's denominator.
- A minor temporal conflict: the transmittal says the extract was pulled 2027-01-05 while clause 4.4 says it is
  taken after the ninety-day run-out.

## What this pass changed, and what it did not

Nothing on the determinism side. Clause 4.2, the ladder, the stump sentence, the three rules, the fork table and
every graded figure are as pass 3 left them, and no closure of fork 1 was attempted.

The four procedural fingerprints from the second leak read are fixed, because the world and the pack carry into
the next architecture:

1. Plan site ids stepped by 37, licence numbers by 23, street numbers by 53, and the tax, claim, member and
   encounter keys by their own constants. Each is now issued from its own stream with uneven gaps.
2. The twelve area names ran A to L in service-area-code order. The mapping is shuffled.
3. Every site was named "<Locality> Dialysis Center" or "<Locality> Infusion Center". A site is now named from
   fifteen templates, one of them carrying an operator's own brand, and fourteen distinct shapes appear across
   the 72 sites in the pack.
4. The licence register reported a position date three days after its own file date. Every document now
   carries its own date and states nothing later than it: the register is produced the evening of the position
   date it reports (2027-02-19 16:42), the two plan exports the next morning (08:12 and 09:05), the agreement
   the week its board approved it (2026-12-14) and the fee schedule the week before it took effect
   (2026-06-24). The three workbooks no longer share one timestamp to the second.

Two smaller items from the same read: the empty `<workbookProtection/>` element the writer emits is stripped,
and a synthesised `sharedStrings.xml` was refused, with the reason in the design note. On clause 4.4's delivery
period sentence, the build thread's reading is that it does not over-steer the out-of-network asks: it closes the
date basis, which is a convention, while ask A's device is the claim header grain, which the sentence says
nothing about and which the judge itself then walked into.

`checks.py` asserts all five shapes, 30 new assertions: twelve id-bearing columns each stepping by at least six
distinct amounts and none by a constant, the names in code order differing from the names in alphabetical order,
more than two name shapes, no two sites sharing a name or an address, and no workbook stating a position or pull
later than its own file date.

## Which graded figures moved

None. `figures.json` differs from pass 3 in exactly two places, neither of them a figure:

- the 40 site-id labels under `site.*`, whose slot values are identical in order (80, 80, 126, 40, 96, 120, ...);
- `call.nearest_short_area`, "Durnsfield" to "Hesper Vale", which is the same area, SA-04, under the name the
  shuffle gave it. Its shortfall is still 20 slots.

Every other leaf of the 211 is unchanged: 3,886 weekly treatment slots, 3,568 required, 6 areas below, the flip
set SA-02, SA-07 and SA-11, 274 positions against 327 attested, all 12 area slot totals and all 96 ask figures.

## Bearing on the re-judge

The re-judge ran against the pack as pass 3 left it, so its verdict describes that pack. Nothing in this pass can
bear on the finding: the fingerprint fixes touch identifiers, names, container dates and one empty XML element,
and the finding is about what evidence clause 4.2 points at, which no identifier or name reaches. The one
cosmetic consequence for the record is that the area the verdict would call Durnsfield is now called Hesper Vale,
and that the judge's own table above keeps the names it was written with.

## Gates re-run after the fix

| Gate | Result |
|---|---|
| `generator/build.py` | 682 assertions passed (652 before, plus the 30 procedural assertions) |
| `generator/verify.py` | PASS, bundle only, own code path: 40 sites, 12 areas, 96 ask figures |
| two rebuilds | byte-identical, `target.zip` md5 `c0e0dfcfcc8ecf0bc864f9e4b9eb8d7a`, `figures.json` identical |
| `figures_check.py` | PASS, 146 figures in blocks 1 to 4, 0 absent |
| `leak.py --asof 2027-02-19` | REVIEW, no LEAK, the same five REVIEW lines the design note answers |
| `precut.py` | exit 0, 52 checks, 0 FAIL, 0 WARN |
| `voice-check.py` | PASS, prompt.txt at 998 characters |
| `generator/ceiling.py` | cracker 0 of 48, 0 of 24 and 4 of 24; pair ceiling 30.8; mirror leakage 4.2 per cent |
| `guard.py surface` | clean, nothing of this build's own in the repeated-filename or deliverable screens |
| `guard.py heart` | WARN, no BLOCK, nearest neighbour 0.05 (task181); the persona note is the card's, which this thread does not edit |
