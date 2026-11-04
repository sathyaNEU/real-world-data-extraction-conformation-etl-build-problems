"""The pair ceiling on the cut pack, from the same code the golden runs, graded as the rubric grades: the periods and the
day count exact, the shortfall within its 100 acre-foot band, each daily mean within its 2 cfs band (27 and 28 July on
met only), the spring volumes to the nearest 100 acre-feet and the peak's flow and time exact. The cracker lands the
call: it sets the 2026 measurements against Rating 7, applies the post-storm shift from the storm's peak and files the
periods, the count, the shortfall and the cause; above the register's table (4.00 ft) it extends the table's own law, so
the freshet days, the spring volumes and the peak come out on that extension. The mirror stops at Rating 7 throughout and
extends the table the same way. The full includer also takes the 2023 memo's high-water segment. Weights 38 / 7 / 55:
the periods 12, the day count 4, the shortfall 6, the cause 6, the daily record 10; instructions 7; May volume 20, June
volume 20, the spring peak 15."""
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B   # noqa: E402
import golden as G   # noqa: E402

W_PER, W_CNT, W_SHORT, W_CAUSE, W_DAILY, W_INSTR, W_MAY, W_JUN, W_PEAK = 12.0, 4.0, 6.0, 6.0, 10.0, 7.0, 20.0, 20.0, 15.0


def score(gold, resp, cause, minimum):
    """The rubric's grading: periods and count exact, the shortfall within its band, each daily mean within its band
    (27 and 28 July on met only), the spring volumes to the nearest 100 acre-feet, the peak's flow and time exact."""
    main = (W_PER if resp["periods"] == gold["periods"] else 0) + (W_CNT if len(resp["dev"]) == len(gold["dev"]) else 0) + \
        (W_SHORT if abs(G.r100(resp["shortfall"]) - G.r100(gold["shortfall"])) <= G.SHORT_BAND_AF else 0) + \
        (W_CAUSE if cause else 0)
    may = W_MAY if G.r100(resp["vol"][5]) == G.r100(gold["vol"][5]) else 0
    jun = W_JUN if G.r100(resp["vol"][6]) == G.r100(gold["vol"][6]) else 0
    rec = [k for k in gold["daily"] if k.month >= 7]
    met_only = (dt.date(2026, 7, 27), dt.date(2026, 7, 28))
    hit = sum(1 for k in rec if ((resp["daily"][k] >= minimum(k)) == (gold["daily"][k] >= minimum(k)) if k in met_only
                                 else abs(G.r0(resp["daily"][k]) - G.r0(gold["daily"][k])) <= G.BAND_CFS))
    main += W_DAILY * hit / len(rec)
    pk = W_PEAK if (G.r0(resp["spring_peak"][1]) == G.r0(gold["spring_peak"][1]) and
                    resp["spring_peak"][0] == gold["spring_peak"][0]) else 0
    return dict(total=main + W_INSTR + may + jun + pk, main=main, ask=may + jun + pk, may=may > 0, jun=jun > 0,
                peak=pk > 0, hit=hit, n=len(rec))


def main(target=None, quiet=False):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    d = B.load(target)
    gold = G.compute(d)
    cracker = G.compute(d, hiwater="power")
    mirror = G.compute(d, route="rating", hiwater="power")
    full = G.compute(d)
    c, m, f = (score(gold, r, cause, d["minimum"]) for r, cause in ((cracker, True), (mirror, False), (full, True)))
    ceiling = (c["total"] + m["total"]) / 2
    if not quiet:
        for name, s in (("cracker", c), ("mirror", m), ("full includer", f)):
            print("%-13s %5.1f  (main %.1f, asks %.1f; May %s, June %s, peak %s; daily means %d of %d)" % (
                name, s["total"], s["main"], s["ask"], "kept" if s["may"] else "missed", "kept" if s["jun"] else "missed",
                "kept" if s["peak"] else "missed", s["hit"], s["n"]))
        print("pair ceiling %.1f; mirror leakage %.1f per cent of ask weight; with the full includer on the call %.1f" % (
            ceiling, 100.0 * m["ask"] / (W_MAY + W_JUN + W_PEAK), (f["total"] + m["total"]) / 2))
    return ceiling


if __name__ == "__main__":
    sys.exit(0 if main() <= 60.0 else 1)
