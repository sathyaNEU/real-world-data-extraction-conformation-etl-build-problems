"""The pack's record files as each system exports them: the two policy administration exports, the policy number
crosswalk, the data warehouse's mid-term adjustments, the two claims exports, the glass partner's job file, the
salvage agent's statements, the rating region map, the industry statistics and the complaints log. Each writer
returns its row count."""
import csv
import datetime as dt

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import books as B
import common as K
import world as W

LEG_TYPE = {"ACC": "ACC", "WSC": "WSC", "THF": "THF", "FIR": "FIR"}
PLAT_TYPE = {"ACC": "Accident", "WSC": "Windscreen", "THF": "Theft", "FIR": "Fire"}
LEG_SECTION = {"OD": "OD", "TPP": "TPP", "TPI": "TPI", "NTF": "NTF", "GLASS": "GLS", "THEFT": "THF", "FIRE": "FIR"}
PLAT_SECTION = {"OD": "Own damage", "TPP": "Third party property", "TPI": "Third party injury",
                "NTF": "Notification only", "GLASS": "Glass", "THEFT": "Theft", "FIRE": "Fire"}
PLAT_LIAB = {"F": "At fault", "S": "Split", "N": "Not at fault", "P": "Pending", "": ""}
LEG_STATUS = {"Open": "O", "Closed": "C", "Reopened": "R"}
PLAT_COVER = {"COMP": "Comprehensive", "TPFT": "Third party, fire and theft"}
PLAT_CHANNEL = {"Direct web": "Direct web", "Direct phone": "Direct phone", "Broker": "Broker"}
LEG_CHANNEL = {"Direct web": "WEB", "Direct phone": "PHONE", "Broker": "BROKER"}
PLAT_EXTRA = {"LEGAL": "Legal expenses", "BREAKDOWN": "Breakdown", "COURTESY": "Courtesy car"}


def _csv(path, header, rows, delim=","):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=delim, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def _sheet(ws, header, rows, widths, fmt=None, freeze=True, fill="D9E2EC"):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(vertical="top", wrap_text=True)
    for row in rows:
        ws.append(row)
    for i, w in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w
    for c, f in (fmt or {}).items():
        for cell in ws[openpyxl.utils.get_column_letter(c + 1)][1:]:
            cell.number_format = f
    if freeze:
        ws.freeze_panes = "A2"


def dmy(d):
    return d.strftime("%d/%m/%Y") if d else ""


def iso(d):
    return d.isoformat() if d else ""


def pence(x):
    return int(round(x * 100))


def money(x):
    return "%.2f" % x


def police_legacy(crime):
    return "%s/%02d/%06d" % crime


def police_platform(crime):
    return "%s%02d%06d" % crime


# ------------------------------------------------------------------------------------------------- policy terms
def write_policy_legacy(path, bk):
    rows = []
    for r in sorted(bk["leg_terms"], key=lambda r: (r["start"], r["ref"])):
        rows.append([r["ref"], r["seq"], dmy(r["start"]), dmy(r["end"]), dmy(r["cancelled"]), r["district"], r["step"],
                     "Y" if r["protected"] else "N", r["cover"], r["reg"], r["veh_group"], r["veh_year"], r["age"],
                     LEG_CHANNEL[r["channel"]], money(r["prem_net"]), money(r["ipt"]), "|".join(r["extras"])])
    return _csv(path, ["POLICY_NO", "TERM_NO", "INCEPTION_DATE", "EXPIRY_DATE", "CANCELLATION_DATE",
                       "GARAGING_DISTRICT", "NCD_STEP", "STEP_PROTECTION", "COVER", "VEHICLE_REG", "ABI_GROUP",
                       "VEHICLE_YEAR", "MAIN_DRIVER_AGE", "CHANNEL", "NET_PREMIUM", "IPT", "ADDONS"], rows)


