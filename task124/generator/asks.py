"""The two ask paths, built on the world the main call reads and written to files the call never opens.

Ask A: the 2026 replacement contracts' completions export (a change order's total joined onto every site it
covers), the change order register (each change order once) and the contracts list (Tri-County's vendor number
changed in July 2026). Ask B: the access agreements (the zone printed on the form when it was signed; plan revision 2
redrew six zone boundaries in October 2026). Every function here is deterministic from its own streams."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import common as K

IN_SCOPE = ("LEAD", "GRR", "LEAD STATUS UNKNOWN")


# ----------------------------------------------------------------------------------------------- the zone redraw
def redraw(segs: pd.DataFrame, lines: pd.DataFrame) -> dict:
    """segment -> zone under plan revision 1, for the segments revision 2 moved (every other segment kept its zone).
    In each pair the moved segments go from the first zone to the second; enough in-scope lines move that every
    zone's agreement count shifts."""
    scope = lines[lines.cls.isin(IN_SCOPE)].groupby("segment").size()
    moved = {}
    for a, b in K.REDRAW_PAIRS:
        r = K.stream("redraw", a, b)
        cand = sorted(sg for sg in segs[(segs.zone == b) & (segs.seg_era < 3)].segment if scope.get(sg, 0) >= 12)
        pick = r.choice(cand, size=6, replace=False)
        for sg in sorted(pick):
            moved[str(sg)] = a
    return moved


# ------------------------------------------------------------------------------------------- ask B: agreements
def agreements(lines: pd.DataFrame, moved: dict) -> pd.DataFrame:
    """One row per agreement form. Lines open in the plan at the extract only (agreements on lines since replaced or
    verified non-lead are archived out of the system's open file)."""
    scope = lines[lines.zone.isin(K.PLAN_ORDER) & lines.cls.isin(IN_SCOPE)].sort_values("sl_id")
    prio = {z: i for i, z in enumerate(K.OUTREACH_ORDER)}
    last = K.INVENTORY_DATE - dt.timedelta(days=1)
    rows = []
    for ln in scope.itertuples():
        r = K.stream("agreement", ln.sl_id)
        i = prio[ln.zone]
        if r.random() >= 0.31 - 0.0125 * i:
            continue
        start = dt.date(2022, 2, 7) + dt.timedelta(days=29 * i)
        d = start + dt.timedelta(days=int(r.integers(0, (last - start).days + 1)))
        if d.weekday() == 6:
            d -= dt.timedelta(days=1)
        ch = "PORTAL" if d >= K.PORTAL_OPEN and r.random() < 0.55 else "PAPER"
        forms = [(d, ch)]
        if r.random() < 0.055:
            if ch == "PAPER":
                d2 = max(d, K.PORTAL_OPEN) + dt.timedelta(days=int(r.integers(5, 121)))
                ch2 = "PORTAL"
            else:
                d2 = d + dt.timedelta(days=int(r.integers(5, 61)))
                ch2 = "PAPER"
            if d2 <= last:
                forms.append((d2, ch2))
        status, status_date = "SIGNED", None
        if len(forms) == 1 and r.random() < 0.026:
            wd = d + dt.timedelta(days=int(r.integers(20, 301)))
            if wd <= last:
                status, status_date = "WITHDRAWN", wd
        for k, (fd, fch) in enumerate(forms):
            zone_on_form = moved.get(ln.segment, ln.zone) if fd < K.REV2_DATE else ln.zone
            legacy = fd < K.MIGRATION
            rows.append(dict(sl_id=ln.sl_id, signed_on=fd, channel=fch,
                             premise_no=str(int(ln.legacy_premise)) if legacy else "",
                             form_sl_id="" if legacy else ln.sl_id, zone_on_form=zone_on_form,
                             status=status if k == 0 else "SIGNED",
                             status_date=status_date if (k == 0 and status == "WITHDRAWN") else fd,
                             zone=ln.zone))
    df = pd.DataFrame(rows).sort_values(["signed_on", "sl_id", "channel"]).reset_index(drop=True)
    seq = {}
    nos = []
    for d in df.signed_on:
        seq[d.year] = seq.get(d.year, 0) + 1
        nos.append("AA-%d-%05d" % (d.year, seq[d.year]))
    df.insert(0, "agreement_no", nos)
    return df


