"""Write the data files of the pack: the agency's hourly operating data and plant register, its published rates
(2025, and the 2024 edition), the engineering firm's array model, Corvane's store sites, the code and utility
tables and the accounts-payable invoice lines."""
import csv
import datetime as dt
import io

import numpy as np

import grid as G
import world as W

H = 8760
LB_PER_T = 2204.62
T_PER_SHORT_TON = 0.90718474
UTC0 = dt.datetime(2025, 1, 1)


def write_csv(path, cols, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(r)
        n += 1
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())
    return n


def iso_off(hours):
    sign = "-" if hours < 0 else "+"
    return "%s%02d:00" % (sign, abs(hours))


def local_clock(code):
    """For each UTC hour beginning h, the end of the hour on the area's local clock (standard time all year; the
    country keeps no daylight saving) and its UTC offset."""
    a = W.AREAS[code]
    out = []
    for h in range(H):
        end = UTC0 + dt.timedelta(hours=h + 1)
        out.append(((end + dt.timedelta(hours=a["utc"])).strftime("%Y-%m-%dT%H:%M:%S") + iso_off(a["utc"]), a["utc"]))
    return out


def imputed_hours(rng):
    """Telemetry gaps the operator filled: a few short runs of hours per area."""
    out = {}
    for code in W.ORDER:
        hrs = set()
        for _ in range(int(rng.integers(5, 9))):
            start = int(rng.integers(30, H - 30))
            hrs.update(range(start, start + int(rng.integers(2, 6))))
        out[code] = sorted(hrs)
    return out


HOURLY_COLS = ["balancing_area", "utc_time_at_end_of_hour", "local_time_at_end_of_hour", "demand_forecast_mw",
               "demand_mw", "demand_imputed", "net_generation_mw", "total_interchange_mw", "ng_coal_mw",
               "ng_natural_gas_mw", "ng_nuclear_mw", "ng_petroleum_mw", "ng_hydro_mw", "ng_wind_mw", "ng_solar_mw",
               "ng_other_mw"]


def hourly_series(world, seed=W.SEED + 31):
    """Integer MW columns per area as the operator files them, with the operator's imputed demand hours and the
    solar plants' station service at night."""
    rng = np.random.default_rng(seed)
    imp = imputed_hours(rng)
    out = {}
    for code in W.ORDER:
        g = world[code]
        f = {k: np.round(v).astype(int) for k, v in g["fuel"].items()}
        cols = {"coal": f.get("coal", np.zeros(H, int)), "natural gas": f.get("natural gas", np.zeros(H, int)),
                "petroleum": f.get("petroleum", np.zeros(H, int)),
                "nuclear": np.round(g["nuc"]).astype(int), "hydro": np.round(g["hydro"]).astype(int),
                "wind": np.round(g["wind"]).astype(int)}
        sol = np.round(g["usolar"]).astype(int)
        night = sol <= 0
        sol[night] = -rng.integers(1, 5, night.sum())
        cols["solar"] = sol if W.AREAS[code].get("solar", 0) else np.zeros(H, int)
        ng = sum(cols.values())
        ti = np.round(g["ti"]).astype(int)
        demand = ng - ti
        dem_rep = demand.astype(float).copy()
        flag = np.array([""] * H, dtype=object)
        for h in imp[code]:
            flag[h] = "Y"
        # imputed hours: the operator files the hour's demand from its net generation and interchange (the hour's
        # own telemetry for demand was lost); the value equals the balance, rounded to the nearest 5 MW
        hs = imp[code]
        for h in hs:
            dem_rep[h] = 5 * round(demand[h] / 5.0)
        dem_rep = np.round(dem_rep).astype(int)
        fc = np.round(g["load"] * (1 + G.ar1(rng, H, 0.95, 0.004)) + rng.normal(0, 25, H)).astype(int)
        out[code] = dict(cols=cols, ng=ng, ti=ti, demand=dem_rep, demand_true=demand, flag=flag, forecast=fc,
                         imputed=hs)
    return out


