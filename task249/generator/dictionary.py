"""DATA_DICTIONARY.md for task249's target folder."""
import params as P

TEXT = """# Data dictionary

{org}, audience data. Files gathered on 15 January 2029 for the 2029 media kit, which quotes the fourth quarter of
2028 (October to December). Times marked UTC are UTC; everything else is Berlin time unless a file says otherwise.

## {sessions}
The analytics platform's export of the quarter's sessions on rhenhagener-anzeiger.de, one row per session, ordered by
client_id and session start.

| column | meaning |
|---|---|
| client_id | the analytics tag's identifier (see analytics_tag_notes.pdf) |
| session_start, session_end | first and last hit of the session, UTC |
| content_group | the edition, from the page's path |
| page_views | pages viewed in the session |
| user_agent | the browser's user-agent string |
| device_category, browser, os | the platform's reading of the user agent |
| ip_prefix | the visitor's address with its last part set to zero |
| user_ref | hashed account number while the reader is signed in, else empty |
| is_bot | the platform's automated-traffic flag |

## {register}
The reader-account service's sign-in register for the quarter: one row per account, device and client_id seen while
signed in.

| column | meaning |
|---|---|
| account_no | reader account |
| device_id | the account service's login cookie on one browser |
| client_id | an analytics identifier the browser carried while signed in |
| first_signed_in, last_signed_in | first and last signed-in session with that client_id, UTC |
| signed_in_sessions | signed-in sessions with that client_id |

## {accounts}
Reader accounts as of 15 January 2029: account_no, created (UTC), origin (registration, digital subscription, print
subscription), home_edition, status, subscriber_no (print subscriptions).

## {paywall}
The paywall console's log of the walls shown in the quarter: shown, client_id, edition, outcome, meter_started.

## {report}
The analytics platform's monthly report of users (distinct client_ids) by content group for 2028.

## {editions}
The twelve editions: code, name, state, district, households (census 2022), former content group.

## {policy}, {tag}, {paynotes}
The audience figures' definitions; the analytics tag and its export; the paywall, accounts and sign-in.

## {subs}
The circulation system's print subscriptions active at some time in the quarter.

| column | meaning |
|---|---|
| sub_no | subscription number, issued in order as subscriptions are entered |
| customer_no | customer |
| edition | the edition delivered |
| product | DAILY (Monday to Saturday), SATURDAY (the Saturday paper only), COMBI (Monday to Saturday, with the e-paper), TRIAL (two weeks) |
| copies | copies a day |
| start_date, end_date | first and last day of delivery (end_date empty: open); subscriptions taken over when the system went live carry 4 January 1999 |
| monthly_price_eur | price a month |

## {susp}
Suspensions in the quarter: sub_no, from_date, to_date (both included), kind (pause, forward, donation).

## {epaper}
The e-paper platform's accesses active at some time in the quarter: access_id, edition, plan, start_date, end_date
(empty: open), price_eur (a month; Digital Annual a year), order_ref (the shop's or app store's order), channel.

## {single}
The wholesaler's single-copy figures for each issue of the quarter at each retail point: issue_date, retail_point,
delivered, returned.

## {points}
Retail points: retail_point, edition, type.

## {nl_contacts}
The newsletter platform's contact export, taken 15 January 2029 at 06:12 UTC.

| column | meaning |
|---|---|
| contact_id | contact |
| email_md5 | hashed address (MD5 of the lower-case address) |
| status | subscribed, unsubscribed, cleaned (address bounced), pending (not confirmed) |
| groups | the editions' newsletters the contact receives, separated by a vertical bar |
| first_optin_utc | when the contact first signed up |
| last_changed_utc | the last change to the contact's record |
| source | where the contact signed up |

## {nl_log}
The platform's activity log (it keeps six months): contact_id, event (subscribed, confirmed, unsubscribed, cleaned,
resubscribed, clicked), at_utc, link (the address of a link clicked in a newsletter).

## {nl_groups}
Changes contacts made to their groups in the preference centre in the same six months: contact_id, changed_utc,
groups_before, groups_after.

## {ads}
The ad server's daily delivery by edition and device: impressions served and viewable, eCPM.

## {reach}
The Media-Analyse 2028 extract by edition: readers per issue, reach, median reader age, interviews.
"""


def write(path, files):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(TEXT.format(org=P.ORG, **files))
