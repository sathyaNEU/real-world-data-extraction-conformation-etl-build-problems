"""task199 pair ceiling, solved rather than asserted.

Scores two responses on the generated rubric's weights and prints both columns:

  cracker  lands the call, runs the hygiene battery (key uniqueness, exact duplicates, unmatched
           joins, fan-out, count ties), reads the data dictionary and executes every filed rule it
           points at. It therefore handles every documented convention and every battery-visible
           mess correctly, and loses only figures a primary device reaches, because each primary is
           an inconsistency nothing in the pack invites (a rollup above its own parts, a control
           total true only in its own scope, a numeric column contradicting its own note field).
  mirror   stops at the most attractive wrong rung on the call, and answers the asks without the
           battery or the dictionary. It loses every figure the cracker loses, plus the figures a
           documented hazard reaches.

Weights are Part 0's (38 recommendation and critical components, 7 instruction-following, 55 asks)
so builds are comparable; `--bands` prints the same pair at the ends of CLAUDE.md's legal bands.

    python3 task199/generator/ceiling.py
    python3 task199/generator/ceiling.py --bands

Stage 2 runs this on the clean truth's figure tables. Stage 3 re-points the keep flags at the cut
pack (each flag becomes an assertion that the response's own path lands outside the figure's bin)
and the gated field takes whichever measurement is worse.
"""
import sys

W_REC, W_INSTR, W_ASK = 38.0, 7.0, 55.0
R_WRONG_CALL = 5.0      # recommendation weight a response that misses the call still keeps
MIRROR_BAR = 35.0
PAIR_BAR = 40.0

# One row per graded ask figure: (ask, figure, reached by the ask's primary, reached by a hazard).
# A figure reached by the primary is lost by both responses; a figure reached only by a hazard is
# lost by the mirror alone; a figure reached by neither is free to both and is a candidate to fold.
FIGURES = []


def add(ask, name, n, primary, hazard):
    for i in range(n):
        FIGURES.append((ask, "%s %d" % (name, i + 1) if n > 1 else name, primary, hazard))


# Ask A: the service's deliveries for 2025 reconciled to its invoices, by quarter and outlet type.
# Primary: the service's contract requires a monthly completeness re-push, so the items that failed
# checksum in one month arrive in the next month's batch under fresh item ids with their publication
# dates kept, while the invoice bills each item once. The re-push runs every month, so it reaches
# every quarter and every outlet type.
add("A", "items delivered, quarter x daily", 4, True, False)
add("A", "items delivered, quarter x radio", 4, True, False)
add("A", "items delivered, quarter x digital", 4, True, False)
add("A", "items delivered, quarter x agency", 4, True, False)
add("A", "amount billed, quarter", 4, True, True)       # hazard H2: invoice amounts in thousands
add("A", "reconciling item group", 5, True, False)

# Ask B: what the register holds for the twelve municipalities outside the designation panel, 2025.
# Primary: the register's published monthly summary is built at desk grain and named by municipality,
# so for every two-municipality desk the seat's count stands above its own parts and the partner's
# below. It reaches every figure in the ask.
add("B", "actions held, municipality", 12, True, False)
add("B", "months holding no action, municipality", 12, True, False)
add("B", "corridor total", 3, True, False)

# Ask C: participants estimated per action by actor sector, 2025.
# Primary: radio-transcript coding writes a reported range's lower bound into the numeric column
# while the note field holds the range, against a manual sentence that says the column carries a
# central estimate. Radio transcripts reach every sector, so the primary reaches every figure.
# The per-sector action counts are not asked for and so are not graded (a figure the prompt never
# asks for is an open fork by construction, determinism-check section 5).
add("C", "mean participants per action, sector", 6, True, False)
add("C", "participants in total, sector", 6, True, False)
add("C", "corridor total", 2, True, False)


def score(weights=(W_REC, W_INSTR, W_ASK)):
    w_rec, w_instr, w_ask = weights
    n = len(FIGURES)
    cracker_keep = [f for f in FIGURES if not f[2]]
    mirror_keep = [f for f in FIGURES if not f[2] and not f[3]]
    lc, ls = len(cracker_keep) / n, len(mirror_keep) / n
    c = w_rec + w_instr + w_ask * lc
    s = R_WRONG_CALL + w_instr + w_ask * ls
    return dict(n=n, cracker_keep=cracker_keep, mirror_keep=mirror_keep, lc=lc, ls=ls,
                c=c, s=s, pair=(c + s) / 2.0, weights=weights)


