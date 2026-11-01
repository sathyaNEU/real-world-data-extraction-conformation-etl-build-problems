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
4. Mass: the year's volume times the volume-weighted mean concentration of the year's compliance samples (24-hour composites; the inspection grabs, which carry suspended solids and pH only, are not compliance samples), each weighted by its day's metered volume, January on the measured COD.
5. Exceedance: each COD mass against the register's limit (kilograms read as such).
6. Tankered waste: accepted receival dockets of 2026 by local receival date, each docket's waste code from the manifest that carries it, a second pass of a load (the same truck within two hours, no manifest of its own) taking the code of the pass before it.

## 4. Deliverable Answers

### trade_waste_cod_review_2026.pdf

1. Customers that exceeded their 2026 COD limit: Coolabah Olives, Glenbrae Meats, Riverbend Poultry, Tallowood Tannery.
2. Customers within their limit: Mt Edwin Cheese, Sunvale Dairy, Hartley St Brewing, Bellbird Beverages, Kingfisher Linen, Golden Crumb, Paddock Fresh, Wattle Pet Foods.
3. Chart of each customer's 2026 COD mass as a share of its limit, the exceeders marked.

### trade_waste_figures_2026.xlsx

1. Tankered liquid waste received at the treatment plant by quarter of 2026, kL:
   - grease trap waste: Q1 5,765, Q2 5,791, Q3 6,128, Q4 6,098
   - septage: Q1 1,724, Q2 1,748, Q3 1,879, Q4 1,683
   - portable toilet waste: Q1 602, Q2 567, Q3 612, Q4 623
   - landfill leachate: Q1 2,198, Q2 1,926, Q3 1,984, Q4 2,414
2. Suspended solids discharged in 2026, t:
   - Coolabah Olives 16.3; Tallowood Tannery 66.2; Mt Edwin Cheese 35.1; Glenbrae Meats 189.8; Riverbend Poultry 94.1; Sunvale Dairy 45.3; Hartley St Brewing 18.3; Bellbird Beverages 8.6; Kingfisher Linen 13.6; Golden Crumb 9.1; Paddock Fresh 54.2; Wattle Pet Foods 43.4