def hourly_rows(series):
    for code in W.ORDER:
        s = series[code]
        clock = local_clock(code)
        former = W.AREAS[code].get("former")
        for h in range(H):
            end = UTC0 + dt.timedelta(hours=h + 1)
            ba = code
            if former and (end + dt.timedelta(hours=clock[h][1])) <= dt.datetime(2025, 7, 1, 0):
                ba = former
            c = s["cols"]
            yield [ba, end.strftime("%Y-%m-%dT%H:%M:%SZ"), clock[h][0], int(s["forecast"][h]), int(s["demand"][h]),
                   s["flag"][h], int(s["ng"][h]), int(s["ti"][h]), int(c["coal"][h]) if W.AREAS[code].get("blocks") and
                   any(b[1] == "coal" for b in W.AREAS[code]["blocks"]) else "",
                   int(c["natural gas"][h]), int(c["nuclear"][h]) if W.AREAS[code].get("nuc") else "",
                   int(c["petroleum"][h]) if any(b[1] == "petroleum" for b in W.AREAS[code]["blocks"]) else "",
                   int(c["hydro"][h]) if W.AREAS[code].get("hydro") else "", int(c["wind"][h]),
                   int(c["solar"][h]) if W.AREAS[code].get("solar") else "", ""]


ARRAY_COLS = ["store_number", "model_run", "hour_beginning_lst", "ac_output_kw"]


def array_rows(arrays):
    t0 = dt.datetime(2025, 1, 1)
    for code in W.ORDER:
        s = W.STORES[code]
        run = "LRS-26-%04d-B" % s["store"]
        v = arrays[code]
        for k in range(H):
            yield [s["store"], run, (t0 + dt.timedelta(hours=k)).strftime("%Y-%m-%d %H:%M"), "%.1f" % v[k]]


PLANT_COLS = ["plant_code", "plant_name", "balancing_area", "primary_fuel", "prime_mover", "nameplate_mw",
              "net_generation_2025_mwh", "co2_2025_short_tons", "operating_status"]


def register(world, series):
    """The register's plant rows: fossil plants' annual net generation from the dispatch, zero-emission plants'
    from the area's hourly series shared out by nameplate; CO2 in short tons."""
    rows = []
    for code in W.ORDER:
        g = world[code]
        for p in g["plants"].values():
            gen = float(p["gen"].sum())
            rows.append(dict(code=p["code"], name=p["name"], ba=code, fuel=p["fuel"], pm=p["pm"], mw=p["mw"],
                             gen=round(gen), co2=round(gen * p["rate"] / T_PER_SHORT_TON) if gen > 0 else 0,
                             status="OP"))
        clean = {"nuclear": g["nuc"], "hydro": g["hydro"], "wind": g["wind"], "solar": g["usolar"]}
        for fuel in ("nuclear", "hydro", "wind", "solar"):
            plist = [p for p in W.CLEAN_PLANTS[code] if p[2] == fuel]
            if not plist:
                continue
            tot = float(np.clip(clean[fuel], 0, None).sum())
            cap = sum(p[4] for p in plist)
            for p in plist:
                rows.append(dict(code=p[0], name=p[1], ba=code, fuel=fuel, pm=p[3], mw=p[4], gen=round(tot * p[4] / cap),
                                 co2=0, status="OP"))
    rows.sort(key=lambda r: (W.ORDER.index(r["ba"]), r["code"]))
    return rows


def plant_rows(rows):
    for r in rows:
        yield [r["code"], r["name"], r["ba"], r["fuel"], r["pm"], r["mw"], r["gen"], r["co2"], r["status"]]


