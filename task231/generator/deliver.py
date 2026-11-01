"""task231 architecture 2: the golden deliverables and figures.json, written from analysis.solve() on the pack.

    rwis_spatial_check_review_2027.xlsx   every station: the spatial test review, the Schedule B and MDSS hours
    spatial_check_retune_memo_2027.docx   the re-tune list for Quillan, with the chart of every station's share
"""
import io
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import openpyxl  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.shared import Cm, Pt, RGBColor  # noqa: E402
from openpyxl.styles import Alignment, Font  # noqa: E402

import analysis as A  # noqa: E402
import params as P  # noqa: E402
import postprocess as PP  # noqa: E402

BOOK, MEMO = P.DELIVERABLES


def r1(x):
    """a share as the workbook and the memo print it"""
    return float("%.1f" % (x + 1e-9))


def table_rows(S):
    M, Asla, B, reg = S["M"], S["A"], S["B"], S["reg"]
    out = []
    for k, s in enumerate(reg["sites"]):
        out.append({"site": s["site"], "name": s["name"], "z": int(s["z"]), "withheld": int(M["withheld"][k]),
                    "fr": int(M["fr"][k]), "share": r1(M["share"][k]), "retune": k in M["retune"],
                    "unavailable": int(Asla["unavailable"][k]), "excluded": int(Asla["excluded"][k]),
                    "freezing": int(B["freezing"][k]), "ice": int(B["ice"][k])})
    return out


