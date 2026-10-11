"""From a simulated service to the claims a plan pays for it.

Each service becomes one or more claim components: the facility's claim (UB-04, revenue code lines with the
hospital's own chargemaster charges) and the professionals' claims (CMS-1500, CPT and HCPCS lines). Professional
lines are allowed at the plan's fee schedule times the group's contract factor, or at the billed charge when the
charge is lower. Hospital outpatient lines are allowed at the hospital's contracted share of charges; inpatient
stays, dialysis, skilled nursing and organ acquisition are paid at a case rate, spread over the claim's lines in
proportion to their charges. Each component carries its own submission lag, adjudication time and the weekly check
run it is paid on.

Component: (claim type, billing NPI, allowed $, days from the last date of service to payment, days to receipt,
            lines, bill type, place of service, diagnosis 1, diagnosis 2)
Line: (revenue code, procedure code, modifier, units, billed cents, allowed cents)"""
import datetime as dt
import math

import numpy as np

import catalog as K
import providers as PV
import world as W

CHARGE_INDEX = {2023: 0.905, 2024: 0.952, 2025: 1.0, 2026: 1.05, 2027: 1.10, 2028: 1.155}
INPATIENT = {"admit", "admit_trauma", "admit_cardiac", "admit_surgery", "joint", "transplant", "delivery", "newborn",
             "nicu", "postacute_facility"}
u01, h = PV.u01, PV.h


def cents(x):
    return int(round(x * 100))


def wpick(items, u):
    """items: [(value, weight)] -> value at the cumulative position u"""
    tot = sum(w for _, w in items)
    acc = 0.0
    for v, w in items:
        acc += w / tot
        if u < acc:
            return v
    return items[-1][0]


def gated(lst, age, sex):
    """entries (code, weight, min age, max age, sex, ...) open to this age and sex"""
    return [x for x in lst if x[2] <= age <= x[3] and (x[4] is None or x[4] == sex)]


def cond_code(pid, cond):
    if cond not in K.COND_CODES:
        return None
    return wpick(K.COND_CODES[cond], u01("cond", pid, cond))


def autoimmune_type(pid):
    i = wpick([(k, x[1]) for k, x in enumerate(K.AUTOIMMUNE)], u01("ai", pid))
    return K.AUTOIMMUNE[i]


# the youngest age a diagnosis is coded at in this plan's claims (first matching prefix), and the sex it belongs to
DX_MIN_AGE = [("R07", 12), ("R06.02", 12), ("R53", 12), ("M54", 12), ("I", 18), ("E11", 12), ("E78", 12), ("R73", 18),
              ("N40", 40), ("N52", 40), ("M17", 40), ("M16", 40), ("M19", 40), ("M23", 14), ("M75", 18), ("M51", 18),
              ("M48", 40), ("S83.2", 12), ("K57", 30), ("K80", 15), ("K81", 15), ("E04", 12), ("R22", 12), ("R91", 18),
              ("J32", 12), ("G43", 10), ("R42", 12), ("G45", 40), ("L97", 40), ("D50", 12), ("R31", 12), ("N20", 12),
              ("K76", 18), ("R10.11", 12), ("F17", 16), ("R92", 25), ("N63", 18), ("N83", 12), ("N92", 12), ("R10.2", 12),
              ("M79.661", 12), ("M25.551", 30), ("G47.33", 2), ("R01", 0), ("Q21", 0)]
PEDS_DX = {"xray": ("R05.9", "J18.9", "R50.9"), "us": ("R10.9", "R11.10"), "ct": ("S06.0X0A", "R51.9"),
           "mri": ("R51.9", "G40.909"), "test": ("R01.1", "R56.9")}


def dx_fits(dx, age, sex):
    for pre, mn in DX_MIN_AGE:
        if dx.startswith(pre):
            return age >= mn
    return True


def specialty_for(dx, age):
    s = "internal"
    for pre, spec in K.DX_SPECIALTY:
        if dx.startswith(pre):
            s = spec
            break
    if age < 18:
        if s in ("cardiology", "gastro", "neuro", "pulm", "endo", "nephro", "hematology", "rheum", "id"):
            return "peds_sub"
        if s not in K.CHILD_SPECIALTIES:
            return "pediatrics"
    elif s == "pediatrics":
        return "internal"
    return s


