"""task197 golden deliverables, written from generator/figures.json (every figure computed once, in build.py):
packaging_referral.docx (the referral), referral_tables.xlsx (the changed products' effects and the antidote courses)
and effects_chart.png (each changed product's effect against the 1.20 line). Two runs are byte-identical."""
import os, sys, json, re, zipfile, shutil, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import world

TASK = os.path.dirname(HERE)
GOLD = os.path.join(TASK, "golden")
F = json.load(open(os.path.join(HERE, "figures.json")))
SAVED = dt.datetime(2026, 11, 6, 15, 42, 0)
MEMO_DATE = "6 November 2026"
HALF = {"2025 H1": "January to June 2025", "2025 H2": "July to December 2025", "2026 H1": "January to June 2026"}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
INK, INK2, MUTED, ACCENT, GRID, SURF = "#0b0b0b", "#52514e", "#9a9993", "#2a78d6", "#dddcd6", "#ffffff"
WORDS = {6: "six", 7: "seven", 8: "eight"}


def month_label(ym):
    y, m = ym.split("-")
    return "%s %s" % (MONTHS[int(m) - 1], y)


def day_label(iso):
    d = dt.date.fromisoformat(iso)
    return "%d %s %d" % (d.day, MONTHS[d.month - 1], d.year)


