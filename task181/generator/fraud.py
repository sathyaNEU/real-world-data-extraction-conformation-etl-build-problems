"""The counterfeit wave and the ordinary fraud around it, then card numbers.

Works on sim.ev (one row per card event, keyed by card slot). Victims are chosen from the slots the
two skimmed terminals read by contact inside their windows; every other victim of counterfeit fraud is
a traveller with no shared terminal. Then counterfeit cash-outs, the member's report (case opened, card
blocked and reissued), card-not-present and lost-card fraud, and the mapping of every event to the card
number live at that moment. Deterministic for world.SEED.
"""
import datetime as dt

import numpy as np
import pandas as pd

import world as W
import sim as S

DAY = S.DAY
CONTACT = (S.E05, S.E80, S.E90)
T_NORMAL, T_CF, T_CNPF, T_LSF, T_CF_BLOCKED = 0, 1, 2, 3, 4


def t_of(d, hour):
    return S.day_of(d) * DAY + int(round(hour * 3600))


class Fraud:
    pass


def _contact(ev):
    return ev.entry.isin(CONTACT)


def changed_in(lc, a, b):
    sel = (lc.date >= a) & (lc.date <= b)
    return set(lc.slot[sel].tolist())


def select_edge_victims(ev, term, d_first, d_last, cand_ok, rng, evening_cut=20.0, open_hour=5.5):
    """First and last member reads of the window made by candidate slots; every other member read at the
    terminal from 20:00 the evening before the first to the first read, and after the last read on its day,
    is removed (the window edges then sit at the same instant whether a reader uses UTC or Eastern dates)."""
    at = ev[(ev.term == term)]
    day = at.t // DAY
    f0 = S.day_of(d_first)
    first_day = at[(day == f0) & (at.t >= f0 * DAY + open_hour * 3600)].sort_values("t")
    first = first_day[first_day.slot.isin(cand_ok)].iloc[0]
    l0 = S.day_of(d_last)
    last_day = at[(day == l0) & (at.t <= l0 * DAY + 19.8 * 3600)].sort_values("t")
    last = last_day[last_day.slot.isin(cand_ok) & (last_day.slot != first.slot)].iloc[-1]
    drop = at[((at.t >= (f0 - 1) * DAY + evening_cut * 3600) & (at.t < first.t)) |
              ((day == l0) & (at.t > last.t))].index
    return int(first.slot), int(last.slot), drop


