"""Files the solution does not read but a solver has to weigh: the rental deposit register by section
for 2025 and the housing inspectorate's 2025 empty-dwelling visits. (The third distractor, the
superseded 31 March 2026 bulletin, is built with the other bulletins.)"""
import datetime as dt
import random

from common import D, SEED
from plan import SECTIONS
from history import rand_day

DEPOSIT_HEADER = ["any", "seccio_censal", "codi_municipi", "contractes_dipositats", "contractes_arrendador_gran_tenidor",
                  "renda_mitjana_eur", "import_fiances_eur"]
VISIT_HEADER = ["expedient", "data_visita", "seccio_censal", "referencia_cadastral", "nif_titular", "resultat",
                "observacions"]


def deposits(stock, nw_sections):
    rng = random.Random(SEED * 61 + 2)
    sections, buildings, dwellings = stock
    codes = [s["code"] for s in SECTIONS]
    extra = sorted(c for c in nw_sections if c[:5] in ("46250", "03014", "12040"))
    codes = sorted(set(codes) | set(rng.sample(extra, min(40, len(extra)))))
    rows = []
    for c in codes:
        n = next((s["N"] for s in SECTIONS if s["code"] == c), rng.randrange(380, 1100))
        k = int(n * rng.uniform(0.07, 0.16))
        lh = int(k * rng.uniform(0.14, 0.47))
        rent = int(rng.uniform(620, 1150)) if c.startswith("46") else int(rng.uniform(540, 900))
        rows.append(["2025", c, c[:5], str(k), str(lh), str(rent), str(k * rent * rng.choice([1, 1, 2]))])
    return rows


def visits(stock, timeline, holders_nif, lh_ids):
    rng = random.Random(SEED * 67 + 4)
    sections, buildings, dwellings = stock
    watch = [s["code"] for s in SECTIONS]
    rows = []
    n = 0
    for _ in range(260):
        day = rand_day(rng, D(2025, 2, 3), D(2025, 12, 12))
        code = rng.choice(watch)
        st = timeline.state(day)
        cands = sorted(r for r, d in dwellings.items() if d["section"] == code and st.get(r) in lh_ids)
        if not cands:
            continue
        ref = rng.choice(cands)
        n += 1
        res = rng.choices(["ocupat", "desocupat", "sense accés"], [0.71, 0.17, 0.12])[0]
        obs = {"ocupat": rng.choice(["", "Llogaters presents", "Contracte de lloguer en vigor", ""]),
               "desocupat": rng.choice(["Sense mobles", "En obres", "Pendent de reforma", "Comptadors donats de baixa"]),
               "sense accés": rng.choice(["Ningú no obri", "Accés tancat", "Segona visita pendent"])}[res]
        rows.append([f"INS-2025-{n:04d}", day.isoformat(), code, ref, holders_nif[st[ref]], res, obs])
    rows.sort(key=lambda r: (r[1], r[0]))
    return rows
