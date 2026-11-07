"""task286 independent verifier: reads only the shipped bundle (target/ or target.zip) and recomputes the call,
every critical component and every ask figure on its own code path, then compares with generator/figures.json.
No generator module is imported. Exit 1 on any mismatch."""
import io
import json
import os
import re
import sys
import zipfile
from datetime import date, datetime

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
WIN0, WIN1 = date(2025, 9, 29), date(2026, 9, 27)
ASOF = date(2026, 9, 27)
CUT = date(2026, 3, 27)
MARGIN = 50
OUT = []


def ok(label, cond, detail=""):
    OUT.append((label, bool(cond), detail))


def bundle():
    """the files as a solver receives them: from target.zip when it exists, else target/."""
    zp = os.path.join(TASK, "target.zip")
    files = {}
    if os.path.exists(zp):
        with zipfile.ZipFile(zp) as z:
            for n in z.namelist():
                files[os.path.basename(n)] = z.read(n)
    else:
        t = os.path.join(TASK, "target")
        for n in os.listdir(t):
            files[n] = open(os.path.join(t, n), "rb").read()
    return files


B = bundle()
figs = json.load(open(os.path.join(HERE, "figures.json")))

# ----------------------------------------------------------------------------------------- the main call
meter = pq.read_table(io.BytesIO(B["meter_reads_daily_2025-26.parquet"])).to_pandas()
ok("V1 the meter file reads back with its five columns", list(meter.columns) == [
    "PROPERTY_REF", "METER_SERIAL", "READ_DATE_UTC", "CONSUMPTION_L", "READ_TYPE"], str(len(meter)))
