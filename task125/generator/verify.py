"""task125 independent verifier: recomputes the designation and every ask figure from target/ with pandas, by its
own route (cell means for the venue excess, merges for the asks), and compares with figures.json.

    python3 task125/generator/verify.py
"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
PATROL = {"1610", "1420", "1430", "2120", "2142", "2170", "3370"}


def t(path):
    return os.path.join(TARGET, path)


def when(s):
    s = s.fillna("")
    day_first = s.str.contains("/")
    out = pd.Series(pd.NaT, index=s.index)
    out[day_first] = pd.to_datetime(s[day_first], format="%d/%m/%Y %H:%M")
    rest = (~day_first) & (s != "")
    out[rest] = pd.to_datetime(s[rest].str[:16], format="%Y-%m-%d %H:%M")
    return out


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    occ = pd.read_csv(t("mps_rms_occurrences_2022_2026.csv"), dtype=str)
    occ["version"] = occ["version"].astype(int)
    last = occ.sort_values(["occurrence_no", "version"]).groupby("occurrence_no").tail(1).copy()
    xw = pd.read_csv(t("rms_offence_code_crosswalk_2023.csv"), dtype=str)
    m = dict(zip(xw.legacy_code, xw.ucr2_code))
    last["code"] = last["offence_code"].map(lambda c: m.get(c, c))
    when_ = when(last["occurred_from"])
    when_ = when_.fillna(when(last["reported"]))
    last["date"] = when_.dt.normalize()
    keep = last[last.code.isin(PATROL) & (last.status != "UNFOUNDED") & last.segment_id.notna() &
                (last.date >= "2022-01-01") & (last.date <= "2026-12-31")].copy()
    segs = pd.read_csv(t("mountjoy_street_segments.csv"), dtype={"segment_id": int})
    keep["segment_id"] = keep.segment_id.astype(int)
    keep = keep[keep.segment_id.isin(segs.segment_id)]
    daily = keep.groupby(["segment_id", "date"]).size()

    xl = pd.read_excel(t("mps_paid_duty_register_2022_2027.xlsx"), sheet_name=None, dtype=str)
    nights = {"G": set(), "L": set()}
    mar = {2026: 0, 2027: 0}
    for name, df in xl.items():
        df.columns = [c.lower().replace(" ", "_") for c in df.columns]
        dcol = "duty_date"
        loc = df["location"].fillna("")
        ev = df[df.category == "EVENT"]
        for _, r in ev.drop_duplicates("booking_no").iterrows():
            d = pd.Timestamp(r[dcol][:10]) if "-" in r[dcol] else pd.to_datetime(r[dcol], format="%d/%m/%Y")
            l = r["location"]
            v = "G" if ("GARDENS" in l) else ("L" if "LAKESHORE" in l else None)
            if v is None:
                continue
            if str(r["status"]).startswith("CANC"):
                continue
            nights[v].add(d)
            if r["client"] == "MOUNTJOY MARINERS HOCKEY CLUB" and d.year in mar:
                mar[d.year] += 1
    days = pd.date_range("2022-01-01", "2026-12-31")
    g = pd.Series(days.isin(list(nights["G"])), index=days)
    l = pd.Series(days.isin(list(nights["L"])), index=days)
    seg_ids = sorted(segs.segment_id)
    mat = daily.unstack(fill_value=0).reindex(index=seg_ids, columns=days, fill_value=0)
    none = (~g) & (~l)
    only_g = g & ~l
    only_l = l & ~g
    base = mat.loc[:, none.values].mean(axis=1)
    ex_g = mat.loc[:, only_g.values].mean(axis=1) - base
    ex_l = mat.loc[:, only_l.values].mean(axis=1) - base
    g26 = sum(1 for d in nights["G"] if d.year == 2026)
    l26 = sum(1 for d in nights["L"] if d.year == 2026)
    exp = base * 365 + ex_g * (g26 - mar[2026]) + ex_l * (l26 + mar[2026])
    top = sorted(exp.sort_values(ascending=False).index[:20].tolist())
    ok = top == fig["designated"]
    fails = [0 if ok else 1]
    print("%s  designation recomputed by cell means (%s)" % ("PASS" if ok else "FAIL", "same 20" if ok else top))

    # asks
    cad = pd.read_csv(t("mps_cad_calls_2026.csv"), dtype=str)
    for c in ("received_utc", "dispatched_utc", "onscene_utc", "cleared_utc"):
        cad[c] = pd.to_datetime(cad[c], format="%Y-%m-%dT%H:%M:%SZ", utc=True).dt.tz_convert("America/Toronto")
    cad = cad[(cad.source != "OFFICER") & (cad.received_utc.dt.year == 2026)]
    cad["segment_id"] = pd.to_numeric(cad.segment_id)
    cad = cad.merge(segs[["segment_id", "ward"]], on="segment_id", how="inner")
    ros = pd.read_csv(t("mps_patrol_roster_2026.csv"), dtype=str)
    ros["crew"] = 1 + ros.officer_2.notna().astype(int)
    u = cad[cad.unit.notna()].copy()
    loc = u.dispatched_utc.dt.tz_localize(None)
    hour = loc.dt.hour
    u["tour"] = np.where((hour >= 7) & (hour < 19), "D", "N")
    tour_day = loc.dt.normalize() - pd.to_timedelta((hour < 7).astype(int), unit="D")
    u["tour_date"] = tour_day.dt.strftime("%Y-%m-%d")
    u = u.merge(ros[["tour_date", "tour", "unit", "crew"]], on=["tour_date", "tour", "unit"], how="left")
    u["oh"] = (u.cleared_utc - u.dispatched_utc).dt.total_seconds() / 3600 * u.crew
    u["q"] = u.received_utc.dt.quarter
    oh = u.groupby(["ward", "q"]).oh.sum()
    bad = 0
    for k, v in fig["ask_officer_hours"].items():
        w, q = k.split()
        got = int(np.floor(oh[(int(w), int(q[1]))] + 0.5))
        bad += got != v
    fails.append(bad)
    print("%s  ask A recomputed (%d of 32 differ)" % ("PASS" if not bad else "FAIL", bad))
    return 0 if not any(fails) else 1


if __name__ == "__main__":
    sys.exit(main())
