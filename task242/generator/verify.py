"""task242 independent verifier: reads only the shipped bundle (target/), the goldens, figures.json and submission.md;
recomputes the call by its own route (the panel's sensitivity in fixed bins of days since onset, each zone's cases by
onset week), both asks by its own code, reads back every format the pack ships, and requires the goldens and the
write-up to carry the same figures."""
import json
import os
import re
import sys

import numpy as np
import pandas as pd
from openpyxl import load_workbook

ZONES = ["Kadalur", "Thenkarai", "Puthanpalli", "Melmangalam", "Vadakkupatti", "Kizhakkoor", "Velliyanur",
         "Chinnakulam", "Periyamalai", "Kottaivayal", "Sengalur", "Aranmanai"]


def canon(s):
    t = re.sub(r"[^a-z]", "", str(s).lower())
    if t.startswith("nonresident"):
        return None
    roman = {"zonei": 0, "zoneii": 1, "zoneiii": 2, "zoneiv": 3, "zonev": 4, "zonevi": 5, "zonevii": 6, "zoneviii": 7,
             "zoneix": 8, "zonex": 9, "zonexi": 10, "zonexii": 11}
    if t in roman:
        return ZONES[roman[t]]
    t = t.replace("zone", "")
    near = {"kadaloor": "kadalur", "puthenpalli": "puthanpalli", "vadakupatti": "vadakkupatti", "kizhakkur": "kizhakkoor",
            "velliyanoor": "velliyanur", "periamalai": "periyamalai", "sengaloor": "sengalur"}
    t = near.get(t, t)
    for z in ZONES:
        if t == z.lower():
            return z
    return None


def pdf_text(p):
    from pypdf import PdfReader
    return " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(p).pages)


def docx_text(p):
    import docx
    return " ".join(x.text for x in docx.Document(p).paragraphs)


