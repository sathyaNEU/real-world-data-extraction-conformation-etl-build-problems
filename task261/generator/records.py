"""Writers for the pack's records: the survey's public-use files as a data archive releases them (the household summary
extract, one row per household per implicate; the person file, one row per person, no implicates since ages are never
imputed; the replicate weight file, one row per household) and Kelvane Life's extracts as its systems write them (the
client register pulled 12 January 2027, the Retirement Income Account pensions at 31 December 2026 with their
nominations, and the lifetime annuity lives listing pulled 12 January 2027 for the 31 December valuation)."""
from __future__ import annotations

import csv
import datetime as dt

import numpy as np

import common as K
import insurer as I

SUMMARY_COLS = ["hhid", "imp", "wgt", "state", "hrp_age", "hrp_sex", "couple", "n_persons", "tenure", "income",
                "assets", "debts", "networth", "house", "super"]


def _writer(path):
    fh = open(path, "w", newline="", encoding="utf-8")
    return fh, csv.writer(fh, lineterminator="\n")


# ---------------------------------------------------------------------------------------------- the survey
def write_summary(path, d):
    order = np.argsort(d["hhid"])
    n_persons = np.bincount([p[0] for p in d["persons"]], minlength=len(d["hhid"]))
    sex_ref = {p[0]: p[3] for p in d["persons"] if p[1] == 1}
    fh, w = _writer(path)
    w.writerow(SUMMARY_COLS)
    rows = 0
    for i in order:
        for m in range(K.IMPLICATES):
            w.writerow([d["hhid"][i], m + 1, "%.4f" % d["wgt"][i], d["state"][i], min(int(d["ref"][i]), 85), sex_ref[i],
                        "Y" if d["couple"][i] else "N", int(n_persons[i]), d["tenure"][i], int(d["income"][m, i]),
                        int(d["assets"][m, i]), int(d["debts"][m, i]), int(d["nw"][m, i]), int(d["house"][m, i]),
                        int(d["super"][m, i])])
            rows += 1
    fh.close()
    return rows


def write_persons(path, d):
    rows = sorted(((d["hhid"][i], rel, age, sex) for i, rel, age, sex in d["persons"]), key=lambda x: (x[0], x[1] != 1))
    fh, w = _writer(path)
    w.writerow(["hhid", "pnum", "relationship", "age", "sex"])
    cur, k = None, 0
    for hh, rel, age, sex in rows:
        k = k + 1 if hh == cur else 1
        cur = hh
        w.writerow([hh, k, rel, min(age, 85), sex])
    fh.close()
    return len(rows)


def write_repweights(path, d):
    order = np.argsort(d["hhid"])
    fh, w = _writer(path)
    w.writerow(["hhid"] + ["rw%03d" % (r + 1) for r in range(K.REPLICATES)])
    for i in order:
        w.writerow([d["hhid"][i]] + ["%.4f" % x if x else "0" for x in d["repw"][:, i]])
    fh.close()
    return len(order)


# ---------------------------------------------------------------------------------------------- Kelvane Life
STATES = ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT", "NT"]
STATE_P = [.32, .26, .2, .1, .07, .02, .02, .01]
OPTIONS = ["Balanced", "Growth", "Conservative", "Cash"]


def write_crm(path, B):
    r = K.rng("crm-file")
    states = r.choice(STATES, len(B.P), p=STATE_P)
    rows = []
    for p in B.P:
        if not p["client"] or (p["since"] is not None and p["since"] > K.PULL):
            continue
        dead = p["dod"] is not None and p["notified"] is not None and p["notified"] <= K.PULL \
            and not p.get("register_unaware")
        rows.append([p["client_id"], p["hh"], p["dob"].isoformat(), p["sex"], states[p["pid"]], p.get("marital", ""),
                     (p["since"] or dt.date(2010, 1, 1)).isoformat(), "Deceased" if dead else "Active",
                     p["dod"].isoformat() if dead else "", ""])
    for o in B.retired:
        rows.append([o["client_id"], o["hh"], o["dob"].isoformat(), o["sex"], states[o["pid"]], o.get("marital", ""),
                     (o["since"] or dt.date(2010, 1, 1)).isoformat(), "Merged", "", o["merged_into"]])
    rows.sort(key=lambda x: x[0])
    fh, w = _writer(path)
    w.writerow(["client_id", "household_id", "date_of_birth", "sex", "state", "marital_status", "client_since",
                "status", "date_of_death", "merged_into"])
    w.writerows(rows)
    fh.close()
    return len(rows)


