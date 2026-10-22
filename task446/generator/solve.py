"""Independent golden path for task446 (architecture 3). Reads target/ only; shares no code or state with
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
        self.fx = {r["currency"]: float(r["units_per_gbp"]) for r in rows(t, "treasury_closing_rates_20260930.csv")}
        self.fac = rows(t, "facility_obligor_extract_20260930.csv")
        self.hist = defaultdict(list)
        self.versions = defaultdict(list)
        for r in rows(t, "facility_limit_history_20261008.csv"):
            k = (r["booking_entity"], r["facility_id"])
            self.hist[k].append((dt.datetime.strptime(r["effective_from"], "%Y-%m-%dT%H:%M:%SZ"),
                                 float(r["committed_limit"])))
            self.versions[k].append((r["effective_from"], r["committed_limit"], r["source"]))
        for v in self.hist.values():
            v.sort()
        for v in self.versions.values():
            v.sort()

    # ------------------------------------------------------------ membership
    def group_of_key(self, date, follow_direct=True, keep_lapsed=True, follow_funds=False, branches=True,
                     successors=True, case_fold=True, apex=True):
        """entity_key -> group_id at a date, under the standard's section 2. apex=False is the reading of 2.2
        without its ultimate-parent clause: the ultimate parent counts only when it is itself booked."""
        top_to_group = {r["ultimate_parent_lei"]: r["group_id"] for r in self.reg if r["ultimate_parent_lei"]}
        key_to_group = {}
        for r in self.obl:
            if not r["group_id"]:
                continue
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
            if lei in top_to_group and (apex or depth > 0 or lei in key_to_group):
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

    def customer_keys(self, date, active_only=False):
        """keys of the customers the credit system had opened by the date (by LEI and by Companies House
        number); active_only is the misreading that takes the extract's status for the status at the date"""
        out = set()
        for r in self.obl:
            if d(r["customer_since"]) > date:
                continue
            if active_only and r["customer_status"] != "ACTIVE":
                continue
            if r["lei"]:
                out.add(r["lei"].upper())
            if r["companies_house_no"]:
                out.add("CRN:" + r["companies_house_no"])
        return out

    def facility_keys(self):
        """the misreading that takes a borrower to be an obligor on the 30 Sep 2026 facility extract"""
        cust = {r["customer_id"]: r for r in self.obl}
        out = set()
        for r in self.fac:
            c = cust.get(r["customer_id"])
            if c and c["lei"]:
                out.add(c["lei"].upper())
            if c and c["companies_house_no"]:
                out.add("CRN:" + c["companies_house_no"])
        return out

    def flag_detail(self, date, borrower="customer", **kw):
        """group -> dict(kind, red, cov) for every group with a member AMBER or RED in the publication for the
        date. kind D: a customer the bank lends to carries the flag; kind I: only members it does not lend to,
        reached through the GLEIF records or as the ultimate parent."""
        resolve, _ = self.group_of_key(date, **kw)
        case_fold = kw.get("case_fold", True)
        if borrower == "customer":
            keys = self.customer_keys(date)
        elif borrower == "active":
            keys = self.customer_keys(date, active_only=True)
        else:
            keys = self.facility_keys()
        out = {}
        ds = date.isoformat()
        for r in self.signals:
            if r["publication_date"] != ds or r["signal"] == "GREEN":
                continue
            k = r["entity_key"]
            if case_fold and not k.startswith("CRN:"):
                k = k.upper()
            g = resolve(k)
            if not g:
                continue
            x = out.setdefault(g, dict(kind="I", red=False, cov=False))
            if k in keys:
                x["kind"] = "D"
            x["red"] = x["red"] or r["signal"] == "RED"
            x["cov"] = x["cov"] or "COVENANT" in r["trigger_codes"]
        return out

    def flagged(self, date, **kw):
        return set(self.flag_detail(date, **kw))

    def cohort_table(self, **kw):
        tab = []
        for i, cs in enumerate(COHORTS):
            date = d(cs)
            M = self.active(date) - self.on_list(date)
            det = {g: v for g, v in self.flag_detail(date, **kw).items() if g in M}
            F = set(det)
            R = (self.reached(date) & M) if i < 4 else None
            tab.append(dict(date=cs, M=M, F=F, R=R, det=det, FD={g for g in F if det[g]["kind"] == "D"},
                            FI={g for g in F if det[g]["kind"] == "I"}))
        return tab


