"""Write the pack under target/ from the simulated truth, each file the way its producing system writes it: the
company's CFI database (four cycles), the contract crew's 2026 export and its September height revisit, the plot
register, the stand table, the species list, the documents and two operations files."""
import csv
import io
import math
import os
import shutil
import sqlite3

import numpy as np

import world as W


def _csv(path, header, rows, pre=None, crlf=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    buf = io.StringIO()
    end = "\r\n" if crlf else "\n"
    for line in pre or []:
        buf.write(line + end)
    wr = csv.writer(buf, lineterminator=end)
    if header:
        wr.writerow(header)
    n = 0
    for r in rows:
        wr.writerow(r)
        n += 1
    open(path, "w", newline="", encoding="utf-8").write(buf.getvalue())
    return n


def _tn(rng, sd, cap):
    return float(np.clip(rng.normal(0, sd), -cap, cap))


def _az(rng, az):
    return int(round((az + _tn(rng, 0.6, 1.2)) % 360)) % 360


def _dist(rng, d):
    return round(max(0.3, d + _tn(rng, 0.2, 0.4)), 1)


def _status26(t):
    if not t.get("alive21"):
        return []
    if t["cut"]:
        return ["C"]
    if t["dies"]:
        return ["D" if t["found_dead"] else "M"]
    if t["tagloss"] == "retag":
        return ["M", "N"]
    if t["tagloss"] == "dup":
        return ["L", "N"]
    return ["L"]


def database(path, x):
    """The company's FieldCruise backend, cycles 2006 to 2021: the stem map once per tree, measurements per cycle."""
    rng = np.random.default_rng(W.SEED + 7)
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.executescript("""
        PRAGMA page_size = 4096;
        CREATE TABLE cycle (cycle_yr INTEGER PRIMARY KEY, field_start TEXT, field_end TEXT, collector TEXT, crew TEXT,
                            azimuth_ref TEXT);
        CREATE TABLE plot (plot_no INTEGER PRIMARY KEY, est_cycle INTEGER, radius_ft REAL, centre_monument TEXT);
        CREATE TABLE plot_visit (plot_no INTEGER, cycle_yr INTEGER, visit_date TEXT, crew TEXT,
                                 PRIMARY KEY (plot_no, cycle_yr));
        CREATE TABLE tree (tag INTEGER PRIMARY KEY, plot_no INTEGER, spp TEXT, azimuth INTEGER, dist_ft REAL,
                           first_cycle INTEGER);
        CREATE TABLE tree_meas (tag INTEGER, cycle_yr INTEGER, dbh_in REAL, status TEXT, cond INTEGER,
                                merch_logs REAL, cull_pct INTEGER, PRIMARY KEY (tag, cycle_yr));
    """)
    cur.executemany("INSERT INTO cycle VALUES (?,?,?,?,?,?)", [
        (2006, "2006-06-12", "2006-10-06", "FieldCruise 3.1", "CFTC inventory crew", "true (declination set on compass)"),
        (2011, "2011-06-20", "2011-09-30", "FieldCruise 3.4", "CFTC inventory crew", "true (declination set on compass)"),
        (2016, "2016-06-06", "2016-09-23", "FieldCruise 4.0", "CFTC inventory crew", "true (declination set on compass)"),
        (2021, "2021-06-14", "2021-10-01", "FieldCruise 4.2", "CFTC inventory crew", "true (declination set on compass)")])
    mons = ["rebar and cap", "rebar and cap", "iron pipe", "rebar and cap, witness tree"]
    cur.executemany("INSERT INTO plot VALUES (?,?,?,?)",
                    [(p["plot"], p["est"], W.PLOT_R, mons[int(rng.integers(0, 4))]) for p in x["plots"]])
    import datetime as dt
    visits = []
    for yr in W.CYCLES:
        start = {2006: dt.date(2006, 6, 12), 2011: dt.date(2011, 6, 20), 2016: dt.date(2016, 6, 6),
                 2021: dt.date(2021, 6, 14)}[yr]
        d, left = start, int(rng.integers(3, 6))
        for p in x["plots"]:
            if yr < p["est"]:
                continue
            while d.weekday() >= 5:
                d += dt.timedelta(days=1)
            visits.append((p["plot"], yr, d.isoformat(), "CFTC"))
            left -= 1
            if left == 0:
                d += dt.timedelta(days=1)
                left = int(rng.integers(3, 6))
    cur.executemany("INSERT INTO plot_visit VALUES (?,?,?,?)", visits)
    trees, meas = [], []
    est = {p["plot"]: p["est"] for p in x["plots"]}
    for t in x["trees"]:
        if t["tag"] is None:
            continue
        cyc = [c for c in W.CYCLES if c in t["hist"] and t["hist"][c] >= 5.0 and c >= est[t["plot"]]]
        first = min(cyc)
        t["az_db"], t["d_db"] = _az(rng, t["az"]), _dist(rng, t["d"])
        trees.append((t["tag"], t["plot"], W.SPECIES[t["sp"]][0], t["az_db"], t["d_db"], first))
        for c in cyc:
            dbh = round(t["hist"][c] + _tn(rng, 0.03, 0.06), 1)
            if c == 2021:
                t["dbh21_db"] = dbh
            saw = dbh >= 11.0 and t["sp"] not in W.HARDWOOD
            logs = (t["merch21"] if c == 2021 else math.floor(min(6, (6 + 2.6 * dbh + rng.normal(0, 7)) / 16.5) * 2) / 2) \
                if saw else None
            logs = max(1.0, logs) if logs is not None else None
            cull = int(rng.choice([0, 0, 0, 0, 0, 0, 10, 10, 20])) if saw else None
            meas.append((t["tag"], c, dbh, "L", (t["cond"] if c == 2021 else None), logs, cull))
        if not t["alive21"] and t.get("end"):
            meas.append((t["tag"], t["end"], None, t["end_code"], (t["cond"] if t["end"] == 2021 else None), None, None))
    trees.sort()
    meas.sort(key=lambda r: (r[0], r[1]))
    cur.executemany("INSERT INTO tree VALUES (?,?,?,?,?,?)", trees)
    cur.executemany("INSERT INTO tree_meas VALUES (?,?,?,?,?,?,?)", meas)
    con.commit()
    con.close()
    return len(meas)


def remeasurement(out, x):
    """The contract crews' 2026 export and the September height revisit for the smoke week's plots."""
    rng = np.random.default_rng(W.SEED + 11)
    pl = {p["plot"]: p for p in x["plots"]}
    rows, rev = [], []
    for t in sorted(x["trees"], key=lambda t: (t["plot"], t["az"], t["d"])):
        p = pl[t["plot"]]
        codes = ["N"] if (t.get("ingrowth") or t.get("missed")) else _status26(t)
        fia = W.SPECIES[t["sp"]][1]
        conifer = t["sp"] not in W.HARDWOOD
        dbh26 = round(t["dbh26"] + _tn(rng, 0.03, 0.06), 1) if t.get("dbh26") else None
        kind = W.STAND[t["cst"]]["kind"]
        dmg = ""
        if kind == "burn" and t.get("char"):
            dmg = "FIRE"
        elif kind == "wild":
            dmg = "FIRE" if rng.random() < 0.8 else ""
        elif kind == "beetle" and t["sp"] in W.PINES and rng.random() < 0.12:
            dmg = "BB"
        elif rng.random() < 0.03:
            dmg = ["FORK", "BTOP", "LEAN", "FORK"][int(rng.integers(0, 4))]
        shared = None
        for code in codes:
            live = code in ("L", "N")
            tag = t["new_tag"] if (code == "N") else t["tag"]
            if live:
                if shared is None:
                    merch = t["merch"] if (conifer and dbh26 is not None and dbh26 >= 11.0) else None
                    shared = (dbh26, merch, t["cull"] if merch else None)
                d_, m_, c_ = shared
                az, dist = _az(rng, t["az"]), _dist(rng, t["d"])
                smoke = p["date26"] in W.SMOKE_DAYS
                rows.append(["%04d" % p["plot"], "%06d" % tag, fia, "%.1f" % d_, az, "%.1f" % dist, code, t["cond"],
                             "" if (m_ is None or smoke) else m_, "" if c_ is None else c_, dmg, p["crew26"], p["date26"]])
                if smoke and m_ is not None:
                    rev.append(["%04d" % p["plot"], "%06d" % tag, fia, "%.1f" % d_, m_, p["crew26"], p["revisit"]])
            elif code == "D":
                rows.append(["%04d" % p["plot"], "%06d" % tag, fia, "", _az(rng, t["az"]), "%.1f" % _dist(rng, t["d"]),
                             "D", t["cond"], "", "", dmg if dmg == "FIRE" else "", p["crew26"], p["date26"]])
            else:   # M and C: nothing measured
                rows.append(["%04d" % p["plot"], "%06d" % tag, fia, "", "", "", code, t["cond"], "", "", "",
                             p["crew26"], p["date26"]])
    rows.sort(key=lambda r: (r[0], r[1]))
    rev.sort(key=lambda r: (r[0], r[1]))
    n1 = _csv(os.path.join(out, W.FILES["t2026"]),
              ["plot_id", "tag", "species_fia", "dbh_in", "azimuth_deg", "dist_ft", "status", "cond_id",
               "merch_ht_ft", "cull_pct", "damage", "crew", "meas_date"], rows)
    n2 = _csv(os.path.join(out, W.FILES["revisit"]),
              ["plot_id", "tag", "species_fia", "dbh_in", "merch_ht_ft", "crew", "revisit_date"], rev)
    return n1, n2


def stand_table(path, x):
    cnt = {}
    for p in x["plots"]:
        cnt[p["stand"]] = cnt.get(p["stand"], 0) + 1
    rows = []
    for sid, ac, kind in W.STANDS:
        st = W.STAND[sid]
        treat, date = "", ""
        if kind == "burn":
            treat, date = "prescribed underburn", W.BURN_DATES[sid]
        elif kind == "wild":
            treat, date = "wildfire (%s)" % W.WILDFIRE[2], W.WILDFIRE[1]
        elif sid in W.ROAD_2023:
            treat, date = "road right-of-way clearing", "2023-08"
        elif sid in W.THINNED_2012:
            treat, date = "commercial thin", "2012-09"
        rows.append((sid, ac, "Sierra mixed conifer" if st["ftype"] == "mixed" else "ponderosa pine", st["site"],
                     cnt[sid], treat, date))
    return _csv(path, ["stand_id", "acres", "forest_type", "site_class", "cfi_plots", "last_treatment", "treatment_date"],
                rows)


def species(path):
    return _csv(path, ["fia_code", "company_code", "common_name", "scientific_name", "group"],
                [(n, a, c, s, g) for a, n, c, s, g in W.SPECIES])


def ads(path):
    rng = np.random.default_rng(W.SEED + 21)
    rows = []
    k = 0
    for sid, ac, kind in W.STANDS:
        if kind == "beetle" or rng.random() < 0.3:
            k += int(rng.integers(3, 17))
            agent, host = ("western pine beetle", "ponderosa pine") if rng.random() < 0.6 else ("fir engraver", "white fir")
            tpa = round(float(rng.uniform(9, 26) if kind == "beetle" else rng.uniform(0.4, 4.5)), 1)
            rows.append(("R5-25-%04d" % (2600 + k), sid, "2025-07-%02d" % int(rng.integers(8, 25)), agent, host,
                         "moderate" if tpa > 8 else "light", tpa, round(float(rng.uniform(6, 0.6 * ac)), 1)))
    return _csv(path, ["polygon_id", "stand_id", "flight_date", "damage_agent", "host", "severity",
                       "trees_per_acre_affected", "polygon_acres"], rows)


def logs(path):
    rows = [("ponderosa pine", "sawlog 12 in. and up", 418, "Quincy"), ("ponderosa pine", "sawlog 6 to 11 in.", 352, "Quincy"),
            ("sugar pine", "sawlog 12 in. and up", 446, "Quincy"), ("white fir", "sawlog", 301, "Quincy"),
            ("Douglas-fir", "sawlog", 389, "Quincy"), ("incense-cedar", "sawlog", 512, "Loyalton"),
            ("ponderosa pine", "fire-killed sawlog (within 12 months)", 297, "Quincy"),
            ("mixed conifer", "chips and hog fuel (per bone dry ton)", 34, "Loyalton")]
    return _csv(path, ["species", "sort", "usd_per_mbf_delivered", "mill", ], [r for r in rows])


def build_pack(out, x):
    import docs as D
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    for k in W.FILES:
        os.makedirs(os.path.dirname(f(k)), exist_ok=True)
    n = {}
    n["db"] = database(f("db"), x)
    n["t2026"], n["revisit"] = remeasurement(out, x)
    n["stands"] = stand_table(f("stands"), x)
    n["species"] = species(f("species"))
    n["ads"] = ads(f("ads"))
    n["logs"] = logs(f("logs"))
    D.write_register(f("register"), x)
    PP.normalize_ooxml(f("register"), W.FORESTER, W.FORESTER, "2016-05-02T15:10:00Z", "2026-09-29T21:04:12Z",
                       excel=True, company=W.COMPANY)
    stamps = [(D.write_manual, "manual", "D:20260412093011-07'00'"), (D.write_policy, "policy", "D:20260814161544-07'00'"),
              (D.write_burns, "burns", "D:20241203111805-08'00'"), (D.write_fire, "fire", "D:20251017140226-07'00'")]
    for fn, key, st in stamps:
        fn(f(key))
        PP.normalize_pdf(f(key), st.encode(), st.encode())
    return n
