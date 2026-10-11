"""Simulate three quarters of 13F filing for a closed population of managers and issuers.

Output is a `World` holding (a) the truth: every manager's position per issuer per quarter, (b) the
filings as EDGAR would carry them (submissions, cover pages, information-table lines), with the
realistic mess, and (c) the issuers' cover-page share counts.
"""
import datetime as dt
from dataclasses import dataclass, field

import numpy as np

import world as W

QUARTERS = ["Q2", "Q3", "Q4"]
PRICE_STEP = {"Q2": None, "Q3": None}


@dataclass
class Filing:
    acc: str
    mid: str
    q: str
    date: dt.date
    form: str            # 13F-HR, 13F-HR/A, 13F-NT
    reporttype: str      # 13F HOLDINGS REPORT, 13F NOTICE, 13F COMBINATION REPORT
    amend_no: int = 0
    amend_type: str = ""
    lines: list = field(default_factory=list)   # dicts: iid, cusip, name, title, value, shares, sht, putcall, disc, othmgr
    thousands: bool = False


class World:
    pass


def _bd(d):
    return W.business_day_on_or_after(d)


def build():
    wd = World()
    mgrs = W.build_managers()
    iss = W.build_issuers()
    r = W.rng("sim")
    M = {m["mid"]: m for m in mgrs}
    I = {i["iid"]: i for i in iss}
    wd.mgrs, wd.iss, wd.M, wd.I = mgrs, iss, M, I

    # ------------------------------------------------ special roles
    by_type = {}
    for m in mgrs:
        by_type.setdefault(m["type"], []).append(m)
    passive = by_type["passive"]
    P0, P1 = passive[0], passive[1]                  # early large complexes
    late_passive = passive[2:]
    lo = sorted(by_type["longonly"], key=lambda m: m["mid"])
    bt = sorted(by_type["banktrust"], key=lambda m: m["mid"])
    ria = sorted(by_type["ria"], key=lambda m: m["mid"])
    TK = lo[0]; TK.update(habit=24.0, size=23.2)                        # Q4 values left in thousands
    SP = bt[0]; SP.update(habit=16.0, size=23.0)                        # several lines per position
    GA1, GA2 = lo[1], lo[2]
    GA1.update(habit=19.0, size=22.6); GA2.update(habit=26.0, size=22.0)
    NH = lo[3]; NH.update(habit=22.0, size=21.8)                        # Q3 NEW HOLDINGS amendment
    RS = bt[1]; RS.update(habit=12.0, size=21.9)                        # Q3 RESTATEMENT
    LATE3 = [lo[4], ria[0], ria[1]]                                     # Q3 filed in January
    for m in LATE3:
        m.update(habit=float(r.uniform(15, 26)), size=max(m["size"], 20.8))
    # family pairs in the register (GA is the one that matters for top holder)
    fam_name = GA1["stem"] + " Investment Group"
    GA2["stem"] = GA1["stem"]
    GA2["disp"] = GA1["stem"] + " Capital Advisors LP"
    GA2["name"] = GA2["disp"].upper()
    GA1["family"] = GA2["family"] = fam_name
    for m in mgrs:
        if m["family"] is None:
            m["family"] = ""
    # a few more families for realism (inert)
    for a, b in [(bt[5], bt[6]), (ria[10], ria[11]), (lo[20], lo[21])]:
        b["stem"] = a["stem"]
        b["disp"] = a["stem"] + " " + b["disp"].split(" ", 1)[1]
        b["name"] = b["disp"].upper()
        a["family"] = b["family"] = a["stem"] + " Financial"
    wd.roles = dict(P0=P0["mid"], P1=P1["mid"], TK=TK["mid"], SP=SP["mid"], GA1=GA1["mid"], GA2=GA2["mid"],
                    NH=NH["mid"], RS=RS["mid"], LATE3=[m["mid"] for m in LATE3],
                    late_passive=[m["mid"] for m in late_passive])

    # notice filers (13F-NT every quarter), attrition (no Q4 filing), new filers (first in Q4)
    notice = [m["mid"] for m in ria[150 - 12:]]
    attrit = [m["mid"] for m in ria[120:124]]
    newq4 = [m["mid"] for m in ria[124:130]]
    wd.notice, wd.attrit, wd.newq4 = set(notice), set(attrit), set(newq4)

    # ------------------------------------------------ filing days
    special_dates = {}
    fdate = {}
    for m in mgrs:
        mid = m["mid"]
        for q in QUARTERS:
            if q in ("Q2", "Q3") and mid in wd.newq4:
                continue
            if q == "Q4" and mid in wd.attrit:
                continue
            sd = 0.5 if m["type"] == "passive" else 1.3
            d = m["habit"] + float(r.normal(0, sd))
            d = min(max(d, 4.0), 45.0)
            day = W.PERIODS[q] + dt.timedelta(days=int(round(d)))
            day = _bd(day)
            if day > W.DEADLINE[q]:
                day = W.DEADLINE[q]
                while day.weekday() >= 5 or day in W.HOLIDAYS:
                    day -= dt.timedelta(days=1)
            fdate[(mid, q)] = day
    # managers whose Q3 report was filed in January
    for m in LATE3:
        fdate[(m["mid"], "Q3")] = _bd(dt.date(2023, 1, 9) + dt.timedelta(days=int(r.integers(0, 10))))
    # pin the special managers' Q4 dates well before the extract
    for m in [TK, SP, GA1, GA2, NH, RS, P0, P1] + LATE3:
        if fdate[(m["mid"], "Q4")] > W.EXTRACT_DATE - dt.timedelta(days=4):
            fdate[(m["mid"], "Q4")] = _bd(W.PERIODS["Q4"] + dt.timedelta(days=int(m["habit"])))
    fdate[(NH["mid"], "Q3")] = dt.date(2022, 11, 10)   # original filed after the same-day cut of its window
    wd.fdate = fdate

    def pending(mid, q, cut):
        """filed for the prior quarter, not yet for q by the cut date"""
        return fdate.get((mid, q), dt.date(2099, 1, 1)) > cut

    wd.pending4 = {m["mid"] for m in mgrs if (m["mid"], "Q3") in fdate and m["mid"] not in wd.notice
                   and pending(m["mid"], "Q4", W.EXTRACT_DATE)}

    # ------------------------------------------------ prices
    for i in iss:
        p4 = i["P4"]
        rr = W.rng("px", i["iid"])
        p3 = p4 / float(np.exp(rr.normal(0.02, 0.11)))
        p2 = p3 / float(np.exp(rr.normal(-0.03, 0.12)))
        i["P3"], i["P2"] = round(p3, 2), round(p2, 2)

    # ------------------------------------------------ share counts
    for i in iss:
        rr = W.rng("so", i["iid"])
        i["S_jul"] = int(round(i["S_oct"] * (1 + rr.normal(0.011, 0.007))))
        i["S_jan"] = int(round(i["S_oct"] * (1 - abs(rr.normal(0.0012, 0.0015)))))
        i["S_apr"] = int(round(i["S_jul"] * (1 + rr.normal(0.001, 0.002))))
    I["W08"]["S_jul"] = int(round(I["W08"]["S_oct"] / 0.9463))          # September tender offer retired shares
    I["W08"]["S_apr"] = I["W08"]["S_jul"] + 18_400

    # ------------------------------------------------ positions
    eligible = {q: [m for m in mgrs if (m["mid"], q) in fdate and m["mid"] not in wd.notice] for q in QUARTERS}
    early4 = [m for m in eligible["Q4"] if m["mid"] not in wd.pending4]
    late4 = [m for m in eligible["Q4"] if m["mid"] in wd.pending4]
    late4 += [M[x] for x in wd.attrit]   # pending at the extract by construction (no Q4 filing ever)
    pos = {q: {} for q in QUARTERS}     # (mid, iid) -> shares (truth)

    def pick(pool, n, rr, exclude=()):
        pool = [m for m in pool if m["mid"] not in exclude]
        w = np.exp(np.array([m["size"] for m in pool]) - 20.0)
        w = w / w.sum()
        n = min(n, len(pool))
        idx = rr.choice(len(pool), size=n, replace=False, p=w)
        return [pool[j] for j in idx]

    special = {TK["mid"], SP["mid"], GA1["mid"], GA2["mid"], P0["mid"], P1["mid"], NH["mid"], RS["mid"]} | {m["mid"] for m in LATE3}
    for i in iss:
        rr = W.rng("pos", i["iid"])
        iid, S = i["iid"], i["S_oct"]
        T = i["A"] / 100 * S
        L = (1 - i["f"]) * T
        E = i["f"] * T
        # --- pending managers' Q3 positions (sum L): late passive complexes carry most of it
        lp = [M[x] for x in wd.roles["late_passive"]]
        lp_share = float(rr.uniform(0.55, 0.72))
        others_late = [m for m in late4 if m["type"] != "passive" and m["mid"] not in wd.attrit]
        nl = int(rr.integers(14, 34)) if i["watch"] else int(rr.integers(8, 26))
        chosen_late = pick(others_late, nl, rr)
        wlp = rr.dirichlet(np.full(len(lp), 6.0)) * lp_share * L
        wol = rr.dirichlet(np.full(len(chosen_late), 1.2)) * (1 - lp_share) * L
        q3late = {}
        for m, v in zip(lp, wlp):
            q3late[m["mid"]] = v
        for m, v in zip(chosen_late, wol):
            q3late[m["mid"]] = q3late.get(m["mid"], 0) + v
        # --- early managers' Q4 positions (sum E)
        fixed = {}
        top = {"P0": 0.094, "P1": 0.071}
        if i["watch"]:
            fixed[P0["mid"]] = (0.088 + rr.uniform(0, 0.012)) * S
            fixed[P1["mid"]] = (0.064 + rr.uniform(0, 0.010)) * S
        else:
            fixed[P0["mid"]] = (0.12 + rr.uniform(0, 0.03)) * E
            fixed[P1["mid"]] = (0.08 + rr.uniform(0, 0.03)) * E
        if iid in ("W02", "W08", "W11"):
            fixed[TK["mid"]] = (0.118 + rr.uniform(0, 0.006)) * S
        elif i["watch"]:
            fixed[TK["mid"]] = (0.010 + rr.uniform(0, 0.012)) * S
        if iid in ("W04", "W09"):
            fixed[SP["mid"]] = (0.112 + rr.uniform(0, 0.006)) * S
        elif i["watch"]:
            fixed[SP["mid"]] = (0.006 + rr.uniform(0, 0.010)) * S
        if iid in ("W05", "W12"):
            fixed[GA1["mid"]] = fixed[P0["mid"]] * 0.885
            fixed[GA2["mid"]] = (0.040 + rr.uniform(0, 0.006)) * S
        if i["watch"]:
            fixed[NH["mid"]] = (0.020 + rr.uniform(0, 0.012)) * S
            fixed[RS["mid"]] = (0.016 + rr.uniform(0, 0.010)) * S
            for m in LATE3:
                fixed[m["mid"]] = (0.006 + rr.uniform(0, 0.007)) * S
        rest = E - sum(fixed.values())
        assert rest > 0.10 * E, (iid, rest / S)
        ne = int(rr.integers(110, 230)) if i["watch"] else int(rr.integers(40, 190))
        cand = [m for m in early4 if m["mid"] not in special]
        chosen = pick(cand, ne, rr)
        we = rr.dirichlet(np.full(len(chosen), 0.9)) * rest
        # cap any generic early holder well below the designed top holders
        cap = 0.045 * S
        over = np.clip(we - cap, 0, None).sum()
        we = np.minimum(we, cap)
        we = we + over * (cap - we) / (cap - we).sum()
        q4early = dict(fixed)
        for m, v in zip(chosen, we):
            q4early[m["mid"]] = q4early.get(m["mid"], 0) + v
        # --- Q3 early positions: turnover, entries and exits, scaled to the September target
        q3early = {}
        for mid, v in q4early.items():
            mm = M[mid]
            if mid in special:
                g = rr.normal(0.0, 0.03)
            elif mm["type"] in ("multistrat", "longonly", "ria"):
                g = rr.normal(0.0, 0.16)
            else:
                g = rr.normal(0.0, 0.06)
            if mid not in special and rr.random() < 0.07:
                continue   # new position in Q4
            q3early[mid] = v * float(np.exp(-g))
        exits = pick([m for m in early4 if m["mid"] not in q4early and m["mid"] not in special],
                     int(rr.integers(4, 12)), rr)
        for m in exits:
            q3early[m["mid"]] = float(rr.uniform(0.0004, 0.004)) * S
        target_e3 = i["sep"] / 100 * i["S_jul"] - L
        flex = [k for k in q3early if k not in special]
        fixed3 = sum(v for k, v in q3early.items() if k in special)
        sc = (target_e3 - fixed3) / sum(q3early[k] for k in flex)
        assert 0.6 < sc < 1.6, (iid, sc)
        for k in flex:
            q3early[k] *= sc
        # --- write truth
        for mid, v in q4early.items():
            pos["Q4"][(mid, iid)] = v
        for mid, v in q3early.items():
            pos["Q3"][(mid, iid)] = v
        for mid, v in q3late.items():
            pos["Q3"][(mid, iid)] = v
            if mid in wd.attrit:
                continue
            pos["Q4"][(mid, iid)] = v * float(1 + rr.normal(0, 0.010))
        # --- Q2: late managers stable, early managers turn over
        for (mid, ii), v in list(pos["Q3"].items()):
            if ii != iid:
                continue
            mm = M[mid]
            if mid in q3late or mm["type"] == "passive":
                pos["Q2"][(mid, iid)] = v * float(1 + rr.normal(0, 0.012))
            else:
                if rr.random() < 0.06:
                    continue
                pos["Q2"][(mid, iid)] = v * float(np.exp(rr.normal(0, 0.13)))
        # small new Q4 filers (pending or not) with tiny positions
        for mid in newq4:
            if rr.random() < 0.35:
                pos["Q4"][(mid, iid)] = float(rr.uniform(0.0002, 0.0012)) * S
    # integerise
    for q in QUARTERS:
        pos[q] = {k: int(round(v)) for k, v in pos[q].items() if v >= 1}
        # drop positions of managers that do not file that quarter
        pos[q] = {k: v for k, v in pos[q].items() if (k[0], q) in fdate}
    wd.pos = pos

    # ------------------------------------------------ filings and lines
    build_filings(wd, r)
    return wd


