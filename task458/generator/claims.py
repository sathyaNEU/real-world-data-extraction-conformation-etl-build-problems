"""The plan's behavioral-health claims and encounters for services in the contract year.

A member with a serious mental illness has no service carrying it before the enrolled month members.py assigns as the
first (none at all when it assigns none); in that month at least one, and each enrolled month after it prescriber visits
at the county's access rate and other services carrying the diagnosis (case management, therapy, primary care, emergency
care) at the rest of a rate that is the same in every county. A member with an opioid use disorder has, from the same
kind of first month, medication visits, opioid treatment program months, counseling and emergency care; other members
with a behavioral-health condition have therapy, medication management and primary care. Behavioral health agencies and
opioid treatment programs report sub-capitated encounters (no payment on the record); community health centers,
emergency physician groups, psychiatric practices and the telepsychiatry group bill fee-for-service claims, each line
allowed the lesser of its billed charge and the fee schedule's amount for its units, the claim's paid amount repeating on
each of its lines. A few claims are replaced by the provider (sometimes twice) and a few duplicates are voided."""
import datetime as dt

import numpy as np

import members as M
import providers as PV
import world as W

D = dt.date
DAY = dt.timedelta(days=1)

E_AND_M = [("99213", 6), ("99214", 10), ("99215", 2)]
PSYCH_EVAL = "90792"
ADDON = "90833"
VISIT_CODES = {"99202", "99203", "99204", "99205", "99211", "99212", "99213", "99214", "99215", "90791", "90792"}
TELE_SHARE = {"Douglas": 0.30, "Okanogan": 0.30, "Adams": 0.14, "Franklin": 0.10, "Grant": 0.10, "Kittitas": 0.08,
              "Walla Walla": 0.10, "Chelan": 0.06, "Benton": 0.05, "Yakima": 0.06}
OTP_OF = {"Yakima": "Yakima", "Benton": "Benton", "Franklin": "Benton", "Grant": "Grant", "Adams": "Grant",
          "Chelan": "Chelan", "Douglas": "Chelan", "Kittitas": "Yakima", "Okanogan": "Okanogan",
          "Walla Walla": "Walla Walla"}
ED_OF = {"Adams": "Grant", "Douglas": "Chelan", "Kittitas": "Yakima", "Okanogan": "Chelan"}
OTHER_BH_SHARE = 0.20      # members without either condition who have another behavioral-health condition
OTHER_BH_RATE = 0.24       # their monthly service rate
OPIOID_UNSPEC = 0.012      # members without an opioid use disorder whose records carry F11.90 (opioid use, unspecified)


def fee(code, day):
    base = W.FEE[code]
    if day >= D(2026, 1, 1) and code in VISIT_CODES | {ADDON, "90832", "90834", "90837"}:
        base = round(base * 1.04, 2)
    return base


def _pick(r, weighted):
    items = [x for x, _ in weighted]
    w = np.array([x for _, x in weighted], dtype=float)
    return items[int(r.choice(len(items), p=w / w.sum()))]


def _nodot(code):
    return code.replace(".", "")


class Book:
    """Who renders and who bills, by county."""

    def __init__(self, clins, orgs, r):
        self.r = r
        self.org = {}
        for o in orgs:
            self.org.setdefault((o["county"], o["kind"]), []).append(o)
        self.pres, self.ther, self.pcp, self.ed, self.sec = {}, {}, {}, {}, {}
        self.tele = []
        self.employer = {}
        for c in clins:
            k = c["kind"]
            home = c["county"]
            if k in ("prescriber", "react", "deact_late_before", "deact_late_after", "mover", "switch"):
                self.pres.setdefault(home, []).append(c)
            elif k == "tele":
                self.tele.append(c)
            elif k == "therapist":
                self.ther.setdefault(home, []).append(c)
            elif k == "pcp":
                self.pcp.setdefault(home, []).append(c)
            elif k == "ed":
                self.ed.setdefault(home, []).append(c)
            elif k == "secondary":
                self.sec.setdefault(home, []).append(c)
        tele_org = self.org[(None, "tele")][0]
        for county, lst in sorted(self.pres.items()):
            for c in lst:
                has_psy = (county, "psy") in self.org
                u = r.random()
                if u < 0.55 or not has_psy and u < 0.75:
                    self.employer[c["npi"]] = ("SUBCAP", self.org[(county, "bha")][0])
                elif has_psy:
                    self.employer[c["npi"]] = ("FFS", self.org[(county, "psy")][0])
                else:
                    self.employer[c["npi"]] = ("FFS", None)          # solo practice, bills under its own NPI
        for c in self.tele:
            self.employer[c["npi"]] = ("FFS", tele_org)
        for county, lst in self.ther.items():
            for c in lst:
                self.employer[c["npi"]] = ("SUBCAP", self.org[(county, "bha")][0])
        for county, lst in list(self.pcp.items()) + list(self.sec.items()):
            chc = self.org.get((county, "chc")) or self.org[(ED_OF.get(county, county), "chc")]
            for c in lst:
                self.employer[c["npi"]] = ("FFS", chc[0])
        for county, lst in self.ed.items():
            edg = self.org.get((county, "edg")) or self.org[(ED_OF.get(county, county), "edg")]
            for c in lst:
                self.employer[c["npi"]] = ("FFS", edg[0])

    def renders_on(self, c, day):
        """A prescriber renders while practising in the ten counties and while the NPI is active."""
        if c["kind"] == "react" and day >= c["deactivated"]:
            return False
        return True

    def prescriber(self, county, day, avoid=None):
        lst = [c for c in self.pres.get(county, []) if self.renders_on(c, day) and c is not avoid]
        return lst[int(self.r.integers(len(lst)))]


