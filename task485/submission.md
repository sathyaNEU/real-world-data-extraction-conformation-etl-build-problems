## Tags

**Domain:** Physical & Environmental Sciences, emissions inventory (an environment ministry's 2026 sulphur dioxide inventory of eighteen permitted coal boilers with wet limestone scrubbers, conformed from four coal suppliers' delivery analyses, the operators' quarterly returns, two quarries' tickets and weekly certificates, the scrubber guarantee schedules and two laboratories' test reports).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**The 2027 Sulphur Dioxide Order lists six boilers, Quarholt Board Mills boiler 2, Dremstead Chemicals, Candrigg Soda Works, Thalwold Foods, Sellhope Rubber and Umbgarth District Heating, whose sulphur dioxide leaving the stack over 2026 was 390, 340, 320, 330, 350 and 340 tonnes against the 250 tonne line; the other twelve boilers are under it.**
Candrigg Soda Works is the nearest to the line among the six at 320 tonnes, and Quarholt Board Mills boiler 1 the highest of the rest at 160. Not Candrigg Soda Works alone, which the removals the scrubbers showed at their 2026 performance tests give when carried across the year: the scrubbers at Quarholt Board Mills boiler 2, Dremstead Chemicals, Thalwold Foods, Sellhope Rubber and Umbgarth District Heating consumed too little limestone for those removals, so their sulphur dioxide runs 3.3 to 5.9 times their tested figures. Not Quarholt Board Mills boiler 1, which its design removal puts at 310 tonnes: over the year its scrubber removed more than its design.

## 2. Critical Components

1. Sulphur dioxide formed from the coal the eighteen boilers fired in 2026, less the ash's share, to the nearest 100: **25,400 tonnes**.
2. Sulphur dioxide the eighteen scrubbers removed over 2026, from the calcium carbonate they consumed, to the nearest 100: **22,400 tonnes**.

## 3. Step-by-Step Solution

1. Took each boiler's coal burned from the four quarters of boiler_returns_2026.xlsx, quarters 1 and 2 on the 2019 template and 3 and 4 on the 2026 template: 893,723 tonnes in all.
2. Took each site's sulphur as received from coal_deliveries_2026.csv, the deliveries received from 1 January to 31 December 2026 weighted by net tonnes (guidance section 4.2), each customer code put to its site through coal_supplier_customers.csv.
3. Took off each boiler's sulphur retained in ash from permitted_boilers_register_2026.xlsx and converted at 64.066 over 32.065: 25,400 tonnes of sulphur dioxide formed.
4. Took each scrubber's limestone consumed as its 2026 tickets in limestone_tickets_2026.csv, put to permits by the Delivery points sheet of limestone_certificates_2026.xlsx, less its silo's change from the first quarter's opening to the fourth quarter's closing stock in the returns, each ticket at its ISO week's calcium carbonate in the same workbook.
5. Converted each scrubber's calcium carbonate to sulphur dioxide removed at its operating stoichiometry in scrubber_guarantee_schedules.pdf, 1.03 to 1.07 moles of calcium carbonate per mole removed: 22,400 tonnes.
6. Subtracted each boiler's removal from its sulphur dioxide formed and tested the remainder unrounded against 250 tonnes (the Order's note, section 2): six boilers at or over the line.
7. For the ash, conformed whinmoss_invoice_lines_2026.xlsx, carnhope_jobs_2026.csv and pellrigg_dockets_2026.xlsx to the sites through ash_contractor_customers.csv, kept bottom and fly ash collected in 2026, read Carnhope's net weights in kilograms, and dropped every Whinmoss line whose reference is a Carnhope or Pellrigg job number, because that line bills the local contractor's own collection, counted on its record: each site's tonnes and recovery share below.
8. The Order lists Quarholt Board Mills boiler 2, Dremstead Chemicals, Candrigg Soda Works, Thalwold Foods, Sellhope Rubber and Umbgarth District Heating.

## 4. Deliverable Answers

### sulphur_dioxide_order_schedule_2027.xlsx

1. Each boiler's sulphur dioxide leaving the stack in 2026, tonnes to the nearest 10, and whether the Order lists it, in the register's order:
   - Quarholt Board Mills boiler 1: 160 tonnes, not listed
   - Quarholt Board Mills boiler 2: 390 tonnes, listed
   - Eskfold Sugar: 70 tonnes, not listed
   - Dremstead Chemicals: 340 tonnes, listed
   - Ulvdale Dyeworks: 90 tonnes, not listed
   - Kirlgate Maltings: 20 tonnes, not listed
   - Vornfield Brewery: 50 tonnes, not listed
   - Yeldholt General Hospital Energy Centre: 70 tonnes, not listed
   - Haskmouth Paper: 40 tonnes, not listed
   - Nethstead Tissue No. 1 boiler: 70 tonnes, not listed
   - Nethstead Tissue No. 2 boiler: 60 tonnes, not listed
   - Pridwold Starch: 120 tonnes, not listed
   - Lathgarth Fibres: 40 tonnes, not listed
   - Candrigg Soda Works: 320 tonnes, listed
   - Thalwold Foods: 330 tonnes, listed
   - Sellhope Rubber: 350 tonnes, listed
   - Umbgarth District Heating: 340 tonnes, listed
   - Wendscar Tannery: 120 tonnes, not listed
2. Each site's boiler ash taken off site in 2026 by the three contractors, tonnes to the nearest 10, and the share sent to recovery at Yarrdale Blocks or Velthwaite Cement Works, per cent to one decimal:
   - Quarholt Board Mills: 23,610 tonnes, 87.4 per cent
   - Eskfold Sugar: 6,200 tonnes, 82.2 per cent
   - Dremstead Chemicals: 8,490 tonnes, 72.9 per cent
   - Ulvdale Dyeworks: 4,120 tonnes, 13.9 per cent
   - Kirlgate Maltings: 2,280 tonnes, 68.8 per cent
   - Vornfield Brewery: 5,870 tonnes, 85.3 per cent
   - Yeldholt General Hospital Energy Centre: 7,320 tonnes, 75.0 per cent
   - Haskmouth Paper: 3,410 tonnes, 71.4 per cent
   - Nethstead Tissue: 11,060 tonnes, 88.5 per cent
   - Pridwold Starch: 9,890 tonnes, 20.9 per cent
   - Lathgarth Fibres: 4,000 tonnes, 71.3 per cent
   - Candrigg Soda Works: 16,560 tonnes, 87.2 per cent
   - Thalwold Foods: 7,000 tonnes, 74.3 per cent
   - Sellhope Rubber: 4,860 tonnes, 15.8 per cent
   - Umbgarth District Heating: 6,760 tonnes, 68.8 per cent
   - Wendscar Tannery: 8,320 tonnes, 17.2 per cent

### boiler_sulphur_dioxide_2026.png

1. A horizontal bar chart of the eighteen boilers' 2026 sulphur dioxide leaving the stack, highest at the top, against a line at 250 tonnes, the six listed boilers in red-brown and every bar labelled with its tonnes to the nearest 10.
