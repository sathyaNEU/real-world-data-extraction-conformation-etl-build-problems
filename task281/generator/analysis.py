"""Every rung, the golden and every ask figure, computed from target/ alone (no world.py, no params.py).

    python3 task281/generator/analysis.py            # prints the ladder, the golden and the asks

The camera behind each image is in no column: it is the serial the Biomedical Engineering location history places
at the clinic on the image's local capture date, and its model comes from the asset register."""
import csv
import datetime as dt
import os
import re
import statistics
import sys
import zlib
import base64
from collections import Counter, defaultdict
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
PT = ZoneInfo("America/Los_Angeles")
REFERABLE_LEVELS = {"moderate NPDR", "severe NPDR", "PDR"}


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pdf_text(path):
    """The text drawn on a PDF's pages: each content stream decoded (ASCII85, then Flate) and its strings joined."""
    data = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"<<(.*?)>>\s*stream\r?\n(.*?)endstream", data, re.S):
        head, raw = m.group(1), m.group(2).strip()
        if b"ASCII85Decode" in head:
            raw = base64.a85decode(raw, adobe=raw.startswith(b"<~") or raw.endswith(b"~>"))
        if b"FlateDecode" in head:
            try:
                raw = zlib.decompress(raw)
            except zlib.error:
                continue
        for s in re.findall(rb"\((.*?)(?<!\\)\)\s*Tj", raw, re.S):
            out.append(s.replace(rb"\(", b"(").replace(rb"\)", b")").replace(rb"\\", b"\\").decode("latin-1"))
    return " ".join(out)


def utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


def mdy(s):
    return dt.datetime.strptime(s, "%m/%d/%Y").date()


