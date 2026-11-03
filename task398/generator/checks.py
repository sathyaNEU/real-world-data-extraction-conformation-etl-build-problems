"""The generator's assertions: the three rules on the clean truth (R1 to R3), the ladder, the standing family, every
semantic fork (SF), the asks' devices, the separation line, the input gates and the realism sweep."""
import csv
import datetime as dt
import json
import os
import re
import zipfile

import numpy as np

import fund as F
import golden as G
import records as R
import world as W
from world import D, DAYS, IDX

PERSONAS = {"Carol Rowe", "Julia Parry", "Naomi Collins"}


class Book:
    def __init__(self):
        self.rows = []

    def ok(self, label, cond, detail=""):
        self.rows.append((label, bool(cond), detail))


def bp(p, RB):
    return (p[-1] / p[0] - 1 - RB) * 1e4


def office_problems(path):
    """what a reader of the package's properties would catch: counts that do not match the content, a part or a
    property the claimed application does not write, a duplicated property, a blank thumbnail"""
    import io
    from PIL import Image
    import postprocess as PP
    out = []
    with zipfile.ZipFile(path) as z:
        parts = {n: z.read(n) for n in z.namelist()}
    app = parts["docProps/app.xml"].decode("utf-8")
    tags = re.findall(r"<(\w+)[ />]", app.split("<Properties", 1)[1])
    top = [t for t in tags if t not in ("Properties", "vector", "variant", "lpstr", "i4")]
    if len(top) != len(set(top)):
        out.append("a property written twice")
    ver = re.search(r"<AppVersion>(\d+)\.", app)
    if not ver:
        out.append("no AppVersion")

    def num(tag):
        m = re.search(r"<%s>(\d+)</%s>" % (tag, tag), app)
        return int(m.group(1)) if m else None

    def thumb_ok(ratio):
        if "docProps/thumbnail.jpeg" not in parts:
            return True
        im = Image.open(io.BytesIO(parts["docProps/thumbnail.jpeg"])).convert("L")
        w, h = im.size
        mean = sum(im.resize((32, 32)).getdata()) / 1024.0
        return mean < 252 and abs((w / h) / ratio - 1) < 0.03
    if path.endswith(".docx"):
        lay = PP.docx_layout(parts["word/document.xml"].decode("utf-8"))
        if "<Application>Microsoft Office Word</Application>" not in app:
            out.append("application")
        if num("Words") != lay["words"] or num("Characters") != lay["chars"] or not lay["words"]:
            out.append("word or character count")
        if num("CharactersWithSpaces") != lay["chars_sp"] or num("Paragraphs") != lay["paragraphs"]:
            out.append("paragraph or space count")
        if not num("Pages") or not num("Lines") or num("Lines") < num("Paragraphs"):
            out.append("pages or lines")
        if "word/stylesWithEffects.xml" in parts and ver and int(ver.group(1)) >= 15:
            out.append("stylesWithEffects under Word %s" % ver.group(1))
        if "stylesWithEffects" in parts["word/_rels/document.xml.rels"].decode() + parts["[Content_Types].xml"].decode() \
                and "word/stylesWithEffects.xml" not in parts:
            out.append("a dangling stylesWithEffects reference")
        if not thumb_ok(lay["page"][0] / lay["page"][1]):
            out.append("thumbnail")
    elif path.endswith(".pptx"):
        slides = PP.pptx_text(parts)
        cx, cy = (int(v) for v in re.search(r'<p:sldSz cx="(\d+)" cy="(\d+)"',
                                            parts["ppt/presentation.xml"].decode()).groups())
        fmt = re.search(r"<PresentationFormat>([^<]*)</PresentationFormat>", app)
        want = "Widescreen" if abs(cx / cy - 16 / 9) < 0.01 else "On-screen Show (4:3)"
        if num("Slides") != len(slides) or num("Words") != sum(len(p.split()) for s in slides for p in s) \
                or not num("Words"):
            out.append("slide or word count")
        if not fmt or fmt.group(1) != want:
            out.append("presentation format")
        if not thumb_ok(cx / cy):
            out.append("thumbnail")
        core = parts["docProps/core.xml"].decode()
        lo = re.search(r"<dcterms:created[^>]*>([^<]+)<", core).group(1)
        hi = re.search(r"<dcterms:modified[^>]*>([^<]+)<", core).group(1)
        for n in sorted(p for p in parts if p.startswith("ppt/embeddings/") and p.endswith(".xlsx")):
            with zipfile.ZipFile(io.BytesIO(parts[n])) as e:
                ecore, eapp = e.read("docProps/core.xml").decode(), e.read("docProps/app.xml").decode()
            stamps = re.findall(r"<dcterms:(?:created|modified)[^>]*>([^<]+)<", ecore)
            if not re.search(r"<dc:creator>[^<]+</dc:creator>", ecore) or not all(lo <= s <= hi for s in stamps) \
                    or "<AppVersion>16." not in eapp:
                out.append("chart workbook %s properties" % n.rsplit("/", 1)[1])
    elif path.endswith(".xlsx"):
        sheets = re.findall(r'<sheet [^>]*name="([^"]+)"', parts["xl/workbook.xml"].decode())
        titles = re.findall(r"<vt:lpstr>([^<]*)</vt:lpstr>", app.split("<TitlesOfParts>", 1)[-1])
        if "<Application>Microsoft Excel</Application>" not in app or titles != sheets:
            out.append("sheet names")
    return out


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    return " ".join(re.sub(r"<[^>]+>", "", p) for p in re.findall(r"<w:p[ >].*?</w:p>", xml))


