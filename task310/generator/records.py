"""The panel's records as the systems that hold them would export them: the recruitment register, the system
survey, the two inverter portals' 2025 exports, the network's revenue-meter half hours and its connection register.
All written from world.py; every Layer 1 trait is produced the way the producing system produces it."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P
import world as W

REC_SEED = [P.SEED, 11]
M0 = dt.datetime(2025, 1, 1, 0, 0)                     # market time, UTC+10, start of 2025
DST_END = dt.datetime(2025, 4, 6, 2, 0)                # market time at which the local clock falls back
DST_START = dt.datetime(2025, 10, 5, 2, 0)             # market time at which the local clock springs forward


def local_of_market(m):
    """Local clock time for a market-time instant: an hour ahead in daylight saving."""
    return m + dt.timedelta(hours=1) if (m < DST_END or m >= DST_START) else m


def _ids(rng):
    nums = rng.choice(np.arange(1000, 9999), 160, replace=False)
    nmis = rng.choice(np.arange(300000, 999999), 160, replace=False)
    return ["HEM-%04d" % n for n in nums], ["4402%06d" % n for n in nmis]


def attach(w):
    """Identifiers, inverter brands, meter serials and the year's events, drawn on their own stream."""
    rng = np.random.default_rng(REC_SEED)
    homes = w["homes"]
    pids, nmis = _ids(rng)
    order = rng.permutation(len(homes))
    for k, i in enumerate(order):
        homes[i]["pid"], homes[i]["nmi"] = pids[k], nmis[k]
    for h in homes:
        h["brand"] = "Velkora" if rng.random() < 0.6 else "Ondrava"
        h["ref"] = ("VKR-%06d" % rng.integers(100000, 999999)) if h["brand"] == "Velkora" else \
            ("OD%dK%08d" % (int(h["ac"]), rng.integers(10 ** 7, 10 ** 8)))
        h["model"] = ("Velkora VK%d-H" % int(round(h["ac"] * 10))) if h["brand"] == "Velkora" else \
            ("Ondrava OD-%d.%dK" % (int(h["ac"]), int(round(h["ac"] * 10)) % 10))
        h["meter"] = "SMN%07d" % rng.integers(10 ** 6, 10 ** 7)
        h["meter_change"] = None
        h["inv_change"] = None
        h["installed"] = _date_from_year(h["conn"], rng)
        h["recruited"] = (dt.date(2024, 3, 4) + dt.timedelta(days=int(rng.integers(0, 200)))).isoformat()
        h["dwelling"] = rng.choice(["detached", "detached", "detached", "semi-detached", "townhouse"])
        h["occupants"] = int(rng.choice([1, 2, 2, 3, 4, 4, 5]) if h["typ"] != "retired" else rng.choice([1, 2, 2]))
    # meter exchanges part-way through the year
    for i in rng.choice(len(homes), 9, replace=False):
        day = int(rng.integers(40, 330))
        hh = int(rng.integers(18, 30))
        homes[i]["meter_change"] = (day * 48 + hh, "LG%08d" % rng.integers(10 ** 7, 10 ** 8))
    # inverter replacements on unlimited Ondrava homes: the old inverter's counter stops, the new one starts at zero
    cand = [i for i, h in enumerate(homes) if h["brand"] == "Ondrava" and h["limit"] >= h["ac"]]
    for i in rng.choice(cand, 3, replace=False):
        day = int(rng.integers(60, 300))
        homes[i]["inv_change"] = (day, "OD%dK%08d" % (int(homes[i]["ac"]), rng.integers(10 ** 7, 10 ** 8)))
    return w


def _date_from_year(y, rng):
    yr = int(y)
    frac = y - yr
    d = dt.date(yr, 1, 1) + dt.timedelta(days=int(frac * 365))
    return d.isoformat()


def apply_events(w):
    """Inverter outages on replacement days: the home's solar is off from 07:00 to 15:00 market time that day."""
    for h in w["homes"]:
        if h["inv_change"]:
            day, _ = h["inv_change"]
            a, b = day * 48 + 14, day * 48 + 30
            for key in ("rec", "pot"):
                h[key] = h[key].copy()
                h[key][a:b] = 0.0
            h["exp"] = np.maximum(h["rec"] - h["load"], 0.0)
            h["imp"] = np.maximum(h["load"] - h["rec"], 0.0)
    return w


