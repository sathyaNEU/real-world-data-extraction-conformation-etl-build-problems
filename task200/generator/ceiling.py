"""The ask sheet's cracker and mirror, run as code on the cut pack, and each device's single-finding lift.

The cracker lands the call, runs the hygiene battery (the first-of-month repeat rows, the code change in the search
log, the two clocks, the export layouts), executes every filed rule (SPS-04's team, screen time, search and
certificate definitions) and reads every document; it takes each ask the careful way short of the reconstruction the
ask's device needs:
  A  CT session rows summed as exported; Pier B log-ons closed at the operator's log-off, the next log-on or the
     shutdown, each badge read through the roster's current badge
  B  each clear search record counted once against the reject of its (first) tray, badges read through the roster
  C  each screener's latest passed certification on its LMS date
The mirror stops at the most attractive wrong rung: A the CT rows summed and only paired Pier B log-ons, B each
record once with the badges read through the register, C the LMS dates. Each device is then fixed alone from the
cracker's route, and the ask weight that one finding buys is asserted at a third or less.

    python3 task200/generator/ceiling.py [target]
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as S_  # noqa: E402

CALL, IF, MISS = 38.0, 7.0, 5.0
ASKS = 55.0


def digest(target):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(target)):
        for f in sorted(files):
            h.update(open(os.path.join(root, f), "rb").read())
    return h.hexdigest()[:12]


def main(target):
    ros = S_.roster(target)
    gold = {"A": S_.ask_hours(target, ros).round(1), "B": S_.ask_clear(target, ros), "C": S_.ask_certs(target, ros)}
    crack = {"A": S_.ask_hours(target, ros, "rows", "golden", register=False).round(1),
             "B": S_.ask_clear(target, ros, split=False, register=False),
             "C": S_.ask_certs(target, ros, "lms")}
    mirror = {"A": S_.ask_hours(target, ros, "rows", "paired", register=False).round(1),
              "B": S_.ask_clear(target, ros, split=False, register=True),
              "C": S_.ask_certs(target, ros, "lms")}
    tol = {"A": 0.05, "B": 0.5, "C": 0.5}
    total = kc = km = 0
    print("pack %s" % digest(target))
    print("%-4s %8s %8s" % ("ask", "cracker", "mirror"))
    for k in ("A", "B", "C"):
        hc = int(((crack[k] - gold[k]).abs() < tol[k]).sum())
        hm = int(((mirror[k] - gold[k]).abs() < tol[k]).sum())
        total += len(gold[k])
        kc += hc
        km += hm
        print("%-4s %5d/%d %5d/%d" % (k, hc, len(gold[k]), hm, len(gold[k])))
    lc, lm = kc / total, km / total
    pair = (CALL + IF + ASKS * lc + MISS + IF + ASKS * lm) / 2
    print("cracker keeps %.1f per cent of ask weight, mirror %.1f per cent" % (100 * lc, 100 * lm))
    # each device fixed alone, from the cracker's route: the ask weight that one finding buys
    lifts = {
        "A: CT rows merged per login": (S_.ask_hours(target, ros, "union", "golden", register=False).round(1), "A"),
        "A and B: badges read through the ID Centre register (A part)":
            (S_.ask_hours(target, ros, "rows", "golden", register=True).round(1), "A"),
        "B: two-tray records split": (S_.ask_clear(target, ros, split=True, register=False), "B"),
        "A and B: badges read through the ID Centre register (B part)":
            (S_.ask_clear(target, ros, split=False, register=True), "B"),
        "C: centre dates through the LMS refs": (S_.ask_certs(target, ros, "joined"), "C"),
        "C: centre certificates the LMS lacks": (S_.ask_certs(target, ros, "lms_plus"), "C"),
    }
    reg = 0
    for name, (v, k) in lifts.items():
        n = int(((v - gold[k]).abs() < tol[k]).sum()) - int(((crack[k] - gold[k]).abs() < tol[k]).sum())
        if "register" in name:
            reg += n
            continue
        print("single finding %-40s %2d of %d figures, %.1f per cent of ask weight" % (name, n, total, 100.0 * n / total))
        assert n / total <= 1 / 3 + 1e-9, name
    print("single finding %-40s %2d of %d figures, %.1f per cent of ask weight" % ("badges through the register (A and B)",
                                                                                    reg, total, 100.0 * reg / total))
    assert reg / total <= 1 / 3 + 1e-9
    print("pair ceiling %.1f" % pair)
    return dict(cracker=lc, mirror=lm, pair=pair)


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    main(t)