class Pack:
    def __init__(self, target=TARGET):
        self.t = target
        f = {fn: os.path.join(target, fn) for fn in os.listdir(target)}
        pick = lambda pat: [p for n, p in sorted(f.items()) if re.search(pat, n)][0]
        self.results = read_csv(pick(r"^retina_ai_results_.*\.csv$"))
        self.validation = read_csv(pick(r"^local_validation_study_.*\.csv$"))
        self.orders = read_csv(pick(r"^ehr_retinal_screening_orders_.*\.csv$"))
        self.registry = read_csv(pick(r"^diabetes_registry_.*\.csv$"))
        self.outside = read_csv(pick(r"^him_outside_eye_reports_.*\.csv$"))
        self.reads = read_csv(pick(r"^pellam_overread_log_.*\.csv$"))
        self.directory = read_csv(pick(r"^clinic_directory\.csv$"))
        from openpyxl import load_workbook
        wb = load_workbook(pick(r"^biomed_asset_register_.*\.xlsx$"), read_only=True)
        self.assets = [r for r in wb["Assets"].iter_rows(min_row=2, values_only=True)]
        self.history = [r for r in wb["Location History"].iter_rows(min_row=2, values_only=True)]
        self.standard = pdf_text(pick(r"^clinical_ai_governance_standard.*\.pdf$"))
        self.protocol = pdf_text(pick(r"^validation_study_protocol.*\.pdf$"))
        self.opspec = pdf_text(pick(r"^retinacheck_operating_points\.pdf$"))
        self.agreement = pdf_text(pick(r"^pellam_reading_agreement.*\.pdf$"))
        self._setup()

    # ------------------------------------------------------------------------------------------------------------
    def _setup(self):
        # the filed facts
        self.ops = [(m.group(1), int(m.group(2))) for m in
                    re.finditer(r"(Standard|Enhanced|High|Maximum) (\d+) or above", self.opspec)]
        self.ops.sort(key=lambda o: -o[1])                       # least sensitive first
        self.floor = int(re.search(r"is at least (\d+) per cent", self.standard).group(1)) / 100.0
        self.capacity = int(re.search(r"up to ([\d,]+) referrals", self.agreement).group(1).replace(",", ""))
        self.pilot = {m.group(1): m.group(2).strip() for m in
                      re.finditer(r"Site ([ABC]) ((?:Wendmere Primary Care|Quarry Hill|Yarrowby Medical))", self.protocol)}
        # the directory crosswalk
        self.by_portal = {d["portal_site"]: d for d in self.directory}
        self.by_ehr = {d["ehr_department"]: d for d in self.directory}
        self.code_of_portal = {d["portal_site"]: d["clinic_code"] for d in self.directory}
        self.code_of_ehr = {d["ehr_department"]: d["clinic_code"] for d in self.directory}
        self.loc_of_code = {d["clinic_code"]: d["biomed_location"] for d in self.directory}
        self.codes = sorted(self.loc_of_code, key=lambda c: self.by_code(c)["portal_site"])
        # cameras: the model of each serial, and each location's placements from the move log
        norm = lambda s: s if str(s).startswith("HO-") else "HO-" + str(s)
        self.model = {}
        for tag, serial, cls, mk, model, acq, loc, status in self.assets:
            if str(cls).startswith("Retinal camera"):
                self.model[norm(serial)] = model
        moves = sorted(((r[2].date() if isinstance(r[2], dt.datetime) else r[2]), norm(r[1]), r[3], r[4])
                       for r in self.history if norm(r[1]) in self.model)
        self.spans = defaultdict(list)                           # location -> [(from, to or None, serial)]
        open_ = {}
        for d, serial, frm, to in moves:
            if (frm, serial) in open_:
                a = open_.pop((frm, serial))
                self.spans[frm].append((a, d, serial))
            open_[(to, serial)] = d
        for (loc, serial), a in open_.items():
            self.spans[loc].append((a, None, serial))
        # the current location of every camera (the Assets sheet's snapshot)
        self.snapshot = defaultdict(list)
        for tag, serial, cls, mk, model, acq, loc, status in self.assets:
            if str(cls).startswith("Retinal camera") and status == "In service":
                self.snapshot[loc].append(model)

    def by_code(self, code):
        return [d for d in self.directory if d["clinic_code"] == code][0]

    def model_at(self, loc, day):
        hits = [s for a, b, s in self.spans[loc] if a <= day and (b is None or day < b)]
        assert len(hits) == 1, (loc, day, hits)
        return self.model[hits[0]]

    # ------------------------------------------------------------------------------------------------------------
    # the validation record
    def val_rows(self, camera=True):
        out = []
        for v in self.validation:
            ref = v["final_level"] in REFERABLE_LEVELS or v["final_dme"] == "Y"
            code = self.code_of_portal[self.pilot[v["site"]]]
            d = mdy(v["capture_date"])
            out.append({"ref": ref, "ung": v["ai_result"] == "Ungradable",
                        "score": int(v["dr_score"]) if v["dr_score"] else None, "site": v["site"], "code": code,
                        "age": v["age_group"], "sex": v["sex"], "dtype": v["diabetes_type"], "a1c": v["hba1c_group"],
                        "eth": v["ethnicity"], "date": d,
                        "model": self.model_at(self.loc_of_code[code], d) if camera else None})
        return out

    @staticmethod
    def detected(r, cut):
        return r["ung"] or (r["score"] is not None and r["score"] >= cut)

    def sens(self, rows, cut):
        rr = [r for r in rows if r["ref"]]
        return sum(self.detected(r, cut) for r in rr) / len(rr) if rr else float("nan")

    # the year's screenings
    def screens(self, dating="local"):
        out = []
        acc_mrn = {o["ACCESSION"]: o["MRN"] for o in self.orders
                   if o["PROC_CODE"] == "IMG92229" and o["ORDER_STATUS"] == "Completed"}
        age = {r["MRN"]: r["AGE_GROUP"] for r in self.registry}
        for r in self.results:
            t = utc(r["Captured (UTC)"])
            day = t.astimezone(PT).date() if dating == "local" else t.date()
            code = self.code_of_portal[r["Site"]]
            out.append({"acc": r["Accession"], "code": code, "day": day, "local": t.astimezone(PT).date(),
                        "ung": r["Result"] == "Ungradable", "score": int(r["DR Score"]) if r["DR Score"] else None,
                        "model": self.model_at(self.loc_of_code[code], day),
                        "age": age.get(acc_mrn.get(r["Accession"]))})
        return out


# ---------------------------------------------------------------------------------------------------------------
def pick_point(P, cells):
    """The least sensitive vendor point whose cell meets the floor, or None (the clinic suspends AI screening)."""
    for nm, cut in P.ops:
        if cells[nm] >= P.floor:
            return nm
    return None


