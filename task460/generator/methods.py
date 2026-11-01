"""Everything the build computes from the shipped files: the golden (each area's marginal emission rate by season
and local standard hour, from the hour-to-hour change in its fossil CO2 against the change in its net generation,
weighted by each store's modelled array output), every rung and reflex of the ladder, the estimator variants that
must agree with the golden, the natural mishandlings that must leave the call where it is, and the asks from the
invoices."""
import csv
import datetime as dt
import os

import numpy as np

import world as W

H = 8760
LB_PER_T = 2204.62
T_PER_SHORT_TON = 0.90718474
UTC0 = dt.datetime(2025, 1, 1)
SEASON = {12: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3, 11: 3}
FUELS = ("coal", "natural gas", "petroleum")
COLS = {"coal": "ng_coal_mw", "natural gas": "ng_natural_gas_mw", "petroleum": "ng_petroleum_mw"}


def _rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _num(x):
    return float(x) if x not in ("", None) else 0.0


# ---------------------------------------------------------------------------------------------- reading the pack
def read_codes(target):
    codes = {}
    for r in _rows(os.path.join(target, W.FILES["codes"])):
        codes[r["ba_code"]] = dict(utc=int(r["utc_offset"][:3]), former=r["former_code"] or None)
    return codes


def read_hourly(target, codes):
    """Per area (current code): arrays over the 8,760 UTC hours of 2025, indexed by the hour's start."""
    alias = {c["former"]: k for k, c in codes.items() if c["former"]}
    out = {k: {f: np.zeros(H) for f in ("demand", "ng", "ti", "coal", "natural gas", "petroleum", "nuclear", "hydro",
                                        "wind", "solar")} for k in codes}
    for k in codes:
        out[k]["imputed"] = np.zeros(H, bool)
        out[k]["seen"] = np.zeros(H, bool)
        out[k]["former"] = np.zeros(H, bool)
    for r in _rows(os.path.join(target, W.FILES["hourly"])):
        code = alias.get(r["balancing_area"], r["balancing_area"])
        end = dt.datetime.strptime(r["utc_time_at_end_of_hour"], "%Y-%m-%dT%H:%M:%SZ")
        h = int((end - UTC0).total_seconds() // 3600) - 1
        a = out[code]
        a["demand"][h] = _num(r["demand_mw"])
        a["ng"][h] = _num(r["net_generation_mw"])
        a["ti"][h] = _num(r["total_interchange_mw"])
        for f, col in (("coal", "ng_coal_mw"), ("natural gas", "ng_natural_gas_mw"), ("petroleum", "ng_petroleum_mw"),
                       ("nuclear", "ng_nuclear_mw"), ("hydro", "ng_hydro_mw"), ("wind", "ng_wind_mw"),
                       ("solar", "ng_solar_mw")):
            a[f][h] = _num(r[col])
        a["imputed"][h] = r["demand_imputed"] == "Y"
        a["seen"][h] = True
        a["former"][h] = r["balancing_area"] != code
    for k in codes:
        assert out[k]["seen"].all(), k
    return out


def read_rates(target, name="rates"):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, W.FILES[name]), data_only=True)
    ws = wb.worksheets[0]
    hdr = [c.value for c in ws[3]]
    out = {}
    for row in ws.iter_rows(min_row=4, values_only=True):
        if not row[0]:
            continue
        d = dict(zip(hdr, row))
        t = lambda v: (v / LB_PER_T) if v is not None else None
        out[d["BA code"]] = dict(avg=t(d["CO2 output emission rate (lb/MWh)"]),
                                 fossil=t(d["CO2 fossil output emission rate (lb/MWh)"]),
                                 nb=t(d["CO2 non-baseload output emission rate (lb/MWh)"]),
                                 fuel={"coal": t(d["CO2 coal output emission rate (lb/MWh)"]),
                                       "natural gas": t(d["CO2 gas output emission rate (lb/MWh)"]),
                                       "petroleum": t(d["CO2 oil output emission rate (lb/MWh)"])})
    return out


