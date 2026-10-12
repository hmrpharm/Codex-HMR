from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

WORK = Path('/private/tmp/hmr-julie')

def style(run):
    run.font.name = 'Montserrat'
    run._element.rPr.rFonts.set(qn('w:ascii'), 'Montserrat')
    run._element.rPr.rFonts.set(qn('w:hAnsi'), 'Montserrat')
    run.font.size = Pt(10)
    run.font.bold = False
    run.font.italic = False
    run.font.underline = False
    run.font.color.rgb = RGBColor(0, 0, 0)

def replace_cell(cell, lines):
    for extra in cell.paragraphs[1:]:
        extra._element.getparent().remove(extra._element)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.clear()
    for n, line in enumerate(lines):
        if n:
            p.add_run().add_break()
        r = p.add_run(line)
        style(r)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP

dmmr = Document(WORK / 'current-dmmr.docx')
dmmr.save(WORK / 'Julie_Ferguson_Follow_Up_HMR.docx')

hmr = Document(WORK / 'current-hmr.docx')
replace_cell(hmr.tables[6].cell(0, 0), [
    'As the pharmacist responsible for undertaking this Medication Management Review, I confirm that the above recommendations are based on the information available at the time of review, current best-practice guidelines, and the patient’s reported priorities and concerns. Please contact me if you would like to discuss any recommendations or require clarification of any issue raised in this report.',
    '', 'Kind regards,', '', 'Mike Lau', 'B. Pharm (Hons) CredPharm (MMR)',
    'Mobile: 0411777023', 'Email: mike.laukh@gmail.com'
])
hmr.save(WORK / 'Julie_Ferguson_HMR_Pharmacist.docx')

def order_medication_rows(table, desired_labels):
    rows = {row.cells[0].text.strip(): row._tr for row in table.rows[1:]}
    for label in desired_labels:
        table._tbl.append(rows[label])

order = [
    'Fluotex 20 mg capsules (fluoxetine) - 2 capsules daily.',
    'Lyrica 25 mg capsules (pregabalin) - 2 capsules before bed.',
    'Olmetec 40 mg tablets (olmesartan medoxomil) - 1 tablet in the evening.',
    'Sifrol ER 0.375 mg extended-release tablets (pramipexole) - 1 tablet before bed.',
    'Mounjaro 10 mg/dose KwikPen (tirzepatide) - as directed.',
    'Estrogel 0.06% gel (estradiol) - one application per arm daily.',
    'Advantan 0.1% fatty ointment (methylprednisolone aceponate) - apply thinly once daily as directed.',
    'Betamethasone valerate 0.05% cream - apply a small amount to affected area twice daily.',
    'Hydrozole 1%/1% cream (hydrocortisone/clotrimazole) - apply twice daily for no longer than 7 days as directed.',
    'Stemetil 5 mg tablets (prochlorperazine) - 1 tablet three times daily as required.'
]

dmmr = Document(WORK / 'Julie_Ferguson_Follow_Up_HMR.docx')
order_medication_rows(dmmr.tables[4], order)
# Remove template-only vertical spacer paragraphs before the sign-off so the
# contact details remain with the letter rather than creating an orphan page.
for index in (28, 29, 30, 32, 33, 34):
    spacer = dmmr.paragraphs[index].paragraph_format
    spacer.space_before = Pt(0)
    spacer.space_after = Pt(0)
    spacer.line_spacing = Pt(1)
dmmr.paragraphs[27].paragraph_format.space_after = Pt(0)
dmmr.paragraphs[31].paragraph_format.space_before = Pt(0)
dmmr.paragraphs[31].paragraph_format.space_after = Pt(0)
# Start the feedback form on a fresh page without modifying the protected form.
dmmr.paragraphs[36].add_run().add_break(WD_BREAK.PAGE)
dmmr.save(WORK / 'Julie_Ferguson_Follow_Up_HMR.docx')

hmr = Document(WORK / 'Julie_Ferguson_HMR_Pharmacist.docx')
order_medication_rows(hmr.tables[4], order)
hmr.save(WORK / 'Julie_Ferguson_HMR_Pharmacist.docx')
