"""The shipped tables as frames: the agreements export and the pilot sheet, in the columns the files carry."""
import pandas as pd

BOOK_COLS = ["agreement_ref", "account_id", "account_name", "urn", "dfe_number", "companies_house_no", "billing_basis",
             "price_band", "pupils_billed", "annual_value_gbp", "agreement_start", "term_start", "term_end",
             "end_date", "status", "signed_by", "signed_by_contact_id", "signed_by_role", "signed_on"]


def book_frame(rows):
    out = []
    for x in rows:
        out.append(dict(agreement_ref=x["agreement_ref"], account_id=x["account_id"], account_name=x["account_name"],
                        urn=x["urn"], dfe_number=x["dfe_number"], companies_house_no=x.get("trust_ch"),
                        billing_basis=x["billing_basis"], price_band=x["price_band"],
                        pupils_billed=x["stale"]["pupils"] if x.get("stale") else x["pupils_billed"],
                        annual_value_gbp=x["stale"]["value"] if x.get("stale") else x["annual_value_gbp"],
                        agreement_start=x["agreement_start"],
                        term_start=x["current_term_start"], term_end=x["current_term_end"],
                        end_date=x.get("end_date"), status=x["status"], signed_by=x["signed_by"],
                        signed_by_contact_id=x["signed_by_contact_id"], signed_by_role=x["signed_by_role"],
                        signed_on=x["signed_on"]))
    b = pd.DataFrame(out, columns=BOOK_COLS)
    b["urn"] = b["urn"].astype("Int64")
    for c in ["agreement_start", "term_start", "term_end", "end_date", "signed_on"]:
        b[c] = pd.to_datetime(b[c]).dt.strftime("%Y-%m-%d")
    return b.sort_values(["account_name", "agreement_ref"]).reset_index(drop=True)


def pilot_frame(reg, licences):
    rows = []
    for L in licences:
        uid = L["uid"]
        rows.append(dict(trust=reg.group_name[uid], companies_house_no=reg.group_ch.get(uid),
                         academies_priced=L["academies"], pupils_priced=L["pupils"],
                         licence_value_gbp=L["licence_value"], agreements_replaced=L["replaced_n"],
                         agreements_replaced_value_gbp=L["replaced_value"],
                         net_new_recurring_revenue_gbp=L["net"], outcome=L["outcome"]))
    return pd.DataFrame(rows)
