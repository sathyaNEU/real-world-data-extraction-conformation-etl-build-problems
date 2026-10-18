"""Write task161/submission.md from generator/figures.json: every figure in it is emitted, never typed."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October"]
BUILDING = [("CAR1", "Del Amo, Carson"), ("RDZ1", "Alondra, Rancho Dominguez"), ("WIL1", "Anaheim Street, Wilmington"),
            ("CMP1", "Artesia, Compton")]


def n(x):
    return "{:,}".format(int(x))


def text(F):
    c, k, st, rv = F["call"], F["components"], F["steps"], F["rivals"]
    u = k["block_use_pct"]
    ov = [k["overflow"]["%s 2027" % m] for m in MON[:6]]
    shares = sorted(a["burn_share"] for a in F["accounts"].values())
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
    out.append("Netted account by account against each account's own forecast shipments, the stock runs %s to %s "
               "positions above our %s rack positions every month, so the second block would hold %.1f%% of its %s "
               "position-months against the space policy's %d%% and the third %.1f%%. Not fading the book's excess at "
               "the %.2f-month half-life the earlier rushes showed, which leaves overflow only in January (block 1 "
               "used %d%%) and takes no block: five seasonal accounts that bought for their whole 2027 season hold %s "
               "of the %s pallets of excess and ship little before summer. Not burning the book's excess at the book's "
               "share of its shipments (%.3f of each pallet shipped), which takes no block, nor each account's own "
               "monthly fall from the earlier rushes (one block), nor holding the whole excess through June (three "
               "blocks)." % (n(k["overflow_min"]), n(k["overflow_max"]), n(st["rack_positions"]), u[1],
                             n(st["position_months"]), st["hurdle_pct"], u[2], rv["fade_half_life_months"],
                             rv["fade_block1_pct"], n(k["seasonal_excess_31dec"]), n(k["excess_31dec"]),
                             rv["book_burn_share"]))
    out.append("")
    out.append("## 2. Critical Components\n")
    out.append("1. Pallets on hand at the close of 6 December for the accounts under contract: **%s**."
               % n(k["on_hand_6dec"]))
    out.append("2. Pallets over normal stock at 31 December: **%s**, of which the five seasonal accounts hold **%s**."
               % (n(k["excess_31dec"]), n(k["seasonal_excess_31dec"])))
    out.append("3. Pallets over normal stock still on hand at 30 June 2027: **%s**." % n(k["excess_30jun"]))
    out.append("4. Block uses over the term: block 1 **%.1f%%**, block 2 **%.1f%%**, block 3 **%.1f%%**." % (u[0], u[1],
                                                                                                         u[2]))
    out.append("")
    out.append("## 3. Step-by-Step Solution\n")
    out.append("1. Stacked wms1_inv_daily_20190401-20220930.txt to the close of 11 September 2022 (Sundays carrying "
               "Saturday's close, legacy codes mapped through client_master_2026-12.xlsx, ROSALESB and ROSALESK as "
               "PD2063) with wms_inventory_nightly_20220913_20261207.csv summed over sites (each run holding the close "
               "of the day before it, per wms_export_dictionary_v3.pdf) and wms_outbound_daily_20220912_20261206.csv: "
               "%s pallets on hand at the close of 6 December." % n(k["on_hand_6dec"]))
    out.append("2. Set each account's normal stock at mid-month as its cover times the mean of that and the next "
               "month's shipments (actual, then forecast), interpolated by day, the cover being its median, over its "
               "months from July 2023 clear of each duty step's month, the three months before it and the five after, "
               "of pallets on hand over the mean of that and the next month's shipments.")
    out.append("3. For each duty step in yv_client_advisories_2019-2026.pdf (1 September 2019, 5 April 2025, 7 August "
               "2025) where an account's excess over normal stock, its mean over the seven days before the step, was "
               "at least %d%% of normal stock, fitted the fall in that excess against cumulative shipments from the "
               "step (a least-squares slope with an intercept) until the excess fell under a quarter of its size or "
               "the next advisory, keeping fits of %d days or more: each account's burn share is the shipment-weighted "
               "mean of its episodes, %.3f to %.3f." % (st["episode_floor_pct"], st["episode_min_days"], shares[0],
                                                        shares[-1]))
    out.append("4. Forecast each account's shipments for December 2026 to July 2027 as the same month a year earlier "
               "times its shipments from December 2025 to November 2026 over the twelve months before, spread over "
               "each month's working days with a Saturday at %s of a weekday (the book's own ratio) and Sundays, "
               "Christmas Eve, Christmas Day, New Year's Day and Memorial Day closed." % st["saturday_weight"])
    out.append("5. Projected each account's close of 31 December as the close of 6 December plus the pallets due in "
               "dec2026_inbound_booking_tracker.xlsx (box-only notices at the account's own pallets per box over the "
               "last %d days, per the tracker) less the rest of December's forecast shipments: %s pallets over normal "
               "stock, %s of them with the five seasonal accounts." % (st["notice_window_days"],
                                                                       n(k["excess_31dec"]),
                                                                       n(k["seasonal_excess_31dec"])))
    out.append("6. Burned each account's excess day by day at its burn share of its forecast shipments until it was "
               "gone, added its normal stock and took the mean of each day's close by month (space policy 3.1): "
               "overflow above %s of %s positions from January to June, with %s pallets of excess left at 30 June."
               % (n(st["rack_positions"]), ", ".join(n(x) for x in ov[:5]) + " and " + n(ov[5]), n(k["excess_30jun"])))
    out.append("7. Ran the block test of space_planning_policy_rev4.pdf section 4.2: blocks 1 and 2 hold %.1f%% and "
               "%.1f%% of their %s position-months and block 3 %.1f%%, so we take %d blocks, %s at the %s per block "
               "in ridley-ames_bldg-b_overflow_blocks_2026-11-19.pdf." % (u[0], u[1], n(st["position_months"]), u[2],
                                                                        c["blocks"], c["cost"], c["price"]))
    out.append("")
    out.append("## 4. Deliverable Answers\n")
    out.append("### overflow_blocks_h1_2027.xlsx\n")
    out.append("1. The call on the Blocks sheet: take %d of the 6 blocks (B-1 and B-2), %s for the term; block uses "
               "%.1f%%, %.1f%% and %.1f%%." % (c["blocks"], c["cost"], u[0], u[1], u[2]))
    out.append("2. Pallets we held outside our racks at the close of 6 December, by building:")
    for code, name in BUILDING:
        out.append("   - %s (%s): %s" % (code, name, n(F["a1"][code])))
    out.append("3. TEU of the import containers whose freight reached us from the two ports, and that TEU as a share of "
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
