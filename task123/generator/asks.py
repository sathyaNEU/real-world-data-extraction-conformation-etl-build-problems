"""K1 (government money inside each fall) and K2 (the Trust's own money inside each fall), on any
window, under the golden handling and under every designed mishandling.

Hardening loop 2: government money also reached grantees through the Trust. From the instalment for
January 2025 to the instalment for March 2026 the Trust paid central government's co-funding with some
grantees' operating instalments (the grants register's Variations sheet records it). Grantees report the
whole instalment as money received from the Trust, so the co-funding is in no government line and in the
register's government figure for no year, and the Trust memo ties to the payment run with it inside. The
golden counts it as government money (K1) by the quarter it reached the grantee, and takes it out of the
Trust's own money (K2)."""
import datetime as dt

from common import fyq, natural_end, SEPT_CENSUS, EXTRACT_DATE, fpos, is_final, quarter_of_date, NQ
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
    """Government money, year to date. GOV_GRT is reissued on the December 2024 form: government grants
    on QFR-16 (contracts sit in FEE_SVC with the FEE_SVC_GOV memo), grants and contracts on QFR-24."""
    if o.short_form:
        return None
    if comps and not is_new_form(q) and is_new_form(q + 4):
        nv = pick_version(W, o, q + 4, cutoff, vhow)
        if nv is not None:
            return nv.lines["GOV_GRT"][1]
    v = pick_version(W, o, q, cutoff, vhow)
    if v is None:
        return None
    L = v.lines
    if is_new_form(q):
        return L["GOV_GRT"][0]
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
    k = fpos(o, q)
    g = gov_ytd(W, o, q, cutoff, **kw)
    if k == 1:
        return g
    b = gov_ytd(W, o, q - 1, cutoff, **kw)
    if b is None:
        return None
    if is_final(o, q) and q4src == "register":
        return reg_gov(W, o, q) - b
    if g is None:
        return None
    return g - b


def cofund_series(W, how="value", statuses=("paid",)):
    """Government co-funding the Trust paid with operating instalments, by quarter. The golden (how='value')
    counts what each payment actually carried (three months' co-funding on the first instalment of each
    quarter, hardening loop 3) in the quarter the payment reached the grantee; how='for' counts it in the
    quarter of the month the instalment was for. The two twelfths readings take a twelfth of the annual
    co-funding (the Variations sheet's figure) on every instalment for January 2025 to March 2026, by
    value date ('twelfths', the path solver round 3 took) or by instalment month ('twelfths_for')."""
    key = ("cofund", how, statuses)
    cache = W.setdefault("_apt_cache", {})
    if key not in cache:
        from lines import cofunded_month
        by = W["by"]
        out = {o.key: [0] * NQ for o in W["orgs"]}
        for p in W["payments"]:
            if p["status"] not in statuses or p["prog"] != "OG":
                continue
            y, m = p["inst_for"]
            if how in ("twelfths", "twelfths_for"):
                co = by[p["org"]].cofund if cofunded_month(y, m) else 0
            else:
                co = p.get("cofund", 0)
            if not co:
                continue
            if how in ("for", "twelfths_for"):
                q = quarter_of_date(dt.date(y, m, 1))
            else:
                q = quarter_of_date(p["value"])
            if 0 <= q < NQ:
                out[p["org"]][q] += co
        cache[key] = out
    return cache[key]


def k1(W, key, cur_q, prior_q, census, q4src="register", cofund="value", **kw):
    """Government money inside the fall: the government lines on the returns (QFR-16 grants plus the
    contracts memo, QFR-24 grants and contracts; a year's final quarter from the register's figure less
    the nine-month year to date), plus the government co-funding the Trust passed on (cofund=None leaves
    it out, 'for' counts it by instalment month)."""
    o = W["by"][key]
    if o.short_form:
        return None
    cutoff = eod(census)
    vals = {q: gov_quarter(W, o, q, cutoff, q4src, **kw) for q in cur_q + prior_q}
    if any(v is None for v in vals.values()):
        return None
    out = sum(vals[q] for q in prior_q) - sum(vals[q] for q in cur_q)
    if cofund:
        cs = cofund_series(W, cofund)[key]
        out += sum(cs[q] for q in prior_q) - sum(cs[q] for q in cur_q)
    return out