def ladder(P, dating="local", weights="screens", stratify=None):
    """Each rung's per-clinic cells (sensitivity at every point) and picks."""
    val = P.val_rows()
    scr = P.screens(dating=dating)
    by_clinic = defaultdict(list)
    for s in scr:
        by_clinic[s["code"]].append(s)
    out = {}
    # rung 0: the pooled validation sensitivity, applied to every clinic
    pooled = {nm: P.sens(val, cut) for nm, cut in P.ops}
    out["pooled"] = {c: (dict(pooled), pick_point(P, pooled)) for c in P.codes}
    # rung 1: the field's transport, post-stratified on the recorded case mix (age group) of each clinic's year
    by_age = {a: [r for r in val if r["age"] == a] for a in sorted({r["age"] for r in val})}
    r1 = {}
    for c in P.codes:
        mix = Counter(s["age"] for s in by_clinic[c] if s["age"])
        n = sum(mix.values())
        cells = {nm: sum(mix[a] / n * P.sens(by_age[a], cut) for a in by_age) for nm, cut in P.ops}
        r1[c] = (cells, pick_point(P, cells))
    out["casemix"] = r1
    # rung 2: the worst pre-specified subgroup at every point, applied to every clinic
    groups = []
    for key in ("age", "sex", "dtype", "a1c", "eth"):
        for v in sorted({r[key] for r in val}):
            groups.append([r for r in val if r[key] == v])
    worst = {nm: min(P.sens(g, cut) for g in groups) for nm, cut in P.ops}
    out["worst_subgroup"] = {c: (dict(worst), pick_point(P, worst)) for c in P.codes}
    # rung 3: by camera, with each clinic's camera read from the register's current snapshot
    bym = {m: [r for r in val if r["model"] == m] for m in ("NR-40", "NR-70")}
    sm = {m: {nm: P.sens(bym[m], cut) for nm, cut in P.ops} for m in bym}
    r3 = {}
    for c in P.codes:
        models = P.snapshot[P.loc_of_code[c]]
        cells = {nm: sum(sm[m][nm] for m in models) / len(models) for nm, cut in P.ops}
        r3[c] = (cells, pick_point(P, cells))
    out["snapshot"] = r3
    # the golden: by camera, each clinic's year weighted by the model behind each screening
    g = {}
    for c in P.codes:
        ss = by_clinic[c]
        if weights == "days":
            days = defaultdict(set)
            for s in ss:
                days[s["model"]].add(s["day"])
            w = {m: len(days[m]) for m in days}
        elif weights == "gradable":
            w = Counter(s["model"] for s in ss if not s["ung"])
        else:
            w = Counter(s["model"] for s in ss)
        n = sum(w.values())
        if stratify == "age":
            mix = Counter((s["model"], s["age"]) for s in ss if s["age"])
            n2 = sum(mix.values())
            cells = {}
            for nm, cut in P.ops:
                cells[nm] = sum(k / n2 * P.sens([r for r in bym[m] if r["age"] == a], cut)
                                for (m, a), k in mix.items())
        else:
            cells = {nm: sum(w[m] / n * sm[m][nm] for m in w) for nm, cut in P.ops}
        g[c] = (cells, pick_point(P, cells), {m: w[m] / n for m in w})
    out["golden"] = g
    out["by_model"] = sm
    out["counts"] = {m: (len(bym[m]), sum(r["ref"] for r in bym[m])) for m in bym}
    return out


def referrals(P, picks):
    """Screenings of the reference year the chosen points would have referred (Ungradable, or a score at or above
    the point's threshold)."""
    cut = dict(P.ops)
    n = 0
    for s in P.screens():
        nm = picks[s["code"]]
        if nm is None or s["ung"] or (s["score"] is not None and s["score"] >= cut[nm]):
            n += 1
    return n


# ---------------------------------------------------------------------------------------------------------------
# the asks
QUARTERS = [("Oct-Dec 2025", dt.date(2025, 10, 1), dt.date(2025, 12, 31)),
            ("Jan-Mar 2026", dt.date(2026, 1, 1), dt.date(2026, 3, 31)),
            ("Apr-Jun 2026", dt.date(2026, 4, 1), dt.date(2026, 6, 30)),
            ("Jul-Sep 2026", dt.date(2026, 7, 1), dt.date(2026, 9, 30))]


def quarter_of(d):
    for q, a, b in QUARTERS:
        if a <= d <= b:
            return q
    return None


def ask_overreads(P, scope="ai", pair=True, clock="local"):
    """The reading center's reads of the AI's referrals: per clinic the referrals read and the share whose closing
    grade is Referable; per quarter of the screening the average calendar days from the screening's local date to
    the closing grade's local date.
    scope 'ai' keeps the referral orders the EHR holds as referrals to the reading center; 'all' keeps every case.
    pair True takes each referral order as one unit closed by its last grade; False takes each case as a unit."""
    proc = {o["ORDER_ID"]: o for o in P.orders}
    cases = sorted(P.reads, key=lambda r: int(r["Case No"]))
    units = defaultdict(list)
    for r in cases:
        o = proc.get(r["Referral Order"])
        if scope == "ai" and (o is None or o["PROC_CODE"] != "REF7734"):
            continue
        key = r["Referral Order"] if pair else r["Case No"]
        units[key].append(r)
    gdate = lambda r: (utc(r["Graded (UTC)"]).astimezone(PT).date() if clock == "local"
                       else utc(r["Graded (UTC)"]).date())
    read, conf = Counter(), Counter()
    days = defaultdict(list)
    for key, rs in units.items():
        first = rs[0]
        o = proc.get(first["Referral Order"])
        code = P.code_of_ehr[o["DEPARTMENT"]]
        sday = mdy(first["Image Date"])
        closing = [r for r in rs if r["Final Grade"] in ("Referable", "Not referable")]
        read[code] += 1
        if closing and closing[-1]["Final Grade"] == "Referable":
            conf[code] += 1
        if closing:
            days[quarter_of(sday)].append((gdate(closing[-1]) - sday).days)
    by_clinic = {c: (read[c], conf[c] / read[c] if read[c] else float("nan")) for c in P.codes}
    by_q = {q: statistics.fmean(days[q]) for q, a, b in QUARTERS}
    return by_clinic, by_q


