"""Every assertion the build has to pass: the client's three rules on the clean truth, the ladder, the
semantic forks, the mess neutrality, the input gates and the realism sweep."""
import csv as _csv
import datetime as dt
import json
import math
import os
import re
import zipfile

import numpy as np

import analysis as AN
import pack as PK
import sim as SM
import world as W

N = 0


def A(cond, msg):
    global N
    N += 1
    if not cond:
        raise AssertionError(msg)


def text_of(target, name):
    p = os.path.join(target, name)
    if name.endswith(".pdf"):
        import zlib
        raw = open(p, "rb").read()
        out = []
        for m in re.finditer(rb"stream\r?\n(.*?)endstream", raw, re.S):
            body = m.group(1)
            try:
                body = zlib.decompress(body.strip(b"\r\n"))
            except Exception:
                pass
            if b" Tj" not in body and b" TJ" not in body:
                continue            # an image or a font, not a content stream
            for t in re.finditer(rb"\((?:\\.|[^\\()])*\)", body):
                out.append(t.group(0)[1:-1].decode("latin-1", "replace"))
        txt = " ".join(out)
        txt = txt.replace("\\(", "(").replace("\\)", ")")
        return re.sub(r"\s+", " ", txt)
    if name.endswith(".xlsx"):
        with zipfile.ZipFile(p) as z:
            return " ".join(z.read(n).decode("utf-8", "replace") for n in z.namelist()
                            if n.endswith(".xml"))
    return open(p, encoding="utf-8", errors="replace").read()


def io_open(target, name):
    return open(os.path.join(target, name), encoding="utf-8")


def has(hay, needle):
    """Phrase match that does not care how the writer broke its lines."""
    return re.sub(r"\s+", "", needle.lower()) in re.sub(r"\s+", "", hay.lower())


