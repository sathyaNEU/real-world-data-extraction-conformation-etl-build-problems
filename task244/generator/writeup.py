"""task244 write-up: figures.json (every figure the submission states, as it states them), the quality note's text and
submission.md, all from the answer computed on the built pack."""
import json

import estim as E
import params as P

FLOW_SHORT = {"UE": "job-finding", "EU": "job-loss"}
S = P.STATUS


def pct(x, k=1):
    return round(100.0 * float(x), k)


def figures(A, V):
    """A: solve.answer on the pack; V: the share each rung puts on every rate"""
    cells = []
    for d in P.DCODES:
        for k in ("UE", "EU"):
            cells.append(dict(district=d, name=P.DNAME[d], flow=FLOW_SHORT[k], key=k,
                              published=pct(A["published"][(d, k)]), true_rate=pct(A["true"][(d, k)]),
                              not_real=pct(A["shares"][(d, k)]), warning=(d, k) in A["warned"]))
    warned = [c for c in cells if c["warning"]]
    clear = [c for c in cells if not c["warning"]]
    M, C = A["M"], A["C"]
    gold = A["warned"]
    p0 = list(V["R0 predictive values multiplied"].values())[0]
    p1 = list(V["R1 correct readings multiplied"].values())[0]
    return dict(
        call=dict(answer="no" if warned else "yes", warned=["%s %s rate" % (c["name"], c["flow"]) for c in warned],
                  count=len(warned), of=len(cells)),
        cells=cells,
        reinterview=dict(persons=int(C.sum()),
                         table={a: {b: int(C[S.index(a), S.index(b)]) for b in S} for a in S},
                         matrix={a + b: pct(M[S.index(a), S.index(b)], 2) for a in S for b in S},
                         misread={k: pct(M[S.index(k[0]), S.index(k[1])], 2) for k in ("EU", "EN", "UE", "UN", "NE", "NU")},
                         correct={s: pct(M[i, i], 2) for i, s in enumerate(S)}),
        bands=dict(warned_low=min(c["not_real"] for c in warned), warned_high=max(c["not_real"] for c in warned),
                   clear_low=min(c["not_real"] for c in clear), clear_high=max(c["not_real"] for c in clear)),
        rungs=dict(ppv_statewide=pct(p0), both_right=pct(p1),
                   net_same=E.warned(V["R2 rate overstatement (net)"]) == gold,
                   flow_net_diff=sorted(set(E.warned(V["R2 flow excess (net)"])) ^ set(gold))),
        match=[dict(district=d, name=P.DNAME[d], persons=int(A["match"][d][0]), rate=round(float(A["match"][d][1]), 1),
                    due=int(A["match"][d][2])) for d in P.DCODES],
        days=[dict(district=d, name=P.DNAME[d], persons=int(A["days"][d][0]), mean=round(float(A["days"][d][1]), 1))
              for d in P.DCODES],
        constants=dict(warn_share=round(100 * P.WARN_SHARE, 1), districts=len(P.DCODES), rates=len(cells),
                       quarters_reinterview="2026Q4 to 2027Q4", pairs=len(P.QUARTERS) - 1,
                       sections_cited="methodology note sections 8.1, 8.2 and 8.3"),
    )