class Coder:
    def __init__(self, seed=W.SEED, D=None):
        self.r = np.random.default_rng(seed + 37)
        self.D = D or PV.Directory()

    # ---------------------------------------------------------------- amounts
    def _noise(self, *key):
        return math.exp(0.12 * (u01("cn", *key) * 2 - 1) * 1.7)

    def fee_line(self, prov, code, units, y, mod="", rev=""):
        """a professional line at the fee schedule (or the charge, if lower)"""
        if mod == "26":
            base = K.PROF26[code] * K.COMMERCIAL
        elif code in K.JCODE:
            base = K.JCODE[code]
        else:
            base = K.FEE[code] * K.COMMERCIAL
        fee = round(base * K.FEE_INDEX[y] * prov.contract, 2)
        unit_charge = round(base * prov.charge * self._noise(prov.npi, code, mod) * CHARGE_INDEX[y], 2)
        if code in K.JCODE:
            unit_charge = round(base * 1.9 * self._noise(prov.npi, code) * CHARGE_INDEX[y], 2)
        allowed = min(unit_charge, fee)
        return (rev, code, mod, units, cents(unit_charge * units), cents(allowed * units))

    def anes_line(self, prov, code, minutes, y, mod):
        units = K.ANES_BASE.get(code, 5) + minutes / 15.0
        allowed = round(units * K.ANES_CF * K.FEE_INDEX[y] * prov.contract, 2)
        charge = round(units * K.ANES_CF * prov.charge * 1.15 * self._noise(prov.npi, code) * CHARGE_INDEX[y], 2)
        return ("", code, mod, minutes, cents(charge), cents(min(allowed, charge)))

    def unit_charge(self, fac, rev, code, base, y):
        return round(base * fac.charge * self._noise(fac.npi, rev, code) * CHARGE_INDEX[y], 2)

    def cpt_base(self, code, cat):
        return K.FEE.get(code, K.JCODE.get(code, 50)) * K.CDM_MARKUP[cat]

    def outpatient(self, fac, y, fixed, variable, target):
        """fixed: [(rev, code, mod, units, category or base charge)], variable: [(rev, weight)]; charges for the
        variable lines are sized so the claim's allowed comes near the target. Returns lines."""
        lines, tot = [], 0.0
        for rev, code, mod, units, cat in fixed:
            base = cat if isinstance(cat, (int, float)) else self.cpt_base(code, cat)
            uc = self.unit_charge(fac, rev, code, base, y)
            ch = round(uc * units, 2)
            lines.append([rev, code, mod, units, ch])
            tot += ch
        if variable:
            want = max(0.0, target / fac.pct - tot) if target else 0.0
            wsum = sum(w for _, w in variable)
            for rev, w in variable:
                share = want * w / wsum * (0.85 + 0.3 * self.r.random())
                if rev in ("0360", "0370", "0710"):
                    per = self.unit_charge(fac, rev, "", K.REV_CHARGE[rev], y)
                    units = max(2, int(round(share / per)))
                    lines.append([rev, "", "", units, round(per * units, 2)])
                else:
                    lines.append([rev, "", "", 1, round(max(share, 30.0 + 160 * w * self.r.random()), 2)])
        out = []
        seen = set()
        for rev, code, mod, units, ch in lines:
            c = cents(ch)
            a = cents(ch * fac.pct)
            while a in seen:
                a -= 1
                c -= 2
            seen.add(a)
            out.append((rev, code, mod, units, c, a))
        return out

    def case_rate(self, fac, y, amount, room, ancillary):
        """room: [(rev, days)] at the chargemaster's daily rate; ancillary: [(rev, code, weight)]; the case rate is
        spread over the lines in proportion to their charges"""
        lines, tot = [], 0.0
        for rev, days in room:
            uc = self.unit_charge(fac, rev, "", K.REV_CHARGE[rev], y)
            lines.append([rev, "", "", days, round(uc * days, 2)])
            tot += uc * days
        target = amount * fac.markup * (0.82 + 0.36 * self.r.random())
        anc = max(target - tot, 0.18 * target)
        wsum = sum(w for _, _, w in ancillary)
        for rev, code, w in ancillary:
            if rev in K.REV_CHARGE and rev not in ("0360", "0370", "0710"):
                uc = self.unit_charge(fac, rev, code, K.REV_CHARGE[rev], y)
                lines.append([rev, code, "", 1, uc])
                tot += uc
                continue
            ch = round(anc * w / wsum * (0.7 + 0.6 * self.r.random()), 2)
            if rev in ("0360", "0370", "0710"):
                per = self.unit_charge(fac, rev, "", K.REV_CHARGE[rev], y)
                units = max(2, int(round(ch / per)))
                lines.append([rev, code, "", units, round(per * units, 2)])
                tot += per * units
            elif code in K.JCODE:
                units = max(1, int(round(ch / (K.JCODE[code] * 3.2 * fac.charge))))
                lines.append([rev, code, "", units, ch])
                tot += ch
            else:
                lines.append([rev, code, "", 1, ch])
                tot += ch
        total_c = sum(cents(l[4]) for l in lines)
        amt_c = cents(amount)
        if total_c < amt_c * 1.6:
            f = amt_c * (1.6 + 0.8 * self.r.random()) / total_c
            lines = [l[:4] + [round(l[4] * f, 2)] for l in lines]
            total_c = sum(cents(l[4]) for l in lines)
        alloc = [amt_c * cents(l[4]) // total_c for l in lines]
        k = max(range(len(lines)), key=lambda i: lines[i][4])
        alloc[k] += amt_c - sum(alloc)
        out, seen = [], set()
        for (rev, code, mod, units, ch), a in zip(lines, alloc):
            while a in seen and a > 1:
                a -= 1
            seen.add(a)
            out.append([rev, code, mod, units, cents(ch), a])
        # the remainder moved by de-duplication goes back to the largest line
        diff = amt_c - sum(l[5] for l in out)
        out[k][5] += diff
        return [tuple(l) for l in out]

    # ---------------------------------------------------------------- lags
    def lags(self, ct, d1, kind, extra=0):
        """days from the last date of service to receipt and to payment (a Thursday check run)"""
        r = self.r
        if ct == "I":
            sub = r.lognormal(math.log(15), 0.65) if kind in INPATIENT else r.lognormal(math.log(10), 0.7)
        else:
            sub = r.lognormal(math.log(7), 0.85)
        if r.random() < 0.04:
            sub += r.uniform(40, 160)            # billed late (a claim held for coordination of benefits, a refiled claim)
        sub = int(min(300, max(1, round(sub)))) + extra
        u = r.random()
        if u < 0.80:
            adj = int(r.integers(0, 5))
        elif u < 0.93:
            adj = int(r.integers(5, 22))
        else:
            adj = int(r.integers(30, 121))       # pended for records, accident details or coordination of benefits
        recv = d1 + dt.timedelta(days=sub)
        paid = W.next_check_run(recv + dt.timedelta(days=adj + 1))
        return (paid - d1).days, (recv - d1).days

    def comp(self, ct, prov, lines, d1, kind, bt="", pos="", dx1="", dx2="", extra=0):
        lines = tuple(tuple(l) for l in lines)
        amt = round(sum(l[5] for l in lines) / 100.0, 2)
        lag, rlag = self.lags(ct, d1, kind, extra)
        return (ct, prov.npi, amt, lag, rlag, lines, bt, pos, dx1, dx2)

    # ---------------------------------------------------------------- the member's providers
    def clinic(self, p, age, d):
        D = self.D
        if age < 18 and u01("peds_family", p.fid) < 0.45:
            return D.sticky("pediatrics", p.fid)
        if age >= 18 and u01("travel_visit", p.pid, d) < 0.03:
            return D.pick(D.travel("family"), u01("tf", p.pid, d))
        spec = "internal" if (age >= 30 and u01("im", p.fid) < 0.3) else "family"
        return D.sticky(spec, p.fid)

    def hospital_for(self, p, kind, info, age):
        D = self.D
        home = D.home_hospital(p.fid)
        if kind == "transplant":
            return D.hosp["tertiary_tc" if info.get("organ") == "kidney" else "tertiary_r"]
        if kind == "nicu":
            wk = info.get("weeks", 40)
            if wk < 32:
                return D.hosp["childrens"] if u01("nicu", p.pid) < 0.6 else D.hosp["tertiary_tc"]
            return D.hosp["regional"]
        if age < 18 and kind in ("admit", "admit_trauma", "admit_surgery") and u01("kidsh", p.pid, info.get("dx")) < 0.45:
            return D.hosp["childrens"]
        if kind in ("admit_trauma", "admit_cardiac", "admit_surgery", "joint", "delivery", "newborn", "postacute_facility") \
                and home.role in ("cah1", "cah2"):
            return D.hosp["regional"]
        if kind == "admit_trauma" and info.get("icu"):
            return D.hosp["tertiary_tc"]
        if kind == "biopsy" and home.role in ("cah1", "cah2"):
            return D.hosp["regional"]
        if kind == "chemo" or kind == "radiation":
            return D.hosp["tertiary_r"] if u01("onc_site", p.pid) < 0.35 else D.hosp["regional"]
        return home

    def specialist(self, p, spec):
        return self.D.sticky(spec, p.pid)

    def dx2_for(self, p, dx1, age):
        r = self.r
        conds = [c for c in sorted(p.conds) if c in K.COND_CODES]
        if p.adhd and age >= 5:
            conds.append("_adhd")
        if not conds or r.random() >= 0.45:
            return ""
        c = conds[int(r.integers(0, len(conds)))]
        code = p.adhd if c == "_adhd" else cond_code(p.pid, c)
        return "" if code == dx1 else code

    # ---------------------------------------------------------------- one service
    def components(self, p, d0, d1, ben, kind, amount, info, parts):
        info = info or {}
        if ben == "R":
            return (("R", "", round(amount, 2), 0, 0, (), "", "", "", ""),)
        age = p.age(d0)
        y = d0.year
        fshare = sum(s for ct, _, s in parts if ct == "I")
        fn = getattr(self, "k_" + kind, None)
        if fn is None:
            if kind.startswith("img_"):
                return self.k_imaging(p, d0, d1, amount * fshare, info, age, y, kind[4:])
            raise KeyError(kind)
        return fn(p, d0, d1, amount * fshare, info, age, y)

    # office and clinic care -------------------------------------------------
    def em_level(self, new, spec, age, nc):
        r = self.r
        u = r.random()
        if new:
            return "99203" if u < (0.5 if not spec else 0.25) else "99204" if u < 0.94 else "99205"
        if age < 18:
            return "99212" if u < 0.05 else "99213" if u < 0.62 else "99214" if u < 0.97 else "99215"
        shift = min(0.25, 0.06 * nc) + (0.12 if spec else 0.0)
        if u < 0.06 - shift / 4:
            return "99212"
        if u < 0.46 - shift:
            return "99213"
        if u < 0.90 - shift / 2:
            return "99214"
        return "99215"

    def k_office(self, p, d0, d1, fac_amt, info, age, y, spec_visit=False, prenatal=False):
        r = self.r
        dx1 = info.get("dx") or "J06.9"
        if prenatal:
            prov = self.specialist(p, "obgyn")
            spec = True
        elif spec_visit:
            s = info.get("spec") or specialty_for(dx1, age)
            prov = self.specialist(p, s)
            spec = True
        else:
            prov = self.clinic(p, age, d0)
            spec = False
            s = prov.spec
        new = r.random() < (0.10 if spec else 0.05)
        lines = [self.fee_line(prov, self.em_level(new, spec, age, p.nchronic), 1, y)]
        pos = "11"
        sp = prov.spec
        if not prenatal and age >= 18 and sp in ("family", "internal", "psychiatry", "endo", "rheum") and r.random() < 0.07:
            lines[0] = lines[0][:2] + ("95",) + lines[0][3:]
            pos = "10"
        else:
            # what else gets done at the visit, by the kind of practice and the problem
            v = r.random()
            if sp in ("family", "internal", "pediatrics", "urgent"):
                if dx1 in ("J02.9", "J02.0", "J03.90") and v < 0.7:
                    lines.append(self.fee_line(prov, "87880", 1, y))
                elif dx1 in ("J10.1", "B34.9") and v < 0.5:
                    lines.append(self.fee_line(prov, "87804", 1, y))
                elif dx1 == "U07.1" and v < 0.6:
                    lines.append(self.fee_line(prov, "87635", 1, y))
                elif dx1 in ("N39.0", "R30.0") and v < 0.8:
                    lines.append(self.fee_line(prov, "81002", 1, y))
                elif dx1 in ("H61.21", "H61.23") and v < 0.85:
                    lines.append(self.fee_line(prov, "69210", 1, y))
                elif dx1 in ("R07.89", "R00.2", "R42") and age >= 18 and v < 0.6:
                    lines.append(self.fee_line(prov, "93000", 1, y))
                elif dx1 in ("S01.81XA", "S61.411A") and v < 0.6:
                    lines.append(self.fee_line(prov, "12001", 1, y))
                elif dx1 in ("L72.0",) and v < 0.4:
                    lines.append(self.fee_line(prov, "10060", 1, y))
                elif dx1 in ("Z30.41", "Z30.011") and v < 0.25:
                    lines.append(self.fee_line(prov, "96372", 1, y))
                    lines.append(self.fee_line(prov, "J1050", 150, y))
                elif dx1 == "R73.03" and v < 0.5:
                    lines.append(self.fee_line(prov, "82962", 1, y))
                elif v < 0.05 and age >= 12:
                    lines.append(self.fee_line(prov, "96372", 1, y))
                    lines.append(self.fee_line(prov, "J3301" if dx1.startswith("M") else "J1030", 4 if dx1.startswith("M") else 1, y))
            elif sp == "derm":
                if v < 0.35:
                    lines.append(self.fee_line(prov, "17000" if age >= 40 else "17110", 1, y))
                elif v < 0.5:
                    lines.append(self.fee_line(prov, "11102", 1, y))
            elif sp == "ortho" and v < 0.25 and age >= 18:
                lines.append(self.fee_line(prov, "20610", 1, y))
                lines.append(self.fee_line(prov, "J3301", 4, y))
            elif sp == "ophth":
                lines[0] = self.fee_line(prov, "92004" if new else "92014", 1, y)
                if v < 0.3 and age >= 40:
                    lines.append(self.fee_line(prov, "92134", 1, y))
            elif sp == "pulm" and v < 0.3 and age >= 6:
                lines.append(self.fee_line(prov, "94060", 1, y))
            elif sp == "allergy" and v < 0.25:
                lines.append(self.fee_line(prov, "95004", int(r.integers(20, 41)), y))
            elif sp == "cardiology" and v < 0.45:
                lines.append(self.fee_line(prov, "93000", 1, y))
            elif sp == "ent" and dx1.startswith("H61") and v < 0.8:
                lines.append(self.fee_line(prov, "69210", 1, y))
            elif sp == "obgyn" and not prenatal and v < 0.08 and age <= 45:
                lines.append(self.fee_line(prov, "58300", 1, y))
                lines.append(self.fee_line(prov, "J7298", 1, y))
                dx1 = "Z30.430"
        dx2 = info.get("dx2") or self.dx2_for(p, dx1, age)
        return (self.comp("P", prov, lines, d1, "office", pos=pos, dx1=dx1, dx2=dx2),)

    def k_office_spec(self, p, d0, d1, fac_amt, info, age, y):
        return self.k_office(p, d0, d1, fac_amt, info, age, y, spec_visit=True)

    def k_prenatal(self, p, d0, d1, fac_amt, info, age, y):
        return self.k_office(p, d0, d1, fac_amt, info, age, y, prenatal=True)

    def k_urgent(self, p, d0, d1, fac_amt, info, age, y):
        r, D = self.r, self.D
        prov = D.sticky("urgent", p.fid) if r.random() < 0.9 else D.pick(D.travel("urgent"), r.random())
        dx1 = info.get("dx") or "J06.9"
        new = r.random() < 0.35
        lines = [self.fee_line(prov, "99203" if new and r.random() < 0.6 else "99204" if new else
                               ("99213" if r.random() < 0.5 else "99214"), 1, y)]
        if dx1 in ("J02.9", "J02.0", "J03.90"):
            lines.append(self.fee_line(prov, "87880", 1, y))
        elif dx1 in ("J10.1", "B34.9", "J06.9") and r.random() < 0.4:
            lines.append(self.fee_line(prov, "87804", 1, y))
            if r.random() < 0.5:
                lines.append(self.fee_line(prov, "87635", 1, y))
        elif dx1 in ("N39.0", "R30.0"):
            lines.append(self.fee_line(prov, "81002", 1, y))
        elif dx1.startswith("S9") or dx1.startswith("S6") or dx1.startswith("S52"):
            lines.append(self.fee_line(prov, {"S93.401A": "73610", "S93.402A": "73610", "S63.501A": "73110",
                                              "S61.411A": "73130", "S52.521A": "73110"}.get(dx1, "73610"), 1, y))
        elif dx1 in ("S01.81XA", "S61.411A"):
            lines.append(self.fee_line(prov, "12001", 1, y))
        if dx1 in ("J01.90", "J20.9") and r.random() < 0.15:
            lines.append(self.fee_line(prov, "96372", 1, y))
            lines.append(self.fee_line(prov, "J0696", 4, y))
        return (self.comp("P", prov, lines, d1, "urgent", pos="20", dx1=dx1, dx2=self.dx2_for(p, dx1, age)),)

    def k_preventive(self, p, d0, d1, fac_amt, info, age, y):
        r = self.r
        days = (d0 - p.dob).days
        prov = self.clinic(p, age, d0)
        if prov.spec not in ("family", "internal", "pediatrics"):
            prov = self.D.sticky("family", p.fid)
        lines = []
        if age >= 18 and p.sex == "F" and age <= 65 and u01("wellwoman", p.pid) < 0.35:
            prov = self.specialist(p, "obgyn")
        code = None
        for lim, est in ((1, "99391"), (5, "99392"), (12, "99393"), (18, "99394"), (40, "99395"), (65, "99396")):
            if age < lim:
                code = est
                break
        code = code or "99397"
        lines.append(self.fee_line(prov, code, 1, y))
        vacc = []
        flu = d0.month in (9, 10, 11, 12, 1) and days >= 183
        if age < 18:
            sched = {0: ["90723", "90677", "90680", "90648"], 1: ["90707", "90716", "90633", "90677"],
                     4: ["90696", "90710"], 5: ["90696", "90710"], 11: ["90715", "90734", "90651"], 12: ["90651"],
                     16: ["90734", "90620"]}
            vacc = list(sched.get(age, []))
            if age == 0 and days < 60:
                vacc = ["90744"]
            if age == 0 and d0.month in (10, 11, 12, 1, 2, 3) and days < 240 and r.random() < 0.6:
                vacc.append("90381")
            if flu and r.random() < 0.45:
                vacc.append("90656")
            if age in (1, 2) and r.random() < 0.7:
                lines.append(self.fee_line(prov, "96110", 1, y))
            if age in (3, 4, 5):
                lines.append(self.fee_line(prov, "99173", 1, y))
            if age >= 12:
                lines.append(self.fee_line(prov, "96127", 1, y))
            for i, v in enumerate(vacc):
                lines.append(self.fee_line(prov, "90460" if i == 0 else "90461", 1, y))
                lines.append(self.fee_line(prov, v, 1, y))
            dx1 = "Z00.121" if r.random() < 0.22 else "Z00.129"
            if days < 29:
                dx1 = "Z00.110" if days < 8 else "Z00.111"
        else:
            if flu and r.random() < 0.4:
                vacc.append("90656")
            if age >= 50 and r.random() < 0.12:
                vacc.append("90750")
            if r.random() < 0.06:
                vacc.append("90715")
            for i, v in enumerate(vacc):
                lines.append(self.fee_line(prov, "90471" if i == 0 else "90472", 1, y))
                lines.append(self.fee_line(prov, v, 1, y))
            dx1 = "Z00.01" if r.random() < 0.3 else "Z00.00"
            if prov.spec == "obgyn":
                dx1 = "Z01.419"
        dx2 = "Z23" if vacc and r.random() < 0.5 else self.dx2_for(p, dx1, age)
        return (self.comp("P", prov, lines, d1, "preventive", pos="11", dx1=dx1, dx2=dx2),)

    # laboratory -------------------------------------------------------------
    def lab_indication(self, p, age, info, d0):
        r = self.r
        c = p.conds
        if info.get("ind"):
            return info["ind"]
        if age < 1:
            return "newborn_bili" if (d0 - p.dob).days < 10 else "child_routine"
        if age < 2:
            return "infant_lead" if r.random() < 0.6 else "child_routine"
        if age < 18:
            return "strep" if r.random() < 0.45 else "uti" if r.random() < 0.3 else "child_routine"
        opts = [("adult_routine", 16), ("fatigue", 5), ("vitd", 4), ("uti", 5 if p.sex == "F" else 1)]
        if age >= 20:
            opts.append(("lipid_screen", 7))
        if age >= 35:
            opts.append(("diabetes_screen", 5))
        if p.sex == "M" and age >= 45:
            opts.append(("prostate", 7))
        if p.sex == "F" and 16 <= age <= 25:
            opts.append(("sti_screen", 4))
        if p.sex == "F" and age <= 50:
            opts.append(("anemia", 3))
        for cond, ind, wt in (("diabetes", "diabetes", 14), ("htn", "htn", 7), ("lipid", "lipid", 6), ("thyroid", "thyroid", 8),
                              ("kidney_tx", "transplant", 20), ("liver_tx", "transplant", 20), ("hiv", "hiv", 14),
                              ("hepc", "hepc", 10), ("afib", "afib", 4), ("chf", "chf", 6), ("esrd", "ckd", 6)):
            if cond in c:
                opts.append((ind, wt))
        if "autoimmune" in c and autoimmune_type(p.pid)[0].startswith("M0"):
            opts.append(("ra", 8))
        return wpick(opts, r.random())

    def k_lab(self, p, d0, d1, fac_amt, info, age, y):
        r, D = self.r, self.D
        ind = self.lab_indication(p, age, info, d0)
        codes, dx = K.LAB_INDICATIONS[ind]
        codes = list(codes)
        if len(codes) > 2:
            keep = max(2, int(round(len(codes) * (0.7 + 0.3 * r.random()))))
            codes = codes[:keep]
        if dx is None:
            cond = {"diabetes": "diabetes", "htn": "htn", "lipid": "lipid", "thyroid": "thyroid", "transplant": None,
                    "hiv": "hiv", "hepc": "hepc", "afib": "afib", "chf": "chf", "ckd": "esrd", "ra": "autoimmune",
                    "uti": None, "strep": None, "prenatal": None, "glucose_tolerance": None, "gbs": None, "anemia": None}[ind]
            if cond == "autoimmune":
                dx = autoimmune_type(p.pid)[0]
            elif cond:
                dx = cond_code(p.pid, cond)
            elif ind == "transplant":
                dx = "Z94.0" if "kidney_tx" in p.conds else "Z94.4"
            elif ind == "uti":
                dx = "N39.0" if r.random() < 0.6 else "R30.0"
            elif ind == "strep":
                dx = "J02.9"
            elif ind in ("prenatal", "glucose_tolerance", "gbs"):
                dx = info.get("dx", "Z34.82")
            elif ind == "anemia":
                dx = "D50.9" if p.sex == "F" else "D64.9"
        if ind in ("diabetes", "lipid", "htn") and info.get("dx2"):
            pass
        blood = any(c not in ("81003", "81001", "87086", "87088", "87880", "87081", "87491", "87591", "87653") for c in codes)
        simple = ind in ("strep", "uti") and r.random() < 0.6
        if simple or (age < 2 and ind != "infant_lead" and r.random() < 0.3):
            prov = self.clinic(p, age, d0)
            lines = [self.fee_line(prov, "87880" if ind == "strep" else "81002" if ind == "uti" else "85018", 1, y)]
            return (self.comp("P", prov, lines, d1, "lab", pos="11", dx1=dx, dx2=""),)
        u = u01("labco", p.fid, y)
        if u < 0.22:
            fac = D.hosp["regional"] if D.home_hospital(p.fid).role in ("cah1", "cah2") else D.home_hospital(p.fid)
            fixed = [("0300" if c not in ("87086", "87088", "87081", "87880", "87653", "87491", "87591") else "0306", c, "", 1, "lab")
                     for c in codes]
            if blood:
                fixed.append(("0300", "36415", "", 1, "lab"))
            lines = self.outpatient(fac, y, fixed, [], 0)
            return (self.comp("I", fac, lines, d1, "lab", bt="141", dx1=dx),)
        prov = D.local("lab")[0 if u < 0.68 else 1]
        lines = [self.fee_line(prov, c, 1, y) for c in codes]
        if blood:
            lines.append(self.fee_line(prov, "36415", 1, y))
        return (self.comp("P", prov, lines, d1, "lab", pos="81", dx1=dx, dx2=self.dx2_for(p, dx, age)),)

    # imaging ----------------------------------------------------------------
    def k_imaging(self, p, d0, d1, fac_amt, info, age, y, modality=None):
        r, D = self.r, self.D
        mod = modality
        if info.get("ob"):
            code, dx = K.OB_US[int(r.integers(0, len(K.OB_US)))]
            dx2 = info.get("dx2", "")
        elif info.get("code"):
            code, dx, dx2 = info["code"], info["dx"], info.get("dx2", "")
        else:
            opts = gated(K.IMAGING[mod], age, p.sex)
            if not opts:
                mod = "xray" if mod != "us" or age >= 1 else "us"
                opts = gated(K.IMAGING[mod], age, p.sex)
            item = opts[int(wpick([(i, x[1]) for i, x in enumerate(opts)], r.random()))]
            code = item[0]
            dxs = [x for x in item[5] if dx_fits(x, age, p.sex)] or list(PEDS_DX[mod])
            dx = dxs[int(r.integers(0, len(dxs)))]
            dx2 = self.dx2_for(p, dx, age)
        cat = {"xray": "xray", "ct": "ct", "mri": "mri", "us": "us"}.get(mod, "us")
        if code in ("77067", "77063", "77065", "77066"):
            cat = "mammo"
        rev = {"xray": "0320", "ct": "0350", "mri": "0610", "us": "0402", "mammo": "0401"}[cat]
        if code in ("93306", "93880", "93971"):
            rev = "0921" if code != "93306" else "0483"
        home = D.home_hospital(p.fid)
        if u01("imgctr", p.pid, d0) < 0.22 and cat in ("xray", "mri", "us", "mammo"):
            prov = D.local("imaging")[0 if u01("ic", p.fid) < 0.65 else 1]
            lines = [self.fee_line(prov, code, 1, y)]
            if code == "77067" and r.random() < 0.6:
                lines.append(self.fee_line(prov, "77063", 1, y))
            return (self.comp("P", prov, lines, d1, "img", pos="11", dx1=dx, dx2=dx2),)
        fac = home
        fixed = [(rev, code, "", 1, cat)]
        if code == "77067" and r.random() < 0.6:
            fixed.append((rev, "77063", "", 1, cat))
        if cat in ("ct", "mri") and code in ("74177", "71260", "71275", "70553"):
            fixed.append(("0636", "Q9967", "", 100, "drug"))
        flines = self.outpatient(fac, y, fixed, [], 0)
        rad = D.hospital_group("radiology", fac)
        plines = [self.fee_line(rad, c, 1, y, mod="26") for _, c, _, _, _ in fixed if c in K.PROF26]
        out = [self.comp("I", fac, flines, d1, "img", bt="131", dx1=dx, dx2=dx2)]
        if plines:
            out.append(self.comp("P", rad, plines, d1, "img", pos="22", dx1=dx, dx2=dx2))
        return tuple(out)

    # emergency --------------------------------------------------------------
    def k_er(self, p, d0, d1, fac_amt, info, age, y):
        r, D = self.r, self.D
        dx1 = info.get("dx") or "R10.9"
        fac = D.home_hospital(p.fid) if r.random() < 0.88 else (D.hosp["regional"] if r.random() < 0.4 else
                                                                  D.travel_hospital(r.random()))
        lvl = "99285" if fac_amt > 3600 else "99284" if fac_amt > 2100 else "99283" if fac_amt > 1000 else "99282"
        ercharge = {"99281": 640, "99282": 1240, "99283": 2260, "99284": 3880, "99285": 5940}
        fixed = [("0450", lvl, "", 1, ercharge[lvl])]
        labs, imgs, drugs = [], [], []
        if age >= 12 or r.random() < 0.4:
            labs += ["85025", "80048" if age < 40 and r.random() < 0.5 else "80053"]
        if dx1.startswith("R07") or dx1 in ("R55", "R00.2", "R06.02"):
            labs.append("84484")
            fixed.append(("0730", "93005", "", 1, K.REV_CHARGE["0730"]))
            imgs.append("71046")
        if dx1 in ("N39.0", "N20.0", "R10.31", "R10.9") or (dx1.startswith("R10") and p.sex == "F"):
            labs.append("81003")
        if dx1 in ("J18.9", "R05.9", "R06.02"):
            imgs.append("71046")
        if dx1 in ("R10.9", "R10.31", "R10.84") and age >= 12 and r.random() < 0.55:
            imgs.append("74177")
        if dx1 == "N20.0":
            imgs.append("74176")
        if dx1 in ("S06.0X0A", "R51.9", "R42", "S00.83XA") and r.random() < 0.6:
            imgs.append("70450")
        if dx1 in ("S52.501A", "S52.521A"):
            imgs.append("73110")
        if dx1 == "S93.401A":
            imgs.append("73610")
        if dx1 in ("R11.2", "R11.10", "A08.4", "R10.9"):
            drugs.append(("J2405", 4))
            drugs.append(("J7030", 1))
        if dx1 in ("M54.50", "N20.0", "R51.9", "G43.909"):
            drugs.append(("J1885", 2))
        if dx1 in ("J18.9", "L03.115", "N39.0") and r.random() < 0.5:
            drugs.append(("J0696", 4))
        if dx1 in ("T78.40XA", "J05.0"):
            drugs.append(("J1100", 10))
        for c in dict.fromkeys(labs):
            fixed.append(("0300" if c != "81003" else "0307", c, "", 1, "lab"))
        for c in dict.fromkeys(imgs):
            rev = "0350" if c in ("74177", "74176", "70450") else "0320"
            fixed.append((rev, c, "", 1, "ct" if rev == "0350" else "xray"))
        for c, units in drugs:
            fixed.append(("0636" if c != "J7030" else "0258", c, "", units, "drug"))
        if drugs:
            fixed.append(("0260", "96374" if r.random() < 0.6 else "96360", "", 1, "chemoadmin"))
        variable = [("0250", 1.0), ("0270", 0.8)]
        flines = self.outpatient(fac, y, fixed, variable, 0)
        out = [self.comp("I", fac, flines, d1, "er", bt="131", dx1=dx1, dx2=self.dx2_for(p, dx1, age))]
        em = D.hospital_group("emergency", fac)
        plines = [self.fee_line(em, lvl, 1, y)]
        if any(l[1] == "93005" for l in flines):
            plines.append(self.fee_line(em, "93010", 1, y))
        if dx1 in ("S01.81XA", "S61.411A"):
            plines.append(self.fee_line(em, "12011" if dx1.startswith("S01") else "12001", 1, y))
        if dx1 in ("S52.501A", "S52.521A"):
            plines.append(self.fee_line(em, "29125", 1, y))
        out.append(self.comp("P", em, plines, d1, "er", pos="23", dx1=dx1))
        rad_codes = [c for c in dict.fromkeys(imgs) if c in K.PROF26]
        if rad_codes:
            rad = D.hospital_group("radiology", fac)
            out.append(self.comp("P", rad, [self.fee_line(rad, c, 1, y, mod="26") for c in rad_codes], d1, "er",
                                 pos="23", dx1=dx1))
        return tuple(out)

    # procedures -------------------------------------------------------------
    def k_op_surgery(self, p, d0, d1, fac_amt, info, age, y):
        r, D = self.r, self.D
        opts = gated(K.OP_SURGERY, age, p.sex)
        item = opts[int(wpick([(i, x[1]) for i, x in enumerate(opts)], r.random()))]
        cpt, _, _, _, _, dxs, spec, anes, asc_ok = item
        dx1 = dxs[int(r.integers(0, len(dxs)))]
        surgeon = self.specialist(p, spec)
        home = D.home_hospital(p.fid)
        if asc_ok and r.random() < 0.58:
            fac = D.pick(D.by_spec["asc"], u01("asc", p.fid))
            fixed = [("0490", cpt, "", 1, "asc")]
            variable = [("0250", 0.25), ("0272", 0.4)]
            bt, apos = "831", "24"
        else:
            fac = home if home.role not in ("cah2",) else D.hosp["regional"]
            fixed = [("0300", "85025", "", 1, "lab")] if age >= 40 and r.random() < 0.3 else []
            fixed.insert(0, ("0360", cpt, "", 1, 0.0))
            variable = [("0360", 0.0), ("0370", 0.12), ("0710", 0.12), ("0250", 0.12), ("0272", 0.16)]
            bt, apos = "131", "22"
        # the facility is paid the procedure's rate; the procedure room line carries the CPT and a time-based charge
        rate = K.OPS_RATE[cpt][0 if bt == "831" else 1] * K.FEE_INDEX[y] * fac.charge * (0.9 + 0.2 * r.random())
        lines = self._surgery_facility(fac, y, fixed, variable, rate)
        dx2 = self.dx2_for(p, dx1, age)
        out = [self.comp("I", fac, lines, d1, "op_surgery", bt=bt, dx1=dx1, dx2=dx2)]
        out.append(self.comp("P", surgeon, [self.fee_line(surgeon, cpt, 1, y)], d1, "op_surgery", pos=apos, dx1=dx1, dx2=dx2))
        if anes and (cpt not in ("64483", "62323", "52000") or r.random() < 0.35):
            agrp = D.hospital_group("anesthesia", fac if fac.spec == "hospital" else D.hosp["regional"])
            minutes = {"00142": 25, "00812": 30, "00811": 35, "00731": 20, "00170": 45, "00120": 20}.get(anes, 60)
            minutes = int(minutes * (0.75 + 0.6 * r.random()))
            out.append(self.comp("P", agrp, [self.anes_line(agrp, anes, minutes, y, "QK" if r.random() < 0.6 else "AA")],
                                 d1, "op_surgery", pos=apos, dx1=dx1))
        if cpt in ("45380", "45385", "43239", "19120", "11402", "11602", "58558"):
            path = D.pick(D.local("pathology"), u01("path", fac.npi))
            out.append(self.comp("P", path, [self.fee_line(path, "88305", 1 if r.random() < 0.7 else 2, y)], d1,
                                 "op_surgery", pos="81", dx1=dx1, extra=3))
        return tuple(out)

    def _surgery_facility(self, fac, y, fixed, variable, target):
        lines, tot = [], 0.0
        for rev, code, mod, units, cat in fixed:
            if rev == "0360":
                continue
            base = cat if isinstance(cat, (int, float)) else self.cpt_base(code, cat)
            ch = self.unit_charge(fac, rev, code, base, y) * units
            lines.append([rev, code, mod, units, round(ch, 2)])
            tot += ch
        want = max(target / fac.pct - tot, 400.0)
        or_line = [l for l in fixed if l[0] == "0360"]
        wsum = sum(w for _, w in variable) + (0.48 if or_line else 0.0)
        if or_line:
            per = self.unit_charge(fac, "0360", "", K.REV_CHARGE["0360"], y)
            units = max(2, int(round(want * 0.48 / wsum / per)))
            lines.insert(0, ["0360", or_line[0][1], "", units, round(per * units, 2)])
        for rev, w in variable:
            if w <= 0:
                continue
            share = want * w / wsum * (0.85 + 0.3 * self.r.random())
            if rev in ("0370", "0710"):
                per = self.unit_charge(fac, rev, "", K.REV_CHARGE[rev], y)
                units = max(2, int(round(share / per)))
                lines.append([rev, "", "", units, round(per * units, 2)])
            elif rev == "0490":
                lines.append([rev, "", "", 1, round(share, 2)])
            else:
                lines.append([rev, "", "", 1, round(max(share, 25.0), 2)])
        out, seen = [], set()
        for rev, code, mod, units, ch in lines:
            c = cents(ch)
            a = cents(ch * fac.pct)
            while a in seen:
                a -= 1
                c -= 2
            seen.add(a)
            out.append((rev, code, mod, units, c, a))
        return out

    def k_op_hospital(self, p, d0, d1, fac_amt, info, age, y):
        r, D = self.r, self.D
        cond = info.get("cond")
        if cond in K.OP_COND:
            cpt, dx1, spec, rev = K.OP_COND[cond]
            if cond == "diabetes":
                dx1 = "E11.621"
        else:
            opts = gated(K.OP_HOSPITAL, age, p.sex)
            item = opts[int(wpick([(i, x[1]) for i, x in enumerate(opts)], r.random()))]
            cpt, _, _, _, _, dxs, spec, rev = item
            dxs = [x for x in dxs if dx_fits(x, age, p.sex)] or (["R01.1", "Q21.1"] if cpt == "93306" else
                                                                ["R56.00" if age < 6 else "R56.9"] if cpt == "95816" else ["R01.1"])
            dx1 = dxs[int(r.integers(0, len(dxs)))]
        home = D.home_hospital(p.fid)
        fac = home if home.role in ("regional", "community") else D.hosp["regional"]
        fixed = [(rev, cpt, "", 1, "test")]
        variable = [("0250", 0.3)] if rev == "0761" else []
        if cpt == "96365":
            fixed.append(("0636", "J1439", "", 750, "drug"))
            fixed.append(("0260", "96366", "", 1, "chemoadmin"))
        if cpt == "96360":
            fixed.append(("0258", "J7030", "", 2, "drug"))
            fixed.append(("0260", "96361", "", 1, "chemoadmin"))
        if cpt == "93017":
            fixed = [(rev, "93017", "", 1, "test")]
        lines = self.outpatient(fac, y, fixed, variable, 0)
        dx2 = self.dx2_for(p, dx1, age)
        out = [self.comp("I", fac, lines, d1, "op_hospital", bt="131", dx1=dx1, dx2=dx2)]
        if spec != "hospitalist":
            prov = self.specialist(p, spec if age >= 18 or spec not in ("cardiology", "pulm", "neuro") else "peds_sub")
            if cpt in K.PROF26:
                pl = [self.fee_line(prov, cpt, 1, y, mod="26")]
            elif cpt == "93017":
                pl = [self.fee_line(prov, "93016", 1, y), self.fee_line(prov, "93018", 1, y)]
            elif cpt == "97597":
                pl = [self.fee_line(prov, "97597", 1, y)]
            elif cpt == "94060":
                pl = [self.fee_line(prov, "94060", 1, y, mod="26")] if "94060" in K.PROF26 else [self.fee_line(prov, "99213", 1, y)]
            else:
                pl = [self.fee_line(prov, "99213", 1, y)]
            out.append(self.comp("P", prov, pl, d1, "op_hospital", pos="22", dx1=dx1))
        return tuple(out)

    def k_biopsy(self, p, d0, d1, fac_amt, info, age, y):
        r, D = self.r, self.D
        dx1 = info.get("dx")
        cpt, spec = {"C50": ("19083", "radiology"), "C18": ("45380", "gastro"), "C20": ("45380", "gastro"),
                     "C34": ("31628", "pulm"), "C83": ("38221", "oncology"), "C91": ("38221", "oncology"),
                     "C61": ("55700", "urology")}[dx1[:3]]
        fac = self.hospital_for(p, "biopsy", info, age)
        fixed = [("0360", cpt, "", 1, 0.0), ("0310", "88305", "", 1, "lab")]
        if cpt == "19083":
            fixed.append(("0402", "76641", "", 1, "us"))
        lines = self._surgery_facility(fac, y, fixed, [("0250", 0.25), ("0272", 0.3), ("0710", 0.1)], fac_amt)
        prov = self.specialist(p, spec) if spec != "radiology" else D.hospital_group("radiology", fac)
        out = [self.comp("I", fac, lines, d1, "biopsy", bt="131", dx1=dx1),
               self.comp("P", prov, [self.fee_line(prov, cpt, 1, y)], d1, "biopsy", pos="22", dx1=dx1)]
        path = D.pick(D.local("pathology"), u01("path", fac.npi))
        out.append(self.comp("P", path, [self.fee_line(path, "88307" if cpt in ("38221", "55700") else "88305", 1, y, mod="26"),
                                         self.fee_line(path, "88342", 1, y)], d1, "biopsy", pos="22", dx1=dx1, extra=4))
        return tuple(out)

    # cancer care ------------------------------------------------------------
    def k_chemo(self, p, d0, d1, fac_amt, info, age, y):
        r, D = self.r, self.D
        site = info.get("site", "lung")
        dxc = info.get("dx")
        drugs, per_month, immuno = K.CHEMO[site]
        fac = self.hospital_for(p, "chemo", info, age)
        fixed = [("0335", "96413", "", 1, "chemoadmin"), ("0335", "96415", "", 1 + int(r.random() < 0.5), "chemoadmin"),
                 ("0260", "96375", "", 1, "chemoadmin"), ("0636", "J2405", "", 8, "drug"), ("0636", "J1100", "", 12, "drug")]
        base_fixed = sum(self.unit_charge(fac, rv, c, self.cpt_base(c, cat), y) * u for rv, c, _, u, cat in fixed) * fac.pct
        room = max(fac_amt - base_fixed, 400.0)
        # the regimen's standard doses, scaled to the patient (body size, dose adjustments)
        std = sum(u * self.unit_charge(fac, "0636", c, self.cpt_base(c, "drug"), y) * fac.pct for c, u in drugs)
        m = room / std
        for c, u in drugs:
            fixed.append(("0636", c, "", max(1, int(round(u * m))), "drug"))
        lines = self.outpatient(fac, y, fixed, [("0250", 1.0)], 0)
        enc = "Z51.12" if immuno else "Z51.11"
        out = [self.comp("I", fac, lines, d1, "chemo", bt="131", dx1=enc, dx2=dxc)]
        onc = self.specialist(p, "oncology")
        out.append(self.comp("P", onc, [self.fee_line(onc, "99215" if r.random() < 0.4 else "99214", 1, y)], d1, "chemo",
                             pos="22", dx1=dxc))
        return tuple(out)

    def k_infusion(self, p, d0, d1, fac_amt, info, age, y):
        r, D = self.r, self.D
        dx1 = info.get("dx") or autoimmune_type(p.pid)[0]
        home = D.home_hospital(p.fid)
        fac = home if home.role in ("regional", "community") else D.hosp["regional"]
        fixed = [("0335", "96413", "", 1, "chemoadmin"), ("0335", "96415", "", 1, "chemoadmin")]
        base = sum(self.unit_charge(fac, rv, c, self.cpt_base(c, cat), y) * u for rv, c, _, u, cat in fixed) * fac.pct
        unit_allowed = self.unit_charge(fac, "0636", "J1745", self.cpt_base("J1745", "drug"), y) * fac.pct
        units = max(20, int(round((fac_amt - base) / unit_allowed)))
        fixed.append(("0636", "J1745", "", units, "drug"))
        lines = self.outpatient(fac, y, fixed, [], 0)
        out = [self.comp("I", fac, lines, d1, "infusion", bt="131", dx1=dx1)]
        if r.random() < 0.3:
            spec = "gastro" if dx1.startswith("K5") else "rheum"
            prov = self.specialist(p, spec)
            out.append(self.comp("P", prov, [self.fee_line(prov, "99213", 1, y)], d1, "infusion", pos="22", dx1=dx1))
        return tuple(out)

    def k_radiation(self, p, d0, d1, fac_amt, info, age, y):
        r, D = self.r, self.D
        dxc = info.get("dx")
        fac = self.hospital_for(p, "radiation", info, age)
        per = self.unit_charge(fac, "0333", "77385", self.cpt_base("77385", "rad") if "77385" in K.FEE else 1800, y)
        fr = max(4, min(23, int(round(fac_amt * 0.9 / (per * fac.pct)))))
        fixed = [("0333", "77385", "", fr, 1800.0), ("0333", "77014", "", max(1, fr // 5), "rad")]
        lines = self.outpatient(fac, y, fixed, [], 0)
        out = [self.comp("I", fac, lines, d1, "radiation", bt="131", dx1="Z51.0", dx2=dxc)]
        ro = self.specialist(p, "radonc")
        pl = [self.fee_line(ro, "77427", max(1, fr // 5), y)]
        if info.get("first"):
            pl.append(self.fee_line(ro, "77263", 1, y))
        out.append(self.comp("P", ro, pl, d1, "radiation", pos="22", dx1=dxc))
        return tuple(out)

    def k_dialysis(self, p, d0, d1, fac_amt, info, age, y):
        r, D = self.r, self.D
        fac = D.pick(D.by_spec["dialysis"], u01("dial", p.pid))
        n = info.get("sessions", 13)
        lines = self.case_rate(fac, y, fac_amt, [("0821", n)], [("0634", "J0882", 0.08), ("0300", "", 0.04)])
        neph = self.specialist(p, "nephro")
        code = "90960" if n >= 12 else "90961" if n >= 8 else "90962"
        return (self.comp("I", fac, lines, d1, "dialysis", bt="721", dx1="N18.6", dx2="Z99.2"),
                self.comp("P", neph, [self.fee_line(neph, code, 1, y)], d1, "dialysis", pos="11", dx1="N18.6", dx2="I12.0"))

    def k_cardiac_rehab(self, p, d0, d1, fac_amt, info, age, y):
        D = self.D
        home = D.home_hospital(p.fid)
        fac = home if home.role in ("regional", "community") else D.hosp["regional"]
        per = self.unit_charge(fac, "0943", "93798", K.REV_CHARGE["0943"], y)
        n = max(4, min(14, int(round(fac_amt / (per * fac.pct)))))
        lines = self.outpatient(fac, y, [("0943", "93798", "", n, K.REV_CHARGE["0943"])], [], 0)
        return (self.comp("I", fac, lines, d1, "cardiac_rehab", bt="131", dx1=info.get("dx", "I25.2"), dx2="Z95.5"),)

    def k_ambulance(self, p, d0, d1, fac_amt, info, age, y):
        r, D = self.r, self.D
        prov = D.sticky("ambulance", p.fid) if r.random() < 0.9 else D.pick(D.travel("ambulance"), r.random())
        dx = info.get("dx")
        code = "A0433" if dx in ("I21.4", "I63.9") and r.random() < 0.4 else "A0427" if r.random() < 0.75 else "A0429"
        miles = int(r.integers(3, 34))
        lines = [self.fee_line(prov, code, 1, y), self.fee_line(prov, "A0425", miles, y)]
        return (self.comp("P", prov, lines, d1, "ambulance", pos="41", dx1=dx, dx2=info.get("dx2", "")),)

    def k_pt(self, p, d0, d1, fac_amt, info, age, y):
        r = self.r
        prov = self.specialist(p, "pt")
        dx1 = info.get("dx", "M54.50")
        if info.get("first") or r.random() < 0.08:
            lines = [self.fee_line(prov, "97161" if r.random() < 0.4 else "97162", 1, y)]
            if r.random() < 0.5:
                lines.append(self.fee_line(prov, "97110", 1, y))
        else:
            lines = [self.fee_line(prov, "97110", int(r.integers(1, 4)), y)]
            for c, pr in (("97140", 0.6), ("97530", 0.3), ("97112", 0.2), ("G0283", 0.15)):
                if r.random() < pr:
                    lines.append(self.fee_line(prov, c, 1 if c != "97140" else int(r.integers(1, 3)), y))
        lines = [l[:2] + ("GP",) + l[3:] for l in lines]
        return (self.comp("P", prov, lines, d1, "pt", pos="11", dx1=dx1),)

    def k_therapy(self, p, d0, d1, fac_amt, info, age, y):
        r = self.r
        prov = self.specialist(p, "therapist") if r.random() < 0.85 else self.specialist(p, "psychiatry")
        dx1 = info.get("dx") or cond_code(p.pid, "depression") or "F41.9"
        tele = r.random() < 0.32
        if info.get("first"):
            code = "90791" if prov.spec == "therapist" else "90792"
        else:
            code = "90837" if r.random() < 0.45 else "90834" if r.random() < 0.85 else "90832"
            if prov.spec == "psychiatry":
                code = "99214" if r.random() < 0.6 else "99213"
        line = self.fee_line(prov, code, 1, y)
        if tele:
            line = line[:2] + ("95",) + line[3:]
        return (self.comp("P", prov, [line], d1, "therapy", pos="10" if tele else "11", dx1=dx1),)

    def k_home_health(self, p, d0, d1, fac_amt, info, age, y):
        r, D = self.r, self.D
        fac = D.pick(D.by_spec["homehealth"], u01("hh", p.fid))
        rn, pt = int(r.integers(2, 8)), int(r.integers(1, 6))
        lines = self.outpatient(fac, y, [("0551", "G0299", "", rn, K.FEE["G0299"] * 1.9),
                                         ("0421", "G0151", "", pt, K.FEE["G0151"] * 1.9)], [], 0)
        return (self.comp("I", fac, lines, d1, "home_health", bt="322", dx1=info.get("dx"), dx2=info.get("dx2", "")),)

    # inpatient --------------------------------------------------------------
    def _hospital_professionals(self, p, fac, d0, d1, los, y, dx1, age, icu=False, cardiac=False, via_er=False):
        r, D = self.r, self.D
        out = []
        hosp = D.hospital_group("hospitalist", fac)
        lines = [self.fee_line(hosp, "99223" if r.random() < 0.7 else "99222", 1, y)]
        sub = max(0, min(los - 1, 20))
        if icu:
            lines.append(self.fee_line(hosp, "99291", max(1, min(sub, los // 2 or 1)), y))
            sub = max(0, sub - max(1, los // 2))
        if sub:
            lines.append(self.fee_line(hosp, "99232" if r.random() < 0.6 else "99233", sub, y))
        lines.append(self.fee_line(hosp, "99239" if los > 3 else "99238", 1, y))
        out.append(self.comp("P", hosp, lines, d1, "admit", pos="21", dx1=dx1))
        if via_er:
            em = D.hospital_group("emergency", fac)
            out.append(self.comp("P", em, [self.fee_line(em, "99285" if r.random() < 0.7 else "99284", 1, y)], d1, "admit",
                                 pos="23", dx1=dx1))
        if cardiac and age >= 18:
            card = self.specialist(p, "cardiology")
            out.append(self.comp("P", card, [self.fee_line(card, "99254" if r.random() < 0.5 else "99253", 1, y),
                                             self.fee_line(card, "99232", max(1, min(los - 1, 5)), y)], d1,
                                 "admit", pos="21", dx1=dx1))
        elif los >= 2 and r.random() < 0.55:
            spec = specialty_for(dx1, age)
            if spec in ("internal", "family", "pediatrics", "hospitalist"):
                spec = "id" if age >= 18 else "peds_sub"
            cons = self.specialist(p, spec)
            out.append(self.comp("P", cons, [self.fee_line(cons, "99253" if r.random() < 0.6 else "99254", 1, y),
                                             self.fee_line(cons, "99231" if r.random() < 0.5 else "99232", max(1, min(los - 1, 4)), y)],
                                 d1, "admit", pos="21", dx1=dx1))
        if r.random() < 0.55:
            rad = D.hospital_group("radiology", fac)
            codes = ["71045"] + (["70450"] if dx1.startswith(("I63", "S06", "R55")) else
                                 ["74177"] if dx1.startswith(("K", "A41", "R10")) else [])
            out.append(self.comp("P", rad, [self.fee_line(rad, c, 1, y, mod="26") for c in codes], d1, "admit", pos="21", dx1=dx1))
        return out

    def _anc(self, kind, info, los, dx1):
        anc = [("0250", "", 0.20), ("0300", "", 0.14), ("0270", "", 0.06)]
        if kind in ("admit_surgery", "admit_trauma", "joint", "transplant"):
            anc += [("0360", "", 0.20), ("0370", "", 0.05), ("0710", "", 0.03)]
        if kind in ("admit_trauma", "joint") or (kind == "admit_surgery" and dx1 in ("M48.062", "I35.0")):
            anc.append(("0278", "", 0.16))
        if kind == "admit_cardiac":
            if dx1.startswith("I21"):
                anc += [("0481", "", 0.0), ("0278", "", 0.10)]
            else:
                anc += [("0350", "70450", 0.04), ("0610", "70551", 0.05)]
        if kind == "transplant":
            anc.append(("0811" if info.get("organ") == "kidney" else "0812", "", 0.0))
        if los >= 3:
            anc.append(("0410", "", 0.04))
        if kind in ("admit", "admit_trauma", "admit_cardiac") and info.get("via_er", True):
            anc.append(("0450", "99285", 0.03))
        anc.append(("0730", "93005", 0.01))
        anc.append(("0320", "71045", 0.01))
        if los >= 4 or kind in ("joint", "admit_trauma"):
            anc += [("0420", "", 0.03), ("0430", "", 0.02)]
        return anc

    def _inpatient(self, p, d0, d1, fac_amt, info, age, y, kind):
        r, D = self.r, self.D
        dx1 = info.get("dx") or "J18.9"
        los = max(1, (d1 - d0).days)
        fac = self.hospital_for(p, kind, info, age)
        icu = info.get("icu", False)
        if icu:
            ic = max(1, los // 2)
            room = [("0200" if kind != "admit_cardiac" else "0210", ic)]
            if los - ic > 0:
                room.append(("0120", los - ic))
        else:
            room = [("0120", los)]
        lines = self.case_rate(fac, y, fac_amt, room, self._anc(kind, info, los, dx1))
        dx2 = info.get("dx2") or self.dx2_for(p, dx1, age)
        out = [self.comp("I", fac, lines, d1, kind, bt="111", dx1=dx1, dx2=dx2)]
        via_er = kind in ("admit", "admit_trauma", "admit_cardiac") and u01("via_er", p.pid, d0) < 0.7 and not info.get("no_ed")
        out += self._hospital_professionals(p, fac, d0, d1, los, y, dx1, age, icu, kind == "admit_cardiac", via_er)
        if kind in ("admit_surgery", "admit_trauma", "joint", "transplant"):
            if kind == "admit_surgery":
                cpt, anes, spec = K.SURG_IP.get(dx1, ("44140", "00790", "gensurg"))
            elif kind == "admit_trauma":
                cpt, anes = K.TRAUMA_CPT.get(dx1, ("27236", "01230"))
                spec = "neurosurg" if dx1.startswith("S06") or dx1.startswith("S32") else "gensurg" if dx1.startswith("S27") else "ortho"
            elif kind == "transplant":
                cpt = "50360" if info.get("organ") == "kidney" else "47135"
                anes, spec = K.ANES_IP[info.get("organ", "kidney")], "transplant"
            else:
                cpt = "27447" if info.get("site") == "knee" else "27130"
                anes, spec = K.ANES_IP["joint_" + info.get("site", "knee")], "ortho"
            surg = self.specialist(p, spec)
            out.append(self.comp("P", surg, [self.fee_line(surg, cpt, 1, y)], d1, kind, pos="21", dx1=dx1))
            if anes:
                agrp = D.hospital_group("anesthesia", fac)
                minutes = int({"00567": 300, "00796": 480, "00868": 240, "00541": 210, "00630": 220,
                               "00210": 260}.get(anes, 140) * (0.8 + 0.4 * r.random()))
                out.append(self.comp("P", agrp, [self.anes_line(agrp, anes, minutes, y, "AA")], d1, kind, pos="21", dx1=dx1))
        if kind == "admit_cardiac" and dx1.startswith("I21"):
            card = self.specialist(p, "cardiology")
            out.append(self.comp("P", card, [self.fee_line(card, "93458", 1, y, mod="26") if "93458" in K.PROF26 else
                                             self.fee_line(card, "93458", 1, y), self.fee_line(card, "92928", 1, y)],
                                 d1, kind, pos="21", dx1=dx1))
        return tuple(out)

    def k_admit(self, p, d0, d1, fac_amt, info, age, y):
        return self._inpatient(p, d0, d1, fac_amt, info, age, y, "admit")

    def k_admit_trauma(self, p, d0, d1, fac_amt, info, age, y):
        return self._inpatient(p, d0, d1, fac_amt, info, age, y, "admit_trauma")

    def k_admit_cardiac(self, p, d0, d1, fac_amt, info, age, y):
        return self._inpatient(p, d0, d1, fac_amt, info, age, y, "admit_cardiac")

    def k_admit_surgery(self, p, d0, d1, fac_amt, info, age, y):
        return self._inpatient(p, d0, d1, fac_amt, info, age, y, "admit_surgery")

    def k_joint(self, p, d0, d1, fac_amt, info, age, y):
        return self._inpatient(p, d0, d1, fac_amt, info, age, y, "joint")

    def k_transplant(self, p, d0, d1, fac_amt, info, age, y):
        return self._inpatient(p, d0, d1, fac_amt, dict(info, icu=True), age, y, "transplant")

    def k_postacute_facility(self, p, d0, d1, fac_amt, info, age, y):
        r, D = self.r, self.D
        days = max(1, (d1 - d0).days)
        irf = info.get("irf", False)
        fac = D.pick(D.by_spec["irf" if irf else "snf"], u01("pac", p.fid))
        room = [("0128" if irf else "0191", days)]
        lines = self.case_rate(fac, y, fac_amt, room, [("0420", "", 0.25), ("0430", "", 0.15), ("0250", "", 0.12),
                                                       ("0300", "", 0.04)] + ([("0440", "", 0.08)] if irf else []))
        dx1 = info.get("dx")
        dx1 = {"I63.9": "I69.351", "S72.001A": "S72.001D", "S82.201A": "S82.201D", "S06.5X0A": "S06.5X0D",
               "S32.009A": "S32.009D", "S27.0XXA": "S27.0XXD"}.get(dx1, "Z48.812" if dx1.startswith("I") else
                                                                   "Z47.89" if dx1.startswith(("M", "S")) else dx1)
        out = [self.comp("I", fac, lines, d1, "postacute_facility", bt="111" if irf else "211", dx1=dx1)]
        doc = self.specialist(p, "pmr") if irf else self.D.hospital_group("hospitalist", D.hosp["regional"])
        visits = max(1, days // 4)
        pl = [self.fee_line(doc, "99223" if irf else "99304", 1, y),
              self.fee_line(doc, "99232" if irf else "99308", visits, y)]
        out.append(self.comp("P", doc, pl, d1, "postacute_facility", pos="61" if irf else "31", dx1=dx1))
        return tuple(out)

    def k_delivery(self, p, d0, d1, fac_amt, info, age, y):
        r, D = self.r, self.D
        cs = info.get("csec")
        los = max(1, (d1 - d0).days)
        fac = self.hospital_for(p, "delivery", info, age)
        lines = self.case_rate(fac, y, fac_amt, [("0112", los)],
                               [("0720", "", 0.0), ("0250", "", 0.12), ("0300", "", 0.07), ("0370", "", 0.06),
                                ("0270", "", 0.04)] + ([("0360", "", 0.18)] if cs else []))
        dx1 = info.get("dx")
        dx2 = "Z37.0"
        out = [self.comp("I", fac, lines, d1, "delivery", bt="111", dx1=dx1, dx2=dx2)]
        ob = self.specialist(p, "obgyn")
        out.append(self.comp("P", ob, [self.fee_line(ob, "59510" if cs else "59400", 1, y)], d1, "delivery", pos="21",
                             dx1=dx1, dx2=dx2, extra=int(r.integers(20, 50))))
        if cs or r.random() < 0.72:
            agrp = D.hospital_group("anesthesia", fac)
            minutes = int((75 if cs else 360) * (0.7 + 0.6 * r.random()))
            out.append(self.comp("P", agrp, [self.anes_line(agrp, "01961" if cs else "01967", minutes, y, "QK")], d1,
                                 "delivery", pos="21", dx1=dx1))
        return tuple(out)

    def k_newborn(self, p, d0, d1, fac_amt, info, age, y):
        r, D = self.r, self.D
        los = max(1, (d1 - d0).days)
        fac = self.hospital_for(p, "newborn", info, age)
        lines = self.case_rate(fac, y, fac_amt, [("0171", los)], [("0250", "", 0.08), ("0300", "", 0.10), ("0270", "", 0.03)])
        dx1 = info.get("dx")
        dx2 = "P59.9" if r.random() < 0.18 else ""
        out = [self.comp("I", fac, lines, d1, "newborn", bt="111", dx1=dx1, dx2=dx2)]
        ped = self.clinic(p, 0, d0) if r.random() < 0.6 else D.hospital_group("hospitalist", fac)
        pl = [self.fee_line(ped, "99460", 1, y)]
        if los > 2:
            pl.append(self.fee_line(ped, "99462", los - 2, y))
        pl.append(self.fee_line(ped, "99238", 1, y))
        out.append(self.comp("P", ped, pl, d1, "newborn", pos="21", dx1=dx1, dx2=dx2))
        if p.sex == "M" and r.random() < 0.55:
            ob = self.D.sticky("obgyn", p.fid)
            out.append(self.comp("P", ob, [self.fee_line(ob, "54150", 1, y)], d1, "newborn", pos="21", dx1="Z41.2"))
        return tuple(out)

    def k_nicu(self, p, d0, d1, fac_amt, info, age, y):
        r, D = self.r, self.D
        days = max(1, (d1 - d0).days)
        fac = self.hospital_for(p, "nicu", info, age)
        wk = info.get("weeks", 40)
        rev = "0174" if wk < 32 else "0173"
        anc = [("0250", "", 0.10), ("0300", "", 0.09), ("0410", "", 0.08), ("0270", "", 0.03), ("0320", "71045", 0.012)]
        lines = self.case_rate(fac, y, fac_amt, [(rev, days)], anc)
        dx1 = info.get("dx")
        dx2 = info.get("dx2", "")
        if fac.npi == self.hospital_for(p, "delivery", {}, 0).npi:
            # born in this hospital: the birth record is the principal diagnosis of the stay
            dx1, dx2 = ("Z38.01" if info.get("csec") else "Z38.00"), dx1
        out = [self.comp("I", fac, lines, d1, "nicu", bt="111", dx1=dx1, dx2=dx2)]
        neo = self.D.sticky("neonatology", fac.npi)
        crit = min(days - 1, 6 if wk < 30 else 3)
        pl = [self.fee_line(neo, "99468", 1, y)]
        if crit > 0:
            pl.append(self.fee_line(neo, "99469", crit, y))
        rest = days - 1 - crit
        if rest > 0:
            pl.append(self.fee_line(neo, "99478" if wk < 30 else "99480", rest, y))
        out.append(self.comp("P", neo, pl, d1, "nicu", pos="21", dx1=dx1, dx2=dx2))
        rad = D.hospital_group("radiology", fac)
        out.append(self.comp("P", rad, [self.fee_line(rad, "71045", max(1, days // 7), y, mod="26")], d1, "nicu",
                             pos="21", dx1=dx1))
        return tuple(out)

    # services that are billed and denied ------------------------------------
    def denied_service(self, p, d, kind):
        """a claim for a service after coverage ended or one the plan does not cover: (prov, lines, pos, dx)"""
        age = p.age(d)
        y = d.year
        if kind == "after_term":
            prov = self.clinic(p, age, d)
            code = "99213" if self.r.random() < 0.6 else "99214"
            dx = wpick([(x[0], x[1]) for x in gated(K.ACUTE, age, p.sex)], self.r.random())
            return prov, [self.fee_line(prov, code, 1, y)], "11", dx
        proc, spec, dx = [("97810", "acupuncture", "M54.50"), ("15823", "plastic", "H02.831"),
                          ("92310", "optometry", "H52.13"), ("V5261", "audiology", "H90.3"),
                          ("97124", "massage", "M62.830")][h(p.pid, d) % 5]
        prov = self.D.sticky(spec, p.pid)
        base = {"97810": 75, "15823": 1450, "92310": 165, "V5261": 2400, "97124": 70}[proc]
        ch = round(base * prov.charge * CHARGE_INDEX[y], 2)
        return prov, [("", proc, "", 1, cents(ch), None)], "11", dx