def register_rates(target):
    """Fuel output rates recomputed from the plant register (short tons to tonnes)."""
    acc = {}
    for r in _rows(os.path.join(target, W.FILES["plants"])):
        f = r["primary_fuel"]
        if f not in FUELS:
            continue
        k = acc.setdefault(r["balancing_area"], {}).setdefault(f, [0.0, 0.0])
        k[0] += _num(r["net_generation_2025_mwh"])
        k[1] += _num(r["co2_2025_short_tons"]) * T_PER_SHORT_TON
    return {a: {f: (v[1] / v[0] if v[0] > 0 else None) for f, v in d.items()} for a, d in acc.items()}


def read_stores(target):
    umap = {r["utility_name"]: r["balancing_area"] for r in _rows(os.path.join(target, W.FILES["utilmap"]))}
    out = {}
    for r in _rows(os.path.join(target, W.FILES["sites"])):
        out[int(r["store_number"])] = dict(name=r["store_name"], town=r["city"], area=umap[r["delivery_utility"]],
                                           dc=float(r["array_kw_dc"]))
    return out


def read_arrays(target):
    out = {}
    for r in _rows(os.path.join(target, W.FILES["arrays"])):
        out.setdefault(int(r["store_number"]), []).append(float(r["ac_output_kw"]))
    return {k: np.array(v) for k, v in out.items()}


def load(target):
    codes = read_codes(target)
    return dict(codes=codes, hourly=read_hourly(target, codes), rates=read_rates(target), reg=register_rates(target),
                stores=read_stores(target), arrays=read_arrays(target))


# ---------------------------------------------------------------------------------------------- clocks
def clock(utc):
    """For an area: each UTC hour's local standard hour (beginning), month and day of the local standard date."""
    t = [UTC0 + dt.timedelta(hours=h + utc) for h in range(H)]
    return np.array([x.hour for x in t]), np.array([x.month for x in t]), np.array([x.timetuple().tm_yday for x in t])


def weights(arr, utc, shift=0):
    """The store's array output placed on the area's UTC hours: local standard hour k is UTC hour k - utc. shift moves
    every hour (an hour's end read as its beginning, or the reverse)."""
    w = np.zeros(H)
    k = np.arange(H)
    h = k - utc + shift
    ok = (h >= 0) & (h < H)
    np.add.at(w, h[ok], arr[ok])
    return w


# ---------------------------------------------------------------------------------------------- the estimators
def emissions(a, rates):
    return sum(a[f] * (rates.get(f) or 0.0) for f in FUELS)


def binned_slope(dy, dx, key, mask=None):
    """OLS slope of dy on dx with an intercept, within each bin of key; every hour gets its bin's slope."""
    out = np.zeros(len(dy))
    m_all = np.ones(len(dy), bool) if mask is None else mask
    for k in np.unique(key):
        m = (key == k)
        mm = m & m_all
        x, y = dx[mm] - dx[mm].mean(), dy[mm] - dy[mm].mean()
        v = (x * x).sum()
        out[m] = (x * y).sum() / v if v > 0 else 0.0
    return out


def mer(a, utc, rates, bins="season_hour", regressor="ng", drop_imputed=False):
    """The marginal emission rate for every UTC hour of 2025: the slope of the hour-to-hour change in the area's fossil
    CO2 on the change in its net generation (or demand, or fossil generation), within bins of the local hour."""
    E = emissions(a, rates)
    lh, mon, _ = clock(utc)
    if bins == "utc_hour":
        lh = (lh - utc) % 24
    x = {"demand": a["demand"], "fossil": sum(a[f] for f in FUELS), "ng": a["ng"]}[regressor]
    dE = np.diff(E, prepend=E[0])
    dX = np.diff(x, prepend=x[0])
    season = np.array([SEASON[m] for m in mon])
    key = {"season_hour": season * 24 + lh, "month_hour": mon * 24 + lh, "hour": lh, "utc_hour": season * 24 + lh,
           "all": np.zeros(H, int)}[bins]
    mask = np.ones(H, bool)
    mask[0] = False
    if drop_imputed:
        imp = a["imputed"] | np.roll(a["imputed"], 1)
        mask &= ~imp
    return binned_slope(dE, dX, key, mask)


