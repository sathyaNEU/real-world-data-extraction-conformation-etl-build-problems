"""Design-time screen of the three asks on a cut pack: the golden and each mishandling, ward by ward."""
import sys

import solve as S


def table(name, rows):
    wards = sorted({w for r in rows.values() for w in r if w})
    print("== %s" % name)
    print("%-22s %s" % ("", " ".join("%9s" % w[:9] for w in wards)))
    for k, r in rows.items():
        diff = sum(1 for w in wards if r.get(w, 0) != rows["golden"].get(w, 0))
        print("%-22s %s  (%d off)" % (k, " ".join("%9s" % r.get(w, 0) for w in wards), diff))


def variants(t, G=None):
    G = G or S.golden(t)
    reg, wo, recs = G["S"]["reg"], G["S"]["ward_of"], G["S"]["recs"]
    A = {"golden": G["supply"],
         "blank lost as 0": S.ask_supply(t, reg, wo, recs, infer_lost=False, blank_lost=0),
         "blank lost as 1": S.ask_supply(t, reg, wo, recs, infer_lost=False, blank_lost=1),
         "every certificate": S.ask_supply(t, reg, wo, recs, dedupe=False),
         "both": S.ask_supply(t, reg, wo, recs, dedupe=False, infer_lost=False)}
    B = {"golden": G["company_money"],
         "every title": S.ask_company(t, recs, wo, group=False)[1],
         "same-day pairs one": S.ask_company(t, recs, wo, rule="2")[1],
         "same-day threes one": S.ask_company(t, recs, wo, rule="3")[1],
         "no update": S.ask_company(t, S.load_ppd(t, apply_update=False), wo)[1]}
    C = {"golden": G["starts"],
         "every claim": S.ask_starts(t, wo, dedupe=False),
         "exact repeats only": S.ask_starts(t, wo, exact_only=True),
         "withdrawn kept": S.ask_starts(t, wo, statuses=("Paid", "Approved", "Withdrawn"))}
    return A, B, C


def main(t):
    G = S.golden(t)
    A, B, C = variants(t, G)
    table("Ask A net additional dwellings", A)
    table("Ask B money paid", B)
    table("Ask C homes started", C)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else S.TARGET)
