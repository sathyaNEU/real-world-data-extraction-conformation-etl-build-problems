"""task244 records: the five quarterly person files of the labour force survey, the supervisors' reinterview results and
fieldwork log, the published 2027 flows tables, the district gazetteer and the context files. Each file is laid out the
way the bureau's systems produce it."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P
import sim

S = P.STATUS
MOVED = set(P.MOVED_EAS)
REL = {"head": 1, "spouse": 2, "child": 3, "other relative": 4}


def agegroup(age):
    return min(5, (age - 15) // 10)


class Records:
    def __init__(self, W):
        self.W = W
        self.rng = np.random.default_rng(P.SEED + 1)
        rng = self.rng
        # a few birth months taken down wrongly at a person's first interview and corrected at the next
        split = {x for (_, _, _, ps) in W.splits for x in ps}
        pids = sorted({p["pid"] for h in W.hhq for p in h["people"]} - split)
        self.bm_first_wrong = set(int(x) for x in rng.choice(pids, size=int(0.008 * len(pids)), replace=False))
        # the month taken down wrongly never belongs to anyone else who lived in the dwelling
        self.bm_wrong = {}
        for h in W.hhq:
            for p in h["people"]:
                if p["pid"] in self.bm_first_wrong and p["pid"] not in self.bm_wrong:
                    sx = p["sex"]
                    for k in range(1, 12):
                        bm = 1 + (p["bm"] - 1 + k) % 12
                        if (sx, p["by"], bm) not in W.taken[h["dw"]]:
                            break
                    self.bm_wrong[p["pid"]] = bm
        # some members are interviewed on a callback day after the household's first visit
        self.callback = {}
        for h in W.hhq:
            for p in h["people"]:
                if p["line"] != h["people"][0]["line"] and rng.random() < 0.14:
                    self.callback[(h["dw"], h["hh"], p["line"], h["q"])] = int(rng.integers(1, 6))
        # a household goes to its supervisor once every member has been interviewed, and a reinterview completed after
        # the window is after it for every member
        sel = {(r["h"]["dw"], r["h"]["hh"], r["h"]["q"]): r for r in W.reint if r["attempts"]}
        for k in sorted(self.callback):
            r = sel.get((k[0], k[1], k[3]))
            if r is None:
                continue
            cap = (r["attempts"][0][0] - r["h"]["day"]).days - 1
            if r["out"] == "late":
                cap = min(cap, (r["attempts"][-1][0] - r["h"]["day"]).days - P.REINT_WINDOW - 1)
            if cap < 1:
                del self.callback[k]
            else:
                self.callback[k] = min(self.callback[k], cap)
        self._persons = None

    # ------------------------------------------------------------------ the person files
    def recorded_district(self, h):
        """the district and enumeration area as the interview recorded them: the six areas moved on 1 April 2027 kept
        their Industrial Corridor codes until then"""
        before = P.Q_START[P.QUARTERS[h["q"]]] < P.BOUNDARY_DATE
        if (h["ed"], h["ee"]) in MOVED and before:
            return h["ed"], h["ee"]
        return h["d"], h["ea"]

    def persons(self):
        if self._persons is not None:
            return self._persons
        W, rng = self.W, self.rng
        seen_first = set()
        rows = []
        for h in W.hhq:
            d_rec, ea_rec = self.recorded_district(h)
            qn = P.QUARTERS[h["q"]]
            for p in h["people"]:
                bm = p["bm"]
                if p["pid"] in self.bm_first_wrong and p["pid"] not in seen_first:
                    bm = self.bm_wrong[p["pid"]]
                seen_first.add(p["pid"])
                day = h["day"] + dt.timedelta(days=self.callback.get((h["dw"], h["hh"], p["line"], h["q"]), 0))
                if day.weekday() == 6:
                    day -= dt.timedelta(days=1)          # no interviews on a Sunday: the callback was the Saturday
                age = day.year - p["by"] - (1 if (day.month < bm) else 0)
                rows.append(dict(quarter=qn, district=d_rec, ea=ea_rec, dwelling=h["dw"], hh=h["hh"], line=p["line"],
                                 visit=h["visit"], int_date=day.isoformat(),
                                 interviewer="%s-%02d" % (d_rec[1:], h["intv"]), resp_line=p["resp_line"],
                                 sex=1 if p["sex"] == "M" else 2, birth_month=bm, birth_year=p["by"], age=age,
                                 relation=REL[p["rel"]], rec=p["rec"], d27=h["d"]))
        df = pd.DataFrame(rows)
        df = df.join(self._items(df["rec"].values))
        df["lfs_status"] = df["rec"] + 1
        # cross-sectional weights: the district's adults over its responding adults, calibrated by sex and age group
        df["agegrp"] = df["age"].clip(15, 74).sub(15).floordiv(10).clip(0, 5)
        cal = {(s, a): 1 + 0.06 * np.sin(1.7 * s + 0.9 * a) for s in (1, 2) for a in range(6)}
        f = np.array([cal[(s, a)] for s, a in zip(df["sex"], df["agegrp"])])
        n = df.groupby(["quarter", "d27"])["line"].transform("size").values
        pop = df["d27"].map(P.DPOP).values * 1000.0
        w = pop / n * f
        w = w / pd.Series(w).groupby([df["quarter"], df["d27"]]).transform("sum").values * pop
        df["wt"] = np.round(w, 2)
        df = df.drop(columns=["agegrp"])
        self._persons = df
        return df

    def _items(self, rec):
        """the questionnaire's job, search and availability items, answered consistently with the recorded status"""
        rng = self.rng
        n = len(rec)
        work, absent, look, avail, future = (np.full(n, np.nan) for _ in range(5))
        u = rng.random((n, 3))
        e, un, nl = rec == 0, rec == 1, rec == 2
        work[e] = np.where(u[e, 0] < 0.93, 1, 2)
        absent[e & (work == 2)] = 1
        work[~e] = 2
        absent[~e] = 2
        fut = un & (u[:, 1] < 0.06)
        look[un] = np.where(fut[un], 2, 1)
        future[fut] = 1
        avail[un] = 1
        # outside the labour force: not looking, or looking but not available
        lk = nl & (u[:, 1] < 0.18)
        look[nl] = np.where(lk[nl], 1, 2)
        avail[nl] = np.where(lk[nl], 2, np.where(u[nl, 2] < 0.3, 1, 2))
        future[nl & (look == 2)] = 2
        out = pd.DataFrame({"q_work": work, "q_absent": absent, "q_look": look, "q_avail": avail, "q_future": future})
        return out.astype("Int64")

    def person_file(self, quarter):
        df = self.persons()
        out = df[df.quarter == quarter].drop(columns=["rec", "d27"]).copy()
        if quarter == "2027Q2":
            # one area's batch went to the server twice
            dup = out[(out.district == "D11") & (out.ea == 5)]
            # the server's restore of 17 May re-ingested the uploads of 14 May, numbering each household it received
            # as the dwelling's next household
            day = out[out.int_date == P.REPLAY_DAY.isoformat()].copy()
            top = df.groupby("dwelling")["hh"].max()
            nxt = {}
            for (dw, hh) in sorted(set(zip(day.dwelling, day.hh))):
                nxt[(dw, hh)] = int(top[dw]) + 1 + sum(1 for k in nxt if k[0] == dw)
            day["hh"] = [nxt[(dw, hh)] for dw, hh in zip(day.dwelling, day.hh)]
            out = pd.concat([out, dup, day]).sort_values(["district", "ea", "dwelling", "hh", "line"], kind="stable")
        return out[["quarter", "district", "ea", "dwelling", "hh", "line", "visit", "int_date", "interviewer",
                    "resp_line", "sex", "birth_month", "birth_year", "age", "relation", "q_work", "q_absent", "q_look",
                    "q_avail", "q_future", "lfs_status", "wt"]]

    # ------------------------------------------------------------------ the reinterview
    def reint_results(self):
        rows = []
        n = 0
        for r in self.W.reint:
            h = r["h"]
            d_rec, ea_rec = self.recorded_district(h)
            for x, p in zip(r["recs"], [p for p in h["people"]]):
                n += 1
                rows.append(dict(reint_id="R%s%05d" % (P.QUARTERS[h["q"]][2:].replace("Q", ""), n),
                                 quarter=P.QUARTERS[h["q"]], district=d_rec, ea=ea_rec, dwelling=h["dw"], hh=h["hh"],
                                 line=p["line"], supervisor=r["sup"], orig_status=x["rec"] + 1,
                                 reint_status=x["reint"] + 1, reconciled=x["recon"] + 1,
                                 outcome="same" if x["reint"] == x["rec"] else "reconciled"))
        return pd.DataFrame(rows)

    def reint_log(self):
        """one row per attempt. The tablet stamps attempt_date when the attempt is saved; from the app update, which
        each supervisor's tablet took at a Friday sync between 18 June and 9 July 2027, it stamps it when the tablet next
        synchronises with the bureau's server (the supervisors sync at the area office on Friday, where they spend the
        day, so a Friday's calls are made in the evening), while visit_start is the clock time the supervisor opened the
        household's reinterview form"""
        rows = []
        n = 0
        rng = np.random.default_rng(P.SEED + 2)
        for r in self.W.reint:
            h = r["h"]
            if not r["attempts"]:
                continue
            d_rec, ea_rec = self.recorded_district(h)
            for i, (day, res) in enumerate(r["attempts"]):
                n += 1
                wd = day.weekday()
                if wd >= 5:
                    start = dt.datetime.combine(day, dt.time(9, 0)) + dt.timedelta(minutes=int(rng.integers(0, 540)))
                elif wd != 4 and rng.random() < 0.35:
                    start = dt.datetime.combine(day, dt.time(9, 0)) + dt.timedelta(minutes=int(rng.integers(0, 420)))
                else:
                    start = dt.datetime.combine(day, dt.time(16, 0)) + dt.timedelta(
                        minutes=int(rng.triangular(0, 120, 299)))
                stamp = day
                if day >= P.APP_UPDATE[r["sup"]]:
                    # the next Friday's sync at the area office, held in office hours, so a Friday evening's visit
                    # waits a week
                    stamp = day + dt.timedelta(days=int((4 - day.weekday()) % 7 or 7))
                rows.append(dict(log_row=n, supervisor=r["sup"], quarter=P.QUARTERS[h["q"]], district=d_rec, ea=ea_rec,
                                 dwelling=h["dw"], hh=h["hh"], attempt=i + 1, attempt_date=stamp.isoformat(),
                                 visit_start=start.strftime("%Y-%m-%d %H:%M"), result=res))
        return pd.DataFrame(rows)

    # ------------------------------------------------------------------ the published flows
    def flows(self):
        """the bureau's 2027 annual flows: persons interviewed in two consecutive quarters, linked on the dwelling,
        household and line numbers, weighted by the longitudinal weights, the four quarter pairs averaged"""
        df = self.persons()
        key = df.set_index(["dwelling", "hh", "line", "quarter"])
        out = {}
        for d in P.DCODES:
            out[d] = np.zeros((3, 3))
        for qi in range(len(P.QUARTERS) - 1):
            a = df[(df.quarter == P.QUARTERS[qi]) & (df.visit <= 3)]
            b = df[df.quarter == P.QUARTERS[qi + 1]]
            m = a.merge(b, on=["dwelling", "hh", "line"], suffixes=("", "_b"))
            m["agegrp"] = m["age"].clip(15, 74).sub(15).floordiv(10).clip(0, 5)
            g = 1 + P.LONG_CAL[0] * np.cos(P.LONG_CAL[1] * m["sex"] + P.LONG_CAL[2] * m["agegrp"])
            for d in P.DCODES:
                md = m[m.d27_b == d]
                w = (P.DPOP[d] * 1000.0) * g[md.index] / g[md.index].sum()
                np.add.at(out[d], (md["rec"].values, md["rec_b"].values), w.values)
        for d in P.DCODES:
            out[d] = out[d] / (len(P.QUARTERS) - 1)
        return out

    def flows_tables(self):
        O = self.flows()
        rows, rates = [], []
        for d in P.DCODES:
            o = np.round(O[d]).astype(int)
            for i, a in enumerate(S):
                for j, b in enumerate(S):
                    rows.append(dict(district=d, district_name=P.DNAME[d], status_q1=P.STATUS_NAME[a],
                                     status_q2=P.STATUS_NAME[b], persons=int(o[i, j])))
            rates.append(dict(district=d, district_name=P.DNAME[d],
                              unemployed_start=int(o[1].sum()), employed_start=int(o[0].sum()),
                              job_finding=round(100 * o[1, 0] / o[1].sum(), 1),
                              job_loss=round(100 * o[0, 1] / o[0].sum(), 1)))
        return pd.DataFrame(rows), pd.DataFrame(rates)

    # ------------------------------------------------------------------ the gazetteer
    def gazetteer(self):
        rows = []
        for d in P.DCODES:
            for ea, ed, ee in sim.ea_codes(d):
                moved = (ed, ee) in MOVED
                rows.append(dict(district=d, district_name=P.DNAME[d], ea=ea,
                                 district_before=ed if (moved or ed != d or ee != ea) else "",
                                 ea_before=ee if (moved or ed != d or ee != ea) else "",
                                 effective=P.BOUNDARY_DATE.isoformat() if (moved or ed != d or ee != ea) else ""))
        return pd.DataFrame(rows)

    # ------------------------------------------------------------------ context files
    def bulletin_rates(self, quarter):
        df = self.persons()
        q = df[df.quarter == quarter]
        out = {}
        for d in P.DCODES + ["state"]:
            x = q if d == "state" else q[q.d27 == d]
            w = x["wt"]
            e, u = w[x.rec == 0].sum(), w[x.rec == 1].sum()
            out[d] = (round(100 * u / (e + u), 1), round(100 * e / w.sum(), 1))
        return out

    def jobcentre(self):
        """registered job seekers at each month's end: a register of those who came to a job centre, unrelated in
        definition to the survey's unemployed"""
        rng = np.random.default_rng(P.SEED + 3)
        rows = []
        for d in P.DCODES:
            base = P.DPOP[d] * (0.006 + 0.010 * (P.DTYPE[d] in ("LL", "HL"))) * rng.uniform(0.8, 1.2)
            vals = []
            for m in range(12):
                base *= rng.uniform(0.97, 1.04)
                vals.append(int(round(base * 1000)))
            rows.append([d, P.DNAME[d]] + vals)
        months = [dt.date(2027, m, 1).strftime("%b %Y") for m in range(1, 13)]
        return pd.DataFrame(rows, columns=["District", "District name"] + months)

    def projections(self):
        rng = np.random.default_rng(P.SEED + 4)
        rows = []
        groups = ["15-24", "25-34", "35-44", "45-54", "55-64", "65+"]
        share = np.array([0.30, 0.24, 0.18, 0.12, 0.09, 0.07])
        for d in P.DCODES:
            for yr, g in ((2026, 0.975), (2027, 1.0), (2028, 1.026)):
                for sx, sw in ((1, 0.494), (2, 0.506)):
                    for ag, sh in zip(groups, share):
                        rows.append(dict(district=d, year=yr, sex=sx, age_group=ag,
                                         persons=int(round(P.DPOP[d] * 1000 * g * sw * sh * rng.uniform(0.985, 1.015)))))
        return pd.DataFrame(rows)
