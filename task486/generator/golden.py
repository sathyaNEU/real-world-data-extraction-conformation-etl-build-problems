"""The golden and every route on the ladder, computed from the pack as shipped (pack_read), never from the world.

Each retail employer is the company (all its PAYE schemes, by company number) or the person or partnership (by
initials and surname) the extract names; each occupier account at 31 March is matched to it by company number where
the district records one, otherwise by name (registered and previous names) or by initials and surname; an account
is an owner's, the premises empty, when it carries empty property relief or names a letting or development company;
a property company held by the same parent as a retail employer is that employer's. The golden places each
multi-site retail employer's employees at its premises by floor area times the staff per square metre of the
premises' description, measured as the ratio of total staff to total floor area of the single-site retail employers
in that description and March."""
import datetime as dt
import re

import numpy as np

import pack_read as PR

M22, M26 = dt.date(2022, 3, 31), dt.date(2026, 3, 31)
DAY = {"22": M22, "26": M26}
LIST = {"22": "17", "26": "23"}
RETAIL_DESC = ("R1", "R2", "R3", "R4", "O1", "W1")
TH = -0.08
UNIT = 50
OWNER_SIC = {"68209", "41100"}      # letting and operating own real estate; development of building projects


def norm(name):
    s = re.split(r"\s+T/A\s+", (name or "").upper())[0]
    s = s.replace("LIMITED", "LTD")
    s = re.sub(r"[^A-Z0-9& ]", " ", s)
    return " ".join(s.split())


def person_key(name):
    s = re.split(r"\s+[Tt]/[Aa]\s+", name or "")[0].strip()
    if "," in s:
        sur, first = [x.strip() for x in s.split(",", 1)]
        return (first[:1].upper(), sur.upper())
    parts = s.replace("&", " & ").split()
    sur = parts[-1].upper()
    firsts = [p for p in parts[:-1] if p != "&"]
    if "&" in parts:
        return ("&".join(f[0].upper() for f in firsts), sur)
    return (firsts[0][0].upper() if firsts else "", sur)


class Pack:
    def __init__(self, target):
        R = PR.read(target)
        self.__dict__.update(R)
        self.co_by_name = {}
        for num, c in self.companies.items():
            for nm in [c["name"]] + c["prev"]:
                self.co_by_name.setdefault(norm(nm), num)
        self.group = {}
        for num, c in self.companies.items():
            if c["psc"]:
                self.group.setdefault(c["psc"], []).append(num)
        self.employers = {yr: self._employers(yr) for yr in ("22", "26")}
        self.occ = {yr: self._occupancy(yr) for yr in ("22", "26")}

    def _employers(self, yr):
        """employer key -> dict(staff, sic, pcs): companies by number, people by initials and surname"""
        out = {}
        for s in self.paye[yr]:
            if s["crn"]:
                k = ("C", s["crn"])
            elif s["sic"].startswith("47"):
                k = ("P",) + person_key(s["name"])
            else:
                k = ("N", norm(s["name"]))
            E = out.setdefault(k, dict(staff=0, sic=s["sic"], pcs=[], schemes=0))
            E["staff"] += s["n"]
            E["pcs"].append((s["pc"], s["n"]))
            E["schemes"] += 1
        return out

    def occupier(self, a, yr):
        """the employer key an account is liable for in occupation, or None when its premises stood empty"""
        if a["relief"] == "EPR":
            return None
        num = a["crn"] or self.co_by_name.get(norm(a["name"]))
        if num:
            c = self.companies.get(num)
            if c and OWNER_SIC & set(c["sic"]):
                # a letting or development company is an owner, unless its parent also holds a retail employer, whose
                # premises it holds
                for sib in self.group.get(c["psc"], []) if c["psc"] else []:
                    if ("C", sib) in self.employers[yr] and self.employers[yr][("C", sib)]["sic"].startswith("47"):
                        return ("C", sib)
                return None
            return ("C", num)
        return ("P",) + person_key(a["name"])

    def _occupancy(self, yr):
        day = DAY[yr]
        ent = PR.in_force(self.lists[LIST[yr]], day)
        at = {}
        for a in self.accounts:
            if a["frm"] <= day and (a["to"] is None or a["to"] >= day):
                assert a["uarn"] not in at, ("two accounts on one day", a["uarn"])
                at[a["uarn"]] = a
        occ, state = {}, {}
        for uarn, e in ent.items():
            a = at.get(uarn)
            k = self.occupier(a, yr) if a else None
            state[uarn] = "empty" if (a is not None and k is None) else ("unbilled" if a is None else "occupied")
            if k is not None:
                occ.setdefault(k, []).append(e)
        self.state = getattr(self, "state", {})
        self.state[yr] = state
        self.entries = getattr(self, "entries", {})
        self.entries[yr] = ent
        return occ

    def retail(self, yr):
        """retail employer key -> (staff, premises entries)"""
        out = {}
        for k, E in self.employers[yr].items():
            if E["sic"].startswith("47") and E["staff"] > 0:
                out[k] = (E["staff"], self.occ[yr].get(k, []))
        return out

    def centre_of(self, pc):
        return self.pcs.get(pc)


