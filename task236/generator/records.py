"""The records each system writes from task236's world: the laboratories' and point-of-care services' influenza
results as the notification gateway received them, the notification system's cases, the sentinel practices' weekly
returns and their swab results, the postcode concordance and population, the testing change register's entries and
two neighbouring extracts the analysis does not use."""
import datetime as dt
import hashlib

import numpy as np
import pandas as pd

import params as P

ILLS = ("flu", "rsv", "oth")
SETTING = {"gp": "general practice", "ed": "emergency department", "dt": "drive-through clinic",
           "inpatient": "hospital inpatient"}
METHOD = {"pcr": "PCR", "panel": "multiplex respiratory panel", "poc": "rapid antigen"}
# how each service words a result
WORDING = {
    "PHL": ("Influenza A RNA DETECTED", "Influenza B RNA DETECTED", "Influenza A/B RNA NOT DETECTED"),
    "SLT": ("Detected: Influenza A", "Detected: Influenza B", "Not detected"),
    "NGD": ("INFLUENZA A POSITIVE", "INFLUENZA B POSITIVE", "NEGATIVE"),
    "HRB": ("Influenza A detected", "Influenza B detected", "Influenza A and B not detected"),
    "CWP": ("Flu A DETECTED", "Flu B DETECTED", "Flu A/B not detected"),
    "IDL": ("Influenza A virus detected by PCR", "Influenza B virus detected by PCR", "No influenza virus detected"),
    "WPN": ("Influenza A DETECTED", "Influenza B DETECTED", "Influenza A/B NOT DETECTED"),
    "STH": ("POSITIVE - Influenza A", "POSITIVE - Influenza B", "NEGATIVE - Influenza A/B"),
}
POC_WORDING = ("Influenza A antigen detected", "Influenza B antigen detected", "Influenza A/B antigen not detected")
# how each laboratory words a preliminary positive (the final report follows)
PRELIM = {
    "PHL": ("Influenza A RNA DETECTED - preliminary, subtyping to follow", "Influenza B RNA DETECTED - preliminary, lineage to follow"),
    "SLT": ("Detected: Influenza A (preliminary report)", "Detected: Influenza B (preliminary report)"),
    "NGD": ("INFLUENZA A POSITIVE - PRELIMINARY", "INFLUENZA B POSITIVE - PRELIMINARY"),
    "HRB": ("Influenza A detected (interim result)", "Influenza B detected (interim result)"),
    "CWP": ("Flu A DETECTED - prelim", "Flu B DETECTED - prelim"),
    "IDL": ("Influenza A virus detected by PCR (preliminary)", "Influenza B virus detected by PCR (preliminary)"),
    "WPN": ("Influenza A DETECTED (PRELIMINARY)", "Influenza B DETECTED (PRELIMINARY)"),
    "STH": ("POSITIVE - Influenza A (preliminary)", "POSITIVE - Influenza B (preliminary)"),
}
ZERO_POSTCODE = ("NGD", "STH")       # services whose systems write 0000 where the request has no address
SWAB_UNTESTED = 0.011
UNTESTED_COMMENTS = ("Specimen leaked in transit; not tested", "Swab received without transport medium; not tested",
                     "Specimen received more than 7 days after collection; not tested", "Unlabelled specimen; not tested")
# postcodes of people living in other states who were tested here (visitors, seasonal workers, border towns)
INTERSTATE_POSTCODES = (2480, 2484, 2650, 2830, 3690, 3500, 4370, 4810, 4870, 2350)
LAG_DAYS = (1, 2, 3, 4, 5)
LAG_P = {"lab": (0.36, 0.33, 0.17, 0.09, 0.05), "PHL": (0.22, 0.34, 0.24, 0.13, 0.07)}


def utc_iso(local_dt):
    return (local_dt - P.UTC_OFFSET).strftime("%Y-%m-%dT%H:%M:%SZ")


def week_of(d):
    return d.isocalendar()[1]


