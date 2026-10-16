"""Ask B's world: initial claims by claims week, region, industry division of the last employer and claim type, as the
board's open-data cube records them from the claims week of 1 January 2023.

The Statistics Office's 2023 revision of the Standard Industrial Classification re-blocked the division codes: several
2006 divisions moved to new codes and their old numbers were given to divisions of other sections, as the NACE
revision did. The board rebuilt its open-data cube on the 2023 classification from the claims week of 4 January 2026.
The weeks before keep the 2006 division codes and the cube's old week label (the claims week's last day, a Saturday);
from the rebuild the cube labels each week by its first day, the Sunday, as the claims system does. Transitional claims
(a claimant whose benefit year has ended filing to start the next) are in the cube under their own claim type and are
not initial claims. Nothing here touches the national or regional counts: each week and region's new and additional
claims are the world's (world.py), split across divisions."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

SWITCH_SUNDAY = K.SIC_SWITCH_SUNDAY      # 4 January 2026
CUBE_FIRST_SUNDAY = dt.date(2023, 1, 1)

GROUPS = ["Agriculture, forestry and fishing", "Mining, energy and utilities", "Manufacturing", "Construction",
          "Wholesale, transport and storage", "Retail trade", "Accommodation and food services",
          "Information and communication", "Financial, insurance and property services",
          "Professional, scientific and technical services", "Administrative and support services",
          "Public administration and safety", "Education and training",
          "Health care, social assistance and other services"]
G = {k + 1: g for k, g in enumerate(GROUPS)}

# SIC 2023 divisions: code -> (title, group number, weight in claims)
SIC2023 = {
    "01": ("Crop and animal production", 1, 2.6), "02": ("Forestry and logging", 1, 0.9),
    "03": ("Fishing and aquaculture", 1, 0.8),
    "05": ("Coal mining", 2, 0.25), "07": ("Metal ore mining", 2, 0.2), "08": ("Other mining and quarrying", 2, 0.35),
    "09": ("Mining support service activities", 2, 0.3), "35": ("Electricity, gas and steam supply", 2, 0.45),
    "36": ("Water collection, treatment and supply", 2, 0.2), "38": ("Waste collection, treatment and disposal", 2, 0.55),
    "10": ("Manufacture of food products", 3, 3.4), "11": ("Manufacture of beverages", 3, 0.6),
    "16": ("Manufacture of wood products", 3, 1.2), "17": ("Manufacture of paper products", 3, 0.4),
    "18": ("Printing and reproduction of recorded media", 3, 0.5), "20": ("Manufacture of chemicals", 3, 0.45),
    "23": ("Manufacture of non-metallic mineral products", 3, 0.6), "24": ("Manufacture of basic metals", 3, 0.4),
    "25": ("Manufacture of fabricated metal products", 3, 1.3), "28": ("Manufacture of machinery and equipment", 3, 0.9),
    "29": ("Manufacture of motor vehicles and trailers", 3, 0.35), "31": ("Manufacture of furniture", 3, 0.6),
    "33": ("Repair and installation of machinery", 3, 0.7),
    "41": ("Construction of buildings", 4, 4.1), "42": ("Civil engineering", 4, 1.9),
    "43": ("Specialised construction activities", 4, 5.0),
    "46": ("Wholesale trade", 5, 3.4), "49": ("Land transport", 5, 2.6), "50": ("Water transport", 5, 0.4),
    "51": ("Air transport", 5, 0.5), "52": ("Warehousing and support activities for transport", 5, 1.6),
    "53": ("Postal and courier activities", 5, 0.9),
    "45": ("Motor vehicle trade and repair", 6, 1.7), "47": ("Retail trade", 6, 8.6),
    "55": ("Accommodation", 7, 3.0), "56": ("Food and beverage service activities", 7, 6.1),
    "58": ("Publishing activities", 8, 0.4), "59": ("Film, video and sound recording", 8, 0.4),
    "60": ("Broadcasting", 8, 0.25), "61": ("Telecommunications", 8, 0.55),
    "62": ("Computer programming and consultancy", 8, 1.1), "63": ("Information service activities", 8, 0.3),
    "64": ("Financial service activities", 9, 0.9), "65": ("Insurance", 9, 0.5),
    "66": ("Activities auxiliary to financial services", 9, 0.35), "68": ("Real estate activities", 9, 1.2),
    "69": ("Legal and accounting activities", 10, 0.9), "70": ("Head offices and management consultancy", 10, 1.0),
    "71": ("Architecture and engineering activities", 10, 1.1), "72": ("Scientific research and development", 10, 0.3),
    "73": ("Advertising and market research", 10, 0.5), "74": ("Other professional and technical activities", 10, 0.45),
    "75": ("Veterinary activities", 10, 0.2),
    "77": ("Rental and leasing activities", 11, 0.6), "78": ("Employment activities", 11, 2.4),
    "79": ("Travel agencies and tour operators", 11, 0.5), "80": ("Security and investigation", 11, 0.7),
    "81": ("Services to buildings and landscape", 11, 1.6), "82": ("Office administration and business support", 11, 1.0),
    "83": ("Public order, safety and regulatory services", 12, 0.6),
    "84": ("Public administration and defence", 12, 1.4),
    "85": ("Education", 13, 2.9),
    "86": ("Human health activities", 14, 2.2), "87": ("Residential care activities", 14, 1.4),
    "88": ("Social work activities", 14, 1.1), "90": ("Creative, arts and entertainment activities", 14, 0.5),
    "93": ("Sports and recreation activities", 14, 0.9), "95": ("Repair of personal and household goods", 14, 0.35),
    "96": ("Other personal service activities", 14, 1.1),
}

# SIC 2006 divisions: code -> (title, [2023 successor codes], [shares]); every successor in one group
SIC2006 = {
    "01": ("Agriculture, hunting and related services", ["01"], [1.0]),
    "03": ("Forestry and logging", ["02"], [1.0]),
    "05": ("Fishing and fish farming", ["03"], [1.0]),
    "07": ("Mining of coal and lignite", ["05"], [1.0]),
    "09": ("Mining of metal ores", ["07"], [1.0]),
    "08": ("Other mining, quarrying and mining services", ["08", "09"], [0.54, 0.46]),
    "35": ("Electricity, gas and water supply", ["35", "36"], [0.69, 0.31]),
    "90": ("Sewage and refuse disposal", ["38"], [1.0]),
    "10": ("Manufacture of food products and beverages", ["10", "11"], [0.85, 0.15]),
    "02": ("Manufacture of wood and paper products", ["16", "17"], [0.75, 0.25]),
    "18": ("Publishing, printing and reproduction of recorded media", ["18"], [1.0]),
    "20": ("Manufacture of chemicals and chemical products", ["20"], [1.0]),
    "23": ("Manufacture of other non-metallic mineral products", ["23"], [1.0]),
    "24": ("Manufacture of basic metals", ["24"], [1.0]),
    "25": ("Manufacture of fabricated metal products", ["25"], [1.0]),
    "28": ("Manufacture of machinery and equipment, repair and installation", ["28", "33"], [0.56, 0.44]),
    "29": ("Manufacture of motor vehicles, trailers and parts", ["29"], [1.0]),
    "31": ("Manufacture of furniture and other manufacturing", ["31"], [1.0]),
    "41": ("Building construction", ["41"], [1.0]),
    "49": ("Civil engineering construction", ["42"], [1.0]),
    "43": ("Building completion and specialised trades", ["43"], [1.0]),
    "46": ("Wholesale trade", ["46"], [1.0]),
    "52": ("Land transport", ["49"], [1.0]),
    "50": ("Water and air transport", ["50", "51"], [0.45, 0.55]),
    "53": ("Supporting and auxiliary transport activities", ["52"], [1.0]),
    "64": ("Post and courier activities", ["53"], [1.0]),
    "77": ("Sale, maintenance and repair of motor vehicles", ["45"], [1.0]),
    "47": ("Retail trade", ["47"], [1.0]),
    "55": ("Hotels and motels", ["55"], [1.0]),
    "93": ("Other short-term accommodation", ["55"], [1.0]),
    "56": ("Restaurants, cafes, bars and catering", ["56"], [1.0]),
    "58": ("Publishing, film, broadcasting and telecommunications", ["58", "59", "60", "61"], [0.25, 0.25, 0.15, 0.35]),
    "62": ("Computer and related activities", ["62"], [1.0]),
    "72": ("Data processing and information services", ["63"], [1.0]),
    "65": ("Financial intermediation and insurance", ["64", "65"], [0.64, 0.36]),
    "73": ("Activities auxiliary to financial intermediation", ["66"], [1.0]),
    "68": ("Real estate activities", ["68"], [1.0]),
    "70": ("Legal, accounting and management services", ["69", "70"], [0.47, 0.53]),
    "71": ("Architectural, engineering and technical services", ["71", "72"], [0.79, 0.21]),
    "74": ("Advertising, research and other professional services", ["73", "74"], [0.53, 0.47]),
    "83": ("Veterinary activities", ["75"], [1.0]),
    "80": ("Renting of machinery, equipment and goods", ["77"], [1.0]),
    "78": ("Labour recruitment and provision of personnel", ["78"], [1.0]),
    "79": ("Travel agencies and tour operators", ["79"], [1.0]),
    "61": ("Investigation and security activities", ["80"], [1.0]),
    "81": ("Building cleaning and landscaping", ["81"], [1.0]),
    "82": ("Office administration and business support", ["82"], [1.0]),
    "84": ("Public administration and defence", ["84", "83"], [0.7, 0.3]),
    "85": ("Primary and secondary education", ["85"], [1.0]),
    "87": ("Tertiary and adult education", ["85"], [1.0]),
    "86": ("Health and social work", ["86", "87", "88"], [0.47, 0.30, 0.23]),
    "95": ("Recreational, cultural and sporting activities", ["90", "93"], [0.36, 0.64]),
    "96": ("Other personal service activities", ["96"], [1.0]),
    "45": ("Repair of personal and household goods", ["95"], [1.0]),
}
# where two 2006 divisions fed one 2023 division, the share of its claims each carried before the rebuild
SOURCE_SHARE = {"55": {"55": 0.8, "93": 0.2}, "85": {"85": 0.8, "87": 0.2}}

# the board's industry groups of the 2023 divisions (the code list)
GROUP_OF_2023 = {c: v[1] for c, v in SIC2023.items()}
TO2006 = {}
for c06, (t, succ, sh) in SIC2006.items():
    for c23, s in zip(succ, sh):
        TO2006.setdefault(c23, []).append((c06, SOURCE_SHARE.get(c23, {}).get(c06, 1.0)))

# the 2026 layoffs and the regions they lean on; the fiscal year's end in the public and education divisions
SURGE_DIV = {"41": 1.62, "42": 1.18, "43": 1.66, "55": 1.55, "56": 1.22, "79": 1.25, "78": 1.12}
SURGE_REG = {"Western": 1.35, "Coastal": 1.4, "Island": 1.3, "Midlands": 1.15}
YEAR_END_DIV = {"84": 2.4, "83": 1.6, "85": 2.9, "72": 1.8, "86": 1.4, "88": 1.5}
# a region's lean towards each group (tourism and primary industry in the outer regions, offices in the Capital)
REGION_TILT = {
    "Northern": {1: 1.5, 3: 1.2, 7: 1.0, 9: 0.8, 10: 0.8},
    "Capital": {1: 0.3, 2: 0.6, 8: 1.9, 9: 1.8, 10: 1.7, 11: 1.3, 12: 1.9, 13: 1.1},
    "Eastern": {1: 1.6, 3: 1.3, 5: 1.1, 12: 0.9},
    "Midlands": {3: 1.5, 4: 1.2, 5: 1.4, 2: 1.3},
    "Western": {1: 1.4, 2: 1.4, 4: 1.25, 7: 1.4, 8: 0.6},
    "Southern": {1: 1.8, 2: 1.5, 3: 1.2, 9: 0.7},
    "Coastal": {7: 1.9, 4: 1.2, 1: 1.2, 6: 1.1, 8: 0.5, 9: 0.6},
    "Island": {7: 2.1, 1: 1.6, 5: 1.3, 8: 0.4, 10: 0.6},
}
T_SHARE = 0.026   # transitional claims, as a share of a week's new claims


def check_tables():
    """The classification's structure the ask depends on."""
    for c06, (t, succ, sh) in SIC2006.items():
        assert c06 in SIC2023, "every 2006 code is a 2023 code: none goes unmatched (%s)" % c06
        assert len({GROUP_OF_2023[c] for c in succ}) == 1, "a 2006 division maps into one group (%s)" % c06
        assert abs(sum(sh) - 1) < 1e-9
    assert sorted(TO2006) == sorted(SIC2023), "every 2023 division has a 2006 source"
    reused = [c for c in SIC2006 if GROUP_OF_2023[c] != GROUP_OF_2023[SIC2006[c][1][0]]]
    groups_touched = set()
    for c in reused:
        groups_touched.add(GROUP_OF_2023[c])
        groups_touched.add(GROUP_OF_2023[SIC2006[c][1][0]])
    new_codes = [c for c in SIC2023 if c not in SIC2006]
    return dict(reused=reused, groups_touched=sorted(groups_touched), new_codes=new_codes)


