"""The golden deliverables for task482 from golden.solve(): the conformed member-year file (CSV), the costing memo to
the bargaining committee (PDF) and the chart of the increases against the mandate's limit (SVG). write() returns
the content of generator/figures.json."""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W    # noqa: E402
import golden as G   # noqa: E402

MEMO_STAMP = b"D:20261016153000-05'00'"
LABEL = {150000: "1,500", 200000: "2,000", 300000: "3,000"}


def amt(c):
    return "%.2f" % (c / 100.0)


def usd(c):
    return "{:,.2f}".format(c / 100.0)


def member_year(path, res):
    mm, dem, put, rel, paid = res["mm"], res["dem"], res["put"], res["rel"], res["paid25"]
    persons = sorted(k for k, m in mm.items() if m > 0)
    tot = dict(rows=0, months=0, paid=0, share=0, put=0, cost={m: 0 for m in W.OPTIONS})
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\r\n")
        wr.writerow(["member_id", "relationship", "covered_months_2025", "plan_paid_2025",
                     "plan_share_2025_services_2027_fees", "put_off_work_2027_fees",
                     "cost_max_1500", "cost_max_2000", "cost_max_3000"])
        for k in persons:
            d, u = dem.get(k, 0), put.get(k, 0)
            cs = [min(d + (u if m > W.MAXIMUM else 0), m) for m in W.OPTIONS]
            wr.writerow([k, rel.get(k, ""), mm[k], amt(paid.get(k, 0)), amt(d), amt(u)] + [amt(c) for c in cs])
            tot["rows"] += 1
            tot["months"] += mm[k]
            tot["paid"] += paid.get(k, 0)
            tot["share"] += d
            tot["put"] += u
            for m, c in zip(W.OPTIONS, cs):
                tot["cost"][m] += c
    for m in W.OPTIONS:
        assert tot["cost"][m] == res["gold"]["options"][m]["cost"], m
    assert tot["months"] == res["gold"]["months"] and tot["put"] == sum(put.values())
    return tot


def memo(path, res, tot):
    import docs as Dc
    import postprocess as PP
    P, T, H, SMALL = Dc.P, Dc.T, Dc.H, Dc.SMALL
    g = res["gold"]["options"]
    A, (owed, kids) = res["ask_a"], res["ortho"]
    call = res["call"]
    s = [P("Memorandum", T),
         P("To: Bargaining Committee (Barry Rowland, Vice President, Finance, chair). From: Audrey Bautista, Benefits "
           "Manager. Date: 16 October 2026.", SMALL),
         P("Subject: Dental Plan annual maximum for 2027, costed under Finance Policy F-17", H),
         P("1. Recommendation", H),
         P("Agree an annual maximum of %s dollars per covered person from 1 January 2027. Under F-17 it adds %.2f "
           "dollars per covered person month to the plan's cost, inside the 1.90 dollars Board Resolution 2026-31 "
           "allows. The union's proposal of 3,000 dollars adds %.2f dollars and is outside the mandate."
           % (LABEL[call], g[200000]["increase"], g[300000]["increase"])),
         P("2. Costing", H),
         Dc._table([["Annual maximum", "2027 cost per covered person month", "Increase over 1,500", "Within the mandate"],
                    ["1,500 (current)", "%.2f" % g[150000]["pmpm_c"], "", ""],
                    ["2,000", "%.2f" % g[200000]["pmpm_c"], "%.2f" % g[200000]["increase"],
                     "Yes" if g[200000]["increase"] * 100 <= W.LIMIT else "No"],
                    ["3,000", "%.2f" % g[300000]["pmpm_c"], "%.2f" % g[300000]["increase"],
                     "Yes" if g[300000]["increase"] * 100 <= W.LIMIT else "No"]],
                   [1.4 * Dc.inch, 2.3 * Dc.inch, 1.5 * Dc.inch, 1.4 * Dc.inch]),
         Dc.Spacer(1, 6),
         P("Basis: the 2025 plan year, %s covered persons and %s covered person months, at Ridgeline's 2027 network "
           "fee schedule. Ridgeline's Classic and Nexus claim lines are taken at their final version and joined to "
           "one record per person through the July 2025 crosswalk; pembrook_dental_member_year_2025.csv carries each "
           "person's year. In 2025, %d members whose predetermination showed the 1,500 dollar maximum reducing the "
           "plan's payment did not have that work done in 2025 and had it done after the plan year started again on "
           "1 January 2026, within the estimate's 12 months: %s dollars of plan share at the 2027 fees. With a higher "
           "maximum that work falls in the plan year, so it is costed in it."
           % ("{:,}".format(tot["rows"]), "{:,}".format(tot["months"]), len(res["put"]), usd(tot["put"]))),
         P("3. Predetermination service, Schedule C.2", H),
         Dc._table([["Quarter of receipt", "Requests received", "Estimated within five business days", "90 per cent met"]] +
                   [[q[:4] + " Q" + q[-1], "{:,}".format(A[q][0]), "{:,}".format(A[q][1]),
                     "Yes" if A[q][1] * 10 >= A[q][0] * 9 else "No"] for q in G.QUARTERS],
                   [1.4 * Dc.inch, 1.5 * Dc.inch, 2.4 * Dc.inch, 1.3 * Dc.inch]),
         Dc.Spacer(1, 6),
         P("4. Orthodontic payments still owed at 30 September 2026", H),
         Dc._table([["Year treatment began", "Children in treatment", "Payments still owed"]] +
                   [[str(y), str(kids[y]), usd(owed[y])] for y in G.START_YEARS],
                   [1.8 * Dc.inch, 1.8 * Dc.inch, 1.8 * Dc.inch]),
         Dc.Spacer(1, 10),
         P("Prepared by Audrey Bautista, Benefits Manager. Reviewed by Barry Rowland, Vice President, Finance.", SMALL)]
    Dc._pdf(path, "Dental Plan Annual Maximum 2027", s, W.PEOPLE["benefits"], W.COMPANY)
    PP.normalize_pdf(path, MEMO_STAMP, MEMO_STAMP)