def write_ria(path, B):
    r = K.rng("ria-file")
    accs = sorted((a for a in B.acc if not a.get("closed")), key=lambda a: a["account"])
    opts = r.choice(OPTIONS, len(accs), p=[.46, .19, .26, .09])
    fh, w = _writer(path)
    w.writerow(["account_no", "member_id", "pension_type", "commenced", "investment_option", "payment_frequency",
                "annual_payment_2026_27", "balance_31_12_2026"])
    # the period-end run takes a member's balance and annual payment from the member's summary
    total = {}
    for a in accs:
        t = total.setdefault(a["owner"], [0.0, 0.0])
        t[0] += a["payment"]
        t[1] += a["balance"]
    for a, opt in zip(accs, opts):
        pay, bal = total[a["owner"]] if a.get("member_total") else (a["payment"], a["balance"])
        w.writerow([a["account"], a["owner_id"], a["type"], a["commenced"].isoformat(), opt, a["freq"],
                    "%.2f" % pay, "%.2f" % bal])
    fh.close()
    return len(accs)


def write_nominations(path, B):
    from faker import Faker
    fk = Faker("en_AU")
    fk.seed_instance(K.SEED % 100000)
    r = K.rng("nominations-file")
    rows = []
    for n in sorted(B.nom, key=lambda n: (B.acc[n["acc"]]["account"], n["rel"])):
        a = B.acc[n["acc"]]
        if a.get("closed"):
            continue
        if n["person"] is not None:
            pp = B.P[n["person"]]
            name = (fk.first_name_male() if pp["sex"] == "M" else fk.first_name_female()) + " " + fk.last_name()
            dob = pp["dob"].isoformat()
        elif n["rel"] == "Child":
            name = fk.first_name() + " " + fk.last_name()
            dob = I.dob_for_age(r, n["child_age"]).isoformat()
        else:
            name, dob = "Legal personal representative", ""
        rows.append([a["account"], n["kind"], name, dob, n["rel"], n["share"],
                     I.rand_date(r, max(a["commenced"], dt.date(2015, 1, 1)), dt.date(2026, 11, 30)).isoformat()])
    fh, w = _writer(path)
    w.writerow(["account_no", "nomination_type", "nominee_name", "nominee_date_of_birth", "relationship",
                "share_percent", "effective_from"])
    w.writerows(rows)
    fh.close()
    return len(rows)


def write_annuities(path, B):
    fh, w = _writer(path)
    w.writerow(["contract_no", "life_no", "client_id", "date_of_birth", "sex", "commenced", "payments_start",
                "indexation", "payment_frequency", "reversion_percent", "annual_amount", "life_status", "date_of_death"])
    n = 0
    for c in sorted(B.ann, key=lambda c: c["contract"]):
        l1, l2 = c["life1"], c["life2"]
        base = I.amount_at_pull(c, B.P[l1]["dod"])
        for no, p in ((1, l1), (2, l2)):
            if p is None:
                continue
            pp = B.P[p]
            dead = pp["dod"] is not None and pp["notified"] is not None and pp["notified"] <= K.PULL
            amt = base if no == 1 else round(I.amount_at_pull(c) * c["pct"] / 100, 2)
            w.writerow([c["contract"], no, pp["client_id"], pp["dob"].isoformat(), pp["sex"], c["commenced"].isoformat(),
                        (c["pay_from"] or c["commenced"]).isoformat(), c["index"], c["freq"],
                        c["pct"] if c["pct"] else "", "%.2f" % amt, "Deceased" if dead else "Alive",
                        pp["dod"].isoformat() if dead else ""])
            n += 1
    fh.close()
    return n
