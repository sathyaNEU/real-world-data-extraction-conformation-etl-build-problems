"""Supply of Lyrevo: wholesaler sell-in for the retail channel, the 3PL's hospital tender call-offs in France,
Italy and Spain, returns, free goods, and the finance view of the same shipments."""
import datetime as dt
import math

import numpy as np

import world as W

TD = dt.timedelta
D = dt.date
EXTRACT_END = W.EXPORT

PRES = {  # EU number suffix: (strength mg, pack size)
    "001": (15, 28), "002": (15, 84), "003": (30, 28), "004": (30, 84),
}
EU = "EU/1/23/1754/"

# national codes per market and presentation (formats as each market's system writes them)
CODES = {
    "DK": ("VNR", {"001": "412578", "002": "412589", "003": "412592", "004": "412604"}),
    "SE": ("VNR", {"001": "412578", "002": "412589", "003": "412592", "004": "412604"}),
    "NO": ("VNR", {"001": "412578", "002": "412589", "003": "412592", "004": "412604"}),
    "FI": ("VNR", {"001": "412578", "002": "412589", "003": "412592", "004": "412604"}),
    "DE": ("PZN", {"001": "04718263", "002": "04718286", "003": "17346921", "004": "04718292"}),
    "AT": ("PZN-AT", {"001": "5491237", "002": "5491243", "003": "5491266", "004": "5491272"}),
    "NL": ("ZI", {"001": "16924811", "002": "16924838", "003": "16924846", "004": "16924854"}),
    "BE": ("CNK", {"001": "4687213", "002": "4687221", "003": "4687239", "004": "4687247"}),
    "FR": ("CIP13", {"001": "3400930271842", "002": "3400930271859", "003": "3400930271866", "004": "3400930271873"}),
    "IT": ("AIC", {"001": "049871014", "002": "049871026", "003": "049871038", "004": "049871040"}),
    "ES": ("CN", {"001": "741258.3", "002": "741259.0", "003": "741260.6", "004": "741261.3"}),
    "PL": ("GTIN", {"001": "5909991482316", "002": "5909991482323", "003": "5909991482330", "004": "5909991482347"}),
    "PT": ("REG", {"001": "5824319", "002": "5824327", "003": "5824335", "004": "5824343"}),
}
HOSP_GTIN = {
    "FR": {"001": "03400930271842", "002": "03400930271859", "003": "03400930271866", "004": "03400930271873"},
    "IT": {"001": "08058926104116", "002": "08058926104123", "003": "08058926104130", "004": "08058926104147"},
    "ES": {"001": "08470007412583", "002": "08470007412590", "003": "08470007412606", "004": "08470007412613"},
}
WHOLESALERS = {
    "DK": ["Kattegat Pharma Distribution A/S", "Øresund Medicin Engros ApS"],
    "SE": ["Svealand Läkemedelsdistribution AB"], "NO": ["Fjordlegemidler AS"], "FI": ["Saimaan Lääketukku Oy"],
    "DE": ["Elbe-Weser Pharmagroßhandel GmbH", "Isartal Arzneimittel-Logistik GmbH", "Rheinauen Pharma GmbH"],
    "AT": ["Donaupharm Großhandel GmbH"], "NL": ["Polder Farmaceutische Groothandel B.V."],
    "BE": ["Scheldepharma NV"], "FR": ["Répartition Pharmaceutique Rhône-Ouest SAS"],
    "IT": ["Distribuzione Farmaci Padana S.p.A."], "ES": ["Distribuidora Farmacéutica Levante S.L."],
    "PL": ["Hurtownia Farmaceutyczna Wisła Sp. z o.o."], "PT": ["Distribuidora Farmacêutica do Tejo, Lda."],
}
STRIPPED_PZN_WHOLESALER = "Elbe-Weser Pharmagroßhandel GmbH"
HOSPITAL_SHARE = 0.80
CASE_PACKS = 10
NET_PRICE = {"001": 1182.0, "002": 3418.0, "003": 2246.0, "004": 6472.0}
MARKET_PRICE = {"DK": 1.04, "SE": 1.02, "NO": 1.06, "FI": 1.01, "DE": 1.08, "AT": 1.00, "NL": 0.97, "BE": 0.95,
                "FR": 0.92, "IT": 0.90, "ES": 0.88, "PL": 0.78, "PT": 0.86}
