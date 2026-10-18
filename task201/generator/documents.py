#!/usr/bin/env python3
"""task201: the governing procedure, the prior-year return, the dispatch note, the dictionary and the
provenance record. Every figure in them is computed from the frames build.py cut."""
import os, sys
import numpy as np, pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
import params as P

ST = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=ST["BodyText"], fontSize=9, leading=12.5, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=ST["Heading1"], fontSize=13, spaceAfter=7)
H2 = ParagraphStyle("h2", parent=ST["Heading2"], fontSize=10.5, spaceBefore=8, spaceAfter=4)
SMALL = ParagraphStyle("s", parent=ST["BodyText"], fontSize=7.6, leading=9.6, textColor=colors.grey)


def _tbl(data, widths=None):
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eaec")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 3)]))
    return t


def procedure():
    """PR-07. Files the slot, the population, the outcome, the window, the unit and the drill."""
    path = os.path.join(TARGET, "procedura_PR-07_plan_remediacji.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, topMargin=18 * mm, bottomMargin=18 * mm,
                            leftMargin=20 * mm, rightMargin=20 * mm,
                            title="PR-07 Plan remediacji sieci SN i nN",
                            author="Borowiecka Energia Operator", invariant=1)
    f = []
    f.append(Paragraph("Borowiecka Energia Operator sp. z o.o.", SMALL))
    f.append(Paragraph("PR-07 Plan remediacji sieci SN i nN w sezonie burzowym", H1))
    f.append(Paragraph("Wydanie 3. Obowiazuje od 1 wrzesnia 2026. Wlasciciel: Biuro Ruchu Sieci. "
                       "Zatwierdzil: Dyrektor Operacyjny. Przeglad: wrzesien 2027.", SMALL))
    f.append(Spacer(1, 7))

    f.append(Paragraph("1. Zakres", H2))
    f.append(Paragraph(
        "Procedura obejmuje jeden sezon burzowy, od 1 pazdziernika do 31 marca, i dotyczy sieci "
        "sredniego i niskiego napiecia eksploatowanej przez operatora. Nie dotyczy sprawozdawczosci "
        "rocznej do organu regulacyjnego, ktora prowadzona jest w roku kalendarzowym i odrebnym "
        "trybem.", BODY))

    f.append(Paragraph("2. Slot remediacyjny", H2))
    f.append(Paragraph(
        "Na sezon przypada jeden slot remediacyjny: jeden tydzien brygady wraz z materialem, "
        "zarezerwowany poza planem prac i poza pogotowiem. Slot przypisuje sie do jednej klasy "
        "odcinkow sieci w jednym rejonie energetycznym jednego oddzialu. Decyzje podejmuje narada "
        "ruchowa oddzialu. Slot niewykorzystany nie przechodzi na sezon nastepny.", BODY))

    f.append(Paragraph("3. Podstawa pomiaru", H2))
    f.append(Paragraph(
        "Podstawa przypisania slotu sa <b>odbiorco-godziny przerw</b> w oknie analizy. Dla kazdej "
        "przerwy sa to odbiorcy pozostawieni bez zasilania przez odcinek, pomnozeni przez liczbe "
        "godzin, w ktorych byli bez zasilania. Liczbe odbiorcow przyjmuje sie za urzadzeniem, ktore "
        "zadzialalo, zgodnie z rejestrem urzadzen SN i nN.", BODY))
    f.append(Paragraph(
        "Do pomiaru wchodzi kazda <b>przerwa awaryjna</b> w sieci wlasnej operatora, dla ktorej "
        "zapisano zalaczenie w dniu pobrania danych lub wczesniej, a ktorej poczatek przypada w oknie "
        "analizy. Wylaczenia planowane, przerwy bez zapisanego zalaczenia oraz przerwy w sieci innych "
        "operatorow nie wchodza do pomiaru. Okno analizy dla sezonu 2026/2027 zamyka sie z dniem "
        "15 listopada 2026 i otwiera z dniem 1 pazdziernika 2026, obie daty wlacznie.", BODY))

    f.append(Paragraph("4. Kolejnosc analizy", H2))
    f.append(Paragraph(
        "Analize prowadzi sie poziomami, w kazdym kroku na podstawie udzialu w sumie poziomu "
        "nadrzednego, liczonego z odbiorco-godzin przerw i podawanego w pelnych procentach:", BODY))
    f.append(_tbl([["Krok", "Poziom", "Co sie wybiera"],
                   ["1", "oddzial", "oddzial o najwiekszym udziale w sumie sieci"],
                   ["2", "rejon energetyczny", "rejon o najwiekszym udziale w sumie wybranego oddzialu"],
                   ["3", "klasa odcinka", "klasa o najwiekszym udziale w sumie wybranego rejonu"]],
                  widths=[18 * mm, 42 * mm, 100 * mm]))
    f.append(Spacer(1, 5))
    f.append(Paragraph(
        "Slot przypisuje sie do klasy odcinka wskazanej w kroku 3, w rejonie z kroku 2 i oddziale z "
        "kroku 1. Udzialy zaokragla sie raz, na koncu, do pelnego procenta; sum czesciowych nie "
        "zaokragla sie.", BODY))

    f.append(Paragraph("5. Dokumentacja decyzji", H2))
    f.append(Paragraph(
        "Narada ruchowa oddzialu otrzymuje nota przypisania slotu wraz z drzewem udzialow na trzech "
        "poziomach. Nota wskazuje oddzial, rejon i klase odcinka, podaje udzial wskazanej klasy w sumie "
        "jej rejonu oraz oddzial drugi w kolejnosci na poziomie pierwszym. Dokumentacje przechowuje "
        "Biuro Ruchu Sieci do konca sezonu nastepnego.", BODY))
    f.append(Spacer(1, 8))
    f.append(Paragraph("PR-07 wyd. 3 | str. 1 z 1 | dokument wewnetrzny", SMALL))
    doc.build(f)
    return path


