# Writes the three golden deliverables of the v2 build from figures.json.
# Usage: python3 -I golden.py <figures.json> <out dir>
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
COUNTIES = ["Gävleborg", "Västernorrland"]
GROUPS = [("email", "Email"), ("sms_push_only", "SMS or app push, not email"), ("none", "None of the three")]
OFFERS = [("O1", "BV27-13-O1", "Julskinka 25 % billigare"), ("O2", "BV27-13-O2", "50 kr rabatt vid köp över 700 kr")]
FORMATS = ["Stor", "Mellan", "Nära"]

def sek(x, d=2):
    return f"{x:,.{d}f}".replace("-", "minus ") if x < 0 else f"{x:,.{d}f}"

# ------------------------------------------------------------------ workbook
wb = Workbook()
ws = wb.active
ws.title = "Card offers"
ws["A1"] = "Julbrevet 2027 card offers: purchases paid on the receipts that redeemed each offer, 1 to 24 December"
ws["A1"].font = Font(bold=True)
ws["A2"] = ("Thousand SEK paid after the offer discount, on the BI warehouse's basis, by the format of the store where "
            "the receipt was rung. At BV113, BV115, BV118, BV125, BV128, BV132 and BV141 the POS receipt totals from late "
            "October 2027 run above the BI warehouse's spend by exactly the discount, so the discount is taken off there.")
ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells("A2:E2")
ws.row_dimensions[2].height = 48
hdr = ["Offer", "Offer text"] + FORMATS
for j, h in enumerate(hdr, 1):
    ws.cell(4, j, h).font = Font(bold=True)
for i, (k, code, text) in enumerate(OFFERS, 5):
    ws.cell(i, 1, code)
    ws.cell(i, 2, text)
    for j, f in enumerate(FORMATS, 3):
        c = ws.cell(i, j, F[f"A|{k}|{f}"])
        c.number_format = "#,##0.0"
ws.column_dimensions["A"].width = 13
ws.column_dimensions["B"].width = 34
for col in "CDE":
    ws.column_dimensions[col].width = 13

ws2 = wb.create_sheet("Reach 2028")
ws2["A1"] = "Households mailed the Julbrevet in 2027: channels that could still send them the 2028 Julbrevet"
ws2["A1"].font = Font(bold=True)
ws2["A2"] = ("14,108 households on the BV27-13-D1 address file, by the county of their postcode area. A household counts "
             "for a channel when an account open at the end of 2027 held consent for it at 00:00 on 1 January 2028 "
             "Swedish time and the platform would still send to it: email leaves out addresses on the email platform's "
             "suppression list (hard bounces in 2027, and members consented at 2027 newsletter releases who were never "
             "sent a 2027 email); app push needs a sign-in to the app and leaves out the tokens whose last three "
             "notifications failed, which the January clean-up removes. Purchases are thousand SEK paid on the receipts "
             "on which any card registered to the households redeemed BV27-13-O1 or O2, on the same basis as the offer sheet.")
ws2["A2"].alignment = Alignment(wrap_text=True, vertical="top")
ws2.merge_cells("A2:D2")
ws2.row_dimensions[2].height = 120
for j, h in enumerate(["County", "Could still be sent the 2028 Julbrevet by", "Households",
                       "Purchases on Julbrevet offer receipts (thousand SEK)"], 1):
    c = ws2.cell(4, j, h)
    c.font = Font(bold=True)
    c.alignment = Alignment(wrap_text=True, vertical="bottom")
r = 5
for county in COUNTIES:
    for g, label in GROUPS:
        ws2.cell(r, 1, county)
        ws2.cell(r, 2, label)
        ws2.cell(r, 3, F[f"B|{county}|{g}"]).number_format = "#,##0"
        ws2.cell(r, 4, F[f"C|{county}|{g}"]).number_format = "#,##0.0"
        r += 1
