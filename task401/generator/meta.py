"""task401 metadata.json: every input file with its description, date, source and licence, and the distractors."""
import json, os
TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'Synthetic records generated for this task by its generator (no real trust\'s or council\'s data); CC0 1.0.'
D = {
 'membership_register_2026-03-16.csv': ('Membership system register extract: every membership on the books since January 2024', '2026-03-16'),
 'access_weekly_usage_2024-01-01_to_2026-03-15.parquet': ('Access-control weekly usage export, gate entries per membership per week', '2026-03-16'),
 'cancellation_requests_2024-01-01_to_2026-03-15.csv': ('Cancellation requests received by the membership team, all channels', '2026-03-16'),
 'legacy_terms_letters_2026-02.xlsx': ('Mailing log of the February 2026 legacy terms letters, with returned post', '2026-02-27'),
 'member_care_calls_2026-02-16_to_2026-03-13.csv': ('Member care team call log', '2026-03-16'),
 'class_bookings_2024-10-07_to_2026-03-15.parquet': ('Class booking system extract', '2026-03-16'),
 'savings_programme_2025-26.docx': ('Board paper: the savings programme and its service changes', '2025-12-09'),
 'operating_contract_schedule_4.pdf': ('Leisure operating contract, Schedule 4 (performance, reporting and review)', '2024-03-18'),
 'membership_terms_2025-26.pdf': ('Membership terms for the 2025-26 membership year', '2025-01-27'),
 'price_list_2025-26.xlsx': ('Price list: membership fees, pay-as-you-go tickets and charges', '2025-01-27'),
 'dd_bureau_A_submissions_2025-09-30_to_2025-12-11.csv': ('Direct Debit submissions report from the bureau used to November 2025', '2025-12-12'),
 'dd_collections_2025-12-01_to_2026-03-13.csv': ('Direct Debit collections report from the bureau used from December 2025', '2026-03-16'),
 'dd_mandates_2026-03-16.csv': ('Direct Debit mandates held by the new bureau', '2026-03-16'),
 'bacs_returns_2025-10_to_2026-03.csv': ('BACS returned collections (ARUDD) from both bureaux', '2026-03-16'),
 'direct_debit_bureau_change_2025-11.pdf': ('Letter to members on the Direct Debit bureau change', '2025-11-03'),
 'till_sales_old_system_2025-10-01_to_2025-11-30.csv': ('Reception till sales report from the old tills', '2025-12-01'),
 'epos_sales_2025-11-01_to_2026-03-15.csv': ('EPOS sales lines from the new reception tills', '2026-03-16'),
 'epos_go_live_notice_2025-10.docx': ('IT and Facilities notice of the EPOS go-live dates and site codes', '2025-10-20'),
 'pool_closures_2025-10-01_to_2026-03-15.csv': ('Duty managers\' log of the times each pool was shut', '2026-03-16'),
 'member_survey_autumn_2025.xlsx': ('Autumn 2025 member satisfaction survey responses', '2025-11-17'),
 'joining_offers_2025-26.xlsx': ('Marketing log of joining offers', '2026-01-28'),
}
def run():
    files = sorted(os.listdir(os.path.join(TASK, 'target')))
    assert set(files) == set(D), set(files) ^ set(D)
    meta = {'task': 'task401', 'organisation': 'Wrenford Leisure Trust and Wrenford Borough Council (invented)',
            'files': [dict(file=f, description=D[f][0], date=D[f][1], source=SRC, license='CC0-1.0') for f in files],
            'distractors': [
                dict(file='member_survey_autumn_2025.xlsx', why='satisfaction and value scores by centre and tariff group read as a measure of which members are unhappy; the review counts cancellations, and the survey predates the changes'),
                dict(file='joining_offers_2025-26.xlsx', why='the January 2026 no-joining-fee offer reads as a cause of the February movement among new members; no change in the review is an offer, and the comparison runs on the members each change applies to')],
            'wrong_basis_distractors': [],
            'deliverables': ['change_review.pdf', 'monthly_return.xlsx']}
    json.dump(meta, open(os.path.join(TASK, 'metadata.json'), 'w'), indent=1, ensure_ascii=False)
    return len(files)


if __name__ == '__main__':
    print(run())
