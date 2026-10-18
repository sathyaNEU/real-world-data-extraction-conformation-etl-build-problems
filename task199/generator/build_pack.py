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

SEED = 230875        # the first seed of a 40-seed scan to clear every stage-3 floor (3 of 40 did)
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
                "Tibu": 0.62, "Sardinata": 0.95, "El Tarra": 0.69, "Convencion": 0.58,
                "Teorama": 0.74, "San Calixto": 0.80, "Hacari": 0.61}
MEAN_EXTRA_DAYS = 1.7      # mean extra days of an action that runs more than one
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


RANGE_FORMS = [
    "entre %d y %d personas segun transcripcion",
    "la emisora reporta de %d a %d asistentes",
    "transcripcion: %d a %d participantes",
    "se escucha entre %d y %d personas en el audio",
    "fuente radial, %d-%d personas",
]


def render_range(action_id, lo, hi):
    """The coder's own wording, stable per entry and taken from the id rather than the draw, so the
    note's text cannot move any count."""
    h = sum((i + 1) * ord(ch) for i, ch in enumerate(action_id))
    return RANGE_FORMS[h % len(RANGE_FORMS)] % (lo, hi)


def draw(seed=SEED):
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
            rng = random.Random("%s|%d-%02d|%d" % (city, y, m, seed))
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
                rng_lo = rng_hi = None
                if rng.random() < 0.22:                     # radio transcript coding
                    lo = int(real * (0.72 + rng.random() * 0.1))
                    hi = int(real * (1.18 + rng.random() * 0.12))
                    rng_lo, rng_hi = lo, hi
                    note = "RANGE"                          # rendered below, per coder
                    numeric = lo
                    real = (lo + hi) // 2
                elif rng.random() < 0.09:
                    numeric, real, note = 0, None, "no reportado"
                reg_lag = 3 + pois(rng, 9)
                aid = new_id(city, d)
                if note == "RANGE":
                    note = render_range(aid, rng_lo, rng_hi)
                actions.append(dict(
                    action_id=aid, city=city, date=d, days=days, tipo=tipo, sector=sect,
                    participantes=numeric, nota=note, truth_participants=real,
                    rango=(rng_lo, rng_hi), registered=d + timedelta(days=reg_lag),
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
    """Gathering-days counted on their own dates, which is what the manual's unit says and what the
    exports hold: before 2026 each day of a prolonged action has its own row and its own date, and
    from 2026 the day count expands the same way. An action that starts inside the window and runs
    past its end contributes only the days inside."""
    n = 0
    for a in actions:
        if a["city"] != city:
            continue
        for k in range(a["days"]):
            if lo <= a["date"] + timedelta(days=k) <= hi:
                n += 1
    return n


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


def rungs(d):
    """Every rung's score per city, computed from the drawn rows, plus the winners."""
    a, dv, ct = d["actions"], d["deliveries"], d["citations"]
    panel = [m[0] for m in core.PANEL]
    cits = {}
    for c in ct:
        for span, (lo, hi) in (("b", BASE), ("w", WIN)):
            if lo <= c["item_date"] <= hi:
                cits[(c["city"], span)] = cits.get((c["city"], span), 0) + 1
    out = {}
    for city in panel:
        ab, aw = action_days(a, city, *BASE), action_days(a, city, *WIN)
        # rows as the exports hold them: the 2026 export collapses a multi-day action into one row
        # and holds both extracts for three months, so the window's rows are neither action-days nor
        # a clean count
        rows_w = sum(1 for x in a if x["city"] == city and WIN[0] <= x["date"] <= WIN[1])
        dup = sum(1 for x in a if x["city"] == city and WIN[0] <= x["date"] <= WIN[1]
                  and (x["date"].year, x["date"].month) in PRELIM_MONTHS
                  and x["registered"] <= date(x["date"].year, x["date"].month, 28))
        rows_w += int(round(dup * PRELIM_SHARE[city]))
        vb, vw = delivered(dv, city, *BASE), delivered(dv, city, *WIN)
        kb = cits.get((city, "b"), 1)
        kw = cits.get((city, "w"), 1)
        out[city] = dict(
            rung0=(rows_w / 6.0) / (ab / 24.0),
            rung1=(aw / 6.0) / (ab / 24.0),
            rung2=((aw / kw) / (ab / kb)) if kw and kb else 0.0,
            rung3=((aw / vw) / (ab / vb)),
            aw=aw, ab=ab, vw=vw, vb=vb)
    return out


def evaluate(d):
    """The stage-3 floors, as a verdict on one drawn pack."""
    r = rungs(d)
    g = core.GOLDEN
    order = {k: sorted(r, key=lambda c: -r[c][k]) for k in ("rung0", "rung1", "rung2", "rung3")}
    win = {k: order[k][0] for k in order}
    second = {k: order[k][1] for k in order}
    pos_default = order["rung1"].index(g) + 1
    margin = r[g]["rung3"] / r[second["rung3"]]["rung3"]
    lead = r[win["rung1"]]["rung1"] / r[g]["rung1"]
    distinct = len({win["rung0"], win["rung1"], win["rung2"], g}) == 4
    ok = (pos_default in (4, 5) and margin >= 1.30 and lead >= 1.20 and distinct
          and win["rung2"] == "Teorama" and win["rung3"] == g)
    return ok, dict(pos_default=pos_default, margin=margin, lead=lead, distinct=distinct,
                    winners={k: win[k] for k in win}, runner_up=second["rung3"], rungs=r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tune", action="store_true")
    ap.add_argument("--seedsearch", type=int, default=0,
                    help="scan this many seeds and report the first that clears every floor")
    args = ap.parse_args()
    if args.seedsearch:
        found = []
        for k in range(args.seedsearch):
            sd = SEED + k * 7919
            ok, info = evaluate(draw(sd))
            if ok:
                found.append((sd, info))
                print("  seed %-10d PASS  golden %dth, decisive margin %.3fx, leader %.2fx, "
                      "rungs %s" % (sd, info["pos_default"], info["margin"], info["lead"],
                                    " ".join("%s=%s" % (k2, v) for k2, v in info["winners"].items())))
                if len(found) >= 3:
                    break
        if not found:
            print("  no seed in the scan cleared every floor")
        else:
            print("\n  chosen: the first qualifying seed, %d" % found[0][0])
        return
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
    write_pack(d, pops)




# =============================================================== writing the bundle

ISSUE = date(2026, 11, 5)            # every file's mtime, the extract date
DESKS = {}                           # city -> the desk seat the monthly summary rolls it into


def desk_seat(city):
    """The service seats each desk in one municipality and the desk serves a pair of them, which is
    what the register's published monthly summary rolls up by (ask B's primary)."""
    if not DESKS:
        pairs = [("Abrego", "La Playa"), ("Rio de Oro", "Gonzalez"), ("Cachira", "Bucarasica"),
                 ("La Esperanza", "El Carmen"), ("San Martin", "Pelaya"),
                 ("Curumani", "Chimichagua")]
        for seat, partner in pairs:
            DESKS[seat] = seat
            DESKS[partner] = seat
    return DESKS.get(city, city)


def code_for(city, when):
    """The national code list merged two municipalities in July 2025 and reissued three codes."""
    if city in RETIRED_CODE and when >= CODE_EFFECTIVE:
        return NEW_CODE[city]
    return DIVIPOLA[city]


def w_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(header)
        wr.writerows(rows)


def write_register(d):
    """Three yearly exports. The 2025 export carries the office's renamed columns and day-first
    dates; the 2026 export carries the day count the template gained and both extracts for three
    months. One row per gathering-day before 2026, one row per action with its day count after."""
    a = sorted(d["actions"], key=lambda x: (x["date"], x["action_id"]))
    for year in (2024, 2025, 2026):
        rows = []
        for x in a:
            if x["date"].year != year:
                continue
            reg = x["registered"]
            if year == 2026:
                rows.append([x["action_id"], x["date"].isoformat(), x["city"],
                             code_for(x["city"], x["date"]), x["tipo"], x["sector"], x["days"],
                             "" if x["participantes"] is None else x["participantes"], x["nota"],
                             reg.isoformat(), "definitivo"])
            elif year == 2025:
                for k in range(x["days"]):
                    rows.append(["%s-%d" % (x["action_id"], k + 1) if x["days"] > 1 else x["action_id"],
                                 (x["date"] + timedelta(days=k)).strftime("%d/%m/%Y"), x["city"],
                                 code_for(x["city"], x["date"]), x["tipo"], x["sector"],
                                 "" if x["participantes"] is None else x["participantes"],
                                 x["nota"], reg.strftime("%d/%m/%Y")])
            else:
                for k in range(x["days"]):
                    rows.append(["%s-%d" % (x["action_id"], k + 1) if x["days"] > 1 else x["action_id"],
                                 (x["date"] + timedelta(days=k)).isoformat(), x["city"],
                                 code_for(x["city"], x["date"]), x["tipo"], x["sector"],
                                 "" if x["participantes"] is None else x["participantes"],
                                 x["nota"], reg.isoformat()])
        if year == 2026:
            # the preliminary extract of three months, held beside the definitive one
            extra = []
            for x in a:
                if (x["date"].year, x["date"].month) not in PRELIM_MONTHS:
                    continue
                if x["registered"] > date(x["date"].year, x["date"].month, 28):
                    continue
                rng = random.Random("prelim|%s" % x["action_id"])
                if rng.random() > PRELIM_SHARE.get(x["city"], 0.7):
                    continue
                extra.append([x["action_id"], x["date"].isoformat(), x["city"],
                              code_for(x["city"], x["date"]), x["tipo"], x["sector"], x["days"],
                              "" if x["participantes"] is None else x["participantes"], x["nota"],
                              x["registered"].isoformat(), "preliminar"])
            rows = sorted(rows + extra, key=lambda r: (r[1], r[10], r[0]))
            w_csv(os.path.join(TARGET, "rac_acciones_2026.csv"),
                  ["action_id", "fecha_accion", "municipio", "divipola", "tipo_accion",
                   "sector_actor", "dias", "participantes_est", "nota_registro", "fecha_registro",
                   "extracto"], rows)
        elif year == 2025:
            w_csv(os.path.join(TARGET, "rac_acciones_2025.csv"),
                  ["id_accion", "fecha_de_accion", "municipio", "cod_divipola", "tipo", "sector",
                   "participantes", "nota", "fecha_de_registro"], rows)
        else:
            w_csv(os.path.join(TARGET, "rac_acciones_2024.csv"),
                  ["action_id", "fecha_accion", "municipio", "divipola", "tipo_accion",
                   "sector_actor", "participantes_est", "nota_registro", "fecha_registro"], rows)
    return True


PANEL_NAMES = {m[0] for m in core.PANEL}


def publication_period(city, when):
    """The month the items on a delivery row were published. The service delivers the first days of a
    month's batch after the month turns, so some rows carry the month before. For the panel that
    happens only in 2026 Q1, which falls in neither the baseline nor the designation window; for the
    municipalities outside the panel it happens through 2025, which is what the invoices bill on."""
    prev = (when.replace(day=1) - timedelta(days=1))
    rng = random.Random("pub|%s|%s" % (city, when))
    if city in PANEL_NAMES:
        if when.year == 2026 and when.month in (1, 2, 3) and when.day <= 3 and rng.random() < 0.55:
            return prev
    else:
        if when.day <= 4 and rng.random() < 0.42:
            return prev
    return when


def write_deliveries(d):
    """The spine: one row per outlet, municipality and day on which the service delivered material.
    items_entregados is everything it delivered from that dateline, items_retenidos the part the
    register's filter kept for screening, and periodo_publicacion the month the items were published.
    The 2026 rows carry the service's renumbered desk codes."""
    rows = []
    for r in sorted(d["deliveries"], key=lambda x: (x["date"], x["outlet"], x["city"])):
        code = r["outlet"] if r["date"].year < 2026 else "RSA-" + r["outlet"]
        lote = "L%s%02d%02d" % (str(r["date"].year)[2:], r["date"].month, r["date"].day)
        pub = publication_period(r["city"], r["date"])
        rows.append([r["date"].isoformat(), code, r["city"], code_for(r["city"], r["date"]),
                     r["delivered"], r["retained"], "%d-%02d" % (pub.year, pub.month), lote])
    w_csv(os.path.join(TARGET, "envios_resena_andina.csv"),
          ["fecha_envio", "codigo_fuente", "municipio_fecha", "cod_divipola", "items_entregados",
           "items_retenidos", "periodo_publicacion", "lote"], rows)
    return len(rows)


def invoice_lines(d):
    """What the service billed for 2025, by desk and publication period, for the municipalities
    outside the panel. The invoice bills the period the items were published in, so a quarter's
    billed items are not the quarter's delivered rows; a credit note covers a batch the register
    rejected wholesale in August."""
    by = {}
    for r in d["deliveries"]:
        if r["city"] in PANEL_NAMES or r["date"].year != 2025:
            continue
        pub = publication_period(r["city"], r["date"])
        key = (desk_seat(r["city"]), pub.year, pub.month)
        by[key] = by.get(key, 0) + r["delivered"]
    lines = []
    for (seat, y, m), items in sorted(by.items()):
        if y != 2025:
            continue
        rate = 2.35 if seat in ("Abrego", "Curumani") else 2.10
        lines.append((seat, m, items, round(items * rate, 1)))
    return lines


def write_citations(d):
    rows = []
    for c in sorted(d["citations"], key=lambda x: (x["item_date"], x["action_id"], x["seq"])):
        rng = random.Random("cite|%s|%d" % (c["action_id"], c["seq"]))
        pool = [o[0] for o in OUTLETS]
        rows.append([c["action_id"], pool[rng.randrange(len(pool))], c["item_date"].isoformat(),
                     "IT-%s-%04d" % (c["item_date"].isoformat().replace("-", ""), rng.randrange(10000))])
    w_csv(os.path.join(TARGET, "citas_rac.csv"),
          ["id_accion", "codigo_fuente", "fecha_item", "id_item"], rows)
    return len(rows)


def write_summary(d):
    """The register's published monthly summary for 2025. It is built from the desks' returns, so a
    desk serving two municipalities reports both under its seat: the seat stands above its own parts
    and the partner below. Panel cities have their own desk, so their rows agree with the detail."""
    a = d["actions"]
    agg = {}
    for x in a:
        seat = desk_seat(x["city"])
        for k in range(x["days"]):
            dt = x["date"] + timedelta(days=k)      # a gathering-day falls in its own month
            if dt.year != 2025:
                continue
            key = (seat, dt.month)
            agg[key] = agg.get(key, 0) + 1
    rows = [[seat, DIVIPOLA[seat], 2025, m, n] for (seat, m), n in
            sorted(agg.items(), key=lambda kv: (kv[0][0], kv[0][1]))]
    w_csv(os.path.join(TARGET, "resumen_mensual_rac_2025.csv"),
          ["municipio_sede", "divipola_sede", "anio", "mes", "acciones_dia"], rows)
    return len(rows)


def write_lookups(pops):
    rows = []
    for city in sorted(DIVIPOLA):
        if city in RETIRED_CODE:
            rows.append([city, RETIRED_CODE[city], "2015-01-01", (CODE_EFFECTIVE - timedelta(days=1)).isoformat(), "retirado"])
            rows.append([city, NEW_CODE[city], CODE_EFFECTIVE.isoformat(), "", "vigente"])
        else:
            rows.append([city, DIVIPOLA[city], "2015-01-01", "", "vigente"])
    w_csv(os.path.join(TARGET, "tabla_municipios.csv"),
          ["municipio", "cod_divipola", "vigente_desde", "vigente_hasta", "estado"], rows)
    # distractor 1: a department-level social listening index, 2026 only
    rng = random.Random("redes")
    rows = []
    for dep in ("Norte de Santander", "Cesar", "Santander"):
        for m in range(1, 10):
            rows.append([dep, 2026, m, round(60 + rng.random() * 70, 1), rng.randrange(900, 4200)])
    w_csv(os.path.join(TARGET, "indice_menciones_redes.csv"),
          ["departamento", "anio", "mes", "indice_menciones", "cuentas_activas"], rows)
    # distractor 2: the transport authority's road incidents
    rng = random.Random("vial")
    rows = []
    for city in sorted(DIVIPOLA):
        for (y, m) in months():
            if y == 2023:
                continue
            rows.append([city, DIVIPOLA[city], "%d-%02d" % (y, m), rng.randrange(0, 9),
                         rng.randrange(0, 4)])
    w_csv(os.path.join(TARGET, "incidencias_viales.csv"),
          ["municipio", "cod_divipola", "periodo", "incidentes_registrados", "cierres_programados"], rows)
    return True


# ------------------------------------------------------------------ workbooks

def write_workbooks(pops):
    import openpyxl
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for tipo, title in (("diario", "Prensa diaria"), ("radio", "Radio"),
                        ("digital", "Portales"), ("agencia", "Agencias")):
        ws = wb.create_sheet(title)
        ws.append(["Codigo", "Medio", "Tipo", "Ambito declarado", "Canal de entrega"])
        for code, name, t, amb in OUTLETS:
            if t != tipo:
                continue
            ws.append([code, name, t, amb, "primario" if t in PUSHED else "consulta"])
        ws.column_dimensions["B"].width = 30
    ws = wb.create_sheet("Notas")
    ws.append(["Panel vigente al 5 de noviembre de 2026. El ambito declarado es el que cada medio"])
    ws.append(["reporta en su ficha; no describe el volumen que remite."])
    ws.append(["Las fichas se revisan al cierre de cada semestre."])
    wb.save(os.path.join(TARGET, "panel_fuentes.xlsx"))

    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    ws = wb.create_sheet("Proyeccion 2026 unidades")
    ws.append(["Municipio", "Cod DIVIPOLA", "Proyeccion 2026", "Vigencia"])
    for city in sorted(pops):
        ws.append([city, DIVIPOLA[city], pops[city], "2026"])
    ws2 = wb.create_sheet("Proyeccion 2026 miles")
    ws2.append(["Municipio", "Cod DIVIPOLA", "Proyeccion 2026 (miles)", "Vigencia"])
    for city in sorted(pops):
        ws2.append([city, DIVIPOLA[city], round(pops[city] / 1000.0, 3), "2026"])
    ws3 = wb.create_sheet("Serie 2018-2024")
    ws3.append(["Municipio", "Cod DIVIPOLA", "Anio", "Proyeccion"])
    for city in sorted(pops):
        for y in range(2018, 2025):
            ws3.append([city, DIVIPOLA[city], y,
                        int(pops[city] * (1 - 0.0042 * (2026 - y)))])
    ws4 = wb.create_sheet("Notas")
    ws4.append(["Proyecciones municipales de poblacion, vigencia 2026, publicadas en la serie"])
    ws4.append(["posterior al censo. La hoja en miles se conserva para los informes que la citan."])
    wb.save(os.path.join(TARGET, "proyecciones_poblacion.xlsx"))


# ---------------------------------------------------------------- documents

def pdf(path, title, blocks):
    """A short operational document: a heading, numbered clauses and small tables. The library runs in
    invariant mode so the bytes carry a fixed date and no random identifiers, and postprocess then
    replaces that date with the document's own issue stamp."""
    from reportlab import rl_config
    rl_config.invariant = 1
    rl_config.useA85 = 0
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["BodyText"], fontName="Times-Roman", fontSize=9.5,
                          leading=12.5, spaceAfter=5)
    head = ParagraphStyle("h", parent=ss["Heading2"], fontName="Times-Bold", fontSize=11,
                          leading=14, spaceBefore=8, spaceAfter=4)
    t1 = ParagraphStyle("t", parent=ss["Title"], fontName="Times-Bold", fontSize=13, leading=16)
    doc = SimpleDocTemplate(path, pagesize=A4, title=title, author="",
                            leftMargin=22 * mm, rightMargin=22 * mm,
                            topMargin=20 * mm, bottomMargin=18 * mm)
    flow = [Paragraph(title, t1), Spacer(1, 6)]
    for kind, payload in blocks:
        if kind == "h":
            flow.append(Paragraph(payload, head))
        elif kind == "p":
            flow.append(Paragraph(payload, body))
        elif kind == "t":
            tb = Table(payload, hAlign="LEFT")
            tb.setStyle(TableStyle([
                ("FONT", (0, 0), (-1, -1), "Times-Roman", 8.5),
                ("FONT", (0, 0), (-1, 0), "Times-Bold", 8.5),
                ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 2)]))
            flow.append(tb)
            flow.append(Spacer(1, 6))
    doc.build(flow)


def write_protocol():
    pdf(os.path.join(TARGET, "protocolo_designacion.pdf"),
        "Protocolo de designacion semestral y mision de verificacion",
        [("p", "Observatorio Territorial del Nororiente. Version 4, aprobada el 12 de febrero de 2026. "
               "Reemplaza la version 3 de julio de 2024."),
         ("h", "2. Panel de seguimiento"),
         ("p", "2.1 El panel comprende once municipios: Valledupar, Barrancabermeja, Aguachica, "
               "Ocana, Tibu, Sardinata, El Tarra, Convencion, Teorama, San Calixto y Hacari. El "
               "registro cubre los demas municipios del corredor sin que les aplique este protocolo."),
         ("p", "2.2 Un municipio entra al panel al inicio de un semestre y permanece mientras el "
               "Observatorio mantenga seguimiento continuo de sus fuentes."),
         ("h", "3. Extractos y cierre"),
         ("p", "3.1 El registro publica un extracto preliminar al final de cada mes y un extracto "
               "definitivo treinta dias despues del cierre del mes. El extracto definitivo reemplaza "
               "al preliminar para todos los efectos de este protocolo."),
         ("p", "3.2 La designacion se calcula sobre el extracto definitivo del 5 de noviembre de 2026, "
               "posterior al cierre definitivo de todos los meses del semestre evaluado."),
         ("h", "4. Designacion"),
         ("p", "4.1 La designacion se refiere a un aumento de la actividad de protesta del municipio. "
               "Los registros del Observatorio son la evidencia de esa actividad y no su medida."),
         ("p", "4.2 Para el semestre del 1 de abril al 30 de septiembre de 2026, ambos dias incluidos, "
               "se compara cada municipio del panel con lo que su propio registro de los veinticuatro "
               "meses terminados el 31 de diciembre de 2025 implica para un semestre, contando las "
               "acciones por su fecha de ocurrencia."),
         ("p", "4.3 Es elegible el municipio del panel que registre al menos treinta acciones en el "
               "semestre y que haya pertenecido al panel durante todo el periodo de comparacion."),
         ("p", "4.4 Se designa un municipio por semestre. Si dos municipios resultan equivalentes, se "
               "designa el de mayor aumento absoluto de acciones."),
         ("p", "4.5 La nota de vigilancia publica, para el municipio designado, su tasa de acciones "
               "registradas por 100.000 habitantes del semestre, tomada de la proyeccion de poblacion "
               "vigente para 2026."),
         ("h", "5. Mision de verificacion"),
         ("p", "5.1 El Observatorio financia una mision de verificacion por semestre. La mision viaja "
               "al municipio designado, trabaja los archivos locales y entrevista a las organizaciones "
               "involucradas."),
         ("p", "5.2 La coordinacion de campo asigna la mision dentro de las tres semanas siguientes a "
               "la publicacion de la nota.")])


def write_manual():
    pdf(os.path.join(TARGET, "manual_codificacion.pdf"),
        "Manual de codificacion de acciones colectivas",
        [("p", "Observatorio Territorial del Nororiente. Edicion 7, enero de 2026. Uso interno del "
               "equipo de codificacion."),
         ("h", "1. Que es una entrada"),
         ("p", "1.1 Existe una entrada cuando ocurrio una accion y una fuente monitoreada remitio una "
               "cuenta de ella. El codificador no abre entrada por una accion de la que no haya "
               "llegado cuenta, ni por una cuenta que no describa una accion."),
         ("p", "1.2 La unidad es una concentracion, en un dia, en un lugar. Una jornada que se repite "
               "al dia siguiente en el mismo lugar se codifica como dos acciones."),
         ("h", "2. Campos"),
         ("p", "2.1 Hasta la plantilla de 2025 cada dia de una accion prolongada ocupaba su propia "
               "fila. La plantilla de 2026 incorpora el campo dias: la fila describe la accion y el "
               "campo indica cuantos dias corrio."),
         ("p", "2.2 El campo participantes_est registra una estimacion central. Cuando la fuente "
               "reporta un rango, el codificador transcribe el rango en la nota."),
         ("p", "2.3 El campo sector_actor toma su valor de la lista vigente. La lista se amplio en "
               "2025 con dos sectores."),
         ("h", "3. Revision"),
         ("p", "3.1 El equipo revisa una muestra de entradas cada mes y corrige la que no cumpla 1.1."),
         ("t", [["Campo", "Plantilla 2024", "Plantilla 2025", "Plantilla 2026"],
                ["fecha de accion", "si", "si", "si"],
                ["dias", "no", "no", "si"],
                ["extracto", "no", "no", "si"],
                ["nota_registro", "si", "si", "si"]])])


def write_bulletin(d):
    """The quarterly bulletin, through 2026 Q1: counts the register published for closed quarters.
    It designates nobody and stops before the window the designation covers."""
    a = d["actions"]
    rows = [["Municipio", "2025 T3", "2025 T4", "2026 T1"]]
    for city in [m[0] for m in core.PANEL]:
        cells = []
        for (y, q) in ((2025, 3), (2025, 4), (2026, 1)):
            lo = date(y, 3 * q - 2, 1)
            hi = date(y + (q == 4), 1 if q == 4 else 3 * q + 1, 1) - timedelta(days=1)
            cells.append(sum(x["days"] for x in a if x["city"] == city and lo <= x["date"] <= hi))
        rows.append([city] + [str(c) for c in cells])
    tipo_rows = [["Tipo de accion", "2026 T1"]]
    for tp in TIPOS:
        n = sum(x["days"] for x in a if x["tipo"] == tp
                and date(2026, 1, 1) <= x["date"] <= date(2026, 3, 31))
        tipo_rows.append([tp, str(n)])
    pdf(os.path.join(TARGET, "boletin_2026T1.pdf"),
        "Boletin trimestral de accion colectiva, primer trimestre de 2026",
        [("p", "Observatorio Territorial del Nororiente. Publicado el 24 de abril de 2026. Las cifras "
               "corresponden al extracto definitivo del trimestre y se revisan si el registro recibe "
               "cuentas posteriores."),
         ("h", "1. Acciones por municipio del panel, acciones-dia"),
         ("t", rows),
         ("h", "2. Composicion del trimestre por tipo de accion"),
         ("t", tipo_rows),
         ("h", "3. Nota metodologica"),
         ("p", "Las cifras cuentan acciones-dia segun el manual de codificacion. El boletin no "
               "compara municipios entre si ni anticipa la designacion semestral, que se publica en "
               "la nota de vigilancia."),
         ("p", "El Observatorio recuerda que un registro construido a partir de prensa depende de lo "
               "que las fuentes remitan y que su cobertura no es uniforme entre municipios.")])


def write_invoices(d):
    lines = invoice_lines(d)
    MONTH = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
             "septiembre", "octubre", "noviembre", "diciembre"]
    blocks = [("p", "Resena Andina S.A.S. Resumen anual de facturacion 2025 para el Observatorio "
                    "Territorial del Nororiente, mesas de lote. Emitido el 19 de enero de 2026."),
              ("p", "La facturacion corresponde al periodo de publicacion de los items, no al dia en "
                    "que se remiten. Los valores estan en miles de pesos.")]
    for q in (1, 2, 3, 4):
        rows = [["Mesa", "Mes", "Items facturados", "Valor (miles COP)"]]
        tot = 0
        for seat, m, items, val in lines:
            if (m - 1) // 3 + 1 != q:
                continue
            rows.append([seat, MONTH[m], str(items), "%.1f" % val])
            tot += items
        rows.append(["Total trimestre", "", str(tot), ""])
        blocks.append(("h", "Trimestre %d de 2025" % q))
        blocks.append(("t", rows))
    blocks.append(("h", "Notas"))
    blocks.append(("p", "Nota credito 2025-08: el Observatorio rechazo el lote del 11 de agosto de la "
                        "mesa de Rio de Oro por duplicacion en origen y no se factura."))
    pdf(os.path.join(TARGET, "facturas_resena_andina_2025.pdf"),
        "Resumen de facturacion 2025, mesas de lote", blocks)


