"""task286 pair ceiling, measured on the cut pack (target.zip): two responses scored on 38 (call and critical
components), 7 (instructions) and 55 (asks, sixteen figures). The cracker lands the call and handles the asks
the careful way (Teversby's Legacy Account link followed to its one legacy account, consecutive accounts merged
within each system, rating list entries joined through the gazetteer cross-reference and counted per entry,
deleted entries dropped). The mirror stops at the void read for the call and handles the asks the same careful
way, the worst honest case for it. Prints the pair and the mirror's share of the ask weight."""
import io
import json
import os
import sys
import zipfile
from datetime import date, datetime

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ASOF, CUT, GO = date(2026, 9, 27), date(2026, 3, 27), date(2026, 5, 5)
figs = json.load(open(os.path.join(HERE, "figures.json")))
areas = sorted(figs["areas"])
with zipfile.ZipFile(os.path.join(TASK, "target.zip")) as z:
    B = {os.path.basename(n): z.read(n) for n in z.namelist()}
gaz = pd.read_csv(io.BytesIO(B["county_gazetteer_extract_2026-10.csv"]), dtype=str, keep_default_na=False)
area_by_uprn = dict(zip(gaz["UPRN"], gaz["COMMUNITY_AREA"]))


def d(s):
    if not s:
        return None
    return datetime.strptime(s, "%d/%m/%Y").date() if "/" in s else date.fromisoformat(s[:10])


def covers(s, e, x):
    return s <= x and (e is None or x <= e)


# ---------------------------------------------------------------- ask 1 the careful way that stops one short
sbc = pd.read_csv(io.BytesIO(B["swanholt_ctax_extract_2026-10-06.csv"]), dtype=str, keep_default_na=False)
leg = pd.read_csv(io.BytesIO(B["teversby_ctax_legacy_archive_to_2026-05-04.csv"]), dtype=str, keep_default_na=False)
from openpyxl import load_workbook
rows = list(load_workbook(io.BytesIO(B["teversby_ctax_extract_2026-10-05.xlsx"]), read_only=True)[
    "Liabilities"].iter_rows(values_only=True))
new = [dict(zip(rows[0], r)) for r in rows[1:]]
lte_c = {a: 0 for a in areas}
for pref, g in sbc.groupby("PROPERTY_REF"):
    per = sorted([(d(r.LIAB_START), d(r.LIAB_END), r.OCC_STATUS) for r in g.itertuples()], key=lambda x: x[0])
    cur = [k for k, p in enumerate(per) if covers(p[0], p[1], ASOF)]
    if not cur or per[cur[0]][2] != "UNOCC UNFURNISHED":
        continue
    j = cur[0]
    while j > 0 and per[j - 1][2] == "UNOCC UNFURNISHED" and per[j - 1][1] and (per[j][0] - per[j - 1][1]).days == 1:
        j -= 1
    if per[j][0] < CUT:
        lte_c[area_by_uprn[g["UPRN"].iloc[0]]] += 1
leg_acc = {r.ACC_NO: (d(r.FROM_DATE), r.STATUS) for r in leg.itertuples()}
by_pid = {}
for r in new:
    by_pid.setdefault(r["Property ID"], []).append(r)
for pid, g in by_pid.items():
    per = []
    for r in g:
        la = r["Legacy Account"] or ""
        s = r["Liability From"].date()
        e = r["Liability To"].date() if r["Liability To"] else None
        unf = (leg_acc[la][1] == "UNOCCUPIED UNFURNISHED") if la else (r["Occupation"] == "Unoccupied" and
                                                                       r["Furnished"] == "N")
        per.append((s, e, unf, la))
    per.sort(key=lambda x: x[0])
    cur = [k for k, p in enumerate(per) if covers(p[0], p[1], ASOF)]
    if not cur or not per[cur[0]][2]:
        continue
    j = cur[0]
    while j > 0 and per[j - 1][2] and per[j - 1][1] and (per[j][0] - per[j - 1][1]).days == 1:
        j -= 1
    start = leg_acc[per[j][3]][0] if per[j][3] else per[j][0]      # the linked legacy account's own start
    if start < CUT:
        lte_c[area_by_uprn[str(g[0]["UPRN"])]] += 1

# ---------------------------------------------------------------- ask 2 counted per list entry
ndr = pd.read_csv(io.BytesIO(B["ndr_self_catering_entries_2026-10.csv"]), dtype=str, keep_default_na=False)
xref = dict(zip(gaz.loc[gaz["NDR_XREF"] != "", "NDR_XREF"], gaz.loc[gaz["NDR_XREF"] != "", "UPRN"]))
lets_c = {a: 0 for a in areas}
for r in ndr.itertuples():
    if covers(d(r.EFFECTIVE_FROM), d(r.EFFECTIVE_TO), ASOF):
        lets_c[area_by_uprn[xref[r.BA_REFERENCE]]] += 1

kept = sum(lte_c[a] == figs["areas"][a]["lte_ctb"] for a in areas) + \
    sum(lets_c[a] == figs["areas"][a]["holiday_let_homes"] for a in areas)
n_ask = 2 * len(areas)
L = kept / n_ask
cracker = 38 + 7 + 55 * L
mirror = 5 + 7 + 55 * L
pair = (cracker + mirror) / 2
print("cracker ask figures kept: %d of %d (long-term empty %d of 8, self-catering %d of 8)" % (
    kept, n_ask, sum(lte_c[a] == figs["areas"][a]["lte_ctb"] for a in areas),
    sum(lets_c[a] == figs["areas"][a]["holiday_let_homes"] for a in areas)))
print("cracker %.1f, mirror %.1f, pair %.1f; mirror keeps %.1f per cent of the ask weight" % (
    cracker, mirror, pair, 100 * L))
sys.exit(0 if pair <= 60 and L < 0.5 else 1)
