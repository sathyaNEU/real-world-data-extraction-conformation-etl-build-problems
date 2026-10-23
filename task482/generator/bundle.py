"""Reads task482's cut pack the way a solver must and computes every figure from it: each plant's 2026 press VOC (used,
captured, destroyed, emitted) under the golden handling and under each rung and licensed variant, each plant's cleaning
VOC away from its presses (ask A) and each plant's gallons received and unaccounted for (ask B). golden.py, checks.py
and ceiling.py call it; verify.py recomputes the golden without it.

The golden handling of the press VOC: each production day's captured VOC (press logs through the safety data sheets,
times the plant's capture efficiency) over the oxidizer's process hours that day, and the mean airflow over them (the
historian, its UTC hours put on Central time, fan speed through the rated airflow), give the day's inlet as carbon
through the plant's carbon content; the outlet is the relation the performance tests trace across the ten oxidizers
(each test's runs on one basis, as carbon): the mean outlet of the runs with an inlet under 2,000 ppmv, and above the
knee the mean share of the inlet passed by the runs over 3,000; the day's controlled VOC is that outlet over the
day's air and hours."""
import csv
import datetime as dt
import os
import re
from collections import defaultdict

import numpy as np

K = 3.1173e-8
TONS = 2000.0
DILUTE, CONC = 2000.0, 3000.0
RENUMBERED = dt.date(2026, 4, 1)
YEAR = 2026
FILES = {
    "register": "deq_printing_plants_register_2027-02.xlsx", "press": "press_material_use_2026.csv",
    "sds": "safety_data_sheet_master_2027-01.xlsx", "hist": "oxidizer_historian_hourly_2026.csv",
    "tests": "oxidizer_performance_tests_2017_2026.pdf", "issues": "stores_cleaning_issues_2026.csv",
    "manifests": "cantrell_bend_manifests_2026.csv", "profiles": "cantrell_bend_waste_profiles_2026.pdf",
    "tickets": "wexcombe_service_tickets_2026.csv", "payments": "solvent_vendor_payments_2026.csv",
    "corvane": "corvane_invoice_export_2026.csv", "haldane": "haldane_statement_2026.xlsx",
    "catalog": "haldane_catalog_2026-04.csv", "counts": "stock_counts_2026.csv",
}


def hround(x):
    """Round half away from zero (the deliverables' rounding)."""
    return int(np.floor(abs(x) + 0.5)) * (1 if x >= 0 else -1)


def round1(x):
    return float(np.floor(abs(x) * 10 + 0.5) / 10.0) * (1 if x >= 0 else -1)


def _csv(target, key):
    with open(os.path.join(target, FILES[key]), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _sheet(target, key, name, header_row=1):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, FILES[key]), read_only=True, data_only=True)
    rows = list(wb[name].iter_rows(values_only=True))
    head = rows[header_row - 1]
    return [dict(zip(head, r)) for r in rows[header_row:] if any(v is not None for v in r)]


def pdf_text(path):
    import pypdf
    return "\n".join(p.extract_text() for p in pypdf.PdfReader(path).pages)


def central(utc):
    """UTC to US Central (daylight time from 2:00 local on 8 March to 2:00 local on 1 November 2026)."""
    if dt.datetime(2026, 3, 8, 8) <= utc < dt.datetime(2026, 11, 1, 7):
        return utc - dt.timedelta(hours=5)
    return utc - dt.timedelta(hours=6)


