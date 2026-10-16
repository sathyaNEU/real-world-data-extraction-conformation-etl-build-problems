"""task233 records: the 2026 survey frame at the release extract, the 2025 final file, the 2025 follow-up's outcomes and
its case crosswalk, the school register, the activity code list, the examination points file and the distractors.

Everything is drawn from the world in sim.py; nothing here changes a leaver's destination or nonresponse."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P
import sim

ABLAB = {3: "AB1", 2: "AB2", 1: "AB3", 0: "AB4"}
CUTS = {3: (480, 625), 2: (360, 479), 1: (240, 359), 0: (95, 239)}
APPEAL = 0.03                     # leavers whose points rose across a band line in the October appeals
REVISED_ONLY = 0.015              # leavers whose points rose on appeal without crossing a line
ONLINE = (0.70, 0.52)             # online share of returns, affluent to deprived
HE_ABROAD = 0.08
SUB_APP, SUB_UNEMP = 0.60, 0.65
ROUTES = [("adviser visit", .35), ("telephone", .30), ("benefits record", .15), ("college enrolment record", .12),
          ("employer record", .08)]
FCODE = {0: "F01", 1: "F02", 5: "F03", 6: "F04", 3: "F05", 7: "F06", 8: "F07"}    # detailed activity -> field code
TYPES = ["Community School", "Community College", "High School", "Secondary School", "Academy", "College",
         "Comprehensive School", "Grammar School"]
QUAL = ["", "North ", "South ", "East ", "West ", "Upper ", "Lower ", "Central "]


def _ts(x):
    return x.strftime("%Y-%m-%dT%H:%M:%SZ")


def _hours_online():
    """hour of day (UTC) an online return comes in: little overnight, a lunchtime rise, most in the evening"""
    w = np.array([1.2, .6, .3, .2, .2, .3, .8, 1.6, 2.4, 2.8, 3.0, 3.4, 4.2, 4.0, 3.6, 3.6, 4.0, 4.8, 6.0, 7.4, 8.2, 7.6,
                  5.4, 2.8])
    return w / w.sum()


def detail(cat, u4):
    """the five release destinations split into the activities the forms ask about: 0 HE, 1 FE, 5 apprenticeship,
    6 other training, 3 employment, 7 unemployed and seeking work, 8 not working or studying"""
    out = np.where(cat == 0, 0, np.where(cat == 1, 1, np.where(cat == 3, 3, 0)))
    out = np.where(cat == 2, np.where(u4 < SUB_APP, 5, 6), out)
    out = np.where(cat == 4, np.where(u4 < SUB_UNEMP, 7, 8), out)
    return out


LDS1 = {0: "H", 1: "F", 5: "A", 6: "T", 3: "E", 7: "U", 8: "N"}
LDS2_2025 = {0: "1", 1: "2", 5: "3", 6: "4", 3: "5", 7: "6", 8: "7"}
LDS2_2026 = {0: "1", 1: "3", 5: "4", 6: "5", 3: "6", 7: "7", 8: "8"}     # code 2: higher education outside the island
DEST = ["HE", "FE", "APP", "EMP", "NEET"]


def code_list():
    rows = [("LDS-1", "H", "Higher education course", "HE"), ("LDS-1", "F", "Further education course", "FE"),
            ("LDS-1", "A", "Apprenticeship", "APP"), ("LDS-1", "T", "Other training programme", "APP"),
            ("LDS-1", "E", "Employment", "EMP"), ("LDS-1", "U", "Unemployed and seeking work", "NEET"),
            ("LDS-1", "N", "Not working or studying (caring, illness, other)", "NEET"),
            ("LDS-2", "1", "Higher education course on the island", "HE"),
            ("LDS-2", "2", "Higher education course outside the island", "HE"),
            ("LDS-2", "3", "Further education course", "FE"), ("LDS-2", "4", "Apprenticeship", "APP"),
            ("LDS-2", "5", "Other training programme", "APP"), ("LDS-2", "6", "Employment", "EMP"),
            ("LDS-2", "7", "Unemployed and seeking work", "NEET"),
            ("LDS-2", "8", "Not working or studying (caring, illness, other)", "NEET")]
    return pd.DataFrame(rows, columns=["form", "activity_code", "activity", "destination"])


class Records:
    def __init__(self, W):
        self.W = W
        self.rng = np.random.default_rng(P.SEED + 7)
        self.school_codes = [s[0] for s in W.school]
        self._school_names()

    def _school_names(self):
        rng = np.random.default_rng(P.SEED + 8)
        places = ["Harbour Road", "Mill Lane", "Oak Park", "Church Street", "Castle Hill", "Market Square", "Station Road",
                  "Bridge Street", "Green Lane", "Park View", "Elm Grove", "Ash Grove", "Cedar Lane", "Hillside", "Meadowbank",
                  "Seaview", "Glenview", "Woodlands", "Brookside", "Quay Street", "Chapel Road", "Orchard Road", "Well Street",
                  "Strand Road", "Spinner Lane", "Tower Hill", "Forge Lane", "Ferry Road", "Abbey Lane", "Rope Walk",
                  "Lime Kiln Road", "Weaver Street", "Bell Lane", "Moor Road", "North Parade", "South Parade", "Long Walk",
                  "Fair Green", "Pound Lane", "Salt Hill", "Shore Road", "Gate Street", "Cooper Street", "Tannery Lane",
                  "Kiln Road", "Pier Road", "Upper Green", "Sandy Lane", "Rock Road", "Cross Street", "Beech Hill",
                  "Willow Bank", "Larch Hill", "Thorn Road", "Holly Bank", "Laurel Hill", "Rowan Park", "Hazel Grove",
                  "Birch Road", "Alder Way", "Furze Hill", "Heather Road", "Clover Hill", "Fern Road", "Ivy Lane",
                  "Bramble Way", "Primrose Hill", "Daisy Hill", "Sorrel Road", "Mallow Street", "Kestrel Way", "Heron Road",
                  "Curlew Road", "Lark Hill", "Swallow Lane", "Wren Street", "Finch Road", "Plover Way", "Tern Road",
                  "Gannet Way", "Puffin Road", "Osprey Lane", "Merlin Park", "Raven Hill", "Rook Lane", "Jackdaw Street",
                  "Starling Road", "Linnet Lane", "Thrush Hill", "Robin Park", "Sparrow Road", "Martin Street", "Swift Lane",
                  "Teal Road", "Widgeon Way", "Snipe Lane", "Dunlin Road", "Knot Street", "Sanderling Way", "Godwit Road",
                  "Whimbrel Lane", "Shearwater Road", "Fulmar Way", "Kittiwake Road", "Guillemot Lane", "Razorbill Road",
                  "Cormorant Way", "Skerry Road", "Eider Lane", "Scoter Road", "Grebe Street", "Coot Lane", "Moorhen Road",
                  "Rail Street", "Crake Lane", "Bittern Road", "Egret Way", "Spoonbill Lane", "Stork Road", "Crane Street",
                  "Bustard Way", "Quail Lane", "Partridge Road", "Pheasant Street", "Grouse Lane", "Ptarmigan Road",
                  "Capercaillie Way", "Woodcock Lane", "Lapwing Road", "Dotterel Street", "Ringlet Lane", "Fritillary Road",
                  "Brimstone Way", "Peacock Lane", "Comma Street", "Skipper Road", "Hairstreak Way", "Copper Lane"]
        types = ["Community School", "Community College", "High School", "Secondary School", "College", "Academy"]
        order = rng.permutation(len(places))
        self.school_name = {}
        for k, s in enumerate(self.W.school):
            self.school_name[s[0]] = "%s %s" % (places[order[k]], types[int(rng.integers(len(types)))])

    # ------------------------------------------------------------------ timing of returns
    def times(self, yr, d, n, online, late=None):
        rng = np.random.default_rng(P.SEED * 1000 + yr * 37 + d)
        if yr == 26:
            open_ = dt.datetime(2026, 10, 1, 8, 0); close = dt.datetime(2026, 10, 30, 17, 0)
        else:
            open_ = dt.datetime(2025, 10, 1, 8, 0); close = dt.datetime(2025, 10, 24, 16, 0)
        span = (close - open_).total_seconds() / 86400
        days = np.arange(int(np.ceil(span)))
        w = np.full(len(days), 0.02); w[:4] = [0.11, 0.08, 0.06, 0.045]; w[7] += 0.045; w[min(18, len(w) - 2)] += 0.035; w[-1] += 0.03
        w = w / w.sum()
        out = []
        for i in range(n):
            day = int(rng.choice(days, p=w))
            if online[i]:
                hour = rng.choice(np.arange(24), p=_hours_online())
            else:
                day = min(day + int(rng.integers(2, 6)), len(days) - 1); hour = int(rng.integers(8, 16))
            t = open_.replace(hour=0) + dt.timedelta(days=day, hours=int(hour), minutes=int(rng.integers(60)),
                                                     seconds=int(rng.integers(60)))
            if t < open_:
                t = open_ + dt.timedelta(minutes=int(rng.integers(1, 600)))
            if t >= close:
                t = close - dt.timedelta(minutes=int(rng.integers(5, 300)))
            out.append(t)
        if late is not None:
            for i in np.where(late)[0]:
                out[i] = close + dt.timedelta(days=float(rng.uniform(3, 150)))
        return out

    # ------------------------------------------------------------------ the frames
    def frame(self, yr):
        W = self.W; cs = W.y26 if yr == 26 else W.y25
        rows = []; truth = []
        refs = self.rng.permutation(sum(c["n"] for c in cs)) + (100001 if yr == 26 else 200001)
        k = 0
        for c in cs:
            d = c["d"][0]; U = W.U[(yr, d)]; n = c["n"]
            t = P.DISTRICTS[d][4]; pon = ONLINE[0] + (ONLINE[1] - ONLINE[0]) * t
            resp = ~c["unk"]
            online = resp & (U["uc"] < pon)
            late = None
            if yr == 25:
                # leavers who returned after the close: respondents in the final file, lower bands more often
                wl = P.UREL[c["band"]] / P.UREL.mean()
                late = resp & (U["us"] < P.LATE_SHARE * wl)
            when = self.times(yr, d, n, online, late)
            det = detail(c["cat"], U["u4"])
            band = c["band"].copy()
            prov = band.copy()
            if yr == 26:
                appealed = (band >= 1) & (U["ua"] < APPEAL)
                prov[appealed] = band[appealed] - 1
            for i in range(n):
                r = dict(leaver_ref="L%d-%06d" % (yr, refs[k]), school_code=self.school_codes[c["school"][i]],
                         sex="F" if U["sex"][i] < 0.49 else "M", attainment_band=ABLAB[int(prov[i])])
                k += 1
                if resp[i]:
                    if online[i]:
                        early = yr == 25 or _ts(when[i]) < P.EDITION_SWITCH
                        build = ("7.1.4" if when[i] < dt.datetime(2025, 10, 9) else "7.2.0") if yr == 25 else ("7.3.2" if early else "8.0.1")
                        if yr == 26 and not early:
                            code = "2" if (det[i] == 0 and U["ux"][i] < HE_ABROAD) else LDS2_2026[int(det[i])]
                        else:
                            code = LDS2_2025[int(det[i])]
                        r.update(return_form="LDS-2", form_build=build, returned_at=_ts(when[i]), activity_code=code)
                    else:
                        r.update(return_form="LDS-1", form_build="", returned_at=_ts(when[i]), activity_code=LDS1[int(det[i])])
                    if yr == 25:
                        r["destination"] = DEST[int(c["cat"][i])]
                    for j, nm in enumerate(DEST):
                        r["alloc_" + nm.lower()] = ""
                else:
                    r.update(return_form="", form_build="", returned_at="", activity_code="")
                    if yr == 25:
                        r["destination"] = ""
                    for j, nm in enumerate(DEST):
                        r["alloc_" + nm.lower()] = "%.4f" % c["alloc"][i, j]
                rows.append(r)
                truth.append(dict(leaver_ref=r["leaver_ref"], d=d, d25=int(c["d25map"][i]), band=int(band[i]), prov=int(prov[i]), cat=int(c["cat"][i]),
                                  unk=bool(c["unk"][i]), late=bool(late[i]) if late is not None else False,
                                  traced=bool(c.get("traced", np.zeros(n, bool))[i]),
                                  unresolved=bool(c.get("unresolved", np.zeros(n, bool))[i]), det=int(det[i])))
        cols = ["leaver_ref", "school_code", "sex", "attainment_band", "return_form", "form_build", "returned_at", "activity_code"]
        cols += (["destination"] if yr == 25 else []) + ["alloc_" + x.lower() for x in DEST]
        df = pd.DataFrame(rows)[cols].sort_values(["school_code", "leaver_ref"]).reset_index(drop=True)
        return df, pd.DataFrame(truth)

    # ------------------------------------------------------------------ the 2025 follow-up
    def followup(self, truth25):
        rng = np.random.default_rng(P.SEED + 11)
        t = truth25[truth25["d25"].isin(P.TRACED)]
        res = t[t["traced"]]
        unres = t[t["unresolved"]]
        late = t[t["late"]]
        late = late[rng.random(len(late)) < (P.TRACE_FRAC + P.SAMPLE_EXTRA)]
        cases = pd.concat([res.assign(kind="resolved"), unres.assign(kind="unresolved"), late.assign(kind="late")])
        cases = cases.iloc[rng.permutation(len(cases))].reset_index(drop=True)
        cases["case_no"] = ["FU25-%05d" % (10001 + i) for i in range(len(cases))]
        out, xw = [], []
        names, probs = zip(*ROUTES)
        start = dt.date(2025, 11, 3)
        for _, r in cases.iterrows():
            xw.append(dict(case_no=r["case_no"], leaver_ref=r["leaver_ref"].replace("L25-", "25-"),
                           district_code=P.CODE[int(r["d25"])], drawn_on=P.FOLLOWUP_DRAWN))
            if r["kind"] == "unresolved":
                out.append(dict(case_no=r["case_no"], route="", resolved_on="", outcome_code="F99"))
                continue
            route = rng.choice(len(names), p=probs)
            when = start + dt.timedelta(days=int(rng.integers(0, 116)))
            code = FCODE[int(r["det"])]
            out.append(dict(case_no=r["case_no"], route=names[route], resolved_on=when.isoformat(), outcome_code=code))
            if rng.random() < P.DUP_SHARE:
                r2 = rng.choice([i for i in range(len(names)) if i != route])
                w2 = when + dt.timedelta(days=int(rng.integers(3, 30)))
                out.append(dict(case_no=r["case_no"], route=names[r2], resolved_on=min(w2, dt.date(2026, 2, 27)).isoformat(), outcome_code=code))
        fo = pd.DataFrame(out)
        fo = fo.assign(_k=fo["resolved_on"].eq("")).sort_values(["_k", "resolved_on", "case_no"]).drop(columns="_k").reset_index(drop=True)
        return fo, pd.DataFrame(xw).sort_values("case_no").reset_index(drop=True), cases

    # ------------------------------------------------------------------ school register and examination points
    def register(self):
        rows = []
        for s in self.W.school:
            rows.append(dict(school_code=s[0], school_name=self.school_name[s[0]], district_2025=P.CODE[s[2]],
                             district_2026=P.CODE[s[1]]))
        return pd.DataFrame(rows).sort_values("school_code").reset_index(drop=True)

    def points(self, truth26):
        rng = np.random.default_rng(P.SEED + 13)
        rows = []
        for _, r in truth26.iterrows():
            lo, hi = CUTS[r["band"]]
            if r["prov"] != r["band"]:
                pts = int(rng.integers(lo, min(lo + 30, hi + 1))); issued = "2026-10-20"
            else:
                pts = int(rng.integers(lo, hi + 1))
                issued = "2026-10-20" if rng.random() < REVISED_ONLY else "2026-08-25"
            rows.append(dict(leaver_ref=r["leaver_ref"], exam_points=pts, results_issued=issued))
        return pd.DataFrame(rows).sort_values("leaver_ref").reset_index(drop=True)

    # ------------------------------------------------------------------ distractors
    def release_2025_tables(self, truth25):
        """the December 2025 release on the 2025 map: returns accepted by the close, the rest allocated"""
        s24 = self.W.s24
        t = truth25
        out = []
        for d in range(P.ND):
            m = t["d25"] == d
            n = int(m.sum())
            closed_resp = m & ~t["unk"] & ~t["late"]
            alloc_rows = t[m & (t["unk"] | t["late"])]
            a = s24[alloc_rows["d25"].to_numpy(), alloc_rows["band"].to_numpy()]
            neet = ((t.loc[closed_resp, "cat"] == 4).sum() + a[:, 4].sum()) / n * 100
            he = ((t.loc[closed_resp, "cat"] == 0).sum() + a[:, 0].sum()) / n * 100
            out.append(dict(district_code=P.CODE[d], district=P.NAME[d], leavers=n, neet_rate=round(neet, 1), he_entry_rate=round(he, 1)))
        return pd.DataFrame(out).sort_values("district_code").reset_index(drop=True)

    def lfs(self):
        rng = np.random.default_rng(P.SEED + 17)
        base = {"North": 13.8, "South": 9.6, "East": 11.9, "West": 10.7}
        rows = []
        for reg, b in base.items():
            for q in range(1, 5):
                rows.append(dict(region=reg, quarter="2025Q%d" % q, age_group="16-24",
                                 neet_rate=round(b + rng.normal(0, 0.6) + (0.4 if q == 1 else 0), 1),
                                 sample_persons=int(rng.integers(380, 720))))
        return pd.DataFrame(rows)

    def careers_contacts(self):
        rng = np.random.default_rng(P.SEED + 19)
        rows = []
        weeks = ["2026-09-28", "2026-10-05", "2026-10-12", "2026-10-19", "2026-10-26", "2026-11-02"]
        season = [0.8, 1.15, 1.2, 1.1, 0.95, 0.7]
        for d in range(P.ND):
            n = self.W.y26[d]["n"]
            for wk, f in zip(weeks, season):
                made = int(round(n * 0.035 * f * rng.uniform(0.9, 1.1)))
                seen = int(round(made * rng.uniform(0.42, 0.58)))
                rows.append(dict(district_code=P.CODE[d], week_starting=wk, contacts_made=made, leavers_seen=seen))
        return pd.DataFrame(rows).sort_values(["district_code", "week_starting"]).reset_index(drop=True)
