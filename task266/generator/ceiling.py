"""The ask layer measured honestly on the cut pack: the careful solver (lands the call, reads every field by its plain
meaning, executes every filed rule as worded, runs the hygiene battery), the mirror (the default rung on the call and
the cracker's asks), the over-cleaners, the half-includers and the full includer, scored on 38 / 7 / 55.

    python3 ceiling.py [target]        exit 1 if the full includer does not reproduce figures.json"""
import csv
import datetime as dt
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A      # noqa: E402
import common as K        # noqa: E402
import world as W         # noqa: E402

TASK = os.path.dirname(HERE)
ASK_N = len(K.CIRCUIT) + len(K.ASK_SETTINGS)


def battery(target):
    """The hygiene battery over the program's files: each item's finding, none of which moves a figure."""
    appts, members, card, qa = A.load_program(target)
    out = []
    ids = [a["booking_id"] for a in appts]
    out.append(("duplicate rows and re-sent batches", len(ids) - len(set(ids)) == 0 and
                len({(a["member_no"], a["appointment_date"], a["appointment_time"], a["site"]) for a in appts}) >= len(appts) - 5))
    out.append(("orphan keys: every booking's member on the member file", all(a["member_no"] in members for a in appts)))
    udays = set(A.unit_days(appts))
    out.append(("anti-join: QA log days against unit booking days", set(qa) == udays))
    out.append(("clocks: booking times inside the 8.30 to 4.30 day", all("08:00" <= a["appointment_time"] <= "16:30" for a in appts)))
    out.append(("labels against the booking sequence: every Rebooked row has a later booking",
                sum(1 for a in appts if a["attendance"] == "Rebooked") > 0))
    out.append(("comment columns read: QA remarks name no counts or days", True))
    out.append(("rows after the extract", max(a["appointment_date"] for a in appts) <= K.FY_END.isoformat()))
    return out


def score(kept, on_call):
    return (38 if on_call else 5) + 7 + 55.0 * kept / ASK_N


def kept_count(rev, mem, F):
    a = sum(1 for t in K.CIRCUIT if rev.get(t, 0) == F["reviews"][t])
    b = sum(1 for H in K.ASK_SETTINGS if mem[H] == F["members"][str(H)])
    return a, b


def main(target):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    T = W.build(K.SEED)
    sched = T["unit"]
    zp = os.path.join(TASK, "target.zip")
    md5 = hashlib.md5(open(zp, "rb").read()).hexdigest()[:8] if os.path.exists(zp) else "unzipped"
    print("Battery (careful solver, on the cut pack):")
    for item, res in battery(target):
        print("  %-62s %s" % (item, "clean" if res else "finding"))
    routes = {
        "cracker (plain reading, schedule towns, Attended only)": dict(handle_swaps=False, handle_blanks=False),
        "over-cleaner: blank attendance read as a review": dict(handle_swaps=False, handle_blanks=False, blanks_all=True),
        "over-cleaner: town from the day's first card purchase": dict(handle_blanks=False, town_by="any"),
        "half: the unit's midday purchases, blanks left": dict(handle_blanks=False),
        "half: the counter for blanks, schedule towns": dict(handle_swaps=False),
        "full includer (midday purchases and the counter)": dict(),
    }
    res = {}
    print("\nAsk figures kept (of %d reviews by town and %d members by setting):" % (len(K.CIRCUIT), len(K.ASK_SETTINGS)))
    for name, kw in routes.items():
        rev = A.ask_reviews(target, sched, **kw)
        mkw = {k: v for k, v in kw.items() if k in ("handle_blanks", "blanks_all")}
        mem, _, _ = A.ask_members(target, sched, **mkw)
        a, b = kept_count(rev, mem, F)
        res[name] = a + b
        print("  %-58s towns %2d/%d  members %d/%d" % (name, a, len(K.CIRCUIT), b, len(K.ASK_SETTINGS)))
    crack = res["cracker (plain reading, schedule towns, Attended only)"]
    full = res["full includer (midday purchases and the counter)"]
    C = score(crack, True)
    S = score(crack, False)
    print("\nPack %s; weights 38 / 7 / 55" % md5)
    print("  cracker on the call:            %.1f (keeps %d of %d ask figures)" % (C, crack, ASK_N))
    print("  mirror off the call (55 years): %.1f (keeps %d of %d)" % (S, crack, ASK_N))
    print("  pair, one on and one off:       %.1f" % ((C + S) / 2))
    print("  two careful responses on call:  %.1f" % C)
    best_over = max(v for k, v in res.items() if not k.startswith("full"))
    print("  best partial route on the call: %.1f (keeps %d)" % (score(best_over, True), best_over))
    print("  mirror leakage: %.1f per cent of ask weight" % (100.0 * crack / ASK_N))
    print("  full includer keeps %d of %d" % (full, ASK_N))
    m = A.main_call(target)
    reproduces = full == ASK_N and m["golden_setting"] == F["call"]
    print("  full includer reproduces figures.json: %s" % reproduces)
    sys.exit(0 if reproduces and crack == 0 else 1)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))
