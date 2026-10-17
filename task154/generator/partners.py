"""Goods trade by partner country and SITC division, as TBS's portal bulk download holds it, and the port loadings.

Every coal miner and both LNG projects lodge periodic export entries, a month's cargoes on one entry lodged in the
following month. TBS's old processing system recorded those entries in the month they were lodged; the new system,
which compiled the statistics from the January 2026 month, dates them by the shipments on their lines, and the
entries lodged in January 2026 for December's cargoes were added to December 2025. Nothing else in the trade
statistics moved month. The ports record each cargo in the month it was loaded."""
from __future__ import annotations

import numpy as np

import common as K
import world as WD

MI = WD.MI
NM = WD.NM
FIRST = "2023-01"          # the bulk download's first month
LAST_PULL = "2026-05"      # the desk's pull on 24 June holds May as the latest month
NEW_SYSTEM = WD.NEW_SYSTEM

# ISO 3166 alpha-2, name, TBS region
COUNTRIES = [
    ("AE", "United Arab Emirates", "Middle East"), ("AR", "Argentina", "Americas"), ("AT", "Austria", "Europe"),
    ("AU", "Australia", "Oceania"), ("BD", "Bangladesh", "South Asia"), ("BE", "Belgium", "Europe"),
    ("BR", "Brazil", "Americas"), ("CA", "Canada", "Americas"), ("CH", "Switzerland", "Europe"),
    ("CL", "Chile", "Americas"), ("CN", "China", "North Asia"), ("CZ", "Czechia", "Europe"),
    ("DE", "Germany", "Europe"), ("DK", "Denmark", "Europe"), ("DZ", "Algeria", "Africa"),
    ("EG", "Egypt", "Africa"), ("ES", "Spain", "Europe"), ("FI", "Finland", "Europe"), ("FJ", "Fiji", "Oceania"),
    ("FR", "France", "Europe"), ("GB", "United Kingdom", "Europe"), ("HK", "Hong Kong", "North Asia"),
    ("ID", "Indonesia", "South-East Asia"), ("IE", "Ireland", "Europe"), ("IL", "Israel", "Middle East"),
    ("IN", "India", "South Asia"), ("IT", "Italy", "Europe"), ("JP", "Japan", "North Asia"),
    ("KR", "Korea, Republic of", "North Asia"), ("KW", "Kuwait", "Middle East"), ("LK", "Sri Lanka", "South Asia"),
    ("MX", "Mexico", "Americas"), ("MY", "Malaysia", "South-East Asia"), ("NC", "New Caledonia", "Oceania"),
    ("NL", "Netherlands", "Europe"), ("NO", "Norway", "Europe"), ("NZ", "New Zealand", "Oceania"),
    ("OM", "Oman", "Middle East"), ("PE", "Peru", "Americas"), ("PG", "Papua New Guinea", "Oceania"),
    ("PH", "Philippines", "South-East Asia"), ("PK", "Pakistan", "South Asia"), ("PL", "Poland", "Europe"),
    ("QA", "Qatar", "Middle East"), ("SA", "Saudi Arabia", "Middle East"), ("SE", "Sweden", "Europe"),
    ("SG", "Singapore", "South-East Asia"), ("TH", "Thailand", "South-East Asia"), ("TR", "Türkiye", "Europe"),
    ("TW", "Taiwan", "North Asia"), ("US", "United States", "Americas"), ("VN", "Viet Nam", "South-East Asia"),
    ("ZA", "South Africa", "Africa"),
]
SPECIAL = [("QS", "Ship and aircraft stores", "Not applicable"), ("QU", "Country not stated", "Not applicable")]
CODES = [c for c, _, _ in COUNTRIES]

