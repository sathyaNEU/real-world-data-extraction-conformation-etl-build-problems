"""The clean truth: Ostrander's sixty DCs week by week from fiscal 2021 week 1 to fiscal 2026 week 44, the injury process
behind every recordable case, and the FY2027 operating plan. Nothing in this module reads or writes a shipped file; the
records, documents and asks are written from it by the other modules."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np
import pandas as pd

import common as K

# (dc number, city, state, WMS code, EHS site name) ; the WMS codes are the DCs' location codes, the EHS names the
# establishment names on each DC's OSHA log
DCS = [
    (104, "Groveport", "OH", "GRV1", "Groveport DC"), (106, "Obetz", "OH", "OBZ1", "Obetz DC"),
    (109, "West Jefferson", "OH", "WJF1", "West Jefferson DC"), (112, "Lockbourne", "OH", "LKB1", "Lockbourne DC"),
    (115, "Mansfield", "OH", "MNF1", "Mansfield DC"), (117, "Vandalia", "OH", "VAN1", "Vandalia DC"),
    (121, "West Chester", "OH", "WCH1", "West Chester DC"), (123, "West Chester", "OH", "WCH2", "West Chester DC 2"),
    (203, "Plainfield", "IN", "PLF1", "Plainfield DC"), (205, "Whitestown", "IN", "WTN1", "Whitestown DC"),
    (208, "Greenwood", "IN", "GRW1", "Greenwood DC"), (211, "Fort Wayne", "IN", "FTW1", "Fort Wayne DC"),
    (302, "Joliet", "IL", "JOL1", "Joliet DC"), (304, "Joliet", "IL", "JOL2", "Joliet DC 2"),
    (306, "Romeoville", "IL", "RMV1", "Romeoville DC"), (309, "Elwood", "IL", "ELW1", "Elwood DC"),
    (311, "Rockford", "IL", "RKF1", "Rockford DC"), (314, "DeKalb", "IL", "DKB1", "DeKalb DC"),
    (402, "Romulus", "MI", "RML1", "Romulus DC"), (405, "Grand Rapids", "MI", "GRR1", "Grand Rapids DC"),
    (407, "Lansing", "MI", "LAN1", "Lansing DC"), (501, "Carlisle", "PA", "CRL1", "Carlisle DC"),
    (503, "Carlisle", "PA", "CRL2", "Carlisle DC 2"), (506, "Bethlehem", "PA", "BTH1", "Bethlehem DC"),
    (508, "York", "PA", "YRK1", "York DC"), (511, "Breinigsville", "PA", "BRN1", "Breinigsville DC"),
    (513, "Pittston", "PA", "PTS1", "Pittston DC"), (602, "Shepherdsville", "KY", "SHP1", "Shepherdsville DC"),
    (604, "Florence", "KY", "FLR1", "Florence DC"), (607, "Walton", "KY", "WLT1", "Walton DC"),
    (609, "Lexington", "KY", "LEX1", "Lexington DC"), (702, "Lebanon", "TN", "LBN1", "Lebanon DC"),
    (704, "Smyrna", "TN", "SMY1", "Smyrna DC"), (706, "Mount Juliet", "TN", "MTJ1", "Mount Juliet DC"),
    (709, "Memphis", "TN", "MEM1", "Memphis DC"), (712, "Memphis", "TN", "MEM2", "Memphis DC 2"),
    (802, "McDonough", "GA", "MCD1", "McDonough DC"), (804, "Jackson", "GA", "JKS1", "Jackson DC"),
    (807, "Braselton", "GA", "BRS1", "Braselton DC"), (809, "Savannah", "GA", "SAV1", "Savannah DC"),
    (811, "Union City", "GA", "UNC1", "Union City DC"), (902, "Kernersville", "NC", "KRN1", "Kernersville DC"),
    (905, "Mebane", "NC", "MEB1", "Mebane DC"), (907, "Gastonia", "NC", "GST1", "Gastonia DC"),
    (910, "Concord", "NC", "CNC1", "Concord DC"), (1002, "Fort Worth", "TX", "FTWT", "Fort Worth DC"),
    (1004, "Wilmer", "TX", "WLM1", "Wilmer DC"), (1007, "Katy", "TX", "KTY1", "Katy DC"),
    (1009, "San Antonio", "TX", "SAT1", "San Antonio DC"), (1011, "Lancaster", "TX", "LNC1", "Lancaster DC"),
    (1102, "Kenosha", "WI", "KNS1", "Kenosha DC"), (1104, "Pleasant Prairie", "WI", "PLP1", "Pleasant Prairie DC"),
    (1106, "Sun Prairie", "WI", "SNP1", "Sun Prairie DC"), (1108, "Oak Creek", "WI", "OKC1", "Oak Creek DC"),
    (1109, "Waukesha", "WI", "WKS1", "Waukesha DC"), (1111, "De Pere", "WI", "DPR1", "De Pere DC"),
    (125, "Hebron", "OH", "HEB1", "Hebron DC"), (214, "Lebanon", "IN", "LBI1", "Lebanon IN DC"),
    (316, "Bolingbrook", "IL", "BLB1", "Bolingbrook DC"), (614, "Hebron", "KY", "HBK1", "Hebron KY DC"),
]
RECODE_DC = 311           # Rockford: re-coded in the WMS and the labour system after its client changed
RECODE_WEEK = (2025, 14)  # fiscal 2025 week 14
RECODE_NEW_NO, RECODE_NEW_CODE = 318, "RKF2"
RESTUDY_DC = 702          # Lebanon TN: selection and putaway re-studied after a re-slot
RESTUDY_WEEK = (2024, 27)

CLIENTS = ["Tolliver Markets", "Hargrove Foods", "Pennock's", "Fairhaven Grocers", "Mahler Fresh", "Briarwood Market",
           "Holbrook Foods", "Ruston Grocery Co.", "Westover Drug & Market", "Caddell's", "Amesbury Foods",
           "Wexley Pantry", "Lyle & Sons Grocers", "Stroud Market", "Coyle Fresh"]
NEW_ACCOUNTS = ["Dunleavy Club", "Pruett Family Grocers"]   # the two FY2027 accounts the programme DCs take on
# accounts won and lost over the history: heavy freight (beverages, water, pet food) or light (health and beauty, paper)
ACCOUNTS = {"heavy": ["Ashgrove Beverage", "Stonecrest Springs", "Marlow Pet Supply"],
            "light": ["Penrose Paper Co.", "Thayer Health & Beauty"]}
ACCOUNT_MIX = {"heavy": {"AMB": 0.12, "CHL": 0.05, "FRZ": 0.05, "HVB": 0.78},
               "light": {"AMB": 0.86, "CHL": 0.05, "FRZ": 0.04, "HVB": 0.05}}


def season_factor(d):
    """The network's weekly volume pattern (by the week's Sunday)."""
    m, day = d.month, d.day
    if (m == 11 and day >= 14) or (m == 12 and day <= 19):
        return 1.16
    if (m == 12 and day >= 20) or (m == 1 and day <= 8):
        return 0.89
    if m == 6 and day >= 27 or (m == 7 and day <= 4):
        return 1.07
    if m in (6, 7, 8):
        return 1.03
    if m == 2:
        return 0.96
    return 1.0


def mix_season(d):
    """Heavy and bulky freight (beverages, water, charcoal) rises in summer; ambient in the holiday build."""
    m = d.month
    hv = 1.0 + 0.30 * math.cos((m - 7) / 12 * 2 * math.pi)
    am = 1.0 + (0.07 if m in (11, 12) else 0.0)
    return {"AMB": am, "CHL": 1.0, "FRZ": 1.0 + (0.05 if m in (11, 12) else 0.0), "HVB": hv}


def dcs_frame():
    r = K.rng("dcs")
    n = len(DCS)
    df = pd.DataFrame(DCS, columns=["dc_no", "city", "state", "wms_code", "ehs_site"])
    df["pace_lr"] = np.clip(r.normal(0.925, 0.028, n), 0.865, 0.985)
    df["base"] = np.exp(K.CONFOUND * (df.pace_lr - K.PACE_REF)) * np.exp(r.normal(0, 0.13, n))
    df["size"] = np.exp(r.normal(np.log(547000), 0.20, n))           # cases a week at FY2021 week 1
    df["growth"] = r.normal(0.022, 0.028, n)                           # yearly volume trend
    mix = r.dirichlet([46, 20, 15, 11], n)
    for i, c in enumerate(K.CATS):
        df["mix_" + c] = mix[:, i]
    df["layout"] = np.round(np.exp(r.normal(0, 0.055, n)), 3)          # PUT and SEL layout factor (as filed, 3 decimals)
    df["ind_share"] = np.clip(r.normal(0.135, 0.015, n), 0.10, 0.17)   # indirect hours over direct
    df["agy_share"] = np.clip(r.normal(0.10, 0.05, n), 0.01, 0.22)    # agency associates' share of direct hours
    df["sqft"] = (np.round(df["size"] / 547000 * r.normal(640, 60, n), -1) * 1000).astype(int)
    df["opened"] = r.integers(1996, 2019, n)
    cl = r.permutation(len(CLIENTS))
    df["clients"] = [CLIENTS[cl[i % len(CLIENTS)]] + ("; " + CLIENTS[cl[(i + 5) % len(CLIENTS)]] if r.random() < 0.4 else "")
                     for i in range(n)]
    return df


def pace_shifts(dcs, prog_nos):
    """Persistent pace changes (an incentive scheme started or dropped, a re-slot, a new general manager, a tight labour
    market): two to four at every DC, when and how much, each pulling the DC back toward its own long-run pace once it
    has drifted."""
    r = K.rng("shifts")
    weeks = K.hist_weeks()
    nw = len(weeks)
    out = {}
    for d in dcs.dc_no:
        k = int(r.integers(2, 5))
        ws = sorted(int(x) for x in r.choice(np.arange(20, nw - 40), k, replace=False))
        lvl, seq = 1.0, []
        for i, w in enumerate(ws):
            size = r.uniform(0.05, 0.12)
            if lvl > 1.03:
                sign = -1
            elif lvl < 0.97:
                sign = 1
            else:
                sign = 1 if r.random() < 0.55 else -1
            if i == k - 1 and not 0.93 <= lvl * (1 + sign * size) <= 1.06:
                sign = -sign
            lvl *= 1 + sign * size
            seq.append((w, sign * size))
        out[int(d)] = seq
    return out


def account_moves(dcs, prog_nos):
    """Accounts won and lost over the history: which DCs, the fiscal week the account's freight starts or stops (a six-week
    ramp), its size against the DC's own volume and its freight. The DC staffs an account's freight at the engineered
    standards, so the account moves the DC's cases and hours and leaves its pace where it was."""
    r = K.rng("accounts")
    weeks = K.hist_weeks()
    idx = {(w[0], w[1]): i for i, w in enumerate(weeks)}
    prog = [d for d in dcs.dc_no if d in prog_nos]
    other = [d for d in dcs.dc_no if d not in prog_nos]
    out = {}
    pick = [d for d in r.choice(prog, 12, replace=False) if d != RECODE_DC][:11]
    for d in pick + list(r.choice(other, 18, replace=False)):
        lo = idx[(2021, 30)]
        hi = idx[(2025, 30)] if d in prog_nos else idx[(2026, 20)]
        w = int(r.integers(lo, hi))
        kind = "heavy" if r.random() < 0.8 else "light"
        won = bool(r.random() < 0.6)
        a = float(r.uniform(0.18, 0.40))
        name = ACCOUNTS[kind][int(r.integers(0, len(ACCOUNTS[kind])))]
        out[int(d)] = (w, kind, won, a, name)
    # Rockford's client transition: a beverage account in from fiscal 2025 week 14, when the DC was re-numbered
    out[RECODE_DC] = (idx[RECODE_WEEK], "heavy", True, 0.26, ACCOUNTS["heavy"][0])
    return out


