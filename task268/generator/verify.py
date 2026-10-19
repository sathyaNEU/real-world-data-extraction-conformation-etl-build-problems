"""Independent verifier for task268. Reads only the shipped bundle (target/) and the goldens, on its own code path
(pandas, no generator module), and recomputes the cohort, the deaths from both sources, every end of follow-up, the
Kaplan-Meier figure the default path files, the golden's weighted estimate, the call and the gap, and both asks; then
reads the goldens back and compares. Exit 0 when everything agrees.

    python3 verify.py <target> <golden>"""
import datetime as dt
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

T, G = sys.argv[1], sys.argv[2]
fails = []


def check(cond, label):
    print(("ok    " if cond else "FAIL  ") + label)
    if not cond:
        fails.append(label)


def half_up(x):
    return int(np.floor(x + 0.5))


f = lambda name: os.path.join(T, name)
pat = pd.read_csv(f("hf_registry_patients.csv"), dtype=str)
vis = pd.read_csv(f("hf_registry_visits_2022_2026.csv"), dtype=str)
ev = pd.read_csv(f("hf_registry_followup_events.csv"), dtype=str, keep_default_na=False)
xw = pd.read_csv(f("mrn_crosswalk_2024.csv"), dtype=str)
fl = pd.read_excel(f("fl_death_linkage_2022_2025.xlsx"), sheet_name="Linked deaths", dtype={"MRN": str})
ex = pd.read_csv(f("tristate_exchange_deaths_2022_2025.txt"), sep="|", dtype=str)
lab = pd.read_csv(f("ntprobnp_results_2025.csv"), dtype=str)
hosp = pd.read_excel(f("hospital_reference.xlsx"), sheet_name="Hospitals")
check(len(fl) > 1000 and len(ex) > 50 and len(hosp) == 6, "every format reads back: csv, pipe-delimited text, xlsx")

# the hospital of each code, from the reference (a campus belongs to its hospital)
code2hosp = dict(zip(hosp["Code"], hosp["Hospital"]))
names = sorted(set(code2hosp.values()))
check(len(names) == 5, "five hospitals in the reference")


def nyha(s):
    m = re.search(r"(IV|III|II|I|[1-4])\s*$", str(s).strip())
    return {"I": 1, "II": 2, "III": 3, "IV": 4, "1": 1, "2": 2, "3": 3, "4": 4}[m.group(1)]


# ---------------------------------------------------------------------------------------------- the cohort
pat["dx"] = pd.to_datetime(pat["diagnosis_date"])
coh = pat[(pat["dx"] >= "2022-01-01") & (pat["dx"] <= "2023-12-31")].copy()
coh["hospital_name"] = coh["hospital"].map(code2hosp)
leg = dict(zip(xw["legacy_mrn"], xw["new_mrn"]))
coh["new_mrn"] = coh["mrn"].map(lambda m: leg.get(m, m))
fl["dod"] = pd.to_datetime(fl["Date of death"])
fl_first = fl.groupby("MRN")["dod"].min()
ex["dod"] = pd.to_datetime(ex["DOD"], format="%Y%m%d")
ex_first = ex.groupby("PARTNER_ID")["dod"].min()
coh["death"] = pd.concat([coh["new_mrn"].map(fl_first), coh["registry_id"].map(ex_first)], axis=1).min(axis=1)
ev["date"] = pd.to_datetime(ev["event_date"])
lost = ev[((ev["event"] == "REL") & ~ev["destination_state"].isin(["GA", "AL", "SC"])) | (ev["event"] == "CNR")]
first_loss = lost.sort_values("date").groupby("registry_id").first()
coh["end"] = coh["registry_id"].map(first_loss["date"])
coh["why"] = coh["registry_id"].map(first_loss["event"])
coh["two"] = coh["dx"].map(lambda d: pd.Timestamp(d.year + 2, d.month, d.day))
dead = coh["death"].notna() & (coh["death"] <= coh["two"]) & (coh["end"].isna() | (coh["death"] <= coh["end"]))
cens = ~dead & coh["end"].notna() & (coh["end"] < coh["two"])
coh["E"] = dead.astype(int)
coh["T"] = np.where(dead, (coh["death"] - coh["dx"]).dt.days,
                    np.where(cens, (coh["end"] - coh["dx"]).dt.days, (coh["two"] - coh["dx"]).dt.days))
