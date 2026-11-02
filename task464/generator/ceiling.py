"""task464 architecture 12: the pair ceiling, measured on the cut pack.

Rubric weights as built: 38 on the main side (the call 10, the 2027 figure 10, the pilot's gain among the restarted 6,
the pilot's loss among the rest of the board 6, the mailbox groups the loss came through 6), 7 on
instruction-following (every route keeps it), 55 on the asks (each send's restarts by people and how many of them
clicked a sponsored job on the send's date or in the 27 days after it: 12 exact figures, equal weight). A figure is kept when it equals the golden at
the prompt's rounding.

Routes, each a complete careful pipeline:
  cracker        lands the call, reads every field by its plain meaning (route, link campaign, account, device, both
                 clocks), executes every filed rule, runs the battery (the warehouse reload's repeated rows dropped,
                 the app channels rejoined, anti-joins, duplicate and re-sent rows, clocks converted). It counts each
                 send's email-link restarts as the restart log records them and a restarter's clicks by account,
                 dropping the clicks with a blank account as unattributable.
  careful2       the same call; the over-cleaning handlings: a restart in the first hour after the send treated as a
                 machine's, and logged-out app clicks tied only through the restart log's app devices.
  mirror         the best response off the call: the holdout uplift carried (keep the series), the asks as the
                 cracker reads them.
  full_includer  the call, every gateway burst removed, every logged-out device tied to its jobseeker. Must reproduce
                 figures.json, or exit 1.

    python3 generator/ceiling.py [target_dir]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import answers as A  # noqa: E402
import world as W   # noqa: E402

W_MAIN, W_INSTR, W_ASK = 38.0, 7.0, 55.0


def main_side(route, tgt, fig):
    wh = A.Warehouse(tgt)
    U = A.uplift(wh)
    if route == "mirror":
        net27 = U * W.SENDS_2027 / 6.0
        call = "keep" if net27 > 0 else "drop"
        Dt, groups = 0.0, []
    else:
        per, aff, ctl = A.damage(wh, "event")
        Dt = sum(sum(v) for v in per.values())
        net27 = (U - Dt) * W.SENDS_2027 / 6.0
        call = "keep" if net27 > 0 else "drop"
        groups = aff
    pts = 0.0
    pts += 10.0 if call == fig["call"] else 0.0
    pts += 10.0 if A.r_to(net27, 100000) == A.r_to(fig["series_2027_clicks_exact"], 100000) else 0.0
    pts += 6.0 if A.r_to(U, 50000) == A.r_to(fig["pilot_uplift_exact"], 50000) else 0.0
    pts += 6.0 if A.r_to(Dt, 50000) == A.r_to(fig["pilot_loss_exact"], 50000) else 0.0
    pts += 6.0 if sorted(groups) == sorted(fig["affected_groups"]) else 0.0
    return pts, call, round(net27)


def ask_figures(route, tgt):
    if route in ("cracker", "mirror"):
        per = A.restarts_by_send(tgt, "plain")
        a2 = A.clicked_within(tgt, per, stitch=False)
    elif route == "careful2":
        per = A.restarts_by_send(tgt, "fast", 3600)
        a2 = clicked_restartlog_only(tgt, per)
    else:
        per = A.restarts_by_send(tgt, "golden")
        a2 = A.clicked_within(tgt, per, stitch=True)
    return [len(s) for s in per], a2


def clicked_restartlog_only(tgt, per):
    """Logged-out app clicks tied only where the restart log carries the device (the partial stitch)."""
    import csv
    import datetime as dt
    from collections import defaultdict
    dev2acct = defaultdict(set)
    for r in A.restart_rows(tgt):
        if r["app_install_id"]:
            dev2acct[r["app_install_id"]].add(r["account_id"])
    days_by_acct = defaultdict(set)
    with open(os.path.join(tgt, "restarted_jobseekers_sponsored_clicks.csv"), newline="") as f:
        for r in csv.DictReader(f):
            acct = r["account_id"]
            if not acct and r["app_install_id"] and len(dev2acct.get(r["app_install_id"], ())) == 1:
                acct = next(iter(dev2acct[r["app_install_id"]]))
            if acct:
                days_by_acct[acct].add(dt.date.fromisoformat(r["clicked_at_uk"][:10]))
    out = []
    for k in range(6):
        lo, hi = A.SENDS[k], A.SENDS[k] + dt.timedelta(days=W.WINDOW - 1)
        out.append(sum(1 for a in per[k] if any(lo <= d <= hi for d in days_by_acct.get(a, ()))))
    return out


def score(route, tgt, fig):
    m, call, net27 = main_side(route, tgt, fig)
    a1, a2 = ask_figures(route, tgt)
    kept = sum(1 for x, g in zip(a1, fig["restarted_by_people"]) if x == g) + \
        sum(1 for x, g in zip(a2, fig["clicked_within_28_days"]) if x == g)
    ask = W_ASK * kept / 12.0
    return {"route": route, "main": m, "call": call, "net27": net27, "asks_kept": kept, "ask_points": ask,
            "total": round(m + W_INSTR + ask, 1), "a1": a1, "a2": a2}


def main(tgt=None):
    base = os.path.dirname(HERE)
    tgt = tgt or os.path.join(base, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    rows = {r: score(r, tgt, fig) for r in ("cracker", "careful2", "mirror", "full_includer")}
    for r, v in rows.items():
        print("%-14s main %5.1f  call %-4s  2027 %9d  asks kept %2d of 12  total %5.1f" %
              (r, v["main"], v["call"], v["net27"], v["asks_kept"], v["total"]))
    fi = rows["full_includer"]
    ok = (fi["a1"] == fig["restarted_by_people"] and fi["a2"] == fig["clicked_within_28_days"]
          and fi["call"] == fig["call"])
    pair = (rows["cracker"]["total"] + rows["mirror"]["total"]) / 2.0
    leak = 100.0 * rows["mirror"]["ask_points"] / W_ASK
    print("pair ceiling (cracker, mirror): %.1f   mirror leakage: %.1f per cent of ask weight" % (pair, leak))
    print("cracker asks kept: %d of 12 (every figure missed: %s)" % (rows["cracker"]["asks_kept"],
                                                                   rows["cracker"]["asks_kept"] == 0))
    json.dump({"pair": pair, "mirror_leakage": leak, "rows": rows},
              open(os.path.join(HERE, "ceiling.json"), "w"), indent=2)
    if not ok:
        print("FAIL: the full includer does not reproduce figures.json")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
