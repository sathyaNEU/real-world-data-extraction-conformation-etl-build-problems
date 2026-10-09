"""Trust payments (operating grants, project grants, Steady Ground instalments) and the income-line
layer of every portal return version, including the 2024 form change and the comparative column.
"""
import datetime as dt

import numpy as np

from common import NQ, FORM_CHANGE_Q, fyq, pay_date, month_add, quarter_of_date
from world import rng_for

RUN_START = dt.date(2018, 7, 1)
RUN_END = dt.date(2026, 9, 30)

NONAPT = ["gov_grant", "gov_contract", "trading", "donations", "other_grants", "investment",
          "other"]
OLD_CODES = ["TOT_INC", "GOV_GRT", "FEE_SVC", "FEE_SVC_GOV", "DON_BEQ", "GRT_OTH", "INV_INC",
             "OTH_INC"]
NEW_CODES = ["TOT_REV", "GOV_GRC", "TRD_SAL", "DON_BEQ", "GRT_NGO", "GRT_NGO_APT", "INV_REV",
             "OTH_REV"]
OLD_SHORT = ["TOT_INC", "DON_BEQ", "OTH_INC"]
NEW_SHORT = ["TOT_REV", "DON_BEQ", "OTH_REV"]
MEMO_CODES = {"FEE_SVC_GOV", "GRT_NGO_APT"}
TOTAL_CODES = {"TOT_INC", "TOT_REV"}


def is_new_form(q):
    return q >= FORM_CHANGE_Q


# ----------------------------------------------------------------------------- payments

def grant_terms(o):
    """Operating grant terms: three-yearly from the start, each at its own annual level."""
    r = rng_for("grant", o.key)
    share = float(r.uniform(0.06, 0.12))
    a = min(max(12_000, int(round(o.income * share / 1200.0)) * 1200), 360_000)
    terms = []
    s = o.og_start
    while s <= o.og_end:
        e = dt.date(s.year + 3, s.month, 1)
        terms.append([s, e, 0])
        s = e
    early = [i for i, t in enumerate(terms) if t[0] <= dt.date(2024, 6, 30)]
    k24 = max(early) if early else 0
    terms[k24][2] = a
    for i in range(k24 + 1, len(terms)):
        terms[i][2] = int(round(terms[i - 1][2] * float(r.uniform(0.99, 1.12)) / 1200.0)) * 1200
    for i in range(k24 - 1, -1, -1):
        terms[i][2] = max(6000, int(round(terms[i + 1][2] / float(r.uniform(1.0, 1.10))
                                          / 1200.0)) * 1200)
    return terms


def months(start, last):
    y, m = start.year, start.month
    while (y, m) <= (last.year, last.month):
        yield y, m
        y, m = month_add(y, m, 1)


def level_at(terms, y, m):
    d = dt.date(y, m, 1)
    for s, e, lv in terms:
        if s <= d < e:
            return lv
    return terms[-1][2]


