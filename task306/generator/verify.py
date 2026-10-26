"""Independent verifier: unzip target.zip into a scratch folder and recompute every graded figure from the bundle with
code that shares nothing with solve.py, then compare with figures.json and the write-up.

    python3 task306/generator/verify.py [target.zip]
"""
import calendar
import datetime as dt
import json
import os
import re
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def ym_add(d, k):
    y, m = d.year + (d.month - 1 + k) // 12, (d.month - 1 + k) % 12 + 1
    return dt.date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def call(T):
    reg = pd.read_csv(os.path.join(T, "rdw_gekentekende_voertuigen_20260630.csv"), dtype=str)
    log = pd.read_csv(os.path.join(T, "accuvervangingen_2014_2026.csv"), dtype=str)
    cv = pd.read_csv(os.path.join(T, "levensduurcurves_tractieaccu.csv"))
    from pypdf import PdfReader
    txt = " ".join(p.extract_text() for p in PdfReader(os.path.join(T, "garantievoorwaarden_tractieaccu_2026.pdf")).pages)
    plat = {"VOLTA": "Volta hatch", "KESTREL": "Kestrel SUV", "PLOVER": "Plover saloon", "MIRA": "Mira city car",
            "TERN": "Tern van"}
    years = {p: int(re.search(re.escape(p) + r"\s+(\d+)\s+years", txt).group(1)) for p in plat.values()}
    ages = cv["pakketleeftijd_jaar"].to_numpy(float)
    tab = {c: cv[c].to_numpy(float) for c in cv.columns[1:]}
    ref = cv.columns[-1]
    reg["p"] = reg["merk"].map(plat)
    reg["fa"] = pd.to_datetime(reg["datum_eerste_toelating"], format="%Y%m%d").dt.date
    reg["nl"] = pd.to_datetime(reg["datum_eerste_tenaamstelling_in_nederland"], format="%Y%m%d").dt.date
    log["k"] = log["kenteken"].str.replace("-", "", regex=False)
    log["d"] = pd.to_datetime(log["vervangdatum"]).dt.date
    log = log.sort_values(["k", "d"], kind="stable")
    by = {k: list(zip(g["d"], g["geplaatst_pakket"])) for k, g in log.groupby("k")}

    def wend(fa, p):
        try:
            return fa.replace(year=fa.year + years[p])
        except ValueError:
            return fa.replace(year=fa.year + years[p], day=28)

    def chance(start, curve, we, frm, worked):
        y0, y1 = dt.date(2027, 1, 1), dt.date(2028, 1, 1)
        lo = max(y0, frm, we)
        a0, a1, a_s = [(x - start).days / 365.25 for x in (lo, y1, worked)]
        if a1 <= a0:
            return 0.0
        F = lambda a: float(np.interp(a, ages, tab[curve]))
        return max(0.0, F(a1) - F(a0)) / max(1 - F(a_s), 1e-9)

    def pack(k, fa, p, before, strict):
        ev = [e for e in by.get(k, []) if (e[0] < before if strict else e[0] <= before)]
        if not ev:
            return fa, p
        d, kind = ev[-1]
        return d, (ref if kind == "Voltwerk revisie" else p)

    snap = dt.date(2026, 6, 30)
    fc = {p: 0.0 for p in plat.values()}
    for r in reg.itertuples():
        s, c = pack(r.kenteken, r.fa, r.p, snap, False)
        fc[r.p] += chance(s, c, wend(r.fa, r.p), snap, snap)
    base = dict(fc)
    win = reg[(reg.fa < reg.nl) & (reg.nl > dt.date(2025, 6, 30)) & (reg.nl <= snap)]
    months = [(2026, m) for m in range(7, 13)] + [(2027, m) for m in range(1, 13)]
    for r in win.itertuples():
        s, c = pack(r.kenteken, r.fa, r.p, r.nl, True)
        we = wend(r.fa, r.p)
        for y, m in months:
            arr = dt.date(y, m, min(r.nl.day, calendar.monthrange(y, m)[1]))
            off = arr - r.nl
            fc[r.p] += chance(s + off, c, we + off, arr, arr) / 12.0
    tot = sum(fc.values())
    raw = {p: 3000 * v / tot / 50 for p, v in fc.items()}
    fl = {p: int(np.floor(x)) for p, x in raw.items()}
    left = 60 - sum(fl.values())
    for p in sorted(raw, key=lambda p: raw[p] - fl[p], reverse=True)[:left]:
        fl[p] += 1
    return {p: 50 * v for p, v in fl.items()}, int(round(tot / 100) * 100), base


