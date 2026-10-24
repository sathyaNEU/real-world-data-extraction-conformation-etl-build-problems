"""task279 records: the simulated polder units written out as the board's, the laboratories' and the contractors' files.

Nothing here changes a simulated column. Point codes, coordinates, coring and survey dates, levels, the levelling grid,
the dipwell hydrology, the register, the parcels and the weather come from the records layer's own random streams, so
the world the seed search chose is the world the files describe."""
from __future__ import annotations

import csv
import datetime as dt
import math

import numpy as np

import common as K
import world as W

HYD_START, HYD_END = dt.date(2014, 4, 1), dt.date(2026, 3, 31)


def write_csv(path, head, rows, delimiter=","):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, delimiter=delimiter, lineterminator="\r\n")
        wr.writerow(head)
        wr.writerows(rows)


def rng(seed, k):
    return np.random.default_rng([seed, k])


def nl(x, nd):
    """A number as a Dutch export writes it: comma decimals."""
    return ("%.*f" % (nd, x)).replace(".", ",")


def workdays(rg, start, end, n):
    days = [start + dt.timedelta(d) for d in range((end - start).days + 1)]
    days = [d for d in days if d.weekday() < 5]
    idx = np.sort(rg.choice(len(days), n, replace=False))
    return [days[i] for i in idx]


