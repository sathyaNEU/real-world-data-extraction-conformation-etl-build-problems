"""The housing agency's budget execution extract, January to September 2026: every programme, phases
A (authorisation), D (commitment), O (obligation) and P (payment)."""
import datetime as dt
import random
from decimal import Decimal

from common import D, SEED, AS_OF, ddmmyyyy, add_workdays, workday
from history import blackout

HEADER = ["exercici", "num_apunt", "data_comptable", "fase", "aplicacio", "programa", "expedient", "tercer",
          "import", "concepte"]
APLIC = {"PPO": "2026.08.431.40.682.00", "ALQ": "2026.08.431.20.480.00", "REH": "2026.08.431.30.780.00",
         "ADQ": "2026.08.431.40.682.10", "GES": "2026.08.431.50.212.00", "FUN": "2026.08.431.00.226.99"}


def money(x):
    return f"{Decimal(x).quantize(Decimal('0.01'))}"


def wd(rng, a, b, dip=False):
    span = (b - a).days
    for _ in range(1000):
        d = a + dt.timedelta(days=rng.randrange(span + 1))
        if not workday(d):
            continue
        if dip and D(2026, 8, 22) <= d <= D(2026, 9, 13) and rng.random() < 0.8:
            continue
        return d
    raise RuntimeError("no day")


