"""task211 golden deliverables and submission.md, written from figures.json alone (every figure emitted, none typed)."""
import io, json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Pt, Inches
import openpyxl
from openpyxl.styles import Font, Alignment
import docs

HERE = Path(__file__).resolve().parent
TASK = HERE.parent
GOLD = TASK / 'golden'
GENS = ['Halvorne', 'Pellbrook', 'Corwen', 'Tessard', 'Wynfield']


def chart(F):
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'svg.hashsalt': 'task211'})
    fig, ax = plt.subplots(figsize=(6.2, 3.0), dpi=150)
    vals = [F['excess_raw'][p] for p in GENS]
    cols = ['#b5462e' if p == F['call'] else '#8c9aa6' for p in GENS]
    ax.bar(GENS, vals, color=cols, width=0.6)
    ax.axhline(0, color='#333333', lw=0.8)
    ax.axhline(2.0, color='#333333', lw=0.8, ls=(0, (4, 3)))
    ax.text(-0.3, 2.12, 'MS-12 referral bar, 2.0', ha='left', va='bottom', fontsize=8)
    k = GENS.index(F['call'])
    ax.text(k, vals[k] + 0.25, '%d' % F['call_excess'], ha='center', fontsize=9, fontweight='bold')
    ax.set_ylabel('Excess qualifying visits\nper 1,000 patient-months')
    ax.set_title('Excess over Levaril, January to June 2026', fontsize=10, loc='left')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', metadata={'Software': None})
    plt.close(fig)
    return buf.getvalue()


def memo(F, path):
    d = Document()
    st = d.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(10.5)
    for line in ('Larkhaven Health, Pharmacy Quality and Formulary', 'To: Formulary Quality Group',
                 'Date: 20 July 2026', 'Subject: Third-quarter laboratory re-test, levetiracetam 500 mg tablets'):
        d.add_paragraph(line)
    p = d.add_paragraph()
    p.add_run('Recommendation: send %s to the contract laboratory. Its patients had %d more qualifying visits per 1,000 '
              'patient-months than the same patients would have had on tablets releasing like Levaril, above the 2.0 '
              'referral bar in MS-12 3.1.' % (F['call'], F['call_excess'])).bold = True
    d.add_paragraph(
        'Halvorne shows the largest raw excess, but it sits in each patient\'s first supply of its new pink tablets, '
        'filled as the Fort Wayne stock reached each distribution centre between December and May. The same excess '
        'follows every change in what a patient\'s tablets look like, Pellbrook patients moved onto the pink tablets and '
        'back during the Pellbrook backorder included, and it does not follow a move between tablets that look alike. '
        'With that first supply held as it was, only %s is above the bar, and its excess runs through every fill.' % F['call'])
    d.add_picture(io.BytesIO(chart(F)), width=Inches(6.2))
    d.add_paragraph('Source: paid claims net of reversals, both hospital feeds dated in Pacific time, transfers counted '
                    'once (MS-12 2.3 to 2.6).').runs[0].font.size = Pt(8.5)
    cp = d.core_properties
    cp.author = 'Larkhaven Health'; cp.last_modified_by = 'Larkhaven Health'; cp.title = 'Re-test referral'
    cp.created = docs.FIXED; cp.modified = docs.FIXED; cp.revision = 1
    d.save(path)
    docs.normalize_ooxml(path)


