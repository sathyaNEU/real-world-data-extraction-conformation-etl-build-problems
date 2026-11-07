"""task250 architecture 4: the institute's governing documents, exported by LibreOffice Writer from Word documents.

QS-HS issue 3 files the WHAT of every quantity the programme reports on its fieldwork (the response rate, web
breakoffs, partial returns and the within-household selection standard); the selection protocol carries the
instruction households were given and the helpdesk's answers. Neither says how the selection accuracy is
estimated."""
import datetime as dt
import os

import params as P
import officedoc as od

LT = dt.timezone(dt.timedelta(hours=0))
LST = dt.timezone(dt.timedelta(hours=1))
ORG = "Instituto de Estudos e Inquéritos às Famílias (IEIF)"
ADDR = "Rua Professor Lima Basto 41, 1070-209 Lisboa"


def qs_hs(path):
    created = dt.datetime(2025, 10, 14, 16, 22, 7, tzinfo=LST)
    modified = dt.datetime(2025, 10, 16, 11, 3, 41, tzinfo=LST)
    s = [
        ("title", "Household Survey Quality Standard (QS-HS)"),
        ("subtitle", "Issue 3, approved 14 October 2025, applying from the 2026 programme. "
                     "Norma de Qualidade dos Inquéritos às Famílias, 3.ª edição."),
        ("table", [["Document", "QS-HS issue 3"], ["Owner", "Head of Survey Methodology"],
                   ["Approved by", "Methods Committee, meeting of 14 October 2025"],
                   ["Replaces", "QS-HS issue 2 (November 2022)"], ["Review", "Before the 2028 programme"]],
         [45, 120]),
        ("h1", "1. Scope"),
        ("p", "This standard applies to every survey of the Household Survey Programme (Programa de Inquéritos às "
              "Famílias) that the Institute fields by post and web, with a paper questionnaire offered to households "
              "that have not answered online by the third mailing. It sets what the Institute reports, survey by "
              "survey, on the fieldwork of each programme year, and the checks the Methods Committee applies before "
              "the next year's fieldwork specification is approved."),
        ("p", "Each survey samples addresses from the national address frame. A sampled address is a case in the "
              "case management system from the day its first letter is posted. The fieldwork regions are the "
              "seven regions the Institute plans fieldwork in: Norte, Centro, Lisboa e Vale do Tejo, Alentejo, "
              "Algarve, Açores and Madeira."),
        ("h1", "2. Definitions"),
        ("p", "**Household.** The person or people who usually live at the address. **Member aged 16 or over.** A "
              "member of the household who is aged 16 or over on the date of the household's first letter."),
        ("p", "**Responding household.** A case with a completed questionnaire, on the web or on paper. Where a "
              "household returns more than one completed questionnaire, its return is the first one the Institute "
              "received, and later ones are not used."),
        ("p", "**Collection stream.** A survey's returns in one mode: its web returns, or its paper returns. A "
              "household belongs to the stream of its return."),
        ("p", "**First letter.** The letter that invites the household to take part and carries its access code. "
              "Addresses in a reserve release receive their first letter on the reserve release date."),
        ("h1", "3. Response rate"),
        ("p", "The response rate reported for a survey, overall and in each fieldwork region, is the American "
              "Association for Public Opinion Research's response rate 3: completed returns over the eligible "
              "cases, where the eligible cases are the cases known to be eligible plus a share e of the cases whose "
              "eligibility is unknown."),
        ("p", "A case is known to be eligible when the household completed a return, left a partial return (section "
              "5) or refused. A case is ineligible when the address is out of scope or the postal service returned "
              "a letter to it as 'endereço inexistente' or 'endereço insuficiente'. A letter returned for any other "
              "reason (destinatário desconhecido, mudou-se, recusado, não reclamado, falecido or outro) leaves the "
              "address's eligibility unknown, as does a case with no return of any kind."),
        ("p", "Out of scope are the addresses the address frame records as communal establishments (alojamento "
              "coletivo) or as non-residential premises, unless the household there completed a return. Mixed-use "
              "buildings are in scope."),
        ("p", "The share e is the share eligible among the cases whose eligibility is known, taken in the same "
              "survey and region as the rate. Rates are reported as per cents to one decimal."),
        ("h1", "4. Web questionnaire breakoffs"),
        ("p", "A household has started the web questionnaire once it has answered the first question, which is the "
              "selection question on the welcome page. A household that started and did not complete a "
              "questionnaire in either mode by the survey's close is a web breakoff. The breakoff share of a "
              "survey is its web breakoffs over the households that started its web questionnaire, as a per cent to "
              "one decimal."),
        ("h1", "5. Partial returns"),
        ("p", "A web questionnaire abandoned after the last page of the core module, and never completed, is a "
              "partial return. Partial returns are not used in estimates. They count as known to be eligible in "
              "the response rate and as web breakoffs in section 4."),
        ("h1", "6. Within-household selection"),
        ("p", "Each survey interviews one member aged 16 or over in each household. Every letter, the paper "
              "questionnaire's cover and the web welcome page ask that the questionnaire be answered by the member "
              "aged 16 or over whose birthday comes next after the date of the household's first letter; the "
              "wording is in the Respondent Selection Protocol. Estimates carry each respondent's selection weight, "
              "the household's number of members aged 16 or over."),
        ("p", "**Selection accuracy.** The selection accuracy of a collection stream for a programme year is the "
              "share of its responding households with two or more members aged 16 or over in which the respondent "
              "was the member whose birthday came next after the date of the household's first letter. The members "
              "aged 16 or over are counted as the return records them. Households whose respondent gave no date of "
              "birth are left out of the share. The accuracy for a year is estimated each January from the year's "
              "returns."),
        ("p", "**The standard.** A collection stream keeps the next-birthday instruction for the following programme "
              "year where its selection accuracy in the year just closed is at least 85 in 100. A stream below that "
              "moves, for the following year, to the household grid with a random selection: on the web the "
              "questionnaire lists the household's members aged 16 or over and selects one at random; on paper a "
              "selection table printed for each address does the same."),
        ("p", "**Reporting.** The Head of Survey Methodology reports each stream's selection accuracy and the "
              "proposed selection for the following year to the Methods Committee before the following year's "
              "letters go to print."),
        ("h1", "7. Records the Institute keeps for these checks"),
        ("p", "The case management system holds each case's mailings, final disposition and the return kept for "
              "it. The web platform logs each session against the access code used. The post room registers every "
              "letter the postal service returns, with the postal service's reason. The scanning contractor "
              "exports the paper returns. None of these records is changed after the survey's close except to "
              "correct a keying error."),
        ("h1", "Revision history"),
        ("table", [["Issue", "Date", "Change"],
                   ["1", "March 2019", "First issue: response rates and partial returns."],
                   ["2", "November 2022", "Web breakoffs added; fieldwork regions reduced to seven."],
                   ["3", "October 2025", "Section 6, within-household selection, added; out-of-scope addresses "
                                         "follow the address frame's use class."]],
         [16, 30, 120]),
        ("sig", [("Amélia Figueiredo", "Head of Survey Methodology"),
                 ("Ismael Loureiro", "Fieldwork Operations Manager")]),
    ]
    doc = od.build_docx(s, "Household Survey Quality Standard (QS-HS), issue 3", ORG,
                        "Quality standard for the Household Survey Programme's fieldwork",
                        ORG + "    " + ADDR, "QS-HS issue 3", created, modified, last_by="Amélia Figueiredo",
                        keywords="QS-HS, qualidade, trabalho de campo")
    od.export_pdf(doc, path, created, modified)


