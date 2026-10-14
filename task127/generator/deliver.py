"""The goldens: the reserve memo (bi_reserve_ye2026.md), the claimant-feature counts (bi_claim_counts_ye2026.csv) and
the chart (bi_unpaid_ye2026.png), every figure computed from the pack by analysis.py."""
from __future__ import annotations

import numpy as np

import analysis as A
import common as K

CARRY_UNIT = 25e6


def compute(target):
    m = A.main_call(target)
    b = m["b"]
    D = m["D"]
    clos = A.closure_rows(D, ages=(8, 12))
    act, exp = A.actual_vs_expected(m["P"])
    fs_naive, fs_trend, trend = A.frequency_severity(b, m["n_ult"], m["P"])
    indicated = float(m["bs"].sum())
    carried = A.round_to(indicated, CARRY_UNIT)
    booked = m["booked"]
    counts = A.counts_by_year(b)
    led = A.ledger_quarters(target)
    by_year = A.by_year(m["bs"])
    paid_year = m["paid_by_year"]
    fig = {
        "call": "Carry $%d million for unpaid bodily injury loss at 31 December 2026, $%.1f million more than the "
                "$%.1f million booked." % (carried / 1e6, (carried - booked) / 1e6, booked / 1e6),
        "carried_musd": carried / 1e6,
        "booked_musd": round(booked / 1e6, 1),
        "gap_musd": round((carried - booked) / 1e6, 1),
        "indicated_musd": round(indicated / 1e6, 1),
        "chain_ladder_musd": round(float(m["cl"].sum()) / 1e6, 1),
        "chain_ladder_carry_musd": A.round_to(float(m["cl"].sum()), CARRY_UNIT) / 1e6,
        "paid_to_date_musd": round(m["paid_to_date"] / 1e6, 1),
        "closed_share_8q_history_pct": round(100 * clos[8][0], 1),
        "closed_share_8q_latest_pct": round(100 * clos[8][1], 1),
        "closed_share_8q_latest_aq": clos[8][2],
        "closed_share_12q_history_pct": round(100 * clos[12][0], 1),
        "closed_share_12q_latest_pct": round(100 * clos[12][1], 1),
        "closed_share_12q_latest_aq": clos[12][2],
        "unpaid_by_year_musd": {str(y): round(v / 1e6, 1) for y, v in by_year.items()},
        "paid_by_year_musd": {str(y): round(v / 1e6, 1) for y, v in paid_year.items()},
        "counts": {str(y): v for y, v in counts.items()},
        "ledger": {"Q%d" % q: v for q, v in led.items()},
        "rungs_musd": {"chain_ladder": round(float(m["cl"].sum()) / 1e6, 1),
                       "latest_4": round(float(m["cl_last4"].sum()) / 1e6, 1),
                       "latest_8": round(float(m["cl_last8"].sum()) / 1e6, 1),
                       "latest_12": round(float(m["cl_last12"].sum()) / 1e6, 1),
                       "fs_open_at_closed_average": round(fs_naive / 1e6, 1),
                       "fs_trended_2017_2019": round(fs_trend / 1e6, 1),
                       "restated_linear": round(indicated / 1e6, 1),
                       "restated_exponential": round(float(m["bs_exp"].sum()) / 1e6, 1),
                       "restated_reported_base": round(float(m["bs_rep"].sum()) / 1e6, 1),
                       "restated_exponential_reported": round(float(m["bs_exp_rep"].sum()) / 1e6, 1),
                       "restated_simple_average": round(float(m["bs_simple"].sum()) / 1e6, 1),
                       "restated_latest_12": round(float(m["bs_last12"].sum()) / 1e6, 1)},
        "actual_vs_expected": round(act / exp, 3),
        "accident_quarters": K.N_AQ,
        "first_accident_year": K.FIRST_AQ[0],
        "carry_unit_musd": int(CARRY_UNIT / 1e6),
        "ledger_account": 5311,
        "fs_trend_pct": round(100 * trend, 1),
    }
    return dict(figures=fig, m=m)


def _m(x):
    return "$%.1f million" % x


