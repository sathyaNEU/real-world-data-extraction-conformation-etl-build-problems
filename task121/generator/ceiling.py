"""The pair ceiling for task121 on the cut pack (supplemental-stumping Part 0 and Part 5), measured in code on the pack
named by its digest. It reads the shipped files itself and shares no code with the golden's asks, so it cannot inherit
the golden's handling.

The cracker is the careful solver. It lands the call (the quick returns) and reads every field by its plain meaning:
first_compression_s as seconds, arrived_utc and answered_utc as UTC, abandoned as Y or N, and the reference's trunk
descriptions. It executes every filed rule as worded:
- QA 1.2: local months, by answer, or by arrival for a call never answered;
- QA 4.2: answered within 15 seconds or less, over the calls answered, abandoned calls out;
- QA 5.1: the reviewer's times run from the start of the recording, and the measure from answer to first compression;
- QA 5.2: each arrest at its primary review, where compressions were coached.
It also runs the hygiene battery (supplemental-stumping 1.1c). Every battery item that changes the computation is a
route of its own, and the cracker keeps an ask figure when any careful route lands it, the worst case for the build.

The mirror is the response on R0 (the release). The asks consume nothing the call's construction produces, so it reads
them the same way, through the same routes.

The full includer handles every device (QA7's times read as minutes and seconds, the passed records left out) and must
reproduce figures.json; the old sheet cracker is printed beside it for comparison.

    python3 task121/generator/ceiling.py [task_dir]     exit 0 when every requirement below holds

Requirements: the cracker misses every ask row; mirror leakage under 50 per cent with no ask whole; the pair at or under
60; two careful responses on the call under 70; the full includer reproduces every graded ask figure.
"""
import decimal
import hashlib
import json
import os
import statistics
import sys

import openpyxl
import pandas as pd

MONTHS = ["2025-%02d" % m for m in range(9, 13)] + ["2026-%02d" % m for m in range(1, 9)]
TZ = "America/Chicago"


def rq(x, q):
    return float(decimal.Decimal(repr(float(x))).quantize(decimal.Decimal(q), rounding=decimal.ROUND_HALF_UP))


def load(target):
    p = lambda f: os.path.join(target, f)
    cad = pd.read_csv(p("cad_medical_calls_2025_2026.csv"), dtype=str, keep_default_na=False)
    tr = pd.read_csv(p("tcpr_arrest_reviews_2025_2026.csv"), dtype=str, keep_default_na=False)
    ch = pd.read_csv(p("che_call_detail_2025_2026.csv"), dtype=str, keep_default_na=False)
    rows = list(openpyxl.load_workbook(p("centre_reference.xlsx"), read_only=True)["Trunk groups"]
                .iter_rows(values_only=True))
    tg911 = {r[0] for r in rows[1:] if str(r[1]).startswith("911")}
    return cad, tr, ch, tg911


