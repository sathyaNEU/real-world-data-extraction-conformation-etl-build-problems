"""The ask sheet's measurement on the cut pack: the cracker (lands the call, runs the battery, executes every filed rule)
and the mirror (the register-only call), each scored figure by figure on the 38/7/55 weights, with every path each ask
offers a response that does not meet its device.

    python3 task306/generator/pair.py <target dir>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P
import solve as S

REC, IF, ASK = 38.0, 7.0, 55.0


def hits(paths, gold, unit):
    """for each path, the platforms whose printed figure equals the golden's"""
    out = {}
    for k, f in paths.items():
        out[k] = sum(1 for n in P.NAMES if round(f[n] / unit) == round(gold[n] / unit))
    return out


def main(target):
    pk = S.Pack(target, P.FILES)
    c = pk.call()
    gold_slots, gold_total = c["lots"]["slots"], int(round(c["total"] / 100.0) * 100)
    reg_slots = S.lots(c["base"])["slots"]
    reg_total = int(round(sum(c["base"].values()) / 100.0) * 100)
    call_n = 6
    mirror_call = sum(reg_slots[n] == gold_slots[n] for n in P.NAMES) + (reg_total == gold_total)
    ln = S.Line(target, P.FILES)
    A, B, C = ln.ask_a(), ln.ask_b(), ln.ask_c()
    pa = {"stores lines summed, returns netted, carriers as 2 (the natural read)": ln.ask_a("naive"),
          "lines alike on pick, lot and quantity collapsed (the over-repair)": ln.ask_a("dedup"),
          "issues only": ln.ask_a("issues_only"),
          "carriers as units": ln.ask_a("units")}
    pb = {"first run by pakket_id (the natural read)": ln.ask_b("by_id"),
          "an aborted run counted as the first": ln.ask_b("abort_counts")}
    pc = {"every AFGEKEURD row in the intake export (the natural read)": ln.ask_c("naive"),
          "every recycler line in the year as a reject": ln.ask_c("all_recycled")}
    # stops of a response that has met ask C's device (it saw that cores the line scrapped read AFGEKEURD) and
    # repairs it another way than the join on kerncode: the ask's ladder, not the paths of a response that misses it
    met_c = {"the cores scrapped on the line taken out of both counts": ln.ask_c("both_out"),
             "the year's scrapped work orders subtracted by count": ln.ask_c("count_scrapped")}
    ha, hb, hc = hits(pa, A, 1.0), hits(pb, B, 0.1), hits(pc, C, 0.1)
    print("ask A, modules per lot (5 figures):")
    for k, v in ha.items():
        print("   %-72s %d of 5" % (k, v))
    print("ask B, first-run pass share (5 figures):")
    for k, v in hb.items():
        print("   %-72s %d of 5" % (k, v))
    print("ask C, intake reject share (5 figures):")
    for k, v in hc.items():
        print("   %-72s %d of 5" % (k, v))
    print("ask C, stops after meeting the device (the ladder; a response that meets it and joins on kerncode lands 5):")
    for k, v in hits(met_c, C, 0.1).items():
        print("   %-72s %d of 5" % (k, v))
    keep = max(ha.values()) + max(hb.values()) + max(hc.values())
    lc = ls = keep / 15.0
    cracker = REC + IF + ASK * lc
    r = REC * mirror_call / call_n
    mirror = r + IF + ASK * ls
    pair = (cracker + mirror) / 2
    print("cracker: the call (6 of 6) and the best path on each ask, %d of 15 ask figures: %.1f" % (keep, cracker))
    print("mirror: the register-only call (%d of 6: %s) and the same ask paths: %.1f" % (mirror_call, reg_slots, mirror))
    print("Pair ceiling: %.1f" % pair)
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * ls))
    print("(the asks read no file the call reads, so both responses take the same ask paths; separation is asserted in "
          "checks.py)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