# SITC Rev. 4 divisions TBS reports, with their section
DIVISIONS = [
    ("00", "Live animals other than animals of division 03"), ("01", "Meat and meat preparations"),
    ("02", "Dairy products and birds' eggs"), ("03", "Fish, crustaceans, molluscs and aquatic invertebrates"),
    ("04", "Cereals and cereal preparations"), ("05", "Vegetables and fruit"),
    ("06", "Sugars, sugar preparations and honey"), ("07", "Coffee, tea, cocoa, spices, and manufactures thereof"),
    ("08", "Feeding stuff for animals (not including unmilled cereals)"),
    ("09", "Miscellaneous edible products and preparations"), ("11", "Beverages"),
    ("12", "Tobacco and tobacco manufactures"), ("21", "Hides, skins and furskins, raw"),
    ("22", "Oil-seeds and oleaginous fruits"), ("24", "Cork and wood"), ("25", "Pulp and waste paper"),
    ("26", "Textile fibres and their wastes"), ("27", "Crude fertilizers and crude minerals"),
    ("28", "Metalliferous ores and metal scrap"), ("29", "Crude animal and vegetable materials, n.e.s."),
    ("32", "Coal, coke and briquettes"), ("33", "Petroleum, petroleum products and related materials"),
    ("34", "Gas, natural and manufactured"), ("41", "Animal oils and fats"),
    ("42", "Fixed vegetable fats and oils, crude, refined or fractionated"),
    ("51", "Organic chemicals"), ("52", "Inorganic chemicals"), ("53", "Dyeing, tanning and colouring materials"),
    ("54", "Medicinal and pharmaceutical products"), ("55", "Essential oils and perfume materials"),
    ("56", "Fertilizers (other than those of group 272)"), ("57", "Plastics in primary forms"),
    ("58", "Plastics in non-primary forms"), ("59", "Chemical materials and products, n.e.s."),
    ("61", "Leather, leather manufactures, n.e.s."), ("62", "Rubber manufactures, n.e.s."),
    ("63", "Cork and wood manufactures (excluding furniture)"), ("64", "Paper, paperboard and articles thereof"),
    ("65", "Textile yarn, fabrics, made-up articles, n.e.s."), ("66", "Non-metallic mineral manufactures, n.e.s."),
    ("67", "Iron and steel"), ("68", "Non-ferrous metals"), ("69", "Manufactures of metals, n.e.s."),
    ("71", "Power-generating machinery and equipment"), ("72", "Machinery specialized for particular industries"),
    ("73", "Metalworking machinery"), ("74", "General industrial machinery and equipment, n.e.s."),
    ("75", "Office machines and automatic data-processing machines"),
    ("76", "Telecommunications and sound-recording and reproducing apparatus and equipment"),
    ("77", "Electrical machinery, apparatus and appliances, n.e.s."), ("78", "Road vehicles"),
    ("79", "Other transport equipment"), ("81", "Prefabricated buildings; sanitary, plumbing, heating and lighting"),
    ("82", "Furniture, and parts thereof"), ("83", "Travel goods, handbags and similar containers"),
    ("84", "Articles of apparel and clothing accessories"), ("85", "Footwear"),
    ("87", "Professional, scientific and controlling instruments and apparatus, n.e.s."),
    ("88", "Photographic apparatus, optical goods, watches and clocks"),
    ("89", "Miscellaneous manufactured articles, n.e.s."),
    ("93", "Special transactions and commodities not classified according to kind"),
    ("97", "Gold, non-monetary (excluding gold ores and concentrates)"),
]
DIV_TITLE = dict(DIVISIONS)

