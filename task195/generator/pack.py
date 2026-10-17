"""The parallel run's own records: the two quality-control exports, the re-run's estimates, the
identity panel register, the lookups the laboratory keeps and the export manifest."""
import csv
import datetime as dt
import json
import math
import os
import random
import re

import world as W


def _write(path, header, rows, delim=",", quoting=csv.QUOTE_MINIMAL):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh, delimiter=delim, lineterminator="\n", quoting=quoting)
        wr.writerow(header)
        wr.writerows(rows)


def nb(value, places):
    """A number as the laboratory's own systems write it, with a decimal comma."""
    if value is None or value == "":
        return ""
    return ("%%.%df" % places % value).replace(".", ",")


def week_ref(day):
    """The partner laboratory's weekly report reference for a result issued on this day."""
    friday = day + dt.timedelta(days=(4 - day.weekday()) % 7)
    return "BA-%d-W%02d" % (friday.isocalendar()[0], friday.isocalendar()[1]), friday


def write_qc(target, specimens):
    """One row per sequencing read, voided reads included, one export per instrument."""
    header = ["specimen_id", "project_code", "agreement_ref", "received_date", "instrument",
              "plate_id", "well", "read_accepted", "mean_depth", "het_excess_pct", "dna_ng_ul",
              "call_source", "hetx_call", "extract_date"]
    rows = {W.INSTRUMENTS[0]: [], W.INSTRUMENTS[1]: []}
    for s in specimens:
        accepted = s["service_flag"] is not None
        if s["replated"]:
            rows[s["instrument"]].append([
                s["specimen_id"], s["project"], s["agreement"], s["received"].isoformat(),
                s["instrument"], s["plate"][:9] + "V" + s["plate"][10:], s["well"], "N",
                "", "", "", "", "", W.AS_OF.isoformat()])
        if accepted:
            rows[s["instrument"]].append([
                s["specimen_id"], s["project"], s["agreement"], s["received"].isoformat(),
                s["instrument"], s["plate"], s["well"], "Y", nb(s["depth"], 1), nb(s["het"], 2),
                nb(s["conc"], 1), s["call_source"], "FLAG" if s["service_flag"] else "CLEAR",
                W.AS_OF.isoformat()])
        else:
            rows[s["instrument"]].append([
                s["specimen_id"], s["project"], s["agreement"], s["received"].isoformat(),
                s["instrument"], s["plate"], s["well"], "N", "", "", "", "", "",
                W.AS_OF.isoformat()])
    for key, inst in (("qc_a", W.INSTRUMENTS[0]), ("qc_b", W.INSTRUMENTS[1])):
        body = sorted(rows[inst], key=lambda r: (r[0], r[7]))
        _write(os.path.join(target, W.FILES[key]), header, body, delim=";")
    return sum(len(v) for v in rows.values())


def write_mf(target, specimens):
    """The v3.4 re-run's mixture-fraction estimate, one row per archived read set."""
    header = ["specimen_id", "read_set_id", "read_set_accepted", "mixture_fraction",
              "markers_assessed", "mean_depth", "pipeline_version", "completed_date"]
    rng = random.Random(W.SEED + 3)
    batch_days = [dt.date(2027, 6, d) for d in (9, 10, 11, 14, 15, 16, 17)]
    rows = []
    for s in specimens:
        for rs in s["read_sets"]:
            done = batch_days[(int(s["plate"][-2:]) + ord(s["plate"][9])) % len(batch_days)]
            rows.append([s["specimen_id"], rs["read_set"], "Y" if rs["accepted"] else "N",
                         "%.4f" % rs["estimate"], 148250 + rng.randint(0, 9400),
                         "%.1f" % rs["depth"], "3.4.1", done.isoformat()])
    rows.sort(key=lambda r: (r[0], r[1]))
    _write(os.path.join(target, W.FILES["mf"]), header, rows)
    return len(rows)


def panel_share(base, z):
    """What the panel types for the second contributor: the same mixture the re-run estimates, read on
    96 targeted markers, which hold up at shares where the re-run's depth does not."""
    return round(max(W.PANEL_LOD + 0.0008, (0.0075 + 0.95 * base) * math.exp(0.30 * z)), 4)


