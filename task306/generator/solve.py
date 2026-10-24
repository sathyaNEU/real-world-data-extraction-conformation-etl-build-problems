"""Every owed figure from the pack's files alone: the 2027 forecast per platform (the cars on the register on 30 June
2026, and the used imports still to arrive, carried at the rate and mix of the twelve months before), the slots by
largest remainder, and the three asks from the line's exports. Also the wrong routes the ladder and the ask sheet
price, each on the same files."""
import calendar
import csv
import datetime as dt
import os
import re
from collections import defaultdict

import numpy as np

NAMES = ["Volta hatch", "Kestrel SUV", "Plover saloon", "Mira city car", "Tern van"]
MAKE = {"VOLTA": "Volta hatch", "KESTREL": "Kestrel SUV", "PLOVER": "Plover saloon", "MIRA": "Mira city car",
        "TERN": "Tern van"}
CODE = {"VH": "Volta hatch", "KS": "Kestrel SUV", "PS": "Plover saloon", "MC": "Mira city car", "TV": "Tern van"}
REFC = "Voltwerk revisiepakket (alle platforms)"
SNAP = dt.date(2026, 6, 30)
Y0, Y1 = dt.date(2027, 1, 1), dt.date(2028, 1, 1)
FY0, FY1 = dt.date(2025, 7, 1), dt.date(2026, 6, 30)
SLOTS, LOT = 3000, 50


def d8(s):
    return dt.date(int(s[:4]), int(s[4:6]), int(s[6:8]))


def iso(s):
    return dt.date(int(s[:4]), int(s[5:7]), int(s[8:10]))


def stamp(s):
    return dt.datetime(int(s[:4]), int(s[5:7]), int(s[8:10]), int(s[11:13]), int(s[14:16]))


def add_years(d, y):
    """the same calendar day y years on (29 February to 28 February)"""
    try:
        return d.replace(year=d.year + y)
    except ValueError:
        return d.replace(year=d.year + y, day=28)