def cohort_counts(tab):
    """for each closed cohort: N, flagged, reaching, flagged and reaching, and the same by kind, colour and
    covenant trigger"""
    out = []
    for c in tab[:4]:
        R, F, det = c["R"], c["F"], c["det"]
        row = dict(N=len(c["M"]), F=len(F), P=len(R), TP=len(R & F))
        for name, sel in (("D", lambda v: v["kind"] == "D"), ("I", lambda v: v["kind"] == "I"),
                          ("RED", lambda v: v["red"]), ("COV", lambda v: v["cov"]),
                          ("D_RED", lambda v: v["kind"] == "D" and v["red"]),
                          ("I_RED", lambda v: v["kind"] == "I" and v["red"]),
                          ("D_COV", lambda v: v["kind"] == "D" and v["cov"])):
            S = {g for g in F if sel(det[g])}
            row[name], row[name + "_R"] = len(S), len(S & R)
        row["U"], row["U_R"] = row["N"] - row["F"], row["P"] - row["TP"]
        out.append(row)
    return out


def measures(tab):
    cc = cohort_counts(tab)
    S = {k: sum(c[k] for c in cc) for k in cc[0]}
    S["FP"] = S["F"] - S["TP"]
    S.update(hit=S["TP"] / S["F"], capture=S["TP"] / S["P"], false_alarm=S["FP"] / (S["N"] - S["P"]),
             miss=(S["P"] - S["TP"]) / (S["N"] - S["F"]), NF=S["F"])
    return S


def _lin(x, y, w=None):
    n = len(x)
    w = w or [1.0] * n
    sw = sum(w)
    mx = sum(a * b for a, b in zip(w, x)) / sw
    my = sum(a * b for a, b in zip(w, y)) / sw
    b = sum(wi * (xi - mx) * (yi - my) for wi, xi, yi in zip(w, x, y)) / sum(wi * (xi - mx) ** 2 for wi, xi in zip(w, x))
    return my - b * mx, b


def _rate(cs, key, mean=False):
    if mean:
        return sum(c[key + "_R"] / c[key] for c in cs) / len(cs)
    return sum(c[key + "_R"] for c in cs) / sum(c[key] for c in cs)