def workbook(F, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Products'
    ws.append(['Levetiracetam 500 mg generics, January to June 2026 (MS-12 2.4 and 2.5)'])
    ws.append([])
    ws.append(['Generic', 'Patient-months of supply', 'Qualifying visits'])
    for p in GENS:
        ws.append([p, F['patient_months'][p], F['visits'][p]])
    ws.append([])
    ws.append(['Referred: %s, excess %d qualifying visits per 1,000 patient-months' % (F['call'], F['call_excess'])])
    s2 = wb.create_sheet('Spend')
    s2.append(['Spend on each generic by quarter received, dollars (purchasing manual 7.3)'])
    s2.append([])
    s2.append(['Generic', 'Q1 2026', 'Q2 2026'])
    for p in GENS:
        s2.append([p, F['spend']['%s Q1' % p], F['spend']['%s Q2' % p]])
    s3 = wb.create_sheet('Backorders')
    s3.append(['Days on backorder at the wholesaler, by quarter (service schedule clause 4)'])
    s3.append([])
    s3.append(['Generic', 'Q1 2026', 'Q2 2026'])
    for p in GENS:
        s3.append([p, F['backorder_days']['%s Q1' % p], F['backorder_days']['%s Q2' % p]])
    for w in (ws, s2, s3):
        w['A1'].font = Font(bold=True)
        for c in w[3]:
            c.font = Font(bold=True)
        w.column_dimensions['A'].width = 14
        for col in 'BC':
            w.column_dimensions[col].width = 24
    for w in (ws, s2):
        for row in w.iter_rows(min_row=4, max_row=8, min_col=2, max_col=3):
            for c in row:
                c.number_format = '#,##0'
    docs.xlsx_props(wb, 'Levetiracetam products')
    wb.save(path)
    docs.normalize_ooxml(path)


def submission(F):
    gens = GENS
    L = ['## Tags', '', '**Domain:** Pharmacology, Pharmacoepidemiology & Safety (safety signal detection).',
         '**Analytical objective:** Anomaly Detection & Diagnostics.', '',
         '## 1. Final Recommendation', '',
         '**Send %s to the third-quarter laboratory re-test: its patients have %d more qualifying visits per 1,000 '
         'patient-months than tablets releasing like Levaril would give them.** Not Halvorne, whose raw excess is the '
         'first supply of its new pink tablets and goes with any change of tablet appearance, not with what Halvorne\'s '
         'tablets contain.' % (F['call'], F['call_excess']), '',
         '## 2. Critical Components', '',
         '1. The excess over the reference sits on the days of each patient\'s first fill of a tablet that looks different '
         'from their previous fill, for every product, and not on a change between identical tablets.',
         '2. %s\'s excess, held at that, is **%d** qualifying visits per 1,000 patient-months, above the 2.0 bar.' % (F['call'], F['call_excess']),
         '', '## 3. Step-by-Step Solution', '',
         '1. Took paid claims net of reversals from dispensing_claims_2025-04_to_2026-06.parquet, mapped both code schemes '
         'through claims_item_crosswalk.csv and ran each member\'s supply per MS-12 2.4.',
         '2. Dated qualifying visits from both hospital feeds in Pacific time, counted transfers once and linked merged '
         'records through mrn_member_crosswalk.csv (MS-12 2.3); attributed each to the product covering its day (2.5).',
         '3. Gave every fill its tablet from product_register.xlsx, dating Halvorne\'s Fort Wayne tablets by each '
         'distribution centre in halvorne_site_change_notice.pdf (pharmacies.csv) and Corwen\'s beige coat by '
         'corwen_film_coat_notice.pdf, and marked each patient\'s first fill of a differently looking tablet.',
         '4. Fitted a Poisson model of qualifying visits on patient-months with product, that first-supply marker, age band '
         '(under 18, 18 to 64, 65 and over, on 2026 less birth year) and drug-resistant epilepsy, and set the product term '
         'to Levaril\'s with the marker held (MS-12 2.6): %s %d per 1,000 patient-months, every other generic under the '
         '2.0 bar.' % (F['call'], F['call_excess']),
         '5. Spend: joined wholesaler_invoice_lines.csv to dc_receiving_log.csv by delivery number and split each line by '
         'the quarter of each receipt part; spread each price adjustment over that ship-to\'s deliveries of the generic '
         'invoiced before it, counted back from the latest until its bottles were made up, and put each share in the quarter '
         'those bottles were received (purchasing manual 7.3).',
         '6. Backorder days: resolved each notice\'s item through wholesaler_item_list.csv as it stood on the notice\'s day '
         '(a pre-cut-over number the list gives no product as a former number belongs to whichever product without a '
         'listed former number stopped shipping when the notice opened), and ended it the day before the product\'s '
         'next shipment in wholesaler_advance_ship_notices.json, case barcodes read to their bottle (clause 4).',
         '7. Recommendation: send %s.' % F['call'], '',
         '## 4. Deliverable Answers', '', '### retest_referral.docx', '',
         '1. Referral: %s, %d excess qualifying visits per 1,000 patient-months.' % (F['call'], F['call_excess']),
         '2. Bar chart of each generic\'s excess over Levaril for January to June 2026, %s highlighted, with the 2.0 bar.' % F['call'],
         '', '### levetiracetam_products.xlsx', '', '1. Patient-months of supply and qualifying visits, January to June 2026:']
    for p in gens:
        L.append('   - %s: %s patient-months, %d qualifying visits' % (p, format(F['patient_months'][p], ','), F['visits'][p]))
    L.append('2. Spend by quarter received, dollars:')
    for p in gens:
        L.append('   - %s: Q1 %s, Q2 %s' % (p, format(F['spend']['%s Q1' % p], ','), format(F['spend']['%s Q2' % p], ',')))
    L.append('3. Days on backorder at the wholesaler:')
    for p in gens:
        L.append('   - %s: Q1 %d, Q2 %d' % (p, F['backorder_days']['%s Q1' % p], F['backorder_days']['%s Q2' % p]))
    (TASK / 'submission.md').write_text('\n'.join(L) + '\n')


def main():
    F = json.loads((HERE / 'figures.json').read_text())
    GOLD.mkdir(exist_ok=True)
    memo(F, GOLD / 'retest_referral.docx')
    workbook(F, GOLD / 'levetiracetam_products.xlsx')
    submission(F)


if __name__ == '__main__':
    main()
