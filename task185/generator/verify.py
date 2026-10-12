"""Independent verifier for task185: reads only target/ (and the goldens), never the generator's state, and recomputes
on its own code path every graded figure: the conversion of each glass reading to the probe from the parallel
observations, the seasons' heat and severe heat days on the present instrument's basis, the two lines, the burn and the
premium; the 2027/28 schedule by sub-district; and the cover's paid claims by season. Exits non-zero on any mismatch
with generator/figures.json or the goldens."""
import datetime as dt
import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def pdf_text(path):
    from pypdf import PdfReader
    return " ".join(pg.extract_text() for pg in PdfReader(path).pages).replace("\n", " ")


def half_up(x):
    return int(math.floor(x + 0.5))


def glass_register(path):
    out = {}
    for name, df in pd.read_excel(path, sheet_name=None, header=None).items():
        year = int(name)
        head = df.index[df.iloc[:, 0].astype(str) == "Day"][0]
        cols = list(df.iloc[head])
        for _, r in df.iloc[head + 1:].iterrows():
            day = int(r.iloc[0])
            for j, m in enumerate(MONTHS, start=1):
                v = r.iloc[cols.index(m)]
                if pd.notna(v):
                    out[dt.date(year, j, day)] = float(v)
    return out


def probe_daily(path):
    df = pd.read_csv(path, dtype={"station_no": str})
    df = df[(df["element"] == "TMAX") & (df["quality"] == "A")].drop_duplicates()
    assert not df["obs_date"].duplicated().any(), "one approved maximum a day"
    return {dt.date.fromisoformat(d): float(v) for d, v in zip(df["obs_date"], df["value"])}


def terms(path):
    t = pdf_text(path)
    m = re.search(r"\$([\d.,]+) for each heat day after the period's first (\d+), plus \$([\d.,]+) for each severe "
                  r"heat day, up to \$([\d.,]+) a hectare", t)
    hr, ded, sr, cap = (float(x.replace(",", "")) for x in m.groups())
    return ded, hr, sr, cap


def main_call(target):
    f = lambda n: os.path.join(target, n)
    stations = json.load(open(f("ncs_station_list_merrin_district.json")))
    old = next(s for s in stations["stations"] if s["name"].startswith("Merrin Flat (Research"))
    change = dt.date.fromisoformat(old["closed"]) + dt.timedelta(days=1)
    glass = glass_register(f("ncs_climatological_register_041207_1964_1995.xlsx"))
    probe = probe_daily(f("ncs_daily_041391_19951101_20270827.csv"))
    par = pd.read_csv(f("ncs_parallel_observations_maxtemp.csv"), dtype={"site_no": str})
    par["diff"] = par["max_probe_small_shield"] - par["max_glass_large_screen"]
    table = par.groupby("max_glass_large_screen")["diff"].mean()
    xs, ys = table.index.values.astype(float), table.values.astype(float)

    def basis(d):
        if d >= change:
            return probe[d]
        g = glass[d]
        return g + float(np.interp(g, xs, ys))

    seasons = list(range(1965, 2027))
    heat, severe, raw_heat = {}, {}, {}
    for s in seasons:
        d0 = dt.date(s, 12, 1)
        days = [d0 + dt.timedelta(k) for k in range((dt.date(s + 1, 3, 1) - d0).days)]
        vals = [basis(d) for d in days]
        raw = [probe[d] if d >= change else glass[d] for d in days]
        heat[s] = sum(v >= 35.0 - 1e-9 for v in vals)
        severe[s] = sum(v >= 40.0 - 1e-9 for v in vals)
        raw_heat[s] = sum(v >= 35.0 - 1e-9 for v in raw)
    ded, hr, sr, cap = terms(f("heat_cover_term_sheet_2027_28_quote.pdf"))
    x = np.array(seasons, float)
    bh, ah = np.polyfit(x, [heat[s] for s in seasons], 1)
    bs, as_ = np.polyfit(x, [severe[s] for s in seasons], 1)
    pays = []
    for s in seasons:
        h = max(0.0, heat[s] + bh * (2027 - s))
        v = max(0.0, severe[s] + bs * (2027 - s))
        pays.append(min(cap, hr * max(0.0, h - ded) + sr * v))
    burn = float(np.mean(pays))
    return {"premium": half_up(burn * 1.32), "heat": ah + bh * 2027, "severe": as_ + bs * 2027,
            "slope_heat": 10 * bh, "conv": dict(zip(xs, ys)),
            "added_heat": sum(heat[s] - raw_heat[s] for s in seasons if s < change.year)}