# ---------------------------------------------------------------------------------------------------------------------
class Inputs:
    def __init__(self, target):
        self.target = target
        reg = _sheet(target, "register", "Plants")
        self.order = [r["Plant"] for r in reg]
        self.fac, self.facno = {}, {}
        self.cf, self.washers = {}, {}
        for r in reg:
            self.fac[r["Facility no."]] = r["Plant"]
            self.facno[r["Plant"]] = r["Facility no."]
            if r["Former name"]:
                m = re.search(r"\(facility (\d{4})\)", r["Former name"])
                self.fac[m.group(1)] = r["Plant"]
            if r["Carbon content of VOC (lb C per lb VOC)"] is not None:
                self.cf[r["Plant"]] = float(r["Carbon content of VOC (lb C per lb VOC)"])
        self.ox = {}
        self.tag = {}
        for r in _sheet(target, "register", "Oxidizers"):
            n = r["Plant"]
            tags = re.findall(r"[A-Z]{3,4}-RTO\d?", r["Historian tag"])
            for t in tags:
                self.tag[t] = n
            self.ox[n] = dict(vendor=r["Manufacturer"], fixed=r["Fan drive"].startswith("Fixed"),
                              Q=float(r["Rated airflow (scfm)"]), logs=r["Historian logs"],
                              qmin=(r["Minimum fan speed (%)"] or 100) / 100.0)
        self.ce = {r["Plant"]: float(r["Capture efficiency (%)"]) / 100.0 for r in _sheet(target, "register",
                                                                                           "Capture")}
        self.controlled = [n for n in self.order if n in self.ox]
        self._sds(target)
        self._press(target)
        self._hist(target)
        self._tests(target)

    # -- safety data sheets -------------------------------------------------------------------------------------------
    def _sds(self, target):
        self.prod = {}
        for r in _sheet(target, "sds", "Products"):
            self.prod[r["Product code"]] = dict(name=r["Product name"], supplier=r["Supplier"],
                                                kind=r["Product type"].upper(), den=float(r["Density (lb/gal)"]),
                                                basis=r["VOC basis"], voc=float(r["VOC"]),
                                                water=float(r["Water (vol %)"] or 0),
                                                exempt=float(r["Exempt compounds (vol %)"] or 0))
        self.revs = []
        for r in _sheet(target, "sds", "Revision log"):
            m = re.search(r"density ([\d.]+) lb/gal and VOC ([\d.]+) per cent by weight under revision (\d+)",
                          r["Change"] or "")
            if m:
                eff = r["Effective from"]
                eff = eff.date() if isinstance(eff, dt.datetime) else eff
                self.revs.append((r["Product code"], eff, float(m.group(1)), float(m.group(2))))

    def vpg(self, code, d=None, vintage=True):
        """lb of VOC per gallon of the product as used on date d: the revision in force that day (vintage) or the
        master's current revision."""
        p = self.prod[code]
        if vintage and d is not None:
            for c, eff, den, wt in self.revs:
                if c == code and d < eff:
                    return den * wt / 100.0
        if p["basis"].startswith("%"):
            return p["den"] * p["voc"] / 100.0
        return p["voc"] * (1 - (p["water"] + p["exempt"]) / 100.0)

    def vpg_misread(self, code):
        """The natural misreading of a less-water-and-exempt figure: as pounds per gallon of the product."""
        p = self.prod[code]
        if p["basis"].startswith("%"):
            return p["den"] * p["voc"] / 100.0
        return p["voc"]

    # -- press logs ---------------------------------------------------------------------------------------------------
    def _press(self, target):
        self.day_voc = defaultdict(lambda: defaultdict(float))       # plant -> production day -> lb VOC
        self.day_voc_misread = defaultdict(lambda: defaultdict(float))
        self.window = defaultdict(dict)                               # plant -> day -> (start, end)
        self.gal_used = defaultdict(lambda: defaultdict(float))       # plant -> material -> gal
        self.rows = defaultdict(list)                                 # plant -> (start, end, lb, day)
        self.basis_rows = defaultdict(lambda: defaultdict(int))
        self.day_voc_utc = defaultdict(lambda: defaultdict(float))
        for r in _csv(target, "press"):
            n = self.fac[r["facility_no"]]
            d = dt.date.fromisoformat(r["log_date"])
            code = r["material_code"]
            q = float(r["quantity"])
            gal = q / self.prod[code]["den"] if r["uom"] == "LB" else q
            lb = gal * self.vpg(code, d)
            st = dt.datetime.strptime(r["start_local"], "%Y-%m-%d %H:%M")
            en = dt.datetime.strptime(r["end_local"], "%Y-%m-%d %H:%M")
            self.day_voc[n][d] += lb
            self.day_voc_misread[n][d] += gal * self.vpg_misread(code)
            self.gal_used[n][code] += gal
            w = self.window[n].get(d)
            self.window[n][d] = (min(w[0], st), max(w[1], en)) if w else (st, en)
            self.rows[n].append((st, en, lb, d))
            self.basis_rows[n][r["record_basis"]] += 1

    # -- historians ---------------------------------------------------------------------------------------------------
    def _hist(self, target):
        hours = defaultdict(dict)        # plant -> local hour -> production day
        for n, w in self.window.items():
            if n not in self.ox:
                continue
            for d, (st, en) in w.items():
                t = st.replace(minute=0)
                while t < en:
                    hours[n][t] = d
                    t += dt.timedelta(hours=1)
        self.proc = defaultdict(lambda: defaultdict(list))     # plant -> day -> [flow, ...] (PROCESS hours)
        self.proc_utc = defaultdict(lambda: defaultdict(list))  # plant -> UTC date -> [flow] (the UTC misreading)
        self.all_hours = defaultdict(lambda: defaultdict(list))
        self.hourly = defaultdict(dict)                         # plant -> local hour -> flow (PROCESS)
        for r in _csv(target, "hist"):
            n = self.tag[r["unit_tag"]]
            ox = self.ox[n]
            utc = dt.datetime.strptime(r["hour_beginning_utc"], "%Y-%m-%dT%H:%MZ")
            lo = central(utc)
            if r["exhaust_flow_scfm"]:
                flow = float(r["exhaust_flow_scfm"])
            else:
                flow = ox["Q"] * float(r["fan_speed_pct"]) / 100.0
            if r["mode"] == "PROCESS":
                d = hours[n].get(lo)
                if d is None:
                    raise ValueError("process hour outside a production day: %s %s" % (n, lo))
                self.proc[n][d].append(flow)
                self.proc_utc[n][utc.date()].append(flow)
                self.hourly[n][lo] = flow
            if r["mode"] != "OFF":
                self.all_hours[n][lo.date()].append(flow)

    # -- performance tests --------------------------------------------------------------------------------------------
    def _tests(self, target):
        txt = pdf_text(os.path.join(target, FILES["tests"]))
        flat = re.sub(r"\s+", " ", txt)
        heads = list(re.finditer(r"([A-Z][A-Za-z ]+?) \(facility (\d{4})\), ([A-Z]{3,4}-RTO\d?)\. Test of (\d{1,2} "
                                 r"[A-Za-z]+ \d{4}) by ([A-Za-z ]+?), report ([A-Z]+-\d{4}-\d+)\.", flat))
        self.tests = []
        for i, h in enumerate(heads):
            body = flat[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(flat)]
            basis = "propane" if "ppmv as propane" in body else "carbon"
            mult = 3.0 if basis == "propane" else 1.0
            runs = []
            for m in re.finditer(r"(?<![\d.])([123]) (\d{2}:\d{2}) ([\d.]+) ([\d.]+) ([\d,]+) ([\d,]+) ([\d.]+) "
                                 r"([\d.]+) ([\d.]+)", body):
                runs.append(dict(ci=float(m.group(3)) * mult, co=float(m.group(4)) * mult,
                                 qi=float(m.group(5).replace(",", "")), qo=float(m.group(6).replace(",", "")),
                                 mi=float(m.group(7)), mo=float(m.group(8)), dre=float(m.group(9))))
            avg = re.search(r"Average ([\d.]+) ([\d.]+) [\d,]+ [\d,]+ [\d.]+ [\d.]+ ([\d.]+)", body)
            prod = re.search(r"Production during the test: (.+?)\.(?: [A-Z]| Run)", body)
            plant = self.tag[h.group(3)]
            self.tests.append(dict(plant=plant, date=dt.datetime.strptime(h.group(4), "%d %B %Y").date(),
                                   firm=h.group(5), basis=basis, runs=runs[:3], dre=float(avg.group(3)),
                                   prod=prod.group(1) if prod else ""))
        assert len(self.tests) == 28 and all(len(t["runs"]) == 3 for t in self.tests), len(self.tests)
        self.ci = np.array([r["ci"] for t in self.tests for r in t["runs"]])
        self.co = np.array([r["co"] for t in self.tests for r in t["runs"]])

    def latest(self, n):
        return max((t for t in self.tests if t["plant"] == n), key=lambda t: t["date"])

    # -- the year by production day -----------------------------------------------------------------------------------
    def plant_days(self, n, utc=False):
        """[(day, captured lb, process hours, mean scfm)] for a controlled plant."""
        ce = self.ce[n]
        out = []
        if utc:
            # the misreading: press days joined to the historian's UTC dates
            for d in sorted(self.day_voc[n]):
                fl = self.proc_utc[n].get(d)
                if not fl:
                    continue
                out.append((d, self.day_voc[n][d] * ce, float(len(fl)), float(np.mean(fl))))
            return out
        for d in sorted(self.day_voc[n]):
            fl = self.proc[n][d]
            out.append((d, self.day_voc[n][d] * ce, float(len(fl)), float(np.mean(fl))))
        return out