def plan_growth(dcs):
    """FY2027 case growth over the same periods of the latest year (the commercial team's forecast by account)."""
    r = K.rng("plan_growth")
    g = r.uniform(-0.03, 0.09, len(dcs))
    order = r.permutation(len(dcs))
    top = order[:20]
    g[top] = r.uniform(0.16, 0.31, 20)
    return g


def simulate():
    dcs = dcs_frame()
    g = plan_growth(dcs)
    dcs["plan_growth"] = g
    prog = set(dcs.dc_no[np.argsort(-g)[:20]])
    dcs["programme"] = dcs.dc_no.isin(prog)
    shifts = pace_shifts(dcs, prog)
    moves = account_moves(dcs, prog)
    for dn, (w0, kind, won, a, name) in moves.items():
        if won:
            k = dcs.index[dcs.dc_no == dn][0]
            dcs.at[k, "clients"] = dcs.at[k, "clients"] + "; " + name
    weeks = K.hist_weeks()
    nw = len(weeks)
    t = np.arange(nw) / 52.0
    seas = np.array([season_factor(w[2]) for w in weeks])
    mixs = [mix_season(w[2]) for w in weeks]
    frames = []
    for _, d in dcs.iterrows():
        r = K.rng("dc_week", int(d.dc_no))
        trend = d["size"] * np.exp(d["growth"] * t)
        vol = trend * seas * np.exp(r.normal(0, 0.052, nw))
        surge = vol / trend
        step = np.ones(nw)
        for w0, sz in shifts[int(d.dc_no)]:
            step[w0:] = step[w0:] * (1 + sz)
        pace = d["pace_lr"] * (1 + K.SURGE_PACE * (surge - 1)) * step * np.exp(r.normal(0, 0.040, nw))
        cases = {}
        for c in K.CATS:
            ms = np.array([m[c] for m in mixs])
            cases[c] = vol * d["mix_" + c] * ms * np.exp(r.normal(0, 0.045, nw))
        # renormalise so the seasonal mix does not move the total
        tot = sum(cases.values())
        for c in K.CATS:
            cases[c] = cases[c] * vol / tot
        if int(d.dc_no) in moves:
            w0, kind, won, a, _ = moves[int(d.dc_no)]
            ramp = np.clip((np.arange(nw) - w0 + 1) / 6.0, 0.0, 1.0)
            share = a * (ramp if won else 1.0 - ramp)
            for c in K.CATS:
                cases[c] = cases[c] + vol * share * ACCOUNT_MIX[kind][c]
        layout = np.full(nw, d["layout"])
        if int(d.dc_no) == RESTUDY_DC:
            k = [i for i, w in enumerate(weeks) if (w[0], w[1]) >= RESTUDY_WEEK][0]
            layout[k:] = round(d["layout"] * 0.93, 3)   # re-slotted: the new standard allows 7 per cent less selection time
        earned_f = {}
        for f in K.FUNCS:
            lf = layout if f in ("PUT", "SEL") else 1.0
            earned_f[f] = sum(cases[c] * K.STD_BASE[f][c] for c in K.CATS) * lf / 60.0
        earned = sum(earned_f.values())
        direct = earned / pace
        dir_f = {}
        for f in K.FUNCS:
            dir_f[f] = earned_f[f] / pace * np.exp(r.normal(0, K.FUNC_SHARE_NOISE, nw))
        sc = direct / sum(dir_f.values())
        for f in K.FUNCS:
            dir_f[f] = dir_f[f] * sc
        indirect = direct * d["ind_share"] * np.exp(r.normal(0, 0.03, nw))
        lam = d["base"] * K.TRIR_REF / 200000.0 * (direct * (pace / K.PACE_REF) ** K.GAMMA + K.INDIRECT_RATE * indirect)
        lam = lam * r.gamma(K.OVERDISP, 1.0 / K.OVERDISP, nw)
        n_rec = r.poisson(lam)
        n_fa = r.poisson(lam * 2.6 * (pace / K.PACE_REF) ** -1.2)   # first aid: not what the vendor prices
        fr = pd.DataFrame({"dc_no": int(d.dc_no), "fy": [w[0] for w in weeks], "wk": [w[1] for w in weeks],
                           "week_start": [w[2] for w in weeks], "pace": pace, "earned": earned, "direct": direct,
                           "indirect": indirect, "lam": lam, "n_rec": n_rec, "n_fa": n_fa, "surge": surge})
        for c in K.CATS:
            fr["c_" + c] = cases[c]
        for f in K.FUNCS:
            fr["h_" + f] = dir_f[f]
            fr["e_" + f] = earned_f[f]
        fr["layout"] = layout
        frames.append(fr)
    hist = pd.concat(frames, ignore_index=True)
    hist["hours"] = hist.direct + hist.indirect
    hist["cases"] = hist[["c_" + c for c in K.CATS]].sum(axis=1)
    hist["per"] = [K.period_of(a, b) for a, b in zip(hist.fy, hist.wk)]
    W = type("World", (), {})()
    W.dcs, W.hist, W.shifts, W.prog, W.moves = dcs, hist, shifts, sorted(prog), moves
    W.plan = build_plan(W)
    W.cases = make_cases(W)
    return W


