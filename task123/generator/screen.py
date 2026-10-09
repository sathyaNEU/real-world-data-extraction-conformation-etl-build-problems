"""The Steady Ground screen under the standing method (T) and under every rival rule the build
asserts against. Generator-side only; the independent verifier carries its own implementation.
"""
import datetime as dt
from collections import defaultdict

from common import (SPINE_FIRST, EXTRACT_DATE, LINE_PCT, MARCH_CENSUSES, SEPT_CENSUS, qend, fyq,
                    fy_q4, natural_end, strike_rate, offer_for, pct1, FLOOR, CAP)


def eod(d):
    return dt.datetime(d.year, d.month, d.day, 23, 59, 59)


def sod(d):
    return dt.datetime(d.year, d.month, d.day, 0, 0, 0)


class Book:
    def __init__(self, orgs, versions, annual):
        self.orgs = {o.key: o for o in orgs}
        self.annual = annual
        self.by_org = defaultdict(list)
        self.by_ref = defaultdict(list)
        self.all_by_org = defaultdict(list)
        for v in versions:
            self.all_by_org[(v.org, v.q)].append(v)
            if v.status == "accepted":
                self.by_org[(v.org, v.q)].append(v)
                self.by_ref[(v.ref, v.q)].append(v)
        for lst in list(self.by_org.values()) + list(self.by_ref.values()):
            lst.sort(key=lambda v: v.accepted)
        self.ref_org = {}
        for o in orgs:
            self.ref_org[o.og_ref] = o.key
            if o.dual:
                self.ref_org[o.pg_ref] = o.key

    def ytd(self, unit_key, q, cutoff, unit="org", basis="held"):
        lst = (self.by_org if unit == "org" else self.by_ref).get((unit_key, q), [])
        best = None
        for v in lst:
            if v.accepted <= cutoff:
                if basis == "first" and v.no != 1:
                    continue
                best = v
        return None if best is None else best.ytd

    def received(self, org, q4, cutoff_date, inclusive=True):
        ar = self.annual.get((org, q4))
        if ar is None or ar.received is None:
            return False
        return ar.received <= cutoff_date if inclusive else ar.received < cutoff_date

    def annual_total(self, org, q4):
        return self.annual[(org, q4)].total


DEFAULT = dict(unit="org", basis="held", stepback="T", q4src="register", reg_at="census",
               inclusive=True, prior="stepped", step_bal=None, drop_unfiled=False, require8=True,
               latest_for_held=False)


def current_at(o, c, unit_kind="op"):
    if unit_kind == "op":
        return o.og_start <= c <= o.og_end
    return o.pg_start <= c <= o.pg_end


def units_for(book, c, unit):
    out = []
    for o in book.orgs.values():
        if not current_at(o, c, "op"):
            continue
        if unit == "org":
            out.append((o.key, o.key, "op"))
        elif unit == "op":
            out.append((o.og_ref, o.key, "op"))
        else:
            out.append((o.og_ref, o.key, "op"))
            if o.dual and current_at(o, c, "pg"):
                out.append((o.pg_ref, o.key, "pg"))
    return out


def row_for(book, c, ukey, okey, opt):
    o = book.orgs[okey]
    unit = opt["unit"]
    cutoff = eod(EXTRACT_DATE) if opt["basis"] == "latest" else eod(c)
    reg_date = EXTRACT_DATE if opt["reg_at"] == "extract" else c
    n_end = natural_end(c)
    step_ok = opt["step_bal"] is None or o.bal in opt["step_bal"]

    def admissible(q):
        if fyq(q, o.bal) != 4:
            return True
        sb = opt["stepback"]
        if not step_ok or sb == "none":
            return True
        if sb == "T":
            return book.received(okey, q, reg_date, opt["inclusive"])
        if sb == "overdue":
            if book.received(okey, q, reg_date, True):
                return True
            return c <= due_date(o, q)
        if sb == "dec":
            return not (o.bal == 12 and c.month == 3 and q == n_end)
        if sb == "amended":
            # step back where the fourth-quarter return carries an accepted version after the census
            lst = book.by_org.get((okey, q), [])
            return not any(v.accepted > eod(c) and v.no > 1 for v in lst)
        raise ValueError(sb)

    e = n_end
    while not all(admissible(q) for q in range(e - 3, e + 1)):
        e -= 1
        if e < n_end - 8:
            return None
    if opt["drop_unfiled"] and e != n_end:
        return None
    cur_q = list(range(e - 3, e + 1))
    pe = e if opt["prior"] == "stepped" else n_end
    prior_q = list(range(pe - 7, pe - 3))

    bunit = "ref" if unit in ("ref", "op") else "org"

    def ytd(q):
        return book.ytd(ukey, q, cutoff, bunit, opt["basis"] if opt["basis"] == "first" else "held")

    def disc(q):
        k = fyq(q, o.bal)
        y = ytd(q)
        if y is None:
            return None
        if k == 1:
            base = 0
        else:
            base = ytd(q - 1)
            if base is None:
                return None
        if k == 4 and opt["q4src"] == "register" and book.received(okey, q, reg_date,
                                                                    opt["inclusive"]):
            return book.annual_total(okey, q) - base
        return y - base

    vals = {}
    for q in sorted(set(cur_q + prior_q)):
        v = disc(q) if q >= SPINE_FIRST else None
        if v is None:
            if opt["require8"]:
                return None
            v = 0
        vals[q] = v
    if sum(vals[q] for q in prior_q) <= 0:
        return None
    cur = sum(vals[q] for q in cur_q)
    prior = sum(vals[q] for q in prior_q)
    fall = prior - cur
    pct = 100.0 * fall / prior
    return {"unit": ukey, "org": okey, "cur": cur, "prior": prior, "fall": fall, "pct": pct,
            "end": e, "pend": pe}


