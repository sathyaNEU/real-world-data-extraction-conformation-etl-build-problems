# DA26 — Which developer community gets the one pair-review launch slot, when an invitation only lands between people who share an organisation

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Product Analytics · developer-platform network growth |
| Mirrors | Seeding a collaboration feature through a social graph when the feature can only be used inside a shared workspace (GitHub organisations, Slack Connect channels, Google Workspace sharing, Meta and Instagram features gated to shared groups) |
| Decision shape | Which of N gets one scarce thing: the developer-relations team can staff one community's launch next month |
| Committed call | The community seeded with pair-review sessions, and the developers its seeding reaches, to the nearest thousand |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · Pattern B (the settled invite ledger pins which invitations can be accepted), with Pattern D (two grains of the connection graph) at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #5 takes the population a flag suggests · #4 never tests its reading against the control · #13 validates on one population, applies to another |
| Calibration form | Settled-transaction ledger: every invite credit offered in 14 closed onboarding campaigns, settled or expired |
| Driving force | The `connected` flag suggests that every connection carries an invitation. An invitation is only ever accepted when inviter and invitee hold memberships of the same organisation on the day it is sent, a pair property reached by an effective-dated self-join of the membership history. The flag agrees for most pairs, and disagrees exactly on the hub connections that make the connection graph's reach look large. |

## 1. Situation

A code-hosting platform launches pair-review sessions next month and its developer-relations team can staff one community's launch. Six
communities are candidates: Web front-end, Data & ML, Mobile, Infrastructure, Embedded systems and Game development. Seeded members get
the feature and invite their connections, whose acceptances spread it further. The launch plan judges the slot on how far the seeding
reaches. Fourteen earlier onboarding campaigns paid an invite credit whenever an invitation was accepted, and their ledger is in the pack.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the network-health dashboard's mean connections per member, the connections file, the membership
  history and the credit ledger. No stakeholder computes a ranking and nothing anyone reports is overturned. The difficulty is which pairs
  an invitation can travel between.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the dashboard. The connections file still yields a clean two-hop reach that names
  Infrastructure, and nothing in the pack says which pairs can accept.
* **Instrument repair.** Make every connection, membership and credit perfectly recorded: they already are. A complete ledger still has
  to be read against a membership history nobody joins to it, so the difficulty survives a better instrument.
* **Lens swap.** The naive population is every connection pair; the answer's population is the pairs sharing an organisation on the
  seeding date. They are different edge sets at a different moment, not one set under two lenses.

## 3. The driving force

A strong solver reads the launch plan's "two accepted invitations", counts two-hop neighbourhoods on the connection graph (which handles
the friendship paradox correctly), removes automation and organisation accounts as the data guide documents, and ranks. Every step is
right. But a pair-review session opens on a repository both people can access, and that only happens inside a shared organisation. The
ledger shows it absolutely: of 37,350 invitations between connections who shared no organisation on the invite date, none settled, while
co-member invitations settled at 41% in every campaign. Data & ML and Infrastructure reach far through connections to developers at other
companies. Embedded developers' connections are mostly colleagues, and contractors who hold memberships in several client organisations
bridge those clusters, so the co-member graph reaches furthest from Embedded.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Two-hop reach approximated from the dashboard's mean connections per member (members × k̄ × (k̄ − 1)) | A, Web front-end (1,630k) | The platform's own network statistic, a textbook reach estimate | The connections file: actual two-hop counts weight neighbours by their own degree |
| 1 | Exact distinct two-hop reach on the connection graph (Pattern D, the edge grain) | B, Data & ML (1,940k, 1.28× Web front-end) | Counts the graph itself and captures the hubs the paradox predicts | The data guide: automation and organisation accounts connect in bulk and cannot accept an invitation |
| 2 | Hygiene: two-hop reach on person accounts only | D, Infrastructure (1,150k, 1.31× Data & ML) | Clean, exact and reconciled to the dashboard's person counts | The ledger: no invitation between non-co-members ever settled |
| 3 | **Decisive:** two-hop reach on connection pairs sharing an organisation on the seeding date, person accounts only | **E, Embedded systems (640k, 1.56× Mobile)** (5th of 6 on rung 0) | — | — |

