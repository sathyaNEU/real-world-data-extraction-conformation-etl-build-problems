"""task212 goldens: every graded figure computed once from the record tables, then the case note and the workbook."""
import io
import datetime as dt
import numpy as np
import pandas as pd
import analysis as A
import asks
import docs
import world
from pack import V_TARGET

NAMES = {h[0]: h[2] for h in docs.HUB_ROWS}
TOWNS = {h[0]: h[3] for h in docs.HUB_ROWS}
ORDER = world.HUB_KEYS


def compute(S):
    W, R = S["W"], S["R"]
    t = A.base_table(R, W["accounts"])
    tf = t.assign(fr=t.fragile, ls=(t.load_above >= 60).astype(int))
    excess = A.cells_oe(tf, ["dshape", "wband", "fr", "ls"])
    ft = A.fit_table(t, R)
    bic_best = ft.bic.idxmin()   # the programme: the estimate with the lowest BIC stands
    excess = ft.loc[bic_best, ORDER].astype(float)
    attr = A.cells_oe(t.assign(fr=t.fragile, sv=t.service), ["dshape", "wband", "fr", "sv"])
    n = t.groupby("hubk").size()
    dam = t.groupby("hubk").dam.sum()
    obs = dam / n * 1e4
    plan = docs.peak_plan(V_TARGET)
    wk = plan[(plan.hub == "VLC") & plan.iso_week.between(48, 52)].sort_values("iso_week")
    V = float(wk.parcels.mean())
    rate = float(excess["VLC"])
    fwd = rate * V / 1e4
    CG, _ = asks.claims_golden(S["cases"], S["pays"], S["refunds"], S["trk"], S["flat"])
    SG, _ = asks.stoppages_golden(S["events"], S["wos"])
    F = {
        "call": "Ribarroja del Turia", "call_hub": NAMES["VLC"],
        "vlc_own_damage_per_10k": int(round(rate / 10.0) * 10),
        "vlc_planned_parcels_week": int(round(V)),
        "peak_weeks": "48 to 52", "peak_week_first": 48, "peak_week_last": 52, "load_edge_kg": 60,
        "rate_unit_parcels": 10000,
        "parcels_week_stopped": int(round(fwd / 100.0) * 100),
        "_zaz_audited_per_10k": round(float(obs["ZAZ"]), 1),
        "_obs": {h: round(float(obs[h]), 1) for h in ORDER},
        "_own": {h: int(round(max(0.0, float(excess[h])) / 10.0) * 10) for h in ORDER},
        "_inspected": {h: int(n[h]) for h in ORDER}, "_damaged": {h: int(dam[h]) for h in ORDER},
        "_attr": {h: round(float(attr[h]), 1) for h in ORDER},
        "_plan_weeks": {int(r.iso_week): int(r.parcels) for r in wk.itertuples()},
        "_rate_exact": rate, "_fwd_exact": fwd, "_bic_best": bic_best,
        "_eur_exact": {h: float(CG.loc[h, "claims_eur"]) for h in ORDER},
        "_hours_exact": {h: float(SG.loc[h, "hours_stood"]) for h in ORDER},
    }
    for h in ORDER:
        F["claims_%s" % h] = int(CG.loc[h, "claims"])
        F["claims_eur_%s" % h] = int(round(float(CG.loc[h, "claims_eur"])))
        F["stoppages_%s" % h] = int(SG.loc[h, "stoppages"])
        F["hours_%s" % h] = round(float(SG.loc[h, "hours_stood"]), 1)
    return F