# ---------------------------------------------------------------------------------------------------------------------
# the outlet relation
def _gn(model, x0, ci, co, iters=100):
    x = np.array(x0, float)
    for _ in range(iters):
        r = (model(x, ci) - co) / co
        J = np.empty((len(ci), len(x)))
        for j in range(len(x)):
            dx = np.zeros_like(x)
            dx[j] = 1e-6 * max(1.0, abs(x[j]))
            J[:, j] = ((model(x + dx, ci) - co) / co - r) / dx[j]
        step = np.linalg.lstsq(J, -r, rcond=None)[0]
        x = x + step
        if np.abs(step).max() < 1e-10:
            break
    rms = float(np.sqrt(np.mean(((model(x, ci) - co) / co) ** 2)))
    return x, rms


def hard(F, p):
    return lambda c: np.maximum(F, p * np.asarray(c, float))


def relation(I, how="golden", sel=None):
    """The outlet (ppmv as carbon) as a function of the inlet, fitted to the tests' runs (sel: a test filter)."""
    tests = [t for t in I.tests if sel is None or sel(t)]
    ci = np.array([r["ci"] for t in tests for r in t["runs"]])
    co = np.array([r["co"] for t in tests for r in t["runs"]])
    if how in ("golden", "mean"):
        F = co[ci < DILUTE].mean()
        p = (co[ci > CONC] / ci[ci > CONC]).mean()
        return hard(F, p), (F, p)
    if how == "median":
        F = float(np.median(co[ci < DILUTE]))
        p = float(np.median(co[ci > CONC] / ci[ci > CONC]))
        return hard(F, p), (F, p)
    if how == "lsq":
        x, rms = _gn(lambda x, c: np.maximum(x[0], x[1] * c), [45.0, 0.018], ci, co)
        return hard(x[0], x[1]), (x[0], x[1], rms)
    if how.startswith("smooth"):
        k = float(how[6:])
        m = lambda x, c: (x[0] ** k + (x[1] * c) ** k) ** (1.0 / k)
        x, rms = _gn(m, [45.0, 0.018], ci, co)
        return (lambda c: m(x, np.asarray(c, float))), (x[0], x[1], rms)
    if how == "interp":
        pts = sorted((np.mean([r["ci"] for r in t["runs"]]), 1 - np.mean([r["co"] for r in t["runs"]]) /
                      np.mean([r["ci"] for r in t["runs"]])) for t in tests)
        xs = np.array([a for a, b in pts])
        ys = np.array([b for a, b in pts])
        return (lambda c: (1 - np.interp(np.asarray(c, float), xs, ys)) * np.asarray(c, float)), (xs.min(), xs.max())
    if how == "linear":
        x, rms = _gn(lambda x, c: x[0] + x[1] * c, [30.0, 0.012], ci, co)
        return (lambda c: x[0] + x[1] * np.asarray(c, float)), (x[0], x[1], rms)
    raise ValueError(how)