def basis_fit(name, cs):
    """Set a basis from a list of cohort rows; return f(row) -> expected arrivals for a cohort or book row. A
    row carries N, F and the cell counts of cohort_counts (outcomes not needed)."""
    N = sum(c["N"] for c in cs)
    F = sum(c["F"] for c in cs)
    P = sum(c["P"] for c in cs)
    TP = sum(c["TP"] for c in cs)
    if name == "hit_and_miss":
        pf, pu = TP / F, (P - TP) / (N - F)
        return lambda r: r["F"] * pf + (r["N"] - r["F"]) * pu
    if name == "mean_hit_and_miss":
        pf = sum(c["TP"] / c["F"] for c in cs) / len(cs)
        pu = sum((c["P"] - c["TP"]) / (c["N"] - c["F"]) for c in cs) / len(cs)
        return lambda r: r["F"] * pf + (r["N"] - r["F"]) * pu
    if name in ("latest_hit_and_miss", "most_stressed_hit_and_miss"):
        c = cs[-1] if name.startswith("latest") else max(cs, key=lambda c: c["P"] / c["N"])
        pf, pu = c["TP"] / c["F"], (c["P"] - c["TP"]) / (c["N"] - c["F"])
        return lambda r: r["F"] * pf + (r["N"] - r["F"]) * pu
    if name == "one_share":
        return lambda r: r["N"] * P / N
    if name == "capture_false_alarm":
        se, fa = TP / P, (F - TP) / (N - P)
        return lambda r: r["N"] * (r["F"] / r["N"] - fa) / (se - fa)
    if name == "hit_and_miss_trended":
        x = [c["F"] / c["N"] for c in cs]
        h0, hb = _lin(x, [c["TP"] / c["F"] for c in cs])
        m0, mb = _lin(x, [(c["P"] - c["TP"]) / (c["N"] - c["F"]) for c in cs])
        return lambda r: r["F"] * (h0 + hb * r["F"] / r["N"]) + (r["N"] - r["F"]) * (m0 + mb * r["F"] / r["N"])
    if name == "share_on_flagged_share":
        c0, b = _lin([c["F"] / c["N"] for c in cs], [c["P"] / c["N"] for c in cs])
        return lambda r: r["N"] * (c0 + b * r["F"] / r["N"])
    if name == "arrivals_on_flagged_count":
        c0, b = _lin([float(c["F"]) for c in cs], [float(c["P"]) for c in cs])
        return lambda r: c0 + b * r["F"]
    if name == "colour_split":
        pr = sum(c["RED_R"] for c in cs) / sum(c["RED"] for c in cs)
        pa = (TP - sum(c["RED_R"] for c in cs)) / (F - sum(c["RED"] for c in cs))
        pu = (P - TP) / (N - F)
        return lambda r: r["RED"] * pr + (r["F"] - r["RED"]) * pa + (r["N"] - r["F"]) * pu
    if name == "covenant_split":
        pc = sum(c["COV_R"] for c in cs) / sum(c["COV"] for c in cs)
        po = (TP - sum(c["COV_R"] for c in cs)) / (F - sum(c["COV"] for c in cs))
        pu = (P - TP) / (N - F)
        return lambda r: r["COV"] * pc + (r["F"] - r["COV"]) * po + (r["N"] - r["F"]) * pu
    if name in ("split", "split_mean"):
        m = name == "split_mean"
        pd_, pi, pu = _rate(cs, "D", m), _rate(cs, "I", m), _rate(cs, "U", m)
        return lambda r: r["D"] * pd_ + r["I"] * pi + (r["N"] - r["F"]) * pu
    if name == "split_colour":
        p = {}
        for k in ("D", "I"):
            n_r, k_r = sum(c[k + "_RED"] for c in cs), sum(c[k + "_RED_R"] for c in cs)
            n_a, k_a = sum(c[k] for c in cs) - n_r, sum(c[k + "_R"] for c in cs) - k_r
            p[k] = (k_r / n_r, k_a / n_a)
        pu = _rate(cs, "U")
        return lambda r: (r["D_RED"] * p["D"][0] + (r["D"] - r["D_RED"]) * p["D"][1] + r["I_RED"] * p["I"][0] +
                          (r["I"] - r["I_RED"]) * p["I"][1] + (r["N"] - r["F"]) * pu)
    if name == "split_covenant":
        n_c, k_c = sum(c["D_COV"] for c in cs), sum(c["D_COV_R"] for c in cs)
        n_o, k_o = sum(c["D"] for c in cs) - n_c, sum(c["D_R"] for c in cs) - k_c
        pi, pu = _rate(cs, "I"), _rate(cs, "U")
        return lambda r: r["D_COV"] * k_c / n_c + (r["D"] - r["D_COV"]) * k_o / n_o + r["I"] * pi + (r["N"] - r["F"]) * pu
    if name == "direct_vs_rest":
        pd_ = _rate(cs, "D")
        prest = sum(c["I_R"] + c["U_R"] for c in cs) / sum(c["I"] + c["U"] for c in cs)
        return lambda r: r["D"] * pd_ + (r["N"] - r["D"]) * prest
    if name == "split_trended":
        t = []
        for k in ("D", "I", "U"):
            a, b = _lin(list(range(len(cs))), [c[k + "_R"] / c[k] for c in cs])
            t.append(a + b * len(cs))
        return lambda r: r["D"] * t[0] + r["I"] * t[1] + (r["N"] - r["F"]) * t[2]
    raise ValueError(name)


