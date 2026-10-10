"""The municipal register (padró) deliveries for the watch-list sections, June and September 2026.

València and Alacant deliver one row per registered person; Castelló de la Plana one row per dwelling
with the number of persons registered. The September delivery lacks València districts 11 and 12 and
Alacant district 2, whose latest delivery is June's. Registrations of non-EU nationals without
permanent residence lapse two years after their alta or last renewal.
"""
import datetime as dt
import random

from common import D, SEED
from plan import SECTIONS

HEADER = ["codi_municipi", "districte", "seccio_censal", "referencia_cadastral", "id_inscripcio",
          "tipus_document", "nacionalitat", "data_alta", "data_ultima_renovacio", "persones"]
JUNE, SEPT = D(2026, 6, 1), D(2026, 9, 1)
MISSING_SEPT = {("46250", "11"), ("46250", "12"), ("03014", "02")}
NAT_UE = ["ROU", "ITA", "BGR", "FRA", "DEU", "PRT", "POL", "NLD", "BEL"]
NAT_X = ["COL", "MAR", "VEN", "UKR", "ARG", "ECU", "PER", "CHN", "HND", "PAK", "SEN", "DZA", "BOL", "CUB", "RUS"]


def build(stock, golden, june_lh, touched, seed=SEED * 59 + 13):
    """golden: ref -> holder on 1 Jan 2027 (R5); june_lh: refs held by large holders on 30 June 2026;
    touched: refs that must read as occupied by valid registrations (the agency's commitments, the twins)."""
    rng = random.Random(seed)
    sections, buildings, dwellings = stock
    ids = set()

    def pid():
        while True:
            x = f"I{rng.randrange(16 ** 9):09x}".upper()
            if x not in ids:
                ids.add(x)
                return x

    def person(kind):
        """kind: es, ue, tp (permanent), tv (temporary, valid), tl (temporary, lapsed)."""
        alta = D(2026, 5, 20) - dt.timedelta(days=rng.randrange(30, 6000))
        if kind == "es":
            return ("DNI", "ESP", alta, None)
        if kind == "ue":
            return ("NIE", rng.choice(NAT_UE), alta, None)
        if kind == "tp":
            return ("TIE-P", rng.choice(NAT_X), alta, None)
        if kind == "tv":
            last = D(2025, 2, 3) + dt.timedelta(days=rng.randrange(0, 470))
            alta = min(alta, last)
            return (rng.choice(["TIE-T", "PAS"]), rng.choice(NAT_X), alta, last if last > alta else None)
        last = D(2022, 6, 1) + dt.timedelta(days=rng.randrange(0, 690))
        alta = min(alta, last)
        return (rng.choice(["TIE-T", "PAS"]), rng.choice(NAT_X), alta, last if last > alta else None)

    def household(valid_only=False, foreign=False):
        n = rng.choice([1, 1, 2, 2, 2, 3, 3, 4, 5])
        out = []
        for i in range(n):
            x = rng.random()
            if foreign and i == 0:
                k = "tv"
            elif valid_only:
                k = "es" if x < 0.85 else "ue"
            else:
                k = "es" if x < 0.74 else ("ue" if x < 0.84 else ("tp" if x < 0.91 else ("tv" if x < 0.97 else "tl")))
            out.append(person(k))
        if not valid_only and all(p[0] in ("TIE-T", "PAS") and (p[3] or p[2]) < D(2024, 6, 1) for p in out):
            out.append(person("es"))
        return out

    plan = {s["code"]: s for s in SECTIONS}
    occ_jun, occ_sep = {}, {}
    status = {}
    for code in sorted(plan):
        s = plan[code]
        e_plain, e_lapsed = s["vac"]
        refs = sorted(r for r, d in dwellings.items() if d["section"] == code)
        lh = [r for r in refs if r in golden and r not in touched]
        rng.shuffle(lh)
        empty = lh[:e_plain]
        lapsed = lh[e_plain:e_plain + e_lapsed]
        foreign = lh[e_plain + e_lapsed:e_plain + e_lapsed + 4]
        for r in refs:
            if r in empty:
                status[r] = "empty"
            elif r in lapsed:
                status[r] = "lapsed"
            elif r in foreign:
                status[r] = "foreign"
            elif r in touched:
                status[r] = "valid"
            elif r in golden:
                status[r] = "occ"
            elif r in june_lh:
                status[r] = "empty" if rng.random() < 0.3 else "occ"
            else:
                status[r] = "empty" if rng.random() < 0.07 else "occ"
        for r in refs:
            st = status[r]
            if st == "empty":
                h = []
            elif st == "lapsed":
                h = [person("tl") for _ in range(rng.choice([1, 1, 2]))]
            elif st == "foreign":
                h = household(foreign=True)
            elif st == "valid":
                h = household(valid_only=True)
            else:
                h = household()
            occ_sep[r] = h
            if (code[:5], code[5:7]) in MISSING_SEPT:
                occ_jun[r] = list(h)
                continue
            # June: a few households moved between the two deliveries (never the graded ones' status)
            if st == "occ" and rng.random() < 0.03:
                occ_jun[r] = []
            elif st == "empty" and r not in golden and rng.random() < 0.15:
                occ_jun[r] = household()
            elif st == "empty" and r in golden and rng.random() < 0.25 and (code[:5], code[5:7]) not in MISSING_SEPT:
                occ_jun[r] = household(valid_only=True)
            else:
                occ_jun[r] = [p for p in h]
    rows = {"06": [], "09": []}
    for which, occ, day in (("06", occ_jun, JUNE), ("09", occ_sep, SEPT)):
        for code in sorted(plan):
            muni, dist = code[:5], code[5:7]
            if which == "09" and (muni, dist) in MISSING_SEPT:
                continue
            refs = sorted(r for r, d in dwellings.items() if d["section"] == code)
            for r in refs:
                h = occ[r]
                if muni == "12040":
                    rows[which].append([muni, dist, code, r, "", "", "", "", "", str(len(h))])
                    continue
                for p in sorted(h, key=lambda p: (p[2], p[1])):
                    rows[which].append([muni, dist, code, r, pid(), p[0], p[1], p[2].isoformat(),
                                        p[3].isoformat() if p[3] else "", ""])
    return rows, status
