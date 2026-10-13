"""The golden deliverables, computed from the shipped files only: coordination_offices_2027.pptx (the secretariat's
deck for the members' council, with the chart of every country's figure) and member_funds_by_country.csv (one row per
country: the members' money spent in 2025, the commitments not yet paid at 30 June 2026, the organisations the
members paid directly in 2025); and figures.json, every figure the write-up states."""
import collections
import csv
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import calc as C        # noqa: E402
import reader as RD     # noqa: E402
import world as W       # noqa: E402

PPTX = "coordination_offices_2027.pptx"
CSV = "member_funds_by_country.csv"


def m1(v):
    return "%.1f" % v


def channels(L):
    """Each country's 2025 members' money by the route it came: directly, through the global fund (its own grants),
    through the Sahel fund."""
    rows = C.dedup(L["rows"])
    mrefs = C.member_refs(L["register"])
    ps = C.held_when_paid(rows, L["fx"], mrefs, "pro_rata")
    sh = C.activity_shares(rows, L["fx"], mrefs, pay_share=ps)
    acts = {}
    for r in rows:
        acts.setdefault(r["aid"], r)
    out = {c: collections.defaultdict(float) for c in W.NAMES}
    for r in rows:
        if r["ttype"] != "4" or r["tdate"].year != W.YEAR or r["rep"] in (C.GREF, C.SREF):
            continue
        s = sh.get(r["aid"], 0.0)
        if not s:
            continue
        f = r["funding"][0]
        route = "direct" if f in mrefs else ("global" if f == C.GREF else "sahel")
        v = C.usd(r, L["fx"]) * s
        for iso, pct in C.countries_of(r):
            out[W.NAME_OF[iso]][route] += v * pct / 100.0 / 1e6
    return out


def compute(target):
    L = RD.load(target)
    R = C.readings(L["rows"], L["fx"], L["register"])
    gold, gs, ss = R["golden"]
    top, margin = C.top3(gold)
    order = sorted(W.NAMES, key=lambda c: -gold[c])
    return dict(L=L, R=R, gold=gold, g_share=gs, s_share=ss, top=top, margin=margin, order=order,
                pipeline=C.ask_pipeline(L["rows"], L["fx"], L["register"]),
                orgs=C.ask_orgs(L["rows"], L["register"], L["registry"]), channels=channels(L))


def figures(X):
    F = collections.OrderedDict()
    F["call"] = list(X["top"])
    F["global_fund_member_share_pct"] = "%.1f" % (100 * X["g_share"])
    F["sahel_fund_member_share_pct"] = "%.1f" % (100 * X["s_share"])
    F["third_over_fourth"] = "%.2f" % X["margin"]
    F["fourth"] = X["order"][3]
    F["spent_2025_usd_m"] = collections.OrderedDict((c, m1(X["gold"][c])) for c in W.NAMES)
    F["committed_unpaid_2026_06_30_usd_m"] = collections.OrderedDict((c, m1(X["pipeline"][c])) for c in W.NAMES)
    F["organisations_paid_directly_2025"] = collections.OrderedDict((c, X["orgs"][c]) for c in W.NAMES)
    F["routes_usd_m"] = collections.OrderedDict(
        (c, collections.OrderedDict((k, m1(X["channels"][c][k])) for k in ("direct", "global", "sahel"))) for c in X["order"][:5])
    rd = collections.OrderedDict()
    for nm in ("same_year", "lifetime", "cum_before_pay", "prior_year", "golden_one", "none", "pay"):
        v, g, s = X["R"][nm]
        rd[nm] = dict(three=C.top3(v)[0], global_share_pct="%.1f" % (100 * g), sahel_share_pct="%.1f" % (100 * s))
    F["readings"] = rd
    F["members_total_spent_2025_usd_m"] = m1(sum(X["gold"].values()))
    return F


