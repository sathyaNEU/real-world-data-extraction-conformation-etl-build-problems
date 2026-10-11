"""The four extracts as the district's warehouse holds them: Ellery's medical claim lines, Quarrystone's PBM claims,
Ellery's eligibility spans and the conversion file Ellery built from Bramwell's records on 1 January 2025.

Every claim component the simulation priced becomes a claim with its own lines; the claim history then carries what
a real one carries: replacement and void claims, denied lines, a resubmission after a denial, claims billed under the
wrong family member and voided, exact duplicate submissions denied as duplicates, services after coverage ended, and
run-out (a claim paid after the cut-off is not in the extract). Payments go out on Ellery's weekly check run. PBM
claims carry return-to-stock and reverse-and-rebill reversals, fill at the members' own pharmacies, by mail and at the
specialty pharmacy, and carry the person code and birth date the PBM held on the day of the fill. None of it changes
what the plan actually allowed for a service that happened."""
import datetime as dt
import math
import zlib
from collections import defaultdict

import numpy as np

import catalog as K
import providers as PV
import world as W

DAY = dt.timedelta(days=1)
CUT = W.PAID_THROUGH
START = W.CONVERSION
SPAN_CODES = {"99221", "99222", "99223", "99231", "99232", "99233", "99238", "99239", "99291", "99468", "99469",
              "99478", "99480", "99460", "99462", "99304", "99308", "99232", "90960", "90961", "90962"}


def h(*parts):
    return zlib.crc32("|".join(str(x) for x in parts).encode())


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


PREVENTIVE_CODES = {"99381", "99382", "99383", "99384", "99385", "99386", "99387", "99391", "99392", "99393", "99394",
                    "99395", "99396", "99397", "90460", "90461", "90471", "90472", "77067", "77063", "96110", "96127",
                    "99173", "88175", "87624", "90656", "90700", "90723", "90677", "90680", "90648", "90744", "90707",
                    "90716", "90710", "90633", "90696", "90715", "90734", "90651", "90620", "90750", "90381"}


def line_mode(kind, ct, plan, idx, proc):
    """how a line shares cost: preventive care and screening are free, PPO office, urgent care and emergency
    facility visits take a copay on their first line, everything else goes to the deductible and coinsurance"""
    if kind == "preventive" or proc in PREVENTIVE_CODES:
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
    name, qty, price, bg, spec, per_fill = K.drug(drug)
    if plan == "HDHP":
        return "ded", 0, None
    rx = W.PLANS["PPO"]["rx"]
    if spec:
        return "pct", 0, rx["S"]
    if bg == "G":
        return "copay", int(rx["G"] * 100), None
    if drug in ("eliquis", "xarelto", "jardiance", "farxiga", "lantus", "basaglar", "humalog") or drug.startswith(
            ("ozempic", "mounjaro", "trulicity")):
        return "copay", int(rx["P"] * 100), None
    return "copay", int(rx["N"] * 100), None