def panel_rows(specimens):
    """The partner laboratory's issued results, with the re-sends and repeat panels it issued."""
    rng = random.Random(W.SEED + 5)
    trng = random.Random(W.SEED + 23)        # the panel's typing record, off the turnaround stream
    rows = []

    def typed(verdict, draw):
        """Markers of the panel's %d that were typed. An INCONCLUSIVE result is one the panel could
        not type enough markers for.""" % W.PANEL_MARKERS
        if verdict == "INCONCLUSIVE":
            return 26 + int(46 * draw)
        return W.PANEL_MARKERS - (0 if draw < 0.55 else int(1 + 8 * draw))

    def row(sid, aliquot, request, day, seq, verdict, share, draw):
        ref, friday = week_ref(day)
        return [sid, aliquot, request, ref, friday.isoformat(), seq, verdict,
                "" if share is None else "%.4f" % share, typed(verdict, draw)]

    for s in specimens:
        if s["verdict"] is None:
            continue
        day = s["panel_from"] + dt.timedelta(days=rng.randint(12, 18))
        share = None
        if s["verdict"] == "MIXED":
            noise = rng.gauss(0.072, 0.045)
            base = (s["estimate"] if s["estimate"] is not None
                    else math.exp(trng.gauss(math.log(0.03), 0.9)))
            share = panel_share(base, (noise - 0.072) / 0.045)
        rng.randint(0, 9999)                 # the register's own request sequence, now taken from
        #                                      the biobank's register and kept here so the panel's
        #                                      turnaround clock does not move
        rows.append(row(s["specimen_id"], "A1", s["request_id"], day, 1, s["verdict"], share,
                        trng.random()))
    # verdicts the register also holds for receipts before the run window
    for k in range(912):
        sid = "NFG27-%06d" % (96000 + k * 4)
        day = dt.date(2027, 2, 2) + dt.timedelta(days=int(k * 0.093))
        verdict = "MIXED" if rng.random() < 0.064 else "CONCORDANT"
        share = (panel_share(math.exp(trng.gauss(math.log(0.028), 0.95)), rng.gauss(0.0, 1.0))
                 if verdict == "MIXED" else None)
        rows.append(row(sid, "A1", "REQ-2027-%05d" % (30500 + k), day, 1, verdict, share,
                        trng.random()))
    return rows


def devices(rows, specimens):
    """The two things the partner laboratory's own week does to its register: a batch of results
    re-sent after a courier loss, and a panel repeated on a second aliquot. Both sit on specimens the
    comparison does not hold."""
    rng = random.Random(W.SEED + 7)
    # a repeat panel can carry the other verdict, so the pool holds no specimen whose membership of
    # the comparison a second verdict could change: the comparison's own specimens and the
    # INCONCLUSIVE ones are out of it
    out_of_comparison = {s["specimen_id"] for s in specimens
                         if s["role"] in ("scope", "noread", "noest")}
    pre = {r[0] for r in rows if r[0].startswith("NFG27-09")}
    eligible = sorted([r for r in rows if r[0] in out_of_comparison or r[0] in pre],
                      key=lambda r: (r[4], r[0]))
    weeks = sorted({r[3] for r in eligible if r[4][5:7] in ("04", "05")})
    extra = []
    plan = {w: n for w, n in zip(weeks, [4, 6, 5, 3, 7, 4, 6, 5, 5])}
    for week, n in sorted(plan.items()):
        pool = [r for r in eligible if r[3] == week]
        rng.shuffle(pool)
        resend = pool[:max(1, n - 2)]
        repeat = pool[max(1, n - 2):n]
        for r in resend:                       # the same result issued a second time
            extra.append(r[:5] + [2] + r[6:])
        for r in repeat:                       # a second aliquot of the same specimen typed again
            verdict = r[6] if rng.random() < 0.72 else ("MIXED" if r[6] == "CONCORDANT" else "CONCORDANT")
            share = ("%.4f" % round(max(W.PANEL_LOD + 0.0009, math.exp(rng.gauss(math.log(0.04), 0.8))), 4)
                     if verdict == "MIXED" else "")
            extra.append([r[0], "A2", r[2], r[3], r[4], 1, verdict, share,
                          W.PANEL_MARKERS - (0 if rng.random() < 0.6 else rng.randint(1, 7))])
    return extra


def write_panel(target, specimens):
    rows = panel_rows(specimens)
    rows = rows + devices(rows, specimens)
    rows.sort(key=lambda r: (r[4], r[0], r[1], r[5]))
    header = ["specimen_id", "aliquot_id", "request_id", "report_ref", "report_date", "result_seq",
              "verdict", "second_contributor_share", "panel_markers_typed"]
    _write(os.path.join(target, W.FILES["panel"]), header, rows)
    return rows


