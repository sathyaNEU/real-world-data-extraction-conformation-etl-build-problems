"""The operating records drawn from the clean truth: service points and their addresses, the DMV plug-in vehicle
notifications as the utility receives and matches them, the rate schedule change log, the 2026 EV charging load study
(its participants' sessions replayed from the same draws the summer was simulated with) and the district weather.

Nothing here changes the truth; every record is a view of it, with the realistic mess of the system that writes it."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import common as K
import world as W

AS_OF = pd.Timestamp(K.AS_OF)
REC = pd.Timestamp(K.RECORD_DATE)

# ------------------------------------------------------------------------------------------------- places
CITIES = {
    "Foothill": [("Cedar Gap", ("95722", "95726")), ("Pine Hollow", ("95735",))],
    "Railyard": [("Calloway", ("95301", "95303"))],
    "Canal": [("Calloway", ("95305", "95307"))],
    "Mission": [("Loma Pardo", ("95318", "95319"))],
    "West Bluff": [("Loma Pardo", ("95321",)), ("Tule Bend", ("95324",))],
    "Crestview": [("Cottrell", ("95340", "95342"))],
    "Lakeside": [("Cottrell", ("95344",)), ("Lake Vardon", ("95346",))],
    "Sunrise": [("Juniper Springs", ("95352", "95353"))],
    "Sandhill": [("Garnet Wells", ("95360", "95362"))],
    "Kingsley": [("Kingsley", ("95365", "95367"))],
    "Highland": [("Cottrell", ("95348",)), ("Copper Flat", ("95349",))],
    "Brookside": [("Calloway", ("95308", "95309"))],
}
TREES = ["Oak", "Walnut", "Almond", "Olive", "Sycamore", "Cottonwood", "Willow", "Pepper", "Magnolia", "Laurel", "Cedar",
         "Juniper", "Manzanita", "Buckeye", "Elderberry", "Hawthorn", "Redbud", "Alder", "Peach", "Apricot", "Fig",
         "Pomegranate", "Orange", "Lemon", "Pistachio", "Plum", "Cherry", "Poplar", "Elm", "Maple", "Ash", "Birch",
         "Locust", "Mulberry", "Persimmon", "Quince", "Chestnut", "Hickory", "Aspen", "Spruce", "Hemlock", "Cypress"]
SURN = ["Hamilton", "Garfield", "Lincoln", "Grant", "Jefferson", "Mendoza", "Avila", "Bennett", "Carver", "Dorsey",
        "Ellison", "Fremont", "Gaines", "Harlan", "Irwin", "Jensen", "Keller", "Lassen", "Morrow", "Nunes", "Ortega",
        "Pardee", "Quintana", "Ramos", "Sutter", "Tafoya", "Ulrich", "Valdez", "Whitman", "Yates", "Zamora", "Bidwell",
        "Castro", "Delgado", "Esparza", "Fong", "Gutierrez", "Hollister", "Ibarra", "Jessup", "Kimball", "Lowry",
        "Machado", "Navarro", "Oliveira", "Pacheco", "Rhodes", "Soto", "Toledo", "Vasquez", "Walsh", "Arroyo",
        "Bettencourt", "Cardoza", "Duarte", "Enos", "Freitas", "Goulart", "Medeiros", "Silveira", "Mattos"]
GEO = ["Canal", "Levee", "Ridge", "Ranch", "Mill", "Quarry", "Depot", "Rail", "River", "Creek", "Meadow", "Vista",
       "Sierra View", "Valley View", "Hillcrest", "Sunset", "Sunrise", "Highland", "Lakeview", "Brookside", "Granite",
       "Foothill", "Mesa", "Prairie", "Harvest", "Vineyard", "Orchard", "Grove", "Fairway", "Golden", "Pioneer",
       "Wagon Wheel", "Stagecoach", "Trail", "Mariposa", "Del Rio", "Las Palmas", "Alta Vista", "Linda Vista",
       "Buena Vista", "Paseo", "Camino Alto", "Bonita", "La Paz", "Rancho", "Monte Verde", "Tierra Bella"]
SUFFIX = [("St", "ST", "Street"), ("Ave", "AVE", "Avenue"), ("Dr", "DR", "Drive"), ("Ct", "CT", "Court"),
          ("Ln", "LN", "Lane"), ("Way", "WAY", "Way"), ("Rd", "RD", "Road"), ("Pl", "PL", "Place"),
          ("Cir", "CIR", "Circle")]
SUF_P = [.24, .22, .17, .1, .08, .07, .07, .03, .02]


def ordinal(n):
    return "%d%s" % (n, "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def streets(di, n):
    r = K.rng("streets", di)
    pool = TREES + SURN + GEO + [ordinal(k) for k in range(1, 31)]
    names = r.choice(pool, size=min(n, len(pool)), replace=False)
    out = []
    for nm in names:
        s = int(r.choice(len(SUFFIX), p=SUF_P))
        if nm[0].isdigit():
            s = 0 if r.random() < .7 else 1
        pre = r.choice(["", "", "", "", "N", "S", "E", "W"]) if r.random() < .25 else ""
        out.append((str(pre), str(nm), s))
    return out


def addresses(T):
    """Every premise's service address, as the customer system holds it: transformers on one lateral share a street,
    the premises on one transformer sit side by side, and a transformer serving nine or more premises serves one
    building whose units carry an apartment designator."""
    tx, pr = T.tx, T.pr
    rows = {}
    for di, d in enumerate(K.DISTRICTS):
        r = K.rng("addr", di)
        name = d[0]
        sts = streets(di, 220)
        cities = CITIES[name]
        counters = {}
        sub = tx[tx.di == di]
        lat_street = {}
        for lat in sub["lateral"].unique():
            lat_street[lat] = int(r.integers(len(sts)))
        city_of_feeder = {f: int(r.integers(len(cities))) for f in sub["feeder"].unique()}
        for t in sub.itertuples():
            si = lat_street[t.lateral]
            if r.random() < .15:
                si = int(r.integers(len(sts)))
            ci = city_of_feeder[t.feeder]
            cname, zips = cities[ci]
            z = zips[si % len(zips)]
            key = (si, ci)
            if key not in counters:
                counters[key] = int(r.integers(1, 90)) * 100 + int(r.choice([0, 1])) * 1
            pis = T.prems_of[t.ti]
            pre, nm, s = sts[si]
            if t.n_prem >= 9:
                num = counters[key]
                counters[key] += int(r.choice([10, 20, 30, 40]))
                style = int(r.integers(3))
                for k, p in enumerate(pis):
                    unit = ("Apt %d" % (k + 1)) if style == 0 else (("Unit %s" % chr(65 + k)) if k < 26 else "Unit %d" % (k + 1)) \
                        if style == 1 else ("Apt %d%02d" % (1 + k // 6, 1 + k % 6))
                    rows[p] = (num, pre, nm, s, unit, cname, z)
            else:
                for p in pis:
                    num = counters[key]
                    counters[key] += int(r.choice([2, 2, 2, 4, 4, 6, 8]))
                    rows[p] = (num, pre, nm, s, "", cname, z)
    a = pd.DataFrame.from_dict(rows, orient="index", columns=["num", "pre", "street", "suf", "unit", "city", "zip"])
    a.index.name = "pi"
    return a.reindex(pr["pi"].values)


def sp_line(a):
    pre = (a.pre + " ").where(a.pre != "", "")
    suf = a.suf.map(lambda s: SUFFIX[s][0])
    line = a.num.astype(str) + " " + pre + a.street + " " + suf
    return (line + (" " + a.unit).where(a.unit != "", "")).str.replace("  ", " ")


def ids(T):
    """Service point ids (ten digits) and unit serials."""
    r = K.rng("sp-ids")
    n = len(T.pr)
    sp = 5000000000 + np.sort(r.choice(np.arange(10 ** 6, 10 ** 9), size=n, replace=False))
    sp = sp[r.permutation(n)]
    return pd.Series(sp, index=T.pr["pi"].values)


SCHED = {K.RATE_TOU: "R-TOU4", K.RATE_CARE: "R-TOU4", K.RATE_EV: "R-EV2", K.RATE_FLAT: "R-1"}


def service_points(T, A, SP):
    pr = T.pr
    tx = T.tx.set_index("ti")
    cur = [W.rate_on(T.pr_base, T.sw, p, AS_OF) for p in pr["pi"]]
    out = pd.DataFrame({
        "sp_id": SP.reindex(pr["pi"]).values,
        "xfmr_loc_id": ["T%d" % x for x in tx.loc[pr["ti"].values, "loc"].values],
        "service_address": sp_line(A).values,
        "city": A["city"].values,
        "zip": A["zip"].values,
        "district": pr["district"].values,
        "rate_schedule": [SCHED[c] for c in cur],
        "care": np.where(pr["base_rate"].values == K.RATE_CARE, "Y", "N"),
    })
    r = K.rng("sp-start")
    start = pd.Timestamp("1998-01-01") + pd.to_timedelta(r.integers(0, 365 * 28, len(out)), unit="D")
    out["account_start"] = np.where(r.random(len(out)) < .15, "", start.strftime("%Y-%m-%d"))
    return out.sort_values("sp_id").reset_index(drop=True)


# ------------------------------------------------------------------------------------------------- rate changes
def rate_changes(T, SP):
    """Every move to R-EV2 since 2018, with the request and the bill-cycle effective date; the winter 2026-27
    enrollment drive's requests came through its campaign page."""
    r = K.rng("rate-log")
    drive_lo, drive_hi = pd.Timestamp(K.DRIVE_START), pd.Timestamp(K.DRIVE_END)
    # a request is received after the summer peak of the premise's transformer whenever the change itself takes
    # effect after it (customers asking in the days after the meter read that set the bill they were reacting to)
    pk26 = dict(zip(T.tx["ti"], W.peak_date(T.tx, 2026)))
    pti = dict(zip(T.pr["pi"], T.pr["ti"]))
    rows = []
    for p, s in sorted(T.sw.items(), key=lambda kv: (kv[1], kv[0])):
        frm = SCHED[T.pr_base[p]]
        if drive_lo <= s <= drive_hi + pd.Timedelta(days=1) and T.pr_district[p] in K.DRIVE_DISTRICTS and \
                T.drive_pi.get(p, False):
            ch = "CAMPAIGN"
            req = s - pd.Timedelta(days=int(r.integers(3, 26)))
        else:
            ch = str(r.choice(["WEB", "CONTACT CTR", "DEALER REF", "WEB", "WEB"]))
            req = s - pd.Timedelta(days=int(r.integers(1, 34)))
        pk = pk26[pti[p]]
        if s > pk >= req and (s - pk).days >= 2:
            req = pk + pd.Timedelta(days=int(r.integers(1, (s - pk).days)))
        rows.append((int(SP[p]), frm, "R-EV2", req.strftime("%Y-%m-%d"), s.strftime("%Y-%m-%d"), ch))
    out = pd.DataFrame(rows, columns=["sp_id", "from_schedule", "to_schedule", "request_date", "effective_date", "channel"])
    out.insert(0, "change_id", ["RC%07d" % (1180000 + 7 * i + int(r.integers(0, 7))) for i in range(len(out))])
    return out


