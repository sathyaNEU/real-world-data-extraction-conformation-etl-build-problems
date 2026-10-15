"""The field the service records come from: every Model K pack the battery plant built from the lots up to ZC2632,
the notebooks the packs went into and their shipments, each owner's use, each pack's capacity life, and every battery
event in service up to the extract (capacity replacements under the warranty, goodwill and paid replacements after
600 cycles, swollen packs, contact and gauge faults, complaints with no fault found), the service packs fitted, the
DACH depot's service orders and their move onto the service case system, the returns depot's log, the carrier's
statement for the returned batteries, the repair partners' invoices and the depot's internal costs."""
from __future__ import annotations

import datetime as dt
import math
from types import SimpleNamespace

import numpy as np

import common as K
import world as WD

SHIP_LOTS = K.LOTS[:24]                      # every lot built and shipped before ZC2638
REGION_MIX = [("DACH", 0.36), ("FRB", 0.21), ("UKI", 0.16), ("NOR", 0.11), ("SOU", 0.16)]
COUNTRIES = {"DACH": [("DE", 0.79), ("AT", 0.11), ("CH", 0.10)],
             "FRB": [("FR", 0.58), ("BE", 0.18), ("NL", 0.21), ("LU", 0.03)],
             "UKI": [("GB", 0.88), ("IE", 0.12)],
             "NOR": [("SE", 0.39), ("NO", 0.22), ("DK", 0.21), ("FI", 0.18)],
             "SOU": [("ES", 0.42), ("IT", 0.46), ("PT", 0.12)]}
PARTNER = {"DACH": "KVD", "FRB": "SVT", "UKI": "HRL", "NOR": "NFX", "SOU": "RPS"}
END = dt.datetime.combine(K.SERVICE_END, dt.time(23, 59))
ALPHA = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"

EVENTS_KEY = (4,)          # the stream of the field's events
APPROVAL_KEY = (11,)       # the stream of the partners' invoice dates

# rates of the battery events other than capacity, per pack-year in service
SWELL_RATE = 0.0011
CONTACT_RATE = 0.0006
GAUGE_RATE = 0.0005
NFF_RATE = 0.0016


def _days(td):
    return td.total_seconds() / 86400.0


