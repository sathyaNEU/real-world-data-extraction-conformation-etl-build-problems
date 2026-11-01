"""task445 architecture 3: an independent recomputation of every graded figure from target/ with pandas, against
generator/figures.json (no import of golden.py)."""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
FIG = json.load(open(os.path.join(HERE, "figures.json")))
BAD = []


def same(name, a, b):
    good = a == b
    print("%s  %-46s %s" % ("PASS" if good else "FAIL", name, a if good else "%s != %s" % (a, b)))
    if not good:
        BAD.append(name)


m = pd.read_csv(os.path.join(T, "p2_essay_marks_2026.csv"), dtype=str)
cen = pd.read_csv(os.path.join(T, "aeb_centres_register.csv"), dtype=str).fillna("")
sa = pd.read_csv(os.path.join(T, "p2_section_a_scan_2026.csv"), dtype={"candidate_no": str})
region = dict(zip(cen.centre_code, cen.region_code))
region.update({o: r for o, r in zip(cen.merged_from, cen.region_code) if o})
tz = dict(zip(cen.centre_code, cen.time_zone))
tz.update({o: z for o, z in zip(cen.merged_from, cen.time_zone) if o})
ent = pd.read_excel(os.path.join(T, "asc_history_entries_2026.xlsx"), sheet_name="Entries", dtype=str)
cur = ent[ent["Entry status"] == "ENTERED"]
later = dict(zip(cur["Previous candidate number"].dropna(), cur.loc[cur["Previous candidate number"].notna(),
                                                                       "Candidate number"]))
entered = dict(zip(cur["Candidate number"], cur["Centre"]))
m["candidate_no"] = m["candidate_no"].map(lambda c: later.get(c, c))
live = m[m.script_status == "MARKED"].copy()
live["rank"] = (live.marking_event == "SENIOR").astype(int)
live = live.sort_values(["candidate_no", "question", "rank", "marked_utc"]).drop_duplicates(
    ["candidate_no", "question"], keep="last")
live["mark"] = live["mark"].astype(int)
wide = live.pivot(index="candidate_no", columns="question", values="mark")
three = wide.dropna()
dem = {}
for q, a, b in (("B4", "B5", "B6"), ("B5", "B4", "B6"), ("B6", "B4", "B5")):
    dem[q[1]] = float(((three[a] + three[b]) / 2 - three[q]).mean())
same("demand to one decimal", {q: "%.1f" % v for q, v in dem.items()}, FIG["demand_1dp"])
raise6 = int(np.floor(dem["6"] + 0.5)) if dem["6"] >= 1.5 else 0
same("Question 6 raise (marks)", raise6, FIG["call"]["raise_marks"])
same("candidates who wrote all three", int(len(three)), FIG["all_three_candidates"])
absent = set(m.loc[m.script_status == "ABSENT", "candidate_no"])
sitting = sorted((set(wide.index) | set(sa.candidate_no)) - absent)
wide = wide.reindex(sitting)
w2 = wide.copy()
w2["B6"] = (w2["B6"] + raise6).clip(upper=25)
best = w2.apply(lambda r: sum(sorted([v for v in r.values if not np.isnan(v)], reverse=True)[:2]), axis=1)
tot = best + sa.set_index("candidate_no")["section_a_total"].reindex(best.index).fillna(0)
cuts = [("A", 66), ("B", 57), ("C", 48), ("D", 39), ("E", 30)]
gr = tot.apply(lambda x: next((g for g, b in cuts if x >= b), "U"))
same("grades after scaling", {g: int((gr == g).sum()) for g in "ABCDEU"}, FIG["grades"])
best0 = wide.apply(lambda r: sum(sorted([v for v in r.values if not np.isnan(v)], reverse=True)[:2]), axis=1)
gr0 = (best0 + sa.set_index("candidate_no")["section_a_total"].reindex(best0.index).fillna(0)).apply(
    lambda x: next((g for g, b in cuts if x >= b), "U"))
same("grades changed by the scaling", int((gr != gr0).sum()), FIG["grade_changed"])
same("candidates graded", int(len(gr)), FIG["candidates_graded"])
reg = pd.Series({c: region[entered[c]] for c in wide.index})
ask_a = {}
for r in ["NT", "QT", "WA", "PC", "ID", "MS"]:
    sub = wide[reg == r]
    ask_a[r] = {"sat": int(len(sub)), "q4": int(sub["B4"].notna().sum()), "q5": int(sub["B5"].notna().sum()),
                "q6": int(sub["B6"].notna().sum())}
same("ask A, by region", ask_a, FIG["ask_a"])
print("verify: %d failures" % len(BAD))
sys.exit(1 if BAD else 0)