def _changes(W):
    tq = truth_q3(W)
    return {k: (tq[2026][k] / tq[2025][k] - 1.0) * 100.0 for k in G}, tq


def settle(W, lo=0.22, hi=0.42):
    """Keep every group's third-quarter change clear of its one-decimal rounding edge: where a change sits within a
    fifth of a bin of an edge, move a few new claims between two divisions of different groups inside one claims week
    and region of July to September 2026 (the week and region's totals, and so every national and regional count, are
    unchanged). The group receiving or giving them is the largest, Retail trade, whose change one claim barely moves;
    its own clearance is settled last."""
    g = K.rng("industry-settle")
    weeks26 = [s for s in W["weeks"] if s.year == 2026 and 7 <= s.month <= 9]
    order = [k for k in G if k != 6] + [6]
    for k in order:
        for _ in range(60):
            chg, tq = _changes(W)
            q = chg[k] * 10.0
            d = abs(q - math.floor(q) - 0.5)            # distance from the rounding edge, in bins
            if lo <= 0.5 - d <= 0.5 and d >= 0.5 - hi:
                pass
            e = abs((q % 1.0) - 0.5)
            if e >= lo:
                break
            # move towards the nearer side away from the edge by about a third of a bin
            target = (math.floor(q) + (0.5 - 0.33 if (q % 1.0) >= 0.5 else 0.5 + 0.33)) / 10.0
            target = (math.floor(q) + 0.17) / 10.0 if (q % 1.0) >= 0.5 else (math.floor(q) + 0.83) / 10.0
            need = int(round((target - chg[k]) / 100.0 * tq[2025][k]))
            if need == 0:
                need = 1 if target > chg[k] else -1
            give, take = (6, k) if need > 0 else (k, 6)
            if k == 6:
                give, take = (14, 6) if need > 0 else (6, 14)
            cnt = abs(need)
            s = weeks26[int(g.integers(len(weeks26)))]
            r = K.REGIONS[int(g.integers(8))]
            src_c = [c for c in W["codes"] if GROUP_OF_2023[c] == give and W["cells"][(s, r, c)][0] >= cnt]
            dst_c = [c for c in W["codes"] if GROUP_OF_2023[c] == take]
            if not src_c:
                continue
            cs, cd = src_c[int(g.integers(len(src_c)))], dst_c[int(g.integers(len(dst_c)))]
            n0, a0, t0 = W["cells"][(s, r, cs)]
            n1, a1, t1 = W["cells"][(s, r, cd)]
            W["cells"][(s, r, cs)] = (n0 - cnt, a0, t0)
            W["cells"][(s, r, cd)] = (n1 + cnt, a1, t1)
    return _changes(W)[0]


