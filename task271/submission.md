## Tags

**Domain:** Biomedical & Clinical Research (statistical genomics).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**The Family Outreach Program should take on the PALB2 protein-truncating and PALB2 missense groups, and none of the other eight.**

Measured on every mother, sister and daughter of the probands, each a carrier with probability one half unless a final report settles it, the two PALB2 groups' risks of breast cancer by 70 are 38 to 43 and 46 to 53 percent across the kin-cohort and the Mendelian likelihood, and no other group's is above 25 percent. Not ATM missense, BARD1 or RAD51D, which Kaplan-Meier on the relatives whose report shows the variant puts at 46, 41 and 34 percent: those groups were identified late (the ATM missense variants reclassified in May 2024, BARD1 and RAD51D added to the panel in July 2023), their tested relatives are mostly women tested for a breast cancer of their own, and counting every relative they stand at 18 to 20, 16 to 18 and 12 to 16 percent. Not CHEK2 protein-truncating, which twice the relatives' share puts at 31 percent before the half who do not carry the variant are given the population's 7.5 percent; it stands at 24 to 25 percent.

## 2. Critical Components

1. Every group is measured on all **9,179** mothers, sisters and daughters of its probands (**2,970** families), **3,170** of them with a test result.
2. Among the living relatives of the four groups identified late, **43 to 80 percent** of those with breast cancer were tested against **13 to 17 percent** of those without.
3. Counting every relative, ATM missense, BARD1 and RAD51D stand at **18 to 20**, **16 to 18** and **12 to 16 percent** and the two PALB2 groups at **38 to 43** and **46 to 53 percent**.

## 3. Step-by-Step Solution

1. Took each family's group and its probands' mothers, sisters and daughters from icrs_pedigree_export_20260930.csv (the probands and half-sisters left out, criteria 2.3): 9,179 women, each with her age at a first breast cancer or her age at the history date or at death.
2. Took each woman's final report from icrs_laboratory_reports_2016_2026.csv (an Amended or Reanalysis report replacing the one it supersedes): 3,170 tested, 1,641 showing the family's variant.
3. Took the population's risk of a first breast cancer by 70 from the rates under 70 in ellisford_tumor_registry_breast_incidence_2016_2025.csv: 7.5 percent.
4. For each group ran Kaplan-Meier on all its mothers, sisters and daughters to the 70th birthday (death and the history date censor) and took the carriers' risk as twice that share less 7.5 percent, each relative a carrier with probability one half: PALB2-PTV 42, PALB2-MIS 49, every other group 24 or less.
5. Checked with a Mendelian likelihood over the same women (the tested women's genotypes, the one-half prior for the rest, the population's hazard for noncarriers or both hazards estimated): the same two groups clear 30 percent and no other group comes within 5 points of it.
6. Known carriers for the clinic (criteria 3.1): women whose final report shows the variant as pathogenic or likely pathogenic, with an enterprise ID, living and not in ellisford_death_linkage_20260930.csv, aged 30 to 74 on 1 April 2027, less those with both breasts removed on the first-course surgery in ellisford_tumor_registry_breast_abstracts.csv (codes 42 and 56, or 41 and 51 by side) and ellisford_surgical_procedures_2019_2026.csv (19303 and 19307 by modifier) together.
7. No screening MRI (criteria 3.2): of those women, the ones with no COMPLETED SCREENING - HIGH RISK study dated 1 October 2025 to 30 September 2026 in ellisford_breast_mri_exams_2024_2026.csv, each study matched to its woman by hospital and record number through ellisford_empi_identifiers.csv.
8. Named PALB2-PTV and PALB2-MIS for the program.

## 4. Deliverable Answers

### family_outreach_groups_2027.xlsx

1. Whether the program takes each group on:
   - PALB2-PTV (PALB2 protein-truncating): taken on
   - PALB2-MIS (PALB2 missense): taken on
   - ATM-PTV (ATM protein-truncating): not taken on
   - ATM-MIS (ATM missense): not taken on
   - CHEK2-PTV (CHEK2 protein-truncating): not taken on
   - CHEK2-MIS (CHEK2 missense): not taken on
   - BARD1-PTV (BARD1 protein-truncating): not taken on
   - RAD51C-PTV (RAD51C protein-truncating): not taken on
   - RAD51D-PTV (RAD51D protein-truncating): not taken on
   - BRIP1-PTV (BRIP1 protein-truncating): not taken on
2. Women already known to carry a variant in the group whom the program would offer the clinic on 1 April 2027:
   - PALB2-PTV: 380
   - PALB2-MIS: 62
   - ATM-PTV: 335
   - ATM-MIS: 60
   - CHEK2-PTV: 516
   - CHEK2-MIS: 384
   - BARD1-PTV: 72
   - RAD51C-PTV: 129
   - RAD51D-PTV: 64
   - BRIP1-PTV: 151
3. Of those women, how many had no screening breast MRI at Ellisford from 1 October 2025 to 30 September 2026:
   - PALB2-PTV: 192
   - PALB2-MIS: 28
   - ATM-PTV: 211
   - ATM-MIS: 35
   - CHEK2-PTV: 336
   - CHEK2-MIS: 242
   - BARD1-PTV: 49
   - RAD51C-PTV: 95
   - RAD51D-PTV: 39
   - BRIP1-PTV: 118

### family_outreach_groups_2027.png

1. Bar chart of the ten groups' estimated risk of breast cancer by age 70 for a woman who carries the variant, with a dashed line at 30 percent and the two PALB2 groups, the only bars past it, highlighted.
