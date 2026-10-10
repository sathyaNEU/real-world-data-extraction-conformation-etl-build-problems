# solver round: round 2, plain

**Proxy score 50.4 / 100** (recommendation 5.0 of 35, instruction 7.0 of 7, asks 38.4 of 58). Main call missed. 4 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: The 2027 order should designate seven sections: 0301401008, 0301402014, 4625001005, 4625002007, 4625011004, 4625011016 and 4625012009.

solver: The 2027 order should designate six of the fourteen watch-list sections: 0301401008 (Alacant d.1, 28.0%), 0301402014 (Alacant d.2, 25.7%), 4625001005 (València Ciutat Vella, 31.4%), 4625002007 (l'Eixample, 29.3%), 4625011004 (Poblats Marítims, 33.3%) and 4625012009 (Camins al Grau, 26.2%). The designated section closest to the 25% line is 0301402014 (155 of 603 dwellings, 25.7%, +0.7 pp). The undesignated section closest to it is 4625001012 (183 of 757, 24.2%, -0.8 pp); it drops out because the public body bought 20 of its dwellings on 6 Nov 2026 under its right of first refusal.

tokens matched 1 of 1 (4625011016)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| designation_brief_2027.pdf | 1 | 3 | 3 | 100% |
| designation_brief_2027.pdf | 2 | 0 | 2 | 0% |
| designation_brief_2027.pdf | 3 | 3 | 3 | 100% |
| designation_brief_2027.pdf | 4 | 3 | 3 | 100% |
| designation_annex_2027.csv | 1 | 50 | 51 | 98% |
| section_bridge_2027.png | 1 | 5 | 13 | 38% |
| section_bridge_2027.png | 2 | 6 | 14 | 43% |
| section_bridge_2027.png | 3 | 1 | 2 | 50% |

## Solver's path

1. Rebuilt 30 Jun 2026 holdings from declaracions_grans_tenidors: for each declarant, took its latest quarter's original return (the last return stays valid if it filed nothing since), swapped in substitutive returns (S), added complementary ones (C), and dropped option (OP) and reservation (RS) lines. 14-character parcel lines were expanded to individual dwellings using the cadastre unit numbers. Malformed references were fixed (spaces and dashes removed, case normalised, 18-character references matched on their first 18 characters). Only residential cadastre units were kept. Result: all 14 sections match the T2 bulletin exactly (e.g. 0301402014 = 165, 4625001012 = 205).
2. Applied deeds from escriptures_inscrites signed 1 Jul to 30 Sep 2026 in watch sections (by signing date): 115 sales and 5 inheritances. A dwelling counts as large-holder (LH) owned at 1 Jan 2027 only if its owner is on the register at that date (registre Titulars). Notable move: Ràfec Habitatge bought 18 dwellings from private sellers on 6 Aug, adding 18 to 4625012009.
3. Checked the public-body budget file (EPPR, PPO programme, phase D commitments). These are first-refusal purchases (tempteig) of notified sales. In all 27 completed cases the deed to Q4600731F was signed exactly 120 days after the commitment, regardless of the sale date declared. So for October to 1 January, a tempteig dwelling passes to the public body (which is not a large holder) on commitment date + 120 days, replacing the declared sale. Declared pending sales without tempteig are applied on their declared date and to their declared buyer.
4. Effect of tempteig: B08104283's 20 dwellings in 4625001012 (declared for sale on 16 Feb 2027) go to the public body on 6 Nov 2026, so 205 becomes 183 (24.2%). B28984920's 13 December sales in 0301402014 move to deeds in January 2027, so they stay large-holder owned at 1 Jan and the section holds 155 (25.7%).
5. Article 4 test: share of cadastre residential dwellings at or above 25%. Six sections pass. Distances: 0301402014 +0.70 pp, 4625012009 +1.21 pp, 4625001012 -0.83 pp, 4625011016 -1.60 pp.
6. Largest group: each owner's group as at 1 Jan 2027 from the register's Vinculacions sheet (effective dates), named from codis_grup.csv; owners with no group go by their register name. This covers the reused codes GT0141 and GT0158, Llucana's move from Terrat to Finestral on 16 Nov, Trespol Castelló leaving Porxo on 13 Dec, and Ribot leaving Cantonera.
7. Dwellings with nobody registered: the September 2026 padró delivery, with June used for the districts September omits (Alacant 02, València 11 and 12). Castelló delivers one row per dwelling, so persones = 0 means empty. TIE-T and PAS registrations not renewed within 2 years were treated as expired. Counted large-holder dwellings at 1 Jan 2027 with no valid registration.
8. Bridges: monthly net change in large-holder dwellings from the event roll-forward, July to December 2026. Designation line = 25% of the section's dwellings: 150.75 for 0301402014 and 189.25 for 4625001012.

confidence: medium-high

notes: The October–December transfers are projected from the pending sales declared at 30 Jun and from the public body's tempteig commitments, dated commitment + 120 days. No file records a sale contracted after 30 Jun outside tempteig. Expired TIE-T/PAS registrations were excluded; the empty-dwelling counts come out the same whether expiry is judged at the delivery date or at 1 Jan 2027.

### designation_brief_2027.pdf (solver's answers)
- designated list and count: 6 sections: 0301401008 Alacant d.1; 0301402014 Alacant d.2; 4625001005 València Ciutat Vella; 4625002007 València l'Eixample; 4625011004 València Poblats Marítims; 4625012009 València Camins al Grau
- designated section closest to the line: 0301402014 (Alacant, district 2, section 014): large-holder share 25.7% (155/603); distance from line +0.7 pp
- undesignated section closest to the line: 4625001012 (València, Ciutat Vella, section 012): large-holder share 24.2% (183/757); distance from line -0.8 pp (0.8 pp below)

### designation_annex_2027.csv (solver's answers)
- 0301401008: LH dwellings 157; share 28.0%; largest group Grup Cantonera, 43 dwellings; LH dwellings with nobody registered 8
- 0301402014: LH dwellings 155; share 25.7%; largest group Grup Barana, 38; no one registered 9
- 0301405003: LH dwellings 109; share 17.8%; largest group Grup Cantonera, 28; no one registered 5
- 1204001006: LH dwellings 154; share 22.4%; largest group Grup Porxo, 40; no one registered 9
- 1204003011: LH dwellings 92; share 17.8%; largest group Grup Arcada, 25; no one registered 6
- 4625001005: LH dwellings 255; share 31.4%; largest group Grup Barana, 89; no one registered 14
- 4625001012: LH dwellings 183; share 24.2%; largest group Grup Xamfrà, 75; no one registered 11
- 4625002007: LH dwellings 202; share 29.3%; largest group Grup Finestral, 73; no one registered 9
- 4625002019: LH dwellings 163; share 22.6%; largest group Grup Finestral, 50; no one registered 12
- 4625005013: LH dwellings 183; share 20.8%; largest group Grup Escaire, 47; no one registered 10
- 4625011004: LH dwellings 310; share 33.3%; largest group Grup Barana, 108; no one registered 17
- 4625011016: LH dwellings 150; share 23.4%; largest group Grup Mitgera, 48; no one registered 7
- 4625012009: LH dwellings 141; share 26.2%; largest group Grup Ràfec, 54; no one registered 13
- 4625013021: LH dwellings 149; share 19.9%; largest group Grup Andana, 48; no one registered 6

### section_bridge_2027.png (solver's answers)
- 0301402014 bridge: 30 Jun bulletin 165 → Jul -2, Aug -2, Sep -2, Oct 0, Nov 0, Dec -4 → 155 at 1 Jan 2027; designation line 150.75 dwellings (25% of 603)
- 4625001012 bridge: 30 Jun bulletin 205 → Jul -1, Aug 0, Sep 0, Oct -1, Nov -20, Dec 0 → 183 at 1 Jan 2027; designation line 189.25 dwellings (25% of 757)
- title count: 6 designated sections
