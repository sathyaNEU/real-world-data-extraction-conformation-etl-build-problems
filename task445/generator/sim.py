"""Simulate three quarters of 13F filing for a closed population of managers and issuers.

Output is a `World` holding (a) the truth: every manager's position per issuer per quarter, (b) the
filings as EDGAR would carry them (submissions, cover pages, information-table lines), with the
realistic mess, and (c) the issuers' cover-page share counts.

Dynamics: an index or ETF sponsor holds a stake of each security read against that quarter's cover-page
count, the stake growing by W.GROW every quarter (its creations buy the whole basket), so its shares move
with its creations and with the issuer's own share count; every other register type is flat in aggregate between quarters while
its individual positions turn over; managers that habitually file after day 34 of the window move little.
Every ask device sits on a bank trust that files every September report by 3 November.
"""
import datetime as dt
from dataclasses import dataclass, field

import numpy as np

import world as W

QUARTERS = ["Q2", "Q3", "Q4"]
SIG_LATE = 0.007
FLOW_SIG = {"multistrat": 0.25, "longonly": 0.15, "ria": 0.18}    # whole-book flows by manager and quarter
SIG_TYPE = {"multistrat": 0.40, "longonly": 0.20, "ria": 0.20, "instit": 0.07, "banktrust": 0.06, "dealer": 0.08}

# ask devices, per cent of the September count (host, watchlist id, kind, size)
A2_LINES = [("A2a", "W02", "CALL", 0.68), ("A2a", "W05", "PUT", 0.80), ("A2b", "W09", "CALL", 0.61),
            ("A2b", "W11", "CALL", 0.45), ("A2b", "W02", "PUT", 0.60)]
TV_LINES = [("TVa", "W01", "COM NEW", 0.50), ("TVa", "W10", "SHS", 0.44), ("TVb", "W07", "CL A", 0.49)]
A3_LINES = [("A3a", "W01", "swap", 0.50), ("A3a", "W04", "check", 0.22), ("A3a", "W06", "swap", 0.23),
            ("A3a", "W08", "check", 0.39), ("A3b", "W10", "check", 0.55), ("A3b", "W12", "swap", 0.53),
            ("A3b", "W01", "check", 0.33), ("A3b", "W06", "check", 0.35)]
KY_LINES = [("KYa", "W03", 0.41), ("KYa", "W04", 0.50), ("KYb", "W09", 0.30), ("KYb", "W12", 0.52)]
# DV-1 (new-holdings host): the trust account's share of each watchlist position, left out of the original.
# DV-2 (restatement host): the original's overstatement of each watchlist position. Both from a deterministic
# search per name (0.0025 steps over 15 to 40 and 12 to 36 per cent, preferring 25 to 30 and 22 to 28) for
# sizes that keep every mishandled September figure at least 0.06 points from the golden and in another
# one-decimal bin, with every Ask A stop in its range; the loop 2 share-count moves make the October count a
# larger hazard, so OTF, AMRB, TAAV, OLPD, SAF and NOPR sit outside the preferred ranges
DV1_T = {"W01": 0.26, "W02": 0.30, "W03": 0.305, "W04": 0.3325, "W05": 0.315, "W06": 0.2825, "W07": 0.285,
         "W08": 0.30, "W09": 0.2725, "W10": 0.27, "W11": 0.2675, "W12": 0.315}
DV2_O = {"W01": 0.28, "W02": 0.28, "W03": 0.315, "W04": 0.135, "W05": 0.1925, "W06": 0.22, "W07": 0.2525,
         "W08": 0.275, "W09": 0.36, "W10": 0.1775, "W11": 0.225, "W12": 0.25}
DV2_KEYED = ("W04", "W09", "W12")
DV2_OPT = [("W01", "CALL", 62_000), ("W06", "PUT", 48_500), ("W10", "CALL", 71_000), ("W02", "PUT", 55_000),
           ("W07", "CALL", 64_500)]
# DV-3: a bank trust's September option positions, kept confidential, added in January when treatment ended
DV3_OPT = [("W03", "CALL", 52_400), ("W08", "PUT", 41_700), ("W11", "CALL", 63_100), ("W05", "CALL", 29_800)]
DV3_DATE = dt.date(2023, 1, 17)
AGENT_RS, AGENT_NH = 950_123, 1_104_659     # the custodian's filing agent and the department's
NH_OMIT = ("W03", "W07", "W09")
A1_NAMES = ("W01", "W02", "W04", "W05", "W06", "W08", "W10", "W11", "W12")
A1_STALE = ("W02", "W05", "W08", "W12")
A1_STALE_RATIO = {'W02': 1.291, 'W05': 1.151, 'W08': 1.161, 'W12': 1.307}       # June over September, the four stale positions
# September count over the October count (watchlist; W08's tender offer set apart), and for the three names
# with an August offering the 10-Q/A count over the 10-Q's
# loop 2: the watchlist's share-count moves in the December window (d, the October-dated count over the
# September count: buybacks, OTF's October follow-on, FENN's shares issued for an acquisition, at-the-market issuance)
_D = {"W01": 0.970, "W03": 1.046, "W04": 0.975, "W05": 1.012, "W06": 0.968, "W07": 1.048, "W09": 1.015, "W12": 0.960}
OCT_U = {"W02": 0.0082, "W10": 0.019, "W11": 0.0101}
OCT_U.update({k: 1 / v - 1 for k, v in _D.items()})
# and in the September window (e, the September count over the June count: GLI's July follow-on, SAF's July
# modified Dutch tender, buybacks)
APR_E = {"W01": 0.985, "W02": 1.050, "W04": 0.990, "W06": 0.988, "W10": 0.960, "W12": 0.980}
A5_V = {"W05": 0.0215, "W09": 0.0255, "W11": 0.0167}


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
    name: str = ""
    addl: str = ""
    sub_q: str = ""          # the period in the submission header, where it differs from the cover page
    dev: bool = False        # a device filing: its accession and pack draws come from their own streams
    ghost: bool = False      # the loop-0 filing's pack draws, not written
    conf: str = ""           # date confidential treatment expired (CONFDENIEDEXPIRED Y)