# ------------------------------------------------------------------------------------------------- DMV
MAKES_BEV = [("TESLA", "MODEL 3", "5YJ3E1E", .22), ("TESLA", "MODEL Y", "7SAYGDE", .24), ("CHEVROLET", "BOLT EV", "1G1FY6S", .08),
             ("NISSAN", "LEAF", "1N4AZ1C", .07), ("FORD", "MUSTANG MACH-E", "3FMTK3S", .06), ("HYUNDAI", "IONIQ 5", "KM8KNDA", .06),
             ("KIA", "EV6", "KNDC3DL", .04), ("VOLKSWAGEN", "ID.4", "1V2GNPE", .05), ("RIVIAN", "R1S", "7PDSGAB", .03),
             ("BMW", "I4", "WBY73AW", .03), ("CHEVROLET", "EQUINOX EV", "3GNKDBR", .04), ("TESLA", "MODEL S", "5YJSA1E", .03),
             ("TESLA", "MODEL X", "7SAXCBE", .02), ("HONDA", "PROLOGUE", "5J6YD9H", .03)]
MAKES_PHEV = [("TOYOTA", "RAV4 PRIME", "JTMFB3F", .26), ("CHRYSLER", "PACIFICA HYBRID", "2C4RC1L", .14),
              ("JEEP", "WRANGLER 4XE", "1C4JJXR", .14), ("JEEP", "GRAND CHEROKEE 4XE", "1C4RJYD", .08),
              ("FORD", "ESCAPE PHEV", "1FMCU0E", .08), ("BMW", "X5 XDRIVE50E", "5UX43EU", .05),
              ("TOYOTA", "PRIUS PRIME", "JTDACAA", .15), ("KIA", "NIRO PHEV", "KNDCM3L", .10)]
