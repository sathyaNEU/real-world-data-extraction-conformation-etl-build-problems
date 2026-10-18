"""task246 records: the files the county's data team gathered after the round, each in the layout of the system that
produced it. NCHA's teams used a tablet form exported to CSV (MUAC in millimetres, dates of birth); PRK's used a form
whose export the partner keeps in a workbook (MUAC in centimetres, age in months). The household rosters of both
partners were merged by the county into one file, each partner's own codes kept."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P
import sim

PARTNER_OF = {a: P.MEASURERS[a][0] for a in P.MEASURERS}
TEAM_NO = {a: P.MEASURERS[a][1] for a in P.MEASURERS}
CODE = {"A1": "NCHA-AN01", "A2": "NCHA-AN02", "A3": "NCHA-AN03", "A4": "NCHA-AN04", "A5": "NCHA-AN05", "A6": "NCHA-AN06",
        "B1": "PRK-AN01", "B2": "PRK-AN02", "B3": "PRK-AN03", "B4": "PRK-AN04", "B4s": "PRK-AN07", "B5": "PRK-AN05",
        "B6": "PRK-AN06"}
FORM_V4 = dt.date(2027, 6, 21)          # the county's household form version 4 on every tablet from this day
# the household form's codes. Version 4 swapped the third and fourth choices of two lists; the server keeps each
# submission's codes as the form on the tablet set them
OUTCOME = {"v3": {"completed": 1, "refused": 2, "absent": 3, "empty": 4},
           "v4": {"completed": 1, "refused": 2, "empty": 3, "absent": 4}}
REASON = {"v3": {"work": 1, "marriage": 2, "died": 3, "caregiver": 4, "school": 5, "livestock": 6, "household": 7},
          "v4": {"work": 1, "marriage": 2, "caregiver": 3, "died": 4, "school": 5, "livestock": 6, "household": 7}}
RESENT = ("A2", dt.date(2027, 6, 22))   # NCHA team 2's anthropometry uploads re-sent after a sync failure
RESYNC_CLUSTER = None                   # set in Records: an NCHA cluster whose household forms were sent twice


def dmy(d):
    return d.strftime("%d/%m/%Y")


def completed_months(dob, day):
    m = (day.year - dob.year) * 12 + (day.month - dob.month)
    if day.day < dob.day:
        m -= 1
    return m


def dob_of(day, age_m):
    return day - dt.timedelta(days=int(round(age_m * 30.4375)))


def uuid(r):
    h = "".join("%02x" % int(x) for x in r.integers(0, 256, 16))
    return "%s-%s-%s-%s-%s" % (h[:8], h[8:12], h[12:16], h[16:20], h[20:])


def body(k, r):
    """weight and height for the record; they play no part in the MUAC figures"""
    age = k["age_m"]
    w = 6.9 + 0.19 * age - 0.25 * (k["sex"] == "F") + r.normal(0, 1.0)
    h = 66.5 + 0.62 * age - 0.004 * age * age - 0.8 * (k["sex"] == "F") + r.normal(0, 3.2)
    return round(float(w), 1), round(float(h), 1)


class Records:
    def __init__(self, W):
        self.W = W
        self.cl = {c["cluster"]: c for c in W.clusters}
        self.hh = {h["hh"]: h for h in W.households}
        died = {self.hh[m["hh"]]["cluster"] for m in W.members if m["status"] == "died" and not m["born"]}
        cands = sorted(c["cluster"] for c in W.clusters if c["cluster"] in died)
        self.resync = cands[int(sim.crng("resync").integers(0, len(cands)))]
        self.extra = self._extra_children()

    # ------------------------------------------------------------------ the sample
    def cluster_sample(self):
        r = sim.crng("listing")
        rows = []
        for c in self.W.clusters:
            rows.append((c["sub"], P.ZNAME[c["zone"]], c["cluster"], "%05d" % c["ea"], int(r.integers(58, 190)),
                         P.PARTNER_SHORT[PARTNER_OF[c["team"]]], TEAM_NO[c["team"]], dmy(c["date"])))
        return pd.DataFrame(rows, columns=["sub_county", "zone", "cluster", "ea_code", "households_listed", "partner",
                                           "team", "date_visited"])

    # ------------------------------------------------------------------ anthropometry
    def _extra_children(self):
        """household members a team measured though they fell outside 6 to 59 months on the day: the protocol leaves
        them out"""
        out = []
        hd = self.hh
        pool = [m for m in self.W.members if m["status"] == "present" and (4.0 <= m["age_m"] < 6.0 or 60.0 <= m["age_m"] < 63.5)]
        r = sim.crng("extra")
        idx = sorted(r.choice(len(pool), 14, replace=False).tolist())
        for i in idx:
            m = pool[i]
            h = hd[m["hh"]]
            level = self.cl[h["cluster"]]["level"]
            own = level + P.AGE_SLOPE * (m["age_m"] - 33.0) + r.normal(0, 9.5)
            a = sim.anthropometrist(h["team"], h["date"])
            _, _, _, b, si, sr, hp = P.MEASURERS[a]
            x = float(sim.heap(own + b + r.normal(0, si) + r.normal(0, sr), r, hp))
            out.append(dict(child=-(i + 1), hh=h["hh"], line=m["line"], cluster=h["cluster"], zone=h["zone"],
                            team=h["team"], date=h["date"], sex=m["sex"], age_m=m["age_m"], own=own, oedema=False,
                            measles=None if m["age_m"] < 9 else "card", measurer=a, muac=x))
        return out

    def _kids(self, partner):
        ks = [k for k in self.W.children + self.extra if PARTNER_OF[k["team"]] == partner]
        return sorted(ks, key=lambda k: (k["date"], TEAM_NO[k["team"]], k["cluster"], self.hh[k["hh"]]["number"], k["line"]))

    def _sync(self, team, day):
        """when a team's tablet sent the day's forms (server time, UTC): most evenings back at base, otherwise the next
        morning before the team set out, or a day later from the more remote clusters"""
        r = sim.crng("sync", team, day.isoformat())
        u = r.random()
        if u < 0.72:
            t = dt.datetime.combine(day, dt.time(15, 20)) + dt.timedelta(minutes=int(r.integers(0, 200)))
        elif u < 0.93:
            t = dt.datetime.combine(day + dt.timedelta(days=1), dt.time(3, 30)) + dt.timedelta(minutes=int(r.integers(0, 120)))
        else:
            t = dt.datetime.combine(day + dt.timedelta(days=2), dt.time(14, 0)) + dt.timedelta(minutes=int(r.integers(0, 300)))
        return t + dt.timedelta(seconds=int(r.integers(0, 60)))

    def _sync_seq(self, team, day):
        key = (team, day)
        self._seq = getattr(self, "_seq", {})
        self._seq[key] = self._seq.get(key, 0) + 1
        return self._seq[key]

    def ncha_children(self):
        rows = []
        typo = {11: 14.0, 523: 1395.0}
        for i, k in enumerate(self._kids("A")):
            r = sim.crng("ncha", k["hh"], k["line"])
            w, h = body(k, r)
            day = k["date"]
            dob = dob_of(day, k["age_m"])
            muac = typo.get(i, k["muac"])
            meas = {"card": "1", "recall": "2", "no": "3", "dk": "8", None: ""}[k["measles"]]
            sub = self._sync(k["team"], day) + dt.timedelta(seconds=int(4 * self._sync_seq(k["team"], day)))
            row = [uuid(r), sub.strftime("%Y-%m-%dT%H:%M:%S"), day.isoformat(), TEAM_NO[k["team"]], k["cluster"],
                   self.hh[k["hh"]]["number"], k["line"], k["sex"].lower(), dmy(dob), "y" if k["oedema"] else "n", w, h,
                   int(muac), meas]
            rows.append(row)
            if (k["team"], day) == RESENT:
                again = list(row)
                again[0] = uuid(r)
                again[1] = (sub + dt.timedelta(days=1, hours=2)).strftime("%Y-%m-%dT%H:%M:%S")
                rows.append(again)
        return pd.DataFrame(rows, columns=["_uuid", "_submission_time", "today", "team", "cluster", "hh_no", "child_no",
                                           "sex", "dob", "oedema", "weight_kg", "height_cm", "muac_mm", "measles"])

    def prk_children(self):
        rows = []
        typo = {37: 1.38, 1210: 136.0}
        lab = {"card": "Yes, card", "recall": "Yes, recall", "no": "No", "dk": "Don't know", None: None}
        for i, k in enumerate(self._kids("B")):
            r = sim.crng("prk", k["hh"], k["line"])
            w, h = body(k, r)
            day = k["date"]
            age = completed_months(dob_of(day, k["age_m"]), day)
            muac_cm = typo.get(i, round(k["muac"] / 10.0, 1))
            rows.append([dmy(day), TEAM_NO[k["team"]], k["cluster"], self.hh[k["hh"]]["number"], k["line"],
                         1 if k["sex"] == "M" else 2, age, 1 if k["oedema"] else 0, w, h, muac_cm, lab[k["measles"]]])
        return pd.DataFrame(rows, columns=["Date", "Team", "Cluster", "HH", "Child line", "Sex", "Age (months)",
                                           "Oedema", "Weight (kg)", "Height (cm)", "MUAC (cm)", "Measles"])

    # ------------------------------------------------------------------ the standardisation test
    def _test_rows(self, partner):
        """(session, child, measurer, reading 1, reading 2) for the partner's anthropometrists, and the supervisor's"""
        out = []
        for a, e in self.W.test.items():
            if PARTNER_OF[a] != partner:
                continue
            for s, rd in zip(e["sessions"], e["reads"]):
                for c in range(rd.shape[1]):
                    out.append((s, c + 1, a, float(rd[0][c]), float(rd[1][c])))
        sup = []
        for s in (1, 2):
            S = self.W.sessions[s][1]
            for c in range(S.shape[1]):
                sup.append((s, c + 1, "SUP", float(S[0][c]), float(S[1][c])))
        return out, sup

    def ncha_test(self):
        out, sup = self._test_rows("A")
        dates = {1: P.TRAINING_TEST, 2: P.REFRESHER}
        rows = []
        for s, c, a, r1, r2 in sorted(sup + out, key=lambda t: (t[0], t[2] != "SUP", t[2], t[1])):
            who = "SUPERVISOR" if a == "SUP" else CODE[a]
            for k, v in ((1, r1), (2, r2)):
                rows.append((s, dmy(dates[s]), "S%d-%02d" % (s, c), who, k, int(v)))
        return pd.DataFrame(rows, columns=["session", "date", "test_child", "measured_by", "reading", "muac_mm"])

    def prk_test_frames(self):
        out, sup = self._test_rows("B")
        frames = []
        for s in (1, 2):
            data = {"Child": ["S%d-%02d" % (s, c) for c in range(1, 11)]}
            sp = [t for t in sup if t[0] == s]
            data["Supervisor 1st"] = [round(t[3] / 10.0, 1) for t in sp]
            data["Supervisor 2nd"] = [round(t[4] / 10.0, 1) for t in sp]
            for a in [m for m in P.MEASURERS if PARTNER_OF[m] == "B"]:
                rows = [t for t in out if t[0] == s and t[2] == a]
                if not rows:
                    continue
                name = P.MEASURERS[a][2]
                data["%s 1st" % name] = [round(t[3] / 10.0, 1) for t in rows]
                data["%s 2nd" % name] = [round(t[4] / 10.0, 1) for t in rows]
            title = "Session %d (%s)" % (s, (P.TRAINING_TEST if s == 1 else P.REFRESHER).strftime("%d %b"))
            frames.append((title, pd.DataFrame(data)))
        return frames

    # ------------------------------------------------------------------ teams
    def teams(self):
        rows = []
        for a in ["A1", "A2", "A3", "A4", "A5", "A6", "B1", "B2", "B3", "B4", "B5", "B6"]:
            partner, no, name = P.MEASURERS[a][:3]
            zones = sorted({c["zone"] for c in self.W.clusters if c["team"] == a}, key=P.ZCODES.index)
            cls = sorted(c["cluster"] for c in self.W.clusters if c["team"] == a)
            days = sorted(c["date"] for c in self.W.clusters if c["team"] == a)
            rows.append((P.PARTNER_SHORT[partner], no, P.TEAM_LEADERS[a], name, CODE[a],
                         "; ".join(P.ZNAME[z] for z in zones), "%d to %d" % (cls[0], cls[-1]) if len(zones) == 1 else
                         ", ".join(str(x) for x in cls), dmy(days[0]), dmy(days[-1])))
        return pd.DataFrame(rows, columns=["Partner", "Team", "Team leader", "Anthropometrist", "Anthropometrist code",
                                           "Zones", "Clusters", "First day", "Last day"])

    def changes(self):
        b4, b4s = P.MEASURERS["B4"][2], P.MEASURERS["B4s"][2]
        rows = [(dmy(dt.date(2027, 6, 26)), "PRK", 4, "%s (%s) left the round after the day's cluster (family "
                 "emergency)." % (b4, CODE["B4"])),
                (dmy(P.REFRESHER), "PRK", 4, "%s (%s) joined team 4 as anthropometrist, from that day's cluster, after the "
                 "refresher session." % (b4s, CODE["B4s"])),
                (dmy(dt.date(2027, 7, 2)), "NCHA", 5, "Team 5's vehicle off the road for the morning; the day's cluster "
                 "started at 13:00.")]
        rows.sort(key=lambda x: dt.datetime.strptime(x[0], "%d/%m/%Y"))
        return pd.DataFrame(rows, columns=["Date", "Partner", "Team", "Change"])

    # ------------------------------------------------------------------ households (the county's household form)
    def _present(self):
        n = {}
        for m in self.W.members:
            if m["status"] == "present":
                n[m["hh"]] = n.get(m["hh"], 0) + 1
        return n

    def _fid(self, h):
        return "HH-%05d" % (h["hh"] * 3 + 1017)

    def visits(self):
        """the county server's household visits: one row a visit, the outcome in the code of the form version on the
        tablet (version 4 from 21 June)"""
        present = self._present()
        r = sim.crng("visits")
        rows = []
        for h in sorted(self.W.households, key=lambda h: (h["date"], h["team"], h["cluster"], h["number"])):
            ver = "v4" if h["date"] >= FORM_V4 else "v3"
            for v, o in enumerate(h["visits"], 1):
                t = dt.datetime.combine(h["date"], dt.time(8, 20)) + dt.timedelta(minutes=int(r.integers(0, 400)) + 145 * (v - 1))
                rows.append([P.PARTNER_SHORT[PARTNER_OF[h["team"]]], TEAM_NO[h["team"]], h["cluster"], h["number"], v,
                             dmy(h["date"]), t.strftime("%H:%M"), OUTCOME[ver][o],
                             present.get(h["hh"]) if o == "completed" else None])
        return pd.DataFrame(rows, columns=["partner", "team", "cluster", "hh_no", "visit", "date", "time", "outcome",
                                           "members_present"])

    @staticmethod
    def why_left(m):
        """why a member left: a child who went with the mother or to another caregiver is drawn as such; anyone else
        by age, on a generator keyed to the member"""
        if m.get("why"):
            return m["why"]
        r = sim.crng("why", m["hh"], m["line"])
        if m["age_m"] < 180:
            opts, p = ["school", "household", "livestock"], [0.5, 0.3, 0.2]
        else:
            opts, p = ["work", "marriage", "livestock", "household"], [0.35, 0.25, 0.25, 0.15]
        return opts[int(r.choice(len(opts), p=p))]

    def members(self):
        """the county server's member roster: one row a member listed. The form's roster lists those present, those
        who left and those who died; a child born and dying within the recall period is kept on the births module, and
        a member who died away from home was entered as having left, with that reason"""
        rows = []
        r0 = sim.crng("members")
        for m in sorted(self.W.members, key=lambda m: (self.hh[m["hh"]]["date"], m["hh"], m["line"])):
            h = self.hh[m["hh"]]
            if m["status"] == "died" and m["born"]:
                continue
            ver = "v4" if h["date"] >= FORM_V4 else "v3"
            dod, reason = None, None
            if m["status"] == "died" and m["away"]:
                status, reason = "L", REASON[ver]["died"]
            elif m["status"] == "left":
                status, reason = "L", REASON[ver][self.why_left(m)]
            elif m["status"] == "died":
                status = "D"
                dod = dmy(h["date"] - dt.timedelta(days=int(r0.integers(3, max(4, h["recall_days"] - 2)))))
            else:
                status = "P"
            age_m = m["age_m"]
            if age_m < 60:
                # an age the respondent gives without a card is often a round number of months
                said = sim.crng("said", m["hh"], m["line"]).random()
                age = int(age_m) if age_m < 12 or said >= 0.3 else min(59, int(12 * round(age_m / 12.0)))
                unit = "months"
            else:
                age, unit = int(age_m // 12), "years"
            row = [h["cluster"], h["number"], self._fid(h), h["date"].isoformat(), m["line"], m["sex"], age, unit, status,
                   "Yes" if m["joined"] else "No", "Yes" if m["born"] else "No", reason, dod]
            rows.append(row)
            if h["cluster"] == self.resync:
                again = list(row)
                again[2] = "HH-%05d" % (h["hh"] * 3 + 1017 + 60000)
                rows.append(again)
        df = pd.DataFrame(rows, columns=["cluster", "hh_no", "form_id", "interview_date", "line_no", "sex", "age",
                                         "age_unit", "status", "joined", "born", "left_reason", "date_of_death"])
        df["left_reason"] = df["left_reason"].astype("Int64")
        return df

    def births(self):
        """the county server's births module: every child born to the household during the recall period"""
        rows = []
        r = sim.crng("births")
        for m in sorted(self.W.members, key=lambda m: (self.hh[m["hh"]]["date"], m["hh"], m["line"])):
            h = self.hh[m["hh"]]
            if not m["born"]:
                continue
            dob = dob_of(h["date"], m["age_m"])
            if m["status"] == "died":
                dod = dob + dt.timedelta(days=int(r.integers(1, max(2, (h["date"] - dob).days))))
                rows.append([h["cluster"], h["number"], self._fid(h), dmy(dob), m["sex"], "died", dmy(dod)])
            else:
                rows.append([h["cluster"], h["number"], self._fid(h), dmy(dob), m["sex"], "alive", None])
        return pd.DataFrame(rows, columns=["cluster", "hh_no", "form_id", "date_of_birth", "sex", "outcome",
                                           "date_of_death"])

    # ------------------------------------------------------------------ distractors
    def market_prices(self):
        r = sim.crng("markets")
        rows = []
        markets = ["Laga Town", "North Laga", "Lake Market", "East Laga", "West Laga"]
        base = {"maize (KES/kg)": 52.0, "beans (KES/kg)": 118.0, "goat, medium (KES/head)": 5200.0,
                "milk (KES/litre)": 74.0}
        month = dt.date(2025, 1, 1)
        while month <= dt.date(2027, 6, 1):
            k = (month.year - 2025) * 12 + month.month - 1
            for mk in markets:
                for item, b in base.items():
                    season = 1 + 0.08 * np.sin(2 * np.pi * (month.month - 3) / 12.0)
                    drought = 1 + (0.18 if dt.date(2025, 9, 1) <= month <= dt.date(2026, 4, 1) else 0.0)
                    if "goat" in item:
                        drought = 2.0 - drought
                    v = b * season * drought * (1 + 0.004 * k) * (1 + r.normal(0, 0.05))
                    rows.append((month.strftime("%Y-%m"), mk, item, round(v, 0 if "goat" in item else 1)))
            month = (month.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        return pd.DataFrame(rows, columns=["month", "market", "commodity", "price"])

    def rainfall(self):
        r = sim.crng("rain")
        rows = []
        stations = ["Laga Town (KMD)", "North Laga mission", "Lake fisheries station", "East Laga dispensary",
                    "West Laga borehole"]
        for st in stations:
            for m in range(1, 8):
                for d in (1, 2, 3):
                    ltm = max(0.0, 22.0 * np.exp(-((m - 4.2) ** 2) / 1.6) + 2.0)
                    v = max(0.0, ltm * r.gamma(1.6, 0.62))
                    rows.append((st, "2027-%02d-D%d" % (m, d), round(v, 1), round(ltm, 1)))
        return pd.DataFrame(rows, columns=["station", "dekad", "rainfall_mm", "long_term_mean_mm"])
