# Install and use

Extract the archive. Copy the `codex-hmr` folder into your Codex skills directory (normally `~/.codex/skills/`). Keep `SKILL.md`, `references/`, `scripts/` and `agents/` together. If a skill with that name already exists, retain its previous version before replacing it. Start a new chat if needed for skill discovery.

Invoke `$codex-hmr` with the selected patient's referral, interview and available supporting sources. Provide the patient identity and any known dates; do not place those files inside the installed skill. The workflow retrieves the current approved master prompt and both Word originals from the restricted Google Drive folders, produces exactly two final DOCX reports, checks them and saves them to the verified patient folder. It leaves all GP decisions, signatures and feedback unfilled.

Required capabilities: connected Google Drive with access to the approved folders and patient-report destination; a DOCX editing/rendering runtime; Montserrat; access to current appropriate clinical references. Validation scripts require Python 3.9+ only. The skill contains workflow instructions and a read-only validator, not an autonomous prescribing engine or a standalone report-generation application. It does not select a model automatically.

Example request:

> Use $codex-hmr for the patient in my attached referral and interview. Retrieve the current approved prompt and original templates, complete both reports, perform clinical and visual QA, and upload them to the correct Patient Reports folder.

The package was built against the October 2026 approved master prompt, retrieved on 11 October 2026. Its clinical and formatting requirements are retained across the linked references. Original template binaries and patient examples are excluded to keep the reusable package free of patient data. Template IDs, source folder IDs and inspection hashes are included; live access or explicitly uploaded approved originals are required at use time.

Run `python3 scripts/test_validate_docx.py` from this folder to check the portable validator. Follow `references/validation-guide.md` for report checks and limitations. Automated checks do not replace clinical review or inspection of both rendered documents.
