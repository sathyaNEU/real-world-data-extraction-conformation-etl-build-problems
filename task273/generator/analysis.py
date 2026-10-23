"""The golden analysis on the cut pack, and every other route through it.

The call: each use's crashes caused per mile driven, against private drivers'. The crashes come straight from the
reports. The miles come from the vehicles the at-fault drivers struck in crashes between moving vehicles: within one
road class, day type and hour, the struck vehicles are a draw from the traffic there, so each use's share of them is its
share of that stratum's miles, and the Department's miles for the stratum (the class's annual VMT spread over the week
by its count stations' hours) turn the shares into miles. The other routes are the rungs of the ladder and the members
of the golden's family."""
import datetime as dt
import math

import common as K
import pack as P

PRIV = ("PV",)


def half_up(x, nd=0):
    q = 10 ** nd
    return math.floor(x * q + 0.5 + 1e-9) / q


def per3(h):
    return "night" if (h >= 21 or h < 6) else ("peak" if h in (7, 8, 16, 17, 18) else "day")


class Data:
    def __init__(self, target):
        self.target = target
        self.cr = P.load(target)
        self.vmt = P.tmr_vmt(target)
        self.atr = P.atr_totals(target)
        self._dow = None

    # ---- the Department's miles by stratum
    def share(self, g):
        cells = self.atr[g]
        s = sum(cells.values())
        return {k: v / s for k, v in cells.items()}

    def dow_share(self, g):
        if self._dow is None:
            import csv
            st = P.stations(self.target)
            tot = {x: {} for x in K.GROUPS}
            with open(P.path(self.target, "atr"), encoding="utf-8", newline="") as f:
                for r in csv.DictReader(f):
                    gg = st[r["STATION_ID"]]
                    wd = dt.date.fromisoformat(r["COUNT_DATE"]).weekday()
                    for h in range(24):
                        v = r["HR%02d" % (h + 1)]
                        if v != "":
                            tot[gg][(wd, h)] = tot[gg].get((wd, h), 0.0) + float(v)
            self._dow = {x: {k: v / sum(c.values()) for k, v in c.items()} for x, c in tot.items()}
        return self._dow[g]

    def avgday_share(self, g, year=2025):
        """The count programme's average-day expansion: the mean day of each type at each hour, times the year's days
        of that type."""
        import csv
        st = P.stations(self.target)
        acc, nd = {}, {}
        with open(P.path(self.target, "atr"), encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                if st[r["STATION_ID"]] != g:
                    continue
                d = dt.date.fromisoformat(r["COUNT_DATE"])
                dtp = "we" if d.weekday() >= 5 else "wd"
                key = (r["STATION_ID"], r["DIR"], dtp)
                nd[key] = nd.get(key, 0) + 1
                for h in range(24):
                    v = r["HR%02d" % (h + 1)]
                    if v != "":
                        acc[(key, h)] = acc.get((key, h), 0.0) + float(v)
        days = {"wd": 0, "we": 0}
        x = dt.date(year, 1, 1)
        while x.year == year:
            days["we" if x.weekday() >= 5 else "wd"] += 1
            x += dt.timedelta(days=1)
        cell = {}
        for (key, h), v in acc.items():
            sid, dr, dtp = key
            cell[(dtp, h)] = cell.get((dtp, h), 0.0) + v / nd[key] * days[dtp]
        s = sum(cell.values())
        return {k: v / s for k, v in cell.items()}

    def stratum_miles(self, grain, shares="sum"):
        """Miles (millions) in each stratum of the grain, 2021 to 2025."""
        E = {}
        for (fc, ur), byy in self.vmt.items():
            g = K.GROUP_OF[(fc, ur)]
            if grain == "dow":
                sh = self.dow_share(g)
                for (wd, h), s in sh.items():
                    k = (g, wd, h)
                    E[k] = E.get(k, 0.0) + sum(byy.values()) * s
                continue
            sh = self.share(g) if shares == "sum" else self.avgday_share(g)
            for (d, h), s in sh.items():
                for y, v in byy.items():
                    k = key_of(grain, y, fc, ur, g, d, h)
                    E[k] = E.get(k, 0.0) + v * s
        return E

    # ---- the crashes
    def mv_crashes(self):
        for c in self.cr.values():
            if sum(1 for u in c["units"] if u["type"] == "MV") >= 2:
                yield c

    def numerators(self, priv=PRIV, mode="all"):
        """Crashes caused, 2021 to 2025: each crash between moving vehicles once for each use whose driver was at
        fault in it (rule 3.2 counts crashes, so two of a use's drivers at fault in one crash are one crash)."""
        af = {}
        for c in self.mv_crashes():
            faults = [u for u in c["units"] if u["type"] == "MV" and u["fault"]]
            if mode == "one" and len(faults) != 1:
                continue
            for use in {"PV" if u["use"] in priv else u["use"] for u in faults}:
                af[use] = af.get(use, 0) + 1
        return af

    def exposure(self, grain, sample="all", priv=PRIV):
        """The struck vehicles by stratum: n[(use, stratum)], tot[stratum]."""
        n, tot = {}, {}
        for c in self.mv_crashes():
            mv = [u for u in c["units"] if u["type"] == "MV"]
            faults = [u for u in mv if u["fault"]]
            if sample == "undet":
                if len(faults) > 1:
                    continue
            elif len(faults) != 1:
                continue
            if sample == "two" and len(mv) != 2:
                continue
            if sample == "nohr" and any(u["fled"] for u in mv):
                continue
            if c["group"] is None or c["hour"] is None:
                continue
            k = crash_key(grain, c)
            for u in mv:
                if u["fault"]:
                    continue
                use = "PV" if u["use"] in priv else u["use"]
                n[(use, k)] = n.get((use, k), 0) + 1
                tot[k] = tot.get(k, 0) + 1
        if sample == "parked":
            for c in self.cr.values():
                if c["group"] is None or c["hour"] is None:
                    continue
                pk = [u for u in c["units"] if u["type"] == "PK"]
                if not pk:
                    continue
                k = crash_key(grain, c)
                for u in pk:
                    use = "PV" if u["use"] in priv else u["use"]
                    n[(use, k)] = n.get((use, k), 0) + 1
                    tot[k] = tot.get(k, 0) + 1
        return n, tot

    def miles(self, grain="full", sample="all", priv=PRIV, shares="sum"):
        E = self.stratum_miles(grain if grain in ("full", "fcl", "yr", "dow") else "full", shares)
        if grain not in ("full", "fcl", "yr", "dow"):
            E = coarsen(E, grain)
        n, tot = self.exposure(grain, sample, priv)
        out = {}
        for (use, k), x in n.items():
            out[use] = out.get(use, 0.0) + E[k] * x / tot[k]
        return out, E, n, tot

    def ratios(self, grain="full", sample="all", priv=PRIV, num="all", shares="sum"):
        af = self.numerators(priv, "one" if num == "one" else "all")
        if num == "hr_private":
            hr = sum(1 for c in self.mv_crashes() if any(u["type"] == "MV" and u["fault"] and u["fled"]
                                                          for u in c["units"])
                     and not any(u["type"] == "MV" and u["fault"] and u["use"] in priv for u in c["units"]))
            af["PV"] = af.get("PV", 0) + hr
        mi, E, n, tot = self.miles(grain, sample, priv, shares)
        rate = {u: af.get(u, 0) / mi[u] for u in mi if mi[u] > 0}
        return {u: rate[u] / rate["PV"] for u in K.CODES}, af, mi, rate


def key_of(grain, y, fc, ur, g, d, h):
    if grain == "full":
        return (g, d, h)
    if grain == "fcl":
        return (fc, ur, d, h)
    if grain == "yr":
        return (y, g, d, h)
    raise ValueError(grain)


def crash_key(grain, c):
    g, d, h = c["group"], c["dtype"], c["hour"]
    return {"full": (g, d, h), "fcl": (c["fc"], c["ur"], d, h), "yr": (c["year"], g, d, h),
            "dow": (g, c["date"].weekday(), h), "coarse": (g, d, per3(h)), "road": g, "hour": (d, h),
            "hour_only": h, "urb": (g[0], d, h), "road_dt": (g, d), "pooled": "all"}[grain]


def coarsen(E, grain):
    out = {}
    for (g, d, h), v in E.items():
        k = {"coarse": (g, d, per3(h)), "road": g, "hour": (d, h), "hour_only": h, "urb": (g[0], d, h),
             "road_dt": (g, d), "pooled": "all"}[grain]
        out[k] = out.get(k, 0.0) + v
    return out


def covered(r):
    return sorted((u for u in K.CODES if r[u] >= K.THRESHOLD), key=K.CODES.index)


# ---------------------------------------------------------------------------------------------------------------
def golden(D):
    r, af, mi, rate = D.ratios()
    return dict(ratio=r, af=af, miles=mi, rate=rate, covered=covered(r))


FAMILY = {
    "fcl": dict(grain="fcl"), "yr": dict(grain="yr"), "dow": dict(grain="dow"),
    "two": dict(sample="two"), "nohr": dict(sample="nohr"), "undet": dict(sample="undet"),
    "mc_private": dict(priv=("PV", "MC")), "one_at_fault": dict(num="one"), "hr_private": dict(num="hr_private"),
    "avgday": dict(shares="avgday"), "periods": dict(grain="coarse"),
}
RUNGS = {
    "pooled": dict(grain="pooled"), "road": dict(grain="road"), "hour": dict(grain="hour"),
    "urban_rural": dict(grain="urb"), "parked_in_sample": dict(sample="parked"),
}


def family(D):
    return {k: D.ratios(**v)[0] for k, v in FAMILY.items()}


def rungs(D):
    out = {k: D.ratios(**v)[0] for k, v in RUNGS.items()}
    out["adjusted"] = mantel_haenszel(D)
    out["culpability"] = culpability(D)
    out["per_vehicle"] = per_vehicle(D)
    return out


def mantel_haenszel(D):
    """The textbook relative crash propensity, adjusted over the full strata: what the at-fault drivers' odds are under
    the same road, day and hour."""
    A, N = {}, {}
    for c in D.mv_crashes():
        mv = [u for u in c["units"] if u["type"] == "MV"]
        faults = [u for u in mv if u["fault"]]
        if len(faults) != 1 or c["group"] is None or c["hour"] is None:
            continue
        k = (c["group"], c["dtype"], c["hour"])
        for u in mv:
            use = u["use"]
            if u["fault"]:
                A[(use, k)] = A.get((use, k), 0) + 1
            else:
                N[(use, k)] = N.get((use, k), 0) + 1
    ks = {k for (_, k) in list(A) + list(N)}
    out = {}
    for x in K.CODES:
        num = den = 0.0
        for k in ks:
            a, n0, ap, np_ = A.get((x, k), 0), N.get((x, k), 0), A.get(("PV", k), 0), N.get(("PV", k), 0)
            t = a + n0 + ap + np_
            if t:
                num += a * np_ / t
                den += ap * n0 / t
        out[x] = num / den
    return out


def culpability(D):
    af, naf = {}, {}
    for c in D.mv_crashes():
        for u in c["units"]:
            if u["type"] != "MV":
                continue
            d = af if u["fault"] else naf
            d[u["use"]] = d.get(u["use"], 0) + 1
    share = {x: af.get(x, 0) / (af.get(x, 0) + naf.get(x, 0)) for x in K.CODES + ["PV"]}
    return {x: share[x] / share["PV"] for x in K.CODES}


def vehicle_years(target):
    """Vehicles a year, 2021 to 2025: fleet returns (permit years from 1 July, each calendar year the mean of the two
    permit years it spans), the platforms' quarterly active vehicles (mean of the four quarters), and the private
    registrations of cars, SUVs, pickups and vans."""
    import openpyxl
    wb = openpyxl.load_workbook(P.path(target, "operators"), read_only=True)
    lab = {v: k for k, v in K.LABEL.items()}
    fy = {}
    for i, r in enumerate(wb["Fleet returns"].iter_rows(values_only=True)):
        if i and r[0]:
            fy[(lab[r[2]], int(r[3][:4]))] = fy.get((lab[r[2]], int(r[3][:4])), 0) + int(r[4])
    vy = {}
    for (u, y0), v in fy.items():
        for y in (y0, y0 + 1):
            if y in K.YEARS:
                vy[u] = vy.get(u, 0.0) + 0.5 * v
    plat = {}
    names = P.operator_names(target)
    for r in P.rows(target, "platforms"):
        u = names[r["PLATFORM"].lower()]
        plat[u] = plat.get(u, 0.0) + int(r["ACTIVE_VEHICLES"]) / 4.0
    vy.update(plat)
    wb2 = openpyxl.load_workbook(P.path(target, "registrations"), read_only=True)
    pv = 0
    for r in wb2["Registrations"].iter_rows(values_only=True):
        if r and r[0] in ("Passenger cars", "Sport utility vehicles", "Pickups", "Vans"):
            pv += int(r[1])
    vy["PV"] = pv
    return vy


def per_vehicle(D):
    af = D.numerators()
    vy = vehicle_years(D.target)
    r = {x: af.get(x, 0) / vy[x] for x in vy}
    return {x: r[x] / r["PV"] for x in K.CODES}


# ---------------------------------------------------------------------------------------------------------------
# the asks
def caused_by(c):
    """The uses whose drivers the officer recorded at fault in this crash (any kind of crash)."""
    return {u["use"] for u in c["units"] if u["type"] in ("MV", "PK") and u["fault"] and u["use"] in K.CODES}


def final_persons(D):
    """Each person once, at their latest record (a person listed again in the same seat of the same unit, or the same
    non-motorist, carries the later report), and K for every death in the state's 30-day register."""
    ps = P.persons(D.target)
    by_rpt = {(c["agency"], c["rpt"]): cid for cid, c in D.cr.items()}
    dead = set()
    for r in P.fatalities(D.target):
        ag = {v: k for k, v in K.AGENCIES.items()}[r["AGENCY"]]
        cid = by_rpt[(ag, r["AGENCY_REPORT_NO"])]
        dead.add((cid, int(r["VEHICLE_NO"]), P.PTYPE[r["PERSON_TYPE"]], int(r["AGE"]), r["SEX"]))
    out = {}
    for cid, lst in ps.items():
        latest = {}
        for p in lst:
            k = (p["unit"], p["seat"]) if p["seat"] else (p["unit"], p["ptype"])
            if k not in latest or p["pno"] > latest[k]["pno"]:
                latest[k] = p
        final = []
        for p in latest.values():
            sev = "K" if (cid, p["unit"], p["ptype"], p["age"], p["sex"]) in dead else p["sev"]
            final.append(dict(p, final=sev))
        out[cid] = final
    return out, dead


def ask_people(D):
    """The people killed or seriously injured in the crashes each use's drivers caused: a person once, killed when the
    register holds the death, seriously injured when the latest record is A."""
    fp, dead = final_persons(D)
    ksi = {u: 0 for u in K.CODES}
    for cid, c in D.cr.items():
        uses = caused_by(c)
        if not uses:
            continue
        n = sum(1 for p in fp.get(cid, ()) if p["final"] in ("K", "A"))
        for u in uses:
            ksi[u] += n
    return ksi


def ask_cost(D):
    fp, dead = final_persons(D)
    cost = P.costs(D.target)
    tot = {u: 0 for u in K.CODES}
    for cid, c in D.cr.items():
        uses = caused_by(c)
        if not uses:
            continue
        sev = min((p["final"] for p in fp.get(cid, ())), key="KABCO".index, default="O")
        for u in uses:
            tot[u] += cost[sev]
    return {u: half_up(v / 1e6, 1) for u, v in tot.items()}, tot


if __name__ == "__main__":
    import os
    import sys
    T = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                           "target")
    D = Data(T)
    g = golden(D)
    print("golden", {u: round(g["ratio"][u], 3) for u in K.CODES}, g["covered"])
    for k, v in family(D).items():
        print("family %-13s" % k, {u: round(v[u], 3) for u in K.CODES}, covered(v))
    for k, v in rungs(D).items():
        print("rung   %-16s" % k, {u: round(v[u], 3) for u in K.CODES}, covered(v))
    print("killed or seriously injured", ask_people(D))
    print("cost", ask_cost(D)[0])