def build_payments(orgs, corpus_offers, reissues):
    """Every payment the Trust made to every grantee. corpus_offers: {round year: {org: offer}}"""
    by = {o.key: o for o in orgs}
    terms_by = {o.key: grant_terms(o) for o in orgs}
    if "TA" in by and "TB" in by:
        terms_by["TA"] = [list(t) for t in terms_by["TB"]]
    pg_level = {}
    pays = []
    for o in sorted(orgs, key=lambda o: o.key):
        terms = terms_by[o.key]
        for y, m in months(o.og_start, o.og_end):
            py, pm = month_add(y, m, -1)
            pays.append(dict(org=o.key, ref=o.og_ref, prog="OG", inst_for=(y, m),
                             value=pay_date(py, pm), amount=level_at(terms, y, m) // 12,
                             status="paid"))
        if o.dual:
            r = rng_for("pg", o.key)
            pa = max(6000, int(round(o.income * float(r.uniform(0.025, 0.05)) / 1200.0)) * 1200)
            pterms = []
            s = o.pg_start
            lv = pa
            while s <= o.pg_end:
                e = dt.date(s.year + 3, s.month, 1)
                pterms.append([s, e, lv])
                step = 1.4 if o.key == "F3" else float(r.uniform(0.92, 1.15))
                lv = int(round(lv * step / 1200.0)) * 1200
                s = e
            pg_level[o.key] = pterms
            for y, m in months(o.pg_start, o.pg_end):
                py, pm = month_add(y, m, -1)
                pays.append(dict(org=o.key, ref=o.pg_ref, prog="PG", inst_for=(y, m),
                                 value=pay_date(py, pm), amount=level_at(pterms, y, m) // 12,
                                 status="paid"))
    sgf_refs = {}
    for ry in sorted(corpus_offers):
        for seq, key in enumerate(sorted(corpus_offers[ry], key=lambda k: by[k].cc), start=1):
            offer = corpus_offers[ry][key]
            ref = f"SGF-{ry}-{seq:02d}"
            sgf_refs[(ry, key)] = ref
            base = int(round(offer / 12.0))
            amts = [base] * 11 + [offer - 11 * base]
            for k in range(12):
                y, m = month_add(ry, 6, k)
                py, pm = month_add(y, m, -1)
                pays.append(dict(org=key, ref=ref, prog="SGF", inst_for=(y, m),
                                 value=pay_date(py, pm), amount=amts[k], status="paid"))
    for key, vd in reissues:
        hit = [p for p in pays if p["org"] == key and p["value"] == vd and p["prog"] == "OG"]
        assert len(hit) == 1, (key, vd, len(hit))
        p = hit[0]
        p["status"] = "returned"
        rd = vd + dt.timedelta(days=6)
        while rd.weekday() >= 5:
            rd += dt.timedelta(days=1)
        assert quarter_of_date(rd) == quarter_of_date(vd)
        pays.append(dict(org=key, ref=p["ref"], prog="OG", inst_for=p["inst_for"], value=rd,
                         amount=p["amount"], status="paid", reissue=True))
    pays.sort(key=lambda p: (p["value"], by[p["org"]].cc, p["ref"], p["inst_for"]))
    pid = 304_117
    for p in pays:
        pid += int(rng_for("pid", p["org"], p["inst_for"][0], p["inst_for"][1]).integers(1, 4))
        p["id"] = f"PR{pid}"
    ret = {(p["org"], p["inst_for"], p["ref"]): p["id"] for p in pays if p["status"] == "returned"}
    for p in pays:
        if p.get("reissue"):
            p["reissue_of"] = ret[(p["org"], p["inst_for"], p["ref"])]
    return pays, terms_by, sgf_refs, pg_level


def apt_by_quarter(pays, orgs, how="value", statuses=("paid",), refs=None):
    """Trust money each grantee received, by quarter. how='value' is the quarter the payment reached
    its account; how='for' is the quarter of the month the instalment was for."""
    out = {o.key: np.zeros(NQ, dtype=np.int64) for o in orgs}
    for p in pays:
        if p["status"] not in statuses:
            continue
        if refs is not None and p["ref"] not in refs.get(p["org"], {p["ref"]}):
            continue
        if how == "value":
            q = quarter_of_date(p["value"])
        elif how == "for":
            y, m = p["inst_for"]
            q = quarter_of_date(dt.date(y, m, 1))
        elif how == "transit":
            # over-cleaned: payments in the last ten days of a quarter dropped as in transit
            from common import qend
            q = quarter_of_date(p["value"])
            if 0 <= q < NQ and (qend(q) - p["value"]).days <= 10:
                continue
        else:
            raise ValueError(how)
        if 0 <= q < NQ:
            out[p["org"]][q] += p["amount"]
    return out


# ----------------------------------------------------------------------------- line split

MIX = {"gov_grant": 0.17, "gov_contract": 0.22, "trading": 0.18, "donations": 0.19,
       "other_grants": 0.13, "investment": 0.04, "other": 0.07}