def build_plan(W):
    """The FY2027 operating plan v3: each DC's cases by period and category (the latest year's same periods grown by the
    commercial forecast, the programme DCs' growth carrying the new accounts' heavy freight), the FY2027 standards, and
    labour hours = earned hours / the planners' productivity target, indirect at the DC's ratio."""
    r = K.rng("plan")
    h = W.hist
    rows = []
    for _, d in W.dcs.iterrows():
        dn = int(d.dc_no)
        hd = h[h.dc_no == dn]
        is_p = bool(d.programme)
        last = hd[(hd.fy == 2026)]
        pace26 = last.earned.sum() / last.direct.sum()
        up = r.uniform(1.075, 1.115) if is_p else r.uniform(0.985, 1.02)
        target = pace26 * up
        lay = float(hd.layout.iloc[-1])
        for p in range(1, 13):
            base = hd[(hd.fy == 2026) & (hd.per == p)]
            if len(base) < len(K.period_weeks(2026, p)):
                base = hd[(hd.fy == 2025) & (hd.per == p)]
            bc = {c: base["c_" + c].sum() for c in K.CATS}
            tot = sum(bc.values())
            g = float(d.plan_growth)
            if is_p:
                # the new accounts: their freight is heavy-weighted (club and grocer beverages, pet food, bulk paper)
                new = tot * g
                newmix = {"AMB": 0.22, "CHL": 0.09, "FRZ": 0.07, "HVB": 0.62}
                c27 = {c: bc[c] + new * newmix[c] for c in K.CATS}
            else:
                c27 = {c: bc[c] * (1 + g) for c in K.CATS}
            c27 = {c: float(round(c27[c])) for c in K.CATS}
            e_f = {}
            for f in K.FUNCS:
                lf = lay if f in ("PUT", "SEL") else 1.0
                e_f[f] = sum(c27[c] * K.STD_BASE[f][c] for c in K.CATS) * lf / 60.0
            e = sum(e_f.values())
            direct = round(e / target, 1)
            ind = round(direct * float(d.ind_share), 1)
            rows.append(dict(dc_no=dn, programme=is_p, per=p, earned=e, direct=direct, indirect=ind, target=target,
                             pace26=pace26, **{"c_" + c: c27[c] for c in K.CATS}, **{"e_" + f: e_f[f] for f in K.FUNCS}))
    P = pd.DataFrame(rows)
    P["hours"] = P.direct + P.indirect
    P["cases"] = P[["c_" + c for c in K.CATS]].sum(axis=1)
    P["weeks"] = [len(K.period_weeks(2027, p)) for p in P.per]
    base = W.dcs.set_index("dc_no").base
    P["truth_flat"] = [base[r_.dc_no] * K.TRIR_REF / 200000.0 * (r_.direct * (r_.target / K.PACE_REF) ** K.GAMMA
                                                                 + K.INDIRECT_RATE * r_.indirect) for r_ in P.itertuples()]
    # the world's expectation: in each week of a period the crews work around the plan's pace as they always have
    # (the week's volume against its planned level, and the week's own noise), hours following the week's volume
    rj = K.rng("plan_weeks")
    J = []
    for r_ in P.itertuples():
        wks = K.period_weeks(2027, r_.per)
        sf = np.array([season_factor(K.week_start(2027, w)) for w in wks])
        sims = []
        for _ in range(400):
            vol = sf * np.exp(rj.normal(0, 0.052, len(wks)))
            surge = vol / vol.mean()
            pace = (1 + K.SURGE_PACE * (surge - 1)) * np.exp(rj.normal(0, 0.040, len(wks)))
            pace = pace / np.average(pace, weights=vol / pace)     # the period's pace is the plan's on average
            hrs = vol / pace
            sims.append(np.sum(hrs * pace ** K.GAMMA) / np.sum(hrs))
        J.append(float(np.mean(sims)))
    P["jensen"] = J
    P["truth"] = [base[r_.dc_no] * K.TRIR_REF / 200000.0 * (r_.direct * (r_.target / K.PACE_REF) ** K.GAMMA * r_.jensen
                                                            + K.INDIRECT_RATE * r_.indirect) for r_ in P.itertuples()]
    return P