def controlled_load(h, rng):
    """Off-peak hot water on its own circuit: the network switches it on between 22:00 and 23:30 market time and it
    runs until the tank is hot."""
    cl = np.zeros(W.HH)
    if h["cl_kwh"] <= 0:
        return cl
    for d in range(365):
        e = h["cl_kwh"] * float(np.clip(rng.normal(1.0, 0.18), 0.5, 1.6)) * (1.25 if d < 60 or d > 330 else 1.0) ** -1
        start = d * 48 + 44 + int(rng.integers(0, 4))
        k = 0
        while e > 1e-9 and start + k < W.HH:
            take = min(e, 1.8)                    # a 3.6 kW element for half an hour
            cl[start + k] += take
            e -= take
            k += 1
    return cl


def panel_register(w):
    rows = []
    for h in w["homes"]:
        rows.append({"panel_id": h["pid"], "region": P.REGIONS[h["region"]], "suburb": h["suburb"],
                     "postcode": h["postcode"], "nmi": h["nmi"], "inverter_brand": h["brand"],
                     "inverter_ref": h["ref"] if not h["inv_change"] else h["inv_change"][1],
                     "recruited": h["recruited"], "dwelling": h["dwelling"], "occupants": h["occupants"]})
    return pd.DataFrame(rows).sort_values("panel_id").reset_index(drop=True)


def system_register(w):
    rows = []
    for h in w["homes"]:
        orient = {"N": "N", "NE": "NE", "NW": "NW", "EW": "E-W"}[h["az"]]
        base = {"panel_id": h["pid"], "array_kwp": h["kwp"], "inverter_brand": h["brand"], "inverter_model": h["model"],
                "inverter_ac_kw": h["ac"], "array_orientation": orient, "tilt_deg": h["tilt"], "installed": h["installed"]}
        if h["inv_change"]:
            day, new = h["inv_change"]
            d = (dt.date(2025, 1, 1) + dt.timedelta(days=day)).isoformat()
            rows.append(dict(base, inverter_ref=h["ref"], valid_from=h["installed"], valid_to=d,
                             note="inverter failed; replaced under warranty"))
            rows.append(dict(base, inverter_ref=new, valid_from=d, valid_to="", note="replacement inverter"))
        else:
            rows.append(dict(base, inverter_ref=h["ref"], valid_from=h["installed"], valid_to="", note=""))
    cols = ["panel_id", "valid_from", "valid_to", "array_kwp", "array_orientation", "tilt_deg", "inverter_brand",
            "inverter_model", "inverter_ac_kw", "inverter_ref", "installed", "note"]
    return pd.DataFrame(rows)[cols].sort_values(["panel_id", "valid_from"]).reset_index(drop=True)


def market_hours():
    return [M0 + dt.timedelta(hours=t) for t in range(W.H)]


def velkora(w):
    """Hourly energy, local clock, hour beginning, with the portal's UTC offset; one local calendar year."""
    rows = []
    mh = market_hours()
    for h in w["homes"]:
        if h["brand"] != "Velkora":
            continue
        e = W.hourly(h["rec"])
        for t in range(-1, W.H - 1):            # local 2025 starts an hour before market 2025 in daylight saving
            m = M0 + dt.timedelta(hours=t)
            loc = local_of_market(m)
            if loc.year != 2025:
                continue
            off = "+11:00" if loc != m else "+10:00"
            wh = int(round(e[t] * 1000)) if t >= 0 else 0
            rows.append((h["ref"], loc.strftime("%Y-%m-%d %H:%M"), off, wh))
    df = pd.DataFrame(rows, columns=["site_ref", "period_start", "utc_offset", "energy_wh"])
    return df


