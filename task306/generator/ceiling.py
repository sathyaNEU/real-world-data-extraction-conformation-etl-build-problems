"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task306/generator/ceiling.py

Rows: the cracker lands the call, runs the hygiene battery and executes every filed rule: it counts one letter per
reference, takes each letter's half from the workflow log's receipt (the asking sentence's basis), re-keys the GP
Connect receipts on patient, sender and document date, recognises the 7 April 2026 batch as a re-send and drops it,
converts the hub's UTC slots, matches the hub's appointments to the practice systems' records on patient and day, and
counts each attended patient in the group register (programme section 4.1); the mirror stops at the pilot's average
take-off on the call and handles the asks the same way, since they carry nothing from it; the full includer also
matches each GP Connect receipt to the letter it follows, keeps the first-time letters in the 7 April batch, and
matches a hub appointment to the same pharmacist's record on the next working day (a stress row, not the gate)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402


def kept(X, G):
    return sum(A.r1(X[k]["rate"]) == A.r1(G[k]["rate"]) for k in G)


def main(target=TARGET):
    D = A.load(target)
    L = A.resolved_letters(D)
    gA, gB = A.letters_received(D, L=L), A.consultations(D)
    n = len(gA) + len(gB)
    rows = {
        "cracker": (A.letters_received(D, L=L, gpconnect="exact", resend_mode="batch"),
                    A.consultations(D, dedupe="same_day")),
        "cracker, unmatched receipts on the letter date": (
            A.letters_received(D, L=L, gpconnect="exact_fallback", resend_mode="batch"),
            A.consultations(D, dedupe="same_day")),
        "cracker, re-sends kept": (A.letters_received(D, L=L, gpconnect="exact", dedupe_resend=False),
                                   A.consultations(D, dedupe="same_day")),
        "full includer": (A.letters_received(D, L=L), A.consultations(D)),
    }
    out = {}
    for name, (a, b) in rows.items():
        out[name] = (kept(a, gA), kept(b, gB))
        print("%-48s keeps ask A %2d of %d, ask B %2d of %d" % (name, out[name][0], len(gA), out[name][1], len(gB)))
    crack = max(sum(v) for k, v in out.items() if k.startswith("cracker"))
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    full = sum(out["full includer"]) / n
    print("cracker keeps %d of %d ask criteria, response %.1f; mirror the same asks off the call, response %.1f"
          % (crack, n, c, s))
    print("full includer (stress row): response %.1f on the call" % (38 + 7 + 55 * full))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    deltas(D, L, gA, gB)
    return (c + s) / 2, 100 * lc


def deltas(D, L, gA, gB):
    """How far each device's mishandling moves the figures it misses, per 1,000 registered patients, unrounded."""
    def span(X, G, keys):
        moved = [abs(X[k]["rate"] - G[k]["rate"]) for k in keys if A.r1(X[k]["rate"]) != A.r1(G[k]["rate"])]
        return (min(moved) if moved else 0.0), (max(moved) if moved else 0.0), len(moved)
    h1 = [k for k in gA if k[1] == "H1"]
    h2 = [k for k in gA if k[1] == "H2"]
    allb = list(gB)
    routes = [
        ("ask A, the 7 April re-sends kept", A.letters_received(D, L=L, dedupe_resend=False), gA, h1),
        ("ask A, the whole 7 April batch dropped", A.letters_received(D, L=L, resend_mode="batch"), gA, h1),
        ("ask A, GP Connect re-keyed on patient, sender and document date",
         A.letters_received(D, L=L, gpconnect="exact"), gA, h2),
        ("ask A, GP Connect receipts left on the letter date", A.letters_received(D, L=L, gpconnect="letter_date"),
         gA, h2),
        ("ask B, hub and practice matched on patient and day", A.consultations(D, dedupe="same_day"), gB, allb),
        ("ask B, a group session as one consultation", A.consultations(D, groups="session"), gB, allb),
    ]
    for name, X, G, keys in routes:
        lo, hi, n_ = span(X, G, keys)
        print("%-66s moves %d of %d figures, by %.2f to %.2f" % (name, n_, len(keys), lo, hi))


if __name__ == "__main__":
    main()
