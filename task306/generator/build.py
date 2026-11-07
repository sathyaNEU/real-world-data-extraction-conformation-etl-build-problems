"""Build task306's pack, goldens, figures.json, submission.md and metadata.json twice, require byte-identical output,
cut target.zip, then run the checks and the verifier.

    python3 task306/generator/build.py
"""
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import docs as D    # noqa: E402
import golden as GD  # noqa: E402
import pack as PK   # noqa: E402
import world as W   # noqa: E402

STAMP = (2026, 12, 1, 7, 15, 0)
SOURCES = {
    "master": "the dealing desk's security master (SEDOL, ISIN, index band, corporate actions)",
    "market": "an exchange data vendor's daily closes and volumes for the London market",
    "backtests": "a quantitative research team's backtest summary workbook",
    "trades": "a backtest engine's rebalance trade log",
    "orders": "an order management system's order blotter export",
    "fills": "an order management system's fill (execution) export",
    "accounts": "a dealing desk's trading account register",
    "policy": "an investment committee's capital allocation policy",
    "tca": "a dealing desk's transaction cost analysis standard",
    "request": "the chief investment officer's email",
    "commissions": "a dealing desk's broker commission schedule",
    "esg": "an asset manager's ESG exclusion list",
    "allocations": "an order management system's post-trade block allocation export",
}


def build_pack(out):
    os.makedirs(out, exist_ok=True)
    f = lambda k: os.path.join(out, PK.FILES[k])
    univ = W.universe()
    days = W.trading_days()
    mkt, cons, month_end = W.market(univ, days)
    cands = W.candidates(univ, days, month_end)
    orders = W.live_orders(univ, mkt, days, month_end)
    n = {}
    PK.write_master(univ, cons, f("master"))
    n["market"] = PK.write_market(mkt, univ, f("market"))
    PK.write_backtests(f("backtests"))
    PK.write_trades(cands, f("trades"))
    n["fills"] = PK.write_orders_fills(orders, f("orders"), f("fills"))
    PK.write_allocations(orders, f("allocations"))
    PK.write_accounts(f("accounts"))
    PK.write_esg(univ, f("esg"))
    PK.write_commissions(f("commissions"))
    D.policy(f("policy"))
    D.tca(f("tca"))
    D.request(f("request"))
    t = dt.datetime(*STAMP).timestamp()
    for k in PK.FILES:
        os.utime(f(k), (t, t))
    return n


def metadata(n):
    meta = {"task": "task306", "architecture": 4, "as_of": "2026-12-01",
            "files": {PK.FILES[k]: {"source": SOURCES[k], "date": "2026-12-01", "license": "synthetic, CC0",
                                    "role": "distractor" if k in PK.DISTRACTORS else "evidence"}
                      for k in PK.FILES},
            "distractors": [PK.FILES[k] for k in PK.DISTRACTORS],
            "largest_file": {"name": PK.FILES["market"], "rows": n["market"]},
            "fills_rows": n["fills"],
            "deliverables": [GD.DECK, GD.BOOK]}
    return meta


def digest(folder):
    h = {}
    for root, _d, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def one_build(base):
    target, golden = os.path.join(base, "target"), os.path.join(base, "golden")
    n = build_pack(target)
    R, fig = GD.write_all(target, golden, base)
    json.dump(fig, open(os.path.join(base, "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump(metadata(n), open(os.path.join(base, "metadata.json"), "w"), indent=1, sort_keys=True)
    return digest(base), fig


def cut_zip(target, path):
    t = STAMP
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=t)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, fn), "rb").read())


def main():
    a, b = tempfile.mkdtemp(), tempfile.mkdtemp()
    ha, fig = one_build(a)
    hb, _ = one_build(b)
    same = ha == hb
    print("two builds byte-identical:", same, "(%d files)" % len(ha))
    if not same:
        for k in sorted(set(ha) | set(hb)):
            if ha.get(k) != hb.get(k):
                print("  differs:", k)
        sys.exit(1)
    for sub in ("target", "golden"):
        dst = os.path.join(TASK, sub)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(a, sub), dst)
    shutil.copy(os.path.join(a, "figures.json"), os.path.join(HERE, "figures.json"))
    shutil.copy(os.path.join(a, "metadata.json"), os.path.join(TASK, "metadata.json"))
    shutil.copy(os.path.join(a, "submission.md"), os.path.join(TASK, "submission.md"))
    shutil.rmtree(a)
    shutil.rmtree(b)
    zp = os.path.join(TASK, "target.zip")
    cut_zip(os.path.join(TASK, "target"), zp)
    print("target.zip sha256", hashlib.sha256(open(zp, "rb").read()).hexdigest())
    print("call", fig["call"], "runner-up", fig["runner_up"], "gap", fig["gap_gbp_m"])
    for script in ("checks.py", "verify.py"):
        p = os.path.join(HERE, script)
        if os.path.exists(p):
            rc = subprocess.call([sys.executable, p])
            print(script, "exit", rc)
            if rc:
                sys.exit(rc)


if __name__ == "__main__":
    main()