def write_dictionary(rowcounts):
    p = os.path.join(TARGET, "diccionario_datos.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write("""# Diccionario de datos, Registro de Acciones Colectivas

Edicion 9, 5 de noviembre de 2026. Describe los archivos del extracto definitivo de esa fecha.

## rac_acciones_2024.csv, rac_acciones_2025.csv, rac_acciones_2026.csv

Una fila es una entrada del registro. Hasta la plantilla de 2025 cada dia de una accion prolongada
ocupa su propia fila; desde 2026 la fila describe la accion y el campo `dias` indica cuantos dias
corrio. La exportacion de 2025 renombro las columnas y escribe las fechas en formato dia primero.

| Campo | Significado |
|---|---|
| action_id, id_accion | identificador de la entrada, unico dentro del anio y del departamento |
| fecha_accion, fecha_de_accion | fecha de ocurrencia de la accion |
| fecha_registro, fecha_de_registro | fecha en que el equipo abrio la entrada |
| municipio | municipio de ocurrencia |
| divipola, cod_divipola | codigo del municipio vigente a la fecha de la accion |
| tipo_accion, tipo | tipo de accion segun el manual |
| sector_actor, sector | sector de la organizacion convocante, lista vigente |
| participantes_est, participantes | estimacion central de participantes; vacio o cero cuando la fuente no reporta |
| nota_registro, nota | transcripcion del codificador, incluye el rango cuando la fuente reporta uno |
| dias | dias que corrio la accion (solo plantilla 2026) |
| extracto | preliminar o definitivo (solo plantilla 2026) |

## envios_resena_andina.csv

Una fila es un dia en que un medio remitio material fechado en un municipio. `items_entregados`
cuenta todo lo que el servicio remitio desde ese municipio, cualquiera sea el tema.
`items_retenidos` cuenta los items que el filtro del registro conservo para revision, es decir los
que pueden describir una accion. `periodo_publicacion` es el mes en que se publicaron los items de
la fila, que no siempre es el mes de la remision. Los codigos de fuente llevan el prefijo RSA desde
2026, cuando el servicio renumero sus mesas.

## citas_rac.csv

Una fila es una cita: un item que el registro vinculo a una entrada. Una entrada puede tener varias
citas y un item puede citar una sola entrada.

## resumen_mensual_rac_2025.csv

Resumen mensual publicado, armado con los retornos de las mesas del servicio. Una mesa atiende mas
de un municipio y reporta bajo su sede, de modo que la columna `municipio_sede` es la sede de la
mesa y no necesariamente el municipio de ocurrencia.

## tabla_municipios.csv

Codigos DIVIPOLA con sus fechas de vigencia. Tres municipios recibieron codigo nuevo en julio de
2025 cuando la lista nacional fusiono dos entidades.

## panel_fuentes.xlsx, proyecciones_poblacion.xlsx

Panel de medios vigente al cierre, una hoja por tipo. Proyecciones municipales de poblacion en
unidades y en miles, mas la serie anterior al censo.

## Archivos de contexto

`indice_menciones_redes.csv` es un indice departamental de menciones en redes contratado en 2026.
`incidencias_viales.csv` recoge incidentes de la autoridad de transporte. Ninguno de los dos entra
en el registro.
""")
    return p


def write_manifest(rowcounts):
    DESC = {
        "rac_acciones_2024.csv": "entradas del registro, plantilla 2024, una fila por dia de accion",
        "rac_acciones_2025.csv": "entradas del registro, plantilla 2025, columnas renombradas",
        "rac_acciones_2026.csv": "entradas del registro, plantilla 2026, con dias y extracto",
        "envios_resena_andina.csv": "remisiones del servicio de prensa por medio, municipio y dia",
        "citas_rac.csv": "citas que vinculan items a entradas",
        "resumen_mensual_rac_2025.csv": "resumen mensual publicado, armado por mesas",
        "tabla_municipios.csv": "codigos DIVIPOLA con vigencias",
        "panel_fuentes.xlsx": "panel de medios al cierre",
        "proyecciones_poblacion.xlsx": "proyecciones de poblacion en unidades y miles",
        "protocolo_designacion.pdf": "protocolo de designacion semestral, version 4",
        "manual_codificacion.pdf": "manual de codificacion, edicion 7",
        "boletin_2026T1.pdf": "boletin trimestral publicado del primer trimestre de 2026",
        "facturas_resena_andina_2025.pdf": "resumen de facturacion 2025 de las mesas de lote",
        "diccionario_datos.md": "diccionario de campos y grano",
        "indice_menciones_redes.csv": "indice departamental de menciones en redes, contratado 2026",
        "incidencias_viales.csv": "incidentes de la autoridad de transporte",
        "manifiesto_exportacion.csv": "este manifiesto",
    }
    rows = [[k, v, DESC.get(k, "archivo del extracto"), "sintetico", "2026-11-05",
             "uso interno del Observatorio"] for k, v in sorted(rowcounts.items())]
    w_csv(os.path.join(TARGET, "manifiesto_exportacion.csv"),
          ["archivo", "filas", "descripcion", "origen", "fecha_extracto", "licencia"], rows)


def write_pack(d, pops):
    """Write every file of the bundle, then normalise the containers and the mtimes so two runs are
    byte identical."""
    import postprocess
    if os.path.isdir(TARGET):
        shutil.rmtree(TARGET)
    os.makedirs(TARGET)
    counts = {}
    write_register(d)
    counts["envios_resena_andina.csv"] = write_deliveries(d)
    counts["citas_rac.csv"] = write_citations(d)
    counts["resumen_mensual_rac_2025.csv"] = write_summary(d)
    write_lookups(pops)
    write_workbooks(pops)
    write_protocol()
    write_manual()
    write_bulletin(d)
    write_invoices(d)
    write_dictionary(counts)
    for name in sorted(os.listdir(TARGET)):
        path = os.path.join(TARGET, name)
        if name.endswith(".csv"):
            with open(path, encoding="utf-8") as f:
                counts[name] = sum(1 for _ in f) - 1
        else:
            counts[name] = ""                      # a document's extent is its pages, not its rows
    write_manifest(counts)

    stamp = "D:20261105091500+00'00'"
    for name in sorted(os.listdir(TARGET)):
        path = os.path.join(TARGET, name)
        if name.endswith(".pdf"):
            postprocess.normalize_pdf(path, stamp.encode(), stamp.encode())
        elif name.endswith(".xlsx"):
            postprocess.normalize_ooxml(path, creator="ohernandez", last_by="ohernandez",
                                        created="2026-11-05T09:15:00Z",
                                        modified="2026-11-05T09:15:00Z", excel=True)
    ts = 1762333200  # 2026-11-05 09:00:00 UTC, the export stamp
    for name in sorted(os.listdir(TARGET)):
        os.utime(os.path.join(TARGET, name), (ts, ts))
    meta = {
        "task": "task199",
        "bundle": "target/",
        "as_of": "2026-11-05",
        "distractor_files": ["indice_menciones_redes.csv", "incidencias_viales.csv"],
        "answer": None,
        "notes": "Synthetic pack. The register, the delivery log, the invoices and the published "
                 "summary are generated from generator/core.py's parameters; municipality names and "
                 "DIVIPOLA codes are real, every organisation, outlet and person is invented.",
        "files": counts,
    }
    json.dump(meta, open(os.path.join(TASK, "metadata.json"), "w"), indent=1, sort_keys=True)
    print()
    print("wrote %d files to target/" % len(os.listdir(TARGET)))
    for name in sorted(os.listdir(TARGET)):
        path = os.path.join(TARGET, name)
        print("   %-34s %9d bytes %s" % (name, os.path.getsize(path),
                                         ("%d rows" % counts[name]) if name in counts else ""))


if __name__ == "__main__":
    main()