def rms_of(I, f):
    return float(np.sqrt(np.mean(((f(I.ci) - I.co) / I.co) ** 2)))


# ---------------------------------------------------------------------------------------------------------------------
def controlled_lb(I, n, f, grain="day", utc=False):
    """The year's VOC the oxidizer let through (lb) with the outlet relation f."""
    cf = I.cf[n]
    if grain == "hour":
        # each log row's VOC spread over its hours, against the historian's hour
        ce = I.ce[n]
        lbh = defaultdict(float)
        for st, en, lb, d in I.rows[n]:
            hrs = max(1, int(round((en - st).total_seconds() / 3600)))
            for k in range(hrs):
                lbh[st.replace(minute=0) + dt.timedelta(hours=k)] += lb * ce / hrs
        tot = 0.0
        for t, q in I.hourly[n].items():
            c = lbh.get(t, 0.0) * cf / (q * 60 * K)
            tot += float(f(c)) * q * 60 * K / cf
        return tot
    tot = 0.0
    for d, cap, h, q in I.plant_days(n, utc=utc):
        c = cap / h * cf / (q * 60 * K)
        tot += float(f(c)) * q * 60 * K / cf * h
    return tot


def press_tons(I, how="golden", grain="day", sel=None, f=None, utc=False, misread=False):
    """Each plant's 2026 press VOC: dict plant -> dict(used, captured, destroyed, emitted) in tons."""
    if f is None and (how in ("golden", "mean", "median", "lsq", "interp", "linear") or how.startswith("smooth")):
        f, _ = relation(I, how, sel)
    out = {}
    for n in I.order:
        src = I.day_voc_misread if misread else I.day_voc
        used = sum(src[n].values()) / TONS
        if n not in I.ox:
            out[n] = dict(used=used, captured=0.0, destroyed=0.0, emitted=used)
            continue
        cap = used * I.ce[n]
        ctl = controlled_lb(I, n, f, grain, utc) / TONS
        out[n] = dict(used=used, captured=cap, destroyed=cap - ctl, emitted=used - cap + ctl)
    return out


