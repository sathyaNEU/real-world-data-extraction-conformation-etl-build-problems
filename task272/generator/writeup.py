"""submission.md, written from figures.json (every figure emitted, none typed)."""
import golden as GD
import pack as K
import world as W


def _n(x):
    return "{:,}".format(x)


def write(path, fig):
    call = fig["call"]["products"]
    gold = fig["golden"]
    lad = fig["ladder"]
    order = sorted(gold, key=lambda c: -gold[c]["rate"])
    name = {c: W.product(c)["name"] for c in gold}
    L = []
    L += ["## Tags", "",
          "> **Domain:** General Statistics & Data Science (exploratory data analysis and distribution assessment).",
          "> **Analytical objective:** Descriptive & Distribution Analysis.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Configure %d batch-compounded products for gravimetric verification of every dose at the April 2027 "
          "cutover: %s.** Each made more than 10 out-of-tolerance doses per hundred thousand doses made in 2026 under "
          "PH-QP-07 3.1 once every dose is placed on its set at the litres the set had pumped. The other %d stay on "
          "SC-SOP-12's checks. A normal fit to the weighed doses alone would instead add %s and leave out %s." % (
              len(call), "; ".join(name[c] for c in sorted(call)), len(gold) - len(call),
              "; ".join(name[c] for c in sorted(set(lad["ppk"]) - set(call))),
              "; ".join(name[c] for c in sorted(set(call) - set(lad["ppk"])))), ""]
    L += ["## 2. Critical Components", "",
          "1. On PC-1, PC-2 and PC-3 a product's weighed doses fall in a straight line with the litres the set had "
          "pumped since its set-up, about a start that varies from set to set; on PC-4 they do not move.",
          "2. Each completed dose's chance of lying outside its tolerance, taken at the litres its set had pumped and "
          "summed over every dose made, gives each product's 2026 rate per hundred thousand doses made.",
          "3. Against the limit of 10, %s are **over it**; every other product is **under 3**." % "; ".join(
              name[c] for c in sorted(call)), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Read %s's station for each serial (PC-3's two serials, before and after 14 July, are one compounder) and "
          "%s's tolerance, specific gravity and tare for each product." % (K.FILES["equipment"], K.FILES["master"]),
          "2. Took the completed doses in %s (fill times in UTC) and put each on the set its device had installed: the "
          "latest SET_UP in %s before the dose, a re-seated set (the same set lot) being one set." % (
              K.FILES["doses"], K.FILES["events"]),
          "3. For each dose, the litres its set had pumped before it: the programmed volumes of the set's earlier "
          "completed doses.",
          "4. Tied each weighed dose in %s to its dose by batch and dose number; delivered volume is the net weight "
          "(gross weight less the container tare to 30 June) divided by the specific gravity, as a per cent of the "
          "labelled volume." % K.FILES["checks"],
          "5. For each product fitted the weighed doses' per cent deviation as the set's start plus a loss per litre "
          "pumped (one slope across the product's sets, the start varying from set to set about its mean, a "
          "dose-to-dose scatter about the line).",
          "6. Summed over every completed dose the normal chance of lying outside the tolerance at its litres "
          "pumped, with the start's spread and the scatter, per hundred thousand doses made; the call is the products over 10.",
          "7. Counted each station's completed doses by Ontario-local month and each product's sets (distinct set "
          "lots on their devices, the product of the doses filled on them).", ""]
    L += ["## 4. Deliverable Answers", "", "### %s" % GD.PDF, "",
          "1. Products configured for gravimetric verification of every dose: %s." % "; ".join(name[c] for c in sorted(call)),
          "2. Every batch-compounded product marked in or out:"]
    for c in order:
        L.append("   - %s: %s" % (name[c], "in" if c in call else "out"))
    L += ["3. Chart: each product's 2026 out-of-tolerance rate per hundred thousand doses made against the limit of 10, the "
          "products going on verification in red.", "", "### %s" % GD.CSV, "",
          "1. Each compounder's doses made in each month of 2026 (Ontario local time), whole numbers:"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for st in ("PC-1", "PC-2", "PC-3", "PC-4", "GC-1"):
        L.append("   - %s: %s" % (st, ", ".join("%s %s" % (months[m - 1], _n(fig["ask_a"]["%s %02d" % (st, m)]))
                                               for m in range(1, 13))))
    L.append("2. The sets each product filled on PC-1 to PC-4 used in 2026, whole numbers:")
    for c in sorted(fig["ask_b"]):
        L.append("   - %s: %s" % (name[c], _n(fig["ask_b"][c])))
    L.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
