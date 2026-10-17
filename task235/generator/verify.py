"""Independent verifier: reads only the shipped bundle (target/, golden/, figures.json, submission.md) and recomputes
every graded figure with its own code, then checks the goldens and the write-up carry them."""
import csv
import json
import os
from decimal import Decimal, ROUND_HALF_UP

import numpy as np
import pandas as pd

VAL = "purchase_service_validations_2026-10-05_to_2026-11-09.csv"
EVT = "warehouse_purchase_completed_2026-10-05_to_2026-11-09.csv"
SES = "session_service_starts_2026-10-05_to_2026-11-09.csv"
LNK = "account_service_links_2026-10-05_to_2026-11-09.csv"
FX = "ecb_euro_reference_rates_2026-09-28_to_2026-11-06.csv"
REG = "build_register.xlsx"
ZERO_DECIMALS = ("JPY", "KRW")


def ts(col):
    return pd.to_datetime(col.str.rstrip("Z"), format="%Y-%m-%dT%H:%M:%S.%f")


def dublin_date(t):
    # Irish Summer Time (UTC+1) ends at 01:00 UTC on Sunday 25 October 2026
    return (t + pd.to_timedelta((t < pd.Timestamp("2026-10-25 01:00")).astype(int), unit="h")).dt.date


def compute(target):
    v = pd.read_csv(os.path.join(target, VAL), dtype=str, keep_default_na=False)
    reg = pd.read_excel(os.path.join(target, REG), sheet_name="Builds", dtype=str)
    label = {r.build_number: ("iOS " if r.platform == "ios" else "Android ") + r.version for r in reg.itertuples()}
    buy = v[(v.transaction_kind == "purchase") & (v.environment == "Production") & (v.purchase_type == "standard")].copy()
    buy["when"] = ts(buy.purchased_at)
    buy["date"] = dublin_date(buy["when"])
    lo, hi = pd.Timestamp("2026-10-12").date(), pd.Timestamp("2026-11-08").date()
    buy = buy[(buy.date >= lo) & (buy.date <= hi)]
    assert buy.store_transaction_id.is_unique
    buy["build"] = buy.app_build.map(label)
    assert buy.build.notna().all()
    # each transaction's event, the first copy the warehouse received
    ev = pd.read_csv(os.path.join(target, EVT), dtype=str, keep_default_na=False)
    ev["got"] = ts(ev.received_at)
    first = ev.groupby("store_transaction_id").got.min()
    buy["got"] = buy.store_transaction_id.map(first)
    # the next session start of the same device after the purchase
    se = pd.read_csv(os.path.join(target, SES), dtype=str, keep_default_na=False, usecols=["device_id", "account_id", "started_at"])
    se["start"] = ts(se.started_at)
    left = buy[["store_transaction_id", "device_id", "when"]].sort_values("when")
    right = se[["device_id", "start"]].sort_values("start")
    nxt = pd.merge_asof(left, right, left_on="when", right_on="start", by="device_id", direction="forward",
                        allow_exact_matches=False)
    buy["next"] = buy.store_transaction_id.map(nxt.set_index("store_transaction_id").start)
    loss = {}
    detail = {}
    parts = {}
    for b, g in buy.groupby("build"):
        came_back = g.next.notna()
        arrived = g.got.notna()
        lost = int((came_back & ~arrived).sum())
        waited = int((came_back & arrived & (g.got >= g.next)).sum())
        still = int((~came_back & ~arrived).sum())
        share = lost / (lost + waited) if lost + waited else 0.0
        loss[b] = (lost + still * share) / len(g)
        detail[b] = (len(g), lost, still, lost / len(g))
        parts[b] = (len(g), lost, waited, still)
    alerts = sorted(b for b, x in loss.items() if x > 0.02)
    # the same alerts whatever share of the open purchases is lost, between none and the platform's or the pooled rate
    rate = lambda bs: sum(parts[b][1] for b in bs) / sum(parts[b][1] + parts[b][2] for b in bs)
    plat = {pl: rate([b for b in parts if b.startswith(pl)]) for pl in ("iOS", "Android")}
    for q_of in (lambda b: 0.0, lambda b: plat[b.split()[0]], lambda b: rate(list(parts))):
        alt = {b: (x[1] + x[3] * q_of(b)) / x[0] for b, x in parts.items()}
        assert sorted(b for b, x in alt.items() if x > 0.02) == alerts, alt
    # paying players: the account links, and each guest account joined to the account its device shows next
    ln = pd.read_csv(os.path.join(target, LNK), dtype=str)
    seen = pd.concat([v.loc[v.device_id != "", ["device_id", "account_id"]].assign(at=ts(v.loc[v.device_id != "", "purchased_at"])),
                      se[["device_id", "account_id"]].assign(at=se.start)]).sort_values(["device_id", "at"], kind="mergesort")
    seen["after"] = seen.groupby("device_id").account_id.shift(-1)
    hop = seen[seen.account_id.str.startswith("gst_") & seen.after.notna() & ~seen.after.fillna("gst_").str.startswith("gst_")]
    boss = {}

    def root(a):
        path = []
        while boss.get(a, a) != a:
            path.append(a)
            a = boss[a]
        for x in path:
            boss[x] = a
        return a
    for a, b2 in list(zip(ln.from_account_id, ln.to_account_id)) + list(zip(hop.account_id, hop.after)):
        ra, rb = root(a), root(b2)
        if ra != rb:
            boss[ra] = rb
    payers = {b: len({root(a) for a in g.account_id}) for b, g in buy.groupby("build")}
    # gross bookings: each price at its currency's minor unit, the ECB rate in force on the Irish date, line by line
    fx = pd.read_csv(os.path.join(target, FX), dtype={"currency": str})
    fx["d"] = pd.to_datetime(fx.date).astype("datetime64[ns]")
    eur = {}
    buy["d"] = pd.to_datetime(buy.date).astype("datetime64[ns]")
    rows = []
    for cur, g in buy.groupby("currency"):
        amount = g.price_minor.astype(int) / (1 if cur in ZERO_DECIMALS else 100)
        if cur == "EUR":
            conv = amount.astype(float)
        else:
            r = fx[fx.currency == cur].sort_values("d")
            m = pd.merge_asof(g[["d"]].reset_index().sort_values("d"), r[["d", "rate"]], on="d", direction="backward")
            rate = m.set_index("index").rate.reindex(g.index)
            conv = amount / rate
        rows.append(pd.DataFrame({"build": g.build, "eur": np.round(conv.values.astype(float) + 1e-9, 2)}))
    lines = pd.concat(rows)
    eur = lines.groupby("build").eur.sum().round(2).to_dict()
    arppu = {b: (Decimal(int(round(eur[b] * 100))) / 100 / payers[b]).quantize(Decimal("0.01"), ROUND_HALF_UP)
             for b in eur}
    return dict(loss=loss, alerts=alerts, detail=detail, payers=payers, eur=eur, arppu=arppu, label=label)


