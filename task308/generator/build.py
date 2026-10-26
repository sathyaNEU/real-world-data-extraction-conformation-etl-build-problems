"""Cut the task308 pack: the claims extract, the exposure extract, the rebuild cost index, the business plan, the
brokers' quotations, the valuation basis, the event definitions, the claims operations report, the Major Loss Unit's
monthly reports, the Lowther and Pike bordereaux, the direct book on 31 December 2025 and the two distractors."""
import datetime as dt
import os

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import docs
import params as P
import postprocess as PP
import records as R

F = P.FILES
PACK = list(F)
DISTRACTORS = list(P.DISTRACTORS)
CONTEXT = ["plan"]
# who issued each document and the day it was saved: the producer and date its container carries (H1)
ISSUED = {"quotes": (P.BROKER, "2026-11-18", None), "basis": (P.ORG, "2024-03-21", None),
          "events": (P.ORG, "2023-12-14", None), "ops": (P.ORG, "2026-02-17", None), "group": (P.ORG, "2026-01-09", None),
          "plan": (P.ORG, "2026-10-29", "Anne Shah"), "index": (P.INDEX_HOUSE, "2026-10-14", P.INDEX_HOUSE),
          "mlu": (P.ORG, "2026-11-06", "Nicholas Hardy")}


def seal(target):
    for k, (who, day, person) in ISSUED.items():
        p = os.path.join(target, F[k])
        PP.scrub(p, who, day)
        if p.endswith(".xlsx"):
            PP.finish_office(p, "%sT08:47:00Z" % day, "%sT16:12:00Z" % day, who, person=person)


def build(target, seed=P.SEED):
    os.makedirs(target, exist_ok=True)
    rec = R.build(seed)
    c = rec["claims"]
    out = c[["claim_ref", "policy_ref", "region", "postcode_district", "peril", "date_of_loss", "date_notified",
             "event_code", "status", "paid", "outstanding", "repair_contractor", "repair_signed_off"]].copy()
    out["event_code"] = out["event_code"].fillna("")
    for col in ("date_of_loss", "date_notified", "repair_signed_off"):
        out[col] = pd.to_datetime(out[col])
    out["paid"] = out["paid"].astype(float).round(2)
    out["outstanding"] = out["outstanding"].astype(float).round(2)
    # written through Arrow with no pandas schema block, as the claims platform's export writes it
    tb = pa.Table.from_pandas(out, preserve_index=False).replace_schema_metadata(None)
    tb = tb.cast(pa.schema([pa.field(f.name, pa.string() if pa.types.is_large_string(f.type) else f.type)
                            for f in tb.schema]))
    pq.write_table(tb, os.path.join(target, F["claims"]), compression="snappy", store_schema=False)
    rec["exposure"].to_csv(os.path.join(target, F["exposure"]), index=False, lineterminator="\n")
    B = rec["bdx"].copy()
    for col in ("term_start", "term_end", "cancellation_effective", "endorsement_effective"):
        B[col] = [x.strftime("%d/%m/%Y") if isinstance(x, dt.date) else "" for x in B[col]]
    B["cancellation_reason"] = B["cancellation_reason"].fillna("")
    B["annual_premium"] = B["annual_premium"].map(lambda v: "%.2f" % v)
    B.to_csv(os.path.join(target, F["bdx"]), index=False, lineterminator="\n")
    rec["direct"].to_csv(os.path.join(target, F["direct"]), index=False, lineterminator="\n")
    rec["flood"].to_csv(os.path.join(target, F["flood"]), index=False, lineterminator="\n")
    ex = rec["exposure"]
    pol25 = ex[ex.year == 2025].groupby("region").policies_in_force_mid_year.sum().to_dict()
    docs.plan(os.path.join(target, F["plan"]), pol25)
    docs.index(os.path.join(target, F["index"]), rec["index"])
    docs.mlu(os.path.join(target, F["mlu"]), rec["mlu_sheets"])
    docs.quotes(os.path.join(target, F["quotes"]))
    docs.basis(os.path.join(target, F["basis"]))
    docs.events(os.path.join(target, F["events"]))
    rep = c[(pd.to_datetime(c.date_of_loss).dt.year == 2025) & (pd.to_datetime(c.date_notified) <= pd.Timestamp("2026-01-31"))]
    docs.ops(os.path.join(target, F["ops"]), rep)
    docs.group(os.path.join(target, F["group"]))
    seal(target)
    return rec
