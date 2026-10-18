"""Read the cut pack the way an analyst does, for checks.py and cracker.py: stitch the capacity layouts through the
roster, read the register's staffing out of its PDF, put the agency reports on Eastern Time. Every route the design
note names is computed here from the shipped files alone."""
from __future__ import annotations

import collections
import datetime as dt
import os
import re
import statistics as st

import numpy as np
import openpyxl
import pandas as pd
import pdfplumber

import common as C

D = dt.date
PACK = C.TARGET


def f(name, pack=None):
    return os.path.join(pack or PACK, name)


def find(pattern, pack=None):
    for n in sorted(os.listdir(pack or PACK)):
        if re.fullmatch(pattern, n):
            return os.path.join(pack or PACK, n)
    raise FileNotFoundError(pattern)


def eastern_offset(t):
    y = t.year
    m = dt.datetime(y, 3, 8)
    while m.weekday() != 6:
        m += dt.timedelta(days=1)
    n = dt.datetime(y, 11, 1)
    while n.weekday() != 6:
        n += dt.timedelta(days=1)
    return -4 if m.replace(hour=2) <= t < n.replace(hour=2) else -5


def utc_to_local(t):
    loc = t + dt.timedelta(hours=-5)
    if eastern_offset(loc) == -4:
        loc = t + dt.timedelta(hours=-4)
    return loc


