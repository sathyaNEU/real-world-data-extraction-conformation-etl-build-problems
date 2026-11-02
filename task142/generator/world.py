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
    e = rng.normal(0, 1.85, n)
    for i in range(n):
        anom[i] = (0.78 * anom[i - 1] if i else 0.0) + e[i]
    # the winter's two cold spells (a January easterly and a late-February frost)
    for i, d in enumerate(ds):
        if D(2026, 1, 5) <= d <= D(2026, 1, 24):
            k = (d - D(2026, 1, 5)).days
            anom[i] += -5.6 * math.sin(math.pi * (k + 1) / 21) - 0.8
        if D(2026, 2, 17) <= d <= D(2026, 2, 27):
            k = (d - D(2026, 2, 17)).days
            anom[i] += -5.2 * math.sin(math.pi * (k + 1) / 12)
        if D(2025, 12, 1) <= d <= D(2025, 12, 9):
            k = (d - D(2025, 12, 1)).days
            anom[i] += -3.4 * math.sin(math.pi * (k + 1) / 10)
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
    """The network's 118 connections in service on 1 October 2025 with their installation regime (truth only),
    connection number, meter generation and meter history."""
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

    def cdate(y0, y1):
        while True:
            d = D(int(rng.integers(y0, y1 + 1)), int(rng.integers(1, 13)), int(rng.integers(1, 29)))
            if d <= D(2025, 5, 30):
                return d

    spec = [("HT", 19), ("REN", 31), ("LT", 56), ("UTIL", 12)]
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
                c["aansluitdatum"] = cdate(2009, 2024)
            elif reg == "LT":
                c["cat"] = "Woningen"
                c["bouwjaar"] = int(rng.integers(1986, 2008)) if rng.random() < 0.3 else int(rng.integers(2008, 2025))
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
                c["aansluitdatum"] = cdate(min(y0, 2025), min(2025, y0 + 2))
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
                c["aansluitdatum"] = cdate(min(y0, 2025), min(2025, y0 + 3))
            # cold-day drop of the installation (K) and the daily-noise scale
            if reg == "HT":
                c["d"] = float(np.clip(rng.normal(24.15, 0.82), 22.5, 25.9))
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
            c["lam"] = float(rng.uniform(0.18, 0.5))
            c["dhw"] = {"HT": 0.05, "REN": 0.045, "LT": 0.075, "UTIL": 0.02}[reg]
            c["tb"] = {"HT": 17.0, "REN": 16.0, "LT": 15.0, "UTIL": 16.5}[reg]
            out.append(c)
    order = rng.permutation(len(out))
    out = [out[i] for i in order]
    nums = rng.choice(np.arange(10100, 13999), size=len(out), replace=False)
    for i, c in enumerate(out):
        c["idx"] = i
        c["nr"] = "AW%05d" % int(nums[i])
        # meter history: generation A (connected before 2016) read in GJ by the drive-by system and exchanged for a
        # refurbished AMR meter at migration; generation B read in MWh and given an AMR module (same serial)
        c["gen"] = "A" if c["aansluitdatum"] < D(2016, 1, 1) else "B"
        c["serial_legacy"] = "%08d" % int(rng.integers(65100000, 65199999) if c["gen"] == "A" else
                                         rng.integers(71050000, 71059999))
        while True:
            md = D(2025, 6, 2) + TD(days=int(rng.integers(0, 100)))
            if md.weekday() < 5:
                break
        c["migration"] = md
        if c["gen"] == "A":
            c["serial_amr"] = "%08d" % int(rng.integers(78340000, 78349999))
            c["amr_begin_kwh"] = float(int(rng.integers(400000, 3200000)))
        else:
            c["serial_amr"] = c["serial_legacy"]
            c["amr_begin_kwh"] = None
        c["start_vol_m3"] = float(int(rng.integers(20000, 380000)))
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
    """Daily truth per connection for the 2025-26 meter year (UTC days): energy (kWh), volume (m3), mean supply and
    return temperatures at the meter."""
    ds = wx["days"]
    tg = wx["tg"] / 10.0
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
            rows.append([d, e, v, ts, tr])
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
    ("2146", "Gruttolaan", 2, 40, 40, 1969, "portiekflat", "F", 5),
    ("2147", "Kwartelstraat", 1, 31, 32, 1970, "portiekflat", "E", 5),
    ("2152", "Vinkenstraat", 2, 48, 48, 1968, "portiekflat", "E", 6),
]
PHASE_DATES = {1: D(2027, 5, 18), 2: D(2027, 7, 6), 3: D(2027, 9, 7), 4: D(2028, 5, 23), 5: D(2028, 7, 11),
               6: D(2028, 9, 5)}
