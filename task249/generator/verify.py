"""An independent recomputation of every owed figure from target/ alone, by other routes than solve.py: the flags
with an additive baseline and each recognised item's time from the first-time candidates' mean seconds scaled by
the candidate's own ratio; ask A from the sitting whose clock was running on each failed workstation and the invigilators' power-cut report;
ask B from each workstation's link state walked through the event log in time order.
python3 verify.py [target]   exit 1 on any difference from generator/figures.json"""
import datetime as dt
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
FILES = {"export3": "results_export_r3_2026-02_to_2027-05.csv", "export4": "results_export_r4_2027-08_to_2027-11.csv",
         "layouts": "form_layouts_2026_2027.csv", "bank": "item_bank_snapshot_2027-12-31.xlsx",
         "crosswalk": "item_renumbering_2027-01-11.csv", "register": "candidate_number_changes.csv",
         "events": "workstation_event_log_2027.csv", "incidents": "invigilator_incident_reports_2027.xlsx",
         "seat": "seat_plan_2027.csv",
         "panel_log": "item_panel_decision_log.csv"}
WIN = ["2026-02", "2026-05", "2026-08", "2026-11", "2027-02", "2027-05", "2027-08", "2027-11"]


def main(target):
    p = lambda k: os.path.join(target, FILES[k])
    a = pd.read_csv(p("export3"), dtype=str, keep_default_na=False)
    b = pd.read_csv(p("export4"), dtype=str, keep_default_na=False)
    rows = []
    for r in a.itertuples(index=False):
        rows.append((r.candidate_no, r.booking_ref, r.window, r.sitting_date, r.form, r.responses,
                     [float(v) if v else np.nan for v in r.item_seconds.split("|")], int(r.score)))
    for r in b.itertuples(index=False):
        d = dt.datetime.strptime(r.sat_on, "%d-%m-%Y").date().isoformat()
        rows.append((r.cand_no, r.booking_ref, r.exam_window, d, r.form_code, r.response_string,
                     [float(v) / 1000 if v else np.nan for v in r.latency_ms.split("|")], int(r.raw_score)))
    reg = pd.read_csv(p("register"), dtype=str)
    prev = dict(zip(reg["candidate_no"], reg["previous_candidate_no"]))

    def root(n):
        while n in prev:
            n = prev[n]
        return n
    cw = dict(pd.read_csv(p("crosswalk"), dtype=str)[["previous_item_id", "item_id"]].itertuples(index=False))
    lay = pd.read_csv(p("layouts"), dtype=str)
    lay["position"] = lay["position"].astype(int)
    lay = lay.sort_values(["window", "form", "position"])
    items = {k: [cw.get(i, i) for i in g["item_id"]] for k, g in lay.groupby(["window", "form"])}
    scored = {k: (g["slot"] == "scored").to_numpy() for k, g in lay.groupby(["window", "form"])}
    bank = pd.read_excel(p("bank"), dtype=str)
    key, model, area, status = (dict(zip(bank["item_id"], bank[c])) for c in ("key", "item_model", "content_area", "status"))
    sit = []
    for cand, bk, win, d, form, resp, secs, raw in rows:
        its = items[(win, form)]
        rc = np.array([c != "-" for c in resp])
        x = np.array([c == key[i] for c, i in zip(resp, its)]) & rc
        sit.append(dict(pid=root(cand), bk=bk, w=WIN.index(win), d=d, form=form, its=its, sc=scored[(win, form)], rc=rc,
                        x=x.astype(float), secs=np.array(secs)))
    hist = {}
    for s in sorted(sit, key=lambda s: (s["w"], s["d"])):
        hist.setdefault(s["pid"], []).append(s)
    first = [h[0] for h in hist.values()]
    pv, ls = {}, {}
    for s in first:
        if s["w"] < 4:
            continue
        for i, xv, r_, t in zip(s["its"], s["x"], s["rc"], s["secs"]):
            if r_:
                pv.setdefault((s["w"], i), []).append(xv)
                ls.setdefault((s["w"], i), []).append(np.log(t))
    pv = {k: np.mean(v) for k, v in pv.items()}
    mu = {k: np.mean(v) for k, v in ls.items()}
    gains = {}
    for h in hist.values():
        for n, s in enumerate(h):
            if s["w"] < 4 or n == 0:
                continue
            seen, seenm = set(), set()
            for e in h[:n]:
                for i, r_ in zip(e["its"], e["rc"]):
                    if r_:
                        seen.add(i); seenm.add(model[i])
            ex = np.array([i in seen or model[i] in seenm for i in s["its"]])
            ep = np.array([pv.get((s["w"], i), np.nan) for i in s["its"]])
            m = np.array([mu.get((s["w"], i), np.nan) for i in s["its"]])
            ok = ~np.isnan(ep)
            base = s["sc"] & ok & s["rc"] & ~ex
            shift = s["x"][base].mean() - ep[base].mean()
            tb = s["rc"] & ~ex & ~np.isnan(m)
            ratio = np.log(s["secs"][tb]) - m[tb]
            t_cf = np.where(s["rc"] & ex & ~np.isnan(m), np.exp(m + ratio.mean() + ratio.var() / 2), np.where(s["rc"], s["secs"], 0))
            within = s["rc"] & (np.cumsum(np.where(s["rc"], t_cf, 0)) <= 4 * 3600)
            reach = (s["x"] * (s["rc"] & ~within) * s["sc"]).sum()
            e = s["sc"] & ok & within & ex
            direct = (s["x"][e] - np.clip(ep[e] + shift, 0, 1)).sum()
            gains.setdefault(s["form"], []).append(direct + reach)
    gain = {f: float(np.mean(v)) for f, v in gains.items() if f.startswith("CC27")}
    flags = sorted(f for f, g in gain.items() if g > 1.0)
    # ask A: a sitting a failure interrupted either carries a WS_FAIL or was resumed on a spare workstation, except the
    # changes of seat a candidate asked for; the power cut's sittings from the invigilators' report
    ev = pd.read_csv(p("events"), dtype=str, keep_default_na=False)
    ev["t"] = pd.to_datetime(ev["event_utc"])
    seat = pd.read_csv(p("seat"), dtype=str)
    where = {(r.centre_code, r.session_date, r.session, r.workstation): r.booking_ref for r in seat.itertuples()}
    rep = pd.read_excel(p("incidents"), sheet_name=None, dtype=str, keep_default_na=False)
    codes = {"Kochi": "COK", "Chennai": "MAA", "Bengaluru": "BLR", "Hyderabad": "HYD", "Pune": "PNQ", "Noida": "NOI"}
    asked, cut_sittings = set(), set()
    for centre, df in rep.items():
        for r in df.itertuples(index=False):
            d = dt.datetime.strptime(r.Date, "%d/%m/%Y").date()
            if "asked to move" in str(r.Report):
                # the spare and the resume time the report names; the typed workstation number can be wrong
                sp = [w for w in str(r.Report).replace(",", " ").replace("(", " ").replace(")", " ").split() if w.startswith("SP")]
                hm = [w.strip(".") for w in str(r.Report).split() if len(w.strip(".")) == 5 and w.strip(".")[2] == ":"]
                asked.add((codes[centre], d.isoformat(), sp[0].strip(".,"), hm[-1]))
            if "Power cut" in str(r.Report):
                h_, m_ = map(int, r.Time.split(":"))
                cut = pd.Timestamp(dt.datetime(d.year, d.month, d.day, h_, m_)) - pd.Timedelta(minutes=330)
                day = ev[(ev["centre_code"] == codes[centre]) & (ev["t"].dt.date == cut.date())]
                st = day[day["event"] == "SESSION_START"].set_index("booking_ref")["t"]
                en = day[day["event"] == "SESSION_END"].set_index("booking_ref")["t"]
                cut_sittings |= {k for k, t0 in st.items() if t0 <= cut < en.get(k, cut)}
    sp_rows = ev[(ev["event"] == "SESSION_RESUME") & ev["workstation"].str.match(r"SP\d")]
    on_spare = set()
    for r in sp_rows.itertuples(index=False):
        loc = r.t + pd.Timedelta(minutes=330)
        if (r.centre_code, loc.date().isoformat(), r.workstation, loc.strftime("%H:%M")) not in asked:
            on_spare.add(r.booking_ref)
    hit = set(ev[ev["event"] == "WS_FAIL"]["booking_ref"]) | on_spare | cut_sittings
    form_of = {s["bk"]: s["form"] for s in sit if s["w"] >= 4}
    ask_a = {f: 0 for f in sorted(gain)}
    for k in hit:
        if k in form_of:
            ask_a[form_of[k]] += 1
    # ask B: walk each workstation's events in time order; a client logs in at its tutorial or at a resume on that
    # workstation, and its link is down from a NET_LOST, or from the login when a NET_BACK comes with no NET_LOST before
    # it, to the NET_BACK, or to the sitting's end; a sitting counts when that overlaps its clock
    clock_of = {}
    for r in ev[ev["event"].isin(["SESSION_START", "SESSION_END"])].itertuples(index=False):
        lo, hi = clock_of.get(r.booking_ref, (None, None))
        if r.event == "SESSION_START":
            lo = r.t if lo is None else min(lo, r.t)
        else:
            hi = r.t if hi is None else max(hi, r.t)
        clock_of[r.booking_ref] = (lo, hi)
    off = set(cut_sittings)
    walk = ev[ev["event"].isin(["TUTORIAL_START", "SESSION_RESUME", "NET_LOST", "NET_BACK"])].sort_values("t")
    for (cc, ws), g in walk.groupby(["centre_code", "workstation"]):
        state = {}
        for r in g.itertuples(index=False):
            b = r.booking_ref
            lo, hi = clock_of.get(b, (None, None))
            if lo is None:
                continue
            if r.event in ("TUTORIAL_START", "SESSION_RESUME"):
                state.setdefault(b, {"login": r.t, "down": None})
                continue
            stt = state.setdefault(b, {"login": lo, "down": None})
            if r.event == "NET_LOST":
                if stt["down"] is None:
                    stt["down"] = r.t
            else:
                a = stt["down"] if stt["down"] is not None else stt["login"]
                if max(lo, a) < min(hi, r.t):
                    off.add(b)
                stt["down"] = None
        for b, stt in state.items():
            lo, hi = clock_of[b]
            if stt["down"] is not None and max(lo, stt["down"]) < hi:
                off.add(b)
    ask_b = {f: 0 for f in sorted(gain)}
    for k in off:
        if k in form_of:
            ask_b[form_of[k]] += 1
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []
    if flags != fig["call"]["flagged"]:
        bad.append("flags %s against %s" % (flags, fig["call"]["flagged"]))
    for f, g in gain.items():
        if abs(g - fig["call"]["gain"][f]) > 0.15:
            bad.append("%s gain %.2f against %.2f" % (f, g, fig["call"]["gain"][f]))
    if ask_a != fig["asks"]["interrupted"]:
        bad.append("ask A %s against %s" % (ask_a, fig["asks"]["interrupted"]))
    if ask_b != fig["asks"]["offline"]:
        bad.append("ask B %s against %s" % (ask_b, fig["asks"]["offline"]))
    print("verify: flags %s; %s" % (", ".join(flags), "agree" if not bad else "; ".join(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")))
