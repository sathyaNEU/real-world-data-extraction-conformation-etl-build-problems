# task116 submission

## Tags

**Domain:** Product Analytics, monetization and subscriptions (packaging a trust-wide licence beside per-school subscriptions).
**Analytical objective:** Opportunity Sizing & Decision Support (the new recurring revenue a capped round of trust-wide licences can realise, from each eligible trust's room to grow down to what can be signed).

## 1. Final Recommendation

**Take the Trust Licence to Bishop Hogarth Catholic Education Trust, Pathway Trust, Swale Academies Trust, Derby Diocesan Academy Trust, Tudor Grange Academies Trust, Advance Learning Partnership, Bradford Diocesan Academies Trust, Bishop Wilkinson Catholic Education Trust, St Oscar Romero Catholic Academy Trust and The Ted Wragg Multi Academy Trust, in that order, and put £152,257 of new recurring revenue on the 2027-28 plan.**

The tenth trust plans at £8,659 against £7,349 for Diocese of Chichester Academy Trust, the first below the line. Not a round that counts an agreement as one school: Bishop Hogarth and Derby Diocesan each have three academies on one agreement that the CRM keys to its lead school, so that count leaves both out and puts Pathway Trust first. Not a round valued at the pilot's own sign rate: the plan takes the rate of the Trust Licence offers closed to date, and the CRM holds a thirteenth offer, declined on 30 September. Not GLF Schools, The Spencer Academies Trust or the other trusts with more room to grow: different people signed their academies' agreements, and the round plan offers the licence only where the same person signed every one. Not a round that counts signatures by name rather than by person, which drops Pathway Trust and St Oscar Romero Catholic Academy Trust because their officer's name is typed two ways on agreements recorded against one CRM contact. Not a round built on agreements read under the URNs the book recorded, which misses the academies that converted after they subscribed and fails to reproduce the pilot.

## 2. Critical Components

1. The plan's sign rate is **7 of 13** Trust Licence offers closed to date.
2. With agreements matched to their academies through the register's successor links, licence fee less the agreements replaced reproduces all **12** pilot offers to the pound.
3. Bishop Hogarth Catholic Education Trust and Derby Diocesan Academy Trust each have **3** academies on one agreement, keyed to one school in the agreements export and named in full on the invoice for its current term.
4. **68** of the 146 open multi-academy trusts outside the pilot with two or more academies on agreements, counting every school an invoice bills, meet the plan's condition that one person signed them all; the tenth of them plans at **£8,659** and Diocese of Chichester Academy Trust, first below the line, at **£7,349**.
5. The round puts **£152,257** on the 2027-28 plan.

## 3. Step-by-Step Solution

1. Took the agreements in force on 1 October 2026 from tb_agreements_2026-10-01.csv and matched each recorded URN to its open academy through the successor links in links_edubasealldata20261007.csv.
2. Read which schools each agreement bills from the invoice for its current term in tb_billing_ledger_2025-04_2026-09.csv: four agreements each bill three or four academies, Bishop Hogarth's and Derby Diocesan's among them.
3. Grouped the academies on agreements by trust from edubasealldata20261007.csv: 146 open multi-academy trusts outside the pilot have at least two academies on agreements, counting every school each invoice bills.
4. Kept the trusts where one CRM contact (signed_by_contact_id) signed every agreement, per the eligibility paragraph of trust_partnerships_plan_2027.docx: 68 trusts.
5. Priced each at £4.05 a pupil on every open academy less the agreements it replaces (licence terms 3 and 4), the construction that reproduces all 12 offers in trust_licence_pilot_2026.xlsx.
6. Planned each of the 68 at new recurring revenue x 7/13, the sign rate of the 13 Trust Licence offers closed to date in tb_crm_opportunities_2022-2026.csv, rounded to the pound, per the round plan.
7. Ranked them: the tenth plans at £8,659, Diocese of Chichester Academy Trust next at £7,349, a gap of £1,310.
8. Recommendation: the ten trusts in that order, £152,257 on the 2027-28 plan.

## 4. Deliverable Answers

### trust_round_spring2027.pptx

1. First slide names the ten trusts in priority order and £152,257 on the 2027-28 plan.
2. Chart building the round up in priority order, each trust's step labelled with the running total after it:
   - 1. Bishop Hogarth Catholic Education Trust: £24,100
   - 2. Pathway Trust: £47,126
   - 3. Swale Academies Trust: £66,927
   - 4. Derby Diocesan Academy Trust: £82,992
   - 5. Tudor Grange Academies Trust: £98,364
   - 6. Advance Learning Partnership: £111,865
   - 7. Bradford Diocesan Academies Trust: £123,991
   - 8. Bishop Wilkinson Catholic Education Trust: £134,272
   - 9. St Oscar Romero Catholic Academy Trust: £143,598
   - 10. The Ted Wragg Multi Academy Trust: £152,257
3. Set after the tenth: Diocese of Chichester Academy Trust, £7,349 planned, £1,310 below the tenth.
4. The chart title carries £152,257.

### trust_round_spring2027.xlsx

1. The workings for the ten: each trust's licence fee, the agreements it replaces, its new recurring revenue, planned value and running total, ending on £152,257.
2. The book at 1 October, pupils billed and recurring revenue:
   - Academies, primary band: 212,265 pupils, £1,030,156
   - Academies, secondary band: 235,861 pupils, £1,222,775
   - Free schools, primary band: 7,264 pupils, £35,239
   - Free schools, secondary band: 13,050 pupils, £72,706
   - Local authority maintained schools, primary band: 251,454 pupils, £1,246,858
   - Local authority maintained schools, secondary band: 70,320 pupils, £368,710
   - Special schools, primary band: none
   - Special schools, secondary band: 14,233 pupils, £81,079
3. Pilot licences, what was credited back when each replaced the schools' subscriptions, and what it bills for 2026-27 net of that credit:
   - Education Learning Trust: £2,189 credited, £12,006 net
   - Gateway Multi Academy Trust: £3,809 credited, £12,816 net
   - Generations Multi Academy Trust: £2,224 credited, £9,189 net
   - Grove Learning Trust: £2,568 credited, £8,363 net
   - Leodis Academies Trust: £2,394 credited, £10,995 net
   - Our Lady Immaculate Catholic Academies Trust Ltd: £4,129 credited, £13,590 net
   - Three Spires Trust: £3,717 credited, £12,835 net
4. Weekly active pupils per hundred billed, weeks beginning 7 September to 12 October 2026:
   - Academies, primary band: 56.4
   - Academies, secondary band: 32.4
   - Free schools, primary band: 55.7
   - Free schools, secondary band: 32.3
   - Local authority maintained schools, primary band: 55.1
   - Local authority maintained schools, secondary band: 31.7
   - Special schools, primary band: none
   - Special schools, secondary band: 26.7
