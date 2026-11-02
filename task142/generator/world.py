"""The clean truth of the task142 world, before any export mess or document is written.

Warmtenet West is a secondary district heating network fed by Stadswarmte Lekstede's OS West station on a
weather-compensated supply curve (90 C at a daily mean of 0 C and below). Its connections run in four installation
regimes that no file names: original radiator systems in pre-1985 blocks (high returns), pre-1985 blocks renovated
before they were connected (insulated, low-temperature emitters), post-1985 residential, and non-residential
buildings. Woonstichting Weidehaven connects fifteen 1960s blocks in six phases in 2027 and 2028, keeping each
block's piping and radiators. Everything here is generated forward from a fixed seed; nothing is fitted to an
answer except the two free parameters tune() sets (the station's design flow and one block load per phase).
"""
import datetime as dt
import math

import numpy as np

import params as P

D = dt.date
TD = dt.timedelta


def days():
    d, out = P.METER_START, []
    while d <= P.METER_END:
        out.append(d)
        d += TD(days=1)
    return out


def nl_offset_hours(t_utc):
    """CET/CEST offset (hours ahead of UTC) for a UTC datetime: CEST from 01:00 UTC on the last Sunday of March to
    01:00 UTC on the last Sunday of October."""
    y = t_utc.year

    def last_sunday(m):
        d = D(y, m, 31)
        while d.weekday() != 6:
            d -= TD(days=1)
        return dt.datetime(d.year, d.month, d.day, 1, 0)
    return 2 if last_sunday(3) <= t_utc < last_sunday(10) else 1


# ------------------------------------------------------------------------------------------------- weather
def weather(rng):
    """Hourly outdoor temperature in local time and the daily TG/TN/TX in tenths of a degree (local days)."""
    ds = days()
    n = len(ds)
    doy = np.array([d.timetuple().tm_yday for d in ds])
    base = 10.6 - 7.6 * np.cos(2 * np.pi * (doy - 22) / 365.25)
    anom = np.zeros(n)
    e = rng.normal(0, 2.35, n)
    for i in range(n):
        anom[i] = (0.78 * anom[i - 1] if i else 0.0) + e[i]
    # the winter's two cold spells (a January easterly and a late-February frost)
    for i, d in enumerate(ds):
        if D(2026, 1, 5) <= d <= D(2026, 1, 24):
            k = (d - D(2026, 1, 5)).days
            anom[i] += -7.4 * math.sin(math.pi * (k + 1) / 21) - 1.2
        if D(2026, 2, 17) <= d <= D(2026, 2, 27):
            k = (d - D(2026, 2, 17)).days
            anom[i] += -6.9 * math.sin(math.pi * (k + 1) / 12)
        if D(2025, 12, 1) <= d <= D(2025, 12, 9):
            k = (d - D(2025, 12, 1)).days
            anom[i] += -4.6 * math.sin(math.pi * (k + 1) / 10)
    daily = base + anom
    amp = 2.4 + 2.2 * (1 + np.cos(2 * np.pi * (doy - 196) / 365.25)) / 2 + rng.uniform(-0.6, 0.6, n)
    hourly = {}
    tg, tn, tx = [], [], []
    for i, d in enumerate(ds):
        hs = []
        for h in range(24):
            v = daily[i] + amp[i] * math.cos(2 * math.pi * (h - 15) / 24) + rng.normal(0, 0.35)
            hs.append(v)
        hs = np.array(hs)
        hs = hs - hs.mean() + daily[i]
        hourly[d] = hs
        tg.append(int(round(hs.mean() * 10)))
        tn.append(int(math.floor(hs.min() * 10 - rng.uniform(0, 6))))
        tx.append(int(math.ceil(hs.max() * 10 + rng.uniform(0, 6))))
    return {"days": ds, "tg": np.array(tg), "tn": np.array(tn), "tx": np.array(tx), "hourly_local": hourly}


def supply_curve(tout):
    return float(np.clip(90.0 - 1.2 * tout, 70.0, 90.0))