YEARCODE = {2014: "E", 2015: "F", 2016: "G", 2017: "H", 2018: "J", 2019: "K", 2020: "L", 2021: "M", 2022: "N", 2023: "P",
            2024: "R", 2025: "S", 2026: "T", 2027: "V"}
STATUS = ["EXPIRED", "TRANSFERRED", "ADDR CHANGE", "OUT OF STATE"]


def dmv_line(a, r):
    """The registered address as DMV keys it: upper case, its own abbreviations, units after a pound sign or written
    out."""
    pre = a.pre
    nm = a.street.upper()
    s = SUFFIX[a.suf]
    suf = s[1] if r.random() < .82 else s[2].upper()
    if pre and r.random() < .3:
        pre = {"N": "NORTH", "S": "SOUTH", "E": "EAST", "W": "WEST"}[pre]
    line = " ".join(x for x in [str(a.num), pre, nm, suf] if x)
    if a.unit:
        u = a.unit.upper().replace("APT ", "").replace("UNIT ", "")
        line += (" #" + u) if r.random() < .45 else (" APT " + u if a.unit.startswith("Apt") else " UNIT " + u)
    return line


def dmv(T, A, SP, unmatched):
    """One row per vehicle registration at an address, as the DMV notification feed delivers it, with the utility's
    address match. unmatched: the vehicles whose notification the matcher could not place (the address keyed in a
    way it does not resolve: a unit left off or a misspelt street); the transformer they sit on is the same either way."""
    v = T.veh.sort_values(["reg", "pi"])
    r = K.rng("dmv")
    rows = []
    for i, x in zip(v.index, v.itertuples()):
        a = A.loc[x.pi]
        bev = x.fuel == "BEV"
        mk = MAKES_BEV if bev else MAKES_PHEV
        k = int(r.choice(len(mk), p=np.array([m[3] for m in mk]) / sum(m[3] for m in mk)))
        make, model, vds, _ = mk[k]
        my = int(min(2027, max(2014, x.reg.year + int(r.choice([-3, -2, -1, 0, 0, 0, 1, 1]) if x.reg.month >= 7 else
                                                     r.choice([-3, -2, -1, -1, 0, 0, 0])))))
        vin = "%s%d%s%s%s" % (vds, int(r.integers(0, 10)), YEARCODE[my], "ABCFNP"[int(r.integers(6))], "******")
        line = dmv_line(a, r)
        matched = "" if i in unmatched else str(int(SP[x.pi]))
        if i in unmatched:
            # the address as keyed: the unit left off, or the street misspelt
            if a.unit:
                line = line.split(" #")[0].split(" APT ")[0].split(" UNIT ")[0]
            else:
                w = line.split(" ")
                j = 1 + int(w[1] in ("N", "S", "E", "W", "NORTH", "SOUTH", "EAST", "WEST"))
                if j < len(w) and len(w[j]) > 3:
                    s_ = w[j]
                    c = int(r.integers(1, len(s_) - 1))
                    w[j] = s_[:c] + s_[c + 1:] if r.random() < .5 else s_[:c] + s_[c] + s_[c:]
                line = " ".join(w)
        if pd.isna(x.dep) or x.dep > AS_OF:
            st, sd = "CURRENT", ""
        else:
            st, sd = STATUS[int(r.choice(4, p=[.30, .45, .17, .08]))], x.dep.strftime("%Y-%m-%d")
        rows.append((vin, make, model, my, "BEV" if bev else "PHEV", line, a.city.upper(), a.zip,
                     x.reg.strftime("%Y-%m-%d"), st, sd, matched, x.pi, i))
    out = pd.DataFrame(rows, columns=["vin_masked", "make", "model", "model_year", "fuel_type", "reg_address", "reg_city",
                                      "reg_zip", "reg_start_date", "reg_status", "status_date", "matched_sp_id", "_pi", "_vi"])
    out.insert(0, "notification_id", "")
    out["match_method"] = np.where(out.matched_sp_id == "", "", np.where(r.random(len(out)) < .91, "EXACT", "NORMALIZED"))
    return out