def golden(D, **kw):
    """Per store: the avoided CO2 per MWh of its array's 2025 output, the output and the tonnes avoided."""
    out = {}
    for st, s in D["stores"].items():
        code = s["area"]
        utc = D["codes"][code]["utc"]
        m = mer(D["hourly"][code], utc, kw.get("rates_override", {}).get(code, D["rates"][code]["fuel"]),
                bins=kw.get("bins", "season_hour"), regressor=kw.get("regressor", "ng"),
                drop_imputed=kw.get("drop_imputed", False))
        w = weights(D["arrays"][st], utc, kw.get("shift", 0))
        out[st] = dict(area=code, rate=float((m * w).sum() / w.sum()), mwh=float(D["arrays"][st].sum() / 1000.0),
                       tonnes=float((m * w).sum() / 1000.0), mer=m, w=w)
    return out


def golden_current_code_only(D):
    """As golden, with the former-code months of the renamed area out of every regression bin."""
    out = {}
    for st, s in D["stores"].items():
        code = s["area"]
        a = D["hourly"][code]
        utc = D["codes"][code]["utc"]
        E = emissions(a, D["rates"][code]["fuel"])
        lh, mon, _ = clock(utc)
        dE = np.diff(E, prepend=E[0])
        dX = np.diff(a["ng"], prepend=a["ng"][0])
        season = np.array([SEASON[m] for m in mon])
        mask = ~a["former"] & ~np.roll(a["former"], 1)
        mask[0] = False
        m = binned_slope(dE, dX, season * 24 + lh, mask)
        w = weights(D["arrays"][st], utc)
        if a["former"].any():
            w = np.where(a["former"], 0.0, w)
        out[st] = float((m * w).sum() / w.sum())
    return out


# ---------------------------------------------------------------------------------------------- the rungs
def rungs(D):
    """Each easy route's figure per store."""
    g = golden(D)
    out = {}
    for st, s in D["stores"].items():
        code = s["area"]
        a = D["hourly"][code]
        utc = D["codes"][code]["utc"]
        r = D["rates"][code]
        E = emissions(a, r["fuel"])
        w = g[st]["w"]
        dE = np.diff(E, prepend=E[0])
        dD = np.diff(a["demand"], prepend=a["demand"][0])
        x, y = dD[1:] - dD[1:].mean(), dE[1:] - dE[1:].mean()
        pooled = float((x * y).sum() / (x * x).sum())
        dN = np.diff(a["ng"], prepend=a["ng"][0])
        xn = dN[1:] - dN[1:].mean()
        pooled_ng = float((xn * y).sum() / (xn * xn).sum())
        intensity = np.where(a["ng"] > 0, E / a["ng"], 0.0)
        out[st] = dict(area=code, avg=r["avg"], nb=r["nb"], fossil=r["fossil"], pooled=pooled, pooled_ng=pooled_ng,
                       all_hours=float(g[st]["mer"].mean()), hourly_average=float((intensity * w).sum() / w.sum()),
                       golden=g[st]["rate"])
    return out


def ranking(fig, key):
    return sorted(fig, key=lambda st: -fig[st][key])


# ---------------------------------------------------------------------------------------------- the asks
SERVICE = "Halworth Utility Payment Services LLC"
Y0, Y1 = dt.date(2025, 1, 1), dt.date(2025, 12, 31)


def read_invoices(target):
    rows = _rows(os.path.join(target, W.FILES["invoices"]))
    for r in rows:
        r["qty"] = float(r["quantity"]) if r["quantity"] else None
        r["amt"] = float(r["line_amount_usd"])
        r["d0"] = dt.date.fromisoformat(r["service_period_start"])
        r["d1"] = dt.date.fromisoformat(r["service_period_end"])
        r["idate"] = dt.date.fromisoformat(r["invoice_date"])
        r["store"] = int(r["store_number"])
        r["src"] = ("supplier" if r["vendor_name"] == W.SUPPLIER else "service" if r["vendor_name"] == SERVICE
                    else "utility")
    return rows