class World:
    pass


def _bd(d):
    return W.business_day_on_or_after(d)


def _pick(pool, n, rr):
    w = np.exp(np.array([m["size"] for m in pool]) - 20.0)
    w = w / w.sum()
    n = min(n, len(pool))
    idx = rr.choice(len(pool), size=n, replace=False, p=w)
    return [pool[j] for j in idx]


def build():
    wd = World()
    mgrs = W.build_managers()
    iss = W.build_issuers()
    r = W.rng("sim")
    M = {m["mid"]: m for m in mgrs}
    I = {i["iid"]: i for i in iss}
    wd.mgrs, wd.iss, wd.M, wd.I = mgrs, iss, M, I

    # ------------------------------------------------ habits: early filers file by day 33, late ones after 35
    for m in mgrs:
        if m["type"] == "passive":
            continue
        h = m["habit"]
        if m["type"] == "banktrust":
            h = min(h, 28.0)
        if m["type"] == "dealer":
            h = min(h, 29.0)
        if 31.5 < h < 36.0:
            h = 31.0 if h < 34.0 else 37.0
        m["habit"] = h

    # ------------------------------------------------ special roles
    by_type = {}
    for m in mgrs:
        by_type.setdefault(m["type"], []).append(m)
    passive = by_type["passive"]
    P0, P1 = passive[0], passive[1]
    late_passive = passive[2:]
    lo = sorted(by_type["longonly"], key=lambda m: m["mid"])
    bt = sorted(by_type["banktrust"], key=lambda m: m["mid"])
    ria = sorted(by_type["ria"], key=lambda m: m["mid"])
    TK = lo[0]; TK.update(habit=24.0, size=23.2)                # December values left in thousands
    SP = bt[0]; SP.update(habit=16.0, size=23.0)                # several lines per position
    GA1, GA2 = lo[1], lo[2]
    GA1.update(habit=19.0, size=22.6); GA2.update(habit=26.0, size=22.0)
    hosts = {"RS": bt[1], "NH": bt[2], "A1": bt[3], "A2a": bt[4], "A2b": bt[7], "TVa": bt[8], "TVb": bt[9],
             "A3a": bt[10], "A3b": bt[11], "KYa": bt[12], "KYb": bt[13]}
    for k, m in hosts.items():
        m.update(habit=min(m["habit"], 24.0), size=max(m["size"], 21.0))
    hosts["RS"]["habit"] = 7.0
    hosts["NH"]["habit"] = 14.0
    hosts["A1"]["habit"] = 12.0
    fam_name = GA1["stem"] + " Investment Group"
    GA2["stem"] = GA1["stem"]
    GA2["disp"] = GA1["stem"] + " Capital Advisors LP"
    GA2["name"] = GA2["disp"].upper()
    GA1["family"] = GA2["family"] = fam_name
    for m in mgrs:
        if m["family"] is None:
            m["family"] = ""
    for a, b in [(bt[5], bt[6]), (ria[10], ria[11]), (lo[20], lo[21])]:
        b["stem"] = a["stem"]
        b["disp"] = a["stem"] + " " + b["disp"].split(" ", 1)[1]
        b["name"] = b["disp"].upper()
        a["family"] = b["family"] = a["stem"] + " Financial"
    wd.roles = dict(P0=P0["mid"], P1=P1["mid"], TK=TK["mid"], SP=SP["mid"], GA1=GA1["mid"], GA2=GA2["mid"],
                    late_passive=[m["mid"] for m in late_passive], **{k: m["mid"] for k, m in hosts.items()})
    special = {P0["mid"], P1["mid"], TK["mid"], SP["mid"], GA1["mid"], GA2["mid"]} | {m["mid"] for m in hosts.values()}
    wd.special = special
    wd.new_name = {P0["mid"]: P0["stem"].upper() + " GLOBAL INDEXING INC"}

    notice = [m["mid"] for m in ria[150 - 12:]]
    attrit = [m["mid"] for m in ria[120:124]]          # stopped filing before 2022: in the register only
    newq4 = [m["mid"] for m in ria[124:130]]
    for x in newq4:
        M[x]["habit"] = min(M[x]["habit"], 30.0)
    wd.notice, wd.attrit, wd.newq4 = set(notice), set(attrit), set(newq4)

    # ------------------------------------------------ filing days
    fdate = {}
    for m in mgrs:
        mid = m["mid"]
        if mid in wd.attrit:
            continue
        for q in QUARTERS:
            if q in ("Q2", "Q3") and mid in wd.newq4:
                continue
            sd = 0.5 if m["type"] == "passive" else 1.3
            d = m["habit"] + float(r.normal(0, sd))
            d = min(max(d, 4.0), 45.0)
            if m["type"] != "passive":
                d = min(d, 33.0) if m["habit"] < 34 else max(d, 36.0)
            day = _bd(W.PERIODS[q] + dt.timedelta(days=int(round(d))))
            if day > W.DEADLINE[q]:
                day = W.DEADLINE[q]
                while day.weekday() >= 5 or day in W.HOLIDAYS:
                    day -= dt.timedelta(days=1)
            fdate[(mid, q)] = day
    fdate[(hosts["RS"]["mid"], "Q3")] = dt.date(2022, 10, 7)
    fdate[(hosts["NH"]["mid"], "Q3")] = dt.date(2022, 10, 14)
    fdate[(hosts["A1"]["mid"], "Q3")] = dt.date(2022, 10, 12)
    wd.fdate = fdate
    cut = {q: W.PERIODS[q] + dt.timedelta(days=W.CUT_DAY) for q in QUARTERS}
    wd.cut = cut
    alive = {m["mid"] for m in mgrs if m["mid"] not in wd.notice and m["mid"] not in wd.attrit}
    late = {x for x in alive if all(fdate[(x, q)] > cut[q] for q in QUARTERS if (x, q) in fdate)}
    early = {x for x in alive if all(fdate[(x, q)] <= cut[q] for q in QUARTERS if (x, q) in fdate)}
    assert late | early == alive and not (late & early)
    assert all(M[x]["type"] not in ("banktrust", "dealer") for x in late)
    wd.late, wd.early = late, early
    wd.pending4 = {x for x in late if (x, "Q3") in fdate}

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
        i["S_jul"] = int(round(i["S_oct"] * (1 + max(0.004, rr.normal(0.011, 0.007)))))
        i["S_jan"] = int(round(i["S_oct"] * (1 - abs(rr.normal(0.0012, 0.0015)))))
        i["S_apr"] = int(round(i["S_jul"] * (1 + rr.normal(0.001, 0.002))))
        if i["iid"] in OCT_U:
            i["S_jul"] = int(round(i["S_oct"] * (1 + OCT_U[i["iid"]])))
            i["S_apr"] = int(round(i["S_jul"] * (1 + rr.normal(0.001, 0.002))))
            if i["iid"] in APR_E:
                i["S_apr"] = int(round(i["S_jul"] / APR_E[i["iid"]]))
        i["S_sep"] = i["S_jul"]
    # texture: about one in ten other covered securities moves its count 3 to 8 per cent in one window
    rx = W.rng("so-texture")
    for i in iss:
        if i["watch"]:
            continue
        u, w_, mv = float(rx.random()), float(rx.random()), float(rx.uniform(0.03, 0.08)) * (1 if rx.random() < 0.55 else -1)
        if u < 0.10:
            if w_ < 0.5:          # the December window: the September count against the October-dated count
                i["S_jul"] = i["S_sep"] = int(round(i["S_oct"] / (1 + mv)))
                i["S_apr"] = int(round(i["S_jul"] * (1 + float(rx.normal(0.001, 0.002)))))
            else:                 # the September window: the June count against the September count
                i["S_apr"] = int(round(i["S_jul"] / (1 + mv)))
    I["W08"]["S_jul"] = I["W08"]["S_sep"] = int(round(I["W08"]["S_oct"] / 0.9463))   # September tender offer
    I["W08"]["S_apr"] = I["W08"]["S_jul"] + 18_400
    for k, iid in enumerate(W.A5_NAMES):          # August offering left out of the 10-Q cover; 10-Q/A count
        rr = W.rng("a5", iid)
        i = I[iid]
        i["S_A5"] = i["S_sep"] = int(round(i["S_oct"] * (1 + OCT_U[iid])))
        i["S_jul"] = int(round(i["S_A5"] / (1 + A5_V[iid])))
        i["S_apr"] = int(round(i["S_jul"] * (1 + rr.normal(0.001, 0.002))))

    # ------------------------------------------------ positions
    pos = {q: {} for q in QUARTERS}
    late_others = [M[x] for x in sorted(late) if M[x]["type"] != "passive" and (x, "Q3") in fdate]
    gen_early = [m for m in mgrs if m["mid"] in early and m["mid"] not in special and m["type"] != "passive"
                 and m["mid"] not in wd.newq4]
    univ_early = [m for m in mgrs if m["mid"] in early and m["type"] != "passive" and m["mid"] not in wd.newq4
                  and m["mid"] not in (TK["mid"], SP["mid"], GA1["mid"], GA2["mid"])]
    generic = {q: {} for q in QUARTERS}     # (mid, iid) -> shares, generic early holders (balanced below)
    dev = {}
    for host, iid, title, pct in TV_LINES:
        dev[(host, iid)] = pct
    for host, iid, kind, pct in A3_LINES:
        dev[(host, iid)] = dev.get((host, iid), 0) + pct
    for host, iid, pct in KY_LINES:
        dev[(host, iid)] = pct
    rf = W.rng("flow")
    flow = {(m["mid"], q): (float(rf.normal(0, FLOW_SIG.get(m["type"], 0.0))) if m["type"] in FLOW_SIG else 0.0)
            for m in mgrs for q in ("43", "32")}
    for i in iss:
        rr = W.rng("pos", i["iid"])
        iid, S = i["iid"], i["S_oct"]
        S3 = i["S_sep"]
        p4, p3, p2 = {}, {}, {}
        # --- index and ETF sponsors that file late
        if i["watch"]:
            LPd, LOs = W.PEND[iid]
            LPd, LOs = LPd / 100 * S, LOs / 100 * S
        else:
            T = i["A"] / 100 * S
            L = (1 - i["f"]) * T
            share = float(rr.uniform(0.55, 0.72))
            LPd, LOs = share * L, (1 - share) * L
        # each complex holds a stake of the security, read against the quarter's OM-4 count, the stake growing
        # W.GROW a quarter: its shares move with its creations and with the issuer's own share count
        dq, jq = i["S_oct"] / i["S_sep"], i["S_sep"] / i["S_apr"]
        w = rr.dirichlet(np.full(len(late_passive), 6.0)) * LPd
        for m, v in zip(late_passive, w):
            s3 = v / (W.GROW * dq)
            p3[m["mid"]] = s3
            p4[m["mid"]] = s3 * W.GROW * dq * (1 + rr.normal(0, 0.0002))
            p2[m["mid"]] = s3 / (W.GROW * jq) * (1 + rr.normal(0, 0.0002))
        # --- every other type that files late
        pool = [m for m in late_others if m["type"] == "multistrat"] if iid == "W07" else late_others
        nl = int(rr.integers(14, 30)) if i["watch"] else int(rr.integers(8, 22))
        chosen = _pick(pool, nl, rr)
        w = rr.dirichlet(np.full(len(chosen), 1.2)) * LOs
        for m, v in zip(chosen, w):
            p3[m["mid"]] = p3.get(m["mid"], 0) + v
        for m in chosen:
            v = p3[m["mid"]]
            p4[m["mid"]] = v * (1 + rr.normal(0, SIG_LATE))
            p2[m["mid"]] = v * (1 + rr.normal(0, SIG_LATE))
        # --- early index sponsors (top holders)
        if i["watch"]:
            p4[P0["mid"]] = (0.090 + rr.uniform(0, 0.010) + (0.006 if iid == "W03" else 0)) * S
            p4[P1["mid"]] = (0.064 + rr.uniform(0, 0.010)) * S
        else:
            E = i["A"] / 100 * S - LPd - LOs
            p4[P0["mid"]] = (0.12 + rr.uniform(0, 0.03)) * E
            p4[P1["mid"]] = (0.08 + rr.uniform(0, 0.03)) * E
        for x in (P0["mid"], P1["mid"]):
            p3[x] = p4[x] / (W.GROW * dq) * (1 + rr.normal(0, 0.0002))
            p2[x] = p3[x] / (W.GROW * jq) * (1 + rr.normal(0, 0.0002))
        # --- other early specials (December-sized top holders, September-sized device hosts)
        if i["watch"]:
            s4 = {}
            if iid in ("W02", "W08", "W11"):
                s4[TK["mid"]] = (0.118 + rr.uniform(0, 0.006)) * S
            else:
                s4[TK["mid"]] = (0.010 + rr.uniform(0, 0.012)) * S
            if iid in ("W04", "W09"):
                s4[SP["mid"]] = (0.112 + rr.uniform(0, 0.006)) * S
            else:
                s4[SP["mid"]] = (0.006 + rr.uniform(0, 0.010)) * S
            if iid in ("W05", "W12"):
                s4[GA1["mid"]] = p4[P0["mid"]] * 0.885
                s4[GA2["mid"]] = (0.040 + rr.uniform(0, 0.006)) * S
            for x, v in s4.items():
                p4[x] = v
                p3[x] = v * float(np.exp(-rr.normal(0, 0.03)))
                p2[x] = p3[x] * float(np.exp(-rr.normal(0, 0.03)))
            s3 = {hosts["RS"]["mid"]: (0.016 + rr.uniform(0, 0.010)) * S3,
                  hosts["NH"]["mid"]: (0.020 + rr.uniform(0, 0.010)) * S3}
            if iid in A1_NAMES:
                s3[hosts["A1"]["mid"]] = (0.010 + rr.uniform(0, 0.005)) * S3
            for (h, ii), pct in dev.items():
                if ii == iid:
                    s3[hosts[h]["mid"]] = s3.get(hosts[h]["mid"], 0) + pct / 100 * S3
            for h in ("A2a", "A2b"):
                s3[hosts[h]["mid"]] = (0.003 + rr.uniform(0, 0.004)) * S3
            for x, v in s3.items():
                p3[x] = v
                p4[x] = v * float(np.exp(rr.normal(0, 0.03)))
                p2[x] = v * float(np.exp(-rr.normal(0, 0.03)))
                if x == hosts["A1"]["mid"] and iid in A1_STALE:
                    p2[x] = v * A1_STALE_RATIO[iid]
        # --- small new filers in December
        for mid in newq4:
            if rr.random() < 0.35:
                p4[mid] = float(rr.uniform(0.0002, 0.0012)) * S
        # --- generic early holders, December
        target4 = i["A"] / 100 * S
        rest = target4 - sum(p4.values())
        assert rest > 0.10 * target4, (iid, rest / S)
        ne = int(rr.integers(110, 230)) if i["watch"] else int(rr.integers(40, 190))
        cand = gen_early if i["watch"] else [m for m in univ_early if m["mid"] not in p4]
        ch = _pick(cand, ne, rr)
        we = rr.dirichlet(np.full(len(ch), 0.9)) * rest
        cap = 0.045 * S
        over = np.clip(we - cap, 0, None).sum()
        we = np.minimum(we, cap)
        we = we + over * (cap - we) / (cap - we).sum()
        g4, g3, g2 = {}, {}, {}
        for m, v in zip(ch, we):
            g4[m["mid"]] = v
        for mid, v in g4.items():
            if rr.random() < 0.07:
                continue
            g3[mid] = v * float(np.exp(-rr.normal(0, SIG_TYPE[M[mid]["type"]]) - flow[(mid, "43")]))
        cand3 = [m for m in cand if m["mid"] not in g4]
        for m in _pick(cand3, int(rr.integers(4, 12)), rr):
            g3[m["mid"]] = float(rr.uniform(0.0004, 0.004)) * S
        for mid, v in g3.items():
            if rr.random() < 0.06:
                continue
            g2[mid] = v * float(np.exp(-rr.normal(0, SIG_TYPE[M[mid]["type"]]) - flow[(mid, "32")]))
        cand2 = [m for m in cand if m["mid"] not in g3]
        for m in _pick(cand2, int(rr.integers(2, 8)), rr):
            g2[m["mid"]] = float(rr.uniform(0.0004, 0.004)) * S
        for q, src in (("Q4", p4), ("Q3", p3), ("Q2", p2)):
            for mid, v in src.items():
                pos[q][(mid, iid)] = v
        for q, src in (("Q4", g4), ("Q3", g3), ("Q2", g2)):
            for mid, v in src.items():
                generic[q][(mid, iid)] = v
                pos[q][(mid, iid)] = pos[q].get((mid, iid), 0) + v

    # ------------------------------------------------ balance: every type other than the sponsors is flat in
    # aggregate among managers that filed both reports, over the twelve names and over every other security
    re_ = W.rng("eps")
    types = [t for t, *_ in W.MGR_TYPES if t != "passive"]
    eps = {}
    for scope in ("watch", "univ"):
        for pair in ("43", "32"):
            for t in types:
                e = float(re_.uniform(0.0001, 0.0003)) * (1 if re_.random() < 0.5 else -1)
                eps[(scope, pair, t)] = e
    wd.eps = eps
    watch = [i["iid"] for i in iss if i["watch"]]
    wset = set(watch)

    def ipf(qa, qb, pair, col_target, slack):
        """scale generic early positions of quarter qb so that, per type, sum(qa)/sum(qb) = 1 + eps over the
        watchlist (and over the other securities), and per watch name qb's total meets col_target"""
        for scope in ("watch", "univ"):
            inscope = (lambda iid: iid in wset) if scope == "watch" else (lambda iid: iid not in wset)
            rows = {}
            for t in types:
                num = sum(v for (mid, iid), v in pos[qa].items() if inscope(iid)
                          and M[mid]["type"] == t and mid in early and mid not in wd.newq4)
                fixed = sum(v for (mid, iid), v in pos[qb].items() if inscope(iid)
                            and M[mid]["type"] == t and mid in early and (mid, iid) not in generic[qb])
                rows[t] = num / (1 + eps[(scope, pair, t)]) - fixed
            X = {k: generic[qb][k] for k in generic[qb] if inscope(k[1])}
            bytype = {t: [k for k in X if M[k[0]]["type"] == t] for t in types}
            if scope == "watch":
                cols = dict(col_target)
                cols[slack] = sum(rows.values()) - sum(v for c, v in cols.items() if c != slack)
                assert cols[slack] > 0, cols[slack]
                bycol = {c: [k for k in X if k[1] == c] for c in watch}
            for _ in range(400 if scope == "watch" else 1):
                for t in types:
                    s = sum(X[k] for k in bytype[t])
                    if s > 0:
                        f = rows[t] / s
                        for k in bytype[t]:
                            X[k] *= f
                if scope == "watch":
                    for c in watch:
                        s = sum(X[k] for k in bycol[c])
                        f = cols[c] / s
                        for k in bycol[c]:
                            X[k] *= f
            for t in types:
                s = sum(X[k] for k in bytype[t])
                assert abs(s / rows[t] - 1) < 1e-7, ("balance", qb, scope, t, s / rows[t])
            for k, v in X.items():
                pos[qb][k] = pos[qb][k] - generic[qb][k] + v
                generic[qb][k] = v

    colS = {}
    for i in iss:
        if not i["watch"] or i["iid"] == W.SEP_SLACK:
            continue
        tot = i["sep"] / 100 * i["S_sep"]
        fixed = sum(v for (mid, iid), v in pos["Q3"].items() if iid == i["iid"] and (mid, iid) not in generic["Q3"])
        colS[i["iid"]] = tot - fixed
    ipf("Q4", "Q3", "43", colS, W.SEP_SLACK)
    colJ = {}
    for c in watch:
        if c == W.JUN_SLACK:
            continue
        g3 = sum(v for (mid, iid), v in generic["Q3"].items() if iid == c)
        f3 = sum(v for (mid, iid), v in pos["Q3"].items() if iid == c and mid in early and (mid, iid) not in generic["Q3"])
        f2 = sum(v for (mid, iid), v in pos["Q2"].items() if iid == c and mid in early and (mid, iid) not in generic["Q2"])
        colJ[c] = (g3 + f3) / W.JUN_MOVE.get(c, 1.0) - f2
    ipf("Q3", "Q2", "32", colJ, W.JUN_SLACK)

    for q in QUARTERS:
        pos[q] = {k: int(round(v)) for k, v in pos[q].items() if v >= 1}
        pos[q] = {k: v for k, v in pos[q].items() if (k[0], q) in fdate}
    wd.pos = pos
    wd.hosts = {k: m["mid"] for k, m in hosts.items()}
    build_filings(wd, r)
    return wd


