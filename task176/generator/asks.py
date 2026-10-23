"""task176 the rows the asks read, none of which the call reads: the child care subsidy's 2026 payment lines, the
food program's 2026 home claims and the licensing inspectors' 2026 visits. Each is generated from the homes open
in 2026 and from centres and exempt carers the call never sees. The devices are the systems' own:
- a child moving between homes, or in split care, has lines at two homes on the same days (a notice period paid
  to the home the child left, or two homes each caring for part of the day);
- a sponsor revising a claim files it again under a new claim number; when Tri-County's sponsorship ended on 15
  May 2026 its homes filed May in two parts, one with each sponsor;
- an unannounced monitoring visit that also investigated a complaint is entered once in each module, the same
  inspector, date, arrival and departure on both records."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as C

Y0, Y1 = dt.date(2026, 1, 1), dt.date(2026, 12, 31)
HOLIDAYS = {dt.date(2026, 1, 1), dt.date(2026, 1, 19), dt.date(2026, 2, 16), dt.date(2026, 5, 25), dt.date(2026, 6, 19),
            dt.date(2026, 7, 3), dt.date(2026, 9, 7), dt.date(2026, 10, 12), dt.date(2026, 11, 11), dt.date(2026, 11, 26),
            dt.date(2026, 11, 27), dt.date(2026, 12, 25)}


def next_workday(d):
    while d.weekday() >= 5 or d in HOLIDAYS:
        d += dt.timedelta(days=1)
    return d
SPONSORS = (("S01", "Allerton Family Day Care Food Program"), ("S02", "Lakeshore Child Nutrition Services"),
            ("S03", "Valley Home Providers Food Program"), ("S04", "Tri-County Child Care Food Program"))
S04_END = dt.date(2026, 5, 15)


def weekdays(a, b):
    """weekdays from a to b inclusive"""
    if b < a:
        return 0
    n = (b - a).days + 1
    full, rem = divmod(n, 7)
    wd = full * 5
    for i in range(rem):
        if (a + dt.timedelta(days=full * 7 + i)).weekday() < 5:
            wd += 1
    return wd


def add_bd(d, n):
    """n business days after d"""
    while n > 0:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d


def active_2026(h):
    s = max(h.lic, Y0)
    e = min(h.close or Y1, Y1)
    return (s, e) if s <= e else None


def months_between(a, b):
    out = []
    d = dt.date(a.year, a.month, 1)
    while d <= b:
        nd = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
        out.append((max(d, a), min(nd - dt.timedelta(days=1), b)))
        d = nd
    return out


class Ccap:
    """subsidised children and their payment lines"""

    def __init__(self, homes, ident):
        r = C.stream("ccap")
        self.lines = []          # (line_no, batch, case, child, provider, ptype, county, s, e, days, rate, amount, status, ref)
        self.truth = {}          # region, half -> union child-days at family child care homes
        act = [(h, active_2026(h)) for h in homes]
        act = [(h, w) for h, w in act if w]
        by_cty = {}
        for h, w in act:
            by_cty.setdefault(h.county, []).append((h, w))
        cid = [0]
        case = [0]

        def new_child():
            cid[0] += 1
            return "C%07d" % (3000000 + cid[0] * 7 + int(r.integers(0, 7)))

        def new_case():
            case[0] += 1
            return "%02d-%06d" % (int(r.integers(10, 99)), 400000 + case[0] * 3 + int(r.integers(0, 3)))

        spells = []   # (child, case, provider_no, ptype, county, start, end, rate)
        for h, (s, e) in act:
            if r.random() > 0.56:
                continue
            for _ in range(1 + int(r.poisson(0.5))):
                a = s + dt.timedelta(days=int(r.integers(-330, max(1, (e - s).days - 30))))
                a = max(a, h.lic + dt.timedelta(days=20))
                b = min(e, a + dt.timedelta(days=int(r.integers(60, 400))))
                if b <= a:
                    continue
                ch, cs = new_child(), new_case()
                rate = 1.0
                spells.append([ch, cs, ident.cur[h.hid], h.ltype, h.county, a, b, rate])
                u = r.random()
                peers = [x for x in by_cty[h.county] if x[0] is not h]
                if u < 0.13 and peers and b < e:
                    # the child moves to another home in the county: the home left is paid ten business days of notice
                    h2, (s2, e2) = peers[int(r.integers(0, len(peers)))]
                    na = b + dt.timedelta(days=1)
                    if s2 <= na <= e2:
                        nb = min(e2, na + dt.timedelta(days=int(r.integers(40, 300))))
                        spells[-1][6] = min(add_bd(b, 10), e)
                        spells.append([ch, cs, ident.cur[h2.hid], h2.ltype, h2.county, na, nb, rate])
                elif u < 0.17 and peers:
                    # split care: a second home on the same days for part of each day
                    h2, (s2, e2) = peers[int(r.integers(0, len(peers)))]
                    xa, xb = max(a, s2), min(b, e2)
                    if xa < xb:
                        spells.append([ch, cs, ident.cur[h2.hid], h2.ltype, h2.county, xa, xb, 0.5])
        # centres and exempt carers, in the same payment run
        for j in range(470):
            pno = "CC%05d" % (20000 + j * 13)
            cty = C.COUNTIES[int(r.integers(0, len(C.COUNTIES)))][0]
            for _ in range(int(r.integers(4, 18))):
                a = Y0 + dt.timedelta(days=int(r.integers(-40, 330)))
                b = a + dt.timedelta(days=int(r.integers(60, 380)))
                spells.append([new_child(), new_case(), pno, "CTR", cty, max(a, dt.date(2025, 12, 1)), min(b, Y1), 1.0])
        for j in range(380):
            pno = "LE%06d" % (700000 + j * 17)
            cty = C.COUNTIES[int(r.integers(0, len(C.COUNTIES)))][0]
            a = Y0 + dt.timedelta(days=int(r.integers(-30, 300)))
            b = a + dt.timedelta(days=int(r.integers(40, 300)))
            spells.append([new_child(), new_case(), pno, "EXEMPT", cty, max(a, dt.date(2025, 12, 1)), min(b, Y1), 1.0])
        # lines: one per child, provider and service month, paid in the statewide run after the month; each run issues
        # one remittance to each payee (the provider, or its network), numbered in the county office's own sequence for that run, and every
        # child line of a remittance carries the remittance's amount
        rate_of = {"SFCC": 812.0, "LFCC": 846.0, "CTR": 1138.0, "EXEMPT": 402.0}
        # family child care networks: a home that joins a network assigns its payments to the network, which is paid
        # one remittance a run for the children of all its homes; networks are small, three to six homes of a county
        rn = C.stream("ccap/networks")
        members = {}
        for h, w in act:
            if rn.random() < 0.12:
                members.setdefault(h.county, []).append(ident.cur[h.hid])
        affil = {}
        for cty in sorted(members):
            lst = members[cty]
            j, k = 0, 0
            while j < len(lst):
                n = int(rn.integers(3, 7))
                k += 1
                for pno in lst[j:j + n]:
                    affil[pno] = "NET%s%02d" % (cty[2:], k)
                j += n
        self.affil = affil

        def payee_of(pno, cty):
            return affil.get(pno, pno)
        by_run = {}
        for ch, cs, pno, pt, cty, a, b, f in spells:
            for ms, me in months_between(max(a, dt.date(2025, 12, 1)), b):
                days = weekdays(ms, me)
                if days == 0:
                    continue
                full = weekdays(dt.date(ms.year, ms.month, 1), month_end(ms))
                amt = round(rate_of[pt] * (0.5 if f < 1 else 1.0) * days / full, 2)
                run = RUNS[(ms.year, ms.month)]
                if run > C.PULL:
                    continue
                by_run.setdefault(run, {}).setdefault((cty, payee_of(pno, cty)), []).append([cs, ch, ms, me, days, amt, pno, pt])
        rows = []
        voided = []
        runs = sorted(by_run)
        payees = {}           # each county office's payee list, in the order payees were first paid
        for k, run in enumerate(runs):
            rem = by_run[run]
            for (cty, pay) in sorted(rem):
                lst = payees.setdefault(cty, {})
                if pay not in lst:
                    lst[pay] = len(lst)
            seq = {}
            for (cty, pay) in sorted(rem, key=lambda x: (x[0], payees[x[0]][x[1]])):
                lines = rem[(cty, pay)]
                seq[cty] = seq.get(cty, 0) + 1
                no = "RM%04d" % seq[cty]
                tot = round(sum(x[5] for x in lines), 2)
                status = "VOID" if (r.random() < 0.012 and k + 1 < len(runs)) else "PAID"
                for x in lines:
                    rows.append([no, run, cty, x[6], x[7], x[0], x[1], x[2], x[3], x[4], tot, status])
                if status == "VOID":
                    # the remittance is paid again in the next run, numbered in that run's sequence
                    nxt = runs[k + 1]
                    by_run[nxt].setdefault((cty, pay), []).extend([list(x) for x in lines])
        rows.sort(key=lambda x: (x[1], x[2], x[0], x[6]))
        self.lines = rows
        self.spells = spells

    def truth_child_days(self):
        """the union of each child's 2026 weekdays at family child care homes, by the homes' region and half"""
        out = {}
        for row in self.lines:
            if row[11] == "VOID" or row[4] not in ("SFCC", "LFCC"):
                continue
            ms, me = max(row[7], Y0), min(row[8], Y1)
            if me < ms:
                continue
            reg = C.COUNTY_REGION[row[2]]
            d = ms
            while d <= me:
                if d.weekday() < 5:
                    out.setdefault((reg, 1 if d.month <= 6 else 2), set()).add((row[6], d))
                d += dt.timedelta(days=1)
        return {k: len(v) for k, v in out.items()}

    def truth_money(self):
        """money paid to family child care homes in the 2026 runs, by region and quarter: each remittance once"""
        seen = {}
        for row in self.lines:
            if row[11] == "VOID" or row[4] not in ("SFCC", "LFCC") or row[1].year != 2026:
                continue
            seen[(row[0], row[1], row[2])] = (C.COUNTY_REGION[row[2]], (row[1].month - 1) // 3 + 1, row[10])
        out = {}
        for reg, q, amt in seen.values():
            out[(reg, q)] = round(out.get((reg, q), 0.0) + amt, 2)
        return out


def month_end(d):
    return dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1) - dt.timedelta(days=1)


RUNS = {}
for _y, _m in [(2025, 12)] + [(2026, m) for m in range(1, 13)]:
    _d = dt.date(_y + (_m == 12), _m % 12 + 1, 1) + dt.timedelta(days=3)
    while _d.weekday() >= 5 or _d in HOLIDAYS or _d == dt.date(2027, 1, 1):
        _d += dt.timedelta(days=1)
    RUNS[(_y, _m)] = _d

CCAP_HEAD = ("remittance_no", "pay_run_date", "county_fips", "provider_no", "provider_type", "case_no", "child_no",
             "service_from", "service_to", "care_days", "remittance_amount", "remittance_status")


def ccap_rows(cc):
    return [(x[0], x[1].isoformat(), x[2], x[3], x[4], x[5], x[6], x[7].isoformat(), x[8].isoformat(), x[9],
             "%.2f" % x[10], x[11]) for x in cc.lines]


class Cacfp:
    def __init__(self, homes, ident):
        r = C.stream("cacfp")
        act = [(h, active_2026(h)) for h in homes]
        act = [(h, w) for h, w in act if w]
        rows = []
        cn = [0]

        def claim_no():
            cn[0] += 1
            return "%s%06d" % ("26", 100000 + cn[0] * 7 + int(r.integers(0, 7)))

        for h, (s, e) in act:
            if r.random() > 0.61:
                continue
            reg = C.COUNTY_REGION[h.county]
            if reg in (3, 4) and r.random() < 0.45:
                sp = "S04"
            elif reg == 5 or (reg == 2 and r.random() < 0.3):
                sp = "S02"
            elif reg == 3 and r.random() < 0.6:
                sp = "S03"
            else:
                sp = "S01"
            new_sp = ("S03" if reg == 3 else "S01") if sp == "S04" else None
            # some homes change sponsor during the year; the month of the change is filed by both sponsors
            sw_m, sw_day, sw_to = None, None, None
            if sp != "S04" and r.random() < 0.06:
                sw_m = int(r.integers(2, 12))
                sw_day = int(r.integers(8, 23))
                sw_to = [x[0] for x in SPONSORS[:3] if x[0] != sp][int(r.integers(0, 2))]
            kids = int(r.integers(3, h.cap + 1))
            att = r.uniform(0.62, 0.9)
            for ms, me in months_between(s, e):
                parts = [(sp, ms, me)]
                if sp == "S04" and ms.month == 5:
                    parts = [("S04", ms, min(me, S04_END)), (new_sp, S04_END + dt.timedelta(days=1), me)]
                elif sp == "S04" and ms > S04_END:
                    parts = [(new_sp, ms, me)]
                elif sw_m is not None and ms.month == sw_m:
                    cut = dt.date(ms.year, ms.month, sw_day)
                    parts = [(sp, ms, min(me, cut)), (sw_to, cut + dt.timedelta(days=1), me)]
                elif sw_m is not None and ms.month > sw_m:
                    parts = [(sw_to, ms, me)]
                for spn, a, b in parts:
                    if b < a:
                        continue
                    wd = weekdays(a, b)
                    if wd == 0:
                        continue
                    bf = int(round(kids * wd * att * r.uniform(0.55, 0.8)))
                    lu = int(round(kids * wd * att * r.uniform(0.85, 1.0)))
                    su = int(round(kids * wd * att * r.uniform(0.0, 0.18)))
                    sn = int(round(kids * wd * att * r.uniform(0.9, 1.6)))
                    sub = b + dt.timedelta(days=int(r.integers(2, 9)))
                    if sub > C.PULL:
                        continue
                    row = [claim_no(), spn, ident.cur[h.hid], h.county, dt.date(a.year, a.month, 1), sub, wd, kids, bf, lu, su, sn]
                    rows.append(row)
                    if r.random() < 0.07:
                        f = r.uniform(0.9, 1.14)
                        rev = [claim_no(), spn, row[2], row[3], row[4], sub + dt.timedelta(days=int(r.integers(8, 50))),
                               wd, kids] + [int(round(v * f)) for v in row[8:12]]
                        if rev[5] <= C.PULL:
                            rows.append(rev)
        # centre claims are filed directly, not through a sponsor; they stay in the extract with no sponsor
        for j in range(160):
            for m in range(1, 13):
                wd = weekdays(dt.date(2026, m, 1), dt.date(2026, m, 28))
                k = int(r.integers(20, 90))
                sub = dt.date(2026, m, 28) + dt.timedelta(days=int(r.integers(5, 12)))
                if sub > C.PULL:
                    continue
                rows.append([claim_no(), "", "CC%05d" % (20000 + j * 13), C.COUNTIES[j % len(C.COUNTIES)][0],
                             dt.date(2026, m, 1), sub, wd, k, k * wd // 2, k * wd, k * wd // 9, k * wd * 3 // 2])
        rows.sort(key=lambda x: (x[5], x[0]))
        self.rows = rows

    def truth_meals(self):
        """by region and half: the latest claim of each sponsor for each home and month, every sponsor's claim kept"""
        last = {}
        for row in self.rows:
            if not row[2].startswith("FC"):
                continue
            key = (row[1], row[2], row[4])
            if key not in last or row[5] > last[key][5]:
                last[key] = row
        out = {}
        for row in last.values():
            reg = C.COUNTY_REGION[row[3]]
            half = 1 if row[4].month <= 6 else 2
            out[(reg, half)] = out.get((reg, half), 0) + sum(row[8:12])
        return out


