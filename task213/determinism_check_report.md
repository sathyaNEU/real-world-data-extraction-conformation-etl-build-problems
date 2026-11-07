# determinism-check report, task213, 2026-11-07

Architecture 1 (Calabash Exchange's Q3 2026 rating-ring sweep for the 1 December integrity notice).

## Pass 1 (target.zip c745b735, judge thread run by the coordinator)

**Verdict:** DETERMINISTIC. **Disposition:** APPROVE, no fix required, no rerun. Order kept: derivation.md was written
from prompt.txt and target/ alone before graded_blocks.md and graded/ were opened. Every golden figure reproduced: the
five rings (241 accounts), 6,517 Q3 ratings given, 597 held, 5,920 expunged and the notice figure 5,900; every dispute,
withdrawal and cashback figure. Gate F strong: the shared-phone route, with the agent-point tablets correctly set aside,
finds two rings and files 2,400. Gate G etl_conformance (entity resolution across devices, wallets and ratings, then a
stated cap), analytical_non_defect, no surface-read dependency, no sole data defect. Gate H domain pass, layers pass,
decisive step analytical.

The coordinator's note on Gate F: the thread's own blind derivation found the three device-less rings as closed wallet
clusters before it opened the graded blocks. That is the build's known stump-power risk, recorded in the pre-ship check
as for task211 and task210: the route a strong analyst takes after reading everything correctly (shared phones, tablets
excluded) still files 2,400, and the portal is the only stump oracle.

The judge's three forks, ruled:
- **A withdrawn-only case counts as a dispute or not** (NG 978 against 837; the decided-for-buyer column unaffected).
  Closed in the prompt before ship, as the judge's optional pin 1 asked: the asking sentence now reads "each market's
  Q3 disputes (orders with a case opened on them, withdrawn or decided, each counted once)". The sentence files the
  counting unit only; which order a case is about stays with SD-04 1.2 and the escrow's own times, where the ask's
  device sits.
- **Whether device-less closed wallet clusters count as run together** (5,900 against 2,400). Not pinned: the sentence
  that would close it names what the decisive step recognises, so the fork is the stump (`stumping` 1.2), and the judge
  found the evidence data-forced (closed funds, no external withdrawals, one market per ring, dense mutual ratings, and
  no competing cluster carrying any of them).
- **Ring labels and order.** Closed in submission.md, as the judge's optional pin 2 asked: each ring line now names the
  ring by its account count, in any order and by any of its accounts, with its busiest seller kept as a reference.

Neither pin changes a file in the pack or a graded figure: target.zip rebuilt byte-identical (c745b735), figures_check 71
of 71, checks 62 of 62, verify 36 of 36. No re-judge, the disposition being APPROVE; the prompt change was re-read by the
leak reader (leak_check_report.md, round 2).

### The thread's verdict, verbatim


Order kept: yes. I read prompt.txt and all 17 files in target/, wrote derivation.md (with every figure), and only then opened graded_blocks.md, graded/q3_ratings_sweep.xlsx, graded/q3_sweep_chart.png and graded/metadata.json.

- **Verdict:** DETERMINISTIC

- **Disposition:** APPROVE. Two optional wording hardenings are listed under Fix (they pin a reading and do not change the pack); no rerun is needed.

- **Why:** Every committed answer (main figure and all supplementary figures) reproduced exactly from the shipped files in my blind derivation: 5 rings, 241 accounts, 6,517 Q3 ratings given, 597 held, 5,920 expunged, notice 5,900. The ring set is forced by the data, because five wallet-closed clusters carry 700 to 1,036 internal ratings each, while every other shared-device or wallet cluster has zero ratings among its members and so fails playbook 2.1 ("trade with one another"). The wrong-basis files (Q2 notice, transparency report) are ruled out by the playbook (3.1) and by the report's own statement that no Q3 sample exists yet.

- **Evidence (recomputed; all match the golden):**

| Item | My value | Golden | Source |
|---|---|---|---|
| Rings (accounts) | 55, 53, 50, 44, 39 = 241 | same | wallet_ledger transfer components with internal ratings, device_links, ratings |
| Ratings given (latest version, first given in Q3 UTC) | 1,341 / 1,379 / 1,355 / 1,179 / 1,263 = 6,517 | same | ratings_2026q3.parquet (190,425 ratings, all v1 in Q3) |
| Held (3.3, seller-role cap, floor half) | 186 / 131 / 153 / 91 / 36 = 597 (13 sellers capped) | same | ratings ratee_role=seller |
| Expunged | 1,155 / 1,248 / 1,202 / 1,088 / 1,227 = 5,920, so 5,900 | same | |
| Disputed orders / decided for buyer | NG 978/557, GH 354/209, KE 367/210, GB 107/62 | same | support_cases + orders |
| Withdrawals by UTC confirm month (USDT, fees) | Jul 1,361,363 / 14,862; Aug 1,429,646 / 15,605; Sep 1,421,931 / 15,102 | same | custodian_outbound, hot-wallet rows only |
| Cashback (USDT, buyers) | NG 1,856/815, GH 191/81, KE 613/289, GB 130/51 | same | wallet_ledger + Groups/Desks |

Traps I confirmed and that the golden handles correctly:
  - Device sweep: the 22-character fingerprint format (app 5.x) is linked to the old 16-hex format (app 4.x) only through exact old.last_seen_ms = new.first_seen_ms on the same account.
  - Tablets: the 45 Calabash Point tablets (calabash_points.csv; 8 lack a v5 fingerprint) must be excluded (playbook 2.3). Left in, each is a false ring of 30 to 140 accounts.
  - Further shared devices: about 50 other shared devices and 1,158 two-account shared devices have zero ratings among their accounts and are not rings.
  - Device-evident rings: devices alone reveal only 2 rings, giving 2,357 expunged (2,400). The other 3 rings (NG 53, KE 44, GH 39) share no device and show only as closed wallet clusters.
  - Holdback: it is a seller-role cap only; buyer-role ratings (4,063) are expunged in full. Variants give 4,782 or 4,820 expunged, and no holdback gives 6,517.
  - Disputes: order_ref is stale for 465 of 2,450 cases (the cited order closed before the case opened). The true order is found with SD-04 1.2, the customer's role from the category, and opened_wat -1h inside the order's escrow window. Decision time equals the order's closed_at for all 2,450. Citing order_ref instead gives 1,995 orders, not 1,806.
  - Dispute decisions: "for buyer" means a buyer's U or a seller's R. This equals the order ending released after a decision, and the 499 returned orders were decided for the seller.
  - Withdrawals: the ledger splits withdrawals above 1,000 USDT into several rows, while the custodian makes one transfer. The 12,436 custodian rows that are deposit-address sweeps into the hot wallets are not withdrawals.
  - Ledger clock: the ledger clock is unlabelled Lagos time (confirmed minus posted-as-UTC is 3 to 40 minutes), and the extract is exactly Q3 in UTC.
  - Cashback: four groups moved their treasury wallet in early August. The register (as of 30 Sep) lists only the new wallets, and the old wallets' July and August cashback adds NG +42 (1,814 to 1,856), KE +155 (458 to 613), GH +23 (168 to 191) and GB +21 (109 to 130) USDT, with buyers NG 801 to 815, KE 235 to 289, GH 72 to 81, GB 48 to 51. The treasury-to-treasury balance transfers (4) are not cashback. Eleven recipients are closed accounts whose wallet_no is blank, so buyers must be counted by receiving wallet.

Forks (reasonable alternative readings):

| Fork | Answers | Assessment |
|---|---|---|
| A withdrawn-only case counts as a dispute or not | NG 978 / GH 354 / KE 367 / GB 107 vs 837 / 301 / 311 / 88 | The "decided for buyer" column is unaffected. The golden reading is the better one (W is a recorded outcome of a case on an order, and the Q2 report counts all closed cases), but the prompt does not say so. Low-moderate risk. |
| Whether device-less closed wallet clusters count as "run together" | 5,900 vs 2,400 | The package has no sentence that defines the linking evidence. The evidence is data-forced: closed funds, no external withdrawals, seeded by a few deposit addresses, one market per ring, and dense mutual ratings. No competing cluster has any of these. Low-moderate risk. |
| Ring labels and order | n/a | The golden names rings by their busiest seller and the prompt does not pin a label. Graded figures per ring are label-independent. |

Gates: A pass (blocks agree with each other and the files). B pass (every decisive fact is shipped: playbook 1.2/2.1 to 3.4, SD-04 1.2 and 2.1, MP-2 1.2, the custodian and ledger data, the outcome-code sheet). The 30 Sep register, the unlabelled Lagos ledger clock and the closed-account wallets are recoverable from the files. C pass with the two low-moderate forks above. D pass. E pass, with the dispute-definition pin suggested below.

Cross-batch check: I have no other task material in my folder (reading elsewhere is barred), so I cannot clear the cross-batch fingerprint; the author's guard covers it.

- **Files/Hygiene:** PASS. 17 shipped files in 4 formats (6 csv, 4 parquet, 2 xlsx, 5 pdf), with no README or tool banners in target/. Synthetic and generated wording sits only in graded/metadata.json (not a solver file). Documents are terse operational artifacts, not explanatory prose. Two declared wrong-basis distractors (transparency_report_2026q2.pdf, integrity_notices_2026.pdf) are relevant and unused. Temporal coherence holds (setting 2026-11-05, Q3 data, register as of 30 Sep, ledger extract equal to Q3 UTC). Layer-1 mess is genuine: fingerprint format migration, WAT vs UTC, released_at renamed settled_at from August, handle changes, split withdrawals, treasury move, closed-account blank wallets. Nothing exclusion-level.

- **Stump power:** Strong. The easy route (link accounts by shared devices, correctly excluding the tablets) gives 2 rings and 2,400, and a reader who also skips the holdback files 6,500 or so. Reading the Q2 notice or prevalence figure gives a wrong-basis scale. Only a solver who rebuilds the funds-flow structure behind the ratings finds the other three rings. The ask layers each carry their own cross-system reconstruction (stale case refs, split withdrawals and sweeps, the moved treasury), and no single ask is solved by a stated rule.

- **Stumping type:** `mechanism: etl_conformance (entity resolution across devices, wallets and ratings, then a stated cap)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported figures (notices, ratings, ledger) are all correct as shipped and the difficulty is reconstructing who is run together and applying the quarter and holdback correctly. On clean data it would still stump, since the device shortcut would still miss the three device-less rings.

- **Three rules:** `domain: pass`, `layers: pass` (Layer 1 is migration, timezone, stale key, split-row and moved-wallet mess; Layer 2 is collusion-ring detection from transaction and device structure), `decisive_step: analytical`. Trust-and-safety integrity analysis (coordinated-network detection, then the capped sweep) is the field's own work, and the swap test fails to reproduce the task with another field's nouns. The decisive step is the unit of analysis (a ring as a transaction-closed group, not a shared phone), and a strong analyst who read every rule correctly could still use shared devices and file 2,400. The holdback is a stated rule, but it is a lower step.

- **Fix:** none required (location: none). Optional prompt-side pins, neither changing any file: (1) say that a dispute is any case opened on the order, withdrawn or decided, so the 978/354/367/107 reading is closed; (2) make the rubric label-independent for ring names and order.