DROP_MIX = {
    "decoy": {"gov_contract": 0.55, "gov_grant": 0.45},
    "decoy_soft": {"gov_contract": 0.5, "gov_grant": 0.3, "donations": 0.2},
    "marker": {"gov_contract": 0.45, "trading": 0.25, "donations": 0.30},
    "answer": {"gov_contract": 0.40, "donations": 0.30, "trading": 0.30},
    "common": {"gov_contract": 0.35, "gov_grant": 0.25, "trading": 0.40},
    "filed_offer": {"gov_contract": 0.30, "gov_grant": 0.20, "trading": 0.30, "donations": 0.20},
    "default": {"trading": 0.45, "donations": 0.30, "gov_contract": 0.25},
}


def alloc(total, weights):
    """Split a whole-dollar total over weights, largest remainder, exact."""
    keys = list(weights)
    w = np.array([max(weights[k], 0.0) for k in keys], dtype=float)
    if w.sum() <= 0:
        w = np.ones(len(keys))
    raw = total * w / w.sum()
    base = np.floor(raw).astype(np.int64)
    rem = int(total - base.sum())
    order = np.argsort(-(raw - base), kind="stable")
    for j in range(rem):
        base[order[j % len(keys)]] += 1
    return {k: int(v) for k, v in zip(keys, base)}


def true_lines(orgs, tot, apt, ref_tot):
    """Discrete quarterly income by true line, summing to the total each quarter."""
    out = {}
    for o in orgs:
        r = rng_for("mix", o.key)
        mix = {k: max(0.005, v * float(r.lognormal(0, 0.35))) for k, v in MIX.items()}
        if o.role in ("decoy", "decoy_soft", "answer", "marker", "common", "filed_offer"):
            mix["gov_contract"] = max(mix["gov_contract"], 0.20)
        phase = int(r.integers(0, 4))
        lump = np.roll(np.array([1.75, 0.45, 1.40, 0.40]), phase)
        dm = DROP_MIX.get(o.role, DROP_MIX["default"])
        L = {}
        for q in range(NQ):
            t = int(tot[o.key][q])
            a = int(apt[o.key][q])
            ref = int(ref_tot[o.key][q])
            w = dict(mix)
            w["gov_grant"] *= lump[q % 4]
            w["gov_contract"] *= float(r.uniform(0.75, 1.25))
            w["donations"] *= 1.25 if q % 4 == 2 else 0.92
            w["trading"] *= float(r.uniform(0.9, 1.1))
            base_nonapt = ref - a
            if base_nonapt <= 0:
                raise AssertionError(f"Trust money exceeds income: {o.key} q{q}")
            lines = alloc(base_nonapt, w)
            drop = ref - t
            if drop != 0:
                part = alloc(abs(drop), dm)
                for k, v in part.items():
                    lines[k] -= v if drop > 0 else -v
                # move any shortfall to the largest line
                for k in list(lines):
                    if lines[k] < 0:
                        big = max(lines, key=lambda x: lines[x])
                        lines[big] += lines[k]
                        lines[k] = 0
            lines["apt"] = a
            assert sum(lines.values()) == t, (o.key, q)
            assert all(v >= 0 for v in lines.values()), (o.key, q, lines)
            L[q] = lines
        out[o.key] = L
    return out


def ytd_lines(L, o, q):
    k = fyq(q, o.bal)
    acc = {}
    for qq in range(q - k + 1, q + 1):
        src = L[qq] if qq >= 0 else L[qq + 4]   # before the modelled span: the next year's quarter
        for kk, v in src.items():
            acc[kk] = acc.get(kk, 0) + v
    return acc


def form_lines(true_ytd, q, short):
    """Map true YTD lines onto the form in force for quarter q."""
    t = true_ytd
    total = sum(v for k, v in t.items())
    if is_new_form(q):
        if short:
            return {"TOT_REV": total, "DON_BEQ": t["donations"], "OTH_REV": total - t["donations"]}
        return {"TOT_REV": total, "GOV_GRC": t["gov_grant"] + t["gov_contract"],
                "TRD_SAL": t["trading"], "DON_BEQ": t["donations"],
                "GRT_NGO": t["other_grants"] + t["apt"], "GRT_NGO_APT": t["apt"],
                "INV_REV": t["investment"], "OTH_REV": t["other"]}
    if short:
        return {"TOT_INC": total, "DON_BEQ": t["donations"], "OTH_INC": total - t["donations"]}
    return {"TOT_INC": total, "GOV_GRT": t["gov_grant"],
            "FEE_SVC": t["trading"] + t["gov_contract"], "FEE_SVC_GOV": t["gov_contract"],
            "DON_BEQ": t["donations"], "GRT_OTH": t["other_grants"] + t["apt"],
            "INV_INC": t["investment"], "OTH_INC": t["other"]}