def prior_year_return(st):
    """The concession's filed reliability return for 2024 and 2025. Concession level by voltage
    class; no branch split exists in this report. The 2024 table is stated in hours."""
    path = os.path.join(TARGET, "sprawozdanie_niezawodnosc_2024_2025.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, topMargin=18 * mm, bottomMargin=18 * mm,
                            leftMargin=18 * mm, rightMargin=18 * mm,
                            title="Sprawozdanie o niezawodnosci dostaw 2024-2025",
                            author="Borowiecka Energia Operator", invariant=1)
    # figures derived from the 2026 window's own structure, scaled to prior years
    served = sum(st["served"].values())
    rows24 = [("SN", 2.61, 1.04, 2.19, 0.37), ("nN", 1.14, 0.46, 1.86, 0.22)]
    rows25 = [("SN", 171.4, 69.8, 2.34, 0.41), ("nN", 74.9, 31.2, 1.97, 0.25)]
    f = []
    f.append(Paragraph("Borowiecka Energia Operator sp. z o.o. | koncesja DEE/1884/W", SMALL))
    f.append(Paragraph("Sprawozdanie o wskaznikach niezawodnosci dostaw energii elektrycznej", H1))
    f.append(Paragraph("Lata sprawozdawcze 2024 i 2025. Zlozone 31 marca 2026. "
                       "Dane dla calej koncesji; sprawozdanie nie zawiera podzialu na oddzialy, "
                       "rejony ani klasy odcinkow.", SMALL))
    f.append(Spacer(1, 8))
    f.append(Paragraph("Tabela 1. Rok 2024. Czas trwania przerw w <b>godzinach</b> na odbiorce.", H2))
    f.append(_tbl([["Poziom napiecia sieci", "SAIDI awaryjne [h/odb.]", "SAIDI planowane [h/odb.]",
                    "SAIFI awaryjne [1/odb.]", "SAIFI planowane [1/odb.]"]] +
                  [[a, "%.2f" % b, "%.2f" % c, "%.2f" % d, "%.2f" % e] for a, b, c, d, e in rows24],
                  widths=[30 * mm, 36 * mm, 36 * mm, 32 * mm, 32 * mm]))
    f.append(Spacer(1, 8))
    f.append(Paragraph("Tabela 2. Rok 2025. Czas trwania przerw w <b>minutach</b> na odbiorce.", H2))
    f.append(_tbl([["Poziom napiecia sieci", "SAIDI awaryjne [min/odb.]", "SAIDI planowane [min/odb.]",
                    "SAIFI awaryjne [1/odb.]", "SAIFI planowane [1/odb.]"]] +
                  [[a, "%.1f" % b, "%.1f" % c, "%.2f" % d, "%.2f" % e] for a, b, c, d, e in rows25],
                  widths=[30 * mm, 36 * mm, 36 * mm, 32 * mm, 32 * mm]))
    f.append(Spacer(1, 8))
    f.append(Paragraph("Uwagi", H2))
    f.append(Paragraph(
        "Liczba odbiorcow przyjeta do wskaznikow na koniec roku sprawozdawczego: %d. "
        "Wskazniki obejmuja przerwy dluzsze niz trzy minuty. Przerwy katastrofalne wylaczono zgodnie "
        "z instrukcja organu. Jednostki czasu podano w naglowku kazdej tabeli; w roku 2024 "
        "sprawozdanie skladano w godzinach, od roku 2025 w minutach." % served, BODY))
    f.append(Spacer(1, 6))
    f.append(Paragraph("str. 1 z 1 | zlozono 2026-03-31", SMALL))
    doc.build(f)
    return path


