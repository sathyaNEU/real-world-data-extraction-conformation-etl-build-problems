"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task485/generator/ceiling.py

Rows. The cracker lands the call and runs the battery: it nets reversals, reads both export layouts, maps the old group
codes to the accounts, assigns every remittance line to its quarter of service and leaves the fiscal 2025 lines out,
prices brand claims at Exhibit C's rates by the pharmacy's network in pharmacy_network_202610.txt, and links each
claim before 1 January 2026 to the roster through the subscriber's legacy cardholder number, keeping the claim's
person code. The mirror stops at the split by ingredient cost on the call and handles the asks the same way, since
nothing in them comes from the call. The full includer also reads each claim's network from its own adjudication (the
retail dispensing fee) and matches dependants on birth date and gender (a stress row, not the gate)."""
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402


def ask_figures(pk, rates, channel, ident):
    f = {}
    for k, v in pk.guarantee(rates, channel=channel).items():
        for ch in A.CHANNELS:
            f["A %s %s claims" % (k, ch)] = v["n"][ch]
        f["A %s guarantee" % k] = int(round(v["guarantee"]))
        f["A %s remitted" % k] = int(round(v["remitted"]))
        f["A %s shortfall" % k] = int(round(v["shortfall"]))
    for (c, a), n in pk.members(ident).items():
        f["B %s %s" % (c, a)] = n
    return f


def main(target=TARGET):
    pk = A.Pack(target)
    rates = A.exhibit_rates(target)
    D = pk.D
    by_legacy = {r["legacy_cardholder_id"]: r["cardholder_id"] for r in D["roster"] if r["legacy_cardholder_id"]}

    def carried(c):
        if c["dos"] >= dt.date(2026, 1, 1):
            return ("N", c["card"], c["pc"])
        new = by_legacy.get(c["card"])
        return ("N", new, c["pc"]) if new else ("O", c["card"], c["pc"])
    gold = ask_figures(pk, rates, pk.channel, pk.persons())
    crack_f = ask_figures(pk, rates, pk.channel_file, {c["no"]: carried(c) for c in D["claims_all"]})
    n = len(gold)
    kept = [k for k in gold if crack_f[k] == gold[k]]
    full = sum(1 for k in gold if gold[k] == gold[k])
    lc = len(kept) / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    na = sum(1 for k in gold if k.startswith("A "))
    ka = sum(1 for k in kept if k.startswith("A "))
    print("cracker (lands the call, battery, the network file read as every date's network, the claim's person code "
          "carried): keeps %d of %d ask criteria (ask A %d of %d, ask B %d of %d), response %.1f"
          % (len(kept), n, ka, na, len(kept) - ka, n - na, c))
    print("  kept: %s" % ", ".join(kept))
    print("mirror (the split by ingredient cost on the call, the same ask handling): keeps %d of %d, response %.1f"
          % (len(kept), n, s))
    print("full includer (network from each claim's own adjudication, dependants on birth date and gender, stress "
          "row): keeps %d of %d, response %.1f" % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main()
