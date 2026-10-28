"""The ask sheet, measured on the cut pack: the cracker (lands the call, runs the hygiene battery, executes every filed
rule: the pathway's last dose and twelve-week test) and the mirror (stops on the most attractive wrong rung, R2, and
does the ask as the cracker does). Weights 38 / 7 / 55 (supplemental-stumping Part 0).

    python3 task304/generator/cracker.py"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import checks
import params as P
import solve as S


def main():
    target = os.path.join(os.path.dirname(HERE), "target")
    R = S.solve(target)
    F, T, AH = R["F"], R["T"], R["AH"]
    stops = checks.ask_stops(T)
    rows = []
    # construction: active and starts per setting (cracker = golden; mirror = R2)
    c_keep = m_keep = 0
    for s in P.SETTINGS:
        for k, kr2 in (("active", "active_R2"), ("starts", "starts_R2")):
            g = S.r10(F[s][k])
            m = S.r10(F[s][kr2])
            c_keep += 1
            m_keep += int(m == g)
            rows.append(("C %s %s" % (s, k), g, g, m))
    # chart: one bar per setting, the setting marked
    c_keep += 2
    m_keep += 1
    rows.append(("C chart bars", "4", "4", "4"))
    rows.append(("C chart marks", "NSP", "NSP", "AP"))
    # the ask: confirmed cures by clinic and half-year (cracker joins on the register's pseudonym)
    a_c = a_m = 0
    for kk in sorted(AH):
        g = AH[kk]["confirmed"]
        cv = stops["pseudonym_only"][kk]["confirmed"]
        a_c += int(cv == g)
        a_m += int(cv == g)
        rows.append(("A %s_%d" % kk, g, cv, cv))
    n_ask = 8 + 2 + len(AH)
    kc = (c_keep + a_c) / n_ask
    km = (m_keep + a_m) / n_ask
    cr = 38 + 7 + 55 * kc
    mr = 5 + 7 + 55 * km
    print("%-22s %8s %8s %8s %s" % ("criterion", "golden", "cracker", "mirror", "cracker verdict"))
    for name, g, c, m in rows:
        verdict = "outside" if name.startswith("C") else ("miss" if c != g else "HIT")
        print("%-22s %8s %8s %8s %s" % (name, g, c, m, verdict))
    print("cracker keeps %d of %d ask criteria (%.3f), mirror %d (%.3f)" % (c_keep + a_c, n_ask, kc, m_keep + a_m, km))
    print("cracker %.1f  mirror %.1f  pair ceiling %.1f  mirror leakage %.1f per cent" %
          (cr, mr, (cr + mr) / 2, 100 * km))
    # the same with a cracker who also links the laboratory's patient record (the worst case for this ask)
    kc2 = (c_keep + len(AH)) / n_ask
    km2 = (m_keep + len(AH)) / n_ask
    print("if every pseudonym of a laboratory patient is read: cracker %.1f mirror %.1f pair %.1f" %
          (38 + 7 + 55 * kc2, 5 + 7 + 55 * km2, (38 + 7 + 55 * kc2 + 5 + 7 + 55 * km2) / 2))
    return (cr + mr) / 2, 100 * km


if __name__ == "__main__":
    main()
