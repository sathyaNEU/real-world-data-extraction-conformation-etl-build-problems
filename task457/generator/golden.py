"""The two deliverables and figures.json, computed from the bundle alone.

coi_committee_docket_2027-02.docx   the office's docket memo to the committee: the fifteen, each with department and
                                    manufacturer, a chart of the fifteen estimates, the 2026
                                    disclosure cycle's two counts and the two supporting tables
faculty_remuneration_2026_conformed.csv  each faculty member's remuneration from manufacturers for each year 2021 to 2026
                                    they owed a disclosure, disclosed and as Open Payments published it"""
import csv
import datetime as dt
import io
import json
import os

import asks as A
import conform as C
import methods as M
import world as W

DOCKET = "coi_committee_docket_2027-02.docx"
WORDS = ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
CONFORMED = "faculty_remuneration_2026_conformed.csv"


def thousand(x):
    return int(round(x / 1000.0)) * 1000


def analysis(target):
    data = C.load(target)
    cf = M.Conformed(data)
    g = M.golden(cf)
    fac = C.faculty(data)
    ents = {e["open_payments_id"]: e["entity_name"] for e in data["entities"] if e["open_payments_id"]}
    for r in data["register"]:
        ents.setdefault(r["Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_ID"],
                        r["Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Name"])
    ranked = g["ranked"]
    members = []
    for e, (est, m) in ranked[:16]:
        f = fac[e]
        members.append({"emp_id": e, "name": "%s %s" % (f["first"], f["last"]), "last": f["last"], "first": f["first"],
                        "dept": W.DEPT_NAME[C.dept_on(data, f, dt.date(2026, 12, 31))], "manufacturer": ents[m],
                        "disclosed": cf.by_person_year[(e, 2026)][m], "estimate": est,
                        "december": cf.day[(e, 2026)].year == 2026})
    est25 = M.estimates(cf, 2025, "line", "n", g["K"], "sum", align="both")
    nm = lambda e: "%s %s" % (fac[e]["first"], fac[e]["last"])
    srt = lambda es: [nm(e) for e in sorted(es, key=lambda e: (fac[e]["last"], fac[e]["first"]))]
    gold = set(g["docket"])
    # the same estimate with every disclosure read as covering the whole year, at its own closest weighting
    k_un = min(M.GRIDS["n"], key=lambda K: M.backtest(cf, "line", "n", K, "sum"))
    unaligned = set(M.docket(cf, "line", "n", k_un, "sum")[0])
    face = set(M.docket(cf, "line", "face")[0])
    asks = A.stops(data)
    under = [e for e in gold if cf.day[(e, 2026)].year > 2026 and
             ranked[[x[0] for x in ranked].index(e)][1][0] >= 1.4 * cf.by_person_year[(e, 2026)][ranked[[x[0] for x in ranked].index(e)][1][1]]]
    return {"data": data, "cf": cf, "golden": g, "members": members, "n2026": len(ranked), "n2025": len(est25),
            "under": srt(under),
            "december": srt(e for e in gold if cf.day[(e, 2026)].year == 2026),
            "unaligned_in": srt(unaligned - gold), "unaligned_out": srt(gold - unaligned), "k_unaligned": k_un,
            "face_in": srt(face - gold), "asks": asks, "face_bt": M.backtest(cf, "line", "face"),
            "unaligned_bt": M.backtest(cf, "line", "n", k_un, "sum")}