def due_date(o, q4):
    fye = qend(q4)
    if o.bal == 3:
        return dt.date(fye.year, 9, 30)
    if o.bal == 6:
        return dt.date(fye.year, 12, 31)
    return dt.date(fye.year + 1, 6, 30)


def screen(book, c, pot, **kw):
    opt = dict(DEFAULT)
    opt.update(kw)
    rows = []
    for ukey, okey, _ in units_for(book, c, opt["unit"]):
        r = row_for(book, c, ukey, okey, opt)
        if r is not None:
            rows.append(r)
    elig = [r for r in rows if r["pct"] >= LINE_PCT]
    rate, offs, total = strike_rate([r["fall"] for r in elig], pot)
    for r in rows:
        r["offer"] = 0
    for r, off in zip(elig, offs):
        r["offer"] = off
    rows.sort(key=lambda r: (-r["fall"], r["unit"]))
    return {"rows": rows, "rate": rate, "total": total, "pot": pot, "census": c,
            "offered": sorted({r["org"] for r in elig}), "n_offers": len(elig)}


def filed_year_screen(book, c, pot, reg_at="census"):
    """R0: twelve-month income is the latest annual return on the register, against the one before."""
    rows = []
    reg_date = EXTRACT_DATE if reg_at == "extract" else c
    for o in book.orgs.values():
        if not current_at(o, c, "op"):
            continue
        recs = sorted(q4 for (k, q4), ar in book.annual.items()
                      if k == o.key and ar.received is not None and ar.received <= reg_date)
        if len(recs) < 2:
            continue
        q_cur, q_pri = recs[-1], recs[-2]
        if q_cur - q_pri != 4:
            continue
        # scope: the round rules' eight quarters of returns on the natural window
        cur = book.annual_total(o.key, q_cur)
        prior = book.annual_total(o.key, q_pri)
        fall = prior - cur
        rows.append({"unit": o.key, "org": o.key, "cur": cur, "prior": prior, "fall": fall,
                     "pct": 100.0 * fall / prior, "end": q_cur, "pend": q_pri})
    elig = [r for r in rows if r["pct"] >= LINE_PCT]
    rate, offs, total = strike_rate([r["fall"] for r in elig], pot)
    for r in rows:
        r["offer"] = 0
    for r, off in zip(elig, offs):
        r["offer"] = off
    rows.sort(key=lambda r: (-r["fall"], r["unit"]))
    return {"rows": rows, "rate": rate, "total": total, "pot": pot, "census": c,
            "offered": sorted({r["org"] for r in elig}), "n_offers": len(elig)}


def published_row(r):
    return (r["cur"], r["prior"], r["fall"], pct1(r["pct"]), r["offer"])


def replay(pub, riv):
    """Rows, offers and rate a rival gives back against a published run (by organisation)."""
    pub_rows = {r["org"]: published_row(r) for r in pub["rows"]}
    riv_rows = defaultdict(list)
    for r in riv["rows"]:
        riv_rows[r["org"]].append(published_row(r))
    rows_back = sum(1 for k, v in pub_rows.items() if v in riv_rows.get(k, []))
    missed = sorted(k for k, v in pub_rows.items() if v not in riv_rows.get(k, []))
    extra = sorted(k for k in riv_rows if k not in pub_rows)
    pub_off = {r["org"]: r["offer"] for r in pub["rows"] if r["offer"]}
    riv_off = defaultdict(list)
    for r in riv["rows"]:
        if r["offer"]:
            riv_off[r["org"]].append(r["offer"])
    offers_back = sum(1 for k, v in pub_off.items() if riv_off.get(k) == [v])
    offers_all = (offers_back == len(pub_off) and sum(len(v) for v in riv_off.values()) == len(pub_off))
    return {"rows_back": rows_back, "n_pub": len(pub_rows), "n_riv": len(riv["rows"]),
            "missed": missed, "extra": extra, "offers_back": offers_back,
            "offers_all": offers_all, "rate_ok": riv["rate"] == pub["rate"],
            "count_ok": len(riv["rows"]) == len(pub_rows)}
