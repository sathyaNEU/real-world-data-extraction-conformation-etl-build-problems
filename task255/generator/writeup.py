"""submission.md from the golden figures (golden.figures), every number written from figures.json's values."""


def pct(p):
    return "%d" % p["pct"]


def kr(x):
    return "{:,}".format(int(x))


def write(F, path):
    joins = F["joins"]
    others = [p for p in F["practices"] if not p["joins"]]
    j_names = ", ".join("%s (%s) %s%%" % (p["name"], p["code"], pct(p)) for p in joins)
    L = []
    L += ["## Tags", "",
          "**Domain:** Pharmacology, Pharmacoepidemiology & Safety (medication adherence and persistence).",
          "**Analytical objective:** Descriptive & Distribution Analysis.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Yes: %s general practices join the 2027 statin follow-up programme: %s.**" % (len(joins), j_names),
          "Each kept fewer than 60 per cent of its new statin users of the second half of 2025 persistent for twelve "
          "months, with each patient's tablets timed at the daily dose their own refills show; every other practice "
          "is at %d per cent or more." % F["floor_others"], ""]
    L += ["## 2. Critical Components", "",
          "1. Twelve-month persistence of the new statin users of 1 July to 31 December 2025 by practice (per cent, "
          "persistent of new users): " + "; ".join("%s %s (%d of %d)" % (p["code"], pct(p), p["k"], p["n"])
                                                     for p in F["practices"]) + ".",
          "2. Joining (under 60): " + ", ".join(p["code"] for p in joins) + "; nearest to the line from above: "
          "%s at %s." % (min(others, key=lambda p: p["share"])["code"], pct(min(others, key=lambda p: p["share"]))),
          ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Read statin_dispensings_202401_202612.csv (dates day-month-year to June 2024, ISO after), joined each "
          "product number to statin_products.csv for ATC code, strength and pack size, and took tablets as packs "
          "times pack size.",
          "2. Took as new users the pseudonyms whose first dispensing from 1 July to 31 December 2025 had no statin "
          "dispensing in the 365 days before, at the practice (practice_register_2026.xlsx) that prescribed that "
          "first dispensing: %s patients." % kr(F["cohort"]),
          "3. Estimated each new user's daily dose from their own dispensings as the tablets dispensed before the "
          "last dispensing over the days from the first to the last (median refill rate, last three refills and "
          "the first year only give the same status for every patient); a patient with one dispensing runs out "
          "within the year at any dose.",
          "4. Laid each dispensing's tablets end to end at that dose from the first dispensing, tablets in hand "
          "used first, and called a patient persistent when no run of more than 30 days without tablets fell in "
          "the 365 days; took each practice's share and set it against 60 per cent "
          "(statin_followup_programme_2027.pdf 2.1, 3.1, 3.2).",
          "5. For the pilot, recovered each pharmacy's rate from pilot_statements_2026.pdf as each statement's "
          "amount over the conversations of its quarter in pilot_conversations_2026.xlsx not cancelled by the "
          "quarter's last day (one rate across the four quarters), and multiplied it by the conversations held in "
          "2026 and never cancelled (pharmacy_pilot_agreement_2026.pdf 2.1).",
          "6. For continuing users, joined the two pseudonyms of each person whose personal number was replaced in "
          "2026 (same birth date and sex, the first pseudonym's dispensings ending before the second's begin, on "
          "the same product line and practice), kept persons with a dispensing in each quarter of 2026 and counted "
          "them at the practice of their last 2026 dispensing (programme 3.3).", ""]
    L += ["## 4. Deliverable Answers", "", "### statinprogram_2027.xlsx", "",
          "1. Joins the programme in 2027: " + ", ".join("%s %s" % (p["code"], p["name"]) for p in joins) + ".",
          "2. Twelve-month persistence by practice (per cent):"]
    for p in F["practices"]:
        L.append("   - %s %s: %s" % (p["code"], p["name"], pct(p)))
    L.append("3. What each pilot pharmacy is entitled to for 2026 (DKK):")
    for p in F["pharmacies"]:
        L.append("   - %s %s: %s" % (p["code"], p["name"], kr(p["due"])))
    L.append("4. Continuing statin users of 2026 by practice (persons):")
    for u in F["users"]:
        L.append("   - %s %s: %d" % (u["code"], u["name"], u["users"]))
    L += ["", "### statinprogram_2027.pdf", "",
          "1. One-page note to the practice planning committee recommending the %s practices, with a bar chart of "
          "each practice's persistence against the 60 per cent line." % len(joins), ""]
    open(path, "w", encoding="utf-8").write("\n".join(L))


def figure_values(F):
    out = []
    for p in F["practices"]:
        out += [p["pct"], p["k"], p["n"], p["code"]]
    for p in F["pharmacies"]:
        out += [kr(p["due"]), p["due"], p["rate"], p["held"], p["paid"]]
    for u in F["users"]:
        out += [u["users"], u["code"]]
    out += [len(F["joins"]), F["cohort"], kr(F["cohort"]), F["floor_others"], 60, 365, 30, 12]
    return out