def write_memo(path, res):
    f = res["figures"]
    led = f["ledger"]
    lines = [
        "# Motor bodily injury: unpaid loss at 31 December 2026",
        "",
        "Ninebark Mutual, private passenger auto liability, bodily injury, gross of reinsurance, undiscounted, "
        "excluding adjusting expenses. Valuation 31 December 2026 (Central time), on the claims extracts run "
        "6 January 2027.",
        "",
        "## The figure",
        "",
        "**Carry $%d million for unpaid bodily injury loss at 31 December 2026: $%.1f million more than the "
        "$%.1f million finance has booked.**" % (f["carried_musd"], f["gap_musd"], f["booked_musd"]),
        "",
        "The estimate is %s, rounded to the nearest $25 million. It is the paid development of the 40 accident "
        "quarters from 2017 Q1, with each quarter's history first restated to the share of its ultimate claimant "
        "features that the latest diagonal had closed at the same age, then developed with volume-weighted factors "
        "over all accident quarters to age 40." % _m(f["indicated_musd"]),
        "",
        "## Why the history is restated",
        "",
        "Bodily injury pays almost entirely at settlement, so a paid triangle develops as fast as claims close. Since "
        "the claims platform went live in July 2024 the book has been closing a smaller share of its claimant "
        "features at each age than it used to: at eight quarters %.1f per cent of ultimate features were closed in "
        "the 2018 to 2020 accident quarters against %.1f per cent for %s, and at twelve quarters %.1f per cent "
        "against %.1f per cent for %s. Paid development measured on the earlier pace treats the slower closings as "
        "smaller claims: developed unrestated, the same triangle gives %s, which would have released money we "
        "will pay." % (f["closed_share_8q_history_pct"], f["closed_share_8q_latest_pct"], f["closed_share_8q_latest_aq"],
                       f["closed_share_12q_history_pct"], f["closed_share_12q_latest_pct"],
                       f["closed_share_12q_latest_aq"], _m(f["chain_ladder_musd"])),
        "",
        "| Accident year | Paid to date ($ million) | Unpaid carried ($ million) |",
        "|---|---:|---:|",
    ]
    for y in range(2017, 2027):
        lines.append("| %d | %.1f | %.1f |" % (y, f["paid_by_year_musd"][str(y)], f["unpaid_by_year_musd"][str(y)]))
    lines.append("| All | %.1f | %.1f |" % (f["paid_to_date_musd"], f["indicated_musd"]))
    lines += [
        "",
        "## Paid losses against the ledger, 2026",
        "",
        "Account 5311 tied to the claims platform's payments, quarter by quarter: what the ledger booked, the part "
        "that was claims payments issued in an earlier quarter (checks the nightly feed posts the morning after, and "
        "wires Treasury books in the month after their bank value date), and the part that was not claims payments "
        "at all.",
        "",
        "| Quarter | Ledger booked ($) | Claims payments issued in an earlier quarter ($) | Not claims payments ($) |",
        "|---|---:|---:|---:|",
    ]
    for q in ("Q1", "Q2", "Q3", "Q4"):
        lines.append("| %s 2026 | %s | %s | %s |" % (q, "{:,.2f}".format(led[q]["booked"]),
                                                    "{:,.2f}".format(led[q]["earlier"]),
                                                    "{:,.2f}".format(led[q]["other"])))
    lines += [
        "",
        "Not claims payments: a December 2025 property damage wire Treasury booked to 5311 (reclassed in April), and "
        "the claims feed's 13 August batch posted a second time on 15 August (reversed in October).",
        "",
        "The claimant-feature counts by accident year are in bi_claim_counts_ye2026.csv; the chart is "
        "bi_unpaid_ye2026.png.",
        "",
    ]
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))


def write_counts(path, res):
    c = res["figures"]["counts"]
    rows = ["accident_year,closed_with_loss_payment,closed_without_loss_payment"]
    for y in range(2017, 2027):
        rows.append("%d,%d,%d" % (y, c[str(y)]["with_payment"], c[str(y)]["without_payment"]))
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(rows) + "\n")


def write_chart(path, res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    f = res["figures"]
    years = list(range(2017, 2027))
    unpaid = [f["unpaid_by_year_musd"][str(y)] for y in years]
    fig, ax = plt.subplots(figsize=(8.6, 4.8), dpi=110)
    bars = ax.bar([str(y) for y in years], unpaid, color="#2f5d3a", width=0.62)
    for b_, v in zip(bars, unpaid):
        if v >= 1.0:
            ax.text(b_.get_x() + b_.get_width() / 2, v + 2.0, "%.0f" % v, ha="center", va="bottom", fontsize=8.5,
                    color="#1b1f1d")
    ax.set_ylabel("Unpaid loss carried ($ million)")
    ax.set_xlabel("Accident year")
    ax.set_title("Motor bodily injury: unpaid loss by accident year at 31 December 2026", fontsize=11)
    ax.text(0.02, 0.95, "Carried $%d million\nBooked $%.1f million" % (f["carried_musd"], f["booked_musd"]),
            transform=ax.transAxes, va="top", fontsize=9.5,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#9aa39d"))
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_ylim(0, max(unpaid) * 1.15)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None}, pil_kwargs={"optimize": False})
    plt.close(fig)
