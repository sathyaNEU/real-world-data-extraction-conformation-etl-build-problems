"""submission.md, drafted from golden.figures() so every figure is emitted, never typed."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as GD   # noqa: E402


def n0(x):
    return "{:,}".format(int(round(x)))


def write(R, path):
    M, A, B, BI = R["M"], R["A"], R["B"], R["B_info"]
    st = M["btp_hub_by_station"]
    hs, ks = st["On or near Calderwick (station)"], st["On or near Kingsway (station)"]
    own, btp = M["F"]["F1 the model as filed"], M["B"]["B2 per-type rates with the warrant share"]
    cl = BI["closures"]
    L = []
    L += ["## Tags", "",
          "**Domain:** Urban & Regional Science (municipal service demand and resource allocation).",
          "**Analytical objective:** Forecasting & Predictive Modeling.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Calderwick Police should give the Tanner Street custody hub a planning figure of %s detentions for 2027-28.**"
          % n0(M["golden"]),
          "The hub will book the six wards' arrests by the force's own officers, %s by the custody demand model, and the "
          "arrests British Transport Police officers make at Calderwick and Kingsway stations, %s, which BTP books into "
          "the suite serving the ward: %s before rounding. Not %s, the model run on the force's arrest records alone, "
          "which hold none of BTP's arrests." % (n0(own), n0(btp), "{:,.1f}".format(M["golden_raw"]), n0(M["default"])), ""]
    L += ["## 2. Critical Components", "",
          "1. The six wards' 2027-28 arrests by Calderwick Police officers, by the custody demand model, are **%s**." % n0(own),
          "2. British Transport Police recorded **%s** crimes in the six wards in 2025-26, all at Calderwick station (%s) "
          "and Kingsway station (%s)." % (n0(M["btp_hub_crimes"]), n0(hs), n0(ks)),
          "3. BTP's arrests at the two stations, those crimes at the force's own 2025-26 arrests per recorded crime of each "
          "type with its warrant share, are **%s** a year." % n0(btp), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Took the six wards that move to Tanner Street from custody_suite_allocation_2027.xlsx and counted their arrests "
          "in calderwick_police_arrests_2021-04_2026-09.csv by financial year of the UK date of arrest: %s in 2025-26."
          % n0(M["own_2025"]),
          "2. Carried each ward's 2025-26 arrests two years at its capped three-year change and summed the six wards, per "
          "the method in custody_demand_model_v2.pdf: %s." % n0(own),
          "3. Read note 2 of the allocation's Notes sheet (a detainee goes to the suite serving the ward of arrest, whichever "
          "force or agency arrests them) and took British Transport Police's rows in police_uk_street_crime_2025-26.csv whose "
          "LSOA lies in the six wards by lsoa21_to_ward_lookup.csv: %s crimes." % n0(M["btp_hub_crimes"]),
          "4. Multiplied BTP's crimes of each type by the force's 2025-26 arrests in that offence group over its own "
          "street-level crimes of that type, and added the force's warrant, recall or breach share (%.1f per cent): %s; "
          "with the model's %s the hub's 2027-28 detentions are %s." % (100 * M["warrant_share"], n0(btp), n0(own),
                                                                         "{:,.1f}".format(M["golden_raw"])),
          "5. For the remand holds, matched each file in cju_remand_files_2025-03_2026-04.csv to the remanded arrest charged "
          "at its suite at its charge time (the linked arrest, or the later arrest when the linked one is the case's earlier "
          "release), added the remanded arrests with no file arrested in the same minute, ward and offence group, each on its "
          "own charge and booking times and the file's handover, and kept the defendants charged in 2025-26 (UK times "
          "converted to UTC): %s defendants." % n0(sum(A[s]["defendants"] for s in GD.SUITES)),
          "6. For the assessments, counted the initial health assessment lines in custody_healthcare_contacts_2025-26.csv, "
          "joining a line that starts at 07:00 or 19:00 on the end of the episode's previous assessment, and placed a closed "
          "suite's team's lines at the suite its wards were booked into while the arrest records show no booking at the "
          "closed suite, from the last booking before the gap to the first after it (Eastmoor at Northgate, 14 August to "
          "2 September 2025; Wendle Cross at Southfields, 3 November 2025 to 30 January 2026).",
          "7. Planning figure for 2027-28: %s detentions." % n0(M["golden"]), ""]
    L += ["## 4. Deliverable Answers", "", "### tanner_street_planning_figure_2027-28.xlsx", "",
          "1. Planning figure for 2027-28: %s detentions (%s unrounded)." % (n0(M["golden"]), "{:,.1f}".format(M["golden_raw"])),
          "2. Built from: %s arrests by Calderwick Police officers in the six wards (custody demand model) and %s arrests by "
          "British Transport Police officers at Calderwick and Kingsway stations (from %s recorded crimes)."
          % (n0(own), n0(btp), n0(M["btp_hub_crimes"])),
          "3. Remand holds, defendants charged in 2025-26 and kept in custody for court, cell hours from charge to handover "
          "and holds over 24 hours from booking in:"]
    for s in GD.SUITES:
        L.append("   - %s: %s cell hours, %s held more than 24 hours" % (s, n0(A[s]["cell_hours"]), n0(A[s]["over_24"])))
    L.append("4. Initial health assessments in 2025-26, begun from 07:00 to 19:00 and begun at night:")
    for s in GD.SUITES:
        L.append("   - %s: %s by day, %s at night" % (s, n0(B[s]["day"]), n0(B[s]["night"])))
    L += ["", "### hub_planning_note.docx", "",
          "1. The note gives the planning figure of %s detentions and its two parts, %s and %s." % (n0(M["golden"]), n0(own), n0(btp)),
          "2. Bar chart of the six wards' arrests from the force's records for each financial year from 2021-22 to 2025-26 (%s), "
          "beside a 2027-28 bar of %s stacked as the model's %s and BTP's %s."
          % (", ".join(n0(M["fy_hub"][y]) for y in sorted(M["fy_hub"])), n0(M["golden"]), n0(own), n0(btp)), ""]
    with open(path, "w") as fh:
        fh.write("\n".join(L))


if __name__ == "__main__":
    write(GD.figures(sys.argv[1] if len(sys.argv) > 1 else GD.BD.TARGET),
          os.path.join(os.path.dirname(HERE), "submission.md"))
