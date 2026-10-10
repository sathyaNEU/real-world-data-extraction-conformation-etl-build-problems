"""task127 generator: the two asks, computed from the files as written, with every designed stop.

Ask A, the pilot's installed cost by co-op: average installed cost per rebated install (whole dollars) and the
rebate as a share of that cost (per cent, one decimal). Ask B, the pilot rebates paid through 30 November 2026
by co-op: dollars (whole dollars) and the pilot installs those payments cover.
"""
import json
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

import params as P

F = P.F
CT = ZoneInfo("America/Chicago")
NAME2CODE = {v: k for k, v in P.COOP_NAME.items()}
SCHED = {"propane furnace (ducted)": 3600, "electric resistance": 4200, "propane boiler (hydronic)": 5400}
HEAD_LINE = "multi-zone heat pump system, indoor head"


def load(tgt):
    tgt = Path(tgt)
    inv = pd.read_csv(tgt / F["invoices"], dtype=str, keep_default_na=False)
    inv["amt"] = inv.amount_usd.astype(float)
    inv["version"] = inv.version.astype(int)
    led = pd.read_csv(tgt / F["ledger"], dtype=str, keep_default_na=False)
    led["amt"] = led.amount_usd.astype(float)
    ret = json.loads((tgt / F["returns"]).read_text())
    pl = pd.read_excel(tgt / F["pilot"], sheet_name="rebates", dtype={"premises_id": str, "rebate_id": str})
    pl["c"] = pl.coop.map(NAME2CODE)
    return dict(inv=inv, led=led, ret=ret, pl=pl)


def _job_totals(inv, version="record", fix_heads=True):
    rows = {}
    for no, g in inv.groupby("invoice_no"):
        vs = sorted(set(g.version))
        if version == "record":
            acc = sorted(set(g[g.accepted_at != ""].version))
            v = acc[-1]
        elif version == "latest":
            v = vs[-1]
        elif version == "first":
            v = vs[0]
        elif version == "lowest":
            v = min(vs, key=lambda x: g[g.version == x].amt.sum())
        elif version == "all":
            v = None
        gg = g if v is None else g[g.version == v]
        tot = 0.0
        for (_, vv), h in gg.groupby(["invoice_no", "version"]):
            heads = h[h.description.str.startswith(HEAD_LINE)]
            rest = h[~h.description.str.startswith(HEAD_LINE)]
            if fix_heads and len(heads):
                tot += heads.amt.iloc[0] + rest.amt.sum()
            else:
                tot += h.amt.sum()
        rows[g.premises_id.iloc[0]] = tot
    return pd.Series(rows)


def ask_a(D, version="record", fix_heads=True, dedupe_lines=False):
    inv = D["inv"]
    if dedupe_lines:
        inv = inv.drop_duplicates(["invoice_no", "version", "description", "amount_usd"])
    tot = _job_totals(inv, version, fix_heads)
    pl = D["pl"].set_index("premises_id")
    cost = tot.reindex(pl.index)
    assert cost.notna().all()
    reb = pl.heating_system_replaced.map(SCHED) + (pl.income_band == P.IN_BAND[0]) * 1000
    out = {}
    for c in P.COOPS:
        m = (pl.c == c).to_numpy()
        avg = cost[m].sum() / m.sum()
        share = reb[m].sum() / cost[m].sum() * 100
        out[c] = (avg, share)
    return out


def returned_ids(D):
    return {n["original_payment_reference"] for n in D["ret"]["notices"]}


def ask_b(D, clock="central", drop_returned=True, one_per_rebate=False, by_release=False,
          cutoff="2026-11-30"):
    led = D["led"].copy()
    if one_per_rebate:
        led = led.drop_duplicates("rebate_id", keep="first")
    if drop_returned:
        led = led[~led.payment_id.isin(returned_ids(D))]
    if by_release:
        day = led.released_on
    else:
        led = led[led.cleared_at != ""]
        t = pd.to_datetime(led.cleared_at, utc=True)
        day = (t.dt.tz_convert(CT) if clock == "central" else t).dt.strftime("%Y-%m-%d")
    led = led[day <= cutoff]
    coop = D["pl"].set_index("rebate_id").c
    led = led.assign(c=led.rebate_id.map(coop))
    assert led.c.notna().all()
    out = {}
    for c in P.COOPS:
        g = led[led.c == c]
        out[c] = (g.amt.sum(), g.rebate_id.nunique())
    return out


def golden(D):
    a = ask_a(D)
    b = ask_b(D)
    return {c: dict(cost=round(a[c][0]), share=round(a[c][1], 1), paid=round(b[c][0]), covered=b[c][1],
                    cost_raw=a[c][0], share_raw=a[c][1]) for c in P.COOPS}


A_STOPS = {
    "latest delivered version": dict(version="latest"),
    "first version": dict(version="first"),
    "lowest-priced version": dict(version="lowest"),
    "every version summed": dict(version="all"),
    "head lines summed as delivered": dict(fix_heads=False),
    "identical lines removed": dict(dedupe_lines=True),
    "natural read (latest, head lines summed)": dict(version="latest", fix_heads=False),
}
B_STOPS = {
    "ledger as it stands, UTC dates": dict(clock="utc", drop_returned=False),
    "returns dropped, UTC dates": dict(clock="utc"),
    "Central dates, returns kept": dict(drop_returned=False),
    "payment run date": dict(by_release=True),
    "one payment per rebate": dict(one_per_rebate=True),
}
