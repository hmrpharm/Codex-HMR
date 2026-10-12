# Validation guide

Use Python 3.9+; the checker has no third-party dependencies. It reads only the two specified DOCX files, makes no edits and uses no network. Output contains structural locations rather than patient text; keep results in the patient workspace, never in the skill package.

`python3 scripts/validate_docx.py original.docx completed.docx --kind dmmr`

Use `--kind hmr` for the other template. Exit 0 means automated checks are clear; exit 1 means findings require review; exit 2 means input is invalid. A clean result is never approval to skip clinical or visual QA.

## Automated coverage

- Valid ZIP/XML input; exact feedback suffix comparison from the known template anchor, ignoring revision-session attributes only.
- Section properties compared, plus original header/footer/media byte changes flagged for inspection.
- Tracked changes and comments flagged; common placeholder instructions detected.
- Text-changed paragraphs checked for explicit left alignment; their text runs checked for explicit Montserrat/10 pt/black, regular formatting, highlight and run shading.
- Recognised medicine-table data rows checked for wholly empty rows and top cell alignment.

The validator intentionally does not repair anything. Formatting findings in an unchanged structural label embedded in a changed paragraph can be false positives. A font inherited correctly can also be flagged; inspect effective formatting and rendered output. Repeated old text may evade changed-text detection. Explicit regular formatting should set bold/italic false and underline false; remove theme font/colour overrides and inspect paragraph/character styles and complex-script settings. No tool here certifies the absence of patient data.

## Mandatory human/agent review

Follow qa.md in full. Check every medicine against source, actual use and purpose separately, chronology, cessation authority, all additional medicines, all photographs/letters and clinically material uncertainty. Check both reports against one internal reconciliation and recommendation set; do not compare template prose mechanically as a substitute.

Inspect all editable areas for leftover sample facts, names, dates, drugs, directions, unsupported normal findings and unused alternatives. Inspect text boxes, headers, footers, comments, revisions, document properties, hyperlinks and embedded material where relevant. Do not include working-source data in the reusable package.

Compare pre-feedback disclaimer, GP decision cells, signature/date/return and follow-up blocks with the originals, allowing only expressly authorised field completions. Confirm all GP boxes, feedback and signatures remain unfilled. Preserve original intentional whitespace. The automatic suffix check does not cover these earlier blocks.

Render both latest DOCX outputs and inspect every page for font substitution, wrapping, clipping, overlap, split headings, empty medicine pages and protected form layout. Use the available document skill's renderer and bundled runtime; do not substitute a user's desktop application if the runtime rules prohibit it. If rendering is unavailable or Montserrat cannot be rendered reliably, state that validation is incomplete and retain local files for correction.

## Script self-test

`python3 scripts/test_validate_docx.py`

Tests use wholly synthetic OOXML fixtures in a temporary directory: intact/altered feedback, invalid DOCX input, correctly styled changed text, incorrect formatting, and unused medicine rows. They do not contain patient records. These fixtures test lint logic, not Word rendering.
