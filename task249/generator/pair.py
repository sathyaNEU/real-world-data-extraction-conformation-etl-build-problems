"""The ask layer measured on the cut pack: each path a response could take through the two asks, the figures it keeps
against the golden, the cracker (on the call, every filed rule executed, the hygiene battery run: the failures read
by their own booking with the power cut added from the report, the link losses read as pairs inside the sitting)
and the mirror (off the call, the first reading of each log), and the pair ceiling.
python3 pair.py [target]"""
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as S

TASK = os.path.dirname(HERE)


def ask_a_paths(target, D):
    ev = pd.read_csv(os.path.join(target, S.FILES["events"]), dtype=str, keep_default_na=False)
    ev["t"] = pd.to_datetime(ev["event_utc"])
    form_of = dict(zip(D["s"]["booking_ref"], D["s"]["form"]))
    win_of = dict(zip(D["s"]["booking_ref"], D["s"]["window"]))

    def count(bk):
        out = {f: 0 for f in S.F27}
        for b in bk:
            if win_of.get(b, "").startswith("2027") and form_of.get(b) in out:
                out[form_of[b]] += 1
        return out
    gold, golden_set = S.ask_a(target, D=D)
    # the failures attributed by time: the latest sitting started on that workstation that day before the failure
    st = ev[ev["event"] == "SESSION_START"]
    by_time = set()
    for r in ev[ev["event"] == "WS_FAIL"].itertuples():
        c = st[(st["centre_code"] == r.centre_code) & (st["workstation"] == r.workstation) & (st["t"] <= r.t)
               & (st["t"].dt.date == r.t.date())]
        if len(c):
            by_time.add(c.sort_values("t").iloc[-1]["booking_ref"])
    power = golden_set - by_time
    assert by_time | power == golden_set
    fail_ref = set(ev[ev["event"] == "WS_FAIL"]["booking_ref"])
    resumes = set(ev[ev["event"] == "SESSION_RESUME"]["booking_ref"])
    spares = set(ev[(ev["event"] == "SESSION_RESUME") & ev["workstation"].str.startswith("SP")]["booking_ref"])
    return {
        "golden": gold,
        "fail_refs": count(fail_ref),
        "fail_refs_and_power": count(fail_ref | power),
        "resumes": count(resumes),
        "resumes_and_power": count(resumes | power),
        "spare_resumes_and_power": count(spares | power),
        "fail_by_time_no_power": count(by_time),
    }


def ask_b_paths(target, D):
    return {"golden": S.ask_b(target, D=D), "lost_refs": S.ask_b(target, D=D, path="lost_refs"),
            "lost_within": S.ask_b(target, D=D, path="lost_within"), "pairs_only": S.ask_b(target, D=D, path="pairs_only")}


def keep(path, golden):
    return sum(path[k] == golden[k] for k in golden)


def main(target):
    D = S.load(target)
    A = ask_a_paths(target, D)
    B = ask_b_paths(target, D)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    assert A["golden"] == fig["asks"]["interrupted"] and B["golden"] == fig["asks"]["offline"]
    print("Ask A paths (forms kept of 10):")
    for k, v in A.items():
        print("  %-26s %2d" % (k, keep(v, A["golden"])))
    print("Ask B paths (forms kept of 10):")
    for k, v in B.items():
        print("  %-26s %2d" % (k, keep(v, B["golden"])))
    n = 20
    kc = keep(A["fail_refs_and_power"], A["golden"]) + keep(B["pairs_only"], B["golden"])
    km = keep(A["fail_refs"], A["golden"]) + keep(B["lost_refs"], B["golden"])
    c = 38 + 7 + 55 * kc / n
    s = 5 + 7 + 55 * km / n
    print("cracker keeps %d of %d ask figures; mirror keeps %d" % (kc, n, km))
    print("pair ceiling %.1f ((%.1f + %.1f) / 2); mirror leakage %.1f per cent of ask weight" % ((c + s) / 2, c, s, 100 * km / n))
    return dict(A=A, B=B, kc=kc, km=km)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))
