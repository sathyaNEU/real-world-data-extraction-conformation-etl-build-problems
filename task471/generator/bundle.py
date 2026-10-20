"""Reading the shipped pack: the two lists, their linkage, the draws, the laboratories' results conformed to nitrate as
nitrogen, and every route the ladder and the ask name, computed from target/ alone (golden.py, ceiling.py and
checks.py use it; verify.py does not)."""
import csv
import datetime as dt
import os
import re

import openpyxl

import pack as P
import world as W

DIRS = {"N", "S", "E", "W", "NORTH", "SOUTH", "EAST", "WEST"}
SUFFIXES = {"RD", "ROAD", "LN", "LANE", "DR", "DRIVE", "TRL", "TRAIL", "HWY", "HIGHWAY", "CT", "COURT", "AVE",
            "AVENUE", "ST", "STREET"}
FRAME_DATE = "2025-08-31"
CLOSE = "2026-06-30"
PRIVATE = {"W", "WELL", "2"}


def _csv(target, key):
    with open(os.path.join(target, P.FILES[key]), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def addr_key(text, num=None):
    """(house number, street name) with directions, suffixes, case and punctuation set aside"""
    t = re.sub(r"[.,#]", " ", str(text).upper()).split()
    if num is None:
        num, t = t[0], t[1:]
    rest = [w for w in t if w not in DIRS and w not in SUFFIXES]
    return int(num), " ".join(rest)


def parcel_key(text):
    d = re.sub(r"\D", "", str(text))
    return d if len(d) == 9 else None


def _iso(v):
    if isinstance(v, (dt.date, dt.datetime)):
        return v.strftime("%Y-%m-%d")
    s = str(v)
    return "%s-%s-%s" % (s[:4], s[4:6], s[6:8]) if re.fullmatch(r"\d{8}", s) else s[:10]


class Pack:
    """opts (the fork table's alternative readings): frame_date, link ("parcel or address", "parcel only",
    "address only"), results ("latest", "earliest"), earlier ("both lists", "permit list only")"""

    def __init__(self, target, frame_date=FRAME_DATE, link="parcel or address", results="latest", earlier="both lists"):
        self.target = target
        self.frame_date, self.link_mode, self.result_mode, self.earlier = frame_date, link, results, earlier
        self._read()
        self._link()
        self._sample()

    # ------------------------------------------------------------------------------------------------- reading
    def _read(self):
        t = self.target
        self.counties = _csv(t, "counties")
        self.codes = [r["COUNTY_CODE"] for r in self.counties]
        self.name = {r["COUNTY_CODE"]: r["COUNTY"] for r in self.counties}
        by_permit_name = {r["PERMIT_DB_COUNTY"]: r["COUNTY_CODE"] for r in self.counties}
        sheet_of = {r["ASSESSOR_SHEET"]: r["COUNTY_CODE"] for r in self.counties}
        # the permit list: active domestic wells drilled under permit from 1986 to the frame date
        self.permits = {k: [] for k in self.codes}
        self.permit_all = {k: [] for k in self.codes}
        for r in _csv(t, "permits"):
            k = by_permit_name[r["COUNTY"]]
            rec = dict(no=r["PERMIT_NO"], addr=addr_key(r["SITE_ADDRESS"]), city=r["SITE_CITY"].upper(),
                       parcel=parcel_key(r["PARCEL_NO"]) if r["PARCEL_NO"] else None, drilled=r["DATE_DRILLED"],
                       use=r["WELL_USE"], status=r["WELL_STATUS"])
            self.permit_all[k].append(rec)
            if (rec["use"] == "DOMESTIC" and rec["status"] == "ACTIVE"
                    and "1986-01-01" <= rec["drilled"] <= self.frame_date):
                self.permits[k].append(rec)
        # the parcel list: residential parcels the assessor records as served by a private well
        wb = openpyxl.load_workbook(os.path.join(t, P.FILES["parcels"]), read_only=True)
        self.parcels = {k: [] for k in self.codes}
        self.parcel_all = {k: [] for k in self.codes}
        for ws in wb.worksheets:
            if ws.title not in sheet_of:
                continue
            k = sheet_of[ws.title]
            rows = ws.iter_rows(values_only=True)
            head = [str(h) for h in next(rows)]
            for row in rows:
                if row[0] is None:
                    continue
                v = dict(zip(head, row))
                if "PIN" in v:
                    pid, a = v["PIN"], addr_key(v["STREET"], num=v["HOUSE_NO"])
                    code, city = v["WATER_SOURCE"], v["CITY"]
                elif "PARCEL_ID" in v:
                    pid, a, code, city = v["PARCEL_ID"], addr_key(v["SITUS_ADDRESS"]), v["WATER"], v["SITUS_CITY"]
                else:
                    pid, a = v["Parcel Number"], addr_key(v["Property Address"])
                    code, city = v["Water Service"], v["Municipality"]
                rec = dict(parcel=parcel_key(pid), addr=a, city=str(city).upper(),
                           code="" if code is None else str(code).strip())
                self.parcel_all[k].append(rec)
                if rec["code"] in PRIVATE:
                    self.parcels[k].append(rec)
        wb.close()
        # the draws
        self.draws = {k: [] for k in self.codes}
        for r in _csv(t, "manifest"):
            self.draws[r["COUNTY_CODE"]].append(r)
        # the laboratories' results, conformed: one nitrate-as-nitrogen result per kit, the latest report standing
        self.results = {}
        late = self.result_mode == "latest"
        for r in _csv(t, "hal"):
            kit = r["KIT_ID"]
            if late and r["RESULT_STATUS"] != "FINAL":
                continue
            if not late and kit in self.results:       # a reanalysed sample's earlier report comes first
                continue
            self.results[kit] = dict(county=r["COUNTY_CODE"], collected=r["COLLECTED"], n=_num(r["NO3N_MG_L"]),
                                     lab="HAL")
        wb = openpyxl.load_workbook(os.path.join(t, P.FILES["ced"]), read_only=True)
        ws = wb.worksheets[0]
        rows = ws.iter_rows(values_only=True)
        head = list(next(rows))
        ced = {}
        for row in rows:
            v = dict(zip(head, row))
            if v["Analyte"] != "Nitrate as N":
                continue
            key = v["Client Kit"]
            rep = _iso(v["Report Date"])
            if key not in ced or (rep > ced[key][0]) == late:
                ced[key] = (rep, dict(county=v["County"], collected=_iso(v["Date Sampled"]),
                                      n=0.0 if v["Qualifier"] == "U" else _num(v["Result"]), lab="CED"))
        wb.close()
        for key, (_rep, rec) in ced.items():
            self.results[key] = rec
        kin = {}
        for r in _csv(t, "kin"):
            if r["PARAMETER"] != "NITRATE":
                continue
            ver = int(r["VERSION"])
            if r["CLIENTID"] not in kin or (ver > kin[r["CLIENTID"]][0]) == late:
                n = 0.0 if r["FLAG"] == "<" else float(r["VALUE"]) / W.NO3_PER_N
                kin[r["CLIENTID"]] = (ver, dict(county=r["CNTY"], collected=_iso(r["SAMPLED"]), n=n, lab="KIN"))
        for key, (_v, rec) in kin.items():
            self.results[key] = rec
        self.requests = _csv(t, "retests")

    # ---------------------------------------------------------------------------------------------- the linkage
    def _link(self):
        """a permit and a parcel are the same well when the permit's parcel number is the parcel's, or, on a permit
        without one, when the permit's site address is the parcel's situs address"""
        self.link = {}
        for k in self.codes:
            by_pid = {p["parcel"]: p for p in self.parcel_all[k]}
            by_addr = {p["addr"]: p for p in self.parcel_all[k]}
            both = 0
            permit_parcel = {}
            for rec in self.permits[k]:
                if self.link_mode == "parcel only":
                    par = by_pid.get(rec["parcel"]) if rec["parcel"] else None
                elif self.link_mode == "address only":
                    par = by_addr.get(rec["addr"])
                else:
                    par = by_pid.get(rec["parcel"]) if rec["parcel"] else by_addr.get(rec["addr"])
                permit_parcel[rec["no"]] = par
                if par is not None and par["code"] in PRIVATE:
                    both += 1
            private_pids = {p["parcel"] for p in self.parcels[k]}
            parcel_permit = {}
            for rec in self.permits[k]:
                par = permit_parcel[rec["no"]]
                if par is not None and par["parcel"] in private_pids:
                    parcel_permit[par["parcel"]] = rec
            NP, NQ = len(self.permits[k]), len(self.parcels[k])
            self.link[k] = dict(NP=NP, NQ=NQ, NB=both, union=NP + NQ - both, Po=NP - both, Qo=NQ - both,
                                permit_parcel=permit_parcel, parcel_permit=parcel_permit)

    # ---------------------------------------------------------------------------------------------- the sample
    def _sample(self):
        """each county's tested wells: which lists drew it, which lists it is on, its first test"""
        self.sample = {}
        for k in self.codes:
            L = self.link[k]
            permits = {p["no"]: p for p in self.permits[k]}
            wells = {}
            nP = nQ = 0
            for r in self.draws[k]:
                if r["OUTCOME"] not in ("TESTED", "TESTED_EARLIER"):
                    continue
                if r["OUTCOME"] == "TESTED_EARLIER" and self.earlier != "both lists":
                    continue
                kit = r["KIT_ID"]
                w = wells.setdefault(kit, dict(kit=kit, drawnP=False, drawnQ=False, onP=False, onQ=False, addr=None))
                if r["FRAME"] == "PERMIT":
                    nP += 1
                    w["drawnP"] = w["onP"] = True
                    rec = permits[r["FRAME_RECORD"]]
                    w["addr"] = rec["addr"]
                    par = L["permit_parcel"][rec["no"]]
                    if par is not None and par["code"] in PRIVATE:
                        w["onQ"] = True
                else:
                    nQ += 1
                    w["drawnQ"] = w["onQ"] = True
                    pid = parcel_key(r["FRAME_RECORD"])
                    if w["addr"] is None:
                        w["addr"] = next(p["addr"] for p in self.parcels[k] if p["parcel"] == pid)
                    if pid in L["parcel_permit"]:
                        w["onP"] = True
            for w in wells.values():
                w["n"] = self.results[w["kit"]]["n"]
                w["y"] = w["n"] > W.STANDARD_N
            self.sample[k] = dict(wells=wells, nP=nP, nQ=nQ, fP=nP / L["NP"], fQ=nQ / L["NQ"])

    # -------------------------------------------------------------------------------------------- the estimators
    def estimate(self, k, route="KA", theta=0.5):
        s, L = self.sample[k], self.link[k]
        fP, fQ = s["fP"], s["fQ"]
        ws = list(s["wells"].values())
        y = lambda w: 1.0 if w["y"] else 0.0
        if route == "KA":           # each tested well over its chance of selection from either list
            tot = 0.0
            for w in ws:
                pi = 1 - (1 - (fP if w["onP"] else 0)) * (1 - (fQ if w["onQ"] else 0))
                tot += y(w) / pi
            return tot
        if route == "sum of rates":     # the same with the two lists' chances added for a well on both
            return sum(y(w) / ((fP if w["onP"] else 0) + (fQ if w["onQ"] else 0)) for w in ws)
        if route == "hartley":      # each list's estimate of its own wells, the wells on both split theta to 1 - theta
            tot = 0.0
            for w in ws:
                both = w["onP"] and w["onQ"]
                if w["drawnP"]:
                    tot += y(w) / fP * (theta if both else 1.0)
                if w["drawnQ"]:
                    tot += y(w) / fQ * ((1 - theta) if both else 1.0)
            return tot
        if route == "domain means":     # each list-membership group's tested share times its wells
            tot = 0.0
            for dom, size in (((True, False), L["Po"]), ((False, True), L["Qo"]), ((True, True), L["NB"])):
                g = [y(w) for w in ws if (w["onP"], w["onQ"]) == dom]
                tot += size * (sum(g) / len(g) if g else 0.0)
            return tot
        if route == "pooled":           # the tested wells' share above, times the wells on the lists
            return sum(y(w) for w in ws) / len(ws) * L["union"]
        if route == "drawn list":       # each tested well over the sampling rate of the list it was drawn from
            return sum(y(w) / (fP if w["drawnP"] else fQ) for w in ws)
        if route == "lists added":      # each list's own estimate, added
            return (sum(y(w) / fP for w in ws if w["drawnP"]) + sum(y(w) / fQ for w in ws if w["drawnQ"]))
        if route == "permit list":      # the permit list's own estimate
            return sum(y(w) / fP for w in ws if w["drawnP"])
        if route == "parcel list":
            return sum(y(w) / fQ for w in ws if w["drawnQ"])
        raise ValueError(route)

    def qualifying(self, route="KA", **kw):
        return [k for k in self.codes if self.estimate(k, route, **kw) >= W.QUALIFY]

    def counts(self, k):
        s = self.sample[k]
        ws = s["wells"].values()
        return dict(tested=len(s["wells"]), above=sum(1 for w in ws if w["y"]), nP=s["nP"], nQ=s["nQ"])

    # ------------------------------------------------------------------------------------------------- the ask
    def retests(self, by="well", channel="all", window=True, first_above=True, survey_only=True):
        """per county: the wells first tested above the standard with a retest sample collected by June 30, 2026,
        and how many of those retests were still above it. by="well" counts each well in the county the survey
        tested it in; by="request" counts it in the county on its request"""
        kit_of = {}         # (county, address) of every tested well -> its first-test kit
        county_of = {}
        first = {}
        for k in self.codes:
            for w in self.sample[k]["wells"].values():
                kit_of[(k, w["addr"])] = w["kit"]
                county_of[w["kit"]] = k
                first[w["kit"]] = w["n"]
        out = {k: [0, 0] for k in self.codes}
        seen = set()
        for r in self.requests:
            if channel == "portal" and r["CHANNEL"] != "PORTAL":
                continue
            if r["CHANNEL"] == "PORTAL":
                kit = r["ORIGINAL_KIT"] or None
            else:
                kit = kit_of.get((r["COUNTY_CODE"], addr_key(r["SHIP_TO_ADDRESS"])))
            res = self.results.get(r["RETEST_KIT"])
            if res is None:
                continue
            if survey_only and kit not in county_of:
                continue
            if window and res["collected"] > CLOSE:
                continue
            if first_above and kit is not None and first.get(kit, 0) <= W.STANDARD_N:
                continue
            k = county_of.get(kit, r["COUNTY_CODE"]) if by == "well" else r["COUNTY_CODE"]
            key = kit or r["RETEST_KIT"]
            if key in seen:
                continue
            seen.add(key)
            out[k][0] += 1
            out[k][1] += 1 if res["n"] > W.STANDARD_N else 0
        return out

    def confirmation_samples(self):
        """the cruder count: every retest sample collected by June 30 in each laboratory's county, still above or not"""
        out = {k: [0, 0] for k in self.codes}
        kits = {r["RETEST_KIT"] for r in self.requests}
        for kit, res in self.results.items():
            if kit in kits and res["collected"] <= CLOSE:
                out[res["county"]][0] += 1
                out[res["county"]][1] += 1 if res["n"] > W.STANDARD_N else 0
        return out


def _num(s):
    s = str(s).strip()
    return 0.0 if s.startswith("<") else float(s)


GOLD_ROUTES = (("KA", {}), ("sum of rates", {}), ("domain means", {}), ("hartley", dict(theta=0.0)),
               ("hartley", dict(theta=0.25)), ("hartley", dict(theta=0.5)), ("hartley", dict(theta=0.75)),
               ("hartley", dict(theta=1.0)))
WRONG_ROUTES = ("pooled", "drawn list", "lists added", "permit list", "parcel list")