BASES = ["split", "split_mean", "split_colour", "split_covenant", "direct_vs_rest", "hit_and_miss",
         "mean_hit_and_miss", "latest_hit_and_miss", "most_stressed_hit_and_miss", "one_share", "capture_false_alarm",
         "hit_and_miss_trended", "share_on_flagged_share", "arrivals_on_flagged_count", "colour_split",
         "covenant_split", "split_trended"]
WINDOWS = dict(latest=slice(3, 4), last2=slice(2, 4), last3=slice(1, 4), first3=slice(0, 3))


def book_row(c):
    """the forward book's counts in the same cells"""
    F, det = c["F"], c["det"]
    row = dict(N=len(c["M"]), F=len(F))
    for name, sel in (("D", lambda v: v["kind"] == "D"), ("I", lambda v: v["kind"] == "I"),
                      ("RED", lambda v: v["red"]), ("COV", lambda v: v["cov"]),
                      ("D_RED", lambda v: v["kind"] == "D" and v["red"]),
                      ("I_RED", lambda v: v["kind"] == "I" and v["red"]),
                      ("D_COV", lambda v: v["kind"] == "D" and v["cov"])):
        row[name] = sum(1 for g in F if sel(det[g]))
    row["U"] = row["N"] - row["F"]
    return row


def basis_test(tab):
    """Each closed cohort predicted from the other three taken together; error = largest miss as a share of
    the cohort's actual arrivals. Returns {basis: (misses, error, forward)}. Never filed: the design's
    evidence that the data force the basis."""
    cc = cohort_counts(tab)
    fwd = book_row(tab[4])
    out = {}
    for name in BASES:
        miss = []
        for i in range(4):
            fn = basis_fit(name, [c for j, c in enumerate(cc) if j != i])
            miss.append(fn(cc[i]) / cc[i]["P"] - 1)
        out[name] = (miss, max(abs(x) for x in miss), basis_fit(name, cc)(fwd))
    return out


def forecast(tab, model="split", window=None):
    """The forecast on the flag-kind basis (or a named basis), with each group's probability for the band
    table: the closed cohorts taken together unless a window is named."""
    cc = cohort_counts(tab)
    cs = cc[WINDOWS[window]] if window else cc
    fwd = tab[4]
    row = book_row(fwd)
    total = basis_fit(model, cs)(row)
    pu = _rate(cs, "U")
    if model in ("split", "split_mean", "split_trended"):
        m = model == "split_mean"
        if model == "split_trended":
            t = []
            for k in ("D", "I", "U"):
                a, b = _lin(list(range(len(cs))), [c[k + "_R"] / c[k] for c in cs])
                t.append(a + b * len(cs))
            pd_, pi, pu = t
        else:
            pd_, pi, pu = _rate(cs, "D", m), _rate(cs, "I", m), _rate(cs, "U", m)

        def p_of(g):
            v = fwd["det"].get(g)
            return pu if v is None else (pd_ if v["kind"] == "D" else pi)
    elif model == "hit_and_miss":
        S = {k: sum(c[k] for c in cs) for k in ("TP", "F", "P", "N")}
        pf, pu = S["TP"] / S["F"], (S["P"] - S["TP"]) / (S["N"] - S["F"])
        pd_ = pi = pf

        def p_of(g):
            return pf if g in fwd["F"] else pu
    else:
        pd_ = pi = None

        def p_of(g):
            raise ValueError("no group probabilities on basis " + model)
    flagged = sum(p_of(g) for g in fwd["F"]) if pd_ is not None else None
    unflagged = (row["N"] - row["F"]) * pu if pd_ is not None else None
    return dict(model=model, window=window, test=basis_test(tab), N1=row["N"], F1=row["F"], D1=row["D"],
                I1=row["I"], a1=row["F"] / row["N"], p_d=pd_, p_i=pi, p_unflag=pu, p_of=p_of, flagged=flagged,
                unflagged=unflagged, total=total, measures=measures(tab), cc=cc, row=row)


