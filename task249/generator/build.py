"""Write task249's target folder from the World and its Records."""
import os
import numpy as np
import pandas as pd
import params as P
import records as RC
import docs as D
import dictionary

FILES = {
    "sessions": "web_sessions_2028q4.parquet",
    "register": "signin_device_register_2028q4.csv",
    "accounts": "reader_accounts.csv",
    "paywall": "paywall_wall_log_2028q4.xlsx",
    "report": "platform_users_by_month_2028.xlsx",
    "editions": "editions.csv",
    "policy": "audience_policy_2029.pdf",
    "tag": "analytics_tag_notes.pdf",
    "paynotes": "paywall_and_accounts_notes.pdf",
    "subs": "circulation_subscriptions_2028q4.csv",
    "susp": "circulation_suspensions_2028q4.csv",
    "epaper": "epaper_accesses_2028q4.csv",
    "single": "single_copy_sales_2028q4.csv",
    "points": "retail_points.csv",
    "nl_contacts": "newsletter_contacts_2029-01-15.csv",
    "nl_log": "newsletter_activity_log.csv",
    "nl_groups": "newsletter_group_changes.csv",
    "ads": "ad_delivery_2028q4.csv",
    "reach": "media_analysis_2028_reach.csv",
    "dictionary": "DATA_DICTIONARY.md",
    "deliv_xlsx": "media_kit_2029_edition_figures.xlsx",
    "deliv_pdf": "measurement_note_2029.pdf",
}
DISTRACTORS = [FILES["ads"], FILES["reach"]]

_CACHE = {}


def records():
    if "r" not in _CACHE:
        _CACHE["r"] = RC.build()
    return _CACHE["r"]


def _parquet(df, path):
    import pyarrow as pa
    import pyarrow.parquet as pq
    schema = pa.schema([("client_id", pa.string()), ("session_start", pa.timestamp("s", tz="UTC")),
                        ("session_end", pa.timestamp("s", tz="UTC")), ("content_group", pa.string()),
                        ("page_views", pa.int16()), ("user_agent", pa.string()), ("device_category", pa.string()),
                        ("browser", pa.string()), ("os", pa.string()), ("ip_prefix", pa.string()),
                        ("user_ref", pa.string()), ("is_bot", pa.bool_())])
    d = df.copy()
    d["session_start"] = pd.to_datetime(d["session_start"]).dt.tz_localize("UTC")
    d["session_end"] = pd.to_datetime(d["session_end"]).dt.tz_localize("UTC")
    d["user_ref"] = d["user_ref"].where(d["user_ref"].notna(), None).astype(object)
    t = pa.Table.from_pandas(d, schema=schema, preserve_index=False).replace_schema_metadata(None)
    pq.write_table(t, path, compression="zstd", compression_level=9, use_dictionary=True, row_group_size=4_000_000,
                   data_page_version="1.0", write_statistics=True)


def _csv(df, path, ts=()):
    d = df.copy()
    for c in ts:
        d[c] = pd.to_datetime(d[c]).dt.strftime("%Y-%m-%d %H:%M:%S")
    d.to_csv(path, index=False, lineterminator="\n")


def run(target):
    os.makedirs(target, exist_ok=True)
    R = records()
    X = R.export()
    _parquet(X, os.path.join(target, FILES["sessions"]))
    G = R.register()
    _csv(G, os.path.join(target, FILES["register"]), ts=("first_signed_in", "last_signed_in"))
    A = R.accounts()
    _csv(A, os.path.join(target, FILES["accounts"]), ts=("created",))
    PW = R.paywall()
    D.paywall_xlsx(os.path.join(target, FILES["paywall"]), PW)
    D.report_xlsx(os.path.join(target, FILES["report"]), R.report(X))
    D.editions_table().to_csv(os.path.join(target, FILES["editions"]), index=False, lineterminator="\n")
    D.policy(os.path.join(target, FILES["policy"]))
    D.tag_notes(os.path.join(target, FILES["tag"]))
    D.paywall_notes(os.path.join(target, FILES["paynotes"]))
    S_, U_, A_, T_, X_ = R.circulation()
    for df, key, cols in ((S_, "subs", ("start_date", "end_date")), (U_, "susp", ("from_date", "to_date")),
                          (A_, "epaper", ("start_date", "end_date")), (X_, "single", ("issue_date",))):
        d = df.copy()
        for c in cols:
            d[c] = pd.to_datetime(d[c]).dt.strftime("%Y-%m-%d")
        d.to_csv(os.path.join(target, FILES[key]), index=False, lineterminator="\n")
    T_.to_csv(os.path.join(target, FILES["points"]), index=False, lineterminator="\n")
    Ct, Et, Gt = R.newsletter_tables()
    _csv(Ct, os.path.join(target, FILES["nl_contacts"]), ts=("first_optin_utc", "last_changed_utc"))
    _csv(Et, os.path.join(target, FILES["nl_log"]), ts=("at_utc",))
    _csv(Gt, os.path.join(target, FILES["nl_groups"]), ts=("changed_utc",))
    ads = R.ad_delivery()
    ads["date"] = pd.to_datetime(ads["date"]).dt.strftime("%Y-%m-%d")
    ads.to_csv(os.path.join(target, FILES["ads"]), index=False, lineterminator="\n")
    R.reach_survey().to_csv(os.path.join(target, FILES["reach"]), index=False, lineterminator="\n")
    dictionary.write(os.path.join(target, FILES["dictionary"]), FILES)
    return R
