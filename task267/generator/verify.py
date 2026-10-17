"""Independent verifier for task267: reads only the shipped bundle (and generator/figures.json to compare), on its own
code path (pandas, the rules parsed from the candidate rules file, the season read from the notes), and recomputes
the call, every rule's two shares, the rungs, and both asks.

    python3 task267/generator/verify.py task267/target"""
import json
import os
import re
import sys

import numpy as np
import pandas as pd
from pypdf import PdfReader

TGT = sys.argv[1]
FIG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
fails = []


def check(cond, label):
    if not cond:
        fails.append(label)


def text(name):
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(os.path.join(TGT, name)).pages))


# ---------------------------------------------------------------------------------------------- the adults screened
enc = pd.read_csv(os.path.join(TGT, "screening_encounters_2026.csv"), dtype=str)
enc = enc.drop_duplicates("encounter_id").sort_values(["screened_at", "encounter_id"])
adults = enc.drop_duplicates("program_id", keep="first").copy()
for c in ("risk_score", "glucose_mg_dl"):
    adults[c] = adults[c].astype(int)
adults["hba1c_pct"] = adults["hba1c_pct"].astype(float)
og = pd.read_csv(os.path.join(TGT, "ogtt_results_2026.txt"), sep="|", dtype=str)
og["key"] = og["PROGRAM_ID"].str.replace(r"\D", "", regex=True).astype(int).map(lambda d: "SF-%07d" % d)
done = og[og["STATUS"] == "COMPLETE"].copy()
done["dm"] = (done["GLU_FASTING_MGDL"].astype(int) >= 126) | (done["GLU_120MIN_MGDL"].astype(float) >= 200)
check(done["key"].is_unique, "one complete OGTT per adult")
adults = adults.merge(done[["key", "dm"]], left_on="program_id", right_on="key", how="left")
adults["tested"] = adults["key"].notna()
adults["dm"] = adults["dm"].fillna(False).astype(bool)
adults["grp"] = np.where(adults["ogtt_referral"] == "RULE", "referred", "not referred")
n_g = adults.groupby("grp").size()
t_g = adults[adults["tested"]].groupby("grp").size()
adults["w"] = np.where(adults["tested"], adults["grp"].map(n_g / t_g), 0.0)

# ---------------------------------------------------------------------------------------------- the candidate rules
rules = pd.read_excel(os.path.join(TGT, "candidate_referral_rules_2027.xlsx"), sheet_name="Candidates 2027")
rules = rules[rules["Rule ID"].notna()]
cols = {"SCORE": adults["risk_score"], "GLUCOSE": adults["glucose_mg_dl"], "HBA1C": adults["hba1c_pct"]}


def flagged(logic):
    out = pd.Series(False, index=adults.index)
    for term in logic.split(" OR "):
        var, op, val = term.split()
        assert op == ">="
        out |= cols[var] >= float(val)
    return out


pro = text("screening_referral_protocol_2026-27.pdf")
target = float(re.search(r"at least (\d+) of every 100 adults with undiagnosed diabetes", pro).group(1))
res = {}
for _, r in rules.iterrows():
    f = flagged(r["Tablet logic"])
    pos = adults["dm"] & adults["tested"]
    res[r["Rule"]] = dict(
        share=100 * f.mean(),
        golden=100 * (adults["w"] * (f & pos)).sum() / (adults["w"] * pos).sum(),
        cc=100 * (f & pos).sum() / pos.sum())


def choose(key):
    ok = [k for k, v in res.items() if v[key] >= target]
    return min(ok, key=lambda k: res[k]["share"]) if ok else "2026 rule"


check(choose("golden") == FIG["call"]["rule_name"], "the call: %s" % choose("golden"))
check(choose("cc") != FIG["call"]["rule_name"], "the default path lands elsewhere")
for k, v in res.items():
    check(round(v["golden"], 1) == FIG["call"]["sensitivity"][k], "sensitivity %s %.3f" % (k, v["golden"]))
    check(round(v["share"], 1) == FIG["call"]["referral_share"][k], "referral share %s %.3f" % (k, v["share"]))
    check(round(v["cc"], 1) == FIG["rungs"]["cc"][k], "complete-case share %s" % k)