def chart_png(X):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = "DejaVu Sans"
    order = list(reversed(X["order"]))
    vals = [X["gold"][c] for c in order]
    col = ["#0f5257" if c in X["top"] else "#b7c4c6" for c in order]
    fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=150)
    ax.barh(order, vals, color=col, height=0.66)
    for i, (c, v) in enumerate(zip(order, vals)):
        ax.text(v + 0.18, i, m1(v), va="center", fontsize=8.6, color="#202326")
    ax.set_xlabel("Members' money spent in 2025 (USD millions)", fontsize=9)
    ax.tick_params(axis="both", labelsize=8.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xlim(0, max(vals) * 1.12)
    ax.set_title("Members' money spent in 2025, by country", fontsize=10.5, loc="left", color="#202326")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_csv(X, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\r\n")
        wr.writerow(["country", "members_money_spent_2025_usd_m", "committed_not_paid_2026_06_30_usd_m",
                     "organisations_paid_directly_2025"])
        for c in W.NAMES:
            wr.writerow([c, m1(X["gold"][c]), m1(X["pipeline"][c]), X["orgs"][c]])


def write_pptx(X, F, path):
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.util import Emu, Inches, Pt
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    TEAL, INK, GREY = RGBColor(0x0F, 0x52, 0x57), RGBColor(0x20, 0x23, 0x26), RGBColor(0x5F, 0x63, 0x68)
    SOURCE = ("Source: IATI Datastore extract of 5 October 2026 and the two funds' activity files; secretariat exchange "
              "table; member funds statistics, methodology note version 2.")
    n_slide = [0]

    def text(slide, x, y, w, h, paras, size=14, color=INK, bold=False):
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, p in enumerate(paras):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            run = para.add_run()
            run.text = p
            run.font.size = Pt(size)
            run.font.color.rgb = color
            run.font.bold = bold
            run.font.name = "Arial"
            para.space_after = Pt(6)
        return tb

    def slide(title):
        n_slide[0] += 1
        s = prs.slides.add_slide(blank)
        text(s, 0.6, 0.35, 12.1, 1.0, [title], size=26, color=TEAL, bold=True)
        text(s, 0.6, 6.85, 11.3, 0.4, [SOURCE], size=9, color=GREY)
        text(s, 12.3, 6.85, 0.6, 0.4, [str(n_slide[0])], size=9, color=GREY)
        return s

    def table(s, x, y, w, rows, widths, size=12):
        shp = s.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(0.4 * len(rows)))
        tbl = shp.table
        for j, wd in enumerate(widths):
            tbl.columns[j].width = Inches(wd)
        for i, r in enumerate(rows):
            for j, v in enumerate(r):
                cell = tbl.cell(i, j)
                cell.text = str(v)
                for p in cell.text_frame.paragraphs:
                    for run in p.runs:
                        run.font.size = Pt(size)
                        run.font.name = "Arial"
                        run.font.bold = (i == 0)
        return tbl

    t1, t2, t3 = X["top"]
    g = X["gold"]
    s = slide("Open the 2027 country coordination offices in %s, %s and %s" % (t1, t2, t3))
    text(s, 0.6, 1.5, 12.0, 4.8, [
        "Paper C/26/14, Members' Council, 9 December 2026.",
        "The council placed the offices where the most of the members' money was spent in 2025. %s (USD %s million), "
        "%s (USD %s million) and %s (USD %s million) lead; the next country, %s, had USD %s million."
        % (t1, m1(g[t1]), t2, m1(g[t2]), t3, m1(g[t3]), X["order"][3], m1(g[X["order"][3]])),
        "Money the members gave through the two pooled funds counts where the funds' grantees spent it, at the members' "
        "share of the money each fund held when it paid: %s per cent of the Pelorus Fund's 2025 grants and %s per cent "
        "of the Sahel Fund's." % (F["global_fund_member_share_pct"], F["sahel_fund_member_share_pct"]),
        "%s, %s, for the secretariat, October 2026." % W.PEOPLE["data"]], size=16)
    s = slide("%s, %s and %s lead the members' money spent in 2025" % (t1, t2, t3))
    s.shapes.add_picture(io.BytesIO(chart_png(X)), Inches(0.9), Inches(1.35), width=Inches(11.4))
    s = slide("Money through the pooled funds counts at the members' share of what each fund held when it paid")
    text(s, 0.6, 1.35, 12.1, 1.9, [
        "The Pelorus Fund collects its donors' contributions from October to December and pays the collection out as "
        "annual grants the following year: its 2025 grants were paid from its 2024 collection, of which the members gave "
        "%s per cent. Its 2025 collection, %s per cent from the members, arrived after its last 2025 grant and pays "
        "for 2026." % (F["global_fund_member_share_pct"], F["readings"]["same_year"]["global_share_pct"]),
        "The Sahel Fund's funders pay in each January and it pays the round out the same year: its 2025 grants carry the "
        "2025 round's mix, %s per cent once the Pelorus Fund's part is counted at %s per cent."
        % (F["sahel_fund_member_share_pct"], F["global_fund_member_share_pct"])], size=14)
    rows = [["Country", "Members directly", "Through the Pelorus Fund", "Through the Sahel Fund", "Total"]]
    for c in X["order"][:5]:
        ch = X["channels"][c]
        rows.append([c, m1(ch["direct"]), m1(ch["global"]), m1(ch["sahel"]), m1(g[c])])
    table(s, 0.9, 3.55, 11.0, rows, [2.6, 2.1, 2.3, 2.1, 1.9])
    text(s, 0.9, 6.1, 11.0, 0.5, ["USD millions, 2025; the five countries with the most members' money."], size=11, color=GREY)
    s = slide("What the offices would work with")
    rows = [["Country", "Committed, not yet paid at 30 June 2026 (USD millions)", "Organisations the members paid directly in 2025"]]
    for c in X["top"]:
        rows.append([c, m1(X["pipeline"][c]), X["orgs"][c]])
    table(s, 0.9, 1.5, 11.0, rows, [2.6, 4.4, 4.0])
    text(s, 0.9, 3.4, 11.0, 2.6, [
        "Every country's figures are in member_funds_by_country.csv.",
        "Next: the secretariat negotiates host-country agreements and office leases for signature in the first quarter "
        "of 2027, within the running costs estimated for each capital."], size=14)
    prs.save(path)


def main(target, golden, figures_path):
    os.makedirs(golden, exist_ok=True)
    X = compute(target)
    F = figures(X)
    write_csv(X, os.path.join(golden, CSV))
    write_pptx(X, F, os.path.join(golden, PPTX))
    import postprocess as PP
    by = W.PEOPLE["data"][0]
    PP.normalize_ooxml(os.path.join(golden, PPTX), by, by, "2026-10-12T09:12:00Z", "2026-10-13T16:48:31Z",
                       title="Country coordination offices 2027", company=W.SECRETARIAT)
    with open(figures_path, "w") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return X