def dmv_outside(T, n=640):
    """Notifications at addresses on no single-phase residential service in the file (apartment buildings on
    three-phase services, businesses, rural addresses served by another utility): the matcher leaves them blank."""
    r = K.rng("dmv-outside")
    rows = []
    for i in range(n):
        di = int(r.integers(len(K.DISTRICTS)))
        name = K.NAMES[di]
        cname, zips = CITIES[name][int(r.integers(len(CITIES[name])))]
        sts = streets(di, 220)
        pre, nm, s = sts[int(r.integers(len(sts)))]
        num = int(r.integers(10, 9900))
        kind = r.random()
        if kind < .45:
            line = "%d %s%s %s #%d" % (num, (pre + " ") if pre else "", nm.upper(), SUFFIX[s][1], int(r.integers(101, 450)))
        elif kind < .75:
            line = "%d %s%s %s STE %d" % (num, (pre + " ") if pre else "", nm.upper(), SUFFIX[s][1], int(r.integers(100, 300)))
        else:
            line = "%d %s RD" % (int(r.integers(10000, 39999)), str(r.choice(["COUNTY", "RANCH", "QUARRY", "MILL CREEK"])))
        reg = pd.Timestamp("2018-01-02") + pd.Timedelta(days=int(r.integers(0, (REC - pd.Timestamp("2018-01-02")).days)))
        bev = r.random() < .8
        mk = MAKES_BEV if bev else MAKES_PHEV
        make, model, vds, _ = mk[int(r.integers(len(mk)))]
        my = int(min(2027, max(2014, reg.year + int(r.choice([-2, -1, 0, 0, 1])))))
        vin = "%s%d%s%s%s" % (vds, int(r.integers(0, 10)), YEARCODE[my], "ABCFNP"[int(r.integers(6))], "******")
        gone = r.random() < .2
        dep = reg + pd.Timedelta(days=int(r.integers(60, 1500))) if gone else None
        if dep is not None and dep > AS_OF:
            dep = None
        rows.append((vin, make, model, my, "BEV" if bev else "PHEV", line, cname.upper(), zips[0], reg.strftime("%Y-%m-%d"),
                     "CURRENT" if dep is None else STATUS[int(r.integers(4))], "" if dep is None else dep.strftime("%Y-%m-%d"),
                     "", -1))
    return pd.DataFrame(rows, columns=["vin_masked", "make", "model", "model_year", "fuel_type", "reg_address", "reg_city",
                                       "reg_zip", "reg_start_date", "reg_status", "status_date", "matched_sp_id", "_pi"])


