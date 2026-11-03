"""The ask layer measured on the cut pack: the 30 graded ask figures (each 2026 quarter's large cash transaction
reports required, filed and filed late for the segment, and each branch's 2026 segment cash through its deposit
ATMs and in its night depository) under the golden's handling and under the handlings a response is likely to take,
scored figure by figure (a hit is the figure at the stated rounding), and the pair ceiling those keeps imply.

    python3 task188/generator/ceiling.py

The cracker lands the call and executes every filed rule: the programme's 24-hour window across accounts and
channels with a night deposit received when counted, each report reference once, Corrections not new reports, the
log's own member field for the segment and its transaction date as the day the cash came in, each terminal at the
site it stood at on the day, and each night bag at the branch the bag register issued it from. The mirror is off
the call and takes the same asks with one row per terminal.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import analysis as A  # noqa: E402

TARGET = os.path.join(os.path.dirname(HERE), "target")

HANDLINGS = {
    "golden": {},
    "cracker": dict(key="member", late_from="transaction", night="bag_register"),
    "mirror": dict(key="member", late_from="transaction", night="bag_register", atm="last"),
    "naive": dict(req="member_bizday", key="member", late_from="transaction", dedupe=False, atm="last", night="home"),
    "account_key_only": dict(late_from="transaction", night="bag_register"),
    "receipt_day_only": dict(key="member", night="bag_register"),
    "both_lctr_devices_read": dict(night="bag_register"),
    "manifest_only": dict(key="member", late_from="transaction"),
    "every_device_read": {},
    "windows_per_account": dict(req="account_window"),
    "one_report_per_business_day": dict(req="member_bizday"),
    "one_report_per_account_day": dict(req="account_bizday"),
    "pacific_calendar_day": dict(req="member_localday"),
    "quarter_on_utc": dict(qclock="utc"),
    "every_original_row": dict(dedupe=False),
    "quarter_submitted": dict(by="submitted"),
    "terminal_last_row": dict(atm="last"),
    "terminal_first_row": dict(atm="first"),
    "night_home_branch": dict(night="home"),
    "night_account_domicile": dict(night="domicile"),
    "night_cash_centre_left_out": dict(night="drop"),
}


def figures(target, p, mem, acc, req="window", qclock="pacific", key="account", late_from="receipt", by="transaction",
            dedupe=True, atm="asof", night="manifest"):
    f = {}
    rq, _ = A.lctr_required(p, mem, how=req, quarter_clock=qclock)
    fl, lt = A.lctr_filed(target, mem, acc, p, key=key, late_from=late_from, by=by, dedupe=dedupe)
    for q in (1, 2, 3, 4):
        f["lctr.q%d.required" % q] = rq[q]
        f["lctr.q%d.filed" % q] = fl[q]
        f["lctr.q%d.late" % q] = lt[q]
    bc = A.branch_cash(target, p, night=night, atm=atm, mem=mem, acc=acc)
    for b, v in bc.items():
        f["branch.%s.atm" % b] = int(round(v["atm"] / 1000.0)) * 1000
        f["branch.%s.night" % b] = int(round(v["night"] / 1000.0)) * 1000
    return f


def measure(target=TARGET):
    p, mem, acc = A.load(target)
    gold = figures(target, p, mem, acc)
    keeps = {}
    for name, kw in HANDLINGS.items():
        f = figures(target, p, mem, acc, **kw)
        hit = [k for k in gold if f[k] == gold[k]]
        keeps[name] = (len(hit), hit, f)
    return gold, keeps


def pair(keep_c, keep_m, total, call=45.0, miss=12.0):
    """the pair ceiling: the cracker on the call, the mirror off it, each keeping its share of 55 ask points"""
    return ((call + 55.0 * keep_c / total) + (miss + 55.0 * keep_m / total)) / 2


def block(hit, prefix):
    return sum(1 for k in hit if k.startswith(prefix))


if __name__ == "__main__":
    gold, keeps = measure()
    n = len(gold)
    print("graded ask figures:", n)
    for k, (v, hit, f) in keeps.items():
        print("  %-30s keeps %2d of %d  (lctr %d of 12, branch %d of 18)" % (
            k, v, n, block(hit, "lctr"), block(hit, "branch")))
    kc, km = keeps["cracker"][0], keeps["mirror"][0]
    print("cracker keeps %.1f per cent of ask weight, mirror %.1f per cent; pair ceiling %.1f" % (
        100.0 * kc / n, 100.0 * km / n, pair(kc, km, n)))