def in_2025(d0, d1):
    a, b = max(d0, Y0), min(d1, Y1)
    return max((b - a).days + 1, 0) / ((d1 - d0).days + 1)


def overlap(a, b, m0, m1):
    return max((min(b, m1) - max(a, m0)).days + 1, 0)


def month_bounds(y, m):
    m0 = dt.date(y, m, 1)
    m1 = (dt.date(y + 1, 1, 1) if m == 12 else dt.date(y, m + 1, 1)) - dt.timedelta(days=1)
    return m0, m1


DIST_ENERGY = ("Distribution energy charge", "Delivery service - energy", "Distribution kWh charge",
               "Energy delivery charge", "Distribution charge per kWh", "Delivery energy charge", "Distribution energy",
               "Electric distribution energy charge")


def is_gas(r):
    d = r["line_description"]
    return d.startswith("Gas ") or d.endswith(", gas service")


def utility_cycles(rows):
    """The delivery utilities' own invoices that reached accounts payable: per meter, each service period's metered kWh
    (the distribution energy quantity, Tennaford's declining blocks summed). A bill the payment service paid carries
    no quantity."""
    cyc = {}
    for r in rows:
        d = r["line_description"]
        if r["src"] == "utility" and r["unit_of_measure"] == "KWH" and (d in DIST_ENERGY or
                                                                        d.startswith("Distribution kWh charge,")):
            cyc.setdefault(r["meter_number"], {})
            k = (r["d0"], r["d1"])
            cyc[r["meter_number"]][k] = cyc[r["meter_number"]].get(k, 0.0) + r["qty"]
    return {m: sorted((a, b, q) for (a, b), q in v.items()) for m, v in cyc.items()}


def supplier_cycles(rows):
    """The supplier's invoices: per meter and service period (the utility's read cycle), its energy quantity and,
    while its first term ran, the renewable portfolio standard line's quantity."""
    out = {}
    for r in rows:
        if r["src"] != "supplier":
            continue
        e = out.setdefault(r["meter_number"], {}).setdefault((r["d0"], r["d1"]), dict(energy=None, rps=None))
        if r["line_description"] == "Energy - fixed price":
            e["energy"] = r["qty"]
        elif r["line_description"].startswith("Renewable portfolio standard"):
            e["rps"] = r["qty"]
    return out


def allocated(cycles, m0, m1):
    return sum(q * overlap(a, b, m0, m1) / ((b - a).days + 1) for a, b, q in cycles)


def loss_factor(cycles, sup):
    """The supplier's first-term quantity over the meter's kWh, over every cycle both the utility's own invoices and
    the supplier's first term bill."""
    own = {(a, b): q for a, b, q in cycles}
    num = sum(e["energy"] for k, e in sup.items() if e["rps"] is not None and k in own)
    den = sum(own[k] for k, e in sup.items() if e["rps"] is not None and k in own)
    return num / den if den else None


def metered(rows):
    """Per meter: its metered kWh by read cycle. The utility's own invoice where it reached accounts payable; else the
    supplier's bill for the cycle: its first term billed the meter's kWh grossed up by the territory's loss factor (the
    ratio its quantities bear to the meter's in every cycle both bill), the standard's cost on the same quantity; its
    second term (no standard line) bills the meter's kWh."""
    cyc, sup = utility_cycles(rows), supplier_cycles(rows)
    out, lf = {}, {}
    for meter, bills in sup.items():
        own = {(a, b): q for a, b, q in cyc.get(meter, [])}
        f = loss_factor(cyc.get(meter, []), bills)
        lf[meter] = f
        out[meter] = sorted((a, b, own[(a, b)] if (a, b) in own else (e["energy"] / f if e["rps"] is not None
                                                                         else e["energy"]))
                            for (a, b), e in bills.items())
    return out, lf, cyc