# ---------------------------------------------------------------------------------------------------- case records
TZ = {"OH": -5, "IN": -5, "MI": -5, "PA": -5, "KY": -5, "GA": -5, "NC": -5, "IL": -6, "TN": -6, "TX": -6, "WI": -6}
DEPT_RISK = {"RCV": 1.20, "PUT": 1.08, "SEL": 1.00, "LOD": 1.12}
JOBS = {"RCV": ["Receiver", "Unloader", "Receiving Lead"], "PUT": ["Forklift Operator", "Reach Truck Operator", "Replenishment Driver"],
        "SEL": ["Order Selector", "Order Selector", "Order Selector", "Selector Trainer"],
        "LOD": ["Loader", "Loader", "Shipping Associate"], "INV": ["Inventory Control Associate", "Cycle Counter"],
        "MNT": ["Maintenance Technician", "Battery Room Attendant"], "SAN": ["Sanitation Associate"],
        "TRN": ["Safety Trainer", "Training Associate"]}
# OIICS 2.01 event codes (two-digit) and natures
EVENTS = {
    "SEL": [("71", "Overexertion involving outside sources", 0.38), ("72", "Repetitive motions involving microtasks", 0.08),
            ("73", "Other exertions or bodily reactions", 0.10), ("62", "Struck by object or equipment", 0.12),
            ("64", "Caught in or compressed by equipment or objects", 0.06), ("42", "Fall on same level", 0.07),
            ("43", "Slip or trip without fall", 0.06), ("26", "Pedestrian vehicular incident", 0.05),
            ("63", "Struck against object or equipment", 0.08)],
    "RCV": [("71", "Overexertion involving outside sources", 0.40), ("62", "Struck by object or equipment", 0.15),
            ("64", "Caught in or compressed by equipment or objects", 0.08), ("43", "Slip or trip without fall", 0.07),
            ("42", "Fall on same level", 0.08), ("63", "Struck against object or equipment", 0.10),
            ("73", "Other exertions or bodily reactions", 0.12)],
    "PUT": [("24", "Collision between vehicles or mobile equipment", 0.12), ("26", "Pedestrian vehicular incident", 0.08),
            ("71", "Overexertion involving outside sources", 0.22), ("62", "Struck by object or equipment", 0.16),
            ("64", "Caught in or compressed by equipment or objects", 0.10), ("44", "Fall to lower level", 0.07),
            ("63", "Struck against object or equipment", 0.15), ("73", "Other exertions or bodily reactions", 0.10)],
    "LOD": [("71", "Overexertion involving outside sources", 0.36), ("62", "Struck by object or equipment", 0.14),
            ("64", "Caught in or compressed by equipment or objects", 0.10), ("44", "Fall to lower level", 0.06),
            ("42", "Fall on same level", 0.08), ("63", "Struck against object or equipment", 0.12),
            ("73", "Other exertions or bodily reactions", 0.14)],
    "IND": [("62", "Struck by object or equipment", 0.18), ("63", "Struck against object or equipment", 0.16),
            ("42", "Fall on same level", 0.14), ("43", "Slip or trip without fall", 0.12),
            ("71", "Overexertion involving outside sources", 0.18), ("53", "Exposure to other harmful substances", 0.06),
            ("64", "Caught in or compressed by equipment or objects", 0.08), ("73", "Other exertions or bodily reactions", 0.08)],
}
NATURES = {"71": ["Sprains, strains, tears", "Back pain, hurt back", "Soreness, pain"],
           "72": ["Carpal tunnel syndrome", "Tendonitis", "Soreness, pain"],
           "73": ["Sprains, strains, tears", "Soreness, pain"],
           "62": ["Bruises, contusions", "Cuts, lacerations", "Fractures"], "63": ["Bruises, contusions", "Cuts, lacerations"],
           "64": ["Fractures", "Crushing injuries", "Bruises, contusions"], "42": ["Sprains, strains, tears", "Bruises, contusions", "Fractures"],
           "43": ["Sprains, strains, tears", "Soreness, pain"], "44": ["Fractures", "Sprains, strains, tears", "Bruises, contusions"],
           "24": ["Bruises, contusions", "Sprains, strains, tears", "Fractures"], "26": ["Fractures", "Bruises, contusions", "Crushing injuries"],
           "53": ["Chemical burns", "Dermatitis"]}
