"""Tallybridge's agreements, built over the real register. Rows are built without side effects; references and
signatory names are assigned once, at the end, so tuning by trial cannot disturb them."""
import datetime as dt
import string

import pandas as pd
from faker import Faker

import roles
from world import AS_AT, annual_value, band_of, rng, term_for

D = dt.date
OFFICER_ROLES = ["Chief Financial Officer", "Business Manager", "Finance Manager", "Chief Executive",
                 "Business Manager", "Finance Manager", "Director of Finance and Operations"]
SCHOOL_ROLES = ["Headteacher", "Headteacher", "Headteacher", "School Business Manager", "Business Manager",
                "Finance Manager"]
LGR_NEW = {940, 941, 942, 943, 838, 839}
# Tallybridge's own people, who must never turn up as a customer's signatory
RESERVED = {"Pamela Andrews", "Henry Miles", "Leah O'Neill", "Joel Bailey", "Philip Saunders", "Maureen Webb"}
# the short form a person may give their first name when they sign
SHORT = {"Alexander": "Alex", "Andrew": "Andy", "Anthony": "Tony", "Benjamin": "Ben", "Catherine": "Cath",
         "Christine": "Chris", "Christopher": "Chris", "Daniel": "Dan", "David": "Dave", "Deborah": "Debbie",
         "Edward": "Ed", "Elizabeth": "Liz", "Frederick": "Fred", "Gregory": "Greg", "Jacqueline": "Jackie",
         "James": "Jim", "Jennifer": "Jen", "Jonathan": "Jon", "Joseph": "Joe", "Joanne": "Jo", "Josephine": "Jo",
         "Katherine": "Kate", "Kathryn": "Kate", "Kenneth": "Ken", "Leonard": "Len", "Margaret": "Maggie",
         "Matthew": "Matt", "Michael": "Mike", "Nicholas": "Nick", "Nicola": "Nicky", "Patricia": "Pat",
         "Peter": "Pete", "Rebecca": "Becky", "Richard": "Rich", "Robert": "Rob", "Samantha": "Sam",
         "Samuel": "Sam", "Stephen": "Steve", "Steven": "Steve", "Susan": "Sue", "Terence": "Terry",
         "Thomas": "Tom", "Timothy": "Tim", "Victoria": "Vicky", "William": "Will"}


def name_variant(name):
    """The same person's name as typed on another agreement: a short first name, or an initial."""
    first, last = name.split(" ", 1)
    return "%s %s" % (SHORT[first], last) if first in SHORT else "%s. %s" % (first[0], last)


def sf_contact(key):
    r = rng("contact", *[str(k) for k in key])
    alpha = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "0034K00" + "".join(alpha[i] for i in r.integers(0, len(alpha), 11))


def sf_id(*key):
    r = rng("sfid", *key)
    alpha = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "0014K00" + "".join(alpha[i] for i in r.integers(0, len(alpha), 11))


def avoid_window(d):
    """No agreement starts between 11 September and 22 October, so 1 October never sits near a term boundary."""
    if (d.month == 9 and d.day >= 11) or (d.month == 10 and d.day <= 22):
        return D(d.year, 11, 1)
    return d


def rand_start(r, lo_year, hi_year, months=(9, 9, 9, 9, 4, 4, 1, 3, 5, 11, 2, 6)):
    y = int(r.integers(lo_year, hi_year + 1))
    m = int(months[int(r.integers(0, len(months)))])
    return avoid_window(D(y, m, 1))