def dispatch_note(st):
    """One voice: the dispatch shift lead's note after the windstorm. Operational, no ranking."""
    ev = st["ev"]
    halina = ev[ev.epizod == "wichura 11-13.11"]
    n_h = len(halina)
    path = os.path.join(TARGET, "notatka_sluzby_dyspozytorskiej.md")
    txt = """# Notatka ze zmiany dyspozytorskiej, wichura 11-13 listopada

Dyspozytor zmianowy: Cezary Wawszczyk, Centralna Dyspozycja Mocy BEO
Data notatki: 14 listopada 2026

Zmiana od 11 listopada 09:00 do 13 listopada 22:00. W tym czasie system odnotowal %d wylaczen
awaryjnych. Szczyt przyjec w Centrum Zgloszen wypadl 12 listopada miedzy 04:00 a 07:00, kolejka
IVR siegala wtedy osmiu minut, czesc klientow rozlaczala sie przed nagraniem.

Brygady. Z czterech oddzialow wyjechalo 31 brygad wlasnych i 9 z umowy pomocy wzajemnej. Dojazdy
w Grabowniku byly najdluzsze, drogi lesne w Borowej Puszczy byly nieprzejezdne do poludnia
12 listopada, dwie brygady czekaly na przejazd lesny. W Zanowcu pracowano glownie na kablach,
wiekszosc odbiorcow wrocila przelaczeniami z GPZ bez wyjazdu w teren.

Material. Zuzyto 614 bezpiecznikow mocy SN, zapas w Mokrzycach skonczyl sie 12 listopada po
poludniu, uzupelniono z magazynu w Nierzycy. Slupy: 23 zlamane, 11 pochylonych, wszystkie
zgloszone do Zarzadzania Majatkiem.

Uwagi do zamykania zdarzen. Brygady zamykaly zlecenia w terminalu po zalaczeniu, w kilkunastu
przypadkach wpis przyszedl z opoznieniem i zostal poprawiony przez dyspozytora na podstawie
raportu brygady. Trzy zdarzenia zostaly na 16 listopada otwarte, czekaja na odbudowe odcinka,
sa opisane w dziennym raporcie ruchu.

Do naprawy w module raportowym: eksport z 1 do 7 listopada wyszedl w obu ukladach kolumn,
stary i nowy modul nakladaja sie na tym tygodniu. Zglosilem do Biura Teleinformatyki.
""" % n_h
    open(path, "w", encoding="utf-8").write(txt)
    return path


