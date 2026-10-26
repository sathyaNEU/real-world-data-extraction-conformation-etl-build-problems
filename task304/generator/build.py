"""Cut the task304 pack: the records, the documents and the two distractor files."""
import os

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import docs
import params as P
import records as R
import world as W

F = P.FILES
PACK = list(F)
DISTRACTORS = ("hpi", "contacts", "appetite", "ratecard")
CONTEXT = ("plan", "policy", "pilot")


def _parquet(df, path):
    # written through Arrow with no pandas schema block, as the mortgage platform's export writes it
    tb = pa.Table.from_pandas(df, preserve_index=False).replace_schema_metadata(None)
    tb = tb.cast(pa.schema([pa.field(f.name, pa.string() if pa.types.is_large_string(f.type) else f.type)
                            for f in tb.schema]))
    pq.write_table(tb, path, compression="snappy", store_schema=False)


def planning_rates(hist, reg):
    """each book's share of the accounts first reaching two payments in arrears from January 2022 to March 2025 that
    were possessed within 18 months of that month (plan paper, section 3)"""
    h = hist.drop_duplicates()
    m = h.period.str[:4].astype(int) * 12 + h.period.str[5:7].astype(int) - 1
    h = h.assign(m=m).sort_values(["account_number", "m"])
    pia = np.floor(h.arrears_balance / h.contractual_payment.where(h.contractual_payment > 0) + 1e-9).fillna(0)
    same = h.account_number.eq(h.account_number.shift())
    prev = np.where(same, pia.shift(), 0)
    ent = h[(pia >= 2).to_numpy() & (prev < 2) & (h.account_status == "Live").to_numpy()]
    lo = int(P.RATE_WINDOW[0][:4]) * 12 + int(P.RATE_WINDOW[0][5:]) - 1
    hi = int(P.RATE_WINDOW[1][:4]) * 12 + int(P.RATE_WINDOW[1][5:]) - 1
    ent = ent[(ent.m >= lo) & (ent.m <= hi)].groupby("account_number").first().reset_index()
    d = pd.to_datetime(reg.possession_date, format="%d/%m/%Y")
    pm = pd.Series((d.dt.year * 12 + d.dt.month - 1).to_numpy(), index=reg.account_number.to_numpy())
    pm = pm[~pm.index.duplicated()]          # a further advance's loan part shares its account's possession
    pmm = ent.account_number.map(pm)
    ent["y"] = (pmm >= ent.m) & (pmm - ent.m <= P.POSS_HORIZON)
    return ent.groupby("book").y.mean().to_dict(), ent.groupby("book").size().to_dict()


def pilot_table(hist, lit, recv):
    """the pilot report's table, from the records: the borrowers whose account first reached two payments in arrears
    in 2024, counting from fewer than two, with no claim for possession or receiver appointment on record by that
    month, split on the account number's last digit; how many reached four payments in arrears, and how many had a
    claim issued, within 12 months"""
    h = hist.drop_duplicates()
    m = h.period.str[:4].astype(int) * 12 + h.period.str[5:7].astype(int) - 1
    h = h.assign(m=m).sort_values(["account_number", "m"])
    pia = np.floor(h.arrears_balance / h.contractual_payment.where(h.contractual_payment > 0) + 1e-9).fillna(0)
    same = h.account_number.eq(h.account_number.shift()).to_numpy()
    prev = np.where(same, pia.shift(), 0)
    ent = h[(pia >= 2).to_numpy() & (prev < 2) & (h.account_status == "Live").to_numpy()
            & (h.m >= P.PILOT[0]).to_numpy() & (h.m <= P.PILOT[1]).to_numpy()].groupby("account_number").m.min()
    cd = pd.to_datetime(lit.loc[lit.action == "Claim issued", "action_date"], format="%Y-%m-%d")
    claims = pd.DataFrame({"account_number": lit.loc[lit.action == "Claim issued", "account_number"].astype(str),
                           "c": (cd.dt.year * 12 + cd.dt.month - 1).to_numpy()})
    rd = pd.to_datetime(recv.date_appointed, format="%d/%m/%Y")
    first_rec = pd.Series((rd.dt.year * 12 + rd.dt.month - 1).to_numpy(), index=recv.account_number.astype(str)).groupby(level=0).min()
    first_claim = claims.groupby("account_number").c.min()
    e = pd.DataFrame({"account_number": ent.index, "m": ent.to_numpy()})
    on_record = (e.account_number.map(first_claim) <= e.m) | (e.account_number.map(first_rec) <= e.m)
    e = e[~on_record.to_numpy()]
    four = h[(pia >= 4).to_numpy()][["account_number", "m"]].merge(e, on="account_number", suffixes=("_x", ""))
    four = set(four.account_number[(four.m_x > four.m) & (four.m_x <= four.m + 12)])
    cl = claims.merge(e, on="account_number")
    cl = set(cl.account_number[(cl.c >= cl.m) & (cl.c <= cl.m + 12)])
    team = e.account_number.str[-1].astype(int) % 2 == 0
    out = {}
    for name, g in (("team", e[team.to_numpy()]), ("usual", e[~team.to_numpy()])):
        out[name + "_n"] = int(len(g))
        out[name + "_four"] = int(g.account_number.isin(four).sum())
        out[name + "_claim"] = int(g.account_number.isin(cl).sum())
    return out


