"""metadata.json in the task folder: per shipped file its source, date, licence and rows, and the distractors."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
SYN = " (fictional, synthetic records)"
LIC = "CC0-1.0 (synthetic, generated for this task)"
AQD = "Ministry of the Environment, Air Quality Directorate"
SOURCES = {
    "so2_order_2027_schedule_note.pdf": (AQD + ", note on the 2027 Sulphur Dioxide Order's schedule", "2027-02-08"),
    "so2_inventory_guidance_2026.pdf": (AQD + ", sulphur dioxide inventory guidance for the 2026 inventory year", "2026-11-02"),
    "permitted_boilers_register_2026.xlsx": ("Ministry of the Environment, permit register of coal boilers, Northern Priority Area", "2027-01-06"),
    "scrubber_guarantee_schedules.pdf": (AQD + ", scrubber suppliers' guarantee schedules copied from the permit files", "2024-03-14"),
    "coal_deliveries_2026.csv": (AQD + ", coal suppliers' 2026 delivery statements, collated", "2027-01-22"),
    "coal_supplier_customers.csv": (AQD + ", coal suppliers' customer codes mapped to permits", "2027-01-22"),
    "boiler_returns_2026.xlsx": (AQD + ", operators' quarterly returns for 2026", "2027-02-02"),
    "limestone_tickets_2026.csv": ("Bromscar Quarry and Molhope Lime and Stone, 2026 delivery tickets to permitted sites", "2027-01-14"),
    "limestone_certificates_2026.xlsx": ("Bromscar Quarry and Molhope Lime and Stone, 2026 weekly certificates, collated by the " + AQD, "2027-01-14"),
    "scrubber_tests_2026_iverstow.pdf": ("Iverstow Emission Testing, 2026 abatement performance tests, summary", "2026-10-16"),
    "scrubber_tests_2026_jarrness.pdf": ("Jarrness Stack Testing, 2026 FGD performance tests, results summary", "2026-11-06"),
    "whinmoss_invoice_lines_2026.xlsx": ("Whinmoss Waste Haulage, 2026 invoice lines for permitted sites, supplied to the " + AQD, "2027-01-11"),
    "carnhope_jobs_2026.csv": ("Carnhope Skips, 2026 job sheet for permitted sites, supplied to the " + AQD, "2027-01-07"),
    "pellrigg_dockets_2026.xlsx": ("Pellrigg and Sons Haulage, 2026 dockets for permitted sites, supplied to the " + AQD, "2027-01-08"),
    "ash_contractor_customers.csv": (AQD + ", ash contractors' customer names mapped to permits", "2027-01-15"),
    "npa_ambient_so2_2026.csv": (AQD + ", Northern Priority Area ambient monitoring network, 2026 monthly means", "2027-01-20"),
    "national_coal_consumption_2025.json": ("National Statistics Office, coal consumption by sector, 2025 (provisional)", "2026-06-25"),
}
DISTRACTORS = ["target/npa_ambient_so2_2026.csv", "target/national_coal_consumption_2025.json"]


def main():
    files = []
    for n in sorted(os.listdir(T)):
        src, date = SOURCES[n]
        rows = None
        if n.endswith(".csv"):
            rows = sum(1 for _ in open(os.path.join(T, n), "rb")) - 1
        files.append(dict(file=n, source=src + SYN, date=date, license=LIC, rows=rows))
    meta = dict(task="task485", title="The 2027 Sulphur Dioxide Order: which coal boilers its schedule lists",
                setting="A fictional environment ministry's air quality directorate in an unnamed coal-producing country "
                        "with a register of permitted coal boilers in a Northern Priority Area: the country, its bodies, "
                        "the firms, the contractors and the people are fictional, and every record is synthetic.",
                as_of="2027-02-09",
                deliverables=["sulphur_dioxide_order_schedule_2027.xlsx", "boiler_sulphur_dioxide_2026.png"],
                distractor_files=DISTRACTORS, stated_inputs=["250 tonnes", "calendar 2026"], files=files)
    assert set(SOURCES) == set(os.listdir(T)), set(SOURCES) ^ set(os.listdir(T))
    json.dump(meta, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