def agreements_answer(ag: pd.DataFrame) -> dict:
    """Distinct lines with an agreement signed and not withdrawn by the extract, by the inventory's zone."""
    ok = ag[ag.status == "SIGNED"]
    return {z: int(ok[ok.zone == z].sl_id.nunique()) for z in K.PLAN_ORDER}


# ----------------------------------------------------------------------------------- ask A: 2026 completions
SURFACES = (("LAWN", 0.45, 640, 1150), ("SIDEWALK", 0.30, 1180, 2460), ("PAVEMENT", 0.25, 2150, 4900))
CO_KINDS = [
    ("Rock excavation, service trench", "site", 1850, 4200),
    ("Additional pavement restoration, full lane width", "site", 2400, 6800),
    ("Interior plumbing reconnection past the meter setter", "site", 650, 1900),
    ("Tree root removal and arborist attendance", "site", 900, 2600),
    ("Traffic control, signalised intersection", "lump", 3100, 9600),
    ("Unmarked utility conflict, relocation", "lump", 2800, 11500),
]


# the engineer's change order entries as the log carries them: what was found or required, where, and how many
# services when there is more than one; worded from each change order's own stream, so no other draw moves
CO_TEXT = {
    "Rock excavation, service trench": (
        "Rock in service trench at {where}; hoe ram and haul-off{n}",
        "Ledge rock at curb stop excavation, {where}{n}",
        "Rock excavation beyond the bid allowance, {where}{n}"),
    "Additional pavement restoration, full lane width": (
        "Full-lane mill and overlay required by the street opening permit, {where}{n}",
        "Pavement restored to full lane width at the inspector's direction, {where}{n}",
        "Additional asphalt restoration, permit condition: {where}{n}"),
    "Interior plumbing reconnection past the meter setter": (
        "Interior reconnection past the setter, house piping would not take the new setter: {where}{n}",
        "Owner-side plumbing reconnected inside the basement, {where}{n}",
        "Reconnect interior piping beyond the meter setter, {where}{n}"),
    "Tree root removal and arborist attendance": (
        "Root pruning with the municipal arborist present, tree lawn services on {where}{n}",
        "Arborist on site for excavation in the tree lawn, {where}{n}",
        "Tree roots removed from the service trench, {where}{n}"),
    "Traffic control, signalised intersection": (
        "Lane closure and flaggers at the signalised intersection, {where}{n}",
        "Police detail and arrow board at the signal, {where}{n}",
        "Traffic control plan for work inside the signalised intersection, {where}{n}"),
    "Unmarked utility conflict, relocation": (
        "Unmarked gas service in the trench at {where}; hand dig and offset{n}",
        "Abandoned storm lateral in the service trench, removed: {where}{n}",
        "Unlocated fiber conduit, standby and relocation, {where}{n}"),
}
COUNT_WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}


def co_description(co_no: str, kind: str, pick, street: dict, address: dict) -> str:
    r = K.stream("co-text", co_no)
    text = CO_TEXT[kind][int(r.integers(len(CO_TEXT[kind])))]
    if len(pick) == 1:
        return text.format(where=address[pick[0]].title(), n="")
    streets = sorted({street[s].title() for s in pick})
    if len(streets) == 1:
        where = streets[0]
    elif len(streets) == 2:
        where = "%s and %s" % tuple(streets)
    else:
        k = len(streets) - 2
        where = "%s, %s and %s other street%s" % (streets[0], streets[1], {1: "one"}.get(k, COUNT_WORDS.get(k)),
                                                    "" if k == 1 else "s")
    n = " (%d services)" % len(pick) if r.random() < 0.5 else ", %s services" % COUNT_WORDS[len(pick)]
    return text.format(where=where, n=n)


def district_holidays(year: int) -> set:
    """Days the district's offices are closed: New Year's Day, Martin Luther King Jr. Day, Memorial Day, Independence
    Day, Labor Day, Thanksgiving and the day after, Christmas Eve and Christmas Day (each observed on the nearest
    weekday)."""
    def observed(d):
        return d - dt.timedelta(days=1) if d.weekday() == 5 else d + dt.timedelta(days=1) if d.weekday() == 6 else d

    def nth_weekday(month, weekday, n):
        d = dt.date(year, month, 1)
        d += dt.timedelta(days=(weekday - d.weekday()) % 7)
        return d + dt.timedelta(days=7 * (n - 1))
    may_31 = dt.date(year, 5, 31)
    thanksgiving = nth_weekday(11, 3, 4)
    return {observed(dt.date(year, 1, 1)), nth_weekday(1, 0, 3), may_31 - dt.timedelta(days=may_31.weekday()),
            observed(dt.date(year, 7, 4)), nth_weekday(9, 0, 1), thanksgiving,
            thanksgiving + dt.timedelta(days=1), observed(dt.date(year, 12, 24)), observed(dt.date(year, 12, 25))}


