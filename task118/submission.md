## Tags

**Domain:** Pharmacology, pharmacoepidemiology and safety (benefit-risk assessment).
**Analytical objective:** Opportunity sizing and decision support.

## 1. Final Recommendation

**Place the hypnotic deprescribing team in Saltreach Coast, where it will avoid 19 emergency admissions for a fall in 2027; Hethermoss is the runner-up at 15, 4 fewer.**
The extra risk of a fall eases the longer a patient has been on a benzodiazepine or Z-drug, and Saltreach Coast's current users started most recently. Not Corvenham Central, which leads only if each start is taken from the patient's first item in the dispensing extract, which opens on 1 April 2026. Not Hethermoss, which leads only if every patient already on the drug when the extract opens is taken to have started over two years before.

## 2. Critical Components

1. Current users (hypnotics_deprescribing_policy_2026.pdf, section 4): **28,253**, **5,034** of them in Saltreach Coast.
2. Admissions for a fall avoided from 1 April to 31 December 2027: **19** in Saltreach Coast, **15** in Hethermoss, **13** or fewer in each other locality.

## 3. Step-by-Step Solution

1. Took the current users from dispensing_hypnotics_2026-04_2026-09.csv (born in 1961 or earlier, an item dispensed 1 July to 30 September 2026), each in the locality of their practice in practice_locality_register_2026.xlsx: 28,253.
2. Dated each user's first start by the first template of their chain in repeat_templates_hypnotics_2026-10-01.csv, walked back by replaces_template_id and, where a template carries a migration_source_ref (Mill Road Group Practice, moved 13 July 2026), on through Q89159_repeat_templates_previous_system_2026-07-12.csv by SupersededRef; a chain whose first template replaces one not in the export started before April 2024.
3. Summed each user's rate ratio less 1 over the days from 1 April to 31 December 2027 at the months since that start, over 365, times 4.0 per 100 and 45 per cent (hypnotics_deprescribing_policy_2026.pdf, sections 4 to 6).
4. Totalled by locality: Saltreach Coast 19, Hethermoss 15, the other four 13 or fewer.
5. Rebuilt the stays in sus_apc_falls_cohort_2025-26.csv (falls_indicator_definition_v2.pdf, F1): episodes into spells by provider_code and hospital_spell_no, and a spell whose patient was discharged to another hospital (destination 51) into the patient's spell at another site beginning that day or the next, however the receiving hospital coded it; counted the stays beginning with an emergency admission, W00 to W19 in their first episode, admitted in 2025-26, by age at admission and the practice's locality (Q80117 through the register's previous codes): Saltreach Coast 889 aged 65 to 79 and 1,327 aged 80 or over.
6. Bed-days (F2): each stay's last discharge less its first admission, summed: Saltreach Coast 22,140.
7. Readmissions (F3): the stays ended alive and followed by another stay beginning with an emergency admission on the day the stay ended or in the 30 days after: Saltreach Coast 347.
8. Recommended Saltreach Coast (19) over Hethermoss (15), 4 fewer.

## 4. Deliverable Answers

### deprescribing_case_2027.docx

1. The locality: Saltreach Coast.
2. Emergency admissions for a fall it avoids in 2027: 19.
3. The runner-up: Hethermoss.
4. How many fewer it would avoid: 4.

### deprescribing_placement_2027.xlsx

1. Emergency admissions for a fall in 2025-26, aged 65 to 79:
   - Corvenham Central: 969
   - Fenmarsh: 720
   - Saltreach Coast: 889
   - Quenford Rise: 653
   - Hethermoss: 574
   - Ledbridge North: 417
2. Emergency admissions for a fall in 2025-26, aged 80 or over:
   - Corvenham Central: 1,282
   - Fenmarsh: 1,082
   - Saltreach Coast: 1,327
   - Quenford Rise: 974
   - Hethermoss: 846
   - Ledbridge North: 643
3. Bed-days those admissions used:
   - Corvenham Central: 21,717
   - Fenmarsh: 19,041
   - Saltreach Coast: 22,140
   - Quenford Rise: 15,978
   - Hethermoss: 13,967
   - Ledbridge North: 11,004
4. Those admissions followed by another emergency admission within 30 days of leaving hospital:
   - Corvenham Central: 358
   - Fenmarsh: 270
   - Saltreach Coast: 347
   - Quenford Rise: 281
   - Hethermoss: 226
   - Ledbridge North: 186