# ------------------------------------------------------------ exposure (CRM-07 6.1)
END_OF_DAY_UTC = dt.datetime(2026, 9, 30, 23, 0, 0)     # end of 30 September 2026, BST


def limit_on_clock(pk, key, ext_limit, clock):
    h = pk.hist.get(key, [])
    if clock == "B1":
        return ext_limit
    if clock == "right":
        sel = [v for t, v in h if t <= END_OF_DAY_UTC]
    elif clock == "B2":
        sel = [v for t, v in h if t.date() <= dt.date(2026, 9, 30)]
    elif clock == "B0":
        sel = [v for t, v in h if t.date() < dt.date(2026, 9, 30)]
    elif clock == "B3":
        sel = [v for t, v in h]
    else:
        raise ValueError(clock)
    return sel[-1] if sel else 0.0


def customer_groups(pk, hz=True, member="both"):
    """customer -> the groups it is a member of at 30 Sep 2026 under 2.2: the group the credit system books it
    to and the group whose ultimate parent its GLEIF records consolidate it into (one group for nearly every
    customer; two for a company consolidated into one group and booked to another). Customers not yet grouped
    are placed through GLEIF (hz). member "booked" or "gleif" reads a two-group customer one way only."""
    date = dt.date(2026, 9, 30)
    resolve, _ = pk.group_of_key(date)
    tops = {r["ultimate_parent_lei"]: r["group_id"] for r in pk.reg if r["ultimate_parent_lei"]}
    ult = {}
    for r in pk.rr:
        st, en = d(r["Relationship.Period1.startDate"]), d(r["Relationship.Period1.endDate"])
        if r["Relationship.RelationshipType"] == "IS_ULTIMATELY_CONSOLIDATED_BY" and st <= date and (en is None or en > date):
            ult[r["Relationship.StartNode.NodeID"]] = r["Relationship.EndNode.NodeID"]
    out = {}
    for r in pk.obl:
        gs = set()
        if r["group_id"]:
            gs.add(r["group_id"])
        elif hz and r["lei"]:
            g = resolve(r["lei"].upper())
            if g:
                gs.add(g)
        lei = r["lei"].upper()
        cons = tops.get(ult.get(lei, ""))
        if r["group_id"] and cons and cons != r["group_id"]:
            if member == "both":
                gs.add(cons)
            elif member == "gleif":
                gs = {cons}
        out[r["customer_id"]] = gs
    return out


def booked_twice(pk, dup="right"):
    """Facilities a reading of the extract's near-duplicates leaves out. Near-duplicates are facilities of one ledger
    with the same customers, product, currency, limit, dates and status. "right": a facility whose whole limit
    history repeats, stamp, limit and source, that of a lower-numbered near-duplicate (the ledger booked one
    creation message twice); "terms": every near-duplicate after the lowest-numbered; "undrawn": the undrawn ones
    among near-duplicates (all but the lowest-numbered where none is drawn); "keep": none."""
    if dup == "keep":
        return set()
    fac = {}
    for r in pk.fac:
        k = (r["booking_entity"], r["facility_id"])
        x = fac.setdefault(k, dict(cust=set(), drawn=0.0, terms=(r["product"], r["currency"], r["committed_limit"],
                                                                 r["start_date"], r["final_maturity_date"],
                                                                 r["facility_status"])))
        x["cust"].add(r["customer_id"])
        x["drawn"] += float(r["drawn_balance"])
    sets = defaultdict(list)
    for k, x in fac.items():
        sets[(k[0], frozenset(x["cust"]), x["terms"])].append(k)
    out = set()
    for ks in sets.values():
        if len(ks) < 2:
            continue
        ks.sort(key=lambda k: int(k[1]))
        if dup == "terms":
            out.update(ks[1:])
        elif dup == "undrawn":
            drawn = [k for k in ks if fac[k]["drawn"] > 0]
            out.update(k for k in ks if fac[k]["drawn"] == 0 and (drawn or k != ks[0]))
        elif dup == "right":
            out.update(k for i, k in enumerate(ks) if any(pk.versions[k] == pk.versions[j] for j in ks[:i]))
        else:
            raise ValueError(dup)
    return out


