"""task242 records: the files the city corporation's systems write from the simulated world. The case line list (the
city's dengue surveillance, fed by hospitals, primary health centres and laboratories), the serosurvey's household
sample, its field app export, the laboratory's specimen register and the residents' IgM results, the laboratory's
verification panel, the Domestic Breeding Checkers' November round, the ward master after the delimitation, and two
records the review does not use (station rainfall, the fogging log). Each table draws on its own random stream."""
import datetime as dt
import uuid

import numpy as np
import pandas as pd

import params as P
import sim as S

CITY = "Neithalpuram"
CORP = "Neithalpuram City Municipal Corporation"
LAB = "Department of Microbiology, Neithalpuram Government Medical College"
ZONE_NAMES = [z[1] for z in P.ZONES]
ZONE_CODES = [z[0] for z in P.ZONES]

# how each kind of reporting unit writes a zone; the official name is the corporation's
VARIANTS = {
    "Kadalur": ["Kadalur", "KADALUR", "Kadaloor", "Zone I"],
    "Thenkarai": ["Thenkarai", "THENKARAI", "Then Karai", "Zone II"],
    "Puthanpalli": ["Puthanpalli", "PUTHANPALLI", "Puthenpalli", "Zone III"],
    "Melmangalam": ["Melmangalam", "MELMANGALAM", "Mel Mangalam", "Zone IV"],
    "Vadakkupatti": ["Vadakkupatti", "VADAKKUPATTI", "Vadakupatti", "Zone V"],
    "Kizhakkoor": ["Kizhakkoor", "KIZHAKKOOR", "Kizhakkur", "Zone VI"],
    "Velliyanur": ["Velliyanur", "VELLIYANUR", "Velliyanoor", "Zone VII"],
    "Chinnakulam": ["Chinnakulam", "CHINNAKULAM", "Chinna Kulam", "Zone VIII"],
    "Periyamalai": ["Periyamalai", "PERIYAMALAI", "Periamalai", "Zone IX"],
    "Kottaivayal": ["Kottaivayal", "KOTTAIVAYAL", "Kottai Vayal", "Zone X"],
    "Sengalur": ["Sengalur", "SENGALUR", "Sengaloor", "Zone XI"],
    "Aranmanai": ["Aranmanai", "ARANMANAI", "Aranmanai Zone", "Zone XII"],
}
OUTSIDE = ["Non-resident (Kanchiyur district)", "Non-resident (Ponneri taluk)", "Non-resident (Vellore district)",
           "Non-resident (other state)"]
PRIVATE_HOSP = ["Sri Lakshmi Multispeciality Hospital", "Annai Velankanni Hospital", "Kaveri Medical Centre",
                "Arogya Nursing Home", "Shanthi Hospital", "Meenakshi Mission Clinic", "Vijaya Childrens Hospital",
                "Sundaram Medical Foundation Annexe", "St. Joseph's Hospital", "Rajam Ortho and General Hospital"]
PRIVATE_LAB = ["Medlife Diagnostics", "Nalam Labs", "Aarthi Scans and Labs", "Precision Path Lab",
               "Thyrocare collection centre", "Suguna Clinical Laboratory"]
WORDS = ["Anna", "Gandhi", "Nehru", "Kamarajar", "Bharathi", "Periyar", "Indira", "Rajaji", "Vivekananda", "Thiru",
         "Kalai", "Kaveri", "Vaigai", "Ponni", "Malar", "Mullai", "Senthil", "Murugan", "Ganapathy", "Lakshmi",
         "Saraswathi", "Velan", "Kumaran", "Sundaram", "Valluvar", "Ilango", "Kambar", "Avvai", "Pari", "Thendral",
         "Nethaji", "Bharathidasan", "Ambedkar", "Vallalar", "Kurinji", "Marutham", "Neithal", "Thamarai", "Alamaram",
         "Vembu", "Mangalam", "Selva", "Raja", "Kalyana", "Sowbagya", "Kamban", "Pandian", "Chera", "Chola"]
SUFFIX = ["Nagar", "puram", "pet", "palayam", "kuppam", "medu", "Colony", "Street", "kottai", "thottam", "Salai"]
OLD_N = [15, 16, 15, 16, 15, 17, 15, 15, 16, 16, 15, 15]     # wards per zone before the 2027 delimitation (186)
NEW_N = [16, 16, 16, 16, 16, 17, 16, 15, 16, 16, 16, 16]     # wards per zone after it (192)
RENUMBER = dt.date(2027, 11, 16)                            # the new ward numbers in the inspectors' forms from here


