"""task183 ceiling: the pair arithmetic measured on the cut pack. Each row is a response modelled as code on
target/, scored on the rubric's weights (38 the call and its components, 7 instruction-following, 55 the asks,
spread evenly over the 48 ask figures), a hit within half a unit of the stated rounding.

The cracker lands the call and runs the careful solver's whole route on the asks: it de-duplicates the re-sent An
Post day by ap_ref, reads every field by its plain meaning
(notes_eur as notes, coin_eur as coin, received_at as the time the log took the Z-report), executes Schedule 2
lodgement by lodgement, reads the hour profile (a Z sent after midnight or in the morning closes the day before) and
the Z numbers against the receipts (a batch fills the days back from there, one Z a day). The mirror stops at the
default path's call and runs the same asks. The full includer handles every device and must reproduce figures.json,
or this script exits 1.

    python3 task183/generator/ceiling.py [target]"""
from __future__ import annotations

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C   # noqa: E402

W_CALL, W_INSTR, W_ASK = 38.0, 7.0, 55.0


def ask_hits(golden, ap, till):
    hits, n = 0, 0
    for m in C.MONTHS:
        for k, i in (("cash_eur", 1), ("fee_eur", 2)):
            n += 1
            hits += abs(ap[m][i] - golden["an_post"][m][k]) < 0.005
        for k, i, tol in (("cash_sales_eur", 1, 0.005), ("paid_outs_eur", 2, 0.005)):
            n += 1
            hits += abs(till[m][i] - golden["till"][m][k]) < tol
    return hits, n


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    P = C.Pack(target)
    digest = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(target, f), "rb").read()).hexdigest()
                                    for f in sorted(os.listdir(target))).encode()).hexdigest()[:16]
    routes = {
        "cracker (on the call, careful route)": (True, C.ap_figures(target, "plain"),
                                                  C.till_figures_ask(P, target, "cracker")),
        "mirror (off the call at the peer screen, same asks)": (False, C.ap_figures(target, "plain"),
                                                                 C.till_figures_ask(P, target, "cracker")),
        "lazy (on the call, received dates, plain notes)": (True, C.ap_figures(target, "plain"),
                                                             C.till_figures_ask(P, target, "received")),
        "notes-only over-correction (on the call)": (True, C.ap_figures(target, "notes_only"),
                                                     C.till_figures_ask(P, target, "cracker")),
        "D3 seen and repaired, D8 read the careful way (on the call)": (True, C.ap_figures(target, "golden"),
                                                                          C.till_figures_ask(P, target, "cracker")),
        "D8 seen, Z-reports laid on the terminal's last days (on the call)": (True, C.ap_figures(target, "plain"),
                                                                               C.till_figures_ask(P, target,
                                                                                                  "terminal_count")),
        "D8 repaired by the terminal's amounts, D3 missed (on the call)": (True, C.ap_figures(target, "plain"),
                                                                            C.till_figures_ask(P, target, "golden")),
        "full includer (every device handled)": (True, C.ap_figures(target, "golden"),
                                                 C.till_figures_ask(P, target, "golden")),
    }
    print("task183 ceiling on pack %s (weights %g / %g / %g)" % (digest, W_CALL, W_INSTR, W_ASK))
    scores = {}
    for name, (on, ap, till) in routes.items():
        h, n = ask_hits(figs, ap, till)
        sc = (W_CALL if on else 5.0) + W_INSTR + W_ASK * h / n
        scores[name] = (sc, h, n)
        print("  %-55s call %-4s asks %2d of %d kept   %.1f" % (name, "yes" if on else "no", h, n, sc))
    fi = scores["full includer (every device handled)"]
    if fi[1] != fi[2]:
        print("full includer does not reproduce figures.json")
        raise SystemExit(1)
    c = scores["cracker (on the call, careful route)"][0]
    m = scores["mirror (off the call at the peer screen, same asks)"][0]
    print("  pair ceiling (cracker and mirror): %.1f" % ((c + m) / 2))
    print("  two careful responses both on the call: %.1f each" % c)
    print("  mirror leakage: %.1f%% of the ask weight" % (100.0 * scores["mirror (off the call at the peer screen, "
                                                                  "same asks)"][1] / fi[2]))
    print("  devices: D3 An Post notes_eur carries all the cash on the older counter platform (plain read of the "
          "field, the battery has no denomination test) ; D8 the till log's received_at for batched mobile tills "
          "(hour profile and Z sequence read, days filled back one a day, the terminal's trading days never read)")
    return scores


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    main(t)