def exposures(pk, grain="group", clock="right", hz=True, order="first", member="both", dup="right"):
    date = dt.date(2026, 9, 30)
    cg = customer_groups(pk, hz, member)
    twice = booked_twice(pk, dup)
    rows_ = [r for r in pk.fac if d(r["start_date"]) <= date < d(r["final_maturity_date"])
             and (r["booking_entity"], r["facility_id"]) not in twice]
    if grain in ("fid", "bkfid"):
        seen, keep = set(), []
        for r in (rows_ if order == "first" else rows_[::-1]):
            k = r["facility_id"] if grain == "fid" else (r["booking_entity"], r["facility_id"])
            if k in seen:
                continue
            seen.add(k)
            keep.append(r)
        rows_ = keep
    exp = defaultdict(float)
    counted = set()
    for r in rows_:
        key = (r["booking_entity"], r["facility_id"])
        lim = limit_on_clock(pk, key, float(r["committed_limit"]), clock)
        rate = pk.fx[r["currency"]] if r["currency"] != "GBP" else 1.0
        for g in sorted(cg.get(r["customer_id"], ())):
            if grain == "group":
                if (g, key) in counted:
                    continue
                counted.add((g, key))
            exp[g] += lim / rate
    return exp


def band_of(x):
    for i, e in enumerate(EDGES):
        if x < e:
            return i
    return 4


def band_table(tab, fc, exp):
    fwd = tab[4]
    p = fc["p_of"]
    out = []
    for b in range(5):
        G = [g for g in fwd["M"] if band_of(exp.get(g, 0.0)) == b]
        Fg = [g for g in G if g in fwd["F"]]
        ea = sum(p(g) for g in G)
        ex = sum(p(g) * exp.get(g, 0.0) for g in G)
        out.append(dict(band=BANDS[b], groups=len(G), flagged=len(Fg),
                        direct=sum(1 for g in Fg if g in fwd["FD"]), indirect=sum(1 for g in Fg if g in fwd["FI"]),
                        committed=sum(exp.get(g, 0.0) for g in G), exp_arrivals=ea,
                        exp_flagged=sum(p(g) for g in Fg), exp_exposure=ex))
    return out


def golden(t=TARGET):
    pk = Pack(t)
    tab = pk.cohort_table()
    fc = forecast(tab)
    exp = exposures(pk)
    bt = band_table(tab, fc, exp)
    return dict(pack=pk, tab=tab, fc=fc, exp=exp, bands=bt, call=round(fc["total"]))


# ------------------------------------------------------------ CRM-07 2.2: the ultimate parent is a member
COMMITTED = dict(call=None, flagged=165, bands=None)