PARTS = {"71": ["Lower back", "Shoulder", "Upper back", "Knee", "Wrist", "Abdomen"], "72": ["Wrist", "Hand", "Elbow", "Shoulder"],
         "73": ["Lower back", "Shoulder", "Knee", "Neck"], "62": ["Hand", "Fingers", "Head", "Foot", "Leg"],
         "63": ["Knee", "Hand", "Head", "Shin", "Elbow"], "64": ["Fingers", "Hand", "Foot", "Toes"],
         "42": ["Knee", "Wrist", "Hip", "Ankle", "Elbow"], "43": ["Ankle", "Knee", "Lower back"],
         "44": ["Ankle", "Wrist", "Back", "Knee"], "24": ["Neck", "Back", "Knee", "Shoulder"], "26": ["Foot", "Ankle", "Leg"],
         "53": ["Hand", "Eyes", "Face"]}
AGENCIES = ["Tamarack Workforce Solutions", "Corwin Staffing", "Halvorsen Labor Partners"]


def _day_shift(r):
    if r.random() < 0.58:
        return int(r.integers(6, 16)), int(r.integers(0, 60))
    h = int(r.integers(17, 27)) % 24
    return h, int(r.integers(0, 60))


def make_cases(W):
    """Every reported case, recordable and first aid, as the world knows it (the clean truth)."""
    h = W.hist
    out = []
    dinfo = W.dcs.set_index("dc_no")
    for dn, hd in h.groupby("dc_no"):
        r = K.rng("cases", int(dn))
        st = dinfo.loc[dn, "state"]
        roster = ["A%06d" % x for x in r.choice(np.arange(100000, 999999), 2600, replace=False)]
        agy = ["T%06d" % x for x in r.choice(np.arange(100000, 999999), 900, replace=False)]
        agy_share = float(dinfo.loc[dn, "agy_share"])
        for row in hd.itertuples():
            for kind, n in (("REC", row.n_rec), ("FA", row.n_fa)):
                if n == 0:
                    continue
                wts = {f: getattr(row, "h_" + f) * DEPT_RISK[f] * (row.pace / K.PACE_REF) ** K.GAMMA for f in K.FUNCS}
                ind_total = row.indirect * K.INDIRECT_RATE
                for dpt, sh in (("INV", 0.34), ("MNT", 0.22), ("SAN", 0.30), ("TRN", 0.14)):
                    wts[dpt] = ind_total * sh
                keys = list(wts)
                p = np.array([wts[k_] for k_ in keys], float)
                p = p / p.sum()
                for _ in range(int(n)):
                    dept = keys[int(r.choice(len(keys), p=p))]
                    day = row.week_start + dt.timedelta(days=int(r.integers(0, 7)))
                    hh, mm = _day_shift(r)
                    if hh < 6:
                        pass
                    ev_pool = EVENTS["IND" if dept in K.INDIRECT else dept]
                    ep = np.array([e[2] for e in ev_pool])
                    ev = ev_pool[int(r.choice(len(ev_pool), p=ep / ep.sum()))]
                    nat = NATURES[ev[0]][int(r.integers(0, len(NATURES[ev[0]])))]
                    part = PARTS[ev[0]][int(r.integers(0, len(PARTS[ev[0]])))]
                    is_agy = dept in K.FUNCS and r.random() < agy_share * 1.15
                    emp = agy[int(r.integers(0, len(agy)))] if is_agy else roster[int(r.integers(0, len(roster)))]
                    rec = dict(dc_no=int(dn), fy=row.fy, wk=row.wk, date=day, hour=hh, minute=mm, dept=dept,
                               job=JOBS[dept][int(r.integers(0, len(JOBS[dept])))], event_code=ev[0], event=ev[1],
                               nature=nat, part=part, employee_id=emp,
                               employer=(AGENCIES[int(dn) % 3] if is_agy else K.ORG), kind=kind, tz=TZ[st])
                    if kind == "REC":
                        u = r.random()
                        rec["case_type"] = "DAFW" if u < 0.32 else ("DJTR" if u < 0.75 else "OTHER")
                        rec["illness"] = ("Skin disorder" if r.random() < 0.5 else "All other illnesses") if r.random() < 0.012 else ""
                        if rec["illness"]:
                            rec["nature"] = "Dermatitis" if rec["illness"] == "Skin disorder" else "Heat exhaustion"
                        rec["privacy"] = r.random() < 0.015
                        away = int(np.clip(np.round(np.exp(r.normal(2.55, 0.95))), 1, 400)) if rec["case_type"] == "DAFW" else 0
                        restr = 0
                        if rec["case_type"] == "DJTR":
                            restr = int(np.clip(np.round(np.exp(r.normal(2.85, 0.8))), 1, 400))
                        elif rec["case_type"] == "DAFW" and r.random() < 0.55:
                            restr = int(np.clip(np.round(np.exp(r.normal(2.3, 0.8))), 1, 300))
                        rec["away_true"], rec["restr_true"] = away, restr
                        rec["separated_after"] = int(r.integers(5, 120)) if r.random() < 0.07 else -1
                        rec["night_return"] = hh >= 17 or hh < 6
                    out.append(rec)
                # a few cases reported, entered as recordable and later found not work-related
            if row.n_rec and r.random() < 0.018:
                day = row.week_start + dt.timedelta(days=int(r.integers(0, 7)))
                hh, mm = _day_shift(r)
                dept = ["SEL", "LOD", "RCV", "PUT"][int(r.integers(0, 4))]
                ev = EVENTS[dept][0]
                out.append(dict(dc_no=int(dn), fy=row.fy, wk=row.wk, date=day, hour=hh, minute=mm, dept=dept,
                                job=JOBS[dept][0], event_code=ev[0], event=ev[1], nature=NATURES[ev[0]][2],
                                part=PARTS[ev[0]][0], employee_id=roster[int(r.integers(0, len(roster)))],
                                employer=K.ORG, kind="REMOVED", tz=TZ[st], case_type="OTHER", illness="",
                                privacy=False, away_true=0, restr_true=0, separated_after=-1, night_return=False))
    C = pd.DataFrame(out)
    C = C.sort_values(["date", "dc_no", "hour", "minute", "employee_id"]).reset_index(drop=True)
    return C
