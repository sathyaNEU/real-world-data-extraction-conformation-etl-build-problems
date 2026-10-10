# solver round: round 1, plain

**Proxy score 88.8 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 46.8 of 58). Main call LANDED. 5 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: The 2027 order should designate six sections: 0301401008, 0301402014, 4625001005, 4625002007, 4625011004 and 4625012009.

solver: The 2027 order should designate six of the fourteen watch-list sections: 0301401008 (Alacant d1, 28.0%), 0301402014 (Alacant d2, 25.7%), 4625001005 (Ciutat Vella, 31.4%), 4625002007 (l'Eixample, 29.3%), 4625011004 (Poblats Marítims, 33.3%) and 4625012009 (Camins al Grau, 26.2%). The designated section closest to the 25% line is 0301402014, at 25.7% and 0.7 pp above it. The undesignated section closest to it is 4625001012 (Ciutat Vella 012), at 24.2% and 0.8 pp below.

tokens matched 1 of 1 (4625011004)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| designation_brief_2027.pdf | 1 | 3 | 3 | 100% |
| designation_brief_2027.pdf | 2 | 1 | 2 | 50% |
| designation_brief_2027.pdf | 3 | 3 | 3 | 100% |
| designation_brief_2027.pdf | 4 | 3 | 3 | 100% |
| designation_annex_2027.csv | 1 | 51 | 51 | 100% |
| section_bridge_2027.png | 1 | 6 | 13 | 46% |
| section_bridge_2027.png | 2 | 7 | 14 | 50% |
| section_bridge_2027.png | 3 | 2 | 2 | 100% |

## Solver's path

1. Rebuilt the large-holder position at 30 June 2026 from declaracions_grans_tenidors. For each declarant I took the latest quarter with an O filing up to 2026T2; an S replaces its O and a C adds to it. Declarants that did not file 2026T2 keep their last declaration; there are 16, and none has deeds or pending sales against it. I normalised references (case, spaces and hyphens; 14-character parcels expanded through the unit ranges; 18-character parcel+càrrec codes matched to the cadastre) and kept PD lines only. The result matches the T2 bulletin in all 14 sections (for example 0301402014 = 165 and 4625001012 = 205). Dwelling counts come from the cadastre's residential units.
2. Checked the pending sales declared with dates in July–September against escriptures_inscrites. All were deeded on the stated date to the stated buyer, so I applied the actual deeds granted from July to September 2026 in date order. A buyer counts as a large holder only if it is on the register's Titulars sheet with no baixa.
3. In EPPR_execucio_pressupost (PPO programme), every pre-emption commitment (phase D) up to September was deeded to Q4600731F exactly 120 days after its commitment date (23 of 23 cases). I matched the PPO references to the declared pending sales from October onward. A pre-empted sale does not go to the declared buyer: the dwelling passes to EPPR on commitment date + 120 days, which for some sales is before and for others after 1 January 2027. Sales without pre-emption were applied on their declared date and to their declared buyer.
4. Three sections turn on this. 4625001012: 20 dwellings declared for sale to another large holder in February 2027 are pre-empted and deeded on 2026-11-06, giving 183/757 = 24.2%. 4625011016: 17 large-holder-to-large-holder sales are pre-empted and deeded on 2026-12-03, giving 150/641 = 23.4%. 0301402014: December sales to individuals are pre-empted with deeds falling in January 2027, so the dwellings stay with the large holder, giving 155/603 = 25.7%.
5. Applied the 25%-or-more rule at 1 January 2027 (Article 4). Six sections are designated. The closest designated section is 0301402014 at +0.705 pp; the closest undesignated one is 4625001012 at -0.826 pp.
6. Assigned each holder to its group from the register's Vinculacions sheet effective at 1 January 2027, not from the codi_grup in the declarations. This gives Habitatges Pilastra → Barana from 2026-10-01; Inversions Llucana → Finestral from 2026-11-16; Trespol Castelló leaves Porxo on 2026-12-13; Gestió Ribot leaves Cantonera; Pati Interior joins Ràfec only in March 2027. Group names come from codis_grup and holders outside any group use their register name.
7. Dwellings with nobody registered: I used the September 2026 padró and, for the districts it does not contain (Alacant 02, València 11 and 12), the June delivery. TIE-T and PAS registrations more than two years past their registration or last renewal date count as expired. For Castelló, delivered one row per dwelling, persones = 0 means empty. The counts come out the same whether expiry is measured at the delivery date or at 1 January 2027.
8. Bridge: month-end large-holder counts for each section from July to December 2026, starting from the bulletin's 30 June figure. The line is 25% of the section's dwellings, in dwellings.

confidence: Medium-high. The 30 June base reconciles exactly with the T2 bulletin, and the 120-day pre-emption lag is constant across all 23 past cases. The main risk is whether a pre-emption deed can fall before the original contract's planned date. That is what drops 4625001012 below the line.

notes: The files do not say whether a pre-emption commitment could still be dropped. I treated phase D commitments as firm, since every past one was deeded. Acquisitions by large holders from October to December are not declared anywhere (OP/RS lines have no dates), so I added none.

### designation_brief_2027.pdf (solver's answers)
- designated list and count: 6 sections designated: 0301401008, 0301402014, 4625001005, 4625002007, 4625011004, 4625012009
- designated section closest to line: 0301402014 (Alacant, districte 2, secció 014): large-holder share 25.7%; distance from line 0.7 percentage points above
- undesignated section closest to line: 4625001012 (València, Ciutat Vella, secció 012): large-holder share 24.2%; distance from line 0.8 percentage points below

### designation_annex_2027.csv (solver's answers)
- 0301401008: large-holder dwellings 157 of 561; share 28.0%; largest group Grup Cantonera, 43 dwellings; large-holder dwellings with nobody on the padró 8
- 0301402014: large-holder dwellings 155 of 603; share 25.7%; largest group Grup Barana, 38 dwellings; nobody on the padró 9
- 0301405003: large-holder dwellings 109 of 612; share 17.8%; largest group Grup Cantonera, 28 dwellings; nobody on the padró 5
- 1204001006: large-holder dwellings 154 of 688; share 22.4%; largest group Grup Porxo, 40 dwellings; nobody on the padró 9
- 1204003011: large-holder dwellings 92 of 516; share 17.8%; largest group Grup Arcada, 25 dwellings; nobody on the padró 6
- 4625001005: large-holder dwellings 255 of 812; share 31.4%; largest group Grup Barana, 89 dwellings; nobody on the padró 14
- 4625001012: large-holder dwellings 183 of 757; share 24.2%; largest group Grup Xamfrà, 75 dwellings; nobody on the padró 11
- 4625002007: large-holder dwellings 202 of 689; share 29.3%; largest group Grup Finestral, 73 dwellings; nobody on the padró 9
- 4625002019: large-holder dwellings 163 of 722; share 22.6%; largest group Grup Finestral, 50 dwellings; nobody on the padró 12
- 4625005013: large-holder dwellings 183 of 879; share 20.8%; largest group Grup Escaire, 47 dwellings; nobody on the padró 10
- 4625011004: large-holder dwellings 310 of 931; share 33.3%; largest group Grup Barana, 108 dwellings; nobody on the padró 17
- 4625011016: large-holder dwellings 150 of 641; share 23.4%; largest group Grup Mitgera, 48 dwellings; nobody on the padró 7
- 4625012009: large-holder dwellings 141 of 538; share 26.2%; largest group Grup Ràfec, 54 dwellings; nobody on the padró 13
- 4625013021: large-holder dwellings 149 of 748; share 19.9%; largest group Grup Andana, 48 dwellings; nobody on the padró 6

### section_bridge_2027.png (solver's answers)
- 0301402014 walk: 30 June bulletin 165 dwellings; Jul -2, Aug -2, Sep -2, Oct 0, Nov 0, Dec -4; annex 155; designation line 150.75 dwellings (25% of 603)
- 4625001012 walk: 30 June bulletin 205 dwellings; Jul -1, Aug 0, Sep 0, Oct -1, Nov -20, Dec 0; annex 183; designation line 189.25 dwellings (25% of 757)
- title count: 6 designated sections
