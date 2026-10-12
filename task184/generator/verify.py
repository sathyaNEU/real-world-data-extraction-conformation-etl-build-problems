"""Independent verifier for task184: reads only target/ (and the goldens), never the generator's state, and
recomputes on its own code path every graded figure: the lanes each host stood down on its posted days last summer,
the passengers the unit would move at each airport in each 2027 period, the call, the runner-up and the flip, and the
three 2026 measures. Exits non-zero on any mismatch with generator/figures.json."""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
NAMES = {"CUL": "Cullinvale", "ARD": "Ardcarrig", "FAR": "Faranloe", "HAL": "Halloran Bay", "ESK": "Eskerford",
         "BRN": "Brennagh", "DRM": "Dromkeel", "GLK": "Glenkessan"}
PERIOD_DAYS = {"Late June": 16, "July": 31, "August": 31}
KEY = {"Late June": "late June", "July": "July", "August": "August"}


def minutes(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def standard(arr, lanes):
    """KAS-STD-07 (2026) sections 3 and 4: passengers outside the 20-minute standard."""
    q, out = 0.0, 0.0
    for a, n in zip(arr, lanes):
        cap = 37.5 * n
        if 15.0 * (q + a / 2.0) / cap > 20.0:
            out += a
        q = max(0.0, q + a - cap)
    return out


def load(target):
    f = lambda n: os.path.join(target, n)
    lanes = pd.read_csv(f("checkpoint_lane_counts_20260615_20260831.csv"))
    post = pd.read_csv(f("mobile_unit_postings_2026.csv"), parse_dates=["week_start", "week_end"])
    r26 = pd.read_csv(f("roster_plan_summer2026.csv"))
    wide = pd.read_excel(f("roster_pattern_summer2027.xlsx"), header=None)
    head = wide.index[wide.iloc[:, 0].astype(str) == "Start"][0]
    body = pd.DataFrame(wide.iloc[head + 1: head + 73].values, columns=list(wide.iloc[head]))
    r27 = body.melt(id_vars="Start", var_name="airport", value_name="lanes_planned").rename(
        columns={"Start": "interval_start"})
    r27["lanes_planned"] = r27["lanes_planned"].astype(int)
    r27 = r27.sort_values(["airport", "interval_start"]).reset_index(drop=True)
    sheet = pd.read_excel(f("summer2027_planning_sheet.xlsx"), sheet_name=None, header=None)
    return lanes, post, r26, r27, sheet


def stood_down(lanes, post, r26):
    """For each host: its own lanes open on its posted days against the 2026 roster pattern, by interval."""
    lanes = lanes.copy()
    lanes["t"] = lanes["interval_start"].map(minutes)
    lanes["d"] = pd.to_datetime(lanes["business_date"])
    days = {}
    for _, p in post.iterrows():
        for d in pd.date_range(p["week_start"], p["week_end"]):
            days[d] = p["airport"]
    own = lanes[~lanes["lane"].str.startswith("M")]
    out = {}
    for code, g in r26.groupby("airport"):
        plan = g.assign(t=g["interval_start"].map(minutes)).set_index("t")["lanes_planned"]
        mine = own[(own["airport"] == code) & own["d"].isin([d for d, c in days.items() if c == code])]
        cnt = mine.groupby(["d", "t"]).size().unstack(fill_value=0).reindex(columns=plan.index, fill_value=0)
        # staff and aircrew lanes open before 05:00 and after 21:00 only; the unit screens 05:00 to 21:00
        inside = (plan.index >= 300) & (plan.index < 1260)
        diff = plan.values[None, :] - cnt.values
        diff[:, ~inside] = 0
        if not (diff == diff[0]).all():
            raise SystemExit("verify: %s stood down different lanes on different posted days" % code)
        out[code] = pd.Series(diff[0], index=plan.index)
    return out


def design_days(sheet):
    dd = {}
    for name in PERIOD_DAYS:
        raw = sheet[name]
        head = raw.index[raw.iloc[:, 0].astype(str) == "Interval start"][0]
        body = raw.iloc[head + 1: head + 73]
        cols = list(raw.iloc[head])
        frame = pd.DataFrame(body.values, columns=cols)
        dd[name] = {c: frame[c].astype(float).values for c in cols[1:]}
    return dd


def posting_figures(target):
    lanes, post, r26, r27, sheet = load(target)
    down = stood_down(lanes, post, r26)
    a26 = r26[["airport", "interval_start", "lanes_planned"]].sort_values(["airport", "interval_start"])
    if not a26.reset_index(drop=True).equals(r27[["airport", "interval_start", "lanes_planned"]]):
        raise SystemExit("verify: the 2026 and 2027 roster patterns differ")
    dd = design_days(sheet)
    res = {}
    for code, g in r27.groupby("airport"):
        g = g.assign(t=g["interval_start"].map(minutes)).sort_values("t")
        plan = g["lanes_planned"].values.astype(float)
        unit = np.where((g["t"].values >= 300) & (g["t"].values < 1260), 3.0, 0.0)
        with_unit = plan - down[code].reindex(g["t"].values).values + unit
        res[code] = {}
        for name, days in PERIOD_DAYS.items():
            a = dd[name][code]
            res[code][KEY[name]] = (standard(a, plan) - standard(a, with_unit)) * days
    return res, dd, r27, down


def flip(res, dd, r27, down, pick):
    best = max(sum(v.values()) for c, v in res.items() if c != pick)
    g = r27[r27["airport"] == pick].assign(t=lambda x: x["interval_start"].map(minutes)).sort_values("t")
    plan = g["lanes_planned"].values.astype(float)
    unit = np.where((g["t"].values >= 300) & (g["t"].values < 1260), 3.0, 0.0)
    with_unit = plan - down[pick].reindex(g["t"].values).values + unit
    for k in range(1, 100):
        tot = 0.0
        for name, days in PERIOD_DAYS.items():
            a = dd[name][pick] * (1 - k / 100.0)
            tot += (standard(a, plan) - standard(a, with_unit)) * days
        if tot < best:
            return k
    return None


def passengers_2026(target):
    lanes = pd.read_csv(os.path.join(target, "checkpoint_lane_counts_20260615_20260831.csv"))
    lanes["t"] = lanes["interval_start"].map(minutes)
    span = lanes.groupby(["airport", "lane"])["t"].agg(["min", "max"])
    staff_like = lanes.groupby(["airport", "lane"])["t"].apply(lambda s: ((s >= 300) & (s < 1260)).sum() == 0)
    keep = lanes.set_index(["airport", "lane"]).index.map(lambda k: not staff_like[k])
    tot = lanes[np.asarray(keep)].groupby("airport")["pax_screened"].sum()
    returns = pd.read_csv(os.path.join(target, "operator_traffic_returns_2026.csv"))
    lanes["month"] = lanes["business_date"].str[:7]
    for m in ("2026-07", "2026-08"):
        mine = lanes[np.asarray(keep) & (lanes["month"] == m).values].groupby("airport")["pax_screened"].sum()
        rep = returns[returns["month"] == m].set_index("airport")["departing_passengers"]
        gap = (rep / mine - 1).abs().max()
        if gap > 0.008:
            raise SystemExit("verify: passenger lanes do not reconcile with the operators' returns in %s" % m)
    return {c: float(v) for c, v in tot.items()}, span


def hotel(target):
    inv = pd.read_excel(os.path.join(target, "hotel_invoices_CC4109_summer2026.xlsx"))
    post = pd.read_csv(os.path.join(target, "mobile_unit_postings_2026.csv"))
    port = dict(zip(post["hotel_po"], post["airport"]))
    inv["airport"] = inv["PO"].map(port)
    amount = inv.groupby("airport")["Amount EUR"].sum()
    stays = inv[inv["Line description"].str.startswith("Accommodation")].groupby("airport")["Nights"].sum()
    logged = post.groupby("airport")["officer_nights"].sum()
    if not (stays == logged.reindex(stays.index)).all():
        raise SystemExit("verify: invoiced officer-nights differ from the postings file")
    return {c: float(amount[c] / stays[c]) for c in amount.index}


def claims(target):
    ex = pd.read_csv(os.path.join(target, "expense_claims_CC4109_2026.csv"), parse_dates=["claim_date"])
    post = pd.read_csv(os.path.join(target, "mobile_unit_postings_2026.csv"), parse_dates=["week_start", "week_end"])
    ex = ex.drop_duplicates(subset=["claim_ref", "line_no"])
    first = ex[ex["category"] == "SUBS-DAY"].groupby("claim_ref")["claim_date"].min()

    def home(d):
        hit = post[(post["week_start"] <= d) & (post["week_end"] >= d)]
        return hit["airport"].iloc[0] if len(hit) else None
    ex["airport"] = ex["claim_ref"].map(first).map(lambda d: home(d) if pd.notna(d) else None)
    tot = ex.dropna(subset=["airport"]).groupby("airport")["amount_eur"].sum()
    weeks = post.groupby("airport").size()
    return {c: float(tot[c] / weeks[c]) for c in tot.index}


def r100(x):
    return int(np.floor(x / 100.0 + 0.5)) * 100


def main(target, golden):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    res, dd, r27, down = posting_figures(target)
    tot = {c: sum(v.values()) for c, v in res.items()}
    order = sorted(tot, key=lambda c: -tot[c])
    pick, runner = order[0], order[1]
    k = flip(res, dd, r27, down, pick)
    pas, _ = passengers_2026(target)
    ht = hotel(target)
    cl = claims(target)
    bad = []

    def same(label, got, want):
        if got != want:
            bad.append("%s: verifier %r, figures.json %r" % (label, got, want))
    same("call", NAMES[pick], fig["call"])
    same("runner_up", NAMES[runner], fig["runner_up"])
    same("pick_total", r100(tot[pick]), fig["pick_total"])
    same("runner_total", r100(tot[runner]), fig["runner_total"])
    same("flip_pct", k, fig["flip_pct"])
    for c in res:
        for n in ("late June", "July", "August"):
            same("moved %s %s" % (c, n), r100(res[c][n]), fig["moved"][NAMES[c]][n])
        same("moved_total %s" % c, r100(tot[c]), fig["moved_total"][NAMES[c]])
        same("passengers_2026 %s" % c, r100(pas[c]), fig["passengers_2026"][NAMES[c]])
        same("hotel %s" % c, round(ht[c] + 1e-9, 2), fig["hotel_per_night"][NAMES[c]])
        same("claims %s" % c, round(cl[c] + 1e-9, 2), fig["claims_per_week"][NAMES[c]])
    for f in ("mobile_team_posting_summer_2027.pdf", "mobile_team_effect_2027.xlsx"):
        if not os.path.exists(os.path.join(golden, f)):
            bad.append("missing golden " + f)
    wb = pd.read_excel(os.path.join(golden, "mobile_team_effect_2027.xlsx"), sheet_name=None, header=None)
    flat = {str(v) for sh in wb.values() for v in sh.values.ravel() if pd.notna(v)}
    for c in res:
        for v in (fig["moved_total"][NAMES[c]], fig["passengers_2026"][NAMES[c]]):
            if str(v) not in flat:
                bad.append("workbook lacks %s for %s" % (v, c))
    if bad:
        raise SystemExit("verify FAILED:\n  " + "\n  ".join(bad))
    print("verify: %d airports, %d period figures, the call (%s), runner-up (%s), flip %d%%, and 24 measures recompute "
          "from target/ alone; goldens present" % (len(res), 3 * len(res), NAMES[pick], NAMES[runner], k))


if __name__ == "__main__":
    main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