def check_membership(G, t=TARGET):
    """The amended 2.2 read literally (the ultimate parent, booked customers and GLEIF consolidation members)
    gives the committed figures; no flag sits on an ultimate parent the bank does not lend to, so the clause's
    reading moves nothing; every apex edge has one reading."""
    import pypdf
    pk, tab = G["pack"], G["tab"]
    std = " ".join("".join(p.extract_text() for p in pypdf.PdfReader(
        os.path.join(t, "early_warning_and_watch_list_standard.pdf")).pages).split())
    assert "A group's members are its ultimate parent, the customers the credit system books to it" in std
    assert len(tab[4]["F"]) == COMMITTED["flagged"]
    if COMMITTED["call"] is not None:
        assert G["call"] == COMMITTED["call"], G["call"]
    if COMMITTED["bands"] is not None:
        got = [(r["groups"], round(r["committed"] / 1e6 + 1e-12, 1), r["flagged"], round(r["exp_arrivals"] + 1e-12, 1),
                round(r["exp_exposure"] / 1e6 + 1e-12, 1)) for r in G["bands"]]
        assert got == COMMITTED["bands"], got
    no_apex = pk.cohort_table(apex=False)
    only = [len(a["F"] - b["F"]) for a, b in zip(tab, no_apex)]
    assert only == [0] * 5 and all(a["det"] == b["det"] for a, b in zip(tab, no_apex)), only
    tops = {r["ultimate_parent_lei"]: r["group_id"] for r in pk.reg}
    assert all(tops), "every group has an ultimate parent LEI"
    booked = {r["lei"]: r["group_id"] for r in pk.obl if r["lei"]}
    assert all(booked[l] == g for l, g in tops.items() if l in booked), "a booked apex is booked to its own group"
    cons = ("IS_ULTIMATELY_CONSOLIDATED_BY", "IS_DIRECTLY_CONSOLIDATED_BY")
    assert not any(r["Relationship.StartNode.NodeID"] in tops for r in pk.rr
                   if r["Relationship.RelationshipType"] in cons), "no apex reports a consolidating parent"
    with open(os.path.join(t, "gleif_repex_20260930.csv"), encoding="utf-8", newline="") as fh:
        rx = list(csv.DictReader(fh))
    assert {r["ExceptionReason"] for r in rx if r["LEI"] in tops} <= {"NON_CONSOLIDATING", "NATURAL_PERSONS",
                                                                        "NO_KNOWN_PERSON"}
    br = {r["Relationship.StartNode.NodeID"] for r in pk.rr if r["Relationship.RelationshipType"] ==
          "IS_INTERNATIONAL_BRANCH_OF" and r["Relationship.EndNode.NodeID"] in tops}
    assert not any(r["entity_key"].upper() in br and r["signal"] != "GREEN" for r in pk.signals
                   if r["publication_date"] in COHORTS), "branches of an apex are green at every cohort date"
    return only


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else TARGET
    G = golden(t)
    print("2.2 membership: flagged %d, apex-only flags by cohort %s" % (len(G["tab"][4]["F"]), check_membership(G, t)))
    fc = G["fc"]
    for c, row in zip(G["tab"], fc["cc"] + [fc["row"]]):
        print(c["date"], "N", row["N"], "F", row["F"], "D", row["D"], "I", row["I"],
              "" if c["R"] is None else "P %d TP %d D_R %d I_R %d U_R %d" % (row["P"], row["TP"], row["D_R"],
                                                                             row["I_R"], row["U_R"]))
    for k, (miss, err, fw) in sorted(fc["test"].items(), key=lambda kv: kv[1][1]):
        print("%-28s %s  worst %6.2f%%  forward %7.2f" % (k, " ".join("%+6.1f" % (100 * x) for x in miss), 100 * err, fw))
    for w_ in WINDOWS:
        print("window %-7s %.3f" % (w_, forecast(G["tab"], window=w_)["total"]))
    print("p_d %.5f p_i %.5f p_u %.5f" % (fc["p_d"], fc["p_i"], fc["p_unflag"]))
    print("caseload %.3f -> %d (flagged %.3f, unflagged %.3f)" % (fc["total"], G["call"], fc["flagged"], fc["unflagged"]))
    for r in G["bands"]:
        print("%-28s groups %4d flagged %3d (D %3d I %2d) committed GBP m %9.3f  exp_arrivals %7.3f"
              "  exp_exposure GBP m %8.3f" % (r["band"], r["groups"], r["flagged"], r["direct"], r["indirect"],
                                              r["committed"] / 1e6, r["exp_arrivals"], r["exp_exposure"] / 1e6))
    print("committed total GBP m %.3f, expected exposure total GBP m %.3f" % (
        sum(r["committed"] for r in G["bands"]) / 1e6, sum(r["exp_exposure"] for r in G["bands"]) / 1e6))