def e1(x):
    return "%.1f" % x


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def office_container(path, kind, words=None):
    """Repack an Office file with one fixed entry time, the saving application's own name and save time, and no
    template thumbnail, so a rebuild is byte-identical and the container reads as the office suite wrote it."""
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    out = []
    for name, data in items:
        if name == "docProps/thumbnail.jpeg":
            continue
        if name == "_rels/.rels":
            data = re.sub(rb'<Relationship [^>]*thumbnail[^>]*/>', b"", data)
        if name == "xl/workbook.xml":
            import docs
            data = docs.strip_workbook_defaults(data)
        if name == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                          rb"\g<1>" + iso(SAVED).encode() + rb"\g<2>", data)
        if name == "docProps/app.xml":
            if kind == "xlsx":
                data = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                        b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
                        b'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
                        b'<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity>'
                        b'<ScaleCrop>false</ScaleCrop><Company>' + world.NETWORK.encode() + b'</Company>'
                        b'<LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
                        b'<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')
            else:
                n_words, n_chars = words
                data = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
                        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
                        '<Template>Normal.dotm</Template><TotalTime>52</TotalTime><Pages>2</Pages>'
                        '<Words>%d</Words><Characters>%d</Characters><Application>Microsoft Office Word</Application>'
                        '<DocSecurity>0</DocSecurity><Lines>%d</Lines><Paragraphs>%d</Paragraphs>'
                        '<ScaleCrop>false</ScaleCrop><Company>%s</Company><LinksUpToDate>false</LinksUpToDate>'
                        '<CharactersWithSpaces>%d</CharactersWithSpaces><SharedDoc>false</SharedDoc>'
                        '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>'
                        % (n_words, n_chars, n_chars // 92 + 1, 19, world.NETWORK, n_chars + n_words)).encode()
        out.append((name, data))
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in out:
            zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
    shutil.move(tmp, path)


# ------------------------------------------------------------------------------------------------ the workbook
def _head(ws, cols, row):
    thin = Side(style="thin", color="BFBFBF")
    for c in range(1, len(cols) + 1):
        cell = ws.cell(row, c)
        cell.value = cols[c - 1]
        cell.font = Font(name="Calibri", bold=True, size=10)
        cell.fill = PatternFill("solid", fgColor="DCE6F1")
        cell.alignment = Alignment(wrap_text=True, vertical="center",
                                   horizontal="left" if c <= 3 else "right")
        cell.border = Border(bottom=thin, top=thin)
    ws.row_dimensions[row].height = 30


def _title(ws, title, note, last_col):
    ws["A1"] = title
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws["A2"] = note
    ws["A2"].font = Font(name="Calibri", italic=True, size=9, color="595959")
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:%s2" % last_col)
    ws.row_dimensions[2].height = 40


def _print(ws, head_row):
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = "%d:%d" % (head_row, head_row)


def workbook(path):
    wb = Workbook()
    thin = Side(style="thin", color="BFBFBF")
    hl_fill = PatternFill("solid", fgColor="FFF2CC")

    ws = wb.active
    ws.title = "Packaging changes"
    _title(ws, "Watched products whose packaging changed between 1 January 2024 and 30 September 2025",
           "Effect: accidental exposures of children under six recorded in the twelve calendar months after the month "
           "the changed pack was first sold at retail, divided by the number the product's packs would have produced "
           "in those months with the previous packaging (CRP-3, section 3). A referral needs at least 1.20 "
           "(section 4).", "G")
    cols = ["Product code", "Product", "Changed packaging", "Changed pack first sold at retail", "Months read",
            "Accidental exposures, children under six", "Effect", "Reaches 1.20"]
    hr = 4
    _head(ws, cols, hr)
    r = hr
    for e in F["effects"]:
        r += 1
        vals = [e["product_code"], e["product"], world.META[e["code"]]["closure_new"],
                dt.date.fromisoformat(e["change"]),
                "%s to %s" % (month_label(e["window"][0]), month_label(e["window"][1])), e["observed"], e["effect"],
                "Yes" if e["reaches"] else "No"]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(r, c, v)
            cell.font = Font(name="Calibri", size=10, bold=bool(e["reaches"]))
            cell.border = Border(bottom=thin)
            cell.alignment = Alignment(vertical="top", wrap_text=c in (2, 3), horizontal="left" if c <= 3 else "right")
            if e["reaches"]:
                cell.fill = hl_fill
        ws.cell(r, 4).number_format = "d mmm yyyy"
        ws.cell(r, 6).number_format = "#,##0"
        ws.cell(r, 7).number_format = "0.0"
    ws.cell(r + 2, 1, "Source: network case export pulled 2 November 2026; %s four-week point-of-sale data (revised "
                      "release, with the preliminary release for the latest period only); watched-product register of "
                      "30 October 2026." % world.PROVIDER).font = Font(name="Calibri", italic=True, size=9, color="595959")
    for col, w in zip("ABCDEFGH", (13, 42, 34, 15, 30, 17, 8, 9)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "C5"
    _print(ws, hr)

    ws2 = wb.create_sheet("Antidote courses")
    _title(ws2, "Antidote courses started at the network's children's hospitals, January 2025 to June 2026",
           "From the hospitals' pharmacy antidote preparation records, 1 July 2024 to 31 October 2026. Each course is "
           "counted once, in the half-year its first bag was prepared. Deferoxamine prepared for a transfusion "
           "admission is not a course for an iron poisoning and is left out.", "F")
    cols2 = ["Hospital code", "Hospital", "Half-year", "Acetylcysteine courses started",
             "Deferoxamine courses started for an iron poisoning", "Both antidotes"]
    _head(ws2, cols2, hr)
    r = hr
    for a in F["antidote"]:
        r += 1
        vals = [a["hospital"], a["name"], HALF[a["half"]], a["acetylcysteine_courses"], a["deferoxamine_courses"],
                a["antidote_courses"]]
        for c, v in enumerate(vals, 1):
            cell = ws2.cell(r, c, v)
            cell.font = Font(name="Calibri", size=10)
            cell.border = Border(bottom=thin)
            cell.alignment = Alignment(horizontal="left" if c <= 3 else "right")
    ws2.cell(r + 2, 1, "Source: %s, network_hospitals list and antidote preparation records as returned by the four "
                       "hospitals' pharmacies." % world.NETWORK).font = Font(name="Calibri", italic=True, size=9,
                                                                            color="595959")
    for col, w in zip("ABCDEF", (13, 36, 22, 16, 24, 12)):
        ws2.column_dimensions[col].width = w
    ws2.freeze_panes = "D5"
    _print(ws2, hr)

    ws3 = wb.create_sheet("Notes")
    notes = [
        ("Prepared", "%s, as at %s, for the network's referral under procedure CRP-3 (issue 4)." % (
            world.PEOPLE["lead"], MEMO_DATE)),
        ("Exposures", "Cases the member centers recorded with reason Unintentional - general in a patient under six "
                      "at the time of the call, counted for the product code on the substance line, in the calendar "
                      "month of the recorded call date (procedure sections 3.2 and 3.3)."),
        ("Expected exposures", "Each product's packs in use rebuilt from its point-of-sale units, each four-week "
                               "period's units spread evenly over its days, run down at a constant monthly rate; the "
                               "rate and the exposures per pack in use fitted to the product's monthly exposures from "
                               "January 2019 to the month before its change, then run forward over the months read."),
        ("Months read", "The twelve calendar months starting the first day of the month after the changed pack was "
                        "first sold at retail. The month of the first sale itself is in neither the fit nor the twelve "
                        "months."),
        ("Rounding", "Effects are rounded to one decimal at the end; whether an effect reaches 1.20 is read on the "
                     "unrounded effect, which gives the same answer for every product here."),
        ("Antidote courses", "Acetylcysteine bags are grouped into courses by the regimen the first bag fits (three "
                             "bags or two) and the patient weight its dose implies; a course stopped after its first "
                             "bag or extended by a further bag is still one course. Deferoxamine for an iron poisoning "
                             "runs in eight-hour bags at one dose; bags of one dose prepared on consecutive evenings "
                             "are transfusion admissions."),
    ]
    ws3["A1"] = "Notes"
    ws3["A1"].font = Font(name="Calibri", bold=True, size=12)
    for i, (k, v) in enumerate(notes, 3):
        ws3.cell(i, 1, k).font = Font(name="Calibri", bold=True, size=10)
        ws3.cell(i, 2, v).font = Font(name="Calibri", size=10)
        ws3.cell(i, 1).alignment = Alignment(vertical="top")
        ws3.cell(i, 2).alignment = Alignment(wrap_text=True, vertical="top")
        ws3.row_dimensions[i].height = 15 * (len(v) // 95 + 1)
    ws3.column_dimensions["A"].width = 20
    ws3.column_dimensions["B"].width = 100

    wb.properties.creator = world.PEOPLE["lead"]
    wb.properties.lastModifiedBy = world.PEOPLE["lead"]
    wb.properties.title = "Referral tables, 2027 Child-Resistant Packaging Review"
    wb.properties.created = dt.datetime(2026, 11, 4, 9, 18, 0)
    wb.save(path)
    office_container(path, "xlsx")


# ------------------------------------------------------------------------------------------------ the chart
def wrap(name, width=34):
    words, lines, cur = name.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return "\n".join(lines)


def chart(path):
    eff = sorted(F["effects"], key=lambda e: F["detail"][e["code"]]["effect"])     # largest at the top
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    fig, ax = plt.subplots(figsize=(9.2, 5.6), dpi=200)
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    ys = list(range(len(eff)))
    thr = F["threshold"]
    ax.axvline(1.0, color="#bdbcb6", lw=1.2, zorder=1)
    ax.axvline(thr, color=INK2, lw=1.1, ls=(0, (4, 3)), zorder=1)
    for y, e in zip(ys, eff):
        v = F["detail"][e["code"]]["effect"]
        col = ACCENT if e["reaches"] else MUTED
        ax.plot([1.0, v], [y, y], color=col, lw=2.0, solid_capstyle="round", zorder=2)
        ax.scatter([v], [y], s=64, color=col, edgecolor=SURF, linewidth=2.0, zorder=3)
        right = v >= 1.0
        ax.text(v + (0.012 if right else -0.012), y, e1(e["effect"]), va="center", ha="left" if right else "right",
                fontsize=9, color=INK, fontweight="bold" if e["reaches"] else "normal")
    ax.set_yticks(ys)
    ax.set_yticklabels([wrap(e["product"]) for e in eff], fontsize=8.4, color=INK)
    for lab, e in zip(ax.get_yticklabels(), eff):
        if e["reaches"]:
            lab.set_fontweight("bold")
    ax.set_xlim(0.86, 1.42)
    ax.set_ylim(-0.7, len(eff) - 0.3)
    ax.set_xticks([0.9, 1.0, 1.1, 1.2, 1.3, 1.4])
    ax.set_xticklabels(["0.9", "1.0", "1.1", "1.2", "1.3", "1.4"], color=INK2)
    ax.tick_params(axis="both", length=0)
    ax.grid(axis="x", color=GRID, lw=0.6, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.set_xlabel("Effect: exposures recorded / exposures expected with the previous packaging", color=INK2,
                  fontsize=8.6)
    ax.text(thr + 0.006, len(eff) - 0.42, "Referral line %.2f" % thr, color=INK2, fontsize=8.4, ha="left", va="bottom")
    ax.text(1.0 - 0.006, len(eff) - 0.42, "No change", color=INK2, fontsize=8.4, ha="right", va="bottom")
    fig.text(0.012, 0.965, "Only the Feverkind Junior Strength cap change reaches the 1.20 referral line",
             fontsize=12.5, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.012, 0.918, "Accidental exposures of children under six in the twelve months after each changed pack "
             "was first sold at retail,\nagainst the number expected had the pack not changed",
             fontsize=8.8, color=INK2, ha="left", va="top", linespacing=1.35)
    fig.text(0.012, 0.016, "Packaging changes first sold at retail 1 January 2024 to 30 September 2025. Sources: %s "
             "case export (2 November 2026);\n%s four-week point-of-sale data; watched-product register "
             "(30 October 2026)." % (world.NETWORK, world.PROVIDER), fontsize=7.4, color=INK2, ha="left", va="bottom",
             linespacing=1.35)
    fig.subplots_adjust(left=0.30, right=0.97, top=0.82, bottom=0.165)
    fig.savefig(path, dpi=200, facecolor=SURF, metadata={"Software": None})
    plt.close(fig)


# ------------------------------------------------------------------------------------------------ the referral
def _page_footer(section, text):
    p = section.footer.paragraphs[0]
    r = p.add_run(text + "   page ")
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor.from_string("7F7F7F")
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "16")
    rpr.append(sz)
    run.append(rpr)
    t = OxmlElement("w:t")
    t.text = "1"
    run.append(t)
    fld.append(run)
    p._p.append(fld)


def memo(path):
    eff = {e["code"]: e for e in F["effects"]}
    call, run = eff[F["call_code"]], eff[F["runner_up_code"]]
    others = [e for e in F["effects"] if e["code"] not in (F["call_code"], F["runner_up_code"])]
    meta = world.META
    short = call["product"].split(" Acetaminophen")[0]
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(27.94), Cm(21.59)
    sec.left_margin = sec.right_margin = Cm(2.3)
    sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(2.0)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    st.paragraph_format.space_after = Pt(6)
    st.paragraph_format.line_spacing = 1.1
    _page_footer(sec, "%s, Toxicovigilance. Referral to the 2027 Child-Resistant Packaging Review." % world.NETWORK)
    texts = []

    def para(text="", bold=False, size=None, color=None, after=None, italic=False):
        p = doc.add_paragraph()
        if text:
            texts.append(text)
            r = p.add_run(text)
            r.bold, r.italic = bold, italic
            if size:
                r.font.size = Pt(size)
            if color:
                r.font.color.rgb = RGBColor.from_string(color)
        if after is not None:
            p.paragraph_format.space_after = Pt(after)
        return p

    para(world.NETWORK.upper(), bold=True, size=9, color="1F4E79", after=0)
    para("Toxicovigilance", size=9, color="595959", after=14)
    para("Referral to the 2027 Child-Resistant Packaging Review", bold=True, size=14, after=8)
    rows = [("To", "%s, Review Secretary, %s" % (world.PEOPLE["secretary"], world.OFFICE)),
            ("From", "%s, Director of Toxicovigilance, %s" % (world.PEOPLE["lead"], world.NETWORK)),
            ("Date", MEMO_DATE),
            ("Reference", "Procedure CRP-3, issue 4; your call for referrals of 21 September 2026"),
            ("Product", "%s (%s)" % (call["product"], call["product_code"]))]
    t = doc.add_table(rows=len(rows), cols=2)
    for i, (k, v) in enumerate(rows):
        a, b = t.rows[i].cells
        a.width, b.width = Cm(2.6), Cm(14.0)
        a.paragraphs[0].add_run(k).bold = True
        b.paragraphs[0].add_run(v)
        texts.append(k + " " + v)
        for c in (a, b):
            c.paragraphs[0].paragraph_format.space_after = Pt(1)
    para(after=4)

    para("The network refers %s, made by %s. Its change from a %s to a %s, first sold at retail on %s, had an effect "
         "of %s under section 3 of the procedure. Our member centers recorded %s accidental exposures of children "
         "under six to the product from %s to %s, three tenths more than its packs would have produced in those "
         "months with the previous cap.*"
         % (call["product"], meta[call["code"]]["maker"], meta[call["code"]]["closure_old"].lower(),
            meta[call["code"]]["closure_new"].lower(), day_label(call["change"]), e1(call["effect"]),
            "{:,}".format(call["observed"]), month_label(call["window"][0]), month_label(call["window"][1])))
    para("It is the largest effect among the %s packaging changes the procedure covers and the only one to reach the "
         "%.2f that section 4 requires. The next largest is %s (%s), whose %s was first sold at retail on %s, at %s. "
         "The gap between the two effects is %s. The other %s changes each come to %s."
         % (WORDS[len(F["effects"])], F["threshold"], run["product"], run["product_code"],
            meta[run["code"]]["closure_new"].lower(), day_label(run["change"]), e1(run["effect"]), e1(F["gap"]),
            WORDS[len(others)], e1(others[0]["effect"])))

    para("How the expected counts were built", bold=True, size=11, after=3)
    para("A young child can only get into a pack that is already in the home, so a product's exposures follow the "
         "packs households still hold rather than the packs sold that month. A bottle of junior fever medicine bought "
         "for the next illness can stay in a cupboard for more than a year; a pack of lozenges or a bottle of eye "
         "drops is used up within weeks. For each product we rebuilt daily packs sold from %s's four-week "
         "point-of-sale data, carried them forward as packs in use running down at a constant monthly rate, and "
         "fitted that rate and the exposures per pack in use to the product's monthly accidental exposures from "
         "January 2019 to the month before its change. The expected count for the twelve months is that model run "
         "forward with the previous packaging's exposures per pack." % world.PROVIDER)
    para("We tested the model on each product's last year before its change, fitting it on the years before that "
         "year: it predicts those twelve months closely for all %s products, which a constant rate per pack sold "
         "does not do for any of them. The usual reading, exposures per pack sold before and after the change, misses "
         "this one. %s sold about a quarter more packs in the year after the new cap went on sale, but most of the "
         "packs in homes that year had been bought before it, so its exposures per pack sold rose by about a tenth "
         "while its exposures per pack in use rose by three tenths." % (WORDS[len(F["effects"])], short))

    para("Supporting tables", bold=True, size=11, after=3)
    para("referral_tables.xlsx lists every change with the months read, the exposures recorded and the effect, and "
         "the antidote courses our four children's hospitals started from January 2025 to June 2026. effects_chart.png "
         "shows the %s effects against the referral line. We can send the case-level extract behind these counts on "
         "request." % WORDS[len(F["effects"])])
    para(after=10)
    para(world.PEOPLE["lead"], bold=True, after=0)
    para("Director of Toxicovigilance, %s" % world.NETWORK, after=16)
    para("* Cases the member centers recorded as unintentional general in a patient under six at the time of the "
         "call, in the calendar month of the recorded call date (procedure sections 3.2 and 3.3). The month the "
         "changed pack was first sold is in neither the fitted record nor the twelve months.",
         size=8.5, color="595959", italic=True)

    cp = doc.core_properties
    cp.author = world.PEOPLE["lead"]
    cp.last_modified_by = world.PEOPLE["lead"]
    cp.title = "Referral to the 2027 Child-Resistant Packaging Review"
    cp.subject = ""
    cp.keywords = ""
    cp.comments = ""
    cp.category = ""
    cp.revision = 4
    cp.created = dt.datetime(2026, 11, 5, 16, 4, 0)
    cp.modified = SAVED
    doc.save(path)
    body = " ".join(texts)
    office_container(path, "docx", words=(len(body.split()), len(body.replace(" ", ""))))


def main():
    os.makedirs(GOLD, exist_ok=True)
    workbook(os.path.join(GOLD, "referral_tables.xlsx"))
    chart(os.path.join(GOLD, "effects_chart.png"))
    memo(os.path.join(GOLD, "packaging_referral.docx"))
    print("golden:", sorted(os.listdir(GOLD)))


if __name__ == "__main__":
    main()
