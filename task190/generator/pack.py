"""Cut the evidence pack under target/. Everything is derived; nothing is placed to be caught."""
import csv
import datetime as dt
import math
import os

import numpy as np

import sim
import world as W

# of the tonnage a final facility confirms, the share confirmed at a recovery operation
REC_OF_CONFIRMED = {"metal": 0.93, "mixed_ci": 0.66, "paper": 0.95, "wood": 0.90,
                    "cd_rubble": 0.97, "glass": 0.96, "plastic": 0.72, "textile": 0.55}
VIA_INTERIM = 0.30                      # share of producer consignments routed through a transfer station
NACE = ["10", "16", "17", "20", "22", "23", "24", "25", "28", "31", "41", "42", "46", "47", "56"]

# waste codes per stream, with the 1 July 2026 revision: one code per stream is replaced.
CODES = {
    "metal":     [("12 01 01", None), ("17 04 05", None), ("19 12 02", "19 12 02*"), ("16 01 17", None)],
    "mixed_ci":  [("20 03 01", None), ("19 12 12", None), ("15 01 06", "15 01 06*"), ("20 03 99", None)],
    "paper":     [("20 01 01", None), ("15 01 01", None), ("19 12 01", None)],
    "wood":      [("15 01 03", None), ("17 02 01", None), ("19 12 07", "19 12 07*")],
    "cd_rubble": [("17 01 07", None), ("17 05 04", None), ("17 09 04", None)],
    "glass":     [("20 01 02", None), ("15 01 07", None), ("17 02 02", None)],
    "plastic":   [("20 01 39", None), ("15 01 02", None), ("19 12 04", "19 12 04*")],
    "textile":   [("20 01 10", None), ("04 02 22", None), ("19 12 08", None)],
}
OPS = [
    ("R3", "recovery", "Recycling or reclamation of organic substances"),
    ("R4", "recovery", "Recycling or reclamation of metals and metal compounds"),
    ("R5", "recovery", "Recycling or reclamation of other inorganic materials"),
    ("R1", "recovery", "Use principally as a fuel to generate energy"),
    ("R13", "interim", "Storage pending any of the operations R1 to R12"),
    ("D1", "disposal", "Deposit into or onto land"),
    ("D10", "disposal", "Incineration on land"),
    ("D15", "interim", "Storage pending any of the operations D1 to D14"),
]
OP_KIND = {c: k for c, k, _d in OPS}
REC_OPS = {"metal": "R4", "mixed_ci": "R1", "paper": "R3", "wood": "R1",
           "cd_rubble": "R5", "glass": "R5", "plastic": "R3", "textile": "R3"}
DIS_OPS = {"metal": "D1", "mixed_ci": "D10", "paper": "D10", "wood": "D10",
           "cd_rubble": "D1", "glass": "D1", "plastic": "D10", "textile": "D1"}


# Place and family-name pools for facility and carrier names, drawn from the pt_PT locale lists
# the fingerprint guard draws personas from and folded to the register's ASCII convention. Names are
# drawn from these pools, never numbered in file order: a register of ninety-six sites named in
# sequence is the tell a reader reports first. Places are held by region so that a site's name and
# its licensed region agree.
PLACES = {
    "Norte": ["Amarante", "Barcelos", "Braga", "Braganca", "Chaves", "Ermesinde", "Espinho",
              "Esposende", "Fafe", "Felgueiras", "Freamunde", "Gandra", "Gondomar", "Guimaraes",
              "Lamego", "Lixa", "Macedo de Cavaleiros", "Maia", "Marco de Canaveses", "Matosinhos"],
    "Centro": ["Abrantes", "Alcobaca", "Anadia", "Aveiro", "Caldas da Rainha", "Cantanhede",
               "Castelo Branco", "Coimbra", "Covilha", "Entroncamento", "Esmoriz", "Estarreja",
               "Fatima", "Fiaes", "Figueira da Foz", "Fundao", "Gafanha da Nazare", "Gouveia",
               "Guarda", "Ilhavo", "Leiria", "Lourosa", "Mangualde", "Marinha Grande", "Mealhada",
               "Meda"],
    "Lisboa": ["Agualva-Cacem", "Almada", "Amadora", "Amora", "Alverca do Ribatejo", "Barreiro",
               "Costa da Caparica", "Lisboa", "Loures"],
    "Alentejo": ["Alcacer do Sal", "Almeirim", "Beja", "Cartaxo", "Elvas", "Estremoz", "Evora"],
    "Algarve": ["Albufeira", "Faro", "Lagoa", "Lagos", "Loule"],
}
SURNAMES = ["Abreu", "Almeida", "Alves", "Amaral", "Amorim", "Andrade", "Anjos", "Antunes",
            "Araujo", "Assuncao", "Azevedo", "Baptista", "Barbosa", "Barros", "Batista", "Borges",
            "Branco", "Brito", "Campos", "Cardoso", "Carneiro", "Carvalho", "Castro", "Coelho",
            "Correia", "Costa", "Cruz", "Cunha", "Domingues", "Esteves", "Faria", "Fernandes",
            "Ferreira", "Figueiredo", "Fonseca", "Freitas", "Garcia", "Gaspar", "Gomes",
            "Goncalves", "Guerreiro", "Henriques", "Jesus", "Leal", "Leite", "Lima", "Lopes",
            "Loureiro", "Lourenco", "Macedo", "Machado", "Magalhaes", "Maia", "Marques", "Martins",
            "Matias", "Matos", "Melo", "Mendes", "Miranda", "Monteiro", "Morais", "Moreira",
            "Mota", "Moura", "Nascimento", "Neto", "Neves", "Nogueira", "Nunes", "Oliveira",
            "Pacheco", "Paiva", "Pereira", "Pinheiro", "Pinho", "Pinto", "Pires", "Ramos", "Reis",
            "Ribeiro", "Rocha", "Rodrigues", "Santos"]
