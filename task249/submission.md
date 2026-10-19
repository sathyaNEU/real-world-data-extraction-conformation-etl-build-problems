# task249 submission

## Tags

**Domain:** Psychology & Behavioral Science (psychometric measurement and scale validation: an assessment firm's unproctored adaptive aptitude test, MAT-R, checked by a proctored verification test, MAT-V, at client employers' selection days).
**Analytical objective:** Data Quality Monitoring & Alerting (how often the new verification check would refer genuine candidates at each client account in 2029, and so which accounts move to the extended verification before the season).

## 1. Final Recommendation

**Move 15 accounts to MAT-V Extended for 2029: KSP, VRD, ANV, PRM, SQR, ABH, MTL, TJM, SHY, TRG, PBH, KVR, RNJ, CHT, LVN; the other 13 stay on the 12-item MAT-V.**

On their 2029 plans each of the 15 would see its check refer at least 20 per cent of its genuine shortlisted candidates, against the 15 per cent cap of MAL-IS-04 section 3.3, while the other 13 stay under the cap. The equivalence study's own rates (2.3 per cent within three days, 6.6 per cent at six weeks or more) keep every account under the cap, because its volunteers were not shortlisted on MAT-R.

## 2. Critical Components

1. An account shortlists on MAT-R, so the candidates it invites are those whose MAT-R estimate ran above their ability, by more the smaller the share it shortlists (the eight finance, consulting and analytics accounts take 1.8 to 4.5 per cent of their applicants) and where MAT-R's standard error widens above +1 logit (Table 4.3); their MAT-V falls short of MAT-R by that much and s.3.2 reads the shortfall.
2. MAT-V sat soon after MAT-R runs higher (the study's retest gain, fitted 0.04 + 0.31 exp(-days/19.5) logit, 0.32 at two days): it keeps the mid-sized day-one accounts NVK, OJS, UJB under the cap, not the day-one accounts that shortlist most selectively, ABH, KSP, VRD, whose shortlisted candidates sit where MAT-R's error is widest.
3. The shortfall is read with MAT-R's error at the candidate's ability, not at the estimate. On the study's own top tenth of MAT-R scorers (223 volunteers), true-score shrinkage with Table 4.3's error at the shrunken ability predicts their mean MAT-V within a fiftieth of a logit of what they scored; with each volunteer's reported error (the error at the estimate, manual s.4.2) it predicts about a tenth of a logit too low, and the same shortcut on the accounts' pools moves NVK, OJS, UJB over the cap.
4. Carrying the study's own rates (2.3 per cent within three days, 6.6 per cent at six weeks or more) moves no account; one MAT-R error for every ability leaves ABH, KSP, VRD under the cap; leaving out the retest gain moves NVK, OJS, UJB over it.

## 3. Step-by-Step Solution

1. Pool per account: candidates whose 2028 result was shared with it (results_shared_2028.csv, PGL folded into NVK per client_accounts.csv, each candidate once), at their completed MAT-R attempt among registered candidates (mat_r_attempts_2028.parquet, candidate_register_2028.csv).
2. Depth: the 2029 plan's shortlist over its expected applicants (client_plans_2029.xlsx).
3. Interval from MAT-R to MAT-V: two days at day-one and first-company drives (Calendar sheet: sitting on day 1, selection day on day 3); otherwise the plan's selection days against the July 2029 test weeks.
4. Retest gain: equivalence study pairs, MAT-V minus MAT-R by interval in days (dates in the file), fitted by least squares weighted by pairs to c + a exp(-days/tau).
5. For each account: abilities drawn normal with the pool's mean and the pool's variance less its mean squared standard error; MAT-R = ability + error at Table 4.3's MAT-R value; the top share by depth shortlisted; MAT-V = ability + retest gain at the interval + error at Table 4.3's MAT-V value; referred when MAT-R exceeds MAT-V + 1.96 x MAT-V's standard error at its estimate; the referred share of the shortlisted.
6. Over 15 per cent: MAT-V Extended.
7. Exposure (MAL-IS-04 s.4): every attempt by a candidate in the register (interrupted attempts included; identities outside the register are not candidates, s.2), test weeks Monday to Sunday in IST, the distinct candidates shown each item over the week's distinct candidates; an item over 12 per cent in any week is rested for 2029.
8. Impersonations (s.5): one sitting per candidate a season, so a sitting's standing is the latest decision on any of the candidate's cases, the desk's appeal cases included (confirmed impersonation or confirmed on appeal stands; overturned on appeal or cleared does not); tier through the candidate register and the college register; per thousand distinct candidates on any 2028 shortlist.
9. Interruptions (s.6): a candidate's attempts in time order make up the season's booking, linked by candidate (from release 5.3.2 a restart carries a fresh booking reference); the booking's device is its first attempt's; interrupted when any attempt was interrupted; finished on another device when the last attempt ran on a different device.

## 4. Deliverable Answers

### verification_bands_2029.xlsx and account_referral_note_2029.pdf

**MAT-V Extended (15):** KSP (Kshitijpath Strategy Partners), VRD (Vardhanmaan Capital), ANV (Anvayam Analytics), PRM (Pramaanika Advisory), SQR (Sumedhika Quant Research), ABH (Abhyudayam Securities), MTL (Mitralekha Consulting), TJM (Tejomaya Asset Management), SHY (Sahyagiri Foods), TRG (Tarangini Telecom), PBH (Prabhatam Motors), KVR (Kaverika Life Sciences), RNJ (Ranjitgarh Energy), CHT (Chaitanyam Insurance), LVN (Lavanyam Retail).
**Standard MAT-V (13):** NVK, UJB, OJS, IDP, RNG, EKD, PGT, AKR, BHM, KTV, UDN, VKT, MDN.

### Item exposure, July 2028 test weeks (ceiling 12 per cent)

| Test week beginning | Items over 12 per cent |
|---|---|
| 3 July | 31 |
| 10 July | 10 |
| 17 July | 5 |
| 24 July | 5 |

Items to be rested before the 2029 season (over 12 per cent in any test week): 41.

### Impersonations standing confirmed, 2028

| College tier | Sittings confirmed | Per thousand candidates shortlisted |
|---|---|---|
| T1 | 5 | 2.5 |
| T2 | 62 | 3.5 |
| T3 | 273 | 10.8 |
| T4 | 244 | 22.6 |

### Interrupted bookings, 2028

| Device | Share of bookings started on it interrupted | Interrupted bookings finished on another device |
|---|---|---|
| desktop | 1.64 per cent | 29 |
| laptop | 4.74 per cent | 209 |
| tablet | 9.33 per cent | 88 |
