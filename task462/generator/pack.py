"""Write the pack's data files: the thirteen survey deliveries in their contractors' own formats, the delivery
register, the pile area register, the fuel laboratory's density tests, the port's berth log, the contract register,
the unloader's event log, the plant historian's export, the control room's shift log and the two side files."""
import csv
import datetime as dt
import os

import numpy as np

import ops as O
import world as W
import yard as Y

D = dt.timedelta


def write_csv(path, header, rows, delimiter=","):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=delimiter, lineterminator="\r\n")
        w.writerow(header)
        n = 0
        for r in rows:
            w.writerow(r)
            n += 1
    return n


# ------------------------------------------------------------------------------------------------ surveys
def write_asc(path, m):
    X, Yg, z = Y.render_a(m)
    ny, nx = z.shape
    lines = ["ncols        %d" % nx, "nrows        %d" % ny, "xllcorner    %.3f" % W.X0, "yllcorner    %.3f" % W.Y0,
             "cellsize     %.3f" % W.A_CELL, "NODATA_value -9999"]
    for j in range(ny - 1, -1, -1):
        row = z[j]
        lines.append(" ".join("-9999" if np.isnan(v) else "%.3f" % v for v in row))
    with open(path, "w", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")
    return ny * nx


def fi_num(v, nd):
    return ("%.*f" % (nd, v)).replace(".", ",")


def write_xyz(path, m):
    E, N, z = Y.render_b(m)
    order = np.lexsort((E, N))
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write("Itä;Pohjoinen;Korkeus\r\n")
        for i in order:
            f.write("%s;%s;%s\r\n" % (fi_num(E[i], 2), fi_num(N[i], 2), fi_num(z[i], 3)))
    return len(order)


def survey_rows():
    rng = np.random.default_rng(W.SEED + 300)
    rows = []
    for m, (d, a, b) in enumerate(W.SURVEYS):
        A = m < W.B_FROM
        delivered = dt.date.fromisoformat(d) + D(days=int(rng.integers(2, 6)))
        rows.append([d, a, b, W.CONTRACTOR_A if A else W.CONTRACTOR_B, W.survey_file(m),
                     "SVL plant grid" if A else "ETRS-TM35FIN", "N60" if A else "N2000",
                     "%.1f" % (W.A_CELL if A else W.B_STEP), int(rng.integers(5, 9)),
                     "%.3f" % rng.uniform(0.009, 0.019), delivered.isoformat()])
    return rows


def area_rows():
    out = []
    for (name, cx, cy, L, Wd, *_rest) in W.PILES:
        coal = _rest[-1]
        xs = [cx - L / 2, cx + L / 2, cx + L / 2, cx - L / 2]
        ys = [cy - Wd / 2, cy - Wd / 2, cy + Wd / 2, cy + Wd / 2]
        r = [name, coal]
        for x, y in zip(xs, ys):
            r += ["%.1f" % (W.X0 + x), "%.1f" % (W.Y0 + y)]
        r.append("%.0f" % (L * Wd))
        out.append(r)
    return out


def density_rows():
    out = []
    for k, (d, coal, area, rho) in enumerate(W.DENSITY_TESTS):
        kg = d < W.DENSITY_UNIT_SWITCH
        out.append(["PT-%s-%02d" % (d[:4], k + 3), d, coal, area, "in-pile, 1 m3 excavation, three pits",
                    ("%.0f" % (rho * 1000)) if kg else ("%.3f" % rho), "kg/m3" if kg else "t/m3"])
    return out


# ------------------------------------------------------------------------------------------------ the port and the plant
IMO = {}


def imo_number(name, rng):
    if name not in IMO:
        while True:
            d = [int(v) for v in rng.integers(0, 10, 6)]
            d[0] = int(rng.integers(9, 10)) if rng.random() < 0.8 else 8
            chk = sum(a * w for a, w in zip(d, (7, 6, 5, 4, 3, 2))) % 10
            num = "".join(map(str, d)) + str(chk)
            if num not in IMO.values():
                IMO[name] = num
                break
    return IMO[name]


def utc(t):
    return t.astimezone(W.UTC).strftime("%Y-%m-%dT%H:%MZ")


def berth_rows(x):
    rng = np.random.default_rng(W.SEED + 400)
    IMO.clear()
    contracts = {c[0]: c for c in W.CONTRACTS}
    order = rng.permutation(len(W.VESSELS))
    rows = []
    for c in x["calls"]:
        con = contracts[c["contract"]]
        vessel = W.VESSELS[order[c["k"] % len(W.VESSELS)]]
        commenced, completed = O.at(c["commence"]), O.at(c["complete"])
        arrived = commenced - D(hours=float(rng.uniform(5, 30)))
        berthed = commenced - D(minutes=int(rng.integers(55, 170)))
        departed = completed + D(minutes=int(rng.integers(80, 260)))
        outturn = c["size"] * (1 + rng.normal(0, 0.0032))
        bl = outturn * (1 + rng.normal(0.0018, 0.0041))
        bl_date = (arrived - D(days=int(rng.integers(3, 6) if con[4] == "Gdansk" else rng.integers(14, 23)))).date()
        port_call = "%s%04d" % ("PC" + str(commenced.year)[2:], 311 + c["k"] * 17 + int(rng.integers(0, 9)))
        rows.append([port_call, vessel, imo_number(vessel, rng), ["MT", "LR", "PA", "MH", "BS", "FI"][c["k"] % 6],
                     con[1], c["contract"], "STEAM COAL IN BULK", con[4].upper(), bl_date.isoformat(),
                     "%.3f" % bl, utc(arrived), utc(berthed), utc(commenced), utc(completed), utc(departed),
                     "%.3f" % outturn])
    return rows


def contract_rows():
    qty = {"RL-HK-2025-03": 260000, "RL-HK-2026-01": 160000, "RL-HK-2026-02": 175000, "RL-HK-2026-03": 300000,
           "RL-HK-2026-07": 25000, "RL-HK-2026-09": 32000}
    period = {"RL-HK-2025-03": ("2025-01-01", "2025-12-31"), "RL-HK-2026-07": ("2026-07-01", "2026-08-31"),
              "RL-HK-2026-09": ("2026-10-15", "2026-11-30")}
    out = []
    for (no, cp, coal, desc, port) in W.CONTRACTS:
        a, b = period.get(no, ("2026-01-01", "2026-12-31"))
        out.append([no, cp, coal, desc, port, qty[no], a, b])
    return out


def gu1_rows(x):
    out = []
    for c in x["calls"]:
        for t, ev, why in c["events"]:
            out.append([O.at(t).strftime("%Y-%m-%d %H:%M:%S%z")[:-2] + ":" + O.at(t).strftime("%z")[-2:], "GU-1",
                        ev, why])
    return out


def historian_rows(x):
    h = O.historian(x)
    n = len(h["CV-01"])
    t0 = O.T0.astimezone(W.UTC)
    for tag, name in (("CV-01", "SVL.CV01.WT15"), ("CV-21", "SVL.CV21.WT15")):
        v = h[tag]
        for i in range(n):
            yield [name, (t0 + D(minutes=15 * i)).strftime("%Y-%m-%dT%H:%M:%SZ"), "%.1f" % v[i]]


def shift_rows(x):
    c01, c21 = O.totalisers(x)
    out = []
    day = O.T0.date()
    while day < O.T1.date():
        for code, h in (("N", 0), ("D", 8), ("E", 16)):
            t = dt.datetime.combine(day, dt.time(h), W.FI)
            i = O.mi(t)
            v01 = c01[i - 1] if i > 0 else 4218553.0
            v21 = c21[i - 1] if i > 0 else 3907112.4
            out.append([day.isoformat(), code, "%02d:00" % h, "%.1f" % v01, "%.1f" % v21])
        day += D(days=1)
    return out


def bunker_rows():
    rng = np.random.default_rng(W.SEED + 500)
    rows = []
    for b in range(1, 7):
        pct = float(rng.uniform(38, 91))
        rows.append(["2026-12-16 09:30", "BH-%d" % b, ["KH-COL", "KH-POL", "KH-USA"][b % 3], "%.0f" % pct,
                     "%.0f" % (pct / 100 * 690)])
    return rows


def analysis_rows(x):
    rng = np.random.default_rng(W.SEED + 600)
    contracts = {c[0]: c for c in W.CONTRACTS}
    rows = []
    for c, b in zip(x["calls"], berth_rows(x)):
        coal = contracts[c["contract"]][2]
        base = {"KH-COL": (11.8, 9.4, 35.1, 0.62, 25.3), "KH-USA": (8.6, 10.9, 33.4, 1.04, 26.2),
                "KH-POL": (10.4, 12.6, 30.2, 0.81, 24.1)}[coal]
        rows.append([b[0], b[1], O.at(c["commence"]).date().isoformat(), coal,
                     "%.1f" % (base[0] + rng.normal(0, 0.6)), "%.1f" % (base[1] + rng.normal(0, 0.5)),
                     "%.1f" % (base[2] + rng.normal(0, 0.7)), "%.2f" % (base[3] + rng.normal(0, 0.05)),
                     "%.2f" % (base[4] + rng.normal(0, 0.25))])
    return rows


def write_data(out, x):
    f = lambda k: os.path.join(out, W.FILES[k])
    n = {}
    for m in range(len(W.SURVEYS)):
        key = "survey%02d" % m
        n[key] = write_asc(f(key), m) if m < W.B_FROM else write_xyz(f(key), m)
    n["deliveries"] = write_csv(f("deliveries"), ["survey_date", "flight_start", "flight_end", "contractor", "file",
                                                  "coordinates", "heights", "grid_m", "checkpoints",
                                                  "checkpoint_rmse_m", "delivered"], survey_rows())
    n["areas"] = write_csv(f("areas"), ["pile_area", "fuel_code", "x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4",
                                        "area_m2"], area_rows())
    n["density"] = write_csv(f("density"), ["test_no", "sampled", "fuel_code", "pile_area", "method", "bulk_density",
                                            "unit"], density_rows())
    n["berth"] = write_csv(f("berth"), ["port_call", "vessel", "imo", "registry", "shipper", "buyer_contract", "cargo",
                                        "load_port", "bl_date", "bl_tonnes", "arrived", "berthed", "commenced",
                                        "completed", "departed", "outturn_tonnes"], berth_rows(x))
    n["contracts"] = write_csv(f("contracts"), ["contract", "counterparty", "fuel_code", "description", "load_port",
                                                "contract_tonnes", "valid_from", "valid_to"], contract_rows())
    n["gu1"] = write_csv(f("gu1"), ["timestamp", "unit", "event", "reason"], gu1_rows(x))
    n["historian"] = write_csv(f("historian"), ["tag", "timestamp", "value"], historian_rows(x))
    n["shiftlog"] = write_csv(f("shiftlog"), ["date", "shift", "reading_time", "CV-01_totaliser_t",
                                              "CV-21_totaliser_t"], shift_rows(x))
    n["bunkers"] = write_csv(f("bunkers"), ["reading_time", "bunker", "fuel_code", "level_pct", "tonnes"],
                             bunker_rows())
    n["analyses"] = write_csv(f("analyses"), ["port_call", "vessel", "sampled", "fuel_code", "total_moisture_pct",
                                              "ash_ad_pct", "volatile_ad_pct", "sulphur_ad_pct", "ncv_ar_mj_kg"],
                              analysis_rows(x))
    return n
