"""Ask ceiling on the cut pack (python3 ceiling.py [task_dir]). Reads only target/; imports nothing from the generator.

Each responder's ask figures are computed from the shipped files the way that responder works, scored against an
independent computation of the golden, a hit within half a unit of the asked rounding. The pair is priced on
38 + 7 + 55 L for a response on the call and 5 + 7 + 55 L for one off it.
"""
import hashlib
import os
import sys
import datetime as dt
import pandas as pd

TASK = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(TASK, "target")
CUT = "2026-10-20"
Q3 = (dt.date(2026, 7, 1), dt.date(2026, 9, 30))


def f(name):
    return os.path.join(T, name)


def digest():
    h = hashlib.sha256()
    for fn in sorted(os.listdir(T)):
        h.update(fn.encode())
        h.update(open(f(fn), "rb").read())
    return h.hexdigest()[:16]


hubs = pd.read_csv(f("hub_register.csv"))
KEYS = list(hubs.hub_name)
loc2hub = dict(zip(hubs.tracking_location, hubs.hub_name))
no2hub = dict(zip(hubs.hub_no, hubs.hub_name))
site2hub = dict(zip(hubs.cmms_site, hubs.hub_name))
area2hub = dict(zip(hubs.cs_area, hubs.hub_name))


def night(ts_local):
    return (ts_local - pd.Timedelta(hours=12)).dt.date


# ------------------------------------------------------------------------------------------------- claims

cases = pd.read_csv(f("damage_claims_cases_2026-10-23.csv"), dtype={"account": str})
cases["account"] = cases.account.fillna("")
trans = pd.read_excel(f("claims_transfers_2026.xlsx"), dtype={"value_date": str})
refunds = pd.read_csv(f("card_refunds_settlement_2026-07-01_2026-10-22.csv"))
trk = pd.read_parquet(f("tracking_events_claimed_parcels.parquet"))
terms = pd.read_excel(f("flat_rate_damage_terms.xlsx"), dtype={"account": str})
rate = dict(zip(terms.account, terms.eur_per_carton))

srt = trk[trk.event == "SORT"].sort_values(["tracking_no", "ts_utc"]).drop_duplicates("tracking_no")
srt_local = pd.to_datetime(srt.ts_utc.str[:19]) + pd.Timedelta(hours=2)
p_hub = dict(zip(srt.tracking_no, srt.location.map(loc2hub)))
p_night = dict(zip(srt.tracking_no, night(srt_local)))


def approved_parcels():
    first = cases.sort_values(["opened", "case_ref"]).drop_duplicates("tracking_no")
    first = first[(first.status == "APPROVED") & (first.decided <= CUT)].copy()
    first["night"] = first.tracking_no.map(p_night)
    first = first[first.night.apply(lambda d: isinstance(d, dt.date) and Q3[0] <= d <= Q3[1])]
    first["hub"] = first.tracking_no.map(p_hub)
    return first


def refund_match(days=3):
    pc = cases[(cases.claimant == "PARTICULAR") & (cases.status == "APPROVED")].sort_values(["decided", "case_ref"])
    rf = refunds.copy()
    rf["d"] = rf.created_utc.str[:10]
    used, out = set(), {}
    by = {a: g for a, g in rf.groupby(rf.amount.round(2))}
    for c in pc.itertuples():
        g = by.get(round(float(c.approved_eur), 2))
        if g is None:
            continue
        hi = (dt.date.fromisoformat(c.decided) + dt.timedelta(days=days)).isoformat()
        cand = g[(g.d >= c.decided) & (g.d <= hi) & ~g.id.isin(used)]
        if len(cand):
            used.add(cand.id.iloc[0])
            out[c.tracking_no] = (float(cand.amount.iloc[0]), cand.d.iloc[0])
    return out


def claims_fig(expand, refunds_mode):
    first = approved_parcels()
    first["k"] = [round(a / rate[ac]) if (expand and ac in rate) else 1 for a, ac in zip(first.approved_eur, first.account)]
    cnt = first.groupby("hub").k.sum().reindex(KEYS).fillna(0)
    keep = set(first.tracking_no)
    case_parcel = dict(zip(cases.case_ref, cases.tracking_no))
    tr = trans[trans.value_date.str[:10] <= CUT].copy()
    tr["parcel"] = tr.case_ref.map(case_parcel)
    tr = tr[tr.parcel.isin(keep)]
    eur = tr.groupby(tr.parcel.map(p_hub)).amount_eur.sum().reindex(KEYS).fillna(0)
    if refunds_mode == "matched":
        m = refund_match()
        add = pd.Series({p: a for p, (a, d) in m.items() if p in keep and d <= CUT})
        eur = eur.add(add.groupby(add.index.map(p_hub)).sum(), fill_value=0).reindex(KEYS).fillna(0)
    elif refunds_mode == "pro_rata":
        tot = refunds[refunds.created_utc.str[:10] <= CUT].amount.sum()
        pv = first[first.claimant == "PARTICULAR"].groupby("hub").approved_eur.sum().reindex(KEYS).fillna(0)
        eur = eur + tot * pv / pv.sum()
    return cnt, eur


