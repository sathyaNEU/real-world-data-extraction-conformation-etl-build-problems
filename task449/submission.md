## Tags

**Domain:** Survey Research & Official Statistics (census, register and administrative data quality).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Certify these Schedule A occupations for the 2027 order, each at or under 1.5 registered jobseekers per vacancy over the four reference dates: 21232 software developers and programmers (1.0), 31301 registered nurses and registered psychiatric nurses (1.1), 32101 licensed practical nurses (1.1), 41221 elementary school and kindergarten teachers (1.2), 62200 chefs (1.2), 63200 cooks (1.3), 72200 electricians (except industrial and power system) (1.3), 72300 plumbers (1.0), 72400 construction millwrights and industrial mechanics (1.2) and 73300 transport truck drivers (1.2). The other Schedule A occupations do not meet the test.** Not the list that counts every posting live on the Workshore Job Board as an open vacancy (it adds 44101, 65201, 75110 and 95106 and drops 62200, 63200, 72200, 72400 and 73300): a self-service posting stays up until its employer takes it down or its 42-day term ends, so filled jobs in the fast-filling occupations swell their vacancies, while Employer Services' postings come down on the outcome day.

## 2. Critical Components

1. The occupations that meet the test: 21232, 31301, 32101, 41221, 62200, 63200, 72200, 72300, 72400 and 73300.
2. Their ratios of registered jobseekers to vacancies, to one decimal: 21232 1.0; 31301 1.1; 32101 1.1; 41221 1.2; 62200 1.2; 63200 1.3; 72200 1.3; 72300 1.0; 72400 1.2; 73300 1.2.
3. 44101, 65201, 75110 and 95106 do not meet the test once each live self-service posting counts by the chance its job was still open on the reference date.

## 3. Step-by-Step Solution

1. Read the program guide: an occupation is listed when its registered jobseekers summed over the four reference dates are at most 1.5 times its vacancies summed over them; a vacancy is a position unfilled on the date with any employer, and the survey's sector estimates are the official totals.
2. Stacked both snapshot layouts on the reference dates (NOC 2016 codes through the concordance, migrated postings by their legacy number) and placed each posting in a survey sector by its employer's NAICS code in the employer accounts.
3. Read every posting's term from both activity logs (the new log's UTC times in Eastern time): renewed, taken down by the employer, expired, or closed by Employer Services.
4. Estimated each occupation's survival to closure (Kaplan-Meier) from Employer Services postings, published to closed, open ones censored at the 14 November 2026 extract.
5. Weighted each live posting: Employer Services postings, and self-service postings renewed in that term or taken down after the date, count in full; one that ran to term end counts (S(a) - S(e)) / (S(s) - S(e)), with a its age on the date and s and e its term's start and end.
6. Shared each sector's survey estimate among occupations by weighted positions, summed the four dates and divided into each occupation's registered jobseekers (June from the 21 July re-run).
7. Matched each hire in both referral logs to the client's job_start report at that employer (employer number, or the employer's name as the client typed it), skipping did_not_start records, and dated referrals carried to the new platform at go-live from the old platform's referral.
8. Counted a start as not retained when a job_end report or the latest Record of Employment from the employer's business number ends the job before day 90.

## 4. Deliverable Answers

### in_demand_2027_briefing.docx

1. The occupations that meet the test: 21232, 31301, 32101, 41221, 62200, 63200, 72200, 72300, 72400 and 73300.
2. Ratios: 21232 1.0; 31301 1.1; 32101 1.1; 41221 1.2; 62200 1.2; 63200 1.3; 72200 1.3; 72300 1.0; 72400 1.2; 73300 1.2.
3. Bar chart of every Schedule A occupation's ratio with the 1.5 line, the occupations that meet the test marked.

### in_demand_2027_tables.xlsx

1. Meets the test: 21232, 31301, 32101, 41221, 62200, 63200, 72200, 72300, 72400 and 73300.
2. Does not meet the test: 13110, 33102, 42202, 44101, 62020, 64100, 65100, 65102, 65200, 65201, 65310, 72106, 72310, 72410, 73400, 75101, 75110, 85101, 94141 and 95106.
3. Ratios of the occupations that meet the test: 21232 1.0; 31301 1.1; 32101 1.1; 41221 1.2; 62200 1.2; 63200 1.3; 72200 1.3; 72300 1.0; 72400 1.2; 73300 1.2.
4. Clients who started a job in a Schedule A occupation on an Employer Services referral, by quarter of the start:
   - July to September 2025: 920
   - October to December 2025: 783
   - January to March 2026: 799
   - April to June 2026: 923
5. Of those, still working for that employer 90 days after starting:
   - July to September 2025: 694
   - October to December 2025: 575
   - January to March 2026: 586
   - April to June 2026: 680
6. Average days from referral to start:
   - July to September 2025: 29.5
   - October to December 2025: 29.5
   - January to March 2026: 29.7
   - April to June 2026: 28.5
