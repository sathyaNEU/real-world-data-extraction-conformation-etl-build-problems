"""What the district recorded: trap-nights, catches by species and sex, and pools with their RT-PCR results, for the
2024 and 2025 seasons and 2026 to the week ending 15 August. The field database migrated to new site IDs on 15 June
2026; a second load on 22 June brought the June Tuesday nights in again, keyed by the pickup morning."""
import datetime as dt
import math

import numpy as np

import ecology as E
import world as W

DAY = dt.timedelta(days=1)


def sites():
    rows = W.site_table()
    for s in rows:
        s["factor"] = E.site_factor(s["site_id"])
        s["active_from"] = dt.date(2024, 6, 1)
        s["active_to"] = None
    # each zone's site factors average one, so a zone's level is its mean catch
    for z in W.ZONES:
        for typ in ("CO2", "gravid"):
            grp = [s for s in rows if s["zone"] == z and s["trap_type"] == typ]
            if grp:
                m = sum(s["factor"] for s in grp) / len(grp)
                for s in grp:
                    s["factor"] /= m
    return rows


def nights():
    """(year, week, set date) for every scheduled night."""
    out = []
    for year, weeks in E.YEARS.items():
        for wk in weeks:
            for d in W.week_nights(year, wk):
                if year == 2026 and d < W.SEASON_2026[0]:
                    continue
                out.append((year, wk, d))
    return out


def status_for(g, site, d, year):
    if year == 2026 and d == W.HOLIDAY_WEEK_MONDAY and g.random() < 0.3:
        return "NS"
    u = g.random()
    if site["trap_type"] == "gravid":
        return "BAT" if u < 0.012 else ("STOLEN" if u < 0.016 else "OK")
    if u < 0.011:
        return "FAN"
    if u < 0.019:
        return "CO2"
    if u < 0.027:
        return "BAT"
    if u < 0.030:
        return "STOLEN"
    return "OK"


FAIL_SCALE = {"FAN": 0.12, "CO2": 0.3, "BAT": 0.18}
# week-32 2026 trap-nights fixed as they happened: the only failures that week
WEEK32_FAIL = {("North Bottoms", 4, 0): "FAN", ("Airport East", 2, 1): "BAT", ("Coulee Hills", 6, 0): "CO2"}
# early-June 2026 failures in zones whose draw had none in the nights the 22 June re-import copied
JUNE_FAIL = {("North Bottoms", 3, dt.date(2026, 6, 2)): "BAT", ("Maple Ridge", 5, dt.date(2026, 6, 9)): "FAN",
             ("Airport East", 7, dt.date(2026, 6, 9)): "CO2", ("South Prairie", 4, dt.date(2026, 6, 2)): "BAT",
             ("Maple Ridge", 2, dt.date(2026, 6, 2)): "CO2", ("South Prairie", 9, dt.date(2026, 6, 9)): "FAN"}


def catch_rows(g, site, d, year, status):
    """Catches of one trap-night: (species, sex, count) for every species with a count."""
    rows = []
    if status in ("NS", "STOLEN"):
        return rows
    scale = FAIL_SCALE.get(status, 1.0)
    species = list(W.VECTORS) + list(E.OTHER_SPECIES)
    for sp in species:
        mu = E.expected_catch(site, sp, d, year) * scale
        n = E.draw_catch(g, mu)
        if n:
            rows.append((sp, "F", n))
        if sp == "CXTA" and site["trap_type"] == "CO2":
            m = int(g.poisson(0.04 * mu))
            if m:
                rows.append((sp, "M", m))
    if year != 2026 or d < dt.date(2026, 8, 1):
        cx = int(g.poisson(0.35)) if site["trap_type"] == "CO2" else 0
        if cx:
            rows.append(("CXSP", "F", cx))
    return rows