def build(W):
    rng = random.Random(SEED * 53 + 11)
    lines = []
    tercers = {}

    def tercer(key):
        if key not in tercers:
            tercers[key] = f"T{3000000 + 7919 * (len(tercers) + 17) % 900000:07d}"
        return tercers[key]

    def add(day, fase, prog, exp, ter, amount, concept):
        assert day <= AS_OF
        lines.append([day, fase, prog, exp, ter, amount, concept])

    # programme authorisations and the July supplement for first offer
    for prog, amt in (("PPO", 9200000), ("ALQ", 5400000), ("REH", 3800000), ("ADQ", 4100000), ("GES", 2650000),
                      ("FUN", 910000)):
        add(D(2026, 1, 5), "A", prog, f"{prog}-2026-0000", "", money(amt), f"Autorització de despesa exercici 2026, programa {prog}")
    add(D(2026, 7, 2), "A", "PPO", "PPO-2026-0000", "", money(14600000),
        "Modificació de crèdit, suplement programa PPO (acord del Consell de 30/06/2026)")
    add(D(2026, 7, 2), "A", "ALQ", "ALQ-2026-0000", "", money(650000), "Modificació de crèdit, suplement programa ALQ")
    # first offer: one D line per dwelling; settled purchases also carry O (deed) and P
    com = sorted(W["book"].commitments, key=lambda c: (c["commit"], c["ref"]))
    exp_of, n = {}, 0
    for c in com:
        key = (c["commit"], c["seller"], c.get("agreement") is not None and W["book"].agreements[c["agreement"] - 1]["agreed"])
        if key not in exp_of:
            n += 1
            exp_of[key] = f"PPO-2026-{n:04d}"
        exp = exp_of[key]
        ter = tercer(c["seller"])
        add(c["commit"], "D", "PPO", exp, ter, money(c["price"]),
            f"Exercici dret de tempteig PPO. Adquisició habitatge RC {c['ref']}. Transmissió notificada amb data "
            f"prevista {ddmmyyyy(c['notified'])}")
        if c.get("deed"):
            add(c["deed"], "O", "PPO", exp, ter, money(c["price"]),
                f"Reconeixement obligació. Escriptura de compravenda habitatge RC {c['ref']}")
            pay = add_workdays(c["deed"], rng.randrange(3, 11))
            if pay <= AS_OF:
                add(pay, "P", "PPO", exp, ter, money(c["price"]), f"Pagament adquisició habitatge RC {c['ref']}")
    # rent support: resolutions in January to March, monthly obligations and payments
    for i in range(232):
        ter = tercer(("alq", i))
        res = wd(rng, D(2026, 1, 12), D(2026, 3, 27))
        monthly = rng.randrange(150, 451)
        months = 9 - res.month + 1
        exp = f"ALQ-2026-{i + 1:04d}"
        add(res, "D", "ALQ", exp, ter, money(monthly * 12), f"Resolució ajuda al lloguer 2026, expedient {exp}")
        for m in range(res.month, 10):
            o = add_workdays(D(2026, m, 8), rng.randrange(0, 3))
            if o > AS_OF:
                continue
            add(o, "O", "ALQ", exp, ter, money(monthly), f"Ajuda al lloguer mensualitat {m:02d}/2026")
            p = add_workdays(o, rng.randrange(2, 6))
            if p <= AS_OF:
                add(p, "P", "ALQ", exp, ter, money(monthly), f"Pagament ajuda al lloguer {m:02d}/2026")
    # building repair grants
    for i in range(112):
        ter = tercer(("reh", i))
        d = wd(rng, D(2026, 2, 2), D(2026, 9, 25), dip=True)
        amt = rng.randrange(6, 90) * 1000 + rng.randrange(0, 1000)
        exp = f"REH-2026-{i + 1:04d}"
        add(d, "D", "REH", exp, ter, money(amt), f"Subvenció rehabilitació edifici, comunitat de propietaris, {exp}")
        o = add_workdays(d, rng.randrange(25, 90))
        if o <= AS_OF:
            part = money(Decimal(amt) * Decimal(rng.choice(["0.5", "1"])))
            add(o, "O", "REH", exp, ter, part, f"Certificació d'obra, {exp}")
            p = add_workdays(o, rng.randrange(5, 15))
            if p <= AS_OF:
                add(p, "P", "REH", exp, ter, part, f"Pagament certificació, {exp}")
    # direct acquisitions outside first offer (negotiated purchases of whole buildings or units)
    for i in range(27):
        ter = tercer(("adq", i))
        d = wd(rng, D(2026, 1, 19), D(2026, 9, 18), dip=True)
        amt = rng.randrange(85, 420) * 1000
        exp = f"ADQ-2026-{i + 1:04d}"
        muni = rng.choice(["Torrent", "Gandia", "Elx", "Sagunt", "Paterna", "Vila-real", "Benidorm", "Alcoi", "Xàtiva"])
        add(d, "D", "ADQ", exp, ter, money(amt), f"Adquisició directa habitatges, {muni}, {exp}")
        o = d + dt.timedelta(days=rng.randrange(21, 75))
        while not workday(o):
            o += dt.timedelta(days=1)
        if o <= AS_OF:
            add(o, "O", "ADQ", exp, ter, money(amt), f"Escriptura adquisició directa, {muni}, {exp}")
            p = add_workdays(o, rng.randrange(3, 12))
            if p <= AS_OF:
                add(p, "P", "ADQ", exp, ter, money(amt), f"Pagament adquisició directa, {exp}")
    # maintenance and management contracts
    for i in range(29):
        ter = tercer(("ges", i))
        exp = f"GES-2026-{i + 1:04d}"
        monthly = rng.randrange(4, 38) * 1000 + rng.randrange(0, 999)
        add(D(2026, 1, 14), "D", "GES", exp, ter, money(monthly * 12), f"Contracte manteniment parc públic, lot {i + 1}")
        for m in range(1, 10):
            o = add_workdays(D(2026, m, 20), rng.randrange(0, 3))
            if o <= AS_OF:
                add(o, "O", "GES", exp, ter, money(monthly), f"Factura manteniment {m:02d}/2026, lot {i + 1}")
                p = add_workdays(o, rng.randrange(10, 25))
                if p <= AS_OF:
                    add(p, "P", "GES", exp, ter, money(monthly), f"Pagament factura manteniment {m:02d}/2026, lot {i + 1}")
    for m in range(1, 10):
        for k in range(18):
            ter = tercer(("fun", k))
            amt = rng.randrange(120, 9000)
            o = wd(rng, D(2026, m, 1), D(2026, m, 26))
            add(o, "O", "FUN", f"FUN-2026-{m:02d}{k:02d}", ter, money(amt), f"Despeses de funcionament {m:02d}/2026")
            p = add_workdays(o, rng.randrange(5, 20))
            if p <= AS_OF:
                add(p, "P", "FUN", f"FUN-2026-{m:02d}{k:02d}", ter, money(amt), "Pagament despeses de funcionament")
    order = {"A": 0, "D": 1, "O": 2, "P": 3}
    lines.sort(key=lambda l: (l[0], order[l[1]], l[3], l[6]))
    out = []
    for i, l in enumerate(lines):
        out.append(["2026", f"{i + 1:06d}", l[0].isoformat(), l[1], APLIC[l[2]], l[2], l[3], l[4], l[5], l[6]])
    return out
