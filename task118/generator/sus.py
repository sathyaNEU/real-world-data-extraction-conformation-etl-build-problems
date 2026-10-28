"""The falls cohort the asks read: SUS admitted patient care episodes, 1 March 2025 to 31 July 2026, for Kestrel Vale
patients aged 65 or over who had an emergency admission with an external cause code in 2025-26. Built as stays (one or
more provider spells joined by transfers between hospitals), each spell one or more consultant episodes, then flattened
to the extract's episode rows; the asks' truth is taken from the stays before they are flattened."""
import datetime as dt

import numpy as np

import params as P
from world import rid

D = dt.timedelta

PROVIDERS = [  # provider, site, site name, kind, trust
    ("RKV", "RKV01", "Kestrel Royal Hospital", "acute", "Kestrel Vale Hospitals NHS Trust"),
    ("RKV", "RKV02", "Saltreach District Hospital", "acute", "Kestrel Vale Hospitals NHS Trust"),
    ("RKV", "RKV03", "Corvenham General Hospital", "acute", "Kestrel Vale Hospitals NHS Trust"),
    ("RWF", "RWF01", "Fenmarsh Royal Infirmary", "acute", "Wold and Fenmarsh University Hospitals NHS Foundation Trust"),
    ("RWF", "RWF03", "Hethermoss Hospital", "acute", "Wold and Fenmarsh University Hospitals NHS Foundation Trust"),
    ("RCW", "RCW11", "Quenford Community Hospital", "community", "Kestrel Wold Community Health NHS Trust"),
    ("RCW", "RCW14", "Ledbridge Community Hospital", "community", "Kestrel Wold Community Health NHS Trust"),
    ("RCW", "RCW17", "Saltreach Memorial Hospital", "community", "Kestrel Wold Community Health NHS Trust"),
]
HOME_SITE = {"CC": "RKV03", "LN": "RKV03", "SC": "RKV02", "QR": "RKV02", "FM": "RWF01", "HM": "RWF03"}
ALT_SITE = {"CC": "RKV01", "LN": "RKV01", "SC": "RKV01", "QR": "RWF03", "FM": "RWF03", "HM": "RWF01"}
TRAUMA = {"RKV02": "RKV01", "RKV03": "RKV01", "RWF03": "RWF01"}     # a district site's hip fractures go to the trust's
COMMUNITY = {"CC": "RCW14", "LN": "RCW14", "SC": "RCW17", "QR": "RCW11", "FM": "RCW11", "HM": "RCW17"}  # trauma unit
OTHER_ACUTE = {"RKV01": "RWF01", "RKV02": "RWF01", "RKV03": "RWF01", "RWF01": "RKV01", "RWF03": "RKV01"}

FALL_PRIMARY = [("S720", 0.20, "hip"), ("S721", 0.07, "hip"), ("S722", 0.03, "hip"), ("S7200", 0.0, "hip"),
                ("S3250", 0.05, "minor"), ("S422", 0.06, "minor"), ("S525", 0.07, "minor"), ("S062", 0.04, "head"),
                ("S065", 0.03, "head"), ("S010", 0.09, "minor"), ("S008", 0.07, "minor"), ("S202", 0.05, "minor"),
                ("T149", 0.05, "minor"), ("R55X", 0.06, "medical"), ("R296", 0.06, "medical"), ("S800", 0.07, "minor")]
FALL_CAUSE = [("W010", 0.22), ("W060", 0.05), ("W100", 0.09), ("W180", 0.18), ("W190", 0.30), ("W199", 0.12),
              ("W050", 0.04)]
OTHER_INJURY = [("S610", "W220"), ("S819", "W540"), ("S300", "X500"), ("S270", "V476"), ("T140", "X590"),
                ("S398", "W229"), ("S010", "W450")]
MEDICAL = [("J189", 0.22), ("N390", 0.18), ("I509", 0.12), ("J440", 0.10), ("A419", 0.08), ("R410", 0.07),
           ("K590", 0.06), ("I489", 0.07), ("E86X", 0.05), ("L039", 0.05)]