CACFP_HEAD = ("claim_no", "sponsor_id", "site_licence_no", "county_fips", "claim_month", "received_date",
              "operating_days", "enrolled_children", "breakfasts", "lunches", "suppers", "snacks")


def cacfp_rows(cf):
    return [(x[0], x[1], x[2], C.COUNTY_NAME[x[3]] + " County", x[4].strftime("%Y-%m"), x[5].isoformat(), x[6], x[7],
             x[8], x[9], x[10], x[11]) for x in cf.rows]


class Visits:
    def __init__(self, homes, ident):
        r = C.stream("visits/2026")
        act = [(h, active_2026(h)) for h in homes]
        act = [(h, w) for h, w in act if w]
        insp = {reg: ["I%03d" % (100 + reg * 20 + j) for j in range(5 + reg % 3 + (3 if reg == 2 else 0))] for reg in C.REGIONS}
        rows = []
        vn = [0]

        def vno():
            vn[0] += 1
            return "V26-%05d" % (10000 + vn[0] * 3 + int(r.integers(0, 3)))

        def slot(s, e):
            if e < s:
                return None
            for _ in range(20):
                d = s + dt.timedelta(days=int(r.integers(0, max(1, (e - s).days + 1))))
                if d.weekday() < 5 and d not in HOLIDAYS:
                    return d
            return None

        def times():
            a = 8 * 60 + int(r.integers(0, 7 * 60)) // 5 * 5
            return a, a + 35 + int(r.integers(0, 34)) * 5

        def add(no, pt, cty, d, kind, ins, a, b, status="COMPLETED"):
            rows.append([vno(), no, pt, cty, d, kind, ins, a, b, status])

        for h, (s, e) in act:
            reg = C.COUNTY_REGION[h.county]
            no = ident.cur[h.hid]
            monitored = r.random() < 0.88 and (e - s).days > 40
            comp = r.random() < 0.095
            md = slot(s, e) if monitored else None
            if md:
                ins = insp[reg][int(r.integers(0, len(insp[reg])))]
                a, b = times()
                add(no, h.ltype, h.county, md, "MONITORING", ins, a, b)
                if comp and r.random() < 0.46:
                    add(no, h.ltype, h.county, md, "COMPLAINT", ins, a, b)
                    comp = False
                if r.random() < 0.12:
                    fd = slot(md + dt.timedelta(days=14), min(e, md + dt.timedelta(days=60)))
                    if fd:
                        ins2 = insp[reg][int(r.integers(0, len(insp[reg])))]
                        a2, b2 = times()
                        add(no, h.ltype, h.county, fd, "FOLLOW-UP", ins2, a2, min(b2, a2 + 90))
                        if r.random() < 0.08:
                            # a complaint investigated the same day by another inspector, at another time
                            others = [x for x in insp[reg] if x != ins2]
                            a3 = min(b2 + 60, 16 * 60)
                            add(no, h.ltype, h.county, fd, "COMPLAINT", others[0], a3, a3 + 70)
            if comp:
                cd = slot(s, e)
                if cd:
                    ins = insp[reg][int(r.integers(0, len(insp[reg])))]
                    a, b = times()
                    add(no, h.ltype, h.county, cd, "COMPLAINT", ins, a, b)
            if md and r.random() < 0.05:
                # a second visit the same day at another time (the inspector back to check a correction, or a
                # complaint investigated separately by a colleague)
                same = r.random() < 0.5
                ins3 = ins if same else [x for x in insp[reg] if x != ins][0]
                _, b0 = rows[-1][7], rows[-1][8]
                a4 = min((b0 or 12 * 60) + 90, 16 * 60)
                add(no, h.ltype, h.county, md, "FOLLOW-UP" if same else "COMPLAINT", ins3, a4, a4 + 40 + int(r.integers(0, 8)) * 5)
            if r.random() < 0.03 and md:
                add(no, h.ltype, h.county, slot(s, e) or md, "MONITORING", insp[reg][0], None, None, "CANCELLED")
        for j in range(470):
            no = "CC%05d" % (20000 + j * 13)
            cty = C.COUNTIES[j % len(C.COUNTIES)][0]
            reg = C.COUNTY_REGION[cty]
            for _ in range(int(r.integers(1, 4))):
                d = slot(Y0, Y1)
                a, b = times()
                add(no, "CTR", cty, d, ["MONITORING", "RENEWAL", "COMPLAINT"][int(r.integers(0, 3))],
                    insp[reg][int(r.integers(0, len(insp[reg])))], a, b + 60)
        rows.sort(key=lambda x: (x[4], x[0]))
        self.rows = rows

    def truth(self):
        """by region: distinct visits (inspector, home, date, arrival) to family child care homes and their hours"""
        seen = {}
        for v in self.rows:
            if v[2] not in ("SFCC", "LFCC") or v[9] != "COMPLETED":
                continue
            key = (v[1], v[4], v[6], v[7])
            seen[key] = (C.COUNTY_REGION[v[3]], (v[8] - v[7]) / 60.0)
        out = {}
        for reg, hrs in seen.values():
            n, t = out.get(reg, (0, 0.0))
            out[reg] = (n + 1, t + hrs)
        return out


VIS_HEAD = ("visit_no", "licence_no", "facility_type", "county", "visit_date", "visit_type", "inspector_id",
            "arrived", "departed", "status")


def hhmm(x):
    return "" if x is None else "%02d:%02d" % divmod(x, 60)


def visit_rows(vs):
    return [(x[0], x[1], x[2], C.COUNTY_NAME[x[3]], x[4].isoformat(), x[5], x[6], hhmm(x[7]), hhmm(x[8]), x[9])
            for x in vs.rows]
