"""The pack's data files, written from the truth in world.py: the residential property price register as the old
system filed it to 10 October 2025 and as the new system has filed it since 1 October 2025, the valuation register's
dwelling attributes, the address point file with each building's electoral division, the electoral divisions, the
census dwelling stock, and two files the index does not use (rents and mortgage drawdowns)."""
import csv
import datetime as dt

import numpy as np

import world as W

FILES = {
    "ppr_old": "ppr_residential_sales_filed_2024-10-01_to_2025-10-10.csv",
    "ppr_new": "ppr_residential_sales_filed_2025-10-01_to_2026-10-14.csv",
    "valuation": "valuation_register_dwellings_extract_2026-10-15.csv",
    "points": "address_points_buildings_extract_2026-10-15.csv",
    "eds": "bso_electoral_divisions_2026.csv",
    "census": "census_2022_dwelling_stock_by_area_and_type.xlsx",
    "method": "bso_rppi_methodology_note_2026.pdf",
    "circular": "dhlgh_circular_rapid_price_growth_areas_2026.pdf",
    "rents": "rta_registered_rents_by_area_2026q2.xlsx",
    "mortgages": "mortgage_drawdowns_by_area_2025-2026.csv",
    "dictionary": "bso_data_dictionary.csv",
    "manifest": "bso_extract_manifest_2026-10-15.csv",
}
COMPANY = "Brannagh Statistics Office"
OLD_COLS = ["Date of Sale (dd/mm/yyyy)", "Address", "County", "Eircode", "Price (€)", "Not Full Market Price",
            "VAT Exclusive", "Description of Property", "Property Size Description"]
NEW_COLS = ["transaction_id", "property_number", "eircode", "la_code", "sale_date", "filed_date", "consideration_eur",
            "market_basis", "dwelling_status"]
VAL_COLS = ["property_number", "eircode", "address", "la_code", "dwelling_type", "floor_area_m2", "year_built",
            "valuation_date"]
PT_COLS = ["eircode", "building_id", "ed_code", "latitude", "longitude", "address_point_status"]
ED_COLS = ["ed_code", "ed_name", "la_code", "la_name"]
MORT_COLS = ["la_code", "quarter", "drawdowns", "value_eur_m", "first_time_buyer_share_pct"]
OLD_WINDOW = (dt.date(2024, 10, 1), dt.date(2025, 10, 10))
NEW_WINDOW = (dt.date(2025, 10, 1), dt.date(2026, 10, 14))
VTYPE = {"detached": "Detached house", "semi-detached": "Semi-detached house", "terraced": "Terraced house",
         "apartment": "Apartment"}
STREETS = ["Main Street", "Church Road", "The Green", "Station Road", "Mill Lane", "Abbey View", "Oak Park",
           "Riverside", "Chapel Hill", "Meadow Court", "Ashgrove", "Castle Heights", "Fairfield", "Woodlands",
           "Beechwood Avenue", "Hazel Close", "The Paddocks", "Cherry Lawn", "Willow Rise", "Glebe Road"]
ROUTING = {c: "G%02d" % (11 + 4 * i) for i, c in enumerate(W.CODES)}
EIR_CHARS = "ACDEFHKNPRTVWXY0123456789"
BLOCK_A = ["Harbour", "Linden", "Quarry", "Foundry", "Granary", "Weir", "Tannery", "Maltings", "Orchard", "Sorrel",
           "Heron", "Kestrel", "Larch", "Rowan", "Alder", "Brook"]
BLOCK_B = ["Court", "House", "Place", "Yard", "Square"]


def write_csv(path, cols, rows, encoding="utf-8"):
    with open(path, "w", newline="", encoding=encoding) as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])
    return len(rows)


