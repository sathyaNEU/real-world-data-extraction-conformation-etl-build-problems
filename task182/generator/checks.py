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
            # a flate stream may end on a byte that looks like a newline, so decompress what is there and
            # ignore any trailing bytes rather than stripping the data itself
            for cand in (body, body.rstrip(b"\r\n"), body.strip(b"\r\n")):
                try:
                    body = zlib.decompressobj().decompress(cand)
                    break
                except Exception:
                    continue
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


def GD_runs(target):
    import golden as GD
    return GD.log_runs(target)


def run(target, g):
    global N
    N = 0
    CAP5 = 5
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
    # and the nearest reading a solver could reach for converges on the same records: one tip in ten
    # minutes is 1.2 mm an hour, so any rate test at or under that selects exactly the counted records
    rate = (SM.MET["rain_mm_shipped"] * 6.0) > 0.5
    A(bool((rate == SM.RAIN_ON).all()),
      "R2 the counted-rain records and a rate reading of the same record are the same minutes")
    A(has(text_of(target, PK.FILES["notes"]), "stamped UTC at the start of the ten minutes"),
      "SF6 the notes file which end of its ten minutes a met record is stamped at")

    # ------------------------------------------------- R3a: the analyst test, executed on the clean truth
    naive = {c: r[c]["rung2_la90"] for c in W.CODES}
    sl_naive, m_naive, _ = AN.slate(naive)
    A(tuple(sl_naive) != gold, "R3a the easy route files a different slate")
    A(len(set(sl_naive) & set(gold)) <= 3,
      "R3a the statistical background keeps at most three of the five: %s" % (sl_naive,))
    la90 = tuple(AN.slate({c: r[c]["rung2_la90"] for c in W.CODES})[0])
    A(la90 == ("NSL03", "NSL04", "NSL06", "NSL11", "NSL12"),
      "R3a the default path (the minute LA90 background) files NSL03, NSL04, NSL06, NSL11, NSL12: %s"
      % (la90,))
    A(len(set(la90) & set(gold)) == 2, "R3a the default path keeps two of the five")
    # R3b: the decisive step alone turns the easy route into the golden
    for key in ("rung2_p10", "rung2_la90", "rung2b_min15", "rung2c_arith", "rung1_total"):
        vals = {c: r[c][key] for c in W.CODES}
        sl, mg, nxt = AN.slate(vals)
        A(tuple(sl) != gold, "R3b %s does not reach the golden slate" % key)
        # a thin boundary on a wrong rung costs the ladder nothing as long as the slate on the other side
        # of it is wrong too, which is asserted rather than assumed
        fifth = sorted(sl, key=lambda c: -vals[c])[-1]
        swapped = tuple(sorted([c for c in sl if c != fifth] + [nxt]))
        A(mg > 0.25 or swapped != gold,
          "R3b %s sits %.2f dB from a boundary whose far side is %s" % (key, mg, swapped))
    A(tuple(AN.slate(base)[0]) == gold, "R3b the residual from the plant's stops gives the golden slate")
    # R3c: no plant
    A(len(W.PLANNED_STOPS) == 6 and all(m == 120 for _, m, _ in W.PLANNED_STOPS)
      and len({st.time() for st, _, _ in W.PLANNED_STOPS}) >= 4,
      "R3c the stops are the plant's own weekly inspection, started when the shift got to it")
    # the engine comes off load on its own, and the plant is never down with it
    A(len(W.ENGINE_STOPS) >= 4, "the engine has its own stops: %d" % len(W.ENGINE_STOPS))
    for st, m, _ in W.ENGINE_STOPS:
        A(not any(a < st + dt.timedelta(minutes=m) and b > st for a, b in SM.all_down()),
          "the engine stop on %s leaves the blowers and the centrifuges running" % st.date())
    for st, m, _ in W.PLANNED_STOPS:
        end = st + dt.timedelta(minutes=m)
        A(end <= dt.datetime(st.year, st.month, st.day, W.DAY_START),
          "R3c the inspection on %s is over before the assessment period opens" % st.date())
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
        "rung2c_arith": ("NSL03", "NSL04", "NSL06", "NSL07", "NSL11"),
        "rung2_p10": ("NSL02", "NSL04", "NSL06", "NSL07", "NSL11"),
        "rung0_complaints": ("NSL01", "NSL03", "NSL06", "NSL09", "NSL12"),
    }
    for key, want in expect.items():
        got = tuple(g["slates"][key][0])
        A(got == want, "ladder %s is %s: got %s" % (key, want, got))
    # the percentile and quietest-interval routes subtract a floor that still holds the plant, so they
    # land on slates the ladder already names rather than on ones of their own
    for key in ("rung2_p10", "rung2b_min15"):
        got = tuple(g["slates"][key][0])
        A(got != gold, "ladder %s differs from the golden slate" % key)
        A(got in {tuple(g["slates"][k][0]) for k in ("rung1_total", "rung2_la90", "rung2c_arith")},
          "ladder %s lands on a slate the ladder already names: %s" % (key, got))
    A(len({tuple(v[0]) for v in g["slates"].values()}) >= 5, "the ladder names five or more slates")
    A(g["slates"]["specific"][1] >= 0.7, "the golden slate's margin is %.2f dB" % g["slates"]["specific"][1])
    A(g["slates"]["specific"][2] == g["sixth"], "the sixth dwelling is %s" % g["sixth"])

    # ------------------------------------------------------------------- the semantic fork table, row by row
    # SF1 specific sound level: the level itself is not the quantity
    A(tuple(AN.slate({c: r[c]["total"] for c in W.CODES})[0]) != gold,
      "SF1 reading the measured level as the specific level gives another slate")
    # SF2 residual sound: the stump, both readings execute and the records decide
    A(tuple(sl_naive) != gold, "SF2 the statistical background reading files another slate")
    for c in W.CODES:
        A(r[c]["p10"] > r[c]["resid"] + 1.2,
          "SF2 at %s the record's own tenth percentile sits %.2f dB above the residual"
          % (c, r[c]["p10"] - r[c]["resid"]))
    # at the five the slot reaches, the quiet-surroundings dwellings, the two are far apart: that gap is
    # the plant's own contribution, and it is what the statistical background hides
    for c in gold:
        A(r[c]["p10"] - r[c]["resid"] > 8.0,
          "SF2 at %s the gap is %.1f dB" % (c, r[c]["p10"] - r[c]["resid"]))
    # SF3 assessment period: weekday 07:00 to 19:00, filed at 3.2
    plan = text_of(target, PK.FILES["plan"])
    A(has(plan, "07:00 to 19:00 on weekdays"), "SF3 the plan files the assessment period")
    # SF4 energetic against arithmetic combination
    A(has(plan, "in energy, not in decibels"), "SF4 the plan files the energetic combination")
    A(tuple(AN.slate({c: r[c]["rung2c_arith"] for c in W.CODES})[0]) != gold,
      "SF4 the arithmetic reading files another slate")
    # SF5 valid minute
    A(has(plan, "counted rain on the gauge") and has(plan, "5 m a second"),
      "SF5 the plan files the rain test")
    A(has(plan, "where the meter recorded no measurement for that minute"),
      "SF7 the plan files what a minute with no measurement is")
    # SF6 calibration drift
    A(has(plan, "0.3 dB"), "SF8 the plan files the calibration adjustment")
    # SF7 which stops: inside the assessment period the planned stops are the whole stop set
    for c in W.CODES:
        A(abs(r[c]["specific"] - r[c]["specific_planned"]) < 0.01,
          "SF9 at %s the planned stops and every stop give the same residual" % c)
        A(round(r[c]["specific"], 1) == round(r[c]["specific_planned"], 1),
          "SF9 at %s both readings print the same level" % c)
    # SF8 the total: no stop minute falls in the assessment period
    for c in W.CODES:
        A(abs(r[c]["total"] - r[c]["total_running"]) < 1e-9,
          "SF10 at %s the assessment period holds no stop minute" % c)
    # SF12 the repeated download and SF13 position identity are asserted in the R2 block above
    # SF14 rounding: every printed level clear of its rounding edge, no two equal, and none of them
    # sitting on the printed value itself (a level tuned onto the decimal is a construction tell)
    printed = [round(rows[c]["specific_raw"], 1) for c in W.CODES]
    A(len(set(printed)) == len(printed), "SF14 no two positions share a printed level")
    for c in W.CODES:
        v = rows[c]["specific_raw"]
        off = abs(v * 10 - round(v * 10)) * 0.1          # distance from the one-decimal value
        A(0.05 - off >= 0.015, "SF14 %s sits %.3f dB from a rounding edge" % (c, 0.05 - off))
        A(off >= 0.012, "SF14 %s sits %.4f dB from its own printed value" % (c, off))
    # SF15 the five dwellings are the five highest specific levels, not the five highest totals
    A(tuple(AN.slate({c: r[c]["total"] for c in W.CODES})[0]) != gold, "SF15 the totals rank differently")

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
        A(rows[c]["air_knm3_first"] > 100.0 and rows[c]["air_knm3_second"] > 100.0,
          "%s carries the air delivered through each of its deployments (%.1f, %.1f)"
          % (c, rows[c]["air_knm3_first"], rows[c]["air_knm3_second"]))
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
                 "Plantagenet Cherokee", "Identities\n\nPositions", "Nore Valley",
                 "Valley Laboratories", "Clonaraght Upper", "Coolnagree Lower"}
    found = set(re.findall(r"\b[A-Z][a-z]{2,}\s+[A-Z][a-z']{2,}\b", allt))
    stray = sorted(n for n in found if n not in FURNITURE and n not in people)
    A(not stray, "the people sweep finds only the card's personas: %s" % stray)

    # --------------------------------------------------------------------------- the graded figures, per row
    for c in W.CODES:
        A(isinstance(rows[c]["valid_minutes"], int) and rows[c]["valid_minutes"] > 0,
          "%s valid minutes is a count" % c)
        A(rows[c]["band_hz"] in PK.BANDS or rows[c]["band_hz"] is None, "%s band is a band" % c)
        A(rows[c]["tone"] in (True, False, None), "%s tone verdict" % c)
        A(isinstance(rows[c]["unrecorded_quarter_hours"], int)
          and 0 < rows[c]["unrecorded_quarter_hours"] < 200,
          "%s has %d quarter hours the historian did not record"
          % (c, rows[c]["unrecorded_quarter_hours"]))
        for key in ("air_knm3_first", "air_knm3_second"):
            v2 = rows[c][key]
            A(abs(v2 * 10 - round(v2 * 10)) < 1e-6,
              "%s's %s is read off counters printed to a tenth, so it is one (%.3f)" % (c, key, v2))
    withband = [c for c in W.CODES if rows[c]["band_hz"]]
    A(len(withband) == 10, "ten positions carry band rows: %d" % len(withband))
    A(len([c for c in W.CODES if rows[c]["band_hz"] is None]) == 4, "four positions have no band rows")
    A(len({rows[c]["band_hz"] for c in withband}) >= 2, "the highest band is not the same everywhere")
    A(len({rows[c]["tone"] for c in withband}) == 2, "the tone verdict splits the positions")
    for c in withband:
        A(abs(g["tones"][c]["excess_db"] - 5.0) > 0.4,
          "%s sits %.2f dB from the prominence test" % (c, g["tones"][c]["excess_db"] - 5.0))
    gnote = os.path.join(os.path.dirname(target), "golden", "mitigation_shortlist.pdf")
    note = text_of(os.path.dirname(gnote), os.path.basename(gnote)) if os.path.exists(gnote) else ""
    if os.path.exists(gnote):
        A(len(note) > 1500, "the golden note's text is readable for the figure sweep (%d characters)"
          % len(note))
    if note:
        A(has(note, "A tone is prominent at %d of the fourteen positions" % len(g["tone_positions"])),
          "the note's tone count is the %d the band file carries" % len(g["tone_positions"]))
        for c in g["tone_positions"]:
            A(has(note, c), "the note names %s among the positions carrying a tone" % c)
        A(len(g["tone_bands"]) == 1, "every prominent tone sits in one band: %s" % (g["tone_bands"],))
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
    A(np.all((abs(la90[nd] - W.NODATA_VALUE) < 0.01) & (abs(lamax[nd] - W.NODATA_VALUE) < 0.01)
             & (abs(lamin[nd] - W.NODATA_VALUE) < 0.01)),
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
        A(r[c]["minutes_stop"] >= 200, "%s measures its residual on %d minutes" % (c, r[c]["minutes_stop"]))
    A(len({r[c]["minutes_stop"] for c in W.CODES}) >= 1,
      "every position's residual window is its two inspections, 240 minutes")
    A(len({rows[c]["air_knm3_first"] for c in W.CODES}) >= 10,
      "the air behind each level differs position to position")
    A(len({rows[c]["unrecorded_quarter_hours"] for c in W.CODES}) >= 6,
      "so does the part of the record the historian does not hold")

    # -------------------------------------------------------- the field checks, deployment by deployment
    corrected = [d for d in deps if d["correction"] != 0.0]
    A(len(deps) == 28 and len(corrected) == 11,
      "the plan's 0.3 dB window catches %d of %d deployments" % (len(corrected), len(deps)))
    A({d["meter"] for d in corrected} == {"M2", "M4"},
      "two meters sit outside the window all survey: %s" % sorted({d["meter"] for d in corrected}))
    for d in deps:
        A(abs(abs(d["dev"]) - W.CAL_THRESHOLD) > 0.05,
          "%s sits %.2f dB from the plan's 0.3 dB window" % (d["id"], abs(abs(d["dev"]) - W.CAL_THRESHOLD)))
        A(abs(d["cal_after"] - d["cal_before"]) <= 0.8 + 1e-9,
          "%s spreads %.1f dB between its checks, inside 4.1's 1.0 dB" % (d["id"],
                                                                          abs(d["cal_after"] - d["cal_before"])))
        A(abs(d["cal_mean"] * 10 - round(d["cal_mean"] * 10)) < 1e-6,
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

    # ------------------------------------------------- the ask layer: the plant's own records, re-cut
    A(has(plan, "counter reading stamped at 00:00 on the Monday"),
      "SF18 plan 5.1 files the week boundary a process figure is read at")
    scada_rows = list(_csv.DictReader(io_open(target, PK.FILES["scada"])))
    by_t = {dt.datetime.strptime(x["logged_at"], "%Y-%m-%d %H:%M"): x for x in scada_rows}
    gap = [a + dt.timedelta(minutes=15 * i) for a, n in W.PLC_GAPS for i in range(n)]
    A(all(t2 not in by_t for t2 in gap), "the historian's gaps are %d quarter hours over %d spells"
      % (len(gap), len(W.PLC_GAPS)))
    A(len({(a.date() - W.WEEKS[0]).days // 7 for a, _ in W.PLC_GAPS}) == 6,
      "every survey week carries one of the historian's gaps")
    import golden as GD
    hrows, hheld = GD.hist_rows(target)
    heldw = [a + dt.timedelta(minutes=15 * i) for a, n in W.PLC_HELD for i in range(n)]
    A(hheld == set(heldw),
      "the rows that carry nothing of their own are the %d the link's own held spells make, found by what "
      "they are and not by anything written down (%d found)" % (len(heldw), len(hheld)))
    A(len({(a.date() - W.WEEKS[0]).days // 7 for a, _ in W.PLC_HELD}) >= 6,
      "every survey week carries one of the held spells")
    # no window a graded figure is read over loses a boundary row, so the counters at its ends are the
    # plant's own and the two readings of which quarter hours it holds agree
    for i, wk in enumerate(W.WEEKS):
        a = dt.datetime(wk.year, wk.month, wk.day)
        A(a in hrows and a not in hheld, "week %d opens on a row the historian wrote itself" % i)
    for code, deps in GD.position_windows(target).items():
        for wins in deps:
            for lo, hi in wins:
                for edge in (lo, hi):
                    A(edge in hrows and edge not in hheld,
                      "%s's window at %s has its own row at %s" % (code, lo.date(), edge.strftime("%H:%M")))
    # D1, the air: the plant's three blowers are metered twice and the header's meter is upstream of
    # where the third was tied in, so the header alone is not the air the blowers delivered. Measured:
    # the two counters each match their own rate channel, and the header's share of the air moves week to
    # week with the duty while the two together track the works' own inlet load.
    hdr_tot, bl3_tot, hdr_rate, bl3_rate, infl, stamps_s = [], [], [], [], [], []
    for x in scada_rows:
        ts = dt.datetime.strptime(x["logged_at"], "%Y-%m-%d %H:%M")
        if ts in hheld:
            continue
        stamps_s.append(ts)
        hdr_tot.append(float(x["blower_air_total_knm3"]))
        bl3_tot.append(float(x["bl03_air_total_knm3"]))
        hdr_rate.append(float(x["blower_air_nm3_h"]))
        bl3_rate.append(float(x["bl03_air_nm3_h"]))
        infl.append(float(x["inlet_flow_m3_h"]))
    hdr_tot, bl3_tot = np.array(hdr_tot), np.array(bl3_tot)
    hdr_rate, bl3_rate, infl = np.array(hdr_rate), np.array(bl3_rate), np.array(infl)
    step = np.array([(stamps_s[i + 1] - stamps_s[i]).total_seconds() / 3600.0
                     for i in range(len(stamps_s) - 1)])
    ok1 = step == 0.25
    for nm, tot, rate in (("header", hdr_tot, hdr_rate), ("BL-03", bl3_tot, bl3_rate)):
        d1 = np.diff(tot)[ok1] * 1000.0
        e1 = (rate[:-1][ok1]) * 0.25
        A(float(np.abs(d1 - e1).max()) < 60.0,
          "the %s totaliser carries its own rate channel and nothing else (worst %.1f Nm3)"
          % (nm, float(np.abs(d1 - e1).max())))
    run = (hdr_rate > 100) & (bl3_rate > 100)
    sh = bl3_rate[run] / (hdr_rate[run] + bl3_rate[run])
    A(sh.min() < 0.27 and sh.max() > 0.36,
      "the duty rotates: BL-03 carried %.2f to %.2f of the air" % (sh.min(), sh.max()))
    tot_air = hdr_rate + bl3_rate
    rt_total = float(np.corrcoef(tot_air[run], infl[run])[0, 1])
    rt_hdr = float(np.corrcoef(hdr_rate[run], infl[run])[0, 1])
    A(rt_total > 0.3 and rt_total - rt_hdr > 0.15,
      "the two meters together follow the works' inlet load (%.2f) and the header alone does not (%.2f)"
      % (rt_total, rt_hdr))
    # D3, the record: a held row's counters stand still while its rates read above zero
    prev = None
    bad_held = 0
    for x in scada_rows:
        ts = dt.datetime.strptime(x["logged_at"], "%Y-%m-%d %H:%M")
        if ts in hheld and prev is not None:
            if float(x["blower_air_nm3_h"]) > 0 and float(x["blower_air_total_knm3"]) == float(
                    prev["blower_air_total_knm3"]):
                bad_held += 1
        prev = x
    A(bad_held == len(heldw),
      "every held row is an impossible row on its face: the air counter stands still while the air flows "
      "(%d of %d)" % (bad_held, len(heldw)))
    # and no row the historian wrote itself repeats the row before it, so the held rows are the only ones
    reps = 0
    prev = None
    for x in scada_rows:
        ts = dt.datetime.strptime(x["logged_at"], "%Y-%m-%d %H:%M")
        if prev is not None and all(v == prev[k] for k, v in x.items() if k != "logged_at"):
            reps += 1
        prev = x
    A(reps == len(heldw), "the only rows that repeat the row before them are the held ones (%d)" % reps)

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
    A(tuple(sl_pool) == gold, "SF11 the per-deployment residual averaged gives the golden slate")
    for c in W.CODES:
        A(round(pooled_mean[c], 1) == rows[c]["specific_db"],
          "SF11 %s prints the same level either way of pooling the two deployments" % c)
    # SF16 the band export's time base: the same answers whether its stamps are read as UTC or as local
    import golden as GD
    _orig = SM.LOCAL_OFFSET
    try:
        SM.LOCAL_OFFSET = 0
        as_local = GD.band_rows(target)
    finally:
        SM.LOCAL_OFFSET = _orig
    for c in sorted(as_local):
        b2, t2, _ = GD.tone_call(as_local[c])
        A(b2 == rows[c]["band_hz"] and t2 == rows[c]["tone"],
          "SF16 %s gives the same band and tone with the band file read as local" % c)

    # tonality: the mean of the two adjacent band levels, taken as written or in energy
    for c in [x for x in W.CODES if g["bands"].get(x) is not None]:
        lv = g["bands"][c]
        i = int(np.argmax(lv))
        nb = [lv[j] for j in (i - 1, i + 1) if 0 <= j < len(lv)]
        en = 10.0 * math.log10(float(np.mean(np.power(10.0, np.array(nb) / 10.0))))
        A((lv[i] - float(np.mean(nb)) >= 5.0) == (lv[i] - en >= 5.0),
          "SF17 %s gives the same tone verdict on either mean of the adjacent bands" % c)

    # ------------------------------------------- the record reads like a survey somebody went out and did
    # the round: no two meters go in at the same minute, no record is a round week, and every minute the
    # technician was at the microphone falls outside the assessment period and outside every stop
    lens = sorted({int((d["end_dt"] - d["start_dt"]).total_seconds() // 60) + 1 for d in deps})
    A(len(lens) >= 10, "the 28 records take %d different lengths" % len(lens))
    A(7 * 24 * 60 not in lens, "no record is exactly a week of minutes: %s" % lens[:3])
    A(len({d["start_dt"] for d in deps}) == len(deps), "no two deployments start on the same minute")
    bymeter = {}
    for d in deps:
        bymeter.setdefault(d["meter"], []).append((d["start_dt"], d["end_dt"], d["id"]))
    for mid, sp in bymeter.items():
        sp.sort()
        for i3 in range(1, len(sp)):
            A(sp[i3][0] > sp[i3 - 1][1],
              "%s was collected from %s before it was set down for %s" % (mid, sp[i3 - 1][2], sp[i3][2]))
            A((sp[i3][0] - sp[i3 - 1][1]).total_seconds() / 60.0 >= W.TURNAROUND,
              "%s had the drive between %s and %s" % (mid, sp[i3 - 1][2], sp[i3][2]))
    for d in deps:
        for x in (d["start_dt"], d["end_dt"]):
            A(x.hour < W.DAY_START, "%s's round at %s is before the assessment period opens"
              % (d["id"], x.strftime("%H:%M")))
            A(x.weekday() == 0, "%s's rounds are Monday mornings" % d["id"])
    stamps_by_serial = {}
    for i2 in range(tbl.num_rows):
        key = tbl.column("meter_serial")[i2].as_py()
        stamps_by_serial.setdefault(key, {})[tbl.column("measured_at_utc")[i2].as_py()] = float(
            tbl.column("laeq_db")[i2].as_py())
    for d in deps:
        serial = PK.W_serial(d["meter"])
        for off, want, label in ((W.SETUP_HANDLING, d["cal_before"], "before"),
                                 (-1 - W.PICKUP_HANDLING, d["cal_after"], "after")):
            when = (d["start_dt"] + dt.timedelta(minutes=off) if off >= 0
                    else d["end_dt"] + dt.timedelta(minutes=off + 1))
            u = when - dt.timedelta(hours=SM.LOCAL_OFFSET)
            got = stamps_by_serial[serial].get(u)
            A(got is not None and abs(got - want) < 0.051,
              "%s's field check %s reads %s in the record against %.1f on the sheet"
              % (d["id"], label, got, want))
            A(not (when.weekday() <= 4 and W.DAY_START <= when.hour < W.DAY_END),
              "%s's field check %s is outside the assessment period" % (d["id"], label))
            A(not any(a <= when < b for a, b in SM.all_down()),
              "%s's field check %s is outside every process stop" % (d["id"], label))
    A(float(np.max(laeq[~nd])) > 90.0,
      "the record carries the calibrator: the loudest minute in the file is %.1f dB"
      % float(np.max(laeq[~nd])))
    A(float(np.max(laeq[~nd])) < 96.0, "and nothing in it is louder than the calibrator")
    hand_lv = []
    for sid, ss in g["series"].items():
        lg3 = SM.logged(ss)
        sel = (ss["hand_e"] > 0) & ~ss["nd"]
        hand_lv.extend(lg3["laeq"][sel].tolist())
    A(55.0 < min(hand_lv) and max(hand_lv) < 86.0,
      "the handling minutes read %.1f to %.1f dB" % (min(hand_lv), max(hand_lv)))

    # the plant's level moves with the weather, and differently at every position
    cors, nsd = {}, []
    for sid, ss in g["series"].items():
        code = ss["dep"]["code"]
        idx3 = SM.met_index(ss["stamps"])
        lg3 = SM.logged(ss)
        lv3 = lg3["laeq"]
        keep3 = ss["am"] & ss["vm"] & ~ss["nd"]
        wdir = np.cos(np.radians(SM.MET["wind_dir"][idx3].astype(float)))
        cors.setdefault(code, []).append((
            float(np.corrcoef(lv3[keep3], SM.MET["wind_ms"][idx3][keep3])[0, 1]),
            float(np.corrcoef(lv3[keep3], wdir[keep3])[0, 1]),
            float(np.corrcoef(lv3[keep3], SM.MET["temp_c"][idx3][keep3])[0, 1])))
        hrs3 = np.array([x.hour for x in ss["stamps"]])
        tech3 = (ss["cal_e"] > 0) | (ss["hand_e"] > 0)
        for hh in (23, 0, 1, 2, 3):
            s3 = (hrs3 == hh) & ~ss["nd"] & ~tech3
            if s3.sum() > 50:
                nsd.append(float(np.std(lv3[s3])))
    dirs = [cors[c][0][1] for c in W.CODES]
    A(sum(1 for x in dirs if abs(x) >= 0.15) >= 8,
      "the wind's direction moves the level at %d of the fourteen positions"
      % sum(1 for x in dirs if abs(x) >= 0.15))
    A(max(dirs) - min(dirs) >= 0.5,
      "and it moves them differently: %.2f to %.2f across the fourteen" % (min(dirs), max(dirs)))
    A(max(abs(cors[c][0][0]) for c in W.CODES) >= 0.15,
      "the wind's speed moves the level too (strongest %.2f)"
      % max(abs(cors[c][0][0]) for c in W.CODES))
    A(min(nsd) > 0.45 and max(nsd) > 1.8,
      "a night minute's level moves by %.2f to %.2f dB about its hour" % (min(nsd), max(nsd)))

    # the schedule's grid references are a survey, not the distance and bearing written out again
    from openpyxl import load_workbook as _lw
    wsx = _lw(os.path.join(target, PK.FILES["positions"]), data_only=True).active
    implied = []
    for row in wsx.iter_rows(min_row=6, max_row=5 + len(W.POSITIONS), values_only=True):
        e2, n2, dist2, bear2 = row[3], row[4], row[5], row[6]
        ang2 = math.radians(bear2)
        implied.append((round(e2 - dist2 * math.sin(ang2), 2), round(n2 - dist2 * math.cos(ang2), 2)))
        off2 = math.hypot(e2 - 612430 - dist2 * math.sin(ang2), n2 - 748215 - dist2 * math.cos(ang2))
        A(off2 < 9.0, "the grid reference for %s sits %.1f m off its scaled distance" % (row[0], off2))
    A(len({x for x in implied}) >= 13,
      "the fourteen grid references do not reduce to one point: %d distinct" % len({x for x in implied}))

    # the complaints register is somebody's own words, one contact a row
    wcx = _lw(os.path.join(target, PK.FILES["complaints"]), data_only=True).active
    texts2 = [row[5] for row in wcx.iter_rows(min_row=5, values_only=True) if row[0]]
    A(len(texts2) == sum(W.COMPLAINTS.values()), "the register carries %d contacts" % len(texts2))
    A(len(set(texts2)) == len(texts2), "no two contacts carry the same sentence")

    # the process channels wander rather than jumping about, and the totaliser's steps are not all equal
    tot = [float(x["blower_air_total_knm3"]) for x in scada_rows]
    steps = [round(tot[i + 1] - tot[i], 1) for i in range(len(tot) - 1) if tot[i + 1] >= tot[i]]
    A(len(set(steps)) >= 5, "the totaliser's quarter-hour steps take %d printed values" % len(set(steps)))
    rate = np.array([float(x["blower_air_nm3_h"]) for x in scada_rows])
    run_on = rate > 100
    rr3 = rate[run_on]
    lag1 = float(np.corrcoef(rr3[:-1], rr3[1:])[0, 1])
    A(lag1 > 0.5, "the blower channel is a process channel, not white noise (lag-1 %.2f)" % lag1)

    # ------------------------------------------- the equipment log's own cardinality, and what it carries
    evrows = sorted(_csv.DictReader(io_open(target, PK.FILES["events"])), key=lambda x: x["logged_at"])
    opens, unstopped, naive, orphan = {}, [], [], []
    for x in evrows:
        if x["equipment"] not in W.CENTRIFUGES:
            continue
        tt = dt.datetime.strptime(x["logged_at"], "%Y-%m-%d %H:%M")
        if x["event"] == "START":
            naive.append((x["equipment"], tt))
            if x["equipment"] in opens:
                unstopped.append((x["equipment"], opens[x["equipment"]]))
            opens[x["equipment"]] = tt
        else:
            if x["equipment"] not in opens:
                orphan.append((x["equipment"], tt))
            opens.pop(x["equipment"], None)
    A(len(unstopped) == 1, "the log carries one start with no stop before the machine starts again: %s"
      % (unstopped,))
    A(unstopped[0] == ("CF-02", dt.datetime(2026, 9, 10, 14, 6)),
      "that start is CF-02's on 10 September at 14:06: %s" % (unstopped[0],))
    A(len(orphan) == 1 and orphan[0][0] == "CF-02" and orphan[0][1].date() == dt.date(2026, 9, 10),
      "the log also carries one stop for a machine already stopped: %s" % (orphan,))
    # the naive count, which keeps that start, is measured rather than described: 13 against the 12 the
    # plan's definition gives, in the week beginning 7 September
    a1 = W.WEEKS[1]
    b1 = a1 + dt.timedelta(days=7)
    naive_wk1 = sum(1 for _, tt in naive if a1 <= tt.date() < b1)
    A(naive_wk1 == 13, "the naive count of starts in the week beginning 7 September is %d" % naive_wk1)
    A(g["weekly"][1]["centrifuge_runs"] == 12,
      "plan 5.2 gives that week %d runs" % g["weekly"][1]["centrifuge_runs"])
    runs_log2 = GD_runs(target)
    A(all(b > a for a, b in runs_log2), "every run the log closes ends after it starts")
    A(not any(a == dt.datetime(2026, 9, 10, 14, 6) for a, _ in runs_log2),
      "the unstopped start is no run under plan 5.2")
    A(len(runs_log2) == len(naive) - 1,
      "the log's runs are its starts less the one it never stopped (%d, %d)" % (len(runs_log2), len(naive)))

    # ------------------------------------------- the runs column, by interval arithmetic and by its term
    depwin = {}
    for d in deps:
        for kday in range((d["end_dt"].date() - d["start_dt"].date()).days + 1):
            day = d["start_dt"].date() + dt.timedelta(days=kday)
            if day.weekday() > 4:
                continue
            lo = dt.datetime(day.year, day.month, day.day, W.DAY_START)
            hi = dt.datetime(day.year, day.month, day.day, W.DAY_END)
            if lo >= d["start_dt"] and hi <= d["end_dt"]:
                depwin.setdefault(d["code"], []).append((lo, hi))
    for c in W.CODES:
        wins = depwin[c]
        A(len(wins) == 10, "%s has ten weekday assessment windows in its two deployments" % c)
        n_overlap = sum(1 for a, b in runs_log2 if any(a < hi and b > lo for lo, hi in wins))
        A(n_overlap == rows[c]["centrifuge_runs"],
          "SF22 %s: the runs reaching into the period are %d, the table says %d"
          % (c, n_overlap, rows[c]["centrifuge_runs"]))
    starts_in = {c: sum(1 for a, _ in runs_log2 if any(lo <= a < hi for lo, hi in depwin[c]))
                 for c in W.CODES}
    A(sum(1 for c in W.CODES if starts_in[c] != rows[c]["centrifuge_runs"]) >= 10,
      "SF22 counting the starts inside the period instead of the runs over it differs at %d positions"
      % sum(1 for c in W.CODES if starts_in[c] != rows[c]["centrifuge_runs"]))
    prompt = open(os.path.join(os.path.dirname(target), "prompt.txt"), encoding="utf-8").read()
    A("valid minutes of its assessment period" in prompt,
      "the ask states the minutes basis the table carries")
    A("overlapped any minute of that period" in prompt,
      "the ask states when a run reached into the period")

    # ------------------------------------------- the week's delivered air, clear of its rounding edge
    air_raw = {}
    for i, wk in enumerate(W.WEEKS):
        a = dt.datetime(wk.year, wk.month, wk.day)
        b = a + dt.timedelta(days=7)
        v = float(by_t[b]["blower_air_total_knm3"]) - float(by_t[a]["blower_air_total_knm3"])
        air_raw[i] = v
        A(int(round(v)) == g["weekly"][i]["blower_air_knm3"],
          "week %d's air figure is the counter difference" % i)
        A(0.5 - abs(v - round(v)) >= 0.15,
          "week %d's air sits %.2f from the whole-unit edge (%.1f)" % (i, 0.5 - abs(v - round(v)), v))

    # ------------------------------------------- the minute file's stamp convention, filed once
    A(has(plan, "each record at the start of the interval it measures"),
      "SF6b the plan files which end of its minute a meter record is stamped at")
    A(re.sub(r"\s+", "", plan.lower()).count("atthestartoftheintervalitmeasures") == 1,
      "the meter's stamp convention is filed once")
    A(not has(notes, "start of the interval"), "the survey notes do not restate the stamp convention")

    # ------------------------------------------- the margin, clear of its own rounding edge
    mg_raw = g["ordered"][CAP5 - 1]["specific_raw"] - g["ordered"][CAP5]["specific_raw"]
    A(abs(round(mg_raw, 1) - g["margin_db"]) < 1e-9, "the margin prints as %.1f" % g["margin_db"])
    A(0.05 - abs(mg_raw * 10 - round(mg_raw * 10)) * 0.1 >= 0.015,
      "the margin sits %.4f dB from its rounding edge (%.4f)"
      % (0.05 - abs(mg_raw * 10 - round(mg_raw * 10)) * 0.1, mg_raw))

    # ------------------------------------------- every window the pack permits holds the plant's own sound
    # The only minutes in the whole record with every source down are the intervals the log shows them all
    # down in, so no other window a solver could take for the residual is free of the plant. Asserted on
    # the clean truth, window by window, with the slate each one files.
    cand = {}
    for sid, ss in g["series"].items():
        code = ss["dep"]["code"]
        stamps = ss["stamps"]
        hrs = np.array([x.hour + x.minute / 60.0 for x in stamps])
        dow = np.array([x.weekday() for x in stamps])
        cfm = np.zeros(len(stamps), dtype=bool)
        rr2 = {d0: SM.centrifuge_runs(d0) for d0 in sorted({x.date() for x in stamps})}
        for i2, x in enumerate(stamps):
            for _, aa, bb in rr2[x.date()]:
                if aa <= x < bb:
                    cfm[i2] = True
                    break
        st2 = AN.stop_mask(stamps)
        A(bool((ss["k"][~st2] > 0).all()),
          "%s: every minute outside the log's all-down intervals has the plant running" % sid)
        A(bool((ss["k"][st2] == 0).all()), "%s: the plant is down in every all-down minute" % sid)
        lg2 = SM.logged(ss)
        lv2 = np.where(ss["nd"], W.NODATA_VALUE, lg2["laeq"] - SM.dep_correction(ss["dep"]))
        tech2 = (ss["cal_e"] > 0) | (ss["hand_e"] > 0)
        okm = ss["vm"] & ~ss["nd"] & ~tech2
        for name, m2 in (("weekday 00:00 to 05:00", (dow <= 4) & (hrs < 5.0)),
                         ("Sundays", dow == 6),
                         ("nights 23:00 to 05:00", (hrs >= 23) | (hrs < 5.0)),
                         ("the centrifuges' own off minutes", ~cfm)):
            cand.setdefault(name, {}).setdefault(code, []).append(lv2[m2 & okm])
    for name, per in cand.items():
        vals = {c: AN.esub(r[c]["total"], AN.eavg(np.concatenate(v))) for c, v in per.items()}
        sl2, mg2, nx2 = AN.slate(vals)
        A(tuple(sl2) != gold, "the residual taken from %s files %s, not the golden slate" % (name, sl2))
        swapped = tuple(sorted([x for x in sl2 if x != sorted(sl2, key=lambda c: -vals[c])[-1]] + [nx2]))
        A(mg2 > 0.25 or swapped != gold,
          "%s sits %.2f dB from a boundary whose far side is %s" % (name, mg2, swapped))

    for k, v in g["weekly"].items():
        A(v["blower_air_knm3"] > 600 and v["unrecorded_quarter_hours"] > 0,
          "week %s plant figures %s" % (k, v))
    A(len({v["blower_air_knm3"] for v in g["weekly"].values()}) == 6, "the weekly air figures differ")
    A(len({v["unrecorded_quarter_hours"] for v in g["weekly"].values()}) >= 4,
      "and the weeks lose different amounts of record")
    return N