REISSUE = {"2112": D(2026, 1, 20), "2146": D(2026, 2, 11)}          # gas EAN re-registered at a capacity change
GAS_EXCHANGE = {"2104": D(2026, 3, 17), "2124": D(2025, 11, 25), "2140": D(2026, 1, 13), "2152": D(2026, 2, 24)}   # meter exchanged, same EAN


def blocks(rng):
    out = []
    for code, st, a, b, dw, by, typ, lab, ph in BLOCKS:
        kwd = rng.uniform(5.4, 6.3) if typ == "galerijflat" else rng.uniform(5.7, 6.7)
        load = int(round(dw * kwd))
        prelim = int(round(load * rng.uniform(1.03, 1.10)))
        out.append({"code": code, "street": st, "from": a, "to": b, "dwellings": dw, "bouwjaar": by, "type": typ,
                    "label": lab, "phase": ph, "load": load, "prelim": prelim,
                    "gfa": int(round(dw * rng.uniform(62, 74))),
                    "date": PHASE_DATES[ph] + TD(days=int(rng.integers(0, 15))),
                    "gas_per_dw": float(rng.uniform(860, 1060))})
    return out


# ------------------------------------------------------------------------------------------------- exports (truth as the systems record it)
def amr_export(rng, wx, conns, amr):
    """Rows the AMR head-end exports: one per meter serial per UTC day, registers at the end of the UTC day.
    Communication gaps (rows absent, first day back without a daily consumption) and temperature-log faults fall on
    days above 0 C only; seven meters are exchanged in summer 2026 (two partial rows on the exchange day)."""
    tg = {d: t / 10.0 for d, t in zip(wx["days"], wx["tg"])}
    cold = {d for d in wx["days"] if tg[d] <= P.TG_WINDOW}
    near_cold = set()
    for d in cold:
        for k in (-1, 0, 1, 2):
            near_cold.add(d + TD(days=k))
    ex_ids = set(int(i) for i in rng.choice(len(conns), size=7, replace=False))
    rows = []
    for c in conns:
        tr = amr[c["idx"]]
        e0 = c["amr_begin_kwh"] if c["gen"] == "A" else None
        c["exchange26"] = None
        if c["idx"] in ex_ids:
            while True:
                xd = D(2026, 6, 8) + TD(days=int(rng.integers(0, 95)))
                if xd.weekday() < 5:
                    break
            c["exchange26"] = (xd, "%08d" % int(rng.integers(78510000, 78519999)), float(int(rng.integers(0, 14))),
                               float(rng.uniform(0.3, 0.55)))
        # gaps: 0 to 3 per meter, 2 to 6 days, never on or next to a day at or below 0 C
        gaps = set()
        firstback = set()
        ng = int(rng.choice([0, 0, 1, 1, 1, 2, 2, 3]))
        tries = 0
        while ng and tries < 200:
            tries += 1
            st = wx["days"][int(rng.integers(5, len(wx["days"]) - 10))]
            ln = int(rng.integers(2, 7))
            span = [st + TD(days=k) for k in range(ln + 1)]
            if any(x in near_cold for x in span) or any(x in gaps or x in firstback for x in span):
                continue
            if c["exchange26"] and any(abs((x - c["exchange26"][0]).days) < 3 for x in span):
                continue
            for x in span[:-1]:
                gaps.add(x)
            firstback.add(span[-1])
            ng -= 1
        tfault = set()
        if rng.random() < 0.25:
            st = wx["days"][int(rng.integers(5, len(wx["days"]) - 10))]
            for k in range(int(rng.integers(1, 4))):
                x = st + TD(days=k)
                if x not in near_cold and x not in gaps and x not in firstback:
                    tfault.add(x)
        c["gaps"] = sorted(gaps)
        c["firstback"] = sorted(firstback)
        c["tfault"] = sorted(tfault)
        reg_e = None
        reg_v = c["start_vol_m3"]
        serial = c["serial_amr"]
        c["amr_open_kwh"] = None
        for (d, e, v, ts, trt) in tr:
            if reg_e is None:
                reg_e = c["amr_open_true"]
                c["amr_open_kwh"] = reg_e
            if c["exchange26"] and d == c["exchange26"][0]:
                xd, nser, nbeg, f = c["exchange26"]
                old_e, old_v = reg_e + e * f, reg_v + v * f
                rows.append([serial, d, int(round(old_e)) - int(round(reg_e)), round(old_v, 2) - round(reg_v, 2),
                             round(ts, 1), round(trt, 1), int(round(old_e)), round(old_v, 2), "V"])
                c["exchange26_old_end"] = int(round(old_e))
                serial = nser
                reg_e, reg_v = nbeg, float(int(rng.integers(0, 3)))
                c["exchange26_new_begin"] = int(round(reg_e))
                new_e, new_v = reg_e + e * (1 - f), reg_v + v * (1 - f)
                rows.append([serial, d, int(round(new_e)) - int(round(reg_e)), round(round(new_v, 2) - round(reg_v, 2), 2),
                             round(ts, 1), round(trt, 1), int(round(new_e)), round(new_v, 2), "V"])
                reg_e, reg_v = new_e, new_v
                continue
            new_e, new_v = reg_e + e, reg_v + v
            if d in gaps:
                reg_e, reg_v = new_e, new_v
                continue
            de = int(round(new_e)) - int(round(reg_e))
            dv = round(round(new_v, 2) - round(reg_v, 2), 2)
            row = [serial, d, de, dv, round(ts, 1), round(trt, 1), int(round(new_e)), round(new_v, 2), "V"]
            if d in firstback:
                row[2], row[3] = None, None
                row[8] = "V"
            if d in tfault:
                row[4], row[5] = None, None
                row[8] = "G"
            rows.append(row)
            reg_e, reg_v = new_e, new_v
        c["amr_close_kwh"] = reg_e
    return rows


