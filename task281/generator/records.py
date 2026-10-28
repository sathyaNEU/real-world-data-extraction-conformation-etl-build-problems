"""The files the utility, its installer and the luminaire maker keep, each written the way its own system writes it.

Every irregularity here is how that system writes its records: the register is a snapshot of the pole inventory on
31 December 2026 (its year is the pole's, its luminaire the one standing that day); the installer's daily logs changed
layout when the installer moved to tablets in January 2023; the legacy work-management system closed at the end of
June 2023 and its open work orders were carried into the successor; the customer portal stamps reports in UTC while
the call centre logs local time."""
import csv
import datetime as dt
import io

import numpy as np

import params as P
from world import EPOCH, d2i, i2d

DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def write_csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(head)
        for r in rows:
            w.writerow(r)


def dtime(x):
    """A fractional day count from EPOCH to a local datetime (minutes)."""
    base = dt.datetime(EPOCH.year, EPOCH.month, EPOCH.day)
    return base + dt.timedelta(minutes=int(round(x * 1440)))


def iso_local(t):
    """A local wall-clock time as the successor system exports it, with its UTC offset."""
    return t.strftime("%Y-%m-%dT%H:%M") + ("-04:00" if eastern_offset(t) == 4 else "-05:00")


def phone_stamp(t):
    """The call centre's log: local time with the zone it was taken in."""
    return t.strftime("%m/%d/%Y %I:%M %p") + (" EDT" if eastern_offset(t) == 4 else " EST")


def eastern_offset(t):
    """UTC offset of US Eastern time at local datetime t (second Sunday of March to first Sunday of November)."""
    y = t.year
    mar = dt.datetime(y, 3, 8)
    while mar.weekday() != 6:
        mar += dt.timedelta(days=1)
    nov = dt.datetime(y, 11, 1)
    while nov.weekday() != 6:
        nov += dt.timedelta(days=1)
    return 4 if mar + dt.timedelta(hours=2) <= t < nov + dt.timedelta(hours=2) else 5