def _edge(rng, x):
    """Sales just outside the two index years that the extract also carries: July to September 2024 sales filed
    from October 2024, and October 2026 sales filed by 14 October."""
    eds = {}
    for e in x["eds"]:
        eds.setdefault(e["area"], []).append(e)
    out = []
    for a in x["areas"]:
        for lo, hi, share in ((dt.date(2024, 7, 1), dt.date(2024, 9, 30), 0.25), (dt.date(2026, 10, 1),
                                                                                   dt.date(2026, 10, 14), 0.04)):
            dd = [d for d in W.days(lo, hi) if d.weekday() < 5]
            for _ in range(int(a["n"] * share)):
                e = eds[a["code"]][int(rng.integers(0, len(eds[a["code"]])))]
                t = W.TYPES[int(rng.choice(4, p=W.TMIX))]
                fl = W.TFLOOR[t] * float(np.exp(rng.normal(0, 0.17)))
                d = dd[int(rng.integers(0, len(dd)))]
                lp = (W._level(a["level"], d, a["growth"]) + e["eff"] + W.TEFF[t] + W.ELAST * np.log(fl / 100.0)
                      + float(rng.normal(0, W.NOISE)))
                out.append({"area": a["code"], "ed": e["code"], "type": t, "floor": round(fl, 1), "new": False,
                            "built": 1998, "date": d, "price": round(float(np.exp(lp)) / 500.0) * 500.0,
                            "market": True, "bulk": None, "edge": True})
    return out