# ------------------------------------------------------------------------------------------------- network
STREETS = {
    "poets": ["Vondelstraat", "Bilderdijklaan", "Da Costastraat", "Potgieterstraat", "Beetsstraat", "Hooftlaan",
              "Huygensstraat", "Tollensstraat", "Staringlaan", "Brederodestraat", "Cats­laan", "Multatulistraat",
              "Gorterstraat", "Van Eedenlaan", "Perkstraat", "Kloosstraat", "Verweylaan", "Boutensstraat",
              "Marsmanplein", "Nijhofflaan"],
    "flowers": ["Goudsbloemstraat", "Klaprooslaan", "Korenbloemhof", "Zonnebloemstraat", "Lavendelhof",
                "Akeleistraat", "Margrietlaan", "Anjerstraat", "Tulpstraat", "Narcissenhof", "Irisstraat",
                "Seringenlaan", "Asterstraat", "Primulahof", "Dahliastraat"],
    "harbour": ["Havenkade", "Dokweg", "Kraanplein", "Ankerstraat", "Steigerweg", "Werfkade", "Kademuur",
                "Sluiswachter", "Loswal", "Meerpaal", "Boeiweg", "Zeilmakerij", "Touwbaan", "Scheepmakershof",
                "Lichtschip", "Kompasweg", "Roerkade", "Spantstraat", "Kielweg", "Bolderstraat"],
    "birds": ["Kievitlaan", "Merelstraat", "Spreeuwenhof", "Leeuwerikstraat", "Zwaluwlaan", "Reigerstraat",
              "Roerdomplaan", "Fazantstraat", "Lijsterlaan", "Vinkenstraat", "Meeuwenlaan", "Kwartelstraat",
              "Grutto­laan", "Wulpstraat", "Pluvierlaan"],
}
WIJKEN_OLD = ["Dichterswijk", "Bloemenbuurt", "Lindenhof", "Oud-West", "Rijnzicht"]
WIJKEN_NEW = ["Havenkwartier", "Werfeiland", "Kadewijk"]
UTIL_NAMES = [("Basisschool De Wilgenhoek", 1979), ("Sporthal Westerpark", 1991), ("Zorgcentrum Rijnhove", 1983),
              ("Kantoor Havenpoort", 2009), ("Brede school Werfeiland", 2016), ("Zwembad De Kade", 1998),
              ("Wijkcentrum Lindenhof", 1975), ("ROC Lekstede locatie West", 2012), ("Gezondheidscentrum Kadewijk", 2019),
              ("Bedrijfsverzamelgebouw Dokpoort", 2005), ("Kinderdagverblijf Het Anker", 2021),
              ("Politiebureau West", 1994)]


def clean(s):
    return s.replace("­", "")