class Records:
    def __init__(self, w):
        self.w = w
        self.rng = np.random.default_rng(np.random.SeedSequence(P.SEED + 7))
        self.idg = np.random.default_rng(np.random.SeedSequence(P.SEED + 19))
        self._index()

    def _index(self):
        w = self.w
        # outages by luminaire, in time order
        self.by_lum = {}
        for i, L in enumerate(w.lum):
            L["_i"] = i
        for o in w.outages:
            if o.get("lum") is not None:
                self.by_lum.setdefault(o["lum"], []).append(o)
        # house numbers for the poles' nearest addresses
        r = self.rng
        self.addr = {}
        used = set()
        for town, pole, street in ([(L["town"], L["pole"], L["street"]) for L in w.lum] +
                                   [(N["town"], N["pole"], N["street"]) for N in w.noncon]):
            while True:
                a = "%d %s" % (int(r.integers(1, 99)) * 20 + int(r.integers(0, 19)), street)
                if (town, a) not in used:
                    break
            used.add((town, a))
            self.addr[pole] = a
        self.pole_year = {L["pole"]: int(r.integers(1969, 2016)) for L in w.lum}
        self.removed_poles = {L["pole"] for L in w.lum
                              if L["exit_type"] == "pole_removed" and L["exit"] <= d2i(P.RECORD_END)}

    # ------------------------------------------------------------------ the register, 31 December 2026
    def register_rows(self):
        w, r = self.w, self.rng
        end = d2i(P.RECORD_END)
        rows = []
        stock_seq = 0
        for i, L in enumerate(w.lum):
            if L["exit_type"] == "pole_removed" and L["exit"] <= end:
                continue                                    # the pole is gone from the inventory
            serial, set_year = L["serial"], self.pole_year[L["pole"]]
            watts = 70 if (L["reprog"] is not None and L["reprog"] <= end) else L["watts"]
            if L["exit"] <= end:                            # a knockdown or a warranty swap: a new luminaire
                stock_seq += 1
                yr = i2d(L["exit"]).year
                serial = "HRX%02d%02d-S%d-%04d" % (yr % 100, i2d(L["exit"]).month, 1 + stock_seq % 3, stock_seq)
                if L["exit_type"] == "knockdown":
                    set_year = yr
            ctl = ("NLC-%s-%03d" % (L["town"], int(r.integers(1, 260))) if P.TOWN_NLC[L["town"]]
                   else "photocontrol")
            rows.append(["SL-%06d" % L["pole"], P.TOWN_NAME[L["town"]], L["street"], self.addr[L["pole"]],
                         set_year, "LED cobra-head", watts, serial, L["phase"], ctl,
                         w.circuit_of.get(L["pole"], "OH")])
        for N in w.noncon:
            k = N["kind"]
            rows.append(["SL-%06d" % N["pole"], P.TOWN_NAME[N["town"]], N["street"], self.addr[N["pole"]],
                         N["set_year"], k.split(" ", 2)[0] + " " + k.split(" ", 2)[2], int(k.split(" ")[1]), "", "",
                         "photocontrol", "OH"])
        rows.sort(key=lambda x: (x[1], x[0]))
        head = ["pole_id", "town", "street", "nearest_address", "pole_set_year", "fixture_type", "lamp_watts",
                "luminaire_serial", "conversion_phase", "control", "feed"]
        return head, rows

    # ------------------------------------------------------------------ the installer's daily logs (by year)
    def install_sheets(self):
        """One sheet a year. 2021 and 2022: the paper-form layout keyed in each evening; from January 2023 the
        tablet app's export, with its own column names and pole identifiers."""
        w, r = self.w, self.rng
        sheets = {}
        for L in sorted(w.lum, key=lambda x: (x["install"], x["crew"], x["pole"])):
            y = L["install"].year
            hps = "HPS %dW %s" % (L["hps_w"], "cobra" if L["hps_w"] <= 150 else "flood")
            if y <= 2022:
                tag = "%d" % L["pole"] if r.random() > 0.04 else "TPL %d" % L["pole"]
                row = [L["install"], L["crew"], L["phase"], P.TOWN_NAME[L["town"]], tag, L["street"], L["serial"],
                       P.CATALOG[L["watts"]], L["lot"], hps, ""]
            else:
                row = [L["install"].strftime("%m/%d/%Y"), L["crew"], L["phase"], P.TOWN_NAME[L["town"]],
                       "SL%06d" % L["pole"], L["street"], L["serial"], P.CATALOG[L["watts"]], L["lot"], hps, ""]
            sheets.setdefault(y, []).append(row)
        head_old = ["Date", "Crew", "Phase", "Municipality", "Pole Tag", "Street", "Luminaire S/N", "Catalog No.",
                    "Lot #", "Removed", "Notes"]
        head_new = ["install_date", "crew_id", "phase", "town", "pole_id", "street", "serial", "catalog",
                    "lot", "removed_fixture", "remarks"]
        # a few remarks crews typed
        for y, rows in sheets.items():
            for row in rows:
                u = r.random()
                if u < 0.004:
                    row[-1] = "arm replaced, rusted"
                elif u < 0.007:
                    row[-1] = "tree trim needed"
                elif u < 0.009:
                    row[-1] = "PE receptacle loose, reseated"
        return {y: (head_old if y <= 2022 else head_new, rows) for y, rows in sorted(sheets.items())}

    # ------------------------------------------------------------------ work orders
    RES_LEG = {"driver": "DRVR", "photocontrol": "PEC", "wiring": "WIRE", "fuse": "FUSE", "lamp": "LAMP",
               "ballast": "BAL", "knockdown": "KD", "luminaire": "LUM", "pole_removed": "REM", "reprogram": "GLR",
               "glare_shield": "GLR", "ug_cable": "UGC"}
    PROB_LEG = {"driver": "OUT", "photocontrol": "OUT", "wiring": "OUT", "fuse": "OUT", "lamp": "OUT",
                "ballast": "OUT", "knockdown": "DMG", "luminaire": "OUT", "pole_removed": "PLN", "reprogram": "CMP",
                "glare_shield": "CMP", "ug_cable": "OUT"}
    ACT_NEW = {"driver": "SL-DRV-RPL", "photocontrol": "SL-PC-RPL", "wiring": "SL-WIRING", "fuse": "SL-FUSE-RPL",
               "lamp": "SL-LAMP-RPL", "ballast": "SL-BALLAST-RPL", "knockdown": "SL-KNOCKDOWN",
               "luminaire": "SL-LUM-RPL", "pole_removed": "SL-POLE-REM", "reprogram": "SL-GLARE",
               "glare_shield": "SL-GLARE", "ug_cable": "SL-UG-CABLE"}

    def unit(self, o):
        """The light an outage belongs to: a conversion luminaire or a sodium or metal halide light."""
        if o.get("lum") is not None or o.get("circuit"):
            L = self.w.lum[o["lum"] if o.get("lum") is not None else o["riser_i"]]
            return dict(pole=L["pole"], town=L["town"], watts=L["watts"], led=True, kind="LED", reprog=L["reprog"])
        N = self.w.noncon[o["nc"]]
        return dict(pole=N["pole"], town=N["town"], watts=int(N["kind"].split(" ")[1]), led=False,
                    kind=N["kind"].split(" ")[0])

    def parts(self, o, U):
        k = o["kind"]
        if U["led"]:
            # a replacement luminaire is taken from stock at the wattage the pole is recorded at
            cur = 70 if (U["reprog"] is not None and U["reprog"] < o["day"]) else U["watts"]
            return {"driver": "HL-SVC-DRV%03d" % cur, "photocontrol": "PC-7PIN-120",
                    "knockdown": "POLE-30AL; " + P.CATALOG[cur], "luminaire": P.CATALOG[cur],
                    "fuse": "FUSE-10A", "glare_shield": "HSS-%d" % cur, "ug_cable": "UG-SPLICE-KIT"}.get(k, "")
        lamp = "LU%d/55" % U["watts"] if U["kind"] == "HPS" else "MH%d/U" % U["watts"]
        return {"lamp": lamp, "ballast": "BAL-%s%d" % (U["kind"], U["watts"]), "photocontrol": "PC-7PIN-120",
                "fuse": "FUSE-10A"}.get(k, "")

    def _wo_events(self):
        """Every outage and service event with its work order times."""
        ev = [(o, self.unit(o)) for o in self.w.outages]
        ev.sort(key=lambda x: (x[0]["created"], x[1]["pole"]))
        return ev

    def legacy_rows(self):
        r = self.rng
        cut = d2i(P.CUTOVER)
        rows, n = [], 0
        for o, L in self._wo_events():
            if o["created"] >= cut:
                continue
            n += 1
            op, cl = dtime(o["created"]), dtime(o["completed"])
            loc = "TPL%d" % L["pole"] if r.random() > 0.05 else "%s / %s" % (self.addr[L["pole"]], "tag %d" % L["pole"])
            closed = cl.strftime("%m/%d/%Y %H:%M") if o["completed"] < cut else ""
            rem = ""
            if o["kind"] == "driver":
                rem = "replaced driver, svc kit" if r.random() < .7 else "drvr dead, replaced"
            elif o["kind"] == "photocontrol":
                rem = "new PE cell"
            elif o["kind"] == "knockdown":
                rem = "pole & lum replaced, police rpt on file" if r.random() < .5 else "veh hit, new pole/fixture"
            elif o["kind"] == "luminaire":
                rem = "fixture swapped, Halberd warranty RMA"
            elif o["kind"] == "fuse":
                rem = "fuse blown, replaced" if r.random() < .5 else ""
            elif o["kind"] == "lamp":
                rem = "relamped" if r.random() < .6 else "lamp cycling, relamped"
            self._leg_no = getattr(self, "_leg_no", 100000) + int(self.idg.integers(2, 29))
            rows.append(["L%06d" % self._leg_no, op.strftime("%m/%d/%Y %H:%M"), closed, loc,
                         self.PROB_LEG[o["kind"]], self.RES_LEG[o["kind"]] if closed else "",
                         "C%02d" % int(r.integers(1, 12)), rem])
        head = ["WO_NO", "OPENED", "CLOSED", "LOCATION", "PROB", "RES", "CREW", "REMARKS"]
        return head, rows

    def new_rows(self):
        """The successor system: every work order created from July 2023, and the legacy work orders still open
        at the cutover, carried in under new numbers with their original opened time."""
        r = self.rng
        cut = d2i(P.CUTOVER)
        rows, n = [], 0
        for o, L in self._wo_events():
            carried = o["created"] < cut <= o["completed"]
            if o["created"] < cut and not carried:
                continue
            n += 1
            yr = dtime(o["created"]).year if not carried else 2023
            u_src = r.random()
            src = ("TROUBLE" if u_src < 0.25 else "PATROL") if (o.get("patrol") or not o.get("reports")) else ""
            if o["kind"] == "pole_removed":
                src = "PLANNED"
            if o["kind"] in ("reprogram", "glare_shield"):
                src = "CMPLT-%05d" % int(r.integers(10000, 99999))
            anchor = None
            for rp in o.get("reports", []):
                if rp.get("anchor"):
                    anchor = rp
            if carried:
                src = "MIGRATED"
            elif o["kind"] == "ug_cable":
                src = "PATROL" if o["patrol"] else "TROUBLE"
            elif anchor is not None:
                src = "CR-%06d" % anchor["id"]
            elif "pre_id" in o and not carried:
                src = "CR-%06d" % o["pre_id"]
            elif carried:
                src = "MIGRATED"
            rep_t = (dtime(anchor["t"]) if anchor is not None else
                     dtime(o["reported"]) if ("reported" in o and o["kind"] != "ug_cable") else dtime(o["created"]))
            done = o["completed"] <= d2i(P.RECORD_END) + 1 - 1e-9
            notes = ""
            if o["kind"] == "driver":
                u_n = r.random()
                notes = "" if u_n < .55 else ("replaced driver" if u_n < .8 else
                                              ("driver swapped, tested OK" if u_n < .93 else "no output from driver"))
            elif o["kind"] == "luminaire":
                notes = "luminaire replaced under warranty"
            parts = self.parts(o, L)
            if o["created"] > d2i(P.RECORD_END) + 1:
                continue
            seq = getattr(self, "_wo_seq", {})
            seq[yr] = seq.get(yr, int(self.idg.integers(40, 400))) + int(self.idg.integers(3, 41))
            self._wo_seq = seq
            rows.append(["WO-%02d-%06d" % (yr % 100, seq[yr]), "SL-%06d" % L["pole"], self.ACT_NEW[o["kind"]],
                         "CLOSED" if done else "OPEN",
                         iso_local(rep_t), iso_local(dtime(o["created"])),
                         iso_local(dtime(o["completed"])) if done else "", src,
                         "C%02d" % int(r.integers(1, 12)), parts if done else "", notes if done else ""])
        head = ["work_order", "asset_id", "activity", "status", "reported_at", "created_at", "completed_at",
                "source", "crew", "parts", "notes"]
        return head, rows

    # ------------------------------------------------------------------ customer outage reports, Dec 2025 to Dec 2026
    def report_rows(self):
        w, r = self.w, self.rng
        lo = dt.datetime(2025, 12, 1)
        rows = []
        for o, rp in w.reports:
            t = dtime(rp["t"])
            if t < lo or t > dt.datetime(2026, 12, 31, 23, 59):
                continue
            if rp.get("foreign"):
                stamp = (t + dt.timedelta(hours=eastern_offset(t))).strftime("%Y-%m-%dT%H:%M:%SZ") \
                    if rp["ch"] == "PORTAL" else phone_stamp(t)
                rows.append(["CR-%06d" % rp["id"], rp["ch"], stamp, "", "%d %s" % (rp["house"], rp["street"]),
                             P.TOWN_NAME[o["town"]], str(r.choice(["light out", "light out in the lot",
                                                                    "park light out", "dark"]))])
                continue
            pl = rp["pole"]
            if rp["ch"] == "PORTAL":
                u = t + dt.timedelta(hours=eastern_offset(t))
                stamp = u.strftime("%Y-%m-%dT%H:%M:%SZ")
                pole = "SL-%06d" % pl
                addr = self.addr[pl]
            else:
                stamp = phone_stamp(t)
                v = r.random()
                gone = pl in self.removed_poles
                pole = "%d" % pl if (v < 0.62 or gone) else ("Pole %d" % pl if v < 0.80 else "")
                addr = self.addr[pl] if pole == "" or r.random() < .5 else ""
            desc = str(r.choice(["light out", "streetlight out", "light out at night", "dark", "light not working",
                                 "light flickering" if o["kind"] in ("photocontrol", "wiring", "lamp") else "light out",
                                 "pole knocked down" if o["kind"] == "knockdown" else "light out"]))
            rows.append(["CR-%06d" % rp["id"], rp["ch"], stamp, pole, addr, P.TOWN_NAME[o["town"]], desc])
        head = ["report_id", "channel", "received", "pole", "address", "town", "description"]
        return head, rows

    # ------------------------------------------------------------------ Corrinvale's networked controls, 2026
    def nlc_rows(self):
        """The control system's monthly record for each Corrinvale node: the hours it held its luminaire dimmed.
        Nodes dim from midnight to 05:00, residential streets to half output and arterials to 70 per cent; a node
        that lost its network for a month records nothing for that month."""
        if hasattr(self, "_nlc"):
            return self._nlc
        self._nodes = set()
        w, r = self.w, self.rng
        import calendar
        end = d2i(P.RECORD_END)
        rows = []
        y0 = d2i(dt.date(2026, 1, 1))
        node_k = 0
        for L in sorted(w.lum, key=lambda x: x["pole"]):
            if not P.TOWN_NLC[L["town"]]:
                continue
            if L["exit_type"] == "pole_removed" and L["exit"] < y0:
                continue
            node_k += 1
            while True:
                node = "%07X" % int(self.idg.integers(0x1000000, 0xFFFFFFF))
                if node not in self._nodes:
                    break
            self._nodes.add(node)
            drift = float(self.idg.uniform(0.955, 1.015))
            dark = self._dark_nights(L)
            level = 70 if r.random() < 0.15 else 50
            for m in range(1, 13):
                a = d2i(dt.date(2026, m, 1))
                b = d2i(dt.date(2026, m, calendar.monthrange(2026, m)[1]))
                last = min(b, end)
                if L["exit_type"] == "pole_removed" and L["exit"] <= last:
                    last = L["exit"] - 1
                nights = max(0, last - a + 1)
                if nights == 0:
                    continue
                night_len = P.BURN_H[m - 1] / calendar.monthrange(2026, m)[1]
                per = min(P.DIM_H_PER_NIGHT, night_len / 2 + 0.6)
                lit = nights - dark.get(m, 0)
                dh = max(0.0, round(lit * per * drift + float(self.idg.normal(0, 0.9)), 1))
                if r.random() < 0.012:
                    continue                                   # no record that month (network outage)
                rows.append([node, "SL-%06d" % L["pole"], "2026-%02d" % m, "%.1f" % dh,
                             "%d" % level])
        head = ["node_id", "pole_id", "month", "dimmed_hours", "dim_level_pct"]
        self._nlc = (head, rows)
        return head, rows

    def _dark_nights(self, L):
        """Nights in each month of 2026 the light was dark, from its outages (a dark light does not dim)."""
        out = {}
        for o in self.by_lum.get(L["_i"], []):
            if o["kind"] in self.w.PLANNED:
                continue
            a, b = int(o["dark"]), int(o["completed"])
            for dday in range(a, b):
                d = i2d(dday)
                if d.year == 2026:
                    out[d.month] = out.get(d.month, 0) + 1
        return out

    # ------------------------------------------------------------------ distractors
    def billing_rows(self):
        w = self.w
        end = d2i(P.RECORD_END)
        counts = {}
        for L in w.lum:
            if L["exit_type"] == "pole_removed" and L["exit"] <= end:
                continue
            cur = 70 if (L["reprog"] is not None and L["reprog"] <= end) else L["watts"]
            k = (L["town"], "SL-LED%d" % cur)
            counts[k] = counts.get(k, 0) + 1
        for N in w.noncon:
            k = (N["town"], "SL-" + N["kind"].split(" ")[0] + N["kind"].split(" ")[1])
            counts[k] = counts.get(k, 0) + 1
        rate = {"SL-LED40": 9.14, "SL-LED70": 11.02, "SL-LED110": 13.66, "SL-HPS100": 12.37, "SL-HPS150": 15.11,
                "SL-MH175": 17.40}
        rows = []
        for (t, rc), n in sorted(counts.items()):
            rows.append(["TPL-SL-%s-01" % t, P.TOWN_NAME[t], "2026-12", rc, n, "%.2f" % rate.get(rc, 0),
                         "%.2f" % (n * rate.get(rc, 0))])
        head = ["account", "municipality", "bill_month", "rate_code", "luminaires_billed", "unit_rate_usd",
                "amount_usd"]
        return head, rows

    def weather_rows(self):
        r = self.rng
        rows = []
        d = dt.date(2021, 1, 1)
        while d <= P.RECORD_END:
            doy = d.timetuple().tm_yday
            mean = 51.5 - 23.5 * np.cos(2 * np.pi * (doy - 18) / 365.25)
            tmax = mean + 9.5 + r.normal(0, 6.5)
            tmin = mean - 9.5 + r.normal(0, 6.0)
            pr = max(0.0, r.normal(-0.05, 0.22)) if r.random() < 0.38 else 0.0
            rows.append([d.isoformat(), "%.0f" % tmax, "%.0f" % min(tmin, tmax - 2), "%.2f" % pr])
            d += dt.timedelta(days=1)
        return ["date", "tmax_f", "tmin_f", "precip_in"], rows

    def vegetation_rows(self):
        w, r = self.w, self.rng
        rows = []
        d = dt.date(2025, 1, 6)
        k = 0
        while d <= P.RECORD_END:
            if d.weekday() < 5 and r.random() < 0.55:
                t = str(r.choice(P.TOWN_CODES))
                k += 1
                self._vp = getattr(self, "_vp", 3100) + int(self.idg.integers(1, 6))
                rows.append(["VP-%05d" % self._vp, d.isoformat(), P.TOWN_NAME[t], str(r.choice(w.streets[t])),
                             int(r.integers(2, 28)), int(r.integers(0, 6)), "T%02d" % int(r.integers(1, 5))])
            d += dt.timedelta(days=1)
        return ["patrol_id", "date", "town", "street", "poles_cleared", "limbs_removed_over_4in", "crew"], rows
