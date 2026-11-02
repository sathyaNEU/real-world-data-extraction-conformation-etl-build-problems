"""submission.md and figures.json, every figure emitted from the frame the goldens are written from."""
import json

import analysis as AN
import pack

H, L = pack.FILES["holds"], pack.FILES["loans"]


def money(x):
    return "£{:,}".format(int(x))


def num(x):
    return "{:,}".format(int(x))


def write(F, sub_path, fig_path):
    rows = F["rows"]
    by = {r["fac"]: r for r in rows}
    worst = sorted(AN.FAC_ORDER, key=lambda f: -abs(F["km_amount100"][f] - by[f]["amount100"]))[:2]
    figs = {
        "call": {r["name"]: r["amount100"] for r in rows},
        "fund": "180,000",
        "holds": {r["name"]: r["holds"] for r in rows},
        "holds_total": num(F["holds_total"]),
        "hold_weeks": {r["name"]: r["hw100"] for r in rows},
        "amount_total": num(F["amount_total100"]),
        "cancelled": num(F["n_cancelled"]),
        "offered": num(F["n_offered"]),
        "km_default_named": {by[f]["name"]: F["km_amount100"][f] for f in AN.FAC_ORDER},
        "rules": {"grace_days": 14, "cap_weeks": 10, "cap_days": 84, "offer_hours": 48, "loans": 40, "left": 10},
        "spend": {by[f]["name"]: F["spend"][f]["r10"] for f in AN.FAC_ORDER},
        "references": ["2027", "100", "10", "2.2", "2.3", "3.2", "3.4", "1"],
        "uncovered": {by[f]["name"]: F["uncovered"][f] for f in AN.FAC_ORDER},
        "uncovered_total": F["uncovered_total"],
        "metered": {by[f]["name"]: F["metered"][f] for f in AN.FAC_ORDER},
        "metered_total": F["metered_total"],
    }
    call_txt = ", ".join("%s %s" % (r["name"], money(r["amount100"])) for r in rows)
    km_txt = ", ".join("%s %s" % (by[f]["name"], money(F["km_amount100"][f])) for f in worst)
    out = []
    out.append("## Tags")
    out.append("")
    out.append("**Domain:** General Statistics & Data Science (missing data, censoring and measurement error: a "
               "university library dividing a course e-textbook fund among faculties on the hold-weeks their "
               "students waited, where a cancelled hold's wait runs to the moment the platform would have offered "
               "it a copy).")
    out.append("**Analytical objective:** Descriptive & Distribution Analysis.")
    out.append("")
    out.append("## 1. Final Recommendation")
    out.append("")
    out.append("**Credit the Course Texts Fund 2027 of £180,000 as %s.** Each cancelled hold waits until the "
               "earliest-placed-first rule would have reached it, and the record shows that moment: the first copy "
               "that came free after the cancellation and went to a hold placed after it, or to nobody. Not the "
               "survival estimate with cancellations treated as censored, which moves money between faculties "
               "(%s, among others), because the students who cancel are the ones who saw a long queue ahead of "
               "them, so the holds still waiting are not like the ones that left." % (call_txt, km_txt))
    out.append("")
    out.append("## 2. Critical Components")
    out.append("")
    out.append("1. Holds counted (students, placed 12 January to 26 April 2026 by UK time): %s, of which %s were "
               "offered a copy and %s were cancelled." % (num(F["holds_total"]), num(F["n_offered"]),
                                                           num(F["n_cancelled"])))
    out.append("2. Holds by faculty: " + ", ".join("%s **%s**" % (r["name"], num(r["holds"])) for r in rows) + ".")
    out.append("3. Hold-weeks by faculty, to the nearest 100: " +
               ", ".join("%s **%s**" % (r["name"], num(r["hw100"])) for r in rows) + ".")
    out.append("4. Amounts by faculty, to the nearest £100: " +
               ", ".join("%s **%s**" % (r["name"], money(r["amount100"])) for r in rows) + ".")
    out.append("")
    out.append("## 3. Step-by-Step Solution")
    out.append("")
    out.append("1. Took the holds in %s placed from 12 January to 26 April 2026 by UK date, dropped patron type "
               "Staff, and gave each the faculty of its department code's school under Schedule 1 of "
               "UC-26-114_course_texts_fund_2027_terms.pdf." % H)
    out.append("2. Took a hold's wait to its offer_made_at where it was offered a copy (fulfilled or lapsed).")
    out.append("3. Listed, title by title, every instant a copy came free (ended_at in %s and the expiry of every "
               "lapsed offer) and the hold placed earliest among those offered a copy at that instant." % L)
    out.append("4. Ended each cancelled hold's wait at the first such instant after its cancellation whose copy went "
               "to a hold placed after it or to no hold (Shelfmark terms 2.2).")
    out.append("5. Took hold-weeks as the wait capped at 84 days, less 14 days, in weeks and never below zero, summed "
               "them by faculty and divided £180,000 in proportion.")
    out.append("6. Spend: converted euro and dollar invoice lines at the month's Finance Office rate, mapped each fund "
               "code to its faculty from 1 August 2026 under Schedule 2, and shared each CT-CORE package line by the "
               "package's titles (KBART online identifiers) on each faculty's 2025-26 essential lists, an item's "
               "ISBN taken through the catalogue's related-record and preceding-edition links to its e-book.")
    out.append("7. Spring lists: counted each 2025-26 Semester 2 essential item whose work had no e-book of the cited "
               "edition or later licensed on 12 January 2026, by title line or by a package then in force.")
    out.append("8. 40-loan licences: took each licence bought before 1 September 2025 at its status-report figure "
               "(one absent from that report had lapsed) and later ones at 40, made every checkout to 30 October 2026 "
               "on the earliest-purchased licence not on loan with loans left, started a re-licence when a licence's "
               "fortieth loan ended (the title's re-licence dated that day, lowest reference first) and charged it to "
               "that licence's faculty, then summed the loans left on licences in force by faculty.")
    out.append("")
    out.append("## 4. Deliverable Answers")
    out.append("")
    out.append("### course_texts_fund_2027.csv")
    out.append("")
    out.append("1. Credit by 2026-27 fund code, to the nearest £100:")
    for r in rows:
        out.append("   - %s (%s): %s" % (r["code"], r["name"], money(r["amount100"])))
    out.append("")
    out.append("### course_texts_fund_2027.xlsx")
    out.append("")
    out.append("1. Division sheet, holds counted, hold-weeks (nearest 100) and amount (nearest £100), with a bar "
               "chart of the amounts:")
    for r in rows:
        out.append("   - %s: %s holds; %s hold-weeks; %s" % (r["name"], num(r["holds"]), num(r["hw100"]),
                                                             money(r["amount100"])))
    out.append("2. Course text spend on invoice lines dated 1 January to 31 October 2026, to the nearest £10:")
    for f in AN.FAC_ORDER:
        out.append("   - %s: %s" % (by[f]["name"], money(F["spend"][f]["r10"])))
    out.append("3. Essential spring 2026 reading-list items the Library could not lend as an e-book on 12 January "
               "2026:")
    for f in AN.FAC_ORDER:
        out.append("   - %s: %d" % (by[f]["name"], F["uncovered"][f]))
    out.append("4. Loans left on the 40-loan licences charged to each faculty and in force at the end of 30 October "
               "2026:")
    for f in AN.FAC_ORDER:
        out.append("   - %s: %s" % (by[f]["name"], num(F["metered"][f])))
    out.append("")
    with open(sub_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(figs, fh, indent=1, sort_keys=True)
    return figs