def densities(P, yr, kind="tot", pool="retail", basis="area"):
    rows = {d: [] for d in RETAIL_DESC}
    src = P.employers[yr]
    for k, E in src.items():
        if E["staff"] <= 0 or (pool == "retail" and not E["sic"].startswith("47")):
            continue
        ps = P.occ[yr].get(k, [])
        if len(ps) == 1 and ps[0]["d"] in rows:
            rows[ps[0]["d"]].append((E["staff"], ps[0]["a"] if basis == "area" else ps[0]["rv"]))
    D = {}
    for d, r in rows.items():
        s = np.array([x[0] for x in r], float)
        x = np.array([x[1] for x in r], float)
        D[d] = dict(tot=s.sum() / x.sum(), mean=np.mean(s / x), median=np.median(s / x))[kind]
    return D


def regression(P, yr, pool="retail"):
    ds = list(RETAIL_DESC)
    X, y = [], []
    for k, E in P.employers[yr].items():
        if E["staff"] <= 0 or (pool == "retail" and not E["sic"].startswith("47")):
            continue
        ps = P.occ[yr].get(k, [])
        if not ps or any(p["d"] not in ds for p in ps):
            continue
        X.append([sum(p["a"] for p in ps if p["d"] == d) for d in ds])
        y.append(E["staff"])
    b = np.linalg.lstsq(np.array(X), np.array(y, float), rcond=None)[0]
    return dict(zip(ds, b))


def rv23_of(P):
    cur = {}
    for e in P.lists["23"]:
        if e["to"] is None:
            cur[e["uarn"]] = e["rv"]
    for e in P.lists["23"]:
        cur.setdefault(e["uarn"], e["rv"])
    return cur


def place(P, yr, how, D=None):
    """employees placed at the premises in each centre (centre code -> employees)"""
    out = {c: 0.0 for c in P.centres}
    R = P.retail(yr)
    r23 = rv23_of(P) if how == "rv23" else None
    for k, (T, ps) in R.items():
        if how == "postcode":
            for pc, n in P.employers[yr][k]["pcs"]:
                c = P.centre_of(pc)
                if c:
                    out[c] += n
            continue
        if not ps:
            continue
        if how == "count":
            wt = np.ones(len(ps))
        elif how == "area":
            wt = np.array([p["a"] for p in ps])
        elif how == "rv":
            wt = np.array([float(p["rv"]) for p in ps])
        elif how == "rv23":
            wt = np.array([float(r23.get(p["uarn"], p["rv"])) for p in ps])
        elif how == "rvd":
            wt = np.array([p["rv"] * D[p["d"]] for p in ps])
        elif how == "classcount":
            wt = np.array([D[p["d"]] for p in ps])
        else:
            wt = np.array([p["a"] * D[p["d"]] for p in ps])
        wt = wt / wt.sum()
        for p, x in zip(ps, wt):
            c = P.centre_of(p["pc"])
            if c:
                out[c] += T * x
    return out