def day2date(d):
    return P.DAY0 + dt.timedelta(days=int(d))


def dmy(d):
    return d.strftime("%d-%m-%Y")


def rng(k):
    return np.random.default_rng([P.SEED, k])


class Records:
    def __init__(self, W):
        self.W = W
        self._survey()
        self._wards()

    # ------------------------------------------------------------------ the case line list
    def line_list(self):
        r = rng(10)
        W = self.W
        units = []
        for k, name in enumerate(ZONE_NAMES):
            units += [("UPHC %s-%d" % (name, j), "uphc", k) for j in (1, 2)]
        units += [("Government Medical College Hospital", "govt", None), ("Government Headquarters Hospital", "govt", None)]
        units += [(u, "pvt", None) for u in PRIVATE_HOSP] + [(u, "lab", None) for u in PRIVATE_LAB]
        tests = {"uphc": (["NS1 RDT", "IgM RDT", "NS1/IgM combo RDT"], [0.5, 0.2, 0.3]),
                 "govt": (["NS1 ELISA", "IgM ELISA", "RT-PCR"], [0.45, 0.4, 0.15]),
                 "pvt": (["NS1 ELISA", "NS1/IgM combo RDT", "IgM ELISA"], [0.4, 0.35, 0.25]),
                 "lab": (["NS1 ELISA", "IgM ELISA", "NS1/IgM combo RDT"], [0.5, 0.3, 0.2])}
        rows = []
        cases = W["cases"]
        ages = np.concatenate([r.integers(1, 15, 30), r.integers(15, 30, 40), r.integers(30, 50, 22), r.integers(50, 80, 8)])
        for (k, d) in cases:
            rows.append(self._case(r, units, tests, ages, ZONE_NAMES[k], k, d))
        # residents of places outside the corporation treated in city hospitals
        city = np.bincount(cases[:, 1] - S.LO, minlength=S.DAYS.size).astype(float)
        nout = int(0.035 * len(cases))
        out_days = r.choice(S.DAYS, size=nout, p=city / city.sum())
        for d in out_days:
            rows.append(self._case(r, units, tests, ages, OUTSIDE[int(r.integers(0, len(OUTSIDE)))], None, int(d)))
        df = pd.DataFrame(rows)
        # a case notified by a private laboratory and again by the hospital that admitted it
        res = df[(df["zone_k"] >= 0) & (df["onset_day"] >= 0)]
        dup = res.sample(frac=0.016, random_state=np.random.RandomState(2421))
        twins = []
        for _, x in dup.iterrows():
            y = x.copy()
            y["notified_day"] = x["notified_day"] + int(r.integers(1, 7))
            y["reporting_unit"] = ["Government Medical College Hospital", "Government Headquarters Hospital"][int(r.integers(0, 2))]
            y["test_done"] = ["NS1 ELISA", "IgM ELISA"][int(r.integers(0, 2))]
            y["classification"] = "CONFIRMED"
            y["hospitalised"] = "Y"
            y["zone"] = VARIANTS[ZONE_NAMES[int(x["zone_k"])]][int(r.integers(0, 4))]
            twins.append(y)
        df = pd.concat([df, pd.DataFrame(twins)], ignore_index=True)
        df = df[df["notified_day"] <= (P.EXTRACT - P.DAY0).days].copy()
        ext = (P.EXTRACT - P.DAY0).days
        df.loc[(df["outcome"] == "RECOVERED") & (df["notified_day"] > ext - 9), "outcome"] = "UNDER TREATMENT"
        df = df.sort_values(["notified_day", "reporting_unit", "onset_day", "age_yrs"], kind="mergesort").reset_index(drop=True)
        yr = df["notified_day"].map(lambda d: day2date(d).year)
        serial = df.groupby(yr).cumcount() + 1
        df.insert(0, "case_no", ["NCMC/DEN/%d/%05d" % (y, s) for y, s in zip(yr, serial)])
        df["notified_on"] = df["notified_day"].map(lambda d: dmy(day2date(d)))
        df["onset_date"] = df["onset_day"].map(lambda d: dmy(day2date(d)))
        self.cases_df = df.copy()
        return df[["case_no", "notified_on", "onset_date", "age_yrs", "sex", "zone", "reporting_unit", "test_done",
                   "classification", "hospitalised", "outcome"]]

    def _case(self, r, units, tests, ages, zone_name, k, d):
        kinds = r.random()
        if k is not None and kinds < 0.42:
            cand = [u for u in units if u[1] == "uphc" and u[2] == k]
        elif kinds < 0.6:
            cand = [u for u in units if u[1] == "govt"]
        elif kinds < 0.85:
            cand = [u for u in units if u[1] == "pvt"]
        else:
            cand = [u for u in units if u[1] == "lab"]
        unit = cand[int(r.integers(0, len(cand)))]
        names, probs = tests[unit[1]]
        test = names[int(r.choice(len(names), p=probs))]
        delay = 1 + int(r.negative_binomial(2, 0.45))
        hosp = "Y" if r.random() < (0.45 if unit[1] in ("govt", "pvt") else 0.05) else "N"
        out = "RECOVERED"
        u = r.random()
        if hosp == "Y" and u < 0.004:
            out = "DIED"
        elif hosp == "Y" and u < 0.012:
            out = "LAMA"
        if k is not None:
            v = VARIANTS[zone_name]
            zt = v[int(r.choice(4, p=[0.62, 0.2, 0.1, 0.08]))]
        else:
            zt = zone_name
        return dict(notified_day=d + delay, onset_day=d, age_yrs=int(ages[int(r.integers(0, len(ages)))]),
                    sex="M" if r.random() < 0.54 else "F", zone=zt, reporting_unit=unit[0], test_done=test,
                    classification="PROBABLE" if "RDT" in test else "CONFIRMED", hospitalised=hosp, outcome=out,
                    zone_k=-1 if k is None else k)

    # ------------------------------------------------------------------ the serosurvey
    def _survey(self):
        W = self.W
        r = rng(11)
        ppl = W["people"]
        hh = {}
        for i, (k, h, m, d) in enumerate(ppl):
            hh.setdefault((int(k), int(h)), []).append((i, int(m), int(d)))
        house, specimens, visits = [], [], []
        ages_pool = np.concatenate([[0] * 2, r.integers(1, 15, 24), r.integers(15, 35, 34), r.integers(35, 60, 28),
                                    r.integers(60, 86, 12)])
        self.age = np.array([int(ages_pool[int(r.integers(0, len(ages_pool)))]) for _ in range(len(ppl))])
        self.sex = np.where(r.random(len(ppl)) < 0.5, "F", "M")
        for k, z in enumerate(W["zones"]):
            n = z["nhh"]
            never = set(r.choice(np.arange(n // 2, n), size=1 + int(r.integers(0, 3)), replace=False).tolist())
            refuse_blood = set()
            for h in range(n):
                mem = hh[(k, h)]
                day = mem[0][2]
                u = r.random()
                status = "occupied" if u >= 0.07 else ("vacant" if u < 0.04 else "not a dwelling")
                rec = dict(zone_k=k, h=h, hid="%02d-%03d" % (k + 1, h + 1), size=len(mem), status=status,
                           never=False, outcome=None, day=day)
                if status != "occupied":
                    rec["outcome"] = 4 if status == "vacant" else 5
                    visits.append((k, h, 1, day, rec["outcome"]))
                    house.append(rec)
                    continue
                if h in never:
                    rec["never"] = True
                    house.append(rec)
                    continue
                # visits: nobody at home sends the team back; refusals and completed interviews end it
                vd, vn, final = day, 0, None
                while final is None:
                    vn += 1
                    u = r.random()
                    if vn == 1:
                        o = 1 if u < 0.66 else (3 if u < 0.89 else (2 if u < 0.985 else 6))
                    else:
                        o = 1 if u < 0.55 else (3 if u < 0.85 else 2)
                    if o == 3 and vn < 3:
                        visits.append((k, h, vn, vd, 3))
                        vd = min(vd + int(r.integers(1, 4)), z["end"])
                        continue
                    final = o
                    visits.append((k, h, vn, vd, o))
                rec["outcome"], rec["day"] = final, vd
                if final == 1:
                    if r.random() < 0.045:
                        refuse_blood.add(h)
                    else:
                        for (i, m, _) in mem:
                            if self.age[i] >= 1 and r.random() < 0.86:
                                specimens.append(dict(i=i, zone_k=k, h=h, m=m, day=vd))
                house.append(rec)
        self.house = pd.DataFrame(house)
        self.visits_raw = visits
        sp = pd.DataFrame(specimens)
        # the laboratory: haemolysed or short specimens are rejected and, while the team is still in the zone, collected
        # again; the cool box from one of a zone's last fieldwork days reached the laboratory warm and most of its sera
        # were haemolysed, after the team had moved on
        r2 = rng(12)
        sp["u"] = r2.random(len(sp))
        sp["u_re"] = r2.random(len(sp))
        cond = np.where(sp["u"] < 0.971, "ACCEPTED", np.where(sp["u"] < 0.991, "HAEMOLYSED", "INSUFFICIENT"))
        sp["condition"] = cond
        self.bad_day = {}
        for k, z in enumerate(W["zones"]):
            m = (sp["zone_k"] == k).values
            for bd in (z["end"], z["end"] - 1, z["end"] - 2, z["end"] - 3):
                hit = m & (sp["day"] == bd).values
                c = np.where(hit & (sp["u_re"].values < 0.62), "HAEMOLYSED", cond)
                lost = pd.Series(c[hit] != "ACCEPTED").groupby(sp["h"].values[hit]).all()
                if 1 <= lost.sum() <= 5:
                    sp.loc[m, "condition"] = c[m]
                    self.bad_day[k] = bd
                    break
        late = np.array([int(d) >= W["zones"][int(k)]["end"] - 3 for d, k in zip(sp["day"], sp["zone_k"])])
        sp["recollect"] = (sp["condition"] != "ACCEPTED") & (~late) & (r2.random(len(sp)) < 0.38)
        sp["barcode"] = ["TS-%02d-%03d-%d" % (k + 1, h + 1, m + 1) for k, h, m in zip(sp["zone_k"], sp["h"], sp["m"])]
        sp["collected_day"] = sp["day"]
        extra = sp[sp["recollect"]].copy()
        extra["barcode"] = extra["barcode"] + "R"
        extra["collected_day"] = extra["day"] + [int(x) for x in r2.integers(2, 5, len(extra))]
        extra["condition"] = np.where(r2.random(len(extra)) < 0.97, "ACCEPTED", "HAEMOLYSED")
        extra["recollect"] = False
        self.specimens = pd.concat([sp, extra], ignore_index=True)

    def sample(self):
        r = rng(13)
        h = self.house.copy()
        streets = ["%s %s" % (WORDS[int(r.integers(0, len(WORDS)))], SUFFIX[int(r.integers(0, len(SUFFIX)))])
                   for _ in range(len(h))]
        h["listing_address"] = ["No. %d, %s" % (int(r.integers(1, 240)), s) for s in streets]
        h["zone"] = [ZONE_NAMES[k] for k in h["zone_k"]]
        h["listing_sl_no"] = h["h"] + 1
        return h[["hid", "zone", "listing_sl_no", "listing_address"]].rename(columns={"hid": "household_id"})

    def visits(self):
        """the field app's export: one submission per visit, a few sent twice from the tablet"""
        r = rng(14)
        rows = []
        teams = {k: (k // 2) for k in range(12)}
        dev = ["collect:%s" % uuid.UUID(int=int(r.integers(0, 2 ** 62)) << 64 | int(r.integers(0, 2 ** 62))).hex[:16]
               for _ in range(6)]
        size = self.house.set_index(["zone_k", "h"])["size"]
        elig_by = {}
        for i, (k, h, m, d) in enumerate(self.W["people"]):
            elig_by[(int(k), int(h))] = elig_by.get((int(k), int(h)), 0) + int(self.age[i] >= 1)
        prev = {}
        for (k, h, vn, d, o) in self.visits_raw:
            t0 = dt.datetime.combine(day2date(d), dt.time(9, 0)) + dt.timedelta(minutes=int(r.integers(0, 480)))
            if (k, h) in prev and t0 <= prev[(k, h)]:
                t0 = prev[(k, h)] + dt.timedelta(minutes=int(r.integers(40, 150)))
            dur = int(r.integers(4, 9)) if o != 1 else int(r.integers(18, 46))
            t1 = t0 + dt.timedelta(minutes=dur)
            prev[(k, h)] = t1
            sub = t1 + dt.timedelta(minutes=int(r.integers(20, 900)))
            team = teams[k]
            rows.append(dict(start=t0, end=t1, sub=sub, deviceid=dev[team], zone=ZONE_NAMES[k],
                             household_id="%02d-%03d" % (k + 1, h + 1), visit_number=vn, visit_outcome=o,
                             members_usual=int(size[(k, h)]) if o == 1 else None,
                             members_eligible=elig_by[(k, h)] if o == 1 else None,
                             interviewer="INT-%02d" % (2 * team + 1 + int(r.integers(0, 2)))))
        df = pd.DataFrame(rows).sort_values("sub", kind="mergesort").reset_index(drop=True)
        twice = df.sample(frac=0.021, random_state=np.random.RandomState(2422)).copy()
        twice["sub"] = twice["sub"] + pd.to_timedelta(r.integers(30, 3000, len(twice)), unit="m")
        df = pd.concat([df, twice], ignore_index=True).sort_values("sub", kind="mergesort").reset_index(drop=True)
        df.insert(0, "_id", np.arange(381201, 381201 + len(df)))
        df.insert(1, "_uuid", [uuid.UUID(int=(int(r.integers(0, 2 ** 62)) << 64) | int(r.integers(0, 2 ** 62)),
                                         version=4).__str__() for _ in range(len(df))])
        ist = dt.timezone(dt.timedelta(hours=5, minutes=30))
        df["_submission_time"] = [(s.replace(tzinfo=ist).astimezone(dt.timezone.utc)).strftime("%Y-%m-%dT%H:%M:%S")
                                  for s in df["sub"]]
        df["start"] = [s.replace(tzinfo=ist).isoformat(timespec="milliseconds") for s in df["start"]]
        df["end"] = [s.replace(tzinfo=ist).isoformat(timespec="milliseconds") for s in df["end"]]
        df["today"] = [s[:10] for s in df["start"]]
        df["__version__"] = np.where(df["today"] < "2027-10-29", "vR7xKpQ3mYcFh2sT9bWdLa", "vN4eGzU8tPqJ6wHc3XyMbo")
        for c in ("members_usual", "members_eligible"):
            df[c] = df[c].map(lambda x: "" if pd.isna(x) else str(int(x)))
        return df[["_id", "_uuid", "start", "end", "today", "deviceid", "zone", "household_id", "visit_number",
                   "visit_outcome", "members_usual", "members_eligible", "interviewer", "__version__",
                   "_submission_time"]]

    def lab_register(self):
        """the laboratory's register of every survey specimen it received, accepted or not"""
        r = rng(15)
        sp = self.specimens.copy()
        recv = []
        for d in sp["collected_day"]:
            t = dt.datetime.combine(day2date(int(d) + 1), dt.time(8, 30)) + dt.timedelta(minutes=int(r.integers(0, 300)))
            recv.append(t)
        sp["received"] = recv
        sp = sp.sort_values(["received", "barcode"], kind="mergesort").reset_index(drop=True)
        sp["lab_no"] = ["SER/27/%05d" % (i + 1) for i in range(len(sp))]
        ok = sp["condition"] == "ACCEPTED"
        sp["action"] = np.where(ok, "TESTED", np.where(sp["recollect"], "REJECTED - RECOLLECTION REQUESTED", "REJECTED"))
        # plates of 88 specimens, run two to five days after receipt, released the next working day
        sp["plate"], sp["tested_day"] = "", -1
        acc = sp[ok].sort_values("received", kind="mergesort")
        plate_no, cur, first = 0, [], None
        for idx, row in acc.iterrows():
            cur.append(idx)
            if len(cur) == 88:
                plate_no += 1
                self._close_plate(sp, cur, plate_no, r)
                cur = []
        if cur:
            plate_no += 1
            self._close_plate(sp, cur, plate_no, r)
        sp["received_on"] = [t.strftime("%Y-%m-%d %H:%M") for t in sp["received"]]
        sp["released_on"] = [day2date(d + 1).isoformat() if d >= 0 else "" for d in sp["tested_day"]]
        sp["zone"] = [ZONE_NAMES[k] for k in sp["zone_k"]]
        self.lab = sp
        return sp[["lab_no", "barcode", "zone", "received_on", "condition", "action", "plate", "released_on"]]

    def _close_plate(self, sp, idx, n, r):
        last = max(sp.loc[i, "received"] for i in idx)
        d = (last.date() - P.DAY0).days + int(r.integers(2, 5))
        for i in idx:
            sp.loc[i, "plate"] = "IGM-27-%03d" % n
            sp.loc[i, "tested_day"] = d

    def results(self):
        """the residents' IgM results: one row per tested resident, the specimen the laboratory tested"""
        r = rng(16)
        lab = self.lab
        t = lab[lab["condition"] == "ACCEPTED"].copy()
        inf, pos = S.read(self.W, t["i"].astype(int).values, t["collected_day"].astype(int).values)
        t["infected"] = inf
        t["result"] = np.where(pos, "REACTIVE", "NON-REACTIVE")
        idx = []
        for res in t["result"]:
            if res == "REACTIVE":
                idx.append(round(float(np.clip(np.exp(r.normal(1.05, 0.42)), 1.11, 7.9)), 2))
            else:
                idx.append(round(float(np.clip(np.exp(r.normal(-1.3, 0.55)), 0.05, 0.89)), 2))
        t["igm_index"] = idx
        t["household_id"] = ["%02d-%03d" % (k + 1, h + 1) for k, h in zip(t["zone_k"], t["h"])]
        t["member_line"] = t["m"] + 1
        t["age_yrs"] = [int(self.age[int(i)]) for i in t["i"]]
        t["sex"] = [self.sex[int(i)] for i in t["i"]]
        t["collected_on"] = [day2date(d).isoformat() for d in t["collected_day"]]
        t = t.sort_values(["zone_k", "household_id", "member_line"], kind="mergesort")
        self.res = t
        return t[["barcode", "household_id", "zone", "member_line", "age_yrs", "sex", "collected_on", "plate",
                  "igm_index", "result"]].rename(columns={"barcode": "specimen_id", "result": "igm_result"})

    # ------------------------------------------------------------------ the verification panel
    def panel(self):
        r = rng(17)
        rows = []
        for arm, i, onset, t, pos in self.W["panel"]:
            if arm != "CASE":
                continue
            o = day2date(onset)
            rows.append(dict(arm="CONFIRMED CASE", ref="FUC/26/%04d" % (i + 1),
                             conf="RT-PCR" if (i * 7) % 10 < 6 else "NS1 ELISA", onset=dmy(o),
                             coll=dmy(o + dt.timedelta(days=t)), pos=pos, key=(i, t)))
        rows.sort(key=lambda x: x["key"])
        kinds = [("Blood donor, pre-season", 150), ("Chikungunya, RT-PCR confirmed", 45), ("Malaria, smear positive", 30),
                 ("Leptospirosis, MAT positive", 30), ("Scrub typhus, IgM ELISA positive", 25),
                 ("Enteric fever, blood culture positive", 20)]
        ctrl = [x for x in self.W["panel"] if x[0] == "CONTROL"]
        j = 0
        for kind, n in kinds:
            for _ in range(n):
                pos = ctrl[j][4]
                if kind.startswith("Blood donor"):
                    c = dt.date(2027, 3, 1) + dt.timedelta(days=int(r.integers(0, 28)))
                    rows.append(dict(arm="NEGATIVE CONTROL", ref="BB/27/%04d" % (j + 1), conf=kind, onset="",
                                     coll=dmy(c), pos=pos, key=None))
                else:
                    o = dt.date(2026, 9, 1) + dt.timedelta(days=int(r.integers(0, 200)))
                    rows.append(dict(arm="NEGATIVE CONTROL", ref="OFI/%02d/%04d" % (o.year % 100, j + 1), conf=kind,
                                     onset=dmy(o), coll=dmy(o + dt.timedelta(days=int(r.integers(6, 22)))), pos=pos,
                                     key=None))
                j += 1
        out = []
        for n, x in enumerate(rows):
            if x["pos"]:
                v = float(np.clip(np.exp(r.normal(0.95, 0.45)), 1.11, 7.5))
            else:
                v = float(np.clip(np.exp(r.normal(-1.25, 0.6)), 0.04, 0.89))
            first, rep = v, ""
            if r.random() < 0.035:                              # a first reading inside the grey zone, read again
                first = float(r.uniform(0.9, 1.1))
                rep = "%.2f" % v
            fr = "REACTIVE" if first >= 1.1 else ("EQUIVOCAL" if first >= 0.9 else "NON-REACTIVE")
            out.append(dict(panel_no="VP-%03d" % (n + 1), arm=x["arm"], patient_ref=x["ref"], confirmed_by=x["conf"],
                            onset_date=x["onset"], collected_on=x["coll"], index_first="%.2f" % first, reading_first=fr,
                            index_repeat=rep, result_final="REACTIVE" if x["pos"] else "NON-REACTIVE"))
        return pd.DataFrame(out)

    # ------------------------------------------------------------------ wards and the November larval round
    def _wards(self):
        """the 2027 delimitation: 186 wards became 192, numbered afresh from Velliyanur round the city"""
        r = rng(18)
        new_order = [6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5]
        new_start, n0 = {}, 0
        for k in new_order:
            new_start[k] = n0
            n0 += NEW_N[k]
        rows, old, names = [], [], set()
        o0 = 0
        for k in range(12):
            olds = list(range(o0 + 1, o0 + OLD_N[k] + 1))
            news = list(range(new_start[k] + 1, new_start[k] + NEW_N[k] + 1))
            split = sorted(r.choice(len(olds), size=NEW_N[k] - OLD_N[k], replace=False).tolist()) if NEW_N[k] > OLD_N[k] else []
            pairs, j = [], 0
            for a, ow in enumerate(olds):
                if a in split:
                    pairs += [(ow, news[j], "part"), (ow, news[j + 1], "part")]
                    j += 2
                else:
                    pairs.append((ow, news[j], "whole"))
                    j += 1
            for ow, nw, how in pairs:
                while True:
                    nm = "%s %s" % (WORDS[int(r.integers(0, len(WORDS)))], SUFFIX[int(r.integers(0, len(SUFFIX)))])
                    if nm not in names:
                        names.add(nm)
                        break
                rows.append(dict(ward_no=nw, ward_name=nm, zone=ZONE_NAMES[k], zone_k=k, old=ow, how=how))
            old += [(ow, k) for ow in olds]
            o0 += OLD_N[k]
        self.new_wards = pd.DataFrame(rows).sort_values("ward_no", kind="mergesort").reset_index(drop=True)
        self.old_zone = dict(old)

    def ward_master(self):
        g = self.new_wards
        out = []
        for _, w in g.iterrows():
            f = "%d (part)" % w["old"] if w["how"] == "part" else "%d" % w["old"]
            out.append(dict(ward_no=w["ward_no"], ward_name=w["ward_name"], zone=w["zone"], former_ward_nos=f))
        return pd.DataFrame(out)

    def inspections(self):
        """the Domestic Breeding Checkers' house inspections in November 2027"""
        r = rng(19)
        rows = []
        q_zone = [0.050, 0.041, 0.058, 0.066, 0.047, 0.036, 0.061, 0.072, 0.054, 0.039, 0.069, 0.044]
        days = [d for d in range(1, 31) if dt.date(2027, 11, d).weekday() != 6]
        serial = {}
        for _, w in self.new_wards.iterrows():
            k, ow, nw = int(w["zone_k"]), int(w["old"]), int(w["ward_no"])
            q = q_zone[k] * float(np.exp(r.normal(0, 0.25)))
            n = int(r.integers(58, 86))
            dbc = ["DBC-%03d%s" % (nw, s) for s in "ab"]
            for _ in range(n):
                serial[ow] = serial.get(ow, 0) + int(r.integers(1, 40))
                pid = "%02d/%03d/%05d" % (k + 1, ow, serial[ow])
                d = int(days[int(r.integers(0, len(days)))])
                who = dbc[int(r.integers(0, 2))]
                base = dict(k=k, old=ow, new=nw, pid=pid, dbc=who)
                if r.random() < 0.06:                         # nobody to open the house: the call is logged, nothing inspected
                    rows.append(dict(base, day=d, wet=0, pos=0, sr="", rem="LOCKED", kind="locked"))
                    d2 = d + int(r.integers(2, 7))
                    if d2 > 30 or dt.date(2027, 11, d2).weekday() == 6 or r.random() >= 0.7:
                        continue
                    d = d2
                wet = int(r.poisson(3.4))
                pos = int(r.binomial(wet, q)) if wet else 0
                sr = "Y" if pos > 0 and r.random() < 0.92 else ("N" if pos > 0 else "")
                u = r.random()
                rem = ("DRY" if wet == 0 else "OWNER ABSENT, INSPECTED WITH NEIGHBOUR" if u < 0.02 else
                       "OVERHEAD TANK NOT ACCESSIBLE" if u < 0.05 else "SR DONE" if sr == "Y" and u < 0.45 else "")
                rows.append(dict(base, day=d, wet=wet, pos=pos, sr=sr, rem=rem, kind="round"))
                if sr == "Y":
                    fd = d + int(r.integers(6, 10))
                    if fd <= 30 and dt.date(2027, 11, fd).weekday() != 6:
                        wet2 = max(0, wet - pos - int(r.integers(0, 2)))
                        u = r.random()
                        pos2 = 0 if u < 0.8 else (1 if u < 0.97 else 2)
                        rows.append(dict(base, day=fd, wet=max(wet2, pos2), pos=pos2, sr="Y" if pos2 else "",
                                         rem="SR DONE" if pos2 else ("DRY" if max(wet2, pos2) == 0 else ""), kind="follow"))
        df = pd.DataFrame(rows).sort_values(["day", "new", "pid"], kind="mergesort").reset_index(drop=True)
        df["inspected_on"] = [dt.date(2027, 11, d).isoformat() for d in df["day"]]
        df["ward_no"] = [o if dt.date(2027, 11, d) < RENUMBER else n for d, o, n in zip(df["day"], df["old"], df["new"])]
        df["record_id"] = ["INS/2711/%05d" % (i + 1) for i in range(len(df))]
        self.insp = df.copy()
        out = df.rename(columns={"pid": "premise_id", "wet": "wet_containers", "pos": "positive_containers",
                                 "sr": "source_reduction", "dbc": "inspector", "rem": "remarks"})
        out["premise_type"] = "Residential"
        out = out[["record_id", "inspected_on", "ward_no", "premise_id", "premise_type", "wet_containers",
                   "positive_containers", "source_reduction", "remarks", "inspector"]]
        dup = out.sample(frac=0.008, random_state=np.random.RandomState(2423))
        out = pd.concat([out, dup]).sort_values(["inspected_on", "record_id"], kind="mergesort").reset_index(drop=True)
        return out

    # ------------------------------------------------------------------ records the review does not use
    def rainfall(self):
        r = rng(20)
        stations = [("TMP-AWS-01", "Corporation headquarters AWS"), ("TMP-ARG-04", "Kadalur rain gauge"),
                    ("TMP-ARG-09", "Periyamalai rain gauge")]
        rows = []
        d = dt.date(2026, 10, 1)
        while d <= dt.date(2027, 12, 31):
            m = d.month
            wet = {10: 0.45, 11: 0.55, 12: 0.35, 1: 0.08, 2: 0.04, 3: 0.04, 4: 0.08, 5: 0.12, 6: 0.3, 7: 0.38, 8: 0.42,
                   9: 0.4}[m]
            for sid, nm in stations:
                f = 1.15 if "Periyamalai" in nm and m in (6, 7, 8, 9) else (1.2 if "Kadalur" in nm and m in (10, 11, 12) else 1.0)
                mm = float(r.gamma(0.8, 14.0) * f) if r.random() < wet else 0.0
                rows.append(dict(station_id=sid, station_name=nm, date=d.isoformat(), rainfall_mm="%.1f" % mm))
            d += dt.timedelta(days=1)
        return pd.DataFrame(rows)

    def fogging(self):
        r = rng(21)
        rows = []
        acts = [("Thermal fogging", 0.45), ("ULV cold fogging", 0.2), ("Indoor space spray", 0.15),
                ("Source reduction drive", 0.2)]
        for d in range(0, 365):
            n = int(r.poisson(1.2 + 3.5 * np.exp(-0.5 * ((d - 245) / 45.0) ** 2) + 2.5 * np.exp(-0.5 * ((d - 315) / 25.0) ** 2)))
            for _ in range(n):
                k = int(r.integers(0, 12))
                w = self.new_wards[self.new_wards["zone_k"] == k].sample(1, random_state=np.random.RandomState(int(r.integers(0, 2 ** 31)))).iloc[0]
                a = acts[int(r.choice(4, p=[x[1] for x in acts]))][0]
                rows.append(dict(date=day2date(d).isoformat(), zone=ZONE_NAMES[k], locality=w["ward_name"], activity=a,
                                 houses_covered=int(r.integers(40, 600)) if a != "Thermal fogging" else "",
                                 insecticide_litres="%.1f" % float(r.uniform(2, 18)) if "fogging" in a or "spray" in a else "",
                                 trigger=["Case cluster", "Routine schedule", "Public complaint"][int(r.choice(3, p=[0.5, 0.35, 0.15]))]))
        return pd.DataFrame(rows)

    # ------------------------------------------------------------------ the published zone values
    def published(self):
        t = self.res
        out = []
        for k, name in enumerate(ZONE_NAMES):
            x = t[t["zone_k"] == k]
            n, a = len(x), int((x["result"] == "REACTIVE").sum())
            out.append(dict(code=ZONE_CODES[k], zone=name, tested=n, reactive=a, share=round(100.0 * a / n, 1)))
        return pd.DataFrame(out)