def rates_table(plants):
    """The agency's published figures by area, computed from the register: generation and CO2 by fuel, the output
    rates in pounds per MWh and the non-baseload output rate."""
    out = {}
    for code in W.ORDER:
        rs = [r for r in plants if r["ba"] == code]
        gen = sum(r["gen"] for r in rs)
        co2_t = sum(r["co2"] * T_PER_SHORT_TON for r in rs)
        fos = [r for r in rs if r["fuel"] in ("coal", "natural gas", "petroleum")]
        fgen = sum(r["gen"] for r in fos)
        fuel = {}
        for f in ("coal", "natural gas", "petroleum", "nuclear", "hydro", "wind", "solar"):
            g = sum(r["gen"] for r in rs if r["fuel"] == f)
            c = sum(r["co2"] * T_PER_SHORT_TON for r in rs if r["fuel"] == f)
            fuel[f] = (g, c)
        num = den = 0.0
        for r in fos:
            cf = r["gen"] / (r["mw"] * H)
            w = 1.0 if cf < 0.2 else (0.0 if cf > 0.8 else (0.8 - cf) / 0.6)
            num += w * r["co2"] * T_PER_SHORT_TON
            den += w * r["gen"]
        lb = lambda c, g: round(c / g * LB_PER_T, 1) if g > 0 else None
        out[code] = dict(gen=gen, co2_short=round(co2_t / T_PER_SHORT_TON), avg=lb(co2_t, gen), fossil=lb(co2_t, fgen),
                         coal=lb(*fuel["coal"][::-1]), gas=lb(*fuel["natural gas"][::-1]),
                         oil=lb(*fuel["petroleum"][::-1]), nb=lb(num, den),
                         mix={f: fuel[f][0] / gen for f in fuel})
    return out


SITE_COLS = ["store_number", "store_name", "city", "latitude", "longitude", "delivery_utility", "array_kw_dc",
             "array_kw_ac", "tilt_deg", "azimuth_deg", "roof_area_sq_ft", "feasibility_study"]


def site_rows():
    for code in W.ORDER:
        s = W.STORES[code]
        yield [s["store"], "Corvane %s" % s["town"], s["town"], "%.4f" % s["lat"], "%.4f" % s["lon"], s["utility"],
               s["dc"], s["ac"], s["tilt"], s["az"], s["roof"], "FS-2026-%04d" % s["store"]]


CODE_COLS = ["ba_code", "ba_name", "utc_offset", "former_code", "code_effective"]


def code_rows():
    for code in W.ORDER:
        a = W.AREAS[code]
        yield [code, a["ba"], iso_off(a["utc"]), a.get("former", ""), "2025-07-01" if a.get("former") else ""]


UTIL_COLS = ["utility_name", "utility_type", "balancing_area", "retail_choice"]


def util_rows():
    extra = {"BRKW": [("Monongah Valley Electric Cooperative", "cooperative")],
             "QLBY": [("North Country Municipal Power", "municipal")],
             "TNFD": [("Prairie Lakes Rural Electric", "cooperative")],
             "GRSF": [("Meramec Electric Cooperative", "cooperative")],
             "FRVW": [("Cascade Ridge Public Utility District", "public power")],
             "OSTM": [("Salt Flats Irrigation and Power District", "public power")],
             "KSTP": [("Santa Clara Valley Municipal Electric", "municipal")],
             "HLVN": [("Piedmont Electric Membership Corporation", "cooperative")]}
    rows = []
    for code in W.ORDER:
        rows.append([W.STORES[code]["utility"], "investor-owned", code, "Y"])
        for nm, kind in extra[code]:
            rows.append([nm, kind, code, "N"])
    rows.sort(key=lambda r: r[0])
    return rows


INVOICE_COLS = ["vendor_number", "vendor_name", "invoice_number", "invoice_date", "store_number", "account_number",
                "meter_number", "service_period_start", "service_period_end", "line_number", "line_description",
                "quantity", "unit_of_measure", "line_amount_usd"]


def invoice_rows(lines):
    for r in lines:
        q = r["qty"]
        yield [r["vendor"], r["vendor_name"], r["invoice"], r["invoice_date"].isoformat(), r["store"], r["account"],
               r["meter"], r["service_from"].isoformat(), r["service_to"].isoformat(), r["line"], r["desc"],
               ("%g" % q) if q != "" else "", r["uom"], "%.2f" % r["amount"]]