def protocol(path):
    created = dt.datetime(2025, 12, 2, 10, 48, 15, tzinfo=LT)
    modified = dt.datetime(2025, 12, 9, 17, 31, 52, tzinfo=LT)
    s = [
        ("title", "Respondent Selection Protocol 2026"),
        ("subtitle", "Household Survey Programme, version 2026.1, 9 December 2025. Protocolo de seleção do "
                     "respondente."),
        ("table", [["Applies to", "Every survey of the 2026 programme, web and paper"],
                   ["Prepared by", "Survey Methodology"], ["Checked by", "Fieldwork Operations"],
                   ["Version", "2026.1 (replaces 2025.2)"]], [40, 125]),
        ("h1", "1. Purpose"),
        ("p", "Each survey interviews one member aged 16 or over in each sampled household. The household chooses "
              "that member itself, by the next-birthday instruction below. This protocol gives the instruction's "
              "wording on every document the household sees, the questions that go with it and the helpdesk's "
              "answers to the questions households ask about it."),
        ("h1", "2. The instruction"),
        ("p", "Every letter carries the instruction in the paragraph after the greeting. The date in it is the date "
              "printed at the top of the household's first letter; reminders repeat that same date."),
        ("table", [["Document", "Wording (Portuguese, as printed)"],
                   ["1.ª carta", "Para que os resultados representem todas as pessoas, pedimos que o questionário seja "
                                 "respondido pela pessoa da sua casa, com 16 ou mais anos, que faça anos primeiro a seguir "
                                 "a [data da 1.ª carta]."],
                   ["Postal de lembrete", "Se ainda não respondeu: o questionário deve ser respondido pela pessoa com "
                                          "16 ou mais anos que faça anos primeiro a seguir a [data da 1.ª carta]."],
                   ["3.ª carta e capa do questionário", "Responda, por favor, a pessoa com 16 ou mais anos que faça "
                                                        "anos primeiro a seguir a [data da 1.ª carta]. Se essa pessoa "
                                                        "já respondeu online, não precisa de devolver este questionário."],
                   ["Página de entrada (web)", "Este questionário deve ser respondido pela pessoa da sua casa, com 16 "
                                               "ou mais anos, que faça anos primeiro a seguir a [data da 1.ª carta]."]],
         [42, 123]),
        ("h1", "3. The selection question"),
        ("p", "The first question on the web welcome page, and question 0 on the paper questionnaire, asks the person "
              "answering to confirm the instruction."),
        ("table", [["Mode", "Question", "Answers"],
                   ["Web", "É a pessoa da sua casa, com 16 ou mais anos, que faz anos primeiro a seguir a [data]?",
                    "Sim / Não, mas vou responder eu"],
                   ["Papel", "P0. É a pessoa da sua casa, com 16 ou mais anos, que faz anos primeiro a seguir a [data]?",
                    "1 Sim / 2 Não, mas respondo eu"]], [18, 100, 47]),
        ("p", "The answer is recorded and the questionnaire continues whatever it is."),
        ("h1", "4. The household grid"),
        ("p", "The second page lists every member of the household, starting with the person answering: sex, year "
              "of birth and relation to the person answering. It then asks how many members are aged 16 or over and "
              "how many people live there in all. The grid gives the household's composition for weighting."),
        ("h1", "5. Helpdesk answers"),
        ("table", [["Question from the household", "Answer the helpdesk gives"],
                   ["Two of us have the same birthday.", "Either of you may answer."],
                   ["The person with the next birthday is away for the whole fieldwork period.",
                    "Please keep the questionnaire for them if they return before the closing date; otherwise there "
                    "is no need to answer."],
                   ["The person with the next birthday does not want to answer.",
                    "We are sorry not to have their views; please do not ask someone else to answer instead."],
                   ["My birthday is on the date of the letter.",
                    "Your birthday is not after that date, so the next one counts in a year's time."],
                   ["I was born on 29 February.", "In 2026, count your birthday as 1 March."],
                   ["Can I answer for someone else?", "No: the questionnaire asks about the person answering."]],
         [70, 95]),
        ("h1", "6. Households that answer twice"),
        ("p", "A household sometimes returns a paper questionnaire after answering online, or the other way round. "
              "The case management system keeps the first return it received for the case and marks the case "
              "complete from that date (QS-HS section 2)."),
        ("h1", "Versions"),
        ("table", [["Version", "Date", "Change"],
                   ["2025.2", "July 2025", "Welcome page wording shortened."],
                   ["2026.1", "December 2025", "Selection question added to the paper questionnaire (P0); helpdesk "
                                               "answers on shared birthdays and 29 February."]], [20, 30, 115]),
        ("sig", [("Amélia Figueiredo", "Head of Survey Methodology"),
                 ("Ismael Loureiro", "Fieldwork Operations Manager")]),
    ]
    doc = od.build_docx(s, "Respondent Selection Protocol 2026", ORG,
                        "Within-household selection: instruction, questions and helpdesk answers",
                        ORG + "    " + ADDR, "Protocolo de seleção do respondente 2026.1", created, modified,
                        last_by="Amélia Figueiredo", keywords="seleção, respondente, protocolo")
    od.export_pdf(doc, path, created, modified)


def write_all(target):
    qs_hs(os.path.join(target, "qs_hs_household_surveys_issue3.pdf"))
    protocol(os.path.join(target, "respondent_selection_protocol_2026.pdf"))
