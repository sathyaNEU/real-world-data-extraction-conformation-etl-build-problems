"""Independent verifier (python3 verify.py): reads only target/, figures.json and submission.md; imports nothing
from the generator. Recomputes the call, the forward figure and every ask figure; exit 1 on any mismatch."""
import json
import os
import re
import sys
import datetime as dt
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
F = json.load(open(os.path.join(HERE, "figures.json")))
SUB = open(os.path.join(TASK, "submission.md")).read()
BAD = []


def chk(name, cond, detail=""):
    print("%s  %s  %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond:
        BAD.append(name)


def p(fn):
    return os.path.join(T, fn)


hubs = pd.read_csv(p("hub_register.csv"))
name2key = {"Zaragoza Plaza": "ZAZ", "Ribarroja": "VLC", "Dos Hermanas": "SVQ", "San Fernando": "MAD",
            "El Prat": "BCN", "Basauri": "BIO"}
KEYS = list(name2key.values())
key_of_no = {r.hub_no: name2key[r.hub_name] for r in hubs.itertuples()}

# ---------------------------------------------------------------------------------------------- main call
hd = pd.read_csv(p("audit_headers_q3_2026.csv"))
ln = pd.read_parquet(p("audit_findings_q3_2026.parquet"))
ln = ln.merge(hd[hd.audit_type == "ROUTINE"][["audit_id", "cage_label", "hub"]], on="audit_id")
ln = ln[ln.condition.isin(["OK", "DAMAGED"])].copy()
ln["dam"] = (ln.condition == "DAMAGED").astype(int)
ln["h"] = ln.hub.map(name2key)
dws = pd.read_parquet(p("dws_induction_q3_2026.parquet")).sort_values(["barcode", "induct_local"])
d1 = dws.drop_duplicates("barcode").set_index("barcode")
ln["kg"] = ln.barcode.map(d1.weight_g) / 1000.0
ln["shape"] = ln.barcode.map(d1["shape"])
man = pd.read_parquet(p("shipment_lines_q3_2026.parquet")).drop_duplicates("barcode").set_index("barcode")
ln["fragile"] = ln.barcode.map(man.fragile)
bl = pd.read_parquet(p("cage_build_log_q3_2026.parquet"))
ld = bl[bl.event == "LOAD"].groupby(["cage_label", "barcode"]).scan_utc.min().reset_index()
ld["w"] = ld.barcode.map(d1.weight_g).fillna(0) / 1000.0
ld = ld.sort_values(["cage_label", "scan_utc", "barcode"])
ld["above"] = ld.groupby("cage_label").w.transform("sum") - ld.groupby("cage_label").w.cumsum()
ln["above"] = ln.barcode.map(ld.set_index("barcode").above)
ln["band"] = pd.cut(ln.kg, [0, 0.5, 1, 2, 5, 10, 99], labels=False)
ln["loaded"] = (ln.above >= 60).astype(int)
exp = ln.groupby(["shape", "band", "fragile", "loaded"]).dam.transform("mean")
ex = ((ln.dam - exp).groupby(ln.h).sum() / ln.groupby("h").size() * 1e4)
chk("call: Ribarroja leads at equal load", ex.idxmax() == "VLC" and F["call"] == "Ribarroja del Turia", ex.round(1).to_dict())
chk("no other hub within 30 per 10,000 of Ribarroja at equal load", (ex.drop("VLC") <= ex["VLC"] - 30).all(),
    ex.round(2).to_dict())
chk("Zaragoza below the network at equal load", ex["ZAZ"] < 0, "%.2f" % ex["ZAZ"])
chk("own sorter damage to the nearest 10", int(round(ex["VLC"] / 10) * 10) == F["vlc_own_damage_per_10k"],
    "%.2f" % ex["VLC"])
plan = pd.read_excel(p("peak_plan_2026.xlsx"))
pk = plan[(plan.basis == "plan") & plan.iso_week.between(48, 52)]["Ribarroja"]
chk("planned parcels a week, weeks 48 to 52", int(round(pk.mean())) == F["vlc_planned_parcels_week"], pk.tolist())
fwd = ex["VLC"] * pk.mean() / 1e4
chk("parcels a week stopped, nearest hundred", int(round(fwd / 100) * 100) == F["parcels_week_stopped"], "%.1f" % fwd)
obs = ln.groupby("h").dam.mean() * 1e4
import statsmodels.api as sm
ln["service"] = ln.barcode.map(man.service)
ldp = ld.copy()
ldp["pos"] = ldp.groupby("cage_label").cumcount()
ldp["n"] = ldp.groupby("cage_label").barcode.transform("size")
ldp["fa"] = (ldp.n - 1 - ldp.pos) / (ldp.n - 1).clip(lower=1)
ldp["cw"] = ldp.groupby("cage_label").w.transform("sum") / 50
ldp["ch"] = ldp.groupby("cage_label").w.transform(lambda x: (x >= 10).sum())
li = ldp.set_index("barcode")
for c in ("fa", "cw", "ch"):
    ln[c] = ln.barcode.map(li[c])
box = (ln["shape"] == "BOX").astype(float)
bag = (ln["shape"] == "BAG").astype(float)
hv = (ln.kg >= 10).astype(float)
base = pd.DataFrame({"c": 1.0, "frag": (ln.fragile == "Y").astype(float), "box": box, "bag": bag,
                     "lkg": np.log(ln.kg.clip(lower=0.05)), "nd": (ln.service == "24H").astype(float),
                     "eco": (ln.service == "ECO").astype(float), "hv": hv})


def bic_fit(f, extra=None):
    X = base.copy()
    X["f"] = f; X["bf"] = box * f; X["gf"] = bag * f; X["hf"] = hv * f
    for k, v in (extra or {}).items():
        X[k] = v
    m = sm.GLM(ln.dam.values, X.values, family=sm.families.Binomial()).fit()
    e = m.predict(X.values)
    exs = (ln.dam - e).groupby(ln.h).sum() / ln.groupby("h").size() * 1e4
    return m.deviance + X.shape[1] * np.log(len(ln)), exs


step = (ln.above >= 60).astype(float)
cand = {"step60": bic_fit(step), "linear": bic_fit(ln.above / 50), "log1p": bic_fit(np.log1p(ln.above)),
        "step60 with position and cage terms": bic_fit(step, {"fa": ln.fa, "cw": ln.cw, "ch": ln.ch, "box_fa": box * ln.fa,
                                                               "box_cw": box * ln.cw, "box_ch": box * ln.ch,
                                                               "fa_cw": ln.fa * ln.cw})}
best = min(cand, key=lambda k: cand[k][0])
chk("the programme's lowest-BIC estimate is the 60 kg step", best == "step60",
    {k: round(v[0], 1) for k, v in cand.items()})
bv = float(cand[best][1]["VLC"])
chk("the lowest-BIC estimate executes to the graded hundred and the nearest 10",
    int(round(bv * pk.mean() / 1e6) * 100) == F["parcels_week_stopped"] and int(round(bv / 10) * 10) == F["vlc_own_damage_per_10k"],
    "%.2f -> %.1f" % (bv, bv * pk.mean() / 1e4))

# ---------------------------------------------------------------------------------------------- claims
loc = {r.tracking_location: name2key[r.hub_name] for r in hubs.itertuples()}
cases = pd.read_csv(p("damage_claims_cases_2026-10-23.csv"), dtype={"account": str})
cases["account"] = cases.account.fillna("")
trk = pd.read_parquet(p("tracking_events_claimed_parcels.parquet"))
s = trk[trk.event == "SORT"].sort_values(["tracking_no", "ts_utc"]).drop_duplicates("tracking_no")
loc_t = pd.to_datetime(s.ts_utc.str[:19]) + pd.Timedelta(hours=2)
s = s.assign(h=s.location.map(loc), night=(loc_t - pd.Timedelta(hours=12)).dt.strftime("%Y-%m-%d"))
s = s.set_index("tracking_no")
terms = pd.read_excel(p("flat_rate_damage_terms.xlsx"), dtype={"account": str}).set_index("account").eur_per_carton
fc = cases.sort_values(["opened", "case_ref"]).drop_duplicates("tracking_no")
fc = fc[(fc.status == "APPROVED") & (fc.decided <= "2026-10-20")].copy()
fc["night"] = fc.tracking_no.map(s.night)
fc = fc[(fc.night >= "2026-07-01") & (fc.night <= "2026-09-30")]
fc["h"] = fc.tracking_no.map(s.h)
fc["k"] = [round(a / terms[c]) if c in terms.index else 1 for a, c in zip(fc.approved_eur, fc.account)]
cnt = fc.groupby("h").k.sum()
keep = set(fc.tracking_no)
tr = pd.read_excel(p("claims_transfers_2026.xlsx"), dtype={"value_date": str})
tr = tr[tr.value_date.str[:10] <= "2026-10-20"]
tr["parcel"] = tr.case_ref.map(cases.set_index("case_ref").tracking_no)
tr = tr[tr.parcel.isin(keep)]
eur = tr.groupby(tr.parcel.map(s.h)).amount_eur.sum()
rf = pd.read_csv(p("card_refunds_settlement_2026-07-01_2026-10-22.csv"))
rf["d"] = rf.created_utc.str[:10]
used, add = set(), []
pv = cases[(cases.claimant == "PARTICULAR") & (cases.status == "APPROVED")].sort_values(["decided", "case_ref"])
for c in pv.itertuples():
    hi = (dt.date.fromisoformat(c.decided) + dt.timedelta(days=3)).isoformat()
    cand = rf[(rf.amount.round(2) == round(c.approved_eur, 2)) & (rf.d >= c.decided) & (rf.d <= hi) & ~rf.id.isin(used)]
    if len(cand):
        used.add(cand.id.iloc[0])
        if c.tracking_no in keep and cand.d.iloc[0] <= "2026-10-20":
            add.append((s.h.get(c.tracking_no), float(cand.amount.iloc[0])))
ad = pd.DataFrame(add, columns=["h", "a"]).groupby("h").a.sum()
eur = eur.add(ad, fill_value=0)
from pypdf import PdfReader
note = re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in PdfReader(p("damage_claims_handling_note.pdf")).pages))
chk("CS-FIN 07 files a flat-rate case's grain and approval basis (read back from the PDF)",
    "opens one case for all the damaged cartons of a consignment, under the tracking number of its first carton" in note
    and "approves it at the account's rate for each damaged carton" in note and "counts once" in note, len(note))
