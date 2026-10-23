"""The pair ceiling, run on the cut pack, against the routes the stage 4 readers actually took on rounds 1 and 2 as well as
the cracker. Every route lands the call (worst case) and works the asks its own way:

  cracker   counts every fiscal 2026 install and sums every receipt line
  reader A  drops installs at premises whose first account predates the install, places premises through the plat
            unit of the parcel number (core without one), dedupes receipts by receipt number
  reader B  drops installs at premises whose first account started more than 1,000 days before the install, places
            premises through their set-up date, dedupes receipts by receipt number
  stored    reader A with the premise's stored UEP_PHASE
  reader D  round 2: a premise's first install, at a premise with no account opened before it, placed through the plat
            unit of the parcel number (address where the parcel is blank); sums Amount on every receipt line
  reader E  reader D counting only premises the extract shows ACTIVE, dedupes receipts by receipt number

The asks read nothing the call's construction produces, so the mirror (the analog on the call) works them the same
way. Weights 38, 7, 55 (supplemental-stumping Part 0); a hit only when exact at the stated rounding.

    python3 ceiling.py <target>"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc                 # noqa: E402

PHASES = ["Core", "1", "2", "3", "4"]


def main(target):
    P = calc.Pack(target)
    r = calc.connections_fy26(target, P)
    fees, lines, by_no = calc.fees_fy26(target)
    golden = [r["golden"][(ph, q)] for ph in PHASES for q in (1, 2, 3, 4)] + [round(fees[q]) for q in (1, 2, 3, 4)]
    paths = {
        "cracker": [r["cracker"][(ph, q)] for ph in PHASES for q in (1, 2, 3, 4)] + [round(lines[q]) for q in (1, 2, 3, 4)],
        "reader A": [r["reader_a"][(ph, q)] for ph in PHASES for q in (1, 2, 3, 4)] + [round(by_no[q]) for q in (1, 2, 3, 4)],
        "reader B": [r["reader_b"][(ph, q)] for ph in PHASES for q in (1, 2, 3, 4)] + [round(by_no[q]) for q in (1, 2, 3, 4)],
        "stored": [r["stored_phase"][(ph, q)] for ph in PHASES for q in (1, 2, 3, 4)] + [round(by_no[q]) for q in (1, 2, 3, 4)],
        "reader D": [r["reader_d"][(ph, q)] for ph in PHASES for q in (1, 2, 3, 4)] + [round(lines[q]) for q in (1, 2, 3, 4)],
        "reader E": [r["reader_e"][(ph, q)] for ph in PHASES for q in (1, 2, 3, 4)] + [round(by_no[q]) for q in (1, 2, 3, 4)],
    }
    n = len(golden)
    keep = {k: sum(1 for a, b in zip(golden, v) if a == b) for k, v in paths.items()}
    for k, v in keep.items():
        print("%-9s keeps %d of %d ask figures" % (k, v, n))
    for i, g in enumerate(golden):
        print("   figure %2d golden %10s  %s  %s" % (i + 1, g, "  ".join("%s %s" % (k, paths[k][i]) for k in paths),
                                                  "miss" if all(paths[k][i] != g for k in paths) else "HIT"))
    worst = max(keep.values())
    Lc = Ls = worst / n
    C_score = 38 + 7 + 55 * Lc
    S_score = 5 + 7 + 55 * Ls
    pair = (C_score + S_score) / 2
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight (worst route)"
          % (C_score, S_score, pair, 100.0 * Ls))
    print("separation: the asks read %s, %s, %s and %s, which the call never reads, and the roll only to place a premise "
          "in its plat unit; no device row sits in the roll or the permit files" % (calc.C.F_AMI, calc.C.F_ACCT, calc.C.F_PREM, calc.C.F_FEES))
    return pair


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