TENDER_DISC = {"FR": 0.17, "IT": 0.21, "ES": 0.19}
REGIONS = {
    "FR": ["Auvergne-Rhône-Alpes", "Île-de-France", "Nouvelle-Aquitaine", "Occitanie", "Hauts-de-France", "Grand Est",
           "Provence-Alpes-Côte d'Azur", "Bretagne", "Pays de la Loire"],
    "IT": ["Lombardia", "Lazio", "Campania", "Veneto", "Emilia-Romagna", "Piemonte", "Toscana", "Sicilia", "Puglia"],
    "ES": ["Comunidad de Madrid", "Cataluña", "Andalucía", "Comunitat Valenciana", "Galicia", "País Vasco",
           "Castilla y León"],
}


def persistence(t):
    """Share of patients still on treatment t days after the first dose (58 per cent at a year)."""
    return np.exp(-(np.maximum(t, 0) / 780.0) ** 0.8)


def daily_demand():
    """Patient-days per market and day, split by strength and by pack size used."""
    days = [W.LAUNCH + TD(days=i) for i in range((EXTRACT_END - W.LAUNCH).days + 1)]
    n = len(days)
    t = np.arange(n)
    P = persistence(t)
    out = {}
    for c in W.MARKET_ORDER:
        starts = np.zeros(n)
        for w in W.weeks():
            s = W.weekly_starts(w, c)
            i = (w - W.LAUNCH).days
            if s > 0 and i < n:
                starts[i:i + 7] += s / 7.0
        on = np.convolve(starts, P)[:n]
        # 30 mg share rises as patients are escalated; 84-tablet packs once a patient is established
        early = np.convolve(starts, (t < 90).astype(float) * P)[:n]
        late = on - early
        s30 = 0.10 * early + 0.37 * late
        p84 = 0.68 * late
        out[c] = dict(days=days, on=on, d30=s30, d15=on - s30, p84=p84, starts=starts)
    return out


