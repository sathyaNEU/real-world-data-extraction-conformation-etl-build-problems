"""The mosquitoes and the virus, as they are: how many females of each species each trap would catch on each night,
and how many of them carry West Nile virus. Everything recorded later (catches, pools, results) is drawn from these.

A CO2-baited light trap draws host-seeking females, most of which have never fed; a gravid trap draws females looking
for water to lay eggs in, every one of which has taken at least one blood meal and so has had the chance to pick up the
virus from a bird. Infection in a gravid trap's catch therefore runs several times the infection in a CO2 trap's."""
import datetime as dt
import math

import numpy as np

import world as W

YEARS = {2024: range(22, 38), 2025: range(22, 38), 2026: range(22, 33)}

# week-32 2026 levels, CO2 traps: females per trap-night (tarsalis, pipiens)
CO2_LEVEL = {
    "Westbrook": (100, 4), "South Prairie": (150, 12), "North Bottoms": (240, 8), "Old Town": (25, 125),
    "Riverside South": (30, 128), "Maple Ridge": (22, 6), "Coulee Hills": (40, 5), "Airport East": (60, 10),
}
# gravid traps, females per trap-night (tarsalis, pipiens)
GRAVID_LEVEL = {"Old Town": (10, 340), "Riverside South": (8, 160)}
# week-32 2026 infection per 1,000 host-seeking females (tarsalis, pipiens)
CO2_INF = {
    "Westbrook": (23.0, 12.0), "South Prairie": (11.5, 7.0), "North Bottoms": (4.2, 3.0), "Old Town": (7.0, 8.0),
    "Riverside South": (7.0, 7.0), "Maple Ridge": (33.0, 12.0), "Coulee Hills": (3.0, 2.0), "Airport East": (6.0, 4.0),
}
# infection among gravid-trap females against host-seeking females (older, every one fed)
GRAVID_RATIO = {"Old Town": (2.9, 4.6), "Riverside South": (2.1, 3.9)}
# the week (2026 MMWR) by which infection reached half its week-32 level, and how fast it climbed
ONSET = {"Westbrook": (29.0, 1.1), "South Prairie": (28.0, 1.2), "North Bottoms": (28.5, 1.0), "Old Town": (29.5, 1.0),
         "Riverside South": (29.5, 1.0), "Maple Ridge": (27.5, 1.3), "Coulee Hills": (26.0, 1.2), "Airport East": (28.5, 1.0)}
OTHER_SPECIES = {"AEVE": 55.0, "AEDO": 6.0, "CUIN": 4.0, "ANEA": 2.5, "AETR": 7.0}
KDISP = 2.4            # night-to-night dispersion of a trap's catch (negative binomial)


def season(sp, date):
    """Seasonal abundance against its week-32 level: Culex tarsalis climbs to a mid-August peak, Culex pipiens later."""
    doy = date.timetuple().tm_yday
    if sp == "CXTA":
        peak, width = 232.0, 33.0
    elif sp == "CXPI":
        peak, width = 238.0, 30.0
    else:
        peak, width = 190.0, 40.0
    ref = 227.0                                   # 15 August
    return math.exp(-0.5 * ((doy - peak) / width) ** 2) / math.exp(-0.5 * ((ref - peak) / width) ** 2)


def year_factor(year, zone):
    g = W.rng("year", year, zone)
    return {2024: 0.72, 2025: 0.86, 2026: 1.0}[year] * (1.0 if year == 2026 else g.uniform(0.8, 1.2))


def infection(zone, sp, date, year=2026):
    """Infection per 1,000 host-seeking females on a night."""
    lvl = CO2_INF[zone][0 if sp == "CXTA" else 1]
    wk = W.mmwr_week(date) + (date.weekday() + 1) % 7 / 7.0
    mid, rate = ONSET[zone]
    if year != 2026:
        g = W.rng("inf-year", year, zone)
        lvl = lvl * g.uniform(0.25, 0.6)
        mid = mid + g.uniform(0.5, 2.5)
    f = 1.0 / (1.0 + math.exp(-rate * (wk - mid)))
    f32 = 1.0 / (1.0 + math.exp(-rate * (32.25 - mid)))
    val = lvl * f / f32
    if zone == "Coulee Hills" and year == 2026:
        # the July focus in the coulees: up to about 19 per 1,000 in mid-July, back near 3 by mid-August
        val = 3.0 + 16.0 * math.exp(-0.5 * ((wk - 28.3) / 1.4) ** 2)
        if sp == "CXPI":
            val *= 0.6
    return val


def site_factor(site_id):
    g = W.rng("site-factor", site_id)
    return float(np.exp(g.normal(0.0, 0.28)))


def expected_catch(site, sp, date, year):
    z = site["zone"]
    if site["trap_type"] == "gravid":
        lv = GRAVID_LEVEL[z][0 if sp == "CXTA" else 1] if sp in W.VECTORS else 0.35
    else:
        if sp in W.VECTORS:
            lv = CO2_LEVEL[z][0 if sp == "CXTA" else 1]
        else:
            lv = OTHER_SPECIES[sp] * (1.6 if z in ("North Bottoms", "Maple Ridge", "Coulee Hills") else 0.8)
    return lv * season(sp, date) * year_factor(year, z) * site["factor"]


def draw_catch(g, mean):
    if mean <= 0:
        return 0
    p = KDISP / (KDISP + mean)
    return int(g.negative_binomial(KDISP, p))