fr = cases[(cases.status == "APPROVED") & cases.account.isin(terms.index)]
mult = fr.approved_eur / fr.account.map(terms)
chk("every approved flat-rate case is a whole number of cartons at its account's rate",
    len(fr) > 0 and bool(((mult - mult.round()).abs() < 1e-9).all()), "%d cases" % len(fr))
for k in KEYS:
    chk("claims %s" % k, int(cnt.get(k, 0)) == F["claims_%s" % k], int(cnt.get(k, 0)))
    chk("claims euros %s" % k, int(round(eur.get(k, 0))) == F["claims_eur_%s" % k], "%.2f" % eur.get(k, 0))

# ---------------------------------------------------------------------------------------------- stoppages
ev = pd.read_csv(p("sorter_event_log_q3_2026.csv"), dtype={"reason": str})
ev["reason"] = ev.reason.fillna("")
ev["ts"] = pd.to_datetime(ev.ts_utc) + pd.Timedelta(hours=2)
ev["h"] = ev.hub_no.map(key_of_no)


def spells(src):
    out, lone = [], []
    for h, g in ev[(ev.source == src) & ev.event.isin(["STOP", "RUN"])].groupby("h"):
        st = None
        for x in g.sort_values("ts", kind="mergesort").itertuples():
            if x.event == "STOP":
                st = (x.ts, x.reason)
            elif st:
                out.append((h, st[0], x.ts, st[1])); st = None
            else:
                lone.append((h, x.ts))
    return pd.DataFrame(out, columns=["h", "t0", "t1", "r"]), pd.DataFrame(lone, columns=["h", "t1"])