def write_crosswalk(target, specimens):
    """The biobank's request register against the laboratory's accessions and plate barcodes."""
    rng = random.Random(W.SEED + 11)
    header = ["request_id", "specimen_id", "plate_barcode", "project_code", "registered_date",
              "biobank_ref"]
    rows = []
    for s in specimens:
        barcode = "PB%07d" % (2710000 + rng.randint(0, 89999))
        if rng.random() < 0.004:               # a barcode reissued after a printer batch was voided
            barcode = "PB%07d" % (2700000 + rng.randint(0, 999))
        stem = re.sub(r"[^A-Z0-9]", "", s["project"])[:3]
        rows.append([s["request_id"], s["specimen_id"], barcode, s["project"],
                     (s["received"] - dt.timedelta(days=rng.randint(1, 9))).isoformat(),
                     "BB-%s-%04d" % (stem, rng.randint(100, 9999))])
    rows.sort(key=lambda r: r[1])
    _write(os.path.join(target, W.FILES["crosswalk"]), header, rows, delim="\t")


def write_plates(target, specimens):
    header = ["plate_id", "well", "specimen_id", "instrument", "run_date", "control_well"]
    rows = []
    for s in specimens:
        rows.append([s["plate"], s["well"], s["specimen_id"], s["instrument"],
                     (s["received"] + dt.timedelta(days=4)).isoformat(),
                     "Y" if s["well"] in ("A01", "H12") else "N"])
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    _write(os.path.join(target, W.FILES["plates"]), header, rows)


def write_config(target):
    cfg = {"pipeline": "GKJ-PIPE", "version": "3.4.1", "run_label": "rerun-2027-03_2027-05",
           "reference_build": "GRCh38.p14", "marker_panel": "gkj-core-150k-v6",
           "contamination_estimator": {"model": "two-component allele-balance mixture",
                                       "min_mean_depth": W.DEPTH_FLOOR,
                                       "min_markers_assessed": 120000,
                                       "output_field": "mixture_fraction",
                                       "output_scale": "fraction of the specimen's reads"},
           "project_scope": [p[0] for p in W.PROJECTS],
           "input_archive": "/archive/gkj/reads/2027/03-05",
           "submitted_by": W.PEOPLE["lead"], "submitted_date": "2027-06-08",
           "notes": "Re-processing of the archived read sets for the March to May 2027 receipts of the "
                    "cohort service projects. Contract agreement receipts are not in the archive path."}
    with open(os.path.join(target, W.FILES["config"]), "w", encoding="utf-8") as fh:
        json.dump(cfg, fh, indent=2, ensure_ascii=False, sort_keys=True)
        fh.write("\n")


def write_dictionary(target):
    header = ["file", "field", "type", "definition"]
    d = [
        (W.FILES["qc_a"], "specimen_id", "text", "The laboratory accession, one per specimen received."),
        (W.FILES["qc_a"], "project_code", "text", "The project the specimen was received under."),
        (W.FILES["qc_a"], "agreement_ref", "text", "The contract agreement a receipt falls under; empty for the cohort service's own projects."),
        (W.FILES["qc_a"], "received_date", "date", "The date the specimen was received, local date."),
        (W.FILES["qc_a"], "read_accepted", "text", "Y where the laboratory accepted the read; N where the read was voided on a failed instrument control, and no call is recorded."),
        (W.FILES["qc_a"], "het_excess_pct", "number", "The specimen's autosomal heterozygosity, per cent, decimal comma."),
        (W.FILES["qc_a"], "call_source", "text", "AUTO where the screen in service produced the call; REVIEWED where the duty bioinformatician reviewed the specimen."),
        (W.FILES["qc_a"], "hetx_call", "text", "The call the screen in service (HETX) recorded for the accepted read: FLAG or CLEAR."),
        (W.FILES["qc_b"], "(all fields)", "", "As the GSQ-A export; the two instruments' exports carry the same layout."),
        (W.FILES["mf"], "read_set_id", "text", "The archived read set the estimate was computed on. A specimen has a second read set where a depth top-up library was sequenced."),
        (W.FILES["mf"], "read_set_accepted", "text", "Y on the read set the laboratory accepted for the specimen."),
        (W.FILES["mf"], "mixture_fraction", "number", "The estimated share of the specimen's reads from a second contributor, as a fraction, four decimals."),
        (W.FILES["panel"], "verdict", "text", "The identity panel's verdict: CONCORDANT, MIXED where a second contributor was typed, INCONCLUSIVE where the panel did not type enough markers."),
        (W.FILES["panel"], "report_ref", "text", "The partner laboratory's weekly report the result was issued in."),
        (W.FILES["panel"], "result_seq", "number", "The sequence number of the result for the specimen and aliquot within the report."),
        (W.FILES["panel"], "second_contributor_share", "number", "The share the panel typed for the second contributor on a MIXED verdict, as a fraction."),
        (W.FILES["history"], "received_utc", "timestamp", "The receipt timestamp as the warehouse stores it, in UTC."),
        (W.FILES["history"], "hetx_call", "text", "The automatic HETX call for the specimen, as the nightly load carries it."),
        (W.FILES["history"], "review_outcome", "text", "The duty bioinformatician's outcome where call_source is REVIEWED: FLAGGED or CLEARED. Empty where the specimen was not reviewed."),
        (W.FILES["history"], "release_status", "text", "RELEASED, WITHHELD or SUPERSEDED, as the release desk left the specimen."),
        (W.FILES["history"], "released_date", "date", "The date the specimen's result was released, local date; empty where nothing was released."),
    ]
    _write(os.path.join(target, W.FILES["dictionary"]), header,
           [[a, b, c, e] for a, b, c, e in d])