def cube_label(sun):
    """The cube's week label: the Saturday before the rebuild, the Sunday from it."""
    return sun + dt.timedelta(days=6) if sun < SWITCH_SUNDAY else sun


def simulate(T):
    """Split each claims week and region's new and additional claims across the 2023 divisions; the transitional
    claims beside them. Returns the clean truth, by 2023 division."""
    g = K.rng("industry")
    codes = sorted(SIC2023)
    base = np.array([SIC2023[c][2] for c in codes])
    weeks = [s for s in T.sundays if CUBE_FIRST_SUNDAY <= s <= K.ASOF_LAST_SUNDAY]
    # a slowly drifting national mix
    drift = {c: np.cumsum(g.normal(0, 0.012, len(weeks))) for c in codes}
    out = {}
    for wi, s in enumerate(weeks):
        i = T.idx[s]
        surge = 0.0
        if s >= dt.date(2026, 5, 24):
            surge = min(1.0, (s - dt.date(2026, 5, 24)).days / 84.0)
        ye = s.month == 6 and (s + dt.timedelta(days=7)).month == 7
        doy = (s + dt.timedelta(days=3)).timetuple().tm_yday
        winter = math.cos(2 * math.pi * (doy - 196) / 365.25)
        for r in K.REGIONS:
            w = base.copy()
            for k, c in enumerate(codes):
                grp = GROUP_OF_2023[c]
                f = REGION_TILT[r].get(grp, 1.0) * math.exp(drift[c][wi] - drift[c][-1] * 0.0)
                if grp in (1, 7):
                    f *= math.exp(0.10 * (-winter if grp == 1 else winter))
                if grp == 4:
                    f *= math.exp(0.06 * winter)
                if surge and c in SURGE_DIV:
                    f *= 1.0 + (SURGE_DIV[c] - 1.0) * surge * SURGE_REG.get(r, 0.85)
                if ye and c in YEAR_END_DIV:
                    f *= YEAR_END_DIV[c]
                w[k] *= f
            p = w / w.sum()
            # the cube is refreshed with each Thursday release: its latest week is at the advance count
            new_ = T.adv_new[r][i] if s == K.ASOF_LAST_SUNDAY else T.new[r][i]
            add_ = T.adv_add[r][i] if s == K.ASOF_LAST_SUNDAY else T.additional[r][i]
            nn = g.multinomial(int(new_), p)
            na = g.multinomial(int(add_), p)
            nt = g.multinomial(int(g.poisson(T_SHARE * new_)), p)
            for k, c in enumerate(codes):
                out[(s, r, c)] = (int(nn[k]), int(na[k]), int(nt[k]))
    W = dict(weeks=weeks, codes=codes, cells=out)
    settle(W)
    return W


