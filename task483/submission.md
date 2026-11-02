## Tags

**Domain:** Pharmacology, Pharmacoepidemiology & Safety (benefit-risk assessment: the coverage side of empiric antibiotic choice for lower urinary tract infection, sized network by network for a GP federation's stewardship pathway).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**Place the two UTI pathway pharmacists in Morrow Cross and Tamsey from 1 April 2027. Moving their 2026 first courses on other antibacterials to nitrofurantoin would have stopped about 70 and 70 mismatched first courses; Kesterby is the runner-up at about 50.**
Read on the urine cultures sent at a first course's own consultation, nitrofurantoin meets a resistant organism in about 5 per cent of first courses, pivmecillinam in 13 and fosfomycin in 10, so the networks whose other courses are mostly pivmecillinam and fosfomycin stop the most. Not Kesterby and Ashwell Vale: priced at the laboratory's cumulative urine antibiogram, which is drawn mostly from cultures sent after a course failed, nitrofurantoin reads far higher and their trimethoprim courses look like the only gain.

## 2. Critical Components

1. Morrow Cross and Tamsey: **70** and **70** mismatched courses stopped (nearest 10); runner-up Kesterby **50**.
2. 2026 first courses on other antibacterials: Morrow Cross **1123**, Tamsey **1098**, Kesterby **543**.

## 3. Step-by-Step Solution

1. Took first courses as specification 2.1 defines them from gp_uti_antibacterial_issues_2024-2026.csv: acute issues of a pathway antibacterial (uti_pathway_code_lists_2027-28.xlsx, sheet Pathway antibacterials) linked to a lower UTI problem (sheet Lower UTI problems), to women aged 16 to 64 at issue, with no such issue to the same pseudonym in the 28 days before; hub issues to the registered practice and Stanbridge Road to Hollin Lane (member_practice_register_2026.xlsx).
2. Counted each network's 2026 first courses by antibacterial (16068 in all).
3. Joined urine_culture_results_2024-2026.csv to the first courses by pseudonym and kept, for each first course of 2024 to 2026, the culture collected on the day of its issue (the day before to the day after gives the same 4658 cultures); most of the laboratory's other cultures from these women follow a failed course and are left out.
4. Each antibacterial's chance is the share of those cultures with any organism reported R to it (MECI, NITR, TRIM and the other columns; I and S are not resistant, no significant growth and mixed growth count as no resistant organism).
5. Each network's mismatched courses stopped is the sum over its 2026 first courses on other antibacterials of the antibacterial's chance less nitrofurantoin's; the two largest get the pharmacists (specification 4.1, 4.2).
6. For the wider advice: patients (women aged 65 and over, men aged 16 and over) with a 2026 culture from a member practice or the hub, network by registered practice, counted once per organism. The laboratory changed system on 7 September 2026 (H-prefixed accession numbers before it): the old system's ENTE is the enterococcus and its ENTC the Enterobacter cloacae complex, which the new system codes ECLO while giving ENTC to the enterococci; the old ENTC isolates are all amoxicillin and co-amoxiclav resistant, as an Enterobacter is and an enterococcus is not, and no ECLO appears before the change.

## 4. Deliverable Answers

### uti_pathway_placement_2027-28.xlsx

1. Pharmacists to Morrow Cross and Tamsey; runner-up Kesterby.
2. Each network's 2026 first courses on antibacterials other than nitrofurantoin, and mismatched courses stopped (nearest 10):
   - Morrow Cross: 1123, 70
   - Tamsey: 1098, 70
   - Kesterby: 543, 50
   - Upper Lode: 610, 40
   - Ashwell Vale: 521, 40
   - Stanbridge North: 1192, 30
   - Brackenholt: 420, 20
3. Bar chart of mismatched courses stopped by network, Morrow Cross and Tamsey marked.
4. Women aged 65 and over and men aged 16 and over with a 2026 urine culture from a practice or the hub that grew an enterococcus, and that grew Enterobacter cloacae (patients):
   - Kesterby: 129, 53
   - Ashwell Vale: 84, 32
   - Morrow Cross: 143, 48
   - Tamsey: 122, 43
   - Stanbridge North: 133, 33
   - Upper Lode: 92, 42
   - Brackenholt: 110, 31

### uti_pathway_placement_note_2027-28.docx

1. One pharmacist to Morrow Cross and one to Tamsey from 1 April 2027, about 70 and 70 mismatched first courses stopped on the 2026 basis against 50 for Kesterby.