SITE_KINDS = {
    "final": ["Centro de Triagem", "Unidade de Tratamento Mecanico e Biologico",
              "Centro de Valorizacao Organica", "Unidade de Valorizacao Energetica",
              "Aterro Sanitario", "Unidade de Reciclagem de Metais",
              "Centro de Processamento de Inertes", "Unidade de Reciclagem de Plasticos"],
    "interim": ["Estacao de Transferencia", "Centro de Recolha e Armazenagem",
                "Parque de Transferencia de Residuos"],
}
CARRIER_FORMS = ["Transportes %s, Lda", "%s & Filhos, Lda", "%s Transportes de Residuos, Lda",
                 "%s Logistica Ambiental, Lda"]
CARRIER_PLACE_FORMS = ["Rodoviaria de %s, Lda", "Transportes Reunidos de %s, Lda"]


def _pick(rng, seq):
    return seq[int(rng.integers(0, len(seq)))]


def _unique(rng, make, n):
    """n distinct names drawn from a pool of forms, in draw order."""
    seen, out = set(), []
    while len(out) < n:
        v = make()
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


# -------------------------------------------------------------- consignment dates: lags and weights
# the fixed-date national holidays the division and the sites keep; movements thin out on them
HOLIDAYS = {(1, 1), (4, 25), (5, 1), (6, 10), (8, 15), (10, 5), (11, 1), (12, 1), (12, 8), (12, 25)}


def _bump(d, rl, back_first=False):
    """A date that falls on a weekend or a national holiday moves to the adjacent working day most
    of the time; a register of continuously operating sites still carries some Saturday and
    holiday movements."""
    closed = d.weekday() >= 5 or (d.month, d.day) in HOLIDAYS
    if not closed or rl.random() >= 0.85:
        return d
    if d.weekday() >= 5:
        if d.weekday() == 5:
            return d - dt.timedelta(days=1) if back_first and rl.random() < 0.7 else d + dt.timedelta(days=2)
        return d + dt.timedelta(days=1) if not back_first or rl.random() < 0.7 else d - dt.timedelta(days=2)
    step = -1 if (back_first and rl.random() < 0.6) else 1
    nd = _open_day(d, step)
    if nd.year != d.year:                    # a holiday at either end of the year moves inwards
        nd = _open_day(d, -step)
    return nd


def _open_day(d, step):
    nd = d + dt.timedelta(days=step)
    while nd.weekday() >= 5 or (nd.month, nd.day) in HOLIDAYS:
        nd += dt.timedelta(days=step)
    return nd
    if d.weekday() == 5:
        return d - dt.timedelta(days=1) if back_first and rl.random() < 0.7 else d + dt.timedelta(days=2)
    return d + dt.timedelta(days=1) if not back_first or rl.random() < 0.7 else d - dt.timedelta(days=2)