def claims_raw():
    a = cases[cases.status == "APPROVED"]
    return (a.groupby(a.hub.map(area2hub)).size().reindex(KEYS).fillna(0),
            a.groupby(a.hub.map(area2hub)).approved_eur.sum().reindex(KEYS).fillna(0))


# ------------------------------------------------------------------------------------------------- stoppages

ev = pd.read_csv(f("sorter_event_log_q3_2026.csv"), dtype={"reason": str})
ev["reason"] = ev.reason.fillna("")
ev["ts"] = pd.to_datetime(ev.ts_utc) + pd.Timedelta(hours=2)
ev["hub"] = ev.hub_no.map(no2hub)
wo = pd.read_excel(f("sorter_work_orders_q3_2026.xlsx"), dtype=str)
wo = wo[wo.order_type == "CORRECTIVE"].copy()
wo["ms"] = pd.to_datetime(wo.machine_stopped, format="%d/%m/%Y %H:%M")
wo["mr"] = pd.to_datetime(wo.machine_running, format="%d/%m/%Y %H:%M")
wo["hub"] = wo.site.map(site2hub)


def spells(sources):
    rows, lone = [], []
    e = ev[ev.source.isin(sources) & ev.event.isin(["STOP", "RUN"])]
    for (h, s), g in e.groupby(["hub", "source"]):
        stop = None
        for x in g.sort_values("ts", kind="mergesort").itertuples():
            if x.event == "STOP":
                stop = (x.ts, x.reason)
            elif stop is not None:
                rows.append((h, s, stop[0], x.ts, stop[1])); stop = None
            else:
                lone.append((h, s, x.ts))
    return pd.DataFrame(rows, columns=["hub", "src", "t0", "t1", "reason"]), pd.DataFrame(lone, columns=["hub", "src", "t1"])


def stop_fig(sp):
    sp = sp[night(sp.t0).between(Q3[0], Q3[1])]
    g = sp.groupby("hub")
    return (g.size().reindex(KEYS).fillna(0),
            g.apply(lambda d: (d.t1 - d.t0).dt.total_seconds().sum() / 3600).reindex(KEYS).fillna(0))


def stop_golden():
    plc, lone = spells(["PLC"])
    sis, _ = spells(["SIS"])
    saf = plc[plc.reason == "SAFETY"]
    add = []
    for h, g in sis.groupby("hub"):
        fh = saf[saf.hub == h]
        pts = []
        for x in g.itertuples():
            c = fh[(fh.t0 >= x.t0) & (fh.t0 <= x.t0 + pd.Timedelta(minutes=12))]
            c = c[((c.t1 - c.t0) - (x.t1 - x.t0)).dt.total_seconds().between(0, 60)]
            if len(c) == 1:
                pts.append(((x.t0 - pd.Timestamp("2026-07-01")).total_seconds() / 86400, (c.t0.iloc[0] - x.t0).total_seconds()))
        n = len(pts)
        mx = sum(p[0] for p in pts) / n; my = sum(p[1] for p in pts) / n
        b = sum((p[0] - mx) * (p[1] - my) for p in pts) / sum((p[0] - mx) ** 2 for p in pts)
        a = my - b * mx
        for x in g.itertuples():
            d = (x.t0 - pd.Timestamp("2026-07-01")).total_seconds() / 86400
            trip = x.t0 + pd.Timedelta(seconds=a + b * d)
            if not ((fh.t0 - trip).abs() <= pd.Timedelta(seconds=20)).any():
                nx = lone[(lone.hub == h) & (lone.t1 > trip)].sort_values("t1")
                add.append((h, "SIS", trip, nx.t1.iloc[0], "SAFETY"))
    lg = pd.concat([plc, pd.DataFrame(add, columns=plc.columns)], ignore_index=True)
    extra = []
    for x in wo.itertuples():
        hit = lg[(lg.hub == x.hub) & (lg.t0 <= x.mr + pd.Timedelta(minutes=2)) & (lg.t1 >= x.ms - pd.Timedelta(minutes=2))]
        if not len(hit):
            extra.append((x.hub, "WO", x.ms, x.mr, ""))
    return pd.concat([lg, pd.DataFrame(extra, columns=plc.columns)], ignore_index=True)


