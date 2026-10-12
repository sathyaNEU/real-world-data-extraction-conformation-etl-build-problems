"""task137 generator checks: the call and its bins, the ladder and every rival the design note names, the estimator
corridor, every semantic fork row (SF1 to SF17), the domain claims the note and write-up make, the asks' goldens,
stops and devices, the separation and distractor deletion tests, the input gates, the realism sweep and the goldens'
agreement with figures.json. Run by build.py on the built pack; raises on the first failure and prints the count of
assertions passed."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil
import tempfile

import numpy as np
import pandas as pd

import asks as AK
import calc as C
import golden as GD
import world as W

N = [0]
ASK_FILES = [W.F_EVENTS, W.F_TRANSFERS, W.F_HOLDINGS, W.F_KIP, W.F_BATCHES]


def ok(cond, msg):
    if not cond:
        raise AssertionError(msg)
    N[0] += 1


def h250(x):
    return GD.h250(x)


def k1000(x):
    return GD.k1000(x)


def room(x, unit):
    """Distance from x to the nearest rounding edge of its bin, in the figure's own units."""
    return abs((x % unit) - unit / 2.0)


def pdf_text(path):
    import pdfplumber
    with pdfplumber.open(path) as pdf:
        return " ".join(" ".join((p.extract_text() or "").split()) for p in pdf.pages)


def docx_text(path):
    import docx
    return " ".join(p.text for p in docx.Document(path).paragraphs)


def months_of(F, U, Cc, R, p):
    return C.hours(F, C.minutes(F, U, Cc, R, p))


def golden_on_copy(target, drop_files):
    tmp = tempfile.mkdtemp(suffix=".t137")
    try:
        for f in os.listdir(target):
            if f not in drop_files:
                shutil.copy2(os.path.join(target, f), os.path.join(tmp, f))
        L2 = C.load(tmp)
        G2 = C.golden(L2)
        out = dict(total=G2["total"], months=G2["months"])
        if not set(drop_files) & set(ASK_FILES):
            A2 = AK.load(tmp)
            out["a"] = AK.ask_a(A2)
            out["b"] = AK.ask_b(A2)
        return out
    finally:
        shutil.rmtree(tmp)


