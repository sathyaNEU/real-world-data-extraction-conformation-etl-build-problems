"""The ask sheet's measurement on the cut pack: the cracker (lands the call, runs the hygiene battery, executes every filed
rule) and the mirror (credits every breaker ticket to the feeder's backbone), each scored figure by figure on the 38/7/55
weights, with every path each ask offers a response that does not meet its device.

    python3 task303/generator/pair.py <target dir>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import figs as FG
import solve as S

REC, IF, ASK = 38.0, 7.0, 55.0


def hits(path, gold, key, unit):
    return sum(1 for f in S.CAND if FG.rnd(path[f][key], unit) == FG.rnd(gold[f][key], unit))


def main(target):
    pk = S.Pack(target)
    g, d = pk.call(True), pk.call(False)
    win = max(S.CAND, key=lambda f: g[f])
    mirror_pick = max(S.CAND, key=lambda f: d[f])
    call_n = 8          # six candidates' figures, the pick and its value
    mirror_call = sum(FG.rnd(d[f], 100) == FG.rnd(g[f], 100) for f in S.CAND) + (mirror_pick == win) \
        + (FG.rnd(d[mirror_pick] * S.INCENTIVE, 1000) == FG.rnd(g[win] * S.INCENTIVE, 1000))
    A, B = pk.storm(), pk.taps()
    pa = {"the outage system's restoration (the natural read)": pk.storm("naive"),
          "the crew's Restored time, every status read as Eastern local time (the careful read)": pk.storm("crew"),
          "every crew device read as Eastern standard time": pk.storm("all_est"),
          "the contract crews' statuses an hour later all year": pk.storm("pbl_all_year"),
          "the crew's Released time": pk.storm("released"),
          "the crew's time only where a restoration stamp repeats": pk.storm("repeated"),
          "the day taken from the UTC stamp": pk.storm("utc_day")}
    pb = {"hours and minutes read right, OUT_DT read as the day the interruption began (the careful read)":
              pk.taps("golden", "naive"),
          "a decimal DUR_MIN read as decimal hours, OUT_DT as the start (the natural read)": pk.taps("hours", "naive"),
          "decimal hours with the closing date handled": pk.taps("hours", "golden"),
          "a decimal DUR_MIN read as minutes (under five dropped as momentary)": pk.taps("minutes", "naive"),
          "the decimal rows dropped": pk.taps("drop", "naive"),
          "every legacy ticket dated the day it closed": pk.taps("golden", "all")}
    print("ask A, storm days 2023 to 2025 (12 figures):")
    ka = 0
    for k, v in pa.items():
        h = hits(v, A, "cmi", 1000) + hits(v, A, "per", 0.1)
        ka = max(ka, h)
        print("   %-72s %d of 12" % (k, h))
    print("ask B, taps 2019 to 2025 (12 figures):")
    kb = 0
    for k, v in pb.items():
        h = hits(v, B, "year", 10) + hits(v, B, "per", 0.1)
        kb = max(kb, h)
        print("   %-72s %d of 12" % (k, h))
    keep = ka + kb
    lc = ls = keep / 24.0
    cracker = REC + IF + ASK * lc
    r = REC * mirror_call / call_n
    mirror = r + IF + ASK * ls
    pair = (cracker + mirror) / 2
    print("cracker: the call (8 of 8) and the best path on each ask, %d of 24 ask figures: %.1f" % (keep, cracker))
    print("mirror: every breaker ticket credited (%d of 8 call criteria: %s at %s) and the same ask paths: %.1f"
          % (mirror_call, mirror_pick, "{:,}".format(FG.rnd(d[mirror_pick], 100)), mirror))
    print("Pair ceiling: %.1f" % pair)
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * ls))
    print("(the asks read rows the call never reads, the storm days and the tap fuses, so both responses take the same "
          "ask paths; separation is asserted in checks.py)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