class Pack:
    def __init__(self, pack=None):
        self.dir = pack or PACK
        self.roster = pd.read_excel(find(r"tpha_members_2026-27\.xlsx", self.dir), sheet_name="Members", dtype=str)
        self.by_member = dict(zip(self.roster["member_no"], self.roster["facility_id"]))
        self.region = dict(zip(self.roster["facility_id"], self.roster["region"]))
        self.name = dict(zip(self.roster["facility_id"], self.roster["hospital"]))
        self.unit = dict(zip(self.roster["facility_id"], self.roster["surge_unit"]))
        self.crs_site = dict(zip(self.roster["crestfield_site_code"], self.roster["facility_id"]))
        self.isn_name = dict(zip(self.roster["inland_seas_facility"], self.roster["facility_id"]))
        self.grid = self._register()
        self.cap = self._capacity()
        self.decl = pd.read_csv(find(r"surge_declarations_.*\.csv", self.dir), dtype=str)
        self.decl["t"] = pd.to_datetime(self.decl["declared_at"])
        self.decl["level_to"] = self.decl["level_to"].astype(int)
        self.decl["level_from"] = self.decl["level_from"].astype(int)
        self.iv = self._intervals()

    # ------------------------------------------------------------------------------------------------ readers
    def _register(self):
        """Each member's agency RN shifts a day at Level 1 and Level 2, read off the register's table rows."""
        grid = {}
        by_name = {v: k for k, v in self.name.items()}
        with pdfplumber.open(find(r"surge_plan_register_2026-27\.pdf", self.dir)) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        for line in text.splitlines():
            for nm, fid in by_name.items():
                if line.startswith(nm + " "):
                    m = re.search(r"\s(\d+)\s+(\d+)\s+\d+\s+\d{1,2} [A-Z][a-z]{2} \d{4}$", line)
                    assert m, line
                    grid[fid] = (int(m.group(1)), int(m.group(2)))
        assert len(grid) == 24, len(grid)
        return grid

    def _capacity(self):
        old = pd.read_csv(find(r"capacity_reports_legacy_.*\.csv", self.dir), dtype=str)
        old = old.sort_values(["member_no", "report_date", "submission"])
        old = old.drop_duplicates(["member_no", "report_date"], keep="last")          # R replaces O
        old["facility_id"] = old["member_no"].map(self.by_member)
        old["census_date"] = pd.to_datetime(old["report_date"]).dt.date - dt.timedelta(days=1)
        old["level"] = old["surge_status"].fillna("").map({"": 0, "S1": 1, "S2": 2})
        old["census"] = old["census_midnight"].astype(int)
        old["beds"] = old["staffed_beds"].astype(int)
        new = pd.read_csv(find(r"capacity_daily_.*\.csv", self.dir), dtype=str)
        new["census_date"] = pd.to_datetime(new["census_date"]).dt.date
        new["level"] = new["surge_level"].astype(int)
        new["census"] = new["inpatients_midnight"].astype(int)
        new["beds"] = new["staffed_beds"].astype(int)
        cols = ["facility_id", "census_date", "census", "beds", "level"]
        cap = pd.concat([old[cols], new[cols]], ignore_index=True)
        cap = cap.sort_values(["facility_id", "census_date"]).reset_index(drop=True)
        assert not cap.duplicated(["facility_id", "census_date"]).any()
        return cap

    def _intervals(self):
        iv = collections.defaultdict(list)
        for fid, g in self.decl.sort_values("t").groupby("facility_id"):
            cur = None
            for _, x in g.iterrows():
                if cur is not None:
                    iv[fid].append((cur[0], x["t"].to_pydatetime(), cur[1]))
                    cur = None
                if x["level_to"] > 0:
                    cur = (x["t"].to_pydatetime(), x["level_to"])
            if cur is not None:
                iv[fid].append((cur[0], dt.datetime(2099, 1, 1), cur[1]))
        return dict(iv)

    def level_at(self, fid, t):
        for a, b, lv in self.iv.get(fid, []):
            if a <= t < b:
                return lv
        return 0

    # ------------------------------------------------------------------------------------------------ the call
    def fids(self, region=None):
        return sorted(k for k, v in self.region.items() if region is None or v == region)

    def draw_nights(self, fid, a, b):
        g = self.grid[fid]
        x = self.cap[(self.cap["facility_id"] == fid) & (self.cap["census_date"] >= a) & (self.cap["census_date"] <= b)]
        return int(sum(g[lv - 1] for lv in x["level"] if lv))

    def draw_shifts(self, fid, a, b):
        g = self.grid[fid]
        n = 0
        d = a
        while d <= b:
            for hh in (7, 19):
                lv = self.level_at(fid, dt.datetime.combine(d, dt.time(hh)))
                if lv:
                    n += g[lv - 1] // 2
            d += dt.timedelta(days=1)
        return n

    def spells(self, fid, a, b):
        x = self.cap[(self.cap["facility_id"] == fid) & (self.cap["census_date"] >= a) & (self.cap["census_date"] <= b)]
        out, cur = [], None
        for d, lv in zip(x["census_date"], x["level"]):
            if lv > 0:
                if cur is None:
                    cur = [d, d]
                cur[1] = d
            elif cur is not None:
                out.append(tuple(cur))
                cur = None
        if cur is not None:
            out.append(tuple(cur))
        return out

    def region_centre(self, region, w, upto=None):
        a, b = C.season_bounds(w)
        if upto:
            b = min(b, upto)
        mids = []
        for fid in self.fids(region):
            sp = self.spells(fid, a, b)
            assert len(sp) == 1, (fid, w, sp)
            s0, s1 = sp[0]
            mids.append(s0.toordinal() + (s1 - s0).days / 2.0)
        return float(np.median(mids))

    def north_waves(self, how="nights"):
        fn = self.draw_nights if how == "nights" else self.draw_shifts
        return [sum(fn(fid, *C.season_bounds(w)) for fid in self.fids("North")) for w in C.CLOSED]

    def golden(self):
        return st.mean(self.north_waves())

    def block_draw(self, fids, w):
        a, b = C.block_weeks(w)
        return sum(self.draw_nights(fid, a, b) for fid in fids)

    # ------------------------------------------------------------------------------------------------ agency lines
    def crestfield(self):
        x = pd.read_csv(find(r"crestfield_member_shifts_.*\.csv", self.dir), dtype=str)
        x["fid"] = x["client_site"].map(self.crs_site)
        x["start_utc"] = pd.to_datetime(x["shift_start_utc"].str.replace("Z", ""))
        x["start_local"] = [utc_to_local(t.to_pydatetime()) for t in x["start_utc"]]
        x["hours"] = x["hours"].astype(float)
        return x

    def inland_seas(self, fname):
        wb = openpyxl.load_workbook(find(fname, self.dir), read_only=True, data_only=True)
        rows = []
        detail = []
        for ws in wb.worksheets:
            vals = list(ws.iter_rows(values_only=True))
            if ws.title.startswith("Wk "):
                hi = [i for i, r in enumerate(vals) if r and r[0] == "Facility"][0]
                for r in vals[hi + 1:]:
                    if r and r[0]:
                        rows.append(dict(zip(vals[hi], r)))
            elif ws.title == "Timesheet detail":
                hi = [i for i, r in enumerate(vals) if r and r[0] == "Facility"][0]
                for r in vals[hi + 1:]:
                    if r and r[0]:
                        detail.append(dict(zip(vals[hi], r)))
        df = pd.DataFrame(rows)
        df["fid"] = df["Facility"].map(self.isn_name)
        df["payroll"] = [v.date() if isinstance(v, dt.datetime) else v for v in df["Payroll date"]]
        return df, pd.DataFrame(detail)