def _acc(cik, yy, seq):
    return f"{cik:010d}-{yy:02d}-{seq:06d}"


ABBR = {"THERMAL": "THERM", "HOLDINGS": "HLDGS", "INSTRUMENTS": "INSTRS", "BIOSCIENCES": "BIOSCI",
        "SYSTEMS": "SYS", "INDUSTRIES": "INDS", "THERAPEUTICS": "THERAPTC", "LOGISTICS": "LOGISTCS",
        "SOFTWARE": "SOFTWRE", "MATERIALS": "MATLS", "ENERGY": "ENRGY", "FINANCIAL": "FINL", "BRANDS": "BRNDS",
        "NETWORKS": "NETWKS", "MEDICAL": "MED", "SEMICONDUCTOR": "SEMICONDTR", "FOODS": "FDS", "REALTY": "RLTY",
        "ROBOTICS": "ROBOTCS", "AEROSPACE": "AEROSP", "WATER": "WTR", "PHARMA": "PHARM", "PAYMENTS": "PMTS",
        "LABS": "LABS", "OUTDOOR": "OUTDR", "PACKAGING": "PKG", "MOBILITY": "MOBLTY", "ANALYTICS": "ANALYTCS",
        "CORPORATION": "CORP", "GROUP": "GRP", "INC": "", "CO": "", "LTD": "LTD", "CORP": "CORP"}


