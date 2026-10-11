"""The four extracts as the district's warehouse holds them: Ellery's medical claim lines, Quarrystone's PBM claims,
Ellery's eligibility spans and the conversion file Ellery built from Bramwell's records on 1 January 2025.

Every service event in sim.events becomes one claim per component with its own lines and codes; the claim history
then carries what a real one carries: replacement and void claims, denied lines, a resubmission after a denial,
claims billed under the wrong family member and voided, duplicates, services after coverage ended, and run-out
(a claim paid after the cut-off is not in the extract). PBM claims carry return-to-stock and reverse-and-rebill
reversals. None of it changes what the plan actually allowed for a service that happened."""
import datetime as dt
import math
import zlib
from collections import defaultdict

import numpy as np

import world as W

DAY = dt.timedelta(days=1)
CUT = W.PAID_THROUGH
START = W.CONVERSION


def h(*parts):
    return zlib.crc32("|".join(str(x) for x in parts).encode())


# ------------------------------------------------------------------ code tables
LABS = ["80053", "85025", "80061", "83036", "84443", "81003", "80048", "82947", "84153", "87086", "82306", "83550"]
IMG = {
    "xray": [("0324", "71046"), ("0320", "73030"), ("0320", "73610"), ("0320", "72100"), ("0320", "73562")],
    "ct": [("0352", "74177"), ("0351", "70450"), ("0352", "71260")],
    "mri": [("0610", "73721"), ("0612", "72148"), ("0611", "70551")],
    "us": [("0402", "76700"), ("0402", "76856"), ("0402", "76805")],
}
OPSURG = [("45380", "00811"), ("45378", "00812"), ("43239", "00731"), ("29881", "01400"), ("47562", "00790"),
          ("66984", "00142"), ("49505", "00830"), ("58558", "00952"), ("19120", "00400"), ("64483", "01992")]
OPSURG_DX = {"45380": "K63.5", "45378": "Z12.11", "43239": "K21.9", "29881": "M23.221", "47562": "K80.20",
             "66984": "H25.11", "49505": "K40.90", "58558": "N92.0", "19120": "N63.10", "64483": "M54.16"}
OPHOSP = [("0483", "93306", "93306"), ("0482", "93017", "93016"), ("0740", "95810", "95810"),
          ("0761", "97597", "97597"), ("0260", "96365", "96365"), ("0920", "93880", "93880")]
OPHOSP_DX = {"93306": "R01.1", "93017": "R07.89", "95810": "G47.33", "97597": "L97.512", "96365": "E86.0", "93880": "I65.23"}
SURG_IP = {"M48.062": ("22612", "00630"), "I35.0": ("33405", "00567"), "K57.20": ("44140", "00790"),
           "E66.01": ("43644", "00797"), "C50.911": ("19303", "00406"), "C50.912": ("19303", "00406"),
           "C18.7": ("44204", "00790"), "C34.11": ("32663", "00541"), "C61": ("55866", "00865")}
TRAUMA_CPT = {"S72.001A": "27236", "S82.201A": "27759", "S27.0XXA": "32551", "S32.009A": "22325", "S06.5X0A": "61312"}
CHEMO_J = {"breast": ("J9355", 60), "colon": ("J9035", 40), "lung": ("J9271", 200), "lymphoma": ("J9312", 70)}
ANES = {"joint_knee": "01402", "joint_hip": "01214", "kidney": "00868", "liver": "00796", "vaginal": "01967", "csec": "01961"}


def em_office(amt, spec, new):
    if new:
        return "99204" if (spec or amt > 170) else "99203"
    if amt < 125:
        return "99213"
    if amt < 185:
        return "99214"
    return "99215"


def prev_code(age):
    for lim, code in ((1, "99391"), (5, "99392"), (12, "99393"), (18, "99394"), (40, "99395"), (65, "99396")):
        if age < lim:
            return code
    return "99397"


