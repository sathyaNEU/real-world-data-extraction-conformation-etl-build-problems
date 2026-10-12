"""The Upper Kestrel Valley Air Quality Management District's world: Harlow Falls along a valley running
northeast to southwest, the district's Harlow Falls station at the district office, the five permitted odor
sources, the calendar and the district's odor complaint procedure."""
import datetime as dt
import math
from zoneinfo import ZoneInfo

LOCAL = ZoneInfo("America/Los_Angeles")
PST = dt.timezone(dt.timedelta(hours=-8))
UTC = dt.timezone.utc

YEAR0 = dt.date(2026, 1, 1)
LAST = dt.date(2026, 9, 30)                       # the station export and the asks end here
SEASON0, SEASON1 = dt.date(2026, 5, 1), dt.date(2026, 9, 30)
EXPORT = dt.datetime(2026, 10, 2, 8, 41)          # the complaint system export, local time
DAYS = [YEAR0 + dt.timedelta(k) for k in range((LAST - YEAR0).days + 1)]
SEASON_DAYS = [d for d in DAYS if SEASON0 <= d <= SEASON1]

# the station (district office, 1180 Mill Street) and the local plane
STATION = (39.74612, -121.61937)
KM_LAT = 1.0 / 110.99
KM_LON = 1.0 / (111.32 * math.cos(math.radians(STATION[0])))
VALLEY_AXIS = 45.0                                 # degrees: up-valley towards the northeast

# the procedure (CP-14 rev. 4)
UPWIND_DEG = 30.0
CALM_MS = 0.5
EVENT_WINDOW = dt.timedelta(hours=2)
MIN_RECORDS = 9                                    # of the hour's twelve 5-minute records

ORG = "Upper Kestrel Valley Air Quality Management District"
ORG_SHORT = "UKVAQMD"
TOWN = "Harlow Falls"


def to_latlon(x_km, y_km):
    return STATION[0] + y_km * KM_LAT, STATION[1] + x_km * KM_LON


def polar(bearing_deg, dist_km):
    return dist_km * math.sin(math.radians(bearing_deg)), dist_km * math.cos(math.radians(bearing_deg))


# the five permitted odor sources: key -> (name, bearing from the station, distance km, permit, operator)
FAC = {
    "landfill": dict(name="Pine Gulch Landfill", short="Pine Gulch Landfill", bearing=38.0, dist=6.2,
                     permit="P-0412", operator="Kestrel County Department of Public Works"),
    "compost": dict(name="Ridgeway Organics composting facility", short="Ridgeway Organics", bearing=238.0,
                    dist=4.6, permit="P-1187", operator="Ridgeway Organics LLC"),
    "wwtp": dict(name="Harlow Falls Water Pollution Control Plant", short="Harlow Falls WPCP", bearing=168.0,
                 dist=1.7, permit="P-0096", operator="City of Harlow Falls"),
    "render": dict(name="Kestrel Valley Rendering", short="Kestrel Valley Rendering", bearing=334.0, dist=4.1,
                   permit="P-0733", operator="Kestrel Valley Rendering Co."),
    "mush": dict(name="Sutter Bend Mushroom Farms substrate wharf", short="Sutter Bend Mushroom Farms",
                 bearing=118.0, dist=3.2, permit="P-1024", operator="Sutter Bend Mushroom Farms Inc."),
}
FKEYS = ["landfill", "compost", "wwtp", "render", "mush"]
for k, f in FAC.items():
    f["xy"] = polar(f["bearing"], f["dist"])
    f["lat"], f["lon"] = (round(v, 5) for v in to_latlon(*f["xy"]))

# 2026 changes the permit list records (every source had one)
CHANGES = {
    "compost": (dt.date(2026, 3, 2), "Permit modification: food waste accepted (City of Harlow Falls collection "
                                     "from 2 March 2026; Kestrel County collection from 1 June 2026)"),
    "wwtp": (dt.date(2026, 4, 13), "Authority to construct: four solar biosolids drying beds placed in service"),
    "landfill": (dt.date(2026, 5, 11), "Cell 7 opened for disposal"),
    "mush": (dt.date(2026, 5, 18), "Phase I substrate wharf extended by two bays"),
    "render": (dt.date(2026, 6, 15), "Second cooking shift (14:00 to 22:30) added"),
}


def bearing_deg(lat0, lon0, lat1, lon1):
    """Initial great-circle bearing, degrees from true north."""
    p0, p1 = math.radians(lat0), math.radians(lat1)
    dl = math.radians(lon1 - lon0)
    x = math.sin(dl) * math.cos(p1)
    y = math.cos(p0) * math.sin(p1) - math.sin(p0) * math.cos(p1) * math.cos(dl)
    return (math.degrees(math.atan2(x, y)) + 360.0) % 360.0


def bearing_planar(lat0, lon0, lat1, lon1):
    dx = (lon1 - lon0) / KM_LON
    dy = (lat1 - lat0) / KM_LAT
    return (math.degrees(math.atan2(dx, dy)) + 360.0) % 360.0


def angdiff(a, b):
    return abs((a - b + 180.0) % 360.0 - 180.0)


def local_to_pst(t):
    """A naive local wall time to the naive PST wall time the station keeps."""
    aware = t.replace(tzinfo=LOCAL)
    return aware.astimezone(PST).replace(tzinfo=None)


def pst_to_local(t):
    return t.replace(tzinfo=PST).astimezone(LOCAL).replace(tzinfo=None)


def in_season(t_local):
    return SEASON0 <= t_local.date() <= SEASON1