def rung_tons(I, rung):
    """The ladder's rungs: R0 latest test's efficiency, R1 the mean of the plant's tests, R2 the permit's 95 per cent,
    R3 the relation at the year's mean inlet, R3m at each month's, R4 the latest test's outlet concentration on each
    day's air, R4b the latest test's outlet rate (lb/hr) over the year's process hours, R5 each oxidizer's own tests."""
    out = {}
    fg, _ = relation(I, "golden")
    for n in I.order:
        used = sum(I.day_voc[n].values()) / TONS
        if n not in I.ox:
            out[n] = used
            continue
        cap = used * I.ce[n]
        cf = I.cf[n]
        days = I.plant_days(n)
        own = [t for t in I.tests if t["plant"] == n]
        lt = I.latest(n)
        if rung == "R0":
            ctl = cap * (1 - lt["dre"] / 100.0)
        elif rung == "R1":
            ctl = cap * (1 - np.mean([t["dre"] for t in own]) / 100.0)
        elif rung == "R2":
            ctl = cap * 0.05
        elif rung in ("R3", "R3m"):
            groups = defaultdict(list)
            for d, c_, h, q in days:
                groups[d.month if rung == "R3m" else 0].append((c_, h, q))
            ctl = 0.0
            for g in groups.values():
                lb = sum(c_ for c_, h, q in g)
                air = sum(q * 60 * K * h for c_, h, q in g)
                cav = lb * cf / air
                ctl += lb * float(fg(cav)) / cav / TONS
        elif rung in ("R4", "R4m"):
            co = (np.mean([r["co"] for r in lt["runs"]]) if rung == "R4" else
                  np.mean([np.mean([r["co"] for r in t["runs"]]) for t in own]))
            ctl = sum(co * q * 60 * K / cf * h for d, c_, h, q in days) / TONS
        elif rung == "R4b":
            co = np.mean([r["co"] for r in lt["runs"]])
            qo = np.mean([r["qo"] for r in lt["runs"]])
            hrs = sum(h for d, c_, h, q in days)
            ctl = co * qo * 60 * K / cf * hrs / TONS
        elif rung == "R5":
            xs = np.array([r["ci"] for t in own for r in t["runs"]])
            ys = np.array([r["co"] for t in own for r in t["runs"]])
            if xs.max() / xs.min() < 1.4:
                ctl = cap * (1 - np.mean([t["dre"] for t in own]) / 100.0)
            else:
                A = np.vstack([np.ones_like(xs), xs]).T
                a, b = np.linalg.lstsq(A, ys, rcond=None)[0]
                ctl = sum((a + b * (c_ / h * cf / (q * 60 * K))) * q * 60 * K / cf * h for d, c_, h, q in days) / TONS
        else:
            raise ValueError(rung)
        out[n] = used - cap + ctl
    return out


