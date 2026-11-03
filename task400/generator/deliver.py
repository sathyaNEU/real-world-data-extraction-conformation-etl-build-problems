"""The golden deliverables (the committee paper and the workings) and the figures the write-up states."""
import pandas as pd
import datetime as dt
import io
import os

import golden as G
import postprocess as PP

COMPANY = "Ternhallow Iron Ore Pty Ltd"
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def figures(target):
    P = G.load(target)
    F = {}
    w = G.window_counts(P)
    F["vi_jul_oct_2025"] = w[2025]
    F["vi_jul_oct_2026"] = w[2026]
    F["monthly"] = G.monthly_counts(P)
    a = G.crit_responses(P)
    rs = G.response_summary(a)
    # stated to the nearest 5 per cent, the precision the rollout weeks carry however they are bounded
    F["resp_window_v43_pct"] = int(5 * round(rs["window"]["4.3"][0] * 20))
    F["resp_window_v5_pct"] = int(5 * round(rs["window"]["5.0.2"][0] * 20))
    gt = G.gate_trips(P)
    for m, (n, nt) in gt.items():
        F["trips_%02d" % m] = n
        F["trips_notag_%02d" % m] = nt
    os_ = G.overspeed(P)
    for (seg, m), (n, o5, _) in os_.items():
        F["os_%s_%02d" % (seg, m)] = n
        F["os5_%s_%02d" % (seg, m)] = o5
    F["call"] = "C"
    # labels the write-up quotes, read from the pack rather than typed
    fw = P["fw"].copy()
    fw["local"] = pd.to_datetime(fw["Applied (UTC)"]) + pd.Timedelta(hours=8)
    u = G.truck_of_unit(P)
    fw = fw.merge(u[["Serial", "Installed"]], on="Serial")
    # the upgrade of units already in service, not a replacement unit loaded with 5.0.2 when it was fitted
    v5 = fw[fw["Version"].str.startswith("5") & (fw["local"].dt.normalize() > pd.to_datetime(fw["Installed"]))]["local"]
    F["rollout_days"] = "%d and %d June 2026" % (v5.min().day, v5.max().day)
    F["firmware_families"] = "4.3 and 5.0.2"
    F["terms_clauses"] = "2.1, 3.1, 3.2, section 4"
    F["rate_basis"] = "per 1,000 truck shifts"
    return F, P, a, rs