# ----------------------------------------------------------------------------- version lines

def spread(true_ytd, delta):
    """Spread a total-income difference over the non-Trust lines, in proportion, exactly."""
    w = {k: float(true_ytd[k]) for k in NONAPT}
    if delta >= 0:
        add = alloc(delta, w)
        return {k: true_ytd.get(k, 0) + add.get(k, 0) for k in true_ytd}
    sub = alloc(-delta, w)
    out = {k: true_ytd.get(k, 0) - sub.get(k, 0) for k in true_ytd}
    assert all(v >= 0 for v in out.values())
    return out


def held_version(book, org, q, cutoff):
    lst = book.by_org.get((org, q), [])
    best = None
    for v in lst:
        if v.accepted <= cutoff:
            best = v
    return best


def attach_lines(W):
    """Give every version its year-to-date lines and its prior-year comparative column."""
    orgs, book, L = W["orgs"], W["book"], W["true_lines"]
    by = W["by"]
    vs = sorted(W["versions"], key=lambda v: (v.q, v.submitted, v.no))
    for v in vs:
        o = by[v.org]
        k = fyq(v.q, o.bal)
        t_ytd = ytd_lines(L[o.key], o, v.q)
        delta = v.ytd - sum(t_ytd.values())
        if delta and v.err_line is not None and t_ytd[v.err_line] + delta >= 0:
            adj = dict(t_ytd)
            adj[v.err_line] += delta
        elif delta and v.err_line is not None:
            adj = dict(t_ytd)
            rest = delta + adj[v.err_line]
            adj[v.err_line] = 0
            adj = spread(adj, rest)
        else:
            adj = spread(t_ytd, delta) if delta else dict(t_ytd)
        memo_adj = 0
        for line, amt in v.shift.items():
            if line == "apt_memo":
                memo_adj += amt
            else:
                adj[line] += amt
        assert all(x >= 0 for x in adj.values()), (v.org, v.q, v.no, adj)
        cur = form_lines(adj, v.q, o.short_form)
        if memo_adj and "GRT_NGO_APT" in cur:
            cur["GRT_NGO_APT"] += memo_adj
        # prior-year comparative, as the grantee held it when filing
        pq = v.q - 4
        hv = held_version(book, o.key, pq, v.submitted) if pq >= 5 else None
        if hv is not None and hv.lines is not None:
            py_total = hv.ytd
            py_src = {c: a for c, (a, _) in hv.lines.items()}
        else:
            ty = ytd_lines(L[o.key], o, pq)
            py_total = sum(ty.values())
            py_src = form_lines(ty, pq, o.short_form)
        if is_new_form(v.q) and not is_new_form(pq):
            # re-presented under the new lines in this year's proportions
            if o.short_form:
                py = {"TOT_REV": py_total, "DON_BEQ": py_src["DON_BEQ"],
                      "OTH_REV": py_total - py_src["DON_BEQ"]}
            else:
                shares = {c: cur[c] for c in NEW_CODES if c not in TOTAL_CODES and c not in MEMO_CODES}
                py = alloc(py_total, shares)
                py["TOT_REV"] = py_total
                apt_share = cur["GRT_NGO_APT"] / cur["TOT_REV"] if cur["TOT_REV"] else 0.0
                py["GRT_NGO_APT"] = int(round(py_total * apt_share))
                py["GRT_NGO_APT"] = min(py["GRT_NGO_APT"], py["GRT_NGO"])
        else:
            py = dict(py_src)
            py[("TOT_REV" if is_new_form(v.q) else "TOT_INC")] = py_total
        v.lines = {c: (cur[c], py.get(c, 0)) for c in cur}
        v.py_total = py_total
    return W
