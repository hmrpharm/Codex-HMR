#!/usr/bin/env python3
"""Read-only DOCX structural lint. Emits locations, never document text. Not clinical approval."""
import argparse
from collections import Counter
import hashlib
import json
import re
import sys
from zipfile import ZipFile, BadZipFile
import xml.etree.ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
NS = {'w': W[1:-1]}
ANCHORS = {'dmmr': 'Thank you for your referral to DMMR Australia',
           'hmr': 'Thank you for your referral to HMR Pharmacist'}

def norm(s):
    return ' '.join(s.split())

def txt(e):
    return ''.join(t.text or '' for t in e.iter(W+'t'))

def canon(e):
    e = ET.fromstring(ET.tostring(e))
    for node in e.iter():
        for key in list(node.attrib):
            if key.startswith(W+'rsid'):
                del node.attrib[key]
    return ET.canonicalize(ET.tostring(e, encoding='unicode'))

def load(path):
    with ZipFile(path) as z:
        if z.testzip():
            raise ValueError('Corrupt ZIP member')
        parts = {n:z.read(n) for n in z.namelist()}
    roots = {n:ET.fromstring(v) for n,v in parts.items() if n.endswith('.xml')}
    return parts, roots

def audit(template, report, kind):
    old, ox = load(template)
    new, nx = load(report)
    findings = []
    def add(code, location, severity='review'):
        findings.append({'code':code, 'location':location, 'severity':severity})
    ob = ox['word/document.xml'].find(W+'body')
    nb = nx['word/document.xml'].find(W+'body')
    anchor = ANCHORS[kind]
    def suffix(body):
        hits=[i for i,e in enumerate(body) if anchor in norm(txt(e))]
        if len(hits)!=1:
            return None
        return [canon(e) for e in list(body)[hits[0]:]]
    a,b=suffix(ob),suffix(nb)
    if a is None or b is None:
        add('feedback_anchor_missing_or_ambiguous','word/document.xml','error')
    elif a != b:
        add('protected_feedback_changed','word/document.xml','error')
    if [canon(e) for e in ob.iter(W+'sectPr')] != [canon(e) for e in nb.iter(W+'sectPr')]:
        add('section_layout_changed','word/document.xml','error')
    protected_parts={n for n in old if n.startswith(('word/header','word/footer','word/media/'))}
    for n in sorted(protected_parts):
        if n not in new or old[n]!=new[n]:
            add('branding_header_footer_changed',n)
    for n,root in nx.items():
        if not n.startswith('word/'):
            continue
        if n.startswith('word/comments') and any(txt(p).strip() for p in root.iter(W+'p')):
            add('review_comments_present',n)
        if any(root.iter(W+'ins')) or any(root.iter(W+'del')):
            add('tracked_changes_present',n)
    # Changed paragraph/run comparison is deliberately conservative. It does not prove
    # that repeated old sample text is safe or identify every newly inserted run.
    old_paras=Counter(norm(txt(p)) for p in ob.iter(W+'p'))
    changed=0
    for pi,p in enumerate(nb.iter(W+'p')):
        content=norm(txt(p)); loc=f'word/document.xml:paragraph[{pi}]'
        if not content:
            continue
        if re.search(r'\[(?:Patient name|DD/MM/YYYY|Referring doctor|Practice email|Medication \d|Patient-reported|Comments,|Purpose according|Issue title|Describe|Provide|Summarise|Record|Document)[^\]]*\]|\(\s*Insert\b|\bInsert (?:patient|name|date)\b',content,re.I):
            add('possible_placeholder',loc)
        if old_paras[content]>0:
            old_paras[content]-=1
            continue
        changed+=1
        pp=p.find(W+'pPr')
        jc=None if pp is None else pp.find(W+'jc')
        if jc is None or jc.get(W+'val')!='left':
            add('changed_paragraph_not_explicit_left',loc)
        for ri,r in enumerate(p.iter(W+'r')):
            if not txt(r).strip():
                continue
            rp=r.find(W+'rPr'); rloc=loc+f'/run[{ri}]'
            def prop(name):
                return None if rp is None else rp.find(W+name)
            f=prop('rFonts'); sz=prop('sz'); c=prop('color')
            if f is None or any(f.get(W+k)!='Montserrat' for k in ('ascii','hAnsi')) or any(k.endswith('Theme') for k in f.attrib):
                add('changed_run_font_not_explicit_montserrat',rloc)
            if sz is None or sz.get(W+'val')!='20':
                add('changed_run_size_not_explicit_10pt',rloc)
            if c is None or c.get(W+'val','').upper()!='000000' or c.get(W+'themeColor'):
                add('changed_run_colour_not_explicit_black',rloc)
            for style in ('b','i'):
                e=prop(style)
                if e is None or e.get(W+'val') not in ('0','false','off'):
                    add('changed_run_regular_requires_check_'+style,rloc)
            u=prop('u')
            if u is not None and u.get(W+'val')!='none':
                add('changed_run_underlined',rloc)
            h=prop('highlight')
            if h is not None and h.get(W+'val')!='none':
                add('changed_run_highlighted',rloc)
            if prop('shd') is not None:
                add('changed_run_shading_requires_check',rloc)
    for ti,t in enumerate(nb.iter(W+'tbl')):
        rows=t.findall(W+'tr')
        if not rows:
            continue
        head=norm(txt(rows[0])).lower()
        if 'prescribed' not in head or 'regimen' not in head or 'purpose' not in head:
            continue
        for ri,row in enumerate(rows[1:],1):
            loc=f'medicine_table[{ti}]/row[{ri}]'
            if not norm(txt(row)):
                add('unused_medicine_row',loc,'error')
            for ci,cell in enumerate(row.findall(W+'tc')):
                if not norm(txt(cell)):
                    continue
                va=cell.find('w:tcPr/w:vAlign',NS)
                if va is None or va.get(W+'val')!='top':
                    add('populated_medicine_cell_not_explicit_top',loc+f'/cell[{ci}]')
    return {'status':'review_required' if findings else 'automated_checks_clear',
            'changed_paragraphs_checked':changed,'findings':findings,
            'limitations':['Not clinical approval or a privacy guarantee.',
            'Changed-text heuristic can miss reused sample text and flags unchanged labels in changed paragraphs.',
            'Inherited styles, all populated cells, medicine coverage and protected pre-feedback blocks require manual review.',
            'Visual rendering of every page and cross-report clinical reconciliation remain mandatory.']}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('template'); ap.add_argument('report')
    ap.add_argument('--kind',choices=ANCHORS,required=True)
    args=ap.parse_args()
    try:
        result=audit(args.template,args.report,args.kind)
    except (OSError,KeyError,ValueError,ET.ParseError,BadZipFile):
        print(json.dumps({'status':'invalid_input','error':'Cannot read a valid Word OOXML document pair.'}))
        return 2
    print(json.dumps(result,indent=2))
    return 1 if result['findings'] else 0
if __name__=='__main__':
    sys.exit(main())
