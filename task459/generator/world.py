"""The fixed world of task459: Calder County Public Utility District No. 1, a public power utility in Washington,
ran a 2026 request for offers for baseload capacity, 2027 to 2036, under ten-year unit-contingent agreements. Ten
gas-fired combined cycles in the Pacific Northwest were offered. The state's emissions performance standard bars a
utility from a long-term baseload commitment with a plant that emits more than 925 pounds of carbon dioxide per net
megawatt-hour, and the district's procurement procedure determines each plant's rate from its own 2024 and 2025
monitoring and meter records.

A plant's carbon dioxide per net megawatt-hour depends on how it is run: a combined cycle burns more fuel per
megawatt-hour at part load and in the hours after a start, and its duct burners add output at a far higher heat rate
than the turbines. The commitment holds each plant at its contract capacity in every hour."""
import datetime as dt

SEED = 4591207

DISTRICT = "Calder County Public Utility District No. 1"
DISTRICT_SHORT = "Calder PUD"
RFO = "2026 Baseload Request for Offers"
PROCEDURE = "Resource Procurement Procedure RP-7"
STANDARD = 925.0                      # pounds of CO2 per net MWh
NEED = 1000.0                         # MW the district fills, each offer taken whole

PEOPLE = {
    "gm": ("Victor Carr", "General Manager"),
    "planning": ("Adrian Dunn", "Manager, Resource Planning"),
    "compliance": ("Julie Jackson", "Environmental Compliance Specialist"),
}

FIRST_DAY = dt.date(2024, 1, 1)       # the records: 2024 and 2025, local standard time (UTC-8)
LAST_DAY = dt.date(2025, 12, 31)
NHOURS = ((LAST_DAY - FIRST_DAY).days + 1) * 24
H2025 = (dt.date(2025, 1, 1) - FIRST_DAY).days * 24       # index of the first 2025 hour
OFFERS_DUE = dt.date(2026, 9, 30)
PACK_DATE = dt.date(2026, 11, 4)      # the evaluation folder as the district shared it
BOARD_DATE = dt.date(2026, 11, 17)
TERM = (dt.date(2027, 1, 1), dt.date(2036, 12, 31))

CO2_PER_MMBTU = 0.05938               # short tons per mmBtu, natural gas (40 CFR 75 Appendix G, Fc 1,040 scf/mmBtu)