def covered(t, key="emitted"):
    vals = {n: (v[key] if isinstance(v, dict) else v) for n, v in t.items()}
    return sorted(n for n, v in vals.items() if v >= 25.0)


# ---------------------------------------------------------------------------------------------------------------------
# ask A: cleaning VOC away from the presses
def profiles(I):
    txt = re.sub(r"\s+", " ", pdf_text(os.path.join(I.target, FILES["profiles"])))
    out = {}
    for m in re.finditer(r"(CB-\d{4}-0\d) .*? (Cleaning|Press operations) ([\d.]+) ", txt):
        out[m.group(1)] = (m.group(2), float(m.group(3)))
    return out


def cleaning_tons(I, vintage=True, stellar=True, kg=True, press_issues=False, all_profiles=False, credit=True,
                  washers=True, voc_pct=True, removed=True):
    """Each plant's 2026 cleaning VOC away from its presses (tons). The flags are the readings checks.py and ceiling.py
    put against the golden: the master's current revision for every issue (vintage), the tickets alone (stellar), a
    manifest's KG read as pounds (kg), issues to the presses counted, every profile credited, no credit, no washers,
    the waste's weight credited as VOC (voc_pct), and the solvent added alone (removed)."""
    out = defaultdict(float)
    for r in _csv(I.target, "issues"):
        n = I.fac[r["facility_no"]]
        if r["issued_to"].startswith("PRESS") and not press_issues:
            continue
        d = dt.date.fromisoformat(r["issue_date"])
        out[n] += float(r["quantity"]) * I.vpg(r["material_code"], d, vintage)
    prof = profiles(I)
    for r in _csv(I.target, "manifests"):
        n = I.fac[r["generator_facility_no"]]
        src, voc = prof[r["waste_profile"]]
        if (src != "Cleaning" and not all_profiles) or not credit:
            continue
        w = float(r["net_weight"]) * (2.20462 if (r["weight_unit"] == "KG" and kg) else 1.0)
        out[n] -= w * (voc / 100.0 if voc_pct else 1.0)
    if not washers:
        return {n: out[n] / TONS for n in I.order}
    for r in _csv(I.target, "tickets"):
        n = I.fac[r["facility_no"]]
        out[n] += (float(r["fresh_added_gal"]) - (float(r["spent_removed_gal"]) if removed else 0.0)) * \
            I.vpg(r["solvent_product"])
    if stellar:
        for r in _csv(I.target, "payments"):
            m = re.search(r"fresh ([\d.]+) gal (\S+), spent ([\d.]+) gal recovered", r["description"])
            if m:
                n = I.fac[r["facility_no"]]
                out[n] += (float(m.group(1)) - (float(m.group(3)) if removed else 0.0)) * I.vpg(m.group(2))
    return {n: out[n] / TONS for n in I.order}


