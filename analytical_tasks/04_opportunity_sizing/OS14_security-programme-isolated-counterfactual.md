# OS14 — Which security programme gets the $6M, when the controls already in place cut most of the attacks the biggest-looking programme would stop

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · cyber-risk investment |
| Mirrors | Choosing the security or reliability investment with the largest incremental effect when existing layers already cut the same failure chains (defence-in-depth programmes at Google and Microsoft, AWS resilience work where backups already cap outage losses, Meta integrity tooling layered on existing classifiers) |
| Decision shape | Which of N gets one scarce thing, with the sizing kept as the graded figure: one $6M programme, five candidates |
| Committed call | The programme funded next year, and the expected annual loss it avoids for the firm, to the nearest $0.1M |
| Gap · Pattern | Gap 3 (objective) over Gap 4 (rule) · the deciding comparison (#20), an isolated counterfactual on top of the existing control chain, with Pattern B for the scenario losses (a reproduction clause) and a coarsened segment (#14) below it |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #20 leaves the deciding comparison unstated · #14 coarsens the segment it was asked about · #1 reports a failed back-test, ships anyway |
| Calibration form | Published control set with a reproduction clause: the sector ISAC's 48 published expected-loss cells (12 scenarios × 2021–2024), with its incident file |
| Driving force | Priced against the gross scenario losses the sector consortium publishes, ransomware protection avoids the most. But the firm already runs an email filter, conditional access on remote logins and immutable backups, and its SOC chain log shows them letting through only 18% of phishing-led losses and 7.5% of remote-access losses. The comparison that decides is each programme's isolated counterfactual on top of that chain, built scenario by scenario from the log: ransomware protection and MFA add little there, while vendor-access control works on a chain nothing yet touches. |

## 1. Situation

A distribution company has $6M for one security programme next year: an email gateway upgrade, MFA on every login, endpoint
ransomware protection, data-loss prevention, or third-party vendor-access control. Its risk policy judges a programme on the expected
annual loss it avoids for the firm. The sector ISAC publishes expected loss per member firm for twelve threat scenarios each year, with
its incident file. The policy admits a loss model only if it reproduces every ISAC cell for 2021–2024. A convenience table rolls the
incidents into three broad categories. The firm's SOC logs every attack attempt with the stage at which it was stopped. The CISO wants
MFA everywhere.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the ISAC's published cells and incident file, the control-efficacy table, the convenience table and
  the SOC's chain log. The CISO is right that MFA stops more attacks than any other single control. No stakeholder read is overturned.
  The difficulty is the comparison the policy's "for the firm" requires, which no table computes.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the CISO's view and the convenience table. The ISAC-certified scenario losses times the efficacy table still
  rank ransomware protection first by 1.49×.
* **Instrument repair.** Record every incident at every peer firm perfectly. Gross scenario losses sharpen and still describe firms
  without this firm's controls.
* **Lens swap.** The naive read is a peer firm with no controls. The answer is this firm with its own chain in place, a different
  population, observed in the firm's own SOC log.

## 3. The driving force

A strong solver rejects the three-category convenience table, because the risk register names twelve scenarios and the ISAC publishes at
that grain. It finds that sample-mean severities reproduce only 31 of the ISAC's 48 cells, refits the tails, reaches 48 of 48 and
satisfies the clause. Ransomware protection then avoids $17.4M a year and leads by 1.49×. But the ISAC's cells are gross: they describe
a member before its controls. This firm's email filter passes 60% of phishing attempts, conditional access passes 30% of stolen-credential
logins, and immutable backups cut ransomware losses by 70%. On top of that chain, ransomware protection avoids $2.8M and MFA $1.7M. Vendor
access is attacked through suppliers' own accounts, which no current control sees, so it keeps its whole $5.2M.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Vendor-claimed efficacy × the convenience table's broad-category expected loss | A, email gateway ($22.0M) | The vendors' claims on the consortium's own category totals | The risk register's twelve scenarios and the ISAC's scenario-level cells: the categories mix scenarios each programme does not touch |
| 1 | Efficacy table × scenario expected loss, sample-mean severity | B, MFA ($12.9M, 1.35× over C) | The right grain, the class list the register spells out | The clause: sample-mean severity reproduces 31 of 48 ISAC cells |
| 2 | Efficacy × scenario loss with fitted-tail severity (48 of 48) | C, ransomware protection ($17.4M, 1.49× over A) | Every published cell reproduced, as the policy demands | The SOC chain log: the existing filter, conditional access and backups already pass only 18% of the losses ransomware protection targets |
| 3 | **Decisive:** each programme's isolated counterfactual, loss with the existing chain less loss with the chain plus the programme, scenario by scenario | **E, vendor-access control** (5th of 5 on rung 0), **$5.2M a year** | — | — |

* **Position table.** Vendor-access control ranks 5th on rung 0, 5th on rung 1 and 4th on rung 2, and leads only rung 3 (1.85× over
  ransomware protection).
* **Discriminator dominance.** Ransomware protection carries a 3.34× advantage into rung 3 ($17.4M against $5.2M). The existing chain
  leaves vendor access's scenario whole (multiplier 1.00) and ransomware protection's at 0.16, an edge of 6.18×, 1.54 times the 4.01×
  floor. Product: 6.18 / 3.34 = 1.85.
* **Partial correction priced (L3).** Every half-applied construction names a wrong programme. A solver who prices programmes on the
  existing chain but keeps sample-mean severities names DLP ($2.54M against vendor access's $2.02M, 1.26×), because sample means miss
  vendor compromise's rare mega-losses. One who applies the chain with one multiplier per broad category blends the access-compromise
  scenarios to 0.41 and names MFA ($4.73M against ransomware protection's $3.81M, 1.24×). One who discounts every programme by the
  firm-wide average leaves ransomware protection on top (1.49×), and one who credits only the backups names MFA ($8.85M against the
  email gateway's $6.66M, 1.33×).
* **Grid.** Chain grain (none, one firm-wide multiplier, one per broad category, per scenario) × severity (sample mean, fitted tail)
  gives 8 cells. Unchained and firm-wide cells name MFA (1.35×) or ransomware protection (1.49×); category cells name MFA (1.24×); the
  scenario chain on sample means names DLP (1.26×). Only the answer cell names vendor-access control.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy says "for the firm". No document says the ISAC's cells are gross of a member's controls, or that the
   SOC log measures the firm's chain.
2. **Corpus blind for a computable reason.** *In every published ISAC cell the loss is gross of member controls, because the consortium
   computes expected loss from incidents before any member's controls are applied.* The fitted-tail model reproduces 48 of 48 cells, and
   the cells cannot show what a control adds on top of another.
3. **No arithmetic symptom.** Scenario losses sum to the ISAC's category totals, the reproduction is exact, and the efficacy table
   multiplies cleanly at every rung.
4. **Not a row predicate.** The chain needs the SOC log's attempts grouped by scenario, each stage's pass-through computed, the stages
   multiplied, and each programme's counterfactual taken against that product.
5. **The enumeration is arithmetic.** No column gives a residual loss; the SOC log records stops, attempt by attempt.
6. **No cutover date.** The existing controls have run unchanged for the eighteen months of the log, and no series steps.
7. **Survives deletion.** Removing every voice and the convenience table leaves the clause-certified rung 2 intact and wrong.

## 6. The calibration corpus

* **Form.** The ISAC's published expected-loss cells (12 scenarios, 2021–2024) and its incident file.
* **What it pins.** Scenario grain and fitted-tail severity: tails fitted above each scenario's 95th percentile reproduce 48 of 48 cells.
  Sample means reproduce 31: they run low where mega-losses are rarely observed (phishing-led ransomware, vendor compromise) and high where
  one outsized loss sits in a short record, and their total falls 32% short, so they fail in aggregate too. Broad categories reproduce
  none.
* **What it is blind to.** The firm's own control chain (above).
* **Twin pair.** The Wholesale and Retail business units are identical on headcount, revenue band, scenario frequencies and gross ISAC
  losses. MFA would avoid $1.22M a year in Wholesale, which has no conditional access, and $0.55M in Retail, whose conditional access covers
  79% of its remote logins, 2.2× apart. Only the chain built from the SOC log separates them.
* **Resemblance points at the decoy.** Ransomware protection most resembles the ISAC's highest-value control case studies, all drawn from
  peers without immutable backups.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The risk policy: a programme is judged on the expected annual loss it avoids for the firm. The policy's clause: a loss
  model is admissible only if it reproduces every ISAC cell for 2021–2024 from the ISAC incident file. The risk register's twelve
  scenarios. The ISAC efficacy table by control and scenario. The firm's control inventory.
* **Empirical pins.** Tail severities, from the reproduction. Stage pass-through, from the SOC log (email 0.60, conditional access 0.30
  on stolen credentials and 0.25 on exposed remote access, backups 0.30 of ransomware loss).
* **Voices.** The CISO: "MFA stops more attacks than anything else we could buy. Every framework says so." The CFO: "Ransomware is the
  tail that can sink us."
* **Licensed wrong basis.** The policy records that the insurer's underwriting review scores programmes on the ISAC's gross scenario
  losses and will present that ranking.

## 8. Determinism by construction

* **Tails.** Maximum-likelihood and probability-weighted fits of the tails agree within $0.05M on every cell, and the reproduction admits
  only fits above the 95th percentile.
* **Independence.** In the SOC log, attempts passing two stages occur at the product of the stages' pass rates within 1%, so the chain
  multiplies.
* **Window.** The log's eighteen months show flat pass-through by quarter; any twelve-month window gives the same multipliers.
* **Scenario mapping.** Every SOC attempt carries one register scenario, and every programme's efficacy is filed by scenario.
* **Rounding.** Vendor access avoids $5.208M (0.84 × $6.2M), which rounds to $5.2M with $0.04M to the nearer bin edge.

## 9. Prompt sketch and deliverables

> I have $6M for one security programme next year, and our CISO wants MFA everywhere because it stops the most attacks. Which programme
> do we fund, and what expected annual loss will it avoid for us, to the nearest $0.1M? A one-line answer for the risk committee, plus
> `programme_case.xlsx`, a chart `loss_avoided_bases.png`, and a one-page `risk_committee_note.pdf`.

* `programme_case.xlsx` — the five programmes on four bases, the scenario chain, the ISAC reproduction, the simulation sheet (ask A) and
  the patch sheet (ask B).
* `loss_avoided_bases.png` — a script-rendered grouped bar chart: the five programmes' loss avoided gross and on the existing chain, side
  by side, ordered by the latter, with each programme's targeted scenarios' chain multiplier annotated and the $6M cost as a reference line.
* `risk_committee_note.pdf` — the committed programme, its figure, and the comparison that decides it against ransomware protection.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight business units, last quarter's phishing-simulation click rate and report
  rate. *Device:* a user who clicks the same simulated link from two devices appears twice under one campaign-user key, and the simulation
  guide counts a user once. Counting rows inflates click rates in the two units with most mobile users.
* **Ask B (device-carried).** For each of six server tiers, the median days from patch release to install and the share over 30 days.
  *Device:* a patch superseded before installation closes with `superseded_by`, and the patch standard times latency to the superseding
  patch's install. Treating superseded patches as never installed inflates the share over 30 days in three tiers.
* **Ask C (validity).** Each programme's loss avoided under each of the four rung bases, and ISAC cells reproduced (of 48) by sample-mean
  and fitted-tail severity.
* **Decoupling.** Pricing programmes gross instead of on the chain changes no figure in asks A or B. Simulation clicks and patch records
  touch neither the ISAC file nor the SOC chain log.

## 11. Rubric arithmetic

8 units × 2 (ask A) + 6 tiers × 2 (ask B) + 5 programmes × 4 bases and 2 reproduction counts (ask C) + the committed programme, its
figure, the runner-up and the margin + 5 named chart parts + 3 files ≈ 62 criteria.

## 12. World-building constraints

* Scenario losses ($M a year; sample mean / fitted tail): phishing-led takeover 10.5 / 9.0; phishing-led ransomware 11.0 / 24.0;
  remote-access ransomware 5.0 / 5.0; vendor compromise 2.4 / 6.2; insider exfiltration 3.6 / 3.0. The convenience table's categories:
  access compromise (takeover, remote-access ransomware, vendor compromise and credential stuffing, $24.0M), malware ($20.0M) and insider
  ($10.0M); vendor claims of 50% on access and malware, 75% on access, 82.5% on malware, 60% on insider and 10% on access give rung 0.
* Efficacy: email gateway 0.5 and 0.3 on the two phishing scenarios; MFA 0.85 takeover, 0.8 remote access; ransomware protection 0.6 on
  both ransomware scenarios; DLP 0.2 takeover, 0.6 insider; vendor access 0.84 vendor compromise.
* Chain multipliers: 0.18, 0.18, 0.075, 1.00, 1.00. Rung leaders A, B, C, E at 1.22×, 1.35×, 1.49×, 1.85×.
* Wholesale and Retail match on every ISAC-visible column.
* Simulation clicks and patch records never touch incidents, cells or the SOC log.