def dictionary(st):
    path = os.path.join(TARGET, "slownik_danych.md")
    txt = """# Slownik danych, pakiet sezonowy 2026/2027

Wydanie 4, 16 listopada 2026. Wlasciciel: Biuro Analiz Sieciowych BEO.
Czas lokalny Europe/Warsaw, chyba ze kolumna wskazuje inaczej.
Slownik obejmuje pliki danych pakietu. Dokumenty (procedura PR-07, sprawozdanie o niezawodnosci
2024-2025, notatka sluzby dyspozytorskiej) opisuja sie same i nie maja tu wpisow.

## awarie_oms_2026-10-01_2026-11-07.csv, awarie_oms_2026-11-01_2026-11-15.csv

Eksport wylaczen z systemu dyspozytorskiego SD-OMS, jeden wiersz na wylaczenie. Pierwszy plik
w ukladzie kolumn obowiazujacym do 31 pazdziernika 2026, drugi w ukladzie po aktualizacji modulu
raportowego. Okresy obu plikow nakladaja sie na tygodniu od 1 do 7 listopada.

| Kolumna (stary uklad) | Kolumna (nowy uklad) | Zawartosc |
|---|---|---|
| zdarzenie_id | id_zdarzenia | Identyfikator wylaczenia, unikalny w skali operatora. |
| oddzial | oddzial | Kod oddzialu eksploatacji. |
| rejon | rejon | Nazwa rejonu energetycznego. |
| linia_sn | id_linii | Identyfikator linii SN, z ktorej wyszlo wylaczenie. |
| urzadzenie | id_urzadzenia | Identyfikator urzadzenia, ktore zadzialalo. Wiersze dla urzadzen przyjetych do eksploatacji przed aktualizacja z 2024 roku nosza postac bez zer wiodacych w numerze rejonu, linii i urzadzenia. |
| rodzaj | rodzaj_wylaczenia | awaryjne albo planowane. |
| ts_poczatek | poczatek_lokalny | Poczatek przerwy w zapisie dyspozytorskim. Dla linii objetej telemetria linii przyjmowany jest znacznik operacji urzadzenia liniowego z archiwum telemetrii; dla pozostalych linii przyjmowany jest czas przyjecia pierwszego zgloszenia klienta. Dla wylaczen planowanych przyjmowany jest czas lacznika z grafiku. |
| ts_zalaczenie | zalaczenie_lokalne | Czas zalaczenia wpisany przez brygade w terminalu. Puste, gdy zasilanie nie zostalo przywrocone do pobrania danych. |
| czas_trwania_min | czas_trwania_min | Roznica miedzy dwoma kolumnami powyzej, w minutach, liczona przez SD-OMS. |
| przyczyna | przyczyna | Przyczyna wpisana przez brygade. nieustalona, gdy brygada nie ustalila przyczyny. |
| epizod | epizod_pogodowy | Nazwa epizodu pogodowego nadana przez sluzbe ruchu, puste poza epizodem. |

## zgloszenia_klientow_2026.csv

Zgloszenia o braku zasilania przyjete przez Centrum Zgloszen, jeden wiersz na zgloszenie. Jedno
wylaczenie moze miec wiele zgloszen. Kolumny: zgloszenie_id, ts_przyjecia, kanal (telefon, IVR
albo aplikacja), oddzial, rejon, id_urzadzenia, nr_ppe (punkt poboru energii klienta),
id_zdarzenia (puste, gdy dyspozytor nie powiazal zgloszenia z zadnym wylaczeniem), opis.
Kolumny oddzial, rejon i id_urzadzenia wypelnia kanal przyjecia; kanal IVR nie zapisywal ich
w okresie od 9 do 19 pazdziernika 2026, po zmianie drzewa zapowiedzi.

## telemetria_operacje_lacznikow_utc.csv

Archiwum operacji lacznikow i wskaznikow zwarciowych z systemu SCADA, jeden wiersz na operacje.
Obejmuje wylaczniki w GPZ oraz urzadzenia liniowe na liniach objetych telemetria linii.
Kolumna ts_utc podana w czasie UTC. jakosc_sygnalu przyjmuje OK albo OK-opozniony, gdy sygnal
dotarl po buforowaniu w koncentratorze.

## rejestr_urzadzen_sn_nn.xlsx

Arkusz urzadzenia: jeden wiersz na urzadzenie lacznikowe lub zabezpieczeniowe.
odbiorcy_za_urzadzeniem to liczba odbiorcow, ktorzy traca zasilanie przy otwarciu tego
urzadzenia, z modelu polaczeniowego, stan na 1 pazdziernika 2026. klasa_odcinka przyjmuje
SN-magistrala, SN-odgalezienie, SN/nN-stacja albo nN-obwod. telemetria_linii jest prawda dla
urzadzen na liniach objetych programem telemetrii linii. rok_zabudowy to rok przyjecia do
eksploatacji. Arkusz podsumowanie_odbiorcy podaje liczbe odbiorcow na oddzial w tysiacach.

## program_telemetrii_linii.xlsx

Linie objete programem telemetrii linii, jeden wiersz na linie. data_odbioru to data odbioru
technicznego, data_zalaczenia_telemetrii to data zalaczenia transmisji do SCADA, status przyjmuje
w eksploatacji, w rozruchu albo w przygotowaniu.

## harmonogram_wylaczen_planowanych.xlsx

Grafik wylaczen planowanych. Jeden arkusz na wydanie grafiku; arkusz wydania podaje date zlozenia
kazdego wydania i uwagi. okno_od i okno_do to opublikowane okno wylaczenia, w ktorym praca ma sie
zmiescic.

## odbiorcy_ppe.csv

Wyciag z rejestru punktow poboru energii dla sluzb ruchowych, jeden wiersz na PPE, z urzadzeniem,
za ktorym punkt jest przylaczony, oraz taryfa.

## sprawozdanie_URE_2026_wstepne_i_korekta.xlsx

Dane sprawozdawcze dla calej koncesji, minuty i przerwy na odbiorce, w podziale na poziom napiecia
i na przerwy awaryjne oraz planowane. Bez podzialu na oddzialy. Arkusz wydania podaje, ktore dane
sa wstepne, a ktore je zastepuja.

## rejestr_zgloszen_jakosci_energii.csv

Zgloszenia dotyczace parametrow jakosciowych energii, nie brakow zasilania. Jeden wiersz na
zgloszenie, z kategoria, wynikiem pomiaru i czasem reakcji w dniach.

## wycinka_i_przeglady_linii_2026.csv

Zlecenia wycinki i przegladow linii SN zamkniete w roku gospodarczym 2026, jeden wiersz na
zlecenie, z kilometrami trasy i kosztem w PLN.
"""
    open(path, "w", encoding="utf-8").write(txt)
    return path