def main(target, golden, figs_path, sub_path):
    V = compute(target)
    assert V["alerts"] == ["Android 7.41.0", "iOS 7.42.0"], V["alerts"]
    rows = list(csv.DictReader(open(os.path.join(golden, "tracking_loss_alerts_2026-11-09.csv"))))
    assert len(rows) == 12
    for r in rows:
        b = ("iOS " if r["platform"] == "ios" else "Android ") + r["version"]
        assert V["label"][r["build_number"]] == b
        assert (r["alert"] == "yes") == (b in V["alerts"]), (b, r)
        assert int(r["paying_players"]) == V["payers"][b], (b, r, V["payers"][b])
        assert r["gross_bookings_per_paying_player_eur"] == str(V["arppu"][b]), (b, r, V["arppu"][b])
    png = os.path.join(golden, "tracking_loss_by_build_2026-11-09.png")
    assert open(png, "rb").read(8) == b"\x89PNG\r\n\x1a\n" and os.path.getsize(png) > 40_000
    assert sorted(os.listdir(golden)) == ["tracking_loss_alerts_2026-11-09.csv", "tracking_loss_by_build_2026-11-09.png"]
    figs = json.load(open(figs_path))
    assert figs["call"] == ["iOS 7.42.0", "Android 7.41.0"] or sorted(figs["call"]) == V["alerts"]
    for b, x in figs["builds"].items():
        assert x["chart_tracking_loss_pct"] == "%.2f" % (100 * V["loss"][b]) and x["paying_players"] == V["payers"][b]
        assert x["gross_bookings_per_paying_player_eur"] == str(V["arppu"][b]) and x["alert"] == (b in V["alerts"])
    n, lost, still, low = V["detail"]["Android 7.41.0"]
    c = figs["components"]["Android 7.41.0"]
    assert (c["purchases"], c["lost"], c["open"]) == (n, lost, still) and still == 0
    n, lost, still, low = V["detail"]["iOS 7.42.0"]
    c = figs["components"]["iOS 7.42.0"]
    assert (c["purchases"], c["lost"], c["open"]) == (n, lost, still) and c["if_every_open_event_arrives"] == "%.2f" % (100 * low)
    assert c["if_no_open_event_arrives"] == "%.2f" % (100 * (lost + still) / n)
    c = figs["components"]["highest_other_lost"]
    top = max((b for b in V["detail"] if b not in V["alerts"]), key=lambda b: V["detail"][b][3])
    assert c["build"] == top and (c["purchases"], c["lost"], c["open"]) == V["detail"][top][:3]
    assert c["lost_pct"] == "%.2f" % (100 * V["detail"][top][3])
    sub = open(sub_path).read()
    assert "—" not in sub and "–" not in sub
    block4 = sub.split("## 4. Deliverable Answers")[1]
    for r in rows:
        b = ("iOS " if r["platform"] == "ios" else "Android ") + r["version"]
        line = "   - %s, build %s: %s, %s paying players, gross bookings per paying player %s" % (
            b, r["build_number"], "alert" if r["alert"] == "yes" else "no alert",
            format(int(r["paying_players"]), ","), r["gross_bookings_per_paying_player_eur"])
        assert line in block4, line
    print("verify: the alert pair (the same at every rate for the open purchases), the components, 12 paying-player "
          "counts and 12 gross bookings per paying player recomputed from the bundle; goldens, figures.json and the "
          "write-up carry them")