def chart_png(F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": "#8c8c88",
                         "axes.labelcolor": "#3d3d3a", "xtick.color": "#3d3d3a", "ytick.color": "#6b6b66"})
    fig, ax = plt.subplots(figsize=(6.6, 3.2), dpi=200)
    x = np.arange(len(ORDER))
    obs = [F["_obs"][h] for h in ORDER]
    own = [F["_own"][h] for h in ORDER]
    ax.bar(x - 0.2, obs, 0.38, color="#2a78d6", edgecolor="white", linewidth=1.0, label="Audited damage, all causes")
    ax.bar(x + 0.2, own, 0.38, color="#eb6834", edgecolor="white", linewidth=1.0,
           label="Part its own sorter accounts for, at equal load in the cage")
    for i, v in enumerate(obs):
        ax.text(x[i] - 0.2, v + 4, "%.1f" % v, ha="center", va="bottom", fontsize=7.0, color="#3d3d3a")
    for i, v in enumerate(own):
        if v:
            ax.text(x[i] + 0.2, v + 4, "about %d" % v, ha="center", va="bottom", fontsize=7.0, color="#3d3d3a")
    ax.set_xticks(x)
    ax.set_xticklabels([TOWNS[h].replace(" de ", "\nde ").replace(" del ", "\ndel ") for h in ORDER], fontsize=7.4)
    ax.set_ylabel("Damaged parcels per 10,000 inspected")
    ax.set_ylim(0, max(obs) * 1.2)
    ax.yaxis.grid(True, color="#e6e6e2", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=7.2, loc="upper right")
    ax.set_title("Only Ribarroja's sorter adds damage once each parcel's load in the cage is held equal",
                 fontsize=8.6, loc="left", color="#1f1f1d")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def note(path, F):
    from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    body, h, t, small = docs.styles()

    def story():
        hdr = Table([["To", "Network operations meeting, 30 October 2026"],
                     ["From", "Julieta Barranco, head of hub engineering"],
                     ["Date", "29 October 2026"], ["Ref", "HE-2026-41, peak survey slot"]],
                    colWidths=[18 * mm, 140 * mm], hAlign="LEFT")
        hdr.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.4), ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.4),
                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5), ("TOPPADDING", (0, 0), (-1, -1), 1.5)]))
        s = [Paragraph("Peak 2026 sortation survey: book it for Ribarroja", t), hdr, Spacer(1, 7)]
        s.append(Paragraph(
            "Book the sorter maker's technician and the survey nights of 2 to 20 November at Ribarroja del Turia. "
            "Comparing each hub's audited parcels with the network's at the same load in the cage, Ribarroja's sorter "
            "damages about %d parcels per 10,000 inspected that the other hubs' sorters would not, and no other hub "
            "comes within 30 per 10,000 of it. The peak plan has Ribarroja sorting %s parcels a week over weeks 48 to 52, so the "
            "repairs should stop about <b>%s damaged parcels a week</b> through the peak."
            % (F["vlc_own_damage_per_10k"], "{:,}".format(F["vlc_planned_parcels_week"]),
               "{:,}".format(F["parcels_week_stopped"])), body))
        s += [Image(chart_png(F), width=170 * mm, height=170 * mm * 3.2 / 6.6),
              Paragraph("Source: routine audits of outbound cages, cage build logs and DWS induction records, "
                        "sorting nights 1 July to 30 September 2026.", small), Spacer(1, 4)]
        s.append(Paragraph("Why not Zaragoza", h))
        s.append(Paragraph(
            "Zaragoza Plaza has the highest audited damage, %.1f per 10,000, and it stays furthest above the network "
            "when the parcels are compared on weight, size, packaging, fragility and service, which is why it looks "
            "like the obvious hub. That excess is crush in the cage. Autorrecambios Cinca Norte's cartons come off their "
            "trailer near the end of the night and are scanned into Zaragoza's cages after almost everything else, so "
            "they ride on top of the parcels beneath them. Dos Hermanas loads Aceites y Vinos Marchenilla's cases after midnight, "
            "part way through each cage. Once each audited parcel carries its own load, the DWS weight of everything "
            "scanned into its cage after it, Zaragoza sits below the network and Dos Hermanas close to it. "
            "A sorter survey "
            "does nothing for crush under cartons; that is a loading question for the two hubs."
            % F["_zaz_audited_per_10k"], body))
        s.append(Paragraph("Why Ribarroja", h))
        s.append(Paragraph(
            "Pavimentos Benicolet's tile cartons arrive on a trailer before the sort opens and go into Ribarroja's cages "
            "first, so Ribarroja's parcels travel with almost nothing on top. Its audited damage looks middling only "
            "because its parcels are spared the crush Zaragoza's and Dos Hermanas's parcels see; Basauri, whose new "
            "paper account also arrives before the sort, sits below the network at equal load. At equal load it is the one hub "
            "clearly above the network, and it stays there whatever load edge is used between 35 and 95 kg, on the count of "
            "cartons above a parcel, or in a fitted model with the load in it. Of the estimates tried, the programme's "
            "lowest-BIC rule keeps the 60 kg step by packaging.", body))
        rows = [["Hub", "Parcels inspected", "Damaged", "Per 10,000", "Own sorter, per 10,000"]]
        for k in ORDER:
            own = F["_own"][k]
            rows.append([NAMES[k], "{:,}".format(F["_inspected"][k]), "{:,}".format(F["_damaged"][k]),
                         "%.1f" % F["_obs"][k], ("about %d" % own) if own else "none"])
        tb = Table(rows, colWidths=[34 * mm, 30 * mm, 22 * mm, 22 * mm, 36 * mm], hAlign="LEFT")
        tb.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.2), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.2),
                                ("ALIGN", (1, 1), (-1, -1), "RIGHT"), ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
                                ("LINEBELOW", (0, -1), (-1, -1), 0.3, colors.HexColor("#999999")),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
        s += [Spacer(1, 3), tb,
              Paragraph("Parcels inspected exclude lines recorded NOT FOUND and the supervisors' check audits, as the "
                        "audit procedure requires; damage codes from both lists count, the list having changed on "
                        "1 August.", small)]
        s.append(Paragraph("Claims and stoppages", h))
        s.append(Paragraph("Each hub's claims money and its sorter's stoppage record are in hub_damage_q3_2026.xlsx. "
                           "Neither changes the choice: claims follow all damage, crush included, and stoppages say "
                           "nothing about what the sorter does to the parcels it carries.", body))
        return s
    docs.pdf(path, "HE-2026-41 peak survey slot", "Julieta Barranco", docs.stamp(2026, 10, 29, 16, 40), story)