def cube_rows(W):
    """The shipped cube: one row per week, region, division and claim type with claims, zeros left out. Before the
    rebuild a 2023 division's claims are coded to its 2006 source division (the split shares where a 2023 division
    came from two)."""
    g = K.rng("industry-2006")
    rows = []
    for s in W["weeks"]:
        lab = cube_label(s).isoformat()
        for r in K.REGIONS:
            if s >= SWITCH_SUNDAY:
                agg = {}
                for c in W["codes"]:
                    agg[c] = W["cells"][(s, r, c)]
            else:
                agg = {}
                for c in W["codes"]:
                    n, a, t = W["cells"][(s, r, c)]
                    src = TO2006[c]
                    if len(src) == 1:
                        parts = [(src[0][0], n, a, t)]
                    else:
                        sh = np.array([x[1] for x in src])
                        sh = sh / sh.sum()
                        nn, na, nt = g.multinomial(n, sh), g.multinomial(a, sh), g.multinomial(t, sh)
                        parts = [(src[k][0], int(nn[k]), int(na[k]), int(nt[k])) for k in range(len(src))]
                    for c06, x, y, z in parts:
                        o = agg.get(c06, (0, 0, 0))
                        agg[c06] = (o[0] + x, o[1] + y, o[2] + z)
            for c in sorted(agg):
                n, a, t = agg[c]
                for ct, v in (("N", n), ("A", a), ("T", t)):
                    if v:
                        rows.append(dict(week=lab, region=r, division=c, claim_type=ct, claims=v))
    return rows


