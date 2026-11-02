"""The golden answer, computed from target/ alone, and the two deliverables written from it.

The construction: every 2026 refund's parcel is dated by replaying the centre's two logs through the hall the way the
2025 labelled returns show it is worked (each parcel opened is the newest one still waiting at that moment), from the
hall's content on 1 January 2026 as the 2025 records leave it; a refund made on day 15 or later counted from that
delivery day (day 0) is late. Asks: every goodwill voucher issued in the month valued in pounds (the Irish site's
vouchers are in euros, converted at the order system's reporting rate), and the 2026 refund-delay vouchers counted and
valued by the category of the order their case names."""
import datetime as dt
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bundle as B   # noqa: E402
import world as W    # noqa: E402

CATS = ["Womenswear", "Menswear", "Footwear", "Home", "Kids", "Accessories"]
MONTHS = ["%d-%02d" % ym for ym in W.WINDOW_MONTHS]
MONTH_NAMES = {m: dt.date(int(m[:4]), int(m[5:]), 1).strftime("%B %Y") for m in MONTHS}


def call_figures(m):
    """{month: (made, late)} -> the return's rows, the payment and the breach months."""
    rows, total_late, breach = {}, 0, []
    for k in MONTHS:
        made, late = m[k]
        share = round(100.0 * late / made, 1)
        met = (made - late) >= W.COMMIT_SHARE * made
        rows[k] = {"refunds_made": made, "refunds_late": late, "late_share_pct": share, "met": "yes" if met else "no"}
        total_late += late
        if not met:
            breach.append(k)
    return rows, total_late * W.PAYMENT_PER_LATE, breach, total_late


def eur_rate(target):
    o = B.orders(target)
    e = o[o.currency == "EUR"]
    r = np.round(e.order_total_gbp / e.order_total, 4)
    return float(r.mode().iloc[0])


def customer_currency(target):
    o = B.orders(target)
    assert (o.groupby("customer_ref").currency.nunique() == 1).all()
    return o.drop_duplicates("customer_ref").set_index("customer_ref").currency.to_dict()


def voucher_values(target, currency_from="customer", rate=None):
    """Value of every voucher issued in each month, in pounds. currency_from 'customer' reads each voucher's currency
    from its customer's orders; 'house' takes every value as pounds (the rung)."""
    v = B.vouchers(target)
    rate = rate if rate is not None else eur_rate(target)
    cc = customer_currency(target)
    mult = v.customer_ref.map(lambda c: rate if (currency_from == "customer" and cc.get(c) == "EUR") else 1.0)
    v = v.assign(gbp=v.value * mult, month=v.issued.dt.strftime("%Y-%m"))
    return {k: int(round(float(v[v.month == k].gbp.sum()))) for k in MONTHS}


def voucher_categories(target, link="case", currency_from="customer", drop_orphans=True):
    """2026 refund-delay vouchers issued January to June, counted and valued (pounds) by the category of the order
    they compensate. link 'case' reads the order through the case the voucher was issued on; 'voucher' reads the
    voucher's own order field (the rung)."""
    v = B.vouchers(target)
    v = v[(v.reason == "Refund delay") & (v.issued >= pd.Timestamp(2026, 1, 1)) & (v.issued < pd.Timestamp(2026, 7, 1))]
    o = B.orders(target).set_index("order_ref")
    if link == "case":
        c = B.cases(target).set_index("case_ref")
        order = v.case_ref.map(c.order_ref)
    else:
        order = v.order_ref
    cat = order.map(o.main_category)
    rate = eur_rate(target)
    cc = customer_currency(target)
    gbp = v.value * v.customer_ref.map(lambda c: rate if (currency_from == "customer" and cc.get(c) == "EUR") else 1.0)
    d = pd.DataFrame({"cat": cat, "gbp": gbp})
    if drop_orphans:
        d = d[d.cat.notna()]
    return {k: {"count": int((d.cat == k).sum()), "value_gbp": int(round(float(d[d.cat == k].gbp.sum())))} for k in CATS}


def compute(target):
    pair = B.replay(target, "newest")
    m = B.refund_table(target, pair)
    mon = B.monthly(m)
    rows, payment, breach, total_late = call_figures(mon)
    vv = voucher_values(target)
    for k in MONTHS:
        rows[k]["vouchers_gbp"] = vv[k]
    fig = {"months": rows, "payment_gbp": payment, "breach_months": breach, "late_total": total_late,
           "refunds_total": int(sum(rows[k]["refunds_made"] for k in MONTHS)),
           "vouchers_total_gbp": int(sum(vv[k] for k in MONTHS)),
           "categories": voucher_categories(target), "eur_rate": eur_rate(target),
           "payment_per_late_gbp": W.PAYMENT_PER_LATE, "commitment_pct": 95, "breach_line_pct": 5}
    return fig, m