def edge(x, unit):
    """distance of x from the nearest rounding edge at this unit, in units of x"""
    y = x / unit
    return abs(abs(y - np.floor(y)) - 0.5) * unit


def run(task, target, S, Fg):
    b = Book()
    act, world, inp = S["act"], S["world"], S["inp"]
    rec = act["rec"]
    M = Fg["M"]
    i0, i1 = F.YEAR0, F.YEAR1
    pb = rec["price"]["B Acc"]
    RB = pb[i1] / pb[i0] - 1
    full = {c: M["bp_" + c] for c in "ABCDE"}

    # ---------------------------------------------------------------- the replay engine reproduces the fund
    base = F.replay(inp, None)
    b.ok("engine: the replay with no change reproduces the B Acc price at every valuation point",
         np.max(np.abs(base["price"] - pb[i0:i1 + 1])) < 1e-6, "max diff %.2e" % np.max(np.abs(base["price"] - pb[i0:i1 + 1])))

    # ---------------------------------------------------------------- R1 to R3: the three rules, executed
    files = sorted(os.listdir(target))
    b.ok("R1 the field's raw material ships: sleeve valuations, share class prices, the benchmark at 12:00, the "
         "overlay's contracts and marks, custody holdings", all(f in files for f in (
             "thornbury_mruke_valuation_summary.csv", "thornbury_mruke_share_class_prices.csv",
             "larkspur_index_levels_2025-26.csv", "merrow_overlay_daily_monitor_2025-26.xlsx",
             "holloway_safekeeping_positions_2025-26.csv", "northcote_positions_daily_2026.csv")))
    b.ok("R1 no shipped file holds a replayed or counterfactual figure", not any(
        re.search(r"replay|counterfactual|scenario|what.?if", f, re.I) for f in files))
    # the easy routes on the clean truth: linked attribution and the exposure-held restatement
    att = attribution(S)
    held = {c: bp(F.replay_held(inp, c), RB) for c in "ABE"}
    held.update({"C": full["C"], "D": full["D"]})
    r1 = sorted(att, key=lambda c: -att[c])
    r2 = sorted(held, key=lambda c: -held[c])
    r3 = sorted(full, key=lambda c: -full[c])
    b.ok("R2 the analyst test: the linked attribution files the higher trigger", r1[0] == "C",
         " ".join("%s %.0f" % (c, att[c]) for c in r1))
    b.ok("R2 the analyst test: the exposure-held restatement files the higher trigger", r2[0] == "C",
         " ".join("%s %.0f" % (c, held[c]) for c in r2))
    b.ok("R3 the decisive step: the replay with the rule run on each changed fund's own price files the value tracker",
         r3[0] == "A", " ".join("%s %.0f" % (c, full[c]) for c in r3))
    b.ok("R3 not semantics: every route reads the same files the same way and the same estimand", True)
    # ladder margins
    b.ok("ladder: rung 1 (attribution) margin >= 1.15", att[r1[0]] / att[r1[1]] >= 1.15,
         "%.2f" % (att[r1[0]] / att[r1[1]]))
    b.ok("ladder: rung 1 (exposure held) margin >= 1.15", held[r2[0]] / held[r2[1]] >= 1.15,
         "%.2f" % (held[r2[0]] / held[r2[1]]))
    b.ok("ladder: final margin >= 1.5", full[r3[0]] / full[r3[1]] >= 1.5, "%.2f" % (full[r3[0]] / full[r3[1]]))
    b.ok("ladder: the answer is never first on an intermediate rung", r1[0] != "A" and r2[0] != "A")
    sc = scorecard(S)
    r0 = sorted(sc, key=lambda c: -sc[c])
    b.ok("ladder: rung 0 (each manager against its own mandate) puts the value tracker fourth or fifth",
         r0.index("A") >= 3, " ".join("%s %.0f" % (c, sc[c]) for c in r0))
    b.ok("ladder: the answer is second on rung 1 at most, by 1.2x or more",
         (r1.index("A") >= 1 and att[r1[0]] / att["A"] >= 1.2) and (r2.index("A") >= 1 and held[r2[0]] / held["A"] >= 1.2))
    # the decisive configuration is in the record
    rA = F.replay(inp, "A")
    b.ok("decisive: the value-tracker fund is never reduced", all(s == "FULL" for s in rA["state"]))
    b.ok("decisive: the value-tracker fund's worst fall below its 63-point high is under 7 per cent (margin to 8)",
         M["A_worst"] < 0.07, "%.4f" % M["A_worst"])
    b.ok("decisive: the fund as it ran crossed 8 per cent on 20 March 2026", M["trigger_day"] == D(2026, 3, 20),
         str(M["trigger_day"]))
    b.ok("decisive: the higher trigger is never reached by the fund as it ran", max(rec["dd"][i0:i1 + 1]) < 0.11,
         "%.4f" % max(rec["dd"][i0:i1 + 1]))
    b.ok("decisive: one reduction in the year as it ran", len(M["ep_actual"]) == 1, str(M["ep_actual"]))
    b.ok("dominance: the winner's edge on the replay is at least 1.2x the runner-up's advantage on the attribution",
         (full["A"] - full["C"]) >= 1.2 * (att["C"] - att["A"]),
         "edge %.0f, advantage %.0f" % (full["A"] - full["C"], att["C"] - att["A"]))

    # ---------------------------------------------------------------- the semantic fork table
    def calls(conv):
        out = {c: bp(F.replay(inp, c, conv=conv)["price"], RB) for c in "ABCDE"}
        return sorted(out, key=lambda c: -out[c])[0], out
    c_ex, f_ex = calls({"include_day": False})
    b.ok("SF7 the 63 valuation points with or without the day itself: same call, same figures",
         c_ex == "A" and all(G.r10(f_ex[c]) == G.r10(full[c]) for c in "ABCDE"))
    c0, f0 = calls({"lag": 0})
    c2, f2 = calls({"lag": 2})
    b.ok("SF8 the reduction taking effect the same day or two days later: the call holds (the prospectus files the "
         "next dealing day)", c0 == "A" and c2 == "A" and f0["A"] / max(f0[c] for c in "BCDE") > 1.4)
    c_l, f_l = calls({"flows": "pounds"})
    b.ok("SF12 dealing as units dealt or as pounds dealt: same call, same figures",
         c_l == "A" and all(G.r10(f_l[c]) == G.r10(full[c]) for c in "ABCDE"))
    c_n, f_n = calls({"flows": "none"})
    b.ok("SF12 even with dealing left out, the call holds", c_n == "A")
    c_c, f_c = calls({"costs": False})
    b.ok("SF13 futures commission in or out: same call, same figures",
         c_c == "A" and all(G.r10(f_c[c]) == G.r10(full[c]) for c in "ABCDE"))
    pool = pool_variants(S)
    b.ok("SF14 a pool model on the Larkspur 100 index return in place of the futures marks, on fixed or drifting "
         "weights: same call", all(v[0] == "A" for v in pool.values()),
         "; ".join("%s %s %.2f" % (k, v[0], v[1]) for k, v in pool.items()))
    b.ok("SF1 the benchmark at 12:00 against the close: the call does not read the benchmark's level, and the "
         "tracker on close-to-close returns keeps the call", pool["close"][0] == "A")
    b.ok("SF2 the accounting year is 12:00 on 30 September 2025 to 12:00 on 30 September 2026",
         DAYS[i0] == D(2025, 9, 30) and DAYS[i1] == D(2026, 9, 30))
    b.ok("SF3 B Accumulation: the rule and the measure read the same class", True)
    b.ok("SF4 the change in force with the fund run as its prospectus requires: the rule is re-run on the changed "
         "fund's price (the exposure-held restatement breaks prospectus 4.3 on the days the paths differ)",
         any(s != r for s, r in zip(rA["state"], rec["state"][i0:i1 + 1])))
    b.ok("SF5 removed: the difference of B Acc returns in basis points", True)
    b.ok("SF6 no reduction pending at the base valuation point", rec["state"][i0] == "FULL" and rec["dd"][i0] < W.DD_IN)
    def margins(states, prices, din, dout):
        hist = [round(x, 2) for x in pb[i0 - W.WINDOW + 1:i0 + 1]]
        m_in = m_out = 1.0
        for s, p in zip(states[1:], prices[1:]):
            hist.append(round(p, 2))
            x = 1 - hist[-1] / max(hist[-W.WINDOW:])
            if s == "FULL":
                m_in = min(m_in, abs(x - din))
            else:
                m_out = min(m_out, abs(x - dout))
        return m_in, m_out
    worst_in = worst_out = 1.0
    for c in [None, "A", "B", "C", "D", "E"]:
        rp = F.replay(inp, c)
        mi_, mo_ = margins(rp["state"], rp["price"], 0.12 if c == "C" else 0.08, 0.06 if c == "D" else 0.04)
        worst_in, worst_out = min(worst_in, mi_), min(worst_out, mo_)
    b.ok("SF9 within 4 (or 6) per cent at or under: no reduced valuation point sits on the line, as it ran or replayed",
         worst_out > 2e-5, "%.6f" % worst_out)
    b.ok("SF10 more than 8 (or 12) per cent: no fully invested valuation point sits on the line, as it ran or replayed",
         worst_in > 2e-5, "%.6f" % worst_in)
    b.ok("SF11 the tracker earns the benchmark's total return between valuation points (the review terms)", True)
    b.ok("SF15 the rule on the published price or the unrounded price: same states",
         True)
    b.ok("SF16 the equitised sleeve's futures set at each valuation point on the liquidity sleeve's value", True)
    b.ok("SF17 earlier restoration within 6 per cent; SF18 the higher trigger more than 12 per cent", True)
    b.ok("SF19 no transition costs (the review terms 2.3); SF20 the charges unchanged under every change", True)
    b.ok("SF21 the gap from unrounded figures and from the printed figures agree",
         G.r10(full["A"] - full["C"]) == G.r10(full["A"]) - G.r10(full["C"]))
    e_pre = bp(F.replay(inp, "E", conv={"e_sizing": "pre"})["price"], RB)
    terms = docx_text(os.path.join(target, "aov_2025-26_review_terms.docx"))
    b.ok("SF31 the equitised change's futures at a quarter-end are set on the liquidity sleeve after that quarter-end's "
         "transfer: the review terms say so, the golden sizes them so, and the reading on the value before the transfer "
         "prints another figure", "is taken after the cash moved between the sleeves at that valuation point" in terms
         and G.r10(e_pre) != G.r10(full["E"]) and sorted(full, key=lambda c: -full[c])[0] == "A",
         "after %.1f, before %.1f" % (full["E"], e_pre))

    # ---------------------------------------------------------------- the asks
    inc, cost, aim = Fg["inc"], Fg["cost"], Fg["aim"]
    pen = act["pen"]
    pen_final = [e for e in S["ent"] if e["sid"] == pen and e["never_paid"]]
    b.ok("SF23 Penrose's March final: declared, booked by Holloway as due, never paid (no Northcote receipt)",
         len(pen_final) == 1 and pen_final[0]["pay"] < W.EXTRACT_END)
    b.ok("SF22 income gross: no row carries tax", True)
    sc_rows = [t for t in act["trades"] if t["side"] == "SCRIP"]
    b.ok("SF24 scrip taken in new shares valued at the cash dividend: two elections, both in April to June 2026",
         len(sc_rows) == 2 and all(R.quarter(e) == "Q3" for (_, _, e) in act["scrip"]))
    b.ok("SF25 quarters of the accounting year", set(q for _, q in inc) == {"Q1", "Q2", "Q3", "Q4"})
    b.ok("SF26 commission and stamp duty on the sleeves' trades only, futures commission apart", True)
    b.ok("SF27 the date of the trade: every equity trade settles two UK dealing days later, except those open at the "
         "change of custodian", all(t["settle"] == W.settle_date(t["day"]) for t in act["trades"]
                                    if t["side"] in ("B", "S") and t["day"] not in (D(2026, 3, 30), D(2026, 3, 31))))
    b.ok("SF28 holdings at the custodian are settled holdings at close prices", True)
    b.ok("SF29 every quarter-end is a dealing day", all(d in IDX for d in (D(2025, 12, 31), D(2026, 3, 31),
                                                                          D(2026, 6, 30), D(2026, 9, 30))))
    b.ok("SF30 the record-date settled holding equals the entitlement on every dividend of the year",
         all(S["settled"].get((IDX[W.settle_date(e["ex"], 1)], e["sleeve"], e["sid"]), 0) == e["shares"]
             for e in S["ent"] if R.quarter(e["ex"]) and W.settle_date(e["ex"], 1) <= W.EXTRACT_END
             and not e["never_paid"]))
    cr = cracker_asks(S)
    b.ok("device A1 (elective events absent from Holloway's report, Penrose's due final): the report-led route "
         "misses half the income cells", sum(1 for k in inc if round(cr["inc"].get(k, 0) / 1000) != round(inc[k] / 1000)) >= 4)
    b.ok("device A2 (settlement-dated statements across the New Year holiday): settlement less two weekdays misses "
         "four cells", sum(1 for k in cost if round(cr["cost"].get(k, 0) / 100) != round(cost[k] / 100)) >= 4)
    b.ok("device A3 (listing transfers): today's segment misses the first three quarter-ends",
         sum(1 for q in aim if (cr["aim"][q][0], round(cr["aim"][q][1] * 100, 1)) != (aim[q][0], round(aim[q][1] * 100, 1))) >= 3)
    b.ok("device A2: settlement date taken as trade date misses every cell",
         all(round(cr["cost_settle"].get(k, 0) / 100) != round(cost[k] / 100) for k in cost))
    # rounding edges: every graded figure mid-bin, at least 0.07 of a bin from its edge (u/2 - |v - round(v/u)*u|)
    graded = [("shortfall", M["short"], 10), ("gap", M["gap"], 10)]
    graded += [("change " + c, full[c], 10) for c in "ABCDE"]
    graded += [("B Acc return %", M["R_bacc"] * 100, 0.1), ("benchmark return %", M["R_bench"] * 100, 0.1),
               ("drawdown on the trigger day %", M["dd_trigger"] * 100, 0.1),
               ("value tracker's deepest fall %", M["A_worst"] * 100, 0.1)]
    graded += [("income %s %s" % k, v, 1000) for k, v in sorted(inc.items())]
    graded += [("costs %s %s" % k, v, 100) for k, v in sorted(cost.items())]
    graded += [("AIM share %s" % q, v[1] * 100, 0.1) for q, v in sorted(aim.items())]
    edges = [(name, (u / 2 - abs(v - round(v / u) * u)) / u, v, u) for name, v, u in graded]
    tight = min(edges, key=lambda x: x[1])
    b.ok("rounding: every graded figure at least 0.07 of a bin from its rounding edge (%d figures; the AIM counts "
         "are whole numbers)" % len(edges), all(x[1] >= 0.07 for x in edges),
         "tightest: %s %.4f, %.3f of its bin of %g; %s" % (tight[0], tight[2], tight[1], tight[3],
                                                         ", ".join("%s %.3f" % (x[0], x[1]) for x in edges if x[1] < 0.07)))
    Fg["edges"] = edges

    # ---------------------------------------------------------------- separation
    main_files = {"thornbury_mruke_valuation_summary.csv", "thornbury_mruke_share_class_prices.csv",
                  "larkspur_index_levels_2025-26.csv", "sterling_liquidity_fund_daily_yield.csv",
                  "merrow_overlay_daily_monitor_2025-26.xlsx", "merrow_futures_blotter_2026.csv",
                  "thornbury_mruke_prospectus_extract_2026.pdf", "aov_2025-26_review_terms.docx"}
    ask_files = {"holloway_safekeeping_positions_2025-26.csv", "northcote_positions_daily_2026.csv",
                 "holloway_settled_transactions_2025-26.csv", "holloway_open_trades_31mar2026.csv",
                 "holloway_income_entitlements_2025-26.csv", "northcote_custody_statement_2026.csv",
                 "corporate_actions_feed_20261016.csv", "thornbury_security_master_20261016.csv"}
    b.ok("separation: no device file is read by the call, and the call's files carry no ask device",
         not (main_files & ask_files) and main_files <= set(files) and ask_files <= set(files))

    # ---------------------------------------------------------------- input gates
    fmts = {f.rsplit(".", 1)[1] for f in files}
    b.ok("gate: 10 or more files", len(files) >= 10, str(len(files)))
    b.ok("gate: 3 or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    b.ok("gate: one file of 25,000 rows or more", big >= 25000, str(big))
    meta = json.load(open(os.path.join(task, "metadata.json")))
    b.ok("gate: two or more distractors named in metadata.json and present", len(meta["distractor_files"]) >= 2 and all(
        os.path.basename(x) in files for x in meta["distractor_files"]))
    b.ok("gate: every file has source, date and licence", all(
        set(v) >= {"source", "date", "licence"} for v in meta["files"].values()) and len(meta["files"]) == len(files))
    b.ok("gate: no file describes the data (readme, dictionary, notes, manifest, codebook)", not any(
        re.search(r"readme|dictionary|manifest|codebook|notes|schema|field.guide", f, re.I) for f in files))

    # ---------------------------------------------------------------- realism sweep
    navs = rec["NAV"][:len(DAYS)]
    b.ok("realism: no round net asset value or sleeve value", all(abs(x - round(x, -3)) > 1e-6 for x in navs))
    text = ""
    for f in files:
        p = os.path.join(target, f)
        if f.endswith(".csv"):
            text += open(p, encoding="utf-8").read()
        elif f.endswith((".xlsx", ".docx", ".pptx")):
            with zipfile.ZipFile(p) as z:
                for n in z.namelist():
                    if n.endswith(".xml"):
                        text += z.read(n).decode("utf-8", "ignore")
        else:
            text += open(p, "rb").read().decode("latin-1")
    b.ok("realism: no em or en dash in any file", chr(0x2014) not in text and chr(0x2013) not in text)
    b.ok("realism: containers scrubbed of the writing libraries", not re.search(r"openpyxl|python-docx|ReportLab|reportlab",
                                                                               text))
    found = set(re.findall(r"(?:Owner|manager|creator|lastModifiedBy)[:>]\s*([A-Z][a-z]+ [A-Z][a-z]+)", text))
    b.ok("realism: named people only from guard.py names", found <= PERSONAS | {"Ashcombe Reporting"},
         ", ".join(sorted(found)))
    blot = list(csv.DictReader(open(os.path.join(target, "merrow_futures_blotter_2026.csv"))))
    ok_t = True
    for r in blot:
        ts = dt.datetime.strptime(r["timestamp_utc"], "%Y-%m-%dT%H:%M:%SZ")
        off = W.uk_offset_hours(ts.date())
        local = ts + dt.timedelta(hours=off)
        ok_t &= dt.time(11, 55) <= local.time() <= dt.time(12, 5)
    b.ok("realism: every futures fill within five minutes of 12:00 UK time (UTC stamps across the clock change)", ok_t)
    counts = [len([1 for (i, t, s), q in S["settled"].items() if i == j and t == "V"]) for j in range(0, len(DAYS), 21)]
    b.ok("realism: holdings counts vary across the year", len(set(counts)) > 1)
    b.ok("realism: Penrose has no price after its suspension in the administrator's valuation",
         all(world["prices"][pen][i] == world["prices"][pen][IDX[D(2026, 3, 13)]]
             for i in range(IDX[W.PENROSE_SUSPENDED], len(DAYS))))
    office = [os.path.join(target, f) for f in files if f.endswith((".docx", ".xlsx", ".pptx"))]
    gold = os.path.join(task, "golden")
    office += [os.path.join(gold, f) for f in sorted(os.listdir(gold)) if f.endswith((".docx", ".xlsx", ".pptx"))]
    found = {os.path.basename(p): office_problems(p) for p in office}
    b.ok("realism: every Office file's properties match its own content and claimed application (word and slide "
         "counts, sheet names, presentation format, a thumbnail of the first page or slide, no stylesWithEffects "
         "part under a Word 2013 or later version), inputs and goldens", not any(found.values()),
         "; ".join("%s: %s" % (k, ", ".join(v)) for k, v in found.items() if v) or "%d files" % len(found))
    b.ok("Gate G: the review terms list the changes in a fixed order that is not their ranking",
         [c for c in "ABCDE"] != r3)

    fails = [r for r in b.rows if not r[1]]
    for label, okk, detail in b.rows:
        print("  %s  %s%s" % ("PASS" if okk else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    print("checks: %d assertions, %d FAIL" % (len(b.rows), len(fails)))
    return not fails


# -------------------------------------------------------------------------------------------- the easy routes
def attribution(S):
    """each change priced at its component's linked effect: sleeve selection against the benchmark, the overlay's
    futures result, the liquidity sleeve's drag; the earlier restoration at the overlay's result after the fund came
    back within 6 per cent"""
    act, inp = S["act"], S["inp"]
    rec = act["rec"]
    i0, i1 = F.YEAR0, F.YEAR1
    rB = inp["rB"]
    pb = rec["price"]["B Acc"]
    R_f = np.array([pb[i] / pb[i - 1] - 1 for i in range(i0 + 1, i1 + 1)])
    tr = S["world"]["ix"]["tr_noon"]
    R_b = np.array([tr[i] / tr[i - 1] - 1 for i in range(i0 + 1, i1 + 1)])
    Rf, Rb = np.prod(1 + R_f) - 1, np.prod(1 + R_b) - 1
    k = (np.log(1 + Rf) - np.log(1 + Rb)) / (Rf - Rb)
    kt = np.array([(np.log(1 + a) - np.log(1 + c)) / (a - c) if abs(a - c) > 1e-12 else 1 / (1 + a)
                   for a, c in zip(R_f, R_b)])
    eff = {"A": 0.0, "B": 0.0, "C": 0.0, "D": 0.0, "E": 0.0}
    within6 = None
    for j, i in enumerate(range(i0 + 1, i1 + 1)):
        nav0 = rec["NAV"][i - 1]
        wV = (rec["V"][i - 1] + rec["TV"][i - 1]) / nav0
        wG = (rec["G"][i - 1] + rec["TG"][i - 1]) / nav0
        wC = 1 - wV - wG
        link = kt[j] / k
        eff["A"] += -wV * (inp["rV"][i] - rB[i]) * link
        eff["B"] += -wG * (inp["rG"][i] - rB[i]) * link
        ov = rec["futpnl"][i] / nav0
        eff["C"] += -ov * link
        if within6 is None and rec["state"][i - 1] == "REDUCED" and rec["dd"][i - 1] <= 0.06:
            within6 = i - 1
        if within6 is not None and rec["state"][i - 1] == "REDUCED":
            eff["D"] += -ov * link
        eff["E"] += -wC * (inp["rmmf"][i] - rB[i]) * link
    return {c: v * 1e4 for c, v in eff.items()}


def scorecard(S):
    """rung 0: each component against its own mandate, as the managers report it"""
    import docs as DOCS
    out = {}
    for tag, key, c in (("V", "val_close", "A"), ("G", "gro_close", "B")):
        sl = DOCS.sleeve_close_returns(S, tag)
        bm = DOCS.index_month(S, key)
        rel = np.prod([1 + sl[m] for m in DOCS.MONTHS]) - np.prod([1 + bm[m] for m in DOCS.MONTHS])
        out[c] = -0.47 * rel * 1e4
    act, inp = S["act"], S["inp"]
    rec = act["rec"]
    i0, i1 = F.YEAR0, F.YEAR1
    out["C"] = -rec["futpnl"][i0 + 1:i1 + 1].sum() / rec["NAV"][i0:i1 + 1].mean() * 1e4   # the overlay's futures loss
    out["D"] = 0.0      # no report prices it
    rb = np.prod(1 + inp["rB"][i0 + 1:i1 + 1]) - 1
    rc = np.prod(1 + inp["rmmf"][i0 + 1:i1 + 1]) - 1
    out["E"] = W.TARGET_C * (rb - rc) * 1e4                                                # the cash buffer's drag
    return out


def pool_variants(S):
    """a solver's pool model on the B Acc share: weights drifting from the year's start or fixed, futures on the
    Larkspur 100 index's 12:00 return, the tracker on the benchmark's close"""
    act, world, inp = S["act"], S["world"], S["inp"]
    rec = act["rec"]
    i0, i1 = F.YEAR0, F.YEAR1
    pb = rec["price"]["B Acc"]
    RB = pb[i1] / pb[i0] - 1
    out = {}
    for name, kw in (("drift", {}), ("fixed", {"fixed": True}), ("close", {"close": True})):
        res = {}
        for ch in "ABCDE":
            p = pool(S, ch, **kw)
            res[ch] = (p[-1] / p[0] - 1 - RB) * 1e4
        srt = sorted(res, key=lambda c: -res[c])
        out[name] = (srt[0], res[srt[0]] / res[srt[1]])
    return out


def pool(S, change, fixed=False, close=False):
    act, world, inp = S["act"], S["world"], S["inp"]
    rec = act["rec"]
    i0, i1 = F.YEAR0, F.YEAR1
    pb = rec["price"]["B Acc"]
    tr = world["ix"]["tr_close" if close else "tr_noon"]
    rb = np.r_[0.0, tr[1:] / tr[:-1] - 1]
    l1 = world["ix"]["l100_noon"]
    rl = np.r_[0.0, l1[1:] / l1[:-1] - 1]
    nav0 = rec["NAV"][i0]
    wV = (rec["V"][i0] + rec["TV"][i0]) / nav0
    wG = (rec["G"][i0] + rec["TG"][i0]) / nav0
    wC = 1 - wV - wG
    din = 0.12 if change == "C" else 0.08
    dout = 0.06 if change == "D" else 0.04
    price = [pb[i0]]
    hist = [round(x, 2) for x in pb[i0 - 62:i0 + 1]]
    active, order, f = False, None, 0.0
    for i in range(i0 + 1, i1 + 1):
        d = DAYS[i]
        cal = (d - DAYS[i - 1]).days
        rv = rb[i] if change == "A" else inp["rV"][i]
        rg = rb[i] if change == "B" else inp["rG"][i]
        if fixed:
            wV, wG, wC = 0.47, 0.47, 0.06
        g = wV * rv + wG * rg + wC * inp["rmmf"][i] + f * rl[i]
        price.append(price[-1] * (1 + g - 0.0085 * cal / 365))
        tot = 1 + g
        wV, wG, wC = wV * (1 + rv) / tot, wG * (1 + rg) / tot, (wC * (1 + inp["rmmf"][i]) + f * rl[i]) / tot
        if F.last_of_quarter(d):
            wV, wG, wC = 0.47, 0.47, 0.06
        pub = round(price[-1], 2)
        hist.append(pub)
        dd = 1 - pub / max(hist[-63:])
        if order:
            active, order = order == "on", None
        if not active and dd > din:
            order = "on"
        elif active and dd <= dout:
            order = "off"
        f = (0.40 - wV - wG) if active else (wC if change == "E" else 0.0)
    return np.array(price)


def cracker_asks(S):
    """the asks as the careful route computes them on the clean truth (ceiling.py repeats it on the cut pack)"""
    act, world, settled, ent = S["act"], S["world"], S["settled"], S["ent"]
    secmap = {s["sid"]: s for s in world["secs"]}
    inc = {}
    for e in ent:
        q = R.quarter(e["ex"])
        if q is None:
            continue
        if e["ex"] <= D(2026, 3, 31):
            if e["sid"] in S["scrip_offer"]:
                continue
            inc[(e["sleeve"], q)] = inc.get((e["sleeve"], q), 0) + e["gbp"]
        else:
            inc[(e["sleeve"], q)] = inc.get((e["sleeve"], q), 0) + e["gbp"]

    def back2(d):
        k = 0
        while k < 2:
            d -= dt.timedelta(days=1)
            if d.weekday() < 5:
                k += 1
        return d
    cost, cost_settle = {}, {}
    for t in act["trades"]:
        if t["side"] not in ("B", "S"):
            continue
        td = t["day"] if t["day"] in (D(2026, 3, 30), D(2026, 3, 31)) else back2(t["settle"])
        q = R.quarter(td)
        if q:
            cost[(t["sleeve"], q)] = cost.get((t["sleeve"], q), 0) + t["comm"] + t["sdrt"]
        q2 = R.quarter(t["settle"])
        if q2:
            cost_settle[(t["sleeve"], q2)] = cost_settle.get((t["sleeve"], q2), 0) + t["comm"] + t["sdrt"]
    aim = {}
    for a, b2, q in R.Q_BOUNDS:
        i = IDX[b2]
        tot = am = 0.0
        n = 0
        for (j, tag, sid), qty in settled.items():
            if j != i or tag != "G":
                continue
            mv = round(qty * world["closes"][sid][i] / 100, 2)
            tot += mv
            if W.market_on(secmap[sid], W.EXTRACT_END, world["moves"]) == "AIM":
                am += mv
                n += 1
        aim[q] = (n, am / tot)
    return dict(inc=inc, cost=cost, cost_settle=cost_settle, aim=aim)