def chart_png(F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    labels = ["%s %s" % (MON[ym % 100 - 1], str(ym // 100)[2:]) for ym, _ in F["monthly"]]
    vals = [v for _, v in F["monthly"]]
    fig, ax = plt.subplots(figsize=(7.2, 3.1), dpi=150)
    cols = ["#7f9fbf" if ym // 100 == 2025 else "#2f5f8f" for ym, _ in F["monthly"]]
    ax.bar(range(len(vals)), vals, color=cols, width=0.72)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.4, str(v), ha="center", va="bottom", fontsize=6.5)
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels(labels, rotation=60, fontsize=6.8)
    ax.set_ylabel("Incidents (VI-COL and VI-SPI)", fontsize=7.5)
    ax.set_title("Mount Bracken vehicle interaction incidents by month, January 2025 to October 2026", fontsize=8.5)
    ax.tick_params(axis="y", labelsize=7)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def paper_docx(path, F):
    import docx
    from docx.shared import Pt, Cm
    d = docx.Document()
    d.styles["Normal"].font.name = "Calibri"
    d.styles["Normal"].font.size = Pt(10.5)
    d.add_heading("Vehicle interaction programme for 2027", level=1)
    p = d.add_paragraph("To: Site safety steering committee, meeting of 19 November 2026. From: Health and Safety "
                        "Superintendent. Under HSE-TOR-026 and improvement notice IN-2026-0417.")
    p.runs[0].font.size = Pt(9)
    d.add_heading("Recommendation", level=2)
    d.add_paragraph("Fund programme C, the collision avoidance alerting review on the haul truck units. The rise in vehicle "
                    "interaction incidents, from %d in July to October 2025 to %d in July to October 2026, came with the "
                    "5.0.2 firmware on the haul truck units: since it went on, operators slow for a critical alert about a "
                    "third of the time, where on the earlier firmware they slowed for nearly nine in ten, and the critical "
                    "alerts nobody slows for now run at more than five times last year's level."
                    % (F["vi_jul_oct_2025"], F["vi_jul_oct_2026"]))
    d.add_heading("What drove the rise", level=2)
    for t in [
        "The firmware went on truck by truck between 2 and 23 June 2026, so for three weeks the same crews drove trucks on "
        "both. Reading each critical alert in those weeks against the truck's speed in the event window the dispatch "
        "system opened on it, operators slowed by 6 km/h or more within six seconds for about %d per cent of critical "
        "alerts from units still on 4.3 and for about %d per cent from units already on 5.0.2." % (F["resp_window_v43_pct"],
                                                                                        F["resp_window_v5_pct"]),
        "The change is in the alerts, not in who was driving: from July, with every unit on 5.0.2, operators slow for "
        "about one critical alert in three, against nearly nine in ten in every month to May.",
        "Alert volumes and acknowledgements did not move, which is why the vendor's report shows nothing: operators still "
        "press acknowledge, they no longer brake.",
        "Not B: the North ramp junction has the most incidents, and more trucks ran the North waste route from June, but "
        "per 1,000 truck shifts in July to October the South pit ore route, which never passes the junction, went from "
        "%.1f to %.1f incidents, against %.1f to %.1f on the North waste route through it." % (
            F["rate_sore_2025"], F["rate_sore_2026"], F["rate_nwst_2025"], F["rate_nwst_2026"]),
        "Not A: the operators' attention did not fall across the board; the same crews slowed on 4.3 units in June.",
        "Not D or E: the fall in slowing came with the firmware on day shifts as on nights, and the crusher pad's share "
        "of incidents fell.",
    ]:
        d.add_paragraph(t, style="List Bullet")
    d.add_heading("Monthly incidents", level=2)
    d.add_picture(io.BytesIO(chart_png(F)), width=Cm(16))
    d.add_paragraph("Counts are register entries classified VI-COL or VI-SPI, by month of occurrence, Western Australian "
                    "time (HSE-TOR-026, 2.1).").runs[0].font.size = Pt(8.5)
    d.save(path)
    PP.normalize_ooxml(path, "Shari Jefferson", "Shari Jefferson", "2026-11-09T01:12:00Z", "2026-11-12T07:40:00Z",
                       title="Vehicle interaction programme for 2027", company=COMPANY)
    PP.scrub_docx(path, total_time=94, title="Vehicle interaction programme for 2027", company=COMPANY)


def workings_xlsx(path, F):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pit gate trips"
    ws.append(["Light-vehicle trips into the pits, July to October 2026"])
    ws["A1"].font = Font(bold=True)
    ws.append(["Month", "Trips", "Trips with no tag detected"])
    for m, name in ((7, "July 2026"), (8, "August 2026"), (9, "September 2026"), (10, "October 2026")):
        ws.append([name, F["trips_%02d" % m], F["trips_notag_%02d" % m]])
    ws.append([])
    ws.append(["One trip per entry through a pit gate. From 14 July the North gate's inner reader reads each vehicle a "
               "few seconds after the outer one, sometimes under a different plate; the pair is one trip."])
    ws.column_dimensions["A"].width = 18
    ws.column_dimensions["B"].width = 10
    ws.column_dimensions["C"].width = 26
    ws2 = wb.create_sheet("Ramp overspeed")
    ws2.append(["Haul truck times over the speed limit in force on the pit ramps, 2026"])
    ws2["A1"].font = Font(bold=True)
    ws2.append(["Ramp", "Month", "Times over the limit", "Peaked more than 5 km/h over"])
    for seg, name in (("NRP", "North pit ramp"), ("SRP", "South pit ramp")):
        for m, mn in ((7, "July 2026"), (8, "August 2026"), (9, "September 2026"), (10, "October 2026")):
            ws2.append([name, mn, F["os_%s_%02d" % (seg, m)], F["os5_%s_%02d" % (seg, m)]])
    ws2.append([])
    ws2.append(["Limits as in force on the day (haul road speed limits). A window that opens on the sample closing the "
                "truck's last window on that ramp, still over the limit, is the same run; each run at its highest speed."])
    for c, wd in zip("ABCD", (18, 10, 20, 28)):
        ws2.column_dimensions[c].width = wd
    wb.save(path)
    PP.normalize_ooxml(path, "Shari Jefferson", "Shari Jefferson", "2026-11-10T03:05:00Z", "2026-11-12T07:22:00Z",
                       excel=True, company=COMPANY)