def _lag(rl, median, sigma, cap, start, limit):
    """A transit, treatment or storage lag: a short mode with a real right tail, truncated to the
    window the extract can observe rather than clamped onto its last day."""
    room = (limit - start).days - 1          # the extract's own day is not a landing place
    if room <= 1:
        return max(1, room)
    for _ in range(6):
        v = max(1, min(cap, int(round(float(rl.lognormal(math.log(median), sigma))))))
        if v <= room:
            return v
    return int(rl.integers(1, room + 1))


def _then(rl, prev, median, sigma, cap, limit):
    """The next leg's date. A draw that would land on or past the extract is redrawn inside the
    window the extract can see, so the tail thins towards the extract date instead of piling onto
    it: a spike on the last day of an extract is an artefact of the cut, not of the register."""
    d = _bump(prev + dt.timedelta(days=_lag(rl, median, sigma, cap, prev, limit)), rl)
    if d >= limit:
        room = (limit - prev).days
        d = prev + dt.timedelta(days=int(rl.integers(1, room))) if room >= 2 else prev
    return max(d, prev)


def _kg_noise(rl, n):
    """Net weights come off a weighbridge in 20 kg steps, so a consignment's recorded tonnage is
    not a whole number. The offsets are in hundredths of a tonne and sum to exactly zero over the
    group, so every tonnage total the deliverables state is the one the design fixed."""
    o = (rl.integers(-25, 26, size=n) * 2).astype(int)
    s = int(o.sum())
    i = 0
    while s != 0:
        j = i % n
        step = -2 if s > 0 else 2
        if -50 <= o[j] + step <= 50:
            o[j] += step
            s += step
        i += 1
    return o


def _writecsv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def _dates(rng, n, year, lo=1, hi=12):
    base = dt.date(year, 1, 1)
    span = (dt.date(year, 12, 31) - base).days
    return [base + dt.timedelta(days=int(d)) for d in rng.integers(0, span + 1, size=n)]


def build_entities(rng):
    """Enterprises: the sampled 1,630, the issued nonrespondents, the out-of-scope, and the wider
    set of permit holders the register's producers are drawn from."""
    ents = []
    eid = 500000
    per_stratum = {}
    for h, (code, _label, N, r) in enumerate(W.STRATA):
        # permit holders in this stratum: everyone in E1, a share of the rest
        hold = {"E1": N, "E2": 600, "E3": 1800, "E4": 3645}[code]
        rows = []
        for i in range(hold):
            eid += 1
            reg = W.REGIONS[int(rng.choice(len(W.REGIONS), p=W.REGION_W))]
            rows.append({"ent": "PT%07d" % eid, "stratum": code, "region": reg,
                         "nace": NACE[int(rng.integers(0, len(NACE)))], "sample_idx": None})
        per_stratum[code] = rows
        ents.extend(rows)
    return ents, per_stratum


def build_crosswalk(ents, rng, path):
    """agency permit number against business register enterprise number. A handful of permits were
    superseded when an enterprise re-registered; one duplicate row survives from a 2019 migration."""
    rows, permit_of, super_pairs = [], {}, []
    dr = np.random.default_rng(W.SEED + 43)      # permit valid-from dates
    pid = 310000
    for e in ents:
        pid += 1
        p = "APA-%06d" % pid
        permit_of[e["ent"]] = p
        vf = (dt.date(2009, 3, 2) + dt.timedelta(days=int(dr.integers(0, 3500)))).isoformat()
        rows.append([p, e["ent"], e["region"], e["nace"], "current", "", vf])
    # 34 supersessions spread over the frame (hazard H4), none inside the 2026 responding sample
    pool = [e for e in ents if e["sample_idx"] is None]
    picks = rng.choice(len(pool), size=34, replace=False)
    for k in picks:
        e = pool[int(k)]
        pid += 1
        newp = "APA-%06d" % pid
        old = permit_of[e["ent"]]
        for r in rows:
            if r[0] == old:
                r[4], r[5] = "superseded", newp
        rows.append([newp, e["ent"], e["region"], e["nace"], "current", "",
                     (dt.date(2024, 1, 8) + dt.timedelta(days=int(dr.integers(0, 330)))).isoformat()])
        super_pairs.append((old, newp, e["ent"], e["region"]))
    # one duplicated crosswalk row from the 2019 migration, same permit and enterprise
    rows.append(list(rows[411]))
    rows.sort(key=lambda r: r[0])
    _writecsv(path, ["agency_permit_no", "enterprise_number", "region", "nace_division",
                     "permit_status", "superseded_by", "valid_from"], rows)
    return permit_of, super_pairs, len(rows)