def rows(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def warranty_years(path):
    """the OEM pack warranty per platform, read from the warranty terms' table"""
    from pypdf import PdfReader
    text = " ".join(p.extract_text() for p in PdfReader(path).pages)
    out = {}
    for n in NAMES:
        m = re.search(re.escape(n) + r"\s+(\d+)\s+years", text)
        out[n] = int(m.group(1))
    return out


class Pack:
    def __init__(self, target, files):
        self.T, self.F = target, {k: os.path.join(target, v) for k, v in files.items()}
        cv = rows(self.F["curves"])
        self.ages = np.array([float(r["pakketleeftijd_jaar"]) for r in cv])
        self.tab = {c: np.array([float(r[c]) for r in cv]) for c in cv[0] if c != "pakketleeftijd_jaar"}
        self.war = warranty_years(self.F["warranty"])
        reg = rows(self.F["register"])
        self.reg = [dict(k=r["kenteken"], n=MAKE[r["merk"]], fu=d8(r["datum_eerste_toelating"]),
                         nl=d8(r["datum_eerste_tenaamstelling_in_nederland"])) for r in reg]
        ev = defaultdict(list)
        for r in rows(self.F["log"]):
            ev[r["kenteken"].replace("-", "")].append((iso(r["vervangdatum"]), r["geplaatst_pakket"]))
        for k in ev:
            ev[k].sort()
        self.ev = ev

    # ---- the call ----------------------------------------------------------------------------------------------
    interp = "linear"

    def F_(self, curve, a):
        if self.interp == "step":
            i = np.clip(np.floor(a).astype(int) if hasattr(a, "__len__") else int(np.floor(a)), 0, len(self.ages) - 1)
            return self.tab[curve][i]
        return np.interp(a, self.ages, self.tab[curve])

    def pack_at(self, car, before=None, inclusive=True):
        """(fitted on, curve) of the car's pack: its last replacement on or before `before`, else the one it was built
        with"""
        last = None
        for d, fitted in self.ev.get(car["k"], []):
            if before is None or d < before or (inclusive and d == before):
                last = (d, fitted)
        if last is None:
            return car["fu"], car["n"]
        return last[0], (REFC if last[1] == "Voltwerk revisie" else car["n"])

    def p_due(self, start, curve, w_end, at_risk_from, survived_to, y0=Y0, y1=Y1, year=365.25, cond=True):
        a_s = (survived_to - start).days / year
        lo = max(y0, at_risk_from, w_end)
        a0, a1 = (lo - start).days / year, (y1 - start).days / year
        if a1 <= a0:
            return 0.0
        num = max(0.0, float(self.F_(curve, a1) - self.F_(curve, a0)))
        return num / max(1.0 - float(self.F_(curve, a_s)), 1e-9) if cond else num

    def w_end(self, car, rule="calendar"):
        y = self.war[car["n"]]
        if rule == "calendar":
            return add_years(car["fu"], y)
        return car["fu"] + dt.timedelta(days=int(round(y * 365.25)))

    def base(self, rule="calendar", year=365.25, cond=True, original=False, warranty_from=None, all_eight=False,
             vw_excl=False):
        out = defaultdict(float)
        for c in self.reg:
            start, curve = (c["fu"], c["n"]) if original else self.pack_at(c, SNAP)
            we = self.w_end(c, rule)
            if vw_excl and curve == REFC:
                we = max(we, add_years(start, 2))
            if all_eight:
                we = add_years(c["fu"], 8)
            if warranty_from == "nl" and c["fu"] < c["nl"]:
                we = add_years(c["nl"], self.war[c["n"]])
                if start == c["fu"]:
                    start = c["nl"]
            out[c["n"]] += self.p_due(start, curve, we, SNAP, SNAP, year=year, cond=cond)
        return dict(out)

    def imports(self, months=12):
        lo = add_months(SNAP, -months)
        return [c for c in self.reg if c["fu"] < c["nl"] and lo < c["nl"] <= SNAP]

    def arrivals(self, months=12, horizon=None, orig=False, weights=None, rule="calendar", year=365.25):
        """the used imports still to arrive: each month from July 2026 to December 2027 takes in the cars the window
        took in, in the window's average month, each on the same day of its month, at the same age and with the pack it
        arrived with"""
        hz = horizon or [(2026, m) for m in range(7, 13)] + [(2027, m) for m in range(1, 13)]
        out = defaultdict(float)
        win = self.imports(months)
        for c in win:
            start, curve = (c["fu"], c["n"]) if orig else self.pack_at(c, c["nl"], inclusive=False)
            we = self.w_end(c, rule)
            for j, (y, m) in enumerate(hz):
                day = min(c["nl"].day, calendar.monthrange(y, m)[1])
                arr = dt.date(y, m, day)
                off = arr - c["nl"]
                wgt = (weights[c["n"]][j] if weights else 1.0) / months
                out[c["n"]] += wgt * self.p_due(start + off, curve, we + off, arr, arr, year=year)
        return dict(out)

    def trend_weights(self, span=36):
        """each platform's monthly imports over the last `span` months, a straight line carried to each month ahead,
        as a multiple of the last twelve months' average"""
        hz = [(2026, m) for m in range(7, 13)] + [(2027, m) for m in range(1, 13)]
        out = {}
        for n in NAMES:
            cnt = []
            for k in range(span, 0, -1):
                a = add_months(SNAP, -k)
                b = add_months(SNAP, -k + 1)
                cnt.append(sum(1 for c in self.reg if c["n"] == n and c["fu"] < c["nl"] and a < c["nl"] <= b))
            x = np.arange(span)
            bb, aa = np.polyfit(x, np.array(cnt, float), 1)
            mean12 = max(np.mean(cnt[-12:]), 1e-9)
            out[n] = [(aa + bb * (span + j)) / mean12 for j in range(len(hz))]
        return out

    def renewal(self):
        """a pack failing after its warranty from July to December 2026 takes a refurbished pack, which can itself fail
        in 2027"""
        out = defaultdict(float)
        for c in self.reg:
            start, curve = self.pack_at(c, SNAP)
            we = self.w_end(c)
            for m in range(7, 13):
                a, b = dt.date(2026, m, 1), add_months(dt.date(2026, m, 1), 1)
                pm = self.p_due(start, curve, we, SNAP, SNAP, y0=a, y1=b)
                if pm <= 0:
                    continue
                mid = a + (b - a) // 2
                out[c["n"]] += pm * self.p_due(mid, REFC, dt.date(1900, 1, 1), mid, mid)
        return dict(out)

    def call(self):
        b = self.base()
        a = self.arrivals()
        fc = {n: b.get(n, 0.0) + a.get(n, 0.0) for n in NAMES}
        return dict(base=b, arrivals=a, forecast=fc, total=sum(fc.values()), lots=lots(fc))


def add_months(d, k):
    y, m = d.year + (d.month - 1 + k) // 12, (d.month - 1 + k) % 12 + 1
    return dt.date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def lots(fc, total=SLOTS, lot=LOT):
    s = sum(fc.values())
    raw = {k: total * v / s / lot for k, v in fc.items()}
    floors = {k: int(np.floor(x)) for k, x in raw.items()}
    b = dict(floors)
    rem = total // lot - sum(b.values())
    order = sorted(raw, key=lambda k: -(raw[k] - floors[k]))
    for k in order[:rem]:
        b[k] += 1
    r = sorted([raw[k] - np.floor(raw[k]) for k in raw], reverse=True)
    margin = r[rem - 1] - r[rem] if 0 < rem < len(r) else 1.0
    return dict(slots={k: v * lot for k, v in b.items()}, margin=float(margin), raw=raw, floors=floors, extra=rem)


# ---- the asks -----------------------------------------------------------------------------------------------------
def in_fy(d):
    return FY0 <= d <= FY1


class Line:
    def __init__(self, target, files):
        F = {k: os.path.join(target, v) for k, v in files.items()}
        self.wo = {r["werkorder"]: r for r in rows(F["workorders"])}
        self.stores = rows(F["stores"])
        self.receipts = rows(F["receipts"])
        self.eol = rows(F["eol"])
        self.bms = rows(F["bms"])
        self.ships = rows(F["shipments"])
        self.intake = rows(F["intake"])
        import openpyxl
        wb = openpyxl.load_workbook(F["parts"], read_only=True)
        hdr, *body = list(wb.active.values)
        self.parts = {r[0]: dict(zip(hdr, r)) for r in body}
        wb = openpyxl.load_workbook(F["recycler"], read_only=True)
        hdr, *body = list(wb.active.values)
        self.recycled = [dict(zip(hdr, r)) for r in body]

    def shipped(self):
        out = defaultdict(int)
        for s in self.ships:
            if in_fy(iso(s["verzonden_op"])):
                out[CODE[self.wo[s["werkorder"]]["platformcode"]]] += 1
        return out

    def batch_picks(self):
        """pick lists whose lines repeat one quantity of one lot over several work orders, on a lot whose lines add up
        to more than the lot received: the quantity went out once"""
        rec = defaultdict(int)
        for r in self.receipts:
            rec[r["partij"]] += int(r["aantal"])
        issued = defaultdict(int)
        for r in self.stores:
            issued[r["partij"]] += int(r["aantal"])
        groups = defaultdict(list)
        for r in self.stores:
            if r["soort"] == "UITGIFTE":
                groups[(r["picklijst"], r["partij"], r["aantal"])].append(r)
        out = {}
        for key, rs in groups.items():
            if len(rs) >= 2 and key[1] in rec and issued[key[1]] > rec[key[1]]:
                out[key] = len(rs)
        return out

    def ask_a(self, mode="gold"):
        """modules a lot of 50 should carry: modules stores issued in the year, net of returns, per pack shipped"""
        ships = self.shipped()
        bp = self.batch_picks()
        cohort = ({s["werkorder"] for s in self.ships if in_fy(iso(s["verzonden_op"]))} if mode == "cohort" else None)
        seen = set()
        mods = defaultdict(float)
        for r in self.stores:
            d = stamp(r["geboekt_op"]).date()
            if not in_fy(d):
                continue
            if cohort is not None and r["werkorder"] not in cohort:
                continue
            n = CODE[self.wo[r["werkorder"]]["platformcode"]]
            per = 1 if mode == "units" else int(self.parts[r["artikelnummer"]]["modules_per_eenheid"])
            q = int(r["aantal"])
            key = (r["picklijst"], r["partij"], r["aantal"])
            if mode in ("gold", "cohort") and r["soort"] == "UITGIFTE" and key in bp:
                if key in seen:
                    continue
                seen.add(key)
            if mode == "dedup" and r["soort"] == "UITGIFTE":
                if key in seen:
                    continue
                seen.add(key)
            if mode == "issues_only" and r["soort"] != "UITGIFTE":
                continue
            mods[n] += q * per
        return {n: 50.0 * mods[n] / ships[n] for n in NAMES}

    def ask_b(self, mode="gold"):
        """share of packs whose first end-of-line run in the year passed (an aborted run is no test)"""
        wo_of = {r["bms_serienummer"]: r["werkorder"] for r in self.bms}
        first = {}
        for r in sorted(self.eol, key=lambda r: (r["start"], r["run_id"])):
            if r["resultaat"] == "ABORT" and mode != "abort_counts":
                continue
            key = r["pakket_id"] if mode == "by_id" else wo_of[r["pakket_id"]]
            if key not in first:
                first[key] = r
        plat = {"VH": "Volta hatch", "KS": "Kestrel SUV", "PS": "Plover saloon", "MC": "Mira city car",
                "TV": "Tern van"}
        out = {}
        for n in NAMES:
            xs = [r for r in first.values() if plat[r["programma"].split("-")[1]] == n and in_fy(stamp(r["start"]).date())]
            out[n] = 100.0 * sum(r["resultaat"] == "PASS" for r in xs) / len(xs)
        return out

    def ask_c(self, mode="gold"):
        """share of the cores received in the year that were rejected at intake: a core the MES shows a work order on
        was built on, so it passed intake, whatever grade it carries on the morning of the export"""
        label = lambda s: {"VOLTA": "Volta hatch", "KESTREL": "Kestrel SUV", "PLOVER": "Plover saloon",
                           "MIRA": "Mira city car", "TERN": "Tern van"}[s.split()[0]]
        built = {w["kerncode"] for w in self.wo.values()}
        tag = {}
        for r in self.recycled:
            q = r["datum_quarantaine"]
            if r["kerncode"]:
                tag[r["kerncode"]] = q.date() if hasattr(q, "date") else q
        rec, rej, line_scrap, same_day = defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int)
        for r in self.intake:
            d = stamp(r["ontvangen_op"]).date()
            if not in_fy(d):
                continue
            n = label(r["label_platform"])
            rec[n] += 1
            if r["keuring"] != "AFGEKEURD":
                continue
            if r["kerncode"] in built:
                line_scrap[n] += 1
            else:
                rej[n] += 1
            same_day[n] += tag.get(r["kerncode"]) == d
        scrapped_fy = defaultdict(int)
        for w in self.wo.values():
            if w["status"] == "AFGEKEURD" and w["afgesloten"] and in_fy(iso(w["afgesloten"])):
                scrapped_fy[CODE[w["platformcode"]]] += 1
        allrec = defaultdict(int)
        for r in self.recycled:
            q = r["datum_quarantaine"]
            q = q.date() if hasattr(q, "date") else q
            if in_fy(q):
                allrec[r["omschrijving"].split(", ", 1)[1]] += 1
        out = {}
        for n in NAMES:
            if mode == "gold":
                out[n] = 100.0 * rej[n] / rec[n]
            elif mode == "naive":
                out[n] = 100.0 * (rej[n] + line_scrap[n]) / rec[n]
            elif mode == "same_day":
                out[n] = 100.0 * same_day[n] / rec[n]
            elif mode == "count_scrapped":
                out[n] = 100.0 * (rej[n] + line_scrap[n] - scrapped_fy[n]) / rec[n]
            elif mode == "both_out":
                out[n] = 100.0 * rej[n] / (rec[n] - line_scrap[n])
            elif mode == "all_recycled":
                out[n] = 100.0 * allrec[n] / rec[n]
            elif mode == "detail":
                out[n] = dict(cores=rec[n], rejected=rej[n], scrapped_on_line=line_scrap[n])
        return out