coh["north"] = cens & (coh["why"] == "REL")
check(coh["T"].max() <= 731 and (coh["two"] <= pd.Timestamp("2025-12-31")).all(),
      "every two-year date falls inside the death sources' completeness")
vis["date"] = pd.to_datetime(vis["visit_date"])
vis["cls"] = vis["nyha_class"].map(nyha)
v = vis.merge(coh[["registry_id", "dx", "T", "north", "hospital_name"]], on="registry_id")
v["d"] = (v["date"] - v["dx"]).dt.days
v = v[(v["d"] > 0) & (v["d"] <= v["T"])].copy()
v["move"] = v["north"] & (v["d"] == v["T"])


def km(df, w_at=None):
    """Product-limit survival at each patient's two-year date (the curve's value after the last day at risk);
    w_at(ids, t) gives each patient's weight in force on day t."""
    S = 1.0
    deaths = df[df["E"] == 1]
    for t in sorted(deaths["T"].unique()):
        risk = df[df["T"] >= t]
        dd = deaths[deaths["T"] == t]
        if w_at is None:
            n, d = len(risk), len(dd)
        else:
            n, d = w_at(risk, t).sum(), w_at(dd, t).sum()
        S *= 1 - d / n
    return S


def ipcw_weights(df_h, v_h):
    """The chance of a move beyond the linkage at a visit, by the class recorded there, from this hospital's visits;
    each patient's weight on day t is the product of 1 / (1 - chance) over the visits before t."""
    rate = v_h.groupby("cls")["move"].mean().clip(upper=0.9)
    vv = v_h.assign(f=1.0 / (1.0 - v_h["cls"].map(rate)))
    by = {rid: (g["d"].to_numpy(), np.cumprod(g.sort_values("d")["f"].to_numpy()))
          for rid, g in vv.sort_values("d").groupby("registry_id")}

    def w_at(rows, t):
        out = []
        for rid in rows["registry_id"]:
            if rid not in by:
                out.append(1.0)
                continue
            d, cp = by[rid]
            k = np.searchsorted(d, t, side="left")
            out.append(cp[k - 1] if k > 0 else 1.0)
        return np.array(out)
    return w_at


surv, kms = {}, {}
for h in names:
    df = coh[coh["hospital_name"] == h]
    kms[h] = km(df)
    surv[h] = km(df, ipcw_weights(df, v[v["hospital_name"] == h]))
order = sorted(names, key=lambda h: surv[h])
pick, runner = order[0], order[1]
gap = 100 * (surv[runner] - surv[pick])
km_pick = min(names, key=lambda h: kms[h])
print("  survival:", ", ".join("%s %.2f" % (h, 100 * surv[h]) for h in order), "| gap %.2f" % gap)
print("  Kaplan-Meier:", ", ".join("%s %.2f" % (h, 100 * kms[h]) for h in sorted(names, key=lambda h: kms[h])))
check(pick == "Gullhaven Hospital" and runner == "Fennick General Hospital", "the weighted estimate: Gullhaven lowest, "
                                                                              "Fennick next")
check(km_pick == "Fennick General Hospital", "the default path (Kaplan-Meier, the moves as ordinary censoring) files "
                                             "Fennick")
km_order = sorted(names, key=lambda h: kms[h])
check(half_up(100 * (kms[km_order[1]] - kms[km_order[0]])) != half_up(gap),
      "the default path's gap prints a different whole point from the golden's")
moved = coh[coh["north"] & (coh["hospital_name"] == pick)]
last_cls = v[v["move"]].set_index("registry_id")["cls"]
hi = (moved["registry_id"].map(last_cls) >= 3).mean()
check(hi > 0.85, "Gullhaven's movers beyond the linkage: %.0f%% in class III or IV at the move" % (100 * hi))