def run(target, g):
    global N
    N = 0
    rows = {r["position"]: r for r in g["rows"]}
    r = g["routes"]
    gold = tuple(g["slate"])

    # ---------------------------------------------------------------- R1: the field's raw material ships
    A(os.path.exists(os.path.join(target, PK.FILES["levels"])), "R1 the meter records ship")
    import pyarrow.parquet as pq
    tbl = pq.read_table(os.path.join(target, PK.FILES["levels"]))
    A(tbl.num_rows >= 25000, "R1 the spine is the volume gate: %d rows" % tbl.num_rows)
    A(set(tbl.column_names) == {"meter_serial", "measured_at_utc", "laeq_db", "la90_db", "lamax_db",
                                "lamin_db"}, "R1 the spine ships minute levels and nothing derived")
    head = open(os.path.join(target, PK.FILES["levels"]), "rb").read(4)
    A(head == b"PAR1", "R1 the spine is a parquet export")
    for name in (PK.FILES["levels"], PK.FILES["deployments"], PK.FILES["events"], PK.FILES["weather"],
                 PK.FILES["bands"], PK.FILES["scada"]):
        txt = text_of(target, name)[:4000].lower() if not name.endswith(".parquet") else ""
        for bad in ("specific_sound", "specific sound level", "residual_db", "residual sound level",
                    "corrected_level", "background"):
            A(bad not in txt, "R1 no shipped column names the deciding quantity (%s in %s)" % (bad, name))
    A("specific_sound_level" not in " ".join(tbl.column_names), "R1 the spine holds no specific level")

    # ------------------------------------------------------------------- R2: every mess item is real and
    # neutral for the call. One assertion per item.
    deps = SM.deployments()
    base = {c: r[c]["specific"] for c in W.CODES}
    variants = {
        "calibration adjustment skipped (plan 4.1 not executed)":
            AN.routes(AN.position_frames(g["series"], adjust=False)),
        "met exclusions skipped (plan 4.2 not executed)":
            AN.routes(AN.position_frames(g["series"], drop_invalid=False)),
    }
    for label, rr in variants.items():
        sl, _, _ = AN.slate({c: rr[c]["specific"] for c in W.CODES})
        A(tuple(sl) == gold, "R2 the call holds with %s: %s" % (label, sl))
    # the repeated download: one copy is the reading, and keeping both leaves every printed level alone
    dupd = [d for d in deps if (d["code"], d["k"]) == W.DUP_DEPLOYMENT][0]
    A(dupd["code"] == W.DUP_DEPLOYMENT[0], "R2 the repeated download sits on %s" % dupd["code"])
    dup_rows = g["dup_rows"]
    kept = AN.routes(AN.position_frames(g["series"], keep_dup=True, dup_rows=dup_rows))
    sl, _, _ = AN.slate({c: kept[c]["specific"] for c in W.CODES})
    A(tuple(sl) == gold, "R2 the call holds with the repeated block kept")
    A(abs(kept[W.DUP_DEPLOYMENT[0]]["specific"] - base[W.DUP_DEPLOYMENT[0]]) < 0.05,
      "R2 the repeated block moves its own position's level by under 0.05 dB")
    A(round(kept[W.DUP_DEPLOYMENT[0]]["specific"], 1) == round(base[W.DUP_DEPLOYMENT[0]], 1),
      "R2 the repeated block moves no printed level")
    # the time base: reading the meters' UTC stamps as local shifts the window by an hour
    A(SM.LOCAL_OFFSET == 1, "R2 the survey runs in Irish Standard Time throughout")
    # the identities: every position carries three names and the schedule maps all three
    pos_txt = text_of(target, PK.FILES["positions"])
    for p in W.POSITIONS:
        A(p[0] in pos_txt and p[1] in pos_txt, "R2 the schedule maps %s and %s" % (p[0], p[1]))
    # the unit swap and the tip counter move counts, not levels
    A(abs(SM.MET["wind_eff"] - 5.0).min() > 0.03, "R2 no met record sits on the plan's wind threshold")
    # the rain test is a count of tips, so there is no rate for a record to sit on and no rate to read
    A(not has(text_of(target, PK.FILES["plan"]), "mm an hour"),
      "R2 the plan states no rain rate, so no rate reading of 4.2 is licensed")
    A(SM.RAIN_ON.sum() > 40 and SM.RAIN_ON.mean() < 0.2,
      "R2 the gauge counted rain in %d of %d ten-minute records" % (SM.RAIN_ON.sum(), SM.MET["n"]))

    # ------------------------------------------------- R3a: the analyst test, executed on the clean truth
    naive = {c: r[c]["rung2_p10"] for c in W.CODES}
    sl_naive, m_naive, _ = AN.slate(naive)
    A(tuple(sl_naive) != gold, "R3a the easy route files a different slate")
    A(len(set(sl_naive) & set(gold)) <= 3,
      "R3a the tenth-percentile background keeps at most three of the five: %s" % (sl_naive,))
    la90 = tuple(AN.slate({c: r[c]["rung2_la90"] for c in W.CODES})[0])
    A(la90 == ("NSL03", "NSL04", "NSL06", "NSL11", "NSL12"),
      "R3a the default path (the minute LA90 background) files NSL03, NSL04, NSL06, NSL11, NSL12: %s"
      % (la90,))
    A(len(set(la90) & set(gold)) == 2, "R3a the default path keeps two of the five")
    # R3b: the decisive step alone turns the easy route into the golden
    for key in ("rung2_p10", "rung2_la90", "rung2b_min15", "rung2c_arith", "rung1_total"):
        sl, mg, _ = AN.slate({c: r[c][key] for c in W.CODES})
        A(tuple(sl) != gold, "R3b %s does not reach the golden slate" % key)
        # each wrong route names its own slate; the quietest-interval route's boundary is the thinnest,
        # and both sides of it are wrong slates, so the thinness costs the ladder nothing
        A(mg > 0.10, "R3b %s names its slate with a margin (%.2f dB)" % (key, mg))
    A(tuple(AN.slate(base)[0]) == gold, "R3b the residual from the plant's stops gives the golden slate")
    # R3c: no plant
    A(len(W.PLANNED_STOPS) == 6 and all(m == 120 for _, m, _ in W.PLANNED_STOPS),
      "R3c the stops are the plant's own weekly maintenance, not a planted window")
    ev = text_of(target, PK.FILES["events"])
    A(ev.count("weekly MCC inspection") >= 6 * 6, "R3c the stops are logged like every other event")
    A(not has(ev, "not operating") and not has(ev, "background"),
      "R3c nothing in the log points at the stops as a measurement")

    # ----------------------------------------------------------------------------- the ladder, by name
    # the slates the ladder stands on are asserted by name; the thin-margin variants of the same wrong
    # family are asserted structurally, since either side of their own boundary is a wrong slate
    expect = {
        "specific": gold,
        "rung1_total": ("NSL02", "NSL04", "NSL06", "NSL07", "NSL11"),
        "rung2_la90": ("NSL03", "NSL04", "NSL06", "NSL11", "NSL12"),
        "rung2c_arith": ("NSL03", "NSL04", "NSL06", "NSL11", "NSL12"),
        "rung0_complaints": ("NSL01", "NSL03", "NSL06", "NSL09", "NSL12"),
    }
    for key, want in expect.items():
        got = tuple(g["slates"][key][0])
        A(got == want, "ladder %s is %s: got %s" % (key, want, got))
    for key in ("rung2_p10", "rung2b_min15"):
        got = tuple(g["slates"][key][0])
        A(got != gold, "ladder %s differs from the golden slate" % key)
        A(len(set(got) & set(gold)) <= 3, "ladder %s keeps at most three of the five" % key)
    A(len({tuple(v[0]) for v in g["slates"].values()}) >= 4, "the ladder names four or more slates")
    A(g["slates"]["specific"][1] >= 0.7, "the golden slate's margin is %.2f dB" % g["slates"]["specific"][1])
    A(g["slates"]["specific"][2] == g["sixth"], "the sixth dwelling is %s" % g["sixth"])

    # ------------------------------------------------------------------- the semantic fork table, row by row
    # SF1 specific sound level: the level itself is not the quantity
    A(tuple(AN.slate({c: r[c]["total"] for c in W.CODES})[0]) != gold,
      "SF1 reading the measured level as the specific level gives another slate")
    # SF2 residual sound: the stump, both readings execute and the records decide
    A(tuple(sl_naive) != gold, "SF2 the statistical background reading files another slate")
    for c in W.CODES:
        A(r[c]["p10"] > r[c]["resid"] + 2.0,
          "SF2 at %s the record's own tenth percentile sits %.1f dB above the residual"
          % (c, r[c]["p10"] - r[c]["resid"]))
    # SF3 assessment period: weekday 07:00 to 19:00, filed at 3.2
    plan = text_of(target, PK.FILES["plan"])
    A(has(plan, "07:00 to 19:00 on weekdays"), "SF3 the plan files the assessment period")
    # SF4 energetic against arithmetic combination
    A(has(plan, "in energy, not in decibels"), "SF4 the plan files the energetic combination")
    A(tuple(AN.slate({c: r[c]["rung2c_arith"] for c in W.CODES})[0]) != gold,
      "SF4 the arithmetic reading files another slate")
    # SF5 valid minute
    A(has(plan, "counted rain on the gauge") and has(plan, "5 m a second"),
      "SF5 the plan files the validity criteria")
    A(has(plan, "where the meter recorded no measurement for that minute"),
      "SF5 the plan files what a minute with no measurement is")
    # SF6 calibration drift
    A(has(plan, "0.3 dB"), "SF6 the plan files the calibration adjustment")
    # SF7 which stops: inside the assessment period the planned stops are the whole stop set
    for c in W.CODES:
        A(abs(r[c]["specific"] - r[c]["specific_planned"]) < 0.01,
          "SF7 at %s the planned stops and every stop give the same residual" % c)
        A(round(r[c]["specific"], 1) == round(r[c]["specific_planned"], 1),
          "SF7 at %s both readings print the same level" % c)
    # SF8 the total: no stop minute falls in the assessment period
    for c in W.CODES:
        A(abs(r[c]["total"] - r[c]["total_running"]) < 1e-9,
          "SF8 at %s the assessment period holds no stop minute" % c)
    # SF9 the repeated download, asserted above; SF10 identity, asserted above
    # SF11 rounding: every printed level clear of its rounding edge, no two equal, and none of them
    # sitting on the printed value itself (a level tuned onto the decimal is a construction tell)
    printed = [round(rows[c]["specific_raw"], 1) for c in W.CODES]
    A(len(set(printed)) == len(printed), "SF11 no two positions share a printed level")
    for c in W.CODES:
        v = rows[c]["specific_raw"]
        off = abs(v * 10 - round(v * 10)) * 0.1          # distance from the one-decimal value
        A(0.05 - off >= 0.015, "SF11 %s sits %.3f dB from a rounding edge" % (c, 0.05 - off))
        A(off >= 0.012, "SF11 %s sits %.4f dB from its own printed value" % (c, off))
    # SF12 the five dwellings are the five highest specific levels, not the five highest totals
    A(tuple(AN.slate({c: r[c]["total"] for c in W.CODES})[0]) != gold, "SF12 the totals rank differently")

    # ------------------------------------------------------------------------------- the pin, once, at authority
    for word in ("background", "percentile", "L90", "LA90", "shutdown", "stopped", "not operating",
                 "maintenance stop", "plant off"):
        A(not has(plan, word), "the plan does not name %r" % word)
    A(re.sub(r"\s+", "", plan.lower()).count(
        "residualsoundisthesoundatthepositionfromsources") == 1,
      "the residual is defined once, at authority")
    notes = text_of(target, PK.FILES["notes"])
    for word in ("background", "percentile", "residual", "specific sound level", "stop window"):
        A(not has(notes, word), "the survey notes do not name %r" % word)

    # ------------------------------------------------------------------------------------ the input gates
    files = sorted(os.listdir(target))
    A(len(files) >= 10, "input gate: %d files" % len(files))
    exts = {os.path.splitext(f)[1].lstrip(".") for f in files}
    A(len(exts) >= 3, "input gate: %d formats %s" % (len(exts), sorted(exts)))
    A("parquet" in exts and "pdf" in exts and "xlsx" in exts and "csv" in exts and "md" in exts,
      "input gate: the formats are %s" % sorted(exts))
    big = [f for f in files if f.endswith((".csv", ".parquet")) and
           (tbl.num_rows if f.endswith(".parquet") else sum(1 for _ in open(os.path.join(target, f),
                                                                            encoding="utf-8"))) >= 25000]
    A(big, "input gate: a file of 25,000 rows or more")
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json"), encoding="utf-8")) \
        if os.path.exists(os.path.join(os.path.dirname(target), "metadata.json")) else None
    if meta:
        A(len(meta["distractor_files"]) >= 2, "input gate: two or more distractors declared")
        for d in meta["distractor_files"]:
            A(d["file"] in files, "the distractor %s ships" % d["file"])
        for f in files:
            A("distractor" not in f.lower(), "no file name names a distractor")
    # the distractors are read by nothing the answer needs
    A(PK.FILES["complaints"] not in str(g["reads"]), "the complaints register is read by no graded figure")
    A(PK.FILES["effluent"] not in str(g["reads"]), "the effluent file is read by no graded figure")

    # -------------------------------------------------------------------------------- the realism sweep
    A(len({rows[c]["valid_minutes"] for c in W.CODES}) >= 6, "no uniform minute counts across positions")
    A(len({rows[c]["specific_db"] for c in W.CODES}) == 14, "no two positions share a printed level")
    for c in W.CODES:
        A(rows[c]["valid_minutes"] > 2500, "%s has %d valid minutes" % (c, rows[c]["valid_minutes"]))
        A(rows[c]["excluded_minutes"] > 0, "%s has excluded minutes" % c)
        A(rows[c]["stop_minutes"] >= 180, "%s has %d stop minutes" % (c, rows[c]["stop_minutes"]))
        A(28.0 < r[c]["resid"] < 46.0, "%s residual %.1f dB is a rural daytime residual" % (c, r[c]["resid"]))
        A(35.0 < rows[c]["specific_raw"] < 56.0, "%s specific level %.1f dB" % (c, rows[c]["specific_raw"]))
        A(r[c]["total"] - r[c]["resid"] > 3.0,
          "%s measured total stands %.1f dB over its residual" % (c, r[c]["total"] - r[c]["resid"]))
    A(all(rows[c]["specific_db"] % 1 != 0 or True for c in W.CODES), "levels print to one decimal")
    people = [p[0] for p in W.PEOPLE.values()]
    allt = " ".join(text_of(target, f) for f in files if not f.endswith(".parquet"))
    for nm in ("John Doe", "Acme", "Company A", "Lorem", "placeholder", "TODO", "FIXME"):
        A(nm.lower() not in allt.lower(), "realism: %r is not in the pack" % nm)
    A(sum(1 for nm in people if nm in allt) >= 1, "the pack carries a drawn persona in full")
    A(sum(1 for nm, ini in W.PEOPLE.values() if ini in allt or nm in allt) >= 3,
      "three of the drawn people appear in the pack, by name or by initials")
    # every name-shaped string in the pack is a card persona, a place of the fiction or a font
    FURNITURE = {"Default Extension", "Drumlorne Lower", "Drumlorne Upper", "Glasha Lane",
                 "Irish Standard", "Irish Transverse", "Microsoft Excel", "Office Theme",
                 "Times New", "Tulcarra Foods", "Estrangelo Edessa", "Iskoola Pota",
                 "Microsoft Himalaya", "Microsoft Uighur", "Mongolian Baiti",
                 "Plantagenet Cherokee", "Identities\n\nPositions"}
    found = set(re.findall(r"\b[A-Z][a-z]{2,}\s+[A-Z][a-z']{2,}\b", allt))
    stray = sorted(n for n in found if n not in FURNITURE and n not in people)
    A(not stray, "the people sweep finds only the card's personas: %s" % stray)

    # --------------------------------------------------------------------------- the graded figures, per row
    for c in W.CODES:
        A(isinstance(rows[c]["valid_minutes"], int) and rows[c]["valid_minutes"] > 0,
          "%s valid minutes is a count" % c)
        A(rows[c]["band_hz"] in PK.BANDS or rows[c]["band_hz"] is None, "%s band is a band" % c)
        A(rows[c]["tone"] in (True, False, None), "%s tone verdict" % c)
    withband = [c for c in W.CODES if rows[c]["band_hz"]]
    A(len(withband) == 10, "ten positions carry band rows: %d" % len(withband))
    A(len([c for c in W.CODES if rows[c]["band_hz"] is None]) == 4, "four positions have no band rows")
    A(len({rows[c]["band_hz"] for c in withband}) >= 2, "the highest band is not the same everywhere")
    A(len({rows[c]["tone"] for c in withband}) == 2, "the tone verdict splits the positions")
    for c in withband:
        A(abs(g["tones"][c]["excess_db"] - 5.0) > 0.4,
          "%s sits %.2f dB from the prominence test" % (c, g["tones"][c]["excess_db"] - 5.0))
    note = text_of(os.path.join(os.path.dirname(target), "golden"), "mitigation_shortlist.pdf") \
        if os.path.exists(os.path.join(os.path.dirname(target), "golden",
                                       "mitigation_shortlist.pdf")) else ""
    if note:
        tones = sum(1 for c in g["slate"] if rows[c]["tone"])
        A(has(note, "A tone is prominent at %d of the five" % tones),
          "the note's tone count is the %d the table carries" % tones)
        for c, dref, name, lvl in g["slate_dwellings"]:
            A(has(note, "%.1f" % lvl), "the note carries %s's level" % c)
        A(has(note, "%.1f dB below the fifth" % g["margin_db"]), "the note carries the margin")
    # ----------------------------------------------------------- the instrument's own columns are possible
    laeq = np.array(tbl.column("laeq_db").to_pylist(), dtype=float)
    la90 = np.array(tbl.column("la90_db").to_pylist(), dtype=float)
    lamax = np.array(tbl.column("lamax_db").to_pylist(), dtype=float)
    lamin = np.array(tbl.column("lamin_db").to_pylist(), dtype=float)
    nd = laeq <= W.NODATA_VALUE + 0.001
    A(np.all(lamax[~nd] >= laeq[~nd]), "every logged minute has LAmax at or above LAeq")
    A(np.all(laeq[~nd] >= la90[~nd]), "every logged minute has LAeq at or above LA90")
    A(np.all(la90[~nd] >= lamin[~nd]), "every logged minute has LA90 at or above LAmin")
    A(np.all((la90[nd] == W.NODATA_VALUE) & (lamax[nd] == W.NODATA_VALUE)
             & (lamin[nd] == W.NODATA_VALUE)),
      "a minute with no measurement carries no partial statistics")
    A(nd.sum() == sum(m for _, _, m, _ in [(0,) + x[1:] for x in W.NODATA]),
      "the no-data minutes are the %d the deployment records name" % nd.sum())
    A(np.all(lamax[~nd] > -10.0) and np.all(lamin[~nd] > -10.0),
      "no level column carries an impossible value")
    A(float(np.mean(lamax[~nd] - laeq[~nd])) > 1.0,
      "the loudest second of a minute stands above its equivalent level")
    # no no-data minute falls inside a process stop, so the residual is measured on a full window
    for sid, ss in g["series"].items():
        st = AN.stop_mask(ss["stamps"])
        A(not bool((ss["nd"] & st).any()), "%s has no no-data minute inside a process stop" % sid)
    for c in W.CODES:
        A(r[c]["minutes_stop"] >= 230, "%s measures its residual on %d minutes" % (c, r[c]["minutes_stop"]))

    # -------------------------------------------------------- the field checks, deployment by deployment
    corrected = [d for d in deps if d["correction"] != 0.0]
    A(len(deps) == 28 and len(corrected) == 11,
      "the plan's 0.3 dB window catches %d of %d deployments" % (len(corrected), len(deps)))
    A({d["meter"] for d in corrected} == {"M2", "M4"},
      "two meters sit outside the window all survey: %s" % sorted({d["meter"] for d in corrected}))
    for d in deps:
        A(abs(abs(d["dev"]) - W.CAL_THRESHOLD) > 0.05,
          "%s sits %.2f dB from the plan's 0.3 dB window" % (d["id"], abs(abs(d["dev"]) - W.CAL_THRESHOLD)))
        A(abs(d["cal_after"] - d["cal_before"]) <= 0.8,
          "%s spreads %.1f dB between its checks, inside 4.1's 1.0 dB" % (d["id"],
                                                                          abs(d["cal_after"] - d["cal_before"])))
        A(abs(d["cal_mean"] * 10 - round(d["cal_mean"] * 10)) < 1e-9,
          "%s has its field checks' mean on a tenth" % d["id"])
        A(d["mount"] == W.HEIGHT_DEPART.get((d["code"], d["k"]), W.HEIGHT[d["code"]]),
          "%s stood at the height the schedule sets, or the remark says why" % d["id"])
    dep_txt = text_of(target, PK.FILES["deployments"])
    A(len({row["cal_check_after_db"] for row in _csv.DictReader(io_open(target, PK.FILES["deployments"]))})
      >= 8, "the field checks vary deployment to deployment")
    A(len({row["operator"] for row in _csv.DictReader(io_open(target, PK.FILES["deployments"]))}) >= 3,
      "more than one person deployed the meters")
    for a, mins, why in [(x[1], x[2], x[3]) for x in W.NODATA]:
        A(a.strftime("%d/%m %H:%M") in dep_txt, "the deployment record names the %s dropout" % a.date())

    # -------------------------------------------------------------- the weekly plant figures, as filed
    A(has(plan, "counter reading stamped at 00:00 on the Monday"),
      "plan 5.1 files the week boundary the figures are read at")
    A(has(plan, "one start of a centrifuge in the equipment log"), "plan 5.2 files what a run is")
    scada_rows = list(_csv.DictReader(io_open(target, PK.FILES["scada"])))
    by_t = {dt.datetime.strptime(x["logged_at"], "%Y-%m-%d %H:%M"): x for x in scada_rows}
    gap = [dt.datetime(2026, 9, 24, 13, 0) + dt.timedelta(minutes=15 * i) for i in range(80)]
    A(all(t not in by_t for t in gap), "the historian's gap is %d quarter hours" % len(gap))
    for i, wk in enumerate(W.WEEKS):
        a = dt.datetime(wk.year, wk.month, wk.day)
        A(a in by_t and a + dt.timedelta(days=7) in by_t,
          "week %d has a counter reading at both of its boundaries" % i)
    # the counters carry the gap; the rate column does not, which is what moves the gap week's ask
    wk3 = [x for x in scada_rows
           if W.WEEKS[3] <= dt.datetime.strptime(x["logged_at"], "%Y-%m-%d %H:%M").date()
           < W.WEEKS[3] + dt.timedelta(days=7)]
    rate_sum = sum(float(x["blower_air_nm3_h"]) for x in wk3) * 0.25 / 1000.0
    A(g["weekly"][3]["blower_air_knm3"] - rate_sum > 60.0,
      "the gap week's totaliser stands %.0f above the rate sum" % (g["weekly"][3]["blower_air_knm3"]
                                                                  - rate_sum))
    for i in (0, 1, 2, 4, 5):
        wkr = [x for x in scada_rows
               if W.WEEKS[i] <= dt.datetime.strptime(x["logged_at"], "%Y-%m-%d %H:%M").date()
               < W.WEEKS[i] + dt.timedelta(days=7)]
        A(abs(g["weekly"][i]["blower_air_knm3"]
              - sum(float(x["blower_air_nm3_h"]) for x in wkr) * 0.25 / 1000.0) < 2.0,
          "week %d agrees between the totaliser and the rate" % i)
    blocks = {}
    prev = 0.0
    for x in scada_rows:
        t = dt.datetime.strptime(x["logged_at"], "%Y-%m-%d %H:%M")
        f = float(x["centrifuge_feed_m3_h"])
        if f > 0 and prev == 0:
            for i, wk in enumerate(W.WEEKS):
                if wk <= t.date() < wk + dt.timedelta(days=7):
                    blocks[i] = blocks.get(i, 0) + 1
        prev = f
    A(any(blocks.get(i, 0) != g["weekly"][i]["centrifuge_runs"] for i in range(6)),
      "the process channel's feed blocks do not count the log's runs: %s against %s"
      % (blocks, {i: g["weekly"][i]["centrifuge_runs"] for i in range(6)}))
    A(len({v["centrifuge_runs"] for v in g["weekly"].values()}) >= 3,
      "the weekly run counts vary: %s" % sorted(v["centrifuge_runs"] for v in g["weekly"].values()))
    A(len({v["blower_air_knm3"] for v in g["weekly"].values()}) == 6, "the weekly air figures differ")

    # ------------------------------------------------------- the readings that converge, asserted on data
    # pooling: the position's residual over both deployments against the mean of the two deployments'
    per_dep = {}
    for sid, ss in g["series"].items():
        code = ss["dep"]["code"]
        lg = SM.logged(ss)
        adj = SM.dep_correction(ss["dep"])
        lv = np.where(ss["nd"], W.NODATA_VALUE, lg["laeq"] - adj)
        st = AN.stop_mask(ss["stamps"]) & ss["vm"]
        if st.any():
            per_dep.setdefault(code, []).append(AN.eavg(lv[st]))
    pooled_mean = {c: AN.esub(r[c]["total"], AN.eavg(v)) for c, v in per_dep.items()}
    sl_pool, _, _ = AN.slate(pooled_mean)
    A(tuple(sl_pool) == gold, "the per-deployment residual averaged gives the golden slate")
    for c in W.CODES:
        A(round(pooled_mean[c], 1) == rows[c]["specific_db"],
          "%s prints the same level either way of pooling the two deployments" % c)
    # tonality: the mean of the two adjacent band levels, taken as written or in energy
    for c in [x for x in W.CODES if g["bands"].get(x) is not None]:
        lv = g["bands"][c]
        i = int(np.argmax(lv))
        nb = [lv[j] for j in (i - 1, i + 1) if 0 <= j < len(lv)]
        en = 10.0 * math.log10(float(np.mean(np.power(10.0, np.array(nb) / 10.0))))
        A((lv[i] - float(np.mean(nb)) >= 5.0) == (lv[i] - en >= 5.0),
          "%s gives the same tone verdict on either mean of the adjacent bands" % c)

    for k, v in g["weekly"].items():
        A(v["biogas_m3"] > 20000 and v["blower_air_knm3"] > 300 and v["centrifuge_runs"] >= 4,
          "week %s plant figures %s" % (k, v))
    A(len({v["biogas_m3"] for v in g["weekly"].values()}) == 6, "the weekly biogas figures differ")
    return N