def _month_days(y, m):
    first = D(y, m, 1)
    last = D(y + (m == 12), m % 12 + 1, 1) - DAY
    return first, last


def month_map(p):
    """month -> (county, member_id) for each contract-year month the person was enrolled (a regular spell wins over a
    retroactive row covering the same month)."""
    out = {}
    for s in sorted(p.spells, key=lambda s: (s["source"] != "RETRO", s["start"])):
        a = max(s["start"], W.WINDOW_START)
        b = min(s["end"] or W.WINDOW_END, W.WINDOW_END)
        for ym in W.months_of(a, b):
            out[ym] = (s["county"], s["member_id"])
    return dict(sorted(out.items()))


def build(persons, clins, orgs):
    """Every claim and encounter line, and each person's true service history for the checks."""
    r = np.random.default_rng([W.SEED, 20])
    bk = Book(clins, orgs, r)
    lines = []
    icn_seq = [0]
    truth = {}

    def icn(received):
        icn_seq[0] += 1
        return "%02d%03d%08d" % (received.year % 100, received.timetuple().tm_yday, 40_000_000 + icn_seq[0] * 7 % 9_999_991)

    other_dx = [(c, w) for c, w in W.OTHER_BH if c != "F11.90"]
    for p in persons:
        mm = month_map(p)
        if not mm:
            continue
        other = (not p.smi and not p.oud and r.random() < OTHER_BH_SHARE)
        unspec = (not p.oud and r.random() < OPIOID_UNSPEC)
        smi_code = _pick(r, W.SMI_COMMON)
        oud_code = _pick(r, W.OUD_COMMON)
        oth_code = _pick(r, other_dx)
        assigned = {}
        seen_first = set()
        t = {"smi_events": 0, "oud_events": 0, "seen": False, "months": len(mm)}
        f_smi, f_oud = p.first["SMI"], p.first["OUD"]
        for i, ((y, m), (county, mid)) in enumerate(mm.items(), start=1):
            first, last = _month_days(y, m)
            acc = W.COUNTIES[county]["access"]
            eng = p.engage
            events = []
            if f_smi is not None and i >= f_smi:
                k = int(r.poisson(W.LAM_SMI * eng)) if i > f_smi else 1 + int(r.poisson(0.5 * W.LAM_SMI * eng))
                events += ["pvisit" if r.random() < acc / W.LAM_SMI else "smi_other" for _ in range(k)]
            if f_oud is not None and i >= f_oud:
                k = int(r.poisson(W.LAM_OUD * eng)) if i > f_oud else 1 + int(r.poisson(0.5 * W.LAM_OUD * eng))
                events += ["oud"] * k
            if other:
                events += ["other"] * int(r.poisson(OTHER_BH_RATE * eng))
            if unspec and r.random() < 0.18:
                events.append("unspec")
            smi_on = f_smi is not None and i >= f_smi
            for ev in events:
                day = first + dt.timedelta(days=int(r.integers(0, (last - first).days + 1)))
                claim = _service(r, bk, p, county, ev, day, assigned, seen_first, smi_code, oud_code, oth_code, smi_on)
                if claim is None:
                    continue
                claim["member_id"] = mid
                claim["person"] = p.pid
                lines_c = _emit(r, claim, icn)
                lines.extend(lines_c)
                if ev in ("pvisit", "smi_other"):
                    t["smi_events"] += 1
                if ev == "oud":
                    t["oud_events"] += 1
        truth[p.pid] = t
    _adjust(r, lines, icn)
    lines.sort(key=lambda x: (x["paid_date"], x["icn"], x["line"]))
    return lines, bk


