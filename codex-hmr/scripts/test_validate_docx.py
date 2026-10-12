#!/usr/bin/env python3
"""Synthetic structural tests; no patient data and no network."""
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import unittest
from validate_docx import audit, W

class ValidatorTests(unittest.TestCase):
    def test_invariants(self):
        with TemporaryDirectory() as d:
            d=Path(d)
            def doc(name,clinical='',feedback='Feedback',extra=''):
                path=d/name
                xml=f'<w:document xmlns:w="{W[1:-1]}"><w:body>{clinical}<w:p><w:r><w:t>Thank you for your referral to HMR Pharmacist</w:t></w:r></w:p><w:p><w:r><w:t>{feedback}</w:t></w:r></w:p>{extra}<w:sectPr/></w:body></w:document>'
                with ZipFile(path,'w') as z:z.writestr('word/document.xml',xml)
                return path
            base=doc('base.docx')
            self.assertEqual(audit(base,base,'hmr')['findings'],[])
            bad=doc('feedback.docx',feedback='Modified')
            self.assertIn('protected_feedback_changed',[x['code'] for x in audit(base,bad,'hmr')['findings']])
            fmt='<w:p><w:pPr><w:jc w:val="left"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Montserrat" w:hAnsi="Montserrat"/><w:sz w:val="20"/><w:color w:val="000000"/><w:b w:val="0"/><w:i w:val="0"/></w:rPr><w:t>Synthetic content</w:t></w:r></w:p>'
            good=doc('good.docx',clinical=fmt)
            self.assertEqual(audit(base,good,'hmr')['findings'],[])
            wrong=doc('wrong.docx',clinical=fmt.replace('Montserrat','Calibri'))
            self.assertIn('changed_run_font_not_explicit_montserrat',[x['code'] for x in audit(base,wrong,'hmr')['findings']])
            table='<w:tbl><w:tr><w:tc><w:p><w:r><w:t>Prescribed regimen purpose</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:p/></w:tc></w:tr></w:tbl>'
            empty=doc('empty.docx',clinical=table)
            self.assertIn('unused_medicine_row',[x['code'] for x in audit(base,empty,'hmr')['findings']])
    def test_invalid_input(self):
        with TemporaryDirectory() as d:
            path=Path(d)/'bad.docx';path.write_text('not a zip')
            from zipfile import BadZipFile
            with self.assertRaises(BadZipFile):audit(path,path,'hmr')

if __name__=='__main__':unittest.main()