* **Position table.** Embedded ranks 5th on rung 0 (790k), 4th on rung 1 (980k) and 3rd on rung 2 (860k), and leads only rung 3. Rung
  leaders beat their runners-up by 1.25×, 1.28×, 1.31× and 1.56×.
* **Discriminator dominance.** Infrastructure carries 1.34× (1,150k against 860k) into rung 3. The share of each community's rung-2 reach
  that survives the co-member construction is 0.744 for Embedded against 0.340 for Infrastructure, an edge of 2.19×, against the 1.2 ×
  1.34 = 1.60 needed (1.37× headroom). The product, 2.19 / 1.34 = 1.63, is Embedded's lead over Infrastructure on rung 3.
* **Partial correction priced (L3).** A solver who builds co-membership but ignores `left_at` (ever co-members) names Infrastructure at
  1,010k, 1.44× Embedded's 700k, because infrastructure engineers change employers often and keep ex-colleague connections. A solver who
  instead transfers each inviter community's settled rate from the ledger onto rung-2 reach names Infrastructure at 276k, 1.75× Web
  front-end, with Embedded last: the onboarding cohorts' embedded inviters were hobbyists outside organisations and settled 11%, against
  24% for infrastructure inviters. Both partials land on rung 2's leader, and neither touches the answer.
* **Grid.** Counting (dashboard approximation or exact) × hygiene (off or on) × invitation population (all connections, ever co-members,
  co-members on the seeding date) = 12 cells. Eleven name Web front-end, Data & ML or Infrastructure. The nearest wrong cell is exact
  counting on the seeding-date co-member graph without hygiene: CI automation accounts are members of the large infrastructure
  organisations, so Infrastructure leads at 760k, 1.16× Embedded's 655k. Reaching it costs skipping a documented exclusion after finding
  the rule.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The feature note describes a session without saying where it can be opened. The launch plan says "accepted
   invitations". No document links acceptance to organisations.
