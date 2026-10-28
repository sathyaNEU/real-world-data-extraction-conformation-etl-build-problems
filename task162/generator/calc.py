"""task162 calculations on the cut pack, never on the truth: LW-LA-04 executed day by day, the Phase 3 forecast by
replaying each day's readings through the valve settings (the golden) and by every rung, Ask A on the near districts'
raw loggers, Ask B's water balance from the outlet meter and the billing extract."""
from __future__ import annotations

import csv
import datetime as dt
import math
import os

import numpy as np

import common as K

BAR = 10.197
N_DAYS = 365


def _read(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _gmt(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M")


def prop_file(out):
    return [f for f in os.listdir(out) if f.startswith("property_extract")][0]


def read_n1(out):
    """N1 by district from LW-LA-04's Table C2, read off the shipped PDF."""
    import re
    import subprocess
    txt = subprocess.run(["pdftotext", "-layout", os.path.join(out, "LW-LA-04_DMA_leakage_assessment_method.pdf"), "-"],
                         capture_output=True, text=True, check=True).stdout
    n1 = {}
    for line in txt.splitlines():
        for code, val in re.findall(r"(NZ\d{2})\s{2,}\S.*?\s{2,}(\d\.\d{2})(?=\s|$)", line):
            n1[code] = float(val)
    return n1


def read_settings(out):
    """Each Phase 3 valve's outlet setting (metres head) from Coldbeck's schedule rev C."""
    import openpyxl
    ws = openpyxl.load_workbook(os.path.join(out, "phase3_prv_schedule_rev_C.xlsx"), read_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    head = next(i for i, r in enumerate(rows) if r and r[0] == "District")
    col = rows[head].index("Outlet setting (m)")
    return {r[0]: float(r[col]) for r in rows[head + 1:] if r and r[0]}


class Pack:
    """The pack read the way LW-LA-04 reads it: hourly arrays per district (365 days x 24 hours, NaN where no
    reading). skip_codes leaves inlet loggers of those register codes out (a rung that misses a retired code)."""

    def __init__(self, out, N1, SETTINGS, skip_codes=()):
        self.out = out
        self.N1 = N1
        self.SETTINGS = SETTINGS
        reg = _read(os.path.join(out, "logger_register.csv"))
        self.reg = reg
        self.unit = {r["logger_serial"]: r["pressure_unit"] for r in reg}
        self.where = {r["logger_serial"]: (r["district_code"], r["point"]) for r in reg}
        codes = {r["old_code"]: r["current_code"] for r in _read(os.path.join(out, "district_code_history.csv"))}
        self.codes = codes
        self.dreg = {r["district_code"]: r for r in _read(os.path.join(out, "district_register.csv"))}
        self.t0 = K.YEAR_START
        shape = (N_DAYS, 24)
        self.flow = {c: np.full(shape, np.nan) for c in self.dreg}
        nrep = {c: np.zeros(shape) for c in self.dreg}
        self.pin = {c: np.full(shape, np.nan) for c in self.dreg}
        self.azp = {c: np.full(shape, np.nan) for c in self.dreg}
        n_inlet = {}
        for r in reg:
            if r["point"] == "inlet" and r["district_code"] not in skip_codes:
                c = codes.get(r["district_code"], r["district_code"])
                n_inlet.setdefault(c, set()).add(r["district_code"])
        seen = set()
        for row in _read(os.path.join(out, "northern_zone_inlet_loggers_2025_26.csv")):
            key = (row["logger_serial"], row["reading_time_gmt"])
            if key in seen:
                continue                                   # the archive's re-sends repeat whole rows
            seen.add(key)
            dc, _ = self.where[row["logger_serial"]]
            if dc in skip_codes:
                continue
            c = codes.get(dc, dc)
            k = int((_gmt(row["reading_time_gmt"]) - self.t0).total_seconds() // 3600)
            d, h = divmod(k, 24)
            if np.isnan(self.flow[c][d, h]):
                self.flow[c][d, h] = 0.0
            self.flow[c][d, h] += float(row["flow_l_s"])
            nrep[c][d, h] += 1
            if dc == c:                                    # the district's own inlet gives its inlet pressure
                pv = float(row["pressure"])
                self.pin[c][d, h] = pv * BAR if self.unit[row["logger_serial"]] == "bar" else pv
        seen = set()
        for row in _read(os.path.join(out, "northern_zone_pressure_loggers_2025_26.csv")):
            key = (row["logger_serial"], row["reading_time_gmt"])
            if key in seen:
                continue
            seen.add(key)
            dc, _ = self.where[row["logger_serial"]]
            k = int((_gmt(row["reading_time_gmt"]) - self.t0).total_seconds() // 3600)
            d, h = divmod(k, 24)
            pv = float(row["pressure"])
            self.azp[dc][d, h] = pv * BAR if self.unit[row["logger_serial"]] == "bar" else pv
        for c in self.dreg:                                # an hour's inflow counts only when every inlet reported
            self.flow[c][nrep[c] < len(n_inlet.get(c, {c}))] = np.nan
        self.props = _read(os.path.join(out, prop_file(out)))

    # ------------------------------------------------------------------------------------------------- households
    def households_by_day(self, code, mode="dwellings", map_codes=True, cls="household"):
        """Properties of a class connected to the district each day, from the property extract, retired codes mapped to
        the current ones. Golden (dwellings): every record with a UPRN counts while connected; a record without one, a
        new build's plot record, counts while no record with a UPRN on its supply point is connected. Rungs: rows (every
        record), supply_points (each connected supply point once), uprn (records with a UPRN only); map_codes=False
        leaves retired codes out."""
        by_sp = {}
        for p in self.props:
            if p["property_class"] != cls:
                continue
            pc = self.codes.get(p["district_code"], p["district_code"]) if map_codes else p["district_code"]
            if pc != code:
                continue
            a = (dt.date.fromisoformat(p["connected"]) - self.t0.date()).days if p["connected"] else -1
            b = (dt.date.fromisoformat(p["disconnected"]) - self.t0.date()).days if p["disconnected"] else 10 ** 6
            by_sp.setdefault(p["supply_point_ref"], []).append((a, b, bool(p["uprn"])))
        hh = np.zeros(N_DAYS)
        for recs in by_sp.values():
            u, n = np.zeros(N_DAYS), np.zeros(N_DAYS)
            for a, b, has in recs:
                lo, hi = max(a, 0), min(b, N_DAYS)
                if lo < hi:
                    (u if has else n)[lo:hi] += 1
            if mode == "dwellings":
                hh += u + np.where(u > 0, 0.0, n)
            elif mode == "rows":
                hh += u + n
            elif mode == "supply_points":
                hh += (u + n) > 0
            elif mode == "uprn":
                hh += u
            else:
                raise ValueError(mode)
        return hh

    # ------------------------------------------------------------------------------------------------- the method
    def valid(self, code, closed_out=()):
        ok = ~np.isnan(self.flow[code]).any(1) & ~np.isnan(self.azp[code]).any(1) & ~np.isnan(self.pin[code]).any(1)
        for d in closed_out:
            ok[d] = False
        return ok

    def day_terms(self, code, hh):
        """Per day: MNF, allowance, NNF (l/s), AZNP (m), NDF (hours), leakage (Ml/d)."""
        n1 = self.N1[code]
        f, a = self.flow[code], self.azp[code]
        nonhh = self.households_by_day(code, cls="non-household")
        mnf = f[:, K.NIGHT_HOUR]
        allow = (hh * K.ALLOWANCE + nonhh * K.NONHH_ALLOWANCE) / 3600.0
        nnf = mnf - allow
        aznp = a[:, K.NIGHT_HOUR]
        with np.errstate(invalid="ignore"):
            ndf = np.sum((a / aznp[:, None]) ** n1, axis=1)
        return dict(mnf=mnf, allow=allow, nnf=nnf, aznp=aznp, ndf=ndf, leak=nnf * 3.6 * ndf / 1000.0)

    def month_mask(self, mi, ok):
        m = K.MONTHS[mi]
        nm = K.MONTHS[mi + 1] if mi < 11 else K.YEAR_END
        sel = np.zeros(N_DAYS, bool)
        sel[(m - self.t0).days:(nm - self.t0).days] = True
        return sel & ok

    def monthly(self, per_day, ok):
        return np.array([float(np.mean(per_day[self.month_mask(mi, ok)])) for mi in range(12)])

    def assess(self, code, hh=None, closed_out=()):
        hh = self.households_by_day(code) if hh is None else hh
        ok = self.valid(code, closed_out)
        t = self.day_terms(code, hh)
        return self.monthly(t["leak"], ok), t, ok

    # ------------------------------------------------------------------------------------------------- the forecast
    def forecast(self, code, mode="replay", S=None):
        """The 2027-28 months with the valve at S, each month as recorded in the same month of 2025-26."""
        S = self.SETTINGS[code] if S is None else S
        n1 = self.N1[code]
        ok = self.valid(code)
        t = self.day_terms(code, self.households_by_day(code))
        a, pi = self.azp[code], self.pin[code]
        if mode in ("replay", "shift", "open_loss", "feedback"):
            if mode in ("replay", "feedback"):
                a2 = a - (pi - np.minimum(pi, S))
            elif mode == "open_loss":
                a2 = a - (pi - np.minimum(pi - K.OPEN_LOSS, S))
            else:
                a2 = a - (pi[:, K.NIGHT_HOUR] - np.minimum(pi[:, K.NIGHT_HOUR], S))[:, None]
            if mode == "feedback":
                a2 = self._feedback(code, a2, t, S)
            aznp2 = a2[:, K.NIGHT_HOUR]
            with np.errstate(invalid="ignore"):
                nnf2 = t["nnf"] * (aznp2 / t["aznp"]) ** n1
                ndf2 = np.sum((a2 / aznp2[:, None]) ** n1, axis=1)
            return self.monthly(nnf2 * 3.6 * ndf2 / 1000.0, ok)
        drop_n = pi[:, K.NIGHT_HOUR] - np.minimum(pi[:, K.NIGHT_HOUR], S)
        aznp2 = t["aznp"] - drop_n
        if mode == "nightratio":
            return self.monthly(t["leak"] * (aznp2 / t["aznp"]) ** n1, ok)
        if mode == "night24":
            nnf2 = t["nnf"] * (aznp2 / t["aznp"]) ** n1
            return self.monthly(t["leak"] - (t["nnf"] - nnf2) * 3.6 * 24 / 1000.0, ok)
        out = []
        for mi in range(12):
            sel = self.month_mask(mi, ok)
            if mode == "typday":
                am, pm = a[sel].mean(0), pi[sel].mean(0)
                a2 = am - (pm - np.minimum(pm, S))
                nnf2 = t["nnf"][sel].mean() * (a2[K.NIGHT_HOUR] / am[K.NIGHT_HOUR]) ** n1
                out.append(nnf2 * 3.6 * float(np.sum((a2 / a2[K.NIGHT_HOUR]) ** n1)) / 1000.0)
            elif mode == "export_ratio":
                L, az = t["leak"][sel].mean(), t["aznp"][sel].mean()
                dn = drop_n[sel].mean()
                out.append(L * ((az - dn) / az) ** n1)
            else:
                raise ValueError(mode)
        return np.array(out)

    def forecast_days(self, code, S=None):
        """The golden's 2027-28 leakage day by day (Ml/d): each hour replayed through the setting."""
        S = self.SETTINGS[code] if S is None else S
        n1 = self.N1[code]
        t = self.day_terms(code, self.households_by_day(code))
        a, pi = self.azp[code], self.pin[code]
        a2 = a - (pi - np.minimum(pi, S))
        aznp2 = a2[:, K.NIGHT_HOUR]
        with np.errstate(invalid="ignore"):
            return t["nnf"] * (aznp2 / t["aznp"]) ** n1 * 3.6 * np.sum((a2 / aznp2[:, None]) ** n1, axis=1) / 1000.0

    def _feedback(self, code, a2, t, S, iters=4):
        """The replay with the district's own head loss refitted to its inflow (pin - azp = c + k q^1.85 over the valid
        hours) and the inflow lowered by the leakage the valve saves, iterated: a refinement the golden leaves out, its
        shift asserted inside every printed figure's cell."""
        n1 = self.N1[code]
        ok = self.valid(code)
        a, pi, q = self.azp[code], self.pin[code], self.flow[code]
        hl = pi - a
        m = ok[:, None] & ~np.isnan(hl) & ~np.isnan(q)
        x = np.clip(q[m], 0.01, None) ** 1.85
        k = np.linalg.lstsq(np.vstack([np.ones_like(x), x]).T, hl[m], rcond=None)[0][1]
        aznp = t["aznp"]
        with np.errstate(invalid="ignore"):
            leak = t["nnf"][:, None] * (a / aznp[:, None]) ** n1
            out = a2
            for _ in range(iters):
                aznp2 = out[:, K.NIGHT_HOUR]
                leak2 = (t["nnf"] * (aznp2 / aznp) ** n1)[:, None] * (out / aznp2[:, None]) ** n1
                dhl = k * (np.clip(q - (leak - leak2), 0.01, None) ** 1.85 - np.clip(q, 0.01, None) ** 1.85)
                out = a2 - dhl
        return out

    def bite_share(self, code, S=None):
        S = self.SETTINGS[code] if S is None else S
        ok = self.valid(code)
        return float(np.mean(self.pin[code][ok] > S))


# ------------------------------------------------------------------------------------------------- the call
def call(P, codes, mode="replay", n1_override=None):
    base = np.zeros(12)
    fc = np.zeros(12)
    saved = dict(P.N1)
    if n1_override is not None:
        for c in codes:
            P.N1[c] = n1_override
    try:
        for c in codes:
            b, _, _ = P.assess(c)
            base += b
            fc += P.forecast(c, mode)
    finally:
        P.N1.update(saved)
    yb, yf = float(base.mean()), float(fc.mean())
    red = yb - yf
    short = max(0.0, K.TARGET - red)
    gangs = int(math.ceil(short / K.GANG_YIELD - 1e-9)) if short > 0 else 0
    return dict(base_months=base, fc_months=fc, base=yb, fc=yf, reduction=red, shortfall=short, gangs=gangs,
                met=red >= K.TARGET)


# ------------------------------------------------------------------------------------------------- Ask A
OPEN_DAYS = list(range((dt.date(2026, 1, 12) - K.YEAR_START.date()).days,
                       (dt.date(2026, 1, 21) - K.YEAR_START.date()).days))


def ask_a(P, near, variant="golden"):
    """Each near district's 2025-26 assessed leakage (Ml/d). Variants are the rungs: rows, supply_points and uprn (the
    dwellings counted by property record, by supply point or by UPRN), unmapped (retired codes left out of the count),
    open_kept (NZ09's and NZ10's open-boundary days kept)."""
    out = {}
    for c in near:
        closed = OPEN_DAYS if (c in ("NZ09", "NZ10") and variant != "open_kept") else ()
        if variant in ("rows", "supply_points", "uprn"):
            hh = P.households_by_day(c, mode=variant)
        elif variant == "unmapped":
            hh = P.households_by_day(c, map_codes=False)
        else:
            hh = P.households_by_day(c)
        m, _, _ = P.assess(c, hh=hh, closed_out=closed)
        out[c] = float(m.mean())
    return out


# ------------------------------------------------------------------------------------------------- Ask B
def _overlap(a, b, y0, y1):
    lo, hi = max(a, y0), min(b, y1)
    return max(0, (hi - lo).days + 1)


def ask_b(out, variant="golden"):
    """The zone's 2025-26 water balance by LW-LA-04 section 8 (Ml/d). Variants are the rungs: no_certificate (the
    outlet meter as recorded), codes_unmapped (retired district codes left out of the zone), no_trunk (the trunk
    main's direct supplies left out), bill_dates (bills counted whole in the year their period ends), dedupe (identical
    bill lines dropped, the flats on a shared supply billed once); and the corridor every printed figure holds across:
    multiply (the as-found error added to the reading rather than divided out), exclusive (bill_to read as the next
    read's date)."""
    y0, y1 = dt.date(2025, 4, 1), dt.date(2026, 3, 31)
    days = (y1 - y0).days + 1
    siv = 0.0
    for r in _read(os.path.join(out, "thornholme_outlet_daily_2025_26.csv")):
        v = float(r["outlet_volume_ml"])
        if dt.date.fromisoformat(r["date"]) < K.CERT_DATE and variant != "no_certificate":
            v = v * (1.0 - K.CERT_ERROR) if variant == "multiply" else v / (1.0 + K.CERT_ERROR)
        siv += v
    siv /= days
    codes = {r["old_code"]: r["current_code"] for r in _read(os.path.join(out, "district_code_history.csv"))}
    zone = {r["district_code"] for r in _read(os.path.join(out, "district_register.csv"))} | {"NZ-TM"}
    sp_ok = set()
    for p in _read(os.path.join(out, prop_file(out))):
        c = p["district_code"] if variant == "codes_unmapped" else codes.get(p["district_code"], p["district_code"])
        if c in zone and not (variant == "no_trunk" and c == "NZ-TM"):
            sp_ok.add(p["supply_point_ref"])
    met = unm = 0.0
    lines = _read(os.path.join(out, "billing_extract_north_2025_26.csv"))
    if variant == "dedupe":
        lines = list({tuple(b.items()): b for b in lines}.values())
    for b in lines:
        if b["supply_point_ref"] not in sp_ok:
            continue
        a, z = dt.date.fromisoformat(b["bill_from"]), dt.date.fromisoformat(b["bill_to"])
        v = float(b["volume_m3"])
        if variant == "bill_dates":
            share = 1.0 if y0 <= z <= y1 else 0.0
        elif variant == "exclusive":
            share = max(0, (min(z, y1 + dt.timedelta(1)) - max(a, y0)).days) / max(1, (z - a).days)
        else:
            share = _overlap(a, z, y0, y1) / ((z - a).days + 1)
        if b["basis"] == "metered":
            met += v * share
        else:
            unm += v * share
    met, unm = met / 1000.0 / days, unm / 1000.0 / days
    unbilled = K.UNBILLED_SHARE * siv
    apparent = K.UNDER_REG * met + K.UNAUTH_SHARE * siv
    return dict(siv=siv, metered=met, unmeasured=unm, unbilled=unbilled, apparent=apparent,
                real=siv - met - unm - unbilled - apparent)
