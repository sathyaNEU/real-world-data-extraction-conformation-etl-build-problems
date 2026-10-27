"""The goldens, from the cut pack only: dbt_skills_groups_2027_28.xlsx (each team: its 2026 assessed patients, whether
it gets a DBT skills group in 2027-28, the clinicians who can co-facilitate one on 1 April 2027, and the mean weeks its
patients on the service's DBT waiting list on 31 December 2026 had waited) and team_instability_2026.png (each team's
share against the 30 per cent line, the funded teams marked), with generator/figures.json and submission.md, every
figure in them emitted from the objects that computed it."""
from __future__ import annotations

import io
import json
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import asks as A
import calc as C
import common as K
import postprocess as PP

INK = "#1d2229"
INK2 = "#4b525c"
GRID = "#e3e6ea"
FUND = "#005eb8"
REST = "#b4bcc6"
WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}


class Out:
    pass


def compute(target):
    allp, reg, eps, pop, res = C.main_call(target)
    X = Out()
    X.pop, X.res = pop, res
    X.sh = C.shares(res, "W")
    X.funded = C.funded(X.sh)
    X.easy = C.funded(C.shares(res, "R1"))
    X.n_total = len(pop)
    X.order = sorted([c for c, _ in K.TEAMS], key=lambda c: (-X.sh[c]["share"], K.TEAM_NAME[c]))
    X.by_name = sorted([c for c, _ in K.TEAMS], key=lambda c: K.TEAM_NAME[c])
    AA = A.ask_a(target)
    X.A = {c: v[0] for c, v in AA.items()}
    X.A_w = {c: v[1] for c, v in AA.items()}
    B = A.ask_b(target)
    X.B_n = {c: v[0] for c, v in B.items()}
    X.B = {c: K.round_half_up(v[1], 1) for c, v in B.items()}
    X.B_raw = {c: v[1] for c, v in B.items()}
    return X


def names(codes):
    s = [K.TEAM_NAME[c] for c, _n in K.TEAMS if c in codes]
    return ", ".join(s[:-1]) + " and " + s[-1] if len(s) > 1 else s[0]


