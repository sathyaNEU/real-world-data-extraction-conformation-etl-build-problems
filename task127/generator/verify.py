"""Independent verifier: reads only the shipped bundle, with pandas and none of the generator's code, and recomputes
the split, every hospital's bed-days, Ask A and Ask B."""
import os

import numpy as np
import pandas as pd

SITES = {"RMC01": "Royal Marchford Hospital", "RMC02": "Wendlebury Hospital", "RSM01": "Ashby Vale Hospital",
         "RSM02": "Cleeve Park Hospital", "RSM03": "Holmford Infirmary"}
DISTRICTS = ["Marchford", "Ashby", "Teme Valley"]
MONTHS = ["2025-12", "2026-01", "2026-02"]


def run(target):
    p = lambda f: os.path.join(target, f)
    sp = pd.read_csv(p("acute_discharges_65plus_2024-12_2026-09.csv"), dtype=str)
    sp = sp.sort_values("submission_id", key=lambda s: s.astype(int)).drop_duplicates(
        ["provider_code", "spell_number"], keep="last")
    sp["ready"] = pd.to_datetime(sp["discharge_ready_date"])
    sp["dis"] = pd.to_datetime(sp["discharge_datetime"]).dt.normalize()
    pr = pd.read_csv(p("gp_practices_2026-09.csv"), dtype=str)
    mp = set(pr.loc[pr["icb"].str.contains("Marchshire"), "practice_code"])
    cov = sp[(sp["discharge_pathway"] == "1") & (sp["p1_care_package"] == "New package")
             & sp["gp_practice_code"].isin(mp) & sp["site_code"].isin(SITES)
             & sp["ready"].between("2025-12-01", "2026-02-28")].copy()
    eq = pd.read_csv(p("ices_order_lines_2024-12_2026-09.csv"), dtype=str)
    eq = eq[eq["delivered_date"].notna()].copy()
    eq["nhs"] = eq["nhs_number"].str.replace(" ", "", regex=False)
    eq["delivered"] = pd.to_datetime(eq["delivered_date"])
    # every delivery to the patient between admission and discharge
    m = cov[["spell_number", "nhs_number", "admission_datetime", "ready", "dis"]].merge(
        eq[["nhs", "delivered"]], left_on="nhs_number", right_on="nhs", how="left")
    m = m[m["delivered"].notna() & (m["delivered"] >= pd.to_datetime(m["admission_datetime"]).dt.normalize())
          & (m["delivered"] <= m["dis"])]
    last = m.groupby("spell_number")["delivered"].max()
    cov["equip"] = cov["spell_number"].map(last)
    start = cov[["ready", "equip"]].max(axis=1)
    cov["saved"] = (cov["dis"] - start).dt.days.clip(lower=0)
    g = cov.groupby("site_code").agg(n=("saved", "size"), s=("saved", "sum"))
    g["v"] = g["s"] / g["n"]
    g = g.sort_values("v", ascending=False)
    left, pk = 1200, {}
    for site, row in g.iterrows():
        pk[site] = int(min(left, row["n"]))
        left -= pk[site]
    bed = {site: pk[site] * g.loc[site, "s"] / g.loc[site, "n"] for site in g.index}
    out = {"packages": {SITES[s]: pk[s] for s in SITES}, "bed": {SITES[s]: int(np.floor(bed[s] + 0.5)) for s in SITES},
           "total": int(np.floor(sum(bed.values()) + 0.5)), "covered": {SITES[s]: int(g.loc[s, "n"]) for s in SITES}}
    # Ask A: nights after the ready date by the site of the ward at the night's midnight and the evening's month
    ws = pd.read_csv(p("acute_ward_stays_2024-12_2026-09.csv"), dtype=str)
    wr = pd.read_csv(p("ward_reference.csv"), dtype=str).set_index("ward_code")["site_code"]
    ws["site"] = ws["ward_code"].map(wr)
    uk = ws["ward_start"].str.contains("/")
    ws["start"] = pd.NaT
    ws.loc[~uk, "start"] = pd.to_datetime(ws.loc[~uk, "ward_start"], format="%Y-%m-%d %H:%M")
    ws.loc[uk, "start"] = pd.to_datetime(ws.loc[uk, "ward_start"], format="%d/%m/%Y %H:%M")
    ws["start"] = pd.to_datetime(ws["start"]).astype("datetime64[ns]")
    nights = []
    a = sp[(sp["dis"] > pd.Timestamp("2025-12-01")) & (sp["ready"] <= pd.Timestamp("2026-02-28"))]
    for _, r in a.iterrows():
        for n in pd.date_range(r["ready"], r["dis"] - pd.Timedelta(days=1)):
            if pd.Timestamp("2025-12-01") <= n <= pd.Timestamp("2026-02-28"):
                nights.append((r["provider_code"], r["spell_number"], n))
    nt = pd.DataFrame(nights, columns=["provider_code", "spell_number", "night"])
    nt["midnight"] = (nt["night"] + pd.Timedelta(days=1)).astype("datetime64[ns]")
    ws_s = ws.sort_values("start")
    nt = nt.sort_values("midnight")
    nt = pd.merge_asof(nt, ws_s[["provider_code", "spell_number", "start", "site"]], left_on="midnight",
                       right_on="start", by=["provider_code", "spell_number"], direction="backward",
                       allow_exact_matches=False)
    nt["month"] = nt["night"].dt.strftime("%Y-%m")
    A = nt.groupby(["site", "month"]).size()
    out["A"] = {(SITES[s], mo): int(A.get((s, mo), 0)) for s in SITES for mo in MONTHS}
    nh = nt.merge(sp[["provider_code", "spell_number", "nhs_number"]], on=["provider_code", "spell_number"])
    AP = nh.groupby(["site", "month"])["nhs_number"].nunique()
    out["AP"] = {(SITES[s], mo): int(AP.get((s, mo), 0)) for s in SITES for mo in MONTHS}
    # Ask B: referrals received each month by care-address district, care started within seven days
    br = pd.read_csv(p("brokerage_referrals_2024-12_2026-09.csv"), dtype=str)
    pc = pd.read_csv(p("postcode_districts_marchshire.csv"), dtype=str).set_index("postcode")["district"]
    inv = pd.read_csv(p("spot_care_invoice_lines_2025-26.csv"), dtype=str)
    inv["ss"] = pd.to_datetime(inv["service_start"], format="%d/%m/%Y")
    inv["ref"] = "BR" + inv["brokerage_ref"].str[3:].astype(int).astype(str).str.zfill(6)
    spot = inv.groupby("ref")["ss"].min()
    br["recv"] = pd.to_datetime(br["received_at"]).dt.normalize()
    br["start"] = pd.to_datetime(br["start_date"]).fillna(br["referral_no"].map(spot))
    k = br["care_postcode"].str.strip().str.upper().str.replace(" ", "", regex=False)
    br["district"] = (k.str[:-3] + " " + k.str[-3:]).map(pc)
    br["month"] = br["recv"].dt.strftime("%Y-%m")
    br["in7"] = (br["start"] - br["recv"]).dt.days <= 7
    b = br[br["month"].isin(MONTHS) & br["district"].isin(DISTRICTS)]
    B = b[b["in7"]].groupby(["district", "month"]).size()
    out["B"] = {(dd, mo): int(B.get((dd, mo), 0)) for dd in DISTRICTS for mo in MONTHS}
    return out


def agree(v, F):
    import core
    M = F["M"]
    for s in core.SITES:
        n = core.HOSPITALS[s]["name"]
        assert v["packages"][n] == M["packages"][s], ("packages", s)
        assert v["bed"][n] == int(M["bed"][s] + 0.5), ("bed", s)
        assert v["covered"][n] == M["caps"][s], ("covered", s)
        for m in core.ASK_MONTHS:
            assert v["A"][(n, "%d-%02d" % m)] == F["A"][(s, m)], ("A", s, m)
            assert v["AP"][(n, "%d-%02d" % m)] == F["AP"][(s, m)], ("AP", s, m)
    assert v["total"] == int(M["total"] + 0.5), "total"
    for dist in core.DISTRICTS:
        for m in core.ASK_MONTHS:
            assert v["B"][(dist, "%d-%02d" % m)] == F["B"][(dist, m)], ("B", dist, m)