class Records:
    def __init__(self, seed=K.SEED, w=None):
        self.seed = seed
        self.w = w or W.World(seed)
        self._units()
        self._points()

    # ------------------------------------------------------------------------------------------------ the units
    def _units(self):
        r = rng(self.seed, 1)
        self.unit = {}
        cx, cy = 113400.0, 445600.0
        for i, code in enumerate(K.UNIT_CODES):
            p = self.w.units[code]["params"]
            col, row = i % 4, i // 4
            x = cx + col * 2650 + r.uniform(-500, 500)
            y = cy + row * 2100 + r.uniform(-400, 400)
            area = float(r.uniform(160, 430))
            sub = float(r.uniform(-7.1, -5.6))            # top of the Pleistocene sand, m NAP
            self.unit[code] = dict(x=x, y=y, area=area, sub=sub, landuse=p["landuse"], role=p["role"])

    # ---------------------------------------------------------------------------------------- monitoring points
    def _points(self):
        r = rng(self.seed, 2)
        d97 = workdays(r, dt.date(1997, 2, 24), dt.date(1997, 5, 16), len(K.UNIT_CODES))
        d24 = workdays(r, dt.date(2024, 3, 11), dt.date(2024, 5, 30), len(K.UNIT_CODES))
        order97 = r.permutation(len(K.UNIT_CODES))
        order24 = r.permutation(len(K.UNIT_CODES))
        new_no = r.choice(np.arange(301, 699), len(K.UNIT_CODES) * K.POINTS_PER_UNIT, replace=False)
        self.points = []
        k = 0
        for i, code in enumerate(K.UNIT_CODES):
            u = self.unit[code]
            day97 = d97[int(np.where(order97 == i)[0][0])]
            day24 = d24[int(np.where(order24 == i)[0][0])]
            for j, pt in enumerate(self.w.units[code]["points"]):
                ang = r.uniform(0, 2 * math.pi)
                dist = r.uniform(250, 700)
                x96 = round(u["x"] + dist * math.cos(ang), 1)
                y96 = round(u["y"] + dist * math.sin(ang), 1)
                off = r.uniform(0.6, 2.8)
                a2 = r.uniform(0, 2 * math.pi)
                x23, y23 = round(x96 + off * math.cos(a2), 2), round(y96 + off * math.sin(a2), 2)
                c97 = day97 + dt.timedelta(int(j > 1))           # the third point some days the next morning
                c24 = day24 + dt.timedelta(int(j == 2 and r.random() < 0.5))
                thick97 = pt["thick"][K.T97]
                thick24 = pt["thick"][K.T24]
                sub = u["sub"] + r.normal(0, 0.08)
                surf97 = sub + thick97 / 100.0
                surf24 = sub + thick24 / 100.0
                lev97_old = round(surf97 + K.DATUM_OFFSET_M + r.normal(0, 0.003), 3)
                lev24 = round(surf24 + r.normal(0, 0.008), 3)
                self.points.append(dict(
                    unit=code, j=j, pt=pt, code97="VM-%s-%d" % (K.UNIT_PREFIX[code], j + 1),
                    code24="HHLV-VMP-%04d" % int(new_no[k]), x96=x96, y96=y96, x23=x23, y23=y23,
                    cored97=c97, cored24=c24, lev97=lev97_old, lev24=lev24))
                k += 1

    def point_rows(self):
        head = ["unit_code", "unit_name", "point_1997", "point_2024", "x_rd_1996", "y_rd_1996", "x_rd_2023", "y_rd_2023",
                "cored_1997", "cored_2024", "surface_level_1997_m", "surface_level_2024_m", "core_length_1997_cm",
                "core_length_2024_cm"]
        rows = []
        for p in sorted(self.points, key=lambda q: (q["unit"], q["code97"])):
            rows.append([p["unit"], K.UNIT_NAME[p["unit"]], p["code97"], p["code24"], "%.1f" % p["x96"], "%.1f" % p["y96"],
                         "%.2f" % p["x23"], "%.2f" % p["y23"], p["cored97"].isoformat(), p["cored24"].isoformat(),
                         "%.3f" % p["lev97"], "%.3f" % p["lev24"], K.CORE97_DEPTH, K.CORE24_DEPTH])
        return head, rows

    # ------------------------------------------------------------------------------------------------ the cores
    def core97_lines(self):
        """Bodemlab Wageveld's 1997 printout: fixed-width, Dutch, comma decimals, page headers every 56 lines."""
        body = []
        n = 0
        for p in sorted(self.points, key=lambda q: (q["cored97"], q["code97"])):
            bd, loi, c = p["pt"]["m97"]
            for s in range(len(bd)):
                n += 1
                top, bot = s * K.SLICE97, (s + 1) * K.SLICE97
                body.append("97-0412-%04d %-10s %s  %3d - %3d   %6s    %5s     %5s" % (
                    n, p["code97"], p["cored97"].strftime("%d-%m-%Y"), top, bot, nl(bd[s], 3), nl(loi[s], 1),
                    nl(c[s], 1)))
        head = [
            "BODEMLAB WAGEVELD                                               pagina %d",
            "Rapport 97-0412   Hoogheemraadschap van het Lageveen - veenmonitoringsnet, nulmeting 1997",
            "Datum rapport: 14-07-1997          Analist: S. Ulrich",
            "Methoden: droge volumieke massa 105 C (steekring per plak); gloeiverlies 550 C, 4 uur; C-totaal droge verbranding",
            "-------------------------------------------------------------------------------------------",
            "Monsternr    Meetpunt   Bemonsterd   Diepte (cm)  Vol.massa  Gloeiverl.  C-totaal",
            "                                                  g/cm3      % d.s.      % d.s.",
            "-------------------------------------------------------------------------------------------",
        ]
        out = []
        per = 56
        pages = [body[i:i + per] for i in range(0, len(body), per)]
        for i, pg in enumerate(pages):
            out += [head[0] % (i + 1)] + head[1:] + pg
            out.append("")
            out.append("\f" if i < len(pages) - 1 else "Einde rapport 97-0412.  Monsters bewaard tot 31-12-1998.")
        return out

    def core24_rows(self):
        """Gouwlanden Laboratoria's LIMS export: one row a reported sample, semicolons and comma decimals."""
        r = rng(self.seed, 3)
        head = ["sample_id", "project", "point_code", "sampling_date", "depth_top_cm", "depth_bottom_cm",
                "field_description", "dry_bulk_density_kg_m3", "loi_550_pct_dm", "total_c_pct_dm", "total_n_pct_dm",
                "moisture_pct_fm", "analysis_date", "report_no"]
        rows = []
        n = 0
        for p in sorted(self.points, key=lambda q: (q["cored24"], q["code24"])):
            bd, loi, c = p["pt"]["m24"]
            ana = p["cored24"] + dt.timedelta(int(r.integers(9, 31)))
            for s in range(len(bd)):
                n += 1
                ash = 100 - loi[s]
                desc = ("venige klei" if ash > 62 else "kleiig veen" if ash > 38 else
                        "veen, veraard" if s < 2 else "veen" if r.random() < 0.8 else "veen met houtresten")
                cn = float(np.clip(r.normal(17.5 if s < 3 else 24.0, 2.2), 11, 34))
                moist = float(np.clip(100 * (1 - bd[s] / (bd[s] + 0.55 + 0.25 * (s > 3))), 55, 92))
                rows.append(["GL24-%05d" % (31207 + n), "HHLV veenmonitoring 2024", p["code24"],
                             p["cored24"].isoformat(), s * K.SLICE24, (s + 1) * K.SLICE24, desc,
                             "%d" % round(bd[s] * 1000), nl(loi[s], 1), nl(c[s], 2), nl(c[s] / cn, 2), nl(moist, 1),
                             ana.isoformat(), "GL-R24-%04d" % (618 + int((ana - dt.date(2024, 3, 1)).days // 7))])
        return head, rows

    def qc24_rows(self):
        """The laboratory's QC file: duplicate analyses of one sample in twenty and the reference material."""
        r = rng(self.seed, 4)
        head = ["qc_id", "qc_type", "sample_id", "analysis_date", "parameter", "result", "unit", "reference_value",
                "recovery_pct"]
        rows = []
        h, body = self.core24_rows()
        n = 0
        for i, row in enumerate(body):
            if i % 20 == 7:
                for par, col, nd in (("loi_550", 8, 1), ("total_c", 9, 2)):
                    v = float(row[col].replace(",", ".")) * (1 + r.normal(0, 0.01))
                    n += 1
                    rows.append(["QC24-%04d" % n, "duplicate", row[0], row[12], par, "%.*f" % (nd, v), "% dm", "", ""])
        for wk in range(14):
            day = dt.date(2024, 3, 25) + dt.timedelta(7 * wk)
            for par, ref in (("loi_550", 61.4), ("total_c", 33.12)):
                v = ref * (1 + r.normal(0, 0.012))
                n += 1
                rows.append(["QC24-%04d" % n, "reference material ISE-P921", "", day.isoformat(), par, "%.2f" % v,
                             "% dm", "%.2f" % ref, "%.1f" % (100 * v / ref)])
        return head, rows

    # ------------------------------------------------------------------------------------- the levelling grid
    def grid(self):
        """The unit's levelling grid, surveyed in 1997 (spirit levelling on the board's benchmarks, old heights) and in
        2024 (RTK-GNSS, current NAP). A peg lost since 1997 is re-staked at its 1996 coordinates; where that spot now
        lies in a ditch, a yard or a fenced plot the contractor shot the nearest open meadow edge under the same number,
        and those edges carry the spoil of decades of ditch cleaning."""
        if hasattr(self, "_grid"):
            return self._grid
        r = rng(self.seed, 5)
        out = []
        for code in K.UNIT_CODES:
            u = self.unit[code]
            pts = [p for p in self.points if p["unit"] == code]
            surf97 = np.mean([p["lev97"] - K.DATUM_OFFSET_M for p in pts])
            low = np.mean([p["pt"]["lowering"] for p in pts])           # cm, the unit's mean lowering
            n = int(np.clip(round(u["area"] / 8.5), 22, 48))
            side = math.sqrt(u["area"] * 1e4)
            day97 = dt.date(1997, 3, 3) + dt.timedelta(int(r.integers(0, 40)))
            day24 = dt.date(2024, 3, 4) + dt.timedelta(int(r.integers(0, 55)))
            lost = set(r.choice(n, int(r.integers(1, 4)), replace=False))
            cand = [i for i in range(n) if i not in lost]
            moved = set(int(x) for x in r.choice(cand, int(r.integers(3, 6)), replace=False))
            for i in range(n):
                gx = u["x"] - side / 2 + (i % 7 + 0.5) * side / 7 + r.normal(0, 25)
                gy = u["y"] - side / 2 + (i // 7 + 0.5) * side / math.ceil(n / 7) + r.normal(0, 25)
                s97 = surf97 + r.normal(0, 0.07)
                lw = low * (1 + 0.12 * r.normal()) + r.normal(0, 0.5)
                rec = dict(unit=code, gp="MV%s-%03d" % (code[3:], i + 1), x97=round(gx, 1), y97=round(gy, 1),
                           d97=day97 + dt.timedelta(int(i // 16)), l97=round(s97 + K.DATUM_OFFSET_M + r.normal(0, 0.003), 3),
                           moved=i in moved, lost=i in lost, true_low=lw)
                if i in lost:
                    rec.update(x24=None, y24=None, d24=None, l24=None)
                elif i in moved:
                    a = r.uniform(0, 2 * math.pi)
                    dd = r.uniform(14, 55)
                    edge = r.uniform(0.10, 0.26)                        # spoil-raised meadow edge, m
                    rec.update(x24=round(gx + dd * math.cos(a), 2), y24=round(gy + dd * math.sin(a), 2),
                               d24=day24 + dt.timedelta(int(i // 20)),
                               l24=round(s97 - lw / 100 + edge + r.normal(0, 0.008), 3))
                else:
                    a = r.uniform(0, 2 * math.pi)
                    dd = abs(r.normal(0, 0.12))
                    rec.update(x24=round(gx + dd * math.cos(a), 2), y24=round(gy + dd * math.sin(a), 2),
                               d24=day24 + dt.timedelta(int(i // 20)),
                               l24=round(s97 - lw / 100 + r.normal(0, 0.008), 3))
                out.append(rec)
        self._grid = out
        return out

    def grid_rows(self):
        head = ["unit_code", "grid_point", "campaign", "survey_date", "method", "x_rd", "y_rd", "level_m", "height_ref"]
        rows = []
        for g in self.grid():
            rows.append([g["unit"], g["gp"], "1997", g["d97"].isoformat(), "spirit levelling", "%.1f" % g["x97"],
                         "%.1f" % g["y97"], "%.3f" % g["l97"], "board benchmarks, heights of 1995"])
        for g in self.grid():
            if g["l24"] is None:
                continue
            rows.append([g["unit"], g["gp"], "2024", g["d24"].isoformat(), "RTK-GNSS", "%.2f" % g["x24"],
                         "%.2f" % g["y24"], "%.3f" % g["l24"], "NAP"])
        return head, rows

    # ----------------------------------------------------------------------------------------------- dipwells
    def weather(self):
        if hasattr(self, "_wx"):
            return self._wx
        r = rng(self.seed, 6)
        days = [HYD_START + dt.timedelta(d) for d in range((HYD_END - HYD_START).days + 1)]
        doy = np.array([d.timetuple().tm_yday for d in days])
        t = 10.4 + 7.6 * np.sin(2 * np.pi * (doy - 112) / 365.25) + r.normal(0, 2.4, len(days))
        et = np.clip(0.2 + 2.0 * (1 + np.sin(2 * np.pi * (doy - 95) / 365.25)) + r.normal(0, 0.45, len(days)), 0, 5.6)
        wet = r.random(len(days)) < (0.52 + 0.08 * np.cos(2 * np.pi * (doy - 340) / 365.25))
        rain = np.where(wet, r.gamma(0.8, 4.3, len(days)), 0.0)
        self._wx = dict(days=days, t=t, et=et, rain=rain)
        return self._wx

    def dipwells(self):
        if hasattr(self, "_dw"):
            return self._dw
        r = rng(self.seed, K.DW_STREAM)
        wx = self.weather()
        surplus = wx["rain"] - wx["et"]
        anom = np.zeros(len(surplus))
        for i in range(1, len(surplus)):
            anom[i] = 0.965 * anom[i - 1] - 0.9 * surplus[i]
        anom = anom / anom.std() * 7.0
        doy = np.array([d.timetuple().tm_yday for d in wx["days"]])
        season = np.cos(2 * np.pi * (doy - 232) / 365.25)           # +1 in late August, the deepest
        dws = []
        gap_unit = str(r.choice(K.UNIT_CODES))
        for code in K.UNIT_CODES:
            p = self.w.units[code]["params"]
            wsum = p["w2"] if p.get("w2") else p["w1"]
            u = self.unit[code]
            for k in (1, 2):
                glg_target = wsum + 14 + r.normal(0, 4)
                amp = r.uniform(26, 34)
                mu = glg_target - amp - 6
                local = np.zeros(len(doy))
                e = r.normal(0, 1.6, len(doy))
                for i in range(1, len(doy)):
                    local[i] = 0.9 * local[i - 1] + e[i]
                wt = mu + amp * season + anom * (0.8 + 0.4 * r.random()) + local
                wt = np.maximum(wt, 2.0)
                top_now = round(float(r.uniform(0.08, 0.30)), 2)
                rec = dict(unit=code, id="PB%s-%d" % (code[3:], k), x=round(u["x"] + r.normal(0, 260), 1),
                           y=round(u["y"] + r.normal(0, 260), 1), installed=dt.date(2013, 11, 4 + int(r.integers(0, 20))),
                           top_now=top_now, wt=wt, filt=(round(float(r.uniform(1.4, 1.9)), 2)),
                           serial="DV%06d" % int(r.integers(100000, 999999)))
                # the 2013 tubes, bent by mowing year after year, were renewed one by one from 2018 to 2022 with
                # capped tubes set lower
                rec["replaced"] = dt.date(2018, 3, 1) + dt.timedelta(int(r.integers(0, 1700)))
                rec["top_old"] = round(top_now + float(r.uniform(0.18, 0.34)), 2)
                if code == gap_unit and k == 2:
                    rec["gap"] = (dt.date(2022, 6, 8), dt.date(2022, 11, 4))
                else:
                    rec["gap"] = None
                dws.append(rec)
        self._dw = dws
        return dws

    def dipwell_series_rows(self):
        r = rng(self.seed, K.DW_STREAM + 1)
        head = ["dipwell_id", "date_time", "source", "depth_below_tube_top_cm", "remark"]
        rows = []
        wx = self.weather()
        for d in self.dipwells():
            for i, day in enumerate(wx["days"]):
                top = d["top_old"] if (d["replaced"] and day < d["replaced"]) else d["top_now"]
                v = d["wt"][i] + 100 * top
                if not (d["gap"] and d["gap"][0] <= day < d["gap"][1]):
                    rows.append([d["id"], "%s 08:00" % day.isoformat(), "logger", "%.1f" % (v + r.normal(0, 0.4)), ""])
                if day.day in (14, 28):
                    rows.append([d["id"], "%s %02d:%02d" % (day.isoformat(), 9 + int(r.integers(0, 6)),
                                                             int(r.integers(0, 60))), "hand",
                                 "%.0f" % (v + r.normal(0, 0.8)), ""])
        rows.sort(key=lambda x: (x[0], x[1], x[2]))
        return head, rows

    def dipwell_meta_rows(self):
        head = ["dipwell_id", "unit_code", "x_rd", "y_rd", "installed", "tube_top_above_surface_m",
                "filter_bottom_m_below_surface", "logger_serial"]
        rows = [[d["id"], d["unit"], "%.1f" % d["x"], "%.1f" % d["y"], d["installed"].isoformat(), "%.2f" % d["top_now"],
                 "%.2f" % d["filt"], d["serial"]] for d in self.dipwells()]
        return head, rows

    def dipwell_maintenance_rows(self):
        r = rng(self.seed, 9)
        head = ["date", "dipwell_id", "action", "note", "by"]
        rows = []
        for d in self.dipwells():
            for yr in range(2014, 2026):
                if r.random() < 0.55:
                    day = dt.date(yr, 1, 1) + dt.timedelta(int(r.integers(30, 330)))
                    rows.append([day.isoformat(), d["id"], "cleaned and flushed", "", "YG"])
            if r.random() < 0.35:
                day = dt.date(2017, 1, 1) + dt.timedelta(int(r.integers(0, 2900)))
                rows.append([day.isoformat(), d["id"], "logger battery replaced", "", "YG"])
            if d["replaced"]:
                rows.append([d["replaced"].isoformat(), d["id"], "tube replaced",
                             "old tube bent by mowing; new capped tube set at the same spot, top %.2f m above "
                             "surface (was %.2f m)" % (d["top_now"], d["top_old"]), "YG"])
            if d["gap"]:
                rows.append([d["gap"][1].isoformat(), d["id"], "logger replaced",
                             "logger found flooded; no logger data since %s" % d["gap"][0].strftime("%d %B %Y").lstrip("0"),
                             "YG"])
        rows.sort()
        return head, rows

    def weather_rows(self):
        wx = self.weather()
        head = ["date", "precipitation_mm", "makkink_et_mm", "t_mean_c"]
        return head, [[d.isoformat(), "%.1f" % p, "%.1f" % e, "%.1f" % t]
                      for d, p, e, t in zip(wx["days"], wx["rain"], wx["et"], wx["t"])]

    # ------------------------------------------------------------------------------- register, parcels, soils
    def register(self):
        if hasattr(self, "_reg"):
            return self._reg
        r = rng(self.seed, 10)
        stations = ["gemaal De Lange Hoef", "gemaal Wageveld", "gemaal Kortewaard", "gemaal Oostzijde"]
        units, changes = [], []
        for i, code in enumerate(K.UNIT_CODES):
            p = self.w.units[code]["params"]
            pts = [q for q in self.points if q["unit"] == code]
            surf24 = float(np.mean([q["lev24"] for q in pts]))
            wsum = p["w2"] if p.get("w2") else p["w1"]
            summer = round(surf24 - (wsum / 100.0 - 0.12) + r.normal(0, 0.02), 2)
            winter = round(summer - float(r.choice([0.05, 0.10, 0.10, 0.15])), 2)
            soil = ("clayey peat" if p["ash"] > 0.40 else "peat with clay cover" if p["ash"] > 0.24 else
                    "sedge and wood peat")
            units.append(dict(code=code, name=K.UNIT_NAME[code], area=round(self.unit[code]["area"], 1),
                              landuse=p["landuse"], soil=soil, station=stations[i % 4], summer=summer, winter=winter))
            # the level history the register's change sheet keeps, newest last
            lvl_s, lvl_w = summer, winter
            hist = []
            if p.get("yd"):
                cut = (p["w2"] - p["w1"]) / 100.0
                hist.append((dt.date(p["yd"], 4, 1), "summer", round(lvl_s + cut, 2), lvl_s,
                             "order amendment %d-%02d: freeboard for the farms on request" % (p["yd"] - 1, 11)))
                hist.append((dt.date(p["yd"], 10, 1), "winter", round(lvl_w + cut, 2), lvl_w,
                             "order amendment %d-%02d: freeboard for the farms on request" % (p["yd"] - 1, 11)))
                lvl_s, lvl_w = round(lvl_s + cut, 2), round(lvl_w + cut, 2)
            for yr in (2017, 2003):
                step = round(float(r.uniform(0.04, 0.08)), 2)
                hist.append((dt.date(yr, 4, 1), "summer", round(lvl_s + step, 2), lvl_s,
                             "peilbesluit Lageveen %d: indexation to surface lowering" % yr))
                hist.append((dt.date(yr, 10, 1), "winter", round(lvl_w + step, 2), lvl_w,
                             "peilbesluit Lageveen %d: indexation to surface lowering" % yr))
                lvl_s, lvl_w = round(lvl_s + step, 2), round(lvl_w + step, 2)
            for h in hist:
                changes.append(dict(code=code, date=h[0], season=h[1], old=h[2], new=h[3], reason=h[4]))
        changes.sort(key=lambda c: (c["date"], c["code"], c["season"]))
        self._reg = dict(units=units, changes=changes)
        return self._reg

    def parcel_rows(self):
        r = rng(self.seed, 11)
        head = ["parcel_id", "unit_code", "area_ha", "crop_code", "crop", "farm_id"]
        rows = []
        n = 0
        for code in K.UNIT_CODES:
            u = self.unit[code]
            p = self.w.units[code]["params"]
            left = u["area"] * float(r.uniform(0.905, 0.94))
            maize = 0.38 if "maize" in p["landuse"] else 0.04
            farms = ["LV%04d" % int(x) for x in r.choice(np.arange(1100, 9800), int(r.integers(4, 9)), replace=False)]
            while left > 0.4:
                a = float(min(left, r.gamma(3.0, 1.6)))
                left -= a
                n += 1
                c = r.random()
                crop = ("259", "snijmais") if c < maize else ("265", "grasland, blijvend") if c < 0.93 else \
                    ("331", "grasland, natuurlijk") if c < 0.98 else ("266", "grasland, tijdelijk")
                rows.append(["%09d" % (40123177 + 37 * n), code, "%.2f" % a, crop[0], crop[1], str(r.choice(farms))])
        return head, rows

    def soil_rows(self):
        r = rng(self.seed, 12)
        head = ["unit_code", "soil_unit", "description", "area_share_pct"]
        rows = []
        desc = {"V1": "peat, earthified topsoil, on sedge and wood peat", "V2": "peat with a thin clay cover",
                "V3": "clayey peat", "V4": "peat with clay cover over 40 cm thick", "K1": "river clay over peat"}
        for u in self.register()["units"]:
            main = {"clayey peat": "V3", "peat with clay cover": "V2", "sedge and wood peat": "V1"}[u["soil"]]
            others = [k for k in desc if k != main]
            sh = [float(r.uniform(58, 82))]
            rest = 100 - sh[0]
            picks = [str(x) for x in r.choice(others, 2, replace=False)]
            s2 = float(r.uniform(0.45, 0.8)) * rest
            sh += [s2, rest - s2]
            for k, v in zip([main] + picks, sh):
                rows.append([u["code"], k, desc[k], "%.0f" % v])
        return head, rows
