"""An independent recomputation of every graded figure from the cut pack, written apart from bundle.py (pandas, its
own PDF reading), compared with generator/figures.json.

    python3 task479/generator/verify.py [target]"""
import json
import os
import re
import sys

import numpy as np
import pandas as pd
import pypdf

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def dept(target):
    rows = []
    for y in range(2018, 2025):
        reader = pypdf.PdfReader(os.path.join(target, "tdor_taxable_lodging_receipts_ty%d.pdf" % y))
        toks = [t.strip() for t in "\n".join(p.extract_text() for p in reader.pages).splitlines() if t.strip()]
        k = 1000 if any("thousands of dollars" in t for t in toks) else 1
        for i, t in enumerate(toks):
            if re.fullmatch(r"[A-Z][a-z]+( [A-Z][a-z]+)?", t) and t != "State" and re.fullmatch(r"[\d,]+", toks[i + 1]):
                nums = [int(v.replace(",", "")) for v in toks[i + 1:i + 6] if re.fullmatch(r"[\d,]+", v)]
                cur = nums[0] if k == 1000 else nums[1]
                rows.append((t, y, cur * k))
    return pd.DataFrame(rows, columns=["county", "year", "first"])


def monitor(target):
    leg = pd.read_csv(os.path.join(target, "tla_monitor_reports_2018-01_to_2022-03.csv"))
    leg["when"] = pd.to_datetime(leg["Received"], format="%m/%d/%Y %H:%M")
    leg = leg.sort_values("when").drop_duplicates(["Property ID", "Report Month"], keep="last")
    leg["year"] = leg["Report Month"].str[-4:].astype(int)
    leg["county"] = leg["County"].str.title()
    leg["rev"] = leg["Room Revenue"]
    cur = pd.read_csv(os.path.join(target, "tla_monitor_reports_2022-04_to_2026-09.csv"), dtype={"county_code": str})
    cur = cur.sort_values("submitted_at_utc").drop_duplicates(["prop_id", "period"], keep="last")
    reg = pd.read_csv(os.path.join(target, "tla_monitor_properties_2026-10-02.csv"))
    cur = cur.merge(reg[["prop_id", "county", "rooms"]], on="prop_id", how="left")
    cur["year"] = cur["period"].str[:4].astype(int)
    cur["month"] = cur["period"].str[5:].astype(int)
    cur["rev"] = cur["room_revenue_cents"] / 100
    return leg, cur, reg


def main(target=None, gdir=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    d = dept(target)
    leg, cur, reg = monitor(target)
    pan = pd.concat([leg[["county", "year", "rev"]], cur[["county", "year", "rev"]]])
    pan = pan[pan.year <= 2025].groupby(["county", "year"]).rev.sum()
    bad = 0
    q = []
    for c, g in d.groupby("county"):
        g = g.set_index("year")["first"]
        r = np.array([g[y] / pan[(c, y)] for y in range(2018, 2025)])
        k, a = np.polyfit(np.arange(2018, 2025), r, 1)
        gr = (a + k * 2025) * pan[(c, 2025)] / g[2024] - 1
        if gr >= 0.06:
            q.append(c)
        bad += int(round(100 * gr)) != fig["growth_pct"][c]
    bad += sorted(q) != fig["call"]["qualifying"]
    a = cur[(cur.year == 2026) & (cur.month <= 8)].groupby("county")[["avail_room_nights", "sold_room_nights", "rev"]].sum()
    for c, r in a.iterrows():
        bad += "%.1f" % (100 * r.sold_room_nights / r.avail_room_nights) != fig["ask_a"][c]["occupancy_pct"]
        bad += "%.2f" % (r.rev / r.sold_room_nights) != fig["ask_a"][c]["adr_usd"]
    # ask B: crosswalk, then the unmapped March 2022 legacy property to the unmapped April 2022 InnSight one with the
    # same county and rooms
    xw = pd.read_csv(os.path.join(target, "innsight_property_id_crosswalk_2022-04.csv"))
    link = dict(zip(xw.legacy_property_id, xw.innsight_prop_id))
    mar = leg[leg["Report Month"] == "03/2022"]
    apr = cur[cur.period == "2022-04"]
    for _, r in mar[~mar["Property ID"].isin(link)].iterrows():
        cand = apr[(~apr.prop_id.isin(set(link.values()))) & (apr.county == r.county) &
                   (apr.avail_room_nights // 30 == r["Rooms Available"] // 31)]
        if len(cand) == 1:
            link[r["Property ID"]] = cand.prop_id.iloc[0]
    aug = cur[cur.period == "2026-08"].set_index("prop_id").avail_room_nights / 31
    j18 = leg[leg["Report Month"] == "01/2018"].copy()
    j18["rooms"] = j18["Rooms Available"] / 31
    j18["new"] = j18["Property ID"].map(link)
    j18["still"] = j18["new"].isin(aug.index)
    j18["aug"] = j18["new"].map(aug)
    for c, g in j18.groupby("county"):
        s = g[g.still]
        bad += "%.1f" % (100 * s.rooms.sum() / g.rooms.sum()) != fig["ask_b"][c]["rooms_share_pct"]
        bad += "%.1f" % (100 * (s.aug.sum() / s.rooms.sum() - 1)) != fig["ask_b"][c]["rooms_change_pct"]
    print("verify: %d figures differ from figures.json" % bad)
    return bad == 0


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else None) else 1)
