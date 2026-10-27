"""The ask sheet's cracker and mirror, run on the cut pack: the pilot's first consultations and six-week follow-ups
by quarter in Krathwold and Lathcombe (16 figures) as a careful solver computes them by each route it could take,
scored against the golden (asks.py). An integer figure is a hit only when it is exact.

    python3 task270/generator/cracker.py [TARGET]"""
from __future__ import annotations

import datetime as dt
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A        # noqa: E402
import common as K      # noqa: E402
import pilot as PL      # noqa: E402

NETS = {"Krathwold": "KRT", "Lathcombe": "LTH"}


def records(target, statements=True):
    """The export, and with statements the payment records the export lacks; each patient through the crosswalk."""
    E, S, P, xmap = A.load_pilot(target)
    rows = E[["record_id", "pharmacy_ods", "network", "patient_ref", "consultation_type", "date", "recorded_on"]].copy()
    rows["rec"] = pd.to_datetime(rows["recorded_on"], dayfirst=True).dt.date
    if statements:
        pay = S[S["line"] == "Payment"]
        late = pay[~pay["record_id"].isin(set(E["record_id"]))].rename(columns={"ods": "pharmacy_ods"})
        late = late.assign(network="", rec=late["statement"].map(lambda m: dt.datetime.strptime(m, "%b %Y").date()))
        rows = pd.concat([rows, late[["record_id", "pharmacy_ods", "network", "patient_ref", "consultation_type",
                                      "date", "rec"]]], ignore_index=True)
    rows["pat"] = rows["patient_ref"].map(lambda k: xmap.get(k, k))
    rows["recovered"] = rows["record_id"].isin(set(S.loc[S["line"] == "Recovery", "record_id"]))
    loc = {r.ods_code: (r.locality, r.relocated_on, r.previous_locality) for r in P.itertuples()}
    label = dict(zip(E["pharmacy_ods"], E["network"]))

    def on_day(ods, d):
        l, when, prev = loc[ods]
        if when and d < dt.date.fromisoformat(when):
            l = prev
        return NETS.get(l)

    rows["net_day"] = [on_day(o, d) for o, d in zip(rows["pharmacy_ods"], rows["date"])]
    rows["net_label"] = rows["pharmacy_ods"].map(lambda o: NETS.get(label.get(o, "")))
    return rows


def count(rows, net="net_day", drop="none", keep="earliest"):
    """C1 and C2 by network and quarter. drop: none, recovered (every recovered record), second (the golden: a
    recovered first consultation whose patient has another first consultation not recovered). keep: which of a
    patient's remaining first consultations is the patient's first (earliest by date, first recorded, or all)."""
    R = rows.copy()
    first = R["consultation_type"] == "First consultation"
    if drop == "recovered":
        R = R[~R["recovered"]]
    elif drop == "second":
        kept = set(R.loc[first & ~R["recovered"], "pat"])
        R = R[~(first & R["recovered"] & R["pat"].isin(kept))]
    F = R[(R["consultation_type"] == "First consultation") & (R["date"] >= PL.PILOT_START)
          & (R["date"] <= PL.PILOT_END)].copy()
    if keep == "earliest":
        F = F.sort_values(["date", "rec", "record_id"]).drop_duplicates("pat", keep="first")
    elif keep == "recorded":
        F = F.sort_values(["rec", "date", "record_id"]).drop_duplicates("pat", keep="first")
    F["n"] = F[net]
    F = F[F["n"].notna()]
    fu = R[R["consultation_type"] == "Follow-up"].groupby("pat")["date"].apply(list).to_dict()
    C1 = {(n, q): 0 for n in ("KRT", "LTH") for q in (1, 2, 3, 4)}
    C2 = dict(C1)
    for r in F.itertuples():
        k = (r.n, PL.quarter(r.date))
        C1[k] += 1
        if any(0 < (d - r.date).days <= 42 for d in fu.get(r.pat, [])):
            C2[k] += 1
    return C1, C2


ROUTES = [
    # the cracker: the call landed, the hygiene battery run, the export reconciled to the statements
    ("cracker", "export and statements; every recovered record out; network on the day from the pharmacy list; "
                "each patient's earliest first consultation", dict(statements=True, net="net_day", drop="recovered")),
    ("K1", "export and statements; recovered out; the portal's network label",
     dict(statements=True, net="net_label", drop="recovered")),
    ("K2", "export and statements; recoveries ignored; each patient's earliest",
     dict(statements=True, net="net_day", drop="none")),
    ("K3", "export and statements; recoveries ignored; each patient's first recorded",
     dict(statements=True, net="net_day", drop="none", keep="recorded")),
    ("K4", "the export alone; network on the day; each patient's earliest",
     dict(statements=False, net="net_day", drop="none")),
    ("K5", "the export alone; the portal's network label; each patient's earliest",
     dict(statements=False, net="net_label", drop="none")),
    ("K6", "the export alone; the portal's network label; every first consultation record",
     dict(statements=False, net="net_label", drop="none", keep="all")),
    ("K7", "the golden's handling on the export alone (no late records)",
     dict(statements=False, net="net_day", drop="second")),
    ("K8", "the golden's handling with the portal's network label",
     dict(statements=True, net="net_label", drop="second")),
]


def run(target=K.TARGET):
    gold1, gold2 = A.pilot_figures(target)
    cache = {}
    out = []
    for name, desc, kw in ROUTES:
        st = kw.pop("statements")
        if st not in cache:
            cache[st] = records(target, statements=st)
        c1, c2 = count(cache[st], **kw)
        kw["statements"] = st
        h1 = [k for k in c1 if c1[k] == gold1[k]]
        h2 = [k for k in c2 if c2[k] == gold2[k]]
        out.append((name, desc, c1, c2, h1, h2))
    return gold1, gold2, out


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else K.TARGET
    gold1, gold2, out = run(target)
    fmt = lambda c: " ".join("%s%d %3d" % (n[0], q, c[(n, q)]) for n in ("KRT", "LTH") for q in (1, 2, 3, 4))
    print("golden first consultations  %s" % fmt(gold1))
    print("golden followed up          %s" % fmt(gold2))
    for name, desc, c1, c2, h1, h2 in out:
        print("%-8s keeps %2d of 16  (%s)" % (name, len(h1) + len(h2), desc))
        print("         first  %s" % fmt(c1))
        print("         follow %s" % fmt(c2))
    crack = out[0]
    print("CRACKER keeps %d of 16 ask figures" % (len(crack[4]) + len(crack[5])))
    return 0 if not (crack[4] or crack[5]) else 1


if __name__ == "__main__":
    sys.exit(main())
