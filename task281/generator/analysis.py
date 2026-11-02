"""Every graded figure and every rung, computed from the shipped bundle under target/ and nothing else."""
import bisect
import collections
import datetime as dt
import os
import re
from zoneinfo import ZoneInfo

import openpyxl

import io_util as IO
import pack

UK = ZoneInfo("Europe/London")
UTC = dt.timezone.utc
FUND = 180000
WIN = (dt.date(2026, 1, 12), dt.date(2026, 4, 26))
GRACE = 14.0
CAP = 84.0
FAC_ORDER = ["AHU", "SSC", "BUS", "LAW", "SAE", "LSC", "MED", "HSC"]
FAC_NAME = {"Arts and Humanities": "AHU", "Social Sciences": "SSC", "Ardmuir Business School": "BUS", "Law": "LAW",
            "Science and Engineering": "SAE", "Life Sciences": "LSC", "Medicine and Dentistry": "MED",
            "Health Sciences": "HSC"}

_CACHE = {}


def parse_ts(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC) if s else None


def uk_date(t):
    return t.astimezone(UK).date()


def days(a, b):
    return (b - a).total_seconds() / 86400.0


def hold_weeks(w):
    return max(0.0, min(w, CAP) - GRACE) / 7.0


class D:
    pass


def load(target):
    if target in _CACHE:
        return _CACHE[target]
    d = D()
    F = pack.FILES
    h, rows = IO.read_csv(os.path.join(target, F["holds"]))
    ix = {c: i for i, c in enumerate(h)}
    d.holds = []
    for r in rows:
        d.holds.append(dict(id=r[ix["hold_id"]], title=r[ix["title_id"]], patron=r[ix["patron_id"]],
                            ptype=r[ix["patron_type"]], dept=r[ix["department_code"]],
                            placed=parse_ts(r[ix["placed_at"]]), status=r[ix["status"]],
                            changed=parse_ts(r[ix["status_changed_at"]]), offered=parse_ts(r[ix["offer_made_at"]]),
                            expires=parse_ts(r[ix["offer_expires_at"]]), checkout=r[ix["checkout_id"]]))
    h, rows = IO.read_csv(os.path.join(target, F["loans"]))
    ix = {c: i for i, c in enumerate(h)}
    d.loans = [dict(id=r[ix["checkout_id"]], title=r[ix["title_id"]], patron=r[ix["patron_id"]],
                    start=parse_ts(r[ix["checked_out_at"]]), days=int(r[ix["loan_days"]]), due=parse_ts(r[ix["due_at"]]),
                    ended=parse_ts(r[ix["ended_at"]]), reason=r[ix["end_reason"]]) for r in rows]
    # Schedule 1 and 2 of the Court's terms
    txt = IO.pdf_text(os.path.join(target, F["terms"]))
    d.terms_text = txt
    d.school_fac = {}
    for name, code in FAC_NAME.items():
        pass
    lines = txt.split("\n")
    flat = " ".join(lines)
    for name, code in sorted(FAC_NAME.items(), key=lambda x: -len(x[0])):
        pass
    # every "School name (CODE)" pair, assigned to the faculty whose row it sits in
    sched1 = flat.split("Schedule 1. Faculties from 1 August 2026")[1].split("Schedule 2.")[0]
    pos = []
    for name, code in FAC_NAME.items():
        for m in re.finditer(re.escape(name) + r"(?=\s)", sched1):
            pos.append((m.start(), code))
    pos.sort()
    for m in re.finditer(r"\(([A-Z]{4})\)", sched1):
        owner = [c for p, c in pos if p < m.start()]
        d.school_fac[m.group(1)] = owner[-1]
    sched2 = flat.split("Schedule 2. Course texts fund codes")[1]
    d.fund_fac = {}
    for m in re.finditer(r"(CT-[A-Z]{2,4})\s", sched2):
        code = m.group(1)
        after = sched2[m.end():m.end() + 160]
        if code == "CT-CORE":
            continue
        cands = [(after.rfind(n), c) for n, c in FAC_NAME.items() if n in after]
        if code[3:] in FAC_ORDER:
            d.fund_fac[code] = code[3:]
        else:
            # the last faculty named on the row is the faculty from 1 August 2026
            best = max((after.find(n) + len(n), c) for n, c in FAC_NAME.items() if n in after.split("CT-")[0])
            d.fund_fac[code] = best[1]
    _CACHE[target] = d
    return d