# ------------------------------------------------------------------------------------------------- the load study
def replay_sessions(T, di, year, want):
    """The charging sessions of the wanted vehicles in one district's summer, from the same random draws the summer was
    simulated with (the stream is consumed in the same order, so every vehicle's days are its own)."""
    veh, sw, pr_base = T.veh, T.sw, T.pr_base
    rr = K.rng("charge", di, year)
    ys = pd.Timestamp(K.summer_start(year))
    off = np.array([W.off_day(year, i) for i in range(K.NDAY)])
    vd = veh[(veh.di == di) & (veh.reg <= pd.Timestamp("%d-09-30" % year))]
    out = {}
    for idx, v in zip(vd.index, vd.itertuples()):
        d0 = max(0, (v.reg - ys).days)
        d1 = K.NDAY if pd.isna(v.dep) else min(K.NDAY, (v.dep - ys).days)
        nd = max(0, d1 - d0)
        u_slip = rr.random(K.NDAY); u_ch = rr.random(K.NDAY)
        st_w = rr.normal(17.6, 1.0, K.NDAY); st_o = rr.normal(15.8, 2.4, K.NDAY)
        en = np.clip(rr.gamma(4.0, v.emean / 4.0, K.NDAY), 1.0, 45.0)
        if nd <= 0 or idx not in want:
            continue
        days = np.arange(d0, d1)
        s = sw.get(v.pi)
        ev2 = np.zeros(nd, bool) if s is None else (ys + pd.to_timedelta(days, unit="D") >= s)
        if pr_base[v.pi] == K.RATE_FLAT:
            ev2[:] = False
        pa = np.where(ev2, K.BEH["EV"][0], K.BEH["TOU"][0])
        pt = np.where(ev2, K.BEH["EV"][1], K.BEH["TOU"][1])
        slip = np.where(ev2, K.SLIP["EV"], K.SLIP["TOU"])
        beh = np.where(v.u_beh < pa, 0, np.where(v.u_beh < pa + pt, 1, 2))
        beh = np.where((beh > 0) & (u_slip[days] < slip), 0, beh)
        charges = u_ch[days] < v.q
        start = np.where(beh == 0, np.where(off[days], st_o[days], st_w[days]), np.where(beh == 1, 21.0, 24.0))
        end = start + en[days] / v.P
        out[idx] = (days, start, end, charges, float(v.P))
    return out