def abbreviate(name):
    w = name.split()
    out = [w[0]] + [ABBR.get(x, x) for x in w[1:]]
    return " ".join(x for x in out if x)


def build_filings(wd, r):
    M, I = wd.M, wd.I
    roles = wd.roles
    H = wd.hosts
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
    titles = {}
    for h, iid, t, pct in TV_LINES:
        titles[(H[h], iid)] = t

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
            elif mm["type"] in ("banktrust", "passive") and mid not in wd.special and rr.random() < 0.30 and sh > 50:
                a = int(sh * rr.uniform(0.2, 0.8)); parts = [a, sh - a]
            title = titles.get((mid, iid), "COM") if q == "Q3" else "COM"
            for k, s in enumerate(parts):
                v = s * px
                v = int(round(v / 1000.0)) if thousands else int(round(v))
                disc = "SOLE" if k == 0 else ("DFND" if mm["type"] in ("banktrust", "passive") else "OTR")
                lines.append(dict(iid=iid, cusip=ii["cusip"], name=ii["name"], title=title,
                                  value=v, shares=int(s), sht="SH", putcall="", disc=disc,
                                  othmgr="" if k == 0 else str(k)))
        return lines

    filings = []
    hold_by = {q: {} for q in QUARTERS}
    for q in QUARTERS:
        for (mid, iid), sh in wd.pos[q].items():
            hold_by[q].setdefault(mid, {})[iid] = sh

    rr = W.rng("lines")
    rs_, nh_, a1_ = H["RS"], H["NH"], H["A1"]
    rd = W.rng("dev-acc")
    used_seq = {}

    def dev_acc(cik, d):
        yy = d.year % 100
        while True:
            seq = int(rd.integers(20_000, 90_000))
            a = _acc(cik, yy, seq)
            if a not in used_seq:
                used_seq[a] = 1
                return a
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
        rtype = "13F COMBINATION REPORT" if M[mid]["type"] == "banktrust" and mid not in wd.special and rr.random() < 0.25 else "13F HOLDINGS REPORT"
        name = wd.new_name.get(mid, "") if q == "Q4" else ""
        addl = "Market values in this report are stated in thousands of dollars." if (mid == roles["TK"] and q == "Q4") else ""
        if mid == nh_ and q == "Q3":
            # DV-1: the original leaves out a second trust account's share of every watchlist position; on 31
            # October the department files a NEW HOLDINGS amendment (amendment 1) adding it, and the custodian's
            # agent files a RESTATEMENT (amendment 2) with one merged line per name, the same afternoon
            tr = {k: int(round(v * DV1_T[k])) for k, v in h.items() if k in DV1_T}
            base = {k: (v - tr[k] if k in tr else v) for k, v in h.items()}
            f0 = Filing(acc_for(mid, d), mid, q, d, "13F-HR", rtype, lines=make_lines(mid, q, base, rr, True), thousands=True)
            for ln in f0.lines:
                if ln["iid"] in NH_OMIT:
                    ln["devdraw"] = True      # lines the loop-0 original left out draw from the device stream
            d2 = dt.date(2022, 10, 31)
            ghost = Filing(acc_for(mid, d2), mid, q, d2, "13F-HR/A", rtype, 1, "NEW HOLDINGS",
                           lines=[dict(disc="SOLE", putcall="") for _ in NH_OMIT], thousands=True)
            ghost.ghost = True                # the loop-0 amendment's draws, so every other row keeps its bytes
            f1 = Filing(dev_acc(AGENT_NH, d2), mid, q, d2, "13F-HR/A", rtype, 1, "NEW HOLDINGS",
                        lines=make_lines(mid, q, tr, rr, True), thousands=True)
            f2 = Filing(dev_acc(AGENT_RS, d2), mid, q, d2, "13F-HR/A", rtype, 2, "RESTATEMENT",
                        lines=make_lines(mid, q, h, rr, True), thousands=True)
            f1.dev = f2.dev = True
            filings += [f0, ghost, f1, f2]
            continue
        if mid == rs_ and q == "Q3":
            # DV-2: the original overstates every watchlist position (a terminated custody account left in the
            # run); the restatement restates every position, adds option lines the original left out and keys a
            # few CUSIPs off-format; its submission header carries the June period (the agent's June template)
            orig = {k: int(round(v * (1 + DV2_O[k]))) if k in DV2_O else v for k, v in h.items()}
            f0 = Filing(acc_for(mid, d), mid, q, d, "13F-HR", rtype, lines=make_lines(mid, q, orig, rr, True), thousands=True)
            d2 = dt.date(2022, 10, 28)
            f1 = Filing(acc_for(mid, d2), mid, q, d2, "13F-HR/A", rtype, 1, "RESTATEMENT",
                        lines=make_lines(mid, q, h, rr, True), thousands=True)
            f1.sub_q = "Q2"
            for ln in f1.lines:
                if ln["iid"] in DV2_KEYED:
                    c = I[ln["iid"]]["cusip"]
                    ln["cusip"] = c.lstrip("0") if c[0] == "0" else c.lower()
            for iid, t, sh in DV2_OPT:
                v = int(round(sh * price["Q3"][iid] / 1000.0))
                f1.lines.append(dict(iid=iid, cusip=I[iid]["cusip"], name=I[iid]["name"], title=t, value=v,
                                     shares=sh, sht="SH", putcall=t.title(), disc="SOLE", othmgr=""))
            filings += [f0, f1]
            continue
        if mid == a1_ and q == "Q3":
            orig = {k: (hold_by["Q2"][mid][k] if k in A1_STALE else v) for k, v in h.items()}
            f0 = Filing(acc_for(mid, d), mid, q, d, "13F-HR", rtype, lines=make_lines(mid, q, orig, rr, True), thousands=True)
            d2 = dt.date(2022, 10, 26)
            f1 = Filing(acc_for(mid, d2), mid, q, d2, "13F-HR/A", rtype, 1, "RESTATEMENT",
                        lines=make_lines(mid, q, h, rr, True), thousands=True)
            filings += [f0, f1]
            continue
        filings.append(Filing(acc_for(mid, d), mid, q, d, "13F-HR", rtype, lines=make_lines(mid, q, h, rr, thousands),
                              thousands=thousands, name=name, addl=addl))

    # ---- option lines with the put/call field filled (dealers and bank trust departments), every quarter
    by_mid_q = {(f.mid, f.q): f for f in filings if f.form == "13F-HR" and not f.amend_no}
    writers_all = sorted(m["mid"] for m in wd.mgrs if m["type"] in ("dealer", "banktrust") and m["mid"] not in wd.special)
    for q in QUARTERS:
        for i in wd.iss:
            ro = W.rng("opt", q, i["iid"])
            budget = (0.0085 if i["watch"] else 0.006) * i["S_oct"] * float(ro.uniform(0.6, 1.0))
            if q == "Q4" and i["iid"] == "W07":
                continue
            if q == "Q4" and i["iid"] == "W03":
                budget *= 0.12
            writers = [x for x in writers_all if (x, q) in by_mid_q]
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
                t = "CALL" if ro.random() < 0.55 else "PUT"
                f.lines.append(dict(iid=i["iid"], cusip=i["cusip"], name=i["name"], title=t, value=v, shares=sh,
                                    sht="SH", putcall=t.title(), disc="SOLE", othmgr=""))

    # ---- A2: options keyed only in the title of class (two wealth departments' filing software)
    byq3 = {f.mid: f for f in filings if f.q == "Q3" and f.form == "13F-HR" and not f.amend_no}
    wd.a2 = []
    for h, iid, t, pct in A2_LINES:
        f = byq3[H[h]]
        i = I[iid]
        sh = int(round(pct / 100 * i["S_sep"] / 100.0)) * 100
        v = int(round(sh * price["Q3"][iid] * 0.06 / 1000.0))
        f.lines.append(dict(iid=iid, cusip=i["cusip"], name=i["name"], title=t, value=v, shares=sh,
                            sht="SH", putcall="", disc="SOLE", othmgr=""))
        wd.a2.append((f.acc, iid, sh))

    # ---- A3: failed check digits under abbreviated issuer names; keyed CUSIPs (leading zeros, lower case)
    allbase = {i["cusip"][:8] for i in wd.iss}
    wd.a3, wd.ky = [], []
    for h, iid, kind, pct in A3_LINES:
        f = byq3[H[h]]
        i = I[iid]
        for ln in f.lines:
            if ln["iid"] == iid and not ln["putcall"]:
                c = i["cusip"]
                if kind == "swap":
                    b8 = c[:8]
                    for a in range(1, 7):
                        nb = b8[:a] + b8[a + 1] + b8[a] + b8[a + 2:]
                        if nb != b8 and nb not in allbase and W.cusip_check(nb) != c[8]:
                            break
                    else:
                        raise AssertionError(("no transposition", iid))
                    ln["cusip"] = nb + c[8]
                else:
                    ln["cusip"] = c[:8] + str((int(c[8]) + 4) % 10)
                ln["name"] = abbreviate(i["name"])
                wd.a3.append((f.acc, iid, kind, ln["shares"]))
    for h, iid, pct in KY_LINES:
        f = byq3[H[h]]
        i = I[iid]
        for ln in f.lines:
            if ln["iid"] == iid and not ln["putcall"]:
                ln["cusip"] = i["cusip"].lstrip("0") if i["cusip"][0] == "0" else i["cusip"].lower()
                wd.ky.append((f.acc, iid, ln["shares"]))
    # ---- DV-3: options a bank trust kept confidential, added in January (NEW HOLDINGS, CONFDENIEDEXPIRED Y)
    plain_bt = [m["mid"] for m in sorted(wd.mgrs, key=lambda m: m["mid"]) if m["type"] == "banktrust"
                and m["mid"] not in wd.special and not m["family"]]
    dv3 = plain_bt[12]
    wd.roles["DV3"] = dv3
    lines = []
    for iid, t, sh in DV3_OPT:
        lines.append(dict(iid=iid, cusip=I[iid]["cusip"], name=I[iid]["name"], title=t,
                          value=int(round(sh * price["Q3"][iid])), shares=sh, sht="SH", putcall=t.title(),
                          disc="SOLE", othmgr=""))
    f3 = Filing(dev_acc(M[dv3]["cik"], DV3_DATE), dv3, "Q3", DV3_DATE, "13F-HR/A", byq3[dv3].reporttype, 1,
                "NEW HOLDINGS", lines=lines, thousands=False, conf="13-JAN-2023")
    f3.dev = True
    filings.append(f3)
    # ---- ordinary same-day pairs: three departments re-file their September report in full the day they filed
    #      it (a cover-page or voting-authority correction), through either filing agent
    wd.sameday = []
    for mid in plain_bt[13:16]:
        f0 = byq3[mid]
        agent = AGENT_RS if len(wd.sameday) % 2 == 0 else AGENT_NH
        fa = Filing(dev_acc(agent, f0.date), mid, "Q3", f0.date, "13F-HR/A", f0.reporttype, 1, "RESTATEMENT",
                    lines=[dict(ln) for ln in f0.lines], thousands=f0.thousands)
        fa.dev = True
        filings.append(fa)
        wd.sameday.append(mid)
    # texture: December lines of other covered securities keyed off-format by bank trust departments
    rc = W.rng("cusip")
    for f in filings:
        if f.q != "Q4" or f.form == "13F-NT" or M[f.mid]["type"] != "banktrust":
            continue
        for ln in f.lines:
            ii = I[ln["iid"]]
            if not ii["watch"] and not ln["putcall"] and rc.random() < 0.01:
                ln["cusip"] = ii["cusip"].lstrip("0") if ii["cusip"][0] == "0" else ii["cusip"].lower()
    wd.filings = filings
