"""task199 pack builder: draws every row from core.py's parameters and writes target/.

    python3 task199/generator/build_pack.py --tune    # draw only, report counts and bin distances
    python3 task199/generator/build_pack.py           # draw and write the bundle

One RNG stream per city and month, so a change to one city's parameters cannot move another city's
rows, and two runs are byte identical. Nothing here is fixed first and reverse engineered: the rows
come from the parameters, and every graded figure is computed from the rows afterwards.
"""
import argparse
import csv
import json
import os
import random
import shutil
from datetime import date, timedelta

import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import core  # noqa: E402
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")

SEED = 199199
STEP = date(2026, 4, 1)              # every presence shift and the activity rise take effect here
WIN = (date(2026, 4, 1), date(2026, 9, 30))
BASE = (date(2024, 1, 1), date(2025, 12, 31))
FIRST = date(2024, 1, 1)
LAST = date(2026, 9, 30)
EXTRACT = date(2026, 11, 5)          # the definitive extract the designation runs on
PRELIM_MONTHS = ((2026, 5), (2026, 6), (2026, 7))   # both extracts in the 2026 export

# Shared seasonal shape, the same for every city, so it cannot move the ranking (asserted).
SEASON = {1: 0.88, 2: 0.93, 3: 1.02, 4: 1.07, 5: 1.09, 6: 1.05,
          7: 1.02, 8: 1.06, 9: 1.04, 10: 1.00, 11: 0.95, 12: 0.89}

# Layer 1 on the main path: the share of a month's actions that made the preliminary extract, and the
# share of actions that run more than one day (collapsed to one row with a day count from 2026).
PRELIM_SHARE = {"Valledupar": 0.78, "Barrancabermeja": 0.71, "Aguachica": 0.66, "Ocana": 0.84,
                "Tibu": 0.62, "Sardinata": 0.55, "El Tarra": 0.69, "Convencion": 0.95,
                "Teorama": 0.74, "San Calixto": 0.80, "Hacari": 0.58}
MULTIDAY = {"Valledupar": 0.12, "Barrancabermeja": 0.18, "Aguachica": 0.09, "Ocana": 0.11,
            "Tibu": 0.14, "Sardinata": 0.16, "El Tarra": 0.21, "Convencion": 0.08,
            "Teorama": 0.13, "San Calixto": 0.10, "Hacari": 0.15}

DIVIPOLA = {
    "Valledupar": "20001", "Barrancabermeja": "68081", "Aguachica": "20011", "Ocana": "54498",
    "Tibu": "54810", "Sardinata": "54720", "El Tarra": "54250", "Convencion": "54206",
    "Teorama": "54800", "San Calixto": "54670", "Hacari": "54344",
    "Abrego": "54003", "Rio de Oro": "20614", "La Playa": "54398", "Cachira": "54128",
    "Gonzalez": "20310", "La Esperanza": "54385", "Bucarasica": "54109", "El Carmen": "54245",
    "San Martin": "20770", "Curumani": "20228", "Chimichagua": "20175", "Pelaya": "20550",
}
# One municipality was re-coded when two were merged in the national list; the register's own city
# table carries both codes with effective dates, and three municipalities' 2025 rows sit under the
# retired code (ask B's hazard, all outside the panel).
RETIRED_CODE = {"La Esperanza": "54385", "Bucarasica": "54109", "Gonzalez": "20310"}
NEW_CODE = {"La Esperanza": "54386", "Bucarasica": "54110", "Gonzalez": "20311"}
CODE_EFFECTIVE = date(2025, 7, 1)

TIPOS = ["Bloqueo de via", "Marcha", "Paro", "Plantón", "Toma de entidad", "Asamblea permanente"]
SECTORES = ["Campesinado", "Transportadores", "Mineria artesanal", "Docentes",
            "Juntas comunales", "Comerciantes"]
SECTOR_NEW = ["Mujeres organizadas", "Juventudes"]      # added to the code list in 2025 (hazard H4)