def _acc(cik, yy, seq):
    return f"{cik:010d}-{yy:02d}-{seq:06d}"


def build_filings(wd, r):
    M, I = wd.M, wd.I
    roles = wd.roles
    agents = [1_104_659, 1_213_900, 1_085_146, 950_123, 1_567_619]
    seqs = {}

    def acc_for(mid, d):
        cik = M[mid]["cik"] if r.random() < 0.45 else int(agents[r.integers(len(agents))])
        yy = d.year % 100
        seqs[(cik, yy)] = seqs.get((cik, yy), int(r.integers(1, 400))) + int(r.integers(1, 30))
        return _acc(cik, yy, seqs[(cik, yy)])

    price = {q: {} for q in QUARTERS}
    for i in wd.iss:
        price["Q2"][i["iid"]] = i["P2"]; price["Q3"][i["iid"]] = i["P3"]; price["Q4"][i["iid"]] = i["P4"]
    wd.price = price

    def make_lines(mid, q, holdings, rr, thousands):
        mm = M[mid]
        lines = []
        for iid, sh in sorted(holdings.items()):
            ii = I[iid]
            px = price[q][iid]
            parts = [sh]
            if mid == roles["SP"] and iid in ("W04", "W09") and q == "Q4":
                a = int(sh * 0.38); b = int(sh * 0.34); parts = [a, b, sh - a - b]
            elif mid == roles["SP"] and q == "Q4" and ii["watch"]:
                a = int(sh * 0.55); parts = [a, sh - a]
            elif mm["type"] in ("banktrust", "passive") and rr.random() < 0.30 and sh > 50:
                a = int(sh * rr.uniform(0.2, 0.8)); parts = [a, sh - a]
            for k, s in enumerate(parts):
                v = s * px
                v = int(round(v / 1000.0)) if thousands else int(round(v))
                disc = "SOLE" if k == 0 else ("DFND" if mm["type"] in ("banktrust", "passive") else "OTR")
                lines.append(dict(iid=iid, cusip=ii["cusip"], name=ii["name"], title="COM",
                                  value=v, shares=int(s), sht="SH", putcall="", disc=disc,
                                  othmgr="" if k == 0 else str(k)))
        return lines

    filings = []
    hold_by = {q: {} for q in QUARTERS}
    for (mid, iid), sh in wd.pos["Q2"].items():
        hold_by["Q2"].setdefault(mid, {})[iid] = sh
    for (mid, iid), sh in wd.pos["Q3"].items():
        hold_by["Q3"].setdefault(mid, {})[iid] = sh
    for (mid, iid), sh in wd.pos["Q4"].items():
        hold_by["Q4"].setdefault(mid, {})[iid] = sh

    rr = W.rng("lines")
    for (mid, q), d in sorted(wd.fdate.items(), key=lambda kv: (kv[1], kv[0])):
        if d > W.EXTRACT_DATE:
            continue
        thousands = d < W.UNIT_SWITCH
        if mid == roles["TK"] and q == "Q4":
            thousands = True       # reported on the old basis after the switch
        if mid in wd.notice:
            filings.append(Filing(acc_for(mid, d), mid, q, d, "13F-NT", "13F NOTICE"))
            continue
        h = dict(hold_by[q].get(mid, {}))
        rtype = "13F COMBINATION REPORT" if M[mid]["type"] in ("banktrust",) and rr.random() < 0.25 else "13F HOLDINGS REPORT"
        if mid == roles["NH"] and q == "Q3":
            conf = {k: v for k, v in h.items() if k in ("W03", "W07", "W09") or (not I[k]["watch"] and rr.random() < 0.04)}
            base = {k: v for k, v in h.items() if k not in conf}
            f0 = Filing(acc_for(mid, d), mid, q, d, "13F-HR", rtype, lines=make_lines(mid, q, base, rr, True), thousands=True)
            filings.append(f0)
            d2 = _bd(dt.date(2023, 1, 12))
            f1 = Filing(acc_for(mid, d2), mid, q, d2, "13F-HR/A", rtype, 1, "NEW HOLDINGS",
                        lines=make_lines(mid, q, conf, rr, False), thousands=False)
            filings.append(f1)
            wd.nh_lines = conf
            continue
        if mid == roles["RS"] and q == "Q3":
            # original carries a keying slip on several positions; the restatement files the whole book
            orig = {}
            for k, v in h.items():
                orig[k] = int(round(v * (1.10 if (I[k]["watch"] and k in ("W02", "W06", "W10")) else 1.0)))
            f0 = Filing(acc_for(mid, d), mid, q, d, "13F-HR", rtype, lines=make_lines(mid, q, orig, rr, True), thousands=True)
            d2 = _bd(dt.date(2022, 12, 2))
            f1 = Filing(acc_for(mid, d2), mid, q, d2, "13F-HR/A", rtype, 1, "RESTATEMENT",
                        lines=make_lines(mid, q, h, rr, True), thousands=True)
            filings += [f0, f1]
            continue
        f = Filing(acc_for(mid, d), mid, q, d, "13F-HR", rtype, lines=make_lines(mid, q, h, rr, thousands), thousands=thousands)
        filings.append(f)

    # ---- option lines (dealers, some hedge funds), every quarter
    by_mid_q = {(f.mid, f.q): f for f in filings if f.form == "13F-HR"}
    dealers = [m["mid"] for m in wd.mgrs if m["type"] == "dealer"]
    hfs = [m["mid"] for m in wd.mgrs if m["type"] == "multistrat" and m["mid"] not in wd.pending4][:10]
    for q in QUARTERS:
        for i in wd.iss:
            ro = W.rng("opt", q, i["iid"])
            budget = (0.0085 if i["watch"] else 0.006) * i["S_oct"] * float(ro.uniform(0.6, 1.0))
            writers = [x for x in dealers + hfs if (x, q) in by_mid_q and x not in wd.pending4]
            k = int(ro.integers(2, 6))
            ws = ro.choice(len(writers), size=k, replace=False)
            amts = ro.dirichlet(np.ones(k)) * budget
            for j, a in zip(ws, amts):
                f = by_mid_q[(writers[j], q)]
                sh = int(round(a / 100.0)) * 100
                if sh <= 0:
                    continue
                v = sh * price[q][i["iid"]]
                v = int(round(v / 1000.0)) if f.thousands else int(round(v))
                f.lines.append(dict(iid=i["iid"], cusip=i["cusip"], name=i["name"], title="CALL" if ro.random() < 0.55 else "PUT",
                                    value=v, shares=sh, sht="SH", putcall="", disc="SOLE", othmgr=""))
                f.lines[-1]["putcall"] = "Call" if f.lines[-1]["title"] == "CALL" else "Put"

    # ---- CUSIP keying in Q3 lines of managers that are not pending at the extract (watchlist),
    #      and in Q4 lines of universe issuers (texture)
    rc = W.rng("cusip")
    repaired = []
    for f in filings:
        if f.form == "13F-NT":
            continue
        for ln in f.lines:
            ii = I[ln["iid"]]
            if ln["putcall"]:
                continue
            if f.q == "Q3" and ii["watch"] and f.mid not in wd.pending4 and f.mid not in (roles["RS"], roles["NH"]) \
                    and ii["iid"] in ("W03", "W04", "W09", "W12") and rc.random() < 0.085:
                if ii["cusip"][0] == "0":
                    ln["cusip"] = ii["cusip"].lstrip("0")
                else:
                    ln["cusip"] = ii["cusip"].lower()
                repaired.append((f.acc, ln["iid"], ln["shares"]))
            elif f.q == "Q4" and not ii["watch"] and rc.random() < 0.004:
                ln["cusip"] = ii["cusip"].lstrip("0") if ii["cusip"][0] == "0" else ii["cusip"].lower()
    # one bad check digit on a Q3 W07 line of a non-pending registered adviser
    for f in filings:
        if f.q == "Q3" and f.mid not in wd.pending4 and M[f.mid]["type"] == "ria" and f.form == "13F-HR":
            hits = [ln for ln in f.lines if ln["iid"] == "W07" and not ln["putcall"]]
            if hits and hits[0]["shares"] > 20_000:
                c = hits[0]["cusip"]
                hits[0]["cusip"] = c[:8] + str((int(c[8]) + 3) % 10)
                repaired.append((f.acc, "W07", hits[0]["shares"]))
                break
    wd.repaired = repaired
    wd.filings = filings