def chart(members, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "svg.hashsalt": "task457",
                         "pdf.fonttype": 42})
    rows = list(reversed(members))
    fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=200)
    labels = ["%s, %s" % (m["last"], m["first"][0] + ".") for m in rows]
    vals = [m["estimate"] / 1000.0 for m in rows]
    cols = ["#9c5b64" if m["december"] else "#6b1f2a" for m in rows]
    ax.barh(range(len(rows)), vals, color=cols, height=0.68)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(labels)
    ax.set_xlabel("Estimated 2026 remuneration from one manufacturer (thousands of US dollars)")
    ax.xaxis.grid(True, color="#e3e4e7", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(0, (int(max(vals) / 25) + 1) * 25)
    ax.set_title("The docket's fifteen, by estimated 2026 remuneration from a single manufacturer", fontsize=9.5,
                 loc="left")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    open(path, "wb").write(buf.getvalue())


def write_docket(an, path, png):
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, Mm, RGBColor
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(215.9), Mm(279.4)
    sec.left_margin = sec.right_margin = Mm(22)
    sec.top_margin, sec.bottom_margin = Mm(18), Mm(18)
    foot = sec.footer.paragraphs[0]
    foot.text = "%s, %s. Docket for the meeting of 11 February 2027. Confidential: committee use." % (W.ORG, W.OFFICE)
    foot.runs[0].font.size = Pt(7.5)

    def para(text, bold=False, size=None, color=None, align=None, space=6, italic=False):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.bold, r.italic = bold, italic
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        if align:
            p.alignment = align
        p.paragraph_format.space_after = Pt(space)
        return p

    def table(header, rows, widths, right=()):
        t = doc.add_table(rows=1, cols=len(header))
        t.style = "Light List"
        t.alignment = WD_TABLE_ALIGNMENT.LEFT
        for k, h in enumerate(header):
            c = t.rows[0].cells[k]
            c.text = h
            c.paragraphs[0].runs[0].bold = True
            c.paragraphs[0].runs[0].font.size = Pt(9)
        for row in rows:
            cells = t.add_row().cells
            for k, v in enumerate(row):
                cells[k].text = v
                cells[k].paragraphs[0].runs[0].font.size = Pt(9)
                if k in right:
                    cells[k].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for row in t.rows:
            for k, w in enumerate(widths):
                row.cells[k].width = Mm(w)
        return t

    para(W.ORG.upper(), bold=True, size=9, color="6B1F2A", space=0)
    para(W.OFFICE, size=9, color="5D6168", space=10)
    para("To: %s\nFrom: %s, Director\nDate: 27 January 2027\nSubject: Docket for the meeting of 11 February 2027" % (
        W.COMMITTEE, W.PEOPLE["director"]), size=10, space=12)
    para("Fifteen faculty members for the February docket", bold=True, size=14, space=4)
    mem = an["members"][:15]
    para("Under section 5 of Policy RI-14 the committee reviews the fifteen members of the clinical faculty with the largest "
         "remuneration from a single manufacturer in 2026. Open Payments will publish 2026 at the end of June, so the "
         "office has estimated each faculty member's remuneration from each manufacturer named in their 2026 annual "
         "disclosure: %d faculty members holding an appointment on 31 December 2026 filed a 2026 disclosure naming a "
         "manufacturer, and all of them were estimated." % an["n2026"], space=6)
    para("Section 5.4 has the office use the estimate that comes closest to the latest year Open Payments has published. "
         "Made from the 2025 disclosures and the years before them, and compared with what Open Payments' January 2027 "
         "publication shows for each of the %d faculty members estimated for 2025, this one comes closer than any estimate "
         "that reads a disclosure as covering its whole year, and the variants of it that come closer still name the same "
         "fifteen. A disclosure carries what each company had paid by the day it was submitted, so a disclosure submitted "
         "in December misses the payments made after it. Each faculty member's reporting share is the total they disclosed "
         "over the total the register shows paid by the day each disclosure was submitted, on the manufacturer-years for "
         "which both a disclosure and a publication show remuneration, 2021 to 2025, weighted toward the same share across "
         "the whole faculty by n/(n+%d), n the number of those manufacturer-years, the whole-number weighting that comes "
         "closest. Each 2026 amount is divided by that share and, where the disclosure was submitted in December, by the share of the year's "
         "payments the same manufacturer had made by that date the year before. A faculty member's estimate is the "
         "largest of their manufacturers'." % (an["n2025"], an["golden"]["K"]), space=6)
    para(("%s of the fifteen submitted their 2026 disclosure in the first days of December, before their retainers' "
          "December installments; corrected as if every disclosure covered the whole year, %s of them would give way to "
          "faculty whose earlier December disclosures made them look like under-reporters. The record also carries "
          "faculty who disclose about half of what manufacturers report paying them, year after year, on records long "
          "enough to measure it; faculty whose records hold a single matched manufacturer-year are weighted toward the "
          "faculty-wide share rather than taken at their own.") % (WORDS[len(an["december"])].capitalize(),
                                                                  WORDS[len(an["unaligned_out"])]), space=10)
    para("The docket, in alphabetical order", bold=True, size=11, space=3)
    rows = [[m["name"] + (" *" if m["december"] else ""), m["dept"], m["manufacturer"],
             "${:,.0f}".format(thousand(m["disclosed"]))] for m in sorted(mem, key=lambda m: (m["last"], m["first"]))]
    table(["Faculty member", "Department", "Manufacturer of the largest 2026 remuneration", "Disclosed for 2026"], rows,
          [42, 44, 62, 26], right=(3,))
    para("Departments are those of each faculty member's primary appointment on 31 December 2026. The amount disclosed is "
         "from the 2026 disclosure in force on 21 January 2027, rounded to the nearest thousand dollars; an asterisk marks "
         "a disclosure submitted in December 2026.", size=8, italic=True, color="5D6168", space=10)
    doc.add_picture(png, width=Mm(165))
    para("The lighter bars are the disclosures submitted in December 2026.", size=8, italic=True, color="5D6168",
         space=10)

    ask = an["asks"]
    para("The 2026 disclosure cycle", bold=True, size=11, space=3)
    a = ask["A"]["golden"]
    para("%s faculty members owed a 2026 disclosure, and %s of them had not submitted it by 11:59 p.m. Eastern time on "
         "15 January 2027." % ("{:,}".format(a[0]), "{:,}".format(a[1])), space=3)
    para("Owed: an appointment on 31 December 2026, each faculty member counted once; a faculty member whose employee "
         "number changed in 2026 filed under the number the disclosure system holds. Not submitted: no submission of the "
         "2026 disclosure by the deadline; the disclosure system records times in UTC.", size=8, italic=True,
         color="5D6168", space=10)
    para("Open Payments, 2025: remuneration to the faculty", bold=True, size=11, space=3)
    b = ask["B"]["golden"]
    rows = [[A.NATURE_LABEL[k], "${:,.0f}".format(thousand(v))] for k, v in b.items()]
    table(["Nature of payment", "Published for 2025"], rows, [110, 40], right=(1,))
    para("Open Payments' publication of 15 January 2027. Faculty members who held an appointment at any time in 2025, all "
         "of their 2025 records; records tied to faculty through Open Payments' covered-recipient profiles; payments made "
         "to the university at a faculty member's request excluded. Rounded to the nearest thousand dollars.", size=8,
         italic=True, color="5D6168", space=10)
    para("2026 remuneration from companies outside Open Payments", bold=True, size=11, space=3)
    c = ask["C"]["golden"]
    rows = [[k, "${:,.0f}".format(thousand(v))] for k, v in c.items()]
    table(["Relationship type", "Disclosed for 2026"], rows, [110, 40], right=(1,))
    para("From the 2026 disclosures in force: companies that appear in Open Payments under no name, the names "
         "manufacturers reported under in earlier years included; two companies the entity list still shows without an "
         "identifier have reported to Open Payments since program year 2025. Rounded to the nearest thousand dollars.",
         size=8, italic=True, color="5D6168", space=6)
    doc.core_properties.author = W.PEOPLE["director"]
    doc.save(path)


def write_conformed(an, path):
    """One row per faculty member and year 2021 to 2026 they owed a disclosure (an appointment on 31 December), under
    the employee number holding that appointment; a faculty member whose number changed is one faculty member."""
    data, cf = an["data"], an["cf"]
    fac = C.faculty(data)
    by_npi = {}
    for e in sorted(fac):
        by_npi.setdefault(fac[e]["npi"], []).append(e)
    rows = []
    for npi, emps in sorted(by_npi.items(), key=lambda kv: min(kv[1])):
        for y in range(2021, 2027):
            day = dt.date(y, 12, 31)
            holder = [e for e in emps if C.holds(fac[e], day)]
            if not holder:
                continue
            e0 = holder[0]
            f = fac[e0]
            dis = {}
            pub = {}
            for e in emps:
                for m, v in cf.by_person_year.get((e, y), {}).items():
                    dis[m] = dis.get(m, 0.0) + v
                if y <= 2025:
                    for m, v in cf.pub_by_person_year.get((e, y), {}).items():
                        pub[m] = pub.get(m, 0.0) + v
            rows.append([e0, f["last"], f["first"], C.dept_on(data, f, day), y, "%.2f" % sum(dis.values()), len(dis),
                         "" if y > 2025 else "%.2f" % sum(pub.values()), "" if y > 2025 else len(pub)])
    rows.sort(key=lambda r: (r[0], r[4]))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["emp_id", "last_name", "first_name", "dept_code", "year", "remuneration_disclosed_usd",
                    "manufacturers_disclosed", "remuneration_published_usd", "manufacturers_published"])
        w.writerows(rows)
    return len(rows)


