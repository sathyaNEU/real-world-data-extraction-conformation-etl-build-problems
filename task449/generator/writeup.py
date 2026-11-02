"""Writes submission.md from figures.json (every number it states is a figure the generator computed)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)

QL = ["July to September 2025", "October to December 2025", "January to March 2026", "April to June 2026"]
SHORT = {
    "21232": "software developers and programmers", "31301": "registered nurses and registered psychiatric nurses",
    "32101": "licensed practical nurses", "41221": "elementary school and kindergarten teachers", "62200": "chefs",
    "63200": "cooks", "72200": "electricians (except industrial and power system)", "72300": "plumbers",
    "72400": "construction millwrights and industrial mechanics", "73300": "transport truck drivers",
    "44101": "home support workers, caregivers and related occupations",
    "65201": "food counter attendants, kitchen helpers and related support occupations",
    "75110": "construction trades helpers and labourers", "95106": "labourers in food and beverage processing",
}


def _join(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def fmt(n):
    return "{:,}".format(int(n))


def text(f):
    L = []
    listed = f["listed"]
    named = ["%s %s (%s)" % (o, SHORT[o], f["ratio_%s" % o]) for o in listed]
    L.append("## Tags\n")
    L.append("**Domain:** Survey Research & Official Statistics (census, register and administrative data quality).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Certify these Schedule A occupations for the 2027 order, each at or under 1.5 registered jobseekers "
             "per vacancy over the four reference dates: %s. The other Schedule A occupations do not meet the test.** "
             "Not the list that counts every posting live on the Workshore Job Board as an open vacancy (it adds %s and "
             "drops %s): a self-service posting stays up until its employer takes it down or its %d-day term ends, so "
             "filled jobs in the fast-filling occupations swell their vacancies, while Employer Services' postings "
             "come down on the outcome day.\n"
             % (_join(named), _join(f["default_extra"]), _join(f["default_missing"]), f["term_days"]))
    L.append("## 2. Critical Components\n")
    L.append("1. The occupations that meet the test: %s." % _join(listed))
    L.append("2. Their ratios of registered jobseekers to vacancies, to one decimal: %s."
             % "; ".join("%s %s" % (o, f["ratio_%s" % o]) for o in listed))
    L.append("3. %s do not meet the test once each live self-service posting counts by the chance its job was still "
             "open on the reference date.\n" % _join(f["default_extra"]))
    L.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Read the program guide: an occupation is listed when its registered jobseekers summed over the four reference "
        "dates are at most 1.5 times its vacancies summed over them; a vacancy is a position unfilled on the date with "
        "any employer, and the survey's sector estimates are the official totals.",
        "Stacked both snapshot layouts on the reference dates (NOC 2016 codes through the concordance, migrated postings "
        "by their legacy number) and placed each posting in a survey sector by its employer's NAICS code in the "
        "employer accounts.",
        "Read every posting's term from both activity logs (the new log's UTC times in Eastern time): renewed, taken "
        "down by the employer, expired, or closed by Employer Services.",
        "Estimated each occupation's survival to closure (Kaplan-Meier) from Employer Services postings, published to "
        "closed, open ones censored at the 14 November 2026 extract.",
        "Weighted each live posting: Employer Services postings, and self-service postings renewed in that term or "
        "taken down after the date, count in full; one that ran to term end counts (S(a) - S(e)) / (S(s) - S(e)), with "
        "a its age on the date and s and e its term's start and end.",
        "Shared each sector's survey estimate among occupations by weighted positions, summed the four dates and "
        "divided into each occupation's registered jobseekers (June from the 21 July re-run).",
        "Matched each hire in both referral logs to the client's job_start report at that employer (employer number, "
        "or the employer's name as the client typed it), skipping did_not_start records, and dated referrals carried "
        "to the new platform at go-live from the old platform's referral.",
        "Counted a start as not retained when a job_end report or the latest Record of Employment from the employer's "
        "business number ends the job before day 90.",
    ]
    for i, s in enumerate(steps, 1):
        L.append("%d. %s" % (i, s))
    L.append("")
    L.append("## 4. Deliverable Answers\n")
    L.append("### in_demand_2027_briefing.docx\n")
    L.append("1. The occupations that meet the test: %s." % _join(listed))
    L.append("2. Ratios: %s." % "; ".join("%s %s" % (o, f["ratio_%s" % o]) for o in listed))
    L.append("3. Bar chart of every Schedule A occupation's ratio with the 1.5 line, the occupations that meet the test "
             "marked.\n")
    L.append("### in_demand_2027_tables.xlsx\n")
    L.append("1. Meets the test: %s." % _join(listed))
    L.append("2. Does not meet the test: %s." % _join(f["not_listed"]))
    L.append("3. Ratios of the occupations that meet the test: %s."
             % "; ".join("%s %s" % (o, f["ratio_%s" % o]) for o in listed))
    L.append("4. Clients who started a job in a Schedule A occupation on an Employer Services referral, by quarter of "
             "the start:")
    for k in range(4):
        L.append("   - %s: %s" % (QL[k], fmt(f["starts_q%d" % (k + 1)])))
    L.append("5. Of those, still working for that employer 90 days after starting:")
    for k in range(4):
        L.append("   - %s: %s" % (QL[k], fmt(f["retained_q%d" % (k + 1)])))
    L.append("6. Average days from referral to start:")
    for k in range(4):
        L.append("   - %s: %s" % (QL[k], f["avg_days_q%d" % (k + 1)]))
    return "\n".join(L) + "\n"


def write(f, path):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text(f))


if __name__ == "__main__":
    f = json.load(open(os.path.join(HERE, "figures.json")))
    write(f, os.path.join(TASK, "submission.md"))