# ---------------------------------------------------------------------------------------------- the asks
lab["rel"] = pd.to_datetime(lab["released"])
l5 = lab[lab["rel"].dt.year == 2025].sort_values("rel")
l5 = l5.drop_duplicates(["performing_lab", "mrn", "collected"], keep="last")
num = l5["result"].map(lambda s: 1e9 if s.startswith(">") else (-1.0 if s.startswith("<") else float(s)))
lab_name = {c: code2hosp[c] for c in ["FEN", "LIN", "BRE", "GUL", "WRE"]}
ask_a = {lab_name[c]: (int((l5["performing_lab"] == c).sum()), int(((l5["performing_lab"] == c) & (num >= 400)).sum()))
         for c in lab_name}
pat["new_mrn"] = pat["mrn"].map(lambda m: leg.get(m, m))
# a diagnosis cannot follow its own enrolment: where the record shows it after, it came on or before the enrolment
pat["eff"] = pat[["dx"]].assign(en=pd.to_datetime(pat["enrolment_date"])).min(axis=1)
first_dx = pat.groupby("new_mrn")["eff"].min()
p5 = pat[pat["eff"].dt.year == 2025]
p5 = p5[p5["new_mrn"].map(first_dx) >= p5["eff"]]
p5 = p5.assign(h=p5["hospital"].map(code2hosp))
ask_b = {h: (int((p5["h"] == h).sum()), int(((p5["h"] == h) & p5["diagnosis_setting"].isin(["Inpatient", "INPT", "IP"]))
                                            .sum())) for h in names}

# ---------------------------------------------------------------------------------------------- the goldens
wb = pd.read_excel(os.path.join(G, "hf_programme_site_2027.xlsx"), sheet_name=None, header=None)
sv = wb["Survival"]
rows = {r[0]: r for r in sv.itertuples(index=False) if r[0] in names}
check(all(int(rows[h][5]) == half_up(100 * surv[h]) for h in names), "the workbook's survival, every hospital")
check(str(sv.iloc[4, 0]) == pick, "the workbook leads with the pick")
rec = " ".join(str(x) for x in sv[0].tolist() if isinstance(x, str) and x.startswith("Recommendation"))
check(("%d points below" % half_up(gap)) in rec and pick in rec, "the recommendation states the pick and the gap")
for sheet, ask in (("Laboratory", ask_a), ("New diagnoses 2025", ask_b)):
    t = {r[0]: (int(r[1]), int(r[2])) for r in wb[sheet].itertuples(index=False) if r[0] in names}
    check(t == ask, "the workbook's %s sheet, every hospital and figure" % sheet)
from pptx import Presentation  # noqa: E402
deck = Presentation(os.path.join(G, "service_line_committee_hf_2027.pptx"))
text = " ".join(sh.text_frame.text for s in deck.slides for sh in s.shapes if sh.has_text_frame)
check(("Host the 2027 programme at %s" % pick) in text and ("%d points below" % half_up(gap)) in text,
      "the deck states the call and the gap")
ch = [sh.chart for s in deck.slides for sh in s.shapes if sh.has_chart][0]
vals = list(ch.plots[0].series[0].values)
cats = list(ch.plots[0].categories)
check(vals == [half_up(100 * surv[h]) for h in order] and len(cats) == 5, "the deck's chart: five hospitals' survival "
                                                                         "in order")
txt = subprocess.run(["pdftotext", "-layout", f("hf_early_diagnosis_programme_charter_2027.pdf"), "-"],
                     capture_output=True, text=True).stdout
txt = " ".join(txt.split())
check("including patients the registry no longer follows" in txt and "lowest two-year survival from diagnosis" in txt,
      "the charter reads back: the estimand, every patient counted")
man = " ".join(subprocess.run(["pdftotext", "-layout", f("hf_registry_manual_v5.pdf"), "-"], capture_output=True,
                              text=True).stdout.split())
check("The registry has no source for deaths in any other state" in man, "the manual reads back: the linkage's reach")
cont = open(f("pack_contents.txt"), encoding="utf-8").read()
check(all(n in cont for n in os.listdir(T) if n != "pack_contents.txt"), "the contents list names every file")
print("verify: %d failures" % len(fails))
sys.exit(1 if fails else 0)