def main(target, golden, figures, submission):
    fig = json.load(open(figures))
    rd = lambda f, **kw: pd.read_csv(os.path.join(target, f), **kw)
    # read back every format the pack ships, each document carrying a filed sentence the build leans on
    reg = load_workbook(os.path.join(target, "epi_cell_indicator_register.xlsx"), data_only=True)
    rows = [r for r in reg["Register 2027"].iter_rows(values_only=True) if r[0] == "SERO-D1"]
    assert rows and "between 1 January 2027 and the collection of their survey specimen" in rows[0][3], "verify: register"
    sop = pdf_text(os.path.join(target, "sop_epi_07_quality_flags.pdf"))
    assert "more than one and a half times the published value or less than two thirds of it" in sop, "verify: SOP M"
    prot = docx_text(os.path.join(target, "serosurvey_2027_protocol.docx"))
    assert "in which at least one member gave a blood specimen" in prot, "verify: protocol response rate"
    vc = pdf_text(os.path.join(target, "vector_surveillance_sop_extract.pdf"))
    assert "Positive containers per 100 houses inspected" in vc, "verify: SOP-VC-02"
    for f in ("flag_review_request.eml", "igm_lot_verification_cover_note.eml"):
        t = open(os.path.join(target, f), encoding="utf-8").read()
        assert t.startswith("From: ") and "Subject: " in t, "verify: %s" % f
    bul = pdf_text(os.path.join(target, "dengue_bulletin_dec2027.pdf"))
    # the published values
    res = rd("serosurvey_2027_igm_results.csv", dtype={"household_id": str})
    res["collected"] = pd.to_datetime(res["collected_on"])
    pub = {z: (int((res["zone"] == z).sum()), int(((res["zone"] == z) & (res["igm_result"] == "REACTIVE")).sum()))
           for z in ZONES}
    for z in ZONES:
        n, a = pub[z]
        assert "%s %d %.1f" % ("{:,}".format(n), a, 100.0 * a / n) in bul, ("verify: bulletin row", z)
    # the assay: sensitivity in fixed bins of days since onset, specificity from the controls
    pan = rd("ngmc_igm_lot_verification_panel.csv", dtype=str)
    cs = pan[pan["arm"] == "CONFIRMED CASE"].copy()
    cs["d"] = (pd.to_datetime(cs["collected_on"], dayfirst=True) - pd.to_datetime(cs["onset_date"], dayfirst=True)).dt.days
    cs["y"] = (cs["result_final"] == "REACTIVE").astype(float)
    edges = [0, 5, 10, 18, 25, 38, 53, 68, 83, 105, 135, 1000]
    se_b = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        x = cs[(cs["d"] >= lo) & (cs["d"] < hi)]
        se_b.append(x["y"].mean() if len(x) else 0.0)
    se_b = np.array(se_b)

    def se(d):
        d = np.asarray(d)
        i = np.clip(np.searchsorted(edges, d, side="right") - 1, 0, len(se_b) - 1)
        return np.where(d < 0, 0.0, se_b[i])
    ct = pan[pan["arm"] == "NEGATIVE CONTROL"]
    sp = 1.0 - (ct["result_final"] == "REACTIVE").mean()
    ll = rd("ncmc_dengue_line_list_2026_27.csv", dtype=str)
    ll["z"] = ll["zone"].map(canon)
    ll["on"] = pd.to_datetime(ll["onset_date"], dayfirst=True)
    ll = ll[ll["z"].notna() & (ll["on"] >= "2027-01-01")]
    flagged, est = [], {}
    for z in ZONES:
        days = ((ll[ll["z"] == z]["on"] - pd.Timestamp("2027-01-01")).dt.days).values
        n = np.bincount(days, minlength=400).astype(float)
        dd = np.arange(n.size)
        x = res[res["zone"] == z]
        s = np.mean([np.sum(n * (dd < c) * se(c - dd)) / np.sum(n * (dd < c))
                     for c in ((x["collected"] - pd.Timestamp("2027-01-01")).dt.days).values])
        nn, a = pub[z]
        p = a / nn
        A = (p + sp - 1) / (s + sp - 1)
        est[z] = 100 * A
        if A / p > 1.5 or A / p < 2 / 3:
            flagged.append(z)
    assert flagged == fig["call"]["flagged"], ("verify: the call", flagged)
    band = fig["components"]["band"]
    for z in ZONES:
        assert abs(est[z] / fig["deliverables"]["estimated"][z] - 1) < band, ("verify: estimate outside the band", z)
    # ask A: the Breteau index (zone from the premise's assessment number)
    ins = rd("dbc_house_inspections_nov2027.csv", dtype={"premise_id": str}).drop_duplicates()
    ins = ins[ins["remarks"].fillna("") != "LOCKED"].sort_values(["inspected_on", "record_id"])
    first = ins.groupby("premise_id").head(1)
    first = first.assign(z=[ZONES[int(p[:2]) - 1] for p in first["premise_id"]])
    for z in ZONES:
        x = first[first["z"] == z]
        v = round(100.0 * x["positive_containers"].sum() / len(x), 1)
        assert v == fig["deliverables"]["breteau"][z], ("verify: Breteau", z, v)
    # ask B: households where a member's specimen reached the laboratory
    smp = rd("serosurvey_2027_household_sample.csv", dtype=str)
    vis = rd("serosurvey_2027_visits_kobo_export.csv", dtype={"household_id": str})
    vis = vis.drop_duplicates(subset=["household_id", "start"]).sort_values(["household_id", "start"])
    last = vis.groupby("household_id")["visit_outcome"].last()
    lab = rd("ngmc_serology_specimen_register_survey.csv", dtype=str)
    gave = {b.split("-")[1] + "-" + b.split("-")[2] for b in lab["barcode"]}
    for z in ZONES:
        h = smp[smp["zone"] == z]["household_id"]
        occ = [x for x in h if last.get(x) not in (4, 5)]
        v = round(100.0 * sum(x in gave for x in occ) / len(occ), 1)
        assert v == fig["deliverables"]["response"][z], ("verify: response rate", z, v)
    # the goldens carry the figures
    wb = load_workbook(os.path.join(golden, "dengue_igm_flag_review_2027.xlsx"), data_only=True)
    ws = wb["Flag review"]
    got = 0
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r[0] and str(r[0]).split(" ", 1)[-1] in ZONES:
            z = str(r[0]).split(" ", 1)[1]
            assert r[4] == fig["deliverables"]["published"][z] and r[5] == fig["deliverables"]["estimated"][z], ("wb", z)
            assert (r[7] == "M") == (z in flagged) and r[8] == fig["deliverables"]["breteau"][z] and \
                r[9] == fig["deliverables"]["response"][z], ("verify: workbook row", z)
            got += 1
    assert got == 12, "verify: workbook rows"
    from pptx import Presentation
    deck = Presentation(os.path.join(golden, "dengue_igm_flags_health_committee.pptx"))
    assert len(deck.slides) == 1, "verify: one slide"
    txt = " ".join(sh.text_frame.text for sh in deck.slides[0].shapes if sh.has_text_frame)
    assert all(z in txt for z in flagged) and not any(z in txt.split("Flagged (M):")[1].split(".")[0]
                                                      for z in ZONES if z not in flagged), "verify: slide text"
    sub = open(submission).read()
    for z in ZONES:
        line = re.search(r"- [IVX]+ %s: ([\d.]+); ([\d.]+); (M|no flag)" % z, sub)
        assert line and float(line.group(1)) == fig["deliverables"]["published"][z] and \
            float(line.group(2)) == fig["deliverables"]["estimated"][z] and (line.group(3) == "M") == (z in flagged), \
            ("verify: submission row", z)
        assert "%s %.1f" % (z, fig["deliverables"]["breteau"][z]) in sub and \
            "%s %.1f" % (z, fig["deliverables"]["response"][z]) in sub, ("verify: submission asks", z)
    print("verify: call (%d flagged), estimates within %d per cent, both asks, every format read back, goldens and "
          "write-up agree" % (len(flagged), int(round(100 * band))))


if __name__ == "__main__":
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(os.path.join(task, "target"), os.path.join(task, "golden"),
         os.path.join(task, "generator", "figures.json"), os.path.join(task, "submission.md"))
