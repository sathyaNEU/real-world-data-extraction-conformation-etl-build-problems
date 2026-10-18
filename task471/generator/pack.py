"""The pack's tables: the survey's keyed cards, the revenue control system's quarterly extracts, the service area's ZIP
list, the bureau's city-market table, Kessick Valley's 10% ticket sample and its T-100 segments."""
import csv
import datetime as dt
import io
import math

import numpy as np

import sim
import world as W


def everything():
    import calibrate
    x = sim.build()
    x["dup_batch"] = calibrate.dup_batch(x, keyed_cards(x))
    return x


def write_csv(path, cols, rows, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(cols)
    for r in rows:
        w.writerow(r)
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())
    return len(rows)


def card_no(wave, n):
    return "%d%06d" % (wave, n)


def wave_index(name):
    return int(name[1])


# ---------------------------------------------------------------------------------------------- the cards
CARD_COLS = ["card_no", "wave", "keying_batch", "box_collected", "home_zip", "destination_code", "nights", "party",
             "purpose"]
VERBATIM_COLS = ["card_no", "question", "as_written"]


def keyed_cards(x):
    """The cards in the order the contractor keyed them: each wave's nights of box collection in turn, each night's
    cards in batches of up to 450 in the order they came out of the box."""
    out = []
    for name, q, start in W.WAVES:
        wc = sorted((c for c in x["cards"] if c["wave"] == name), key=lambda c: (c["collected"], c["serial"]))
        batch, count, last = 0, 0, None
        for c in wc:
            if c["collected"] != last or count >= 450:
                batch += 1
                count = 0
                last = c["collected"]
            count += 1
            out.append((c, "%d-%02d" % (wave_index(name), batch), c["zip_keyed"]))
    return out


def card_rows(x):
    """One row per card in keying order; the export carried one keying batch twice, its second copy straight after
    the first."""
    rows = []
    for name, q, start in W.WAVES:
        wave_rows = [[card_no(wave_index(name), c["serial"]), wave_index(name), b, c["collected"].isoformat(), z,
                      c["dest_code"], c["nights"], c["party_keyed"], c["purpose"]]
                     for c, b, z in keyed_cards(x) if c["wave"] == name]
        for i, r in enumerate(wave_rows):
            rows.append(r)
            if r[2] == x["dup_batch"] and (i + 1 == len(wave_rows) or wave_rows[i + 1][2] != r[2]):
                rows += [list(q_) for q_ in wave_rows if q_[2] == x["dup_batch"]]
    return rows


STATE = {"TPA": "FL", "PIE": "FL", "RSW": "FL", "MCO": "FL", "SFB": "FL", "FLL": "FL", "MIA": "FL", "SRQ": "FL",
         "PBI": "FL", "JAX": "FL", "PHX": "AZ", "AZA": "AZ", "LAS": "NV", "RNO": "NV", "MYR": "SC", "SAV": "GA",
         "SAN": "CA", "LAX": "CA", "SFO": "CA", "SNA": "CA", "DEN": "CO", "BNA": "TN", "BOS": "MA", "DFW": "TX",
         "DAL": "TX", "IAH": "TX", "HOU": "TX", "AUS": "TX", "SAT": "TX", "ATL": "GA", "MSP": "MN", "SEA": "WA",
         "PDX": "OR", "SLC": "UT", "MSY": "LA", "RDU": "NC", "PHL": "PA"}


def as_written(card, s):
    """How a destination reads once keyed from a hand-written card: mostly as the traveller wrote it, sometimes in
    capitals or lower case, with the state added, a full stop, or a letter dropped or doubled."""
    rng = np.random.default_rng([W.SEED, 13, wave_index(card["wave"]), card["serial"]])
    u = rng.random(4)
    out = s
    if u[0] < 0.07:
        out = out.upper()
    elif u[0] < 0.15:
        out = out.lower()
    if u[1] < 0.06 and card["airport"] in STATE and len(out) > 3 and "," not in out:
        out = out + (", " if u[2] < 0.5 else " ") + STATE[card["airport"]]
    elif u[1] < 0.08:
        out = out + "."
    if u[3] < 0.025 and len(out) > 5 and out.isalpha():
        i = 1 + int(u[2] * (len(out) - 2))
        out = out[:i] + out[i + 1:] if u[3] < 0.0125 else out[:i] + out[i] + out[i:]
    return out


def verbatim_rows(x):
    rows = []
    for c, b, z in keyed_cards(x):
        no = card_no(wave_index(c["wave"]), c["serial"])
        rows.append([no, "Q2", as_written(c, c["dest_written"])])
        rows.append([no, "Q4", c["party_written"]])
    return rows


