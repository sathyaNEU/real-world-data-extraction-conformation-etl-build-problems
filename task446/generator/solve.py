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
        self.fx = {r["currency"]: float(r["units_per_gbp"]) for r in rows(t, "treasury_closing_rates_20260930.csv")}
        self.fac = rows(t, "facility_obligor_extract_20260930.csv")
        self.hist = defaultdict(list)
        for r in rows(t, "facility_limit_history_20261008.csv"):
            self.hist[(r["booking_entity"], r["facility_id"])].append(
                (dt.datetime.strptime(r["effective_from"], "%Y-%m-%dT%H:%M:%SZ"), float(r["committed_limit"])))
        for v in self.hist.values():
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


def cohort_counts(tab):
    """N, flagged, reaching, flagged and reaching for each closed cohort"""
    out = []
    for c in tab[:4]:
        out.append(dict(N=len(c["M"]), F=len(c["F"]), P=len(c["R"]), TP=len(c["R"] & c["F"])))
    return out


def measures(tab):
    cc = cohort_counts(tab)
    P = sum(c["P"] for c in cc)
    TP = sum(c["TP"] for c in cc)
    NF = sum(c["F"] for c in cc)
    N = sum(c["N"] for c in cc)
    FP = NF - TP
    return dict(hit=TP / NF, capture=TP / P, false_alarm=FP / (N - P), miss=(P - TP) / (N - NF),
                P=P, TP=TP, NF=NF, N=N, FP=FP)


# ------------------------------------------------------------ CRM-07 5.2: the bases and the test
def _lin(x, y, w=None):
    n = len(x)
    w = w or [1.0] * n
    sw = sum(w)
    mx = sum(a * b for a, b in zip(w, x)) / sw
    my = sum(a * b for a, b in zip(w, y)) / sw
    b = sum(wi * (xi - mx) * (yi - my) for wi, xi, yi in zip(w, x, y)) / sum(wi * (xi - mx) ** 2 for wi, xi in zip(w, x))
    return my - b * mx, b


def basis_fit(name, cs):
    """Set a basis from a list of cohorts (dicts N, F, P, TP); return f(N, F) -> (p_flag, p_unflag) or a share."""
    N = sum(c["N"] for c in cs)
    F = sum(c["F"] for c in cs)
    P = sum(c["P"] for c in cs)
    TP = sum(c["TP"] for c in cs)
    if name == "hit_and_miss":
        pf, pu = TP / F, (P - TP) / (N - F)
        return lambda n, f: (pf, pu)
    if name == "one_share":
        s = P / N
        return lambda n, f: (s, s)
    if name == "arrivals_per_flagged":
        r = P / F
        return lambda n, f: (r, 0.0)
    if name == "every_flagged_reaches":
        pu = (P - TP) / (N - F)
        return lambda n, f: (1.0, pu)
    if name in ("capture_false_alarm", "mean_capture_false_alarm"):
        if name == "capture_false_alarm":
            se, fa = TP / P, (F - TP) / (N - P)
        else:
            se = sum(c["TP"] / c["P"] for c in cs) / len(cs)
            fa = sum((c["F"] - c["TP"]) / (c["N"] - c["P"]) for c in cs) / len(cs)

        def g(n, f):
            a = f / n
            s = (a - fa) / (se - fa)
            return se * s / a, (1 - se) * s / (1 - a)
        return g
    if name in ("share_on_flagged_share", "share_on_flagged_share_weighted"):
        x = [c["F"] / c["N"] for c in cs]
        y = [c["P"] / c["N"] for c in cs]
        c0, b = _lin(x, y, [float(c["N"]) for c in cs] if name.endswith("weighted") else None)
        return lambda n, f: ("share", c0 + b * f / n)
    if name == "arrivals_on_flagged_and_book":
        # least squares P = b1 F + b2 N, no intercept
        sff = sum(c["F"] ** 2 for c in cs)
        snn = sum(c["N"] ** 2 for c in cs)
        sfn = sum(c["F"] * c["N"] for c in cs)
        sfp = sum(c["F"] * c["P"] for c in cs)
        snp = sum(c["N"] * c["P"] for c in cs)
        det = sff * snn - sfn ** 2
        b1, b2 = (sfp * snn - snp * sfn) / det, (snp * sff - sfp * sfn) / det
        return lambda n, f: ("share", (b1 * f + b2 * n) / n)
    if name == "hit_and_miss_trended":
        x = [c["F"] / c["N"] for c in cs]
        h0, hb = _lin(x, [c["TP"] / c["F"] for c in cs])
        m0, mb = _lin(x, [(c["P"] - c["TP"]) / (c["N"] - c["F"]) for c in cs])
        return lambda n, f: (h0 + hb * f / n, m0 + mb * f / n)
    if name == "mean_hit_and_miss":
        pf = sum(c["TP"] / c["F"] for c in cs) / len(cs)
        pu = sum((c["P"] - c["TP"]) / (c["N"] - c["F"]) for c in cs) / len(cs)
        return lambda n, f: (pf, pu)
    if name in ("latest_hit_and_miss", "most_stressed_hit_and_miss"):
        c = cs[-1] if name.startswith("latest") else max(cs, key=lambda c: c["P"] / c["N"])
        pf, pu = c["TP"] / c["F"], (c["P"] - c["TP"]) / (c["N"] - c["F"])
        return lambda n, f: (pf, pu)
    raise ValueError(name)