# ------------------------------------------------------------------------------------------------- the deliverables
def write_return(fig, path):
    import csv
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["month", "refunds_made", "refunds_made_late", "late_share_pct", "met_95pct_commitment",
                    "goodwill_vouchers_issued_gbp"])
        for k in MONTHS:
            r = fig["months"][k]
            w.writerow([k, r["refunds_made"], r["refunds_late"], "%.1f" % r["late_share_pct"], r["met"], r["vouchers_gbp"]])
        tot = fig["refunds_total"]
        w.writerow(["2026-01 to 2026-06", tot, fig["late_total"], "%.1f" % (100.0 * fig["late_total"] / tot), "",
                    fig["vouchers_total_gbp"]])


def chart(fig, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 8.6, "svg.hashsalt": "467"})
    f, ax = plt.subplots(figsize=(6.3, 2.85), dpi=200)
    xs = np.arange(len(MONTHS))
    vals = [fig["months"][k]["late_share_pct"] for k in MONTHS]
    missed = [fig["months"][k]["met"] == "no" for k in MONTHS]
    cols = ["#9c2f3f" if m else "#8a96a3" for m in missed]
    ax.bar(xs, vals, width=0.58, color=cols, zorder=2)
    ax.axhline(5.0, color="#3a3a3a", lw=1.0, ls=(0, (4, 3)), zorder=3)
    ax.text(-0.42, 5.7, "Commitment: 5.0% late at most", ha="left", va="bottom", fontsize=7.6, color="#3a3a3a")
    top = max(vals)
    for x, v, m in zip(xs, vals, missed):
        ax.text(x, v + top * 0.02, "%.1f%%" % v, ha="center", va="bottom", fontsize=7.8, color="#1c1c1c")
        if m:
            ax.text(x, v + top * 0.09, "missed", ha="center", va="bottom", fontsize=7.0, color="#9c2f3f")
    ax.set_xticks(xs)
    ax.set_xticklabels([dt.date(int(k[:4]), int(k[5:]), 1).strftime("%b %Y") for k in MONTHS])
    ax.set_ylabel("Refunds made late (% of the month)")
    ax.set_ylim(0, top * 1.25)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#9a9a9a")
    ax.tick_params(colors="#3a3a3a")
    ax.grid(axis="y", color="#e6e6e6", lw=0.6, zorder=0)
    f.tight_layout()
    f.savefig(path, metadata={"Software": None})
    plt.close(f)


def late_sources(m):
    """The delivery months behind the half-year's late refunds, and the months those refunds were made in."""
    made = pd.to_datetime(m.day)
    days = (made - pd.to_datetime(m.delivered.dt.date)).dt.days
    late = m[(days >= W.LATE_DAY) & (made >= pd.Timestamp(2026, 1, 1)) & (made < pd.Timestamp(2026, 7, 1))]
    out = {}
    for k, d in late.groupby(late.delivered.dt.strftime("%Y-%m")):
        out[k] = (len(d), sorted(set(pd.to_datetime(d.day).dt.strftime("%Y-%m"))))
    return out


def backlog_sentence(sources):
    """One sentence on where the late refunds come from, read off late_sources: the month whose deliveries carry most
    of them, the months those were refunded in, and the delivery month of the rest."""
    word = lambda k: dt.date(int(k[:4]), int(k[5:]), 1).strftime("%B")
    names = lambda ks: (", ".join(word(k) for k in ks[:-1]) + " and " + word(ks[-1])) if len(ks) > 1 else word(ks[0])
    main = max(sources, key=lambda k: sources[k][0])
    n, made = sources[main]
    total = sum(v[0] for v in sources.values())
    s = ("%s the %s backlog at the centre: parcels delivered in %s that waited at the back of the hall were opened as it "
         "cleared and refunded from %s to %s." % ("The late refunds follow" if n == total else "Most of the late refunds "
                                                  "follow", word(main), word(main), word(made[0]), word(made[-1])))
    rest = [k for k in sorted(sources) if k != main]
    if rest:
        made_rest = sorted(set(x for k in rest for x in sources[k][1]))
        assert not set(made_rest) & set(made), "a month holds late refunds from two delivery months"
        s += " The late refunds made in %s are for parcels delivered in %s." % (names(made_rest), names(rest))
    return s