def ondrava(w):
    """Lifetime yield counters read at each local hour end; a replaced inverter starts its own counter at zero."""
    rng = np.random.default_rng([P.SEED, 13])
    rows = []
    for h in w["homes"]:
        if h["brand"] != "Ondrava":
            continue
        e = W.hourly(h["rec"])
        counter = int(rng.integers(2_000_000, 40_000_000))
        serial = h["ref"]
        chg = h["inv_change"]
        for t in range(-1, W.H - 1):
            m_end = M0 + dt.timedelta(hours=t + 1)
            loc_end = local_of_market(m_end - dt.timedelta(minutes=1)) + dt.timedelta(minutes=1)
            if chg and t == chg[0] * 24 + 7:                  # the new inverter is commissioned at 07:00 market time
                serial, counter = chg[1], 0
            wh = int(round(e[t] * 1000)) if t >= 0 else 0
            counter += wh
            ls = loc_end
            if not (dt.datetime(2025, 1, 1, 1, 0) <= ls <= dt.datetime(2026, 1, 1, 0, 0)):
                continue
            rows.append((serial, ls.strftime("%Y-%m-%d %H:%M"), counter))
    return pd.DataFrame(rows, columns=["serial", "read_at", "total_yield_wh"])


def meter(w):
    """Revenue-meter half hours in market time (interval ending), general import E1, controlled load E2, export B1."""
    rng = np.random.default_rng([P.SEED, 17])
    frames = []
    ends = pd.date_range("2025-01-01 00:30", "2026-01-01 00:00", freq="30min").strftime("%Y-%m-%d %H:%M")
    for h in w["homes"]:
        cl = controlled_load(h, rng)
        h["cl"] = cl
        serial = np.array([h["meter"]] * W.HH, dtype=object)
        qual = np.array(["A"] * W.HH, dtype=object)
        if h["meter_change"]:
            k, new = h["meter_change"]
            serial[k:] = new
            qual[k - 1:k + 1] = "E"
        # communication gaps the network fills from the meter's own register on the next read: substituted values
        for _ in range(int(rng.integers(0, 3))):
            a = int(rng.integers(0, W.HH - 20))
            qual[a:a + int(rng.integers(2, 12))] = "S"
        df = pd.DataFrame({"nmi": h["nmi"], "meter_serial": serial, "interval_end": ends,
                           "e1_kwh": np.round(h["imp"], 3), "e2_kwh": np.round(cl, 3) if h["cl_kwh"] > 0 else np.nan,
                           "b1_kwh": np.round(h["exp"], 3), "quality": qual})
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def connection_register(w):
    rows = []
    rng = np.random.default_rng([P.SEED, 19])
    code_of = {5.0: "MEG-STD", 1.5: "MEG-L15", 0.5: "MEG-CZ05"}
    for h in w["homes"]:
        code = code_of[h["limit"]]
        appr = h["installed"]
        rows.append({"nmi": h["nmi"], "agreement_code": code, "export_limit_kw": h["limit"],
                     "approved_inverter_kw": h["ac"], "effective_from": appr, "effective_to": ""})
    return pd.DataFrame(rows).sort_values("nmi").reset_index(drop=True)


def household_survey(w):
    """The panel's 2024 recruitment survey: dwelling and appliances, as the homes reported them."""
    rng = np.random.default_rng([P.SEED, 23])
    rows = []
    for h in w["homes"]:
        big = h["day_kwh"] > 21
        rows.append({"panel_id": h["pid"], "bedrooms": int(rng.choice([3, 4, 4, 5]) if big else rng.choice([2, 3, 3, 4])),
                     "pool_pump": "Y" if rng.random() < (0.45 if big else 0.12) else "N",
                     "ducted_air_conditioning": "Y" if rng.random() < (0.7 if big else 0.3) else "N",
                     "electric_vehicle": "Y" if rng.random() < 0.06 else "N",
                     "gas_heating": "Y" if rng.random() < (0.5 if h["region"] == "TAR" else 0.2) else "N",
                     "hot_water": "electric off-peak" if h["cl_kwh"] > 0 else rng.choice(["gas", "heat pump", "solar"]),
                     "home_during_day": "most days" if h["typ"] == "retired" else rng.choice(["some days", "rarely"])})
    return pd.DataFrame(rows).sort_values("panel_id").reset_index(drop=True)