def build(target, seed=P.SEED):
    os.makedirs(target, exist_ok=True)
    r = R.build(seed)
    _parquet(r["bk"], os.path.join(target, F["book"]))
    _parquet(r["hist"], os.path.join(target, F["history"]))
    reg = r["poss"][["account_number", "book", "possession_date", "route", "debt_at_possession"]]
    reg.to_csv(os.path.join(target, F["possessions"]), index=False, lineterminator="\n")
    r["sales"].to_csv(os.path.join(target, F["sales"]), index=False, lineterminator="\n")
    r["recv"].to_csv(os.path.join(target, F["receivers"]), index=False, lineterminator="\n")
    r["lit"].to_csv(os.path.join(target, F["litigation"]), index=False, lineterminator="\n")
    rates, _ = planning_rates(r["hist"], reg)
    docs.plan(os.path.join(target, F["plan"]), rates)
    docs.pilot(os.path.join(target, F["pilot"]), pilot_table(r["hist"], r["lit"], r["recv"]))
    docs.policy(os.path.join(target, F["policy"]))
    docs.appetite(os.path.join(target, F["appetite"]))
    docs.ratecard(os.path.join(target, F["ratecard"]))
    docs.dictionary(os.path.join(target, F["dictionary"]))
    hp = []
    for k in range(6):
        for m in range(W.ym(2010, 1), W.SNAP + 1):
            hp.append(("%d-%02d" % (m // 12, m % 12 + 1), P.REGION_NAMES[k], " ".join(P.REGION_PC[k]),
                       round(float(W.hpi(m, k) / W.hpi(W.ym(2010, 1), k) * 100), 1)))
    pd.DataFrame(hp, columns=["month", "area", "postcode_districts", "index_jan2010_100"]).to_csv(
        os.path.join(target, F["hpi"]), index=False, lineterminator="\n")
    rng = np.random.default_rng(seed + 11)
    rows = []
    reasons = ["Payment query", "Arrears and difficulty", "Product switch", "Redemption statement", "Overpayment", "Other"]
    base = {"Payment query": 2100, "Arrears and difficulty": 640, "Product switch": 1500,
            "Redemption statement": 900, "Overpayment": 420, "Other": 700}
    for mo in range(1, 13):
        for rs in reasons:
            rows.append(("2025-%02d" % mo, rs, int(base[rs] * rng.uniform(0.85, 1.15)), round(float(rng.uniform(4.0, 11.0)), 1)))
    pd.DataFrame(rows, columns=["month", "contact_reason", "calls_answered", "average_handle_minutes"]).to_csv(
        os.path.join(target, F["contacts"]), index=False, lineterminator="\n")
    return r