# Each offered plant. Configuration: '2x1' (two combustion turbines with heat recovery steam generators, one steam
# turbine), '1x1', or '1x1ss' (single-shaft: turbine and steam turbine on one generator).
#   pmax   gross MW without duct firing at 59 F       hr     gross Btu/kWh at full unfired load, 59 F
#   pl     part-load coefficient                       db     duct burner MW (0 none)        dbhr   duct firing Btu/kWh
#   zone   climate (east of the Cascades or west)       disp   dispatch style                 bypass  HRSG bypass
#   offer  'unfired' (capability at 100 F without duct firing) or 'fired' (with the duct burners at full)
PLANTS = [
    dict(key="SB", eia="Sorrel Butte Energy Center", epa="Sorrel Butte Energy Ctr", trade="Sorrel Butte CCGT",
         seller="Sorrel Butte Power LLC", code=61207, state="WA", county="Benton", zone="east", config="2x1", year=2006,
         pmax=640, hr=6950, pl=0.80, db=0, dbhr=0, f0=0.012, f1=0.021, disp="cycle_daily", bypass="N", offer="unfired",
         sf=1.2, price=11.80),
    dict(key="KC", eia="Kessling Creek Generating Station", epa="Kessling Creek", trade="Kessling Creek Generating Station",
         seller="Kessling Creek Energy LLC", code=61842, state="WA", county="Cowlitz", zone="west", config="1x1ss",
         year=2008, pmax=300, hr=6850, pl=0.95, db=0, dbhr=0, f0=0.013, f1=0.022, disp="cycle_daily", bypass="N",
         offer="unfired", price=12.10),
    dict(key="TL", eia="Tamarack Landing Power Project", epa="Tamarack Landing CCCT", trade="Tamarack Landing",
         seller="Tamarack Landing Generation LP", code=62115, state="OR", county="Umatilla", zone="east", config="2x1",
         year=1999, pmax=560, hr=7180, pl=0.52, db=170, dbhr=10950, f0=0.011, f1=0.022, disp="base", bypass="Y",
         offer="fired", price=11.40),
    dict(key="OF", eia="Ochre Flat Energy Facility", epa="Ochre Flat Energy Facility", trade="Ochre Flat 7HA",
         seller="Ochre Flat Power Partners", code=62930, state="WA", county="Grays Harbor", zone="west", config="1x1",
         year=2021, pmax=380, hr=6290, pl=0.50, db=0, dbhr=0, f0=0.010, f1=0.020, disp="base", bypass="N",
         offer="unfired", price=16.20),
    dict(key="PM", eia="Brenmoor Mill Generating Plant", epa="Brenmoor Mill", trade="Brenmoor Mill Combined Cycle",
         seller="Brenmoor Mill Energy LLC", code=63304, state="OR", county="Columbia", zone="west", config="1x1",
         year=1994, pmax=210, hr=8340, pl=0.55, db=0, dbhr=0, f0=0.015, f1=0.025, disp="cycle_seasonal", bypass="Y",
         offer="unfired", price=9.80),
    dict(key="JD", eia="Juniper Draw Power Station", epa="Juniper Draw Power Station", trade="Juniper Draw",
         seller="Juniper Draw Energy LLC", code=63711, state="WA", county="Franklin", zone="east", config="2x1",
         year=2004, pmax=600, hr=7080, pl=0.52, db=140, dbhr=10800, f0=0.011, f1=0.021, disp="base", bypass="N",
         offer="unfired", price=11.55),
    dict(key="LH", eia="Lindgren Hill Generating Station", epa="Lindgren Hill", trade="Lindgren Hill Generating Station",
         seller="Lindgren Hill Power LLC", code=64058, state="WA", county="Lewis", zone="west", config="1x1", year=2003,
         pmax=320, hr=6900, pl=0.58, db=0, dbhr=0, f0=0.013, f1=0.022, disp="mid", bypass="Y", offer="unfired",
         price=13.10),
    dict(key="AG", eia="Ashby Gulch Energy Center", epa="Ashby Gulch Energy Center", trade="Ashby Gulch CC",
         seller="Ashby Gulch Generation LLC", code=64492, state="OR", county="Morrow", zone="east", config="1x1",
         year=2009, pmax=300, hr=6850, pl=0.85, db=60, dbhr=10500, f0=0.013, f1=0.023, disp="cycle_daily", bypass="Y",
         offer="unfired", price=12.40),
    dict(key="MP", eia="Moraine Point Generating Station", epa="Moraine Point", trade="Moraine Point",
         seller="Moraine Point Energy LLC", code=64803, state="WA", county="Skagit", zone="west", config="1x1",
         year=2002, pmax=330, hr=6935, pl=0.52, db=0, dbhr=0, f0=0.012, f1=0.021, disp="base", bypass="N",
         offer="unfired", price=12.25),
    dict(key="CB", eia="Coldbrook Combined Cycle", epa="Coldbrook", trade="Coldbrook Combined Cycle",
         seller="Coldbrook Power Company", code=65177, state="WA", county="Walla Walla", zone="east", config="2x1",
         year=1997, pmax=500, hr=7790, pl=0.52, db=0, dbhr=0, f0=0.012, f1=0.023, disp="base", bypass="Y",
         offer="unfired", price=10.40),
]
KEYS = [p["key"] for p in PLANTS]
P = {p["key"]: p for p in PLANTS}

# EPA monitoring: one stack per combustion turbine. Moraine Point's stack was renumbered when its monitoring system
# was replaced on 1 July 2025 (CT-1 to 1A); Coldbrook's monitoring plan reports turbine-only gross load.
RENUMBER = {"MP": ("CT-1", "1A", dt.date(2025, 7, 1))}
TURBINE_ONLY_LOAD = {"CB"}


def stacks(key):
    p = P[key]
    if key in RENUMBER:
        return [RENUMBER[key][0]]
    if p["config"] == "2x1":
        return ["CT1", "CT2"]
    if p["config"] == "1x1ss":
        return ["1"]
    return ["CT1"]


def gads_units(key):
    c = P[key]["config"]
    return {"2x1": ["CT1", "CT2", "ST1"], "1x1": ["CT1", "ST1"], "1x1ss": ["CS1"]}[c]


# co-located units under the same EIA plant code that are not part of any offer (simple-cycle peakers)
PEAKERS = {"PM": [("GT3", 46.0, 2001), ("GT4", 46.0, 2001)], "CB": [("GT5", 88.0, 2010)]}

# two offers carry no EIA plant code (the sellers left the field blank)
OFFER_NO_CODE = {"KC", "AG"}

CLIMATE = {"east": dict(mean=52.5, amp=23.0, diurnal=10.5, sd=4.2), "west": dict(mean=51.5, amp=12.5, diurnal=7.0, sd=3.2)}


def cap_unfired(pmax, t):
    """gross MW a combined cycle can make without duct firing at ambient temperature t (F)"""
    if t >= 59.0:
        return pmax * (1.0 - 0.0033 * (t - 59.0))
    return pmax * min(1.04, 1.0 + 0.0022 * (59.0 - t))


DESIGN_T = 100.0

# a forced outage on New Year's morning, and one running from New Year's Eve into 2026 (local standard time)
BOUNDARY = {"OF": (dt.datetime(2025, 1, 1, 0, 42), dt.datetime(2025, 1, 1, 12, 13)),
            "MP": (dt.datetime(2025, 12, 31, 17, 26), dt.datetime(2026, 1, 1, 9, 51))}                      # sellers rate a baseload contract capacity at the 100 F design day