def chart(path, res):
    g = res["gold"]["options"]
    vals = [(LABEL[m], g[m]["increase"]) for m in W.OPTIONS[1:]]
    x0, y0, wd, ht, top = 90, 330, 480, 250, 2.5
    y = lambda v: y0 - ht * v / top
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="640" height="400" viewBox="0 0 640 400" '
           'font-family="Arial, Helvetica, sans-serif">',
           '<rect width="640" height="400" fill="#ffffff"/>',
           '<text x="24" y="30" font-size="16" font-weight="bold" fill="#222222">Dental Plan 2027: increase in cost per '
           'covered person month</text>',
           '<text x="24" y="50" font-size="12" fill="#555555">Finance Policy F-17, 2025 plan year at 2027 fees, '
           'against the current 1,500 dollar maximum</text>']
    for k in range(6):
        v = 0.5 * k
        out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#e3e3e3" stroke-width="1"/>' % (x0, y(v), x0 + wd, y(v)))
        out.append('<text x="%d" y="%.1f" font-size="11" fill="#555555" text-anchor="end">%.2f</text>' % (x0 - 8, y(v) + 4, v))
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#333333" stroke-width="1"/>' % (x0, y0, x0 + wd, y0))
    for i, (lab, v) in enumerate(vals):
        cx = x0 + 120 + 240 * i
        colour = "#2f6f9f" if v * 100 <= W.LIMIT else "#b5523b"
        out.append('<rect x="%d" y="%.1f" width="120" height="%.1f" fill="%s"/>' % (cx - 60, y(v), y0 - y(v), colour))
        out.append('<text x="%d" y="%.1f" font-size="13" font-weight="bold" fill="#222222" text-anchor="middle">%.2f</text>'
                   % (cx, y(v) - 8, v))
        out.append('<text x="%d" y="%d" font-size="12" fill="#222222" text-anchor="middle">%s dollar maximum</text>'
                   % (cx, y0 + 20, lab))
    lim = W.LIMIT / 100.0
    out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#222222" stroke-width="1.5" stroke-dasharray="6 4"/>'
               % (x0, y(lim), x0 + wd, y(lim)))
    out.append('<text x="%d" y="%.1f" font-size="11" fill="#222222" text-anchor="end">Board Resolution 2026-31 limit '
               '%.2f</text>' % (x0 + wd, y(lim) - 6, lim))
    out.append('<text x="24" y="%d" font-size="11" fill="#555555" transform="rotate(-90 24 %d)">Dollars per covered '
               'person month</text>' % (y0 - 40, y0 - 40))
    out.append('<text x="24" y="385" font-size="10" fill="#777777">Benefits Department, 16 October 2026</text>')
    out.append('</svg>')
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")


def write(gpath, res):
    tot = member_year(gpath("member_year"), res)
    memo(gpath("memo"), res, tot)
    chart(gpath("chart"), res)
    g, n = res["gold"]["options"], res["naive"]["options"]
    owed, kids = res["ortho"]
    return dict(
        call=dict(maximum=LABEL[res["call"]], continuance=LABEL[res["naive_call"]]),
        constants=dict(current="1,500", options=["2,000", "3,000"], limit="1.90", deductible=50, validity_months=12,
                       standard_days=5, standard_share=90),
        plan_year=dict(persons=tot["rows"], months=tot["months"]),
        cost={LABEL[m]: "%.2f" % g[m]["pmpm_c"] for m in W.OPTIONS},
        increase={LABEL[m]: "%.2f" % g[m]["increase"] for m in W.OPTIONS[1:]},
        continuance_increase={LABEL[m]: "%.2f" % n[m]["increase"] for m in W.OPTIONS[1:]},
        put_off=dict(members=len(res["put"]), amount=usd(tot["put"])),
        member_year=dict(rows=tot["rows"], months=tot["months"], put=usd(tot["put"]),
                         cost={LABEL[m]: usd(tot["cost"][m]) for m in W.OPTIONS}),
        ask_a={q: list(res["ask_a"][q]) for q in G.QUARTERS},
        ask_b={str(y): dict(children=kids[y], owed=usd(owed[y])) for y in G.START_YEARS})