def build_microdata(samp, idx, ents, per_stratum, path):
    """One row per responding enterprise, one column per waste stream, zeros explicit. No region:
    the enterprise's region is in the crosswalk."""
    # Statistical confidentiality: the released micro-data carries a survey record identifier
    # rather than the business register number, so a record cannot be traced to a named
    # enterprise or to that enterprise's movements in the register.
    keys = [k for k, _n, _p, _m, _c in W.STREAMS]
    w = sim.weights()
    rows = []
    rid = 0
    for h, (code, _label, N, r) in enumerate(W.STRATA):
        pool = per_stratum[code]
        for j in range(r):
            e = pool[j % len(pool)]
            e["sample_idx"] = (h, j)
            rid += 1
            rows.append(["BWS26-%05d" % rid, code, "%.6f" % w[h], e["nace"]] +
                        ["%.3f" % samp[k][h][j] for k in keys])
    hdr = ["record_id", "stratum_code", "design_weight", "nace_division"] + \
          ["arisings_t_" + k for k in keys]
    rows.sort(key=lambda r: r[0])
    return _writecsv(path, hdr, rows)


def build_facilities(rng, path):
    nr = np.random.default_rng(W.SEED + 37)      # the name and licence-date stream
    fac, rows, used = [], [], set()
    fid = 70000
    for i in range(96):
        fid += 1
        role = "interim" if i % 3 == 0 else "final"
        reg = W.REGIONS[int(rng.choice(len(W.REGIONS), p=W.REGION_W))]
        p = "APA-F%05d" % fid
        ops = "R13,D15" if role == "interim" else ",".join(sorted({REC_OPS[k] for k, *_ in W.STREAMS} | {"D1", "D10"}))
        while True:
            nm = "%s de %s" % (_pick(nr, SITE_KINDS[role]), _pick(nr, PLACES[reg]))
            if nm not in used:
                used.add(nm)
                break
        lic = (dt.date(2008, 1, 1) + dt.timedelta(days=int(nr.integers(0, 3650)))).isoformat()
        fac.append({"permit": p, "role": role, "region": reg})
        rows.append([p, nm, reg, role, ops, lic])
    _writecsv(path, ["facility_permit_no", "facility_name", "region", "facility_role",
                     "licensed_operations", "licensed_from"], rows)
    return fac


def _consignments(rng, rl, key, target_rec, confirmed, despatched, year):
    """Consignments for one stream in one year, each tonnage as a weighbridge records it (whole
    hundredths of a tonne), summing exactly to the three class totals: confirmed at a recovery
    operation, confirmed at disposal, despatched but unconfirmed."""
    out = []
    for cls, total in (("rec", target_rec), ("dis", confirmed - target_rec),
                       ("unc", despatched - confirmed)):
        if total <= 0:
            continue
        mean = 19.0
        n = max(2, int(round(total / mean)))
        t = np.maximum(1, np.round(rng.lognormal(math.log(mean) - 0.18, 0.6, size=n)).astype(int))
        diff = total - int(t.sum())
        i = 0
        while diff != 0:                       # spread the residue one tonne at a time
            j = i % n
            if diff > 0:
                t[j] += 1
                diff -= 1
            elif t[j] > 1:
                t[j] -= 1
                diff += 1
            i += 1
        for v in (t.astype(int) * 100 + _kg_noise(rl, n)):
            out.append((cls, int(v)))
    rng.shuffle(out)
    return out