def workbook(rows, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Spatial test review"
    hdr = ["Site code", "Site name", "Elevation (m)", "Hours withheld by the spatial test", "False-rejection hours",
           "False-rejection share of winter hours (%)", "Re-tune before winter 2027/28"]
    ws.append(hdr)
    for r in rows:
        ws.append([r["site"], r["name"], r["z"], r["withheld"], r["fr"], r["share"], "Yes" if r["retune"] else "No"])
    for c in ws[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for row in ws.iter_rows(min_row=2, min_col=6, max_col=6):
        for c in row:
            c.number_format = "0.0"
    n = len(rows) + 1
    ws.cell(row=n + 2, column=1, value="Winter 1 October 2026 00:00 to 1 May 2027 00:00 Mountain time (%s hours). "
                                       "A station is re-tuned where its share is above 2 per cent (Data Quality "
                                       "Standard Rev 2, section 3)." % format(P.NH, ","))
    for i, w in enumerate([10, 22, 11, 16, 14, 18, 16]):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w
    ws.row_dimensions[1].height = 45
    ws.freeze_panes = "A2"
    ws2 = wb.create_sheet("Service and pavement")
    hdr2 = ["Site code", "Site name", "Unavailable hours (Schedule B)", "Excluded hours (planned outages)",
            "Freezing hours (travel lane)", "Ice hours (travel lane)"]
    ws2.append(hdr2)
    for r in rows:
        ws2.append([r["site"], r["name"], r["unavailable"], r["excluded"], r["freezing"], r["ice"]])
    for c in ws2[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws2.append(["Total", None, sum(r["unavailable"] for r in rows), sum(r["excluded"] for r in rows),
                sum(r["freezing"] for r in rows), sum(r["ice"] for r in rows)])
    for c in ws2[ws2.max_row]:
        c.font = Font(bold=True)
    for i, w in enumerate([10, 22, 15, 15, 14, 12]):
        ws2.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w
    ws2.row_dimensions[1].height = 45
    ws2.freeze_panes = "A2"
    wb.save(path)
    PP.normalize_ooxml(path, P.PEOPLE["engineer"][0], P.PEOPLE["engineer"][0], "2027-05-19T15:08:00Z",
                       "2027-05-21T22:47:00Z", excel=True, company=P.ORG)


def chart(rows):
    order = sorted(rows, key=lambda r: (r["share"], r["site"]))
    vals = [r["share"] for r in order]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
    fig, ax = plt.subplots(figsize=(6.4, 6.6), dpi=150)
    col = ["#b5523b" if r["retune"] else "#7f9fb3" for r in order]
    y = list(range(len(order)))
    ax.barh(y, vals, color=col, height=0.66)
    ax.axvline(P.RETUNE_LINE_PCT, color="#333333", lw=1.0, ls="--")
    ax.text(P.RETUNE_LINE_PCT + 0.15, 1.0, "re-tune line, 2 per cent", fontsize=7.5, color="#333333")
    for yy, r in zip(y, order):
        if r["share"] > 0:
            ax.text(r["share"] + 0.12, yy, "%.1f" % r["share"], va="center", fontsize=7)
    ax.set_yticks(y)
    ax.set_yticklabels(["%s %s" % (r["site"], r["name"]) for r in order], fontsize=7)
    ax.set_xlim(0, max(vals) * 1.12)
    ax.set_xlabel("False rejections by the spatial test, per cent of winter 2026/27 hours")
    ax.set_title("Spatial test false-rejection share by station, winter 2026/27", fontsize=9.5, loc="left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def _cell(c, text, bold=False, right=False, size=8.5):
    c.text = ""
    p = c.paragraphs[0]
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    if right:
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT


def memo(rows, S, path):
    ret = [r for r in rows if r["retune"]]
    below = sorted([r for r in rows if not r["retune"]], key=lambda r: -r["share"])
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.2)
        s.top_margin = Cm(1.8)
        s.bottom_margin = Cm(1.8)
        fp = s.footer.paragraphs[0]
        fp.text = "%s  |  Maintenance Division, ITS  |  internal" % P.ORG
        fp.runs[0].font.size = Pt(8)
        fp.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    for k, v in [("To", "%s, ITS Program Manager" % P.PEOPLE["manager"][0]),
                 ("From", "%s, ITS Engineer" % P.PEOPLE["engineer"][0]), ("Date", "21 May 2027"),
                 ("Subject", "Spatial test re-tune list for winter 2027/28")]:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run("%s:\t" % k)
        r.bold = True
        p.add_run(v)
    doc.add_paragraph()
    h = doc.add_paragraph()
    r = h.add_run("Re-tune the air temperature spatial test at %s stations before winter 2027/28: %s." % (
        {8: "eight"}.get(len(ret), str(len(ret))), ", ".join("%s %s" % (x["site"], x["name"]) for x in ret)))
    r.bold = True
    r.font.size = Pt(12)
    doc.add_paragraph(
        "Under section 3 of the data quality standard a station goes on the list when the spatial test withheld a "
        "right air temperature in more than 2 per cent of the winter's hours. These stations were at %s per cent; "
        "the highest of the other stations was %.1f per cent, so none is close to the line." % (
            ", ".join("%.1f" % x["share"] for x in sorted(ret, key=lambda x: x["site"])), below[0]["share"]))
    doc.add_paragraph(
        "Most of what the test withheld at these stations was the basins' cold air on still nights. Halvorsen "
        "Meadow, Teller Junction and Bitterbrush Flat read together, as do Cutler Meadow and Ransom Creek, and "
        "their cold readings were the air: each withheld reading agrees with the other floor stations of its "
        "basin that hour. Kimball Grade, Echo Grade and Ptarmigan Grade sit above those pools; the test's estimate "
        "for them leans on the cold floor stations close by, and their withheld readings agree with the passes "
        "and benches around them carried to their elevation. A check against the regional lapse line, or "
        "against the HRRR forecast, calls the floor readings wrong, because neither has the pools in it.")
    doc.add_paragraph(
        "What the test withheld at Monument Pass and Thunder Saddle (rime on the probe), Sapphire Hill (a "
        "connector fault), Big Prairie (sun on the radiation shield) and Fenwick (a wet filter in the spring) was "
        "wrong, and was rightly withheld; those stations are not on the list.")
    t = doc.add_table(rows=1, cols=5)
    t.style = "Light Grid Accent 1"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c, x in zip(t.rows[0].cells, ["Station", "Elevation (m)", "Hours withheld", "False-rejection hours",
                                       "Share (%)"]):
        _cell(c, x, bold=True)
    for x in ret:
        cells = t.add_row().cells
        for k, (c, v) in enumerate(zip(cells, ["%s %s" % (x["site"], x["name"]), "{:,}".format(x["z"]),
                                               "{:,}".format(x["withheld"]), "{:,}".format(x["fr"]),
                                               "%.1f" % x["share"]])):
            _cell(c, v, right=k > 0)
    p = doc.add_paragraph()
    r = p.add_run("Share: winter hours with a false rejection by the spatial test, as a percentage of the %s hours "
                  "from 1 October 2026 00:00 to 1 May 2027 00:00 Mountain time." % format(P.NH, ","))
    r.font.size = Pt(8)
    doc.add_picture(chart(rows), width=Cm(15.5))
    tot_un = sum(x["unavailable"] for x in rows)
    doc.add_paragraph(
        "The workbook has every station's review line, its Schedule B unavailable hours (%s across the network) "
        "and its travel-lane freezing and ice hours for the section reports." % format(tot_un, ","))
    p = doc.add_paragraph()
    r = p.add_run("Sources: ESS atmospheric export and Quillan QC withheld log, winter 2026/27; RWIS site register; "
                  "central server message log, modem register and planned outage notices; pavement sensor "
                  "export.")
    r.font.size = Pt(8)
    doc.save(path)
    PP.normalize_ooxml(path, P.PEOPLE["engineer"][0], P.PEOPLE["engineer"][0], "2027-05-20T16:30:00Z",
                       "2027-05-21T23:05:00Z", company=P.ORG)


def figures(rows, S):
    ret = [r for r in rows if r["retune"]]
    below = sorted([r for r in rows if not r["retune"]], key=lambda r: -r["share"])
    f = {"retune_sites": [r["site"] for r in ret], "retune_count": len(ret), "winter_hours": P.NH,
         "winter_hours_s": format(P.NH, ","), "highest_below": "%.1f" % below[0]["share"],
         "line": "2", "stations": {}}
    for r in rows:
        f["stations"][r["site"]] = {"share": "%.1f" % r["share"], "withheld": r["withheld"], "fr": r["fr"],
                                    "unavailable": r["unavailable"], "excluded": r["excluded"],
                                    "freezing": "{:,}".format(r["freezing"]), "ice": r["ice"],
                                    "z": "{:,}".format(r["z"])}
    f["total_unavailable"] = format(sum(r["unavailable"] for r in rows), ",")
    f["total_freezing"] = format(sum(r["freezing"] for r in rows), ",")
    f["total_ice"] = format(sum(r["ice"] for r in rows), ",")
    f["total_excluded"] = sum(r["excluded"] for r in rows)
    return f


def write_all(target, golden_dir, here):
    import writeup as WU
    S = A.solve(target)
    S["target"] = target
    rows = table_rows(S)
    os.makedirs(golden_dir, exist_ok=True)
    workbook(rows, os.path.join(golden_dir, BOOK))
    memo(rows, S, os.path.join(golden_dir, MEMO))
    fig = WU.enrich(figures(rows, S), rows, S)
    json.dump(fig, open(os.path.join(here, "figures.json"), "w"), indent=1, sort_keys=True)
    open(os.path.join(here, "figures.json"), "a").write("\n")
    return fig, rows, S