def per_ask():
    out = {}
    for ask in sorted({f[0] for f in FIGURES}):
        rows = [f for f in FIGURES if f[0] == ask]
        out[ask] = dict(n=len(rows),
                        cracker=len([f for f in rows if not f[2]]),
                        mirror=len([f for f in rows if not f[2] and not f[3]]))
    return out


def main():
    r = score()
    print("=" * 94)
    print("PAIR CEILING, solved on Part 0's weights (%.0f recommendation, %.0f instruction, %.0f asks)"
          % (W_REC, W_INSTR, W_ASK))
    print("=" * 94)
    print("  %d graded ask figures across %d asks" % (r["n"], len({f[0] for f in FIGURES})))
    print()
    print("  %-10s %-44s %10s %10s" % ("response", "what it does", "ask keep", "score"))
    print("  %-10s %-44s %10s %10.1f" % ("cracker", "lands the call, battery and dictionary run",
                                         "%d of %d" % (len(r["cracker_keep"]), r["n"]), r["c"]))
    print("  %-10s %-44s %10s %10.1f" % ("mirror", "stops at the most attractive wrong rung",
                                         "%d of %d" % (len(r["mirror_keep"]), r["n"]), r["s"]))
    print()
    print("  PAIR CEILING          %.1f   (bar %.0f, build to 40)" % (r["pair"], PAIR_BAR))
    print("  MIRROR LEAKAGE        %.1f per cent of ask weight   (bar under %.0f)"
          % (100 * r["ls"], MIRROR_BAR))
    print("  verdict               %s" % ("PASS" if r["pair"] <= PAIR_BAR and 100 * r["ls"] < MIRROR_BAR
                                          else "FAIL"))
    print()
    if len(r["cracker_keep"]) == len(r["mirror_keep"]):
        print("  the two rows agree on the asks, and that is a property of the design rather than a")
        print("  duplicated measurement: every ask device sits outside the call's declared population")
        print("  (a municipality the protocol does not cover, a column the call never reads, or 2025),")
        print("  so neither response's call error reaches an ask figure. The separation assertions in")
        print("  checks.py prove it by count. What differs between the rows is the call, worth %.0f."
              % (W_REC - R_WRONG_CALL))
    print()
    print("  the two columns are scored from different readings, ask by ask:")
    print("  %-5s %8s %10s %10s" % ("ask", "figures", "cracker", "mirror"))
    for ask, d in per_ask().items():
        print("  %-5s %8d %10s %10s" % (ask, d["n"], "%d kept" % d["cracker"], "%d kept" % d["mirror"]))
    print()
    print("  figures free to both responses (fold or cut these if the cut-pack measurement rises):")
    for f in r["mirror_keep"]:
        print("      ask %s  %s" % (f[0], f[1]))

    print()
    print("=" * 94)
    print("SWEEP  the pair at each cracker keep count, so the target is solved rather than argued")
    print("=" * 94)
    n = r["n"]
    print("  (the mirror is held at the %d figures a hazard does not reach, its measured value)"
          % len(r["mirror_keep"]))
    print("  %-14s %8s %8s %8s" % ("cracker keeps", "Lc", "pair", "verdict"))
    for keep in range(0, n + 1, max(1, n // 14)):
        lc = keep / n
        c = W_REC + W_INSTR + W_ASK * lc
        pair = (c + r["s"]) / 2.0
        print("  %-14s %8.3f %8.1f %8s" % ("%d of %d" % (keep, n), lc, pair,
                                           "PASS" if pair <= PAIR_BAR else "FAIL"))
    limit = None
    for keep in range(n, -1, -1):
        pair = (W_REC + W_INSTR + W_ASK * keep / n + r["s"]) / 2.0
        if pair <= PAIR_BAR:
            limit = keep
            break
    print("  the cracker may keep at most %d of %d figures before the pair breaches %.0f;"
          " it keeps %d" % (limit, n, PAIR_BAR, len(r["cracker_keep"])))

    if "--bands" in sys.argv:
        print()
        print("=" * 94)
        print("THE SAME PAIR AT THE ENDS OF CLAUDE.md's LEGAL BANDS (the gate reads Part 0's row)")
        print("=" * 94)
        for w in ((38.0, 7.0, 55.0), (30.0, 10.0, 60.0), (40.0, 5.0, 55.0)):
            rr = score(w)
            print("  weights %-18s cracker %5.1f  mirror %5.1f  pair %5.1f"
                  % ("%.0f/%.0f/%.0f" % w, rr["c"], rr["s"], rr["pair"]))




# ------------------------------------------------- forcing, measured on the cut pack

def forcing():
    """Per ask figure, the natural read's value against the golden's, read from the shipped bundle.
    A figure counts as moved when the two differ by more than the rounding its asking sentence
    states: whole items and whole actions, participants and rates to one decimal.

        python3 task199/generator/ceiling.py --forcing
    """
    import csv
    import json as _json
    import os as _os
    from datetime import date as _date
    here = _os.path.dirname(_os.path.abspath(__file__))
    target = _os.path.join(_os.path.dirname(here), "target")
    fig = _json.load(open(_os.path.join(here, "figures.json"), encoding="utf-8"))

    def rows(name):
        with open(_os.path.join(target, name), encoding="utf-8") as f:
            return list(csv.DictReader(f))

    PANEL = {w["city"] for w in fig["watch_note"]}
    moved = []

    # Ask A. The natural read takes each quarter's delivery rows as that quarter's billing, so the
    # billed column equals the delivered column and no quarter has a gap to close.
    for q in (1, 2, 3, 4):
        nat = fig["ask_a_totals"]["T%d" % q]
        gold = fig["ask_a_billed"]["T%d" % q]
        moved.append(("A billed T%d" % q, nat, gold, abs(nat - gold) >= 1))
    for k, v in fig["ask_a_lines"].items():
        moved.append(("A reconciling group %s" % k, 0, v, v >= 1))

    # Ask B. The natural read takes the published monthly summary, which is seated by desk.
    summ = {}
    for r in rows("resumen_mensual_rac_2025.csv"):
        summ[r["municipio_sede"]] = summ.get(r["municipio_sede"], 0) + int(r["acciones_dia"])
    for x in fig["ask_b"]:
        nat = summ.get(x["city"], 0)
        moved.append(("B held %s" % x["city"], nat, x["held"], abs(nat - x["held"]) >= 1))

    # Ask C. The natural read takes the numeric participants column as it stands: a reported range
    # enters at its lower bound and an unreported figure enters as zero.
    tot, n, mx = {}, {}, {}
    for name, dcol, scol, pcol in (("rac_acciones_2025.csv", "fecha_de_accion", "sector",
                                    "participantes"),):
        for r in rows(name):
            if r["municipio"] in PANEL:
                continue
            v = r[pcol]
            v = int(v) if v not in ("", None) else 0
            s = r[scol]
            tot[s] = tot.get(s, 0) + v
            n[s] = n.get(s, 0) + 1
            mx[s] = max(mx.get(s, 0), v)
    for x in fig["ask_c"]:
        nat = round(tot.get(x["sector"], 0) / max(n.get(x["sector"], 1), 1), 1)
        moved.append(("C per action %s" % x["sector"], nat, x["per_action"],
                      abs(nat - x["per_action"]) > 0.05))
        natt = tot.get(x["sector"], 0)
        moved.append(("C total %s" % x["sector"], natt, x["total"],
                      abs(natt - x["total"]) >= 1))

    print("=" * 96)
    print("ASK FORCING, measured on the cut pack: the natural read against the golden")
    print("=" * 96)
    print("  %-34s %12s %12s %8s" % ("figure", "natural", "golden", "moved"))
    for label, nat, gold, ok_ in moved:
        print("  %-34s %12s %12s %8s" % (label, nat, gold, "yes" if ok_ else "NO"))
    hit = sum(1 for _, _, _, o in moved if o)
    print("\n  %d of %d sampled figures move beyond their stated rounding" % (hit, len(moved)))
    return 0 if hit == len(moved) else 1


if __name__ == "__main__":
    if "--forcing" in sys.argv:
        sys.exit(forcing())
    main()