def contract_of(zone: str) -> str:
    for c in K.CONTRACTS_2026:
        if zone in c[3]:
            return c[0]
    raise KeyError(zone)


def _cents(x: float) -> float:
    return round(float(x), 2)


def completions(lines: pd.DataFrame):
    """Returns (lines with the quarter-end completions moved, sites, change orders). sites: one row per completed
    full replacement (local completion time, paid columns); change orders: one row each with its sites."""
    lines = lines.copy()
    rep = lines[lines.replaced.map(lambda d: isinstance(d, dt.date) and d.year == 2026)].copy()
    rep["contract"] = rep.zone.map(contract_of)
    rep = rep.sort_values("sl_id")
    # paid columns for every site
    sites = []
    for ln in rep.itertuples():
        r = K.stream("site", ln.sl_id)
        c = [x for x in K.CONTRACTS_2026 if x[0] == ln.contract][0]
        length = int(np.clip(round(r.lognormal(np.log(56), 0.33)), 28, 160))
        u = r.random()
        acc = 0.0
        for name, p, lo, hi in SURFACES:
            acc += p
            if u < acc:
                surface, rest = name, lo + (hi - lo) * r.random()
                break
        minute = int(r.integers(8 * 60 + 25, 16 * 60 + 50))
        sites.append(dict(sl_id=ln.sl_id, zone=ln.zone, contract=ln.contract, date=ln.replaced, minute=minute,
                          length=length, surface=surface, paid_base=c[4],
                          paid_extra_ft=_cents(max(0, length - 50) * c[5]), paid_restoration=_cents(rest)))
    st = pd.DataFrame(sites)
    # quarter-end completions closed in the evening: on the last day of the first three quarters each contract
    # closes a job after 8 pm local, which is the next day in UTC; at the March and September ends they are the
    # quarter's long services under pavement, at the June end ordinary ones
    for n_qe, qe in enumerate(K.QUARTER_ENDS):
        for c in K.CONTRACTS_2026:
            r = K.stream("quarter-end", qe.isoformat(), c[0])
            pool = st[(st.contract == c[0]) & (st.date >= qe - dt.timedelta(days=16)) & (st.date < qe)]
            big = n_qe != 1
            k = 1 if (c[0] == "2026-LSL-03" or not big) else 2
            take = list(r.choice(sorted(pool.sl_id), size=k, replace=False))
            for sl in take:
                i = st.index[st.sl_id == sl][0]
                st.at[i, "date"] = qe
                st.at[i, "minute"] = int(r.integers(20 * 60 + 5, 23 * 60 + 35))
                if big:
                    st.at[i, "length"] = int(r.integers(118, 151))
                    st.at[i, "surface"] = "PAVEMENT"
                    st.at[i, "paid_restoration"] = _cents(4600 + 1000 * r.random())
                else:
                    st.at[i, "length"] = int(r.integers(44, 63))
                    st.at[i, "surface"] = "SIDEWALK"
                    st.at[i, "paid_restoration"] = _cents(1250 + 500 * r.random())
                rate = [x for x in K.CONTRACTS_2026 if x[0] == c[0]][0][5]
                st.at[i, "paid_extra_ft"] = _cents(max(0, st.at[i, "length"] - 50) * rate)
                st.at[i, "evening"] = True
                lines.loc[lines.sl_id == sl, "replaced"] = qe
    st["evening"] = st.get("evening", False)
    st["evening"] = st.evening.fillna(False).astype(bool)
    st["quarter"] = st.date.map(K.quarter_of)
    street = {sl: a.split(" ", 1)[1] for sl, a in zip(lines.sl_id, lines.address)}
    address = dict(zip(lines.sl_id, lines.address))
    closed = district_holidays(2026)
    # change orders: every contract-quarter carries several, at least one covering two or more sites; a change
    # order's sites all complete in one quarter and it is approved inside that quarter
    cos = []
    used = set()
    for c in K.CONTRACTS_2026:
        n_co = 0
        for q in (1, 2, 3, 4):
            r = K.stream("change-orders", c[0], q)
            qend = dt.date(2026, 3 * q, 31 if q in (1, 4) else 30)
            pool = st[(st.contract == c[0]) & (st.quarter == q) & ~st.evening &
                      (st.date <= qend - dt.timedelta(days=22))].sort_values("sl_id")
            n_here = int(st[(st.contract == c[0]) & (st.quarter == q)].shape[0])
            want = 2 + n_here // 28
            sizes = [int(r.integers(3, 7))] + [int(r.choice([1, 1, 2, 2, 3, 4])) for _ in range(want - 1)]
            zone_of = dict(zip(pool.sl_id, pool.zone))
            for s_n in sizes:
                free = [s for s in pool.sl_id if s not in used]
                if len(free) < s_n:
                    break
                # a change order covers neighbouring sites: the nearest service lines in the seed's zone
                seed = str(r.choice(free))
                near = sorted((s for s in free if zone_of[s] == zone_of[seed]),
                              key=lambda s: (abs(int(s[2:]) - int(seed[2:])), s))
                if len(near) < s_n:
                    near = sorted(free, key=lambda s: (abs(int(s[2:]) - int(seed[2:])), s))
                pick = sorted(near[:s_n])
                kind = CO_KINDS[int(r.integers(len(CO_KINDS)))]
                if kind[1] == "site":
                    amt = sum(kind[2] + (kind[3] - kind[2]) * r.random() for _ in pick)
                else:
                    amt = kind[2] + (kind[3] - kind[2]) * r.random() + 350 * (len(pick) - 1)
                last_done = max(st.loc[st.sl_id.isin(pick), "date"])
                appr = last_done + dt.timedelta(days=int(r.integers(3, 21)))
                appr = min(appr, qend)
                while appr.weekday() >= 5 or appr in closed:
                    appr -= dt.timedelta(days=1)
                n_co += 1
                used.update(pick)
                co_no = "CO-%s-%03d" % (c[0][-2:], n_co)
                cos.append(dict(co_no=co_no, contract=c[0], approved=appr,
                                description=co_description(co_no, kind[0], pick, street, address),
                                amount=_cents(amt), sites=list(pick), quarter=q))
    co = pd.DataFrame(cos)
    st["co_no"] = ""
    for row in co.itertuples():
        st.loc[st.sl_id.isin(row.sites), "co_no"] = row.co_no
    # re-closed work orders: a restoration correction re-closes one or two sites per contract
    st["reclosed_restoration"] = np.nan
    st["reclosed_days"] = 0
    for c in K.CONTRACTS_2026:
        r = K.stream("reclose", c[0])
        pool = sorted(st[(st.contract == c[0]) & (st.co_no == "") & ~st.evening].sl_id)
        for sl in r.choice(pool, size=2 if c[0] != "2026-LSL-03" else 1, replace=False):
            i = st.index[st.sl_id == sl][0]
            st.at[i, "reclosed_restoration"] = _cents(st.at[i, "paid_restoration"] + float(r.choice([-1, 1])) *
                                                      (280 + 900 * r.random()))
            st.at[i, "reclosed_days"] = int(r.integers(6, 31))
    return lines, st.reset_index(drop=True), co


def site_total(st: pd.DataFrame) -> pd.Series:
    """What a site was paid before change orders, on its latest closing."""
    rest = st.reclosed_restoration.where(st.reclosed_restoration.notna(), st.paid_restoration)
    return st.paid_base + st.paid_extra_ft + rest


def payments_answer(st: pd.DataFrame, co: pd.DataFrame) -> dict:
    """(contract, quarter) -> paid per full replacement completed, unrounded: the sites' paid base, extra length
    and restoration on their latest closing, plus each change order once, over the sites completed (local time)."""
    tot = site_total(st)
    out = {}
    for c in K.CONTRACTS_2026:
        for q in (1, 2, 3, 4):
            m = (st.contract == c[0]) & (st.quarter == q)
            cos = co[(co.contract == c[0]) & (co.quarter == q)].amount.sum()
            out[(c[0], q)] = (float(tot[m].sum()) + float(cos)) / int(m.sum())
    return out