plc, lone = spells("PLC")
trip = ev[(ev.source == "SIS") & (ev.event == "TRIP")]
chk("the safety system logs TRIPs with a cause code and nothing else", set(ev[ev.source == "SIS"].event) == {"TRIP"} and
    trip.reason.str.len().gt(0).all(), ev[ev.source == "SIS"].event.value_counts().to_dict())
pair = [((plc[(plc.h == x.h) & (plc.r == "SAFETY")].t0 - x.ts).dt.total_seconds().abs().min()) for x in trip.itertuples()]
chk("every TRIP sits within a second of a PLC SAFETY stop or inside a spell whose STOP the log lost",
    sum(v <= 1 for v in pair) + len(lone) == len(trip), "%d echoed, %d RUNs no STOP precedes" % (sum(v <= 1 for v in pair), len(lone)))
extra = []
for x in lone.itertuples():
    prev = trip[(trip.h == x.h) & (trip.ts < x.t1)].ts.max()   # the TRIP before each RUN no STOP precedes
    extra.append((x.h, prev, x.t1, "SAFETY"))
allsp = pd.concat([plc, pd.DataFrame(extra, columns=plc.columns)], ignore_index=True)
wo = pd.read_excel(p("sorter_work_orders_q3_2026.xlsx"), dtype=str)
wo = wo[wo.order_type == "CORRECTIVE"]
site = {r.cmms_site: name2key[r.hub_name] for r in hubs.itertuples()}
add = []
for x in wo.itertuples():
    h = site[x.site]
    ms = pd.to_datetime(x.machine_stopped, format="%d/%m/%Y %H:%M")
    mr = pd.to_datetime(x.machine_running, format="%d/%m/%Y %H:%M")
    if not ((allsp.h == h) & (allsp.t0 <= mr + pd.Timedelta(minutes=2)) & (allsp.t1 >= ms - pd.Timedelta(minutes=2))).any():
        add.append((h, ms, mr, ""))
allsp = pd.concat([allsp, pd.DataFrame(add, columns=plc.columns)], ignore_index=True)
nt = (allsp.t0 - pd.Timedelta(hours=12)).dt.strftime("%Y-%m-%d")
allsp = allsp[(nt >= "2026-07-01") & (nt <= "2026-09-30")]
hrs = allsp.assign(x=(allsp.t1 - allsp.t0).dt.total_seconds() / 3600).groupby("h").x.sum()
for k in KEYS:
    chk("stoppages %s" % k, int((allsp.h == k).sum()) == F["stoppages_%s" % k], int((allsp.h == k).sum()))
    chk("hours stood %s" % k, round(float(hrs[k]), 1) == F["hours_%s" % k], "%.3f" % hrs[k])

# ---------------------------------------------------------------------------------------------- write-up
for k, v in F.items():
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        txt = "{:,}".format(v) if isinstance(v, int) else ("%.1f" % v)
        chk("write-up carries %s" % k, txt in SUB, txt)
chk("no em or en dash in the write-up", "\u2014" not in SUB and "\u2013" not in SUB)
print("%d FAIL" % len(BAD))
sys.exit(1 if BAD else 0)