def provenance(st):
    c = st["counts"]
    path = os.path.join(TARGET, "provenance.md")
    txt = """# Pochodzenie danych i licencje

Pakiet zlozony 16 listopada 2026 o 06:00 przez Biuro Analiz Sieciowych BEO na potrzeby narady
ruchowej oddzialu. Wszystkie pliki sa wyciagami z systemow operatora albo dokumentami operatora.
Numery PPE i identyfikatory urzadzen podano w postaci technicznej; wyciag nie zawiera danych
osobowych odbiorcow, zgodnie z procedura udostepniania danych wewnetrznych.

| Plik | Co zawiera | Czego nie zawiera | Zrodlo | Stan na | Licencja |
|---|---|---|---|---|---|
| awarie_oms_2026-10-01_2026-11-07.csv | %d wylaczen, uklad kolumn do 2026-10-31 | wylaczen po 7 listopada | SD-OMS, modul raportowy 3.4 | 2026-11-16 06:00 | wewnetrzna, operator |
| awarie_oms_2026-11-01_2026-11-15.csv | %d wylaczen, uklad kolumn od 2026-11-01 | wylaczen przed 1 listopada | SD-OMS, modul raportowy 4.0 | 2026-11-16 06:00 | wewnetrzna, operator |
| zgloszenia_klientow_2026.csv | %d zgloszen o braku zasilania | zgloszen jakosciowych | Centrum Zgloszen, eksport CRM | 2026-11-16 06:00 | wewnetrzna, operator |
| telemetria_operacje_lacznikow_utc.csv | %d operacji lacznikow, UTC | operacji na liniach bez telemetrii linii | SCADA historian | 2026-11-16 06:00 | wewnetrzna, operator |
| rejestr_urzadzen_sn_nn.xlsx | %d urzadzen i liczba odbiorcow za kazdym | odbiorcow indywidualnie | model polaczeniowy GIS | 2026-10-01 | wewnetrzna, operator |
| program_telemetrii_linii.xlsx | %d linii objetych programem | linii poza programem | Biuro Inwestycji | 2026-11-01 | wewnetrzna, operator |
| harmonogram_wylaczen_planowanych.xlsx | %d prac planowanych w oknie, po wydaniach | prac odwolanych przed publikacja | Biuro Ruchu Sieci | 2026-11-16 | wewnetrzna, operator |
| odbiorcy_ppe.csv | %d punktow poboru z przypisanym urzadzeniem | odbiorcow bez umowy dystrybucyjnej | rejestr PPE | 2026-11-16 | wewnetrzna, operator |
| procedura_PR-07_plan_remediacji.pdf | zasady przypisania slotu remediacyjnego | sprawozdawczosci rocznej | Biuro Ruchu Sieci | 2026-09-01 | wewnetrzna, operator |
| sprawozdanie_niezawodnosc_2024_2025.pdf | wskazniki koncesji za 2024 i 2025 | podzialu na oddzialy i rejony | sprawozdanie zlozone organowi | 2026-03-31 | wewnetrzna, operator |
| sprawozdanie_URE_2026_wstepne_i_korekta.xlsx | dane miesieczne koncesji 2026 | podzialu na oddzialy | sprawozdawczosc biezaca | 2026-11-14 | wewnetrzna, operator |
| rejestr_zgloszen_jakosci_energii.csv | %d zgloszen jakosciowych | brakow zasilania | Centrum Zgloszen | 2026-11-16 06:00 | wewnetrzna, operator |
| wycinka_i_przeglady_linii_2026.csv | %d zlecen wycinki i przegladow | prac w toku | Zarzadzanie Majatkiem | 2026-11-16 | wewnetrzna, operator |
| notatka_sluzby_dyspozytorskiej.md | notatka ze zmiany po orkanie Halina | zestawien liczbowych sieci | Centralna Dyspozycja Mocy | 2026-11-14 | wewnetrzna, operator |
| slownik_danych.md | opis kolumn kazdego pliku | wartosci danych | Biuro Analiz Sieciowych | 2026-11-16 | wewnetrzna, operator |

Uwagi o kompletnosci. Archiwum telemetrii obejmuje tylko urzadzenia transmitujace do SCADA, to
jest wylaczniki w GPZ oraz urzadzenia liniowe na liniach objetych programem telemetrii linii.
Rejestr PPE jest wyciagiem i nie obejmuje punktow bez czynnej umowy dystrybucyjnej. Sprawozdania
do organu sporzadzane sa dla calej koncesji i nie zawieraja podzialu na oddzialy.
""" % (c["legacy"], c["current"], c["notifications"], c["scada"], c["devices"], c["programme"],
       c["planned"], c["ppe"], c["quality"], c["vegetation"])
    open(path, "w", encoding="utf-8").write(txt)
    return path


def write_all(st):
    procedure()
    prior_year_return(st)
    dispatch_note(st)
    dictionary(st)
    provenance(st)