# ---------------------------------------------------------------------------------------------- the register
def garage_counts():
    rng = np.random.default_rng(W.SEED + 4000)
    out = {}
    for i in range(365):
        d = dt.date(W.YEAR, 1, 1) + dt.timedelta(days=i)
        out[d] = int(rng.poisson(W.GARAGE_PER_DAY * W.GARAGE_SEASON[(d.month - 1) // 3 + 1] * sim.dow_factor(d)))
    return out


def permit_counts():
    rng = np.random.default_rng(W.SEED + 5000)
    out = {}
    for i in range(365):
        d = dt.date(W.YEAR, 1, 1) + dt.timedelta(days=i)
        wk = d.weekday() < 5
        out[d] = {"Economy C": int(rng.poisson(74 if wk else 31)), "Economy D": int(rng.poisson(58 if wk else 24)),
                  "Long-Term": int(rng.poisson(9)), "Garage": int(rng.poisson(118 if wk else 52))}
    return out


def register_rows(x, q):
    ent = {(d, l): n for d, l, n in x["entries"]}
    gar = garage_counts()
    per = permit_counts()
    days = sorted({d for d, l, n in x["entries"] if (d.month - 1) // 3 + 1 == q})
    rows = []
    for d in days:
        for lot in ["Economy C", "Economy D", "Long-Term", "Garage"]:
            n = gar[d] if lot == "Garage" else ent[(d, lot)]
            if d < W.UPGRADE:
                rows.append([d.strftime("%m/%d/%Y"), W.LOT_OLD[lot], n])
            else:
                rows.append([d.isoformat(), W.LOT_NEW[lot], n, per[d][lot]])
    cols = ["Date", "Lot", "Transient Entries"] if days[0] < W.UPGRADE else ["business_date", "facility", "transient_entries",
                                                                    "permit_entries"]
    return cols, rows


# ---------------------------------------------------------------------------------------------- reference tables
ZIP_COLS = ["county", "zip_code", "post_office"]


def zip_rows():
    rows = []
    for county, (zips, _) in W.COUNTIES.items():
        for z in zips:
            rows.append([county, z, W.PLACES[z]])
    return rows


MARKET_COLS = ["code", "code_type", "name", "city_market", "market_code"]


def market_rows():
    rows = []
    for mcode, (mname, airports) in W.CITY_MARKETS.items():
        for ap, _ in airports:
            rows.append([ap, "airport", W.AIRPORT_NAMES[ap], mname, mcode])
        if mcode in W.METRO:
            rows.append([W.METRO[mcode], "metro", "%s, all airports" % mname, mname, mcode])
    for code, city, name, _ in W.OTHER_AIRPORTS:
        rows.append([code, "airport", name, city, code])
    rows.sort(key=lambda r: (r[3], r[1] != "metro", r[0]))
    return rows


# ---------------------------------------------------------------------------------------------- Kessick Valley's ticket sample
COORD = {"KVR": (41.21, -85.62), "ORD": (41.98, -87.90), "CLT": (35.21, -80.94), "DTW": (42.21, -83.35),
         "TPA": (27.98, -82.53), "PIE": (27.91, -82.69), "PHX": (33.43, -112.01), "AZA": (33.31, -111.66),
         "RSW": (26.54, -81.76), "MCO": (28.43, -81.31), "SFB": (28.78, -81.24), "FLL": (26.07, -80.15),
         "LAS": (36.08, -115.15), "MYR": (33.68, -78.93), "SAN": (32.73, -117.19), "DEN": (39.86, -104.67),
         "BNA": (36.12, -86.68), "DCA": (38.85, -77.04), "IAD": (38.95, -77.46), "BWI": (39.18, -76.67),
         "LGA": (40.78, -73.87), "EWR": (40.69, -74.17), "JFK": (40.64, -73.78), "BOS": (42.36, -71.01),
         "DFW": (32.90, -97.04), "DAL": (32.85, -96.85), "IAH": (29.98, -95.34), "HOU": (29.65, -95.28),
         "ATL": (33.64, -84.43), "MSP": (44.88, -93.22), "LAX": (33.94, -118.41), "SEA": (47.45, -122.31),
         "MIA": (25.79, -80.29), "MSY": (29.99, -90.26)}
MARKET_ID = {"KVR": 34921, "CHI": 30977, "CLT": 31057, "DTT": 31295, "TPA": 33195, "PHX": 30466, "RSW": 31714,
             "ORL": 31454, "FLL": 32467, "LAS": 32211, "MYR": 33284, "SAN": 33570, "DEN": 30325, "BNA": 30693,
             "WAS": 30852, "NYC": 31703, "BOS": 30721, "DFW": 30194, "HOU": 31453, "ATL": 30397, "MSP": 31650,
             "LAX": 32575, "SEA": 30559, "MIA": 32467, "MSY": 33495}
TICKET_COLS = ["ItinID", "MktID", "MktCoupons", "Year", "Quarter", "Origin", "OriginCityMarketID", "Dest",
               "DestCityMarketID", "AirportGroup", "TkCarrier", "OpCarrierGroup", "BulkFare", "Passengers", "MktFare",
               "MktDistance", "NonStopMiles"]
HUB_CARRIER = {"ORD": "7L", "CLT": "4B", "DTW": "9R"}


def miles(a, b):
    (la1, lo1), (la2, lo2) = COORD[a], COORD[b]
    p1, p2 = math.radians(la1), math.radians(la2)
    dl = math.radians(lo2 - lo1)
    c = math.sin(p1) * math.sin(p2) + math.cos(p1) * math.cos(p2) * math.cos(dl)
    return int(round(3958.8 * math.acos(max(-1.0, min(1.0, c)))))


def market_of(ap):
    for m, (n, aps) in W.CITY_MARKETS.items():
        if any(a == ap for a, _ in aps):
            return m
    return ap


def ticket_rows():
    rng = np.random.default_rng(W.SEED + 6000)
    dests = {"TPA": 150, "PHX": 120, "RSW": 70, "MCO": 260, "FLL": 90, "LAS": 230, "MYR": 60, "SAN": 110, "DEN": 300,
             "BNA": 120, "DCA": 140, "IAD": 60, "BWI": 40, "LGA": 210, "EWR": 160, "JFK": 90, "BOS": 270, "DFW": 200,
             "DAL": 30, "IAH": 120, "HOU": 50, "ATL": 330, "MSP": 160, "LAX": 210, "SEA": 150, "MIA": 120,
             "MSY": 90, "ORD": 610, "CLT": 380, "DTW": 400}
    season = {"TPA": (1.8, 1.0, 0.6), "PHX": (1.7, 1.0, 0.5), "RSW": (2.0, 0.9, 0.4), "MCO": (1.4, 1.1, 1.0),
              "FLL": (1.6, 0.9, 0.6), "MYR": (0.4, 1.1, 1.9)}
    rows, itin = [], 2026100000
    for q in (1, 2, 3):
        for ap, n in dests.items():
            k = int(rng.poisson(n * season.get(ap, (1.0, 1.0, 1.0))[q - 1]))
            for _ in range(k):
                itin += int(rng.integers(3, 40))
                hub = ap if ap in HUB_CARRIER else ["ORD", "CLT", "DTW"][rng.choice(3, p=(0.42, 0.31, 0.27))]
                car = HUB_CARRIER[hub]
                rt = rng.random() < 0.72
                pax = 1 + int(rng.poisson(0.35))
                d = miles("KVR", ap)
                flown = d if hub == ap else miles("KVR", hub) + miles(hub, ap)
                fare1 = round(float(95 + 0.135 * d * rng.lognormal(0.0, 0.35)), 2)
                bulk = 1 if rng.random() < 0.01 else 0
                group = "KVR:%s" % ap if hub == ap else "KVR:%s:%s" % (hub, ap)
                mk = market_of(ap)
                out = [itin, itin * 10 + 1, 1 if hub == ap else 2, 2026, q, "KVR", MARKET_ID["KVR"], ap,
                       MARKET_ID.get(mk, 30000 + sum(map(ord, ap))), group, car, car, bulk, pax,
                       "%.2f" % fare1, flown, d]
                rows.append(out)
                if rt:
                    fare2 = round(fare1 * float(rng.uniform(0.85, 1.2)), 2)
                    back = ":".join(reversed(group.split(":")))
                    rows.append([itin, itin * 10 + 2, out[2], 2026, q, ap, out[8], "KVR", MARKET_ID["KVR"], back, car,
                                 car, bulk, pax, "%.2f" % fare2, flown, d])
    return rows


T100_COLS = ["YEAR", "MONTH", "UNIQUE_CARRIER", "ORIGIN", "DEST", "AIRCRAFT_TYPE", "DEPARTURES_SCHEDULED",
             "DEPARTURES_PERFORMED", "SEATS", "PASSENGERS", "DISTANCE"]


def t100_rows():
    rng = np.random.default_rng(W.SEED + 7000)
    spec = [("7L", "ORD", "E175", 76, 3, 1), ("4B", "CLT", "CRJ-900", 76, 2, 0), ("9R", "DTW", "CRJ-700", 65, 2, 1)]
    rows = []
    for m in range(1, 13):
        first = dt.date(2026, m, 1)
        ndays = (dt.date(2026 + (m == 12), m % 12 + 1, 1) - first).days
        sats = sum(1 for i in range(ndays) if (first + dt.timedelta(days=i)).weekday() == 5)
        for car, hub, ac, seats, freq, ex_sat in spec:
            for o, d in (("KVR", hub), (hub, "KVR")):
                sched = freq * ndays - ex_sat * sats
                perf = sched - int(rng.poisson(sched * 0.012))
                lf = float(rng.uniform(0.71, 0.86))
                rows.append([2026, m, car, o, d, ac, sched, perf, perf * seats, int(perf * seats * lf), miles("KVR", hub)])
    return rows