# export divisions with their share of their section's exports
EXP_DIV = {
    "0": {"01": 0.30, "02": 0.52, "03": 0.06, "04": 0.02, "05": 0.06, "09": 0.03, "00": 0.01},
    "1": {"11": 0.97, "12": 0.03}, "2": {"24": 0.55, "26": 0.12, "28": 0.18, "21": 0.05, "25": 0.06, "29": 0.04},
    "4": {"41": 0.80, "42": 0.20}, "5": {"51": 0.18, "54": 0.22, "55": 0.08, "56": 0.10, "57": 0.12, "59": 0.30},
    "6": {"68": 0.62, "64": 0.12, "63": 0.10, "67": 0.08, "69": 0.08},
    "7": {"72": 0.25, "74": 0.22, "77": 0.18, "78": 0.10, "79": 0.15, "76": 0.10},
    "8": {"87": 0.38, "89": 0.32, "82": 0.12, "84": 0.18}, "9": {"93": 0.55, "97": 0.45},
}
IMP_DIV = {
    "0": {"01": 0.06, "03": 0.08, "04": 0.18, "05": 0.20, "06": 0.08, "07": 0.15, "08": 0.10, "09": 0.15},
    "1": {"11": 0.80, "12": 0.20}, "2": {"22": 0.30, "27": 0.25, "28": 0.25, "29": 0.20},
    "3": {"33": 0.88, "34": 0.12}, "4": {"42": 1.00},
    "5": {"51": 0.12, "52": 0.06, "53": 0.05, "54": 0.30, "55": 0.08, "56": 0.10, "57": 0.10, "58": 0.07,
          "59": 0.12},
    "6": {"62": 0.10, "64": 0.12, "65": 0.15, "66": 0.10, "67": 0.20, "68": 0.08, "69": 0.25},
    "7": {"71": 0.08, "72": 0.14, "73": 0.03, "74": 0.13, "75": 0.10, "76": 0.12, "77": 0.12, "78": 0.24,
          "79": 0.04},
    "8": {"81": 0.08, "82": 0.10, "83": 0.04, "84": 0.22, "85": 0.07, "87": 0.12, "88": 0.05, "89": 0.32},
    "9": {"93": 0.70, "97": 0.30},
}
# the main markets of each export division and the main sources of each import division (relative weights; the
# rest of the division's trade is spread over the other countries)
EXP_MKT = {
    "01": {"CN": 30, "US": 22, "GB": 8, "JP": 8, "KR": 5, "SA": 4, "MY": 3, "DE": 3, "CA": 3},
    "02": {"CN": 28, "DZ": 9, "AU": 7, "MY": 6, "ID": 6, "VN": 5, "PH": 5, "SA": 5, "US": 4, "TH": 4, "SG": 4, "JP": 4},
    "03": {"AU": 25, "US": 20, "CN": 20, "JP": 10, "HK": 8, "KR": 5},
    "05": {"JP": 22, "CN": 18, "AU": 12, "US": 10, "TW": 8, "KR": 8, "SG": 5},
    "11": {"AU": 30, "US": 25, "GB": 15, "CN": 10, "CA": 8, "NL": 4},
    "24": {"CN": 60, "KR": 12, "IN": 10, "JP": 8, "AU": 4},
    "28": {"CN": 45, "JP": 25, "KR": 15, "AU": 6},
    "41": {"CN": 30, "AU": 20, "MY": 15, "ID": 10},
    "54": {"AU": 35, "US": 20, "CN": 12, "SG": 8, "JP": 6},
    "59": {"AU": 40, "CN": 12, "US": 10, "SG": 6, "FJ": 6},
    "68": {"JP": 35, "US": 20, "KR": 15, "CN": 12, "TW": 6, "SG": 4},
    "72": {"AU": 40, "US": 15, "CN": 8, "FJ": 5, "PG": 5},
    "74": {"AU": 45, "US": 12, "FJ": 6, "PG": 6, "NC": 4},
    "79": {"AU": 30, "US": 20, "SG": 10, "IE": 10, "FR": 8},
    "87": {"AU": 35, "US": 30, "DE": 6, "GB": 6, "CN": 5},
    "93": {"AU": 30, "US": 15, "CN": 10},
    "97": {"AU": 55, "HK": 15, "CH": 15, "SG": 10},
}
IMP_SRC = {
    "33": {"SG": 35, "KR": 25, "MY": 12, "JP": 8, "CN": 6, "IN": 5},
    "34": {"QA": 50, "AU": 30, "MY": 20},
    "78": {"JP": 45, "KR": 12, "CN": 12, "TH": 10, "DE": 8, "US": 4},
    "75": {"CN": 45, "US": 12, "TW": 10, "MY": 8, "TH": 6},
    "76": {"CN": 50, "VN": 12, "KR": 10, "US": 8},
    "84": {"CN": 55, "BD": 12, "VN": 10, "IN": 6},
    "54": {"US": 20, "DE": 15, "IE": 12, "CH": 12, "GB": 8, "AU": 8, "IN": 6},
    "67": {"CN": 35, "KR": 15, "JP": 15, "AU": 10},
}
# coal and LNG: each market's share (coal by tonnes, LNG by cargoes)
COAL_MKT = {"JP": 0.30, "IN": 0.22, "KR": 0.18, "CN": 0.14, "TW": 0.08, "TH": 0.03, "VN": 0.03, "PH": 0.02}
LNG_MKT = {"JP": 0.38, "CN": 0.22, "KR": 0.18, "TW": 0.12, "IN": 0.05, "TH": 0.05}
COND_MKT = {"SG": 0.50, "KR": 0.25, "JP": 0.15, "CN": 0.10}

# seasonal factors (original over seasonally adjusted) by section: dairy follows the milking season
SEASON = {"0": [1.18, 1.10, 1.06, 0.98, 0.88, 0.80, 0.78, 0.86, 0.96, 1.08, 1.14, 1.18]}


def season(s, m):
    mon = WD.MON[m]
    if s in SEASON:
        return SEASON[s][mon - 1]
    return 1.0 + 0.015 * np.sin(2 * np.pi * (mon - 3) / 12.0 + int(s))


def _spread(r, weights, scale):
    """Shares over every country: the named weights plus a thin spread over the rest."""
    w = {c: 0.15 * r.gamma(0.6) for c in CODES}
    for c, v in weights.items():
        w[c] = v * scale
    tot = sum(w.values())
    return {c: v / tot for c, v in w.items()}