COMORB = ["I10X", "E119", "F03X", "N189", "Z864", "I489", "M819", "E039", "Z921", "F329", "H269", "G20X"]
TFC = {"hip": ["110", "430"], "minor": ["180", "300", "430"], "head": ["150", "180", "430"],
       "medical": ["300", "430", "400"], "community": ["314", "430"], "rehab": ["314"]}


def _pick(rs, items):
    w = np.array([i[1] for i in items], dtype=float)
    return items[int(rs.choice(len(items), p=w / w.sum()))]


class Gen:
    def __init__(self, prs):
        self.rs = np.random.default_rng(P.SEED + 7)
        self.prs = prs
        self.spell_no = {s[1]: 0 for s in PROVIDERS}
        self.by_loc = {}
        for p in prs:
            self.by_loc.setdefault(p["locality"], []).append(p)
        self.patients, self.stays = [], []

    def practice(self, loc):
        ps = self.by_loc[loc]
        w = np.array([p["weight"] for p in ps])
        return ps[int(self.rs.choice(len(ps), p=w / w.sum()))]["code"]

    def new_spell_no(self, site):
        self.spell_no[site] += 1
        return "%s%07d" % (site[-2:], 3100000 + self.spell_no[site] * 7 + int(self.rs.integers(0, 7)))

    def episodes(self, start, end, primary, secondary, kind, in_hospital_fall=False):
        """split a spell into consultant episodes; the first carries the admitting coding"""
        rs = self.rs
        n = 1 if (end - start).days < 2 else int(rs.choice([1, 2, 3], p=[0.58, 0.32, 0.10]))
        cuts = sorted({start + D(days=int(rs.integers(1, max(2, (end - start).days)))) for _ in range(n - 1)})
        bounds = [start] + cuts + [end]
        eps = []
        for k in range(len(bounds) - 1):
            if k == 0:
                diags = [primary] + secondary
                tfc = TFC[kind][int(rs.integers(0, len(TFC[kind])))]
            else:
                follow = ["Z509", "Z478", primary] if kind == "hip" else [primary, "Z751", "R268"]
                diags = [follow[int(rs.integers(0, len(follow)))]] + [c for c in secondary if not c.startswith(("W", "V", "X"))]
                if in_hospital_fall and k == 1:
                    diags = diags[:1] + ["S008", "W060"] + diags[1:]
                tfc = TFC["rehab" if kind == "hip" else kind][0] if rs.random() < 0.5 else TFC[kind][-1]
            eps.append(dict(start=bounds[k], end=bounds[k + 1], diags=diags[:8], tfc=tfc))
        return eps

    def comorb(self):
        k = int(self.rs.integers(0, 5))
        return [COMORB[int(i)] for i in self.rs.choice(len(COMORB), size=k, replace=False)]