def weather_2425(rng):
    """Daily mean temperatures for the 2024-25 gas year (local days), a mild winter."""
    out = {}
    d = D(2024, 10, 1)
    a = 0.0
    while d <= D(2025, 9, 30):
        doy = d.timetuple().tm_yday
        a = 0.78 * a + rng.normal(0, 1.85)
        cool = -5.5 * math.sin(math.pi * ((d - D(2025, 9, 17)).days + 1) / 15) if D(2025, 9, 17) <= d <= D(2025, 9, 30) else 0.0
        out[d] = 11.0 - 7.2 * math.cos(2 * math.pi * (doy - 22) / 365.25) + a + cool
        d += TD(days=1)
    return out


def legacy_and_open(rng, conns, wx):
    """The 2024-25 gas year as the drive-by system read it (GJ for generation A, MWh for generation B), the summer
    2025 migration, and each meter's AMR opening register on 1 October 2025 00:00 UTC."""
    t24 = weather_2425(rng)
    reads = []
    route_day = {w: {} for w in WIJKEN_OLD + WIJKEN_NEW}
    for c in conns:
        k_gj = 3.6
        cons = {}
        for d, t in t24.items():
            phi = load_fraction(c, t)
            cons[d] = c["kw"] * c["u"] * phi * 24 * float(np.exp(rng.normal(0, 0.035)))
        start = max(D(2024, 10, 1), c["aansluitdatum"])
        yrs = max(0.0, (D(2024, 10, 1) - c["aansluitdatum"]).days / 365.25)
        annual = sum(cons.values())
        reg0 = float(int(rng.integers(0, 900))) if c["aansluitdatum"] >= D(2024, 10, 1) else \
            annual * yrs * float(rng.uniform(0.92, 1.05)) + float(int(rng.integers(0, 3000)))
        c["leg_reg_at_start"] = reg0
        unit = "GJ" if c["gen"] == "A" else "MWh"

        def fmt(kwh):
            return round(kwh / 277.7778, 3) if unit == "GJ" else round(kwh / 1000.0, 3)

        dl_ = sorted(cons)
        pref = {}
        acc = reg0
        for x in dl_:
            pref[x] = acc
            if x >= start:
                acc += cons[x]
        end_acc = acc

        def reg_at(day, frac):
            if day > dl_[-1]:
                return end_acc
            base_ = pref[day] if day >= start else reg0
            if day >= start and day in cons:
                base_ += frac * cons[day]
            return base_
        ser = c["serial_legacy"]
        if c["aansluitdatum"] < D(2024, 10, 1):
            reads.append([ser, D(2024, 10, 1), fmt(reg_at(D(2024, 10, 1), 0.42)), unit, "J"])
            c["leg_annual_kwh"] = reg_at(D(2024, 10, 1), 0.42)
        else:
            reads.append([ser, c["aansluitdatum"], fmt(reg0), unit, "A"])
            c["leg_annual_kwh"] = reg0
        m = D(2024, 11, 1)
        while m < c["migration"]:
            w = c["wijk"]
            if m not in route_day[w]:
                route_day[w][m] = int(rng.integers(1, 7))
            rd = D(m.year, m.month, route_day[w][m])
            if rd > c["aansluitdatum"] and rd < c["migration"] and rng.random() > 0.03:
                reads.append([ser, rd, fmt(reg_at(rd, 0.45)), unit, "M"])
            m = D(m.year + (m.month // 12), m.month % 12 + 1, 1)
        mig_frac = 0.40
        reg_mig = reg_at(c["migration"], mig_frac)
        if c["gen"] == "A":
            reads.append([ser, c["migration"], fmt(reg_mig), unit, "W"])
            c["leg_end_kwh"] = reg_mig
            # refurbished AMR meter from the migration time to 1 October 2025 00:00 UTC
            open_reg = c["amr_begin_kwh"] + (reg_at(D(2025, 9, 30), 1.0) - reg_mig) + (2 / 24) * cons[D(2025, 9, 30)]
        else:
            c["leg_end_kwh"] = None
            open_reg = reg_at(D(2025, 9, 30), 1.0) + (2 / 24) * cons[D(2025, 9, 30)]
        c["amr_open_true"] = open_reg
        c["gy2425_true"] = (reg_at(D(2025, 9, 30), 1.0) + (2 / 24) * cons[D(2025, 9, 30)]) - c["leg_annual_kwh"]
    reads.sort(key=lambda r: (r[1], r[0]))
    return reads


def gas_truth(rng, blks, wx):
    """Monthly telemetry reads of the blocks' boiler-room gas meters (06:00 local on the first of the month), the
    grid operator's meter master data, and the true gas-year consumption per block."""
    tg = {d: t / 10.0 for d, t in zip(wx["days"], wx["tg"])}
    reads, master = [], []
    for b in blks:
        w = {d: max(0.0, 18.0 - t) + 0.45 for d, t in tg.items()}
        tot_w = sum(w.values())
        annual = b["dwellings"] * b["gas_per_dw"]
        daily = {d: annual * w[d] / tot_w * float(np.exp(rng.normal(0, 0.05))) for d in w}
        b["gas_true"] = sum(daily.values())
        ean = "8716%014d" % int(rng.integers(10**12, 10**13 - 1))
        b["ean"] = ean
        g = "G65" if b["dwellings"] >= 80 else ("G40" if b["dwellings"] >= 48 else "G25")
        ser = "%s%07d" % (rng.choice(["E", "F", "K"]), int(rng.integers(1000000, 9999999)))
        reg = float(int(rng.integers(150000, 2400000)))
        months = [D(2025, 10, 1)] + [D(2025 + (10 + k) // 12, (10 + k) % 12 + 1, 1) for k in range(12)]
        events = []
        if b["code"] in REISSUE:
            events.append(("reissue", REISSUE[b["code"]]))
        if b["code"] in GAS_EXCHANGE:
            events.append(("exchange", GAS_EXCHANGE[b["code"]]))
        cur = {"ean": ean, "ser": ser, "g": g, "reg": reg, "from": D(2014, 4, 2) + TD(days=int(rng.integers(0, 2500)))}
        if b["code"] in REISSUE:
            old_ean = "8716%014d" % int(rng.integers(10**12, 10**13 - 1))
            cur["ean"] = old_ean
            cur["g"] = "G40" if g == "G65" else "G25"
        segs = []
        d = D(2025, 10, 1)
        for i, m in enumerate(months):
            pass
        # walk the days, cutting segments at events (an event takes effect at 10:00 local on its date)
        day_list = sorted(daily)
        ev = dict((e[1], e[0]) for e in events)
        seg = dict(cur)
        seg["start_reg"] = seg["reg"]
        seg["start"] = D(2025, 10, 1)
        seg_reads = []
        reg_now = seg["reg"]
        for m in months:
            pass
        mi = 0
        x = D(2025, 10, 1)
        while x <= D(2026, 10, 1):
            if x in [mm for mm in months]:
                seg_reads.append((seg["ean"], seg["ser"], dt.datetime(x.year, x.month, x.day, 6, 0), round(reg_now), "T"))
            if x in ev:
                kind = ev[x]
                part = 0.42 * daily.get(x, 0.0)
                end_reg = reg_now + part
                if kind == "reissue":
                    seg_reads.append((seg["ean"], seg["ser"], dt.datetime(x.year, x.month, x.day, 10, 0), round(end_reg), "E"))
                    master.append({"ean": seg["ean"], "ser": seg["ser"], "g": seg["g"], "block": b, "in": seg["from"],
                                   "out": x, "reason": "capaciteitswijziging", "end": round(end_reg), "begin": None})
                    new = {"ean": ean, "ser": "%s%07d" % (rng.choice(["E", "F", "K"]), int(rng.integers(1000000, 9999999))),
                           "g": g, "from": x}
                    nb = float(int(rng.integers(0, 9)))
                    seg_reads.append((new["ean"], new["ser"], dt.datetime(x.year, x.month, x.day, 10, 0), round(nb), "B"))
                    seg = new
                    reg_now = nb + (daily.get(x, 0.0) - part)
                    seg["begin"] = nb
                else:
                    master.append({"ean": seg["ean"], "ser": seg["ser"], "g": seg["g"], "block": b, "in": seg["from"],
                                   "out": x, "reason": "meterwissel", "end": round(end_reg), "begin": None})
                    new = {"ean": seg["ean"], "ser": "%s%07d" % (rng.choice(["E", "F", "K"]), int(rng.integers(1000000, 9999999))),
                           "g": seg["g"], "from": x}
                    nb = float(int(rng.integers(0, 9)))
                    seg = new
                    seg["begin"] = nb
                    reg_now = nb + (daily.get(x, 0.0) - part)
                x += TD(days=1)
                continue
            reg_now += daily.get(x, 0.0)
            x += TD(days=1)
        master.append({"ean": seg["ean"], "ser": seg["ser"], "g": seg["g"], "block": b, "in": seg["from"], "out": None,
                       "reason": "", "end": None, "begin": seg.get("begin")})
        b["gas_reads"] = seg_reads
        b["ean_current"] = seg["ean"]
        reads += seg_reads
    reads.sort(key=lambda r: (r[2], r[0]))
    return reads, master


# ------------------------------------------------------------------------------------------------- station
def committed_flow(conns, rows, wx):
    """The hydraulic study's committed design-day flow: each connection's contracted capacity over CP times the mean
    of its metered daily drops on days at or below 0 C (procedure 3.2 for connections in service)."""
    tg = {d: t / 10.0 for d, t in zip(wx["days"], wx["tg"])}
    by_ser = {}
    for r in rows:
        if r[4] is not None and tg[r[1]] <= P.TG_WINDOW:
            by_ser.setdefault(r[0], []).append(r[4] - r[5])
    tot = 0.0
    for c in conns:
        dd = float(np.mean(by_ser[c["serial_amr"]]))
        tot += c["kw"] / (P.CP * dd)
    return tot


def scada(rng, wx, conns, amr):
    """Hourly station record in UTC: flow, supply and return, heat, pump power."""
    ds = wx["days"]
    out = []
    hours_utc = []
    for d in ds:
        for h in range(24):
            hours_utc.append(dt.datetime(d.year, d.month, d.day, h))
    # local hourly temperature by UTC hour
    loc_temp = {}
    for d in ds:
        for h in range(24):
            loc_temp[dt.datetime(d.year, d.month, d.day, h)] = wx["hourly_local"][d][h]
    E = {d: 0.0 for d in ds}
    V = {d: 0.0 for d in ds}
    for c in conns:
        for (d, e, v, ts, tr) in amr[c["idx"]]:
            E[d] += e
            V[d] += v
    ts_station = dict(zip(ds, wx["ts_station"]))
    loss = {}
    for d in ds:
        tr_mix = ts_station[d] - E[d] / (P.CP * V[d])
        loss[d] = 24 * 23.5 * ((ts_station[d] + tr_mix) / 2 - 10.0)
    prof = []
    for h in range(24):
        prof.append(1 + 0.22 * math.cos(2 * math.pi * (h - 6) / 24) + 0.08 * math.cos(4 * math.pi * (h - 18) / 24))
    for t in hours_utc:
        off = nl_offset_hours(t)
        lt = t + TD(hours=off)
        d = t.date()
        hl = lt.hour
        p = prof[hl] / sum(prof)
        flow = V[d] * p * float(np.exp(rng.normal(0, 0.02)))
        heat = (E[d] + loss[d]) * p * float(np.exp(rng.normal(0, 0.02)))
        tout = loc_temp.get(dt.datetime(lt.year, lt.month, lt.day, hl), None)
        if tout is None:
            tout = wx["hourly_local"][d][hl]
        ts = supply_curve(tout) + float(rng.normal(0, 0.25))
        tr = ts - heat / (P.CP * flow)
        pump = 21.0 + 9.2e-8 * flow ** 3 + float(rng.normal(0, 0.6))
        if flow > 470:
            p1, p2 = pump / 2 + float(rng.normal(0, 0.3)), pump / 2 + float(rng.normal(0, 0.3))
        else:
            p1, p2 = pump, 0.0
        out.append([t, round(flow, 1), round(ts, 1), round(tr, 1), round(heat / 1000.0, 3), round(p1, 1), round(p2, 1)])
    return out, E, V, loss


# ------------------------------------------------------------------------------------------------- families and tuning
def family(rows, conns, wx, sel, how, win=0.0, route="T", supply="own"):
    tg = {d: t / 10.0 for d, t in zip(wx["days"], wx["tg"])}
    ser2c = {}
    for c in conns:
        ser2c[c["serial_amr"]] = c
        if c.get("exchange26"):
            ser2c[c["exchange26"][1]] = c
    tsst = dict(zip(wx["days"], wx["ts_station"]))
    per = {}
    for r in rows:
        c = ser2c[r[0]]
        if not sel(c) or tg[r[1]] > win:
            continue
        p = per.setdefault(c["idx"], {"dt": [], "E": 0.0, "V": 0.0, "kw": c["kw"]})
        if r[4] is not None:
            p["dt"].append((r[4] if supply == "own" else tsst[r[1]]) - r[5])
        if r[2] is not None:
            p["E"] += r[2]
            p["V"] += r[3]
    if route == "T":
        ds = np.array([np.mean(p["dt"]) for p in per.values()])
    else:
        ds = np.array([p["E"] / (P.CP * p["V"]) for p in per.values()])
    q = np.array([p["kw"] for p in per.values()])
    if how == "mean":
        return float(ds.mean())
    if how == "median":
        return float(np.median(ds))
    if how == "harm":
        return float(q.sum() / (q / ds).sum())
    if how == "flow":
        return float(sum(p["E"] for p in per.values()) / (P.CP * sum(p["V"] for p in per.values())))
    raise ValueError(how)


SEL = {
    "HT": lambda c: c["regime"] == "HT",
    "PRE": lambda c: c["bouwjaar"] < 1985,
    "PRE_RES": lambda c: c["bouwjaar"] < 1985 and c["cat"] == "Woningen",
    "ERA": lambda c: 1955 <= c["bouwjaar"] <= 1975,
    "BLOCKYEARS": lambda c: 1962 <= c["bouwjaar"] <= 1971,
    "ALL": lambda c: True,
    "RES": lambda c: c["cat"] == "Woningen",
}


def families(rows, conns, wx):
    f = {"golden": {}, "golden_wide": {}, "pre": {}, "net": {}}
    for how in ("mean", "median", "harm", "flow"):
        for win in (0.0, -1.0, 1.0, -2.0, 2.0):
            f["golden"][("T", how, win)] = family(rows, conns, wx, SEL["HT"], how, win)
        if how != "flow":
            f["golden"][("E", how, 0.0)] = family(rows, conns, wx, SEL["HT"], how, 0.0, route="E")
            f["golden_wide"][("stn", how, 0.0)] = family(rows, conns, wx, SEL["HT"], how, 0.0, supply="station")
        f["golden_wide"][("season", how)] = family(rows, conns, wx, SEL["HT"], how, 99.0)
        for k in ("PRE", "PRE_RES", "ERA", "BLOCKYEARS"):
            f["pre"][(k, how)] = family(rows, conns, wx, SEL[k], how)
        for k in ("ALL", "RES"):
            f["net"][(k, how)] = family(rows, conns, wx, SEL[k], how)
    return f


def dist_to_edge(x, unit):
    r = x / unit
    return unit * (0.5 - abs(r - round(r)))


def same_bin(vals, unit, margin):
    rs = {round(v / unit) for v in vals}
    return len(rs) == 1 and min(dist_to_edge(v, unit) for v in vals) >= margin


def tune(blks, fam):
    """Set the station's available design-day flow H (a multiple of 10 m3/h, the pump and exchanger limit less the
    committed flow) and one block load per phase (the largest block's design load within 8 per cent) so that every
    licensed estimate of the like installations' drop gives the same call and every graded figure clears its bin
    edge. The search is deterministic and moves no figure by hand."""
    g = list(fam["golden"].values())
    gw = g + [v for v in fam["golden_wide"].values()]
    g_lo, g_hi = min(g), max(g)
    gw_lo, gw_hi = min(gw), max(gw)
    p_lo = min(fam["pre"].values())
    base = {ph: [b for b in blks if b["phase"] == ph] for ph in range(1, 7)}
    big = {ph: max(base[ph], key=lambda b: b["load"]) for ph in base}
    best = None
    for H in range(140, 200, 10):
        opts = {}
        for ph in range(1, 7):
            o = []
            b0 = big[ph]["load"]
            for dlt in range(-int(0.08 * b0), int(0.08 * b0) + 1):
                K = sum(b["load"] for b in base[ph]) + dlt
                fl = [K / (P.CP * x) for x in g]
                if same_bin(fl, 5, 0.35):
                    o.append((abs(dlt), dlt, K))
            opts[ph] = sorted(o)[:30]
        if any(not opts[ph] for ph in opts):
            continue
        first = {}
        for a in opts[1]:
            for b in opts[2]:
                for c3 in opts[3]:
                    KA = a[2] + b[2] + c3[2]
                    cost = a[0] + b[0] + c3[0]
                    if KA in first and first[KA][0] <= cost:
                        continue
                    if not (KA / (P.CP * g_lo) <= H / 1.08 and KA / (P.CP * gw_lo) <= H / 1.04
                            and KA / (P.CP * 20.0) >= 1.06 * H):
                        continue
                    f3 = [KA / (P.CP * x) for x in g]
                    if not same_bin(f3, 10, 1.0) or max(f3) >= H:
                        continue
                    first[KA] = (cost, (a[1], b[1], c3[1]))
        second = {}
        for d4 in opts[4]:
            for e5 in opts[5]:
                for f6_ in opts[6]:
                    K2 = d4[2] + e5[2] + f6_[2]
                    cost = d4[0] + e5[0] + f6_[0]
                    if K2 not in second or second[K2][0] > cost:
                        second[K2] = (cost, (d4[1], e5[1], f6_[1]))
        for KA, (ca, da) in first.items():
            for K2, (cb, db) in second.items():
                cost = ca + cb
                if best is not None and cost >= best[0]:
                    continue
                KAB = KA + K2
                if not (KAB / (P.CP * g_hi) >= 1.08 * H and KAB / (P.CP * gw_hi) >= 1.04 * H
                        and KAB / (P.CP * p_lo) <= H / 1.06):
                    continue
                f6 = [KAB / (P.CP * x) for x in g]
                if not same_bin(f6, 10, 1.0):
                    continue
                if not same_bin([v - H for v in f6], 10, 1.0):
                    continue
                best = (cost, H, {1: da[0], 2: da[1], 3: da[2], 4: db[0], 5: db[1], 6: db[2]})
    if best is None:
        raise SystemExit("tune: no feasible setting")
    cost, H, dl = best
    for ph, dlt in dl.items():
        big[ph]["load"] += dlt
        big[ph]["prelim"] = int(round(big[ph]["prelim"] + dlt * 1.05))
    return H, dl


def build(seed=P.SEED):
    rng = np.random.default_rng(seed)
    wx = weather(rng)
    conns = connections(rng)
    amr, ts_station = amr_truth(rng, wx, conns)
    wx["ts_station"] = ts_station
    blks = blocks(rng)
    rng2 = np.random.default_rng(seed + 1000)
    legacy = legacy_and_open(rng2, conns, wx)
    rows = amr_export(rng2, wx, conns, amr)
    fam = families(rows, conns, wx)
    H, dl = tune(blks, fam)
    committed = committed_flow(conns, rows, wx)
    rng3 = np.random.default_rng(seed + 2000)
    gas_reads, gas_master = gas_truth(rng3, blks, wx)
    sc, E, V, loss = scada(rng3, wx, conns, amr)
    w = {"wx": wx, "conns": conns, "amr": amr, "blocks": blks, "legacy": legacy, "amr_rows": rows, "fam": fam,
         "H": H, "tune": dl, "committed": committed, "capacity": int(round(committed)) + H,
         "gas_reads": gas_reads, "gas_master": gas_master, "scada": sc}
    return w


if __name__ == "__main__":
    import time
    t0 = time.time()
    w = build()
    tg = w["wx"]["tg"] / 10
    print("cold days", int((tg <= 0).sum()), "min TG", tg.min())
    f = w["fam"]
    for k in ("golden", "golden_wide", "pre", "net"):
        v = list(f[k].values())
        print(k, round(min(v), 2), round(max(v), 2))
    print("H", w["H"], "tune", w["tune"], "committed", round(w["committed"], 1), "capacity", w["capacity"])
    print("rows", len(w["amr_rows"]), "legacy", len(w["legacy"]), "gas", len(w["gas_reads"]), "scada", len(w["scada"]))
    print("blocks", [(b["code"], b["phase"], b["load"]) for b in w["blocks"]])
    print(round(time.time() - t0, 1), "s")
