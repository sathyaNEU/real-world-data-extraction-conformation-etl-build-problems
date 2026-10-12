"""Every figure the build owes, computed from the files under target/ (the generator's own reading; verify.py
is the independent one): the season's odor events, the station's hourly winds, the rungs and the fork grid, the
asks under the golden handling and under each mishandling, the chart's sectors."""
import collections
import csv
import datetime as dt
import json
import os

import core
import logic as L
import pack as P

SECTORS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]


def tparse(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M")


def read_met(target):
    met = collections.defaultdict(list)
    with open(os.path.join(target, P.FILES["met"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            t = tparse(r["datetime_pst"])
            if r["qc"] == "M":
                met[(t.date(), t.hour)].append((t.minute, None, None, None, "M"))
            else:
                met[(t.date(), t.hour)].append((t.minute, float(r["ws_ms"]), float(r["wd_deg"]),
                                                float(r["sigma_theta_deg"]), "V"))
    return met


def read_held(target):
    """Minutes the maintenance log shows the vane held or the monitor unplugged: {(date, hour): set(minutes)}."""
    rows = list(csv.DictReader(open(os.path.join(target, P.FILES["maint"]), encoding="utf-8")))
    spans = []
    start = None
    for r in rows:
        w = r["work"].lower()
        if "vane held" in w:
            d = dt.date.fromisoformat(r["date"])
            a = dt.datetime.combine(d, dt.time.fromisoformat(r["start_pst"]))
            b = dt.datetime.combine(d, dt.time.fromisoformat(r["end_pst"]))
            spans.append((a, b))
        elif "cable left unplugged" in w:
            start = dt.datetime.combine(dt.date.fromisoformat(r["date"]), dt.time.fromisoformat(r["start_pst"]))
        elif "installed and connected" in w and start is not None:
            spans.append((start, dt.datetime.combine(dt.date.fromisoformat(r["date"]), dt.time.fromisoformat(r["end_pst"]))))
            start = None
    held = collections.defaultdict(set)
    for a, b in spans:
        t = a
        while t < b:
            held[(t.date(), t.hour)].add(t.minute)
            t += dt.timedelta(minutes=5)
    return held, spans


def hourly(met, held=None, method="vector"):
    out = {}
    for key, recs in met.items():
        h = held.get(key) if held is not None else None
        w = L.hour_wind(recs, h, method)
        out[key] = w
    return out


def read_complaints(target):
    with open(os.path.join(target, P.FILES["complaints"]), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["received_t"] = tparse(r["received"])
        r["noticed_t"] = tparse(r["noticed"])
        r["lat"] = float(r["latitude"])
        r["lon"] = float(r["longitude"])
    return rows


def read_boundary(target):
    gj = json.load(open(os.path.join(target, P.FILES["boundary"]), encoding="utf-8"))
    ring = gj["features"][0]["geometry"]["coordinates"][0]
    return [(lat, lon) for lon, lat in ring[:-1]]


def read_ocs(target):
    return list(csv.DictReader(open(os.path.join(target, P.FILES["ocs"]), encoding="utf-8")))


def clean(rows, ocs, poly, resends=True, utc=True, imported=True, district=True, pairs_over=False, key="text"):
    """The golden handling, each step switchable for the asks' stops.
    resends: one report once (the procedure's definition of a complaint): a report the app sent again carries the
    same household and time noticed, arrives later, and its text is the saved draft of the report already received;
    key: how a solver finds a report received twice ('text' the golden; 'household' any second row with the same
    household and time noticed; 'contact' any second row with the same contact and time noticed);
    utc: app rows written in UTC until the 30 April release (their noticed time falls after their received time);
    imported: rows carried over from the retired system (matched on address and description) belong to 2025;
    district: rows from outside the boundary are referred; pairs_over: the over-cleaner keeping one row per
    household and clock hour."""
    out = []
    seen = set()
    seen_text = {}
    ocs_keys = {(L.norm_address(o["location"]), o["complaint_text"].strip().lower()) for o in ocs}
    for r in sorted(rows, key=lambda r: (r["received_t"], r["complaint_no"])):
        r = dict(r)
        t = r["noticed_t"]
        if utc and r["channel"] == "App" and t > r["received_t"]:
            off = 8 if t - dt.timedelta(hours=8) < dt.datetime(2026, 3, 8, 2) else 7
            t = t - dt.timedelta(hours=off)
        r["noticed_local"] = t
        if imported and (L.norm_address(r["address"]), r["description"].strip().lower()) in ocs_keys \
                and r["received_t"].date() == dt.date(2026, 1, 6):
            r["noticed_local"] = None              # noticed in November or December 2025
        if district and not P.point_in(r["lat"], r["lon"], poly):
            continue
        r["household"] = L.norm_address(r["address"])
        if resends:
            if key == "text":
                k = (r["household"], r["noticed"])
                if k in seen and any(r["description"].strip().lower() in p for p in seen_text[k]):
                    continue
                seen.add(k)
                seen_text.setdefault(k, []).append(r["description"].strip().lower())
            else:
                k = ("K", r["household"] if key == "household" else r["contact_id"], r["noticed"])
                if k in seen:
                    continue
                seen.add(k)
        if pairs_over:
            k2 = ("P", r["household"], r["noticed"][:13])
            if k2 in seen:
                continue
            seen.add(k2)
        out.append(r)
    return out


def season_events(clean_rows):
    rr = [dict(household=r["household"], noticed=r["noticed_local"], lat=r["lat"], lon=r["lon"])
          for r in clean_rows if r["noticed_local"] is not None and core.in_season(r["noticed_local"])]
    return L.events(rr)


def months_noticed(clean_rows):
    c = collections.Counter()
    for r in clean_rows:
        t = r["noticed_local"]
        if t is not None and core.YEAR0 <= t.date() <= core.LAST:
            c[t.month] += 1
    return [c[m] for m in range(1, 10)]


def station_hours(met, held, months=range(5, 10), local=True, method="vector", use_held=True):
    """Usable and calm hours per month (local months by default)."""
    hw = hourly(met, held if use_held else None, method)
    usable = collections.Counter()
    calm = collections.Counter()
    for (d, h), w in hw.items():
        t = dt.datetime(d.year, d.month, d.day, h)
        m = core.pst_to_local(t).month if local else t.month
        y = core.pst_to_local(t).year if local else t.year
        if y != 2026:
            continue
        if w is not None:
            usable[m] += 1
            if w[0] < core.CALM_MS:
                calm[m] += 1
    return [usable[m] for m in months], [calm[m] for m in months]


def sector_counts(evs, hw):
    c = collections.Counter()
    calm = nowind = 0
    for e in evs:
        d, h = L.event_hour(e)
        w = hw.get((d, h))
        if w is None:
            nowind += 1
        elif w[0] < core.CALM_MS:
            calm += 1
        else:
            c[SECTORS[int(((w[1] + 11.25) % 360) // 22.5)]] += 1
    return [c[s] for s in SECTORS], calm, nowind


def description_tally(clean_rows):
    words = {"landfill": ("dump", "landfill", "trash", "garbage"), "wwtp": ("sewage", "sewer", "rotten egg"),
             "render": ("rendering", "dead animal", "meat"), "mush": ("manure", "mushroom", "ammonia"),
             "compost": ("compost", "rotting food", "spoiled food", "vinegar")}
    c = collections.Counter()
    for r in clean_rows:
        if r["noticed_local"] is None or not core.in_season(r["noticed_local"]):
            continue
        low = r["description"].lower()
        for f, ws in words.items():
            if any(w in low for w in ws):
                c[f] += 1
    return {f: c[f] for f in core.FKEYS}


def main(target):
    met = read_met(target)
    held, spans = read_held(target)
    hw = hourly(met, held)
    rows = read_complaints(target)
    ocs = read_ocs(target)
    poly = read_boundary(target)
    gold = clean(rows, ocs, poly)
    evs = season_events(gold)
    F = dict(n_events=len(evs), events=evs, hw=hw)
    for mode in ("count", "all", "same", "month", "pm1", "incl"):
        O, E = L.compare(evs, hw, mode if mode != "count" else "count")
        F[mode] = (O, E)
    O, E = F["same"]
    F["O"] = O
    F["E"] = {f: E[f] for f in core.FKEYS}
    F["excess"] = {f: O[f] - E[f] for f in core.FKEYS}
    F["ratio"] = {f: O[f] / E[f] for f in core.FKEYS}
    order, _ = L.pick(O, E, "excess")
    F["call"], F["rival"] = order[0], order[1]
    F["R0"] = L.pick(*F["count"], "count")
    F["R1"] = L.pick(*F["all"], "ratio")
    F["sectors"], F["calm_events"], F["nowind_events"] = sector_counts(evs, hw)
    F["desc"] = description_tally(gold)
    F["months"] = months_noticed(gold)
    F["carried"] = sum(1 for r in gold if r["noticed_local"] is None)
    F["usable"], F["calm"] = station_hours(met, held)
    F["gold_rows"] = gold
    F["met"], F["held"], F["spans"] = met, held, spans
    F["rows"], F["ocs"], F["poly"] = rows, ocs, poly
    return F
