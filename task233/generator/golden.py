"""The golden deliverables and figures.json, computed from target/ through analysis.py."""
import datetime as dt
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import analysis
from io_util import esc, repack_xlsx, write_pdf

SHORT = {"Compliant": "Compliant", "Corrective action": "Corrective action", "Service credit": "Service credit"}


def money(x):
    return "{:,}".format(int(round(x)))


def figures(res):
    p = res["pack"]
    outs = res["outcomes"]
    names = p.region_name
    found = len(p.counted())
    dis = {r: 100.0 - a for r, a in p.agreement().items()}
    corr = [names[r] for r in p.regions if outs[r] == "Corrective action"]
    cred = [names[r] for r in p.regions if outs[r] == "Service credit"]
    comp = [names[r] for r in p.regions if outs[r] == "Compliant"]
    gold = res["golden"]
    fig = {
        "call": {"corrective_action": corr, "service_credit": cred, "compliant": comp,
                 "compliant_count": len(comp), "credit_dollars": money(res["credit"]),
                 "credit_regions_fee": {names[r]: money(p.fees[r]) for r in p.regions if outs[r] == "Service credit"},
                 "credit_percent": int(round(p.credit_rate * 100))},
        "components": {
            "prices_rechecked_found": "{:,}".format(found),
            "disagreement_low": "%.1f" % min(dis.values()), "disagreement_high": "%.1f" % max(dis.values()),
            "disagreement_low_region": names[min(dis, key=dis.get)], "disagreement_high_region": names[max(dis, key=dis.get)],
            "credit_region_accuracy_whole": {names[r]: int(round(gold[r])) for r in p.regions if outs[r] == "Service credit"},
            "corrective_accuracy_whole": sorted({int(round(gold[r])) for r in p.regions if outs[r] == "Corrective action"}),
            "days_per_month": "30.4",
            "band_compliant": "%.1f" % p.band_compliant, "band_credit": "%.1f" % p.band_credit,
            "default_credit_dollars": money(p.credit(p.outcomes(p.agreement()))),
        },
        "deliverables": {},
    }
    for r in p.regions:
        fig["deliverables"][r] = {"region": names[r], "outcome": outs[r], "timeliness": "%.1f" % res["timeliness"][r],
                                  "missed_visits": res["missed"][r], "replacement_acceptance": "%.1f" % res["acceptance"][r]}
    return fig