# ------------------------------------------------------------------ the main call
def call_population(d):
    """holds a student placed in the window (UK dates), with the faculty they count for"""
    out = []
    for h in d.holds:
        if h["ptype"] == "Staff":
            continue
        ld = uk_date(h["placed"])
        if not (WIN[0] <= ld <= WIN[1]):
            continue
        school = h["dept"].split("-")[-1].upper()
        out.append((h, d.school_fac[school]))
    return out


def free_events(d):
    """per title, every instant a copy came free: a checkout's end and an offer that lapsed, with the placement
    instant of the hold the copy was offered to at that instant (None when nobody was waiting)"""
    if hasattr(d, "_free"):
        return d._free
    offers = collections.defaultdict(list)
    for h in d.holds:
        if h["offered"] is not None:
            offers[(h["title"], h["offered"])].append(h["placed"])
    ev = collections.defaultdict(list)
    for l in d.loans:
        if l["ended"] is not None:
            ev[l["title"]].append(l["ended"])
    for h in d.holds:
        if h["status"] == "Offer expired":
            ev[h["title"]].append(h["changed"])
    out = {}
    for t, times in ev.items():
        times.sort()
        lst = []
        used = collections.Counter()
        for tm in times:
            rec = offers.get((t, tm), [])
            k = used[(t, tm)]
            used[(t, tm)] += 1
            lst.append((tm, sorted(rec)[k] if k < len(rec) else None))
        out[t] = lst
    d._free = out
    return out


def counterfactual_offer(d, h):
    """the instant a copy would have been offered to a cancelled hold had it stayed: the first instant after the
    cancellation at which a copy came free and went to a later-placed hold or to nobody"""
    evs = free_events(d).get(h["title"], [])
    times = [e[0] for e in evs]
    i = bisect.bisect_right(times, h["changed"])
    for tm, rec in evs[i:]:
        if rec is None or rec > h["placed"]:
            return tm
    return None


def next_later_offer(d, h):
    later = [g["offered"] for g in d._by_title[h["title"]] if g["placed"] > h["placed"] and g["offered"] is not None]
    return min(later) if later else None


def waits(d, method="golden"):
    """per counted hold: (faculty, title, wait in days or None, observed days, event flag)"""
    pop = call_population(d)
    if not hasattr(d, "_by_title"):
        d._by_title = collections.defaultdict(list)
        for h in d.holds:
            d._by_title[h["title"]].append(h)
    extract = max(max(h["placed"] for h in d.holds), max(l["start"] for l in d.loans))
    out = []
    for h, fac in pop:
        st = h["status"]
        if h["offered"] is not None:
            w = days(h["placed"], h["offered"])
            out.append((fac, h["title"], w, w, 1, h))
        elif st.startswith("Cancelled"):
            obs = days(h["placed"], h["changed"])
            if method == "golden":
                cf = counterfactual_offer(d, h)
            elif method == "simple":
                cf = next_later_offer(d, h)
            else:
                cf = None
            w = days(h["placed"], cf) if cf else CAP + 1
            out.append((fac, h["title"], w, obs, 0, h))
        else:
            w = days(h["placed"], extract)
            out.append((fac, h["title"], w, w, 0, h))
    return out


def km_excess(obs):
    """restricted mean of hold-weeks from a Kaplan-Meier curve: obs is a list of (days, event)"""
    pairs = sorted(obs)
    n = len(pairs)
    S, at = 1.0, n
    pts = [(0.0, 1.0)]
    for t, e in pairs:
        if e:
            S *= (1.0 - 1.0 / at)
        at -= 1
        pts.append((t, S))
    tot = 0.0
    for k in range(len(pts) - 1):
        a, s = pts[k]
        b = pts[k + 1][0]
        lo, hi = max(a, GRACE), min(b, CAP)
        if hi > lo:
            tot += s * (hi - lo)
    lt, ls = pts[-1]
    if lt < CAP:
        tot += ls * (CAP - max(lt, GRACE))
    return tot / 7.0