def chart_png(X):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    from matplotlib.patches import Patch
    for f in ("/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf",
              "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf"):
        font_manager.fontManager.addfont(f)
    plt.rcParams["font.family"] = "Carlito"
    plt.rcParams["svg.hashsalt"] = "task270"
    vals = [100 * X.sh[c]["share"] for c in X.order]
    fig = plt.figure(figsize=(8.6, 4.5), dpi=170)
    ax = fig.add_axes([0.075, 0.24, 0.905, 0.6])
    xs = np.arange(len(X.order))
    ax.bar(xs, vals, width=0.62, color=[FUND if c in X.funded else REST for c in X.order], zorder=3)
    ax.axhline(K.LINE, color=INK, lw=1.1, ls=(0, (5, 3)), zorder=4)
    ax.text(len(X.order) - 0.45, K.LINE + 0.8, "30% line", ha="right", va="bottom", fontsize=9.2, color=INK)
    ax.set_xticks(xs)
    ax.set_xticklabels([K.TEAM_NAME[c] for c in X.order], fontsize=9.2, color=INK2, rotation=30, ha="right")
    ax.set_ylabel("Patients with high emotional instability (%)", fontsize=9.2, color=INK2)
    ax.set_ylim(0, 60)
    ax.set_yticks([0, 10, 20, 30, 40, 50, 60])
    ax.grid(axis="y", color=GRID, lw=0.7, zorder=1)
    ax.tick_params(axis="y", labelsize=9.2, colors=INK2, length=0)
    ax.tick_params(axis="x", length=0)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("#9aa1aa")
    ax.legend(handles=[Patch(color=FUND, label="DBT skills group 2027-28"), Patch(color=REST, label="No group")],
              loc="upper right", bbox_to_anchor=(1.0, 1.0), frameon=False, fontsize=9, ncol=2)
    fig.text(0.075, 0.965, "%s teams have 30%% or more of their 2026 assessed patients at high emotional instability"
             % WORDS[len(X.funded)].capitalize(), fontsize=12, color=INK, fontweight="bold", va="top")
    fig.text(0.075, 0.91, "Share of each team's patients with instability of 2.0 or more, read over the three hours "
             "between the collaborative app's prompts", fontsize=9, color=INK2, va="top")
    fig.text(0.075, 0.025, "Source: trust mood app exports, January to December 2026; assessment fortnights register; "
             "care episodes. Teams as from 1 October 2026.", fontsize=8, color=INK2)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=170, metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_xlsx(path, X):
    wb = Workbook()
    thin = Side(style="thin", color="C9CED4")
    head_fill = PatternFill("solid", fgColor="E8EDF2")
    bold = Font(name="Calibri", bold=True)
    ws = wb.active
    ws.title = "Teams 2027-28"
    ws["A1"] = ("DBT skills groups 2027-28: %s of the eleven community mental health teams reach the 30 per cent line"
                % WORDS[len(X.funded)])
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws["A2"] = ("A group in each team where 30 per cent or more of the patients it assessed with the mood app in 2026 "
                "have high emotional instability as the collaborative's app will measure it. Teams as from "
                "1 October 2026.")
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:H2")
    ws.row_dimensions[2].height = 32
    cols = ["Team code", "Team", "Patients assessed in 2026", "DBT skills group 2027-28",
            "Clinicians able to co-facilitate on 1 April 2027", "Whole-time equivalent they hold in the team",
            "Patients on the DBT waiting list, 31 December 2026",
            "Mean weeks waited since the service received the referral"]
    for j, c in enumerate(cols, 1):
        cell = ws.cell(row=4, column=j, value=c)
        cell.font = bold
        cell.fill = head_fill
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        cell.border = Border(bottom=thin)
    ws.row_dimensions[4].height = 46
    r = 5
    for c in X.by_name:
        ws.cell(row=r, column=1, value=c)
        ws.cell(row=r, column=2, value=K.TEAM_NAME[c] + " CMHT")
        ws.cell(row=r, column=3, value=X.sh[c]["n"])
        ws.cell(row=r, column=4, value="Yes" if c in X.funded else "No")
        ws.cell(row=r, column=5, value=X.A[c])
        ws.cell(row=r, column=6, value=X.A_w[c]).number_format = "0.00"
        ws.cell(row=r, column=7, value=X.B_n[c])
        ws.cell(row=r, column=8, value=X.B[c]).number_format = "0.0"
        if c in X.funded:
            for j in (2, 4):
                ws.cell(row=r, column=j).font = Font(name="Calibri", bold=True, color="00468C")
        r += 1
    ws.cell(row=r, column=2, value="All teams").font = bold
    ws.cell(row=r, column=3, value=X.n_total)
    ws.cell(row=r, column=5, value=sum(X.A.values()))
    ws.cell(row=r, column=6, value=round(sum(X.A_w.values()), 2)).number_format = "0.00"
    ws.cell(row=r, column=7, value=sum(X.B_n.values()))
    for j in range(1, 9):
        ws.cell(row=r, column=j).border = Border(top=thin)
    notes = [
        "Patients assessed: each patient once, on their latest 2026 fortnight with at least 56 of its 112 prompts "
        "answered, in the team that held their care on the fortnight's first day.",
        "Co-facilitators: DBT programme operating standard 4.2 on the day the groups start, 1 April 2027; staff record "
        "at 4 January 2027 and learning records to December 2026.",
        "Waiting list: the referral module at 8 January 2027; a referral keyed in from the service's own database from "
        "22 June 2026 dated by the service's acknowledgement letter, as every referral is.",
    ]
    for i, t in enumerate(notes):
        cell = ws.cell(row=r + 2 + i, column=1, value=t)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        cell.font = Font(name="Calibri", size=9, color="4B525C")
        ws.merge_cells(start_row=r + 2 + i, start_column=1, end_row=r + 2 + i, end_column=8)
        ws.row_dimensions[r + 2 + i].height = 26
    for col, w in zip("ABCDEFGH", (10, 22, 12, 12, 16, 14, 16, 16)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"
    ws.print_title_rows = "4:4"
    wb.save(path)


def figures(X):
    F = {"funded": [K.TEAM_NAME[c] for c in X.funded], "easy_route": [K.TEAM_NAME[c] for c in X.easy],
         "patients_assessed": X.n_total, "funded_count": len(X.funded),
         "parameters": {"line_pct": 30, "high": "2.0", "prompts": K.PROMPTS, "completed_prompts": K.COMPLETE,
                        "trust_block_minutes": K.BLOCK_MIN, "collab_interval_hours": 3, "window_hours": ["2.5", "3.5"],
                        "wte": "0.4", "dbt_standard": ["2.2", "3.1", "3.2", "4.2"], "paper_section": 2, "standard_sections": ["2.1", "3.1",
                                                                                                        "3.2", "3.3"]}}
    for c, _n in K.TEAMS:
        F["assessed_" + c] = X.sh[c]["n"]
        F["cofacilitators_" + c] = X.A[c]
        F["wte_" + c] = "%.2f" % X.A_w[c]
        F["mean_weeks_" + c] = "%.1f" % X.B[c]
        F["waiting_" + c] = X.B_n[c]
        F["group_" + c] = "Yes" if c in X.funded else "No"
    return F


def writeup(X):
    """submission.md: the five blocks, every figure from X."""
    L = []
    added = [c for c in X.funded if c not in X.easy]
    L.append("## Tags\n")
    L.append("**Domain:** Psychology & Behavioral Science (experience sampling and intensive longitudinal analysis: "
             "each community team's share of its 2026 assessed patients with high emotional instability).")
    L.append("**Analytical objective:** Descriptive & Distribution Analysis.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Fund a DBT skills group in 2027-28 in %s, and in none of the other %s teams.**"
             % (names(X.funded), WORDS[11 - len(X.funded)]))
    L.append("Read over the three hours between the collaborative app's prompts, 30 per cent or more of each of these "
             "teams' 2026 assessed patients reach 2.0. Not %s alone, which the change between the trust app's "
             "adjacent prompts gives: those prompts sat about 90 minutes apart and negative affect moves further in "
             "three hours, so that reading leaves %s under the line." % (names(X.easy), names(added)))
    L.append("")
    L.append("## 2. Critical Components\n")
    L.append("1. Patients counted: **%s**, each once on their latest completed 2026 fortnight, in the team holding "
             "their care on its first day, Haddersley North and South as one team." % format(X.n_total, ","))
    L.append("2. The trust app's adjacent prompts sat about **%d minutes** apart against the collaborative's three "
             "hours, and the change in negative affect between two same-day ratings grows with the time between "
             "them." % K.BLOCK_MIN)
    L.append("3. Each patient's emotional instability is read at three hours, the interval between the collaborative "
             "app's prompts, before the **2.0** line is applied.")
    L.append("")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Read both app exports on one 0 to 10 scale (version 3's sliders divided by ten, version 4's UTC "
             "times put in UK time, its resent rows dropped), joined app codes to patients through %s, and took each "
             "patient's latest 2026 fortnight in %s with at least %d of its %d prompts answered (the committee paper, "
             "section 2), in the team %s shows on its first day: %s patients."
             % (K.F_ENROL, K.F_REGISTER, K.COMPLETE, K.PROMPTS, K.F_EPISODES, format(X.n_total, ",")))
    L.append("2. Took negative affect at each answered prompt as the mean of its four items (the collaborative's "
             "standard, 3.1).")
    L.append("3. Measured each patient's emotional instability over the three hours between the collaborative app's "
             "prompts (standard 2.1 and 3.2) as the root mean square change in negative affect between their "
             "same-day ratings 2.5 to 3.5 hours apart.")
    L.append("4. Counted each team's patients at 2.0 or more (standard 3.3): %s reach 30 per cent or more."
             % names(X.funded))
    L.append("5. Counted each team's clinicians whose learning record, under their own or their previous employee "
             "number, holds PTD-301, EXT-0412 or PTD-114 completed before 1 April 2025 (the four-day course that code "
             "carried until the catalogue rebuild, as the 2024-25 annual report lists it), with a non-administrative "
             "assignment in the team of 0.4 WTE or more on 1 April 2027 and no leaving date on or before 16 September "
             "2027 (DBT programme operating standard 4.2), and summed those assignments' whole-time equivalent.")
    L.append("6. Took each patient on the DBT waiting list on 31 December 2026 in %s (accepted for DBT, added by then "
             "and not removed by then), dated each referral by the service's acknowledgement letter in %s (DBT "
             "programme operating standard 2.2), the latest for the patient on or before the module's received date "
             "through %s, which replaces the date the module stamped on the referrals keyed in from the service's "
             "database from 22 June 2026, and averaged the days to 31 December over seven by the team holding the "
             "patient's care on 31 December." % (K.F_MODULE, K.F_LETTERS, K.F_INDEX))
    L.append("7. The committee funds a DBT skills group in %s." % names(X.funded))
    L.append("")
    L.append("## 4. Deliverable Answers\n")
    L.append("### %s\n" % K.X_GOLD)
    L.append("1. Teams that get a DBT skills group in 2027-28: %s; the other %s teams do not."
             % (names(X.funded), WORDS[11 - len(X.funded)]))
    L.append("2. Each team, whether it gets a group, the clinicians who can co-facilitate one on 1 April 2027 and the "
             "whole-time equivalent they hold in the team (two decimals), and the mean weeks the patients in its care "
             "on 31 December 2026 who were then on the DBT waiting list had waited since the service received their "
             "referral (one decimal):")
    for c in X.by_name:
        L.append("   - %s: %s, %d clinician%s holding %.2f WTE, %.1f weeks"
                 % (K.TEAM_NAME[c], "group" if c in X.funded else "no group", X.A[c], "" if X.A[c] == 1 else "s",
                    X.A_w[c], X.B[c]))
    L.append("")
    L.append("### %s\n" % K.P_GOLD)
    L.append("3. Bar chart of each team's share of its 2026 assessed patients with high emotional instability against "
             "the 30 per cent line, the five funded teams in blue.")
    return "\n".join(L) + "\n"


def main(target=K.TARGET, golden=K.GOLDEN, figs=os.path.join(K.HERE, "figures.json"),
         sub=os.path.join(K.TASK, "submission.md")):
    os.makedirs(golden, exist_ok=True)
    X = compute(target)
    png = chart_png(X)
    with open(os.path.join(golden, K.P_GOLD), "wb") as fh:
        fh.write(png)
    write_xlsx(os.path.join(golden, K.X_GOLD), X)
    PP.normalize_ooxml(os.path.join(golden, K.X_GOLD), K.PEOPLE["ccio"], K.PEOPLE["ccio"], "2027-01-18T10:12:00Z",
                       "2027-01-20T16:31:00Z", excel=True, company=K.TRUST)
    with open(figs, "w") as fh:
        json.dump(figures(X), fh, indent=1, sort_keys=True)
    with open(sub, "w", encoding="utf-8") as fh:
        fh.write(writeup(X))
    return X


if __name__ == "__main__":
    main()
