# The register era's data traps, instance by instance

> **Source.** The design notes, generators, answer keys and submissions of tasks 1 to 24, the builds that carried
> their difficulty in planted data-quality devices aimed at the main answer (`task20/DATASET_NOTES.md` names tasks 10
> to 23 the register-era spec). The shipped ledger has no rows for them: portal results exist only for task16, task17
> and task20, recorded in those builds' own notes. SKILL.md Part 4 holds the families these instances belong to; this
> file holds what was actually planted, what a habitual sweep sees, and what each one measured.
>
> **Hygiene key.** **N** no default sweep surfaces it · **W** a sweep surfaces it but the habitual repair is wrong ·
> **T** the habitual tie passes on the wrong path.
>
> **Evidence tiers.** **[M]** portal result · **[I]** internal panel or rollout · **[B]** built, no recorded outcome ·
> **[X]** died.
>
> **These instances were aimed at the main answer**, which Gate G now bans (`planted_defect_flip`). Their mechanisms
> are reused at the ask layer, behind the separation proof in SKILL.md Part 1, never on the main path.

---

## Part 1. The instances, by family

### D1 duplication and identity

- **task10 T8, replay under fresh ids [B].** A June migration re-emits subscriptions under new `subscription_id`s,
  one day later and off in the fourth decimal, and the copies reach the capture feed too. Genuine same-date pairs
  punish a business-key dedup (law 5). Organ: `psp_batch_totals.csv`, where 202 of 465 batches overshoot. **N**:
  invoice-to-capture counts tie, and only the amount tie to batch totals fires. (`task10/SOLUTION.md`,
  `build/gen_data.py`)
- **task9 T6, content clones [B].** Sessions and purchases are cloned with only the primary key changed. Organ: a
  dedup on content; the clones also break uniqueness of `purchases.interaction_id`. **W**: exact-duplicate and
  primary-key checks come back clean.
- **task7 tag-v2, a second source of the same traffic [B].** A second tag container (31,225 rows) mirrors one
  section's traffic with fresh row references and tags 62 per cent of one funnel's steps as success. It is
  volume-neutral, so totals tie. Organ: the funnel compared across sources, 94 against 56 per cent. **N**.
  (`task7/scripts/DESIGN_V3.md`)
- **task18 N1, repeated keys with opposite meanings [I].** A repeated key is either a staggered regional pair (keep
  both rows) or a replay under a fresh `capture_batch` (drop it), and no row is byte-identical. Equal volumes and the
  weekly fill-rate file give it away. **W**: both earlier panel reports collapsed on the key.
- **task16 T5, recycled reference numbers [M].** A blanket dedup on PRO numbers deletes 299 real shipments. On the
  portal, revision 2 scored 46 and 25; by revision 3 both top responses filed all 15 figures, the 494 migration
  duplicates included. Battery-visible duplicates are solved at scale. (`task16/DATASET_NOTES.md`)
- **Earlier builds, same family [B]:** Rock invoice lines copied under new ids plus "(1)/(2)" export copies (task2),
  `remove_from_cart` clones (task3), a re-delivered batch of 140 identical settlement ids (task4), near-duplicate
  installment rows (task5), a re-run under fresh event ids and 82 companies duplicated under a second tenant
  (task8), case-sensitive ids that a casefold join double-counts (task19).

### D2 version, vintage and stored labels

- **task14 event rename [B].** A dated label change, so a filter on the old label drops the later rows.
  (`task14/solution.md`)
- **task24 catalog snapshot [B].** The catalog is a snapshot taken after a line change, so attribution has to use the
  transaction date, not the snapshot's line.
- **task23 D1, a withdrawn restatement [B].** `billing_arr_restatement_2026Q2.csv` covers exactly the blank values
  (category A below) and was withdrawn; 140 of its 200 rows match the receivables backfill. **T**.

### D3 meaning, units and encodings

- **task14 short-year dates [B].** 123 `effective_from` values read `25-09-23`, which pandas parses as 2023-09-25,
  and the misparse flips the answer. Organ: every other year in the column is 2025. **N**.
- **task11 T1, mixed quote direction [B].** FX quotes run both ways and survive `gmv + discount = mrp`, so the
  identity confirms the wrong read. **T**.
- **Earlier builds [B]:** zero-width characters in `user_id` (task1), NBSP and ZWSP inside tier labels (task3), a
  capture with no currency so INR reads as USD (task4), an email in `seller_id` (task5).

### D4 absence and sentinels

- **task13, evidence as absence in another file [B].** 282 of 543 disputes coded 13.1 have no line in
  `ticket_transfer_errors.log`, which means the ticket was delivered and the dispute is fraud. Organ: the log header,
  "a transfer that completed before event start emits no line". **N**: no habitual join reaches the error log.