def _t(cents):
    return "%d.%02d" % (cents // 100, cents % 100)


def build_register(samp, ents, permit_of, fac, rng, paths, pop=None):
    """2026 (two half-year extracts, the schema changed on 1 July) and 2025 producer-origin
    consignments with their legs, plus the child consignments interim facilities forward."""
    att = sim.attainment(samp)
    # the lag and weighbridge draws come from their own stream, so the consignment allocation,
    # the producers, the codes and the sites are the ones the rest of the pack was cut with
    rl = np.random.default_rng(W.SEED + 23)
    limit = dt.date.fromisoformat(W.EXTRACT_REGISTER)
    interim = [f for f in fac if f["role"] == "interim"]
    finals = [f for f in fac if f["role"] == "final"]
    producers = [e for e in ents]
    # a stream's movements come from the enterprises that produce it, so each consignment's
    # producer is drawn from the stratum distribution of that stream's own arisings
    by_stratum_ents = {}
    for h, (code, _l, _N, _r) in enumerate(W.STRATA):
        by_stratum_ents[h] = [e for e in ents if e["stratum"] == code]
    strat_share = {}
    for key, _n, _p, _m, _c in W.STREAMS:
        if pop is None:
            strat_share[key] = [0.25] * 4
        else:
            tot = sum(float(pop[key][h].sum()) for h in range(4))
            strat_share[key] = [float(pop[key][h].sum()) / tot for h in range(4)]
    legs26, legs25 = [], []
    cno = 4000000
    renotified = 0
    for key, _n, _p, _m, _c in W.STREAMS:
        rec26 = att[key]["recovered_t"]
        conf26 = int(round(rec26 / REC_OF_CONFIRMED[key]))
        desp26 = int(round(conf26 / W.CONFIRMED_SHARE[key]))
        rec25 = int(round(rec26 * 0.962))
        conf25 = int(round(rec25 / REC_OF_CONFIRMED[key]))
        desp25 = int(round(conf25 / W.CONFIRMED_SHARE[key]))
        for year, rec, conf, desp, sink in ((2026, rec26, conf26, desp26, legs26),
                                            (2025, rec25, conf25, desp25, legs25)):
            cons = _consignments(rng, rl, key, rec, conf, desp, year)
            dates = _dates(rng, len(cons), year)
            for (cls, cents), d in zip(cons, dates):
                cno += 1
                parent_is_producer = ""
                hh = int(rng.choice(4, p=strat_share[key]))
                poolh = by_stratum_ents[hh]
                prod = poolh[int(rng.integers(0, len(poolh)))]
                codes = CODES[key]
                base, repl = codes[int(rng.integers(0, len(codes)))]
                code = repl if (repl and year == 2026 and d >= dt.date(2026, 7, 1)) else base
                via = rng.random() < VIA_INTERIM and cls != "unc"
                carrier = "APA-C%05d" % (80000 + int(rng.integers(0, 140)))
                pnum = "NW%08d" % cno
                seq = 1
                d = _bump(d, rl, back_first=True)
                chain_date = d.isoformat()
                tonnes = _t(cents)
                recv = _then(rl, d, 1.3, 0.55, 14, limit)
                rows = [[pnum, seq, "PRODUCER_DESPATCH", d.isoformat(), permit_of[prod["ent"]],
                         carrier, "", code, tonnes, "", parent_is_producer]]
                if via:
                    f = interim[int(rng.integers(0, len(interim)))]
                    seq += 1
                    rows.append([pnum, seq, "FACILITY_RECEIPT", recv.isoformat(),
                                 permit_of[prod["ent"]], carrier, f["permit"], code, tonnes, "", ""])
                    seq += 1
                    held = _then(rl, recv, 2.4, 0.75, 30, limit)
                    rows.append([pnum, seq, "TREATMENT_CONFIRMED", held.isoformat(),
                                 permit_of[prod["ent"]], carrier, f["permit"], code, tonnes, "R13", ""])
                    cno += 1
                    child = "NW%08d" % cno
                    g = finals[int(rng.integers(0, len(finals)))]
                    op = REC_OPS[key] if cls == "rec" else (DIS_OPS[key] if cls == "dis" else "")
                    fwd = _then(rl, held, 11.0, 0.70, 120, limit)
                    frecv = _then(rl, fwd, 1.3, 0.55, 14, limit)
                    rows.append([child, 1, "PRODUCER_DESPATCH", fwd.isoformat(),
                                 f["permit"], carrier, "", code, tonnes, "", pnum])
                    rows.append([child, 2, "FACILITY_RECEIPT", frecv.isoformat(),
                                 f["permit"], carrier, g["permit"], code, tonnes, "", pnum])
                    if cls != "unc":
                        rows.append([child, 3, "TREATMENT_CONFIRMED",
                                     _then(rl, frecv, 3.0, 0.80, 45, limit).isoformat(),
                                     f["permit"], carrier, g["permit"], code, tonnes, op, pnum])
                else:
                    g = finals[int(rng.integers(0, len(finals)))]
                    seq += 1
                    rows.append([pnum, seq, "FACILITY_RECEIPT", recv.isoformat(),
                                 permit_of[prod["ent"]], carrier, g["permit"], code, tonnes, "", ""])
                    if cls != "unc":
                        op = REC_OPS[key] if cls == "rec" else DIS_OPS[key]
                        seq += 1
                        rows.append([pnum, seq, "TREATMENT_CONFIRMED",
                                     _then(rl, recv, 3.0, 0.80, 45, limit).isoformat(),
                                     permit_of[prod["ent"]], carrier, g["permit"], code, tonnes, op, ""])
                for r in rows:
                    sink.append((chain_date, r))
    hdr25 = ["consignment_no", "leg_seq", "leg_type", "leg_date", "producer_permit", "carrier_permit",
             "facility_permit", "waste_code", "tonnes", "operation_code", "parent_consignment"]
    hdr26b = ["consignment_ref", "leg_no", "leg_kind", "leg_dt", "producer_permit_no", "carrier_permit_no",
              "site_permit_no", "ewc_code", "net_tonnes", "treatment_op", "parent_ref"]
    # the extract is cut by the chain's own producer despatch date, so a child forwarded in
    # January 2027 ships beside the parent it continues
    h1 = sorted([r for cd, r in legs26 if cd < "2026-07-01"], key=lambda r: (r[3], r[0], r[1]))
    h2 = sorted([r for cd, r in legs26 if cd >= "2026-07-01"], key=lambda r: (r[3], r[0], r[1]))
    n1 = _writecsv(paths["h1"], hdr25, h1)
    n2 = _writecsv(paths["h2"], hdr26b, h2)
    y25 = [r for _cd, r in legs25]
    y25, renot = _renotify(y25, rng, cno)
    y25 = sorted(y25, key=lambda r: (r[3], r[0], r[1]))
    n3 = _writecsv(paths["y25"], hdr25, y25)
    return n1, n2, n3, att, renot


def _renotify(y25, rng, cno):
    """Ask A2's primary. A 2025 notification cancelled after despatch (the carrier changed) was
    re-notified: the register holds both, the later one continuing the earlier, and the facility
    confirmed against each number it held. Counting confirmations counts the tonnage twice."""
    import collections as _c
    chains = _c.defaultdict(list)
    for r in y25:
        chains[r[0]].append(r)
    cand = []
    for c, rs in chains.items():
        d = [x for x in rs if x[2] == "PRODUCER_DESPATCH"][0]
        conf = [x for x in rs if x[2] == "TREATMENT_CONFIRMED"]
        if d[10] or not conf:
            continue
        if OP_KIND.get(conf[0][9]) == "recovery" and not d[4].startswith("APA-F"):
            cand.append(c)
    # spread the re-notifications over all eight streams, so every figure in ask A2 moves
    code2s = {}
    for k, lst in CODES.items():
        for b, rp in lst:
            code2s[b] = k
            if rp:
                code2s[rp] = k
    by_stream = _c.defaultdict(list)
    for c in sorted(cand):
        d = [x for x in chains[c] if x[2] == "PRODUCER_DESPATCH"][0]
        by_stream[code2s[d[7]]].append(c)
    want = {"metal": 6, "mixed_ci": 6, "paper": 6, "wood": 5,
            "cd_rubble": 6, "glass": 5, "plastic": 5, "textile": 4}
    picks = []
    for k, _n, _p, _m, _cv in W.STREAMS:
        pool = by_stream[k]
        take = min(want[k], len(pool))
        sel = rng.choice(len(pool), size=take, replace=False)
        picks.extend(pool[int(i)] for i in sel)
    extra, pairs = [], []
    for c in sorted(picks):
        cno += 1
        new = "NW%08d" % cno
        for r in chains[c]:
            q = list(r)
            q[0] = new
            q[10] = c
            q[3] = (dt.date.fromisoformat(r[3]) + dt.timedelta(days=4)).isoformat()
            extra.append(q)
        d = [x for x in chains[c] if x[2] == "PRODUCER_DESPATCH"][0]
        pairs.append((c, new, d[7], float(d[8])))
    return y25 + extra, pairs


# ---------------------------------------------------------------- ask populations and references

MUNI = {
    "Norte": ["Barcelos", "Guimaraes", "Penafiel", "Amarante", "Valongo", "Esposende", "Felgueiras"],
    "Centro": ["Viseu", "Covilha", "Leiria", "Pombal", "Tondela", "Mangualde"],
    "Lisboa": ["Sintra", "Loures", "Almada", "Mafra", "Palmela", "Alenquer"],
    "Alentejo": ["Beja", "Elvas", "Sines", "Moura"],
    "Algarve": ["Loule", "Silves", "Tavira", "Olhao"],
}
AUTHORITY = {"Norte": "Associacao de Municipios do Vale do Sousa",
             "Centro": "Associacao de Municipios da Beira Interior",
             "Lisboa": "Associacao de Municipios da Lezira",
             "Alentejo": "Associacao de Municipios do Baixo Alentejo",
             "Algarve": "Associacao de Municipios do Sotavento"}
AUTH_MEMBERS = {r: MUNI[r][:3] for r in MUNI}
HUNDREDKG = {"Tondela", "Mangualde"}        # hazard H1: a legacy return still in hundreds of kilograms


def build_response_log(ents, per_stratum, permit_of, rng, path):
    """One row per collection contact. A field trip covers several enterprises in one region and the
    trip's own field days sit on every row it covers, the grain unstated."""
    teams = {r: "EQ-%s" % r[:3].upper() for r in W.REGIONS}
    issued = []
    for code, _label, N, r in W.STRATA:
        pool = per_stratum[code]
        want = W.ISSUED[code]
        issued.extend(pool[:want])
    responders = {e["ent"] for e in issued if e["sample_idx"] is not None}
    oos = set()
    for code in W.OUT_OF_SCOPE:
        pool = [e for e in per_stratum[code] if e["sample_idx"] is None][:W.OUT_OF_SCOPE[code]]
        oos |= {e["ent"] for e in pool}
    rows, visits = [], {}
    by_region = {r: [e for e in issued if e["region"] == r] for r in W.REGIONS}
    cid = 900000
    for region in W.REGIONS:
        pool = by_region[region]
        # group the enterprises that take a field visit into trips of 2 to 7 in this region
        visit_pool = [e for e in pool if rng.random() < 0.34]
        i, vno = 0, 0
        while i < len(visit_pool):
            size = int(rng.integers(2, 8))
            trip = visit_pool[i:i + size]
            i += size
            vno += 1
            vref = "V-%s-%04d" % (region[:3].upper(), vno)
            day = dt.date(2026, 3, 1) + dt.timedelta(days=int(rng.integers(0, 210)))
            days = round(float(rng.uniform(0.6, 1.0)), 2)
            visits[vref] = (region, days, day)
            for e in trip:
                e["_visit"] = (vref, days, day)
        for e in pool:
            cid += 1
            case = "C2026-%06d" % cid
            seq = 0
            ncon = int(rng.integers(1, 4))
            for j in range(ncon):
                seq += 1
                d = dt.date(2026, 2, 1) + dt.timedelta(days=int(rng.integers(0, 250)))
                rows.append([case, permit_of[e["ent"]], seq, d.isoformat(), teams[region],
                             "", "telephone" if j == 0 else "reminder", "0.00", "d",
                             "contact made" if j < ncon - 1 else "return received"])
            if "_visit" in e:
                vref, days, day = e["_visit"]
                seq += 1
                val = days * 8.0 if region == "Alentejo" else days
                rows.append([case, permit_of[e["ent"]], seq, day.isoformat(), teams[region], vref,
                             "field visit", ("%.2f" % val), "h" if region == "Alentejo" else "d",
                             "return received"])
            seq += 1
            if e["ent"] in oos:
                out = "out of scope"
            elif e["ent"] in responders:
                out = "usable return"
            else:
                out = "no return"
            d = dt.date(2026, 11, 1) + dt.timedelta(days=int(rng.integers(0, 60)))
            rows.append([case, permit_of[e["ent"]], seq, d.isoformat(), teams[region], "",
                         "edit check", "0.00", "d", out])
    # hazard H3: one re-sent operations batch, exact duplicate rows
    dup = [list(r) for r in rows[1200:1215]]
    rows.extend(dup)
    rows.sort(key=lambda r: (r[0], r[2], r[3]))
    n = _writecsv(path, ["case_ref", "agency_permit_no", "contact_seq", "contact_date", "team_id",
                         "visit_ref", "contact_mode", "field_days", "time_unit", "outcome"], rows)
    return n, visits, len(dup)


def build_municipal(rng, fac, path_ret, path_rec):
    """Municipal collections and the licensed facilities' receipts of municipal waste. Five
    inter-municipal authorities file a return covering their member municipalities, which file too."""
    ret, base = [], {}
    for region in W.REGIONS:
        for m in MUNI[region]:
            monthly = []
            scale = float(rng.uniform(900, 2600))
            for mth in range(1, 13):
                t = scale * (0.92 + 0.16 * math.sin((mth - 3) / 12.0 * 2 * math.pi)) * float(rng.uniform(0.95, 1.05))
                monthly.append(round(t, 1))
            base[m] = monthly
            for mth in range(1, 13):
                v = monthly[mth - 1]
                if m in HUNDREDKG:
                    ret.append([m, region, "2026-%02d" % mth, "%.1f" % round(v * 10.0, 1), "100kg"])
                else:
                    ret.append([m, region, "2026-%02d" % mth, "%.1f" % v, "t"])
    for region in W.REGIONS:
        a = AUTHORITY[region]
        for mth in range(1, 13):
            v = sum(base[m][mth - 1] for m in AUTH_MEMBERS[region])
            ret.append([a, region, "2026-%02d" % mth, "%.1f" % round(v, 1), "t"])
    ret.sort(key=lambda r: (r[1], r[0], r[2]))
    n1 = _writecsv(path_ret, ["reporting_entity", "region", "reference_month", "collected", "unit"], ret)
    finals = [f for f in fac if f["role"] == "final"]
    rec = []
    for region in W.REGIONS:
        for m in MUNI[region]:
            tot = sum(base[m])
            # 94 to 99 per cent of collections reach a licensed facility within the year
            share = float(rng.uniform(0.94, 0.99))
            left = tot * share
            while left > 0:
                load = min(left, float(rng.uniform(14, 34)))
                f = finals[int(rng.integers(0, len(finals)))]
                d = dt.date(2026, 1, 1) + dt.timedelta(days=int(rng.integers(0, 365)))
                rec.append([f["permit"], d.isoformat(), m, region, "%.3f" % round(load, 3)])
                left -= load
    rec.sort(key=lambda r: (r[1], r[0], r[2]))
    n2 = _writecsv(path_rec, ["facility_permit_no", "receipt_date", "origin_entity",
                              "origin_region", "tonnes"], rec)
    return n1, n2, base


def build_code_crosswalk(path):
    rows = []
    for key, _n, _p, _m, _c in W.STREAMS:
        for base, repl in CODES[key]:
            rows.append([base, key, STREAM_NAME_LOCAL[key], "2014-01-01",
                         "2026-06-30" if repl else "", repl or ""])
            if repl:
                rows.append([repl, key, STREAM_NAME_LOCAL[key], W.CODE_REVISION, "", ""])
    rows.sort(key=lambda r: r[0])
    return _writecsv(path, ["waste_code", "stream_key", "statistical_stream", "valid_from",
                            "valid_to", "replaced_by"], rows)


STREAM_NAME_LOCAL = {k: n for k, n, _p, _m, _c in W.STREAMS}


def build_distractors(rng, fac, path_veh, path_haz):
    nr = np.random.default_rng(W.SEED + 41)      # the carrier-name stream
    allplaces = [pl for reg in W.REGIONS for pl in PLACES[reg]]

    def make():
        if nr.random() < 0.72:
            return _pick(nr, CARRIER_FORMS) % _pick(nr, SURNAMES)
        return _pick(nr, CARRIER_PLACE_FORMS) % _pick(nr, allplaces)

    names = _unique(nr, make, 140)
    rows = []
    for i in range(140):
        p = "APA-C%05d" % (80000 + i)
        for v in range(int(rng.integers(2, 7))):
            rows.append([p, names[i], "%02d-%s-%02d" % (int(rng.integers(10, 99)),
                         "ABCDEFGHJ"[int(rng.integers(0, 9))] * 2, int(rng.integers(10, 99))),
                         float(round(rng.uniform(7.5, 26.0), 1)),
                         (dt.date(2026, 1, 1) + dt.timedelta(days=int(rng.integers(0, 365)))).isoformat()])
    rows.sort(key=lambda r: (r[0], r[2]))
    n1 = _writecsv(path_veh, ["carrier_permit_no", "carrier_name", "vehicle_registration",
                              "gross_capacity_t", "permit_checked_on"], rows)
    rows = []
    for i in range(420):
        rows.append(["TFS-2026-%04d" % (i + 1),
                     ["ES", "FR", "DE", "NL", "BE"][int(rng.integers(0, 5))],
                     ["R4", "R5", "R1", "D10"][int(rng.integers(0, 4))],
                     float(round(rng.uniform(18, 600), 1)),
                     (dt.date(2026, 1, 1) + dt.timedelta(days=int(rng.integers(0, 365)))).isoformat(),
                     ["consented", "consented", "consented", "withdrawn"][int(rng.integers(0, 4))]])
    rows.sort(key=lambda r: r[0])
    n2 = _writecsv(path_haz, ["notification_no", "destination_country", "intended_operation",
                              "notified_tonnes", "consent_date", "notification_status"], rows)
    return n1, n2