BASES = ["hit_and_miss", "one_share", "arrivals_per_flagged", "every_flagged_reaches", "capture_false_alarm",
         "mean_capture_false_alarm", "share_on_flagged_share", "share_on_flagged_share_weighted",
         "arrivals_on_flagged_and_book", "hit_and_miss_trended", "mean_hit_and_miss", "latest_hit_and_miss",
         "most_stressed_hit_and_miss"]


def predict(fn, n, f):
    p = fn(n, f)
    if p[0] == "share":
        return n * p[1]
    return f * p[0] + (n - f) * p[1]


def basis_test(tab):
    """5.2's test: each closed cohort predicted from the other three taken together; error = largest miss as a
    share of the cohort's actual arrivals. Returns {basis: (misses, error, forward)}."""
    cc = cohort_counts(tab)
    N1, F1 = len(tab[4]["M"]), len(tab[4]["F"])
    out = {}
    for name in BASES:
        miss = []
        for i in range(4):
            fn = basis_fit(name, [c for j, c in enumerate(cc) if j != i])
            miss.append(predict(fn, cc[i]["N"], cc[i]["F"]) / cc[i]["P"] - 1)
        out[name] = (miss, max(abs(x) for x in miss), predict(basis_fit(name, cc), N1, F1))
    return out


def forecast(tab, model=None):
    """The forecast on the basis 5.2's test selects (or on a named basis)."""
    test = basis_test(tab)
    if model is None:
        model = min(test, key=lambda k: test[k][1])
    cc = cohort_counts(tab)
    fwd = tab[4]
    N1, F1 = len(fwd["M"]), len(fwd["F"])
    pf, pu = basis_fit(model, cc)(N1, F1)
    m = measures(tab)
    return dict(model=model, test=test, N1=N1, F1=F1, a1=F1 / N1, p_flag=pf, p_unflag=pu, flagged=F1 * pf,
                unflagged=(N1 - F1) * pu, total=F1 * pf + (N1 - F1) * pu, measures=m)


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


def customer_groups(pk, hz=True):
    cg = {r["customer_id"]: r["group_id"] for r in pk.obl}
    if hz:
        resolve, _ = pk.group_of_key(dt.date(2026, 9, 30))
        for r in pk.obl:
            if not r["group_id"] and r["lei"]:
                cg[r["customer_id"]] = resolve(r["lei"].upper()) or ""
    return cg


def exposures(pk, grain="group", clock="right", hz=True, order="first"):
    date = dt.date(2026, 9, 30)
    cg = customer_groups(pk, hz)
    rows_ = [r for r in pk.fac if d(r["start_date"]) <= date < d(r["final_maturity_date"])]
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
        g = cg.get(r["customer_id"], "")
        if not g:
            continue
        key = (r["booking_entity"], r["facility_id"])
        if grain == "group":
            if (g, key) in counted:
                continue
            counted.add((g, key))
        lim = limit_on_clock(pk, key, float(r["committed_limit"]), clock)
        rate = pk.fx[r["currency"]] if r["currency"] != "GBP" else 1.0
        exp[g] += lim / rate
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
        out.append(dict(band=BANDS[b], groups=len(G), flagged=len(Fg), committed=sum(exp.get(g, 0.0) for g in G),
                        exp_flagged=ef, exp_unflagged=eu, exp_total=ef + eu, exp_exposure=ex))
    return out