def class_mean_staff(P, yr):
    rows = {d: [] for d in RETAIL_DESC}
    for k, (T, ps) in P.retail(yr).items():
        if len(ps) == 1 and ps[0]["d"] in rows:
            rows[ps[0]["d"]].append(T)
    return {d: float(np.mean(v)) for d, v in rows.items()}


def family(P):
    """(name, how, D22, D26) for the golden and every licensed member that takes the density step"""
    S = [("golden", "d", densities(P, "22"), densities(P, "26"))]
    for kind in ("mean", "median"):
        S.append(("d_" + kind, "d", densities(P, "22", kind), densities(P, "26", kind)))
    S.append(("d_all", "d", densities(P, "22", pool="all"), densities(P, "26", pool="all")))
    D26 = densities(P, "26")
    S.append(("d_pooled26", "d", D26, D26))
    S.append(("d_reg", "d", regression(P, "22"), regression(P, "26")))
    S.append(("d_reg_all", "d", regression(P, "22", "all"), regression(P, "26", "all")))
    S.append(("d_rv", "rvd", densities(P, "22", basis="rv"), densities(P, "26", basis="rv")))
    S.append(("classcount", "classcount", class_mean_staff(P, "22"), class_mean_staff(P, "26")))
    return S


STANDING = ("golden", "d_mean", "d_median", "d_all", "d_pooled26", "d_reg", "d_reg_all")


def routes(P):
    """every route's employment by centre in both Marches"""
    out = {}
    for name, how, D22, D26 in family(P):
        out[name] = (place(P, "22", how, D22), place(P, "26", how, D26))
    for how in ("postcode", "count", "area", "rv", "rv23"):
        out[how] = (place(P, "22", how), place(P, "26", how))
    return out


def change(lv):
    a, b = lv
    return {c: b[c] / a[c] - 1 for c in a}


def qualifying(lv):
    ch = change(lv)
    return sorted(c for c, v in ch.items() if v <= TH)


# ------------------------------------------------------------------------------------------------ asks

def vacancy(P):
    """asks A and B: for each district, the shop premises in its designated centres empty at each 31 March, and of
    those the ones empty for twelve months or more; an unbilled premises is occupied (no account means no liability,
    and an empty premises' owner is liable), and an empty spell runs back through consecutive owner accounts"""
    by_uarn = {}
    for a in P.accounts:
        by_uarn.setdefault(a["uarn"], []).append(a)
    for v in by_uarn.values():
        v.sort(key=lambda a: a["frm"])
    out = {}
    for yr in ("22", "26"):
        day = DAY[yr]
        empty, long = {}, {}
        for uarn, e in P.entries[yr].items():
            c = P.centre_of(e["pc"])
            if e["d"] != "R1" or not c:
                continue
            d = P.centres[c][1]
            empty.setdefault(d, 0)
            long.setdefault(d, 0)
            if P.state[yr][uarn] != "empty":
                continue
            empty[d] += 1
            acc = by_uarn[uarn]
            i = [j for j, a in enumerate(acc) if a["frm"] <= day and (a["to"] is None or a["to"] >= day)][0]
            start = acc[i]["frm"]
            while i > 0 and acc[i - 1]["to"] is not None and acc[i - 1]["to"] + dt.timedelta(days=1) == acc[i]["frm"] \
                    and P.occupier(acc[i - 1], yr) is None:
                i -= 1
                start = acc[i]["frm"]
            if start <= dt.date(day.year - 1, 4, 1):
                long[d] += 1
        out[yr] = (empty, long)
    return out


def summary(target):
    P = Pack(target)
    R = routes(P)
    return P, R