def write_policy_platform(path, bk):
    rows = []
    for r in sorted(bk["plat_terms"], key=lambda r: (r["start"], r["ref"])):
        cancel = r["cancelled"] + dt.timedelta(days=1) if r["cancelled"] else None
        rows.append([r["ref"], r["seq"], iso(r["start"]), iso(r["end"] + dt.timedelta(days=1)), iso(cancel),
                     "%s %s" % (r["district"], r["inward"]), r["step"], "true" if r["protected"] else "false",
                     PLAT_COVER[r["cover"]], r["reg"], r["veh_group"], r["veh_year"], r["age"],
                     PLAT_CHANNEL[r["channel"]], money(r["prem_net"]), money(r["ipt"]),
                     ";".join(PLAT_EXTRA[e] for e in r["extras"])])
    return _csv(path, ["policy_number", "term_number", "term_start", "term_end", "cancellation_date",
                       "garaging_postcode", "ncd_step", "step_protection", "cover_type", "vehicle_registration",
                       "abi_group", "year_of_manufacture", "main_driver_age_band", "sales_channel", "net_premium_gbp",
                       "ipt_gbp", "add_ons"], rows)


def write_crosswalk(path, bk):
    rows = [[a, b, iso(d)] for a, b, d in bk["crosswalk"]]
    return _csv(path, ["legacy_policy_no", "platform_policy_number", "first_platform_term_start"], rows)


def write_mtas(path, bk):
    rows = []
    for m in sorted(bk["mtas"], key=lambda m: (m["day"], m["ref"], m["kind"])):
        plat = m["system"] == "P"
        where = cover = reg = group = ""
        if m["kind"] == "Change of address":
            where = "%s %s" % (m["district"], m["inward"]) if plat else m["district"]
        elif m["kind"] == "Change of cover":
            cover = PLAT_COVER[m["cover"]] if plat else m["cover"]
        else:
            reg, group = m["reg"], m["veh_group"]
        rows.append(["PLATFORM" if plat else "LEGACY", m["ref"], m["seq"], iso(m["start"]), iso(m["day"]),
                     m["kind"], where, cover, reg, group, money(m["prem"])])
    return _csv(path, ["source_system", "policy_number", "term_number", "term_start", "effective_date",
                       "adjustment_type", "new_garaging", "new_cover", "new_vehicle_reg", "new_abi_group",
                       "premium_change_gbp"], rows)


# ------------------------------------------------------------------------------------------------- claims
def _in_export(c, system):
    if c["system"] != system:
        return False
    d = c["notified"].date()
    return K.FIRST_INCEPTION <= d <= K.EXTRACT


def write_claims_legacy(path, bk):
    rows = []
    for c in bk["claims"]:
        if not _in_export(c, "L"):
            continue
        rows.append([c["no"], c["ref"], dmy(c["loss"]), dmy(c["notified"].date()), LEG_TYPE[c["kind"]],
                     LEG_SECTION[c["section"]], c["liab"], LEG_STATUS[c["status"]], pence(c["paid"]),
                     pence(c["outstanding"]), pence(c["recovered"]),
                     police_legacy(c["police"]) if c["police"] else "", c["supplier"], c["supplier_ref"]])
    return _csv(path, ["CLAIM_NO", "POLICY_NO", "LOSS_DATE", "NOTIFIED_DATE", "CLAIM_TYPE", "SECTION", "FAULT",
                       "STATUS", "PAID_AMT", "OS_AMT", "RECOV_AMT", "POLICE_REF", "SUPPLIER", "SUPPLIER_REF"], rows)


def write_claims_platform(path, bk):
    rows = []
    for c in bk["claims"]:
        if not _in_export(c, "P"):
            continue
        rows.append([c["no"], c["ref"], iso(c["loss"]), B.utc(c["notified"]).strftime("%Y-%m-%dT%H:%M:%SZ"),
                     PLAT_TYPE[c["kind"]], PLAT_SECTION[c["section"]], PLAT_LIAB[c["liab"]], c["status"],
                     money(c["paid"]), money(c["outstanding"]), money(c["recovered"]),
                     police_platform(c["police"]) if c["police"] else "", c["supplier"], c["supplier_ref"]])
    return _csv(path, ["claim_number", "policy_number", "loss_date", "notified_at", "claim_type", "section",
                       "liability", "status", "paid_gbp", "outstanding_gbp", "recovered_gbp", "police_reference",
                       "supplier", "supplier_reference"], rows)