def ask_lines(P, split="timesheet", isn_date="end", utc="convert"):
    """Last winter's agency shifts as a response counts them: (fid, agency, start, on surge unit, bill-to pool).
    split: 'timesheet' counts a Crestfield night once, 'line' counts each billing line; isn_date: 'end' reads a night's
    payroll date as the day it ends, 'start' as the day it starts; utc: 'convert' puts Crestfield on Eastern Time,
    'raw' reads its UTC stamps as local."""
    out = []
    cr = P.crestfield()
    if split == "timesheet":
        cr = cr.sort_values(["timesheet_no", "start_utc"]).drop_duplicates("timesheet_no", keep="first")
    for _, x in cr.iterrows():
        t = x["start_local"] if utc == "convert" else x["start_utc"].to_pydatetime()
        out.append((x["fid"], "C", t, x["unit"] == P.unit[x["fid"]], x["bill_to"] == "TPHA POOL"))
    for fname in (r"inland_seas_member_shifts_2025-26\.xlsx", r"inland_seas_member_shifts_2026-27\.xlsx"):
        df, _ = P.inland_seas(fname)
        for _, x in df.iterrows():
            day = x["payroll"]
            if x["Shift"] == "N":
                d0 = day - dt.timedelta(days=1) if isn_date == "end" else day
                t = dt.datetime.combine(d0, dt.time(19))
            else:
                t = dt.datetime.combine(day, dt.time(7))
            out.append((x["fid"], "I", t, x["Unit"] == P.unit[x["fid"]], x["Bill to"] == "TPHA Pool"))
    return out


def ask_figures(P, lines, by_census=False):
    """Ask A (funded shifts), Ask B (billed to the pool, not funded) per member, and the weekly funded shifts by
    agency for the chart, over last winter."""
    lvl = None
    if by_census:
        lvl = {(a, b): c for a, b, c in zip(P.cap["facility_id"], P.cap["census_date"], P.cap["level"])}
    fA, fB, wk = collections.Counter(), collections.Counter(), collections.Counter()
    w0 = D(2025, 11, 3)
    for fid, ag, t, su, pool in lines:
        if not (D(2025, 11, 1) <= t.date() <= D(2026, 3, 31)):
            continue
        act = (lvl.get((fid, t.date()), 0) > 0) if by_census else (P.level_at(fid, t) > 0)
        fu = su and act
        if fu:
            fA[fid] += 1
            k = (t.date() - w0).days // 7
            if 0 <= k < 21:
                wk[(k, ag)] += 1
        if pool and not fu:
            fB[fid] += 1
    return fA, fB, wk


def chart_figures(P, lines, by_census=False):
    """The chart's two labelled figures as a response computes them: its busiest Monday-to-Sunday week by funded shifts
    (by the week each shift started in, 3 November 2025 to 29 March 2026), that week's funded total, and how many agency
    shifts starting that week were billed to the pool."""
    lvl = None
    if by_census:
        lvl = {(a, b): c for a, b, c in zip(P.cap["facility_id"], P.cap["census_date"], P.cap["level"])}
    w0 = D(2025, 11, 3)
    fund, bill = collections.Counter(), collections.Counter()
    for fid, ag, t, su, pool in lines:
        k = (t.date() - w0).days // 7
        if not 0 <= k < 21:
            continue
        act = (lvl.get((fid, t.date()), 0) > 0) if by_census else (P.level_at(fid, t) > 0)
        if su and act:
            fund[k] += 1
        if pool:
            bill[k] += 1
    kb = max(range(21), key=lambda k: (fund[k], -k))
    return kb, fund[kb], bill[kb], fund, bill


PATHS = (("golden", dict(), False),
         ("cracker", dict(split="line", isn_date="end"), False),
         ("cracker, A2 cracked", dict(split="timesheet", isn_date="end"), False),
         ("cracker without the dictionary", dict(split="line", isn_date="start"), False),
         ("mirror", dict(split="line", isn_date="start"), True))


def cracker_report(report, pack=None, quiet=False):
    P = Pack(pack)
    south = P.fids("Southeast") + P.fids("West and Central")
    rows = {}
    for name, kw, cen in PATHS:
        lines = ask_lines(P, **kw)
        fA, fB, _ = ask_figures(P, lines, by_census=cen)
        kb, ft, bt, _, _ = chart_figures(P, lines, by_census=cen)
        rows[name] = (fA, fB, (ft, bt))
    g = rows["golden"]
    return report(rows, g[0], g[1], g[2], south, quiet)


