"""task238 checks: the three rules executed on the simulator's clean truth (R1 to R3c), every semantic fork row (SF1 to
SF14), the golden against the generating model with its margins, the rungs, the ask devices and their stops, the
separation of the call from the devices, the documents' pins, the input gates and the realism sweep."""
import datetime as dt
import json
import os
import re

import numpy as np
import pandas as pd

import estim as E
import params as P

N = [0]
HERE = os.path.dirname(os.path.abspath(__file__))
CODES = [x[0] for x in P.INDEXES]
TOL = {x[0]: x[4] for x in P.INDEXES}
MISHANDLED = {
    "late returns kept (the close ignored)": dict(late_rule="none"),
    "the close read on the UTC date": dict(late_rule="utcdate"),
    "the close at UTC+12 on 30 September": dict(late_rule="fixed12"),
    "returns giving an age under 18 kept": dict(teens=True),
    "the 9 to 12 August staff-entry interviews read as web": dict(staff_as="web"),
    "the CATI clock read as UTC": dict(order="naive"),
    "the CATI clock read at UTC+12 all year": dict(order="fixed12"),
    "both records of a twice-answered address kept": dict(keep="both"),
}


def ok(cond, label):
    assert cond, label
    N[0] += 1


def _pdf_text(path):
    from pypdf import PdfReader
    return " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(path).pages)


def _docx_text(path):
    import docx
    return " ".join(p.text for p in docx.Document(path).paragraphs)


def band_from(eff):
    return E.band_of(eff)


# ------------------------------------------------------------------ the clean truth: households before any record
def clean(W):
    c = W.complete
    d = pd.DataFrame(dict(letter=np.where(W.letter_a[c], "A", "B"), mode=np.where(W.web[c], "web", "cati"),
                          age=W.age[c], sex=np.where(W.female[c], 2, 1), qual=np.where(W.deg[c], 4, np.where(W.post[c], 3, 2)),
                          emp=np.where(W.emp[c], 1, 2), tenure=np.where(W.rent[c], 3, 1), hhsize=W.hh[c],
                          region_code=W.region[c].astype(str)))
    vals = {}
    for code, name, item, kind, tol, th in P.INDEXES:
        ph, wb = W.ans[code]
        y = np.where(W.web[c], wb[c], ph[c]).astype(float)
        vals[code] = y if kind == "score" else 100 * y
    return d, vals


def clean_routes(d, vals):
    out = {}
    webm = (d["mode"] == "web").values
    A = (d["letter"] == "A").values
    X = E.design(d)
    Z = np.column_stack([X, A])
    what = Z @ np.linalg.lstsq(Z, webm.astype(float), rcond=None)[0]
    for code in CODES:
        y = vals[code]
        itt = y[A].mean() - y[~A].mean()
        dw = webm[A].mean() - webm[~A].mean()
        out[code] = dict(raw=y[webm].mean() - y[~webm].mean(),
                         adj=np.linalg.lstsq(np.column_stack([X, webm]), y, rcond=None)[0][-1],
                         itt=itt, wald=itt / dw,
                         tsls=np.linalg.lstsq(np.column_stack([X, what]), y, rcond=None)[0][-1],
                         perprotocol=y[A & webm].mean() - y[~A & ~webm].mean())
    return out


def route_bands(rt):
    return {r: band_from({c: rt[c][r] for c in CODES}) for r in ("raw", "adj", "itt", "wald", "tsls", "perprotocol")}


def pack_routes(s):
    out = {}
    for code, name, item, kind, tol, th in P.INDEXES:
        out[code] = E.routes(s, code, item, kind)
    return out