def asks(T):
    fy = lambda s: ("2025-07-01" <= s[:10] <= "2026-06-30")
    wo = pd.read_csv(os.path.join(T, "mes_werkorders_2025-26.csv"), dtype=str).set_index("werkorder")
    code = {"VH": "Volta hatch", "KS": "Kestrel SUV", "PS": "Plover saloon", "MC": "Mira city car", "TV": "Tern van"}
    st = pd.read_csv(os.path.join(T, "magazijn_mutaties_2025-26.csv"), dtype=str)
    st["aantal"] = st["aantal"].astype(int)
    rc = pd.read_csv(os.path.join(T, "magazijn_ontvangsten_2025-26.csv"), dtype=str)
    rc["aantal"] = rc["aantal"].astype(int)
    parts = pd.read_excel(os.path.join(T, "artikelstam_modules.xlsx")).set_index("artikelnummer")
    sh = pd.read_csv(os.path.join(T, "verzendingen_2025-26.csv"), dtype=str)
    sh = sh[sh["verzonden_op"].map(fy)]
    shipped = sh["werkorder"].map(lambda w: code[wo.loc[w, "platformcode"]]).value_counts()
    st = st[st["geboekt_op"].map(fy)].copy()
    over = set(st.groupby("partij")["aantal"].sum().loc[lambda s: s > rc.groupby("partij")["aantal"].sum()
                                                        .reindex(s.index).fillna(1e9)].index)
    st["mod"] = st["aantal"] * st["artikelnummer"].map(parts["modules_per_eenheid"])
    st["p"] = st["werkorder"].map(lambda w: code[wo.loc[w, "platformcode"]])
    rep = st[(st["soort"] == "UITGIFTE") & st["partij"].isin(over)]
    grp = rep.groupby(["picklijst", "partij", "aantal"])
    drop = []
    for _, g in grp:
        if len(g) >= 2:
            drop.extend(g.index[1:])
    a = st.drop(index=drop).groupby("p")["mod"].sum()
    A = {p: 50.0 * a[p] / shipped[p] for p in code.values()}
    eol = pd.read_csv(os.path.join(T, "eol_testlog_2025-26.csv"), dtype=str)
    bms = pd.read_csv(os.path.join(T, "mes_bms_koppelingen_2025-26.csv"), dtype=str)
    eol["wo"] = eol["pakket_id"].map(dict(zip(bms["bms_serienummer"], bms["werkorder"])))
    first = eol[eol["resultaat"] != "ABORT"].sort_values(["start", "run_id"]).groupby("wo").head(1)
    first = first[first["start"].map(fy)]
    first["p"] = first["programma"].str.split("-").str[1].map(code)
    B = (100.0 * first.groupby("p")["resultaat"].apply(lambda s: (s == "PASS").mean())).to_dict()
    ink = pd.read_csv(os.path.join(T, "kernen_inname_2025-26.csv"), dtype=str)
    ink = ink[ink["ontvangen_op"].map(fy)]
    ink["p"] = ink["label_platform"].str.split().str[0].map({"VOLTA": "Volta hatch", "KESTREL": "Kestrel SUV",
                                                             "PLOVER": "Plover saloon", "MIRA": "Mira city car",
                                                             "TERN": "Tern van"})
    built = set(wo["kerncode"])
    ink["rej"] = (ink["keuring"] == "AFGEKEURD") & ~ink["kerncode"].isin(built)
    C = (100.0 * ink.groupby("p")["rej"].mean()).to_dict()
    return A, B, C


def texts(T):
    """every document the call or the asks lean on, read back through one extractor per format, each with a positive
    control from the writer's own text"""
    from pypdf import PdfReader
    import zipfile as zf
    out = {}
    for f in ("garantievoorwaarden_tractieaccu_2026.pdf", "rdw_extract_veldbeschrijving.pdf",
              "prijslijst_revisiepakketten_2026.pdf"):
        out[f] = " ".join(p.extract_text() for p in PdfReader(os.path.join(T, f)).pages)
    with zf.ZipFile(os.path.join(T, "tooling_plan_2027_draft.docx")) as z:
        x = z.read("word/document.xml").decode("utf-8")
    out["tooling_plan_2027_draft.docx"] = re.sub(r"\s+", " ", " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", x)))
    out["lijn_exports_toelichting.md"] = open(os.path.join(T, "lijn_exports_toelichting.md"), encoding="utf-8").read()
    for k in out:
        out[k] = re.sub(r"\s+", " ", out[k])
    return out


