"""The pack's documents: the Environmental Protection Office's note on ammonia factors for cattle, the Ammonia
Reduction Programme's designation rules, and the statistics office's June census tables for cattle."""
import reportlab.rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import registry as R
import world as W

reportlab.rl_config.invariant = 1
STY = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=STY["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.8, spaceAfter=6)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10)
H = ParagraphStyle("h", parent=STY["Heading2"], fontName="Helvetica-Bold", fontSize=11, spaceBefore=8, spaceAfter=4)
T = ParagraphStyle("t", parent=STY["Title"], fontName="Helvetica-Bold", fontSize=14, spaceAfter=10, alignment=0)
CAP = ParagraphStyle("c", parent=BODY, fontName="Helvetica-Oblique", fontSize=8, leading=10, spaceBefore=2)
EPO = "Environmental Protection Office"
DEPT = "Ministry of Agriculture"
NSO = "National Statistics Office"
STAMPS = {"epo": b"D:20250818103000+01'00'", "arp": b"D:20250930151500+01'00'", "census": b"D:20260917110000+01'00'"}
CATNAME = {"dairy_cow": "Dairy cows", "suckler_cow": "Suckler cows", "over24": "Cattle over 24 months",
           "m12_24": "Cattle 12 to 24 months", "calf": "Calves"}
ORDER = ["calf", "m12_24", "over24", "dairy_cow", "suckler_cow"]


def _pdf(path, title, story, author, org):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=org, subject=title, producer=org)

    def footer(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.drawString(20 * mm, 11 * mm, org + "  |  " + title)
        c.drawRightString(A4[0] - 20 * mm, 11 * mm, "%d" % d.page)
        c.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def P(text, style=BODY):
    return Paragraph(text, style)


def _table(rows, widths=None, size=8.5):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", size), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", size),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black), ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                           ("ALIGN", (1, 1), (-1, -1), "RIGHT"), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                           ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    return t


def _h(text):
    return Paragraph(text, ParagraphStyle("th", parent=SMALL, fontName="Helvetica-Bold", alignment=2))