def run(sim):
    rng = np.random.default_rng(W.SEED + 31)
    cat, ev, lc, slots, members = sim.cat, sim.ev.copy(), sim.lifecycle.copy(), sim.slots, sim.members
    ev["resp"] = np.int8(0)
    ev["tag"] = np.int8(T_NORMAL)
    OPT6 = cat.fuel["terminals"][5]
    OPT5 = cat.fuel["terminals"][4]
    SCO = cat.lombard["terminals"][4:10]
    SCO2 = cat.lombard["terminals"][5]
    STAFFED = cat.lombard["terminals"][0:4]
    COFFEE = cat.coffee["terminals"][0]
    WASH = cat.wash["terminals"][0]
    plaza_terms = set(cat.fuel["terminals"]) | {COFFEE, WASH}

    # cards lost, damaged or closed late in the period cannot carry a later fraud claim; a renewal due
    # after the skim is superseded by the fraud reissue
    late = lc[(lc.date >= dt.date(2026, 7, 25)) & (lc.reason != "RN")]
    busy = set(late.slot.tolist())
    day = ev.t // DAY
    contact = _contact(ev)
    sco2_any = set(ev.slot[ev.term == SCO2].tolist())
    plaza_any = set(ev.slot[ev.term.isin(sorted(plaza_terms))].tolist())
    member_of = slots.member.values
    mem_plaza = set(member_of[sorted(plaza_any)].tolist())

    # pump victims ------------------------------------------------------------------------------------
    pw0, pw1 = S.day_of(W.PUMP_WINDOW[0]), S.day_of(W.PUMP_WINDOW[1])
    in_pw = (ev.term == OPT6) & contact & (day >= pw0) & (day <= pw1)
    pump_cand = sorted(set(ev.slot[in_pw].tolist()) - busy - sco2_any)
    first_s, last_s, drop = select_edge_victims(ev, OPT6, W.PUMP_WINDOW[0], W.PUMP_WINDOW[1], pump_cand, rng)
    ev = ev.drop(drop)
    rest = [s for s in pump_cand if s not in (first_s, last_s)]
    wts = np.array([1.0 if slots.card_type.iat[s] == "Debit" else 0.75 for s in rest])
    pick = rng.choice(rest, size=W.N_PUMP_VICTIMS - 2, replace=False, p=wts / wts.sum())
    pump_v = [first_s, last_s] + sorted(int(x) for x in pick)

    # PIN pad victims ---------------------------------------------------------------------------------
    day = ev.t // DAY
    contact = _contact(ev)
    sw0, sw1 = S.day_of(W.SCO_WINDOW[0]), S.day_of(W.SCO_WINDOW[1])
    in_sw = (ev.term == SCO2) & contact & (day >= sw0) & (day <= sw1)
    travellers = set(i for i, m in enumerate(members.itertuples()) if m.traveller)
    pp_cand = sorted(s for s in set(ev.slot[in_sw].tolist()) - busy
                     if member_of[s] not in mem_plaza and member_of[s] not in travellers)
    first_p, last_p, drop = select_edge_victims(ev, SCO2, W.SCO_WINDOW[0], W.SCO_WINDOW[1], pp_cand, rng,
                                                open_hour=7.0)
    ev = ev.drop(drop)
    rest = [s for s in pp_cand if s not in (first_p, last_p)]
    wts = np.array([1.0 if slots.card_type.iat[s] == "Debit" else 0.6 for s in rest])
    pick = rng.choice(rest, size=W.N_PINPAD_VICTIMS - 2, replace=False, p=wts / wts.sum())
    pp_v = [first_p, last_p] + sorted(int(x) for x in pick)

    # victims' visits before the windows went to other pumps (tapped) and to the staffed lanes ---------
    day = ev.t // DAY
    vp = ev.slot.isin(pump_v)
    mv = np.nonzero((vp & (ev.term == OPT6) & (day < pw0)).values)[0]
    other_opt = [x for x in cat.fuel["terminals"] if x != OPT6]
    nfc = slots.nfc.values
    drop_i = []
    for i in mv:
        if nfc[ev.slot.values[i]]:
            ev.iat[i, ev.columns.get_loc("term")] = int(rng.choice(other_opt))
            ev.iat[i, ev.columns.get_loc("entry")] = S.E07
        else:
            drop_i.append(ev.index[i])
    ev = ev.drop(drop_i)
    day = ev.t // DAY
    vpp = ev.slot.isin(pp_v)
    mv = vpp & (ev.term == SCO2) & (day < sw0)
    ev.loc[mv, "term"] = np.array(STAFFED, dtype=np.int32)[rng.integers(0, 4, int(mv.sum()))]

    # background victims: travellers with card-present use outside Ontario, no plaza, no Lombard -------
    trips = pd.DataFrame(sim.trips, columns=["member", "dest", "a", "b"])
    trips["away"] = [S_dest_away(d) for d in trips.dest]
    lomb_any = set(ev.slot[ev.term.isin(cat.lombard["terminals"])].tolist())
    bg_rows = []
    used_members = set(member_of[pump_v].tolist()) | set(member_of[pp_v].tolist())
    for r in trips[trips.away].sort_values(["b", "member"]).itertuples():
        if r.member in used_members or r.member in mem_plaza:
            continue
        road = slots[(slots.member == r.member) & slots.road]
        if not len(road):
            continue
        s = int(road.slot.iat[0])
        if s in busy or s in lomb_any or s in plaza_any:
            continue
        lo = max(S.day_of(W.BACKGROUND_FIRST_USE[0]), r.b + 6)
        hi = min(S.day_of(W.BACKGROUND_FIRST_USE[1]), r.b + 48)
        if lo > hi:
            continue
        bg_rows.append((s, int(r.member), lo, hi, int(r.dest)))
    fr = Fraud()
    fr.cat, fr.slots, fr.members = cat, slots, members
    fr.pump_v, fr.pp_v, fr.bg_pool = pump_v, pp_v, bg_rows
    fr.terms = {"OPT6": OPT6, "SCO2": SCO2, "COFFEE": COFFEE, "WASH": WASH, "SCO": SCO, "STAFFED": STAFFED,
                "OPT": list(cat.fuel["terminals"])}
    fr.ev, fr.lc = ev, lc
    return fr