class Builder:
    def __init__(self, S, rng):
        self.S = S
        self.r = rng
        self.npi = {k: [W.make_npi(b) for b in v] for k, v in W.PROVIDER_BASES.items()}
        self.pharm_npi = [W.make_npi(b) for b in W.PHARMACY_BASES]
        self.plan_at = {}

    # ---------------------------------------------------------------- coverage
    def fam_state(self, fam, d):
        plan, tier = fam.hist[0][1], fam.hist[0][2]
        for eff, pl, ti in fam.hist:
            if eff <= d:
                plan, tier = pl, ti
        cls = fam.cls_hist[0][1]
        for eff, c in fam.cls_hist:
            if eff <= d:
                cls = c
        return plan, tier, cls

    def spans(self, p):
        """coverage spans with the current administrator, as of the extract (inclusive dates; blank end = open)"""
        fam = self.S.fams[p.fid]
        a = max(p.start, START)
        b = p.end
        if a > CUT or (b is not None and b < a):
            return []
        changes = sorted({eff for eff, _, _ in fam.hist if a < eff} | {eff for eff, _ in fam.cls_hist if a < eff})
        cuts = [a] + [c for c in changes if (b is None or c <= b) and c <= CUT]
        out = []
        for i, s in enumerate(cuts):
            e = cuts[i + 1] - DAY if i + 1 < len(cuts) else b
            if e is not None and e > CUT:
                e = None
            plan, tier, cls = self.fam_state(fam, s)
            if out and out[-1][2:] == (plan, tier, cls):
                out[-1] = (out[-1][0], e, plan, tier, cls)
            else:
                out.append((s, e, plan, tier, cls))
        return out

    # ---------------------------------------------------------------- claim lines for one component
    def lines(self, ev, comp, p):
        """returns (bill_type or '', place of service or '', [(rev, proc, mod, units, weight)])"""
        r = self.r
        pid, d0, d1, ben, kind, comps, info = ev
        ct, prov, amt, lag = comp
        dx = info.get("dx", "") if info else ""
        los = max(1, (d1 - d0).days)
        age = p.age(d0)
        if ct == "P":
            if kind in ("office", "office_spec", "prenatal", "urgent"):
                spec = kind == "office_spec"
                new = r.random() < 0.06
                code = em_office(amt, spec, new)
                ls = [("", code, "", 1, 1.0)]
                if kind == "urgent":
                    pos = "20"
                    if r.random() < 0.35:
                        ls.append(("", "87880", "", 1, 0.12))
                else:
                    pos = "11" if (prov != "specialist" or r.random() < 0.8) else "22"
                    if r.random() < 0.12:
                        ls.append(("", "96372", "", 1, 0.09))
                return "", pos, ls
            if kind == "preventive":
                ls = [("", prev_code(age), "", 1, 1.0)]
                if age < 18 and r.random() < 0.6:
                    ls += [("", "90460", "", 1, 0.08), ("", "90700" if age < 7 else "90651", "", 1, 0.3)]
                elif d0.month >= 9 and r.random() < 0.5:
                    ls += [("", "90471", "", 1, 0.07), ("", "90686", "", 1, 0.12)]
                return "", "11", ls
            if kind == "lab":
                k = int(r.integers(1, 4))
                picks = list(dict.fromkeys(r.choice(LABS, size=k, replace=False)))
                ls = [("", c, "", 1, 1.0 + 0.4 * r.random()) for c in picks]
                if r.random() < 0.7:
                    ls.append(("", "36415", "", 1, 0.08))
                return "", "81", ls
            if kind.startswith("img_") or kind == "cancer_img":
                rev, cpt = IMG[kind[4:]][int(r.integers(0, len(IMG[kind[4:]])))] if kind.startswith("img_") else ("0352", "74177")
                return "", "22", [("", cpt, "26", 1, 1.0)]
            if kind == "er":
                lvl = "99285" if amt > 1000 else "99284" if amt > 650 else "99283"
                ls = [("", lvl, "", 1, 1.0)]
                if r.random() < 0.3:
                    ls.append(("", "93010", "", 1, 0.08))
                return "", "23", ls
            if kind == "op_surgery":
                cpt, anes = OPSURG[h(pid, d0, "op") % len(OPSURG)]
                if prov == "anesthesia":
                    return "", "24", [("", anes, "QK", int(r.integers(5, 13)), 1.0)]
                return "", "24", [("", cpt, "", 1, 1.0)]
            if kind == "op_hospital":
                rev, cpt, prof = OPHOSP[h(pid, d0, "oph") % len(OPHOSP)]
                return "", "22", [("", prof, "26" if prof == cpt and rev != "0761" and rev != "0260" else "", 1, 1.0)]
            if kind in ("admit", "admit_trauma", "admit_cardiac", "admit_surgery", "transplant", "joint", "postacute_facility"):
                if prov in ("specialist", "transplant") and kind in ("admit_surgery", "admit_trauma", "transplant", "joint"):
                    if kind == "admit_surgery":
                        cpt = SURG_IP.get(dx, ("44140", "00790"))[0]
                    elif kind == "admit_trauma":
                        cpt = TRAUMA_CPT.get(dx, "27236")
                    elif kind == "transplant":
                        cpt = "50360" if info.get("organ") == "kidney" else "47135"
                    else:
                        cpt = "27447" if info.get("site") == "knee" else "27130"
                    ls = [("", cpt, "", 1, 1.0)]
                    if los > 2:
                        ls.append(("", "99024", "", 1, 0.0))
                    return "", "21", ls
                if prov == "anesthesia":
                    if kind == "transplant":
                        code = ANES[info.get("organ", "kidney")]
                    elif kind == "joint":
                        code = ANES["joint_" + info.get("site", "knee")]
                    else:
                        code = SURG_IP.get(dx, ("", "00790"))[1]
                    return "", "21", [("", code, "AA", int(r.integers(10, 26)), 1.0)]
                if kind == "admit_cardiac" and prov == "specialist" and dx.startswith("I21"):
                    return "", "21", [("", "93458", "26", 1, 0.35), ("", "92928", "", 1, 0.65)]
                n_sub = max(0, min(los - 1, 6))
                ls = [("", "99223", "", 1, 1.0)]
                if n_sub:
                    ls.append(("", "99233" if kind != "admit" else "99232", "", n_sub, 0.55 * n_sub))
                ls.append(("", "99239" if los > 3 else "99238", "", 1, 0.6))
                return "", "21", ls
            if kind == "delivery":
                if prov == "anesthesia":
                    return "", "21", [("", ANES["csec" if info.get("csec") else "vaginal"], "QK", int(r.integers(6, 15)), 1.0)]
                return "", "21", [("", "59510" if info.get("csec") else "59400", "", 1, 1.0)]
            if kind == "newborn":
                return "", "21", [("", "99460", "", 1, 1.0), ("", "99238", "", 1, 0.45)]
            if kind == "nicu":
                days = max(1, los)
                k1 = min(days - 1, 6)
                ls = [("", "99468", "", 1, 1.0)]
                if k1 > 0:
                    ls.append(("", "99469", "", k1, 0.42 * k1))
                if days - 1 - k1 > 0:
                    ls.append(("", "99480", "", days - 1 - k1, 0.2 * (days - 1 - k1)))
                return "", "21", ls
            if kind == "dialysis":
                return "", "11", [("", "90960", "", 1, 1.0)]
            if kind in ("chemo", "infusion"):
                return "", "11", [("", "99215" if kind == "chemo" else "99214", "", 1, 1.0)]
            if kind == "radiation":
                return "", "22", [("", "77427", "", 4, 1.0)]
            if kind == "biopsy":
                cpt = {"C50.911": "19083", "C50.912": "19083", "C18.7": "45380", "C34.11": "31628", "C83.30": "38221",
                       "C91.10": "38221", "C61": "55700"}.get(dx, "19083")
                return "", "22", [("", cpt, "", 1, 0.75), ("", "88305", "26", 1, 0.25)]
            if kind == "cardiac_rehab":
                return "", "22", [("", "99214", "", 1, 1.0)]
            if kind == "pt":
                if r.random() < 0.12:
                    return "", "11", [("", "97162", "", 1, 1.0)]
                return "", "11", [("", "97110", "GP", int(r.integers(2, 4)), 0.65), ("", "97140", "GP", 1, 0.35)]
            if kind == "therapy":
                tele = r.random() < 0.35
                return "", "10" if tele else "11", [("", "90837" if amt > 135 else "90834", "95" if tele else "", 1, 1.0)]
            if kind == "ambulance":
                return "", "41", [("", "A0427", "", 1, 0.82), ("", "A0425", "", int(r.integers(4, 22)), 0.18)]
            return "", "11", [("", "99214", "", 1, 1.0)]
        # institutional
        if kind.startswith("img_"):
            rev, cpt = IMG[kind[4:]][h(pid, d0, kind) % len(IMG[kind[4:]])]
            return "131", "", [(rev, cpt, "", 1, 1.0)]
        if kind == "er":
            lvl = "99285" if amt > 3800 else "99284" if amt > 2200 else "99283"
            ls = [("0450", lvl, "", 1, 0.48), ("0300", "80053", "", 1, 0.1), ("0305", "85025", "", 1, 0.05)]
            if r.random() < 0.55:
                ls.append(("0350", "70450", "", 1, 0.24) if r.random() < 0.4 else ("0324", "71046", "", 1, 0.09))
            if r.random() < 0.5:
                ls.append(("0636", "J2405", "", 1, 0.03))
            ls.append(("0250", "", "", 1, 0.05))
            return "131", "", ls
        if kind == "op_surgery":
            cpt, anes = OPSURG[h(pid, d0, "op") % len(OPSURG)]
            if prov == "asc":
                return "831", "", [("0490", cpt, "", 1, 0.86), ("0250", "", "", 1, 0.06), ("0272", "", "", 1, 0.08)]
            return "131", "", [("0360", cpt, "", 1, 0.62), ("0370", "", "", 1, 0.12), ("0710", "", "", 1, 0.09),
                               ("0250", "", "", 1, 0.07), ("0272", "", "", 1, 0.06), ("0300", "85025", "", 1, 0.04)]
        if kind == "op_hospital":
            rev, cpt, prof = OPHOSP[h(pid, d0, "oph") % len(OPHOSP)]
            ls = [(rev, cpt, "", 1, 0.9), ("0250", "", "", 1, 0.1)]
            return "131", "", ls
        if kind in ("admit", "admit_trauma", "admit_cardiac", "admit_surgery", "joint", "transplant", "delivery",
                    "newborn", "nicu", "postacute_facility"):
            icu = info.get("icu", False)
            days = max(1, los)
            ls = []
            if kind == "nicu":
                ls = [("0174" if info.get("dx") == "P07.32" else "0173", "", "", days, 0.78 * days / max(days, 1)),
                      ("0250", "", "", 1, 0.06), ("0300", "", "", 1, 0.06), ("0410", "", "", 1, 0.06), ("0320", "71045", "", 1, 0.04)]
                return "111", "", ls
            if kind == "newborn":
                return "111", "", [("0171", "", "", days, 0.85), ("0300", "", "", 1, 0.1), ("0250", "", "", 1, 0.05)]
            if kind == "delivery":
                return "111", "", [("0720", "", "", 1, 0.34), ("0122", "", "", days, 0.4), ("0250", "", "", 1, 0.1),
                                   ("0300", "", "", 1, 0.06), ("0370", "", "", 1, 0.1)]
            if kind == "postacute_facility":
                return "211", "", [("0120", "", "", days, 0.7), ("0420", "", "", 1, 0.14), ("0430", "", "", 1, 0.1), ("0250", "", "", 1, 0.06)]
            room_w = 0.42
            if icu:
                ic = max(1, days // 2)
                ls.append(("0200" if kind != "admit_cardiac" else "0210", "", "", ic, 0.26))
                if days - ic > 0:
                    ls.append(("0120", "", "", days - ic, 0.18))
            else:
                ls.append(("0120", "", "", days, room_w))
            ls += [("0250", "", "", 1, 0.09), ("0300", "", "", 1, 0.07), ("0270", "", "", 1, 0.05)]
            if kind in ("admit_surgery", "admit_trauma", "joint", "transplant"):
                ls += [("0360", "", "", 1, 0.2), ("0370", "", "", 1, 0.05), ("0710", "", "", 1, 0.03)]
            if kind in ("admit_trauma", "joint") or (kind == "admit_surgery" and info.get("dx") in ("M48.062", "I35.0")):
                ls.append(("0278", "", "", 1, 0.16))
            if kind == "admit_cardiac":
                if info.get("dx", "").startswith("I21"):
                    ls += [("0481", "", "", 1, 0.22), ("0278", "", "", 1, 0.12)]
                else:
                    ls += [("0350", "70450", "", 1, 0.05), ("0610", "70551", "", 1, 0.07)]
            if kind == "transplant":
                ls.append(("0812" if info.get("organ") == "liver" else "0811", "", "", 1, 0.48))
            if kind in ("admit", "admit_trauma", "admit_cardiac") and r.random() < 0.65:
                ls.append(("0450", "99285", "", 1, 0.04))
            if days >= 3 and r.random() < 0.5:
                ls.append(("0410", "", "", 1, 0.03))
            ls.append(("0730", "93005", "", 1, 0.01))
            return "111", "", ls
        if kind == "dialysis":
            n = info.get("sessions", 13)
            return "721", "", [("0821", "90999", "", n, 0.93), ("0636", "J1756", "", 1, 0.03), ("0300", "", "", 1, 0.04)]
        if kind == "chemo":
            jc, units = CHEMO_J.get(info.get("site", "lung"), ("J9271", 200))
            return "131", "", [("0335", "96413", "", 1, 0.06), ("0335", "96415", "", int(r.integers(1, 3)), 0.03),
                               ("0636", jc, "", units, 0.86), ("0260", "96375", "", 1, 0.02), ("0250", "", "", 1, 0.03)]
        if kind == "infusion":
            return "131", "", [("0335", "96413", "", 1, 0.07), ("0335", "96415", "", 1, 0.03),
                               ("0636", "J1745", "", int(r.integers(40, 81)), 0.9)]
        if kind == "radiation":
            return "131", "", [("0333", "77385", "", int(r.integers(14, 23)), 0.88), ("0333", "77014", "", 1, 0.12)]
        if kind == "biopsy":
            return "131", "", [("0360", "", "", 1, 0.7), ("0310", "88305", "", 1, 0.18), ("0250", "", "", 1, 0.12)]
        if kind == "cardiac_rehab":
            return "131", "", [("0943", "93798", "", int(r.integers(8, 13)), 1.0)]
        if kind == "home_health":
            return "321", "", [("0551", "G0299", "", int(r.integers(3, 9)), 0.7), ("0421", "G0151", "", int(r.integers(2, 6)), 0.3)]
        return "131", "", [("0510", "G0463", "", 1, 1.0)]


def split_cents(total, weights):
    """split total (cents) across weights; the remainder goes to the heaviest line"""
    s = sum(weights)
    parts = [int(math.floor(total * w / s)) for w in weights]
    k = max(range(len(weights)), key=lambda i: weights[i])
    parts[k] += total - sum(parts)
    return parts


# ------------------------------------------------------------------ cost sharing
class CostShare:
    """per-member accumulators for the plan year that starts on 1 July"""

    def __init__(self):
        self.acc = defaultdict(lambda: [0, 0])     # (pid, plan year) -> [deductible used, out of pocket] in cents

    def apply(self, pid, d, plan, allowed_c, mode, copay_c=0):
        """mode: 'none' (preventive), 'copay', 'ded' (deductible then coinsurance). returns (ded, copay, coins)"""
        py = d.year if d.month >= 7 else d.year - 1
        a = self.acc[(pid, py)]
        P = W.PLANS[plan]
        ded_lim, oop_lim, coins = int(P["ded"] * 100), int(P["oop"] * 100), P["coins"]
        room = max(0, oop_lim - a[1])
        if mode == "none" or allowed_c <= 0 or room == 0:
            return 0, 0, 0
        if mode == "copay":
            c = min(copay_c, allowed_c, room)
            a[1] += c
            return 0, c, 0
        dd = min(max(0, ded_lim - a[0]), allowed_c, room)
        a[0] += dd
        a[1] += dd
        room -= dd
        co = min(int(round((allowed_c - dd) * coins)), room)
        a[1] += co
        return dd, 0, co


def line_mode(kind, ct, prov, plan, idx):
    """how a line shares cost: preventive care is free, PPO office, urgent care and emergency facility visits take a
    copay on their first line, everything else goes to the deductible and coinsurance"""
    if kind == "preventive":
        return "none", 0
    if plan == "PPO":
        P = W.PLANS["PPO"]
        if kind in ("office", "prenatal") and ct == "P" and idx == 0:
            return "copay", int(P["pcp_copay"] * 100)
        if kind == "office_spec" and ct == "P" and idx == 0:
            return "copay", int(P["spec_copay"] * 100)
        if kind == "urgent" and idx == 0:
            return "copay", int(P["uc_copay"] * 100)
        if kind == "er" and ct == "I":
            return ("copay", int(P["er_copay"] * 100)) if idx == 0 else ("none", 0)
        if kind in ("office", "office_spec", "prenatal", "urgent") and ct == "P":
            return "none", 0
    return "ded", 0


def rx_mode(drug, plan):
    name, ndc, qty, price, bg, spec = W.DRUGS[drug]
    if plan == "HDHP":
        return "ded", 0, None
    rx = W.PLANS["PPO"]["rx"]
    if spec:
        return "pct", 0, rx["S"]
    if bg == "G":
        return "copay", int(rx["G"] * 100), None
    if drug in ("eliquis", "jardiance", "lantus") or drug.startswith(("ozempic", "mounjaro")):
        return "copay", int(rx["P"] * 100), None
    return "copay", int(rx["N"] * 100), None


# ------------------------------------------------------------------ assembling the extracts
class Pack:
    def __init__(self, S, seed):
        self.S = S
        self.rb = np.random.default_rng(seed + 101)     # claim structure and codes
        self.rm = np.random.default_rng(seed + 131)     # claim history mess
        self.rx = np.random.default_rng(seed + 151)     # PBM layout and reversals
        self.B = Builder(S, self.rb)
        self.cs = CostShare()

    def plan_of(self, p, d):
        return self.B.fam_state(self.S.fams[p.fid], d)[0]

    # ---------------------------------------------------------------- true claims and fills, priced and cost-shared
    def price(self):
        S = self.S
        med, fills = [], []
        for ev in S.events:
            if ev[1] < START or ev[1] > CUT:
                continue
            p = S.people[ev[0]]
            if p.member_id is None:
                continue
            if ev[3] == "R":
                fills.append(ev)
                continue
            for ci, comp in enumerate(ev[5]):
                bt, pos, ls = self.B.lines(ev, comp, p)
                cents = int(round(comp[2] * 100))
                weights = [max(w, 0.0) for (_, _, _, _, w) in ls]
                if sum(weights) == 0:
                    weights = [1.0] * len(ls)
                alloc = split_cents(cents, weights) if cents > 0 else [0] * len(ls)
                mark = 1.6 + 0.9 * self.rb.random() if comp[0] == "P" else 2.1 + 1.3 * self.rb.random()
                lines = []
                for (rev, proc, mod, units, w), a in zip(ls, alloc):
                    billed = int(round(a * mark)) if a > 0 else int(round((1800 + 2600 * self.rb.random())))
                    lines.append([rev, proc, mod, units, billed, a, 0, 0, 0, ""])
                ix = self.B.npi[comp[1]] if comp[1] in self.B.npi else self.B.npi["primary"]
                npi = ix[h(p.pid, comp[1]) % len(ix)] if comp[1] in ("primary", "specialist", "hospital") else ix[h(ev[1], p.pid) % len(ix)]
                dx2 = ""
                cs_ = [c for c in sorted(p.conds) if c in W.ICD and W.ICD[c][0] != ev[6].get("dx")]
                if cs_ and self.rb.random() < 0.45:
                    dx2 = W.ICD[cs_[h(p.pid, ev[1]) % len(cs_)]][0]
                dx1 = ev[6].get("dx", "R69")
                if ev[4] == "op_surgery":
                    dx1 = OPSURG_DX[OPSURG[h(p.pid, ev[1], "op") % len(OPSURG)][0]]
                elif ev[4] == "op_hospital" and not ev[6].get("dx", "").startswith(("I50", "J44")):
                    dx1 = OPHOSP_DX[OPHOSP[h(p.pid, ev[1], "oph") % len(OPHOSP)][1]]
                med.append({"pid": p.pid, "d0": ev[1], "d1": ev[2], "ct": comp[0], "bt": bt, "pos": pos,
                            "dx1": dx1, "dx2": dx2, "npi": npi, "lines": lines, "kind": ev[4],
                            "prov": comp[1], "lag": comp[3], "key": (p.pid, ev[1].isoformat(), ev[4], ci), "clean": True})
        # cost sharing in date order across medical and pharmacy, member by member
        items = [(c["pid"], c["d0"], 0, i) for i, c in enumerate(med)] + [(ev[0], ev[1], 1, i) for i, ev in enumerate(fills)]
        items.sort()
        fill_cs = [None] * len(fills)
        for pid, d, typ, i in items:
            p = S.people[pid]
            plan = self.plan_of(p, d)
            if typ == 0:
                c = med[i]
                for k, ln in enumerate(c["lines"]):
                    mode, cop = line_mode(c["kind"], c["ct"], c["prov"], plan, k)
                    ln[6], ln[7], ln[8] = self.cs.apply(pid, d, plan, ln[5], mode, cop)
            else:
                ev = fills[i]
                drug = ev[6]["drug"]
                cents = int(round(ev[5][0][2] * 100))
                mode, cop, pct = rx_mode(drug, plan)
                if mode == "pct":
                    py = d.year if d.month >= 7 else d.year - 1
                    a = self.cs.acc[(pid, py)]
                    room = max(0, int(W.PLANS[plan]["oop"] * 100) - a[1])
                    v = min(int(round(cents * pct[0])), int(pct[1] * 100), room)
                    a[1] += v
                    fill_cs[i] = v
                else:
                    dd, co, ci = self.cs.apply(pid, d, plan, cents, "copay" if mode == "copay" else "ded", cop)
                    fill_cs[i] = dd + co + ci
        self.med, self.fills, self.fill_cs = med, fills, fill_cs

    # ---------------------------------------------------------------- medical claim history
    def medical_versions(self):
        """every adjudicated claim version: dicts with pid, freq, ref (index of the version it acts on), paid, lines,
        status. Versions paid after the cut-off are dropped at the end."""
        S, r = self.S, self.rm
        V = []

        def emit(c, pid, freq, paid, lines, ref=None, denial=None, bt=None):
            V.append({"pid": pid, "freq": freq, "ref": ref, "paid": paid, "lines": lines, "denial": denial,
                      "d0": c["d0"], "d1": c["d1"], "ct": c["ct"], "bt": bt if bt is not None else c["bt"], "pos": c["pos"],
                      "dx1": c["dx1"], "dx2": c["dx2"], "npi": c["npi"]})
            return len(V) - 1

        fam_members = defaultdict(list)
        for p in S.people:
            if p.member_id is not None:
                fam_members[p.fid].append(p)
        for c in self.med:
            p = S.people[c["pid"]]
            paid = c["d1"] + dt.timedelta(days=c["lag"])
            lines = [list(l) for l in c["lines"]]
            n0 = len(V)
            self._claim_mess(c, p, paid, lines, r, V, emit, fam_members)
            c["clean"] = len(V) == n0 + 1 and V[n0]["freq"] == "1" and V[n0]["denial"] is None and V[n0]["paid"] <= CUT
        self._extra_denials(r, emit)
        self.versions = V

    def _claim_mess(self, c, p, paid, lines, r, V, emit, fam_members):
        """one claim's history: resubmission after a denial, a claim billed under the wrong family member and
        voided, a replacement, a bundled line denied, a duplicate denied or paid in error and voided"""
        u = r.random()
        inpatient = c["bt"].startswith("11")
        # a claim denied for missing information and paid on resubmission
        if c["ct"] == "P" and u < 0.008:
            emit(c, c["pid"], "1", paid, [l[:5] + [None, None, None, None, ""] for l in lines], denial="16")
            paid = paid + dt.timedelta(days=int(r.integers(18, 50)))
            emit(c, c["pid"], "1", paid, lines)
            return
        # billed first under another member of the family, voided, then billed correctly
        if c["ct"] == "P" and p.rel != "E" and u < 0.012:
            others = [q for q in fam_members[p.fid] if q.pid != p.pid and q.covered_on(c["d0"])]
            if others:
                q = others[h(p.pid, c["d0"]) % len(others)]
                w = emit(c, q.pid, "1", paid, lines)
                vpaid = paid + dt.timedelta(days=int(r.integers(20, 61)))
                emit(c, q.pid, "8", vpaid, [l[:4] + [-x for x in l[4:9]] + [""] for l in lines], ref=w)
                emit(c, c["pid"], "1", vpaid + dt.timedelta(days=int(r.integers(0, 11))), lines)
                return
        # replacement claims: late charges on inpatient bills, corrected units or codes elsewhere
        rep_p = 0.22 if inpatient else 0.05 if c["ct"] == "I" else 0.015
        if r.random() < rep_p:
            orig = self.wrong_version(c, lines, r)
            o = emit(c, c["pid"], "1", paid, orig)
            rpaid = paid + dt.timedelta(days=int(r.integers(25, 111)))
            if r.random() < 0.08:
                mid = self.wrong_version(c, lines, r)
                o = emit(c, c["pid"], "7", rpaid, mid, ref=o)
                rpaid = rpaid + dt.timedelta(days=int(r.integers(30, 81)))
            emit(c, c["pid"], "7", rpaid, lines, ref=o)
        else:
            o = emit(c, c["pid"], "1", paid, lines)
            # bundled line denied on a paid claim
            if c["ct"] == "P" and c["kind"] in ("lab", "office", "office_spec") and r.random() < 0.06:
                V[o]["lines"] = lines + [["", "36415" if c["kind"] == "lab" else "99211", "", 1,
                                          int(r.integers(1500, 4600)), None, None, None, None, "97"]]
        # duplicates: denied on receipt, or paid in error and voided
        if c["ct"] == "P":
            v = r.random()
            if v < 0.015:
                emit(c, c["pid"], "1", paid + dt.timedelta(days=int(r.integers(7, 31))),
                     [l[:5] + [None, None, None, None, ""] for l in lines], denial="18")
            elif v < 0.0175:
                dp = paid + dt.timedelta(days=int(r.integers(5, 21)))
                d_ = emit(c, c["pid"], "1", dp, [list(l) for l in lines])
                emit(c, c["pid"], "8", dp + dt.timedelta(days=int(r.integers(30, 91))),
                     [l[:4] + [-x for x in l[4:9]] + [""] for l in lines], ref=d_)

    def _extra_denials(self, r, emit):
        """services after coverage ended, and services the plan does not cover"""
        S = self.S
        for p in S.people:
            if p.member_id is None:
                continue
            if p.end is not None and START <= p.end <= CUT - dt.timedelta(days=40) and p.death is None and r.random() < 0.25:
                for _ in range(int(r.integers(1, 3))):
                    d = p.end + dt.timedelta(days=int(r.integers(3, 41)))
                    c = {"d0": d, "d1": d, "ct": "P", "bt": "", "pos": "11", "dx1": "J06.9", "dx2": "",
                         "npi": self.B.npi["primary"][h(p.pid, "primary") % len(self.B.npi["primary"])]}
                    emit(c, p.pid, "1", d + dt.timedelta(days=int(r.integers(10, 35))),
                         [["", "99213", "", 1, int(r.integers(19000, 26000)), None, None, None, None, ""]], denial="27")
            if p.covered_on(dt.date(2026, 1, 1)) and r.random() < 0.012:
                d = dt.date(2025, 3, 1) + dt.timedelta(days=int(r.integers(0, 640)))
                if p.covered_on(d) and p.age(d) >= 18:
                    proc = ["97810", "15823", "92310", "V5261", "97124"][h(p.pid, d) % 5]
                    c = {"d0": d, "d1": d, "ct": "P", "bt": "", "pos": "11", "dx1": "Z41.1" if proc == "15823" else "Z01.00",
                         "dx2": "", "npi": self.B.npi["specialist"][h(p.pid, d) % len(self.B.npi["specialist"])]}
                    emit(c, p.pid, "1", d + dt.timedelta(days=int(r.integers(12, 40))),
                         [["", proc, "", 1, int(r.integers(9000, 160000)), None, None, None, None, ""]], denial="204")

    def wrong_version(self, c, lines, r):
        """the version a replacement corrects: an inpatient bill without its late charges, or a first line priced on
        the wrong units"""
        out = [list(l) for l in lines]
        if c["ct"] == "I" and len(out) > 2:
            return out[:-int(r.integers(1, 3))]
        f = 0.5 if r.random() < 0.5 else 1.6
        l = out[0]
        l[3] = max(1, int(round(l[3] * f))) if l[3] > 1 else (2 if f > 1 else 1)
        l[4] = int(round(l[4] * f))
        new_a = int(round(l[5] * f))
        ded, cop, coi = l[6], l[7], l[8]
        if ded + cop + coi > new_a:
            ded = min(ded, new_a)
            cop = min(cop, new_a - ded)
            coi = min(coi, new_a - ded - cop)
        l[5], l[6], l[7], l[8] = new_a, ded, cop, coi
        return out

    # ---------------------------------------------------------------- PBM claims
    def pharmacy_rows(self):
        S, r = self.S, self.rx
        rxno = {}
        out = []
        home = {}
        self.rx_clean = set()
        for i, ev in enumerate(self.fills):
            pid, d0 = ev[0], ev[1]
            p = S.people[pid]
            info = ev[6]
            drug = info["drug"]
            name, ndc, qty, price, bg, spec = W.DRUGS[drug]
            key = (pid, drug)
            st = rxno.get(key)
            acute = drug in ("amoxicillin",) or (drug in ("ondansetron", "enoxaparin") and False)
            if st is None or acute or st[1] >= 11 or (d0 - st[2]).days > 365:
                st = [int(r.integers(1000000, 9999999)) if not spec else int(r.integers(30000000, 39999999)), -1, d0]
            st[1] += 1
            rxno[key] = st
            if spec:
                ph = W.SPECIALTY_PHARMACY
            else:
                if pid not in home:
                    home[pid] = h(p.fid, "pharm") % (len(W.PHARMACY_BASES) - 1)
                ph = home[pid] if r.random() < 0.9 else int(r.integers(0, len(W.PHARMACY_BASES) - 1))
            gross = int(round(ev[5][0][2] * 100))
            fee = 0 if spec else (int(r.integers(110, 176)) if bg == "G" else int(r.integers(70, 101)))
            fee = min(fee, gross // 2)
            pay = self.fill_cs[i]
            base = {"pid": pid, "rx": st[0], "fill": st[1], "dos": d0, "ph": ph, "drug": drug, "qty": info["qty"],
                    "days": info["days"], "ingr": gross - fee, "fee": fee, "pat": pay, "daw": "1" if (bg == "B" and r.random() < 0.03) else "0"}
            u = r.random()
            if u < 0.015:
                # reverse and rebill: the first submission carried the wrong days supply
                wrong = dict(base)
                f = 3.0 if info["days"] <= 30 else 1 / 3.0
                wrong["days"] = int(round(info["days"] * f))
                wrong["qty"] = round(info["qty"] * f, 1) if bg == "B" else int(round(info["qty"] * f))
                wrong["ingr"] = int(round(base["ingr"] * f))
                wrong["pat"] = min(int(round(pay * f)), wrong["ingr"] + fee)
                out.append(("B1", wrong, d0))
                out.append(("B2", wrong, d0))
                out.append(("B1", base, d0))
            elif u < 0.045 and not spec:
                # filled and never picked up: returned to stock and reversed, then filled again later
                early = d0 - dt.timedelta(days=int(r.integers(5, 21)))
                if early >= max(START, p.start):
                    rts = dict(base)
                    rts["dos"] = early
                    out.append(("B1", rts, early))
                    out.append(("B2", rts, early + dt.timedelta(days=int(r.integers(10, 15)))))
                out.append(("B1", base, d0))
            else:
                out.append(("B1", base, d0))
                self.rx_clean.add(i)
        self.rx_out = out


    # ---------------------------------------------------------------- writers
    def medical_rows(self):
        r = self.rm
        S = self.S
        keep = [v for v in self.versions if v["paid"] <= CUT]
        idx = {id(v): i for i, v in enumerate(self.versions)}
        for v in keep:
            back = int(r.integers(2, 13))
            v["recv"] = max(v["d1"], v["paid"] - dt.timedelta(days=back))
        order = sorted(range(len(keep)), key=lambda i: (keep[i]["recv"], keep[i]["paid"], keep[i]["pid"], i))
        seq = defaultdict(int)
        number = {}
        for i in order:
            v = keep[i]
            d = v["recv"]
            seq[d] += 1 + int(r.integers(0, 4))
            number[idx[id(v)]] = "%02d%03d%06d" % (d.year % 100, d.timetuple().tm_yday, seq[d])
        rows = []
        for v in keep:
            num = number[idx[id(v)]]
            orig = number[v["ref"]] if v["ref"] is not None else ""
            mid = S.people[v["pid"]].member_id
            bt = (v["bt"][:2] + v["freq"]) if v["bt"] else ""
            for k, l in enumerate(v["lines"]):
                rev, proc, mod, units, billed, allowed, ded, cop, coi, den = l
                den = den or v["denial"] or ""
                if allowed is None:
                    amts = ["", "", "", "", "0.00"]
                else:
                    paid = allowed - ded - cop - coi
                    amts = ["%.2f" % (allowed / 100), "%.2f" % (ded / 100), "%.2f" % (cop / 100), "%.2f" % (coi / 100),
                            "%.2f" % (paid / 100)]
                rows.append([num, str(k + 1), v["ct"], bt, v["freq"], orig, mid, v["d0"].isoformat(), v["d1"].isoformat(),
                             v["paid"].isoformat(), v["pos"] if v["ct"] == "P" else "", rev, proc, mod, v["dx1"], v["dx2"],
                             v["npi"], str(units), "%.2f" % (billed / 100)] + amts + [den])
        rows.sort(key=lambda x: (x[9], x[0], int(x[1])))
        return rows

    def pbm_rows(self):
        S, r = self.S, self.rx
        evs = sorted(self.rx_out, key=lambda x: (x[2], 0 if x[0] == "B1" else 1, x[1]["pid"], x[1]["rx"]))
        seq = defaultdict(int)
        rows = []
        for txn, b, proc in evs:
            p = S.people[b["pid"]]
            seq[proc] += 1 + int(r.integers(0, 3))
            num = "%04d%03d%07d" % (proc.year, proc.timetuple().tm_yday, seq[proc] + 1000 * int(r.integers(1, 9)))
            name, ndc, qty, price, bg, spec = W.DRUGS[b["drug"]]
            sg = -1 if txn == "B2" else 1
            gross = b["ingr"] + b["fee"]
            pat = min(b["pat"], gross)
            vals = [b["ingr"] * sg, b["fee"] * sg, gross * sg, pat * sg, (gross - pat) * sg]
            q = b["qty"]
            qtxt = ("%.1f" % q).rstrip("0").rstrip(".") if isinstance(q, float) else str(q)
            fam = S.fams[p.fid]
            rel = "1" if p.rel in ("E", "R") else "2" if p.rel == "S" else "3"
            rows.append([num, txn, "%07d" % b["rx"] if b["rx"] < 10000000 else "%08d" % b["rx"], "%02d" % b["fill"],
                         b["dos"].strftime("%Y%m%d"), proc.strftime("%Y%m%d"), "%09d" % int(fam.emp), p.code,
                         p.dob.strftime("%Y%m%d"), "2" if p.sex == "F" else "1", rel, self.B.pharm_npi[b["ph"]],
                         W.NCPDP_IDS[b["ph"]], ndc, name, bg, b["daw"], qtxt, str(b["days"])]
                        + ["%.2f" % (x / 100) for x in vals])
        return rows

    def eligibility_rows(self):
        S = self.S
        cls_code = {"T": "TCH", "S": "ESP", "A": "ADM", "R": "RET"}
        rel_code = {"E": "SUB", "R": "SUB", "S": "SPS", "C": "DEP"}
        rows = []
        for p in S.people:
            if p.member_id is None:
                continue
            fam = S.fams[p.fid]
            for s, e, plan, tier, cls in self.B.spans(p):
                rows.append([p.member_id, fam.emp, p.code, rel_code[p.rel], p.dob.isoformat(), p.sex, cls_code[cls], tier,
                             W.PLAN_CODE[plan], s.isoformat(), e.isoformat() if e else ""])
        rows.sort(key=lambda x: (x[0], x[9]))
        return rows

    def crosswalk_rows(self, avoid):
        """Ellery's conversion file: one row per Bramwell member record converted on 1 January 2025. A handful of
        members had two Bramwell records (re-enrolled under a second subscriber number); both map to one member."""
        S, r = self.S, self.rm
        conv = [p for p in S.people if p.legacy is not None]
        cost24 = defaultdict(float)
        for ev in S.events:
            if ev[1].year == 2024:
                cost24[ev[0]] += sum(c[2] for c in ev[5])
        pool = [p for p in conv if p.pid not in avoid and cost24[p.pid] < 1500 and p.rel != "E"]
        dups = []
        for i in sorted(r.choice(len(pool), size=9, replace=False)):
            dups.append(pool[int(i)])
        rel_code = {"E": "SUB", "R": "SUB", "S": "SPS", "C": "DEP"}
        rows = []
        for p in conv:
            fam = S.fams[p.fid]
            root, suf = p.legacy.split("-")
            rows.append([root, suf, p.member_id, fam.emp, p.code, rel_code[p.rel], p.dob.strftime("%m/%d/%Y"), ""])
        for p in dups:
            fam = S.fams[p.fid]
            root2 = "%08d" % int(r.integers(60100000, 64990000))
            p.legacy2 = root2 + "-" + ("02" if p.rel == "S" else "03")
            rows.append([root2, p.legacy2.split("-")[1], p.member_id, fam.emp, p.code, rel_code[p.rel],
                         p.dob.strftime("%m/%d/%Y"), "MERGED DUPLICATE PRIOR RECORD"])
            for row in rows:
                if row[2] == p.member_id and row[7] == "":
                    row[7] = "MERGED DUPLICATE PRIOR RECORD"
        rows.sort(key=lambda x: (x[0], x[1]))
        return rows


MED_COLS = ["claim_number", "line_number", "claim_type", "bill_type", "claim_frequency_code", "original_claim_number",
            "member_id", "first_date_of_service", "last_date_of_service", "paid_date", "place_of_service", "revenue_code",
            "procedure_code", "modifier", "diagnosis_code_1", "diagnosis_code_2", "billing_npi", "units", "billed_amount",
            "allowed_amount", "deductible_amount", "copay_amount", "coinsurance_amount", "plan_paid_amount",
            "denial_reason_code"]
PBM_COLS = ["CLAIM_NBR", "TXN_CD", "RX_NBR", "FILL_NBR", "DATE_OF_SERVICE", "DATE_PROCESSED", "CARDHOLDER_ID", "PERSON_CD",
            "PATIENT_DOB", "PATIENT_GENDER_CD", "RELATIONSHIP_CD", "PHARMACY_NPI", "PHARMACY_NCPDP_ID", "NDC", "DRUG_NAME",
            "BRAND_GENERIC_CD", "DAW_CD", "QTY_DISPENSED", "DAYS_SUPPLY", "INGREDIENT_COST", "DISPENSING_FEE",
            "GROSS_AMT_DUE", "PATIENT_PAY_AMT", "PLAN_PAY_AMT"]
ELIG_COLS = ["member_id", "employee_number", "person_code", "relationship", "birth_date", "sex", "employee_class",
             "coverage_tier", "plan_code", "span_start", "span_end"]
XW_COLS = ["prior_subscriber_number", "prior_member_suffix", "member_id", "employee_number", "person_code",
           "relationship", "birth_date", "conversion_note"]


def write_csv(path, cols, rows):
    with open(path, "w", newline="") as f:
        f.write(",".join(cols) + "\n")
        for row in rows:
            f.write(",".join(('"%s"' % x) if ("," in x) else x for x in row) + "\n")
