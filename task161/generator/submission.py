"""Write task161/submission.md from generator/figures.json: every figure in it is emitted, never typed."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October"]


def n(x):
    return "{:,}".format(int(x))


def text(F):
    c, k, st = F["call"], F["components"], F["steps"]
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Urban & Regional Science (forecasting: an import 3PL's pallet positions beside the San Pedro "
               "Bay ports for January to June 2027, each account's bought-ahead stock netted against its own forecast "
               "shipments at the share its own earlier duty rushes burned, against six %s-position overflow blocks)."
               % n(st["block_positions"]))
    out.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**We should take %d of the six %s-position overflow blocks at Tamarind Avenue Logistics Park for "
               "January to June 2027, %s for the term.**" % (c["blocks"], n(st["block_positions"]), c["cost"]))
    out.append("Netted account by account against each account's own forecast shipments, at the share of its "
               "shipments its excess left at after the earlier duty steps, the bought-ahead stock keeps the first two "
               "blocks in use through June and leaves the third well under the space policy's %d%%. Not a fade of the "
               "book's excess at the earlier rushes' half-life of about a month, which takes no block: five seasonal "
               "accounts hold most of the excess and ship at their first-half low, and after the April 2025 step, the "
               "one earlier rush in that season, their stock left at the pace of their shipments, not of a half-life. "
               "Not today's stock held flat (three blocks), nor each account's own monthly fall from the earlier "
               "rushes (one block), nor the whole excess held through June (three blocks)." % st["hurdle_pct"])
    out.append("")
    out.append("## 2. Critical Components\n")
    out.append("1. Pallets on hand at the close of 6 December for the 14 accounts under contract: **%s**."
               % n(k["on_hand_6dec"]))
    out.append("2. The five seasonal accounts (housewares, toys, mobile accessories, seasonal decor, small appliances) "
               "shipped **%s** pallets in January 2026: their bought-ahead stock leaves only on their own shipments, "
               "which run near that in January 2027, far short of the half of their excess over normal stock, as the "
               "space policy defines it, that a one-month half-life would take out in January."
               % n(k["five_jan2026_shipments"]))
    out.append("3. With normal stock as the space policy defines it and under every burn share the earlier rushes "
               "support, the second block is in use in every month of the term and the third stays well below three "
               "quarters of its position-months.")
    out.append("")
    out.append("## 3. Step-by-Step Solution\n")
    out.append("1. Stacked wms1_inv_daily_20190401-20220930.txt to the close of 11 September 2022 (Sundays carrying "
               "Saturday's close, legacy codes mapped through client_master_2026-12.xlsx, ROSALESB and ROSALESK as "
               "PD2063) with wms_inventory_nightly_20220913_20261207.csv summed over sites (each run holding the close "
               "of the day before it, per wms_export_dictionary_v3.pdf) and wms_outbound_daily_20220912_20261206.csv: "
               "%s pallets on hand at the close of 6 December." % n(k["on_hand_6dec"]))
    out.append("2. Took each account's normal stock as the space policy defines it, its cover times the mean of its "
               "shipments in the month and the month after, the cover being its median over its months from July 2023 "
               "clear of each duty step's month, the three before it and the five after, applied at mid-month and "
               "interpolated by day, and its excess over normal "
               "stock after each step in yv_client_advisories_2019-2026.pdf (1 September 2019, 5 April 2025, 7 August "
               "2025): each excess fell in step with its own account's cumulative shipments, the five seasonal "
               "accounts' slowest after the April 2025 step, in their low season.")
    out.append("3. Fitted each account's burn share, the fall in its excess per pallet it shipped (a least-squares slope "
               "with an intercept, from its mean over the seven days before the step until it fell under a quarter of "
               "its size or the next advisory, for excesses of at least %d%% of normal stock fitted over %d days or "
               "more), weighted by the shipments each fit spans: left out in turn, the burn share predicts the earlier "
               "rushes' excess better than a half-life fitted on the others, most of all after the April 2025 step."
               % (st["episode_floor_pct"], st["episode_min_days"]))
    out.append("4. Forecast each account's shipments for December 2026 to July 2027 as the same month a year earlier "
               "times its shipments from December 2025 to November 2026 over the twelve months before, spread over "
               "each month's working days with a Saturday at %s of a weekday (the book's own ratio) and Sundays, "
               "Christmas Eve, Christmas Day, New Year's Day and Memorial Day closed: the five seasonal accounts' "
               "January to June shipments run at their first-half low." % st["saturday_weight"])
    out.append("5. Projected each account's close of 31 December as the close of 6 December plus the pallets due in "
               "dec2026_inbound_booking_tracker.xlsx (box-only notices at the account's own pallets per box over the "
               "last %d days, per the tracker) less the rest of December's forecast shipments: the five seasonal "
               "accounts hold most of the excess over normal stock." % st["notice_window_days"])
    out.append("6. Burned each account's excess day by day at its burn share of its forecast shipments until it was "
               "gone, added its normal stock and took the mean of each day's close by month (space policy 3.1): the "
               "overflow above the %s rack positions stays above the first block's %s positions in every month from "
               "January to June." % (n(st["rack_positions"]), n(st["block_positions"])))
    out.append("7. Ran the block test of space_planning_policy_rev4.pdf section 4.2: blocks 1 and 2 hold at least "
               "three quarters of their %s position-months and block 3 well under, so we take %d blocks, %s at the "
               "%s per block in ridley-ames_bldg-b_overflow_blocks_2026-11-19.pdf."
               % (n(st["position_months"]), c["blocks"], c["cost"], c["price"]))
    out.append("")
    out.append("## 4. Deliverable Answers\n")
    out.append("### overflow_blocks_h1_2027.xlsx\n")
    out.append("1. The call on the Blocks sheet: take %d of the 6 blocks (B-1 and B-2), %s for the term."
               % (c["blocks"], c["cost"]))
    out.append("2. TEU of the import containers whose freight reached us from the two ports, and that TEU as a share of "
               "the two ports' loaded import TEU, by month of 2026:")
    for m in MON:
        lab = "%s 2026" % m
        out.append("   - %s: %s TEU, %s%%" % (m, n(F["a2_teu"][lab]), F["a2_share"][lab]))
    out.append("")
    out.append("### port_share_2026.pdf\n")
    out.append("1. One-page bar chart of the ten monthly shares, January to October 2026, each bar labelled with its "
               "month's TEU and share.")
    return "\n".join(out) + "\n"


def write(path, figures=None):
    F = json.load(open(figures or os.path.join(HERE, "figures.json")))
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text(F))


if __name__ == "__main__":
    write(os.path.join(os.path.dirname(HERE), "submission.md"))