def epo_pdf(path):
    t1 = [["Category", _h("Housed"), _h("At grass")]] + \
        [[CATNAME[c], "%.4f" % W.NEX[c][0], "%.4f" % W.NEX[c][1]] for c in ORDER]
    t2 = [["Stage", _h("Share")],
          ["Housed manure: TAN as a share of nitrogen excreted", "%.2f" % W.TAN_HOUSED],
          ["Housing: NH3-N lost as a share of TAN excreted", "%.2f" % W.EF_HOUSING],
          ["Storage: NH3-N lost as a share of TAN entering the store", "%.2f" % W.EF_STORAGE],
          ["Spreading: NH3-N lost as a share of TAN spread (2024 mix of methods)", "%.2f" % W.EF_SPREADING],
          ["At grass: TAN as a share of nitrogen excreted", "%.2f" % W.TAN_GRASS],
          ["Grazing: NH3-N lost as a share of TAN deposited", "%.2f" % W.EF_GRAZING]]
    t3 = [["Category", _h("Housed"), _h("At grass")]] + \
        [[CATNAME[c], "%.4f" % W.RATE[c][0], "%.4f" % W.RATE[c][1]] for c in ORDER]
    t4 = [["Region", _h("Housing date"), _h("Turnout date"), _h("Housed days"), _h("Grass days")]]
    for r in W.REG:
        (im, idd), (om, od) = W.HOUSING[r]
        h = W.housed_days(r)
        t4.append([r, W.dd(W.di(W.D(2025, im, idd))).strftime("%-d %b"), W.D(2026, om, od).strftime("%-d %b"), str(h),
                   str(W.NDAY - h)])
    t5 = [["Region"] + [_h(CATNAME[c]) for c in ORDER]]
    for r in W.REG:
        t5.append([r] + ["%.1f" % W.annual_factor(r, c) for c in ORDER])
    s = [P("Ammonia emission factors for cattle", T),
         P("Tier 2 factors for the national ammonia inventory, 2025 edition. %s, Air Emissions Inventory Unit. "
           "Issued 18 August 2025; replaces the 2019 edition." % EPO, SMALL),
         P("1. Scope", H),
         P("This note gives the factors the national inventory applies to ammonia from cattle manure from the 2025 "
           "submission, and that regional and farm estimates made on the inventory's method should use. They cover "
           "the four stages at which ammonia is lost from cattle manure: in the house, in the store, when the stored "
           "manure is spread, and from the dung and urine cattle deposit at grazing. Fertiliser and other livestock "
           "are covered by separate notes."),
         P("2. Categories", H),
         P("Calves are cattle under 12 months of age. Cattle 12 to 24 months and cattle over 24 months exclude cows. "
           "A cow is a female from the day of her first calving: a dairy cow if her breed is one of the dairy breeds "
           "in the annex, a suckler cow otherwise. An animal passes from one category to the next on the day it reaches "
           "12 or 24 months or first calves; a bull, a steer and a heifer that has not calved are cattle of their age."),
         P("3. The mass flow", H),
         P("Table 1 gives the nitrogen a head of each category excretes in a day while housed and while at grass. Of "
           "the nitrogen excreted in the house a share is total ammoniacal nitrogen (TAN), of which a share is lost as "
           "ammonia-nitrogen (NH3-N) in the house, a share of what reaches the store is lost in storage and a share of "
           "what is spread is lost at spreading (Table 2). Of the TAN deposited at grass a share is lost at grazing. "
           "NH3-N is converted to ammonia (NH3) at 17/14."),
         _table(t1, [80 * mm, 30 * mm, 30 * mm]),
         P("Table 1. Nitrogen excreted, kg N a head a day.", CAP),
         Spacer(1, 4),
         _table(t2, [125 * mm, 25 * mm]),
         P("Table 2. Ammoniacal shares and loss fractions.", CAP),
         P("4. The factors", H),
         _table(t3, [80 * mm, 30 * mm, 30 * mm]),
         P("Table 3. Ammonia from cattle manure, kg NH3 a head a day. The housed rate covers the house, the store and "
           "the spreading of the manure produced while the animal is housed, and applies on the days inside the housing "
           "season of the region where the animal is kept (Table 4); the grass rate applies on its other days. The "
           "rates are rounded to four decimals and are applied as printed.", CAP),
         Spacer(1, 4),
         _table(t4, [40 * mm, 27 * mm, 27 * mm, 25 * mm, 25 * mm]),
         P("Table 4. Housing seasons by region (2024 regions), from the %s's Livestock Housing Survey 2025. Housed days "
           "run from the housing date to the day before the turnout date; the days are those of a 365-day year." % DEPT,
           CAP),
         Spacer(1, 4),
         _table(t5, [30 * mm] + [28 * mm] * 5, size=8),
         P("Table 5. Ammonia a head a year, kg NH3, for an animal kept in one region for the whole year: the Table 3 "
           "rates over the region's housed and grass days in Table 4, rounded to one decimal.", CAP),
         P("5. Changes from the 2019 edition", H),
         P("Housing seasons are now given by region from the Livestock Housing Survey in place of a single national "
           "season of 150 days. The spreading fraction reflects the 2024 mix of spreading methods, a larger share of "
           "slurry now going on by trailing shoe and trailing hose. Nitrogen excretion of dairy cows at grass is revised "
           "up on the 2023 to 2024 grass analyses."),
         P("Annex. Dairy breeds", H),
         P("Register breed codes HO (Holstein), FR (Friesian), JE (Jersey), NR (Norwegian Red) and MO (Montbeliarde). "
           "Every other breed code, and every cross (a code ending in X), is a beef breed.")]
    _pdf(path, "Ammonia emission factors for cattle, 2025 edition", s, "Air Emissions Inventory Unit", EPO)


def arp_pdf(path):
    s = [P("Ammonia Reduction Programme 2025 to 2030", T),
         P("Designation of Ammonia Action Regions: rules, 2025 edition. %s, Ammonia Programme Unit. Made by the "
           "Minister on 30 September 2025." % DEPT, SMALL),
         P("1. Purpose", H),
         P("The Programme reduces ammonia from agriculture towards the national ceiling for 2030. Each autumn the "
           "Minister designates as Ammonia Action Regions the regions whose ammonia from cattle manure is highest for "
           "their farmed land, and the measures in section 6 apply in a designated region for the spreading season "
           "that follows."),
         P("2. The programme year", H),
         P("The programme year runs from 1 November to 31 October. Designations the Minister makes by 1 December 2026 "
           "rest on the programme year 1 November 2025 to 31 October 2026 and apply from 13 January 2027, when the "
           "closed period for spreading ends."),
         P("3. The measure", H),
         P("A region's measure is the ammonia from cattle manure arising in the region over the programme year, in "
           "kilograms of ammonia (NH3), computed with the %s's factors for cattle (Ammonia emission factors for "
           "cattle, 2025 edition): the housing, storage and spreading of the manure of housed cattle and the dung and "
           "urine of cattle at grass, for cattle of all ages. Ammonia from fertiliser and from other livestock is "
           "outside the measure." % EPO),
         P("4. Regions and farmed land", H),
         P("The regions are the twelve regions of the Ministry's 2024 regional structure, and a herd is in the "
           "region of its district in the herd register. A region's farmed land is the area declared in the Land "
           "Parcel Register for 2026 by the herds in the region, a commonage parcel counted at each herd's share of it."),
         P("5. The line", H),
         P("A region whose measure is 26 kilograms of ammonia a hectare of farmed land or more is designated. The Unit "
           "reports each region's measure in tonnes to one decimal and in kilograms a hectare to two decimals; the "
           "designation is decided on the unrounded figures."),
         P("6. Measures in an Ammonia Action Region", H),
         P("From the start of the spreading season, every farm in a designated region stocked above 100 kilograms of "
           "organic nitrogen a hectare must spread cattle slurry by low-emission equipment, that is a trailing shoe, a "
           "trailing hose (including a dribble bar and an umbilical dribble bar system) or shallow injection, and may "
           "not use a splash plate; and must cover any slurry store built after 1 January 2025. The measures stay in "
           "force for a region in each spreading season for which it is designated."),
         P("7. Timetable", H),
         P("The Ammonia Programme Unit puts each region's measure and farmed land to the Minister by 20 November. The "
           "Minister designates by 1 December and the designations are published with the Unit's figures.")]
    _pdf(path, "Ammonia Action Regions: designation rules, 2025 edition", s, "Ammonia Programme Unit", DEPT)


