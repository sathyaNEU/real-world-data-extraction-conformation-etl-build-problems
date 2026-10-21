"""An independent recomputation of every owed figure from target/ alone, by other routes than solve.py: the flags
with an additive baseline and each recognised item's time from the first-time candidates' mean seconds scaled by
the candidate's own ratio; ask A from each sitting's own events in order (a failure it stopped after, a restart before it
resumed in place), the reported failures by spare and minute and the power-cut report; ask B from each workstation's link
state walked through the event log in time order, kept where another client logged the loss and the clock was running.
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
    # the event log walked centre by centre in time order, each sitting's own events kept in order
    ev = pd.read_csv(p("events"), dtype=str, keep_default_na=False)
    ev["t"] = pd.to_datetime(ev["event_utc"])
    ev = ev.sort_values(["t", "event"], kind="stable")
    rep = pd.read_excel(p("incidents"), sheet_name=None, dtype=str, keep_default_na=False)
    codes = {"Kochi": "COK", "Chennai": "MAA", "Bengaluru": "BLR", "Hyderabad": "HYD", "Pune": "PNQ", "Noida": "NOI"}
    shift = pd.Timedelta(minutes=330)
    own = {}
    for r in ev[ev["booking_ref"] != ""].itertuples(index=False):
        own.setdefault(r.booking_ref, []).append(r)
    clock_of = {}
    for k_, lst in own.items():
        s0 = min((r.t for r in lst if r.event == "SESSION_START"), default=None)
        e0 = max((r.t for r in lst if r.event == "SESSION_END"), default=None)
        clock_of[k_] = (s0, e0)
    # ask A: a WS_FAIL the sitting stopped after; a restart of the sitting's workstation before it resumed there; a
    # reported failure of a computer or its keyboard, mouse or screen, by the spare and minute it resumed on; the sittings
    # running when the power cut began
    hit = set()
    for k_, lst in own.items():
        for n, r in enumerate(lst):
            if r.event == "WS_FAIL":
                later = [q for q in lst[n + 1:] if q.event != "WS_FAIL" and q.t > r.t]
                if later and later[0].event in ("SESSION_RESUME", "SESSION_END"):
                    hit.add(k_)
    boot = ev[ev["event"] == "WS_REBOOT"]
    boots = {}
    for r in boot.itertuples(index=False):
        boots.setdefault((r.centre_code, r.workstation), []).append(r.t)
    for k_, lst in own.items():
        for n, r in enumerate(lst):
            if r.event == "SESSION_RESUME" and not r.workstation.startswith("SP") and n:
                if any(lst[n - 1].t < t <= r.t for t in boots.get((r.centre_code, r.workstation), [])):
                    hit.add(k_)
    on_spare = {}
    for r in ev[(ev["event"] == "SESSION_RESUME") & ev["workstation"].str.match(r"SP\d")].itertuples(index=False):
        loc = r.t + shift
        on_spare[(r.centre_code, loc.date().isoformat(), r.workstation, loc.strftime("%H:%M"))] = r.booking_ref
    words = ("stopped responding", "froze", "hung", "not responding", "crashed", "frozen", "stopped working", "went blank",
             "stuck")
    cut_sittings, stopped_at = set(), []
    for centre, df in rep.items():
        for r in df.itertuples(index=False):
            d = dt.datetime.strptime(r.Date, "%d/%m/%Y").date()
            text = str(r.Report)
            clean = text.replace(",", " ").replace("(", " ").replace(")", " ").replace(";", " ")
            hm = [w.strip(".") for w in clean.split() if len(w.strip(".")) == 5 and w.strip(".")[2] == ":"]
            sp = [w.strip(".") for w in clean.split() if w.strip(".").startswith("SP")]
            if "All clocks stopped at" in text:
                h_, m_ = map(int, text.split("All clocks stopped at ")[1][:5].split(":"))
                stopped_at.append((codes[centre], pd.Timestamp(dt.datetime(d.year, d.month, d.day, h_, m_)) - shift))
                continue
            if "Power cut" in text:
                h_, m_ = map(int, r.Time.split(":"))
                cut = pd.Timestamp(dt.datetime(d.year, d.month, d.day, h_, m_)) - shift
                for k_, (s0, e0) in clock_of.items():
                    if own[k_][0].centre_code == codes[centre] and s0 is not None and s0 <= cut < (e0 or cut):
                        cut_sittings.add(k_)
                continue
            if sp and hm and any(w in text.lower() for w in words):
                k_ = on_spare.get((codes[centre], d.isoformat(), sp[0], hm[-1]))
                if k_:
                    hit.add(k_)
    hit |= cut_sittings
    form_of = {s["bk"]: s["form"] for s in sit if s["w"] >= 4}
    ask_a = {f: 0 for f in sorted(gain)}
    for k_ in hit:
        if k_ in form_of:
            ask_a[form_of[k_]] += 1
    # ask B: each client's link state walked through its workstation's events; a loss counts when another client at the
    # centre logged the loss too (a loss one client logged alone is its own connection), and while the sitting's clock
    # ran (a hall's clocks stopped before its link went down, to each sitting's next resume)
    halt = {}
    for cc, t in stopped_at:
        for k_, lst in own.items():
            s0, e0 = clock_of[k_]
            if lst[0].centre_code == cc and s0 is not None and s0 < t < e0:
                back = [q.t for q in lst if q.event == "SESSION_RESUME" and q.t > t]
                if back:
                    halt.setdefault(k_, []).append((t, min(back)))
    netrows = ev[ev["event"].isin(["NET_LOST", "NET_BACK"])]
    stamps = {}
    for r in netrows.itertuples(index=False):
        stamps.setdefault(r.centre_code, []).append((r.t, r.booking_ref, r.workstation))
    downs = []
    walk = ev[ev["event"].isin(["TUTORIAL_START", "SESSION_RESUME", "NET_LOST", "NET_BACK"])]
    for (cc, ws), g in walk.groupby(["centre_code", "workstation"], sort=True):
        state = {}
        for r in g.itertuples(index=False):
            k_ = r.booking_ref
            if clock_of.get(k_, (None, None))[0] is None:
                continue
            if r.event in ("TUTORIAL_START", "SESSION_RESUME"):
                state.setdefault(k_, {"login": r.t, "down": None})
                continue
            stt = state.setdefault(k_, {"login": clock_of[k_][0], "down": None})
            if r.event == "NET_LOST":
                if stt["down"] is None:
                    stt["down"] = r.t
            else:
                downs.append((cc, ws, k_, stt["down"] if stt["down"] is not None else stt["login"], r.t))
                stt["down"] = None
        for k_, stt in state.items():
            if stt["down"] is not None:
                downs.append((cc, ws, k_, stt["down"], clock_of[k_][1]))
    off = set(cut_sittings)
    two = pd.Timedelta(minutes=2)
    for cc, ws, k_, lo, hi in downs:
        if not any(lo - two <= t <= hi + two and (b_, w_) != (k_, ws) for t, b_, w_ in stamps[cc]):
            continue
        s0, e0 = clock_of[k_]
        spans = [(s0, e0)]
        for a_, z_ in halt.get(k_, []):
            spans = [x for p_, q_ in spans for x in ([(p_, q_)] if z_ <= p_ or a_ >= q_ else
                                                     [y for y in ((p_, a_), (z_, q_)) if y[0] < y[1]])]
        if any(max(p_, lo) < min(q_, hi) for p_, q_ in spans):
            off.add(k_)
    ask_b = {f: 0 for f in sorted(gain)}
    for k_ in off:
        if k_ in form_of:
            ask_b[form_of[k_]] += 1
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