# ------------------------------------------------------------------------------------------------- glass partner
def glass_jobs(bk):
    """The partner's 2025 job lines, its job references in booking order."""
    jobs = [g for g in bk["glass"] if g["network"] and g["booked"].year == 2025]
    lines = []
    n = 2507000
    for g in sorted(jobs, key=lambda g: (g["booked"], g["ev"], g["follow"])):
        n += 1
        ref = "CVG%07d" % n
        g["job_ref"] = ref
        billed = "Customer" if g["customer"] else K.SHORT
        work = []
        if not g.get("calib_only"):
            work.append(("Windscreen replacement" if g["repl"] else "Windscreen repair", g["net"]))
        if g["calib"]:
            work.append(("ADAS camera recalibration", g["calib"]))
        for no, (desc, amount) in enumerate(work, 1):
            lines.append([ref, no, g["booked"].strftime("%d/%m/%Y %H:%M"), dmy(g["fitted"]), g["ref"], g["reg"],
                          g["fit_district"], desc, billed, money(amount), money(round(amount * 0.2, 2)),
                          g["fitted"].strftime("%Y-%m")])
    return lines


def write_glass(path, lines):
    return _csv(path, ["job_ref", "line_no", "booked", "fitted_date", "insurer_policy_ref", "vehicle_reg",
                       "fitting_postcode_district", "description", "billed_to", "net_amount", "vat_amount",
                       "invoice_month"], lines)


# ------------------------------------------------------------------------------------------------- salvage
def write_salvage(path, bk, w, seed=W.SEED):
    rng = np.random.default_rng([seed, 31])
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    n = 0
    for year in (2025, 2026):
        rows = []
        for s in bk["salvage"]:
            if s["sold"].year != year:
                continue
            c = s["claim"]
            fees = round(float(rng.uniform(85, 180)), 2)
            cat = {"THF": "Recovered theft", "FIR": "Cat B"}.get(c["kind"], "Cat S" if rng.random() < 0.7 else "Cat N")
            rows.append([s["lot"], s["sold"], c["no"], B.term_on(w["terms"][c["term"]], c["loss"])[2], cat,
                         round(s["proceeds"] + fees, 2), fees, s["proceeds"]])
        ws = wb.create_sheet("Statements %d" % year)
        _sheet(ws, ["Lot", "Sale date", "Client claim ref", "Registration", "Category", "Hammer price (GBP)",
                    "Agent fees (GBP)", "Net proceeds remitted (GBP)"], rows, [10, 12, 16, 12, 16, 16, 15, 22],
               fmt={1: "dd/mm/yyyy", 5: "#,##0.00", 6: "#,##0.00", 7: "#,##0.00"})
        n += len(rows)
    wb.save(path)
    return n


# ------------------------------------------------------------------------------------------------- region map
def write_region_map(path):
    rows = []
    for code, name, ds in K.REGIONS:
        for d in ds:
            if d in K.REMAP:
                old, new = K.REMAP[d]
                rows.append([d, old, K.NAME[old], "2019-01-01", (K.REMAP_DATE - dt.timedelta(days=1)).isoformat()])
                rows.append([d, new, K.NAME[new], K.REMAP_DATE.isoformat(), ""])
            else:
                rows.append([d, code, name, "2019-01-01", ""])

    def key(r):
        import re
        m = re.match(r"([A-Z]+)(\d+)", r[0])
        return (m.group(1), int(m.group(2)), r[3])
    rows.sort(key=key)
    return _csv(path, ["postcode_district", "rating_region_code", "rating_region", "effective_from", "effective_to"],
                rows)