def school_row(reg, urn_current, start, signer_key, role, signed_on, *, urn_recorded=None, status="In force",
               end=None, kind="Per pupil", site=None, uid=None, tag=None):
    cur = reg.info[int(urn_current)]
    rec = urn_recorded if urn_recorded is not None else urn_current
    recrow = reg.info[int(rec)]
    band = band_of(cur["PhaseOfEducation (name)"])
    on = AS_AT if end is None else end - dt.timedelta(days=1)
    ts, te = term_for(start, on)
    pupils = int(cur["NumberOfPupils"])
    if site is not None:
        pupils = int(round(pupils * site[1]))
    billed = roles.pupils_billed(urn_current if site is None else "%s/%s" % (urn_current, site[0]), pupils, ts)
    la = int(recrow["LA (code)"])
    estno = int(recrow["EstablishmentNumber"]) if not pd.isna(recrow["EstablishmentNumber"]) else 0
    if (la in LGR_NEW and not pd.isna(recrow.get("PreviousLA (code)"))
            and not pd.isna(recrow.get("PreviousEstablishmentNumber")) and start < D(2021, 4, 1)):
        la, estno = int(recrow["PreviousLA (code)"]), int(recrow["PreviousEstablishmentNumber"])
    name = recrow["EstablishmentName"]
    if site is not None:
        name = "%s (%s site)" % (name, site[0])
    return dict(account_key=("acc", int(rec), site[0] if site else None), account_name=name, urn=int(rec),
                dfe_number="%d%04d" % (la, estno), billing_basis=kind, price_band=band, pupils_billed=billed,
                agreement_start=start, current_term_start=ts,
                current_term_end=te if end is None else end - dt.timedelta(days=1),
                annual_value_gbp=annual_value(band, ts, billed), status=status,
                signer_key=signer_key, signed_by_role=role, signed_on=signed_on,
                urn_current=int(urn_current), uid=uid, tag=tag, site=site[0] if site else None,
                pupils_current=pupils)


def group_row(reg, uid, covered, start, role, tag):
    """One agreement on the lead school's account that bills every school it covers, the lead first."""
    lead = int(covered[0])
    row = school_row(reg, lead, start, ("officer", uid), role, start, uid=uid, tag=tag)
    ts = row["current_term_start"]
    pupils = [int(reg.info[int(s)]["NumberOfPupils"]) for s in covered]
    billed = [roles.pupils_billed(int(s), p, ts) for s, p in zip(covered, pupils)]
    row["covers"] = [int(s) for s in covered]
    row["covers_pupils"] = pupils
    row["pupils_billed"] = sum(billed)
    row["annual_value_gbp"] = round(sum(annual_value(row["price_band"], ts, b) for b in billed), 2)
    row["pupils_current"] = sum(pupils)
    return row


def group_value(x, ts, shift=0):
    """A group agreement's annual value for the term starting `ts`, each school billed and priced on its own;
    `shift` moves the lead school's billed pupils (the settle step's nudge)."""
    total = 0.0
    for i, (s, p) in enumerate(zip(x["covers"], x["covers_pupils"])):
        b = roles.pupils_billed(int(s), p, ts) + (shift if i == 0 else 0)
        total += annual_value(x["price_band"], ts, b)
    return round(total, 2)


def central_rows(reg, uid, acads, purchase, scope, pre_k, tag, r, subset=None):
    """The trust office bought for every academy it held at `purchase` (primaries only when scope says so)."""
    role = OFFICER_ROLES[int(r.integers(0, len(OFFICER_ROLES)))]
    if subset is not None:
        cov = acads[acads["URN"].isin(subset)]
    else:
        cov = acads[acads["joined"].dt.date < purchase]
        if scope == "primary":
            cov = cov[cov["band"] == "Primary"]
    rows, pre_left = [], pre_k
    for _, a in cov.iterrows():
        urn = int(a["URN"])
        start, rec = purchase, None
        if pre_left > 0 and not pd.isna(a["open_d"]):
            cs = D(int(a["open_d"].year) - 2, 4, 1)
            if cs.year >= 2015 and cs < purchase:
                p = roles.pred_eligible(reg, urn, cs)
                if p is not None:
                    start, rec = cs, p
                    pre_left -= 1
        rows.append(school_row(reg, urn, start, ("officer", uid), role, purchase, urn_recorded=rec, uid=uid,
                               tag=tag))
    return rows, pre_left


