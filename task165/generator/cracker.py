"""task165 cracker and mirror, run on the cut pack: the pair ceiling and the mirror's leakage.

The cracker lands the call (the earlier moves' gain read at each new street's own Priority 2 salt), runs the hygiene
battery (keys, duplicates, unmatched joins, units and clocks converted) and executes every filed rule on the fields it
holds: each dome's stock from the survey's date brought forward by every weighing at its own scale house and the latest
dispatch issue; the arterial salt as the platform's rows by the route code's yard, the contractor's returns added and
the season read on local dates, to the nearest 50 t. The mirror stops at the default path (the Priority 1 collectors' rate less the new
streets' own Priority 2 salt) and is as careful on the asks. Each response is scored on Part 0's weights: the call and
its components 38, the instructions 7, the asks 55 shared over every ask figure and the chart's parts.

    python3 cracker.py [target]"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C  # noqa: E402
import common as K  # noqa: E402

TARGET = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
W_CALL, W_IF, W_ASK = 38.0, 7.0, 55.0
CHART_PARTS = 2          # every yard and winter shown and labelled; the title
CHART_CONTENT = 1        # the chart carries Ask B's figures


def r1(v):
    return round(v + 1e-9, 1)


def ask_points(stock, room, art, gold):
    gs, gr, ga = gold
    ka = sum(1 for y in C.YARDS if r1(stock[y]) == r1(gs[y])) + sum(1 for y in C.YARDS if r1(room[y]) == r1(gr[y]))
    kb = sum(1 for k in ga if C.r50(art[k]) == C.r50(ga[k]))
    content = 1 if kb == len(ga) else 0
    n = 8 + 12 + CHART_CONTENT + CHART_PARTS
    keep = ka + kb + content + CHART_PARTS
    return keep / n * W_ASK, (ka, kb, content), keep, n


def main(target=TARGET, quiet=False):
    P = C.Pack(target)
    gold_call = round(C.golden(P) / 100.0) * 100
    gs, gr = C.ask_a(target)
    ga = C.arterial_salt(target)
    gold = (gs, gr, ga)
    routes = {
        "cracker": (round(C.golden(P) / 100.0) * 100, C.ask_a(target, "day_after"), C.arterial_salt(target, "rows")),
        "mirror": (round(C.r1_default(P) / 100.0) * 100, C.ask_a(target, "day_after"), C.arterial_salt(target, "rows")),
    }
    out = {}
    lines = []
    for who, (call, (st, rm), art) in routes.items():
        m = W_CALL if call == gold_call else 5.0
        pts, (ka, kb, cc), keep, n = ask_points(st, rm, art, gold)
        out[who] = (m + W_IF + pts, pts)
        lines.append("%-8s call %s (%s) %4.1f; instructions %.0f; asks %5.1f of %.0f (A %d/8, B %d/12, chart content %d, "
                     "parts %d) -> %5.1f" % (who, "landed" if call == gold_call else "missed", int(call), m, W_IF, pts,
                                            W_ASK, ka, kb, cc, CHART_PARTS, m + W_IF + pts))
    pair = (out["cracker"][0] + out["mirror"][0]) / 2
    leak = out["mirror"][1] / W_ASK * 100
    # the most obvious device cracked: Ridge's weighings for Lakeshore read off the remarks (A2), the contractor
    # added (B2, already in), the capture window converted (A1), and both of A's
    variants = {
        "A2 cracked (remarks read)": (C.ask_a(target, "day_after_dome"), C.arterial_salt(target, "rows")),
        "A1 cracked (capture end in local time)": (C.ask_a(target, "sheets"), C.arterial_salt(target, "rows")),
        "B1 cracked (run totals once)": (C.ask_a(target, "day_after"), C.arterial_salt(target, "runs_once")),
        "B1b cracked (brine netted)": (C.ask_a(target, "day_after"), C.arterial_salt(target, "net_brine")),
        "two devices, A1 and A2": (C.ask_a(target), C.arterial_salt(target, "rows")),
        "two devices, B1 and B1b": (C.ask_a(target, "day_after"), C.arterial_salt(target)),
    }
    worst = 0.0
    for name, ((st, rm), art) in variants.items():
        pts, parts, keep, n = ask_points(st, rm, art, gold)
        tot = W_CALL + W_IF + pts
        pr = (tot + out["mirror"][0]) / 2
        if not name.startswith("two devices"):
            worst = max(worst, pr)
        lines.append("cracker with %-40s asks %5.1f (A %d/8, B %d/12) -> %5.1f; pair %5.1f" % (
            name, pts, parts[0], parts[1], tot, pr))
    lines.append("Pair ceiling: %.1f" % pair)
    lines.append("Mirror leakage: %.1f per cent of ask weight" % leak)
    lines.append("Pair with the most obvious device cracked: %.1f" % worst)
    lines.append("Both top responses on the call, no device cracked: %.1f" % (out["cracker"][0]))
    if not quiet:
        print("\n".join(lines))
    return {"pair": pair, "leak": leak, "worst": worst, "cracker": out["cracker"][0], "mirror": out["mirror"][0],
            "lines": lines}


if __name__ == "__main__":
    main()