check(len(adults) == FIG["counts"]["adults"] and int(adults["tested"].sum()) == FIG["counts"]["tested"], "counts")

# ---------------------------------------------------------------------------------------------- Ask A
notes = text("season_2026_extract_notes.pdf")
m = re.search(r"(\d+) March to (\d+) November 2026", notes)
start, end = pd.Timestamp(2026, 3, int(m.group(1))), pd.Timestamp(2026, 11, int(m.group(2)))
log = pd.read_csv(os.path.join(TGT, "gq200_run_log_2026.csv"), dtype=str, keep_default_na=False)
log["t"] = pd.to_datetime(log["run_started"])
keyf = ["serial_number", "run_type", "sample_id", "result_pct", "error_code", "cartridge_lot"]
copies = []
for h in (4, 5):
    shifted = log[keyf + ["t"]].copy()
    shifted["t"] = shifted["t"] + pd.Timedelta(hours=h)
    shifted["copy"] = True
    copies.append(log.merge(shifted, on=keyf + ["t"], how="left")["copy"].fillna(False).astype(bool).values)
log = log[~(copies[0] | copies[1])]
err = text("gq200_error_codes.pdf")
spent = set(re.findall(r"(E-\d\d) [^E]*?During the measurement", err))
check(len(spent) == 4, "four measurement-phase codes read (%s)" % sorted(spent))
log = log[(log["error_code"] == "") | log["error_code"].isin(spent)]
log = log[(log["t"].dt.normalize() >= start) & (log["t"].dt.normalize() <= end)]
reg = pd.read_excel(os.path.join(TGT, "analyzer_asset_register.xlsx"), sheet_name="Analyzers")
reg["to"] = reg["In service to"].fillna(pd.Timestamp(2099, 1, 1))
log["day"] = log["t"].dt.normalize()
mm = log.merge(reg, left_on="serial_number", right_on="Serial number")
mm = mm[(mm["day"] >= mm["In service from"]) & (mm["day"] <= mm["to"])]
check(len(mm) == len(log), "every run on exactly one tag")
cart = mm.groupby("Asset tag").size().to_dict()
for tag, v in FIG["ask_a"].items():
    check(cart.get(tag) == v, "Ask A %s: %s against %s" % (tag, cart.get(tag), v))

# ---------------------------------------------------------------------------------------------- Ask B
inv = pd.read_csv(os.path.join(TGT, "thessler_invoice_lines_2026.csv"), dtype=str, keep_default_na=False)
inv["cents"] = (inv["amount_usd"].astype(float) * 100).round().astype(int)
amt = inv.set_index(inv["document_number"] + " line " + inv["line"])["cents"]
inv["v"] = np.where(inv["document_type"] == "Invoice", inv["cents"], -inv["applies_to"].map(amt).fillna(0).astype(int))
check((inv.loc[inv["document_type"] != "Invoice", "applies_to"].isin(amt.index)).all(), "every credit resolves")
inv["month"] = pd.to_datetime(inv["service_date"]).dt.month
inv["year"] = pd.to_datetime(inv["service_date"]).dt.year
ours = set(og["ACCESSION"])
s = inv[(inv["year"] == 2026) & inv["month"].between(3, 11)]
names = ["March", "April", "May", "June", "July", "August", "September", "October", "November"]
for i, nm in enumerate(names):
    part = s[s["month"] == i + 3]
    tot = part["v"].sum() / 100
    scr = part[part["accession"].isin(ours)]["v"].sum() / 100
    check(abs(tot - FIG["ask_b"][nm]["billed"]) < .001, "Ask B %s billed %.2f" % (nm, tot))
    check(abs(scr - FIG["ask_b"][nm]["screened"]) < .001, "Ask B %s screened %.2f" % (nm, scr))

if fails:
    print("VERIFY FAILED:")
    for f in fails:
        print("  " + f)
    sys.exit(1)
print("verify: call, %d rules' shares, the rungs and %d ask figures recomputed from the bundle alone" %
      (len(res), len(FIG["ask_a"]) + 2 * len(FIG["ask_b"])))