2. **Pattern B, pinned by a construction.** The co-member rule reproduces 14 of 14 campaigns' settled totals within 1.6% at one pooled
   41.0% rate. The best rival (connection flag with each inviter community's rate) reproduces 5 of 14 within 10%, and its misses run one
   way on the forward set. The rule is a construction, not a menu: no row in any file carries co-membership, and the nearest columns
   (profile company text, same community, same country) recover 0.41 to 0.62 of the co-member pair set.
3. **No arithmetic symptom.** Invitations reconcile to settled plus expired credits, connection counts tie to the dashboard, and the
   membership file passes every key and interval check.
4. **Not a row predicate.** It needs a self-join of membership intervals on organisation, a test that both intervals cover the date,
   an intersection with the connection pairs, and a breadth-first count over the resulting graph.
5. **The enumeration is arithmetic.** Which pairs can carry an invitation is computed; no column says "can collaborate".
6. **No cutover date.** Memberships churn continuously and no series steps. The seeding date only fixes the snapshot.
7. **Survives deletion.** With every voice and the dashboard removed, the natural pipeline still stops at Infrastructure.

## 6. The calibration corpus

* **Form.** The invite-credit ledger: 61,300 invitations across 14 onboarding campaigns (2023–2026), each with inviter, invitee, send
  date and status. A credit settles when the invitee opens a session with the inviter within 30 days, and expires otherwise.
* **What it pins.** 23,950 invitations ran between co-members on the send date and 9,820 settled (41.0%; 40.6% to 41.9% in every
  campaign). 37,350 did not, and 0 settled. Every invitation went to a connection, so the `connected` flag cannot separate them.
* **Twin pair.** Campaigns OB-2024-03 and OB-2025-01 are identical on seeds (2,400), invitations (16,800), inviter community mix, inviter
  degree distribution and window. They settled 4,120 and 1,980 credits (2.08×), at co-member shares of 0.60 and 0.29. No community or
  cohort rate reproduces both.
* **Every rule exercised.** One campaign holds invitations sent the week after an inviter left an organisation (none settled) and one
  holds invitations between contractors with memberships in two client organisations (they settle at the same 41%).
* **Resemblance points at the decoy.** On inviter degree, connection density and community mix, Infrastructure resembles the two
  highest-settling campaigns.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The launch plan: the slot goes to the community whose seeding puts the feature within two accepted invitations of the
  most developers, seeded members excluded. Seeding goes to every account carrying the community label on the seeding date. The data
  guide: automation and organisation accounts cannot accept invitations.
* **Empirical pins.** Which pairs can accept, from the ledger joined to the membership history.
* **Voices.** The growth lead: "The paradox is the whole story; seed where the hubs are." The developer-relations manager: "Infrastructure
  people carry every launch we run."
* **Licensed wrong basis.** The launch plan records that the growth council ranks communities on connection-graph reach and will bring
  that ranking to the launch review.

## 8. Determinism by construction

* **As-of convention.** No membership starts or ends within 14 days of the seeding date or of any ledger send date, so inclusive and
  exclusive interval conventions converge.
* **Reach definition.** Distinct person accounts at distance one or two from any seed, seeds excluded, as the launch plan files.
  Connections are one row per mutual pair, so direction is not a fork.
* **Ledger maturity.** Every campaign closed more than 30 days before the extract, and no credit is pending.
* **Account classes.** `account_type` separates person, organisation and automation accounts exactly, and no person account is
  misclassed.

## 9. Prompt sketch and deliverables

> We can staff one community through the pair-review launch next month, and growth is convinced the friendship paradox picks it. Tell
> me which community gets the slot and how many developers its seeding reaches, to the nearest thousand, in one line for the launch
> review. Send `launch_slot.xlsx` with the sheets below, a chart `reach_by_basis.png`, and a one-page `slot_memo.pdf`.

* `launch_slot.xlsx` — the reach build for all six communities, the activity sheet (ask A) and the return-gap sheet (ask B).
* `reach_by_basis.png` — grouped bars of each community's reach under the four rung bases, the co-member basis highlighted, the chosen
  community marked, and the twin campaigns' settled counts inset.
* `slot_memo.pdf` — the committed community, its reach, and why each other community falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six communities, distinct developers who opened a session of the previous
  collaboration feature in each of the last six months. *Device:* the account-merge log maps retired IDs to surviving IDs; counting raw
  IDs double counts 3,900 developers in the months before their merge. Connections migrate on merge, so the graph is untouched.
* **Ask B (device-carried).** For each community, the median days from a developer's first to second session of that feature. *Device:*
  the logging spec splits a session crossing midnight UTC into two rows sharing a `session_id`; reading rows as sessions puts a false
  day-0 return on 18% of developers and drags two communities' medians to zero.
* **Ask C (validity).** Each community's reach under each of the four rung bases.
* **Decoupling.** Clearing the co-member construction changes no figure in asks A or B.

## 11. Rubric arithmetic

6 communities × 6 months (ask A) + 6 medians (ask B) + 6 × 4 bases (ask C) + the committed community, its reach and its margin + 5 named
chart parts + 3 files ≈ 77 criteria.

## 12. World-building constraints

* Rung figures (thousands): rung 0 A 1,630, C 1,300, B 1,140, D 1,020, E 790, F 600; rung 1 B 1,940, A 1,520, D 1,210, E 980, C 890,
  F 610; rung 2 D 1,150, B 880, E 860, A 790, C 700, F 520; rung 3 E 640, C 410, D 391, A 380, B 300, F 260.
* Ledger: 61,300 invitations, 23,950 co-member (9,820 settled), 37,350 not (0 settled). Co-member rates 40.6% to 41.9% per campaign.
* Twin campaigns identical on every visible column, settling 4,120 and 1,980. Ever-co-member reach: D 1,010, E 700. No-hygiene
  co-member reach: D 760, E 655.
* No membership change within 14 days of any send date or the seeding date. Merges and midnight splits never touch a membership or a
  connection pair.
