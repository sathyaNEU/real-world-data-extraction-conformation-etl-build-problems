"""The ask sheet's measurement on the cut pack: the cracker (lands the call, runs the hygiene battery, executes every
filed rule it points at) and the mirror (the strongest response off the call, stopping at the most attractive wrong
rung of each ask), each ask figure scored against the golden at half a unit of its rounding.

    python3 task273/generator/cracker.py [target]

Ask A, the cracker: the synthetic checks running in January taken off every hour (the YAML's defaults applied, the
checks created after January left on), the old path up to each rename and the new path from it, the employers on 1
November from the CRM's accounts, on 1 January the accounts whose subscription started by then with their 2026 plan
changes undone, plus the accounts cancelled during the year that are no longer in the CRM. It reads the CRM's
subscription start as the start of the account's custom, so the accounts that were cancelled and signed again in
2026 drop out of 1 January.
Ask B, the cracker: legacy cents to dollars, void credits out, every credit dated by its incident (Eastern), the old
route names mapped through the changelog, reversals netted, and each credit found in both billing systems kept once,
as the new system (the system of record) holds it.
The mirror: Ask A on the current route only, the synthetic checks left in, both days' employers on their current
plans; Ask B with each credit found in both systems counted in both."""
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN   # noqa: E402
import common as K      # noqa: E402
import pack as P        # noqa: E402

JAN1 = dt.date(2026, 1, 1)


def growth_cracker(target, ep, mirror=False):
    emp = P.employers(target)
    ev = P.subscription_events(target)
    byemp = {}
    for e in sorted(ev, key=lambda x: (x["effective_date"], x["event_id"])):
        byemp.setdefault(e["employer_id"], []).append(e)
    jan = {}
    for eid, r in emp.items():
        if dt.date.fromisoformat(r["subscription_start"]) > JAN1:
            continue
        plan = r["plan"]
        if not mirror:
            for e in reversed(byemp.get(eid, [])):
                if e["event"] == "plan_change":
                    plan = e["plan_before"]
        jan[eid] = plan
    if not mirror:
        for eid, lst in byemp.items():
            if eid in emp:
                continue
            kinds = [e["event"] for e in lst]
            if "cancellation" not in kinds or "new_subscription" in kinds[:kinds.index("cancellation")]:
                continue
            k = kinds.index("cancellation")
            plan = lst[k]["plan_before"]
            for e in reversed(lst[:k]):
                if e["event"] == "plan_change":
                    plan = e["plan_before"]
            jan[eid] = plan
    out = {}
    for c in K.CODES:
        pl = set(ep[c]["plans"])
        out[c] = (sum(1 for r in emp.values() if r["plan"] in pl), sum(1 for p in jan.values() if p in pl))
    return out


def ask_a_route(target, who):
    ep, _ = P.register(target)
    if who == "cracker":
        peaks = AN.busiest(AN.january_series(target, ep, "golden"), AN.synthetic_per_hour(target))
        g = growth_cracker(target, ep)
    else:
        peaks = AN.busiest(AN.january_series(target, ep, "current"))
        g = growth_cracker(target, ep, mirror=True)
    return {c: AN.half_up(peaks[c][0] * g[c][0] / g[c][1]) for c in K.CODES}


def ask_b_route(target, who):
    rc = AN.route_codes(target)
    inc = P.incidents(target)
    leg = P.legacy_credits(target)
    new = P.new_credits(target)

    def code_in_window(key):
        i = inc[key]
        d = (i["start"] + AN.EST).date()
        return rc.get(i["comp"]) if K.WINDOW_FROM <= d <= K.WINDOW_TO else None

    in_new = {(x["account"], x["incident"]) for x in new if x["type"] == "credit"}
    cents = {c: 0 for c in K.CODES}
    for x in leg:
        if x["status"] != "issued":
            continue
        if who == "cracker" and (x["account"], x["incident"]) in in_new:
            continue                       # the copy the new system holds is kept
        c = code_in_window(x["incident"])
        if c:
            cents[c] += int(x["amount"])
    for x in new:
        c = code_in_window(x["incident"])
        if c:
            cents[c] += int(round(float(x["amount"]) * 100))
    return {c: AN.half_up(v / 100.0) for c, v in cents.items()}


def score(target):
    a = {c: v["forecast"] for c, v in AN.ask_a(target).items()}
    b0, _ = AN.ask_b(target)
    b = {c: v["dollars"] for c, v in b0.items()}
    out = {}
    for who in ("cracker", "mirror"):
        ra, rb = ask_a_route(target, who), ask_b_route(target, who)
        out[who] = dict(a_hits=[c for c in K.CODES if abs(ra[c] - a[c]) <= 0.5],
                        b_hits=[c for c in K.CODES if abs(rb[c] - b[c]) <= 0.5],
                        a_gap=(min(abs(ra[c] - a[c]) for c in K.CODES), max(abs(ra[c] - a[c]) for c in K.CODES)),
                        b_gap=(min(abs(rb[c] - b[c]) for c in K.CODES), max(abs(rb[c] - b[c]) for c in K.CODES)))
    n = 2 * len(K.CODES)
    lc = (len(out["cracker"]["a_hits"]) + len(out["cracker"]["b_hits"])) / n
    ls = (len(out["mirror"]["a_hits"]) + len(out["mirror"]["b_hits"])) / n
    out["pair_ceiling"] = ((38 + 7 + 55 * lc) + (5 + 7 + 55 * ls)) / 2.0
    out["mirror_leakage_pct"] = 100.0 * ls
    return out


if __name__ == "__main__":
    T = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    s = score(T)
    for who in ("cracker", "mirror"):
        x = s[who]
        print("%-8s Ask A hits %d of 24 (gap %d to %d requests an hour); Ask B hits %d of 24 (gap %d to %d dollars)"
              % (who, len(x["a_hits"]), x["a_gap"][0], x["a_gap"][1], len(x["b_hits"]), x["b_gap"][0], x["b_gap"][1]))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % (s["pair_ceiling"],
                                                                                s["mirror_leakage_pct"]))