def census_pdf(path, w, cen):
    code = {h["farm_no"]: h["region_pre2024"] for h in w.herds if h.get("farm_no") and "out_farm_of" not in h}
    tot = {r: {k: 0 for k in R.NSO_CATS} for r in W.REG}
    farms = {r: 0 for r in W.REG}
    for f, c in cen.items():
        r = code[f]
        farms[r] += 1
        for k in R.NSO_CATS:
            tot[r][k] += c.get(k, 0)
    heads = ["Dairy cows", "Other cows", "Bulls", "Male 2 yrs+", "Female 2 yrs+", "Male 1-2 yrs", "Female 1-2 yrs",
             "Male calves", "Female calves", "Total"]
    t1 = [["Region"] + [_h(x) for x in heads]]
    state = {k: 0 for k in R.NSO_CATS}
    for r in W.REG:
        vals = [tot[r][k] for k in R.NSO_CATS]
        for k in R.NSO_CATS:
            state[k] += tot[r][k]
        t1.append(["%d %s" % (int(W.RCODE[r]), r)] + ["{:,}".format(v) for v in vals] + ["{:,}".format(sum(vals))])
    t1.append(["State"] + ["{:,}".format(state[k]) for k in R.NSO_CATS] + ["{:,}".format(sum(state.values()))])
    t2 = [["Region", _h("Farms with cattle"), _h("Cattle a farm")]]
    for r in W.REG:
        n = sum(tot[r].values())
        t2.append(["%d %s" % (int(W.RCODE[r]), r), "{:,}".format(farms[r]), "%.1f" % (n / farms[r])])
    tb = _table(t1, [27 * mm] + [14.5 * mm] * 10, size=7)
    tb.setStyle(TableStyle([("LINEABOVE", (0, len(t1) - 1), (-1, len(t1) - 1), 0.5, colors.black),
                            ("FONT", (0, len(t1) - 1), (-1, len(t1) - 1), "Helvetica-Bold", 7)]))
    s = [P("June Agricultural Census 2026: cattle", T),
         P("Final results. %s, Agriculture Statistics. Published 17 September 2026." % NSO, SMALL),
         P("The census counts the cattle on every farm in the State at midnight on 31 May 2026 (the census of 1 June). "
           "Farmers return the census on one form for all the land they farm, so a farmer with more than one holding or "
           "herd number returns their cattle once, under their farm number. The farm-level file "
           "nso_june_livestock_census_2026.csv carries the returns behind these tables."),
         Spacer(1, 2),
         tb,
         P("Table 1. Cattle on farms on 1 June 2026 by census region and category. Cows are females that have calved; "
           "dairy cows are those kept for milk production. Bulls are males of 2 years and over kept for breeding.", CAP),
         Spacer(1, 6),
         _table(t2, [40 * mm, 30 * mm, 30 * mm]),
         P("Table 2. Farms with cattle on 1 June 2026 by census region.", CAP),
         P("Notes", H),
         P("Census regions and their codes are those in use since the 2016 frame revision. The %s's 2024 regional "
           "structure, which moved three districts from Coastal Vale to Southern Vale, will be adopted from the 2027 "
           "census." % DEPT),
         P("Response: 96.8 per cent of farms in the frame returned the census; the counts for the remaining farms are "
           "taken from the National Bovine Register's record of the cattle on their herds at the reference date.")]
    _pdf(path, "June Agricultural Census 2026: cattle", s, "Agriculture Statistics", NSO)