def ask_a(target, rate):
    f = lambda n: os.path.join(target, n)
    sch = pd.read_csv(f("policy_schedule_HC104_merrin_valley_2027-08-26.csv"), dtype=str, keep_default_na=False)
    on = "2027-12-01"
    live = sch[(sch["inception"] <= on) & ((sch["cancelled_from"] == "") | (sch["cancelled_from"] > on))]
    blocks = live.drop_duplicates(["grower_ref", "block_no"])[["grower_ref", "block_no", "insured_ha"]].copy()
    blocks["member"] = blocks["grower_ref"].str.replace("MV-", "", regex=False).astype(int)
    blocks["block"] = blocks["block_no"].astype(int)
    blocks["ha"] = blocks["insured_ha"].astype(float)
    reg = pd.read_excel(f("merrin_valley_block_register_2027-08.xlsx"), header=3)
    sd = reg.drop_duplicates(["Member no", "Block"]).set_index(["Member no", "Block"])["Sub-district"]
    blocks["sd"] = [sd[(m, b)] for m, b in zip(blocks["member"], blocks["block"])]
    out = {}
    for name, g in blocks.groupby("sd"):
        ha = round(float(g["ha"].sum()), 1)
        out[name] = {"blocks": int(len(g)), "ha": ha, "premium": half_up(rate * ha)}
    return out


def ask_b(target):
    f = lambda n: os.path.join(target, n)
    reg = pd.read_csv(f("claims_register_heat_cover_2020_2027.csv"))
    season = reg.drop_duplicates("claim_no").set_index("claim_no")["season"]
    led = pd.read_csv(f("gl6120_weather_claims_payments_FY2020_FY2028.csv"))
    paid = led.groupby("reference")["amount"].sum()
    df = pd.DataFrame({"season": [season[c] for c in paid.index], "amount": paid.values})
    out = {}
    for s, g in df.groupby("season"):
        out[s] = {"claims": int(len(g)), "amount": half_up(float(g["amount"].sum()))}
    return out


def main(target, golden):
    fig = json.load(open(os.path.join(TASK, "generator", "figures.json")))
    mc = main_call(target)
    bad = []

    def eq(a, b, what):
        if a != b:
            bad.append("%s: verifier %r, figures %r" % (what, a, b))
    eq(mc["premium"], fig["call_premium_per_ha"], "premium")
    eq("%.1f" % mc["heat"], fig["expected_heat_days_2027_28"], "expected heat days")
    eq("%.1f" % mc["severe"], fig["expected_severe_days_2027_28"], "expected severe days")
    eq("%.2f" % mc["slope_heat"], fig["heat_line_slope_days_per_decade"], "heat line slope")
    eq(mc["added_heat"], fig["glass_era_heat_days_added"], "glass-era heat days added")
    eq("%.2f" % mc["conv"][34.5], fig["conversion_at_34_5"], "conversion at 34.5")
    a = ask_a(target, mc["premium"])
    eq(a, fig["sub_districts"], "sub-districts")
    b = ask_b(target)
    eq(b, fig["seasons"], "seasons")
    gp = pd.read_csv(os.path.join(golden, "heat_cover_payouts.csv"), dtype={"season": str})
    eq({r.season: {"claims": int(r.claims_paid), "amount": int(r.paid_dollars)} for r in gp.itertuples()}, b,
       "payouts csv")
    q = pdf_text(os.path.join(golden, "heat_cover_quote_2027_28.pdf"))
    for token in ["$%d a hectare" % mc["premium"], fig["expected_heat_days_2027_28"] + " heat days",
                  fig["expected_severe_days_2027_28"] + " severe heat days"] + \
                 ["${:,}".format(v["premium"]) for v in a.values()] + ["%.1f" % v["ha"] for v in a.values()]:
        if token not in q:
            bad.append("quote lacks %r" % token)
    if bad:
        print("verify FAILED:\n  " + "\n  ".join(bad))
        sys.exit(1)
    print("verify: premium $%d a hectare, %s heat days, %s severe days; %d sub-districts and %d seasons recomputed "
          "from target/ and matched in both goldens" % (mc["premium"], fig["expected_heat_days_2027_28"],
                                                         fig["expected_severe_days_2027_28"], len(a), len(b)))


if __name__ == "__main__":
    main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