def main(target, out, figures_path):
    os.makedirs(out, exist_ok=True)
    an = analysis(target)
    png = os.path.join(os.path.dirname(figures_path), "docket_chart.png")
    chart(an["members"][:15], png)
    write_docket(an, os.path.join(out, DOCKET), png)
    os.remove(png)
    n_rows = write_conformed(an, os.path.join(out, CONFORMED))
    mem = an["members"]
    a, b, c = an["asks"]["A"]["golden"], an["asks"]["B"]["golden"], an["asks"]["C"]["golden"]
    fig = {
        "call": sorted(m["name"] for m in mem[:15]),
        "call_members": [{"name": m["name"], "department": m["dept"], "manufacturer": m["manufacturer"],
                          "disclosed_2026": thousand(m["disclosed"])} for m in sorted(mem[:15], key=lambda m: (m["last"], m["first"]))],
        "faculty_estimated_2026": an["n2026"],
        "faculty_estimated_2025": an["n2025"],
        "weighting_k_lines": an["golden"]["K"],
        "december_filers_on_docket": an["december"],
        "under_reporters": an["under"],
        "whole_year_reading_instead": an["unaligned_in"],
        "whole_year_reading_drops": an["unaligned_out"],
        "ask_a": {"owed": a[0], "not_submitted": a[1]},
        "ask_b": {A.NATURE_LABEL[k]: thousand(v) for k, v in b.items()},
        "ask_c": {k: thousand(v) for k, v in c.items()},
        "conformed_rows": n_rows,
        "deadline_eastern": "11:59",
        "policy_sections_cited": ["2.1", "2.2", "5.2", "5.4"],
    }
    json.dump(fig, open(figures_path, "w"), indent=1, sort_keys=False)
    open(figures_path, "a").write("\n")
    return an
