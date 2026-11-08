## Tags

**Domain:** Pharmacology, Pharmacoepidemiology & Safety (safety signal detection).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**We should refer Feverkind Junior Strength Acetaminophen Oral Suspension to the 2027 Child-Resistant Packaging Review: its packaging change had an effect of 1.3, the only one of the eight changes to reach 1.20.** The runner-up is Embercalm Nicotine Polacrilex Lozenge Mint at 1.1, a gap of 0.2. Not Dozinox Nighttime Sleep-Aid, which leads on exposures per pack sold only because it sold far fewer packs after its move to blisters while the bottles bought before stayed in homes; not Embercalm on its raw rise, which its tripled pack sales carried.

## 2. Critical Components

1. Feverkind Junior Strength's changed pack was first sold at retail on 16 September 2024, so its twelve months run October 2024 to September 2025, with **5,475** accidental exposures of children under six recorded.
2. Against the exposures its packs in use would have produced with the previous cap, its effect is **1.3**, the only effect of at least **1.20**.
3. Embercalm Nicotine Polacrilex Lozenge Mint recorded **13,038** from May 2025 to April 2026, an effect of **1.1**; the gap between the two effects is **0.2**.

## 3. Step-by-Step Solution

1. Took the eight packaging changes first sold at retail between 1 January 2024 and 30 September 2025 from the Packaging changes sheet of watched_products_register.xlsx, each with its date of first retail sale (procedure CRP-3, sections 2 and 3.3).
2. Counted the lines of case_export_watched_products.csv with reason Unintentional - general, patient_age_years under six and the product's product_code, by calendar month of call_received_local (sections 3.2 and 3.3): Feverkind Junior Strength has 5,475 in its twelve months.
3. Rebuilt each product's daily packs sold from halcyon_pos_4wk_revised.csv, taking halcyon_pos_4wk_preliminary.csv only for the period the revision lacks, spreading each four-week period's units evenly over its days and summing the product's UPCs and channels.
4. Modelled each product's monthly exposures as a constant rate times its packs in use, every day's purchases draining geometrically at the product's own pace, and fitted the rate and the pace by Poisson likelihood to the product's months from January 2019 to the month before its change month.
5. Back-tested the model on each product's last year before its change, fitted on the years before: it predicts every held-out year far better than a constant rate per pack sold, and Feverkind Junior Strength's better than a time series on sales and trend.
6. Ran each fitted model through the product's twelve months for the exposures expected with the previous packaging and divided the recorded count by it: Feverkind Junior Strength 1.3, Embercalm 1.1, the other six 1.0.
7. For the asks, read antidote_preparations_2024-07_2026-10.csv by hospital: an acetylcysteine course is a first bag with the later bags whose doses fit the three-bag or the two-bag regimen at the weight that first bag implies and at the regimen's hours, and a deferoxamine course for an iron poisoning is a chain of same-dose bags about eight hours apart, leaving out the bags of one dose prepared on consecutive evenings for transfusion admissions; courses are counted in the half-year their first bag was prepared.
8. Applied section 4: Feverkind Junior Strength has the largest effect and the only one of at least 1.20, so it is referred, with Embercalm the runner-up and a gap of 0.2.

## 4. Deliverable Answers

### packaging_referral.docx

1. Product referred: Feverkind Junior Strength Acetaminophen Oral Suspension (MP-40211)
2. Its effect: 1.3
3. Runner-up: Embercalm Nicotine Polacrilex Lozenge Mint (MP-40864), effect 1.1
4. Gap between their effects: 0.2

### referral_tables.xlsx

1. Every watched product whose packaging changed, its effect and whether it reaches 1.20:
   - Feverkind Junior Strength Acetaminophen Oral Suspension: 1.3, reaches 1.20
   - Embercalm Nicotine Polacrilex Lozenge Mint: 1.1, does not reach 1.20
   - Dozinox Nighttime Sleep-Aid Doxylamine Succinate Tablets: 1.0, does not reach 1.20
   - Vapocare Medicated Chest Rub: 1.0, does not reach 1.20
   - Coughex Children's Dextromethorphan Cough Syrup: 1.0, does not reach 1.20
   - Ibucalm Children's Ibuprofen Oral Suspension: 1.0, does not reach 1.20
   - Sunnybear Kids Multivitamin with Iron Gummies: 1.0, does not reach 1.20
   - Clearview Redness Relief Tetrahydrozoline Eye Drops: 1.0, does not reach 1.20
2. Courses started, each hospital and half-year (acetylcysteine; deferoxamine for an iron poisoning; the two together), whole numbers:
   - Tallgrass Children's Hospital, January to June 2025: 40; 2; 42
   - Tallgrass Children's Hospital, July to December 2025: 43; 3; 46
   - Tallgrass Children's Hospital, January to June 2026: 46; 3; 49
   - Lakeshore Children's Medical Center, January to June 2025: 51; 2; 53
   - Lakeshore Children's Medical Center, July to December 2025: 57; 1; 58
   - Lakeshore Children's Medical Center, January to June 2026: 46; 4; 50
   - Riverbend Children's Hospital, January to June 2025: 59; 3; 62
   - Riverbend Children's Hospital, July to December 2025: 77; 6; 83
   - Riverbend Children's Hospital, January to June 2026: 57; 2; 59
   - Ozark Children's Hospital, January to June 2025: 27; 2; 29
   - Ozark Children's Hospital, July to December 2025: 37; 3; 40
   - Ozark Children's Hospital, January to June 2026: 30; 2; 32

### effects_chart.png

1. One dot per changed product at its effect, labelled to one decimal, against a dashed referral line at 1.20; Feverkind Junior Strength is highlighted as the only product past the line.