def _service(r, bk, p, county, ev, day, assigned, seen_first, smi_code, oud_code, oth_code, smi_on=False):
    """One service: the rendering clinician, the billing provider, the arrangement, the place, the lines, the codes."""
    tele = False
    # a prescriber records a patient's serious mental illness, so a member who has one sees a prescriber for an opioid
    # use disorder only from the month a service first carries the illness
    if ev == "pvisit" or ev == "oud" and (smi_on or not p.smi) and r.random() < 0.35 or ev == "other" and r.random() < 0.30:
        kind = "pvisit"
        key = (county, ev == "pvisit")
        pres = assigned.get(key)
        if pres is None or not bk.renders_on(pres, day):
            pres = bk.tele[int(r.integers(len(bk.tele)))] if r.random() < TELE_SHARE[county] else bk.prescriber(county, day)
            assigned[key] = pres
        arr, org = bk.employer[pres["npi"]]
        tele = pres["kind"] == "tele" or r.random() < 0.08
        if pres["npi"] not in seen_first and r.random() < 0.5:
            procs = [(PSYCH_EVAL, 1)]
        else:
            procs = [(_pick(r, E_AND_M), 1)]
            if r.random() < 0.30:
                procs.append((ADDON, 1))
        seen_first.add(pres["npi"])
        dx = {"pvisit": smi_code, "oud": oud_code, "other": oth_code}[ev]
        dxs = [dx] + ([_pick(r, W.OTHER_BH)] if r.random() < 0.25 else [])
        if ev == "pvisit" and r.random() < 0.03:
            dxs = [_pick(r, W.OTHER_BH), smi_code]
        if smi_on and smi_code not in dxs:
            dxs = dxs[:1] + [smi_code] + dxs[1:]          # a prescriber records a patient's serious mental illness
        pos = ("10" if r.random() < 0.6 else "02") if tele else ("53" if arr == "SUBCAP" else "11")
        return {"render": pres["npi"], "bill": org["npi"] if org else pres["npi"], "arr": arr, "pos": pos,
                "procs": procs, "dx": dxs, "day": day, "mod": "95" if tele else ""}
    if ev == "smi_other" or ev == "oud" or ev == "other" or ev == "unspec":
        dx = {"smi_other": smi_code, "oud": oud_code, "other": oth_code, "unspec": "F11.90"}[ev]
        u = r.random()
        if ev == "unspec":
            u = 0.80 + 0.2 * r.random()
        if ev == "oud" and u < 0.35:
            otp_c = OTP_OF[county]
            otp = bk.org[(otp_c, "otp")][0]
            first, last = _month_days(day.year, day.month)
            return {"render": "", "bill": otp["npi"], "arr": "SUBCAP", "pos": "57", "procs": [("H0020", int(r.integers(8, 31)))],
                    "dx": [dx], "day": first, "thru": last}
        if u < 0.45:
            bha = bk.org[(county, "bha")][0]
            ther = bk.ther[county][int(r.integers(len(bk.ther[county])))]
            if ev == "oud":
                code = _pick(r, [("H0004", 3), ("H0005", 2)])
                return {"render": ther["npi"], "bill": bha["npi"], "arr": "SUBCAP", "pos": "57", "procs": [(code, int(r.integers(1, 5)))],
                        "dx": [dx], "day": day}
            if r.random() < 0.5:
                code = _pick(r, [("H0036", 4), ("H0039", 2), ("H2015", 2), ("T1017", 1)])
                rend = "" if r.random() < 0.5 else ther["npi"]
                return {"render": rend, "bill": bha["npi"], "arr": "SUBCAP", "pos": "53", "procs": [(code, int(r.integers(1, 9)))],
                        "dx": [dx], "day": day}
            code = _pick(r, [("90834", 4), ("90837", 3), ("90832", 2), ("90847", 1)])
            return {"render": ther["npi"], "bill": bha["npi"], "arr": "SUBCAP", "pos": "53", "procs": [(code, 1)],
                    "dx": [dx], "day": day}
        if u < 0.80:
            pool = bk.pcp[county] + bk.sec.get(county, [])
            pcp = pool[int(r.integers(len(pool)))]
            arr, org = bk.employer[pcp["npi"]]
            gen = _pick(r, W.GENERAL)
            dxs = [gen, dx] if r.random() < 0.7 else [dx, gen]
            return {"render": pcp["npi"], "bill": org["npi"], "arr": "FFS", "pos": "11", "procs": [(_pick(r, [("99213", 5), ("99214", 4)]), 1)],
                    "dx": dxs, "day": day}
        ed_c = ED_OF.get(county, county)
        doc = bk.ed[ed_c][int(r.integers(len(bk.ed[ed_c])))]
        arr, org = bk.employer[doc["npi"]]
        lead = _pick(r, [("R45.851", 1), ("R44.0", 1), ("F43.0", 1), ("T40.2X1A", 1)]) if r.random() < 0.4 else dx
        dxs = [lead] + ([dx] if lead != dx else [])
        return {"render": doc["npi"], "bill": org["npi"], "arr": "FFS", "pos": "23", "procs": [(_pick(r, W.OTHER_PROC["ed"]), 1)],
                "dx": dxs, "day": day}
    return None


