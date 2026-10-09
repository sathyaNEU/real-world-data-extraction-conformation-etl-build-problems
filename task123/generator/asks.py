"""K1 (government money inside each fall) and K2 (the Trust's own money inside each fall), on any
window, under the golden handling and under every designed mishandling."""
import datetime as dt

from common import fyq, natural_end, SEPT_CENSUS, EXTRACT_DATE
from lines import is_new_form, apt_by_quarter
from screen import eod


def pick_version(W, o, q, cutoff, how="held"):
    book = W["book"]
    if how == "pg" and o.dual:
        lst = book.by_ref.get((o.pg_ref, q), [])
        best = None
        for v in lst:
            if v.accepted <= cutoff:
                best = v
        if best is not None:
            return best
    if how == "delivered":
        cands = [v for v in book.all_by_org.get((o.key, q), []) if v.submitted <= cutoff]
        if cands:
            return max(cands, key=lambda v: (v.submitted, v.no))
    lst = book.by_org.get((o.key, q), [])
    best = None
    for v in lst:
        if v.accepted <= cutoff:
            best = v
    return best


def gov_ytd(W, o, q, cutoff, mapping="correct", vhow="held", comps=False):
    if o.short_form:
        return None
    if comps and not is_new_form(q) and is_new_form(q + 4):
        nv = pick_version(W, o, q + 4, cutoff, vhow)
        if nv is not None:
            return nv.lines["GOV_GRC"][1]
    v = pick_version(W, o, q, cutoff, vhow)
    if v is None:
        return None
    L = v.lines
    if "GOV_GRC" in L:
        return L["GOV_GRC"][0]
    if mapping == "correct":
        return L["GOV_GRT"][0] + L["FEE_SVC_GOV"][0]
    if mapping == "label":
        return L["GOV_GRT"][0]
    if mapping == "over":
        return L["GOV_GRT"][0] + L["FEE_SVC"][0]
    raise ValueError(mapping)


def reg_gov(W, o, q4):
    return W["annual"][(o.key, q4)].lines["gov"]


def gov_quarter(W, o, q, cutoff, q4src, **kw):
    k = fyq(q, o.bal)
    g = gov_ytd(W, o, q, cutoff, **kw)
    if k == 1:
        return g
    b = gov_ytd(W, o, q - 1, cutoff, **kw)
    if b is None:
        return None
    if k == 4 and q4src == "register":
        return reg_gov(W, o, q) - b
    if g is None:
        return None
    return g - b


def k1(W, key, cur_q, prior_q, census, q4src="register", **kw):
    o = W["by"][key]
    if o.short_form:
        return None
    cutoff = eod(census)
    vals = {q: gov_quarter(W, o, q, cutoff, q4src, **kw) for q in cur_q + prior_q}
    if any(v is None for v in vals.values()):
        return None
    return sum(vals[q] for q in prior_q) - sum(vals[q] for q in cur_q)


def apt_series(W, how="value", statuses=("paid",), drop_pg=False):
    key = (how, statuses, drop_pg)
    cache = W.setdefault("_apt_cache", {})
    if key not in cache:
        refs = None
        if drop_pg:
            refs = {}
            for o in W["orgs"]:
                if o.dual:
                    refs[o.key] = {r for r in W["refs_of"][o.key] if r != o.pg_ref}
        cache[key] = apt_by_quarter(W["payments"], W["orgs"], how=how, statuses=statuses,
                                    refs=refs)
    return cache[key]


def memo_quarter(W, o, q, cutoff, run, vhow="held", comps=False):
    """Trust money in quarter q read from the returns' memo where the form carries it, from the
    payment run series `run` where it does not."""
    k = fyq(q, o.bal)

    def ytd(qq):
        if comps and not is_new_form(qq) and is_new_form(qq + 4) and not o.short_form:
            nv = pick_version(W, o, qq + 4, cutoff, vhow)
            if nv is not None and "GRT_NGO_APT" in nv.lines:
                return nv.lines["GRT_NGO_APT"][1]
        if is_new_form(qq) and not o.short_form:
            v = pick_version(W, o, qq, cutoff, vhow)
            return v.lines["GRT_NGO_APT"][0]
        kk = fyq(qq, o.bal)
        return int(sum(run[o.key][qq - kk + 1:qq + 1]))

    if k == 1:
        return ytd(q)
    return ytd(q) - ytd(q - 1)


def k2(W, key, cur_q, prior_q, census, how="value", statuses=("paid",), drop_pg=False,
       memo=None):
    o = W["by"][key]
    s = apt_series(W, how, statuses, drop_pg)
    if memo is not None:
        cutoff = eod(census)
        vals = {q: memo_quarter(W, o, q, cutoff, s, **memo) for q in cur_q + prior_q}
    else:
        vals = {q: int(s[o.key][q]) for q in cur_q + prior_q}
    return sum(vals[q] for q in prior_q) - sum(vals[q] for q in cur_q)


def windows(row):
    e, pe = row["end"], row["pend"]
    return list(range(e - 3, e + 1)), list(range(pe - 7, pe - 3))