def workbook(path, F):
    rows = []
    for k in ORDER:
        rows.append((NAMES[k], F["_inspected"][k], F["_damaged"][k], F["_obs"][k], F["_own"][k],
                     F["claims_%s" % k], F["claims_eur_%s" % k], F["stoppages_%s" % k], F["hours_%s" % k]))
    hubs = pd.DataFrame(rows, columns=["Hub", "Parcels inspected", "Damaged", "Audited damage per 10,000",
                                       "Own sorter damage per 10,000", "Damaged parcels with approved claim",
                                       "Claims paid (EUR)", "Sorter stoppages", "Hours stood"])
    ins, dam = sum(F["_inspected"].values()), sum(F["_damaged"].values())
    tot = pd.DataFrame([("Network", ins, dam, round(dam / ins * 1e4, 1), None,
                         sum(F["claims_%s" % k] for k in ORDER), int(round(sum(F["_eur_exact"].values()))),
                         sum(F["stoppages_%s" % k] for k in ORDER), round(sum(F["_hours_exact"].values()), 1))],
                       columns=hubs.columns)
    hubs = pd.concat([hubs, tot], ignore_index=True)
    wk = pd.DataFrame([(w, p) for w, p in sorted(F["_plan_weeks"].items())], columns=["ISO week", "Planned parcels"])
    surv = pd.DataFrame([("Survey hub", F["call"]),
                         ("Own sorter damage per 10,000 inspected, at equal load", F["vlc_own_damage_per_10k"]),
                         ("Planned parcels a week, peak weeks 48 to 52", F["vlc_planned_parcels_week"]),
                         ("Damaged parcels a week stopped over the peak", F["parcels_week_stopped"])],
                        columns=["Item", "Value"])
    notes = pd.DataFrame([
        ("Population", "Parcels found in routine audits of outbound cages built on the sorting nights of 1 July to "
                       "30 September 2026; NOT FOUND lines and check audits left out (audit procedure v4)."),
        ("Own sorter damage", "Damaged parcels per 10,000 inspected above the six-hub expectation at equal load: "
                              "the lowest-BIC logistic estimate (shape, log weight, fragility, service, heavy-carton "
                              "flag, and 60 kg or more scanned in on top, by packaging), to the nearest 10; none "
                              "where at or below (survey programme, section 2)."),
        ("Claims", "Damaged parcels whose first case was approved by 20 October, a flat-rate case counting each damaged "
                   "carton it covers, charged to the hub of the parcel's first sort; money paid by 20 October by "
                   "transfer or card refund (note CS-FIN 07)."),
        ("Stoppages", "Spells the sorter stood still on the sorting nights, whichever record shows them, each once "
                      "(standard ENG-11)."),
        ("As of", "Audits closed 9 October 2026; claims export 23 October 2026; prepared 29 October 2026.")],
        columns=["Item", "Note"])
    docs.sheet_xlsx(path, [("Hubs Q3 2026", hubs), ("Survey", surv), ("Ribarroja peak plan", wk), ("Notes", notes)],
                    "Hub Engineering", "2026-10-29T16:30:00Z", "Hub damage Q3 2026",
                    widths={"Hub": 16, "Item": 46, "Value": 20, "ISO week": 10, "Planned parcels": 16, "Note": 100,
                            "Audited damage per 10,000": 14, "Own sorter damage per 10,000": 14,
                            "Damaged parcels with approved claim": 16, "Claims paid (EUR)": 14},
                    numfmt={"Parcels inspected": "#,##0", "Damaged": "#,##0", "Claims paid (EUR)": "#,##0",
                            "Planned parcels": "#,##0", "Hours stood": "0.0", "Audited damage per 10,000": "0.0",
                            "Damaged parcels with approved claim": "#,##0"})


