"""The files the agency hands over: the extract, the registers, the standard and the rest."""
import csv
import datetime as dt
import json
import os
import random

import world as W
import sim

# the verbatim terms reporters write, and what the dictionary maps them to. The July revision
# brought two of them under one preferred term.
VERBATIM = {
    "Pyrexia": ["Pyrexia", "Fever", "High temperature"],
    "Headache": ["Headache", "Cephalalgia"],
    "Fatigue": ["Fatigue", "Tiredness", "Lassitude"],
    "Myalgia": ["Myalgia", "Muscle pain"],
    "Injection site pain": ["Injection site pain", "Sore arm"],
    "Lymphadenopathy": ["Lymphadenopathy", "Swollen glands"],
    "Nausea": ["Nausea", "Feeling sick"],
    "Dizziness": ["Dizziness", "Light headedness"],
    "Rash": ["Rash", "Skin eruption"],
    "Pruritus": ["Pruritus", "Itching"],
    "Urticaria": ["Urticaria", "Hives"],
    "Diarrhoea": ["Diarrhoea", "Loose stools"],
    "Vomiting": ["Vomiting"],
    "Abdominal pain": ["Abdominal pain", "Stomach pain"],
    "Arthralgia": ["Arthralgia", "Joint pain"],
    "Paraesthesia": ["Paraesthesia", "Tingling"],
    "Syncope": ["Syncope", "Fainting"],
    "Palpitations": ["Palpitations"],
    "Hypertension": ["Hypertension", "Raised blood pressure"],
    "Tachycardia": ["Tachycardia", "Fast heart rate"],
    "Dyspnoea": ["Dyspnoea", "Breathlessness"],
    "Alopecia": ["Alopecia", "Hair loss"],
    "Dry mouth": ["Dry mouth"],
    "Insomnia": ["Insomnia", "Sleeplessness"],
    "Hepatic enzyme increased": ["Hepatic enzyme increased", "Raised liver enzymes"],
    "Thrombocytopenia": ["Thrombocytopenia", "Low platelets"],
}
# what the revision of 20 July changed: one preferred term came inside the agency's seriousness list
SERIOUSNESS_CHANGED = {"Lymphadenopathy"}

DUP_SHARE = {True: 0.76, False: 0.26}   # the campaign's holder submits almost everything it hears


def _off_boundary(d):
    """no submission is received on the first or the last day of the quarter, so reading the window
    inclusively or exclusively selects the same reports"""
    while d in (W.Q_FROM, W.Q_TO):
        d += dt.timedelta(days=1)
    return d