# The outlet panel. type drives whether the service pushes or the register pulls, and the ambito is
# what the registry publishes; neither says anything about volumes.
OUTLETS = [
    ("RA-D01", "Diario del Nororiente", "diario", "regional"),
    ("RA-D02", "La Brujula de Ocana", "diario", "subregional"),
    ("RA-D03", "El Vigia del Zulia", "diario", "subregional"),
    ("RA-D04", "Catatumbo Hoy", "diario", "subregional"),
    ("RA-D05", "El Surco", "diario", "local"),
    ("RA-D06", "Diario del Cesar Medio", "diario", "regional"),
    ("RA-D07", "La Jornada del Magdalena", "diario", "regional"),
    ("RA-R01", "Radio Minuto Norte", "radio", "regional"),
    ("RA-R02", "Voces del Catatumbo", "radio", "subregional"),
    ("RA-R03", "Radio Sardinata", "radio", "local"),
    ("RA-R04", "Emisora Comunal Teorama", "radio", "local"),
    ("RA-R05", "Radio Rio de Oro", "radio", "local"),
    ("RA-R06", "Frecuencia Aguachica", "radio", "local"),
    ("RA-G01", "Portal Nororiente", "digital", "regional"),
    ("RA-G02", "Tibu al Dia", "digital", "local"),
    ("RA-G03", "Convencion Informa", "digital", "local"),
    ("RA-G04", "El Tarra Noticias", "digital", "local"),
    ("RA-G05", "Boletin Minero del Sur", "digital", "sectorial"),
    ("RA-G06", "Corredor Informativo", "digital", "regional"),
    ("RA-A01", "Agencia Andina de Prensa", "agencia", "nacional"),
    ("RA-A02", "Servicio Informativo Oriente", "agencia", "nacional"),
]
PUSHED = {"diario", "radio", "digital"}      # the service pushes these; agency feeds are pulled

# Which outlets file from which city, with the monthly item share and the month the pair starts.
# The risers gain pairs on STEP; nothing states that, and only the delivered volumes show it.
def pairs_for(city, idx):
    """A deterministic outlet assignment: a local core plus regionals, and new pairs for the risers."""
    rng = random.Random("pair|%s" % city)
    local = [o for o in OUTLETS if o[3] in ("local", "subregional")]
    regional = [o for o in OUTLETS if o[3] in ("regional", "sectorial")]
    agency = [o for o in OUTLETS if o[3] == "nacional"]
    n_local = 2 if city in [c[0] for c in core.PANEL] else 1
    chosen = rng.sample(local, n_local) + rng.sample(regional, 2) + [agency[idx % 2]]
    return chosen


def allocate_presence(city, base_month_items, riser_mult):
    """Split a city's monthly delivered items across its outlet pairs, and add the pairs that start
    on STEP so the city's total rises by riser_mult. Shares vary by outlet, never uniformly."""
    rng = random.Random("pres|%s" % city)
    idx = sorted(DIVIPOLA).index(city)
    chosen = pairs_for(city, idx)
    weights = [0.9 + rng.random() * 1.6 for _ in chosen]
    tot = sum(weights)
    out = [(o[0], base_month_items * w / tot, FIRST) for o, w in zip(chosen, weights)]
    if riser_mult > 1.0001:
        extra = base_month_items * (riser_mult - 1.0)
        pool = [o for o in OUTLETS if o[0] not in {c[0] for c in chosen}
                and o[3] in ("local", "subregional", "regional")]
        new = random.Random("new|%s" % city).sample(pool, 3)
        w2 = [1.0, 0.75, 0.55]
        s2 = sum(w2)
        out += [(o[0], extra * w / s2, STEP) for o, w in zip(new, w2)]
    return out