def build_packs(W):
    """Every lot's 7,200 Model K packs with their serials, build days and where each went: into a notebook (NB), to
    service stock (SVC) or scrapped at the end-of-line test (SCR). ZC2638's packs are in the bonded store (HOLD)."""
    packs = []
    for lot in SHIP_LOTS + [K.NEW_LOT]:
        r = K.rng("packs", lot)
        b0 = K.LOT_START[lot] + dt.timedelta(days=14)
        days = [b0 + dt.timedelta(days=i) for i in range(16) if (b0 + dt.timedelta(days=i)).weekday() < 5][:10]
        per_day = np.full(len(days), K.MODEL_K_PACKS // len(days))
        per_day[: K.MODEL_K_PACKS - per_day.sum()] += 1
        seq = {}
        disp = r.choice(["NB", "SVC", "SCR"], K.MODEL_K_PACKS, p=[0.9435, 0.0515, 0.0050])
        i = 0
        for d, n in zip(days, per_day):
            for _ in range(int(n)):
                line = "ABC"[int(r.integers(0, 3))]
                key = (d, line)
                seq[key] = seq.get(key, 0) + 1
                serial = "KP%s%s%04d" % (d.strftime("%y%m%d"), line, seq[key])
                t = dt.datetime.combine(d, dt.time(6, 0)) + dt.timedelta(minutes=int(r.integers(0, 15 * 60)))
                packs.append(SimpleNamespace(serial=serial, lot=lot, built=t, line=line,
                                             disp="HOLD" if lot == K.NEW_LOT else str(disp[i])))
                i += 1
    W.field_packs = packs
    return packs


def pack_lives(W):
    """Each pack's capacity life on QP-3: the weakest of its three cells, the cells of one formation tray sharing that
    tray's effect (the lot's predicted spread, the tray effect and each cell's own)."""
    sd_pred = math.sqrt((WD.B1 * WD.CELL_LNQ_SD) ** 2 + (WD.B2 * WD.DR_SD) ** 2)
    by_lot = {}
    for p in W.field_packs:
        by_lot.setdefault(p.lot, []).append(p)
    for lot, ps in by_lot.items():
        if lot == K.NEW_LOT:
            continue
        r = K.rng("pack-lives", lot)
        mq, mr = W.lot_levels[lot]
        mu = WD.B0 + WD.B1 * mq + WD.B2 * mr
        n = len(ps)
        t = r.normal(0.0, WD.SD_TRAY, n)
        cells = mu + r.normal(0.0, sd_pred, (n, 3)) + t[:, None] + r.normal(0.0, WD.SD_CELL, (n, 3))
        life = np.exp(cells.min(axis=1))
        for p, L in zip(ps, life):
            p.life = float(L)


def notebooks(W):
    """The notebooks the NB packs went into, their builds, shipments, the owners' first use and their use (cycles a day),
    and the returns refurbished and shipped again with the same battery."""
    nbs = []
    r = K.rng("notebooks")
    used = set()
    for p in W.field_packs:
        if p.disp != "NB":
            continue
        while True:
            s = "KV" + "".join(ALPHA[int(x)] for x in r.integers(0, len(ALPHA), 9))
            if s not in used:
                used.add(s)
                break
        built = p.built + dt.timedelta(days=float(r.uniform(2.0, 12.0)))
        shipped = (built + dt.timedelta(days=float(r.uniform(1.0, 24.0)))).replace(hour=0, minute=0, second=0,
                                                                                  microsecond=0)
        reg = REGION_MIX[int(np.searchsorted(np.cumsum([w for _, w in REGION_MIX]), r.random()))][0]
        cs = COUNTRIES[reg]
        country = cs[int(np.searchsorted(np.cumsum([w for _, w in cs]), r.random() * 0.999999))][0]
        model = "K14" if r.random() < 0.6 else "K15"
        act = shipped + dt.timedelta(days=float(4.0 + r.exponential(11.0)))
        use = float(math.exp(math.log(0.74) + 0.55 * r.normal()))
        nb = SimpleNamespace(serial=s, pack=p.serial, lot=p.lot, model=model, built=built, shipped=shipped,
                             region=reg, country=country, act=act, use=use, order="CUST" if r.random() < 0.72 else "CHAN",
                             refurb=None)
        if r.random() < 0.0092:
            back = shipped + dt.timedelta(days=float(r.uniform(6.0, 28.0)))
            again = (back + dt.timedelta(days=float(r.uniform(14.0, 40.0)))).replace(hour=0, minute=0, second=0,
                                                                                   microsecond=0)
            nb.refurb = again
            nb.act = again + dt.timedelta(days=float(4.0 + r.exponential(11.0)))
        nbs.append(nb)
    W.notebooks = nbs
    return nbs


def service_stock(W):
    """Service packs in stock, oldest first: a lot's SVC packs join the stock a week after they are built."""
    stock = sorted([p for p in W.field_packs if p.disp == "SVC"], key=lambda p: p.built)
    for p in stock:
        p.available = p.built + dt.timedelta(days=7)
    return stock


def events(W):
    """Walk every notebook through its service life to the extract: the fitted pack fails on capacity when its cycles
    reach its life; other battery events arrive at their rates. Each repair fits the oldest service pack in stock."""
    stock = service_stock(W)
    si = [0]
    pack_by = {p.serial: p for p in W.field_packs}
    r = K.rng("events", *EVENTS_KEY)
    rr = K.rng("service-pack-lives")
    sd_pred = math.sqrt((WD.B1 * WD.CELL_LNQ_SD) ** 2 + (WD.B2 * WD.DR_SD) ** 2)
    evs = []

    def take_stock(when):
        while si[0] < len(stock) and stock[si[0]].available > when:
            break
        p = stock[si[0]]
        si[0] += 1
        if not hasattr(p, "life"):
            mq, mr = W.lot_levels[p.lot]
            mu = WD.B0 + WD.B1 * mq + WD.B2 * mr
            t = rr.normal(0.0, WD.SD_TRAY)
            cells = mu + rr.normal(0.0, sd_pred, 3) + t + rr.normal(0.0, WD.SD_CELL, 3)
            p.life = float(math.exp(cells.min()))
        return p

    order = sorted(W.notebooks, key=lambda n: n.act)
    for nb in order:
        cur = pack_by[nb.pack]
        fit_t = nb.act            # the current pack's cycle clock starts here
        t0 = nb.act
        guard = 0
        while guard < 6:
            guard += 1
            # next event time for each kind, from t0
            yrs = lambda rate: min(float(r.exponential(1.0 / rate)) * 365.25, 9000.0)
            t_cap = fit_t + dt.timedelta(days=min(cur.life / nb.use, 9000.0))
            cands = [("CAP", t_cap)]
            for code, rate in (("SWL", SWELL_RATE), ("CON", CONTACT_RATE), ("BMS", GAUGE_RATE), ("NFF", NFF_RATE)):
                cands.append((code, t0 + dt.timedelta(days=yrs(rate))))
            code, tf = min(cands, key=lambda x: x[1])
            if tf > END:
                break
            cycles = (tf - fit_t).total_seconds() / 86400.0 * nb.use
            ev = SimpleNamespace(nb=nb, code=code, t_fail=tf, cycles=int(cycles), removed=cur.serial, region=nb.region)
            if code == "CAP":
                if cycles <= K.WARRANTY_CYCLES:
                    if r.random() < 0.05:        # the owner never asks
                        break
                    ev.warranty = "WTY"
                else:
                    u = r.random()
                    if u < 0.14:
                        ev.warranty = "GW"
                    elif u < 0.36:
                        ev.warranty = "OOW"
                    else:
                        break
                ev.fcc = float(r.uniform(74.5, 79.9))
            elif code == "NFF":
                ev.warranty = "WTY"
                ev.fcc = float(r.uniform(80.4, 86.0))
            else:
                ev.warranty = "WTY"
                ev.fcc = float(r.uniform(84.0, 98.5))
            lag = 1.0 + r.exponential(15.0) if code in ("CAP", "NFF") else 0.5 + r.exponential(4.0)
            ev.opened = tf + dt.timedelta(days=lag)
            turn = (6.0 + r.gamma(2.0, 2.6)) if nb.region == "DACH" else (2.5 + r.gamma(2.0, 1.9))
            ev.closed = ev.opened + dt.timedelta(days=turn)
            if ev.opened > END:
                break
            ev.labour_min = int(round(r.normal(34.0, 6.0) if code != "NFF" else r.normal(21.0, 4.0)))
            if code == "NFF":
                ev.fitted = None
                evs.append(ev)
                t0 = ev.closed
                continue
            if ev.closed > END:
                ev.closed = None       # still open at the extract
                ev.fitted = None
                evs.append(ev)
                break
            newp = take_stock(ev.closed)
            ev.fitted = newp.serial
            evs.append(ev)
            cur = newp
            fit_t = ev.closed
            t0 = ev.closed
    W.events = evs
    return evs


def systems(W):
    """Where each event is recorded. The DACH depot kept its service orders in SAP until 1 March 2026 and works in the
    service case system from 2 March; orders created from 1 September 2025 were migrated into the case system with
    their SAP order number. The partners record their cases in the case system throughout."""
    r = K.rng("systems")
    mig_from = dt.datetime(2025, 9, 1)
    cut = dt.datetime.combine(K.MIGRATION, dt.time(0, 0))
    sap, cases = [], []
    nsap = 4_000_118_400
    ncase = {}

    def case_no(when):
        y = when.year % 100
        ncase[y] = ncase.get(y, 0) + int(r.integers(1, 4))
        return "KS%02d-%06d" % (y, 12000 + ncase[y])

    for ev in sorted(W.events, key=lambda e: e.opened):
        if ev.region == "DACH" and ev.opened < cut:
            nsap += int(r.integers(1, 6))
            ev.sap = nsap
            sap.append(ev)
            if ev.opened >= mig_from:
                ev.case = case_no(dt.datetime(2026, 3, 2))
                ev.migrated = True
                cases.append(ev)
            else:
                ev.case = None
                ev.migrated = False
        else:
            ev.sap = None
            ev.migrated = False
            ev.case = case_no(ev.opened)
            cases.append(ev)
    # a partner's case is closed when the warranty desk approves the partner's claim for it, some business days after
    # the repair; the depot closes its own cases when the repair is done
    rc = K.rng("claim-approval")
    for ev in sorted(W.events, key=lambda e: e.opened):
        if ev.closed is None:
            ev.case_closed = None
            continue
        if ev.region == "DACH":
            # the depot closes its case when the repair is done, in its working day
            off = K.cet_offset(ev.closed)
            loc = ev.closed + dt.timedelta(hours=off)
            if loc.hour < 7 or loc.hour >= 17:
                loc = dt.datetime.combine(loc.date(), dt.time(7, 5)) + dt.timedelta(minutes=int(rc.integers(0, 590)))
            ev.closed = loc - dt.timedelta(hours=off)
            ev.case_closed = ev.closed
            continue
        if ev.warranty == "OOW":
            # paid repairs close when the customer has paid and collected
            t = ev.closed + dt.timedelta(days=1.0 + float(rc.gamma(2.0, 1.8)))
            while t.weekday() >= 5:
                t += dt.timedelta(days=1)
            ev.case_closed = dt.datetime.combine(t.date(), dt.time(6, 30)) + dt.timedelta(minutes=int(rc.integers(0, 600)))
        else:
            ev.case_closed = "claim"     # closed when the warranty desk approves the partner's invoice (invoices())
    W.sap_orders = sap
    W.cases = cases
    return sap, cases


def returns(W):
    """The returns depot in Bielefeld receives the batteries the repairs removed, consignment by consignment: each
    partner sends its removed batteries weekly, the DACH depot hands them over daily. Swollen batteries are scrapped
    where they are removed and never travel; a few others never arrive. The carrier bills each consignment once."""
    r = K.rng("returns")
    rows = []
    cons = []
    by_week = {}
    for ev in W.events:
        if ev.code in ("NFF", "SWL") or ev.fitted is None or ev.closed is None:
            continue
        if r.random() < 0.055:
            continue
        wk = ev.closed.isocalendar()[:2]
        key = (PARTNER[ev.region], wk) if ev.region != "DACH" else ("KVD", ev.closed.date())
        by_week.setdefault(key, []).append(ev)
    ncons = 77_310_000
    for key, evs in sorted(by_week.items(), key=lambda kv: (min(e.closed for e in kv[1]), kv[0][0])):
        last = max(e.closed for e in evs)
        pickup = last.date() + dt.timedelta(days=int(r.integers(1, 4)))
        while pickup.weekday() >= 5:
            pickup += dt.timedelta(days=1)
        ncons += int(r.integers(3, 40))
        cno = "%d" % ncons
        n = len(evs)
        partner = key[0]
        if partner == "KVD":
            charge = 0.0
        else:
            base = {"SVT": 21.40, "HRL": 34.80, "NFX": 39.60, "RPS": 27.90}[partner]
            charge = round(base + 2.35 * n + float(r.normal(0.0, 0.6)), 2)
        recv = pickup + dt.timedelta(days=int(r.integers(1, 5)))
        while recv.weekday() >= 5:
            recv += dt.timedelta(days=1)
        cons.append(SimpleNamespace(no=cno, partner=partner, pickup=pickup, received=recv, n=n, charge=charge,
                                    country=evs[0].nb.country, weight=round(n * 0.31 + 0.4, 1)))
        for ev in evs:
            ev.consignment = cno
            depot_fcc = ev.fcc + float(r.normal(0.6, 0.9)) if ev.code == "CAP" else ev.fcc + float(r.normal(0.0, 0.8))
            rows.append(SimpleNamespace(ev=ev, cons=cno, received=recv, serial=ev.removed, fcc=round(depot_fcc, 1),
                                        charge=charge, partner=partner))
    W.returns = rows
    W.consignments = cons
    return rows, cons


def simulate_field(W):
    build_packs(W)
    pack_lives(W)
    notebooks(W)
    events(W)
    systems(W)
    returns(W)
    return W


if __name__ == "__main__":
    import collections
    W = WD.simulate()
    simulate_field(W)
    print("packs", len(W.field_packs), "notebooks", len(W.notebooks), "events", len(W.events))
    c = collections.Counter((e.code, e.warranty) for e in W.events)
    print(c)
    cap = [e for e in W.events if e.code == "CAP" and e.warranty == "WTY" and e.closed is not None]
    orig = {nb.pack for nb in W.notebooks}
    by = collections.Counter(next(p.lot for p in [None] if False) if False else e.nb.lot for e in cap if e.removed in orig)
    for lot in K.ASK_LOTS:
        n_ship = sum(1 for nb in W.notebooks if nb.lot == lot)
        print(lot, by.get(lot, 0), n_ship, "%.2f%%" % (100 * by.get(lot, 0) / n_ship))
    print("sap", len(W.sap_orders), "cases", len(W.cases), "migrated", sum(1 for e in W.cases if e.migrated))
    print("returns", len(W.returns), "consignments", len(W.consignments))


# ---------------------------------------------------------------------------------------------------- money
FEES = {   # partner: currency, labour, handling, diagnosis only (no fault found)
    "SVT": ("EUR", 38.85, 6.00, 24.00),
    "HRL": ("GBP", 34.00, 5.50, 21.00),
    "NFX": ("SEK", 514.0, 75.0, 310.0),
    "RPS": ("EUR", 35.85, 5.00, 22.00),
}
PARTNER_NAME = {"SVT": "Dauvergne Réparation SAS", "HRL": "Tolley Marsh Repair Ltd", "NFX": "Ljungqvist Service AB",
                "RPS": "Ferrucci Assistenza S.r.l."}
PARTNER_CODE = {"SVT": "DVG", "HRL": "TMR", "NFX": "LJQ", "RPS": "FRC", "KVD": "KVD"}   # the vendor codes the systems write
PARTNER_CITY = {"SVT": ("Lille", "FR"), "HRL": ("Sheffield", "GB"), "NFX": ("Jönköping", "SE"),
                "RPS": ("Bologna", "IT")}
INV_PREFIX = {"SVT": "DVG-F", "HRL": "TM-", "NFX": "LJQ-", "RPS": "FA/"}
PACK_COST = [(dt.date(2025, 10, 1), 52.40), (dt.date(2026, 1, 1), 49.80)]
DEPOT_PRICE = [(dt.date(2025, 10, 1), 31.60), (dt.date(2026, 1, 1), 33.10)]
COLLECTION_FEE = 12.80


def valid(table, d):
    v = None
    for start, x in table:
        if d >= start:
            v = x
    return v


def month_ends(first, last):
    out = []
    y, m = first
    while (y, m) <= last:
        nm = dt.date(y + (m // 12), m % 12 + 1, 1)
        out.append(nm - dt.timedelta(days=1))
        y, m = nm.year, nm.month
    return out


def fx_rates():
    """Treasury's month-end rates, units of each currency per euro, January 2025 to September 2026."""
    r = K.rng("fx")
    out = {}
    g, s = 0.8412, 11.212
    for m in month_ends((2025, 1), (2026, 9)):
        g = g * math.exp(r.normal(0.0004, 0.0085))
        s = s * math.exp(r.normal(-0.0006, 0.0105))
        out[(m.year, m.month)] = {"GBP": round(g, 4), "SEK": round(s, 4), "CHF": round(0.9421 + r.normal(0, 0.004), 4),
                                  "NOK": round(11.62 + r.normal(0, 0.09), 4), "DKK": round(7.4605 + r.normal(0, 0.0012), 4)}
    return out


def invoices(W):
    """Each partner's monthly invoice for the jobs it carried out in the month, September 2025 to September 2026: one line
    per repair under the warranty or as goodwill (no-fault-found cases at the diagnosis fee). Tolley Marsh Repair's
    March 2026 invoice went out with the old handling fee and one job twice; it was reissued as TM-2603-R1."""
    r = K.rng("invoices")
    inv = {p: [] for p in FEES}
    start = dt.datetime(2025, 9, 1)
    for ev in sorted(W.cases, key=lambda e: (e.closed or END, e.case)):
        if ev.region == "DACH" or ev.closed is None or ev.closed < start or ev.closed > END:
            continue
        if ev.warranty == "OOW":
            continue
        p = FD_PARTNER(ev.region)
        cur, lab, hand, diag = FEES[p]
        if ev.code == "NFF":
            line = (diag, 0.0)
        else:
            line = (lab, hand)
        inv[p].append(SimpleNamespace(ev=ev, labour=line[0], handling=line[1], month=(ev.closed.year, ev.closed.month)))
    jobs = {p: 0 for p in FEES}
    seeds = {"SVT": 40100, "HRL": 117500, "NFX": 2600, "RPS": 9300}
    for p, lines in inv.items():
        jobs[p] = seeds[p]
        for ln in sorted(lines, key=lambda x: (x.month, x.ev.closed, x.ev.case)):
            jobs[p] += int(r.integers(1, 9))
            ln.job = ("%s%06d" % ({"SVT": "DV", "HRL": "TMJ", "NFX": "", "RPS": "FA-"}[p], jobs[p]))
    W.invoices = inv
    # each partner invoices a month's jobs early in the next month, and the warranty desk closes the month's cases when
    # it approves the invoice; Tolley Marsh's March 2026 invoice was queried and approved only as reissued
    W.invoice_issue, W.invoice_approved, W.invoice_reissue = {}, {}, {}
    for p in FEES:
        ri = K.rng("invoice-dates", p, *APPROVAL_KEY)
        for (y, m) in [(2024, mm) for mm in range(9, 13)] + [(2025, mm) for mm in range(1, 13)] + \
                      [(2026, mm) for mm in range(1, 10)]:
            nm = dt.date(y + (m // 12), m % 12 + 1, 1)
            d = nm + dt.timedelta(days=int(ri.integers(2, 7)))
            while d.weekday() >= 5:
                d += dt.timedelta(days=1)
            W.invoice_issue[(p, y, m)] = d
            a = d + dt.timedelta(days=3 + int(ri.gamma(2.0, 5.5)))
            if p == "HRL" and (y, m) == (2026, 3):
                re = d + dt.timedelta(days=16)
                while re.weekday() >= 5:
                    re += dt.timedelta(days=1)
                W.invoice_reissue[(p, y, m)] = re
                a = re + dt.timedelta(days=int(ri.integers(3, 7)))
            while a.weekday() >= 5:
                a += dt.timedelta(days=1)
            W.invoice_approved[(p, y, m)] = a
    rc = K.rng("claim-close-times")
    for ev in sorted(W.events, key=lambda e: (e.opened, e.nb.serial)):
        if getattr(ev, "case_closed", None) == "claim":
            if ev.closed > END:
                ev.case_closed = None         # a diagnosis finished after the extract
                continue
            a = W.invoice_approved[(PARTNER[ev.region], ev.closed.year, ev.closed.month)]
            ev.case_closed = dt.datetime.combine(a, dt.time(7, 0)) + dt.timedelta(minutes=int(rc.integers(0, 540)))
    return inv


def FD_PARTNER(region):
    return PARTNER[region]


def simulate_money(W):
    W.fx = fx_rates()
    invoices(W)
    return W