def apt_series(W, how="value", statuses=("paid",), drop_pg=False, progs=("OG", "PG", "SGF")):
    """Trust money by quarter. The golden counts every programme by the quarter the money reached the
    grantee: operating and project grants from the payment run, Steady Ground instalments rebuilt from
    the offers sheet and rule 7 (they are paid from the Fund's own account and appear in no run)."""
    key = (how, statuses, drop_pg, progs)
    cache = W.setdefault("_apt_cache", {})
    if key not in cache:
        refs = None
        if drop_pg:
            refs = {}
            for o in W["orgs"]:
                if o.dual:
                    refs[o.key] = {r for r in W["refs_of"][o.key] if r != o.pg_ref}
        cache[key] = apt_by_quarter(W["payments"], W["orgs"], how=how, statuses=statuses,
                                    refs=refs, progs=progs)
    return cache[key]


def memo_quarter(W, o, q, cutoff, run, vhow="held", comps=False):
    """Trust money in quarter q read from the returns' memo where the form carries it, from the
    payment run series `run` where it does not."""
    k = fpos(o, q)

    def ytd(qq):
        if comps and not is_new_form(qq) and is_new_form(qq + 4) and not o.short_form:
            nv = pick_version(W, o, qq + 4, cutoff, vhow)
            if nv is not None and "GRT_NGO_APT" in nv.lines:
                return nv.lines["GRT_NGO_APT"][1]
        if is_new_form(qq) and not o.short_form:
            v = pick_version(W, o, qq, cutoff, vhow)
            return v.lines["GRT_NGO_APT"][0]
        kk = fpos(o, qq)
        return int(sum(run[o.key][qq - kk + 1:qq + 1]))

    if k == 1:
        return ytd(q)
    return ytd(q) - ytd(q - 1)


def k2(W, key, cur_q, prior_q, census, how="value", statuses=("paid",), drop_pg=False,
       memo=None, progs=("OG", "PG", "SGF"), cofund_out=True, cofund_how=None):
    """The Trust's own money inside the fall: operating and project grants from the payment run and the
    Steady Ground instalments rebuilt from the offers sheet, by the quarter the money reached the
    grantee, less the government co-funding the run carries (cofund_out=False leaves it in)."""
    o = W["by"][key]
    s = apt_series(W, how, statuses, drop_pg, progs)
    if memo is not None:
        cutoff = eod(census)
        vals = {q: memo_quarter(W, o, q, cutoff, s, **memo) for q in cur_q + prior_q}
    else:
        vals = {q: int(s[o.key][q]) for q in cur_q + prior_q}
    out = sum(vals[q] for q in prior_q) - sum(vals[q] for q in cur_q)
    if cofund_out and "OG" in progs:
        cs = cofund_series(W, cofund_how or (how if how in ("value", "for") else "value"), statuses)[key]
        if how == "transit":
            cs = transit_cofund(W, key)
        out -= sum(cs[q] for q in prior_q) - sum(cs[q] for q in cur_q)
    return out


def transit_cofund(W, key):
    """The co-funding under the ten-day transit stop (payments in a quarter's last ten days dropped)."""
    from common import qend
    out = [0] * NQ
    for p in W["payments"]:
        if p["org"] != key or not p.get("cofund") or p["status"] != "paid":
            continue
        q = quarter_of_date(p["value"])
        if 0 <= q < NQ and (qend(q) - p["value"]).days > 10:
            out[q] += p["cofund"]
    return out


def windows(row):
    e, pe = row["end"], row["pend"]
    return list(range(e - 3, e + 1)), list(range(pe - 7, pe - 3))