def pools_from(g, site, d, year, catch, lab):
    """Split each vector species' females into pools of at most the laboratory's size and test them: a pool with an
    infected female returns a cycle threshold, 35 or under positive, 35 to 38 inconclusive and retested."""
    out = []
    mx = W.POOL_MAX[lab]
    for sp, sex, n in catch:
        if sex != "F" or sp not in W.VECTORS:
            continue
        p = E.infection(site["zone"], sp, d, year) / 1000.0
        if site["trap_type"] == "gravid":
            p = min(0.12, p * E.GRAVID_RATIO[site["zone"]][0 if sp == "CXTA" else 1])
        sizes = [mx] * (n // mx) + ([n % mx] if n % mx else [])
        for k in sizes:
            inf = int(g.binomial(k, p))
            rec = dict(species=sp, females=k, infected=inf, ct=None, result="NEG", ct_txt="Undetermined", final="NEG")
            if inf:
                ct = float(min(max(31.4 - 2.0 * math.log2(inf) + g.normal(0, 1.8), 18.5), 37.9))
                rec["ct"] = ct
                if ct <= 35.0:
                    rec.update(result="POS", ct_txt="%.1f" % ct, final="POS")
                else:
                    r = ct - 1.4 + g.normal(0, 0.9)
                    rec.update(result="INC", ct_txt="%.1f" % ct, retest_ct=r, final="POS" if r <= 35.0 else "NEG")
            out.append(rec)
    return out


def simulate():
    S = sites()
    by_zone_site = {}
    for s in S:
        by_zone_site.setdefault((s["zone"], s["trap_type"]), []).append(s)
    tn, catches, pools = [], [], []
    tn_id = 1
    crews = W.CREWS
    for (year, wk, d) in nights():
        for z in W.ZONES:
            for typ in ("CO2", "gravid"):
                grp = by_zone_site.get((z, typ), [])
                for k, s in enumerate(grp):
                    g = W.rng("night", s["site_id"], d.isoformat(), W.SALT.get(z, 0))
                    if year == 2026 and wk == 32:
                        st = WEEK32_FAIL.get((z, k, 0 if d.weekday() == 0 else 1), "OK") if typ == "CO2" else "OK"
                    else:
                        st = status_for(g, s, d, year)
                        if typ == "CO2" and st == "OK":
                            st = JUNE_FAIL.get((z, k, d), st)
                    rec = dict(tn_id=None, site_id=s["site_id"], zone=z, trap_type=typ, set_date=d, pickup_date=d + DAY,
                               status=st, crew=crews[(W.ZONES.index(z) + k + d.toordinal()) % len(crews)], year=year,
                               week=wk, origin="field")
                    rows = catch_rows(g, s, d, year, st)
                    lab = W.lab_of(z)
                    pl = pools_from(g, s, d, year, rows, lab)
                    tn.append(rec)
                    catches.append(rows)
                    for p in pl:
                        p.update(site_id=s["site_id"], zone=z, trap_type=typ, collected=d + DAY, lab=lab, year=year, week=wk)
                    pools.append(pl)
    # Maple Ridge's enhanced trapping after its first positive pool: extra Wednesday and Thursday nights
    for d in W.ENHANCED:
        for k, s in enumerate(by_zone_site[("Maple Ridge", "CO2")]):
            g = W.rng("enhanced", s["site_id"], d.isoformat())
            rec = dict(tn_id=None, site_id=s["site_id"], zone="Maple Ridge", trap_type="CO2", set_date=d,
                       pickup_date=d + DAY, status="OK", crew=crews[k % len(crews)], year=2026, week=W.mmwr_week(d),
                       origin="enhanced")
            rows = catch_rows(g, s, d, 2026, "OK")
            pl = pools_from(g, s, d, 2026, rows, "district")
            for p in pl:
                p.update(site_id=s["site_id"], zone="Maple Ridge", trap_type="CO2", collected=d + DAY, lab="district",
                         year=2026, week=W.mmwr_week(d))
            tn.append(rec)
            catches.append(rows)
            pools.append(pl)
    # Maple Ridge's first positive pool of the season, from the night of 2 June: the fullest Culex tarsalis pool that
    # night held one infected female
    zf, df = W.FIRST_POSITIVE
    cand = [p for i, pl in enumerate(pools) for p in pl if tn[i]["zone"] == zf and tn[i]["set_date"] == df and
            tn[i]["trap_type"] == "CO2" and p["species"] == "CXTA"]
    first = max(cand, key=lambda p: (p["females"], p["site_id"]))
    first.update(infected=max(1, first["infected"]), ct=33.6, result="POS", ct_txt="33.6", final="POS")
    # order of entry: the bulk migration (2024, 2025 and 2026 to 14 June) in date order, then the new app from 15 June,
    # with the 22 June re-import of the legacy system's 1 to 14 June nights (keyed by pickup date) in between
    order = sorted(range(len(tn)), key=lambda i: (tn[i]["set_date"], W.ZONES.index(tn[i]["zone"]), tn[i]["site_id"]))
    migrated = [i for i in order if tn[i]["set_date"] <= W.LEGACY_END]
    app = [i for i in order if tn[i]["set_date"] > W.LEGACY_END]
    copies = []
    for i in migrated:
        r = tn[i]
        # the second load of 22 June brought back the nights the first load dropped, the Tuesdays of 2 and 9 June,
        # and keyed them by the morning the traps were picked up
        if r["year"] == 2026 and r["origin"] == "field" and r["set_date"].weekday() == 1:
            c = dict(r)
            c.update(set_date=r["pickup_date"], pickup_date=r["pickup_date"] + DAY, origin="reimport")
            copies.append((c, catches[i]))
    seq = 1
    final_tn, final_catch, final_pools = [], [], []
    app_before = [i for i in app if tn[i]["set_date"] < W.REIMPORT]
    app_after = [i for i in app if tn[i]["set_date"] >= W.REIMPORT]
    for i in migrated + app_before:
        tn[i]["tn_id"] = seq
        seq += 1
        final_tn.append(tn[i])
        final_catch.append(catches[i])
        final_pools.append(pools[i])
    for c, rows in copies:
        c["tn_id"] = seq
        seq += 1
        final_tn.append(c)
        final_catch.append(rows)
        final_pools.append([])
    for i in app_after:
        tn[i]["tn_id"] = seq
        seq += 1
        final_tn.append(tn[i])
        final_catch.append(catches[i])
        final_pools.append(pools[i])
    return dict(sites=S, tn=final_tn, catches=final_catch, pools=final_pools)


def number_pools(sim):
    """Sample numbers in the order each laboratory received them."""
    flat = []
    for i, pl in enumerate(sim["pools"]):
        for p in pl:
            p["tn_index"] = i
            flat.append(p)
    flat.sort(key=lambda p: (p["collected"], p["lab"], p["site_id"], p["species"]))
    count = {}
    for p in flat:
        key = (p["lab"], p["year"])
        count[key] = count.get(key, 0) + 1
        n = count[key]
        p["sample_no"] = ("%02d-%04d" % (p["year"] % 100, n)) if p["lab"] == "district" else ("RCPHL-%02d-%04d" % (p["year"] % 100, n))
    return flat


DB = "rcvcd_surveillance_2024_2026.sqlite"
TRAP_TYPE = {"CO2": "CO2", "gravid": "GRAVID"}
LAB_CODE = {"district": "RCVCD", "county": "RCPHL"}


def _entered(tn):
    """When each trap-night record was created: legacy records keep their legacy entry time through the 15 June
    migration, the field app stamps the pickup morning, and the 22 June re-import stamps the import run."""
    out = {}
    k = 0
    for r in tn:
        if r["origin"] == "reimport":
            t = dt.datetime(2026, 6, 22, 14, 3, 11) + dt.timedelta(seconds=2 * k)
            k += 1
        else:
            g = W.rng("entered", r["site_id"], r["set_date"].isoformat(), r["origin"])
            base = dt.datetime.combine(r["pickup_date"], dt.time(9, 0))
            t = base + dt.timedelta(minutes=int(g.integers(0, 330)), seconds=int(g.integers(0, 60)))
        out[r["tn_id"]] = t
    return out


def write_db(path, sim, flat):
    """The district's field database as extracted at 08:20 on 17 August 2026."""
    import os
    import sqlite3
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    con.execute("PRAGMA page_size = 4096")
    cur = con.cursor()
    cur.executescript("""
        CREATE TABLE sites (site_id TEXT PRIMARY KEY, trap_type TEXT NOT NULL, zone TEXT NOT NULL, habitat TEXT,
            section TEXT NOT NULL, latitude REAL, longitude REAL, in_service_from TEXT);
        CREATE TABLE trap_nights (tn_id INTEGER PRIMARY KEY, site_id TEXT NOT NULL REFERENCES sites(site_id),
            set_date TEXT NOT NULL, pickup_date TEXT NOT NULL, status TEXT NOT NULL, crew TEXT, entered TEXT NOT NULL);
        CREATE TABLE catches (tn_id INTEGER NOT NULL REFERENCES trap_nights(tn_id), species TEXT NOT NULL,
            sex TEXT NOT NULL, count INTEGER NOT NULL);
        CREATE TABLE pools (pool_id TEXT PRIMARY KEY, tn_id INTEGER NOT NULL REFERENCES trap_nights(tn_id),
            species TEXT NOT NULL, females INTEGER NOT NULL, lab TEXT NOT NULL, sent TEXT NOT NULL);
        CREATE TABLE pool_tests (pool_id TEXT NOT NULL REFERENCES pools(pool_id), test_no INTEGER NOT NULL,
            tested TEXT NOT NULL, result TEXT NOT NULL, ct REAL);
        CREATE TABLE species (code TEXT PRIMARY KEY, name TEXT NOT NULL, pooled_for_testing TEXT NOT NULL);
        CREATE TABLE status_codes (code TEXT PRIMARY KEY, description TEXT NOT NULL);
    """)
    for s in sorted(sim["sites"], key=lambda s: s["site_id"]):
        cur.execute("INSERT INTO sites VALUES (?,?,?,?,?,?,?,?)",
                    (s["site_id"], TRAP_TYPE[s["trap_type"]], s["zone"], s["habitat"], s["section"], s["lat"], s["lon"],
                     s["active_from"].isoformat()))
    ent = _entered(sim["tn"])
    for r, rows in zip(sim["tn"], sim["catches"]):
        cur.execute("INSERT INTO trap_nights VALUES (?,?,?,?,?,?,?)",
                    (r["tn_id"], r["site_id"], r["set_date"].isoformat(), r["pickup_date"].isoformat(), r["status"],
                     r["crew"], ent[r["tn_id"]].strftime("%Y-%m-%d %H:%M:%S")))
        for sp, sex, n in rows:
            cur.execute("INSERT INTO catches VALUES (?,?,?,?)", (r["tn_id"], sp, sex, n))
    for p in sorted(flat, key=lambda p: (p["lab"], p["sample_no"])):
        tn = sim["tn"][p["tn_index"]]
        sent = p["collected"] + dt.timedelta(days=1 if p["lab"] == "county" else 0)
        cur.execute("INSERT INTO pools VALUES (?,?,?,?,?,?)",
                    (p["sample_no"], tn["tn_id"], p["species"], p["females"], LAB_CODE[p["lab"]], sent.isoformat()))
        if keyed(p):
            for t in tests_of(p):
                cur.execute("INSERT INTO pool_tests VALUES (?,?,?,?,?)", (p["sample_no"],) + t)
    for code, name in W.SPECIES.items():
        cur.execute("INSERT INTO species VALUES (?,?,?)", (code, name, "Y" if code in W.VECTORS else "N"))
    for code, desc in W.STATUS.items():
        cur.execute("INSERT INTO status_codes VALUES (?,?)", (code, desc))
    con.commit()
    cur.execute("VACUUM")
    con.close()


def keyed(p):
    """The district keys the county laboratory's results from its weekly report on the Monday after; the week-32
    report (14 August) was not yet keyed at the extract."""
    return not (p["lab"] == "county" and p["year"] == 2026 and p["week"] == 32)


def tests_of(p):
    """(test_no, tested, result, ct) for each RT-PCR run on a pool."""
    lag = 3 if p["lab"] == "district" else 2
    first = p["collected"] + dt.timedelta(days=lag)
    out = [(1, first.isoformat(), p["result"], None if p["ct"] is None else round(p["ct"], 1))]
    if p["result"] == "INC":
        r = p["retest_ct"]
        res = "POS" if p["final"] == "POS" else "NEG"
        out.append((2, (first + dt.timedelta(days=1)).isoformat(), res, round(r, 1) if r <= 38.0 else None))
    return out
