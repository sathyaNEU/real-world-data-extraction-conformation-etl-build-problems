"""An independent recomputation of every graded figure from the shipped files alone (pandas and statsmodels, no
generator module but the file names), against figures.json: the list, the deciding bands, the components, item (b)
and item (c)."""
import json
import os
import re
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = os.path.dirname(os.path.abspath(__file__))
T0 = pd.Timestamp("2027-09-30 11:00", tz="UTC")
NS = 92 * 144


def main(target):
    fails = []
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    f = lambda n: os.path.join(target, n)
    r = pd.read_csv(f("nh3_online_readings_2027Q4.csv"))
    r["slot"] = ((pd.to_datetime(r["reading_end_utc"], utc=True) - T0).dt.total_seconds() // 600).astype(int) - 1
    reg = pd.read_excel(f("online_analyser_register.xlsx"), sheet_name="Analysers")
    pts = pd.read_excel(f("online_analyser_register.xlsx"), sheet_name="Sample points")
    chk = pd.read_excel(f("analyser_verification_2027Q4.xlsx"), sheet_name="Checks Q4 2027")
    lab = pd.read_csv(f("lims_ammonia_2027Q4.csv"))
    old = dict(re.findall(r"^\s+(TW-\S+)\s+(TUR\S+)\s*$", open(f("Kowhai_Bay_new_site_codes_from_1_November.eml")).read(),
                          flags=re.M))
    code2pt = dict(zip(pts["Laboratory code"].dropna(), pts.loc[pts["Laboratory code"].notna(), "Sample point"]))
    lab["point"] = lab["lims_point"].map(lambda c: code2pt.get(old.get(c, c)))
    lab["plant"] = lab["point"].str[:3]
    lab["water"] = lab["point"].str[4:6]
    for c in ("collected", "received", "analysed", "released"):
        lab[c] = pd.to_datetime(lab[c], format="%d/%m/%Y %H:%M")
    offsets = {}
    forms = {}
    for _, a in reg.iterrows():
        code = a["Analyser tag"].split("-")[1]
        seq = [p.strip().split("-")[1] for p in a["Port sequence"].split(">")]
        x = r[r["site_code"] == code]
        good = x[x["qc"] == "G"].drop_duplicates("slot", keep="last").set_index("slot")["nh3_n_mgl"]
        ver = x[x["qc"] == "V"].set_index("slot")["nh3_n_mgl"]
        s = pd.Series(np.nan, index=range(NS))
        s.loc[good.index] = good.values
        cell = s.copy()
        cell.loc[ver.index] = ver.values
        port = pd.Series([seq[i % 3] for i in range(NS)])
        raw = s.where(port == "RW1").interpolate(limit_direction="both")
        # one pair of carryover shares for the analyser, fitted on both treated ports together, each port with its
        # own level and its own response to the raw water 2 to 8 hours back
        parts = []
        for sp in ("FI1", "FW1"):
            df = pd.DataFrame({"r": s, "p1": cell.shift(1), "p2": cell.shift(2)})
            for L in range(12, 49, 3):
                df["%s_L%d" % (sp, L)] = raw.shift(L)
            df = df[(port == sp) & df.index.isin(good.index)].iloc[16:].dropna()
            df["is_" + sp] = 1.0
            df["port"] = sp
            parts.append(df)
        big = pd.concat(parts).fillna(0.0)
        X = big.drop(columns=["r", "port"])
        b = sm.OLS(big["r"], X).fit().params
        k1, k2 = b["p1"], b["p2"]
        carry = {}
        for sp in ("FI1", "FW1"):
            d = big[big["port"] == sp]
            carry[sp] = (k1 * (d["p1"] - d["r"]).mean() + k2 * (d["p2"] - d["r"]).mean()) / (1 - k1 - k2)
        dev = chk[chk["Analyser tag"] == a["Analyser tag"]][["Reading 1", "Reading 2", "Reading 3"]].to_numpy().mean() - 0.1
        form = None
        if abs(dev) >= 0.003:
            g = lab[(lab["plant"] == code) & (lab["water"] == "RW")]
            rows = []
            for _, q in g.iterrows():
                t = q["collected"].tz_localize("Pacific/Auckland").tz_convert("UTC")
                i = int((t - T0).total_seconds() // 600)
                cand = [j for j in range(max(i - 60, 2), min(i + 61, NS)) if port[j] == "RW1" and not np.isnan(s[j])
                        and not np.isnan(cell[j - 1]) and not np.isnan(cell[j - 2])]
                j = min(cand, key=lambda j: abs(j - i))
                v = float(q["result"])
                rows.append((v, s[j] - v - (k1 * (cell[j - 1] - v) + k2 * (cell[j - 2] - v))))
            rows = np.array(rows)
            z = np.sum((rows[:, 1] - dev) ** 2); sp_ = np.sum((rows[:, 1] - dev / 0.1 * rows[:, 0]) ** 2)
            form = "zero" if z < sp_ else "span"
        forms[code] = (form, dev)
        for sp in ("FI1", "FW1"):
            lvl = s[(port == sp)].mean()
            cal = 0 if form is None else (dev if form == "zero" else dev / 0.1 * lvl)
            offsets["%s-%s" % (code, sp)] = carry[sp] + cal
    flagged = sorted(k for k, v in offsets.items() if abs(v) > 0.005)
    if flagged != fig["flagged"]:
        fails.append(("flagged", flagged, fig["flagged"]))
    lo = min(abs(offsets[k]) for k in flagged); hi = max(abs(v) for k, v in offsets.items() if k not in flagged)
    if not (lo >= fig["flag_band_print"] and hi <= np.ceil(fig["unflagged_band_high"] * 1000) / 1000):
        fails.append(("bands", lo, hi))
    if forms["HOL"][0] != "zero" or forms["CAL"][0] != "span":
        fails.append(("forms", forms["HOL"], forms["CAL"]))
    if round(forms["HOL"][1], 3) != fig["hol_zero_error"]:
        fails.append(("hol zero", forms["HOL"][1]))
    if round(abs(forms["CAL"][1]) / 0.1 * 100) != fig["cal_span_pct"]:
        fails.append(("cal span", forms["CAL"][1]))
    if abs(offsets["HOL-FW1"]) >= np.ceil(fig["unflagged_band_high"] * 1000) / 1000:
        fails.append(("HOL-FW1 within the unflagged band", offsets["HOL-FW1"]))
    # item (b): the analysis stamps run behind the reception and release clocks; bracket the offset from the rows and
    # count with every offset inside it (the hour, standard time against daylight time, is one of them)
    lo = (lab["received"] - lab["analysed"]).dt.total_seconds().max() / 60
    hi = (lab["released"] - lab["analysed"]).dt.total_seconds().min() / 60
    if not lo < 60 < hi:
        fails.append(("clock bracket", lo, hi))
    t = lab[lab["water"] != "RW"].copy()
    # one bottle, one sample: two rows with the same point, analysis stamp and result are one bottle logged twice
    t = t.drop_duplicates(subset=["point", "analysed", "result"])
    names = dict(zip(reg["Analyser tag"].str.split("-").str[1], reg["Plant"]))
    for m in sorted({lo + 0.5, 60.0, hi - 0.5}):
        late = (t["analysed"] + pd.Timedelta(minutes=m) - t["collected"]) > pd.Timedelta(hours=24)
        b = late.groupby(t["plant"]).sum()
        for code, n in b.items():
            if int(n) != fig["ask_a"][names[code]]:
                fails.append(("ask a", m, code, int(n), fig["ask_a"][names[code]]))
    # item (c): at the PLC a slot is good unless no reading reached the PLC there or the analyser was on its check
    # port. A failed poll takes the plant's whole record and is filled from the outstation unless its store was lost;
    # a fault stops the analyser until a technician clears it and checks it. So only a stretch of unfilled F rows at
    # every port with no check-port reading straight after it was the telemetry's; a port's own unfilled F rows, with
    # the other ports read between them, are readings the PLC never had
    for _, a in reg.iterrows():
        code = a["Analyser tag"].split("-")[1]
        seq = [p.strip().split("-")[1] for p in a["Port sequence"].split(">")]
        x = r[r["site_code"] == code]
        fi = [i for i in range(NS) if seq[i % 3] == "FI1"]
        qc = x.groupby("slot")["qc"].agg(lambda q: "".join(sorted(q)))
        lone = sorted(i for i, q in qc.items() if q == "F")
        telem = set()
        run = []
        for i in lone + [None]:
            if run and (i is None or i - run[-1] > 3):
                whole = run == list(range(run[0], run[-1] + 1))
                if whole and not any(qc.get(j, "") == "V" for j in range(run[-1] + 1, run[-1] + 4)):
                    telem |= set(range(run[0], run[-1] + 1))
                run = []
            if i is not None:
                run.append(i)
        good = [i for i in fi if qc.get(i, "") not in ("F", "V") or i in telem]
        gaps = np.diff(good) * 10 / 60
        hrs = float(np.sum(np.clip(gaps - 2, 0, None)))
        if round(hrs, 1) != fig["ask_b"][names[code]]:
            fails.append(("ask b", code, hrs, fig["ask_b"][names[code]]))
    return fails


if __name__ == "__main__":
    out = main(sys.argv[1])
    print("verify: %d failures" % len(out))
    for o in out:
        print(" ", o)
    sys.exit(1 if out else 0)