def load_study(T, n_tou=184, n_ev=138):
    """The 2026 EV charging load study: premises with a vehicle all summer on R-TOU4 or R-EV2 (unchanged all summer),
    sampled by rate, each EVSE submetered at 15 minutes from enrollment. Returns the participant table and the
    interval table (interval-ending local time, kWh)."""
    r = K.rng("load-study")
    v = T.veh
    ys, ye = pd.Timestamp("2026-06-01"), pd.Timestamp("2026-09-30")
    whole = v[(v.reg < ys) & (v.dep.isna() | (v.dep > ye)) & (v.phase == "hist")]
    one = whole.groupby("pi").size()
    whole = whole[whole.pi.map(one) == 1]
    rate_s = np.array([W.rate_on(T.pr_base, T.sw, p, ys) for p in whole["pi"]])
    rate_e = np.array([W.rate_on(T.pr_base, T.sw, p, ye) for p in whole["pi"]])
    stable = rate_s == rate_e
    tou = whole[stable & (rate_s == K.RATE_TOU)]
    ev = whole[stable & (rate_s == K.RATE_EV)]
    pick = list(r.choice(tou.index.values, size=n_tou, replace=False)) + list(r.choice(ev.index.values, size=n_ev, replace=False))
    pick = sorted(pick, key=lambda i: (int(v.loc[i, "di"]), int(i)))
    sessions = {}
    for di in sorted(set(int(v.loc[i, "di"]) for i in pick)):
        sessions.update(replay_sessions(T, di, 2026, set(i for i in pick if int(v.loc[i, "di"]) == di)))
    parts, ivals = [], []
    nq = K.NDAY * 96
    qstart = np.arange(96) * 0.25
    for k, i in enumerate(r.permutation(pick)):
        x = v.loc[i]
        pid = "LR26-%04d" % (k + 1 + 3 * (k // 40))
        days, start, end, charges, P = sessions[i]
        kwh = np.zeros(nq + 96)
        for d, s0, e0, c in zip(days, start, end, charges):
            if not c:
                continue
            base = d * 96
            lo = int(np.floor(s0 / 0.25))
            hi = int(np.ceil(e0 / 0.25))
            for q in range(lo, hi):
                ov = min(e0, (q + 1) * 0.25) - max(s0, q * 0.25)
                if ov > 0 and base + q < len(kwh):
                    kwh[base + q] += ov * P
        kwh = kwh[:nq]
        late = r.random() < .1
        enr = int(r.integers(9, 50)) if late else 0
        mask = np.zeros(nq, bool)
        mask[enr * 96:] = True
        # communication gaps: whole days or runs of intervals lost at the head-end
        for _ in range(int(r.poisson(1.3))):
            g0 = int(r.integers(enr * 96, nq))
            mask[g0:g0 + int(r.integers(4, 200))] = False
        rate = W.rate_on(T.pr_base, T.sw, int(x.pi), ys)
        parts.append((pid, K.NAMES[int(x.di)], "R-EV2" if rate == K.RATE_EV else "R-TOU4", x.fuel,
                      "L1" if P < 2 else "L2", P, (ys + pd.Timedelta(days=enr)).strftime("%Y-%m-%d"),
                      int((nq - enr * 96)), int(mask.sum())))
        q = np.where(mask)[0]
        ivals.append(pd.DataFrame({"participant_id": pid, "q": q, "kwh": np.round(kwh[q], 3)}))
    P_ = pd.DataFrame(parts, columns=["participant_id", "district", "rate_schedule", "fuel_type", "evse_level",
                                      "charging_kw", "data_start", "intervals_expected", "intervals_received"])
    I = pd.concat(ivals, ignore_index=True)
    I["interval_ending"] = ys + pd.to_timedelta((I["q"] + 1) * 15, unit="m")
    I = I[["participant_id", "interval_ending", "kwh"]].sort_values(["participant_id", "interval_ending"]).reset_index(drop=True)
    return P_.sort_values("participant_id").reset_index(drop=True), I


# ------------------------------------------------------------------------------------------------- weather
STATIONS = {"Foothill": ("CVW-14", "Cedar Gap airfield"), "Railyard": ("CVW-02", "Calloway service center"),
            "Canal": ("CVW-03", "Calloway canal yard"), "Mission": ("CVW-06", "Loma Pardo substation"),
            "West Bluff": ("CVW-07", "Tule Bend substation"), "Crestview": ("CVW-09", "Cottrell service center"),
            "Lakeside": ("CVW-10", "Lake Vardon pump station"), "Sunrise": ("CVW-11", "Juniper Springs substation"),
            "Sandhill": ("CVW-05", "Garnet Wells substation"), "Kingsley": ("CVW-08", "Kingsley service center"),
            "Highland": ("CVW-12", "Copper Flat substation"), "Brookside": ("CVW-04", "Brookside substation")}


def weather():
    rows = []
    r = K.rng("wx-gaps")
    for di, d in enumerate(K.DISTRICTS):
        sid, sname = STATIONS[d[0]]
        for y in K.SUMMERS:
            tt = W.temperatures(di, y)
            miss = set(r.choice(K.NDAY, size=int(r.integers(0, 4)), replace=False).tolist())
            for i in range(K.NDAY):
                day = K.day_of(y, i)
                rows.append((sid, sname, day.strftime("%Y-%m-%d"), "" if i in miss else "%d" % int(tt[i]),
                             "M" if i in miss else ""))
    return pd.DataFrame(rows, columns=["station_id", "station_name", "date", "tmax_f", "qc_flag"])