def months_between(a, b):
    out = []
    y, m = a.year, a.month
    while (y, m) <= (b.year, b.month):
        out.append((y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def _cumround(vals):
    out, cum, prev = [], 0.0, 0
    for v in vals:
        cum += v
        r = int(math.floor(cum + 0.5))
        out.append(r - prev)
        prev = r
    return out


SCALE_PRE = 0.99668  # demand before the reporting interval
SCALE_INT = 0.98732  # demand in the reporting interval and after
S30 = 1.39          # share of patient-days on the 30 mg tablet
COVER = 35.0
RET_SHARE = 0.035    # returned share of an invoice line, where a return follows
STARTER = 1.4        # free 28-tablet PSP bridging packs per new patient
POST_DAYS = 6        # days of October 2026 in the extracts


def build(rng_seed=254):
    """Return (sell-in rows, call-off rows, finance rows, truth) with quantities in packs (sell-in) and
    shipper cases (call-offs)."""
    g = np.random.default_rng([254, 900])
    dem = daily_demand()
    sellin, calloff = [], []
    fin = {}
    for c in W.MARKET_ORDER:
        dd = dem[c]
        days = dd["days"]
        launch = W.MARKETS[c][0]
        mlist = months_between(launch, EXTRACT_END)
        hosp = HOSPITAL_SHARE if c in W.HOSPITAL_MARKETS else 0.0
        # monthly demand in tablets by presentation
        mon = {}
        for (y, m) in mlist:
            idx = [i for i, d in enumerate(days) if d.year == y and d.month == m
                   and not ((y, m) == (EXTRACT_END.year, EXTRACT_END.month) and d.day > POST_DAYS)]
            d15 = float(dd["d15"][idx].sum())
            d30 = float(dd["d30"][idx].sum())
            on = float(dd["on"][idx].sum())
            f84 = float(dd["p84"][idx].sum()) / on if on > 0 else 0.0
            new = float(dd["starts"][idx].sum())
            sc = SCALE_INT if (y, m) >= (2025, 10) else SCALE_PRE
            d30s = d30 * S30
            d15, d30 = (d15 + d30 - d30s) * sc, d30s * sc
            mon[(y, m)] = {"001": d15 * (1 - f84), "002": d15 * f84, "003": d30 * (1 - f84), "004": d30 * f84,
                           "new": new, "ndays": len(idx)}
        # retail channel through wholesalers: demand plus the change in their stock (35 days of cover)
        whs = WHOLESALERS[c]
        wsh = {1: [1.0], 2: [0.58, 0.42], 3: [0.44, 0.34, 0.22]}[len(whs)]
        prev_stock = {p: 0.0 for p in PRES}
        retail = {}
        for (y, m) in mlist:
            row = mon[(y, m)]
            for p in PRES:
                dmd = row[p] * (1 - hosp)
                per_day = dmd / max(row["ndays"], 1)
                stock = COVER * per_day if (y, m) != (EXTRACT_END.year, EXTRACT_END.month) else prev_stock[p]
                retail[(y, m, p)] = max(0.0, dmd + stock - prev_stock[p])
                prev_stock[p] = stock
        for p in PRES:
            packs = _cumround([retail[(y, m, p)] / PRES[p][1] for (y, m) in mlist])
            for (y, m), q in zip(mlist, packs):
                for wi, wname in enumerate(whs):
                    qq = _cumround([q * s for s in wsh])[wi] if len(whs) > 1 else q
                    if qq <= 0:
                        continue
                    price = round(NET_PRICE[p] * MARKET_PRICE[c], 2)
                    # stock later returned (short-dated, damaged) was invoiced first
                    rq = int(round(qq * RET_SHARE * (0.6 + 0.8 * g.random()))) if g.random() < 0.55 else 0
                    sellin.append(dict(market=c, wholesaler=wname, period="%04d-%02d" % (y, m), pres=p, doc="F2",
                                       qty=qq + rq, value=round((qq + rq) * price, 2), reason=""))
                    fin[(c, y, (m - 1) // 3 + 1)] = fin.get((c, y, (m - 1) // 3 + 1), 0.0) + (qq + rq) * price
                    # returns credited one or two months later
                    if True:
                        if rq > 0:
                            lag = 1 + int(g.random() * 2)
                            yy, mmn = y + (m + lag - 1) // 12, (m + lag - 1) % 12 + 1
                            if (yy, mmn) <= (EXTRACT_END.year, EXTRACT_END.month):
                                sellin.append(dict(market=c, wholesaler=wname, period="%04d-%02d" % (yy, mmn), pres=p,
                                                   doc="RE", qty=-rq, value=-round(rq * price, 2),
                                                   reason="Return - short expiry" if g.random() < 0.7 else "Return - damaged"))
                                key = (c, yy, (mmn - 1) // 3 + 1)
                                fin[key] = fin.get(key, 0.0) - rq * price
                    if g.random() < 0.18:
                        fq = 1 + int(g.random() * max(1, qq * 0.01))
                        sellin.append(dict(market=c, wholesaler=wname, period="%04d-%02d" % (y, m), pres=p, doc="FOC",
                                           qty=fq, value=0.0, reason="Replacement - damaged in transit"))
        # PSP bridging packs (15 mg x 28), free of charge through the wholesaler, while reimbursement is arranged
        if c in ("DE", "NL", "DK", "SE", "NO", "FI", "AT"):
            st = _cumround([mon[k]["new"] * STARTER for k in mlist])
            for (y, m), q in zip(mlist, st):
                if q > 0:
                    sellin.append(dict(market=c, wholesaler=whs[0], period="%04d-%02d" % (y, m), pres="001", doc="FOC",
                                       qty=q, value=0.0, reason="PSP bridging pack"))
        # hospital channel: the 3PL's call-offs against regional tenders, in shipper cases of 10 packs
        if hosp > 0:
            regs = REGIONS[c]
            rw = g.dirichlet(np.ones(len(regs)) * 6)
            for p in PRES:
                for ri, reg in enumerate(regs):
                    vals, dates = [], []
                    for (y, m) in mlist:
                        row = mon[(y, m)]
                        q = row[p] * hosp * rw[ri] / PRES[p][1] / CASE_PACKS
                        if (y, m) == (EXTRACT_END.year, EXTRACT_END.month):
                            ds = [D(y, m, dd) for dd in (2, 6) if dd <= POST_DAYS] or [D(y, m, 1)]
                        else:
                            ds = [D(y, m, 3 + int(g.random() * 4)), D(y, m, 17 + int(g.random() * 4))]
                            if (y, m) == (launch.year, launch.month):
                                q *= 2.2
                        for dte in ds:
                            if dte < launch:
                                continue
                            vals.append(q / len(ds))
                            dates.append(dte)
                    cases = _cumround(vals)
                    for dte, qc in zip(dates, cases):
                        if qc <= 0:
                            continue
                        calloff.append(dict(market=c, region=reg, date=dte, pres=p, cases=qc,
                                            hosp="%s-H%03d" % (c, 101 + ri * 7 + int(g.random() * 5))))
                        price = NET_PRICE[p] * MARKET_PRICE[c] * (1 - TENDER_DISC[c])
                        key = (c, dte.year, (dte.month - 1) // 3 + 1)
                        fin[key] = fin.get(key, 0.0) + qc * CASE_PACKS * price
    return sellin, calloff, fin