def ask_b(cad, tr, qa7_minsec=False, dedup=None, trim=None, month_by="answer"):
    """median seconds from answer to the first coached compression, primary reviews, by local month (QA 1.2, 5.1, 5.2)"""
    loc = lambda s: pd.to_datetime(s, format="%m/%d/%Y %H:%M:%S")
    ans = cad.set_index("incident_no")["call_answered"].map(loc)
    x = tr[(tr["review_type"] == "Primary") & (tr["first_compression_s"] != "")].copy()
    if dedup:
        x = x.drop_duplicates(dedup)
    x["fc"] = x["first_compression_s"].astype(int)
    if qa7_minsec:
        q = (x["reviewer"] == "QA7") & (x["fc"] >= 100)
        x.loc[q, "fc"] = (x.loc[q, "fc"] // 100) * 60 + x.loc[q, "fc"] % 100
    x["a"] = x["incident_no"].map(ans)
    x["s"] = (loc(x["recording_started"]) + pd.to_timedelta(x["fc"], unit="s") - x["a"]).dt.total_seconds()
    if trim:
        x = x[x["s"] <= trim]
    key = x["a"] if month_by == "answer" else loc(x["recording_started"])
    x["m"] = key.dt.strftime("%Y-%m")
    return {m: rq(statistics.median(x.loc[x["m"] == m, "s"]), "1") for m in MONTHS}


def ask_c(ch, tg911, drop_passed=False, dedup=None, drop_zero=False):
    """share of 911 calls answered within 15 seconds of arriving, over the calls answered, by local month (QA 1.2, 4.2)"""
    h = ch[ch["trunk_group"].isin(tg911)].copy()
    if dedup:
        h = h.drop_duplicates(dedup)
    if drop_passed:
        ends = set(zip(h["trunk_group"], h["ani"], h["released_utc"]))
        h = h[[(t, a, r) not in ends for t, a, r in zip(h["trunk_group"], h["ani"], h["arrived_utc"])]]
    arr = pd.to_datetime(h["arrived_utc"], utc=True)
    ans = pd.to_datetime(h["answered_utc"].replace("", None), utc=True)
    h = h.assign(m=ans.fillna(arr).dt.tz_convert(TZ).dt.strftime("%Y-%m"), wait=(ans - arr).dt.total_seconds())
    h = h[h["abandoned"] == "N"]
    if drop_zero:
        h = h[h["wait"] > 0]
    return {m: rq(100.0 * (h.loc[h["m"] == m, "wait"] <= 15).sum() / (h["m"] == m).sum(), "0.1") for m in MONTHS}


def digest(task):
    z = os.path.join(task, "target.zip")
    if os.path.exists(z):
        return "target.zip " + hashlib.md5(open(z, "rb").read()).hexdigest()
    t = os.path.join(task, "target")
    h = hashlib.md5()
    for f in sorted(os.listdir(t)):
        h.update(open(os.path.join(t, f), "rb").read())
    return "target/ " + h.hexdigest()


def main(task):
    target = os.path.join(task, "target")
    gold = json.load(open(os.path.join(task, "generator", "figures.json")))["asks"]
    gb, gc = gold["B"]["median_first_compression_s"], gold["C"]["answered_within_15s_pct"]
    hit_b = lambda f: {m: abs(f[m] - gb[m]) < 0.5 for m in MONTHS}
    hit_c = lambda f: {m: abs(f[m] - gc[m]) < 0.05 for m in MONTHS}
    cad, tr, ch, tg911 = load(target)
    print("pack:", digest(task))
    print("asks graded: %s (no Ask A)" % ", ".join(sorted(gold)))

    careful_b = [("careful: primary, coached, QA 5.1 clock, every time as seconds", {}),
                 ("+ exact duplicate reviews dropped", {"dedup": list(tr.columns)}),
                 ("+ near-exact duplicates dropped (incident, reviewer, compression)",
                  {"dedup": ["incident_no", "reviewer", "first_compression_s"]}),
                 ("+ times over ten minutes trimmed", {"trim": 600}),
                 ("+ months by the recording's start", {"month_by": "recording"})]
    careful_c = [("careful: 911 trunks, answered, local month answered, every record", {}),
                 ("+ exact duplicates dropped (every column but call_id)",
                  {"dedup": [c for c in ch.columns if c != "call_id"]}),
                 ("+ near-exact duplicates dropped (trunk, number, arrived)",
                  {"dedup": ["trunk_group", "ani", "arrived_utc"]}),
                 ("+ near-exact duplicates dropped (trunk, number, answered)",
                  {"dedup": ["trunk_group", "ani", "answered_utc"]}),
                 ("+ zero-second answers dropped", {"drop_zero": True})]
    kept_b = {m: False for m in MONTHS}
    kept_c = {m: False for m in MONTHS}
    print("\nAsk B, median time to first compression (12 figures, whole seconds): careful routes")
    for name, kw in careful_b:
        f = ask_b(cad, tr, **kw)
        h = hit_b(f)
        kept_b = {m: kept_b[m] or h[m] for m in MONTHS}
        off = [abs(f[m] - gb[m]) for m in MONTHS]
        print("  %-70s keeps %2d of 12 (off by %d to %d s)" % (name, sum(h.values()), min(off), max(off)))
    print("Ask C, share of 911 calls answered within 15 s (12 figures, one decimal): careful routes")
    for name, kw in careful_c:
        f = ask_c(ch, tg911, **kw)
        h = hit_c(f)
        kept_c = {m: kept_c[m] or h[m] for m in MONTHS}
        off = [abs(f[m] - gc[m]) for m in MONTHS]
        print("  %-70s keeps %2d of 12 (off by %.1f to %.1f)" % (name, sum(h.values()), min(off), max(off)))

    # the device audit: what each battery item finds on the device's rows, and why the cracker still misses
    q = tr[tr["first_compression_s"] != ""].copy()
    q["fc"] = q["first_compression_s"].astype(int)
    q7 = q[q["reviewer"] == "QA7"]
    rest = q[q["reviewer"] != "QA7"]
    h = ch[ch["trunk_group"].isin(tg911)]
    ends = set(zip(h["trunk_group"], h["ani"], h["released_utc"]))
    passed = sum((t, a, r) in ends for t, a, r in zip(h["trunk_group"], h["ani"], h["arrived_utc"]))
    exact = int(h.drop(columns=["call_id"]).duplicated().sum())
    near = int(h.duplicated(["trunk_group", "ani", "arrived_utc"]).sum())
    print("\nDevice audit")
    print("  B, QA7 keys minutes and seconds without the colon: the cracker reads first_compression_s as seconds by its "
          "name and executes QA 5.1 and 5.2; duplicate removal and trimming leave QA7's %d timed reviews in, and the "
          "keying shows only across reviewers (%d of QA7's times of 100 or more end in 60 to 99, against %d of the "
          "others'), a comparison no battery item makes: miss" %
          (len(q7), int(((q7["fc"] >= 100) & (q7["fc"] % 100 >= 60)).sum()),
           int(((rest["fc"] >= 100) & (rest["fc"] % 100 >= 60)).sum())))
    print("  C, a passed call's record arrives the second its first record was released: the cracker counts every record "
          "on the 911 trunks; exact duplicates %d, near-exact (trunk, number, arrived) %d, so the battery removes none "
          "of the %d passed records, which only chaining a number's records shows: miss" % (exact, near, passed))

    fb = ask_b(cad, tr, qa7_minsec=True)
    fc = ask_c(ch, tg911, drop_passed=True)
    full = sum(hit_b(fb).values()) + sum(hit_c(fc).values())
    sb = ask_b(cad, tr)
    sc = ask_c(ch, tg911)
    sheet = sum(hit_b(sb).values()) + sum(hit_c(sc).values())
    print("\nfull includer (QA7 as minutes and seconds, passed records out): %d of 24, figures.json %s" %
          (full, "reproduced" if full == 24 else "NOT reproduced"))
    print("sheet cracker (every time as seconds, every record a call): %d of 24" % sheet)

    n = 24
    kc = sum(kept_b.values()) + sum(kept_c.values())
    ks = kc                                       # the mirror reads the asks through the same routes
    lc, ls = kc / n, ks / n
    cracker = 38 + 7 + 55 * lc
    mirror = 5 + 7 + 55 * ls
    pair = (cracker + mirror) / 2
    both_on = 38 + 7 + 55 * lc
    whole = [a for a, k in (("B", kept_b), ("C", kept_c)) if all(k.values())]
    print("\ncracker (careful solver, on the call): keeps %d of %d ask figures (B %d, C %d): %.1f" %
          (kc, n, sum(kept_b.values()), sum(kept_c.values()), cracker))
    print("mirror (on R0, the release): keeps %d of %d ask figures: %.1f" % (ks, n, mirror))
    print("mirror leakage: %.1f per cent of ask weight; asks whole for the mirror: %s" %
          (100 * ls, ", ".join(whole) or "none"))
    print("pair ceiling: %.1f (bar 60)" % pair)
    print("two careful responses on the call: %.1f each, pair %.1f (bar 70)" % (both_on, both_on))
    ok = kc == 0 and 100 * ls < 50 and not whole and pair <= 60 and both_on < 70 and full == n
    print("verdict:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
