"""task304 architecture 5: every rung, the golden and the asks, computed from target/ alone.

Main call: each listed junction's expected annual injury collisions as it stands at its 2026 traffic, from the validated
record 2021 to 2025: a safety performance function (negative binomial, log link, major and minor traffic, layout and
year terms) fitted to the county's give-way and stop-controlled T, staggered and crossroads junctions, combined with the
junction's own five-year count by empirical Bayes, and carried to 2026 traffic at the window's average year level; the
benefit is that times one less the fund's crash modification factor.

Asks: the 2026 provisional collisions January to September on the county's roads by quarter and 30-day severity, and
their casualties by road user, with the force's June 2026 migration re-sends counted once (the amended copy kept), the
fatal collision unit's 30-day deaths applied, and trunk-road sections left out by the road register."""
import datetime as dt
import json
import os
import re
from collections import defaultdict

import numpy as np

from io_util import pdf_text, read_csv, read_xlsx
from nbfit import nb2

WINDOW = [2021, 2022, 2023, 2024, 2025]
PRESENT = 2026
CMF = {"X": 0.52, "T": 0.70, "ST": 0.70}       # read back from the guidance in Pack.cmf_from_guidance
GROUPS = ["Pedestrian", "Pedal cyclist", "Motorcyclist", "Car occupant"]
NEW_GROUP = {"Car": "Car occupant", "Taxi or private hire car": "Car occupant", "Pedal cycle": "Pedal cyclist",
             "Motorcycle 125cc and under": "Motorcyclist", "Motorcycle 125cc to 500cc": "Motorcyclist",
             "Motorcycle over 500cc": "Motorcyclist"}
SEV = {"Fatal": 1, "Serious": 2, "Slight": 3}
MATCH_MINUTES = 20        # a re-sent record and its old-system copy: same date and road, within these minutes
MATCH_METRES = 40         # and within these metres
DEATH_DAYS = 30           # Annex A1: a casualty who dies within 30 days of the collision is killed


def d_dmy(s):
    return dt.datetime.strptime(s, "%d/%m/%Y").date()


