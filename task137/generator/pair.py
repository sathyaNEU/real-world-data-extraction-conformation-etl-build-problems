"""The cracker and the mirror run on the cut pack, scored figure by figure against figures.json, and the pair ceiling
on the weights of supplemental-stumping Part 0 (38 for the call and its components, 7 for instruction-following, 55
for the asks).

The cracker lands the call and, on the asks, does what the pack's filed sentences and the hygiene battery do: it reads
the remand files' times as UK times and filters to charges in 2025-26, joins each file to its linked arrest (every key
matches), runs the reverse unmatched join and attaches each remanded arrest without a file that was arrested in the same
minute, ward and offence group as a file's arrest to that file, on the file's times; it merges an episode's assessment
lines that abut at a shift handover, and counts each line at the suite its row names.
The mirror misses the call and stops one sweep earlier on each ask: the remand files as they stand, each at its linked
arrest, and the assessment lines merged the same way.

    python3 pair.py [target_dir]
"""
import datetime as dt
import json
import os
import sys
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
UK = ZoneInfo("Europe/London")
SUITES = ["Northgate", "Eastmoor", "Southfields", "Wendle Cross"]
W_CALL, W_IF, W_ASK, R_MISS = 38.0, 7.0, 55.0, 5.0


def load(tgt):
    names = os.listdir(tgt)
    pick = lambda pre: os.path.join(tgt, [n for n in names if n.startswith(pre)][0])
    a = pd.read_csv(pick("calderwick_police_arrests"))
    a["book"] = pd.to_datetime(a.booked_in_utc, utc=True)
    hm = a.detention_hhmm.str.split(":", expand=True).astype(int)
    a["charge"] = a.book + pd.to_timedelta(hm[0] * 60 + hm[1], unit="m")
    c = pd.read_csv(pick("cju_remand_files"))
    for col in ("charged", "handed_to_escort"):
        c[col + "_t"] = pd.to_datetime(c[col], format="%d/%m/%Y %H:%M").dt.tz_localize(UK, ambiguous=True).dt.tz_convert("UTC")
    h = pd.read_csv(pick("custody_healthcare_contacts"))
    h["start"], h["end"] = pd.to_datetime(h.started), pd.to_datetime(h.ended)
    return a, c, h


def fy(ts):
    t = ts.dt.tz_convert(UK)
    return np.where(t.dt.month >= 4, t.dt.year, t.dt.year - 1)


def ask_a_routes(a, c):
    rem = a[a.outcome == "Charged - remanded in custody"]
    c = c[fy(c.charged_t) == 2025]
    j = c.merge(a[["arrest_ref", "book", "arrested_utc", "ward", "offence_group"]], left_on="linked_arrest",
                right_on="arrest_ref", how="left")
    assert j.arrest_ref.notna().all()
    mirror = j.assign(hours=(j.handed_to_escort_t - j.charged_t).dt.total_seconds() / 3600,
                      over=(j.handed_to_escort_t - j.book).dt.total_seconds() > 86400)
    # the reverse join: remanded arrests charged in 2025-26 that no file links
    orphan = rem[(fy(rem.charge) == 2025) & ~rem.arrest_ref.isin(set(c.linked_arrest))]
    co = orphan.merge(j[["urn", "custody_suite", "arrested_utc", "ward", "offence_group", "charged_t", "handed_to_escort_t"]],
                      on=["arrested_utc", "ward", "offence_group"], suffixes=("", "_file"))
    co = co.assign(hours=(co.handed_to_escort_t - co.charged_t).dt.total_seconds() / 3600,
                   over=(co.handed_to_escort_t - co.book).dt.total_seconds() > 86400)
    cracker = pd.concat([mirror[["custody_suite", "hours", "over"]],
                         co[["custody_suite_file", "hours", "over"]].rename(columns={"custody_suite_file": "custody_suite"})])
    out = {}
    for name, x in (("cracker", cracker), ("mirror", mirror)):
        g = x.groupby("custody_suite")
        out[name] = {}
        for s in SUITES:
            out[name]["ask_a.%s.cell_hours" % s] = int(round(g.hours.sum()[s]))
            out[name]["ask_a.%s.over_24_hours" % s] = int(g.over.sum()[s])
    out["orphans_left"] = int(len(orphan) - co.arrest_ref.nunique())
    return out


def ask_b_routes(h):
    iha = h[h.contact_type == "Initial health assessment"].sort_values(["episode_ref", "start"])
    prev = iha.groupby("episode_ref").end.shift()
    abut = (prev == iha.start) & iha.start.dt.minute.eq(0) & iha.start.dt.hour.isin([7, 19])
    kept = iha[~abut]
    sh = np.where((kept.start.dt.hour >= 7) & (kept.start.dt.hour < 19), "day", "night")
    g = kept.assign(sh=sh).groupby(["suite", "sh"]).size()
    f = {"ask_b.%s.%s" % (s, k): int(g.get((s, k), 0)) for s in SUITES for k in ("day", "night")}
    return {"cracker": f, "mirror": f}


def main(tgt):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    a, c, h = load(tgt)
    A, B = ask_a_routes(a, c), ask_b_routes(h)
    keys = [k for k in fig if k.startswith("ask_")]
    res = {}
    for who in ("cracker", "mirror"):
        got = dict(A[who], **B[who])
        hits = [k for k in keys if abs(got[k] - fig[k]) <= 0.5]
        res[who] = hits
        for k in keys:
            print("%-8s %-36s golden %6d  route %6d  %s" % (who, k, fig[k], got[k], "keep" if k in hits else "miss"))
    lc, ls = len(res["cracker"]) / len(keys), len(res["mirror"]) / len(keys)
    C = W_CALL + W_IF + W_ASK * lc
    S = R_MISS + W_IF + W_ASK * ls
    print("cracker keeps %d of %d ask figures; mirror keeps %d of %d; remanded arrests the cracker cannot place: %d"
          % (len(res["cracker"]), len(keys), len(res["mirror"]), len(keys), A["orphans_left"]))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f; mirror leakage %.1f per cent of ask weight"
          % (C, S, (C + S) / 2, 100 * ls))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