def faculty_hold_weeks(d, method="golden"):
    W = waits(d, "golden" if method in ("golden", "filled", "to_cancel") or method.startswith("km") else method)
    hw = collections.defaultdict(float)
    n = collections.Counter()
    for fac, t, w, obs, ev, h in W:
        n[fac] += 1
    if method in ("golden", "simple"):
        for fac, t, w, obs, ev, h in W:
            hw[fac] += hold_weeks(w)
    elif method == "filled":
        for fac, t, w, obs, ev, h in W:
            if ev:
                hw[fac] += hold_weeks(w)
    elif method == "to_cancel":
        for fac, t, w, obs, ev, h in W:
            hw[fac] += hold_weeks(obs)
    elif method == "km_fac":
        for f in FAC_ORDER:
            rr = [(obs, ev) for fac, t, w, obs, ev, h in W if fac == f]
            hw[f] = len(rr) * km_excess(rr)
    elif method == "km_pool":
        x = km_excess([(obs, ev) for fac, t, w, obs, ev, h in W])
        for f in FAC_ORDER:
            hw[f] = n[f] * x
    elif method == "km_title":
        byt = collections.defaultdict(list)
        for row in W:
            byt[row[1]].append(row)
        for t, rr in byt.items():
            x = km_excess([(r[3], r[4]) for r in rr])
            for r in rr:
                hw[r[0]] += x
    return {f: hw[f] for f in FAC_ORDER}, {f: n[f] for f in FAC_ORDER}


def allocate(hw):
    tot = sum(hw.values())
    return {f: FUND * hw[f] / tot for f in FAC_ORDER}


def main_call(target, method="golden"):
    d = load(target)
    hw, n = faculty_hold_weeks(d, method)
    return dict(hw=hw, n=n, amount=allocate(hw), total_hw=sum(hw.values()))


# ------------------------------------------------------------------ the asks
def norm_isbn(s):
    s = re.sub(r"[^0-9Xx]", "", s or "").upper()
    if len(s) == 10:
        core = "978" + s[:9]
        ssum = sum((1 if i % 2 == 0 else 3) * int(c) for i, c in enumerate(core))
        return core + str((10 - ssum % 10) % 10)
    return s


def load_admin(target):
    d = load(target)
    if hasattr(d, "cat"):
        return d
    F = pack.FILES
    h, rows = IO.read_csv(os.path.join(target, F["catalogue"]))
    ix = {c: i for i, c in enumerate(h)}
    d.cat = {r[ix["mms_id"]]: dict(mms=r[ix["mms_id"]], edition=int(re.match(r"\d+", r[ix["edition"]]).group(0)),
                                   isbn=r[ix["isbn"]], rtype=r[ix["resource_type"]], platform=r[ix["shelfmark_title_id"]],
                                   linked=r[ix["related_record_mms"]], prev=r[ix["preceding_edition_mms"]])
             for r in rows}
    d.cat_by_isbn = {v["isbn"]: v for v in d.cat.values()}
    h, rows = IO.read_csv(os.path.join(target, F["lists"]))
    ix = {c: i for i, c in enumerate(h)}
    d.items = [dict(id=r[ix["list_item_id"]], course=r[ix["course_code"]], period=r[ix["teaching_period"]],
                    edition=int(re.match(r"\d+", r[ix["edition"]]).group(0)), isbn=r[ix["isbn"]],
                    importance=r[ix["importance"]]) for r in rows]
    wb = openpyxl.load_workbook(os.path.join(target, F["courses"]), read_only=True)
    d.course_school = {}
    for ws in wb.worksheets:
        for r in list(ws.iter_rows(values_only=True))[1:]:
            d.course_school[r[0]] = r[2]
    wb = openpyxl.load_workbook(os.path.join(target, F["register"]), read_only=True)
    rows = list(wb["Licences"].iter_rows(values_only=True))
    hd = {c: i for i, c in enumerate(rows[0])}
    d.reg = [dict(lic=r[hd["Licence ID"]], platform=r[hd["Platform title ID"]], eisbn=r[hd["e-ISBN"]],
                  model=r[hd["Licence model"]], copies=r[hd["Copies"]], date=_as_date(r[hd["Order date"]]),
                  po=r[hd["PO line"]], otype=r[hd["Order type"]], price=r[hd["Net price (line)"]],
                  cur=r[hd["Currency"]], fund=r[hd["Fund code"]]) for r in rows[1:]]
    prow = list(wb["Packages"].iter_rows(values_only=True))
    d.pkgs = [dict(name=r[0], publisher=r[1], start=_as_date(r[3]), end=_as_date(r[4]), po=r[5], price=r[6], cur=r[7])
              for r in prow[1:]]
    d.kbart = {}
    for pname, fn in pack.KBART.items():
        h, rows = IO.read_csv(os.path.join(target, fn), delimiter="\t")
        ix = {c: i for i, c in enumerate(h)}
        d.kbart[pname] = [dict(print=r[ix["print_identifier"]], online=r[ix["online_identifier"]]) for r in rows]
    h, rows = IO.read_csv(os.path.join(target, F["invoices"]))
    ix = {c: i for i, c in enumerate(h)}
    d.inv = [dict(vendor=r[ix["supplier"]], inv=r[ix["invoice_no"]],
                  date=dt.datetime.strptime(r[ix["invoice_date"]], "%d/%m/%Y").date(), po=r[ix["po_line"]],
                  isbn=r[ix["isbn"]], cur=r[ix["currency"]], amount=float(r[ix["net_amount"]]),
                  fund=r[ix["fund_code"]], ltype=r[ix["line_type"]], desc=r[ix["description"]]) for r in rows]
    h, rows = IO.read_csv(os.path.join(target, F["rates"]))
    d.rates = {r[0]: (float(r[1]), float(r[2])) for r in rows}
    h, rows = IO.read_csv(os.path.join(target, F["status"]))
    d.status = {(r[0], int(r[1])): int(r[4]) for r in rows}
    return d