# ---------------------------------------------------------------------------------------------------- timing routes
REG_NAME = {"SE": "Southeast", "WC": "West and Central", "NO": "North"}


def anchor(P, kind, w, upto=None):
    """A region's place in a winter as the census shows it: the median of its members' spell midpoints, its first
    surge night ('first'), or the statewide first surge night or median midpoint over the 16 southern members."""
    a, b = C.season_bounds(w)
    b = min(b, upto) if upto else b
    if kind in ("SE", "WC", "NO"):
        return P.region_centre(REG_NAME[kind], w, upto)
    if kind.endswith("first"):
        fids = P.fids(REG_NAME[kind[:2]]) if kind[:2] in REG_NAME else P.fids("Southeast") + P.fids("West and Central")
        return min(P.spells(f, a, b)[0][0].toordinal() for f in fids)
    if kind == "state":
        mids = []
        for f in P.fids("Southeast") + P.fids("West and Central"):
            s0, s1 = P.spells(f, a, b)[0]
            mids.append(s0.toordinal() + (s1 - s0).days / 2.0)
        return float(np.median(mids))
    raise ValueError(kind)


def window(P, fids, delta):
    a, b = C.BLOCK_2027
    return sum(P.draw_nights(f, a - dt.timedelta(days=delta), b - dt.timedelta(days=delta)) for f in fids)


def aligned(P, kind):
    """Every member's closed-winter census moved so the anchor sits where it sits this winter at the pull, read over the
    block weeks and averaged over the five closed winters."""
    a27 = anchor(P, kind, 2027, C.CENSUS_END)
    return st.mean(window(P, P.fids(), int(round(a27 - anchor(P, kind, w)))) for w in C.CLOSED)


def placed(P, up, onset=False, agg="mean"):
    """The North's closed-winter waves placed this winter at an upstream anchor plus the closed winters' lag."""
    ku, kn = (up + "first", "NOfirst") if onset else (up, "NO")
    lags = [anchor(P, kn, w) - anchor(P, ku, w) for w in C.CLOSED]
    lag = st.mean(lags) if agg == "mean" else st.median(lags)
    pred = anchor(P, ku, 2027, C.CENSUS_END) + lag
    return st.mean(window(P, P.fids("North"), int(round(pred - anchor(P, kn, w)))) for w in C.CLOSED)


def ww_peaks(P):
    """Each region's influenza A peak in the wastewater each winter: the sewersheds' log concentration over PMMoV,
    averaged by sample date, smoothed over a centred fifteen days, its highest point from October to the end of the
    season (to the last sample this winter)."""
    import json
    import math
    d = json.load(open(find(r"wastewater_results_.*\.json", P.dir)))
    latest = {}
    for r in d["results"]:
        if r["target"] != "Influenza A" or r["concentration_copies_per_l"] is None:
            continue
        k = (r["sewershed_id"], r["sample_date"])
        if k not in latest or r["result_status"] == "revised":
            latest[k] = r
    by = collections.defaultdict(list)
    for (shed, day), r in latest.items():
        by[(shed[3:5], D.fromisoformat(day))].append(math.log(r["concentration_copies_per_l"] / r["pmmov_copies_per_l"]))
    out = {}
    for reg in ("SE", "WC", "NO"):
        for w in C.WINTERS:
            a, b = C.season_bounds(w)
            a = a - dt.timedelta(days=30)
            days = sorted(k[1] for k in by if k[0] == reg and a <= k[1] <= b)
            vals = {x: st.mean(by[(reg, x)]) for x in days}
            sm = {x: st.mean(vals[y] for y in days if abs((y - x).days) <= 7) for x in days}
            out[(reg, w)] = max(days, key=lambda x: sm[x]).toordinal()
    return out


def ww_route(P, up):
    """The North placed this winter from an upstream region's wastewater peak, the closed winters' peak-to-peak lag and
    the North's own wastewater-to-census offset, its closed waves read over the block weeks."""
    pk = ww_peaks(P)
    lags = [pk[("NO", w)] - pk[(up, w)] for w in C.CLOSED]
    off = [anchor(P, "NO", w) - pk[("NO", w)] for w in C.CLOSED]
    pred = pk[(up, 2027)] + st.mean(lags) + st.mean(off)
    return st.mean(window(P, P.fids("North"), int(round(pred - anchor(P, "NO", w)))) for w in C.CLOSED)