def run(target, golden, Wd=None, H=None, meta_path=None):
    p = lambda f: os.path.join(target, f)
    L = C.load(target)
    G = C.golden(L)
    F, cases, R, U, Cc = G["F"], G["cases"], G["R"], G["U"], G["C"]
    cv = cases[cases["conv"]]
    g, gm = G["total"], G["months"]
    figs = json.load(open(os.path.join(os.path.dirname(golden), "generator", "figures.json")))
    sow, proc = pdf_text(p(W.F_SOW)), docx_text(p(W.F_PROCEDURE))
    briefs = {q: pdf_text(p(W.brief_name(q))) for q in W.PAST + [W.FWD]}

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "fewer than 10 files")
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(fmts) >= 3, "fewer than 3 formats: %s" % fmts)
    with open(p(W.F_DIALS)) as fh:
        ok(sum(1 for _ in fh) - 1 >= 25000, "no file of 25,000 rows")
    meta = json.load(open(meta_path))
    ok(sorted(meta["distractor_files"]) == sorted(W.DISTRACTORS), "metadata distractors")
    ok(all(d in files for d in W.DISTRACTORS), "a distractor is missing from the pack")
    ok(not any("distractor" in f.lower() for f in files), "a file name says distractor")
    ok(meta["deliverables"] == [GD.BOOK, GD.NOTE], "metadata deliverables")
    ok(len(meta["files"]) == len(files) and all(x["license"] and x["source"] and x["date"] for x in meta["files"]),
       "metadata file records")

    # ------------------------------------------------------------------ the call
    ok(len(F) == W.FWD_LIST_SIZE == 18400, "list size %d" % len(F))
    ok(abs(sum(gm.values()) - g) < 1e-6, "months do not add to the total")
    ok(sum(h250(v) for v in gm.values()) == h250(g), "rounded months do not add to the rounded booking")
    ok(figs["call"]["booking_hours"] == "{:,}".format(h250(g)), "figures.json booking")
    for k, nm in GD.MONTHS.items():
        ok(figs["call"]["hours_by_month"][nm] == "{:,}".format(h250(gm[k])), "figures.json %s" % nm)
    ok(room(g, 250) >= 25, "SF13 booking %.1f within 25 hours of an edge" % g)
    for k in (1, 2, 3):
        ok(room(gm[k], 250) >= 25, "SF13 month %d %.1f within 25 hours of an edge" % (k, gm[k]))

    # ------------------------------------------------------------------ the ladder and every rival
    Rg = C.rungs(L, G)
    for k in ("R0_latest", "R0_all", "R1_pooled", "R2a_latest", "R2b_term", "R2c_locked", "R2d_trend"):
        ok(Rg[k] <= 0.92 * g and h250(Rg[k]) != h250(g), "rung %s %.1f too near the golden %.1f" % (k, Rg[k], g))
    ok(Rg["R3_no_release"] >= 1.03 * g and h250(Rg["R3_no_release"]) != h250(g), "drop without release share")
    pooled = float(cv["ret"].mean())
    rivals = {"pooled": pooled, "latest": float(cv[cv["campaign"] == W.PAST[-1]]["ret"].mean()),
              "term": F["term"].map(cv.groupby("term")["ret"].mean())}
    lb = cv.groupby(np.floor(cv["rate"] / 0.25 + 1e-9))["ret"].mean()
    fk = np.floor(F["rate"] / 0.25 + 1e-9)
    keys = np.array(sorted(lb.index))
    rivals["locked"] = fk.map(lambda k: lb[keys[np.argmin(np.abs(keys - k))]])
    lt = cv.groupby([np.floor(cv["rate"] / 0.25 + 1e-9), cv["term"]])["ret"].mean()
    rivals["locked x term"] = [lt.get((k, t), pooled) for k, t in zip(fk, F["term"])]
    last = cv[cv["campaign"] == W.PAST[-1]].groupby("term")["ret"].mean()
    rivals["latest by term"] = F["term"].map(last).fillna(pooled)
    qs = cv.groupby("campaign")["ret"].mean().reindex(W.PAST)
    a, b = np.polyfit(np.arange(len(W.PAST)), qs.values, 1)
    rivals["trend"] = float(np.clip(b + a * (len(W.PAST) + 1), 0, 1))
    tt = {}
    for t, gt in cv.groupby("term"):
        q = gt.groupby("campaign")["ret"].mean().reindex(W.PAST).dropna()
        a, b = np.polyfit([W.PAST.index(c) for c in q.index], q.values, 1)
        tt[t] = float(np.clip(b + a * (len(W.PAST) + 1), 0, 1))
    rivals["term trend"] = F["term"].map(tt)
    for nm, share in rivals.items():
        tot, mon = months_of(F, U, Cc, R, np.asarray(share, dtype=float) if not np.isscalar(share) else share)
        ok(tot <= 0.92 * g, "rival %s %.1f within 8 per cent of the golden" % (nm, tot))
        ok(h250(tot) != h250(g) and all(h250(mon[k]) != h250(gm[k]) for k in (1, 2, 3)),
           "rival %s lands a graded figure: %.1f %s" % (nm, tot, mon))
    ok(figs["default_path"]["pooled_share_hours"] == "{:,}".format(h250(Rg["R1_pooled"])), "default path figure")

    # ------------------------------------------------------------------ the corridor (SF7, SF8, SF9)
    fam = C.family(L, G)
    for nm, (tot, mon) in fam.items():
        ok(h250(tot) == h250(g), "SF8/SF9 %s files %d" % (nm, h250(tot)))
        ok(all(h250(mon[k]) == h250(gm[k]) for k in (1, 2, 3)), "SF8/SF9 %s month %s" % (nm, mon))
    ok(len(fam) >= 30, "family too small")
    pl, coef = C.p_linear(cases, F["drop"])
    ok(coef[0] + coef[1] * cv["drop"].min() < 0 and cv.loc[cv["drop"] < -1, "ret"].mean() < 0.01,
       "SF8 the linear fit is not refused by the past data")
    band = cv[(cv["drop"] >= 2.5)]
    ok(abs(coef[0] + coef[1] * 2.5 - band["ret"].mean()) > 0.2, "SF8 the linear fit tracks the high drops")

    # ------------------------------------------------------------------ SF rows
    ok("Agent time is billed per event at the minutes below" in sow and "agent-hours" in sow, "SF1 SOW 2.1")
    ok(not any(w in f.lower() for f in files for w in ("roster", "timesheet", "shift")), "SF1 shift data shipped")
    ok("forecast to need, rounded to the nearest 250 hours" in proc, "SF2 procedure 6.1")
    ok("in multiples of 250" in sow, "SF2 SOW 2.2 block multiples")
    ok(F["customer_no"].is_unique and "The list carries one deposit per member" in proc, "SF3 one deposit per member")
    ok(F["maturity"].min() >= pd.Timestamp("2027-01-01") and F["maturity"].max() <= pd.Timestamp("2027-03-31"),
       "SF4 maturities outside the quarter")
    dnc = L["dnc"]
    ok(pd.to_datetime(dnc["recorded"]).max() <= pd.Timestamp(W.CUT_FWD), "SF5 register entry after the cut")
    wd = pd.to_datetime(dnc["withdrawn"].replace("", None)).dropna()
    ok(wd.empty or wd.max() <= pd.Timestamp(W.CUT_FWD), "SF5 withdrawal after the cut")
    ok(pd.to_datetime(L["contacts"]["recorded"]).max() <= pd.Timestamp(W.CUT_FWD), "SF5 contact point after the cut")
    ok("reinvests for the same term at the posted rate in force on its maturity date" in proc, "SF6 Terms 9.2 in 5.1")
    ok("Reinvestment rates for deposits maturing this quarter" in briefs[W.FWD] and "draft" in briefs[W.FWD],
       "SF6 the draft brief's rates")
    ok("as approved by ALCO" in briefs[W.FWD], "SF6 the card approved")
    ok("every campaign the contact centre has closed under the statement of work" in proc, "SF7 procedure 6.1")
    for nm in ("subset/2025", "subset/2026", "subset/latest4"):
        ok(nm in fam, "SF7 %s missing" % nm)
    ok(float(G["m"][F["cfg"] == ""].abs().sum()) == 0.0, "SF10 hours on a deposit with no callable number")
    ok("A deposit with no callable number is not released" in proc, "SF10 procedure 4.3")
    rel = L["release"]
    ok(set(rel.loc[rel["status"] == "NOT RELEASED", "reason"]) == {"INSTRUCTED", "NO CALLABLE NUMBER"},
       "SF11 release reasons")
    ok(set(rel.loc[rel["status"] == "RELEASED", "reason"]) == {""}, "SF11 released rows carry a reason")
    ok("A deposit is not released if the holder has given maturity instructions by then" in proc, "SF11 procedure 4.2")
    cl = L["close"]
    ok(len(cl) == int((rel["status"] == "RELEASED").sum()), "SF11 one close-out per released case")
    ok((cl["close_reason"] == "WITHDRAWN").sum() > 100, "SF12 withdrawn cases in the close-outs")
    ok(set(cl["close_reason"]) <= {"CONVERSATION", "EXHAUSTED", "WITHDRAWN", "MATURED"}, "SF12 close reasons")
    ok("structural/bins0.25+0.000" in fam, "SF12 the per-number model with withdrawals")
    row22 = re.search(r"intend to withdraw ([A-Z, ]+?) 22 or move the funds", sow)
    ok(row22 is not None and set(row22.group(1).replace(",", " ").split()) == set(W.RETENTION), "SF14 SOW 22-minute row")
    row15 = re.search(r"does not reach the holder ([A-Z, ]+?) 1\.5", sow)
    ok(row15 is not None and set(row15.group(1).replace(",", " ").split()) == set(W.NOT_REACHED),
       "SF15 SOW 1.5-minute row")
    for m in sorted(set(F["maturity"].dt.date)):
        ok(len(W.dialling_days(m - dt.timedelta(days=21), m)) >= W.DIALS_PER_NUMBER,
           "SF16 %s has too few dialling days" % m)
    raw = pd.read_csv(p(W.F_LIST_FWD), dtype=str)
    st_ = pd.to_datetime(raw["start_date"])
    mt = pd.to_datetime(raw["maturity_date"])
    yrs = raw["term_months"].astype(int) // 12
    ok(all((m_.year - s_.year == y_) and (m_.month == s_.month) for s_, m_, y_ in zip(st_, mt, yrs)),
       "SF17 a term disagrees with its dates")
    for sf in range(1, 18):
        ok(("SF%d" % sf) in open(__file__).read(), "SF%d not asserted" % sf)

    # ------------------------------------------------------------------ domain claims in the note and write-up
    bands = pd.cut(cv["drop"], [-99, 0, 0.5, 1.0, 1.5, 2.0, 2.5, 99], right=False)
    for key in ("campaign", "term"):
        t = cv.groupby([key, bands], observed=True)["ret"].agg(["mean", "size"])
        for kv, sub in t.groupby(level=0):
            s = sub[sub["size"] >= 150]["mean"].values
            ok(all(np.diff(s) > 0), "the share does not rise with the drop within %s %s: %s" % (key, kv, s))
    ok(float(cv.loc[cv["drop"] < 0, "ret"].mean()) < 0.01, "share where the rate rose")
    hi = cv[cv["drop"] >= 2.5]
    ok(figs["components"]["past_share_at_2_5_or_more_pct"] == "%d" % int(np.floor(100 * hi["ret"].mean() + 0.5)),
       "past share at 2.5 or more")
    ok(figs["components"]["past_pooled_share_pct"] == "%d" % int(np.floor(100 * pooled + 0.5)), "pooled share")
    sp = F[(F["term"] == 4) & (F["rate"] == 5.65)]
    ok(figs["components"]["deposits_at_5_65_four_year"] == "{:,}".format(len(sp)), "four-year deposits at 5.65")
    ok(set(sp["drop"].round(2)) == {round(5.65 - L["cards"][W.FWD][4], 2)}, "the special's drop")
    ok(len(sp) > 0.5 * len(F), "the special is not most of the list")
    past4 = cv[cv["term"] == 4]
    ok(float(past4["ret"].mean()) < 0.05, "past four-year share")
    pl4 = L["past_lists"][L["past_lists"]["term"] == 4]
    ok(pl4["maturity"].dt.year.min() >= 2025 and pl4["maturity"].dt.year.max() <= 2026, "past four-year deposits")
    d = L["dials"]
    mins = d["outcome"].map(W.billed_minutes)
    listed = L["past_lists"].groupby("campaign").size()
    per = {q: float(mins[d["case_ref"].str[2:6] == q[2:4] + q[-2:]].sum()) / listed[q] for q in W.PAST}
    ok(max(per.values()) < g * 60 / len(F), "a past campaign used more minutes per listed deposit than the forecast")
    ok(len(set(listed.values)) == len(listed), "identical list sizes across campaigns")
    share = G["ret"] / G["conv"]
    ok(figs["components"]["retention_share_pct"] == "%d" % (5 * int(np.floor(100 * share / 5 + 0.5))), "share figure")
    ok(abs(100 * share - int(figs["components"]["retention_share_pct"])) < 2.5, "about 60 per cent")
    ok(figs["components"]["no_callable_number"] == "{:,}".format(int((F["cfg"] == "").sum())), "no callable count")
    ok(figs["steps"]["release_share_pct"] == "%.1f" % (100 * R), "release share")

    # ------------------------------------------------------------------ the asks
    A = AK.load(target)
    st = AK.all_stops(A)
    ga, gb = st["A"]["golden"], st["B"]["golden"]
    for q in W.PAST:
        n_, a_ = ga[q]
        ok(figs["ask_a"][q]["deposits"] == "{:,}".format(n_) and figs["ask_a"][q]["principal_nzd"] == "{:,}".format(
            k1000(a_)), "ask A figures %s" % q)
        ok(room(a_, 1000) >= 70, "ask A %s principal near an edge" % q)
        for mode in ("own", "holder", "nobreak"):
            n2, a2 = st["A"][mode][q]
            ok(n2 != n_ and k1000(a2) != k1000(a_), "ask A %s %s lands" % (mode, q))
        n2, a2 = st["A"]["whole"][q]
        ok(n2 == n_ and k1000(a2) != k1000(a_), "ask A whole %s" % q)
        n2, a2 = st["A"]["anyreinv"][q]
        if q.startswith("2026"):
            ok(n2 != n_ and k1000(a2) != k1000(a_), "ask A anyreinv %s lands" % q)
    for k in (1, 2, 3):
        t_, n_ = gb[k]
        nm = GD.MONTHS[k]
        ok(figs["ask_b"][nm]["maturing_nzd"] == "{:,}".format(k1000(t_)) and
           figs["ask_b"][nm]["not_on_list_nzd"] == "{:,}".format(k1000(n_)), "ask B figures %s" % nm)
        ok(room(t_, 1000) >= 70 and room(n_, 1000) >= 70, "ask B %s near an edge" % nm)
        for mode in ("rows_both", "dedup_both", "dedup_core", "rows_core", "deferred"):
            t2, n2 = st["B"][mode][k]
            ok(k1000(t2) != k1000(t_) and k1000(n2) != k1000(n_), "ask B %s %s lands" % (mode, nm))
    reinv, gone, opens, by_holder, out = AK._index(A)
    lists = A["lists"]
    ev = A["events"]
    mature = set(zip(ev.loc[ev["event_type"] == "MATURE", "account"], ev.loc[ev["event_type"] == "MATURE", "event_date"]))
    ok(all((a, m.date().isoformat()) in mature for a, m in zip(lists["account"], lists["maturity"])),
       "ask A a listed deposit has no MATURE event at its maturity")
    near = 0
    for a, m in zip(lists["account"], lists["maturity"]):
        m = m.date()
        accts = [a] + [to for to, _ in out.get((a, m), []) if to in opens]
        for x in accts:
            near += sum(1 for d_ in gone.get(x, []) if 25 <= (d_ - m).days <= 35)
    ok(near == 0, "ask A C1: %d breaks or closes between day 25 and day 35" % near)
    tr = A["transfers"]
    sav = tr["from_account"].str.len().eq(16) & tr["from_account"].str[-3:].isin(W.SAV_SUFFIXES)
    ok(not (sav & tr["to_account"].isin(set(opens))).any(), "ask A C1: savings moved into a term deposit")
    pay = set(zip(ev.loc[ev["event_type"] == "PAYOUT", "account"], ev.loc[ev["event_type"] == "PAYOUT", "event_date"]))
    ok(not any((a, d_.isoformat()) in pay for a, d_ in reinv), "ask A a deposit both reinvested and paid out")
    ok(sum(1 for (a, m), v in out.items() for to, _ in v if to in opens) > 1000, "ask A few change-of-term chains")
    fresh = set(opens) - set(tr.loc[tr["narrative"] == "MATURITY PROCEEDS", "to_account"])
    ok(len(fresh) > 200, "ask A holders opened no deposits with new money (%d)" % len(fresh))
    hold = A["hold"]
    fwd = A["fwd"].set_index("account")
    hd = hold.drop_duplicates("account").set_index("account")
    ok(set(fwd.index) <= set(hd.index), "ask B a listed deposit is missing from the holdings view")
    ok(np.allclose(hd.loc[fwd.index, "principal"].values, fwd["principal"].values), "ask B principal disagrees")
    ok((hd.loc[fwd.index, "maturity_date"].values == fwd["maturity_date"].values).all(), "ask B maturity disagrees")
    ok((hd.loc[fwd.index, "product"] == "TD").all(), "ask B a certificate on the list")
    ok(hold["account"].duplicated().sum() > 1000, "ask B no joint holders")
    bt = A["batches"]
    both = set(bt.loc[bt["status"] == "DEFERRED", "cert_no"]) & set(bt.loc[bt["status"] == "MIGRATED", "cert_no"])
    ok(len(both) > 10, "ask B no certificate deferred then moved")
    mig = bt[bt["status"] == "MIGRATED"]
    kic = set(hold.loc[hold["product"] == "KIC", "account"])
    kipm = A["kip"].set_index("cert_no")["maturity_date"]
    inh1 = mig[(kipm.reindex(mig["cert_no"]).values >= "2027-01-01") & (kipm.reindex(mig["cert_no"]).values <= "2027-06-30")]
    ok(set(inh1["new_account"]) <= kic, "ask B a moved certificate is not in the holdings view")
    kq1 = A["kip"][(A["kip"]["maturity_date"] >= "2027-01-01") & (A["kip"]["maturity_date"] <= "2027-03-31")]
    ok((~kq1["cert_no"].isin(set(mig["cert_no"]))).sum() > 20, "ask B no certificate left on the platform")

    # ------------------------------------------------------------------ separation and distractor deletion
    s1 = golden_on_copy(target, ASK_FILES)
    ok(abs(s1["total"] - g) < 1e-9 and all(abs(s1["months"][k] - gm[k]) < 1e-9 for k in (1, 2, 3)),
       "the call moves without the ask files")
    s2 = golden_on_copy(target, list(W.DISTRACTORS))
    ok(abs(s2["total"] - g) < 1e-9 and s2["a"] == ga and s2["b"] == gb, "a distractor moves a figure")

    # ------------------------------------------------------------------ realism sweep
    stamp = W.EXPORT_STAMP.timestamp()
    ok(all(abs(os.path.getmtime(p(f)) - stamp) < 1 for f in files), "an mtime is off the export stamp")
    for f in files:
        if f.endswith((".csv", ".txt", ".eml")):
            txt = open(p(f), encoding="utf-8", errors="replace").read()
            ok("\u2014" not in txt and "\u2013" not in txt, "a dash in %s" % f)
    for f in [W.F_SOW, W.F_PROPOSAL] + [W.brief_name(q) for q in W.PAST + [W.FWD]]:
        ok("\u2014" not in pdf_text(p(f)), "an em dash in %s" % f)
    ok("\u2014" not in proc, "an em dash in the procedure")
    import email
    from email import policy as _pol
    msg = email.message_from_bytes(open(p(W.F_THREAD), "rb").read(), policy=_pol.default)
    eml = " ".join(str(msg[h]) for h in ("From", "To", "Cc")) + " " + msg.get_body().get_content()
    for who in ("product", "vendor", "head"):
        ok(W.PEOPLE[who] in eml, "the thread is missing %s" % who)
    ok(dt.date(2026, 11, 2).weekday() == 0 and dt.date(2026, 11, 4).weekday() == 2 and
       dt.date(2026, 11, 17).weekday() == 1 and dt.date(2026, 11, 20).weekday() == 4, "the thread's days of the week")
    ok("approved by the Deposits Committee" in proc and "Deposits Committee signs off" in eml, "the forum is filed")
    for q in W.PAST + [W.FWD]:
        n_ = W.FWD_LIST_SIZE if q == W.FWD else int(listed[q])
        ok("{:,}".format(n_) in briefs[q], "brief %s does not carry its list size" % q)
        card = C.read_card(p(W.brief_name(q)))
        ok(card == {t: W.card(q, t) for t in W.TERMS}, "brief %s card" % q)
    ok(len(set(F["principal"])) > 5000, "the list's principal is too uniform")
    ok(int(F["principal"].sum()) % 1000 != 0, "a round list total")
    import openpyxl
    ok("wholesale" in str(openpyxl.load_workbook(p(W.F_OUTLOOK)).active["A2"].value), "the outlook's scope line")

    # ------------------------------------------------------------------ the goldens agree with figures.json
    wb = openpyxl.load_workbook(os.path.join(golden, GD.BOOK), data_only=True)
    ws = wb["Booking"]
    vals = {ws.cell(row=r, column=1).value: ws.cell(row=r, column=8).value for r in range(5, 9)}
    ok(vals["Quarter"] == h250(g), "workbook booking")
    for k, nm in GD.MONTHS.items():
        ok(vals["%s 2027" % nm] == h250(gm[k]), "workbook %s" % nm)
    ws2 = wb["Kept at 30 days"]
    for r, q in enumerate(W.PAST, 5):
        ok(ws2.cell(row=r, column=4).value == ga[q][0] and ws2.cell(row=r, column=5).value == k1000(ga[q][1]),
           "workbook ask A %s" % q)
    ws3 = wb["Maturing Q1 2027"]
    for r, k in enumerate((1, 2, 3), 5):
        ok(ws3.cell(row=r, column=2).value == k1000(gb[k][0]) and ws3.cell(row=r, column=3).value == k1000(gb[k][1]),
           "workbook ask B %d" % k)
    pm = GD.compute(target)["per_month"]
    for k in (1, 2, 3):
        talk = (pm[k]["conv"] * W.MIN_CONVERSATION + pm[k]["ret"] * (W.MIN_RETENTION - W.MIN_CONVERSATION)) / 60.0
        ok(0.65 <= talk / pm[k]["hours"] < 0.75 and pm[k]["ret"] > 0.5 * pm[k]["conv"],
           "the chart's title: month %d talk share %.3f" % (k, talk / pm[k]["hours"]))
    note = docx_text(os.path.join(golden, GD.NOTE))
    ok(note.count(figs["call"]["booking_hours"]) >= 1 and
       ("Book %s agent-hours" % figs["call"]["booking_hours"]) in note, "the note does not open with the booking")
    print("checks: %d assertions passed (golden %.1f hours, months %s; family %d members)" % (
        N[0], g, {k: round(v, 1) for k, v in gm.items()}, len(fam)))
    return N[0]