def devolved_rows(reg, uid, acads, k, pre_k, tag, r, smallest=True, exclude=()):
    sell = acads[~acads["URN"].isin(exclude)].sort_values(["NumberOfPupils", "URN"], ascending=[smallest, True])
    pool = sell.head(max(3 * k, k + 2))
    order = list(pool.index)
    r.shuffle(order)
    rows, pre_left = [], pre_k
    # place the pre-conversion agreements first, on academies that can carry one
    for idx in list(order):
        if pre_left == 0 or len(rows) >= k:
            break
        a = acads.loc[idx]
        if pd.isna(a["open_d"]):
            continue
        cs = D(int(a["open_d"].year) - 1, 11, 1)
        if cs.year < 2015:
            continue
        p = roles.pred_eligible(reg, int(a["URN"]), cs)
        if p is None:
            continue
        rows.append(school_row(reg, int(a["URN"]), cs, ("head", int(a["URN"])), SCHOOL_ROLES[len(rows) % 6],
                               term_for(cs, AS_AT)[0], urn_recorded=p, uid=uid, tag=tag))
        order.remove(idx)
        pre_left -= 1
    for idx in order:
        if len(rows) >= k:
            break
        a = acads.loc[idx]
        start = rand_start(r, 2019, 2025)
        conv = a["open_d"]
        if not pd.isna(conv) and conv.date() > start:
            start = avoid_window(D(conv.year + 1, 1, 1))
        rows.append(school_row(reg, int(a["URN"]), start, ("head", int(a["URN"])),
                               SCHOOL_ROLES[int(r.integers(0, len(SCHOOL_ROLES)))], term_for(start, AS_AT)[0],
                               uid=uid, tag=tag))
    return rows, pre_left


def net_of(acads, rows):
    return roles.RATE * float(acads["NumberOfPupils"].sum()) - sum(x["annual_value_gbp"] for x in rows)


def finalise(rows, names_seed=116):
    """Assign agreement references in start order and signatory names, once."""
    f = Faker("en_GB")
    f.seed_instance(names_seed)
    used, who = set(), {}

    def person(key):
        if key not in who:
            while True:
                n = "%s %s" % (f.first_name(), f.last_name())
                if n not in used and n not in RESERVED:
                    used.add(n)
                    who[key] = n
                    break
        return who[key]

    order = sorted((i for i in range(len(rows)) if not rows[i].get("copy_of")),
                   key=lambda i: (rows[i]["agreement_start"], rows[i]["urn"] or 0, str(rows[i]["site"]),
                                  rows[i]["billing_basis"]))
    n = 100417
    for i in order:
        x = rows[i]
        r = rng("refgap", i)
        n += 1 + int(r.integers(0, 4))
        x["agreement_ref"] = "TBA-%06d" % n
        x["account_id"] = sf_id(*x["account_key"])
        x["signed_by"] = person(x["signer_key"])
    # a signer who shares a surname with another (a business manager and a head, different first names)
    for x in rows:
        if x.get("surname_from") and not x.get("copy_of"):
            key, other = x["signer_key"], x["surname_from"]
            surname = who[other].split(" ", 1)[1]
            if who[key].split(" ", 1)[1] != surname:
                while True:
                    first = f.first_name()
                    cand = "%s %s" % (first, surname)
                    if first != who[other].split(" ", 1)[0] and cand not in used and cand not in RESERVED:
                        used.add(cand)
                        who[key] = cand
                        break
    for x in rows:
        if not x.get("copy_of"):
            x["signed_by"] = who[x["signer_key"]]
            if x.get("name_variant"):
                x["signed_by"] = name_variant(x["signed_by"])
            x["signed_by_contact_id"] = sf_contact(x["signer_key"])
    by_id = {id(x): x for x in rows}
    for x in rows:
        if x.get("copy_of"):
            o = by_id[x["copy_of"]]
            x["agreement_ref"] = o["agreement_ref"]
            x["account_id"] = sf_id(*x["account_key"])
            x["signed_by"] = o["signed_by"]
            x["signed_by_contact_id"] = o["signed_by_contact_id"]
    return rows
