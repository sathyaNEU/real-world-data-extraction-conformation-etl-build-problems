"""task252 goldens: the return workbook ammonia_channel_offsets_2027Q4.xlsx and the chart
ammonia_channel_offsets_2027Q4.png, written from figures.json."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import params as P
import postprocess

XLSX = "ammonia_channel_offsets_2027Q4.xlsx"
PNG = "ammonia_channel_offsets_2027Q4.png"
HEAD = PatternFill("solid", fgColor="DCE6EC")
FLAG = PatternFill("solid", fgColor="F6DED6")


def _head(ws, row, cols):
    for j, h in enumerate(cols, 1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")


def _widths(ws, ws_w):
    for j, w in enumerate(ws_w, 1):
        ws.column_dimensions[get_column_letter(j)].width = w


def workbook(path, fig):
    wb = Workbook()
    ws = wb.active
    ws.title = "Return Q4 2027"
    ws["A1"] = "Six treated-water ammonia channels flagged for the fourth quarter of 2027"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Online monitoring return, WQ-DS-04 section 7. Prepared by Water Quality Compliance, %s, "
                "January 2028." % P.ORG)
    ws["A2"].font = Font(italic=True, size=9)
    _head(ws, 4, ["Item (a): flagged channel", "Plant", "Water", "Analyser", "Reads"])
    r = 5
    for ch in fig["flagged"]:
        code, sp = ch.split("-")
        water = {"FI1": "Filtered", "FW1": "Final"}[sp]
        ws.append([ch, P.NAME[code], water, P.tag(code), "High" if fig["offsets"][ch] > 0 else "Low"])
        r += 1
    r += 1
    _head(ws, r, ["Plant", "Item (b): filtered and final water samples analysed more than 24 h after collection",
                  "Item (c): hours at the fixed chlorine dose, filtered water ammonia reading not available"])
    for c in P.CODES:
        r += 1
        ws.cell(row=r, column=1, value=P.NAME[c])
        ws.cell(row=r, column=2, value=fig["ask_a"][P.NAME[c]])
        ws.cell(row=r, column=3, value=fig["ask_b"][P.NAME[c]]).number_format = "0.0"
    ws.row_dimensions[r - 8].height = 44
    _widths(ws, [26, 30, 36, 16, 10])
    ws.freeze_panes = "A5"

    ws = wb.create_sheet("Channels")
    _head(ws, 1, ["Channel", "Plant", "Water", "Carryover (mg/L as N)", "Calibration error at the channel's level "
                  "(mg/L as N)", "Sample line (mg/L as N)", "Offset (mg/L as N)", "Flagged"])
    for ch in sorted(fig["offsets"]):
        code, sp = ch.split("-")
        cal = fig["offsets"][ch] - fig["carry"][ch] - fig["line"][ch]
        ws.append([ch, P.NAME[code], {"FI1": "Filtered", "FW1": "Final"}[sp], fig["carry"][ch], round(cal, 4),
                   fig["line"][ch], fig["offsets"][ch], "Yes" if ch in fig["flagged"] else "No"])
        if ch in fig["flagged"]:
            for cell in ws[ws.max_row]:
                cell.fill = FLAG
    for row in ws.iter_rows(min_row=2, min_col=4, max_col=7):
        for cell in row:
            cell.number_format = "+0.000;-0.000;0.000"
    _widths(ws, [11, 13, 10, 14, 22, 14, 12, 9])
    ws.freeze_panes = "A2"

    ws = wb.create_sheet("Analysers")
    _head(ws, 1, ["Analyser", "Plant", "Carryover from the port before", "Carryover from two ports before",
                  "Check mean, Q4 (mg/L as N)", "Calibration error", "Filtered sample line"])
    form = {"zero": "Zero error: the same shortfall at every level", "span": "Span error: shortfall in proportion",
            "none": "Within the checks' scatter"}
    for c in P.CODES:
        a = fig["analysers"][c]
        ch = "%s-FI1" % c
        line = ("Takes %s of the ammonia when grown; rises %.3f to %.3f at each monthly flush (six hours after, two "
                "days before)" % (
            fig["line_share_words"][ch], fig["line_step_low"][ch], fig["line_step_high"][ch])
            if ch in fig["line_share"] else "No change at the flushes")
        ws.append([P.tag(c), P.NAME[c], a["k1"] if c in ("BRN", "DUN", "ELS", "GAR", "HOL") else "under 0.01",
                   a["k2"] if c in ("BRN", "DUN", "ELS", "GAR", "HOL") else "under 0.01", a["check_mean"],
                   form[a["form"]], line])
    for row in ws.iter_rows(min_row=2, min_col=3, max_col=4):
        for cell in row:
            if isinstance(cell.value, float):
                cell.number_format = "0.000"
    for row in ws.iter_rows(min_row=2, min_col=5, max_col=5):
        for cell in row:
            cell.number_format = "0.0000"
    _widths(ws, [15, 13, 16, 16, 15, 44, 70])
    ws.freeze_panes = "A2"

    ws = wb.create_sheet("Notes")
    notes = [
        "Offset: WQ-DS-04 section 3, the mean over the channel's readings held in the historian with quality G for the "
        "quarter (New Zealand time) of the reading less the ammonia in the water at its sample point; flagged beyond "
        "0.005 mg/L as N either way (section 4).",
        "Carryover: the cell does not empty between ports, so each reading is a mix of its own water with shares of the "
        "two samples before it. The shares are the analyser's, fitted once on both treated ports' readings against the "
        "readings of the two slots before them, each port with its own level and its own response to the raw water "
        "2 to 8 hours earlier; the check cycles count as the cell's content. A slot the historian filled from the "
        "outstation after a failed poll counts by its G row.",
        "Calibration: Holmedale and Calderwood read about 8 per cent low on the 0.100 standard. Against the raw grabs, "
        "with the raw port's own carryover from the treated ports ahead of it taken out, Holmedale reads the same 0.008 "
        "low (a zero error, carried whole to its treated channels) and Calderwood about 8 per cent low (a span error, "
        "about 0.001 at its treated levels).",
        "Sample lines: the check standard enters at the check port, after the sample lines, and the laboratory's grabs "
        "come from the taps, so neither sees what a line takes. With carryover and calibration taken out, Calderwood's "
        "and Holmedale's filtered readings rise at every monthly line flush in the register's planned maintenance log "
        "and fall back over the following days as the unchlorinated line's film grows again (fitted on the days since "
        "the flush with the raw water's lagged response, regrowth time %.1f days); averaged over the quarter's G "
        "readings their lines read %.3f and %.3f below the water. No other channel moves at the flushes." % (
            fig["line_tau_days"], fig["line_loss_mean"]["CAL-FI1"], fig["line_loss_mean"]["HOL-FI1"]),
        "Item (b): the laboratory's analysis stamps run behind its reception and release times (some runs are "
        "stamped up to %d minutes before reception logged their bottles, and no result is released within %d minutes "
        "of its stamp), so the stamps move forward an hour, the analyser keeping standard time against the daylight "
        "time of the other clocks; any shift in that range counts the same. October's treated samples are under the "
        "laboratory's old codes (its notice of 28 October 2027). Each bottle counts once: the 7 December round's "
        "treated bottles appear twice in the export, logged again on unpacking under the courier docket's pickup time, "
        "with the same point, analysis stamp, result and release." % (fig["clock_lo"], fig["clock_hi"]),
        "Item (c): the PLC reads the analyser directly, so a slot the historian lost, filled after a failed poll, or "
        "lost in a run of failed polls at every port that nothing filled, no technician's check followed and the "
        "analyser's port sequence ran through unbroken (the telemetry's, one a plant in November) was good at the "
        "plant. A run after which the sequence starts again at the raw water port is the analyser's own stop (each "
        "analyser once, on the storm night of 26 to 27 October or 3 to 4 December, until the morning reset), and a "
        "filtered port's own run of F rows, with the other ports read between them, is a reading that never reached "
        "the PLC (once at each plant); both count with the analyser's faults and its check cycles, each gap beyond "
        "the two-hour hold.",
    ]
    for i, n in enumerate(notes, 1):
        ws.cell(row=i, column=1, value=n).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[i].height = 58
    ws.column_dimensions["A"].width = 120
    wb.save(path)
    postprocess.scrub(path, P.ORG, "2028-01-19")
    postprocess.finish_office(path, "2028-01-17T21:04:00Z", "2028-01-19T02:37:00Z", P.ORG)


def chart(path, fig):
    off = fig["offsets"]
    plants = P.CODES
    fig_, ax = plt.subplots(figsize=(9.2, 5.4), dpi=150)
    ax.axhspan(-P.THRESH, P.THRESH, color="#E9EEF2", zorder=0)
    ax.axhline(P.THRESH, color="#7A8A96", lw=0.9, ls="--", zorder=1)
    ax.axhline(-P.THRESH, color="#7A8A96", lw=0.9, ls="--", zorder=1)
    ax.axhline(0, color="#B5BEC6", lw=0.8, zorder=1)
    for i, c in enumerate(plants):
        for dx, sp, mk in ((-0.14, "FI1", "o"), (0.14, "FW1", "s")):
            ch = "%s-%s" % (c, sp)
            v = off[ch]
            hot = ch in fig["flagged"]
            ax.plot([i + dx], [v], marker=mk, ms=8, color="#B23A1E" if hot else "#5C7080",
                    mfc="#B23A1E" if hot else "white", mew=1.6, zorder=3)
            if hot:
                ax.annotate(ch, (i + dx, v), xytext=(4, 6), textcoords="offset points", fontsize=8, color="#7A2614")
    ax.annotate("HOL-FI1: carryover cancelled by\nits filtered line's loss", (6.86, off["HOL-FI1"]), xytext=(4.95, -0.0086),
                fontsize=8, color="#3A4A56", arrowprops=dict(arrowstyle="-", color="#7A8A96", lw=0.8))
    ax.annotate("HOL-FW1: carryover cancelled\nby Holmedale's zero error", (7.14, off["HOL-FW1"]), xytext=(5.75, -0.0133),
                fontsize=8, color="#3A4A56", arrowprops=dict(arrowstyle="-", color="#7A8A96", lw=0.8))
    ax.text(7.45, P.THRESH + 0.0004, "+0.005", fontsize=8, color="#5C6B76", ha="right")
    ax.text(7.45, -P.THRESH - 0.0013, "-0.005", fontsize=8, color="#5C6B76", ha="right")
    ax.set_xticks(range(len(plants)))
    ax.set_xticklabels([P.NAME[c] for c in plants], fontsize=9)
    ax.set_ylabel("Offset, Q4 2027 (mg/L as N)", fontsize=9)
    ax.set_ylim(-0.0155, 0.032)
    ax.tick_params(axis="y", labelsize=8.5)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%.3f"))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    h1 = plt.Line2D([], [], marker="o", ls="", color="#5C7080", mfc="white", label="Filtered water (FI1)")
    h2 = plt.Line2D([], [], marker="s", ls="", color="#5C7080", mfc="white", label="Final water (FW1)")
    h3 = plt.Line2D([], [], marker="o", ls="", color="#B23A1E", mfc="#B23A1E", label="Flagged (beyond 0.005)")
    ax.legend(handles=[h1, h2, h3], loc="upper left", fontsize=8, frameon=False)
    ax.set_title("Six of 16 treated-water ammonia channels read more than 0.005 mg/L as N off, Q4 2027",
                 fontsize=11, loc="left")
    fig_.text(0.01, 0.012, "Source: historian readings, monthly checks, laboratory grabs and the planned maintenance log, "
              "Q4 2027.\nOffset = sequencer carryover + the analyser's calibration error at the channel's level + the "
              "sample line's loss.", fontsize=7, color="#5C6B76", linespacing=1.4)
    fig_.tight_layout(rect=(0, 0.05, 1, 1))
    fig_.savefig(path, metadata={"Software": None})
    plt.close(fig_)


def write(folder, fig):
    os.makedirs(folder, exist_ok=True)
    workbook(os.path.join(folder, XLSX), fig)
    chart(os.path.join(folder, PNG), fig)
