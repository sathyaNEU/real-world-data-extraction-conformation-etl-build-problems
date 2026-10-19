"""The cracker and the mirror on the cut pack, scored against figures.json.

The cracker lands the call and runs the hygiene battery (key uniqueness on NHS numbers and episode identifiers, exact
duplicates, the master index's merged numbers and spaced NHS numbers, deaths on the Spine), then takes each ask as
the questionnaire states it from the file that carries it: B1 and B2 from the episodes open on 30 September 2026,
less the patients the Spine records as dead, by the latest diagnosis on the record; C1 and C2 from the pathway
tracker's referral and diagnosis dates. The mirror stops off the call (the slope through every sitting) and takes
the other natural reading of each ask: every episode still open on the extract, and the tracker's dates.

Weights are the skill's: 38 for the call and its components, 7 for instruction-following, 55 for the asks, a figure
a hit at its stated rounding."""
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K      # noqa: E402
import pack as PK       # noqa: E402

DAY = K.WINDOW[1]


def episodes_open(P):
    ep = P["episodes"].copy()
    ep["nhs"] = PK.digits(ep.nhs_number)
    ep["start"] = pd.to_datetime(ep.episode_start).dt.date
    ep["end"] = pd.to_datetime(ep.episode_end.replace("", None)).dt.date
    ep["clinic"] = ep.site_code.map(P["site2clinic"])
    return ep[(ep.start <= DAY) & (ep.end.isna() | (ep.end > DAY))]


def ask_a(P, spine=True):
    op = episodes_open(P)
    pmi = P["pmi"][P["pmi"].record_status == "Active"].set_index("nhs")
    if spine:
        dod = pd.to_datetime(pmi.date_of_death.replace("", None)).dt.date
        op = op[~op.nhs.map(dod).apply(lambda d: d is not None and not pd.isna(d) and d <= DAY)]
    lat = PK.latest_dx(P, DAY)
    op = op[op.nhs.map(lat).fillna("").map(PK.in_scope)]
    dob = pd.to_datetime(pmi.date_of_birth).dt.date
    age = op.nhs.map(dob).apply(lambda b: K.TRIAL_ENTRY.year - b.year - ((1, 1) < (b.month, b.day)))
    op = op.assign(age=age.values)
    return ({c: op[op.clinic == c].nhs.nunique() for c in K.NAMES},
            {c: op[(op.clinic == c) & (op.age <= K.AGE_LIMIT)].nhs.nunique() for c in K.NAMES})


def ask_b(P):
    tr = P["tracker"].copy()
    tr["ref"] = pd.to_datetime(tr["Referral date"]).dt.date
    tr["dxd"] = pd.to_datetime(tr["Diagnosis date"]).dt.date
    a0, a1 = K.ASK_YEAR
    t = tr[tr.dxd.notna()]
    t = t[(t.dxd >= a0) & (t.dxd <= a1)].copy()
    t["days"] = [(d - r).days for d, r in zip(t.dxd, t.ref)]
    share = {c: round(100.0 * float((t[t.Clinic == c].days <= K.SIX_WEEKS).mean()), 1) for c in K.NAMES}
    mean = {c: round(float(t[t.Clinic == c].days.mean()), 1) for c in K.NAMES}
    return share, mean


def score(fig, a_under, a_age, b_share, b_mean):
    rows, h = [], 0
    for c in K.NAMES:
        hits = [a_under[c] == fig["ask_a"]["under_follow_up"][c], a_age[c] == fig["ask_a"]["aged_85_or_under"][c],
                b_share[c] == fig["ask_b"]["within_42_days_pct"][c], b_mean[c] == fig["ask_b"]["average_days"][c]]
        h += sum(hits)
        rows.append((c, a_under[c], fig["ask_a"]["under_follow_up"][c], a_age[c], fig["ask_a"]["aged_85_or_under"][c],
                     b_share[c], fig["ask_b"]["within_42_days_pct"][c], b_mean[c], fig["ask_b"]["average_days"][c],
                     "".join("x" if x else "." for x in hits)))
    return h, rows


def run(task, quiet=False):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    P = PK.load(os.path.join(task, "target"))
    total = 32
    ca, rows_c = score(fig, *ask_a(P, spine=True), *ask_b(P))
    ma, rows_m = score(fig, *ask_a(P, spine=False), *ask_b(P))
    cracker = 38 + 7 + 55.0 * ca / total
    mirror = 5 + 7 + 55.0 * ma / total
    pair = (cracker + mirror) / 2
    if not quiet:
        for title, rows in (("cracker", rows_c), ("mirror", rows_m)):
            print(title, "(clinic, B1 got/golden, B2 got/golden, C1 got/golden, C2 got/golden, hits)")
            for r in rows:
                print("   %-12s B1 %4d/%4d  B2 %4d/%4d  C1 %5.1f/%5.1f  C2 %5.1f/%5.1f  %s" % r)
        print("cracker keeps %d of %d ask figures; mirror keeps %d of %d" % (ca, total, ma, total))
        print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of the ask weight"
              % (cracker, mirror, pair, 100.0 * ma / total))
    return dict(cracker_hits=ca, mirror_hits=ma, total=total, pair=pair, cracker=cracker, mirror=mirror)


if __name__ == "__main__":
    r = run(os.path.dirname(HERE))
    sys.exit(0 if r["cracker_hits"] == 0 else 1)
