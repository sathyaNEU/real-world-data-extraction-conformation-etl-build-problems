"""The ask sheet's measurement on the cut pack: the cracker (lands the call, runs the battery, executes every filed rule)
and the mirror (builds Hallam Down at the meter), each scored figure by figure on the 38/7/55 weights, with every path
each ask offers a response that does not meet its device.

    python3 task301/generator/pair.py <target dir>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P
import solve as SV

REC, IF, ASK = 38.0, 7.0, 55.0


def hits(a, path, unit):
    return sum(1 for f in P.OPERATING if round(a[f][path] / unit) == round(a[f]["gold"] / unit))


def main(target):
    K = SV.Pack(target)
    c = SV.call(K)
    a, b = SV.ask_a(K), SV.ask_b(K)
    n = len(P.OPERATING)
    pa = {"the station file's sensor serial to its certificate in force each day (the natural join)": "label_asof",
          "the station file's sensor serial to its latest certificate": "label_latest",
          "the register's sensitivity on every day": "register",
          "the right sensor each day, each sensor's latest certificate": "gold_latest",
          "the right sensitivities over every day's satellite irradiation": "all_days"}
    pb = {"the CMMS attended stamp less the CMMS raised stamp (the natural read)": "cmms",
          "the CMMS attended stamp in UTC less the alarm's raised time": "attended",
          "the CMMS attended stamp, unconverted, less the alarm's raised time": "mixed",
          "the van tracker's entry read as UTC": "tracker_raw",
          "the van tracker less the work order's raised stamp": "from_wo",
          "the CMMS attended stamp where it falls before the alarm cleared": "possible_only"}
    # a response that has met ask B's device (the tracker's arrival in UK time) and skips the van the technician had
    met_b = {"the first van of any technician at the farm after the alarm": "any_van"}
    ha = {k: hits(a, v, 0.001) for k, v in pa.items()}
    hb = {k: hits(b, v, 0.1) for k, v in pb.items()}
    print("ask A, pyranometer ratio (%d figures), paths of a response that misses the device:" % n)
    for k, v in ha.items():
        print("   %-96s %2d of %d" % (k, v, n))
    print("ask B, hours to arrival (%d figures), paths of a response that misses the device:" % n)
    for k, v in hb.items():
        print("   %-96s %2d of %d" % (k, v, n))
    print("ask B, a stop after meeting the device (the ask's ladder; the van the technician had lands %d):" % n)
    for k, v in met_b.items():
        print("   %-96s %2d of %d" % (k, hits(b, v, 0.1), n))
    ka, kb = max(ha.values()), max(hb.values())
    mirror = 0.0 + IF + ASK * (ka + kb) / (2.0 * n)
    print("mirror: Hallam Down at the meter, both devices missed: %.1f" % mirror)
    for label, x, y in [("both devices missed", ka, kb), ("ask A's device met", n, kb), ("ask B's device met", ka, n),
                        ("both devices met", n, n)]:
        cr = REC + IF + ASK * (x + y) / (2.0 * n)
        print("cracker (the call), %-22s %5.1f   pair %5.1f" % (label + ":", cr, (cr + mirror) / 2))
    print("(the asks read no file the call reads, so both responses take the same ask paths; separation is asserted in "
          "checks.py)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
