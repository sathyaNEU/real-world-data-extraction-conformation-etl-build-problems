# task130 · Observatori del Parc Residencial, the 2027 large-holder designation of census sections

## Tags

**Domain:** Demographic & Social Science (housing: large-holder ownership of dwellings by census section, decided by a regional housing observatory).
**Analytical objective:** Data Extraction & Conformation (ETL) (versioned quarterly dwelling returns, a parcel-to-dwelling format change, option and reservation lines, malformed cadastral references, a deed extract and a public agency's budget commitments conformed into one holdings table per section on 1 January 2027).

## 1. Final Recommendation

**The 2027 order should designate seven sections: 0301401008, 0301402014, 4625001005, 4625002007, 4625011004, 4625011016 and 4625012009.**

The line is decided by 0301402014 at 25.7% (0.7 points over) and 4625001012 at 24.2% (0.8 points under). Not the roll from the returns alone, even with the agency's takeovers on its 120-day clock, which leaves out the dwellings of holders inscribed after 30 June that have lodged no return yet and so drops 4625011016. Not last year's method, which carries every notified sale to its agreed buyer and date and so keeps 4625001012 and drops 0301402014. Not the 30 June bulletin's list, because Article 4 of the order counts holdings on 1 January.

## 2. Critical Components

1. Every first-offer purchase the agency has completed was executed **120 days** after its commitment
2. Habitatges Cornisa SL, inscribed in the register after 30 June 2026 with no return yet, holds **18** dwellings in 4625011016
3. 4625011016 holds **168** large-holder dwellings on 1 January 2027, **26.2%**
4. 4625001012 holds **183**, **24.2%**
5. 0301402014 holds **155**, **25.7%**

## 3. Step-by-Step Solution

1. Conformed each holder's latest return for a quarter up to 2026T2 in `declaracions_grans_tenidors_2024T3_2026T2.csv` per `guia_presentacio_declaracio_trimestral_2024-01.pdf` (an S return replaces the return it refers to, a C return adds its lines, a holder with no 2026T2 return stands on its latest earlier quarter), kept PD lines only, expanded parcel lines (the pre-April 2026 format, `avis_portal_canvi_format_2026-03.eml`) to one dwelling per `unitats` charge in `cadastre_habitatges_extracte_20260928.csv`, and resolved each unmatched reference, separators removed and upper-cased, to the one cadastre reference with the same first 18 characters: the 30 June counts tie to `butlleti_parc_residencial_2026T2.pdf` in all 14 sections.
2. Rolled every dwelling to 1 January 2027 per Article 2.4 of `ordre_designacio_seccions_grans_tenidors.pdf`: deeds in `escriptures_inscrites_2024-07_2026-09.csv` executed after 30 June and registered by 30 September applied in execution order, then notified sales not yet executed passed on `data_transmissio_prevista` if on or before 1 January 2027; a buyer listed in the register's Titulars sheet without `data_baixa` becomes the holder, any other buyer takes the dwelling out of the count.
3. Read the agency's commitments from `EPPR_execucio_pressupost_2026_gen-set.csv` (programme PPO, phase D, concept naming a tempteig, reference after "RC"), whose 27 purchases already in the deed extract were each executed 120 days after the D line and none on the notified date, and moved each committed sale to the agency 120 days after commitment instead of to its agreed buyer and date (the agency is not a large holder, Article 2.1), stopping the same roll at each month end for the bridges: 4625001012 falls to 183 and 0301402014 keeps the December sales completing 13 to 22 January, at 155.
4. Added the holders on the `Titulars` sheet of `registre_grans_tenidors_20261001.xlsx` with no return in the returns file (four, inscribed July to September 2026), each holding the dwellings whose latest deed in the extract names it as buyer (Articles 2.1 and 2.4): Habitatges Cornisa SL holds 18 in 4625011016, which reaches 168, and Pòrtic Residencial SL holds 5 in 4625001005 and 6 in 4625013021.
5. Divided each section's count by its `Residencial` units in the cadastre extract and applied Article 4's 25 per cent: seven sections designated; the distance to the line is taken from the unrounded share.
6. Largest group: each holder mapped to the group code of its `Vinculacions` link in `registre_grans_tenidors_20261001.xlsx` in force on 1 January 2027 (start on or before, end blank or on or after), named through `codis_grup.csv`, a holder in no group counted alone.
7. Dwellings with nobody registered: the latest delivery per district in `padro_lliurament_2026-09.csv`, else `padro_lliurament_2026-06.csv` (València districts 11 and 12, Alacant district 2), occupied when a per-dwelling row has `persones` above 0 or a per-person row is live, a TIE-T or PAS registration lapsing two years after the later of `data_alta` and `data_ultima_renovacio` against the delivery's reference day, the 1st of its month (`nota_intercanvi_padro_rev2.txt`).
8. Recommendation: designate 0301401008, 0301402014, 4625001005, 4625002007, 4625011004, 4625011016 and 4625012009.

## 4. Deliverable Answers

### designation_brief_2027.pdf
1. Designated sections: 0301401008, 0301402014, 4625001005, 4625002007, 4625011004, 4625011016 and 4625012009
2. Number of designated sections: 7
3. Designated section closest to the line: 0301402014, 25.7%, 0.7 percentage points above the line
4. Undesignated section closest to the line: 4625001012, 24.2%, 0.8 percentage points below the line

### designation_annex_2027.csv
1. One row per watch-list section (large-holder dwellings, share, largest group, its dwellings, large-holder dwellings with nobody registered):
   - 0301401008: 157, 28.0%, Grup Cantonera, 43, 8
   - 0301402014: 155, 25.7%, Grup Barana, 38, 9
   - 0301405003: 109, 17.8%, Grup Cantonera, 28, 5
   - 1204001006: 154, 22.4%, Grup Porxo, 40, 9
   - 1204003011: 92, 17.8%, Grup Arcada, 25, 6
   - 4625001005: 260, 32.0%, Grup Barana, 89, 14
   - 4625001012: 183, 24.2%, Grup Xamfrà, 75, 11
   - 4625002007: 202, 29.3%, Grup Finestral, 73, 9
   - 4625002019: 163, 22.6%, Grup Finestral, 50, 12
   - 4625005013: 183, 20.8%, Grup Escaire, 47, 10
   - 4625011004: 310, 33.3%, Grup Barana, 108, 17
   - 4625011016: 168, 26.2%, Grup Mitgera, 48, 7
   - 4625012009: 141, 26.2%, Grup Ràfec, 54, 13
   - 4625013021: 155, 20.7%, Grup Andana, 48, 6

### section_bridge_2027.png
1. 4625001012: 205 on 30 June; July -1, August 0, September 0, October -1, November -20, December 0; 183 on 1 January; designation line at 189.25 dwellings
2. 0301402014: 165 on 30 June; July -2, August -2, September -2, October 0, November 0, December -4; 155 on 1 January; designation line at 150.75 dwellings
3. Title carries the number of designated sections: 7