def build(prs):
    g = Gen(prs)
    rs = g.rs
    names = {c: n for c, n, _, _ in P.LOCALITIES}
    sid_n = 0
    fh_code = [p["code"] for p in prs if p["predecessor"] == P.MERGED[0]][0]

    def patient(loc):
        nonlocal sid_n
        sid_n += 1
        age0 = int(min(103, 65 + rs.gamma(3.2, 5.8)))           # age on 1 April 2025
        pr = g.practice(loc)
        marsh = loc == P.MERGED[1] and pr == fh_code and rs.random() < 0.55
        p = dict(sid="S" + rid("sus", sid_n, n=11, alpha="0123456789ABCDEF"), loc=loc, practice=pr, marsh=marsh,
                 age0=age0, bday=int(rs.integers(0, 365)), sex="F" if rs.random() < 0.63 else "M", stays=[])
        g.patients.append(p)
        return p

    def age_at(p, d):
        return p["age0"] + (1 if (d - P.FY_FROM).days >= p["bday"] else 0) + (1 if (d - P.FY_FROM).days >= p["bday"] + 365 else 0)

    def practice_at(p, d):
        return P.MERGED[0] if (p["marsh"] and d < P.MERGED_ON) else p["practice"]

    def spell(p, site, method, source, start, end, primary, secondary, kind, dest, dmethod, in_fall=False):
        return dict(site=site, provider=site[:3], spell_no=g.new_spell_no(site), method=method, source=source,
                    start=start, end=end, dest=dest, dmethod=dmethod, practice=practice_at(p, start),
                    age=age_at(p, start), episodes=g.episodes(start, end, primary, secondary, kind, in_fall))

    def receiving(acute):
        """how the receiving hospital codes a patient moved in from another hospital"""
        if acute:
            m = _pick(rs, [("2B", 0.68), ("21", 0.20), ("81", 0.12)])[0]
        else:
            m = _pick(rs, [("81", 0.92), ("28", 0.08)])[0]
        return m, ("51" if rs.random() < (0.88 if acute else 0.90) else "19")

    def leave(kind, hops, end, latest_end, rehab_ok=True):
        """where a spell ends: died, home or a care home, or moved to a community hospital for rehabilitation"""
        if rs.random() < (0.05 if kind == "hip" else 0.025):
            return "79", "4"
        p_tr = {"hip": 0.26, "head": 0.10, "minor": 0.06, "medical": 0.05}.get(kind, 0.03) if hops < 2 else 0.0
        if rehab_ok and rs.random() < p_tr and end + D(days=25) < latest_end:
            return "51", "1"
        return ("19" if rs.random() < 0.86 else ["54", "65", "85"][int(rs.integers(0, 3))]), "1"

    def stay(p, start, primary, secondary, kind, method, source, fall, latest_end):
        """one stay: the admitting spell and any moves to another hospital, to the day the patient leaves hospital
        care. A hip fracture seen at a district site is moved to the trust's trauma unit, mostly the same day."""
        loc = p["loc"]
        site = HOME_SITE[loc] if rs.random() < 0.85 else ALT_SITE[loc]
        spells = []
        cur_kind = kind
        if kind == "hip" and site in TRAUMA and rs.random() < 0.78:
            stay0 = 0 if rs.random() < 0.80 else 1
            spells.append(spell(p, site, method, source, start, start + D(days=stay0), primary, secondary, kind, "51",
                                "1"))
            gap = 0 if rs.random() < 0.90 else 1
            m, src = receiving(True)
            s0 = spells[-1]["end"] + D(days=gap)
            e0 = min(s0 + D(days=int(min(50, rs.lognormal(2.55, 0.45)))), latest_end)
            dest, dm = leave("hip", 1, e0, latest_end)
            spells.append(spell(p, TRAUMA[site], m, src, s0, e0, primary, secondary, "hip", dest, dm))
        else:
            los = {"hip": rs.lognormal(2.75, 0.45), "head": rs.lognormal(1.7, 0.7), "minor": rs.lognormal(1.2, 0.9),
                   "medical": rs.lognormal(1.6, 0.75)}[kind]
            los = int(min(60, los if rs.random() > (0.10 if kind == "minor" else 0.02) else 0))
            end = min(start + D(days=los), latest_end)
            dest, dm = leave(kind, 0, end, latest_end)
            if dest == "19" and kind in ("head", "medical") and rs.random() < 0.05 and end + D(days=20) < latest_end:
                dest = "51"                                     # moved to the other trust's acute site
            spells.append(spell(p, site, method, source, start, end, primary, secondary, kind, dest, dm,
                                in_fall=(not fall and kind == "medical" and rs.random() < 0.04)))
        hops = len(spells) - 1
        while spells[-1]["dest"] == "51":
            prev = spells[-1]
            hops += 1
            gap = 0 if rs.random() < 0.86 else 1
            s0 = prev["end"] + D(days=gap)
            if prev["site"].startswith("RCW") or cur_kind in ("hip", "minor") or hops > 1 or rs.random() < 0.5:
                nsite = COMMUNITY[loc] if not prev["site"].startswith("RCW") else ("RCW11" if prev["site"] != "RCW11"
                                                                                  else "RCW14")
                m, src = receiving(False)
                e0 = min(s0 + D(days=max(1, int(min(55, rs.lognormal(2.9, 0.4))))), latest_end)
                pr, sec, k2 = "Z509", [primary] + [c for c in secondary if not c.startswith(("W", "X", "V"))], "community"
            else:
                nsite = OTHER_ACUTE[prev["site"]]
                m, src = receiving(True)
                e0 = min(s0 + D(days=max(1, int(min(30, rs.lognormal(1.9, 0.6))))), latest_end)
                pr, sec, k2 = primary, secondary, cur_kind
            dest, dm = leave(k2, hops, e0, latest_end, rehab_ok=not nsite.startswith("RCW") or hops < 2)
            spells.append(spell(p, nsite, m, src, s0, e0, pr, sec, k2, dest, dm))
            cur_kind = k2
        st = dict(spells=spells, fall=fall, start=spells[0]["start"], end=spells[-1]["end"],
                  died=spells[-1]["dmethod"] == "4", age=spells[0]["age"], practice=spells[0]["practice"],
                  emergency=True)
        if not all(st["end"] <= x["start"] or st["start"] >= x["end"] for x in p["stays"]):
            return None
        p["stays"].append(st)
        g.stays.append((p, st))
        return st

    def free(p, a, b):
        return all(b < s["start"] or a > s["end"] for s in p["stays"])

    def admit_method(fall):
        m = _pick(rs, [("21", 0.84), ("22", 0.04), ("28", 0.05), ("2A", 0.03), ("2D", 0.02), ("23", 0.01), ("24", 0.01)])
        return m[0]

    def source():
        return "19" if rs.random() < 0.85 else ["54", "65", "85"][int(rs.integers(0, 3))]

    def fall_codes():
        pr, _, kind = _pick(rs, FALL_PRIMARY)
        cause = _pick(rs, FALL_CAUSE)[0]
        sec = g.comorb()
        sec.insert(int(rs.integers(0, len(sec) + 1)), cause)
        return pr, sec, kind

    # the index stays of 2025-26: falls by locality, then other injuries
    for code, name, _, _ in P.LOCALITIES:
        n_falls = int(rs.poisson(P.OVER_65[code] * P.FALLS_PER_100[code] / 100.0))
        made = 0
        while made < n_falls:
            p = patient(code)
            k = 1 + int(rs.random() < 0.09) + int(rs.random() < 0.02)
            for _ in range(k):
                if made >= n_falls:
                    break
                for _try in range(20):
                    d = P.FY_FROM + D(days=int(rs.integers(0, 365)))
                    if free(p, d - D(days=2), d + D(days=70)):
                        break
                pr, sec, kind = fall_codes()
                if stay(p, d, pr, sec, kind, admit_method(True), source(), True, P.FY_TO + D(days=91)):
                    made += 1
        for _ in range(int(round(n_falls * 0.17))):
            p = patient(code)
            d = P.FY_FROM + D(days=int(rs.integers(0, 365)))
            pr, cause = OTHER_INJURY[int(rs.integers(0, len(OTHER_INJURY)))]
            sec = g.comorb()
            sec.insert(0, cause)
            stay(p, d, pr, sec, "minor", admit_method(False), source(), False, P.FY_TO + D(days=91))

    # readmissions after a stay, then the cohort's other admissions across the extract's window
    for p in list(g.patients):
        for st in sorted(list(p["stays"]), key=lambda s: s["start"]):
            if st["died"] or rs.random() > 0.135:
                continue
            gap = int(min(30, rs.exponential(10.0)))
            if rs.random() < 0.06:
                gap = 0
            d = st["end"] + D(days=gap)
            if d > P.SUS_TO - D(days=15) or not all(d > s["end"] or d + D(days=12) < s["start"]
                                                     for s in p["stays"] if s is not st):
                continue
            if rs.random() < 0.25:
                pr, sec, kind = fall_codes()
                stay(p, d, pr, sec, kind, admit_method(True), source(), True, P.SUS_TO - D(days=1))
            else:
                pr = _pick(rs, MEDICAL)[0]
                stay(p, d, pr, g.comorb(), "medical", admit_method(False), source(), False, P.SUS_TO - D(days=1))
        if any(s["died"] for s in p["stays"]):
            continue
        for _ in range(int(rs.poisson(0.55 * 17 / 12))):
            d = P.SUS_FROM + D(days=int(rs.integers(0, (P.SUS_TO - P.SUS_FROM).days - 20)))
            if not free(p, d - D(days=1), d + D(days=15)):
                continue
            if any(s["died"] and s["end"] < d for s in p["stays"]):
                continue
            if rs.random() < 0.2:
                pr, sec, kind = fall_codes()
                stay(p, d, pr, sec, kind, admit_method(True), source(), True, P.SUS_TO - D(days=1))
            else:
                pr = _pick(rs, MEDICAL)[0]
                stay(p, d, pr, g.comorb(), "medical", admit_method(False), source(), False, P.SUS_TO - D(days=1))
        if rs.random() < 0.12:
            d = P.SUS_FROM + D(days=int(rs.integers(0, (P.SUS_TO - P.SUS_FROM).days - 10)))
            if free(p, d - D(days=1), d + D(days=6)) and not any(s["died"] and s["end"] < d for s in p["stays"]):
                site = HOME_SITE[p["loc"]]
                pr = ["H251", "M161", "M171", "K409", "C443"][int(rs.integers(0, 5))]
                sp = spell(p, site, ["11", "12", "13"][int(rs.integers(0, 3))], "19", d,
                           d + D(days=int(rs.integers(0, 5))), pr, g.comorb(), "medical", "19", "1")
                st = dict(spells=[sp], fall=False, start=d, end=sp["end"], died=False, age=sp["age"],
                          practice=sp["practice"], emergency=False)
                p["stays"].append(st)
                g.stays.append((p, st))
    # a patient who died has no later admission
    for p in g.patients:
        dead = [s["end"] for s in p["stays"] if s["died"]]
        if dead:
            cut = min(dead)
            gone = [s for s in p["stays"] if s["start"] >= cut and not (s["died"] and s["end"] == cut)]
            keep = [s for s in p["stays"] if not any(s is x for x in gone)]
            p["stays"] = keep
            for s in gone:
                g.stays = [x for x in g.stays if x[1] is not s]
    return g