def ask_downtime(P, route="history"):
    """Each camera fault in the reference year (a service ticket on a retinal camera): the clinic days with no AI
    screening captured at the clinic while its camera was out of service, and the AI screenings cancelled for it.
    route 'history' ends the outage when the location history moves the next camera in; 'closed' ends it at the
    ticket's close; 'cancel_days' counts the days carrying an equipment cancellation."""
    a, b = dt.date(2025, 10, 1), dt.date(2026, 9, 30)
    tickets = [t for t in read_csv([os.path.join(P.t, fn) for fn in sorted(os.listdir(P.t))
                                    if fn.startswith("biomed_service_tickets")][0])
               if t["Equipment Class"].startswith("Retinal camera") and a <= mdy(t["Opened"]) <= b]
    norm = lambda s: s if str(s).startswith("HO-") else "HO-" + str(s)
    code_of_loc = {v: k for k, v in P.loc_of_code.items()}
    captured = defaultdict(set)
    for r in P.results:
        captured[P.code_of_portal[r["Site"]]].add(utc(r["Captured (UTC)"]).astimezone(PT).date())
    out = {}
    for t in sorted(tickets, key=lambda t: mdy(t["Opened"])):
        loc, opened = t["Location"], mdy(t["Opened"])
        code = code_of_loc[loc]
        ins = sorted((r[2].date() if isinstance(r[2], dt.datetime) else r[2]) for r in P.history
                     if r[4] == loc and norm(r[1]) in P.model and
                     (r[2].date() if isinstance(r[2], dt.datetime) else r[2]) > opened)
        back = ins[0]
        if route == "closed":
            back = mdy(t["Closed"]) if t["Closed"] else b + dt.timedelta(days=1)
        dept = P.by_code(code)["ehr_department"]
        canc = [o for o in P.orders if o["DEPARTMENT"] == dept and o["PROC_CODE"] == "IMG92229" and
                o["ORDER_STATUS"] == "Cancelled" and o["CANCEL_REASON"] == "Equipment unavailable" and
                opened <= mdy(o["ORDER_DATE"]) < back]
        if route == "cancel_days":
            days = len({o["ORDER_DATE"] for o in canc})
        else:
            days = 0
            d = opened + dt.timedelta(days=1)
            while d < back:
                if d.weekday() < 5 and d not in captured[code]:
                    days += 1
                d += dt.timedelta(days=1)
        out[t["Ticket"]] = {"clinic": code, "opened": opened, "days": days, "cancelled": len(canc)}
    return out


# ---------------------------------------------------------------------------------------------------------------
def golden(P):
    L = ladder(P)
    picks = {c: L["golden"][c][1] for c in P.codes}
    cells = {c: L["golden"][c][0] for c in P.codes}
    ov_c, ov_q = ask_overreads(P)
    return {"ladder": L, "picks": picks, "cells": cells, "referrals": referrals(P, picks),
            "overreads_clinic": ov_c, "overreads_quarter": ov_q, "downtime": ask_downtime(P)}


def main():
    P = Pack()
    G = golden(P)
    L = G["ladder"]
    print("operating points", P.ops, "floor", P.floor, "capacity", P.capacity, "pilots", P.pilot)
    print("validation by camera (n, referable):", L["counts"])
    for m, d in L["by_model"].items():
        print("  %s %s" % (m, {k: round(100 * v, 2) for k, v in d.items()}))
    for rung in ("pooled", "casemix", "worst_subgroup", "snapshot", "golden"):
        picks = {c: L[rung][c][1] for c in P.codes}
        print("%-15s %s  referrals %d" % (rung, picks, referrals(P, picks)))
    for c in P.codes:
        cells, pk, w = L["golden"][c]
        print("  %s %-24s NR-40 share %.3f  %s -> %s" % (c, P.by_code(c)["portal_site"], w.get("NR-40", 0.0),
                                                        ["%.2f" % (100 * cells[nm]) for nm, _ in P.ops], pk))
    print("overreads by clinic", {c: (n, round(100 * s, 2)) for c, (n, s) in G["overreads_clinic"].items()})
    print("overreads by quarter", {q: round(v, 3) for q, v in G["overreads_quarter"].items()})
    print("downtime", G["downtime"])


if __name__ == "__main__":
    main()