# ---------------------------------------------------------------------------------------------------------------------
# ask B: gallons received that the counts and the press logs leave unaccounted for
ASK_B_KINDS = ("INK", "COATING", "ADHESIVE")


def catalog(I):
    cat = {}
    for r in _csv(I.target, "catalog"):
        cat[r["item_no"]] = dict(code=r["product_code"], sold=r["sold_by"], replaces=r["replaces_item"])
    old = {r["replaces"]: item for item, r in cat.items() if r["replaces"]}
    return cat, old


def unaccounted_gal(I, chain=True, by_ship=True, lb=True, returns=True):
    """Each plant's 2026 gallons of inks, coatings and adhesives received and unaccounted for. The flags: Haldane's old
    item numbers read on the current catalog (chain), the document date for the ship date (by_ship), pounds read as
    gallons (lb), returns left out (returns)."""
    cat, old = catalog(I)
    names = {}
    for code, x in I.prod.items():
        names[x["name"].upper()] = code
    recv = defaultdict(float)
    # Corvane: the item is the product code without its prefix, then the pack
    for r in _csv(I.target, "corvane"):
        n = _ship_to(I, r["SHIP_TO"])
        d = dt.datetime.strptime(r["SHIP_DATE" if by_ship else "INVOICE_DATE"], "%Y%m%d").date()
        if d.year != YEAR:
            continue
        code = "CV-" + r["ITEM"].rsplit("-", 1)[0]
        if I.prod[code]["kind"] in ASK_B_KINDS and (returns or float(r["QTY"]) > 0):
            recv[n] += float(r["QTY"])
    for r in _sheet(I.target, "haldane", "Statement detail", header_row=2):
        n = _ship_to(I, r["Ship to"])
        d = r["Ship date" if by_ship else "Doc date"]
        d = d.date() if isinstance(d, dt.datetime) else d
        if d.year != YEAR:
            continue
        doc_d = r["Doc date"].date() if isinstance(r["Doc date"], dt.datetime) else r["Doc date"]
        item = str(r["Item"])
        if chain and doc_d < RENUMBERED and item in old:
            item = old[item]
        code, sold = cat[item]["code"], cat[item]["sold"]
        if I.prod[code]["kind"] not in ASK_B_KINDS:
            continue
        q = float(r["Qty"])
        if q < 0 and not returns:
            continue
        recv[n] += q / I.prod[code]["den"] if (sold == "LB" and lb) else q
    stock = defaultdict(float)
    for r in _csv(I.target, "counts"):
        n = I.fac[r["facility_no"]]
        code = r["material_code"]
        if I.prod[code]["kind"] not in ASK_B_KINDS:
            continue
        q = float(r["quantity"])
        g = q / I.prod[code]["den"] if r["uom"] == "LB" else q
        stock[n] += g if r["count_date"].startswith("2026-01-01") else -g
    out = {}
    for n in I.order:
        used = sum(g for code, g in I.gal_used[n].items() if I.prod[code]["kind"] in ASK_B_KINDS)
        out[n] = stock[n] + recv[n] - used
    return out


def _ship_to(I, name):
    name = name.strip().upper()
    for fac, n in I.fac.items():
        if n.upper() == name:
            return n
    if name == "THAMESIDE LAMINATING":
        return [n for n in I.order if n.startswith("Kelvedon")][0]
    raise KeyError(name)