def workbook(res, path):
    p = res["pack"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Assessment"
    ws.append(["Price Collection Quality Standard: quarterly assessment, July to September 2026"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Tallis Field Research Ltd, Price Collection Services Agreement. Issued 16 October 2026 by the Prices Division, National Statistics Office."])
    ws.append([])
    hdr = ["Region", "Region name", "Outcome", "Timeliness (%)", "Missed visits", "Replacement acceptance (%)"]
    ws.append(hdr)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    fill = {"Corrective action": PatternFill("solid", fgColor="FCE9C8"), "Service credit": PatternFill("solid", fgColor="F6CFCB")}
    for r in p.regions:
        o = res["outcomes"][r]
        ws.append([r, p.region_name[r], o, round(res["timeliness"][r], 1), res["missed"][r], round(res["acceptance"][r], 1)])
        row = ws.max_row
        ws.cell(row, 4).number_format = "0.0"
        ws.cell(row, 6).number_format = "0.0"
        if o in fill:
            ws.cell(row, 3).fill = fill[o]
    ws.append([])
    cred = [r for r in p.regions if res["outcomes"][r] == "Service credit"]
    ws.append(["Service credit for the quarter ($)", None, int(round(res["credit"]))])
    ws.cell(ws.max_row, 1).font = Font(bold=True)
    ws.cell(ws.max_row, 3).number_format = "#,##0"
    ws.append(["Basis: %d per cent of the quarterly collection fee in Schedule 4 for %s ($%s)." %
               (round(p.credit_rate * 100), ", ".join(p.region_name[r] for r in cred), ", $".join(money(p.fees[r]) for r in cred))])
    for col, w in zip("ABCDEF", (9, 20, 19, 14, 13, 18)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"
    wb.save(path)
    repack_xlsx(path, "Prices Division", "2026-10-15T20:10:00Z", "2026-10-16T01:35:00Z",
                "PCQS assessment Q3 2026", "National Statistics Office")


def chart(res, png):
    p = res["pack"]
    gold = res["golden"]
    names = [p.region_name[r] for r in p.regions]
    vals = [gold[r] for r in p.regions]
    col = {"Compliant": "#4c7a9a", "Corrective action": "#d9a441", "Service credit": "#b5523b"}
    cols = [col[res["outcomes"][r]] for r in p.regions]
    fig, ax = plt.subplots(figsize=(7.4, 3.9), dpi=150)
    y = list(range(len(names)))[::-1]
    ax.barh(y, [v - 93.0 for v in vals], left=93.0, color=cols, height=0.62)
    ax.axvline(p.band_compliant, color="#333333", lw=1.0, ls="--")
    ax.axvline(p.band_credit, color="#333333", lw=1.0, ls=":")
    ax.text(p.band_compliant + 0.06, len(names) - 0.35, "Compliant from %.1f" % p.band_compliant, fontsize=7.5,
            va="bottom")
    ax.text(p.band_credit - 0.06, len(names) - 0.35, "Service credit below %.1f" % p.band_credit, fontsize=7.5,
            va="bottom", ha="right")
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlim(93.0, 100.0)
    ax.set_xlabel("Estimated collection accuracy, July to September 2026 (per cent)", fontsize=8)
    ax.tick_params(axis="x", labelsize=8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=col[k], label=k) for k in col], fontsize=7.5, loc="upper center",
              bbox_to_anchor=(0.45, -0.17), ncol=3, frameon=False)
    cred = [p.region_name[r] for r in p.regions if res["outcomes"][r] == "Service credit"]
    ncorr = sum(1 for r in p.regions if res["outcomes"][r] == "Corrective action")
    ax.set_title("%s falls below %.1f per cent; %s regions sit between the bands"
                 % (" and ".join(cred), p.band_credit, {4: "four", 3: "three", 5: "five"}.get(ncorr, str(ncorr))),
                 fontsize=9, loc="left")
    fig.tight_layout()
    fig.savefig(png, metadata={"Software": None})
    plt.close(fig)


def letter(res, path, png):
    p = res["pack"]
    outs = res["outcomes"]
    nm = p.region_name
    corr = [nm[r] for r in p.regions if outs[r] == "Corrective action"]
    cred = [r for r in p.regions if outs[r] == "Service credit"]
    comp = [nm[r] for r in p.regions if outs[r] == "Compliant"]

    def andlist(xs):
        return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]
    blocks = [
        ("s", "National Statistics Office, Prices Division"),
        ("s", "16 October 2026"),
        ("p", "Lucia Morrison<br/>Contract Manager, Tallis Field Research Ltd"),
        ("t", "Price collection assessment, July to September 2026"),
        ("p", "Dear Lucia,"),
        ("p", "This is the quarterly assessment under the Price Collection Quality Standard (version 3.0) for the "
              "collection your teams carried out from July to September 2026."),
        ("p", "<b>Outcomes.</b> %s %s placed under corrective action, with accompanied collection in every month of "
              "the October to December quarter. %s %s below %.1f per cent and so carries a service credit as well as "
              "accompanied collection. The other %s regions are compliant: %s." %
         (andlist(corr), "are" if len(corr) > 1 else "is", andlist([nm[r] for r in cred]), "falls" if len(cred) == 1 else "fall",
          p.band_credit,
          {9: "nine"}.get(len(comp), str(len(comp))), andlist(comp))),
        ("p", "<b>Service credit.</b> The credit for the quarter is $%s, %d per cent of the quarterly collection fee in "
              "Schedule 4 for %s ($%s). It will be deducted from the invoice for the October to December quarter." %
         (money(res["credit"]), round(p.credit_rate * 100), andlist([nm[r] for r in cred]), ", $".join(money(p.fees[r]) for r in cred))),
        ("p", "<b>How accuracy was estimated.</b> The Field Quality Team's officers re-collected prices from one to "
              "several days after your collectors' visits, so a re-collected price can differ because the outlet "
              "changed the price in between. Each re-collection was allowed the chance that its item's price had "
              "moved since the visit, from the item's monthly frequency of price change in the price database and the "
              "days between the visit and the re-collection, before the share of correctly recorded prices was set "
              "against the bands."),
        ("image", (png, 170, 89.6)),
        ("p", "Timeliness, missed visits and replacement acceptance for each region are in the attached workbook, "
              "pcqs_2026q3_assessment.xlsx. Please confirm the accompanied collection arrangements for the five regions "
              "by 30 October."),
        ("p", "Yours sincerely,"),
        ("p", "Joanne MacDonald<br/>Head of Prices, National Statistics Office"),
    ]
    write_pdf(path, "Price collection assessment Q3 2026", "Prices Division", "National Statistics Office", blocks,
              "Prices Division, National Statistics Office", "D:20261016093000+13'00'", "D:20261016093000+13'00'")


def build(target, outdir, gendir):
    res = analysis.run(target)
    os.makedirs(outdir, exist_ok=True)
    fig = figures(res)
    with open(os.path.join(gendir, "figures.json"), "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
    workbook(res, os.path.join(outdir, "pcqs_2026q3_assessment.xlsx"))
    png = os.path.join(gendir, "_chart.png")
    chart(res, png)
    letter(res, os.path.join(outdir, "pcqs_2026q3_contractor_letter.pdf"), png)
    os.remove(png)
    return res, fig


if __name__ == "__main__":
    import sys
    t = sys.argv[1]
    build(t, sys.argv[2], os.path.dirname(os.path.abspath(__file__)))
    print("golden written")
