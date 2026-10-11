"""Assertions over the built pack and the goldens: the call, every rung by name with its 25 per cent margins, the
answer grid cell by cell with its variants, the evidence the pack carries, every ask figure (rounding edges, ties,
bands) and every ask stop, mess neutrality, MG-02's wording, the banned vocabulary, the pack gates, containers,
dates, people and invented names. Everything is computed from target/ and golden/ through golden.py, plus the
simulated world where an assertion is about the world itself."""
import datetime as dt
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

import numpy as np
import openpyxl
import pandas as pd
import pdfplumber

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A    # noqa: E402
import build as B       # noqa: E402
import golden as G      # noqa: E402
import models as M      # noqa: E402
import sim as S         # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)
N_ASSERT = [0]
LOG = []
ASOF = "2026-10-13"


def ok(cond, msg):
    N_ASSERT[0] += 1
    if not cond:
        raise AssertionError(msg)


L2C = {b["label"]: b["code"] for b in W.BORES}
C2L = {v: k for k, v in L2C.items()}


def codes(*labels):
    return sorted(L2C[x] for x in labels)


ANSWER = codes("CM1", "CM2", "CM3", "CM4", "A1")
RUNG_SETS = {
    "R1 decline from the baseline assessment": codes("A1", "A2", "A3", "A4", "A5", "A6", "A7", "B4"),
    "R1b decline from the June 2022 level": codes("A1", "A2", "A3", "A4", "A5", "A6", "A7", "B4"),
    "R1b decline from the 2012 to 2022 mean": codes("A1", "A2", "A3", "A4", "A5", "A6", "A7", "B4"),
    "R2 less the reference bores' change, pooled": codes("A1"),
    "R2 less the reference bores' change, matched by unit": codes("A1"),
    "R2b pre-July 2022 trend extrapolated, from 2017": codes("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "B4"),
    "R2b pre-July 2022 trend extrapolated, from 2012": codes("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "B4"),
    "R3 one rainfall-departure window for every bore, 12 months": codes("A1"),
    "R3 one rainfall-departure window for every bore, 3 years": codes("A1"),
}
COMPLAINANTS = codes("A2", "A3", "A5", "B4")
OFFERS = {"Yarrowmere Pastoral Co Pty Ltd": codes("CM1", "CM3"), "Tondara Grazing Pty Ltd": codes("CM2"),
          "Bluebush Downs Pty Ltd": codes("CM4"), "Cypress Ridge Pastoral Trust": codes("A1")}
# the shipped ask figures (printed rounding); a change here is a moved answer and fails the build
EXPECT = {  # label: (September 2026 level m AHD, change since baseline m, decline caused by the mine m, impaired)
    "CM1": (207.77, -2.44, 8.9, True), "CM2": (195.44, -2.46, 8.4, True), "CM3": (214.47, -2.49, 9.3, True),
    "CM4": (203.49, -2.21, 8.2, True), "CM5": (209.84, 1.74, 2.4, False), "A1": (209.50, -8.78, 4.6, True),
    "A2": (209.51, -4.63, 0.8, False), "A3": (205.24, -5.23, 0.7, False), "A4": (204.86, -4.64, 0.5, False),
    "A5": (209.61, -4.84, 0.6, False), "A6": (201.27, -4.81, 0.4, False), "A7": (199.16, -4.69, 0.3, False),
    "A8": (202.33, -0.98, 0.2, False), "A9": (201.88, -0.87, 0.1, False), "B1": (238.12, -2.59, 1.1, False),
    "B2": (241.33, -3.02, 1.6, False), "B3": (243.13, -2.68, 0.9, False), "B4": (245.75, -8.70, 1.3, False)}
BANNED = re.compile(r"counterfactual|transfer function|response function|\bTFN\b|cumulative rainfall departure|\bCRD\b|"
                    r"climate[- ]adjusted|climate adjustment|deseasonali[sz]\w*|detrend\w*|recharge model|pastas|menyanthes|"
                    r"without the mine|would have been", re.I)
TOOLCHAIN = re.compile(r"python-docx|python-pptx|openpyxl|reportlab|matplotlib|pandas|numpy|pyarrow|distractor|"
                       r"\bclaude\b|anthropic|lorem|placeholder|\bseed\b|\bsimulat\w*|\bsynthetic\b", re.I)
# real Queensland coal mines and mining companies an invented name must not sit near (H21)
REAL = ["goonyella", "riverside", "broadmeadow", "moranbah", "grosvenor", "peak downs", "saraji", "norwich park",
        "caval ridge", "daunia", "poitrel", "isaac plains", "carborough", "coppabella", "moorvale", "millennium",
        "eagle downs", "burton", "hail creek", "south walker", "lake vermont", "middlemount", "olive downs", "foxleigh",
        "german creek", "oaky creek", "kestrel", "crinum", "gregory", "blackwater", "curragh", "yarrabee", "jellinbah",
        "ensham", "minerva", "rolleston", "kogan", "newlands", "collinsville", "sonoma", "byerwen", "carmichael",
        "kevin's corner", "alpha", "clermont", "blair athol", "red hill", "ironbark", "vulcan", "winchester south",
        "isaac downs", "teviot", "wollombi", "mavis downs", "bowen gas", "bhp", "bma", "anglo", "glencore", "peabody",
        "whitehaven", "stanmore", "coronado", "yancoal", "new hope", "bowen coking", "pembroke", "fitzroy", "jellinbah",
        "qcoal", "adani", "bravus", "sojitz", "idemitsu", "mitsui", "thiess", "macmahon", "bucyrus", "magnetic south",
        "baralaba", "cook colliery", "callide", "meandu", "dawson", "moura", "cameby downs", "new acland", "wilkie creek"]
INVENTED = ["kelvale", "tarrabool", "mundoora", "yarrowmere", "tondara", "bluebush downs", "kurrajong park", "cypress ridge",
            "saltbush flat", "brolga plains", "wilga vale", "ghost gum", "lancewood flat", "bellbird downs",
            "coolibah springs", "gidgee creek", "bottletree"]


def edge_distance(x, places):
    u = x * 10 ** places
    return abs((u - math.floor(u)) - 0.5)


def lev(a, b):
    """Edit distance."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


# ------------------------------------------------------------------ text of the shipped files

def file_text(path):
    if path.endswith(".pdf"):
        with pdfplumber.open(path) as p:
            return "\n".join(pg.extract_text() or "" for pg in p.pages)
    if path.endswith(".xlsx"):
        wb = openpyxl.load_workbook(path, read_only=True)
        return "\n".join(str(v) for ws in wb.worksheets for row in ws.iter_rows(values_only=True) for v in row
                         if v is not None) + "\n" + "\n".join(ws.title for ws in wb.worksheets)
    if path.endswith(".docx"):
        from docx import Document
        d = Document(path)
        out = [p.text for p in d.paragraphs]
        for t in d.tables:
            out += [c.text for r in t.rows for c in r.cells]
        return "\n".join(out)
    if path.endswith(".parquet"):
        import pyarrow.parquet as pq
        t = pq.read_table(path, columns=["logger_serial"])
        return "logger_serial timestamp_utc pressure_kpa temperature_c\n" + "\n".join(sorted(set(t.column(0).to_pylist())))
    if path.endswith(".csv"):
        df = pd.read_csv(path, dtype=str, keep_default_na=False)
        return " ".join(df.columns) + "\n" + "\n".join(str(x) for c in df.columns if df[c].map(len).max() < 400
                                                        for x in df[c].unique() if not re.fullmatch(r"[-\d.:TZ ]+", x))
    return open(path, encoding="utf-8", errors="ignore").read()


# ------------------------------------------------------------------ the checks

def run(target, golden_dir, world=None, meta_path=None, quiet=False):
    g = G.solve(target, with_grid=True)
    obs, LH, bores = g["obs"], g["LH"], g["bores"]
    trig = {k: A.TRIGGER[obs[k]["cls"]] for k in LH}

    # ---------------------------------------------------------------- the call and the ladder
    ok(g["answer"] == ANSWER, "answer moved: %s" % [C2L[x] for x in g["answer"]])
    ok(len(LH) == 18 and sorted(g["REF"]) == codes("RA1", "RA2", "RB1"), "18 register bores and three reference bores")
    ok(g["complainants"] == sorted(COMPLAINANTS, key=lambda k: bores[k]["complaint"]), "rung 0: the four complaints")
    ok(not set(g["complainants"]) & set(g["answer"]), "rung 0: no complainant's bore is in the answer")
    LOG.append("R0 the complaints -> %s (none impaired)" % ", ".join(C2L[k] for k in g["complainants"]))
    for name, vals in g["rungs"].items():
        s = A.designate(vals, obs)
        ok(s == RUNG_SETS[name], "%s gives %s" % (name, [C2L[x] for x in s]))
        ok(s != ANSWER, "%s gives the answer" % name)
        bad = A.margin_ok(vals, obs)
        ok(not bad, "%s: within 25 per cent of a trigger: %s" % (name, {C2L[k]: v for k, v in bad.items()}))
        thin = min((abs(vals[k] / trig[k] - 1), C2L[k]) for k in LH)
        LOG.append("%s -> %s (thinnest %.2f of trigger, %s)" % (name, ", ".join(C2L[x] for x in s), thin[0], thin[1]))
    r1 = g["rungs"]["R1 decline from the baseline assessment"]
    ok(all(r1[L2C[x]] >= 2.5 for x in ("A2", "A3", "A4", "A5", "A6", "A7")), "rung 1: A2 to A7 fell 2.5 m or more")
    ok(r1[L2C["B4"]] >= 6.25 and all(r1[L2C[x]] <= 3.75 for x in ("CM1", "CM2", "CM3", "CM4")), "rung 1: B4 and CM")
    ok(all(1.5 <= r1[L2C[x]] <= 3.5 for x in ("CM1", "CM2", "CM3", "CM4")), "coal-measure bores fell 1.5 to 3.5 m")
    ok(len({tuple(v) for v in RUNG_SETS.values()} | {tuple(ANSWER), tuple(sorted(COMPLAINANTS))}) == 5,
       "five distinct sets on the ladder (rungs 2 and 3 share A1 alone)")
    LOG.append("R4 each bore's own response (answer) -> %s" % ", ".join(C2L[x] for x in g["answer"]))

    # ---------------------------------------------------------------- the grid, cell by cell, and the variants
    cl = g["cl"]
    summary = {}
    bands = {k: [np.inf, -np.inf] for k in LH}
    settings = [("base", g["grid"], obs)]
    for vname, kw, rule in (("assessment level as the last static September reading", {}, "last"),
                            ("pumped dips removed by the robust outlier rule", {"pumped": "outlier"}, "mean"),
                            ("the 2012 to 2014 feet record dropped", {"drop_feet": True}, "mean")):
        o2 = G.observations(target, **kw)[0] if kw else obs
        settings.append((vname, A.grid(o2, LH, cl, level_rule=rule), o2))
    for vname, grid, o2 in settings:
        ok(len(grid) == 40, "grid size %d" % len(grid))
        for cell, vals in sorted(grid.items()):
            s = A.designate(vals, o2)
            ok(s == ANSWER, "%s cell %s gives %s" % (vname, cell, [C2L[x] for x in s]))
            bad = A.margin_ok(vals, o2)
            ok(not bad, "%s cell %s margins %s" % (vname, cell, {C2L[k]: v for k, v in bad.items()}))
            for k in LH:
                m_ = (vals[k] / trig[k] - 1) if k in ANSWER else (1 - vals[k] / trig[k])
                key = (vname, cell[0])
                if key not in summary or m_ < summary[key][0]:
                    summary[key] = (m_, C2L[k], round(vals[k], 2), cell)
                if vname == "base":
                    bands[k][0] = min(bands[k][0], vals[k])
                    bands[k][1] = max(bands[k][1], vals[k])
    for (vname, fam), (m_, lab, v, cell) in sorted(summary.items()):
        LOG.append("grid %s, %s: 8 cells, 0 misses, thinnest %.3f of trigger (%s %.2f in %s)" % (
            vname, fam, m_, lab, v, "/".join(cell)))
    g["grid_summary"] = summary
    g["bands"] = bands
    for k in LH:
        ok(bands[k][0] <= g["drawdown"][k] <= bands[k][1], "golden drawdown inside its band at %s" % C2L[k])
        r1k = g["rungs"]["R1 decline from the baseline assessment"][k]
        ok(not (bands[k][0] <= r1k <= bands[k][1]), "the baseline decline at %s sits inside its band" % C2L[k])
    LOG.append("drawdown bands (40 cells): " + "; ".join("%s %.1f to %.1f" % (C2L[k], bands[k][0], bands[k][1]) for k in
                                                         sorted(LH, key=lambda c: list(EXPECT).index(C2L[c]))))

    # ---------------------------------------------------------------- evidence the pack carries
    ev = G.evidence(g)
    g["evidence"] = ev
    for k in codes("CM1", "CM2", "CM3", "CM4"):
        ok(0.5 <= ev["rise_2021_22"][k] <= 1.0, "%s rising 0.5 to 1 m a year since 2021: %.2f" % (C2L[k], ev["rise_2021_22"][k]))
    for k, v in ev["ref_tracking_max_abs"].items():
        ok(v <= 0.5, "the per-bore model tracks reference bore %s within 0.5 m (%.2f)" % (C2L[k], v))
    for k, v in ev["mine_coal_decline"].items():
        ok(20 <= v <= 40, "the cone at %s: %.1f m" % (C2L[k], v))
    LOG.append("evidence: coal-measure rise 2021-22 %s m/yr; reference tracking max %s m; mine coal-measure bores fell %s m" % (
        ", ".join("%s %.2f" % (C2L[k], v) for k, v in sorted(ev["rise_2021_22"].items())),
        ", ".join("%s %.2f" % (C2L[k], v) for k, v in sorted(ev["ref_tracking_max_abs"].items())),
        ", ".join("%s %.1f" % (C2L[k], v) for k, v in sorted(ev["mine_coal_decline"].items()))))

    # ---------------------------------------------------------------- the asks
    printed = {}
    for k in LH:
        lab = C2L[k]
        L, C, Dd, imp = g["levels"][k], g["change"][k], g["drawdown"][k], g["impaired"][k]
        e = EXPECT[lab]
        ok((round(L, 2), round(C, 2), round(Dd, 1), imp) == e, "ask figures moved at %s: %s" % (
            lab, (round(L, 2), round(C, 2), round(Dd, 1), imp)))
        ok(edge_distance(L, 2) >= 0.15 and edge_distance(C, 2) >= 0.15 and edge_distance(Dd, 1) >= 0.15,
           "%s: a graded figure near a rounding edge (%.4f, %.4f, %.3f)" % (lab, L, C, Dd))
        ok(Dd > 0.05, "%s drawdown prints positive" % lab)
        printed[k] = e
    for i in range(3):
        vals = [printed[k][i] for k in LH]
        ok(len(set(vals)) == len(vals), "a tie among the graded figures in column %d" % i)
    ok(g["offers"] == {o: sorted(v) for o, v in OFFERS.items()} or {o: sorted(v) for o, v in g["offers"].items()} == OFFERS,
       "offers moved: %s" % g["offers"])
    ok(len(g["offers"]) == 4, "four offers")
    LOG.append("edge distances (fraction of the last printed unit): levels min %.2f, changes min %.2f, drawdowns min %.2f" % (
        min(edge_distance(g["levels"][k], 2) for k in LH), min(edge_distance(g["change"][k], 2) for k in LH),
        min(edge_distance(g["drawdown"][k], 1) for k in LH)))

    # ---------------------------------------------------------------- ask stops
    stops = {}

    def stop(label, other, field, expect_moved):
        moved = {C2L[k] for k in LH if round(other[k], 2) != round(g[field][k], 2)}
        ok(moved == set(expect_moved), "ask stop '%s' moves %s, expected %s" % (label, sorted(moved), sorted(expect_moved)))
        stops[label] = {C2L[k]: (round(g[field][k], 2), round(other[k], 2)) for k in LH if C2L[k] in moved}
        LOG.append("ask stop, %s: %s" % (label, "; ".join("%s %.2f -> %.2f" % (k, a, b) for k, (a, b) in stops[label].items())))

    o_mp = G.observations(target, mp_history=False)[0]
    stop("measuring point history ignored", {k: A.assessment_level(o_mp[k]) - o_mp[k]["baseline"] for k in LH}, "change",
         ["CM2", "A6"])
    o_pump = G.observations(target, pumped="keep")[0]
    stop("pumped dips kept", {k: A.assessment_level(o_pump[k]) for k in LH}, "levels", ["CM4", "A5", "B1"])
    o_raw = G.observations(target, compensate=False)[0]
    logged = [k for k in LH if obs[k]["logger"] is not None]
    stop("loggers left uncompensated", {k: A.assessment_level(o_raw[k]) for k in LH}, "levels", [C2L[k] for k in logged])
    for k in logged:
        dlt = A.assessment_level(o_raw[k]) - g["levels"][k]
        ok(9.5 <= dlt <= 10.5, "uncompensated loggers move %s by about 10 m (%.2f)" % (C2L[k], dlt))
    last = {k: A.assessment_level(obs[k], "last") for k in LH}
    moved_last = [C2L[k] for k in LH if round(last[k], 2) != round(g["levels"][k], 2)]
    stop("the last reading instead of the September mean", last, "levels", moved_last)
    ok(len(moved_last) >= 12, "the last reading moves most September levels")
    o_utc = G.observations(target, day_basis="utc")[0]
    stop("UTC days instead of Queensland days", {k: A.assessment_level(o_utc[k]) for k in LH}, "levels", ["A1", "B4"])
    o_981 = G.observations(target, density=9.81)[0]
    moved_981 = [C2L[k] for k in LH if round(A.assessment_level(o_981[k]), 2) != round(g["levels"][k], 2)]
    LOG.append("9.81 kPa per metre instead of the notes' 9.80665: moves the printed level at %s" % (", ".join(moved_981) or "no bore"))
    g["stops"] = stops

    # ---------------------------------------------------------------- mess neutrality of the main call
    neutral = {}
    for label, kw in (("measuring point history ignored", dict(mp_history=False)),
                      ("duplicate dips kept", dict(dedupe=False)),
                      ("pumped dips kept", dict(pumped="keep")),
                      ("the feet record read as metres", dict(feet=False)),
                      ("the 2012 to 2014 rounds dropped (registered numbers not mapped)", dict(drop_feet=True)),
                      ("UTC days for the loggers", dict(day_basis="utc")),
                      ("loggers left uncompensated", dict(compensate=False))):
        o2 = G.observations(target, **kw)[0]
        dd = {k: A.cell(o2, k, cl, *G.PRIMARY)[0] for k in LH}
        s = sorted(k for k in LH if dd[k] > trig[k])
        neutral[label] = (s, [C2L[x] for x in s])
        recorded = label in ("pumped dips kept", "loggers left uncompensated", "the feet record read as metres")
        if not recorded:
            ok(s == ANSWER, "the main call moves under '%s': %s" % (label, [C2L[x] for x in s]))
        LOG.append("mess, %s: main call %s" % (label, "unchanged" if s == ANSWER else "moves to %s" % [C2L[x] for x in s]))
    g["neutral"] = neutral
    dips_all = G.observations(target, pumped="keep")[4]
    sep_rows = dips_all[(dips_all["reading_date"] >= "2026-09-01") & (dips_all["reading_date"] <= "2026-09-30")]
    ok(sorted(C2L[c] for c in sep_rows.loc[sep_rows["pump_remark"], "code"]) == ["A5", "B1", "CM4"],
       "three pumped dips in September 2026")
    ok((sep_rows["pump_remark"] == sep_rows["pump_outlier"]).all(), "the remark and the outlier rule agree in September 2026")
    LOG.append("pumped dips: %d flagged by remark, %d by the outlier rule, %d by both" % (
        int(dips_all["pump_remark"].sum()), int(dips_all["pump_outlier"].sum()),
        int((dips_all["pump_remark"] & dips_all["pump_outlier"]).sum())))

    # ---------------------------------------------------------------- the world behind the pack
    if world is not None:
        hd = world["hd"]
        sep = slice(S.idx(dt.date(2026, 9, 1)), S.idx(dt.date(2026, 9, 30)) + 1)
        mar = slice(S.idx(dt.date(2026, 3, 1)), S.idx(dt.date(2026, 3, 31)) + 1)
        for lab in ("CM1", "CM2", "CM3", "CM4"):
            c = hd[lab]["climate"]
            ok(c[sep].mean() > c[mar].mean(), "%s: the climate path still rising in 2026" % lab)
            truth = hd[lab]["dd"][sep].mean()
            ok(abs(truth - g["drawdown"][L2C[lab]]) < 0.5, "%s: estimate near the true drawdown" % lab)
        LOG.append("world: true drawdown at September 2026 %s" % ", ".join(
            "%s %.2f" % (lab, hd[lab]["dd"][sep].mean()) for lab in ("CM1", "CM2", "CM3", "CM4", "CM5", "A1", "B4")))
        for lab in W.LANDHOLDER + W.REFERENCE + W.MINE_BORES:
            h = hd[lab]["h"][S.idx(dt.date(2012, 1, 1)):S.idx(dt.date(2026, 10, 6))]
            ok(h.max() < W.BY_LABEL[lab]["gl"] - 0.5, "%s: the water table stays below ground" % lab)

    # ---------------------------------------------------------------- MG-02 and the notes
    mg = " ".join(file_text(os.path.join(target, "MG-02_bore_assessment_and_make_good.pdf")).split())
    ok("A decline with another cause is not the mine's" in mg, "MG-02 4.1 says other declines are not the mine's")
    ok(not re.search(r"baseline[^.]{0,80}\b(less|minus|difference|compared)", mg, re.I), "MG-02 defines no decline from the baseline")
    ok(not re.search(r"\b(model|regression|reference bore|rainfall|climate|method)\b", mg, re.I), "MG-02 names no attribution method")
    ok("2 m for an unconsolidated aquifer and 5 m for a consolidated aquifer" in mg, "MG-02 3.1 triggers")
    notes = open(os.path.join(target, "monitoring_network_notes.md")).read()
    ok("9.80665" in notes and "9.80665" not in mg, "the compensation constant stated once, in the notes")
    reg = file_text(os.path.join(target, "landholder_bore_register.xlsx"))
    ok("2 m" not in reg and "5 m" not in reg, "the register does not restate the triggers")
    ok("holds no current water levels" in reg, "the register is labelled for the question it answers")

    # ---------------------------------------------------------------- vocabulary, every text-bearing file and the prompt
    prompt = open(os.path.join(TASK, "prompt.md")).read()
    texts = {f: file_text(os.path.join(target, f)) for f in sorted(os.listdir(target))}
    texts["../prompt.md"] = prompt
    for f, t in texts.items():
        hits = sorted(set(m_.group(0).lower() for m_ in BANNED.finditer(t)))
        ok(not hits, "%s carries %s" % (f, hits))
        ok("\u2014" not in t, "%s carries an em dash" % f)
        if f != "../prompt.md":
            tc = sorted(set(m_.group(0) for m_ in TOOLCHAIN.finditer(t)))
            ok(not tc, "%s carries toolchain or author words %s" % (f, tc))
    for f in os.listdir(golden_dir):
        gt = file_text(os.path.join(golden_dir, f))
        ok("\u2014" not in gt, "golden %s carries an em dash" % f)
        ok(not BANNED.search(gt), "golden %s carries banned vocabulary" % f)

    # ---------------------------------------------------------------- pack gates
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    ok(len(files) >= 10 and len(files) == 11, "file count %d" % len(files))
    ok(len(fmts) >= 3, "formats %s" % fmts)
    rows = {f: rows_of(os.path.join(target, f)) for f in files}
    ok(max(v for v in rows.values() if v) >= 25000, "a file of 25,000 rows or more")
    ok(not any(f.startswith(".") for f in files), "no dot files")
    g["pack"] = dict(files=len(files), formats=fmts, rows=rows)
    if meta_path and os.path.exists(meta_path):
        meta = json.load(open(meta_path))
        dis = meta["distractor_files"]
        ok(len(dis) == 2 and all(d_ in files for d_ in dis), "two distractors named in metadata.json and shipped")
        ok(sorted(x["path"] for x in meta["files"]) == files, "metadata.json lists exactly the shipped files")
        for d_ in dis:
            tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
            try:
                for f in files:
                    if f != d_:
                        shutil.copy(os.path.join(target, f), tmp)
                g2 = G.solve(tmp, with_grid=False)
                same = (g2["answer"] == g["answer"] and g2["offers"] == g["offers"]
                        and all(abs(g2[x][k] - g[x][k]) < 1e-12 for x in ("levels", "change", "drawdown") for k in LH)
                        and g2["complainants"] == g["complainants"])
                ok(same, "the golden reads %s" % d_)
            finally:
                shutil.rmtree(tmp)
        LOG.append("distractors %s: the golden recomputes unchanged without each" % ", ".join(dis))
    ok(sorted(os.listdir(golden_dir)) == ["bore_impact_assessment.xlsx", "make_good_recommendation.docx"], "the two deliverables")

    # ---------------------------------------------------------------- containers and dates
    sig = re.compile(rb"openpyxl|Openpyxl|ReportLab|reportlab|python-docx|python-pptx|matplotlib")
    for f in files + ["../golden/bore_impact_assessment.xlsx", "../golden/make_good_recommendation.docx"]:
        p = os.path.join(target, f)
        if f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(p) as z:
                meta_b = b"".join(z.read(n) for n in z.namelist() if n.startswith("docProps/"))
                stamps = {i.date_time for i in z.infolist()}
            ok(not sig.search(meta_b), "%s carries a writer signature" % f)
            ok(stamps == {(1980, 1, 1, 0, 0, 0)}, "%s zip stamps" % f)
            for m_ in re.findall(rb"\d{4}-\d\d-\d\dT", meta_b):
                ok(b"2012" <= m_[:4] <= b"2026", "%s stamp %s out of band" % (f, m_))
        if f.endswith(".pdf"):
            b = open(p, "rb").read()
            ok(not sig.search(b), "%s carries a writer signature" % f)
            ok(all(b"2026" == m_[2:6] for m_ in re.findall(rb"D:\d{14}", b)), "%s dates" % f)
    scrub = os.path.join(REPO, ".claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py")
    out = subprocess.run([sys.executable, scrub, target, "--floor", "2012-01-01", "--ceiling", "2026-10-09"],
                         capture_output=True, text=True).stdout
    ok("clean" in out, "producer audit: %s" % out.strip()[:200])
    late = {}
    for f in files:
        t = texts[f] if not f.endswith(".csv") else open(os.path.join(target, f)).read()
        for m_ in re.finditer(r"\b(20\d\d-\d\d-\d\d)\b", t):
            if m_.group(1) > ASOF:
                late.setdefault(f, set()).add(m_.group(1))
    ok(not late, "dates after the as-of date: %s" % late)
    import pyarrow.parquet as pq
    ts = pq.read_table(os.path.join(target, "logger_pressure_2015-2026.parquet"), columns=["timestamp_utc"]).column(0)
    ok(str(pd.Timestamp(ts.to_numpy().max())) <= "2026-10-06 23:59:59", "loggers end at the October downloads")
    dips = pd.read_csv(os.path.join(target, "water_level_dips_2012-2026.csv"), dtype=str)
    ok(dips["reading_date"].max() <= "2026-10-06" and dips["reading_date"].min() >= "2012-03-01", "dip dates")
    clim = pd.read_csv(os.path.join(target, "daily_climate_1990-2026.csv"), dtype=str)
    ok(clim["date"].iloc[0] == "1990-01-01" and clim["date"].iloc[-1] == "2026-09-30", "climate 1990 to 30 September 2026")
    take = pd.read_csv(os.path.join(target, "pit_dewatering_2022-2026.csv"), dtype=str)
    ok(take["date"].min() == "2022-07-04", "the take begins on 4 July 2022")
    ok(sorted(take.loc[take["source_id"].str.startswith("AD"), "date"].groupby(take["source_id"]).min())[0] >= "2023-03-01",
       "advance dewatering bores from March 2023")

    # ---------------------------------------------------------------- the climate is plausible for the region
    c = pd.read_csv(os.path.join(target, "daily_climate_1990-2026.csv"))
    c["wy"] = [int(d_[:4]) + (int(d_[5:7]) >= 10) for d_ in c["date"]]
    full = c[(c["wy"] >= 1991) & (c["wy"] <= 2026)]
    annual = full.groupby("wy")["rain_mm"].sum()
    ok(520 <= annual[annual.index <= 2022].mean() <= 680, "rainfall about 600 mm a year")
    ok(1650 <= full.groupby("wy")["morton_apet_mm"].sum().mean() <= 1900, "evaporation about 1,800 mm a year")
    mon = c.assign(m=[int(d_[5:7]) for d_ in c["date"]]).groupby("m")["rain_mm"].mean()
    ok(mon[[12, 1, 2, 3]].sum() > 2.2 * mon[[6, 7, 8, 9]].sum(), "summer-dominant rainfall")
    for y in (2023, 2024, 2025, 2026):
        ok(annual[y] < 0.7 * annual[annual.index <= 2022].mean(), "a failed season in %d" % y)
    for y in (2020, 2021):
        ok(annual[y] > 1.3 * annual[annual.index <= 2022].mean(), "a wet season in %d" % y)
    LOG.append("climate: mean annual rainfall to 2022 %.0f mm, evaporation %.0f mm; water years 2020 to 2026 %s" % (
        annual[annual.index <= 2022].mean(), full.groupby("wy")["morton_apet_mm"].sum().mean(),
        ", ".join("%d %.0f" % (y, annual[y]) for y in range(2020, 2027))))

    # ---------------------------------------------------------------- the goldens agree with the solve
    wb = openpyxl.load_workbook(os.path.join(golden_dir, "bore_impact_assessment.xlsx"), data_only=True)
    ws = wb["Assessment"]
    head = [c_.value for c_ in ws[4]]
    grows = [dict(zip(head, [c_.value for c_ in r])) for r in ws.iter_rows(min_row=5, max_row=22)]
    ok(len(grows) == 18 and all(r["Bore"] for r in grows), "the workbook has 18 rows")
    for r in grows:
        lab = C2L[r["Bore"]]
        e = EXPECT[lab]
        ok((r["September 2026 level (m AHD)"], r["Change since baseline (m)"], r["Decline caused by the mine (m)"],
            r["Impaired capacity"] == "Yes") == e, "workbook row %s" % lab)
    memo = file_text(os.path.join(golden_dir, "make_good_recommendation.docx"))
    ok("Stephen Anderson" in memo and "four offers" in memo, "the memo names the general manager and the count")
    for owner, bs in OFFERS.items():
        ok(owner in memo and all(b_ in memo for b_ in bs), "the memo names %s and its bores" % owner)
    for k in COMPLAINANTS:
        e = EXPECT[C2L[k]]
        ok(("%.2f m" % abs(e[1])) in memo and ("%.1f m" % e[2]) in memo and bores[k]["name"] in memo,
           "the memo tells %s's owner what lowered it" % C2L[k])
    ok(re.search(r"tracked to within 0\.[1-5] m", memo), "the memo's tracking claim")

    # ---------------------------------------------------------------- people and invented names
    people = set(W.PEOPLE.values())
    sys.path.insert(0, os.path.join(REPO, ".claude/skills/fingerprint"))
    try:
        import business
        found = set()
        for f in files + ["../golden/make_good_recommendation.docx", "../golden/bore_impact_assessment.xlsx", "../prompt.md"]:
            p = os.path.join(target, f)
            found |= {"%s %s" % x for x in business.people_in_text(file_text(p))}
        ok(found <= people, "personas outside the card: %s" % (found - people))
        LOG.append("personas in the pack and goldens: %s" % ", ".join(sorted(found)))
    except ImportError:
        pass
    for name in INVENTED:
        core = re.sub(r"\b(downs|park|ridge|flat|plains|vale|springs|creek)\b", "", name).strip()
        for real in REAL:
            rcore = re.sub(r"\b(downs|park|ridge|flat|plains|vale|springs|creek)\b", "", real).strip()
            if not core or not rcore:
                continue
            ok(lev(core, rcore) > 2 and core not in rcore and rcore not in core,
               "invented name %r sits near the real %r (H21)" % (name, real))

    sub = os.path.join(TASK, "submission.md")
    if os.path.exists(sub):
        check_submission(open(sub).read(), g)
    if not quiet:
        for line in LOG:
            print("  " + line)
    print("checks: %d assertions passed" % N_ASSERT[0])
    return N_ASSERT[0], LOG, g


def check_submission(text, g):
    """Every figure the write-up owes is the solve's own, and every figure in its components and steps recomputes."""
    ok("\u2014" not in text, "submission carries an em dash")
    lh, ans = g["LH"], g["answer"]
    coal = [k for k in ans if g["obs"][k]["unit"] == "coal"]
    falls = ", ".join("%.2f" % -g["change"][k] for k in coal[:-1]) + " and %.2f" % -g["change"][coal[-1]]
    ok("fell only **%s m**" % falls in text, "component 1: %s" % falls)
    dds = ", ".join("%.1f" % g["drawdown"][k] for k in coal[:-1]) + " and %.1f" % g["drawdown"][coal[-1]]
    ok("at **%s m**" % dds in text, "component 2: %s" % dds)
    a1 = [k for k in ans if g["obs"][k]["unit"] == "alluvium"][0]
    ok("at %s at **%.1f m**" % (a1, g["drawdown"][a1]) in text, "component 2: %s" % a1)
    cps = g["complainants"]
    ok("**%s m**" % (", ".join("%.2f" % -g["change"][k] for k in cps[:-1]) + " and %.2f" % -g["change"][cps[-1]]) in text,
       "component 3 falls")
    ok("**%s m**" % (", ".join("%.1f" % g["drawdown"][k] for k in cps[:-1]) + " and %.1f" % g["drawdown"][cps[-1]]) in text,
       "component 3 shares")
    ok("held by **four** owners" in text and len(g["offers"]) == 4, "component 4")
    lo, hi = min(-g["change"][k] for k in coal), max(-g["change"][k] for k in coal)
    ok("fell only %.2f to %.2f m" % (lo, hi) in text, "step 3 range")
    dlo, dhi = min(g["drawdown"][k] for k in coal), max(g["drawdown"][k] for k in coal)
    ok("%.1f to %.1f m at the four coal-measure bores" % (dlo, dhi) in text, "step 5 and block 1 range")
    others = [k for k in lh if k not in ans]
    ok(max(g["drawdown"][k] for k in others) < 2.45 and "2.4 m or less at the other %d" % len(others) in text, "step 5 others")
    means = [g["fits"][k]["kernel"][1] / 365.25 for k in coal]
    ok(6.0 <= min(means) and max(means) < 7.0 and "over six to seven years" in text, "step 4 coal measures %s" % means)
    am = [g["fits"][k]["kernel"][1] / 365.25 for k in lh if g["obs"][k]["unit"] == "alluvium"]
    ok(0.35 <= min(am) and max(am) <= 0.65 and "about half a year" in text, "step 4 alluvium %s" % am)
    tr = max(g["evidence"]["ref_tracking_max_abs"].values())
    ok(tr <= 0.3 and "within 0.3 m" in text, "step 6 tracking %.3f" % tr)
    shares = [g["drawdown"][k] for k in cps]
    ok("%.1f to %.1f m" % (min(shares), max(shares)) in text, "block 1 complainants' shares")
    ok(text.count("\n## ") + text.startswith("## ") == 5 and "## Tags" in text and "## 4. Deliverable Answers" in text, "five blocks")
    ok(not BANNED.search(text), "submission carries banned vocabulary")
    for lab, (L, C, Dd, imp) in EXPECT.items():
        k = L2C[lab]
        line = [l_ for l_ in text.split("\n") if l_.strip().startswith("- %s " % k)]
        ok(len(line) == 1, "block 4 row for %s" % k)
        s = line[0]
        ok(("%.2f m AHD" % L) in s and (("%+.2f m" % C).replace("+", "+") in s or ("%.2f m" % C) in s)
           and ("%.1f m" % Dd) in s and (("yes" if imp else "no") in s.lower()), "block 4 figures for %s: %s" % (k, s))


def rows_of(path):
    if path.endswith(".csv"):
        with open(path) as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        import pyarrow.parquet as pq
        return int(pq.ParquetFile(path).metadata.num_rows)
    return None


if __name__ == "__main__":
    run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), meta_path=os.path.join(TASK, "metadata.json"))