def _names(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


def _count(n):
    return WORDS.get(n, str(n))


def _span(xs, unit=" per cent"):
    return "%.1f to %.1f%s" % (min(xs), max(xs), unit)


def golden_content(F):
    warned = [c for c in F["cells"] if c["warning"]]
    clear = [c for c in F["cells"] if not c["warning"]]
    wf = [c for c in warned if c["key"] == "UE"]
    wl = [c for c in warned if c["key"] == "EU"]
    cf = [c for c in clear if c["key"] == "UE"]
    cl = [c for c in clear if c["key"] == "EU"]
    b, m, r, k = F["bands"], F["reinterview"], F["rungs"], F["constants"]
    mr = [x["rate"] for x in F["match"]]
    dy = [x["mean"] for x in F["days"]]
    lead = ("The 2027 annual flows tables cannot go out without the classification-error warning: %d of the %d district "
            "rates carry it." % (F["call"]["count"], k["rates"]))
    paras = [
        "The warning goes on the job-finding rates of %s, and on the job-loss rates of %s. In each of them %s of the "
        "moves the rate counts are not real moves, a third or more. The other %d rates go out without it, at %s. The "
        "chart shows every rate against the line." %
        (_names([c["name"] for c in wf]), _names([c["name"] for c in wl]),
         _span([c["not_real"] for c in warned]), len(clear), _span([c["not_real"] for c in clear])),
        "How the check was made. A person the tables count as moving between two statuses may have held the same status "
        "in both quarters and been recorded wrongly in one of them. The supervisors' reinterview measures how often that "
        "happens: of the {:,} persons reinterviewed within the window over the five quarters whose interviews enter the "
        "tables, an employed person was recorded unemployed {:.2f} per cent of the time, an unemployed person employed "
        "{:.2f} per cent and outside the labour force {:.2f} per cent, and a person outside the labour force unemployed "
        "{:.2f} per cent. With that error taken out at both quarters of each pair, each district's published flows give "
        "its true flows, and a rate's share of counted moves that are not real moves is one less the true moves recorded "
        "correctly in both quarters, over the moves the table counts.".format(
            m["persons"], m["misread"]["EU"], m["misread"]["UE"], m["misread"]["UN"], m["misread"]["NU"]),
        "Why these rates. Most adults stay employed, or outside the labour force, from one quarter to the next, so rare "
        "misreadings of those large groups add up to a large part of the few real moves into or out of unemployment. "
        "The job-loss rates warned are those of the districts where few employed people lose work (true job-loss rates "
        "of %s a quarter, against %s in the other %s), and the job-finding rates warned those where few of the "
        "unemployed find work (%s, against %s). Multiplying the chances that each of a counted mover's two recorded "
        "statuses is right would put every rate at %.1f per cent and warn none: a counted move is far likelier than a "
        "single record to be a misreading, because most people's status did not change." %
        (_span([c["true_rate"] for c in wl]), _span([c["true_rate"] for c in cl]), _count(len(cl)),
         _span([c["true_rate"] for c in wf]), _span([c["true_rate"] for c in cf]), r["ppv_statewide"]),
        "Match rate and reinterview timing. Over the year's four quarter pairs, %s of the persons interviewed in a "
        "dwelling due another visit were interviewed again at its next visit, by district. The supervisors completed "
        "the 2027 reinterviews a mean of %.1f to %.1f days after each person's own interview. The workbook "
        "(elfs_2027_flows_quality.xlsx) has every figure." % (_span(mr), min(dy), max(dy)),
    ]
    sources = ("Sources: %s 2027 annual flows tables as tabulated (28 January 2028); reinterview results and fieldwork "
               "log, 2026Q4 to 2027Q4; quarterly person files, 2026Q4 to 2027Q4; district gazetteer; methodology note, "
               "2027 edition; reinterview protocol, version 3." % P.SURVEY_SHORT)
    footnote = ("Note. The six enumeration areas that moved from the Industrial Corridor to the Metropolitan Fringe on "
                "1 April 2027 are counted in the Fringe in every quarter, their 2026Q4 and 2027Q1 interviews included, "
                "as the tables count them.")
    return dict(title="Quality note: 2027 annual labour market flows", lead=lead, paras=paras, sources=sources,
                footnote=footnote)


def submission(F):
    warned = [c for c in F["cells"] if c["warning"]]
    wf = [c for c in warned if c["key"] == "UE"]
    wl = [c for c in warned if c["key"] == "EU"]
    b, m, r, k = F["bands"], F["reinterview"], F["rungs"], F["constants"]
    n, rest = F["call"]["count"], k["rates"] - F["call"]["count"]
    out = ["## Tags\n",
           "**Domain:** Survey Research & Official Statistics (nonresponse, calibration and measurement-error "
           "adjustment).  ",
           "**Analytical objective:** Data Quality Monitoring & Alerting.\n",
           "## 1. Final Recommendation\n",
           "**No: the 2027 annual flows tables cannot go out without the classification-error warning; %d of the %d "
           "district rates carry it, the job-finding rates of %s, and the job-loss rates of %s.**" %
           (n, k["rates"], _names([c["name"] for c in wf]), _names([c["name"] for c in wl])),
           "",
           "The deciding figure is each rate's share of counted moves that are not real moves, read through the "
           "reconciled reinterview's classification error at both quarters of each pair: %.1f to %.1f per cent for the "
           "%d warned rates against the one-third line, %.1f to %.1f per cent for the other %d. Not the reinterview's "
           "predictive values of the two recorded statuses multiplied, which puts every rate at %.1f per cent and warns "
           "none; not the chances that each status is recorded correctly multiplied, which puts every rate at %.1f per "
           "cent and warns none." % (b["warned_low"], b["warned_high"], n, b["clear_low"], b["clear_high"], rest,
                                     r["ppv_statewide"], r["both_right"]),
           "",
           "## 2. Critical Components\n",
           "1. The reinterview's classification error, {:,} persons reinterviewed within the window over 2026Q4 to "
           "2027Q4: recorded correctly **{:.2f}%** of the employed, **{:.2f}%** of the unemployed and **{:.2f}%** of "
           "those outside the labour force; an unemployed person recorded employed **{:.2f}%** and outside the labour "
           "force **{:.2f}%**, an employed person recorded unemployed **{:.2f}%**, a person outside the labour force "
           "recorded unemployed **{:.2f}%**.".format(
               m["persons"], m["correct"]["E"], m["correct"]["U"], m["correct"]["N"], m["misread"]["UE"],
               m["misread"]["UN"], m["misread"]["EU"], m["misread"]["NU"]),
           "2. Each rate's share of counted moves that are not real moves: **%.1f to %.1f%%** for the %d warned rates, "
           "**%.1f to %.1f%%** for the other %d." % (b["warned_low"], b["warned_high"], n, b["clear_low"],
                                                     b["clear_high"], rest),
           "",
           "## 3. Step-by-Step Solution\n",
           "1. Read Table F1 of elfs_2027_annual_flows_tables.xlsx: each district's persons in each pair of statuses in "
           "two consecutive quarters, the average of the four quarter pairs (methodology note, section 7).",
           "2. Tabulated the {:,} persons in elfs_reinterview_results_2026q4_2027q4.csv by reconciled status and the "
           "status the original interview recorded, each person once and unweighted (reinterview protocol, sections 4 "
           "and 7): the chance each true status is recorded as each status, carried unrounded into every share."
           .format(m["persons"]),
           "3. For each district, took that classification error out of Table F1 at both quarters of each pair (each "
           "quarter's interview by a different interviewer, methodology note section 3) to get the true flows.",
           "4. For each rate, the share of counted moves that are not real moves is one less the true flow times the two "
           "statuses' chances of a correct record, over the counted flow (methodology note, section 8.1): %d rates at a "
           "third or more." % n,
           "5. Match rates: each person interviewed in a dwelling due another visit, found at the dwelling's next visit "
           "as section 8.2 files; each person once, so the 2027Q2 records of 14 May received again under the "
           "dwelling's next household numbers (every field but the household number repeated) and Market Towns area "
           "5's batch received twice count once; districts as from 1 April 2027 (elfs_district_gazetteer_2027.csv).",
           "6. Reinterview timing: each 2027 person's own interview date to the date of the visit that completed the "
           "household's reinterview, from visit_start in elfs_reinterview_fieldwork_log_2026q4_2027q4.csv (from each "
           "tablet's app update, taken at a Friday sync between 18 June and 9 July 2027, the log's call date is the "
           "next Friday sync); section 8.3.",
           "7. The tables carry the warning on %d of the %d rates." % (n, k["rates"]),
           "",
           "## 4. Deliverable Answers\n",
           "### elfs_2027_flows_quality.xlsx\n",
           "1. Each rate's share of counted moves that are not real moves (per cent) and the warning, %d rows:" % k["rates"]]
    for c in F["cells"]:
        out.append("   - %s (%s) %s: %.1f, %s" % (c["name"], c["district"], c["flow"], c["not_real"],
                                                  "warning" if c["warning"] else "no warning"))
    out.append("2. Each district's match rate (per cent) and the persons it is based on, summed over the four quarter "
               "pairs 2026Q4 to 2027Q4:")
    for x in F["match"]:
        out.append("   - %s: %.1f, %s persons" % (x["name"], x["rate"], "{:,}".format(x["due"])))
    out.append("3. Each district's mean days from interview to reinterview, interviews of 2027:")
    for x in F["days"]:
        out.append("   - %s: %.1f days" % (x["name"], x["mean"]))
    out += ["",
            "### elfs_2027_flows_note.docx\n",
            "1. The answer: the tables cannot go out without the warning; %d of the %d rates carry it, each named." %
            (n, k["rates"]),
            "2. Chart: each of the %d rates' share of counted moves that are not real moves, with the one-third warning "
            "line and the warned rates marked." % k["rates"]]
    return "\n".join(out) + "\n"


def write(path_json, F):
    with open(path_json, "w") as fh:
        json.dump(F, fh, indent=1)
        fh.write("\n")