def ids(x):
    """Property numbers, eircodes, addresses, filing days and transaction ids, in one seeded pass."""
    rng = np.random.default_rng(W.SEED + 1)
    x["sales"] += _edge(rng, x)
    used = set()
    addrs = set()
    blocks = {}
    for i, j in enumerate(rng.permutation(len(x["sales"]))):
        s = x["sales"][j]
        s["pn"] = "%07d" % (1204411 + 13 * i)
        while True:
            e = ROUTING[s["area"]] + " " + "".join(EIR_CHARS[int(k)] for k in rng.integers(0, len(EIR_CHARS), 4))
            if e not in used and not e[4].isdigit():
                used.add(e)
                break
        s["eircode"] = e
        if s["bulk"] is not None:
            k, units = s["bulk"]
            n = blocks.setdefault(k, [0])
            n[0] += 1
            s["address"] = "Apartment %d, %s %s, %s" % (n[0], BLOCK_A[k % len(BLOCK_A)], BLOCK_B[k // len(BLOCK_A)],
                                                       W.NAMES[s["area"]])
        elif s["type"] == "apartment":
            while True:
                s["address"] = "Apartment %d, %d %s, %s" % (int(rng.integers(1, 40)), int(rng.integers(1, 90)),
                                                           STREETS[int(rng.integers(0, len(STREETS)))],
                                                           W.NAMES[s["area"]])
                if s["address"] not in addrs:
                    break
        else:
            while True:
                s["address"] = "%d %s, %s" % (int(rng.integers(1, 900)), STREETS[int(rng.integers(0, len(STREETS)))],
                                              W.NAMES[s["area"]])
                if s["address"] not in addrs:
                    break
        addrs.add(s["address"])
        lag = int(min(150, max(3, round(float(rng.lognormal(np.log(26), 0.55))))))
        s["filed"] = s["date"] + dt.timedelta(days=lag)
        if s["bulk"] is not None:
            s["filed"] = s["date"] + dt.timedelta(days=21)
        s["eir_shown"] = rng.random() > 0.08
        s["eir_style"] = int(rng.integers(0, 4))
        s["lat"] = 53.2 + (W.CODES.index(s["area"]) % 4) * 0.31 + float(rng.uniform(0, 0.25))
        s["lon"] = -8.9 + (W.CODES.index(s["area"]) // 4) * 0.42 + float(rng.uniform(0, 0.35))
    x["sales"].sort(key=lambda s: s["pn"])
    for i, s in enumerate(sorted(x["sales"], key=lambda s: (s["filed"], s["pn"]))):
        s["tid"] = "PPR-%06d" % (500113 + 3 * i)


def filed_price(s, vat_exclusive):
    return round(s["price"] / (1 + W.VAT), 2) if (vat_exclusive and s["new"]) else s["price"]


def _eir(s):
    e = s["eircode"]
    return [e, e.replace(" ", ""), e.lower(), " " + e][s["eir_style"]]


def _size_desc(s):
    if not s["new"]:
        return ""
    if s["floor"] < 38:
        return "less than 38 sq metres"
    if s["floor"] < 125:
        return "greater than or equal to 38 sq metres and less than 125 sq metres"
    return "greater than or equal to 125 sq metres"


def old_rows(x):
    """The old system's filings, 1 October 2024 to 10 October 2025, in its public layout: day-first dates, a euro
    price as text, new dwellings filed exclusive of VAT, the eircode as keyed and sometimes missing."""
    rows = []
    for s in sorted(x["sales"], key=lambda s: (s["filed"], s["pn"])):
        if not OLD_WINDOW[0] <= s["filed"] <= OLD_WINDOW[1]:
            continue
        price = filed_price(s, True)
        rows.append((s["date"].strftime("%d/%m/%Y"), s["address"], W.NAMES[s["area"]],
                     _eir(s) if s["eir_shown"] else "", "€{:,.2f}".format(price),
                     "No" if s["market"] else "Yes", "Yes" if s["new"] else "No",
                     "New Dwelling house /Apartment" if s["new"] else "Second-Hand Dwelling house /Apartment",
                     _size_desc(s)))
    return rows


def new_rows(x):
    """The new system's filings from 1 October 2025 (it ran beside the old one to 10 October): ISO dates, the
    consideration including VAT, the property number and the eircode as the register holds them."""
    rows = []
    for s in sorted(x["sales"], key=lambda s: (s["filed"], s["tid"])):
        if not NEW_WINDOW[0] <= s["filed"] <= NEW_WINDOW[1]:
            continue
        rows.append((s["tid"], s["pn"], s["eircode"], s["area"], s["date"].isoformat(), s["filed"].isoformat(),
                     "%.2f" % s["price"], "FMP" if s["market"] else "NFMP", "NEW" if s["new"] else "SH"))
    return rows


def in_extract(s):
    return OLD_WINDOW[0] <= s["filed"] <= OLD_WINDOW[1] or NEW_WINDOW[0] <= s["filed"] <= NEW_WINDOW[1]


def valuation_rows(x):
    rows = []
    for s in x["sales"]:
        if in_extract(s):
            vd = dt.date(2025, 6, 30) if s["date"] < dt.date(2025, 6, 30) or not s["new"] else dt.date(2026, 6, 30)
            rows.append((s["pn"], s["eircode"], s["address"], s["area"], VTYPE[s["type"]], "%.1f" % s["floor"],
                         s["built"], vd.isoformat()))
    return rows


def point_rows(x):
    rows = []
    bid = {}
    for s in x["sales"]:
        if in_extract(s):
            key = s["address"].split(", ", 1)[1] if s["bulk"] is not None else s["pn"]
            b = bid.setdefault(key, "B%08d" % (30117 + 11 * len(bid)))
            rows.append((s["eircode"], b, s["ed"], "%.5f" % s["lat"], "%.5f" % s["lon"], "active"))
    rows.sort()
    return rows


def ed_rows(x):
    return [(e["code"], e["name"], e["area"], W.NAMES[e["area"]]) for e in sorted(x["eds"], key=lambda e: e["code"])]


def stock(x):
    """Census 2022 occupied and vacant dwellings by area and type: the stock of which a year's sales are about four
    in a hundred, in the area's long-run mix."""
    rng = np.random.default_rng(W.SEED + 3)
    out = {}
    for a in x["areas"]:
        tot = int(a["n"] / 0.041)
        mix = np.array(W.TMIX) * rng.uniform(0.9, 1.1, 4)
        mix = mix / mix.sum()
        out[a["code"]] = [int(round(tot * m / 10.0)) * 10 for m in mix]
    return out


def mortgage_rows(x):
    rng = np.random.default_rng(W.SEED + 4)
    rows = []
    for a in x["areas"]:
        for q in ("2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2"):
            n = int(a["n"] / 4 * float(rng.uniform(0.45, 0.6)))
            rows.append((a["code"], q, n, "%.1f" % (n * float(np.exp(a["level"])) * float(rng.uniform(0.78, 0.86)) / 1e6),
                         "%.1f" % float(rng.uniform(44, 58))))
    return rows
