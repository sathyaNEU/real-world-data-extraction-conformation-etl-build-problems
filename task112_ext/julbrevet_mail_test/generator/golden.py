# Writes the three golden deliverables from figures.json. Usage: python3 -I golden.py <figures.json> <out dir>
import datetime as dt, json, os, re, sys, zipfile
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Pt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

F = json.load(open(sys.argv[1], encoding="utf-8"))
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
WHEN = dt.datetime(2028, 1, 16, 11, 50)
AUTHOR = "Brannvik Plus CRM"
FORMATS, WEEKS = ["Stor", "Mellan", "Nära"], [48, 49, 50, 51]
DATES = {48: "1 to 5 Dec", 49: "6 to 12 Dec", 50: "13 to 19 Dec", 51: "20 to 24 Dec"}
NOTE = ("BV27-13-O2 (50 kr rabatt vid köp över 700 kr) receipts of 1 to 24 December 2027 with a basket under 750 SEK "
        "before the 50 kr discount, amounts as the BI warehouse counts purchases. At BV101, BV104, BV106, BV110, BV113, "
        "BV114, BV115, BV118, BV119, BV128, BV129, BV132, BV138 and BV141 the POS receipt totals from late October 2027 "
        "run above the BI warehouse's spend by exactly the discount, so 50 SEK is taken off there before the test. "
        "Redemptions the POS export lists under BV27-13-O1 with 50 SEK off a basket over 700 SEK are BV27-13-O2 "
        "redemptions and are counted.")


def sheet(ws, title, head, rows, widths):
    ws["A1"] = title
    ws["A1"].font = Font(bold=True)
    ws["A2"] = NOTE
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(head))
    ws.row_dimensions[2].height = 104
    for j, h in enumerate(head, 1):
        c = ws.cell(4, j, h)
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
    ws.row_dimensions[4].height = 32
    for i, row in enumerate(rows, 5):
        for j, v in enumerate(row, 1):
            c = ws.cell(i, j, v)
            if isinstance(v, float):
                c.number_format = "#,##0.0"
            elif isinstance(v, int) and j > 1:
                c.number_format = "#,##0"
    for col, w in zip("ABCD", widths):
        ws.column_dimensions[col].width = w


wb = Workbook()
ws1 = wb.active
ws1.title = "By store format"
sheet(ws1, "O2 receipts with a basket under 750 SEK, by store format",
      ["Store format", "Receipts", "Purchases paid (thousand SEK)"],
      [[f, F[f"F|{f}|receipts"], F[f"F|{f}|paid"]] for f in FORMATS], [16, 12, 26])
ws2 = wb.create_sheet("By week")
sheet(ws2, "O2 receipts with a basket under 750 SEK, by ISO week",
      ["ISO week", "Dates", "Receipts", "Purchases paid (thousand SEK)"],
      [[w, DATES[w], F[f"W|{w}|receipts"], F[f"W|{w}|paid"]] for w in WEEKS], [12, 14, 12, 26])
wb.properties.creator = AUTHOR
wb.properties.lastModifiedBy = AUTHOR
wb.properties.created = WHEN
wb.properties.modified = WHEN
wb.save(os.path.join(OUT, "julbrevet_2028_plan.xlsx"))

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(11)
paras = [
    ("Julbrevet 2027 mailing: drop it from the 2028 plan", True),
    ("Drop the addressed Julbrevet mailing from the 2028 plan: it caused about 137 SEK of extra December purchases per "
     "piece (90 percent range minus 56.99 to 331.42), but the margin on the lower end, minus 14.25 SEK per piece, does "
     "not cover the 11.40 SEK piece cost.", False),
    ("The test rested on the 1,942 eligible households in the three postcode areas held back from printing (803, 805 and "
     "852). The control was assigned by area, so the range comes from the spread between the 27 areas.", False),
    (f"On the threshold offer, {F['M|receipts']:,} receipts that redeemed BV27-13-O2 had a basket under 750 SEK before "
     f"the 50 kr discount ({F['F|Stor|receipts']:,} at Stor, {F['F|Mellan|receipts']:,} at Mellan and "
     f"{F['F|Nära|receipts']:,} at Nära stores), and {F['M|paid']:,.1f} thousand SEK was paid on them.", False),
]
for text, bold in paras:
    run = doc.add_paragraph().add_run(text)
    run.bold = bold
cp = doc.core_properties
cp.author = AUTHOR
cp.last_modified_by = AUTHOR
cp.created = WHEN
cp.modified = WHEN
cp.revision = 3
cp.title = ""
cp.comments = ""
doc.save(os.path.join(OUT, "julbrevet_mail_call.docx"))

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=110)
cols = {"Stor": "#225a70", "Mellan": "#7aa0b2", "Nära": "#c8cdd1"}
bottom = [0] * len(WEEKS)
for f in FORMATS:
    vals = [F[f"C|{w}|{f}"] for w in WEEKS]
    ax.bar(range(len(WEEKS)), vals, 0.55, bottom=bottom, color=cols[f], label=f)
    for i, v in enumerate(vals):
        if v >= 3:
            ax.text(i, bottom[i] + v / 2, str(v), ha="center", va="center", fontsize=10,
                    color="white" if f == "Stor" else "black")
    bottom = [b + v for b, v in zip(bottom, vals)]
for i, w in enumerate(WEEKS):
    ax.text(i, bottom[i] + 0.6, str(F[f"W|{w}|receipts"]), ha="center", va="bottom", fontweight="bold")
ax.set_xticks(range(len(WEEKS)))
ax.set_xticklabels([f"Week {w}\n{DATES[w]}" for w in WEEKS])
ax.set_ylabel("Receipts")
ax.set_ylim(0, max(bottom) * 1.25)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(title="Store format", frameon=False, loc="upper left")
fig.suptitle("BV27-13-O2 receipts with a basket under 750 SEK before the discount", fontsize=13, fontweight="bold",
             x=0.02, ha="left")
ax.set_title("1 to 24 December 2027, amounts as the BI warehouse counts purchases", fontsize=10, loc="left",
             color="#444444")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "julbrevet_reach_2028.png"), metadata={"Software": None})


def settle(path):
    """Office writers stamp the save time into the package; set it to the memo's own date."""
    zin = zipfile.ZipFile(path)
    items = [(i, zin.read(i)) for i in zin.infolist()]
    zin.close()
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for i, data in items:
            if i.filename == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*", rb"\g<1>2028-01-16T11:50:00Z", data)
            if i.filename == "docProps/app.xml" and path.endswith(".xlsx"):
                data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Excel</Application>", data)
                data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
            info = zipfile.ZipInfo(i.filename, date_time=(2028, 1, 16, 11, 50, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data)


settle(os.path.join(OUT, "julbrevet_2028_plan.xlsx"))
settle(os.path.join(OUT, "julbrevet_mail_call.docx"))
print("written", sorted(os.listdir(OUT)))