def sf_rows(T, fig, A):
    """SF25 to SF27 recomputed from the bundle with this file's own code: the projection cells the 2027 fleet's later
    registrations converge over (SF25), the pack-per-car readings (SF26) and the lot stock rule on ask A (SF27)"""
    bad = []
    reg = pd.read_csv(os.path.join(T, "rdw_gekentekende_voertuigen_20260630.csv"), dtype=str)
    log = pd.read_csv(os.path.join(T, "accuvervangingen_2014_2026.csv"), dtype=str)
    cv = pd.read_csv(os.path.join(T, "levensduurcurves_tractieaccu.csv"))
    from pypdf import PdfReader
    txt = " ".join(p.extract_text() for p in PdfReader(os.path.join(T, "garantievoorwaarden_tractieaccu_2026.pdf")).pages)
    plat = {"VOLTA": "Volta hatch", "KESTREL": "Kestrel SUV", "PLOVER": "Plover saloon", "MIRA": "Mira city car",
            "TERN": "Tern van"}
    years = {p: int(re.search(re.escape(p) + r"\s+(\d+)\s+years", txt).group(1)) for p in plat.values()}
    ages = cv["pakketleeftijd_jaar"].to_numpy(float)
    tab = {c: cv[c].to_numpy(float) for c in cv.columns[1:]}
    ref = cv.columns[-1]
    reg["p"] = reg["merk"].map(plat)
    reg["fa"] = pd.to_datetime(reg["datum_eerste_toelating"], format="%Y%m%d").dt.date
    reg["nl"] = pd.to_datetime(reg["datum_eerste_tenaamstelling_in_nederland"], format="%Y%m%d").dt.date
    log["d"] = pd.to_datetime(log["vervangdatum"]).dt.date
    log["k"] = log["kenteken"].str.replace("-", "", regex=False)
    by = {k: sorted(zip(g["d"], g["geplaatst_pakket"])) for k, g in log.groupby("k")}
    y0, y1, snap = dt.date(2027, 1, 1), dt.date(2028, 1, 1), dt.date(2026, 6, 30)

    def wend(fa, p):
        try:
            return fa.replace(year=fa.year + years[p])
        except ValueError:
            return fa.replace(year=fa.year + years[p], day=28)

    def F(curve, a):
        return float(np.interp(a, ages, tab[curve]))

    def p27(start, curve, we, frm):
        lo = max(y0, frm, we)
        a0, a1, a_s = (lo - start).days / 365.25, (y1 - start).days / 365.25, (frm - start).days / 365.25
        return 0.0 if a1 <= a0 else max(0.0, F(curve, a1) - F(curve, a0)) / max(1 - F(curve, a_s), 1e-9)

    def pack(k, fa, p, before, strict):
        ev = [e for e in by.get(k, []) if (e[0] < before if strict else e[0] <= before)]
        return (fa, p) if not ev else (ev[-1][0], ref if ev[-1][1] == "Voltwerk revisie" else p)

    def split(fc):
        tot = sum(fc.values())
        raw = {p: 3000 * v / tot / 50 for p, v in fc.items()}
        fl = {p: int(np.floor(x)) for p, x in raw.items()}
        for p in sorted(raw, key=lambda p: raw[p] - fl[p], reverse=True)[:60 - sum(fl.values())]:
            fl[p] += 1
        return {p: 50 * v for p, v in fl.items()}, int(round(tot / 100) * 100)

    base, start_of_day = {p: 0.0 for p in plat.values()}, {p: 0.0 for p in plat.values()}
    for r in reg.itertuples():
        s, c = pack(r.kenteken, r.fa, r.p, snap, False)
        base[r.p] += p27(s, c, wend(r.fa, r.p), snap)
        s, c = pack(r.kenteken, r.fa, r.p, snap, True)
        start_of_day[r.p] += p27(s, c, wend(r.fa, r.p), snap)
    imp = reg[reg.fa < reg.nl]
    horizon = [(2026, m) for m in range(7, 13)] + [(2027, m) for m in range(1, 13)]

    def window(months):
        return imp[(imp.nl > ym_add(snap, -months)) & (imp.nl <= snap)]

    def carry(win, rate_months, placing):
        out = {p: 0.0 for p in plat.values()}
        for r in win.itertuples():
            s, c = pack(r.kenteken, r.fa, r.p, r.nl, True)
            we = wend(r.fa, r.p)
            for when, w in placing(r):
                off = when - r.nl
                out[r.p] += w / rate_months * p27(s + off, c, we + off, when)
        return out

    same_day = lambda r: [(dt.date(y, m, min(r.nl.day, calendar.monthrange(y, m)[1])), 1.0) for y, m in horizon]
    mid_month = lambda r: [(dt.date(y, m, 15), 1.0) for y, m in horizon]
    mid_quarter = lambda r: [(dt.date(y, m, 15), 3.0) for y, m in horizon if m % 3 == 2]
    later = lambda r: [(d, 12.0) for d in (ym_add(r.nl, 12), ym_add(r.nl, 24)) if snap < d < y1]
    cells = {"trailing 6 months": carry(window(6), 6, same_day), "trailing 24 months": carry(window(24), 24, same_day),
             "trailing 36 months": carry(window(36), 36, same_day), "trailing 12 months, mid-month": carry(window(12), 12, mid_month),
             "trailing 12 months by quarter, mid-quarter": carry(window(12), 12, mid_quarter),
             "the last 12 months replayed": carry(window(12), 12, later)}
    gold = carry(window(12), 12, same_day)
    for k, a in cells.items():
        slots, total = split({p: base[p] + a[p] for p in base})
        if slots != fig["slots"] or total != fig["total"]:
            bad.append("SF25 %s files %s and %d" % (k, slots, total))
    reg_slots, reg_total = split(base)
    if reg_slots != fig["register_only"]["slots"] or reg_slots == fig["slots"]:
        bad.append("SF25 the register-only reading files %s" % reg_slots)
    if int(round(sum(base.values()))) != fig["base_total"] or int(round(sum(start_of_day.values()))) == fig["base_total"]:
        bad.append("SF26 the register's figure %.1f, at the start of 30 June %.1f" % (sum(base.values()), sum(start_of_day.values())))
    if split({p: start_of_day[p] + gold[p] for p in base}) != (fig["slots"], fig["total"]):
        bad.append("SF26 the start-of-day reading of 30 June moves the call")
    # SF27: running stock by lot, receipts first on their day
    st = pd.read_csv(os.path.join(T, "magazijn_mutaties_2025-26.csv"), dtype=str)
    st["aantal"] = st["aantal"].astype(int)
    rc = pd.read_csv(os.path.join(T, "magazijn_ontvangsten_2025-26.csv"), dtype=str)
    rc["aantal"] = rc["aantal"].astype(int)
    if rc["partij"].duplicated().any():
        bad.append("SF27 a lot with two receipt rows")
    got = dict(zip(rc["partij"], rc["aantal"]))
    day = dict(zip(rc["partij"], rc["datum"]))
    rep = st[(st["soort"] == "UITGIFTE")].groupby(["picklijst", "partij", "aantal"]).filter(lambda g: len(g) >= 2)

    if (st[st["partij"].isin(got)]["geboekt_op"].str[:10] < st[st["partij"].isin(got)]["partij"].map(day)).any():
        bad.append("SF27 a line booked against a lot before the lot was received")

    def below(collapse):
        out = set()
        for lot, g in st[st["partij"].isin(got)].sort_values("geboekt_op", kind="stable").groupby("partij"):
            if collapse:
                dup = rep[rep["partij"] == lot]
                g = g.drop(index=[i for _, h in dup.groupby(["picklijst", "aantal"]) for i in h.index[1:]])
            if (got[lot] - g["aantal"].cumsum()).min() < 0:
                out.add(lot)
        return out

    low = below(False)
    if len(low) != 8 or below(True) & low:
        bad.append("SF27 lots below zero as written %s; after counting each repeated quantity once %s" % (sorted(low), sorted(below(True) & low)))
    wo = pd.read_csv(os.path.join(T, "mes_werkorders_2025-26.csv"), dtype=str).set_index("werkorder")
    code = {"VH": "Volta hatch", "KS": "Kestrel SUV", "PS": "Plover saloon", "MC": "Mira city car", "TV": "Tern van"}
    parts = pd.read_excel(os.path.join(T, "artikelstam_modules.xlsx")).set_index("artikelnummer")
    sh = pd.read_csv(os.path.join(T, "verzendingen_2025-26.csv"), dtype=str)
    sh = sh[(sh["verzonden_op"] >= "2025-07-01") & (sh["verzonden_op"] <= "2026-06-30")]
    shipped = sh["werkorder"].map(lambda w: code[wo.loc[w, "platformcode"]]).value_counts()
    fy = st[(st["geboekt_op"].str[:10] >= "2025-07-01") & (st["geboekt_op"].str[:10] <= "2026-06-30")].copy()
    tot = fy.groupby("partij")["aantal"].sum()
    k = {lot: got[lot] / tot[lot] for lot in low}
    fy["mod"] = fy["aantal"] * fy["partij"].map(lambda x: k.get(x, 1.0)) * fy["artikelnummer"].map(parts["modules_per_eenheid"])
    capped = fy.groupby(fy["werkorder"].map(lambda w: code[wo.loc[w, "platformcode"]]))["mod"].sum()
    for p in code.values():
        if abs(50.0 * capped[p] / shipped[p] - A[p]) > 1e-9:
            bad.append("SF27 %s brought back to its receipts %.3f against %.3f" % (p, 50.0 * capped[p] / shipped[p], A[p]))
    return bad