# ------------------------------------------------------------------ assembling the extracts
class Pack:
    def __init__(self, S, seed, protect=()):
        self.S = S
        self.rm = np.random.default_rng(seed + 131)     # claim history mess
        self.rx = np.random.default_rng(seed + 151)     # PBM layout and reversals
        self.cs = CostShare()
        self.D = S.coder.D
        self.PH = PV.Pharmacies()
        self.protect = set(protect)
        self.corrections()

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

    def plan_of(self, p, d):
        return self.fam_state(self.S.fams[p.fid], d)[0]

    # ---------------------------------------------------------------- birth-date corrections and person codes
    def corrections(self):
        """Ellery corrected a handful of birth dates Bramwell had wrong. Where the corrected date changed the order of
        two children, Ellery renumbered their person codes from the correction date, as it numbers dependents by date
        of birth. No member of a stratification list is in these families."""
        S, r = self.S, np.random.default_rng(52367)
        self.old_dob = {}          # pid -> (Bramwell birth date, correction date)
        self.code_hist = {}        # pid -> [(from date, person code)]
        fams = []
        for fam in S.fams:
            mem = [S.people[i] for i in fam.members]
            if any(p.pid in self.protect for p in mem):
                continue
            kids = [p for p in mem if p.rel == "C" and p.legacy and p.code and (p.end is None or p.end >= dt.date(2025, 10, 1))]
            if len(kids) == 2 and len([p for p in mem if p.rel == "C"]) == 2:
                a, b = sorted(kids, key=lambda q: q.dob)
                if a.dob.year // 10 == b.dob.year // 10 and b.dob.year < 2024:
                    fams.append((fam, [a, b]))
        picks = [fams[int(i)] for i in sorted(r.choice(len(fams), size=4, replace=False))]
        for fam, kids in picks:
            a, b = kids[0], kids[1]                       # a is the older child
            # Bramwell had the older child's birth year one digit off, late enough to put the child second
            wrong = None
            for yr in range(b.dob.year, min(2024, a.dob.year - a.dob.year % 10 + 9) + 1):
                if yr != a.dob.year and (yr, a.dob.month, a.dob.day) > (b.dob.year, b.dob.month, b.dob.day):
                    wrong = dt.date(yr, a.dob.month, min(a.dob.day, 28))
                    break
            if wrong is None:
                continue
            fix = dt.date(2025, int(r.integers(3, 10)), int(r.integers(1, 28)))
            self.old_dob[a.pid] = (wrong, fix)
            self.code_hist[a.pid] = [(START, b.code), (fix, a.code)]
            self.code_hist[b.pid] = [(START, a.code), (fix, b.code)]
        adults = [p for p in S.people if p.legacy and p.rel in ("E", "S") and p.pid not in self.protect
                  and (p.end is None or p.end >= dt.date(2026, 1, 1)) and S.fams[p.fid] not in [x[0] for x in picks]]
        for i in sorted(r.choice(len(adults), size=3, replace=False)):
            p = adults[int(i)]
            if p.dob.day <= 12 and p.dob.day != p.dob.month:
                wrong = dt.date(p.dob.year, p.dob.day, p.dob.month)
            else:
                wrong = dt.date(p.dob.year - 1, p.dob.month, min(p.dob.day, 28))
            self.old_dob[p.pid] = (wrong, dt.date(2025, int(r.integers(2, 12)), int(r.integers(1, 28))))

    def code_on(self, p, d):
        code = p.code
        for eff, c in self.code_hist.get(p.pid, ()):
            if eff <= d:
                code = c
        return code

    def dob_on(self, p, d):
        x = self.old_dob.get(p.pid)
        return x[0] if x and d < x[1] else p.dob

    # ---------------------------------------------------------------- true claims and fills, cost-shared
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
                ct, npi, amt, lag, rlag, lines, bt, pos, dx1, dx2 = comp
                span = ct == "I" or any(l[1] in SPAN_CODES for l in lines) or ev[4] == "dialysis"
                d1c = ev[2] if span else ev[1]
                med.append({"pid": p.pid, "d0": ev[1], "d1": d1c, "end": ev[2], "ct": ct, "bt": bt, "pos": pos,
                            "dx1": dx1, "dx2": dx2 if dx2 != dx1 else "", "npi": npi, "kind": ev[4],
                            "lines": [[l[0], l[1], l[2], l[3], l[4], l[5], 0, 0, 0, ""] for l in lines],
                            "paid": ev[2] + dt.timedelta(days=lag), "recv": ev[2] + dt.timedelta(days=rlag),
                            "key": (p.pid, ev[1].isoformat(), ev[4], ci), "clean": True})
        items = [(c["pid"], c["d0"], 0, i) for i, c in enumerate(med)] + [(ev[0], ev[1], 1, i) for i, ev in enumerate(fills)]
        items.sort()
        fill_cs = [None] * len(fills)
        for pid, d, typ, i in items:
            p = S.people[pid]
            plan = self.plan_of(p, d)
            if typ == 0:
                c = med[i]
                for k, ln in enumerate(c["lines"]):
                    if ln[5] is None:
                        continue
                    mode, cop = line_mode(c["kind"], c["ct"], plan, k, ln[1])
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
        """every adjudicated claim version: dicts with pid, freq, ref (index of the version it acts on), recv, paid,
        lines, status. Versions paid after the cut-off are dropped at the end."""
        S, r = self.S, self.rm
        V = []

        def emit(c, pid, freq, recv, paid, lines, ref=None, denial=None):
            V.append({"pid": pid, "freq": freq, "ref": ref, "recv": recv, "paid": paid, "lines": lines, "denial": denial,
                      "d0": c["d0"], "d1": c["d1"], "ct": c["ct"], "bt": c["bt"], "pos": c["pos"],
                      "dx1": c["dx1"], "dx2": c["dx2"], "npi": c["npi"]})
            return len(V) - 1

        fam_members = defaultdict(list)
        for p in S.people:
            if p.member_id is not None:
                fam_members[p.fid].append(p)
        seen = set()
        for c in self.med:
            p = S.people[c["pid"]]
            lines = [list(l) for l in c["lines"]]
            # a second read of the same film by the same group on the same day is billed as a repeat procedure
            sig = (c["pid"], c["d0"], c["npi"], tuple(l[1] for l in lines))
            if c["ct"] == "P" and sig in seen and all(l[1][:1] == "7" for l in lines):
                lines = [l[:2] + ["76"] + l[3:] for l in lines]
            seen.add(sig)
            n0 = len(V)
            self._claim_mess(c, p, lines, r, V, emit, fam_members)
            c["clean"] = len(V) == n0 + 1 and V[n0]["freq"] == "1" and V[n0]["denial"] is None and V[n0]["paid"] <= CUT \
                and all(l[9] == "" for l in V[n0]["lines"])
        self._extra_denials(r, emit)
        self.versions = V

    def later(self, d, lo, hi):
        """a provider's next submission, lo to hi days after d, and the check run that settles it"""
        recv = W.receipt_day(d + dt.timedelta(days=int(self.rm.integers(lo, hi))), self.rm.random())
        return recv, W.next_check_run(recv + dt.timedelta(days=int(self.rm.integers(1, 8))))

    def _claim_mess(self, c, p, lines, r, V, emit, fam_members):
        """one claim's history: resubmission after a denial, a claim billed under the wrong family member and
        voided, a replacement, a bundled line denied, an exact duplicate denied"""
        u = r.random()
        inpatient = c["bt"].startswith("11")
        recv, paid = c["recv"], c["paid"]
        denied = lambda ls: [l[:5] + [None, None, None, None, ""] for l in ls]
        # a claim denied for missing information and paid on resubmission
        if c["ct"] == "P" and u < 0.008:
            emit(c, c["pid"], "1", recv, paid, denied(lines), denial="16")
            recv, paid = self.later(paid, 7, 40)
            emit(c, c["pid"], "1", recv, paid, lines)
            return
        # billed first under another member of the family, voided, then billed correctly
        if c["ct"] == "P" and p.rel != "E" and u < 0.012:
            others = [q for q in fam_members[p.fid] if q.pid != p.pid and q.covered_on(c["d0"]) and q.sex == p.sex
                      and (q.age(c["d0"]) < 18) == (p.age(c["d0"]) < 18)]
            if others:
                q = others[h(p.pid, c["d0"]) % len(others)]
                w = emit(c, q.pid, "1", recv, paid, lines)
                vrecv, vpaid = self.later(paid, 15, 55)
                emit(c, q.pid, "8", vrecv, vpaid, [l[:4] + [-x for x in l[4:9]] + [""] for l in lines], ref=w)
                rrecv, rpaid = self.later(vrecv, 0, 7)
                emit(c, c["pid"], "1", rrecv, rpaid, lines)
                return
        # replacement claims: late charges on inpatient bills, corrected units or codes elsewhere; and on a few 2025
        # claims a provider's appeal or a rate correction settled a year or more after the first payment
        rep_p = 0.22 if inpatient else 0.05 if c["ct"] == "I" else 0.015
        late = c["d0"].year == 2025 and r.random() < (0.014 if c["ct"] == "I" else 0.003)
        if late or r.random() < rep_p:
            orig = self.wrong_version(c, lines, r)
            o = emit(c, c["pid"], "1", recv, paid, orig)
            rrecv, rpaid = self.later(paid, 20, 100)
            hi = (CUT - paid).days - 25
            settled_late = False
            if late and hi > 300:
                lrecv, lpaid = self.later(paid, 300, min(640, hi))
                if lpaid <= CUT:
                    rrecv, rpaid = lrecv, lpaid
                    settled_late = True
            if not settled_late and r.random() < 0.08:
                mid = self.wrong_version(c, lines, r)
                o = emit(c, c["pid"], "7", rrecv, rpaid, mid, ref=o)
                rrecv, rpaid = self.later(rpaid, 25, 70)
            emit(c, c["pid"], "7", rrecv, rpaid, lines, ref=o)
            last_recv, last_paid = rrecv, rpaid
        else:
            o = emit(c, c["pid"], "1", recv, paid, lines)
            # bundled line denied on a paid claim
            if c["ct"] == "P" and c["kind"] in ("lab", "office", "office_spec") and r.random() < 0.06:
                prov_npi = c["npi"]
                extra = "36415" if c["kind"] == "lab" else "99211"
                if not any(l[1] == extra for l in lines):
                    base = K.FEE[extra]
                    V[o]["lines"] = lines + [["", extra, "", 1, int(round(base * 2.2 * 100)), None, None, None, None, "97"]]
            last_recv, last_paid = recv, paid
        # the same claim submitted again: Ellery denies an exact duplicate
        if r.random() < (0.016 if c["ct"] == "P" else 0.008):
            drecv, dpaid = self.later(recv, 3, 30)
            emit(c, c["pid"], "1", drecv, dpaid, denied(lines), denial="18")

    def _extra_denials(self, r, emit):
        """services after coverage ended, and services the plan does not cover"""
        S = self.S
        coder = S.coder
        for p in S.people:
            if p.member_id is None:
                continue
            ends = [e for s0, e in p.spans() if e is not None and START <= e <= CUT - dt.timedelta(days=40)
                    and not (p.death is not None and e == p.death)]
            for end in ends:
                if r.random() >= 0.25:
                    continue
                for _ in range(int(r.integers(1, 3))):
                    d = W.next_business_day(end + dt.timedelta(days=int(r.integers(3, 41))))
                    if p.covered_on(d) or (p.death is not None and d > p.death):
                        continue
                    prov, ls, pos, dx = coder.denied_service(p, d, "after_term")
                    c = {"d0": d, "d1": d, "ct": "P", "bt": "", "pos": pos, "dx1": dx, "dx2": "", "npi": prov.npi}
                    recv = W.receipt_day(d + dt.timedelta(days=int(r.integers(4, 30))), r.random())
                    emit(c, p.pid, "1", recv, W.next_check_run(recv + DAY),
                         [[l[0], l[1], l[2], l[3], l[4], None, None, None, None, ""] for l in ls], denial="27")
            if p.covered_on(dt.date(2026, 1, 1)) and r.random() < 0.012:
                d = W.next_business_day(dt.date(2025, 3, 1) + dt.timedelta(days=int(r.integers(0, 640))))
                if p.covered_on(d) and p.age(d) >= 18:
                    prov, ls, pos, dx = coder.denied_service(p, d, "not_covered")
                    c = {"d0": d, "d1": d, "ct": "P", "bt": "", "pos": pos, "dx1": dx, "dx2": "", "npi": prov.npi}
                    recv = W.receipt_day(d + dt.timedelta(days=int(r.integers(6, 35))), r.random())
                    emit(c, p.pid, "1", recv, W.next_check_run(recv + DAY),
                         [[l[0], l[1], l[2], l[3], l[4], None, None, None, None, ""] for l in ls], denial="204")

    def wrong_version(self, c, lines, r):
        """the version a replacement corrects: an inpatient bill without its late charges, or a first line priced on
        the wrong units"""
        out = [list(l) for l in lines]
        if c["ct"] == "I" and len(out) > 2:
            return out[:-int(r.integers(1, 3))]
        l = out[0]
        if l[3] > 1:
            f = 0.5 if r.random() < 0.5 else 1.5
            nu = max(1, int(round(l[3] * f)))
        else:
            nu = 2
        f = nu / l[3]
        l[3] = nu
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
    def pharmacy_for(self, p, drug, ds, d, r):
        PH = self.PH
        if K.is_specialty(drug):
            return PH.specialty
        if ds >= 84 and K.DRUGS[drug][3] == "G" and PV.u01("mail", p.fid) < 0.32:
            return PH.mail
        a = p.age(d)
        if p.rel == "C" and 18 <= a <= 24 and PV.u01("college", p.pid) < 0.45 and d.month in (1, 2, 3, 4, 9, 10, 11, 12):
            return PH.travel[PV.h("campus", p.pid) % len(PH.travel)]
        u = r.random()
        if u < 0.035:
            return PH.travel[int(r.integers(0, len(PH.travel)))]
        if u < 0.12:
            return PH.second(p.fid, int(r.integers(0, 2)))
        return PH.home(p.fid)

    def ndc_for(self, drug, ph, d):
        ndcs = K.DRUGS[drug][6]
        q = (d.year * 4 + (d.month - 1) // 3) // 2           # a pharmacy changes supplier now and then
        return ndcs[PV.h("ndc", drug, ph, q) % len(ndcs)]

    def pharmacy_rows(self):
        S, r = self.S, self.rx
        rxno = {}
        out = []
        self.rx_clean = set()
        for i, ev in enumerate(self.fills):
            pid, d0 = ev[0], ev[1]
            p = S.people[pid]
            info = ev[6]
            drug = info["drug"]
            name, qty, price, bg, spec, per_fill = K.drug(drug)
            ph = self.pharmacy_for(p, drug, info["days"], d0, r)
            key = (pid, drug, ph)
            st = rxno.get(key)
            acute = per_fill and not spec and bg == "G" and drug not in ("albuterol", "fluticasone_hfa", "budesonide_formoterol",
                                                                          "fluticasone_nasal")
            if st is None or acute or st[1] >= 11 or (d0 - st[2]).days > 365:
                st = [int(r.integers(1000000, 9999999)) if not spec else int(r.integers(30000000, 39999999)), -1, d0]
            st[1] += 1
            rxno[key] = st
            gross = int(round(ev[5][0][2] * 100))
            fee = 0 if spec else (int(r.integers(110, 176)) if bg == "G" else int(r.integers(70, 101)))
            fee = min(fee, gross // 2)
            pay = self.fill_cs[i]
            base = {"pid": pid, "rx": st[0], "fill": st[1], "dos": d0, "ph": ph, "drug": drug, "qty": info["qty"],
                    "days": info["days"], "ingr": gross - fee, "fee": fee, "pat": pay, "ndc": self.ndc_for(drug, ph, d0),
                    "daw": "1" if (bg == "B" and r.random() < 0.03) else "0"}
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
                if early >= START and p.covered_on(early):
                    rts = dict(base)
                    rts["dos"] = early
                    out.append(("B1", rts, early))
                    rev = early + dt.timedelta(days=int(r.integers(10, 15)))
                    if rev <= CUT:
                        out.append(("B2", rts, rev))
                out.append(("B1", base, d0))
            else:
                out.append(("B1", base, d0))
                self.rx_clean.add(i)
        self.rx_out = out

    # ---------------------------------------------------------------- writers
    def medical_rows(self):
        S = self.S
        keep = [v for v in self.versions if v["paid"] <= CUT]
        idx = {id(v): i for i, v in enumerate(self.versions)}
        order = sorted(range(len(keep)), key=lambda i: (keep[i]["recv"], keep[i]["paid"], keep[i]["pid"], i))
        seq = defaultdict(int)
        number = {}
        r = self.rm
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
            name, qty, price, bg, spec, per_fill = K.drug(b["drug"])
            sg = -1 if txn == "B2" else 1
            gross = b["ingr"] + b["fee"]
            pat = min(b["pat"], gross)
            vals = [b["ingr"] * sg, b["fee"] * sg, gross * sg, pat * sg, (gross - pat) * sg]
            q = b["qty"]
            qtxt = ("%.1f" % q).rstrip("0").rstrip(".") if isinstance(q, float) else str(q)
            fam = S.fams[p.fid]
            rel = "1" if p.rel in ("E", "R") else "2" if p.rel == "S" else "3"
            npi, ncpdp = self.PH.rows[b["ph"]][0], self.PH.rows[b["ph"]][1]
            rows.append([num, txn, "%07d" % b["rx"] if b["rx"] < 10000000 else "%08d" % b["rx"], "%02d" % b["fill"],
                         b["dos"].strftime("%Y%m%d"), proc.strftime("%Y%m%d"), "%09d" % int(fam.emp), self.code_on(p, b["dos"]),
                         self.dob_on(p, b["dos"]).strftime("%Y%m%d"), "2" if p.sex == "F" else "1", rel, npi, ncpdp,
                         b["ndc"], name, bg, b["daw"], qtxt, str(b["days"])] + ["%.2f" % (x / 100) for x in vals])
        return rows

    def spans(self, p):
        """coverage spans with the current administrator, as of the extract (inclusive dates; blank end = open): one
        row for each stretch of coverage, split where the plan, tier, class or person code changes"""
        fam = self.S.fams[p.fid]
        out = []
        for a0, b in p.spans():
            a = max(a0, START)
            if a > CUT or (b is not None and b < a):
                continue
            changes = {eff for eff, _, _ in fam.hist if a < eff} | {eff for eff, _ in fam.cls_hist if a < eff} | \
                {eff for eff, _ in self.code_hist.get(p.pid, ()) if a < eff}
            cuts = [a] + sorted(c for c in changes if (b is None or c <= b) and c <= CUT)
            seg = []
            for i, s in enumerate(cuts):
                e = cuts[i + 1] - DAY if i + 1 < len(cuts) else b
                if e is not None and e > CUT:
                    e = None
                plan, tier, cls = self.fam_state(fam, s)
                code = self.code_on(p, s)
                if seg and seg[-1][2:] == (plan, tier, cls, code):
                    seg[-1] = (seg[-1][0], e, plan, tier, cls, code)
                else:
                    seg.append((s, e, plan, tier, cls, code))
            out += seg
        return out

    def eligibility_rows(self):
        S = self.S
        cls_code = {"T": "TCH", "S": "ESP", "A": "ADM", "R": "RET", "C": "COB"}
        rel_code = {"E": "SUB", "R": "SUB", "S": "SPS", "C": "DEP"}
        rows = []
        for p in S.people:
            if p.member_id is None:
                continue
            fam = S.fams[p.fid]
            for s, e, plan, tier, cls, code in self.spans(p):
                rows.append([p.member_id, fam.emp, code, rel_code[p.rel], p.dob.isoformat(), p.sex, cls_code[cls], tier,
                             W.PLAN_CODE[plan], s.isoformat(), e.isoformat() if e else ""])
        rows.sort(key=lambda x: (x[0], x[9]))
        return rows

    def crosswalk_rows(self, avoid):
        """Ellery's conversion file: one row per Bramwell member record converted on 1 January 2025. A handful of
        members had two Bramwell records (re-enrolled under a second subscriber number); both map to one member. The
        birth date and person code are as Ellery converted them from Bramwell's file."""
        S, r = self.S, self.rm
        conv = [p for p in S.people if p.legacy is not None]
        cost24 = defaultdict(float)
        for ev in S.events:
            if ev[1].year == 2024:
                cost24[ev[0]] += sum(c[2] for c in ev[5])
        pool = [p for p in conv if p.pid not in avoid and cost24[p.pid] < 1500 and p.rel != "E" and p.pid not in self.old_dob]
        dups = []
        for i in sorted(r.choice(len(pool), size=9, replace=False)):
            dups.append(pool[int(i)])
        rel_code = {"E": "SUB", "R": "SUB", "S": "SPS", "C": "DEP"}
        rows = []
        for p in conv:
            fam = S.fams[p.fid]
            root, suf = p.legacy.split("-")
            rows.append([root, suf, p.member_id, fam.emp, self.code_on(p, START), rel_code[p.rel],
                         self.dob_on(p, START).strftime("%m/%d/%Y"), ""])
        for p in dups:
            fam = S.fams[p.fid]
            root2 = "%08d" % int(r.integers(60100000, 64990000))
            p.legacy2 = root2 + "-" + ("02" if p.rel == "S" else "03")
            rows.append([root2, p.legacy2.split("-")[1], p.member_id, fam.emp, self.code_on(p, START), rel_code[p.rel],
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