def asks(target, D, golden_fig):
    rows = read_invoices(target)
    mon, lf, cyc = metered(rows)
    meter_store = {}
    for r in rows:
        if r["src"] == "supplier":
            meter_store[r["meter_number"]] = r["store"]
    out = {}
    for st, s in D["stores"].items():
        ms = [m for m in mon if meter_store[m] == st]
        use = sum(q * in_2025(a, b) for m in ms for a, b, q in mon[m]) / 1000.0
        months = np.array([sum(allocated(mon[m], *month_bounds(2025, k)) for m in ms) for k in range(1, 13)]) / 1000.0
        paid = sum(r["amt"] * in_2025(r["d0"], r["d1"]) for r in rows if r["store"] == st and not is_gas(r))
        arr_m = np.zeros(12)
        t0 = dt.datetime(2025, 1, 1)
        arr = D["arrays"][st]
        for k in range(H):
            arr_m[(t0 + dt.timedelta(hours=k)).month - 1] += arr[k] / 1000.0
        out[st] = dict(use_mwh=use, paid=paid, price=paid / use, share=100.0 * golden_fig[st]["mwh"] / use,
                       months=months, array_months=arr_m, lf={m: lf[m] for m in ms})
    return out


def ask_wrong_paths(target, D, golden_fig):
    """The natural and half-repaired readings of the invoice asks, each a complete pipeline. Use: every kWh line summed;
    the utilities' own invoices alone; the utilities' invoices with the supplier's energy quantity filling the cycles
    they no longer carry, as billed or divided by the loss factor learnt where both bill (the reconciled fill); the
    supplier's energy quantity for the whole year, as billed or divided by that factor. Dollars: a bill that
    reached accounts payable and was paid by the service as well counted once; the service's lines left out; the gas
    lines kept."""
    rows = read_invoices(target)
    cyc, sup = utility_cycles(rows), supplier_cycles(rows)
    meter_store = {r["meter_number"]: r["store"] for r in rows if r["src"] == "supplier"}
    direct_bills = {r["invoice_number"] for r in rows if r["src"] == "utility"}
    out = {}
    for st in D["stores"]:
        acc = dict(kwh_all=0.0, util_only=0.0, fill_raw=0.0, fill_recon=0.0, sup_raw=0.0, sup_lf=0.0)
        for meter, bills in sup.items():
            if meter_store[meter] != st:
                continue
            own = {(a, b): q for a, b, q in cyc.get(meter, [])}
            f = loss_factor(cyc.get(meter, []), bills)
            acc["util_only"] += sum(q * in_2025(a, b) for (a, b), q in own.items())
            for (a, b), e in bills.items():
                fr = in_2025(a, b)
                acc["sup_raw"] += e["energy"] * fr
                acc["sup_lf"] += e["energy"] / f * fr
                if (a, b) in own:
                    acc["fill_raw"] += own[(a, b)] * fr
                    acc["fill_recon"] += own[(a, b)] * fr
                else:
                    acc["fill_raw"] += e["energy"] * fr
                    acc["fill_recon"] += e["energy"] / f * fr
        acc["kwh_all"] = sum(r["qty"] * in_2025(r["d0"], r["d1"]) for r in rows
                             if r["store"] == st and r["unit_of_measure"] == "KWH")
        out[st] = {k: v / 1000.0 for k, v in acc.items()}
        paid = lambda keep: sum(r["amt"] * in_2025(r["d0"], r["d1"]) for r in rows if r["store"] == st and keep(r))
        twice = lambda r: r["src"] == "service" and r["line_description"].split(" bill ")[1].split()[0] in direct_bills
        out[st].update(paid_dedup=paid(lambda r: not is_gas(r) and not twice(r)),
                       paid_no_service=paid(lambda r: not is_gas(r) and r["src"] != "service"),
                       paid_with_gas=paid(lambda r: True),
                       paid_golden=paid(lambda r: not is_gas(r)))
    return out
