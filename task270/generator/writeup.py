"""submission.md from generator/figures.json: the five blocks, every figure emitted from the generator's own
numbers."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402


def f1(x):
    return "%.1f" % x


def n0(x):
    return "{:,}".format(int(x))


def text(fig):
    c, cp = fig["call"], fig["components"]
    R, X = fig["asks"]["R"], fig["asks"]["X"]["expected_first_donation_bookings"]
    r3, ctx = c["reach3_pct"], fig["context"]
    pick, run = c["schedule"], c["runner_up"]
    third = [s for s in K.SCHED if s not in (pick, run)][0]
    above = R["campaign_weeks_above_baseline"]
    out = ["## Tags", "",
           "**Domain:** Marketing & Consumer Research (media reach, frequency and audience measurement).",
           "**Analytical objective:** Descriptive & Distribution Analysis.", ""]
    out += ["## 1. Final Recommendation", "",
            "**Gota Viva should buy Schedule %s, first place in young prime time, for April 2027.**" % pick,
            "It puts the film three or more times before %s per cent of adults aged 18 to 34, %s points ahead of "
            "Schedule %s at %s per cent. Not Schedule %s: its prime-time rotation spots are placed by the channels, "
            "and of the %s rotation bookings Vértice, Litoral and Pulsar+ sold for prime time in the reference weeks, "
            "%s (%s per cent) aired in daytime breaks, so the rotation places prime time shows overstate it. Not "
            "Schedule %s, whose last places in sport and late night reach %s per cent." % (
                f1(r3[pick]), f1(c["lead_points"]), run, f1(r3[run]), run, n0(cp["prime_rotation_bookings"]),
                n0(cp["prime_rotation_bookings_aired_outside_prime"]), f1(cp["share_aired_outside_prime_pct"]), third,
                f1(r3[third])), ""]
    out += ["## 2. Critical Components", "",
            "1. Of the **%s** prime-time rotation bookings on Vértice, Litoral and Pulsar+ in the reference weeks, "
            "**%s** (**%s** per cent) aired outside prime time." % (
                n0(cp["prime_rotation_bookings"]), n0(cp["prime_rotation_bookings_aired_outside_prime"]),
                f1(cp["share_aired_outside_prime_pct"])),
            "2. Schedule A reaches **%s** per cent of adults 18 to 34 three or more times." % f1(r3["A"]),
            "3. Schedule B reaches **%s** per cent three or more times." % f1(r3["B"]),
            "4. Schedule C reaches **%s** per cent three or more times." % f1(r3["C"]), ""]
    out += ["## 3. Step-by-Step Solution", "",
            "1. Mapped each spot line of esquemas_campanha_2027.xlsx to the same weekday of reference week n, 2 to 29 "
            "March 2026 (briefing_campanha_jovens_2027.pdf, clause 3.2), Pulsar+ as Pulsar through canais_codigos.csv.",
            "2. Kept the live statements of panel members in audimetria_visionamentos_2026-03.csv on the local clock "
            "(UTC, one hour added from the clock change of 29 March), and the members of 18 to 34 with their 28-day "
            "weight from audimetria_individuos_2026-03.csv (clause 3.3).",
            "3. Placed each first-place and last-place spot at the first or last place of its break in "
            "emissao_publicitaria_2026-03.csv (dia_tv, programa, intervalo_no_programa), with the start and length "
            "that place had (clause 3.3).",
            "4. Joined reservas_publicidade_2026-03.csv to the as-run log on id_reserva: %s of the %s rotation "
            "bookings sold for prime time on Vértice, Litoral and Pulsar+ aired outside prime time, in daytime "
            "breaks." % (n0(cp["prime_rotation_bookings_aired_outside_prime"]), n0(cp["prime_rotation_bookings"])),
            "5. Read each rotation spot at every place where that reference day's prime-time rotation bookings on its "
            "channel aired, each with the share of those bookings that aired there (clause 3.4).",
            "6. Counted a member as seeing a place watched live for at least half its seconds and took each member's "
            "chance of seeing the film three or more times across independent spots (clause 3.5), weighted over the 18 "
            "to 34 universe: A %s, B %s and C %s per cent." % (f1(r3["A"]), f1(r3["B"]), f1(r3["C"])),
            "7. Applied the response rule in notas_extracao_portal_dador.txt to marcacoes_portal_dador_2025.csv with a "
            "person as their identity document (documento_hash), since people who registered again after the portal "
            "went live on 17 March 2025 hold two donor numbers: %s a week before the campaign, its four weeks %s, %s, "
            "%s and %s above that (%s in all), %s per thousand of the %s thousand relatorio_campanha_jovens_2025.pdf "
            "reports reached three or more times." % (f1(R["baseline_weekly_average"]), f1(above[0]), f1(above[1]),
                                                      f1(above[2]), f1(above[3]), f1(R["campaign_weeks_total_above"]),
                                                      "%.2f" % R["response_per_thousand_reached3"],
                                                      f1(ctx["reached3_2025_thousands"])),
            "8. Bought Schedule %s, %s points ahead of %s; at that response it brings about %s first-donation "
            "bookings, against %s for %s and %s for %s." % (pick, f1(c["lead_points"]), run, n0(X[pick]), n0(X[run]),
                                                           run, n0(X[third]), third), ""]
    out += ["## 4. Deliverable Answers", "",
            "### plano_tv_jovens_2027.xlsx", "",
            "1. Schedule to buy: %s; runner-up %s; lead **%s** points of the 18 to 34 universe." % (
                pick, run, f1(c["lead_points"])),
            "2. Reached three or more times: A **%s**, B **%s**, C **%s** per cent." % (f1(r3["A"]), f1(r3["B"]),
                                                                                    f1(r3["C"])),
            "3. April 2025 campaign: average weekly first-donation bookings by adults 18 to 34 in the four weeks before "
            "it **%s**; its four weeks minus that average **%s**, **%s**, **%s** and **%s**, **%s** in all; response "
            "**%s** per thousand adults it reached three or more times." % (
                f1(R["baseline_weekly_average"]), f1(above[0]), f1(above[1]), f1(above[2]), f1(above[3]),
                f1(R["campaign_weeks_total_above"]), "%.2f" % R["response_per_thousand_reached3"]),
            "4. Expected first-donation bookings at that response: A **%s**, B **%s**, C **%s**." % (
                n0(X["A"]), n0(X["B"]), n0(X["C"])), "",
            "### recomendacao_esquema_tv_2027.pptx", "",
            "1. Two column charts on slide 2, each schedule's share reached three or more times beside its expected "
            "first-donation bookings, Schedule %s's columns in red as the one to buy." % pick, ""]
    return "\n".join(out)


if __name__ == "__main__":
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    path = os.path.join(os.path.dirname(HERE), "submission.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text(fig))
    print("wrote", path)