def truth(g, register):
    """the asks per locality from the stays: fall admissions in 2025-26 aged 65 to 79 and 80 or over, the bed-days of
    those stays, and those followed by another emergency admission within 30 days of leaving hospital care"""
    loc_of = {r["code"]: r["locality"] for r in register}
    for r in register:
        if r["predecessor"]:
            loc_of[r["predecessor"]] = r["locality"]
    out = {c: dict(falls_65_79=0, falls_80=0, bed_days=0, readmitted=0) for c, _, _, _ in P.LOCALITIES}
    for p in g.patients:
        stays = sorted(p["stays"], key=lambda s: s["start"])
        for st in stays:
            if not st["fall"] or not (P.FY_FROM <= st["start"] <= P.FY_TO):
                continue
            first = st["spells"][0]
            assert first["method"] not in ("2B", "81") and first["method"].startswith("2")
            assert any(c[:3] >= "W00" and c[:3] <= "W19" for c in first["episodes"][0]["diags"])
            o = out[loc_of[st["practice"]]]
            o["falls_65_79" if st["age"] < 80 else "falls_80"] += 1
            o["bed_days"] += (st["end"] - st["start"]).days
            if not st["died"]:
                if any(s["emergency"] and s is not st and st["end"] <= s["start"] <= st["end"] + D(days=30)
                       for s in stays):
                    o["readmitted"] += 1
    return out


