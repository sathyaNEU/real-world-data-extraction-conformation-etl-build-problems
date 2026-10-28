"""task464 architecture 6: the input pack.

Writes the authority's own records. Nothing here states a fill rate, a yield or a ranking: the commissioning
schedule gives places funded, the enrolment extracts give enrolments, and the two live in different systems.

Layer 1 mess, all of it produced by the authority's own systems and none of it carrying the stump:
  the two intakes come out of different intake systems, so AUT25 is a flat CSV and SPR26 is JSON with its own
  field names; two partners were renamed by a merger part way through, so the AUT25 extract carries old names
  and SPR26 carries codes; local learner references are re-issued across partners, so only the unique learner
  number joins; the achievement release ships preliminary and revised with an overlap.
"""
import csv, json, os, datetime as dt
import numpy as np
import world as W
import sim as S

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")

# The merger: the trading name in use for the autumn intake, before the rename.
FORMER_NAME = {"ASH": "Ashcombe Community College", "FAI": "Fairholt Skills Centre"}
WARDS = ["TCA-01", "TCA-02", "TCA-03", "TCA-04", "TCA-05", "TCA-06", "TCA-07", "TCA-08"]
AGE_BANDS = ["19-23", "24-29", "30-39", "40-49", "50-59", "60+"]
PRIOR = ["Entry 3", "Level 1", "Level 1 partial", "none recorded"]
COURSE = {"AUT25": "NUM2-A", "SPR26": "NUM2-B"}


def _d(s):
    return dt.date.fromisoformat(s)


def build(sim):
    rng = np.random.default_rng(W.SEED + 7)
    os.makedirs(OUT, exist_ok=True)
    apps, offers, enrol_a, enrol_s, ach = [], [], [], [], []
    uln_counter = 1000000000

    for p in W.PARTNERS:
        for ik in W.INTAKES:
            c = sim["cells"][(p["key"], ik["code"])]
            n = c["n"]
            term = _d(ik["term_start"])
            census = _d(ik["census"])
            # the partner's ballot runs ballot_weeks before the census date
            ballot_day = census - dt.timedelta(weeks=p["ballot_weeks"])
            order_pos = np.argsort(c["rank"])          # applicant index in ballot order
            for i in range(n):
                uln_counter += 1
                uln = str(uln_counter)
                ref = "AP-%s-%s-%05d" % (ik["code"], p["key"], i + 1)
                # applications arrive over the ten weeks before the ballot
                appdate = ballot_day - dt.timedelta(days=int(rng.integers(7, 77)))
                apps.append({
                    "application_ref": ref, "uln": uln, "partner_code": p["key"],
                    "intake_code": ik["code"], "application_date": appdate.isoformat(),
                    "ballot_position": int(c["rank"][i]) + 1,
                    "ward_code": WARDS[int(rng.integers(0, len(WARDS)))],
                    "age_band": AGE_BANDS[int(rng.integers(0, len(AGE_BANDS)))],
                    "prior_attainment": PRIOR[int(rng.integers(0, len(PRIOR)))],
                })
                # offers. Round 1 is the ballot itself; later rounds are the waitlist working down the order.
                if c["offered"][i]:
                    first = bool(c["won_first"][i])
                    if first:
                        odate = ballot_day
                        rnd = 1
                    else:
                        # the waitlist works down the order between the ballot and the census date
                        depth = int(c["rank"][i]) - c["places"] + 1
                        span = max(1, c["boundary"] - c["places"] + 1)
                        frac = min(1.0, depth / span)
                        days = (census - ballot_day).days
                        odate = ballot_day + dt.timedelta(days=max(1, int(round(frac * max(1, days - 1)))))
                        rnd = 2
                    took = bool(c["enrolled"][i])
                    resp = "accepted" if took else ("declined" if rng.random() < 0.82 else "no response")
                    rdate = odate + dt.timedelta(days=int(rng.integers(1, 9)))
                    if rdate > census:
                        rdate = census
                    offers.append({
                        "offer_ref": "OF-%s-%s-%05d" % (ik["code"], p["key"], len(offers) + 1),
                        "application_ref": ref, "offer_round": rnd,
                        "offer_date": odate.isoformat(), "response": resp,
                        "response_date": rdate.isoformat(),
                    })
                    if took:
                        start = term + dt.timedelta(days=int(rng.integers(0, 12)))
                        row = {"uln": uln, "course_code": COURSE[ik["code"]],
                               "start_date": start.isoformat(), "application_ref": ref}
                        if ik["code"] == "AUT25":
                            # layout A: the partner by its trading name at the time
                            enrol_a.append(dict(row, provider_name=FORMER_NAME.get(p["key"], p["name"]),
                                                learner_ref="%s/%05d" % (p["key"], (i % 9000) + 1)))
                        else:
                            # layout B, a different system: codes, different field names, nested
                            enrol_s.append({"learnerUln": uln, "providerCode": p["key"],
                                            "course": COURSE[ik["code"]],
                                            "enrolment": {"startDate": start.isoformat(),
                                                          "applicationRef": ref},
                                            "localRef": "%s/%05d" % (p["key"], (i % 9000) + 1)})
                # achievement: released for every applicant the authority tracks, enrolled or not
                outcome = "achieved" if c["achieved"][i] else "not achieved"
                award = _d(ik["release_prelim"]) - dt.timedelta(days=int(rng.integers(5, 40)))
                ach.append({"uln": uln, "partner_code": p["key"], "intake_code": ik["code"],
                            "course_code": COURSE[ik["code"]], "outcome": outcome,
                            "award_date": award.isoformat()})
    return apps, offers, enrol_a, enrol_s, ach