def stop_deep():
    """A cracker past the battery: counts each PLC RUN no STOP precedes as a stoppage, timed from the safety
    system's STOP before it as written."""
    plc, lone = spells(["PLC"])
    sis, _ = spells(["SIS"])
    add = []
    for x in lone.itertuples():
        prev = sis[(sis.hub == x.hub) & (sis.t0 < x.t1)].sort_values("t0")
        if len(prev):
            add.append((x.hub, "SIS", prev.t0.iloc[-1], x.t1, ""))
    return pd.concat([plc, pd.DataFrame(add, columns=plc.columns)], ignore_index=True)


def stop_all_sources():
    sp, _ = spells(["PLC", "SIS"])
    return sp.drop_duplicates(["hub", "t0"])


def stop_plc_plus_orders():
    plc, _ = spells(["PLC"])
    w = wo.rename(columns={"ms": "t0", "mr": "t1"}).assign(src="WO", reason="")[["hub", "src", "t0", "t1", "reason"]]
    return pd.concat([plc, w], ignore_index=True)


# ------------------------------------------------------------------------------------------------- scoring

def score(fig, gold, unit):
    return int(((fig - gold).abs() <= unit / 2 + 1e-9).sum())


def main():
    gc, ge = claims_fig(True, "matched")
    gs, gh = stop_fig(stop_golden())
    gold = {"claims": (gc, 1), "claims_eur": (ge.round(2), 1), "stoppages": (gs, 1), "hours": (gh, 0.1)}
    resp = {
        "cracker": dict(zip(gold, list(claims_fig(False, "none")) + list(stop_fig(spells(["PLC"])[0])))),
        "deep_cracker": dict(zip(gold, list(claims_fig(False, "none")) + list(stop_fig(stop_deep())))),
        "full_includer_a": dict(zip(gold, list(claims_fig(False, "pro_rata")) + list(stop_fig(stop_all_sources())))),
        "full_includer_b": dict(zip(gold, list(claims_fig(False, "none")) + list(stop_fig(stop_plc_plus_orders())))),
        "full_includer_c": dict(zip(gold, list(claims_fig(True, "pro_rata")) + list(stop_fig(stop_all_sources())))),
        "cracker_expand": dict(zip(gold, list(claims_fig(True, "none")) + list(stop_fig(spells(["PLC"])[0])))),
        "no_repair": dict(zip(gold, list(claims_raw()) + [ev[ev.event == "STOP"].groupby("hub").size().reindex(KEYS).fillna(0),
                                                           stop_fig(stop_all_sources())[1]])),
    }
    n = sum(len(v[0]) for v in gold.values())
    print("pack digest", digest(), "| ask figures", n)
    print("golden:")
    print(pd.DataFrame({k: v[0] for k, v in gold.items()}).round(2).to_string())
    kept = {}
    for name, r in resp.items():
        per = {k: score(r[k], gold[k][0], gold[k][1]) for k in gold}
        kept[name] = sum(per.values()) / n
        print("%-16s" % name, " ".join("%s %d/6" % (k, v) for k, v in per.items()), "| kept %.3f" % kept[name])
    lc = kept["cracker"]
    ls = max(kept["full_includer_a"], kept["full_includer_b"], kept["full_includer_c"])
    on_off = ((38 + 7 + 55 * lc) + (5 + 7 + 55 * ls)) / 2
    both_on = 38 + 7 + 55 * lc
    deep_on = 38 + 7 + 55 * kept["deep_cracker"]
    print("pair, cracker on the call and the full includer off it: %.1f" % on_off)
    print("pair, two crackers on the call: %.1f" % both_on)
    print("pair, two deep crackers on the call: %.1f" % deep_on)
    print("pair, two crackers who read the flat rates as cartons on the call: %.1f" % (38 + 7 + 55 * kept["cracker_expand"]))
    print("mirror leakage (the full includer's keep of the ask weight): %.1f per cent" % (100 * ls))
    return dict(kept=kept, on_off=on_off, both_on=both_on, deep_on=deep_on, digest=digest())


if __name__ == "__main__":
    main()