def golden(t=TARGET):
    pk = Pack(t)
    tab = pk.cohort_table()
    fc = forecast(tab)
    exp = exposures(pk)
    bt = band_table(tab, fc, exp)
    return dict(pack=pk, tab=tab, fc=fc, exp=exp, bands=bt, call=round(fc["total"]))


# ------------------------------------------------------------ CRM-07 2.2: the ultimate parent is a member
COMMITTED = dict(call=133, flagged=165, apex_only=[6, 5, 3, 5, 6], bands=[
    (201, 475.8, 21.4, 6.5, 69.6), (306, 3016.2, 34.0, 9.8, 411.5), (250, 7153.8, 29.6, 7.9, 1108.6),
    (120, 8213.8, 12.6, 3.9, 1121.5), (36, 6640.9, 6.3, 1.0, 1283.4)])


def check_membership(G, t=TARGET):
    """The amended 2.2 read literally (the ultimate parent, booked customers and GLEIF consolidation members)
    gives the committed figures; the apex-only flags are counted; every apex edge has one reading."""
    import pypdf
    pk, tab = G["pack"], G["tab"]
    std = " ".join("".join(p.extract_text() for p in pypdf.PdfReader(
        os.path.join(t, "early_warning_and_watch_list_standard.pdf")).pages).split())
    assert "A group's members are its ultimate parent, the customers the credit system books to it" in std
    assert len(tab[4]["F"]) == COMMITTED["flagged"] and G["call"] == COMMITTED["call"]
    got = [(r["groups"], round(r["committed"] / 1e6 + 1e-12, 1), round(r["exp_flagged"] + 1e-12, 1),
            round(r["exp_unflagged"] + 1e-12, 1), round(r["exp_exposure"] / 1e6 + 1e-12, 1)) for r in G["bands"]]
    assert got == COMMITTED["bands"], got
    no_apex = pk.cohort_table(apex=False)
    only = [len(a["F"] - b["F"]) for a, b in zip(tab, no_apex)]
    assert only == COMMITTED["apex_only"] and all(not (b["F"] - a["F"]) for a, b in zip(tab, no_apex)), only
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
    for c in G["tab"]:
        print(c["date"], len(c["M"]), len(c["F"]), None if c["R"] is None else (len(c["R"]), len(c["R"] & c["F"])))
    fc = G["fc"]
    m = fc["measures"]
    for k, (miss, err, fw) in sorted(fc["test"].items(), key=lambda kv: kv[1][1]):
        print("%-34s %s  worst %6.2f%%  forward %7.2f" % (k, " ".join("%+6.1f" % (100 * x) for x in miss), 100 * err, fw))
    print("basis used:", fc["model"])
    print("hit %.4f capture %.4f false-alarm %.4f miss %.5f" % (m["hit"], m["capture"], m["false_alarm"], m["miss"]))
    print("forward N %d flagged %d; p_flag %.5f p_unflag %.5f" % (fc["N1"], fc["F1"], fc["p_flag"], fc["p_unflag"]))
    print("caseload %.3f -> %d (flagged %.3f, unflagged %.3f)" % (fc["total"], G["call"], fc["flagged"], fc["unflagged"]))
    for r in G["bands"]:
        print("%-28s groups %4d flagged %3d  committed GBP m %9.3f  exp_flag %7.3f exp_unflag %7.3f  exp_exposure GBP m %8.3f"
              % (r["band"], r["groups"], r["flagged"], r["committed"] / 1e6, r["exp_flagged"], r["exp_unflagged"],
                 r["exp_exposure"] / 1e6))
    print("committed total GBP m %.3f, expected exposure total GBP m %.3f" % (
        sum(r["committed"] for r in G["bands"]) / 1e6, sum(r["exp_exposure"] for r in G["bands"]) / 1e6))