def _as_date(v):
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    return dt.datetime.strptime(str(v), "%Y-%m-%d").date()


def work_of(d, isbn, chain=True):
    """the Shelfmark e-book record an ISBN leads to, following the catalogue's related and preceding-edition
    links: returns (platform title id or None, cited edition)"""
    rec = d.cat_by_isbn.get(norm_isbn(isbn))
    if rec is None:
        return None, None
    ed = rec["edition"]
    if rec["platform"]:
        return rec["platform"], ed
    if rec["linked"] and rec["linked"] in d.cat and d.cat[rec["linked"]]["platform"]:
        return d.cat[rec["linked"]]["platform"], ed
    if chain:
        # an earlier edition: find the record whose preceding edition is this one
        for v in d.cat.values():
            if v["prev"] == rec["mms"] and v["platform"]:
                return v["platform"], ed
    return None, ed


def list_faculty(d, course):
    return d.school_fac[d.course_school[course]]


def package_titles(d):
    """platform titles each package carries, read through the KBART online identifiers"""
    out = {}
    for pname, rows in d.kbart.items():
        s = set()
        for r in rows:
            rec = d.cat_by_isbn.get(norm_isbn(r["online"]))
            if rec and rec["platform"]:
                s.add(rec["platform"])
        out[pname] = s
    return out


def ask_a(target, variant="golden"):
    """each faculty's course text spend on invoices dated 1 Jan to 31 Oct 2026, in pounds"""
    d = load_admin(target)
    spend = collections.defaultdict(float)
    pk_titles = package_titles(d)
    # titles on each faculty's essential 2025-26 lists
    fac_titles = collections.defaultdict(set)
    for it in d.items:
        if it["importance"] != "Essential" or not it["period"].startswith("2025-26"):
            continue
        if variant == "direct_isbn":
            rec = d.cat_by_isbn.get(norm_isbn(it["isbn"]))
            plat = rec["platform"] if rec else None
        else:
            plat, _ = work_of(d, it["isbn"])
        if plat:
            fac_titles[list_faculty(d, it["course"])].add(plat)
    for ln in d.inv:
        if not (dt.date(2026, 1, 1) <= ln["date"] <= dt.date(2026, 10, 31)):
            continue
        key = ln["date"].strftime("%Y-%m")
        eur, usd = d.rates[key]
        gbp = ln["amount"] if ln["cur"] == "GBP" else ln["amount"] / (eur if ln["cur"] == "EUR" else usd)
        if variant == "no_fx":
            gbp = ln["amount"]
        if ln["fund"] == "CT-CORE":
            pk = [p for p in d.pkgs if p["po"] == ln["po"]][0]
            titles = pk_titles[pk["name"]]
            counts = {f: len(fac_titles[f] & titles) for f in FAC_ORDER}
            if variant == "even_packages":
                counts = {f: 1 for f in FAC_ORDER}
            tot = sum(counts.values())
            for f in FAC_ORDER:
                spend[f] += gbp * counts[f] / tot
        else:
            spend[d.fund_fac[ln["fund"]]] += gbp
    return {f: spend[f] for f in FAC_ORDER}