EP_COLS = ["sus_pseudo_id", "provider_code", "site_code", "hospital_spell_no", "episode_no", "admission_date",
           "admission_method", "admission_source", "episode_start_date", "episode_end_date", "discharge_date",
           "discharge_method", "discharge_destination", "age_at_start", "sex", "gp_practice_code",
           "treatment_function_code", "primary_diagnosis", "diag_02", "diag_03", "diag_04", "diag_05", "diag_06",
           "diag_07", "diag_08"]


def rows(g):
    out = []
    for p, st in g.stays:
        for sp in st["spells"]:
            n = len(sp["episodes"])
            for k, ep in enumerate(sp["episodes"]):
                last = k == n - 1
                diags = ep["diags"] + [""] * (8 - len(ep["diags"]))
                out.append([p["sid"], sp["provider"], sp["site"], sp["spell_no"], k + 1, sp["start"], sp["method"],
                            sp["source"], ep["start"], ep["end"], sp["end"] if last else "",
                            sp["dmethod"] if last else "", sp["dest"] if last else "",
                            sp["age"], p["sex"],
                            sp["practice"] if not (p["marsh"] and ep["start"] >= P.MERGED_ON) else p["practice"],
                            ep["tfc"]] + diags)
    out.sort(key=lambda r: (r[5], r[2], r[3], r[4]))
    return out