def truth_q3(W):
    """Initial claims (new and additional) by group in the claims weeks of July to September 2025 and 2026."""
    out = {}
    for y in (2025, 2026):
        tot = {k: 0 for k in G}
        for s in W["weeks"]:
            if s.year == y and 7 <= s.month <= 9:
                for r in K.REGIONS:
                    for c in W["codes"]:
                        n, a, t = W["cells"][(s, r, c)]
                        tot[GROUP_OF_2023[c]] += n + a
        out[y] = tot
    return out


def ask_b(rows, label="switch", codes="concordance", transitional=False):
    """The change in initial claims by group from July to September 2025 to July to September 2026, from the cube's
    rows. label 'switch' reads each week's Sunday from its label (the label minus six days before the rebuild, the
    label itself from it); 'saturday' and 'sunday' read every label one way; 'month' takes the label's own month.
    codes 'concordance' maps the 2006 codes before the rebuild through the concordance; 'current' reads every code
    on the current list."""
    tot = {2025: {k: 0 for k in G}, 2026: {k: 0 for k in G}}
    for r in rows:
        d = dt.date.fromisoformat(r["week"])
        if label == "switch":
            sun = d - dt.timedelta(days=6) if d.weekday() == 5 else d
        elif label == "saturday":
            sun = d - dt.timedelta(days=6)
        elif label == "sunday":
            sun = d
        else:
            sun = None
        mon = (sun.year, sun.month) if sun else (d.year, d.month)
        if mon[0] not in (2025, 2026) or not 7 <= mon[1] <= 9:
            continue
        if r["claim_type"] == "T" and not transitional:
            continue
        before = (d.weekday() == 5) if label == "switch" else (d < dt.date(2026, 1, 4))
        c = r["division"]
        if codes == "concordance" and before:
            grp = GROUP_OF_2023[SIC2006[c][1][0]]
        else:
            grp = GROUP_OF_2023[c]
        tot[mon[0]][grp] += int(r["claims"])
    chg = {k: (tot[2026][k] / tot[2025][k] - 1.0) * 100.0 for k in G}
    return chg, tot


if __name__ == "__main__":
    import world as WD
    info = check_tables()
    print("reused 2006 codes", info["reused"], "groups touched", len(info["groups_touched"]), "new 2023 codes", info["new_codes"])
    T = WD.simulate()
    W = simulate(T)
    rows = cube_rows(W)
    print("cube rows", len(rows))
    tq = truth_q3(W)
    gold, tot = ask_b([{k: str(v) for k, v in r.items()} for r in rows])
    for k in G:
        tchg = (tq[2026][k] / tq[2025][k] - 1) * 100
        print("%-52s %7d %7d  %6.2f  truth %6.2f" % (G[k], tot[2025][k], tot[2026][k], gold[k], tchg))