def S_dest_away(di):
    import places
    town, prov, country, _ = places.DESTINATIONS[di]
    return country == "US" or prov != "ON"


# first counterfeit use ------------------------------------------------------------------------------
def window_reads(ev, slots_, term, d0, d1):
    day = ev.t // DAY
    x = ev[ev.slot.isin(slots_) & (ev.term == term) & _contact(ev) & (day >= S.day_of(d0)) & (day <= S.day_of(d1))]
    g = x.groupby("slot").t.agg(["min", "max"])
    return {int(k): (int(v["min"]), int(v["max"])) for k, v in g.iterrows()}


def assign_first_use(fr, rng):
    ev = fr.ev
    out = {}
    pr = window_reads(ev, fr.pump_v, fr.terms["OPT6"], *W.PUMP_WINDOW)
    lo, hi = S.day_of(W.PUMP_FIRST_USE[0]), S.day_of(W.PUMP_FIRST_USE[1])
    for i, s in enumerate(fr.pump_v):
        r1, r2 = pr[s][0] // DAY, pr[s][1] // DAY
        if i == 0:
            f = lo
        else:
            f = r1 + int(rng.integers(18, 37))
            f = max(f, r2 + 2, lo)
            f = min(f, hi, r1 + 43)
        assert f >= r2 + 2 and f - r1 <= 44, (s, r1, r2, f)
        out[s] = ("pump", f)
    sr = window_reads(ev, fr.pp_v, fr.terms["SCO2"], *W.SCO_WINDOW)
    lo, hi = S.day_of(W.PINPAD_FIRST_USE[0]), S.day_of(W.PINPAD_FIRST_USE[1])
    for i, s in enumerate(fr.pp_v):
        r1, r2 = sr[s][0] // DAY, sr[s][1] // DAY
        if i == 0:
            f = lo
        else:
            f = r1 + int(rng.integers(15, 33))
            f = max(f, r2 + 2, lo)
            f = min(f, hi, r1 + 43)
        assert f >= r2 + 2 and f - r1 <= 44, (s, r1, r2, f)
        out[s] = ("pinpad", f)
    fr.pump_reads, fr.pp_reads = pr, sr
    return out