# ------------------------------------------------------------------------------------------------- distractors
def write_industry(path, seed=W.SEED):
    """National private car claims statistics by cover and peril, 2021 to 2025 (frequency per 100 vehicle-years and
    average incurred cost), as the statistics service publishes them."""
    rng = np.random.default_rng([seed, 41])
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    base = {("Comprehensive", "Accident"): (10.9, 3260), ("Comprehensive", "Windscreen"): (10.6, 452),
            ("Comprehensive", "Theft"): (0.74, 9850), ("Comprehensive", "Fire"): (0.09, 6420),
            ("Third party, fire and theft", "Accident"): (12.8, 3910), ("Third party, fire and theft", "Theft"): (1.02, 6340),
            ("Third party, fire and theft", "Fire"): (0.11, 4980)}
    growth = {2021: 0.86, 2022: 0.91, 2023: 1.00, 2024: 1.06, 2025: 1.09}
    rows = []
    for (cover, peril), (f, a) in base.items():
        for y in sorted(growth):
            fy = round(f * (0.97 + 0.06 * rng.random()) * (1.0 if y > 2021 else 0.93), 2)
            ay = int(round(a * growth[y] * (0.98 + 0.04 * rng.random())))
            vy = int(round(21.4e6 * (0.62 if cover == "Comprehensive" else 0.14) * (0.99 + 0.02 * rng.random())))
            rows.append([y, cover, peril, vy, fy, ay])
    ws = wb.create_sheet("Private car by peril")
    _sheet(ws, ["Year", "Cover", "Peril", "Vehicle-years (all contributors)", "Claims per 100 vehicle-years",
                "Average incurred (GBP)"], rows, [7, 26, 12, 18, 16, 16],
           fmt={3: "#,##0", 4: "0.00", 5: "#,##0"})
    notes = wb.create_sheet("Notes")
    for line in ["Private Motor Statistics Service: contributor returns, private car, Great Britain.",
                 "Claims are counted on a notified basis and costed at the contributor's incurred at 31 March after the "
                 "year end. Windscreen claims include repairs and replacements settled direct with a glass network.",
                 "Vehicle-years are earned exposure on policies in force at any time in the year.",
                 "Released 14 May 2026. Contributors with fewer than 25,000 vehicle-years are pooled."]:
        notes.append([line])
    notes.column_dimensions["A"].width = 120
    wb.save(path)
    return len(rows)


def write_complaints(path, bk, seed=W.SEED):
    rng = np.random.default_rng([seed, 43])
    cats = [("Claims handling", 0.31), ("Premium at renewal", 0.22), ("No-claims step", 0.12),
            ("Windscreen repair", 0.08), ("Cancellation and refunds", 0.09), ("Policy documents", 0.07),
            ("Courtesy car", 0.05), ("Data protection", 0.03), ("Broker service", 0.03)]
    names, probs = zip(*cats)
    pool = [r for r in bk["leg_terms"] + bk["plat_terms"] if r["start"] <= dt.date(2025, 12, 31) and r["end"] >= dt.date(2025, 1, 1)]
    rows = []
    n = 0
    for k in range(1640):
        day = dt.date(2025, 1, 2) + dt.timedelta(days=int(rng.integers(0, 362)))
        r = pool[int(rng.integers(len(pool)))]
        cat = names[int(rng.choice(len(names), p=np.array(probs) / sum(probs)))]
        outcome = str(rng.choice(["Upheld", "Partly upheld", "Not upheld", "Withdrawn"], p=[0.27, 0.19, 0.47, 0.07]))
        closed = day + dt.timedelta(days=int(min(56, rng.gamma(2.0, 9.0))) + 1)
        redress = 0.0
        if outcome in ("Upheld", "Partly upheld"):
            redress = round(float(rng.choice([25, 50, 75, 100, 150, 250])) if rng.random() < 0.7
                            else float(rng.uniform(40, 900)), 2)
        n += 1
        rows.append(["CMP-25-%05d" % n, iso(day), str(rng.choice(["Phone", "Email", "Web form", "Letter"],
                                                                   p=[0.48, 0.27, 0.2, 0.05])),
                     r["ref"], cat, outcome, iso(closed) if closed <= K.EXTRACT else "", money(redress),
                     "Y" if rng.random() < 0.04 else "N"])
    rows.sort(key=lambda r: (r[1], r[0]))
    return _csv(path, ["complaint_ref", "received", "channel", "policy_number", "category", "outcome", "closed",
                       "redress_gbp", "referred_to_ombudsman"], rows)
