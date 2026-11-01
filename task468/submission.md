## Tags

**Domain:** Physical & Environmental Sciences (emissions inventory: a water utility's releases to sewer, trade waste chemical oxygen demand on the agreements' reference method).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Coolabah Olives, Glenbrae Meats, Riverbend Poultry and Tallowood Tannery exceeded their agreements' 2026 COD limits and go on the annual return with a notice of agreement review; no other customer did.**
The dichromate COD the agreements limit also reads chloride, which TOC does not, so each 2026 TOC sample is converted on its own chloride; Mt Edwin Cheese's chloride fell after its brine recovery started in May and Tallowood Tannery's rose from March, so the ratios their 2025 parallel samples carried misstate both.

## 2. Critical Components

1. The COD equivalent of a TOC sample carries the sample's chloride: fitted on the parallel samples, COD rises **about 0.23 mg/L per mg/L of chloride** beside about 2.8 per mg/L of TOC.
2. Customers over their limits: **Coolabah Olives, Glenbrae Meats, Riverbend Poultry, Tallowood Tannery**.
3. Within their limits: Mt Edwin Cheese, Sunvale Dairy, Hartley St Brewing, Bellbird Beverages, Kingfisher Linen, Golden Crumb, Paddock Fresh, Wattle Pet Foods.

## 3. Step-by-Step Solution

1. Laboratory: the legacy LIMS (local times, site codes through the crosswalk) and LabWare (UTC to Queensland time, point identifiers), duplicates (-D) dropped, re-issued results (-R) replacing the originals, suspended solids below 5 mg/L at 2.5.
2. Conversion: COD regressed on TOC and chloride over the samples tested both ways in October to December 2025, with a constant, applied to each 2026 TOC sample with its own chloride.
3. Volume: each meter's hourly register read in Queensland time over the local year; across an exchange the removed meter to its final read and the installed meter from its opening read, both from the field job log.
4. Mass: the year's volume times the volume-weighted mean concentration of the year's compliance samples, each weighted by its day's metered volume, January on the measured COD.
5. Exceedance: each COD mass against the register's limit (kilograms read as such).

## 4. Deliverable Answers

### trade_waste_cod_review_2026.pdf

1. Customers that exceeded their 2026 COD limit: Coolabah Olives, Glenbrae Meats, Riverbend Poultry, Tallowood Tannery.
2. Customers within their limit: Mt Edwin Cheese, Sunvale Dairy, Hartley St Brewing, Bellbird Beverages, Kingfisher Linen, Golden Crumb, Paddock Fresh, Wattle Pet Foods.
3. Chart of each customer's 2026 COD mass as a share of its limit, the exceeders marked.

### trade_waste_figures_2026.xlsx

1. Volume discharged by quarter of 2026, kL:
   - Coolabah Olives: Q1 11,031, Q2 11,710, Q3 11,051, Q4 10,376
   - Tallowood Tannery: Q1 13,956, Q2 14,994, Q3 13,989, Q4 13,239
   - Mt Edwin Cheese: Q1 16,370, Q2 17,493, Q3 16,707, Q4 15,164
   - Glenbrae Meats: Q1 32,757, Q2 35,337, Q3 32,299, Q4 30,830
   - Riverbend Poultry: Q1 28,001, Q2 30,254, Q3 28,305, Q4 26,975
   - Sunvale Dairy: Q1 41,552, Q2 44,518, Q3 41,782, Q4 39,247
   - Hartley St Brewing: Q1 7,558, Q2 8,143, Q3 7,765, Q4 7,087
   - Bellbird Beverages: Q1 18,761, Q2 20,081, Q3 19,139, Q4 18,088
   - Kingfisher Linen: Q1 26,350, Q2 28,195, Q3 26,221, Q4 24,479
   - Golden Crumb: Q1 6,786, Q2 7,222, Q3 6,850, Q4 6,292
   - Paddock Fresh: Q1 22,969, Q2 24,556, Q3 23,187, Q4 21,438
   - Wattle Pet Foods: Q1 11,840, Q2 12,657, Q3 12,020, Q4 11,192
2. Suspended solids discharged in 2026, t:
   - Coolabah Olives 16.3; Tallowood Tannery 66.2; Mt Edwin Cheese 35.1; Glenbrae Meats 189.8; Riverbend Poultry 94.1; Sunvale Dairy 45.3; Hartley St Brewing 18.3; Bellbird Beverages 8.6; Kingfisher Linen 13.6; Golden Crumb 9.1; Paddock Fresh 54.2; Wattle Pet Foods 43.4
