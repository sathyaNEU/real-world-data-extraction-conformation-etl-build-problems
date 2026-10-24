"""The independent verifier: reads only the shipped bundle (target/), the golden deliverables and figures.json, on its
own code path (pandas for the tables, pdfplumber for the documents), and recomputes the certification, every city's
figures and both reports.

    python3 task482/generator/verify.py
"""
import calendar
import json
import math
import os
import re
import sys

import pandas as pd
import pdfplumber

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
GD = os.path.join(TASK, "golden")
OK, BAD = [0], []


def v(label, cond, detail=""):
    OK[0] += 1
    if not cond:
        BAD.append(label)
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  (" + detail + ")") if detail else ""))


def f(prefix):
    m = [n for n in os.listdir(T) if n.startswith(prefix)]
    assert len(m) == 1, prefix
    return os.path.join(T, m[0])


def pdf(prefix):
    with pdfplumber.open(f(prefix)) as d:
        return " ".join(" ".join(p.extract_text() or "" for p in d.pages).split())


def half_up(x, nd=0):
    k = 10 ** nd
    return math.floor(x * k + 0.5) / k


def ndays(ym):
    return calendar.monthrange(ym[0], ym[1])[1]


def months(a, b):
    out = [a]
    while out[-1] != b:
        y, m = out[-1]
        out.append((y + 1, 1) if m == 12 else (y, m + 1))
    return out


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))

    # ---------------------------------------------------------------- the documents, read back
    act, ordn, fact = pdf("seasonal_communities_aid_act"), pdf("lake_protection_fee_ordinance"), pdf("quillmere_basin_wastewater")
    v("pdf: the Act reads back", "Busiest month" in act and "Section 5" in act)
    v("pdf: the ordinance reads back", "Marketplace platforms" in ordn)
    v("pdf: the fact sheet reads back", "force main" in fact)
    approp = int(re.search(r"USD ([\d,]+) is appropriated", act).group(1).replace(",", ""))
    v("pdf: the appropriation is USD 2,400,000 and the test three times residents",
      approp == 2400000 and "at least three times its resident population" in act)
    my = re.search(r"For aid year 2027 it is 1 October (\d{4}) through 30 September (\d{4})", act)
    MY = months((int(my.group(1)), 10), (int(my.group(2)), 9))
    v("pdf: the measurement year is October 2025 to September 2026", MY[0] == (2025, 10) and MY[-1] == (2026, 9))
    r1, r2 = [float(x) for x in re.findall(r"USD (1\.\d\d) a guest-night", ordn)]
    v("pdf: the fee is 1.25 through 2025 and 1.50 from 1 January 2026", (r1, r2) == (1.25, 1.50))
    k834 = float(re.search(r"per liter times ([\d.]+)", fact).group(1))
    v("pdf: the fact sheet's load convention is 8.34", k834 == 8.34)

    # ---------------------------------------------------------------- residents
    pop = pd.read_csv(f("quillmere_county_population"), dtype={"GEOID": str})
    cities = pop[pop["GEOGRAPHY"].str.endswith(" city")]
    R = dict(zip(cities["GEOGRAPHY"].str[:-5], cities["POPEST_2026_07_01"].astype(int)))
    towns = list(figs["order"])
    v("residents: eight basin cities, 1 July 2026", sorted(R) == sorted(towns))

    # ---------------------------------------------------------------- the plants' influent
    e = pd.read_csv(f("edmr_dmr_export"), dtype={"PARAMETER_CODE": str, "MONITORING_LOCATION_CODE": str})
    e["end"] = pd.to_datetime(e["MONITORING_PERIOD_END_DATE"], format="%m/%d/%Y")
    e["rec"] = pd.to_datetime(e["RECEIVED_DATE"], format="%m/%d/%Y")
    acc = e[e["SUBMISSION_STATUS"] == "Accepted"].sort_values("rec")
    acc = acc.groupby(["PERMIT_ID", "end", "MONITORING_LOCATION_CODE", "PARAMETER_CODE"]).tail(1)
    acc = acc.assign(ym=list(zip(acc["end"].dt.year, acc["end"].dt.month)))
    val = {(r.PERMIT_ID, r.ym, r.MONITORING_LOCATION_CODE, r.PARAMETER_CODE): float(r.DMR_VALUE) for r in acc.itertuples()}
    permit = {"Birchwick": "MN0099127", "Teskadel": "MN0099146", "Sorrelton": "MN0099158", "Tamsen Point": "MN0099173",
              "Narrows": "MN0099181"}
    BOD = {}
    for n, pid in permit.items():
        if n == "Narrows":
            continue
        for ym in {k[1] for k in val if k[0] == pid}:
            BOD[(n, ym)] = val[(pid, ym, "G", "50050")] * val[(pid, ym, "G", "00310")] * k834
    for sheet, df in pd.read_excel(f("ruddmere_pinehold_ponds"), sheet_name=None, header=3).items():
        n = sheet.rsplit(" ", 1)[0]
        for r in df.itertuples(index=False):
            if not isinstance(r[0], str):
                continue
            d = pd.to_datetime(r[0], format="%b %Y")
            BOD[(n, (d.year, d.month))] = float(r[1]) * float(r[2]) * k834
    mt = pd.read_csv(f("narrows_joint_member_meters"))
    ts = pd.to_datetime(mt["READ_AT"], format="%m/%d/%Y %H:%M")
    ts = ts.where(~((ts.dt.hour == 0) & (ts.dt.minute == 0)), ts - pd.Timedelta(days=1))
    mt = mt.assign(ym=list(zip(ts.dt.year, ts.dt.month)))
    gal = mt.groupby(["MEMBER", "ym"])["VOLUME_SINCE_LAST_READ_GAL"].sum().to_dict()
    for ym in {k[1] for k in val if k[0] == "MN0099181"}:
        for n in ("Esker Narrows", "Hollin Bay"):
            BOD[(n, ym)] = gal[(n, ym)] / ndays(ym) / 1e6 * val[("MN0099181", ym, "G", "00310")] * k834
    v("plants: 21 months of influent BOD load for each city", all(sum(1 for k in BOD if k[0] == n) == 21 for n in towns))

    # ---------------------------------------------------------------- paid guests on an average day
    paid = {}
    rt = pd.read_csv(f("lake_protection_fee_returns_2"))
    rt["filed"] = pd.to_datetime(rt["DATE_FILED"], format="%m/%d/%Y")
    rt = rt.sort_values("filed")
    base = rt[rt["RETURN_TYPE"].isin(["Original", "Amended"])].groupby(["ACCOUNT_NO", "PERIOD_START"]).tail(1)
    cur = pd.concat([base, rt[rt["RETURN_TYPE"] == "Supplemental"]])
    for r in cur.itertuples():
        a = pd.to_datetime(r.PERIOD_START, format="%m/%d/%Y")
        b = pd.to_datetime(r.PERIOD_END, format="%m/%d/%Y")
        ms = months((a.year, a.month), (b.year, b.month))
        tot = sum(ndays(x) for x in ms)
        for x in ms:
            paid[(r.PROPERTY_CITY, x)] = paid.get((r.PROPERTY_CITY, x), 0) + r.GUEST_NIGHTS_TOTAL * ndays(x) / tot
    lw = pd.read_csv(f("lakeward_stays_remittance"))
    ck = pd.read_csv(f("kettle_and_pine_remittance"))
    ck_arr = pd.to_datetime(ck["Reservation"].str[1:7], format="%y%m%d") - pd.to_timedelta(ck["Nights"], unit="D")
    stays = pd.concat([pd.DataFrame(dict(city=lw["listing_city"].str.title(), arr=pd.to_datetime(lw["check_in"]),
                                         nights=lw["nights"], guests=lw["guests"])),
                       pd.DataFrame(dict(city=ck["Municipality"], arr=ck_arr, nights=ck["Nights"],
                                         guests=ck["Party size"]))], ignore_index=True)
    nights = stays.loc[stays.index.repeat(stays["nights"])].copy()
    nights["d"] = nights["arr"] + pd.to_timedelta(nights.groupby(level=0).cumcount(), unit="D")
    gn = nights.groupby(["city", nights["d"].dt.year, nights["d"].dt.month])["guests"].sum()
    for (c, y, m), g in gn.items():
        paid[(c, (y, m))] = paid.get((c, (y, m)), 0) + g
    per_day = {k: g / ndays(k[1]) for k, g in paid.items()}

    # ---------------------------------------------------------------- the certification
    W = [(2026, m) for m in (1, 2, 3, 4)]
    qual = []
    for n in towns:
        lpp = sum(BOD[(n, ym)] / (R[n] + per_day.get((n, ym), 0)) for ym in W) / len(W)
        pres = {ym: BOD[(n, ym)] / lpp for ym in MY}
        b = max(pres, key=pres.get)
        name = calendar.month_name[b[1]] + " %d" % b[0]
        c = figs["cities"][n]
        q = pres[b] >= 3 * R[n]
        if q:
            qual.append(n)
        v("certification: %s busiest %s, %s present, %s" % (n, name, "{:,}".format(int(half_up(pres[b] / 1000) * 1000)),
                                                            "qualifies" if q else "does not qualify"),
          c["busiest"] == name and c["present"] == int(half_up(pres[b] / 1000) * 1000) and c["qualifies"] == q
          and c["residents"] == R[n] and c["three_x"] == 3 * R[n])
    share = approp // len(qual)
    v("certification: %d cities qualify at USD %s each" % (len(qual), "{:,}".format(share)),
      qual == figs["call"]["qualify"] and share == figs["call"]["share"] and share * len(qual) == approp
      and all(figs["cities"][n]["aid"] == (share if n in qual else 0) for n in towns))

    # ---------------------------------------------------------------- report 1: the fee by city and quarter
    qmap = {1: [(2025, 7), (2025, 8), (2025, 9)], 2: [(2025, 10), (2025, 11), (2025, 12)],
            3: [(2026, 1), (2026, 2), (2026, 3)], 4: [(2026, 4), (2026, 5), (2026, 6)]}
    qof = {ym: q for q, ms in qmap.items() for ym in ms}
    fee = {}
    for r in cur.itertuples():
        a = pd.to_datetime(r.PERIOD_START, format="%m/%d/%Y")
        q = qof.get((a.year, a.month))
        if q:
            fee[(r.PROPERTY_CITY, q)] = fee.get((r.PROPERTY_CITY, q), 0) + r.FEE_DUE
    short = nights[nights["nights"] < 30].copy()
    short["rate"] = (short["d"] >= pd.Timestamp("2026-01-01")).map({True: r2, False: r1})
    short["q"] = [qof.get((d.year, d.month)) for d in short["d"]]
    short = short[short["q"].notna()]
    for (c, q), x in (short["rate"] * short["guests"]).groupby([short["city"], short["q"]]).sum().items():
        fee[(c, int(q))] = fee.get((c, int(q)), 0) + x
    okA = [n for n in towns for q in (1, 2, 3, 4) if int(half_up(fee.get((n, q), 0))) == figs["ask_a"][n]["q%d" % q]]
    v("report 1: 32 fee figures, whole dollars", len(okA) == 32, "%d of 32" % len(okA))
    cks = ck.assign(arr=ck_arr)
    cks = cks[cks["Nights"] < 30]
    first26 = ((pd.Timestamp("2026-01-01") - cks["arr"]).dt.days).clip(lower=0)
    n25 = first26.where(first26 < cks["Nights"], cks["Nights"])
    est = (n25 * r1 + (cks["Nights"] - n25) * r2) * cks["Party size"]
    v("report 1: every Kettle & Pine fee remitted is the party times the rate on each night before the departure its "
      "reservation carries", bool(((est - cks["Fee remitted (USD)"]).abs() < 0.005).all()))

    # ---------------------------------------------------------------- report 2: phosphorus by plant and half
    tp = {}
    for n, pid in permit.items():
        for m in range(1, 13):
            x = val[(pid, (2025, m), "1", "50050")] * val[(pid, (2025, m), "1", "00665")] * k834 * ndays((2025, m))
            tp[(n, 1 if m <= 6 else 2)] = tp.get((n, 1 if m <= 6 else 2), 0) + x
    for sheet, df in pd.read_excel(f("ruddmere_pinehold_ponds"), sheet_name=None, header=3).items():
        n, yr = sheet.rsplit(" ", 1)
        if yr != "2025":
            continue
        for r in df.itertuples(index=False):
            if isinstance(r[0], str) and r[4] == "Yes":
                d = pd.to_datetime(r[0], format="%b %Y")
                tp[(n, 1 if d.month <= 6 else 2)] = tp.get((n, 1 if d.month <= 6 else 2), 0) + \
                    float(r[6]) * float(r[9]) * k834 * ndays((d.year, d.month))
    okB = [n for n in figs["plants"] for h in (1, 2) if abs(half_up(tp[(n, h)], 1) - figs["ask_b"][n]["h%d" % h]) < 1e-9]
    v("report 2: 14 phosphorus figures, one decimal", len(okB) == 14, "%d of 14" % len(okB))

    # ---------------------------------------------------------------- the golden deliverables carry the same figures
    wb = pd.read_excel(os.path.join(GD, "seasonal_communities_aid_2027_certification.xlsx"), sheet_name=None, header=None)
    v("golden: four sheets", list(wb) == ["Certification", "Lake Protection Fee", "Phosphorus 2025", "Notes"])
    cert = wb["Certification"].iloc[4:12]
    v("golden: the certification sheet carries every city's figures",
      all(int(r[3]) == figs["cities"][r[0]]["present"] and r[2] == figs["cities"][r[0]]["busiest"] and
          int(r[5]) == figs["cities"][r[0]]["aid"] and (r[4] == "Yes") == figs["cities"][r[0]]["qualifies"]
          for r in cert.itertuples(index=False)))
    fs = wb["Lake Protection Fee"].iloc[4:12]
    v("golden: the fee sheet carries the 32 figures",
      all([int(r[k]) for k in (1, 2, 3, 4)] == [figs["ask_a"][r[0]]["q%d" % q] for q in (1, 2, 3, 4)]
          for r in fs.itertuples(index=False)))
    ps = wb["Phosphorus 2025"].iloc[4:11]
    v("golden: the phosphorus sheet carries the 14 figures",
      all(abs(float(r[1]) - figs["ask_b"][n]["h1"]) < 1e-9 and abs(float(r[2]) - figs["ask_b"][n]["h2"]) < 1e-9
          for r, n in zip(ps.itertuples(index=False), figs["plants"])))
    v("golden: the chart is rendered", os.path.getsize(os.path.join(GD, "busiest_month_population_2026.png")) > 20000)

    print()
    print("%d checks, %d failed" % (OK[0], len(BAD)))
    for b in BAD:
        print("  FAILED: " + b)
    return 1 if BAD else 0


if __name__ == "__main__":
    sys.exit(main())