def reflex_sweep(P):
    """Every cheap route a strong analyst might file without timing the regions' waves, measured on the cut pack:
    flat rates over the season, transfers from the south by bed, the Januaries by every summary, the pool's own order
    book, the season's remainder and the peak-four-weeks shortcut. Returns {route: block before rounding}."""
    allf, south, north = P.fids(), P.fids("Southeast") + P.fids("West and Central"), P.fids("North")
    beds = dict(zip(P.roster["facility_id"], P.roster["staffed_med_surg_beds"].astype(int)))
    seas = {w: sum(P.draw_nights(f, *C.season_bounds(w)) for f in allf) for w in C.CLOSED}
    seas_s = {w: sum(P.draw_nights(f, *C.season_bounds(w)) for f in south) for w in C.CLOSED}
    jan = {w: P.block_draw(allf, w) for w in C.CLOSED}
    fA, _, _ = ask_figures(P, ask_lines(P))
    funded = sum(fA[f] for f in south)
    ndays = 151
    bs, bn = sum(beds[f] for f in south), sum(beds[f] for f in north)

    def peak28(w, fids):
        a, b = C.season_bounds(w)
        best, d = 0, a
        while d + dt.timedelta(days=27) <= b:
            best = max(best, sum(P.draw_nights(f, d, d + dt.timedelta(days=27)) for f in fids))
            d += dt.timedelta(days=7)
        return best
    a27 = C.season_bounds(2027)[0]
    sofar = sum(P.draw_nights(f, a27, C.CENSUS_END) for f in allf)
    bo = pd.read_excel(find(r"january_block_orders_.*\.xlsx", P.dir))
    book = [int(x) for x in bo["block_shifts"].dropna()]
    out = {
        "flat: the pool's mean season draw (16 members) spread over the season, four weeks": st.mean(seas_s.values()) * 28 / ndays,
        "flat: the same, 4 of 22 weeks": st.mean(seas_s.values()) * 4 / 22.0,
        "flat: the same, 4 of the chart's 21 weeks": st.mean(seas_s.values()) * 4 / 21.0,
        "flat: the lowest closed season, four weeks of 151 days": min(seas_s.values()) * 28 / ndays,
        "flat: last winter's funded shifts, four weeks of 151 days": funded * 28 / ndays,
        "flat: all 24 members' mean season draw, four weeks": st.mean(seas.values()) * 28 / ndays,
        "transfer: the south's season draw per staffed bed times the North's beds": st.mean(seas_s.values()) / bs * bn,
        "transfer: last winter's funded shifts per staffed bed times the North's beds": funded / bs * bn,
        "Januaries: mean (the default path)": st.mean(jan.values()),
        "Januaries: median": st.median(jan.values()),
        "Januaries: last three": st.mean([jan[w] for w in C.CLOSED[-3:]]),
        "Januaries: last": jan[C.CLOSED[-1]],
        "Januaries: smallest": min(jan.values()),
        "Januaries: per southern bed times all beds": st.mean(jan.values()) / bs * (bs + bn),
        "season mean times the mean January share": st.mean(seas.values()) * st.mean(jan[w] / seas[w] for w in C.CLOSED),
        "order book: last block": float(book[-1]),
        "order book: mean block": st.mean(book),
        "remainder: the usual season less this winter's draw to the pull": st.mean(seas.values()) - sofar,
        "peak four weeks of each closed season, all members": st.mean(peak28(w, allf) for w in C.CLOSED),
        "aligned: every member moved onto this winter's Southeast centre": aligned(P, "SE"),
        "aligned: every member moved onto this winter's first Southeast surge night": aligned(P, "SEfirst"),
        "aligned: every member moved onto this winter's first surge night anywhere": aligned(P, "statefirst"),
        "aligned: every member moved onto this winter's southern median centre": aligned(P, "state"),
        "eyeballed: the North at the Southeast's centre plus the mean lag": placed(P, "SE"),
        "eyeballed: the North at the Southeast's centre plus the median lag": placed(P, "SE", agg="median"),
        "eyeballed: the North's first night at the Southeast's first plus the mean lag": placed(P, "SE", onset=True),
        "eyeballed: the North's first night at the Southeast's first plus the median lag": placed(P, "SE", onset=True, agg="median"),
        "wastewater only: the North from the Southeast's peak": ww_route(P, "SE"),
    }
    return out