CONTROLS = {
    "tooling_plan_2027_draft.docx": ["in calendar 2027", "largest-remainder rule", "read by straight lines",
                                     "taken to stay in use", "whether or not our own warranty still covers it",
                                     "those first registered here from 1 July 2026 to the end of 2027",
                                     "at the end of 30 June 2026", "a pack fitted in its place later is left out"],
    "garantievoorwaarden_tractieaccu_2026.pdf": ["wherever in the EU", "does not start a new period",
                                                 "Mira city car 5 years"],
    "rdw_extract_veldbeschrijving.pdf": ["first admitted to the road", "first registered to a holder in the Netherlands"],
    "lijn_exports_toelichting.md": ["an aborted run is no test of the pack", "the date on the quarantine tag",
                                    "carries a negative quantity", "no lot's stock goes below zero",
                                    "one row per supplier lot"],
    "prijslijst_revisiepakketten_2026.pdf": ["price list 2026"],
}


def main(zpath=None):
    zpath = zpath or os.path.join(TASK, "target.zip")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(zpath) as z:
            z.extractall(tmp)
        T = os.path.join(tmp, "target") if os.path.isdir(os.path.join(tmp, "target")) else tmp
        slots, total, _ = call(T)
        A, B, C = asks(T)
        docs = texts(T)
        rows = sf_rows(T, fig, A)
    bad = list(rows)
    for f, needles in CONTROLS.items():
        if not docs.get(f):
            bad.append("%s reads back empty" % f)
        for s in needles:
            if s not in docs.get(f, ""):
                bad.append("%s lacks %r" % (f, s))
    if slots != fig["slots"]:
        bad.append("slots %s" % slots)
    if total != fig["total"]:
        bad.append("total %s" % total)
    for p in slots:
        if int(round(A[p])) != fig["ask_a"][p]:
            bad.append("ask A %s %.3f" % (p, A[p]))
        if round(B[p], 1) != fig["ask_b"][p]:
            bad.append("ask B %s %.3f" % (p, B[p]))
        if round(C[p], 1) != fig["ask_c"][p]:
            bad.append("ask C %s %.3f" % (p, C[p]))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    for p, v in fig["slots"].items():
        if "%s: %s" % (p, "{:,}".format(v)) not in sub:
            bad.append("write-up lacks %s %s" % (p, v))
    if bad:
        print("VERIFY FAIL: " + "; ".join(bad))
        return 1
    print("verify: the bundle recomputes every graded figure (slots, total, 15 ask figures); %d documents read back with "
          "their filed sentences; SF25 six projection cells, SF26 the start-of-day reading and SF27 the lot stock rule "
          "recomputed" % len(CONTROLS))
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