class Pack:
    def __init__(self, target):
        self.t = target
        self._inventory()
        self._record()
        self.cmf = self.cmf_from_guidance()
        self.listed = self.screening_list()

    def p(self, n):
        return os.path.join(self.t, n)

    # ------------------------------------------------------------------ readers
    def _inventory(self):
        head, body = read_xlsx(self.p("junction_inventory_2026.xlsx"), "Junctions")
        ix = {h: i for i, h in enumerate(head)}
        self.years = sorted(int(h.split("_")[-1]) for h in head if h.startswith("aadt_major_"))
        self.nodes = {}
        self.former = {}
        for r in body:
            node = r[ix["node"]]
            self.nodes[node] = dict(node=node, name=r[ix["junction_name"]], layout=r[ix["layout"]],
                                    control=r[ix["control"]], district=r[ix["district"]],
                                    roads="%s / %s" % (r[ix["major_road"]], r[ix["minor_road"]]),
                                    maj={y: float(r[ix["aadt_major_%d" % y]]) for y in self.years},
                                    mnr={y: float(r[ix["aadt_minor_%d" % y]]) for y in self.years})
            if r[ix["former_node"]]:
                self.former[r[ix["former_node"]]] = node

    def _record(self):
        head, body = read_csv(self.p("collision_records_2016_2025.csv"))
        ix = {h: i for i, h in enumerate(head)}
        self.counts = defaultdict(int)           # (node, year) -> injury collisions
        self.n_records = len(body)
        for r in body:
            node = r[ix["junction_node"]].strip()
            if not node:
                continue
            node = self.former.get(node, node)
            y = d_dmy(r[ix["collision_date"]]).year
            self.counts[(node, y)] += 1

    def cmf_from_guidance(self):
        txt = " ".join(pdf_text(self.p("junction_safety_fund_guidance_2027.pdf")).split())
        x = float(re.search(r"Crossroads \(four arms\) (\d\.\d\d)", txt).group(1))
        t = float(re.search(r"T junction or staggered junction (\d\.\d\d)", txt).group(1))
        return {"X": x, "T": t, "ST": t}

    def screening_list(self):
        txt = pdf_text(self.p("network_screening_2026.pdf"))
        nodes = re.findall(r"\b(J\d{4,5})\b", txt)
        return [n for n in nodes if n in self.nodes]

    def reference(self):
        return [n for n, v in self.nodes.items() if v["layout"] in ("T", "ST", "X") and v["control"] in ("GW", "STOP")]

    def screened_by_rule(self, minimum=12):
        return sorted(n for n in self.reference() if sum(self.counts[(n, y)] for y in WINDOW) >= minimum)

    # ------------------------------------------------------------------ the safety performance function
    def design(self, rows, form="majmin", stx=True, yeardum=True, years=WINDOW):
        cols = [np.ones(len(rows)), np.array([r["layout"] == "X" for r in rows], dtype=float)]
        if stx:
            cols.append(np.array([r["layout"] == "ST" for r in rows], dtype=float))
        if form == "majmin":
            cols += [np.log([r["maj"] for r in rows]), np.log([r["mnr"] for r in rows])]
        else:
            cols += [np.log([r["maj"] + r["mnr"] for r in rows])]
        if yeardum:
            cols += [np.array([r["year"] == y for r in rows], dtype=float) for y in years[1:]]
        return np.column_stack(cols)

    def spf(self, form="majmin", stx=True, yeardum=True, years=WINDOW, kmode="mle"):
        rows = []
        for n in self.reference():
            v = self.nodes[n]
            for y in years:
                rows.append(dict(node=n, layout=v["layout"], maj=v["maj"][y], mnr=v["mnr"][y], year=y,
                                 n=self.counts[(n, y)]))
        X = self.design(rows, form, stx, yeardum, years)
        y = np.array([r["n"] for r in rows], dtype=float)
        b, a, ll = nb2(X, y)
        fit = np.exp(X @ b)
        if kmode == "moments":
            a = max(float((((y - fit) ** 2 - fit)).sum() / (fit ** 2).sum()), 1e-3)
        return dict(b=b, a=a, ll=ll, form=form, stx=stx, yeardum=yeardum, years=years, rows=rows, fit=fit)

    def predict(self, m, node, year, level_years=None):
        """Predicted injury collisions a year at the node's traffic in `year`, at the average of the model's year levels
        over `level_years` (the window when the model has year terms)."""
        v = self.nodes[node]
        if not m["yeardum"]:
            levels = [m["years"][0]]
        else:
            levels = level_years or [y for y in m["years"] if y in WINDOW]
        out = 0.0
        for ly in levels:
            r = dict(layout=v["layout"], maj=v["maj"][year], mnr=v["mnr"][year], year=ly)
            out += float(np.exp(self.design([r], m["form"], m["stx"], m["yeardum"], m["years"]) @ m["b"])[0])
        return out / len(levels)

    # ------------------------------------------------------------------ the main call
    def junction_figures(self, m=None, level="mean"):
        m = m or self.spf()
        out = {}
        for node in self.listed:
            v = self.nodes[node]
            mus = [self.predict(m, node, y, [y] if m["yeardum"] else None) for y in WINDOW]
            musum = sum(mus)
            obs = sum(self.counts[(node, y)] for y in WINDOW)
            w = 1.0 / (1.0 + m["a"] * musum)
            lev = [y for y in WINDOW] if level == "mean" else [WINDOW[-1]]
            mu26 = self.predict(m, node, PRESENT, lev if m["yeardum"] else None)
            eb = (w * musum + (1 - w) * obs) / musum * mu26
            cmf = self.cmf[v["layout"]]
            aadt_win = sum(v["maj"][y] + v["mnr"][y] for y in WINDOW)
            out[node] = dict(node=node, name=v["name"], layout=v["layout"], cmf=cmf, obs=obs, obs_year=obs / 5.0,
                             mu_window=musum, mu2026=mu26, w=w, expected=eb, benefit=eb * (1 - cmf),
                             obs_benefit=obs / 5.0 * (1 - cmf), spf_benefit=mu26 * (1 - cmf),
                             traffic_obs_benefit=obs / 5.0 * mu26 / (musum / 5.0) * (1 - cmf),
                             rate_mev=obs / (aadt_win * 365 / 1e6))
        return out

    # ------------------------------------------------------------------ the licensed family of fits
    FAMILY = [
        ("junction-year, year terms (the golden)", dict()),
        ("junction-year, no year terms", dict(yeardum=False)),
        ("junction-year, 2025 year level", dict(level="last")),
        ("junction-year, moment overdispersion", dict(kmode="moments")),
        ("junction-year, staggered pooled with T", dict(stx=False)),
        ("five-year site totals", dict(unit="total")),
        ("five-year site totals, staggered pooled with T", dict(unit="total", stx=False)),
        ("layout-split junction-year (crossroads; T and staggered)", dict(groups=[("X",), ("T", "ST")])),
        ("layout-split junction-year (each layout)", dict(groups=[("X",), ("T",), ("ST",)])),
        ("layout-split five-year totals (crossroads; T and staggered)", dict(unit="total", groups=[("X",), ("T", "ST")])),
        ("layout-split five-year totals (each layout)", dict(unit="total", groups=[("X",), ("T",), ("ST",)])),
        ("five-year site totals on 2026 traffic", dict(unit="total", cov26=True)),
        ("junction-year, stop-control term", dict(ctrl=True)),
        ("five-year site totals, stop-control term", dict(unit="total", ctrl=True)),
        ("junction-year, at the 2021 to 2025 traffic", dict(window=True)),
    ]

    def _fit_group(self, layouts, unit, stx, yeardum, kmode, ctrl=False, cov26=False):
        rows = []
        for n in self.reference():
            v = self.nodes[n]
            if v["layout"] not in layouts:
                continue
            if unit == "year":
                for y in WINDOW:
                    rows.append(dict(layout=v["layout"], maj=v["maj"][y], mnr=v["mnr"][y], year=y, n=self.counts[(n, y)],
                                     off=0.0, stop=v["control"] == "STOP"))
            else:
                if cov26:
                    maj, mnr = v["maj"][PRESENT], v["mnr"][PRESENT]
                else:
                    maj, mnr = float(np.mean([v["maj"][y] for y in WINDOW])), float(np.mean([v["mnr"][y] for y in WINDOW]))
                rows.append(dict(layout=v["layout"], maj=maj, mnr=mnr, year=None, n=sum(self.counts[(n, y)] for y in WINDOW),
                                 off=float(np.log(len(WINDOW))), stop=v["control"] == "STOP"))
        present = sorted(set(r["layout"] for r in rows))
        terms = []
        if "X" in present and len(present) > 1:
            terms.append("X")
        if stx and "ST" in present and len(present) > 1:
            terms.append("ST")
        years = WINDOW if (unit == "year" and yeardum) else []

        def X_(rr):
            cols = [np.ones(len(rr))] + [np.array([r["layout"] == t for r in rr], dtype=float) for t in terms]
            cols += [np.log([r["maj"] for r in rr]), np.log([r["mnr"] for r in rr])]
            cols += [np.array([r["year"] == y for r in rr], dtype=float) for y in years[1:]]
            if ctrl:
                cols.append(np.array([r["stop"] for r in rr], dtype=float))
            return np.column_stack(cols)
        X = X_(rows)
        y = np.array([r["n"] for r in rows], dtype=float)
        off = np.array([r["off"] for r in rows])
        b, a, ll = nb2(X, y, off)
        if kmode == "moments":
            fit = np.exp(X @ b + off)
            a = max(float((((y - fit) ** 2 - fit)).sum() / (fit ** 2).sum()), 1e-3)
        return dict(b=b, a=a, X_=X_, years=years, terms=terms)

    def family_benefits(self, unit="year", stx=True, yeardum=True, kmode="mle", level="mean", groups=None, ctrl=False,
                        cov26=False, window=False):
        groups = groups or [("T", "ST", "X")]
        out = {}
        for g in groups:
            m = self._fit_group(g, unit, stx, yeardum, kmode, ctrl, cov26)

            def mu(v, traffic_year, level_year, mean_traffic=False):
                maj = float(np.mean([v["maj"][y] for y in WINDOW])) if mean_traffic else v["maj"][traffic_year]
                mnr = float(np.mean([v["mnr"][y] for y in WINDOW])) if mean_traffic else v["mnr"][traffic_year]
                if mean_traffic and cov26:
                    maj, mnr = v["maj"][PRESENT], v["mnr"][PRESENT]
                r = dict(layout=v["layout"], maj=maj, mnr=mnr, year=level_year, stop=v["control"] == "STOP")
                return float(np.exp(m["X_"]([r]) @ m["b"])[0])
            for node in self.listed:
                v = self.nodes[node]
                if v["layout"] not in g:
                    continue
                if unit == "year":
                    mus = [mu(v, y, y) for y in WINDOW]
                    lev = WINDOW if level == "mean" else [WINDOW[-1]]
                    mu26 = float(np.mean([mu(v, PRESENT, ly) for ly in lev])) if m["years"] else mu(v, PRESENT, None)
                    musum = sum(mus)
                else:
                    musum = len(WINDOW) * mu(v, None, None, mean_traffic=True)
                    mu26 = mu(v, PRESENT, None)
                if window:
                    mu26 = musum / len(WINDOW)
                obs = sum(self.counts[(node, y)] for y in WINDOW)
                w = 1.0 / (1.0 + m["a"] * musum)
                eb = (w * musum + (1 - w) * obs) / musum * mu26
                out[v["name"]] = dict(benefit=eb * (1 - self.cmf[v["layout"]]), expected=eb, k=m["a"], w=w,
                                      model=mu26 * (1 - self.cmf[v["layout"]]))
        return out

    def family(self):
        return {label: self.family_benefits(**spec) for label, spec in self.FAMILY}

    def ladder(self, figs=None):
        figs = figs or self.junction_figures()

        def top(key):
            s = sorted(figs.values(), key=lambda r: -r[key])
            return s[0]["name"], s[0][key] / s[1][key], s
        return {"rate": top("rate_mev"), "observed": top("obs_benefit"), "traffic_observed": top("traffic_obs_benefit"),
                "model_only": top("spf_benefit"), "golden": top("benefit")}

    # ------------------------------------------------------------------ the asks (2026 provisional data)
    def road_register(self):
        """Register sections: a classified road's sections each span the eastings between their start and end grid
        references (the roads are registered on an east-west line); C-class and unclassified roads have one entry."""
        head, body = read_csv(self.p("road_network_register_2026.csv"))
        ix = {h: i for i, h in enumerate(head)}
        reg = []
        for r in body:
            if r[ix["start_easting"]]:
                e0, e1 = sorted((int(r[ix["start_easting"]]), int(r[ix["end_easting"]])))
            else:
                e0, e1 = None, None
            reg.append(dict(road=r[ix["road_number"]], e0=e0, e1=e1, auth=r[ix["highway_authority"]]))
        return reg

    def county_road(self, road, easting, reg=None):
        """The register's section containing the collision's easting on its road (C-class and unclassified roads by
        their own entries) decides whether the county is its highway authority."""
        reg = reg or self.road_register()
        key = "C" if road.startswith("C") else road
        secs = [s for s in reg if s["road"] == key]
        if not secs:
            raise KeyError("road %s is not in the register" % road)
        for s in secs:
            if s["e0"] is None or s["e0"] <= easting < s["e1"] or (easting == s["e1"] == max(x["e1"] for x in secs)):
                return s["auth"] == "Ardleshire County Council"
        raise KeyError("easting %d on %s is in no register section" % (easting, road))

    def sections_hit(self, road, easting, reg=None):
        reg = reg or self.road_register()
        key = "C" if road.startswith("C") else road
        return [s for s in reg if s["road"] == key and (s["e0"] is None or s["e0"] <= easting < s["e1"])]

    def provisional(self, dedupe="match", deaths="match", trunk="register"):
        """Collisions January to September 2026 (one record each), with casualties and the true quarter."""
        reg = self.road_register()
        head, body = read_csv(self.p("police_collisions_2026_jan_may.csv"))
        ix = {h: i for i, h in enumerate(head)}
        old = {}
        for r in body:
            hh, mm = r[ix["collision_time"]].split(":")
            d = d_dmy(r[ix["collision_date"]])
            old[r[ix["accident_ref"]]] = dict(ref=r[ix["accident_ref"]], date=d,
                                              t=dt.datetime(d.year, d.month, d.day, int(hh), int(mm)),
                                              e=int(r[ix["easting"]]), n=int(r[ix["northing"]]), road=r[ix["first_road"]],
                                              cas=[], src="old")
        hk, bk = read_csv(self.p("police_casualties_2026_jan_may.csv"))
        kx = {h: i for i, h in enumerate(hk)}
        for r in bk:
            ctype = r[kx["casualty_type"]]
            old[r[kx["accident_ref"]]]["cas"].append(dict(sev=int(r[kx["casualty_severity"]]),
                                                          sex="M" if r[kx["sex"]] == "1" else "F", age=int(r[kx["age"]]),
                                                          group=ctype if ctype in GROUPS else None))
        doc = json.load(open(self.p("police_export_2026_jun_sep.json"), encoding="utf-8"))
        new = []
        for c in doc["collisions"]:
            t = dt.datetime.fromisoformat(c["occurred"]).replace(tzinfo=None)
            vt = {v["vehicle"]: v["type"] for v in c["vehicles"]}
            cas = []
            for k in c["casualties"]:
                g = "Pedestrian" if k["class"] == "Pedestrian" else NEW_GROUP.get(vt.get(k["vehicle"]))
                cas.append(dict(sev=SEV[k["severity"]], sex=k["sex"], age=k["age"], group=g))
            new.append(dict(ref=c["collision_id"], date=t.date(), t=t, e=c["easting"], n=c["northing"], road=c["road"],
                            cas=cas, src="new", status=c["record_status"]))
        # the migration's re-sends: a new-system record dated before 1 June 2026 is a migrated collision; its old-system
        # copy is the record on the same date and road within 20 minutes and 40 metres
        twins = {}
        if dedupe == "match":
            byday = defaultdict(list)
            for o in old.values():
                byday[(o["date"], o["road"])].append(o)
            for c in new:
                if c["date"] >= dt.date(2026, 6, 1):
                    continue
                cands = [o for o in byday[(c["date"], c["road"])]
                         if abs((o["t"] - c["t"]).total_seconds()) <= MATCH_MINUTES * 60
                         and np.hypot(o["e"] - c["e"], o["n"] - c["n"]) <= MATCH_METRES]
                if len(cands) == 1:
                    twins[cands[0]["ref"]] = c["ref"]
        if dedupe == "match":
            recs = [o for o in old.values() if o["ref"] not in twins] + new
        elif dedupe == "ref":                     # distinct references only: the re-sends counted twice
            recs = list(old.values()) + new
        else:                                     # drop the new system's pre-June records, keep the first submission
            recs = list(old.values()) + [c for c in new if c["date"] >= dt.date(2026, 6, 1)]
        # 30-day deaths from the fatal collision investigation unit
        if deaths == "match":
            head, body = read_xlsx(self.p("fatal_casualty_notifications_2026.xlsx"), "Notifications 2026")
            hx = {h: i for i, h in enumerate(head)}
            byday = defaultdict(list)
            for c in recs:
                byday[(c["date"], c["road"])].append(c)
            self.notif_matched = 0
            for r in body:
                cd = d_dmy(r[hx["collision_date"]]) if isinstance(r[hx["collision_date"]], str) else r[hx["collision_date"]].date()
                dd = d_dmy(r[hx["date_of_death"]]) if isinstance(r[hx["date_of_death"]], str) else r[hx["date_of_death"]].date()
                if (dd - cd).days > DEATH_DAYS:
                    continue
                hh, mm = str(r[hx["approx_time"]]).split(":")[:2]
                tt = dt.datetime(cd.year, cd.month, cd.day, int(hh), int(mm))
                sex = "M" if r[hx["casualty_sex"]] == "Male" else "F"
                cands = [c for c in byday[(cd, r[hx["road"]])] if abs((c["t"] - tt).total_seconds()) <= 1800
                         and any(k["sex"] == sex and k["age"] == int(r[hx["casualty_age"]]) for k in c["cas"])]
                if len(cands) == 1:
                    self.notif_matched += 1
                    k = [k for k in cands[0]["cas"] if k["sex"] == sex and k["age"] == int(r[hx["casualty_age"]])][0]
                    k["sev"] = 1
        if trunk == "register":
            recs = [c for c in recs if self.county_road(c["road"], c["e"], reg)]
        elif trunk == "road":
            trunk_roads = {s["road"] for s in reg if s["auth"] != "Ardleshire County Council"}
            recs = [c for c in recs if c["road"] not in trunk_roads]
        elif trunk == "classified":                # only the register's numbered roads, unclassified left out
            recs = [c for c in recs if c["road"] != "U" and self.county_road(c["road"], c["e"], reg)]
        for c in recs:
            c["q"] = (c["date"].month - 1) // 3 + 1
            c["sev"] = min(k["sev"] for k in c["cas"])
        return recs

    def ask_a(self, **kw):
        recs = self.provisional(**kw)
        a = {(q, s): 0 for q in (1, 2, 3) for s in (1, 2, 3)}
        for c in recs:
            a[(c["q"], c["sev"])] += 1
        return a

    def ask_b(self, **kw):
        recs = self.provisional(**kw)
        b = {(q, g): 0 for q in (1, 2, 3) for g in GROUPS}
        for c in recs:
            for k in c["cas"]:
                if k["group"]:
                    b[(c["q"], k["group"])] += 1
        return b


def golden(target):
    pk = Pack(target)
    figs = pk.junction_figures()
    lad = pk.ladder(figs)
    return pk, figs, lad