def write_note(fig, path, png, sources=None):
    from reportlab.lib.units import mm
    from reportlab.platypus import Image, Paragraph, Spacer
    import docs as D
    h1, h1s, h2 = D.heads(D.PLUM, "LiberationSans")
    doc, frame = D._doc(path, "Refunds made late, January to June 2026", W.PEOPLE["compliance"],
                        "Wrenfield & Holt Ltd  |  Regulatory Compliance  |  Ref TS/CON/26/0417", face="LiberationSans")
    breach = [MONTH_NAMES[k].split()[0] for k in fig["breach_months"]]
    breach_txt = (", ".join(breach[:-1]) + " and " + breach[-1]) if len(breach) > 1 else (breach[0] if breach else "none")
    rows = [["Category of the order", "Vouchers issued for a refund delay", "Value (GBP)"]]
    for k in CATS:
        c = fig["categories"][k]
        rows.append([k, "{:,}".format(c["count"]), "{:,}".format(c["value_gbp"])])
    rows.append(["All categories", "{:,}".format(sum(fig["categories"][k]["count"] for k in CATS)),
                 "{:,}".format(sum(fig["categories"][k]["value_gbp"] for k in CATS))])
    tot = fig["refunds_total"]
    s = [Paragraph("Refunds made late, January to June 2026: &pound;%s to the goodwill fund"
                   % "{:,}".format(fig["payment_gbp"]), h1),
         Paragraph("To %s, %s, Trading Standards Service, %s. From %s, %s, Wrenfield &amp; Holt Ltd. "
                   "12 November 2026. Ref TS/CON/26/0417. Sent with the return under paragraph 2 of the written "
                   "assurance of 9 October 2026." % (W.PEOPLE["officer"], W.ROLES["officer"], W.COUNCIL,
                                                    W.PEOPLE["compliance"], W.ROLES["compliance"]), h1s),
         Paragraph("Payment and commitment", h2),
         Paragraph("We made %s refunds in January to June 2026 for goods returned to our Cotterby returns centre. Of "
                   "those, %s were made on day 15 or later, counting calendar days from the day the goods-in scan "
                   "recorded the parcel at the centre. Under paragraph 5 we will pay <b>&pound;%s</b> into the customer "
                   "goodwill fund held by the Meridale Consumer Trust (%s refunds at &pound;15) within 28 days of this "
                   "return. The 95 per cent commitment in paragraph 4 was <b>not met in %s</b>; it was met in the other "
                   "months. %s"
                   % ("{:,}".format(tot), "{:,}".format(fig["late_total"]), "{:,}".format(fig["payment_gbp"]),
                      "{:,}".format(fig["late_total"]), breach_txt, backlog_sentence(sources)), D.SANS),
         Image(png, width=160 * mm, height=160 * mm * 2.85 / 6.3),
         Paragraph("Refunds made late as a share of each month's refunds. Source: Cotterby goods-in and returns "
                   "processing records and the refund ledger, extracts of 30 October 2026.", D.SMALL),
         Paragraph("How each refund was dated", h2),
         Paragraph("Apart from %s parcels still on prepaid labels in early January, the parcels the centre received in "
                   "2026 carry no reference that the goods-in scans and the processing records share, so each refund's "
                   "delivery day is the goods-in scan of the parcel the centre opened for it. We matched the two records "
                   "in the order the centre works its returns hall: the parcel opened is always the newest one waiting, "
                   "rejected parcels included. That order holds on all %s openings where both records carry the "
                   "parcel's prepaid label, from December 2024 until the last labelled parcels were opened in April "
                   "2026, and it reproduces the late refunds the labels show for February and December 2025."
                   % ("{:,}".format(fig["labels"]["labelled_2026"]), "{:,}".format(fig["labels"]["labelled_openings"])),
                   D.SANS),
         Paragraph("Goodwill vouchers for refund delays", h2),
         Paragraph("Every voucher our customer services team gave for a refund delay in January to June 2026, by the "
                   "main category of the order the refund was on, which is the order named in the customer's case (the "
                   "voucher record's own order field names, for some vouchers, a later order of the customer's that was "
                   "never returned or refunded). "
                   "Irish site vouchers are in euros and are converted at our 2026 reporting rate of &pound;%.2f a "
                   "euro." % fig["eur_rate"], D.SANS),
         D._table(rows, [62 * mm, 58 * mm, 38 * mm], head="#ece6ea"),
         Paragraph("Source: goodwill voucher system, customer case system and order extract, 30 October 2026.", D.SMALL),
         Spacer(1, 8),
         Paragraph("Shares are of each month's refunds made, to one decimal. A refund made on day 14 meets the "
                   "commitment. Refunds for parcels delivered in 2025 count in the month they were made, from their own "
                   "delivery day. Vouchers count in the UK calendar month they were issued.", D.SMALL),
         Spacer(1, 4),
         Paragraph("%s, %s" % (W.PEOPLE["compliance"], W.ROLES["compliance"]), D.SMALL)]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def main(target, gdir, fig_path, extra=None):
    os.makedirs(gdir, exist_ok=True)
    fig, m = compute(target)
    if extra:
        fig.update(extra)
    write_return(fig, os.path.join(gdir, W.GOLDEN["return"]))
    png = os.path.join(gdir, ".chart.png")
    chart(fig, png)
    write_note(fig, os.path.join(gdir, W.GOLDEN["note"]), png, sources=late_sources(m))
    os.remove(png)
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return fig