def wr(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def submissions(cases):
    """one submission per case per channel that reported it, in receipt order"""
    rng = random.Random(W.SEED * 23 + 7)
    out = []
    sid = 1200000
    for c in cases:
        chans = [c["channel"]]
        p = DUP_SHARE[c["code"] == W.DOMINANT]
        if rng.random() < p and c["channel"] != "licence holder":
            chans.append("licence holder")
        for k, ch in enumerate(chans):
            sid += 1
            lag = c["lag"] if k == 0 else c["lag"] + rng.choice([1, 2, 3, 4, 6, 8, 11])
            out.append({
                "sub": "SUB-%07d" % sid, "case": c["case"], "channel": ch,
                "receipt": c["receipt"] if k == 0 else min(_off_boundary(
                    c["receipt"] + dt.timedelta(days=rng.choice([0, 1, 1, 2, 3, 5]))),
                    W.CODED_BY - dt.timedelta(days=1)),
                "report": c["receipt"] - dt.timedelta(days=lag),
                "reporter": c["reporter"] if ch != "licence holder" else "other health professional",
                "region": c["region"], "age": c["age"], "sex": c["sex"],
                "code": c["code"], "reactions": c["reactions"],
                "coded": min(c["receipt"] + dt.timedelta(days=rng.choice([1, 2, 2, 3, 4, 6, 9, 14])),
                             W.CODED_BY),
            })
    out.sort(key=lambda s: (s["receipt"], s["sub"]))
    return out


def reported_name(code, receipt):
    """the product name as the reporter gave it, which changed when the licence transferred"""
    if code == W.RENAMED[0] and receipt >= W.TRANSFER:
        return W.RENAMED[2]
    if code == W.RENAMED[0]:
        return W.RENAMED[1]
    if code == W.DOMINANT:
        return W.DOM_NAME
    return dict((p[0], p[1]) for p in W.PRODUCTS)[code]


def verbatim_for(reaction, receipt, rng):
    """what the reporter wrote, and the dictionary version the case was coded at"""
    terms = VERBATIM[reaction]
    v = terms[rng.randrange(len(terms))]
    return v, reaction, "2026.2" if receipt >= W.DICT_REVISION else "2026.1"


def write_extract(tgt, subs):
    rng = random.Random(W.SEED * 29 + 3)
    rows = []
    for s in subs:
        for r in s["reactions"]:
            v, coded, ver = verbatim_for(r, s["receipt"], rng)
            rows.append([s["sub"], s["case"], reported_name(s["code"], s["receipt"]), v, ver,
                         "yes" if r in sim.SERIOUS and rng.random() < .86 else "no"])
    return wr(os.path.join(tgt, "spontaneous_reports_extract.csv"),
              ["submission_id", "case_id", "product_reported", "reaction_verbatim",
               "dictionary_version", "seriousness_reported"], rows)


def write_master(tgt, subs):
    rows = [[s["sub"], s["case"], s["channel"], s["receipt"].isoformat(), s["report"].isoformat(),
             s["coded"].isoformat(), s["reporter"], s["region"], s["age"], s["sex"]] for s in subs]
    return wr(os.path.join(tgt, "report_master.csv"),
              ["submission_id", "case_id", "channel", "receipt_date", "report_date", "coded_date",
               "reporter_type", "region", "age_band", "sex"], rows)


def write_register(tgt):
    rows = []
    for code, name, holder, atc, _n, _ex in W.PRODUCTS:
        if code == W.RENAMED[0]:
            rows.append([code, W.RENAMED[2], W.RENAMED[1], W.TRANSFER.isoformat(), W.RENAMED[4],
                         atc, "2019-04-11"])
        else:
            h = sum(ord(c) for c in code + name)
            rows.append([code, name, "", "", holder, atc, "%d-%02d-%02d" % (
                1998 + h % 27, (h // 7) % 12 + 1, (h // 3) % 27 + 1)])
    rows.append([W.DOMINANT, W.DOM_NAME, "", "", "Nordsund Vaccines A/S", "J07BX", "2024-09-02"])
    rows.sort()
    return wr(os.path.join(tgt, "product_register.csv"),
              ["product_code", "product_name", "former_name", "name_changed_from",
               "licence_holder", "atc_code", "authorised_from"], rows)


def write_dictionary(tgt):
    """both versions in force during the window, each a full release of the mappings"""
    rows = []
    for ver, frm in (("2026.1", "2026-01-15"), ("2026.2", W.DICT_REVISION.isoformat())):
        for pref, terms in sorted(VERBATIM.items()):
            for v in terms:
                term = pref
                if term in SERIOUSNESS_CHANGED:
                    ser = "yes" if ver == "2026.2" else "no"
                else:
                    ser = "yes" if term in sim.SERIOUS else "no"
                rows.append([v, term, ver, frm, ser])
    rows.sort(key=lambda r: (r[2], r[0]))
    return wr(os.path.join(tgt, "reaction_dictionary.csv"),
              ["reaction_verbatim", "preferred_term", "dictionary_version", "version_from",
               "serious"], rows)


def write_listed(tgt):
    rows = sorted([code, r] for code, rs in W.LISTED.items() for r in rs)
    return wr(os.path.join(tgt, "product_information_listed.csv"),
              ["product_code", "preferred_term"], rows)


def write_closed(tgt, cases):
    """the pairs the desk assessed and closed in the twelve months before the window"""
    rng = random.Random(W.SEED * 37 + 11)
    pool = [(c, r) for c, _n, _h, _a, _k, _e in W.PRODUCTS for r in W.LISTED.get(c, ())]
    rng.shuffle(pool)
    rows = []
    d = W.Q_FROM - dt.timedelta(days=360)
    for code, r in pool[:26]:
        d += dt.timedelta(days=rng.choice([6, 9, 11, 14, 17, 21]))
        rows.append([code, r, d.isoformat(),
                     (d + dt.timedelta(days=rng.choice([21, 28, 35, 44, 56]))).isoformat(),
                     rng.choice(["no further action", "no further action", "no further action",
                                 "product information updated", "kept under review"])])
    rows.sort()
    return wr(os.path.join(tgt, "closed_assessments_register.csv"),
              ["product_code", "preferred_term", "opened_on", "closed_on", "outcome"], rows)


def write_campaign(tgt):
    """the regional campaign's doses by week, which is why the quarter looks as it does"""
    rng = random.Random(W.SEED * 41 + 13)
    rows = []
    d = W.Q_FROM
    while d <= W.Q_TO:
        wk = d.isocalendar()[1]
        ramp = 0.18 if d < dt.date(2026, 8, 1) else (1.0 if d < dt.date(2026, 9, 15) else 0.62)
        for reg, share in zip(W.REGIONS, (.31, .23, .11, .15, .20)):
            rows.append([d.isoformat(), wk, reg,
                         int(round(44000 * ramp * share * (0.9 + 0.2 * rng.random())))])
        d += dt.timedelta(days=7)
    return wr(os.path.join(tgt, "campaign_vaccination_log.csv"),
              ["week_commencing", "iso_week", "region", "doses_administered"], rows)


def write_manifest(tgt, counts):
    out = {"run_pulled": W.AS_OF.isoformat(),
           "database": "ADR database, national instance",
           "window_basis": "receipt date",
           "window": {"from": W.Q_FROM.isoformat(), "to": W.Q_TO.isoformat()},
           "files": [{"name": n, "rows": r} for n, r in sorted(counts.items())],
           "notes": ["Submissions that failed coding are held outside the extract and are listed in "
                     "coding_exceptions.csv, which runs to the day before the pull.",
                     "The dictionary is shipped at both versions in force during the window."]}
    p = os.path.join(tgt, "run_inventory.json")
    with open(p, "w") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
    return len(out["files"])