def months():
    out = []
    y, m = FIRST.year, FIRST.month
    while (y, m) <= (LAST.year, LAST.month):
        out.append((y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def month_days(y, m):
    nxt = date(y + (m == 12), 1 if m == 12 else m + 1, 1)
    return (nxt - date(y, m, 1)).days


def pois(rng, lam):
    if lam <= 0:
        return 0
    if lam > 40:
        return max(0, int(round(rng.gauss(lam, lam ** 0.5))))
    import math
    el, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= el:
            return k
        k += 1


def draw():
    """Every row of the world, from core.py's parameters. Returns the realised truth."""
    t = core.panel_truth()
    panel = {m[0]: m for m in core.PANEL}
    outside = dict(core.OUTSIDE)
    actions, citations, deliveries = [], [], []
    seq = {}

    def new_id(city, d):
        key = (DIVIPOLA[city][:2], d.year)
        seq[key] = seq.get(key, 0) + 1
        return "AC-%s-%d-%05d" % (key[0], d.year, seq[key])

    for (y, m) in months():
        first = date(y, m, 1)
        ndays = month_days(y, m)
        post = first >= STEP
        for city in list(panel) + list(outside):
            rng = random.Random("%s|%d-%02d|%d" % (city, y, m, SEED))
            if city in panel:
                nm, pop, lam0, pres0, p0, r0, lm, pm, rm = panel[city]
                lam = lam0 * (lm if post else 1.0) * SEASON[m]
                p = min(core.CAP, p0 * (pm if post else 1.0))
                r_mean = r0 * (rm if post else 1.0)
                pres = pres0 * (pm if post else 1.0) * (0.94 + 0.12 * SEASON[m])
                md = MULTIDAY[city]
            else:
                base = outside[city] / 9000.0
                lam = base * 6.0 * SEASON[m]
                p = 0.38
                r_mean = 1.4
                pres = max(40.0, outside[city] / 95.0) * (0.94 + 0.12 * SEASON[m])
                md = 0.12
            n = pois(rng, lam * p)
            for _ in range(n):
                d = first + timedelta(days=rng.randrange(ndays))
                days = 1
                if rng.random() < md:
                    days = 2 + pois(rng, 0.7)
                tipo = TIPOS[min(len(TIPOS) - 1, pois(rng, 1.6))]
                sect = (SECTOR_NEW[rng.randrange(2)]
                        if (y >= 2025 and rng.random() < 0.06) else SECTORES[min(5, pois(rng, 1.7))])
                # participants: a central estimate, except where the coder worked from a radio
                # transcript, which records a range and writes its lower bound in the numeric column
                scale = {"Bloqueo de via": 120, "Marcha": 260, "Paro": 420, "Plantón": 90,
                         "Toma de entidad": 70, "Asamblea permanente": 150}[tipo]
                real = max(8, int(scale * (0.45 + rng.random() * 1.5)))
                note, numeric = "", real
                if rng.random() < 0.22:                     # radio transcript coding
                    lo = int(real * (0.72 + rng.random() * 0.1))
                    hi = int(real * (1.18 + rng.random() * 0.12))
                    note = "entre %d y %d personas segun transcripcion" % (lo, hi)
                    numeric = lo
                    real = (lo + hi) // 2
                elif rng.random() < 0.09:
                    numeric, real, note = 0, None, "no reportado"
                reg_lag = 3 + pois(rng, 9)
                aid = new_id(city, d)
                actions.append(dict(
                    action_id=aid, city=city, date=d, days=days, tipo=tipo, sector=sect,
                    participantes=numeric, nota=note, truth_participants=real,
                    registered=d + timedelta(days=reg_lag),
                    r_mean=r_mean))
                ncit = 1 + pois(rng, max(0.0, r_mean - 1.0))
                for j in range(ncit):
                    citations.append(dict(action_id=aid, city=city,
                                          item_date=d + timedelta(days=rng.randrange(0, 3)),
                                          seq=j))
            # deliveries, at outlet x city x day
            alloc = allocate_presence(city, pres, (panel[city][7] if city in panel else 1.0))
            for (code, per_month, start) in alloc:
                if first < start:
                    continue
                active = max(1, int(round(ndays * (0.34 + 0.30 * rng.random()))))
                dayset = sorted(rng.sample(range(ndays), active))
                left = pois(rng, per_month)
                if left <= 0:
                    continue
                for i, dd in enumerate(dayset):
                    remaining = len(dayset) - i
                    give = max(1, int(round(left / remaining * (0.7 + 0.6 * rng.random()))))
                    give = min(give, left - (remaining - 1)) if remaining > 1 else left
                    if give <= 0:
                        continue
                    left -= give
                    deliveries.append(dict(date=first + timedelta(days=dd), outlet=code,
                                           city=city, delivered=give))
                    if left <= 0:
                        break
    # retained items: the items that reported an action, plus near misses the filter kept
    by_key = {}
    for c in citations:
        by_key.setdefault((c["city"], c["item_date"]), 0)
        by_key[(c["city"], c["item_date"])] += 1
    for row in deliveries:
        rng = random.Random("ret|%s|%s|%s" % (row["city"], row["date"], row["outlet"]))
        cited = by_key.get((row["city"], row["date"]), 0)
        share = min(row["delivered"], int(round(cited * 0.45)) + pois(rng, 0.25))
        row["retained"] = max(0, min(row["delivered"], share))
    return dict(actions=actions, citations=citations, deliveries=deliveries, truth=t)


def action_days(actions, city, lo, hi):
    return sum(a["days"] for a in actions
               if a["city"] == city and lo <= a["date"] <= hi)


def delivered(deliveries, city, lo, hi):
    return sum(r["delivered"] for r in deliveries
               if r["city"] == city and lo <= r["date"] <= hi)


def tune_population(count, planned, unit=0.1, floor=0.3):
    """Choose the published population so the graded rate sits at least `floor` of the printed unit
    from its bin edge, on a value that is not round and a population that is not round either: a
    projection of exactly 150,000 and a rate of exactly 40.0 both read as synthetic. The search is a
    deterministic scan over a narrow band around the planned projection."""
    best = None
    for pop in range(int(planned * 0.985), int(planned * 1.015)):
        if pop % 50 == 0:                       # a projection is never a round figure
            continue
        v = count / pop * 1e5
        printed = round(v, 1)
        if abs(printed - round(printed)) < 1e-9:  # never a round printed rate
            continue
        edge = unit / 2 - abs(v - round(v / unit) * unit)
        if edge < floor * unit:
            continue
        # prefer the value furthest from its bin edge, then the population closest to the plan
        key = (round(edge, 6), -abs(pop - planned))
        if best is None or key > (round(best[1], 6), -abs(best[0] - planned)):
            best = (pop, edge, v)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tune", action="store_true")
    args = ap.parse_args()
    d = draw()
    a, c, dv = d["actions"], d["citations"], d["deliveries"]
    print("drawn: %d actions, %d citations, %d delivery rows" % (len(a), len(c), len(dv)))
    panel = [m[0] for m in core.PANEL]
    print()
    print("%-17s %8s %8s %9s %9s %8s" % ("city", "base ad", "win ad", "base del", "win del", "rise"))
    rows = {}
    for city in panel:
        ab = action_days(a, city, *BASE)
        aw = action_days(a, city, *WIN)
        vb = delivered(dv, city, *BASE)
        vw = delivered(dv, city, *WIN)
        rise = (aw / 6.0) / (ab / 24.0)
        dec = ((aw / vw) / (ab / vb))
        rows[city] = dict(ab=ab, aw=aw, vb=vb, vw=vw, rise=rise, dec=dec)
        print("%-17s %8d %8d %9d %9d %8.3f" % (city, ab, aw, vb, vw, rise))
    print()
    print("default path ranking:", ", ".join(
        "%s %.3f" % (k, rows[k]["rise"]) for k in sorted(rows, key=lambda k: -rows[k]["rise"])[:5]))
    print("decisive ranking:    ", ", ".join(
        "%s %.3f" % (k, rows[k]["dec"]) for k in sorted(rows, key=lambda k: -rows[k]["dec"])[:5]))
    print()
    print("population tuning, so every graded rate clears 0.3 of the printed unit:")
    planned = {m[0]: m[1] for m in core.PANEL}
    pops = {}
    for city in panel:
        pop, edge, v = tune_population(rows[city]["aw"], planned[city])
        pops[city] = pop
        print("  %-17s count %4d  pop %7d  rate %8.3f prints %6.1f  edge %.4f = %.2f u"
              % (city, rows[city]["aw"], pop, v, round(v, 1), edge, edge / 0.1))
    json.dump({"populations": pops}, open(os.path.join(HERE, "populations.json"), "w"), indent=1)
    if args.tune:
        return
    print("\n(writing the bundle is the next step in this module)")


if __name__ == "__main__":
    main()