def write(apps, offers, enrol_a, enrol_s, ach):
    """Writes the call's own path. Row order is fixed, so two rebuilds are byte identical."""
    written = []

    def csvw(name, rows, fields):
        rows = sorted(rows, key=lambda r: tuple(str(r[f]) for f in fields[:2]))
        path = os.path.join(OUT, name)
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
            w.writeheader()
            for r in rows:
                w.writerow({k: r[k] for k in fields})
        written.append((name, len(rows)))

    csvw("place_applications_2025_2026.csv", apps,
         ["application_ref", "uln", "partner_code", "intake_code", "application_date",
          "ballot_position", "ward_code", "age_band", "prior_attainment"])
    csvw("place_offers.csv", offers,
         ["offer_ref", "application_ref", "offer_round", "offer_date", "response", "response_date"])
    csvw("enrolments_autumn_2025.csv", enrol_a,
         ["provider_name", "learner_ref", "uln", "course_code", "start_date", "application_ref"])

    # The spring intake comes out of the replacement intake system: JSON, its own field names.
    sp = sorted(enrol_s, key=lambda r: (r["providerCode"], r["learnerUln"]))
    path = os.path.join(OUT, "enrolments_spring_2026.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"extract": "Learner Enrolment Extract", "intake": "SPR26",
                   "generatedFor": "Thornmere Combined Authority adult skills return",
                   "records": sp}, fh, indent=1, sort_keys=False)
        fh.write("\n")
    written.append(("enrolments_spring_2026.json", len(sp)))

    # The achievement release ships twice. The revised release restates a slice of the preliminary one and is
    # the one in force; both are shipped because both were issued.
    rng = np.random.default_rng(W.SEED + 19)
    prelim, revised = [], []
    for r in sorted(ach, key=lambda r: (r["partner_code"], r["uln"])):
        prelim.append(dict(r, release="preliminary"))
        revised.append(dict(r, release="revised"))
    # a slice of the preliminary release carried a provisional outcome that the revised release corrects
    idx = rng.choice(len(prelim), size=int(len(prelim) * 0.031), replace=False)
    for j in idx:
        prelim[j] = dict(prelim[j], outcome="result pending")
    fields = ["uln", "partner_code", "intake_code", "course_code", "outcome", "award_date", "release"]
    csvw("achievement_release_preliminary.csv", prelim, fields)
    csvw("achievement_release_revised.csv", revised, fields)
    return written


def main():
    sim = S.simulate()
    rows = write(*build(sim))
    for name, n in rows:
        print("  %-42s %7d rows" % (name, n))
    return rows


if __name__ == "__main__":
    main()
