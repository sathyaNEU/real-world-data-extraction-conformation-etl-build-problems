## Tags

**Domain:** Human Factors & Ergonomics (human reliability assessment).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Hold the family re-slot as drawn: it would take Aubrine's 2027 mis-pick claims to about 3,800, 3.7 per 10,000 order lines against the Schedule 3 limit of 2.5, where today's layout stays at 1.7.**
Not the 2026 claims per line carried onto 2027 (about 1,700, inside the limit), which assumes the layout cannot change what the check-weigh lets through. Not a look-alike multiplier fitted on claims beside same-line or same-family faces, which reads the claims' clustering as pickers erring more and also stays inside the limit.

## 2. Critical Components

1. The baseline is **1,619** validated wrong-item claims on **9,682,373** order lines in the 52 weeks to 20 September 2026
2. **15.6%** of those picks sat beside a face whose item weighs within 15 g of theirs; on the plan's faces and 2027 lines **34.5%** would
3. Claims run at **10.71** per 10,000 picks beside a face within 15 g, the same beside look-alike and other neighbours

## 3. Step-by-Step Solution

1. Counted the validated Wrong item received claims in aubrine_claims_register.xlsx on lines despatched 22 September 2025 to 20 September 2026, as Schedule 3 counts them: 1,619, on 9,682,373 lines in pick_velocity_by_week.csv.
2. Placed each claim's products and each MISPICK hold's items on location_master.csv through item_master.csv: every wrong item came from the face to the left or right on the same shelf, every claim's pair weighs within 15 g and every hold's pair further apart (pack_bench_procedure.pdf, step 3), and holds plus claims per line are the same whatever the neighbour.
3. Weighted each item's share of neighbours within 15 g by its lines: 15.6% of 2026 picks, 10.71 claims per 10,000 such picks.
4. Rebuilt the plan's shelves from slotting_plan_2027.xlsx (Faces 2027) with its 2027 forecast lines: 34.5% of 2027 picks would sit beside a face within 15 g, against 15.9% on today's faces.
5. Carried 10.71 per 10,000 onto both layouts: 3,800 claims and 3.7 per 10,000 lines under the plan, 1.7 under today's layout, against the limit of 2.5.
6. In corsley_invoice_lines.csv each Premium reconciliation line is the night hours at GBP 1.47 plus the Sunday hours at GBP 2.36 of the four-week pay period ending the Sunday nine days before its invoice; spread back onto those shifts and added to the hours billed, by the month each shift started, it gives the cost of an agency hour worked.
7. In returns_grading_log.csv, kept each return's latest grade and read grades 2 and 3 as repack and scrap on bench sheets and as scrap and repack on the handheld from 8 June 2026, the one reading under which ravelrig_invoices_2025-26.pdf reproduces at constant prices (GBP 0.84 small, GBP 1.31 large); shares and scrapped value at item_master.csv standard cost, by family.
8. The plan breaks the limit and today's layout does not, so the re-slot is held as drawn.

## 4. Deliverable Answers

### reslot_claims_2027.xlsx

1. Mis-pick claims on 2027's order lines under the family re-slot: 3,800.
2. Claims per 10,000 order lines, 2027: 3.7 under the re-slot, 1.7 under today's layout; the limit is 2.5, so the re-slot is over it.
3. Cost of an agency hour worked, by month (GBP):
   - September 2025: 16.38
   - October 2025: 16.37
   - November 2025: 16.52
   - December 2025: 16.32
   - January 2026: 16.15
   - February 2026: 16.15
   - March 2026: 16.20
   - April 2026: 16.77
   - May 2026: 16.88
   - June 2026: 16.86
   - July 2026: 16.83
   - August 2026: 16.84
4. Returned units, October 2025 to September 2026, by family:
   - Make-up: repacked 21.0%, scrapped 20.4%, stock value scrapped GBP 27,088
   - Skincare: repacked 16.3%, scrapped 28.8%, stock value scrapped GBP 26,512
   - Fragrance: repacked 25.8%, scrapped 23.5%, stock value scrapped GBP 23,931
   - Haircare: repacked 27.6%, scrapped 19.8%, stock value scrapped GBP 8,772
   - Bath and body: repacked 17.8%, scrapped 25.8%, stock value scrapped GBP 6,068

### reslot_review_2027.pptx

1. One slide, the call in its title, with a bar chart of claims per 10,000 order lines: the actual for the 52 weeks at 1.7, today's layout at 1.7 and the family re-slot at 3.7 for the coming year, and the Schedule 3 limit of 2.5 as a dashed line.