- **task15 S1, an absence recovered from logs [I].** 260 treatment activators have no row at all after a release.
  Organ: the metric definition, which names no table, plus the service log; the control arm reconciles exactly.
  **N**. Version 3 was solved internally; version 4.1 is untested.
- **task23 A, blanks missing not at random [B].** `arr_usd` is blank on 200 migrated multi-year accounts averaging
  $500k against $148k for the populated ones. **W**: a null check finds the blanks, and `.mean()` is the wrong repair.
- **task12 T8, a drain-down channel [I].** 1,419 orders routed through a third-party warehouse reach neither the order
  file nor settlement, and the cutover drains in stages (50, 25, 10 per cent), so a split by date misclassifies.
  Organ: the manifest anti-joined against the order file. The build was solved internally at version 2.0; version
  2.1, which carries the harder traps, is untested.

### D5 scope and population

- **task14 sandbox accounts [B].** 118 accounts with a "(Sandbox)" suffix are typed `customer`. Organ: the partner
  runbook. **N**.
- **task22 B, zero-consideration rows [I].** A zero-charge plan inflates the ledger, the export and the manifest
  equally, so all three tie at 0.00 per cent. Organ: `net_price == 0` in the price book and the consideration rule.
  **T**. One panel report found it, and "it cost it one paragraph".
- **task22 C, a habitual repair right for one population [I].** Billing-correction rows return with blank region
  and currency, and North America is also written blank. Organ: the currency column and the correction notes.
  **W**. A single-market version fell to elimination.
- **task17 X0, misclassification across a category boundary [M].** Six property lenders file development lending as
  agriculture because of its collateral, putting MRK 48.7bn in the farm book. Organ: the manual's section 5;
  collateral is 100 against 0 per cent. **N**. On the portal it stumped one top response until the full section 5
  procedure was filed, after which both landed. (`task17/DATASET_NOTES.md`)
- **task6 [B]:** auto-generated orders with no marker, beside an incomplete incident list.

### D6 grain and aggregation

- **task20 DEC-6, an event quantity on every line it covers [M].** One disposition event's quantity repeats on every
  receipt it covers (10 references, up to four times each). Organ: the repeated reference, date and quantity, and
  lines larger than their own receipts. **W** in principle, yet on the portal "the responses summed the fanned-out
  lines" on the asks (92.0 per cent yield against 97.4808). Both top responses still landed the main call, so the build
  was not stumped, and on the main path the device was judged `planted_defect_flip`. (`task20/DATASET_NOTES.md`)

### D7 keys and linkage

- **task4 [B]:** identity carried by `email_alias`, not the account key.
- **task16 T10 [B]:** `delivered_ts` overwritten with the plan date.

### D8 time and clocks

- **task11 T3 [B]:** lines stamped with the settlement date where the order date is needed.
- **task19 R-DERIVE [B]:** tenure anchored on the current contract rather than the first.

### D9 self-validation (false cleans)

- **task12 T9 [I].** A reconciliation flash reports 19,161 = 19,161 with $0.00 variance, true within its own scope,
  beside a false incident closure.
- **task13 T6 [B].** The trailer count ties to the un-deduplicated parse.
- **task21 DEC-R, a derived measure to rebuild [X].** A hotfix batch leaves `full_pallet_eaches` out of the bronze
  `qty_eaches`; row parity and the goods-receipt tie both pass (**T**). Two internal rollouts defused it: the
  component names gave the identity away, and `goods_value_usd / qty` inverted straight to the answer. (Law 8: the
  answer must not invert from another column.)

---

## Part 2. What the record supports

- **Battery-visible duplicates are solved at scale** (task16 revision 3, 494 duplicates removed by both top
  responses), so a D1 device ships only with its over-cleaning half (task10's genuine same-date pairs, task16's
  recycled numbers).
- **Filing the full adjudicating procedure hands the device over** (task17 X0, solved by both once section 5 was
  complete; task105 v4 at the ask layer, every filed device rule executed). The rule is filed, its relevance is one
  uninvited question away (law 1).
- **Answers that invert from another column are defused** (task21 DEC-R), and so are components named for what they
  are.
- **False cleans run through most of the sets** (task12 T9, task13 T6, task21's row parity, task22 B's three-way
  0.00 per cent tie, task11's identity): every control that ties on the wrong path certifies the wrong number (D9).
- **Absence in another file needs no camouflage**, because no default join reaches the file that carries the
  evidence (task13's error log, task15 S1's service log). None of these instances has a recorded outcome in its
  final form, so the record does not yet measure how quiet they are.