def energy_by_market(W):
    """Shipments of coal, condensate and LNG by market and month of shipment: tonnes and $m."""
    r = K.rng("energy", "markets")
    ship_t = {k: {} for k in ("32", "33", "34")}
    ship_v = {k: {} for k in ("32", "33", "34")}
    for k, shares in (("32", COAL_MKT), ("33", COND_MKT)):
        tot_t = W.E_T[k]
        draw = {c: s * np.exp(r.normal(0.0, 0.09, NM)) for c, s in shares.items()}
        norm = sum(draw.values())
        for c in shares:
            ship_t[k][c] = tot_t * draw[c] / norm
            ship_v[k][c] = ship_t[k][c] * W.E_P[k] / 1e6
    mk = list(LNG_MKT)
    p = np.array([LNG_MKT[c] for c in mk])
    for c in mk:
        ship_t["34"][c] = np.zeros(NM)
    for m in range(NM):
        n = int(W.LNG_CARGOES[m])
        dest = r.choice(len(mk), size=n, p=p)
        for i, d in enumerate(dest):
            ship_t["34"][mk[d]][m] += W.LNG_SIZES[m][i]
    for c in mk:
        ship_v["34"][c] = ship_t["34"][c] * W.E_P["34"] / 1e6
    W.SHIP_T, W.SHIP_V = ship_t, ship_v


tbs_month = WD.tbs_month


def bulk(W):
    """The bulk download's rows: {(month, flow, country, division): [value $000, quantity, unit]}, original terms.
    Each section's month adds up to TBS's original-terms total for it; coal, condensate and LNG follow TBS's
    recording of periodic entries (tbs_month)."""
    months = range(MI[FIRST], MI[LAST_PULL] + 1)
    rows = {}
    W.ORIG_X, W.ORIG_M = {}, {}
    for flow, divs, mkts, out in (("X", EXP_DIV, EXP_MKT, W.ORIG_X), ("M", IMP_DIV, IMP_SRC, W.ORIG_M)):
        for s, dshare in divs.items():
            if flow == "X" and s == "3":
                continue
            val = (W.PORTAL_VX if flow == "X" else W.PORTAL_VM)[s]      # as TBS's tables stood on 24 June
            dr = K.rng("bulk", flow, s)
            dnoise = {d: np.exp(dr.normal(0.0, 0.035, NM)) for d in dshare}
            setup = {}
            for d in dshare:
                rr = K.rng("bulk", flow, d)
                wts = _spread(rr, mkts.get(d, {}), 6.0)
                keep = sorted(wts, key=lambda c: (-wts[c], c))[:int(rr.integers(10, 27))]
                if flow == "M" or rr.uniform() < 0.5:
                    keep.append("QU")
                    wts["QU"] = 0.004
                setup[d] = (keep, wts, {c: np.exp(rr.normal(0.0, 0.10, NM)) for c in keep})
            series = np.zeros(NM)
            for m in months:
                total = int(round(val[m] * season(s, m) * 1000.0))     # $000, original terms
                dz = sum(dshare[d] * dnoise[d][m] for d in dshare)
                cells = []
                for d in dshare:
                    keep, wts, noise = setup[d]
                    v_div = total * dshare[d] * dnoise[d][m] / dz
                    z = sum(wts[c] * noise[c][m] for c in keep)
                    for c in keep:
                        cells.append([d, c, v_div * wts[c] * noise[c][m] / z])
                ints = [int(round(v)) for _, _, v in cells]
                big = max(range(len(cells)), key=lambda i: cells[i][2])
                ints[big] += total - sum(ints)
                for (d, c, _), v in zip(cells, ints):
                    if v >= 1:
                        rows[(WD.MONTHS[m], flow, c, d)] = [v, None, None]
                series[m] = total / 1000.0
            out[s] = series
    for k in ("32", "33", "34"):
        for c in W.SHIP_V[k]:
            for m in months:
                v = tbs_month(W.SHIP_V[k][c], m)
                q = tbs_month(W.SHIP_T[k][c], m)
                if v <= 0:
                    continue
                unit = "kl" if k == "33" else "t"
                qq = q * (1.0 / 0.85 if k == "33" else 1.0)          # condensate in kilolitres
                rows[(WD.MONTHS[m], "X", c, k)] = [int(round(v * 1000.0)), int(round(qq)), unit]
    W.BULK = rows
    return rows


def port_loadings(W):
    """The ports' monthly bulk loadings by port and cargo, tonnes, by month of loading."""
    r = K.rng("ports")
    out = {}
    for m in range(MI[FIRST] - 1, MI["2026-06"] + 1):
        coal = W.E_T["32"][m]
        a = 0.62 + r.normal(0.0, 0.02)
        out[(WD.MONTHS[m], "Coal", "Port Ardley")] = coal * a * (1 + r.normal(0, 0.003))
        out[(WD.MONTHS[m], "Coal", "Saltpan Bay")] = coal * (1 - a) * (1 + r.normal(0, 0.003))
        out[(WD.MONTHS[m], "LNG", "Cape Mallory")] = W.E_T["34"][m] * (1 + r.normal(0, 0.002))
        out[(WD.MONTHS[m], "Condensate", "Cape Mallory")] = W.E_T["33"][m] * (1 + r.normal(0, 0.004))
    W.PORTS = out
    return out