ws2.column_dimensions["A"].width = 16
ws2.column_dimensions["B"].width = 40
ws2.column_dimensions["C"].width = 12
ws2.column_dimensions["D"].width = 22
ws2.row_dimensions[4].height = 32
wb.properties.creator = AUTHOR
wb.properties.lastModifiedBy = AUTHOR
wb.properties.created = WHEN
wb.properties.modified = WHEN
wb.save(os.path.join(OUT, "julbrevet_2028_plan.xlsx"))

# ------------------------------------------------------------------ memo
none_hh = F["M|none|households"]
none_buy = F["M|none|paid"]
assert none_hh == sum(F[f"B|{c}|none"] for c in COUNTIES)
doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(11)
paras = [
    ("Julbrevet 2027 mailing: drop it from the 2028 plan", True),
    ("Drop the addressed Julbrevet mailing from the 2028 plan: it caused about 137 SEK of extra December purchases per "
     "piece (90 percent range minus 56.99 to 331.42), but the margin on the lower end, minus 14.25 SEK per piece, does "
     "not cover the 11.40 SEK piece cost.", False),
    ("Julbrevet is the December campaign of Brannvik Plus. The mailing went to 14,108 eligible households. The control "
     "is the 1,942 eligible households in the three postcode areas (803, 805 and 852) held back from printing.", False),
    ("Mailed households bought 2,298.58 SEK per household in December against 2,161.36 SEK in the held-back areas, so "
     "the lift is 137.21 SEK per piece. The control was assigned by area, so the 90 percent range comes from the spread "
     "between the 27 areas: minus 56.99 to 331.42 SEK per piece.", False),
    ("At the plan's 25 percent gross margin the lower end is worth minus 14.25 SEK per piece against the 11.40 SEK piece "
     "cost, so the mailing misses the line by 25.65 SEK per piece. For the mailing to pay, the test would have needed "
     "to show 239.81 SEK per piece (break-even 45.60 plus 2.0615 times the standard error 94.21). The test rested on "
     "1,942 control households.", False),
    ("Counting households as separate observations gives a narrower range, but the three held-back areas move "
     "together, so that range is tighter than the data allows.", False),
    (f"What dropping the letter leaves: {none_hh:,} of the 14,108 mailed households cannot be sent the 2028 Julbrevet "
     f"by email, SMS or app push ({F['B|Gävleborg|none']:,} in Gävleborg, {F['B|Västernorrland|none']:,} in "
     f"Västernorrland). Those households paid {none_buy:,.1f} thousand SEK on receipts that redeemed a Julbrevet card "
     "offer in December 2027. The workbook has the split by county and channel and the offer figures by store format.",
     False),
]
for text, bold in paras:
    p = doc.add_paragraph()
    run = p.add_run(text)
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

# ------------------------------------------------------------------ chart
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
fig, ax = plt.subplots(figsize=(11, 6), dpi=110)
cols = ["#225a70", "#7aa0b2", "#c8cdd1"]
w = 0.26
for k, (g, label) in enumerate(GROUPS):
    xs = [i + (k - 1) * w for i in range(len(COUNTIES))]
    vals = [F[f"B|{c}|{g}"] for c in COUNTIES]
    bars = ax.bar(xs, vals, w * 0.92, color=cols[k], label=label)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 40, f"{v:,}", ha="center", va="bottom", fontsize=10)
ax.set_xticks(range(len(COUNTIES)))
ax.set_xticklabels(COUNTIES)
ax.set_ylabel("Households mailed the Julbrevet in 2027")
ax.set_ylim(0, 4600)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(title="Could still be sent the 2028 Julbrevet by", frameon=False, loc="upper right")
fig.suptitle("Julbrevet 2028 without the letter: which channels could still reach the 2027 mailed households",
             fontsize=13, fontweight="bold", x=0.02, ha="left")
ax.set_title("Accounts open at the end of 2027, consent at that date, platform suppression and token clean-up applied",
             fontsize=10, loc="left", color="#444444")
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