class Records:
    def __init__(self, W, seed=P.RECORD_SEED):
        self.W = W
        self.seed = seed
        self._places()

    def _stream(self, k):
        return np.random.default_rng(self.seed * 100 + k)

    # ------------------------------------------------------------------ postcodes, the concordance, population
    def _places(self):
        rng = self._stream(1)
        used = set()
        self.postcodes = {}            # current region -> [(postcode, erp)]
        base = 9010
        for code, name, pop, *_ in P.REGIONS:
            n = P.POSTCODES_PER_REGION[code]
            w = rng.gamma(2.2, 1.0, size=n)
            erp = np.maximum(400, np.round(pop * w / w.sum())).astype(int)
            erp[-1] += pop - int(erp.sum())
            pcs = []
            for j in range(n):
                base += int(rng.integers(1, 4))
                while base in used:
                    base += 1
                used.add(base)
                pcs.append((str(base), int(erp[j])))
            self.postcodes[code] = pcs
            base += 13
        # the postcodes that moved on the boundary date: the largest ones of the old region's border, now in the new
        self.moved = {}
        for frm, to, ranks in P.MOVED:
            by_size = sorted(self.postcodes[to], key=lambda x: (-x[1], x[0]))
            for k in ranks:
                self.moved[by_size[k][0]] = frm
        self.region_of = {pc: code for code, pcs in self.postcodes.items() for pc, _ in pcs}
        self.region_on = lambda pc, d: (self.moved[pc] if pc in self.moved and d < P.BOUNDARY_DATE
                                        else self.region_of.get(pc, "OS"))

    def concordance(self):
        names = {r[0]: r[1] for r in P.REGIONS}
        rows = []
        for code, pcs in self.postcodes.items():
            for pc, _ in pcs:
                if pc in self.moved:
                    old = self.moved[pc]
                    rows.append((pc, old, names[old], "2019-07-01", (P.BOUNDARY_DATE - dt.timedelta(days=1)).isoformat()))
                    rows.append((pc, code, names[code], P.BOUNDARY_DATE.isoformat(), ""))
                else:
                    rows.append((pc, code, names[code], "2019-07-01", ""))
        return pd.DataFrame(rows, columns=["postcode", "region_code", "region_name", "effective_from", "effective_to"]).sort_values(
            ["postcode", "effective_from"]).reset_index(drop=True)

    def population(self):
        rows = [(pc, erp) for code, pcs in self.postcodes.items() for pc, erp in pcs]
        return pd.DataFrame(rows, columns=["postcode", "erp_30_june_2026"]).sort_values("postcode").reset_index(drop=True)

    # ------------------------------------------------------------------ people
    def _person(self, rng, code, illness):
        pcs = self.postcodes[code]
        w = np.array([e for _, e in pcs], dtype=float)
        pc = pcs[int(rng.choice(len(pcs), p=w / w.sum()))][0]
        if illness == "rsv":
            age = int(rng.choice([0, 1, 2, 3, 4, 70, 75, 80, 85], p=[0.24, 0.2, 0.14, 0.08, 0.06, 0.08, 0.08, 0.07, 0.05]))
            age = int(max(0, age + rng.integers(-1, 3))) if age >= 70 else age
        else:
            age = int(np.clip(rng.gamma(2.0, 19.0), 0, 98))
        sex = "F" if rng.random() < 0.53 else "M"
        if rng.random() < 0.002:
            sex = "X"
        if rng.random() < P.INTERSTATE:
            pc = str(int(rng.choice(INTERSTATE_POSTCODES)))
        key = hashlib.sha256(("%d-%s-%d" % (self.seed, code, int(rng.integers(1 << 40)))).encode()).hexdigest()[:16]
        return dict(key=key, postcode=pc, age=age, sex=sex)

    # ------------------------------------------------------------------ results through the gateway
    def _requester(self, rng, code):
        """the requesting practice's, hospital's or clinic's postcode: one of the region's postcodes"""
        pcs = self.postcodes[code]
        w = np.array([e for _, e in pcs], dtype=float)
        return pcs[int(rng.choice(len(pcs), p=w / w.sum()))][0]

    def results(self):
        rng = self._stream(2)
        tc = self.W.test_counts
        rows = []
        n_id = [0]
        acc = {}

        def nid():
            n_id[0] += 1
            return "ELR27%08d" % (n_id[0] * 7 + 3)

        def accession(svc):
            acc[svc] = acc.get(svc, 0) + int(rng.integers(1, 4))
            return "%s27-%07d" % (svc, 100000 + acc[svc])

        def service(code, d, method):
            if method == "poc":             # each region's practices hold their own block of codes
                base = 1000 * (1 + [r[0] for r in P.REGIONS].index(code))
                return "POC%04d" % int(rng.integers(base, base + 40 * P.POSTCODES_PER_REGION[code]))
            labs = P.REGION_LABS[code]
            s = labs[int(rng.integers(len(labs)))]
            if s in P.MERGED[:2] and d >= P.CHANGES["CW"][0]:
                s = P.MERGED[2]
            return s

        def released(d, svc):
            """a laboratory result reaches the gateway after the laboratory's turnaround, released in the morning
            validation round, through the working day or in the evening"""
            lag = LAG_DAYS[int(rng.choice(5, p=LAG_P["PHL" if svc == "PHL" else "lab"]))]
            u = rng.random()
            h = float(rng.uniform(5.5, 9.0) if u < 0.27 else rng.uniform(9.0, 18.0) if u < 0.81 else rng.uniform(18.0, 23.5))
            return dt.datetime.combine(d + dt.timedelta(days=lag), dt.time(0)) + dt.timedelta(hours=h)

        def lab_rows(base, svc, setting, ftype, sub, d):
            """the rows a laboratory PCR writes: a preliminary positive first where the service sends one, then the
            final report; returns the rows and the time the first reached the gateway"""
            rec = released(d, svc)
            words = WORDING[svc]
            if ftype is None:
                return [dict(base, result_id=nid(), result=words[2], result_status="F", received_utc=utc_iso(rec))], rec
            out = []
            fin = rec
            if svc in P.PRELIM_SERVICES or (P.PRELIM_ED and setting in ("ed", "inpatient")):
                out.append(dict(base, result_id=nid(), result=PRELIM[svc][0 if ftype == "A" else 1], result_status="P",
                                received_utc=utc_iso(rec)))
                lo, hi = (20.0, 60.0) if svc == "PHL" else P.FINAL_AFTER
                fin = rec + dt.timedelta(hours=float(rng.uniform(lo, hi)))
            if svc == "PHL":
                txt = ("Influenza %s RNA DETECTED" % sub) if ftype == "A" else "Influenza B/Victoria lineage RNA DETECTED"
            else:
                txt = words[0] if ftype == "A" else words[1]
            out.append(dict(base, result_id=nid(), result=txt, result_status="F", received_utc=utc_iso(fin)))
            return out, rec

        def person_base(person, svc, method, setting, d, code):
            pc = person["postcode"]
            return dict(specimen_id=accession(svc if method != "poc" else "POC"), service_code=svc,
                        service_type="point of care" if method == "poc" else "laboratory", method=METHOD[method],
                        analyte="Influenza A and B", patient_key=person["key"], sex=person["sex"], age_years=person["age"],
                        residential_postcode=pc, requester_postcode=self._requester(rng, code),
                        requester_setting=SETTING[setting], collection_date=d.isoformat())

        self.positives = []            # (person, collection date, first receipt, method, flu type, region, setting)
        for r in tc.itertuples():
            people = [self._person(rng, r.region, r.illness) for _ in range(r.tested)]
            pos_idx = set(rng.choice(r.tested, size=r.positive, replace=False).tolist()) if r.positive else set()
            for i, person in enumerate(people):
                svc = service(r.region, r.date, r.method)
                if rng.random() < P.MISSING_POSTCODE:
                    person["postcode"] = "0000" if svc in ZERO_POSTCODE else ""
                positive = i in pos_idx
                ftype = ("B" if rng.random() < P.FLU_B_SHARE else "A") if positive else None
                sub = (list(P.SUBTYPE_A)[int(rng.random() >= P.SUBTYPE_A["A(H3N2)"])]) if ftype == "A" else None
                base = person_base(person, svc, r.method, r.setting, r.date, r.region)
                if r.method == "panel":
                    rec = released(r.date, svc)
                    for an, hit in (("Influenza A", ftype == "A"), ("Influenza B", ftype == "B")):
                        rows.append(dict(base, result_id=nid(), analyte=an, result="Detected" if hit else "Not detected",
                                         result_status="F", received_utc=utc_iso(rec)))
                elif r.method == "poc":
                    rec = dt.datetime.combine(r.date, dt.time(0)) + dt.timedelta(hours=float(rng.uniform(17.5, 22.0)))
                    txt = POC_WORDING[0] if ftype == "A" else POC_WORDING[1] if ftype == "B" else POC_WORDING[2]
                    rows.append(dict(base, result_id=nid(), result=txt, result_status="F", received_utc=utc_iso(rec)))
                else:
                    out, rec = lab_rows(base, svc, r.setting, ftype, sub, r.date)
                    rows.extend(out)
                if not positive:
                    continue
                self.positives.append((person, r.date, rec, r.method, ftype, r.region, r.setting))
                # a point-of-care positive sent on for PCR, or a repeat specimen within days
                if (r.method == "poc" and rng.random() < P.POC_CONFIRM) or rng.random() < P.REPEAT:
                    d2 = r.date + dt.timedelta(days=int(rng.integers(0, 4)))
                    if d2 <= P.D1:
                        svc2 = service(r.region, d2, "pcr")
                        b2 = person_base(person, svc2, "pcr", r.setting, d2, r.region)
                        out, rec2 = lab_rows(b2, svc2, r.setting, ftype, sub, d2)
                        rows.extend(out)
                        self.positives.append((person, d2, rec2, "pcr", ftype, r.region, r.setting))
                # an emergency patient admitted and re-swabbed every few days until a swab is negative
                if r.setting == "ed" and rng.random() < P.RESWAB["65+" if person["age"] >= 65 else "<65"]:
                    shed = P.SHED[0] + float(rng.gamma(P.SHED[1], P.SHED[2]))
                    t = int(rng.integers(*P.RESWAB_GAP))
                    while True:
                        d3 = r.date + dt.timedelta(days=t)
                        if d3 > P.D1:
                            break
                        svc3 = service(r.region, d3, "pcr")
                        b3 = person_base(person, svc3, "pcr", "inpatient", d3, r.region)
                        still = t <= shed
                        out, rec3 = lab_rows(b3, svc3, "inpatient", ftype if still else None, sub, d3)
                        rows.extend(out)
                        if not still:
                            break
                        self.positives.append((person, d3, rec3, "pcr", ftype, r.region, "inpatient"))
                        t += int(rng.integers(*P.RESWAB_GAP))
        cols = ["result_id", "specimen_id", "service_code", "service_type", "method", "analyte", "result", "result_status",
                "patient_key", "sex", "age_years", "residential_postcode", "requester_postcode", "requester_setting",
                "collection_date", "received_utc"]
        df = pd.DataFrame(rows)[cols]
        df = df[df.received_utc <= utc_iso(P.PULL)]
        return df.sort_values(["received_utc", "result_id"]).reset_index(drop=True)

    # ------------------------------------------------------------------ the sentinel network
    def sentinel_returns(self):
        pr = self.W.practices
        rng = self._stream(4)
        codes = {}
        rows = []
        july = {}
        for r in pr.itertuples():
            pcode = codes.setdefault((r.region, r.practice), "SGP%03d" % (len(codes) * 7 % 997 + 101))
            week_ending = dt.date.fromisocalendar(2027, int(r.week), 7)
            size = int(r.list_size)
            if int(r.week) >= 26:            # the July quarter's list sizes
                size = july.setdefault(pcode, int(round(size * (1 + float(rng.normal(0.004, 0.018))))))
            if r.returned:
                rows.append((pcode, r.region, int(r.week), week_ending.isoformat(), size, int(r.consultations),
                             int(r.ili), "received"))
            else:
                rows.append((pcode, r.region, int(r.week), week_ending.isoformat(), size, None, None, "not received"))
        self.practice_code = codes
        out = pd.DataFrame(rows, columns=["practice_code", "region_code", "iso_week", "week_ending", "list_size",
                                          "consultations", "ili_consultations", "return_status"])
        for c in ("consultations", "ili_consultations"):
            out[c] = out[c].astype("Int64")
        return out

    def sentinel_swabs(self):
        sw = self.W.swabs
        rng = self._stream(5)
        rows = []
        for i, r in enumerate(sw.itertuples()):
            pcode = self.practice_code[(r.region, r.practice)]
            monday = dt.date.fromisocalendar(2027, int(r.week), 1)
            d = monday + dt.timedelta(days=int(rng.choice(6, p=[0.24, 0.21, 0.19, 0.17, 0.13, 0.06])))
            flu_a = r.flu_positive and rng.random() >= P.FLU_B_SHARE
            flu_b = r.flu_positive and not flu_a
            rsv = r.illness == "rsv" and rng.random() < 0.95
            cov = r.illness == "oth" and rng.random() < 0.16
            det = lambda x: "detected" if x else "not detected"
            if rng.random() < SWAB_UNTESTED:
                rows.append(("SW27-%06d" % (i * 13 + 7), pcode, d.isoformat(), "", "", "", "",
                             UNTESTED_COMMENTS[int(rng.integers(len(UNTESTED_COMMENTS)))]))
                continue
            rows.append(("SW27-%06d" % (i * 13 + 7), pcode, d.isoformat(), det(flu_a), det(flu_b), det(rsv), det(cov), ""))
        return pd.DataFrame(rows, columns=["swab_id", "practice_code", "collection_date", "influenza_a", "influenza_b",
                                           "rsv", "sars_cov_2", "lab_comment"]).sort_values(["collection_date", "swab_id"]).reset_index(drop=True)

    # ------------------------------------------------------------------ neighbouring extracts the analysis does not use
    def vaccine_doses(self):
        rng = self._stream(6)
        rows = []
        for code, name, pop, *_ in P.REGIONS:
            for w in range(14, 37):
                lvl = pop * (0.0075 * np.exp(-0.5 * ((w - 17.5) / 3.2) ** 2) + 0.0009)
                rows.append((code, w, dt.date.fromisocalendar(2027, w, 7).isoformat(), int(rng.poisson(lvl * 0.72)),
                             int(rng.poisson(lvl * 0.28))))
        return pd.DataFrame(rows, columns=["region_code", "iso_week", "week_ending", "doses_general_practice",
                                           "doses_pharmacy"])

    def turnaround(self, res):
        """each laboratory's weekly turnaround, specimen collection (taken as 10:00 on the collection date) to the
        final report reaching the gateway, by ISO week of collection"""
        f = res[(res.service_type == "laboratory") & (res.result_status == "F")].drop_duplicates("specimen_id")
        rec = pd.to_datetime(f.received_utc.str.slice(0, 19)) + P.UTC_OFFSET
        col = pd.to_datetime(f.collection_date) + pd.Timedelta(hours=10)
        h = (rec - col).dt.total_seconds() / 3600.0
        t = pd.DataFrame({"service_code": f.service_code.values, "iso_week": pd.to_datetime(f.collection_date).dt.isocalendar().week.astype(int).values,
                          "hours": h.values})
        g = t.groupby(["service_code", "iso_week"]).hours
        out = pd.DataFrame({"specimens": g.size(), "median_hours_collection_to_final": g.median().round(1),
                            "p90_hours_collection_to_final": g.quantile(0.9).round(1)}).reset_index()
        out["week_ending"] = [dt.date.fromisocalendar(2027, int(w), 7).isoformat() for w in out.iso_week]
        out = out[out.iso_week.between(14, 35)]
        return out[["service_code", "iso_week", "week_ending", "specimens", "median_hours_collection_to_final",
                    "p90_hours_collection_to_final"]].sort_values(["service_code", "iso_week"]).reset_index(drop=True)

    def register(self):
        rows = []
        names = {r[0]: r[1] for r in P.REGIONS}
        for i, (code, (d, kind, text)) in enumerate(sorted(P.CHANGES.items(), key=lambda x: (x[1][0], x[0]))):
            entered = d - dt.timedelta(days=int(3 + (i * 5) % 9))
            rows.append(("TCR-27-%03d" % (i + 4), code, names[code], d.isoformat(), text, P.PEOPLE["lab"], entered.isoformat()))
        return pd.DataFrame(rows, columns=["entry", "region_code", "region_name", "effective_date", "change", "recorded_by",
                                           "entered"])