CHARGE = {}


def _charge(r, bill, code):
    """A billing provider's charge for a code: its charge master's price, mostly well above the plan's fee; a few
    community and group practices price some codes under it."""
    k = (bill, code)
    if k not in CHARGE:
        if r.random() < 0.09:
            CHARGE[k] = float(round(W.FEE[code] * (0.84 + 0.14 * r.random())))
        else:
            CHARGE[k] = float(round(W.FEE[code] * (1.5 + 0.9 * r.random()) / 5) * 5)
    return CHARGE[k]


def allowed(billed, code, units, day):
    """A fee-for-service line's allowed amount: the lesser of its billed charge and the fee schedule's for its units."""
    return min(billed, round(fee(code, day) * units, 2))


def _emit(r, cl, icn):
    received = cl["day"] + dt.timedelta(days=int(r.integers(3, 40)))
    paid = received + dt.timedelta(days=int(r.integers(7, 60) if cl["arr"] == "FFS" else r.integers(10, 75)))
    num = icn(received)
    out = []
    billed = [float(_charge(r, cl["bill"], code) * units) for code, units in cl["procs"]]
    total = round(sum(allowed(b, code, units, cl["day"]) for b, (code, units) in zip(billed, cl["procs"])), 2)
    for i, (code, units) in enumerate(cl["procs"]):
        dx = [_nodot(x) for x in cl["dx"]][:4] + [""] * (4 - min(4, len(cl["dx"])))
        out.append({"icn": num, "line": i + 1, "freq": "1", "orig": "", "member_id": cl["member_id"], "person": cl["person"],
                    "arr": cl["arr"], "bill": cl["bill"], "render": cl["render"], "pos": cl["pos"], "proc": code,
                    "mod": cl.get("mod", "") if code != "H0020" else "", "units": units, "from": cl["day"],
                    "thru": cl.get("thru", cl["day"]), "dx": dx,
                    "billed": billed[i], "paid": total if cl["arr"] == "FFS" else 0.0,
                    "received": received, "paid_date": paid})
    return out


def _adjust(r, lines, icn):
    """Provider replacements (about 3 per cent of fee-for-service claims, a tenth of them replaced again) and voided
    duplicates (about 1 per cent: the same claim paid twice, the second voided)."""
    claims = {}
    for ln in lines:
        claims.setdefault(ln["icn"], []).append(ln)
    order = sorted(claims)
    extra = []
    for num in order:
        cl = claims[num]
        if cl[0]["arr"] != "FFS":
            continue
        u = r.random()
        if u < 0.03:
            prev = cl
            for k in range(2 if r.random() < 0.10 else 1):
                rec = prev[0]["paid_date"] + dt.timedelta(days=int(r.integers(5, 70)))
                new = icn(rec)
                procs = [(x["proc"], x["units"]) for x in prev]
                if procs[0][0] in ("99213", "99214", "99215"):
                    alt = {"99213": "99214", "99214": "99213" if r.random() < 0.5 else "99215", "99215": "99214"}[procs[0][0]]
                    procs[0] = (alt, 1)
                bills = [float(_charge(r, prev[0]["bill"], c) * u_) for c, u_ in procs]
                total = round(sum(allowed(b, c, u_, prev[0]["from"]) for b, (c, u_) in zip(bills, procs)), 2)
                pd = rec + dt.timedelta(days=int(r.integers(7, 40)))
                if pd > W.PAID_THROUGH:
                    break                    # not yet adjudicated when the extract was run
                rep = []
                for i, (c, u_) in enumerate(procs):
                    x = dict(prev[min(i, len(prev) - 1)])
                    x.update({"icn": new, "line": i + 1, "freq": "7", "orig": prev[0]["icn"], "proc": c, "units": u_,
                              "billed": bills[i], "paid": total, "received": rec, "paid_date": pd})
                    rep.append(x)
                extra.extend(rep)
                prev = rep
        elif u < 0.04:
            rec = cl[0]["received"] + dt.timedelta(days=int(r.integers(1, 20)))
            dup = icn(rec)
            pd = rec + dt.timedelta(days=int(r.integers(7, 30)))
            copy = [dict(x, icn=dup, received=rec, paid_date=pd) for x in cl]
            vrec = pd + dt.timedelta(days=int(r.integers(10, 60)))
            vpaid = vrec + dt.timedelta(days=int(r.integers(5, 20)))
            if vpaid > W.PAID_THROUGH or pd > W.PAID_THROUGH:
                continue                     # the duplicate and its void fall after the extract's run-out
            vnum = icn(vrec)
            void = [dict(x, icn=vnum, freq="8", orig=dup, paid=0.0, received=vrec, paid_date=vpaid) for x in cl]
            extra.extend(copy + void)
    lines.extend(extra)