def choose_background(fr, rng, first_use):
    """Travellers whose counterfeit source is not in the data: no two of them were read by contact, in their
    lookbacks, at a terminal that few other members use, and at most two went to the same destination."""
    pool = fr.bg_pool
    ev = fr.ev
    day = (ev.t // DAY).values
    cont = ev.entry.isin(CONTACT).values
    span = (day >= S.day_of(dt.date(2026, 6, 26))) & (day <= S.day_of(dt.date(2026, 10, 1)))
    n_act = ev.slot[span].nunique()
    sel = span & cont & (ev.term.values >= 0)
    users = pd.Series(ev.slot.values[sel]).groupby(ev.term.values[sel]).nunique()
    base = (users / n_act).to_dict()
    pool_slots = sorted(set(p[0] for p in pool))
    sub = ev[ev.slot.isin(pool_slots) & ev.entry.isin((S.E05, S.E07, S.E80, S.E90, S.E91)) & (ev.term >= 0)]
    by_slot = {s: g for s, g in sub.groupby("slot")}
    town_of_term = np.array([fr.cat.merchants[t["merchant"]]["town"] for t in fr.cat.terminals])
    dest_towns = {d[0] for d in __import__("places").DESTINATIONS if d[2] == "US" or d[1] != "ON"}
    order = rng.permutation(len(pool))
    chosen, towns, dests, seen_terms, seen_slots = [], {}, {}, set(), set()
    for j in order:
        s, m, lo, hi, dest = pool[j]
        town = fr.members.town.iat[m]
        if towns.get(town, 0) >= 7 or s in first_use or s in seen_slots:
            continue
        f = int(rng.integers(lo, hi + 1))
        g = by_slot.get(s)
        terms, visited = set(), set()
        if g is not None:
            d = (g.t // DAY).values
            inlb = (d >= f - 60) & (d <= f - 1)
            visited = {town_of_term[t] for t in g.term.values[inlb].tolist()} & dest_towns
            terms = set(g.term.values[inlb & g.entry.isin(CONTACT).values].tolist())
        if any(dests.get(v, 0) >= 2 for v in visited):
            continue
        if any(base.get(t, 0.0) < 0.03 for t in terms & seen_terms):
            continue
        chosen.append(s)
        seen_slots.add(s)
        first_use[s] = ("background", f)
        towns[town] = towns.get(town, 0) + 1
        for v in visited:
            dests[v] = dests.get(v, 0) + 1
        seen_terms |= terms
        if len(chosen) == W.N_BACKGROUND_VICTIMS:
            break
    assert len(chosen) == W.N_BACKGROUND_VICTIMS, len(chosen)
    fr.bg_v = chosen
    return chosen


# cash-outs ------------------------------------------------------------------------------------------
def cashout_places(cat):
    out = {"US_atm": [], "CA_atm": [], "US_store": [], "CA_store": []}
    for m in cat.merchants:
        if m["role"] != "cashout":
            continue
        key = ("US" if m["country"] == "US" else "CA") + ("_atm" if m["cat"] == "atm" else "_store")
        out[key].append(m["idx"])
    return out


def sessions_for(fr, rng, s, f, twin, places_):
    """Counterfeit transactions on a victim's card from day f; returns event dicts and the report time."""
    cat = fr.cat
    ctype = fr.slots.card_type.iat[s]
    rows = []
    n_sess = 1 + int(rng.random() < 0.36) + int(rng.random() < 0.12)
    region = "US" if rng.random() < 0.62 else "CA"
    n_sess = min(n_sess, S.day_of(W.SIM_END) - f + 1)
    for k in range(n_sess):
        d = f + k
        h = 10.0 + 12.8 * rng.random() if k else 10.5 + 11.0 * rng.random()
        t = d * DAY + int(h * 3600)
        if ctype == "Debit" or rng.random() < 0.35:
            m = int(rng.choice(places_[region + "_atm"]))
            term = cat.merchants[m]["terminals"][0]
            sur = cat.merchants[m]["surcharge"]
            amounts = [200, 300, 400, 500] if region == "US" else [200, 300, 400, 500, 600, 800]
            nwd = 1 + int(rng.random() < 0.55) + int(rng.random() < 0.2)
            if rng.random() < 0.25:
                rows.append(dict(t=t, merch=m, term=term, kind=S.K_BAL, amount=0.0, resp=0))
                t += int(rng.integers(40, 150))
            if rng.random() < 0.12:
                big = max(amounts) + 200
                rows.append(dict(t=t, merch=m, term=term, kind=S.K_ATM, amount=big + sur, resp=4))   # 61
                t += int(rng.integers(30, 90))
            for j in range(nwd):
                a = float(rng.choice(amounts))
                rows.append(dict(t=t, merch=m, term=term, kind=S.K_ATM, amount=a + sur, resp=0))
                t += int(rng.integers(60, 260))
            if twin and k == 0:
                a = rows[-1]["amount"]
                rows.append(dict(t=t, merch=m, term=term, kind=S.K_ATM, amount=a, resp=0))
                t += int(rng.integers(60, 200))
        else:
            m = int(rng.choice(places_[region + "_store"]))
            term = cat.merchants[m]["terminals"][int(rng.integers(0, len(cat.merchants[m]["terminals"])))]
            for j in range(1 + int(rng.random() < 0.5)):
                a = round(float(rng.lognormal(np.log(520.0), 0.55)), 2)
                a = float(np.clip(a, 149.0, 1890.0))
                rows.append(dict(t=t, merch=m, term=term, kind=S.K_PUR, amount=a, resp=0))
                t += int(rng.integers(300, 1500))
            if twin and k == 0:
                m2 = int(rng.choice(places_[region + "_atm"]))
                term2 = cat.merchants[m2]["terminals"][0]
                a = float(rng.choice([300, 400, 500])) + cat.merchants[m2]["surcharge"]
                t += int(rng.integers(900, 2400))
                for _ in range(2):
                    rows.append(dict(t=t, merch=m2, term=term2, kind=S.K_ATM, amount=a, resp=0))
                    t += int(rng.integers(70, 220))
    rows.sort(key=lambda r: r["t"])
    first_ok = next(r for r in rows if r["resp"] == 0 and r["kind"] != S.K_BAL)
    assert first_ok["t"] // DAY == f
    # the member reports: same day, the next, or two to three days on
    last_t = max(r["t"] for r in rows if r["t"] // DAY == f)
    u = rng.random()
    if u < 0.5:
        rep = last_t + int(rng.integers(3600, 5 * 3600))
        if rep // DAY > f:
            rep = f * DAY + int(23.6 * 3600)
    else:
        dd = f + (1 if u < 0.83 else int(rng.integers(2, 4)))
        hr = 20.2 + 3.2 * rng.random() if rng.random() < 0.22 else 8.2 + 11.5 * rng.random()
        rep = dd * DAY + int(hr * 3600)
    rep = min(rep, S.day_of(W.SIM_END) * DAY + int(18.75 * 3600))
    out = []
    for r in rows:
        if r["t"] >= rep:
            if r["kind"] == S.K_BAL:
                continue
            r = dict(r, resp=6, tag=T_CF_BLOCKED)        # 62 restricted card after the block
        else:
            r = dict(r, tag=T_CF)
        out.append(r)
    blocked = [r for r in out if r["tag"] == T_CF_BLOCKED]
    if len(blocked) > 2:
        keep = set(id(r) for r in blocked[:2])
        out = [r for r in out if r["tag"] != T_CF_BLOCKED or id(r) in keep]
    return out, rep


def add_counterfeit(fr, rng, first_use):
    places_ = cashout_places(fr.cat)
    victims = sorted(first_use)
    twins_debit = [s for s in victims if fr.slots.card_type.iat[s] == "Debit"]
    twins_credit = [s for s in victims if fr.slots.card_type.iat[s] == "Credit"]
    tw = set(rng.choice(twins_debit, size=5, replace=False).tolist()) | \
        set(rng.choice(twins_credit, size=2, replace=False).tolist())
    rows, reports = [], {}
    for s in victims:
        kind, f = first_use[s]
        out, rep = sessions_for(fr, rng, s, f, s in tw, places_)
        for r in out:
            r["slot"] = s
            r["entry"] = S.E90
            rows.append(r)
        reports[s] = rep
    cf = pd.DataFrame(rows)
    fr.twins = sorted(tw)
    fr.reports = reports
    return cf


# ordinary fraud around the wave ---------------------------------------------------------------------
def add_noise_fraud(fr, rng, exclude):
    cat, slots, lc = fr.cat, fr.slots, fr.lc
    busy = changed_in(lc, dt.date(2026, 7, 25), W.SIM_END)
    cnp_m = [m["idx"] for m in cat.merchants if m["cat"] == "cnp"]
    rows, reports, kinds = [], {}, {}
    pool = [s for s in range(len(slots)) if s not in exclude and s not in busy]
    cred = [s for s in pool if slots.card_type.iat[s] == "Credit"]
    deb = [s for s in pool if slots.card_type.iat[s] == "Debit"]
    pick = sorted(rng.choice(cred, size=118, replace=False).tolist() + rng.choice(deb, size=29, replace=False).tolist())
    for s in pick:
        f = int(rng.integers(S.day_of(dt.date(2026, 8, 2)), S.day_of(dt.date(2026, 9, 30))))
        n = 1 + int(rng.poisson(1.6))
        t = f * DAY + int((7 + 16 * rng.random()) * 3600)
        last = t
        for j in range(n):
            m = int(rng.choice(cnp_m))
            a = round(float(np.clip(rng.lognormal(np.log(140.0), 0.8), 9.99, 1450.0)), 2)
            rows.append(dict(slot=s, t=t, merch=m, term=-1, kind=S.K_CNP, amount=a, resp=0, tag=T_CNPF,
                             entry=S.E81))
            last = t
            t += int(rng.integers(600, 30 * 3600))
        dd = last // DAY + int(rng.choice([0, 1, 1, 2, 3, 5]))
        hr = 20.3 + 3.0 * rng.random() if rng.random() < 0.18 else 8.0 + 11.8 * rng.random()
        reports[s] = min(max(dd * DAY + int(hr * 3600), last + 1800), S.day_of(W.SIM_END) * DAY + int(18.5 * 3600))
        kinds[s] = "Card not present"
    # lost and stolen cards used before the member called
    lsrows = lc[(lc.reason == "LS") & (lc.date >= dt.date(2026, 8, 4))]
    local = {}
    for m in cat.merchants:
        if m["role"] == "ordinary" and m["country"] == "CA" and m["cat"] in ("convenience", "liquor", "fastfood",
                                                                             "pharmacy", "discount", "fuelshop"):
            local.setdefault(m["town"], []).append(m["idx"])
    for r in lsrows.itertuples():
        s = int(r.slot)
        if s in exclude or rng.random() > 0.55:
            continue
        town = fr.members.town.iat[int(slots.member.iat[s])]
        f = S.day_of(r.date) - int(rng.integers(0, 2))
        t = f * DAY + int((9 + 9 * rng.random()) * 3600)
        last = t
        for j in range(2 + int(rng.random() < 0.5)):
            m = int(rng.choice(local[town]))
            a = round(float(np.clip(rng.lognormal(np.log(48.0), 0.5), 6.0, 99.0)), 2)
            term = cat.merchants[m]["terminals"][0]
            rows.append(dict(slot=s, t=t, merch=m, term=term, kind=S.K_PUR, amount=a, resp=0, tag=T_LSF,
                             entry=S.E07))
            last = t
            t += int(rng.integers(900, 7200))
        reports[s] = max(S.day_of(r.date) * DAY + int((8 + 12 * rng.random()) * 3600), last + 1800)
        kinds[s] = "Lost or stolen"
    return pd.DataFrame(rows), reports, kinds


# card numbers ---------------------------------------------------------------------------------------
REASON_TEXT = {"RN": "Renewal", "LS": "Lost", "ST": "Stolen", "DM": "Damaged", "FR": "Fraud", "CL": "Closed"}


def build_changes(fr, rng, reports, kinds):
    """One row per change to a card slot: the instant the old number stops, and the day the new one starts."""
    rows = []
    rep_slots = set(reports)
    for r in fr.lc.itertuples():
        s = int(r.slot)
        if s in rep_slots and r.reason != "LS":
            continue          # a card reported for fraud is reissued for that; the later change never happens
        d = S.day_of(r.date)
        if r.reason == "RN":
            rows.append((s, d * DAY + int((7 + 12 * rng.random()) * 3600), "RN", d))
        elif r.reason == "CL":
            rows.append((s, d * DAY + int((9.5 + 7 * rng.random()) * 3600), "CL", None))
        else:
            t = reports.get(s, d * DAY + int((8 + 12 * rng.random()) * 3600))
            reason = r.reason
            if reason == "LS":
                reason = "ST" if rng.random() < 0.3 else "LS"
            rows.append((s, t, reason, t // DAY + int(r.gap)))
    for s, t in reports.items():
        if kinds.get(s) == "Lost or stolen":
            continue
        ctype = fr.slots.card_type.iat[s]
        d = t // DAY
        if ctype == "Debit":
            nd = d + 1
            while not S.WORKDAY[min(nd, S.ND - 1)] and nd < S.ND - 1:
                nd += 1
            nd += int(rng.random() < 0.3)
        else:
            nd = d + int(rng.integers(6, 10))
        rows.append((s, t, "FR", nd))
    ch = pd.DataFrame(rows, columns=["slot", "t_switch", "reason", "new_day"])
    return ch.sort_values(["slot", "t_switch"]).reset_index(drop=True)


def map_tokens(fr, rng, ev, changes):
    slots = fr.slots
    used = set()

    def tok():
        while True:
            x = "%016X" % int(rng.integers(0, 2 ** 63))
            if x not in used:
                used.add(x)
                return x

    toks = []           # token rows
    seg_slot, seg_t0, seg_t1, seg_tok = [], [], [], []
    ch_by = {s: g for s, g in changes.groupby("slot", sort=True)}
    for s in range(len(slots)):
        sl = slots.iloc[s]
        cur = {"token": tok(), "slot": s, "member_id": sl.member_id, "card_type": sl.card_type,
               "secondary": bool(sl.secondary), "issued_on": sl.issued_on, "exp": (int(sl.exp_y), int(sl.exp_m)),
               "start_t": -10 ** 12}
        t0 = -10 ** 12
        if s in ch_by:
            for c in ch_by[s].itertuples():
                cur["end_t"], cur["end_reason"] = int(c.t_switch), c.reason
                toks.append(cur)
                seg_slot.append(s); seg_t0.append(t0); seg_t1.append(int(c.t_switch)); seg_tok.append(len(toks) - 1)
                if c.reason == "CL":
                    cur = None
                    break
                nd = int(c.new_day)
                start = nd * DAY if c.reason != "RN" else int(c.t_switch)
                if c.reason == "RN":
                    iss = S.date_of(nd) - dt.timedelta(int(rng.integers(18, 40)))
                    exp = (cur["exp"][0] + (3 if sl.card_type == "Debit" else 4), cur["exp"][1])
                else:
                    iss = S.date_of(c.t_switch // DAY)
                    yrs = 3 if sl.card_type == "Debit" else 4
                    exp = (iss.year + yrs, iss.month)
                cur = {"token": tok(), "slot": s, "member_id": sl.member_id, "card_type": sl.card_type,
                       "secondary": bool(sl.secondary), "issued_on": iss, "exp": exp, "start_t": start,
                       "prev": len(toks) - 1}
                t0 = start
        if cur is not None:
            cur["end_t"], cur["end_reason"] = None, None
            toks.append(cur)
            seg_slot.append(s); seg_t0.append(t0); seg_t1.append(10 ** 12); seg_tok.append(len(toks) - 1)
    seg = pd.DataFrame({"slot": seg_slot, "t0": seg_t0, "t1": seg_t1, "tok": seg_tok})
    # every event to the number live at its instant; events in a replacement gap or after closure drop
    ev = ev.reset_index(drop=True)
    ev["_i"] = np.arange(len(ev))
    left = ev[["t", "slot", "_i"]].sort_values(["t", "_i"], kind="mergesort")
    left = left.astype({"t": np.int64, "slot": np.int64})
    seg = seg.astype({"slot": np.int64, "t0": np.int64, "t1": np.int64})
    m1 = pd.merge_asof(left, seg.sort_values("t0", kind="mergesort"), left_on="t", right_on="t0", by="slot",
                       direction="backward")
    tokv = np.where((m1.t < m1.t1).values, m1.tok.values, -1)
    out = np.full(len(ev), -1)
    out[m1._i.values] = np.nan_to_num(tokv, nan=-1).astype(int)
    # a counterfeit attempt after the block stays on the blocked number: the segment that ended last
    m2 = pd.merge_asof(left, seg.sort_values("t1", kind="mergesort"), left_on="t", right_on="t1", by="slot",
                       direction="backward")
    blocked = ev.tag.values[m2._i.values] == T_CF_BLOCKED
    out[m2._i.values[blocked]] = m2.tok.values[blocked].astype(int)
    ev["tok"] = out
    ev = ev[ev.tok >= 0].drop(columns="_i").sort_values(["t", "slot"], kind="mergesort").reset_index(drop=True)
    tokens = pd.DataFrame(toks)
    tokens["tok"] = np.arange(len(tokens))
    return ev, tokens


def settle_late_reads(fr, rng, first_use):
    """Between a window's close and the card's first counterfeit use, victims keep shopping: at the
    re-terminalled pump they tap, at Lombard they go through the staffed lanes."""
    ev = fr.ev
    cat = fr.cat
    day = (ev.t // DAY).values
    opt6 = fr.terms["OPT6"]
    sco = set(fr.terms["SCO"])
    staffed = fr.terms["STAFFED"]
    nfc = fr.slots.nfc.values
    e_col = ev.columns.get_loc("entry")
    t_col = ev.columns.get_loc("term")
    drop_i = []
    for s, (kind, f) in sorted(first_use.items()):
        rows = np.nonzero((ev.slot.values == s) & np.isin(ev.entry.values, CONTACT))[0]
        for i in rows:
            term, d = int(ev.term.values[i]), int(day[i])
            if kind == "pump" and term == opt6 and d > S.day_of(W.PUMP_OUT_OF_SERVICE) and d < f:
                if nfc[s]:
                    ev.iat[i, e_col] = S.E07
                else:
                    drop_i.append(ev.index[i])
            if kind == "pinpad" and term in sco and d >= S.day_of(W.SCO_NEW_TIDS) and d < f:
                ev.iat[i, t_col] = int(rng.choice(staffed))
    fr.ev = ev.drop(drop_i)


def build(sim):
    fr = run(sim)
    rng = np.random.default_rng(W.SEED + 41)
    first_use = assign_first_use(fr, rng)
    choose_background(fr, rng, first_use)
    fr.first_use = first_use
    settle_late_reads(fr, rng, first_use)
    cf = add_counterfeit(fr, rng, first_use)
    noise, nreports, nkinds = add_noise_fraud(fr, np.random.default_rng(W.SEED + 43), exclude=set(first_use))
    reports = dict(fr.reports)
    reports.update(nreports)
    kinds = {s: "Counterfeit" for s in first_use}
    kinds.update(nkinds)
    ev = pd.concat([fr.ev, cf, noise], ignore_index=True)
    for c, dtp in (("slot", np.int32), ("term", np.int32), ("kind", np.int8), ("entry", np.int8),
                   ("resp", np.int8), ("tag", np.int8)):
        ev[c] = ev[c].astype(dtp)
    changes = build_changes(fr, np.random.default_rng(W.SEED + 47), reports, kinds)
    ev, tokens = map_tokens(fr, np.random.default_rng(W.SEED + 53), ev, changes)
    lo = S.day_of(dt.date(2026, 5, 31)) * DAY + (24 - W.UTC_OFFSET_H) * 3600
    hi = S.day_of(W.SIM_END) * DAY + (24 - W.UTC_OFFSET_H) * 3600
    ev = ev[(ev.t >= lo) & (ev.t < hi)].reset_index(drop=True)
    fr.ev, fr.tokens, fr.changes, fr.reports, fr.kinds = ev, tokens, changes, reports, kinds
    # victims as card numbers: the number the first counterfeit transaction was made on
    cfev = ev[(ev.tag == T_CF)].sort_values("t")
    first_tok = cfev.groupby("slot").tok.first()
    fr.victim_tok = {int(first_tok[s]): (first_use[s][0], first_use[s][1]) for s in first_use}
    # the two skimmed readers took every card by chip in August and September (C1: the chip-only reading
    # and the contact reading select the same cards)
    day = fr.ev.t.values // DAY
    calm = np.isin(fr.ev.term.values, [fr.terms["OPT6"], fr.terms["SCO2"]]) & \
        (day >= S.day_of(dt.date(2026, 8, 1))) & (day <= S.day_of(dt.date(2026, 9, 30))) & \
        np.isin(fr.ev.entry.values, (S.E80, S.E90))
    fr.ev.loc[calm, "entry"] = np.int8(S.E05)
    tune_pack(fr)
    return fr


def tune_pack(fr):
    import tune as T
    cat = fr.cat
    rng = np.random.default_rng(W.SEED + 61)
    eng = T.Engine(cat, fr.ev)
    eng.nfc = fr.slots.nfc.values
    V = {k: v[1] for k, v in fr.victim_tok.items()}
    kind = {k: v[0] for k, v in fr.victim_tok.items()}
    V78 = {k: f for k, f in V.items() if kind[k] != "pump"}
    V31 = {k: f for k, f in V.items() if kind[k] == "background"}
    tid = lambda term: term * 10
    designed = [tid(fr.terms["OPT6"]), tid(fr.terms["SCO2"]), tid(fr.terms["COFFEE"]), tid(fr.terms["WASH"])]
    sco2 = tid(fr.terms["SCO2"])
    rules = [(V, 10, 2.9, 60, "span", "contact"), (V, 3, 8.0, 60, "span", "contact"),
             (V78, 3, 10.0, 60, "span", "contact"), (V31, 2, 3.0, 60, "span", "contact")]
    for L in (45, 60, 90):
        for base in ("span", "period"):
            for modes in ("contact", "cp"):
                rules.append((V78, 10, lambda sc: sc.loc[sco2, "lift"] / 1.3, L, base, modes))
                if modes == "contact":
                    rules.append((V, 10, 3.3, L, base, modes))
                    rules.append((V31, 3, 3.0, L, base, modes))
    log = []
    ok = T.trim(eng, rng, V, designed, rules, log=log)
    tk = fr.tokens
    slot_of_tok = dict(zip(tk.tok, tk.slot))
    win = {}
    for r in tk.itertuples():
        a = max(0, int(r.start_t // DAY) + 1) if r.start_t > 0 else 0
        b = int(r.end_t // DAY) - 1 if r.end_t is not None and not pd.isna(r.end_t) else S.ND - 1
        win[r.tok] = (a, b)
    pump_tokens = [k for k in V if kind[k] == "pump"]
    T.car_wash_twin(eng, rng, V, pump_tokens, tid(fr.terms["WASH"]), tid(fr.terms["SCO2"]), W.CARWASH_TWIN_VICTIMS,
                    slot_of_tok, win)
    ok2 = T.trim(eng, rng, V, designed, rules, log=log)
    fr.tune_log, fr.tune_ok = log, (ok, ok2)
    fr.ev = eng.ev
