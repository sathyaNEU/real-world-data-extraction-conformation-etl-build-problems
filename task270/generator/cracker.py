"""The cracker's path on the cut pack (supplemental-stumping 1.1): a response that lands the call (each rotation spot
over the places the reference day's bookings aired), runs the hygiene battery (key uniqueness, exact and near-exact
duplicate rows, unmatched joins, fan-out) and executes every filed rule it points at. On Ask F it reads the
at-least-once reach off the same replay; on Ask R it executes the extract notes' rule (each person once, at the date
of the first first-donation booking they made, aged 18 to 34 that day, whatever the outcome), with a person read as a
donor number: id_dador is unique per registration, no booking repeats, and every join closes, so the battery drops
nothing; Ask X takes that response onto the call's reach. Every ask figure is scored against figures.json: a hit is
within half a unit of the stated rounding. The mirror (the response on the in-window rotation places, schedule B)
runs the asks the same way; its Ask F and X figures for schedule B also move. Prints the sheet and the pair
ceiling."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN    # noqa: E402
import asks as AS        # noqa: E402
import common as K       # noqa: E402


def score(task, route_main):
    target = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    P = AN.Pack(target)
    a = AS.all_asks(target, P, route_main=route_main, route_resp="donor")
    g = fig["asks"]
    rows = []
    r = a["response"]
    rows.append(("R", "baseline average", abs(r["avg"] - g["R"]["baseline_weekly_average"]) < 0.05))
    for k, (x, y) in enumerate(zip(r["above"], g["R"]["campaign_weeks_above_baseline"])):
        rows.append(("R", "week %d above" % (k + 1), abs(x - y) < 0.05))
    rows.append(("R", "total above", abs(r["extra"] - g["R"]["campaign_weeks_total_above"]) < 0.05))
    rows.append(("R", "response", abs(r["per_thousand"] - g["R"]["response_per_thousand_reached3"]) < 0.005))
    for s in K.SCHED:
        rows.append(("X", "bookings %s" % s, int(K.r(a["bookings"][s] / 10.0) * 10) ==
                     g["X"]["expected_first_donation_bookings"][s]))
    return rows


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
    crk = score(task, "golden")
    mir = score(task, "asrun")
    for name, rows in (("cracker", crk), ("mirror", mir)):
        for ask in ("R", "X"):
            r = [x for x in rows if x[0] == ask]
            print("%s Ask %s: keeps %d of %d%s" % (name, ask, sum(x[2] for x in r), len(r),
                                                   "" if not any(x[2] for x in r) else
                                                   " (" + ", ".join(x[1] for x in r if x[2]) + ")"))
    n = len(crk)
    lc, lm = sum(x[2] for x in crk) / n, sum(x[2] for x in mir) / n
    pair = ((38 + 7 + 55 * lc) + (5 + 7 + 55 * lm)) / 2
    print("cracker %d of %d ask figures; mirror %d of %d; mirror leakage %.1f per cent; pair ceiling %.1f" % (
        sum(x[2] for x in crk), n, sum(x[2] for x in mir), n, 100 * lm, pair))
    sys.exit(0 if pair <= 40 else 1)
