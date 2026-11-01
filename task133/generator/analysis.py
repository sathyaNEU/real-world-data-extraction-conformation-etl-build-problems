"""Every rung of the call and both asks, computed from target/ alone (task133 architecture 4)."""
import csv
import datetime as dt
import os
import re
from collections import defaultdict

from openpyxl import load_workbook

import params as P

WB = "weighbridge_tickets_port_kowhai_FY2026.csv"
SC = "log_scaling_port_kowhai_FY2026.csv"
FLEET = "fleet_register_2026-06-30.xlsx"
PLAN = "harvest_plan_FY2028.xlsx"
GRADESPEC = "export_log_grade_specifications_2025.pdf"


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class Pack:
    def __init__(self, tdir):
        self.tdir = tdir
        self.wb = read_csv(os.path.join(tdir, WB))
        self.sc = read_csv(os.path.join(tdir, SC))
        ws = load_workbook(os.path.join(tdir, FLEET), read_only=True)["Fleet"]
        rows = list(ws.iter_rows(values_only=True))
        hdr = rows[2]
        self.units = [dict(zip(hdr, r)) for r in rows[3:] if r[0]]
        self.by_rego = {}
        for u in self.units:
            self.by_rego[u["Registration"]] = u
            if u["Previous registration"]:
                self.by_rego[u["Previous registration"]] = u
        self.length = self.grade_lengths()
        pw = load_workbook(os.path.join(tdir, PLAN), read_only=True)["Export"]
        prow = list(pw.iter_rows(values_only=True))
        names = {P.GRADES[g]["name"]: g for g in P.GRADE_ORDER}
        hdr = prow[3]
        self.plan = defaultdict(float)
        for r in prow[4:]:
            if not r[0]:
                continue
            for h, v in zip(hdr[1:], r[1:]):
                if h in names:
                    self.plan[names[h]] += float(v)
        self.link()

    def grade_lengths(self):
        from io_util import pdf_text
        txt = pdf_text(os.path.join(self.tdir, GRADESPEC)).splitlines()
        out = {}
        for i, t in enumerate(txt):
            if t in P.GRADES and i + 2 < len(txt):
                out[t] = float(txt[i + 2])
        return out

    def link(self):
        """Each port weighbridge ticket to the scaling record of the same truck that follows it."""
        by = defaultdict(list)
        for s in self.sc:
            by[s["truck_rego"]].append((dt.datetime.strptime(s["scaled_at"], "%Y-%m-%d %H:%M:%S"), s))
        for v in by.values():
            v.sort(key=lambda x: x[0])
        self.loads = []
        for t in self.wb:
            tw = dt.datetime.strptime(t["weighed_at"], "%d/%m/%Y %H:%M")
            cands = [s for ts, s in by[t["vehicle_rego"]] if tw <= ts <= tw + dt.timedelta(minutes=60)]
            s = cands[0]
            u = self.by_rego.get(t["vehicle_rego"])
            self.loads.append(dict(ticket=t["ticket_no"], grade=t["product_code"], net=float(t["net_tonnes"]),
                                   jas=float(s["jas_m3"]), unit=u, rego=t["vehicle_rego"], date=tw.date()))

    def cap(self, u, grade, fixed_length=None):
        L = fixed_length or self.length[grade]
        return float(u["Full bunks %s m logs (JAS m3)" % ("12.1" if L == 12.1 else ("5.9" if L == 5.9 else "3.9"))])

    def payload(self, ld, mode="golden", dens=None):
        u = ld["unit"]
        if u is None:
            return None
        gross = P.NEW_GROSS if u["50MAX permit"] == "Y" else P.OLD_GROSS
        m = gross - float(u["Tare (t)"])
        d = dens if dens is not None else ld["net"] / ld["jas"]
        if mode == "mass_only":
            return m
        if mode == "at_limit_only":
            at_limit = ld["net"] + float(u["Tare (t)"]) >= P.OLD_GROSS - 0.2
            return m if at_limit else ld["net"]
        if mode == "plus_six":
            return ld["net"] + (6.0 if u["50MAX permit"] == "Y" else 0.0)
        if mode == "one_capacity":
            return min(m, self.cap(u, ld["grade"], fixed_length=12.1) * d)
        return min(m, self.cap(u, ld["grade"]) * d)

    def loads_by_grade(self, mode="golden", grade_density=False, drop_unmapped=False):
        dmean = {}
        if grade_density:
            for g in P.GRADE_ORDER:
                ls = [l for l in self.loads if l["grade"] == g]
                dmean[g] = sum(l["net"] for l in ls) / sum(l["jas"] for l in ls)
        pay = defaultdict(list)
        for l in self.loads:
            if l["unit"] is None:
                continue
            if drop_unmapped and l["rego"] != l["unit"]["Registration"]:
                continue
            pay[l["grade"]].append(self.payload(l, mode, dmean.get(l["grade"]) if grade_density else None))
        return {g: self.plan[g] / (sum(pay[g]) / len(pay[g])) for g in P.GRADE_ORDER}

    def fleet_average(self):
        """R0: every load gains six tonnes, fleet-wide average payload."""
        avg = sum(l["net"] for l in self.loads) / len(self.loads)
        tot = sum(self.plan.values())
        return {g: self.plan[g] / (avg + 6.0) for g in P.GRADE_ORDER}