def ask_b(target, variant="golden"):
    """essential items on each faculty's spring 2026 lists that could not be lent on 12 January 2026"""
    d = load_admin(target)
    day = dt.date(2026, 1, 12)
    licensed = set(r["platform"] for r in d.reg if r["date"] <= day)
    pk = package_titles(d)
    in_pkg = set()
    for p in d.pkgs:
        if p["start"] <= day <= p["end"]:
            in_pkg |= pk[p["name"]]
    ed_of = {v["platform"]: v["edition"] for v in d.cat.values() if v["platform"]}
    out = collections.Counter()
    for it in d.items:
        if it["importance"] != "Essential" or it["period"] != "2025-26 Semester 2":
            continue
        fac = list_faculty(d, it["course"])
        if variant == "direct_isbn":
            rec = d.cat_by_isbn.get(norm_isbn(it["isbn"]))
            plat = rec["platform"] if rec else None
            ced = it["edition"]
        elif variant == "no_chain":
            plat, ced = work_of(d, it["isbn"], chain=False)
        else:
            plat, ced = work_of(d, it["isbn"])
        ok = False
        if plat and ed_of.get(plat, 0) >= (ced or 0):
            if plat in licensed or (variant != "register_only" and plat in in_pkg):
                ok = True
        if not ok:
            out[fac] += 1
    return {f: out[f] for f in FAC_ORDER}


def ask_c(target, variant="golden"):
    """each faculty's 40-loan licences in force at the end of 30 October 2026 with ten or fewer loans left"""
    d = load_admin(target)
    cutoff = dt.datetime(2026, 10, 30, 23, 59, 59, tzinfo=UK).astimezone(UTC)
    rec_start = dt.datetime(2025, 9, 1, tzinfo=UTC)
    copies = collections.defaultdict(list)   # platform -> list of copy dicts
    lic_lines = {r["lic"]: r for r in d.reg}
    for r in d.reg:
        if r["model"] != "1 user, 40 loans":
            continue
        for k in range(int(r["copies"])):
            left = d.status.get((r["lic"], k + 1), 40) if r["date"] <= rec_start.date() else 40
            if variant == "no_status":
                left = 40
            since = None
            if r["otype"] == "Renewal":
                since = "renewal"
            copies[r["platform"]].append(dict(lic=r["lic"], k=k + 1, date=r["date"], left=left, fund=r["fund"],
                                              otype=r["otype"], po=r["po"], lapsed=None, since=since))
    loans_by_title = collections.defaultdict(list)
    for l in d.loans:
        loans_by_title[l["title"]].append(l)
    for plat, cps in copies.items():
        # a renewal is held from the instant the licence it replaces lapsed
        for c in cps:
            if c["otype"] == "Renewal":
                c["held"] = None
            elif c["date"] <= rec_start.date():
                c["held"] = rec_start - dt.timedelta(days=1)
            else:
                c["held"] = dt.datetime(c["date"].year, c["date"].month, c["date"].day, 9, 0, tzinfo=UTC)
        pending = {}   # lapsed licence id -> lapse instant
        for l in sorted(loans_by_title.get(plat, []), key=lambda x: x["start"]):
            for c in cps:
                if c["otype"] == "Renewal" and c["held"] is None:
                    src = c["po"].split("-")[1] if variant != "renewal_dates" else None
                    if src and src in pending:
                        c["held"] = pending.pop(src)
                    elif variant == "renewal_dates":
                        c["held"] = dt.datetime(c["date"].year, c["date"].month, c["date"].day, 0, 0, tzinfo=UTC)
            if variant == "even":
                continue
            live = sorted([c for c in cps if c["held"] is not None and c["held"] <= l["start"] and c["lapsed"] is None
                           and c["left"] > 0], key=lambda c: (c["held"], c["lic"], c["k"]))
            if not live:
                continue
            c = live[0]
            c["left"] -= 1
            if c["left"] == 0:
                end = l["ended"]
                c["lapsed"] = end if end else dt.datetime(2099, 1, 1, tzinfo=UTC)
                if end:
                    pending[c["lic"]] = end
        if variant == "even":
            n = len([l for l in loans_by_title.get(plat, []) if l["start"] <= cutoff])
            live = [c for c in cps]
            for c in live:
                c["left"] -= n / max(1, len(live))
    out = collections.Counter()
    for plat, cps in copies.items():
        for c in cps:
            held = c.get("held")
            in_force = held is not None and held <= cutoff and (c["lapsed"] is None or c["lapsed"] > cutoff)
            if variant == "even":
                in_force = c["date"] <= cutoff.date()
            if in_force and c["left"] <= 10:
                out[d.fund_fac[c["fund"]]] += 1
    return {f: out[f] for f in FAC_ORDER}
