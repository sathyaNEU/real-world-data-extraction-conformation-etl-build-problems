"""Independent verifier for task501: reads only the shipped bundle (the target folder) with the csv module and pdfplumber,
shares no code with the generator, recomputes the call (the next-generation matrix from the survey's diaries kept in
school term) and every ask figure (each option's people on the register by the year they were born, and their valid
doses with each twin's dose where it was given), and compares them with generator/figures.json.

    python3 task501/generator/verify.py <target> <figures.json>"""
import csv
import datetime as dt
import json
import os
import re
import sys

import numpy as np

GROUPS = [(0, 4), (5, 9), (10, 14), (15, 19), (20, 24), (25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 54),
          (55, 59), (60, 64), (65, 69), (70, 200)]
OPTS = {"A": (2013, 2017), "B": (2008, 2012), "C": (2003, 2007), "D": (1993, 1997), "E": (1993, 2002)}


def rows(target, name):
    with open(os.path.join(target, name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def find(target, prefix):
    return [f for f in os.listdir(target) if f.startswith(prefix)][0]


def pdf_text(target, name):
    """A shipped PDF's text through pdfplumber, whitespace collapsed (the extractor every PDF read here uses)."""
    import pdfplumber
    with pdfplumber.open(os.path.join(target, name)) as pdf:
        text = " ".join((p.extract_text() or "") for p in pdf.pages)
    return re.sub(r"\s+", " ", text)


def group(a):
    return next(i for i, (lo, hi) in enumerate(GROUPS) if lo <= a <= hi)


def call(target):
    prof = {}
    for r in rows(target, find(target, "measles_immunity_profile")):
        y = 1927 if "earlier" in r["year_of_birth"] else int(r["year_of_birth"])
        prof[y] = float(r["per_cent_immune"]) / 100
    N = np.zeros(15)
    S = np.zeros(15)
    by_yob = {}
    for r in rows(target, find(target, "population_projection")):
        a = 100 if "over" in r["age_at_1_january_2028"] else int(r["age_at_1_january_2028"])
        y = 1927 if "earlier" in r["year_of_birth"] else int(r["year_of_birth"])
        n = int(r["persons"])
        g = group(a)
        N[g] += n
        S[g] += n * (1 - prof[y])
        by_yob[y] = by_yob.get(y, 0) + n
    # the contact matrix from the survey's public use file: the diaries kept in school term (May 2023), mean contacts
    # per participant by participant band (columns) and contact band (rows), contacts of unknown age left out
    labels = ["%d-%d" % g if g[1] < 200 else "70+" for g in GROUPS]
    band = {lab: k for k, lab in enumerate(labels)}
    term = {}
    for r in rows(target, find(target, "nscs_2023_participants")):
        if dt.date.fromisoformat(r["diary_date"]).month == 5:
            term[r["part_id"]] = band[r["age_band"]]
    n = np.bincount(list(term.values()), minlength=15).astype(float)
    C = np.zeros((15, 15))
    for r in rows(target, find(target, "nscs_2023_contacts")):
        j = term.get(r["part_id"])
        if j is not None and r["contact_age_band"] in band:
            C[band[r["contact_age_band"]], j] += 1
    M = (C / n[None, :]).T
    text = pdf_text(target, find(target, "mmr_catch_up_options"))
    made = {}
    for m in re.finditer(r"(\d{4}) to (\d{4}) \d{1,2} to \d{1,2} .*?(\d{1,3}(?:,\d{3})+) (\d{1,3}(?:,\d{3})*) (\d{2})% "
                         r"(\d{1,3}(?:,\d{3})*)", text):
        span = (int(m.group(1)), int(m.group(2)))
        made.setdefault(span, []).append(int(m.group(6).replace(",", "")))
    sp = re.search(r"Of option E.s ([\d,]+) expected people made immune, ([\d,]+) are among those born (\d{4}) to "
                   r"(\d{4}) and ([\d,]+) among those born (\d{4}) to (\d{4})", text)
    n = lambda x: int(x.replace(",", ""))
    e_parts = [((int(sp.group(3)), int(sp.group(4))), n(sp.group(2))), ((int(sp.group(6)), int(sp.group(7))), n(sp.group(5)))]
    assert n(sp.group(1)) == made[(1993, 2002)][0] == sum(x for _, x in e_parts), "option E's split"
    eff = {"A": [((2013, 2017), made[(2013, 2017)][0])], "B": [((2008, 2012), made[(2008, 2012)][0])],
           "C": [((2003, 2007), made[(2003, 2007)][0])], "D": [((1993, 1997), made[(1993, 1997)][0])],
           "E": e_parts}
    q = 15.0 / max(abs(np.linalg.eigvals(M)))

    def R(Sg):
        return float(max(abs(np.linalg.eigvals(q * (Sg / N)[:, None] * M.T))))
    out = {"No catch-up": R(S)}
    for k, parts in eff.items():
        S2 = S.copy()
        for (a, b), mi in parts:
            g = group(2027 - b)
            assert g == group(2027 - a)
            S2[g] -= mi
        out["Option %s" % k] = R(S2)
    return out


def tenth(iso_date):
    d = dt.date.fromisoformat(iso_date)
    return dt.date(d.year + 10, d.month, d.day)


def merged_events(target, unresolved_out=False):
    """Every event with the registration it now belongs to (merges followed to the surviving record), less the GP
    lines the query log shows replaced or withdrawn. unresolved_out: also drop any line whose query is not closed as
    confirmed by the as-at date (an open query read as not standing; the counts must not move)."""
    surv = {r["retired_number"]: r["surviving_number"] for r in rows(target, find(target, "register_merges"))}
    log = rows(target, find(target, "gp_return_queries"))
    drop = {r["line_ref"] for r in log if r["outcome"] in ("Replaced by corrected line", "Withdrawn by practice")}
    if unresolved_out:
        drop |= {r["line_ref"] for r in log if r["outcome"] != "Confirmed as sent" or not r["closed_on"]
                 or r["closed_on"] > "2027-06-30"}
    out = []
    for r in rows(target, find(target, "register_mmr_events")):
        if r["source_ref"] in drop:
            continue
        p = r["person_number"]
        while p in surv:
            p = surv[p]
        out.append((p, dt.date.fromisoformat(r["date_given"]), r["source_ref"]))
    return out


def born(target, ev, rule="both"):
    """Registration -> the date the child was born. A date of birth held ten years early is read ten years on: the
    child was registered from the birth notification 6 to 45 days after the date ten years on (rule "registration"),
    and its first GP dose came 12 to 17 months after that date (rule "first_dose"); the golden takes both."""
    first = {}
    for p, d, ref in ev:
        if ref.startswith("GPR-") and (p not in first or d < first[p]):
            first[p] = d
    out = {}
    for r in rows(target, find(target, "register_people")):
        p, held = r["person_number"], dt.date.fromisoformat(r["date_of_birth"])
        t = tenth(r["date_of_birth"])
        by_reg = 6 <= (dt.date.fromisoformat(r["registered_on"]) - t).days <= 45
        by_dose = p in first and 365 <= (first[p] - t).days <= 525
        hit = {"both": by_reg and by_dose, "registration": by_reg, "first_dose": by_dose}[rule]
        out[p] = t if hit else held
    return out


def residents(target, dob):
    """Registration -> (date of birth as born, living in the region): an address in the State whose local health
    office, read in the scheme in force when recorded, is in the region (LH27 before 1 July 2024 is Monaghan West)."""
    cut = dt.date(2024, 7, 1)
    region = {"LH20", "LH21", "LH22", "LH23", "LH24", "LH25", "LH26"}
    codes = {r["lho_code"]: r["health_region"] for r in rows(target, find(target, "lho_codes"))}
    assert {c for c, h in codes.items() if h == "Oriel Health Region"} == region
    people = {}
    for r in rows(target, find(target, "register_people")):
        code, rec = r["lho_code"], dt.date.fromisoformat(r["lho_recorded"])
        in_state = not r["postcode"].strip().upper().startswith("BT")
        here = in_state and (code in region or (code == "LH27" and rec < cut))
        people[r["person_number"]] = (dob[r["person_number"]], here)
    return people


HOUSE = ("date_of_birth", "sex", "gp_practice", "registered_on", "lho_code", "lho_recorded", "postcode")


def twins_given_back(target, ev, key=HOUSE):
    """A child has one MMR dose at a visit: where one registration holds two GP lines given on one day, the second is
    the dose of the one other registration sharing its key (by default every household field) that holds no GP line
    that day. Returns the events with those lines given back, and the number given back (None where a key leaves a
    doubled day with no single match)."""
    mates = {}
    for r in rows(target, find(target, "register_people")):
        mates.setdefault(tuple(r[k] for k in key), []).append(r["person_number"])
    home = {p: k for k, ps in mates.items() for p in ps}
    days = {}
    for p, d, ref in ev:
        if ref.startswith("GPR-"):
            days.setdefault((p, d), []).append(ref)
    out, moved = list(ev), 0
    give = {}
    for (p, d), refs in days.items():
        if len(set(refs)) < 2:
            continue
        cand = [q for q in mates.get(home.get(p), []) if q != p and (q, d) not in days]
        if len(cand) != 1:
            return ev, None
        for ref in sorted(set(refs))[1:]:
            give[(p, d, ref)] = cand[0]
    for i, (p, d, ref) in enumerate(out):
        if (p, d, ref) in give:
            out[i] = (give[(p, d, ref)], d, ref)
            moved += 1
    return out, moved


def doses(people, ev):
    """Valid doses per person under guidelines 12.5, from the date each was born."""
    asat = dt.date(2027, 6, 30)
    per = {}
    for p, d, ref in ev:
        if d <= asat and p in people:
            per.setdefault(p, []).append(d)
    count = {}
    for q, ds in per.items():
        dob = people[q][0]
        first = dt.date(dob.year + 1, dob.month, dob.day)
        n, prev = 0, None
        for d in sorted(ds):
            if d < first or (prev is not None and (d - prev).days < 28):
                continue
            n, prev = n + 1, d
        count[q] = n
    return count


def figures_of(people, cnt):
    out = {}
    for k, (a, b) in OPTS.items():
        res = [p for p, (dob, here) in people.items() if here and a <= dob.year <= b]
        out[k] = (len(res), sum(1 for p in res if cnt.get(p, 0) == 0), sum(1 for p in res if cnt.get(p, 0) == 1))
    return out


def main(argv):
    target, figs_path = argv[0], argv[1]
    figs = json.load(open(figs_path, encoding="utf-8"))
    bad = []
    r = call(target)
    for k, v in r.items():
        shown = "%.1f" % (np.floor(v * 10 + 0.5) / 10)
        if shown != figs["reproduction_number"][k]:
            bad.append(("R " + k, shown, figs["reproduction_number"][k]))
    below = [k for k, v in r.items() if v < 1]
    if below != ["Option B"] or r["No catch-up"] < 1:
        bad.append(("call", below, "Option B"))
    if any(r_["outcome"] not in ("Confirmed as sent", "Replaced by corrected line", "Withdrawn by practice")
           for r_ in rows(target, find(target, "gp_return_queries"))):
        bad.append(("query log", "an unresolved query", "every query closed"))
    ev = merged_events(target)
    holders = {}
    for p, d, ref in ev:
        if ref.startswith("GPR-"):
            holders.setdefault(ref, set()).add(p)
    if any(len(h) > 1 for h in holders.values()):
        bad.append(("GP lines", "a line on two registrations", "each line on one registration"))
    dob = born(target, ev)
    for rule in ("registration", "first_dose"):
        if born(target, ev, rule) != dob:
            bad.append(("date of birth by the %s alone" % rule, "a different set", "the same registrations"))
    people = residents(target, dob)
    given, n_moved = twins_given_back(target, ev)
    for key in (("date_of_birth", "sex", "gp_practice"), ("date_of_birth", "sex", "registered_on"),
                ("date_of_birth", "sex", "gp_practice", "registered_on")):
        alt, n_alt = twins_given_back(target, ev, key)
        if n_alt != n_moved or sorted(alt) != sorted(given):
            bad.append(("co-twin by " + "/".join(key), "another match", "the household's"))
    cnt = doses(people, given)
    cnt_u = doses(people, twins_given_back(target, merged_events(target, unresolved_out=True))[0])
    got = figures_of(people, cnt)
    if got != figures_of(people, cnt_u):
        bad.append(("open-query reading", "moves the dose counts", "no move"))
    for k in OPTS:
        n_res, n0, n1 = got[k]
        for label, val, key in (("residents", n_res, "ask1_register_residents"), ("none", n0, "ask2_no_valid_dose"),
                                ("one", n1, "ask2_one_valid_dose")):
            if int(figs[key][k].replace(",", "")) != val:
                bad.append((label + " " + k, val, figs[key][k]))
    if bad:
        for b in bad:
            print("VERIFY MISMATCH", b)
        raise SystemExit(1)
    print("VERIFY   independent recomputation matches figures.json: 6 reproduction numbers from the term-time diaries, "
          "the call, 15 ask figures (%d dates of birth read ten years on, the same under either signature alone; %d "
          "twins' GP lines given back, the same under every co-twin key); no GP line on two registrations; the dose "
          "counts do not move with unresolved queries read as not standing"
          % (sum(1 for r_ in rows(target, find(target, "register_people"))
                 if dob[r_["person_number"]].isoformat() != r_["date_of_birth"]), n_moved))


if __name__ == "__main__":
    main(sys.argv[1:])
