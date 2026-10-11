"""Independent golden path for task446 (architecture 2). Reads target/ only; shares no code or state with
the generator.

    python3 task446/generator/solve.py [target_dir]

Readings that the checks compare against the golden are switched by keyword arguments.
"""
import csv
import datetime as dt
import os
import sys
from collections import defaultdict

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "..", "target")
COHORTS = ["2022-09-30", "2023-09-30", "2024-09-30", "2025-09-30", "2026-09-30"]
EDGES = [5e6, 15e6, 40e6, 100e6]
BANDS = ["Under GBP 5m", "GBP 5m and under GBP 15m", "GBP 15m and under GBP 40m",
         "GBP 40m and under GBP 100m", "GBP 100m and over"]


def d(s):
    return dt.date.fromisoformat(s[:10]) if s else None


def rows(t, name):
    with open(os.path.join(t, name), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


class Pack:
    def __init__(self, t=TARGET):
        self.t = t
        self.signals = rows(t, "ews_entity_signals_2022-09_to_2026-09.csv")
        self.lei = {r["LEI"]: r for r in rows(t, "gleif_lei_cdf_20260930.csv")}
        self.rr = rows(t, "gleif_rr_cdf_20260930.csv")
        self.obl = rows(t, "credit_obligor_master_20260930.csv")
        self.wl = rows(t, "watch_list_history_2020-01_to_2026-09.csv")
        wb = openpyxl.load_workbook(os.path.join(t, "credit_group_register_20260930.xlsx"), read_only=True)
        ws = wb["Group register"]
        it = ws.iter_rows(values_only=True)
        hdr = None
        self.reg = []
        for r in it:
            if r and r[0] == "group_id":
                hdr = r
                continue
            if hdr and r and r[0]:
                rec = dict(zip(hdr, r))
                for k in ("relationship_start", "relationship_end"):
                    v = rec[k]
                    rec[k] = v.date() if isinstance(v, dt.datetime) else v
                self.reg.append(rec)
        self.fx = {r["currency"]: float(r["closing_rate"]) for r in rows(t, "treasury_closing_rates_20260930.csv")}

    # ------------------------------------------------------------ membership
    def group_of_key(self, date, follow_direct=True, keep_lapsed=True, follow_funds=False, branches=True,
                     successors=True, case_fold=True):
        """entity_key -> group_id at a date, under the standard's section 2."""
        top_to_group = {r["ultimate_parent_lei"]: r["group_id"] for r in self.reg if r["ultimate_parent_lei"]}
        key_to_group = {}
        for r in self.obl:
            if r["lei"]:
                key_to_group[r["lei"]] = r["group_id"]
            if r["companies_house_no"]:
                key_to_group["CRN:" + r["companies_house_no"]] = r["group_id"]
        ult, direct, branch, fund = {}, {}, {}, {}
        for r in self.rr:
            st = d(r["Relationship.Period1.startDate"])
            en = d(r["Relationship.Period1.endDate"])
            in_force = st <= date and (en is None or en > date)
            if not in_force:
                continue
            if not keep_lapsed and r["Registration.RegistrationStatus"] == "LAPSED":
                continue
            a, b, typ = r["Relationship.StartNode.NodeID"], r["Relationship.EndNode.NodeID"], r["Relationship.RelationshipType"]
            if typ == "IS_ULTIMATELY_CONSOLIDATED_BY":
                ult[a] = b
            elif typ == "IS_DIRECTLY_CONSOLIDATED_BY":
                direct[a] = b
            elif typ == "IS_INTERNATIONAL_BRANCH_OF":
                branch[a] = b
            elif typ == "IS_FUND-MANAGED_BY":
                fund[a] = b

        def resolve(lei, depth=0):
            if depth > 8:
                return None
            if not keep_lapsed and self.lei.get(lei, {}).get("Registration.RegistrationStatus") == "LAPSED":
                return None
            if lei in top_to_group:
                return top_to_group[lei]
            if lei in key_to_group:
                return key_to_group[lei]
            if successors:
                s = self.lei.get(lei, {}).get("Entity.SuccessorEntity.SuccessorLEI")
                if s:
                    return resolve(s, depth + 1)
            if lei in ult:
                return resolve(ult[lei], depth + 1)
            if follow_direct and lei in direct:
                return resolve(direct[lei], depth + 1)
            if branches and lei in branch:
                return resolve(branch[lei], depth + 1)
            if follow_funds and lei in fund:
                return resolve(fund[lei], depth + 1)
            return None
        return resolve, key_to_group

    # ------------------------------------------------------------ cohorts
    def active(self, date):
        out = set()
        for r in self.reg:
            st, en = r["relationship_start"], r["relationship_end"]
            if st <= date and (en is None or en > date):
                out.add(r["group_id"])
        return out

    def on_list(self, date):
        out = set()
        for r in self.wl:
            st, en = d(r["placed_on"]), d(r["removed_on"])
            if st <= date and (en is None or en > date):
                out.add(r["group_id"])
        return out

    def reached(self, date):
        end = dt.date(date.year + 1, date.month, date.day)
        return {r["group_id"] for r in self.wl if date < d(r["placed_on"]) <= end}

    def flagged(self, date, **kw):
        resolve, _ = self.group_of_key(date, **kw)
        case_fold = kw.get("case_fold", True)
        out = set()
        ds = date.isoformat()
        for r in self.signals:
            if r["publication_date"] != ds or r["signal"] == "GREEN":
                continue
            k = r["entity_key"]
            if case_fold and not k.startswith("CRN:"):
                k = k.upper()
            g = resolve(k)
            if g:
                out.add(g)
        return out

    def cohort_table(self, **kw):
        tab = []
        for i, cs in enumerate(COHORTS):
            date = d(cs)
            M = self.active(date) - self.on_list(date)
            F = self.flagged(date, **kw) & M
            R = (self.reached(date) & M) if i < 4 else None
            tab.append(dict(date=cs, M=M, F=F, R=R))
        return tab


def measures(tab):
    P = sum(len(c["R"]) for c in tab[:4])
    TP = sum(len(c["R"] & c["F"]) for c in tab[:4])
    NF = sum(len(c["F"]) for c in tab[:4])
    N = sum(len(c["M"]) for c in tab[:4])
    FP = NF - TP
    return dict(hit=TP / NF, capture=TP / P, false_alarm=FP / (N - P), miss=(P - TP) / (N - NF),
                P=P, TP=TP, NF=NF, N=N, FP=FP)


def forecast(tab, model="error_rates"):
    m = measures(tab)
    fwd = tab[4]
    N1, F1 = len(fwd["M"]), len(fwd["F"])
    a1 = F1 / N1
    if model == "error_rates":
        se, f = m["capture"], m["false_alarm"]
        p1 = (a1 - f) / (se - f)
        pf, pu = se * p1 / a1, (1 - se) * p1 / (1 - a1)
    elif model == "yield":
        pf, pu = m["hit"], m["miss"]
    else:
        raise ValueError(model)
    return dict(N1=N1, F1=F1, a1=a1, p_flag=pf, p_unflag=pu, flagged=F1 * pf, unflagged=(N1 - F1) * pu,
                total=F1 * pf + (N1 - F1) * pu, measures=m)


# ------------------------------------------------------------ exposure
def exposures(pk, scheduled=False, with_dac=True, fx_multiply=False, count_matured=False, status_filter=True):
    date = dt.date(2026, 9, 30)
    files = ["facility_extract_hbplc_20260930.csv" if scheduled else "facility_extract_hbplc_20260930_rerun.csv"]
    if with_dac:
        files.append("facility_extract_hbdac_20260930.csv")
    cust_group = {r["customer_id"]: r["group_id"] for r in pk.obl}
    exp = defaultdict(float)
    for fn in files:
        for r in rows(pk.t, fn):
            if status_filter and r["facility_status"] != "ACTIVE":
                continue
            if not count_matured and d(r["final_maturity_date"]) <= date:
                continue
            lim = float(r["committed_limit"])
            rate = pk.fx.get(r["currency"], 1.0) if r["currency"] != "GBP" else 1.0
            exp[cust_group[r["customer_id"]]] += lim * rate if fx_multiply else lim / rate
    return exp


def band_of(x):
    for i, e in enumerate(EDGES):
        if x < e:
            return i
    return 4


def band_table(tab, fc, exp):
    fwd = tab[4]
    out = []
    for b in range(5):
        G = [g for g in fwd["M"] if band_of(exp.get(g, 0.0)) == b]
        Fg = [g for g in G if g in fwd["F"]]
        Ug = [g for g in G if g not in fwd["F"]]
        ef = len(Fg) * fc["p_flag"]
        eu = len(Ug) * fc["p_unflag"]
        ex = fc["p_flag"] * sum(exp.get(g, 0.0) for g in Fg) + fc["p_unflag"] * sum(exp.get(g, 0.0) for g in Ug)
        out.append(dict(band=BANDS[b], groups=len(G), flagged=len(Fg), exp_flagged=ef, exp_unflagged=eu,
                        exp_total=ef + eu, committed=sum(exp.get(g, 0.0) for g in G), exp_exposure=ex))
    return out


def golden(t=TARGET):
    pk = Pack(t)
    tab = pk.cohort_table()
    fc = forecast(tab, "error_rates")
    exp = exposures(pk)
    bt = band_table(tab, fc, exp)
    return dict(pack=pk, tab=tab, fc=fc, exp=exp, bands=bt, call=round(fc["total"]))


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else TARGET
    G = golden(t)
    for c in G["tab"]:
        print(c["date"], len(c["M"]), len(c["F"]), None if c["R"] is None else (len(c["R"]), len(c["R"] & c["F"])))
    fc = G["fc"]
    m = fc["measures"]
    print("hit %.4f capture %.4f false-alarm %.4f miss %.5f" % (m["hit"], m["capture"], m["false_alarm"], m["miss"]))
    print("forward N %d flagged %d; p_flag %.5f p_unflag %.5f" % (fc["N1"], fc["F1"], fc["p_flag"], fc["p_unflag"]))
    print("caseload %.3f -> %d (flagged %.3f, unflagged %.3f)" % (fc["total"], G["call"], fc["flagged"], fc["unflagged"]))
    for r in G["bands"]:
        print("%-28s groups %4d flagged %3d  exp_flag %7.3f exp_unflag %7.3f  committed %10.1f  exp_exposure GBP m %8.3f"
              % (r["band"], r["groups"], r["flagged"], r["exp_flagged"], r["exp_unflagged"], r["committed"] / 1e6,
                 r["exp_exposure"] / 1e6))
    print("expected exposure total GBP m %.3f" % (sum(r["exp_exposure"] for r in G["bands"]) / 1e6))