def connections(rng):
    """The network's 118 connections in service on 1 October 2025 with their installation regime (truth only)."""
    out = []
    used = set()

    def addr(fam, lo=2, hi=180):
        streets = STREETS[fam]
        while True:
            st = clean(streets[int(rng.integers(len(streets)))])
            a = int(rng.integers(lo, hi)) // 2 * 2 + (int(rng.integers(0, 2)) if fam == "harbour" else 0)
            span = int(rng.choice([16, 24, 32, 40, 48, 56, 64]))
            key = (st, a // 70)
            if key in used:
                continue
            used.add(key)
            return st, a, a + span - 2 if fam != "harbour" else a

    spec = [("HT", 19), ("REN", 31), ("LT", 56), ("UTIL", 12)]
    k = 0
    for reg, n in spec:
        for j in range(n):
            c = {"regime": reg}
            if reg in ("HT", "REN"):
                c["cat"] = "Woningen"
                c["bouwjaar"] = int(rng.integers(1951, 1985))
                fam = "poets" if rng.random() < 0.55 else ("flowers" if rng.random() < 0.7 else "birds")
                st, a, b = addr(fam)
                c["object"] = "Flat %s %d-%d" % (st, a, b) if rng.random() < 0.7 else "Complex %s %d t/m %d" % (st, a, b)
                c["adres"] = "%s %d" % (st, a)
                c["wijk"] = WIJKEN_OLD[int(rng.integers(len(WIJKEN_OLD)))]
                c["kw"] = int(np.clip(rng.lognormal(math.log(380 if reg == "HT" else 265), 0.33), 140, 760) // 5 * 5)
                c["aansluitdatum"] = D(int(rng.integers(2009, 2024)), int(rng.integers(1, 13)), int(rng.integers(1, 28)))
            elif reg == "LT":
                c["cat"] = "Woningen"
                c["bouwjaar"] = int(rng.choice([int(rng.integers(1986, 2008)), int(rng.integers(2008, 2025))],
                                               p=None))
                fam = "harbour" if c["bouwjaar"] >= 2005 else ("flowers" if rng.random() < 0.5 else "birds")
                st, a, b = addr(fam)
                if fam == "harbour":
                    c["object"] = "Appartementen %s %d" % (st, a) if rng.random() < 0.5 else "Woonblok %s %d" % (st, a)
                    c["wijk"] = WIJKEN_NEW[int(rng.integers(len(WIJKEN_NEW)))]
                else:
                    c["object"] = "Woningen %s %d-%d" % (st, a, b)
                    c["wijk"] = WIJKEN_OLD[int(rng.integers(len(WIJKEN_OLD)))]
                c["adres"] = "%s %d" % (st, a)
                c["kw"] = int(np.clip(rng.lognormal(math.log(300), 0.48), 60, 950) // 5 * 5)
                y0 = max(2009, c["bouwjaar"] + 1)
                c["aansluitdatum"] = D(min(2025, int(rng.integers(y0, y0 + 3))), int(rng.integers(1, 13)),
                                       int(rng.integers(1, 28)))
            else:
                name, by = UTIL_NAMES[j]
                c["cat"] = "Utiliteit"
                c["bouwjaar"] = by
                c["object"] = name
                fam = "harbour" if by >= 2005 else "poets"
                st, a, b = addr(fam)
                c["adres"] = "%s %d" % (st, a)
                c["wijk"] = WIJKEN_NEW[int(rng.integers(len(WIJKEN_NEW)))] if by >= 2005 else \
                    WIJKEN_OLD[int(rng.integers(len(WIJKEN_OLD)))]
                c["kw"] = int(np.clip(rng.lognormal(math.log(420), 0.45), 120, 1100) // 5 * 5)
                y0 = max(2009, by + 1)
                c["aansluitdatum"] = D(min(2025, int(rng.integers(y0, y0 + 4))), int(rng.integers(1, 13)),
                                       int(rng.integers(1, 28)))
            # cold-day drop of the installation (K) and the daily-noise scale
            if reg == "HT":
                c["d"] = float(np.clip(rng.normal(24.55, 0.82), 22.9, 26.3))
                c["sd"] = 0.42
            elif reg == "REN":
                c["d"] = float(np.clip(rng.normal(42.4, 2.2), 37.5, 47.5))
                c["sd"] = 0.75
            elif reg == "LT":
                c["d"] = float(np.clip(rng.normal(50.1, 2.5), 45.0, 56.0))
                c["sd"] = 0.8
            else:
                c["d"] = float(np.clip(rng.normal(39.2, 2.3), 34.5, 44.0))
                c["sd"] = 0.9
            c["u"] = float(rng.uniform(0.70, 0.88))
            c["lam"] = float(rng.uniform(0.22, 0.62))
            c["dhw"] = {"HT": 0.05, "REN": 0.045, "LT": 0.075, "UTIL": 0.02}[reg]
            c["tb"] = {"HT": 17.0, "REN": 16.0, "LT": 15.0, "UTIL": 16.5}[reg]
            out.append(c)
            k += 1
    order = rng.permutation(len(out))
    out = [out[i] for i in order]
    for i, c in enumerate(out):
        c["idx"] = i
    return out


def drop_of(c, tg, rng_eps):
    reg, d = c["regime"], c["d"]
    if tg <= 0:
        g = {"HT": 0.04, "REN": 0.08, "LT": 0.05, "UTIL": 0.10}[reg] * (tg + 2.5)
    elif tg <= 14:
        base = {"HT": 0.04, "REN": 0.08, "LT": 0.05, "UTIL": 0.10}[reg] * 2.5
        g = base + {"HT": 0.21, "REN": 0.14, "LT": 0.09, "UTIL": 0.17}[reg] * tg
    else:
        g = {"HT": -4.5, "REN": -9.0, "LT": -7.5, "UTIL": -11.0}[reg]
    return d + g + rng_eps


def load_fraction(c, tg):
    heat = max(0.0, (c["tb"] - tg) / (c["tb"] - P.DESIGN_TOUT))
    return (1 - c["dhw"]) * heat + c["dhw"]


def amr_truth(rng, wx, conns):
    """Daily truth per connection: energy (kWh), volume (m3), mean supply and return temperatures at the meter."""
    ds = wx["days"]
    tg = wx["tg"] / 10.0
    # station daily mean supply from the hourly curve (local hours are close enough to the UTC day for the mean)
    ts_station = np.array([np.mean([supply_curve(v) for v in wx["hourly_local"][d]]) for d in ds])
    rec = {}
    for c in conns:
        rows = []
        for i, d in enumerate(ds):
            phi = load_fraction(c, tg[i])
            e = c["kw"] * c["u"] * phi * 24 * float(np.exp(rng.normal(0, 0.035)))
            dt_ = drop_of(c, tg[i], float(rng.normal(0, c["sd"])))
            loss = c["lam"] * (1 + 2.6 * (1 - min(1.0, phi / 0.8)))
            ts = ts_station[i] - loss + float(rng.normal(0, 0.12))
            tr = ts - dt_
            v = e / (P.CP * dt_)
            rows.append((d, e, v, ts, tr))
        rec[c["idx"]] = rows
    return rec, ts_station


# ------------------------------------------------------------------------------------------------- converting blocks
BLOCKS = [
    # code, street, from, to, dwellings, build year, type, label, phase
    ("2104", "Kievitlaan", 2, 96, 96, 1964, "galerijflat", "E", 1),
    ("2105", "Kievitlaan", 98, 160, 64, 1964, "galerijflat", "E", 1),
    ("2111", "Reigerstraat", 1, 79, 80, 1966, "galerijflat", "F", 1),
    ("2112", "Roerdomplaan", 2, 112, 112, 1967, "galerijflat", "E", 2),
    ("2118", "Fazantstraat", 3, 65, 64, 1965, "portiekflat", "E", 2),
    ("2119", "Fazantstraat", 67, 129, 64, 1965, "portiekflat", "F", 2),
    ("2123", "Zwaluwlaan", 2, 88, 88, 1968, "galerijflat", "E", 3),
    ("2124", "Leeuwerikstraat", 1, 71, 72, 1969, "galerijflat", "D", 3),
    ("2130", "Spreeuwenhof", 2, 48, 48, 1963, "portiekflat", "F", 3),
    ("2131", "Merelstraat", 1, 47, 48, 1962, "portiekflat", "E", 3),
    ("2140", "Wulpstraat", 2, 48, 48, 1970, "portiekflat", "E", 4),
    ("2141", "Pluvierlaan", 1, 39, 40, 1971, "portiekflat", "E", 4),
    ("2146", "Grutto­laan", 2, 40, 40, 1969, "portiekflat", "F", 5),
    ("2147", "Kwartelstraat", 1, 31, 32, 1970, "portiekflat", "E", 5),
    ("2152", "Vinkenstraat", 2, 48, 48, 1968, "portiekflat", "E", 6),
]
PHASE_DATES = {1: D(2027, 5, 18), 2: D(2027, 7, 6), 3: D(2027, 9, 7), 4: D(2028, 5, 23), 5: D(2028, 7, 11),
               6: D(2028, 9, 5)}


def blocks(rng):
    out = []
    for code, st, a, b, dw, by, typ, lab, ph in BLOCKS:
        st = clean(st)
        kwd = rng.uniform(5.4, 6.3) if typ == "galerijflat" else rng.uniform(5.7, 6.7)
        load = int(round(dw * kwd))
        prelim = int(round(load * rng.uniform(1.03, 1.10)))
        out.append({"code": code, "street": st, "from": a, "to": b, "dwellings": dw, "bouwjaar": by, "type": typ,
                    "label": lab, "phase": ph, "load": load, "prelim": prelim,
                    "gfa": int(round(dw * rng.uniform(62, 74))),
                    "date": PHASE_DATES[ph] + TD(days=int(rng.integers(0, 15)))})
    return out


# ------------------------------------------------------------------------------------------------- station
def committed_flow(conns, amr):
    """The hydraulic study's committed design-day flow: each connection's contracted capacity over CP times its own
    metered drop on days at or below 0 C (procedure 3.2 for connections in service)."""
    tot = 0.0
    per = {}
    for c in conns:
        rows = amr[c["idx"]]
        dts = [ts - tr for (d, e, v, ts, tr) in rows if _tg_of(d) <= P.TG_WINDOW]
        dd = float(np.mean(dts))
        f = c["kw"] / (P.CP * dd)
        per[c["idx"]] = (dd, f)
        tot += f
    return tot, per


_TG = {}


def _tg_of(d):
    return _TG[d]


def build(seed=P.SEED):
    rng = np.random.default_rng(seed)
    wx = weather(rng)
    for d, t in zip(wx["days"], wx["tg"]):
        _TG[d] = t / 10.0
    conns = connections(rng)
    amr, ts_station = amr_truth(rng, wx, conns)
    blks = blocks(rng)
    w = {"wx": wx, "conns": conns, "amr": amr, "ts_station": ts_station, "blocks": blks, "rng": rng}
    return w


if __name__ == "__main__":
    w = build()
    tg = w["wx"]["tg"] / 10
    print("cold days", int((tg <= 0).sum()), "min TG", tg.min(), "coldest", w["wx"]["days"][int(tg.argmin())])
    print("TG<=-1", int((tg <= -1).sum()), "TG<=1", int((tg <= 1).sum()))
    from collections import Counter
    print(Counter(c["regime"] for c in w["conns"]))
    tot, per = committed_flow(w["conns"], w["amr"])
    print("committed", round(tot, 1), "sum kW", sum(c["kw"] for c in w["conns"]))
    print("blocks load", sum(b["load"] for b in w["blocks"]), [b["load"] for b in w["blocks"]])
