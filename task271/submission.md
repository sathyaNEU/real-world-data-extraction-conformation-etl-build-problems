## Tags

**Domain:** Survey Research & Official Statistics (nonresponse, calibration and measurement error adjustment).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Trevanna should put the 2027 Community Engagement Support navigator teams in Pierce, Spokane, King and Thurston-Mason.**

Estimated over every member the survey sampled, reached or not, these four have the smallest shares of expansion members who worked 80 hours or more in March 2026 (42, 44, 46 and 47 per cent). Not North Sound, which the interviewed members' own answers put among the four: members in work rarely answer a weekday daytime call, so the members never reached are mostly members in work, and North Sound's calls went out mostly by day from the Member Services Center. Not those answers reweighted to each region's age and sex, or the members reached late carried to the members never reached, which leave that gap in place and name North Sound again.

## 2. Critical Components

1. **3,204** of the 15,000 sampled members were never reached, and the survey's answer is known for **11,544** (10,635 completed interviews and 909 members who declined but answered the key question).
2. Across all 15,000 sampled members the estimated share who worked 80 hours or more is **51 per cent**, against **41 per cent** of the members interviewed.

## 3. Step-by-Step Solution

1. Took the 15,000 sampled cases in mwis_2026_sample.csv and their survey calls: Kestrelby's from kestrelby_mwis_dialer_export.csv (the February pilot's MW26P cases and the TEST calls left out) and the Member Services Center's MWIS outbound calls from trevanna_msc_mwis_activity.xlsx, joined on member ID, each call placed in its window by Pacific time (weekday day, weekday evening, Saturday).
2. Read each case's calls in time order to the first that reached the member (dialer 1100 or 2110, CRM Spoke to member): 10,635 completed, 1,161 declined, 3,204 never reached.
3. Took the class from mwis_2026_interviews.csv, total March hours of 80 or more for a completed interview and the key question's answer for a member who declined (TEST rows left out), known for 11,544 members.
4. Fitted a latent class callback model by EM to every sampled member's calls: each class's chance that a call in each window reaches the member, the same in every region; a reached member's chance of declining the same in either class; each region's share of the class; members of unknown class weighted by their posterior.
5. Averaged each region's 1,500 members (known class or posterior) and ranked the regions unrounded (criteria 2.1 to 2.4): Pierce 42, Spokane 44, King 46, Thurston-Mason 47.
6. Members covered on 1 October 2026 (criteria 3.1 and 3.2): the roster's members whose enrollment began by 1 October and had not ended, with members the change log terminated on or after 1 October restored (including those enrolled again later in October) and each member at the county before any move logged after 1 October, aged 19 to 64 on that day, by the county's region in apple_health_regions.xlsx.
7. Parents and caretakers (criteria 3.3): of those members, case heads, spouses and caretaker relatives in hca_household_composition_20261015.csv whose case had a child under 14 on 1 October 2026, from the children's birth dates and days in the case, each person counted once.
8. Named Pierce, Spokane, King and Thurston-Mason for the track.

## 4. Deliverable Answers

### ce_support_regions_2027.xlsx

1. Track regions, with each one's estimated share of expansion members aged 19 to 64 who worked 80 hours or more in March 2026, to the whole percent:
   - Pierce: 42 per cent
   - Spokane: 44 per cent
   - King: 46 per cent
   - Thurston-Mason: 47 per cent
2. Members covered on 1 October 2026, aged 19 to 64, by region:
   - Great Rivers: 4,286
   - Greater Columbia: 8,730
   - King: 21,346
   - North Central: 3,316
   - North Sound: 11,560
   - Pierce: 12,836
   - Salish: 4,120
   - Southwest: 7,866
   - Spokane: 9,922
   - Thurston-Mason: 4,615
3. Parents and caretaker relatives of a child under 14 on 1 October 2026, by region:
   - Great Rivers: 994
   - Greater Columbia: 1,989
   - King: 5,036
   - North Central: 773
   - North Sound: 2,632
   - Pierce: 2,835
   - Salish: 981
   - Southwest: 1,839
   - Spokane: 2,306
   - Thurston-Mason: 1,044

### ce_support_regions_2027.png

1. Bar chart of the ten regions' estimated shares, smallest at the top, Pierce, Spokane, King and Thurston-Mason highlighted above a line marking the four navigator teams, each region's whole percent beside its bar.