def write_manifest(target, counts):
    header = ["file", "produced_by", "pulled", "covers", "rows", "note"]
    rows = [
        [W.FILES["qc_a"], "LIMS quality-control export", W.AS_OF.isoformat(),
         "GSQ-A reads, receipts 2027-03-01 to 2027-05-31", counts["qc_a"], "semicolon delimited, decimal comma"],
        [W.FILES["qc_b"], "LIMS quality-control export", W.AS_OF.isoformat(),
         "GSQ-B reads, receipts 2027-03-01 to 2027-05-31", counts["qc_b"], "semicolon delimited, decimal comma"],
        [W.FILES["mf"], "GKJ-PIPE v3.4.1 re-run", "2027-06-18",
         "archived read sets, cohort service projects", counts["mf"], "one row per read set"],
        [W.FILES["panel"], "identity panel register", W.AS_OF.isoformat(),
         "results issued 2027-02-05 to 2027-06-18", counts["panel"], "as issued by " + W.PARTNER],
        [W.FILES["weekly"], W.PARTNER, W.AS_OF.isoformat(),
         "weekly reports, 5 March to 18 June 2027", "", "scanned to PDF as each report arrived"],
        [W.FILES["history"], "QC warehouse extract", "2027-03-04",
         "receipts 2026-02-15 to 2027-02-28", counts["history"], "nightly load, two call columns"],
        [W.FILES["volumes"], "laboratory reporting pack", "2027-03-06",
         "releases 2026-03 to 2027-02", counts["volumes"], ""],
        [W.FILES["dilution"], "analytical sensitivity run", "2027-04-02",
         "2027Q1 dilution panel", "", "prepared by the method group"],
        [W.FILES["crosswalk"], "biobank request register", W.AS_OF.isoformat(),
         "requests registered 2027-02 to 2027-05", counts["crosswalk"], "tab separated"],
        [W.FILES["protocol"], "quality system", "2027-06-21", "KVAL-07 issue 4", "", ""],
        [W.FILES["modelcard"], "bioinformatics group", "2027-06-11", "estimator v3.4", "", ""],
        [W.FILES["dictionary"], "quality system", W.AS_OF.isoformat(), "validation extracts", "", ""],
        [W.FILES["config"], "GKJ-PIPE", "2027-06-08", "re-run configuration", "", ""],
        [W.FILES["runlog"], "LIMS run log", W.AS_OF.isoformat(),
         "receipts 2027-03-01 to 2027-05-31", counts["runlog"], "one row per received aliquot"],
        [W.FILES["costs"], "finance", "2027-01-15", "2027 unit costs", counts["costs"], "NOK, excluding VAT"],
        [W.FILES["platform"], "method group", "2025-11-20", "extraction platform validation", "", ""],
        [W.FILES["plates"], "LIMS plate map", W.AS_OF.isoformat(), "2027Q2 plates", counts["plates"], ""],
    ]
    _write(os.path.join(target, W.FILES["manifest"]), header, rows)
    with open(os.path.join(target, W.FILES["manifest"]), "a", encoding="utf-8") as fh:
        fh.write("# compiled by the quality team, %s, for the KVAL-07 validation record\n"
                 % W.AS_OF.isoformat())