def run(target, golden, o, X):
    N[0] = 0
    W = o["W"]
    import build as B
    files = {k: os.path.join(target, f) for k, f in B.FILES.items()}
    iss, web, cati = X["iss"], X["web"], X["cati"]
    s = X["s"]
    std = _pdf_text(files["standard"])
    plan = _pdf_text(files["plan"])
    close = _docx_text(files["close"])
    dic = open(files["dict"]).read()

    # ------------------------------------------------------------ the golden
    ok(X["band"] == 4 and X["bind"] == "BD" and X["runner"] == "VL",
       "golden: band 4, heavy drinking binding, volunteering next (%s %s %s)" % (X["band"], X["bind"], X["runner"]))
    truth = {code: (W.ans[code][1][W.complete] - W.ans[code][0][W.complete]).mean() * (1 if code in P.SCORE else 100)
             for code in CODES}
    tb = band_from(truth)
    ok(tb[0] == 4 and tb[1] == "BD", "golden: the generating model's own mode effects set band 4 on heavy drinking")
    wb = X["widest"]["BD"]
    ok(4.25 <= wb <= 4.75, "golden: heavy drinking's widest band sits mid-bin (%.3f)" % wb)

    # ------------------------------------------------------------ R1: the field's raw material ships, no deciding column
    banned = re.compile(r"effect|band|index|score|wald|instrument|complier|weight|mode_", re.I)
    for k in ("issued", "web", "cati", "calls", "regions"):
        cols = pd.read_csv(files[k], nrows=1).columns
        ok(not [c for c in cols if banned.search(c)], "R1 no column of %s holds a mode effect, a band or a score"
           % B.FILES[k])
    ok({"letter", "login_code", "address_id"} <= set(iss.columns) and "last_section" in web.columns
       and "RESULT" in cati.columns, "R1 the assignment records and both systems' answers ship at record level")
    ok(len(s) == int(W.complete.sum()), "R1 the completes the plan's rules build are the generator's completes (%d)"
       % len(s))
    true_mode = pd.Series(np.where(W.web, "web", "cati"), index=[o["R"].address_id[i] for i in range(W.n)])
    ok((s.set_index("address_id")["mode"] == true_mode.loc[s["address_id"]].values).all(),
       "R1 every complete's mode as built is the mode the household answered in")

    # ------------------------------------------------------------ R3a and R3b: the analyst test on the clean truth
    d, vals = clean(W)
    cr = clean_routes(d, vals)
    cb = route_bands(cr)
    ok(cb["adj"][0] == 3 and cb["adj"][1] == "SF",
       "R3a the easy route on the clean truth (web against telephone completes, every recorded characteristic held "
       "fixed) files 3 with safe after dark binding (%s)" % (cb["adj"][:2],))
    ok(cb["raw"][0] == 2, "R3a the raw comparison on the clean truth files 2 (%s)" % (cb["raw"][:2],))
    ok(cb["perprotocol"][0] == 3, "R3a letter A's online against letter B's telephone completes files 3")
    ok(cb["itt"][0] == 6, "R3a the letters' raw difference on the clean truth files 6 (%s)" % (cb["itt"][:2],))
    ok(cb["wald"][0] == 4 and cb["wald"][1] == "BD",
       "R3b the decisive step alone (the letters' difference over their difference in web uptake) files 4")
    ok(cb["tsls"][0] == 4, "R3b two-stage least squares with the letter as the instrument files 4 on the clean truth")
    ok(all(cb[r][0] != 4 for r in ("raw", "adj", "itt", "perprotocol")),
       "R3b every lower rung's single correction leaves the band off 4")

    # ------------------------------------------------------------ the rungs on the pack, by name and margin
    pr = pack_routes(s)
    pb = route_bands(pr)
    ok(pb["raw"][0] == 2 and pb["raw"][1] == "BD", "rung 0a raw comparison: 2, heavy drinking (%s)" % (pb["raw"][:2],))
    ok(pb["adj"][0] == 3 and pb["adj"][1] == "SF", "rung 0 adjusted comparison: 3, safe after dark (%s)" % (pb["adj"][:2],))
    ok(pb["perprotocol"][0] == 3, "rung 1 letter A online against letter B telephone: 3")
    ok(pb["itt"][0] == 6 and pb["itt"][1] == "BD", "rung 2 the letters' raw difference: 6 (%s)" % (pb["itt"][:2],))
    ok(pb["wald"][0] == 4 and pb["tsls"][0] == 4, "rung 3 the Wald estimator and two-stage least squares: 4 and 4")
    ok(abs(pb["adj"][2]["SF"] - 3.5) >= 0.05 and abs(pb["itt"][2]["BD"] - 6.5) >= 0.15,
       "rung margins: the adjusted binding band %.2f and the raw-difference band %.2f sit inside their bins"
       % (pb["adj"][2]["SF"], pb["itt"][2]["BD"]))
    ok(4 + 1 < pb["itt"][2]["BD"] < 7 and 3 <= pb["adj"][2]["SF"] < 4 and pb["raw"][2]["BD"] < 3,
       "position: raw 2 < adjusted 3 < golden 4 < raw difference 6, the golden bracketed")
    # other routes an analyst could take
    q_eff = {}
    for code, name, item, kind, tol, th in P.INDEXES:
        q_eff[code] = np.mean([E.wald(s[s["quarter"] == q], code, item, kind)[0] for q in P.QUARTERS])
    ok(band_from(q_eff)[0] == 4, "route: the Wald estimator per quarter, averaged, files 4")
    per_q = {q: band_from({c: E.wald(s[s["quarter"] == q], c, it, k)[0] for c, n_, it, k, t_, th_ in P.INDEXES})
             for q in P.QUARTERS}
    ok(all(v[1] == "BD" for v in per_q.values()), "route: each quarter alone binds on heavy drinking (%s)"
       % {q: v[0] for q, v in per_q.items()})
    issued_dw = {}
    for code, name, item, kind, tol, th in P.INDEXES:
        ok_, y = E.index_values(s, code, item, kind)
        t = s.loc[ok_]
        A = (t["letter"] == "A").values
        itt = y.values[A].mean() - y.values[~A].mean()
        el = iss[~iss["final_outcome"].isin(["4.1", "4.2", "4.3"])]
        wa = ((t["mode"] == "web") & (t["letter"] == "A")).sum() / (el["letter"] == "A").sum()
        wbb = ((t["mode"] == "web") & (t["letter"] == "B")).sum() / (el["letter"] == "B").sum()
        issued_dw[code] = itt / (wa - wbb)
    ok(band_from(issued_dw)[0] == 2, "route: the letters' difference over web uptake per issued address files 2")
    adjl = {}
    for code, name, item, kind, tol, th in P.INDEXES:
        ok_, y = E.index_values(s, code, item, kind)
        t = s.loc[ok_]
        keep = t[["age", "sex", "qual", "emp", "tenure", "hhsize"]].notna().all(axis=1).values
        Xd = E.design(t[keep])
        adjl[code] = np.linalg.lstsq(np.column_stack([Xd, (t["letter"] == "A").values[keep],
                                                     (t["mode"] == "web").values[keep]]), y.values[keep], rcond=None)[0][-1]
    ok(band_from(adjl)[0] not in (4, 5), "route: the adjusted comparison with the letter as a control files %d"
       % band_from(adjl)[0])

    # ------------------------------------------------------------ R2: every mess item neutral for the call
    comp = {}
    for name, kw in MISHANDLED.items():
        sm = E.completes(iss, web, cati, **kw)
        r = pack_routes(sm)
        b = route_bands(r)
        ok(b["wald"][0] == 4 and b["wald"][1] == "BD" and 4 <= b["wald"][2]["BD"] < 5 and b["tsls"][0] == 4,
           "R2 %s: the band stays 4, heavy drinking binding" % name)
        ok(b["adj"][0] == 3 and b["itt"][0] in (6, 7) and b["raw"][0] == 2,
           "R2 %s: the wrong rungs stay wrong" % name)
        comp[name] = sm
    part = web[web["last_section"] < 6].copy()
    ok(len(part) > 0 and part["submitted_utc"].isna().all(), "R2 partial web returns carry no submission time")

    # ------------------------------------------------------------ the critical components hold for both estimators
    for est in ("wald", "tsls"):
        wd = {c: 100 * TOL[c] / abs(pr[c][est]) for c in CODES}
        ok(4 <= wd["BD"] < 5 and 6 <= wd["VL"] < 7 and min(v for c, v in wd.items() if c not in ("BD", "VL")) >= 8,
           "components under %s: heavy drinking 4 to under 5, volunteering 6 to under 7, every other 8 or more" % est)
        ok(6 < pr["BD"][est] <= 7.5, "components under %s: heavy drinking's effect more than 6, at most 7.5" % est)

    # ------------------------------------------------------------ R3c: nothing planted
    ok(not re.search(r"\d+(\.\d+)? (percentage )?points? of web share|band of \d", std + plan + close),
       "R3c no document states a band")
    ok(not re.search(r"mode effect (of|is|was) [-\d]", std + plan + close, re.I), "R3c no document states a mode effect")
    ok(not re.search(r"instrument|wald|two-stage|complier|encourage", std + plan + close + dic, re.I),
       "R3c no document names the estimator")
    dup_rows = web.drop(columns=["response_id"]).duplicated().sum() + cati.drop(columns=["CASE_ID"]).duplicated().sum()
    ok(dup_rows == 0, "R3c no copied rows in either export")

    # ------------------------------------------------------------ semantic forks on the call
    ok("every household in the population it is measured on answered online" in std and
       "every one of those households answered by telephone" in std,
       "SF1 the mode effect is filed as the whole population answering online against by telephone")
    ok(pb["raw"][0] != 4, "SF1 the respondent-group reading (web completes against telephone completes) files %d"
       % pb["raw"][0])
    ok("percentage of a quarter's completes made online" in std, "SF2 web share is a share of completes")
    ok(band_from(issued_dw)[0] != 4, "SF2 a share of issued addresses gives another band, so the filed one binds")
    ok("widest whole-point band" in std and 5 * pr["BD"]["wald"] / 100 > TOL["BD"],
       "SF3 the band is the widest whole point within tolerance: 5 points would breach heavy drinking's")
    ok("central estimate of its mode effect" in std, "SF4 the band is set on central estimates")
    ok("both quarters and under both letters" in std, "SF5 the effects are measured on both quarters, both letters")
    ok(all(v[0] == 4 for v in per_q.values()), "SF5 a single quarter alone files the same band (%s)"
       % {q: v[0] for q, v in per_q.items()})
    ok("highest result" in plan and "first counts" in plan, "SF6 the plan files the address's result and the first complete")
    cbk = pd.read_excel(files["codebook"], sheet_name="Indexes", dtype=str)
    ok(set(CODES) <= set(cbk["code"].dropna()), "SF7 the codebook's Indexes sheet scores every headline index")
    alt = {}
    for code, name, item, kind, tol, th in P.INDEXES:
        v = s[item]
        if kind == "score":
            continue
        base = v.notna()
        y = v[base].isin(E.COUNTED[code]).astype(float) * 100
        t = s.loc[base]
        A = (t["letter"] == "A").values
        dw = (t["mode"] == "web").values[A].mean() - (t["mode"] == "web").values[~A].mean()
        alt[code] = (y.values[A].mean() - y.values[~A].mean()) / dw
    for code in P.SCORE:
        alt[code] = X["effects"][code]
    ok(band_from(alt)[0] == 4, "SF8 counting don't know, refused and prefer not to say in a percentage's base files 4")
    ok("points" in std and "percentage points" in std, "SF9 the tolerances carry their units")
    ok("d/100 times the index's mode effect" in std, "SF10 the artefact is d/100 times the mode effect")
    ok(pb["tsls"][0] == pb["wald"][0], "SF11 with or without the recorded characteristics as controls: the same band")
    ok("reference share" in std.lower(), "SF12 the reference share is filed and the band does not use it")
    ok(comp["the 9 to 12 August staff-entry interviews read as web"] is not None, "SF13 the outage interviews: same call")
    ok("aged 18 or over" in plan and "counts only when it comes from the person the letters ask for" in plan,
       "SF14 a complete comes only from the person the letters ask for, the household member aged 18 or over")
    wv = web[web["last_section"] == 6].copy()
    wv["address_id"] = iss.set_index("login_code").loc[wv["login_code"], "address_id"].values
    cv = cati[cati["RESULT"] == "C"].copy()
    twice = sorted(set(wv["address_id"]) & set(cv["ADDRESS_ID"]))
    paired = {}
    for code, name, item, kind, tol, th in P.INDEXES:
        a_ = wv.drop_duplicates("address_id").set_index("address_id").loc[twice, item]
        b_ = cv.drop_duplicates("ADDRESS_ID").set_index("ADDRESS_ID").loc[twice, item]
        keep = a_.isin(list(E.VALID[item])).values & b_.isin(list(E.VALID[item])).values
        a_, b_ = a_[keep].astype(float).values, b_[keep].astype(float).values
        if kind != "score":
            a_, b_ = np.isin(a_, E.COUNTED[code]) * 100.0, np.isin(b_, E.COUNTED[code]) * 100.0
        paired[code] = (a_ - b_).mean() if (a_ - b_).mean() != 0 else 1e-9
    ok(len(twice) == 345 and band_from(paired)[0] == 2 and "An address counts once" in plan,
       "SF15 the %d addresses answering twice, compared within household, would file %d: the plan counts an address "
       "once and MS-14 measures the effects on the test's completes" % (len(twice), band_from(paired)[0]))

    # ------------------------------------------------------------ the asks: devices and stops
    G = X["response"]
    edge = min(0.05 - abs(round(v["rate"], 1) - v["rate"]) for v in G.values())
    ok(edge >= 0.02, "ask 1: every response rate 0.02 or more inside its rounding bin (%.3f)" % edge)
    stops = {"the sample system's 1.1 codes": E.response(iss, s, "sms"),
             "eligible on the field codes alone": E.response(iss, s, "sms_codes_only"),
             "completes over field-coded eligible": E.response(iss, s, "mixed")}
    for name in ("returns giving an age under 18 kept", "the close read on the UTC date", "late returns kept (the close ignored)"):
        stops[name] = E.response(iss, comp[name])
    for name, r in stops.items():
        moved = sum(round(r[k]["rate"], 1) != round(G[k]["rate"], 1) for k in G)
        ok(moved == 4, "ask 1 stop %s moves all four rates (%d)" % (name, moved))
    r = E.response(iss, comp["the close at UTC+12 on 30 September"])
    moved = [k for k in G if round(r[k]["rate"], 1) != round(G[k]["rate"], 1)]
    ok(len(moved) >= 1 and all(k[0] == "2027Q3" for k in moved), "ask 1 stop UTC+12 at the third quarter's close moves %s"
       % moved)
    V = X["valid"]
    for name, sm in comp.items():
        vm = E.valid_by_mode(sm)
        moved = sum(vm[c][m] != V[c][m] for c in CODES for m in ("web", "cati"))
        need = 24 if name in ("the 9 to 12 August staff-entry interviews read as web", "the CATI clock read as UTC",
                              "the CATI clock read at UTC+12 all year", "both records of a twice-answered address kept") else 12
        ok(moved >= need, "ask 2 stop %s moves %d of 24 counts" % (name, moved))
    web2 = web.copy()
    web2["submitted_utc"] = web2["submitted_utc"].fillna(web2["last_saved_utc"])
    web2["last_section"] = 6
    allp = E.completes(iss, web2, cati)
    ok(sum(E.valid_by_mode(allp)[c]["web"] != V[c]["web"] for c in CODES) >= 9,
       "ask 2 stop partial returns counted moves the online counts of every section reached")
    rb = route_bands(pack_routes(allp))
    ok(rb["wald"][0] == 4, "R2 partial returns counted: the band stays 4")

    # ------------------------------------------------------------ the devices are real, fair and unmarked
    ev = o["R"].events
    staff_out = [e for e in ev if e["opened"] == "staff" and P.OUTAGE[0] <= e["utc"].astimezone(E.MT).date() <= P.OUTAGE[1]]
    ok(staff_out and all(e["mode"] == "cati" for e in staff_out),
       "device outage: every staff-opened return of 9 to 12 August is a telephone interview (%d)" % len(staff_out))
    ok(sum(1 for e in ev if e["opened"] == "staff" and e["mode"] == "web") >= 200,
       "device outage: staff-opened self-completions outside the window give the column a benign twin")
    teen = web[web["age"] < 18]
    ok(len(teen) >= 120 and teen["age"].between(15, 17).all(), "device under 18: %d returns aged 15 to 17" % len(teen))
    lock = iss[iss["final_outcome"].isin(["4.1", "4.2"]) & iss["address_id"].isin(s["address_id"])]
    ok(len(lock) == 144, "device locked codes: 144 field-coded ineligible addresses with a complete (%d)" % len(lock))
    close_q3 = E.close_utc("2027Q3")
    t = pd.to_datetime(web["submitted_utc"], utc=True)
    dst_hour = ((t > close_q3) & (t <= close_q3 + pd.Timedelta(hours=1))).sum()
    ok(dst_hour >= 15, "device clock: %d returns in the hour after the third quarter's close" % dst_hour)
    ok((t[t.notna()] <= pd.Timestamp("2027-10-10 23:59", tz="UTC")).all(), "H16 no web return after the extract")

    # ------------------------------------------------------------ separation: the call reads no device row
    gold = E.completes(iss, web, cati)
    locked_in = gold["address_id"].isin(iss.loc[iss["final_outcome"].isin(["4.1", "4.2"]), "address_id"]).sum()
    ok(locked_in == 144, "separation: the call's completes keep the locked addresses' completes (%d)" % locked_in)
    ok(len(set(teen["login_code"]) & set(iss.set_index("address_id").loc[gold["address_id"], "login_code"])) == 0,
       "separation: no under-18 return in the call's completes")

    # ------------------------------------------------------------ dates and distractors
    ok(pd.to_datetime(iss["outcome_date"]).max() <= pd.Timestamp("2027-10-11"), "H16 no outcome after the extract")
    calls = pd.read_csv(files["calls"])
    ok(pd.to_datetime(calls["CALL_TIME"]).max() <= pd.Timestamp("2027-09-30 23:59"), "H16 no call after the close")
    ct = pd.to_datetime(calls["CALL_TIME"]).dt.date
    ok(((ct >= P.OUTAGE[0]) & (ct <= P.OUTAGE[1])).sum() == 0, "the call records have the outage's gap")
    pub = pd.read_csv(files["published"])
    ok(pd.to_datetime(pub["released"]).max() <= pd.Timestamp("2027-10-20"), "H16 no release after the as-of date")
    ok(set(B.DISTRACTORS) == {"calls", "published"}, "distractors: the call records and the published series")

    # ------------------------------------------------------------ realism and the pack
    for k, f in files.items():
        if f.endswith((".csv", ".md")):
            txt = open(f, encoding="utf-8").read()
            ok("—" not in txt and "–" not in txt, "no dash in %s" % os.path.basename(f))
    ok("—" not in std + plan + close and "–" not in std + plan + close, "no dash in the documents")
    ok(len(files) >= 10 and len({f.rsplit(".", 1)[1] for f in files.values()}) >= 3 and len(iss) >= 25000,
       "input gates: %d files, formats %s, the issued sample %d rows" % (len(files), sorted({f.rsplit('.', 1)[1]
                                                                                            for f in files.values()}), len(iss)))
    return N[0]