def ladder(tdir):
    pk = Pack(tdir)
    res = {
        "golden": pk.loads_by_grade("golden"),
        "R0_fleet_average_plus_six": pk.fleet_average(),
        "R1_permit_units_to_the_new_limit": pk.loads_by_grade("mass_only"),
        "R2_loads_at_the_old_limit_only": pk.loads_by_grade("at_limit_only"),
        "R3_one_bunk_volume_per_unit": pk.loads_by_grade("one_capacity"),
        "R4_plus_six_on_permit_units": pk.loads_by_grade("plus_six"),
        "V_grade_mean_density": pk.loads_by_grade("golden", grade_density=True),
        "V_unmapped_plates_dropped": pk.loads_by_grade("golden", drop_unmapped=True),
    }
    return pk, res


# ====================================================================== the asks
def _d(s):
    return dt.datetime.strptime(s, "%d/%m/%Y").date()


def quarter(d):
    if not (P.FY26[0] <= d <= P.FY26[1]):
        return None
    return "Q%d" % ((d.month - 7) % 12 // 3 + 1)


def ask_a(tdir, pk=None, by_owner=True, credits=True):
    """FY2026 cartage by the carrier whose unit hauled the load, NZD."""
    pk = pk or Pack(tdir)
    rows = read_csv(os.path.join(tdir, "cartage_invoices_FY2026.csv"))
    code_of = {v: k for k, v in P.CARRIERS.items()}
    out = defaultdict(float)
    seen = set()
    rego_of = {t["ticket_no"]: t["vehicle_rego"] for t in pk.wb}
    for r in rows:
        amt = float(r["amount_nzd"])
        if not credits and amt < 0:
            continue
        if by_owner:
            u = pk.by_rego.get(rego_of.get(r["ticket_ref"]))
            car = code_of[u["Carrier"]] if u else r["carrier_code"]
        else:
            car = r["carrier_code"]
        out[car] += amt
    return {c: out.get(c, 0.0) for c in P.CARRIERS}


def ask_b(tdir, by_weighbridge=True, dedupe=True):
    """FY2026 tonnes delivered to each domestic mill by quarter of the date crossing the mill weighbridge."""
    out = {(m, q): 0.0 for m in P.MILLS for q in ("Q1", "Q2", "Q3", "Q4")}
    if by_weighbridge:
        for r in read_csv(os.path.join(tdir, "mill_weighbridge_logs_FY2026.csv")):
            if not r["supplier_docket"].startswith("MFP"):
                continue
            d = dt.datetime.strptime(r["weigh_in"], "%Y-%m-%d %H:%M").date()
            q = quarter(d)
            if q:
                out[(r["mill_code"], q)] += float(r["gross_t"]) - float(r["tare_t"])
        return out
    seen = set()
    for r in read_csv(os.path.join(tdir, "mill_dockets_FY2026.csv")):
        if dedupe and r["docket_no"] in seen:
            continue
        seen.add(r["docket_no"])
        q = quarter(_d(r["docket_date"]))
        if q:
            out[(r["mill_code"], q)] += float(r["tonnes"])
    return out


if __name__ == "__main__":
    import sys
    pk, res = ladder(sys.argv[1])
    for k, v in res.items():
        print("%-34s %8.0f  " % (k, sum(v.values())) + "  ".join("%s %6.0f" % (g, v[g]) for g in P.GRADE_ORDER))