meter["READ_DATE_UTC"] = pd.to_datetime(meter["READ_DATE_UTC"]).dt.date
day = meter.groupby(["PROPERTY_REF", "READ_DATE_UTC"], as_index=False)["CONSUMPTION_L"].sum()
day = day[(day["READ_DATE_UTC"] >= WIN0) & (day["READ_DATE_UTC"] <= WIN1)].copy()
day["WEEK"] = day["READ_DATE_UTC"].map(lambda d: (d - WIN0).days // 7)
wk = day.groupby(["PROPERTY_REF", "WEEK"])["CONSUMPTION_L"].agg(["max", "min", "count"]).reset_index()
ok("V2 every property has seven meter days in each of the 52 weeks", (wk["count"] == 7).all() and
   wk.groupby("PROPERTY_REF")["WEEK"].nunique().eq(52).all())
wk["quiet"] = (wk["max"] - wk["min"]) <= MARGIN
empty_weeks = wk.groupby("PROPERTY_REF")["quiet"].sum()
match = pd.read_csv(io.BytesIO(B["pw_property_uprn_match_2026-10.csv"]), dtype=str)
gaz = pd.read_csv(io.BytesIO(B["county_gazetteer_extract_2026-10.csv"]), dtype=str)
area_by_uprn = dict(zip(gaz["UPRN"], gaz["COMMUNITY_AREA"]))
dw = gaz[gaz["CLASS"].str.startswith("RD")]
pc_area = dw.groupby("POSTCODE_LOCATOR")["COMMUNITY_AREA"].agg(lambda s: sorted(set(s)))
ok("V3 every dwelling postcode lies in one community area", pc_area.map(len).eq(1).all())
pc_area = pc_area.map(lambda x: x[0]).to_dict()


def area_of(row):
    if isinstance(row["UPRN"], str) and row["UPRN"]:
        return area_by_uprn[row["UPRN"]]
    return pc_area[row["POSTCODE"]]


match["AREA"] = match.apply(area_of, axis=1)
prop_area = dict(zip(match["PROPERTY_REF"], match["AREA"]))
res = pd.DataFrame({"empty": empty_weeks})
res["area"] = res.index.map(prop_area)
left = res[res["empty"] >= 26]
counts = left.groupby("area").size().to_dict()
areas = sorted(figs["areas"])
ok("V4 each area's homes left empty for 26 or more weeks recompute", all(
    counts.get(a, 0) == figs["areas"][a]["left_empty"] for a in areas),
   str({a: (counts.get(a, 0), figs["areas"][a]["left_empty"]) for a in areas}))
bands = {a: [int(((left["area"] == a) & (left["empty"] <= 38)).sum()),
             int(((left["area"] == a) & (left["empty"] >= 39) & (left["empty"] <= 51)).sum()),
             int(((left["area"] == a) & (left["empty"] == 52)).sum())] for a in areas}
ok("V5 the week bands recompute", all(bands[a] == [figs["areas"][a]["w26_38"], figs["areas"][a]["w39_51"],
                                                   figs["areas"][a]["w52"]] for a in areas))
rank = sorted(areas, key=lambda a: -counts.get(a, 0))
ok("V6 the call, runner-up and gap recompute", rank[0] == figs["call"] and rank[1] == figs["runner_up"]
   and counts[rank[0]] - counts[rank[1]] == figs["gap"], "%s %s %d" % (rank[0], rank[1],
                                                                        counts[rank[0]] - counts[rank[1]]))
homes_n = dw.groupby("COMMUNITY_AREA").size().to_dict()
ok("V7 homes per area on the gazetteer recompute", all(homes_n[a] == figs["areas"][a]["homes"] for a in areas))
# the margin corridor and the easy route from the bundle alone
alt = {}
for m in (30, 70):
    q = wk.assign(q=(wk["max"] - wk["min"]) <= m).groupby("PROPERTY_REF")["q"].sum()
    alt[m] = pd.DataFrame({"e": q, "a": q.index.map(prop_area)}).query("e >= 26").groupby("a").size().to_dict()
ok("V8 margins of 30 and 70 litres file the same counts", alt[30] == counts and alt[70] == counts)
tot = day.groupby(["PROPERTY_REF", "WEEK"])["CONSUMPTION_L"].sum().reset_index()
void = tot.assign(v=tot["CONSUMPTION_L"] < 300).groupby("PROPERTY_REF")["v"].sum()
vc = pd.DataFrame({"e": void, "a": void.index.map(prop_area)}).query("e >= 26").groupby("a").size()
ok("V9 the default path (void weeks under 300 litres) names Ellingsea", vc.idxmax() == "Ellingsea",
   str(vc.sort_values(ascending=False).head(3).to_dict()))

# --------------------------------------------------------------------------------------- ask 1: the CTB count
def parse_d(s):
    if not isinstance(s, str) or not s:
        return None
    if "/" in s:
        return datetime.strptime(s, "%d/%m/%Y").date()
    return date.fromisoformat(s[:10])


sbc = pd.read_csv(io.BytesIO(B["swanholt_ctax_extract_2026-10-06.csv"]), dtype=str, keep_default_na=False)
leg = pd.read_csv(io.BytesIO(B["teversby_ctax_legacy_archive_to_2026-05-04.csv"]), dtype=str,
                  keep_default_na=False)
from openpyxl import load_workbook
wb = load_workbook(io.BytesIO(B["teversby_ctax_extract_2026-10-05.xlsx"]), read_only=True)
rows = list(wb["Liabilities"].iter_rows(values_only=True))
new = pd.DataFrame(rows[1:], columns=rows[0])
ok("V10 the three council tax extracts read back", len(sbc) > 0 and len(leg) > 0 and len(new) > 0,
   "%d %d %d" % (len(sbc), len(leg), len(new)))
for c in ("Liability From", "Liability To"):
    new[c] = pd.Series([x.date() if isinstance(x, datetime) else None for x in new[c]], index=new.index,
                       dtype=object)
for c in ("FROM_DATE", "TO_DATE"):
    leg[c] = leg[c].map(parse_d)
for c in ("LIAB_START", "LIAB_END"):
    sbc[c] = sbc[c].map(parse_d)


def covers(s, e, d):
    return s <= d and (e is None or pd.isna(e) or d <= e)


def spell_start(periods, idx, is_unf):
    """walk back from period idx over consecutive periods that are unoccupied and unfurnished."""
    j = idx
    while j > 0 and is_unf(periods[j - 1]) and not pd.isna(periods[j - 1][1]) and \
            (periods[j][0] - periods[j - 1][1]).days == 1:
        j -= 1
    return periods[j][0]


lte = {a: 0 for a in areas}
# Swanholt: one system, every liability on the property
for pref, g in sbc.groupby("PROPERTY_REF"):
    per = sorted([(r.LIAB_START, r.LIAB_END, r.OCC_STATUS) for r in g.itertuples()], key=lambda x: x[0])
    cur = [k for k, p in enumerate(per) if covers(p[0], p[1], ASOF)]
    if not cur or per[cur[0]][2] != "UNOCC UNFURNISHED":
        continue
    if spell_start(per, cur[0], lambda p: p[2] == "UNOCC UNFURNISHED") < CUT:
        lte[area_by_uprn[g["UPRN"].iloc[0]]] += 1
# Teversby: the legacy archive's periods by VO reference, then the new system's
leg_by_vo = {}
for r in leg.itertuples():
    leg_by_vo.setdefault(r.VO_REF, []).append((r.FROM_DATE, r.TO_DATE, r.STATUS, r.ACC_NO))
leg_acc = {r.ACC_NO: r.STATUS for r in leg.itertuples()}
for pid, g in new.groupby("Property ID"):
    per = []
    for r in g.itertuples():
        la = r._8 if isinstance(r._8, str) and r._8.strip() else ""
        if la:      # Legacy Account: carried across at go-live, furnishing from the archive
            unf = leg_acc[la] == "UNOCCUPIED UNFURNISHED"
        else:
            unf = r.Occupation == "Unoccupied" and r.Furnished == "N"
        per.append((r._9, r._10, unf, la))
    per.sort(key=lambda x: x[0])
    cur = [k for k, p in enumerate(per) if covers(p[0], p[1], ASOF)]
    if not cur or not per[cur[0]][2]:
        continue
    j = cur[0]
    while j > 0 and per[j - 1][2] and not pd.isna(per[j - 1][1]) and (per[j][0] - per[j - 1][1]).days == 1:
        j -= 1
    start = per[j][0]
    if per[j][3]:     # a carried account: its empty spell runs back through the archive on the same dwelling
        vo = g["Valuation List Ref"].iloc[0]
        lp = sorted(leg_by_vo[vo], key=lambda x: x[0])
        k = [i for i, p in enumerate(lp) if p[3] == per[j][3]][0]
        start = spell_start(lp, k, lambda p: p[2] == "UNOCCUPIED UNFURNISHED")
    if start < CUT:
        lte[area_by_uprn[str(g["UPRN"].iloc[0])]] += 1
ok("V11 the long-term empty homes (CTB basis, 27 September 2026) recompute", all(
    lte[a] == figs["areas"][a]["lte_ctb"] for a in areas), str({a: (lte[a], figs["areas"][a]["lte_ctb"])
                                                                for a in areas}))

# ------------------------------------------------------------------------------- ask 2: self-catering homes
ndr = pd.read_csv(io.BytesIO(B["ndr_self_catering_entries_2026-10.csv"]), dtype=str, keep_default_na=False)
ndr["F"] = ndr["EFFECTIVE_FROM"].map(parse_d)
ndr["T"] = ndr["EFFECTIVE_TO"].map(parse_d)
live = ndr[ndr.apply(lambda r: covers(r["F"], r["T"], ASOF), axis=1)]
xref = gaz[gaz["NDR_XREF"].fillna("") != ""]
by_ref = dict(zip(xref["NDR_XREF"], xref["UPRN"]))
kids = gaz[gaz["PARENT_UPRN"].fillna("") != ""].groupby("PARENT_UPRN").size().to_dict()
cls = dict(zip(gaz["UPRN"], gaz["CLASS"]))
lets = {a: 0 for a in areas}
for r in live.itertuples():
    u = by_ref[r.BA_REFERENCE]
    lets[area_by_uprn[u]] += kids[u] if cls[u] == "PP" else 1
ok("V12 the homes on the business rates list as self-catering lets recompute", all(
    lets[a] == figs["areas"][a]["holiday_let_homes"] for a in areas), str(lets))

# ------------------------------------------------------------------------------------- documents read back
from pypdf import PdfReader


def text(name):
    return " ".join(p.extract_text() for p in PdfReader(io.BytesIO(B[name])).pages)


tor = text("homes_in_use_pilot_terms_of_reference_v1-2.pdf")
ok("V13 the terms of reference read back (positive control) and file the WHAT",
   len(tor) > 2000 and "at least 26 of the 52 weeks" in re.sub(r"\s+", " ", tor)
   and "on any day of it" in re.sub(r"\s+", " ", tor))
ctb = re.sub(r"\s+", " ", text("council_taxbase_returns_october_2025.pdf"))
ok("V14 the Council Taxbase returns read back and define a long-term empty home",
   "unoccupied and substantially unfurnished for more than six months" in ctb)
hna = re.sub(r"\s+", " ", text("housing_needs_assessment_2024_summary.pdf"))
cen = pd.read_csv(io.BytesIO(B["census2021_household_spaces_oa.csv"]))
lkp = pd.read_csv(io.BytesIO(B["oa21_to_community_area_bestfit.csv"]))
cc = cen.merge(lkp, left_on="geography code", right_on="OA21CD").groupby("CA_NAME")[
    ["Household spaces: All household spaces", "Household spaces: No usual residents"]].sum()
okh = all(("%s" % "{:,}".format(int(r["Household spaces: No usual residents"]))) in hna for _, r in cc.iterrows())
ok("V15 the housing needs assessment's table agrees with the census file through the lookup", okh)
dsa = re.sub(r"\s+", " ", text("pennimouth_water_data_sharing_agreement_PW-DSA-2026-014.pdf"))
ok("V16 the data sharing agreement reads back", "1 September 2025 to 4 October 2026" in dsa)
for n, t in (("tor", tor), ("ctb", ctb), ("hna", hna), ("dsa", dsa)):
    ok("V17 no document mentions a leak or a steady flow (%s)" % n, not re.search(
        r"\bleak|steady flow|continuous flow|running cistern|constant flow", t, re.I))

fails = [o for o in OUT if not o[1]]
for label, good, detail in OUT:
    print("%s  %s%s" % ("PASS" if good else "FAIL", label, ("  [" + detail + "]") if detail and not good else ""))
print("verify: %d checks, %d failed" % (len(OUT), len(fails)))
sys.exit(1 if fails else 0)
